package de.pytales.zdf.ui.screens

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import de.pytales.zdf.content.GameContent
import de.pytales.zdf.model.ModusKonfiguration
import de.pytales.zdf.model.OnboardingGrundsatz
import de.pytales.zdf.model.SpielModus
import de.pytales.zdf.ui.components.ArchivStempel
import de.pytales.zdf.ui.components.ArchivTrennlinie
import de.pytales.zdf.ui.components.SchriftgroessenSchalter
import de.pytales.zdf.ui.components.archivFokusGruppe
import de.pytales.zdf.ui.components.archivFokusRahmen
import de.pytales.zdf.ui.components.archivUeberschrift
import de.pytales.zdf.ui.state.SpielUiState
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.ArchivUebergaenge
import de.pytales.zdf.ui.theme.LayoutKlasse
import de.pytales.zdf.ui.theme.Schriftgroesse

/**
 * Startmenü (`GamePhase.Start`) im ruhigen Archivpapier-Design:
 * - Titel, Untertitel und Zielgruppe aus `content/konfiguration.json`
 * - Auswahl *Kurzer Verlauf* vs. *Langer Verlauf* (mit Umfang & Dauer)
 * - 3 per Tipp/Klick aufklappbare Onboarding-Grundsätze (`onboarding.grundsaetze`)
 * - Schriftgrößen-Schalter (`klein`/`mittel`/`gross`), ruhige Übergänge / Animationen reduzieren,
 *   optionaler dezenter Ton (mit harter Musiksperre an Front & Etappe), Analysemodus & Unterrichts-Direktwahl
 * - Dezenter Zugang zur AP-3-Komponenten-Vorschau für Lehrkräfte & Entwicklung.
 */
@Composable
fun StartScreen(
    content: GameContent,
    uiState: SpielUiState,
    onModusWaehlen: (SpielModus) -> Unit,
    onGrundsatzToggle: (String) -> Unit,
    onSchriftgroesseChange: (Schriftgroesse) -> Unit,
    onAnalyseModusToggle: () -> Unit,
    onReduzierteAnimationenToggle: () -> Unit,
    onAudioToggle: () -> Unit,
    onDirektwahlChange: (Boolean) -> Unit,
    onDurchgangBeginnen: () -> Unit,
    onUiVorschauOeffnen: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val konf = content.konfiguration
    val direktwahlOption = content.herkunft.direktwahlOption
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val layoutKlasse = ArchivTheme.layoutKlasse
    val aktiverModus = uiState.gameState.modus
    val direktwahlAktiv = uiState.gameState.direktwahlAktiv

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(farben.papier),
    ) {
        ArchivKopfBand(
            marke = "1914 – 1919",
            titel = konf.spielTitel,
            untertitel = "${konf.untertitel} · ${konf.zielgruppe}",
            schriftgroesse = uiState.schriftgroesse,
            onSchriftgroesseChange = onSchriftgroesseChange,
            analyseModus = uiState.analyseModus,
            onAnalyseModusToggle = onAnalyseModusToggle,
            audioZustand = uiState.audioZustand,
            onAudioToggle = onAudioToggle,
        )

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .verticalScroll(rememberScrollState()),
            contentAlignment = Alignment.TopCenter,
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .widthIn(max = metrik.maxInhaltsBreite)
                    .padding(horizontal = metrik.aussenAbstand, vertical = metrik.elementAbstand)
                    .archivFokusGruppe(),
                verticalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
            ) {
                // 1. Verlaufsauswahl (Kurzer Verlauf vs. Langer Verlauf)
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = farben.papierHell,
                    shape = RoundedCornerShape(4.dp),
                    border = BorderStroke(1.dp, farben.linie),
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(metrik.kartenInnenAbstand),
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            Text(
                                text = "Umfang des Durchgangs wählen",
                                style = MaterialTheme.typography.headlineSmall,
                                color = farben.tinte,
                                modifier = Modifier
                                    .weight(1f)
                                    .archivUeberschrift(),
                            )
                            ArchivStempel(
                                text = "OHNE PUNKTE",
                                farbe = farben.tinteMatt,
                                hintergrund = farben.papier,
                            )
                        }

                        val modi = listOf(SpielModus.KURZ, SpielModus.LANG)
                        val nebeneinander = layoutKlasse != LayoutKlasse.KOMPAKT &&
                            uiState.schriftgroesse != Schriftgroesse.GROSS

                        if (nebeneinander) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(IntrinsicSize.Min)
                                    .archivFokusGruppe(),
                                horizontalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
                            ) {
                                modi.forEach { modus ->
                                    val modusKonf = konf.modi.getValue(modus)
                                    ModusAuswahlKarte(
                                        modus = modus,
                                        konf = modusKonf,
                                        ausgewaehlt = modus == aktiverModus,
                                        onClick = { onModusWaehlen(modus) },
                                        modifier = Modifier
                                            .weight(1f)
                                            .fillMaxHeight(),
                                    )
                                }
                            }
                        } else {
                            Column(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .archivFokusGruppe(),
                                verticalArrangement = Arrangement.spacedBy(10.dp),
                            ) {
                                modi.forEach { modus ->
                                    val modusKonf = konf.modi.getValue(modus)
                                    ModusAuswahlKarte(
                                        modus = modus,
                                        konf = modusKonf,
                                        ausgewaehlt = modus == aktiverModus,
                                        onClick = { onModusWaehlen(modus) },
                                        modifier = Modifier.fillMaxWidth(),
                                    )
                                }
                            }
                        }

                        ArchivTrennlinie(farbe = farben.linieFein)

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            val gewaehltKonf = konf.modi.getValue(aktiverModus)
                            Column(
                                modifier = Modifier.weight(1f),
                                verticalArrangement = Arrangement.spacedBy(2.dp),
                            ) {
                                Text(
                                    text = "Ausgewählt: ${gewaehltKonf.bezeichnung}",
                                    style = MaterialTheme.typography.titleSmall,
                                    color = farben.tinte,
                                )
                                Text(
                                    text = if (direktwahlAktiv) {
                                        "Unterrichts-Direktwahl aktiv: Pfad wird nach der Herkunft direkt gewählt."
                                    } else {
                                        "Gestraffter Einstieg in den August 1914 mit Herkunft und Musterung bzw. Erwerb."
                                    },
                                    style = MaterialTheme.typography.bodySmall,
                                    color = farben.tinteMatt,
                                )
                            }

                            if (layoutKlasse != LayoutKlasse.KOMPAKT) {
                                ArchivPrimaerKnopf(
                                    label = "Durchgang beginnen",
                                    onClick = onDurchgangBeginnen,
                                )
                            }
                        }

                        if (layoutKlasse == LayoutKlasse.KOMPAKT) {
                            ArchivPrimaerKnopf(
                                label = "Durchgang beginnen",
                                onClick = onDurchgangBeginnen,
                                modifier = Modifier.fillMaxWidth(),
                            )
                        }
                    }
                }

                // 2. Drei aufklappbare Onboarding-Grundsätze
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = farben.papierHell,
                    shape = RoundedCornerShape(4.dp),
                    border = BorderStroke(1.dp, farben.linie),
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(metrik.kartenInnenAbstand),
                        verticalArrangement = Arrangement.spacedBy(10.dp),
                    ) {
                        Text(
                            text = "Drei Grundsätze vor Beginn",
                            style = MaterialTheme.typography.titleLarge,
                            color = farben.tinte,
                            modifier = Modifier.archivUeberschrift(),
                        )
                        Text(
                            text = konf.onboarding.aufforderung,
                            style = MaterialTheme.typography.bodySmall,
                            color = farben.tinteMatt,
                        )

                        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            konf.onboarding.grundsaetze.forEachIndexed { index, grundsatz ->
                                OnboardingGrundsatzKarte(
                                    nummer = index + 1,
                                    grundsatz = grundsatz,
                                    aufgeklappt = grundsatz.id in uiState.aufgeklappteGrundsaetze,
                                    onToggle = { onGrundsatzToggle(grundsatz.id) },
                                )
                            }
                        }
                    }
                }

                // 3. Einstellungen für Lesbarkeit, Zugänglichkeit, Audio & Unterricht
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = farben.papierHell,
                    shape = RoundedCornerShape(4.dp),
                    border = BorderStroke(1.dp, farben.linie),
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(metrik.kartenInnenAbstand),
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        Text(
                            text = "Lesbarkeit, Zugänglichkeit & Unterrichts-Optionen",
                            style = MaterialTheme.typography.titleLarge,
                            color = farben.tinte,
                            modifier = Modifier.archivUeberschrift(),
                        )

                        // Schriftgröße
                        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                            Text(
                                text = "Schriftgröße: ${uiState.schriftgroesse.bezeichnung} — ${uiState.schriftgroesse.beschreibung}",
                                style = MaterialTheme.typography.bodySmall,
                                color = farben.tinteMatt,
                            )
                            SchriftgroessenSchalter(
                                aktuell = uiState.schriftgroesse,
                                onAuswahl = onSchriftgroesseChange,
                                aufDunkel = false,
                                kompakt = false,
                            )
                        }

                        ArchivTrennlinie(farbe = farben.linieFein)

                        // Ruhige Übergänge / Animationen reduzieren (AP 6)
                        ArchivSchalterZeile(
                            titel = "Ruhige Übergänge: Animationen reduzieren",
                            beschreibung = "Schaltet sanfte Phasen- und Kartenübergänge sowie Aufklapp-Animationen ab — für sofortige, vollkommen ruhige Wechsel auf Beamer, bei Bewegungsempfindlichkeit oder mit Bildschirmleser.",
                            aktiv = uiState.reduzierteAnimationen,
                            onToggle = onReduzierteAnimationenToggle,
                            statusLabelAktiv = "REDUZIERT",
                            statusLabelInaktiv = "SANFT",
                        )

                        // Optionaler dezenter Ton mit harter Musiksperre an Front & Etappe (AP 6)
                        ArchivSchalterZeile(
                            titel = "Dezenter Ton (Musiksperre an Front & Etappe)",
                            beschreibung = "Sehr leise, ruhige Begleitung im Startmenü und in der Heimat. Auf den Pfaden Front und Etappe sowie bei vorzeitigem Einschnitt herrscht strikt respektvolle Stille.",
                            aktiv = uiState.audioAktiv,
                            onToggle = onAudioToggle,
                            statusLabelAktiv = "LEISE",
                            statusLabelInaktiv = "STUMM",
                        )

                        // Analysemodus
                        ArchivSchalterZeile(
                            titel = "Analysemodus (Quellen & Archiv-Hinweise)",
                            beschreibung = "Öffnet historische Quellen, Vollbelege, Vertiefungshinweise und Archiv-IDs auf jeder Karte automatisch für das Unterrichtsgespräch.",
                            aktiv = uiState.analyseModus,
                            onToggle = onAnalyseModusToggle,
                        )

                        // Unterrichts-Schalter „Pfad direkt wählen“
                        if (direktwahlOption.aktiv) {
                            ArchivSchalterZeile(
                                titel = "Pfad direkt wählen (Unterrichts-Schalter)",
                                beschreibung = direktwahlOption.beschreibung,
                                aktiv = direktwahlAktiv,
                                onToggle = { onDirektwahlChange(!direktwahlAktiv) },
                            )
                        }
                    }
                }

                // 4. Dezenter Fußbereich mit Link zur AP-3-Komponenten-Vorschau (mind. 48 dp Touch-Ziel)
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 4.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text(
                        text = "PyTales Lernspiele · ${konf.zielgruppe}",
                        style = MaterialTheme.typography.labelSmall,
                        color = farben.tinteMatt,
                        modifier = Modifier.weight(1f),
                    )
                    Box(
                        modifier = Modifier
                            .defaultMinSize(minWidth = metrik.minTouchHoehe, minHeight = metrik.minTouchHoehe)
                            .clip(RoundedCornerShape(3.dp))
                            .border(1.dp, farben.linie, RoundedCornerShape(3.dp))
                            .archivFokusRahmen(eckRadius = 3.dp, aufDunkel = false)
                            .clickable(onClick = onUiVorschauOeffnen)
                            .semantics {
                                role = Role.Button
                                contentDescription = "UI- und Bildwelt-Vorschau für Lehrkräfte und Entwicklung öffnen"
                            }
                            .padding(horizontal = 12.dp, vertical = 8.dp),
                        contentAlignment = Alignment.Center,
                    ) {
                        Text(
                            text = "UI-Vorschau (AP 3)",
                            style = MaterialTheme.typography.labelSmall,
                            color = farben.tinte,
                        )
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
}

@Composable
private fun ModusAuswahlKarte(
    modus: SpielModus,
    konf: ModusKonfiguration,
    ausgewaehlt: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val flaeche = if (ausgewaehlt) farben.papierDunkel else farben.papier
    val rahmen = if (ausgewaehlt) farben.akzent else farben.linie

    Surface(
        modifier = modifier
            .defaultMinSize(minHeight = 120.dp)
            .clip(RoundedCornerShape(4.dp))
            .archivFokusRahmen(eckRadius = 4.dp, aufDunkel = false)
            .clickable(onClick = onClick)
            .clearAndSetSemantics {
                role = Role.RadioButton
                selected = ausgewaehlt
                stateDescription = if (ausgewaehlt) "Ausgewählt" else "Nicht ausgewählt"
                contentDescription = "${konf.bezeichnung}: ${konf.umfang} ${konf.dauer}"
            },
        color = flaeche,
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(if (ausgewaehlt) 2.dp else 1.dp, rahmen),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = konf.bezeichnung,
                    style = MaterialTheme.typography.titleMedium,
                    color = farben.tinte,
                    fontWeight = FontWeight.Bold,
                )
                ArchivStempel(
                    text = if (ausgewaehlt) "GEWÄHLT" else "${konf.zielzahl} KARTEN",
                    farbe = if (ausgewaehlt) farben.akzent else farben.tinteMatt,
                    hintergrund = farben.papierHell,
                )
            }

            Text(
                text = konf.umfang,
                style = MaterialTheme.typography.bodyMedium,
                color = farben.tinte,
            )

            Text(
                text = konf.dauer,
                style = MaterialTheme.typography.bodySmall,
                color = farben.tinteMatt,
            )

            if (modus == SpielModus.KURZ) {
                Text(
                    text = "Empfohlen für eine 45-Minuten-Stunde.",
                    style = MaterialTheme.typography.labelSmall,
                    color = farben.akzent,
                )
            }
        }
    }
}

@Composable
private fun OnboardingGrundsatzKarte(
    nummer: Int,
    grundsatz: OnboardingGrundsatz,
    aufgeklappt: Boolean,
    onToggle: () -> Unit,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val reduziert = ArchivTheme.reduzierteAnimationen

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .border(1.dp, if (aufgeklappt) farben.akzent else farben.linieFein, RoundedCornerShape(3.dp))
            .background(if (aufgeklappt) farben.papier else farben.papier.copy(alpha = 0.6f), RoundedCornerShape(3.dp)),
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .defaultMinSize(minHeight = metrik.minTouchHoehe)
                .archivFokusRahmen(eckRadius = 3.dp, aufDunkel = false)
                .clickable(onClick = onToggle)
                .clearAndSetSemantics {
                    role = Role.Button
                    selected = aufgeklappt
                    stateDescription = if (aufgeklappt) "Aufgeklappt" else "Zugeklappt"
                    contentDescription = if (aufgeklappt) {
                        "Grundsatz $nummer: ${grundsatz.satz} zuklappen"
                    } else {
                        "Grundsatz $nummer: ${grundsatz.satz} aufklappen"
                    }
                }
                .padding(horizontal = 12.dp, vertical = 10.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Row(
                horizontalArrangement = Arrangement.spacedBy(10.dp),
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.weight(1f),
            ) {
                ArchivStempel(
                    text = "0$nummer",
                    farbe = if (aufgeklappt) farben.akzent else farben.tinteMatt,
                    hintergrund = farben.papierHell,
                )
                Text(
                    text = grundsatz.satz,
                    style = MaterialTheme.typography.titleSmall,
                    color = farben.tinte,
                    fontWeight = FontWeight.SemiBold,
                )
            }
            Text(
                text = if (aufgeklappt) "Weniger ▴" else "Mehr ▾",
                style = MaterialTheme.typography.labelSmall,
                color = farben.tinteMatt,
            )
        }

        AnimatedVisibility(
            visible = aufgeklappt,
            enter = ArchivUebergaenge.aufklappEnter(reduziert),
            exit = ArchivUebergaenge.aufklappExit(reduziert),
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(farben.papierHell)
                    .padding(horizontal = 14.dp, vertical = 10.dp),
            ) {
                Text(
                    text = grundsatz.mehr,
                    style = MaterialTheme.typography.bodyMedium,
                    color = farben.tinte,
                )
            }
        }
    }
}
