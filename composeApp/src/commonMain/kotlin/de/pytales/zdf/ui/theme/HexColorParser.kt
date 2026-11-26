package de.pytales.zdf.ui.theme

import androidx.compose.ui.graphics.Color

/**
 * Plattformübergreifender Parser für Hex-Farbangaben aus `content/konfiguration.json`
 * (`#RRGGBB` oder `#AARRGGBB`, optional ohne führendes `#`).
 */
object HexColorParser {

    /**
     * Parst einen Hex-Farbstring in einen 32-Bit-ARGB-Wert (`0xAARRGGBB`).
     *
     * @throws IllegalArgumentException wenn der String kein gültiger 6- oder 8-stelliger Hex-Farbwert ist.
     */
    fun parseArgb(hex: String): Long {
        val bereinigt = hex.trim().removePrefix("#")
        require(bereinigt.length == 6 || bereinigt.length == 8) {
            "Ungültiger Hex-Farbwert '$hex': erwartet 6 (RRGGBB) oder 8 (AARRGGBB) Hex-Zeichen."
        }
        require(bereinigt.all { it.isHexDigit() }) {
            "Ungültiger Hex-Farbwert '$hex': enthält ungültige Zeichen."
        }
        val wert = bereinigt.toLong(16)
        return if (bereinigt.length == 6) {
            0xFF000000L or wert
        } else {
            wert
        }
    }

    /**
     * Parst einen Hex-Farbstring direkt in eine Compose-[Color].
     */
    fun parseColor(hex: String): Color = Color(parseArgb(hex))

    /**
     * Parst einen Hex-Farbstring oder gibt bei ungültigem Wert [fallback] zurück.
     */
    fun parseColorOrDefault(hex: String, fallback: Color): Color =
        runCatching { parseColor(hex) }.getOrDefault(fallback)

    private fun Char.isHexDigit(): Boolean =
        this in '0'..'9' || this in 'a'..'f' || this in 'A'..'F'
}
