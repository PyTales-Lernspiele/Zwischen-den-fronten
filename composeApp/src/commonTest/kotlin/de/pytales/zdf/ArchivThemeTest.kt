package de.pytales.zdf

import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import de.pytales.zdf.ui.theme.ArchivFarben
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
        val mittelBeamer = layoutMetrikFuer(LayoutKlasse.MITTEL, Schriftgroesse.GROSS)
        val breit = layoutMetrikFuer(LayoutKlasse.BREIT, Schriftgroesse.GROSS)

        assertEquals(2, kompakt.werteSpalten)
        assertFalse(kompakt.kopfNebeneinander)
        assertFalse(kompakt.optionenNebeneinander)

        assertEquals(4, mittel.werteSpalten)
        assertTrue(mittel.kopfNebeneinander)
        assertTrue(mittel.optionenNebeneinander)
        assertFalse(mittelBeamer.optionenNebeneinander, "Bei Tablet + Beamer-Schrift werden Optionen gestapelt")

        assertEquals(4, breit.werteSpalten)
        assertTrue(breit.kopfNebeneinander)
        assertTrue(breit.optionenNebeneinander)
        assertTrue(breit.maxInhaltsBreite > mittel.maxInhaltsBreite)
        assertTrue(mittel.maxInhaltsBreite > kompakt.maxInhaltsBreite)
        assertTrue(breit.segmentHoehe > mittel.segmentHoehe)

        listOf(kompakt, mittel, mittelBeamer, breit).forEach { metrik ->
            assertTrue(metrik.minTouchHoehe >= 48.dp, "Touch-Mindesthöhe verletzt: $metrik")
        }
    }
}
