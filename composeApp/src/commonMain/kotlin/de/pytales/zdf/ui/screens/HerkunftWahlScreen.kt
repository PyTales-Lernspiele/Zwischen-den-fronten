package de.pytales.zdf.ui.screens

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxHeight
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
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.clearAndSetSemantics
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.Herkunft
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.ui.components.ArchivStempel
import de.pytales.zdf.ui.components.ArchivTrennlinie
import de.pytales.zdf.ui.components.archivFokusGruppe
import de.pytales.zdf.ui.components.archivFokusRahmen
import de.pytales.zdf.ui.components.archivLiveHinweis
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.LayoutKlasse
import de.pytales.zdf.ui.theme.Schriftgroesse

/**
 * Gestraffter 2–3-Klick-Einstieg (`GamePhase.HerkunftWahl`):
 * - 1. Soziale Herkunft (4 Milieus mit `zusatz`, `text`, `folge`)
 * - 2. Geschlecht (`m`/`w`) und Jahrgang (`18` / `35`)
 * - 3. Optional bei aktivem Unterrichts-Schalter: direkte Pfadwahl (`front` / `etappe` / `heimat`).
 */
@Composable
fun HerkunftWahlScreen(
    engine: GameEngine,
    uiState: SpielUiState,
    onHerkunftWaehlen: (String) -> Unit,
    onGeschlechtWaehlen: (Geschlecht) -> Unit,
    onAlterWaehlen: (Int) -> Unit,
    onDirektPfadWaehlen: (Pfad) -> Unit,
    onBestaetigen: () -> Unit,
    onSchriftgroesseChange: (Schriftgroesse) -> Unit,
    onAnalyseModusToggle: () -> Unit,
    onAudioToggle: () -> Unit = {},
    modifier: Modifier = Modifier,
) {
    val content = engine.content
    val herkuenfte = content.herkunft.herkuenfte
    val jahrgaenge = content.herkunft.jahrgaenge
    val direktwahlAktiv = uiState.gameState.direktwahlAktiv
    val entwurf = uiState.herkunftEntwurf
    val vollstaendig = entwurf.istVollstaendig(direktwahlAktiv)

    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val layoutKlasse = ArchivTheme.layoutKlasse
    val zweispaltig = layoutKlasse != LayoutKlasse.KOMPAKT && uiState.schriftgroesse != Schriftgroesse.GROSS

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(farben.papier),
    ) {
        ArchivKopfBand(
            marke = "AUGUST 1914 · EINSTIEG",
            titel = "Wer bist du zu Beginn des Krieges?",
            untertitel = if (direktwahlAktiv) {
                "Unterrichts-Direktwahl aktiv: Herkunft, Figur und Pfad festlegen"
            } else {
                "Wähle Herkunft, Geschlecht und Jahrgang — danach beginnt der August 1914."
            },
            schriftgroesse = uiState.schriftgroesse,
            onSchriftgroesseChange = onSchriftgroesseChange,
            analyseModus = uiState.analyseModus,
            onAnalyseModusToggle = onAnalyseModusToggle,
            audioZustand = uiState.audioZustand,
            onAudioToggle = onAudioToggle,
        )

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
                    .archivInhaltsSafeArea()
                    .widthIn(max = metrik.maxInhaltsBreite)
                    .padding(horizontal = metrik.aussenAbstand, vertical = metrik.elementAbstand)
                    .archivFokusGruppe(),
                verticalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
            ) {
                // Schritt 1: Soziale Herkunft (4 Milieus)
                AbschnittBlatt(
                    schrittMarke = "SCHRITT 1",
                    titel = "Soziale Herkunft",
                    untertitel = "Wo du aufgewachsen bist, prägt Vorräte, Nachbarschaft und den Blick der Behörden.",
                ) {
                    if (zweispaltig) {
                        herkuenfte.chunked(2).forEach { paar ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(IntrinsicSize.Min),
                                horizontalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
                            ) {
                                paar.forEach { herkunft ->
                                    HerkunftKarte(
                                        herkunft = herkunft,
                                        ausgewaehlt = entwurf.herkunftId == herkunft.id,
                                        onClick = { onHerkunftWaehlen(herkunft.id) },
                                        modifier = Modifier
                                            .weight(1f)
                                            .fillMaxHeight(),
                                    )
                                }
                                if (paar.size == 1) {
                                    Spacer(modifier = Modifier.weight(1f))
                                }
                            }
                        }
                    } else {
                        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            herkuenfte.forEach { herkunft ->
                                HerkunftKarte(
                                    herkunft = herkunft,
                                    ausgewaehlt = entwurf.herkunftId == herkunft.id,
                                    onClick = { onHerkunftWaehlen(herkunft.id) },
                                    modifier = Modifier.fillMaxWidth(),
                                )
                            }
                        }
                    }
                }

                // Schritt 2: Geschlecht & Jahrgang
                AbschnittBlatt(
                    schrittMarke = "SCHRITT 2",
                    titel = "Geschlecht & Jahrgang",
                    untertitel = "Entscheidet über Wehrpflicht, Musterung und deine Rolle in Familie und Beruf.",
                ) {
                    val gruppenNebeneinander = layoutKlasse == LayoutKlasse.BREIT

                    val geschlechtBlock: @Composable (Modifier) -> Unit = { mod ->
                        Column(
                            modifier = mod,
                            verticalArrangement = Arrangement.spacedBy(8.dp),
                        ) {
                            Text(
                                text = "Geschlecht",
                                style = MaterialTheme.typography.titleSmall,
                                color = farben.tinte,
                            )
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(IntrinsicSize.Min),
                                horizontalArrangement = Arrangement.spacedBy(10.dp),
                            ) {
                                AuswahlKachel(
                                    titel = "Männlich",
                                    untertitel = "1914 wehrpflichtig (17–45 Jahre)",
                                    ausgewaehlt = entwurf.geschlecht == Geschlecht.MAENNLICH,
                                    onClick = { onGeschlechtWaehlen(Geschlecht.MAENNLICH) },
                                    modifier = Modifier
                                        .weight(1f)
                                        .fillMaxHeight(),
                                )
                                AuswahlKachel(
                                    titel = "Weiblich",
                                    untertitel = "Alltag in Heimat oder Lazarett",
                                    ausgewaehlt = entwurf.geschlecht == Geschlecht.WEIBLICH,
                                    onClick = { onGeschlechtWaehlen(Geschlecht.WEIBLICH) },
                                    modifier = Modifier
                                        .weight(1f)
                                        .fillMaxHeight(),
                                )
                            }
                        }
                    }

                    val jahrgangBlock: @Composable (Modifier) -> Unit = { mod ->
                        val startJahr = content.kapitel.kapitel.first().jahr
                        Column(
                            modifier = mod,
                            verticalArrangement = Arrangement.spacedBy(8.dp),
                        ) {
                            Text(
                                text = "Jahrgang im August $startJahr",
                                style = MaterialTheme.typography.titleSmall,
                                color = farben.tinte,
                            )
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(IntrinsicSize.Min),
                                horizontalArrangement = Arrangement.spacedBy(10.dp),
                            ) {
                                jahrgaenge.forEach { option ->
                                    val jahrgang = startJahr - option.alter
                                    val klasseHinweis = if (entwurf.geschlecht == Geschlecht.MAENNLICH) {
                                        " · ${engine.altersgruppe(option.alter).second}"
                                    } else {
                                        ""
                                    }
                                    AuswahlKachel(
                                        titel = "${option.alter} Jahre (Jg. $jahrgang)",
                                        untertitel = "${option.marke}$klasseHinweis",
                                        ausgewaehlt = entwurf.alter == option.alter,
                                        onClick = { onAlterWaehlen(option.alter) },
                                        modifier = Modifier
                                            .weight(1f)
                                            .fillMaxHeight(),
                                    )
                                }
                            }
                        }
                    }

                    if (gruppenNebeneinander) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
                            verticalAlignment = Alignment.Top,
                        ) {
                            geschlechtBlock(Modifier.weight(1f))
                            jahrgangBlock(Modifier.weight(1f))
                        }
                    } else {
                        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
                            geschlechtBlock(Modifier.fillMaxWidth())
                            jahrgangBlock(Modifier.fillMaxWidth())
                        }
                    }
                }

                // Schritt 3 (optional): Pfad direkt wählen im Unterrichts-Modus
                if (direktwahlAktiv) {
                    AbschnittBlatt(
                        schrittMarke = "SCHRITT 3 · UNTERRICHT",
                        titel = "Pfad direkt wählen",
                        untertitel = "Die Musterung wird übersprungen. Alle drei historischen Lebensbereiche sind sofort zugänglich.",
                    ) {
                        val pfade = content.konfiguration.pfade.reihenfolge
                        val pfadNebeneinander = layoutKlasse != LayoutKlasse.KOMPAKT

                        if (pfadNebeneinander) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(IntrinsicSize.Min),
                                horizontalArrangement = Arrangement.spacedBy(10.dp),
                            ) {
                                pfade.forEach { pfad ->
                                    val pfadDef = content.konfiguration.pfade.definitionen.getValue(pfad)
                                    AuswahlKachel(
                                        titel = pfadDef.marke,
                                        untertitel = "${pfadDef.ort} — ${pfadKurzbeschreibung(pfad)}",
                                        ausgewaehlt = entwurf.direktwahlPfad == pfad,
                                        onClick = { onDirektPfadWaehlen(pfad) },
                                        modifier = Modifier
                                            .weight(1f)
                                            .fillMaxHeight(),
                                    )
                                }
                            }
                        } else {
                            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                                pfade.forEach { pfad ->
                                    val pfadDef = content.konfiguration.pfade.definitionen.getValue(pfad)
                                    AuswahlKachel(
                                        titel = pfadDef.marke,
                                        untertitel = "${pfadDef.ort} — ${pfadKurzbeschreibung(pfad)}",
                                        ausgewaehlt = entwurf.direktwahlPfad == pfad,
                                        onClick = { onDirektPfadWaehlen(pfad) },
                                        modifier = Modifier.fillMaxWidth(),
                                    )
                                }
                            }
                        }
                    }
                }

                // Abschluss-Bestätigung (kein Zurück!)
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = farben.papierHell,
                    shape = RoundedCornerShape(4.dp),
                    border = BorderStroke(1.25.dp, if (vollstaendig) farben.tinte else farben.linie),
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(metrik.kartenInnenAbstand),
                        verticalArrangement = Arrangement.spacedBy(10.dp),
                    ) {
                        val zusammenfassung = baueAuswahlZusammenfassung(
                            content = content,
                            herkunftId = entwurf.herkunftId,
                            geschlecht = entwurf.geschlecht,
                            alter = entwurf.alter,
                            direktwahlAktiv = direktwahlAktiv,
                            direktwahlPfad = entwurf.direktwahlPfad,
                        )
                        Text(
                            text = if (vollstaendig) {
                                "Deine Ausgangslage: $zusammenfassung"
                            } else {
                                "Noch offen: $zusammenfassung"
                            },
                            style = MaterialTheme.typography.bodyMedium,
                            color = if (vollstaendig) farben.tinte else farben.tinteMatt,
                            fontWeight = if (vollstaendig) FontWeight.SemiBold else FontWeight.Normal,
                            modifier = Modifier.archivLiveHinweis(),
                        )

                        ArchivPrimaerKnopf(
                            label = if (direktwahlAktiv) {
                                "Mit dieser Ausgangslage in 1914 starten"
                            } else {
                                "In den August 1914 starten"
                            },
                            aktiviert = vollstaendig,
                            onClick = onBestaetigen,
                            modifier = if (layoutKlasse == LayoutKlasse.KOMPAKT) {
                                Modifier.fillMaxWidth()
                            } else {
                                Modifier
                            },
                        )
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
}

@Composable
private fun AbschnittBlatt(
    schrittMarke: String,
    titel: String,
    untertitel: String,
    content: @Composable () -> Unit,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik

    Surface(
        modifier = Modifier.fillMaxWidth(),
        color = farben.papierHell,
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(1.dp, farben.linie),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(metrik.kartenInnenAbstand),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                ArchivStempel(
                    text = schrittMarke,
                    farbe = farben.akzent,
                )
                Text(
                    text = titel,
                    style = MaterialTheme.typography.headlineSmall,
                    color = farben.tinte,
                    modifier = Modifier.archivUeberschrift(),
                )
                Text(
                    text = untertitel,
                    style = MaterialTheme.typography.bodySmall,
                    color = farben.tinteMatt,
                )
            }
            content()
        }
    }
}

@Composable
private fun HerkunftKarte(
    herkunft: Herkunft,
    ausgewaehlt: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val flaeche = if (ausgewaehlt) farben.papierDunkel else farben.papier
    val rahmen = if (ausgewaehlt) farben.akzent else farben.linie

    Surface(
        modifier = modifier
            .defaultMinSize(minHeight = 140.dp)
            .clip(RoundedCornerShape(4.dp))
            .archivFokusRahmen(eckRadius = 4.dp, aufDunkel = false)
            .clickable(onClick = onClick)
            .clearAndSetSemantics {
                role = Role.RadioButton
                selected = ausgewaehlt
                stateDescription = if (ausgewaehlt) "Ausgewählt" else "Nicht ausgewählt"
                contentDescription = "${herkunft.titel}: ${herkunft.zusatz}. ${herkunft.folge}"
            },
        color = flaeche,
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(if (ausgewaehlt) 2.dp else 1.dp, rahmen),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = herkunft.titel,
                        style = MaterialTheme.typography.titleLarge,
                        color = farben.tinte,
                    )
                    Text(
                        text = herkunft.zusatz,
                        style = MaterialTheme.typography.bodySmall,
                        color = farben.tinteMatt,
                    )
                }
                if (ausgewaehlt) {
                    ArchivStempel(
                        text = "GEWÄHLT",
                        farbe = farben.akzent,
                        hintergrund = farben.papierHell,
                    )
                }
            }

            Text(
                text = herkunft.text,
                style = MaterialTheme.typography.bodyMedium,
                color = farben.tinte,
            )

            ArchivTrennlinie(farbe = farben.linieFein)

            Text(
                text = herkunft.folge,
                style = MaterialTheme.typography.bodySmall,
                fontStyle = FontStyle.Italic,
                color = farben.tinteMatt,
            )
        }
    }
}

@Composable
private fun AuswahlKachel(
    titel: String,
    untertitel: String,
    ausgewaehlt: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val flaeche = if (ausgewaehlt) farben.papierDunkel else farben.papier
    val rahmen = if (ausgewaehlt) farben.akzent else farben.linie

    Surface(
        modifier = modifier
            .defaultMinSize(minHeight = metrik.minTouchHoehe + 20.dp)
            .clip(RoundedCornerShape(4.dp))
            .archivFokusRahmen(eckRadius = 4.dp, aufDunkel = false)
            .clickable(onClick = onClick)
            .clearAndSetSemantics {
                role = Role.RadioButton
                selected = ausgewaehlt
                stateDescription = if (ausgewaehlt) "Ausgewählt" else "Nicht ausgewählt"
                contentDescription = "$titel: $untertitel"
            },
        color = flaeche,
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(if (ausgewaehlt) 2.dp else 1.dp, rahmen),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 12.dp, vertical = 10.dp),
            verticalArrangement = Arrangement.spacedBy(4.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = titel,
                    style = MaterialTheme.typography.titleSmall,
                    color = farben.tinte,
                    fontWeight = FontWeight.SemiBold,
                    modifier = Modifier.weight(1f),
                )
                if (ausgewaehlt) {
                    ArchivStempel(
                        text = "✓",
                        farbe = farben.akzent,
                    )
                }
            }
            Text(
                text = untertitel,
                style = MaterialTheme.typography.bodySmall,
                color = farben.tinteMatt,
            )
        }
    }
}

private fun pfadKurzbeschreibung(pfad: Pfad): String = when (pfad) {
    Pfad.FRONT -> "Stellungskrieg, Marsch und Grabenalltag"
    Pfad.ETAPPE -> "Lazarett, Schreibstube und Nachschub hinter der Front"
    Pfad.HEIMAT -> "Erwerb, Versorgung, Familie und Alltag im Reich"
}

private fun baueAuswahlZusammenfassung(
    content: de.pytales.zdf.content.GameContent,
    herkunftId: String?,
    geschlecht: Geschlecht?,
    alter: Int?,
    direktwahlAktiv: Boolean,
    direktwahlPfad: Pfad?,
): String {
    val offen = mutableListOf<String>()
    if (herkunftId == null) offen += "Herkunft"
    if (geschlecht == null) offen += "Geschlecht"
    if (alter == null) offen += "Jahrgang"
    if (direktwahlAktiv && direktwahlPfad == null) offen += "Pfad"

    if (offen.isNotEmpty()) {
        return "Bitte noch ${offen.joinToString(", ")} auswählen."
    }

    val herkunftTitel = content.herkunftById[herkunftId]?.titel.orEmpty()
    val geschlechtText = if (geschlecht == Geschlecht.MAENNLICH) "männlich" else "weiblich"
    val startJahr = content.kapitel.kapitel.first().jahr
    val jahrgang = startJahr - requireNotNull(alter)
    val teile = mutableListOf(herkunftTitel, geschlechtText, "$alter Jahre (Jahrgang $jahrgang)")
    if (direktwahlAktiv && direktwahlPfad != null) {
        val pfadMarke = content.konfiguration.pfade.definitionen[direktwahlPfad]?.marke ?: direktwahlPfad.code
        teile += pfadMarke
    }
    return teile.joinToString(" · ")
}
