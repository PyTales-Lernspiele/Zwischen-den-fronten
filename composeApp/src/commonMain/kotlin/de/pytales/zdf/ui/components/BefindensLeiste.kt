package de.pytales.zdf.ui.components

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
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
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
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import de.pytales.zdf.audio.SoundEffekt
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.state.WertKachelUiState
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.LocalSoundEffektSpielen

/**
 * Flache, luftige Befindensleiste mit allen 4 Befindenswerten
 * (*Hunger, Erschöpfung, Verdacht, Einsamkeit*):
 * - 5-Segment-Balken (*voll = gut* über `ValueMetrics`)
 * - Stufenfarben (`stufenHell` auf dunkler Kopfleiste, `stufen` auf hellem Papier)
 * - Letzte Veränderung (`+1` / `-1`)
 * - Tipp-/Klick-Auswahl öffnet die ruhige [WertErklaerKarte] als Overlay ohne Seitenverschiebung.
 */
@Composable
fun BefindensLeiste(
    werte: List<WertKachelUiState>,
    ausgewaehlterWert: WertSchluessel?,
    onWertTippen: (WertSchluessel) -> Unit,
    modifier: Modifier = Modifier,
    aufDunkel: Boolean = true,
    spalten: Int = ArchivTheme.metrik.werteSpalten,
    schlank: Boolean = false,
) {
    val effektiveSpalten = spalten.coerceIn(1, 4)
    val zeilen = werte.chunked(effektiveSpalten)

    Column(
        modifier = modifier
            .fillMaxWidth()
            .archivFokusGruppe(),
        verticalArrangement = Arrangement.spacedBy(4.dp),
    ) {
        zeilen.forEach { zeile ->
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(if (schlank) 10.dp else 14.dp),
            ) {
                zeile.forEach { wert ->
                    WertKachel(
                        wert = wert,
                        istAusgewaehlt = wert.schluessel == ausgewaehlterWert,
                        aufDunkel = aufDunkel,
                        schlank = schlank,
                        onClick = { onWertTippen(wert.schluessel) },
                        modifier = Modifier.weight(1f),
                    )
                }
                repeat(effektiveSpalten - zeile.size) {
                    Spacer(modifier = Modifier.weight(1f))
                }
            }
        }
    }
}

/**
 * Einzelner flacher, luftiger Befindenswert ohne schweren Kastenrahmen:
 * zeigt Bezeichnung, kompaktes Delta und den 5-Segment-Balken klar auf einen Blick.
 */
@Composable
fun WertKachel(
    wert: WertKachelUiState,
    istAusgewaehlt: Boolean,
    aufDunkel: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    schlank: Boolean = false,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val spieleEffekt = LocalSoundEffektSpielen.current
    val stufenFarbe = if (aufDunkel) farben.stufenFarbeHell(wert.stufe) else farben.stufenFarbe(wert.stufe)
    val leereSegmentFarbe = if (aufDunkel) farben.segmentDunkel else farben.segmentLeer
    val hintergrund = when {
        aufDunkel && istAusgewaehlt -> farben.dunkelHell
        aufDunkel -> Color.Transparent
        istAusgewaehlt -> farben.papierDunkel
        else -> Color.Transparent
    }
    val titelFarbe = if (aufDunkel) {
        if (wert.istKritisch) stufenFarbe else farben.textHell
    } else {
        farben.tinte
    }

    val beschreibung = buildString {
        append("${wert.bezeichnung}: ${wert.stufenName}, ")
        append("${wert.gefuellteSegmente} von ${wert.segmenteGesamt} Segmenten")
        if (wert.aenderungsText != null) {
            append(", letzte Änderung ${wert.aenderungsText}")
        }
        append(". ")
        append(if (istAusgewaehlt) "Erklärkarte schließen." else "Tippen für Erklärung.")
    }

    Column(
        modifier = modifier
            .defaultMinSize(minHeight = metrik.minTouchHoehe)
            .clip(RoundedCornerShape(5.dp))
            .background(hintergrund)
            .archivFokusRahmen(eckRadius = 5.dp, aufDunkel = aufDunkel)
            .clickable {
                spieleEffekt(SoundEffekt.KLICK_SANFT)
                onClick()
            }
            .clearAndSetSemantics {
                role = Role.Button
                selected = istAusgewaehlt
                stateDescription = if (istAusgewaehlt) "Erklärung geöffnet" else "Erklärung geschlossen"
                contentDescription = beschreibung
            }
            .padding(
                horizontal = if (schlank) 6.dp else 8.dp,
                vertical = if (schlank) 6.dp else 7.dp,
            ),
        verticalArrangement = Arrangement.Center,
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                text = wert.bezeichnung,
                style = MaterialTheme.typography.labelMedium,
                color = titelFarbe,
                fontWeight = if (wert.istKritisch || istAusgewaehlt) FontWeight.SemiBold else FontWeight.Medium,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
                modifier = Modifier.weight(1f),
            )

            if (wert.aenderungsText != null) {
                Spacer(modifier = Modifier.width(4.dp))
                WertDeltaBadge(
                    text = wert.aenderungsText,
                    schlechter = wert.aenderungIstSchlechter,
                    aufDunkel = aufDunkel,
                )
            }
        }

        Spacer(modifier = Modifier.height(5.dp))

        FuenfSegmentBalken(
            gefuellteSegmente = wert.gefuellteSegmente,
            segmenteGesamt = wert.segmenteGesamt,
            aktiveFarbe = stufenFarbe,
            leereFarbe = leereSegmentFarbe,
            segmentHoehe = if (schlank) 5.dp else 6.dp,
        )
    }
}

@Composable
private fun WertDeltaBadge(
    text: String,
    schlechter: Boolean,
    aufDunkel: Boolean,
) {
    val farben = ArchivTheme.farben
    val akzentFarbe = farben.deltaFarbe(schlechter = schlechter, aufDunkel = aufDunkel)

    Text(
        text = text,
        style = MaterialTheme.typography.labelSmall,
        color = akzentFarbe,
        fontWeight = FontWeight.Bold,
        maxLines = 1,
    )
}

/**
 * Ruhige Erklärkarte für den ausgewählten Befindenswert (für Darstellung im leichten Overlay).
 * Zeigt Name, Stufe, 5-Segment-Balken, aktuellen Zustandssatz, Erklärung und Auswirkung.
 */
@Composable
fun WertErklaerKarte(
    wert: WertKachelUiState?,
    onSchliessen: () -> Unit,
    modifier: Modifier = Modifier,
) {
    if (wert == null) return
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val spieleEffekt = LocalSoundEffektSpielen.current
    val stufenFarbe = farben.stufenFarbe(wert.stufe)

    Surface(
        modifier = modifier
            .fillMaxWidth()
            .archivLiveHinweis(),
        color = farben.papierHell,
        shape = RoundedCornerShape(8.dp),
        border = BorderStroke(0.75.dp, farben.linieFein),
        shadowElevation = 8.dp,
    ) {
        Column(modifier = Modifier.fillMaxWidth()) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(2.5.dp)
                    .background(stufenFarbe),
            )

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 20.dp, vertical = 16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(10.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.weight(1f),
                    ) {
                        Text(
                            text = wert.bezeichnung,
                            style = MaterialTheme.typography.headlineSmall,
                            color = farben.tinte,
                            modifier = Modifier.archivUeberschrift(),
                        )
                        Text(
                            text = wert.stufenName,
                            style = MaterialTheme.typography.labelMedium,
                            color = stufenFarbe,
                            fontWeight = FontWeight.SemiBold,
                        )
                        if (wert.aenderungsText != null) {
                            WertDeltaBadge(
                                text = wert.aenderungsText,
                                schlechter = wert.aenderungIstSchlechter,
                                aufDunkel = false,
                            )
                        }
                    }

                    Box(
                        modifier = Modifier
                            .defaultMinSize(minWidth = metrik.minTouchHoehe, minHeight = metrik.minTouchHoehe)
                            .clip(RoundedCornerShape(6.dp))
                            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = false)
                            .clickable {
                                spieleEffekt(SoundEffekt.KLICK_SANFT)
                                onSchliessen()
                            }
                            .semantics {
                                role = Role.Button
                                contentDescription = "Erklärkarte für ${wert.bezeichnung} schließen"
                            },
                        contentAlignment = Alignment.Center,
                    ) {
                        SchliessenIcon(farbe = farben.tinteMatt, groesse = 18.dp)
                    }
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    FuenfSegmentBalken(
                        gefuellteSegmente = wert.gefuellteSegmente,
                        segmenteGesamt = wert.segmenteGesamt,
                        aktiveFarbe = stufenFarbe,
                        leereFarbe = farben.segmentLeer,
                        modifier = Modifier.width(120.dp),
                    )
                    Text(
                        text = wert.stufenKurz,
                        style = MaterialTheme.typography.bodySmall,
                        color = farben.tinteMatt,
                        modifier = Modifier.weight(1f),
                    )
                }

                // Zitat mit feiner linker Linie statt Kasten
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(IntrinsicSize.Min),
                    horizontalArrangement = Arrangement.spacedBy(10.dp),
                ) {
                    Box(
                        modifier = Modifier
                            .width(2.dp)
                            .fillMaxHeight()
                            .background(stufenFarbe.copy(alpha = 0.75f)),
                    )
                    Text(
                        text = "„${wert.zustandssatz}“",
                        style = MaterialTheme.typography.bodyMedium,
                        fontFamily = FontFamily.Serif,
                        fontStyle = FontStyle.Italic,
                        color = farben.tinte,
                        modifier = Modifier.padding(vertical = 2.dp),
                    )
                }

                Text(
                    text = wert.erklaerung,
                    style = MaterialTheme.typography.bodyMedium,
                    color = farben.tinte,
                )
                Text(
                    text = wert.folge,
                    style = MaterialTheme.typography.bodySmall,
                    color = if (wert.istKritisch) farben.akzent else farben.tinteMatt,
                    fontWeight = if (wert.istKritisch) FontWeight.SemiBold else FontWeight.Normal,
                )
            }
        }
    }
}
