package de.pytales.zdf.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
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
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import de.pytales.zdf.audio.SoundEffekt
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.components.ArchivStempel
import de.pytales.zdf.ui.components.archivFokusGruppe
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.state.UiStateMapper
import de.pytales.zdf.ui.theme.ArchivTheme

/**
 * Ruhiger Jahres-Auftakt (`GamePhase.KapitelStart`) als offene Buch-Doppelseite:
 * links das gerahmte 16:9-Kapitelbild, rechts freie Typografie direkt auf dem Archivpapier
 * ohne Kastenrahmen und ohne doppelte Überschriften.
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun KapitelStartScreen(
    engine: GameEngine,
    uiState: SpielUiState,
    phase: GamePhase.KapitelStart,
    onStarteKapitel: () -> Unit,
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
    val kapitelUi = remember(engine, phase, uiState.gameState.pfad) {
        UiStateMapper.mapKapitelStart(engine, phase, uiState.gameState.pfad)
    }
    val laschenLuftOben = if (uiState.kopfleisteEingeklappt) 26.dp else 0.dp

    val textSpalte: @Composable (Modifier) -> Unit = { mod ->
        Column(
            modifier = mod,
            verticalArrangement = Arrangement.spacedBy(if (kompakt) 10.dp else 14.dp),
        ) {
            Text(
                text = if (kapitelUi.istEpilog) "Epilog ${kapitelUi.jahr}" else "Jahr ${kapitelUi.jahr}",
                style = MaterialTheme.typography.labelMedium,
                fontFamily = FontFamily.Serif,
                color = farben.akzent,
                fontWeight = FontWeight.SemiBold,
            )

            Text(
                text = kapitelUi.ueberschrift,
                style = if (kompakt) MaterialTheme.typography.headlineSmall else MaterialTheme.typography.headlineMedium,
                color = farben.tinte,
                modifier = Modifier.archivUeberschrift(),
            )

            Text(
                text = kapitelUi.text,
                style = MaterialTheme.typography.bodyLarge,
                color = farben.tinte,
            )

            if (!kapitelUi.leitfrage.isNullOrBlank()) {
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
                            .background(farben.akzentMatt.copy(alpha = 0.72f)),
                    )
                    Text(
                        text = "„${kapitelUi.leitfrage}“",
                        style = MaterialTheme.typography.bodyMedium,
                        fontFamily = FontFamily.Serif,
                        fontStyle = FontStyle.Italic,
                        color = farben.tinteMatt,
                        modifier = Modifier.weight(1f),
                    )
                }
            }

            // Sichtbare Kapitelwirkung (ab 1915) kompakt ohne graue Box
            if (kapitelUi.wirkungText != null || kapitelUi.wirkungen.isNotEmpty()) {
                Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    if (kapitelUi.wirkungText != null) {
                        Text(
                            text = kapitelUi.wirkungText,
                            style = MaterialTheme.typography.bodySmall,
                            color = farben.tinteMatt,
                        )
                    }
                    if (kapitelUi.wirkungen.isNotEmpty()) {
                        FlowRow(
                            horizontalArrangement = Arrangement.spacedBy(6.dp),
                            verticalArrangement = Arrangement.spacedBy(6.dp),
                        ) {
                            kapitelUi.wirkungen.forEach { wirkung ->
                                val farbe = farben.deltaFarbe(
                                    schlechter = wirkung.schlechter,
                                    aufDunkel = false,
                                )
                                ArchivStempel(
                                    text = "${wirkung.name} ${wirkung.zeichen}",
                                    farbe = farbe,
                                    hintergrund = farbe.copy(alpha = 0.08f),
                                )
                            }
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(2.dp))

            ArchivPrimaerKnopf(
                label = kapitelUi.aktionLabel,
                klickEffekt = SoundEffekt.KAPITELWECHSEL,
                onClick = onStarteKapitel,
            )
        }
    }

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
        if (metrik.zweispaltigeBuehne) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center,
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxSize()
                        .archivInhaltsSafeArea()
                        .widthIn(max = metrik.maxInhaltsBreite)
                        .padding(
                            horizontal = metrik.aussenAbstand,
                            vertical = if (kompakt) 10.dp else 20.dp,
                        )
                        .archivFokusGruppe(),
                    horizontalArrangement = Arrangement.spacedBy(if (kompakt) 20.dp else 32.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Box(
                        modifier = Modifier
                            .weight(0.44f)
                            .fillMaxHeight(),
                        contentAlignment = Alignment.Center,
                    ) {
                        KapitelbildRahmen(kapitelbild = kapitelUi.kapitelbild)
                    }
                    Box(
                        modifier = Modifier
                            .weight(0.56f)
                            .fillMaxHeight()
                            .verticalScroll(rememberScrollState())
                            .padding(top = laschenLuftOben),
                        contentAlignment = Alignment.CenterStart,
                    ) {
                        textSpalte(Modifier.fillMaxWidth())
                    }
                }
            }
        } else {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState()),
                contentAlignment = Alignment.TopCenter,
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .archivInhaltsSafeArea()
                        .widthIn(max = metrik.maxInhaltsBreite)
                        .padding(
                            start = metrik.aussenAbstand,
                            end = metrik.aussenAbstand,
                            top = if (uiState.kopfleisteEingeklappt) 34.dp else 14.dp,
                            bottom = 18.dp,
                        )
                        .archivFokusGruppe(),
                    verticalArrangement = Arrangement.spacedBy(16.dp),
                ) {
                    KapitelbildRahmen(kapitelbild = kapitelUi.kapitelbild)
                    textSpalte(Modifier.fillMaxWidth())
                }
            }
        }
    }
}
