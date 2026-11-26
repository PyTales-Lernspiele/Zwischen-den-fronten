package de.pytales.zdf.ui.theme

import androidx.compose.runtime.Immutable
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

/**
 * Responsive Layout-Klassen für alle drei Zielplattformen:
 * - [KOMPAKT]: Android-Hochformat / schmale Fenster (< 600 dp)
 * - [MITTEL]: Tablets / mittelgroße Querformat-Fenster (600 bis < 960 dp)
 * - [BREIT]: Desktop, WebApp im Querformat und Beamer (>= 960 dp)
 */
enum class LayoutKlasse(
    val code: String,
    val bezeichnung: String,
) {
    KOMPAKT("kompakt", "Kompakt"),
    MITTEL("mittel", "Mittel"),
    BREIT("breit", "Breit");

    companion object {
        const val BREAKPOINT_MITTEL_DP: Float = 600f
        const val BREAKPOINT_BREIT_DP: Float = 960f

        fun vonBreiteDp(breiteDp: Float): LayoutKlasse = when {
            breiteDp < BREAKPOINT_MITTEL_DP -> KOMPAKT
            breiteDp < BREAKPOINT_BREIT_DP -> MITTEL
            else -> BREIT
        }

        fun vonBreite(breite: Dp): LayoutKlasse = vonBreiteDp(breite.value)
    }
}

/**
 * Abgeleitete Abstände, Spaltenzahlen und Touch-Mindestgrößen für die aktuelle [LayoutKlasse]
 * und [Schriftgroesse].
 */
@Immutable
data class LayoutMetrik(
    val klasse: LayoutKlasse,
    val aussenAbstand: Dp,
    val elementAbstand: Dp,
    val kartenInnenAbstand: Dp,
    val maxInhaltsBreite: Dp,
    val werteSpalten: Int,
    val kopfNebeneinander: Boolean,
    val optionenNebeneinander: Boolean,
    val portraitGroesse: Dp,
    val segmentHoehe: Dp,
    val minTouchHoehe: Dp,
)

/**
 * Berechnet konsistente Layout-Metriken für eine Kombination aus [LayoutKlasse] und [Schriftgroesse].
 */
fun layoutMetrikFuer(
    klasse: LayoutKlasse,
    schriftgroesse: Schriftgroesse = Schriftgroesse.MITTEL,
): LayoutMetrik {
    val segmentHoehe = when (schriftgroesse) {
        Schriftgroesse.KLEIN -> 7.dp
        Schriftgroesse.MITTEL -> 8.dp
        Schriftgroesse.GROSS -> 10.dp
    }
    return when (klasse) {
        LayoutKlasse.KOMPAKT -> LayoutMetrik(
            klasse = klasse,
            aussenAbstand = 12.dp,
            elementAbstand = 10.dp,
            kartenInnenAbstand = 14.dp,
            maxInhaltsBreite = 600.dp,
            werteSpalten = 2,
            kopfNebeneinander = false,
            optionenNebeneinander = false,
            portraitGroesse = 52.dp,
            segmentHoehe = segmentHoehe,
            minTouchHoehe = 48.dp,
        )

        LayoutKlasse.MITTEL -> LayoutMetrik(
            klasse = klasse,
            aussenAbstand = 20.dp,
            elementAbstand = 14.dp,
            kartenInnenAbstand = 18.dp,
            maxInhaltsBreite = 880.dp,
            werteSpalten = 4,
            kopfNebeneinander = true,
            optionenNebeneinander = schriftgroesse != Schriftgroesse.GROSS,
            portraitGroesse = 64.dp,
            segmentHoehe = segmentHoehe,
            minTouchHoehe = 48.dp,
        )

        LayoutKlasse.BREIT -> LayoutMetrik(
            klasse = klasse,
            aussenAbstand = 28.dp,
            elementAbstand = 18.dp,
            kartenInnenAbstand = 24.dp,
            maxInhaltsBreite = 1120.dp,
            werteSpalten = 4,
            kopfNebeneinander = true,
            optionenNebeneinander = true,
            portraitGroesse = 74.dp,
            segmentHoehe = segmentHoehe,
            minTouchHoehe = 48.dp,
        )
    }
}
