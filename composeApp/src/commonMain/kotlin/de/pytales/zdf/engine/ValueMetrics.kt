package de.pytales.zdf.engine

import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.HartesEndeId
import de.pytales.zdf.model.Konfiguration
import de.pytales.zdf.model.Stimmung
import de.pytales.zdf.model.WertSchluessel
import kotlin.math.abs

/**
 * Aufbereiteter Anzeigestatus eines der 4 Befindenswerte für Kopfleiste, Bilanz & Tests.
 */
data class WertStatus(
    val schluessel: WertSchluessel,
    val bezeichnung: String,
    val rohwert: Int,
    val maximum: Int,
    val stufe: Int,
    val stufenName: String,
    val stufenKurz: String,
    val gefuellteSegmente: Int,
    val segmenteGesamt: Int,
    val letzteRohAenderung: Int,
    val angezeigteAenderung: Int,
    val erklaerung: String,
    val folge: String,
)

/**
 * Menschenlesbare Darstellung einer Werteveränderung in der Sprache der Anzeige
 * (ein Plus bei Hunger/Erschöpfung/Verdacht/Einsamkeit ist immer schlecht, ein Minus immer gut).
 */
data class WirkungZeile(
    val schluessel: WertSchluessel,
    val name: String,
    val richtung: String,
    val schlechter: Boolean,
    val rohBetrag: Int,
    val gezeigt: Int,
    val zeichen: String,
)

/**
 * Aktueller Zustand der Live-Emotions-Kachel rechts oben.
 */
data class LiveEmotionSnapshot(
    val stimmung: Stimmung,
    val portraitId: String?,
    val ausloesenderWert: WertSchluessel?,
    val hoechsteStufe: Int,
    val istUeberschrieben: Boolean,
)

/**
 * Reine Berechnungen rund um die 4 Befindenswerte (0–12, 5 Stufen, Balken voll = gut),
 * Zustandssätze, harte Abbruchschwellen und die Live-Emotions-Kachel.
 */
class ValueMetrics(
    private val konfiguration: Konfiguration,
) {
    private val werteKonf = konfiguration.werte
    private val stimmungenKonf = konfiguration.stimmungen
    private val schwellen = konfiguration.harteEnden.schwellen

    fun wertBegrenzen(wert: Int): Int =
        wert.coerceIn(werteKonf.minimum, werteKonf.maximum)

    /**
     * Wendet Änderungen auf einen Wertestand an und gibt (neueWerte, tatsaechlichAngekommeneAenderungen) zurück.
     */
    fun werteAnwenden(
        aktuell: Map<WertSchluessel, Int>,
        aenderungen: Map<WertSchluessel, Int>,
    ): Pair<Map<WertSchluessel, Int>, Map<WertSchluessel, Int>> {
        if (aenderungen.isEmpty()) {
            return aktuell to emptyMap()
        }
        val neu = LinkedHashMap<WertSchluessel, Int>(werteKonf.reihenfolge.size)
        val diff = LinkedHashMap<WertSchluessel, Int>()
        for (schluessel in werteKonf.reihenfolge) {
            val vorher = aktuell[schluessel] ?: werteKonf.minimum
            val delta = aenderungen[schluessel] ?: 0
            val nachher = wertBegrenzen(vorher + delta)
            neu[schluessel] = nachher
            val effektiv = nachher - vorher
            if (effektiv != 0) {
                diff[schluessel] = effektiv
            }
        }
        return neu to diff
    }

    /**
     * Rechnet den Rohwert (0–12) in eine einheitliche Belastungsstufe (0 = gut .. 4 = kritisch) um.
     */
    fun stufeVonWert(schluessel: WertSchluessel, wert: Int): Int {
        val begrenzt = wertBegrenzen(wert)
        val definition = werteKonf.definitionen.getValue(schluessel)
        val gemessen = if (definition.hochIstGut) {
            werteKonf.maximum - begrenzt
        } else {
            begrenzt
        }
        return when {
            gemessen <= 1 -> 0
            gemessen <= 4 -> 1
            gemessen <= 7 -> 2
            gemessen <= 10 -> 3
            else -> 4
        }
    }

    fun alleStufen(werte: Map<WertSchluessel, Int>): Map<WertSchluessel, Int> =
        werteKonf.reihenfolge.associateWith { schluessel ->
            stufeVonWert(schluessel, werte[schluessel] ?: werteKonf.minimum)
        }

    /**
     * Balkenanzeige *voll = gut*:
     * Bei Stufe 0 sind alle 5 Segmente gefüllt, bei Stufe 4 bleibt 1 Restsegment stehen.
     */
    fun gefuellteSegmente(stufe: Int): Int {
        val segmente = werteKonf.segmenteJeBalken
        val s = stufe.coerceIn(0, segmente - 1)
        return if (werteKonf.balkenVollIstGut) {
            segmente - s
        } else {
            s + 1
        }
    }

    /**
     * Ob Segment `segmentIndex` (0-basiert von links) gefüllt ist.
     */
    fun segmentGefuellt(segmentIndex: Int, stufe: Int): Boolean {
        val segmente = werteKonf.segmenteJeBalken
        val s = stufe.coerceIn(0, segmente - 1)
        return if (werteKonf.balkenVollIstGut) {
            segmentIndex <= (segmente - 1 - s)
        } else {
            segmentIndex <= s
        }
    }

    /**
     * Liefert den Wert mit der höchsten Belastungsstufe (bei Gleichstand in der konfigurierten Reihenfolge).
     */
    fun schwaechsterWert(werte: Map<WertSchluessel, Int>): WertSchluessel {
        var gewaehlt = werteKonf.reihenfolge.first()
        var hoechste = -1
        for (schluessel in werteKonf.reihenfolge) {
            val stufe = stufeVonWert(schluessel, werte[schluessel] ?: werteKonf.minimum)
            if (stufe > hoechste) {
                hoechste = stufe
                gewaehlt = schluessel
            }
        }
        return gewaehlt
    }

    fun zustandssatz(werte: Map<WertSchluessel, Int>): String {
        val schwaechster = schwaechsterWert(werte)
        val stufe = stufeVonWert(schwaechster, werte[schwaechster] ?: werteKonf.minimum)
        val definition = werteKonf.definitionen.getValue(schwaechster)
        return definition.zustandssaetze[stufe]
    }

    /**
     * Berechnet die Live-Stimmung für die Charakter-Kachel rechts oben:
     * - Eine explizite Ereignis- oder Options-Überschreibung hat Vorrang.
     * - Sonst gilt die Stimmung des schwächsten Wertes ab `stimmungen.abStufe` (Stufe 2).
     * - Darunter bleibt die Stimmung `neutral`.
     */
    fun berechneStimmung(
        werte: Map<WertSchluessel, Int>,
        ueberschreibung: Stimmung? = null,
    ): Stimmung {
        if (ueberschreibung != null) return ueberschreibung
        val schwaechster = schwaechsterWert(werte)
        val stufe = stufeVonWert(schwaechster, werte[schwaechster] ?: werteKonf.minimum)
        if (stufe < stimmungenKonf.abStufe) {
            return stimmungenKonf.standard
        }
        return stimmungenKonf.ausWert[schwaechster] ?: stimmungenKonf.standard
    }

    /**
     * Erzeugt die standardisierte Portrait-ID `portrait_<herkunft>_<geschlecht>_<stimmung>`.
     */
    fun portraitId(
        herkunftId: String,
        geschlecht: Geschlecht,
        stimmung: Stimmung,
    ): String = "portrait_${herkunftId}_${geschlecht.code}_${stimmung.code}"

    fun liveEmotion(
        werte: Map<WertSchluessel, Int>,
        herkunftId: String?,
        geschlecht: Geschlecht?,
        ueberschreibung: Stimmung? = null,
    ): LiveEmotionSnapshot {
        val schwaechster = schwaechsterWert(werte)
        val stufe = stufeVonWert(schwaechster, werte[schwaechster] ?: werteKonf.minimum)
        val stimmung = berechneStimmung(werte, ueberschreibung)
        val portrait = if (herkunftId != null && geschlecht != null) {
            portraitId(herkunftId, geschlecht, stimmung)
        } else {
            null
        }
        val ausloeser = when {
            ueberschreibung != null -> null
            stufe >= stimmungenKonf.abStufe -> schwaechster
            else -> null
        }
        return LiveEmotionSnapshot(
            stimmung = stimmung,
            portraitId = portrait,
            ausloesenderWert = ausloeser,
            hoechsteStufe = stufe,
            istUeberschrieben = ueberschreibung != null,
        )
    }

    fun werteAnzeige(
        werte: Map<WertSchluessel, Int>,
        letzteAenderungen: Map<WertSchluessel, Int> = emptyMap(),
    ): List<WertStatus> = werteKonf.reihenfolge.map { schluessel ->
        val definition = werteKonf.definitionen.getValue(schluessel)
        val rohwert = wertBegrenzen(werte[schluessel] ?: werteKonf.minimum)
        val stufe = stufeVonWert(schluessel, rohwert)
        val rohDelta = letzteAenderungen[schluessel] ?: 0
        val anzeigeDelta = if (definition.hochIstGut) -rohDelta else rohDelta
        WertStatus(
            schluessel = schluessel,
            bezeichnung = definition.bezeichnung,
            rohwert = rohwert,
            maximum = werteKonf.maximum,
            stufe = stufe,
            stufenName = definition.stufenNamen[stufe],
            stufenKurz = definition.stufenKurz[stufe],
            gefuellteSegmente = gefuellteSegmente(stufe),
            segmenteGesamt = werteKonf.segmenteJeBalken,
            letzteRohAenderung = rohDelta,
            angezeigteAenderung = anzeigeDelta,
            erklaerung = definition.erklaerung,
            folge = definition.folge,
        )
    }

    fun wirkungZeilen(wirkung: Map<WertSchluessel, Int>): List<WirkungZeile> {
        if (wirkung.isEmpty()) return emptyList()
        return buildList {
            for (schluessel in werteKonf.reihenfolge) {
                val betrag = wirkung[schluessel] ?: 0
                if (betrag == 0) continue
                val definition = werteKonf.definitionen.getValue(schluessel)
                val schlechter = if (definition.hochIstGut) betrag < 0 else betrag > 0
                val gezeigt = if (definition.hochIstGut) -betrag else betrag
                val stark = abs(betrag) >= 2
                val richtung = when {
                    schlechter && stark -> "steigt deutlich"
                    schlechter -> "steigt"
                    stark -> "sinkt deutlich"
                    else -> "sinkt"
                }
                add(
                    WirkungZeile(
                        schluessel = schluessel,
                        name = definition.bezeichnung,
                        richtung = richtung,
                        schlechter = schlechter,
                        rohBetrag = betrag,
                        gezeigt = gezeigt,
                        zeichen = if (gezeigt > 0) "+$gezeigt" else gezeigt.toString(),
                    )
                )
            }
        }
    }

    /**
     * Prüft die drei harten Werte-Abbruchschwellen. Im Epilog (`jahr >= epilogJahr`) greifen sie nicht mehr.
     * `rueckhalt` (Einsamkeit) beendet den Durchgang bewusst niemals.
     */
    fun pruefeHartesEnde(
        werte: Map<WertSchluessel, Int>,
        jahr: Int,
        epilogJahr: Int,
    ): HartesEndeId? {
        if (jahr >= epilogJahr) return null
        val versorgung = werte[WertSchluessel.VERSORGUNG] ?: werteKonf.minimum
        val belastung = werte[WertSchluessel.BELASTUNG] ?: werteKonf.minimum
        val aufmerksamkeit = werte[WertSchluessel.AUFMERKSAMKEIT] ?: werteKonf.minimum
        return when {
            versorgung < schwellen.versorgungUnter -> HartesEndeId.ENDE_VERHUNGERT
            belastung >= schwellen.belastungAb -> HartesEndeId.ENDE_ZUSAMMENBRUCH
            aufmerksamkeit >= schwellen.aufmerksamkeitAb -> HartesEndeId.ENDE_VERHAFTET
            else -> null
        }
    }

    /**
     * Entschärft eine Kapitelwirkung beim Übergang in den Epilog 1919, sodass der
     * Jahreswechsel selbst keinen tödlichen Abbruch mehr auslöst.
     */
    fun wirkungEntschaerfen(
        werte: Map<WertSchluessel, Int>,
        wirkung: Map<WertSchluessel, Int>,
    ): Map<WertSchluessel, Int> {
        val sicher = wirkung.toMutableMap()

        val versorgung = werte[WertSchluessel.VERSORGUNG] ?: werteKonf.minimum
        val versorgungDelta = sicher[WertSchluessel.VERSORGUNG] ?: 0
        if (versorgung + versorgungDelta < schwellen.versorgungUnter) {
            sicher[WertSchluessel.VERSORGUNG] = schwellen.versorgungUnter - versorgung
        }

        val belastung = werte[WertSchluessel.BELASTUNG] ?: werteKonf.minimum
        val belastungGrenze = schwellen.belastungAb - 1
        val belastungDelta = sicher[WertSchluessel.BELASTUNG] ?: 0
        if (belastung + belastungDelta > belastungGrenze) {
            sicher[WertSchluessel.BELASTUNG] = belastungGrenze - belastung
        }

        val aufmerksamkeit = werte[WertSchluessel.AUFMERKSAMKEIT] ?: werteKonf.minimum
        val aufmerksamkeitGrenze = schwellen.aufmerksamkeitAb - 1
        val aufmerksamkeitDelta = sicher[WertSchluessel.AUFMERKSAMKEIT] ?: 0
        if (aufmerksamkeit + aufmerksamkeitDelta > aufmerksamkeitGrenze) {
            sicher[WertSchluessel.AUFMERKSAMKEIT] = aufmerksamkeitGrenze - aufmerksamkeit
        }

        return sicher.filterValues { it != 0 }
    }
}
