package de.pytales.zdf.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
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
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import de.pytales.zdf.audio.SoundEffekt
import de.pytales.zdf.model.Kartentyp
import de.pytales.zdf.ui.state.EntscheidungsKarteUiState
import de.pytales.zdf.ui.state.EntscheidungsOptionUiState
import de.pytales.zdf.ui.state.EreignisAusgangUiState
import de.pytales.zdf.ui.state.QuelleUiState
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.LocalSoundEffektSpielen

/**
 * Offene Buchseiten-Ansicht für die Entscheidungsphase (`GamePhase.EreignisAnzeige`):
 * - Bewusst **ohne Kasten-in-Kasten-Rahmen** — die Typografie ruht unmittelbar auf dem warmen
 *   Archivpapier wie auf einer aufgeschlagenen Buchseite.
 * - Klarer typspezifischer Titel (Alltagsbericht, Feldpostbrief, Lebensmittelkarte, Tagesblatt,
 *   Amtliche Verfügung), unaufdringlicher Link „Quelle“ (öffnet ein ruhiges Quellen-Overlay),
 *   ruhiger Erzähltext und exakt **zwei klar getrennte Entscheidungs-Buttons**.
 */
@Composable
fun EntscheidungsKarte(
    karte: EntscheidungsKarteUiState,
    onOptionWaehlen: (Int) -> Unit,
    modifier: Modifier = Modifier,
    ausgewaehlteOptionIndex: Int? = null,
    optionenAktiv: Boolean = true,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val kompakt = metrik.kompakteHoehe
    var quelleOffen by remember(karte.ereignisId) { mutableStateOf(false) }

    Column(
        modifier = modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(if (kompakt) 12.dp else 16.dp),
    ) {
        // Ruhiger offener Buchseiten-Kopf: klarer Titel links, dezenter Link „Quelle“ rechts
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(3.dp),
            ) {
                Text(
                    text = offenerKartenTitel(karte.kartentyp),
                    style = if (kompakt) MaterialTheme.typography.titleLarge else MaterialTheme.typography.headlineSmall,
                    fontFamily = FontFamily.Serif,
                    color = if (karte.kartentyp == Kartentyp.KARTE) farben.akzent else farben.tinte,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.archivUeberschrift(),
                )
                if (karte.kartentyp == Kartentyp.ZEITUNG || karte.kartentyp == Kartentyp.AMTLICH) {
                    ArchivTrennlinie(
                        farbe = farben.tinte.copy(alpha = 0.42f),
                        doppelt = true,
                    )
                }
            }

            QuellenLink(
                onClick = { quelleOffen = true },
            )
        }

        // Ruhiger Erzähltext direkt auf dem Archivpapier
        KartenTextOffen(
            kartentyp = karte.kartentyp,
            text = karte.text,
        )

        // Exakt zwei klar getrennte, gleichwertige Entscheidungs-Buttons
        EntscheidungsOptionenGruppe(
            optionen = karte.optionen,
            ausgewaehlteOptionIndex = ausgewaehlteOptionIndex,
            aktiv = optionenAktiv,
            nebeneinanderErlaubt = false,
            onOptionWaehlen = onOptionWaehlen,
        )
    }

    if (quelleOffen) {
        QuelleOverlayDialog(
            quelle = karte.quelle,
            onSchliessen = { quelleOffen = false },
        )
    }
}

private fun offenerKartenTitel(kartentyp: Kartentyp): String = when (kartentyp) {
    Kartentyp.KARTE -> "Alltagsbericht"
    Kartentyp.FELDPOST -> "Feldpostbrief"
    Kartentyp.LEBENSMITTEL -> "Lebensmittelkarte"
    Kartentyp.ZEITUNG -> "Tagesblatt"
    Kartentyp.AMTLICH -> "Amtliche Verfügung"
}

@Composable
private fun KartenTextOffen(
    kartentyp: Kartentyp,
    text: String,
) {
    val farben = ArchivTheme.farben

    when (kartentyp) {
        Kartentyp.FELDPOST -> {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(IntrinsicSize.Min),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                Box(
                    modifier = Modifier
                        .width(2.dp)
                        .fillMaxHeight()
                        .background(farben.akzentMatt.copy(alpha = 0.55f)),
                )
                Text(
                    text = text,
                    style = MaterialTheme.typography.bodyLarge,
                    color = farben.tinte,
                    modifier = Modifier.weight(1f),
                )
            }
        }

        Kartentyp.ZEITUNG -> {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(IntrinsicSize.Min),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                Box(
                    modifier = Modifier
                        .width(2.dp)
                        .fillMaxHeight()
                        .background(farben.tinte.copy(alpha = 0.45f)),
                )
                Text(
                    text = text,
                    style = MaterialTheme.typography.bodyLarge,
                    fontFamily = FontFamily.Serif,
                    color = farben.tinte,
                    modifier = Modifier.weight(1f),
                )
            }
        }

        else -> {
            Text(
                text = text,
                style = MaterialTheme.typography.bodyLarge,
                color = farben.tinte,
            )
        }
    }
}

/**
 * Genau zwei klar getrennte, gleichwertige Entscheidungs-Schaltflächen (ohne Richtig/Falsch-Hierarchie).
 */
@Composable
fun EntscheidungsOptionenGruppe(
    optionen: List<EntscheidungsOptionUiState>,
    ausgewaehlteOptionIndex: Int?,
    aktiv: Boolean,
    nebeneinanderErlaubt: Boolean,
    onOptionWaehlen: (Int) -> Unit,
    modifier: Modifier = Modifier,
) {
    val abstand = if (ArchivTheme.metrik.kompakteHoehe) 10.dp else 12.dp

    Column(
        modifier = modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(abstand),
    ) {
        optionen.forEach { option ->
            EntscheidungsOptionButton(
                option = option,
                istAusgewaehlt = ausgewaehlteOptionIndex == option.index,
                aktiv = aktiv,
                onClick = { onOptionWaehlen(option.index) },
                modifier = Modifier.fillMaxWidth(),
            )
        }
    }
}

/**
 * Einzelner klar abgesetzter, ruhiger Entscheidungs-Button auf warmem Archivpapier.
 */
@Composable
fun EntscheidungsOptionButton(
    option: EntscheidungsOptionUiState,
    istAusgewaehlt: Boolean,
    aktiv: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val kompakt = ArchivTheme.metrik.kompakteHoehe
    val flaeche = when {
        istAusgewaehlt -> farben.papierDunkel.copy(alpha = 0.78f)
        !aktiv -> farben.papierHell.copy(alpha = 0.55f)
        else -> farben.papierHell
    }
    val rahmen = when {
        istAusgewaehlt -> farben.akzent
        !aktiv -> farben.linieFein.copy(alpha = 0.5f)
        else -> farben.linieFein.copy(alpha = 0.9f)
    }
    val semantik = buildString {
        append("Entscheidung ${option.index + 1}: ${option.titel}. ")
        if (option.hinweis != null) {
            append("Hinweis: ${option.hinweis}. ")
        }
        append(option.beschreibung)
    }

    Surface(
        modifier = modifier
            .defaultMinSize(minHeight = if (kompakt) 56.dp else 64.dp)
            .clip(RoundedCornerShape(6.dp))
            .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = false)
            .clickable(enabled = aktiv, onClick = onClick)
            .clearAndSetSemantics {
                role = Role.Button
                selected = istAusgewaehlt
                stateDescription = when {
                    istAusgewaehlt -> "Gewählt"
                    !aktiv -> "Nicht gewählt"
                    else -> "Auswählbar"
                }
                contentDescription = semantik
            },
        color = flaeche,
        shape = RoundedCornerShape(6.dp),
        border = BorderStroke(if (istAusgewaehlt) 1.4.dp else 0.75.dp, rahmen),
        shadowElevation = if (aktiv) 1.dp else 0.dp,
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .height(IntrinsicSize.Min),
        ) {
            Box(
                modifier = Modifier
                    .width(if (istAusgewaehlt) 3.5.dp else 2.5.dp)
                    .fillMaxHeight()
                    .background(
                        when {
                            istAusgewaehlt -> farben.akzent
                            aktiv -> farben.akzentMatt.copy(alpha = 0.52f)
                            else -> Color.Transparent
                        },
                    ),
            )

            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(
                        horizontal = if (kompakt) 13.dp else 16.dp,
                        vertical = if (kompakt) 10.dp else 12.dp,
                    ),
                verticalArrangement = Arrangement.spacedBy(3.dp),
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text(
                        text = option.titel,
                        style = MaterialTheme.typography.titleSmall,
                        color = if (aktiv || istAusgewaehlt) farben.tinte else farben.tinteMatt,
                        fontWeight = FontWeight.SemiBold,
                        modifier = Modifier.weight(1f),
                    )
                    if (istAusgewaehlt) {
                        HakenIcon(
                            farbe = farben.akzent,
                            groesse = 15.dp,
                            modifier = Modifier.padding(start = 8.dp),
                        )
                    }
                }

                Text(
                    text = option.beschreibung,
                    style = MaterialTheme.typography.bodySmall,
                    color = farben.tinteMatt,
                )

                if (option.hinweis != null) {
                    Text(
                        text = option.hinweis,
                        style = MaterialTheme.typography.labelSmall,
                        fontStyle = FontStyle.Italic,
                        color = farben.akzent,
                    )
                }
            }
        }
    }
}

/**
 * Dezenter, unaufdringlicher Link „Quelle“ (≥ 48 dp Touch-Ziel), der das ruhige
 * Quellen-Overlay öffnet, ohne die Buchseite nach unten aufzublähen.
 */
@Composable
fun QuellenLink(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val spieleEffekt = LocalSoundEffektSpielen.current

    Row(
        modifier = modifier
            .defaultMinSize(minWidth = metrik.minTouchHoehe, minHeight = metrik.minTouchHoehe)
            .clip(RoundedCornerShape(5.dp))
            .archivFokusRahmen(eckRadius = 5.dp, aufDunkel = false)
            .clickable {
                spieleEffekt(SoundEffekt.KLICK_SANFT)
                onClick()
            }
            .clearAndSetSemantics {
                role = Role.Button
                contentDescription = "Historische Quelle ansehen"
            }
            .padding(horizontal = 8.dp, vertical = 6.dp),
        horizontalArrangement = Arrangement.spacedBy(5.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        QuelleBuchIcon(
            farbe = farben.tinteMatt,
            groesse = 14.dp,
        )
        Text(
            text = "Quelle",
            style = MaterialTheme.typography.labelMedium,
            color = farben.tinteMatt,
        )
    }
}

/**
 * Ruhiges Quellen-Overlay (Vollbeleg, Quellenart, quellenkritische Einordnung & Vertiefung).
 */
@Composable
fun QuelleOverlayDialog(
    quelle: QuelleUiState,
    onSchliessen: () -> Unit,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val spieleEffekt = LocalSoundEffektSpielen.current

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
                            .padding(horizontal = 20.dp, vertical = 16.dp),
                        verticalArrangement = Arrangement.spacedBy(10.dp),
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            Text(
                                text = quelle.artLabel,
                                style = MaterialTheme.typography.labelMedium,
                                fontFamily = FontFamily.Serif,
                                color = farben.akzent,
                                fontWeight = FontWeight.SemiBold,
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
                                        contentDescription = "Historische Quelle schließen"
                                    },
                                contentAlignment = Alignment.Center,
                            ) {
                                SchliessenIcon(farbe = farben.tinteMatt, groesse = 18.dp)
                            }
                        }

                        Text(
                            text = quelle.kurz,
                            style = MaterialTheme.typography.titleLarge,
                            fontFamily = FontFamily.Serif,
                            color = farben.tinte,
                            modifier = Modifier.archivUeberschrift(),
                        )

                        if (quelle.voll != null) {
                            Text(
                                text = quelle.voll,
                                style = MaterialTheme.typography.bodySmall,
                                fontStyle = FontStyle.Italic,
                                color = farben.tinteMatt,
                            )
                        }

                        ArchivTrennlinie(farbe = farben.linieFein.copy(alpha = 0.65f))

                        Text(
                            text = quelle.einordnung,
                            style = MaterialTheme.typography.bodyMedium,
                            color = farben.tinte,
                        )

                        if (quelle.vertiefung != null) {
                            Text(
                                text = quelle.vertiefung,
                                style = MaterialTheme.typography.bodySmall,
                                color = farben.tinteMatt,
                            )
                        }
                    }
                }
            }
        }
    }
}

/**
 * Ruhige, offene Ausgangs-Ansicht nach einer getroffenen Entscheidung (`GamePhase.EreignisAusgang`):
 * Ersetzt die Entscheidungs-Buttons vollständig auf der rechten Buchseite — auf einen Blick
 * ohne Scroll-Chaos lesbar: gewählte Entscheidung als Kopfzeile, Ausgangstext, kompakte
 * Werte-Veränderung und prominenter „Weiter“-Button.
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun EreignisAusgangKarte(
    ausgang: EreignisAusgangUiState,
    weiterLabel: String,
    onWeiter: () -> Unit,
    modifier: Modifier = Modifier,
    quelle: QuelleUiState? = null,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val kompakt = metrik.kompakteHoehe
    var quelleOffen by remember(ausgang.ereignisId) { mutableStateOf(false) }

    Column(
        modifier = modifier
            .fillMaxWidth()
            .archivLiveHinweis(),
        verticalArrangement = Arrangement.spacedBy(if (kompakt) 12.dp else 16.dp),
    ) {
        // Gewählte Entscheidung kurz als ruhige Kopfzeile (+ optionaler Quelle-Link)
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(2.dp),
            ) {
                Text(
                    text = "Gewählt",
                    style = MaterialTheme.typography.labelSmall,
                    color = farben.tinteMatt,
                )
                Text(
                    text = ausgang.gewaehlterTitel,
                    style = if (kompakt) MaterialTheme.typography.titleLarge else MaterialTheme.typography.headlineSmall,
                    fontFamily = FontFamily.Serif,
                    color = farben.akzent,
                    modifier = Modifier.archivUeberschrift(),
                )
            }

            if (quelle != null) {
                QuellenLink(onClick = { quelleOffen = true })
            }
        }

        // Ausgangstext offen auf dem warmen Archivpapier
        Text(
            text = ausgang.ausgangsText,
            style = MaterialTheme.typography.bodyLarge,
            color = farben.tinte,
        )

        // Kompakte Werte-Veränderung (+1 / -1) & optionale Prägung
        if (ausgang.wirkungen.isNotEmpty() || ausgang.neueMerkmaleNamen.isNotEmpty()) {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                if (ausgang.wirkungen.isNotEmpty()) {
                    FlowRow(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp),
                    ) {
                        ausgang.wirkungen.forEach { wirkung ->
                            val farbe = farben.deltaFarbe(
                                schlechter = wirkung.schlechter,
                                aufDunkel = false,
                            )
                            ArchivStempel(
                                text = "${wirkung.name} ${wirkung.zeichen}",
                                farbe = farbe,
                                hintergrund = farbe.copy(alpha = 0.08f),
                            )
                        }
                    }
                }

                if (ausgang.neueMerkmaleNamen.isNotEmpty()) {
                    Text(
                        text = "Prägung: ${ausgang.neueMerkmaleNamen.joinToString(", ")}",
                        style = MaterialTheme.typography.bodySmall,
                        fontFamily = FontFamily.Serif,
                        fontStyle = FontStyle.Italic,
                        color = farben.tinteMatt,
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(2.dp))

        // Prominenter „Weiter“-Button
        Surface(
            modifier = Modifier
                .defaultMinSize(minWidth = metrik.minTouchHoehe, minHeight = metrik.minTouchHoehe)
                .clip(RoundedCornerShape(6.dp))
                .archivFokusRahmen(eckRadius = 6.dp, aufDunkel = false)
                .clickable(onClick = onWeiter)
                .semantics {
                    role = Role.Button
                    contentDescription = weiterLabel
                },
            color = farben.tinte,
            shape = RoundedCornerShape(6.dp),
        ) {
            Box(
                modifier = Modifier.padding(horizontal = 24.dp, vertical = 12.dp),
                contentAlignment = Alignment.Center,
            ) {
                Text(
                    text = weiterLabel,
                    style = MaterialTheme.typography.labelLarge,
                    color = farben.papierHell,
                )
            }
        }
    }

    if (quelleOffen && quelle != null) {
        QuelleOverlayDialog(
            quelle = quelle,
            onSchliessen = { quelleOffen = false },
        )
    }
}
