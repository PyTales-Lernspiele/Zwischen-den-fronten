package de.pytales.zdf.ui.screens

import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.ui.UiBaukastenDemo
import de.pytales.zdf.ui.state.SpielController

/**
 * Durchgängiger Spielbildschirm-Router für alle Phasen von 1914 bis 1919
 * (plus optionalen Zugang zur AP-3-Komponenten-Vorschau aus dem Startmenü).
 */
@Composable
fun SpielScreen(
    controller: SpielController,
    modifier: Modifier = Modifier,
) {
    val uiState by controller.uiState.collectAsState()

    if (uiState.zeigeUiVorschau) {
        UiBaukastenDemo(
            content = controller.content,
            schriftgroesse = uiState.schriftgroesse,
            onSchriftgroesseChange = controller::setzeSchriftgroesse,
            onZurueckZumSpiel = controller::uiVorschauSchliessen,
            modifier = modifier,
        )
        return
    }

    when (val phase = uiState.gameState.phase) {
        is GamePhase.Start -> StartScreen(
            content = controller.content,
            uiState = uiState,
            onModusWaehlen = controller::waehleModus,
            onGrundsatzToggle = controller::toggleOnboardingGrundsatz,
            onSchriftgroesseChange = controller::setzeSchriftgroesse,
            onAnalyseModusToggle = controller::toggleAnalyseModus,
            onDirektwahlChange = controller::setzeDirektwahlAktiv,
            onDurchgangBeginnen = controller::durchgangBeginnen,
            onUiVorschauOeffnen = controller::uiVorschauOeffnen,
            modifier = modifier,
        )

        is GamePhase.HerkunftWahl -> HerkunftWahlScreen(
            engine = controller.engine,
            uiState = uiState,
            onHerkunftWaehlen = controller::waehleHerkunftEntwurf,
            onGeschlechtWaehlen = controller::waehleGeschlechtEntwurf,
            onAlterWaehlen = controller::waehleAlterEntwurf,
            onDirektPfadWaehlen = controller::waehleDirektPfadEntwurf,
            onBestaetigen = controller::bestaetigePerson,
            onSchriftgroesseChange = controller::setzeSchriftgroesse,
            onAnalyseModusToggle = controller::toggleAnalyseModus,
            modifier = modifier,
        )

        is GamePhase.MusterungErgebnis -> MusterungErgebnisScreen(
            engine = controller.engine,
            uiState = uiState,
            phase = phase,
            onBestaetigen = controller::bestaetigeMusterung,
            onSchriftgroesseChange = controller::setzeSchriftgroesse,
            onAnalyseModusToggle = controller::toggleAnalyseModus,
            onWertErklaerungChange = controller::waehleWertErklaerung,
            modifier = modifier,
        )

        is GamePhase.ErwerbWahl -> ErwerbWahlScreen(
            engine = controller.engine,
            uiState = uiState,
            phase = phase,
            onErwerbMarkieren = controller::markiereErwerb,
            onBestaetigen = controller::bestaetigeAusgewaehltenErwerb,
            onSchriftgroesseChange = controller::setzeSchriftgroesse,
            onAnalyseModusToggle = controller::toggleAnalyseModus,
            onWertErklaerungChange = controller::waehleWertErklaerung,
            modifier = modifier,
        )

        is GamePhase.KapitelStart -> KapitelStartScreen(
            engine = controller.engine,
            uiState = uiState,
            phase = phase,
            onStarteKapitel = controller::starteKapitel,
            onSchriftgroesseChange = controller::setzeSchriftgroesse,
            onAnalyseModusToggle = controller::toggleAnalyseModus,
            onWertErklaerungChange = controller::waehleWertErklaerung,
            modifier = modifier,
        )

        is GamePhase.EreignisAnzeige,
        is GamePhase.EreignisAusgang,
        -> EreignisScreen(
            engine = controller.engine,
            uiState = uiState,
            onOptionWaehlen = controller::waehleOption,
            onWeiterNachAusgang = controller::weiterNachAusgang,
            onSchriftgroesseChange = controller::setzeSchriftgroesse,
            onAnalyseModusToggle = controller::toggleAnalyseModus,
            onWertErklaerungChange = controller::waehleWertErklaerung,
            modifier = modifier,
        )

        is GamePhase.KapitelAbschluss -> KapitelAbschlussScreen(
            engine = controller.engine,
            uiState = uiState,
            phase = phase,
            onNaechstesKapitel = controller::naechstesKapitelStarten,
            onSchriftgroesseChange = controller::setzeSchriftgroesse,
            onAnalyseModusToggle = controller::toggleAnalyseModus,
            onWertErklaerungChange = controller::waehleWertErklaerung,
            modifier = modifier,
        )

        is GamePhase.Abgeschlossen -> AbschlussScreen(
            engine = controller.engine,
            uiState = uiState,
            phase = phase,
            onAuffangnetzBestaetigen = controller::auffangnetzBestaetigen,
            onNeuerDurchgang = controller::neuerDurchgang,
            onSchriftgroesseChange = controller::setzeSchriftgroesse,
            onAnalyseModusToggle = controller::toggleAnalyseModus,
            modifier = modifier,
        )
    }
}
