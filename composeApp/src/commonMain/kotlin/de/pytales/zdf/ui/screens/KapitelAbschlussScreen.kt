package de.pytales.zdf.ui.screens

import androidx.compose.foundation.BorderStroke
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
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.components.ArchivTrennlinie
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.state.UiStateMapper
import de.pytales.zdf.ui.theme.ArchivTheme

/**
 * Jahresrückblick (`GamePhase.KapitelAbschluss`) im ruhigen Buchdruck-Querformat:
 * links der historische Jahresrückblick samt persönlichem Befindenszitat,
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
    val zeigeRandLeiste = uiState.kopfleisteEingeklappt && metrik.kopfNebeneinander
    val gameState = uiState.gameState

    val abschlussUi = remember(engine, phase, gameState.pfad, gameState.werte) {
        UiStateMapper.mapKapitelAbschluss(
            content = engine.content,
            phase = phase,
            pfad = gameState.pfad,
            zustandssatz = engine.zustandssatz(gameState),
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
        Box(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState()),
            contentAlignment = Alignment.TopCenter,
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .archivInhaltsSafeArea(ohneRechtenRand = zeigeRandLeiste)
                    .widthIn(max = metrik.maxInhaltsBreite)
                    .padding(
                        horizontal = metrik.aussenAbstand,
                        vertical = if (kompakt) 8.dp else 16.dp,
                    ),
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
                                .background(farben.tinte),
                        )

                        val linkeSpalte: @Composable (Modifier) -> Unit = { mod ->
                            Column(
                                modifier = mod,
                                verticalArrangement = Arrangement.spacedBy(if (kompakt) 9.dp else 12.dp),
                            ) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically,
                                ) {
                                    Text(
                                        text = "Jahresrückblick ${abschlussUi.jahr}",
                                        style = MaterialTheme.typography.labelMedium,
                                        fontFamily = FontFamily.Serif,
                                        color = farben.akzent,
                                        fontWeight = FontWeight.SemiBold,
                                    )
                                    Text(
                                        text = "${abschlussUi.zeitraum} · ${abschlussUi.pfadMarke}",
                                        style = MaterialTheme.typography.labelSmall,
                                        color = farben.tinteMatt,
                                    )
                                }

                                Text(
                                    text = abschlussUi.ueberschrift,
                                    style = if (kompakt) MaterialTheme.typography.headlineSmall else MaterialTheme.typography.headlineMedium,
                                    color = farben.tinte,
                                    modifier = Modifier.archivUeberschrift(),
                                )

                                if (abschlussUi.stichworte.isNotEmpty()) {
                                    Text(
                                        text = abschlussUi.stichworte.joinToString("  ·  "),
                                        style = MaterialTheme.typography.labelSmall,
                                        color = farben.tinteMatt,
                                    )
                                }

                                ArchivTrennlinie(farbe = farben.linieFein.copy(alpha = 0.65f))

                                if (abschlussUi.rueckblick != null) {
                                    Text(
                                        text = abschlussUi.rueckblick,
                                        style = MaterialTheme.typography.bodyLarge,
                                        color = farben.tinte,
                                    )
                                }

                                // Ruhiges persönliches Jahresende-Zitat
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(IntrinsicSize.Min)
                                        .padding(top = 2.dp),
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
                                verticalArrangement = Arrangement.spacedBy(12.dp),
                            ) {
                                BogenHinweisNotiz(
                                    titel = "Historische Leitfrage",
                                    text = abschlussUi.leitfrage,
                                    hervorgehoben = false,
                                )

                                BogenHinweisNotiz(
                                    titel = "Was ${abschlussUi.jahr} kippt · ${abschlussUi.pfadMarke}",
                                    text = abschlussUi.kipppunkt,
                                    hervorgehoben = true,
                                )

                                Spacer(modifier = Modifier.height(2.dp))

                                ArchivPrimaerKnopf(
                                    label = abschlussUi.weiterLabel,
                                    onClick = onNaechstesKapitel,
                                    modifier = Modifier.fillMaxWidth(),
                                )
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
                                linkeSpalte(Modifier.weight(0.54f))
                                rechteSpalte(Modifier.weight(0.46f))
                            }
                        } else {
                            Column(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(metrik.kartenInnenAbstand),
                                verticalArrangement = Arrangement.spacedBy(14.dp),
                            ) {
                                linkeSpalte(Modifier.fillMaxWidth())
                                ArchivTrennlinie()
                                rechteSpalte(Modifier.fillMaxWidth())
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(10.dp))
            }
        }
    }
}

@Composable
private fun BogenHinweisNotiz(
    titel: String,
    text: String,
    hervorgehoben: Boolean,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val akzentLinie = if (hervorgehoben) farben.akzent else farben.linie

    Row(
        modifier = modifier
            .fillMaxWidth()
            .semantics(mergeDescendants = true) {}
            .background(
                if (hervorgehoben) farben.papierDunkel.copy(alpha = 0.48f) else farben.papier.copy(alpha = 0.65f),
                RoundedCornerShape(5.dp),
            )
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
                .padding(horizontal = 12.dp, vertical = 10.dp),
            verticalArrangement = Arrangement.spacedBy(4.dp),
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
