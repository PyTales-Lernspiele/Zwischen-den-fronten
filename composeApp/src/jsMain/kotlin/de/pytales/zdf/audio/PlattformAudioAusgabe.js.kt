package de.pytales.zdf.audio

actual fun erstellePlattformAudioAusgabe(): AudioAusgabe = JsWebAudioAusgabe()

private class JsWebAudioAusgabe : AudioAusgabe {
    override fun aktualisiere(spur: AudioSpur, lautstaerke: Float) {
        val begrenzt = AudioRegelwerk.begrenzeLautstaerke(lautstaerke)
        if (spur == AudioSpur.STILLE || begrenzt <= 0f) {
            stoppe()
            return
        }
        jsWebAudioSpiele(spur.code, begrenzt.toDouble())
    }

    override fun stoppe() {
        jsWebAudioStoppe()
    }

    override fun freigeben() {
        jsWebAudioFreigeben()
    }
}

private val jsWebAudioSpieleFn: dynamic = js(
    """
    function(spurCode, lautstaerke) {
        try {
            var Ctx = window.AudioContext || window.webkitAudioContext;
            if (!Ctx) return;
            var st = window.__zdfAudio;
            if (!st) {
                var ctx = new Ctx();
                var filter = ctx.createBiquadFilter();
                filter.type = 'lowpass';
                filter.frequency.value = 420;
                var gain = ctx.createGain();
                gain.gain.value = 0.0001;
                filter.connect(gain);
                gain.connect(ctx.destination);
                st = { ctx: ctx, filter: filter, gain: gain, oscs: [], spur: '' };
                window.__zdfAudio = st;
            }
            if (st.ctx.state === 'suspended') {
                st.ctx.resume().catch(function() {});
            }
            var freqMap = {
                start_ruhig: [146.83, 220.00, 349.23],
                heimat_ruhig: [130.81, 196.00, 329.63],
                epilog_ruhig: [110.00, 164.81, 261.63]
            };
            var freqs = freqMap[spurCode];
            if (!freqs) {
                var nowStop = st.ctx.currentTime;
                st.gain.gain.cancelScheduledValues(nowStop);
                st.gain.gain.setTargetAtTime(0.0001, nowStop, 0.08);
                return;
            }
            if (st.spur !== spurCode || st.oscs.length === 0) {
                for (var i = 0; i < st.oscs.length; i++) {
                    try { st.oscs[i].stop(); st.oscs[i].disconnect(); } catch (e) {}
                }
                st.oscs = [];
                for (var j = 0; j < freqs.length; j++) {
                    var osc = st.ctx.createOscillator();
                    var partGain = st.ctx.createGain();
                    osc.type = 'sine';
                    osc.frequency.value = freqs[j];
                    partGain.gain.value = j === 0 ? 0.55 : (j === 1 ? 0.30 : 0.15);
                    osc.connect(partGain);
                    partGain.connect(st.filter);
                    osc.start();
                    st.oscs.push(osc);
                }
                st.spur = spurCode;
            }
            var now = st.ctx.currentTime;
            var ziel = Math.max(0.0001, Math.min(0.12, lautstaerke * 0.25));
            st.gain.gain.cancelScheduledValues(now);
            st.gain.gain.setTargetAtTime(ziel, now, 0.15);
        } catch (e) {}
    }
    """,
)

private val jsWebAudioStoppeFn: dynamic = js(
    """
    function() {
        try {
            var st = window.__zdfAudio;
            if (!st) return;
            var now = st.ctx.currentTime;
            st.gain.gain.cancelScheduledValues(now);
            st.gain.gain.setTargetAtTime(0.0001, now, 0.06);
            for (var i = 0; i < st.oscs.length; i++) {
                try { st.oscs[i].stop(now + 0.25); } catch (e) {}
            }
            st.oscs = [];
            st.spur = '';
        } catch (e) {}
    }
    """,
)

private val jsWebAudioFreigebenFn: dynamic = js(
    """
    function() {
        try {
            var st = window.__zdfAudio;
            if (!st) return;
            for (var i = 0; i < st.oscs.length; i++) {
                try { st.oscs[i].stop(); st.oscs[i].disconnect(); } catch (e) {}
            }
            st.oscs = [];
            st.spur = '';
            if (st.ctx && st.ctx.state !== 'closed') {
                st.ctx.close().catch(function() {});
            }
            window.__zdfAudio = null;
        } catch (e) {}
    }
    """,
)

private fun jsWebAudioSpiele(spurCode: String, lautstaerke: Double) {
    jsWebAudioSpieleFn(spurCode, lautstaerke)
}

private fun jsWebAudioStoppe() {
    jsWebAudioStoppeFn()
}

private fun jsWebAudioFreigeben() {
    jsWebAudioFreigebenFn()
}
