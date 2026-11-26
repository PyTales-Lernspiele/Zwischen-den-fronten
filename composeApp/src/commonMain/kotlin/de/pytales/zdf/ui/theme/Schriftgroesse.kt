package de.pytales.zdf.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

/**
 * Drei wählbare Schriftgrößen-Stufen für unterschiedliche Endgeräte und den Unterricht:
 * - [KLEIN]: kompakt für kleinere Smartphone-Bildschirme
 * - [MITTEL]: gut lesbarer Standard für Tablet, Desktop und Web
 * - [GROSS]: Beamer- und Klassenzimmertauglichkeit (gut lesbar aus der letzten Reihe)
 */
enum class Schriftgroesse(
    val code: String,
    val bezeichnung: String,
    val kurzZeichen: String,
    val faktor: Float,
    val beschreibung: String,
) {
    KLEIN(
        code = "klein",
        bezeichnung = "Klein",
        kurzZeichen = "A-",
        faktor = 0.88f,
        beschreibung = "Kompakt für kleine Bildschirme",
    ),
    MITTEL(
        code = "mittel",
        bezeichnung = "Mittel",
        kurzZeichen = "A",
        faktor = 1.00f,
        beschreibung = "Standard für Tablet & Desktop",
    ),
    GROSS(
        code = "gross",
        bezeichnung = "Groß",
        kurzZeichen = "A+",
        faktor = 1.24f,
        beschreibung = "Beamer & Unterricht (hohe Lesbarkeit)",
    );

    fun naechste(): Schriftgroesse = when (this) {
        KLEIN -> MITTEL
        MITTEL -> GROSS
        GROSS -> GROSS
    }

    fun vorherige(): Schriftgroesse = when (this) {
        KLEIN -> KLEIN
        MITTEL -> KLEIN
        GROSS -> MITTEL
    }

    companion object {
        fun fromCode(code: String?): Schriftgroesse =
            entries.firstOrNull { it.code.equals(code?.trim(), ignoreCase = true) } ?: MITTEL
    }
}

/**
 * Erzeugt die Archivpapier-Typografie für die gewählte [Schriftgroesse].
 *
 * Gestaltungsgrundsätze für Klasse 8 (13–14 Jahre) und Beamer:
 * - Historische Serifen für Kapitel-, Dokument- und Zeitungstitel
 * - Klare, serifenlose Schrift mit großzügigem Zeilenabstand (~1,45–1,55×) für Fließtext
 * - Monospace für Aktenzeichen, Stempel-Codes, Änderungs-Badges und Medien-IDs
 */
fun buildArchivTypography(groesse: Schriftgroesse): Typography {
    val f = groesse.faktor
    return Typography(
        displayLarge = TextStyle(
            fontFamily = FontFamily.Serif,
            fontWeight = FontWeight.Bold,
            fontSize = (34f * f).sp,
            lineHeight = (42f * f).sp,
            letterSpacing = (-0.25f).sp,
        ),
        displayMedium = TextStyle(
            fontFamily = FontFamily.Serif,
            fontWeight = FontWeight.Bold,
            fontSize = (30f * f).sp,
            lineHeight = (38f * f).sp,
        ),
        displaySmall = TextStyle(
            fontFamily = FontFamily.Serif,
            fontWeight = FontWeight.Bold,
            fontSize = (26f * f).sp,
            lineHeight = (34f * f).sp,
        ),
        headlineLarge = TextStyle(
            fontFamily = FontFamily.Serif,
            fontWeight = FontWeight.Bold,
            fontSize = (24f * f).sp,
            lineHeight = (32f * f).sp,
        ),
        headlineMedium = TextStyle(
            fontFamily = FontFamily.Serif,
            fontWeight = FontWeight.Bold,
            fontSize = (21f * f).sp,
            lineHeight = (29f * f).sp,
        ),
        headlineSmall = TextStyle(
            fontFamily = FontFamily.Serif,
            fontWeight = FontWeight.SemiBold,
            fontSize = (19f * f).sp,
            lineHeight = (26f * f).sp,
        ),
        titleLarge = TextStyle(
            fontFamily = FontFamily.Serif,
            fontWeight = FontWeight.SemiBold,
            fontSize = (18f * f).sp,
            lineHeight = (25f * f).sp,
        ),
        titleMedium = TextStyle(
            fontFamily = FontFamily.SansSerif,
            fontWeight = FontWeight.SemiBold,
            fontSize = (16f * f).sp,
            lineHeight = (23f * f).sp,
            letterSpacing = 0.1.sp,
        ),
        titleSmall = TextStyle(
            fontFamily = FontFamily.SansSerif,
            fontWeight = FontWeight.SemiBold,
            fontSize = (14.5f * f).sp,
            lineHeight = (20.5f * f).sp,
            letterSpacing = 0.1.sp,
        ),
        bodyLarge = TextStyle(
            fontFamily = FontFamily.SansSerif,
            fontWeight = FontWeight.Normal,
            fontSize = (16.5f * f).sp,
            lineHeight = (25f * f).sp,
            letterSpacing = 0.15.sp,
        ),
        bodyMedium = TextStyle(
            fontFamily = FontFamily.SansSerif,
            fontWeight = FontWeight.Normal,
            fontSize = (14.5f * f).sp,
            lineHeight = (21.5f * f).sp,
            letterSpacing = 0.15.sp,
        ),
        bodySmall = TextStyle(
            fontFamily = FontFamily.SansSerif,
            fontWeight = FontWeight.Normal,
            fontSize = (13f * f).sp,
            lineHeight = (19f * f).sp,
            letterSpacing = 0.2.sp,
        ),
        labelLarge = TextStyle(
            fontFamily = FontFamily.SansSerif,
            fontWeight = FontWeight.SemiBold,
            fontSize = (14f * f).sp,
            lineHeight = (19.5f * f).sp,
            letterSpacing = 0.2.sp,
        ),
        labelMedium = TextStyle(
            fontFamily = FontFamily.SansSerif,
            fontWeight = FontWeight.Medium,
            fontSize = (12.5f * f).sp,
            lineHeight = (17.5f * f).sp,
            letterSpacing = 0.4.sp,
        ),
        labelSmall = TextStyle(
            fontFamily = FontFamily.Monospace,
            fontWeight = FontWeight.Medium,
            fontSize = (11.5f * f).sp,
            lineHeight = (16f * f).sp,
            letterSpacing = 0.4.sp,
        ),
    )
}
