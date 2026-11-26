package de.pytales.zdf.ui.media

import androidx.compose.runtime.Immutable

/**
 * Kennzeichnet, aus welcher Medien-Stufe ein angefragtes Motiv tatsächlich bedient wird.
 */
enum class BildEbene(val kurzLabel: String) {
    EINZELSZENE_STUFE2("Stufe 2 · Einzelszene"),
    SCHAUPLATZ_STUFE1("Stufe 1 · Schauplatz"),
    KAPITEL_STUFE1("Stufe 1 · Kapitel"),
    PORTRAIT_STUFE1("Stufe 1 · Live-Emotion"),
    PORTRAIT_BASIS_FALLBACK("Stufe 1 · Basis-Portrait"),
    PLATZHALTER("Archiv-Platzhalter"),
}

/**
 * Ergebnis der plattformunabhängigen Bild-Auflösung für Szenen, Kapitel und Live-Portraits.
 */
@Immutable
data class AufgeloestesBild(
    val angefragteId: String,
    val aufgeloesteId: String?,
    val ebene: BildEbene,
    val istFallback: Boolean,
) {
    val istVorhanden: Boolean get() = aufgeloesteId != null
}

/**
 * Reine, zustandslose und vollständig testbare Bild-Auflösung für AP 5 (Stufe 1 → Stufe 2):
 *
 * - Szenenbild: `einzelSzenenbild` (Stufe 2) → `schauplatzBild` (Stufe 1) → Archiv-Platzhalter
 * - Kapitelbild: `kapitel_<jahr>` (Stufe 1) → Archiv-Platzhalter
 * - Live-Emotions-Portrait: `portrait_<herkunft>_<g>_<stimmung>` (Stufe 1)
 *   → `portrait_<herkunft>_<g>_neutral` (Basis-Fallback derselben Figur) → Archiv-Platzhalter
 */
object BildAufloeser {

    private val BEKANNTE_STIMMUNGEN: Set<String> = setOf(
        "neutral",
        "hungrig",
        "erschoepft",
        "angst",
        "einsam",
    )

    fun loeseSzene(
        bildId: String,
        schauplatzBild: String,
        verfuegbareIds: Set<String>,
    ): AufgeloestesBild {
        if (bildId.isNotBlank() && bildId in verfuegbareIds) {
            return AufgeloestesBild(
                angefragteId = bildId,
                aufgeloesteId = bildId,
                ebene = BildEbene.EINZELSZENE_STUFE2,
                istFallback = false,
            )
        }
        if (schauplatzBild.isNotBlank() && schauplatzBild in verfuegbareIds) {
            return AufgeloestesBild(
                angefragteId = bildId,
                aufgeloesteId = schauplatzBild,
                ebene = BildEbene.SCHAUPLATZ_STUFE1,
                istFallback = true,
            )
        }
        return AufgeloestesBild(
            angefragteId = bildId,
            aufgeloesteId = null,
            ebene = BildEbene.PLATZHALTER,
            istFallback = true,
        )
    }

    fun loeseKapitel(
        kapitelBildId: String,
        verfuegbareIds: Set<String>,
    ): AufgeloestesBild {
        if (kapitelBildId.isNotBlank() && kapitelBildId in verfuegbareIds) {
            return AufgeloestesBild(
                angefragteId = kapitelBildId,
                aufgeloesteId = kapitelBildId,
                ebene = BildEbene.KAPITEL_STUFE1,
                istFallback = false,
            )
        }
        return AufgeloestesBild(
            angefragteId = kapitelBildId,
            aufgeloesteId = null,
            ebene = BildEbene.PLATZHALTER,
            istFallback = true,
        )
    }

    fun loesePortrait(
        portraitId: String,
        verfuegbareIds: Set<String>,
    ): AufgeloestesBild {
        if (portraitId.isNotBlank() && portraitId in verfuegbareIds) {
            return AufgeloestesBild(
                angefragteId = portraitId,
                aufgeloesteId = portraitId,
                ebene = BildEbene.PORTRAIT_STUFE1,
                istFallback = false,
            )
        }
        val basisId = basisPortraitIdFuer(portraitId)
        if (basisId != null && basisId != portraitId && basisId in verfuegbareIds) {
            return AufgeloestesBild(
                angefragteId = portraitId,
                aufgeloesteId = basisId,
                ebene = BildEbene.PORTRAIT_BASIS_FALLBACK,
                istFallback = true,
            )
        }
        return AufgeloestesBild(
            angefragteId = portraitId,
            aufgeloesteId = null,
            ebene = BildEbene.PLATZHALTER,
            istFallback = true,
        )
    }

    /**
     * Leitet aus `portrait_<herkunft>_<m|w>_<stimmung>` die neutrale Basis-Portrait-ID
     * derselben Figur ab (`portrait_<herkunft>_<m|w>_neutral`).
     */
    internal fun basisPortraitIdFuer(portraitId: String): String? {
        if (!portraitId.startsWith("portrait_")) return null
        val letzterUnterstrich = portraitId.lastIndexOf('_')
        if (letzterUnterstrich <= "portrait_".length) return null
        val stimmung = portraitId.substring(letzterUnterstrich + 1)
        if (stimmung !in BEKANNTE_STIMMUNGEN || stimmung == "neutral") return null
        return portraitId.substring(0, letzterUnterstrich + 1) + "neutral"
    }
}
