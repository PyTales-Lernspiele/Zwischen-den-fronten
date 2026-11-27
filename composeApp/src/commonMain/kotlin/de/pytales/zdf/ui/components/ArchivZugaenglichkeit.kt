package de.pytales.zdf.ui.components

import androidx.compose.foundation.border
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.input.key.Key
import androidx.compose.ui.input.key.KeyEventType
import androidx.compose.ui.input.key.key
import androidx.compose.ui.input.key.onPreviewKeyEvent
import androidx.compose.ui.input.key.type
import androidx.compose.ui.input.pointer.PointerIcon
import androidx.compose.ui.input.pointer.pointerHoverIcon
import androidx.compose.ui.semantics.LiveRegionMode
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.isTraversalGroup
import androidx.compose.ui.semantics.liveRegion
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import de.pytales.zdf.ui.theme.ArchivTheme

/**
 * Zeichnet bei Tastaturfokus (Desktop/Web) einen klar sichtbaren, kontrastreichen
 * Archiv-Fokusrahmen (`2.5 dp`) um bedienbare Schaltflächen und Auswahlkarten.
 * Mit der Maus (PC/Web) zeigt der Zeiger über diesen Elementen zusätzlich die Hand.
 *
 * Wichtig: In der Modifier-Kette **vor** `.clickable(...)` einfügen, damit `onFocusChanged`
 * den von `clickable` erzeugten Fokus-Knoten beobachtet.
 */
@Composable
fun Modifier.archivFokusRahmen(
    eckRadius: Dp = 4.dp,
    aufDunkel: Boolean = false,
): Modifier {
    var fokussiert by remember { mutableStateOf(false) }
    val farben = ArchivTheme.farben
    val fokusFarbe = if (aufDunkel) farben.stufenFarbeHell(2) else farben.akzent
    return this
        .pointerHoverIcon(PointerIcon.Hand)
        .onFocusChanged { state -> fokussiert = state.isFocused }
        .then(
            if (fokussiert) {
                Modifier.border(2.5.dp, fokusFarbe, RoundedCornerShape(eckRadius))
            } else {
                Modifier
            },
        )
}

/**
 * Kennzeichnet eine Überschrift semantisch für Screenreader-Navigation.
 */
fun Modifier.archivUeberschrift(): Modifier = this.semantics {
    heading()
}

/**
 * Kennzeichnet einen dynamisch aktualisierten Hinweis- oder Ausgangsbereich als höfliche
 * Live-Region für Bildschirmleser.
 */
fun Modifier.archivLiveHinweis(): Modifier = this.semantics {
    liveRegion = LiveRegionMode.Polite
}

/**
 * Gruppiert zusammengehörige Bereiche für eine klare Tab-/Screenreader-Reihenfolge.
 */
fun Modifier.archivFokusGruppe(): Modifier = this.semantics {
    isTraversalGroup = true
}

/**
 * Ermöglicht auf Desktop und Web das ruhige Schließen aufgeklappter Erklär- oder Detailkarten
 * über die Escape-Taste.
 */
fun Modifier.archivEscapeAktion(
    aktiv: Boolean,
    onEscape: () -> Unit,
): Modifier = if (!aktiv) {
    this
} else {
    this.onPreviewKeyEvent { event ->
        if (event.type == KeyEventType.KeyDown && event.key == Key.Escape) {
            onEscape()
            true
        } else {
            false
        }
    }
}
