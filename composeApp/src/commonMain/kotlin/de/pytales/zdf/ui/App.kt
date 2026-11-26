package de.pytales.zdf.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import de.pytales.zdf.content.ContentLoader
import de.pytales.zdf.content.GameContent
import de.pytales.zdf.engine.GameEngine

private val PapierFarbe = Color(0xFFEFE9DC)
private val TinteFarbe = Color(0xFF1F1C18)
private val TinteMattFarbe = Color(0xFF57514A)
private val AkzentFarbe = Color(0xFF8A3324)

/**
 * Minimaler AP-2-Startbildschirm (Platzhalter).
 * Prüft das plattformübergreifende Laden der JSON-Dateien aus `content/` und die Initialisierung der [GameEngine].
 * Die eigentliche Archivpapier-Oberfläche folgt in AP 3.
 */
@Composable
fun App() {
    var content by remember { mutableStateOf<GameContent?>(null) }
    var fehler by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(Unit) {
        try {
            content = ContentLoader.loadFromComposeResources()
        } catch (e: Throwable) {
            fehler = e.message ?: e::class.simpleName ?: "Unbekannter Ladefehler"
        }
    }

    MaterialTheme {
        Surface(
            modifier = Modifier.fillMaxSize(),
            color = PapierFarbe,
        ) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(PapierFarbe)
                    .padding(32.dp),
                contentAlignment = Alignment.Center,
            ) {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(12.dp),
                ) {
                    val geladen = content
                    when {
                        fehler != null -> {
                            Text(
                                text = "Fehler beim Laden der Spielinhalte",
                                style = MaterialTheme.typography.headlineSmall,
                                color = AkzentFarbe,
                                fontWeight = FontWeight.Bold,
                            )
                            Text(
                                text = fehler.orEmpty(),
                                style = MaterialTheme.typography.bodyMedium,
                                color = TinteFarbe,
                            )
                        }

                        geladen == null -> {
                            Text(
                                text = "Zwischen den Fronten",
                                style = MaterialTheme.typography.headlineMedium,
                                color = TinteFarbe,
                                fontWeight = FontWeight.Bold,
                            )
                            Text(
                                text = "Spielinhalte werden geladen …",
                                style = MaterialTheme.typography.bodyMedium,
                                color = TinteMattFarbe,
                            )
                        }

                        else -> {
                            val engine = remember(geladen) { GameEngine(geladen) }
                            val startZustand = remember(engine) { engine.neuesSpiel() }
                            val stimmung = engine.liveEmotion(startZustand).stimmung

                            Text(
                                text = geladen.konfiguration.spielTitel,
                                style = MaterialTheme.typography.headlineMedium,
                                color = TinteFarbe,
                                fontWeight = FontWeight.Bold,
                            )
                            Text(
                                text = geladen.konfiguration.untertitel,
                                style = MaterialTheme.typography.titleMedium,
                                color = AkzentFarbe,
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = "${geladen.ereignisse.ereignisse.size} Ereignisse · " +
                                    "${geladen.kapitel.kapitel.size} Kapitel · " +
                                    "${geladen.merkmale.register.size} Merkmale · " +
                                    "${geladen.medienplan.portraits.size} Live-Portraits",
                                style = MaterialTheme.typography.bodyMedium,
                                color = TinteFarbe,
                            )
                            Text(
                                text = "Engine bereit (Jahr ${startZustand.jahr}, Stimmung: ${stimmung.code}) — UI folgt in AP 3.",
                                style = MaterialTheme.typography.bodySmall,
                                color = TinteMattFarbe,
                            )
                        }
                    }
                }
            }
        }
    }
}
