package de.pytales.zdf.ui.state

import androidx.compose.runtime.Immutable
import de.pytales.zdf.content.GameContent
import de.pytales.zdf.engine.EinstiegKontext
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.engine.GameState
import de.pytales.zdf.engine.Lebenslage
import de.pytales.zdf.engine.ProtokollEintrag
import de.pytales.zdf.engine.WirkungZeile
import de.pytales.zdf.model.Ereignis
import de.pytales.zdf.model.Erwerbslage
import de.pytales.zdf.model.Kapitel
import de.pytales.zdf.model.Kartentyp
import de.pytales.zdf.model.MusterungsGrad
import de.pytales.zdf.model.MusterungsVermerk
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
 * Aufbereiteter UI-Zustand für das 16:9-Kapitelbild (vorbereitet für die 6 WebP-Kapitelbilder in AP 5).
 */
@Immutable
data class KapitelbildUiState(
    val bildId: String,
    val jahr: Int,
    val zeitraum: String,
    val ueberschrift: String,
    val pfadMarke: String,
    val istEpilog: Boolean,
    val ressourcenPfad: String,
    val istImMedienplan: Boolean,
)

/**
 * Aufbereiteter UI-Zustand für das Musterungsergebnis-Blatt (`GamePhase.MusterungErgebnis`).
 */
@Immutable
data class MusterungUiState(
    val grad: MusterungsGrad,
    val gradKurz: String,
    val gradLang: String,
    val gradErklaerung: String,
    val vermerk: MusterungsVermerk?,
    val vermerkKurz: String?,
    val vermerkLang: String?,
    val vermerkErklaerung: String?,
    val befund: String,
    val heeresklasse: String,
    val anlassBezeichnung: String,
    val zielPfad: Pfad,
    val zielPfadMarke: String,
    val zielPfadOrt: String,
    val zielPfadFolge: String,
    val personName: String,
    val jahrgang: Int?,
    val herkunftTitel: String,
    val friedensberuf: String,
    val groesseCm: Int?,
    val brustumfangCm: Int?,
)

/**
 * Aufbereiteter UI-Zustand für eine wählbare Erwerbslage (`GamePhase.ErwerbWahl`)
 * inklusive historischer Einordnung aus `GameEngine.erwerbHinweis(...)`.
 */
@Immutable
data class ErwerbOptionUiState(
    val id: String,
    val titel: String,
    val zusatz: String,
    val text: String,
    val folge: String,
    val berufsBezeichnung: String,
    val hinweisStempel: String?,
    val hinweisText: String?,
    val wirkungen: List<WirkungZeile>,
    val etappeMoeglich: Boolean,
)

/**
 * Aufbereiteter UI-Zustand für die ruhige Jahres-Auftaktkarte (`GamePhase.KapitelStart`).
 */
@Immutable
data class KapitelStartUiState(
    val jahr: Int,
    val istEpilog: Boolean,
    val zeitraum: String,
    val ueberschrift: String,
    val text: String,
    val stichworte: List<String>,
    val leitfrage: String?,
    val wirkungText: String?,
    val wirkungen: List<WirkungZeile>,
    val kapitelbild: KapitelbildUiState,
    val aktionLabel: String,
)

/**
 * Aufbereiteter UI-Zustand für den Jahresrückblick (`GamePhase.KapitelAbschluss`).
 */
@Immutable
data class KapitelAbschlussUiState(
    val jahr: Int,
    val zeitraum: String,
    val ueberschrift: String,
    val rueckblick: String?,
    val stichworte: List<String>,
    val leitfrage: String,
    val kipppunkt: String,
    val pfadMarke: String,
    val zustandssatz: String,
    val naechstesKapitelJahr: Int?,
    val naechstesKapitelTitel: String?,
    val weiterLabel: String,
)

/**
 * Lesbarer Eintrag aus dem Spielprotokoll für den Entscheidungsrückblick im Lebenslauf.
 */
@Immutable
data class ProtokollUiEintrag(
    val jahr: Int,
    val ereignisId: String,
    val station: String,
    val wahl: String,
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

    fun mapKapitelbild(
        content: GameContent,
        kapitel: Kapitel,
        pfad: Pfad,
    ): KapitelbildUiState {
        val pfadMarke = content.konfiguration.pfade.definitionen[pfad]?.marke ?: pfad.code
        val dateityp = content.medienplan.format.dateityp
        val imPlan = content.medienplan.kapitelbilder.any { it.id == kapitel.bildId }
        return KapitelbildUiState(
            bildId = kapitel.bildId,
            jahr = kapitel.jahr,
            zeitraum = kapitel.zeitraum,
            ueberschrift = kapitel.ueberschrift,
            pfadMarke = pfadMarke,
            istEpilog = kapitel.istEpilog,
            ressourcenPfad = "kapitel/${kapitel.bildId}.$dateityp",
            istImMedienplan = imPlan,
        )
    }

    fun mapMusterungErgebnis(
        content: GameContent,
        phase: GamePhase.MusterungErgebnis,
        person: Lebenslage?,
    ): MusterungUiState {
        val musterungDaten = content.herkunft.musterung
        val daten = phase.daten
        val gradInfo = musterungDaten.grade[daten.grad]
        val vermerkInfo = daten.vermerk?.let { musterungDaten.vermerke[it] }
        val pfadDef = content.konfiguration.pfade.definitionen[phase.zielPfad]

        val anlass = when (daten.strenge) {
            "august_1914" -> "Kriegsfreiwillige Meldung (August 1914)"
            "einberufung" -> "Reguläre Einberufung"
            else -> daten.strenge
        }

        val zielFolge = when (phase.zielPfad) {
            Pfad.FRONT -> "Überweisung an einen Feldtruppenteil — dein Weg führt an die Front."
            Pfad.ETAPPE -> "Einsatz im rückwärtigen Dienst — dein Weg führt in die Etappe."
            Pfad.HEIMAT -> "Kein Front- oder Etappendienst — du bleibst im Reich und wählst deinen Platz in der Heimat."
        }

        return MusterungUiState(
            grad = daten.grad,
            gradKurz = gradInfo?.kurz ?: daten.grad.code,
            gradLang = gradInfo?.lang ?: daten.grad.code,
            gradErklaerung = gradInfo?.erklaerung.orEmpty(),
            vermerk = daten.vermerk,
            vermerkKurz = vermerkInfo?.kurz,
            vermerkLang = vermerkInfo?.lang,
            vermerkErklaerung = vermerkInfo?.erklaerung,
            befund = daten.befund,
            heeresklasse = daten.heeresklasse,
            anlassBezeichnung = anlass,
            zielPfad = phase.zielPfad,
            zielPfadMarke = pfadDef?.marke ?: phase.zielPfad.code,
            zielPfadOrt = pfadDef?.ort.orEmpty(),
            zielPfadFolge = zielFolge,
            personName = person?.vollerName?.ifBlank { null } ?: "Gemusterte Person",
            jahrgang = person?.jahrgang,
            herkunftTitel = person?.herkunftTitel.orEmpty(),
            friedensberuf = person?.friedensberuf.orEmpty(),
            groesseCm = person?.groesseCm,
            brustumfangCm = person?.brustumfangCm,
        )
    }

    fun mapErwerbOptionen(
        engine: GameEngine,
        state: GameState,
        optionen: List<Erwerbslage>,
    ): List<ErwerbOptionUiState> {
        val geschlecht = state.person?.geschlecht
        return optionen.map { erwerb ->
            val hinweis = engine.erwerbHinweis(state, erwerb)
            val berufsBezeichnung = geschlecht?.let { erwerb.bezeichnung[it] } ?: erwerb.titel
            ErwerbOptionUiState(
                id = erwerb.id,
                titel = erwerb.titel,
                zusatz = erwerb.zusatz,
                text = erwerb.text,
                folge = erwerb.folge,
                berufsBezeichnung = berufsBezeichnung,
                hinweisStempel = hinweis?.first,
                hinweisText = hinweis?.second,
                wirkungen = engine.metrics.wirkungZeilen(erwerb.werte),
                etappeMoeglich = erwerb.etappeMoeglich,
            )
        }
    }

    fun mapKapitelStart(
        engine: GameEngine,
        phase: GamePhase.KapitelStart,
        pfad: Pfad,
    ): KapitelStartUiState {
        val kapitel = phase.kapitel
        val leitfrage = kapitel.bogen[pfad]?.frage
        val aktionLabel = if (kapitel.istEpilog) {
            "Epilog ${kapitel.jahr} beginnen"
        } else {
            "In das Jahr ${kapitel.jahr} eintreten"
        }
        return KapitelStartUiState(
            jahr = kapitel.jahr,
            istEpilog = kapitel.istEpilog,
            zeitraum = kapitel.zeitraum,
            ueberschrift = kapitel.ueberschrift,
            text = kapitel.text,
            stichworte = kapitel.stichworte,
            leitfrage = leitfrage,
            wirkungText = kapitel.wirkungText?.trim()?.ifBlank { null },
            wirkungen = engine.metrics.wirkungZeilen(phase.kapitelWirkung),
            kapitelbild = mapKapitelbild(engine.content, kapitel, pfad),
            aktionLabel = aktionLabel,
        )
    }

    fun mapKapitelAbschluss(
        content: GameContent,
        phase: GamePhase.KapitelAbschluss,
        pfad: Pfad,
        zustandssatz: String,
    ): KapitelAbschlussUiState {
        val kapitel = phase.kapitel
        val kapitelListe = content.kapitel.kapitel
        val aktuellerIndex = kapitelListe.indexOfFirst { it.jahr == kapitel.jahr }
        val naechstes = kapitelListe.getOrNull(aktuellerIndex + 1)
        val pfadMarke = content.konfiguration.pfade.definitionen[pfad]?.marke ?: pfad.code

        val weiterLabel = when {
            naechstes == null -> "Zum Abschluss 1919"
            naechstes.istEpilog -> "Weiter zum Epilog ${naechstes.jahr}: ${naechstes.ueberschrift}"
            else -> "Weiter in das Jahr ${naechstes.jahr}: ${naechstes.ueberschrift}"
        }

        return KapitelAbschlussUiState(
            jahr = kapitel.jahr,
            zeitraum = kapitel.zeitraum,
            ueberschrift = kapitel.ueberschrift,
            rueckblick = kapitel.rueckblick?.trim()?.ifBlank { null },
            stichworte = kapitel.stichworte,
            leitfrage = phase.bogen.frage,
            kipppunkt = phase.bogen.kippt,
            pfadMarke = pfadMarke,
            zustandssatz = zustandssatz,
            naechstesKapitelJahr = naechstes?.jahr,
            naechstesKapitelTitel = naechstes?.ueberschrift,
            weiterLabel = weiterLabel,
        )
    }

    /**
     * Liefert die passende Beschriftung für den Fortfahren-Knopf nach einem Entscheidungs-Ausgang.
     */
    fun mapWeiterLabel(
        engine: GameEngine,
        state: GameState,
        phase: GamePhase.EreignisAusgang,
    ): String {
        if (phase.istFinale) {
            return "Zum Lebenslauf 1919"
        }
        if (phase.istEinstieg) {
            return when (state.einstiegKontext) {
                EinstiegKontext.MELDUNG -> "Zum Musterungsbescheid"
                EinstiegKontext.ETAPPE -> if (phase.gewaehlteOptionIndex == 0) {
                    "In das Jahr 1914"
                } else {
                    "Weiter"
                }

                EinstiegKontext.OFFIZIER,
                EinstiegKontext.ABSCHIED,
                EinstiegKontext.KEINER,
                -> "In das Jahr 1914"
            }
        }
        if (engine.metrics.pruefeHartesEnde(state.werte, state.jahr, engine.content.kapitel.epilogJahr) != null) {
            return "Weiter"
        }

        val kapitel = engine.content.kapitelByJahr[state.jahr]
        val sollZiehungen = kapitel?.ziehungen?.get(state.modus) ?: 1
        val kapitelFertig = state.ziehungenImKapitel >= sollZiehungen ||
            (engine.verfuegbareEreignisse(state).isEmpty() && state.vorgemerkteKetten.none { it.abJahr <= state.jahr })
        if (kapitelFertig) {
            return if (kapitel?.istEpilog == true || state.jahr >= engine.content.kapitel.epilogJahr) {
                "Zur Abschluss-Szene 1919"
            } else {
                "Zum Jahresrückblick ${state.jahr}"
            }
        }
        return "Nächstes Ereignis"
    }

    /**
     * Erzeugt die ruhige Kontextzeile für `KopfLeiste` (Kapitel + Fortschritt oder Einstieg/Epilog).
     */
    fun mapKopfKapitelTitel(
        content: GameContent,
        state: GameState,
    ): String? {
        val kapitel = content.kapitelByJahr[state.jahr]
        val sollZiehungen = kapitel?.ziehungen?.get(state.modus) ?: 1
        return when (val phase = state.phase) {
            is GamePhase.MusterungErgebnis -> "Einstieg · Musterungsbescheid"
            is GamePhase.ErwerbWahl -> "Einstieg · Erwerbslage 1914"
            is GamePhase.KapitelStart -> if (phase.kapitel.istEpilog) {
                "Epilog · ${phase.kapitel.ueberschrift}"
            } else {
                phase.kapitel.ueberschrift
            }

            is GamePhase.KapitelAbschluss -> "Jahresrückblick · ${phase.kapitel.ueberschrift}"
            is GamePhase.EreignisAnzeige -> when {
                phase.istEinstieg -> "Einstieg · August 1914"
                phase.istFinale -> "Epilog · Abschluss 1919"
                else -> {
                    val nummer = (state.ziehungenImKapitel + 1).coerceAtMost(sollZiehungen)
                    val titel = kapitel?.ueberschrift.orEmpty()
                    if (titel.isNotBlank()) "$titel · Station $nummer/$sollZiehungen" else "Station $nummer/$sollZiehungen"
                }
            }

            is GamePhase.EreignisAusgang -> when {
                phase.istEinstieg -> "Einstieg · August 1914"
                phase.istFinale -> "Epilog · Abschluss 1919"
                else -> {
                    val nummer = state.ziehungenImKapitel.coerceIn(1, sollZiehungen)
                    val titel = kapitel?.ueberschrift.orEmpty()
                    if (titel.isNotBlank()) "$titel · Station $nummer/$sollZiehungen" else "Station $nummer/$sollZiehungen"
                }
            }

            else -> kapitel?.ueberschrift
        }
    }

    /**
     * Bereitet die protokollierten Entscheidungen eines Durchgangs lesbar für den Lebenslauf auf.
     */
    fun mapProtokollEintraege(
        content: GameContent,
        protokoll: List<ProtokollEintrag>,
    ): List<ProtokollUiEintrag> = protokoll.map { eintrag ->
        val station = when (eintrag.ereignisId) {
            "herkunft" -> "Herkunft & Figur"
            "musterung" -> "Musterung"
            "erwerb" -> "Erwerbslage 1914"
            else -> {
                val ev = content.ereignisById[eintrag.ereignisId]
                if (ev != null) {
                    val typ = kartentypBezeichnung(ev.kartentyp)
                    "${ev.ort} ($typ)"
                } else {
                    eintrag.ereignisId
                }
            }
        }
        ProtokollUiEintrag(
            jahr = eintrag.jahr,
            ereignisId = eintrag.ereignisId,
            station = station,
            wahl = eintrag.wahl,
        )
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
