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
import de.pytales.zdf.ui.components.PlattformZurueckHandler
import de.pytales.zdf.ui.state.SpielController
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.ArchivUebergaenge

/**
 * Übergangsschlüssel für ruhige, abschaltbare Phasenwechsel in [SpielScreen].
 * `EreignisAnzeige` und `EreignisAusgang` teilen denselben Schlüssel, damit das Aufklappen
 * des Ausgangs ruhig innerhalb von [EreignisScreen] geschieht, ohne die Kopfleiste flackern zu lassen.
 */
private sealed interface BildschirmSchluessel {
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
 * Musiksperre an Front & Etappe, Hintergrund-Pausierung, Android-Zurück-Leitplanke
 * sowie aufgeräumtem Einstellungs- und Grundsätze-Dialog).
 */
@Composable
fun SpielScreen(
    controller: SpielController,
    modifier: Modifier = Modifier,
    appImVordergrund: Boolean = true,
    onAppBeenden: (() -> Unit)? = null,
) {
    val uiState by controller.uiState.collectAsState()
    val reduzierteAnimationen = ArchivTheme.reduzierteAnimationen

    // Android-Zurück-Taste / Zurück-Geste: schließt Dialoge & Erklärkarten sauber und
    // wahrt während eines Durchgangs die „Kein Zurück“-Leitplanke über die Sicherheitsabfrage.
    PlattformZurueckHandler(aktiv = uiState.sollZurueckAbfangen) {
        controller.verarbeiteZurueckTaste()
    }

    // Plattformübergreifende Audio-Steuerung mit harter Musiksperre an Front & Etappe
    // sowie sauberer Pausierung beim Wechsel der App in den Hintergrund (`onPause`/`onStop`).
    val audioKoordinator = remember {
        AudioKoordinator(erstellePlattformAudioAusgabe())
    }
    val audioZustand = uiState.audioZustand
    LaunchedEffect(audioZustand, appImVordergrund) {
        audioKoordinator.setzeHintergrundPausiert(!appImVordergrund)
        if (!appImVordergrund) {
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

    val schluessel: BildschirmSchluessel = when (val phase = uiState.gameState.phase) {
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

    AnimatedContent(
        targetState = schluessel,
        transitionSpec = { ArchivUebergaenge.phasenTransitionSpec(reduzierteAnimationen) },
        label = "spielPhasenUebergang",
        modifier = modifier,
    ) { ziel ->
        when (ziel) {
            BildschirmSchluessel.Start -> StartScreen(
                content = controller.content,
                uiState = uiState,
                onModusWaehlen = controller::waehleModus,
                onAudioToggle = controller::toggleAudioAktiv,
                onEinstellungenOeffnen = controller::einstellungenOeffnen,
                onGrundsaetzeOeffnen = controller::grundsaetzeOeffnen,
                onDurchgangBeginnen = controller::durchgangBeginnen,
            )

            BildschirmSchluessel.HerkunftWahl -> HerkunftWahlScreen(
                engine = controller.engine,
                uiState = uiState,
                onHerkunftWaehlen = controller::waehleHerkunftEntwurf,
                onGeschlechtWaehlen = controller::waehleGeschlechtEntwurf,
                onAlterWaehlen = controller::waehleAlterEntwurf,
                onDirektPfadWaehlen = controller::waehleDirektPfadEntwurf,
                onBestaetigen = controller::bestaetigePerson,
                onAudioToggle = controller::toggleAudioAktiv,
                onEinstellungenOeffnen = controller::einstellungenOeffnen,
            )

            BildschirmSchluessel.MusterungErgebnis -> {
                val phase = uiState.gameState.phase as? GamePhase.MusterungErgebnis ?: return@AnimatedContent
                MusterungErgebnisScreen(
                    engine = controller.engine,
                    uiState = uiState,
                    phase = phase,
                    onBestaetigen = controller::bestaetigeMusterung,
                    onAudioToggle = controller::toggleAudioAktiv,
                    onEinstellungenOeffnen = controller::einstellungenOeffnen,
                    onKopfleisteToggle = controller::toggleKopfleisteEingeklappt,
                    onWertErklaerungChange = controller::waehleWertErklaerung,
                    onEmotionDetailsOffenChange = controller::setzeEmotionDetailsOffen,
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
                    onAudioToggle = controller::toggleAudioAktiv,
                    onEinstellungenOeffnen = controller::einstellungenOeffnen,
                    onKopfleisteToggle = controller::toggleKopfleisteEingeklappt,
                    onWertErklaerungChange = controller::waehleWertErklaerung,
                    onEmotionDetailsOffenChange = controller::setzeEmotionDetailsOffen,
                )
            }

            is BildschirmSchluessel.KapitelStart -> {
                val phase = uiState.gameState.phase as? GamePhase.KapitelStart ?: return@AnimatedContent
                KapitelStartScreen(
                    engine = controller.engine,
                    uiState = uiState,
                    phase = phase,
                    onStarteKapitel = controller::starteKapitel,
                    onAudioToggle = controller::toggleAudioAktiv,
                    onEinstellungenOeffnen = controller::einstellungenOeffnen,
                    onKopfleisteToggle = controller::toggleKopfleisteEingeklappt,
                    onWertErklaerungChange = controller::waehleWertErklaerung,
                    onEmotionDetailsOffenChange = controller::setzeEmotionDetailsOffen,
                )
            }

            BildschirmSchluessel.Ereignis -> EreignisScreen(
                engine = controller.engine,
                uiState = uiState,
                onOptionWaehlen = controller::waehleOption,
                onWeiterNachAusgang = controller::weiterNachAusgang,
                onAudioToggle = controller::toggleAudioAktiv,
                onEinstellungenOeffnen = controller::einstellungenOeffnen,
                onKopfleisteToggle = controller::toggleKopfleisteEingeklappt,
                onWertErklaerungChange = controller::waehleWertErklaerung,
                onEmotionDetailsOffenChange = controller::setzeEmotionDetailsOffen,
            )

            is BildschirmSchluessel.KapitelAbschluss -> {
                val phase = uiState.gameState.phase as? GamePhase.KapitelAbschluss ?: return@AnimatedContent
                KapitelAbschlussScreen(
                    engine = controller.engine,
                    uiState = uiState,
                    phase = phase,
                    onNaechstesKapitel = controller::naechstesKapitelStarten,
                    onAudioToggle = controller::toggleAudioAktiv,
                    onEinstellungenOeffnen = controller::einstellungenOeffnen,
                    onKopfleisteToggle = controller::toggleKopfleisteEingeklappt,
                    onWertErklaerungChange = controller::waehleWertErklaerung,
                    onEmotionDetailsOffenChange = controller::setzeEmotionDetailsOffen,
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
                    onAudioToggle = controller::toggleAudioAktiv,
                    onEinstellungenOeffnen = controller::einstellungenOeffnen,
                )
            }
        }
    }

    // Ruhiger Einstellungs-Dialog (jederzeit über das Zahnrad-Symbol erreichbar)
    if (uiState.einstellungenOffen) {
        EinstellungenDialog(
            content = controller.content,
            uiState = uiState,
            onSchriftgroesseChange = controller::setzeSchriftgroesse,
            onReduzierteAnimationenToggle = controller::toggleReduzierteAnimationen,
            onAudioToggle = controller::toggleAudioAktiv,
            onDirektwahlChange = controller::setzeDirektwahlAktiv,
            onSchliessen = controller::einstellungenSchliessen,
        )
    }

    // Grundsätze-Dialog im Startmenü
    if (uiState.grundsaetzeOffen) {
        GrundsaetzeDialog(
            grundsaetze = controller.content.konfiguration.onboarding.grundsaetze,
            aufgeklappteIds = uiState.aufgeklappteGrundsaetze,
            onGrundsatzToggle = controller::toggleOnboardingGrundsatz,
            onSchliessen = controller::grundsaetzeSchliessen,
        )
    }

    // Ruhige Sicherheitsabfrage beim Verlassen eines laufenden oder abgeschlossenen Durchgangs
    if (uiState.verlassenDialogOffen) {
        VerlassenSicherheitsDialog(
            istAbgeschlossen = uiState.gameState.phase is GamePhase.Abgeschlossen,
            onBleiben = controller::verlassenDialogSchliessen,
            onZumStartmenue = controller::durchgangNachBestaetigungVerlassen,
            onAppBeenden = onAppBeenden?.let { beenden ->
                {
                    controller.verlassenDialogSchliessen()
                    beenden()
                }
            },
        )
    }
}
