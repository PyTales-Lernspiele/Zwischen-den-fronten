package de.pytales.zdf.audio

import java.util.concurrent.LinkedBlockingQueue
import java.util.concurrent.TimeUnit
import javax.sound.sampled.AudioFormat
import javax.sound.sampled.AudioSystem
import javax.sound.sampled.DataLine
import javax.sound.sampled.SourceDataLine
import kotlin.concurrent.thread

actual fun erstellePlattformAudioAusgabe(): AudioAusgabe = DesktopAudioAusgabe()

/**
 * Dezente Desktop-JVM-Audio-Ausgabe über `javax.sound.sampled`:
 * - Spielt getragene Kammermusik auf einem leichtgewichtigen Daemon-Thread mit weichem
 *   120-ms-Einblenden beim Spurwechsel.
 * - Spielt kurze, taktile Soundeffekte über eine eigene schlanke Daemon-Warteschlange.
 * - Beendet die Ausgabe bei `stoppe()` oder `AudioSpur.STILLE` unverzüglich (wichtig für
 *   die harte Musiksperre an Front & Etappe).
 * - Fängt Headless-/Container-Umgebungen ohne Soundkarte lautlos ab.
 */
private class DesktopAudioAusgabe : AudioAusgabe {

    private data class SfxAuftrag(
        val effekt: SoundEffekt,
        val lautstaerke: Float,
    )

    private val lock = Any()
    private val sfxLock = Any()

    @Volatile
    private var aktiv = false

    @Volatile
    private var freigegeben = false

    @Volatile
    private var aktuelleSession: Long = 0L

    @Volatile
    private var aktuelleSpur: AudioSpur = AudioSpur.STILLE

    @Volatile
    private var aktuelleLautstaerke: Float = 0f

    private var workerThread: Thread? = null
    private var line: SourceDataLine? = null

    private val sfxQueue = LinkedBlockingQueue<SfxAuftrag>(3)
    private var sfxThread: Thread? = null
    private var sfxLine: SourceDataLine? = null

    override fun aktualisiere(spur: AudioSpur, lautstaerke: Float) {
        val begrenzt = AudioRegelwerk.begrenzeLautstaerke(lautstaerke)
        if (freigegeben || spur == AudioSpur.STILLE || begrenzt <= 0f) {
            stoppe()
            return
        }
        synchronized(lock) {
            if (freigegeben) return
            val spurGewechselt = aktuelleSpur != spur
            aktuelleSpur = spur
            aktuelleLautstaerke = begrenzt
            if (aktiv && workerThread?.isAlive == true && !spurGewechselt) {
                return
            }
            if (spurGewechselt) {
                schliesseLine()
            }
            aktiv = true
            val session = ++aktuelleSession
            workerThread = thread(
                start = true,
                isDaemon = true,
                name = "zdf-archiv-audio",
            ) {
                schleifeAbspielen(session, spur)
            }
        }
    }

    override fun spieleEffekt(effekt: SoundEffekt, lautstaerke: Float) {
        val begrenzt = AudioRegelwerk.begrenzeLautstaerke(lautstaerke)
        if (freigegeben || begrenzt <= 0f) return
        synchronized(sfxLock) {
            if (freigegeben) return
            while (sfxQueue.size >= 2) {
                sfxQueue.poll()
            }
            sfxQueue.offer(SfxAuftrag(effekt, begrenzt))
            if (sfxThread?.isAlive != true) {
                sfxThread = thread(
                    start = true,
                    isDaemon = true,
                    name = "zdf-archiv-sfx",
                ) {
                    sfxSchleife()
                }
            }
        }
    }

    override fun stoppe() {
        synchronized(lock) {
            aktiv = false
            aktuelleSession++
            aktuelleSpur = AudioSpur.STILLE
            aktuelleLautstaerke = 0f
            schliesseLine()
        }
    }

    override fun freigeben() {
        freigegeben = true
        stoppe()
        synchronized(sfxLock) {
            sfxQueue.clear()
            schliesseSfxLine()
            sfxThread = null
        }
        synchronized(lock) {
            workerThread = null
        }
    }

    private fun schleifeAbspielen(session: Long, zielSpur: AudioSpur) {
        val sampleRate = RuhigeArchivSynthese.SAMPLE_RATE
        val format = AudioFormat(
            sampleRate.toFloat(),
            16,
            1,
            true,
            false,
        )
        val info = DataLine.Info(SourceDataLine::class.java, format)
        val lokaleLine = try {
            if (!AudioSystem.isLineSupported(info)) return
            (AudioSystem.getLine(info) as SourceDataLine).apply {
                open(format, 4096)
                start()
            }
        } catch (_: Throwable) {
            synchronized(lock) {
                if (aktuelleSession == session) aktiv = false
            }
            return
        }

        synchronized(lock) {
            if (!aktiv || aktuelleSession != session) {
                runCatching {
                    lokaleLine.stop()
                    lokaleLine.close()
                }
                return
            }
            line = lokaleLine
        }

        val puffer = ByteArray(2048)
        var sampleIndex = 0L
        val einblendSamples = (sampleRate * 0.12).toLong().coerceAtLeast(1L)
        try {
            while (aktiv && aktuelleSession == session) {
                val spur = aktuelleSpur
                val pegel = aktuelleLautstaerke
                if (spur != zielSpur || spur == AudioSpur.STILLE || pegel <= 0f) {
                    break
                }
                RuhigeArchivSynthese.fuellePcm16Puffer(
                    spur = spur,
                    lautstaerke = pegel,
                    startSampleIndex = sampleIndex,
                    ziel = puffer,
                )
                if (sampleIndex < einblendSamples) {
                    wendeEinblendRampeAn(puffer, sampleIndex, einblendSamples)
                }
                sampleIndex += puffer.size / 2
                lokaleLine.write(puffer, 0, puffer.size)
            }
        } catch (_: Throwable) {
            // Line wurde beim Stoppen geschlossen oder Audiogerät entfernt
        } finally {
            synchronized(lock) {
                if (line === lokaleLine) {
                    line = null
                }
            }
            runCatching {
                lokaleLine.stop()
                lokaleLine.flush()
                lokaleLine.close()
            }
        }
    }

    private fun sfxSchleife() {
        val format = AudioFormat(
            ArchivSfxSynthese.SAMPLE_RATE.toFloat(),
            16,
            1,
            true,
            false,
        )
        val info = DataLine.Info(SourceDataLine::class.java, format)
        if (!runCatching { AudioSystem.isLineSupported(info) }.getOrDefault(false)) return

        while (!freigegeben) {
            val auftrag = try {
                sfxQueue.poll(3L, TimeUnit.SECONDS)
            } catch (_: InterruptedException) {
                break
            } ?: break

            if (freigegeben) break

            val pcm = ArchivSfxSynthese.erzeugePcm16(auftrag.effekt, auftrag.lautstaerke)
            if (pcm.isEmpty()) continue

            val lokaleSfxLine = try {
                (AudioSystem.getLine(info) as SourceDataLine).apply {
                    open(format, maxOf(2048, minOf(pcm.size, 8192)))
                    start()
                }
            } catch (_: Throwable) {
                continue
            }

            synchronized(sfxLock) {
                schliesseSfxLine()
                if (freigegeben) {
                    runCatching { lokaleSfxLine.close() }
                    return
                }
                sfxLine = lokaleSfxLine
            }

            try {
                lokaleSfxLine.write(pcm, 0, pcm.size)
                lokaleSfxLine.drain()
            } catch (_: Throwable) {
                // Line beim Stoppen/Schließen unterbrochen
            } finally {
                synchronized(sfxLock) {
                    if (sfxLine === lokaleSfxLine) {
                        sfxLine = null
                    }
                }
                runCatching {
                    lokaleSfxLine.stop()
                    lokaleSfxLine.flush()
                    lokaleSfxLine.close()
                }
            }
        }
    }

    private fun wendeEinblendRampeAn(
        puffer: ByteArray,
        startSampleIndex: Long,
        einblendSamples: Long,
    ) {
        val sampleAnzahl = puffer.size / 2
        for (i in 0 until sampleAnzahl) {
            val pos = startSampleIndex + i
            if (pos >= einblendSamples) break
            val faktor = pos.toDouble() / einblendSamples.toDouble()
            val idx = i * 2
            val lo = puffer[idx].toInt() and 0xFF
            val hi = puffer[idx + 1].toInt() shl 8
            val alt = (hi or lo).toShort().toInt()
            val neu = (alt * faktor).toInt()
            puffer[idx] = (neu and 0xFF).toByte()
            puffer[idx + 1] = ((neu ushr 8) and 0xFF).toByte()
        }
    }

    private fun schliesseLine() {
        val aktuell = line
        line = null
        if (aktuell != null) {
            runCatching {
                aktuell.stop()
                aktuell.flush()
                aktuell.close()
            }
        }
    }

    private fun schliesseSfxLine() {
        val aktuell = sfxLine
        sfxLine = null
        if (aktuell != null) {
            runCatching {
                aktuell.stop()
                aktuell.flush()
                aktuell.close()
            }
        }
    }
}
