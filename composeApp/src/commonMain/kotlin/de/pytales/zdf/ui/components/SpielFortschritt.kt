package de.pytales.zdf.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
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
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.clearAndSetSemantics
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import de.pytales.zdf.ui.theme.ArchivTheme

/**
 * Gut lesbare Zeitleiste 1914–1919: zeigt auf einen Blick, in welchem Jahr (Kapitel) man gerade ist
 * und wie viel noch vor einem liegt. Vergangene Jahre sind gefüllt, das aktuelle Jahr ist hervorgehoben.
 */
@Composable
fun ZeitleistenFortschritt(
    jahre: List<Int>,
    aktuellesJahr: Int,
    modifier: Modifier = Modifier,
) {
    if (jahre.isEmpty()) return
    val farben = ArchivTheme.farben
    val kompakt = ArchivTheme.metrik.kompakteHoehe
    val aktuellerIndex = jahre.indexOfLast { it <= aktuellesJahr }.coerceAtLeast(0)

    Row(
        modifier = modifier
            .fillMaxWidth()
            .clearAndSetSemantics {
                contentDescription = "Kapitel ${aktuellerIndex + 1} von ${jahre.size}: Jahr ${jahre[aktuellerIndex]}"
            },
        horizontalArrangement = Arrangement.spacedBy(4.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        jahre.forEachIndexed { index, jahr ->
            val vergangen = index < aktuellerIndex
            val aktuell = index == aktuellerIndex
            Column(
                modifier = Modifier.weight(1f),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(3.dp),
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(if (aktuell) 5.dp else 3.dp)
                        .background(
                            when {
                                aktuell -> farben.akzent
                                vergangen -> farben.tinte.copy(alpha = 0.55f)
                                else -> farben.linieFein
                            },
                            RoundedCornerShape(3.dp),
                        ),
                )
                if (!kompakt || aktuell || index == 0 || index == jahre.lastIndex) {
                    Text(
                        text = jahr.toString(),
                        style = MaterialTheme.typography.labelSmall,
                        fontWeight = if (aktuell) FontWeight.Bold else FontWeight.Normal,
                        color = when {
                            aktuell -> farben.akzent
                            vergangen -> farben.tinteMatt
                            else -> farben.tinteMatt.copy(alpha = 0.6f)
                        },
                        textAlign = TextAlign.Center,
                    )
                }
            }
        }
    }
}

/**
 * Fest verankerte Aktionsleiste am unteren Rand: Hier liegt immer, was als Nächstes zu tun ist
 * (zwei Entscheidungen oder „Weiter“). So muss niemand suchen oder erst scrollen.
 */
@Composable
fun AktionsLeiste(
    modifier: Modifier = Modifier,
    frage: String? = null,
    inhalt: @Composable ColumnScope.() -> Unit,
) {
    val farben = ArchivTheme.farben
    val kompakt = ArchivTheme.metrik.kompakteHoehe
    Surface(
        modifier = modifier.fillMaxWidth(),
        color = farben.papierHell,
        shape = RoundedCornerShape(8.dp),
        shadowElevation = 6.dp,
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, farben.linie.copy(alpha = 0.6f), RoundedCornerShape(8.dp))
                .padding(horizontal = if (kompakt) 10.dp else 14.dp, vertical = if (kompakt) 8.dp else 12.dp),
            verticalArrangement = Arrangement.spacedBy(if (kompakt) 6.dp else 10.dp),
        ) {
            if (frage != null) {
                Row(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Box(
                        modifier = Modifier
                            .size(8.dp)
                            .background(farben.akzent, CircleShape),
                    )
                    Text(
                        text = frage,
                        style = if (kompakt) MaterialTheme.typography.titleSmall else MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold,
                        color = farben.tinte,
                    )
                }
            }
            inhalt()
        }
    }
}
