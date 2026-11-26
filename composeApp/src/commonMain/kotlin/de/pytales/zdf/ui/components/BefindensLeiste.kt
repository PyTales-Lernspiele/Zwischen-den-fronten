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
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.state.WertKachelUiState
import de.pytales.zdf.ui.theme.ArchivTheme

/**
 * Schlanke, einzeilige Befindensleiste mit allen 4 Befindenswerten
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
        verticalArrangement = Arrangement.spacedBy(6.dp),
    ) {
        zeilen.forEach { zeile ->
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(if (schlank) 6.dp else 8.dp),
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
 * Einzelne tipp-/klickbare Kachel eines Befindenswerts mit 5-Segment-Balken und Delta-Hinweis.
 * Im schlanken Querformat-Modus (~48–52 dp hoch) bleibt sie luftig und sofort erfassbar.
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
    val stufenFarbe = if (aufDunkel) farben.stufenFarbeHell(wert.stufe) else farben.stufenFarbe(wert.stufe)
    val leereSegmentFarbe = if (aufDunkel) farben.segmentDunkel else farben.segmentLeer
    val flaeche = when {
        aufDunkel && istAusgewaehlt -> farben.dunkelHell
        aufDunkel -> farben.dunkelHell.copy(alpha = 0.72f)
        istAusgewaehlt -> farben.papierDunkel
        else -> farben.papierHell
    }
    val rahmenFarbe = when {
        istAusgewaehlt -> stufenFarbe
        wert.istKritisch && aufDunkel -> stufenFarbe.copy(alpha = 0.45f)
        aufDunkel -> farben.segmentDunkel.copy(alpha = 0.75f)
        else -> farben.linieFein
    }
    val titelFarbe = if (aufDunkel) farben.textHell else farben.tinte

    val beschreibung = buildString {
        append("${wert.bezeichnung}: ${wert.stufenName}, ")
        append("${wert.gefuellteSegmente} von ${wert.segmenteGesamt} Segmenten")
        if (wert.aenderungsText != null) {
            append(", letzte Änderung ${wert.aenderungsText}")
        }
        append(". ")
        append(if (istAusgewaehlt) "Erklärkarte schließen." else "Tippen für Erklärung.")
    }

    Surface(
        modifier = modifier
            .defaultMinSize(minHeight = metrik.minTouchHoehe)
            .clip(RoundedCornerShape(6.dp))
            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = aufDunkel)
            .clickable(onClick = onClick)
            .clearAndSetSemantics {
                role = Role.Button
                selected = istAusgewaehlt
                stateDescription = if (istAusgewaehlt) "Erklärung geöffnet" else "Erklärung geschlossen"
                contentDescription = beschreibung
            },
        color = flaeche,
        shape = RoundedCornerShape(6.dp),
        border = BorderStroke(
            width = if (istAusgewaehlt) 1.25.dp else 0.75.dp,
            color = rahmenFarbe,
        ),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(
                    horizontal = if (schlank) 8.dp else 10.dp,
                    vertical = if (schlank) 5.dp else 7.dp,
                ),
            verticalArrangement = Arrangement.spacedBy(if (schlank) 4.dp else 5.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = wert.bezeichnung,
                    style = if (schlank) MaterialTheme.typography.labelMedium else MaterialTheme.typography.labelLarge,
                    color = titelFarbe,
                    fontWeight = FontWeight.SemiBold,
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

            FuenfSegmentBalken(
                gefuellteSegmente = wert.gefuellteSegmente,
                segmenteGesamt = wert.segmenteGesamt,
                aktiveFarbe = stufenFarbe,
                leereFarbe = leereSegmentFarbe,
                segmentHoehe = if (schlank) 5.5.dp else metrik.segmentHoehe,
            )

            if (!schlank) {
                Text(
                    text = wert.stufenName,
                    style = MaterialTheme.typography.labelSmall,
                    color = stufenFarbe,
                    fontWeight = FontWeight.Medium,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
            }
        }
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
    val hintergrund = akzentFarbe.copy(alpha = if (aufDunkel) 0.18f else 0.12f)

    Box(
        modifier = Modifier
            .background(hintergrund, RoundedCornerShape(3.dp))
            .padding(horizontal = 4.dp, vertical = 0.5.dp),
    ) {
        Text(
            text = text,
            style = MaterialTheme.typography.labelSmall,
            color = akzentFarbe,
            fontWeight = FontWeight.Bold,
            maxLines = 1,
        )
    }
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
                    .height(3.dp)
                    .background(stufenFarbe),
            )

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 18.dp, vertical = 14.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp),
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
                        ArchivStempel(
                            text = wert.stufenName,
                            farbe = stufenFarbe,
                            hintergrund = stufenFarbe.copy(alpha = 0.09f),
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
                            .clickable(onClick = onSchliessen)
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
                        modifier = Modifier.width(124.dp),
                    )
                    Text(
                        text = wert.stufenKurz,
                        style = MaterialTheme.typography.bodySmall,
                        color = farben.tinteMatt,
                        modifier = Modifier.weight(1f),
                    )
                }

                // Zitat mit feiner linker Linie statt Kasten-in-Kasten
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(IntrinsicSize.Min)
                        .background(farben.papier.copy(alpha = 0.72f), RoundedCornerShape(4.dp))
                        .padding(end = 12.dp),
                    horizontalArrangement = Arrangement.spacedBy(10.dp),
                ) {
                    Box(
                        modifier = Modifier
                            .width(2.5.dp)
                            .fillMaxHeight()
                            .background(stufenFarbe.copy(alpha = 0.8f)),
                    )
                    Text(
                        text = "„${wert.zustandssatz}“",
                        style = MaterialTheme.typography.bodyMedium,
                        fontFamily = FontFamily.Serif,
                        fontStyle = FontStyle.Italic,
                        color = farben.tinte,
                        modifier = Modifier.padding(vertical = 8.dp),
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
