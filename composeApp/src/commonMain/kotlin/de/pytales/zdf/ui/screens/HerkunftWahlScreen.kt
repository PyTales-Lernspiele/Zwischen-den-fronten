package de.pytales.zdf.ui.screens

import androidx.compose.animation.AnimatedContent
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import de.pytales.zdf.audio.SoundEffekt
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.Herkunft
import de.pytales.zdf.model.Pfad
import de.pytales.zdf.ui.components.HakenIcon
import de.pytales.zdf.ui.components.archivFokusGruppe
import de.pytales.zdf.ui.components.archivFokusRahmen
import de.pytales.zdf.ui.components.archivPapierHintergrund
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.media.ArchivPortraitBild
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.ArchivUebergaenge
import de.pytales.zdf.ui.theme.LocalSoundEffektSpielen

/**
 * Ruhiger, zweistufiger Einstieg vor Spielbeginn (`GamePhase.HerkunftWahl`):
 * - **Schritt 1:** Nur die 4 sozialen Herkünfte klar, großzügig und mit knapper Typografie auswählen.
 * - **Schritt 2:** Geschlecht + Jahrgang (und optional Direktwahl-Pfad) neben dem großen
 *   Live-Stil-A-Portrait der gewählten Figur + klarer Start-Button „In den August 1914“.
 * - Innerhalb der Figuren-Erstellung vor Spielbeginn ist der freie Wechsel zwischen Schritt 1
 *   und 2 jederzeit erlaubt; ab Bestätigung gilt strikt „Kein Zurück“.
 */
@Composable
fun HerkunftWahlScreen(
    engine: GameEngine,
    uiState: SpielUiState,
    onHerkunftWaehlen: (String) -> Unit,
    onSchrittWechseln: (Int) -> Unit,
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
    val schritt = if (entwurf.schritt == 2 && entwurf.herkunftId != null) 2 else 1
    val gewaehlteHerkunft = entwurf.herkunftId?.let { content.herkunftById[it] }
    val vollstaendig = entwurf.istVollstaendig(direktwahlAktiv)

    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val reduziert = ArchivTheme.reduzierteAnimationen
    val kompakt = metrik.kompakteHoehe
    val querformat = metrik.zweispaltigeBuehne
    val spieleEffekt = LocalSoundEffektSpielen.current
    val startJahr = content.kapitel.kapitel.first().jahr

    Column(
        modifier = modifier
            .fillMaxSize()
            .archivPapierHintergrund(),
    ) {
        // Ultra-schlankes Kopfband mit ruhigem 2-Schritt-Anzeiger
        ArchivKopfBand(
            marke = "August $startJahr",
            audioZustand = uiState.audioZustand,
            onAudioToggle = onAudioToggle,
            onEinstellungenOeffnen = onEinstellungenOeffnen,
            linksZusatz = {
                Row(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    SchrittAnzeigerChip(
                        nummer = 1,
                        label = "Herkunft",
                        aktiv = schritt == 1,
                        klickbar = schritt != 1,
                        onClick = {
                            spieleEffekt(SoundEffekt.KLICK_SANFT)
                            onSchrittWechseln(1)
                        },
                    )
                    Text(
                        text = "—",
                        style = MaterialTheme.typography.labelMedium,
                        color = farben.textHell.copy(alpha = 0.42f),
                    )
                    SchrittAnzeigerChip(
                        nummer = 2,
                        label = "Figur",
                        aktiv = schritt == 2,
                        klickbar = schritt != 2 && entwurf.kannZuSchrittZwei,
                        onClick = {
                            spieleEffekt(SoundEffekt.KLICK_SANFT)
                            onSchrittWechseln(2)
                        },
                    )
                }
            },
        )

        AnimatedContent(
            targetState = schritt,
            transitionSpec = { ArchivUebergaenge.phasenTransitionSpec(reduziert) },
            label = "herkunftSchrittWechsel",
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f),
        ) { aktiverSchritt ->
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState()),
                contentAlignment = Alignment.Center,
            ) {
                if (aktiverSchritt == 1) {
                    // ---------------------------------------------------------
                    // SCHRITT 1: Nur die 4 sozialen Herkünfte — großzügig & ruhig
                    // ---------------------------------------------------------
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .archivInhaltsSafeArea()
                            .widthIn(max = 920.dp)
                            .padding(
                                horizontal = metrik.aussenAbstand,
                                vertical = if (kompakt) 12.dp else 22.dp,
                            )
                            .archivFokusGruppe(),
                        verticalArrangement = Arrangement.spacedBy(if (kompakt) 12.dp else 18.dp),
                    ) {
                        Text(
                            text = "Aus welchem Haus stammst du?",
                            style = if (kompakt) MaterialTheme.typography.headlineSmall else MaterialTheme.typography.headlineMedium,
                            color = farben.tinte,
                            modifier = Modifier.archivUeberschrift(),
                        )

                        if (querformat) {
                            herkuenfte.chunked(2).forEach { paar ->
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(IntrinsicSize.Min),
                                    horizontalArrangement = Arrangement.spacedBy(if (kompakt) 12.dp else 16.dp),
                                ) {
                                    paar.forEach { herkunft ->
                                        HerkunftKarte(
                                            herkunft = herkunft,
                                            ausgewaehlt = entwurf.herkunftId == herkunft.id,
                                            kompakt = kompakt,
                                            onClick = {
                                                spieleEffekt(SoundEffekt.KLICK_SANFT)
                                                onHerkunftWaehlen(herkunft.id)
                                            },
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
                                        kompakt = kompakt,
                                        onClick = {
                                            spieleEffekt(SoundEffekt.KLICK_SANFT)
                                            onHerkunftWaehlen(herkunft.id)
                                        },
                                        modifier = Modifier.fillMaxWidth(),
                                    )
                                }
                            }
                        }

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.End,
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            ArchivPrimaerKnopf(
                                label = "Weiter",
                                akzentStil = true,
                                aktiviert = entwurf.kannZuSchrittZwei,
                                onClick = { onSchrittWechseln(2) },
                            )
                        }
                    }
                } else {
                    // ---------------------------------------------------------
                    // SCHRITT 2: Live-Stil-A-Portrait + Geschlecht & Jahrgang
                    // ---------------------------------------------------------
                    val portraitBlock: @Composable (Modifier) -> Unit = { mod ->
                        Column(
                            modifier = mod,
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.spacedBy(if (kompakt) 8.dp else 12.dp),
                        ) {
                            val portraitGroesse = if (kompakt) 126.dp else 164.dp
                            val geschlechtCode = (entwurf.geschlecht ?: Geschlecht.WEIBLICH).code
                            val portraitId = "portrait_${entwurf.herkunftId ?: "arbeiterschaft"}_${geschlechtCode}_neutral"

                            Surface(
                                color = farben.papierHell,
                                shape = RoundedCornerShape(6.dp),
                                border = BorderStroke(0.75.dp, farben.linieFein.copy(alpha = 0.85f)),
                                shadowElevation = 2.dp,
                            ) {
                                Box(
                                    modifier = Modifier
                                        .padding(6.dp)
                                        .size(portraitGroesse)
                                        .clip(RoundedCornerShape(4.dp))
                                        .background(farben.papier),
                                    contentAlignment = Alignment.Center,
                                ) {
                                    ArchivPortraitBild(
                                        portraitId = portraitId,
                                        stimmungsFarbe = farben.akzent,
                                        beschreibung = "Stil-A-Portrait der gewählten Figur",
                                    ) {}
                                }
                            }

                            if (gewaehlteHerkunft != null) {
                                Text(
                                    text = gewaehlteHerkunft.titel,
                                    style = MaterialTheme.typography.titleLarge,
                                    fontFamily = FontFamily.Serif,
                                    color = farben.tinte,
                                    textAlign = TextAlign.Center,
                                )
                            }

                            ArchivTextKnopf(
                                label = "← Herkunft ändern",
                                onClick = { onSchrittWechseln(1) },
                            )
                        }
                    }

                    val auswahlBlock: @Composable (Modifier) -> Unit = { mod ->
                        Column(
                            modifier = mod,
                            verticalArrangement = Arrangement.spacedBy(if (kompakt) 12.dp else 16.dp),
                        ) {
                            // Geschlecht
                            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                                Text(
                                    text = "Geschlecht",
                                    style = MaterialTheme.typography.labelLarge,
                                    fontFamily = FontFamily.Serif,
                                    color = farben.tinteMatt,
                                )
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(IntrinsicSize.Min),
                                    horizontalArrangement = Arrangement.spacedBy(10.dp),
                                ) {
                                    AuswahlKachel(
                                        titel = "Männlich",
                                        untertitel = "Wehrpflichtig 1914",
                                        ausgewaehlt = entwurf.geschlecht == Geschlecht.MAENNLICH,
                                        onClick = {
                                            spieleEffekt(SoundEffekt.KLICK_SANFT)
                                            onGeschlechtWaehlen(Geschlecht.MAENNLICH)
                                        },
                                        modifier = Modifier
                                            .weight(1f)
                                            .fillMaxHeight(),
                                    )
                                    AuswahlKachel(
                                        titel = "Weiblich",
                                        untertitel = "Heimat oder Lazarett",
                                        ausgewaehlt = entwurf.geschlecht == Geschlecht.WEIBLICH,
                                        onClick = {
                                            spieleEffekt(SoundEffekt.KLICK_SANFT)
                                            onGeschlechtWaehlen(Geschlecht.WEIBLICH)
                                        },
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
                                    style = MaterialTheme.typography.labelLarge,
                                    fontFamily = FontFamily.Serif,
                                    color = farben.tinteMatt,
                                )
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(IntrinsicSize.Min),
                                    horizontalArrangement = Arrangement.spacedBy(10.dp),
                                ) {
                                    jahrgaenge.forEach { option ->
                                        val jahrgang = startJahr - option.alter
                                        val hinweis = if (entwurf.geschlecht == Geschlecht.MAENNLICH) {
                                            engine.altersgruppe(option.alter).second
                                        } else {
                                            option.marke
                                        }
                                        AuswahlKachel(
                                            titel = "${option.alter} Jahre (Jg. $jahrgang)",
                                            untertitel = hinweis,
                                            ausgewaehlt = entwurf.alter == option.alter,
                                            onClick = {
                                                spieleEffekt(SoundEffekt.KLICK_SANFT)
                                                onAlterWaehlen(option.alter)
                                            },
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
                                        text = "Lebensbereich (Direktwahl)",
                                        style = MaterialTheme.typography.labelLarge,
                                        fontFamily = FontFamily.Serif,
                                        color = farben.akzent,
                                    )
                                    Row(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .height(IntrinsicSize.Min),
                                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                                    ) {
                                        content.konfiguration.pfade.reihenfolge.forEach { pfad ->
                                            val pfadDef = content.konfiguration.pfade.definitionen.getValue(pfad)
                                            AuswahlKachel(
                                                titel = pfadDef.marke.removePrefix("An der ").removePrefix("In der "),
                                                untertitel = pfadKurzHinweis(pfad),
                                                ausgewaehlt = entwurf.direktwahlPfad == pfad,
                                                onClick = {
                                                    spieleEffekt(SoundEffekt.KLICK_SANFT)
                                                    onDirektPfadWaehlen(pfad)
                                                },
                                                modifier = Modifier
                                                    .weight(1f)
                                                    .fillMaxHeight(),
                                            )
                                        }
                                    }
                                }
                            }

                            Spacer(modifier = Modifier.height(2.dp))

                            ArchivPrimaerKnopf(
                                label = "In den August $startJahr",
                                akzentStil = true,
                                aktiviert = vollstaendig,
                                klickEffekt = SoundEffekt.ENTSCHEIDUNG,
                                onClick = onBestaetigen,
                                modifier = Modifier.fillMaxWidth(),
                            )
                        }
                    }

                    if (querformat) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .archivInhaltsSafeArea()
                                .widthIn(max = 920.dp)
                                .padding(
                                    horizontal = metrik.aussenAbstand,
                                    vertical = if (kompakt) 10.dp else 20.dp,
                                )
                                .archivFokusGruppe(),
                            horizontalArrangement = Arrangement.spacedBy(if (kompakt) 24.dp else 36.dp),
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            portraitBlock(Modifier.weight(0.36f))
                            auswahlBlock(Modifier.weight(0.64f))
                        }
                    } else {
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .archivInhaltsSafeArea()
                                .widthIn(max = 480.dp)
                                .padding(horizontal = metrik.aussenAbstand, vertical = 16.dp)
                                .archivFokusGruppe(),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.spacedBy(16.dp),
                        ) {
                            portraitBlock(Modifier.fillMaxWidth())
                            auswahlBlock(Modifier.fillMaxWidth())
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun SchrittAnzeigerChip(
    nummer: Int,
    label: String,
    aktiv: Boolean,
    klickbar: Boolean,
    onClick: () -> Unit,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val textFarbe = when {
        aktiv -> farben.textHell
        klickbar -> farben.textHell.copy(alpha = 0.72f)
        else -> farben.textHell.copy(alpha = 0.42f)
    }

    Box(
        modifier = Modifier
            .defaultMinSize(minHeight = metrik.minTouchHoehe)
            .clip(RoundedCornerShape(5.dp))
            .archivFokusRahmen(eckRadius = 5.dp, aufDunkel = true)
            .then(if (klickbar) Modifier.clickable(onClick = onClick) else Modifier)
            .clearAndSetSemantics {
                role = Role.Tab
                selected = aktiv
                contentDescription = "Schritt $nummer: $label"
            }
            .padding(horizontal = 6.dp),
        contentAlignment = Alignment.Center,
    ) {
        Text(
            text = "$nummer · $label",
            style = MaterialTheme.typography.labelMedium,
            fontFamily = FontFamily.Serif,
            color = if (aktiv) farben.stufenFarbeHell(2) else textFarbe,
            fontWeight = if (aktiv) FontWeight.Bold else FontWeight.Medium,
        )
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
    val flaeche = if (ausgewaehlt) farben.papierHell else farben.papierHell.copy(alpha = 0.58f)
    val rahmen = if (ausgewaehlt) farben.akzent else farben.linieFein.copy(alpha = 0.85f)

    Surface(
        modifier = modifier
            .defaultMinSize(minHeight = if (kompakt) 88.dp else 112.dp)
            .clip(RoundedCornerShape(6.dp))
            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = false)
            .clickable(onClick = onClick)
            .clearAndSetSemantics {
                role = Role.RadioButton
                selected = ausgewaehlt
                stateDescription = if (ausgewaehlt) "Ausgewählt" else "Nicht ausgewählt"
                contentDescription = "${herkunft.titel}: ${herkunft.zusatz}. ${herkunft.text}"
            },
        color = flaeche,
        shape = RoundedCornerShape(6.dp),
        border = BorderStroke(if (ausgewaehlt) 1.4.dp else 0.75.dp, rahmen),
        shadowElevation = if (ausgewaehlt) 1.dp else 0.dp,
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
                    .padding(
                        horizontal = if (kompakt) 14.dp else 16.dp,
                        vertical = if (kompakt) 10.dp else 14.dp,
                    ),
                verticalArrangement = Arrangement.spacedBy(4.dp),
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
                    color = farben.tinteMatt,
                    maxLines = if (kompakt) 2 else 3,
                    overflow = TextOverflow.Ellipsis,
                )
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
    val flaeche = if (ausgewaehlt) farben.papierHell else Color.Transparent
    val rahmen = if (ausgewaehlt) farben.akzent else farben.linieFein.copy(alpha = 0.85f)

    Surface(
        modifier = modifier
            .defaultMinSize(minHeight = metrik.minTouchHoehe + 6.dp)
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
        border = BorderStroke(if (ausgewaehlt) 1.3.dp else 0.75.dp, rahmen),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 12.dp, vertical = 9.dp),
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
                maxLines = 1,
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
