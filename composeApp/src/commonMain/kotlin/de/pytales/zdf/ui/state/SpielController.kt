package de.pytales.zdf.ui.state

import androidx.compose.runtime.Immutable
import de.pytales.zdf.audio.AudioRegelwerk
import de.pytales.zdf.audio.AudioZustand
import de.pytales.zdf.content.GameContent
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.engine.GameState
import de.pytales.zdf.engine.KotlinRandomSource
import de.pytales.zdf.engine.RandomSource
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.SpielModus
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.theme.Schriftgroesse
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

/**
 * Zwischenstand der Auswahl auf dem Bildschirm `HerkunftWahl`, bevor die Figur
 * verbindlich erzeugt wird (gestraffter 2–3-Klick-Einstieg).
 */
@Immutable
data class HerkunftEntwurf(
    val herkunftId: String? = null,
    val geschlecht: Geschlecht? = null,
    val alter: Int? = null,
    val direktwahlPfad: Pfad? = null,
) {
    fun istVollstaendig(direktwahlAktiv: Boolean): Boolean =
        herkunftId != null &&
            geschlecht != null &&
            alter != null &&
            (!direktwahlAktiv || direktwahlPfad != null)
}

/**
 * Ergebnis einer System-Zurück-Aktion (z. B. Android-Zurück-Taste / Zurück-Geste).
 *
 * Setzt die pädagogische Leitplanke „Kein Zurück“ auch auf Android konsequent durch:
 * Es wird niemals zu einer vorherigen Karte oder Entscheidung zurückgesprungen.
 */
enum class ZurueckErgebnis {
    /** Offene Verlassen-Sicherheitsabfrage wurde ruhig geschlossen. */
    DIALOG_GESCHLOSSEN,

    /** Die AP-3-Komponenten-Vorschau wurde geschlossen (zurück ins Startmenü). */
    UI_VORSCHAU_GESCHLOSSEN,

    /** Eine geöffnete Befindens- oder Figuren-Erklärkarte wurde geschlossen. */
    ERKLAERKARTE_GESCHLOSSEN,

    /** Eine ruhige Sicherheitsabfrage zum Verlassen des Durchgangs wurde geöffnet. */
    SICHERHEITSABFRAGE_GEOEFFNET,

    /** Im Startmenü ohne offene Überlagerung greift das normale System-Zurück (App verlassen). */
    SYSTEM_STANDARD,
}

/**
 * Unveränderlicher Gesamt-UI-Zustand rund um [GameState] und globale UI-Einstellungen.
 */
@Immutable
data class SpielUiState(
    val gameState: GameState,
    val schriftgroesse: Schriftgroesse = Schriftgroesse.MITTEL,
    val analyseModus: Boolean = false,
    val reduzierteAnimationen: Boolean = false,
    val audioAktiv: Boolean = false,
    val audioLautstaerke: Float = AudioRegelwerk.STANDARD_LAUTSTAERKE,
    val zeigeUiVorschau: Boolean = false,
    val aufgeklappteGrundsaetze: Set<String> = emptySet(),
    val ausgewaehlterWert: WertSchluessel? = null,
    val emotionDetailsOffen: Boolean = false,
    val verlassenDialogOffen: Boolean = false,
    val herkunftEntwurf: HerkunftEntwurf = HerkunftEntwurf(),
    val ausgewaehlterErwerbId: String? = null,
    val auffangnetzBestaetigt: Boolean = false,
) {
    val istImAuffangnetz: Boolean
        get() {
            val phase = gameState.phase
            return phase is GamePhase.Abgeschlossen &&
                phase.hartesEnde != null &&
                !auffangnetzBestaetigt
        }

    /** `true`, wenn in der Kopfleiste eine Befindens- oder Figuren-Erklärkarte geöffnet ist. */
    val hatOffeneErklaerKarte: Boolean
        get() = ausgewaehlterWert != null || emotionDetailsOffen

    /** `true` ab Einstieg (`HerkunftWahl`) bis vor dem Abschluss (`Abgeschlossen`). */
    val istImLaufendenDurchgang: Boolean
        get() = gameState.phase !is GamePhase.Start && gameState.phase !is GamePhase.Abgeschlossen

    /**
     * Gibt an, ob die System-Zurück-Taste abgefangen werden muss.
     * Im Startmenü ohne offene Vorschau/Dialog bleibt sie frei für normales App-Verlassen.
     */
    val sollZurueckAbfangen: Boolean
        get() = verlassenDialogOffen ||
            zeigeUiVorschau ||
            hatOffeneErklaerKarte ||
            gameState.phase !is GamePhase.Start

    /**
     * Effektiver Audio-Zustand inkl. harter Musiksperre auf `front`, `etappe` und im Auffangnetz.
     */
    val audioZustand: AudioZustand
        get() = AudioRegelwerk.bestimmeZustand(
            gameState = gameState,
            audioAktiv = audioAktiv,
            lautstaerke = audioLautstaerke,
        )
}

/**
 * Testbarer, plattformunabhängiger Spiel-Controller rund um [GameEngine] und [GameState].
 *
 * Setzt die pädagogischen Leitplanken strikt durch:
 * - **Kein Zurück:** Alle Spielschritte laufen ausschließlich vorwärts durch die [GamePhase]-Kette.
 * - **Kein Speichern/Laden:** Ein Durchgang wird von Anfang bis Ende in einem Zug gespielt.
 * - **Genau zwei Entscheidungen:** Nur die zwei Optionen (Index 0 oder 1) des aktuellen Ereignisses sind wählbar.
 * - **Robuste Phasen-Prüfung:** Doppelklicks oder phasenfremde Aufrufe werden sicher ignoriert (`false`),
 *   statt den Durchgang abzubrechen.
 */
class SpielController(
    val engine: GameEngine,
    initialSchriftgroesse: Schriftgroesse = Schriftgroesse.MITTEL,
    initialAnalyseModus: Boolean = false,
    initialReduzierteAnimationen: Boolean = false,
    initialAudioAktiv: Boolean = false,
    initialAudioLautstaerke: Float = AudioRegelwerk.STANDARD_LAUTSTAERKE,
) {
    constructor(
        content: GameContent,
        random: RandomSource = KotlinRandomSource(),
        initialSchriftgroesse: Schriftgroesse = Schriftgroesse.MITTEL,
        initialAnalyseModus: Boolean = false,
        initialReduzierteAnimationen: Boolean = false,
        initialAudioAktiv: Boolean = false,
        initialAudioLautstaerke: Float = AudioRegelwerk.STANDARD_LAUTSTAERKE,
    ) : this(
        engine = GameEngine(content, random),
        initialSchriftgroesse = initialSchriftgroesse,
        initialAnalyseModus = initialAnalyseModus,
        initialReduzierteAnimationen = initialReduzierteAnimationen,
        initialAudioAktiv = initialAudioAktiv,
        initialAudioLautstaerke = initialAudioLautstaerke,
    )

    val content: GameContent
        get() = engine.content

    private val _uiState = MutableStateFlow(
        SpielUiState(
            gameState = engine.neuesSpiel(),
            schriftgroesse = initialSchriftgroesse,
            analyseModus = initialAnalyseModus,
            reduzierteAnimationen = initialReduzierteAnimationen,
            audioAktiv = initialAudioAktiv,
            audioLautstaerke = AudioRegelwerk.begrenzeLautstaerke(initialAudioLautstaerke),
        ),
    )

    val uiState: StateFlow<SpielUiState> = _uiState.asStateFlow()

    val aktuellerZustand: SpielUiState
        get() = _uiState.value

    // -------------------------------------------------------------------------
    // Globale UI-Einstellungen (jederzeit im Unterricht umschaltbar)
    // -------------------------------------------------------------------------

    fun setzeSchriftgroesse(schriftgroesse: Schriftgroesse) {
        _uiState.update { it.copy(schriftgroesse = schriftgroesse) }
    }

    fun setzeAnalyseModus(aktiv: Boolean) {
        _uiState.update { it.copy(analyseModus = aktiv) }
    }

    fun toggleAnalyseModus() {
        _uiState.update { it.copy(analyseModus = !it.analyseModus) }
    }

    fun setzeReduzierteAnimationen(aktiv: Boolean) {
        _uiState.update { it.copy(reduzierteAnimationen = aktiv) }
    }

    fun toggleReduzierteAnimationen() {
        _uiState.update { it.copy(reduzierteAnimationen = !it.reduzierteAnimationen) }
    }

    fun setzeAudioAktiv(aktiv: Boolean) {
        _uiState.update { it.copy(audioAktiv = aktiv) }
    }

    fun toggleAudioAktiv() {
        _uiState.update { it.copy(audioAktiv = !it.audioAktiv) }
    }

    fun setzeAudioLautstaerke(lautstaerke: Float) {
        val begrenzt = AudioRegelwerk.begrenzeLautstaerke(lautstaerke)
        _uiState.update { it.copy(audioLautstaerke = begrenzt) }
    }

    fun waehleWertErklaerung(schluessel: WertSchluessel?) {
        _uiState.update {
            it.copy(
                ausgewaehlterWert = schluessel,
                emotionDetailsOffen = if (schluessel != null) false else it.emotionDetailsOffen,
            )
        }
    }

    fun setzeEmotionDetailsOffen(offen: Boolean) {
        _uiState.update {
            it.copy(
                emotionDetailsOffen = offen,
                ausgewaehlterWert = if (offen) null else it.ausgewaehlterWert,
            )
        }
    }

    /**
     * Schließt geöffnete Befindens- oder Figuren-Erklärkarten in der Kopfleiste.
     * Gibt `true` zurück, wenn mindestens eine Karte geöffnet war.
     */
    fun schliesseErklaerKarten(): Boolean {
        val aktuell = _uiState.value
        if (!aktuell.hatOffeneErklaerKarte) return false
        _uiState.value = aktuell.copy(
            ausgewaehlterWert = null,
            emotionDetailsOffen = false,
        )
        return true
    }

    /**
     * Verarbeitet die System-Zurück-Taste (insbesondere Android `BackHandler`) gemäß der
     * „Kein Zurück“-Leitplanke:
     * 1. Offene Sicherheitsabfrage schließen (sichere Standardaktion: im Durchgang bleiben).
     * 2. AP-3-UI-Vorschau schließen.
     * 3. Geöffnete Befindens- oder Figuren-Erklärkarte schließen.
     * 4. Während eines laufenden oder abgeschlossenen Durchgangs niemals rückwärts navigieren,
     *    sondern eine ruhige Sicherheitsabfrage öffnen.
     * 5. Im Startmenü ohne Überlagerungen greift das normale System-Zurück.
     */
    fun verarbeiteZurueckTaste(): ZurueckErgebnis {
        val aktuell = _uiState.value
        return when {
            aktuell.verlassenDialogOffen -> {
                _uiState.value = aktuell.copy(verlassenDialogOffen = false)
                ZurueckErgebnis.DIALOG_GESCHLOSSEN
            }

            aktuell.zeigeUiVorschau -> {
                _uiState.value = aktuell.copy(zeigeUiVorschau = false)
                ZurueckErgebnis.UI_VORSCHAU_GESCHLOSSEN
            }

            aktuell.hatOffeneErklaerKarte -> {
                _uiState.value = aktuell.copy(
                    ausgewaehlterWert = null,
                    emotionDetailsOffen = false,
                )
                ZurueckErgebnis.ERKLAERKARTE_GESCHLOSSEN
            }

            aktuell.gameState.phase is GamePhase.Start -> ZurueckErgebnis.SYSTEM_STANDARD

            else -> {
                _uiState.value = aktuell.copy(verlassenDialogOffen = true)
                ZurueckErgebnis.SICHERHEITSABFRAGE_GEOEFFNET
            }
        }
    }

    fun verlassenDialogSchliessen(): Boolean {
        val aktuell = _uiState.value
        if (!aktuell.verlassenDialogOffen) return false
        _uiState.value = aktuell.copy(verlassenDialogOffen = false)
        return true
    }

    /**
     * Bricht einen Durchgang ausschließlich nach ausdrücklicher Bestätigung in der
     * ruhigen Verlassen-Sicherheitsabfrage ab und kehrt sauber ins Startmenü zurück.
     * Globale Unterrichts- und Zugänglichkeits-Einstellungen bleiben erhalten.
     */
    fun durchgangNachBestaetigungVerlassen(): Boolean {
        val aktuell = _uiState.value
        if (!aktuell.verlassenDialogOffen) return false
        _uiState.value = aktuell.copy(
            gameState = engine.neuesSpiel(
                modus = aktuell.gameState.modus,
                direktwahlAktiv = aktuell.gameState.direktwahlAktiv,
            ),
            zeigeUiVorschau = false,
            ausgewaehlterWert = null,
            emotionDetailsOffen = false,
            verlassenDialogOffen = false,
            herkunftEntwurf = HerkunftEntwurf(),
            ausgewaehlterErwerbId = null,
            auffangnetzBestaetigt = false,
        )
        return true
    }

    /**
     * Öffnet die AP-3-Komponenten-Vorschau ausschließlich aus dem Startmenü
     * (für Lehrkräfte & Entwicklung), niemals während eines laufenden Durchgangs.
     */
    fun uiVorschauOeffnen(): Boolean {
        val aktuell = _uiState.value
        if (aktuell.gameState.phase !is GamePhase.Start) return false
        _uiState.value = aktuell.copy(zeigeUiVorschau = true)
        return true
    }

    fun uiVorschauSchliessen(): Boolean {
        val aktuell = _uiState.value
        if (!aktuell.zeigeUiVorschau) return false
        _uiState.value = aktuell.copy(zeigeUiVorschau = false)
        return true
    }

    // -------------------------------------------------------------------------
    // Startmenü (GamePhase.Start)
    // -------------------------------------------------------------------------

    fun waehleModus(modus: SpielModus): Boolean {
        val aktuell = _uiState.value
        if (aktuell.gameState.phase !is GamePhase.Start) return false
        _uiState.value = aktuell.copy(
            gameState = engine.neuesSpiel(
                modus = modus,
                direktwahlAktiv = aktuell.gameState.direktwahlAktiv,
            ),
        )
        return true
    }

    fun setzeDirektwahlAktiv(aktiv: Boolean): Boolean {
        val aktuell = _uiState.value
        if (aktuell.gameState.phase !is GamePhase.Start) return false
        val erlaubt = content.herkunft.direktwahlOption.aktiv
        val effektiv = aktiv && erlaubt
        _uiState.value = aktuell.copy(
            gameState = engine.neuesSpiel(
                modus = aktuell.gameState.modus,
                direktwahlAktiv = effektiv,
            ),
        )
        return true
    }

    fun toggleOnboardingGrundsatz(grundsatzId: String): Boolean {
        val aktuell = _uiState.value
        if (aktuell.gameState.phase !is GamePhase.Start) return false
        val existiert = content.konfiguration.onboarding.grundsaetze.any { it.id == grundsatzId }
        if (!existiert) return false

        val neu = if (grundsatzId in aktuell.aufgeklappteGrundsaetze) {
            aktuell.aufgeklappteGrundsaetze - grundsatzId
        } else {
            aktuell.aufgeklappteGrundsaetze + grundsatzId
        }
        _uiState.value = aktuell.copy(aufgeklappteGrundsaetze = neu)
        return true
    }

    fun durchgangBeginnen(): Boolean {
        val aktuell = _uiState.value
        if (aktuell.gameState.phase !is GamePhase.Start) return false
        val naechster = engine.herkunftWahlOeffnen(
            state = aktuell.gameState,
            modus = aktuell.gameState.modus,
            direktwahlAktiv = aktuell.gameState.direktwahlAktiv,
        )
        _uiState.value = aktuell.copy(
            gameState = naechster,
            zeigeUiVorschau = false,
            ausgewaehlterWert = null,
            emotionDetailsOffen = false,
            verlassenDialogOffen = false,
            herkunftEntwurf = HerkunftEntwurf(),
            ausgewaehlterErwerbId = null,
            auffangnetzBestaetigt = false,
        )
        return true
    }

    // -------------------------------------------------------------------------
    // Gestraffter Einstieg: Herkunft, Musterung & Erwerbswahl
    // -------------------------------------------------------------------------

    fun waehleHerkunftEntwurf(herkunftId: String): Boolean {
        val aktuell = _uiState.value
        if (aktuell.gameState.phase !is GamePhase.HerkunftWahl) return false
        if (herkunftId !in content.herkunftById) return false
        _uiState.value = aktuell.copy(
            herkunftEntwurf = aktuell.herkunftEntwurf.copy(herkunftId = herkunftId),
        )
        return true
    }

    fun waehleGeschlechtEntwurf(geschlecht: Geschlecht): Boolean {
        val aktuell = _uiState.value
        if (aktuell.gameState.phase !is GamePhase.HerkunftWahl) return false
        _uiState.value = aktuell.copy(
            herkunftEntwurf = aktuell.herkunftEntwurf.copy(geschlecht = geschlecht),
        )
        return true
    }

    fun waehleAlterEntwurf(alter: Int): Boolean {
        val aktuell = _uiState.value
        if (aktuell.gameState.phase !is GamePhase.HerkunftWahl) return false
        if (content.herkunft.jahrgaenge.none { it.alter == alter }) return false
        _uiState.value = aktuell.copy(
            herkunftEntwurf = aktuell.herkunftEntwurf.copy(alter = alter),
        )
        return true
    }

    fun waehleDirektPfadEntwurf(pfad: Pfad): Boolean {
        val aktuell = _uiState.value
        if (aktuell.gameState.phase !is GamePhase.HerkunftWahl) return false
        if (!aktuell.gameState.direktwahlAktiv) return false
        _uiState.value = aktuell.copy(
            herkunftEntwurf = aktuell.herkunftEntwurf.copy(direktwahlPfad = pfad),
        )
        return true
    }

    fun bestaetigePerson(): Boolean {
        val aktuell = _uiState.value
        if (aktuell.gameState.phase !is GamePhase.HerkunftWahl) return false
        val entwurf = aktuell.herkunftEntwurf
        if (!entwurf.istVollstaendig(aktuell.gameState.direktwahlAktiv)) return false

        return waehlePerson(
            herkunftId = requireNotNull(entwurf.herkunftId),
            geschlecht = requireNotNull(entwurf.geschlecht),
            alter = requireNotNull(entwurf.alter),
            direktwahlPfad = if (aktuell.gameState.direktwahlAktiv) entwurf.direktwahlPfad else null,
        )
    }

    fun waehlePerson(
        herkunftId: String,
        geschlecht: Geschlecht,
        alter: Int,
        direktwahlPfad: Pfad? = null,
    ): Boolean {
        val aktuell = _uiState.value
        if (aktuell.gameState.phase !is GamePhase.HerkunftWahl) return false
        if (herkunftId !in content.herkunftById) return false
        if (direktwahlPfad != null && !content.herkunft.direktwahlOption.aktiv) return false

        val effektiverDirektPfad = if (aktuell.gameState.direktwahlAktiv) {
            direktwahlPfad ?: return false
        } else {
            direktwahlPfad
        }

        val naechster = engine.waehlePerson(
            state = aktuell.gameState,
            herkunftId = herkunftId,
            geschlecht = geschlecht,
            alter = alter,
            direktwahlPfad = effektiverDirektPfad,
        )
        _uiState.value = aktuell.copy(
            gameState = naechster,
            ausgewaehlterWert = null,
            emotionDetailsOffen = false,
            verlassenDialogOffen = false,
            ausgewaehlterErwerbId = null,
        )
        return true
    }

    fun bestaetigeMusterung(): Boolean {
        val aktuell = _uiState.value
        if (aktuell.gameState.phase !is GamePhase.MusterungErgebnis) return false
        val naechster = engine.bestaetigeMusterung(aktuell.gameState)
        _uiState.value = aktuell.copy(
            gameState = naechster,
            ausgewaehlterWert = null,
            emotionDetailsOffen = false,
            verlassenDialogOffen = false,
            ausgewaehlterErwerbId = null,
        )
        return true
    }

    fun markiereErwerb(erwerbId: String): Boolean {
        val aktuell = _uiState.value
        val phase = aktuell.gameState.phase as? GamePhase.ErwerbWahl ?: return false
        if (phase.optionen.none { it.id == erwerbId }) return false
        _uiState.value = aktuell.copy(ausgewaehlterErwerbId = erwerbId)
        return true
    }

    fun bestaetigeAusgewaehltenErwerb(): Boolean {
        val erwerbId = _uiState.value.ausgewaehlterErwerbId ?: return false
        return waehleErwerb(erwerbId)
    }

    fun waehleErwerb(erwerbId: String): Boolean {
        val aktuell = _uiState.value
        val phase = aktuell.gameState.phase as? GamePhase.ErwerbWahl ?: return false
        if (phase.optionen.none { it.id == erwerbId }) return false
        val naechster = engine.waehleErwerb(aktuell.gameState, erwerbId)
        _uiState.value = aktuell.copy(
            gameState = naechster,
            ausgewaehlterWert = null,
            emotionDetailsOffen = false,
            verlassenDialogOffen = false,
            ausgewaehlterErwerbId = null,
        )
        return true
    }

    // -------------------------------------------------------------------------
    // Kapitel- & Ereignisschleife (1914–1919)
    // -------------------------------------------------------------------------

    fun starteKapitel(): Boolean {
        val aktuell = _uiState.value
        if (aktuell.gameState.phase !is GamePhase.KapitelStart) return false
        val naechster = engine.starteKapitel(aktuell.gameState)
        _uiState.value = aktuell.copy(
            gameState = naechster,
            ausgewaehlterWert = null,
            emotionDetailsOffen = false,
            verlassenDialogOffen = false,
            auffangnetzBestaetigt = false,
        )
        return true
    }

    fun waehleOption(optionIndex: Int): Boolean {
        val aktuell = _uiState.value
        val phase = aktuell.gameState.phase as? GamePhase.EreignisAnzeige ?: return false
        if (optionIndex !in phase.ereignis.optionen.indices) return false
        val naechster = engine.waehleOption(aktuell.gameState, optionIndex)
        _uiState.value = aktuell.copy(
            gameState = naechster,
            ausgewaehlterWert = null,
            emotionDetailsOffen = false,
            verlassenDialogOffen = false,
            auffangnetzBestaetigt = false,
        )
        return true
    }

    fun weiterNachAusgang(): Boolean {
        val aktuell = _uiState.value
        if (aktuell.gameState.phase !is GamePhase.EreignisAusgang) return false
        val naechster = engine.weiterNachAusgang(aktuell.gameState)
        _uiState.value = aktuell.copy(
            gameState = naechster,
            ausgewaehlterWert = null,
            emotionDetailsOffen = false,
            verlassenDialogOffen = false,
            auffangnetzBestaetigt = false,
        )
        return true
    }

    fun naechstesKapitelStarten(): Boolean {
        val aktuell = _uiState.value
        if (aktuell.gameState.phase !is GamePhase.KapitelAbschluss) return false
        val naechster = engine.naechstesKapitelStarten(aktuell.gameState)
        _uiState.value = aktuell.copy(
            gameState = naechster,
            ausgewaehlterWert = null,
            emotionDetailsOffen = false,
            verlassenDialogOffen = false,
        )
        return true
    }

    // -------------------------------------------------------------------------
    // Abschluss: Auffangnetz & Neuer Durchgang
    // -------------------------------------------------------------------------

    fun auffangnetzBestaetigen(): Boolean {
        val aktuell = _uiState.value
        val phase = aktuell.gameState.phase as? GamePhase.Abgeschlossen ?: return false
        if (phase.hartesEnde == null || aktuell.auffangnetzBestaetigt) return false
        _uiState.value = aktuell.copy(
            auffangnetzBestaetigt = true,
            verlassenDialogOffen = false,
        )
        return true
    }

    /**
     * Startet nach abgeschlossenem Durchgang (regulär 1919 oder nach Auffangnetz) einen
     * frischen Durchgang im Startmenü. Globale Unterrichts- und Zugänglichkeits-Einstellungen
     * (`schriftgroesse`, `analyseModus`, `reduzierteAnimationen`, `audioAktiv`, `audioLautstaerke`,
     * gewählter `modus` und `direktwahlAktiv`) bleiben erhalten.
     */
    fun neuerDurchgang(): Boolean {
        val aktuell = _uiState.value
        if (aktuell.gameState.phase !is GamePhase.Abgeschlossen) return false
        _uiState.value = aktuell.copy(
            gameState = engine.neuesSpiel(
                modus = aktuell.gameState.modus,
                direktwahlAktiv = aktuell.gameState.direktwahlAktiv,
            ),
            zeigeUiVorschau = false,
            ausgewaehlterWert = null,
            emotionDetailsOffen = false,
            verlassenDialogOffen = false,
            herkunftEntwurf = HerkunftEntwurf(),
            ausgewaehlterErwerbId = null,
            auffangnetzBestaetigt = false,
        )
        return true
    }
}
