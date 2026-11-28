package de.pytales.zdf.ui.screens

import androidx.compose.foundation.BorderStroke
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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.components.ArchivStempel
import de.pytales.zdf.ui.components.ArchivTrennlinie
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.state.UiStateMapper
import de.pytales.zdf.ui.theme.ArchivTheme

/**
 * Ruhiger Jahres-Auftakt (`GamePhase.KapitelStart`) als zweispaltige Buchseite im Querformat:
 * links das gerahmte 16:9-Kapitelbild im Passepartout, rechts Kapitelüberschrift,
 * geschichtlicher Auftakt, Leitfrage und spürbare Jahreswechsel-Wirkung.
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
    val zeigeRandLeiste = uiState.kopfleisteEingeklappt && metrik.kopfNebeneinander
    val kapitelUi = remember(engine, phase, uiState.gameState.pfad) {
        UiStateMapper.mapKapitelStart(engine, phase, uiState.gameState.pfad)
    }

    val textBlatt: @Composable (Modifier) -> Unit = { mod ->
        Surface(
            modifier = mod,
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
                        .background(farben.akzent),
                )

                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(
                            horizontal = metrik.kartenInnenAbstand,
                            vertical = if (kompakt) 12.dp else 18.dp,
                        ),
                    verticalArrangement = Arrangement.spacedBy(if (kompakt) 9.dp else 12.dp),
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        Text(
                            text = if (kapitelUi.istEpilog) "Epilog ${kapitelUi.jahr}" else "Jahr ${kapitelUi.jahr}",
                            style = MaterialTheme.typography.labelMedium,
                            fontFamily = FontFamily.Serif,
                            color = farben.akzent,
                            fontWeight = FontWeight.SemiBold,
                        )
                        Text(
                            text = kapitelUi.zeitraum,
                            style = MaterialTheme.typography.labelSmall,
                            color = farben.tinteMatt,
                        )
                    }

                    Text(
                        text = kapitelUi.ueberschrift,
                        style = if (kompakt) MaterialTheme.typography.headlineSmall else MaterialTheme.typography.headlineMedium,
                        color = farben.tinte,
                        modifier = Modifier.archivUeberschrift(),
                    )

                    if (kapitelUi.stichworte.isNotEmpty()) {
                        Text(
                            text = kapitelUi.stichworte.joinToString("  ·  "),
                            style = MaterialTheme.typography.labelSmall,
                            color = farben.tinteMatt,
                        )
                    }

                    ArchivTrennlinie(farbe = farben.linieFein.copy(alpha = 0.65f))

                    Text(
                        text = kapitelUi.text,
                        style = MaterialTheme.typography.bodyLarge,
                        color = farben.tinte,
                    )

                    // Ruhige Leitfrage mit linker Akzentlinie
                    if (!kapitelUi.leitfrage.isNullOrBlank()) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(IntrinsicSize.Min)
                                .background(farben.papier.copy(alpha = 0.65f), RoundedCornerShape(4.dp)),
                        ) {
                            Box(
                                modifier = Modifier
                                    .width(2.5.dp)
                                    .fillMaxHeight()
                                    .background(farben.akzentMatt),
                            )
                            Text(
                                text = "„${kapitelUi.leitfrage}“",
                                style = MaterialTheme.typography.bodyMedium,
                                fontFamily = FontFamily.Serif,
                                fontStyle = FontStyle.Italic,
                                color = farben.tinte,
                                modifier = Modifier
                                    .weight(1f)
                                    .padding(horizontal = 12.dp, vertical = 8.dp),
                            )
                        }
                    }

                    // Sichtbare Kapitelwirkung (ab 1915)
                    if (kapitelUi.wirkungText != null || kapitelUi.wirkungen.isNotEmpty()) {
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .background(farben.papierDunkel.copy(alpha = 0.45f), RoundedCornerShape(5.dp))
                                .padding(horizontal = 12.dp, vertical = 9.dp),
                            verticalArrangement = Arrangement.spacedBy(6.dp),
                        ) {
                            if (kapitelUi.wirkungText != null) {
                                Text(
                                    text = kapitelUi.wirkungText,
                                    style = MaterialTheme.typography.bodySmall,
                                    color = farben.tinte,
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
                                            hintergrund = farben.papierHell,
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    // Fest verankerter Knopf: immer sichtbar, auch auf kleinen Handys
    val weiterKnopf: @Composable () -> Unit = {
        ArchivPrimaerKnopf(
            label = "${kapitelUi.aktionLabel}  →",
            onClick = onStarteKapitel,
            akzentStil = true,
            modifier = Modifier.fillMaxWidth(),
        )
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
                contentAlignment = Alignment.TopCenter,
            ) {
                Row(
                    modifier = Modifier
                        .archivInhaltsSafeArea(ohneRechtenRand = zeigeRandLeiste)
                        .widthIn(max = metrik.maxInhaltsBreite)
                        .fillMaxSize()
                        .padding(
                            horizontal = metrik.aussenAbstand,
                            vertical = if (kompakt) 8.dp else 16.dp,
                        ),
                    horizontalArrangement = Arrangement.spacedBy(if (kompakt) 14.dp else 20.dp),
                    verticalAlignment = Alignment.Top,
                ) {
                    Column(
                        modifier = Modifier
                            .weight(0.44f)
                            .fillMaxHeight()
                            .verticalScroll(rememberScrollState()),
                    ) {
                        KapitelbildRahmen(kapitelbild = kapitelUi.kapitelbild)
                    }
                    Column(
                        modifier = Modifier
                            .weight(0.56f)
                            .fillMaxHeight(),
                        verticalArrangement = Arrangement.spacedBy(if (kompakt) 6.dp else 10.dp),
                    ) {
                        Column(
                            modifier = Modifier
                                .weight(1f, fill = false)
                                .verticalScroll(rememberScrollState()),
                        ) {
                            textBlatt(Modifier.fillMaxWidth())
                        }
                        weiterKnopf()
                    }
                }
            }
        } else {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .archivInhaltsSafeArea(),
                horizontalAlignment = Alignment.CenterHorizontally,
            ) {
                Column(
                    modifier = Modifier
                        .weight(1f, fill = false)
                        .widthIn(max = metrik.maxInhaltsBreite)
                        .fillMaxWidth()
                        .verticalScroll(rememberScrollState())
                        .padding(horizontal = metrik.aussenAbstand, vertical = 14.dp),
                    verticalArrangement = Arrangement.spacedBy(14.dp),
                ) {
                    KapitelbildRahmen(kapitelbild = kapitelUi.kapitelbild)
                    textBlatt(Modifier.fillMaxWidth())
                }
                Box(
                    modifier = Modifier
                        .widthIn(max = metrik.maxInhaltsBreite)
                        .fillMaxWidth()
                        .padding(horizontal = metrik.aussenAbstand, vertical = 8.dp),
                ) {
                    weiterKnopf()
                }
            }
        }
    }
}
