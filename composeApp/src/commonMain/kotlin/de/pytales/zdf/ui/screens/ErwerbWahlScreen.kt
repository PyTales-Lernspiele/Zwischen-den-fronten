package de.pytales.zdf.ui.screens

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
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.clearAndSetSemantics
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.components.ArchivStempel
import de.pytales.zdf.ui.components.ArchivTrennlinie
import de.pytales.zdf.ui.components.archivFokusGruppe
import de.pytales.zdf.ui.components.archivFokusRahmen
import de.pytales.zdf.ui.components.archivLiveHinweis
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.state.ErwerbOptionUiState
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.state.UiStateMapper
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.LayoutKlasse
import de.pytales.zdf.ui.theme.Schriftgroesse

/**
 * Erwerbswahl im August 1914 (`GamePhase.ErwerbWahl`) für Figuren in der Heimat:
 * zeigt die für Herkunft, Geschlecht und Musterungsstatus verfügbaren Tätigkeiten
 * inklusive historischer Einordnungs-Stempel aus `GameEngine.erwerbHinweis(...)`.
 */
@Composable
fun ErwerbWahlScreen(
    engine: GameEngine,
    uiState: SpielUiState,
    phase: GamePhase.ErwerbWahl,
    onErwerbMarkieren: (String) -> Unit,
    onBestaetigen: () -> Unit,
    onSchriftgroesseChange: (Schriftgroesse) -> Unit,
    onAnalyseModusToggle: () -> Unit,
    onAudioToggle: () -> Unit = {},
    onWertErklaerungChange: (WertSchluessel?) -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val layoutKlasse = ArchivTheme.layoutKlasse
    val zweispaltig = layoutKlasse != LayoutKlasse.KOMPAKT && uiState.schriftgroesse != Schriftgroesse.GROSS

    val optionenUi = remember(engine, uiState.gameState, phase.optionen) {
        UiStateMapper.mapErwerbOptionen(engine, uiState.gameState, phase.optionen)
    }
    val ausgewaehlt = optionenUi.firstOrNull { it.id == uiState.ausgewaehlterErwerbId }
    val person = uiState.gameState.person

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(farben.papier),
    ) {
        SpielKopfLeiste(
            engine = engine,
            uiState = uiState,
            onSchriftgroesseChange = onSchriftgroesseChange,
            onAnalyseModusToggle = onAnalyseModusToggle,
            onAudioToggle = onAudioToggle,
            onWertErklaerungChange = onWertErklaerungChange,
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
                    .widthIn(max = metrik.maxInhaltsBreite)
                    .padding(horizontal = metrik.aussenAbstand, vertical = metrik.elementAbstand)
                    .archivFokusGruppe(),
                verticalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
            ) {
                // Einordnungskopf
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
                        verticalArrangement = Arrangement.spacedBy(6.dp),
                    ) {
                        ArchivStempel(
                            text = "AUGUST 1914 · ERWERBSLAGE",
                            farbe = farben.akzent,
                        )
                        Text(
                            text = "Wovon lebst du, während der Krieg beginnt?",
                            style = MaterialTheme.typography.headlineSmall,
                            color = farben.tinte,
                            modifier = Modifier.archivUeberschrift(),
                        )
                        Text(
                            text = buildString {
                                if (person != null) {
                                    append("${person.vollerName} (${person.herkunftTitel}, Jahrgang ${person.jahrgang}). ")
                                }
                                append("Viele Männer werden eingezogen, Löhne fallen weg und neue Stellen öffnen sich. Wähle deine Aufgabe in der Heimat.")
                            },
                            style = MaterialTheme.typography.bodyMedium,
                            color = farben.tinteMatt,
                        )
                    }
                }

                // Verfügbare Erwerbslagen (bis zu 4 Karten)
                if (zweispaltig) {
                    optionenUi.chunked(2).forEach { paar ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(IntrinsicSize.Min),
                            horizontalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
                        ) {
                            paar.forEach { option ->
                                ErwerbKarte(
                                    option = option,
                                    ausgewaehlt = option.id == uiState.ausgewaehlterErwerbId,
                                    analyseModus = uiState.analyseModus,
                                    onClick = { onErwerbMarkieren(option.id) },
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
                        optionenUi.forEach { option ->
                            ErwerbKarte(
                                option = option,
                                ausgewaehlt = option.id == uiState.ausgewaehlterErwerbId,
                                analyseModus = uiState.analyseModus,
                                onClick = { onErwerbMarkieren(option.id) },
                                modifier = Modifier.fillMaxWidth(),
                            )
                        }
                    }
                }

                // Bestätigungsleiste (Schutz vor Fehltippen bei „kein Zurück“)
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = farben.papierHell,
                    shape = RoundedCornerShape(4.dp),
                    border = BorderStroke(1.25.dp, if (ausgewaehlt != null) farben.tinte else farben.linie),
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(metrik.kartenInnenAbstand),
                        verticalArrangement = Arrangement.spacedBy(10.dp),
                    ) {
                        Text(
                            text = if (ausgewaehlt != null) {
                                "Gewählte Tätigkeit: ${ausgewaehlt.titel} (${ausgewaehlt.berufsBezeichnung})"
                            } else {
                                "Tippe oder klicke eine Erwerbslage an, um sie festzulegen."
                            },
                            style = MaterialTheme.typography.bodyMedium,
                            color = if (ausgewaehlt != null) farben.tinte else farben.tinteMatt,
                            fontWeight = if (ausgewaehlt != null) FontWeight.SemiBold else FontWeight.Normal,
                            modifier = Modifier.archivLiveHinweis(),
                        )
                        ArchivPrimaerKnopf(
                            label = if (ausgewaehlt != null) {
                                "Als ${ausgewaehlt.berufsBezeichnung} beginnen"
                            } else {
                                "Tätigkeit festlegen"
                            },
                            aktiviert = ausgewaehlt != null,
                            onClick = onBestaetigen,
                            modifier = if (layoutKlasse == LayoutKlasse.KOMPAKT) {
                                Modifier.fillMaxWidth()
                            } else {
                                Modifier
                            },
                        )
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun ErwerbKarte(
    option: ErwerbOptionUiState,
    ausgewaehlt: Boolean,
    analyseModus: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val flaeche = if (ausgewaehlt) farben.papierDunkel else farben.papierHell
    val rahmen = if (ausgewaehlt) farben.akzent else farben.linie

    Surface(
        modifier = modifier
            .defaultMinSize(minHeight = 148.dp)
            .clip(RoundedCornerShape(4.dp))
            .archivFokusRahmen(eckRadius = 4.dp, aufDunkel = false)
            .clickable(onClick = onClick)
            .clearAndSetSemantics {
                role = Role.RadioButton
                selected = ausgewaehlt
                stateDescription = if (ausgewaehlt) "Ausgewählt" else "Nicht ausgewählt"
                contentDescription = buildString {
                    append("${option.titel}: ${option.zusatz}. ")
                    if (option.hinweisStempel != null) {
                        append("Historischer Hinweis: ${option.hinweisStempel}. ")
                    }
                    append(option.folge)
                }
            },
        color = flaeche,
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(if (ausgewaehlt) 2.dp else 1.dp, rahmen),
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
                verticalAlignment = Alignment.Top,
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = option.titel,
                        style = MaterialTheme.typography.titleLarge,
                        color = farben.tinte,
                    )
                    Text(
                        text = option.zusatz,
                        style = MaterialTheme.typography.bodySmall,
                        color = farben.tinteMatt,
                    )
                }
                if (ausgewaehlt) {
                    ArchivStempel(
                        text = "GEWÄHLT",
                        farbe = farben.akzent,
                        hintergrund = farben.akzent.copy(alpha = 0.14f),
                    )
                }
            }

            // Historischer Einordnungs-Stempel aus GameEngine.erwerbHinweis(...)
            if (option.hinweisStempel != null && option.hinweisText != null) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(farben.papier, RoundedCornerShape(3.dp))
                        .border(1.dp, farben.akzent.copy(alpha = 0.55f), RoundedCornerShape(3.dp))
                        .padding(10.dp),
                    verticalArrangement = Arrangement.spacedBy(4.dp),
                ) {
                    ArchivStempel(
                        text = option.hinweisStempel,
                        farbe = farben.akzent,
                    )
                    Text(
                        text = option.hinweisText,
                        style = MaterialTheme.typography.bodySmall,
                        color = farben.tinte,
                    )
                }
            }

            Text(
                text = option.text,
                style = MaterialTheme.typography.bodyMedium,
                color = farben.tinte,
            )

            ArchivTrennlinie(farbe = farben.linieFein)

            Text(
                text = option.folge,
                style = MaterialTheme.typography.bodySmall,
                fontStyle = FontStyle.Italic,
                color = farben.tinteMatt,
            )

            if (analyseModus && option.wirkungen.isNotEmpty()) {
                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp),
                ) {
                    option.wirkungen.forEach { w ->
                        ArchivStempel(
                            text = "${w.name} ${w.zeichen}",
                            farbe = farben.deltaFarbe(schlechter = w.schlechter, aufDunkel = false),
                        )
                    }
                }
            }
        }
    }
}
