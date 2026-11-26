package de.pytales.zdf

import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.engine.KotlinRandomSource
import de.pytales.zdf.engine.RandomSource
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.HartesEndeId
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.SpielModus
import kotlin.random.Random
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertIs
import kotlin.test.assertNull
import kotlin.test.assertTrue

class EventDrawingAndChainsTest {

    private val content = loadTestGameContent()

    @Test
    fun modusFilterungGewichtBonusUndKapitelTraegerZuschlag() {
        val engine = GameEngine(content, KotlinRandomSource(Random(11)))

        var kurz = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.KURZ, direktwahlAktiv = true))
        kurz = engine.waehlePerson(kurz, "arbeiterschaft", Geschlecht.MAENNLICH, 18, direktwahlPfad = Pfad.FRONT)

        val verfuegbarKurz = engine.verfuegbareEreignisse(kurz)
        assertTrue(verfuegbarKurz.isNotEmpty())
        assertTrue(verfuegbarKurz.all { it.kern })
        assertTrue(verfuegbarKurz.none { it.nurKette })

        // Kapitel 1914 Front hat Träger: front_1914_marsch und front_1914_erster_toter
        val offeneTraeger = engine.offeneBogenTraeger(kurz)
        assertEquals(setOf("front_1914_marsch", "front_1914_erster_toter"), offeneTraeger)

        val marsch = content.ereignisById.getValue("front_1914_marsch")
        assertEquals(marsch.gewicht + content.kapitel.bogenZuschlag, engine.ereignisGewicht(kurz, marsch))

        // Sobald einer der Träger gespielt wurde, entfällt der Bogen-Zuschlag für alle
        val nachTraeger = kurz.copy(gespielteEreignisse = kurz.gespielteEreignisse + "front_1914_marsch")
        assertTrue(engine.offeneBogenTraeger(nachTraeger).isEmpty())
        val toter = content.ereignisById.getValue("front_1914_erster_toter")
        assertEquals(toter.gewicht, engine.ereignisGewicht(nachTraeger, toter))

        // gewichtBonus: front_1914_schanzen hat +4 bei ohne_mantel
        val schanzen = content.ereignisById.getValue("front_1914_schanzen")
        assertEquals(schanzen.gewicht, engine.ereignisGewicht(kurz, schanzen))
        val ohneMantel = kurz.copy(merkmale = kurz.merkmale + "ohne_mantel")
        assertEquals(schanzen.gewicht + 4, engine.ereignisGewicht(ohneMantel, schanzen))
    }

    @Test
    fun entscheidungsKetteWirdVorgemerktUndImZieljahrPriorisiertGezogen() {
        val engine = GameEngine(content, KotlinRandomSource(Random(21)))
        var s = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.LANG, direktwahlAktiv = true))
        s = engine.waehlePerson(s, "arbeiterschaft", Geschlecht.MAENNLICH, 18, direktwahlPfad = Pfad.FRONT)

        // 1915: front_kamerad Option 0 merkt front_nachfrage mit abJahr = 1 (also ab 1916) vor
        val kamerad = content.ereignisById.getValue("front_kamerad")
        s = s.copy(
            jahr = 1915,
            ziehungenImKapitel = 0,
            phase = GamePhase.EreignisAnzeige(kamerad, kamerad.text.standard),
        )
        s = engine.waehleOption(s, 0)
        assertTrue(s.hatMerkmal("kamerad_gedeckt"))
        assertEquals(1, s.vorgemerkteKetten.size)
        assertEquals("front_nachfrage", s.vorgemerkteKetten.first().ereignisId)
        assertEquals(1916, s.vorgemerkteKetten.first().abJahr)

        // Im Jahr 1915 ist front_nachfrage noch NICHT fällig
        s = engine.weiterNachAusgang(s)
        val zweites1915 = assertIs<GamePhase.EreignisAnzeige>(s.phase)
        assertTrue(zweites1915.ereignis.id != "front_nachfrage")
        assertEquals(1, s.vorgemerkteKetten.size)

        // Wechsel nach 1916 -> erste Ziehung muss zwingend die fällige Kette `front_nachfrage` sein!
        val kap1915 = content.kapitelByJahr.getValue(1915)
        s = s.copy(
            phase = GamePhase.KapitelAbschluss(kap1915, kap1915.bogen.getValue(Pfad.FRONT))
        )
        s = engine.naechstesKapitelStarten(s)
        assertEquals(1916, s.jahr)
        s = engine.starteKapitel(s)
        val gezogen1916 = assertIs<GamePhase.EreignisAnzeige>(s.phase)
        assertEquals("front_nachfrage", gezogen1916.ereignis.id)
        assertTrue(s.vorgemerkteKetten.isEmpty())
    }

    @Test
    fun wiederholbareKartenWerdenBeimKapitelwechselFreigegeben() {
        val engine = GameEngine(content, KotlinRandomSource(Random(31)))
        var s = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.LANG, direktwahlAktiv = true))
        s = engine.waehlePerson(s, "arbeiterschaft", Geschlecht.MAENNLICH, 18, direktwahlPfad = Pfad.FRONT)

        val kap1914 = content.kapitelByJahr.getValue(1914)
        // front_trommelfeuer ist wiederholbar=true, front_1914_marsch ist wiederholbar=false
        s = s.copy(
            gespielteEreignisse = listOf("front_trommelfeuer", "front_1914_marsch"),
            phase = GamePhase.KapitelAbschluss(kap1914, kap1914.bogen.getValue(Pfad.FRONT)),
        )
        s = engine.naechstesKapitelStarten(s)
        assertFalse("front_trommelfeuer" in s.gespielteEreignisse)
        assertTrue("front_1914_marsch" in s.gespielteEreignisse)
    }

    @Test
    fun zufallsAusgangGefallenFuehrtDirektInRespektvollesAuffangnetz() {
        // front_gas Option 1 („Auf die Böschung steigen“) hat zufallsAusgaenge: gewicht 5 (ueberlebt), gewicht 1 (ende_gefallen).
        // Bei pickWeighted mit roll = 6 (= gesamt) trifft es ende_gefallen.
        val lethalRng = object : RandomSource {
            override fun nextInt(fromInclusive: Int, untilExclusive: Int): Int = untilExclusive - 1
        }
        val engine = GameEngine(content, lethalRng)
        var s = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.KURZ, direktwahlAktiv = true))
        s = engine.waehlePerson(s, "arbeiterschaft", Geschlecht.MAENNLICH, 18, direktwahlPfad = Pfad.FRONT)

        val gas = content.ereignisById.getValue("front_gas")
        s = s.copy(
            jahr = 1915,
            phase = GamePhase.EreignisAnzeige(gas, gas.text.standard),
        )
        s = engine.waehleOption(s, 1)
        val ende = assertIs<GamePhase.Abgeschlossen>(s.phase)
        assertEquals(HartesEndeId.ENDE_GEFALLEN, ende.hartesEnde?.id)
        assertTrue(ende.lebenslauf.istVorzeitigerAbbruch)
        assertEquals(4, ende.lebenslauf.faecher.size)
        assertEquals("Gefallen", ende.lebenslauf.faecher[3].merkmalName)
    }

    @Test
    fun epilog1919EndetMitWirtshausWahlUndFuehrtInDenLebenslauf() {
        val engine = GameEngine(content, KotlinRandomSource(Random(42)))
        var s = engine.herkunftWahlOeffnen(engine.neuesSpiel(SpielModus.KURZ, direktwahlAktiv = true))
        s = engine.waehlePerson(s, "buergertum", Geschlecht.MAENNLICH, 35, direktwahlPfad = Pfad.ETAPPE)

        val kap1919 = content.kapitelByJahr.getValue(1919)
        s = s.copy(
            jahr = 1919,
            ziehungenImKapitel = 0,
            phase = GamePhase.KapitelStart(kap1919),
        )
        // Kurz-Modus 1919 hat 1 Ziehung vor dem Finale
        s = engine.starteKapitel(s)
        assertIs<GamePhase.EreignisAnzeige>(s.phase)
        s = engine.waehleOption(s, 0)
        s = engine.weiterNachAusgang(s)

        // Danach zwingend das 1919-Finale `wirtshaus_wahl`
        val finale = assertIs<GamePhase.EreignisAnzeige>(s.phase)
        assertEquals(GameEngine.EREIGNIS_FINALE_WIRTSHAUS, finale.ereignis.id)
        assertTrue(finale.istFinale)
        assertTrue(finale.aufgeloesterText.contains("Listen geführt"))

        // Option 0: Widersprechen -> Merkmal `wirtshaus_widersprochen` in Fach 3
        s = engine.waehleOption(s, 0)
        assertTrue(s.hatMerkmal("wirtshaus_widersprochen"))
        s = engine.weiterNachAusgang(s)

        val abgeschlossen = assertIs<GamePhase.Abgeschlossen>(s.phase)
        assertNull(abgeschlossen.hartesEnde)
        assertFalse(abgeschlossen.lebenslauf.istVorzeitigerAbbruch)
        assertEquals("wirtshaus_widersprochen", abgeschlossen.lebenslauf.faecher[3].merkmalId)
    }
}
