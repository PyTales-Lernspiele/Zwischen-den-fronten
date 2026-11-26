package de.pytales.zdf.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.WindowInsetsSides
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.only
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.layout.windowInsetsTopHeight
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.clearAndSetSemantics
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import de.pytales.zdf.audio.SoundEffekt
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.state.LiveEmotionUiState
import de.pytales.zdf.ui.state.WertKachelUiState
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.ArchivUebergaenge
import de.pytales.zdf.ui.theme.LocalSoundEffektSpielen

/**
 * Ruhige, flache und platzsparende Kopfleiste:
 * - **Aufgeklappt:** Einzeilig, flach und luftig direkt auf der dunklen Leiste ohne Kasten-in-Kasten;
 *   zeigt alle 4 Befindenswerte, das Live-Portrait sowie dezente Symbole für Ton, Einstellungen
 *   und Einklappen.
 * - **Eingeklappt:** Verschwindet vollständig nach oben (0 dp Inhalts-Höhe, keine permanente
 *   Seitenleiste!), sodass die gesamte Bildschirmbreite und -höhe frei für das aufgeschlagene
 *   Archivbuch bleibt. Über eine einzige dezente Ecke/Lasche oben rechts ([KopfLeisteLasche])
 *   lässt sich die Leiste jederzeit mit einem Tippen auf- und wieder zuklappen.
 * - **Erklärkarten:** Öffnen stets als ruhiges Overlay ohne Seitenverschiebung.
 */
@Composable
fun KopfLeiste(
    jahr: Int,
    werte: List<WertKachelUiState>,
    emotion: LiveEmotionUiState,
    modifier: Modifier = Modifier,
    eingeklappt: Boolean = false,
    onEingeklapptToggle: (() -> Unit)? = null,
    ausgewaehlterWert: WertSchluessel? = null,
    onAusgewaehlterWertChange: ((WertSchluessel?) -> Unit)? = null,
    emotionDetailsOffen: Boolean? = null,
    onEmotionDetailsOffenChange: ((Boolean) -> Unit)? = null,
    zusatzAktionen: (@Composable () -> Unit)? = null,
    portraitContent: (@Composable BoxScope.(portraitId: String) -> Unit)? = null,
) {
    var internerWert by remember { mutableStateOf<WertSchluessel?>(null) }
    var internEmotionOffen by remember { mutableStateOf(false) }

    val aktiverWertSchluessel = if (onAusgewaehlterWertChange != null) {
        ausgewaehlterWert
    } else {
        internerWert
    }
    val aktiveEmotionOffen = if (onEmotionDetailsOffenChange != null && emotionDetailsOffen != null) {
        emotionDetailsOffen
    } else {
        internEmotionOffen
    }

    val setzeEmotionOffen: (Boolean) -> Unit = { offen ->
        if (offen) {
            if (onAusgewaehlterWertChange != null) {
                onAusgewaehlterWertChange(null)
            } else {
                internerWert = null
            }
        }
        if (onEmotionDetailsOffenChange != null) {
            onEmotionDetailsOffenChange(offen)
        } else {
            internEmotionOffen = offen
        }
    }

    val setzeWert: (WertSchluessel?) -> Unit = { neu ->
        if (neu != null) {
            if (onEmotionDetailsOffenChange != null) {
                onEmotionDetailsOffenChange(false)
            } else {
                internEmotionOffen = false
            }
        }
        if (onAusgewaehlterWertChange != null) {
            onAusgewaehlterWertChange(neu)
        } else {
            internerWert = neu
        }
    }

    val ausgewaehlterStatus = werte.firstOrNull { it.schluessel == aktiverWertSchluessel }
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val reduziert = ArchivTheme.reduzierteAnimationen
    val detailOffen = ausgewaehlterStatus != null || aktiveEmotionOffen
    val istQuerformat = metrik.kopfNebeneinander

    if (onAusgewaehlterWertChange == null && onEmotionDetailsOffenChange == null) {
        PlattformZurueckHandler(aktiv = detailOffen) {
            setzeWert(null)
            setzeEmotionOffen(false)
        }
    }

    Column(
        modifier = modifier
            .fillMaxWidth()
            .archivFokusGruppe()
            .archivEscapeAktion(aktiv = detailOffen) {
                setzeWert(null)
                setzeEmotionOffen(false)
            },
    ) {
        if (eingeklappt) {
            // Eingeklappt: 0 dp Inhalts-Höhe — nur Statusbar-Fläche + hauchfeine Trennlinie
            Spacer(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(farben.dunkel)
                    .windowInsetsTopHeight(WindowInsets.safeDrawing),
            )
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(1.dp)
                    .background(farben.linie.copy(alpha = 0.45f)),
            )
        } else {
            // Dunkle Haupt-Kopfleiste (randabfallend hinter Statusbar & Notch, innen flach & luftig)
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(farben.dunkel),
                contentAlignment = Alignment.Center,
            ) {
                BoxWithConstraints(
                    modifier = Modifier
                        .fillMaxWidth()
                        .windowInsetsPadding(
                            WindowInsets.safeDrawing.only(WindowInsetsSides.Top + WindowInsetsSides.Horizontal),
                        )
                        .widthIn(max = metrik.maxInhaltsBreite)
                        .padding(
                            horizontal = metrik.aussenAbstand,
                            vertical = if (metrik.kompakteHoehe) 2.dp else 5.dp,
                        ),
                ) {
                    val verfuegbareBreite = maxWidth

                    if (istQuerformat) {
                        val zeigeJahrLinks = verfuegbareBreite >= 860.dp
                        val nurPortrait = verfuegbareBreite < 780.dp
                        val werteSchlank = metrik.kompakteHoehe || verfuegbareBreite < 960.dp

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(if (werteSchlank) 8.dp else 14.dp),
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            if (zeigeJahrLinks) {
                                Text(
                                    text = jahr.toString(),
                                    style = MaterialTheme.typography.titleMedium,
                                    fontFamily = FontFamily.Serif,
                                    color = farben.stufenFarbeHell(2),
                                    fontWeight = FontWeight.Bold,
                                )
                            }

                            BefindensLeiste(
                                werte = werte,
                                ausgewaehlterWert = aktiverWertSchluessel,
                                onWertTippen = { schluessel ->
                                    setzeWert(if (aktiverWertSchluessel == schluessel) null else schluessel)
                                },
                                aufDunkel = true,
                                spalten = 4,
                                schlank = werteSchlank,
                                modifier = Modifier.weight(1f),
                            )

                            LiveEmotionsKachel(
                                emotion = emotion,
                                aufDunkel = true,
                                kompakt = true,
                                nurPortrait = nurPortrait,
                                detailsOffen = aktiveEmotionOffen,
                                onTippen = { setzeEmotionOffen(!aktiveEmotionOffen) },
                                portraitGroesse = if (werteSchlank) 36.dp else 44.dp,
                                portraitContent = portraitContent,
                                modifier = if (nurPortrait) {
                                    Modifier
                                } else {
                                    Modifier.widthIn(min = 136.dp, max = 186.dp)
                                },
                            )

                            if (zusatzAktionen != null || onEingeklapptToggle != null) {
                                Row(
                                    horizontalArrangement = Arrangement.spacedBy(0.dp),
                                    verticalAlignment = Alignment.CenterVertically,
                                ) {
                                    if (zusatzAktionen != null) {
                                        zusatzAktionen()
                                    }
                                    if (onEingeklapptToggle != null) {
                                        KopfLeisteKlappKnopf(
                                            eingeklappt = false,
                                            onClick = onEingeklapptToggle,
                                        )
                                    }
                                }
                            }
                        }
                    } else {
                        // Schmale Fenster (< 600 dp): luftige zweizeilige Darstellung
                        Column(
                            modifier = Modifier.fillMaxWidth(),
                            verticalArrangement = Arrangement.spacedBy(4.dp),
                        ) {
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
                                        text = jahr.toString(),
                                        style = MaterialTheme.typography.titleSmall,
                                        fontFamily = FontFamily.Serif,
                                        color = farben.stufenFarbeHell(2),
                                        fontWeight = FontWeight.Bold,
                                    )
                                    LiveEmotionsKachel(
                                        emotion = emotion,
                                        aufDunkel = true,
                                        kompakt = true,
                                        detailsOffen = aktiveEmotionOffen,
                                        onTippen = { setzeEmotionOffen(!aktiveEmotionOffen) },
                                        portraitGroesse = 34.dp,
                                        portraitContent = portraitContent,
                                        modifier = Modifier.weight(1f, fill = false),
                                    )
                                }

                                Row(
                                    horizontalArrangement = Arrangement.spacedBy(0.dp),
                                    verticalAlignment = Alignment.CenterVertically,
                                ) {
                                    if (zusatzAktionen != null) {
                                        zusatzAktionen()
                                    }
                                    if (onEingeklapptToggle != null) {
                                        KopfLeisteKlappKnopf(
                                            eingeklappt = false,
                                            onClick = onEingeklapptToggle,
                                        )
                                    }
                                }
                            }

                            AnimatedVisibility(
                                visible = !eingeklappt,
                                enter = ArchivUebergaenge.aufklappEnter(reduziert),
                                exit = ArchivUebergaenge.aufklappExit(reduziert),
                            ) {
                                BefindensLeiste(
                                    werte = werte,
                                    ausgewaehlterWert = aktiverWertSchluessel,
                                    onWertTippen = { schluessel ->
                                        setzeWert(if (aktiverWertSchluessel == schluessel) null else schluessel)
                                    },
                                    aufDunkel = true,
                                    spalten = 2,
                                    schlank = true,
                                )
                            }
                        }
                    }
                }
            }

            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(1.dp)
                    .background(farben.akzent.copy(alpha = 0.62f)),
            )
        }
    }

    // Geöffnete Wert- oder Figuren-Erklärkarte erscheint als leichtes, ruhiges Overlay/Popover
    if (ausgewaehlterStatus != null || aktiveEmotionOffen) {
        val schliessen = {
            setzeWert(null)
            setzeEmotionOffen(false)
        }
        Dialog(
            onDismissRequest = schliessen,
            properties = DialogProperties(
                dismissOnBackPress = true,
                dismissOnClickOutside = true,
                usePlatformDefaultWidth = false,
            ),
        ) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .windowInsetsPadding(WindowInsets.safeDrawing)
                    .padding(horizontal = 20.dp, vertical = 14.dp)
                    .archivEscapeAktion(aktiv = true, onEscape = schliessen),
                contentAlignment = Alignment.Center,
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .widthIn(max = 520.dp)
                        .verticalScroll(rememberScrollState()),
                ) {
                    if (ausgewaehlterStatus != null) {
                        WertErklaerKarte(
                            wert = ausgewaehlterStatus,
                            onSchliessen = schliessen,
                        )
                    } else {
                        LiveEmotionDetailKarte(
                            emotion = emotion,
                            onSchliessen = schliessen,
                            portraitContent = portraitContent,
                        )
                    }
                }
            }
        }
    }
}

/**
 * Einzige dezente Ecke/Lasche oben rechts bei eingeklappter Kopfleiste:
 * - Verbraucht 0 dp Seitenleiste und frisst keinerlei Bildschirmbreite.
 * - Zeigt diskret die 4 farbcodierten Befindens-Punkte + Ausklapp-Pfeil in einer kleinen
 *   Lesezeichen-Lasche (mit vollem ≥ 48×48 dp Touch-Ziel).
 * - Ein einziges Tippen klappt die vollständige Kopfleiste ruhig auf.
 */
@Composable
fun KopfLeisteLasche(
    werte: List<WertKachelUiState>,
    emotion: LiveEmotionUiState,
    onAusklappen: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val minTouch = ArchivTheme.metrik.minTouchHoehe
    val spieleEffekt = LocalSoundEffektSpielen.current
    val laschenForm = RoundedCornerShape(bottomStart = 8.dp, bottomEnd = 8.dp)

    Box(
        modifier = modifier
            .windowInsetsPadding(WindowInsets.safeDrawing.only(WindowInsetsSides.End))
            .padding(end = 10.dp)
            .defaultMinSize(minWidth = minTouch, minHeight = minTouch)
            .clip(laschenForm)
            .archivFokusRahmen(eckRadius = 8.dp, aufDunkel = false)
            .clickable {
                spieleEffekt(SoundEffekt.KLICK_SANFT)
                onAusklappen()
            }
            .clearAndSetSemantics {
                role = Role.Button
                selected = false
                stateDescription = "Kopfleiste eingeklappt"
                contentDescription = "Kopfleiste aufklappen (${emotion.personName}, ${emotion.stimmungBezeichnung}; " +
                    werte.joinToString(", ") { "${it.bezeichnung} ${it.stufenName}" } + ")"
            },
        contentAlignment = Alignment.TopEnd,
    ) {
        Row(
            modifier = Modifier
                .clip(laschenForm)
                .background(farben.dunkel.copy(alpha = 0.90f))
                .border(0.75.dp, farben.segmentDunkel, laschenForm)
                .padding(horizontal = 10.dp, vertical = 7.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            // 4 dezente Statuspunkte für Hunger, Erschöpfung, Verdacht, Einsamkeit
            Row(
                horizontalArrangement = Arrangement.spacedBy(4.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                werte.forEach { wert ->
                    Box(
                        modifier = Modifier
                            .size(6.dp)
                            .clip(CircleShape)
                            .background(farben.stufenFarbeHell(wert.stufe)),
                    )
                }
            }

            ChevronIcon(
                nachOben = false,
                farbe = farben.textHell.copy(alpha = 0.88f),
                groesse = 14.dp,
            )
        }
    }
}

@Composable
internal fun KopfLeisteKlappKnopf(
    eingeklappt: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val minTouch = ArchivTheme.metrik.minTouchHoehe
    val spieleEffekt = LocalSoundEffektSpielen.current

    Box(
        modifier = modifier
            .defaultMinSize(minWidth = minTouch, minHeight = minTouch)
            .clip(RoundedCornerShape(6.dp))
            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = true)
            .clickable {
                spieleEffekt(SoundEffekt.KLICK_SANFT)
                onClick()
            }
            .clearAndSetSemantics {
                role = Role.Button
                selected = eingeklappt
                stateDescription = if (eingeklappt) "Kopfleiste eingeklappt" else "Kopfleiste ausgeklappt"
                contentDescription = if (eingeklappt) {
                    "Kopfleiste ausklappen"
                } else {
                    "Kopfleiste einklappen"
                }
            },
        contentAlignment = Alignment.Center,
    ) {
        ChevronIcon(
            nachOben = !eingeklappt,
            farbe = farben.textHell.copy(alpha = 0.88f),
            groesse = 17.dp,
        )
    }
}
