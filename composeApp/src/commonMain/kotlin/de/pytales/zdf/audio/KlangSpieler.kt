package de.pytales.zdf.audio

import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.runtime.staticCompositionLocalOf
import de.pytales.zdf.resources.Res

/**
 * Spielt [Klang]e ab, sofern Klangeffekte eingeschaltet sind und die App im Vordergrund ist.
 * Lädt die WAV-Dateien einmalig beim Start (ca. 170 KB) aus den Compose-Ressourcen.
 */
class KlangSpieler(
    private val ausgabe: KlangAusgabe,
) {
    var aktiv: Boolean = true
    var lautstaerke: Float = KlangRegelwerk.STANDARD_LAUTSTAERKE
    var imVordergrund: Boolean = true

    private var geladen = false

    suspend fun ladeAlle() {
        if (geladen) return
        geladen = true
        Klang.entries.forEach { klang ->
            val bytes = if (ausgabe.brauchtRohdaten) {
                runCatching { Res.readBytes(klang.ressourcenPfad) }.getOrNull()
            } else {
                null
            }
            val uri = runCatching { Res.getUri(klang.ressourcenPfad) }.getOrNull()
            runCatching { ausgabe.lade(klang, bytes, uri) }
        }
    }

    fun spiele(klang: Klang) {
        if (!aktiv || !imVordergrund) return
        val pegel = KlangRegelwerk.begrenzeLautstaerke(lautstaerke) * klang.pegel
        if (pegel <= 0f) return
        runCatching { ausgabe.spiele(klang, pegel) }
    }

    fun freigeben() {
        runCatching { ausgabe.freigeben() }
    }
}

/** Zugriff auf den [KlangSpieler] für beliebige Bedienelemente (z. B. Schalter, Auswahlkarten). */
val LocalKlangSpieler = staticCompositionLocalOf<KlangSpieler?> { null }

/** Kurzform: spielt [klang], falls ein [KlangSpieler] bereitgestellt ist. */
fun KlangSpieler?.tippen(klang: Klang = Klang.TIPPEN) {
    this?.spiele(klang)
}

@Composable
fun rememberKlangSpieler(): KlangSpieler {
    val spieler = remember { KlangSpieler(erstellePlattformKlangAusgabe()) }
    LaunchedEffect(spieler) { spieler.ladeAlle() }
    DisposableEffect(spieler) {
        onDispose { spieler.freigeben() }
    }
    return spieler
}
