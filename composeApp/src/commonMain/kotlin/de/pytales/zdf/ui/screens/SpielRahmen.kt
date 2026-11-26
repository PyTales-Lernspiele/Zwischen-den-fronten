package de.pytales.zdf.ui.screens

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
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
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.HorizontalDivider
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
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import de.pytales.zdf.audio.AudioSperrGrund
import de.pytales.zdf.audio.AudioZustand
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.components.ArchivStempel
import de.pytales.zdf.ui.components.ArchivTrennlinie
import de.pytales.zdf.ui.components.KopfLeiste
import de.pytales.zdf.ui.components.SchriftgroessenSchalter
import de.pytales.zdf.ui.components.archivEscapeAktion
import de.pytales.zdf.ui.components.archivFokusGruppe
import de.pytales.zdf.ui.components.archivFokusRahmen
import de.pytales.zdf.ui.components.archivLiveHinweis
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.media.ArchivKapitelBild
import de.pytales.zdf.ui.media.BildAufloeser
import de.pytales.zdf.ui.media.LocalMedienRegister
import de.pytales.zdf.ui.state.KapitelbildUiState
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.state.UiStateMapper
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.LayoutKlasse
import de.pytales.zdf.ui.theme.Schriftgroesse

/**
 * Dunkles Archiv-Kopfband für Bildschirme ohne Befindensleiste
 * (`Start`, `HerkunftWahl` und `Abgeschlossen`) mit klar sichtbarem Stummschalter,
 * Analysemodus-Schalter, dreistufiger Schriftgröße (alle Touch-Ziele ≥ 48 dp)
 * und Safe-Area-Insets für Statusleiste & Kamera-Notch.
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
internal fun ArchivKopfBand(
    marke: String,
    titel: String,
    schriftgroesse: Schriftgroesse,
    onSchriftgroesseChange: (Schriftgroesse) -> Unit,
    analyseModus: Boolean,
    onAnalyseModusToggle: (() -> Unit)? = null,
    audioZustand: AudioZustand? = null,
    onAudioToggle: (() -> Unit)? = null,
    untertitel: String? = null,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val kompakt = ArchivTheme.layoutKlasse == LayoutKlasse.KOMPAKT

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
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .windowInsetsPadding(
                        WindowInsets.safeDrawing.only(WindowInsetsSides.Top + WindowInsetsSides.Horizontal),
                    )
                    .widthIn(max = metrik.maxInhaltsBreite)
                    .padding(horizontal = metrik.aussenAbstand, vertical = 12.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
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
                        ArchivStempel(
                            text = marke,
                            farbe = farben.stufenFarbeHell(2),
                            hintergrund = farben.dunkelHell,
                        )
                        if (!untertitel.isNullOrBlank() && !kompakt) {
                            Text(
                                text = untertitel,
                                style = MaterialTheme.typography.labelMedium,
                                color = farben.textHell.copy(alpha = 0.84f),
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis,
                            )
                        }
                    }

                    if (!kompakt) {
                        Row(
                            horizontalArrangement = Arrangement.spacedBy(6.dp),
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            if (audioZustand != null && onAudioToggle != null) {
                                AudioKopfKnopf(
                                    audioZustand = audioZustand,
                                    kompakt = false,
                                    onToggle = onAudioToggle,
                                )
                            }
                            if (onAnalyseModusToggle != null) {
                                AnalyseModusKopfKnopf(
                                    aktiv = analyseModus,
                                    kompakt = false,
                                    onToggle = onAnalyseModusToggle,
                                )
                            }
                            SchriftgroessenSchalter(
                                aktuell = schriftgroesse,
                                onAuswahl = onSchriftgroesseChange,
                                aufDunkel = true,
                                kompakt = false,
                            )
                        }
                    }
                }

                if (kompakt) {
                    FlowRow(
                        horizontalArrangement = Arrangement.spacedBy(6.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp),
                        itemVerticalAlignment = Alignment.CenterVertically,
                    ) {
                        if (audioZustand != null && onAudioToggle != null) {
                            AudioKopfKnopf(
                                audioZustand = audioZustand,
                                kompakt = true,
                                onToggle = onAudioToggle,
                            )
                        }
                        if (onAnalyseModusToggle != null) {
                            AnalyseModusKopfKnopf(
                                aktiv = analyseModus,
                                kompakt = true,
                                onToggle = onAnalyseModusToggle,
                            )
                        }
                        SchriftgroessenSchalter(
                            aktuell = schriftgroesse,
                            onAuswahl = onSchriftgroesseChange,
                            aufDunkel = true,
                            kompakt = true,
                        )
                    }
                }

                Text(
                    text = titel,
                    style = if (kompakt) {
                        MaterialTheme.typography.headlineMedium
                    } else {
                        MaterialTheme.typography.headlineLarge
                    },
                    color = farben.textHell,
                    modifier = Modifier.archivUeberschrift(),
                )
                if (!untertitel.isNullOrBlank() && kompakt) {
                    Text(
                        text = untertitel,
                        style = MaterialTheme.typography.bodySmall,
                        color = farben.textHell.copy(alpha = 0.84f),
                    )
                }
            }
        }
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(3.dp)
                .background(farben.akzent),
        )
        HorizontalDivider(thickness = 1.dp, color = farben.linie)
    }
}

/**
 * Spiel-Kopfleiste mit vollständiger [KopfLeiste] (Befindensleiste + Live-Emotions-Kachel)
 * sowie dezentem Stummschalter (inkl. Anzeige der Musiksperre an Front & Etappe),
 * Schriftgrößen- und Analysemodus-Zugriff für den Unterricht.
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
internal fun SpielKopfLeiste(
    engine: GameEngine,
    uiState: SpielUiState,
    onSchriftgroesseChange: (Schriftgroesse) -> Unit,
    onAnalyseModusToggle: () -> Unit,
    onAudioToggle: () -> Unit,
    onWertErklaerungChange: (WertSchluessel?) -> Unit,
    onEmotionDetailsOffenChange: (Boolean) -> Unit = {},
    modifier: Modifier = Modifier,
) {
    val gameState = uiState.gameState
    val kompakt = ArchivTheme.layoutKlasse == LayoutKlasse.KOMPAKT
    val werteUi = remember(engine, gameState) {
        UiStateMapper.mapBefindensLeiste(engine, gameState)
    }
    val emotionUi = remember(engine, gameState) {
        UiStateMapper.mapLiveEmotion(engine, gameState)
    }
    val kapitelTitel = remember(engine.content, gameState) {
        UiStateMapper.mapKopfKapitelTitel(engine.content, gameState)
    }

    KopfLeiste(
        jahr = gameState.jahr,
        werte = werteUi,
        emotion = emotionUi,
        kapitelTitel = kapitelTitel,
        analyseModus = uiState.analyseModus,
        ausgewaehlterWert = uiState.ausgewaehlterWert,
        onAusgewaehlterWertChange = onWertErklaerungChange,
        emotionDetailsOffen = uiState.emotionDetailsOffen,
        onEmotionDetailsOffenChange = onEmotionDetailsOffenChange,
        zusatzAktionen = {
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                verticalArrangement = Arrangement.spacedBy(6.dp),
                itemVerticalAlignment = Alignment.CenterVertically,
            ) {
                AudioKopfKnopf(
                    audioZustand = uiState.audioZustand,
                    kompakt = kompakt,
                    onToggle = onAudioToggle,
                )
                AnalyseModusKopfKnopf(
                    aktiv = uiState.analyseModus,
                    kompakt = kompakt,
                    onToggle = onAnalyseModusToggle,
                )
                SchriftgroessenSchalter(
                    aktuell = uiState.schriftgroesse,
                    onAuswahl = onSchriftgroesseChange,
                    aufDunkel = true,
                    kompakt = kompakt,
                )
            }
        },
        modifier = modifier,
    )
}

/**
 * Klar sichtbarer Stummschalter in der Kopfleiste.
 * Zeigt auf `front`, `etappe` und im Auffangnetz ausdrücklich die respektvolle Stille
 * (harte Musiksperre) an, während die allgemeine Toneinstellung weiterhin umgeschaltet
 * werden kann (ohne dass auf gesperrten Pfaden jemals Musik erklingt).
 */
@Composable
internal fun AudioKopfKnopf(
    audioZustand: AudioZustand,
    kompakt: Boolean,
    onToggle: () -> Unit,
) {
    val farben = ArchivTheme.farben
    val minTouch = ArchivTheme.metrik.minTouchHoehe
    val gesperrt = audioZustand.musikGesperrt
    val spielt = audioZustand.spieltGerade

    val flaeche = when {
        gesperrt -> farben.dunkelHell
        spielt -> farben.stufenFarbe(0)
        else -> farben.dunkelHell
    }
    val rahmen = when {
        gesperrt -> farben.segmentDunkel
        spielt -> farben.stufenFarbeHell(0)
        else -> farben.linie.copy(alpha = 0.65f)
    }
    val textFarbe = when {
        gesperrt -> farben.textHell.copy(alpha = 0.86f)
        spielt -> farben.papierHell
        else -> farben.textHell
    }

    val anzeigeText = when {
        gesperrt -> when (audioZustand.sperrGrund) {
            AudioSperrGrund.PFAD_FRONT -> if (kompakt) "Stille" else "Stille · Front"
            AudioSperrGrund.PFAD_ETAPPE -> if (kompakt) "Stille" else "Stille · Etappe"
            else -> "Stille"
        }

        spielt -> if (kompakt) "Ton: An" else "Ton: Leise"
        else -> if (kompakt) "Stumm" else "Ton: Aus"
    }

    val statusText = when {
        gesperrt -> audioZustand.sperrGrund?.hinweis ?: "Respektvolle Stille."
        spielt -> "Dezenter Ton eingeschaltet (${audioZustand.aktiveSpur.bezeichnung})."
        else -> "Stummgeschaltet."
    }

    val beschreibung = when {
        gesperrt -> "$statusText Tippen, um die allgemeine Ton-Einstellung (${if (audioZustand.audioAktiv) "ein" else "aus"}) für Startmenü und Heimat umzuschalten."
        spielt -> "$statusText Tippen zum Stummschalten."
        else -> "$statusText Tippen, um dezenten Ton für Startmenü und Heimat einzuschalten."
    }

    Surface(
        modifier = Modifier
            .defaultMinSize(minWidth = minTouch, minHeight = minTouch)
            .clip(RoundedCornerShape(3.dp))
            .archivFokusRahmen(eckRadius = 3.dp, aufDunkel = true)
            .clickable(onClick = onToggle)
            .clearAndSetSemantics {
                role = Role.Switch
                selected = audioZustand.audioAktiv && !gesperrt
                stateDescription = statusText
                contentDescription = beschreibung
            },
        color = flaeche,
        shape = RoundedCornerShape(3.dp),
        border = BorderStroke(1.dp, rahmen),
    ) {
        Box(
            modifier = Modifier.padding(horizontal = if (kompakt) 10.dp else 12.dp, vertical = 8.dp),
            contentAlignment = Alignment.Center,
        ) {
            Text(
                text = anzeigeText,
                style = MaterialTheme.typography.labelMedium,
                color = textFarbe,
                fontWeight = if (spielt) FontWeight.Bold else FontWeight.Medium,
                maxLines = 1,
            )
        }
    }
}

@Composable
internal fun AnalyseModusKopfKnopf(
    aktiv: Boolean,
    kompakt: Boolean,
    onToggle: () -> Unit,
) {
    val farben = ArchivTheme.farben
    val minTouch = ArchivTheme.metrik.minTouchHoehe
    val flaeche = if (aktiv) farben.akzent else farben.dunkelHell
    val rahmen = if (aktiv) farben.stufenFarbeHell(2) else farben.linie.copy(alpha = 0.65f)
    val textFarbe = if (aktiv) farben.papierHell else farben.textHell

    Surface(
        modifier = Modifier
            .defaultMinSize(minWidth = minTouch, minHeight = minTouch)
            .clip(RoundedCornerShape(3.dp))
            .archivFokusRahmen(eckRadius = 3.dp, aufDunkel = true)
            .clickable(onClick = onToggle)
            .clearAndSetSemantics {
                role = Role.Switch
                selected = aktiv
                stateDescription = if (aktiv) "Eingeschaltet" else "Ausgeschaltet"
                contentDescription = if (aktiv) {
                    "Analysemodus ist eingeschaltet. Tippen zum Ausschalten."
                } else {
                    "Analysemodus ist ausgeschaltet. Tippen zum Einschalten."
                }
            },
        color = flaeche,
        shape = RoundedCornerShape(3.dp),
        border = BorderStroke(1.dp, rahmen),
    ) {
        Box(
            modifier = Modifier.padding(horizontal = if (kompakt) 10.dp else 12.dp, vertical = 8.dp),
            contentAlignment = Alignment.Center,
        ) {
            Text(
                text = if (kompakt) {
                    if (aktiv) "Analyse ✓" else "Analyse"
                } else {
                    if (aktiv) "Analysemodus: Ein" else "Analysemodus"
                },
                style = MaterialTheme.typography.labelMedium,
                color = textFarbe,
                fontWeight = if (aktiv) FontWeight.Bold else FontWeight.Medium,
                maxLines = 1,
            )
        }
    }
}

/**
 * Kontraststarker primärer Archiv-Button (z. B. „Durchgang beginnen“, „Weiter“, „Neuer Durchgang“).
 */
@Composable
internal fun ArchivPrimaerKnopf(
    label: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    aktiviert: Boolean = true,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val flaeche = if (aktiviert) farben.tinte else farben.papierDunkel
    val textFarbe = if (aktiviert) farben.papierHell else farben.tinteMatt
    val rahmen = if (aktiviert) farben.tinte else farben.linie

    Surface(
        modifier = modifier
            .defaultMinSize(minWidth = metrik.minTouchHoehe, minHeight = metrik.minTouchHoehe)
            .clip(RoundedCornerShape(4.dp))
            .archivFokusRahmen(eckRadius = 4.dp, aufDunkel = false)
            .clickable(enabled = aktiviert, onClick = onClick)
            .semantics {
                role = Role.Button
                contentDescription = label
            },
        color = flaeche,
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(1.dp, rahmen),
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
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik

    Surface(
        modifier = modifier
            .defaultMinSize(minWidth = metrik.minTouchHoehe, minHeight = metrik.minTouchHoehe)
            .clip(RoundedCornerShape(4.dp))
            .archivFokusRahmen(eckRadius = 4.dp, aufDunkel = false)
            .clickable(enabled = aktiviert, onClick = onClick)
            .semantics {
                role = Role.Button
                contentDescription = label
            },
        color = if (aktiviert) farben.papierHell else farben.papier,
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(1.dp, if (aktiviert) farben.linie else farben.linieFein),
    ) {
        Box(
            modifier = Modifier.padding(horizontal = 18.dp, vertical = 12.dp),
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
 * Touch-/Klick-Umschalter im Archivstil für Optionen im Startmenü
 * (Analysemodus, Animationen reduzieren, Dezenter Ton, Unterrichts-Direktwahl).
 */
@Composable
internal fun ArchivSchalterZeile(
    titel: String,
    beschreibung: String,
    aktiv: Boolean,
    onToggle: () -> Unit,
    modifier: Modifier = Modifier,
    statusLabelAktiv: String = "EIN",
    statusLabelInaktiv: String = "AUS",
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik

    Surface(
        modifier = modifier
            .fillMaxWidth()
            .defaultMinSize(minHeight = metrik.minTouchHoehe)
            .clip(RoundedCornerShape(4.dp))
            .archivFokusRahmen(eckRadius = 4.dp, aufDunkel = false)
            .clickable(onClick = onToggle)
            .clearAndSetSemantics {
                role = Role.Switch
                selected = aktiv
                stateDescription = if (aktiv) "Eingeschaltet" else "Ausgeschaltet"
                contentDescription = "$titel: ${if (aktiv) "eingeschaltet" else "ausgeschaltet"}. $beschreibung"
            },
        color = if (aktiv) farben.papierDunkel.copy(alpha = 0.72f) else farben.papier,
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(if (aktiv) 1.5.dp else 1.dp, if (aktiv) farben.akzent else farben.linieFein),
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 14.dp, vertical = 12.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(3.dp),
            ) {
                Text(
                    text = titel,
                    style = MaterialTheme.typography.titleSmall,
                    color = farben.tinte,
                    fontWeight = FontWeight.SemiBold,
                )
                Text(
                    text = beschreibung,
                    style = MaterialTheme.typography.bodySmall,
                    color = farben.tinteMatt,
                )
            }

            ArchivStempel(
                text = if (aktiv) statusLabelAktiv else statusLabelInaktiv,
                farbe = if (aktiv) farben.akzent else farben.tinteMatt,
                hintergrund = if (aktiv) farben.papierHell else farben.papierHell,
                grossbuchstaben = true,
            )
        }
    }
}

/**
 * Ruhiger 16:9-Kapitelbild-Rahmen (`1280×720` gemäß `content/medienplan.json`):
 * nutzt standardmäßig [ArchivKapitelBild] (`kapitel_1914`..`kapitel_1919`, WebP) mit
 * automatischem Fallback auf die bisherige Archiv-Kapiteltafel.
 */
@Composable
internal fun KapitelbildRahmen(
    kapitelbild: KapitelbildUiState,
    analyseModus: Boolean,
    modifier: Modifier = Modifier,
    bildContent: (@Composable BoxScope.(bildId: String) -> Unit)? = null,
) {
    val farben = ArchivTheme.farben
    val medienRegister = LocalMedienRegister.current
    val aufgeloest = remember(kapitelbild.bildId, medienRegister) {
        BildAufloeser.loeseKapitel(kapitelbild.bildId, medienRegister.verfuegbareIds)
    }
    val rahmenBeschreibung =
        "Kapitelbild ${kapitelbild.jahr}: ${kapitelbild.ueberschrift} (${kapitelbild.zeitraum})"

    Surface(
        modifier = modifier
            .fillMaxWidth()
            .semantics { contentDescription = rahmenBeschreibung },
        color = farben.papierDunkel,
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(1.dp, farben.linie),
    ) {
        Column(modifier = Modifier.fillMaxWidth()) {
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
                            val eckLaenge = 16.dp.toPx()

                            drawRect(
                                color = farben.linieFein.copy(alpha = 0.72f),
                                topLeft = Offset(inset, inset),
                                size = Size(w - 2 * inset, h - 2 * inset),
                                style = Stroke(width = 1f),
                            )

                            val markenFarbe = farben.linie.copy(alpha = 0.9f)
                            val strich = 1.5f
                            drawLine(markenFarbe, Offset(inset, inset), Offset(inset + eckLaenge, inset), strich)
                            drawLine(markenFarbe, Offset(inset, inset), Offset(inset, inset + eckLaenge), strich)
                            drawLine(markenFarbe, Offset(w - inset - eckLaenge, inset), Offset(w - inset, inset), strich)
                            drawLine(markenFarbe, Offset(w - inset, inset), Offset(w - inset, inset + eckLaenge), strich)
                            drawLine(markenFarbe, Offset(inset, h - inset), Offset(inset + eckLaenge, h - inset), strich)
                            drawLine(markenFarbe, Offset(inset, h - inset - eckLaenge), Offset(inset, h - inset), strich)
                            drawLine(markenFarbe, Offset(w - inset - eckLaenge, h - inset), Offset(w - inset, h - inset), strich)
                            drawLine(markenFarbe, Offset(w - inset, h - inset - eckLaenge), Offset(w - inset, h - inset), strich)

                            val horizontY = h * 0.72f
                            drawLine(
                                color = farben.linieFein.copy(alpha = 0.5f),
                                start = Offset(inset * 2f, horizontY),
                                end = Offset(w - inset * 2f, horizontY),
                                strokeWidth = 1f,
                            )
                        }

                        Column(
                            modifier = Modifier
                                .align(Alignment.Center)
                                .padding(horizontal = 24.dp),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.spacedBy(6.dp),
                        ) {
                            Text(
                                text = kapitelbild.jahr.toString(),
                                style = MaterialTheme.typography.displaySmall,
                                color = farben.akzent,
                                textAlign = TextAlign.Center,
                            )
                            Text(
                                text = kapitelbild.ueberschrift,
                                style = MaterialTheme.typography.headlineSmall,
                                color = farben.tinte,
                                textAlign = TextAlign.Center,
                                maxLines = 2,
                                overflow = TextOverflow.Ellipsis,
                            )
                            Text(
                                text = kapitelbild.zeitraum,
                                style = MaterialTheme.typography.bodySmall,
                                fontStyle = FontStyle.Italic,
                                color = farben.tinteMatt,
                                textAlign = TextAlign.Center,
                            )
                            Text(
                                text = "Kapiteltafel 16:9",
                                style = MaterialTheme.typography.labelSmall,
                                color = farben.tinteMatt,
                                textAlign = TextAlign.Center,
                            )
                        }
                    }
                }

                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .align(Alignment.TopStart)
                        .padding(14.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    ArchivStempel(
                        text = if (kapitelbild.istEpilog) "EPILOG ${kapitelbild.jahr}" else "KAPITEL ${kapitelbild.jahr}",
                        farbe = farben.akzent,
                        hintergrund = farben.papierHell.copy(alpha = 0.94f),
                    )
                    ArchivStempel(
                        text = kapitelbild.pfadMarke,
                        farbe = farben.tinteMatt,
                        hintergrund = farben.papierHell.copy(alpha = 0.94f),
                    )
                }
            }

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
                        "Kapitelbild: ${kapitelbild.bildId} (${aufgeloest.ebene.kurzLabel})"
                    } else {
                        "${kapitelbild.ueberschrift} · ${kapitelbild.zeitraum}"
                    },
                    style = MaterialTheme.typography.labelSmall,
                    color = if (analyseModus) farben.tinte else farben.tinteMatt,
                    fontWeight = if (analyseModus) FontWeight.SemiBold else FontWeight.Normal,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f),
                )
                if (analyseModus) {
                    Text(
                        text = kapitelbild.ressourcenPfad,
                        style = MaterialTheme.typography.labelSmall,
                        color = farben.tinteMatt,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                    )
                }
            }
        }
    }
}

/**
 * Ergänzt sichere horizontale und untere Safe-Area-Abstände (`WindowInsets.safeDrawing`)
 * für scrollbare Inhaltsbereiche unterhalb der Kopfleiste, damit Karten und Schaltflächen
 * niemals hinter Navigationsleiste, Gesten-Balken oder seitlicher Kamera-Notch verschwinden.
 */
@Composable
internal fun Modifier.archivInhaltsSafeArea(): Modifier =
    this.windowInsetsPadding(
        WindowInsets.safeDrawing.only(WindowInsetsSides.Horizontal + WindowInsetsSides.Bottom),
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
    val metrik = ArchivTheme.metrik

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
                .padding(horizontal = 20.dp, vertical = 16.dp)
                .archivEscapeAktion(aktiv = true, onEscape = onBleiben),
            contentAlignment = Alignment.Center,
        ) {
            Surface(
                modifier = Modifier
                    .fillMaxWidth()
                    .widthIn(max = 480.dp)
                    .archivFokusGruppe()
                    .archivLiveHinweis(),
                color = farben.papierHell,
                shape = RoundedCornerShape(4.dp),
                border = BorderStroke(1.25.dp, farben.tinte),
                shadowElevation = 6.dp,
            ) {
                Column(modifier = Modifier.fillMaxWidth()) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(3.dp)
                            .background(farben.akzent),
                    )
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(metrik.kartenInnenAbstand),
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        ArchivStempel(
                            text = if (istAbgeschlossen) "LEBENSLAUF · HINWEIS" else "KEIN ZURÜCK · DURCHGANG",
                            farbe = farben.akzent,
                            hintergrund = farben.papier,
                        )
                        Text(
                            text = if (istAbgeschlossen) {
                                "Abgeschlossenen Durchgang verlassen?"
                            } else {
                                "Laufenden Durchgang wirklich verlassen?"
                            },
                            style = MaterialTheme.typography.headlineSmall,
                            color = farben.tinte,
                            modifier = Modifier.archivUeberschrift(),
                        )
                        Text(
                            text = if (istAbgeschlossen) {
                                "Dein 4-Fächer-Lebenslauf ist fertig. Wenn du jetzt zum Startmenü wechselst oder die App schließt, wird dieser Durchgang zurückgesetzt."
                            } else {
                                "In „Zwischen den Fronten“ lässt sich keine Entscheidung rückgängig machen. Wenn du jetzt zum Startmenü wechselst oder die App schließt, geht der laufende Durchgang verloren."
                            },
                            style = MaterialTheme.typography.bodyMedium,
                            color = farben.tinte,
                        )

                        ArchivTrennlinie(farbe = farben.linieFein)

                        Column(
                            modifier = Modifier.fillMaxWidth(),
                            verticalArrangement = Arrangement.spacedBy(8.dp),
                        ) {
                            ArchivPrimaerKnopf(
                                label = if (istAbgeschlossen) "Beim Lebenslauf bleiben" else "Im Durchgang bleiben",
                                onClick = onBleiben,
                                modifier = Modifier.fillMaxWidth(),
                            )
                            ArchivSekundaerKnopf(
                                label = if (istAbgeschlossen) {
                                    "Zum Startmenü (Neuer Durchgang)"
                                } else {
                                    "Durchgang beenden & zum Startmenü"
                                },
                                onClick = onZumStartmenue,
                                modifier = Modifier.fillMaxWidth(),
                            )
                            if (onAppBeenden != null) {
                                ArchivSekundaerKnopf(
                                    label = "App schließen",
                                    onClick = onAppBeenden,
                                    modifier = Modifier.fillMaxWidth(),
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}
