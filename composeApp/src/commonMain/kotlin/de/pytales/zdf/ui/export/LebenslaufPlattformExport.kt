package de.pytales.zdf.ui.export

import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable

/**
 * Rückmeldung einer plattformübergreifenden Export-, Druck- oder Kopieraktion.
 */
@Immutable
data class ExportErgebnis(
    val erfolgreich: Boolean,
    val meldung: String,
)

/**
 * Plattform-Brücke für Druckansicht, Datei-Speicherung/Teilen und Zwischenablage
 * (Desktop JVM, WebApp WasmJS/JS, Android).
 */
interface PlattformExportBruecke {
    val druckenLabel: String
    val speichernLabel: String

    fun drucken(dokument: LebenslaufExportDokument): ExportErgebnis
    fun speichernOderTeilen(dokument: LebenslaufExportDokument): ExportErgebnis
    fun kopieren(dokument: LebenslaufExportDokument): ExportErgebnis
}

/**
 * Liefert die passende [PlattformExportBruecke] für die jeweilige Zielplattform.
 */
@Composable
expect fun rememberPlattformExportBruecke(): PlattformExportBruecke
