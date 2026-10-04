/* =====================================================================
   Fluids I — interactive simulations
   Each sim initialises only when its <figure class="sim" id="…"> exists.
   Uses Sim.stage / Sim.controls / Sim.out from site.js; colours from Sim.C.
   ===================================================================== */
(function () {
  'use strict';
  if (typeof Sim === 'undefined') return;

  const G = 9.8, P0 = 101300;
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const lerp = (a, b, t) => a + (b - a) * t;
  const smooth = t => (t <= 0 ? 0 : t >= 1 ? 1 : t * t * (3 - 2 * t));
  const T = (ctx, s, x, y, o) => Sim.text(ctx, s, x, y, o);

  function rgba(hex, a) {
    hex = (hex || '#3A8CCB').replace('#', '').trim();
    if (hex.length === 3) hex = hex.split('').map(c => c + c).join('');
    const n = parseInt(hex, 16);
    return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`;
  }
  function parts(id) {
    const root = document.getElementById(id);
    if (!root) return null;
    return { root, stageEl: root.querySelector('.sim-stage'), panel: root.querySelector('.sim-panel') };
  }
  function setRange(panel, id, val) {
    const inp = panel.querySelector('#' + id);
    if (!inp) return;
    inp.value = val;
    inp.dispatchEvent(new Event('input'));
  }
  function showMode(panel, mode) {
    panel.querySelectorAll('[data-mode]').forEach(el => {
      el.hidden = el.dataset.mode.split(' ').indexOf(mode) < 0;
    });
  }
  const kPa = p => (Math.abs(p) < 1e4 ? (p / 1000).toFixed(2) : (p / 1000).toFixed(1)) + ' kPa';
  const fix = (x, d) => (+x).toFixed(d);

  /* Text with a letter subscript, e.g. lab(ctx,'F','B',…) → F_B */
  function lab(ctx, base, sub, x, y, o = {}) {
    const size = o.size || 13, wt = o.weight || 650, font = Sim.C.font;
    ctx.save();
    ctx.font = `${wt} ${size}px ${font}`;
    const wb = ctx.measureText(base).width;
    ctx.font = `${wt} ${Math.max(11, size * 0.78)}px ${font}`;
    const ws = ctx.measureText(sub).width;
    const tw = wb + ws + 1;
    let x0 = x;
    if (o.align === 'center') x0 = x - tw / 2; else if (o.align === 'right') x0 = x - tw;
    if (o.bg) { ctx.fillStyle = o.bg; Sim.rrect(ctx, x0 - 4, y - size / 2 - 4, tw + 8, size + 9, 5); ctx.fill(); }
    ctx.fillStyle = o.color || Sim.C.ink;
    ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
    ctx.font = `${wt} ${size}px ${font}`; ctx.fillText(base, x0, y);
    ctx.font = `${wt} ${Math.max(11, size * 0.78)}px ${font}`; ctx.fillText(sub, x0 + wb + 1, y + size * 0.3);
    ctx.restore();
  }

  /* vertical dimension line with end ticks */
  function dim(ctx, x, y1, y2, color) {
    Sim.line(ctx, [[x, y1], [x, y2]], { color, width: 1.3 });
    Sim.line(ctx, [[x - 4, y1], [x + 4, y1]], { color, width: 1.3 });
    Sim.line(ctx, [[x - 4, y2], [x + 4, y2]], { color, width: 1.3 });
  }

  /* simple pointer tracking on a canvas (tap anywhere; drag with mouse/pen) */
  function pointer(st, cb) {
    let down = false;
    st.canvas.addEventListener('pointerdown', e => { down = true; cb(st.toLocal(e), true); });
    window.addEventListener('pointermove', e => { if (down) cb(st.toLocal(e), false); });
    const up = () => { down = false; };
    window.addEventListener('pointerup', up);
    window.addEventListener('pointercancel', up);
  }

  /* ------------------------------------------------------------------
     Flow engine: a pipe with centreline yc(x) and diameter D(x).
     Particles carry a "volume coordinate" u = ∫A ds; every particle
     advances by the SAME Q·dt, so equal volumes cross every section
     per second (continuity is built in, not faked).
     ------------------------------------------------------------------ */
  function buildPath(x0, x1, yc, D, n = 360) {
    const xs = new Float64Array(n + 1), us = new Float64Array(n + 1);
    let u = 0, px = x0, py = yc(x0);
    for (let i = 0; i <= n; i++) {
      const x = x0 + (x1 - x0) * i / n, y = yc(x);
      if (i) { const d = D((x + px) / 2); u += d * d * Math.hypot(x - px, y - py); }
      xs[i] = x; us[i] = u; px = x; py = y;
    }
    return {
      x0, x1, yc, D, total: u,
      xAt(uu) {
        let lo = 0, hi = n;
        while (hi - lo > 1) { const m = (lo + hi) >> 1; if (us[m] <= uu) lo = m; else hi = m; }
        const f = (uu - us[lo]) / ((us[hi] - us[lo]) || 1);
        return xs[lo] + (xs[hi] - xs[lo]) * clamp(f, 0, 1);
      },
    };
  }
  function makeParticles(path, lanes, spacingPx, Dref) {
    const per = Math.max(4, Math.round(path.total / (Dref * Dref * spacingPx)));
    const arr = [];
    lanes.forEach((s, li) => {
      for (let k = 0; k < per; k++) arr.push({ u: ((k + (li % 2) * 0.5) / per) * path.total, s });
    });
    return arr;
  }
  function drawPipe(ctx, path, o = {}) {
    const c = Sim.C, top = [], bot = [], N = 120;
    for (let i = 0; i <= N; i++) {
      const x = path.x0 + (path.x1 - path.x0) * i / N, y = path.yc(x), d = path.D(x) / 2;
      top.push([x, y - d]); bot.push([x, y + d]);
    }
    ctx.save();
    ctx.beginPath();
    top.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]));
    for (let i = bot.length - 1; i >= 0; i--) ctx.lineTo(bot[i][0], bot[i][1]);
    ctx.closePath();
    ctx.fillStyle = o.fill || c.liquid; ctx.fill();
    ctx.restore();
    if (o.lanes) {
      o.lanes.forEach(s => {
        const pts = [];
        for (let i = 0; i <= N; i++) { const x = path.x0 + (path.x1 - path.x0) * i / N; pts.push([x, path.yc(x) + s * path.D(x) / 2]); }
        Sim.line(ctx, pts, { color: rgba(c.water, 0.28), width: 1 });
      });
    }
    Sim.line(ctx, top, { color: c.ink2, width: 3 });
    Sim.line(ctx, bot, { color: c.ink2, width: 3 });
  }
  function drawParticles(ctx, path, ps, col) {
    ctx.save();
    ctx.fillStyle = col || Sim.C.water;
    ps.forEach(p => {
      const x = path.xAt(p.u);
      const y = path.yc(x) + p.s * path.D(x) / 2;
      ctx.beginPath(); ctx.arc(x, y, 2.6, 0, Math.PI * 2); ctx.fill();
    });
    ctx.restore();
  }

  Sim.maps.pctH = v => Math.round(v * 100) + '% of H';
  Sim.maps.spin = v => (Math.abs(v) < 0.001 ? 'none' : (v > 0 ? 'backspin ' : 'topspin ') + Math.round(Math.abs(v) * 100) + '%');
  Sim.maps.ratio = v => v.toFixed(1) + '×';

  /* ==================================================================
     1. Pressure at depth — tank + probe + P–h line
     ================================================================== */
  function simPressure() {
    const p = parts('sim-pressure'); if (!p) return;
    const LQ = {
      water: { rho: 1000, name: 'Water', col: 'water' },
      oil: { rho: 800, name: 'Oil', col: 'amber' },
      sea: { rho: 1030, name: 'Seawater', col: 'teal' },
      hg: { rho: 13600, name: 'Mercury', col: 'muted' },
    };
    let v, st, geo = null;
    const update = () => {
      const L = LQ[v.liq], h = v['pr-h'], pg = L.rho * G * h, P = P0 + pg;
      Sim.out(p.panel, 'P', kPa(P));
      Sim.out(p.panel, 'atm', (P / P0).toFixed(2) + ' atm');
      Sim.out(p.panel, 'gauge', kPa(pg));
      Sim.out(p.panel, 'rho', L.rho + ' kg/m³');
    };
    v = Sim.controls(p.panel, vals => { v = vals; update(); st && st.redraw(); });

    function draw(ctx, w, h) {
      const c = Sim.C, L = LQ[v.liq], col = c[L.col], d = v['pr-h'];
      const narrow = w < 520;
      const tx0 = 14, tw = Math.round(w * (narrow ? 0.44 : 0.42)), tx1 = tx0 + tw;
      const yS = 52, yB = h - 22, pxm = (yB - yS) / 10;
      geo = { tx0, tx1, yS, yB, pxm };
      // liquid with depth shading
      const grd = ctx.createLinearGradient(0, yS, 0, yB);
      const a0 = L.col === 'muted' ? 0.32 : 0.14, a1 = L.col === 'muted' ? 0.6 : 0.42;
      grd.addColorStop(0, rgba(col, a0)); grd.addColorStop(1, rgba(col, a1));
      ctx.fillStyle = grd; ctx.fillRect(tx0, yS, tw, yB - yS);
      Sim.line(ctx, [[tx0, yS], [tx1, yS]], { color: rgba(col, 0.9), width: 2 });
      Sim.line(ctx, [[tx0, yS - 30], [tx0, yB], [tx1, yB], [tx1, yS - 30]], { color: c.ink2, width: 3 });
      // atmosphere pushing on the surface
      [0.18, 0.82].forEach(k => Sim.arrow(ctx, tx0 + tw * k, yS - 30, tx0 + tw * k, yS - 4, { color: c.muted, width: 1.5, head: 7 }));
      lab(ctx, 'P', '0', tx0 + tw * 0.5, yS - 18, { color: c.ink2, size: 13, align: 'center' });
      T(ctx, L.name, tx1 - 6, yB - 12, { size: 11.5, color: c.ink2, align: 'right', weight: 650 });
      // depth scale between tank and graph
      for (let m = 0; m <= 10; m += 2) {
        const y = yS + m * pxm;
        Sim.line(ctx, [[tx1 + 2, y], [tx1 + 7, y]], { color: c.muted, width: 1 });
        T(ctx, String(m), tx1 + 10, y, { size: 11, color: c.muted, mono: true });
      }
      T(ctx, 'h (m)', tx1 + 4, yS - 30, { size: 11, color: c.muted, weight: 600 });
      // probe
      const px = tx0 + tw * 0.64, py = yS + d * pxm;
      const Pmax = P0 + L.rho * G * 10, P = P0 + L.rho * G * d;
      const la = 8 + 20 * (P / Pmax), r0 = 7;
      for (let k = 0; k < 8; k++) {
        const a = k * Math.PI / 4, ca = Math.cos(a), sa = Math.sin(a);
        Sim.arrow(ctx, px + ca * (r0 + la + 2), py + sa * (r0 + la + 2), px + ca * (r0 + 1), py + sa * (r0 + 1), { color: c.coral, width: 1.8, head: 7 });
      }
      ctx.save(); ctx.fillStyle = c.surface; ctx.strokeStyle = c.ink; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(px, py, r0, 0, Math.PI * 2); ctx.fill(); ctx.stroke(); ctx.restore();
      // depth bracket
      if (d > 0.05) {
        dim(ctx, tx0 + 10, yS, py, c.ink2);
        if (d >= 0.8) T(ctx, d.toFixed(1) + ' m', tx0 + 16, (yS + py) / 2, { size: 11.5, mono: true, color: c.ink, bg: 'rgba(255,255,255,0.85)' });
      }
      // graph: depth down (aligned with the tank), pressure across
      const gx = tx1 + 40, gx1 = w - 14, gw = gx1 - gx;
      const Pax = v.liq === 'hg' ? 1500e3 : 250e3;
      const X = PP => gx + PP / Pax * gw;
      Sim.line(ctx, [[gx, yS], [gx, yB]], { color: c.ink2, width: 1.5 });
      Sim.line(ctx, [[gx, yS], [gx1, yS]], { color: c.ink2, width: 1.5 });
      const ticks = v.liq === 'hg' ? [0, 500e3, 1000e3, 1500e3] : [0, 100e3, 200e3];
      ticks.forEach(tk => {
        Sim.line(ctx, [[X(tk), yS], [X(tk), yS - 4]], { color: c.muted, width: 1 });
        T(ctx, String(tk / 1000), X(tk), yS - 12, { size: 11, color: c.muted, align: tk === 0 ? 'left' : 'center', mono: true });
      });
      T(ctx, 'P (kPa) →', gx1, yS - 32, { size: 11, color: c.muted, align: 'right', weight: 600 });
      // gauge wedge + line
      const xP0 = X(P0), xEnd = X(P0 + L.rho * G * 10);
      ctx.save(); ctx.fillStyle = rgba(c.coral, 0.10);
      ctx.beginPath(); ctx.moveTo(xP0, yS); ctx.lineTo(xEnd, yB); ctx.lineTo(xP0, yB); ctx.closePath(); ctx.fill(); ctx.restore();
      Sim.line(ctx, [[xP0, yS], [xP0, yB]], { color: c.muted, width: 1, dash: [3, 4] });
      Sim.line(ctx, [[xP0, yS], [xEnd, yB]], { color: c.accent, width: 2.5 });
      lab(ctx, 'P', '0', xP0 + 4, yS + 12, { size: 12, color: c.ink2 });
      if (xEnd - xP0 > 40) T(ctx, 'ρgh', xP0 + 6, yB - 12, { size: 11.5, color: c.coral, weight: 650 });
      // current point
      const xd = X(P);
      Sim.line(ctx, [[px + r0 + 30, py], [xd, py]], { color: c.muted, width: 1, dash: [4, 4] });
      ctx.save(); ctx.fillStyle = c.accent; ctx.beginPath(); ctx.arc(xd, py, 5, 0, Math.PI * 2); ctx.fill(); ctx.restore();
      const lbl = (P / 1000).toFixed(0) + ' kPa';
      const right = xd + 70 < gx1;
      T(ctx, lbl, right ? xd + 8 : xd - 8, py + (d > 9 ? -14 : 14), { size: 11.5, mono: true, color: c.accent, align: right ? 'left' : 'right', bg: 'rgba(255,255,255,0.85)' });
    }
    st = Sim.stage(p.stageEl, { aspect: 16 / 10, minH: 280, maxH: 430, draw });
    pointer(st, (pt) => {
      if (!geo) return;
      if (pt.x < geo.tx0 - 10 || pt.x > geo.tx1 + 10) return;
      const d = clamp((pt.y - geo.yS) / geo.pxm, 0, 10);
      setRange(p.panel, 'pr-h', d.toFixed(1));
    });
  }

  /* ==================================================================
     1b. Hydrostatic paradox — three vessels, same height
     ================================================================== */
  function simParadox() {
    const p = parts('sim-paradox'); if (!p) return;
    const Hm = 0.30; // vessel height represented (m)
    const shapes = [
      { name: 'A · straight', f: () => 1 },
      { name: 'B · flared', f: e => 1 + 1.3 * e },
      { name: 'C · narrow neck', f: e => (e < 0.3 ? 1 : e < 0.42 ? lerp(1, 0.32, (e - 0.3) / 0.12) : 0.32) },
    ];
    let v, st;
    const weightFactor = (s, eh) => { // V / (A_base·h) for a round vessel
      if (eh <= 0) return 1;
      let acc = 0; const n = 200;
      for (let i = 0; i < n; i++) { const e = (i + 0.5) / n * eh; const r = s.f(e); acc += r * r; }
      return acc / n;
    };
    const update = () => {
      const h = v['px-h'], P = 1000 * G * h;
      Sim.out(p.panel, 'P', P.toFixed(0) + ' Pa');
      Sim.out(p.panel, 'F', (P * 20e-4).toFixed(2) + ' N');
    };
    v = Sim.controls(p.panel, vals => { v = vals; update(); st && st.redraw(); });
    function draw(ctx, w, h) {
      const c = Sim.C, cw = w / 3, yBase = h - 50, Hv = yBase - 30;
      const b = Math.min(cw * 0.34, 58), eh = v['px-h'] / Hm, yL = yBase - eh * Hv;
      shapes.forEach((s, i) => {
        const cx = cw * (i + 0.5), left = [], right = [];
        for (let k = 0; k <= 60; k++) {
          const e = k / 60, half = b * s.f(e) / 2, y = yBase - e * Hv;
          left.push([cx - half, y]); right.push([cx + half, y]);
        }
        // liquid
        ctx.save();
        ctx.beginPath();
        left.forEach((q, k) => k ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]));
        for (let k = right.length - 1; k >= 0; k--) ctx.lineTo(right[k][0], right[k][1]);
        ctx.closePath(); ctx.clip();
        ctx.fillStyle = c.liquid; ctx.fillRect(cx - cw / 2, yL, cw, yBase - yL);
        ctx.restore();
        Sim.line(ctx, left, { color: c.ink2, width: 2.5 });
        Sim.line(ctx, right, { color: c.ink2, width: 2.5 });
        Sim.line(ctx, [[cx - b / 2 - 1, yBase], [cx + b / 2 + 1, yBase]], { color: c.ink2, width: 3 });
        // equal pressure arrows on the base
        const la = 6 + 26 * eh;
        [-0.28, 0, 0.28].forEach(k => Sim.arrow(ctx, cx + k * b, yBase - 2 - la, cx + k * b, yBase - 2, { color: c.coral, width: 1.8, head: 6 }));
        T(ctx, s.name, cx, 12, { size: 11.5, color: c.ink2, align: 'center', weight: 650 });
        T(ctx, 'P same', cx, yBase + 15, { size: 11.5, color: c.coral, align: 'center', weight: 650 });
        T(ctx, 'W = ' + weightFactor(s, eh).toFixed(2) + ' F', cx, yBase + 33, { size: 11.5, color: c.ink, align: 'center', mono: true });
      });
      Sim.line(ctx, [[6, yL], [w - 6, yL]], { color: c.water, width: 1.2, dash: [5, 5] });
      T(ctx, 'same h', w - 8, yL - 9, { size: 11, color: c.water, align: 'right', weight: 650 });
    }
    st = Sim.stage(p.stageEl, { aspect: 16 / 8, minH: 240, maxH: 330, draw });
  }

  /* ==================================================================
     2. U-tube: open manometer / two immiscible liquids
     ================================================================== */
  function simUtube() {
    const p = parts('sim-utube'); if (!p) return;
    let v, st;
    const update = () => {
      showMode(p.panel, v.umode);
      if (v.umode === 'mano') {
        const Pg = v['ut-P'] * 1000 - P0, dh = Pg / (13600 * G) * 100;
        Sim.out(p.panel, 'gauge', kPa(Pg));
        Sim.out(p.panel, 'dh', dh.toFixed(1) + ' cm');
        Sim.out(p.panel, 'abs', (76 + dh).toFixed(1) + ' cm Hg');
      } else {
        const ho = v['ut-ho'], hw = ho * v['ut-rho'] / 1000;
        Sim.out(p.panel, 'hw', hw.toFixed(2) + ' cm');
        Sim.out(p.panel, 'diff', (ho - hw).toFixed(2) + ' cm');
      }
    };
    v = Sim.controls(p.panel, vals => { v = vals; update(); st && st.redraw(); });

    function tubePath(ctx, xL, xR, yTop, yBend) {
      const r = (xR - xL) / 2;
      ctx.beginPath();
      ctx.moveTo(xL, yTop); ctx.lineTo(xL, yBend);
      ctx.arc(xL + r, yBend, r, Math.PI, 0, true);
      ctx.lineTo(xR, yTop);
    }
    // stroke the liquid portion: from level yA on left arm, round the bend, up to level yB on right arm
    function fillU(ctx, xL, xR, yA, yB, yBend, tw, color) {
      const r = (xR - xL) / 2;
      ctx.save();
      ctx.strokeStyle = color; ctx.lineWidth = tw; ctx.lineCap = 'butt';
      ctx.beginPath();
      ctx.moveTo(xL, yA); ctx.lineTo(xL, yBend);
      ctx.arc(xL + r, yBend, r, Math.PI, 0, true);
      ctx.lineTo(xR, yB);
      ctx.stroke(); ctx.restore();
    }
    function draw(ctx, w, h) {
      const c = Sim.C, mano = v.umode === 'mano';
      const cx = mano ? w * 0.56 : w * 0.5;
      const dArm = Math.min(w * 0.22, 110), tw = 16;
      const xL = cx - dArm / 2, xR = cx + dArm / 2;
      const yT = 44, yBend = h - 36 - dArm / 2;
      const s = Math.min(6.5, (yBend - yT - 14) / 26);
      const y0 = yT + 14 + 13 * s;
      // tube outline
      ctx.save(); ctx.lineCap = 'butt';
      tubePath(ctx, xL, xR, yT, yBend); ctx.strokeStyle = c.ink2; ctx.lineWidth = tw + 5; ctx.stroke();
      tubePath(ctx, xL, xR, yT, yBend); ctx.strokeStyle = '#FFFFFF'; ctx.lineWidth = tw; ctx.stroke();
      ctx.restore();
      const hgCol = 'rgba(115,124,145,0.75)';
      if (mano) {
        const Pg = v['ut-P'] * 1000 - P0, dh = Pg / (13600 * G) * 100;
        const yLl = y0 + dh / 2 * s, yRl = y0 - dh / 2 * s;
        // gas bulb + connector + gas in left arm
        const bx = Math.max(34, xL - 72), by = yT + 6, br = 24;
        ctx.save();
        ctx.fillStyle = rgba(c.coral, 0.16); ctx.strokeStyle = c.ink2; ctx.lineWidth = 2.5;
        ctx.beginPath(); ctx.arc(bx, by, br, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
        ctx.restore();
        Sim.line(ctx, [[bx + br, by - 5], [xL - tw / 2 - 2, by - 5]], { color: c.ink2, width: 2.5 });
        Sim.line(ctx, [[bx + br, by + 5], [xL - tw / 2 - 2, by + 5]], { color: c.ink2, width: 2.5 });
        ctx.save(); ctx.fillStyle = rgba(c.coral, 0.16);
        ctx.fillRect(bx + br - 2, by - 4, xL - bx - br, 8);
        ctx.fillRect(xL - tw / 2, by - 4, tw, yLl - by + 4);
        ctx.restore();
        // close the left arm top (sealed to gas line)
        Sim.line(ctx, [[xL - tw / 2 - 2, yT - 2], [xL + tw / 2 + 2, yT - 2]], { color: c.ink2, width: 2.5 });
        T(ctx, 'gas', bx, by, { size: 12, align: 'center', weight: 650, color: c.coral });
        T(ctx, v['ut-P'].toFixed(0) + ' kPa', bx, by + br + 12, { size: 11, align: 'center', mono: true, color: c.ink2 });
        fillU(ctx, xL, xR, yLl, yRl, yBend, tw, hgCol);
        T(ctx, 'open: P₀', xR, yT - 14, { size: 11.5, align: 'center', color: c.ink2, weight: 650 });
        T(ctx, 'mercury', xR + tw / 2 + 8, yBend + 4, { size: 11, color: c.muted, weight: 650 });
        // level lines + h bracket
        const bxk = xR + tw / 2 + 12;
        Sim.line(ctx, [[xL - tw / 2, yLl], [bxk + 4, yLl]], { color: c.muted, width: 1, dash: [3, 3] });
        Sim.line(ctx, [[xR - tw / 2, yRl], [bxk + 4, yRl]], { color: c.muted, width: 1, dash: [3, 3] });
        if (Math.abs(dh) > 0.3) dim(ctx, bxk, yLl, yRl, c.accent);
        T(ctx, 'h = ' + dh.toFixed(1) + ' cm', bxk + 8, (yLl + yRl) / 2, { size: 11.5, mono: true, color: c.accent, weight: 650 });
        T(ctx, dh >= 0 ? 'gas above P₀: open side higher' : 'gas below P₀: open side lower', w / 2, h - 10, { size: 11.5, color: c.ink2, align: 'center' });
      } else {
        const ho = v['ut-ho'], hw = ho * v['ut-rho'] / 1000;
        const delta = hw / 2;
        const yI = y0 + delta * s, yW = y0 - delta * s, yO = yI - ho * s;
        fillU(ctx, xL, xR, yI, yW, yBend, tw, 'rgba(58,140,203,0.45)');
        if (ho > 0) {
          ctx.save(); ctx.fillStyle = rgba(c.amber, 0.55);
          ctx.fillRect(xL - tw / 2, yO, tw, yI - yO); ctx.restore();
        }
        T(ctx, 'open', xL, yT - 14, { size: 11, align: 'center', color: c.muted });
        T(ctx, 'open', xR, yT - 14, { size: 11, align: 'center', color: c.muted });
        // same-level line through the interface
        Sim.line(ctx, [[xL - 40, yI], [xR + 40, yI]], { color: c.coral, width: 1.3, dash: [5, 4] });
        ctx.save(); ctx.fillStyle = c.coral;
        [[xL, yI], [xR, yI]].forEach(q => { ctx.beginPath(); ctx.arc(q[0], q[1], 3.5, 0, Math.PI * 2); ctx.fill(); });
        ctx.restore();
        T(ctx, 'A', xL - 14, yI + 11, { size: 12, color: c.coral, weight: 700, align: 'center' });
        T(ctx, 'B', xR + 14, yI + 11, { size: 12, color: c.coral, weight: 700, align: 'center' });
        // brackets
        if (ho > 0.4) {
          const xl = xL - tw / 2 - 12;
          dim(ctx, xl, yO, yI, c.amber);
          T(ctx, 'oil h₁', xl - 6, (yO + yI) / 2 - 7, { size: 11.5, align: 'right', color: c.amber, weight: 650 });
          T(ctx, ho.toFixed(1) + ' cm', xl - 6, (yO + yI) / 2 + 8, { size: 11, align: 'right', color: c.amber, mono: true });
          const xr = xR + tw / 2 + 12;
          Sim.line(ctx, [[xR - tw / 2, yO], [xR + tw / 2 + 16, yO]], { color: c.muted, width: 1, dash: [3, 3] });
          dim(ctx, xr, yW, yI, c.water);
          T(ctx, 'water h₂', xr + 6, (yW + yI) / 2 - 7, { size: 11.5, color: c.water, weight: 650 });
          T(ctx, hw.toFixed(2) + ' cm', xr + 6, (yW + yI) / 2 + 8, { size: 11, color: c.water, mono: true });
        }
        T(ctx, 'A, B: same level, same liquid → equal pressure', w / 2, h - 10, { size: 11.5, color: c.ink2, align: 'center' });
      }
    }
    st = Sim.stage(p.stageEl, { aspect: 16 / 10, minH: 290, maxH: 420, draw });
  }

  /* ==================================================================
     3. Hydraulic lift
     ================================================================== */
  function simHydraulic() {
    const p = parts('sim-hydraulic'); if (!p) return;
    let v, st, play = false, x1 = 12;
    const btn = p.panel.querySelector('[data-act="play"]');
    const xInp = p.panel.querySelector('#hy-x');
    const xOut = p.panel.querySelector('output[data-for="hy-x"]');
    const calc = () => {
      const A1 = Math.PI * Math.pow(v['hy-d1'] / 200, 2), A2 = Math.PI * Math.pow(v['hy-d2'] / 200, 2);
      const F1 = v['hy-F'], P = F1 / A1, F2 = P * A2, x2 = x1 * A1 / A2;
      return { A1, A2, F1, P, F2, x2, ratio: A2 / A1 };
    };
    const update = () => {
      const k = calc();
      Sim.out(p.panel, 'ratio', '× ' + k.ratio.toFixed(1));
      Sim.out(p.panel, 'P', kPa(k.P));
      Sim.out(p.panel, 'F2', k.F2 < 1e4 ? k.F2.toFixed(0) + ' N' : Sim.sci(k.F2, 2) + ' N');
      Sim.out(p.panel, 'x2', (k.x2 * 10).toFixed(k.x2 < 1 ? 2 : 1) + ' mm');
      Sim.out(p.panel, 'win', (k.F1 * x1 / 100).toFixed(2) + ' J');
      Sim.out(p.panel, 'wout', (k.F2 * k.x2 / 100).toFixed(2) + ' J');
    };
    v = Sim.controls(p.panel, vals => { v = vals; if (!play) x1 = vals['hy-x']; update(); st && st.redraw(); });
    if (btn) btn.addEventListener('click', () => {
      if (Sim.reduced) { setRange(p.panel, 'hy-x', 20); return; }
      play = !play; btn.textContent = play ? 'Stop' : 'Animate push';
      btn.setAttribute('aria-pressed', play ? 'true' : 'false');
    });
    function draw(ctx, w, h, t) {
      const c = Sim.C;
      if (play) {
        x1 = 15 - 15 * Math.cos(t * 1.3);
        xInp.value = x1.toFixed(1);
        if (xOut) xOut.textContent = x1.toFixed(1) + ' cm';
        update();
      }
      const k = calc();
      const yG = h - 26, yPipeBot = yG - 6, yPipeTop = yPipeBot - 20, yCylTop = 70;
      const yRest = Math.max(118, h * 0.44);
      const s = Math.min(3.2, (yPipeTop - yRest - 8) / 30);
      const kd = Math.min(w * 0.40, 270) / 30;
      const ws = Math.max(9, v['hy-d1'] * kd), wb = Math.max(ws + 6, v['hy-d2'] * kd);
      const xs = Math.max(ws / 2 + 54, w * 0.2), xb = Math.min(w - wb / 2 - 26, w * 0.66);
      const y1 = yRest + x1 * s, y2 = yRest - k.x2 * s;
      // liquid
      ctx.save(); ctx.fillStyle = c.liquid; ctx.beginPath();
      ctx.rect(xs - ws / 2, y1, ws, yPipeBot - y1);
      ctx.rect(xb - wb / 2, y2, wb, yPipeBot - y2);
      ctx.rect(xs, yPipeTop, xb - xs, yPipeBot - yPipeTop);
      ctx.fill('nonzero'); ctx.restore();
      // walls
      Sim.line(ctx, [[xs - ws / 2, yCylTop], [xs - ws / 2, yPipeBot], [xb + wb / 2, yPipeBot], [xb + wb / 2, yCylTop - 20]], { color: c.ink2, width: 3 });
      Sim.line(ctx, [[xs + ws / 2, yCylTop], [xs + ws / 2, yPipeTop], [xb - wb / 2, yPipeTop], [xb - wb / 2, yCylTop - 20]], { color: c.ink2, width: 3 });
      // rest line
      Sim.line(ctx, [[xs - ws / 2 - 6, yRest], [xb + wb / 2 + 8, yRest]], { color: c.muted, width: 1, dash: [4, 4] });
      // small piston + rod + F1
      ctx.save(); ctx.fillStyle = c.ink2;
      ctx.fillRect(xs - ws / 2, y1 - 7, ws, 7);
      ctx.fillRect(xs - 1.5, y1 - 44, 3, 37);
      ctx.fillRect(xs - 12, y1 - 48, 24, 5);
      ctx.restore();
      Sim.arrow(ctx, xs, y1 - 92, xs, y1 - 52, { color: c.coral, width: 2.5 });
      lab(ctx, 'F', '1', xs + 16, y1 - 84, { color: c.coral, size: 13 });
      T(ctx, k.F1.toFixed(0) + ' N', xs + 16, y1 - 68, { size: 11, mono: true, color: c.coral });
      // x1 bracket
      if (x1 > 1) { dim(ctx, xs - ws / 2 - 14, yRest, y1, c.coral); lab(ctx, 'x', '1', xs - ws / 2 - 20, (yRest + y1) / 2, { size: 12, color: c.coral, align: 'right' }); }
      // big piston + load
      ctx.save(); ctx.fillStyle = c.ink2; ctx.fillRect(xb - wb / 2, y2 - 7, wb, 7); ctx.restore();
      const lw = Math.max(46, wb * 0.72), lh = 30;
      ctx.save(); ctx.fillStyle = c.indigoSoft; ctx.strokeStyle = c.indigo; ctx.lineWidth = 2;
      Sim.rrect(ctx, xb - lw / 2, y2 - 7 - lh, lw, lh, 5); ctx.fill(); ctx.stroke(); ctx.restore();
      T(ctx, 'load', xb, y2 - 7 - lh / 2, { size: 11.5, align: 'center', color: c.indigo, weight: 650 });
      Sim.arrow(ctx, xb, y2 - 9 - lh, xb, y2 - 9 - lh - 36, { color: c.green, width: 2.5 });
      lab(ctx, 'F', '2', xb - 8, y2 - 9 - lh - 26, { color: c.green, size: 13, align: 'right' });
      T(ctx, k.F2 < 1e4 ? k.F2.toFixed(0) + ' N' : Sim.sci(k.F2, 1) + ' N', xb - 8, y2 - 9 - lh - 10, { size: 11, mono: true, color: c.green, align: 'right' });
      // x2 bracket (tiny!)
      const bx2 = xb + wb / 2 + 12;
      if (k.x2 * s > 2) dim(ctx, bx2, y2, yRest, c.green);
      // labels under cylinders
      lab(ctx, 'd', '1', xs - 2, yG + 12, { size: 12, color: c.ink2, align: 'right' });
      T(ctx, '= ' + v['hy-d1'].toFixed(1) + ' cm', xs, yG + 12, { size: 11.5, color: c.ink2, mono: true });
      lab(ctx, 'd', '2', xb - 2, yG + 12, { size: 12, color: c.ink2, align: 'right' });
      T(ctx, '= ' + v['hy-d2'].toFixed(1) + ' cm', xb, yG + 12, { size: 11.5, color: c.ink2, mono: true });
      T(ctx, xb - wb / 2 - xs > 230 ? 'same pressure everywhere in the liquid' : 'same P throughout', (xs + ws / 2 + xb - wb / 2) / 2, yPipeTop - 10, { size: 11, color: c.water, align: 'center', weight: 600 });
      T(ctx, 'force × ' + k.ratio.toFixed(1) + '   distance ÷ ' + k.ratio.toFixed(1), w / 2, 14, { size: 12, color: c.ink, align: 'center', weight: 650 });
    }
    st = Sim.stage(p.stageEl, { aspect: 4 / 3, minH: 300, maxH: 440, draw, animate: true });
  }

  /* ==================================================================
     4. Floating lab — damped settling, one or two liquids
     ================================================================== */
  function simFloat() {
    const p = parts('sim-float'); if (!p) return;
    let v, st;
    const S = { y: -0.8, vel: 0 }; // y = depth of block bottom below surface, in block heights
    const IF = 1.5; // interface depth (two-liquid mode) in block heights
    const floorD = () => (v.fmode === 'two' ? 3.5 : 3.1);
    const layers = () => (v.fmode === 'two'
      ? [{ a: 0, b: IF, rho: v['fl-r1'] }, { a: IF, b: 99, rho: v['fl-r2'] }]
      : [{ a: 0, b: 99, rho: v['fl-rl'] }]);
    const FB = y => layers().reduce((sum, L) => sum + L.rho * Math.max(0, Math.min(y, L.b) - Math.max(y - 1, L.a)), 0);
    const eq = () => {
      const rb = v['fl-rb'];
      if (v.fmode === 'two') {
        const r1 = v['fl-r1'], r2 = v['fl-r2'];
        if (rb < r1) return { y: rb / r1, st: 'floats in upper liquid' };
        if (rb < r2) return { y: IF + (rb - r1) / (r2 - r1), st: 'rests at the interface' };
        return { y: floorD(), st: 'sinks to the bottom' };
      }
      const rl = v['fl-rl'];
      if (rb < rl) return { y: rb / rl, st: 'floats' };
      if (rb === rl) return { y: Math.max(1, Math.min(S.y, floorD())), st: 'floats anywhere (neutral)' };
      return { y: floorD(), st: 'sinks' };
    };
    const update = () => {
      showMode(p.panel, v.fmode);
      const rb = v['fl-rb'], e = eq();
      Sim.out(p.panel, 'status', e.st);
      let sub, fbw, app;
      if (v.fmode === 'two') {
        const r1 = v['fl-r1'], r2 = v['fl-r2'];
        sub = rb < r1 ? rb / r1 : 1;
        fbw = rb < r2 ? 1 : (r2 / rb);
        app = rb < r2 ? 0 : 1 - r2 / rb;
        const lower = rb < r1 ? 0 : rb < r2 ? (rb - r1) / (r2 - r1) : 1;
        Sim.out(p.panel, 'lower', Math.round(lower * 100) + '%');
      } else {
        const rl = v['fl-rl'];
        sub = rb < rl ? rb / rl : 1;
        fbw = rb <= rl ? 1 : rl / rb;
        app = rb <= rl ? 0 : 1 - rl / rb;
      }
      Sim.out(p.panel, 'sub', Math.round(sub * 100) + '%');
      Sim.out(p.panel, 'fbw', fbw.toFixed(2));
      Sim.out(p.panel, 'app', app === 0 ? '0 (floats)' : app.toFixed(2) + ' W');
    };
    v = Sim.controls(p.panel, vals => { v = vals; update(); if (Sim.reduced) S.y = eq().y; st && st.redraw(); });
    const drop = p.panel.querySelector('[data-act="drop"]');
    if (drop) drop.addEventListener('click', () => { S.y = -0.9; S.vel = 0; if (Sim.reduced) S.y = eq().y; st && st.redraw(); });
    if (Sim.reduced) S.y = eq().y;

    function step(dt) {
      const rb = v['fl-rb'], gs = 22, cdamp = 4.2, n = 6;
      for (let i = 0; i < n; i++) {
        const h = dt / n;
        const inLiquid = clamp(S.y, 0, 1);
        const acc = gs * (1 - FB(S.y) / rb) - cdamp * S.vel * (0.25 + inLiquid);
        S.vel += acc * h; S.y += S.vel * h;
        const fd = floorD();
        if (S.y >= fd) { S.y = fd; if (S.vel > 0) S.vel = 0; }
      }
    }
    function draw(ctx, w, h, t, dt) {
      const c = Sim.C;
      if (!Sim.reduced && dt) step(dt);
      const L = Math.min(h * 0.155, 56), yS = 58, fd = floorD();
      const cwid = Math.min(w * 0.7, 420), cx = w / 2, x0 = cx - cwid / 2, x1 = cx + cwid / 2;
      const yF = yS + fd * L;
      // block (drawn first so the liquid tints the submerged part)
      const rb = v['fl-rb'], bw = L * 1.4, yTop = yS + (S.y - 1) * L;
      ctx.save();
      ctx.fillStyle = rgba(c.amber, clamp(0.25 + 0.6 * rb / 2000, 0.25, 0.85));
      ctx.strokeStyle = c.amber; ctx.lineWidth = 2;
      Sim.rrect(ctx, cx - bw / 2, yTop, bw, L, 4); ctx.fill(); ctx.stroke();
      ctx.restore();
      // liquids
      if (v.fmode === 'two') {
        ctx.save();
        ctx.fillStyle = rgba(c.amber, 0.18); ctx.fillRect(x0, yS, cwid, IF * L);
        ctx.fillStyle = rgba(c.water, 0.26); ctx.fillRect(x0, yS + IF * L, cwid, yF - yS - IF * L);
        ctx.restore();
        Sim.line(ctx, [[x0, yS + IF * L], [x1, yS + IF * L]], { color: rgba(c.water, 0.7), width: 1.5 });
        T(ctx, 'ρ₁ = ' + v['fl-r1'], x0 + 8, yS + 13, { size: 11.5, color: c.amber, mono: true });
        T(ctx, 'ρ₂ = ' + v['fl-r2'], x0 + 8, yS + IF * L + 13, { size: 11.5, color: c.water, mono: true });
      } else {
        ctx.save(); ctx.fillStyle = rgba(c.water, 0.22); ctx.fillRect(x0, yS, cwid, yF - yS); ctx.restore();
        T(ctx, 'ρ = ' + v['fl-rl'], x0 + 8, yS + 13, { size: 11.5, color: c.water, mono: true });
      }
      Sim.line(ctx, [[x0, yS], [x1, yS]], { color: rgba(c.water, 0.85), width: 2 });
      Sim.line(ctx, [[x0, yS - 40], [x0, yF], [x1, yF], [x1, yS - 40]], { color: c.ink2, width: 3 });
      T(ctx, 'ρ = ' + rb, cx, yTop + L / 2, { size: 11.5, align: 'center', color: c.ink, mono: true, weight: 600 });
      // forces (per unit volume × g, drawn to scale)
      const kA = (L * 2) / 2000, fb = FB(S.y), cyB = yTop + L / 2;
      const wl = Math.min(kA * rb, h - 24 - cyB);
      Sim.arrow(ctx, cx + bw / 2 + 12, cyB, cx + bw / 2 + 12, cyB + wl, { color: c.coral, width: 2.5 });
      T(ctx, 'W', cx + bw / 2 + 12, cyB + wl + 11, { size: 12.5, color: c.coral, weight: 700, align: 'center' });
      if (fb > 1) {
        Sim.arrow(ctx, cx - bw / 2 - 12, cyB, cx - bw / 2 - 12, cyB - kA * fb, { color: c.green, width: 2.5 });
        lab(ctx, 'F', 'B', cx - bw / 2 - 12, cyB - kA * fb - 11, { size: 12.5, color: c.green, align: 'center' });
      }
      if (S.y >= fd - 1e-6 && rb > fb + 1) {
        const nlen = Math.min(kA * (rb - fb), h - 8 - yF);
        Sim.arrow(ctx, cx, yF + nlen, cx, yF, { color: c.indigo, width: 2.5 });
        T(ctx, 'N', cx + 9, yF + nlen - 2, { size: 12, color: c.indigo, weight: 700 });
      }
    }
    st = Sim.stage(p.stageEl, { aspect: 4 / 3, minH: 300, maxH: 440, draw, animate: true });
  }

  /* ==================================================================
     5. Continuity — particles in a pipe with an adjustable throat
     ================================================================== */
  function simContinuity() {
    const p = parts('sim-continuity'); if (!p) return;
    let v, st, path = null, ps = [], key = '', cnt = [0, 0];
    const lanes = [-0.76, -0.38, 0, 0.38, 0.76];
    const update = () => {
      const r = v['co-r'], v1 = v['co-v'];
      Sim.out(p.panel, 'v2', (v1 / r).toFixed(2) + ' m/s');
      Sim.out(p.panel, 'd', Math.sqrt(r).toFixed(2));
      Sim.out(p.panel, 'Q', (10 * v1 * 100).toFixed(0) + ' cm³/s');
      cnt = [0, 0];
    };
    v = Sim.controls(p.panel, vals => { v = vals; update(); st && st.redraw(); });
    function geometry(w, h) {
      const D1 = Math.min(h * 0.46, 120), D2 = D1 * Math.sqrt(v['co-r']);
      const xa = w * 0.26, xb = w * 0.4, xc = w * 0.62, xd = w * 0.76, yc = h / 2 + 4;
      const D = x => D1 - (D1 - D2) * (x < xb ? smooth((x - xa) / (xb - xa)) : x <= xc ? 1 : smooth((xd - x) / (xd - xc)));
      const k = [w, h, v['co-r']].join('|');
      if (k !== key) {
        const old = path;
        path = buildPath(-20, w + 20, () => yc, D);
        if (!old || !ps.length || old.total === 0) ps = makeParticles(path, lanes, 22, D1);
        else { const f = path.total / old.total; ps.forEach(q => { q.u *= f; }); }
        key = k;
      }
      return { D1, D2, xb, xc, yc, gates: [w * 0.13, (xb + xc) / 2] };
    }
    function draw(ctx, w, h, t, dt) {
      const c = Sim.C, g = geometry(w, h);
      drawPipe(ctx, path, { lanes });
      // advance particles — identical volume step for all
      if (dt) {
        const Q = g.D1 * g.D1 * 46 * v['co-v'];
        ps.forEach(q => {
          const xOld = path.xAt(q.u);
          q.u += Q * dt;
          let wrapped = false;
          if (q.u >= path.total) { q.u -= path.total; wrapped = true; }
          if (!wrapped) {
            const xNew = path.xAt(q.u);
            g.gates.forEach((gx, i) => { if (xOld < gx && xNew >= gx) cnt[i]++; });
          }
        });
      }
      drawParticles(ctx, path, ps, c.water);
      // gates + counters
      g.gates.forEach((gx, i) => {
        const half = path.D(gx) / 2;
        Sim.line(ctx, [[gx, g.yc - half - 8], [gx, g.yc + half + 8]], { color: c.coral, width: 1.5, dash: [4, 3] });
        T(ctx, Sim.reduced ? 'gate ' + (i + 1) : 'crossed: ' + cnt[i], gx, g.yc - g.D1 / 2 - 22, { size: 11.5, color: c.coral, align: 'center', weight: 650, mono: !Sim.reduced });
      });
      // velocity arrows below the pipe
      const v1 = v['co-v'], v2 = v1 / v['co-r'], kv = Math.min(30, w / 14);
      const ya = g.yc + g.D1 / 2 + 18;
      [[g.gates[0], v1, '1'], [g.gates[1], v2, '2']].forEach(([gx, vv, n]) => {
        const len = Math.min(kv * vv, w * 0.24);
        Sim.arrow(ctx, gx - len / 2, ya, gx + len / 2, ya, { color: c.accent, width: 2.5, head: 8 });
        lab(ctx, 'v', n, gx - len / 2 - 6, ya, { size: 12.5, color: c.accent, align: 'right' });
      });
      lab(ctx, 'A', '1', g.gates[0] + 8, g.yc - g.D1 / 2 + 12, { size: 12, color: c.ink2 });
      lab(ctx, 'A', '2', g.gates[1] + 8, g.yc - g.D2 / 2 - 10, { size: 12, color: c.ink2 });
    }
    st = Sim.stage(p.stageEl, { aspect: 16 / 8, minH: 240, maxH: 360, draw, animate: true });
  }

  /* ==================================================================
     6. Bernoulli energy bars — pipe that narrows and rises
     ================================================================== */
  function simBernoulli() {
    const p = parts('sim-bernoulli'); if (!p) return;
    let v, st, path = null, ps = [], key = '';
    const lanes = [-0.6, 0, 0.6];
    const P1 = 100e3, RHO = 1000;
    const calc = () => {
      const v1 = v['be-v'], r = v['be-r'], hh = v['be-h'], v2 = v1 * r;
      const k1 = 0.5 * RHO * v1 * v1, k2 = 0.5 * RHO * v2 * v2, g2 = RHO * G * hh;
      const E = P1 + k1, P2 = E - k2 - g2;
      return { v1, v2, k1, k2, g1: 0, g2, P2, E };
    };
    const update = () => {
      const k = calc();
      Sim.out(p.panel, 'v2', k.v2.toFixed(2) + ' m/s');
      Sim.out(p.panel, 'P1', kPa(P1));
      Sim.out(p.panel, 'P2', kPa(k.P2));
      Sim.out(p.panel, 'dP', kPa(P1 - k.P2));
    };
    v = Sim.controls(p.panel, vals => { v = vals; update(); st && st.redraw(); });
    function draw(ctx, w, h, t, dt) {
      const c = Sim.C, k = calc();
      const pw = Math.round(w * (w < 560 ? 0.6 : 0.64));
      const D1 = Math.min(h * 0.17, 46), D2 = D1 / Math.sqrt(v['be-r']);
      const yLow = h - 34 - D1 / 2, pxm = (h * 0.42) / 4, yHigh = yLow - v['be-h'] * pxm;
      const xm1 = pw * 0.38, xm2 = pw * 0.62;
      const kk = [w, h, v['be-r'], v['be-h']].join('|');
      if (kk !== key) {
        const yc = x => yLow + (yHigh - yLow) * smooth((x - xm1) / (xm2 - xm1));
        const D = x => D1 + (D2 - D1) * smooth((x - xm1) / (xm2 - xm1));
        const old = path;
        path = buildPath(-10, pw, yc, D);
        if (!old || !ps.length) ps = makeParticles(path, lanes, 20, D1);
        else { const f = path.total / old.total; ps.forEach(q => { q.u *= f; }); }
        key = kk;
      }
      // datum
      Sim.line(ctx, [[0, yLow], [pw, yLow]], { color: c.muted, width: 1, dash: [3, 5] });
      T(ctx, 'h = 0 (datum)', 6, yLow + D1 / 2 + 14, { size: 11, color: c.muted });
      drawPipe(ctx, path, {});
      if (dt) { const Q = D1 * D1 * 30 * v['be-v']; ps.forEach(q => { q.u = (q.u + Q * dt) % path.total; }); }
      drawParticles(ctx, path, ps, c.water);
      // section markers
      [[pw * 0.14, '1'], [pw * 0.86, '2']].forEach(([x, n]) => {
        const y = path.yc(x), d = path.D(x) / 2;
        Sim.line(ctx, [[x, y - d - 6], [x, y + d + 6]], { color: c.ink, width: 1.5, dash: [3, 3] });
        T(ctx, n, x, y - d - 16, { size: 13, weight: 750, align: 'center', color: c.ink });
      });
      if (v['be-h'] > 0.15) {
        const xh = pw * 0.86 + 0;
        Sim.line(ctx, [[pw * 0.14, yHigh], [xh, yHigh]], { color: c.green, width: 1, dash: [3, 4] });
        T(ctx, 'h = ' + v['be-h'].toFixed(1) + ' m', pw * 0.16, yHigh - 10, { size: 11.5, color: c.green, mono: true, weight: 650 });
      }
      // stacked bars
      const bx0 = pw + 12, bx1 = w - 8, bW = Math.min(36, (bx1 - bx0 - 20) / 2 - 4);
      const legend = [['P', c.water], ['½ρv²', c.coral], ['ρgh', c.green]];
      legend.forEach(([s, col], i) => {
        const ly = 12 + i * 16;
        ctx.save(); ctx.fillStyle = col; ctx.fillRect(bx0, ly - 5, 10, 10); ctx.restore();
        T(ctx, s, bx0 + 15, ly, { size: 11.5, color: c.ink2, weight: 600 });
      });
      const yBot = h - 24, yTopBar = 66, scale = (yBot - yTopBar) / (k.E * 1.04);
      const bars = [[P1, k.k1, 0], [k.P2, k.k2, k.g2]];
      const bxs = [bx0 + 6, bx0 + 6 + bW + 16];
      bars.forEach((b, i) => {
        let y = yBot;
        const seg = (val, col) => {
          const hh = Math.max(0, val * scale);
          ctx.save(); ctx.fillStyle = col; ctx.fillRect(bxs[i], y - hh, bW, hh); ctx.restore();
          y -= hh;
        };
        seg(b[2], c.green); seg(b[0], rgba(c.water, 0.85)); seg(b[1], c.coral);
        T(ctx, String(i + 1), bxs[i] + bW / 2, yBot + 12, { size: 12.5, weight: 750, align: 'center' });
      });
      const yE = yBot - k.E * scale;
      Sim.line(ctx, [[bxs[0] - 4, yE], [bxs[1] + bW + 4, yE]], { color: c.ink, width: 1.3, dash: [4, 3] });
      T(ctx, 'total same', (bxs[0] + bxs[1] + bW) / 2, yE - 9, { size: 11, color: c.ink, align: 'center', weight: 650 });
    }
    st = Sim.stage(p.stageEl, { aspect: 16 / 9, minH: 290, maxH: 420, draw, animate: true });
  }

  /* ==================================================================
     7. Venturimeter (+ optional pitot tube)
     ================================================================== */
  function simVenturi() {
    const p = parts('sim-venturi'); if (!p) return;
    let v, st, path = null, ps = [], key = '';
    const lanes = [-0.62, -0.2, 0.2, 0.62];
    const H1 = 0.30, A1 = 20; // m static head at section 1; A1 in cm²
    const calc = () => {
      const v1 = v['ve-v'], r = v['ve-r'], v2 = v1 * r;
      const dh = (v2 * v2 - v1 * v1) / (2 * G), pit = v1 * v1 / (2 * G);
      return { v1, v2, r, dh, pit, dP: 1000 * G * dh, Q: A1 * v1 * 100 };
    };
    const update = () => {
      const k = calc();
      Sim.out(p.panel, 'v2', k.v2.toFixed(2) + ' m/s');
      Sim.out(p.panel, 'Q', k.Q.toFixed(0) + ' cm³/s');
      Sim.out(p.panel, 'dP', k.dP.toFixed(0) + ' Pa');
      Sim.out(p.panel, 'dh', (k.dh * 100).toFixed(1) + ' cm');
      Sim.out(p.panel, 'pit', (k.pit * 100).toFixed(2) + ' cm');
    };
    v = Sim.controls(p.panel, vals => { v = vals; update(); st && st.redraw(); });
    function draw(ctx, w, h, t, dt) {
      const c = Sim.C, k = calc();
      const yc = h * 0.72, D1 = Math.min(h * 0.2, 54), D2 = D1 / Math.sqrt(k.r);
      const xa = w * 0.3, xb = w * 0.44, xc = w * 0.56, xd = w * 0.72;
      const D = x => D1 - (D1 - D2) * (x < xb ? smooth((x - xa) / (xb - xa)) : x <= xc ? 1 : smooth((xd - x) / (xd - xc)));
      const kk = [w, h, k.r].join('|');
      if (kk !== key) {
        const old = path;
        path = buildPath(-10, w + 10, () => yc, D);
        if (!old || !ps.length) ps = makeParticles(path, lanes, 20, D1);
        else { const f = path.total / old.total; ps.forEach(q => { q.u *= f; }); }
        key = kk;
      }
      drawPipe(ctx, path, {});
      if (dt) { const Q = D1 * D1 * 70 * k.v1; ps.forEach(q => { q.u = (q.u + Q * dt) % path.total; }); }
      drawParticles(ctx, path, ps, c.water);
      const s = (yc - D1 / 2 - 26) / 0.40, cw = 12, yColTop = 16;
      const cols = [
        { x: w * 0.15, H: H1, name: 'wide' },
        { x: w * 0.5, H: H1 - k.dh, name: 'throat' },
        { x: w * 0.86, H: v.third === 'pitot' ? H1 + k.pit : H1, name: v.third === 'pitot' ? 'pitot' : 'wide' },
      ];
      cols.forEach((col, i) => {
        const base = yc - D(col.x) / 2, yLev = yc - col.H * s;
        const pitot = i === 2 && v.third === 'pitot';
        const yBottom = pitot ? yc : base;
        // liquid
        ctx.save(); ctx.fillStyle = 'rgba(58,140,203,0.45)';
        if (yLev < yBottom) ctx.fillRect(col.x - cw / 2, Math.max(yLev, yColTop), cw, yBottom - Math.max(yLev, yColTop));
        if (pitot) ctx.fillRect(col.x - 26, yc - cw / 2, 26, cw);
        ctx.restore();
        Sim.line(ctx, [[col.x - cw / 2, yColTop], [col.x - cw / 2, pitot ? yc - cw / 2 : base]], { color: c.ink2, width: 2 });
        Sim.line(ctx, [[col.x + cw / 2, yColTop], [col.x + cw / 2, pitot ? yc + cw / 2 : base]], { color: c.ink2, width: 2 });
        if (pitot) {
          Sim.line(ctx, [[col.x - cw / 2, yc - cw / 2], [col.x - 26, yc - cw / 2]], { color: c.ink2, width: 2 });
          Sim.line(ctx, [[col.x + cw / 2, yc + cw / 2], [col.x - 26, yc + cw / 2]], { color: c.ink2, width: 2 });
        }
        if (yLev >= base && !pitot) T(ctx, 'P < P₀', col.x, base - 12, { size: 11, color: c.coral, align: 'center', weight: 700, bg: 'rgba(255,255,255,0.9)' });
        T(ctx, col.name, col.x, yc + D1 / 2 + 14, { size: 11.5, color: c.ink2, align: 'center', weight: 600 });
      });
      // Δh between 1 and 2
      const y1 = yc - cols[0].H * s, y2 = yc - cols[1].H * s;
      const xm = (cols[0].x + cols[1].x) / 2 + 8;
      Sim.line(ctx, [[cols[0].x + cw / 2, y1], [xm + 6, y1]], { color: c.muted, width: 1, dash: [3, 3] });
      Sim.line(ctx, [[xm - 6, Math.min(y2, yc - D2 / 2)], [cols[1].x - cw / 2, Math.min(y2, yc - D2 / 2)]], { color: c.muted, width: 1, dash: [3, 3] });
      if (k.dh * s > 4) dim(ctx, xm, y1, Math.min(y2, yc - D2 / 2), c.accent);
      T(ctx, 'Δh = ' + (k.dh * 100).toFixed(1) + ' cm', xm + 8, (y1 + Math.min(y2, yc - D2 / 2)) / 2, { size: 11.5, color: c.accent, mono: true, weight: 650, bg: 'rgba(255,255,255,0.85)' });
      if (v.third === 'pitot' && k.pit * s > 3) {
        const x3 = cols[2].x - cw / 2 - 8, yS3 = yc - H1 * s, yP3 = yc - cols[2].H * s;
        Sim.line(ctx, [[x3 - 4, yS3], [cols[2].x + cw / 2, yS3]], { color: c.green, width: 1, dash: [3, 3] });
        dim(ctx, x3, yS3, yP3, c.green);
        T(ctx, 'v₁²/2g', x3 - 6, (yS3 + yP3) / 2, { size: 11.5, color: c.green, align: 'right', weight: 650 });
      }
      Sim.arrow(ctx, 8, yc, 36, yc, { color: c.accent, width: 2 });
    }
    st = Sim.stage(p.stageEl, { aspect: 16 / 9, minH: 290, maxH: 420, draw, animate: true });
  }

  /* ==================================================================
     8. Torricelli — tank, hole, jet, range
     ================================================================== */
  function simTorricelli() {
    const p = parts('sim-torricelli'); if (!p) return;
    let v, st;
    const calc = () => {
      const H = v['to-H'], y = v['to-y'] * H, dP = v['to-P'] * 1000;
      const Hp = H + dP / (1000 * G), depth = H - y;
      const vel = Math.sqrt(2 * G * depth + 2 * dP / 1000);
      const R = 2 * Math.sqrt(Math.max(0, (Hp - y) * y));
      const yStar = Math.min(Hp / 2, H);
      const Rmax = 2 * Math.sqrt(Math.max(0, (Hp - yStar) * yStar));
      const ym = Hp - y; // mirror hole height
      return { H, y, dP, Hp, depth, vel, R, yStar, Rmax, ym, tf: Math.sqrt(2 * y / G) };
    };
    const update = () => {
      const k = calc();
      Sim.out(p.panel, 'depth', k.depth.toFixed(2) + ' m');
      Sim.out(p.panel, 'v', k.vel.toFixed(2) + ' m/s');
      Sim.out(p.panel, 'R', k.R.toFixed(2) + ' m');
      Sim.out(p.panel, 'Rmax', k.Rmax.toFixed(2) + ' m at y = ' + k.yStar.toFixed(2) + ' m');
    };
    v = Sim.controls(p.panel, vals => { v = vals; update(); st && st.redraw(); });
    function jet(ctx, x0, yG, s, y, vel, o) {
      const tl = Math.sqrt(2 * y / G), pts = [];
      for (let i = 0; i <= 40; i++) { const tt = tl * i / 40; pts.push([x0 + vel * tt * s, yG - (y - 0.5 * G * tt * tt) * s]); }
      Sim.line(ctx, pts, o);
      return pts[pts.length - 1];
    }
    function draw(ctx, w, h, t) {
      const c = Sim.C, k = calc();
      const yG = h - 30, tankW = clamp(w * 0.16, 50, 110), tx0 = 16, tx1 = tx0 + tankW;
      const s = Math.min((yG - 30) / 4.4, (w - tx1 - 22) / 6.3);
      const yTopWall = yG - 4.3 * s, ySurf = yG - k.H * s, yHole = yG - k.y * s;
      // ground
      Sim.line(ctx, [[6, yG], [w - 6, yG]], { color: c.ink2, width: 2 });
      // water
      ctx.save(); ctx.fillStyle = c.liquid; ctx.fillRect(tx0, ySurf, tankW, yG - ySurf); ctx.restore();
      Sim.line(ctx, [[tx0, ySurf], [tx1, ySurf]], { color: c.liquidEdge, width: 2 });
      // walls (gap at hole)
      Sim.line(ctx, [[tx0, yTopWall], [tx0, yG], [tx1, yG], [tx1, yHole + 3]], { color: c.ink2, width: 3 });
      Sim.line(ctx, [[tx1, yHole - 3], [tx1, yTopWall]], { color: c.ink2, width: 3 });
      if (k.dP > 0) {
        ctx.save(); ctx.fillStyle = c.ink2; ctx.fillRect(tx0 + 2, ySurf - 7, tankW - 4, 7); ctx.restore();
        [0.3, 0.7].forEach(f => Sim.arrow(ctx, tx0 + tankW * f, ySurf - 30, tx0 + tankW * f, ySurf - 9, { color: c.plum, width: 2, head: 7 }));
        T(ctx, '+ΔP', tx0 + tankW / 2, ySurf - 38, { size: 11.5, color: c.plum, align: 'center', weight: 700 });
      }
      // brackets inside tank
      const bxk = tx0 + 12;
      if (k.depth * s > 10) { dim(ctx, bxk, ySurf, yHole, c.coral); T(ctx, 'h', bxk + 7, (ySurf + yHole) / 2, { size: 12.5, color: c.coral, weight: 700 }); }
      if (k.y * s > 10) { dim(ctx, bxk, yHole, yG, c.indigo); T(ctx, 'y', bxk + 7, (yHole + yG) / 2, { size: 12.5, color: c.indigo, weight: 700 }); }
      Sim.line(ctx, [[bxk, yHole], [tx1, yHole]], { color: c.muted, width: 1, dash: [2, 3] });
      // max-range marker
      const xMax = tx1 + k.Rmax * s;
      ctx.save(); ctx.fillStyle = c.green;
      ctx.beginPath(); ctx.moveTo(xMax, yG - 1); ctx.lineTo(xMax - 5, yG - 9); ctx.lineTo(xMax + 5, yG - 9); ctx.closePath(); ctx.fill(); ctx.restore();
      T(ctx, 'max', xMax, yG - 17, { size: 11, color: c.green, align: 'center', weight: 700 });
      // mirror hole
      if (v.mirror === 'on' && k.ym > 0.02 && k.ym < k.H && Math.abs(k.ym - k.y) > 0.03) {
        const yM = yG - k.ym * s, vm = Math.sqrt(2 * G * (k.Hp - k.ym));
        jet(ctx, tx1, yG, s, k.ym, vm, { color: rgba(c.plum, 0.7), width: 2, dash: [5, 5] });
        ctx.save(); ctx.fillStyle = c.plum; ctx.beginPath(); ctx.arc(tx1, yM, 3.5, 0, Math.PI * 2); ctx.fill(); ctx.restore();
        T(ctx, 'mirror hole', tx1 + 6, yM - 10, { size: 11, color: c.plum, weight: 650 });
      }
      // jet
      ctx.save();
      const end = jet(ctx, tx1, yG, s, k.y, k.vel, { color: rgba(c.water, 0.75), width: 5 });
      if (!Sim.reduced) {
        ctx.lineDashOffset = -t * 70;
        jet(ctx, tx1, yG, s, k.y, k.vel, { color: 'rgba(255,255,255,0.75)', width: 2, dash: [3, 12] });
      }
      ctx.restore();
      ctx.save(); ctx.fillStyle = rgba(c.water, 0.4);
      ctx.beginPath(); ctx.ellipse(end[0], yG, 10, 3.5, 0, 0, Math.PI * 2); ctx.fill(); ctx.restore();
      // range arrow under ground
      if (k.R * s > 12) {
        Sim.arrow(ctx, tx1, yG + 13, end[0], yG + 13, { color: c.accent, width: 1.8, head: 7 });
        T(ctx, 'R = ' + k.R.toFixed(2) + ' m', (tx1 + end[0]) / 2, yG + 13, { size: 11.5, color: c.accent, align: 'center', mono: true, weight: 650, bg: 'rgba(255,255,255,0.92)' });
      }
      if (Math.abs(k.R - k.Rmax) < 0.012 * Math.max(k.Rmax, 0.1)) T(ctx, 'maximum range!', w - 10, 34, { size: 12.5, color: c.green, align: 'right', weight: 750 });
      T(ctx, 'v = ' + k.vel.toFixed(2) + ' m/s', w - 10, 14, { size: 11.5, color: c.water, mono: true, weight: 650, align: 'right' });
    }
    st = Sim.stage(p.stageEl, { aspect: 16 / 10, minH: 290, maxH: 430, draw, animate: true });
  }

  /* ==================================================================
     9. Dynamic lift: aerofoil streamlines + Magnus effect
     ================================================================== */
  function simLift() {
    const p = parts('sim-lift'); if (!p) return;
    let v, st;
    // ---- wing particles
    const wingP = [];
    // ---- ball state
    let ballLines = null, ballKey = '', ballP = [], theta = 0;
    const update = () => {
      showMode(p.panel, v.lmode);
      if (v.lmode === 'wing') {
        const rho = +v.rho, dP = 0.5 * rho * (v['li-vt'] * v['li-vt'] - v['li-vb'] * v['li-vb']);
        Sim.out(p.panel, 'dP', dP.toFixed(0) + ' Pa');
        Sim.out(p.panel, 'L', Math.abs(dP * v['li-A']) < 1e5 ? (dP * v['li-A']).toFixed(0) + ' N' : Sim.sci(dP * v['li-A'], 2) + ' N');
      } else {
        const sp = v['li-spin'];
        Sim.out(p.panel, 'fast', Math.abs(sp) < 0.01 ? 'neither' : sp > 0 ? 'top' : 'bottom');
        Sim.out(p.panel, 'force', Math.abs(sp) < 0.01 ? 'none' : sp > 0 ? 'upward (lift)' : 'downward (dip)');
      }
    };
    v = Sim.controls(p.panel, vals => { v = vals; update(); st && st.redraw(); });

    // NACA-like cambered aerofoil, chord from 0..1
    const thick = xi => 5 * 0.14 * (0.2969 * Math.sqrt(xi) - 0.126 * xi - 0.3516 * xi * xi + 0.2843 * xi ** 3 - 0.1015 * xi ** 4);
    const camb = xi => (xi < 0.4 ? 0.06 / 0.16 * (0.8 * xi - xi * xi) : 0.06 / 0.36 * (0.2 + 0.8 * xi - xi * xi));

    function drawWing(ctx, w, h, t, dt) {
      const c = Sim.C;
      const cx = w * 0.5, cy = h * 0.52, ch = Math.min(w * 0.5, 320), xLE = cx - ch / 2;
      const vt = v['li-vt'], vb = v['li-vb'];
      const kap = clamp((vt - vb) / ((vt + vb) / 2) * 5, -1.2, 1.2);
      const U = x => { const xi = (x - xLE) / ch; return xi <= 0 || xi >= 1 ? 0 : (camb(xi) + thick(xi)) * ch; };
      const Lw = x => { const xi = (x - xLE) / ch; return xi <= 0 || xi >= 1 ? 0 : -(camb(xi) - thick(xi)) * ch; };
      const B = x => Math.exp(-Math.pow((x - cx) / (0.7 * ch), 2));
      const gap = Math.max(12, (h / 2 - 22) / 5.6);
      const K = 5;
      const cU = (j, x) => 1 - kap * 0.42 * B(x) * Math.exp(-(j - 1) / 2);
      const cL = (j, x) => 1 + kap * 0.28 * B(x) * Math.exp(-(j - 1) / 2);
      const laneY = (side, k, x) => {
        let sum = 0;
        for (let j = 1; j <= k; j++) sum += side < 0 ? cU(j, x) : cL(j, x);
        const wk = Math.exp(-(k - 1) / 3);
        return side < 0 ? cy - U(x) * wk - gap * sum : cy + Lw(x) * wk + gap * sum;
      };
      // streamlines
      for (const side of [-1, 1]) for (let k = 1; k <= K; k++) {
        const pts = [];
        for (let x = 0; x <= w; x += 4) pts.push([x, laneY(side, k, x)]);
        Sim.line(ctx, pts, { color: rgba(c.water, 0.35), width: 1.2 });
      }
      // particles
      if (!wingP.length) {
        for (const side of [-1, 1]) for (let k = 1; k <= K; k++) for (let i = 0; i < 9; i++) wingP.push({ side, k, x: (i + (k % 2) * 0.5) / 9 });
      }
      const base = 0.06 + 0.0016 * (vt + vb) / 2; // fraction of width per second
      ctx.save(); ctx.fillStyle = c.water;
      wingP.forEach(q => {
        const xpx = q.x * w;
        const f = q.side < 0 ? 1 / cU(1, xpx) : 1 / cL(1, xpx);
        if (dt) { q.x += base * f * dt; if (q.x > 1.02) q.x -= 1.04; }
        const X = q.x * w;
        ctx.beginPath(); ctx.arc(X, laneY(q.side, q.k, X), 2.4, 0, Math.PI * 2); ctx.fill();
      });
      ctx.restore();
      // aerofoil
      ctx.save();
      ctx.beginPath();
      for (let i = 0; i <= 80; i++) { const xi = 1 - Math.cos(Math.PI * i / 160); const x = xLE + xi * ch; i ? ctx.lineTo(x, cy - U(x + 1e-9) ) : ctx.moveTo(x, cy); }
      for (let i = 80; i >= 0; i--) { const xi = 1 - Math.cos(Math.PI * i / 160); const x = xLE + xi * ch; ctx.lineTo(x, cy + Lw(x + 1e-9)); }
      ctx.closePath();
      ctx.fillStyle = c.indigoSoft; ctx.strokeStyle = c.indigo; ctx.lineWidth = 2; ctx.fill(); ctx.stroke();
      ctx.restore();
      // pressure arrows (pressure pushes inward on the surface)
      const lt = 13 * (1 - 0.45 * kap), lb = 13 * (1 + 0.45 * kap);
      [0.2, 0.4, 0.6, 0.8].forEach(xi => {
        const x = xLE + xi * ch;
        Sim.arrow(ctx, x, cy - U(x) - 4 - Math.max(4, lt), x, cy - U(x) - 3, { color: c.coral, width: 1.6, head: 6 });
        Sim.arrow(ctx, x, cy + Lw(x) + 4 + Math.max(4, lb), x, cy + Lw(x) + 3, { color: c.coral, width: 1.6, head: 6 });
      });
      // net lift
      const L = 20 + 34 * Math.abs(kap) / 1.2;
      if (Math.abs(kap) > 0.02) {
        const up = kap > 0;
        Sim.arrow(ctx, cx + ch * 0.62, cy, cx + ch * 0.62, up ? cy - L : cy + L, { color: c.green, width: 3 });
        T(ctx, up ? 'lift' : 'down-force', cx + ch * 0.62 + 8, up ? cy - L + 6 : cy + L - 6, { size: 12, color: c.green, weight: 700 });
      }
      const topTxt = kap >= 0 ? 'faster air · lower P' : 'slower air · higher P';
      const botTxt = kap >= 0 ? 'slower air · higher P' : 'faster air · lower P';
      T(ctx, topTxt, 8, 13, { size: 11.5, color: c.ink2, weight: 650, bg: 'rgba(255,255,255,0.85)' });
      T(ctx, botTxt, 8, h - 13, { size: 11.5, color: c.ink2, weight: 650, bg: 'rgba(255,255,255,0.85)' });
      T(ctx, 'air →', w - 8, 13, { size: 11.5, color: c.muted, align: 'right', weight: 650 });
    }

    function ballField(cx, cy, R, Uf, Gam) {
      return (x, y) => {
        const X = x - cx, Y = cy - y, r2 = X * X + Y * Y, r4 = r2 * r2;
        const re = Uf - Uf * R * R * (X * X - Y * Y) / r4 + Gam * Y / (2 * Math.PI * r2);
        const im = Uf * R * R * 2 * X * Y / r4 + Gam * X / (2 * Math.PI * r2);
        return [re, im]; // screen velocity: (re, +im) because screen y is flipped
      };
    }
    function drawBall(ctx, w, h, t, dt) {
      const c = Sim.C;
      const cx = w * 0.5, cy = h * 0.5, R = Math.min(h * 0.15, 38), Uf = 60;
      const spin = v['li-spin'];
      const Gam = spin * 0.8 * 4 * Math.PI * Uf * R;
      const F = ballField(cx, cy, R, Uf, Gam);
      const key = [w, h, spin].join('|');
      const gap = (h - 20) / 12;
      if (key !== ballKey) {
        ballLines = [];
        for (let j = -6; j <= 6; j++) {
          let x = -4, y = cy + j * gap + (j === 0 ? 0.01 : 0);
          const pts = [[x, y]];
          for (let n = 0; n < 900 && x < w + 4; n++) {
            const v1 = F(x, y), m1 = Math.hypot(v1[0], v1[1]) || 1;
            const xm = x + 1.5 * v1[0] / m1, ym = y + 1.5 * v1[1] / m1;
            const v2 = F(xm, ym), m2 = Math.hypot(v2[0], v2[1]) || 1;
            x += 3 * v2[0] / m2; y += 3 * v2[1] / m2;
            if (Math.hypot(x - cx, y - cy) < R) break;
            if (n % 2 === 0) pts.push([x, y]);
          }
          ballLines.push(pts);
        }
        ballKey = key;
        if (!ballP.length) for (let i = 0; i < 70; i++) ballP.push({ x: Math.random() * w, y: cy + (Math.floor(Math.random() * 13) - 6) * gap, age: 0 });
      }
      ballLines.forEach(pts => Sim.line(ctx, pts, { color: rgba(c.water, 0.32), width: 1.2 }));
      ctx.save(); ctx.fillStyle = c.water;
      ballP.forEach(q => {
        if (dt) {
          for (let i = 0; i < 3; i++) { const vv = F(q.x, q.y); q.x += vv[0] * dt / 3; q.y += vv[1] * dt / 3; }
          q.age += dt;
          if (q.x > w + 4 || q.age > 14 || Math.hypot(q.x - cx, q.y - cy) < R) {
            q.x = -4; q.y = cy + (Math.floor(Math.random() * 13) - 6) * gap + (Math.random() - 0.5) * 4; q.age = 0;
          }
        }
        ctx.beginPath(); ctx.arc(q.x, q.y, 2.3, 0, Math.PI * 2); ctx.fill();
      });
      ctx.restore();
      // ball with rotating seam
      if (dt) theta += spin * 5 * dt;
      ctx.save();
      ctx.fillStyle = '#FFFFFF'; ctx.strokeStyle = c.ink2; ctx.lineWidth = 2.5;
      ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.translate(cx, cy); ctx.rotate(theta);
      ctx.strokeStyle = c.coral; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(-R * 1.25, 0, R * 0.95, -0.75, 0.75); ctx.stroke();
      ctx.beginPath(); ctx.arc(R * 1.25, 0, R * 0.95, Math.PI - 0.75, Math.PI + 0.75); ctx.stroke();
      ctx.restore();
      // spin arrow (arc)
      if (Math.abs(spin) > 0.01) {
        const r2 = R + 9, a0 = -2.2, a1 = -0.9;
        ctx.save(); ctx.strokeStyle = c.plum; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(cx, cy, r2, a0, a1); ctx.stroke(); ctx.restore();
        const ae = spin > 0 ? a1 : a0, dir = spin > 0 ? 1 : -1;
        const ex = cx + r2 * Math.cos(ae), ey = cy + r2 * Math.sin(ae);
        const tx = -Math.sin(ae) * dir, ty = Math.cos(ae) * dir;
        Sim.arrow(ctx, ex - tx * 6, ey - ty * 6, ex + tx * 2, ey + ty * 2, { color: c.plum, width: 2, head: 7 });
        const L = 22 + 30 * Math.abs(spin);
        Sim.arrow(ctx, cx + R + 26, cy, cx + R + 26, spin > 0 ? cy - L : cy + L, { color: c.green, width: 3 });
        T(ctx, 'Magnus force', cx + R + 34, spin > 0 ? cy - L + 4 : cy + L - 4, { size: 11.5, color: c.green, weight: 700 });
      }
      T(ctx, 'ball moves ←   (air streams past →)', 8, 13, { size: 11.5, color: c.ink2, weight: 650, bg: 'rgba(255,255,255,0.85)' });
      if (Math.abs(spin) > 0.01) T(ctx, (spin > 0 ? 'top' : 'bottom') + ': surface moves with the air → faster → lower P', 8, h - 13, { size: 11.5, color: c.ink2, bg: 'rgba(255,255,255,0.85)' });
    }
    function draw(ctx, w, h, t, dt) {
      if (v.lmode === 'ball') drawBall(ctx, w, h, t, dt); else drawWing(ctx, w, h, t, dt);
    }
    st = Sim.stage(p.stageEl, { aspect: 16 / 9, minH: 270, maxH: 420, draw, animate: true });
  }

  /* ==================================================================
     10. Accelerating containers: tan θ = a/g ; g_eff = g + a
     ================================================================== */
  function simAccel() {
    const p = parts('sim-accel'); if (!p) return;
    let v, st;
    const update = () => {
      const a = v['ac-a'];
      showMode(p.panel, v.adir);
      if (v.adir === 'h') {
        const th = Math.atan(Math.abs(a) / G) * 180 / Math.PI;
        Sim.out(p.panel, 'th', th.toFixed(1) + '°');
        Sim.out(p.panel, 'dy', (Math.abs(a) / G * 100).toFixed(1) + ' cm');
      } else {
        const ge = G + a;
        Sim.out(p.panel, 'ge', ge.toFixed(1) + ' m/s²');
        Sim.out(p.panel, 'pb', ge <= 0.001 ? '0 (free fall)' : kPa(1000 * ge * 0.5));
        Sim.out(p.panel, 'frac', ge <= 0.001 ? 'no buoyancy' : '60% (unchanged)');
      }
    };
    v = Sim.controls(p.panel, vals => { v = vals; update(); st && st.redraw(); });
    function draw(ctx, w, h) {
      const c = Sim.C, a = v['ac-a'];
      const side = Math.min(h * 0.62, 170), cx = Math.min(w * 0.42, w / 2 - 20), yTop = 30, x0 = cx - side / 2, x1 = cx + side / 2, yB = yTop + side;
      const yMean = yTop + side * 0.45;
      if (v.adir === 'h') {
        const tn = a / G, yl = yMean + (side / 2) * tn, yr = yMean - (side / 2) * tn;
        // rear wall (opposite the acceleration) is higher: a>0 → accel to right → left higher
        const yL = yMean - (side / 2) * tn, yR = yMean + (side / 2) * tn;
        void yl; void yr;
        ctx.save();
        ctx.beginPath(); ctx.rect(x0, yTop, side, side); ctx.clip();
        ctx.beginPath(); ctx.moveTo(x0, yL); ctx.lineTo(x1, yR); ctx.lineTo(x1, yB); ctx.lineTo(x0, yB); ctx.closePath();
        ctx.fillStyle = c.liquid; ctx.fill();
        ctx.restore();
        Sim.line(ctx, [[x0, yL], [x1, yR]], { color: c.liquidEdge, width: 2, });
        Sim.line(ctx, [[x0, yTop], [x0, yB], [x1, yB], [x1, yTop]], { color: c.ink2, width: 3 });
        // wheels
        ctx.save(); ctx.fillStyle = c.ink2;
        [x0 + side * 0.2, x1 - side * 0.2].forEach(x => { ctx.beginPath(); ctx.arc(x, yB + 9, 7, 0, Math.PI * 2); ctx.fill(); });
        ctx.restore();
        if (Math.abs(a) > 0.05) {
          const L = 20 + 40 * Math.abs(a) / G, dir = Math.sign(a);
          Sim.arrow(ctx, cx - dir * L / 2, yB + 30, cx + dir * L / 2, yB + 30, { color: c.accent, width: 3 });
          T(ctx, 'a', cx + dir * (L / 2 + 10), yB + 30, { size: 13, color: c.accent, weight: 700, align: 'center' });
          // angle mark at horizontal reference
          Sim.line(ctx, [[cx - side * 0.42, yMean], [cx + side * 0.42, yMean]], { color: c.muted, width: 1, dash: [3, 4] });
          T(ctx, 'θ', cx + (a > 0 ? -side * 0.3 : side * 0.3), yMean + (a > 0 ? -8 : -8), { size: 13, color: c.coral, weight: 700, align: 'center' });
          T(ctx, a > 0 ? 'rear (left) higher' : 'rear (right) higher', cx, yTop - 14, { size: 11.5, color: c.ink2, align: 'center', weight: 600 });
        } else T(ctx, 'no acceleration: level surface', cx, yTop - 14, { size: 11.5, color: c.ink2, align: 'center', weight: 600 });
        // vector triangle: g down, −a pseudo, g_eff ⟂ surface
        const vx = Math.max(x1 + 40, w - 80), vy = yTop + 22, kg = Math.min(70, h * 0.3);
        if (vx + 50 < w + 30) {
          Sim.arrow(ctx, vx, vy, vx, vy + kg, { color: c.ink2, width: 2 });
          T(ctx, 'g', vx - 8, vy + kg / 2, { size: 12.5, color: c.ink2, weight: 700, align: 'right' });
          if (Math.abs(a) > 0.05) {
            Sim.arrow(ctx, vx, vy + kg, vx - kg * a / G, vy + kg, { color: c.plum, width: 2 });
            T(ctx, '−a', vx - kg * a / G / 2, vy + kg + 12, { size: 12, color: c.plum, weight: 700, align: 'center' });
            Sim.arrow(ctx, vx, vy, vx - kg * a / G, vy + kg, { color: c.coral, width: 2.5 });
          }
          lab(ctx, 'g', 'eff', vx + 6, vy + 6, { size: 12.5, color: c.coral });
        }
      } else {
        const ge = G + a;
        // lift cabin
        ctx.save(); ctx.strokeStyle = c.line2; ctx.lineWidth = 2; ctx.setLineDash([6, 5]);
        ctx.strokeRect(x0 - 18, yTop - 18, side + 36, side + 30); ctx.restore();
        ctx.save(); ctx.fillStyle = c.liquid; ctx.fillRect(x0, yMean, side, yB - yMean); ctx.restore();
        Sim.line(ctx, [[x0, yMean], [x1, yMean]], { color: c.liquidEdge, width: 2 });
        Sim.line(ctx, [[x0, yTop], [x0, yB], [x1, yB], [x1, yTop]], { color: c.ink2, width: 3 });
        // floating block (60% submerged always while g_eff > 0)
        const bw = side * 0.3, bh = side * 0.22;
        const sub = ge > 0.001 ? 0.6 : 0.6; // fraction unchanged; in free fall it just stays where it is
        ctx.save(); ctx.fillStyle = rgba(c.amber, 0.55); ctx.strokeStyle = c.amber; ctx.lineWidth = 2;
        Sim.rrect(ctx, cx - bw / 2, yMean - bh * (1 - sub), bw, bh, 3); ctx.fill(); ctx.stroke(); ctx.restore();
        // bottom pressure arrows ∝ g_eff
        const la = clamp(ge / G, 0, 2) * 16;
        if (la > 1) [0.2, 0.5, 0.8].forEach(f => Sim.arrow(ctx, x0 + side * f, yB - 3 - la, x0 + side * f, yB - 3, { color: c.coral, width: 1.8, head: 6 }));
        if (Math.abs(a) > 0.05) {
          const L = 20 + 30 * Math.abs(a) / G, dir = Math.sign(a);
          Sim.arrow(ctx, x1 + 34, cy0(), x1 + 34, cy0() - dir * L, { color: c.accent, width: 3 });
          T(ctx, 'a', x1 + 44, cy0() - dir * L / 2, { size: 13, color: c.accent, weight: 700 });
        }
        lab(ctx, 'g', 'eff', cx - 30, yTop - 6, { size: 12.5, color: c.coral });
        T(ctx, '= g + a = ' + ge.toFixed(1), cx - 6, yTop - 6, { size: 12, color: c.coral, mono: true });
        if (ge <= 0.001) T(ctx, 'free fall: P = P₀ everywhere, no upthrust', cx, yB + 26, { size: 11.5, color: c.coral, align: 'center', weight: 650 });
        function cy0() { return (yTop + yB) / 2; }
      }
    }
    st = Sim.stage(p.stageEl, { aspect: 16 / 9, minH: 260, maxH: 380, draw });
  }

  simPressure();
  simParadox();
  simUtube();
  simHydraulic();
  simFloat();
  simContinuity();
  simBernoulli();
  simVenturi();
  simTorricelli();
  simLift();
  simAccel();
})();
