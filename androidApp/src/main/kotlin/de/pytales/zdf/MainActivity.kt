package de.pytales.zdf

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.SystemBarStyle
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import de.pytales.zdf.audio.AndroidAudioLebenszyklus
import de.pytales.zdf.ui.App

/**
 * Android-Einstiegspunkt für „Zwischen den Fronten“ (Alltag 1914–1919):
 * - Aktiviert Edge-to-Edge mit dunkler Archiv-Statusleiste (`#15130F`, helle System-Icons)
 *   und warmer Archivpapier-Navigationsleiste (`#EFE9DC`, dunkle System-Icons). Sichere
 *   Safe-Area-Insets (`WindowInsets.safeDrawing`) in der UI verhindern Abschneiden unter
 *   Kamera-Notch, Statusbar und Navigationsleiste.
 * - Stoppt optionales Audio beim Wechsel in den Hintergrund (`onPause` / `onStop`)
 *   synchron und nimmt es bei Rückkehr (`onResume`) nur auf erlaubten Pfaden wieder auf.
 * - Übergibt [finish] für das bestätigte Schließen über die ruhige Zurück-Sicherheitsabfrage.
 */
class MainActivity : ComponentActivity() {

    private var appImVordergrund by mutableStateOf(true)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.dark(ARCHIV_DUNKEL_ARGB),
            navigationBarStyle = SystemBarStyle.light(
                scrim = ARCHIV_PAPIER_ARGB,
                darkScrim = ARCHIV_DUNKEL_ARGB,
            ),
        )

        setContent {
            App(
                appImVordergrund = appImVordergrund,
                onAppBeenden = ::finish,
            )
        }
    }

    override fun onResume() {
        super.onResume()
        AndroidAudioLebenszyklus.onVordergrund()
        appImVordergrund = true
    }

    override fun onPause() {
        appImVordergrund = false
        AndroidAudioLebenszyklus.onHintergrund()
        super.onPause()
    }

    override fun onStop() {
        appImVordergrund = false
        AndroidAudioLebenszyklus.onHintergrund()
        super.onStop()
    }

    private companion object {
        const val ARCHIV_DUNKEL_ARGB: Int = 0xFF15130F.toInt()
        const val ARCHIV_PAPIER_ARGB: Int = 0xFFEFE9DC.toInt()
    }
}
