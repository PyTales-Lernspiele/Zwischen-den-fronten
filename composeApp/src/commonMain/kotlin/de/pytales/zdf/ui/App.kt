package de.pytales.zdf.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import de.pytales.zdf.content.ContentLoader
import de.pytales.zdf.content.GameContent
import de.pytales.zdf.ui.components.ArchivTrennlinie
import de.pytales.zdf.ui.screens.SpielScreen
import de.pytales.zdf.ui.state.SpielController
import de.pytales.zdf.ui.theme.ArchivPapierTheme
import de.pytales.zdf.ui.theme.ArchivTheme
import de.pytales.zdf.ui.theme.Schriftgroesse

/**
 * Gemeinsamer Einstiegspunkt für Android, Windows Desktop (JVM) und WebApp (`wasmJs` + JS).
 *
 * Lädt die geprüften JSON-Inhalte aus `content/`, initialisiert das [ArchivPapierTheme]
 * direkt aus `konfiguration.json` und startet über [SpielController] und [SpielScreen]
 * direkt in das echte Spiel (`GamePhase.Start` bis 1919 bzw. Auffangnetz).
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

    val geladen = content
    val controller = remember(geladen) {
        geladen?.let { SpielController(content = it) }
    }
    val uiState = controller?.uiState?.collectAsState()?.value
    val schriftgroesse = uiState?.schriftgroesse ?: Schriftgroesse.MITTEL
    val reduzierteAnimationen = uiState?.reduzierteAnimationen ?: false

    ArchivPapierTheme(
        farbwelt = geladen?.konfiguration?.farbwelt,
        schriftgroesse = schriftgroesse,
        reduzierteAnimationen = reduzierteAnimationen,
    ) {
        val farben = ArchivTheme.farben
        Surface(
            modifier = Modifier.fillMaxSize(),
            color = farben.papier,
        ) {
            when {
                fehler != null -> LadeStatusKarte(
                    titel = "Fehler beim Laden der Spielinhalte",
                    untertitel = fehler.orEmpty(),
                    istFehler = true,
                )

                controller == null -> LadeStatusKarte(
                    titel = "Zwischen den Fronten",
                    untertitel = "Archivdaten (1914–1919) werden geladen …",
                    istFehler = false,
                )

                else -> SpielScreen(controller = controller)
            }
        }
    }
}

@Composable
private fun LadeStatusKarte(
    titel: String,
    untertitel: String,
    istFehler: Boolean,
) {
    val farben = ArchivTheme.farben
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(farben.papier)
            .padding(24.dp),
        contentAlignment = Alignment.Center,
    ) {
        Surface(
            modifier = Modifier.widthIn(max = 520.dp),
            color = farben.papierHell,
            shape = RoundedCornerShape(4.dp),
            border = BorderStroke(1.dp, if (istFehler) farben.akzent else farben.linie),
        ) {
            Column(
                modifier = Modifier.padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(10.dp),
            ) {
                Text(
                    text = titel,
                    style = MaterialTheme.typography.headlineMedium,
                    color = if (istFehler) farben.akzent else farben.tinte,
                    textAlign = TextAlign.Center,
                )
                ArchivTrennlinie(farbe = farben.linieFein)
                Text(
                    text = untertitel,
                    style = MaterialTheme.typography.bodyMedium,
                    color = farben.tinteMatt,
                    textAlign = TextAlign.Center,
                )
            }
        }
    }
}
