package de.pytales.zdf.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
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
import de.pytales.zdf.model.Kartentyp
import de.pytales.zdf.ui.state.EntscheidungsKarteUiState
import de.pytales.zdf.ui.state.EntscheidungsOptionUiState
import de.pytales.zdf.ui.state.EreignisAusgangUiState
import de.pytales.zdf.ui.state.QuelleUiState
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.ArchivUebergaenge

/**
 * Entscheidungskarte im ruhigen Buchdruck- & Archiv-Stil für alle 5 historischen Kartentypen:
 * - [Kartentyp.KARTE]: klassisches Archivpapier-Blatt
 * - [Kartentyp.FELDPOST]: Feldpostbrief mit feinem Poststempel und linker Falzlinie
 * - [Kartentyp.LEBENSMITTEL]: Bezugskarte mit dezent perforiertem Markenrand
 * - [Kartentyp.ZEITUNG]: Tagesblatt-Meldung mit doppeltem Zeitungskopf und Serifen-Satz
 * - [Kartentyp.AMTLICH]: Amtliche Verfügung mit feinem Doppelrahmen
 *
 * Enthält stets exakt zwei gleichwertige Entscheidungs-Schaltflächen sowie eine
 * schlichte, unaufdringlich aufklappbare „Historische Quelle“.
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

    val papierFlaeche = when (karte.kartentyp) {
        Kartentyp.KARTE,
        Kartentyp.FELDPOST,
        Kartentyp.AMTLICH,
        -> farben.papierHell

        Kartentyp.LEBENSMITTEL,
        Kartentyp.ZEITUNG,
        -> farben.papierHell.copy(alpha = 0.92f)
    }

    val rahmenFarbe = when (karte.kartentyp) {
        Kartentyp.AMTLICH -> farben.linie.copy(alpha = 0.85f)
        Kartentyp.LEBENSMITTEL -> Color.Transparent
        else -> farben.linieFein.copy(alpha = 0.82f)
    }

    val gestrichelterRandModifier = if (karte.kartentyp == Kartentyp.LEBENSMITTEL) {
        Modifier.drawBehind {
            val strich = 1.25.dp.toPx()
            drawRoundRect(
                color = farben.linie.copy(alpha = 0.78f),
                topLeft = Offset(strich / 2f, strich / 2f),
                size = Size(size.width - strich, size.height - strich),
                cornerRadius = CornerRadius(6.dp.toPx(), 6.dp.toPx()),
                style = Stroke(
                    width = strich,
                    pathEffect = PathEffect.dashPathEffect(floatArrayOf(9f, 6f), 0f),
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
        shape = RoundedCornerShape(6.dp),
        border = if (karte.kartentyp == Kartentyp.LEBENSMITTEL) {
            null
        } else {
            BorderStroke(if (karte.kartentyp == Kartentyp.AMTLICH) 1.dp else 0.75.dp, rahmenFarbe)
        },
        shadowElevation = 2.dp,
    ) {
        Column(modifier = Modifier.fillMaxWidth()) {
            // Typspezifischer, ruhiger Buchdruck-Kopf
            KartenKopfNachTyp(karte = karte)

            // Hauptkörper: Erzähltext + zwei klare Entscheidungen + schlichte Quelle
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(
                        horizontal = metrik.kartenInnenAbstand,
                        vertical = if (metrik.kompakteHoehe) 12.dp else 16.dp,
                    ),
                verticalArrangement = Arrangement.spacedBy(if (metrik.kompakteHoehe) 12.dp else 14.dp),
            ) {
                KartenTextNachTyp(
                    kartentyp = karte.kartentyp,
                    text = karte.text,
                )

                ArchivTrennlinie(farbe = farben.linieFein.copy(alpha = 0.65f))

                EntscheidungsOptionenGruppe(
                    optionen = karte.optionen,
                    ausgewaehlteOptionIndex = ausgewaehlteOptionIndex,
                    aktiv = optionenAktiv,
                    nebeneinanderErlaubt = metrik.optionenNebeneinander,
                    onOptionWaehlen = onOptionWaehlen,
                )

                QuellenEinordnungBox(
                    quelle = karte.quelle,
                    ereignisId = karte.ereignisId,
                )
            }
        }
    }
}

@Composable
private fun KartenKopfNachTyp(karte: EntscheidungsKarteUiState) {
    val farben = ArchivTheme.farben
    val innen = ArchivTheme.metrik.kartenInnenAbstand
    val kompakt = ArchivTheme.metrik.kompakteHoehe

    when (karte.kartentyp) {
        Kartentyp.KARTE -> {
            Column(modifier = Modifier.fillMaxWidth()) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(2.5.dp)
                        .background(farben.akzent.copy(alpha = 0.85f)),
                )
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = innen, vertical = if (kompakt) 7.dp else 9.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text(
                        text = karte.kartentypBezeichnung,
                        style = MaterialTheme.typography.labelMedium,
                        fontFamily = FontFamily.Serif,
                        color = farben.akzent,
                        fontWeight = FontWeight.SemiBold,
                    )
                    Text(
                        text = karte.aktenzeichen,
                        style = MaterialTheme.typography.labelSmall,
                        color = farben.tinteMatt,
                    )
                }
                ArchivTrennlinie(farbe = farben.linieFein.copy(alpha = 0.6f))
            }
        }

        Kartentyp.FELDPOST -> {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(farben.papier.copy(alpha = 0.45f)),
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = innen, vertical = if (kompakt) 7.dp else 9.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Column(verticalArrangement = Arrangement.spacedBy(1.dp)) {
                        Text(
                            text = "Feldpostbrief",
                            style = MaterialTheme.typography.titleMedium,
                            color = farben.tinte,
                            fontWeight = FontWeight.SemiBold,
                        )
                        Text(
                            text = karte.aktenzeichen,
                            style = MaterialTheme.typography.labelSmall,
                            color = farben.tinteMatt,
                        )
                    }
                    FeldpostStempel(jahr = karte.jahr)
                }
                ArchivTrennlinie(farbe = farben.akzentMatt.copy(alpha = 0.45f))
            }
        }

        Kartentyp.LEBENSMITTEL -> {
            Column(modifier = Modifier.fillMaxWidth()) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(farben.papierDunkel.copy(alpha = 0.55f))
                        .padding(horizontal = innen, vertical = if (kompakt) 7.dp else 9.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Column(
                        verticalArrangement = Arrangement.spacedBy(1.dp),
                        modifier = Modifier.weight(1f),
                    ) {
                        Text(
                            text = "Reichs-Lebensmittelkarte",
                            style = MaterialTheme.typography.titleSmall,
                            color = farben.tinte,
                            fontWeight = FontWeight.SemiBold,
                        )
                        Text(
                            text = karte.aktenzeichen,
                            style = MaterialTheme.typography.labelSmall,
                            color = farben.tinteMatt,
                        )
                    }
                    Row(
                        modifier = Modifier.clearAndSetSemantics {},
                        horizontalArrangement = Arrangement.spacedBy(4.dp),
                    ) {
                        listOf("I", "II", "III").forEach { abschnitt ->
                            Text(
                                text = abschnitt,
                                style = MaterialTheme.typography.labelSmall,
                                fontFamily = FontFamily.Serif,
                                color = farben.tinteMatt,
                                modifier = Modifier
                                    .background(farben.papierHell.copy(alpha = 0.85f), RoundedCornerShape(3.dp))
                                    .padding(horizontal = 6.dp, vertical = 2.dp),
                            )
                        }
                    }
                }
                ArchivTrennlinie(farbe = farben.linieFein)
            }
        }

        Kartentyp.ZEITUNG -> {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = innen, vertical = if (kompakt) 8.dp else 10.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(4.dp),
            ) {
                ArchivTrennlinie(farbe = farben.tinte.copy(alpha = 0.72f), doppelt = true)
                Text(
                    text = "Tagesblatt · Meldung",
                    style = MaterialTheme.typography.titleLarge,
                    color = farben.tinte,
                    fontWeight = FontWeight.Bold,
                    textAlign = TextAlign.Center,
                    modifier = Modifier.archivUeberschrift(),
                )
                Text(
                    text = "${karte.aktenzeichen} · ${karte.pfadMarke}",
                    style = MaterialTheme.typography.labelSmall,
                    color = farben.tinteMatt,
                    textAlign = TextAlign.Center,
                )
                ArchivTrennlinie(farbe = farben.tinte.copy(alpha = 0.72f), doppelt = true)
            }
        }

        Kartentyp.AMTLICH -> {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(farben.papierDunkel.copy(alpha = 0.42f)),
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = innen, vertical = if (kompakt) 7.dp else 9.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text(
                        text = "Amtliche Verfügung",
                        style = MaterialTheme.typography.titleMedium,
                        color = farben.tinte,
                        fontWeight = FontWeight.SemiBold,
                        modifier = Modifier
                            .weight(1f)
                            .archivUeberschrift(),
                    )
                    Text(
                        text = karte.aktenzeichen,
                        style = MaterialTheme.typography.labelSmall,
                        color = farben.tinteMatt,
                    )
                }
                ArchivTrennlinie(farbe = farben.tinte.copy(alpha = 0.55f), doppelt = true)
            }
        }
    }
}

@Composable
private fun FeldpostStempel(jahr: Int) {
    val farben = ArchivTheme.farben
    Box(
        modifier = Modifier
            .size(38.dp)
            .clearAndSetSemantics {},
        contentAlignment = Alignment.Center,
    ) {
        Canvas(modifier = Modifier.matchParentSize()) {
            val radius = size.minDimension / 2f - 1.5.dp.toPx()
            drawCircle(
                color = farben.akzentMatt.copy(alpha = 0.65f),
                radius = radius,
                style = Stroke(width = 1.dp.toPx()),
            )
            drawCircle(
                color = farben.akzentMatt.copy(alpha = 0.38f),
                radius = radius - 2.5.dp.toPx(),
                style = Stroke(width = 0.75.dp.toPx()),
            )
        }
        Text(
            text = jahr.toString(),
            style = MaterialTheme.typography.labelSmall,
            fontFamily = FontFamily.Serif,
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
                        .background(farben.tinte.copy(alpha = 0.55f)),
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
 * Passt sich automatisch an die tatsächliche Kartenbreite an: nebeneinander ab ~460 dp
 * Kartenbreite (Tablets/Desktop), darunter ruhig und gut lesbar gestapelt.
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
    val abstand = if (ArchivTheme.metrik.kompakteHoehe) 8.dp else 10.dp

    BoxWithConstraints(modifier = modifier.fillMaxWidth()) {
        val zeigeNebeneinander = nebeneinanderErlaubt && optionen.size == 2 && maxWidth >= 460.dp

        if (zeigeNebeneinander) {
            Row(
                modifier = Modifier
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
                modifier = Modifier.fillMaxWidth(),
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
}

/**
 * Einzelne gleichwertige Entscheidungs-Schaltfläche im ruhigen Buchdruck-Papierstil.
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
        istAusgewaehlt -> farben.papierDunkel.copy(alpha = 0.85f)
        !aktiv -> farben.papier.copy(alpha = 0.52f)
        else -> farben.papier
    }
    val rahmen = when {
        istAusgewaehlt -> farben.akzent
        !aktiv -> farben.linieFein.copy(alpha = 0.55f)
        else -> farben.linieFein
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
            .defaultMinSize(minHeight = if (kompakt) 58.dp else 68.dp)
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
        border = BorderStroke(if (istAusgewaehlt) 1.5.dp else 0.9.dp, rahmen),
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .height(IntrinsicSize.Min),
        ) {
            // Dezente linke Akzentlinie bei Auswahl oder warm ruhende Kante
            Box(
                modifier = Modifier
                    .width(if (istAusgewaehlt) 3.5.dp else 2.5.dp)
                    .fillMaxHeight()
                    .background(
                        when {
                            istAusgewaehlt -> farben.akzent
                            aktiv -> farben.akzentMatt.copy(alpha = 0.45f)
                            else -> Color.Transparent
                        },
                    ),
            )

            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(
                        horizontal = if (kompakt) 12.dp else 14.dp,
                        vertical = if (kompakt) 9.dp else 11.dp,
                    ),
                verticalArrangement = Arrangement.spacedBy(4.dp),
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
 * Schlichte, unaufdringlich aufklappbare „Historische Quelle“ am Fuß jeder Ereigniskarte.
 */
@Composable
fun QuellenEinordnungBox(
    quelle: QuelleUiState,
    ereignisId: String,
    modifier: Modifier = Modifier,
) {
    val farben = ArchivTheme.farben
    val metrik = ArchivTheme.metrik
    val reduziert = ArchivTheme.reduzierteAnimationen
    var aufgeklappt by remember(ereignisId) { mutableStateOf(false) }

    Column(modifier = modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .defaultMinSize(minHeight = metrik.minTouchHoehe)
                .clip(RoundedCornerShape(5.dp))
                .archivFokusRahmen(eckRadius = 5.dp, aufDunkel = false)
                .clickable { aufgeklappt = !aufgeklappt }
                .clearAndSetSemantics {
                    role = Role.Button
                    selected = aufgeklappt
                    stateDescription = if (aufgeklappt) "Aufgeklappt" else "Zugeklappt"
                    contentDescription = if (aufgeklappt) {
                        "Historische Quelle zuklappen"
                    } else {
                        "Historische Quelle aufklappen"
                    }
                }
                .padding(horizontal = 4.dp, vertical = 6.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Row(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.weight(1f),
            ) {
                QuelleBuchIcon(
                    farbe = if (aufgeklappt) farben.akzent else farben.tinteMatt,
                    groesse = 15.dp,
                )
                Text(
                    text = "Historische Quelle",
                    style = MaterialTheme.typography.labelMedium,
                    color = if (aufgeklappt) farben.akzent else farben.tinteMatt,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
            }
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
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(IntrinsicSize.Min)
                    .background(farben.papier.copy(alpha = 0.68f), RoundedCornerShape(5.dp)),
            ) {
                Box(
                    modifier = Modifier
                        .width(2.dp)
                        .fillMaxHeight()
                        .background(farben.linie),
                )
                Column(
                    modifier = Modifier
                        .weight(1f)
                        .padding(horizontal = 12.dp, vertical = 10.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp),
                ) {
                    Text(
                        text = "${quelle.artLabel} · ${quelle.kurz}",
                        style = MaterialTheme.typography.titleSmall,
                        color = farben.tinte,
                    )

                    if (quelle.voll != null) {
                        Text(
                            text = quelle.voll,
                            style = MaterialTheme.typography.bodySmall,
                            fontStyle = FontStyle.Italic,
                            color = farben.tinteMatt,
                        )
                    }

                    Text(
                        text = quelle.einordnung,
                        style = MaterialTheme.typography.bodySmall,
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

/**
 * Ruhige Ausgangs-Karte nach einer getroffenen Entscheidung:
 * zeigt die gewählte Entscheidung, den Erzähl-Ausgang, spürbare Wertewirkungen (`+1`/`-1`)
 * und die klare Fortfahren-Schaltfläche.
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
        modifier = modifier
            .fillMaxWidth()
            .archivLiveHinweis(),
        color = farben.papierHell,
        shape = RoundedCornerShape(6.dp),
        border = BorderStroke(0.75.dp, farben.linieFein),
        shadowElevation = 2.dp,
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .height(IntrinsicSize.Min),
        ) {
            Box(
                modifier = Modifier
                    .width(3.dp)
                    .fillMaxHeight()
                    .background(farben.tinte),
            )
            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(
                        horizontal = metrik.kartenInnenAbstand,
                        vertical = if (metrik.kompakteHoehe) 12.dp else 16.dp,
                    ),
                verticalArrangement = Arrangement.spacedBy(10.dp),
            ) {
                Text(
                    text = ausgang.gewaehlterTitel,
                    style = MaterialTheme.typography.titleMedium,
                    color = farben.akzent,
                    modifier = Modifier.archivUeberschrift(),
                )

                Text(
                    text = ausgang.ausgangsText,
                    style = MaterialTheme.typography.bodyLarge,
                    color = farben.tinte,
                )

                if (ausgang.wirkungen.isNotEmpty()) {
                    FlowRow(
                        horizontalArrangement = Arrangement.spacedBy(6.dp),
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

                Spacer(modifier = Modifier.height(2.dp))

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
                        modifier = Modifier.padding(horizontal = 22.dp, vertical = 12.dp),
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
