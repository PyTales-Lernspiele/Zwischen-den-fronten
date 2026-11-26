package de.pytales.zdf.ui.media

import androidx.compose.runtime.Stable
import androidx.compose.runtime.staticCompositionLocalOf
import de.pytales.zdf.resources.Res
import de.pytales.zdf.resources.allDrawableResources
import org.jetbrains.compose.resources.DrawableResource

/**
 * Plattformübergreifender Zugriff auf die als Compose-Multiplatform-Ressourcen
 * eingebundenen WebP-Illustrationen (Android, Desktop JVM, Web WasmJS & JS).
 */
@Stable
interface MedienRegister {
    /** Menge aller aktuell im Build vorhandenen Medien-IDs (ohne Dateiendung). */
    val verfuegbareIds: Set<String>

    /** Liefert die Compose-[DrawableResource] zur Medien-ID oder `null`, falls nicht vorhanden. */
    fun drawableFuer(id: String): DrawableResource?
}

/**
 * Produktive Implementierung auf Basis der automatisch aus `content/media/**/*.webp`
 * generierten Compose-Multiplatform-Drawables (`Res.allDrawableResources`).
 */
object ComposeMedienRegister : MedienRegister {
    private val drawables: Map<String, DrawableResource> by lazy {
        Res.allDrawableResources
    }

    override val verfuegbareIds: Set<String>
        get() = drawables.keys

    override fun drawableFuer(id: String): DrawableResource? = drawables[id]
}

/**
 * CompositionLocal für das aktive [MedienRegister] (erlaubt saubere Überschreibung in Tests/Vorschauen).
 */
val LocalMedienRegister = staticCompositionLocalOf<MedienRegister> { ComposeMedienRegister }
