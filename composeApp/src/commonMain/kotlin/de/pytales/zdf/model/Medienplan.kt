package de.pytales.zdf.model

import kotlinx.serialization.Serializable

@Serializable
data class Medienplan(
    val hinweis: String,
    val format: MedienFormat,
    val zusammenfassung: MedienZusammenfassung,
    val portraits: List<PortraitAsset>,
    val kapitelbilder: List<KapitelbildAsset>,
    val schauplatzbilder: List<SchauplatzbildAsset>,
    val einzelSzenenbilder: List<EinzelSzenenbildAsset>,
)

@Serializable
data class MedienFormat(
    val dateityp: String,
    val szenenMasse: List<Int>,
    val portraitMasse: List<Int>,
)

@Serializable
data class MedienZusammenfassung(
    val stufe1PortraitsLiveEmotionen: Int,
    val stufe1Kapitelbilder: Int,
    val stufe1Schauplatzbilder: Int,
    val stufe1Gesamt: Int,
    val stufe2EinzelSzenenbilder: Int,
)

@Serializable
data class PortraitAsset(
    val id: String,
    val herkunft: String,
    val geschlecht: Geschlecht,
    val stimmung: Stimmung,
    val stufe: Int,
    val status: String,
)

@Serializable
data class KapitelbildAsset(
    val id: String,
    val jahr: Int,
    val titel: String,
    val stufe: Int,
    val status: String,
)

@Serializable
data class SchauplatzbildAsset(
    val id: String,
    val stufe: Int,
    val status: String,
)

@Serializable
data class EinzelSzenenbildAsset(
    val id: String,
    val fallback: String,
    val ort: String,
    val jahre: List<Int>,
    val pfade: List<Pfad>,
    val stufe: Int,
    val status: String,
)
