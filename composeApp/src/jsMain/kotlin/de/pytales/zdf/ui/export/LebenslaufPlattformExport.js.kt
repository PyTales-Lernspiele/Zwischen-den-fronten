package de.pytales.zdf.ui.export

import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember

@Composable
actual fun rememberPlattformExportBruecke(): PlattformExportBruecke =
    remember { JsWebExportBruecke() }

private class JsWebExportBruecke : PlattformExportBruecke {

    override val druckenLabel: String = "Druckansicht öffnen & drucken"
    override val speichernLabel: String = "Druckblatt herunterladen (.html)"

    override fun drucken(dokument: LebenslaufExportDokument): ExportErgebnis {
        return if (jsOeffneDruckansichtFn(dokument.druckHtml) == true) {
            ExportErgebnis(
                erfolgreich = true,
                meldung = "Druckansicht im neuen Browser-Tab geöffnet (dort drucken oder als PDF sichern).",
            )
        } else if (jsLadeHtmlHerunterFn("${dokument.dateinameBasis}.html", dokument.druckHtml) == true) {
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
        return if (jsLadeHtmlHerunterFn(dateiname, dokument.druckHtml) == true) {
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
        return if (jsKopiereTextFn(dokument.klartext) == true) {
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

private val jsOeffneDruckansichtFn: dynamic = js(
    """
    function(html) {
        try {
            var win = window.open('', '_blank');
            if (!win) return false;
            win.document.open();
            win.document.write(html);
            win.document.close();
            win.focus();
            setTimeout(function() { try { win.print(); } catch (e) {} }, 250);
            return true;
        } catch (e) {
            return false;
        }
    }
    """,
)

private val jsLadeHtmlHerunterFn: dynamic = js(
    """
    function(dateiname, html) {
        try {
            var blob = new Blob([html], { type: 'text/html;charset=utf-8' });
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = dateiname;
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            setTimeout(function() { URL.revokeObjectURL(url); }, 1500);
            return true;
        } catch (e) {
            return false;
        }
    }
    """,
)

private val jsKopiereTextFn: dynamic = js(
    """
    function(text) {
        try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).catch(function() {});
                return true;
            }
            var ta = document.createElement('textarea');
            ta.value = text;
            ta.setAttribute('readonly', '');
            ta.style.position = 'fixed';
            ta.style.opacity = '0';
            document.body.appendChild(ta);
            ta.select();
            var ok = document.execCommand('copy');
            document.body.removeChild(ta);
            return !!ok;
        } catch (e) {
            return false;
        }
    }
    """,
)
