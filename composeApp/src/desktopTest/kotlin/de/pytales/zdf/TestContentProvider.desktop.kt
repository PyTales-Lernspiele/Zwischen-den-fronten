package de.pytales.zdf

actual fun readTestContentJson(fileName: String): String {
    val stream = Thread.currentThread().contextClassLoader?.getResourceAsStream("content/$fileName")
        ?: error("Test-Ressource 'content/$fileName' wurde nicht gefunden (Gradle syncContentToTestResources prüfen).")
    return stream.bufferedReader(Charsets.UTF_8).use { it.readText() }
}
