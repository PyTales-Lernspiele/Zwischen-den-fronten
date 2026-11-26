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
import de.pytales.zdf.ui.components.ArchivStempel
import de.pytales.zdf.ui.components.ArchivTrennlinie
import de.pytales.zdf.ui.components.archivFokusGruppe
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.state.UiStateMapper
import de.pytales.zdf.ui.theme.ArchivTheme

/**
 * Musterungsergebnis-Blatt (`GamePhase.MusterungErgebnis`) als ruhige, offene Akten-Buchseite:
 * ohne verschachtelte graue Boxen und ohne überladene Trennlinien — klare Hierarchie aus
 * Tauglichkeitsbefund links und knappen Personendaten + Bestätigung rechts.
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
    val musterungUi = remember(engine.content, phase, uiState.gameState.person) {
        UiStateMapper.mapMusterungErgebnis(engine.content, phase, uiState.gameState.person)
    }
    val topAbstand = if (uiState.kopfleisteEingeklappt) 34.dp else if (kompakt) 12.dp else 22.dp

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
                        bottom = if (kompakt) 14.dp else 24.dp,
                    )
                    .archivFokusGruppe(),
                verticalArrangement = Arrangement.spacedBy(if (kompakt) 14.dp else 20.dp),
            ) {
                // Schlichter Dokumentkopf ohne Kastenrahmen
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        Column(
                            modifier = Modifier.weight(1f),
                            verticalArrangement = Arrangement.spacedBy(2.dp),
                        ) {
                            Text(
                                text = "Musterungsbescheid",
                                style = if (kompakt) MaterialTheme.typography.headlineSmall else MaterialTheme.typography.headlineMedium,
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
                    ArchivTrennlinie(farbe = farben.tinte.copy(alpha = 0.45f), doppelt = true)
                }

                val befundSpalte: @Composable (Modifier) -> Unit = { mod ->
                    Column(
                        modifier = mod,
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        Text(
                            text = "${musterungUi.gradKurz} — ${musterungUi.gradLang}",
                            style = MaterialTheme.typography.titleLarge,
                            fontFamily = FontFamily.Serif,
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
                                    .height(IntrinsicSize.Min),
                                horizontalArrangement = Arrangement.spacedBy(10.dp),
                            ) {
                                Box(
                                    modifier = Modifier
                                        .width(2.dp)
                                        .fillMaxHeight()
                                        .background(farben.akzent),
                                )
                                Column(
                                    modifier = Modifier.weight(1f),
                                    verticalArrangement = Arrangement.spacedBy(2.dp),
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
                                .height(IntrinsicSize.Min),
                            horizontalArrangement = Arrangement.spacedBy(10.dp),
                        ) {
                            Box(
                                modifier = Modifier
                                    .width(2.dp)
                                    .fillMaxHeight()
                                    .background(farben.tinte.copy(alpha = 0.65f)),
                            )
                            Column(
                                modifier = Modifier.weight(1f),
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
                        verticalArrangement = Arrangement.spacedBy(9.dp),
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
                            add("Befund" to musterungUi.befund)
                            if (musterungUi.groesseCm != null && musterungUi.brustumfangCm != null) {
                                add(
                                    "Körpermaße" to "${musterungUi.groesseCm} cm · Brustumfang ${musterungUi.brustumfangCm} cm",
                                )
                            }
                        }

                        eintraege.forEach { (feld, wert) ->
                            AktenEintragZeile(feld = feld, wert = wert)
                        }

                        Spacer(modifier = Modifier.height(6.dp))

                        ArchivPrimaerKnopf(
                            label = "Bescheid entgegennehmen",
                            klickEffekt = SoundEffekt.ENTSCHEIDUNG,
                            onClick = onBestaetigen,
                            modifier = Modifier.fillMaxWidth(),
                        )
                    }
                }

                if (metrik.zweispaltigeBuehne) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(if (kompakt) 24.dp else 36.dp),
                        verticalAlignment = Alignment.Top,
                    ) {
                        befundSpalte(Modifier.weight(0.48f))
                        aktenSpalte(Modifier.weight(0.52f))
                    }
                } else {
                    Column(verticalArrangement = Arrangement.spacedBy(18.dp)) {
                        befundSpalte(Modifier.fillMaxWidth())
                        ArchivTrennlinie(farbe = farben.linieFein.copy(alpha = 0.6f))
                        aktenSpalte(Modifier.fillMaxWidth())
                    }
                }
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
            .semantics(mergeDescendants = true) {},
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        verticalAlignment = Alignment.Top,
    ) {
        Text(
            text = feld,
            style = MaterialTheme.typography.labelMedium,
            color = farben.tinteMatt,
            modifier = Modifier.widthIn(min = 110.dp, max = 128.dp),
        )
        Text(
            text = wert,
            style = MaterialTheme.typography.bodySmall,
            color = farben.tinte,
            modifier = Modifier.weight(1f),
        )
    }
}
