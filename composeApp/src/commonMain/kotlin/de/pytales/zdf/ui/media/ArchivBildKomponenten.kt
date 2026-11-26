package de.pytales.zdf.ui.media

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import org.jetbrains.compose.resources.painterResource

/**
 * Lädt ein Live-Emotions-Portrait (`320×320` WebP) plattformübergreifend mit sauberem Fallback:
 * exakte Stimmung (Stufe 1) → neutrales Basis-Portrait derselben Figur → Archiv-Platzhalter.
 */
@Composable
fun ArchivPortraitBild(
    portraitId: String,
    stimmungsFarbe: Color,
    beschreibung: String,
    modifier: Modifier = Modifier,
    medienRegister: MedienRegister = LocalMedienRegister.current,
    platzhalter: @Composable BoxScope.() -> Unit,
) {
    val aufgeloest = remember(portraitId, medienRegister) {
        BildAufloeser.loesePortrait(portraitId, medienRegister.verfuegbareIds)
    }
    val drawable = remember(aufgeloest.aufgeloesteId, medienRegister) {
        aufgeloest.aufgeloesteId?.let(medienRegister::drawableFuer)
    }

    Box(modifier = modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        if (drawable != null) {
            Image(
                painter = painterResource(drawable),
                contentDescription = beschreibung,
                contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxSize(),
            )
            // Feiner Stimmungs-Akzentbalken am unteren Bildrand verbindet Bild und Live-Stimmung
            Box(
                modifier = Modifier
                    .align(Alignment.BottomCenter)
                    .fillMaxWidth()
                    .height(3.dp)
                    .background(stimmungsFarbe.copy(alpha = 0.88f)),
            )
        } else {
            platzhalter()
        }
    }
}

/**
 * Lädt ein 16:9-Szenenbild (`1280×720` WebP) plattformübergreifend mit automatischer
 * Fallback-Kette: `einzelSzenenbild` (Stufe 2) → `schauplatzBild` (Stufe 1) → Archiv-Platzhalter.
 */
@Composable
fun ArchivSzenenBild(
    bildId: String,
    schauplatzBild: String,
    beschreibung: String,
    modifier: Modifier = Modifier,
    medienRegister: MedienRegister = LocalMedienRegister.current,
    platzhalter: @Composable BoxScope.() -> Unit,
) {
    val aufgeloest = remember(bildId, schauplatzBild, medienRegister) {
        BildAufloeser.loeseSzene(bildId, schauplatzBild, medienRegister.verfuegbareIds)
    }
    val drawable = remember(aufgeloest.aufgeloesteId, medienRegister) {
        aufgeloest.aufgeloesteId?.let(medienRegister::drawableFuer)
    }

    Box(modifier = modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        if (drawable != null) {
            Image(
                painter = painterResource(drawable),
                contentDescription = beschreibung,
                contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxSize(),
            )
        } else {
            platzhalter()
        }
    }
}

/**
 * Lädt ein 16:9-Kapitelbild (`1280×720` WebP, `kapitel_1914`..`kapitel_1919`) plattformübergreifend
 * mit automatischem Fallback auf die bisherige Archiv-Kapiteltafel.
 */
@Composable
fun ArchivKapitelBild(
    kapitelBildId: String,
    beschreibung: String,
    modifier: Modifier = Modifier,
    medienRegister: MedienRegister = LocalMedienRegister.current,
    platzhalter: @Composable BoxScope.() -> Unit,
) {
    val aufgeloest = remember(kapitelBildId, medienRegister) {
        BildAufloeser.loeseKapitel(kapitelBildId, medienRegister.verfuegbareIds)
    }
    val drawable = remember(aufgeloest.aufgeloesteId, medienRegister) {
        aufgeloest.aufgeloesteId?.let(medienRegister::drawableFuer)
    }

    Box(modifier = modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        if (drawable != null) {
            Image(
                painter = painterResource(drawable),
                contentDescription = beschreibung,
                contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxSize(),
            )
        } else {
            platzhalter()
        }
    }
}
