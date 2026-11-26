package de.pytales.zdf.ui.screens

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.ui.semantics.semantics
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
import de.pytales.zdf.ui.theme.LayoutKlasse
import de.pytales.zdf.ui.theme.Schriftgroesse

/**
 * Jahresrückblick (`GamePhase.KapitelAbschluss`):
 * fasst das durchlebte Kriegsjahr zusammen, stellt die historische Leitfrage & den Kipppunkt
 * ([KapitelBogen]) für den gespielten Pfad heraus und führt in das nächste Jahr (bis Epilog 1919).
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun KapitelAbschlussScreen(
    engine: GameEngine,
    uiState: SpielUiState,
    phase: GamePhase.KapitelAbschluss,
    onNaechstesKapitel: () -> Unit,
    onSchriftgroesseChange: (Schriftgroesse) -> Unit,
    onAnalyseModusToggle: () -> Unit,
    onAudioToggle: () -> Unit = {},
    onWertErklaerungChange: (WertSchluessel?) -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val layoutKlasse = ArchivTheme.layoutKlasse
    val gameState = uiState.gameState

    val abschlussUi = remember(engine, phase, gameState.pfad, gameState.werte) {
        UiStateMapper.mapKapitelAbschluss(
            content = engine.content,
            phase = phase,
            pfad = gameState.pfad,
            zustandssatz = engine.zustandssatz(gameState),
        )
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
                    .padding(horizontal = metrik.aussenAbstand, vertical = metrik.elementAbstand),
                verticalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
            ) {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
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
                                .background(farben.tinte),
                        )

                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(metrik.kartenInnenAbstand),
                            verticalArrangement = Arrangement.spacedBy(14.dp),
                        ) {
                            // Kopfzeile
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically,
                            ) {
                                ArchivStempel(
                                    text = "JAHRESRÜCKBLICK · ${abschlussUi.jahr}",
                                    farbe = farben.tinte,
                                    hintergrund = farben.papierDunkel,
                                )
                                Text(
                                    text = "${abschlussUi.zeitraum} · ${abschlussUi.pfadMarke}",
                                    style = MaterialTheme.typography.labelSmall,
                                    color = farben.tinteMatt,
                                )
                            }

                            Text(
                                text = abschlussUi.ueberschrift,
                                style = MaterialTheme.typography.headlineMedium,
                                color = farben.tinte,
                                modifier = Modifier.archivUeberschrift(),
                            )

                            if (abschlussUi.stichworte.isNotEmpty()) {
                                FlowRow(
                                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                                    verticalArrangement = Arrangement.spacedBy(6.dp),
                                ) {
                                    abschlussUi.stichworte.forEach { stichwort ->
                                        ArchivStempel(
                                            text = stichwort,
                                            farbe = farben.tinteMatt,
                                            hintergrund = farben.papier,
                                        )
                                    }
                                }
                            }

                            ArchivTrennlinie(farbe = farben.linieFein)

                            // Historischer Jahresrückblick
                            if (abschlussUi.rueckblick != null) {
                                Text(
                                    text = abschlussUi.rueckblick,
                                    style = MaterialTheme.typography.bodyLarge,
                                    color = farben.tinte,
                                )
                            }

                            // Leitfrage & Kipppunkt (KapitelBogen)
                            val kartenNebeneinander = layoutKlasse != LayoutKlasse.KOMPAKT &&
                                uiState.schriftgroesse != Schriftgroesse.GROSS

                            if (kartenNebeneinander) {
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(IntrinsicSize.Min),
                                    horizontalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
                                ) {
                                    BogenHinweisKarte(
                                        marke = "HISTORISCHE LEITFRAGE",
                                        text = abschlussUi.leitfrage,
                                        hervorgehoben = false,
                                        modifier = Modifier
                                            .weight(1f)
                                            .fillMaxHeight(),
                                    )
                                    BogenHinweisKarte(
                                        marke = "WAS IN ${abschlussUi.jahr} KIPPT (${abschlussUi.pfadMarke.uppercase()})",
                                        text = abschlussUi.kipppunkt,
                                        hervorgehoben = true,
                                        modifier = Modifier
                                            .weight(1f)
                                            .fillMaxHeight(),
                                    )
                                }
                            } else {
                                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                                    BogenHinweisKarte(
                                        marke = "HISTORISCHE LEITFRAGE",
                                        text = abschlussUi.leitfrage,
                                        hervorgehoben = false,
                                        modifier = Modifier.fillMaxWidth(),
                                    )
                                    BogenHinweisKarte(
                                        marke = "WAS IN ${abschlussUi.jahr} KIPPT (${abschlussUi.pfadMarke.uppercase()})",
                                        text = abschlussUi.kipppunkt,
                                        hervorgehoben = true,
                                        modifier = Modifier.fillMaxWidth(),
                                    )
                                }
                            }

                            // Persönlicher Stand am Jahresende
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .background(farben.papier, RoundedCornerShape(3.dp))
                                    .border(1.dp, farben.linieFein, RoundedCornerShape(3.dp))
                                    .padding(horizontal = 12.dp, vertical = 10.dp),
                            ) {
                                Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
                                    Text(
                                        text = "DEINE LAGE AM ENDE DES JAHRES ${abschlussUi.jahr}",
                                        style = MaterialTheme.typography.labelSmall,
                                        color = farben.tinteMatt,
                                    )
                                    Text(
                                        text = "„${abschlussUi.zustandssatz}“",
                                        style = MaterialTheme.typography.bodyMedium,
                                        fontStyle = FontStyle.Italic,
                                        color = farben.tinte,
                                    )
                                }
                            }

                            ArchivTrennlinie(farbe = farben.linieFein)

                            ArchivPrimaerKnopf(
                                label = abschlussUi.weiterLabel,
                                onClick = onNaechstesKapitel,
                                modifier = if (layoutKlasse == LayoutKlasse.KOMPAKT) {
                                    Modifier.fillMaxWidth()
                                } else {
                                    Modifier
                                },
                            )
                        }
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
}

@Composable
private fun BogenHinweisKarte(
    marke: String,
    text: String,
    hervorgehoben: Boolean,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val akzentLinie = if (hervorgehoben) farben.akzent else farben.linie

    Row(
        modifier = modifier
            .semantics(mergeDescendants = true) {}
            .border(1.dp, if (hervorgehoben) farben.akzent.copy(alpha = 0.55f) else farben.linieFein, RoundedCornerShape(3.dp))
            .background(if (hervorgehoben) farben.papierDunkel.copy(alpha = 0.52f) else farben.papier, RoundedCornerShape(3.dp))
            .height(IntrinsicSize.Min),
    ) {
        Box(
            modifier = Modifier
                .width(3.dp)
                .fillMaxHeight()
                .background(akzentLinie),
        )
        Column(
            modifier = Modifier
                .weight(1f)
                .padding(12.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Text(
                text = marke,
                style = MaterialTheme.typography.labelSmall,
                color = if (hervorgehoben) farben.akzent else farben.tinteMatt,
                fontWeight = FontWeight.Bold,
            )
            Text(
                text = text,
                style = MaterialTheme.typography.bodyMedium,
                color = farben.tinte,
            )
        }
    }
}
