package de.pytales.zdf.audio

import java.util.concurrent.Executors
import javax.sound.sampled.AudioFormat
import javax.sound.sampled.AudioSystem
import javax.sound.sampled.DataLine
import javax.sound.sampled.SourceDataLine

actual fun erstellePlattformKlangAusgabe(): KlangAusgabe = DesktopKlangAusgabe()

/**
 * Desktop-Klangeffekte über `javax.sound.sampled` auf einem eigenen Daemon-Thread.
 * Fängt Headless-/Container-Umgebungen ohne Soundkarte lautlos ab.
 */
private class DesktopKlangAusgabe : KlangAusgabe {

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
        if (freigegeben) return
        val pcm = synchronized(klaenge) { klaenge[klang] } ?: return
        val daten = pcm.alsPcm16Bytes(lautstaerke)
        runCatching {
            ausfuehrer.execute {
                runCatching {
                    val format = AudioFormat(pcm.abtastrate.toFloat(), 16, 1, true, false)
                    val info = DataLine.Info(SourceDataLine::class.java, format)
                    if (!AudioSystem.isLineSupported(info)) return@runCatching
                    val line = AudioSystem.getLine(info) as SourceDataLine
                    line.open(format)
                    line.start()
                    line.write(daten, 0, daten.size)
                    line.drain()
                    line.stop()
                    line.close()
                }
            }
        }
    }

    override fun freigeben() {
        freigegeben = true
        ausfuehrer.shutdownNow()
    }
}
