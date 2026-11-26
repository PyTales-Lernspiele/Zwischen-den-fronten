package de.pytales.zdf

import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.engine.KotlinRandomSource
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.HartesEndeId
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.SpielModus
import de.pytales.zdf.model.Stimmung
import de.pytales.zdf.model.WertSchluessel
import kotlin.random.Random
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNull
import kotlin.test.assertTrue

class ValuesAndLiveEmotionTest {

    private val content = loadTestGameContent()
    private val engine = GameEngine(content, KotlinRandomSource(Random(1234)))
    private val metrics = engine.metrics

    @Test
    fun stufenUndBalkenVollIstGutFuerAlleVierWerte() {
        // versorgung & rueckhalt: hochIstGut = true (12 -> Stufe 0, 0 -> Stufe 4)
        assertEquals(0, metrics.stufeVonWert(WertSchluessel.VERSORGUNG, 12))
        assertEquals(0, metrics.stufeVonWert(WertSchluessel.VERSORGUNG, 11))
        assertEquals(1, metrics.stufeVonWert(WertSchluessel.VERSORGUNG, 10))
        assertEquals(1, metrics.stufeVonWert(WertSchluessel.VERSORGUNG, 8))
        assertEquals(2, metrics.stufeVonWert(WertSchluessel.VERSORGUNG, 7))
        assertEquals(2, metrics.stufeVonWert(WertSchluessel.VERSORGUNG, 5))
        assertEquals(3, metrics.stufeVonWert(WertSchluessel.VERSORGUNG, 4))
        assertEquals(3, metrics.stufeVonWert(WertSchluessel.VERSORGUNG, 2))
        assertEquals(4, metrics.stufeVonWert(WertSchluessel.VERSORGUNG, 1))
        assertEquals(4, metrics.stufeVonWert(WertSchluessel.VERSORGUNG, 0))

        // belastung & aufmerksamkeit: hochIstGut = false (0 -> Stufe 0, 12 -> Stufe 4)
        assertEquals(0, metrics.stufeVonWert(WertSchluessel.BELASTUNG, 0))
        assertEquals(0, metrics.stufeVonWert(WertSchluessel.BELASTUNG, 1))
        assertEquals(1, metrics.stufeVonWert(WertSchluessel.BELASTUNG, 2))
        assertEquals(1, metrics.stufeVonWert(WertSchluessel.BELASTUNG, 4))
        assertEquals(2, metrics.stufeVonWert(WertSchluessel.BELASTUNG, 5))
        assertEquals(2, metrics.stufeVonWert(WertSchluessel.BELASTUNG, 7))
        assertEquals(3, metrics.stufeVonWert(WertSchluessel.BELASTUNG, 8))
        assertEquals(3, metrics.stufeVonWert(WertSchluessel.BELASTUNG, 10))
        assertEquals(4, metrics.stufeVonWert(WertSchluessel.BELASTUNG, 11))
        assertEquals(4, metrics.stufeVonWert(WertSchluessel.BELASTUNG, 12))

        // Balken voll = gut: Stufe 0 -> 5 gefüllt, Stufe 4 -> 1 Restsegment
        assertEquals(5, metrics.gefuellteSegmente(0))
        assertEquals(4, metrics.gefuellteSegmente(1))
        assertEquals(3, metrics.gefuellteSegmente(2))
        assertEquals(2, metrics.gefuellteSegmente(3))
        assertEquals(1, metrics.gefuellteSegmente(4))

        assertTrue(metrics.segmentGefuellt(4, 0))
        assertFalse(metrics.segmentGefuellt(4, 1))
        assertTrue(metrics.segmentGefuellt(0, 4))
        assertFalse(metrics.segmentGefuellt(1, 4))
    }

    @Test
    fun begrenzungUndWirkungZeilenBildenAnzeigeVorzeichenKorrektAb() {
        val start = mapOf(
            WertSchluessel.VERSORGUNG to 1,
            WertSchluessel.BELASTUNG to 11,
            WertSchluessel.AUFMERKSAMKEIT to 0,
            WertSchluessel.RUECKHALT to 12,
        )
        val (neu, diff) = metrics.werteAnwenden(
            start,
            mapOf(
                WertSchluessel.VERSORGUNG to -3,
                WertSchluessel.BELASTUNG to 3,
                WertSchluessel.AUFMERKSAMKEIT to -2,
                WertSchluessel.RUECKHALT to 2,
            ),
        )
        assertEquals(0, neu[WertSchluessel.VERSORGUNG])
        assertEquals(12, neu[WertSchluessel.BELASTUNG])
        assertEquals(0, neu[WertSchluessel.AUFMERKSAMKEIT])
        assertEquals(12, neu[WertSchluessel.RUECKHALT])
        assertEquals(mapOf(WertSchluessel.VERSORGUNG to -1, WertSchluessel.BELASTUNG to 1), diff)

        // Hunger sinkt (versorgung +2 -> gezeigt -2, schlechter = false)
        val zeilen = metrics.wirkungZeilen(
            mapOf(
                WertSchluessel.VERSORGUNG to -2,
                WertSchluessel.BELASTUNG to -1,
            )
        )
        assertEquals(2, zeilen.size)
        assertEquals("Hunger", zeilen[0].name)
        assertEquals("+2", zeilen[0].zeichen)
        assertTrue(zeilen[0].schlechter)
        assertEquals("steigt deutlich", zeilen[0].richtung)

        assertEquals("Erschöpfung", zeilen[1].name)
        assertEquals("-1", zeilen[1].zeichen)
        assertFalse(zeilen[1].schlechter)
        assertEquals("sinkt", zeilen[1].richtung)
    }

    @Test
    fun liveEmotionUndPortraitIdReagierenAufSchwaechstenWertUndUeberschreibung() {
        val gut = mapOf(
            WertSchluessel.VERSORGUNG to 9,     // Stufe 1
            WertSchluessel.BELASTUNG to 3,      // Stufe 1
            WertSchluessel.AUFMERKSAMKEIT to 1, // Stufe 0
            WertSchluessel.RUECKHALT to 9,      // Stufe 1
        )
        assertEquals(Stimmung.NEUTRAL, metrics.berechneStimmung(gut))

        // Ab Stufe 2 reagiert die Kachel auf den schwächsten Wert
        val hungrig = gut + (WertSchluessel.VERSORGUNG to 6) // Stufe 2
        assertEquals(Stimmung.HUNGRIG, metrics.berechneStimmung(hungrig))

        val erschoepft = gut + (WertSchluessel.BELASTUNG to 8) // Stufe 3
        assertEquals(Stimmung.ERSCHOEPFT, metrics.berechneStimmung(erschoepft))

        val angst = gut + (WertSchluessel.AUFMERKSAMKEIT to 9) // Stufe 3
        assertEquals(Stimmung.ANGST, metrics.berechneStimmung(angst))

        val einsam = gut + (WertSchluessel.RUECKHALT to 3) // Stufe 3
        assertEquals(Stimmung.EINSAM, metrics.berechneStimmung(einsam))

        // Explizite Überschreibung schlägt den berechneten Zustand
        assertEquals(Stimmung.ANGST, metrics.berechneStimmung(gut, ueberschreibung = Stimmung.ANGST))

        // Portrait-ID und Zustandssatz über GameState prüfen
        var state = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.KURZ, direktwahlAktiv = true))
        state = engine.waehlePerson(state, "buergertum", Geschlecht.WEIBLICH, 35, direktwahlPfad = Pfad.ETAPPE)
        state = state.copy(werte = erschoepft)

        val snap = engine.liveEmotion(state)
        assertEquals(Stimmung.ERSCHOEPFT, snap.stimmung)
        assertEquals("portrait_buergertum_w_erschoepft", snap.portraitId)
        assertEquals(WertSchluessel.BELASTUNG, snap.ausloesenderWert)
        assertFalse(snap.istUeberschrieben)
        assertEquals(
            content.konfiguration.werte.definitionen.getValue(WertSchluessel.BELASTUNG).zustandssaetze[3],
            engine.zustandssatz(state),
        )

        // Ereignis- & Options-Überschreibung live prüfen (`front_1917_steckruebe` hat stimmung = hungrig)
        val steckruebe = content.ereignisById.getValue("front_1917_steckruebe")
        val anzeigeState = state.copy(
            werte = gut,
            stimmungUeberschreibung = steckruebe.stimmung,
            phase = GamePhase.EreignisAnzeige(steckruebe, steckruebe.text.standard),
        )
        assertEquals(Stimmung.HUNGRIG, engine.liveEmotion(anzeigeState).stimmung)
        assertEquals("portrait_buergertum_w_hungrig", engine.portraitId(anzeigeState))
        assertTrue(engine.liveEmotion(anzeigeState).istUeberschrieben)

        // Options-Überschreibung (`front_1914_erster_toter` Option 0 -> stimmung = einsam)
        val toter = content.ereignisById.getValue("front_1914_erster_toter")
        val vorWahl = state.copy(
            werte = gut,
            stimmungUeberschreibung = toter.stimmung,
            phase = GamePhase.EreignisAnzeige(toter, toter.text.standard),
        )
        assertEquals(Stimmung.NEUTRAL, engine.liveEmotion(vorWahl).stimmung)
        val nachWahl = engine.waehleOption(vorWahl, 0)
        assertEquals(Stimmung.EINSAM, engine.liveEmotion(nachWahl).stimmung)
        assertEquals("portrait_buergertum_w_einsam", engine.portraitId(nachWahl))
    }

    @Test
    fun harteAbbruchschwellenEpilogSchutzUndVerdachtsverjaehrung() {
        val basis = mapOf(
            WertSchluessel.VERSORGUNG to 5,
            WertSchluessel.BELASTUNG to 5,
            WertSchluessel.AUFMERKSAMKEIT to 5,
            WertSchluessel.RUECKHALT to 0, // Einsamkeit allein bricht niemals ab!
        )
        assertNull(metrics.pruefeHartesEnde(basis, 1916, 1919))
        assertEquals(
            HartesEndeId.ENDE_VERHUNGERT,
            metrics.pruefeHartesEnde(basis + (WertSchluessel.VERSORGUNG to 0), 1916, 1919),
        )
        assertEquals(
            HartesEndeId.ENDE_ZUSAMMENBRUCH,
            metrics.pruefeHartesEnde(basis + (WertSchluessel.BELASTUNG to 12), 1917, 1919),
        )
        assertEquals(
            HartesEndeId.ENDE_VERHAFTET,
            metrics.pruefeHartesEnde(basis + (WertSchluessel.AUFMERKSAMKEIT to 12), 1918, 1919),
        )

        // Ab Epilog 1919 greifen harte Werteschwellen nicht mehr
        assertNull(metrics.pruefeHartesEnde(basis + (WertSchluessel.VERSORGUNG to 0), 1919, 1919))
        assertNull(metrics.pruefeHartesEnde(basis + (WertSchluessel.BELASTUNG to 12), 1919, 1919))

        // wirkungEntschaerfen schützt beim Wechsel nach 1919
        val kritisch = mapOf(
            WertSchluessel.VERSORGUNG to 1,
            WertSchluessel.BELASTUNG to 11,
            WertSchluessel.AUFMERKSAMKEIT to 11,
            WertSchluessel.RUECKHALT to 2,
        )
        val entschaerft = metrics.wirkungEntschaerfen(
            kritisch,
            mapOf(
                WertSchluessel.VERSORGUNG to -2,
                WertSchluessel.BELASTUNG to 2,
                WertSchluessel.AUFMERKSAMKEIT to 2,
                WertSchluessel.RUECKHALT to -1,
            ),
        )
        assertEquals(mapOf(WertSchluessel.RUECKHALT to -1), entschaerft)

        // Verdachtsverjährung: Nach 3 ruhigen Ziehungen sinkt aufmerksamkeit um 1
        val neutralEv = content.ereignisById.getValue("front_1914_erster_toter") // Option 1 ändert aufmerksamkeit nicht
        var s = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.LANG, direktwahlAktiv = true))
        s = engine.waehlePerson(s, "arbeiterschaft", Geschlecht.MAENNLICH, 18, direktwahlPfad = Pfad.FRONT)
        s = s.copy(
            werte = s.werte + (WertSchluessel.AUFMERKSAMKEIT to 5),
            verdachtStand = 5,
            verdachtRuhig = 0,
        )

        repeat(2) {
            s = s.copy(phase = GamePhase.EreignisAnzeige(neutralEv, neutralEv.text.standard))
            s = engine.waehleOption(s, 1)
            assertEquals(5, s.werte[WertSchluessel.AUFMERKSAMKEIT])
        }
        // Dritte ruhige Ziehung senkt Verdacht auf 4
        s = s.copy(phase = GamePhase.EreignisAnzeige(neutralEv, neutralEv.text.standard))
        s = engine.waehleOption(s, 1)
        assertEquals(4, s.werte[WertSchluessel.AUFMERKSAMKEIT])
        assertEquals(0, s.verdachtRuhig)
    }
}
