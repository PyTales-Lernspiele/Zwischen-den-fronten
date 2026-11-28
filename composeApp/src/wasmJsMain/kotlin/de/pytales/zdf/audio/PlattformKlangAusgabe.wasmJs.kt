@file:OptIn(ExperimentalWasmJsInterop::class)

package de.pytales.zdf.audio

actual fun erstellePlattformKlangAusgabe(): KlangAusgabe = WasmKlangAusgabe()

/**
 * Web-Klangeffekte (WasmJS) über die Web Audio API: Der Browser lädt und dekodiert die WAV-Dateien
 * selbst per URL. Der AudioContext wird beim ersten Tippen/Tastendruck freigeschaltet.
 */
private class WasmKlangAusgabe : KlangAusgabe {
    override val brauchtRohdaten: Boolean = false

    override fun lade(klang: Klang, rohdaten: ByteArray?, uri: String?) {
        if (uri != null) wasmKlangLade(klang.name, uri)
    }

    override fun spiele(klang: Klang, lautstaerke: Float) {
        wasmKlangSpiele(klang.name, lautstaerke.toDouble())
    }

    override fun freigeben() = Unit
}

private fun wasmKlangLade(name: String, uri: String): Unit = js(
    """
    (() => {
        try {
            const Ctx = window.AudioContext || window.webkitAudioContext;
            if (!Ctx) return;
            let k = window.__zdfKlang;
            if (!k) {
                k = { ctx: new Ctx(), puffer: {} };
                window.__zdfKlang = k;
                const freischalten = () => {
                    if (k.ctx.state === 'suspended') k.ctx.resume().catch(() => {});
                };
                ['pointerdown', 'keydown', 'touchstart'].forEach(ev =>
                    window.addEventListener(ev, freischalten, { capture: true, passive: true }));
            }
            fetch(uri)
                .then(r => r.arrayBuffer())
                .then(buf => new Promise((ok, fehler) => k.ctx.decodeAudioData(buf, ok, fehler)))
                .then(audio => { k.puffer[name] = audio; })
                .catch(() => {});
        } catch (_) {}
    })()
    """,
)

private fun wasmKlangSpiele(name: String, lautstaerke: Double): Unit = js(
    """
    (() => {
        try {
            const k = window.__zdfKlang;
            if (!k || !k.puffer[name] || document.hidden) return;
            if (k.ctx.state === 'suspended') k.ctx.resume().catch(() => {});
            const quelle = k.ctx.createBufferSource();
            quelle.buffer = k.puffer[name];
            const gain = k.ctx.createGain();
            gain.gain.value = Math.max(0, Math.min(1, lautstaerke));
            quelle.connect(gain);
            gain.connect(k.ctx.destination);
            quelle.start();
        } catch (_) {}
    })()
    """,
)
