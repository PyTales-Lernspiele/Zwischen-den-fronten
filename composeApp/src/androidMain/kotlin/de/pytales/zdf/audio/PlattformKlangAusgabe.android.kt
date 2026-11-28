package de.pytales.zdf.audio

import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import java.util.concurrent.Executors

actual fun erstellePlattformKlangAusgabe(): KlangAusgabe = AndroidKlangAusgabe()

/**
 * Android-Klangeffekte über kurze statische [AudioTrack]s (`MODE_STATIC`, 16-Bit-PCM mono).
 * Im Hintergrund ([AndroidAudioLebenszyklus.imHintergrund]) wird nichts abgespielt.
 */
private class AndroidKlangAusgabe : KlangAusgabe {

    override val brauchtRohdaten: Boolean = true

    private val klaenge = mutableMapOf<Klang, PcmKlang>()
    private val ausfuehrer = Executors.newSingleThreadExecutor { r ->
        Thread(r, "zdf-klangeffekte").apply { isDaemon = true }
    }

    @Volatile
    private var freigegeben = false

    override fun lade(klang: Klang, rohdaten: ByteArray?, uri: String?) {
        val pcm = rohdaten?.let { WavDekoder.dekodiere(it) } ?: return
        synchronized(klaenge) { klaenge[klang] = pcm }
    }

    override fun spiele(klang: Klang, lautstaerke: Float) {
        if (freigegeben || AndroidAudioLebenszyklus.imHintergrund) return
        val pcm = synchronized(klaenge) { klaenge[klang] } ?: return
        runCatching {
            ausfuehrer.execute { spieleJetzt(pcm, lautstaerke) }
        }
    }

    private fun spieleJetzt(pcm: PcmKlang, lautstaerke: Float) {
        runCatching {
            val samples = pcm.skaliert(lautstaerke)
            val track = AudioTrack.Builder()
                .setAudioAttributes(
                    AudioAttributes.Builder()
                        .setUsage(AudioAttributes.USAGE_GAME)
                        .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                        .build(),
                )
                .setAudioFormat(
                    AudioFormat.Builder()
                        .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                        .setSampleRate(pcm.abtastrate)
                        .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                        .build(),
                )
                .setBufferSizeInBytes(samples.size * 2)
                .setTransferMode(AudioTrack.MODE_STATIC)
                .build()
            track.write(samples, 0, samples.size)
            track.play()
            // Statischen Track nach dem Abspielen wieder freigeben
            Thread.sleep((pcm.dauerSekunden * 1000).toLong() + 120L)
            runCatching {
                track.stop()
                track.release()
            }
        }
    }

    override fun freigeben() {
        freigegeben = true
        ausfuehrer.shutdownNow()
    }
}
