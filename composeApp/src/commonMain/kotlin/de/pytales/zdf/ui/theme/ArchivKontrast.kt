package de.pytales.zdf.ui.theme

import androidx.compose.ui.graphics.Color
import kotlin.math.max
import kotlin.math.min
import kotlin.math.pow

/**
 * WCAG-2.1-Kontrastberechnung für die Archivpapier-Farbwelt (Beamer- und Klassenzimmertauglichkeit).
 */
object ArchivKontrast {

    const val SCHWELLE_AA_NORMAL: Double = 4.5
    const val SCHWELLE_AA_GROSS: Double = 3.0
    const val SCHWELLE_AAA_NORMAL: Double = 7.0

    /**
     * Berechnet die relative Leuchtdichte einer sRGB-Farbe gemäß WCAG 2.1 (0.0 = Schwarz, 1.0 = Weiß).
     */
    fun relativeLuminanz(farbe: Color): Double {
        val r = linearisiereKanal(farbe.red.toDouble())
        val g = linearisiereKanal(farbe.green.toDouble())
        val b = linearisiereKanal(farbe.blue.toDouble())
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    }

    /**
     * Mischt eine teiltransparente Vordergrundfarbe deckend auf einen Hintergrund,
     * bevor der reale Lesekontrast berechnet wird.
     */
    fun aufHintergrund(vordergrund: Color, hintergrund: Color): Color {
        val a = vordergrund.alpha.coerceIn(0f, 1f)
        if (a >= 1f) return vordergrund
        val inv = 1f - a
        return Color(
            red = vordergrund.red * a + hintergrund.red * inv,
            green = vordergrund.green * a + hintergrund.green * inv,
            blue = vordergrund.blue * a + hintergrund.blue * inv,
            alpha = 1f,
        )
    }

    /**
     * Berechnet das Kontrastverhältnis (`1.0` bis `21.0`) zwischen Vorder- und Hintergrundfarbe.
     */
    fun kontrastVerhaeltnis(vordergrund: Color, hintergrund: Color): Double {
        val effektivVorder = aufHintergrund(vordergrund, hintergrund)
        val l1 = relativeLuminanz(effektivVorder)
        val l2 = relativeLuminanz(hintergrund)
        val hell = max(l1, l2)
        val dunkel = min(l1, l2)
        return (hell + 0.05) / (dunkel + 0.05)
    }

    fun erfuelltWcagAA(
        vordergrund: Color,
        hintergrund: Color,
        grosseSchrift: Boolean = false,
    ): Boolean {
        val schwelle = if (grosseSchrift) SCHWELLE_AA_GROSS else SCHWELLE_AA_NORMAL
        return kontrastVerhaeltnis(vordergrund, hintergrund) >= schwelle
    }

    private fun linearisiereKanal(wert: Double): Double {
        val begrenzt = wert.coerceIn(0.0, 1.0)
        return if (begrenzt <= 0.03928) {
            begrenzt / 12.92
        } else {
            ((begrenzt + 0.055) / 1.055).pow(2.4)
        }
    }
}
