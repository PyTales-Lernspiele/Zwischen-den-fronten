package de.pytales.zdf.ui.theme

import androidx.compose.animation.ContentTransform
import androidx.compose.animation.EnterTransition
import androidx.compose.animation.ExitTransition
import androidx.compose.animation.core.AnimationSpec
import androidx.compose.animation.core.snap
import androidx.compose.animation.core.tween
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.animation.togetherWith
import androidx.compose.runtime.Immutable
import androidx.compose.ui.graphics.Color

/**
 * Parameter-Satz für ruhige, respektvolle Übergänge im Archivpapier-Stil.
 *
 * - Normalmodus (`reduzierteAnimationen = false`): sanfte, kurze Überblendungen ohne Unruhe,
 *   ohne Hüpfen oder hektisches Einfliegen.
 * - Reduzierter Modus (`reduzierteAnimationen = true`): sofortige Wechsel (`0 ms`),
 *   kein weiches Nachscrollen und keine Aufklapp-Bewegung (ideal für Beamer,
 *   Bewegungsempfindlichkeit und Bildschirmleser).
 */
@Immutable
data class UebergangsProfil(
    val reduzierteAnimationen: Boolean,
    val phasenDauerMs: Int,
    val aufklappDauerMs: Int,
    val farbDauerMs: Int,
    val sanftScrollen: Boolean,
    val vertikalAufklappen: Boolean,
)

/**
 * Zentrale, vollständig testbare Übergangs- und Animationssteuerung für AP 6.
 */
object ArchivUebergaenge {

    val RUHIG = UebergangsProfil(
        reduzierteAnimationen = false,
        phasenDauerMs = 220,
        aufklappDauerMs = 180,
        farbDauerMs = 220,
        sanftScrollen = true,
        vertikalAufklappen = true,
    )

    val REDUZIERT = UebergangsProfil(
        reduzierteAnimationen = true,
        phasenDauerMs = 0,
        aufklappDauerMs = 0,
        farbDauerMs = 0,
        sanftScrollen = false,
        vertikalAufklappen = false,
    )

    fun profilFuer(reduzierteAnimationen: Boolean): UebergangsProfil =
        if (reduzierteAnimationen) REDUZIERT else RUHIG

    /**
     * Ruhige Überblendung für Karten- und Phasenwechsel (oder sofortiger Wechsel bei
     * reduzierten Animationen).
     */
    fun phasenTransitionSpec(reduzierteAnimationen: Boolean): ContentTransform {
        val profil = profilFuer(reduzierteAnimationen)
        if (profil.phasenDauerMs <= 0) {
            return EnterTransition.None togetherWith ExitTransition.None
        }
        val ausblendDauer = (profil.phasenDauerMs * 2) / 3
        return fadeIn(animationSpec = tween(durationMillis = profil.phasenDauerMs)) togetherWith
            fadeOut(animationSpec = tween(durationMillis = ausblendDauer))
    }

    /**
     * Ruhiges Einblenden für aufklappbare Kästen (Quellen-Einordnung, Grundsätze,
     * Erklärkarten, Ausgangskarte, Entscheidungsprotokoll).
     */
    fun aufklappEnter(reduzierteAnimationen: Boolean): EnterTransition {
        val profil = profilFuer(reduzierteAnimationen)
        if (profil.aufklappDauerMs <= 0) {
            return EnterTransition.None
        }
        val fade = fadeIn(animationSpec = tween(durationMillis = profil.aufklappDauerMs))
        return if (profil.vertikalAufklappen) {
            fade + expandVertically(animationSpec = tween(durationMillis = profil.aufklappDauerMs))
        } else {
            fade
        }
    }

    /**
     * Ruhiges Ausblenden für aufklappbare Kästen.
     */
    fun aufklappExit(reduzierteAnimationen: Boolean): ExitTransition {
        val profil = profilFuer(reduzierteAnimationen)
        if (profil.aufklappDauerMs <= 0) {
            return ExitTransition.None
        }
        val ausblendDauer = (profil.aufklappDauerMs * 5) / 6
        val fade = fadeOut(animationSpec = tween(durationMillis = ausblendDauer))
        return if (profil.vertikalAufklappen) {
            fade + shrinkVertically(animationSpec = tween(durationMillis = ausblendDauer))
        } else {
            fade
        }
    }

    /**
     * Sanfte Farbangleichung für 5-Segment-Balken und Live-Emotions-Kachel
     * (bzw. sofortiges `snap()` bei reduzierten Animationen).
     */
    fun farbSpec(reduzierteAnimationen: Boolean): AnimationSpec<Color> {
        val profil = profilFuer(reduzierteAnimationen)
        return if (profil.farbDauerMs <= 0) {
            snap()
        } else {
            tween(durationMillis = profil.farbDauerMs)
        }
    }
}
