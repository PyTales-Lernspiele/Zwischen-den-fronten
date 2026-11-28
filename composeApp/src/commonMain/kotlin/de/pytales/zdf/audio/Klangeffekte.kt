package de.pytales.zdf.audio

import de.pytales.zdf.engine.GamePhase

/**
 * Kurze, leise Archiv-Klangeffekte (Papier, Stift, Stempel, Buch) als Rückmeldung auf
 * Bedienhandlungen und Spielschritte.
 *
 * Alle Aufnahmen stammen von Freesound.org und stehen unter **CC0 1.0** (gemeinfrei);
 * Herkunft und Bearbeitung sind in `docs/KLAENGE.md` dokumentiert.
 * Bewusst gibt es **keine** Kriegsgeräusche (Schüsse, Explosionen, Sirenen): Die Effekte sind
 * reine „Schreibtisch- und Akten“-Klänge und damit auch an Front und Etappe unbedenklich —
 * die harte Musiksperre aus [AudioRegelwerk] betrifft ausschließlich die Hintergrundmusik.
 *
 * @property datei Dateiname unter `files/klaenge/` (16-Bit-PCM-WAV, mono, 22,05 kHz).
 * @property pegel Feinabgleich der wahrgenommenen Lautheit (0..1), damit alle Effekte gleich ruhig wirken.
 */
enum class Klang(
    val datei: String,
    val pegel: Float,
) {
    /** Kurzer, weicher Klick bei Auswahl, Schaltern und Symbolknöpfen. */
    TIPPEN("tippen.wav", 0.55f),

    /** Umblättern einer Seite: neues Ereignis, nächster Schritt. */
    UMBLAETTERN("umblaettern.wav", 0.8f),

    /** Bleistiftstrich: Eine Entscheidung wird festgehalten. */
    ENTSCHEIDUNG("entscheidung.wav", 0.6f),

    /** Amtsstempel: Musterungsbescheid. */
    STEMPEL("stempel.wav", 0.6f),

    /** Ein Buch wird aufgeschlagen: neues Kapitel / neues Jahr. */
    KAPITEL("kapitel.wav", 0.9f),

    /** Ein Blatt wird hingeschoben: Erklärkarte oder Dialog öffnet sich. */
    KARTE("karte.wav", 0.5f),

    /** Schreibmaschinen-Glocke: Kapitelrückblick ist fertig „getippt“. */
    KAPITEL_ABSCHLUSS("kapitelabschluss.wav", 0.55f),

    /** Ein Buch wird zugeschlagen: Lebenslauf bzw. Ende des Durchgangs. */
    ABSCHLUSS("abschluss.wav", 0.75f),
    ;

    /** Pfad für `Res.readBytes(...)` bzw. `Res.getUri(...)`. */
    val ressourcenPfad: String
        get() = "files/klaenge/$datei"
}

/**
 * Plattformunabhängige Zuordnung von Spielschritten zu [Klang]en (vollständig testbar).
 */
object KlangRegelwerk {

    const val STANDARD_LAUTSTAERKE: Float = 0.7f

    /**
     * Stabiler Schlüssel einer Phase: Ein Klang wird nur gespielt, wenn sich dieser Schlüssel ändert
     * (verhindert doppelte Klänge bei Neuzeichnungen oder Einstellungsänderungen).
     */
    fun phasenSchluessel(phase: GamePhase): String = when (phase) {
        is GamePhase.Start -> "start"
        is GamePhase.HerkunftWahl -> "herkunft"
        is GamePhase.MusterungErgebnis -> "musterung"
        is GamePhase.ErwerbWahl -> "erwerb"
        is GamePhase.KapitelStart -> "kapitel-${phase.kapitel.jahr}"
        is GamePhase.EreignisAnzeige -> "ereignis-${phase.ereignis.id}"
        is GamePhase.EreignisAusgang -> "ausgang-${phase.ereignis.id}"
        is GamePhase.KapitelAbschluss -> "rueckblick-${phase.kapitel.jahr}"
        is GamePhase.Abgeschlossen -> "abschluss"
    }

    /**
     * Klang beim Wechsel von [vorher] nach [nachher]; `null`, wenn kein Klang passt
     * (z. B. erster Aufbau der App oder unveränderte Phase).
     */
    fun klangFuerPhasenwechsel(vorher: GamePhase?, nachher: GamePhase): Klang? {
        if (vorher == null) return null
        if (phasenSchluessel(vorher) == phasenSchluessel(nachher)) return null
        return when (nachher) {
            is GamePhase.Start -> Klang.ABSCHLUSS.takeIf { vorher !is GamePhase.Abgeschlossen } ?: Klang.UMBLAETTERN
            is GamePhase.HerkunftWahl -> Klang.UMBLAETTERN
            is GamePhase.MusterungErgebnis -> Klang.STEMPEL
            is GamePhase.ErwerbWahl -> Klang.UMBLAETTERN
            is GamePhase.KapitelStart -> Klang.KAPITEL
            is GamePhase.EreignisAnzeige -> Klang.UMBLAETTERN
            is GamePhase.EreignisAusgang -> Klang.ENTSCHEIDUNG
            is GamePhase.KapitelAbschluss -> Klang.KAPITEL_ABSCHLUSS
            is GamePhase.Abgeschlossen -> Klang.ABSCHLUSS
        }
    }

    /** Begrenzt die Effekt-Lautstärke auf `0..1`. */
    fun begrenzeLautstaerke(lautstaerke: Float): Float =
        if (lautstaerke.isNaN()) 0f else lautstaerke.coerceIn(0f, 1f)
}

/**
 * Dekodiertes Mono-PCM eines Klangs.
 */
class PcmKlang(
    val abtastrate: Int,
    val samples: ShortArray,
) {
    val dauerSekunden: Double
        get() = if (abtastrate <= 0) 0.0 else samples.size.toDouble() / abtastrate

    /** Liefert die Samples als 16-Bit-Little-Endian-Bytes, mit [faktor] skaliert. */
    fun alsPcm16Bytes(faktor: Float): ByteArray {
        val f = faktor.coerceIn(0f, 1f)
        val ziel = ByteArray(samples.size * 2)
        for (i in samples.indices) {
            val s = (samples[i] * f).toInt().coerceIn(Short.MIN_VALUE.toInt(), Short.MAX_VALUE.toInt())
            ziel[i * 2] = (s and 0xFF).toByte()
            ziel[i * 2 + 1] = ((s ushr 8) and 0xFF).toByte()
        }
        return ziel
    }

    /** Liefert die Samples skaliert als ShortArray. */
    fun skaliert(faktor: Float): ShortArray {
        val f = faktor.coerceIn(0f, 1f)
        return ShortArray(samples.size) { i -> (samples[i] * f).toInt().toShort() }
    }
}

/**
 * Minimaler, robuster RIFF/WAVE-Dekoder für 16-Bit-PCM (mono oder stereo → mono).
 * Unbekannte Chunks (`LIST`, `fact`, …) werden übersprungen.
 */
object WavDekoder {

    fun dekodiere(bytes: ByteArray): PcmKlang? {
        if (bytes.size < 44) return null
        if (text(bytes, 0) != "RIFF" || text(bytes, 8) != "WAVE") return null

        var pos = 12
        var formatTag = -1
        var kanaele = 0
        var abtastrate = 0
        var bitsProSample = 0
        var datenStart = -1
        var datenLaenge = 0

        while (pos + 8 <= bytes.size) {
            val id = text(bytes, pos)
            val laenge = int32(bytes, pos + 4)
            val inhalt = pos + 8
            if (laenge < 0 || inhalt > bytes.size) return null
            when (id) {
                "fmt " -> {
                    if (laenge < 16 || inhalt + 16 > bytes.size) return null
                    formatTag = int16(bytes, inhalt)
                    kanaele = int16(bytes, inhalt + 2)
                    abtastrate = int32(bytes, inhalt + 4)
                    bitsProSample = int16(bytes, inhalt + 14)
                }

                "data" -> {
                    datenStart = inhalt
                    datenLaenge = minOf(laenge, bytes.size - inhalt)
                }
            }
            if (datenStart >= 0 && formatTag >= 0) break
            pos = inhalt + laenge + (laenge and 1)
        }

        // 1 = PCM, 0xFFFE = WAVE_FORMAT_EXTENSIBLE (bei 16 Bit ebenfalls PCM)
        if (formatTag != 1 && formatTag != 0xFFFE) return null
        if (bitsProSample != 16 || kanaele !in 1..2 || abtastrate <= 0 || datenStart < 0) return null

        val frameBytes = 2 * kanaele
        val frames = datenLaenge / frameBytes
        val samples = ShortArray(frames)
        for (i in 0 until frames) {
            val basis = datenStart + i * frameBytes
            samples[i] = if (kanaele == 1) {
                int16Signed(bytes, basis).toShort()
            } else {
                ((int16Signed(bytes, basis) + int16Signed(bytes, basis + 2)) / 2).toShort()
            }
        }
        return PcmKlang(abtastrate = abtastrate, samples = samples)
    }

    private fun text(b: ByteArray, off: Int): String =
        if (off + 4 > b.size) "" else CharArray(4) { (b[off + it].toInt() and 0xFF).toChar() }.concatToString()

    private fun int16(b: ByteArray, off: Int): Int =
        (b[off].toInt() and 0xFF) or ((b[off + 1].toInt() and 0xFF) shl 8)

    private fun int16Signed(b: ByteArray, off: Int): Int = int16(b, off).toShort().toInt()

    private fun int32(b: ByteArray, off: Int): Int =
        (b[off].toInt() and 0xFF) or
            ((b[off + 1].toInt() and 0xFF) shl 8) or
            ((b[off + 2].toInt() and 0xFF) shl 16) or
            ((b[off + 3].toInt() and 0xFF) shl 24)
}

/**
 * Plattform-Ausgabe für kurze Klangeffekte.
 * Alle Implementierungen fangen fehlende Hardware oder Browser-Richtlinien lautlos ab.
 */
interface KlangAusgabe {
    /** `true`, wenn die Plattform die WAV-Rohdaten braucht (Android, Desktop); Web lädt per URL. */
    val brauchtRohdaten: Boolean

    fun lade(klang: Klang, rohdaten: ByteArray?, uri: String?)

    /** Spielt [klang] mit [lautstaerke] (0..1, bereits inkl. [Klang.pegel]) ab. */
    fun spiele(klang: Klang, lautstaerke: Float)

    fun freigeben()
}

/** Stille Fallback-Ausgabe (Tests, Headless). */
object StilleKlangAusgabe : KlangAusgabe {
    override val brauchtRohdaten: Boolean = false
    override fun lade(klang: Klang, rohdaten: ByteArray?, uri: String?) = Unit
    override fun spiele(klang: Klang, lautstaerke: Float) = Unit
    override fun freigeben() = Unit
}

expect fun erstellePlattformKlangAusgabe(): KlangAusgabe
