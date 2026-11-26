package de.pytales.zdf.ui.theme

import androidx.compose.material3.ColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Immutable
import androidx.compose.ui.graphics.Color
import de.pytales.zdf.model.Farbwelt

/**
 * Vollständige Archivpapier-Farbpalette, abgeleitet aus `farbwelt` in `content/konfiguration.json`.
 *
 * Helle Archivflächen (`papier`, `papierHell`, `papierDunkel`) tragen die Erzähl- und
 * Entscheidungskarten mit hoher Kontrastschärfe (`tinte` auf `papier` > 14:1).
 * Die dunkle Kopfleiste (`dunkel`, `dunkelHell`) verankert Befindensleiste und
 * Live-Emotions-Kachel mit hellen Stufenfarben (`stufenHell`) für gute Beamer-Lesbarkeit.
 */
@Immutable
data class ArchivFarben(
    val papier: Color,
    val papierHell: Color,
    val papierDunkel: Color,
    val tinte: Color,
    val tinteMatt: Color,
    val linie: Color,
    val linieFein: Color,
    val akzent: Color,
    val akzentMatt: Color,
    val dunkel: Color,
    val dunkelHell: Color,
    val segmentLeer: Color,
    val segmentDunkel: Color,
    val textHell: Color,
    val stufen: List<Color>,
    val stufenHell: List<Color>,
) {
    init {
        require(stufen.isNotEmpty()) { "stufen darf nicht leer sein." }
        require(stufenHell.isNotEmpty()) { "stufenHell darf nicht leer sein." }
    }

    /**
     * Stufenfarbe (0 = gut .. 4 = kritisch) für helle Archivpapier-Flächen.
     */
    fun stufenFarbe(stufe: Int): Color = stufen[stufe.coerceIn(0, stufen.lastIndex)]

    /**
     * Helle Stufenfarbe (0 = gut .. 4 = kritisch) für dunkle Kopfleisten-Flächen.
     */
    fun stufenFarbeHell(stufe: Int): Color = stufenHell[stufe.coerceIn(0, stufenHell.lastIndex)]

    /**
     * Kontraststarke Signalfarbe für Werteänderungen (`+1`/`-1` in Anzeigelogik).
     */
    fun deltaFarbe(schlechter: Boolean, aufDunkel: Boolean): Color {
        val index = if (schlechter) stufen.lastIndex else 0
        return if (aufDunkel) stufenFarbeHell(index) else stufenFarbe(index)
    }

    /**
     * Bildet die Archiv-Palette auf ein konsistentes Material-3-[ColorScheme] ab.
     */
    fun toMaterialColorScheme(): ColorScheme = lightColorScheme(
        primary = akzent,
        onPrimary = papierHell,
        primaryContainer = papierDunkel,
        onPrimaryContainer = tinte,
        secondary = tinteMatt,
        onSecondary = papierHell,
        secondaryContainer = papierDunkel,
        onSecondaryContainer = tinte,
        tertiary = stufenFarbe(0),
        onTertiary = papierHell,
        tertiaryContainer = papierDunkel,
        onTertiaryContainer = tinte,
        background = papier,
        onBackground = tinte,
        surface = papierHell,
        onSurface = tinte,
        surfaceVariant = papierDunkel,
        onSurfaceVariant = tinteMatt,
        surfaceContainerLowest = papierHell,
        surfaceContainerLow = papier,
        surfaceContainer = papier,
        surfaceContainerHigh = papierDunkel,
        surfaceContainerHighest = segmentLeer,
        outline = linie,
        outlineVariant = linieFein,
        error = stufenFarbe(4),
        onError = papierHell,
        errorContainer = papierDunkel,
        onErrorContainer = stufenFarbe(4),
        inverseSurface = dunkel,
        inverseOnSurface = textHell,
        inversePrimary = akzentMatt,
        scrim = dunkel,
    )

    companion object {
        /**
         * Baut [ArchivFarben] direkt aus dem deserialisierten [Farbwelt]-Block von `content/konfiguration.json`.
         */
        fun fromFarbwelt(farbwelt: Farbwelt): ArchivFarben {
            require(farbwelt.stufen.isNotEmpty()) { "farbwelt.stufen darf nicht leer sein." }
            require(farbwelt.stufenHell.isNotEmpty()) { "farbwelt.stufenHell darf nicht leer sein." }
            return ArchivFarben(
                papier = HexColorParser.parseColor(farbwelt.papier),
                papierHell = HexColorParser.parseColor(farbwelt.papierHell),
                papierDunkel = HexColorParser.parseColor(farbwelt.papierDunkel),
                tinte = HexColorParser.parseColor(farbwelt.tinte),
                tinteMatt = HexColorParser.parseColor(farbwelt.tinteMatt),
                linie = HexColorParser.parseColor(farbwelt.linie),
                linieFein = HexColorParser.parseColor(farbwelt.linieFein),
                akzent = HexColorParser.parseColor(farbwelt.akzent),
                akzentMatt = HexColorParser.parseColor(farbwelt.akzentMatt),
                dunkel = HexColorParser.parseColor(farbwelt.dunkel),
                dunkelHell = HexColorParser.parseColor(farbwelt.dunkelHell),
                segmentLeer = HexColorParser.parseColor(farbwelt.segmentLeer),
                segmentDunkel = HexColorParser.parseColor(farbwelt.segmentDunkel),
                textHell = HexColorParser.parseColor(farbwelt.textHell),
                stufen = farbwelt.stufen.map(HexColorParser::parseColor),
                stufenHell = farbwelt.stufenHell.map(HexColorParser::parseColor),
            )
        }

        /**
         * Synchroner Fallback für die Ladeansicht (identisch zu `content/konfiguration.json`).
         */
        fun default(): ArchivFarben = ArchivFarben(
            papier = Color(0xFFEFE9DC),
            papierHell = Color(0xFFF7F3EA),
            papierDunkel = Color(0xFFE2DBCA),
            tinte = Color(0xFF1F1C18),
            tinteMatt = Color(0xFF57514A),
            linie = Color(0xFF8D8578),
            linieFein = Color(0xFFB6AE9E),
            akzent = Color(0xFF8A3324),
            akzentMatt = Color(0xFFA85C4A),
            dunkel = Color(0xFF15130F),
            dunkelHell = Color(0xFF241F19),
            segmentLeer = Color(0xFFCFC7B6),
            segmentDunkel = Color(0xFF39332B),
            textHell = Color(0xFFDED7C9),
            stufen = listOf(
                Color(0xFF3F5B3A),
                Color(0xFF6D6A3A),
                Color(0xFF8A6A2C),
                Color(0xFF8F4A20),
                Color(0xFF7C1D14),
            ),
            stufenHell = listOf(
                Color(0xFF8BB07F),
                Color(0xFFC0B871),
                Color(0xFFD3A75C),
                Color(0xFFDC8B5F),
                Color(0xFFD76A5E),
            ),
        )
    }
}
