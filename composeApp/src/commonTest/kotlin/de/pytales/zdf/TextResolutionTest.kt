package de.pytales.zdf

import de.pytales.zdf.engine.TextResolver
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.TextFassung
import de.pytales.zdf.model.TextVariante
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class TextResolutionTest {

    private val content = loadTestGameContent()
    private val prioritaet = content.merkmale.textPrioritaet

    @Test
    fun pfadVariantenBeiWirtshausWahlWerdenKorrektAufgeloest() {
        val wirtshaus = content.ereignisById.getValue("wirtshaus_wahl")

        val front = TextResolver.aufloesen(wirtshaus.text, 1919, Pfad.FRONT, emptyList(), prioritaet)
        val etappe = TextResolver.aufloesen(wirtshaus.text, 1919, Pfad.ETAPPE, emptyList(), prioritaet)
        val heimat = TextResolver.aufloesen(wirtshaus.text, 1919, Pfad.HEIMAT, emptyList(), prioritaet)

        assertTrue(front.contains("vier Jahre vorn"))
        assertTrue(etappe.contains("Listen geführt"))
        assertTrue(heimat.contains("vier Jahre angestanden"))
    }

    @Test
    fun jahresStufenBeiTrommelfeuerUndBrotschlangeAusgang() {
        val trommelfeuer = content.ereignisById.getValue("front_trommelfeuer")
        val t1914 = TextResolver.aufloesen(trommelfeuer.text, 1914, Pfad.FRONT, emptyList(), prioritaet)
        val t1916 = TextResolver.aufloesen(trommelfeuer.text, 1916, Pfad.FRONT, emptyList(), prioritaet)
        val t1918 = TextResolver.aufloesen(trommelfeuer.text, 1918, Pfad.FRONT, emptyList(), prioritaet)

        assertTrue(t1914.contains("So etwas hat keiner von euch vorher gehört"))
        assertTrue(t1916.contains("seit zwei Tagen"))
        assertTrue(t1918.contains("nicht mehr Tage"))

        // Option 0 von heimat_brotschlange hat abJahr 1914, 1916, 1918 -> 1915 greift 1914, 1917 greift 1916
        val brotAusgang = content.ereignisById.getValue("heimat_brotschlange").optionen[0].ausgang
        val a1914 = TextResolver.aufloesen(brotAusgang, 1914, Pfad.HEIMAT, emptyList(), prioritaet)
        val a1915 = TextResolver.aufloesen(brotAusgang, 1915, Pfad.HEIMAT, emptyList(), prioritaet)
        val a1916 = TextResolver.aufloesen(brotAusgang, 1916, Pfad.HEIMAT, emptyList(), prioritaet)
        val a1917 = TextResolver.aufloesen(brotAusgang, 1917, Pfad.HEIMAT, emptyList(), prioritaet)
        val a1918 = TextResolver.aufloesen(brotAusgang, 1918, Pfad.HEIMAT, emptyList(), prioritaet)

        assertEquals(a1914, a1915)
        assertEquals(a1916, a1917)
        assertTrue(a1914 != a1916 && a1916 != a1918)
    }

    @Test
    fun kombinierteJahrUndMerkmalVariantenBeachtenJahresVorzugUndPrioritaet() {
        val todesnachricht = content.ereignisById.getValue("heimat_todesnachricht")

        // 1915 nutzt die 1914er Jahresstufe + Merkmal-Variante
        val ehemann1915 = TextResolver.aufloesen(
            todesnachricht.text, 1915, Pfad.HEIMAT, listOf("ehemann_im_feld"), prioritaet
        )
        assertTrue(ehemann1915.contains("Witwenantrag"))

        val vater1915 = TextResolver.aufloesen(
            todesnachricht.text, 1915, Pfad.HEIMAT, listOf("vater_im_feld"), prioritaet
        )
        assertTrue(vater1915.contains("Die Jüngste fragt"))

        // In 1917 gewinnt die neuere 1917er Jahresstufe gegenüber dem 1914er Merkmalstext
        val jahr1917 = TextResolver.aufloesen(
            todesnachricht.text, 1917, Pfad.HEIMAT, listOf("ehemann_im_feld"), prioritaet
        )
        assertTrue(jahr1917.contains("dritte schwarze Streifen"))

        // Winterstellung 1917 mit und ohne ohne_mantel vs 1918
        val winter = content.ereignisById.getValue("front_1917_winterstellung")
        val mitMantel = TextResolver.aufloesen(winter.text, 1917, Pfad.FRONT, emptyList(), prioritaet)
        val ohneMantel = TextResolver.aufloesen(winter.text, 1917, Pfad.FRONT, listOf("ohne_mantel"), prioritaet)
        val winter1918 = TextResolver.aufloesen(winter.text, 1918, Pfad.FRONT, listOf("ohne_mantel"), prioritaet)

        assertTrue(mitMantel.contains("Pumpe ist eingefroren"))
        assertTrue(ohneMantel.contains("Über der Jacke hast du nichts mehr"))
        assertTrue(winter1918.contains("Fußlappen"))
    }

    @Test
    fun textPrioritaetEntscheidetBeiMehrerenPassendenMerkmalenUndFaelltSonstAufStandardZurueck() {
        val fassung = TextFassung(
            standard = "Standardtext",
            varianten = listOf(
                TextVariante(text = "Arbeiterschaft-Text", merkmal = "arbeiterschaft"),
                TextVariante(text = "Offizier-Text", merkmal = "offizier"),
            ),
        )
        // offizier steht vor arbeiterschaft in merkmale.json -> textPrioritaet
        val beide = TextResolver.aufloesen(
            fassung, 1915, Pfad.FRONT, listOf("arbeiterschaft", "offizier"), prioritaet
        )
        assertEquals("Offizier-Text", beide)

        val keine = TextResolver.aufloesen(
            fassung, 1915, Pfad.FRONT, listOf("buergertum"), prioritaet
        )
        assertEquals("Standardtext", keine)
    }
}
