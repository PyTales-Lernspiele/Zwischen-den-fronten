package de.pytales.zdf

import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import de.pytales.zdf.ui.theme.AnzeigeSkalierung
import de.pytales.zdf.ui.theme.ArchivFarben
import de.pytales.zdf.ui.theme.ArchivKontrast
import de.pytales.zdf.ui.theme.ArchivUebergaenge
import de.pytales.zdf.ui.theme.HexColorParser
import de.pytales.zdf.ui.theme.LayoutKlasse
import de.pytales.zdf.ui.theme.Schriftgroesse
import de.pytales.zdf.ui.theme.buildArchivTypography
import de.pytales.zdf.ui.theme.layoutMetrikFuer
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertFalse
import kotlin.test.assertTrue

class ArchivThemeTest {

    private val content = loadTestGameContent()

    @Test
    fun hexColorParserUnterstuetztRgbArgbUndLehntUngueltigeWerteAb() {
        assertEquals(0xFFEFE9DCL, HexColorParser.parseArgb("#efe9dc"))
        assertEquals(0xFFEFE9DCL, HexColorParser.parseArgb("  EFE9DC "))
        assertEquals(0x8015130FL, HexColorParser.parseArgb("#8015130f"))
        assertEquals(Color(0xFF8A3324), HexColorParser.parseColor("#8a3324"))

        assertFailsWith<IllegalArgumentException> { HexColorParser.parseArgb("") }
        assertFailsWith<IllegalArgumentException> { HexColorParser.parseArgb("#fff") }
        assertFailsWith<IllegalArgumentException> { HexColorParser.parseArgb("#12345g") }
        assertFailsWith<IllegalArgumentException> { HexColorParser.parseArgb("#+12345") }
        assertFailsWith<IllegalArgumentException> { HexColorParser.parseArgb("#1234567") }

        val fallback = Color(0xFF1F1C18)
        assertEquals(fallback, HexColorParser.parseColorOrDefault("ungueltig", fallback))
        assertEquals(Color(0xFF8A3324), HexColorParser.parseColorOrDefault("#8a3324", fallback))
    }

    @Test
    fun archivFarbenWerdenDirektAusKonfigurationJsonGebautUndEntsprechenDefault() {
        val ausJson = ArchivFarben.fromFarbwelt(content.konfiguration.farbwelt)
        val standard = ArchivFarben.default()

        assertEquals(standard, ausJson)
        assertEquals(Color(0xFFEFE9DC), ausJson.papier)
        assertEquals(Color(0xFFF7F3EA), ausJson.papierHell)
        assertEquals(Color(0xFFE2DBCA), ausJson.papierDunkel)
        assertEquals(Color(0xFF1F1C18), ausJson.tinte)
        assertEquals(Color(0xFF8A3324), ausJson.akzent)
        assertEquals(Color(0xFF15130F), ausJson.dunkel)

        assertEquals(5, ausJson.stufen.size)
        assertEquals(5, ausJson.stufenHell.size)
        assertEquals(5, ausJson.stufen.toSet().size)
        assertEquals(5, ausJson.stufenHell.toSet().size)

        // Bereichsbegrenzung bei extremen Stufenindizes
        assertEquals(ausJson.stufen.first(), ausJson.stufenFarbe(-5))
        assertEquals(ausJson.stufen.last(), ausJson.stufenFarbe(99))
        assertEquals(ausJson.stufenHell.first(), ausJson.stufenFarbeHell(-1))
        assertEquals(ausJson.stufenHell.last(), ausJson.stufenFarbeHell(42))

        // Deltafarben: schlechter -> kritische Stufe, besser -> gute Stufe
        assertEquals(ausJson.stufen.last(), ausJson.deltaFarbe(schlechter = true, aufDunkel = false))
        assertEquals(ausJson.stufen.first(), ausJson.deltaFarbe(schlechter = false, aufDunkel = false))
        assertEquals(ausJson.stufenHell.last(), ausJson.deltaFarbe(schlechter = true, aufDunkel = true))
        assertEquals(ausJson.stufenHell.first(), ausJson.deltaFarbe(schlechter = false, aufDunkel = true))

        // Material-3-ColorScheme-Mapping prüfen
        val scheme = ausJson.toMaterialColorScheme()
        assertEquals(ausJson.papier, scheme.background)
        assertEquals(ausJson.tinte, scheme.onBackground)
        assertEquals(ausJson.papierHell, scheme.surface)
        assertEquals(ausJson.tinte, scheme.onSurface)
        assertEquals(ausJson.akzent, scheme.primary)
        assertEquals(ausJson.dunkel, scheme.inverseSurface)
        assertEquals(ausJson.textHell, scheme.inverseOnSurface)
    }

    @Test
    fun schriftgroessenSkalierenMonotonUndSindBeamerTauglich() {
        assertEquals(listOf("klein", "mittel", "gross"), Schriftgroesse.entries.map { it.code })
        assertEquals(Schriftgroesse.KLEIN, Schriftgroesse.fromCode("KLEIN"))
        assertEquals(Schriftgroesse.GROSS, Schriftgroesse.fromCode(" gross "))
        assertEquals(Schriftgroesse.MITTEL, Schriftgroesse.fromCode("unbekannt"))
        assertEquals(Schriftgroesse.MITTEL, Schriftgroesse.fromCode(null))

        assertEquals(Schriftgroesse.MITTEL, Schriftgroesse.KLEIN.naechste())
        assertEquals(Schriftgroesse.GROSS, Schriftgroesse.MITTEL.naechste())
        assertEquals(Schriftgroesse.GROSS, Schriftgroesse.GROSS.naechste())
        assertEquals(Schriftgroesse.MITTEL, Schriftgroesse.GROSS.vorherige())
        assertEquals(Schriftgroesse.KLEIN, Schriftgroesse.MITTEL.vorherige())
        assertEquals(Schriftgroesse.KLEIN, Schriftgroesse.KLEIN.vorherige())

        val klein = buildArchivTypography(Schriftgroesse.KLEIN)
        val mittel = buildArchivTypography(Schriftgroesse.MITTEL)
        val gross = buildArchivTypography(Schriftgroesse.GROSS)

        val stile = listOf(
            Triple(klein.displaySmall, mittel.displaySmall, gross.displaySmall),
            Triple(klein.headlineLarge, mittel.headlineLarge, gross.headlineLarge),
            Triple(klein.headlineMedium, mittel.headlineMedium, gross.headlineMedium),
            Triple(klein.headlineSmall, mittel.headlineSmall, gross.headlineSmall),
            Triple(klein.titleLarge, mittel.titleLarge, gross.titleLarge),
            Triple(klein.titleMedium, mittel.titleMedium, gross.titleMedium),
            Triple(klein.titleSmall, mittel.titleSmall, gross.titleSmall),
            Triple(klein.bodyLarge, mittel.bodyLarge, gross.bodyLarge),
            Triple(klein.bodyMedium, mittel.bodyMedium, gross.bodyMedium),
            Triple(klein.bodySmall, mittel.bodySmall, gross.bodySmall),
            Triple(klein.labelLarge, mittel.labelLarge, gross.labelLarge),
            Triple(klein.labelMedium, mittel.labelMedium, gross.labelMedium),
            Triple(klein.labelSmall, mittel.labelSmall, gross.labelSmall),
        )

        stile.forEach { (k, m, g) ->
            assertTrue(k.fontSize.value < m.fontSize.value, "Erwartet klein < mittel für $k / $m")
            assertTrue(m.fontSize.value < g.fontSize.value, "Erwartet mittel < gross für $m / $g")
            assertTrue(k.lineHeight.value > k.fontSize.value)
            assertTrue(m.lineHeight.value > m.fontSize.value)
            assertTrue(g.lineHeight.value > g.fontSize.value)
        }

        // Unterrichts-/Beamer-Lesbarkeit sicherstellen
        assertTrue(klein.bodyLarge.fontSize >= 14.sp)
        assertTrue(mittel.bodyLarge.fontSize >= 16.sp)
        assertTrue(gross.bodyLarge.fontSize >= 20.sp)
    }

    @Test
    fun layoutBreakpointsUndResponsiveMetrikenGreifenExakt() {
        assertEquals(LayoutKlasse.KOMPAKT, LayoutKlasse.vonBreiteDp(0f))
        assertEquals(LayoutKlasse.KOMPAKT, LayoutKlasse.vonBreiteDp(360f))
        assertEquals(LayoutKlasse.KOMPAKT, LayoutKlasse.vonBreiteDp(599.9f))

        assertEquals(LayoutKlasse.MITTEL, LayoutKlasse.vonBreiteDp(600f))
        assertEquals(LayoutKlasse.MITTEL, LayoutKlasse.vonBreiteDp(768f))
        assertEquals(LayoutKlasse.MITTEL, LayoutKlasse.vonBreiteDp(959.9f))

        assertEquals(LayoutKlasse.BREIT, LayoutKlasse.vonBreiteDp(960f))
        assertEquals(LayoutKlasse.BREIT, LayoutKlasse.vonBreiteDp(1200f))
        assertEquals(LayoutKlasse.BREIT, LayoutKlasse.vonBreiteDp(1920f))
        assertEquals(LayoutKlasse.BREIT, LayoutKlasse.vonBreite(1280.dp))

        val kompakt = layoutMetrikFuer(LayoutKlasse.KOMPAKT, Schriftgroesse.MITTEL)
        val mittel = layoutMetrikFuer(LayoutKlasse.MITTEL, Schriftgroesse.MITTEL)
        val mittelSmartphoneQuer = layoutMetrikFuer(LayoutKlasse.MITTEL, Schriftgroesse.MITTEL, hoeheDp = 380f)
        val mittelBeamer = layoutMetrikFuer(LayoutKlasse.MITTEL, Schriftgroesse.GROSS)
        val breit = layoutMetrikFuer(LayoutKlasse.BREIT, Schriftgroesse.GROSS)

        assertEquals(2, kompakt.werteSpalten)
        assertFalse(kompakt.kopfNebeneinander)
        assertFalse(kompakt.optionenNebeneinander)
        assertFalse(kompakt.zweispaltigeBuehne)

        assertEquals(4, mittel.werteSpalten)
        assertTrue(mittel.kopfNebeneinander)
        assertTrue(mittel.optionenNebeneinander)
        assertTrue(mittel.zweispaltigeBuehne)
        assertFalse(mittel.kompakteHoehe)
        assertTrue(mittelSmartphoneQuer.kompakteHoehe)
        assertTrue(mittelSmartphoneQuer.zweispaltigeBuehne)
        assertTrue(mittelSmartphoneQuer.portraitGroesse <= mittel.portraitGroesse)
        assertFalse(mittelBeamer.optionenNebeneinander, "Bei Tablet + Beamer-Schrift werden Optionen gestapelt")

        assertEquals(4, breit.werteSpalten)
        assertTrue(breit.kopfNebeneinander)
        assertTrue(breit.optionenNebeneinander)
        assertTrue(breit.zweispaltigeBuehne)
        assertTrue(breit.maxInhaltsBreite > mittel.maxInhaltsBreite)
        assertTrue(mittel.maxInhaltsBreite > kompakt.maxInhaltsBreite)
        assertTrue(breit.segmentHoehe > mittel.segmentHoehe)

        listOf(kompakt, mittel, mittelSmartphoneQuer, mittelBeamer, breit).forEach { metrik ->
            assertTrue(metrik.minTouchHoehe >= 48.dp, "Touch-Mindesthöhe verletzt: $metrik")
        }
    }

    @Test
    fun ruhigeUebergaengeUndReduzierteAnimationenSindSauberKonfiguriert() {
        val ruhig = ArchivUebergaenge.profilFuer(reduzierteAnimationen = false)
        assertFalse(ruhig.reduzierteAnimationen)
        assertTrue(ruhig.phasenDauerMs in 120..300)
        assertTrue(ruhig.aufklappDauerMs in 100..250)
        assertTrue(ruhig.farbDauerMs in 100..260)
        assertTrue(ruhig.sanftScrollen)
        assertTrue(ruhig.vertikalAufklappen)

        val reduziert = ArchivUebergaenge.profilFuer(reduzierteAnimationen = true)
        assertTrue(reduziert.reduzierteAnimationen)
        assertEquals(0, reduziert.phasenDauerMs)
        assertEquals(0, reduziert.aufklappDauerMs)
        assertEquals(0, reduziert.farbDauerMs)
        assertFalse(reduziert.sanftScrollen)
        assertFalse(reduziert.vertikalAufklappen)

        // Auch die Compose-Übergangs-Fabriken laufen ohne Fehler
        ArchivUebergaenge.phasenTransitionSpec(false)
        ArchivUebergaenge.phasenTransitionSpec(true)
        ArchivUebergaenge.aufklappEnter(false)
        ArchivUebergaenge.aufklappEnter(true)
        ArchivUebergaenge.aufklappExit(false)
        ArchivUebergaenge.aufklappExit(true)
        ArchivUebergaenge.farbSpec(false)
        ArchivUebergaenge.farbSpec(true)
    }

    @Test
    fun archivFarbweltErfuelltWcagAAKontrasteFuerBeamerUndUnterricht() {
        val farben = ArchivFarben.fromFarbwelt(content.konfiguration.farbwelt)

        val pflichtPaare = listOf(
            "tinte auf papier" to (farben.tinte to farben.papier),
            "tinte auf papierHell" to (farben.tinte to farben.papierHell),
            "tinte auf papierDunkel" to (farben.tinte to farben.papierDunkel),
            "tinteMatt auf papier" to (farben.tinteMatt to farben.papier),
            "tinteMatt auf papierHell" to (farben.tinteMatt to farben.papierHell),
            "tinteMatt auf papierDunkel" to (farben.tinteMatt to farben.papierDunkel),
            "akzent auf papier" to (farben.akzent to farben.papier),
            "akzent auf papierHell" to (farben.akzent to farben.papierHell),
            "akzent auf papierDunkel" to (farben.akzent to farben.papierDunkel),
            "papierHell auf tinte" to (farben.papierHell to farben.tinte),
            "papierHell auf akzent" to (farben.papierHell to farben.akzent),
            "textHell auf dunkel" to (farben.textHell to farben.dunkel),
            "textHell auf dunkelHell" to (farben.textHell to farben.dunkelHell),
            "textHell@0.76 auf dunkelHell" to (farben.textHell.copy(alpha = 0.76f) to farben.dunkelHell),
        )

        pflichtPaare.forEach { (name, paar) ->
            val ratio = ArchivKontrast.kontrastVerhaeltnis(paar.first, paar.second)
            assertTrue(
                ArchivKontrast.erfuelltWcagAA(paar.first, paar.second),
                "WCAG AA (>= 4.5:1) verletzt für $name: $ratio",
            )
        }

        // Alle 5 Stufenfarben erfüllen WCAG AA auf hellem Papier (stufen) bzw. dunkler Kopfleiste (stufenHell)
        farben.stufen.forEachIndexed { stufe, farbe ->
            assertTrue(
                ArchivKontrast.erfuelltWcagAA(farbe, farben.papierHell),
                "Stufe $stufe verletzt WCAG AA auf papierHell",
            )
        }
        farben.stufenHell.forEachIndexed { stufe, farbe ->
            assertTrue(
                ArchivKontrast.erfuelltWcagAA(farbe, farben.dunkel),
                "Helle Stufe $stufe verletzt WCAG AA auf dunkel",
            )
            assertTrue(
                ArchivKontrast.erfuelltWcagAA(farbe, farben.dunkelHell),
                "Helle Stufe $stufe verletzt WCAG AA auf dunkelHell",
            )
        }
    }

    @Test
    fun anzeigeSkalierungVergroessertNurGrosseBildschirmeUndBleibtBegrenzt() {
        // Smartphones, kompakte Tablets & kleine Fenster: nie verkleinern
        assertEquals(1f, AnzeigeSkalierung.faktorFuer(915f, 412f))
        assertEquals(1f, AnzeigeSkalierung.faktorFuer(1080f, 810f))
        assertEquals(1f, AnzeigeSkalierung.faktorFuer(1366f, 650f))
        assertEquals(1f, AnzeigeSkalierung.faktorFuer(0f, 0f))
        assertEquals(1f, AnzeigeSkalierung.faktorFuer(Float.NaN, 900f))

        // Laptop mit 125 % Windows-Skalierung (ca. 1536 × 730): nur leicht größer
        assertEquals(1.05f, AnzeigeSkalierung.faktorFuer(1536f, 730f), 0.001f)
        // Full-HD-Browserfenster (ca. 1906 × 931): spürbar größer, begrenzt durch die Höhe
        assertEquals(1.35f, AnzeigeSkalierung.faktorFuer(1906f, 931f), 0.001f)
        // Großes Tablet im Querformat (iPad Pro 12,9″: 1366 × 1024)
        assertEquals(1.20f, AnzeigeSkalierung.faktorFuer(1366f, 1024f), 0.001f)
        // 10-Zoll-Android-Tablet im Querformat (1280 × 800 dp)
        assertEquals(1.10f, AnzeigeSkalierung.faktorFuer(1280f, 800f), 0.001f)
        // WQHD-Monitor (2560 × 1300) und 4K-Beamer: höchstens 1,75
        assertEquals(1.75f, AnzeigeSkalierung.faktorFuer(2560f, 1300f), 0.001f)
        assertEquals(AnzeigeSkalierung.MAX_FAKTOR, AnzeigeSkalierung.faktorFuer(3840f, 2000f))

        // Nach der Skalierung bleibt die Spielfläche mindestens so groß wie die Referenzfläche
        listOf(1366f to 1024f, 1906f to 931f, 2560f to 1300f).forEach { (b, h) ->
            val f = AnzeigeSkalierung.faktorFuer(b, h)
            assertTrue(b / f >= AnzeigeSkalierung.REFERENZ_BREITE_DP, "Breite nach Skalierung zu klein: $b/$f")
            assertTrue(h / f >= AnzeigeSkalierung.REFERENZ_HOEHE_DP, "Höhe nach Skalierung zu klein: $h/$f")
            assertEquals(LayoutKlasse.BREIT, LayoutKlasse.vonBreiteDp(b / f))
        }
    }
}
