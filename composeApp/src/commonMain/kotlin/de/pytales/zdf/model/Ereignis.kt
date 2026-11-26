package de.pytales.zdf.model

import kotlinx.serialization.Serializable

@Serializable
data class EreignisseDaten(
    val schemaVersion: Int,
    val anzahl: Int,
    val ereignisse: List<Ereignis>,
)

@Serializable
data class Ereignis(
    val id: String,
    val kategorie: EreignisKategorie,
    val jahre: List<Int>,
    val pfade: List<Pfad>,
    val ort: String,
    val schauplatzBild: String,
    val bildId: String,
    val kartentyp: Kartentyp,
    val kern: Boolean,
    val gewicht: Int,
    val gewichtBonus: Map<String, Int> = emptyMap(),
    val wiederholbar: Boolean = false,
    val nurKette: Boolean = false,
    val stimmung: Stimmung? = null,
    val braucht: List<String> = emptyList(),
    val brauchtEines: List<String> = emptyList(),
    val verbietet: List<String> = emptyList(),
    val knuepftAn: List<String> = emptyList(),
    val text: TextFassung,
    val optionen: List<EreignisOption>,
    val quelle: Quelle,
)

@Serializable
data class TextFassung(
    val standard: String,
    val varianten: List<TextVariante> = emptyList(),
)

@Serializable
data class TextVariante(
    val text: String,
    val pfad: Pfad? = null,
    val merkmal: String? = null,
    val abJahr: Int? = null,
)

@Serializable
data class EreignisOption(
    val titel: String,
    val beschreibung: String,
    val ausgang: TextFassung,
    val hinweis: String? = null,
    val wirkung: Map<WertSchluessel, Int> = emptyMap(),
    val merkmale: List<String> = emptyList(),
    val stimmung: Stimmung? = null,
    val folgeEreignis: FolgeEreignis? = null,
    val zufallsAusgaenge: List<ZufallsAusgang> = emptyList(),
)

@Serializable
data class FolgeEreignis(
    val id: String,
    val abJahr: Int = 0,
)

@Serializable
data class ZufallsAusgang(
    val gewicht: Int = 1,
    val ausgang: String? = null,
    val wirkung: Map<WertSchluessel, Int> = emptyMap(),
    val sprungEnde: HartesEndeId? = null,
)

@Serializable
data class Quelle(
    val kurz: String,
    val voll: String? = null,
    val art: String,
    val einordnung: String,
    val vertiefung: String? = null,
)
