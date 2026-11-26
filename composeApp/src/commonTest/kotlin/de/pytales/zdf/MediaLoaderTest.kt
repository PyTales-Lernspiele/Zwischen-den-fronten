package de.pytales.zdf

import de.pytales.zdf.ui.media.BildAufloeser
import de.pytales.zdf.ui.media.BildEbene
import de.pytales.zdf.ui.media.ComposeMedienRegister
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNotNull
import kotlin.test.assertNull
import kotlin.test.assertTrue

/**
 * Prüfsuite für AP 5 — Multiplatform-Bild-Loader, Fallback-Ketten, Compose-Drawable-Bindung
 * und WebP-Integrität (Header & exakte Pixelmaße gemäß `content/medienplan.json`).
 */
class MediaLoaderTest {

    private val content = loadTestGameContent()

    @Test
    fun szenenAufloesungNutztStufe2VorStufe1VorPlatzhalter() {
        val nurSchauplatz = setOf("schauplatz_graben")
        val mitEinzelszene = setOf("schauplatz_graben", "front_1916_verdun")

        val stufe2 = BildAufloeser.loeseSzene(
            bildId = "front_1916_verdun",
            schauplatzBild = "schauplatz_graben",
            verfuegbareIds = mitEinzelszene,
        )
        assertEquals("front_1916_verdun", stufe2.aufgeloesteId)
        assertEquals(BildEbene.EINZELSZENE_STUFE2, stufe2.ebene)
        assertFalse(stufe2.istFallback)
        assertTrue(stufe2.istVorhanden)

        val stufe1 = BildAufloeser.loeseSzene(
            bildId = "front_1916_verdun",
            schauplatzBild = "schauplatz_graben",
            verfuegbareIds = nurSchauplatz,
        )
        assertEquals("schauplatz_graben", stufe1.aufgeloesteId)
        assertEquals(BildEbene.SCHAUPLATZ_STUFE1, stufe1.ebene)
        assertTrue(stufe1.istFallback)
        assertTrue(stufe1.istVorhanden)

        val platzhalter = BildAufloeser.loeseSzene(
            bildId = "front_1916_verdun",
            schauplatzBild = "schauplatz_graben",
            verfuegbareIds = emptySet(),
        )
        assertNull(platzhalter.aufgeloesteId)
        assertEquals(BildEbene.PLATZHALTER, platzhalter.ebene)
        assertTrue(platzhalter.istFallback)
        assertFalse(platzhalter.istVorhanden)
    }

    @Test
    fun portraitAufloesungNutztExakteStimmungVorBasisNeutralVorPlatzhalter() {
        val nurBasis = setOf("portrait_arbeiterschaft_w_neutral")
        val mitStimmung = setOf(
            "portrait_arbeiterschaft_w_neutral",
            "portrait_arbeiterschaft_w_hungrig",
        )

        val exakt = BildAufloeser.loesePortrait("portrait_arbeiterschaft_w_hungrig", mitStimmung)
        assertEquals("portrait_arbeiterschaft_w_hungrig", exakt.aufgeloesteId)
        assertEquals(BildEbene.PORTRAIT_STUFE1, exakt.ebene)
        assertFalse(exakt.istFallback)

        val basisFallback = BildAufloeser.loesePortrait("portrait_arbeiterschaft_w_hungrig", nurBasis)
        assertEquals("portrait_arbeiterschaft_w_neutral", basisFallback.aufgeloesteId)
        assertEquals(BildEbene.PORTRAIT_BASIS_FALLBACK, basisFallback.ebene)
        assertTrue(basisFallback.istFallback)

        val unbekannt = BildAufloeser.loesePortrait("portrait_unbekannt_hungrig", nurBasis)
        assertNull(unbekannt.aufgeloesteId)
        assertEquals(BildEbene.PLATZHALTER, unbekannt.ebene)
        assertFalse(unbekannt.istVorhanden)
    }

    @Test
    fun kapitelAufloesungNutztKapitelbildOderArchivPlatzhalter() {
        val vorhanden = BildAufloeser.loeseKapitel("kapitel_1914", setOf("kapitel_1914"))
        assertEquals("kapitel_1914", vorhanden.aufgeloesteId)
        assertEquals(BildEbene.KAPITEL_STUFE1, vorhanden.ebene)
        assertFalse(vorhanden.istFallback)

        val fehlt = BildAufloeser.loeseKapitel("kapitel_1919", setOf("kapitel_1914"))
        assertNull(fehlt.aufgeloesteId)
        assertEquals(BildEbene.PLATZHALTER, fehlt.ebene)
        assertTrue(fehlt.istFallback)
    }

    @Test
    fun composeMedienRegisterStimmtExaktMitMedienplanUndGueltigenWebpDateienUeberein() {
        val plan = content.medienplan
        val portraitMasse = plan.format.portraitMasse[0] to plan.format.portraitMasse[1]
        val szenenMasse = plan.format.szenenMasse[0] to plan.format.szenenMasse[1]
        val dateityp = plan.format.dateityp

        val erwarteteVorhandeneIds = mutableSetOf<String>()

        fun pruefeEintraege(
            ordner: String,
            erwarteteMasse: Pair<Int, Int>,
            eintraege: List<Pair<String, String>>,
        ) {
            for ((id, status) in eintraege) {
                val relPfad = "$ordner/$id.$dateityp"
                val bytes = readTestMediaBytes(relPfad)
                if (status == "vorhanden") {
                    erwarteteVorhandeneIds += id
                    assertNotNull(
                        bytes,
                        "Als 'vorhanden' markiertes Asset fehlt in den Test-Ressourcen: media/$relPfad",
                    )
                    val masse = leseWebpMasse(bytes)
                    assertEquals(
                        erwarteteMasse,
                        masse,
                        "Falsche WebP-Auflösung für '$id': erwartet $erwarteteMasse, gefunden $masse",
                    )
                    assertNotNull(
                        ComposeMedienRegister.drawableFuer(id),
                        "ComposeMedienRegister kennt das vorhandene Drawable '$id' nicht.",
                    )
                } else {
                    assertNull(
                        bytes,
                        "Datei media/$relPfad existiert bereits, steht im Medienplan aber noch auf '$status'.",
                    )
                }
            }
        }

        pruefeEintraege(
            ordner = "portraits",
            erwarteteMasse = portraitMasse,
            eintraege = plan.portraits.map { it.id to it.status },
        )
        pruefeEintraege(
            ordner = "kapitel",
            erwarteteMasse = szenenMasse,
            eintraege = plan.kapitelbilder.map { it.id to it.status },
        )
        pruefeEintraege(
            ordner = "schauplaetze",
            erwarteteMasse = szenenMasse,
            eintraege = plan.schauplatzbilder.map { it.id to it.status },
        )
        pruefeEintraege(
            ordner = "szenen",
            erwarteteMasse = szenenMasse,
            eintraege = plan.einzelSzenenbilder.map { it.id to it.status },
        )

        assertTrue(
            erwarteteVorhandeneIds.size >= 8,
            "Erwartet mindestens die 8 Stil-A-Kernbilder aus AP 5a, gefunden ${erwarteteVorhandeneIds.size}.",
        )
        assertEquals(
            erwarteteVorhandeneIds,
            ComposeMedienRegister.verfuegbareIds,
            "ComposeMedienRegister.verfuegbareIds muss exakt den vorhandenen WebP-Assets entsprechen.",
        )

        // Konkrete End-to-End-Prüfung mit dem realen Register
        val brotschlange = BildAufloeser.loeseSzene(
            bildId = "einstieg_meldung",
            schauplatzBild = "schauplatz_brotschlange",
            verfuegbareIds = ComposeMedienRegister.verfuegbareIds,
        )
        assertTrue(brotschlange.istVorhanden)
        assertEquals("schauplatz_brotschlange", brotschlange.aufgeloesteId)
        assertEquals(BildEbene.SCHAUPLATZ_STUFE1, brotschlange.ebene)

        val arbeiterinHungrig = BildAufloeser.loesePortrait(
            portraitId = "portrait_arbeiterschaft_w_hungrig",
            verfuegbareIds = ComposeMedienRegister.verfuegbareIds,
        )
        assertTrue(arbeiterinHungrig.istVorhanden)
    }

    private fun leseWebpMasse(data: ByteArray): Pair<Int, Int> {
        assertTrue(data.size >= 30, "WebP-Datei zu klein (${data.size} Bytes).")
        assertEquals("RIFF", data.decodeToString(0, 4), "Fehlender RIFF-Header.")
        assertEquals("WEBP", data.decodeToString(8, 12), "Fehlende WEBP-Signatur.")

        return when (val chunk = data.decodeToString(12, 16)) {
            "VP8 " -> {
                assertEquals(0x9d, data[23].toInt() and 0xFF, "Ungültiger VP8-Startcode (Byte 0).")
                assertEquals(0x01, data[24].toInt() and 0xFF, "Ungültiger VP8-Startcode (Byte 1).")
                assertEquals(0x2a, data[25].toInt() and 0xFF, "Ungültiger VP8-Startcode (Byte 2).")
                val w = (u16le(data, 26)) and 0x3FFF
                val h = (u16le(data, 28)) and 0x3FFF
                w to h
            }

            "VP8L" -> {
                assertEquals(0x2f, data[20].toInt() and 0xFF, "Ungültige VP8L-Signatur.")
                val bits = u32le(data, 21)
                ((bits and 0x3FFF) + 1) to (((bits ushr 14) and 0x3FFF) + 1)
            }

            "VP8X" -> {
                val w = u24le(data, 24) + 1
                val h = u24le(data, 27) + 1
                w to h
            }

            else -> error("Unbekannter WebP-Chunk-Typ: $chunk")
        }
    }

    private fun u16le(b: ByteArray, off: Int): Int =
        (b[off].toInt() and 0xFF) or ((b[off + 1].toInt() and 0xFF) shl 8)

    private fun u24le(b: ByteArray, off: Int): Int =
        (b[off].toInt() and 0xFF) or
            ((b[off + 1].toInt() and 0xFF) shl 8) or
            ((b[off + 2].toInt() and 0xFF) shl 16)

    private fun u32le(b: ByteArray, off: Int): Int =
        (b[off].toInt() and 0xFF) or
            ((b[off + 1].toInt() and 0xFF) shl 8) or
            ((b[off + 2].toInt() and 0xFF) shl 16) or
            ((b[off + 3].toInt() and 0xFF) shl 24)
}
