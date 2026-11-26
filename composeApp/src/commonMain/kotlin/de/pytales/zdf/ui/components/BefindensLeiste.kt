package de.pytales.zdf.ui.components

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
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.defaultMinSize
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
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.state.WertKachelUiState
import de.pytales.zdf.ui.theme.ArchivTheme

/**
 * Obere Befindensleiste mit allen 4 Befindenswerten (*Hunger, Erschöpfung, Verdacht, Einsamkeit*):
 * - 5-Segment-Balken (*voll = gut* über `ValueMetrics`)
 * - Stufenfarben (`stufenHell` auf dunklem Kopfbalken, `stufen` auf hellem Archivpapier)
 * - Letzte Veränderung (`+1` / `-1` in Anzeigelogik)
 * - Touch-/Klick-Auswahl zum Anheften der [WertErklaerKarte] (kein reines Hover!).
 */
@Composable
fun BefindensLeiste(
    werte: List<WertKachelUiState>,
    ausgewaehlterWert: WertSchluessel?,
    onWertTippen: (WertSchluessel) -> Unit,
    modifier: Modifier = Modifier,
    aufDunkel: Boolean = true,
    spalten: Int = ArchivTheme.metrik.werteSpalten,
) {
    val effektiveSpalten = spalten.coerceIn(1, 4)
    val zeilen = werte.chunked(effektiveSpalten)

    Column(
        modifier = modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        zeilen.forEach { zeile ->
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                zeile.forEach { wert ->
                    WertKachel(
                        wert = wert,
                        istAusgewaehlt = wert.schluessel == ausgewaehlterWert,
                        aufDunkel = aufDunkel,
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
 * Einzelne tipp-/klickbare Kachel eines Befindenswerts mit 5-Segment-Balken und Delta-Badge.
 */
@Composable
fun WertKachel(
    wert: WertKachelUiState,
    istAusgewaehlt: Boolean,
    aufDunkel: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val stufenFarbe = if (aufDunkel) farben.stufenFarbeHell(wert.stufe) else farben.stufenFarbe(wert.stufe)
    val leereSegmentFarbe = if (aufDunkel) farben.segmentDunkel else farben.segmentLeer
    val flaeche = when {
        aufDunkel && istAusgewaehlt -> farben.dunkelHell.copy(alpha = 0.98f)
        aufDunkel -> farben.dunkelHell
        istAusgewaehlt -> farben.papierDunkel
        else -> farben.papierHell
    }
    val rahmenFarbe = when {
        istAusgewaehlt -> stufenFarbe
        aufDunkel -> farben.segmentDunkel
        else -> farben.linieFein
    }
    val titelFarbe = if (aufDunkel) farben.textHell else farben.tinte
    val hinweisFarbe = if (aufDunkel) farben.textHell.copy(alpha = 0.72f) else farben.tinteMatt

    val beschreibung = buildString {
        append("${wert.bezeichnung}: ${wert.stufenName}, ")
        append("${wert.gefuellteSegmente} von ${wert.segmenteGesamt} Segmenten")
        if (wert.aenderungsText != null) {
            append(", letzte Änderung ${wert.aenderungsText}")
        }
        append(". Tippen für Erklärung.")
    }

    Surface(
        modifier = modifier
            .defaultMinSize(minHeight = metrik.minTouchHoehe)
            .clip(RoundedCornerShape(4.dp))
            .clickable(onClick = onClick)
            .semantics {
                role = Role.Button
                selected = istAusgewaehlt
                contentDescription = beschreibung
            },
        color = flaeche,
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(
            width = if (istAusgewaehlt) 1.5.dp else 1.dp,
            color = rahmenFarbe,
        ),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 10.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(5.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = wert.bezeichnung,
                    style = MaterialTheme.typography.labelLarge,
                    color = titelFarbe,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f),
                )

                if (wert.aenderungsText != null) {
                    Spacer(modifier = Modifier.width(6.dp))
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
            )

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = wert.stufenName,
                    style = MaterialTheme.typography.labelSmall,
                    color = stufenFarbe,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f),
                )
                Text(
                    text = if (istAusgewaehlt) "▴" else "▾",
                    style = MaterialTheme.typography.labelSmall,
                    color = hinweisFarbe,
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
    val hintergrund = akzentFarbe.copy(alpha = if (aufDunkel) 0.22f else 0.14f)

    Box(
        modifier = Modifier
            .border(1.dp, akzentFarbe.copy(alpha = 0.7f), RoundedCornerShape(2.dp))
            .background(hintergrund, RoundedCornerShape(2.dp))
            .padding(horizontal = 5.dp, vertical = 1.dp),
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
 * Angeheftete Touch-/Klick-Erklärkarte für den ausgewählten Befindenswert.
 * Zeigt Stufenname, Kurzbeschreibung, aktuellen `zustandssatz`, `erklaerung` und `folge`.
 */
@Composable
fun WertErklaerKarte(
    wert: WertKachelUiState?,
    onSchliessen: () -> Unit,
    modifier: Modifier = Modifier,
) {
    AnimatedVisibility(
        visible = wert != null,
        enter = fadeIn() + expandVertically(),
        exit = fadeOut() + shrinkVertically(),
        modifier = modifier,
    ) {
        if (wert != null) {
            val farben = ArchivTheme.farben
            val stufenFarbe = farben.stufenFarbe(wert.stufe)

            Surface(
                modifier = Modifier.fillMaxWidth(),
                color = farben.papierHell,
                shape = RoundedCornerShape(4.dp),
                border = BorderStroke(1.dp, farben.linie),
                shadowElevation = 2.dp,
            ) {
                Column(modifier = Modifier.fillMaxWidth()) {
                    // Farbstreifen entsprechend aktueller Belastungsstufe
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(3.dp)
                            .background(stufenFarbe),
                    )

                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(ArchivTheme.metrik.kartenInnenAbstand),
                        verticalArrangement = Arrangement.spacedBy(10.dp),
                    ) {
                        // Kopfzeile mit Name, Stufe und Schließen-Schaltfläche
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            Row(
                                horizontalArrangement = Arrangement.spacedBy(8.dp),
                                verticalAlignment = Alignment.CenterVertically,
                                modifier = Modifier.weight(1f),
                            ) {
                                Text(
                                    text = wert.bezeichnung,
                                    style = MaterialTheme.typography.titleLarge,
                                    color = farben.tinte,
                                )
                                ArchivStempel(
                                    text = wert.stufenName,
                                    farbe = stufenFarbe,
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
                                    .defaultMinSize(minHeight = 40.dp)
                                    .clip(RoundedCornerShape(3.dp))
                                    .border(1.dp, farben.linieFein, RoundedCornerShape(3.dp))
                                    .clickable(onClick = onSchliessen)
                                    .semantics {
                                        role = Role.Button
                                        contentDescription = "Erklärkarte für ${wert.bezeichnung} schließen"
                                    }
                                    .padding(horizontal = 10.dp, vertical = 6.dp),
                                contentAlignment = Alignment.Center,
                            ) {
                                Text(
                                    text = "Schließen ×",
                                    style = MaterialTheme.typography.labelMedium,
                                    color = farben.tinteMatt,
                                )
                            }
                        }

                        // Balken & Kurzstatus
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
                                text = "${wert.gefuellteSegmente}/${wert.segmenteGesamt} Balken voll · ${wert.stufenKurz}",
                                style = MaterialTheme.typography.bodySmall,
                                color = farben.tinteMatt,
                                modifier = Modifier.weight(1f),
                            )
                        }

                        // Aktueller Zustandssatz als ruhiges Archiv-Zitat
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .background(farben.papier, RoundedCornerShape(3.dp))
                                .border(1.dp, farben.linieFein, RoundedCornerShape(3.dp))
                                .padding(horizontal = 12.dp, vertical = 10.dp),
                        ) {
                            Text(
                                text = "„${wert.zustandssatz}“",
                                style = MaterialTheme.typography.bodyMedium,
                                fontStyle = FontStyle.Italic,
                                color = farben.tinte,
                            )
                        }

                        // Erklärung & Folge aus konfiguration.json
                        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                            Text(
                                text = wert.erklaerung,
                                style = MaterialTheme.typography.bodyMedium,
                                color = farben.tinte,
                            )
                            Text(
                                text = "Auswirkung: ${wert.folge}",
                                style = MaterialTheme.typography.bodySmall,
                                color = if (wert.istKritisch) farben.akzent else farben.tinteMatt,
                                fontWeight = if (wert.istKritisch) FontWeight.SemiBold else FontWeight.Normal,
                            )
                        }
                    }
                }
            }
        }
    }
}
