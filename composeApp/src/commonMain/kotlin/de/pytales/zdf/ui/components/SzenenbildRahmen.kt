package de.pytales.zdf.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.Column
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
 * Stimmungsvoll gerahmte 16:9-Illustration (`1280×720`) im ruhigen Buch-Passepartout
 * mit genau **einer einzigen ruhigen Orts-/Jahreszeile** direkt darunter — frei von
 * Zusatzkästen, Stempeln und Zitat-Balken.
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

    Column(
        modifier = modifier
            .fillMaxWidth()
            .semantics { contentDescription = rahmenBeschreibung },
        verticalArrangement = Arrangement.spacedBy(8.dp),
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

                                drawRect(
                                    color = farben.linieFein.copy(alpha = 0.50f),
                                    topLeft = Offset(inset, inset),
                                    size = Size(w - 2 * inset, h - 2 * inset),
                                    style = Stroke(width = 0.9f),
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
            }
        }

        // Genau eine ruhige Orts- und Jahreszeile unter dem Bild
        Text(
            text = "${szenenbild.ort} · ${szenenbild.jahr}",
            style = MaterialTheme.typography.bodySmall,
            fontFamily = FontFamily.Serif,
            fontStyle = FontStyle.Italic,
            color = farben.tinteMatt,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
            modifier = Modifier.padding(horizontal = 2.dp),
        )
    }
}
