package de.pytales.zdf.ui.components

import androidx.compose.runtime.Composable

/**
 * Plattform-Brücke für die System-Zurück-Taste bzw. Zurück-Geste.
 *
 * - **Android:** bindet `androidx.activity.compose.BackHandler` ein, um geöffnete
 *   Erklärkarten sauber zu schließen und während eines laufenden Durchgangs die
 *   „Kein Zurück“-Leitplanke mit einer ruhigen Sicherheitsabfrage zu schützen.
 * - **Desktop JVM & Web:** No-Op (dort greift [archivEscapeAktion] für Tastatur-Escape).
 */
@Composable
expect fun PlattformZurueckHandler(
    aktiv: Boolean,
    onZurueck: () -> Unit,
)
