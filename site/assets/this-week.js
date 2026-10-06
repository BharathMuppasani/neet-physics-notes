/* =====================================================================
   This week's page — heat vs temperature, temperature scales, gas
   thermometer, expansion lab, bimetallic strip, water near 4 °C and the
   capillary-rise virtual lab, first law on a P–V diagram and the Carnot
   limit for engines, plus planner ticks and problem self-marking.
   Each sim initialises only if its host figure exists.
   ===================================================================== */
(function () {
  'use strict';
  if (typeof Sim === 'undefined') return;

  const G = 9.8;
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const fig = id => document.getElementById(id);
  const fx = (x, dp) => (+x).toFixed(dp);

  /* cold blue → warm amber → hot red, for a temperature t in [lo, hi] */
  const RAMP = [[58, 140, 203], [232, 163, 61], [214, 96, 74]];
  function heatColor(t, lo, hi, alpha) {
    const f = clamp((t - lo) / (hi - lo), 0, 1) * 2, i = Math.min(1, Math.floor(f)), u = f - i;
    const c = RAMP[i].map((v, k) => Math.round(v + (RAMP[i + 1][k] - v) * u));
    return `rgba(${c[0]}, ${c[1]}, ${c[2]}, ${alpha === undefined ? 1 : alpha})`;
  }
  function setInput(input, v) {
    input.value = v;
    input.dispatchEvent(new Event('input', { bubbles: true }));
  }
  function hatch(ctx, x, y, w, h) {
    const C = Sim.C;
    ctx.save();
    ctx.fillStyle = C.surface2; ctx.fillRect(x, y, w, h);
    ctx.beginPath(); ctx.rect(x, y, w, h); ctx.clip();
    ctx.strokeStyle = C.line2; ctx.lineWidth = 1;
    for (let i = -h; i < w + h; i += 8) { ctx.beginPath(); ctx.moveTo(x + i, y + h); ctx.lineTo(x + i + h, y); ctx.stroke(); }
    ctx.restore();
    ctx.save(); ctx.strokeStyle = C.ink2; ctx.lineWidth = 1.5; ctx.strokeRect(x, y, w, h); ctx.restore();
  }
  function niceStep(span, n) {
    const raw = span / n, e = Math.pow(10, Math.floor(Math.log10(raw))), m = raw / e;
    return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10) * e;
  }

  /* =================================================================
     1. Heat flow between two blocks of water
     ================================================================= */
  function initHeatFlow() {
    const root = fig('sim-heatflow'); if (!root) return;
    const host = root.querySelector('.sim-stage');
    const btn = root.querySelector('[data-act="contact"]');
    let P = null, contact = false, elapsed = 0;
    const seed = n => Array.from({ length: n }, (_, i) => ({ x: (0.5 + i * 0.7548777) % 1, y: (0.5 + i * 0.5698403) % 1, p: i * 1.7 })); // R2 low-discrepancy scatter
    const dotsA = seed(60), dotsB = seed(60);
    const LAMBDA = 0.9;

    function temps() {
      const TA = P['hf-ta'], TB = P['hf-tb'], mA = P['hf-ma'], mB = P['hf-mb'];
      const Tf = (mA * TA + mB * TB) / (mA + mB);
      const k = contact ? Math.exp(-LAMBDA * elapsed) : 1;
      const tA = Tf + (TA - Tf) * k, tB = Tf + (TB - Tf) * k;
      return { TA, TB, mA, mB, Tf, tA, tB, Q: mA * 4186 * (TA - tA) };
    }

    function block(ctx, x, y, side, T, dots, t, label, m) {
      const C = Sim.C;
      ctx.save();
      ctx.fillStyle = heatColor(T, 0, 200, 0.9);
      Sim.rrect(ctx, x, y - side, side, side, 8); ctx.fill();
      ctx.strokeStyle = 'rgba(27,34,51,.35)'; ctx.lineWidth = 1.5; ctx.stroke();
      ctx.beginPath(); ctx.rect(x + 3, y - side + 3, side - 6, side - 6); ctx.clip();
      const n = clamp(Math.round(6 + 44 * Math.sqrt(m / 5)), 6, dots.length);
      const amp = 4.5 * Math.sqrt((T + 273) / 473);
      const freq = 4 + 6 * Math.sqrt((T + 273) / 473);
      ctx.fillStyle = 'rgba(255,255,255,.85)';
      for (let i = 0; i < n; i++) {
        const d = dots[i];
        const px = x + 8 + d.x * (side - 16) + amp * Math.sin(t * freq * 1.3 + d.p);
        const py = y - side + 8 + d.y * (side - 16) + amp * Math.cos(t * freq + d.p * 1.7);
        ctx.beginPath(); ctx.arc(px, py, 2.6, 0, Math.PI * 2); ctx.fill();
      }
      ctx.restore();
      Sim.text(ctx, `${fx(T, 1)} °C`, x + side / 2, y - side - 30, { size: 17, weight: 750, align: 'center', color: C.ink });
      Sim.text(ctx, `${label} · ${fx(m, 1)} kg`, x + side / 2, y - side - 11, { size: 12.5, weight: 600, align: 'center', color: C.muted });
    }

    function draw(ctx, w, h, t, dt) {
      if (!P) return;
      const C = Sim.C;
      if (contact) elapsed += dt;
      const s = temps();
      const ground = h - 26, cx = w / 2;
      const S = Math.min(h - 100, w * 0.3);
      const sA = S * Math.cbrt(s.mA / 5), sB = S * Math.cbrt(s.mB / 5);
      const gap = contact ? 0 : 46;
      ctx.strokeStyle = C.line2; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.moveTo(16, ground); ctx.lineTo(w - 16, ground); ctx.stroke();
      block(ctx, cx - gap / 2 - sA, ground, sA, s.tA, dotsA, t, 'A', s.mA);
      block(ctx, cx + gap / 2, ground, sB, s.tB, dotsB, t, 'B', s.mB);
      const diff = s.tA - s.tB;
      if (contact && Math.abs(diff) > 0.3) {
        const y = ground - Math.min(sA, sB) / 2, dir = diff > 0 ? 1 : -1;
        const lw = 2 + 6 * Math.min(1, Math.abs(diff) / 150);
        Sim.arrow(ctx, cx - 34 * dir, y, cx + 34 * dir, y, { color: C.ink, width: lw, head: 10 + lw });
        Sim.text(ctx, 'heat', cx, y - 16, { size: 12.5, weight: 700, align: 'center', color: C.ink, bg: 'rgba(255,255,255,.85)' });
      } else if (!contact) {
        Sim.text(ctx, 'apart', cx, ground - 12, { size: 11.5, align: 'center', color: C.muted });
      }
      readouts(s);
    }
    function readouts(s) {
      Sim.out(root, 'a', `${fx(s.tA, 1)} °C`);
      Sim.out(root, 'b', `${fx(s.tB, 1)} °C`);
      Sim.out(root, 'f', `${fx(s.Tf, 1)} °C`);
      Sim.out(root, 'q', contact ? `${fx(Math.abs(s.Q) / 1000, 1)} kJ` : '0 kJ');
      Sim.out(root, 'calc', `T_f = (${fx(s.mA, 1)}×${fx(s.TA, 0)} + ${fx(s.mB, 1)}×${fx(s.TB, 0)}) ÷ (${fx(s.mA, 1)} + ${fx(s.mB, 1)}) = ${fx(s.Tf, 1)} °C · Q = m_A c (T_A − T_f) = ${fx(s.mA * 4186 * Math.abs(s.TA - s.Tf) / 1000, 1)} kJ`);
      const hot = s.TA > s.TB ? 'A' : 'B', cold = hot === 'A' ? 'B' : 'A';
      const UA = s.mA * (s.TA + 273), UB = s.mB * (s.TB + 273);
      let note;
      if (Math.abs(s.TA - s.TB) < 0.5) note = 'Same temperature: they are already in thermal equilibrium, so no heat flows, even though the masses differ.';
      else if (!contact) note = `Predict: which way will heat flow, and will the final temperature be nearer A's or B's? Then put them in contact.`;
      else {
        note = `Heat flows from ${hot} (hotter) to ${cold}. Both end at ${fx(s.Tf, 1)} °C, closer to the temperature of the heavier block.`;
        const hotterHasLess = hot === 'A' ? UA < UB : UB < UA;
        if (hotterHasLess) note += ` ${cold} stores more internal energy (it has more mass), yet heat still flows into it.`;
      }
      Sim.out(root, 'note', note);
    }
    const st = Sim.stage(host, { aspect: 16 / 9, minH: 250, maxH: 360, animate: true, draw });
    const restart = () => { contact = false; elapsed = 0; btn.textContent = 'Put them in contact'; };
    P = Sim.controls(root, v => { P = v; restart(); st.redraw(); });
    btn.addEventListener('click', () => {
      contact = !contact; elapsed = Sim.reduced ? 60 : 0;
      btn.textContent = contact ? 'Separate and reset' : 'Put them in contact';
      st.redraw();
    });
    root.querySelector('[data-act="nail"]').addEventListener('click', () => {
      setInput(root.querySelector('#hf-ta'), 200); setInput(root.querySelector('#hf-ma'), 0.1);
      setInput(root.querySelector('#hf-tb'), 30); setInput(root.querySelector('#hf-mb'), 5);
    });
    st.redraw();
  }

  /* =================================================================
     2. One thermometer, four scales
     ================================================================= */
  function initScales() {
    const root = fig('sim-scales'); if (!root) return;
    const host = root.querySelector('.sim-stage');
    const slider = root.querySelector('#sc-t');
    let P = null, geo = null;
    const TMIN = -60, TMAX = 160;

    function draw(ctx, w, h) {
      if (!P) return;
      const C = Sim.C;
      const t = P['sc-t'], L = P['sc-l'], U = P['sc-u'];
      const yTop = 34, yBot = h - 52;
      const Y = c => yBot - (c - TMIN) / (TMAX - TMIN) * (yBot - yTop);
      const tx = 40;
      geo = { Y, yTop, yBot, tx };
      // thermometer
      ctx.save();
      ctx.fillStyle = C.surface; ctx.strokeStyle = C.ink2; ctx.lineWidth = 1.5;
      Sim.rrect(ctx, tx - 8, yTop - 14, 16, yBot - yTop + 30, 8); ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.arc(tx, yBot + 26, 15, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.fillStyle = C.coral;
      ctx.beginPath(); ctx.arc(tx, yBot + 26, 11, 0, Math.PI * 2); ctx.fill();
      ctx.fillRect(tx - 3.5, Y(t), 7, yBot + 20 - Y(t));
      ctx.restore();
      // columns
      const scales = [
        { name: '°C', v: c => c },
        { name: '°F', v: c => 1.8 * c + 32 },
        { name: 'K', v: c => c + 273.15 },
        { name: '°X', v: c => L + (U - L) * c / 100, mine: true },
      ];
      const x0 = 84, colW = (w - x0 - 10) / 4;
      [0, 100].forEach(c => {
        Sim.line(ctx, [[tx + 12, Y(c)], [w - 10, Y(c)]], { color: C.line2, width: 1, dash: [4, 4] });
        Sim.text(ctx, c === 0 ? 'ice point' : 'steam point', w - 12, Y(c) - 8, { size: 10.5, color: C.muted, align: 'right' });
      });
      scales.forEach((s, i) => {
        const ax = x0 + i * colW + 8;
        const v0 = s.v(TMIN), v1 = s.v(TMAX), step = niceStep(v1 - v0, 7);
        ctx.save(); ctx.strokeStyle = s.mine ? C.coral : C.ink2; ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.moveTo(ax, yTop); ctx.lineTo(ax, yBot); ctx.stroke(); ctx.restore();
        Sim.text(ctx, s.name, ax, yTop - 18, { size: 14, weight: 750, align: 'center', color: s.mine ? C.coral : C.ink });
        for (let v = Math.ceil(v0 / step) * step; v <= v1 + 1e-9; v += step) {
          const c = (v - s.v(0)) / (s.v(100) - s.v(0)) * 100, y = Y(c);
          Sim.line(ctx, [[ax, y], [ax + 6, y]], { color: C.ink2, width: 1 });
          if (colW > 52) Sim.text(ctx, String(+v.toFixed(2)), ax + 9, y, { size: 10.5, color: C.muted, mono: true });
        }
      });
      // reading line
      const yt = Y(t);
      Sim.line(ctx, [[tx + 10, yt], [w - 10, yt]], { color: C.coral, width: 2 });
      scales.forEach((s, i) => {
        const ax = x0 + i * colW + 8;
        const val = s.v(t);
        Sim.text(ctx, fx(val, 1), ax + 2, yt - 13, { size: 12, weight: 700, color: '#fff', bg: s.mine ? C.coral : C.ink, mono: true });
      });
    }
    function update() {
      const t = P['sc-t'], L = P['sc-l'], U = P['sc-u'];
      const F = 1.8 * t + 32, K = t + 273.15, X = L + (U - L) * t / 100;
      Sim.out(root, 'c', `${fx(t, 1)} °C`);
      Sim.out(root, 'f', `${fx(F, 1)} °F`);
      Sim.out(root, 'k', `${fx(K, 2)} K`);
      Sim.out(root, 'x', `${fx(X, 1)} °X`);
      let note = `Fraction of the way from the ice point to the steam point: ${fx(t / 100, 3)}. Every scale gives this same fraction.`;
      if (Math.abs(t + 40) < 0.3) note = 'At −40 the Celsius and Fahrenheit readings are the same.';
      else if (Math.abs(t - 37) < 0.3) note = 'Body temperature: 37 °C = 98.6 °F = 310 K.';
      Sim.out(root, 'note', note);
    }
    const st = Sim.stage(host, { aspect: 4 / 3, minH: 330, maxH: 460, draw });
    P = Sim.controls(root, v => { P = v; update(); st.redraw(); });
    root.querySelectorAll('[data-go]').forEach(b => b.addEventListener('click', () => setInput(slider, b.dataset.go)));
    const fromPointer = e => {
      if (!geo) return;
      const p = st.toLocal(e);
      const c = TMIN + (geo.yBot - p.y) / (geo.yBot - geo.yTop) * (TMAX - TMIN);
      setInput(slider, Math.round(clamp(c, TMIN, TMAX) * 2) / 2);
    };
    let dragging = false;
    st.canvas.style.cursor = 'ns-resize';
    st.canvas.addEventListener('pointerdown', e => { dragging = true; st.canvas.setPointerCapture(e.pointerId); fromPointer(e); });
    st.canvas.addEventListener('pointermove', e => { if (dragging) fromPointer(e); });
    st.canvas.addEventListener('pointerup', () => { dragging = false; });
    st.canvas.addEventListener('pointercancel', () => { dragging = false; });
    update(); st.redraw();
  }

  /* =================================================================
     3. Constant-volume gas thermometer → absolute zero
     ================================================================= */
  function initGas() {
    const root = fig('sim-gas'); if (!root) return;
    const host = root.querySelector('.sim-stage');
    let P = null;
    const gases = [{ p0: 0.6, c: 'water' }, { p0: 1.0, c: 'coral' }, { p0: 1.5, c: 'plum' }];
    const Pof = (p0, t) => p0 * (t + 273.15) / 273.15;

    function draw(ctx, w, h) {
      if (!P) return;
      const C = Sim.C, t = P['gs-t'], ext = P.ext === 'yes';
      const box = { x: 46, y: 26, w: w - 66, h: h - 70 };
      const ax = Sim.axes(ctx, box, {
        xmin: -300, xmax: 130, ymin: 0, ymax: 2.3,
        xticks: [-273, -200, -100, 0, 100], yticks: [0, 0.5, 1, 1.5, 2],
        xlabel: 'temperature (°C)', ylabel: 'P (atm)',
      });
      gases.forEach(g => {
        const col = C[g.c];
        if (ext) Sim.line(ctx, [[ax.X(-273.15), ax.Y(0)], [ax.X(-50), ax.Y(Pof(g.p0, -50))]], { color: col, width: 2, dash: [6, 5] });
        Sim.line(ctx, [[ax.X(-50), ax.Y(Pof(g.p0, -50))], [ax.X(120), ax.Y(Pof(g.p0, 120))]], { color: col, width: 3 });
        ctx.save(); ctx.fillStyle = col;
        ctx.beginPath(); ctx.arc(ax.X(t), ax.Y(Pof(g.p0, t)), 5.5, 0, Math.PI * 2); ctx.fill(); ctx.restore();
      });
      Sim.line(ctx, [[ax.X(t), box.y], [ax.X(t), box.y + box.h]], { color: C.line2, width: 1, dash: [3, 4] });
      if (ext) {
        ctx.save(); ctx.fillStyle = C.ink; ctx.beginPath(); ctx.arc(ax.X(-273.15), ax.Y(0), 6, 0, Math.PI * 2); ctx.fill(); ctx.restore();
        Sim.text(ctx, 'all meet at −273.15 °C = 0 K', ax.X(-273.15) + 10, ax.Y(0) - 16, { size: 12.5, weight: 700, color: C.ink, bg: 'rgba(255,255,255,.9)' });
      } else {
        Sim.text(ctx, 'Keep cooling… where do the lines go?', ax.X(-250), ax.Y(1.9), { size: 12.5, weight: 600, color: C.muted });
      }
    }
    function update() {
      const t = P['gs-t'], T = t + 273.15, p = Pof(1, t);
      Sim.out(root, 'tk', `${fx(T, 2)} K`);
      Sim.out(root, 'p', `${fx(p, 3)} atm`);
      Sim.out(root, 'ratio', `${fx(p / T * 1000, 3)} × 10⁻³ atm/K`);
      const perC = Math.abs(t) < 0.5 ? 'undefined (t = 0)' : fx(p / t, 4) + ' atm/°C';
      Sim.out(root, 'note', P.ext === 'yes'
        ? 'Every sample, large or small, reaches zero pressure at the same temperature. That point is the zero of the Kelvin scale.'
        : `P ÷ T(K) stays at 3.661 × 10⁻³ atm/K. P ÷ t(°C) is ${perC}, which keeps changing. Now press "Extend the lines".`);
    }
    const st = Sim.stage(host, { aspect: 16 / 10, minH: 260, maxH: 380, draw });
    P = Sim.controls(root, v => { P = v; update(); st.redraw(); });
    update(); st.redraw();
  }

  /* =================================================================
     4. Expansion lab — plate with hole / rod between rigid walls
     ================================================================= */
  const MATS = {
    al: { name: 'Aluminium', a: 2.5e-5, Y: 7.0e10 },
    brass: { name: 'Brass', a: 1.8e-5, Y: 9.1e10 },
    steel: { name: 'Steel', a: 1.2e-5, Y: 2.0e11 },
    glass: { name: 'Pyrex', a: 0.32e-5, Y: 6.4e10 },
    invar: { name: 'Invar', a: 0.12e-5, Y: 1.4e11 },
  };
  function initExpand() {
    const root = fig('sim-expand'); if (!root) return;
    const host = root.querySelector('.sim-stage');
    const MAG = 40;
    let P = null;

    function draw(ctx, w, h) {
      if (!P) return;
      const C = Sim.C, m = MATS[P.mat], dT = P['ex-dt'];
      const s = 1 + m.a * dT * MAG;
      const fill = heatColor(dT, -100, 300, 0.85);
      if (P.mode === 'plate') {
        const cx = w / 2, cy = h / 2 + 6;
        const w0 = Math.min(w * 0.56, (h - 70) * 1.45), h0 = w0 / 1.45, r0 = h0 * 0.24;
        ctx.save();
        ctx.fillStyle = fill; ctx.strokeStyle = 'rgba(27,34,51,.45)'; ctx.lineWidth = 1.5;
        Sim.rrect(ctx, cx - w0 * s / 2, cy - h0 * s / 2, w0 * s, h0 * s, 10); ctx.fill(); ctx.stroke();
        ctx.fillStyle = '#F7F8FB';
        ctx.beginPath(); ctx.arc(cx, cy, r0 * s, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
        ctx.setLineDash([5, 5]); ctx.strokeStyle = C.ink;
        Sim.rrect(ctx, cx - w0 / 2, cy - h0 / 2, w0, h0, 10); ctx.stroke();
        ctx.beginPath(); ctx.arc(cx, cy, r0, 0, Math.PI * 2); ctx.stroke();
        ctx.restore();
        Sim.arrow(ctx, cx - r0 * s, cy, cx + r0 * s, cy, { color: C.ink, width: 1.4, head: 8 });
        Sim.arrow(ctx, cx + r0 * s, cy, cx - r0 * s, cy, { color: C.ink, width: 1.4, head: 8 });
        Sim.text(ctx, 'hole', cx, cy - 12, { size: 12, weight: 700, align: 'center' });
        Sim.text(ctx, 'dashed = before heating · change drawn 40× larger', 12, 16, { size: 11.5, color: C.muted });
      } else {
        const wallW = 26, x1 = 26 + wallW, x2 = w - 26 - wallW, cy = h / 2, th = 30;
        hatch(ctx, 26, cy - 70, wallW, 140); hatch(ctx, x2, cy - 70, wallW, 140);
        ctx.save(); ctx.fillStyle = fill; ctx.strokeStyle = 'rgba(27,34,51,.45)'; ctx.lineWidth = 1.5;
        ctx.fillRect(x1, cy - th / 2, x2 - x1, th); ctx.strokeRect(x1, cy - th / 2, x2 - x1, th); ctx.restore();
        const grow = (x2 - x1) * m.a * dT * MAG;
        if (Math.abs(grow) > 1) {
          ctx.save(); ctx.setLineDash([5, 4]); ctx.strokeStyle = C.coral; ctx.lineWidth = 1.5;
          ctx.fillStyle = dT > 0 ? 'rgba(214,96,74,.18)' : 'rgba(58,140,203,.12)';
          const gx = dT > 0 ? x2 : x2 + grow, gw = Math.abs(grow);
          ctx.fillRect(gx, cy - th / 2, gw, th); ctx.strokeRect(gx, cy - th / 2, gw, th); ctx.restore();
          Sim.text(ctx, dT > 0 ? 'would grow into the wall' : 'would shrink away from the wall', x2 - 6, cy - th / 2 - 16, { size: 12, weight: 650, align: 'right', color: C.coral });
          const inward = dT > 0, a = 46, ay = cy;
          if (inward) {
            Sim.arrow(ctx, x1 + a + 30, ay, x1 + 30, ay, { color: C.ink, width: 2.5 });
            Sim.arrow(ctx, x2 - a - 30, ay, x2 - 30, ay, { color: C.ink, width: 2.5 });
          } else {
            Sim.arrow(ctx, x1 + 30, ay, x1 + a + 30, ay, { color: C.ink, width: 2.5 });
            Sim.arrow(ctx, x2 - 30, ay, x2 - a - 30, ay, { color: C.ink, width: 2.5 });
          }
          Sim.text(ctx, inward ? 'walls push in: compression' : 'walls pull out: tension', w / 2, cy + th / 2 + 24, { size: 13, weight: 700, align: 'center' });
        }
        Sim.text(ctx, 'rigid walls · change drawn 40× larger', 12, 16, { size: 11.5, color: C.muted });
      }
    }
    function update() {
      const m = MATS[P.mat], dT = P['ex-dt'];
      const lab = (k, t) => { const el = root.querySelector(`[data-k="${k}"]`); if (el) el.textContent = t; };
      lab('r1', 'α'); Sim.out(root, 'r1', `${Sim.sci(m.a, 2)} K⁻¹`);
      const dL = m.a * dT * 1000; // mm for a 1 m length
      if (P.mode === 'plate') {
        lab('r2', 'ΔL of a 1 m edge'); Sim.out(root, 'r2', `${fx(dL, 2)} mm`);
        lab('r3', '10.000 cm hole →'); Sim.out(root, 'r3', `${fx(10 * (1 + m.a * dT), 4)} cm`);
        lab('r4', 'Area / volume'); Sim.out(root, 'r4', `${fx(2 * m.a * dT * 100, 3)} % / ${fx(3 * m.a * dT * 100, 3)} %`);
        Sim.out(root, 'note', dT === 0 ? 'Set a temperature change.' : dT > 0
          ? 'The hole grows by exactly the same fraction as the metal, as if the whole plate were photo-enlarged.'
          : 'On cooling, the plate and the hole both shrink by the same fraction.');
      } else {
        const stress = m.Y * m.a * dT;
        lab('r2', 'Free 1 m rod would change'); Sim.out(root, 'r2', `${fx(dL, 2)} mm`);
        lab('r3', 'Thermal stress YαΔT'); Sim.out(root, 'r3', `${fx(Math.abs(stress) / 1e6, 1)} MPa`);
        lab('r4', 'Force if A = 2 cm²'); Sim.out(root, 'r4', `${fx(Math.abs(stress) * 2e-4 / 1000, 2)} kN`);
        Sim.out(root, 'note', dT === 0 ? 'Set a temperature change.'
          : `${dT > 0 ? 'Compressive' : 'Tensile'} stress. It is the same for a 1 m or a 10 m rod, because stress = YαΔT has no length in it. Try Invar: tiny α, tiny stress.`);
      }
    }
    const st = Sim.stage(host, { aspect: 16 / 10, minH: 260, maxH: 380, draw });
    P = Sim.controls(root, v => { P = v; update(); st.redraw(); });
    update(); st.redraw();
  }

  /* =================================================================
     5. Bimetallic strip thermostat (true scale: L = 10 cm, d = 0.5 mm)
     ================================================================= */
  const PAIRS = {
    bi: { top: 'Brass', bot: 'Iron', a1: 1.8e-5, a2: 1.2e-5, c1: '#C2850E', c2: '#737C91' },
    cs: { top: 'Copper', bot: 'Steel', a1: 1.7e-5, a2: 1.2e-5, c1: '#D6604A', c2: '#737C91' },
    ai: { top: 'Aluminium', bot: 'Invar', a1: 2.5e-5, a2: 0.12e-5, c1: '#9AA3B5', c2: '#4B5BD0' },
  };
  function initBimetal() {
    const root = fig('sim-bimetal'); if (!root) return;
    const host = root.querySelector('.sim-stage');
    const L = 0.10, D = 0.5e-3, OFF = 2e-3;
    let P = null;
    const kappa = (p, dT) => (p.a1 - p.a2) * dT / D;
    const defl = k => Math.abs(k) < 1e-9 ? 0 : (1 - Math.cos(k * L)) / k; // + = downwards

    function draw(ctx, w, h) {
      if (!P) return;
      const C = Sim.C, p = PAIRS[P.pair], dT = P['bm-dt'];
      const maxDown = defl(kappa(p, 200)), maxUp = -defl(kappa(p, -100));
      const x0 = 70;
      const ppm = Math.min((w - x0 - 70) / L, (h - 80) / (maxDown + maxUp + 0.004));
      const y0 = Math.max(40, (h - (maxDown + maxUp) * ppm) / 2) + maxUp * ppm;
      const k = kappa(p, dT) / ppm; // px⁻¹
      const Lpx = L * ppm, N = 60, th = 7;
      const pt = s => Math.abs(k) < 1e-9 ? [x0 + s, y0] : [x0 + Math.sin(k * s) / k, y0 + (1 - Math.cos(k * s)) / k];
      const nrm = s => [Math.sin(k * s), -Math.cos(k * s)]; // points "up" from the centre line
      const layer = (off0, off1, col) => {
        const a = [], b = [];
        for (let i = 0; i <= N; i++) {
          const s = Lpx * i / N, c = pt(s), n = nrm(s);
          a.push([c[0] + n[0] * off0, c[1] + n[1] * off0]);
          b.push([c[0] + n[0] * off1, c[1] + n[1] * off1]);
        }
        Sim.line(ctx, a.concat(b.reverse()), { color: 'rgba(27,34,51,.5)', width: 1, fill: col, close: true });
      };
      layer(th, 0, p.c1); layer(0, -th, p.c2);
      hatch(ctx, x0 - 34, y0 - 30, 34, 60);
      // contact screw that touches the strip at rest
      const tip = pt(Lpx), cxp = x0 + Lpx - 4, restTop = y0 - th;
      const tipTop = tip[1] - th * Math.cos(k * Lpx);
      const cy = Math.min(restTop, tipTop);
      ctx.save(); ctx.fillStyle = C.ink2; ctx.fillRect(cxp - 6, cy - 22, 12, 20); ctx.restore();
      const on = defl(kappa(p, dT)) < OFF;
      // lamp
      const lx = w - 34, ly = 34;
      ctx.save();
      if (on) { ctx.fillStyle = 'rgba(194,133,14,.25)'; ctx.beginPath(); ctx.arc(lx, ly, 22, 0, Math.PI * 2); ctx.fill(); }
      ctx.fillStyle = on ? '#F2B630' : C.surface2; ctx.strokeStyle = C.ink2; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.arc(lx, ly, 12, 0, Math.PI * 2); ctx.fill(); ctx.stroke(); ctx.restore();
      Sim.text(ctx, on ? 'heater ON' : 'heater OFF', lx, ly + 26, { size: 11.5, weight: 700, align: 'center', color: on ? C.amber : C.muted });
      Sim.text(ctx, `${p.top} (larger α)`, x0 + 6, y0 - th - 12, { size: 12, weight: 650, color: C.ink });
      Sim.text(ctx, p.bot, x0 + 6, y0 + th + 12, { size: 12, weight: 650, color: C.ink });
      Sim.text(ctx, 'true scale: 10 cm strip, layers drawn thicker', 12, h - 12, { size: 11, color: C.muted });
    }
    function update() {
      const p = PAIRS[P.pair], dT = P['bm-dt'], k = kappa(p, dT), y = defl(k);
      Sim.out(root, 'da', `${Sim.sci(p.a1 - p.a2, 2)} K⁻¹`);
      Sim.out(root, 'R', Math.abs(k) < 1e-9 ? 'straight' : `${fx(1 / Math.abs(k), 2)} m`);
      Sim.out(root, 'y', `${fx(Math.abs(y) * 1000, 1)} mm ${y > 0 ? 'down' : y < 0 ? 'up' : ''}`);
      const on = y < OFF;
      Sim.out(root, 'sw', on ? 'ON' : 'OFF');
      const dToff = 2 * D * OFF / (L * L * (p.a1 - p.a2));
      const msg = dT > 0 ? `Heated: ${p.top} grows more, so it sits on the outer (convex) side and the strip bends towards ${p.bot}.`
        : dT < 0 ? `Cooled: ${p.top} shrinks more, so it is now on the inner side and the strip bends towards ${p.top}.`
        : 'No temperature change: the strip is straight.';
      Sim.out(root, 'note', `${msg} The contact opens and switches the heater off above about +${fx(dToff, 0)} K.`);
    }
    const st = Sim.stage(host, { aspect: 16 / 8, minH: 240, maxH: 320, draw });
    P = Sim.controls(root, v => { P = v; update(); st.redraw(); });
    update(); st.redraw();
  }

  /* =================================================================
     6. Water near 4 °C — density curve and a lake in winter
     ================================================================= */
  const RHO = [999.84, 999.90, 999.94, 999.96, 999.97, 999.96, 999.94, 999.90, 999.85, 999.78, 999.70, 999.61, 999.50];
  const rhoAt = t => { const i = clamp(Math.floor(t), 0, 11), f = t - i; return RHO[i] + (RHO[i + 1] - RHO[i]) * f; };
  /* lake colour: pale at 0 °C, deepest blue at 4 °C (densest), lighter teal when warmer */
  const waterCol = t => {
    t = clamp(t, 0, 12);
    const a = t <= 4 ? [169, 214, 242] : [47, 111, 176], b = t <= 4 ? [47, 111, 176] : [88, 170, 186];
    const u = t <= 4 ? t / 4 : (t - 4) / 8;
    return `rgb(${a.map((v, k) => Math.round(v + (b[k] - v) * u)).join(',')})`;
  };
  function initWater() {
    const root = fig('sim-water'); if (!root) return;
    const host = root.querySelector('.sim-stage');
    let P = null;

    function lake(ctx, x, y, w, h, air) {
      const C = Sim.C;
      Sim.text(ctx, `Air ${air > 0 ? '+' : ''}${air} °C`, x + w / 2, y + 10, { size: 13, weight: 700, align: 'center', color: air < 0 ? C.water : C.amber });
      const top = y + 30, bot = y + h - 6, l = x + 6, r = x + w - 6;
      ctx.save();
      ctx.beginPath(); ctx.moveTo(l, top); ctx.lineTo(r, top); ctx.lineTo(r - 26, bot); ctx.lineTo(l + 26, bot); ctx.closePath();
      ctx.clip();
      const grad = ctx.createLinearGradient(0, top, 0, bot);
      let iceH = 0;
      if (air >= 4) { grad.addColorStop(0, waterCol(air)); grad.addColorStop(1, waterCol(air)); }
      else if (air >= 0) { grad.addColorStop(0, waterCol(air)); grad.addColorStop(0.45, waterCol(4)); grad.addColorStop(1, waterCol(4)); }
      else { iceH = 10 + (-air) * 2.2; grad.addColorStop(0, waterCol(0)); grad.addColorStop(0.5, waterCol(3.5)); grad.addColorStop(1, waterCol(4)); }
      ctx.fillStyle = grad; ctx.fillRect(l, top, r - l, bot - top);
      if (iceH) {
        ctx.fillStyle = '#EAF4FB'; ctx.fillRect(l, top, r - l, iceH);
        ctx.strokeStyle = '#9CC3E3'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(l, top + iceH); ctx.lineTo(r, top + iceH); ctx.stroke();
      }
      ctx.restore();
      ctx.save(); ctx.strokeStyle = C.ink2; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.moveTo(l, top); ctx.lineTo(l + 26, bot); ctx.lineTo(r - 26, bot); ctx.lineTo(r, top); ctx.stroke(); ctx.restore();
      if (iceH) Sim.text(ctx, 'ice 0 °C', x + w / 2, top + iceH / 2, { size: 11.5, weight: 700, align: 'center', color: C.ink2 });
      const topT = air >= 4 ? air : Math.max(air, 0);
      Sim.text(ctx, `${topT} °C`, r - 10, top + iceH + 14, { size: 11.5, weight: 700, align: 'right', color: topT < 2.5 ? C.ink : '#fff' });
      Sim.text(ctx, `${air >= 4 ? air : 4} °C`, r - 34, bot - 14, { size: 11.5, weight: 700, align: 'right', color: '#fff' });
      // fish
      const fx0 = l + 50, fy = bot - 22;
      ctx.save(); ctx.fillStyle = C.amber;
      ctx.beginPath(); ctx.ellipse(fx0, fy, 13, 6, 0, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.moveTo(fx0 - 11, fy); ctx.lineTo(fx0 - 21, fy - 6); ctx.lineTo(fx0 - 21, fy + 6); ctx.closePath(); ctx.fill();
      ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(fx0 + 7, fy - 1.5, 1.6, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    }
    function draw(ctx, w, h) {
      if (!P) return;
      const C = Sim.C, t = P['wt-t'];
      const wide = w >= 560;
      const gW = wide ? w * 0.56 : w, gH = wide ? h : h * 0.55;
      const box = { x: 62, y: 28, w: gW - 84, h: gH - 76 };
      const ax = Sim.axes(ctx, box, {
        xmin: 0, xmax: 12, ymin: 999.45, ymax: 1000.02,
        xticks: [0, 2, 4, 6, 8, 10, 12], yticks: [999.5, 999.7, 999.9],
        yfmt: v => v.toFixed(1), xlabel: 'T (°C)', ylabel: 'ρ (kg m⁻³)',
      });
      const pts = []; for (let i = 0; i <= 120; i++) { const tt = i / 10; pts.push([ax.X(tt), ax.Y(rhoAt(tt))]); }
      Sim.line(ctx, pts, { color: C.water, width: 3 });
      Sim.line(ctx, [[ax.X(4), ax.Y(999.97)], [ax.X(4), box.y + box.h]], { color: C.line2, width: 1, dash: [3, 4] });
      Sim.text(ctx, 'densest at 4 °C', ax.X(4) + 8, ax.Y(999.97) - 12, { size: 11.5, weight: 700, color: C.water });
      const y = ax.Y(rhoAt(t));
      ctx.save(); ctx.fillStyle = C.coral; ctx.beginPath(); ctx.arc(ax.X(t), y, 6, 0, Math.PI * 2); ctx.fill(); ctx.restore();
      if (wide) lake(ctx, gW + 4, 10, w - gW - 12, h - 20, P['wt-air']);
      else lake(ctx, 10, gH, w - 20, h - gH - 6, P['wt-air']);
    }
    function update() {
      const t = P['wt-t'], air = P['wt-air'], r = rhoAt(t);
      Sim.out(root, 'rho', `${fx(r, 2)} kg/m³`);
      Sim.out(root, 'vol', `${fx(1e6 / r, 2)} cm³`);
      Sim.out(root, 'dir', t < 3.9 ? 'it contracts' : t > 4.1 ? 'it expands' : 'hardly changes');
      Sim.out(root, 'note', air < 0
        ? 'Ice is lighter than water, so it floats and insulates the lake. Below it the water warms to 4 °C at the bottom, so fish survive.'
        : air < 4 ? 'Water colder than 4 °C is lighter, so it stays on top. Convection stops and the 4 °C water stays at the bottom.'
        : 'Above 4 °C, cooled surface water is denser and sinks, so convection mixes the whole lake.');
    }
    const st = Sim.stage(host, { aspect: 16 / 10, minH: 400, maxH: 440, draw });
    P = Sim.controls(root, v => { P = v; update(); st.redraw(); });
    update(); st.redraw();
  }

  /* =================================================================
     7. Experiment 6 — capillary rise virtual lab with detergent
     ================================================================= */
  function initCapLab() {
    const root = fig('sim-caplab'); if (!root) return;
    const host = root.querySelector('.sim-stage');
    const tbody = root.querySelector('[data-r="rows"]');
    const meanEl = root.querySelector('[data-r="mean"]');
    const RADII = [0.20, 0.30, 0.45, 0.60]; // mm
    const NAMES = ['A', 'B', 'C', 'D'];
    const rows = [];
    let P = null;
    const Tclean = th => 0.0757 - 0.000148 * th - 0.0000002 * th * th;
    const Tof = (th, drops) => { const Tw = Tclean(th); return Tw - (Tw - 0.030) * drops / (drops + 2); };
    const rhoOf = th => 1000 - 0.0049 * (th - 4) * (th - 4);
    const hOf = (rmm, T, rho) => 2 * T / (rmm * 1e-3 * rho * G); // m

    function draw(ctx, w, h) {
      if (!P) return;
      const C = Sim.C, th = P['cl-temp'], drops = P['cl-det'], sel = +P.tube;
      const T = Tof(th, drops), rho = rhoOf(th);
      const bl = 20, br = w - 66, yw = h - 64, bb = h - 12;
      const ppc = (yw - 36) / 9; // px per cm
      const tint = drops ? `rgba(${58 + drops * 8},${140 - drops * 5},${203 - drops * 3},0.30)` : 'rgba(58,140,203,0.24)';
      // beaker water
      ctx.save(); ctx.fillStyle = tint; ctx.fillRect(bl, yw, br - bl, bb - yw); ctx.restore();
      Sim.line(ctx, [[bl, yw - 40], [bl, bb], [br, bb], [br, yw - 40]], { color: C.ink2, width: 2 });
      Sim.line(ctx, [[bl, yw], [br, yw]], { color: C.liquidEdge, width: 1.5 });
      // ruler
      const rx = w - 46;
      Sim.line(ctx, [[rx, yw], [rx, yw - 9 * ppc]], { color: C.ink2, width: 1.5 });
      for (let c = 0; c <= 9; c++) {
        Sim.line(ctx, [[rx, yw - c * ppc], [rx + 8, yw - c * ppc]], { color: C.ink2, width: 1 });
        Sim.text(ctx, String(c), rx + 12, yw - c * ppc, { size: 10.5, mono: true, color: C.muted });
        if (c < 9) Sim.line(ctx, [[rx, yw - (c + 0.5) * ppc], [rx + 4, yw - (c + 0.5) * ppc]], { color: C.line2, width: 1 });
      }
      Sim.text(ctx, 'cm', rx + 4, yw - 9 * ppc - 14, { size: 10.5, color: C.muted });
      // tubes
      const span = br - bl;
      RADII.forEach((rmm, i) => {
        const cx = bl + span * (i + 0.5) / 4;
        const inner = 4 + rmm * 22, wall = 3;
        const top = 22, bottom = yw + 34;
        const hp = hOf(rmm, T, rho) * 100 * ppc;
        const ym = yw - hp;
        // water column + meniscus
        ctx.save(); ctx.fillStyle = drops ? tint.replace('0.30', '0.55') : 'rgba(58,140,203,0.5)';
        ctx.beginPath();
        ctx.moveTo(cx - inner / 2, bottom); ctx.lineTo(cx - inner / 2, ym - inner * 0.45);
        ctx.quadraticCurveTo(cx, ym + inner * 0.45, cx + inner / 2, ym - inner * 0.45);
        ctx.lineTo(cx + inner / 2, bottom); ctx.closePath(); ctx.fill(); ctx.restore();
        // glass walls
        ctx.save(); ctx.fillStyle = 'rgba(205,210,221,.65)'; ctx.strokeStyle = i === sel ? C.plum : C.ink2; ctx.lineWidth = i === sel ? 2 : 1.2;
        ctx.fillRect(cx - inner / 2 - wall, top, wall, bottom - top); ctx.strokeRect(cx - inner / 2 - wall, top, wall, bottom - top);
        ctx.fillRect(cx + inner / 2, top, wall, bottom - top); ctx.strokeRect(cx + inner / 2, top, wall, bottom - top);
        ctx.restore();
        Sim.text(ctx, NAMES[i], cx, 12, { size: 12.5, weight: 750, align: 'center', color: i === sel ? C.plum : C.ink2 });
        if (i === sel) {
          const dx = cx + inner / 2 + wall + 10;
          Sim.line(ctx, [[cx - inner, ym], [dx + 4, ym]], { color: C.plum, width: 1, dash: [3, 3] });
          Sim.arrow(ctx, dx, (yw + ym) / 2, dx, ym, { color: C.plum, width: 1.4, head: 7 });
          Sim.arrow(ctx, dx, (yw + ym) / 2, dx, yw, { color: C.plum, width: 1.4, head: 7 });
          Sim.text(ctx, 'h', dx + 6, (yw + ym) / 2, { size: 13, weight: 750, color: C.plum });
          ctx.save(); ctx.strokeStyle = C.plum; ctx.lineWidth = 1.2;
          ctx.beginPath(); ctx.arc(cx, ym, 9, 0, Math.PI * 2); ctx.moveTo(cx - 13, ym); ctx.lineTo(cx + 13, ym); ctx.stroke(); ctx.restore();
        }
      });
      Sim.text(ctx, 'tube widths exaggerated · heights to scale', bl + 4, bb - 10, { size: 10.5, color: C.muted });
    }
    function update() {
      const th = P['cl-temp'], drops = P['cl-det'], r = RADII[+P.tube];
      const T = Tof(th, drops), rho = rhoOf(th), hm = hOf(r, T, rho);
      Sim.out(root, 'r', `${fx(r, 2)} mm`);
      Sim.out(root, 'h', `${fx(hm * 100, 2)} cm`);
      Sim.out(root, 'hr', `${Sim.sci(hm * r * 1e-3, 2)} m²`);
      Sim.out(root, 'T', `${fx(T, 4)} N/m`);
      const Tw = Tclean(th);
      Sim.out(root, 'note', drops > 0
        ? `Detergent lowered T from ${fx(Tw, 4)} to ${fx(T, 4)} N/m, so every column dropped by the same fraction (${fx((1 - T / Tw) * 100, 0)} %).`
        : th !== 25 ? `At ${th} °C, clean water has T = ${fx(T, 4)} N/m. Hotter water has lower T, so the columns are lower.`
        : 'Narrow tube, high rise: h × r is the same for all four tubes. Record a reading from each tube, then add detergent.');
    }
    function render() {
      if (!rows.length) {
        tbody.innerHTML = '<tr><td colspan="7" class="muted">No readings yet. Pick a tube and press "Record this reading".</td></tr>';
        meanEl.textContent = ''; return;
      }
      tbody.innerHTML = rows.map((r, i) => `<tr><td>${i + 1}</td><td>${r.name}</td><td>${fx(r.r, 3)}</td><td>${r.drops ? r.drops + ' drops' : 'none'}</td><td>${r.th} °C</td><td>${fx(r.h, 2)}</td><td>${fx(r.T, 4)}</td></tr>`).join('');
      const groups = new Map();
      rows.forEach(r => { const k = `${r.drops}|${r.th}`; if (!groups.has(k)) groups.set(k, []); groups.get(k).push(r.T); });
      meanEl.textContent = [...groups].map(([k, list]) => {
        const [d, th] = k.split('|');
        const mean = list.reduce((a, b) => a + b, 0) / list.length;
        return `${+d ? d + ' drops detergent' : 'Clean water'}, ${th} °C: mean T = ${fx(mean, 4)} N/m (${list.length} reading${list.length > 1 ? 's' : ''})`;
      }).join(' · ');
    }
    root.querySelector('[data-act="record"]').addEventListener('click', () => {
      const th = P['cl-temp'], drops = P['cl-det'], i = +P.tube, r = RADII[i];
      const T = Tof(th, drops), rho = rhoOf(th);
      const rm = r + (Math.random() - 0.5) * 0.008;               // mm, microscope reading
      const hm = hOf(r, T, rho) * 100 + (Math.random() - 0.5) * 0.04; // cm
      rows.push({ name: NAMES[i], r: rm, drops, th, h: hm, T: rm * 1e-3 * hm * 1e-2 * rho * G / 2 });
      if (rows.length > 12) rows.shift();
      render();
    });
    root.querySelector('[data-act="clear"]').addEventListener('click', () => { rows.length = 0; render(); });
    const st = Sim.stage(host, { aspect: 16 / 11, minH: 330, maxH: 460, draw });
    P = Sim.controls(root, v => { P = v; update(); st.redraw(); });
    update(); st.redraw();
  }

  /* =================================================================
     8. First law on a P–V diagram — 1 mol ideal gas, four processes
     ================================================================= */
  function initPV() {
    const root = fig('sim-pv'); if (!root) return;
    const host = root.querySelector('.sim-stage');
    const lbl = root.querySelector('[data-lbl]');
    const R = 8.314, TA = 300, VA = 0.010, PA = R * TA / VA;
    let P = null;

    function solve() {
      const x = P['pv-x'], mono = P.gas === 'mono';
      const Cv = (mono ? 1.5 : 2.5) * R, g = mono ? 5 / 3 : 1.4;
      let VB = VA * x, PB, TB, W;
      const Pv = v => P.proc === 'isobaric' ? PA : P.proc === 'isothermal' ? PA * VA / v : PA * Math.pow(VA / v, g);
      if (P.proc === 'isochoric') { VB = VA; TB = TA * x; PB = PA * x; W = 0; }
      else if (P.proc === 'isobaric') { PB = PA; TB = TA * x; W = PA * (VB - VA); }
      else if (P.proc === 'isothermal') { PB = PA / x; TB = TA; W = R * TA * Math.log(x); }
      else { PB = Pv(VB); TB = TA * Math.pow(x, 1 - g); W = (PA * VA - PB * VB) / (g - 1); }
      const dU = Cv * (TB - TA);
      return { x, VB, PB, TB, W, dU, Q: dU + W, Pv };
    }
    function bars(ctx, box, s) {
      const C = Sim.C, items = [['Q', s.Q, C.coral], ['ΔU', s.dU, C.amber], ['W', s.W, C.teal]];
      const scale = Math.max(1000, ...items.map(i => Math.abs(i[1])));
      const zero = box.y + box.h / 2, half = box.h / 2 - 40, bw = Math.min(46, box.w / 3 * 0.55);
      Sim.line(ctx, [[box.x, zero], [box.x + box.w, zero]], { color: C.ink2, width: 1.2 });
      items.forEach(([name, v, col], i) => {
        const cx = box.x + box.w * (i + 0.5) / 3, hgt = v / scale * half;
        ctx.save(); ctx.fillStyle = col; ctx.fillRect(cx - bw / 2, zero - Math.max(hgt, 0), bw, Math.abs(hgt)); ctx.restore();
        const lab = `${v >= 0 ? '+' : '−'}${fx(Math.abs(v), 0)} J`;
        Sim.text(ctx, name, cx, hgt >= 0 ? zero + 14 : zero - 14, { size: 13, weight: 750, align: 'center', color: col });
        Sim.text(ctx, lab, cx, hgt >= 0 ? zero - hgt - 11 : zero - hgt + 11, { size: 11.5, weight: 650, align: 'center', mono: true, color: C.ink });
      });
      Sim.text(ctx, 'Q = ΔU + W', box.x + box.w / 2, box.y + 8, { size: 12.5, weight: 700, align: 'center', color: C.ink2 });
    }
    function draw(ctx, w, h) {
      if (!P) return;
      const C = Sim.C, s = solve(), wide = w >= 560;
      const gW = wide ? w * 0.66 : w, gH = wide ? h : h * 0.62;
      const box = { x: 54, y: 26, w: gW - 74, h: gH - 66 };
      const ax = Sim.axes(ctx, box, { xmin: 0, xmax: 22, ymin: 0, ymax: 820, xticks: [0, 5, 10, 15, 20], yticks: [0, 200, 400, 600, 800], xlabel: 'V (L)', ylabel: 'P (kPa)' });
      const X = v => ax.X(v * 1000), Y = p => ax.Y(p / 1000);
      // reference isotherms through A and B
      [TA, s.TB].forEach((T, i) => {
        if (i && Math.abs(T - TA) < 1) return;
        const pts = []; for (let v = 0.004; v <= 0.022; v += 0.0002) { const p = R * T / v; if (p <= 820e3) pts.push([X(v), Y(p)]); }
        Sim.line(ctx, pts, { color: C.line2, width: 1, dash: [4, 4] });
        const pe = R * T / 0.021; if (pe < 800e3) Sim.text(ctx, `${fx(T, 0)} K`, X(0.021), Y(pe) - 9, { size: 10.5, color: C.muted, align: 'right' });
      });
      // path and the work area under it
      const pts = [];
      if (P.proc === 'isochoric') pts.push([X(VA), Y(PA)], [X(VA), Y(s.PB)]);
      else for (let k = 0; k <= 60; k++) { const v = VA + (s.VB - VA) * k / 60; pts.push([X(v), Y(s.Pv(v))]); }
      if (P.proc !== 'isochoric' && Math.abs(s.VB - VA) > 1e-6) {
        Sim.line(ctx, pts.concat([[X(s.VB), Y(0)], [X(VA), Y(0)]]), { color: 'none', fill: s.W >= 0 ? 'rgba(19,129,126,.18)' : 'rgba(214,96,74,.18)', close: true });
        const mid = (VA + s.VB) / 2;
        Sim.text(ctx, s.W >= 0 ? 'area = W (by gas)' : 'area = work on gas', X(mid), Y(s.Pv(mid)) + (box.y + box.h - Y(s.Pv(mid))) / 2, { size: 11.5, weight: 700, align: 'center', color: s.W >= 0 ? C.teal : C.coral });
      }
      Sim.line(ctx, pts, { color: C.ink, width: 3 });
      const n = pts.length; if (Math.hypot(pts[n - 1][0] - pts[0][0], pts[n - 1][1] - pts[0][1]) > 8) Sim.arrow(ctx, pts[n - 2][0], pts[n - 2][1], pts[n - 1][0], pts[n - 1][1], { color: C.ink, width: 3, head: 12 });
      [[VA, PA, 'A'], [s.VB, s.PB, 'B']].forEach(([v, p, name]) => {
        ctx.save(); ctx.fillStyle = name === 'A' ? C.ink2 : C.teal; ctx.beginPath(); ctx.arc(X(v), Y(p), 5.5, 0, Math.PI * 2); ctx.fill(); ctx.restore();
        Sim.text(ctx, name, X(v) + 9, Y(p) - 10, { size: 13, weight: 750 });
      });
      bars(ctx, wide ? { x: gW + 4, y: 20, w: w - gW - 14, h: h - 40 } : { x: 20, y: gH + 4, w: w - 40, h: h - gH - 12 }, s);
    }
    function update() {
      const s = solve();
      lbl.textContent = P.proc === 'isochoric' ? 'Final temperature ÷ start temperature' : 'Final volume ÷ start volume';
      const sgn = v => `${v >= 0 ? '+' : '−'}${fx(Math.abs(v), 0)} J`;
      Sim.out(root, 'q', sgn(s.Q)); Sim.out(root, 'u', sgn(s.dU)); Sim.out(root, 'w', sgn(s.W));
      Sim.out(root, 'state', `${fx(s.PB / 1000, 0)} kPa, ${fx(s.VB * 1000, 1)} L, ${fx(s.TB, 0)} K`);
      const up = s.x >= 1, mono = P.gas === 'mono';
      const notes = {
        isochoric: up ? 'Volume is fixed, so W = 0 and every joule of heat goes into internal energy.' : 'Cooling at fixed volume: W = 0, so the heat that leaves comes straight out of U.',
        isobaric: `At constant pressure the heat splits: W = nRΔT goes into work and ΔU = nC<sub>V</sub>ΔT stays inside. Here ${mono ? '3/5' : '5/7'} of Q raises U.`,
        isothermal: up ? 'Temperature is fixed, so ΔU = 0 and Q = W: all the heat taken in is turned into work.' : 'Isothermal compression: ΔU = 0, so the work done on the gas leaves as heat.',
        adiabatic: up ? 'No heat flows (Q = 0), so the gas pays for its work out of its own internal energy and cools.' : 'No heat flows (Q = 0), so the work done on the gas raises U and the gas heats up, like a bicycle pump.',
      };
      root.querySelector('[data-r="note"]').innerHTML = notes[P.proc];
    }
    const st = Sim.stage(host, { aspect: 16 / 10, minH: 360, maxH: 440, draw });
    P = Sim.controls(root, v => { P = v; update(); st.redraw(); });
    update(); st.redraw();
  }

  /* =================================================================
     9. Heat engine / refrigerator against the Carnot limit
     ================================================================= */
  function initEngine() {
    const root = fig('sim-engine'); if (!root) return;
    const host = root.querySelector('.sim-stage');
    let P = null;

    function solve() {
      const T1 = P['en-t1'], T2 = P['en-t2'], ok = T2 < T1;
      if (P.mode === 'engine') {
        const lim = ok ? 1 - T2 / T1 : 0, eta = P['en-eta'] / 100, Q1 = 1000, W = eta * Q1, Q2 = Q1 - W;
        const verdict = !ok ? '—' : eta >= 1 ? 'Impossible' : eta > lim + 1e-9 ? 'Impossible' : eta > lim - 0.005 ? 'Ideal Carnot only' : 'Possible';
        return { T1, T2, ok, lim, Q1, W, Q2, verdict, bad: verdict === 'Impossible' };
      }
      const lim = ok ? T2 / (T1 - T2) : 0, cop = P['en-cop'], Q2 = 1000, W = Q2 / cop, Q1 = Q2 + W;
      const verdict = !ok ? '—' : cop > lim + 1e-9 ? 'Impossible' : cop > lim - 0.05 ? 'Ideal Carnot only' : 'Possible';
      return { T1, T2, ok, lim, Q1, W, Q2, verdict, bad: verdict === 'Impossible' };
    }
    function draw(ctx, w, h) {
      if (!P) return;
      const C = Sim.C, s = solve(), eng = P.mode === 'engine';
      const bw = Math.min(w - 40, 340), bx = (w - bw) / 2 - 40, bh = 46, cx = bx + bw / 2, cy = h / 2, r = 34;
      ctx.save();
      ctx.fillStyle = C.coralSoft; ctx.strokeStyle = C.coral; ctx.lineWidth = 1.5;
      Sim.rrect(ctx, bx, 14, bw, bh, 10); ctx.fill(); ctx.stroke();
      ctx.fillStyle = C.waterSoft; ctx.strokeStyle = C.water;
      Sim.rrect(ctx, bx, h - 14 - bh, bw, bh, 10); ctx.fill(); ctx.stroke();
      ctx.restore();
      Sim.text(ctx, `Hot reservoir  T₁ = ${s.T1} K`, cx, 14 + bh / 2, { size: 13.5, weight: 700, align: 'center', color: C.coral });
      Sim.text(ctx, `Cold ${eng ? 'sink' : 'inside'}  T₂ = ${s.T2} K`, cx, h - 14 - bh / 2, { size: 13.5, weight: 700, align: 'center', color: C.water });
      const big = Math.max(s.Q1, s.Q2, s.W, 1);
      const wd = q => 3 + 15 * Math.min(1, q / big);
      const top = 14 + bh + 4, bot = h - 14 - bh - 4;
      if (eng) {
        Sim.arrow(ctx, cx, top, cx, cy - r - 2, { color: C.coral, width: wd(s.Q1), head: 12 + wd(s.Q1) * 0.6 });
        if (s.Q2 > 0.5) Sim.arrow(ctx, cx, cy + r + 2, cx, bot, { color: C.water, width: wd(s.Q2), head: 12 + wd(s.Q2) * 0.6 });
        if (s.W > 0.5) Sim.arrow(ctx, cx + r + 2, cy, Math.min(w - 20, cx + r + 120), cy, { color: C.teal, width: wd(s.W), head: 12 + wd(s.W) * 0.6 });
        Sim.text(ctx, `Q₁ = ${fx(s.Q1, 0)} J`, cx + 14, (top + cy - r) / 2, { size: 12.5, weight: 700 });
        Sim.text(ctx, `Q₂ = ${fx(s.Q2, 0)} J`, cx + 14, (cy + r + bot) / 2, { size: 12.5, weight: 700 });
        Sim.text(ctx, `W = ${fx(s.W, 0)} J`, cx + r + 10, cy - 20, { size: 12.5, weight: 700, color: C.teal });
      } else {
        Sim.arrow(ctx, cx, bot, cx, cy + r + 2, { color: C.water, width: wd(s.Q2), head: 12 + wd(s.Q2) * 0.6 });
        Sim.arrow(ctx, cx, cy - r - 2, cx, top, { color: C.coral, width: wd(s.Q1), head: 12 + wd(s.Q1) * 0.6 });
        Sim.arrow(ctx, Math.min(w - 20, cx + r + 120), cy, cx + r + 2, cy, { color: C.teal, width: wd(s.W), head: 12 + wd(s.W) * 0.6 });
        Sim.text(ctx, `Q₁ = ${fx(s.Q1, 0)} J`, cx + 14, (top + cy - r) / 2, { size: 12.5, weight: 700 });
        Sim.text(ctx, `Q₂ = ${fx(s.Q2, 0)} J`, cx + 14, (cy + r + bot) / 2, { size: 12.5, weight: 700 });
        Sim.text(ctx, `W = ${fx(s.W, 0)} J`, cx + r + 10, cy - 20, { size: 12.5, weight: 700, color: C.teal });
      }
      ctx.save(); ctx.fillStyle = s.bad ? C.coral : C.teal; ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill(); ctx.restore();
      Sim.text(ctx, s.bad ? '✗' : eng ? 'engine' : 'fridge', cx, cy, { size: s.bad ? 26 : 12.5, weight: 750, align: 'center', color: '#fff' });
    }
    function update() {
      const s = solve(), eng = P.mode === 'engine';
      root.querySelectorAll('[data-only]').forEach(el => { el.hidden = el.dataset.only !== P.mode; });
      root.querySelector('[data-k="lim"]').textContent = eng ? 'Carnot limit η' : 'Carnot limit β';
      root.querySelector('[data-k="other"]').textContent = eng ? 'Heat to cold sink Q₂' : 'Heat to room Q₁';
      Sim.out(root, 'lim', !s.ok ? '—' : eng ? `${fx(s.lim * 100, 1)} %` : fx(s.lim, 2));
      Sim.out(root, 'w', `${fx(s.W, 0)} J`);
      Sim.out(root, 'other', `${fx(eng ? s.Q2 : s.Q1, 0)} J`);
      Sim.out(root, 'verdict', s.verdict);
      let note;
      if (!s.ok) note = 'The cold reservoir must be colder than the hot one. Lower T₂ or raise T₁.';
      else if (eng) note = P['en-eta'] >= 100 ? 'A 100 % engine would turn all its heat into work. The Kelvin–Planck statement forbids this.'
        : s.bad ? `This engine claims more than the Carnot limit of ${fx(s.lim * 100, 1)} %, so the second law says it cannot exist.`
        : `Per 1000 J taken from the hot reservoir, ${fx(s.W, 0)} J becomes work and ${fx(s.Q2, 0)} J must be rejected. To raise the limit, widen the gap between T₁ and T₂.`;
      else note = s.bad ? `No refrigerator between these temperatures can beat β = ${fx(s.lim, 2)} (Clausius statement).`
        : `To pull 1000 J out of the cold inside, at least ${fx(1000 / s.lim, 0)} J of work is needed. A smaller temperature gap makes the job easier.`;
      Sim.out(root, 'note', note);
    }
    const st = Sim.stage(host, { aspect: 16 / 10, minH: 320, maxH: 400, draw });
    P = Sim.controls(root, v => { P = v; update(); st.redraw(); });
    update(); st.redraw();
  }

  /* =================================================================
     Page helpers: saved ticks, self-marking, reveal-all
     ================================================================= */
  const KEY = 'week-thermal-v1:';
  const load = k => { try { return JSON.parse(localStorage.getItem(KEY + k)) || {}; } catch (e) { return {}; } };
  const save = (k, v) => { try { localStorage.setItem(KEY + k, JSON.stringify(v)); } catch (e) { /* storage blocked: keep working */ } };

  function initTicks(selector, attr, key, after) {
    const box = document.querySelector(selector); if (!box) return;
    const state = load(key);
    const inputs = [...box.querySelectorAll(`input[${attr}]`)];
    inputs.forEach(inp => {
      inp.checked = !!state[inp.getAttribute(attr)];
      inp.addEventListener('change', () => {
        state[inp.getAttribute(attr)] = inp.checked; if (!inp.checked) delete state[inp.getAttribute(attr)];
        save(key, state); after && after(inputs);
      });
    });
    after && after(inputs);
  }

  function initMarks() {
    const probs = [...document.querySelectorAll('details.prob')];
    const board = document.querySelector('[data-score]');
    if (!probs.length || !board) return;
    const marks = load('marks');
    let onlyRetry = false;
    const refresh = () => {
      let got = 0, retry = 0;
      probs.forEach(d => {
        const m = marks[d.dataset.p];
        d.classList.toggle('got', m === 'got'); d.classList.toggle('retry', m === 'retry');
        d.querySelectorAll('.mark button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.m === m)));
        if (m === 'got') got++; else if (m === 'retry') retry++;
        d.hidden = onlyRetry && m !== 'retry';
      });
      board.querySelector('[data-s="got"]').textContent = got;
      board.querySelector('[data-s="retry"]').textContent = retry;
      board.querySelector('[data-s="left"]').textContent = probs.length - got - retry;
    };
    probs.forEach(d => {
      const row = document.createElement('div');
      row.className = 'mark';
      row.innerHTML = '<button type="button" data-m="got" aria-pressed="false">✓ I got it</button><button type="button" data-m="retry" aria-pressed="false">↻ Retry later</button>';
      d.appendChild(row);
      row.querySelectorAll('button').forEach(b => b.addEventListener('click', () => {
        if (marks[d.dataset.p] === b.dataset.m) delete marks[d.dataset.p]; else marks[d.dataset.p] = b.dataset.m;
        save('marks', marks); refresh();
      }));
    });
    const only = board.querySelector('[data-act="only-retry"]');
    only.addEventListener('click', () => { onlyRetry = !onlyRetry; only.setAttribute('aria-pressed', String(onlyRetry)); refresh(); });
    board.querySelector('[data-act="reset-score"]').addEventListener('click', () => {
      Object.keys(marks).forEach(k => delete marks[k]); save('marks', marks); refresh();
    });
    refresh();
  }

  function initRevealAll() {
    const all = document.querySelector('[data-reveal-all]'); if (!all) return;
    all.addEventListener('click', () => {
      const open = all.getAttribute('aria-pressed') !== 'true';
      document.querySelectorAll('details.ask').forEach(d => { d.open = open; });
      all.setAttribute('aria-pressed', String(open));
      all.textContent = open ? 'Hide every answer' : 'Show every answer';
    });
  }

  function init() {
    initHeatFlow(); initScales(); initGas(); initExpand(); initBimetal(); initWater(); initPV(); initEngine(); initCapLab();
    initTicks('[data-plan]', 'data-day', 'plan');
    initTicks('[data-ready]', 'data-item', 'ready', inputs => {
      const el = document.querySelector('[data-ready-count]');
      if (el) el.textContent = `${inputs.filter(i => i.checked).length} of ${inputs.length} ready.`;
    });
    initMarks(); initRevealAll();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
