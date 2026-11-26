package de.pytales.zdf.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
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
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.ArchivUebergaenge
import de.pytales.zdf.ui.theme.Schriftgroesse

/**
 * Verleiht dem Archivpapier-Hintergrund eine sehr sanfte, warme Papier-Vignette
 * (wie ein aufgeschlagenes historisches Skizzenbuch), ohne Unruhe oder Kontrastverlust.
 */
@Composable
fun Modifier.archivPapierHintergrund(): Modifier {
    val farben = ArchivTheme.farben
    return this
        .background(farben.papier)
        .drawBehind {
            val radius = (size.maxDimension * 0.78f).coerceAtLeast(1f)
            drawRect(
                brush = Brush.radialGradient(
                    colors = listOf(
                        farben.papierHell.copy(alpha = 0.42f),
                        Color.Transparent,
                        farben.papierDunkel.copy(alpha = 0.34f),
                    ),
                    center = Offset(size.width * 0.5f, size.height * 0.42f),
                    radius = radius,
                ),
            )
        }
}

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
    segmentAbstand: Dp = 2.5.dp,
) {
    val gesamt = segmenteGesamt.coerceAtLeast(1)
    val gefuellt = gefuellteSegmente.coerceIn(0, gesamt)
    val animierteFarbe by animateColorAsState(
        targetValue = aktiveFarbe,
        animationSpec = ArchivUebergaenge.farbSpec(ArchivTheme.reduzierteAnimationen),
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
                    .clip(RoundedCornerShape(2.dp))
                    .background(if (istGefuellt) animierteFarbe else leereFarbe),
            )
        }
    }
}

/**
 * Zurückhaltende Archiv-Marke (z. B. für Risikohinweise wie „gegen die Vorschrift“,
 * Wirkungs-Deltas oder Datumsangaben). Bewusst leise und ohne grellen Stempel-Look.
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
                border = BorderStroke(0.75.dp, farbe.copy(alpha = 0.36f)),
                shape = RoundedCornerShape(4.dp),
            )
            .background(color = hintergrund, shape = RoundedCornerShape(4.dp))
            .padding(horizontal = 8.dp, vertical = 2.5.dp),
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
 * Feine Buchdruck-Haarlinie (einfach oder doppelt für Zeitungs- und Behördenköpfe).
 */
@Composable
fun ArchivTrennlinie(
    modifier: Modifier = Modifier,
    farbe: Color = ArchivTheme.farben.linieFein.copy(alpha = 0.72f),
    doppelt: Boolean = false,
) {
    Column(
        modifier = modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(2.dp),
    ) {
        HorizontalDivider(
            thickness = if (doppelt) 1.5.dp else 0.75.dp,
            color = farbe,
        )
        if (doppelt) {
            HorizontalDivider(
                thickness = 0.65.dp,
                color = farbe.copy(alpha = 0.65f),
            )
        }
    }
}

/**
 * Feine dekorative Buchdruck-Zierlinie mit zarter mittiger Raute für ruhige Abschnittstrenner.
 */
@Composable
fun ArchivZierLinie(
    modifier: Modifier = Modifier,
    farbe: Color = ArchivTheme.farben.linieFein,
    akzentFarbe: Color = ArchivTheme.farben.akzent.copy(alpha = 0.65f),
) {
    Canvas(
        modifier = modifier
            .fillMaxWidth()
            .height(10.dp),
    ) {
        val cy = size.height / 2f
        val cx = size.width / 2f
        val raute = 3.dp.toPx()
        val luecke = 9.dp.toPx()
        val strich = 0.75.dp.toPx()

        if (cx > luecke) {
            drawLine(
                brush = Brush.horizontalGradient(
                    colors = listOf(Color.Transparent, farbe.copy(alpha = 0.75f)),
                    startX = 0f,
                    endX = cx - luecke,
                ),
                start = Offset(0f, cy),
                end = Offset(cx - luecke, cy),
                strokeWidth = strich,
            )
            drawLine(
                brush = Brush.horizontalGradient(
                    colors = listOf(farbe.copy(alpha = 0.75f), Color.Transparent),
                    startX = cx + luecke,
                    endX = size.width,
                ),
                start = Offset(cx + luecke, cy),
                end = Offset(size.width, cy),
                strokeWidth = strich,
            )
        }

        val pfad = Path().apply {
            moveTo(cx, cy - raute)
            lineTo(cx + raute, cy)
            lineTo(cx, cy + raute)
            lineTo(cx - raute, cy)
            close()
        }
        drawPath(path = pfad, color = akzentFarbe)
    }
}

/**
 * Zeichnet feine Tusche-Eckzierden in die vier Ecken eines Bild-Passepartouts
 * (angelehnt an historische Buch- und Skizzenbuch-Tafeln).
 */
fun Modifier.archivEckenDekor(
    farbe: Color,
    einrueckung: Dp = 5.dp,
    schenkelLaenge: Dp = 10.dp,
): Modifier = this.drawBehind {
    val inset = einrueckung.toPx()
    val len = schenkelLaenge.toPx()
    val stroke = 1.dp.toPx()
    val w = size.width
    val h = size.height
    if (w <= inset * 2 + len || h <= inset * 2 + len) return@drawBehind

    // Oben links
    drawLine(farbe, Offset(inset, inset), Offset(inset + len, inset), stroke)
    drawLine(farbe, Offset(inset, inset), Offset(inset, inset + len), stroke)
    // Oben rechts
    drawLine(farbe, Offset(w - inset - len, inset), Offset(w - inset, inset), stroke)
    drawLine(farbe, Offset(w - inset, inset), Offset(w - inset, inset + len), stroke)
    // Unten links
    drawLine(farbe, Offset(inset, h - inset), Offset(inset + len, h - inset), stroke)
    drawLine(farbe, Offset(inset, h - inset - len), Offset(inset, h - inset), stroke)
    // Unten rechts
    drawLine(farbe, Offset(w - inset - len, h - inset), Offset(w - inset, h - inset), stroke)
    drawLine(farbe, Offset(w - inset, h - inset - len), Offset(w - inset, h - inset), stroke)
}

/**
 * Dreistufiger Umschalter für die Schriftgröße (`Klein`, `Mittel`, `Groß`).
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
    val minTouch = ArchivTheme.metrik.minTouchHoehe
    val rahmenFarbe = if (aufDunkel) farben.linie.copy(alpha = 0.55f) else farben.linieFein
    val hintergrund = if (aufDunkel) farben.dunkelHell else farben.papier
    val aktivHintergrund = if (aufDunkel) farben.akzent else farben.tinte
    val aktivText = farben.papierHell
    val inaktivText = if (aufDunkel) farben.textHell else farben.tinte

    Surface(
        modifier = modifier.archivFokusGruppe(),
        color = hintergrund,
        shape = RoundedCornerShape(6.dp),
        border = BorderStroke(0.75.dp, rahmenFarbe),
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Schriftgroesse.entries.forEach { stufe ->
                val istAktiv = stufe == aktuell
                Box(
                    modifier = Modifier
                        .weight(1f, fill = !kompakt)
                        .defaultMinSize(
                            minWidth = if (kompakt) minTouch else 72.dp,
                            minHeight = minTouch,
                        )
                        .clip(RoundedCornerShape(5.dp))
                        .background(if (istAktiv) aktivHintergrund else Color.Transparent)
                        .archivFokusRahmen(eckRadius = 5.dp, aufDunkel = aufDunkel)
                        .clickable { onAuswahl(stufe) }
                        .semantics {
                            role = Role.RadioButton
                            selected = istAktiv
                            stateDescription = if (istAktiv) "Ausgewählt" else "Nicht ausgewählt"
                            contentDescription = "Schriftgröße ${stufe.bezeichnung}: ${stufe.beschreibung}"
                        }
                        .padding(horizontal = if (kompakt) 10.dp else 14.dp, vertical = 8.dp),
                    contentAlignment = Alignment.Center,
                ) {
                    Text(
                        text = if (kompakt) stufe.kurzZeichen else "${stufe.kurzZeichen}  ${stufe.bezeichnung}",
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
