package de.pytales.zdf

import de.pytales.zdf.audio.ArchivSfxSynthese
import de.pytales.zdf.audio.AudioAusgabe
import de.pytales.zdf.audio.AudioKoordinator
import de.pytales.zdf.audio.AudioRegelwerk
import de.pytales.zdf.audio.AudioSperrGrund
import de.pytales.zdf.audio.AudioSpur
import de.pytales.zdf.audio.RuhigeArchivSynthese
import de.pytales.zdf.audio.SoundEffekt
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
import kotlin.math.abs
import kotlin.math.sqrt
import kotlin.random.Random
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNotEquals
import kotlin.test.assertNull
import kotlin.test.assertTrue

/**
 * Prüfsuite für optionales Audio, getragene Kammermusik-Synthese, taktile Soundeffekte
 * sowie die harte Musiksperre auf `front`, `etappe` und im Auffangnetz.
 */
class AudioRegelwerkTest {

    private val content = loadTestGameContent()
    private val engine = GameEngine(content, KotlinRandomSource(Random(1914)))

    private class FakeAudioAusgabe : AudioAusgabe {
        val abgespielteSpuren = mutableListOf<Pair<AudioSpur, Float>>()
        val abgespielteEffekte = mutableListOf<Pair<SoundEffekt, Float>>()
        var stoppAufrufe: Int = 0
        var freigabeAufrufe: Int = 0

        override fun aktualisiere(spur: AudioSpur, lautstaerke: Float) {
            abgespielteSpuren += spur to lautstaerke
        }

        override fun spieleEffekt(effekt: SoundEffekt, lautstaerke: Float) {
            abgespielteEffekte += effekt to lautstaerke
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

    @Test
    fun koordinatorPausiertImHintergrundUndRespektiertMusiksperreBeiRueckkehr() {
        val fakeAusgabe = FakeAudioAusgabe()
        val koordinator = AudioKoordinator(fakeAusgabe)

        val controller = SpielController(
            content = content,
            random = KotlinRandomSource(Random(91)),
            initialAudioAktiv = true,
        )

        // 1. Startmenü spielt ruhig
        koordinator.synchronisiereZustand(controller.aktuellerZustand.audioZustand)
        assertEquals(1, fakeAusgabe.abgespielteSpuren.size)
        assertEquals(AudioSpur.START_RUHIG, fakeAusgabe.abgespielteSpuren.last().first)

        // 2. App geht in Hintergrund (onPause / onStop) -> Audio stoppt sofort
        val stoppsVorPause = fakeAusgabe.stoppAufrufe
        koordinator.setzeHintergrundPausiert(true)
        assertTrue(koordinator.imHintergrundPausiert)
        assertTrue(fakeAusgabe.stoppAufrufe > stoppsVorPause)

        // Zustandswechsel in erlaubte Heimat während Hintergrund darf kein Audio starten
        controller.setzeDirektwahlAktiv(true)
        controller.durchgangBeginnen()
        controller.waehlePerson("arbeiterschaft", Geschlecht.WEIBLICH, 18, direktwahlPfad = Pfad.HEIMAT)
        koordinator.synchronisiereZustand(controller.aktuellerZustand.audioZustand)
        assertEquals(1, fakeAusgabe.abgespielteSpuren.size)

        // 3. Rückkehr in Vordergrund (onResume) in erlaubter Heimat -> dezente Heimat-Begleitung startet
        koordinator.setzeHintergrundPausiert(false)
        assertFalse(koordinator.imHintergrundPausiert)
        assertEquals(2, fakeAusgabe.abgespielteSpuren.size)
        assertEquals(AudioSpur.HEIMAT_RUHIG, fakeAusgabe.abgespielteSpuren.last().first)

        // 4. Hintergrund + Wechsel auf Front (Musiksperre) -> Rückkehr bleibt strikt stumm
        koordinator.setzeHintergrundPausiert(true)
        val frontController = SpielController(
            content = content,
            random = KotlinRandomSource(Random(92)),
            initialAudioAktiv = true,
        )
        frontController.setzeDirektwahlAktiv(true)
        frontController.durchgangBeginnen()
        frontController.waehlePerson("buergertum", Geschlecht.MAENNLICH, 18, direktwahlPfad = Pfad.FRONT)
        koordinator.synchronisiereZustand(frontController.aktuellerZustand.audioZustand)
        koordinator.setzeHintergrundPausiert(false)
        assertEquals(2, fakeAusgabe.abgespielteSpuren.size, "Nach Rückkehr auf Front darf keine Musik starten.")

        // 5. Stummgeschaltet im Hintergrund -> Rückkehr bleibt stumm
        controller.setzeAudioAktiv(false)
        koordinator.synchronisiereZustand(controller.aktuellerZustand.audioZustand)
        koordinator.setzeHintergrundPausiert(true)
        koordinator.setzeHintergrundPausiert(false)
        assertEquals(2, fakeAusgabe.abgespielteSpuren.size, "Stummgeschalteter Ton darf nach Rückkehr nicht starten.")
    }

    @Test
    fun kammermusikHatEchteDynamikRuhepausenUndNahtlosenLoopKeinStatischerDauerton() {
        val spuren = listOf(AudioSpur.START_RUHIG, AudioSpur.HEIMAT_RUHIG, AudioSpur.EPILOG_RUHIG)
        val ersteBloecke = mutableMapOf<AudioSpur, ByteArray>()

        for (spur in spuren) {
            val partitur = RuhigeArchivSynthese.partiturFuer(spur)
            assertTrue(
                partitur.dauerSekunden in 30.0..60.0,
                "Komposition $spur soll 30–60 s Zyklus besitzen, gefunden: ${partitur.dauerSekunden}",
            )
            assertTrue(partitur.klavierNoten.size >= 10, "$spur braucht eine echte Klavier-Phrasierung.")
            assertTrue(partitur.celloBoegen.isNotEmpty(), "$spur braucht getragene tiefe Cello-Bögen.")
            assertTrue(
                partitur.klavierNoten.map { it.midiNote }.toSet().size >= 5,
                "$spur muss melodisch-harmonische Bewegung statt statischem Dreiklang haben.",
            )

            // Messfenster von 0,5 s über den gesamten Zyklus -> echte Ruhepausen + Klangspitzen prüfen
            val fensterSamples = RuhigeArchivSynthese.SAMPLE_RATE / 2
            val puffer = ByteArray(fensterSamples * 2)
            val fensterAnzahl = (partitur.dauerSekunden * 2.0).toInt()
            val rmsWerte = mutableListOf<Double>()
            var maxAbsGesamt = 0

            for (f in 0 until fensterAnzahl) {
                val startSample = f.toLong() * fensterSamples
                RuhigeArchivSynthese.fuellePcm16Puffer(spur, 0.24f, startSample, puffer)
                if (f == 0) {
                    ersteBloecke[spur] = puffer.copyOf(2048)
                }
                var sumSq = 0.0
                for (i in puffer.indices step 2) {
                    val sample = lesePcm16Sample(puffer, i)
                    val a = abs(sample)
                    if (a > maxAbsGesamt) maxAbsGesamt = a
                    sumSq += sample.toDouble() * sample.toDouble()
                }
                rmsWerte += sqrt(sumSq / fensterSamples)
            }

            val stilleFenster = rmsWerte.count { it < 20.0 }
            val aktiveSpitze = rmsWerte.maxOrNull() ?: 0.0
            assertTrue(
                stilleFenster >= 6,
                "$spur muss echte Ruhepausen/Atemräume ohne Dauerton haben (stille 0,5s-Fenster: $stilleFenster).",
            )
            assertTrue(
                aktiveSpitze > 180.0,
                "$spur braucht klar hörbare musikalische Phrasen (max RMS: $aktiveSpitze).",
            )
            assertTrue(
                maxAbsGesamt <= Short.MAX_VALUE / 3,
                "$spur muss dezent ausgesteuert bleiben (maxAbs=$maxAbsGesamt).",
            )

            // Nahtloser, knackfreier Loop-Übergang an der Zyklusgrenze
            val gesamtSamples = (partitur.dauerSekunden * RuhigeArchivSynthese.SAMPLE_RATE).toLong()
            val grenzePuffer = ByteArray(4)
            RuhigeArchivSynthese.fuellePcm16Puffer(spur, 0.24f, gesamtSamples - 1, grenzePuffer)
            val letztes = lesePcm16Sample(grenzePuffer, 0)
            val erstes = lesePcm16Sample(grenzePuffer, 2)
            assertTrue(
                abs(erstes - letztes) < 400,
                "Knackfreier Loop-Übergang verletzt bei $spur: letztes=$letztes, erstes=$erstes",
            )
        }

        // Alle drei Spuren klingen eigenständig unterschiedlich
        assertFalse(ersteBloecke.getValue(AudioSpur.START_RUHIG).contentEquals(ersteBloecke.getValue(AudioSpur.HEIMAT_RUHIG)))
        assertFalse(ersteBloecke.getValue(AudioSpur.HEIMAT_RUHIG).contentEquals(ersteBloecke.getValue(AudioSpur.EPILOG_RUHIG)))
        assertFalse(ersteBloecke.getValue(AudioSpur.START_RUHIG).contentEquals(ersteBloecke.getValue(AudioSpur.EPILOG_RUHIG)))
    }

    @Test
    fun soundEffekteSyntheseUndSchutzregelnUnterMusiksperreUndAuffangnetz() {
        // 1. PCM-Synthese aller 4 Effekte erzeugt saubere, dezente Wellenformen und Stille bei Pegel 0
        for (effekt in SoundEffekt.entries) {
            val stumm = ArchivSfxSynthese.erzeugePcm16(effekt, 0f)
            assertTrue(stumm.all { it == 0.toByte() }, "$effekt muss bei Lautstärke 0 komplett still sein.")

            val pcm = ArchivSfxSynthese.erzeugePcm16(effekt, 0.24f)
            assertTrue(pcm.isNotEmpty())
            var maxAbs = 0
            for (i in pcm.indices step 2) {
                val a = abs(lesePcm16Sample(pcm, i))
                if (a > maxAbs) maxAbs = a
            }
            assertTrue(
                maxAbs in 20..(Short.MAX_VALUE / 2),
                "$effekt muss ein sanftes, hörbares Signal erzeugen (maxAbs=$maxAbs).",
            )
        }
        assertNotEquals(
            ArchivSfxSynthese.dauerMsFuer(SoundEffekt.KLICK_SANFT),
            ArchivSfxSynthese.dauerMsFuer(SoundEffekt.ENTSCHEIDUNG),
        )

        // 2. Regelwerk & Koordinator: abgeschaltete Effekte sind immer stumm
        val fake = FakeAudioAusgabe()
        val koordinator = AudioKoordinator(fake)
        val startState = engine.neuesSpiel()
        koordinator.synchronisiere(startState, audioAktiv = false, effekteAktiv = false)
        for (effekt in SoundEffekt.entries) {
            assertFalse(koordinator.spieleEffekt(effekt))
        }
        assertTrue(fake.abgespielteEffekte.isEmpty())

        // 3. Effekte unabhängig von Grundmusik erlaubt (Startmenü / Heimat)
        koordinator.synchronisiere(startState, audioAktiv = false, effekteAktiv = true)
        assertTrue(koordinator.spieleEffekt(SoundEffekt.KLICK_SANFT))
        assertTrue(koordinator.spieleEffekt(SoundEffekt.ENTSCHEIDUNG))
        assertTrue(koordinator.spieleEffekt(SoundEffekt.KAPITELWECHSEL))
        assertTrue(koordinator.spieleEffekt(SoundEffekt.EINSCHNITT))
        assertEquals(4, fake.abgespielteEffekte.size)

        // 4. Unter Musiksperre (Front / Etappe): taktile Papier-/Klicklaute ja, musikalische Impulse NEIN
        var front = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.KURZ, direktwahlAktiv = true))
        front = engine.waehlePerson(front, "buergertum", Geschlecht.MAENNLICH, 18, direktwahlPfad = Pfad.FRONT)
        koordinator.synchronisiere(front, audioAktiv = true, effekteAktiv = true)
        assertTrue(koordinator.spieleEffekt(SoundEffekt.KLICK_SANFT))
        assertTrue(koordinator.spieleEffekt(SoundEffekt.ENTSCHEIDUNG))
        assertFalse(koordinator.spieleEffekt(SoundEffekt.KAPITELWECHSEL), "Kein musikalischer Kapitelimpuls an der Front.")
        assertFalse(koordinator.spieleEffekt(SoundEffekt.EINSCHNITT), "Kein musikalischer Einschnitt-Ton an der Front.")

        // 5. Im Auffangnetz: EINSCHNITT & KAPITELWECHSEL strikt verboten (niemals Game-Over-Jingle!)
        var heimat = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.KURZ, direktwahlAktiv = true))
        heimat = engine.waehlePerson(heimat, "arbeiterschaft", Geschlecht.WEIBLICH, 18, direktwahlPfad = Pfad.HEIMAT)
        val hartesEnde = HartesEndeErgebnis(
            id = HartesEndeId.ENDE_VERHUNGERT,
            titel = "Verhungert",
            text = "Ein ruhiger Einschnitt.",
            jahr = 1917,
        )
        val auffangState = heimat.copy(
            jahr = 1917,
            phase = GamePhase.Abgeschlossen(
                hartesEnde = hartesEnde,
                lebenslauf = engine.lebenslaufCalculator.berechneLebenslauf(heimat.copy(jahr = 1917), hartesEnde),
            ),
        )
        koordinator.synchronisiere(auffangState, audioAktiv = true, effekteAktiv = true)
        assertFalse(koordinator.spieleEffekt(SoundEffekt.EINSCHNITT), "Im Auffangnetz darf kein musikalischer Ton erklingen.")
        assertFalse(koordinator.spieleEffekt(SoundEffekt.KAPITELWECHSEL))

        // 6. Im Hintergrund pausiert: auch Klickgeräusche strikt blockiert
        koordinator.synchronisiere(startState, audioAktiv = true, effekteAktiv = true)
        koordinator.setzeHintergrundPausiert(true)
        assertFalse(koordinator.spieleEffekt(SoundEffekt.KLICK_SANFT))
    }

    private fun lesePcm16Sample(puffer: ByteArray, byteIndex: Int): Int {
        val lo = puffer[byteIndex].toInt() and 0xFF
        val hi = puffer[byteIndex + 1].toInt() shl 8
        return (hi or lo).toShort().toInt()
    }
}
