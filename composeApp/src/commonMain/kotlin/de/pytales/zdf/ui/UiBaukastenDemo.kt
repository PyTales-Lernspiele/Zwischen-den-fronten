package de.pytales.zdf.ui

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import de.pytales.zdf.content.GameContent
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.engine.GameState
import de.pytales.zdf.engine.KotlinRandomSource
import de.pytales.zdf.engine.TextResolver
import de.pytales.zdf.model.Ereignis
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.Kartentyp
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.model.SpielModus
import de.pytales.zdf.model.Stimmung
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.components.ArchivStempel
import de.pytales.zdf.ui.components.ArchivTrennlinie
import de.pytales.zdf.ui.components.EntscheidungsKarte
import de.pytales.zdf.ui.components.EreignisAusgangKarte
import de.pytales.zdf.ui.components.KopfLeiste
import de.pytales.zdf.ui.components.SchriftgroessenSchalter
import de.pytales.zdf.ui.components.SzenenbildRahmen
import de.pytales.zdf.ui.state.UiStateMapper
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.LayoutKlasse
import de.pytales.zdf.ui.theme.Schriftgroesse
import kotlin.random.Random

/**
 * Kuratierte Beispiel-Ereignisse aus `content/ereignisse.json` für die 5 Kartentypen
 * in der AP-3-Vorschau (fällt automatisch auf das erste passende Ereignis zurück).
 */
internal object DemoBeispiele {
    private val BEVORZUGTE_IDS: Map<Kartentyp, String> = mapOf(
        Kartentyp.KARTE to "front_1914_marsch",
        Kartentyp.FELDPOST to "alltag_rotstift",
        Kartentyp.LEBENSMITTEL to "heimat_1915_brotkarte",
        Kartentyp.ZEITUNG to "heimat_1917_unterseeboot",
        Kartentyp.AMTLICH to "front_1918_befehl",
    )

    fun ereignisseFuerTyp(content: GameContent, typ: Kartentyp): List<Ereignis> {
        val alle = content.ereignisse.ereignisse.filter { it.kartentyp == typ }
        val bevorzugtId = BEVORZUGTE_IDS[typ]
        val bevorzugt = alle.firstOrNull { it.id == bevorzugtId }
        return if (bevorzugt != null) {
            listOf(bevorzugt) + alle.filter { it.id != bevorzugtId }
        } else {
            alle
        }
    }

    fun startZustand(
        engine: GameEngine,
        herkunftId: String,
        geschlecht: Geschlecht,
        ereignis: Ereignis,
    ): GameState {
        val zielPfad = ereignis.pfade.firstOrNull() ?: Pfad.FRONT
        var state = engine.herkunftWahlOeffnen(
            engine.neuesSpiel(modus = SpielModus.KURZ, direktwahlAktiv = true),
            modus = SpielModus.KURZ,
            direktwahlAktiv = true,
        )
        state = engine.waehlePerson(
            state = state,
            herkunftId = herkunftId,
            geschlecht = geschlecht,
            alter = 18,
            direktwahlPfad = zielPfad,
        )
        return zeigeEreignis(engine, state, ereignis)
    }

    fun zeigeEreignis(
        engine: GameEngine,
        state: GameState,
        ereignis: Ereignis,
    ): GameState {
        val jahr = ereignis.jahre.firstOrNull() ?: state.jahr
        val pfad = if (state.pfad in ereignis.pfade) {
            state.pfad
        } else {
            ereignis.pfade.firstOrNull() ?: state.pfad
        }
        val aufgeloesterText = TextResolver.aufloesen(
            fassung = ereignis.text,
            jahr = jahr,
            pfad = pfad,
            merkmale = state.merkmale,
            textPrioritaet = engine.content.merkmale.textPrioritaet,
        )
        return state.copy(
            jahr = jahr,
            pfad = pfad,
            person = state.person?.copy(pfad = pfad),
            stimmungUeberschreibung = ereignis.stimmung,
            phase = GamePhase.EreignisAnzeige(
                ereignis = ereignis,
                aufgeloesterText = aufgeloesterText,
            ),
        )
    }

    /**
     * Setzt realistische Werte-Änderungen über `ValueMetrics`, sodass Befindensleiste (inkl. Delta)
     * und Live-Emotions-Kachel live auf die gewählte [Stimmung] reagieren.
     */
    fun stimmungSimulieren(
        engine: GameEngine,
        state: GameState,
        zielStimmung: Stimmung,
    ): GameState {
        val zielWerte = when (zielStimmung) {
            Stimmung.NEUTRAL -> mapOf(
                WertSchluessel.VERSORGUNG to 10,
                WertSchluessel.BELASTUNG to 2,
                WertSchluessel.AUFMERKSAMKEIT to 1,
                WertSchluessel.RUECKHALT to 10,
            )

            Stimmung.HUNGRIG -> mapOf(
                WertSchluessel.VERSORGUNG to 4,
                WertSchluessel.BELASTUNG to 3,
                WertSchluessel.AUFMERKSAMKEIT to 2,
                WertSchluessel.RUECKHALT to 8,
            )

            Stimmung.ERSCHOEPFT -> mapOf(
                WertSchluessel.VERSORGUNG to 8,
                WertSchluessel.BELASTUNG to 9,
                WertSchluessel.AUFMERKSAMKEIT to 2,
                WertSchluessel.RUECKHALT to 8,
            )

            Stimmung.ANGST -> mapOf(
                WertSchluessel.VERSORGUNG to 8,
                WertSchluessel.BELASTUNG to 3,
                WertSchluessel.AUFMERKSAMKEIT to 9,
                WertSchluessel.RUECKHALT to 8,
            )

            Stimmung.EINSAM -> mapOf(
                WertSchluessel.VERSORGUNG to 8,
                WertSchluessel.BELASTUNG to 3,
                WertSchluessel.AUFMERKSAMKEIT to 2,
                WertSchluessel.RUECKHALT to 3,
            )
        }
        val delta = WertSchluessel.entries.associateWith { schluessel ->
            (zielWerte[schluessel] ?: 0) - (state.werte[schluessel] ?: 0)
        }
        val (neueWerte, effektiv) = engine.metrics.werteAnwenden(state.werte, delta)
        return state.copy(
            werte = neueWerte,
            letzteAenderungen = effektiv,
            stimmungUeberschreibung = null,
        )
    }
}

/**
 * Interaktive AP-3-Komponenten-Vorschau auf Basis echter JSON-Inhalte (`content/`)
 * und einer echten [GameEngine]-Instanz — zugleich Blaupause für den vollständigen
 * Spieldurchgang in AP 4.
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun UiBaukastenDemo(
    content: GameContent,
    schriftgroesse: Schriftgroesse,
    onSchriftgroesseChange: (Schriftgroesse) -> Unit,
    modifier: Modifier = Modifier,
) {
    val engine = remember(content) { GameEngine(content, KotlinRandomSource(Random(1914))) }

    var aktiverKartentyp by remember { mutableStateOf(Kartentyp.KARTE) }
    var ereignisIndexImTyp by remember { mutableStateOf(0) }
    var herkunftIndex by remember { mutableStateOf(0) }
    var geschlecht by remember { mutableStateOf(Geschlecht.MAENNLICH) }
    var analyseModus by remember { mutableStateOf(false) }
    var werkzeugleisteOffen by remember { mutableStateOf(true) }

    val herkuenfte = content.herkunft.herkuenfte
    val aktiveHerkunft = herkuenfte[herkunftIndex % herkuenfte.size]
    val typEreignisse = remember(content, aktiverKartentyp) {
        DemoBeispiele.ereignisseFuerTyp(content, aktiverKartentyp)
    }
    val aktivesEreignis = typEreignisse[ereignisIndexImTyp % typEreignisse.size]

    var gameState by remember(engine) {
        mutableStateOf(
            DemoBeispiele.startZustand(
                engine = engine,
                herkunftId = aktiveHerkunft.id,
                geschlecht = geschlecht,
                ereignis = aktivesEreignis,
            ),
        )
    }

    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val layoutKlasse = ArchivTheme.layoutKlasse

    val werteUi = remember(engine, gameState) {
        UiStateMapper.mapBefindensLeiste(engine, gameState)
    }
    val emotionUi = remember(engine, gameState) {
        UiStateMapper.mapLiveEmotion(engine, gameState)
    }
    val kapitelTitel = content.kapitelByJahr[gameState.jahr]?.ueberschrift

    val anzeigePhase = gameState.phase
    val angezeigtesEreignis = when (anzeigePhase) {
        is GamePhase.EreignisAnzeige -> anzeigePhase.ereignis
        is GamePhase.EreignisAusgang -> anzeigePhase.ereignis
        else -> aktivesEreignis
    }
    val aufgeloesterText = when (anzeigePhase) {
        is GamePhase.EreignisAnzeige -> anzeigePhase.aufgeloesterText
        is GamePhase.EreignisAusgang -> TextResolver.aufloesen(
            fassung = anzeigePhase.ereignis.text,
            jahr = gameState.jahr,
            pfad = gameState.pfad,
            merkmale = gameState.merkmale,
            textPrioritaet = content.merkmale.textPrioritaet,
        )
        else -> aktivesEreignis.text.standard
    }

    val kartenUi = remember(content, angezeigtesEreignis, aufgeloesterText, gameState.jahr, gameState.pfad) {
        UiStateMapper.mapEntscheidungsKarte(
            content = content,
            ereignis = angezeigtesEreignis,
            aufgeloesterText = aufgeloesterText,
            jahr = gameState.jahr,
            pfad = gameState.pfad,
        )
    }
    val ausgangUi = remember(engine, anzeigePhase) {
        if (anzeigePhase is GamePhase.EreignisAusgang) {
            UiStateMapper.mapEreignisAusgang(engine, anzeigePhase)
        } else {
            null
        }
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(farben.papier),
    ) {
        // 1. Obere Befindensleiste + Live-Emotions-Kachel rechts oben
        KopfLeiste(
            jahr = gameState.jahr,
            werte = werteUi,
            emotion = emotionUi,
            kapitelTitel = kapitelTitel,
            analyseModus = analyseModus,
            zusatzAktionen = {
                SchriftgroessenSchalter(
                    aktuell = schriftgroesse,
                    onAuswahl = onSchriftgroesseChange,
                    aufDunkel = true,
                    kompakt = layoutKlasse == LayoutKlasse.KOMPAKT,
                )
            },
        )

        // 2. Scrollbarer Hauptbereich: Demo-Steuerung + echte Spielbühne (Szenenbild + Entscheidungskarte)
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .verticalScroll(rememberScrollState()),
            contentAlignment = Alignment.TopCenter,
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .widthIn(max = metrik.maxInhaltsBreite)
                    .padding(horizontal = metrik.aussenAbstand, vertical = metrik.elementAbstand),
                verticalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
            ) {
                // Klappbare AP-3-Vorschau-Werkzeugleiste
                DemoWerkzeugLeiste(
                    offen = werkzeugleisteOffen,
                    onToggleOffen = { werkzeugleisteOffen = !werkzeugleisteOffen },
                    layoutKlasse = layoutKlasse,
                    schriftgroesse = schriftgroesse,
                    onSchriftgroesseChange = onSchriftgroesseChange,
                    aktiverKartentyp = aktiverKartentyp,
                    ereignisPositionText = "${(ereignisIndexImTyp % typEreignisse.size) + 1}/${typEreignisse.size}",
                    onKartentypWaehlen = { neuerTyp ->
                        aktiverKartentyp = neuerTyp
                        ereignisIndexImTyp = 0
                        val neuesEreignis = DemoBeispiele.ereignisseFuerTyp(content, neuerTyp).first()
                        gameState = DemoBeispiele.zeigeEreignis(engine, gameState, neuesEreignis)
                    },
                    onNaechstesEreignis = {
                        val naechsterIndex = (ereignisIndexImTyp + 1) % typEreignisse.size
                        ereignisIndexImTyp = naechsterIndex
                        gameState = DemoBeispiele.zeigeEreignis(engine, gameState, typEreignisse[naechsterIndex])
                    },
                    aktiveStimmung = emotionUi.stimmung,
                    onStimmungWaehlen = { ziel ->
                        gameState = DemoBeispiele.stimmungSimulieren(engine, gameState, ziel)
                    },
                    herkunftTitel = aktiveHerkunft.titel,
                    geschlecht = geschlecht,
                    onHerkunftWechseln = {
                        val naechste = (herkunftIndex + 1) % herkuenfte.size
                        herkunftIndex = naechste
                        gameState = DemoBeispiele.startZustand(
                            engine = engine,
                            herkunftId = herkuenfte[naechste].id,
                            geschlecht = geschlecht,
                            ereignis = angezeigtesEreignis,
                        )
                    },
                    onGeschlechtWechseln = {
                        val neu = if (geschlecht == Geschlecht.MAENNLICH) {
                            Geschlecht.WEIBLICH
                        } else {
                            Geschlecht.MAENNLICH
                        }
                        geschlecht = neu
                        gameState = DemoBeispiele.startZustand(
                            engine = engine,
                            herkunftId = aktiveHerkunft.id,
                            geschlecht = neu,
                            ereignis = angezeigtesEreignis,
                        )
                    },
                    analyseModus = analyseModus,
                    onAnalyseModusToggle = { analyseModus = !analyseModus },
                )

                // Eigentliche Spielbühne: 16:9 Szenenbild-Rahmen + Entscheidungskarte (bzw. Ausgang)
                val buehneNebeneinander = layoutKlasse == LayoutKlasse.BREIT

                if (buehneNebeneinander) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
                        verticalAlignment = Alignment.Top,
                    ) {
                        Column(
                            modifier = Modifier.weight(0.42f),
                            verticalArrangement = Arrangement.spacedBy(10.dp),
                        ) {
                            SzenenbildRahmen(
                                szenenbild = kartenUi.szenenbild,
                                analyseModus = analyseModus,
                            )
                            ZustandsNotiz(
                                zustandssatz = emotionUi.zustandssatz,
                                portraitId = emotionUi.portraitId,
                                analyseModus = analyseModus,
                            )
                        }

                        Column(
                            modifier = Modifier.weight(0.58f),
                            verticalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
                        ) {
                            EntscheidungsKarte(
                                karte = kartenUi,
                                ausgewaehlteOptionIndex = (anzeigePhase as? GamePhase.EreignisAusgang)?.gewaehlteOptionIndex,
                                optionenAktiv = anzeigePhase is GamePhase.EreignisAnzeige,
                                analyseModus = analyseModus,
                                onOptionWaehlen = { optionIndex ->
                                    if (gameState.phase is GamePhase.EreignisAnzeige) {
                                        gameState = engine.waehleOption(gameState, optionIndex)
                                    }
                                },
                            )

                            if (ausgangUi != null) {
                                EreignisAusgangKarte(
                                    ausgang = ausgangUi,
                                    weiterLabel = "Karte erneut prüfen / nächste Beispielkarte",
                                    onWeiter = {
                                        val naechsterIndex = (ereignisIndexImTyp + 1) % typEreignisse.size
                                        ereignisIndexImTyp = naechsterIndex
                                        gameState = DemoBeispiele.zeigeEreignis(
                                            engine = engine,
                                            state = gameState,
                                            ereignis = typEreignisse[naechsterIndex],
                                        )
                                    },
                                )
                            }
                        }
                    }
                } else {
                    // Android-Hochformat (KOMPAKT) und Tablet (MITTEL): klarer vertikaler Lesefluss
                    SzenenbildRahmen(
                        szenenbild = kartenUi.szenenbild,
                        analyseModus = analyseModus,
                    )

                    EntscheidungsKarte(
                        karte = kartenUi,
                        ausgewaehlteOptionIndex = (anzeigePhase as? GamePhase.EreignisAusgang)?.gewaehlteOptionIndex,
                        optionenAktiv = anzeigePhase is GamePhase.EreignisAnzeige,
                        analyseModus = analyseModus,
                        onOptionWaehlen = { optionIndex ->
                            if (gameState.phase is GamePhase.EreignisAnzeige) {
                                gameState = engine.waehleOption(gameState, optionIndex)
                            }
                        },
                    )

                    if (ausgangUi != null) {
                        EreignisAusgangKarte(
                            ausgang = ausgangUi,
                            weiterLabel = "Nächste Beispielkarte laden",
                            onWeiter = {
                                val naechsterIndex = (ereignisIndexImTyp + 1) % typEreignisse.size
                                ereignisIndexImTyp = naechsterIndex
                                gameState = DemoBeispiele.zeigeEreignis(
                                    engine = engine,
                                    state = gameState,
                                    ereignis = typEreignisse[naechsterIndex],
                                )
                            },
                        )
                    }

                    ZustandsNotiz(
                        zustandssatz = emotionUi.zustandssatz,
                        portraitId = emotionUi.portraitId,
                        analyseModus = analyseModus,
                    )
                }

                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun DemoWerkzeugLeiste(
    offen: Boolean,
    onToggleOffen: () -> Unit,
    layoutKlasse: LayoutKlasse,
    schriftgroesse: Schriftgroesse,
    onSchriftgroesseChange: (Schriftgroesse) -> Unit,
    aktiverKartentyp: Kartentyp,
    ereignisPositionText: String,
    onKartentypWaehlen: (Kartentyp) -> Unit,
    onNaechstesEreignis: () -> Unit,
    aktiveStimmung: Stimmung,
    onStimmungWaehlen: (Stimmung) -> Unit,
    herkunftTitel: String,
    geschlecht: Geschlecht,
    onHerkunftWechseln: () -> Unit,
    onGeschlechtWechseln: () -> Unit,
    analyseModus: Boolean,
    onAnalyseModusToggle: () -> Unit,
) {
    val farben = ArchivTheme.farben

    Surface(
        modifier = Modifier.fillMaxWidth(),
        color = farben.papierDunkel.copy(alpha = 0.72f),
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(1.dp, farben.linie),
    ) {
        Column(modifier = Modifier.fillMaxWidth()) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .defaultMinSize(minHeight = 44.dp)
                    .clickable(onClick = onToggleOffen)
                    .semantics {
                        role = Role.Button
                        contentDescription = if (offen) {
                            "UI-Baukasten-Steuerung einklappen"
                        } else {
                            "UI-Baukasten-Steuerung ausklappen"
                        }
                    }
                    .padding(horizontal = 12.dp, vertical = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Row(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.weight(1f),
                ) {
                    ArchivStempel(
                        text = "AP 3 · UI-VORSCHAU",
                        farbe = farben.akzent,
                    )
                    Text(
                        text = "Layout: ${layoutKlasse.bezeichnung} · Schrift: ${schriftgroesse.bezeichnung}",
                        style = MaterialTheme.typography.labelMedium,
                        color = farben.tinteMatt,
                    )
                }
                Text(
                    text = if (offen) "Ausblenden ▴" else "Steuerung ▾",
                    style = MaterialTheme.typography.labelSmall,
                    color = farben.tinte,
                )
            }

            AnimatedVisibility(
                visible = offen,
                enter = fadeIn() + expandVertically(),
                exit = fadeOut() + shrinkVertically(),
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(farben.papierHell.copy(alpha = 0.7f))
                        .padding(12.dp),
                    verticalArrangement = Arrangement.spacedBy(10.dp),
                ) {
                    // Zeile 1: Kartentypen (alle 5) + Durchblättern
                    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text(
                            text = "Kartentyp (echte Ereignisse aus content/ereignisse.json):",
                            style = MaterialTheme.typography.labelMedium,
                            color = farben.tinteMatt,
                        )
                        FlowRow(
                            horizontalArrangement = Arrangement.spacedBy(6.dp),
                            verticalArrangement = Arrangement.spacedBy(6.dp),
                        ) {
                            Kartentyp.entries.forEach { typ ->
                                DemoAuswahlKnopf(
                                    label = UiStateMapper.kartentypBezeichnung(typ),
                                    aktiv = typ == aktiverKartentyp,
                                    onClick = { onKartentypWaehlen(typ) },
                                )
                            }
                            DemoAuswahlKnopf(
                                label = "Nächstes Beispiel ($ereignisPositionText)",
                                aktiv = false,
                                onClick = onNaechstesEreignis,
                            )
                        }
                    }

                    ArchivTrennlinie(farbe = farben.linieFein)

                    // Zeile 2: Live-Emotion / Werte-Simulation
                    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text(
                            text = "Live-Emotion & Werte testen (Befindensleiste oben antippen für Erklärkarte):",
                            style = MaterialTheme.typography.labelMedium,
                            color = farben.tinteMatt,
                        )
                        FlowRow(
                            horizontalArrangement = Arrangement.spacedBy(6.dp),
                            verticalArrangement = Arrangement.spacedBy(6.dp),
                        ) {
                            Stimmung.entries.forEach { stimmung ->
                                DemoAuswahlKnopf(
                                    label = UiStateMapper.formatStimmungBezeichnung(stimmung),
                                    aktiv = stimmung == aktiveStimmung,
                                    onClick = { onStimmungWaehlen(stimmung) },
                                )
                            }
                        }
                    }

                    ArchivTrennlinie(farbe = farben.linieFein)

                    // Zeile 3: Figur, Analysemodus & Schriftgröße
                    FlowRow(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp),
                        itemVerticalAlignment = Alignment.CenterVertically,
                    ) {
                        DemoAuswahlKnopf(
                            label = "Herkunft: $herkunftTitel",
                            aktiv = false,
                            onClick = onHerkunftWechseln,
                        )
                        DemoAuswahlKnopf(
                            label = "Figur: ${if (geschlecht == Geschlecht.MAENNLICH) "männlich" else "weiblich"}",
                            aktiv = false,
                            onClick = onGeschlechtWechseln,
                        )
                        DemoAuswahlKnopf(
                            label = if (analyseModus) "Analysemodus: Ein" else "Analysemodus: Aus",
                            aktiv = analyseModus,
                            onClick = onAnalyseModusToggle,
                        )
                        SchriftgroessenSchalter(
                            aktuell = schriftgroesse,
                            onAuswahl = onSchriftgroesseChange,
                            aufDunkel = false,
                            kompakt = false,
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun DemoAuswahlKnopf(
    label: String,
    aktiv: Boolean,
    onClick: () -> Unit,
) {
    val farben = ArchivTheme.farben
    Surface(
        modifier = Modifier
            .defaultMinSize(minHeight = 40.dp)
            .clip(RoundedCornerShape(3.dp))
            .clickable(onClick = onClick)
            .semantics {
                role = Role.Button
                selected = aktiv
            },
        color = if (aktiv) farben.tinte else farben.papier,
        shape = RoundedCornerShape(3.dp),
        border = BorderStroke(1.dp, if (aktiv) farben.tinte else farben.linie),
    ) {
        Box(
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
            contentAlignment = Alignment.Center,
        ) {
            Text(
                text = label,
                style = MaterialTheme.typography.labelMedium,
                color = if (aktiv) farben.papierHell else farben.tinte,
                fontWeight = if (aktiv) FontWeight.SemiBold else FontWeight.Normal,
            )
        }
    }
}

@Composable
private fun ZustandsNotiz(
    zustandssatz: String,
    portraitId: String,
    analyseModus: Boolean,
) {
    val farben = ArchivTheme.farben
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .border(1.dp, farben.linieFein, RoundedCornerShape(3.dp))
            .background(farben.papierHell.copy(alpha = 0.72f), RoundedCornerShape(3.dp))
            .padding(12.dp),
        verticalArrangement = Arrangement.spacedBy(4.dp),
    ) {
        Text(
            text = "Aktueller Zustandssatz",
            style = MaterialTheme.typography.labelSmall,
            color = farben.tinteMatt,
            fontWeight = FontWeight.SemiBold,
        )
        Text(
            text = "„$zustandssatz“",
            style = MaterialTheme.typography.bodyMedium,
            fontStyle = FontStyle.Italic,
            color = farben.tinte,
        )
        if (analyseModus) {
            Text(
                text = "Aktives Portrait-Asset: $portraitId",
                style = MaterialTheme.typography.labelSmall,
                color = farben.akzent,
            )
        }
    }
}
