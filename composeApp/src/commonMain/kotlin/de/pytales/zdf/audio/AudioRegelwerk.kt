package de.pytales.zdf.audio

import androidx.compose.runtime.Immutable
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.engine.GameState
import de.pytales.zdf.model.Pfad

/**
 * Dezente, respektvolle Tonspuren der Anwendung.
 *
 * Auf den Pfaden [Pfad.FRONT] und [Pfad.ETAPPE] sowie im Auffangnetz ist ausschließlich
 * [STILLE] zulässig — dort greift die harte Musiksperre.
 */
enum class AudioSpur(
    val code: String,
    val bezeichnung: String,
) {
    STILLE("stille", "Stille"),
    START_RUHIG("start_ruhig", "Ruhige Archiv-Begleitung"),
    HEIMAT_RUHIG("heimat_ruhig", "Dezente Heimat-Begleitung"),
    EPILOG_RUHIG("epilog_ruhig", "Ruhiger Ausklang 1919"),
}

/**
 * Eindeutiger Grund, warum aktuell keine Musik abgespielt wird.
 */
enum class AudioSperrGrund(
    val code: String,
    val kurzLabel: String,
    val hinweis: String,
) {
    STUMMGESCHALTET(
        code = "stumm",
        kurzLabel = "Ton: Aus",
        hinweis = "Ton ist stummgeschaltet.",
    ),
    PFAD_FRONT(
        code = "front_sperre",
        kurzLabel = "Stille · Front",
        hinweis = "Respektvolle Stille: Auf dem Pfad Front wird strikt keine Musik abgespielt.",
    ),
    PFAD_ETAPPE(
        code = "etappe_sperre",
        kurzLabel = "Stille · Etappe",
        hinweis = "Respektvolle Stille: Auf dem Pfad Etappe wird strikt keine Musik abgespielt.",
    ),
    AUFFANGNETZ(
        code = "auffangnetz_stille",
        kurzLabel = "Stille · Einschnitt",
        hinweis = "Respektvolle Stille bei vorzeitigem Abbruch des Lebenswegs.",
    ),
}

/**
 * Unveränderlicher, vollständig prüfbarer Audio-Zustand für UI und Plattform-Ausgabe.
 */
@Immutable
data class AudioZustand(
    val audioAktiv: Boolean,
    val lautstaerke: Float,
    val aktiveSpur: AudioSpur,
    val musikGesperrt: Boolean,
    val sperrGrund: AudioSperrGrund?,
) {
    val spieltGerade: Boolean
        get() = aktiveSpur != AudioSpur.STILLE && audioAktiv && !musikGesperrt && lautstaerke > 0f
}

/**
 * Reines, plattformunabhängiges Regelwerk für das optionale dezente Audio.
 *
 * Zentrale pädagogische Leitplanke:
 * - **Harte Musiksperre auf `front` und `etappe`:** Sobald eine Figur den Pfad `front`
 *   oder `etappe` betritt (einschließlich Musterungsbescheid mit Zielpfad `front`/`etappe`
 *   sowie Abschluss eines `front`-/`etappe`-Durchgangs), wird strikt [AudioSpur.STILLE]
 *   erzwungen — unabhängig vom Stummschalter oder der eingestellten Lautstärke.
 * - **Respektvolle Stille im Auffangnetz:** Bei vorzeitigem Abbruch vor 1919 wird ebenfalls
 *   strikt keine Musik gespielt.
 * - **Standardmäßig schul- und browserfreundlich:** Ton startet stumm (`audioAktiv = false`)
 *   und bleibt bei Aktivierung auf einer sehr leisen, dezenten Lautstärke begrenzt.
 */
object AudioRegelwerk {

    const val STANDARD_LAUTSTAERKE: Float = 0.22f
    const val MAX_DEZENTE_LAUTSTAERKE: Float = 0.35f

    /**
     * Pfade mit harter Musiksperre (strikte, respektvolle Stille).
     */
    fun istMusikGesperrtFuerPfad(pfad: Pfad): Boolean =
        pfad == Pfad.FRONT || pfad == Pfad.ETAPPE

    /**
     * Begrenzt die Lautstärke auf den dezenten, unterrichtstauglichen Bereich (`0.0f .. 0.35f`).
     */
    fun begrenzeLautstaerke(lautstaerke: Float): Float =
        if (lautstaerke.isNaN()) 0f else lautstaerke.coerceIn(0f, MAX_DEZENTE_LAUTSTAERKE)

    /**
     * Ermittelt, ob im aktuellen [GameState] eine harte pädagogische Musiksperre greift.
     * Gibt `null` zurück, wenn dezenter Ton grundsätzlich erlaubt ist (Startmenü, Herkunftswahl,
     * Heimat-Pfad oder regulärer Heimat-Abschluss 1919).
     */
    fun musikSperreFuer(gameState: GameState): AudioSperrGrund? = when (val phase = gameState.phase) {
        is GamePhase.Start,
        is GamePhase.HerkunftWahl,
        -> null

        is GamePhase.MusterungErgebnis -> pfadSperre(phase.zielPfad)

        is GamePhase.Abgeschlossen -> when {
            phase.hartesEnde != null -> AudioSperrGrund.AUFFANGNETZ
            else -> pfadSperre(gameState.pfad)
        }

        is GamePhase.ErwerbWahl,
        is GamePhase.KapitelStart,
        is GamePhase.EreignisAnzeige,
        is GamePhase.EreignisAusgang,
        is GamePhase.KapitelAbschluss,
        -> pfadSperre(gameState.pfad)
    }

    /**
     * Berechnet den effektiven [AudioZustand] aus aktuellem [GameState] und Nutzereinstellung.
     * Die harte Musiksperre hat stets oberste Priorität vor `audioAktiv`.
     */
    fun bestimmeZustand(
        gameState: GameState,
        audioAktiv: Boolean,
        lautstaerke: Float = STANDARD_LAUTSTAERKE,
    ): AudioZustand {
        val effektiveLautstaerke = begrenzeLautstaerke(lautstaerke)
        val sperre = musikSperreFuer(gameState)
        if (sperre != null) {
            return AudioZustand(
                audioAktiv = audioAktiv,
                lautstaerke = effektiveLautstaerke,
                aktiveSpur = AudioSpur.STILLE,
                musikGesperrt = true,
                sperrGrund = sperre,
            )
        }

        if (!audioAktiv || effektiveLautstaerke <= 0f) {
            return AudioZustand(
                audioAktiv = audioAktiv,
                lautstaerke = effektiveLautstaerke,
                aktiveSpur = AudioSpur.STILLE,
                musikGesperrt = false,
                sperrGrund = AudioSperrGrund.STUMMGESCHALTET,
            )
        }

        val spur = when (val phase = gameState.phase) {
            is GamePhase.Start,
            is GamePhase.HerkunftWahl,
            -> AudioSpur.START_RUHIG

            is GamePhase.Abgeschlossen -> AudioSpur.EPILOG_RUHIG

            is GamePhase.KapitelStart -> if (phase.kapitel.istEpilog || gameState.jahr >= 1919) {
                AudioSpur.EPILOG_RUHIG
            } else {
                AudioSpur.HEIMAT_RUHIG
            }

            is GamePhase.EreignisAnzeige -> if (phase.istFinale || gameState.jahr >= 1919) {
                AudioSpur.EPILOG_RUHIG
            } else {
                AudioSpur.HEIMAT_RUHIG
            }

            is GamePhase.EreignisAusgang -> if (phase.istFinale || gameState.jahr >= 1919) {
                AudioSpur.EPILOG_RUHIG
            } else {
                AudioSpur.HEIMAT_RUHIG
            }

            is GamePhase.MusterungErgebnis,
            is GamePhase.ErwerbWahl,
            is GamePhase.KapitelAbschluss,
            -> if (gameState.jahr >= 1919) AudioSpur.EPILOG_RUHIG else AudioSpur.HEIMAT_RUHIG
        }

        return AudioZustand(
            audioAktiv = true,
            lautstaerke = effektiveLautstaerke,
            aktiveSpur = spur,
            musikGesperrt = false,
            sperrGrund = null,
        )
    }

    private fun pfadSperre(pfad: Pfad): AudioSperrGrund? = when (pfad) {
        Pfad.FRONT -> AudioSperrGrund.PFAD_FRONT
        Pfad.ETAPPE -> AudioSperrGrund.PFAD_ETAPPE
        Pfad.HEIMAT -> null
    }
}

/**
 * Schlanke, plattformübergreifende Audio-Ausgabe-Schnittstelle für Android, Desktop JVM
 * und Web (WasmJS + JS) sowie Unit-Test-Fakes.
 */
interface AudioAusgabe {
    fun aktualisiere(spur: AudioSpur, lautstaerke: Float)
    fun stoppe()
    fun freigeben()
}

/**
 * Stille Standard-/Fallback-Ausgabe (z. B. für Headless-Umgebungen oder Tests).
 */
object StilleAudioAusgabe : AudioAusgabe {
    override fun aktualisiere(spur: AudioSpur, lautstaerke: Float) = Unit
    override fun stoppe() = Unit
    override fun freigeben() = Unit
}

/**
 * Koordiniert [AudioRegelwerk] und [AudioAusgabe] mit doppelter Absicherung der Musiksperre:
 * Sobald [AudioZustand.spieltGerade] `false` ist oder eine Sperre greift, wird garantiert
 * [AudioAusgabe.stoppe] aufgerufen und niemals eine Musikspur an die Plattform übergeben.
 */
class AudioKoordinator(
    private val ausgabe: AudioAusgabe,
) {
    var letzterZustand: AudioZustand? = null
        private set

    var imHintergrundPausiert: Boolean = false
        private set

    private var ausgabeLaeuft: Boolean = false

    fun synchronisiere(
        gameState: GameState,
        audioAktiv: Boolean,
        lautstaerke: Float = AudioRegelwerk.STANDARD_LAUTSTAERKE,
    ): AudioZustand {
        val zustand = AudioRegelwerk.bestimmeZustand(
            gameState = gameState,
            audioAktiv = audioAktiv,
            lautstaerke = lautstaerke,
        )
        synchronisiereZustand(zustand)
        return zustand
    }

    fun synchronisiereZustand(zustand: AudioZustand) {
        val bisher = letzterZustand
        letzterZustand = zustand

        // Hintergrund-Lebenszyklus (z. B. Android onPause/onStop): Audio strikt gestoppt halten
        if (imHintergrundPausiert) {
            if (ausgabeLaeuft || bisher == null || zustand.musikGesperrt) {
                ausgabe.stoppe()
                ausgabeLaeuft = false
            }
            return
        }

        // Doppelte Schutzschranke: bei Sperre, Stille oder Stummschaltung immer strikt stoppen
        if (!zustand.spieltGerade || zustand.musikGesperrt || zustand.aktiveSpur == AudioSpur.STILLE) {
            if (ausgabeLaeuft || bisher == null || bisher.spieltGerade || zustand.musikGesperrt) {
                ausgabe.stoppe()
                ausgabeLaeuft = false
            }
            return
        }

        val unveraendert = ausgabeLaeuft &&
            bisher != null &&
            bisher.spieltGerade &&
            bisher.aktiveSpur == zustand.aktiveSpur &&
            bisher.lautstaerke == zustand.lautstaerke
        if (!unveraendert) {
            ausgabe.aktualisiere(zustand.aktiveSpur, zustand.lautstaerke)
            ausgabeLaeuft = true
        }
    }

    /**
     * Pausiert bzw. stummt die Audio-Ausgabe sofort beim Wechsel der App in den Hintergrund
     * (`pausiert = true`, z. B. Android `onPause`/`onStop`) und nimmt sie bei Rückkehr in den
     * Vordergrund (`pausiert = false`) nur dann wieder auf, wenn der letzte Zustand explizit
     * abspielbar und nicht gesperrt ist (Front/Etappe/Auffangnetz bleiben strikt stumm).
     */
    fun setzeHintergrundPausiert(pausiert: Boolean) {
        if (imHintergrundPausiert == pausiert) {
            if (pausiert && ausgabeLaeuft) {
                ausgabe.stoppe()
                ausgabeLaeuft = false
            }
            return
        }
        imHintergrundPausiert = pausiert
        if (pausiert) {
            ausgabe.stoppe()
            ausgabeLaeuft = false
        } else {
            val zustand = letzterZustand ?: return
            if (zustand.spieltGerade && !zustand.musikGesperrt && zustand.aktiveSpur != AudioSpur.STILLE) {
                ausgabe.aktualisiere(zustand.aktiveSpur, zustand.lautstaerke)
                ausgabeLaeuft = true
            } else {
                ausgabe.stoppe()
                ausgabeLaeuft = false
            }
        }
    }

    fun stoppe() {
        letzterZustand = letzterZustand?.copy(aktiveSpur = AudioSpur.STILLE)
        ausgabe.stoppe()
        ausgabeLaeuft = false
    }

    fun freigeben() {
        ausgabe.stoppe()
        ausgabe.freigeben()
        ausgabeLaeuft = false
        imHintergrundPausiert = false
        letzterZustand = null
    }
}
