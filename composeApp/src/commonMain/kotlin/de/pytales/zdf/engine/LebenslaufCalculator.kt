package de.pytales.zdf.engine

import de.pytales.zdf.content.GameContent
import de.pytales.zdf.model.AusgangBedingung
import de.pytales.zdf.model.AusgangDefinition
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.Nachklang
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.WertSchluessel

/**
 * Ergebnis eines der 4 festen Fächer des Lebenslaufs:
 * 0: Woher du kamst
 * 1: Wohin es dich brachte
 * 2: Was du entschieden hast
 * 3: Wie es ausging
 */
data class LebenslaufFachErgebnis(
    val fachIndex: Int,
    val titel: String,
    val merkmalId: String?,
    val merkmalName: String?,
    val eintrag: Nachklang?,
)

/**
 * Chronologischer Eintrag auf der Lebenslauf-Zeitleiste.
 */
data class LebenslaufZeitleistenEintrag(
    val jahr: Int,
    val datum: String,
    val text: String,
    val quelle: String,
    val fachTitel: String? = null,
    val merkmalId: String? = null,
)

/**
 * Vollständiges Ergebnis für den Schlussbildschirm — sowohl bei regulärem
 * Erreichen des Epilog-Finales 1919 als auch beim respektvollen Auffangnetz
 * nach einem vorzeitigen Abbruch.
 */
data class LebenslaufErgebnis(
    val istVorzeitigerAbbruch: Boolean,
    val hartesEnde: HartesEndeErgebnis?,
    val ausgang: AusgangDefinition?,
    val faecher: List<LebenslaufFachErgebnis>,
    val zeitleiste: List<LebenslaufZeitleistenEintrag>,
    val fazit: String,
    val werteBilanz: List<WertStatus>,
)

/**
 * Berechnet den 4-Fächer-Lebenslauf, die deklarativen Ausgänge aus `merkmale.json`
 * und das respektvolle Auffangnetz bei vorzeitigem Abbruch.
 */
class LebenslaufCalculator(
    private val content: GameContent,
    private val metrics: ValueMetrics,
) {
    private val merkmaleDaten = content.merkmale
    private val lebenslaufKonf = merkmaleDaten.lebenslauf
    private val registerIndex: Map<String, Int> =
        content.registerReihenfolge.withIndex().associate { (idx, key) -> key to idx }

    /**
     * Wertet eine deklarative [AusgangBedingung] aus `merkmale.json` gegen Stufen, Pfad,
     * Geschlecht und gesammelte Merkmale aus.
     */
    fun bedingungTrifftZu(
        bedingung: AusgangBedingung,
        stufen: Map<WertSchluessel, Int>,
        pfad: Pfad,
        geschlecht: Geschlecht?,
        merkmale: Set<String>,
    ): Boolean {
        if (bedingung.immer) return true

        if (bedingung.pfade.isNotEmpty() && pfad !in bedingung.pfade) {
            return false
        }

        if (bedingung.geschlecht != null && geschlecht != bedingung.geschlecht) {
            return false
        }

        if (bedingung.einesDerMerkmale.isNotEmpty() &&
            bedingung.einesDerMerkmale.none { it in merkmale }
        ) {
            return false
        }

        if (bedingung.minStufe.any { (schluessel, min) -> (stufen[schluessel] ?: 0) < min }) {
            return false
        }

        if (bedingung.maxStufe.any { (schluessel, max) -> (stufen[schluessel] ?: 0) > max }) {
            return false
        }

        if (bedingung.minStufeEines.isNotEmpty() &&
            bedingung.minStufeEines.none { (schluessel, min) -> (stufen[schluessel] ?: 0) >= min }
        ) {
            return false
        }

        if (bedingung.oderMerkmal.isNotEmpty() || bedingung.oderMinStufe.isNotEmpty()) {
            val merkmalOk = bedingung.oderMerkmal.any { it in merkmale }
            val stufeOk = bedingung.oderMinStufe.any { (schluessel, min) ->
                (stufen[schluessel] ?: 0) >= min
            }
            if (!merkmalOk && !stufeOk) {
                return false
            }
        }

        return true
    }

    /**
     * Bestimmt den höchstrangigen passenden Ausgang aus `merkmale.json` (Fallback: `weitergelebt`).
     */
    fun bestimmeAusgang(
        stufen: Map<WertSchluessel, Int>,
        pfad: Pfad,
        geschlecht: Geschlecht?,
        merkmale: Set<String>,
    ): AusgangDefinition {
        var bester: AusgangDefinition? = null
        for (ausgang in lebenslaufKonf.ausgaenge) {
            if (!bedingungTrifftZu(ausgang.bedingung, stufen, pfad, geschlecht, merkmale)) {
                continue
            }
            if (bester == null || ausgang.rang > bester.rang) {
                bester = ausgang
            }
        }
        return bester ?: lebenslaufKonf.ausgaenge.first { it.id == "weitergelebt" }
    }

    /**
     * Ordnet ein Merkmal einem der 4 festen Fächer zu (0..3) oder liefert `null`.
     */
    fun fachFuerMerkmal(merkmalId: String): Int? {
        if (merkmalId in lebenslaufKonf.schlussMerkmale) {
            return lebenslaufKonf.faecher.lastIndex
        }
        val eintrag = merkmaleDaten.register[merkmalId] ?: return null
        val index = lebenslaufKonf.faecher.indexOfFirst { fach ->
            eintrag.gruppe in fach.gruppen
        }
        return if (index >= 0) index else null
    }

    /**
     * Wählt je Fach den höchstrangigen Eintrag (bei Gleichstand nach Registerreihenfolge).
     * Bleibt ein Fach leer, rückt nichts aus anderen Fächern nach.
     */
    fun berechneFaecher(
        merkmale: Collection<String>,
        hartesEnde: HartesEndeErgebnis? = null,
    ): List<LebenslaufFachErgebnis> {
        val besteJeFach = mutableMapOf<Int, String>()

        for (merkmalId in merkmale) {
            val eintrag = merkmaleDaten.register[merkmalId] ?: continue
            // Im regulären Lebenslauf zählen nur Merkmale mit Nachklang;
            // beim Auffangnetz (vorzeitiger Abbruch) dürfen auch Merkmale ohne Nachkriegs-Nachklang
            // die Fächer 0..2 sichtbar machen, damit Herkunft/Station/Entscheidungen gewürdigt werden.
            if (hartesEnde == null && eintrag.nachklang == null) continue

            val fachIndex = fachFuerMerkmal(merkmalId) ?: continue
            if (hartesEnde != null && fachIndex == lebenslaufKonf.faecher.lastIndex) continue

            val bisher = besteJeFach[fachIndex]
            if (bisher == null || vergleicheMerkmalRang(merkmalId, bisher) < 0) {
                besteJeFach[fachIndex] = merkmalId
            }
        }

        return lebenslaufKonf.faecher.mapIndexed { index, fachKonf ->
            if (hartesEnde != null && index == lebenslaufKonf.faecher.lastIndex) {
                LebenslaufFachErgebnis(
                    fachIndex = index,
                    titel = fachKonf.titel,
                    merkmalId = hartesEnde.id.code,
                    merkmalName = hartesEnde.titel,
                    eintrag = Nachklang(
                        jahr = hartesEnde.jahr,
                        datum = hartesEnde.jahr.toString(),
                        text = hartesEnde.text,
                    ),
                )
            } else {
                val gewaehlt = besteJeFach[index]
                val reg = gewaehlt?.let { merkmaleDaten.register[it] }
                LebenslaufFachErgebnis(
                    fachIndex = index,
                    titel = fachKonf.titel,
                    merkmalId = gewaehlt,
                    merkmalName = reg?.name,
                    eintrag = if (hartesEnde == null) reg?.nachklang else null,
                )
            }
        }
    }

    fun berechneLebenslauf(
        state: GameState,
        hartesEnde: HartesEndeErgebnis? = null,
    ): LebenslaufErgebnis {
        val stufen = metrics.alleStufen(state.werte)
        val merkmalSet = state.merkmale.toSet()
        val werteBilanz = metrics.werteAnzeige(state.werte, state.letzteAenderungen)

        if (hartesEnde != null) {
            return berechneAuffangnetzLebenslauf(state, hartesEnde, werteBilanz)
        }

        val ausgang = bestimmeAusgang(
            stufen = stufen,
            pfad = state.pfad,
            geschlecht = state.person?.geschlecht,
            merkmale = merkmalSet,
        )
        val faecher = berechneFaecher(state.merkmale, hartesEnde = null)

        val eintraege = mutableListOf<LebenslaufZeitleistenEintrag>()

        val kriegsende = lebenslaufKonf.kriegsende[state.pfad]
            ?: lebenslaufKonf.kriegsende.getValue(Pfad.HEIMAT)
        eintraege.add(
            LebenslaufZeitleistenEintrag(
                jahr = kriegsende.jahr,
                datum = kriegsende.datum,
                text = kriegsende.text,
                quelle = "Kriegsende",
            )
        )

        eintraege.add(
            LebenslaufZeitleistenEintrag(
                jahr = ausgang.eintrag.jahr,
                datum = ausgang.eintrag.datum,
                text = ausgang.eintrag.text,
                quelle = "Ausgang",
            )
        )

        for (fach in faecher) {
            val nachklang = fach.eintrag ?: continue
            val merkmalName = fach.merkmalName ?: continue
            eintraege.add(
                LebenslaufZeitleistenEintrag(
                    jahr = nachklang.jahr,
                    datum = nachklang.datum,
                    text = nachklang.text,
                    quelle = "${fach.titel}: $merkmalName",
                    fachTitel = fach.titel,
                    merkmalId = fach.merkmalId,
                )
            )
        }

        val politischeLage = lebenslaufKonf.politischeLage.firstOrNull { eintrag ->
            bedingungTrifftZu(
                bedingung = eintrag.bedingung,
                stufen = stufen,
                pfad = state.pfad,
                geschlecht = state.person?.geschlecht,
                merkmale = merkmalSet,
            )
        }
        if (politischeLage != null) {
            eintraege.add(
                LebenslaufZeitleistenEintrag(
                    jahr = politischeLage.eintrag.jahr,
                    datum = politischeLage.eintrag.datum,
                    text = politischeLage.eintrag.text,
                    quelle = "Lage",
                )
            )
        }

        val versailles = lebenslaufKonf.versailles
        eintraege.add(
            LebenslaufZeitleistenEintrag(
                jahr = versailles.jahr,
                datum = versailles.datum,
                text = versailles.text,
                quelle = "Versailles",
            )
        )

        // Stabile Sortierung nach Jahr: Reihenfolge innerhalb desselben Jahres bleibt erhalten.
        val sortiert = eintraege.sortedBy { it.jahr }

        return LebenslaufErgebnis(
            istVorzeitigerAbbruch = false,
            hartesEnde = null,
            ausgang = ausgang,
            faecher = faecher,
            zeitleiste = sortiert,
            fazit = erstelleFazitText(ausgang, stufen),
            werteBilanz = werteBilanz,
        )
    }

    /**
     * Respektvolles Auffangnetz: Auch bei einem vorzeitigen Abbruch vor 1919 erhalten
     * Schülerinnen und Schüler einen vollständigen, würdigen 4-Fächer-Lebenslauf
     * ohne Urteil oder „Game Over“-Sprache — ohne widersprüchliche Nachkriegseinträge.
     */
    private fun berechneAuffangnetzLebenslauf(
        state: GameState,
        hartesEnde: HartesEndeErgebnis,
        werteBilanz: List<WertStatus>,
    ): LebenslaufErgebnis {
        val faecher = berechneFaecher(state.merkmale, hartesEnde = hartesEnde)
        val zeitleiste = mutableListOf<LebenslaufZeitleistenEintrag>()

        val person = state.person
        if (person != null) {
            val pfadDef = content.konfiguration.pfade.definitionen[state.pfad]
            val startText = buildString {
                append(person.vollerName)
                append(", ")
                append(person.herkunftTitel)
                append(" (Jahrgang ")
                append(person.jahrgang)
                append("). ")
                if (pfadDef != null) {
                    append(pfadDef.marke)
                    append(" — ")
                    append(person.stand)
                    append(".")
                }
            }
            zeitleiste.add(
                LebenslaufZeitleistenEintrag(
                    jahr = 1914,
                    datum = "August 1914",
                    text = startText,
                    quelle = "Beginn",
                    fachTitel = lebenslaufKonf.faecher.getOrNull(0)?.titel,
                )
            )
        }

        val wichtigeEntscheidung = faecher.getOrNull(2)?.merkmalName
        if (wichtigeEntscheidung != null) {
            zeitleiste.add(
                LebenslaufZeitleistenEintrag(
                    jahr = hartesEnde.jahr,
                    datum = "1914 bis ${hartesEnde.jahr}",
                    text = "Geprägt durch Entscheidungen auf diesem Weg: $wichtigeEntscheidung.",
                    quelle = faecher[2].titel,
                    fachTitel = faecher[2].titel,
                    merkmalId = faecher[2].merkmalId,
                )
            )
        }

        zeitleiste.add(
            LebenslaufZeitleistenEintrag(
                jahr = hartesEnde.jahr,
                datum = hartesEnde.jahr.toString(),
                text = hartesEnde.text,
                quelle = hartesEnde.titel,
                fachTitel = lebenslaufKonf.faecher.lastOrNull()?.titel,
                merkmalId = hartesEnde.id.code,
            )
        )

        val fazit = "Dein Weg bricht im Jahr ${hartesEnde.jahr} ab (${hartesEnde.titel}). " +
            "Das ist kein persönliches Versagen: Zwischen 1914 und 1918 endeten Millionen " +
            "Lebenswege durch Hunger, Erschöpfung, Gewalt oder staatlichen Zwang, bevor der Krieg vorbei war."

        return LebenslaufErgebnis(
            istVorzeitigerAbbruch = true,
            hartesEnde = hartesEnde,
            ausgang = null,
            faecher = faecher,
            zeitleiste = zeitleiste.sortedBy { it.jahr },
            fazit = fazit,
            werteBilanz = werteBilanz,
        )
    }

    private fun erstelleFazitText(
        ausgang: AusgangDefinition,
        stufen: Map<WertSchluessel, Int>,
    ): String {
        val werteKonf = content.konfiguration.werte
        val schwer = werteKonf.reihenfolge.mapNotNull { schluessel ->
            if ((stufen[schluessel] ?: 0) >= 3) {
                werteKonf.definitionen.getValue(schluessel).bezeichnung
            } else {
                null
            }
        }
        if (ausgang.id == "weitergelebt" && schwer.isEmpty()) {
            return "Von rund dreizehn Millionen eingezogenen Männern kamen etwa elf Millionen zurück. " +
                "Ein Leben wie deines war der Regelfall, und auch dieser Regelfall war kein leichtes Leben."
        }
        if (schwer.isNotEmpty()) {
            val aufzaehlung = when (schwer.size) {
                1 -> schwer.first()
                else -> schwer.dropLast(1).joinToString(", ") + " und " + schwer.last()
            }
            return "Am schwersten wiegt am Ende: $aufzaehlung. Aus Millionen solcher Lebensläufe " +
                "entstand die Stimmung, in der die Republik von 1919 verteidigt oder abgelehnt wurde."
        }
        return "Was aus diesen Jahren folgte, entschied sich selten an einem einzigen Tag. " +
            "Es entschied sich daran, was Menschen danach über sie erzählten."
    }

    private fun vergleicheMerkmalRang(a: String, b: String): Int {
        val rangA = merkmaleDaten.register[a]?.rang ?: 0
        val rangB = merkmaleDaten.register[b]?.rang ?: 0
        if (rangA != rangB) return rangB.compareTo(rangA)

        val posA = registerIndex[a] ?: Int.MAX_VALUE
        val posB = registerIndex[b] ?: Int.MAX_VALUE
        if (posA != posB) return posA.compareTo(posB)

        return a.compareTo(b)
    }
}
