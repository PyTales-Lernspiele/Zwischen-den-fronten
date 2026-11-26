package de.pytales.zdf.ui.screens

import androidx.compose.animation.AnimatedContent
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import de.pytales.zdf.audio.AudioKoordinator
import de.pytales.zdf.audio.erstellePlattformAudioAusgabe
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.ui.UiBaukastenDemo
import de.pytales.zdf.ui.state.SpielController
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.ArchivUebergaenge

/**
 * Übergangsschlüssel für ruhige, abschaltbare Phasenwechsel in [SpielScreen].
 * `EreignisAnzeige` und `EreignisAusgang` teilen denselben Schlüssel, damit das Aufklappen
 * des Ausgangs ruhig innerhalb von [EreignisScreen] geschieht, ohne die Kopfleiste flackern zu lassen.
 */
private sealed interface BildschirmSchluessel {
    data object UiVorschau : BildschirmSchluessel
    data object Start : BildschirmSchluessel
    data object HerkunftWahl : BildschirmSchluessel
    data object MusterungErgebnis : BildschirmSchluessel
    data object ErwerbWahl : BildschirmSchluessel
    data class KapitelStart(val jahr: Int) : BildschirmSchluessel
    data object Ereignis : BildschirmSchluessel
    data class KapitelAbschluss(val jahr: Int) : BildschirmSchluessel
    data object Auffangnetz : BildschirmSchluessel
    data object Lebenslauf : BildschirmSchluessel
}

/**
 * Durchgängiger Spielbildschirm-Router für alle Phasen von 1914 bis 1919
 * (inkl. ruhiger, abschaltbarer Phasenwechsel, optionalem dezentem Audio mit harter
 * Musiksperre an Front & Etappe sowie optionalem Zugang zur AP-3-Komponenten-Vorschau).
 */
@Composable
fun SpielScreen(
    controller: SpielController,
    modifier: Modifier = Modifier,
) {
    val uiState by controller.uiState.collectAsState()
    val reduzierteAnimationen = ArchivTheme.reduzierteAnimationen

    // Plattformübergreifende Audio-Steuerung mit harter Musiksperre an Front & Etappe
    val audioKoordinator = remember {
        AudioKoordinator(erstellePlattformAudioAusgabe())
    }
    val audioZustand = uiState.audioZustand
    LaunchedEffect(audioZustand, uiState.zeigeUiVorschau) {
        if (uiState.zeigeUiVorschau) {
            audioKoordinator.stoppe()
        } else {
            audioKoordinator.synchronisiereZustand(audioZustand)
        }
    }
    DisposableEffect(audioKoordinator) {
        onDispose {
            audioKoordinator.freigeben()
        }
    }

    val schluessel: BildschirmSchluessel = when {
        uiState.zeigeUiVorschau -> BildschirmSchluessel.UiVorschau
        else -> when (val phase = uiState.gameState.phase) {
            is GamePhase.Start -> BildschirmSchluessel.Start
            is GamePhase.HerkunftWahl -> BildschirmSchluessel.HerkunftWahl
            is GamePhase.MusterungErgebnis -> BildschirmSchluessel.MusterungErgebnis
            is GamePhase.ErwerbWahl -> BildschirmSchluessel.ErwerbWahl
            is GamePhase.KapitelStart -> BildschirmSchluessel.KapitelStart(phase.kapitel.jahr)
            is GamePhase.EreignisAnzeige,
            is GamePhase.EreignisAusgang,
            -> BildschirmSchluessel.Ereignis

            is GamePhase.KapitelAbschluss -> BildschirmSchluessel.KapitelAbschluss(phase.kapitel.jahr)
            is GamePhase.Abgeschlossen -> if (uiState.istImAuffangnetz) {
                BildschirmSchluessel.Auffangnetz
            } else {
                BildschirmSchluessel.Lebenslauf
            }
        }
    }

    AnimatedContent(
        targetState = schluessel,
        transitionSpec = { ArchivUebergaenge.phasenTransitionSpec(reduzierteAnimationen) },
        label = "spielPhasenUebergang",
        modifier = modifier,
    ) { ziel ->
        when (ziel) {
            BildschirmSchluessel.UiVorschau -> UiBaukastenDemo(
                content = controller.content,
                schriftgroesse = uiState.schriftgroesse,
                onSchriftgroesseChange = controller::setzeSchriftgroesse,
                onZurueckZumSpiel = controller::uiVorschauSchliessen,
            )

            BildschirmSchluessel.Start -> StartScreen(
                content = controller.content,
                uiState = uiState,
                onModusWaehlen = controller::waehleModus,
                onGrundsatzToggle = controller::toggleOnboardingGrundsatz,
                onSchriftgroesseChange = controller::setzeSchriftgroesse,
                onAnalyseModusToggle = controller::toggleAnalyseModus,
                onReduzierteAnimationenToggle = controller::toggleReduzierteAnimationen,
                onAudioToggle = controller::toggleAudioAktiv,
                onDirektwahlChange = controller::setzeDirektwahlAktiv,
                onDurchgangBeginnen = controller::durchgangBeginnen,
                onUiVorschauOeffnen = controller::uiVorschauOeffnen,
            )

            BildschirmSchluessel.HerkunftWahl -> HerkunftWahlScreen(
                engine = controller.engine,
                uiState = uiState,
                onHerkunftWaehlen = controller::waehleHerkunftEntwurf,
                onGeschlechtWaehlen = controller::waehleGeschlechtEntwurf,
                onAlterWaehlen = controller::waehleAlterEntwurf,
                onDirektPfadWaehlen = controller::waehleDirektPfadEntwurf,
                onBestaetigen = controller::bestaetigePerson,
                onSchriftgroesseChange = controller::setzeSchriftgroesse,
                onAnalyseModusToggle = controller::toggleAnalyseModus,
                onAudioToggle = controller::toggleAudioAktiv,
            )

            BildschirmSchluessel.MusterungErgebnis -> {
                val phase = uiState.gameState.phase as? GamePhase.MusterungErgebnis ?: return@AnimatedContent
                MusterungErgebnisScreen(
                    engine = controller.engine,
                    uiState = uiState,
                    phase = phase,
                    onBestaetigen = controller::bestaetigeMusterung,
                    onSchriftgroesseChange = controller::setzeSchriftgroesse,
                    onAnalyseModusToggle = controller::toggleAnalyseModus,
                    onAudioToggle = controller::toggleAudioAktiv,
                    onWertErklaerungChange = controller::waehleWertErklaerung,
                )
            }

            BildschirmSchluessel.ErwerbWahl -> {
                val phase = uiState.gameState.phase as? GamePhase.ErwerbWahl ?: return@AnimatedContent
                ErwerbWahlScreen(
                    engine = controller.engine,
                    uiState = uiState,
                    phase = phase,
                    onErwerbMarkieren = controller::markiereErwerb,
                    onBestaetigen = controller::bestaetigeAusgewaehltenErwerb,
                    onSchriftgroesseChange = controller::setzeSchriftgroesse,
                    onAnalyseModusToggle = controller::toggleAnalyseModus,
                    onAudioToggle = controller::toggleAudioAktiv,
                    onWertErklaerungChange = controller::waehleWertErklaerung,
                )
            }

            is BildschirmSchluessel.KapitelStart -> {
                val phase = uiState.gameState.phase as? GamePhase.KapitelStart ?: return@AnimatedContent
                KapitelStartScreen(
                    engine = controller.engine,
                    uiState = uiState,
                    phase = phase,
                    onStarteKapitel = controller::starteKapitel,
                    onSchriftgroesseChange = controller::setzeSchriftgroesse,
                    onAnalyseModusToggle = controller::toggleAnalyseModus,
                    onAudioToggle = controller::toggleAudioAktiv,
                    onWertErklaerungChange = controller::waehleWertErklaerung,
                )
            }

            BildschirmSchluessel.Ereignis -> EreignisScreen(
                engine = controller.engine,
                uiState = uiState,
                onOptionWaehlen = controller::waehleOption,
                onWeiterNachAusgang = controller::weiterNachAusgang,
                onSchriftgroesseChange = controller::setzeSchriftgroesse,
                onAnalyseModusToggle = controller::toggleAnalyseModus,
                onAudioToggle = controller::toggleAudioAktiv,
                onWertErklaerungChange = controller::waehleWertErklaerung,
            )

            is BildschirmSchluessel.KapitelAbschluss -> {
                val phase = uiState.gameState.phase as? GamePhase.KapitelAbschluss ?: return@AnimatedContent
                KapitelAbschlussScreen(
                    engine = controller.engine,
                    uiState = uiState,
                    phase = phase,
                    onNaechstesKapitel = controller::naechstesKapitelStarten,
                    onSchriftgroesseChange = controller::setzeSchriftgroesse,
                    onAnalyseModusToggle = controller::toggleAnalyseModus,
                    onAudioToggle = controller::toggleAudioAktiv,
                    onWertErklaerungChange = controller::waehleWertErklaerung,
                )
            }

            BildschirmSchluessel.Auffangnetz,
            BildschirmSchluessel.Lebenslauf,
            -> {
                val phase = uiState.gameState.phase as? GamePhase.Abgeschlossen ?: return@AnimatedContent
                AbschlussScreen(
                    engine = controller.engine,
                    uiState = uiState,
                    phase = phase,
                    onAuffangnetzBestaetigen = controller::auffangnetzBestaetigen,
                    onNeuerDurchgang = controller::neuerDurchgang,
                    onSchriftgroesseChange = controller::setzeSchriftgroesse,
                    onAnalyseModusToggle = controller::toggleAnalyseModus,
                    onAudioToggle = controller::toggleAudioAktiv,
                )
            }
        }
    }
}
