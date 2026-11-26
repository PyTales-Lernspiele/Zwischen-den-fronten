package de.pytales.zdf.engine

import de.pytales.zdf.model.Ereignis
import de.pytales.zdf.model.EreignisOption
import de.pytales.zdf.model.Erwerbslage
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.HartesEndeId
import de.pytales.zdf.model.Kapitel
import de.pytales.zdf.model.KapitelBogen
import de.pytales.zdf.model.MusterungsGrad
import de.pytales.zdf.model.MusterungsVermerk
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.SpielModus
import de.pytales.zdf.model.Stimmung
import de.pytales.zdf.model.WertSchluessel

/**
 * Erzeugte Personen- und Lebenslage der gespielten Figur (reine Anzeige & historische Rahmung).
 */
data class Lebenslage(
    val herkunftId: String,
    val herkunftTitel: String,
    val geschlecht: Geschlecht,
    val alter: Int,
    val jahrgang: Int,
    val vorname: String,
    val familienname: String,
    val friedensberuf: String,
    val stand: String,
    val heeresklasse: String,
    val groesseCm: Int,
    val brustumfangCm: Int,
    val pfad: Pfad,
    val musterung: MusterungsGrad? = null,
    val vermerk: MusterungsVermerk? = null,
    val befund: String? = null,
    val erwerbId: String? = null,
) {
    val vollerName: String
        get() = "$vorname $familienname".trim()
}

data class MusterungErgebnisDaten(
    val grad: MusterungsGrad,
    val vermerk: MusterungsVermerk?,
    val befund: String,
    val heeresklasse: String,
    val strenge: String,
)

data class VorgemerkteKette(
    val ereignisId: String,
    val abJahr: Int,
)

data class ProtokollEintrag(
    val jahr: Int,
    val ereignisId: String,
    val wahl: String,
)

enum class EinstiegKontext {
    KEINER,
    MELDUNG,
    OFFIZIER,
    ETAPPE,
    ABSCHIED,
}

data class HartesEndeErgebnis(
    val id: HartesEndeId,
    val titel: String,
    val text: String,
    val jahr: Int,
)

/**
 * Abgeschlossene Spielphase für den UI-Zustandsautomaten.
 */
sealed interface GamePhase {
    data object Start : GamePhase

    data object HerkunftWahl : GamePhase

    data class MusterungErgebnis(
        val daten: MusterungErgebnisDaten,
        val zielPfad: Pfad,
    ) : GamePhase

    data class ErwerbWahl(
        val optionen: List<Erwerbslage>,
    ) : GamePhase

    data class KapitelStart(
        val kapitel: Kapitel,
        val kapitelWirkung: Map<WertSchluessel, Int> = emptyMap(),
    ) : GamePhase

    data class EreignisAnzeige(
        val ereignis: Ereignis,
        val aufgeloesterText: String,
        val istEinstieg: Boolean = false,
        val istFinale: Boolean = false,
    ) : GamePhase

    data class EreignisAusgang(
        val ereignis: Ereignis,
        val gewaehlteOptionIndex: Int,
        val option: EreignisOption,
        val ausgangsText: String,
        val wertaenderungen: Map<WertSchluessel, Int>,
        val neueMerkmale: List<String>,
        val istEinstieg: Boolean = false,
        val istFinale: Boolean = false,
    ) : GamePhase

    data class KapitelAbschluss(
        val kapitel: Kapitel,
        val bogen: KapitelBogen,
    ) : GamePhase

    data class Abgeschlossen(
        val hartesEnde: HartesEndeErgebnis?,
        val lebenslauf: LebenslaufErgebnis,
    ) : GamePhase
}

/**
 * Unveränderlicher Gesamtzustand eines Spieldurchgangs.
 */
data class GameState(
    val phase: GamePhase = GamePhase.Start,
    val modus: SpielModus = SpielModus.KURZ,
    val direktwahlAktiv: Boolean = false,
    val direktwahlPfad: Pfad? = null,
    val jahr: Int = 1914,
    val pfad: Pfad = Pfad.HEIMAT,
    val person: Lebenslage? = null,
    val werte: Map<WertSchluessel, Int> = emptyMap(),
    val letzteAenderungen: Map<WertSchluessel, Int> = emptyMap(),
    val merkmale: List<String> = emptyList(),
    val gespielteEreignisse: List<String> = emptyList(),
    val vorgemerkteKetten: List<VorgemerkteKette> = emptyList(),
    val ziehungenImKapitel: Int = 0,
    val stimmungUeberschreibung: Stimmung? = null,
    val verdachtRuhig: Int = 0,
    val verdachtStand: Int = 0,
    val protokoll: List<ProtokollEintrag> = emptyList(),
    val einstiegKontext: EinstiegKontext = EinstiegKontext.KEINER,
) {
    fun hatMerkmal(name: String): Boolean = name in merkmale
}
