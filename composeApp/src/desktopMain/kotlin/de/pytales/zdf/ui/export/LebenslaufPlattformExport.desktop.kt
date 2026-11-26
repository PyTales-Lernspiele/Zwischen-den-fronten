package de.pytales.zdf.ui.export

import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import java.awt.Desktop
import java.awt.FileDialog
import java.awt.Frame
import java.awt.GraphicsEnvironment
import java.awt.Toolkit
import java.awt.datatransfer.StringSelection
import java.io.File
import java.nio.charset.StandardCharsets
import java.nio.file.Files

@Composable
actual fun rememberPlattformExportBruecke(): PlattformExportBruecke =
    remember { DesktopExportBruecke() }

private class DesktopExportBruecke : PlattformExportBruecke {

    override val druckenLabel: String = "Druckansicht im Browser öffnen"
    override val speichernLabel: String = "Als Druckblatt speichern (.html)"

    override fun drucken(dokument: LebenslaufExportDokument): ExportErgebnis {
        return try {
            val tempDatei = Files.createTempFile("${dokument.dateinameBasis}_", ".html").toFile()
            tempDatei.writeText(dokument.druckHtml, StandardCharsets.UTF_8)
            tempDatei.deleteOnExit()

            if (!GraphicsEnvironment.isHeadless() && Desktop.isDesktopSupported()) {
                val desktop = Desktop.getDesktop()
                if (desktop.isSupported(Desktop.Action.BROWSE)) {
                    desktop.browse(tempDatei.toURI())
                    return ExportErgebnis(
                        erfolgreich = true,
                        meldung = "Druckansicht im Browser geöffnet (dort über Strg+P drucken oder als PDF sichern).",
                    )
                }
            }
            ExportErgebnis(
                erfolgreich = true,
                meldung = "Druckblatt erstellt unter: ${tempDatei.absolutePath}",
            )
        } catch (e: Throwable) {
            ExportErgebnis(
                erfolgreich = false,
                meldung = "Druckansicht konnte nicht geöffnet werden: ${e.message ?: "Unbekannter Fehler"}",
            )
        }
    }

    override fun speichernOderTeilen(dokument: LebenslaufExportDokument): ExportErgebnis {
        val standardName = "${dokument.dateinameBasis}.html"
        return try {
            val zielDatei = if (!GraphicsEnvironment.isHeadless()) {
                val dialog = FileDialog(null as Frame?, "Lebenslauf als Druckblatt speichern", FileDialog.SAVE)
                dialog.file = standardName
                dialog.isVisible = true
                val ordner = dialog.directory
                val datei = dialog.file
                dialog.dispose()
                if (ordner == null || datei == null) {
                    return ExportErgebnis(
                        erfolgreich = false,
                        meldung = "Speichern abgebrochen.",
                    )
                }
                val mitEndung = if (datei.endsWith(".html", ignoreCase = true) ||
                    datei.endsWith(".txt", ignoreCase = true)
                ) {
                    datei
                } else {
                    "$datei.html"
                }
                File(ordner, mitEndung)
            } else {
                File(System.getProperty("user.home", "."), standardName)
            }

            val inhalt = if (zielDatei.name.endsWith(".txt", ignoreCase = true)) {
                dokument.klartext
            } else {
                dokument.druckHtml
            }
            zielDatei.writeText(inhalt, StandardCharsets.UTF_8)
            ExportErgebnis(
                erfolgreich = true,
                meldung = "Gespeichert unter: ${zielDatei.absolutePath}",
            )
        } catch (e: Throwable) {
            ExportErgebnis(
                erfolgreich = false,
                meldung = "Datei konnte nicht gespeichert werden: ${e.message ?: "Unbekannter Fehler"}",
            )
        }
    }

    override fun kopieren(dokument: LebenslaufExportDokument): ExportErgebnis {
        return try {
            val clipboard = Toolkit.getDefaultToolkit().systemClipboard
            clipboard.setContents(StringSelection(dokument.klartext), null)
            ExportErgebnis(
                erfolgreich = true,
                meldung = "Lebenslauf und Protokoll wurden in die Zwischenablage kopiert.",
            )
        } catch (e: Throwable) {
            ExportErgebnis(
                erfolgreich = false,
                meldung = "Kopieren in die Zwischenablage nicht möglich: ${e.message ?: "Unbekannter Fehler"}",
            )
        }
    }
}
