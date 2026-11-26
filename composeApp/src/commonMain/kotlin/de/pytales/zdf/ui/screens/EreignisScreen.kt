package de.pytales.zdf.ui.screens

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.AnimatedVisibility
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
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.unit.dp
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.engine.TextResolver
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.components.EntscheidungsKarte
import de.pytales.zdf.ui.components.EreignisAusgangKarte
import de.pytales.zdf.ui.components.SzenenbildRahmen
import de.pytales.zdf.ui.components.archivFokusGruppe
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.state.UiStateMapper
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.ArchivUebergaenge

/**
 * Landscape-First-Ereignisbühne für `GamePhase.EreignisAnzeige` und `GamePhase.EreignisAusgang`:
 * - Oben: schlanke, ein-/ausklappbare Kopfleiste via [SpielBuehnenRahmen]
 * - Im Querformat (`MITTEL` & `BREIT`): zweispaltige Buch-Bühne — links bleibt die
 *   stimmungsvoll gerahmte 16:9-Illustration samt ruhiger Orts-/Jahresangabe und Befindens-Notiz
 *   ruhig sichtbar, rechts stehen Erzählkarte, die beiden Entscheidungen und der Ausgang.
 */
@Composable
fun EreignisScreen(
    engine: GameEngine,
    uiState: SpielUiState,
    onOptionWaehlen: (Int) -> Unit,
    onWeiterNachAusgang: () -> Unit,
    onAudioToggle: () -> Unit,
    onEinstellungenOeffnen: () -> Unit,
    onKopfleisteToggle: () -> Unit,
    onWertErklaerungChange: (WertSchluessel?) -> Unit,
    onEmotionDetailsOffenChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier,
) {
    val gameState = uiState.gameState
    val phase = gameState.phase
    val metrik = ArchivTheme.metrik
    val reduziert = ArchivTheme.reduzierteAnimationen
    val uebergangsProfil = remember(reduziert) { ArchivUebergaenge.profilFuer(reduziert) }
    val zeigeRandLeiste = uiState.kopfleisteEingeklappt && metrik.kopfNebeneinander

    val ereignis = when (phase) {
        is GamePhase.EreignisAnzeige -> phase.ereignis
        is GamePhase.EreignisAusgang -> phase.ereignis
        else -> return
    }

    val aufgeloesterText = remember(phase, gameState.jahr, gameState.pfad, gameState.merkmale) {
        when (phase) {
            is GamePhase.EreignisAnzeige -> phase.aufgeloesterText
            is GamePhase.EreignisAusgang -> TextResolver.aufloesen(
                fassung = phase.ereignis.text,
                jahr = gameState.jahr,
                pfad = gameState.pfad,
                merkmale = gameState.merkmale,
                textPrioritaet = engine.content.merkmale.textPrioritaet,
            )

            else -> ereignis.text.standard
        }
    }

    val kartenUi = remember(engine.content, ereignis, aufgeloesterText, gameState.jahr, gameState.pfad) {
        UiStateMapper.mapEntscheidungsKarte(
            content = engine.content,
            ereignis = ereignis,
            aufgeloesterText = aufgeloesterText,
            jahr = gameState.jahr,
            pfad = gameState.pfad,
        )
    }

    val ausgangUi = remember(engine, phase) {
        if (phase is GamePhase.EreignisAusgang) {
            UiStateMapper.mapEreignisAusgang(engine, phase)
        } else {
            null
        }
    }

    val weiterLabel = remember(engine, gameState, phase) {
        if (phase is GamePhase.EreignisAusgang) {
            UiStateMapper.mapWeiterLabel(engine, gameState, phase)
        } else {
            "Weiter"
        }
    }

    val zustandssatz = remember(engine, gameState.werte) {
        engine.zustandssatz(gameState)
    }

    val kapitelHinweis = remember(engine.content, gameState) {
        UiStateMapper.mapKopfKapitelTitel(engine.content, gameState)
    }

    val rechterScroll = rememberScrollState()
    val einzelScroll = rememberScrollState()

    // Beim Wechsel auf ein neues Ereignis ruhig nach oben scrollen
    LaunchedEffect(ereignis.id) {
        rechterScroll.scrollTo(0)
        einzelScroll.scrollTo(0)
    }

    // Nach Wahl einer Option sanft zur Ausgangskarte scrollen (mit Respekt für reduzierte Animationen)
    LaunchedEffect(phase is GamePhase.EreignisAusgang, metrik.zweispaltigeBuehne, uebergangsProfil.sanftScrollen) {
        if (phase is GamePhase.EreignisAusgang) {
            val zielScroll = if (metrik.zweispaltigeBuehne) rechterScroll else einzelScroll
            if (uebergangsProfil.sanftScrollen) {
                zielScroll.animateScrollTo(zielScroll.maxValue)
            } else {
                zielScroll.scrollTo(zielScroll.maxValue)
            }
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
        AnimatedContent(
            targetState = ereignis.id,
            transitionSpec = { ArchivUebergaenge.phasenTransitionSpec(reduziert) },
            label = "ereignisKartenWechsel",
            modifier = Modifier.fillMaxSize(),
        ) { _ ->
            if (metrik.zweispaltigeBuehne) {
                // Echte zweispaltige Querformat-Bühne: links ruhendes 16:9-Motiv, rechts Erzählkarte
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.TopCenter,
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxSize()
                            .archivInhaltsSafeArea(ohneRechtenRand = zeigeRandLeiste)
                            .widthIn(max = metrik.maxInhaltsBreite)
                            .padding(
                                horizontal = metrik.aussenAbstand,
                                vertical = if (metrik.kompakteHoehe) 8.dp else 14.dp,
                            )
                            .archivFokusGruppe(),
                        horizontalArrangement = Arrangement.spacedBy(if (metrik.kompakteHoehe) 12.dp else 18.dp),
                        verticalAlignment = Alignment.Top,
                    ) {
                        // Linke Bildspalte (bleibt beim Lesen rechts ruhig stehen, bei Bedarf selbst scrollbar)
                        Column(
                            modifier = Modifier
                                .weight(0.43f)
                                .fillMaxHeight()
                                .verticalScroll(rememberScrollState()),
                            verticalArrangement = Arrangement.spacedBy(8.dp),
                        ) {
                            SzenenbildRahmen(szenenbild = kartenUi.szenenbild)

                            if (!kapitelHinweis.isNullOrBlank()) {
                                Text(
                                    text = kapitelHinweis,
                                    style = MaterialTheme.typography.labelSmall,
                                    color = ArchivTheme.farben.tinteMatt,
                                    modifier = Modifier.padding(horizontal = 4.dp),
                                )
                            }

                            BefindensNotizFluestern(zustandssatz = zustandssatz)
                        }

                        // Rechte Erzähl- & Entscheidungsspalte (unabhängig ruhig scrollbar)
                        Column(
                            modifier = Modifier
                                .weight(0.57f)
                                .fillMaxHeight()
                                .verticalScroll(rechterScroll),
                            verticalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
                        ) {
                            EntscheidungsKarte(
                                karte = kartenUi,
                                ausgewaehlteOptionIndex = (phase as? GamePhase.EreignisAusgang)?.gewaehlteOptionIndex,
                                optionenAktiv = phase is GamePhase.EreignisAnzeige,
                                onOptionWaehlen = onOptionWaehlen,
                            )

                            AnimatedVisibility(
                                visible = ausgangUi != null,
                                enter = ArchivUebergaenge.aufklappEnter(reduziert),
                                exit = ArchivUebergaenge.aufklappExit(reduziert),
                            ) {
                                if (ausgangUi != null) {
                                    EreignisAusgangKarte(
                                        ausgang = ausgangUi,
                                        weiterLabel = weiterLabel,
                                        onWeiter = onWeiterNachAusgang,
                                    )
                                }
                            }

                            Spacer(modifier = Modifier.height(8.dp))
                        }
                    }
                }
            } else {
                // Schmale Fenster (< 600 dp): sauberer vertikaler Lesefluss
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .verticalScroll(einzelScroll),
                    contentAlignment = Alignment.TopCenter,
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .archivInhaltsSafeArea()
                            .widthIn(max = metrik.maxInhaltsBreite)
                            .padding(horizontal = metrik.aussenAbstand, vertical = metrik.elementAbstand)
                            .archivFokusGruppe(),
                        verticalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
                    ) {
                        SzenenbildRahmen(szenenbild = kartenUi.szenenbild)

                        EntscheidungsKarte(
                            karte = kartenUi,
                            ausgewaehlteOptionIndex = (phase as? GamePhase.EreignisAusgang)?.gewaehlteOptionIndex,
                            optionenAktiv = phase is GamePhase.EreignisAnzeige,
                            onOptionWaehlen = onOptionWaehlen,
                        )

                        AnimatedVisibility(
                            visible = ausgangUi != null,
                            enter = ArchivUebergaenge.aufklappEnter(reduziert),
                            exit = ArchivUebergaenge.aufklappExit(reduziert),
                        ) {
                            if (ausgangUi != null) {
                                EreignisAusgangKarte(
                                    ausgang = ausgangUi,
                                    weiterLabel = weiterLabel,
                                    onWeiter = onWeiterNachAusgang,
                                )
                            }
                        }

                        BefindensNotizFluestern(zustandssatz = zustandssatz)

                        Spacer(modifier = Modifier.height(12.dp))
                    }
                }
            }
        }
    }
}

/**
 * Sehr ruhige, ungerahmte Befindens-Randnotiz mit feiner linker Linie statt grauer Box.
 */
@Composable
private fun BefindensNotizFluestern(
    zustandssatz: String,
) {
    val farben = ArchivTheme.farben
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .height(IntrinsicSize.Min)
            .semantics(mergeDescendants = true) {}
            .padding(horizontal = 4.dp, vertical = 2.dp),
        horizontalArrangement = Arrangement.spacedBy(10.dp),
    ) {
        Box(
            modifier = Modifier
                .width(2.dp)
                .fillMaxHeight()
                .background(farben.akzentMatt.copy(alpha = 0.65f)),
        )
        Text(
            text = "„$zustandssatz“",
            style = MaterialTheme.typography.bodySmall,
            fontFamily = FontFamily.Serif,
            fontStyle = FontStyle.Italic,
            color = farben.tinteMatt,
            modifier = Modifier.weight(1f),
        )
    }
}
