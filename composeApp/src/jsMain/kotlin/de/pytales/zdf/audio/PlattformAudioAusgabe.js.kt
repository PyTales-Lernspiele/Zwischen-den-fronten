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

    override fun spieleEffekt(effekt: SoundEffekt, lautstaerke: Float) {
        val begrenzt = AudioRegelwerk.begrenzeLautstaerke(lautstaerke)
        if (begrenzt <= 0f) return
        jsWebAudioEffekt(effekt.code, begrenzt.toDouble())
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
                filter.frequency.value = 820;
                var musicGain = ctx.createGain();
                musicGain.gain.value = 0.0001;
                filter.connect(musicGain);
                musicGain.connect(ctx.destination);
                var sfxGain = ctx.createGain();
                sfxGain.gain.value = 1.0;
                sfxGain.connect(ctx.destination);
                st = {
                    ctx: ctx,
                    filter: filter,
                    musicGain: musicGain,
                    sfxGain: sfxGain,
                    nodes: [],
                    timer: null,
                    spur: '',
                    cycleStart: 0,
                    cursor: 0,
                    noiseBuf: null
                };
                window.__zdfAudio = st;
            }
            if (st.ctx.state === 'suspended') {
                st.ctx.resume().catch(function() {});
            }
            var scores = {
                start_ruhig: {
                    dur: 48.0,
                    piano: [
                        [0.00, 4.4, 50, 0.70], [0.95, 3.8, 57, 0.60], [2.35, 3.9, 65, 0.62],
                        [4.15, 3.5, 64, 0.54], [5.90, 4.6, 62, 0.66], [6.05, 4.4, 50, 0.45],
                        [13.60, 4.2, 46, 0.64], [14.55, 3.8, 58, 0.56], [16.10, 3.6, 62, 0.60],
                        [17.85, 3.8, 69, 0.48], [19.70, 4.5, 67, 0.62], [19.90, 4.3, 55, 0.50],
                        [27.40, 4.0, 55, 0.60], [28.80, 3.6, 58, 0.54], [30.40, 3.8, 62, 0.58],
                        [32.20, 4.0, 57, 0.56], [33.40, 3.4, 64, 0.52], [34.95, 2.8, 61, 0.46],
                        [39.20, 4.8, 50, 0.66], [40.30, 4.2, 57, 0.52], [41.80, 3.4, 65, 0.42],
                        [42.20, 3.0, 62, 0.48]
                    ],
                    cello: [
                        [0.40, 9.6, 50, 0.36], [14.00, 9.8, 46, 0.34],
                        [27.80, 5.2, 43, 0.32], [33.00, 5.4, 45, 0.30], [39.40, 5.6, 50, 0.28]
                    ]
                },
                heimat_ruhig: {
                    dur: 52.0,
                    piano: [
                        [0.00, 4.4, 45, 0.64], [1.10, 3.9, 64, 0.56], [3.10, 3.8, 60, 0.58],
                        [5.25, 3.4, 59, 0.50], [6.95, 3.6, 57, 0.56],
                        [14.80, 4.2, 53, 0.58], [15.95, 3.8, 57, 0.52], [17.70, 3.7, 65, 0.54],
                        [19.65, 3.5, 64, 0.48], [21.25, 3.5, 62, 0.54],
                        [29.00, 4.2, 52, 0.56], [30.30, 3.8, 59, 0.50], [32.10, 3.6, 67, 0.44],
                        [34.00, 3.5, 64, 0.50], [35.85, 3.3, 62, 0.46],
                        [43.00, 3.6, 62, 0.48], [44.55, 3.5, 60, 0.46], [46.00, 2.8, 57, 0.50],
                        [46.15, 2.6, 52, 0.36]
                    ],
                    cello: [
                        [0.60, 9.2, 45, 0.32], [15.20, 8.8, 48, 0.28], [29.40, 8.6, 43, 0.30]
                    ]
                },
                epilog_ruhig: {
                    dur: 44.0,
                    piano: [
                        [0.00, 4.2, 57, 0.52], [2.05, 3.8, 59, 0.44], [4.15, 3.8, 60, 0.48],
                        [6.35, 3.4, 64, 0.40],
                        [14.40, 4.4, 53, 0.48], [16.10, 3.9, 60, 0.44], [18.50, 3.6, 67, 0.36],
                        [20.80, 3.6, 64, 0.42],
                        [29.20, 4.0, 62, 0.46], [31.50, 3.8, 60, 0.42], [33.85, 3.6, 59, 0.38],
                        [35.80, 3.8, 57, 0.44]
                    ],
                    cello: [
                        [14.80, 8.8, 45, 0.24], [30.40, 8.2, 45, 0.22]
                    ]
                }
            };
            var score = scores[spurCode];
            if (!score) {
                var nowStop = st.ctx.currentTime;
                st.musicGain.gain.cancelScheduledValues(nowStop);
                st.musicGain.gain.setTargetAtTime(0.0001, nowStop, 0.05);
                return;
            }
            var midiHz = function(m) { return 440.0 * Math.pow(2.0, (m - 69) / 12.0); };
            var playPiano = function(when, dur, midi, vel) {
                var c = st.ctx;
                var freq = midiHz(midi);
                var lp = c.createBiquadFilter();
                lp.type = 'lowpass';
                lp.frequency.setValueAtTime(Math.min(1100, freq * 2.8), when);
                lp.frequency.exponentialRampToValueAtTime(Math.max(220, freq * 1.15), when + Math.min(dur, 1.4));
                var g = c.createGain();
                g.gain.setValueAtTime(0.0001, when);
                g.gain.linearRampToValueAtTime(vel * 0.24, when + 0.020);
                g.gain.exponentialRampToValueAtTime(Math.max(0.0001, vel * 0.06), when + dur * 0.45);
                g.gain.exponentialRampToValueAtTime(0.0001, when + dur);
                var o1 = c.createOscillator();
                var o2 = c.createOscillator();
                o1.type = 'triangle';
                o2.type = 'sine';
                o1.frequency.setValueAtTime(freq, when);
                o2.frequency.setValueAtTime(freq + 0.32, when);
                var g2 = c.createGain();
                g2.gain.value = 0.35;
                o1.connect(lp);
                o2.connect(g2);
                g2.connect(lp);
                lp.connect(g);
                g.connect(st.filter);
                o1.start(when);
                o2.start(when);
                o1.stop(when + dur + 0.05);
                o2.stop(when + dur + 0.05);
                st.nodes.push(o1, o2);
            };
            var playCello = function(when, dur, midi, vel) {
                var c = st.ctx;
                var freq = midiHz(midi);
                var lp = c.createBiquadFilter();
                lp.type = 'lowpass';
                lp.frequency.setValueAtTime(340, when);
                var g = c.createGain();
                g.gain.setValueAtTime(0.0001, when);
                g.gain.linearRampToValueAtTime(vel * 0.16, when + dur * 0.46);
                g.gain.linearRampToValueAtTime(0.0001, when + dur);
                var osc = c.createOscillator();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(freq, when);
                var lfo = c.createOscillator();
                var lfoGain = c.createGain();
                lfo.frequency.setValueAtTime(4.1, when);
                lfoGain.gain.setValueAtTime(freq * 0.0018, when);
                lfo.connect(lfoGain);
                lfoGain.connect(osc.frequency);
                osc.connect(lp);
                lp.connect(g);
                g.connect(st.filter);
                osc.start(when);
                lfo.start(when);
                osc.stop(when + dur + 0.05);
                lfo.stop(when + dur + 0.05);
                st.nodes.push(osc, lfo);
            };

            if (st.spur !== spurCode || !st.timer) {
                if (st.timer) { clearInterval(st.timer); st.timer = null; }
                for (var i = 0; i < st.nodes.length; i++) {
                    try { st.nodes[i].stop(); st.nodes[i].disconnect(); } catch (e) {}
                }
                st.nodes = [];
                st.spur = spurCode;
                st.cycleStart = st.ctx.currentTime + 0.04;
                st.cursor = -0.01;
                var tick = function() {
                    try {
                        var nowT = st.ctx.currentTime;
                        var elapsed = nowT - st.cycleStart;
                        if (elapsed >= score.dur) {
                            var wraps = Math.floor(elapsed / score.dur);
                            st.cycleStart += wraps * score.dur;
                            st.cursor -= wraps * score.dur;
                        }
                        var fromT = st.cursor;
                        var toT = (nowT - st.cycleStart) + 0.35;
                        for (var p = 0; p < score.piano.length; p++) {
                            var n = score.piano[p];
                            if (n[0] > fromT && n[0] <= toT) {
                                playPiano(st.cycleStart + n[0], n[1], n[2], n[3]);
                            }
                        }
                        for (var c = 0; c < score.cello.length; c++) {
                            var b = score.cello[c];
                            if (b[0] > fromT && b[0] <= toT) {
                                playCello(st.cycleStart + b[0], b[1], b[2], b[3]);
                            }
                        }
                        st.cursor = toT;
                        if (st.nodes.length > 48) {
                            st.nodes = st.nodes.slice(-24);
                        }
                    } catch (e) {}
                };
                tick();
                st.timer = setInterval(tick, 120);
            }
            var now = st.ctx.currentTime;
            var ziel = Math.max(0.0001, Math.min(0.45, lautstaerke * 1.15));
            st.musicGain.gain.cancelScheduledValues(now);
            st.musicGain.gain.setTargetAtTime(ziel, now, 0.14);
        } catch (e) {}
    }
    """,
)

private val jsWebAudioEffektFn: dynamic = js(
    """
    function(effektCode, lautstaerke) {
        try {
            var Ctx = window.AudioContext || window.webkitAudioContext;
            if (!Ctx) return;
            var st = window.__zdfAudio;
            if (!st) {
                var ctx = new Ctx();
                var filter = ctx.createBiquadFilter();
                filter.type = 'lowpass';
                filter.frequency.value = 820;
                var musicGain = ctx.createGain();
                musicGain.gain.value = 0.0001;
                filter.connect(musicGain);
                musicGain.connect(ctx.destination);
                var sfxGain = ctx.createGain();
                sfxGain.gain.value = 1.0;
                sfxGain.connect(ctx.destination);
                st = {
                    ctx: ctx,
                    filter: filter,
                    musicGain: musicGain,
                    sfxGain: sfxGain,
                    nodes: [],
                    timer: null,
                    spur: '',
                    cycleStart: 0,
                    cursor: 0,
                    noiseBuf: null
                };
                window.__zdfAudio = st;
            }
            if (st.ctx.state === 'suspended') {
                st.ctx.resume().catch(function() {});
            }
            var c = st.ctx;
            var now = c.currentTime + 0.004;
            var pegel = Math.max(0.0001, Math.min(0.35, lautstaerke));
            if (!st.noiseBuf) {
                var len = Math.floor(c.sampleRate * 0.25);
                var buf = c.createBuffer(1, len, c.sampleRate);
                var data = buf.getChannelData(0);
                for (var i = 0; i < len; i++) {
                    data[i] = Math.random() * 2.0 - 1.0;
                }
                st.noiseBuf = buf;
            }
            if (effektCode === 'klick_sanft') {
                var osc = c.createOscillator();
                var g = c.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(280, now);
                osc.frequency.exponentialRampToValueAtTime(160, now + 0.032);
                g.gain.setValueAtTime(0.0001, now);
                g.gain.linearRampToValueAtTime(pegel * 0.28, now + 0.003);
                g.gain.exponentialRampToValueAtTime(0.0001, now + 0.036);
                osc.connect(g);
                g.connect(st.sfxGain);
                osc.start(now);
                osc.stop(now + 0.042);
            } else if (effektCode === 'entscheidung') {
                var src = c.createBufferSource();
                src.buffer = st.noiseBuf;
                var bp = c.createBiquadFilter();
                bp.type = 'bandpass';
                bp.frequency.setValueAtTime(1050, now);
                bp.Q.setValueAtTime(1.3, now);
                var ng = c.createGain();
                ng.gain.setValueAtTime(0.0001, now);
                ng.gain.linearRampToValueAtTime(pegel * 0.24, now + 0.045);
                ng.gain.exponentialRampToValueAtTime(0.0001, now + 0.14);
                src.connect(bp);
                bp.connect(ng);
                ng.connect(st.sfxGain);
                src.start(now);
                src.stop(now + 0.15);
            } else if (effektCode === 'kapitelwechsel') {
                var lp = c.createBiquadFilter();
                lp.type = 'lowpass';
                lp.frequency.setValueAtTime(520, now);
                var kg = c.createGain();
                kg.gain.setValueAtTime(0.0001, now);
                kg.gain.linearRampToValueAtTime(pegel * 0.22, now + 0.03);
                kg.gain.exponentialRampToValueAtTime(0.0001, now + 0.56);
                var k1 = c.createOscillator();
                var k2 = c.createOscillator();
                k1.type = 'triangle';
                k2.type = 'sine';
                k1.frequency.setValueAtTime(146.83, now);
                k2.frequency.setValueAtTime(220.0, now);
                k1.connect(lp);
                k2.connect(lp);
                lp.connect(kg);
                kg.connect(st.sfxGain);
                k1.start(now);
                k2.start(now);
                k1.stop(now + 0.58);
                k2.stop(now + 0.58);
            } else if (effektCode === 'einschnitt') {
                var elp = c.createBiquadFilter();
                elp.type = 'lowpass';
                elp.frequency.setValueAtTime(480, now);
                var eg = c.createGain();
                eg.gain.setValueAtTime(0.0001, now);
                eg.gain.linearRampToValueAtTime(pegel * 0.18, now + 0.025);
                eg.gain.exponentialRampToValueAtTime(0.0001, now + 0.34);
                var eo = c.createOscillator();
                eo.type = 'sine';
                eo.frequency.setValueAtTime(220.0, now);
                eo.connect(elp);
                elp.connect(eg);
                eg.connect(st.sfxGain);
                eo.start(now);
                eo.stop(now + 0.36);
            }
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
            if (st.timer) {
                clearInterval(st.timer);
                st.timer = null;
            }
            var now = st.ctx.currentTime;
            st.musicGain.gain.cancelScheduledValues(now);
            st.musicGain.gain.setTargetAtTime(0.0001, now, 0.04);
            for (var i = 0; i < st.nodes.length; i++) {
                try { st.nodes[i].stop(now + 0.16); } catch (e) {}
            }
            st.nodes = [];
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
            if (st.timer) {
                clearInterval(st.timer);
                st.timer = null;
            }
            for (var i = 0; i < st.nodes.length; i++) {
                try { st.nodes[i].stop(); st.nodes[i].disconnect(); } catch (e) {}
            }
            st.nodes = [];
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

private fun jsWebAudioEffekt(effektCode: String, lautstaerke: Double) {
    jsWebAudioEffektFn(effektCode, lautstaerke)
}

private fun jsWebAudioStoppe() {
    jsWebAudioStoppeFn()
}

private fun jsWebAudioFreigeben() {
    jsWebAudioFreigebenFn()
}
