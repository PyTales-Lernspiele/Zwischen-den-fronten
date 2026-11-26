package de.pytales.zdf.content

import de.pytales.zdf.model.EreignisseDaten
import de.pytales.zdf.model.HerkunftDaten
import de.pytales.zdf.model.KapitelDaten
import de.pytales.zdf.model.Konfiguration
import de.pytales.zdf.model.Medienplan
import de.pytales.zdf.model.MerkmaleDaten
import de.pytales.zdf.model.Sprachregeln
import de.pytales.zdf.resources.Res
import kotlinx.serialization.json.Json

/**
 * Lädt und deserialisiert alle 7 Spielinhalts-Dateien aus `content/` (Single Source of Truth).
 */
object ContentLoader {
    const val FILE_KONFIGURATION = "konfiguration.json"
    const val FILE_HERKUNFT = "herkunft.json"
    const val FILE_KAPITEL = "kapitel.json"
    const val FILE_MERKMALE = "merkmale.json"
    const val FILE_EREIGNISSE = "ereignisse.json"
    const val FILE_SPRACHREGELN = "sprachregeln.json"
    const val FILE_MEDIENPLAN = "medienplan.json"

    val ALL_FILES: List<String> = listOf(
        FILE_KONFIGURATION,
        FILE_HERKUNFT,
        FILE_KAPITEL,
        FILE_MERKMALE,
        FILE_EREIGNISSE,
        FILE_SPRACHREGELN,
        FILE_MEDIENPLAN,
    )

    val json: Json = Json {
        ignoreUnknownKeys = false
        explicitNulls = false
    }

    fun parseFromProvider(readFile: (String) -> String): GameContent = GameContent(
        konfiguration = json.decodeFromString<Konfiguration>(readFile(FILE_KONFIGURATION)),
        herkunft = json.decodeFromString<HerkunftDaten>(readFile(FILE_HERKUNFT)),
        kapitel = json.decodeFromString<KapitelDaten>(readFile(FILE_KAPITEL)),
        merkmale = json.decodeFromString<MerkmaleDaten>(readFile(FILE_MERKMALE)),
        ereignisse = json.decodeFromString<EreignisseDaten>(readFile(FILE_EREIGNISSE)),
        sprachregeln = json.decodeFromString<Sprachregeln>(readFile(FILE_SPRACHREGELN)),
        medienplan = json.decodeFromString<Medienplan>(readFile(FILE_MEDIENPLAN)),
    )

    suspend fun loadFromComposeResources(): GameContent {
        val cache = buildMap {
            for (fileName in ALL_FILES) {
                val bytes = Res.readBytes("files/content/$fileName")
                put(fileName, bytes.decodeToString())
            }
        }
        return parseFromProvider { cache.getValue(it) }
    }
}
