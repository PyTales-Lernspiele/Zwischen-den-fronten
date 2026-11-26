package de.pytales.zdf

import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application
import androidx.compose.ui.window.rememberWindowState
import de.pytales.zdf.ui.App

fun main() = application {
    Window(
        onCloseRequest = ::exitApplication,
        title = "Zwischen den Fronten (1914–1919)",
        state = rememberWindowState(width = 1200.dp, height = 800.dp),
    ) {
        App()
    }
}
