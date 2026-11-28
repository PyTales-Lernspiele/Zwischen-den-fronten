package de.pytales.zdf.audio

actual fun erstellePlattformKlangAusgabe(): KlangAusgabe = JsKlangAusgabe()

/**
 * Web-Klangeffekte (JS-Fallback) über die Web Audio API; Browser lädt und dekodiert die WAVs per URL.
 */
private class JsKlangAusgabe : KlangAusgabe {
    override val brauchtRohdaten: Boolean = false

    override fun lade(klang: Klang, rohdaten: ByteArray?, uri: String?) {
        if (uri != null) jsKlangLadeFn(klang.name, uri)
    }

    override fun spiele(klang: Klang, lautstaerke: Float) {
        jsKlangSpieleFn(klang.name, lautstaerke.toDouble())
    }

    override fun freigeben() = Unit
}

private val jsKlangLadeFn: dynamic = js(
    """
    function(name, uri) {
        try {
            var Ctx = window.AudioContext || window.webkitAudioContext;
            if (!Ctx) return;
            var k = window.__zdfKlang;
            if (!k) {
                k = { ctx: new Ctx(), puffer: {} };
                window.__zdfKlang = k;
                var freischalten = function() {
                    if (k.ctx.state === 'suspended') k.ctx.resume().catch(function() {});
                };
                ['pointerdown', 'keydown', 'touchstart'].forEach(function(ev) {
                    window.addEventListener(ev, freischalten, { capture: true, passive: true });
                });
            }
            fetch(uri)
                .then(function(r) { return r.arrayBuffer(); })
                .then(function(buf) { return new Promise(function(ok, fehler) { k.ctx.decodeAudioData(buf, ok, fehler); }); })
                .then(function(audio) { k.puffer[name] = audio; })
                .catch(function() {});
        } catch (e) {}
    }
    """,
)

private val jsKlangSpieleFn: dynamic = js(
    """
    function(name, lautstaerke) {
        try {
            var k = window.__zdfKlang;
            if (!k || !k.puffer[name] || document.hidden) return;
            if (k.ctx.state === 'suspended') k.ctx.resume().catch(function() {});
            var quelle = k.ctx.createBufferSource();
            quelle.buffer = k.puffer[name];
            var gain = k.ctx.createGain();
            gain.gain.value = Math.max(0, Math.min(1, lautstaerke));
            quelle.connect(gain);
            gain.connect(k.ctx.destination);
            quelle.start();
        } catch (e) {}
    }
    """,
)
