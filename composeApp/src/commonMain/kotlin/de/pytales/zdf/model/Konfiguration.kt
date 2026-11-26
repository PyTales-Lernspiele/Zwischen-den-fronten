package de.pytales.zdf.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class Konfiguration(
    val spielTitel: String,
    val untertitel: String,
    val zielgruppe: String,
    val farbwelt: Farbwelt,
    val werte: WerteKonfiguration,
    val stimmungen: StimmungenKonfiguration,
    val pfade: PfadeKonfiguration,
    val modi: Map<SpielModus, ModusKonfiguration>,
    val onboarding: OnboardingKonfiguration,
    val harteEnden: HarteEndenKonfiguration,
)

@Serializable
data class Farbwelt(
    val papier: String,
    val papierHell: String,
    val papierDunkel: String,
    val tinte: String,
    val tinteMatt: String,
    val linie: String,
    val linieFein: String,
    val akzent: String,
    val akzentMatt: String,
    val dunkel: String,
    val dunkelHell: String,
    val segmentLeer: String,
    val segmentDunkel: String,
    val textHell: String,
    val stufen: List<String>,
    val stufenHell: List<String>,
)

@Serializable
data class WerteKonfiguration(
    val reihenfolge: List<WertSchluessel>,
    val minimum: Int,
    val maximum: Int,
    val segmenteJeBalken: Int,
    val balkenVollIstGut: Boolean,
    val definitionen: Map<WertSchluessel, WertDefinition>,
)

@Serializable
data class WertDefinition(
    val bezeichnung: String,
    val hochIstGut: Boolean,
    val erklaerung: String,
    val folge: String,
    val stufenNamen: List<String>,
    val stufenKurz: List<String>,
    val zustandssaetze: List<String>,
)

@Serializable
data class StimmungenKonfiguration(
    val beschreibung: String,
    val standard: Stimmung,
    val alle: List<Stimmung>,
    val abStufe: Int,
    val ausWert: Map<WertSchluessel, Stimmung>,
)

@Serializable
data class PfadeKonfiguration(
    val reihenfolge: List<Pfad>,
    val definitionen: Map<Pfad, PfadDefinition>,
)

@Serializable
data class PfadDefinition(
    val marke: String,
    val ort: String,
    val basisWerte: Map<WertSchluessel, Int>,
)

@Serializable
data class ModusKonfiguration(
    val bezeichnung: String,
    val zielzahl: Int,
    val nurKern: Boolean,
    val umfang: String,
    val dauer: String,
)

@Serializable
data class OnboardingKonfiguration(
    val aufforderung: String,
    val grundsaetze: List<OnboardingGrundsatz>,
)

@Serializable
data class OnboardingGrundsatz(
    val id: String,
    val satz: String,
    val mehr: String,
)

@Serializable
data class HarteEndenKonfiguration(
    val schwellen: AbbruchSchwellen,
    val texte: Map<HartesEndeId, HartesEndeText>,
)

@Serializable
data class AbbruchSchwellen(
    @SerialName("versorgung_unter")
    val versorgungUnter: Int,
    @SerialName("belastung_ab")
    val belastungAb: Int,
    @SerialName("aufmerksamkeit_ab")
    val aufmerksamkeitAb: Int,
)

@Serializable
data class HartesEndeText(
    val titel: String,
    val text: String,
)
