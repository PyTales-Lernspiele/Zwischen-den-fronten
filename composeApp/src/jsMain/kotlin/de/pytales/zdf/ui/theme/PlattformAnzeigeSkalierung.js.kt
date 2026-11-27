package de.pytales.zdf.ui.theme

import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect

@Composable
actual fun PlattformAnzeigeSkalierung(faktor: Float) {
    SideEffect { skaliereBarrierefreiheitsEbene(faktor.toDouble()) }
}

// Shadow-DOM von ComposeViewport: <layerRoot> mit <canvas>, Interop-Ebene und zuletzt der Barrierefreiheits-Ebene
private fun skaliereBarrierefreiheitsEbene(faktor: Double) {
    js("""{
    var root = document.body ? document.body.shadowRoot : null;
    var ebene = root ? root.firstElementChild : null;
    var a11y = ebene && ebene.children.length >= 3 ? ebene.lastElementChild : null;
    if (a11y && a11y.tagName === "DIV") {
        if (faktor > 1.0001) {
            a11y.style.transformOrigin = "0 0";
            a11y.style.transform = "scale(" + faktor + ")";
        } else {
            a11y.style.transform = "";
        }
    }
}""")
}
