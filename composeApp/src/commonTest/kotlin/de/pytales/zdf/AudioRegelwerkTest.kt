package de.pytales.zdf

import de.pytales.zdf.audio.AudioAusgabe
import de.pytales.zdf.audio.AudioKoordinator
import de.pytales.zdf.audio.AudioRegelwerk
import de.pytales.zdf.audio.AudioSperrGrund
import de.pytales.zdf.audio.AudioSpur
import de.pytales.zdf.audio.RuhigeArchivSynthese
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.engine.HartesEndeErgebnis
import de.pytales.zdf.engine.KotlinRandomSource
import de.pytales.zdf.engine.MusterungErgebnisDaten
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.HartesEndeId
import de.pytales.zdf.model.MusterungsGrad
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.SpielModus
import de.pytales.zdf.ui.state.SpielController
import kotlin.random.Random
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNull
import kotlin.test.assertTrue

/**
 * Prüfsuite für AP 6 — Optionales dezentes Audio und harte Musiksperre auf `front` & `etappe`.
 */
class AudioRegelwerkTest {

    private val content = loadTestGameContent()
    private val engine = GameEngine(content, KotlinRandomSource(Random(1914)))

    private class FakeAudioAusgabe : AudioAusgabe {
        val abgespielteSpuren = mutableListOf<Pair<AudioSpur, Float>>()
        var stoppAufrufe: Int = 0
        var freigabeAufrufe: Int = 0

        override fun aktualisiere(spur: AudioSpur, lautstaerke: Float) {
            abgespielteSpuren += spur to lautstaerke
        }

        override fun stoppe() {
            stoppAufrufe++
        }

        override fun freigeben() {
            freigabeAufrufe++
        }
    }

    @Test
    fun standardStummUndDezenteLautstaerkeBegrenzung() {
        val startState = engine.neuesSpiel()
        val stumm = AudioRegelwerk.bestimmeZustand(startState, audioAktiv = false)
        assertFalse(stumm.spieltGerade)
        assertFalse(stumm.musikGesperrt)
        assertEquals(AudioSpur.STILLE, stumm.aktiveSpur)
        assertEquals(AudioSperrGrund.STUMMGESCHALTET, stumm.sperrGrund)

        // Aktiv im Startmenü -> ruhige Archiv-Begleitung mit begrenzter Lautstärke
        val aktiv = AudioRegelwerk.bestimmeZustand(startState, audioAktiv = true, lautstaerke = 1.0f)
        assertTrue(aktiv.spieltGerade)
        assertFalse(aktiv.musikGesperrt)
        assertEquals(AudioSpur.START_RUHIG, aktiv.aktiveSpur)
        assertNull(aktiv.sperrGrund)
        assertEquals(AudioRegelwerk.MAX_DEZENTE_LAUTSTAERKE, aktiv.lautstaerke)

        // Grenzwerte für Lautstärke
        assertEquals(0f, AudioRegelwerk.begrenzeLautstaerke(-0.5f))
        assertEquals(0f, AudioRegelwerk.begrenzeLautstaerke(Float.NaN))
        assertEquals(0.2f, AudioRegelwerk.begrenzeLautstaerke(0.2f))
        assertEquals(AudioRegelwerk.MAX_DEZENTE_LAUTSTAERKE, AudioRegelwerk.begrenzeLautstaerke(0.9f))
    }

    @Test
    fun harteMusiksperreAufFrontUndEtappeInAllenSpielphasen() {
        assertTrue(AudioRegelwerk.istMusikGesperrtFuerPfad(Pfad.FRONT))
        assertTrue(AudioRegelwerk.istMusikGesperrtFuerPfad(Pfad.ETAPPE))
        assertFalse(AudioRegelwerk.istMusikGesperrtFuerPfad(Pfad.HEIMAT))

        val kapitel1915 = content.kapitelByJahr.getValue(1915)
        val ereignisFront = content.ereignisById.getValue("front_1914_marsch")
        val musterungDaten = MusterungErgebnisDaten(
            grad = MusterungsGrad.KV,
            vermerk = null,
            befund = "Ohne Befund",
            heeresklasse = "Ersatzreserve",
            strenge = "einberufung",
        )

        for (pfad in listOf(Pfad.FRONT, Pfad.ETAPPE)) {
            val erwarteterGrund = if (pfad == Pfad.FRONT) {
                AudioSperrGrund.PFAD_FRONT
            } else {
                AudioSperrGrund.PFAD_ETAPPE
            }

            var basis = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.KURZ, direktwahlAktiv = true))
            basis = engine.waehlePerson(basis, "buergertum", Geschlecht.MAENNLICH, 18, direktwahlPfad = pfad)
            val lebenslaufRegulaer = engine.lebenslaufCalculator.berechneLebenslauf(basis.copy(jahr = 1919))

            val phasen = listOf(
                GamePhase.MusterungErgebnis(daten = musterungDaten, zielPfad = pfad),
                GamePhase.KapitelStart(kapitel = kapitel1915),
                GamePhase.EreignisAnzeige(ereignis = ereignisFront, aufgeloesterText = ereignisFront.text.standard),
                GamePhase.EreignisAusgang(
                    ereignis = ereignisFront,
                    gewaehlteOptionIndex = 0,
                    option = ereignisFront.optionen[0],
                    ausgangsText = ereignisFront.optionen[0].ausgang.standard,
                    wertaenderungen = emptyMap(),
                    neueMerkmale = emptyList(),
                ),
                GamePhase.KapitelAbschluss(kapitel = kapitel1915, bogen = kapitel1915.bogen.getValue(pfad)),
                GamePhase.Abgeschlossen(hartesEnde = null, lebenslauf = lebenslaufRegulaer),
            )

            for (phase in phasen) {
                val state = basis.copy(pfad = pfad, phase = phase)
                val zustand = AudioRegelwerk.bestimmeZustand(state, audioAktiv = true, lautstaerke = 1.0f)
                assertEquals(AudioSpur.STILLE, zustand.aktiveSpur, "Unerlaubte Musik auf $pfad in Phase $phase")
                assertTrue(zustand.musikGesperrt, "Musiksperre muss auf $pfad in Phase $phase greifen")
                assertFalse(zustand.spieltGerade, "spieltGerade muss auf $pfad in Phase $phase false sein")
                assertEquals(erwarteterGrund, zustand.sperrGrund)
            }
        }
    }

    @Test
    fun heimatSpieltDezentUndAuffangnetzErzwingtRespektvolleStille() {
        var heimat = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.KURZ, direktwahlAktiv = true))
        heimat = engine.waehlePerson(heimat, "arbeiterschaft", Geschlecht.WEIBLICH, 18, direktwahlPfad = Pfad.HEIMAT)

        // In Heimat (ErwerbWahl / 1914–1918) darf dezente Heimat-Begleitung laufen
        val zustandErwerb = AudioRegelwerk.bestimmeZustand(heimat, audioAktiv = true)
        assertTrue(zustandErwerb.spieltGerade)
        assertFalse(zustandErwerb.musikGesperrt)
        assertEquals(AudioSpur.HEIMAT_RUHIG, zustandErwerb.aktiveSpur)

        // Im regulären Heimat-Epilog 1919 -> ruhiger Ausklang
        val epilogState = heimat.copy(
            jahr = 1919,
            phase = GamePhase.Abgeschlossen(
                hartesEnde = null,
                lebenslauf = engine.lebenslaufCalculator.berechneLebenslauf(heimat.copy(jahr = 1919)),
            ),
        )
        val zustandEpilog = AudioRegelwerk.bestimmeZustand(epilogState, audioAktiv = true)
        assertTrue(zustandEpilog.spieltGerade)
        assertFalse(zustandEpilog.musikGesperrt)
        assertEquals(AudioSpur.EPILOG_RUHIG, zustandEpilog.aktiveSpur)

        // Im Auffangnetz (vorzeitiger Abbruch) auch in der Heimat strikte Stille
        val hartesEnde = HartesEndeErgebnis(
            id = HartesEndeId.ENDE_VERHUNGERT,
            titel = "Verhungert",
            text = "Ein ruhiger Einschnitt.",
            jahr = 1917,
        )
        val abbruchState = heimat.copy(
            jahr = 1917,
            phase = GamePhase.Abgeschlossen(
                hartesEnde = hartesEnde,
                lebenslauf = engine.lebenslaufCalculator.berechneLebenslauf(heimat.copy(jahr = 1917), hartesEnde),
            ),
        )
        val zustandAbbruch = AudioRegelwerk.bestimmeZustand(abbruchState, audioAktiv = true)
        assertEquals(AudioSpur.STILLE, zustandAbbruch.aktiveSpur)
        assertTrue(zustandAbbruch.musikGesperrt)
        assertFalse(zustandAbbruch.spieltGerade)
        assertEquals(AudioSperrGrund.AUFFANGNETZ, zustandAbbruch.sperrGrund)
    }

    @Test
    fun koordinatorStopptSofortBeimWechselAufFrontUndEtappe() {
        val fakeAusgabe = FakeAudioAusgabe()
        val koordinator = AudioKoordinator(fakeAusgabe)

        val controller = SpielController(
            content = content,
            random = KotlinRandomSource(Random(77)),
            initialAudioAktiv = true,
        )

        // 1. Startmenü -> ruhige Begleitung startet
        koordinator.synchronisiereZustand(controller.aktuellerZustand.audioZustand)
        assertEquals(1, fakeAusgabe.abgespielteSpuren.size)
        assertEquals(AudioSpur.START_RUHIG, fakeAusgabe.abgespielteSpuren.last().first)

        // 2. Direktwahl Front -> sobald Front betreten wird, wird sofort gestoppt und keine Musik mehr abgespielt
        controller.setzeDirektwahlAktiv(true)
        controller.durchgangBeginnen()
        controller.waehlePerson("buergertum", Geschlecht.MAENNLICH, 18, direktwahlPfad = Pfad.FRONT)

        val vorFrontSpuren = fakeAusgabe.abgespielteSpuren.size
        val vorFrontStopps = fakeAusgabe.stoppAufrufe
        koordinator.synchronisiereZustand(controller.aktuellerZustand.audioZustand)
        assertTrue(fakeAusgabe.stoppAufrufe > vorFrontStopps, "Beim Betreten von Front muss stoppe() gerufen werden.")
        assertEquals(vorFrontSpuren, fakeAusgabe.abgespielteSpuren.size, "Auf Front darf aktualisiere() nicht aufgerufen werden.")

        // Auch beim Weiterklicken in Kapitel und Ereignis an der Front bleibt es strikt still
        controller.starteKapitel()
        koordinator.synchronisiereZustand(controller.aktuellerZustand.audioZustand)
        controller.waehleOption(0)
        koordinator.synchronisiereZustand(controller.aktuellerZustand.audioZustand)
        assertEquals(vorFrontSpuren, fakeAusgabe.abgespielteSpuren.size)

        // 3. Gleichfalls strikte Stille auf Etappe
        val etappeController = SpielController(
            content = content,
            random = KotlinRandomSource(Random(88)),
            initialAudioAktiv = true,
        )
        etappeController.setzeDirektwahlAktiv(true)
        etappeController.durchgangBeginnen()
        etappeController.waehlePerson("adel", Geschlecht.WEIBLICH, 35, direktwahlPfad = Pfad.ETAPPE)
        koordinator.synchronisiereZustand(etappeController.aktuellerZustand.audioZustand)
        assertEquals(vorFrontSpuren, fakeAusgabe.abgespielteSpuren.size)
        assertTrue(etappeController.aktuellerZustand.audioZustand.musikGesperrt)
        assertEquals(AudioSperrGrund.PFAD_ETAPPE, etappeController.aktuellerZustand.audioZustand.sperrGrund)

        koordinator.freigeben()
        assertEquals(1, fakeAusgabe.freigabeAufrufe)
    }

    @Test
    fun syntheseErzeugtStilleBeiStilleSpurUndLeiseSamplesBeiErlaubtenSpuren() {
        val stillePuffer = ByteArray(512) { 42 }
        RuhigeArchivSynthese.fuellePcm16Puffer(AudioSpur.STILLE, 0.3f, 0L, stillePuffer)
        assertTrue(stillePuffer.all { it == 0.toByte() }, "AudioSpur.STILLE muss ausschließlich Null-Samples erzeugen.")

        val heimatPuffer = ByteArray(1024)
        RuhigeArchivSynthese.fuellePcm16Puffer(AudioSpur.HEIMAT_RUHIG, 0.22f, 0L, heimatPuffer)
        assertTrue(heimatPuffer.any { it != 0.toByte() }, "Erlaubte Spur muss sanftes Audiosignal erzeugen.")

        // Spitzenwert bleibt deutlich unter Vollaussteuerung (dezenter Pegel)
        var maxAbs = 0
        for (i in heimatPuffer.indices step 2) {
            val lo = heimatPuffer[i].toInt() and 0xFF
            val hi = heimatPuffer[i + 1].toInt() shl 8
            val sample = (hi or lo).toShort().toInt()
            val absVal = if (sample < 0) -sample else sample
            if (absVal > maxAbs) maxAbs = absVal
        }
        assertTrue(maxAbs in 1..(Short.MAX_VALUE / 4), "Pegel muss dezent bleiben, gefunden maxAbs=$maxAbs")
    }
}
