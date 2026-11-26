package de.pytales.zdf.ui.components

import androidx.compose.animation.AnimatedVisibility
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
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import de.pytales.zdf.model.Kartentyp
import de.pytales.zdf.ui.state.EntscheidungsKarteUiState
import de.pytales.zdf.ui.state.EntscheidungsOptionUiState
import de.pytales.zdf.ui.state.EreignisAusgangUiState
import de.pytales.zdf.ui.state.QuelleUiState
import de.pytales.zdf.ui.theme.ArchivTheme

/**
 * Entscheidungskarten-Baukasten für alle 5 historischen Kartentypen:
 * - [Kartentyp.KARTE]: klassische Archivpapier-Alltagskarte
 * - [Kartentyp.FELDPOST]: Feldpostbrief mit Poststempel und feiner Falzlinie
 * - [Kartentyp.LEBENSMITTEL]: Bezugs-/Lebensmittelkarte mit perforiertem Markenrand
 * - [Kartentyp.ZEITUNG]: Tagesblatt-Meldung mit doppeltem Zeitungskopf und Spaltenlinie
 * - [Kartentyp.AMTLICH]: Amtliche Verfügung mit doppeltem Aktenrahmen und Dienstsiegel
 *
 * Enthält stets exakt zwei gleichwertige Entscheidungs-Schaltflächen (inkl. optionalem
 * Hinweis-Stempel) sowie die aufklappbare historische Quellen-Einordnung für den Unterricht.
 */
@Composable
fun EntscheidungsKarte(
    karte: EntscheidungsKarteUiState,
    onOptionWaehlen: (Int) -> Unit,
    modifier: Modifier = Modifier,
    ausgewaehlteOptionIndex: Int? = null,
    optionenAktiv: Boolean = true,
    analyseModus: Boolean = false,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik

    val papierFlaeche = when (karte.kartentyp) {
        Kartentyp.KARTE,
        Kartentyp.FELDPOST,
        Kartentyp.AMTLICH,
        -> farben.papierHell

        Kartentyp.LEBENSMITTEL,
        Kartentyp.ZEITUNG,
        -> farben.papier
    }

    val rahmenFarbe = when (karte.kartentyp) {
        Kartentyp.AMTLICH -> farben.tinte.copy(alpha = 0.72f)
        Kartentyp.LEBENSMITTEL -> Color.Transparent // eigener gestrichelter Markenrand
        else -> farben.linie
    }

    val gestrichelterRandModifier = if (karte.kartentyp == Kartentyp.LEBENSMITTEL) {
        Modifier.drawBehind {
            val strich = 1.5.dp.toPx()
            drawRoundRect(
                color = farben.linie,
                topLeft = Offset(strich / 2f, strich / 2f),
                size = Size(size.width - strich, size.height - strich),
                cornerRadius = CornerRadius(4.dp.toPx(), 4.dp.toPx()),
                style = Stroke(
                    width = strich,
                    pathEffect = PathEffect.dashPathEffect(floatArrayOf(10f, 6f), 0f),
                ),
            )
        }
    } else {
        Modifier
    }

    Surface(
        modifier = modifier
            .fillMaxWidth()
            .then(gestrichelterRandModifier),
        color = papierFlaeche,
        shape = RoundedCornerShape(4.dp),
        border = if (karte.kartentyp == Kartentyp.LEBENSMITTEL) {
            null
        } else {
            BorderStroke(if (karte.kartentyp == Kartentyp.AMTLICH) 1.5.dp else 1.dp, rahmenFarbe)
        },
        shadowElevation = 1.dp,
    ) {
        // Amtliche Karten erhalten zusätzlich einen feinen inneren Doppelrahmen
        val innenRahmenModifier = if (karte.kartentyp == Kartentyp.AMTLICH) {
            Modifier
                .padding(4.dp)
                .border(0.75.dp, farben.linieFein, RoundedCornerShape(2.dp))
        } else {
            Modifier
        }

        Column(
            modifier = Modifier
                .fillMaxWidth()
                .then(innenRahmenModifier),
        ) {
            // Typspezifischer Dokumentkopf
            KartenKopfNachTyp(karte = karte)

            // Hauptkörper: Erzähltext + zwei gleichwertige Wahl-Schaltflächen + Quelle
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(metrik.kartenInnenAbstand),
                verticalArrangement = Arrangement.spacedBy(metrik.elementAbstand),
            ) {
                KartenTextNachTyp(
                    kartentyp = karte.kartentyp,
                    text = karte.text,
                )

                ArchivTrennlinie(farbe = farben.linieFein)

                EntscheidungsOptionenGruppe(
                    optionen = karte.optionen,
                    ausgewaehlteOptionIndex = ausgewaehlteOptionIndex,
                    aktiv = optionenAktiv,
                    nebeneinander = metrik.optionenNebeneinander,
                    onOptionWaehlen = onOptionWaehlen,
                )

                QuellenEinordnungBox(
                    quelle = karte.quelle,
                    ereignisId = karte.ereignisId,
                    kartentypBezeichnung = karte.kartentypBezeichnung,
                    bildId = karte.szenenbild.bildId,
                    analyseModus = analyseModus,
                )
            }
        }
    }
}

@Composable
private fun KartenKopfNachTyp(karte: EntscheidungsKarteUiState) {
    val farben = ArchivTheme.farben
    val innen = ArchivTheme.metrik.kartenInnenAbstand

    when (karte.kartentyp) {
        Kartentyp.KARTE -> {
            Column(modifier = Modifier.fillMaxWidth()) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(3.dp)
                        .background(farben.akzent),
                )
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = innen, vertical = 10.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text(
                        text = karte.kartentypKopfzeile,
                        style = MaterialTheme.typography.labelMedium,
                        color = farben.akzent,
                        fontWeight = FontWeight.Bold,
                    )
                    Text(
                        text = karte.aktenzeichen,
                        style = MaterialTheme.typography.labelSmall,
                        color = farben.tinteMatt,
                    )
                }
                ArchivTrennlinie(farbe = farben.linieFein)
            }
        }

        Kartentyp.FELDPOST -> {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(farben.papier.copy(alpha = 0.55f)),
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = innen, vertical = 10.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
                        Text(
                            text = karte.kartentypKopfzeile,
                            style = MaterialTheme.typography.titleMedium,
                            fontFamily = FontFamily.Serif,
                            color = farben.tinte,
                            fontWeight = FontWeight.Bold,
                        )
                        Text(
                            text = karte.aktenzeichen,
                            style = MaterialTheme.typography.labelSmall,
                            color = farben.tinteMatt,
                        )
                    }
                    FeldpostStempel(jahr = karte.jahr)
                }
                ArchivTrennlinie(farbe = farben.akzentMatt.copy(alpha = 0.6f))
            }
        }

        Kartentyp.LEBENSMITTEL -> {
            Column(modifier = Modifier.fillMaxWidth()) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(farben.papierDunkel)
                        .padding(horizontal = innen, vertical = 10.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Column(
                        verticalArrangement = Arrangement.spacedBy(2.dp),
                        modifier = Modifier.weight(1f),
                    ) {
                        Text(
                            text = karte.kartentypKopfzeile,
                            style = MaterialTheme.typography.labelLarge,
                            color = farben.tinte,
                            fontWeight = FontWeight.Bold,
                        )
                        Text(
                            text = karte.aktenzeichen,
                            style = MaterialTheme.typography.labelSmall,
                            color = farben.tinteMatt,
                        )
                    }
                    // Stilisierte Marken-Abschnitte einer historischen Lebensmittelkarte
                    Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                        listOf("I", "II", "III").forEach { abschnitt ->
                            Box(
                                modifier = Modifier
                                    .border(1.dp, farben.linie, RoundedCornerShape(1.dp))
                                    .background(farben.papierHell)
                                    .padding(horizontal = 6.dp, vertical = 2.dp),
                            ) {
                                Text(
                                    text = abschnitt,
                                    style = MaterialTheme.typography.labelSmall,
                                    color = farben.tinteMatt,
                                )
                            }
                        }
                    }
                }
                ArchivTrennlinie(farbe = farben.linie)
            }
        }

        Kartentyp.ZEITUNG -> {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = innen, vertical = 12.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(6.dp),
            ) {
                ArchivTrennlinie(farbe = farben.tinte, doppelt = true)
                Text(
                    text = karte.kartentypKopfzeile,
                    style = MaterialTheme.typography.headlineSmall,
                    fontFamily = FontFamily.Serif,
                    color = farben.tinte,
                    fontWeight = FontWeight.Bold,
                    textAlign = TextAlign.Center,
                )
                Text(
                    text = "${karte.aktenzeichen} · ${karte.pfadMarke}",
                    style = MaterialTheme.typography.labelSmall,
                    color = farben.tinteMatt,
                    textAlign = TextAlign.Center,
                )
                ArchivTrennlinie(farbe = farben.tinte, doppelt = true)
            }
        }

        Kartentyp.AMTLICH -> {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(farben.papierDunkel.copy(alpha = 0.65f)),
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = innen, vertical = 10.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Column(
                        verticalArrangement = Arrangement.spacedBy(2.dp),
                        modifier = Modifier.weight(1f),
                    ) {
                        Text(
                            text = karte.kartentypKopfzeile,
                            style = MaterialTheme.typography.titleMedium,
                            fontFamily = FontFamily.Serif,
                            color = farben.tinte,
                            fontWeight = FontWeight.Bold,
                        )
                        Text(
                            text = karte.aktenzeichen,
                            style = MaterialTheme.typography.labelSmall,
                            color = farben.tinteMatt,
                        )
                    }
                    ArchivStempel(
                        text = "AMTLICH",
                        farbe = farben.akzent,
                        grossbuchstaben = true,
                    )
                }
                ArchivTrennlinie(farbe = farben.tinte.copy(alpha = 0.7f), doppelt = true)
            }
        }
    }
}

@Composable
private fun FeldpostStempel(jahr: Int) {
    val farben = ArchivTheme.farben
    Box(
        modifier = Modifier.size(46.dp),
        contentAlignment = Alignment.Center,
    ) {
        Canvas(modifier = Modifier.matchParentSize()) {
            val radius = size.minDimension / 2f - 2.dp.toPx()
            drawCircle(
                color = farben.akzentMatt.copy(alpha = 0.75f),
                radius = radius,
                style = Stroke(width = 1.25.dp.toPx()),
            )
            drawCircle(
                color = farben.akzentMatt.copy(alpha = 0.45f),
                radius = radius - 3.dp.toPx(),
                style = Stroke(width = 0.75.dp.toPx()),
            )
        }
        Text(
            text = jahr.toString(),
            style = MaterialTheme.typography.labelSmall,
            color = farben.akzent,
            fontWeight = FontWeight.Bold,
        )
    }
}

@Composable
private fun KartenTextNachTyp(
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
                        .background(farben.tinte.copy(alpha = 0.65f)),
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
 * Genau zwei gleichwertige Entscheidungs-Schaltflächen (ohne Richtig/Falsch-Hierarchie).
 * Bei [nebeneinander] = true symmetrisch nebeneinander mit identischer Höhe;
 * bei `false` (Android-Hochformat / Beamer auf mittlerer Breite) gestapelt.
 */
@Composable
fun EntscheidungsOptionenGruppe(
    optionen: List<EntscheidungsOptionUiState>,
    ausgewaehlteOptionIndex: Int?,
    aktiv: Boolean,
    nebeneinander: Boolean,
    onOptionWaehlen: (Int) -> Unit,
    modifier: Modifier = Modifier,
) {
    val abstand = ArchivTheme.metrik.elementAbstand

    if (nebeneinander && optionen.size == 2) {
        Row(
            modifier = modifier
                .fillMaxWidth()
                .height(IntrinsicSize.Min),
            horizontalArrangement = Arrangement.spacedBy(abstand),
        ) {
            optionen.forEach { option ->
                EntscheidungsOptionButton(
                    option = option,
                    istAusgewaehlt = ausgewaehlteOptionIndex == option.index,
                    aktiv = aktiv,
                    onClick = { onOptionWaehlen(option.index) },
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxHeight(),
                )
            }
        }
    } else {
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
}

/**
 * Einzelne gleichwertige Entscheidungs-Schaltfläche mit optionalem Hinweis-Stempel
 * (z. B. „gegen die Vorschrift“, „Briefzensur“, „fällt auf“).
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
    val flaeche = when {
        istAusgewaehlt -> farben.papierDunkel
        else -> farben.papier
    }
    val rahmen = when {
        istAusgewaehlt -> farben.akzent
        else -> farben.linie
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
            .defaultMinSize(minHeight = 76.dp)
            .clip(RoundedCornerShape(4.dp))
            .clickable(enabled = aktiv, onClick = onClick)
            .semantics {
                role = Role.Button
                selected = istAusgewaehlt
                contentDescription = semantik
            },
        color = flaeche,
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(if (istAusgewaehlt) 2.dp else 1.25.dp, rahmen),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 14.dp, vertical = 12.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            if (option.hinweis != null) {
                ArchivStempel(
                    text = option.hinweis,
                    farbe = farben.akzent,
                )
            }

            Text(
                text = option.titel,
                style = MaterialTheme.typography.titleMedium,
                color = farben.tinte,
                fontWeight = FontWeight.SemiBold,
            )

            Text(
                text = option.beschreibung,
                style = MaterialTheme.typography.bodyMedium,
                color = farben.tinteMatt,
            )
        }
    }
}

/**
 * Aufklappbare historische Quellen-Einordnung für den Geschichtsunterricht und Analysemodus.
 * Öffnet automatisch im [analyseModus] und lässt sich jederzeit per Tipp/Klick ein- oder ausklappen.
 */
@Composable
fun QuellenEinordnungBox(
    quelle: QuelleUiState,
    ereignisId: String,
    kartentypBezeichnung: String,
    bildId: String,
    analyseModus: Boolean,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    var aufgeklappt by remember(ereignisId) { mutableStateOf(analyseModus) }

    LaunchedEffect(analyseModus) {
        aufgeklappt = analyseModus
    }

    Column(
        modifier = modifier
            .fillMaxWidth()
            .border(1.dp, farben.linieFein, RoundedCornerShape(3.dp))
            .background(farben.papierDunkel.copy(alpha = 0.48f), RoundedCornerShape(3.dp)),
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .defaultMinSize(minHeight = 44.dp)
                .clickable { aufgeklappt = !aufgeklappt }
                .semantics {
                    role = Role.Button
                    contentDescription = if (aufgeklappt) {
                        "Historische Einordnung und Quelle zuklappen"
                    } else {
                        "Historische Einordnung und Quelle aufklappen"
                    }
                }
                .padding(horizontal = 12.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Row(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.weight(1f),
            ) {
                Text(
                    text = if (analyseModus) {
                        "Analysemodus · Historische Einordnung & Quelle"
                    } else {
                        "Historische Einordnung & Quelle"
                    },
                    style = MaterialTheme.typography.labelLarge,
                    color = if (analyseModus) farben.akzent else farben.tinte,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
            }
            Text(
                text = if (aufgeklappt) "Zuklappen ▴" else "Aufklappen ▾",
                style = MaterialTheme.typography.labelSmall,
                color = farben.tinteMatt,
            )
        }

        AnimatedVisibility(
            visible = aufgeklappt,
            enter = fadeIn() + expandVertically(),
            exit = fadeOut() + shrinkVertically(),
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(farben.papierHell.copy(alpha = 0.85f))
                    .padding(12.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                Row(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    ArchivStempel(
                        text = quelle.artLabel,
                        farbe = farben.tinteMatt,
                        hintergrund = farben.papier,
                    )
                    Text(
                        text = quelle.kurz,
                        style = MaterialTheme.typography.titleSmall,
                        color = farben.tinte,
                        modifier = Modifier.weight(1f),
                    )
                }

                if (quelle.voll != null) {
                    Text(
                        text = "Nachweis: ${quelle.voll}",
                        style = MaterialTheme.typography.bodySmall,
                        fontStyle = FontStyle.Italic,
                        color = farben.tinteMatt,
                    )
                }

                Text(
                    text = quelle.einordnung,
                    style = MaterialTheme.typography.bodyMedium,
                    color = farben.tinte,
                )

                if (quelle.vertiefung != null) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(farben.papier, RoundedCornerShape(3.dp))
                            .border(1.dp, farben.linieFein, RoundedCornerShape(3.dp))
                            .padding(10.dp),
                    ) {
                        Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                            Text(
                                text = "Vertiefung für den Unterricht",
                                style = MaterialTheme.typography.labelMedium,
                                color = farben.akzent,
                                fontWeight = FontWeight.SemiBold,
                            )
                            Text(
                                text = quelle.vertiefung,
                                style = MaterialTheme.typography.bodySmall,
                                color = farben.tinte,
                            )
                        }
                    }
                }

                if (analyseModus) {
                    ArchivTrennlinie(farbe = farben.linieFein)
                    Text(
                        text = "Archiv-ID: $ereignisId · Kartentyp: $kartentypBezeichnung · Bild-ID: $bildId",
                        style = MaterialTheme.typography.labelSmall,
                        color = farben.tinteMatt,
                    )
                }
            }
        }
    }
}

/**
 * Wiederverwendbare Ausgangs-Karte nach einer getroffenen Entscheidung:
 * zeigt gewählte Entscheidung, Erzähl-Ausgang, sichtbare Wertewirkungen (`+1`/`-1`)
 * und eine klare Fortfahren-Schaltfläche (direkt nutzbar in AP-3-Demo und AP-4-Spielschleife).
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun EreignisAusgangKarte(
    ausgang: EreignisAusgangUiState,
    weiterLabel: String,
    onWeiter: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik

    Surface(
        modifier = modifier.fillMaxWidth(),
        color = farben.papierHell,
        shape = RoundedCornerShape(4.dp),
        border = BorderStroke(1.25.dp, farben.linie),
    ) {
        Column(modifier = Modifier.fillMaxWidth()) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(3.dp)
                    .background(farben.tinte),
            )
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(metrik.kartenInnenAbstand),
                verticalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                Text(
                    text = "ENTSCHEIDUNG: ${ausgang.gewaehlterTitel.uppercase()}",
                    style = MaterialTheme.typography.labelMedium,
                    color = farben.tinteMatt,
                    fontWeight = FontWeight.Bold,
                )

                Text(
                    text = ausgang.ausgangsText,
                    style = MaterialTheme.typography.bodyLarge,
                    color = farben.tinte,
                )

                if (ausgang.wirkungen.isNotEmpty()) {
                    FlowRow(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        ausgang.wirkungen.forEach { wirkung ->
                            val farbe = farben.deltaFarbe(
                                schlechter = wirkung.schlechter,
                                aufDunkel = false,
                            )
                            ArchivStempel(
                                text = "${wirkung.name} ${wirkung.zeichen} (${wirkung.richtung})",
                                farbe = farbe,
                            )
                        }
                    }
                }

                if (ausgang.neueMerkmaleNamen.isNotEmpty()) {
                    Text(
                        text = "Prägung vermerkt: ${ausgang.neueMerkmaleNamen.joinToString(", ")}",
                        style = MaterialTheme.typography.bodySmall,
                        fontStyle = FontStyle.Italic,
                        color = farben.tinteMatt,
                    )
                }

                Spacer(modifier = Modifier.height(2.dp))

                Surface(
                    modifier = Modifier
                        .defaultMinSize(minHeight = metrik.minTouchHoehe)
                        .clip(RoundedCornerShape(4.dp))
                        .clickable(onClick = onWeiter)
                        .semantics {
                            role = Role.Button
                            contentDescription = weiterLabel
                        },
                    color = farben.tinte,
                    shape = RoundedCornerShape(4.dp),
                ) {
                    Box(
                        modifier = Modifier.padding(horizontal = 20.dp, vertical = 12.dp),
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
        }
    }
}
