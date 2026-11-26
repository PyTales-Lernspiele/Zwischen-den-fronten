package de.pytales.zdf

import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.HartesEndeId
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.SpielModus
import de.pytales.zdf.model.Stimmung
import de.pytales.zdf.model.WertSchluessel
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNotNull
import kotlin.test.assertTrue

class ContentDeserializationTest {

    private val content = loadTestGameContent()

    @Test
    fun alleSiebenJsonDateienWerdenStrengDeserialisiert() {
        assertEquals("Zwischen den Fronten", content.konfiguration.spielTitel)
        assertEquals(4, content.konfiguration.werte.reihenfolge.size)
        assertEquals(0, content.konfiguration.werte.minimum)
        assertEquals(12, content.konfiguration.werte.maximum)
        assertEquals(5, content.konfiguration.werte.segmenteJeBalken)
        assertTrue(content.konfiguration.werte.balkenVollIstGut)

        assertEquals(4, content.herkunft.herkuenfte.size)
        assertEquals(6, content.herkunft.erwerbslagen.size)
        assertTrue(content.herkunft.direktwahlOption.aktiv)

        assertEquals(6, content.kapitel.kapitel.size)
        assertEquals(listOf(1914, 1915, 1916, 1917, 1918, 1919), content.kapitel.kapitel.map { it.jahr })
        assertEquals(1919, content.kapitel.epilogJahr)

        assertEquals(34, content.merkmale.register.size)
        assertEquals(4, content.merkmale.lebenslauf.faecher.size)
        assertEquals(10, content.merkmale.lebenslauf.ausgaenge.size)

        assertEquals(104, content.ereignisse.anzahl)
        assertEquals(104, content.ereignisse.ereignisse.size)

        assertEquals(20, content.sprachregeln.maxWoerterJeSatz)
        assertEquals(11, content.sprachregeln.tabuBegriffe.size)
        assertEquals(6, content.sprachregeln.pruefBegriffe.size)

        assertEquals(40, content.medienplan.portraits.size)
        assertEquals(6, content.medienplan.kapitelbilder.size)
        assertEquals(17, content.medienplan.schauplatzbilder.size)
        assertEquals(104, content.medienplan.einzelSzenenbilder.size)
    }

    @Test
    fun strikteZweiEntscheidungsRegelUndReferenzenSindVollstaendig() {
        for (ev in content.ereignisse.ereignisse) {
            assertEquals(2, ev.optionen.size, "Ereignis '${ev.id}' muss exakt 2 Optionen haben.")
            assertTrue(ev.text.standard.isNotBlank(), "Ereignis '${ev.id}' hat leeren Standardtext.")
            assertTrue(ev.pfade.isNotEmpty(), "Ereignis '${ev.id}' hat keine Pfade.")
            for (opt in ev.optionen) {
                assertTrue(opt.titel.isNotBlank(), "Option in '${ev.id}' hat keinen Titel.")
                assertTrue(opt.ausgang.standard.isNotBlank(), "Option in '${ev.id}' hat keinen Ausgangstext.")
                opt.folgeEreignis?.let { fe ->
                    assertNotNull(
                        content.ereignisById[fe.id],
                        "Folgeereignis '${fe.id}' aus '${ev.id}' fehlt in ereignisse.json."
                    )
                }
            }
        }

        // Alle Kapitel-Träger existieren und sind kern=true
        for (kap in content.kapitel.kapitel) {
            for (pfad in Pfad.entries) {
                val bogen = kap.bogen[pfad]
                assertNotNull(bogen, "Kapitel ${kap.jahr} hat keinen Bogen für $pfad.")
                for (traegerId in bogen.traeger) {
                    val ev = assertNotNull(
                        content.ereignisById[traegerId],
                        "Träger '$traegerId' in ${kap.jahr}/$pfad existiert nicht."
                    )
                    assertTrue(ev.kern, "Träger '$traegerId' in ${kap.jahr}/$pfad muss kern=true sein.")
                }
            }
        }

        // Alle 40 Live-Emotions-Portraits sind im Medienplan enthalten
        val metrics = GameEngine(content).metrics
        for (herkunft in content.herkunft.herkuenfte) {
            for (geschlecht in Geschlecht.entries) {
                for (stimmung in Stimmung.entries) {
                    val id = metrics.portraitId(herkunft.id, geschlecht, stimmung)
                    assertNotNull(
                        content.portraitById[id],
                        "Portrait '$id' fehlt in medienplan.json."
                    )
                }
            }
        }

        // Alle 4 harten Enden, 4 Werte, 3 Pfade und 2 Modi sind vollständig konfiguriert
        assertEquals(HartesEndeId.entries.toSet(), content.konfiguration.harteEnden.texte.keys)
        assertEquals(WertSchluessel.entries.toSet(), content.konfiguration.werte.definitionen.keys)
        assertEquals(Pfad.entries.toSet(), content.konfiguration.pfade.definitionen.keys)
        assertEquals(SpielModus.entries.toSet(), content.konfiguration.modi.keys)
    }
}
