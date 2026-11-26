@file:OptIn(ExperimentalWasmJsInterop::class)

package de.pytales.zdf.ui.export

import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember

@Composable
actual fun rememberPlattformExportBruecke(): PlattformExportBruecke =
    remember { WasmWebExportBruecke() }

private class WasmWebExportBruecke : PlattformExportBruecke {

    override val druckenLabel: String = "Druckansicht öffnen & drucken"
    override val speichernLabel: String = "Druckblatt herunterladen (.html)"

    override fun drucken(dokument: LebenslaufExportDokument): ExportErgebnis {
        return if (wasmOeffneDruckansicht(dokument.druckHtml)) {
            ExportErgebnis(
                erfolgreich = true,
                meldung = "Druckansicht im neuen Browser-Tab geöffnet (dort drucken oder als PDF sichern).",
            )
        } else if (wasmLadeHtmlHerunter("${dokument.dateinameBasis}.html", dokument.druckHtml)) {
            ExportErgebnis(
                erfolgreich = true,
                meldung = "Popup blockiert — Druckblatt wurde stattdessen als HTML-Datei heruntergeladen.",
            )
        } else {
            ExportErgebnis(
                erfolgreich = false,
                meldung = "Druckansicht konnte nicht geöffnet werden. Nutze alternativ „Text kopieren“.",
            )
        }
    }

    override fun speichernOderTeilen(dokument: LebenslaufExportDokument): ExportErgebnis {
        val dateiname = "${dokument.dateinameBasis}.html"
        return if (wasmLadeHtmlHerunter(dateiname, dokument.druckHtml)) {
            ExportErgebnis(
                erfolgreich = true,
                meldung = "Druckblatt „$dateiname“ wurde heruntergeladen.",
            )
        } else {
            ExportErgebnis(
                erfolgreich = false,
                meldung = "Download konnte im Browser nicht gestartet werden.",
            )
        }
    }

    override fun kopieren(dokument: LebenslaufExportDokument): ExportErgebnis {
        return if (wasmKopiereText(dokument.klartext)) {
            ExportErgebnis(
                erfolgreich = true,
                meldung = "Lebenslauf und Protokoll wurden in die Zwischenablage kopiert.",
            )
        } else {
            ExportErgebnis(
                erfolgreich = false,
                meldung = "Zwischenablage nicht freigegeben. Öffne unten die Textvorschau zum Markieren.",
            )
        }
    }
}

private fun wasmOeffneDruckansicht(html: String): Boolean = js(
    """
    (() => {
        try {
            const win = window.open('', '_blank');
            if (!win) return false;
            win.document.open();
            win.document.write(html);
            win.document.close();
            win.focus();
            setTimeout(() => { try { win.print(); } catch (_) {} }, 250);
            return true;
        } catch (_) {
            return false;
        }
    })()
    """,
)

private fun wasmLadeHtmlHerunter(dateiname: String, html: String): Boolean = js(
    """
    (() => {
        try {
            const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = dateiname;
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            setTimeout(() => URL.revokeObjectURL(url), 1500);
            return true;
        } catch (_) {
            return false;
        }
    })()
    """,
)

private fun wasmKopiereText(text: String): Boolean = js(
    """
    (() => {
        try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).catch(() => {});
                return true;
            }
            const ta = document.createElement('textarea');
            ta.value = text;
            ta.setAttribute('readonly', '');
            ta.style.position = 'fixed';
            ta.style.opacity = '0';
            document.body.appendChild(ta);
            ta.select();
            const ok = document.execCommand('copy');
            document.body.removeChild(ta);
            return !!ok;
        } catch (_) {
            return false;
        }
    })()
    """,
)
