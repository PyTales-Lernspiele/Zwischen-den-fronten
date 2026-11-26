package de.pytales.zdf.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
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
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import de.pytales.zdf.audio.SoundEffekt
import de.pytales.zdf.model.Stimmung
import de.pytales.zdf.ui.media.ArchivPortraitBild
import de.pytales.zdf.ui.state.LiveEmotionUiState
import de.pytales.zdf.ui.theme.ArchivFarben
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.ArchivUebergaenge
import de.pytales.zdf.ui.theme.LocalSoundEffektSpielen

/**
 * Flache, unaufdringliche Live-Emotions-Kachel rechts oben in der Kopfleiste:
 * - Reagiert live auf `GameEngine.liveEmotion(state)` (`neutral`, `hungrig`, `erschoepft`, `angst`, `einsam`).
 * - Zeigt das Stil-A-Portrait (`portrait_<herkunft>_<geschlecht>_<stimmung>`, WebP)
 *   über [ArchivPortraitBild] — direkt auf der Leiste ohne überflüssigen äußeren Kastenrahmen.
 * - Bei [nurPortrait] = true zeigt sie platzsparend nur das gerahmte Portrait mit Stimmungs-Akzent;
 *   Tippen öffnet stets die volle ruhige Figuren-Ansicht als Overlay.
 */
@Composable
fun LiveEmotionsKachel(
    emotion: LiveEmotionUiState,
    modifier: Modifier = Modifier,
    aufDunkel: Boolean = true,
    kompakt: Boolean = false,
    nurPortrait: Boolean = false,
    detailsOffen: Boolean = false,
    onTippen: (() -> Unit)? = null,
    portraitGroesse: Dp = ArchivTheme.metrik.portraitGroesse,
    portraitContent: (@Composable BoxScope.(portraitId: String) -> Unit)? = null,
) {
    val farben = ArchivTheme.farben
    val reduziert = ArchivTheme.reduzierteAnimationen
    val spieleEffekt = LocalSoundEffektSpielen.current
    val stimmungsFarbe by animateColorAsState(
        targetValue = stimmungsAkzentFarbe(
            stimmung = emotion.stimmung,
            hoechsteStufe = emotion.hoechsteStufe,
            farben = farben,
            aufDunkel = aufDunkel,
        ),
        animationSpec = ArchivUebergaenge.farbSpec(reduziert),
        label = "stimmungsFarbe",
    )

    val hintergrund = when {
        detailsOffen && aufDunkel -> farben.dunkelHell
        detailsOffen -> farben.papierDunkel
        else -> Color.Transparent
    }
    val titelFarbe = if (aufDunkel) farben.textHell else farben.tinte

    val semantikText = buildString {
        append("${emotion.personName}, ${emotion.stand}, ${emotion.pfadMarke}. ")
        append("Stimmung: ${emotion.stimmungBezeichnung}")
        if (emotion.ausloeserBezeichnung != null) {
            append(" (${emotion.ausloeserBezeichnung})")
        }
        if (onTippen != null) {
            append(if (detailsOffen) ". Figuren-Ansicht schließen." else ". Tippen für Figuren-Ansicht.")
        } else {
            append(".")
        }
    }

    val klickModifier = if (onTippen != null) {
        Modifier
            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = aufDunkel)
            .clickable {
                spieleEffekt(SoundEffekt.KLICK_SANFT)
                onTippen()
            }
            .clearAndSetSemantics {
                role = Role.Button
                selected = detailsOffen
                stateDescription = if (detailsOffen) "Figuren-Ansicht geöffnet" else "Figuren-Ansicht geschlossen"
                contentDescription = semantikText
            }
    } else {
        Modifier.clearAndSetSemantics {
            contentDescription = semantikText
        }
    }

    Row(
        modifier = modifier
            .defaultMinSize(minWidth = ArchivTheme.metrik.minTouchHoehe, minHeight = ArchivTheme.metrik.minTouchHoehe)
            .clip(RoundedCornerShape(6.dp))
            .background(hintergrund)
            .then(klickModifier)
            .padding(
                horizontal = if (nurPortrait) 4.dp else 6.dp,
                vertical = 3.dp,
            ),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        ArchivPortraitRahmen(
            emotion = emotion,
            stimmungsFarbe = stimmungsFarbe,
            groesse = portraitGroesse,
            aufDunkel = aufDunkel,
            portraitContent = portraitContent,
        )

        if (!nurPortrait) {
            Column(
                modifier = Modifier.weight(1f, fill = !kompakt),
                verticalArrangement = Arrangement.spacedBy(1.dp),
            ) {
                Text(
                    text = emotion.personName,
                    style = MaterialTheme.typography.labelMedium,
                    color = titelFarbe,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )

                Row(
                    horizontalArrangement = Arrangement.spacedBy(5.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Box(
                        modifier = Modifier
                            .size(6.dp)
                            .clip(CircleShape)
                            .background(stimmungsFarbe),
                    )
                    Text(
                        text = emotion.stimmungBezeichnung,
                        style = MaterialTheme.typography.labelSmall,
                        color = stimmungsFarbe,
                        fontWeight = FontWeight.Medium,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                    )
                }
            }
        }
    }
}

/**
 * Quadratischer 1:1-Portraitrahmen (`320×320` WebP) mit automatischem Multiplatform-Loader
 * ([ArchivPortraitBild]) und ruhigem Archiv-Platzhalter als Fallback.
 */
@Composable
fun ArchivPortraitRahmen(
    emotion: LiveEmotionUiState,
    stimmungsFarbe: Color,
    groesse: Dp,
    aufDunkel: Boolean,
    modifier: Modifier = Modifier,
    portraitContent: (@Composable BoxScope.(portraitId: String) -> Unit)? = null,
) {
    val farben = ArchivTheme.farben
    val innenFlaeche = if (aufDunkel) farben.dunkel else farben.papier
    val silhouettenFarbe = if (aufDunkel) {
        farben.textHell.copy(alpha = 0.24f)
    } else {
        farben.tinte.copy(alpha = 0.20f)
    }
    val rahmenLinie = if (aufDunkel) farben.linie.copy(alpha = 0.55f) else farben.linieFein

    Box(
        modifier = modifier
            .size(groesse)
            .clip(RoundedCornerShape(4.dp))
            .background(innenFlaeche)
            .border(1.dp, stimmungsFarbe.copy(alpha = 0.80f), RoundedCornerShape(4.dp)),
        contentAlignment = Alignment.Center,
    ) {
        if (portraitContent != null) {
            portraitContent(emotion.portraitId)
        } else {
            ArchivPortraitBild(
                portraitId = emotion.portraitId,
                stimmungsFarbe = stimmungsFarbe,
                beschreibung = "Portrait von ${emotion.personName} (${emotion.stimmungBezeichnung})",
            ) {
                Canvas(modifier = Modifier.fillMaxSize()) {
                    val w = size.width
                    val h = size.height
                    val rand = w * 0.08f

                    drawRect(
                        color = rahmenLinie,
                        topLeft = Offset(rand, rand),
                        size = Size(w - 2 * rand, h - 2 * rand),
                        style = Stroke(width = 1f),
                    )

                    val kopfRadius = w * 0.16f
                    drawCircle(
                        color = silhouettenFarbe,
                        radius = kopfRadius,
                        center = Offset(w * 0.5f, h * 0.38f),
                    )
                    val schulterPfad = Path().apply {
                        moveTo(w * 0.20f, h * 0.88f)
                        cubicTo(
                            w * 0.24f,
                            h * 0.60f,
                            w * 0.76f,
                            h * 0.60f,
                            w * 0.80f,
                            h * 0.88f,
                        )
                        close()
                    }
                    drawPath(path = schulterPfad, color = silhouettenFarbe)

                    drawRect(
                        color = stimmungsFarbe.copy(alpha = 0.85f),
                        topLeft = Offset(0f, h - 3.dp.toPx()),
                        size = Size(w, 3.dp.toPx()),
                    )
                }

                Text(
                    text = emotion.initialen,
                    style = MaterialTheme.typography.titleSmall,
                    color = if (aufDunkel) farben.textHell.copy(alpha = 0.88f) else farben.tinte.copy(alpha = 0.84f),
                    fontWeight = FontWeight.SemiBold,
                )
            }
        }
    }
}

/**
 * Ruhige Figuren-Detailkarte für die Darstellung im leichten Overlay (ohne Technik-/Asset-IDs).
 */
@Composable
fun LiveEmotionDetailKarte(
    emotion: LiveEmotionUiState,
    onSchliessen: () -> Unit,
    modifier: Modifier = Modifier,
    portraitContent: (@Composable BoxScope.(portraitId: String) -> Unit)? = null,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val spieleEffekt = LocalSoundEffektSpielen.current
    val akzent = stimmungsAkzentFarbe(
        stimmung = emotion.stimmung,
        hoechsteStufe = emotion.hoechsteStufe,
        farben = farben,
        aufDunkel = false,
    )

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
                    .background(akzent),
            )
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 20.dp, vertical = 16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(14.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    ArchivPortraitRahmen(
                        emotion = emotion,
                        stimmungsFarbe = akzent,
                        groesse = 82.dp,
                        aufDunkel = false,
                        portraitContent = portraitContent,
                    )
                    Column(
                        modifier = Modifier.weight(1f),
                        verticalArrangement = Arrangement.spacedBy(3.dp),
                    ) {
                        Text(
                            text = emotion.personName,
                            style = MaterialTheme.typography.headlineSmall,
                            color = farben.tinte,
                            modifier = Modifier.archivUeberschrift(),
                        )
                        Text(
                            text = "${emotion.herkunftTitel} · ${emotion.stand}",
                            style = MaterialTheme.typography.bodySmall,
                            color = farben.tinteMatt,
                        )
                        Row(
                            horizontalArrangement = Arrangement.spacedBy(6.dp),
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(7.dp)
                                    .clip(CircleShape)
                                    .background(akzent),
                            )
                            Text(
                                text = "${emotion.stimmungBezeichnung} · ${emotion.stimmungKurzhinweis}",
                                style = MaterialTheme.typography.labelMedium,
                                color = akzent,
                                fontWeight = FontWeight.Medium,
                            )
                        }
                    }
                    Box(
                        modifier = Modifier
                            .align(Alignment.Top)
                            .defaultMinSize(minWidth = metrik.minTouchHoehe, minHeight = metrik.minTouchHoehe)
                            .clip(RoundedCornerShape(6.dp))
                            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = false)
                            .clickable {
                                spieleEffekt(SoundEffekt.KLICK_SANFT)
                                onSchliessen()
                            }
                            .semantics {
                                role = Role.Button
                                contentDescription = "Figuren-Ansicht schließen"
                            },
                        contentAlignment = Alignment.Center,
                    ) {
                        SchliessenIcon(farbe = farben.tinteMatt, groesse = 18.dp)
                    }
                }

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
                            .background(akzent.copy(alpha = 0.75f)),
                    )
                    Text(
                        text = "„${emotion.zustandssatz}“",
                        style = MaterialTheme.typography.bodyMedium,
                        fontFamily = FontFamily.Serif,
                        fontStyle = FontStyle.Italic,
                        color = farben.tinte,
                        modifier = Modifier.padding(vertical = 2.dp),
                    )
                }
            }
        }
    }
}

internal fun stimmungsAkzentFarbe(
    stimmung: Stimmung,
    hoechsteStufe: Int,
    farben: ArchivFarben,
    aufDunkel: Boolean,
): Color {
    val stufe = when (stimmung) {
        Stimmung.NEUTRAL -> 0
        Stimmung.HUNGRIG,
        Stimmung.ERSCHOEPFT,
        Stimmung.ANGST,
        Stimmung.EINSAM,
        -> hoechsteStufe.coerceIn(2, 4)
    }
    return if (aufDunkel) farben.stufenFarbeHell(stufe) else farben.stufenFarbe(stufe)
}
