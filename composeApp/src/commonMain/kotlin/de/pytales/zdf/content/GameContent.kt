package de.pytales.zdf.content

import de.pytales.zdf.model.Ereignis
import de.pytales.zdf.model.EreignisseDaten
import de.pytales.zdf.model.Erwerbslage
import de.pytales.zdf.model.Herkunft
import de.pytales.zdf.model.HerkunftDaten
import de.pytales.zdf.model.Kapitel
import de.pytales.zdf.model.KapitelDaten
import de.pytales.zdf.model.Konfiguration
import de.pytales.zdf.model.Medienplan
import de.pytales.zdf.model.MerkmaleDaten
import de.pytales.zdf.model.PortraitAsset
import de.pytales.zdf.model.Sprachregeln

/**
 * Vollständiger, typsicher geladener Spielinhalt aus den 7 JSON-Dateien unter `content/`.
 */
data class GameContent(
    val konfiguration: Konfiguration,
    val herkunft: HerkunftDaten,
    val kapitel: KapitelDaten,
    val merkmale: MerkmaleDaten,
    val ereignisse: EreignisseDaten,
    val sprachregeln: Sprachregeln,
    val medienplan: Medienplan,
) {
    val ereignisById: Map<String, Ereignis> = ereignisse.ereignisse.associateBy { it.id }
    val kapitelByJahr: Map<Int, Kapitel> = kapitel.kapitel.associateBy { it.jahr }
    val herkunftById: Map<String, Herkunft> = herkunft.herkuenfte.associateBy { it.id }
    val erwerbById: Map<String, Erwerbslage> = herkunft.erwerbslagen.associateBy { it.id }
    val portraitById: Map<String, PortraitAsset> = medienplan.portraits.associateBy { it.id }
    val registerReihenfolge: List<String> = merkmale.register.keys.toList()
}
