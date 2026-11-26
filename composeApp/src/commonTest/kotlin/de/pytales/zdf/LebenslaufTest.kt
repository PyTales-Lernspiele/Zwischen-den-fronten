package de.pytales.zdf

import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GameState
import de.pytales.zdf.engine.HartesEndeErgebnis
import de.pytales.zdf.engine.KotlinRandomSource
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.HartesEndeId
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.SpielModus
import de.pytales.zdf.model.WertSchluessel
import kotlin.random.Random
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNotNull
import kotlin.test.assertNull
import kotlin.test.assertTrue

class LebenslaufTest {

    private val content = loadTestGameContent()
    private val engine = GameEngine(content, KotlinRandomSource(Random(77)))
    private val calc = engine.lebenslaufCalculator

    @Test
    fun alleZehnDeklarativenAusgaengeWerdenKorrektBestimmt() {
        val ruhig = mapOf(
            WertSchluessel.VERSORGUNG to 1,
            WertSchluessel.BELASTUNG to 1,
            WertSchluessel.AUFMERKSAMKEIT to 1,
            WertSchluessel.RUECKHALT to 1,
        )

        // 1. gezeichnet (rang 90): versorgung >= 3
        assertEquals(
            "gezeichnet",
            calc.bestimmeAusgang(ruhig + (WertSchluessel.VERSORGUNG to 3), Pfad.HEIMAT, Geschlecht.WEIBLICH, emptySet()).id,
        )
        // 2. nervenkrank (rang 88): belastung >= 3
        assertEquals(
            "nervenkrank",
            calc.bestimmeAusgang(ruhig + (WertSchluessel.BELASTUNG to 3), Pfad.FRONT, Geschlecht.MAENNLICH, emptySet()).id,
        )
        // 3. aktenkundig (rang 86): aufmerksamkeit >= 3
        assertEquals(
            "aktenkundig",
            calc.bestimmeAusgang(ruhig + (WertSchluessel.AUFMERKSAMKEIT to 3), Pfad.ETAPPE, Geschlecht.MAENNLICH, emptySet()).id,
        )
        // 4. vereinsamt (rang 84): rueckhalt >= 3
        assertEquals(
            "vereinsamt",
            calc.bestimmeAusgang(ruhig + (WertSchluessel.RUECKHALT to 3), Pfad.HEIMAT, Geschlecht.WEIBLICH, emptySet()).id,
        )
        // Priorität: gezeichnet (90) schlägt nervenkrank (88)
        assertEquals(
            "gezeichnet",
            calc.bestimmeAusgang(
                ruhig + (WertSchluessel.VERSORGUNG to 3) + (WertSchluessel.BELASTUNG to 4),
                Pfad.FRONT, Geschlecht.MAENNLICH, emptySet(),
            ).id,
        )
        // 5. nicht_angekommen (rang 70): front/etappe + (belastung >= 2 || rueckhalt >= 2)
        assertEquals(
            "nicht_angekommen",
            calc.bestimmeAusgang(ruhig + (WertSchluessel.BELASTUNG to 2), Pfad.ETAPPE, Geschlecht.MAENNLICH, emptySet()).id,
        )
        // 6. in_der_bewegung (rang 68): (arbeiterschaft/ruestung) && (vorangegangen || aufmerksamkeit >= 2)
        assertEquals(
            "in_der_bewegung",
            calc.bestimmeAusgang(ruhig, Pfad.HEIMAT, Geschlecht.MAENNLICH, setOf("arbeiterschaft", "vorangegangen")).id,
        )
        assertEquals(
            "in_der_bewegung",
            calc.bestimmeAusgang(
                ruhig + (WertSchluessel.AUFMERKSAMKEIT to 2),
                Pfad.HEIMAT, Geschlecht.MAENNLICH, setOf("ruestung"),
            ).id,
        )
        // 7. auf_eigenen_beinen (rang 66): w + Erwerbsmerkmal + belastung <= 2
        assertEquals(
            "auf_eigenen_beinen",
            calc.bestimmeAusgang(
                ruhig + (WertSchluessel.BELASTUNG to 2),
                Pfad.HEIMAT, Geschlecht.WEIBLICH, setOf("haushalt"),
            ).id,
        )
        // 8. bewahrt_und_verloren (rang 64): buergertum/adel + versorgung <= 1
        assertEquals(
            "bewahrt_und_verloren",
            calc.bestimmeAusgang(ruhig, Pfad.HEIMAT, Geschlecht.MAENNLICH, setOf("buergertum")).id,
        )
        // 9. zusammengeblieben (rang 40): rueckhalt <= 1 && belastung <= 2 && versorgung <= 2
        assertEquals(
            "zusammengeblieben",
            calc.bestimmeAusgang(
                mapOf(
                    WertSchluessel.VERSORGUNG to 2,
                    WertSchluessel.BELASTUNG to 2,
                    WertSchluessel.AUFMERKSAMKEIT to 1,
                    WertSchluessel.RUECKHALT to 1,
                ),
                Pfad.HEIMAT, Geschlecht.MAENNLICH, setOf("landbevoelkerung"),
            ).id,
        )
        // 10. weitergelebt (rang 0): Auffangausgang, wenn keine spezifische Lage greift
        assertEquals(
            "weitergelebt",
            calc.bestimmeAusgang(
                mapOf(
                    WertSchluessel.VERSORGUNG to 2,
                    WertSchluessel.BELASTUNG to 2,
                    WertSchluessel.AUFMERKSAMKEIT to 1,
                    WertSchluessel.RUECKHALT to 2,
                ),
                Pfad.HEIMAT, Geschlecht.MAENNLICH, setOf("landbevoelkerung"),
            ).id,
        )
    }

    @Test
    fun vierFaecherRegelUndChronologischeZeitleiste() {
        var state = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.LANG, direktwahlAktiv = true))
        state = engine.waehlePerson(state, "buergertum", Geschlecht.MAENNLICH, 18, direktwahlPfad = Pfad.FRONT)
        state = state.copy(
            jahr = 1919,
            werte = mapOf(
                WertSchluessel.VERSORGUNG to 8,
                WertSchluessel.BELASTUNG to 5,
                WertSchluessel.AUFMERKSAMKEIT to 2,
                WertSchluessel.RUECKHALT to 8,
            ),
            merkmale = listOf(
                "buergertum",               // Fach 0 (rang 34)
                "kriegsfreiwillig",         // Fach 1 (rang 60)
                "offizier",                 // Fach 1 (rang 58) -> kriegsfreiwillig gewinnt!
                "kamerad_gedeckt",          // Fach 2 (rang 78)
                "ohne_mantel",              // Fach 2 (rang 34) -> kamerad_gedeckt gewinnt!
                "wirtshaus_widersprochen",  // Fach 3 (schlussMerkmale)
            ),
        )

        val lebenslauf = engine.erstelleLebenslauf(state)
        assertFalse(lebenslauf.istVorzeitigerAbbruch)
        assertEquals(4, lebenslauf.faecher.size)
        assertEquals("buergertum", lebenslauf.faecher[0].merkmalId)
        assertEquals("kriegsfreiwillig", lebenslauf.faecher[1].merkmalId)
        assertEquals("kamerad_gedeckt", lebenslauf.faecher[2].merkmalId)
        assertEquals("wirtshaus_widersprochen", lebenslauf.faecher[3].merkmalId)

        // Zeitleiste muss chronologisch sortiert sein und Kriegsende + Versailles + Dolchstoß-Lage enthalten
        val jahre = lebenslauf.zeitleiste.map { it.jahr }
        assertEquals(jahre.sorted(), jahre)
        assertTrue(lebenslauf.zeitleiste.any { it.quelle == "Kriegsende" })
        assertTrue(lebenslauf.zeitleiste.any { it.quelle == "Versailles" })
        assertTrue(lebenslauf.zeitleiste.any { it.quelle == "Lage" && it.text.contains("Hindenburg") })

        // Leeres Fach bleibt leer (kein Nachrücken aus anderen Fächern)
        val ohneTat = calc.berechneFaecher(listOf("arbeiterschaft", "ruestung", "wirtshaus_geschwiegen"))
        assertEquals("arbeiterschaft", ohneTat[0].merkmalId)
        assertEquals("ruestung", ohneTat[1].merkmalId)
        assertNull(ohneTat[2].merkmalId)
        assertEquals("wirtshaus_geschwiegen", ohneTat[3].merkmalId)
    }

    @Test
    fun respektvollesAuffangnetzFuerAlleVierHartenEnden() {
        var basis = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.KURZ, direktwahlAktiv = true))
        basis = engine.waehlePerson(basis, "arbeiterschaft", Geschlecht.WEIBLICH, 35, direktwahlPfad = Pfad.HEIMAT)
        basis = engine.waehleErwerb(basis, "ruestung")
        basis = basis.copy(
            jahr = 1917,
            merkmale = basis.merkmale + "vorangegangen",
        )

        for (endeId in HartesEndeId.entries) {
            val textDef = content.konfiguration.harteEnden.texte.getValue(endeId)
            val hart = HartesEndeErgebnis(
                id = endeId,
                titel = textDef.titel,
                text = textDef.text,
                jahr = 1917,
            )
            val lebenslauf = engine.erstelleLebenslauf(basis, hartesEnde = hart)
            assertTrue(lebenslauf.istVorzeitigerAbbruch)
            assertEquals(endeId, lebenslauf.hartesEnde?.id)
            assertNull(lebenslauf.ausgang)
            assertEquals(4, lebenslauf.faecher.size)
            assertNotNull(lebenslauf.faecher[0].merkmalName)
            assertEquals("ruestung", lebenslauf.faecher[1].merkmalId)
            assertEquals("vorangegangen", lebenslauf.faecher[2].merkmalId)
            assertEquals(textDef.titel, lebenslauf.faecher[3].merkmalName)
            assertTrue(lebenslauf.zeitleiste.all { it.jahr <= 1917 })
            assertTrue(lebenslauf.fazit.contains("1917"))
        }
    }
}
