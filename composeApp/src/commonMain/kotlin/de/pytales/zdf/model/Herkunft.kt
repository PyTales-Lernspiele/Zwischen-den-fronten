package de.pytales.zdf.model

import kotlinx.serialization.Serializable

@Serializable
data class HerkunftDaten(
    val jahrgaenge: List<JahrgangOption>,
    val altersgruppen: List<Altersgruppe>,
    val herkuenfte: List<Herkunft>,
    val erwerbslagen: List<Erwerbslage>,
    val musterung: MusterungDaten,
    val direktwahlOption: DirektwahlOption,
)

@Serializable
data class JahrgangOption(
    val alter: Int,
    val marke: String,
)

@Serializable
data class Altersgruppe(
    val von: Int,
    val bis: Int,
    val schluessel: String,
    val bezeichnung: String,
)

@Serializable
data class Herkunft(
    val id: String,
    val titel: String,
    val zusatz: String,
    val text: String,
    val folge: String,
    val werte: Map<WertSchluessel, Int> = emptyMap(),
    val merkmale: List<String> = emptyList(),
    val berufe: Map<Geschlecht, List<String>>,
    val vornamen: Map<Geschlecht, List<String>>,
    val familiennamen: List<String>,
)

@Serializable
data class Erwerbslage(
    val id: String,
    val titel: String,
    val zusatz: String,
    val text: String,
    val folge: String,
    val bezeichnung: Map<Geschlecht, String>,
    val werte: Map<WertSchluessel, Int> = emptyMap(),
    val merkmale: List<String> = emptyList(),
    val brauchtHerkunft: List<String> = emptyList(),
    val nurGeschlecht: Geschlecht? = null,
    val verbietetMerkmal: List<String> = emptyList(),
    val hinweisFuer: List<String> = emptyList(),
    val etappeMoeglich: Boolean = false,
)

@Serializable
data class MusterungDaten(
    val grade: Map<MusterungsGrad, MusterungGradInfo>,
    val vermerke: Map<MusterungsVermerk, MusterungVermerkInfo>,
    val grundwerte: Map<String, Map<String, Int>>,
    val herkunftEinfluss: Map<String, Map<String, Int>>,
    val strenge: Map<String, Map<String, Int>>,
    val ukWahrscheinlichkeit: Map<String, Int>,
)

@Serializable
data class MusterungGradInfo(
    val kurz: String,
    val lang: String,
    val erklaerung: String,
    val befunde: List<String>,
)

@Serializable
data class MusterungVermerkInfo(
    val kurz: String,
    val lang: String,
    val erklaerung: String,
)

@Serializable
data class DirektwahlOption(
    val aktiv: Boolean,
    val beschreibung: String,
)
