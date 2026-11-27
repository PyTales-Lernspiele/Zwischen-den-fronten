package de.pytales.zdf.ui.theme

import androidx.compose.runtime.Composable

/**
 * Plattform-Brücke für die automatische [AnzeigeSkalierung].
 *
 * - **Web (WasmJS & JS):** Compose Multiplatform berechnet die Lage seiner unsichtbaren
 *   Barrierefreiheits-Elemente (für Screenreader) mit der Pixeldichte des jeweiligen UI-Knotens.
 *   Weil die Anzeige-Skalierung diese Dichte vergrößert, würden die Elemente um genau den
 *   [faktor] verschoben liegen. Die Web-Brücke skaliert die Barrierefreiheits-Ebene deshalb
 *   per CSS um denselben Faktor, sodass sie wieder deckungsgleich über der Spielfläche liegt.
 * - **Android & Desktop JVM:** No-Op (dort nutzen Screenreader die echten Bildschirmkoordinaten).
 */
@Composable
expect fun PlattformAnzeigeSkalierung(faktor: Float)
