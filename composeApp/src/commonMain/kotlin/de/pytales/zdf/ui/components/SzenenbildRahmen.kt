package de.pytales.zdf.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import de.pytales.zdf.ui.media.ArchivSzenenBild
import de.pytales.zdf.ui.media.LocalMedienRegister
import de.pytales.zdf.ui.state.SzenenbildUiState
import de.pytales.zdf.ui.theme.ArchivTheme

/**
 * Stimmungsvoll gerahmtes 16:9-Szenenbild (`1280×720`) im Buchdruck-/Skizzenbuch-Passepartout:
 * - Zeigt die Stil-A-Illustration ungestört ohne aufgedruckte Stempel über dem Motiv.
 * - Nutzt [ArchivSzenenBild] mit automatischem Fallback
 *   (`einzelSzenenbild` (Stufe 2) → `schauplatzBild` (Stufe 1) → ruhige Skizzenbuch-Tafel).
 * - Darunter eine ruhige, unaufdringliche Orts-, Jahres- und Pfadangabe.
 */
@Composable
fun SzenenbildRahmen(
    szenenbild: SzenenbildUiState,
    modifier: Modifier = Modifier,
    bildContent: (@Composable BoxScope.(bildId: String, schauplatzBild: String) -> Unit)? = null,
) {
    val farben = ArchivTheme.farben
    val medienRegister = LocalMedienRegister.current
    val rahmenBeschreibung =
        "Szenenbild: ${szenenbild.ort}, ${szenenbild.schauplatzLabel}, Jahr ${szenenbild.jahr}"

    Surface(
        modifier = modifier
            .fillMaxWidth()
            .semantics { contentDescription = rahmenBeschreibung },
        color = farben.papierHell,
        shape = RoundedCornerShape(6.dp),
        border = BorderStroke(0.75.dp, farben.linieFein.copy(alpha = 0.85f)),
        shadowElevation = 2.dp,
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .archivEckenDekor(
                    farbe = farben.linie.copy(alpha = 0.45f),
                    einrueckung = 5.dp,
                    schenkelLaenge = 8.dp,
                )
                .padding(8.dp),
            verticalArrangement = Arrangement.spacedBy(7.dp),
        ) {
            // 16:9 Bildfläche frei von Stempeln über der Illustration
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .aspectRatio(16f / 9f)
                    .clip(RoundedCornerShape(3.dp))
                    .background(farben.papier),
            ) {
                if (bildContent != null) {
                    bildContent(szenenbild.bildId, szenenbild.schauplatzBild)
                } else {
                    ArchivSzenenBild(
                        bildId = szenenbild.bildId,
                        schauplatzBild = szenenbild.schauplatzBild,
                        beschreibung = rahmenBeschreibung,
                        medienRegister = medienRegister,
                    ) {
                        Canvas(modifier = Modifier.fillMaxSize()) {
                            val w = size.width
                            val h = size.height
                            val inset = 12.dp.toPx()
                            val eckLaenge = 12.dp.toPx()

                            drawRect(
                                color = farben.linieFein.copy(alpha = 0.55f),
                                topLeft = Offset(inset, inset),
                                size = Size(w - 2 * inset, h - 2 * inset),
                                style = Stroke(width = 0.9f),
                            )

                            val markenFarbe = farben.akzentMatt.copy(alpha = 0.55f)
                            val strich = 1.25f
                            drawLine(markenFarbe, Offset(inset, inset), Offset(inset + eckLaenge, inset), strich)
                            drawLine(markenFarbe, Offset(inset, inset), Offset(inset, inset + eckLaenge), strich)
                            drawLine(markenFarbe, Offset(w - inset - eckLaenge, inset), Offset(w - inset, inset), strich)
                            drawLine(markenFarbe, Offset(w - inset, inset), Offset(w - inset, inset + eckLaenge), strich)
                            drawLine(markenFarbe, Offset(inset, h - inset), Offset(inset + eckLaenge, h - inset), strich)
                            drawLine(markenFarbe, Offset(inset, h - inset - eckLaenge), Offset(inset, h - inset), strich)
                            drawLine(markenFarbe, Offset(w - inset - eckLaenge, h - inset), Offset(w - inset, h - inset), strich)
                            drawLine(markenFarbe, Offset(w - inset, h - inset - eckLaenge), Offset(w - inset, h - inset), strich)

                            val horizontY = h * 0.70f
                            drawLine(
                                color = farben.linieFein.copy(alpha = 0.45f),
                                start = Offset(inset * 2.2f, horizontY),
                                end = Offset(w - inset * 2.2f, horizontY),
                                strokeWidth = 0.85f,
                            )
                        }

                        Column(
                            modifier = Modifier
                                .align(Alignment.Center)
                                .padding(horizontal = 24.dp),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.spacedBy(4.dp),
                        ) {
                            Text(
                                text = szenenbild.jahr.toString(),
                                style = MaterialTheme.typography.labelMedium,
                                fontFamily = FontFamily.Serif,
                                color = farben.akzent,
                                textAlign = TextAlign.Center,
                            )
                            Text(
                                text = szenenbild.ort,
                                style = MaterialTheme.typography.headlineSmall,
                                color = farben.tinte,
                                textAlign = TextAlign.Center,
                                maxLines = 2,
                                overflow = TextOverflow.Ellipsis,
                            )
                            Text(
                                text = szenenbild.schauplatzLabel,
                                style = MaterialTheme.typography.bodySmall,
                                fontFamily = FontFamily.Serif,
                                fontStyle = FontStyle.Italic,
                                color = farben.tinteMatt,
                                textAlign = TextAlign.Center,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis,
                            )
                        }
                    }
                }
            }

            // Ruhige Bildunterschrift unter dem Passepartout
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 4.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = "${szenenbild.ort} · ${szenenbild.jahr}",
                    style = MaterialTheme.typography.bodySmall,
                    fontFamily = FontFamily.Serif,
                    fontStyle = FontStyle.Italic,
                    color = farben.tinte,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f),
                )
                Text(
                    text = szenenbild.pfadMarke,
                    style = MaterialTheme.typography.labelSmall,
                    color = farben.tinteMatt,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
            }
        }
    }
}
