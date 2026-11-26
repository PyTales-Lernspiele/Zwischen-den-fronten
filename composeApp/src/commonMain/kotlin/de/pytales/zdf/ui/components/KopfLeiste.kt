package de.pytales.zdf.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.BorderStroke
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
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.only
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.layout.windowInsetsTopHeight
import androidx.compose.foundation.rememberScrollState
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
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.state.LiveEmotionUiState
import de.pytales.zdf.ui.state.WertKachelUiState
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.ArchivUebergaenge

/**
 * Sehr schlanke, einzeilige und ein-/ausklappbare Kopfleiste für Querformat-Displays:
 * - Zeigt im ausgeklappten Zustand kompakt in einer einzigen Zeile (~58–66 dp Höhe) alle 4
 *   Befindenswerte (*Hunger, Erschöpfung, Verdacht, Einsamkeit*), die [LiveEmotionsKachel]
 *   rechts oben sowie dezente Symbole für Ton, Einstellungen und Einklappen.
 * - Geöffnete Wert- oder Figuren-Erklärkarten erscheinen als ruhiges, leichtes Overlay/Popover,
 *   ohne die Spielbühne nach unten wegzudrücken.
 * - Im eingeklappten Zustand im Querformat zieht sich die obere Leiste vollständig zurück
 *   (nur Statusbar-Hintergrund + feine Zierlinie), während [EingeklappteKopfRandLeiste] rechts
 *   am Rand Ausklappen, Mini-Portrait, 4 Farbindikatoren, Ton und Einstellungen bereithält.
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
        if (eingeklappt && istQuerformat) {
            // Im Querformat eingeklappt: 0 dp Inhalts-Höhe — nur Statusleisten-Hintergrund + feine Linie
            Spacer(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(farben.dunkel)
                    .windowInsetsTopHeight(WindowInsets.safeDrawing),
            )
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(1.5.dp)
                    .background(farben.akzent.copy(alpha = 0.72f)),
            )
        } else {
            // Dunkle Haupt-Kopfleiste (reicht randabfallend hinter Statusbar & Notch)
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
                            vertical = if (metrik.kompakteHoehe) 4.dp else 6.dp,
                        ),
                ) {
                    val verfuegbareBreite = maxWidth

                    if (istQuerformat) {
                        val zeigeJahrLinks = verfuegbareBreite >= 920.dp
                        val nurPortrait = verfuegbareBreite < 740.dp
                        val werteSchlank = metrik.kompakteHoehe || verfuegbareBreite < 960.dp

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(if (werteSchlank) 6.dp else 10.dp),
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            if (zeigeJahrLinks) {
                                Text(
                                    text = jahr.toString(),
                                    style = MaterialTheme.typography.titleMedium,
                                    fontFamily = FontFamily.Serif,
                                    color = farben.stufenFarbeHell(2),
                                    fontWeight = FontWeight.Bold,
                                    modifier = Modifier.padding(end = 4.dp),
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
                                portraitGroesse = if (werteSchlank) 40.dp else metrik.portraitGroesse,
                                portraitContent = portraitContent,
                                modifier = if (nurPortrait) {
                                    Modifier
                                } else {
                                    Modifier.widthIn(min = 148.dp, max = 196.dp)
                                },
                            )

                            if (zusatzAktionen != null || onEingeklapptToggle != null) {
                                Row(
                                    horizontalArrangement = Arrangement.spacedBy(2.dp),
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
                        // Schmale Fenster (< 600 dp): kompakt einklappbar auf eine 48-dp-Mikroleiste
                        Column(
                            modifier = Modifier.fillMaxWidth(),
                            verticalArrangement = Arrangement.spacedBy(6.dp),
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
                                    if (eingeklappt) {
                                        MiniWerteIndikatorZeile(
                                            werte = werte,
                                            onClick = onEingeklapptToggle,
                                        )
                                    } else {
                                        LiveEmotionsKachel(
                                            emotion = emotion,
                                            aufDunkel = true,
                                            kompakt = true,
                                            detailsOffen = aktiveEmotionOffen,
                                            onTippen = { setzeEmotionOffen(!aktiveEmotionOffen) },
                                            portraitGroesse = 36.dp,
                                            portraitContent = portraitContent,
                                            modifier = Modifier.weight(1f, fill = false),
                                        )
                                    }
                                }

                                Row(
                                    horizontalArrangement = Arrangement.spacedBy(2.dp),
                                    verticalAlignment = Alignment.CenterVertically,
                                ) {
                                    if (zusatzAktionen != null) {
                                        zusatzAktionen()
                                    }
                                    if (onEingeklapptToggle != null) {
                                        KopfLeisteKlappKnopf(
                                            eingeklappt = eingeklappt,
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
                    .height(1.5.dp)
                    .background(farben.akzent.copy(alpha = 0.78f)),
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
 * Schmale rechte Archiv-Randleiste (~54 dp breit), die im Querformat bei eingeklappter
 * Kopfleiste 0 dp vertikale Höhe verbraucht und dennoch sofortigen Zugriff auf Ausklappen,
 * Live-Portrait, 4 farbcodierte Status-Indikatoren, Ton und Einstellungen bietet — ohne
 * jemals Text oder Illustrationen zu überdecken.
 */
@Composable
fun EingeklappteKopfRandLeiste(
    werte: List<WertKachelUiState>,
    emotion: LiveEmotionUiState,
    onAusklappen: () -> Unit,
    onEmotionTippen: () -> Unit,
    modifier: Modifier = Modifier,
    zusatzAktionenVertikal: (@Composable () -> Unit)? = null,
    portraitContent: (@Composable BoxScope.(portraitId: String) -> Unit)? = null,
) {
    val farben = ArchivTheme.farben
    val stimmungsFarbe = stimmungsAkzentFarbe(
        stimmung = emotion.stimmung,
        hoechsteStufe = emotion.hoechsteStufe,
        farben = farben,
        aufDunkel = true,
    )

    Row(
        modifier = modifier
            .fillMaxHeight()
            .background(farben.dunkel)
            .windowInsetsPadding(
                WindowInsets.safeDrawing.only(WindowInsetsSides.End + WindowInsetsSides.Bottom),
            )
            .archivFokusGruppe(),
    ) {
        Box(
            modifier = Modifier
                .width(1.dp)
                .fillMaxHeight()
                .background(farben.akzent.copy(alpha = 0.55f)),
        )
        Column(
            modifier = Modifier
                .fillMaxHeight()
                .width(54.dp)
                .padding(vertical = 4.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(4.dp),
        ) {
            // Exakt oben rechts, wo der Einklappen-Knopf lag
            KopfLeisteKlappKnopf(
                eingeklappt = true,
                onClick = onAusklappen,
            )

            // Kompaktes Live-Portrait (48×48 Touch-Ziel)
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(RoundedCornerShape(6.dp))
                    .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = true)
                    .clickable(onClick = onEmotionTippen)
                    .clearAndSetSemantics {
                        role = Role.Button
                        contentDescription = "${emotion.personName} (${emotion.stimmungBezeichnung}). Tippen für Figuren-Ansicht."
                    },
                contentAlignment = Alignment.Center,
            ) {
                ArchivPortraitRahmen(
                    emotion = emotion,
                    stimmungsFarbe = stimmungsFarbe,
                    groesse = 38.dp,
                    aufDunkel = true,
                    portraitContent = portraitContent,
                )
            }

            // 4 farbcodierte Status-Indikatoren auf einen Blick (Tippen klappt Leiste aus)
            Column(
                modifier = Modifier
                    .defaultMinSize(minWidth = 48.dp, minHeight = 48.dp)
                    .clip(RoundedCornerShape(6.dp))
                    .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = true)
                    .clickable(onClick = onAusklappen)
                    .clearAndSetSemantics {
                        role = Role.Button
                        contentDescription = "Befindenswerte anzeigen: " +
                            werte.joinToString(", ") { "${it.bezeichnung} ${it.stufenName}" } +
                            ". Tippen, um Kopfleiste auszuklappen."
                    }
                    .padding(horizontal = 10.dp, vertical = 6.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(4.dp),
            ) {
                werte.forEach { wert ->
                    val farbe = farben.stufenFarbeHell(wert.stufe)
                    Box(
                        modifier = Modifier
                            .width(24.dp)
                            .height(5.dp)
                            .clip(RoundedCornerShape(2.dp))
                            .background(farben.segmentDunkel),
                    ) {
                        val anteil = (wert.gefuellteSegmente.toFloat() / wert.segmenteGesamt.coerceAtLeast(1))
                            .coerceIn(0.18f, 1f)
                        Box(
                            modifier = Modifier
                                .fillMaxWidth(anteil)
                                .fillMaxHeight()
                                .background(farbe),
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.weight(1f))

            if (zusatzAktionenVertikal != null) {
                zusatzAktionenVertikal()
            }
        }
    }
}

@Composable
private fun MiniWerteIndikatorZeile(
    werte: List<WertKachelUiState>,
    onClick: (() -> Unit)?,
) {
    val farben = ArchivTheme.farben
    Row(
        modifier = Modifier
            .clip(RoundedCornerShape(4.dp))
            .then(
                if (onClick != null) {
                    Modifier.clickable(onClick = onClick)
                } else {
                    Modifier
                },
            )
            .padding(horizontal = 6.dp, vertical = 6.dp),
        horizontalArrangement = Arrangement.spacedBy(5.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        werte.forEach { wert ->
            val farbe = farben.stufenFarbeHell(wert.stufe)
            Box(
                modifier = Modifier
                    .size(width = 16.dp, height = 6.dp)
                    .clip(RoundedCornerShape(2.dp))
                    .background(farbe),
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

    Box(
        modifier = modifier
            .defaultMinSize(minWidth = minTouch, minHeight = minTouch)
            .clip(RoundedCornerShape(6.dp))
            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = true)
            .clickable(onClick = onClick)
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
        Box(
            modifier = Modifier
                .size(34.dp)
                .clip(RoundedCornerShape(6.dp))
                .background(farben.dunkelHell.copy(alpha = 0.85f))
                .border(0.75.dp, farben.segmentDunkel, RoundedCornerShape(6.dp)),
            contentAlignment = Alignment.Center,
        ) {
            ChevronIcon(
                nachOben = !eingeklappt,
                farbe = farben.textHell,
                groesse = 16.dp,
            )
        }
    }
}
