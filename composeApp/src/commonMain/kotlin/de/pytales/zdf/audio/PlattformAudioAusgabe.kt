package de.pytales.zdf.audio

import kotlin.math.PI
import kotlin.math.sin

/**
 * Plattform-Fabrik für eine dezente, klickfreie Audio-Ausgabe (Android, Desktop JVM, Web).
 * Alle Implementierungen fangen fehlende Hardware oder Browser-Richtlinien lautlos ab.
 */
expect fun erstellePlattformAudioAusgabe(): AudioAusgabe

/**
 * Reine, leichte Synthese sehr ruhiger, warmer Kammerklänge (16-Bit-PCM) ohne externe
 * Binärdateien. Wird ausschließlich für erlaubte Spuren ([AudioSpur.START_RUHIG],
 * [AudioSpur.HEIMAT_RUHIG], [AudioSpur.EPILOG_RUHIG]) genutzt; [AudioSpur.STILLE] erzeugt
 * ausschließlich Null-Samples.
 */
object RuhigeArchivSynthese {

    const val SAMPLE_RATE: Int = 22_050
    private const val ZWEI_PI: Double = 2.0 * PI

    /**
     * Liefert die ruhigen Grundfrequenzen (in Hz) für die jeweilige Spur:
     * offene, gedämpfte Quinte/Terz im warmen tiefen Register — bewusst ruhig und zurückhaltend.
     */
    fun frequenzenFuer(spur: AudioSpur): DoubleArray = when (spur) {
        AudioSpur.STILLE -> DoubleArray(0)
        // Ruhige offene d-Moll-/D-Quinte (D3, A3, F4)
        AudioSpur.START_RUHIG -> doubleArrayOf(146.83, 220.00, 349.23)
        // Gedämpfter C-Dur/a-Moll-Ruheklang für Heimatalltag (C3, G3, E4)
        AudioSpur.HEIMAT_RUHIG -> doubleArrayOf(130.81, 196.00, 329.63)
        // Nachdenklicher offener Ausklang 1919 (A2, E3, C4)
        AudioSpur.EPILOG_RUHIG -> doubleArrayOf(110.00, 164.81, 261.63)
    }

    /**
     * Erzeugt einen Puffer mit 16-Bit-Little-Endian-PCM-Samples (mono).
     */
    fun fuellePcm16Puffer(
        spur: AudioSpur,
        lautstaerke: Float,
        startSampleIndex: Long,
        ziel: ByteArray,
    ) {
        val begrenzt = AudioRegelwerk.begrenzeLautstaerke(lautstaerke)
        val freqs = frequenzenFuer(spur)
        if (freqs.isEmpty() || begrenzt <= 0f) {
            ziel.fill(0)
            return
        }

        val sampleAnzahl = ziel.size / 2
        // Sanfte, sehr langsame Atem-Hüllkurve (ca. 9 Sekunden Periode), nie aufdringlich
        val basisAmplitude = begrenzt.toDouble() * 0.24 * Short.MAX_VALUE
        val gewichte = doubleArrayOf(0.55, 0.30, 0.15)

        for (i in 0 until sampleAnzahl) {
            val t = (startSampleIndex + i).toDouble() / SAMPLE_RATE.toDouble()
            val atem = 0.72 + 0.28 * sin(ZWEI_PI * 0.11 * t)
            var summe = 0.0
            for (k in freqs.indices) {
                summe += sin(ZWEI_PI * freqs[k] * t) * gewichte[k]
            }
            val sample = (summe * atem * basisAmplitude)
                .toInt()
                .coerceIn(Short.MIN_VALUE.toInt(), Short.MAX_VALUE.toInt())
            val byteIndex = i * 2
            ziel[byteIndex] = (sample and 0xFF).toByte()
            ziel[byteIndex + 1] = ((sample ushr 8) and 0xFF).toByte()
        }
    }
}
