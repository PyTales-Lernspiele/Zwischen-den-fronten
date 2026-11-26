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
import de.pytales.zdf.ui.components.ArchivStempel
import de.pytales.zdf.ui.components.ArchivTrennlinie
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.state.UiStateMapper
import de.pytales.zdf.ui.theme.ArchivTheme

/**
 * Musterungsergebnis-Blatt (`GamePhase.MusterungErgebnis`) im Stil einer ruhigen
 * amtlichen Urkunde — im Querformat übersichtlich zweispaltig gegliedert.
 */
@Composable
fun MusterungErgebnisScreen(
    engine: GameEngine,
    uiState: SpielUiState,
    phase: GamePhase.MusterungErgebnis,
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
    val zeigeRandLeiste = uiState.kopfleisteEingeklappt && metrik.kopfNebeneinander
    val musterungUi = remember(engine.content, phase, uiState.gameState.person) {
        UiStateMapper.mapMusterungErgebnis(engine.content, phase, uiState.gameState.person)
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
                    border = BorderStroke(0.9.dp, farben.linie.copy(alpha = 0.78f)),
                    shadowElevation = 2.dp,
                ) {
                    Column(modifier = Modifier.fillMaxWidth()) {
                        // Amtlicher Dokumentkopf
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .background(farben.papierDunkel.copy(alpha = 0.42f))
                                .padding(
                                    horizontal = metrik.kartenInnenAbstand,
                                    vertical = if (kompakt) 9.dp else 12.dp,
                                ),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            Column(
                                modifier = Modifier.weight(1f),
                                verticalArrangement = Arrangement.spacedBy(2.dp),
                            ) {
                                Text(
                                    text = "Musterungsbescheid",
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
                                hintergrund = farben.papierHell,
                            )
                        }
                        ArchivTrennlinie(farbe = farben.tinte.copy(alpha = 0.55f), doppelt = true)

                        val befundSpalte: @Composable (Modifier) -> Unit = { mod ->
                            Column(
                                modifier = mod,
                                verticalArrangement = Arrangement.spacedBy(10.dp),
                            ) {
                                Text(
                                    text = "${musterungUi.gradKurz} — ${musterungUi.gradLang}",
                                    style = MaterialTheme.typography.titleLarge,
                                    color = farben.akzent,
                                )
                                Text(
                                    text = musterungUi.gradErklaerung,
                                    style = MaterialTheme.typography.bodyMedium,
                                    color = farben.tinte,
                                )

                                if (musterungUi.vermerkLang != null && musterungUi.vermerkErklaerung != null) {
                                    Row(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .height(IntrinsicSize.Min)
                                            .background(farben.papier.copy(alpha = 0.7f), RoundedCornerShape(4.dp)),
                                    ) {
                                        Box(
                                            modifier = Modifier
                                                .width(2.5.dp)
                                                .fillMaxHeight()
                                                .background(farben.akzent),
                                        )
                                        Column(
                                            modifier = Modifier
                                                .weight(1f)
                                                .padding(horizontal = 12.dp, vertical = 8.dp),
                                            verticalArrangement = Arrangement.spacedBy(3.dp),
                                        ) {
                                            Text(
                                                text = "Vermerk: ${musterungUi.vermerkKurz} — ${musterungUi.vermerkLang}",
                                                style = MaterialTheme.typography.titleSmall,
                                                color = farben.akzent,
                                            )
                                            Text(
                                                text = musterungUi.vermerkErklaerung,
                                                style = MaterialTheme.typography.bodySmall,
                                                color = farben.tinte,
                                            )
                                        }
                                    }
                                }

                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(IntrinsicSize.Min)
                                        .background(farben.papier.copy(alpha = 0.55f), RoundedCornerShape(4.dp)),
                                ) {
                                    Box(
                                        modifier = Modifier
                                            .width(2.5.dp)
                                            .fillMaxHeight()
                                            .background(farben.tinte),
                                    )
                                    Column(
                                        modifier = Modifier
                                            .weight(1f)
                                            .padding(horizontal = 12.dp, vertical = 8.dp),
                                        verticalArrangement = Arrangement.spacedBy(2.dp),
                                    ) {
                                        Text(
                                            text = "Zuweisung: ${musterungUi.zielPfadMarke}",
                                            style = MaterialTheme.typography.titleSmall,
                                            color = farben.tinte,
                                        )
                                        Text(
                                            text = musterungUi.zielPfadFolge,
                                            style = MaterialTheme.typography.bodySmall,
                                            fontStyle = FontStyle.Italic,
                                            color = farben.tinteMatt,
                                        )
                                    }
                                }
                            }
                        }

                        val aktenSpalte: @Composable (Modifier) -> Unit = { mod ->
                            Column(
                                modifier = mod,
                                verticalArrangement = Arrangement.spacedBy(8.dp),
                            ) {
                                val eintraege = buildList {
                                    add(
                                        "Gemusterter" to buildString {
                                            append(musterungUi.personName)
                                            if (musterungUi.jahrgang != null) {
                                                append(" (Jg. ${musterungUi.jahrgang})")
                                            }
                                        },
                                    )
                                    add(
                                        "Herkunft & Beruf" to listOf(
                                            musterungUi.herkunftTitel,
                                            musterungUi.friedensberuf,
                                        ).filter { it.isNotBlank() }.joinToString(" · "),
                                    )
                                    add("Heeresklasse" to musterungUi.heeresklasse)
                                    add("Ärztlicher Befund" to musterungUi.befund)
                                    if (musterungUi.groesseCm != null && musterungUi.brustumfangCm != null) {
                                        add(
                                            "Körpermaße" to "${musterungUi.groesseCm} cm · Brustumfang ${musterungUi.brustumfangCm} cm",
                                        )
                                    }
                                }

                                eintraege.forEachIndexed { idx, (feld, wert) ->
                                    AktenEintragZeile(feld = feld, wert = wert)
                                    if (idx < eintraege.lastIndex) {
                                        ArchivTrennlinie(farbe = farben.linieFein.copy(alpha = 0.55f))
                                    }
                                }

                                Spacer(modifier = Modifier.height(4.dp))

                                ArchivPrimaerKnopf(
                                    label = "Bescheid entgegennehmen",
                                    onClick = onBestaetigen,
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
                                befundSpalte(Modifier.weight(0.46f))
                                aktenSpalte(Modifier.weight(0.54f))
                            }
                        } else {
                            Column(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(metrik.kartenInnenAbstand),
                                verticalArrangement = Arrangement.spacedBy(14.dp),
                            ) {
                                befundSpalte(Modifier.fillMaxWidth())
                                ArchivTrennlinie()
                                aktenSpalte(Modifier.fillMaxWidth())
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
private fun AktenEintragZeile(
    feld: String,
    wert: String,
) {
    val farben = ArchivTheme.farben
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .semantics(mergeDescendants = true) {}
            .padding(vertical = 2.dp),
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        verticalAlignment = Alignment.Top,
    ) {
        Text(
            text = feld,
            style = MaterialTheme.typography.labelMedium,
            color = farben.tinteMatt,
            modifier = Modifier.widthIn(min = 120.dp, max = 140.dp),
        )
        Text(
            text = wert,
            style = MaterialTheme.typography.bodySmall,
            color = farben.tinte,
            modifier = Modifier.weight(1f),
        )
    }
}
