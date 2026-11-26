package de.pytales.zdf.model

import kotlinx.serialization.Serializable

@Serializable
data class Sprachregeln(
    val zielgruppe: String,
    val maxWoerterJeSatz: Int,
    val zielSchnittWoerterJeSatz: Int,
    val tabuBegriffe: List<SprachBegriff>,
    val pruefBegriffe: List<SprachBegriff>,
)

@Serializable
data class SprachBegriff(
    val begriff: String,
    val grund: String,
)
