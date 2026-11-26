package de.pytales.zdf.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sin

/**
 * Feine Federzeichnungs-Symbole im Stil A (Sepia-Tinte / Archiv-Skizzenbuch).
 * Verzichtet bewusst auf schwere Icon-Fonts, damit APK- und Web-Bundle klein bleiben
 * und die Linienführung exakt zu den Tusche- und Aquarell-Illustrationen passt.
 */

@Composable
fun TonIcon(
    aktiv: Boolean,
    gesperrt: Boolean,
    farbe: Color,
    modifier: Modifier = Modifier,
    groesse: Dp = 20.dp,
) {
    Canvas(modifier = modifier.size(groesse)) {
        val w = size.width
        val h = size.height
        val strich = (w * 0.085f).coerceAtLeast(1.4f)
        val stroke = Stroke(width = strich, cap = StrokeCap.Round, join = StrokeJoin.Round)

        // Lautsprecher-Korpus
        val lautsprecher = Path().apply {
            moveTo(w * 0.16f, h * 0.39f)
            lineTo(w * 0.33f, h * 0.39f)
            lineTo(w * 0.54f, h * 0.22f)
            lineTo(w * 0.54f, h * 0.78f)
            lineTo(w * 0.33f, h * 0.61f)
            lineTo(w * 0.16f, h * 0.61f)
            close()
        }
        drawPath(path = lautsprecher, color = farbe, style = stroke)

        when {
            gesperrt -> {
                // Ruhiger kurzer Querstrich (respektvolle Stille an Front/Etappe)
                drawLine(
                    color = farbe.copy(alpha = 0.78f),
                    start = Offset(w * 0.68f, h * 0.50f),
                    end = Offset(w * 0.88f, h * 0.50f),
                    strokeWidth = strich,
                    cap = StrokeCap.Round,
                )
            }

            aktiv -> {
                // Zwei leise Schallwellen
                drawArc(
                    color = farbe,
                    startAngle = -42f,
                    sweepAngle = 84f,
                    useCenter = false,
                    topLeft = Offset(w * 0.48f, h * 0.32f),
                    size = Size(w * 0.26f, h * 0.36f),
                    style = stroke,
                )
                drawArc(
                    color = farbe.copy(alpha = 0.75f),
                    startAngle = -46f,
                    sweepAngle = 92f,
                    useCenter = false,
                    topLeft = Offset(w * 0.52f, h * 0.18f),
                    size = Size(w * 0.40f, h * 0.64f),
                    style = stroke,
                )
            }

            else -> {
                // Schlichter diagonaler Stumm-Strich
                drawLine(
                    color = farbe,
                    start = Offset(w * 0.66f, h * 0.36f),
                    end = Offset(w * 0.88f, h * 0.64f),
                    strokeWidth = strich,
                    cap = StrokeCap.Round,
                )
                drawLine(
                    color = farbe,
                    start = Offset(w * 0.88f, h * 0.36f),
                    end = Offset(w * 0.66f, h * 0.64f),
                    strokeWidth = strich,
                    cap = StrokeCap.Round,
                )
            }
        }
    }
}

@Composable
fun EinstellungenIcon(
    farbe: Color,
    modifier: Modifier = Modifier,
    groesse: Dp = 20.dp,
) {
    Canvas(modifier = modifier.size(groesse)) {
        val cx = size.width / 2f
        val cy = size.height / 2f
        val rAussen = size.minDimension * 0.34f
        val rInnen = size.minDimension * 0.15f
        val zahnLaenge = size.minDimension * 0.11f
        val strich = (size.minDimension * 0.085f).coerceAtLeast(1.4f)
        val stroke = Stroke(width = strich, cap = StrokeCap.Round, join = StrokeJoin.Round)

        drawCircle(color = farbe, radius = rAussen, center = Offset(cx, cy), style = stroke)
        drawCircle(color = farbe, radius = rInnen, center = Offset(cx, cy), style = stroke)

        for (i in 0 until 8) {
            val winkel = (i * 45.0) * PI / 180.0
            val cosA = cos(winkel).toFloat()
            val sinA = sin(winkel).toFloat()
            drawLine(
                color = farbe,
                start = Offset(cx + cosA * rAussen, cy + sinA * rAussen),
                end = Offset(cx + cosA * (rAussen + zahnLaenge), cy + sinA * (rAussen + zahnLaenge)),
                strokeWidth = strich,
                cap = StrokeCap.Round,
            )
        }
    }
}

@Composable
fun ChevronIcon(
    nachOben: Boolean,
    farbe: Color,
    modifier: Modifier = Modifier,
    groesse: Dp = 18.dp,
) {
    Canvas(modifier = modifier.size(groesse)) {
        val w = size.width
        val h = size.height
        val strich = (w * 0.10f).coerceAtLeast(1.5f)
        val pfad = Path().apply {
            if (nachOben) {
                moveTo(w * 0.22f, h * 0.62f)
                lineTo(w * 0.50f, h * 0.34f)
                lineTo(w * 0.78f, h * 0.62f)
            } else {
                moveTo(w * 0.22f, h * 0.38f)
                lineTo(w * 0.50f, h * 0.66f)
                lineTo(w * 0.78f, h * 0.38f)
            }
        }
        drawPath(
            path = pfad,
            color = farbe,
            style = Stroke(width = strich, cap = StrokeCap.Round, join = StrokeJoin.Round),
        )
    }
}

@Composable
fun SchliessenIcon(
    farbe: Color,
    modifier: Modifier = Modifier,
    groesse: Dp = 18.dp,
) {
    Canvas(modifier = modifier.size(groesse)) {
        val w = size.width
        val h = size.height
        val strich = (w * 0.095f).coerceAtLeast(1.5f)
        drawLine(
            color = farbe,
            start = Offset(w * 0.24f, h * 0.24f),
            end = Offset(w * 0.76f, h * 0.76f),
            strokeWidth = strich,
            cap = StrokeCap.Round,
        )
        drawLine(
            color = farbe,
            start = Offset(w * 0.76f, h * 0.24f),
            end = Offset(w * 0.24f, h * 0.76f),
            strokeWidth = strich,
            cap = StrokeCap.Round,
        )
    }
}

@Composable
fun HakenIcon(
    farbe: Color,
    modifier: Modifier = Modifier,
    groesse: Dp = 16.dp,
) {
    Canvas(modifier = modifier.size(groesse)) {
        val w = size.width
        val h = size.height
        val strich = (w * 0.12f).coerceAtLeast(1.6f)
        val pfad = Path().apply {
            moveTo(w * 0.18f, h * 0.52f)
            lineTo(w * 0.42f, h * 0.76f)
            lineTo(w * 0.84f, h * 0.26f)
        }
        drawPath(
            path = pfad,
            color = farbe,
            style = Stroke(width = strich, cap = StrokeCap.Round, join = StrokeJoin.Round),
        )
    }
}

@Composable
fun QuelleBuchIcon(
    farbe: Color,
    modifier: Modifier = Modifier,
    groesse: Dp = 16.dp,
) {
    Canvas(modifier = modifier.size(groesse)) {
        val w = size.width
        val h = size.height
        val strich = (w * 0.095f).coerceAtLeast(1.3f)
        val stroke = Stroke(width = strich, cap = StrokeCap.Round, join = StrokeJoin.Round)
        drawRoundRect(
            color = farbe,
            topLeft = Offset(w * 0.20f, h * 0.14f),
            size = Size(w * 0.60f, h * 0.72f),
            cornerRadius = CornerRadius(w * 0.08f, w * 0.08f),
            style = stroke,
        )
        drawLine(
            color = farbe,
            start = Offset(w * 0.36f, h * 0.14f),
            end = Offset(w * 0.36f, h * 0.86f),
            strokeWidth = strich,
            cap = StrokeCap.Round,
        )
        drawLine(
            color = farbe,
            start = Offset(w * 0.47f, h * 0.38f),
            end = Offset(w * 0.68f, h * 0.38f),
            strokeWidth = strich,
            cap = StrokeCap.Round,
        )
        drawLine(
            color = farbe,
            start = Offset(w * 0.47f, h * 0.56f),
            end = Offset(w * 0.64f, h * 0.56f),
            strokeWidth = strich,
            cap = StrokeCap.Round,
        )
    }
}
