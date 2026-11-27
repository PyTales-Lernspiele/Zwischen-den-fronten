package de.pytales.zdf.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

/**
 * Drei wählbare Schriftgrößen-Stufen für unterschiedliche Endgeräte und den Unterricht:
 * - [KLEIN]: kompakt für kleine Smartphone-Displays
 * - [MITTEL]: gut lesbarer Standard für Smartphone, Tablet, Desktop und Web
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
        beschreibung = "Kompakt für kleine Displays",
    ),
    MITTEL(
        code = "mittel",
        bezeichnung = "Mittel",
        kurzZeichen = "A",
        faktor = 1.00f,
        beschreibung = "Ruhiger Standard",
    ),
    GROSS(
        code = "gross",
        bezeichnung = "Groß",
        kurzZeichen = "A+",
        faktor = 1.24f,
        beschreibung = "Groß für Beamer & Unterricht",
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
 * Erzeugt die harmonische Buchdruck- & Archivpapier-Typografie für die gewählte [Schriftgroesse].
 *
 * Gestaltungsgrundsätze für Klasse 8 (13–14 Jahre) und Beamer:
 * - Warme Buchdruck-Serifen für Titel, Kapitelköpfe, Ausgänge und historische Zitate
 * - Ruhige, gut lesbare Leseschrift mit großzügigem Zeilenabstand (~1,45–1,52×) für Alltagstexte
 * - Zurückhaltende, fein gesperrte Auszeichnungen für Zeit- und Ortsangaben (ohne technischen Look)
 */
fun buildArchivTypography(
    groesse: Schriftgroesse,
    titelschrift: FontFamily = FontFamily.Serif,
): Typography {
    val f = groesse.faktor
    return Typography(
        displayLarge = TextStyle(
            fontFamily = titelschrift,
            fontWeight = FontWeight.Bold,
            fontSize = (34f * f).sp,
            lineHeight = (42f * f).sp,
            letterSpacing = (-0.25f).sp,
        ),
        displayMedium = TextStyle(
            fontFamily = titelschrift,
            fontWeight = FontWeight.Bold,
            fontSize = (29f * f).sp,
            lineHeight = (36f * f).sp,
            letterSpacing = (-0.15f).sp,
        ),
        displaySmall = TextStyle(
            fontFamily = titelschrift,
            fontWeight = FontWeight.Bold,
            fontSize = (25f * f).sp,
            lineHeight = (32f * f).sp,
        ),
        headlineLarge = TextStyle(
            fontFamily = titelschrift,
            fontWeight = FontWeight.Bold,
            fontSize = (23f * f).sp,
            lineHeight = (30f * f).sp,
        ),
        headlineMedium = TextStyle(
            fontFamily = titelschrift,
            fontWeight = FontWeight.Bold,
            fontSize = (20.5f * f).sp,
            lineHeight = (27.5f * f).sp,
        ),
        headlineSmall = TextStyle(
            fontFamily = titelschrift,
            fontWeight = FontWeight.SemiBold,
            fontSize = (18.5f * f).sp,
            lineHeight = (25f * f).sp,
        ),
        titleLarge = TextStyle(
            fontFamily = titelschrift,
            fontWeight = FontWeight.SemiBold,
            fontSize = (17.5f * f).sp,
            lineHeight = (24f * f).sp,
        ),
        titleMedium = TextStyle(
            fontFamily = titelschrift,
            fontWeight = FontWeight.SemiBold,
            fontSize = (15.5f * f).sp,
            lineHeight = (22f * f).sp,
            letterSpacing = 0.05.sp,
        ),
        titleSmall = TextStyle(
            fontFamily = titelschrift,
            fontWeight = FontWeight.SemiBold,
            fontSize = (14f * f).sp,
            lineHeight = (19.5f * f).sp,
            letterSpacing = 0.05.sp,
        ),
        bodyLarge = TextStyle(
            fontFamily = FontFamily.SansSerif,
            fontWeight = FontWeight.Normal,
            fontSize = (16.5f * f).sp,
            lineHeight = (24.5f * f).sp,
            letterSpacing = 0.1.sp,
        ),
        bodyMedium = TextStyle(
            fontFamily = FontFamily.SansSerif,
            fontWeight = FontWeight.Normal,
            fontSize = (14.5f * f).sp,
            lineHeight = (21f * f).sp,
            letterSpacing = 0.1.sp,
        ),
        bodySmall = TextStyle(
            fontFamily = FontFamily.SansSerif,
            fontWeight = FontWeight.Normal,
            fontSize = (13f * f).sp,
            lineHeight = (18.5f * f).sp,
            letterSpacing = 0.15.sp,
        ),
        labelLarge = TextStyle(
            fontFamily = FontFamily.SansSerif,
            fontWeight = FontWeight.SemiBold,
            fontSize = (13.5f * f).sp,
            lineHeight = (18.5f * f).sp,
            letterSpacing = 0.15.sp,
        ),
        labelMedium = TextStyle(
            fontFamily = FontFamily.SansSerif,
            fontWeight = FontWeight.Medium,
            fontSize = (12.5f * f).sp,
            lineHeight = (17f * f).sp,
            letterSpacing = 0.25.sp,
        ),
        labelSmall = TextStyle(
            fontFamily = FontFamily.SansSerif,
            fontWeight = FontWeight.Medium,
            fontSize = (11.5f * f).sp,
            lineHeight = (15.5f * f).sp,
            letterSpacing = 0.35.sp,
        ),
    )
}
