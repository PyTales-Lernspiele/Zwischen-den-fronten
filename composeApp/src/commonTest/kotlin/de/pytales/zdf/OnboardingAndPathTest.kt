package de.pytales.zdf

import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.engine.KotlinRandomSource
import de.pytales.zdf.engine.RandomSource
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.MusterungsGrad
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.SpielModus
import de.pytales.zdf.model.WertSchluessel
import kotlin.random.Random
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertIs
import kotlin.test.assertNotNull
import kotlin.test.assertTrue

class OnboardingAndPathTest {

    private val content = loadTestGameContent()

    @Test
    fun unterrichtsSchalterDirektwahlFuerAlleDreiPfade() {
        val engine = GameEngine(content, KotlinRandomSource(Random(7)))

        // 1. Direktwahl FRONT
        var front = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.KURZ, direktwahlAktiv = true))
        front = engine.waehlePerson(front, "buergertum", Geschlecht.MAENNLICH, 18, direktwahlPfad = Pfad.FRONT)
        val frontPhase = assertIs<GamePhase.KapitelStart>(front.phase)
        assertEquals(1914, frontPhase.kapitel.jahr)
        assertEquals(Pfad.FRONT, front.pfad)
        assertEquals(MusterungsGrad.KV, front.person?.musterung)
        assertEquals("Musketier", front.person?.stand)
        assertTrue(front.hatMerkmal("buergertum"))
        assertTrue(front.hatMerkmal("gemustert"))
        assertFalse(front.hatMerkmal("kinder"))
        // Front-Basis (8, 2, 1, 8) + Bürgertum (+1 versorgung, -1 aufmerksamkeit) = (9, 2, 0, 8)
        assertEquals(9, front.werte[WertSchluessel.VERSORGUNG])
        assertEquals(2, front.werte[WertSchluessel.BELASTUNG])
        assertEquals(0, front.werte[WertSchluessel.AUFMERKSAMKEIT])
        assertEquals(8, front.werte[WertSchluessel.RUECKHALT])

        // 2. Direktwahl ETAPPE mit Frau -> historisch konsistenter Lazarettdienst
        var etappeW = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.KURZ, direktwahlAktiv = true))
        etappeW = engine.waehlePerson(etappeW, "adel", Geschlecht.WEIBLICH, 35, direktwahlPfad = Pfad.ETAPPE)
        assertIs<GamePhase.KapitelStart>(etappeW.phase)
        assertEquals(Pfad.ETAPPE, etappeW.pfad)
        assertEquals("Etappenlazarett", etappeW.person?.stand)
        assertTrue(etappeW.hatMerkmal("lazarett"))
        assertTrue(etappeW.hatMerkmal("kinder"))
        assertTrue(etappeW.hatMerkmal("aeltere_kinder"))

        // 3. Direktwahl HEIMAT -> gestrafft: Erwerbswahl direkt ins Jahr 1914 (ohne Abschiedskarte)
        var heimat = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.KURZ, direktwahlAktiv = true))
        heimat = engine.waehlePerson(heimat, "arbeiterschaft", Geschlecht.WEIBLICH, 35, direktwahlPfad = Pfad.HEIMAT)
        val erwerbPhase = assertIs<GamePhase.ErwerbWahl>(heimat.phase)
        assertTrue(erwerbPhase.optionen.isNotEmpty())
        assertTrue(heimat.hatMerkmal("ehemann_im_feld"))

        heimat = engine.waehleErwerb(heimat, "ruestung")
        val heimatStart = assertIs<GamePhase.KapitelStart>(heimat.phase)
        assertEquals(1914, heimatStart.kapitel.jahr)
        assertEquals(Pfad.HEIMAT, heimat.pfad)
        assertTrue(heimat.hatMerkmal("ruestung"))
    }

    @Test
    fun regulaererWeiblicherEinstiegMitLazarettUndWechselInEtappe() {
        val engine = GameEngine(content, KotlinRandomSource(Random(99)))
        var s = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.KURZ))
        s = engine.waehlePerson(s, "landbevoelkerung", Geschlecht.WEIBLICH, 18)

        // 18 Jahre -> vater_im_feld, keine Kinder
        assertTrue(s.hatMerkmal("vater_im_feld"))
        assertFalse(s.hatMerkmal("kinder"))
        val erwerbPhase = assertIs<GamePhase.ErwerbWahl>(s.phase)
        assertTrue(erwerbPhase.optionen.any { it.id == "lazarett" })

        s = engine.waehleErwerb(s, "lazarett")
        val etappeFrage = assertIs<GamePhase.EreignisAnzeige>(s.phase)
        assertEquals(GameEngine.EREIGNIS_EINSTIEG_ETAPPE, etappeFrage.ereignis.id)
        assertTrue(etappeFrage.istEinstieg)

        // Option 0: Sich melden -> Wechsel in die Etappe
        s = engine.waehleOption(s, 0)
        assertIs<GamePhase.EreignisAusgang>(s.phase)
        s = engine.weiterNachAusgang(s)
        assertIs<GamePhase.KapitelStart>(s.phase)
        assertEquals(Pfad.ETAPPE, s.pfad)
        assertEquals("Etappenlazarett", s.person?.stand)
        assertEquals(0, s.ziehungenImKapitel)
    }

    @Test
    fun regulaererMaennlicherEinstiegMitMusterungUndOffizierslaufbahn() {
        // Deterministischer RNG: wählt stets die kleinste Zahl -> kv (und bei ukWahrscheinlichkeit 10%
        // erst ab 11 keine UK-Stellung: wir steuern genau 1 für kv und 99 für keine UK).
        val scriptedRng = object : RandomSource {
            private val queue = ArrayDeque(listOf(0, 0, 0, 170, 85, 1, 99, 0))
            override fun nextInt(fromInclusive: Int, untilExclusive: Int): Int {
                val raw = if (queue.isNotEmpty()) queue.removeFirst() else fromInclusive
                return raw.coerceIn(fromInclusive, untilExclusive - 1)
            }
        }
        val engine = GameEngine(content, scriptedRng)
        var s = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.LANG))
        s = engine.waehlePerson(s, "adel", Geschlecht.MAENNLICH, 35)

        val meldung = assertIs<GamePhase.EreignisAnzeige>(s.phase)
        assertEquals(GameEngine.EREIGNIS_EINSTIEG_MELDUNG, meldung.ereignis.id)

        // Option 0: Kriegsfreiwillig melden
        s = engine.waehleOption(s, 0)
        assertTrue(s.hatMerkmal("kriegsfreiwillig"))
        s = engine.weiterNachAusgang(s)

        val musterung = assertIs<GamePhase.MusterungErgebnis>(s.phase)
        assertEquals(MusterungsGrad.KV, musterung.daten.grad)
        assertEquals(Pfad.FRONT, musterung.zielPfad)
        assertNotNull(s.person?.befund)
        assertTrue(s.hatMerkmal("gemustert"))

        // Bestätigen -> Adel + 35 Jahre + Front -> Offizierslaufbahn steht offen
        s = engine.bestaetigeMusterung(s)
        val offizier = assertIs<GamePhase.EreignisAnzeige>(s.phase)
        assertEquals(GameEngine.EREIGNIS_EINSTIEG_OFFIZIER, offizier.ereignis.id)

        s = engine.waehleOption(s, 0)
        assertTrue(s.hatMerkmal("offizier"))
        s = engine.weiterNachAusgang(s)
        assertIs<GamePhase.KapitelStart>(s.phase)
        assertEquals("Offiziersaspirant", s.person?.stand)
        assertEquals(0, s.ziehungenImKapitel)
    }
}
