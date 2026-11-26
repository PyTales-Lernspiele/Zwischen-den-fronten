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
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.layout.windowInsetsPadding
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
import androidx.compose.ui.unit.dp
import de.pytales.zdf.content.GameContent
import de.pytales.zdf.model.ModusKonfiguration
import de.pytales.zdf.model.SpielModus
import de.pytales.zdf.ui.components.ArchivZierLinie
import de.pytales.zdf.ui.components.HakenIcon
import de.pytales.zdf.ui.components.archivEckenDekor
import de.pytales.zdf.ui.components.archivFokusGruppe
import de.pytales.zdf.ui.components.archivFokusRahmen
import de.pytales.zdf.ui.components.archivPapierHintergrund
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.media.ArchivSzenenBild
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.theme.ArchivTheme

/**
 * Einladender, ruhiger Querformat-Startbildschirm im Buchdruck- & Skizzenbuch-Stil:
 * - Links: stimmungsvoll gerahmtes Stil-A-Motiv (`schauplatz_brotschlange`) mit Buchtitel
 *   „Zwischen den Fronten“ & „Alltag 1914–1919“
 * - Rechts: klare, aufgeräumte Auswahl *Kurzer Verlauf* / *Langer Verlauf*, prominenter
 *   Button „Durchgang beginnen“ sowie dezente Zugänge für *Grundsätze* und *Einstellungen*
 * - Frei von Analysemodus, Entwickler-Vorschau, Stempel-Flut und verschachtelten Kästen.
 */
@Composable
fun StartScreen(
    content: GameContent,
    uiState: SpielUiState,
    onModusWaehlen: (SpielModus) -> Unit,
    onAudioToggle: () -> Unit,
    onEinstellungenOeffnen: () -> Unit,
    onGrundsaetzeOeffnen: () -> Unit,
    onDurchgangBeginnen: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val konf = content.konfiguration
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val aktiverModus = uiState.gameState.modus
    val direktwahlAktiv = uiState.gameState.direktwahlAktiv
    val querformat = metrik.zweispaltigeBuehne

    val werkzeugZeile: @Composable (Modifier) -> Unit = { mod ->
        Row(
            modifier = mod.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                text = "Verlauf wählen",
                style = MaterialTheme.typography.labelMedium,
                fontFamily = FontFamily.Serif,
                color = farben.tinteMatt,
                fontWeight = FontWeight.SemiBold,
            )
            Row(
                horizontalArrangement = Arrangement.spacedBy(2.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                AudioIconKnopf(
                    audioZustand = uiState.audioZustand,
                    aufDunkel = false,
                    onToggle = onAudioToggle,
                )
                EinstellungenIconKnopf(
                    aufDunkel = false,
                    hatHinweisPunkt = direktwahlAktiv,
                    onClick = onEinstellungenOeffnen,
                )
            }
        }
    }

    Box(
        modifier = modifier
            .fillMaxSize()
            .archivPapierHintergrund()
            .windowInsetsPadding(WindowInsets.safeDrawing)
            .verticalScroll(rememberScrollState())
            .padding(
                horizontal = metrik.aussenAbstand,
                vertical = if (metrik.kompakteHoehe) 10.dp else 24.dp,
            ),
        contentAlignment = Alignment.Center,
    ) {
        val titelBuehne: @Composable (Modifier) -> Unit = { mod ->
            Column(
                modifier = mod,
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(if (metrik.kompakteHoehe) 8.dp else 14.dp),
            ) {
                // Stimmungsvoll gerahmtes Stil-A-Titelmotiv
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = farben.papierHell,
                    shape = RoundedCornerShape(6.dp),
                    border = BorderStroke(0.75.dp, farben.linieFein.copy(alpha = 0.85f)),
                    shadowElevation = 3.dp,
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .archivEckenDekor(
                                farbe = farben.linie.copy(alpha = 0.45f),
                                einrueckung = 5.dp,
                                schenkelLaenge = 9.dp,
                            )
                            .padding(8.dp),
                    ) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .aspectRatio(16f / 9f)
                                .clip(RoundedCornerShape(3.dp))
                                .background(farben.papier),
                        ) {
                            ArchivSzenenBild(
                                bildId = "schauplatz_brotschlange",
                                schauplatzBild = "schauplatz_brotschlange",
                                beschreibung = "Illustration im Stil A: Alltag in einer deutschen Straße um 1915",
                            ) {
                                Box(
                                    modifier = Modifier.fillMaxSize(),
                                    contentAlignment = Alignment.Center,
                                ) {
                                    Text(
                                        text = "1914 – 1919",
                                        style = MaterialTheme.typography.headlineMedium,
                                        color = farben.akzent,
                                    )
                                }
                            }
                        }
                    }
                }

                // Buchdruck-Titelblock unter dem Motiv
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(3.dp),
                ) {
                    Text(
                        text = "1914  —  1919",
                        style = MaterialTheme.typography.labelMedium,
                        fontFamily = FontFamily.Serif,
                        color = farben.akzent,
                        fontWeight = FontWeight.SemiBold,
                    )
                    Text(
                        text = konf.spielTitel,
                        style = if (metrik.kompakteHoehe) {
                            MaterialTheme.typography.headlineMedium
                        } else {
                            MaterialTheme.typography.displaySmall
                        },
                        color = farben.tinte,
                        textAlign = TextAlign.Center,
                        modifier = Modifier.archivUeberschrift(),
                    )
                    Text(
                        text = "Alltag 1914–1919  ·  ${konf.zielgruppe}",
                        style = MaterialTheme.typography.bodySmall,
                        fontFamily = FontFamily.Serif,
                        fontStyle = FontStyle.Italic,
                        color = farben.tinteMatt,
                        textAlign = TextAlign.Center,
                    )
                }
            }
        }

        val aktionsSpalte: @Composable (Modifier, Boolean) -> Unit = { mod, mitWerkzeugZeile ->
            Column(
                modifier = mod.archivFokusGruppe(),
                verticalArrangement = Arrangement.spacedBy(if (metrik.kompakteHoehe) 8.dp else 14.dp),
            ) {
                if (mitWerkzeugZeile) {
                    werkzeugZeile(Modifier)
                }

                // Auswahl Kurzer Verlauf / Langer Verlauf
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    listOf(SpielModus.KURZ, SpielModus.LANG).forEach { modus ->
                        val modusKonf = konf.modi.getValue(modus)
                        StartModusKarte(
                            modus = modus,
                            konf = modusKonf,
                            ausgewaehlt = modus == aktiverModus,
                            kompakt = metrik.kompakteHoehe,
                            onClick = { onModusWaehlen(modus) },
                        )
                    }
                }

                if (direktwahlAktiv) {
                    Text(
                        text = "Unterrichts-Direktwahl aktiv: Pfad wird nach der Herkunft frei gewählt.",
                        style = MaterialTheme.typography.labelSmall,
                        fontStyle = FontStyle.Italic,
                        color = farben.akzent,
                    )
                }

                ArchivPrimaerKnopf(
                    label = "Durchgang beginnen",
                    akzentStil = true,
                    onClick = onDurchgangBeginnen,
                    modifier = Modifier.fillMaxWidth(),
                )

                ArchivZierLinie(
                    farbe = farben.linieFein.copy(alpha = 0.7f),
                    akzentFarbe = farben.akzent.copy(alpha = 0.45f),
                )

                // Dezente Zugänge zu Grundsätzen & Einstellungen
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    ArchivTextKnopf(
                        label = "Drei Grundsätze",
                        onClick = onGrundsaetzeOeffnen,
                    )
                    ArchivTextKnopf(
                        label = "Einstellungen",
                        hervorgehoben = direktwahlAktiv,
                        onClick = onEinstellungenOeffnen,
                    )
                }
            }
        }

        if (querformat) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .widthIn(max = 1040.dp),
                horizontalArrangement = Arrangement.spacedBy(if (metrik.kompakteHoehe) 20.dp else 32.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                titelBuehne(Modifier.weight(0.48f))
                aktionsSpalte(Modifier.weight(0.52f), true)
            }
        } else {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .widthIn(max = 520.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
            ) {
                werkzeugZeile(Modifier)
                titelBuehne(Modifier.fillMaxWidth())
                aktionsSpalte(Modifier.fillMaxWidth(), false)
            }
        }
    }
}

@Composable
private fun StartModusKarte(
    modus: SpielModus,
    konf: ModusKonfiguration,
    ausgewaehlt: Boolean,
    kompakt: Boolean,
    onClick: () -> Unit,
) {
    val farben = ArchivTheme.farben
    val flaeche = if (ausgewaehlt) farben.papierHell else farben.papierHell.copy(alpha = 0.62f)
    val rahmen = if (ausgewaehlt) farben.akzent else farben.linieFein.copy(alpha = 0.85f)
    val kurzInfo = when (modus) {
        SpielModus.KURZ -> "${konf.zielzahl} Stationen · ca. 15–20 Min. (Einzelstunde)"
        SpielModus.LANG -> "${konf.zielzahl} Stationen · ca. 25–35 Min. (Vertiefung)"
    }

    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .defaultMinSize(minHeight = if (kompakt) 58.dp else 72.dp)
            .clip(RoundedCornerShape(6.dp))
            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = false)
            .clickable(onClick = onClick)
            .clearAndSetSemantics {
                role = Role.RadioButton
                selected = ausgewaehlt
                stateDescription = if (ausgewaehlt) "Ausgewählt" else "Nicht ausgewählt"
                contentDescription = "${konf.bezeichnung}: $kurzInfo. ${konf.umfang}"
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
                    .width(if (ausgewaehlt) 3.5.dp else 0.dp)
                    .fillMaxHeight()
                    .background(if (ausgewaehlt) farben.akzent else Color.Transparent),
            )
            Row(
                modifier = Modifier
                    .weight(1f)
                    .padding(
                        horizontal = if (kompakt) 12.dp else 16.dp,
                        vertical = if (kompakt) 9.dp else 12.dp,
                    ),
                horizontalArrangement = Arrangement.spacedBy(10.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Column(
                    modifier = Modifier.weight(1f),
                    verticalArrangement = Arrangement.spacedBy(2.dp),
                ) {
                    Text(
                        text = konf.bezeichnung,
                        style = MaterialTheme.typography.titleMedium,
                        fontFamily = FontFamily.Serif,
                        color = farben.tinte,
                        fontWeight = if (ausgewaehlt) FontWeight.Bold else FontWeight.SemiBold,
                    )
                    Text(
                        text = kurzInfo,
                        style = MaterialTheme.typography.bodySmall,
                        color = farben.tinteMatt,
                    )
                    if (!kompakt) {
                        Text(
                            text = konf.umfang,
                            style = MaterialTheme.typography.bodySmall,
                            color = farben.tinteMatt.copy(alpha = 0.88f),
                        )
                    }
                }
                if (ausgewaehlt) {
                    HakenIcon(
                        farbe = farben.akzent,
                        groesse = 16.dp,
                    )
                }
            }
        }
    }
}
