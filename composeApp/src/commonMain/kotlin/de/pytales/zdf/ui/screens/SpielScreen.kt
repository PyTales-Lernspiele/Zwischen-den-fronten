package de.pytales.zdf.ui.screens

import androidx.compose.animation.AnimatedContent
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import de.pytales.zdf.audio.AudioKoordinator
import de.pytales.zdf.audio.SoundEffekt
import de.pytales.zdf.audio.erstellePlattformAudioAusgabe
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.ui.components.PlattformZurueckHandler
import de.pytales.zdf.ui.state.SpielController
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.ArchivUebergaenge
import de.pytales.zdf.ui.theme.LocalSoundEffektSpielen

/**
 * Übergangsschlüssel für ruhige, abschaltbare Phasenwechsel in [SpielScreen].
 * `EreignisAnzeige` und `EreignisAusgang` teilen denselben Schlüssel, damit der Wechsel
 * in die Ausgangs-Ansicht ruhig innerhalb der rechten Buchseite von [EreignisScreen] geschieht.
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
 * (inkl. ruhiger, abschaltbarer Phasenwechsel, getragener Kammermusik + dezenter Soundeffekte
 * mit harter Musiksperre an Front, Etappe & im Auffangnetz, Hintergrund-Pausierung,
 * Android-Zurück-Leitplanke und automatischem Einklappen der Kopfleiste auf flachen Displays).
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
    val metrik = ArchivTheme.metrik

    // Auf flachen Querformat-Displays (Smartphones) Kopfleiste standardmäßig eingeklappt starten
    LaunchedEffect(metrik.kompakteHoehe) {
        controller.uebernehmeStandardKopfleisteFuerDisplay(metrik.kompakteHoehe)
    }

    // Android-Zurück-Taste / Zurück-Geste: schließt Dialoge & Erklärkarten sauber und
    // wahrt während eines Durchgangs die „Kein Zurück“-Leitplanke über die Sicherheitsabfrage.
    PlattformZurueckHandler(aktiv = uiState.sollZurueckAbfangen) {
        controller.verarbeiteZurueckTaste()
    }

    // Plattformübergreifende Audio- & SFX-Steuerung mit harter Musiksperre an Front, Etappe
    // & im Auffangnetz sowie sofortiger Pausierung im Hintergrund (`onPause`/`onStop`).
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

    val spieleEffekt = remember(audioKoordinator) {
        { effekt: SoundEffekt ->
            audioKoordinator.spieleEffekt(effekt)
            Unit
        }
    }

    val onMasterAudioToggle = remember(controller, audioKoordinator) {
        {
            val warAllesAus = !controller.aktuellerZustand.audioAktiv && !controller.aktuellerZustand.effekteAktiv
            controller.toggleAudioAktiv()
            val neuerZustand = controller.aktuellerZustand.audioZustand
            audioKoordinator.synchronisiereZustand(neuerZustand)
            if (warAllesAus) {
                audioKoordinator.spieleEffekt(SoundEffekt.KLICK_SANFT)
            }
        }
    }

    val onEffekteSchalterToggle = remember(controller, audioKoordinator) {
        {
            val wirdAktiv = !controller.aktuellerZustand.effekteAktiv
            controller.toggleEffekteAktiv()
            val neuerZustand = controller.aktuellerZustand.audioZustand
            audioKoordinator.synchronisiereZustand(neuerZustand)
            if (wirdAktiv) {
                audioKoordinator.spieleEffekt(SoundEffekt.KLICK_SANFT)
            }
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

    // Respektvoller, leiser Einzelton beim regulären Erreichen des Lebenslaufs (im Auffangnetz
    // sowie unter Musiksperre durch AudioRegelwerk strikt stumm).
    LaunchedEffect(schluessel) {
        if (schluessel == BildschirmSchluessel.Lebenslauf) {
            audioKoordinator.spieleEffekt(SoundEffekt.EINSCHNITT)
        }
    }

    CompositionLocalProvider(
        LocalSoundEffektSpielen provides spieleEffekt,
    ) {
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
                    onAudioToggle = onMasterAudioToggle,
                    onEinstellungenOeffnen = controller::einstellungenOeffnen,
                    onGrundsaetzeOeffnen = controller::grundsaetzeOeffnen,
                    onDurchgangBeginnen = controller::durchgangBeginnen,
                )

                BildschirmSchluessel.HerkunftWahl -> HerkunftWahlScreen(
                    engine = controller.engine,
                    uiState = uiState,
                    onHerkunftWaehlen = controller::waehleHerkunftEntwurf,
                    onSchrittWechseln = controller::geheZuHerkunftSchritt,
                    onGeschlechtWaehlen = controller::waehleGeschlechtEntwurf,
                    onAlterWaehlen = controller::waehleAlterEntwurf,
                    onDirektPfadWaehlen = controller::waehleDirektPfadEntwurf,
                    onBestaetigen = controller::bestaetigePerson,
                    onAudioToggle = onMasterAudioToggle,
                    onEinstellungenOeffnen = controller::einstellungenOeffnen,
                )

                BildschirmSchluessel.MusterungErgebnis -> {
                    val phase = uiState.gameState.phase as? GamePhase.MusterungErgebnis ?: return@AnimatedContent
                    MusterungErgebnisScreen(
                        engine = controller.engine,
                        uiState = uiState,
                        phase = phase,
                        onBestaetigen = controller::bestaetigeMusterung,
                        onAudioToggle = onMasterAudioToggle,
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
                        onAudioToggle = onMasterAudioToggle,
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
                        onAudioToggle = onMasterAudioToggle,
                        onEinstellungenOeffnen = controller::einstellungenOeffnen,
                        onKopfleisteToggle = controller::toggleKopfleisteEingeklappt,
                        onWertErklaerungChange = controller::waehleWertErklaerung,
                        onEmotionDetailsOffenChange = controller::setzeEmotionDetailsOffen,
                    )
                }

                BildschirmSchluessel.Ereignis -> EreignisScreen(
                    engine = controller.engine,
                    uiState = uiState,
                    onOptionWaehlen = { index ->
                        spieleEffekt(SoundEffekt.ENTSCHEIDUNG)
                        controller.waehleOption(index)
                    },
                    onWeiterNachAusgang = {
                        spieleEffekt(SoundEffekt.ENTSCHEIDUNG)
                        controller.weiterNachAusgang()
                    },
                    onAudioToggle = onMasterAudioToggle,
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
                        onAudioToggle = onMasterAudioToggle,
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
                        onAudioToggle = onMasterAudioToggle,
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
                onGrundmusikToggle = controller::toggleGrundmusik,
                onEffekteToggle = onEffekteSchalterToggle,
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
}
