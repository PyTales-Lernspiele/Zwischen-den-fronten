package de.pytales.zdf

import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.engine.KotlinRandomSource
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.Kartentyp
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.SpielModus
import de.pytales.zdf.model.Stimmung
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.DemoBeispiele
import de.pytales.zdf.ui.state.UiStateMapper
import kotlin.random.Random
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNotNull
import kotlin.test.assertNull
import kotlin.test.assertTrue

class UiStateMapperTest {

    private val content = loadTestGameContent()
    private val engine = GameEngine(content, KotlinRandomSource(Random(1914)))

    @Test
    fun befindensLeisteBildetAlleVierWerteSegmenteDeltasUndZustandssaetzeAb() {
        var state = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.KURZ, direktwahlAktiv = true))
        state = engine.waehlePerson(state, "arbeiterschaft", Geschlecht.MAENNLICH, 18, direktwahlPfad = Pfad.FRONT)
        state = state.copy(
            werte = mapOf(
                WertSchluessel.VERSORGUNG to 5,     // Stufe 2 (Hungrig) -> 3/5 Segmente
                WertSchluessel.BELASTUNG to 1,      // Stufe 0 (Ausgeruht) -> 5/5 Segmente
                WertSchluessel.AUFMERKSAMKEIT to 9, // Stufe 3 (In den Akten) -> 2/5 Segmente
                WertSchluessel.RUECKHALT to 11,     // Stufe 0 (Nicht allein) -> 5/5 Segmente
            ),
            letzteAenderungen = mapOf(
                WertSchluessel.VERSORGUNG to -2,    // Hunger steigt (+2, schlechter)
                WertSchluessel.BELASTUNG to -1,     // Erschöpfung sinkt (-1, besser)
                WertSchluessel.AUFMERKSAMKEIT to 2, // Verdacht steigt (+2, schlechter)
            ),
        )

        val kacheln = UiStateMapper.mapBefindensLeiste(engine, state)
        assertEquals(
            listOf(
                WertSchluessel.VERSORGUNG,
                WertSchluessel.BELASTUNG,
                WertSchluessel.AUFMERKSAMKEIT,
                WertSchluessel.RUECKHALT,
            ),
            kacheln.map { it.schluessel },
        )

        val hunger = kacheln[0]
        assertEquals("Hunger", hunger.bezeichnung)
        assertEquals(2, hunger.stufe)
        assertEquals(3, hunger.gefuellteSegmente)
        assertEquals(5, hunger.segmenteGesamt)
        assertEquals("+2", hunger.aenderungsText)
        assertTrue(hunger.aenderungIstSchlechter)
        assertFalse(hunger.istKritisch)
        assertEquals(
            content.konfiguration.werte.definitionen.getValue(WertSchluessel.VERSORGUNG).zustandssaetze[2],
            hunger.zustandssatz,
        )
        assertTrue(hunger.erklaerung.isNotBlank())
        assertTrue(hunger.folge.isNotBlank())

        val erschoepfung = kacheln[1]
        assertEquals("Erschöpfung", erschoepfung.bezeichnung)
        assertEquals(5, erschoepfung.gefuellteSegmente)
        assertEquals("-1", erschoepfung.aenderungsText)
        assertFalse(erschoepfung.aenderungIstSchlechter)

        val verdacht = kacheln[2]
        assertEquals("Verdacht", verdacht.bezeichnung)
        assertEquals(2, verdacht.gefuellteSegmente)
        assertEquals("+2", verdacht.aenderungsText)
        assertTrue(verdacht.istKritisch)

        val einsamkeit = kacheln[3]
        assertEquals("Einsamkeit", einsamkeit.bezeichnung)
        assertNull(einsamkeit.aenderungsText)
        assertEquals(5, einsamkeit.gefuellteSegmente)
    }

    @Test
    fun liveEmotionDecktAlleVierzigMedienplanPortraitsUndAlleFuenfStimmungenAb() {
        val gesehenePortraits = mutableSetOf<String>()

        for (herkunft in content.herkunft.herkuenfte) {
            for (geschlecht in Geschlecht.entries) {
                var state = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.KURZ, direktwahlAktiv = true))
                state = engine.waehlePerson(state, herkunft.id, geschlecht, 18, direktwahlPfad = Pfad.HEIMAT)

                for (stimmung in Stimmung.entries) {
                    val simuliert = DemoBeispiele.stimmungSimulieren(engine, state, stimmung)
                    val ui = UiStateMapper.mapLiveEmotion(engine, simuliert)

                    assertEquals(stimmung, ui.stimmung)
                    assertEquals("portrait_${herkunft.id}_${geschlecht.code}_${stimmung.code}", ui.portraitId)
                    assertEquals("portraits/${ui.portraitId}.webp", ui.portraitRessourcenPfad)
                    assertTrue(ui.istImMedienplan, "Portrait fehlt im Medienplan: ${ui.portraitId}")
                    assertTrue(ui.personName.isNotBlank())
                    assertTrue(ui.initialen.length in 1..2)
                    assertTrue(ui.zustandssatz.isNotBlank())
                    gesehenePortraits += ui.portraitId
                }
            }
        }

        assertEquals(40, gesehenePortraits.size)
        assertEquals(content.medienplan.portraits.map { it.id }.toSet(), gesehenePortraits)

        // Fallback ohne zugewiesene Person (Startzustand: Heimat-Basisversorgung 6 -> HUNGRIG)
        val leer = UiStateMapper.mapLiveEmotion(engine, engine.neuesSpiel())
        assertEquals(Stimmung.HUNGRIG, leer.stimmung)
        assertEquals("portrait_unbekannt_hungrig", leer.portraitId)
        assertFalse(leer.istImMedienplan)
        assertEquals("ZF", leer.initialen)

        val leerNeutral = UiStateMapper.mapLiveEmotion(
            engine,
            DemoBeispiele.stimmungSimulieren(engine, engine.neuesSpiel(), Stimmung.NEUTRAL),
        )
        assertEquals(Stimmung.NEUTRAL, leerNeutral.stimmung)
        assertEquals("portrait_unbekannt_neutral", leerNeutral.portraitId)
    }

    @Test
    fun alleEreignisseUndAlleFuenfKartentypenWerdenSauberAufUiModelleAbgebildet() {
        val kopfzeilen = Kartentyp.entries.map { UiStateMapper.kartentypKopfzeile(it) }.toSet()
        assertEquals(5, kopfzeilen.size, "Alle 5 Kartentypen müssen eigene Dokumentköpfe besitzen.")

        for (typ in Kartentyp.entries) {
            val liste = DemoBeispiele.ereignisseFuerTyp(content, typ)
            assertTrue(liste.isNotEmpty(), "Kein reales Ereignis für Kartentyp $typ gefunden.")
        }

        // Alle 104 Ereignisse aus content/ereignisse.json vollständig durchprüfen
        var zaehlerMitHinweis = 0
        for (ereignis in content.ereignisse.ereignisse) {
            val jahr = ereignis.jahre.firstOrNull() ?: 1914
            val pfad = ereignis.pfade.firstOrNull() ?: Pfad.HEIMAT
            val ui = UiStateMapper.mapEntscheidungsKarte(
                content = content,
                ereignis = ereignis,
                aufgeloesterText = ereignis.text.standard,
                jahr = jahr,
                pfad = pfad,
            )
            assertEquals(2, ui.optionen.size, "2-Wahl-Regel verletzt bei ${ereignis.id}")
            assertTrue(ui.szenenbild.schauplatzLabel.isNotBlank())
            assertTrue(
                ui.szenenbild.istStufe1Verfuegbar,
                "Schauplatzbild '${ereignis.schauplatzBild}' fehlt in medienplan.json (Ereignis ${ereignis.id})",
            )
            assertTrue(ui.szenenbild.szenenRessourcenPfad.endsWith(".webp"))
            assertTrue(ui.szenenbild.fallbackRessourcenPfad.endsWith(".webp"))
            assertTrue(ui.quelle.artLabel.isNotBlank())
            assertTrue(ui.quelle.einordnung.isNotBlank())
            if (ui.optionen.any { it.hinweis != null }) {
                zaehlerMitHinweis++
            }
        }
        assertTrue(zaehlerMitHinweis > 0, "Erwartet reale Ereignisse mit optionalem Hinweis-Stempel.")

        // Komplette Demo-Entscheidung inklusive Ausgangs-Mapping prüfen
        val marsch = content.ereignisById.getValue("front_1914_marsch")
        val start = DemoBeispiele.startZustand(engine, "arbeiterschaft", Geschlecht.MAENNLICH, marsch)
        val nachWahl = engine.waehleOption(start, 0)
        val ausgangPhase = nachWahl.phase as? GamePhase.EreignisAusgang
        assertNotNull(ausgangPhase)
        val ausgangUi = UiStateMapper.mapEreignisAusgang(engine, ausgangPhase)
        assertEquals("front_1914_marsch", ausgangUi.ereignisId)
        assertEquals(marsch.optionen[0].titel, ausgangUi.gewaehlterTitel)
        assertTrue(ausgangUi.ausgangsText.isNotBlank())
    }
}
