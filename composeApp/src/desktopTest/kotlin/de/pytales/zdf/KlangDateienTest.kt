package de.pytales.zdf

import de.pytales.zdf.audio.Klang
import de.pytales.zdf.audio.WavDekoder
import java.io.File
import kotlin.test.Test
import kotlin.test.assertNotNull
import kotlin.test.assertTrue

/**
 * Prüft, dass alle mitgelieferten Klangdateien vorhanden, dekodierbar und kurz sind.
 */
class KlangDateienTest {

    private val ordner = listOf(
        File("src/commonMain/composeResources/files/klaenge"),
        File("composeApp/src/commonMain/composeResources/files/klaenge"),
    ).first { it.isDirectory }

    @Test
    fun alleKlaengeSindKurzeMonoWavs() {
        Klang.entries.forEach { klang ->
            val datei = File(ordner, klang.datei)
            assertTrue(datei.isFile, "Klangdatei fehlt: ${klang.datei}")
            assertTrue(datei.length() < 64_000, "Klangdatei zu groß: ${klang.datei}")
            val pcm = WavDekoder.dekodiere(datei.readBytes())
            assertNotNull(pcm, "Nicht dekodierbar: ${klang.datei}")
            assertTrue(pcm.dauerSekunden in 0.03..1.0, "Unpassende Dauer ${pcm.dauerSekunden}s: ${klang.datei}")
            assertTrue(pcm.samples.any { it.toInt() != 0 }, "Stille Datei: ${klang.datei}")
        }
    }
}
