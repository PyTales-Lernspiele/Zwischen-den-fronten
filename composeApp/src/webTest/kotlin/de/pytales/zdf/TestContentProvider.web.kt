package de.pytales.zdf

actual fun readTestContentJson(fileName: String): String {
    error("Direktes Dateiladen für '$fileName' wird in Web-Unit-Tests ohne Browser-Harness nicht unterstützt.")
}

actual fun readTestMediaBytes(relativePath: String): ByteArray? = null
