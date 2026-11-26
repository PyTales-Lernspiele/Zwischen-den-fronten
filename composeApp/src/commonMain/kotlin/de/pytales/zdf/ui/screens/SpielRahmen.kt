package de.pytales.zdf.ui.screens

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.WindowInsetsSides
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.only
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
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
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import de.pytales.zdf.audio.AudioZustand
import de.pytales.zdf.audio.SoundEffekt
import de.pytales.zdf.content.GameContent
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.model.OnboardingGrundsatz
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.components.ArchivTrennlinie
import de.pytales.zdf.ui.components.ChevronIcon
import de.pytales.zdf.ui.components.EinstellungenIcon
import de.pytales.zdf.ui.components.KopfLeiste
import de.pytales.zdf.ui.components.KopfLeisteLasche
import de.pytales.zdf.ui.components.SchliessenIcon
import de.pytales.zdf.ui.components.SchriftgroessenSchalter
import de.pytales.zdf.ui.components.TonIcon
import de.pytales.zdf.ui.components.archivEscapeAktion
import de.pytales.zdf.ui.components.archivFokusGruppe
import de.pytales.zdf.ui.components.archivFokusRahmen
import de.pytales.zdf.ui.components.archivLiveHinweis
import de.pytales.zdf.ui.components.archivPapierHintergrund
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.media.ArchivKapitelBild
import de.pytales.zdf.ui.media.LocalMedienRegister
import de.pytales.zdf.ui.state.KapitelbildUiState
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.state.UiStateMapper
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.ArchivUebergaenge
import de.pytales.zdf.ui.theme.LocalSoundEffektSpielen
import de.pytales.zdf.ui.theme.Schriftgroesse

/**
 * Gemeinsamer, radikal ruhiger Rahmen für alle Spielphasen mit Befindensleiste
 * (`Musterung`, `Erwerb`, `KapitelStart`, `Ereignis`, `KapitelAbschluss`):
 * - **Aufgeklappt:** Flache, luftige [KopfLeiste] oben.
 * - **Eingeklappt:** Volle Bildschirmbreite & -höhe für das aufgeschlagene Buch — keine
 *   dunkle Seitenleiste! Einzig die kleine dezente Ecke/Lasche ([KopfLeisteLasche]) oben
 *   rechts öffnet die Kopfleiste jederzeit mit einem Tippen.
 */
@Composable
internal fun SpielBuehnenRahmen(
    engine: GameEngine,
    uiState: SpielUiState,
    onAudioToggle: () -> Unit,
    onEinstellungenOeffnen: () -> Unit,
    onKopfleisteToggle: () -> Unit,
    onWertErklaerungChange: (WertSchluessel?) -> Unit,
    onEmotionDetailsOffenChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier,
    inhalt: @Composable BoxScope.() -> Unit,
) {
    val gameState = uiState.gameState
    val werteUi = remember(engine, gameState) {
        UiStateMapper.mapBefindensLeiste(engine, gameState)
    }
    val emotionUi = remember(engine, gameState) {
        UiStateMapper.mapLiveEmotion(engine, gameState)
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .archivPapierHintergrund(),
    ) {
        KopfLeiste(
            jahr = gameState.jahr,
            werte = werteUi,
            emotion = emotionUi,
            eingeklappt = uiState.kopfleisteEingeklappt,
            onEingeklapptToggle = onKopfleisteToggle,
            ausgewaehlterWert = uiState.ausgewaehlterWert,
            onAusgewaehlterWertChange = onWertErklaerungChange,
            emotionDetailsOffen = uiState.emotionDetailsOffen,
            onEmotionDetailsOffenChange = onEmotionDetailsOffenChange,
            zusatzAktionen = {
                AudioIconKnopf(
                    audioZustand = uiState.audioZustand,
                    aufDunkel = true,
                    onToggle = onAudioToggle,
                )
                EinstellungenIconKnopf(
                    aufDunkel = true,
                    onClick = onEinstellungenOeffnen,
                )
            },
        )

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f),
        ) {
            inhalt()

            if (uiState.kopfleisteEingeklappt) {
                KopfLeisteLasche(
                    werte = werteUi,
                    emotion = emotionUi,
                    onAusklappen = onKopfleisteToggle,
                    modifier = Modifier.align(Alignment.TopEnd),
                )
            }
        }
    }
}

/**
 * Extrem schlankes, einzeiliges dunkles Archiv-Kopfband für Bildschirme ohne Befindensleiste
 * (`HerkunftWahl`, `Auffangnetz`, `Lebenslauf`). Zeigt nur eine knappe Kontextzeile links
 * (niemals doppelte Überschriften!) sowie die flachen Ton- und Einstellungs-Symbole rechts.
 */
@Composable
internal fun ArchivKopfBand(
    marke: String,
    audioZustand: AudioZustand,
    onAudioToggle: () -> Unit,
    onEinstellungenOeffnen: () -> Unit,
    modifier: Modifier = Modifier,
    titel: String? = null,
    linksZusatz: (@Composable () -> Unit)? = null,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik

    Column(
        modifier = modifier
            .fillMaxWidth()
            .archivFokusGruppe(),
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(farben.dunkel),
            contentAlignment = Alignment.Center,
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .windowInsetsPadding(
                        WindowInsets.safeDrawing.only(WindowInsetsSides.Top + WindowInsetsSides.Horizontal),
                    )
                    .widthIn(max = metrik.maxInhaltsBreite)
                    .padding(
                        horizontal = metrik.aussenAbstand,
                        vertical = if (metrik.kompakteHoehe) 2.dp else 4.dp,
                    ),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                if (linksZusatz != null) {
                    Box(modifier = Modifier.weight(1f)) {
                        linksZusatz()
                    }
                } else {
                    Row(
                        modifier = Modifier.weight(1f),
                        horizontalArrangement = Arrangement.spacedBy(10.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        Text(
                            text = marke,
                            style = MaterialTheme.typography.labelMedium,
                            fontFamily = FontFamily.Serif,
                            color = farben.stufenFarbeHell(2),
                            fontWeight = FontWeight.SemiBold,
                            maxLines = 1,
                        )
                        if (!titel.isNullOrBlank()) {
                            Text(
                                text = "·  $titel",
                                style = MaterialTheme.typography.titleSmall,
                                fontFamily = FontFamily.Serif,
                                color = farben.textHell,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis,
                            )
                        }
                    }
                }

                Row(
                    horizontalArrangement = Arrangement.spacedBy(0.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    AudioIconKnopf(
                        audioZustand = audioZustand,
                        aufDunkel = true,
                        onToggle = onAudioToggle,
                    )
                    EinstellungenIconKnopf(
                        aufDunkel = true,
                        onClick = onEinstellungenOeffnen,
                    )
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

/**
 * Flacher, ruhiger Ton-Umschalter (48×48 dp Touch-Ziel, ohne Kastenrahmen).
 * Bei Stummschaltung über dieses Symbol ist sofort alles still (Grundmusik + Klickgeräusche).
 */
@Composable
internal fun AudioIconKnopf(
    audioZustand: AudioZustand,
    aufDunkel: Boolean,
    onToggle: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val minTouch = ArchivTheme.metrik.minTouchHoehe
    val gesperrt = audioZustand.musikGesperrt
    val spielt = audioZustand.spieltGerade
    val tonAn = audioZustand.hatAktivenTon

    val iconFarbe = when {
        gesperrt -> if (aufDunkel) farben.textHell.copy(alpha = 0.56f) else farben.tinteMatt.copy(alpha = 0.72f)
        tonAn -> if (aufDunkel) farben.stufenFarbeHell(0) else farben.stufenFarbe(0)
        else -> if (aufDunkel) farben.textHell.copy(alpha = 0.85f) else farben.tinteMatt
    }

    val statusText = when {
        gesperrt && !audioZustand.effekteAktiv -> audioZustand.sperrGrund?.hinweis ?: "Respektvolle Stille."
        gesperrt -> "${audioZustand.sperrGrund?.hinweis ?: "Respektvolle Stille."} Klickgeräusche aktiv."
        spielt && audioZustand.effekteAktiv -> "Grundmusik und Klickgeräusche eingeschaltet."
        spielt -> "Grundmusik eingeschaltet."
        audioZustand.effekteAktiv -> "Klick- und Papiergeräusche eingeschaltet."
        else -> "Stummgeschaltet."
    }
    val beschreibung = if (tonAn || audioZustand.audioAktiv || audioZustand.effekteAktiv) {
        "$statusText Tippen zum vollständigen Stummschalten."
    } else {
        "$statusText Tippen, um Grundmusik und Klickgeräusche einzuschalten."
    }

    Box(
        modifier = modifier
            .defaultMinSize(minWidth = minTouch, minHeight = minTouch)
            .clip(RoundedCornerShape(6.dp))
            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = aufDunkel)
            .clickable(onClick = onToggle)
            .clearAndSetSemantics {
                role = Role.Switch
                selected = tonAn
                stateDescription = statusText
                contentDescription = beschreibung
            },
        contentAlignment = Alignment.Center,
    ) {
        TonIcon(
            aktiv = tonAn,
            gesperrt = gesperrt && !audioZustand.effekteAktiv,
            farbe = iconFarbe,
            groesse = 19.dp,
        )
    }
}

/**
 * Flaches Einstellungs-Symbol (Zahnrad, 48×48 dp Touch-Ziel, ohne Kastenrahmen).
 */
@Composable
internal fun EinstellungenIconKnopf(
    aufDunkel: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    hatHinweisPunkt: Boolean = false,
) {
    val farben = ArchivTheme.farben
    val minTouch = ArchivTheme.metrik.minTouchHoehe
    val spieleEffekt = LocalSoundEffektSpielen.current
    val iconFarbe = if (aufDunkel) farben.textHell.copy(alpha = 0.88f) else farben.tinte

    Box(
        modifier = modifier
            .defaultMinSize(minWidth = minTouch, minHeight = minTouch)
            .clip(RoundedCornerShape(6.dp))
            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = aufDunkel)
            .clickable {
                spieleEffekt(SoundEffekt.KLICK_SANFT)
                onClick()
            }
            .clearAndSetSemantics {
                role = Role.Button
                contentDescription = "Einstellungen öffnen (Schriftgröße, Musik, Geräusche, Animationen)"
            },
        contentAlignment = Alignment.Center,
    ) {
        Box(contentAlignment = Alignment.Center) {
            EinstellungenIcon(
                farbe = iconFarbe,
                groesse = 19.dp,
            )
            if (hatHinweisPunkt) {
                Box(
                    modifier = Modifier
                        .align(Alignment.TopEnd)
                        .size(6.dp)
                        .clip(CircleShape)
                        .background(farben.akzent),
                )
            }
        }
    }
}

/**
 * Ruhiger, klar gegliederter Einstellungs-Dialog:
 * Schriftgröße, **Grundmusik** (Ein/Aus), **Klick- & Papiergeräusche** (Ein/Aus),
 * Animationen reduzieren sowie (vor Spielbeginn) Unterrichts-Direktwahl.
 */
@Composable
internal fun EinstellungenDialog(
    content: GameContent,
    uiState: SpielUiState,
    onSchriftgroesseChange: (Schriftgroesse) -> Unit,
    onReduzierteAnimationenToggle: () -> Unit,
    onGrundmusikToggle: () -> Unit,
    onEffekteToggle: () -> Unit,
    onDirektwahlChange: (Boolean) -> Unit,
    onSchliessen: () -> Unit,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val spieleEffekt = LocalSoundEffektSpielen.current
    val direktwahlOption = content.herkunft.direktwahlOption
    val imStartmenue = uiState.gameState.phase is GamePhase.Start
    val direktwahlAktiv = uiState.gameState.direktwahlAktiv

    Dialog(
        onDismissRequest = onSchliessen,
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
                .archivEscapeAktion(aktiv = true, onEscape = onSchliessen),
            contentAlignment = Alignment.Center,
        ) {
            Surface(
                modifier = Modifier
                    .fillMaxWidth()
                    .widthIn(max = 520.dp)
                    .archivFokusGruppe(),
                color = farben.papierHell,
                shape = RoundedCornerShape(8.dp),
                border = BorderStroke(0.75.dp, farben.linieFein),
                shadowElevation = 8.dp,
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .verticalScroll(rememberScrollState()),
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(2.5.dp)
                            .background(farben.akzent),
                    )

                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 20.dp, vertical = 14.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            Text(
                                text = "Einstellungen",
                                style = MaterialTheme.typography.headlineSmall,
                                color = farben.tinte,
                                modifier = Modifier.archivUeberschrift(),
                            )
                            Box(
                                modifier = Modifier
                                    .defaultMinSize(minWidth = metrik.minTouchHoehe, minHeight = metrik.minTouchHoehe)
                                    .clip(RoundedCornerShape(6.dp))
                                    .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = false)
                                    .clickable {
                                        spieleEffekt(SoundEffekt.KLICK_SANFT)
                                        onSchliessen()
                                    }
                                    .semantics {
                                        role = Role.Button
                                        contentDescription = "Einstellungen schließen"
                                    },
                                contentAlignment = Alignment.Center,
                            ) {
                                SchliessenIcon(farbe = farben.tinteMatt, groesse = 18.dp)
                            }
                        }

                        // 1. Schriftgröße
                        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                            Text(
                                text = "Schriftgröße",
                                style = MaterialTheme.typography.titleSmall,
                                color = farben.tinte,
                            )
                            SchriftgroessenSchalter(
                                aktuell = uiState.schriftgroesse,
                                onAuswahl = {
                                    spieleEffekt(SoundEffekt.KLICK_SANFT)
                                    onSchriftgroesseChange(it)
                                },
                                aufDunkel = false,
                                kompakt = false,
                                modifier = Modifier.fillMaxWidth(),
                            )
                        }

                        ArchivTrennlinie(farbe = farben.linieFein.copy(alpha = 0.55f))

                        // 2. Grundmusik (getragene Kammermusik)
                        ArchivSchalterZeile(
                            titel = "Grundmusik",
                            beschreibung = if (uiState.audioZustand.musikGesperrt) {
                                "An Front, Etappe und bei Einschnitt herrscht respektvolle Stille."
                            } else {
                                "Getragene Kammermusik im Startmenü und in der Heimat."
                            },
                            aktiv = uiState.audioAktiv,
                            onToggle = {
                                spieleEffekt(SoundEffekt.KLICK_SANFT)
                                onGrundmusikToggle()
                            },
                        )

                        // 3. Klick- & Papiergeräusche
                        ArchivSchalterZeile(
                            titel = "Klick- & Papiergeräusche",
                            beschreibung = "Leises Tippen und Umblättern bei Entscheidungen.",
                            aktiv = uiState.effekteAktiv,
                            onToggle = onEffekteToggle,
                        )

                        ArchivTrennlinie(farbe = farben.linieFein.copy(alpha = 0.55f))

                        // 4. Animationen reduzieren
                        ArchivSchalterZeile(
                            titel = "Animationen reduzieren",
                            beschreibung = "Sofortige Wechsel ohne Überblendungen.",
                            aktiv = uiState.reduzierteAnimationen,
                            onToggle = {
                                spieleEffekt(SoundEffekt.KLICK_SANFT)
                                onReduzierteAnimationenToggle()
                            },
                        )

                        // 5. Unterrichts-Direktwahl
                        if (direktwahlOption.aktiv) {
                            ArchivTrennlinie(farbe = farben.linieFein.copy(alpha = 0.55f))
                            ArchivSchalterZeile(
                                titel = "Pfad direkt wählen (Unterricht)",
                                beschreibung = if (imStartmenue) {
                                    "Front, Etappe oder Heimat direkt nach der Herkunft wählen."
                                } else {
                                    "Nur vor Beginn eines Durchgangs umstellbar."
                                },
                                aktiv = direktwahlAktiv,
                                aktiviert = imStartmenue,
                                onToggle = {
                                    spieleEffekt(SoundEffekt.KLICK_SANFT)
                                    onDirektwahlChange(!direktwahlAktiv)
                                },
                            )
                        }
                    }
                }
            }
        }
    }
}

/**
 * Ruhiger Buchdruck-Dialog für die drei Grundsätze vor Spielbeginn.
 */
@Composable
internal fun GrundsaetzeDialog(
    grundsaetze: List<OnboardingGrundsatz>,
    aufgeklappteIds: Set<String>,
    onGrundsatzToggle: (String) -> Unit,
    onSchliessen: () -> Unit,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val spieleEffekt = LocalSoundEffektSpielen.current
    val roemisch = listOf("I", "II", "III", "IV")

    Dialog(
        onDismissRequest = onSchliessen,
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
                .archivEscapeAktion(aktiv = true, onEscape = onSchliessen),
            contentAlignment = Alignment.Center,
        ) {
            Surface(
                modifier = Modifier
                    .fillMaxWidth()
                    .widthIn(max = 540.dp)
                    .archivFokusGruppe(),
                color = farben.papierHell,
                shape = RoundedCornerShape(8.dp),
                border = BorderStroke(0.75.dp, farben.linieFein),
                shadowElevation = 8.dp,
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .verticalScroll(rememberScrollState()),
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(2.5.dp)
                            .background(farben.akzent),
                    )
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 20.dp, vertical = 14.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            Text(
                                text = "Drei Grundsätze",
                                style = MaterialTheme.typography.headlineSmall,
                                color = farben.tinte,
                                modifier = Modifier.archivUeberschrift(),
                            )
                            Box(
                                modifier = Modifier
                                    .defaultMinSize(minWidth = metrik.minTouchHoehe, minHeight = metrik.minTouchHoehe)
                                    .clip(RoundedCornerShape(6.dp))
                                    .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = false)
                                    .clickable {
                                        spieleEffekt(SoundEffekt.KLICK_SANFT)
                                        onSchliessen()
                                    }
                                    .semantics {
                                        role = Role.Button
                                        contentDescription = "Grundsätze schließen"
                                    },
                                contentAlignment = Alignment.Center,
                            ) {
                                SchliessenIcon(farbe = farben.tinteMatt, groesse = 18.dp)
                            }
                        }

                        grundsaetze.forEachIndexed { index, grundsatz ->
                            val offen = grundsatz.id in aufgeklappteIds
                            GrundsatzZeile(
                                numeral = roemisch.getOrElse(index) { "${index + 1}" },
                                grundsatz = grundsatz,
                                aufgeklappt = offen,
                                onToggle = {
                                    spieleEffekt(SoundEffekt.KLICK_SANFT)
                                    onGrundsatzToggle(grundsatz.id)
                                },
                            )
                            if (index < grundsaetze.lastIndex) {
                                ArchivTrennlinie(farbe = farben.linieFein.copy(alpha = 0.55f))
                            }
                        }

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.End,
                        ) {
                            ArchivPrimaerKnopf(
                                label = "Verstanden",
                                onClick = onSchliessen,
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun GrundsatzZeile(
    numeral: String,
    grundsatz: OnboardingGrundsatz,
    aufgeklappt: Boolean,
    onToggle: () -> Unit,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val reduziert = ArchivTheme.reduzierteAnimationen

    Column(modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .defaultMinSize(minHeight = metrik.minTouchHoehe)
                .clip(RoundedCornerShape(5.dp))
                .archivFokusRahmen(eckRadius = 5.dp, aufDunkel = false)
                .clickable(onClick = onToggle)
                .clearAndSetSemantics {
                    role = Role.Button
                    selected = aufgeklappt
                    stateDescription = if (aufgeklappt) "Aufgeklappt" else "Zugeklappt"
                    contentDescription = "${grundsatz.satz} ${grundsatz.mehr}"
                }
                .padding(vertical = 6.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                text = "$numeral.",
                style = MaterialTheme.typography.titleMedium,
                fontFamily = FontFamily.Serif,
                color = farben.akzent,
                fontWeight = FontWeight.Bold,
            )
            Text(
                text = grundsatz.satz,
                style = MaterialTheme.typography.titleSmall,
                color = farben.tinte,
                modifier = Modifier.weight(1f),
            )
            ChevronIcon(
                nachOben = aufgeklappt,
                farbe = farben.tinteMatt,
                groesse = 15.dp,
            )
        }
        AnimatedVisibility(
            visible = aufgeklappt,
            enter = ArchivUebergaenge.aufklappEnter(reduziert),
            exit = ArchivUebergaenge.aufklappExit(reduziert),
        ) {
            Text(
                text = grundsatz.mehr,
                style = MaterialTheme.typography.bodyMedium,
                color = farben.tinteMatt,
                modifier = Modifier.padding(start = 26.dp, bottom = 6.dp),
            )
        }
    }
}

/**
 * Kontraststarker, warmer primärer Archiv-Button (z. B. „Durchgang beginnen“, „Weiter“).
 */
@Composable
internal fun ArchivPrimaerKnopf(
    label: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    aktiviert: Boolean = true,
    akzentStil: Boolean = false,
    klickEffekt: SoundEffekt? = SoundEffekt.KLICK_SANFT,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val spieleEffekt = LocalSoundEffektSpielen.current
    val flaeche = when {
        !aktiviert -> farben.papierDunkel
        akzentStil -> farben.akzent
        else -> farben.tinte
    }
    val textFarbe = if (aktiviert) farben.papierHell else farben.tinteMatt
    val rahmen = if (aktiviert) flaeche else farben.linieFein

    Surface(
        modifier = modifier
            .defaultMinSize(minWidth = metrik.minTouchHoehe, minHeight = metrik.minTouchHoehe)
            .clip(RoundedCornerShape(6.dp))
            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = false)
            .clickable(enabled = aktiviert) {
                if (klickEffekt != null) spieleEffekt(klickEffekt)
                onClick()
            }
            .semantics {
                role = Role.Button
                contentDescription = label
            },
        color = flaeche,
        shape = RoundedCornerShape(6.dp),
        border = BorderStroke(1.dp, rahmen),
        shadowElevation = if (aktiviert) 1.dp else 0.dp,
    ) {
        Box(
            modifier = Modifier.padding(horizontal = 22.dp, vertical = 12.dp),
            contentAlignment = Alignment.Center,
        ) {
            Text(
                text = label,
                style = MaterialTheme.typography.labelLarge,
                color = textFarbe,
                textAlign = TextAlign.Center,
            )
        }
    }
}

/**
 * Ruhiger sekundärer Archiv-Button auf hellem Papier.
 */
@Composable
internal fun ArchivSekundaerKnopf(
    label: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    aktiviert: Boolean = true,
    klickEffekt: SoundEffekt? = SoundEffekt.KLICK_SANFT,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val spieleEffekt = LocalSoundEffektSpielen.current

    Surface(
        modifier = modifier
            .defaultMinSize(minWidth = metrik.minTouchHoehe, minHeight = metrik.minTouchHoehe)
            .clip(RoundedCornerShape(6.dp))
            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = false)
            .clickable(enabled = aktiviert) {
                if (klickEffekt != null) spieleEffekt(klickEffekt)
                onClick()
            }
            .semantics {
                role = Role.Button
                contentDescription = label
            },
        color = if (aktiviert) farben.papierHell else farben.papier,
        shape = RoundedCornerShape(6.dp),
        border = BorderStroke(0.75.dp, if (aktiviert) farben.linie else farben.linieFein),
    ) {
        Box(
            modifier = Modifier.padding(horizontal = 18.dp, vertical = 11.dp),
            contentAlignment = Alignment.Center,
        ) {
            Text(
                text = label,
                style = MaterialTheme.typography.labelLarge,
                color = if (aktiviert) farben.tinte else farben.tinteMatt,
                textAlign = TextAlign.Center,
            )
        }
    }
}

/**
 * Schlichter, zurückhaltender Text-Button (z. B. „Grundsätze“, „Herkunft ändern“).
 */
@Composable
internal fun ArchivTextKnopf(
    label: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    hervorgehoben: Boolean = false,
    klickEffekt: SoundEffekt? = SoundEffekt.KLICK_SANFT,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val spieleEffekt = LocalSoundEffektSpielen.current

    Box(
        modifier = modifier
            .defaultMinSize(minWidth = metrik.minTouchHoehe, minHeight = metrik.minTouchHoehe)
            .clip(RoundedCornerShape(6.dp))
            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = false)
            .clickable {
                if (klickEffekt != null) spieleEffekt(klickEffekt)
                onClick()
            }
            .semantics {
                role = Role.Button
                contentDescription = label
            }
            .padding(horizontal = 12.dp, vertical = 8.dp),
        contentAlignment = Alignment.Center,
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelLarge,
            color = if (hervorgehoben) farben.akzent else farben.tinteMatt,
            textAlign = TextAlign.Center,
        )
    }
}

/**
 * Aufgeräumte Schalter-Zeile ohne Kasten-in-Kasten-Rahmen (für Einstellungen & Export-Option).
 */
@Composable
internal fun ArchivSchalterZeile(
    titel: String,
    beschreibung: String,
    aktiv: Boolean,
    onToggle: () -> Unit,
    modifier: Modifier = Modifier,
    aktiviert: Boolean = true,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik

    Row(
        modifier = modifier
            .fillMaxWidth()
            .defaultMinSize(minHeight = metrik.minTouchHoehe)
            .clip(RoundedCornerShape(6.dp))
            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = false)
            .clickable(enabled = aktiviert, onClick = onToggle)
            .clearAndSetSemantics {
                role = Role.Switch
                selected = aktiv
                stateDescription = if (aktiv) "Eingeschaltet" else "Ausgeschaltet"
                contentDescription = "$titel: ${if (aktiv) "eingeschaltet" else "ausgeschaltet"}. $beschreibung"
            }
            .padding(vertical = 4.dp),
        horizontalArrangement = Arrangement.spacedBy(14.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Column(
            modifier = Modifier.weight(1f),
            verticalArrangement = Arrangement.spacedBy(2.dp),
        ) {
            Text(
                text = titel,
                style = MaterialTheme.typography.titleSmall,
                color = if (aktiviert) farben.tinte else farben.tinteMatt,
            )
            Text(
                text = beschreibung,
                style = MaterialTheme.typography.bodySmall,
                color = farben.tinteMatt,
            )
        }

        val bahnFarbe = when {
            !aktiviert -> farben.segmentLeer.copy(alpha = 0.6f)
            aktiv -> farben.akzent
            else -> farben.segmentLeer
        }
        Box(
            modifier = Modifier
                .size(width = 44.dp, height = 26.dp)
                .clip(RoundedCornerShape(13.dp))
                .background(bahnFarbe)
                .padding(3.dp),
            contentAlignment = if (aktiv) Alignment.CenterEnd else Alignment.CenterStart,
        ) {
            Box(
                modifier = Modifier
                    .size(20.dp)
                    .clip(CircleShape)
                    .background(farben.papierHell),
            )
        }
    }
}

/**
 * Stimmungsvoll gerahmtes 16:9-Kapitelbild (`1280×720`) im ruhigen Buch-Passepartout
 * mit einer einzigen schlichten Zeitraum-Zeile darunter (keine doppelte Kapitelüberschrift).
 */
@Composable
internal fun KapitelbildRahmen(
    kapitelbild: KapitelbildUiState,
    modifier: Modifier = Modifier,
    bildContent: (@Composable BoxScope.(bildId: String) -> Unit)? = null,
) {
    val farben = ArchivTheme.farben
    val medienRegister = LocalMedienRegister.current
    val rahmenBeschreibung =
        "Kapitelbild ${kapitelbild.jahr}: ${kapitelbild.ueberschrift} (${kapitelbild.zeitraum})"

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
                        bildContent(kapitelbild.bildId)
                    } else {
                        ArchivKapitelBild(
                            kapitelBildId = kapitelbild.bildId,
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
                                verticalArrangement = Arrangement.spacedBy(5.dp),
                            ) {
                                Text(
                                    text = kapitelbild.jahr.toString(),
                                    style = MaterialTheme.typography.displaySmall,
                                    color = farben.akzent,
                                    textAlign = TextAlign.Center,
                                )
                                Text(
                                    text = kapitelbild.ueberschrift,
                                    style = MaterialTheme.typography.titleLarge,
                                    color = farben.tinte,
                                    textAlign = TextAlign.Center,
                                    maxLines = 2,
                                    overflow = TextOverflow.Ellipsis,
                                )
                            }
                        }
                    }
                }
            }
        }

        Text(
            text = "${kapitelbild.zeitraum} · ${kapitelbild.pfadMarke}",
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

/**
 * Ergänzt sichere horizontale und untere Safe-Area-Abstände (`WindowInsets.safeDrawing`)
 * für scrollbare Inhaltsbereiche unterhalb der Kopfleiste.
 */
@Composable
internal fun Modifier.archivInhaltsSafeArea(
    ohneRechtenRand: Boolean = false,
): Modifier = this.windowInsetsPadding(
    WindowInsets.safeDrawing.only(
        if (ohneRechtenRand) {
            WindowInsetsSides.Start + WindowInsetsSides.Bottom
        } else {
            WindowInsetsSides.Horizontal + WindowInsetsSides.Bottom
        },
    ),
)

/**
 * Ruhige Sicherheitsabfrage im Archivpapier-Stil für die Android-Zurück-Taste während eines
 * Durchgangs (wahrt die „Kein Zurück“-Leitplanke und verhindert versehentliches Abbrechen).
 */
@Composable
internal fun VerlassenSicherheitsDialog(
    istAbgeschlossen: Boolean,
    onBleiben: () -> Unit,
    onZumStartmenue: () -> Unit,
    onAppBeenden: (() -> Unit)? = null,
) {
    val farben = ArchivTheme.farben

    Dialog(
        onDismissRequest = onBleiben,
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
                .archivEscapeAktion(aktiv = true, onEscape = onBleiben),
            contentAlignment = Alignment.Center,
        ) {
            Surface(
                modifier = Modifier
                    .fillMaxWidth()
                    .widthIn(max = 460.dp)
                    .archivFokusGruppe()
                    .archivLiveHinweis(),
                color = farben.papierHell,
                shape = RoundedCornerShape(8.dp),
                border = BorderStroke(0.75.dp, farben.linieFein),
                shadowElevation = 8.dp,
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .verticalScroll(rememberScrollState()),
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(2.5.dp)
                            .background(farben.akzent),
                    )
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 20.dp, vertical = 16.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        Text(
                            text = if (istAbgeschlossen) {
                                "Lebenslauf verlassen?"
                            } else {
                                "Durchgang wirklich beenden?"
                            },
                            style = MaterialTheme.typography.headlineSmall,
                            color = farben.tinte,
                            modifier = Modifier.archivUeberschrift(),
                        )
                        Text(
                            text = if (istAbgeschlossen) {
                                "Wenn du zum Startmenü wechselst oder die App schließt, wird dieser Durchgang zurückgesetzt."
                            } else {
                                "Entscheidungen lassen sich nicht rückgängig machen. Beim Verlassen geht der laufende Durchgang verloren."
                            },
                            style = MaterialTheme.typography.bodyMedium,
                            color = farben.tinteMatt,
                        )

                        Column(
                            modifier = Modifier.fillMaxWidth(),
                            verticalArrangement = Arrangement.spacedBy(8.dp),
                        ) {
                            ArchivPrimaerKnopf(
                                label = if (istAbgeschlossen) "Beim Lebenslauf bleiben" else "Im Durchgang bleiben",
                                onClick = onBleiben,
                                modifier = Modifier.fillMaxWidth(),
                            )
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.spacedBy(8.dp),
                            ) {
                                ArchivSekundaerKnopf(
                                    label = "Zum Startmenü",
                                    onClick = onZumStartmenue,
                                    modifier = Modifier.weight(1f),
                                )
                                if (onAppBeenden != null) {
                                    ArchivSekundaerKnopf(
                                        label = "App schließen",
                                        onClick = onAppBeenden,
                                        modifier = Modifier.weight(1f),
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
