package de.pytales.zdf.ui.theme

import androidx.compose.runtime.Immutable
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

/**
 * Responsive Layout-Klassen für alle drei Zielplattformen:
 * - [KOMPAKT]: Schmale Fenster (< 600 dp)
 * - [MITTEL]: Smartphones im Querformat (ca. 720–930 × 360–430 dp) & kompakte Tablets (600 bis < 960 dp)
 * - [BREIT]: Schul-Tablets im Querformat, Desktop, WebApp und Beamer (>= 960 dp)
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

        /** Schwelle unterhalb derer ein Querformat-Display als flach gilt (Smartphone-Querformat). */
        const val SCHWELLE_FLACHE_HOEHE_DP: Float = 500f

        fun vonBreiteDp(breiteDp: Float): LayoutKlasse = when {
            breiteDp < BREAKPOINT_MITTEL_DP -> KOMPAKT
            breiteDp < BREAKPOINT_BREIT_DP -> MITTEL
            else -> BREIT
        }

        fun vonBreite(breite: Dp): LayoutKlasse = vonBreiteDp(breite.value)
    }
}

/**
 * Automatische Anzeige-Skalierung für große Bildschirme (PC-Monitore, Beamer, große Tablets).
 *
 * Bezugsgröße ist eine Spielfläche von [REFERENZ_BREITE_DP] × [REFERENZ_HOEHE_DP]. Ist das Fenster in
 * beiden Richtungen größer, wächst die gesamte Oberfläche (Schrift, Abstände, Bilder) gleichmäßig mit,
 * statt in einer kleinen Insel in der Bildschirmmitte zu bleiben. Weil Compose dabei in voller
 * Auflösung neu zeichnet, bleibt alles gestochen scharf – anders als beim Browser-Zoom.
 *
 * Kleinere Fenster (Smartphones, kompakte Tablets) werden nie verkleinert (Faktor 1).
 */
object AnzeigeSkalierung {
    const val REFERENZ_BREITE_DP: Float = 1120f
    const val REFERENZ_HOEHE_DP: Float = 680f
    const val MAX_FAKTOR: Float = 1.75f

    /** Schrittweite, damit kleine Fensteränderungen nicht ständig neu skalieren. */
    private const val SCHRITTE_JE_EINHEIT: Float = 20f

    fun faktorFuer(breiteDp: Float, hoeheDp: Float): Float {
        if (breiteDp.isNaN() || hoeheDp.isNaN() || breiteDp <= 0f || hoeheDp <= 0f) return 1f
        val roh = minOf(breiteDp / REFERENZ_BREITE_DP, hoeheDp / REFERENZ_HOEHE_DP)
        val abgerundet = kotlin.math.floor(roh * SCHRITTE_JE_EINHEIT) / SCHRITTE_JE_EINHEIT
        return abgerundet.coerceIn(1f, MAX_FAKTOR)
    }
}

/**
 * Abgeleitete Abstände, Spaltenzahlen und Touch-Mindestgrößen für die aktuelle [LayoutKlasse],
 * [Schriftgroesse] und Bildschirmhöhe (optimiert für breite, aber flache Querformat-Displays).
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
    val zweispaltigeBuehne: Boolean,
    val kompakteHoehe: Boolean,
    val portraitGroesse: Dp,
    val segmentHoehe: Dp,
    val minTouchHoehe: Dp,
)

/**
 * Berechnet konsistente, Landscape-First-optimierte Layout-Metriken für eine Kombination aus
 * [LayoutKlasse], [Schriftgroesse] und optionaler verfügbarer Bildschirmhöhe ([hoeheDp]).
 */
fun layoutMetrikFuer(
    klasse: LayoutKlasse,
    schriftgroesse: Schriftgroesse = Schriftgroesse.MITTEL,
    hoeheDp: Float? = null,
): LayoutMetrik {
    val flacheHoehe = hoeheDp != null && hoeheDp < LayoutKlasse.SCHWELLE_FLACHE_HOEHE_DP
    val segmentHoehe = when (schriftgroesse) {
        Schriftgroesse.KLEIN -> 6.dp
        Schriftgroesse.MITTEL -> if (flacheHoehe) 6.dp else 7.dp
        Schriftgroesse.GROSS -> 9.dp
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
            zweispaltigeBuehne = false,
            kompakteHoehe = flacheHoehe,
            portraitGroesse = 44.dp,
            segmentHoehe = segmentHoehe,
            minTouchHoehe = 48.dp,
        )

        LayoutKlasse.MITTEL -> LayoutMetrik(
            klasse = klasse,
            aussenAbstand = if (flacheHoehe) 12.dp else 18.dp,
            elementAbstand = if (flacheHoehe) 10.dp else 14.dp,
            kartenInnenAbstand = if (flacheHoehe) 14.dp else 18.dp,
            maxInhaltsBreite = 940.dp,
            werteSpalten = 4,
            kopfNebeneinander = true,
            optionenNebeneinander = schriftgroesse != Schriftgroesse.GROSS,
            zweispaltigeBuehne = true,
            kompakteHoehe = flacheHoehe,
            portraitGroesse = if (flacheHoehe) 42.dp else 48.dp,
            segmentHoehe = segmentHoehe,
            minTouchHoehe = 48.dp,
        )

        LayoutKlasse.BREIT -> LayoutMetrik(
            klasse = klasse,
            aussenAbstand = if (flacheHoehe) 16.dp else 28.dp,
            elementAbstand = if (flacheHoehe) 12.dp else 18.dp,
            kartenInnenAbstand = if (flacheHoehe) 16.dp else 22.dp,
            maxInhaltsBreite = 1160.dp,
            werteSpalten = 4,
            kopfNebeneinander = true,
            optionenNebeneinander = true,
            zweispaltigeBuehne = true,
            kompakteHoehe = flacheHoehe,
            portraitGroesse = if (flacheHoehe) 44.dp else 52.dp,
            segmentHoehe = segmentHoehe,
            minTouchHoehe = 48.dp,
        )
    }
}
