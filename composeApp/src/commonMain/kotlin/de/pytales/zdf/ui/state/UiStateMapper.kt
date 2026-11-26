package de.pytales.zdf.ui.state

import androidx.compose.runtime.Immutable
import de.pytales.zdf.content.GameContent
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.engine.GameState
import de.pytales.zdf.engine.WirkungZeile
import de.pytales.zdf.model.Ereignis
import de.pytales.zdf.model.Kartentyp
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.Quelle
import de.pytales.zdf.model.Stimmung
import de.pytales.zdf.model.WertSchluessel

/**
 * Aufbereiteter UI-Zustand für eine einzelne Kachel in der oberen Befindensleiste
 * sowie deren aufklappbare Touch-/Klick-Erklärkarte.
 */
@Immutable
data class WertKachelUiState(
    val schluessel: WertSchluessel,
    val bezeichnung: String,
    val rohwert: Int,
    val maximum: Int,
    val stufe: Int,
    val stufenName: String,
    val stufenKurz: String,
    val zustandssatz: String,
    val erklaerung: String,
    val folge: String,
    val gefuellteSegmente: Int,
    val segmenteGesamt: Int,
    val angezeigteAenderung: Int,
    val aenderungsText: String?,
    val aenderungIstSchlechter: Boolean,
    val istKritisch: Boolean,
)

/**
 * Aufbereiteter UI-Zustand für die Live-Emotions-Kachel rechts oben
 * inkl. vorbereiteter AP-5-Portrait-ID (`portrait_<herkunft>_<geschlecht>_<stimmung>`).
 */
@Immutable
data class LiveEmotionUiState(
    val stimmung: Stimmung,
    val stimmungBezeichnung: String,
    val stimmungKurzhinweis: String,
    val ausloeserBezeichnung: String?,
    val portraitId: String,
    val portraitRessourcenPfad: String,
    val istImMedienplan: Boolean,
    val personName: String,
    val stand: String,
    val herkunftTitel: String,
    val pfadMarke: String,
    val initialen: String,
    val hoechsteStufe: Int,
    val istUeberschrieben: Boolean,
    val zustandssatz: String,
)

/**
 * Aufbereiteter UI-Zustand für den 16:9-Szenenbild-Rahmen (vorbereitet für AP-5-WebP-Bilder).
 */
@Immutable
data class SzenenbildUiState(
    val bildId: String,
    val schauplatzBild: String,
    val schauplatzLabel: String,
    val ort: String,
    val jahr: Int,
    val pfadMarke: String,
    val szenenRessourcenPfad: String,
    val fallbackRessourcenPfad: String,
    val istStufe1Verfuegbar: Boolean,
    val istStufe2Geplant: Boolean,
)

@Immutable
data class EntscheidungsOptionUiState(
    val index: Int,
    val titel: String,
    val beschreibung: String,
    val hinweis: String?,
)

@Immutable
data class QuelleUiState(
    val kurz: String,
    val voll: String?,
    val art: String,
    val artLabel: String,
    val einordnung: String,
    val vertiefung: String?,
)

@Immutable
data class EntscheidungsKarteUiState(
    val ereignisId: String,
    val kartentyp: Kartentyp,
    val kartentypKopfzeile: String,
    val kartentypBezeichnung: String,
    val aktenzeichen: String,
    val ort: String,
    val jahr: Int,
    val pfadMarke: String,
    val text: String,
    val optionen: List<EntscheidungsOptionUiState>,
    val quelle: QuelleUiState,
    val szenenbild: SzenenbildUiState,
)

@Immutable
data class EreignisAusgangUiState(
    val ereignisId: String,
    val gewaehlterTitel: String,
    val ausgangsText: String,
    val wirkungen: List<WirkungZeile>,
    val neueMerkmaleNamen: List<String>,
)

/**
 * Reine, zustandslose Mapping-Funktionen von [GameEngine] / [GameState] / [GameContent]
 * auf die darstellungsfertigen UI-Zustände für AP 3 und AP 4.
 */
object UiStateMapper {

    private val SCHAUPLATZ_LABELS: Map<String, String> = mapOf(
        "schauplatz_amt" to "Amt",
        "schauplatz_bahnhof" to "Bahnhof",
        "schauplatz_bauernhof" to "Bauernhof",
        "schauplatz_brotschlange" to "Brotschlange",
        "schauplatz_etappe" to "Etappe",
        "schauplatz_fabrik" to "Fabrik",
        "schauplatz_gefangenenlager" to "Gefangenenlager",
        "schauplatz_graben" to "Grabenstellung",
        "schauplatz_landstrasse" to "Landstraße",
        "schauplatz_lazarett" to "Lazarett",
        "schauplatz_nachschub" to "Nachschub",
        "schauplatz_niemandsland" to "Niemandsland",
        "schauplatz_quartier" to "Quartier",
        "schauplatz_schreibstube" to "Schreibstube",
        "schauplatz_versammlung" to "Versammlung",
        "schauplatz_wirtshaus" to "Wirtshaus",
        "schauplatz_wohnviertel" to "Wohnviertel",
    )

    private val QUELLEN_ART_LABELS: Map<String, String> = mapOf(
        "akte" to "Amtliche Akte",
        "bild" to "Bildquelle",
        "brief" to "Brief / Feldpost",
        "darstellung" to "Historische Darstellung",
        "erinnerung" to "Zeitzeugen-Erinnerung",
        "gesetz" to "Gesetz / Verordnung",
        "statistik" to "Statistik",
        "zeitung" to "Zeitungsartikel",
    )

    fun mapBefindensLeiste(
        engine: GameEngine,
        state: GameState,
    ): List<WertKachelUiState> {
        val definitionen = engine.content.konfiguration.werte.definitionen
        return engine.werteAnzeige(state).map { status ->
            val definition = definitionen.getValue(status.schluessel)
            val satz = definition.zustandssaetze.getOrElse(status.stufe) {
                definition.zustandssaetze.lastOrNull().orEmpty()
            }
            val delta = status.angezeigteAenderung
            val deltaText = when {
                delta > 0 -> "+$delta"
                delta < 0 -> delta.toString()
                else -> null
            }
            WertKachelUiState(
                schluessel = status.schluessel,
                bezeichnung = status.bezeichnung,
                rohwert = status.rohwert,
                maximum = status.maximum,
                stufe = status.stufe,
                stufenName = status.stufenName,
                stufenKurz = status.stufenKurz,
                zustandssatz = satz,
                erklaerung = status.erklaerung,
                folge = status.folge,
                gefuellteSegmente = status.gefuellteSegmente,
                segmenteGesamt = status.segmenteGesamt,
                angezeigteAenderung = delta,
                aenderungsText = deltaText,
                aenderungIstSchlechter = delta > 0,
                istKritisch = status.stufe >= 3,
            )
        }
    }

    fun mapLiveEmotion(
        engine: GameEngine,
        state: GameState,
    ): LiveEmotionUiState {
        val content = engine.content
        val snapshot = engine.liveEmotion(state)
        val person = state.person
        val pfadMarke = content.konfiguration.pfade.definitionen[state.pfad]?.marke ?: state.pfad.code
        val portraitId = snapshot.portraitId ?: "portrait_unbekannt_${snapshot.stimmung.code}"
        val dateityp = content.medienplan.format.dateityp
        val ausloeserBezeichnung = when {
            snapshot.istUeberschrieben -> "Aktuelle Szene"
            snapshot.ausloesenderWert != null ->
                content.konfiguration.werte.definitionen[snapshot.ausloesenderWert]?.bezeichnung
            else -> null
        }

        val vollerName = person?.vollerName?.ifBlank { null } ?: "Ohne Zuordnung"
        val stand = person?.stand?.ifBlank { null } ?: "Ausgangslage 1914"
        val herkunftTitel = person?.herkunftTitel?.ifBlank { null } ?: "Noch offen"
        val initialen = if (person != null) {
            berechneInitialen(person.vorname, person.familienname)
        } else {
            "ZF"
        }

        return LiveEmotionUiState(
            stimmung = snapshot.stimmung,
            stimmungBezeichnung = formatStimmungBezeichnung(snapshot.stimmung),
            stimmungKurzhinweis = formatStimmungKurzhinweis(snapshot.stimmung),
            ausloeserBezeichnung = ausloeserBezeichnung,
            portraitId = portraitId,
            portraitRessourcenPfad = "portraits/$portraitId.$dateityp",
            istImMedienplan = portraitId in content.portraitById,
            personName = vollerName,
            stand = stand,
            herkunftTitel = herkunftTitel,
            pfadMarke = pfadMarke,
            initialen = initialen,
            hoechsteStufe = snapshot.hoechsteStufe,
            istUeberschrieben = snapshot.istUeberschrieben,
            zustandssatz = engine.zustandssatz(state),
        )
    }

    fun mapSzenenbild(
        content: GameContent,
        ereignis: Ereignis,
        jahr: Int,
        pfad: Pfad,
    ): SzenenbildUiState {
        val pfadMarke = content.konfiguration.pfade.definitionen[pfad]?.marke ?: pfad.code
        val dateityp = content.medienplan.format.dateityp
        val hatStufe1 = content.medienplan.schauplatzbilder.any { it.id == ereignis.schauplatzBild }
        val hatStufe2 = content.medienplan.einzelSzenenbilder.any { it.id == ereignis.bildId }

        return SzenenbildUiState(
            bildId = ereignis.bildId,
            schauplatzBild = ereignis.schauplatzBild,
            schauplatzLabel = formatSchauplatzLabel(ereignis.schauplatzBild),
            ort = ereignis.ort,
            jahr = jahr,
            pfadMarke = pfadMarke,
            szenenRessourcenPfad = "szenen/${ereignis.bildId}.$dateityp",
            fallbackRessourcenPfad = "schauplaetze/${ereignis.schauplatzBild}.$dateityp",
            istStufe1Verfuegbar = hatStufe1,
            istStufe2Geplant = hatStufe2,
        )
    }

    fun mapEntscheidungsKarte(
        content: GameContent,
        ereignis: Ereignis,
        aufgeloesterText: String,
        jahr: Int,
        pfad: Pfad,
    ): EntscheidungsKarteUiState {
        val pfadMarke = content.konfiguration.pfade.definitionen[pfad]?.marke ?: pfad.code
        val szenenbild = mapSzenenbild(content, ereignis, jahr, pfad)

        return EntscheidungsKarteUiState(
            ereignisId = ereignis.id,
            kartentyp = ereignis.kartentyp,
            kartentypKopfzeile = kartentypKopfzeile(ereignis.kartentyp),
            kartentypBezeichnung = kartentypBezeichnung(ereignis.kartentyp),
            aktenzeichen = aktenzeichenFuer(ereignis.kartentyp, jahr, ereignis.ort),
            ort = ereignis.ort,
            jahr = jahr,
            pfadMarke = pfadMarke,
            text = aufgeloesterText,
            optionen = ereignis.optionen.mapIndexed { index, option ->
                EntscheidungsOptionUiState(
                    index = index,
                    titel = option.titel,
                    beschreibung = option.beschreibung,
                    hinweis = option.hinweis?.trim()?.ifBlank { null },
                )
            },
            quelle = mapQuelle(ereignis.quelle),
            szenenbild = szenenbild,
        )
    }

    fun mapQuelle(quelle: Quelle): QuelleUiState = QuelleUiState(
        kurz = quelle.kurz,
        voll = quelle.voll?.trim()?.ifBlank { null },
        art = quelle.art,
        artLabel = formatQuellenArt(quelle.art),
        einordnung = quelle.einordnung,
        vertiefung = quelle.vertiefung?.trim()?.ifBlank { null },
    )

    fun mapEreignisAusgang(
        engine: GameEngine,
        phase: GamePhase.EreignisAusgang,
    ): EreignisAusgangUiState {
        val register = engine.content.merkmale.register
        return EreignisAusgangUiState(
            ereignisId = phase.ereignis.id,
            gewaehlterTitel = phase.option.titel,
            ausgangsText = phase.ausgangsText,
            wirkungen = engine.metrics.wirkungZeilen(phase.wertaenderungen),
            neueMerkmaleNamen = phase.neueMerkmale.map { id -> register[id]?.name ?: id },
        )
    }

    fun formatStimmungBezeichnung(stimmung: Stimmung): String = when (stimmung) {
        Stimmung.NEUTRAL -> "Gefasst"
        Stimmung.HUNGRIG -> "Hungrig"
        Stimmung.ERSCHOEPFT -> "Erschöpft"
        Stimmung.ANGST -> "Angst"
        Stimmung.EINSAM -> "Einsam"
    }

    fun formatStimmungKurzhinweis(stimmung: Stimmung): String = when (stimmung) {
        Stimmung.NEUTRAL -> "Lage noch tragbar"
        Stimmung.HUNGRIG -> "Der Hunger nagt"
        Stimmung.ERSCHOEPFT -> "Kräfte schwinden"
        Stimmung.ANGST -> "Unter Beobachtung"
        Stimmung.EINSAM -> "Auf dich gestellt"
    }

    fun kartentypKopfzeile(kartentyp: Kartentyp): String = when (kartentyp) {
        Kartentyp.KARTE -> "ALLTAGSBERICHT"
        Kartentyp.FELDPOST -> "FELDPOSTBRIEF"
        Kartentyp.LEBENSMITTEL -> "REICHS-LEBENSMITTELKARTE"
        Kartentyp.ZEITUNG -> "TAGESBLATT · MELDUNG"
        Kartentyp.AMTLICH -> "AMTLICHE VERFÜGUNG"
    }

    fun kartentypBezeichnung(kartentyp: Kartentyp): String = when (kartentyp) {
        Kartentyp.KARTE -> "Alltagskarte"
        Kartentyp.FELDPOST -> "Feldpost"
        Kartentyp.LEBENSMITTEL -> "Lebensmittelkarte"
        Kartentyp.ZEITUNG -> "Zeitung"
        Kartentyp.AMTLICH -> "Amtlich"
    }

    fun aktenzeichenFuer(kartentyp: Kartentyp, jahr: Int, ort: String): String = when (kartentyp) {
        Kartentyp.KARTE -> "$jahr · $ort"
        Kartentyp.FELDPOST -> "Poststempel $jahr · $ort"
        Kartentyp.LEBENSMITTEL -> "Ausgabe $jahr · $ort"
        Kartentyp.ZEITUNG -> "Ausgabe $jahr · $ort"
        Kartentyp.AMTLICH -> "Az. $jahr · $ort"
    }

    fun formatSchauplatzLabel(schauplatzBild: String): String {
        SCHAUPLATZ_LABELS[schauplatzBild]?.let { return it }
        val bereinigt = schauplatzBild.removePrefix("schauplatz_").replace('_', ' ').trim()
        if (bereinigt.isEmpty()) return "Schauplatz"
        return bereinigt.split(' ')
            .filter { it.isNotBlank() }
            .joinToString(" ") { wort ->
                wort.replaceFirstChar { zeichen -> zeichen.uppercaseChar() }
            }
    }

    fun formatQuellenArt(art: String): String {
        val norm = art.trim().lowercase()
        QUELLEN_ART_LABELS[norm]?.let { return it }
        if (norm.isEmpty()) return "Quelle"
        return norm.replaceFirstChar { it.uppercaseChar() }
    }

    fun berechneInitialen(vorname: String, familienname: String): String {
        val v = vorname.trim().firstOrNull()?.uppercaseChar()
        val f = familienname.trim().firstOrNull()?.uppercaseChar()
        return when {
            v != null && f != null -> "$v$f"
            v != null -> v.toString()
            f != null -> f.toString()
            else -> "ZF"
        }
    }
}
