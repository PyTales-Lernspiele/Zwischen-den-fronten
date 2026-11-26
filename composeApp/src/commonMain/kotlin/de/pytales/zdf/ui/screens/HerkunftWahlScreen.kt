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
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.clearAndSetSemantics
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.Herkunft
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.ui.components.ArchivTrennlinie
import de.pytales.zdf.ui.components.HakenIcon
import de.pytales.zdf.ui.components.archivFokusGruppe
import de.pytales.zdf.ui.components.archivFokusRahmen
import de.pytales.zdf.ui.components.archivLiveHinweis
import de.pytales.zdf.ui.components.archivPapierHintergrund
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.media.ArchivPortraitBild
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.theme.ArchivTheme

/**
 * Gestraffter 2–3-Klick-Einstieg (`GamePhase.HerkunftWahl`) im ruhigen Querformat-Layout:
 * - Links: die 4 sozialen Herkünfte als luftiges 2×2-Raster
 * - Rechts: Geschlecht, Jahrgang, (optional) Unterrichts-Direktwahl sowie Vorschau-Portrait
 *   und Bestätigung zum Start in den August 1914.
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
    onAudioToggle: () -> Unit,
    onEinstellungenOeffnen: () -> Unit,
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
    val kompakt = metrik.kompakteHoehe
    val querformat = metrik.zweispaltigeBuehne
    val startJahr = content.kapitel.kapitel.first().jahr

    val herkunftBlock: @Composable (Modifier) -> Unit = { mod ->
        Column(
            modifier = mod,
            verticalArrangement = Arrangement.spacedBy(if (kompakt) 8.dp else 10.dp),
        ) {
            Text(
                text = "Soziale Herkunft",
                style = MaterialTheme.typography.titleLarge,
                color = farben.tinte,
                modifier = Modifier.archivUeberschrift(),
            )

            herkuenfte.chunked(2).forEach { paar ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(IntrinsicSize.Min),
                    horizontalArrangement = Arrangement.spacedBy(if (kompakt) 8.dp else 10.dp),
                ) {
                    paar.forEach { herkunft ->
                        HerkunftKarte(
                            herkunft = herkunft,
                            ausgewaehlt = entwurf.herkunftId == herkunft.id,
                            kompakt = kompakt,
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
        }
    }

    val figurUndStartBlock: @Composable (Modifier) -> Unit = { mod ->
        Column(
            modifier = mod,
            verticalArrangement = Arrangement.spacedBy(if (kompakt) 10.dp else 14.dp),
        ) {
            // Geschlecht
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text(
                    text = "Geschlecht",
                    style = MaterialTheme.typography.titleMedium,
                    fontFamily = FontFamily.Serif,
                    color = farben.tinte,
                    modifier = Modifier.archivUeberschrift(),
                )
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(IntrinsicSize.Min),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    AuswahlKachel(
                        titel = "Männlich",
                        untertitel = "Wehrpflichtig 1914",
                        ausgewaehlt = entwurf.geschlecht == Geschlecht.MAENNLICH,
                        onClick = { onGeschlechtWaehlen(Geschlecht.MAENNLICH) },
                        modifier = Modifier
                            .weight(1f)
                            .fillMaxHeight(),
                    )
                    AuswahlKachel(
                        titel = "Weiblich",
                        untertitel = "Heimat oder Lazarett",
                        ausgewaehlt = entwurf.geschlecht == Geschlecht.WEIBLICH,
                        onClick = { onGeschlechtWaehlen(Geschlecht.WEIBLICH) },
                        modifier = Modifier
                            .weight(1f)
                            .fillMaxHeight(),
                    )
                }
            }

            // Jahrgang
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text(
                    text = "Alter im August $startJahr",
                    style = MaterialTheme.typography.titleMedium,
                    fontFamily = FontFamily.Serif,
                    color = farben.tinte,
                    modifier = Modifier.archivUeberschrift(),
                )
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(IntrinsicSize.Min),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    jahrgaenge.forEach { option ->
                        val jahrgang = startJahr - option.alter
                        val klasseHinweis = if (entwurf.geschlecht == Geschlecht.MAENNLICH) {
                            engine.altersgruppe(option.alter).second
                        } else {
                            option.marke
                        }
                        AuswahlKachel(
                            titel = "${option.alter} Jahre (Jg. $jahrgang)",
                            untertitel = klasseHinweis,
                            ausgewaehlt = entwurf.alter == option.alter,
                            onClick = { onAlterWaehlen(option.alter) },
                            modifier = Modifier
                                .weight(1f)
                                .fillMaxHeight(),
                        )
                    }
                }
            }

            // Optional: Unterrichts-Direktwahl
            if (direktwahlAktiv) {
                Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text(
                        text = "Lebensbereich (Unterrichts-Direktwahl)",
                        style = MaterialTheme.typography.titleMedium,
                        fontFamily = FontFamily.Serif,
                        color = farben.akzent,
                        modifier = Modifier.archivUeberschrift(),
                    )
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(IntrinsicSize.Min),
                        horizontalArrangement = Arrangement.spacedBy(6.dp),
                    ) {
                        content.konfiguration.pfade.reihenfolge.forEach { pfad ->
                            val pfadDef = content.konfiguration.pfade.definitionen.getValue(pfad)
                            AuswahlKachel(
                                titel = pfadDef.marke.removePrefix("An der ").removePrefix("In der "),
                                untertitel = pfadKurzHinweis(pfad),
                                ausgewaehlt = entwurf.direktwahlPfad == pfad,
                                onClick = { onDirektPfadWaehlen(pfad) },
                                modifier = Modifier
                                    .weight(1f)
                                    .fillMaxHeight(),
                            )
                        }
                    }
                }
            }

            // Ruhige Zusammenfassung mit Stil-A-Portraitvorschau & Start-Button
            Surface(
                modifier = Modifier.fillMaxWidth(),
                color = farben.papierHell,
                shape = RoundedCornerShape(6.dp),
                border = BorderStroke(0.75.dp, if (vollstaendig) farben.akzent.copy(alpha = 0.6f) else farben.linieFein),
                shadowElevation = 1.dp,
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(if (kompakt) 12.dp else 14.dp),
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

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        if (entwurf.herkunftId != null && entwurf.geschlecht != null) {
                            val vorschauId = "portrait_${entwurf.herkunftId}_${entwurf.geschlecht.code}_neutral"
                            Box(
                                modifier = Modifier
                                    .size(48.dp)
                                    .clip(RoundedCornerShape(4.dp))
                                    .background(farben.papier),
                            ) {
                                ArchivPortraitBild(
                                    portraitId = vorschauId,
                                    stimmungsFarbe = farben.stufenFarbe(0),
                                    beschreibung = "Vorschau-Portrait der gewählten Figur",
                                ) {}
                            }
                        }

                        Text(
                            text = zusammenfassung,
                            style = MaterialTheme.typography.bodySmall,
                            color = if (vollstaendig) farben.tinte else farben.tinteMatt,
                            fontWeight = if (vollstaendig) FontWeight.Medium else FontWeight.Normal,
                            modifier = Modifier
                                .weight(1f)
                                .archivLiveHinweis(),
                        )
                    }

                    ArchivPrimaerKnopf(
                        label = "In den August $startJahr starten",
                        akzentStil = true,
                        aktiviert = vollstaendig,
                        onClick = onBestaetigen,
                        modifier = Modifier.fillMaxWidth(),
                    )
                }
            }
        }
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .archivPapierHintergrund(),
    ) {
        ArchivKopfBand(
            marke = "August $startJahr",
            titel = "Wer bist du zu Beginn des Krieges?",
            untertitel = if (direktwahlAktiv) "Direktwahl aktiv" else "Ausgangslage wählen",
            audioZustand = uiState.audioZustand,
            onAudioToggle = onAudioToggle,
            onEinstellungenOeffnen = onEinstellungenOeffnen,
        )

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .verticalScroll(rememberScrollState()),
            contentAlignment = Alignment.TopCenter,
        ) {
            if (querformat) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .archivInhaltsSafeArea()
                        .widthIn(max = metrik.maxInhaltsBreite)
                        .padding(
                            horizontal = metrik.aussenAbstand,
                            vertical = if (kompakt) 10.dp else 16.dp,
                        )
                        .archivFokusGruppe(),
                    horizontalArrangement = Arrangement.spacedBy(if (kompakt) 14.dp else 22.dp),
                    verticalAlignment = Alignment.Top,
                ) {
                    herkunftBlock(Modifier.weight(0.55f))
                    figurUndStartBlock(Modifier.weight(0.45f))
                }
            } else {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .archivInhaltsSafeArea()
                        .widthIn(max = metrik.maxInhaltsBreite)
                        .padding(horizontal = metrik.aussenAbstand, vertical = 14.dp)
                        .archivFokusGruppe(),
                    verticalArrangement = Arrangement.spacedBy(16.dp),
                ) {
                    herkunftBlock(Modifier.fillMaxWidth())
                    ArchivTrennlinie()
                    figurUndStartBlock(Modifier.fillMaxWidth())
                    Spacer(modifier = Modifier.height(12.dp))
                }
            }
        }
    }
}

@Composable
private fun HerkunftKarte(
    herkunft: Herkunft,
    ausgewaehlt: Boolean,
    kompakt: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val flaeche = if (ausgewaehlt) farben.papierHell else farben.papierHell.copy(alpha = 0.68f)
    val rahmen = if (ausgewaehlt) farben.akzent else farben.linieFein.copy(alpha = 0.85f)

    Surface(
        modifier = modifier
            .defaultMinSize(minHeight = if (kompakt) 104.dp else 128.dp)
            .clip(RoundedCornerShape(6.dp))
            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = false)
            .clickable(onClick = onClick)
            .clearAndSetSemantics {
                role = Role.RadioButton
                selected = ausgewaehlt
                stateDescription = if (ausgewaehlt) "Ausgewählt" else "Nicht ausgewählt"
                contentDescription = "${herkunft.titel}: ${herkunft.zusatz}. ${herkunft.folge}"
            },
        color = flaeche,
        shape = RoundedCornerShape(6.dp),
        border = BorderStroke(if (ausgewaehlt) 1.4.dp else 0.75.dp, rahmen),
        shadowElevation = if (ausgewaehlt) 2.dp else 0.dp,
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .height(IntrinsicSize.Min),
        ) {
            Box(
                modifier = Modifier
                    .width(if (ausgewaehlt) 3.dp else 0.dp)
                    .fillMaxHeight()
                    .background(if (ausgewaehlt) farben.akzent else Color.Transparent),
            )
            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(horizontal = if (kompakt) 11.dp else 14.dp, vertical = if (kompakt) 9.dp else 12.dp),
                verticalArrangement = Arrangement.spacedBy(if (kompakt) 4.dp else 6.dp),
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text(
                        text = herkunft.titel,
                        style = MaterialTheme.typography.titleMedium,
                        fontFamily = FontFamily.Serif,
                        color = farben.tinte,
                        fontWeight = FontWeight.Bold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.weight(1f),
                    )
                    if (ausgewaehlt) {
                        HakenIcon(farbe = farben.akzent, groesse = 15.dp)
                    }
                }

                Text(
                    text = herkunft.zusatz,
                    style = MaterialTheme.typography.labelSmall,
                    color = farben.akzent,
                )

                Text(
                    text = herkunft.text,
                    style = MaterialTheme.typography.bodySmall,
                    color = farben.tinte,
                )

                if (!kompakt) {
                    Text(
                        text = herkunft.folge,
                        style = MaterialTheme.typography.bodySmall,
                        fontFamily = FontFamily.Serif,
                        fontStyle = FontStyle.Italic,
                        color = farben.tinteMatt,
                    )
                }
            }
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
    val flaeche = if (ausgewaehlt) farben.papierHell else farben.papierHell.copy(alpha = 0.62f)
    val rahmen = if (ausgewaehlt) farben.akzent else farben.linieFein.copy(alpha = 0.85f)

    Surface(
        modifier = modifier
            .defaultMinSize(minHeight = metrik.minTouchHoehe + 8.dp)
            .clip(RoundedCornerShape(6.dp))
            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = false)
            .clickable(onClick = onClick)
            .clearAndSetSemantics {
                role = Role.RadioButton
                selected = ausgewaehlt
                stateDescription = if (ausgewaehlt) "Ausgewählt" else "Nicht ausgewählt"
                contentDescription = "$titel: $untertitel"
            },
        color = flaeche,
        shape = RoundedCornerShape(6.dp),
        border = BorderStroke(if (ausgewaehlt) 1.4.dp else 0.75.dp, rahmen),
        shadowElevation = if (ausgewaehlt) 1.dp else 0.dp,
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 11.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(2.dp),
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
                    fontWeight = if (ausgewaehlt) FontWeight.Bold else FontWeight.SemiBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f),
                )
                if (ausgewaehlt) {
                    HakenIcon(farbe = farben.akzent, groesse = 14.dp)
                }
            }
            Text(
                text = untertitel,
                style = MaterialTheme.typography.labelSmall,
                color = farben.tinteMatt,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
            )
        }
    }
}

private fun pfadKurzHinweis(pfad: Pfad): String = when (pfad) {
    Pfad.FRONT -> "Graben & Marsch"
    Pfad.ETAPPE -> "Lazarett & Dienst"
    Pfad.HEIMAT -> "Alltag im Reich"
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
    if (alter == null) offen += "Alter"
    if (direktwahlAktiv && direktwahlPfad == null) offen += "Lebensbereich"

    if (offen.isNotEmpty()) {
        return "Noch wählen: ${offen.joinToString(", ")}."
    }

    val herkunftTitel = content.herkunftById[herkunftId]?.titel.orEmpty()
    val geschlechtText = if (geschlecht == Geschlecht.MAENNLICH) "männlich" else "weiblich"
    val startJahr = content.kapitel.kapitel.first().jahr
    val jahrgang = startJahr - requireNotNull(alter)
    val teile = mutableListOf(herkunftTitel, geschlechtText, "$alter Jahre (Jg. $jahrgang)")
    if (direktwahlAktiv && direktwahlPfad != null) {
        val pfadMarke = content.konfiguration.pfade.definitionen[direktwahlPfad]?.marke ?: direktwahlPfad.code
        teile += pfadMarke
    }
    return teile.joinToString(" · ")
}
