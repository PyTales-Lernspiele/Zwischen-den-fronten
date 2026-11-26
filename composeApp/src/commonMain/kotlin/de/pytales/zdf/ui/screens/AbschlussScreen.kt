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
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
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
import androidx.compose.ui.draw.clip
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
import de.pytales.zdf.ui.components.ArchivZierLinie
import de.pytales.zdf.ui.components.ChevronIcon
import de.pytales.zdf.ui.components.FuenfSegmentBalken
import de.pytales.zdf.ui.components.archivFokusGruppe
import de.pytales.zdf.ui.components.archivFokusRahmen
import de.pytales.zdf.ui.components.archivLiveHinweis
import de.pytales.zdf.ui.components.archivPapierHintergrund
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.export.ExportErgebnis
import de.pytales.zdf.ui.export.LebenslaufExportDokument
import de.pytales.zdf.ui.export.LebenslaufExporter
import de.pytales.zdf.ui.export.PlattformExportBruecke
import de.pytales.zdf.ui.export.rememberPlattformExportBruecke
import de.pytales.zdf.ui.media.ArchivPortraitBild
import de.pytales.zdf.ui.state.ProtokollUiEintrag
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.state.UiStateMapper
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.ArchivUebergaenge
import de.pytales.zdf.ui.theme.LayoutKlasse

/**
 * Schlussbildschirm (`GamePhase.Abgeschlossen`):
 * - Bei vorzeitigem Abbruch (`hartesEnde != null && !auffangnetzBestaetigt`): ruhiges,
 *   respektvolles Auffangnetz mit historischer Einordnung (kein Game-Over-Schock, kein Punktestand)
 * - Danach bzw. bei regulärem Erreichen von 1919: luftiger, ruhig gesetzter **4-Fächer-Lebenslauf**
 *   mit Portrait, Personendaten, historischem Ausgang, allen 4 Fächern, chronologischer Zeitleiste,
 *   aufklappbarem Entscheidungsweg, Wertebilanz, Druck-/Export-Werkzeug und „Neuer Durchgang“.
 */
@Composable
fun AbschlussScreen(
    engine: GameEngine,
    uiState: SpielUiState,
    phase: GamePhase.Abgeschlossen,
    onAuffangnetzBestaetigen: () -> Unit,
    onNeuerDurchgang: () -> Unit,
    onAudioToggle: () -> Unit,
    onEinstellungenOeffnen: () -> Unit,
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
            onAudioToggle = onAudioToggle,
            onEinstellungenOeffnen = onEinstellungenOeffnen,
            modifier = modifier,
        )
    } else {
        LebenslaufAnsicht(
            engine = engine,
            uiState = uiState,
            phase = phase,
            onNeuerDurchgang = onNeuerDurchgang,
            onAudioToggle = onAudioToggle,
            onEinstellungenOeffnen = onEinstellungenOeffnen,
            modifier = modifier,
        )
    }
}

/**
 * Ruhiges, respektvolles Auffangnetz bei vorzeitigem Einschnitt vor 1919
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
    onAudioToggle: () -> Unit,
    onEinstellungenOeffnen: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val kompakt = metrik.kompakteHoehe
    val person = uiState.gameState.person
    val pfadMarke = engine.content.konfiguration.pfade.definitionen[uiState.gameState.pfad]?.marke
        ?: uiState.gameState.pfad.code

    Column(
        modifier = modifier
            .fillMaxSize()
            .archivPapierHintergrund(),
    ) {
        ArchivKopfBand(
            marke = "Jahr ${hartesEnde.jahr}",
            titel = "Dein Weg endet vor 1919",
            untertitel = listOfNotNull(person?.vollerName, pfadMarke).joinToString(" · "),
            audioZustand = uiState.audioZustand,
            onAudioToggle = onAudioToggle,
            onEinstellungenOeffnen = onEinstellungenOeffnen,
        )

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .verticalScroll(rememberScrollState()),
            contentAlignment = Alignment.Center,
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .archivInhaltsSafeArea()
                    .widthIn(max = 920.dp)
                    .padding(horizontal = metrik.aussenAbstand, vertical = if (kompakt) 12.dp else 20.dp)
                    .archivFokusGruppe(),
            ) {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = farben.papierHell,
                    shape = RoundedCornerShape(6.dp),
                    border = BorderStroke(0.75.dp, farben.linieFein.copy(alpha = 0.85f)),
                    shadowElevation = 2.dp,
                ) {
                    Column(modifier = Modifier.fillMaxWidth()) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(2.5.dp)
                                .background(farben.tinteMatt),
                        )

                        val erzaehlSpalte: @Composable (Modifier) -> Unit = { mod ->
                            Column(
                                modifier = mod,
                                verticalArrangement = Arrangement.spacedBy(10.dp),
                            ) {
                                Text(
                                    text = "${hartesEnde.jahr} · $pfadMarke",
                                    style = MaterialTheme.typography.labelMedium,
                                    fontFamily = FontFamily.Serif,
                                    color = farben.tinteMatt,
                                )
                                Text(
                                    text = hartesEnde.titel,
                                    style = if (kompakt) MaterialTheme.typography.headlineMedium else MaterialTheme.typography.headlineLarge,
                                    color = farben.tinte,
                                    modifier = Modifier.archivUeberschrift(),
                                )
                                Text(
                                    text = hartesEnde.text,
                                    style = MaterialTheme.typography.bodyLarge,
                                    color = farben.tinte,
                                )
                            }
                        }

                        val einordnungsSpalte: @Composable (Modifier) -> Unit = { mod ->
                            Column(
                                modifier = mod,
                                verticalArrangement = Arrangement.spacedBy(12.dp),
                            ) {
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(IntrinsicSize.Min)
                                        .background(farben.papier.copy(alpha = 0.72f), RoundedCornerShape(5.dp)),
                                ) {
                                    Box(
                                        modifier = Modifier
                                            .width(2.5.dp)
                                            .fillMaxHeight()
                                            .background(farben.tinteMatt),
                                    )
                                    Column(
                                        modifier = Modifier
                                            .weight(1f)
                                            .padding(horizontal = 12.dp, vertical = 10.dp),
                                        verticalArrangement = Arrangement.spacedBy(5.dp),
                                    ) {
                                        Text(
                                            text = "Kein persönliches Versagen",
                                            style = MaterialTheme.typography.titleSmall,
                                            fontFamily = FontFamily.Serif,
                                            color = farben.tinte,
                                        )
                                        Text(
                                            text = fazit,
                                            style = MaterialTheme.typography.bodySmall,
                                            color = farben.tinte,
                                        )
                                        Text(
                                            text = "Dein bisheriger Weg bleibt im Lebenslauf vollständig erhalten.",
                                            style = MaterialTheme.typography.bodySmall,
                                            fontStyle = FontStyle.Italic,
                                            color = farben.tinteMatt,
                                        )
                                    }
                                }

                                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
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
                            }
                        }

                        if (metrik.zweispaltigeBuehne) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(metrik.kartenInnenAbstand),
                                horizontalArrangement = Arrangement.spacedBy(if (kompakt) 18.dp else 26.dp),
                                verticalAlignment = Alignment.Top,
                            ) {
                                erzaehlSpalte(Modifier.weight(0.54f))
                                einordnungsSpalte(Modifier.weight(0.46f))
                            }
                        } else {
                            Column(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(metrik.kartenInnenAbstand),
                                verticalArrangement = Arrangement.spacedBy(14.dp),
                            ) {
                                erzaehlSpalte(Modifier.fillMaxWidth())
                                ArchivTrennlinie()
                                einordnungsSpalte(Modifier.fillMaxWidth())
                            }
                        }
                    }
                }
            }
        }
    }
}

/**
 * Ruhiger, übersichtlicher 4-Fächer-Lebenslauf im Querformat-Buchdruck-Stil.
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun LebenslaufAnsicht(
    engine: GameEngine,
    uiState: SpielUiState,
    phase: GamePhase.Abgeschlossen,
    onNeuerDurchgang: () -> Unit,
    onAudioToggle: () -> Unit,
    onEinstellungenOeffnen: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val kompakt = metrik.kompakteHoehe
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
    val emotionUi = remember(engine, gameState) {
        UiStateMapper.mapLiveEmotion(engine, gameState)
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

    var exportMitProtokoll by remember { mutableStateOf(true) }
    val exportDokument = remember(engine.content, gameState, phase, exportMitProtokoll) {
        LebenslaufExporter.erstelleDokument(
            content = engine.content,
            gameState = gameState,
            phase = phase,
            mitProtokoll = exportMitProtokoll,
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
            .archivPapierHintergrund(),
    ) {
        ArchivKopfBand(
            marke = "Lebenslauf $zeitspanne",
            titel = person?.vollerName?.ifBlank { null } ?: "Abgeschlossener Lebenslauf",
            untertitel = listOfNotNull(
                person?.herkunftTitel?.ifBlank { null },
                person?.let { "Jg. ${it.jahrgang}" },
                pfadMarke,
            ).joinToString(" · "),
            audioZustand = uiState.audioZustand,
            onAudioToggle = onAudioToggle,
            onEinstellungenOeffnen = onEinstellungenOeffnen,
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
                    .archivInhaltsSafeArea()
                    .widthIn(max = metrik.maxInhaltsBreite)
                    .padding(
                        horizontal = metrik.aussenAbstand,
                        vertical = if (kompakt) 10.dp else 18.dp,
                    )
                    .archivFokusGruppe(),
                verticalArrangement = Arrangement.spacedBy(if (kompakt) 12.dp else 18.dp),
            ) {
                // 1. Ausgang & Personenblatt (im Querformat zweispaltig mit Stil-A-Portrait)
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = farben.papierHell,
                    shape = RoundedCornerShape(6.dp),
                    border = BorderStroke(0.75.dp, farben.linieFein.copy(alpha = 0.85f)),
                    shadowElevation = 2.dp,
                ) {
                    Column(modifier = Modifier.fillMaxWidth()) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(2.5.dp)
                                .background(if (lebenslauf.istVorzeitigerAbbruch) farben.tinteMatt else farben.akzent),
                        )

                        val ausgangSpalte: @Composable (Modifier) -> Unit = { mod ->
                            Column(
                                modifier = mod,
                                verticalArrangement = Arrangement.spacedBy(8.dp),
                            ) {
                                Text(
                                    text = if (lebenslauf.istVorzeitigerAbbruch) {
                                        "Vorzeitiger Einschnitt · $endJahr"
                                    } else {
                                        "Historischer Ausgang · 1919"
                                    },
                                    style = MaterialTheme.typography.labelMedium,
                                    fontFamily = FontFamily.Serif,
                                    color = if (lebenslauf.istVorzeitigerAbbruch) farben.tinteMatt else farben.akzent,
                                    fontWeight = FontWeight.SemiBold,
                                )

                                val ausgang = lebenslauf.ausgang
                                val hartesEnde = lebenslauf.hartesEnde
                                when {
                                    ausgang != null -> {
                                        Text(
                                            text = ausgang.titel,
                                            style = if (kompakt) MaterialTheme.typography.headlineMedium else MaterialTheme.typography.headlineLarge,
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
                                            style = MaterialTheme.typography.bodyMedium,
                                            color = farben.tinte,
                                        )
                                    }

                                    hartesEnde != null -> {
                                        Text(
                                            text = "${hartesEnde.titel} ($endJahr)",
                                            style = if (kompakt) MaterialTheme.typography.headlineMedium else MaterialTheme.typography.headlineLarge,
                                            color = farben.tinte,
                                            modifier = Modifier.archivUeberschrift(),
                                        )
                                        Text(
                                            text = hartesEnde.text,
                                            style = MaterialTheme.typography.bodyMedium,
                                            color = farben.tinte,
                                        )
                                        Text(
                                            text = lebenslauf.fazit,
                                            style = MaterialTheme.typography.bodySmall,
                                            fontStyle = FontStyle.Italic,
                                            color = farben.tinteMatt,
                                        )
                                    }
                                }
                            }
                        }

                        val steckbriefSpalte: @Composable (Modifier) -> Unit = { mod ->
                            Column(
                                modifier = mod,
                                verticalArrangement = Arrangement.spacedBy(8.dp),
                            ) {
                                if (person != null) {
                                    Row(
                                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                                        verticalAlignment = Alignment.CenterVertically,
                                    ) {
                                        Box(
                                            modifier = Modifier
                                                .size(if (kompakt) 60.dp else 72.dp)
                                                .clip(RoundedCornerShape(5.dp))
                                                .background(farben.papier)
                                                .border(0.75.dp, farben.linieFein, RoundedCornerShape(5.dp)),
                                        ) {
                                            ArchivPortraitBild(
                                                portraitId = emotionUi.portraitId,
                                                stimmungsFarbe = farben.akzent,
                                                beschreibung = "Portrait von ${person.vollerName}",
                                            ) {}
                                        }
                                        Column(
                                            modifier = Modifier.weight(1f),
                                            verticalArrangement = Arrangement.spacedBy(2.dp),
                                        ) {
                                            Text(
                                                text = person.vollerName,
                                                style = MaterialTheme.typography.titleMedium,
                                                fontFamily = FontFamily.Serif,
                                                color = farben.tinte,
                                                fontWeight = FontWeight.Bold,
                                            )
                                            Text(
                                                text = "${person.herkunftTitel} · Jg. ${person.jahrgang}",
                                                style = MaterialTheme.typography.bodySmall,
                                                color = farben.tinteMatt,
                                            )
                                            Text(
                                                text = "$modusBezeichnung · $pfadMarke",
                                                style = MaterialTheme.typography.labelSmall,
                                                color = farben.tinteMatt,
                                            )
                                        }
                                    }

                                    ArchivTrennlinie(farbe = farben.linieFein.copy(alpha = 0.6f))

                                    SteckbriefZeile("Friedensberuf", person.friedensberuf)
                                    SteckbriefZeile("Stellung im Krieg", person.stand)
                                    if (musterungText != null) {
                                        SteckbriefZeile("Musterung", musterungText)
                                    }
                                }
                            }
                        }

                        if (metrik.zweispaltigeBuehne) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(metrik.kartenInnenAbstand),
                                horizontalArrangement = Arrangement.spacedBy(if (kompakt) 18.dp else 26.dp),
                                verticalAlignment = Alignment.Top,
                            ) {
                                ausgangSpalte(Modifier.weight(0.56f))
                                steckbriefSpalte(Modifier.weight(0.44f))
                            }
                        } else {
                            Column(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(metrik.kartenInnenAbstand),
                                verticalArrangement = Arrangement.spacedBy(12.dp),
                            ) {
                                ausgangSpalte(Modifier.fillMaxWidth())
                                ArchivTrennlinie()
                                steckbriefSpalte(Modifier.fillMaxWidth())
                            }
                        }
                    }
                }

                // 2. Die 4 Fächer des Lebenslaufs (sauberes 2×2-Raster im Querformat)
                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text(
                        text = "Was diesen Weg geprägt hat",
                        style = MaterialTheme.typography.headlineSmall,
                        color = farben.tinte,
                        modifier = Modifier.archivUeberschrift(),
                    )

                    if (metrik.zweispaltigeBuehne) {
                        lebenslauf.faecher.chunked(2).forEach { paar ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(IntrinsicSize.Min),
                                horizontalArrangement = Arrangement.spacedBy(if (kompakt) 10.dp else 14.dp),
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

                // 3. Chronologische Zeitleiste & Befindensstand
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = farben.papierHell,
                    shape = RoundedCornerShape(6.dp),
                    border = BorderStroke(0.75.dp, farben.linieFein.copy(alpha = 0.85f)),
                    shadowElevation = 1.dp,
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(metrik.kartenInnenAbstand),
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        Text(
                            text = "Zeitleiste deines Weges",
                            style = MaterialTheme.typography.headlineSmall,
                            color = farben.tinte,
                            modifier = Modifier.archivUeberschrift(),
                        )

                        Column(verticalArrangement = Arrangement.spacedBy(0.dp)) {
                            lebenslauf.zeitleiste.forEachIndexed { idx, eintrag ->
                                ZeitleistenEintragZeile(
                                    eintrag = eintrag,
                                    istLetzter = idx == lebenslauf.zeitleiste.lastIndex,
                                )
                            }
                        }

                        if (lebenslauf.werteBilanz.isNotEmpty()) {
                            ArchivZierLinie()
                            WerteBilanzBlock(
                                werte = lebenslauf.werteBilanz,
                                endJahr = endJahr,
                            )
                        }
                    }
                }

                // 4. Aufklappbarer Entscheidungsweg
                if (protokollUi.isNotEmpty()) {
                    EntscheidungsProtokollBox(eintraege = protokollUi)
                }

                // 5. Lebenslauf drucken/sichern & Neuer Durchgang
                LebenslaufExportUndNeustartKarte(
                    dokument = exportDokument,
                    bruecke = exportBruecke,
                    hatProtokoll = protokollUi.isNotEmpty(),
                    mitProtokoll = exportMitProtokoll,
                    onMitProtokollToggle = { exportMitProtokoll = !exportMitProtokoll },
                    onNeuerDurchgang = onNeuerDurchgang,
                )

                Spacer(modifier = Modifier.height(14.dp))
            }
        }
    }
}

@Composable
private fun SteckbriefZeile(
    feld: String,
    wert: String,
) {
    val farben = ArchivTheme.farben
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .semantics(mergeDescendants = true) {},
        horizontalArrangement = Arrangement.spacedBy(10.dp),
    ) {
        Text(
            text = feld,
            style = MaterialTheme.typography.labelSmall,
            color = farben.tinteMatt,
            modifier = Modifier.widthIn(min = 104.dp, max = 120.dp),
        )
        Text(
            text = wert,
            style = MaterialTheme.typography.bodySmall,
            color = farben.tinte,
            modifier = Modifier.weight(1f),
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
        color = if (istGefuellt) farben.papierHell else farben.papierHell.copy(alpha = 0.55f),
        shape = RoundedCornerShape(6.dp),
        border = BorderStroke(0.75.dp, farben.linieFein.copy(alpha = 0.85f)),
        shadowElevation = if (istGefuellt) 1.dp else 0.dp,
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 14.dp, vertical = 12.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = fach.titel,
                    style = MaterialTheme.typography.labelMedium,
                    fontFamily = FontFamily.Serif,
                    color = farben.akzent,
                    fontWeight = FontWeight.SemiBold,
                    modifier = Modifier.weight(1f),
                )
                if (fach.eintrag != null) {
                    Text(
                        text = fach.eintrag.datum,
                        style = MaterialTheme.typography.labelSmall,
                        color = farben.tinteMatt,
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
                        style = MaterialTheme.typography.bodySmall,
                        color = farben.tinte,
                    )
                }
            } else {
                Text(
                    text = "Kein einzelner Schwerpunkt vermerkt.",
                    style = MaterialTheme.typography.bodySmall,
                    fontStyle = FontStyle.Italic,
                    color = farben.tinteMatt,
                )
            }
        }
    }
}

@Composable
private fun ZeitleistenEintragZeile(
    eintrag: LebenslaufZeitleistenEintrag,
    istLetzter: Boolean,
) {
    val farben = ArchivTheme.farben

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .semantics(mergeDescendants = true) {}
            .height(IntrinsicSize.Min),
        horizontalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        // Feine durchgehende Sepia-Zeitlinie mit Punkt
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier.fillMaxHeight(),
        ) {
            Box(
                modifier = Modifier
                    .padding(top = 6.dp)
                    .size(8.dp)
                    .clip(CircleShape)
                    .background(farben.akzent),
            )
            if (!istLetzter) {
                Box(
                    modifier = Modifier
                        .width(1.dp)
                        .weight(1f)
                        .background(farben.linieFein),
                )
            }
        }

        Column(
            modifier = Modifier
                .weight(1f)
                .padding(bottom = if (istLetzter) 2.dp else 12.dp),
            verticalArrangement = Arrangement.spacedBy(2.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = eintrag.datum,
                    style = MaterialTheme.typography.labelMedium,
                    fontFamily = FontFamily.Serif,
                    color = farben.tinte,
                    fontWeight = FontWeight.SemiBold,
                )
                Text(
                    text = eintrag.quelle,
                    style = MaterialTheme.typography.labelSmall,
                    color = farben.tinteMatt,
                )
            }
            Text(
                text = eintrag.text,
                style = MaterialTheme.typography.bodySmall,
                color = farben.tinte,
            )
        }
    }
}

@Composable
private fun WerteBilanzBlock(
    werte: List<WertStatus>,
    endJahr: Int,
) {
    val farben = ArchivTheme.farben
    val spalten = if (ArchivTheme.layoutKlasse == LayoutKlasse.KOMPAKT) 1 else 2

    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Text(
            text = "Befindensstand ($endJahr)",
            style = MaterialTheme.typography.titleLarge,
            color = farben.tinte,
            modifier = Modifier.archivUeberschrift(),
        )

        werte.chunked(spalten).forEach { zeile ->
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(14.dp),
            ) {
                zeile.forEach { status ->
                    val stufenFarbe = farben.stufenFarbe(status.stufe)
                    Column(
                        modifier = Modifier
                            .weight(1f)
                            .semantics(mergeDescendants = true) {}
                            .background(farben.papier.copy(alpha = 0.55f), RoundedCornerShape(5.dp))
                            .padding(horizontal = 12.dp, vertical = 9.dp),
                        verticalArrangement = Arrangement.spacedBy(5.dp),
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

@Composable
private fun EntscheidungsProtokollBox(
    eintraege: List<ProtokollUiEintrag>,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val reduziert = ArchivTheme.reduzierteAnimationen
    var aufgeklappt by remember { mutableStateOf(false) }

    Surface(
        modifier = Modifier.fillMaxWidth(),
        color = farben.papierHell,
        shape = RoundedCornerShape(6.dp),
        border = BorderStroke(0.75.dp, farben.linieFein.copy(alpha = 0.85f)),
    ) {
        Column(modifier = Modifier.fillMaxWidth()) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .defaultMinSize(minHeight = metrik.minTouchHoehe)
                    .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = false)
                    .clickable { aufgeklappt = !aufgeklappt }
                    .clearAndSetSemantics {
                        role = Role.Button
                        selected = aufgeklappt
                        stateDescription = if (aufgeklappt) "Aufgeklappt" else "Zugeklappt"
                        contentDescription = if (aufgeklappt) {
                            "Entscheidungen im Überblick (${eintraege.size} Stationen) zuklappen"
                        } else {
                            "Entscheidungen im Überblick (${eintraege.size} Stationen) aufklappen"
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
                        fontFamily = FontFamily.Serif,
                        color = farben.tinte,
                    )
                    Text(
                        text = "Zum Nachlesen und Vergleichen aufklappen.",
                        style = MaterialTheme.typography.bodySmall,
                        color = farben.tinteMatt,
                    )
                }
                ChevronIcon(
                    nachOben = aufgeklappt,
                    farbe = farben.tinteMatt,
                    groesse = 16.dp,
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
                        .padding(horizontal = metrik.kartenInnenAbstand)
                        .padding(bottom = 14.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    ArchivTrennlinie()
                    eintraege.forEachIndexed { idx, eintrag ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .semantics(mergeDescendants = true) {}
                                .padding(vertical = 3.dp),
                            horizontalArrangement = Arrangement.spacedBy(12.dp),
                            verticalAlignment = Alignment.Top,
                        ) {
                            Text(
                                text = eintrag.jahr.toString(),
                                style = MaterialTheme.typography.labelMedium,
                                fontFamily = FontFamily.Serif,
                                color = farben.akzent,
                                fontWeight = FontWeight.SemiBold,
                            )
                            Column(
                                modifier = Modifier.weight(1f),
                                verticalArrangement = Arrangement.spacedBy(1.dp),
                            ) {
                                Text(
                                    text = eintrag.wahl,
                                    style = MaterialTheme.typography.bodyMedium,
                                    color = farben.tinte,
                                    fontWeight = FontWeight.Medium,
                                )
                                Text(
                                    text = eintrag.station,
                                    style = MaterialTheme.typography.labelSmall,
                                    color = farben.tinteMatt,
                                )
                            }
                        }
                        if (idx < eintraege.lastIndex) {
                            ArchivTrennlinie(farbe = farben.linieFein.copy(alpha = 0.45f))
                        }
                    }
                }
            }
        }
    }
}

/**
 * Ruhige Abschluss-Karte für Lebenslauf-Druck, Export/Kopieren und „Neuer Durchgang“.
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun LebenslaufExportUndNeustartKarte(
    dokument: LebenslaufExportDokument,
    bruecke: PlattformExportBruecke,
    hatProtokoll: Boolean,
    mitProtokoll: Boolean,
    onMitProtokollToggle: () -> Unit,
    onNeuerDurchgang: () -> Unit,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val reduziert = ArchivTheme.reduzierteAnimationen

    var letztesErgebnis by remember { mutableStateOf<ExportErgebnis?>(null) }
    var textVorschauOffen by remember { mutableStateOf(false) }

    Surface(
        modifier = Modifier.fillMaxWidth(),
        color = farben.papierHell,
        shape = RoundedCornerShape(6.dp),
        border = BorderStroke(0.75.dp, farben.linieFein.copy(alpha = 0.85f)),
        shadowElevation = 1.dp,
    ) {
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
                Column(
                    modifier = Modifier.weight(1f),
                    verticalArrangement = Arrangement.spacedBy(2.dp),
                ) {
                    Text(
                        text = "Lebenslauf sichern oder drucken",
                        style = MaterialTheme.typography.headlineSmall,
                        color = farben.tinte,
                        modifier = Modifier.archivUeberschrift(),
                    )
                    Text(
                        text = "Als ruhiges A4-Druckblatt oder Text für Mappe und Gespräch.",
                        style = MaterialTheme.typography.bodySmall,
                        color = farben.tinteMatt,
                    )
                }

                if (metrik.zweispaltigeBuehne) {
                    ArchivPrimaerKnopf(
                        label = "Neuer Durchgang",
                        akzentStil = true,
                        onClick = onNeuerDurchgang,
                    )
                }
            }

            if (hatProtokoll) {
                ArchivSchalterZeile(
                    titel = "Entscheidungsprotokoll einschließen",
                    beschreibung = "Alle Stationen mit in Druckblatt und Text übernehmen.",
                    aktiv = mitProtokoll,
                    onToggle = onMitProtokollToggle,
                )
            }

            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
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
                    label = if (textVorschauOffen) "Vorschau ausblenden" else "Textvorschau",
                    onClick = { textVorschauOffen = !textVorschauOffen },
                )
            }

            val ergebnis = letztesErgebnis
            if (ergebnis != null) {
                val hinweisFarbe = if (ergebnis.erfolgreich) farben.stufenFarbe(0) else farben.akzent
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(IntrinsicSize.Min)
                        .archivLiveHinweis()
                        .background(farben.papier.copy(alpha = 0.72f), RoundedCornerShape(4.dp)),
                ) {
                    Box(
                        modifier = Modifier
                            .width(2.5.dp)
                            .fillMaxHeight()
                            .background(hinweisFarbe),
                    )
                    Text(
                        text = ergebnis.meldung,
                        style = MaterialTheme.typography.bodySmall,
                        color = farben.tinte,
                        modifier = Modifier
                            .weight(1f)
                            .padding(horizontal = 12.dp, vertical = 8.dp),
                    )
                }
            }

            AnimatedVisibility(
                visible = textVorschauOffen,
                enter = ArchivUebergaenge.aufklappEnter(reduziert),
                exit = ArchivUebergaenge.aufklappExit(reduziert),
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(farben.papier, RoundedCornerShape(5.dp))
                        .border(0.75.dp, farben.linieFein, RoundedCornerShape(5.dp))
                        .padding(12.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp),
                ) {
                    Text(
                        text = "Markierbare Textvorschau",
                        style = MaterialTheme.typography.labelSmall,
                        color = farben.tinteMatt,
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

            if (!metrik.zweispaltigeBuehne) {
                ArchivTrennlinie()
                ArchivPrimaerKnopf(
                    label = "Neuer Durchgang",
                    akzentStil = true,
                    onClick = onNeuerDurchgang,
                    modifier = Modifier.fillMaxWidth(),
                )
            }
        }
    }
}
