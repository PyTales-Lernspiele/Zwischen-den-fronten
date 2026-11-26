package de.pytales.zdf.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.tween
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import de.pytales.zdf.model.Stimmung
import de.pytales.zdf.ui.media.ArchivPortraitBild
import de.pytales.zdf.ui.media.BildAufloeser
import de.pytales.zdf.ui.media.LocalMedienRegister
import de.pytales.zdf.ui.state.LiveEmotionUiState
import de.pytales.zdf.ui.theme.ArchivFarben
import de.pytales.zdf.ui.theme.ArchivTheme

/**
 * Live-Emotions-Kachel rechts oben:
 * - Reagiert live auf `GameEngine.liveEmotion(state)` (`neutral`, `hungrig`, `erschoepft`, `angst`, `einsam`).
 * - Zeigt Name, Stand, Pfad und aktuelle Stimmung der Figur.
 * - Lädt standardmäßig die Rollen-Portraits (`portrait_<herkunft>_<geschlecht>_<stimmung>`, WebP)
 *   über [ArchivPortraitBild] mit automatischem Basis-Portrait- und Archiv-Platzhalter-Fallback;
 *   über den optionalen [portraitContent]-Slot lässt sich die Darstellung gezielt überschreiben.
 */
@Composable
fun LiveEmotionsKachel(
    emotion: LiveEmotionUiState,
    modifier: Modifier = Modifier,
    aufDunkel: Boolean = true,
    kompakt: Boolean = false,
    detailsOffen: Boolean = false,
    onTippen: (() -> Unit)? = null,
    portraitGroesse: Dp = ArchivTheme.metrik.portraitGroesse,
    portraitContent: (@Composable BoxScope.(portraitId: String) -> Unit)? = null,
) {
    val farben = ArchivTheme.farben
    val stimmungsFarbe by animateColorAsState(
        targetValue = stimmungsAkzentFarbe(
            stimmung = emotion.stimmung,
            hoechsteStufe = emotion.hoechsteStufe,
            farben = farben,
            aufDunkel = aufDunkel,
        ),
        animationSpec = tween(durationMillis = 250),
        label = "stimmungsFarbe",
    )

    val hintergrund = if (aufDunkel) farben.dunkelHell else farben.papierHell
    val rahmen = when {
        detailsOffen -> stimmungsFarbe
        aufDunkel -> farben.segmentDunkel
        else -> farben.linie
    }
    val titelFarbe = if (aufDunkel) farben.textHell else farben.tinte
    val nebenFarbe = if (aufDunkel) farben.textHell.copy(alpha = 0.76f) else farben.tinteMatt

    val semantikText = buildString {
        append("${emotion.personName}, ${emotion.stand}, ${emotion.pfadMarke}. ")
        append("Aktuelle Stimmung: ${emotion.stimmungBezeichnung}")
        if (emotion.ausloeserBezeichnung != null) {
            append(" (${emotion.ausloeserBezeichnung})")
        }
        append(".")
    }

    val klickModifier = if (onTippen != null) {
        Modifier
            .clickable(onClick = onTippen)
            .semantics {
                role = Role.Button
                selected = detailsOffen
                contentDescription = semantikText
            }
    } else {
        Modifier.semantics {
            contentDescription = semantikText
        }
    }

    Surface(
        modifier = modifier
            .defaultMinSize(minHeight = ArchivTheme.metrik.minTouchHoehe)
            .clip(RoundedCornerShape(4.dp))
            .then(klickModifier),
        color = hintergrund,
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(if (detailsOffen) 1.5.dp else 1.dp, rahmen),
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            ArchivPortraitRahmen(
                emotion = emotion,
                stimmungsFarbe = stimmungsFarbe,
                groesse = portraitGroesse,
                aufDunkel = aufDunkel,
                portraitContent = portraitContent,
            )

            Column(
                modifier = Modifier.weight(1f, fill = !kompakt),
                verticalArrangement = Arrangement.spacedBy(2.dp),
            ) {
                Text(
                    text = emotion.personName,
                    style = MaterialTheme.typography.titleSmall,
                    color = titelFarbe,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
                Text(
                    text = "${emotion.stand} · ${emotion.pfadMarke}",
                    style = MaterialTheme.typography.bodySmall,
                    color = nebenFarbe,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )

                Row(
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Box(
                        modifier = Modifier
                            .size(8.dp)
                            .clip(CircleShape)
                            .background(stimmungsFarbe),
                    )
                    Text(
                        text = buildString {
                            append(emotion.stimmungBezeichnung)
                            if (!kompakt && emotion.ausloeserBezeichnung != null) {
                                append(" · ${emotion.ausloeserBezeichnung}")
                            }
                        },
                        style = MaterialTheme.typography.labelSmall,
                        color = stimmungsFarbe,
                        fontWeight = FontWeight.SemiBold,
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
    val innenFlaeche = if (aufDunkel) farben.dunkel else farben.papierDunkel
    val silhouettenFarbe = if (aufDunkel) {
        farben.textHell.copy(alpha = 0.24f)
    } else {
        farben.tinte.copy(alpha = 0.20f)
    }
    val rahmenLinie = if (aufDunkel) farben.linie.copy(alpha = 0.55f) else farben.linie

    Box(
        modifier = modifier
            .size(groesse)
            .clip(RoundedCornerShape(3.dp))
            .background(innenFlaeche)
            .border(1.dp, stimmungsFarbe.copy(alpha = 0.78f), RoundedCornerShape(3.dp)),
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
                // Ruhiger, würdiger Archiv-Portrait-Platzhalter als Fallback
                Canvas(modifier = Modifier.fillMaxSize()) {
                    val w = size.width
                    val h = size.height
                    val rand = w * 0.08f

                    // Feiner innerer Passepartout-Rahmen
                    drawRect(
                        color = rahmenLinie,
                        topLeft = Offset(rand, rand),
                        size = Size(w - 2 * rand, h - 2 * rand),
                        style = Stroke(width = 1f),
                    )

                    // Dezente Büsten-Silhouette (Kopf + Schulterbogen, ruhig und zeitlos)
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

                    // Feiner Stimmungs-Akzentbalken am unteren Bildrand
                    drawRect(
                        color = stimmungsFarbe.copy(alpha = 0.85f),
                        topLeft = Offset(0f, h - 3.dp.toPx()),
                        size = Size(w, 3.dp.toPx()),
                    )
                }

                // Ruhiges Monogramm über dem historischen Passepartout
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
 * Aufklappbare Detailkarte zur Live-Emotions-Kachel (zeigt vergrößertes Portrait, Herkunft,
 * Zustandssatz und im Analysemodus die exakte Portrait-Asset-Auflösung).
 */
@Composable
fun LiveEmotionDetailKarte(
    emotion: LiveEmotionUiState,
    sichtbar: Boolean,
    analyseModus: Boolean,
    onSchliessen: () -> Unit,
    modifier: Modifier = Modifier,
    portraitContent: (@Composable BoxScope.(portraitId: String) -> Unit)? = null,
) {
    AnimatedVisibility(
        visible = sichtbar,
        enter = fadeIn() + expandVertically(),
        exit = fadeOut() + shrinkVertically(),
        modifier = modifier,
    ) {
        val farben = ArchivTheme.farben
        val medienRegister = LocalMedienRegister.current
        val aufgeloest = remember(emotion.portraitId, medienRegister) {
            BildAufloeser.loesePortrait(emotion.portraitId, medienRegister.verfuegbareIds)
        }
        val akzent = stimmungsAkzentFarbe(
            stimmung = emotion.stimmung,
            hoechsteStufe = emotion.hoechsteStufe,
            farben = farben,
            aufDunkel = false,
        )

        Surface(
            modifier = Modifier.fillMaxWidth(),
            color = farben.papierHell,
            shape = RoundedCornerShape(4.dp),
            border = BorderStroke(1.dp, farben.linie),
            shadowElevation = 2.dp,
        ) {
            Column(modifier = Modifier.fillMaxWidth()) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(3.dp)
                        .background(akzent),
                )
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(ArchivTheme.metrik.kartenInnenAbstand),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        ArchivPortraitRahmen(
                            emotion = emotion,
                            stimmungsFarbe = akzent,
                            groesse = 64.dp,
                            aufDunkel = false,
                            portraitContent = portraitContent,
                        )
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = emotion.personName,
                                style = MaterialTheme.typography.titleLarge,
                                color = farben.tinte,
                            )
                            Text(
                                text = "${emotion.herkunftTitel} · ${emotion.stand} · ${emotion.pfadMarke}",
                                style = MaterialTheme.typography.bodySmall,
                                color = farben.tinteMatt,
                            )
                        }
                        Box(
                            modifier = Modifier
                                .defaultMinSize(minHeight = 40.dp)
                                .clip(RoundedCornerShape(3.dp))
                                .border(1.dp, farben.linieFein, RoundedCornerShape(3.dp))
                                .clickable(onClick = onSchliessen)
                                .semantics {
                                    role = Role.Button
                                    contentDescription = "Figuren-Ansicht schließen"
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

                    Row(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        ArchivStempel(
                            text = "Stimmung: ${emotion.stimmungBezeichnung}",
                            farbe = akzent,
                        )
                        Text(
                            text = emotion.stimmungKurzhinweis,
                            style = MaterialTheme.typography.bodySmall,
                            color = farben.tinteMatt,
                        )
                    }

                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(farben.papier, RoundedCornerShape(3.dp))
                            .border(1.dp, farben.linieFein, RoundedCornerShape(3.dp))
                            .padding(horizontal = 12.dp, vertical = 8.dp),
                    ) {
                        Text(
                            text = "„${emotion.zustandssatz}“",
                            style = MaterialTheme.typography.bodyMedium,
                            fontStyle = FontStyle.Italic,
                            color = farben.tinte,
                        )
                    }

                    if (analyseModus) {
                        val zielHinweis = when {
                            aufgeloest.aufgeloesteId == null -> "Archiv-Platzhalter"
                            aufgeloest.aufgeloesteId == emotion.portraitId -> aufgeloest.ebene.kurzLabel
                            else -> "→ ${aufgeloest.aufgeloesteId} (${aufgeloest.ebene.kurzLabel})"
                        }
                        Text(
                            text = "Portrait-Asset: ${emotion.portraitId} · $zielHinweis",
                            style = MaterialTheme.typography.labelSmall,
                            color = farben.tinteMatt,
                        )
                    }
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
