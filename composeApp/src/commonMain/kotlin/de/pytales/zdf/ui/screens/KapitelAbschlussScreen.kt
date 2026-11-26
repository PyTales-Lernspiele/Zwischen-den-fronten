package de.pytales.zdf.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import de.pytales.zdf.audio.SoundEffekt
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.components.ArchivTrennlinie
import de.pytales.zdf.ui.components.archivFokusGruppe
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.state.UiStateMapper
import de.pytales.zdf.ui.theme.ArchivTheme

/**
 * Jahresrückblick (`GamePhase.KapitelAbschluss`) als ruhige, offene Buchseite:
 * ohne Kasten-in-Kasten-Rahmen — links Jahresrückblick & persönlicher Zustandssatz,
 * rechts Leitfrage, Kipppunkt des Pfades und Übergang ins nächste Jahr.
 */
@Composable
fun KapitelAbschlussScreen(
    engine: GameEngine,
    uiState: SpielUiState,
    phase: GamePhase.KapitelAbschluss,
    onNaechstesKapitel: () -> Unit,
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
    val gameState = uiState.gameState

    val abschlussUi = remember(engine, phase, gameState.pfad, gameState.werte) {
        UiStateMapper.mapKapitelAbschluss(
            content = engine.content,
            phase = phase,
            pfad = gameState.pfad,
            zustandssatz = engine.zustandssatz(gameState),
        )
    }
    val topAbstand = if (uiState.kopfleisteEingeklappt) 34.dp else if (kompakt) 12.dp else 24.dp

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
            val linkeSpalte: @Composable (Modifier) -> Unit = { mod ->
                Column(
                    modifier = mod,
                    verticalArrangement = Arrangement.spacedBy(if (kompakt) 10.dp else 14.dp),
                ) {
                    Text(
                        text = "Jahresrückblick ${abschlussUi.jahr} · ${abschlussUi.pfadMarke}",
                        style = MaterialTheme.typography.labelMedium,
                        fontFamily = FontFamily.Serif,
                        color = farben.akzent,
                        fontWeight = FontWeight.SemiBold,
                    )

                    Text(
                        text = abschlussUi.ueberschrift,
                        style = if (kompakt) MaterialTheme.typography.headlineSmall else MaterialTheme.typography.headlineMedium,
                        color = farben.tinte,
                        modifier = Modifier.archivUeberschrift(),
                    )

                    if (abschlussUi.rueckblick != null) {
                        Text(
                            text = abschlussUi.rueckblick,
                            style = MaterialTheme.typography.bodyLarge,
                            color = farben.tinte,
                        )
                    }

                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(IntrinsicSize.Min),
                        horizontalArrangement = Arrangement.spacedBy(10.dp),
                    ) {
                        Box(
                            modifier = Modifier
                                .width(2.dp)
                                .fillMaxHeight()
                                .background(farben.linie),
                        )
                        Text(
                            text = "„${abschlussUi.zustandssatz}“",
                            style = MaterialTheme.typography.bodyMedium,
                            fontFamily = FontFamily.Serif,
                            fontStyle = FontStyle.Italic,
                            color = farben.tinteMatt,
                            modifier = Modifier.weight(1f),
                        )
                    }
                }
            }

            val rechteSpalte: @Composable (Modifier) -> Unit = { mod ->
                Column(
                    modifier = mod,
                    verticalArrangement = Arrangement.spacedBy(if (kompakt) 14.dp else 18.dp),
                ) {
                    OffeneBogenNotiz(
                        titel = "Historische Leitfrage",
                        text = abschlussUi.leitfrage,
                        hervorgehoben = false,
                    )

                    OffeneBogenNotiz(
                        titel = "Was ${abschlussUi.jahr} kippt",
                        text = abschlussUi.kipppunkt,
                        hervorgehoben = true,
                    )

                    Spacer(modifier = Modifier.height(2.dp))

                    ArchivPrimaerKnopf(
                        label = abschlussUi.weiterLabel,
                        klickEffekt = SoundEffekt.KAPITELWECHSEL,
                        onClick = onNaechstesKapitel,
                        modifier = Modifier.fillMaxWidth(),
                    )
                }
            }

            if (metrik.zweispaltigeBuehne) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .archivInhaltsSafeArea()
                        .widthIn(max = 940.dp)
                        .padding(
                            start = metrik.aussenAbstand,
                            end = metrik.aussenAbstand,
                            top = topAbstand,
                            bottom = if (kompakt) 14.dp else 24.dp,
                        )
                        .archivFokusGruppe(),
                    horizontalArrangement = Arrangement.spacedBy(if (kompakt) 24.dp else 36.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    linkeSpalte(Modifier.weight(0.54f))
                    rechteSpalte(Modifier.weight(0.46f))
                }
            } else {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .archivInhaltsSafeArea()
                        .widthIn(max = 600.dp)
                        .padding(
                            start = metrik.aussenAbstand,
                            end = metrik.aussenAbstand,
                            top = topAbstand,
                            bottom = 20.dp,
                        )
                        .archivFokusGruppe(),
                    verticalArrangement = Arrangement.spacedBy(18.dp),
                ) {
                    linkeSpalte(Modifier.fillMaxWidth())
                    ArchivTrennlinie(farbe = farben.linieFein.copy(alpha = 0.6f))
                    rechteSpalte(Modifier.fillMaxWidth())
                }
            }
        }
    }
}

@Composable
private fun OffeneBogenNotiz(
    titel: String,
    text: String,
    hervorgehoben: Boolean,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben

    Row(
        modifier = modifier
            .fillMaxWidth()
            .semantics(mergeDescendants = true) {}
            .height(IntrinsicSize.Min),
        horizontalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        Box(
            modifier = Modifier
                .width(2.5.dp)
                .fillMaxHeight()
                .background(if (hervorgehoben) farben.akzent else farben.linie),
        )
        Column(
            modifier = Modifier.weight(1f),
            verticalArrangement = Arrangement.spacedBy(3.dp),
        ) {
            Text(
                text = titel,
                style = MaterialTheme.typography.labelMedium,
                fontFamily = FontFamily.Serif,
                color = if (hervorgehoben) farben.akzent else farben.tinteMatt,
                fontWeight = FontWeight.SemiBold,
            )
            Text(
                text = text,
                style = MaterialTheme.typography.bodyMedium,
                color = farben.tinte,
            )
        }
    }
}
