package de.pytales.zdf.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.Schriftgroesse

/**
 * Ruhiger 5-Segment-Balken (*voll = gut* gemäß `ValueMetrics`).
 *
 * Gefüllte Segmente links in der Stufenfarbe; leere Segmente rechts im passenden
 * Hintergrundton für helle oder dunkle Flächen.
 */
@Composable
fun FuenfSegmentBalken(
    gefuellteSegmente: Int,
    segmenteGesamt: Int,
    aktiveFarbe: Color,
    leereFarbe: Color,
    modifier: Modifier = Modifier,
    segmentHoehe: Dp = ArchivTheme.metrik.segmentHoehe,
    segmentAbstand: Dp = 3.dp,
) {
    val gesamt = segmenteGesamt.coerceAtLeast(1)
    val gefuellt = gefuellteSegmente.coerceIn(0, gesamt)
    val animierteFarbe by animateColorAsState(
        targetValue = aktiveFarbe,
        animationSpec = tween(durationMillis = 220),
        label = "segmentFarbe",
    )

    Row(
        modifier = modifier
            .fillMaxWidth()
            .semantics {
                contentDescription = "$gefuellt von $gesamt Segmenten gefüllt"
            },
        horizontalArrangement = Arrangement.spacedBy(segmentAbstand),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        for (index in 0 until gesamt) {
            val istGefuellt = index < gefuellt
            Box(
                modifier = Modifier
                    .weight(1f)
                    .height(segmentHoehe)
                    .clip(RoundedCornerShape(1.5.dp))
                    .background(if (istGefuellt) animierteFarbe else leereFarbe),
            )
        }
    }
}

/**
 * Rechteckiger Archiv-Stempel für optionale Risikohinweise (z. B. „gegen die Vorschrift“),
 * Dokumenttypen oder Quellen-Kategorien.
 */
@Composable
fun ArchivStempel(
    text: String,
    modifier: Modifier = Modifier,
    farbe: Color = ArchivTheme.farben.akzent,
    hintergrund: Color = farbe.copy(alpha = 0.08f),
    grossbuchstaben: Boolean = false,
) {
    val anzeige = if (grossbuchstaben) text.uppercase() else text
    Box(
        modifier = modifier
            .border(
                border = BorderStroke(1.dp, farbe.copy(alpha = 0.72f)),
                shape = RoundedCornerShape(2.dp),
            )
            .background(color = hintergrund, shape = RoundedCornerShape(2.dp))
            .padding(horizontal = 7.dp, vertical = 2.dp),
    ) {
        Text(
            text = anzeige,
            style = MaterialTheme.typography.labelSmall,
            color = farbe,
            fontWeight = FontWeight.SemiBold,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
        )
    }
}

/**
 * Dezente einfache oder doppelte Archiv-Trennlinie (z. B. für Zeitungs- und Behördenköpfe).
 */
@Composable
fun ArchivTrennlinie(
    modifier: Modifier = Modifier,
    farbe: Color = ArchivTheme.farben.linieFein,
    doppelt: Boolean = false,
) {
    Column(
        modifier = modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(2.dp),
    ) {
        HorizontalDivider(
            thickness = if (doppelt) 2.dp else 1.dp,
            color = farbe,
        )
        if (doppelt) {
            HorizontalDivider(
                thickness = 0.75.dp,
                color = farbe.copy(alpha = 0.75f),
            )
        }
    }
}

/**
 * Dreistufiger Umschalter für die Schriftgröße (`Klein`, `Mittel`, `Groß`/Beamer).
 * Einsetzbar sowohl auf dunkler Kopfleiste als auch auf hellem Archivpapier.
 */
@Composable
fun SchriftgroessenSchalter(
    aktuell: Schriftgroesse,
    onAuswahl: (Schriftgroesse) -> Unit,
    modifier: Modifier = Modifier,
    aufDunkel: Boolean = false,
    kompakt: Boolean = false,
) {
    val farben = ArchivTheme.farben
    val rahmenFarbe = if (aufDunkel) farben.linie.copy(alpha = 0.65f) else farben.linie
    val hintergrund = if (aufDunkel) farben.dunkelHell else farben.papierHell
    val aktivHintergrund = if (aufDunkel) farben.akzent else farben.tinte
    val aktivText = farben.papierHell
    val inaktivText = if (aufDunkel) farben.textHell else farben.tinte

    Surface(
        modifier = modifier,
        color = hintergrund,
        shape = RoundedCornerShape(3.dp),
        border = BorderStroke(1.dp, rahmenFarbe),
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Schriftgroesse.entries.forEach { stufe ->
                val istAktiv = stufe == aktuell
                Box(
                    modifier = Modifier
                        .defaultMinSize(minWidth = if (kompakt) 40.dp else 52.dp, minHeight = 40.dp)
                        .background(if (istAktiv) aktivHintergrund else Color.Transparent)
                        .clickable { onAuswahl(stufe) }
                        .semantics {
                            role = Role.RadioButton
                            selected = istAktiv
                            contentDescription = "Schriftgröße ${stufe.bezeichnung}: ${stufe.beschreibung}"
                        }
                        .padding(horizontal = if (kompakt) 10.dp else 12.dp, vertical = 6.dp),
                    contentAlignment = Alignment.Center,
                ) {
                    Text(
                        text = if (kompakt) stufe.kurzZeichen else "${stufe.kurzZeichen} ${stufe.bezeichnung}",
                        style = MaterialTheme.typography.labelMedium,
                        color = if (istAktiv) aktivText else inaktivText,
                        fontWeight = if (istAktiv) FontWeight.Bold else FontWeight.Medium,
                        maxLines = 1,
                    )
                }
            }
        }
    }
}
