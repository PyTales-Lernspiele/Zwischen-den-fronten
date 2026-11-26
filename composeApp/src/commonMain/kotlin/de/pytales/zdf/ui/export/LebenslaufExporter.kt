package de.pytales.zdf.ui.export

import androidx.compose.runtime.Immutable
import de.pytales.zdf.content.GameContent
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.engine.GameState
import de.pytales.zdf.ui.state.ProtokollUiEintrag
import de.pytales.zdf.ui.state.UiStateMapper

/**
 * Plattformübergreifend aufbereitetes Export- und Druckdokument für den Abschlussbildschirm:
 * - [klartext]: klar gegliederter UTF-8-Text für Zwischenablage, Teilen oder Textdatei
 * - [druckHtml]: in sich geschlossenes, druckoptimiertes A4-Archivblatt (ohne externe Abhängigkeiten)
 *   für Browser-Druck, PDF-Export (Desktop/Web) und Android-PrintManager.
 */
@Immutable
data class LebenslaufExportDokument(
    val dateinameBasis: String,
    val titel: String,
    val klartext: String,
    val druckHtml: String,
)

/**
 * Reine, zustandslose und vollständig testbare Aufbereitung des 4-Fächer-Lebenslaufs
 * und des Entscheidungsprotokolls für Auswertung und Unterrichtsgespräch in Klasse 8.
 */
object LebenslaufExporter {

    private const val REFLEXIONSFRAGE_REGULAER =
        "Gesprächsimpuls: Welche Entscheidung war im Rückblick am schwersten abzuwägen — " +
            "und was wusste deine Figur damals noch nicht über die kommenden Jahre?"

    private const val REFLEXIONSFRAGE_ABBRUCH =
        "Gesprächsimpuls: Welche äußeren Umstände (Versorgung, Belastung, staatliche Kontrolle " +
            "oder Kriegsverlauf) haben diesen Lebensweg geprägt — und welche Handlungsspielräume " +
            "blieben den Menschen überhaupt?"

    fun erstelleDokument(
        content: GameContent,
        gameState: GameState,
        phase: GamePhase.Abgeschlossen,
        mitProtokoll: Boolean = true,
    ): LebenslaufExportDokument {
        val lebenslauf = phase.lebenslauf
        val person = gameState.person
        val endJahr = lebenslauf.hartesEnde?.jahr ?: 1919
        val zeitspanne = if (endJahr <= 1914) "1914" else "1914–$endJahr"
        val pfadMarke = content.konfiguration.pfade.definitionen[gameState.pfad]?.marke
            ?: gameState.pfad.code
        val modusBezeichnung = content.konfiguration.modi[gameState.modus]?.bezeichnung
            ?: gameState.modus.code
        val protokollUi = if (mitProtokoll) {
            UiStateMapper.mapProtokollEintraege(content, gameState.protokoll)
        } else {
            emptyList()
        }

        val musterungText = if (person?.musterung == null) {
            null
        } else {
            val mDaten = content.herkunft.musterung
            val gradKurz = mDaten.grade[person.musterung]?.kurz ?: person.musterung.code
            val vermerkKurz = person.vermerk?.let { mDaten.vermerke[it]?.kurz }
            buildString {
                append(gradKurz)
                if (vermerkKurz != null) append(", $vermerkKurz")
                if (!person.befund.isNullOrBlank()) append(" (${person.befund})")
            }
        }

        val figurName = person?.vollerName?.ifBlank { null } ?: "Unbenannte Figur"
        val titel = "Lebenslauf $zeitspanne — $figurName"
        val dateinameBasis = bereinigeDateiname("lebenslauf_${figurName}_1914_$endJahr")

        val klartext = baueKlartext(
            content = content,
            gameState = gameState,
            phase = phase,
            figurName = figurName,
            zeitspanne = zeitspanne,
            endJahr = endJahr,
            pfadMarke = pfadMarke,
            modusBezeichnung = modusBezeichnung,
            musterungText = musterungText,
            protokollUi = protokollUi,
        )

        val druckHtml = baueDruckHtml(
            content = content,
            gameState = gameState,
            phase = phase,
            titel = titel,
            figurName = figurName,
            zeitspanne = zeitspanne,
            endJahr = endJahr,
            pfadMarke = pfadMarke,
            modusBezeichnung = modusBezeichnung,
            musterungText = musterungText,
            protokollUi = protokollUi,
        )

        return LebenslaufExportDokument(
            dateinameBasis = dateinameBasis,
            titel = titel,
            klartext = klartext,
            druckHtml = druckHtml,
        )
    }

    /**
     * Erzeugt einen betriebssystem- und browser-sicheren ASCII-Dateinamen ohne Endung.
     */
    fun bereinigeDateiname(eingabe: String): String {
        val ersetzt = eingabe.lowercase()
            .replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
            .replace("ß", "ss")
        val sb = StringBuilder()
        var letzterUnterstrich = false
        for (ch in ersetzt) {
            if (ch in 'a'..'z' || ch in '0'..'9') {
                sb.append(ch)
                letzterUnterstrich = false
            } else if (!letzterUnterstrich && sb.isNotEmpty()) {
                sb.append('_')
                letzterUnterstrich = true
            }
        }
        val bereinigt = sb.toString().trim('_')
        return bereinigt.ifBlank { "lebenslauf_zwischen_den_fronten" }
    }

    /**
     * Maskiert Sonderzeichen zuverlässig für sicheres HTML-Rendering.
     */
    fun escapeHtml(text: String): String = buildString(text.length + 16) {
        for (ch in text) {
            when (ch) {
                '&' -> append("&amp;")
                '<' -> append("&lt;")
                '>' -> append("&gt;")
                '"' -> append("&quot;")
                '\'' -> append("&#39;")
                else -> append(ch)
            }
        }
    }

    private fun baueKlartext(
        content: GameContent,
        gameState: GameState,
        phase: GamePhase.Abgeschlossen,
        figurName: String,
        zeitspanne: String,
        endJahr: Int,
        pfadMarke: String,
        modusBezeichnung: String,
        musterungText: String?,
        protokollUi: List<ProtokollUiEintrag>,
    ): String = buildString {
        val konf = content.konfiguration
        val lebenslauf = phase.lebenslauf
        val person = gameState.person

        appendLine("======================================================================")
        appendLine("${konf.spielTitel.uppercase()} (${konf.untertitel})")
        appendLine("Lebenslauf $zeitspanne — $figurName")
        appendLine("======================================================================")
        appendLine("Verlauf: $modusBezeichnung" + if (gameState.direktwahlPfad != null) " (Unterrichts-Direktwahl)" else "")
        appendLine("Zielgruppe: ${konf.zielgruppe}")
        appendLine()

        if (person != null) {
            appendLine("1. PERSONENBLATT (AUSGANGSLAGE 1914)")
            appendLine("----------------------------------------------------------------------")
            appendLine("Name:               ${person.vollerName}")
            appendLine("Herkunft:           ${person.herkunftTitel}")
            appendLine("Jahrgang:           ${person.jahrgang} (${person.alter} Jahre im August 1914)")
            appendLine("Friedensberuf:      ${person.friedensberuf}")
            appendLine("Stellung im Krieg:  ${person.stand} · $pfadMarke")
            if (musterungText != null) {
                appendLine("Musterung:          $musterungText")
            }
            appendLine()
        }

        appendLine(
            if (lebenslauf.istVorzeitigerAbbruch) {
                "2. VORZEITIGER EINSCHNITT ($endJahr) — HISTORISCHE EINORDNUNG"
            } else {
                "2. HISTORISCHER AUSGANG (1919)"
            },
        )
        appendLine("----------------------------------------------------------------------")
        val ausgang = lebenslauf.ausgang
        val hartesEnde = lebenslauf.hartesEnde
        when {
            ausgang != null -> {
                appendLine(ausgang.titel)
                appendLine("„${ausgang.deutung}“")
                appendLine()
                appendLine(lebenslauf.fazit)
            }

            hartesEnde != null -> {
                appendLine("${hartesEnde.titel} ($endJahr)")
                appendLine(hartesEnde.text)
                appendLine()
                appendLine("Historische Einordnung (kein persönliches Versagen):")
                appendLine(lebenslauf.fazit)
            }
        }
        appendLine()

        appendLine("3. 4-FÄCHER-LEBENSLAUF (WAS DIESEN WEG GEPRÄGT HAT)")
        appendLine("----------------------------------------------------------------------")
        lebenslauf.faecher.forEach { fach ->
            append("Fach ${fach.fachIndex + 1} — ${fach.titel}: ")
            if (fach.merkmalName != null) {
                append(fach.merkmalName)
                if (fach.eintrag != null) {
                    append(" (${fach.eintrag.datum})")
                }
                appendLine()
                if (fach.eintrag != null) {
                    appendLine("  ${fach.eintrag.text}")
                }
            } else {
                appendLine("Kein einzelner Schwerpunkt vermerkt.")
            }
        }
        appendLine()

        appendLine("4. CHRONOLOGISCHE ZEITLEISTE")
        appendLine("----------------------------------------------------------------------")
        lebenslauf.zeitleiste.forEach { eintrag ->
            appendLine("- [${eintrag.datum}] (${eintrag.quelle}): ${eintrag.text}")
        }
        appendLine()

        if (protokollUi.isNotEmpty()) {
            appendLine("5. ENTSCHEIDUNGSPROTOKOLL (${protokollUi.size} STATIONEN)")
            appendLine("----------------------------------------------------------------------")
            protokollUi.forEachIndexed { idx, eintrag ->
                appendLine("${idx + 1}. ${eintrag.jahr} · ${eintrag.station}: ${eintrag.wahl}")
            }
            appendLine()
        }

        if (lebenslauf.werteBilanz.isNotEmpty()) {
            val nummer = if (protokollUi.isNotEmpty()) 6 else 5
            appendLine("$nummer. BEFINDENSSTAND AM ENDE ($endJahr, OHNE PUNKTE)")
            appendLine("----------------------------------------------------------------------")
            lebenslauf.werteBilanz.forEach { status ->
                val balken = "■".repeat(status.gefuellteSegmente) +
                    "□".repeat((status.segmenteGesamt - status.gefuellteSegmente).coerceAtLeast(0))
                appendLine(
                    "- ${status.bezeichnung}: ${status.stufenName} " +
                        "[$balken ${status.gefuellteSegmente}/${status.segmenteGesamt}] — ${status.stufenKurz}",
                )
            }
            appendLine()
        }

        appendLine("----------------------------------------------------------------------")
        appendLine(
            if (lebenslauf.istVorzeitigerAbbruch) REFLEXIONSFRAGE_ABBRUCH else REFLEXIONSFRAGE_REGULAER,
        )
    }.trimEnd()

    private fun baueDruckHtml(
        content: GameContent,
        gameState: GameState,
        phase: GamePhase.Abgeschlossen,
        titel: String,
        figurName: String,
        zeitspanne: String,
        endJahr: Int,
        pfadMarke: String,
        modusBezeichnung: String,
        musterungText: String?,
        protokollUi: List<ProtokollUiEintrag>,
    ): String {
        val konf = content.konfiguration
        val fw = konf.farbwelt
        val lebenslauf = phase.lebenslauf
        val person = gameState.person
        val e = ::escapeHtml

        return buildString {
            appendLine("<!DOCTYPE html>")
            appendLine("<html lang=\"de\">")
            appendLine("<head>")
            appendLine("  <meta charset=\"UTF-8\">")
            appendLine("  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">")
            appendLine("  <title>${e(titel)} — ${e(konf.spielTitel)}</title>")
            appendLine("  <style>")
            appendLine("    @page { size: A4; margin: 15mm 16mm; }")
            appendLine("    * { box-sizing: border-box; }")
            appendLine("    body {")
            appendLine("      margin: 0; padding: 24px;")
            appendLine("      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;")
            appendLine("      font-size: 11pt; line-height: 1.48;")
            appendLine("      color: ${e(fw.tinte)}; background: ${e(fw.papier)};")
            appendLine("    }")
            appendLine("    .seite { max-width: 820px; margin: 0 auto; background: ${e(fw.papierHell)}; border: 1.5px solid ${e(fw.linie)}; padding: 22px 26px; }")
            appendLine("    .kopf { border-bottom: 2.5px solid ${e(fw.akzent)}; padding-bottom: 12px; margin-bottom: 16px; }")
            appendLine("    .stempel { display: inline-block; font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 8.5pt; font-weight: 700; letter-spacing: 0.04em; padding: 2px 7px; border: 1px solid ${e(fw.akzent)}; color: ${e(fw.akzent)}; background: ${e(fw.papier)}; border-radius: 2px; }")
            appendLine("    .stempel-matt { border-color: ${e(fw.linie)}; color: ${e(fw.tinteMatt)}; }")
            appendLine("    h1, h2, h3 { font-family: Georgia, 'Times New Roman', serif; margin: 0; color: ${e(fw.tinte)}; }")
            appendLine("    h1 { font-size: 19pt; margin-top: 6px; }")
            appendLine("    h2 { font-size: 13pt; margin-bottom: 8px; border-bottom: 1px solid ${e(fw.linieFein)}; padding-bottom: 4px; }")
            appendLine("    .untertitel { color: ${e(fw.tinteMatt)}; font-size: 9.5pt; margin-top: 4px; }")
            appendLine("    .klassenzeile { display: flex; justify-content: space-between; gap: 16px; margin-top: 10px; padding-top: 8px; border-top: 1px dashed ${e(fw.linieFein)}; font-size: 9.5pt; color: ${e(fw.tinteMatt)}; }")
            appendLine("    .abschnitt { margin-bottom: 16px; break-inside: avoid; }")
            appendLine("    .meta-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(175px, 1fr)); gap: 8px; margin-top: 10px; }")
            appendLine("    .meta-feld { background: ${e(fw.papier)}; border: 1px solid ${e(fw.linieFein)}; padding: 6px 9px; border-radius: 2px; }")
            appendLine("    .meta-label { font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 7.5pt; color: ${e(fw.tinteMatt)}; text-transform: uppercase; }")
            appendLine("    .meta-wert { font-weight: 600; font-size: 9.5pt; margin-top: 2px; }")
            appendLine("    .deutung { font-family: Georgia, serif; font-style: italic; color: ${e(fw.akzent)}; font-size: 11.5pt; margin: 6px 0; }")
            appendLine("    .hinweis-box { background: ${e(fw.papier)}; border-left: 3px solid ${e(fw.akzent)}; padding: 9px 12px; margin-top: 8px; }")
            appendLine("    .faecher-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }")
            appendLine("    .fach-karte { background: ${e(fw.papier)}; border: 1px solid ${e(fw.linie)}; padding: 10px 12px; border-radius: 2px; break-inside: avoid; }")
            appendLine("    .fach-kopf { display: flex; justify-content: space-between; align-items: baseline; gap: 8px; margin-bottom: 4px; }")
            appendLine("    .fach-titel { font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 8pt; font-weight: 700; color: ${e(fw.akzent)}; text-transform: uppercase; }")
            appendLine("    .fach-name { font-family: Georgia, serif; font-weight: 700; font-size: 11pt; margin-bottom: 4px; }")
            appendLine("    .zeitleiste-eintrag { border-left: 3px solid ${e(fw.akzent)}; background: ${e(fw.papier)}; padding: 7px 11px; margin-bottom: 7px; break-inside: avoid; }")
            appendLine("    .zeitleiste-meta { display: flex; justify-content: space-between; font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 8.5pt; color: ${e(fw.tinteMatt)}; margin-bottom: 3px; }")
            appendLine("    table.protokoll { width: 100%; border-collapse: collapse; font-size: 9.5pt; }")
            appendLine("    table.protokoll th, table.protokoll td { border: 1px solid ${e(fw.linieFein)}; padding: 5px 8px; text-align: left; vertical-align: top; }")
            appendLine("    table.protokoll th { background: ${e(fw.papierDunkel)}; font-size: 8.5pt; text-transform: uppercase; }")
            appendLine("    table.protokoll tr { break-inside: avoid; }")
            appendLine("    .werte-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }")
            appendLine("    .wert-karte { background: ${e(fw.papier)}; border: 1px solid ${e(fw.linieFein)}; padding: 8px 10px; }")
            appendLine("    .segmente { display: flex; gap: 3px; margin: 5px 0; }")
            appendLine("    .seg { flex: 1; height: 7px; border-radius: 1px; background: ${e(fw.segmentLeer)}; }")
            appendLine("    .seg.aktiv { background: ${e(fw.tinte)}; }")
            appendLine("    .fuss { margin-top: 16px; padding-top: 10px; border-top: 1px solid ${e(fw.linie)}; font-size: 9.5pt; color: ${e(fw.tinteMatt)}; font-style: italic; }")
            appendLine("    .druck-leiste { max-width: 820px; margin: 0 auto 12px auto; display: flex; justify-content: flex-end; gap: 8px; }")
            appendLine("    .druck-knopf { background: ${e(fw.tinte)}; color: ${e(fw.papierHell)}; border: none; padding: 8px 16px; border-radius: 3px; font-weight: 600; cursor: pointer; }")
            appendLine("    @media print {")
            appendLine("      body { background: #ffffff; padding: 0; }")
            appendLine("      .seite { border: none; padding: 0; max-width: none; background: #ffffff; }")
            appendLine("      .druck-leiste { display: none; }")
            appendLine("      .fach-karte, .zeitleiste-eintrag, .meta-feld, .wert-karte, .hinweis-box { background: #faf8f4; }")
            appendLine("    }")
            appendLine("  </style>")
            appendLine("</head>")
            appendLine("<body>")
            appendLine("  <div class=\"druck-leiste\">")
            appendLine("    <button class=\"druck-knopf\" onclick=\"window.print()\">Drucken / Als PDF sichern</button>")
            appendLine("  </div>")
            appendLine("  <main class=\"seite\">")
            appendLine("    <header class=\"kopf\">")
            appendLine("      <span class=\"stempel\">${e(konf.spielTitel.uppercase())} · $zeitspanne</span>")
            append("      <span class=\"stempel stempel-matt\">${e(modusBezeichnung)}")
            if (gameState.direktwahlPfad != null) append(" · Direktwahl")
            appendLine("</span>")
            appendLine("      <h1>${e(figurName)}</h1>")
            appendLine("      <div class=\"untertitel\">${e(konf.untertitel)} · ${e(pfadMarke)} · ${e(konf.zielgruppe)}</div>")
            appendLine("      <div class=\"klassenzeile\">")
            appendLine("        <span>Name / Klasse: ___________________________</span>")
            appendLine("        <span>Datum: _________________</span>")
            appendLine("      </div>")
            appendLine("    </header>")

            // 1. Ausgang / Auffangnetz + Personenblatt
            appendLine("    <section class=\"abschnitt\">")
            val ausgang = lebenslauf.ausgang
            val hartesEnde = lebenslauf.hartesEnde
            when {
                ausgang != null -> {
                    appendLine("      <h2>Historischer Ausgang (1919): ${e(ausgang.titel)}</h2>")
                    appendLine("      <p class=\"deutung\">„${e(ausgang.deutung)}“</p>")
                    appendLine("      <p>${e(lebenslauf.fazit)}</p>")
                }

                hartesEnde != null -> {
                    appendLine("      <h2>Vorzeitiger Einschnitt ($endJahr): ${e(hartesEnde.titel)}</h2>")
                    appendLine("      <p>${e(hartesEnde.text)}</p>")
                    appendLine("      <div class=\"hinweis-box\"><strong>Historische Einordnung · Kein persönliches Versagen:</strong> ${e(lebenslauf.fazit)}</div>")
                }
            }

            if (person != null) {
                appendLine("      <div class=\"meta-grid\">")
                appendMetaFeld("Name", person.vollerName, e)
                appendMetaFeld("Herkunft", person.herkunftTitel, e)
                appendMetaFeld("Jahrgang", "${person.jahrgang} (${person.alter} Jahre 1914)", e)
                appendMetaFeld("Friedensberuf", person.friedensberuf, e)
                appendMetaFeld("Stellung im Krieg", "${person.stand} · $pfadMarke", e)
                if (musterungText != null) {
                    appendMetaFeld("Musterung", musterungText, e)
                }
                appendLine("      </div>")
            }
            appendLine("    </section>")

            // 2. 4-Fächer-Lebenslauf
            appendLine("    <section class=\"abschnitt\">")
            appendLine("      <h2>4-Fächer-Lebenslauf — Was diesen Weg geprägt hat</h2>")
            appendLine("      <div class=\"faecher-grid\">")
            lebenslauf.faecher.forEach { fach ->
                appendLine("        <article class=\"fach-karte\">")
                appendLine("          <div class=\"fach-kopf\">")
                appendLine("            <span class=\"fach-titel\">Fach ${fach.fachIndex + 1} · ${e(fach.titel)}</span>")
                if (fach.eintrag != null) {
                    appendLine("            <span class=\"stempel stempel-matt\">${e(fach.eintrag.datum)}</span>")
                }
                appendLine("          </div>")
                if (fach.merkmalName != null) {
                    appendLine("          <div class=\"fach-name\">${e(fach.merkmalName)}</div>")
                    if (fach.eintrag != null) {
                        appendLine("          <div>${e(fach.eintrag.text)}</div>")
                    }
                } else {
                    appendLine("          <div style=\"font-style: italic; color: ${e(fw.tinteMatt)};\">Kein einzelner Schwerpunkt vermerkt.</div>")
                }
                appendLine("        </article>")
            }
            appendLine("      </div>")
            appendLine("    </section>")

            // 3. Zeitleiste
            appendLine("    <section class=\"abschnitt\">")
            appendLine("      <h2>Chronologische Zeitleiste</h2>")
            lebenslauf.zeitleiste.forEach { eintrag ->
                appendLine("      <div class=\"zeitleiste-eintrag\">")
                appendLine("        <div class=\"zeitleiste-meta\"><strong>${e(eintrag.datum)}</strong><span>${e(eintrag.quelle)}</span></div>")
                appendLine("        <div>${e(eintrag.text)}</div>")
                appendLine("      </div>")
            }
            appendLine("    </section>")

            // 4. Entscheidungsprotokoll
            if (protokollUi.isNotEmpty()) {
                appendLine("    <section class=\"abschnitt\">")
                appendLine("      <h2>Entscheidungsprotokoll (${protokollUi.size} Stationen)</h2>")
                appendLine("      <table class=\"protokoll\">")
                appendLine("        <thead><tr><th>Nr.</th><th>Jahr</th><th>Station</th><th>Gewählter Weg</th></tr></thead>")
                appendLine("        <tbody>")
                protokollUi.forEachIndexed { idx, eintrag ->
                    appendLine(
                        "          <tr><td>${idx + 1}</td><td>${eintrag.jahr}</td>" +
                            "<td>${e(eintrag.station)}</td><td><strong>${e(eintrag.wahl)}</strong></td></tr>",
                    )
                }
                appendLine("        </tbody>")
                appendLine("      </table>")
                appendLine("    </section>")
            }

            // 5. Befindensstand
            if (lebenslauf.werteBilanz.isNotEmpty()) {
                appendLine("    <section class=\"abschnitt\">")
                appendLine("      <h2>Befindensstand am Ende ($endJahr · ohne Punkte)</h2>")
                appendLine("      <div class=\"werte-grid\">")
                lebenslauf.werteBilanz.forEach { status ->
                    appendLine("        <div class=\"wert-karte\">")
                    appendLine("          <div style=\"display:flex;justify-content:space-between;align-items:center;\">")
                    appendLine("            <strong>${e(status.bezeichnung)}</strong>")
                    appendLine("            <span class=\"stempel stempel-matt\">${e(status.stufenName)} (${status.gefuellteSegmente}/${status.segmenteGesamt})</span>")
                    appendLine("          </div>")
                    append("          <div class=\"segmente\">")
                    for (seg in 0 until status.segmenteGesamt) {
                        val klasse = if (seg < status.gefuellteSegmente) "seg aktiv" else "seg"
                        append("<span class=\"$klasse\"></span>")
                    }
                    appendLine("</div>")
                    appendLine("          <div style=\"font-size:9pt;color:${e(fw.tinteMatt)};\">${e(status.stufenKurz)}</div>")
                    appendLine("        </div>")
                }
                appendLine("      </div>")
                appendLine("    </section>")
            }

            // Fußzeile mit Reflexionsimpuls
            val impuls = if (lebenslauf.istVorzeitigerAbbruch) REFLEXIONSFRAGE_ABBRUCH else REFLEXIONSFRAGE_REGULAER
            appendLine("    <footer class=\"fuss\">${e(impuls)}</footer>")
            appendLine("  </main>")
            appendLine("</body>")
            appendLine("</html>")
        }
    }

    private fun StringBuilder.appendMetaFeld(
        label: String,
        wert: String,
        escape: (String) -> String,
    ) {
        appendLine("        <div class=\"meta-feld\"><div class=\"meta-label\">${escape(label)}</div><div class=\"meta-wert\">${escape(wert)}</div></div>")
    }
}
