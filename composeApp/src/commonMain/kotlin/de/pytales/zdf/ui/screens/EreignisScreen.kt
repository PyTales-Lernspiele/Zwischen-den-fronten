package de.pytales.zdf.ui.screens

import androidx.compose.animation.AnimatedContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
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
 * Radikal geklärte Buchseiten-Ereignisbühne für `GamePhase.EreignisAnzeige` und `GamePhase.EreignisAusgang`:
 * - **Links:** Ausschließlich die stimmungsvoll gerahmte 16:9-Illustration + genau eine ruhige
 *   Orts-/Jahreszeile darunter (keine zusätzlichen Kästen, Kapitelzeilen oder Zitat-Balken).
 * - **Rechts:** Flache, offene Buchseiten-Typografie direkt auf warmem Archivpapier.
 *   Nach einer Entscheidung wechselt die rechte Seite ruhig in die **Ausgangs-Ansicht**
 *   (statt alte Entscheidungsbuttons stehen zu lassen und den Ausgang darunter zu stapeln) —
 *   vollständig auf einen Blick lesbar, ohne Scroll-Chaos.
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
    val kompakt = metrik.kompakteHoehe
    val istAusgang = phase is GamePhase.EreignisAusgang

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

    val rechterScroll = rememberScrollState()
    val einzelScroll = rememberScrollState()

    // Beim Ereignis- oder Ansichts-Wechsel (Entscheidung -> Ausgang) sauber oben beginnen
    LaunchedEffect(ereignis.id, istAusgang) {
        rechterScroll.scrollTo(0)
        einzelScroll.scrollTo(0)
    }

    // Dezenter oberer Abstand rechts, wenn die kleine Kopfleisten-Lasche oben rechts schwebt
    val laschenLuftOben = if (uiState.kopfleisteEingeklappt) 26.dp else 0.dp

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
                                start = metrik.aussenAbstand,
                                end = metrik.aussenAbstand,
                                top = if (kompakt) 10.dp else 20.dp,
                                bottom = if (kompakt) 10.dp else 20.dp,
                            )
                            .archivFokusGruppe(),
                        horizontalArrangement = Arrangement.spacedBy(if (kompakt) 20.dp else 32.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        // Linke Buchseite: NUR 16:9-Illustration + eine ruhige Orts-/Jahreszeile
                        Box(
                            modifier = Modifier
                                .weight(0.44f)
                                .fillMaxHeight(),
                            contentAlignment = Alignment.Center,
                        ) {
                            SzenenbildRahmen(szenenbild = kartenUi.szenenbild)
                        }

                        // Rechte Buchseite: offene Typografie — wechselt ruhig von Entscheidung zu Ausgang
                        Box(
                            modifier = Modifier
                                .weight(0.56f)
                                .fillMaxHeight()
                                .verticalScroll(rechterScroll)
                                .padding(top = laschenLuftOben),
                            contentAlignment = Alignment.CenterStart,
                        ) {
                            AnimatedContent(
                                targetState = istAusgang,
                                transitionSpec = { ArchivUebergaenge.phasenTransitionSpec(reduziert) },
                                label = "ereignisRechteSeite",
                                modifier = Modifier.fillMaxWidth(),
                            ) { zeigeAusgang ->
                                if (zeigeAusgang && ausgangUi != null) {
                                    EreignisAusgangKarte(
                                        ausgang = ausgangUi,
                                        weiterLabel = weiterLabel,
                                        quelle = kartenUi.quelle,
                                        onWeiter = onWeiterNachAusgang,
                                    )
                                } else {
                                    EntscheidungsKarte(
                                        karte = kartenUi,
                                        ausgewaehlteOptionIndex = null,
                                        optionenAktiv = true,
                                        onOptionWaehlen = onOptionWaehlen,
                                    )
                                }
                            }
                        }
                    }
                }
            } else {
                // Schmale Fenster (< 600 dp): sauberer vertikaler Buchfluss, Entscheidung -> Ausgang im Wechsel
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
                            .padding(
                                start = metrik.aussenAbstand,
                                end = metrik.aussenAbstand,
                                top = if (uiState.kopfleisteEingeklappt) 34.dp else 14.dp,
                                bottom = 18.dp,
                            )
                            .archivFokusGruppe(),
                        verticalArrangement = Arrangement.spacedBy(16.dp),
                    ) {
                        SzenenbildRahmen(szenenbild = kartenUi.szenenbild)

                        AnimatedContent(
                            targetState = istAusgang,
                            transitionSpec = { ArchivUebergaenge.phasenTransitionSpec(reduziert) },
                            label = "ereignisEinzelSeite",
                            modifier = Modifier.fillMaxWidth(),
                        ) { zeigeAusgang ->
                            if (zeigeAusgang && ausgangUi != null) {
                                EreignisAusgangKarte(
                                    ausgang = ausgangUi,
                                    weiterLabel = weiterLabel,
                                    quelle = kartenUi.quelle,
                                    onWeiter = onWeiterNachAusgang,
                                )
                            } else {
                                EntscheidungsKarte(
                                    karte = kartenUi,
                                    ausgewaehlteOptionIndex = null,
                                    optionenAktiv = true,
                                    onOptionWaehlen = onOptionWaehlen,
                                )
                            }
                        }

                        Spacer(modifier = Modifier.height(6.dp))
                    }
                }
            }
        }
    }
}
