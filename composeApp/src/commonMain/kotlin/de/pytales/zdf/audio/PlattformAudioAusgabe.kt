package de.pytales.zdf.audio

import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.exp
import kotlin.math.min
import kotlin.math.pow
import kotlin.math.sin
import kotlin.math.sqrt
import kotlin.math.tanh

/**
 * Plattform-Fabrik für eine dezente, knackfreie Audio-Ausgabe (Android, Desktop JVM, Web).
 * Alle Implementierungen fangen fehlende Hardware oder Browser-Richtlinien lautlos ab.
 */
expect fun erstellePlattformAudioAusgabe(): AudioAusgabe

/**
 * Einzelner gedämpfter Filzklavier-Ton (Felt Piano) innerhalb einer [KammerPartitur].
 */
data class KlavierNote(
    val startSek: Double,
    val dauerSek: Double,
    val midiNote: Int,
    val anschlag: Double,
)

/**
 * Langsamer, getragener Cello-Bogen mit sanftem Ein- und Ausblenden (nie statischer Dauerton).
 */
data class CelloBogen(
    val startSek: Double,
    val dauerSek: Double,
    val midiNote: Int,
    val pegel: Double,
)

/**
 * Zyklische Kammermusik-Partitur (ca. 44–52 Sekunden) mit bewussten Ruhepausen/Atemräumen
 * zwischen den Phrasen.
 */
data class KammerPartitur(
    val dauerSekunden: Double,
    val klavierNoten: List<KlavierNote>,
    val celloBoegen: List<CelloBogen>,
)

/**
 * Reine, offline-fähige Kammermusik-Synthese (16-Bit-PCM) für getragene, bedrückend-melancholische
 * Begleitung ohne externe Audiodateien:
 * - Gedämpftes **Filzklavier (Felt Piano)** mit weichem Anschlag, schnellem Oberton-Abklingen,
 *   leicht verstimmter zweiter Saite und natürlichem Ausklang.
 * - Leise, tiefe **Cello-Bögen** mit langsamer Bogen-Hüllkurve (`sin(π·u)^1.8`) und subtilem Vibrato.
 * - Echte **Ruhepausen / Atemräume** zwischen den Moll-Phrasen — niemals ein statischer Dauerton.
 * - Analytische Tiefpass-Dämpfung und weiche Sättigung (`tanh`) für warmen, knackfreien Klang
 *   auch auf kleinen Smartphone-Lautsprechern.
 *
 * Wird ausschließlich für erlaubte Spuren ([AudioSpur.START_RUHIG], [AudioSpur.HEIMAT_RUHIG],
 * [AudioSpur.EPILOG_RUHIG]) genutzt; [AudioSpur.STILLE] erzeugt ausschließlich Null-Samples.
 */
object RuhigeArchivSynthese {

    const val SAMPLE_RATE: Int = 22_050
    private const val ZWEI_PI: Double = 2.0 * PI

    // -------------------------------------------------------------------------
    // Drei eigenständige, getragene Moll-Kompositionen (44–52 s) mit Ruhepausen
    // -------------------------------------------------------------------------

    /**
     * START_RUHIG — „August 1914 · Schwere Vorahnung“ (d-Moll, 48,0 s)
     * Getragene d-Moll / B-Dur / g-Moll / A7sus4-Motive mit weiten Atempausen.
     */
    private val PARTITUR_START = KammerPartitur(
        dauerSekunden = 48.0,
        klavierNoten = listOf(
            // Phrase 1 (0.0 – 10.6 s): d-Moll — schweres Seufzermotiv
            KlavierNote(0.00, 4.4, 50, 0.70), // D3
            KlavierNote(0.95, 3.8, 57, 0.60), // A3
            KlavierNote(2.35, 3.9, 65, 0.62), // F4
            KlavierNote(4.15, 3.5, 64, 0.54), // E4
            KlavierNote(5.90, 4.6, 62, 0.66), // D4
            KlavierNote(6.05, 4.4, 50, 0.45), // D3
            // Atempause (10.6 – 13.6 s): 3,0 s Ruhe

            // Phrase 2 (13.6 – 24.4 s): B-Dur -> g-Moll — dunkles Absinken
            KlavierNote(13.60, 4.2, 46, 0.64), // Bb2
            KlavierNote(14.55, 3.8, 58, 0.56), // Bb3
            KlavierNote(16.10, 3.6, 62, 0.60), // D4
            KlavierNote(17.85, 3.8, 69, 0.48), // A4 (leise)
            KlavierNote(19.70, 4.5, 67, 0.62), // G4
            KlavierNote(19.90, 4.3, 55, 0.50), // G3
            // Atempause (24.4 – 27.4 s): 3,0 s Ruhe

            // Phrase 3 (27.4 – 37.8 s): g-Moll -> A7sus4 -> A7 (bedrückende Spannung)
            KlavierNote(27.40, 4.0, 55, 0.60), // G3
            KlavierNote(28.80, 3.6, 58, 0.54), // Bb3
            KlavierNote(30.40, 3.8, 62, 0.58), // D4
            KlavierNote(32.20, 4.0, 57, 0.56), // A3
            KlavierNote(33.40, 3.4, 64, 0.52), // E4
            KlavierNote(34.95, 2.8, 61, 0.46), // C#4 (leise moll-dominantisch)
            // Kurzer Atemzug (37.8 – 39.2 s)

            // Phrase 4 (39.2 – 45.2 s): Rückkehr nach d-Moll, dann Ausklang in Stille bis 48.0 s
            KlavierNote(39.20, 4.8, 50, 0.66), // D3
            KlavierNote(40.30, 4.2, 57, 0.52), // A3
            KlavierNote(41.80, 3.4, 65, 0.42), // F4
            KlavierNote(42.20, 3.0, 62, 0.48), // D4
            // Stille (45.2 – 48.0 s): 2,8 s Atemraum vor nahtlosem Loop
        ),
        celloBoegen = listOf(
            CelloBogen(0.40, 9.6, 50, 0.36),  // D3 sanft getragen
            CelloBogen(14.00, 9.8, 46, 0.34), // Bb2
            CelloBogen(27.80, 5.2, 43, 0.32), // G2
            CelloBogen(33.00, 5.4, 45, 0.30), // A2
            CelloBogen(39.40, 5.6, 50, 0.28), // D3 verklingend
        ),
    )

    /**
     * HEIMAT_RUHIG — „Grauer Alltag · Warten und Mangel“ (a-Moll / e-Moll, 52,0 s)
     * Sparsame, bedrückend-nachdenkliche Klavierphrasen mit besonders weiten Pausen zum ruhigen Lesen.
     */
    private val PARTITUR_HEIMAT = KammerPartitur(
        dauerSekunden = 52.0,
        klavierNoten = listOf(
            // Phrase 1 (0.0 – 10.6 s): a-Moll — stilles Tasten
            KlavierNote(0.00, 4.4, 45, 0.64), // A2
            KlavierNote(1.10, 3.9, 64, 0.56), // E4
            KlavierNote(3.10, 3.8, 60, 0.58), // C4
            KlavierNote(5.25, 3.4, 59, 0.50), // B3
            KlavierNote(6.95, 3.6, 57, 0.56), // A3
            // Weite Ruhepause (10.6 – 14.8 s): 4,2 s Stille

            // Phrase 2 (14.8 – 24.8 s): Fmaj7 -> d-Moll — schwerer Alltag
            KlavierNote(14.80, 4.2, 53, 0.58), // F3
            KlavierNote(15.95, 3.8, 57, 0.52), // A3
            KlavierNote(17.70, 3.7, 65, 0.54), // F4
            KlavierNote(19.65, 3.5, 64, 0.48), // E4
            KlavierNote(21.25, 3.5, 62, 0.54), // D4
            // Weite Ruhepause (24.8 – 29.0 s): 4,2 s Stille

            // Phrase 3 (29.0 – 39.2 s): e-Moll -> a-Moll — kühle Melancholie
            KlavierNote(29.00, 4.2, 52, 0.56), // E3
            KlavierNote(30.30, 3.8, 59, 0.50), // B3
            KlavierNote(32.10, 3.6, 67, 0.44), // G4 (sehr zart)
            KlavierNote(34.00, 3.5, 64, 0.50), // E4
            KlavierNote(35.85, 3.3, 62, 0.46), // D4
            // Weite Ruhepause (39.2 – 43.0 s): 3,8 s Stille

            // Phrase 4 (43.0 – 48.8 s): einsames Klavier ohne Cello
            KlavierNote(43.00, 3.6, 62, 0.48), // D4
            KlavierNote(44.55, 3.5, 60, 0.46), // C4
            KlavierNote(46.00, 2.8, 57, 0.50), // A3
            KlavierNote(46.15, 2.6, 52, 0.36), // E3
            // Ruhepause (48.8 – 52.0 s): 3,2 s Stille vor Loop
        ),
        celloBoegen = listOf(
            CelloBogen(0.60, 9.2, 45, 0.32),  // A2
            CelloBogen(15.20, 8.8, 48, 0.28), // C3 (über F3)
            CelloBogen(29.40, 8.6, 43, 0.30), // G2 (dunkel unter e-Moll)
        ),
    )

    /**
     * EPILOG_RUHIG — „1919 · Erschöpfter Ausklang“ (a-Moll / Cmaj7, 44,0 s)
     * Äußerst karg, fragil und leise mit langen Momenten der Stille.
     */
    private val PARTITUR_EPILOG = KammerPartitur(
        dauerSekunden = 44.0,
        klavierNoten = listOf(
            // Phrase 1 (0.0 – 9.8 s): zerbrechliche Einzelnoten
            KlavierNote(0.00, 4.2, 57, 0.52), // A3
            KlavierNote(2.05, 3.8, 59, 0.44), // B3
            KlavierNote(4.15, 3.8, 60, 0.48), // C4
            KlavierNote(6.35, 3.4, 64, 0.40), // E4
            // Lange Stille (9.8 – 14.4 s): 4,6 s

            // Phrase 2 (14.4 – 24.4 s): fragiles Fmaj7
            KlavierNote(14.40, 4.4, 53, 0.48), // F3
            KlavierNote(16.10, 3.9, 60, 0.44), // C4
            KlavierNote(18.50, 3.6, 67, 0.36), // G4 (hauchleise)
            KlavierNote(20.80, 3.6, 64, 0.42), // E4
            // Lange Stille (24.4 – 29.2 s): 4,8 s

            // Phrase 3 (29.2 – 39.6 s): erschöpftes Verklingen
            KlavierNote(29.20, 4.0, 62, 0.46), // D4
            KlavierNote(31.50, 3.8, 60, 0.42), // C4
            KlavierNote(33.85, 3.6, 59, 0.38), // B3
            KlavierNote(35.80, 3.8, 57, 0.44), // A3
            // Lange Stille (39.6 – 44.0 s): 4,4 s vor Loop
        ),
        celloBoegen = listOf(
            CelloBogen(14.80, 8.8, 45, 0.24), // A2 sehr leise
            CelloBogen(30.40, 8.2, 45, 0.22), // A2 hauchdünn verklingend
        ),
    )

    private val PARTITUR_LEER = KammerPartitur(
        dauerSekunden = 1.0,
        klavierNoten = emptyList(),
        celloBoegen = emptyList(),
    )

    /**
     * Liefert die vollständige Kammermusik-Partitur für die jeweilige [AudioSpur].
     */
    fun partiturFuer(spur: AudioSpur): KammerPartitur = when (spur) {
        AudioSpur.STILLE -> PARTITUR_LEER
        AudioSpur.START_RUHIG -> PARTITUR_START
        AudioSpur.HEIMAT_RUHIG -> PARTITUR_HEIMAT
        AudioSpur.EPILOG_RUHIG -> PARTITUR_EPILOG
    }

    /**
     * Charakteristische Grundfrequenzen (Hz) der jeweiligen Moll-Tonart (Referenzwerte).
     */
    fun frequenzenFuer(spur: AudioSpur): DoubleArray = when (spur) {
        AudioSpur.STILLE -> DoubleArray(0)
        AudioSpur.START_RUHIG -> doubleArrayOf(midiZuHz(50), midiZuHz(57), midiZuHz(65))
        AudioSpur.HEIMAT_RUHIG -> doubleArrayOf(midiZuHz(45), midiZuHz(52), midiZuHz(60))
        AudioSpur.EPILOG_RUHIG -> doubleArrayOf(midiZuHz(45), midiZuHz(57), midiZuHz(60))
    }

    fun midiZuHz(midi: Int): Double = 440.0 * 2.0.pow((midi - 69) / 12.0)

    /**
     * Erzeugt einen Puffer mit 16-Bit-Little-Endian-PCM-Samples (mono) der laufenden
     * Kammermusik-Komposition (nahtlos schleifend, warm tiefpass-gedämpft, knackfrei).
     */
    fun fuellePcm16Puffer(
        spur: AudioSpur,
        lautstaerke: Float,
        startSampleIndex: Long,
        ziel: ByteArray,
    ) {
        val begrenzt = AudioRegelwerk.begrenzeLautstaerke(lautstaerke)
        val partitur = partiturFuer(spur)
        if (spur == AudioSpur.STILLE || begrenzt <= 0f || partitur.klavierNoten.isEmpty()) {
            ziel.fill(0)
            return
        }

        val sampleAnzahl = ziel.size / 2
        val zyklus = partitur.dauerSekunden
        val klavier = partitur.klavierNoten
        val cello = partitur.celloBoegen
        // Angenehmer, ruhiger Kammermusik-Pegel (sicher deutlich unter Vollaussteuerung)
        val masterGain = begrenzt.toDouble() * 0.44 * Short.MAX_VALUE

        // Aktivitätsfenster für diesen Block (~46 ms) einmalig vorfiltern -> minimaler CPU-Bedarf
        val tStart = ((startSampleIndex.toDouble() / SAMPLE_RATE.toDouble()) % zyklus + zyklus) % zyklus
        val blockDauer = sampleAnzahl.toDouble() / SAMPLE_RATE.toDouble()
        val aktiveKlavier = klavier.filter { istImBlockAktiv(tStart, blockDauer, it.startSek, it.dauerSek, zyklus) }
        val aktiveCello = cello.filter { istImBlockAktiv(tStart, blockDauer, it.startSek, it.dauerSek, zyklus) }

        if (aktiveKlavier.isEmpty() && aktiveCello.isEmpty()) {
            ziel.fill(0)
            return
        }

        for (i in 0 until sampleAnzahl) {
            val tGesamt = (startSampleIndex + i).toDouble() / SAMPLE_RATE.toDouble()
            val t = ((tGesamt % zyklus) + zyklus) % zyklus
            var summe = 0.0

            // 1. Filzklavier-Stimmen
            for (k in aktiveKlavier.indices) {
                val note = aktiveKlavier[k]
                val dt = zeitSeitStart(t, note.startSek, zyklus)
                if (dt >= 0.0 && dt < note.dauerSek) {
                    summe += berechneFilzklavierSample(note, dt)
                }
            }

            // 2. Tiefe Cello-Bögen
            for (c in aktiveCello.indices) {
                val bogen = aktiveCello[c]
                val dt = zeitSeitStart(t, bogen.startSek, zyklus)
                if (dt >= 0.0 && dt < bogen.dauerSek) {
                    summe += berechneCelloSample(bogen, dt)
                }
            }

            // Sanfte analoge Sättigung verhindert jede Übersteuerung
            val geformt = tanh(summe * 0.82)
            val sample = (geformt * masterGain)
                .toInt()
                .coerceIn(Short.MIN_VALUE.toInt(), Short.MAX_VALUE.toInt())
            val byteIndex = i * 2
            ziel[byteIndex] = (sample and 0xFF).toByte()
            ziel[byteIndex + 1] = ((sample ushr 8) and 0xFF).toByte()
        }
    }

    /**
     * Berechnet ein einzelnes gedämpftes Filzklavier-Sample (Felt Piano):
     * weicher 18-ms-Filzanschlag, zweistufiger natürlicher Ausklang, schnell abklingende
     * Obertöne und analytische Tiefpass-Wärme (~760 Hz).
     */
    private fun berechneFilzklavierSample(note: KlavierNote, dt: Double): Double {
        val freq = midiZuHz(note.midiNote)
        val dauer = note.dauerSek

        // Weicher Filzhammer-Anschlag (startet exakt bei 0.0 -> absolut knackfrei)
        val anschlagHuelle = 1.0 - exp(-dt / 0.018)
        // Zweistufiger Piano-Ausklang (warmer Kern + leises Raum-Nachklingen)
        val abklingHuelle = 0.64 * exp(-dt / (dauer * 0.36)) + 0.36 * exp(-dt / (dauer * 0.92))
        // Sanfter Ausblend-Auslauf auf den letzten 0.45 s bis exakt 0.0
        val auslaufStart = (dauer - 0.45).coerceAtLeast(0.05)
        val auslauf = if (dt > auslaufStart) {
            val u = ((dt - auslaufStart) / (dauer - auslaufStart)).coerceIn(0.0, 1.0)
            0.5 * (1.0 + cos(PI * u))
        } else {
            1.0
        }

        val huelle = anschlagHuelle * abklingHuelle * auslauf
        if (huelle < 1e-5) return 0.0

        val w = ZWEI_PI * freq * dt
        val p1 = sin(w) + 0.18 * sin(ZWEI_PI * (freq + 0.32) * dt)
        val p2 = sin(2.0 * w + 0.15) * 0.28 * tiefpassFaktor(freq * 2.0, 760.0) * exp(-dt / 0.55)
        val p3 = sin(3.0 * w + 0.40) * 0.10 * tiefpassFaktor(freq * 3.0, 760.0) * exp(-dt / 0.22)
        val p4 = sin(4.0 * w) * 0.03 * tiefpassFaktor(freq * 4.0, 760.0) * exp(-dt / 0.10)
        // Hauchfeiner Filz-Korpus-Impuls beim Anschlag (sehr dumpf und kurz)
        val filz = sin(ZWEI_PI * 118.0 * dt) * 0.05 * exp(-dt / 0.016) * anschlagHuelle

        return (p1 * 0.72 + p2 + p3 + p4 + filz) * huelle * note.anschlag * 0.46
    }

    /**
     * Berechnet ein einzelnes tiefes, dunkles Cello-Sample mit langsamer Bogen-Hüllkurve
     * (`sin(π·u)^1.8`), subtilem organischem Vibrato und stark gedämpften Streicher-Obertönen.
     */
    private fun berechneCelloSample(bogen: CelloBogen, dt: Double): Double {
        val u = (dt / bogen.dauerSek).coerceIn(0.0, 1.0)
        val huelle = sin(PI * u).pow(1.8)
        if (huelle < 1e-5) return 0.0

        val freq = midiZuHz(bogen.midiNote)
        val vibTiefe = 0.0020 * min(1.0, dt / 1.6)
        val vibPhase = (vibTiefe * freq / 4.1) * (1.0 - cos(ZWEI_PI * 4.1 * dt))
        val phase = ZWEI_PI * freq * dt + vibPhase

        val k1 = sin(phase)
        val k2 = sin(2.0 * phase + 0.28) * 0.36 * tiefpassFaktor(freq * 2.0, 440.0)
        val k3 = sin(3.0 * phase + 0.65) * 0.14 * tiefpassFaktor(freq * 3.0, 440.0)
        val k4 = sin(4.0 * phase + 0.90) * 0.04 * tiefpassFaktor(freq * 4.0, 440.0)

        return (k1 + k2 + k3 + k4) * huelle * bogen.pegel * 0.34
    }

    private fun tiefpassFaktor(freqHz: Double, grenzHz: Double): Double {
        val verhaeltnis = freqHz / grenzHz
        return 1.0 / sqrt(1.0 + verhaeltnis * verhaeltnis)
    }

    private fun zeitSeitStart(t: Double, startSek: Double, zyklus: Double): Double {
        val diff = t - startSek
        return if (diff >= 0.0) diff else diff + zyklus
    }

    private fun istImBlockAktiv(
        tStart: Double,
        blockDauer: Double,
        noteStart: Double,
        noteDauer: Double,
        zyklus: Double,
    ): Boolean {
        val dtStart = zeitSeitStart(tStart, noteStart, zyklus)
        if (dtStart < noteDauer) return true
        // Falls die Note innerhalb des aktuellen Blocks erst beginnt
        val bisStart = zeitSeitStart(noteStart, tStart, zyklus)
        return bisStart <= blockDauer + 0.002
    }
}

/**
 * Synthetisiert kurze, organische, dezente 16-Bit-PCM-Soundeffekte (mono, 22.050 Hz)
 * für taktile Rückmeldung ohne externe Audiodateien:
 * - [SoundEffekt.KLICK_SANFT]: 38 ms warmes, dumpfes Holz-/Karton-Tippen
 * - [SoundEffekt.ENTSCHEIDUNG]: 140 ms weiches Papier-Umblättern (bandpass-gefiltertes Rauschen)
 * - [SoundEffekt.KAPITELWECHSEL]: 560 ms gedämpfter dunkler Klavier-Tiefklang (D3 + A3)
 * - [SoundEffekt.EINSCHNITT]: 340 ms sehr leiser, respektvoller gedämpfter Einzelton (A3)
 */
object ArchivSfxSynthese {

    const val SAMPLE_RATE: Int = RuhigeArchivSynthese.SAMPLE_RATE
    private const val ZWEI_PI: Double = 2.0 * PI

    fun dauerMsFuer(effekt: SoundEffekt): Int = when (effekt) {
        SoundEffekt.KLICK_SANFT -> 38
        SoundEffekt.ENTSCHEIDUNG -> 140
        SoundEffekt.KAPITELWECHSEL -> 560
        SoundEffekt.EINSCHNITT -> 340
    }

    /**
     * Erzeugt den kompletten 16-Bit-Little-Endian-PCM-Puffer für den gewünschten [SoundEffekt].
     */
    fun erzeugePcm16(
        effekt: SoundEffekt,
        lautstaerke: Float,
    ): ByteArray {
        val begrenzt = AudioRegelwerk.begrenzeLautstaerke(lautstaerke)
        val sampleAnzahl = (SAMPLE_RATE * dauerMsFuer(effekt)) / 1000
        val ziel = ByteArray(sampleAnzahl * 2)
        if (begrenzt <= 0f || sampleAnzahl <= 0) return ziel

        val gain = begrenzt.toDouble() * Short.MAX_VALUE
        when (effekt) {
            SoundEffekt.KLICK_SANFT -> fuelleKlickSanft(ziel, sampleAnzahl, gain)
            SoundEffekt.ENTSCHEIDUNG -> fuellePapierBlaettern(ziel, sampleAnzahl, gain)
            SoundEffekt.KAPITELWECHSEL -> fuelleKapitelWechsel(ziel, sampleAnzahl, gain)
            SoundEffekt.EINSCHNITT -> fuelleEinschnitt(ziel, sampleAnzahl, gain)
        }
        return ziel
    }

    private fun fuelleKlickSanft(ziel: ByteArray, sampleAnzahl: Int, gain: Double) {
        var rauschZustand = 0x5A17_1914L
        var lpRauschen = 0.0
        val dauer = sampleAnzahl.toDouble() / SAMPLE_RATE.toDouble()

        for (i in 0 until sampleAnzahl) {
            val t = i.toDouble() / SAMPLE_RATE.toDouble()
            // Deterministisches Rauschen für feines Karton-Tippen
            rauschZustand = rauschZustand * 6364136223846793005L + 1442695040888963407L
            val weiss = ((rauschZustand ushr 33).toDouble() / 2147483648.0) * 2.0 - 1.0
            lpRauschen += 0.24 * (weiss - lpRauschen)

            val anstieg = min(1.0, t / 0.0018)
            val auslauf = if (t > dauer - 0.006) {
                ((dauer - t) / 0.006).coerceIn(0.0, 1.0)
            } else {
                1.0
            }
            val holz = sin(ZWEI_PI * 265.0 * t) * exp(-t / 0.0062) * 0.58 +
                sin(ZWEI_PI * 490.0 * t) * exp(-t / 0.0032) * 0.24
            val karton = lpRauschen * exp(-t / 0.0055) * 0.30
            val wert = (holz + karton) * anstieg * auslauf * 0.42

            schreibeSample(ziel, i, wert * gain)
        }
    }

    private fun fuellePapierBlaettern(ziel: ByteArray, sampleAnzahl: Int, gain: Double) {
        var rauschZustand = 0x1914_1918L
        val dauer = sampleAnzahl.toDouble() / SAMPLE_RATE.toDouble()
        // Zwei gestaffelte 1-Pol-Filter bilden ein warmes Bandpass-Fenster (~350–1550 Hz)
        var lpHoch = 0.0
        var lpTief = 0.0
        var lpWeich = 0.0

        for (i in 0 until sampleAnzahl) {
            val t = i.toDouble() / SAMPLE_RATE.toDouble()
            val u = (t / dauer).coerceIn(0.0, 1.0)

            rauschZustand = rauschZustand * 6364136223846793005L + 1442695040888963407L
            val weiss = ((rauschZustand ushr 33).toDouble() / 2147483648.0) * 2.0 - 1.0

            // Bandpass: Tiefpass (~1550 Hz) minus tieferem Tiefpass (~340 Hz)
            lpHoch += 0.34 * (weiss - lpHoch)
            lpTief += 0.09 * (weiss - lpTief)
            val band = lpHoch - lpTief
            lpWeich += 0.42 * (band - lpWeich)

            // Organische Papier-Hüllkurve: sanftes Streichen, leichte Falz-Welle, leises Ausklingen
            val huelle = sin(PI * u).pow(1.45) * (0.78 + 0.22 * sin(PI * (u * 2.15).coerceIn(0.0, 1.0)))
            // Hauch von weichem Karton-Körper beim Auflegen
            val koerper = sin(ZWEI_PI * 195.0 * t) * exp(-t / 0.022) * 0.14 * min(1.0, t / 0.006)
            val wert = (lpWeich * 0.92 + koerper) * huelle * 0.46

            schreibeSample(ziel, i, wert * gain)
        }
    }

    private fun fuelleKapitelWechsel(ziel: ByteArray, sampleAnzahl: Int, gain: Double) {
        val dauer = sampleAnzahl.toDouble() / SAMPLE_RATE.toDouble()
        val f1 = RuhigeArchivSynthese.midiZuHz(50) // D3 (146.83 Hz)
        val f2 = RuhigeArchivSynthese.midiZuHz(57) // A3 (220.00 Hz)

        for (i in 0 until sampleAnzahl) {
            val t = i.toDouble() / SAMPLE_RATE.toDouble()
            val anstieg = 1.0 - exp(-t / 0.028)
            val abkling = exp(-t / 0.22)
            val auslauf = if (t > dauer - 0.12) {
                val u = ((t - (dauer - 0.12)) / 0.12).coerceIn(0.0, 1.0)
                0.5 * (1.0 + cos(PI * u))
            } else {
                1.0
            }
            val klang = sin(ZWEI_PI * f1 * t) * 0.62 +
                sin(ZWEI_PI * f1 * 2.0 * t) * 0.16 * exp(-t / 0.10) +
                sin(ZWEI_PI * f2 * t) * 0.34 * exp(-t / 0.18)
            val wert = klang * anstieg * abkling * auslauf * 0.36
            schreibeSample(ziel, i, wert * gain)
        }
    }

    private fun fuelleEinschnitt(ziel: ByteArray, sampleAnzahl: Int, gain: Double) {
        val dauer = sampleAnzahl.toDouble() / SAMPLE_RATE.toDouble()
        val f = RuhigeArchivSynthese.midiZuHz(57) // A3 (220.00 Hz)

        for (i in 0 until sampleAnzahl) {
            val t = i.toDouble() / SAMPLE_RATE.toDouble()
            val anstieg = 1.0 - exp(-t / 0.022)
            val abkling = exp(-t / 0.13)
            val auslauf = if (t > dauer - 0.08) {
                val u = ((t - (dauer - 0.08)) / 0.08).coerceIn(0.0, 1.0)
                0.5 * (1.0 + cos(PI * u))
            } else {
                1.0
            }
            val klang = sin(ZWEI_PI * f * t) * 0.78 +
                sin(ZWEI_PI * f * 2.0 * t) * 0.12 * exp(-t / 0.06)
            val wert = klang * anstieg * abkling * auslauf * 0.30
            schreibeSample(ziel, i, wert * gain)
        }
    }

    private fun schreibeSample(ziel: ByteArray, index: Int, rohWert: Double) {
        val sample = (tanh(rohWert / Short.MAX_VALUE) * Short.MAX_VALUE)
            .toInt()
            .coerceIn(Short.MIN_VALUE.toInt(), Short.MAX_VALUE.toInt())
        val byteIndex = index * 2
        ziel[byteIndex] = (sample and 0xFF).toByte()
        ziel[byteIndex + 1] = ((sample ushr 8) and 0xFF).toByte()
    }
}
