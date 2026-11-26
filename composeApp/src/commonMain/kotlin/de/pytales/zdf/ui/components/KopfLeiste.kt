package de.pytales.zdf.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import de.pytales.zdf.model.WertSchluessel
import de.pytales.zdf.ui.state.LiveEmotionUiState
import de.pytales.zdf.ui.state.WertKachelUiState
import de.pytales.zdf.ui.theme.ArchivTheme

/**
 * Vollständige responsive Kopfleiste von „Zwischen den Fronten“:
 * - Dunkler Archiv-Kopf (`dunkel`) mit Jahr/Pfad-Orientierung
 * - Obere [BefindensLeiste] (4 Werte, 5-Segment-Balken, Delta, Touch-/Klick-Erklärkarte)
 * - [LiveEmotionsKachel] rechts oben (bei [LayoutKlasse.MITTEL] und [LayoutKlasse.BREIT])
 *   bzw. kompakt über der 2×2-Befindensleiste (bei [LayoutKlasse.KOMPAKT])
 * - Angeheftete Erklär- bzw. Figuren-Detailkarte direkt unterhalb der Leiste.
 */
@Composable
fun KopfLeiste(
    jahr: Int,
    werte: List<WertKachelUiState>,
    emotion: LiveEmotionUiState,
    modifier: Modifier = Modifier,
    kapitelTitel: String? = null,
    analyseModus: Boolean = false,
    ausgewaehlterWert: WertSchluessel? = null,
    onAusgewaehlterWertChange: ((WertSchluessel?) -> Unit)? = null,
    zusatzAktionen: (@Composable () -> Unit)? = null,
    portraitContent: (@Composable BoxScope.(portraitId: String) -> Unit)? = null,
) {
    var internerWert by remember { mutableStateOf<WertSchluessel?>(null) }
    var emotionDetailsOffen by remember { mutableStateOf(false) }

    val aktiverWertSchluessel = if (onAusgewaehlterWertChange != null) {
        ausgewaehlterWert
    } else {
        internerWert
    }
    val setzeWert: (WertSchluessel?) -> Unit = { neu ->
        if (neu != null) {
            emotionDetailsOffen = false
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

    Column(modifier = modifier.fillMaxWidth()) {
        // Dunkle Haupt-Kopfleiste
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(farben.dunkel),
            contentAlignment = Alignment.Center,
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .widthIn(max = metrik.maxInhaltsBreite)
                    .padding(horizontal = metrik.aussenAbstand, vertical = 10.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp),
            ) {
                // Schmale Kontextzeile: Jahr · Kapitel/Pfad + optionale Werkzeuge
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
                            text = jahr.toString(),
                            farbe = farben.stufenFarbeHell(2),
                            hintergrund = farben.dunkelHell,
                        )
                        Text(
                            text = buildString {
                                append(emotion.pfadMarke)
                                if (!kapitelTitel.isNullOrBlank()) {
                                    append(" · $kapitelTitel")
                                }
                            },
                            style = MaterialTheme.typography.labelMedium,
                            color = farben.textHell.copy(alpha = 0.85f),
                            fontWeight = FontWeight.Medium,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                        )
                    }

                    if (zusatzAktionen != null) {
                        zusatzAktionen()
                    }
                }

                // Kernbereich: Befindensleiste + Live-Emotions-Kachel rechts oben
                if (metrik.kopfNebeneinander) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        BefindensLeiste(
                            werte = werte,
                            ausgewaehlterWert = aktiverWertSchluessel,
                            onWertTippen = { schluessel ->
                                setzeWert(if (aktiverWertSchluessel == schluessel) null else schluessel)
                            },
                            aufDunkel = true,
                            spalten = metrik.werteSpalten,
                            modifier = Modifier.weight(1f),
                        )

                        LiveEmotionsKachel(
                            emotion = emotion,
                            aufDunkel = true,
                            kompakt = false,
                            detailsOffen = emotionDetailsOffen,
                            onTippen = {
                                val neu = !emotionDetailsOffen
                                emotionDetailsOffen = neu
                                if (neu) setzeWert(null)
                            },
                            portraitContent = portraitContent,
                            modifier = Modifier.widthIn(min = 230.dp, max = 310.dp),
                        )
                    }
                } else {
                    // Android-Hochformat (KOMPAKT): Kachel oben kompakt, 4 Werte als 2×2-Raster darunter
                    LiveEmotionsKachel(
                        emotion = emotion,
                        aufDunkel = true,
                        kompakt = true,
                        detailsOffen = emotionDetailsOffen,
                        onTippen = {
                            val neu = !emotionDetailsOffen
                            emotionDetailsOffen = neu
                            if (neu) setzeWert(null)
                        },
                        portraitContent = portraitContent,
                        modifier = Modifier.fillMaxWidth(),
                    )

                    BefindensLeiste(
                        werte = werte,
                        ausgewaehlterWert = aktiverWertSchluessel,
                        onWertTippen = { schluessel ->
                            setzeWert(if (aktiverWertSchluessel == schluessel) null else schluessel)
                        },
                        aufDunkel = true,
                        spalten = metrik.werteSpalten,
                    )
                }
            }
        }

        HorizontalDivider(thickness = 1.dp, color = farben.linie)

        // Aufgeklappte Touch-/Klick-Erklärkarte bzw. Figuren-Detailkarte direkt unter der Kopfleiste
        if (ausgewaehlterStatus != null || emotionDetailsOffen) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(farben.papier),
                contentAlignment = Alignment.Center,
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .widthIn(max = metrik.maxInhaltsBreite)
                        .padding(horizontal = metrik.aussenAbstand, vertical = 10.dp),
                ) {
                    WertErklaerKarte(
                        wert = ausgewaehlterStatus,
                        onSchliessen = { setzeWert(null) },
                    )
                    LiveEmotionDetailKarte(
                        emotion = emotion,
                        sichtbar = emotionDetailsOffen && ausgewaehlterStatus == null,
                        analyseModus = analyseModus,
                        onSchliessen = { emotionDetailsOffen = false },
                        portraitContent = portraitContent,
                    )
                }
            }
        }
    }
}
