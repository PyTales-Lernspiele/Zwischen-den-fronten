package de.pytales.zdf.ui.components

import androidx.activity.compose.BackHandler
import androidx.compose.runtime.Composable

@Composable
actual fun PlattformZurueckHandler(
    aktiv: Boolean,
    onZurueck: () -> Unit,
) {
    BackHandler(enabled = aktiv, onBack = onZurueck)
}
