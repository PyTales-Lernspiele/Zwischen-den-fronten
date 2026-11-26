package de.pytales.zdf.ui.screens

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
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
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
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
import de.pytales.zdf.ui.theme.LayoutKlasse
import de.pytales.zdf.ui.theme.Schriftgroesse

/**
 * Durchgängiger Ereignis-Bildschirm für `GamePhase.EreignisAnzeige` und `GamePhase.EreignisAusgang`:
 * verbindet [SpielKopfLeiste] (`BefindensLeiste` + `LiveEmotionsKachel` mit AP-5-Portrait-Loader),
 * [SzenenbildRahmen] (mit automatischem Stufe-2→Stufe-1→Platzhalter-Loader),
 * [EntscheidungsKarte] (alle 5 Kartentypen, genau 2 Entscheidungen) und [EreignisAusgangKarte]
 * mit ruhigen, abschaltbaren Kartenwechseln (`ArchivUebergaenge`).
 */
@Composable
fun EreignisScreen(
    engine: GameEngine,
    uiState: SpielUiState,
    onOptionWaehlen: (Int) -> Unit,
    onWeiterNachAusgang: () -> Unit,
    onSchriftgroesseChange: (Schriftgroesse) -> Unit,
    onAnalyseModusToggle: () -> Unit,
    onAudioToggle: () -> Unit = {},
    onWertErklaerungChange: (WertSchluessel?) -> Unit,
    onEmotionDetailsOffenChange: (Boolean) -> Unit = {},
    modifier: Modifier = Modifier,
) {
    val gameState = uiState.gameState
    val phase = gameState.phase
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val layoutKlasse = ArchivTheme.layoutKlasse
    val reduziert = ArchivTheme.reduzierteAnimationen
    val uebergangsProfil = remember(reduziert) { ArchivUebergaenge.profilFuer(reduziert) }
    val scrollState = rememberScrollState()

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

    // Beim Wechsel auf ein neues Ereignis ruhig nach oben scrollen
    LaunchedEffect(ereignis.id) {
        scrollState.scrollTo(0)
    }

    // Im Hochformat nach Wahl einer Option zur neuen Ausgangskarte scrollen (mit Respekt für reduzierte Animationen)
    LaunchedEffect(phase is GamePhase.EreignisAusgang, layoutKlasse, uebergangsProfil.sanftScrollen) {
        if (phase is GamePhase.EreignisAusgang && layoutKlasse != LayoutKlasse.BREIT) {
            if (uebergangsProfil.sanftScrollen) {
                scrollState.animateScrollTo(scrollState.maxValue)
            } else {
                scrollState.scrollTo(scrollState.maxValue)
            }
        }
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
            onEmotionDetailsOffenChange = onEmotionDetailsOffenChange,
        )

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .verticalScroll(scrollState),
            contentAlignment = Alignment.TopCenter,
        ) {
            AnimatedContent(
                targetState = ereignis.id,
                transitionSpec = { ArchivUebergaenge.phasenTransitionSpec(reduziert) },
                label = "ereignisKartenWechsel",
                modifier = Modifier
                    .fillMaxWidth()
                    .archivInhaltsSafeArea()
                    .widthIn(max = metrik.maxInhaltsBreite),
            ) { _ ->
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = metrik.aussenAbstand, vertical = metrik.elementAbstand)
                        .archivFokusGruppe(),
                    verticalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
                ) {
                    val buehneNebeneinander = layoutKlasse == LayoutKlasse.BREIT

                    if (buehneNebeneinander) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
                            verticalAlignment = Alignment.Top,
                        ) {
                            Column(
                                modifier = Modifier.weight(0.42f),
                                verticalArrangement = Arrangement.spacedBy(10.dp),
                            ) {
                                SzenenbildRahmen(
                                    szenenbild = kartenUi.szenenbild,
                                    analyseModus = uiState.analyseModus,
                                )
                                BefindensNotizBox(zustandssatz = zustandssatz)
                            }

                            Column(
                                modifier = Modifier.weight(0.58f),
                                verticalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
                            ) {
                                EntscheidungsKarte(
                                    karte = kartenUi,
                                    ausgewaehlteOptionIndex = (phase as? GamePhase.EreignisAusgang)?.gewaehlteOptionIndex,
                                    optionenAktiv = phase is GamePhase.EreignisAnzeige,
                                    analyseModus = uiState.analyseModus,
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
                            }
                        }
                    } else {
                        SzenenbildRahmen(
                            szenenbild = kartenUi.szenenbild,
                            analyseModus = uiState.analyseModus,
                        )

                        EntscheidungsKarte(
                            karte = kartenUi,
                            ausgewaehlteOptionIndex = (phase as? GamePhase.EreignisAusgang)?.gewaehlteOptionIndex,
                            optionenAktiv = phase is GamePhase.EreignisAnzeige,
                            analyseModus = uiState.analyseModus,
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

                        BefindensNotizBox(zustandssatz = zustandssatz)
                    }

                    Spacer(modifier = Modifier.height(16.dp))
                }
            }
        }
    }
}

@Composable
private fun BefindensNotizBox(
    zustandssatz: String,
) {
    val farben = ArchivTheme.farben
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .semantics(mergeDescendants = true) {}
            .border(1.dp, farben.linieFein, RoundedCornerShape(3.dp))
            .background(farben.papierHell.copy(alpha = 0.72f), RoundedCornerShape(3.dp))
            .padding(12.dp),
        verticalArrangement = Arrangement.spacedBy(4.dp),
    ) {
        Text(
            text = "Aktuelle Lage",
            style = MaterialTheme.typography.labelSmall,
            color = farben.tinteMatt,
            fontWeight = FontWeight.SemiBold,
        )
        Text(
            text = "„$zustandssatz“",
            style = MaterialTheme.typography.bodyMedium,
            fontStyle = FontStyle.Italic,
            color = farben.tinte,
        )
    }
}
