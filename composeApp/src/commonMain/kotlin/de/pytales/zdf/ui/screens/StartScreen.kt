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
import de.pytales.zdf.audio.SoundEffekt
import de.pytales.zdf.content.GameContent
import de.pytales.zdf.model.ModusKonfiguration
import de.pytales.zdf.model.SpielModus
import de.pytales.zdf.ui.components.HakenIcon
import de.pytales.zdf.ui.components.archivFokusGruppe
import de.pytales.zdf.ui.components.archivFokusRahmen
import de.pytales.zdf.ui.components.archivPapierHintergrund
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.media.ArchivSzenenBild
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.LocalSoundEffektSpielen

/**
 * Radikal ruhiger, aufgeräumter Startbildschirm wie eine aufgeschlagene Buch-Titelseite:
 * - Oben rechts (genau einmal, ohne doppelte Zugänge): flache Symbole für Ton & Einstellungen.
 * - Links: stimmungsvoll gerahmtes Stil-A-Titelbild + Titel „Zwischen den Fronten“ & „1914–1919“.
 * - Rechts: schlichte Auswahl *Kurz* / *Lang*, prominenter Button „Durchgang beginnen“ und
 *   eine einzelne unauffällige Fußzeile für *Grundsätze*. Viel ruhige Archivpapier-Fläche.
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
    val kompakt = metrik.kompakteHoehe
    val aktiverModus = uiState.gameState.modus
    val direktwahlAktiv = uiState.gameState.direktwahlAktiv
    val querformat = metrik.zweispaltigeBuehne

    Box(
        modifier = modifier
            .fillMaxSize()
            .archivPapierHintergrund()
            .windowInsetsPadding(WindowInsets.safeDrawing),
    ) {
        // Einziger, unaufdringlicher Zugang zu Ton & Einstellungen oben rechts
        Row(
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(horizontal = metrik.aussenAbstand, vertical = 4.dp),
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

        // Zentrierte Buch-Titelseite mit viel freier Archivpapier-Fläche
        Box(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(
                    start = metrik.aussenAbstand,
                    end = metrik.aussenAbstand,
                    top = if (kompakt) 44.dp else 56.dp,
                    bottom = if (kompakt) 14.dp else 28.dp,
                ),
            contentAlignment = Alignment.Center,
        ) {
            val titelBuehne: @Composable (Modifier) -> Unit = { mod ->
                Column(
                    modifier = mod,
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(if (kompakt) 10.dp else 16.dp),
                ) {
                    Surface(
                        modifier = Modifier.fillMaxWidth(),
                        color = farben.papierHell,
                        shape = RoundedCornerShape(5.dp),
                        border = BorderStroke(0.75.dp, farben.linieFein.copy(alpha = 0.78f)),
                        shadowElevation = 2.dp,
                    ) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(6.dp),
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
                                            text = "1914–1919",
                                            style = MaterialTheme.typography.headlineMedium,
                                            color = farben.akzent,
                                        )
                                    }
                                }
                            }
                        }
                    }

                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(2.dp),
                    ) {
                        Text(
                            text = "1914–1919",
                            style = MaterialTheme.typography.labelMedium,
                            fontFamily = FontFamily.Serif,
                            color = farben.akzent,
                            fontWeight = FontWeight.SemiBold,
                        )
                        Text(
                            text = konf.spielTitel,
                            style = if (kompakt) {
                                MaterialTheme.typography.headlineMedium
                            } else {
                                MaterialTheme.typography.displaySmall
                            },
                            color = farben.tinte,
                            textAlign = TextAlign.Center,
                            modifier = Modifier.archivUeberschrift(),
                        )
                    }
                }
            }

            val aktionsSpalte: @Composable (Modifier) -> Unit = { mod ->
                Column(
                    modifier = mod.archivFokusGruppe(),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(if (kompakt) 12.dp else 18.dp),
                ) {
                    // Schlichte Auswahl Kurz / Lang
                    Column(
                        modifier = Modifier.fillMaxWidth(),
                        verticalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        listOf(SpielModus.KURZ, SpielModus.LANG).forEach { modus ->
                            val modusKonf = konf.modi.getValue(modus)
                            StartModusOption(
                                modus = modus,
                                konf = modusKonf,
                                ausgewaehlt = modus == aktiverModus,
                                kompakt = kompakt,
                                onClick = { onModusWaehlen(modus) },
                            )
                        }
                    }

                    if (direktwahlAktiv) {
                        Text(
                            text = "Direktwahl für den Unterricht aktiv",
                            style = MaterialTheme.typography.labelSmall,
                            fontStyle = FontStyle.Italic,
                            color = farben.akzent,
                            modifier = Modifier.fillMaxWidth(),
                        )
                    }

                    ArchivPrimaerKnopf(
                        label = "Durchgang beginnen",
                        akzentStil = true,
                        klickEffekt = SoundEffekt.ENTSCHEIDUNG,
                        onClick = onDurchgangBeginnen,
                        modifier = Modifier.fillMaxWidth(),
                    )

                    // Einzelne unauffällige Fußzeile für Grundsätze
                    ArchivTextKnopf(
                        label = "Grundsätze",
                        onClick = onGrundsaetzeOeffnen,
                    )
                }
            }

            if (querformat) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .widthIn(max = 980.dp),
                    horizontalArrangement = Arrangement.spacedBy(if (kompakt) 28.dp else 44.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    titelBuehne(Modifier.weight(0.50f))
                    aktionsSpalte(Modifier.weight(0.44f))
                }
            } else {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .widthIn(max = 460.dp),
                    verticalArrangement = Arrangement.spacedBy(20.dp),
                ) {
                    titelBuehne(Modifier.fillMaxWidth())
                    aktionsSpalte(Modifier.fillMaxWidth())
                    Spacer(modifier = Modifier.height(4.dp))
                }
            }
        }
    }
}

@Composable
private fun StartModusOption(
    modus: SpielModus,
    konf: ModusKonfiguration,
    ausgewaehlt: Boolean,
    kompakt: Boolean,
    onClick: () -> Unit,
) {
    val farben = ArchivTheme.farben
    val spieleEffekt = LocalSoundEffektSpielen.current
    val titel = when (modus) {
        SpielModus.KURZ -> "Kurz"
        SpielModus.LANG -> "Lang"
    }
    val kurzInfo = when (modus) {
        SpielModus.KURZ -> "${konf.zielzahl} Stationen · ca. 15–20 Min."
        SpielModus.LANG -> "${konf.zielzahl} Stationen · ca. 25–35 Min."
    }

    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .defaultMinSize(minHeight = if (kompakt) 52.dp else 60.dp)
            .clip(RoundedCornerShape(6.dp))
            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = false)
            .clickable {
                spieleEffekt(SoundEffekt.KLICK_SANFT)
                onClick()
            }
            .clearAndSetSemantics {
                role = Role.RadioButton
                selected = ausgewaehlt
                stateDescription = if (ausgewaehlt) "Ausgewählt" else "Nicht ausgewählt"
                contentDescription = "${konf.bezeichnung}: $kurzInfo"
            },
        color = if (ausgewaehlt) farben.papierHell else Color.Transparent,
        shape = RoundedCornerShape(6.dp),
        border = BorderStroke(
            width = if (ausgewaehlt) 1.2.dp else 0.75.dp,
            color = if (ausgewaehlt) farben.akzent else farben.linieFein.copy(alpha = 0.85f),
        ),
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
            Row(
                modifier = Modifier
                    .weight(1f)
                    .padding(
                        horizontal = if (kompakt) 14.dp else 16.dp,
                        vertical = if (kompakt) 10.dp else 12.dp,
                    ),
                horizontalArrangement = Arrangement.spacedBy(10.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = titel,
                    style = MaterialTheme.typography.titleMedium,
                    fontFamily = FontFamily.Serif,
                    color = farben.tinte,
                    fontWeight = if (ausgewaehlt) FontWeight.Bold else FontWeight.SemiBold,
                )
                Text(
                    text = kurzInfo,
                    style = MaterialTheme.typography.bodySmall,
                    color = farben.tinteMatt,
                    modifier = Modifier.weight(1f),
                )
                if (ausgewaehlt) {
                    HakenIcon(
                        farbe = farben.akzent,
                        groesse = 15.dp,
                    )
                }
            }
        }
    }
}
