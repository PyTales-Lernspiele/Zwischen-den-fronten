@file:OptIn(ExperimentalWasmJsInterop::class)

package de.pytales.zdf.audio

actual fun erstellePlattformAudioAusgabe(): AudioAusgabe = WasmWebAudioAusgabe()

private class WasmWebAudioAusgabe : AudioAusgabe {
    override fun aktualisiere(spur: AudioSpur, lautstaerke: Float) {
        val begrenzt = AudioRegelwerk.begrenzeLautstaerke(lautstaerke)
        if (spur == AudioSpur.STILLE || begrenzt <= 0f) {
            stoppe()
            return
        }
        wasmWebAudioSpiele(spur.code, begrenzt.toDouble())
    }

    override fun stoppe() {
        wasmWebAudioStoppe()
    }

    override fun freigeben() {
        wasmWebAudioFreigeben()
    }
}

private fun wasmWebAudioSpiele(spurCode: String, lautstaerke: Double): Unit = js(
    """
    (() => {
        try {
            const Ctx = window.AudioContext || window.webkitAudioContext;
            if (!Ctx) return;
            let st = window.__zdfAudio;
            if (!st) {
                const ctx = new Ctx();
                const filter = ctx.createBiquadFilter();
                filter.type = 'lowpass';
                filter.frequency.value = 420;
                const gain = ctx.createGain();
                gain.gain.value = 0.0001;
                filter.connect(gain);
                gain.connect(ctx.destination);
                st = { ctx, filter, gain, oscs: [], spur: '' };
                window.__zdfAudio = st;
            }
            if (st.ctx.state === 'suspended') {
                st.ctx.resume().catch(() => {});
            }
            const freqMap = {
                start_ruhig: [146.83, 220.00, 349.23],
                heimat_ruhig: [130.81, 196.00, 329.63],
                epilog_ruhig: [110.00, 164.81, 261.63]
            };
            const freqs = freqMap[spurCode];
            if (!freqs) {
                const now = st.ctx.currentTime;
                st.gain.gain.cancelScheduledValues(now);
                st.gain.gain.setTargetAtTime(0.0001, now, 0.08);
                return;
            }
            if (st.spur !== spurCode || st.oscs.length === 0) {
                st.oscs.forEach(o => { try { o.stop(); o.disconnect(); } catch (_) {} });
                st.oscs = freqs.map((f, idx) => {
                    const osc = st.ctx.createOscillator();
                    const partGain = st.ctx.createGain();
                    osc.type = 'sine';
                    osc.frequency.value = f;
                    partGain.gain.value = idx === 0 ? 0.55 : (idx === 1 ? 0.30 : 0.15);
                    osc.connect(partGain);
                    partGain.connect(st.filter);
                    osc.start();
                    return osc;
                });
                st.spur = spurCode;
            }
            const now = st.ctx.currentTime;
            const ziel = Math.max(0.0001, Math.min(0.12, lautstaerke * 0.25));
            st.gain.gain.cancelScheduledValues(now);
            st.gain.gain.setTargetAtTime(ziel, now, 0.15);
        } catch (_) {}
    })()
    """,
)

private fun wasmWebAudioStoppe(): Unit = js(
    """
    (() => {
        try {
            const st = window.__zdfAudio;
            if (!st) return;
            const now = st.ctx.currentTime;
            st.gain.gain.cancelScheduledValues(now);
            st.gain.gain.setTargetAtTime(0.0001, now, 0.06);
            st.oscs.forEach(o => { try { o.stop(now + 0.25); } catch (_) {} });
            st.oscs = [];
            st.spur = '';
        } catch (_) {}
    })()
    """,
)

private fun wasmWebAudioFreigeben(): Unit = js(
    """
    (() => {
        try {
            const st = window.__zdfAudio;
            if (!st) return;
            st.oscs.forEach(o => { try { o.stop(); o.disconnect(); } catch (_) {} });
            st.oscs = [];
            st.spur = '';
            if (st.ctx && st.ctx.state !== 'closed') {
                st.ctx.close().catch(() => {});
            }
            window.__zdfAudio = null;
        } catch (_) {}
    })()
    """,
)
