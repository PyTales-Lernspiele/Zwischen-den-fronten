package de.pytales.zdf.audio

import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import kotlin.concurrent.thread

actual fun erstellePlattformAudioAusgabe(): AudioAusgabe = AndroidAudioAusgabe()

/**
 * Dezente Android-Audio-Ausgabe über [AudioTrack] (`MODE_STREAM`, 16-Bit-PCM mono).
 * Beendet die Wiedergabe sofort bei [stoppe] (harte Musiksperre an Front & Etappe).
 */
private class AndroidAudioAusgabe : AudioAusgabe {

    private val lock = Any()
    @Volatile
    private var aktiv = false
    @Volatile
    private var aktuelleSpur: AudioSpur = AudioSpur.STILLE
    @Volatile
    private var aktuelleLautstaerke: Float = 0f

    private var workerThread: Thread? = null
    private var track: AudioTrack? = null

    override fun aktualisiere(spur: AudioSpur, lautstaerke: Float) {
        val begrenzt = AudioRegelwerk.begrenzeLautstaerke(lautstaerke)
        if (spur == AudioSpur.STILLE || begrenzt <= 0f) {
            stoppe()
            return
        }
        synchronized(lock) {
            aktuelleSpur = spur
            aktuelleLautstaerke = begrenzt
            if (aktiv && workerThread?.isAlive == true) {
                return
            }
            aktiv = true
            workerThread = thread(
                start = true,
                isDaemon = true,
                name = "zdf-android-audio",
            ) {
                schleifeAbspielen()
            }
        }
    }

    override fun stoppe() {
        synchronized(lock) {
            aktiv = false
            aktuelleSpur = AudioSpur.STILLE
            aktuelleLautstaerke = 0f
            schliesseTrack()
        }
    }

    override fun freigeben() {
        stoppe()
        synchronized(lock) {
            workerThread = null
        }
    }

    private fun schleifeAbspielen() {
        val sampleRate = RuhigeArchivSynthese.SAMPLE_RATE
        val minPuffer = AudioTrack.getMinBufferSize(
            sampleRate,
            AudioFormat.CHANNEL_OUT_MONO,
            AudioFormat.ENCODING_PCM_16BIT,
        )
        if (minPuffer <= 0) {
            synchronized(lock) { aktiv = false }
            return
        }

        val lokalerTrack = try {
            AudioTrack.Builder()
                .setAudioAttributes(
                    AudioAttributes.Builder()
                        .setUsage(AudioAttributes.USAGE_GAME)
                        .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                        .build(),
                )
                .setAudioFormat(
                    AudioFormat.Builder()
                        .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                        .setSampleRate(sampleRate)
                        .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                        .build(),
                )
                .setBufferSizeInBytes(maxOf(minPuffer, 4096))
                .setTransferMode(AudioTrack.MODE_STREAM)
                .build()
                .apply { play() }
        } catch (_: Throwable) {
            synchronized(lock) { aktiv = false }
            return
        }

        synchronized(lock) {
            if (!aktiv) {
                runCatching {
                    lokalerTrack.stop()
                    lokalerTrack.release()
                }
                return
            }
            track = lokalerTrack
        }

        val puffer = ByteArray(2048)
        var sampleIndex = 0L
        try {
            while (aktiv) {
                val spur = aktuelleSpur
                val pegel = aktuelleLautstaerke
                if (spur == AudioSpur.STILLE || pegel <= 0f) {
                    break
                }
                RuhigeArchivSynthese.fuellePcm16Puffer(
                    spur = spur,
                    lautstaerke = pegel,
                    startSampleIndex = sampleIndex,
                    ziel = puffer,
                )
                sampleIndex += puffer.size / 2
                val geschrieben = lokalerTrack.write(puffer, 0, puffer.size)
                if (geschrieben < 0) break
            }
        } catch (_: Throwable) {
            // AudioTrack wurde beim Stoppen freigegeben
        } finally {
            synchronized(lock) {
                if (track === lokalerTrack) {
                    track = null
                }
            }
            runCatching {
                lokalerTrack.pause()
                lokalerTrack.flush()
                lokalerTrack.stop()
                lokalerTrack.release()
            }
        }
    }

    private fun schliesseTrack() {
        val aktuell = track
        track = null
        if (aktuell != null) {
            runCatching {
                aktuell.pause()
                aktuell.flush()
                aktuell.stop()
                aktuell.release()
            }
        }
    }
}
