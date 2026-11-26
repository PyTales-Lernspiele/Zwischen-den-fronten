package de.pytales.zdf.ui.screens

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.clearAndSetSemantics
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.engine.HartesEndeErgebnis
import de.pytales.zdf.engine.LebenslaufFachErgebnis
import de.pytales.zdf.engine.LebenslaufZeitleistenEintrag
import de.pytales.zdf.engine.WertStatus
import de.pytales.zdf.ui.components.ArchivStempel
import de.pytales.zdf.ui.components.ArchivTrennlinie
import de.pytales.zdf.ui.components.FuenfSegmentBalken
import de.pytales.zdf.ui.components.archivFokusGruppe
import de.pytales.zdf.ui.components.archivFokusRahmen
import de.pytales.zdf.ui.components.archivLiveHinweis
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.export.ExportErgebnis
import de.pytales.zdf.ui.export.LebenslaufExportDokument
import de.pytales.zdf.ui.export.LebenslaufExporter
import de.pytales.zdf.ui.export.PlattformExportBruecke
import de.pytales.zdf.ui.export.rememberPlattformExportBruecke
import de.pytales.zdf.ui.state.ProtokollUiEintrag
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.state.UiStateMapper
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.ArchivUebergaenge
import de.pytales.zdf.ui.theme.LayoutKlasse
import de.pytales.zdf.ui.theme.Schriftgroesse

/**
 * Schlussbildschirm (`GamePhase.Abgeschlossen`):
 * - Bei vorzeitigem Abbruch (`hartesEnde != null && !auffangnetzBestaetigt`): ruhiges,
 *   respektvolles Auffangnetz mit historischer Einordnung (kein Game-Over-Schock, kein Punktestand)
 *   und Übergang in den erreichten 4-Fächer-Lebenslauf.
 * - Danach bzw. bei regulärem Erreichen von 1919: vollständiger **4-Fächer-Lebenslauf**
 *   mit Personendaten, historischem Ausgang, allen 4 Fächern, chronologischer Zeitleiste,
 *   aufklappbarem Entscheidungsweg, Wertebilanz, **Export-/Druckansicht für das Klassenzimmer**
 *   (Desktop JVM, WebApp, Android) und sauberem „Neuer Durchgang“-Button.
 */
@Composable
fun AbschlussScreen(
    engine: GameEngine,
    uiState: SpielUiState,
    phase: GamePhase.Abgeschlossen,
    onAuffangnetzBestaetigen: () -> Unit,
    onNeuerDurchgang: () -> Unit,
    onSchriftgroesseChange: (Schriftgroesse) -> Unit,
    onAnalyseModusToggle: () -> Unit,
    onAudioToggle: () -> Unit = {},
    modifier: Modifier = Modifier,
) {
    val hartesEnde = phase.hartesEnde
    if (hartesEnde != null && !uiState.auffangnetzBestaetigt) {
        AuffangnetzAnsicht(
            engine = engine,
            uiState = uiState,
            hartesEnde = hartesEnde,
            fazit = phase.lebenslauf.fazit,
            onLebenslaufAnsehen = onAuffangnetzBestaetigen,
            onNeuerDurchgang = onNeuerDurchgang,
            onSchriftgroesseChange = onSchriftgroesseChange,
            onAnalyseModusToggle = onAnalyseModusToggle,
            onAudioToggle = onAudioToggle,
            modifier = modifier,
        )
    } else {
        LebenslaufAnsicht(
            engine = engine,
            uiState = uiState,
            phase = phase,
            onNeuerDurchgang = onNeuerDurchgang,
            onSchriftgroesseChange = onSchriftgroesseChange,
            onAnalyseModusToggle = onAnalyseModusToggle,
            onAudioToggle = onAudioToggle,
            modifier = modifier,
        )
    }
}

/**
 * Ruhiges, respektvolles Auffangnetz bei vorzeitigem Abbruch vor 1919
 * (bewusst ohne Schockeffekte, ohne Vorwurf und ohne Punktestand).
 */
@Composable
private fun AuffangnetzAnsicht(
    engine: GameEngine,
    uiState: SpielUiState,
    hartesEnde: HartesEndeErgebnis,
    fazit: String,
    onLebenslaufAnsehen: () -> Unit,
    onNeuerDurchgang: () -> Unit,
    onSchriftgroesseChange: (Schriftgroesse) -> Unit,
    onAnalyseModusToggle: () -> Unit,
    onAudioToggle: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val layoutKlasse = ArchivTheme.layoutKlasse
    val person = uiState.gameState.person
    val pfadMarke = engine.content.konfiguration.pfade.definitionen[uiState.gameState.pfad]?.marke
        ?: uiState.gameState.pfad.code

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(farben.papier),
    ) {
        ArchivKopfBand(
            marke = "${hartesEnde.jahr} · EINSCHNITT",
            titel = "Dein Weg endet vor 1919",
            untertitel = listOfNotNull(person?.vollerName, pfadMarke).joinToString(" · "),
            schriftgroesse = uiState.schriftgroesse,
            onSchriftgroesseChange = onSchriftgroesseChange,
            analyseModus = uiState.analyseModus,
            onAnalyseModusToggle = onAnalyseModusToggle,
            audioZustand = uiState.audioZustand,
            onAudioToggle = onAudioToggle,
        )

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .verticalScroll(rememberScrollState()),
            contentAlignment = Alignment.TopCenter,
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .widthIn(max = 760.dp)
                    .padding(horizontal = metrik.aussenAbstand, vertical = metrik.elementAbstand)
                    .archivFokusGruppe(),
                verticalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
            ) {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = farben.papierHell,
                    shape = RoundedCornerShape(4.dp),
                    border = BorderStroke(1.25.dp, farben.linie),
                    shadowElevation = 1.dp,
                ) {
                    Column(modifier = Modifier.fillMaxWidth()) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(3.dp)
                                .background(farben.tinteMatt),
                        )

                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(metrik.kartenInnenAbstand),
                            verticalArrangement = Arrangement.spacedBy(14.dp),
                        ) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically,
                            ) {
                                ArchivStempel(
                                    text = "JAHR ${hartesEnde.jahr}",
                                    farbe = farben.tinteMatt,
                                    hintergrund = farben.papier,
                                )
                                Text(
                                    text = pfadMarke,
                                    style = MaterialTheme.typography.labelSmall,
                                    color = farben.tinteMatt,
                                )
                            }

                            Text(
                                text = hartesEnde.titel,
                                style = MaterialTheme.typography.headlineLarge,
                                color = farben.tinte,
                                modifier = Modifier.archivUeberschrift(),
                            )

                            Text(
                                text = hartesEnde.text,
                                style = MaterialTheme.typography.bodyLarge,
                                color = farben.tinte,
                            )

                            ArchivTrennlinie(farbe = farben.linieFein)

                            // Respektvolle historische Einordnung
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .background(farben.papier, RoundedCornerShape(3.dp))
                                    .border(1.dp, farben.linie, RoundedCornerShape(3.dp))
                                    .padding(14.dp),
                            ) {
                                Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                                    Text(
                                        text = "HISTORISCHE EINORDNUNG · KEIN PERSÖNLICHES VERSAGEN",
                                        style = MaterialTheme.typography.labelSmall,
                                        color = farben.tinte,
                                        fontWeight = FontWeight.Bold,
                                    )
                                    Text(
                                        text = fazit,
                                        style = MaterialTheme.typography.bodyMedium,
                                        color = farben.tinte,
                                    )
                                    Text(
                                        text = "Dein bisheriger Weg bleibt vollständig erhalten und lässt sich im Lebenslauf nachvollziehen, drucken oder sichern.",
                                        style = MaterialTheme.typography.bodySmall,
                                        fontStyle = FontStyle.Italic,
                                        color = farben.tinteMatt,
                                    )
                                }
                            }

                            if (layoutKlasse == LayoutKlasse.KOMPAKT) {
                                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                                    ArchivPrimaerKnopf(
                                        label = "Erreichten Lebenslauf ansehen",
                                        onClick = onLebenslaufAnsehen,
                                        modifier = Modifier.fillMaxWidth(),
                                    )
                                    ArchivSekundaerKnopf(
                                        label = "Neuer Durchgang",
                                        onClick = onNeuerDurchgang,
                                        modifier = Modifier.fillMaxWidth(),
                                    )
                                }
                            } else {
                                Row(
                                    horizontalArrangement = Arrangement.spacedBy(12.dp),
                                    verticalAlignment = Alignment.CenterVertically,
                                ) {
                                    ArchivPrimaerKnopf(
                                        label = "Erreichten Lebenslauf ansehen",
                                        onClick = onLebenslaufAnsehen,
                                    )
                                    ArchivSekundaerKnopf(
                                        label = "Neuer Durchgang",
                                        onClick = onNeuerDurchgang,
                                    )
                                }
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
}

/**
 * Vollständige Darstellung des 4-Fächer-Lebenslaufs aus [LebenslaufCalculator]:
 * Personendaten, historischer Ausgang (bzw. vorzeitiger Einschnitt), alle 4 Fächer,
 * chronologische Zeitleiste, aufklappbarer Entscheidungsweg, Wertebilanz,
 * Klassenzimmer-Export/Druckansicht & „Neuer Durchgang“.
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun LebenslaufAnsicht(
    engine: GameEngine,
    uiState: SpielUiState,
    phase: GamePhase.Abgeschlossen,
    onNeuerDurchgang: () -> Unit,
    onSchriftgroesseChange: (Schriftgroesse) -> Unit,
    onAnalyseModusToggle: () -> Unit,
    onAudioToggle: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val layoutKlasse = ArchivTheme.layoutKlasse
    val gameState = uiState.gameState
    val person = gameState.person
    val lebenslauf = phase.lebenslauf
    val pfadMarke = engine.content.konfiguration.pfade.definitionen[gameState.pfad]?.marke
        ?: gameState.pfad.code
    val modusBezeichnung = engine.content.konfiguration.modi[gameState.modus]?.bezeichnung
        ?: gameState.modus.code
    val protokollUi = remember(engine.content, gameState.protokoll) {
        UiStateMapper.mapProtokollEintraege(engine.content, gameState.protokoll)
    }

    val endJahr = lebenslauf.hartesEnde?.jahr ?: 1919
    val zeitspanne = if (endJahr <= 1914) "1914" else "1914–$endJahr"

    val musterungText = remember(engine.content, person) {
        if (person?.musterung == null) {
            null
        } else {
            val mDaten = engine.content.herkunft.musterung
            val gradKurz = mDaten.grade[person.musterung]?.kurz ?: person.musterung.code
            val vermerkKurz = person.vermerk?.let { mDaten.vermerke[it]?.kurz }
            buildString {
                append(gradKurz)
                if (vermerkKurz != null) append(", $vermerkKurz")
                if (!person.befund.isNullOrBlank()) append(" (${person.befund})")
            }
        }
    }

    // Export-/Druckaufbereitung für das Klassenzimmer
    var exportMitProtokoll by remember { mutableStateOf(true) }
    val exportDokument = remember(
        engine.content,
        gameState,
        phase,
        exportMitProtokoll,
        uiState.analyseModus,
    ) {
        LebenslaufExporter.erstelleDokument(
            content = engine.content,
            gameState = gameState,
            phase = phase,
            mitProtokoll = exportMitProtokoll,
            analyseModus = uiState.analyseModus,
        )
    }
    val exportBruecke = rememberPlattformExportBruecke()

    val scrollState = rememberScrollState()
    LaunchedEffect(uiState.auffangnetzBestaetigt) {
        scrollState.scrollTo(0)
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(farben.papier),
    ) {
        ArchivKopfBand(
            marke = "LEBENSLAUF · $zeitspanne",
            titel = person?.vollerName?.ifBlank { null } ?: "Abgeschlossener Lebenslauf",
            untertitel = listOfNotNull(
                person?.herkunftTitel?.ifBlank { null },
                person?.let { "Jahrgang ${it.jahrgang}" },
                pfadMarke,
            ).joinToString(" · "),
            schriftgroesse = uiState.schriftgroesse,
            onSchriftgroesseChange = onSchriftgroesseChange,
            analyseModus = uiState.analyseModus,
            onAnalyseModusToggle = onAnalyseModusToggle,
            audioZustand = uiState.audioZustand,
            onAudioToggle = onAudioToggle,
        )

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .verticalScroll(scrollState),
            contentAlignment = Alignment.TopCenter,
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .widthIn(max = metrik.maxInhaltsBreite)
                    .padding(horizontal = metrik.aussenAbstand, vertical = metrik.elementAbstand)
                    .archivFokusGruppe(),
                verticalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
            ) {
                // 1. Personenblatt & Historischer Ausgang (oder vorzeitiger Einschnitt)
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = farben.papierHell,
                    shape = RoundedCornerShape(4.dp),
                    border = BorderStroke(1.25.dp, farben.linie),
                    shadowElevation = 1.dp,
                ) {
                    Column(modifier = Modifier.fillMaxWidth()) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(3.dp)
                                .background(if (lebenslauf.istVorzeitigerAbbruch) farben.tinteMatt else farben.akzent),
                        )

                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(metrik.kartenInnenAbstand),
                            verticalArrangement = Arrangement.spacedBy(12.dp),
                        ) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically,
                            ) {
                                ArchivStempel(
                                    text = if (lebenslauf.istVorzeitigerAbbruch) {
                                        "AUFFANGNETZ · ABBRUCH $endJahr"
                                    } else {
                                        "HISTORISCHER AUSGANG · 1919"
                                    },
                                    farbe = if (lebenslauf.istVorzeitigerAbbruch) farben.tinteMatt else farben.akzent,
                                )
                                Text(
                                    text = buildString {
                                        append(modusBezeichnung)
                                        if (gameState.direktwahlPfad != null) {
                                            append(" · Direktwahl")
                                        }
                                    },
                                    style = MaterialTheme.typography.labelSmall,
                                    color = farben.tinteMatt,
                                )
                            }

                            // Ausgangstitel & Deutung
                            val ausgang = lebenslauf.ausgang
                            val hartesEnde = lebenslauf.hartesEnde
                            when {
                                ausgang != null -> {
                                    Text(
                                        text = ausgang.titel,
                                        style = MaterialTheme.typography.headlineLarge,
                                        color = farben.tinte,
                                        modifier = Modifier.archivUeberschrift(),
                                    )
                                    Text(
                                        text = "„${ausgang.deutung}“",
                                        style = MaterialTheme.typography.titleMedium,
                                        fontFamily = FontFamily.Serif,
                                        fontStyle = FontStyle.Italic,
                                        color = farben.akzent,
                                    )
                                    Text(
                                        text = lebenslauf.fazit,
                                        style = MaterialTheme.typography.bodyLarge,
                                        color = farben.tinte,
                                    )
                                    if (uiState.analyseModus && ausgang.lehrplan.isNotBlank()) {
                                        Box(
                                            modifier = Modifier
                                                .fillMaxWidth()
                                                .background(farben.papier, RoundedCornerShape(3.dp))
                                                .border(1.dp, farben.linieFein, RoundedCornerShape(3.dp))
                                                .padding(10.dp),
                                        ) {
                                            Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
                                                Text(
                                                    text = "ANALYSEMODUS · LEHRPLANBEZUG",
                                                    style = MaterialTheme.typography.labelSmall,
                                                    color = farben.akzent,
                                                    fontWeight = FontWeight.Bold,
                                                )
                                                Text(
                                                    text = ausgang.lehrplan,
                                                    style = MaterialTheme.typography.bodySmall,
                                                    color = farben.tinte,
                                                )
                                            }
                                        }
                                    }
                                }

                                hartesEnde != null -> {
                                    Text(
                                        text = "${hartesEnde.titel} (${hartesEnde.jahr})",
                                        style = MaterialTheme.typography.headlineLarge,
                                        color = farben.tinte,
                                        modifier = Modifier.archivUeberschrift(),
                                    )
                                    Text(
                                        text = hartesEnde.text,
                                        style = MaterialTheme.typography.bodyLarge,
                                        color = farben.tinte,
                                    )
                                    Text(
                                        text = lebenslauf.fazit,
                                        style = MaterialTheme.typography.bodyMedium,
                                        color = farben.tinteMatt,
                                    )
                                }
                            }

                            // Personendaten-Steckbrief
                            if (person != null) {
                                ArchivTrennlinie(farbe = farben.linieFein)
                                FlowRow(
                                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                                    verticalArrangement = Arrangement.spacedBy(8.dp),
                                ) {
                                    PersonMerkmalStempel("Name", person.vollerName)
                                    PersonMerkmalStempel("Herkunft", person.herkunftTitel)
                                    PersonMerkmalStempel("Jahrgang", "${person.jahrgang} (${person.alter} Jahre 1914)")
                                    PersonMerkmalStempel("Friedensberuf", person.friedensberuf)
                                    PersonMerkmalStempel("Stellung im Krieg", "${person.stand} · $pfadMarke")
                                    if (musterungText != null) {
                                        PersonMerkmalStempel("Musterung", musterungText)
                                    }
                                }
                            }
                        }
                    }
                }

                // 2. Die 4 Fächer des Lebenslaufs
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = farben.papierHell,
                    shape = RoundedCornerShape(4.dp),
                    border = BorderStroke(1.dp, farben.linie),
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(metrik.kartenInnenAbstand),
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
                            ArchivStempel(
                                text = "4-FÄCHER-LEBENSLAUF",
                                farbe = farben.tinte,
                                hintergrund = farben.papierDunkel,
                            )
                            Text(
                                text = "Was diesen Weg geprägt hat",
                                style = MaterialTheme.typography.headlineSmall,
                                color = farben.tinte,
                                modifier = Modifier.archivUeberschrift(),
                            )
                        }

                        val zweispaltig = layoutKlasse != LayoutKlasse.KOMPAKT &&
                            uiState.schriftgroesse != Schriftgroesse.GROSS

                        if (zweispaltig) {
                            lebenslauf.faecher.chunked(2).forEach { paar ->
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(IntrinsicSize.Min),
                                    horizontalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
                                ) {
                                    paar.forEach { fach ->
                                        LebenslaufFachKarte(
                                            fach = fach,
                                            modifier = Modifier
                                                .weight(1f)
                                                .fillMaxHeight(),
                                        )
                                    }
                                    if (paar.size == 1) {
                                        Spacer(modifier = Modifier.weight(1f))
                                    }
                                }
                            }
                        } else {
                            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                                lebenslauf.faecher.forEach { fach ->
                                    LebenslaufFachKarte(
                                        fach = fach,
                                        modifier = Modifier.fillMaxWidth(),
                                    )
                                }
                            }
                        }
                    }
                }

                // 3. Chronologische Zeitleiste
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = farben.papierHell,
                    shape = RoundedCornerShape(4.dp),
                    border = BorderStroke(1.dp, farben.linie),
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(metrik.kartenInnenAbstand),
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
                            ArchivStempel(
                                text = "CHRONOLOGIE",
                                farbe = farben.akzent,
                            )
                            Text(
                                text = "Zeitleiste deines Weges",
                                style = MaterialTheme.typography.headlineSmall,
                                color = farben.tinte,
                                modifier = Modifier.archivUeberschrift(),
                            )
                        }

                        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            lebenslauf.zeitleiste.forEach { eintrag ->
                                ZeitleistenEintragKarte(eintrag = eintrag)
                            }
                        }
                    }
                }

                // 4. Aufklappbares Entscheidungsprotokoll (für Vergleich & Gespräch in der Klasse)
                if (protokollUi.isNotEmpty()) {
                    EntscheidungsProtokollBox(
                        eintraege = protokollUi,
                        analyseModus = uiState.analyseModus,
                    )
                }

                // 5. Abschließende Befindens-Bilanz (ohne Punkte/Noten)
                if (lebenslauf.werteBilanz.isNotEmpty()) {
                    WerteBilanzKarte(
                        werte = lebenslauf.werteBilanz,
                        endJahr = endJahr,
                    )
                }

                // 6. Export- & Druckansicht für das Klassenzimmer (AP 6)
                LebenslaufExportKarte(
                    dokument = exportDokument,
                    bruecke = exportBruecke,
                    hatProtokoll = protokollUi.isNotEmpty(),
                    mitProtokoll = exportMitProtokoll,
                    onMitProtokollToggle = { exportMitProtokoll = !exportMitProtokoll },
                )

                // 7. Neuer Durchgang
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = farben.papierHell,
                    shape = RoundedCornerShape(4.dp),
                    border = BorderStroke(1.25.dp, farben.tinte),
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(metrik.kartenInnenAbstand),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        if (layoutKlasse == LayoutKlasse.KOMPAKT) {
                            Column(
                                modifier = Modifier.fillMaxWidth(),
                                verticalArrangement = Arrangement.spacedBy(10.dp),
                            ) {
                                Text(
                                    text = "Einen anderen Lebensweg zwischen 1914 und 1919 erkunden",
                                    style = MaterialTheme.typography.bodyMedium,
                                    color = farben.tinte,
                                )
                                ArchivPrimaerKnopf(
                                    label = "Neuer Durchgang",
                                    onClick = onNeuerDurchgang,
                                    modifier = Modifier.fillMaxWidth(),
                                )
                            }
                        } else {
                            Column(
                                modifier = Modifier.weight(1f),
                                verticalArrangement = Arrangement.spacedBy(2.dp),
                            ) {
                                Text(
                                    text = "Durchgang abgeschlossen",
                                    style = MaterialTheme.typography.titleMedium,
                                    color = farben.tinte,
                                )
                                Text(
                                    text = "Starte einen neuen Durchgang mit anderer Herkunft, anderem Jahrgang oder anderem Pfad.",
                                    style = MaterialTheme.typography.bodySmall,
                                    color = farben.tinteMatt,
                                )
                            }
                            ArchivPrimaerKnopf(
                                label = "Neuer Durchgang",
                                onClick = onNeuerDurchgang,
                            )
                        }
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
}

/**
 * Klassenzimmer-Exportkarte (AP 6):
 * Druckansicht (A4-Archivblatt), Datei-Download / Teilen, Kopieren in die Zwischenablage
 * sowie eine aufklappbare, markierbare Textvorschau direkt im Bildschirm.
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun LebenslaufExportKarte(
    dokument: LebenslaufExportDokument,
    bruecke: PlattformExportBruecke,
    hatProtokoll: Boolean,
    mitProtokoll: Boolean,
    onMitProtokollToggle: () -> Unit,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val layoutKlasse = ArchivTheme.layoutKlasse
    val reduziert = ArchivTheme.reduzierteAnimationen

    var letztesErgebnis by remember { mutableStateOf<ExportErgebnis?>(null) }
    var textVorschauOffen by remember { mutableStateOf(false) }

    Surface(
        modifier = Modifier.fillMaxWidth(),
        color = farben.papierHell,
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(1.dp, farben.linie),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(metrik.kartenInnenAbstand),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                ArchivStempel(
                    text = "KLASSENZIMMER · AUSWERTUNG & DRUCK",
                    farbe = farben.akzent,
                    hintergrund = farben.papier,
                )
                Text(
                    text = "Lebenslauf sichern oder drucken",
                    style = MaterialTheme.typography.headlineSmall,
                    color = farben.tinte,
                    modifier = Modifier.archivUeberschrift(),
                )
                Text(
                    text = "Bereitet deinen 4-Fächer-Lebenslauf als ruhiges A4-Druckblatt (PDF/Drucker) oder strukturierten Text für Mappe und Unterrichtsgespräch auf.",
                    style = MaterialTheme.typography.bodySmall,
                    color = farben.tinteMatt,
                )
            }

            if (hatProtokoll) {
                ArchivSchalterZeile(
                    titel = "Entscheidungsprotokoll in Export & Druck einschließen",
                    beschreibung = "Listet alle getroffenen Stationen chronologisch mit auf, um Wege in der Klasse zu vergleichen.",
                    aktiv = mitProtokoll,
                    onToggle = onMitProtokollToggle,
                )
            }

            if (layoutKlasse == LayoutKlasse.KOMPAKT) {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    ArchivPrimaerKnopf(
                        label = bruecke.druckenLabel,
                        onClick = { letztesErgebnis = bruecke.drucken(dokument) },
                        modifier = Modifier.fillMaxWidth(),
                    )
                    ArchivSekundaerKnopf(
                        label = bruecke.speichernLabel,
                        onClick = { letztesErgebnis = bruecke.speichernOderTeilen(dokument) },
                        modifier = Modifier.fillMaxWidth(),
                    )
                    ArchivSekundaerKnopf(
                        label = "Als Text kopieren",
                        onClick = { letztesErgebnis = bruecke.kopieren(dokument) },
                        modifier = Modifier.fillMaxWidth(),
                    )
                    ArchivSekundaerKnopf(
                        label = if (textVorschauOffen) "Textvorschau ausblenden" else "Textvorschau anzeigen",
                        onClick = { textVorschauOffen = !textVorschauOffen },
                        modifier = Modifier.fillMaxWidth(),
                    )
                }
            } else {
                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(10.dp),
                    verticalArrangement = Arrangement.spacedBy(10.dp),
                ) {
                    ArchivPrimaerKnopf(
                        label = bruecke.druckenLabel,
                        onClick = { letztesErgebnis = bruecke.drucken(dokument) },
                    )
                    ArchivSekundaerKnopf(
                        label = bruecke.speichernLabel,
                        onClick = { letztesErgebnis = bruecke.speichernOderTeilen(dokument) },
                    )
                    ArchivSekundaerKnopf(
                        label = "Als Text kopieren",
                        onClick = { letztesErgebnis = bruecke.kopieren(dokument) },
                    )
                    ArchivSekundaerKnopf(
                        label = if (textVorschauOffen) "Textvorschau ausblenden" else "Textvorschau anzeigen",
                        onClick = { textVorschauOffen = !textVorschauOffen },
                    )
                }
            }

            // Höfliche Live-Rückmeldung nach Export-, Druck- oder Kopieraktion
            val ergebnis = letztesErgebnis
            if (ergebnis != null) {
                val hinweisFarbe = if (ergebnis.erfolgreich) farben.stufenFarbe(0) else farben.akzent
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .archivLiveHinweis()
                        .background(farben.papier, RoundedCornerShape(3.dp))
                        .border(1.dp, hinweisFarbe.copy(alpha = 0.7f), RoundedCornerShape(3.dp))
                        .padding(horizontal = 12.dp, vertical = 10.dp),
                ) {
                    Text(
                        text = ergebnis.meldung,
                        style = MaterialTheme.typography.bodySmall,
                        color = farben.tinte,
                        fontWeight = FontWeight.Medium,
                    )
                }
            }

            // Aufklappbare, markierbare Klartext-Vorschau (funktioniert auf jedem Schulgerät auch offline)
            AnimatedVisibility(
                visible = textVorschauOffen,
                enter = ArchivUebergaenge.aufklappEnter(reduziert),
                exit = ArchivUebergaenge.aufklappExit(reduziert),
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .border(1.dp, farben.linieFein, RoundedCornerShape(3.dp))
                        .background(farben.papier, RoundedCornerShape(3.dp))
                        .padding(12.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    Text(
                        text = "EXPORT-TEXTVORSCHAU (MARKIERBAR · ${dokument.dateinameBasis}.html)",
                        style = MaterialTheme.typography.labelSmall,
                        color = farben.tinteMatt,
                        fontWeight = FontWeight.SemiBold,
                    )
                    SelectionContainer {
                        Text(
                            text = dokument.klartext,
                            style = MaterialTheme.typography.bodySmall,
                            fontFamily = FontFamily.Monospace,
                            color = farben.tinte,
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun PersonMerkmalStempel(
    feld: String,
    wert: String,
) {
    val farben = ArchivTheme.farben
    Column(
        modifier = Modifier
            .semantics(mergeDescendants = true) {}
            .border(0.75.dp, farben.linieFein, RoundedCornerShape(3.dp))
            .background(farben.papier, RoundedCornerShape(3.dp))
            .padding(horizontal = 10.dp, vertical = 6.dp),
        verticalArrangement = Arrangement.spacedBy(2.dp),
    ) {
        Text(
            text = feld.uppercase(),
            style = MaterialTheme.typography.labelSmall,
            color = farben.tinteMatt,
        )
        Text(
            text = wert,
            style = MaterialTheme.typography.bodySmall,
            color = farben.tinte,
            fontWeight = FontWeight.Medium,
        )
    }
}

@Composable
private fun LebenslaufFachKarte(
    fach: LebenslaufFachErgebnis,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val istGefuellt = fach.merkmalName != null

    Surface(
        modifier = modifier.semantics(mergeDescendants = true) {},
        color = if (istGefuellt) farben.papier else farben.papier.copy(alpha = 0.5f),
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(1.dp, if (istGefuellt) farben.linie else farben.linieFein),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = "FACH ${fach.fachIndex + 1} · ${fach.titel.uppercase()}",
                    style = MaterialTheme.typography.labelSmall,
                    color = farben.akzent,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.weight(1f),
                )
                if (fach.eintrag != null) {
                    ArchivStempel(
                        text = fach.eintrag.datum,
                        farbe = farben.tinteMatt,
                        hintergrund = farben.papierHell,
                    )
                }
            }

            if (istGefuellt) {
                Text(
                    text = fach.merkmalName.orEmpty(),
                    style = MaterialTheme.typography.titleMedium,
                    fontFamily = FontFamily.Serif,
                    color = farben.tinte,
                    fontWeight = FontWeight.Bold,
                )
                if (fach.eintrag != null) {
                    Text(
                        text = fach.eintrag.text,
                        style = MaterialTheme.typography.bodyMedium,
                        color = farben.tinte,
                    )
                }
            } else {
                Text(
                    text = "Kein einzelner Schwerpunkt vermerkt.",
                    style = MaterialTheme.typography.bodyMedium,
                    fontStyle = FontStyle.Italic,
                    color = farben.tinteMatt,
                )
            }
        }
    }
}

@Composable
private fun ZeitleistenEintragKarte(
    eintrag: LebenslaufZeitleistenEintrag,
) {
    val farben = ArchivTheme.farben

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .semantics(mergeDescendants = true) {}
            .border(1.dp, farben.linieFein, RoundedCornerShape(3.dp))
            .background(farben.papier, RoundedCornerShape(3.dp))
            .height(IntrinsicSize.Min),
    ) {
        Box(
            modifier = Modifier
                .width(4.dp)
                .fillMaxHeight()
                .background(farben.akzent.copy(alpha = 0.72f)),
        )
        Column(
            modifier = Modifier
                .weight(1f)
                .padding(12.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                ArchivStempel(
                    text = eintrag.datum,
                    farbe = farben.tinte,
                    hintergrund = farben.papierHell,
                )
                Text(
                    text = eintrag.quelle,
                    style = MaterialTheme.typography.labelSmall,
                    color = farben.tinteMatt,
                )
            }
            Text(
                text = eintrag.text,
                style = MaterialTheme.typography.bodyMedium,
                color = farben.tinte,
            )
        }
    }
}

@Composable
private fun EntscheidungsProtokollBox(
    eintraege: List<ProtokollUiEintrag>,
    analyseModus: Boolean,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val reduziert = ArchivTheme.reduzierteAnimationen
    var aufgeklappt by remember { mutableStateOf(analyseModus) }

    LaunchedEffect(analyseModus) {
        if (analyseModus) aufgeklappt = true
    }

    Surface(
        modifier = Modifier.fillMaxWidth(),
        color = farben.papierHell,
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(1.dp, farben.linie),
    ) {
        Column(modifier = Modifier.fillMaxWidth()) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .defaultMinSize(minHeight = metrik.minTouchHoehe)
                    .archivFokusRahmen(eckRadius = 4.dp, aufDunkel = false)
                    .clickable { aufgeklappt = !aufgeklappt }
                    .clearAndSetSemantics {
                        role = Role.Button
                        selected = aufgeklappt
                        stateDescription = if (aufgeklappt) "Aufgeklappt" else "Zugeklappt"
                        contentDescription = if (aufgeklappt) {
                            "Chronologische Entscheidungsliste (${eintraege.size} Stationen) zuklappen"
                        } else {
                            "Chronologische Entscheidungsliste (${eintraege.size} Stationen) aufklappen"
                        }
                    }
                    .padding(horizontal = metrik.kartenInnenAbstand, vertical = 12.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = "Deine Entscheidungen im Überblick (${eintraege.size} Stationen)",
                        style = MaterialTheme.typography.titleMedium,
                        color = farben.tinte,
                    )
                    Text(
                        text = "Zum Nachlesen und Vergleichen im Unterricht aufklappen.",
                        style = MaterialTheme.typography.bodySmall,
                        color = farben.tinteMatt,
                    )
                }
                Text(
                    text = if (aufgeklappt) "Zuklappen ▴" else "Aufklappen ▾",
                    style = MaterialTheme.typography.labelSmall,
                    color = farben.tinteMatt,
                )
            }

            AnimatedVisibility(
                visible = aufgeklappt,
                enter = ArchivUebergaenge.aufklappEnter(reduziert),
                exit = ArchivUebergaenge.aufklappExit(reduziert),
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(farben.papier.copy(alpha = 0.65f))
                        .padding(metrik.kartenInnenAbstand),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    eintraege.forEach { eintrag ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .semantics(mergeDescendants = true) {}
                                .border(0.75.dp, farben.linieFein, RoundedCornerShape(3.dp))
                                .background(farben.papierHell, RoundedCornerShape(3.dp))
                                .padding(horizontal = 10.dp, vertical = 8.dp),
                            horizontalArrangement = Arrangement.spacedBy(10.dp),
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            ArchivStempel(
                                text = eintrag.jahr.toString(),
                                farbe = farben.tinteMatt,
                                hintergrund = farben.papier,
                            )
                            Column(
                                modifier = Modifier.weight(1f),
                                verticalArrangement = Arrangement.spacedBy(2.dp),
                            ) {
                                Text(
                                    text = eintrag.station,
                                    style = MaterialTheme.typography.labelMedium,
                                    color = farben.tinteMatt,
                                )
                                Text(
                                    text = eintrag.wahl,
                                    style = MaterialTheme.typography.bodyMedium,
                                    color = farben.tinte,
                                    fontWeight = FontWeight.Medium,
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun WerteBilanzKarte(
    werte: List<WertStatus>,
    endJahr: Int,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val spalten = if (ArchivTheme.layoutKlasse == LayoutKlasse.KOMPAKT) 1 else 2

    Surface(
        modifier = Modifier.fillMaxWidth(),
        color = farben.papierHell,
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(1.dp, farben.linie),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(metrik.kartenInnenAbstand),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Text(
                text = "Befindensstand am Ende ($endJahr)",
                style = MaterialTheme.typography.titleLarge,
                color = farben.tinte,
                modifier = Modifier.archivUeberschrift(),
            )

            werte.chunked(spalten).forEach { zeile ->
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(10.dp),
                ) {
                    zeile.forEach { status ->
                        val stufenFarbe = farben.stufenFarbe(status.stufe)
                        Column(
                            modifier = Modifier
                                .weight(1f)
                                .semantics(mergeDescendants = true) {}
                                .border(0.75.dp, farben.linieFein, RoundedCornerShape(3.dp))
                                .background(farben.papier, RoundedCornerShape(3.dp))
                                .padding(10.dp),
                            verticalArrangement = Arrangement.spacedBy(6.dp),
                        ) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically,
                            ) {
                                Text(
                                    text = status.bezeichnung,
                                    style = MaterialTheme.typography.titleSmall,
                                    color = farben.tinte,
                                )
                                ArchivStempel(
                                    text = status.stufenName,
                                    farbe = stufenFarbe,
                                    hintergrund = farben.papierHell,
                                )
                            }
                            FuenfSegmentBalken(
                                gefuellteSegmente = status.gefuellteSegmente,
                                segmenteGesamt = status.segmenteGesamt,
                                aktiveFarbe = stufenFarbe,
                                leereFarbe = farben.segmentLeer,
                            )
                            Text(
                                text = status.stufenKurz,
                                style = MaterialTheme.typography.bodySmall,
                                color = farben.tinteMatt,
                            )
                        }
                    }
                    repeat(spalten - zeile.size) {
                        Spacer(modifier = Modifier.weight(1f))
                    }
                }
            }
        }
    }
}
