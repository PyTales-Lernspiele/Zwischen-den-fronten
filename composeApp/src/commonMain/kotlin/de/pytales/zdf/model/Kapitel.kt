package de.pytales.zdf.model

import kotlinx.serialization.Serializable

@Serializable
data class KapitelDaten(
    val epilogJahr: Int,
    val bogenZuschlag: Int,
    val kapitel: List<Kapitel>,
)

@Serializable
data class Kapitel(
    val jahr: Int,
    val istEpilog: Boolean,
    val zeitraum: String,
    val ueberschrift: String,
    val text: String,
    val stichworte: List<String>,
    val rueckblick: String? = null,
    val bildId: String,
    val ziehungen: Map<SpielModus, Int>,
    val wirkungAllgemein: Map<WertSchluessel, Int> = emptyMap(),
    val wirkungNachPfad: Map<Pfad, Map<WertSchluessel, Int>> = emptyMap(),
    val wirkungText: String? = null,
    val bogen: Map<Pfad, KapitelBogen>,
)

@Serializable
data class KapitelBogen(
    val frage: String,
    val kippt: String,
    val traeger: List<String>,
)
