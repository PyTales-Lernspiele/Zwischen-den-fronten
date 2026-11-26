package de.pytales.zdf.ui.screens

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
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
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.clearAndSetSemantics
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import de.pytales.zdf.audio.SoundEffekt
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.components.HakenIcon
import de.pytales.zdf.ui.components.archivFokusGruppe
import de.pytales.zdf.ui.components.archivFokusRahmen
import de.pytales.zdf.ui.components.archivLiveHinweis
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.state.ErwerbOptionUiState
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.state.UiStateMapper
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.LocalSoundEffektSpielen

/**
 * Erwerbswahl im August 1914 (`GamePhase.ErwerbWahl`) für Figuren in der Heimat:
 * luftiges 2-Spalten-Raster ohne innere graue Boxen und ohne extra Rahmen um die
 * Bestätigungszeile.
 */
@Composable
fun ErwerbWahlScreen(
    engine: GameEngine,
    uiState: SpielUiState,
    phase: GamePhase.ErwerbWahl,
    onErwerbMarkieren: (String) -> Unit,
    onBestaetigen: () -> Unit,
    onAudioToggle: () -> Unit,
    onEinstellungenOeffnen: () -> Unit,
    onKopfleisteToggle: () -> Unit,
    onWertErklaerungChange: (WertSchluessel?) -> Unit,
    onEmotionDetailsOffenChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val kompakt = metrik.kompakteHoehe
    val zweispaltig = metrik.zweispaltigeBuehne
    val spieleEffekt = LocalSoundEffektSpielen.current

    val optionenUi = remember(engine, uiState.gameState, phase.optionen) {
        UiStateMapper.mapErwerbOptionen(engine, uiState.gameState, phase.optionen)
    }
    val ausgewaehlt = optionenUi.firstOrNull { it.id == uiState.ausgewaehlterErwerbId }
    val topAbstand = if (uiState.kopfleisteEingeklappt) 34.dp else if (kompakt) 10.dp else 18.dp

    SpielBuehnenRahmen(
        engine = engine,
        uiState = uiState,
        onAudioToggle = onAudioToggle,
        onEinstellungenOeffnen = onEinstellungenOeffnen,
        onKopfleisteToggle = onKopfleisteToggle,
        onWertErklaerungChange = onWertErklaerungChange,
        onEmotionDetailsOffenChange = onEmotionDetailsOffenChange,
        modifier = modifier,
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState()),
            contentAlignment = Alignment.Center,
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .archivInhaltsSafeArea()
                    .widthIn(max = 940.dp)
                    .padding(
                        start = metrik.aussenAbstand,
                        end = metrik.aussenAbstand,
                        top = topAbstand,
                        bottom = if (kompakt) 12.dp else 20.dp,
                    )
                    .archivFokusGruppe(),
                verticalArrangement = Arrangement.spacedBy(if (kompakt) 12.dp else 16.dp),
            ) {
                Text(
                    text = "Wovon lebst du im August 1914?",
                    style = if (kompakt) MaterialTheme.typography.headlineSmall else MaterialTheme.typography.headlineMedium,
                    color = farben.tinte,
                    modifier = Modifier.archivUeberschrift(),
                )

                if (zweispaltig) {
                    optionenUi.chunked(2).forEach { paar ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(IntrinsicSize.Min),
                            horizontalArrangement = Arrangement.spacedBy(if (kompakt) 10.dp else 14.dp),
                        ) {
                            paar.forEach { option ->
                                ErwerbKarte(
                                    option = option,
                                    ausgewaehlt = option.id == uiState.ausgewaehlterErwerbId,
                                    kompakt = kompakt,
                                    onClick = {
                                        spieleEffekt(SoundEffekt.KLICK_SANFT)
                                        onErwerbMarkieren(option.id)
                                    },
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
                                kompakt = kompakt,
                                onClick = {
                                    spieleEffekt(SoundEffekt.KLICK_SANFT)
                                    onErwerbMarkieren(option.id)
                                },
                                modifier = Modifier.fillMaxWidth(),
                            )
                        }
                    }
                }

                // Schlichte offene Bestätigungszeile direkt auf dem Archivpapier (kein Kasten)
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 2.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text(
                        text = if (ausgewaehlt != null) {
                            "${ausgewaehlt.titel} · ${ausgewaehlt.berufsBezeichnung}"
                        } else {
                            "Wähle deine Aufgabe in der Heimat."
                        },
                        style = MaterialTheme.typography.bodySmall,
                        color = if (ausgewaehlt != null) farben.tinte else farben.tinteMatt,
                        fontWeight = if (ausgewaehlt != null) FontWeight.Medium else FontWeight.Normal,
                        modifier = Modifier
                            .weight(1f)
                            .padding(end = 12.dp)
                            .archivLiveHinweis(),
                    )
                    ArchivPrimaerKnopf(
                        label = if (ausgewaehlt != null) {
                            "Als ${ausgewaehlt.berufsBezeichnung} beginnen"
                        } else {
                            "Tätigkeit festlegen"
                        },
                        akzentStil = ausgewaehlt != null,
                        aktiviert = ausgewaehlt != null,
                        klickEffekt = SoundEffekt.ENTSCHEIDUNG,
                        onClick = onBestaetigen,
                    )
                }
            }
        }
    }
}

@Composable
private fun ErwerbKarte(
    option: ErwerbOptionUiState,
    ausgewaehlt: Boolean,
    kompakt: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val flaeche = if (ausgewaehlt) farben.papierHell else farben.papierHell.copy(alpha = 0.58f)
    val rahmen = if (ausgewaehlt) farben.akzent else farben.linieFein.copy(alpha = 0.85f)

    Surface(
        modifier = modifier
            .defaultMinSize(minHeight = if (kompakt) 96.dp else 118.dp)
            .clip(RoundedCornerShape(6.dp))
            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = false)
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
        shape = RoundedCornerShape(6.dp),
        border = BorderStroke(if (ausgewaehlt) 1.4.dp else 0.75.dp, rahmen),
        shadowElevation = if (ausgewaehlt) 1.dp else 0.dp,
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .height(IntrinsicSize.Min),
        ) {
            Box(
                modifier = Modifier
                    .width(if (ausgewaehlt) 3.dp else 0.dp)
                    .fillMaxHeight()
                    .background(if (ausgewaehlt) farben.akzent else Color.Transparent),
            )
            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(horizontal = if (kompakt) 13.dp else 15.dp, vertical = if (kompakt) 10.dp else 12.dp),
                verticalArrangement = Arrangement.spacedBy(4.dp),
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text(
                        text = option.titel,
                        style = MaterialTheme.typography.titleMedium,
                        fontFamily = FontFamily.Serif,
                        color = farben.tinte,
                        fontWeight = FontWeight.Bold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.weight(1f),
                    )
                    if (ausgewaehlt) {
                        HakenIcon(farbe = farben.akzent, groesse = 15.dp)
                    }
                }

                if (option.hinweisStempel != null && option.hinweisText != null) {
                    Text(
                        text = "${option.hinweisStempel} · ${option.hinweisText}",
                        style = MaterialTheme.typography.labelSmall,
                        fontStyle = FontStyle.Italic,
                        color = farben.akzent,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis,
                    )
                } else {
                    Text(
                        text = option.zusatz,
                        style = MaterialTheme.typography.labelSmall,
                        color = farben.tinteMatt,
                    )
                }

                Text(
                    text = option.text,
                    style = MaterialTheme.typography.bodySmall,
                    color = farben.tinte,
                )

                if (!kompakt) {
                    Text(
                        text = option.folge,
                        style = MaterialTheme.typography.bodySmall,
                        fontFamily = FontFamily.Serif,
                        fontStyle = FontStyle.Italic,
                        color = farben.tinteMatt,
                    )
                }
            }
        }
    }
}
