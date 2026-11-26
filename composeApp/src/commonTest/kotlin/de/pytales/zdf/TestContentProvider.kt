package de.pytales.zdf

import de.pytales.zdf.content.ContentLoader
import de.pytales.zdf.content.GameContent

expect fun readTestContentJson(fileName: String): String

fun loadTestGameContent(): GameContent =
    ContentLoader.parseFromProvider(::readTestContentJson)
