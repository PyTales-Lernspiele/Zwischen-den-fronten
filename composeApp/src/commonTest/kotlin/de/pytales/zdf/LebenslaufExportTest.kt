package de.pytales.zdf

import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.engine.HartesEndeErgebnis
import de.pytales.zdf.engine.KotlinRandomSource
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.HartesEndeId
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.SpielModus
import de.pytales.zdf.ui.export.LebenslaufExporter
import de.pytales.zdf.ui.state.SpielController
import kotlin.random.Random
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertIs
import kotlin.test.assertNotNull
import kotlin.test.assertTrue

/**
 * Prüfsuite für AP 6 — Klassenzimmer-Export & Druckaufbereitung (`LebenslaufExporter`).
 */
class LebenslaufExportTest {

    private val content = loadTestGameContent()

    @Test
    fun regulaererDurchgangErzeugtVollstaendigenKlartextUndDruckHtml() {
        val controller = spieleRegulaerBis1919(Pfad.HEIMAT, "buergertum", Geschlecht.WEIBLICH)
        val gameState = controller.aktuellerZustand.gameState
        val phase = assertIs<GamePhase.Abgeschlossen>(gameState.phase)
        val person = assertNotNull(gameState.person)
        val ausgang = assertNotNull(phase.lebenslauf.ausgang)

        val dokument = LebenslaufExporter.erstelleDokument(
            content = content,
            gameState = gameState,
            phase = phase,
            mitProtokoll = true,
        )

        // Dateiname & Titel
        assertTrue(dokument.dateinameBasis.startsWith("lebenslauf_"))
        assertTrue(dokument.dateinameBasis.endsWith("_1914_1919"))
        assertTrue(dokument.dateinameBasis.all { it in 'a'..'z' || it in '0'..'9' || it == '_' })
        assertTrue(dokument.titel.contains("1914–1919"))
        assertTrue(dokument.titel.contains(person.vollerName))

        // Klartext enthält alle Pflichtbestandteile für den Unterricht
        val text = dokument.klartext
        assertTrue(text.contains("ZWISCHEN DEN FRONTEN"))
        assertTrue(text.contains(person.vollerName))
        assertTrue(text.contains(person.herkunftTitel))
        assertTrue(text.contains(ausgang.titel))
        assertTrue(text.contains("4-FÄCHER-LEBENSLAUF"))
        for (i in 1..4) {
            assertTrue(text.contains("Fach $i"), "Fach $i fehlt im Export-Klartext")
        }
        assertTrue(text.contains("CHRONOLOGISCHE ZEITLEISTE"))
        assertTrue(text.contains("ENTSCHEIDUNGSPROTOKOLL"))
        assertTrue(text.contains("BEFINDENSSTAND AM ENDE (1919"))
        assertTrue(text.contains("Gesprächsimpuls:"))

        // Druck-HTML ist ein vollständiges, eigenständiges A4-Druckdokument
        val html = dokument.druckHtml
        assertTrue(html.startsWith("<!DOCTYPE html>"))
        assertTrue(html.contains("<html lang=\"de\">"))
        assertTrue(html.contains("@page { size: A4;"))
        assertTrue(html.contains("@media print"))
        assertTrue(html.contains("window.print()"))
        assertTrue(html.contains("Name / Klasse:"))
        assertTrue(html.contains(LebenslaufExporter.escapeHtml(person.vollerName)))
        assertTrue(html.contains(LebenslaufExporter.escapeHtml(ausgang.titel)))
        assertTrue(html.contains("Entscheidungsprotokoll"))
        assertTrue(html.contains("<table class=\"protokoll\">"))

        // Option „ohne Entscheidungsprotokoll“ lässt das Protokoll in beiden Formaten sauber weg
        val ohneProtokoll = LebenslaufExporter.erstelleDokument(
            content = content,
            gameState = gameState,
            phase = phase,
            mitProtokoll = false,
        )
        assertFalse(ohneProtokoll.klartext.contains("ENTSCHEIDUNGSPROTOKOLL"))
        assertFalse(ohneProtokoll.druckHtml.contains("<table class=\"protokoll\">"))
    }

    @Test
    fun auffangnetzExportBleibtRespektvollUndDokumentiertErreichtenWeg() {
        val engine = GameEngine(content, KotlinRandomSource(Random(1916)))
        var state = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.KURZ, direktwahlAktiv = true))
        state = engine.waehlePerson(state, "arbeiterschaft", Geschlecht.MAENNLICH, 35, direktwahlPfad = Pfad.FRONT)

        val hartesEnde = HartesEndeErgebnis(
            id = HartesEndeId.ENDE_ZUSAMMENBRUCH,
            titel = "Zusammengebrochen",
            text = content.konfiguration.harteEnden.texte.getValue(HartesEndeId.ENDE_ZUSAMMENBRUCH).text,
            jahr = 1916,
        )
        val lebenslauf = engine.lebenslaufCalculator.berechneLebenslauf(state.copy(jahr = 1916), hartesEnde)
        val phase = GamePhase.Abgeschlossen(hartesEnde = hartesEnde, lebenslauf = lebenslauf)

        val dokument = LebenslaufExporter.erstelleDokument(
            content = content,
            gameState = state.copy(jahr = 1916, phase = phase),
            phase = phase,
            mitProtokoll = true,
        )

        assertTrue(dokument.dateinameBasis.endsWith("_1914_1916"))
        assertTrue(dokument.klartext.contains("VORZEITIGER EINSCHNITT (1916)"))
        assertTrue(dokument.klartext.contains("kein persönliches Versagen"))
        assertTrue(dokument.klartext.contains("Zusammengebrochen"))
        assertFalse(dokument.klartext.contains("Game Over", ignoreCase = true))

        assertTrue(dokument.druckHtml.contains("Vorzeitiger Einschnitt (1916): Zusammengebrochen"))
        assertTrue(dokument.druckHtml.contains("Kein persönliches Versagen"))
    }

    @Test
    fun htmlEscapingUndDateinamenBereinigungSindSicher() {
        assertEquals(
            "&lt;script&gt;alert(&quot;x&quot; &amp; &#39;y&#39;)&lt;/script&gt;",
            LebenslaufExporter.escapeHtml("<script>alert(\"x\" & 'y')</script>"),
        )
        assertEquals(
            "lebenslauf_kaethe_mueller_koeln_strasse_1914_1919",
            LebenslaufExporter.bereinigeDateiname("Lebenslauf Käthe Müller / Köln-Straße (1914–1919)!!"),
        )
        assertEquals(
            "lebenslauf_zwischen_den_fronten",
            LebenslaufExporter.bereinigeDateiname("   ///   "),
        )
    }

    private fun spieleRegulaerBis1919(
        pfad: Pfad,
        herkunftId: String,
        geschlecht: Geschlecht,
    ): SpielController {
        for (seed in 1..30) {
            val controller = SpielController(content, KotlinRandomSource(Random(4000 + seed)))
            controller.waehleModus(SpielModus.KURZ)
            controller.setzeDirektwahlAktiv(true)
            controller.durchgangBeginnen()
            controller.waehlePerson(herkunftId, geschlecht, 18, direktwahlPfad = pfad)

            var schritte = 0
            while (schritte < 120) {
                schritte++
                when (val phase = controller.aktuellerZustand.gameState.phase) {
                    is GamePhase.ErwerbWahl -> controller.waehleErwerb(phase.optionen.first().id)
                    is GamePhase.MusterungErgebnis -> controller.bestaetigeMusterung()
                    is GamePhase.KapitelStart -> controller.starteKapitel()
                    is GamePhase.EreignisAnzeige -> controller.waehleOption(0)
                    is GamePhase.EreignisAusgang -> controller.weiterNachAusgang()
                    is GamePhase.KapitelAbschluss -> controller.naechstesKapitelStarten()
                    is GamePhase.Abgeschlossen -> {
                        if (!phase.lebenslauf.istVorzeitigerAbbruch) return controller
                        break
                    }

                    else -> break
                }
            }
        }
        error("Kein regulärer 1919-Durchgang gefunden.")
    }
}
