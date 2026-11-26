package de.pytales.zdf

import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.engine.KotlinRandomSource
import de.pytales.zdf.engine.RandomSource
import de.pytales.zdf.model.Ereignis
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.MusterungsGrad
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.SpielModus
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.state.SpielController
import de.pytales.zdf.ui.state.UiStateMapper
import de.pytales.zdf.ui.state.ZurueckErgebnis
import de.pytales.zdf.ui.theme.Schriftgroesse
import kotlin.random.Random
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertIs
import kotlin.test.assertNotNull
import kotlin.test.assertNull
import kotlin.test.assertTrue

class SpielControllerTest {

    private val content = loadTestGameContent()

    @Test
    fun startmenueEinstellungenGrundsaetzeUndKopfleisteEinklappen() {
        val controller = SpielController(content, KotlinRandomSource(Random(1914)))

        val start = controller.aktuellerZustand
        assertIs<GamePhase.Start>(start.gameState.phase)
        assertEquals(SpielModus.KURZ, start.gameState.modus)
        assertFalse(start.gameState.direktwahlAktiv)
        assertEquals(Schriftgroesse.MITTEL, start.schriftgroesse)
        assertFalse(start.reduzierteAnimationen)
        assertFalse(start.audioAktiv)
        assertFalse(start.audioZustand.spieltGerade)
        assertFalse(start.kopfleisteEingeklappt)
        assertFalse(start.einstellungenOffen)
        assertFalse(start.grundsaetzeOffen)
        assertTrue(start.aufgeklappteGrundsaetze.isEmpty())

        // Modus, Schriftgröße, reduzierte Animationen, Audio, Kopfleiste & Direktwahl umschalten
        assertTrue(controller.waehleModus(SpielModus.LANG))
        assertEquals(SpielModus.LANG, controller.aktuellerZustand.gameState.modus)

        controller.setzeSchriftgroesse(Schriftgroesse.GROSS)
        assertEquals(Schriftgroesse.GROSS, controller.aktuellerZustand.schriftgroesse)

        controller.toggleReduzierteAnimationen()
        assertTrue(controller.aktuellerZustand.reduzierteAnimationen)
        controller.setzeReduzierteAnimationen(false)
        assertFalse(controller.aktuellerZustand.reduzierteAnimationen)
        controller.setzeReduzierteAnimationen(true)
        assertTrue(controller.aktuellerZustand.reduzierteAnimationen)

        controller.toggleAudioAktiv()
        assertTrue(controller.aktuellerZustand.audioAktiv)
        assertTrue(controller.aktuellerZustand.audioZustand.spieltGerade)
        controller.setzeAudioLautstaerke(0.9f)
        assertEquals(0.35f, controller.aktuellerZustand.audioLautstaerke)

        controller.toggleKopfleisteEingeklappt()
        assertTrue(controller.aktuellerZustand.kopfleisteEingeklappt)
        controller.setzeKopfleisteEingeklappt(false)
        assertFalse(controller.aktuellerZustand.kopfleisteEingeklappt)
        controller.toggleKopfleisteEingeklappt()
        assertTrue(controller.aktuellerZustand.kopfleisteEingeklappt)

        assertTrue(controller.setzeDirektwahlAktiv(true))
        assertTrue(controller.aktuellerZustand.gameState.direktwahlAktiv)

        // Einstellungs- und Grundsätze-Dialog im Startmenü öffnen und schließen
        controller.einstellungenOeffnen()
        assertTrue(controller.aktuellerZustand.einstellungenOffen)
        assertTrue(controller.einstellungenSchliessen())
        assertFalse(controller.aktuellerZustand.einstellungenOffen)

        assertTrue(controller.grundsaetzeOeffnen())
        assertTrue(controller.aktuellerZustand.grundsaetzeOffen)

        // Alle 3 Onboarding-Grundsätze lassen sich auf- und wieder zuklappen
        val grundsaetze = content.konfiguration.onboarding.grundsaetze
        assertEquals(3, grundsaetze.size)
        for (grundsatz in grundsaetze) {
            assertTrue(controller.toggleOnboardingGrundsatz(grundsatz.id))
            assertTrue(grundsatz.id in controller.aktuellerZustand.aufgeklappteGrundsaetze)
        }
        assertTrue(controller.toggleOnboardingGrundsatz(grundsaetze.first().id))
        assertFalse(grundsaetze.first().id in controller.aktuellerZustand.aufgeklappteGrundsaetze)
        assertFalse(controller.toggleOnboardingGrundsatz("unbekannter_grundsatz"))
        assertTrue(controller.grundsaetzeSchliessen())
        assertFalse(controller.aktuellerZustand.grundsaetzeOffen)

        // Nach Start in HerkunftWahl darf Grundsätze-Dialog nicht mehr geöffnet werden, Einstellungen schon
        assertTrue(controller.durchgangBeginnen())
        assertIs<GamePhase.HerkunftWahl>(controller.aktuellerZustand.gameState.phase)
        assertFalse(controller.grundsaetzeOeffnen())
        controller.einstellungenOeffnen()
        assertTrue(controller.aktuellerZustand.einstellungenOffen)
        assertTrue(controller.einstellungenSchliessen())
    }

    @Test
    fun leitplankenKeinZurueckUndPhasenSchutz() {
        val controller = SpielController(content, KotlinRandomSource(Random(42)))

        // Im Startmenü sind Spielschritte und Neuer Durchgang gesperrt
        assertFalse(controller.waehleOption(0))
        assertFalse(controller.weiterNachAusgang())
        assertFalse(controller.starteKapitel())
        assertFalse(controller.naechstesKapitelStarten())
        assertFalse(controller.bestaetigeMusterung())
        assertFalse(controller.waehleErwerb("ruestung"))
        assertFalse(controller.neuerDurchgang())

        // Start -> HerkunftWahl
        controller.setzeDirektwahlAktiv(true)
        assertTrue(controller.durchgangBeginnen())
        assertFalse(controller.durchgangBeginnen())

        // Unvollständige Auswahl darf nicht bestätigt werden
        assertFalse(controller.bestaetigePerson())
        assertTrue(controller.waehleHerkunftEntwurf("buergertum"))
        assertTrue(controller.waehleGeschlechtEntwurf(Geschlecht.MAENNLICH))
        assertTrue(controller.waehleAlterEntwurf(18))
        assertFalse(controller.bestaetigePerson(), "Bei aktiver Direktwahl muss auch der Pfad gewählt sein.")
        assertTrue(controller.waehleDirektPfadEntwurf(Pfad.FRONT))
        assertTrue(controller.bestaetigePerson())

        assertIs<GamePhase.KapitelStart>(controller.aktuellerZustand.gameState.phase)
        assertFalse(controller.neuerDurchgang(), "Kein Abbruch/Reset mitten im laufenden Durchgang.")

        // In EreignisAnzeige sind nur die exakt 2 Optionen (0 oder 1) zulässig
        assertTrue(controller.starteKapitel())
        val anzeige = assertIs<GamePhase.EreignisAnzeige>(controller.aktuellerZustand.gameState.phase)
        assertEquals(2, anzeige.ereignis.optionen.size)
        assertFalse(controller.waehleOption(-1))
        assertFalse(controller.waehleOption(2))

        // Wert-Erklärkarte öffnet und wird beim nächsten Spielschritt automatisch geschlossen
        controller.waehleWertErklaerung(WertSchluessel.VERSORGUNG)
        assertEquals(WertSchluessel.VERSORGUNG, controller.aktuellerZustand.ausgewaehlterWert)

        assertTrue(controller.waehleOption(0))
        assertNull(controller.aktuellerZustand.ausgewaehlterWert)
        assertIs<GamePhase.EreignisAusgang>(controller.aktuellerZustand.gameState.phase)
        // Doppelklick auf Option im Ausgang wird ignoriert (kein Zurück / kein Absturz)
        assertFalse(controller.waehleOption(1))
    }

    @Test
    fun kompletterUiDurchlaufAlleDreiPfadeImDirektwahlModus() {
        val szenarien = listOf(
            Triple(Pfad.FRONT, SpielModus.KURZ, "buergertum"),
            Triple(Pfad.ETAPPE, SpielModus.KURZ, "adel"),
            Triple(Pfad.HEIMAT, SpielModus.KURZ, "landbevoelkerung"),
            Triple(Pfad.FRONT, SpielModus.LANG, "arbeiterschaft"),
            Triple(Pfad.ETAPPE, SpielModus.LANG, "buergertum"),
            Triple(Pfad.HEIMAT, SpielModus.LANG, "adel"),
        )

        for ((index, szenario) in szenarien.withIndex()) {
            val (pfad, modus, herkunftId) = szenario
            val geschlecht = if (pfad == Pfad.FRONT) Geschlecht.MAENNLICH else Geschlecht.WEIBLICH
            val alter = if (index % 2 == 0) 18 else 35

            // Deterministischer Durchlauf mit kluger Wahlstrategie -> erreicht zuverlässig 1919
            var abgeschlossenerController: SpielController? = null
            for (seedOffset in 0..25) {
                val controller = SpielController(
                    content = content,
                    random = KotlinRandomSource(Random(2000 + index * 100 + seedOffset)),
                    initialSchriftgroesse = Schriftgroesse.GROSS,
                    initialReduzierteAnimationen = true,
                    initialAudioAktiv = true,
                    initialKopfleisteEingeklappt = true,
                )
                assertTrue(controller.waehleModus(modus))
                assertTrue(controller.setzeDirektwahlAktiv(true))
                assertTrue(controller.durchgangBeginnen())

                assertTrue(controller.waehleHerkunftEntwurf(herkunftId))
                assertTrue(controller.waehleGeschlechtEntwurf(geschlecht))
                assertTrue(controller.waehleAlterEntwurf(alter))
                assertTrue(controller.waehleDirektPfadEntwurf(pfad))
                assertTrue(controller.bestaetigePerson())

                val ergebnis = spieleBisAbschlussMitUiPruefung(controller, riskant = false)
                if (!ergebnis.lebenslauf.istVorzeitigerAbbruch) {
                    abgeschlossenerController = controller
                    break
                }
            }

            val fertig = assertNotNull(
                abgeschlossenerController,
                "Erwartete regulären 1919-Abschluss für $pfad / $modus.",
            )
            val abschluss = assertIs<GamePhase.Abgeschlossen>(fertig.aktuellerZustand.gameState.phase)
            assertNull(abschluss.hartesEnde)
            assertFalse(fertig.aktuellerZustand.istImAuffangnetz)
            assertEquals(pfad, fertig.aktuellerZustand.gameState.pfad)
            assertEquals(1919, fertig.aktuellerZustand.gameState.jahr)
            assertNotNull(abschluss.lebenslauf.ausgang)
            assertEquals(4, abschluss.lebenslauf.faecher.size)
            assertTrue(abschluss.lebenslauf.zeitleiste.isNotEmpty())
            assertEquals(
                abschluss.lebenslauf.zeitleiste.map { it.jahr }.sorted(),
                abschluss.lebenslauf.zeitleiste.map { it.jahr },
            )
            assertTrue(
                fertig.aktuellerZustand.gameState.gespielteEreignisse.contains(GameEngine.EREIGNIS_FINALE_WIRTSHAUS),
                "Epilog-Finale wirtshaus_wahl muss vor Abschluss 1919 gespielt worden sein.",
            )

            // Auf Front & Etappe greift auch am Ende die harte Musiksperre
            if (pfad == Pfad.FRONT || pfad == Pfad.ETAPPE) {
                assertTrue(fertig.aktuellerZustand.audioZustand.musikGesperrt)
                assertFalse(fertig.aktuellerZustand.audioZustand.spieltGerade)
            } else {
                assertFalse(fertig.aktuellerZustand.audioZustand.musikGesperrt)
                assertTrue(fertig.aktuellerZustand.audioZustand.spieltGerade)
            }

            val protokollUi = UiStateMapper.mapProtokollEintraege(content, fertig.aktuellerZustand.gameState.protokoll)
            assertTrue(protokollUi.size >= 8, "Protokoll muss alle getroffenen Stationen enthalten.")
            assertTrue(protokollUi.all { it.station.isNotBlank() && it.wahl.isNotBlank() })

            // Neuer Durchgang nach Abschluss bewahrt globale Unterrichts- & Zugänglichkeits-Einstellungen
            assertTrue(fertig.neuerDurchgang())
            assertIs<GamePhase.Start>(fertig.aktuellerZustand.gameState.phase)
            assertEquals(Schriftgroesse.GROSS, fertig.aktuellerZustand.schriftgroesse)
            assertTrue(fertig.aktuellerZustand.kopfleisteEingeklappt)
            assertTrue(fertig.aktuellerZustand.reduzierteAnimationen)
            assertTrue(fertig.aktuellerZustand.audioAktiv)
            assertEquals(modus, fertig.aktuellerZustand.gameState.modus)
            assertTrue(fertig.aktuellerZustand.gameState.direktwahlAktiv)
        }
    }

    @Test
    fun regulaererDurchlaufMitMusterungUndOffiziersEinstiegBis1919() {
        // Scripted RNG: erzwingt k. v. ohne u. k. -> Front -> Offizierslaufbahn (Adel, 35 Jahre)
        val scriptedRng = object : RandomSource {
            private val queue = ArrayDeque(listOf(0, 0, 0, 176, 88, 1, 99, 0))
            override fun nextInt(fromInclusive: Int, untilExclusive: Int): Int {
                val raw = if (queue.isNotEmpty()) queue.removeFirst() else fromInclusive
                return raw.coerceIn(fromInclusive, untilExclusive - 1)
            }
        }

        val controller = SpielController(content, scriptedRng)
        assertTrue(controller.waehleModus(SpielModus.KURZ))
        assertTrue(controller.durchgangBeginnen())
        assertTrue(controller.waehlePerson("adel", Geschlecht.MAENNLICH, 35))

        // Einstiegs-Ereignis: Meldung
        val meldung = assertIs<GamePhase.EreignisAnzeige>(controller.aktuellerZustand.gameState.phase)
        assertEquals(GameEngine.EREIGNIS_EINSTIEG_MELDUNG, meldung.ereignis.id)
        assertTrue(controller.waehleOption(0))

        val meldungAusgang = assertIs<GamePhase.EreignisAusgang>(controller.aktuellerZustand.gameState.phase)
        assertEquals(
            "Zum Musterungsbescheid",
            UiStateMapper.mapWeiterLabel(controller.engine, controller.aktuellerZustand.gameState, meldungAusgang),
        )
        assertTrue(controller.weiterNachAusgang())

        // Musterungsergebnis-Blatt prüfen
        val musterungPhase = assertIs<GamePhase.MusterungErgebnis>(controller.aktuellerZustand.gameState.phase)
        assertEquals(MusterungsGrad.KV, musterungPhase.daten.grad)
        assertEquals(Pfad.FRONT, musterungPhase.zielPfad)

        val musterungUi = UiStateMapper.mapMusterungErgebnis(
            content = content,
            phase = musterungPhase,
            person = controller.aktuellerZustand.gameState.person,
        )
        assertEquals("k. v.", musterungUi.gradKurz)
        assertEquals("kriegsverwendungsfähig", musterungUi.gradLang)
        assertTrue(musterungUi.befund.isNotBlank())
        assertTrue(musterungUi.heeresklasse.isNotBlank())
        assertEquals("An der Front", musterungUi.zielPfadMarke)
        assertEquals(176, musterungUi.groesseCm)
        assertEquals(88, musterungUi.brustumfangCm)

        // Bestätigen -> Offiziers-Einstieg
        assertTrue(controller.bestaetigeMusterung())
        val offizier = assertIs<GamePhase.EreignisAnzeige>(controller.aktuellerZustand.gameState.phase)
        assertEquals(GameEngine.EREIGNIS_EINSTIEG_OFFIZIER, offizier.ereignis.id)
        assertTrue(controller.waehleOption(0))
        assertTrue(controller.weiterNachAusgang())

        // Jetzt in KapitelStart 1914 und weiter bis Abschluss
        val start1914 = assertIs<GamePhase.KapitelStart>(controller.aktuellerZustand.gameState.phase)
        assertEquals(1914, start1914.kapitel.jahr)
        assertEquals("Offiziersaspirant", controller.aktuellerZustand.gameState.person?.stand)

        val abschluss = spieleBisAbschlussMitUiPruefung(controller, riskant = false)
        assertEquals(4, abschluss.lebenslauf.faecher.size)
        assertTrue(controller.neuerDurchgang())
    }

    @Test
    fun musterungMitUkVermerkFuehrtInErwerbWahlUndZeigtVermerkImBescheid() {
        // Scripted RNG: wählt kv (wurf=1) UND u. k. (wurf=1 <= ukWahrscheinlichkeit 18) -> Zielpfad HEIMAT
        val scriptedRng = object : RandomSource {
            private val queue = ArrayDeque(listOf(0, 0, 0, 172, 84, 1, 1, 0))
            override fun nextInt(fromInclusive: Int, untilExclusive: Int): Int {
                val raw = if (queue.isNotEmpty()) queue.removeFirst() else fromInclusive
                return raw.coerceIn(fromInclusive, untilExclusive - 1)
            }
        }

        val controller = SpielController(content, scriptedRng)
        assertTrue(controller.durchgangBeginnen())
        assertTrue(controller.waehlePerson("arbeiterschaft", Geschlecht.MAENNLICH, 35))
        assertTrue(controller.waehleOption(1)) // Einberufungsbefehl abwarten
        assertTrue(controller.weiterNachAusgang())

        val musterung = assertIs<GamePhase.MusterungErgebnis>(controller.aktuellerZustand.gameState.phase)
        assertEquals(Pfad.HEIMAT, musterung.zielPfad)

        val musterungUi = UiStateMapper.mapMusterungErgebnis(
            content = content,
            phase = musterung,
            person = controller.aktuellerZustand.gameState.person,
        )
        assertEquals("u. k.", musterungUi.vermerkKurz)
        assertNotNull(musterungUi.vermerkLang)
        assertNotNull(musterungUi.vermerkErklaerung)
        assertEquals("In der Heimat", musterungUi.zielPfadMarke)

        // Bestätigen führt direkt in die Erwerbswahl (ohne haushalt/wohlfahrt wegen uk & männlich)
        assertTrue(controller.bestaetigeMusterung())
        val erwerbPhase = assertIs<GamePhase.ErwerbWahl>(controller.aktuellerZustand.gameState.phase)
        assertTrue(erwerbPhase.optionen.isNotEmpty())
        assertTrue(controller.waehleErwerb(erwerbPhase.optionen.first().id))
        assertIs<GamePhase.EreignisAnzeige>(controller.aktuellerZustand.gameState.phase)
    }

    @Test
    fun erwerbswahlMitHistorischenEinordnungsStempelnUndEtappenWechsel() {
        // 1. Weibliche Figur (Arbeiterschaft, 18 Jahre) -> 1914-selten-Stempel für Rüstung & Verwaltung
        val controllerW = SpielController(content, KotlinRandomSource(Random(31)))
        assertTrue(controllerW.durchgangBeginnen())
        assertTrue(controllerW.waehlePerson("arbeiterschaft", Geschlecht.WEIBLICH, 18))

        val erwerbPhaseW = assertIs<GamePhase.ErwerbWahl>(controllerW.aktuellerZustand.gameState.phase)
        val optionenUiW = UiStateMapper.mapErwerbOptionen(
            engine = controllerW.engine,
            state = controllerW.aktuellerZustand.gameState,
            optionen = erwerbPhaseW.optionen,
        )
        val ruestungW = assertNotNull(optionenUiW.firstOrNull { it.id == "ruestung" })
        assertEquals("1914 selten", ruestungW.hinweisStempel)
        assertNotNull(ruestungW.hinweisText)
        assertEquals("Granatendreherin", ruestungW.berufsBezeichnung)

        val verwaltungW = assertNotNull(optionenUiW.firstOrNull { it.id == "verwaltung" })
        assertEquals("1914 selten", verwaltungW.hinweisStempel)

        // 2-Schritt-Auswahl (markieren + bestätigen) auf Lazarett -> Einstieg Etappe -> Etappe 1914
        assertFalse(controllerW.bestaetigeAusgewaehltenErwerb())
        assertTrue(controllerW.markiereErwerb("lazarett"))
        assertEquals("lazarett", controllerW.aktuellerZustand.ausgewaehlterErwerbId)
        assertTrue(controllerW.bestaetigeAusgewaehltenErwerb())

        val etappeFrage = assertIs<GamePhase.EreignisAnzeige>(controllerW.aktuellerZustand.gameState.phase)
        assertEquals(GameEngine.EREIGNIS_EINSTIEG_ETAPPE, etappeFrage.ereignis.id)
        assertTrue(controllerW.waehleOption(0))
        assertTrue(controllerW.weiterNachAusgang())

        val kapitel1914 = assertIs<GamePhase.KapitelStart>(controllerW.aktuellerZustand.gameState.phase)
        assertEquals(1914, kapitel1914.kapitel.jahr)
        assertEquals(Pfad.ETAPPE, controllerW.aktuellerZustand.gameState.pfad)

        // 2. Männliche Adelsfigur im Direktwahl-Heimat-Pfad -> „unüblich“-Stempel für Rüstung
        val controllerAdel = SpielController(content, KotlinRandomSource(Random(32)))
        assertTrue(controllerAdel.setzeDirektwahlAktiv(true))
        assertTrue(controllerAdel.durchgangBeginnen())
        assertTrue(controllerAdel.waehlePerson("adel", Geschlecht.MAENNLICH, 35, direktwahlPfad = Pfad.HEIMAT))

        val erwerbPhaseAdel = assertIs<GamePhase.ErwerbWahl>(controllerAdel.aktuellerZustand.gameState.phase)
        val optionenUiAdel = UiStateMapper.mapErwerbOptionen(
            engine = controllerAdel.engine,
            state = controllerAdel.aktuellerZustand.gameState,
            optionen = erwerbPhaseAdel.optionen,
        )
        val ruestungAdel = assertNotNull(optionenUiAdel.firstOrNull { it.id == "ruestung" })
        assertEquals("unüblich", ruestungAdel.hinweisStempel)
        assertNotNull(ruestungAdel.hinweisText)
    }

    @Test
    fun hartesEndeMitRespektvollemAuffangnetzUndErreichtemLebenslauf() {
        // Suche deterministisch einen Durchgang im langen Verlauf (riskante Wahlstrategie), der
        // in ein echtes hartes Ende läuft — komplett über SpielController gesteuert.
        var abbruchController: SpielController? = null
        for (seed in 1..200) {
            val pfad = when (seed % 3) {
                0 -> Pfad.FRONT
                1 -> Pfad.HEIMAT
                else -> Pfad.ETAPPE
            }
            val controller = SpielController(content, KotlinRandomSource(Random(5000 + seed)))
            controller.waehleModus(SpielModus.LANG)
            controller.setzeDirektwahlAktiv(true)
            controller.durchgangBeginnen()
            controller.waehlePerson(
                herkunftId = "arbeiterschaft",
                geschlecht = if (pfad == Pfad.FRONT) Geschlecht.MAENNLICH else Geschlecht.WEIBLICH,
                alter = 35,
                direktwahlPfad = pfad,
            )

            val abschluss = spieleBisAbschlussMitUiPruefung(controller, riskant = true)
            if (abschluss.hartesEnde != null) {
                abbruchController = controller
                break
            }
        }

        val controller = assertNotNull(
            abbruchController,
            "Riskante Wahlstrategie im langen Verlauf muss zuverlässig mindestens ein hartes Ende auslösen.",
        )

        // 1. Direkt nach Abbruch: respektvolles Auffangnetz aktiv
        assertTrue(controller.aktuellerZustand.istImAuffangnetz)
        assertFalse(controller.aktuellerZustand.auffangnetzBestaetigt)
        val abschluss = assertIs<GamePhase.Abgeschlossen>(controller.aktuellerZustand.gameState.phase)
        val hartesEnde = assertNotNull(abschluss.hartesEnde)
        assertTrue(abschluss.lebenslauf.istVorzeitigerAbbruch)
        assertNull(abschluss.lebenslauf.ausgang)
        assertTrue(hartesEnde.titel.isNotBlank())
        assertTrue(hartesEnde.text.isNotBlank())
        assertTrue(abschluss.lebenslauf.fazit.contains("kein persönliches Versagen"))
        assertEquals(4, abschluss.lebenslauf.faecher.size)
        assertEquals(hartesEnde.titel, abschluss.lebenslauf.faecher[3].merkmalName)

        // 2. Übergang in den erreichten 4-Fächer-Lebenslauf
        assertTrue(controller.auffangnetzBestaetigen())
        assertFalse(controller.aktuellerZustand.istImAuffangnetz)
        assertTrue(controller.aktuellerZustand.auffangnetzBestaetigt)
        assertFalse(controller.auffangnetzBestaetigen())

        // 3. Sauberer Neustart möglich
        assertTrue(controller.neuerDurchgang())
        assertIs<GamePhase.Start>(controller.aktuellerZustand.gameState.phase)
        assertFalse(controller.aktuellerZustand.auffangnetzBestaetigt)
    }

    @Test
    fun alleSechsKapitelUndKapitelAbschluesseWerdenVollstaendigAufUiAbgebildet() {
        val engine = GameEngine(content, KotlinRandomSource(Random(1918)))
        for (kapitel in content.kapitel.kapitel) {
            for (pfad in Pfad.entries) {
                val wirkung = engine.kapitelWirkung(kapitel.jahr, pfad)
                val startUi = UiStateMapper.mapKapitelStart(
                    engine = engine,
                    phase = GamePhase.KapitelStart(kapitel = kapitel, kapitelWirkung = wirkung),
                    pfad = pfad,
                )
                assertEquals(kapitel.jahr, startUi.jahr)
                assertEquals(kapitel.bildId, startUi.kapitelbild.bildId)
                assertTrue(startUi.kapitelbild.istImMedienplan, "Kapitelbild ${kapitel.bildId} fehlt im Medienplan.")
                assertEquals("kapitel/${kapitel.bildId}.webp", startUi.kapitelbild.ressourcenPfad)
                assertTrue(startUi.stichworte.isNotEmpty())
                assertNotNull(startUi.leitfrage)
                assertTrue(startUi.aktionLabel.isNotBlank())

                if (!kapitel.istEpilog) {
                    val bogen = kapitel.bogen.getValue(pfad)
                    val abschlussUi = UiStateMapper.mapKapitelAbschluss(
                        content = content,
                        phase = GamePhase.KapitelAbschluss(kapitel = kapitel, bogen = bogen),
                        pfad = pfad,
                        zustandssatz = "Es reicht.",
                    )
                    assertEquals(bogen.frage, abschlussUi.leitfrage)
                    assertEquals(bogen.kippt, abschlussUi.kipppunkt)
                    assertNotNull(abschlussUi.rueckblick)
                    assertNotNull(abschlussUi.naechstesKapitelJahr)
                    assertTrue(abschlussUi.weiterLabel.contains(abschlussUi.naechstesKapitelJahr.toString()))
                }
            }
        }
    }

    @Test
    fun zurueckTasteSchliesstDialogeUndErklaerKartenUndWahrtKeinZurueckLeitplanke() {
        val controller = SpielController(
            content = content,
            random = KotlinRandomSource(Random(701)),
            initialSchriftgroesse = Schriftgroesse.GROSS,
            initialReduzierteAnimationen = true,
            initialAudioAktiv = true,
            initialKopfleisteEingeklappt = true,
        )

        // 1. Im Startmenü ohne Überlagerungen greift System-Zurück
        assertFalse(controller.aktuellerZustand.sollZurueckAbfangen)
        assertEquals(ZurueckErgebnis.SYSTEM_STANDARD, controller.verarbeiteZurueckTaste())

        // 2. Geöffnete Einstellungen und Grundsätze schließen sich über Zurück sauber
        controller.einstellungenOeffnen()
        assertTrue(controller.aktuellerZustand.sollZurueckAbfangen)
        assertEquals(ZurueckErgebnis.DIALOG_GESCHLOSSEN, controller.verarbeiteZurueckTaste())
        assertFalse(controller.aktuellerZustand.einstellungenOffen)

        assertTrue(controller.grundsaetzeOeffnen())
        assertTrue(controller.aktuellerZustand.sollZurueckAbfangen)
        assertEquals(ZurueckErgebnis.DIALOG_GESCHLOSSEN, controller.verarbeiteZurueckTaste())
        assertFalse(controller.aktuellerZustand.grundsaetzeOffen)

        // 3. Laufenden Durchgang starten bis in ein Ereignis
        assertTrue(controller.waehleModus(SpielModus.LANG))
        assertTrue(controller.setzeDirektwahlAktiv(true))
        assertTrue(controller.durchgangBeginnen())
        assertTrue(controller.waehlePerson("buergertum", Geschlecht.MAENNLICH, 18, direktwahlPfad = Pfad.FRONT))
        assertTrue(controller.starteKapitel())
        val ereignisPhase = assertIs<GamePhase.EreignisAnzeige>(controller.aktuellerZustand.gameState.phase)
        assertTrue(controller.aktuellerZustand.istImLaufendenDurchgang)
        assertTrue(controller.aktuellerZustand.sollZurueckAbfangen)

        // 4. Geöffnete Wert-Erklärkarte schließt sich auf Zurück sauber (ohne Dialog)
        controller.waehleWertErklaerung(WertSchluessel.VERSORGUNG)
        assertTrue(controller.aktuellerZustand.hatOffeneErklaerKarte)
        assertFalse(controller.aktuellerZustand.emotionDetailsOffen)
        assertEquals(ZurueckErgebnis.ERKLAERKARTE_GESCHLOSSEN, controller.verarbeiteZurueckTaste())
        assertNull(controller.aktuellerZustand.ausgewaehlterWert)
        assertFalse(controller.aktuellerZustand.verlassenDialogOffen)
        assertEquals(ereignisPhase, controller.aktuellerZustand.gameState.phase)

        // 5. Geöffnete Figuren-Detailkarte schließt sich auf Zurück ebenfalls sauber
        controller.setzeEmotionDetailsOffen(true)
        assertTrue(controller.aktuellerZustand.emotionDetailsOffen)
        assertNull(controller.aktuellerZustand.ausgewaehlterWert)
        assertEquals(ZurueckErgebnis.ERKLAERKARTE_GESCHLOSSEN, controller.verarbeiteZurueckTaste())
        assertFalse(controller.aktuellerZustand.emotionDetailsOffen)
        assertFalse(controller.aktuellerZustand.verlassenDialogOffen)

        // 6. Geöffnete Einstellungen im laufenden Durchgang schließen sich vor der Sicherheitsabfrage
        controller.einstellungenOeffnen()
        assertEquals(ZurueckErgebnis.DIALOG_GESCHLOSSEN, controller.verarbeiteZurueckTaste())
        assertFalse(controller.aktuellerZustand.einstellungenOffen)
        assertFalse(controller.aktuellerZustand.verlassenDialogOffen)

        // 7. Ohne offene Überlagerung öffnet Zurück die ruhige Sicherheitsabfrage (kein Zurück zur letzten Karte!)
        assertFalse(controller.durchgangNachBestaetigungVerlassen(), "Verlassen darf ohne offene Abfrage nicht greifen.")
        assertEquals(ZurueckErgebnis.SICHERHEITSABFRAGE_GEOEFFNET, controller.verarbeiteZurueckTaste())
        assertTrue(controller.aktuellerZustand.verlassenDialogOffen)
        assertEquals(ereignisPhase, controller.aktuellerZustand.gameState.phase)

        // Erneutes Zurück schließt den Dialog sicher und bleibt im Durchgang
        assertEquals(ZurueckErgebnis.DIALOG_GESCHLOSSEN, controller.verarbeiteZurueckTaste())
        assertFalse(controller.aktuellerZustand.verlassenDialogOffen)
        assertEquals(ereignisPhase, controller.aktuellerZustand.gameState.phase)

        // 8. Ausdrücklich bestätigtes Verlassen kehrt sauber ins Startmenü zurück & bewahrt Einstellungen
        assertEquals(ZurueckErgebnis.SICHERHEITSABFRAGE_GEOEFFNET, controller.verarbeiteZurueckTaste())
        assertTrue(controller.durchgangNachBestaetigungVerlassen())
        assertIs<GamePhase.Start>(controller.aktuellerZustand.gameState.phase)
        assertFalse(controller.aktuellerZustand.verlassenDialogOffen)
        assertEquals(Schriftgroesse.GROSS, controller.aktuellerZustand.schriftgroesse)
        assertTrue(controller.aktuellerZustand.kopfleisteEingeklappt)
        assertTrue(controller.aktuellerZustand.reduzierteAnimationen)
        assertTrue(controller.aktuellerZustand.audioAktiv)
        assertEquals(SpielModus.LANG, controller.aktuellerZustand.gameState.modus)
        assertTrue(controller.aktuellerZustand.gameState.direktwahlAktiv)
    }

    @Test
    fun zurueckTasteSchuetztAuchAbgeschlossenenLebenslaufVorVersehentlichemVerlassen() {
        val controller = SpielController(content, KotlinRandomSource(Random(702)))
        assertTrue(controller.setzeDirektwahlAktiv(true))
        assertTrue(controller.durchgangBeginnen())
        assertTrue(controller.waehlePerson("landbevoelkerung", Geschlecht.WEIBLICH, 18, direktwahlPfad = Pfad.HEIMAT))
        spieleBisAbschlussMitUiPruefung(controller, riskant = false)

        val abschluss = assertIs<GamePhase.Abgeschlossen>(controller.aktuellerZustand.gameState.phase)
        assertFalse(controller.aktuellerZustand.istImLaufendenDurchgang)
        assertTrue(controller.aktuellerZustand.sollZurueckAbfangen)

        // Erstes Zurück öffnet die ruhige Abfrage, damit der fertige Lebenslauf vor Druck/Export geschützt bleibt
        assertEquals(ZurueckErgebnis.SICHERHEITSABFRAGE_GEOEFFNET, controller.verarbeiteZurueckTaste())
        assertTrue(controller.aktuellerZustand.verlassenDialogOffen)
        assertEquals(abschluss, controller.aktuellerZustand.gameState.phase)

        // Bleiben schließt Dialog ohne Datenverlust
        assertTrue(controller.verlassenDialogSchliessen())
        assertFalse(controller.aktuellerZustand.verlassenDialogOffen)
        assertEquals(abschluss, controller.aktuellerZustand.gameState.phase)
    }

    // -------------------------------------------------------------------------
    // Hilfsfunktionen für durchgängige Controller- & UI-Mapping-Tests
    // -------------------------------------------------------------------------

    private fun spieleBisAbschlussMitUiPruefung(
        controller: SpielController,
        riskant: Boolean,
    ): GamePhase.Abgeschlossen {
        var sicherheitsSchritte = 0
        while (sicherheitsSchritte < 160) {
            sicherheitsSchritte++
            val uiState = controller.aktuellerZustand
            val gameState = uiState.gameState

            // Kopfleiste & Live-Emotion dürfen in jeder Spielphase nach Personenerzeugung niemals brechen
            if (gameState.person != null) {
                val leiste = UiStateMapper.mapBefindensLeiste(controller.engine, gameState)
                assertEquals(4, leiste.size)
                val emotion = UiStateMapper.mapLiveEmotion(controller.engine, gameState)
                assertTrue(emotion.istImMedienplan, "Unbekanntes Portrait: ${emotion.portraitId}")
                UiStateMapper.mapKopfKapitelTitel(content, gameState)
            }

            when (val phase = gameState.phase) {
                is GamePhase.ErwerbWahl -> {
                    val optionenUi = UiStateMapper.mapErwerbOptionen(controller.engine, gameState, phase.optionen)
                    assertTrue(optionenUi.isNotEmpty())
                    val zielId = if (riskant && optionenUi.any { it.id == "ruestung" }) {
                        "ruestung"
                    } else {
                        optionenUi.first().id
                    }
                    assertTrue(controller.markiereErwerb(zielId))
                    assertTrue(controller.bestaetigeAusgewaehltenErwerb())
                }

                is GamePhase.MusterungErgebnis -> {
                    val mUi = UiStateMapper.mapMusterungErgebnis(content, phase, gameState.person)
                    assertTrue(mUi.gradKurz.isNotBlank())
                    assertTrue(controller.bestaetigeMusterung())
                }

                is GamePhase.KapitelStart -> {
                    val kUi = UiStateMapper.mapKapitelStart(controller.engine, phase, gameState.pfad)
                    assertTrue(kUi.kapitelbild.istImMedienplan)
                    assertTrue(controller.starteKapitel())
                }

                is GamePhase.EreignisAnzeige -> {
                    val karteUi = UiStateMapper.mapEntscheidungsKarte(
                        content = content,
                        ereignis = phase.ereignis,
                        aufgeloesterText = phase.aufgeloesterText,
                        jahr = gameState.jahr,
                        pfad = gameState.pfad,
                    )
                    assertEquals(2, karteUi.optionen.size)
                    val optionIndex = waehleStrategischeOption(controller.engine, gameState, phase.ereignis, riskant)
                    assertTrue(controller.waehleOption(optionIndex))
                }

                is GamePhase.EreignisAusgang -> {
                    val ausgangUi = UiStateMapper.mapEreignisAusgang(controller.engine, phase)
                    assertTrue(ausgangUi.ausgangsText.isNotBlank())
                    val weiterLabel = UiStateMapper.mapWeiterLabel(controller.engine, gameState, phase)
                    assertTrue(weiterLabel.isNotBlank())
                    assertTrue(controller.weiterNachAusgang())
                }

                is GamePhase.KapitelAbschluss -> {
                    val abschlussUi = UiStateMapper.mapKapitelAbschluss(
                        content = content,
                        phase = phase,
                        pfad = gameState.pfad,
                        zustandssatz = controller.engine.zustandssatz(gameState),
                    )
                    assertTrue(abschlussUi.leitfrage.isNotBlank())
                    assertTrue(abschlussUi.kipppunkt.isNotBlank())
                    assertTrue(controller.naechstesKapitelStarten())
                }

                is GamePhase.Abgeschlossen -> return phase

                is GamePhase.Start,
                is GamePhase.HerkunftWahl,
                -> error("Unerwartete Phase in laufendem Durchgang: $phase")
            }
        }
        error("Durchgang hat das Sicherheitslimit von 160 Schritten überschritten.")
    }

    private fun waehleStrategischeOption(
        engine: GameEngine,
        state: de.pytales.zdf.engine.GameState,
        ereignis: Ereignis,
        riskant: Boolean,
    ): Int {
        fun bewerte(optionIndex: Int): Int {
            val option = ereignis.optionen[optionIndex]
            val (nachher, _) = engine.metrics.werteAnwenden(state.werte, option.wirkung)
            val versorgung = nachher[WertSchluessel.VERSORGUNG] ?: 0
            val belastung = nachher[WertSchluessel.BELASTUNG] ?: 0
            val aufmerksamkeit = nachher[WertSchluessel.AUFMERKSAMKEIT] ?: 0
            val rueckhalt = nachher[WertSchluessel.RUECKHALT] ?: 0
            val toedlichesRisiko = if (option.zufallsAusgaenge.any { it.sprungEnde != null }) -50 else 0
            // Hoher Score = sicherer / gesünder; niedriger Score = riskanter / belastender
            return versorgung * 4 - belastung * 4 - aufmerksamkeit * 3 + rueckhalt + toedlichesRisiko
        }
        val score0 = bewerte(0)
        val score1 = bewerte(1)
        return if (riskant) {
            if (score0 <= score1) 0 else 1
        } else {
            if (score0 >= score1) 0 else 1
        }
    }
}
