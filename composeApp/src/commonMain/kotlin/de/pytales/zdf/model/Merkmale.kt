package de.pytales.zdf.model

import kotlinx.serialization.Serializable

@Serializable
data class MerkmaleDaten(
    val textPrioritaet: List<String>,
    val register: Map<String, MerkmalEintrag>,
    val lebenslauf: LebenslaufKonfiguration,
)

@Serializable
data class MerkmalEintrag(
    val gruppe: MerkmalGruppe,
    val name: String,
    val rang: Int,
    val nachklang: Nachklang? = null,
)

@Serializable
data class Nachklang(
    val jahr: Int,
    val datum: String,
    val text: String,
)

@Serializable
data class LebenslaufKonfiguration(
    val faecher: List<LebenslaufFachKonfiguration>,
    val schlussMerkmale: List<String>,
    val kriegsende: Map<Pfad, Nachklang>,
    val politischeLage: List<PolitischeLageEintrag>,
    val versailles: Nachklang,
    val ausgaenge: List<AusgangDefinition>,
)

@Serializable
data class LebenslaufFachKonfiguration(
    val titel: String,
    val gruppen: List<MerkmalGruppe>,
)

@Serializable
data class PolitischeLageEintrag(
    val id: String,
    val bedingung: AusgangBedingung,
    val eintrag: Nachklang,
)

@Serializable
data class AusgangDefinition(
    val id: String,
    val titel: String,
    val rang: Int,
    val bedingung: AusgangBedingung,
    val deutung: String,
    val eintrag: Nachklang,
    val lehrplan: String,
)

@Serializable
data class AusgangBedingung(
    val immer: Boolean = false,
    val pfade: List<Pfad> = emptyList(),
    val geschlecht: Geschlecht? = null,
    val einesDerMerkmale: List<String> = emptyList(),
    val minStufe: Map<WertSchluessel, Int> = emptyMap(),
    val maxStufe: Map<WertSchluessel, Int> = emptyMap(),
    val minStufeEines: Map<WertSchluessel, Int> = emptyMap(),
    val oderMerkmal: List<String> = emptyList(),
    val oderMinStufe: Map<WertSchluessel, Int> = emptyMap(),
)
