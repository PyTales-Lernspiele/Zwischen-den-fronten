package de.pytales.zdf.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import de.pytales.zdf.ui.media.ArchivSzenenBild
import de.pytales.zdf.ui.media.BildAufloeser
import de.pytales.zdf.ui.media.LocalMedienRegister
import de.pytales.zdf.ui.state.SzenenbildUiState
import de.pytales.zdf.ui.theme.ArchivTheme

/**
 * Ruhiger 16:9-Szenenbild-Rahmen (`1280×720` gemäß `content/medienplan.json`):
 * - Zeigt Ortsangabe, Schauplatz-Tag, Jahr und die aufgelöste Illustration.
 * - Nutzt standardmäßig [ArchivSzenenBild] mit automatischem Fallback
 *   (`einzelSzenenbild` (Stufe 2) → `schauplatzBild` (Stufe 1) → Archiv-Platzhalter);
 *   über [bildContent] lässt sich die Bildfläche bei Bedarf gezielt überschreiben.
 */
@Composable
fun SzenenbildRahmen(
    szenenbild: SzenenbildUiState,
    modifier: Modifier = Modifier,
    analyseModus: Boolean = false,
    bildContent: (@Composable BoxScope.(bildId: String, schauplatzBild: String) -> Unit)? = null,
) {
    val farben = ArchivTheme.farben
    val medienRegister = LocalMedienRegister.current
    val aufgeloest = remember(szenenbild.bildId, szenenbild.schauplatzBild, medienRegister) {
        BildAufloeser.loeseSzene(
            bildId = szenenbild.bildId,
            schauplatzBild = szenenbild.schauplatzBild,
            verfuegbareIds = medienRegister.verfuegbareIds,
        )
    }
    val rahmenBeschreibung =
        "Szenenbild: ${szenenbild.ort}, Schauplatz ${szenenbild.schauplatzLabel}, Jahr ${szenenbild.jahr}"

    Surface(
        modifier = modifier
            .fillMaxWidth()
            .semantics { contentDescription = rahmenBeschreibung },
        color = farben.papierDunkel,
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(1.dp, farben.linie),
    ) {
        Column(modifier = Modifier.fillMaxWidth()) {
            // 16:9 Bildfläche
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .aspectRatio(16f / 9f)
                    .padding(6.dp)
                    .clip(RoundedCornerShape(2.dp))
                    .background(farben.papier)
                    .border(1.dp, farben.linieFein, RoundedCornerShape(2.dp)),
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
                        // Ruhiger Archiv-Passepartout-Platzhalter als Fallback, falls weder Stufe 2 noch Stufe 1 vorliegt
                        Canvas(modifier = Modifier.fillMaxSize()) {
                            val w = size.width
                            val h = size.height
                            val inset = 10.dp.toPx()
                            val eckLaenge = 14.dp.toPx()

                            // Zarter innerer Rahmen
                            drawRect(
                                color = farben.linieFein.copy(alpha = 0.7f),
                                topLeft = Offset(inset, inset),
                                size = Size(w - 2 * inset, h - 2 * inset),
                                style = Stroke(width = 1f),
                            )

                            // Dezente Archiv-Passermarken an den vier Ecken
                            val markenFarbe = farben.linie.copy(alpha = 0.85f)
                            val strich = 1.5f
                            drawLine(markenFarbe, Offset(inset, inset), Offset(inset + eckLaenge, inset), strich)
                            drawLine(markenFarbe, Offset(inset, inset), Offset(inset, inset + eckLaenge), strich)
                            drawLine(markenFarbe, Offset(w - inset - eckLaenge, inset), Offset(w - inset, inset), strich)
                            drawLine(markenFarbe, Offset(w - inset, inset), Offset(w - inset, inset + eckLaenge), strich)
                            drawLine(markenFarbe, Offset(inset, h - inset), Offset(inset + eckLaenge, h - inset), strich)
                            drawLine(markenFarbe, Offset(inset, h - inset - eckLaenge), Offset(inset, h - inset), strich)
                            drawLine(
                                markenFarbe,
                                Offset(w - inset - eckLaenge, h - inset),
                                Offset(w - inset, h - inset),
                                strich,
                            )
                            drawLine(
                                markenFarbe,
                                Offset(w - inset, h - inset - eckLaenge),
                                Offset(w - inset, h - inset),
                                strich,
                            )

                            // Sehr ruhige Horizont- und Rahmenlinien als Bildkompositions-Anhaltspunkt
                            val horizontY = h * 0.68f
                            drawLine(
                                color = farben.linieFein.copy(alpha = 0.55f),
                                start = Offset(inset * 2f, horizontY),
                                end = Offset(w - inset * 2f, horizontY),
                                strokeWidth = 1f,
                            )
                        }

                        // Mittige ruhige Archiv-Beschriftung
                        Column(
                            modifier = Modifier
                                .align(Alignment.Center)
                                .padding(horizontal = 24.dp),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.spacedBy(4.dp),
                        ) {
                            Text(
                                text = szenenbild.ort,
                                style = MaterialTheme.typography.headlineSmall,
                                color = farben.tinte,
                                textAlign = TextAlign.Center,
                                maxLines = 2,
                                overflow = TextOverflow.Ellipsis,
                            )
                            Text(
                                text = "${szenenbild.pfadMarke} · ${szenenbild.jahr}",
                                style = MaterialTheme.typography.bodySmall,
                                fontStyle = FontStyle.Italic,
                                color = farben.tinteMatt,
                                textAlign = TextAlign.Center,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis,
                            )
                            Text(
                                text = "Archivtafel · ${szenenbild.schauplatzLabel}",
                                style = MaterialTheme.typography.labelSmall,
                                color = farben.linie,
                                textAlign = TextAlign.Center,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis,
                            )
                        }
                    }
                }

                // Schauplatz-Tag oben links + Orts-/Jahres-Tag oben rechts
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .align(Alignment.TopStart)
                        .padding(14.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    ArchivStempel(
                        text = szenenbild.schauplatzLabel,
                        farbe = farben.tinte,
                        hintergrund = farben.papierHell.copy(alpha = 0.92f),
                    )
                    ArchivStempel(
                        text = "${szenenbild.ort} · ${szenenbild.jahr}",
                        farbe = farben.tinteMatt,
                        hintergrund = farben.papierHell.copy(alpha = 0.92f),
                    )
                }
            }

            // Untere Bildregister-Zeile (im Analysemodus inkl. aufgelöster Stufe & Fallback-Quelle)
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(if (analyseModus) farben.papier else farben.papierDunkel)
                    .padding(horizontal = 12.dp, vertical = 6.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = if (analyseModus) {
                        val ziel = aufgeloest.aufgeloesteId ?: "Platzhalter"
                        "Bild: ${szenenbild.bildId} → $ziel (${aufgeloest.ebene.kurzLabel})"
                    } else {
                        "${szenenbild.ort} · ${szenenbild.pfadMarke}"
                    },
                    style = MaterialTheme.typography.labelSmall,
                    color = if (analyseModus) farben.tinte else farben.tinteMatt,
                    fontWeight = if (analyseModus) FontWeight.SemiBold else FontWeight.Normal,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f),
                )
                Text(
                    text = if (analyseModus) {
                        "Fallback: ${szenenbild.schauplatzBild}"
                    } else {
                        "${szenenbild.schauplatzLabel} · ${szenenbild.jahr}"
                    },
                    style = MaterialTheme.typography.labelSmall,
                    color = farben.tinteMatt,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
            }
        }
    }
}
