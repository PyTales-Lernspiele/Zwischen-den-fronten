package de.pytales.zdf.audio

import javax.sound.sampled.AudioFormat
import javax.sound.sampled.AudioSystem
import javax.sound.sampled.DataLine
import javax.sound.sampled.SourceDataLine
import kotlin.concurrent.thread

actual fun erstellePlattformAudioAusgabe(): AudioAusgabe = DesktopAudioAusgabe()

/**
 * Dezente Desktop-JVM-Audio-Ausgabe über `javax.sound.sampled`.
 *
 * - Arbeitet auf einem leichtgewichtigen Daemon-Thread ohne externe Sounddateien.
 * - Bei `stoppe()` oder `AudioSpur.STILLE` wird die Ausgabe unverzüglich geleert und beendet
 *   (wichtig für die harte Musiksperre an Front & Etappe).
 * - Fängt Headless-/Container-Umgebungen ohne Soundkarte lautlos ab.
 */
private class DesktopAudioAusgabe : AudioAusgabe {

    private val lock = Any()
    @Volatile
    private var aktiv = false
    @Volatile
    private var aktuelleSpur: AudioSpur = AudioSpur.STILLE
    @Volatile
    private var aktuelleLautstaerke: Float = 0f

    private var workerThread: Thread? = null
    private var line: SourceDataLine? = null

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
                name = "zdf-archiv-audio",
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
            schliesseLine()
        }
    }

    override fun freigeben() {
        stoppe()
        synchronized(lock) {
            workerThread = null
        }
    }

    private fun schleifeAbspielen() {
        val format = AudioFormat(
            RuhigeArchivSynthese.SAMPLE_RATE.toFloat(),
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
            synchronized(lock) { aktiv = false }
            return
        }

        synchronized(lock) {
            if (!aktiv) {
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
}
