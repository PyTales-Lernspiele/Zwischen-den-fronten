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
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontFamily
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
 * Musterungsergebnis-Blatt (`GamePhase.MusterungErgebnis`) im Stil einer amtlichen Verfügung:
 * zeigt Tauglichkeitsgrad (`k. v.` / `g. v.` / `a. v.` / `d. u.`), optionalen Vermerk (`u. k.` / `zurückgestellt`),
 * ärztlichen Befund, Heeresklasse, Körpermaße und Zielpfad.
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun MusterungErgebnisScreen(
    engine: GameEngine,
    uiState: SpielUiState,
    phase: GamePhase.MusterungErgebnis,
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
    val musterungUi = remember(engine.content, phase, uiState.gameState.person) {
        UiStateMapper.mapMusterungErgebnis(engine.content, phase, uiState.gameState.person)
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
                    border = BorderStroke(1.5.dp, farben.tinte.copy(alpha = 0.72f)),
                    shadowElevation = 1.dp,
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(4.dp)
                            .border(0.75.dp, farben.linieFein, RoundedCornerShape(2.dp)),
                    ) {
                        // Amtlicher Dokumentkopf
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .background(farben.papierDunkel.copy(alpha = 0.65f)),
                        ) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(horizontal = metrik.kartenInnenAbstand, vertical = 12.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically,
                            ) {
                                Column(
                                    modifier = Modifier.weight(1f),
                                    verticalArrangement = Arrangement.spacedBy(2.dp),
                                ) {
                                    Text(
                                        text = "MUSTERUNGSBESCHEID",
                                        style = MaterialTheme.typography.headlineSmall,
                                        fontFamily = FontFamily.Serif,
                                        color = farben.tinte,
                                        fontWeight = FontWeight.Bold,
                                        modifier = Modifier.archivUeberschrift(),
                                    )
                                    Text(
                                        text = "Ersatzkommission · ${musterungUi.anlassBezeichnung}",
                                        style = MaterialTheme.typography.labelSmall,
                                        color = farben.tinteMatt,
                                    )
                                }
                                ArchivStempel(
                                    text = musterungUi.gradKurz,
                                    farbe = farben.akzent,
                                    grossbuchstaben = true,
                                )
                            }
                            ArchivTrennlinie(farbe = farben.tinte.copy(alpha = 0.7f), doppelt = true)
                        }

                        // Hauptinhalt
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(metrik.kartenInnenAbstand),
                            verticalArrangement = Arrangement.spacedBy(14.dp),
                        ) {
                            // Tauglichkeitsgrad & Vermerk hervorgehoben
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .background(farben.papier, RoundedCornerShape(3.dp))
                                    .border(1.dp, farben.linie, RoundedCornerShape(3.dp))
                                    .padding(14.dp),
                            ) {
                                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                    FlowRow(
                                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                                        verticalArrangement = Arrangement.spacedBy(6.dp),
                                    ) {
                                        ArchivStempel(
                                            text = "TAUGLICHKEIT: ${musterungUi.gradKurz}",
                                            farbe = farben.akzent,
                                        )
                                        if (musterungUi.vermerkKurz != null) {
                                            ArchivStempel(
                                                text = "VERMERK: ${musterungUi.vermerkKurz}",
                                                farbe = farben.tinte,
                                                hintergrund = farben.papierDunkel,
                                            )
                                        }
                                        ArchivStempel(
                                            text = "ZIELPFAD: ${musterungUi.zielPfadMarke}",
                                            farbe = farben.tinte,
                                            hintergrund = farben.papierHell,
                                        )
                                    }

                                    Text(
                                        text = "${musterungUi.gradKurz} — ${musterungUi.gradLang}",
                                        style = MaterialTheme.typography.titleLarge,
                                        color = farben.tinte,
                                    )
                                    Text(
                                        text = musterungUi.gradErklaerung,
                                        style = MaterialTheme.typography.bodyLarge,
                                        color = farben.tinte,
                                    )

                                    if (musterungUi.vermerkLang != null && musterungUi.vermerkErklaerung != null) {
                                        ArchivTrennlinie(farbe = farben.linieFein)
                                        Text(
                                            text = "Zusatzvermerk: ${musterungUi.vermerkKurz} — ${musterungUi.vermerkLang}",
                                            style = MaterialTheme.typography.titleSmall,
                                            color = farben.akzent,
                                        )
                                        Text(
                                            text = musterungUi.vermerkErklaerung,
                                            style = MaterialTheme.typography.bodyMedium,
                                            color = farben.tinte,
                                        )
                                    }
                                }
                            }

                            // Akten-Zeilen: Person, Befund, Heeresklasse, Zielpfad
                            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                AktenZeile(
                                    feld = "Gemusterter",
                                    wert = buildString {
                                        append(musterungUi.personName)
                                        if (musterungUi.jahrgang != null) {
                                            append(" (Jahrgang ${musterungUi.jahrgang})")
                                        }
                                    },
                                )
                                AktenZeile(
                                    feld = "Herkunft & Beruf",
                                    wert = listOf(musterungUi.herkunftTitel, musterungUi.friedensberuf)
                                        .filter { it.isNotBlank() }
                                        .joinToString(" · "),
                                )
                                AktenZeile(
                                    feld = "Heeresklasse",
                                    wert = musterungUi.heeresklasse,
                                )
                                AktenZeile(
                                    feld = "Ärztlicher Befund",
                                    wert = musterungUi.befund,
                                )
                                if (musterungUi.groesseCm != null && musterungUi.brustumfangCm != null) {
                                    AktenZeile(
                                        feld = "Körpermaße",
                                        wert = "${musterungUi.groesseCm} cm · Brustumfang ${musterungUi.brustumfangCm} cm",
                                    )
                                }
                                AktenZeile(
                                    feld = "Zuweisung",
                                    wert = "${musterungUi.zielPfadMarke} (${musterungUi.zielPfadOrt}) — ${musterungUi.zielPfadFolge}",
                                )
                            }

                            ArchivTrennlinie(farbe = farben.linieFein)

                            ArchivPrimaerKnopf(
                                label = "Musterungsbescheid entgegennehmen",
                                onClick = onBestaetigen,
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
private fun AktenZeile(
    feld: String,
    wert: String,
) {
    val farben = ArchivTheme.farben
    val kompakt = ArchivTheme.layoutKlasse == LayoutKlasse.KOMPAKT

    if (kompakt) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .semantics(mergeDescendants = true) {}
                .border(0.75.dp, farben.linieFein, RoundedCornerShape(2.dp))
                .background(farben.papier.copy(alpha = 0.45f), RoundedCornerShape(2.dp))
                .padding(horizontal = 10.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(2.dp),
        ) {
            Text(
                text = feld.uppercase(),
                style = MaterialTheme.typography.labelSmall,
                color = farben.tinteMatt,
            )
            Text(
                text = wert,
                style = MaterialTheme.typography.bodyMedium,
                color = farben.tinte,
            )
        }
    } else {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .semantics(mergeDescendants = true) {}
                .border(0.75.dp, farben.linieFein, RoundedCornerShape(2.dp))
                .background(farben.papier.copy(alpha = 0.45f), RoundedCornerShape(2.dp))
                .padding(horizontal = 12.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalAlignment = Alignment.Top,
        ) {
            Text(
                text = feld,
                style = MaterialTheme.typography.labelLarge,
                color = farben.tinteMatt,
                modifier = Modifier.widthIn(min = 160.dp, max = 180.dp),
            )
            Text(
                text = wert,
                style = MaterialTheme.typography.bodyMedium,
                color = farben.tinte,
                modifier = Modifier.weight(1f),
            )
        }
    }
}
