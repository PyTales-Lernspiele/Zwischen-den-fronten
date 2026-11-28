package de.pytales.zdf

import de.pytales.zdf.audio.Klang
import de.pytales.zdf.audio.KlangAusgabe
import de.pytales.zdf.audio.KlangRegelwerk
import de.pytales.zdf.audio.KlangSpieler
import de.pytales.zdf.audio.WavDekoder
import de.pytales.zdf.engine.GameEngine
import de.pytales.zdf.engine.GamePhase
import de.pytales.zdf.engine.KotlinRandomSource
import de.pytales.zdf.model.Geschlecht
import de.pytales.zdf.model.SpielModus
import de.pytales.zdf.ui.state.SpielController
import kotlin.random.Random
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNotNull
import kotlin.test.assertNull
import kotlin.test.assertTrue

/**
 * Prüfsuite für die kurzen Archiv-Klangeffekte (WAV-Dekoder, Zuordnung zu Spielschritten, Ein/Aus).
 */
class KlangeffekteTest {

    private val content = loadTestGameContent()
    private val engine = GameEngine(content, KotlinRandomSource(Random(1916)))

    private class FakeKlangAusgabe : KlangAusgabe {
        override val brauchtRohdaten: Boolean = false
        val gespielt = mutableListOf<Pair<Klang, Float>>()
        override fun lade(klang: Klang, rohdaten: ByteArray?, uri: String?) = Unit
        override fun spiele(klang: Klang, lautstaerke: Float) {
            gespielt += klang to lautstaerke
        }
        override fun freigeben() = Unit
    }

    private fun wav(samples: ShortArray, kanaele: Int = 1, rate: Int = 22_050, mitListChunk: Boolean = true): ByteArray {
        val daten = ArrayList<Byte>()
        fun str(s: String) = s.forEach { daten += it.code.toByte() }
        fun i32(v: Int) = repeat(4) { daten += ((v ushr (8 * it)) and 0xFF).toByte() }
        fun i16(v: Int) = repeat(2) { daten += ((v ushr (8 * it)) and 0xFF).toByte() }
        val datenBytes = samples.size * 2
        val liste = if (mitListChunk) 12 else 0
        str("RIFF"); i32(4 + 24 + liste + 8 + datenBytes); str("WAVE")
        str("fmt "); i32(16); i16(1); i16(kanaele); i32(rate); i32(rate * 2 * kanaele); i16(2 * kanaele); i16(16)
        if (mitListChunk) {
            str("LIST"); i32(4); str("INFO")
        }
        str("data"); i32(datenBytes)
        samples.forEach { i16(it.toInt()) }
        return daten.toByteArray()
    }

    @Test
    fun wavDekoderLiestMonoPcmUndUeberspringtFremdeChunks() {
        val pcm = WavDekoder.dekodiere(wav(shortArrayOf(0, 1000, -1000, 32767, -32768)))
        assertNotNull(pcm)
        assertEquals(22_050, pcm.abtastrate)
        assertEquals(listOf<Short>(0, 1000, -1000, 32767, -32768), pcm.samples.toList())
    }

    @Test
    fun wavDekoderMischtStereoZuMono() {
        val pcm = WavDekoder.dekodiere(wav(shortArrayOf(1000, 3000, -2000, 0), kanaele = 2, mitListChunk = false))
        assertNotNull(pcm)
        assertEquals(listOf<Short>(2000, -1000), pcm.samples.toList())
    }

    @Test
    fun wavDekoderLehntUngueltigeDatenAb() {
        assertNull(WavDekoder.dekodiere(ByteArray(10)))
        assertNull(WavDekoder.dekodiere(ByteArray(64) { 'X'.code.toByte() }))
    }

    @Test
    fun pcmSkalierungBegrenztLautstaerke() {
        val pcm = WavDekoder.dekodiere(wav(shortArrayOf(10000, -10000)))!!
        assertEquals(listOf<Short>(5000, -5000), pcm.skaliert(0.5f).toList())
        assertEquals(listOf<Short>(10000, -10000), pcm.skaliert(3f).toList())
        val bytes = pcm.alsPcm16Bytes(0.5f)
        assertEquals(4, bytes.size)
        assertEquals(5000, (bytes[0].toInt() and 0xFF) or (bytes[1].toInt() shl 8))
    }

    @Test
    fun spielschritteBekommenPassendeKlaenge() {
        val controller = SpielController(engine = engine)
        val phasen = mutableListOf(controller.uiState.value.gameState.phase)
        fun merke() { phasen += controller.uiState.value.gameState.phase }

        assertTrue(controller.waehleModus(SpielModus.KURZ))
        assertTrue(controller.durchgangBeginnen()); merke()
        val herkunft = content.herkunft.herkuenfte.first().id
        controller.waehleHerkunftEntwurf(herkunft)
        controller.waehleGeschlechtEntwurf(Geschlecht.WEIBLICH)
        controller.waehleAlterEntwurf(content.herkunft.jahrgaenge.first().alter)
        assertTrue(controller.bestaetigePerson()); merke()

        // Erster Wechsel: Start → Herkunftswahl = Umblättern
        assertEquals(Klang.UMBLAETTERN, KlangRegelwerk.klangFuerPhasenwechsel(phasen[0], phasen[1]))
        // Kein Klang beim ersten Aufbau und bei unveränderter Phase
        assertNull(KlangRegelwerk.klangFuerPhasenwechsel(null, phasen[0]))
        assertNull(KlangRegelwerk.klangFuerPhasenwechsel(phasen[1], phasen[1]))

        // Bis zur ersten Entscheidung weiterspielen und Klänge prüfen
        var schritte = 0
        while (schritte++ < 20) {
            val vorher = controller.uiState.value.gameState.phase
            when (vorher) {
                is GamePhase.ErwerbWahl -> controller.waehleErwerb(vorher.optionen.first().id)
                is GamePhase.KapitelStart -> controller.starteKapitel()
                is GamePhase.MusterungErgebnis -> controller.bestaetigeMusterung()
                is GamePhase.EreignisAnzeige -> {
                    controller.waehleOption(0)
                    val nachher = controller.uiState.value.gameState.phase
                    assertTrue(nachher is GamePhase.EreignisAusgang)
                    assertEquals(Klang.ENTSCHEIDUNG, KlangRegelwerk.klangFuerPhasenwechsel(vorher, nachher))
                    break
                }
                else -> break
            }
            val nachher = controller.uiState.value.gameState.phase
            val erwartet = when (nachher) {
                is GamePhase.KapitelStart -> Klang.KAPITEL
                is GamePhase.EreignisAnzeige -> Klang.UMBLAETTERN
                is GamePhase.ErwerbWahl -> Klang.UMBLAETTERN
                is GamePhase.MusterungErgebnis -> Klang.STEMPEL
                else -> null
            }
            if (erwartet != null) {
                assertEquals(erwartet, KlangRegelwerk.klangFuerPhasenwechsel(vorher, nachher))
            }
        }
    }

    @Test
    fun klangSpielerRespektiertSchalterUndHintergrund() {
        val ausgabe = FakeKlangAusgabe()
        val spieler = KlangSpieler(ausgabe)
        spieler.spiele(Klang.TIPPEN)
        assertEquals(1, ausgabe.gespielt.size)
        assertTrue(ausgabe.gespielt.single().second in 0f..1f)

        spieler.aktiv = false
        spieler.spiele(Klang.TIPPEN)
        assertEquals(1, ausgabe.gespielt.size)

        spieler.aktiv = true
        spieler.imVordergrund = false
        spieler.spiele(Klang.KAPITEL)
        assertEquals(1, ausgabe.gespielt.size)
    }

    @Test
    fun klaengeSindStandardmaessigAnUndUmschaltbar() {
        val controller = SpielController(engine = engine)
        assertTrue(controller.uiState.value.klaengeAktiv)
        // Hintergrundmusik bleibt standardmäßig aus
        assertFalse(controller.uiState.value.audioAktiv)
        controller.toggleKlaengeAktiv()
        assertFalse(controller.uiState.value.klaengeAktiv)
    }
}
