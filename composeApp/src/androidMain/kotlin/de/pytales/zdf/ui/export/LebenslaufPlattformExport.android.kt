package de.pytales.zdf.ui.export

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.print.PrintAttributes
import android.print.PrintManager
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext

@Composable
actual fun rememberPlattformExportBruecke(): PlattformExportBruecke {
    val context = LocalContext.current
    return remember(context) { AndroidExportBruecke(context) }
}

private class AndroidExportBruecke(
    private val context: Context,
) : PlattformExportBruecke {

    override val druckenLabel: String = "Drucken / als PDF sichern"
    override val speichernLabel: String = "Als Text teilen"

    // Referenz halten, bis der Druckauftrag vom System übernommen wurde
    private var aktiverDruckWebView: WebView? = null

    override fun drucken(dokument: LebenslaufExportDokument): ExportErgebnis {
        return try {
            val printManager = context.getSystemService(Context.PRINT_SERVICE) as? PrintManager
                ?: return ExportErgebnis(
                    erfolgreich = false,
                    meldung = "Druckdienst ist auf diesem Gerät nicht verfügbar.",
                )

            val webView = WebView(context)
            webView.settings.javaScriptEnabled = false
            webView.webViewClient = object : WebViewClient() {
                override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean = false

                override fun onPageFinished(view: WebView, url: String?) {
                    val adapter = view.createPrintDocumentAdapter(dokument.dateinameBasis)
                    printManager.print(
                        dokument.titel,
                        adapter,
                        PrintAttributes.Builder()
                            .setMediaSize(PrintAttributes.MediaSize.ISO_A4)
                            .build(),
                    )
                    aktiverDruckWebView = null
                }
            }
            aktiverDruckWebView = webView
            webView.loadDataWithBaseURL(
                null,
                dokument.druckHtml,
                "text/html",
                "UTF-8",
                null,
            )
            ExportErgebnis(
                erfolgreich = true,
                meldung = "Android-Druckvorschau geöffnet (Drucker oder „Als PDF speichern“ wählen).",
            )
        } catch (e: Throwable) {
            ExportErgebnis(
                erfolgreich = false,
                meldung = "Druckvorschau konnte nicht geöffnet werden: ${e.message ?: "Unbekannter Fehler"}",
            )
        }
    }

    override fun speichernOderTeilen(dokument: LebenslaufExportDokument): ExportErgebnis {
        return try {
            val sendIntent = Intent(Intent.ACTION_SEND).apply {
                type = "text/plain"
                putExtra(Intent.EXTRA_SUBJECT, dokument.titel)
                putExtra(Intent.EXTRA_TEXT, dokument.klartext)
            }
            val chooser = Intent.createChooser(sendIntent, "Lebenslauf teilen oder sichern").apply {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            context.startActivity(chooser)
            ExportErgebnis(
                erfolgreich = true,
                meldung = "Teilen-Menü geöffnet (z. B. für Notizen, E-Mail oder Lernplattform).",
            )
        } catch (e: Throwable) {
            ExportErgebnis(
                erfolgreich = false,
                meldung = "Teilen-Menü konnte nicht geöffnet werden: ${e.message ?: "Unbekannter Fehler"}",
            )
        }
    }

    override fun kopieren(dokument: LebenslaufExportDokument): ExportErgebnis {
        return try {
            val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as? ClipboardManager
                ?: return ExportErgebnis(
                    erfolgreich = false,
                    meldung = "Zwischenablage ist nicht verfügbar.",
                )
            clipboard.setPrimaryClip(ClipData.newPlainText(dokument.titel, dokument.klartext))
            ExportErgebnis(
                erfolgreich = true,
                meldung = "Lebenslauf und Protokoll wurden in die Zwischenablage kopiert.",
            )
        } catch (e: Throwable) {
            ExportErgebnis(
                erfolgreich = false,
                meldung = "Kopieren fehlgeschlagen: ${e.message ?: "Unbekannter Fehler"}",
            )
        }
    }
}
