package de.pytales.zdf.ui.screens

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
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
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.components.ArchivStempel
import de.pytales.zdf.ui.components.ArchivTrennlinie
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.state.UiStateMapper
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.LayoutKlasse
import de.pytales.zdf.ui.theme.Schriftgroesse

/**
 * Ruhige Jahres-Auftaktkarte (`GamePhase.KapitelStart`):
 * zeigt Zeitraum, Überschrift, Einführungstext, historische Stichworte,
 * den 16:9-[KapitelbildRahmen] (`kapitel.bildId` über den Multiplatform-Bild-Loader mit
 * Archivtafel-Fallback) sowie die spürbare Kapitelwirkung (falls vorhanden).
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun KapitelStartScreen(
    engine: GameEngine,
    uiState: SpielUiState,
    phase: GamePhase.KapitelStart,
    onStarteKapitel: () -> Unit,
    onSchriftgroesseChange: (Schriftgroesse) -> Unit,
    onAnalyseModusToggle: () -> Unit,
    onWertErklaerungChange: (WertSchluessel?) -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val layoutKlasse = ArchivTheme.layoutKlasse
    val kapitelUi = remember(engine, phase, uiState.gameState.pfad) {
        UiStateMapper.mapKapitelStart(engine, phase, uiState.gameState.pfad)
    }

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
                    .padding(horizontal = metrik.aussenAbstand, vertical = metrik.elementAbstand),
                verticalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
            ) {
                val nebeneinander = layoutKlasse == LayoutKlasse.BREIT

                val bildBlock: @Composable (Modifier) -> Unit = { mod ->
                    KapitelbildRahmen(
                        kapitelbild = kapitelUi.kapitelbild,
                        analyseModus = uiState.analyseModus,
                        modifier = mod,
                    )
                }

                val textBlatt: @Composable (Modifier) -> Unit = { mod ->
                    Surface(
                        modifier = mod,
                        color = farben.papierHell,
                        shape = RoundedCornerShape(4.dp),
                        border = BorderStroke(1.dp, farben.linie),
                        shadowElevation = 1.dp,
                    ) {
                        Column(modifier = Modifier.fillMaxWidth()) {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(3.dp)
                                    .background(farben.akzent),
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
                                        text = if (kapitelUi.istEpilog) {
                                            "EPILOG · ${kapitelUi.jahr}"
                                        } else {
                                            "JAHR ${kapitelUi.jahr}"
                                        },
                                        farbe = farben.akzent,
                                    )
                                    Text(
                                        text = kapitelUi.zeitraum,
                                        style = MaterialTheme.typography.labelSmall,
                                        color = farben.tinteMatt,
                                    )
                                }

                                Text(
                                    text = kapitelUi.ueberschrift,
                                    style = MaterialTheme.typography.headlineMedium,
                                    color = farben.tinte,
                                )

                                // Stichworte des Jahres
                                if (kapitelUi.stichworte.isNotEmpty()) {
                                    FlowRow(
                                        horizontalArrangement = Arrangement.spacedBy(6.dp),
                                        verticalArrangement = Arrangement.spacedBy(6.dp),
                                    ) {
                                        kapitelUi.stichworte.forEach { stichwort ->
                                            ArchivStempel(
                                                text = stichwort,
                                                farbe = farben.tinteMatt,
                                                hintergrund = farben.papier,
                                            )
                                        }
                                    }
                                }

                                ArchivTrennlinie(farbe = farben.linieFein)

                                Text(
                                    text = kapitelUi.text,
                                    style = MaterialTheme.typography.bodyLarge,
                                    color = farben.tinte,
                                )

                                // Leitfrage für das Jahr (ruhige didaktische Rahmung)
                                if (!kapitelUi.leitfrage.isNullOrBlank()) {
                                    Box(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .background(farben.papier, RoundedCornerShape(3.dp))
                                            .border(1.dp, farben.linieFein, RoundedCornerShape(3.dp))
                                            .padding(12.dp),
                                    ) {
                                        Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
                                            Text(
                                                text = "LEITFRAGE FÜR DIESES JAHR",
                                                style = MaterialTheme.typography.labelSmall,
                                                color = farben.tinteMatt,
                                            )
                                            Text(
                                                text = "„${kapitelUi.leitfrage}“",
                                                style = MaterialTheme.typography.bodyMedium,
                                                fontStyle = FontStyle.Italic,
                                                color = farben.tinte,
                                            )
                                        }
                                    }
                                }

                                // Sichtbare Kapitelwirkung (falls vorhanden, ab 1915)
                                if (kapitelUi.wirkungText != null || kapitelUi.wirkungen.isNotEmpty()) {
                                    Column(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .background(farben.papierDunkel.copy(alpha = 0.55f), RoundedCornerShape(3.dp))
                                            .border(1.dp, farben.linie, RoundedCornerShape(3.dp))
                                            .padding(12.dp),
                                        verticalArrangement = Arrangement.spacedBy(8.dp),
                                    ) {
                                        Text(
                                            text = "WIRKUNG DES JAHRESWECHSELS",
                                            style = MaterialTheme.typography.labelSmall,
                                            color = farben.tinte,
                                            fontWeight = FontWeight.Bold,
                                        )
                                        if (kapitelUi.wirkungText != null) {
                                            Text(
                                                text = kapitelUi.wirkungText,
                                                style = MaterialTheme.typography.bodyMedium,
                                                color = farben.tinte,
                                            )
                                        }
                                        if (kapitelUi.wirkungen.isNotEmpty()) {
                                            FlowRow(
                                                horizontalArrangement = Arrangement.spacedBy(8.dp),
                                                verticalArrangement = Arrangement.spacedBy(8.dp),
                                            ) {
                                                kapitelUi.wirkungen.forEach { wirkung ->
                                                    val farbe = farben.deltaFarbe(
                                                        schlechter = wirkung.schlechter,
                                                        aufDunkel = false,
                                                    )
                                                    ArchivStempel(
                                                        text = "${wirkung.name} ${wirkung.zeichen} (${wirkung.richtung})",
                                                        farbe = farbe,
                                                    )
                                                }
                                            }
                                        }
                                    }
                                }

                                Spacer(modifier = Modifier.height(2.dp))

                                ArchivPrimaerKnopf(
                                    label = kapitelUi.aktionLabel,
                                    onClick = onStarteKapitel,
                                    modifier = if (layoutKlasse == LayoutKlasse.KOMPAKT) {
                                        Modifier.fillMaxWidth()
                                    } else {
                                        Modifier
                                    },
                                )
                            }
                        }
                    }
                }

                if (nebeneinander) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
                        verticalAlignment = Alignment.Top,
                    ) {
                        bildBlock(Modifier.weight(0.44f))
                        textBlatt(Modifier.weight(0.56f))
                    }
                } else {
                    bildBlock(Modifier.fillMaxWidth())
                    textBlatt(Modifier.fillMaxWidth())
                }

                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
}
