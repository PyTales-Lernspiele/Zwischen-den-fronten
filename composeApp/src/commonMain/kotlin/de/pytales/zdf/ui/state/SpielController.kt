package de.pytales.zdf.ui.state

import androidx.compose.runtime.Immutable
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
 * Unveränderlicher Gesamt-UI-Zustand rund um [GameState] und globale UI-Einstellungen.
 */
@Immutable
data class SpielUiState(
    val gameState: GameState,
    val schriftgroesse: Schriftgroesse = Schriftgroesse.MITTEL,
    val analyseModus: Boolean = false,
    val zeigeUiVorschau: Boolean = false,
    val aufgeklappteGrundsaetze: Set<String> = emptySet(),
    val ausgewaehlterWert: WertSchluessel? = null,
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
) {
    constructor(
        content: GameContent,
        random: RandomSource = KotlinRandomSource(),
        initialSchriftgroesse: Schriftgroesse = Schriftgroesse.MITTEL,
        initialAnalyseModus: Boolean = false,
    ) : this(
        engine = GameEngine(content, random),
        initialSchriftgroesse = initialSchriftgroesse,
        initialAnalyseModus = initialAnalyseModus,
    )

    val content: GameContent
        get() = engine.content

    private val _uiState = MutableStateFlow(
        SpielUiState(
            gameState = engine.neuesSpiel(),
            schriftgroesse = initialSchriftgroesse,
            analyseModus = initialAnalyseModus,
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

    fun waehleWertErklaerung(schluessel: WertSchluessel?) {
        _uiState.update { it.copy(ausgewaehlterWert = schluessel) }
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
        _uiState.value = aktuell.copy(auffangnetzBestaetigt = true)
        return true
    }

    /**
     * Startet nach abgeschlossenem Durchgang (regulär 1919 oder nach Auffangnetz) einen
     * frischen Durchgang im Startmenü. Globale UI-Einstellungen (`schriftgroesse`, `analyseModus`,
     * gewählter `modus` und `direktwahlAktiv`) bleiben für den Unterricht erhalten.
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
            herkunftEntwurf = HerkunftEntwurf(),
            ausgewaehlterErwerbId = null,
            auffangnetzBestaetigt = false,
        )
        return true
    }
}
