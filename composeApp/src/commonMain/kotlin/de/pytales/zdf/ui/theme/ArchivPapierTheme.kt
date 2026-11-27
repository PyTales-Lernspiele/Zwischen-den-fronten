package de.pytales.zdf.ui.theme

import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Shapes
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.ReadOnlyComposable
import androidx.compose.runtime.remember
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Density
import androidx.compose.ui.unit.dp
import de.pytales.zdf.model.Farbwelt
import de.pytales.zdf.resources.Res
import de.pytales.zdf.resources.spectral_semibold
import org.jetbrains.compose.resources.Font

val LocalArchivFarben = staticCompositionLocalOf { ArchivFarben.default() }
val LocalSchriftgroesse = staticCompositionLocalOf { Schriftgroesse.MITTEL }
val LocalLayoutKlasse = staticCompositionLocalOf { LayoutKlasse.BREIT }
val LocalLayoutMetrik = staticCompositionLocalOf {
    layoutMetrikFuer(LayoutKlasse.BREIT, Schriftgroesse.MITTEL)
}
val LocalReduzierteAnimationen = staticCompositionLocalOf { false }

/**
 * Ruhige, kantige Archiv-Formen (Papierbögen, Stempel, Aktenblätter statt runder Spiel-Pills).
 */
val ArchivShapes = Shapes(
    extraSmall = RoundedCornerShape(3.dp),
    small = RoundedCornerShape(5.dp),
    medium = RoundedCornerShape(6.dp),
    large = RoundedCornerShape(8.dp),
    extraLarge = RoundedCornerShape(10.dp),
)

/**
 * Zentraler Zugriffspunkt auf Farben, Schriftgröße, Animationsmodus und responsive Layout-Metriken im Theme.
 */
object ArchivTheme {
    val farben: ArchivFarben
        @Composable
        @ReadOnlyComposable
        get() = LocalArchivFarben.current

    val schriftgroesse: Schriftgroesse
        @Composable
        @ReadOnlyComposable
        get() = LocalSchriftgroesse.current

    val layoutKlasse: LayoutKlasse
        @Composable
        @ReadOnlyComposable
        get() = LocalLayoutKlasse.current

    val metrik: LayoutMetrik
        @Composable
        @ReadOnlyComposable
        get() = LocalLayoutMetrik.current

    val reduzierteAnimationen: Boolean
        @Composable
        @ReadOnlyComposable
        get() = LocalReduzierteAnimationen.current
}

/**
 * Material-3- und Custom-Theme für „Zwischen den Fronten“ in Archivpapier-Optik.
 *
 * - Übernimmt die Farbwelt direkt aus `content/konfiguration.json` (Fallback bis geladen).
 * - Skaliert die gesamte Typografie über die 3 Stufen [Schriftgroesse.KLEIN], [Schriftgroesse.MITTEL]
 *   und [Schriftgroesse.GROSS] (Beamer-Modus).
 * - Steuert ruhige Übergänge bzw. reduzierte Animationen zentral über [reduzierteAnimationen].
 * - Erkennt die [LayoutKlasse] und Querformat-Höhe automatisch anhand der verfügbaren Fenstergröße,
 *   sofern kein explizites [layoutKlasseOverride] gesetzt wird.
 */
@Composable
fun ArchivPapierTheme(
    farbwelt: Farbwelt? = null,
    schriftgroesse: Schriftgroesse = Schriftgroesse.MITTEL,
    reduzierteAnimationen: Boolean = false,
    layoutKlasseOverride: LayoutKlasse? = null,
    content: @Composable () -> Unit,
) {
    val farben = remember(farbwelt) {
        if (farbwelt != null) ArchivFarben.fromFarbwelt(farbwelt) else ArchivFarben.default()
    }
    val colorScheme = remember(farben) { farben.toMaterialColorScheme() }
    val titelfont = Font(Res.font.spectral_semibold, weight = FontWeight.SemiBold)
    val typography = remember(schriftgroesse, titelfont) {
        buildArchivTypography(schriftgroesse, FontFamily(titelfont))
    }

    if (layoutKlasseOverride != null) {
        val metrik = remember(layoutKlasseOverride, schriftgroesse) {
            layoutMetrikFuer(layoutKlasseOverride, schriftgroesse)
        }
        CompositionLocalProvider(
            LocalArchivFarben provides farben,
            LocalSchriftgroesse provides schriftgroesse,
            LocalLayoutKlasse provides layoutKlasseOverride,
            LocalLayoutMetrik provides metrik,
            LocalReduzierteAnimationen provides reduzierteAnimationen,
        ) {
            MaterialTheme(
                colorScheme = colorScheme,
                typography = typography,
                shapes = ArchivShapes,
                content = content,
            )
        }
    } else {
        BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
            // Große Bildschirme: gesamte Oberfläche gleichmäßig und scharf vergrößern
            val basisDichte = LocalDensity.current
            val skalierung = AnzeigeSkalierung.faktorFuer(maxWidth.value, maxHeight.value)
            val dichte = remember(basisDichte, skalierung) {
                Density(density = basisDichte.density * skalierung, fontScale = basisDichte.fontScale)
            }
            PlattformAnzeigeSkalierung(skalierung)
            val breiteDp = maxWidth.value / skalierung
            val hoeheDp = maxHeight.value / skalierung
            val ermittelteKlasse = LayoutKlasse.vonBreiteDp(breiteDp)
            val metrik = remember(ermittelteKlasse, schriftgroesse, hoeheDp) {
                layoutMetrikFuer(ermittelteKlasse, schriftgroesse, hoeheDp = hoeheDp)
            }
            CompositionLocalProvider(
                LocalDensity provides dichte,
                LocalArchivFarben provides farben,
                LocalSchriftgroesse provides schriftgroesse,
                LocalLayoutKlasse provides ermittelteKlasse,
                LocalLayoutMetrik provides metrik,
                LocalReduzierteAnimationen provides reduzierteAnimationen,
            ) {
                MaterialTheme(
                    colorScheme = colorScheme,
                    typography = typography,
                    shapes = ArchivShapes,
                    content = content,
                )
            }
        }
    }
}
