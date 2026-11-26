package de.pytales.zdf.audio

import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import kotlin.concurrent.thread

actual fun erstellePlattformAudioAusgabe(): AudioAusgabe = AndroidAudioAusgabe()

/**
 * Synchroner Android-Lebenszyklus-Schutz für die [AudioTrack]-Ausgabe:
 * Wird direkt aus `MainActivity.onPause()` / `onStop()` aufgerufen, damit optionales Audio
 * beim Wechsel in den Hintergrund (oder in Druck-/Teilen-Dialoge) sofort ohne Verzögerung
 * gestoppt wird — noch bevor Compose einen weiteren Frame verarbeitet.
 */
object AndroidAudioLebenszyklus {
    private val lock = Any()
    private val aktiveAusgaben = mutableSetOf<AndroidAudioAusgabe>()

    @Volatile
    var imHintergrund: Boolean = false
        private set

    internal fun registriere(ausgabe: AndroidAudioAusgabe) {
        synchronized(lock) {
            aktiveAusgaben += ausgabe
        }
    }

    internal fun entferne(ausgabe: AndroidAudioAusgabe) {
        synchronized(lock) {
            aktiveAusgaben -= ausgabe
        }
    }

    fun onVordergrund() {
        synchronized(lock) {
            imHintergrund = false
        }
    }

    fun onHintergrund() {
        val kopie = synchronized(lock) {
            imHintergrund = true
            aktiveAusgaben.toList()
        }
        kopie.forEach { it.stoppe() }
    }
}

/**
 * Dezente Android-Audio-Ausgabe über [AudioTrack] (`MODE_STREAM`, 16-Bit-PCM mono).
 * Beendet die Wiedergabe sofort bei [stoppe] (harte Musiksperre an Front & Etappe sowie
 * Hintergrundwechsel über [AndroidAudioLebenszyklus]).
 */
internal class AndroidAudioAusgabe : AudioAusgabe {

    private val lock = Any()
    @Volatile
    private var aktiv = false
    @Volatile
    private var aktuelleSession: Long = 0L
    @Volatile
    private var aktuelleSpur: AudioSpur = AudioSpur.STILLE
    @Volatile
    private var aktuelleLautstaerke: Float = 0f

    private var workerThread: Thread? = null
    private var track: AudioTrack? = null

    init {
        AndroidAudioLebenszyklus.registriere(this)
    }

    override fun aktualisiere(spur: AudioSpur, lautstaerke: Float) {
        val begrenzt = AudioRegelwerk.begrenzeLautstaerke(lautstaerke)
        if (AndroidAudioLebenszyklus.imHintergrund || spur == AudioSpur.STILLE || begrenzt <= 0f) {
            stoppe()
            return
        }
        synchronized(lock) {
            if (AndroidAudioLebenszyklus.imHintergrund) {
                aktiv = false
                aktuelleSession++
                aktuelleSpur = AudioSpur.STILLE
                aktuelleLautstaerke = 0f
                schliesseTrack()
                return
            }
            aktuelleSpur = spur
            aktuelleLautstaerke = begrenzt
            if (aktiv && workerThread?.isAlive == true) {
                return
            }
            aktiv = true
            val session = ++aktuelleSession
            workerThread = thread(
                start = true,
                isDaemon = true,
                name = "zdf-android-audio",
            ) {
                schleifeAbspielen(session)
            }
        }
    }

    override fun stoppe() {
        synchronized(lock) {
            aktiv = false
            aktuelleSession++
            aktuelleSpur = AudioSpur.STILLE
            aktuelleLautstaerke = 0f
            schliesseTrack()
        }
    }

    override fun freigeben() {
        stoppe()
        AndroidAudioLebenszyklus.entferne(this)
        synchronized(lock) {
            workerThread = null
        }
    }

    private fun schleifeAbspielen(session: Long) {
        val sampleRate = RuhigeArchivSynthese.SAMPLE_RATE
        val minPuffer = AudioTrack.getMinBufferSize(
            sampleRate,
            AudioFormat.CHANNEL_OUT_MONO,
            AudioFormat.ENCODING_PCM_16BIT,
        )
        if (minPuffer <= 0) {
            synchronized(lock) {
                if (aktuelleSession == session) aktiv = false
            }
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
            synchronized(lock) {
                if (aktuelleSession == session) aktiv = false
            }
            return
        }

        synchronized(lock) {
            if (!aktiv || aktuelleSession != session || AndroidAudioLebenszyklus.imHintergrund) {
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
            while (aktiv && aktuelleSession == session && !AndroidAudioLebenszyklus.imHintergrund) {
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
