package de.pytales.zdf.audio

import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import java.util.concurrent.LinkedBlockingQueue
import java.util.concurrent.TimeUnit
import kotlin.concurrent.thread

actual fun erstellePlattformAudioAusgabe(): AudioAusgabe = AndroidAudioAusgabe()

/**
 * Synchroner Android-Lebenszyklus-Schutz für die [AudioTrack]-Ausgabe:
 * Wird direkt aus `MainActivity.onPause()` / `onStop()` aufgerufen, damit Grundmusik und
 * Soundeffekte beim Wechsel in den Hintergrund (oder in Druck-/Teilen-Dialoge) sofort ohne
 * Verzögerung gestoppt werden — noch bevor Compose einen weiteren Frame verarbeitet.
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
        kopie.forEach { it.stoppeAlles() }
    }
}

/**
 * Dezente Android-Audio-Ausgabe über [AudioTrack] (16-Bit-PCM mono):
 * - Getragene Kammermusik (`MODE_STREAM`) mit weichem 120-ms-Einblenden beim Spurwechsel.
 * - Kurze, taktile Soundeffekte (`MODE_STATIC` über leichtgewichtige Einzel-Worker-Warteschlange).
 * - Beendet die Wiedergabe sofort bei [stoppe] (harte Musiksperre an Front & Etappe sowie
 *   Hintergrundwechsel über [AndroidAudioLebenszyklus]).
 */
internal class AndroidAudioAusgabe : AudioAusgabe {

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
    private var track: AudioTrack? = null

    private val sfxQueue = LinkedBlockingQueue<SfxAuftrag>(3)
    private var sfxThread: Thread? = null
    private var aktiverSfxTrack: AudioTrack? = null

    init {
        AndroidAudioLebenszyklus.registriere(this)
    }

    override fun aktualisiere(spur: AudioSpur, lautstaerke: Float) {
        val begrenzt = AudioRegelwerk.begrenzeLautstaerke(lautstaerke)
        if (freigegeben || AndroidAudioLebenszyklus.imHintergrund || spur == AudioSpur.STILLE || begrenzt <= 0f) {
            stoppe()
            return
        }
        synchronized(lock) {
            if (freigegeben || AndroidAudioLebenszyklus.imHintergrund) {
                beendeMusikGesperrt()
                return
            }
            val spurGewechselt = aktuelleSpur != spur
            aktuelleSpur = spur
            aktuelleLautstaerke = begrenzt
            if (aktiv && workerThread?.isAlive == true && !spurGewechselt) {
                return
            }
            if (spurGewechselt) {
                schliesseTrack()
            }
            aktiv = true
            val session = ++aktuelleSession
            workerThread = thread(
                start = true,
                isDaemon = true,
                name = "zdf-android-audio",
            ) {
                schleifeAbspielen(session, spur)
            }
        }
    }

    override fun spieleEffekt(effekt: SoundEffekt, lautstaerke: Float) {
        val begrenzt = AudioRegelwerk.begrenzeLautstaerke(lautstaerke)
        if (freigegeben || AndroidAudioLebenszyklus.imHintergrund || begrenzt <= 0f) return
        synchronized(sfxLock) {
            if (freigegeben || AndroidAudioLebenszyklus.imHintergrund) return
            while (sfxQueue.size >= 2) {
                sfxQueue.poll()
            }
            sfxQueue.offer(SfxAuftrag(effekt, begrenzt))
            if (sfxThread?.isAlive != true) {
                sfxThread = thread(
                    start = true,
                    isDaemon = true,
                    name = "zdf-android-sfx",
                ) {
                    sfxSchleife()
                }
            }
        }
    }

    override fun stoppe() {
        synchronized(lock) {
            beendeMusikGesperrt()
        }
    }

    internal fun stoppeAlles() {
        stoppe()
        synchronized(sfxLock) {
            sfxQueue.clear()
            schliesseSfxTrack()
        }
    }

    override fun freigeben() {
        freigegeben = true
        stoppeAlles()
        AndroidAudioLebenszyklus.entferne(this)
        synchronized(lock) {
            workerThread = null
        }
        synchronized(sfxLock) {
            sfxThread = null
        }
    }

    private fun beendeMusikGesperrt() {
        aktiv = false
        aktuelleSession++
        aktuelleSpur = AudioSpur.STILLE
        aktuelleLautstaerke = 0f
        schliesseTrack()
    }

    private fun schleifeAbspielen(session: Long, zielSpur: AudioSpur) {
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
        val einblendSamples = (sampleRate * 0.12).toLong().coerceAtLeast(1L)
        try {
            while (aktiv && aktuelleSession == session && !AndroidAudioLebenszyklus.imHintergrund) {
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

    private fun sfxSchleife() {
        val sampleRate = ArchivSfxSynthese.SAMPLE_RATE
        val minPuffer = runCatching {
            AudioTrack.getMinBufferSize(
                sampleRate,
                AudioFormat.CHANNEL_OUT_MONO,
                AudioFormat.ENCODING_PCM_16BIT,
            )
        }.getOrDefault(-1)
        if (minPuffer <= 0) return

        while (!freigegeben) {
            val auftrag = try {
                sfxQueue.poll(3L, TimeUnit.SECONDS)
            } catch (_: InterruptedException) {
                break
            } ?: break

            if (freigegeben || AndroidAudioLebenszyklus.imHintergrund) break

            val rohPcm = ArchivSfxSynthese.erzeugePcm16(auftrag.effekt, auftrag.lautstaerke)
            if (rohPcm.isEmpty()) continue

            val pufferGroesse = maxOf(rohPcm.size, minPuffer)
            val gepolstert = if (rohPcm.size < pufferGroesse) {
                ByteArray(pufferGroesse).also { rohPcm.copyInto(it) }
            } else {
                rohPcm
            }

            val sfxTrack = try {
                AudioTrack.Builder()
                    .setAudioAttributes(
                        AudioAttributes.Builder()
                            .setUsage(AudioAttributes.USAGE_ASSISTANCE_SONIFICATION)
                            .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                            .build(),
                    )
                    .setAudioFormat(
                        AudioFormat.Builder()
                            .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                            .setSampleRate(sampleRate)
                            .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                            .build(),
                    )
                    .setBufferSizeInBytes(pufferGroesse)
                    .setTransferMode(AudioTrack.MODE_STATIC)
                    .build()
            } catch (_: Throwable) {
                continue
            }

            synchronized(sfxLock) {
                schliesseSfxTrack()
                if (freigegeben || AndroidAudioLebenszyklus.imHintergrund) {
                    runCatching { sfxTrack.release() }
                    return
                }
                aktiverSfxTrack = sfxTrack
            }

            try {
                val geschrieben = sfxTrack.write(gepolstert, 0, gepolstert.size)
                if (geschrieben > 0 && !freigegeben && !AndroidAudioLebenszyklus.imHintergrund) {
                    sfxTrack.play()
                    val warteMs = (ArchivSfxSynthese.dauerMsFuer(auftrag.effekt) + 35).toLong()
                    var vergangen = 0L
                    while (vergangen < warteMs && !freigegeben && !AndroidAudioLebenszyklus.imHintergrund && sfxQueue.isEmpty()) {
                        Thread.sleep(20L)
                        vergangen += 20L
                    }
                }
            } catch (_: Throwable) {
                // Track wurde vorzeitig beendet
            } finally {
                synchronized(sfxLock) {
                    if (aktiverSfxTrack === sfxTrack) {
                        aktiverSfxTrack = null
                    }
                }
                runCatching {
                    sfxTrack.pause()
                    sfxTrack.flush()
                    sfxTrack.stop()
                    sfxTrack.release()
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

    private fun schliesseSfxTrack() {
        val aktuell = aktiverSfxTrack
        aktiverSfxTrack = null
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
