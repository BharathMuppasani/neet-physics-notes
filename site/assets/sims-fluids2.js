/* =====================================================================
   Fluids II simulations — viscosity, Stokes, Reynolds, surface tension,
   soap film, contact angle, drops & bubbles, connected bubbles, capillary.
   Each sim initialises only if its host figure exists.
   ===================================================================== */
(function () {
  'use strict';
  if (typeof Sim === 'undefined') return;

  const G = 9.8;
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const lerp = (a, b, t) => a + (b - a) * t;
  const fig = id => document.getElementById(id);
  const stages = [];

  /* nice upper bound for an axis: 1, 2, 2.5, 5 × 10^n */
  function niceMax(x) {
    if (!(x > 0)) return 1;
    const e = Math.pow(10, Math.floor(Math.log10(x)));
    const m = x / e;
    const n = m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10;
    return n * e;
  }
  function fmt(x, unit, dp) {
    return Sim.sci(x, dp === undefined ? 2 : dp) + (unit || '');
  }
  /* hatched rectangle (fixed solid) */
  function hatch(ctx, x, y, w, h, color) {
    const C = Sim.C;
    ctx.save();
    ctx.fillStyle = C.surface2; ctx.fillRect(x, y, w, h);
    ctx.beginPath(); ctx.rect(x, y, w, h); ctx.clip();
    ctx.strokeStyle = color || C.line2; ctx.lineWidth = 1;
    for (let i = -h; i < w + h; i += 8) { ctx.beginPath(); ctx.moveTo(x + i, y + h); ctx.lineTo(x + i + h, y); ctx.stroke(); }
    ctx.restore();
    ctx.save(); ctx.strokeStyle = C.ink2; ctx.lineWidth = 1.5;
    ctx.strokeRect(x, y, w, h); ctx.restore();
  }
  function dimArrow(ctx, x, y1, y2, label, color) {
    const c = color || Sim.C.ink2;
    Sim.arrow(ctx, x, (y1 + y2) / 2, x, y1, { color: c, width: 1.2, head: 7 });
    Sim.arrow(ctx, x, (y1 + y2) / 2, x, y2, { color: c, width: 1.2, head: 7 });
    if (label) Sim.text(ctx, label, x - 8, (y1 + y2) / 2, { size: 12, weight: 650, color: c, align: 'right' });
  }

  /* =================================================================
     1. Viscosity — layers between plates / pipe flow
     ================================================================= */
  function initVisc() {
    const root = fig('sim-visc'); if (!root) return;
    const host = root.querySelector('.sim-stage'), panel = root.querySelector('.sim-panel');
    let P = null;
    const dots = [];
    for (let i = 0; i < 10; i++) for (let j = 0; j < 6; j++) dots.push({ layer: i, x: (j + Math.random() * 0.8) / 6 });

    function geom(w, h) {
      const L = 46, R = w - 14, top0 = 40, bot = h - 34;
      const frac = 0.4 + 0.6 * (P['vis-d'] - 0.5) / 4.5;
      const gp = (bot - top0) * frac;
      return { L, R, top0, bot, gp, k: Math.min(16, (R - L) / 30) };
    }

    function draw(ctx, w, h, t, dt) {
      if (!P) return;
      const C = Sim.C, g = geom(w, h);
      const pipe = P.mode === 'pipe';
      const v = P['vis-v'];
      const W = g.R - g.L;
      const speedPx = f => g.k * v * f;            // px/s for a layer with speed fraction f
      const x0 = g.L + 10;
      const maxLen = Math.min(W * 0.5, 230) * (v / 10) + 4;
      const N = pipe ? 10 : 8;

      let yTopEdge, yBotEdge;                       // liquid boundaries
      if (pipe) {
        const yc = (g.top0 + g.bot) / 2 + 2;
        yTopEdge = yc - g.gp / 2; yBotEdge = yc + g.gp / 2;
      } else { yTopEdge = g.bot - g.gp; yBotEdge = g.bot; }
      const H = yBotEdge - yTopEdge;
      const layerF = i => {                         // centre position (0 bottom .. 1 top) and speed fraction
        const pos = (i + 0.5) / N;
        if (!pipe) return { pos, f: pos };
        const eta = pos * 2 - 1;
        return { pos, f: 1 - eta * eta };
      };

      // liquid bands
      for (let i = 0; i < N; i++) {
        const y1 = yBotEdge - (i + 1) / N * H;
        ctx.fillStyle = i % 2 ? 'rgba(58,140,203,0.13)' : 'rgba(58,140,203,0.22)';
        ctx.fillRect(g.L, y1, W, H / N + 0.5);
      }

      // tracer dots
      dots.forEach(d => {
        if (d.layer >= N) return;
        const lf = layerF(d.layer);
        d.x += dt * speedPx(lf.f) / W;
        d.x -= Math.floor(d.x);
        const y = yBotEdge - lf.pos * H;
        ctx.beginPath(); ctx.arc(g.L + d.x * W, y, 2.6, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(58,140,203,0.75)'; ctx.fill();
      });

      // dye line (starts straight, shears with time)
      const xd = g.L + W * 0.52;
      const maxSpd = speedPx(1);
      const period = clamp((g.R - xd - 12) / Math.max(maxSpd, 1), 1.2, 6);
      const td = Sim.reduced ? period * 0.7 : (t % (period + 0.6));
      const tt = Math.min(td, period);
      const pts = [];
      for (let s = 0; s <= 30; s++) {
        const pos = s / 30;
        const f = pipe ? 1 - Math.pow(pos * 2 - 1, 2) : pos;
        pts.push([xd + speedPx(f) * tt, yBotEdge - pos * H]);
      }
      Sim.line(ctx, pts, { color: C.plum, width: 3 });
      Sim.text(ctx, 'dye line', xd - 4, yBotEdge - H * (pipe ? 0.92 : 0.12), { size: 11, color: C.plum, align: 'right', weight: 650 });

      // velocity arrows + profile
      const prof = [];
      for (let i = 0; i < N; i++) {
        const lf = layerF(i);
        const y = yBotEdge - lf.pos * H;
        const len = maxLen * lf.f;
        if (len > 4) Sim.arrow(ctx, x0, y, x0 + len, y, { color: C.indigo, width: 2, head: 7 });
      }
      for (let s = 0; s <= 30; s++) {
        const pos = s / 30;
        const f = pipe ? 1 - Math.pow(pos * 2 - 1, 2) : pos;
        prof.push([x0 + maxLen * f, yBotEdge - pos * H]);
      }
      Sim.line(ctx, prof, { color: C.ink2, width: 1.3, dash: [4, 4] });
      Sim.line(ctx, [[x0, yTopEdge - 4], [x0, yBotEdge + 4]], { color: C.ink2, width: 1.2 });

      // walls / plates
      const off = Sim.reduced ? 0 : (g.k * v * t) % 16;
      if (pipe) {
        hatch(ctx, g.L, yTopEdge - 12, W, 12);
        hatch(ctx, g.L, yBotEdge, W, 12);
        Sim.text(ctx, 'pipe wall · v = 0', g.L + 2, yTopEdge - 22, { size: 12, color: C.ink2, weight: 600 });
        Sim.text(ctx, 'fastest on the axis', x0 + maxLen + 8, (yTopEdge + yBotEdge) / 2, { size: 11.5, color: C.indigo, weight: 650, bg: 'rgba(255,255,255,0.8)' });
        dimArrow(ctx, g.L - 16, yTopEdge, yBotEdge, 'd');
      } else {
        hatch(ctx, g.L, g.bot, W, 12);
        Sim.text(ctx, 'fixed plate · v = 0', g.L + 2, g.bot + 24, { size: 12, color: C.ink2, weight: 600 });
        // moving top plate with moving stripes
        const yp = yTopEdge - 12;
        ctx.save();
        ctx.fillStyle = C.ink2; ctx.fillRect(g.L, yp, W, 12);
        ctx.beginPath(); ctx.rect(g.L, yp, W, 12); ctx.clip();
        ctx.strokeStyle = 'rgba(255,255,255,0.35)'; ctx.lineWidth = 3;
        for (let x = g.L - 16 + off; x < g.R + 16; x += 16) { ctx.beginPath(); ctx.moveTo(x, yp + 12); ctx.lineTo(x + 8, yp); ctx.stroke(); }
        ctx.restore();
        Sim.text(ctx, 'moving plate · speed v', g.L + 2, yp - 13, { size: 12, color: C.ink, weight: 650 });
        Sim.arrow(ctx, g.R - 74, yp - 13, g.R - 4, yp - 13, { color: C.coral, width: 2.5, label: 'F', lx: -36, ly: -12, size: 12.5 });
        dimArrow(ctx, g.L - 16, yTopEdge, yBotEdge, 'd');
      }
    }

    const st = Sim.stage(host, { aspect: 4 / 3, minH: 260, maxH: 440, animate: true, draw });
    stages.push(st);

    const lblV = panel.querySelector('[data-lbl="v"]'), lblD = panel.querySelector('[data-lbl="d"]');
    const areaCtrl = panel.querySelector('[data-only="plates"]');
    const note = panel.querySelector('[data-r="note"]');
    const kGrad = panel.querySelector('[data-k="grad"]'), kStress = panel.querySelector('[data-k="stress"]');

    Sim.controls(panel, vals => {
      P = Object.assign({}, vals);
      const v = P['vis-v'] * 0.01, d = P['vis-d'] * 1e-3, eta = P['vis-eta'], A = P['vis-A'] * 1e-4;
      const pipe = P.mode === 'pipe';
      lblV.textContent = pipe ? 'Centre speed v' : 'Top plate speed v';
      lblD.textContent = pipe ? 'Pipe diameter d' : 'Film thickness d';
      areaCtrl.hidden = pipe;
      if (pipe) {
        const grad = 4 * v / d;
        kGrad.textContent = 'Gradient at wall'; kStress.textContent = 'Stress at wall';
        Sim.out(panel, 'grad', fmt(grad, ' s⁻¹'));
        Sim.out(panel, 'stress', fmt(eta * grad, ' Pa'));
        Sim.out(panel, 'F', '—');
        note.textContent = 'In a pipe the layers are nested cylinders. Speed is zero at the wall and greatest on the axis, giving a parabolic profile; the dye line bends into a curve.';
      } else {
        const grad = v / d;
        kGrad.textContent = 'Velocity gradient v/d'; kStress.textContent = 'Viscous stress ηv/d';
        Sim.out(panel, 'grad', fmt(grad, ' s⁻¹'));
        Sim.out(panel, 'stress', fmt(eta * grad, ' Pa'));
        Sim.out(panel, 'F', fmt(eta * A * grad, ' N'));
        note.textContent = 'Watch the purple dye line: it starts vertical and leans over, because higher layers move faster. Halve d and the gradient (and F) doubles.';
      }
      st.redraw();
    });
  }

  /* =================================================================
     2. Stokes' law — ball falling in a jar + live v–t graph
     ================================================================= */
  function initStokes() {
    const root = fig('sim-stokes'); if (!root) return;
    const host = root.querySelector('.sim-stage'), panel = root.querySelector('.sim-panel');
    const TPS = 0.45, TMAX = 8;            // display seconds per τ; graph length in τ
    let P = null;
    const state = { tp: 0, running: false, done: false };
    let ghosts = [];

    function phys() {
      const r = P['st-r'] * 1e-3, rho = P['st-rho'], sig = P['st-sig'], eta = P['st-eta'];
      const V = 4 / 3 * Math.PI * r * r * r;
      let vt = 2 * r * r * (rho - sig) * G / (9 * eta);
      if (Math.abs(rho - sig) < 1) vt = 0;
      return { r, rho, sig, eta, vt, tau: 2 * rho * r * r / (9 * eta), W: V * rho * G, B: V * sig * G };
    }
    const sFrac = tp => clamp((tp - 1 + Math.exp(-tp)) / (TMAX - 1), 0, 1);

    function draw(ctx, w, h, t, dt) {
      if (!P) return;
      const C = Sim.C, ph = phys();
      if (state.running && dt > 0) {
        state.tp += dt / TPS;
        if (state.tp >= TMAX) { state.tp = TMAX; state.running = false; state.done = true; }
      }
      const tp = state.tp, vr = 1 - Math.exp(-tp);
      const rising = ph.vt < 0, neutral = ph.vt === 0;

      // ---- jar
      const jx = 10, jw = clamp(w * 0.36, 112, 210), jy = 12, jb = h - 14, liqTop = jy + 20;
      ctx.fillStyle = C.liquid; ctx.fillRect(jx, liqTop, jw, jb - liqTop);
      Sim.line(ctx, [[jx, liqTop], [jx + jw, liqTop]], { color: C.liquidEdge, width: 1.5 });
      Sim.line(ctx, [[jx, jy], [jx, jb], [jx + jw, jb], [jx + jw, jy]], { color: C.ink2, width: 2 });
      Sim.text(ctx, 'liquid σ, η', jx + jw - 6, jb - 12, { size: 11, color: C.water, align: 'right', weight: 600 });

      const br = 5 + (P['st-r'] - 0.5) / 2.5 * 11;
      const yA = liqTop + 52, yB = jb - 52;
      const f = sFrac(tp);
      let by = neutral ? (yA + yB) / 2 : rising ? yB - f * (yB - yA) : yA + f * (yB - yA);
      const bx = jx + jw / 2;

      // ball
      ctx.save();
      ctx.beginPath(); ctx.arc(bx, by, br, 0, Math.PI * 2);
      if (ph.rho < ph.sig) { ctx.fillStyle = 'rgba(255,255,255,0.9)'; ctx.fill(); ctx.strokeStyle = C.water; ctx.lineWidth = 1.5; ctx.stroke(); }
      else {
        const gr = ctx.createRadialGradient(bx - br * 0.4, by - br * 0.4, 1, bx, by, br);
        gr.addColorStop(0, '#C9CFDB'); gr.addColorStop(1, C.ink2);
        ctx.fillStyle = gr; ctx.fill();
      }
      ctx.restore();

      // force arrows (scaled to the larger of W, B)
      const sc = 44 / Math.max(ph.W, ph.B);
      const lenW = ph.W * sc, lenB = ph.B * sc, lenF = Math.abs(ph.W - ph.B) * vr * sc;
      const moving = tp > 0 && !neutral;
      if (!rising) {
        Sim.arrow(ctx, bx, by + br, bx, by + br + lenW, { color: C.coral, width: 2.5 });
        Sim.text(ctx, 'W', bx + 7, by + br + lenW - 4, { size: 12, weight: 700, color: C.coral });
        Sim.arrow(ctx, bx - 7, by - br, bx - 7, by - br - lenB, { color: C.water, width: 2.5 });
        Sim.text(ctx, 'B', bx - 13, by - br - lenB + 4, { size: 12, weight: 700, color: C.water, align: 'right' });
        if (moving && lenF > 2) {
          Sim.arrow(ctx, bx + 7, by - br, bx + 7, by - br - lenF, { color: C.plum, width: 2.5 });
          Sim.text(ctx, 'Fᵥ', bx + 13, by - br - lenF + 4, { size: 12, weight: 700, color: C.plum });
        }
      } else {
        Sim.arrow(ctx, bx - 7, by + br, bx - 7, by + br + lenW, { color: C.coral, width: 2.5 });
        Sim.text(ctx, 'W', bx - 13, by + br + lenW - 4, { size: 12, weight: 700, color: C.coral, align: 'right' });
        Sim.arrow(ctx, bx, by - br, bx, by - br - lenB, { color: C.water, width: 2.5 });
        Sim.text(ctx, 'B', bx + 7, by - br - lenB + 4, { size: 12, weight: 700, color: C.water });
        if (moving && lenF > 2) {
          Sim.arrow(ctx, bx + 7, by + br, bx + 7, by + br + lenF, { color: C.plum, width: 2.5 });
          Sim.text(ctx, 'Fᵥ', bx + 13, by + br + lenF - 4, { size: 12, weight: 700, color: C.plum });
        }
      }
      const status = neutral ? 'ρ = σ: floats in place' : rising ? 'ρ < σ: it rises' : (tp === 0 ? 'press Drop' : vr > 0.99 ? 'W = B + Fᵥ' : 'speeding up');
      Sim.text(ctx, status, bx, jy + 8, { size: 11.5, weight: 650, color: C.ink2, align: 'center' });

      // ---- graph
      const gx = jx + jw + 44, gy = 30, gw = w - gx - 14, gh = h - gy - 40;
      if (gw < 60) return;
      const vtc = Math.abs(ph.vt) * 100;   // cm/s
      const ymax = niceMax(Math.max(vtc, ...ghosts.map(g => Math.abs(g)), 1e-9) * 1.15);
      const yf = v => { const s = Sim.sci(v, 2); return s; };
      const ax = Sim.axes(ctx, { x: gx, y: gy, w: gw, h: gh }, {
        xmin: 0, xmax: TMAX, ymin: 0, ymax,
        xticks: [0, 2, 4, 6, 8], yticks: [0, ymax / 2, ymax],
        xfmt: v => v ? v + 'τ' : '0', yfmt: yf, xlabel: 'time', ylabel: 'speed (cm/s)'
      });
      const curve = (vt, upto, color, width, dash) => {
        const pts = [];
        for (let i = 0; i <= 80; i++) { const x = upto * i / 80; pts.push([ax.X(x), ax.Y(vt * (1 - Math.exp(-x)))]); }
        Sim.line(ctx, pts, { color, width, dash });
      };
      ghosts.forEach(g => curve(Math.abs(g), TMAX, C.line2, 2, [5, 4]));
      if (vtc > 0) {
        Sim.line(ctx, [[gx, ax.Y(vtc)], [gx + gw, ax.Y(vtc)]], { color: C.accent, width: 1.2, dash: [3, 4] });
        Sim.text(ctx, 'vₜ = ' + Sim.sci(vtc, 2) + ' cm/s', gx + gw, ax.Y(vtc) - 10, { size: 11.5, weight: 650, color: C.accent, align: 'right' });
      }
      if (tp > 0) {
        curve(vtc, tp, C.accent, 2.5);
        ctx.beginPath(); ctx.arc(ax.X(tp), ax.Y(vtc * vr), 4, 0, Math.PI * 2); ctx.fillStyle = C.accent; ctx.fill();
        if (tp > 4.6 && vtc > 0) Sim.text(ctx, 'net force ≈ 0', ax.X(5.2), ax.Y(vtc) + 16, { size: 11, color: C.ink2, align: 'center' });
      }
    }

    const st = Sim.stage(host, { aspect: 4 / 3, minH: 300, maxH: 460, animate: true, draw });
    stages.push(st);

    const reset = () => { state.tp = 0; state.running = false; state.done = false; };
    const keepGhost = () => { if (state.tp > 0.5 && state.runVt !== undefined) { ghosts.push(state.runVt); if (ghosts.length > 3) ghosts.shift(); } };
    Sim.controls(panel, vals => {
      if (P) keepGhost();
      P = Object.assign({}, vals);
      const ph = phys();
      reset();
      Sim.out(panel, 'vt', ph.vt === 0 ? '0 (floats)' : Sim.sci(Math.abs(ph.vt) * 100, 2) + ' cm/s ' + (ph.vt > 0 ? '↓' : '↑'));
      Sim.out(panel, 'tau', Sim.sci(ph.tau * 1000, 2) + ' ms');
      Sim.out(panel, 'fv', Sim.sci(Math.abs(ph.W - ph.B) * 1000, 2) + ' mN');
      st.redraw();
    });
    root.querySelector('[data-act="drop"]').addEventListener('click', () => {
      const ph = phys();
      keepGhost();
      state.runVt = ph.vt * 100;
      state.tp = 0; state.done = false; state.running = true;
      if (Sim.reduced) { state.tp = TMAX; state.running = false; state.done = true; }
      st.redraw();
    });
    root.querySelector('[data-act="reset"]').addEventListener('click', () => { reset(); ghosts = []; st.redraw(); });
  }

  /* =================================================================
     3. Reynolds number — dye thread in a pipe
     ================================================================= */
  function initReynolds() {
    const root = fig('sim-reynolds'); if (!root) return;
    const host = root.querySelector('.sim-stage'), panel = root.querySelector('.sim-panel');
    let Re = 600, simT = 0, dye = [], tracers = [], needPrefill = true;
    const modes = [
      { a: 1.0, k: 2.2, m: 1 }, { a: 0.6, k: 4.1, m: 2 }, { a: 0.45, k: 6.3, m: 3 },
      { a: 0.3, k: 9.0, m: 2 }, { a: 0.25, k: 12.0, m: 4 }
    ].map((md, i) => Object.assign(md, { ph: Math.random() * 6.28, i }));

    function beta(t) {
      if (Re < 1000) return 0;
      if (Re < 2000) {
        const base = 0.45 * (Re - 1000) / 1000;
        const s = 0.5 + 0.5 * Math.sin(t * 1.1 + 3 * Math.sin(t * 0.33));
        return base * s * s * 1.6;
      }
      return 0.5 + 0.5 * Math.min(1, (Re - 2000) / 1500);
    }
    function geo(w, h) {
      const L = 8, R = w - 8, yT = 40, yB = h - 66;
      return { L, R, yT, yB, H: yB - yT, yc: (yT + yB) / 2, xn: L + 28, U: 55 + 55 * Re / 4000 };
    }
    function meanU(eta, U, b) {
      const lam = 1.5 * U * (1 - eta * eta);
      const tur = 1.15 * U * Math.pow(Math.max(0, 1 - Math.abs(eta)), 1 / 7);
      const m = Math.min(1, b * 1.4);
      return lam * (1 - m) + tur * m;
    }
    function step(dt, gm) {
      simT += dt;
      const b = beta(simT), H = gm.H, A = b * gm.U * 0.13;
      const adv = (p) => {
        const eta = clamp((p.y - gm.yc) / (H / 2), -1, 1);
        let vx = meanU(eta, gm.U, b), vy = 0;
        if (A > 0) {
          const X = p.x / H, Y = (eta + 1) / 2;
          for (const md of modes) {
            const th = md.k * X - md.k * (gm.U / H) * 0.9 * simT + md.ph + 1.5 * Math.sin(0.3 * simT + md.i);
            const sy = Math.sin(md.m * Math.PI * Y), cy = Math.cos(md.m * Math.PI * Y);
            vx += A * md.a * Math.sin(th) * md.m * Math.PI * cy;
            vy += -A * md.a * md.k * Math.cos(th) * sy;
          }
          vy += (Math.random() - 0.5) * b * 160;
        }
        p.x += vx * dt; p.y += vy * dt;
        const lo = gm.yT + 2, hi = gm.yB - 2;
        if (p.y < lo) p.y = 2 * lo - p.y; if (p.y > hi) p.y = 2 * hi - p.y;
        p.y = clamp(p.y, lo, hi);
      };
      const n = Math.max(1, Math.round(dt * 140));
      for (let i = 0; i < n; i++) dye.push({ x: gm.xn + Math.random() * 3, y: gm.yc + (Math.random() - 0.5) * 1.2 });
      dye.forEach(adv);
      dye = dye.filter(p => p.x < gm.R);
      if (dye.length > 1600) dye.splice(0, dye.length - 1600);
      tracers.forEach(p => { adv(p); if (p.x > gm.R) { p.x = gm.L; p.y = gm.yT + Math.random() * gm.H; } });
    }
    function prefill(gm) {
      dye = []; simT = 0;
      for (let i = 0; i < 260; i++) step(1 / 30, gm);
    }

    function draw(ctx, w, h, t, dt) {
      const C = Sim.C, gm = geo(w, h);
      if (!tracers.length) for (let i = 0; i < 70; i++) tracers.push({ x: gm.L + Math.random() * (gm.R - gm.L), y: gm.yT + Math.random() * gm.H });
      if (Sim.reduced) { if (needPrefill) { prefill(gm); needPrefill = false; } }
      else if (dt > 0) step(dt, gm);

      // pipe
      ctx.fillStyle = C.liquid; ctx.fillRect(gm.L, gm.yT, gm.R - gm.L, gm.H);
      hatch(ctx, gm.L, gm.yT - 10, gm.R - gm.L, 10);
      hatch(ctx, gm.L, gm.yB, gm.R - gm.L, 10);
      ctx.fillStyle = 'rgba(58,140,203,0.45)';
      tracers.forEach(p => ctx.fillRect(p.x - 1.2, p.y - 1.2, 2.4, 2.4));
      // nozzle
      Sim.line(ctx, [[gm.xn - 2, gm.yT], [gm.xn - 2, gm.yc]], { color: C.ink2, width: 3 });
      // dye
      ctx.fillStyle = 'rgba(139,78,159,0.55)';
      dye.forEach(p => ctx.fillRect(p.x - 1.6, p.y - 1.6, 3.2, 3.2));

      // mean profile at right end
      const b = beta(simT), px = gm.R - 72;
      const prof = [];
      for (let i = 0; i <= 24; i++) {
        const eta = -1 + 2 * i / 24;
        prof.push([px + meanU(eta, gm.U, b) * 0.38, gm.yc + eta * gm.H / 2]);
      }
      Sim.line(ctx, [[px, gm.yT], [px, gm.yB]], { color: C.ink2, width: 1 });
      Sim.line(ctx, prof, { color: C.ink, width: 1.6 });
      for (let i = 1; i < 6; i++) {
        const eta = -1 + 2 * i / 6;
        Sim.arrow(ctx, px, gm.yc + eta * gm.H / 2, px + meanU(eta, gm.U, b) * 0.38, gm.yc + eta * gm.H / 2, { color: C.ink, width: 1.3, head: 6 });
      }

      // regime header
      const reg = Re < 1000 ? ['Laminar (streamline)', C.green] : Re <= 2000 ? ['Unsteady / transition', C.amber] : ['Turbulent', C.coral];
      Sim.text(ctx, reg[0] + ' · Re = ' + Re, gm.L + 2, 16, { size: 13, weight: 700, color: reg[1] });
      Sim.text(ctx, 'mean profile', gm.R - 2, 16, { size: 11, color: C.ink2, align: 'right' });

      // regime meter
      const mx0 = gm.L + 4, mx1 = gm.R - 4, my = h - 34;
      const X = v => mx0 + (mx1 - mx0) * v / 4000;
      ctx.fillStyle = C.greenSoft; ctx.fillRect(X(0), my, X(1000) - X(0), 10);
      ctx.fillStyle = C.amberSoft; ctx.fillRect(X(1000), my, X(2000) - X(1000), 10);
      ctx.fillStyle = C.coralSoft; ctx.fillRect(X(2000), my, X(4000) - X(2000), 10);
      Sim.text(ctx, 'laminar', (X(0) + X(1000)) / 2, my + 22, { size: 11, color: C.green, align: 'center', weight: 650 });
      Sim.text(ctx, 'unsteady', (X(1000) + X(2000)) / 2, my + 22, { size: 11, color: C.amber, align: 'center', weight: 650 });
      Sim.text(ctx, 'turbulent', (X(2000) + X(4000)) / 2, my + 22, { size: 11, color: C.coral, align: 'center', weight: 650 });
      Sim.text(ctx, '1000', X(1000), my - 8, { size: 11, color: C.muted, align: 'center', mono: true });
      Sim.text(ctx, '2000', X(2000), my - 8, { size: 11, color: C.muted, align: 'center', mono: true });
      const mxp = X(Re);
      ctx.beginPath(); ctx.moveTo(mxp, my + 11); ctx.lineTo(mxp - 6, my + 19); ctx.lineTo(mxp + 6, my + 19); ctx.closePath();
      ctx.fillStyle = C.ink; ctx.fill();
      Sim.line(ctx, [[mxp, my - 2], [mxp, my + 12]], { color: C.ink, width: 2 });
    }

    const st = Sim.stage(host, { aspect: 16 / 9, minH: 250, maxH: 360, animate: true, draw });
    stages.push(st);
    Sim.controls(panel, vals => {
      Re = vals['re-Re'];
      const reg = Re < 1000 ? 'Laminar' : Re <= 2000 ? 'Unsteady' : 'Turbulent';
      Sim.out(panel, 'regime', reg);
      Sim.out(panel, 'speed', (Re * 0.01).toFixed(1) + ' cm/s');
      needPrefill = true;
      st.redraw();
    });
  }

  /* =================================================================
     4a. Molecules — bulk vs surface, tap to move
     ================================================================= */
  function initMolecules() {
    const root = fig('sim-molecules'); if (!root) return;
    const host = root.querySelector('.sim-stage'), panel = root.querySelector('.sim-panel');
    const specials = [{ i: null, j: 5, name: 'A' }, { i: null, j: 0, name: 'B' }];
    let sel = 1, lat = null, dragging = false;

    function build(w, h) {
      const sp = clamp(w / 16, 20, 30), ys = Math.round(h * 0.3);
      const rows = [], cols = Math.ceil(w / sp) + 6;
      for (let j = 0; ; j++) {
        const y = ys + sp * 0.55 + j * sp * 0.866;
        if (y > h + 3 * sp) break;
        rows.push(y);
      }
      const visRows = rows.filter(y => y < h - sp * 0.5).length;
      const visCols = Math.floor(w / sp);
      lat = { sp, ys, rows, cols, visRows, visCols, w, h, Rr: 2.15 * sp };
      specials.forEach((s, k) => {
        if (s.i === null) s.i = Math.round((k ? 0.68 : 0.27) * visCols);
        s.i = clamp(s.i, 1, visCols - 1);
        s.j = clamp(s.j, 0, Math.max(0, visRows - 1));
      });
      if (specials[0].j < 3) specials[0].j = Math.min(Math.max(3, visRows - 2), visRows - 1);
    }
    const pos = (i, j) => ({ x: (i + (j % 2) * 0.5) * lat.sp, y: lat.rows[j] });
    function neighbours(s) {
      const p = pos(s.i, s.j), out = [];
      for (let j = Math.max(0, s.j - 3); j <= Math.min(lat.rows.length - 1, s.j + 3); j++) {
        for (let i = s.i - 4; i <= s.i + 4; i++) {
          if (i === s.i && j === s.j) continue;
          const q = pos(i, j), d = Math.hypot(q.x - p.x, q.y - p.y);
          if (d < lat.Rr) out.push({ x: q.x, y: q.y, d });
        }
      }
      let nx = 0, ny = 0;
      out.forEach(q => { nx += (q.x - p.x) / q.d; ny += (q.y - p.y) / q.d; });
      return { p, list: out, nx, ny, mag: Math.hypot(nx, ny) };
    }

    function draw(ctx, w, h, t) {
      if (!lat || lat.w !== w || lat.h !== h) build(w, h);
      const C = Sim.C, sp = lat.sp, ys = lat.ys;
      ctx.fillStyle = C.liquid; ctx.fillRect(0, ys, w, h - ys);
      Sim.line(ctx, [[0, ys], [w, ys]], { color: C.liquidEdge, width: 2 });
      Sim.text(ctx, 'AIR (no molecules pulling from above)', 10, 16, { size: 12, color: C.muted, weight: 600 });
      Sim.text(ctx, 'surface', w - 8, ys - 10, { size: 11.5, color: C.water, weight: 650, align: 'right' });

      const isSpecial = (i, j) => specials.some(s => s.i === i && s.j === j);
      const info = specials.map(neighbours);

      // range circles (behind molecules)
      info.forEach((nb, k) => {
        const p = nb.p;
        ctx.save();
        ctx.beginPath(); ctx.arc(p.x, p.y, lat.Rr, 0, Math.PI * 2); ctx.clip();
        ctx.fillStyle = 'rgba(214,96,74,0.13)'; ctx.fillRect(p.x - lat.Rr, p.y - lat.Rr, 2 * lat.Rr, ys - (p.y - lat.Rr));
        ctx.restore();
        ctx.save(); ctx.setLineDash([4, 4]); ctx.strokeStyle = k === sel ? C.accent : C.line2; ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.arc(p.x, p.y, lat.Rr, 0, Math.PI * 2); ctx.stroke(); ctx.restore();
      });

      // lattice molecules
      const jit = Sim.reduced ? 0 : 0.9;
      for (let j = 0; j < lat.rows.length; j++) {
        for (let i = -2; i < lat.cols; i++) {
          if (isSpecial(i, j)) continue;
          const p = pos(i, j);
          if (p.y > h + sp) continue;
          const x = p.x + jit * Math.sin(t * 2.3 + i * 1.7 + j * 0.9), y = p.y + jit * Math.cos(t * 2.1 + i * 0.7 + j * 1.3);
          ctx.beginPath(); ctx.arc(x, y, sp * 0.3, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(58,140,203,0.55)'; ctx.fill();
        }
      }

      // attraction arrows + net force for each special
      info.forEach((nb, k) => {
        const p = nb.p;
        nb.list.forEach(q => {
          const f = 0.62;
          Sim.arrow(ctx, p.x, p.y, p.x + (q.x - p.x) * f, p.y + (q.y - p.y) * f, { color: 'rgba(75,91,208,0.7)', width: 1.3, head: 6 });
        });
        ctx.beginPath(); ctx.arc(p.x, p.y, sp * 0.36, 0, Math.PI * 2);
        ctx.fillStyle = k === sel ? C.accent : C.indigo; ctx.fill();
        if (k === sel) { ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(139,78,159,0.35)'; ctx.beginPath(); ctx.arc(p.x, p.y, sp * 0.36 + 4, 0, Math.PI * 2); ctx.stroke(); }
        Sim.text(ctx, specials[k].name, p.x, p.y + 0.5, { size: 11.5, weight: 700, color: '#fff', align: 'center' });
        if (nb.mag > 0.05) {
          const s = 7.5;
          Sim.arrow(ctx, p.x, p.y + sp * 0.3, p.x + nb.nx * s, p.y + sp * 0.3 + nb.ny * s, { color: C.coral, width: 3.5, head: 11 });
        }
        const lab = nb.mag < 0.05 ? 'net force = 0' : 'net pull inward';
        const ly = nb.mag < 0.05 ? p.y + lat.Rr + 12 : p.y + sp * 0.3 + nb.ny * 7.5 + 14;
        Sim.text(ctx, lab, p.x, Math.min(ly, h - 10), { size: 11.5, weight: 700, color: nb.mag < 0.05 ? C.green : C.coral, align: 'center', bg: 'rgba(255,255,255,0.85)' });
      });

      const s = info[sel];
      Sim.out(panel, 'nb', String(s.list.length));
      Sim.out(panel, 'net', s.mag < 0.05 ? '0 (balanced)' : s.mag.toFixed(1) + ' units ↓');
    }

    const st = Sim.stage(host, { aspect: 16 / 9, minH: 250, maxH: 380, animate: true, draw });
    stages.push(st);
    st.canvas.classList.add('tap');

    function placeAt(pt) {
      if (!lat) return;
      const j = clamp(Math.round((pt.y - lat.rows[0]) / (lat.sp * 0.866)), 0, lat.visRows - 1);
      const i = clamp(Math.round(pt.x / lat.sp - (j % 2) * 0.5), 1, lat.visCols - 1);
      const other = specials[1 - sel];
      if (other.i === i && other.j === j) return;
      specials[sel].i = i; specials[sel].j = j;
      st.redraw();
    }
    function hit(pt) {
      for (let k = 0; k < 2; k++) {
        const p = pos(specials[k].i, specials[k].j);
        if (Math.hypot(pt.x - p.x, pt.y - p.y) < lat.sp * 0.7) return k;
      }
      return -1;
    }
    st.canvas.addEventListener('pointerdown', e => {
      const pt = st.toLocal(e), k = hit(pt);
      if (k >= 0) { sel = k; dragging = e.pointerType !== 'touch'; st.redraw(); }
      else placeAt(pt);
    });
    st.canvas.addEventListener('pointermove', e => { if (dragging) placeAt(st.toLocal(e)); });
    window.addEventListener('pointerup', () => { dragging = false; });

    const go = j => { if (!lat) return; const s = specials[sel], o = specials[1 - sel];
      s.j = clamp(j, 0, lat.visRows - 1); if (o.i === s.i && o.j === s.j) s.i = clamp(s.i + 2, 1, lat.visCols - 1); st.redraw(); };
    root.querySelector('[data-act="bulk"]').addEventListener('click', () => go(Math.min(5, lat.visRows - 2)));
    root.querySelector('[data-act="surface"]').addEventListener('click', () => go(0));
    root.querySelector('[data-act="second"]').addEventListener('click', () => go(1));
  }

  /* =================================================================
     4b. Soap film on a U-frame
     ================================================================= */
  function initFilm() {
    const root = fig('sim-film'); if (!root) return;
    const host = root.querySelector('.sim-stage'), panel = root.querySelector('.sim-panel');
    let P = null;

    function draw(ctx, w, h, t) {
      if (!P) return;
      const C = Sim.C;
      const L = P['fl-L'], dx = P['fl-x'];
      const s = Math.min((w - 110) / 10.2, (h - 84) / 10);
      const x0 = 28, yc = 22 + (h - 62) / 2;
      const yT = yc - L * s / 2, yB = yc + L * s / 2;
      const armEnd = x0 + 10.2 * s;
      const xs = x0 + (4 + dx) * s;

      // film
      const ph = Sim.reduced ? 0 : t * 0.25;
      const gr = ctx.createLinearGradient(x0, yT, xs, yB);
      gr.addColorStop(0, `rgba(139,78,159,${0.16 + 0.06 * Math.sin(ph)})`);
      gr.addColorStop(0.5, `rgba(58,140,203,${0.18 + 0.06 * Math.sin(ph + 2)})`);
      gr.addColorStop(1, `rgba(194,133,14,${0.16 + 0.06 * Math.sin(ph + 4)})`);
      ctx.fillStyle = gr; ctx.fillRect(x0, yT, xs - x0, yB - yT);
      // new area created
      if (dx > 0) {
        ctx.save(); ctx.setLineDash([4, 4]); ctx.strokeStyle = C.ink2; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(x0 + 4 * s, yT); ctx.lineTo(x0 + 4 * s, yB); ctx.stroke(); ctx.restore();
        if (dx * s > 64) Sim.text(ctx, 'new film', x0 + (4 + dx / 2) * s - 6, yB - 12, { size: 11.5, color: C.ink2, align: 'center', weight: 600 });
      }
      // frame (U)
      Sim.line(ctx, [[armEnd, yT], [x0, yT], [x0, yB], [armEnd, yB]], { color: C.ink, width: 4 });
      // slider
      Sim.line(ctx, [[xs, yT - 8], [xs, yB + 8]], { color: C.ink2, width: 5 });
      Sim.text(ctx, 'L', xs + 10, yT + 12, { size: 12, weight: 700, color: C.ink2 });

      // surface-tension pulls (into the film) and applied force (outward)
      const n = 4;
      for (let i = 0; i < n; i++) {
        const y = yT + (i + 0.5) / n * (yB - yT);
        Sim.arrow(ctx, xs - 3, y, xs - 3 - Math.min(26, 0.9 * s + 8), y, { color: C.plum, width: 2, head: 7 });
      }
      const Fpx = 18 + 70 * (P['fl-T'] * L) / (0.08 * 10);
      Sim.arrow(ctx, xs + 4, yc, xs + 4 + Fpx, yc, { color: C.coral, width: 3 });
      Sim.text(ctx, 'F = 2TL', xs + 8, yc + 16, { size: 12, weight: 700, color: C.coral });
      Sim.text(ctx, 'film pulls: TL (front) + TL (back)', x0 + 6, yB + 18, { size: 11.5, weight: 650, color: C.plum });
      if (dx > 0) dimArrowH(ctx, x0 + 4 * s, xs, yT - 14, 'Δx');
    }
    function dimArrowH(ctx, x1, x2, y, label) {
      const c = Sim.C.ink2;
      if (x2 - x1 < 10) return;
      Sim.arrow(ctx, (x1 + x2) / 2, y, x1, y, { color: c, width: 1.2, head: 6 });
      Sim.arrow(ctx, (x1 + x2) / 2, y, x2, y, { color: c, width: 1.2, head: 6 });
      Sim.text(ctx, label, (x1 + x2) / 2, y - 10, { size: 12, color: c, align: 'center', weight: 650 });
    }

    const st = Sim.stage(host, { aspect: 4 / 3, minH: 300, maxH: 440, animate: true, draw });
    stages.push(st);
    Sim.controls(panel, vals => {
      P = Object.assign({}, vals);
      const L = P['fl-L'] / 100, T = P['fl-T'], dx = P['fl-x'] / 100;
      const F = 2 * T * L;
      Sim.out(panel, 'F', fmt(F, ' N'));
      Sim.out(panel, 'W', fmt(F * dx, ' J'));
      Sim.out(panel, 'dA', (2 * P['fl-L'] * P['fl-x']).toFixed(1) + ' cm²');
      st.redraw();
    });
  }

  /* shared: meniscus height offset (y-up, relative to the contact line) across a tube of half-width r */
  function meniscusY(x, r, th) {
    const c = Math.cos(th);
    if (Math.abs(c) < 0.01) return 0;
    const Rm = r / Math.abs(c);
    return r * Math.tan(th) - Math.sign(c) * Math.sqrt(Math.max(0, Rm * Rm - x * x));
  }
  function glassTube(ctx, x, y1, y2, rp, wall) {
    const C = Sim.C;
    ctx.save();
    ctx.fillStyle = 'rgba(69,79,102,0.22)'; ctx.strokeStyle = C.ink2; ctx.lineWidth = 1.2;
    ctx.fillRect(x - rp - wall, y1, wall, y2 - y1); ctx.strokeRect(x - rp - wall, y1, wall, y2 - y1);
    ctx.fillRect(x + rp, y1, wall, y2 - y1); ctx.strokeRect(x + rp, y1, wall, y2 - y1);
    ctx.restore();
  }
  /* liquid column inside a tube from yBottom up to a meniscus whose contact line is at yc */
  function column(ctx, tx, rp, yBottom, yc, th, color) {
    color = color || column.fill;
    const pts = [[tx - rp, yBottom], [tx - rp, yc]];
    for (let i = 0; i <= 24; i++) { const x = -rp + 2 * rp * i / 24; pts.push([tx + x, yc - meniscusY(x, rp, th)]); }
    pts.push([tx + rp, yc], [tx + rp, yBottom]);
    Sim.line(ctx, pts, { color: 'none', fill: color || 'rgba(58,140,203,0.45)', close: true });
    const top = pts.slice(2, 27);
    Sim.line(ctx, top, { color: Sim.C.water, width: 1.8 });
  }

  /* =================================================================
     5. Contact angle — drop on a solid + capillary meniscus
     ================================================================= */
  function initContact() {
    const root = fig('sim-contact'); if (!root) return;
    const host = root.querySelector('.sim-stage'), panel = root.querySelector('.sim-panel');
    let deg = 30;

    function draw(ctx, w, h) {
      const C = Sim.C, th = deg * Math.PI / 180, pw = w / 2;
      // ---------- left: drop on a solid
      ctx.save(); ctx.beginPath(); ctx.rect(0, 0, pw - 1, h); ctx.clip();
      const ys = Math.round(h * 0.6), cx = pw / 2;
      hatch(ctx, 10, ys, pw - 20, 22);
      Sim.text(ctx, 'Drop on a solid', 12, 14, { size: 12.5, weight: 700, color: C.ink });
      const Rb = Math.min(pw * 0.21, h * 0.25), A0 = Math.PI * Rb * Rb / 2, amax = pw * 0.44;
      let px = cx + amax;
      if (deg < 1) {
        ctx.fillStyle = 'rgba(58,140,203,0.45)'; ctx.fillRect(cx - amax, ys - 3, 2 * amax, 3);
      } else {
        let R = Math.sqrt(A0 / (th - Math.sin(th) * Math.cos(th)));
        if (R * Math.sin(th) > amax && deg < 90) R = amax / Math.sin(th);
        const a = R * Math.sin(th), cyc = ys + R * Math.cos(th);
        px = cx + a;
        ctx.save();
        ctx.beginPath(); ctx.rect(0, 0, pw, ys); ctx.clip();
        ctx.beginPath(); ctx.arc(cx, cyc, R, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(58,140,203,0.4)'; ctx.fill();
        ctx.strokeStyle = C.water; ctx.lineWidth = 2; ctx.stroke();
        ctx.restore();
      }
      // tangent + angle
      const dx = -Math.cos(th), dy = -Math.sin(th);
      Sim.line(ctx, [[px - dx * 26, ys - dy * 26], [px + dx * 62, ys + dy * 62]], { color: C.ink, width: 1.4, dash: [5, 4] });
      Sim.line(ctx, [[px, ys], [px - 50, ys]], { color: C.accent, width: 2.5 });
      ctx.save(); ctx.strokeStyle = C.accent; ctx.lineWidth = 2.5;
      ctx.beginPath(); ctx.arc(px, ys, 22, Math.PI, Math.PI + Math.max(th, 0.001)); ctx.stroke(); ctx.restore();
      const la = Math.PI + th / 2;
      Sim.text(ctx, 'θ', px + Math.cos(la) * 34, ys + Math.sin(la) * 34 - (deg < 20 ? 6 : 0), { size: 14, weight: 700, color: C.accent, align: 'center' });
      const wets = deg < 89.5, flat = Math.abs(deg - 90) < 0.5;
      const msg = flat ? 'adhesion ≈ cohesion' : wets ? 'adhesion > cohesion: spreads' : 'cohesion > adhesion: beads up';
      Sim.text(ctx, msg, cx, ys + 38, { size: 12, weight: 650, color: wets ? C.green : flat ? C.ink2 : C.coral, align: 'center' });
      ctx.restore();

      // divider
      Sim.line(ctx, [[pw, 12], [pw, h - 12]], { color: C.line, width: 1 });

      // ---------- right: capillary tube
      const x0 = pw + 12, x1 = w - 10, yL = Math.round(h * 0.56), yb = h - 12;
      const tx = pw + pw * 0.48, rp = clamp(pw * 0.07, 10, 18), wall = 4;
      const tTop = 48, tBot = h - 24;
      const hmax = Math.min(yL - tTop - 30, tBot - yL - 18);
      const level = hmax * Math.cos(th);
      const yc = yL - level;
      Sim.text(ctx, 'Capillary tube', x0 + 2, 14, { size: 12.5, weight: 700, color: C.ink });
      ctx.fillStyle = 'rgba(58,140,203,0.3)'; ctx.fillRect(x0, yL, x1 - x0, yb - yL);
      Sim.line(ctx, [[x0, yL], [x1, yL]], { color: C.liquidEdge, width: 1.5 });
      Sim.line(ctx, [[x0, yL - 30], [x0, yb], [x1, yb], [x1, yL - 30]], { color: C.ink2, width: 2 });
      ctx.fillStyle = '#F8F9FC'; ctx.fillRect(tx - rp, tTop, 2 * rp, tBot - tTop);
      column.fill = null;
      column(ctx, tx, rp, tBot, yc, th);
      glassTube(ctx, tx, tTop, tBot, rp, wall);
      if (Math.abs(level) > 12) {
        const ax = tx + rp + wall + 16;
        Sim.line(ctx, [[tx + rp + wall, yc], [ax + 8, yc]], { color: C.ink2, width: 1, dash: [3, 3] });
        dimArrow(ctx, ax, yc, yL, '', C.ink2);
        Sim.text(ctx, level > 0 ? 'rises' : 'falls', ax + 8, (yc + yL) / 2, { size: 12, weight: 700, color: level > 0 ? C.green : C.coral });
      }
      const men = flat ? 'flat' : wets ? 'concave' : 'convex';
      Sim.text(ctx, men + ' meniscus', tx, 32, { size: 11.5, weight: 650, color: C.ink2, align: 'center' });
    }

    const st = Sim.stage(host, { aspect: 16 / 10, minH: 260, maxH: 400, draw });
    stages.push(st);
    Sim.controls(panel, vals => {
      deg = vals['ca-th'];
      const flat = Math.abs(deg - 90) < 0.5, wets = deg < 89.5;
      Sim.out(panel, 'wet', flat ? 'Neutral' : wets ? 'Yes' : 'No');
      Sim.out(panel, 'men', flat ? 'Flat' : wets ? 'Concave' : 'Convex');
      Sim.out(panel, 'cap', flat ? 'No change' : wets ? 'Rises' : 'Falls');
      st.redraw();
    });
    root.querySelectorAll('[data-preset]').forEach(b => b.addEventListener('click', () => {
      const inp = root.querySelector('#ca-th');
      inp.value = b.dataset.preset; inp.dispatchEvent(new Event('input'));
    }));
  }

  /* =================================================================
     6a. Drops & bubbles — surfaces and force balance on a half
     ================================================================= */
  function initBubbles() {
    const root = fig('sim-bubbles'); if (!root) return;
    const host = root.querySelector('.sim-stage'), panel = root.querySelector('.sim-panel');
    let P = null;
    const nSurf = k => (k === 'soap' ? 2 : 1);

    function body(ctx, cx, cy, rv, kind, half) {
      const C = Sim.C;
      const a0 = half ? -Math.PI / 2 : 0, a1 = half ? Math.PI / 2 : Math.PI * 2;
      ctx.save();
      if (kind === 'drop') {
        ctx.beginPath(); ctx.arc(cx, cy, rv, a0, a1); if (half) ctx.closePath();
        ctx.fillStyle = 'rgba(58,140,203,0.38)'; ctx.fill(); ctx.strokeStyle = C.water; ctx.lineWidth = 2.5; ctx.stroke();
      } else if (kind === 'soap') {
        ctx.beginPath(); ctx.arc(cx, cy, rv, a0, a1); if (half) ctx.closePath();
        ctx.fillStyle = 'rgba(139,78,159,0.05)'; ctx.fill();
        ctx.beginPath(); ctx.arc(cx, cy, rv, a0, a1); ctx.arc(cx, cy, rv - 7, a1, a0, true); ctx.closePath();
        ctx.fillStyle = 'rgba(139,78,159,0.22)'; ctx.fill();
        ctx.strokeStyle = C.plum; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(cx, cy, rv, a0, a1); ctx.stroke();
        ctx.beginPath(); ctx.arc(cx, cy, rv - 7, a0, a1); ctx.stroke();
        if (half) Sim.line(ctx, [[cx, cy - rv], [cx, cy + rv]], { color: C.line2, width: 1, dash: [3, 3] });
      } else {
        ctx.beginPath(); ctx.arc(cx, cy, rv, a0, a1); if (half) ctx.closePath();
        ctx.fillStyle = 'rgba(255,255,255,0.95)'; ctx.fill(); ctx.strokeStyle = C.water; ctx.lineWidth = 2.5; ctx.stroke();
      }
      ctx.restore();
    }

    function draw(ctx, w, h) {
      if (!P) return;
      const C = Sim.C, kind = P.kind, pw = w / 2, n = nSurf(kind);
      const R = P['db-R'];
      const rv = Math.min(pw * 0.33, (h - 90) * 0.4) * (0.6 + 0.4 * Math.log(R / 0.5) / Math.log(60));
      const cy = 30 + (h - 70) / 2;
      if (kind === 'air') { ctx.fillStyle = C.liquid; ctx.fillRect(8, 24, w - 16, h - 64); }

      // left: whole object
      const cx = pw / 2;
      body(ctx, cx, cy, rv, kind, false);
      Sim.text(ctx, 'Whole', 12, 12, { size: 12.5, weight: 700, color: C.ink });
      Sim.text(ctx, 'P_in', cx, cy - 8, { size: 12, weight: 700, color: C.ink, align: 'center' });
      Sim.line(ctx, [[cx, cy + 4], [cx + rv * 0.7071, cy + 4 + rv * 0.7071 - 4]], { color: C.ink2, width: 1.2 });
      Sim.text(ctx, 'r', cx + rv * 0.32, cy + rv * 0.4 + 8, { size: 12, weight: 700, color: C.ink2 });
      Sim.text(ctx, 'P_out', 14, h - 50, { size: 12, weight: 700, color: C.ink2 });
      const sLab = kind === 'drop' ? '1 surface (liquid–air)' : kind === 'soap' ? '2 surfaces: outer + inner' : '1 surface (liquid–air)';
      Sim.text(ctx, sLab, cx, Math.max(cy - rv - 12, 30), { size: 11.5, weight: 700, color: kind === 'soap' ? C.plum : C.water, align: 'center', bg: 'rgba(255,255,255,0.85)' });

      Sim.line(ctx, [[pw, 10], [pw, h - 50]], { color: C.line, width: 1 });

      // right: right half, force balance
      const fx = pw + pw * 0.34;
      body(ctx, fx, cy, rv, kind, true);
      Sim.text(ctx, 'Cut in half: right half', pw + 10, 12, { size: 12.5, weight: 700, color: C.ink });
      for (let k = -1; k <= 1; k++) {
        const y = cy + k * rv * 0.45;
        Sim.arrow(ctx, fx + 3, y, fx + 3 + Math.max(16, rv * 0.55), y, { color: C.ink, width: 2, head: 7 });
      }
      // rim pulls (to the left), one per surface
      const len = 30;
      [[cy - rv, 1], [cy + rv, -1]].forEach(([y, sgn]) => {
        Sim.arrow(ctx, fx, y, fx - len, y, { color: C.plum, width: 2.5, head: 8 });
        if (n === 2) Sim.arrow(ctx, fx, y + sgn * 7, fx - len, y + sgn * 7, { color: C.plum, width: 2.5, head: 8 });
      });
      Sim.text(ctx, (n === 2 ? '2 × ' : '') + 'T·2πr', fx - len / 2, cy - rv - 14, { size: 12, weight: 700, color: C.plum, align: 'center' });
      Sim.text(ctx, 'ΔP·πr²', fx + Math.max(16, rv * 0.55) + 8, cy, { size: 12, weight: 700, color: C.ink });

      // equation
      const eq = n === 2 ? 'ΔP·πr² = 2·T·2πr   ⇒   ΔP = 4T/r' : 'ΔP·πr² = T·2πr   ⇒   ΔP = 2T/r';
      Sim.text(ctx, eq, w / 2, h - 22, { size: 13, weight: 700, color: C.accent, align: 'center', mono: true });
    }

    const st = Sim.stage(host, { aspect: 16 / 10, minH: 270, maxH: 400, draw });
    stages.push(st);
    Sim.controls(panel, vals => {
      P = Object.assign({}, vals);
      const n = nSurf(P.kind), r = P['db-R'] * 1e-3, T = P['db-T'];
      Sim.out(panel, 'n', String(n));
      Sim.out(panel, 'P', Sim.sci(2 * n * T / r, 2) + ' Pa');
      Sim.out(panel, 'E', Sim.sci(n * 4 * Math.PI * r * r * T, 2) + ' J');
      st.redraw();
    });
  }

  /* =================================================================
     6b. Two soap bubbles joined through a valve
     ================================================================= */
  function initConnect() {
    const root = fig('sim-connect'); if (!root) return;
    const host = root.querySelector('.sim-stage'), panel = root.querySelector('.sim-panel');
    const a = 0.8, T = 0.03, K = 22;
    const S = { h1: 0, h2: 0, open: false, done: false, Vtot: 0 };
    const vol = hc => Math.PI * hc * (3 * a * a + hc * hc) / 6;
    const rad = hc => (a * a + hc * hc) / (2 * hc);
    const invV = V => { let hc = Math.max(0.05, Math.cbrt(6 * V / Math.PI)); for (let i = 0; i < 30; i++) { hc -= (vol(hc) - V) / (Math.PI * (a * a + hc * hc) / 2); hc = Math.max(1e-3, hc); } return hc; };
    const hOf = r => r + Math.sqrt(Math.max(0, r * r - a * a));
    let P = null;

    function reset() {
      S.h1 = hOf(P['cb-r1']); S.h2 = hOf(P['cb-r2']);
      S.Vtot = vol(S.h1) + vol(S.h2); S.open = false; S.done = false;
    }
    function step(dt) {
      if (!S.open || S.done) return;
      for (let k = 0; k < 4; k++) {
        const f = 1 / rad(S.h1) - 1 / rad(S.h2);
        if (Math.abs(f) < 0.002) { S.done = true; break; }
        let V1 = vol(S.h1) - K * f * dt / 4;
        V1 = clamp(V1, 1e-3, S.Vtot - 1e-3);
        S.h1 = invV(V1); S.h2 = invV(S.Vtot - V1);
      }
    }
    function bubble(ctx, cx, my, s, hc, label, sub) {
      const C = Sim.C, R = rad(hc), cyU = hc - R, phi0 = Math.atan2(R - hc, a);
      const pts = [];
      for (let i = 0; i <= 60; i++) {
        const p = phi0 + (Math.PI - 2 * phi0) * i / 60;
        pts.push([cx + R * Math.cos(p) * s, my - (cyU + R * Math.sin(p)) * s]);
      }
      Sim.line(ctx, pts, { color: C.plum, width: 2, fill: 'rgba(139,78,159,0.10)', close: true });
      const topY = my - hc * s;
      Sim.text(ctx, label, cx, Math.max(12, topY - 26), { size: 12.5, weight: 700, color: C.ink, align: 'center' });
      Sim.text(ctx, sub, cx, Math.max(26, topY - 11), { size: 11.5, weight: 600, color: C.ink2, align: 'center', mono: true });
    }

    function draw(ctx, w, h, t, dt) {
      if (!P) return;
      const C = Sim.C;
      if (dt > 0) step(dt);
      const x1 = w * 0.27, x2 = w * 0.7, my = h - 74, py = h - 34;
      const s = Math.min((my - 40) / 10.4, (x2 - x1) / 8.3, (w - x2 - 6) / 5.2, (x1 - 6) / 3.1);
      const ap = a * s;
      // pipe & stubs
      ctx.save(); ctx.fillStyle = '#F3F4F8'; ctx.strokeStyle = C.ink2; ctx.lineWidth = 2;
      const pt = Math.max(6, ap * 0.7);
      ctx.fillRect(x1 - ap, my, 2 * ap, py - my); ctx.fillRect(x2 - ap, my, 2 * ap, py - my);
      ctx.fillRect(x1 - ap, py - pt, x2 - x1 + 2 * ap, 2 * pt);
      ctx.beginPath();
      ctx.moveTo(x1 - ap, my); ctx.lineTo(x1 - ap, py + pt); ctx.lineTo(x2 + ap, py + pt); ctx.lineTo(x2 + ap, my);
      ctx.moveTo(x1 + ap, my); ctx.lineTo(x1 + ap, py - pt); ctx.lineTo(x2 - ap, py - pt); ctx.lineTo(x2 - ap, my);
      ctx.stroke(); ctx.restore();
      // valve
      const vx = (x1 + x2) / 2;
      ctx.beginPath(); ctx.arc(vx, py, pt + 5, 0, Math.PI * 2); ctx.fillStyle = C.surface; ctx.fill();
      ctx.strokeStyle = C.ink; ctx.lineWidth = 2; ctx.stroke();
      if (S.open) Sim.line(ctx, [[vx - pt - 3, py], [vx + pt + 3, py]], { color: C.green, width: 3 });
      else Sim.line(ctx, [[vx, py - pt - 3], [vx, py + pt + 3]], { color: C.coral, width: 3 });
      Sim.text(ctx, S.open ? 'valve open' : 'valve closed', vx, py + pt + 16, { size: 11.5, weight: 650, color: S.open ? C.green : C.coral, align: 'center' });

      const R1 = rad(S.h1), R2 = rad(S.h2);
      const p1 = 4 * T / (R1 / 100), p2 = 4 * T / (R2 / 100);
      bubble(ctx, x1, my, s, S.h1, 'Bubble 1', 'ΔP ' + p1.toFixed(1) + ' Pa');
      bubble(ctx, x2, my, s, S.h2, 'Bubble 2', 'ΔP ' + p2.toFixed(1) + ' Pa');
      if (S.open && Math.abs(S.h1 - a) < 0.1) Sim.text(ctx, 'hemisphere: highest pressure', x1, my + 14, { size: 11, weight: 650, color: C.coral, align: 'center', bg: 'rgba(255,255,255,0.9)' });

      // flow chevrons
      if (S.open && !S.done) {
        const dir = p1 > p2 ? 1 : -1, span = x2 - x1 - 2 * pt - 20;
        for (let k = 0; k < 4; k++) {
          const u = ((k / 4) + (Sim.reduced ? 0 : t * 0.6)) % 1;
          const x = dir > 0 ? x1 + 10 + u * span : x2 - 10 - u * span;
          if (Math.abs(x - vx) < pt + 8) continue;
          Sim.arrow(ctx, x - dir * 6, py, x + dir * 6, py, { color: C.accent, width: 2, head: 6 });
        }
      }
      if (S.done) Sim.text(ctx, 'Equilibrium: both caps have the same radius of curvature', 10, 14, { size: 11.5, weight: 700, color: C.green });

      Sim.out(panel, 'p1', p1.toFixed(1) + ' Pa');
      Sim.out(panel, 'p2', p2.toFixed(1) + ' Pa');
      Sim.out(panel, 'flow', !S.open ? 'valve closed' : S.done ? 'stopped' : (p1 > p2 ? '1 → 2' : '2 → 1'));
    }

    const st = Sim.stage(host, { aspect: 16 / 10, minH: 280, maxH: 420, animate: true, draw });
    stages.push(st);
    Sim.controls(panel, vals => { P = Object.assign({}, vals); reset(); st.redraw(); });
    root.querySelector('[data-act="open"]').addEventListener('click', () => {
      if (S.done) reset();
      S.open = true;
      if (Sim.reduced) { for (let i = 0; i < 20000 && !S.done; i++) step(0.02); }
      st.redraw();
    });
    root.querySelector('[data-act="reset"]').addEventListener('click', () => { reset(); st.redraw(); });
  }

  /* =================================================================
     7. Capillary tube lab
     ================================================================= */
  function initCapillary() {
    const root = fig('sim-capillary'); if (!root) return;
    const host = root.querySelector('.sim-stage'), panel = root.querySelector('.sim-panel');
    const note = panel.querySelector('[data-r="note"]');
    let P = null, cur = [0, 0, 0], snap = true;

    function phys() {
      const r = P['cp-r'] * 1e-3, th = P['cp-th'] * Math.PI / 180, T = P['cp-T'], rho = P['cp-rho'];
      const c = Math.abs(P['cp-th'] - 90) < 0.5 ? 0 : Math.cos(th);
      const h = 2 * T * c / (r * rho * G);          // m
      return { r, th, T, rho, c, h, hc: h * 100, R: c === 0 ? Infinity : r / Math.abs(c), W: 2 * Math.PI * r * T * c };
    }
    const cm = x => {
      const a = Math.abs(x);
      return (a >= 10 ? x.toFixed(1) : a >= 1 ? x.toFixed(2) : x.toFixed(3)) + ' cm';
    };

    function ruler(ctx, x, yL, sc, Hview, up) {
      const C = Sim.C, step = niceMax(Hview / 5);
      const dir = up ? -1 : 1;
      Sim.line(ctx, [[x, yL], [x, yL + dir * Hview * sc]], { color: C.ink2, width: 1.2 });
      for (let v = 0; v <= Hview + 1e-9; v += step) {
        const y = yL + dir * v * sc;
        Sim.line(ctx, [[x - 4, y], [x + 4, y]], { color: C.ink2, width: 1.2 });
        Sim.text(ctx, +v.toPrecision(3) + '', x - 7, y, { size: 11, color: C.muted, align: 'right', mono: true });
      }
      Sim.text(ctx, 'cm', x + 8, yL + dir * Hview * sc + (up ? -2 : 2), { size: 11, color: C.muted, weight: 600 });
    }

    function draw(ctx, w, h, t, dt) {
      if (!P) return;
      const C = Sim.C, ph = phys(), mode = P.mode;
      const up = ph.hc >= 0, heavy = ph.rho > 5000;
      column.fill = heavy ? 'rgba(115,124,145,0.55)' : null;
      let Hview = niceMax(Math.max(Math.abs(ph.hc) * 1.2, 0.5));
      const yL = up ? h - 62 : 76;
      let sc = up ? (yL - 46) / Hview : (h - 40 - yL) / Hview;
      const rp = clamp(3 + P['cp-r'] * 5, 5, 15), wall = 3;

      // trough
      const tx0 = 12, tx1 = w - 12, yb = h - 12;
      ctx.fillStyle = heavy ? 'rgba(115,124,145,0.35)' : 'rgba(58,140,203,0.3)'; ctx.fillRect(tx0, yL, tx1 - tx0, yb - yL);
      Sim.line(ctx, [[tx0, yL], [tx1, yL]], { color: heavy ? C.muted : C.liquidEdge, width: 1.5 });
      Sim.line(ctx, [[tx0, Math.min(yL - 24, h - 80)], [tx0, yb], [tx1, yb], [tx1, Math.min(yL - 24, h - 80)]], { color: C.ink2, width: 2 });
      ruler(ctx, 44, yL, sc, Hview, up);

      const ease = (i, target) => {
        if (snap || Sim.reduced || !(dt > 0)) { if (snap || Sim.reduced) cur[i] = target; }
        else cur[i] += (target - cur[i]) * Math.min(1, dt * 3.5);
        return cur[i];
      };
      const label = (txt, x, y, color, align) => Sim.text(ctx, txt, x, y, { size: 12, weight: 700, color: color || C.ink, align: align || 'left', bg: 'rgba(255,255,255,0.85)' });

      if (mode === 'compare') {
        const xs = [w * 0.4, w * 0.6, w * 0.8], rb = clamp(2 + P['cp-r'] * 3, 3.5, 7);
        xs.forEach((x, i) => {
          const k = i + 1, rpi = rb * k, tgt = ph.hc / k;
          const hcur = ease(i, tgt);
          const top = up ? yL - Hview * sc - 4 : 30, bot = up ? yL + 34 : h - 28;
          ctx.fillStyle = '#F8F9FC'; ctx.fillRect(x - rpi, top, 2 * rpi, bot - top);
          column(ctx, x, rpi, bot, yL - hcur * sc, ph.c === 0 ? Math.PI / 2 : ph.th);
          glassTube(ctx, x, top, bot, rpi, wall);
          Sim.text(ctx, k === 1 ? 'r' : k + 'r', x, top - 10, { size: 12, weight: 700, color: C.ink2, align: 'center' });
          if (Math.abs(hcur * sc) > 14) label(k === 1 ? 'h' : 'h/' + k, x + rpi + wall + 4, yL - hcur * sc / 2, C.accent);
        });
        snap = false;
        return;
      }

      if (mode === 'tilt') {
        const al = P['cp-a'] * Math.PI / 180, px = w * 0.3;
        const lcm = ph.hc / Math.cos(al);
        const scT = Math.min(sc, (tx1 - px - rp - 20) / Math.max(1e-9, Hview * Math.tan(al)));
        const lcur = ease(0, lcm);
        const lenUp = Hview * scT / Math.cos(al), lenDown = up ? 30 : Math.abs(lcm) * scT + 30;
        ctx.save(); ctx.translate(px, yL); ctx.rotate(al);
        ctx.fillStyle = '#F8F9FC'; ctx.fillRect(-rp, -lenUp, 2 * rp, lenUp + lenDown);
        column(ctx, 0, rp, lenDown, -lcur * scT, ph.c === 0 ? Math.PI / 2 : ph.th);
        glassTube(ctx, 0, -lenUp, lenDown, rp, wall);
        ctx.restore();
        // vertical reference + angle arc
        Sim.line(ctx, [[px, yL], [px, yL - 70]], { color: C.ink2, width: 1, dash: [4, 4] });
        ctx.save(); ctx.strokeStyle = C.accent; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(px, yL, 40, -Math.PI / 2, -Math.PI / 2 + al); ctx.stroke(); ctx.restore();
        if (al > 0.05) Sim.text(ctx, 'α', px + 52 * Math.sin(al / 2), yL - 52 * Math.cos(al / 2), { size: 13, weight: 700, color: C.accent, align: 'center' });
        // same vertical height
        const hv = lcur * Math.cos(al) * scT;
        const ex = px + Math.sin(al) * lcur * scT;
        Sim.line(ctx, [[60, yL - hv], [ex, yL - hv]], { color: C.coral, width: 1.4, dash: [5, 4] });
        if (Math.abs(hv) > 16) label('vertical h = ' + cm(lcur * Math.cos(al)), 64, yL - hv + (up ? -14 : 14), C.coral);
        const mx = px + Math.sin(al) * lcur * scT / 2 + 14 * Math.cos(al), my = yL - Math.cos(al) * lcur * scT / 2 + 14 * Math.sin(al);
        if (Math.abs(lcur * scT) > 30) label('l = ' + cm(lcur), mx + rp, my, C.accent);
        snap = false;
        return;
      }

      // normal / short / fall: single tube
      const x = w * 0.55;
      let topY = up ? yL - Hview * sc - 4 : 30;
      const bot = up ? yL + 34 : h - 28;
      let thDraw = ph.c === 0 ? Math.PI / 2 : ph.th;
      let target = ph.hc;
      if (mode === 'short' && up && ph.hc > 0) {
        const lfrac = P['cp-L'] / 100;
        topY = yL - ph.hc * lfrac * sc;
        target = ph.hc * lfrac;
        thDraw = Math.acos(clamp(ph.c * lfrac, -1, 1));
        Sim.line(ctx, [[x - 40, yL - ph.hc * sc], [x + 60, yL - ph.hc * sc]], { color: C.muted, width: 1.2, dash: [4, 4] });
        label('h if the tube were long enough', x - 40, yL - ph.hc * sc - 14, C.muted);
      } else if (mode === 'fall' && up && ph.hc > 0) {
        target = (yL - topY) / sc;
        label('g_eff = 0 (free fall)', 64, 18, C.coral);
      }
      const hcur = ease(0, target);
      ctx.fillStyle = '#F8F9FC'; ctx.fillRect(x - rp, topY, 2 * rp, bot - topY);
      const yc = Math.max(topY, yL - hcur * sc);
      column(ctx, x, rp, bot, yc, thDraw);
      glassTube(ctx, x, topY, bot, rp, wall);
      if (Math.abs(hcur * sc) > 14) {
        const ax = x + rp + wall + 18;
        Sim.line(ctx, [[x + rp + wall, yc], [ax + 6, yc]], { color: C.ink2, width: 1, dash: [3, 3] });
        dimArrow(ctx, ax, yc, yL, '', C.ink2);
        label((up ? 'h = ' : 'falls ') + cm(Math.abs(hcur)), ax + 8, (yc + yL) / 2, up ? C.green : C.coral);
      }
      if (mode === 'short' && up && ph.hc > 0) label('no overflow · flatter meniscus', x + rp + 8, topY - 12, C.accent);
      snap = false;
    }

    const st = Sim.stage(host, { aspect: 4 / 3, minH: 300, maxH: 480, animate: true, draw });
    stages.push(st);
    const ctrls = [...panel.querySelectorAll('[data-mode]')];
    let lastMode = null;
    Sim.controls(panel, vals => {
      P = Object.assign({}, vals);
      if (P.mode !== lastMode) { snap = P.mode !== 'fall' && P.mode !== 'compare'; if (P.mode === 'fall') cur[0] = phys().hc; if (P.mode === 'compare') cur = [0, 0, 0]; lastMode = P.mode; }
      ctrls.forEach(c => { c.hidden = c.dataset.mode !== P.mode; });
      const ph = phys();
      Sim.out(panel, 'h', ph.c === 0 ? '0 cm' : (ph.hc > 0 ? '+' : '−') + cm(Math.abs(ph.hc)) + (ph.hc < 0 ? ' (falls)' : ''));
      Sim.out(panel, 'R', ph.c === 0 ? '∞ (flat)' : Sim.sci(ph.R * 1000, 2) + ' mm');
      Sim.out(panel, 'W', Sim.sci(Math.abs(ph.W) * 1000, 2) + ' mN');
      const al = P['cp-a'], lfrac = P['cp-L'] / 100;
      const notes = {
        normal: 'h = 2T cos θ / (rρg). Halve r and h doubles; push θ past 90° and the liquid falls instead.',
        compare: 'Tubes of radius r, 2r, 3r: heights h, h/2, h/3, so h × r is constant. The mass lifted (= 2πrT cos θ / g) grows ∝ r.',
        tilt: 'Vertical height stays ' + cm(Math.abs(ph.hc)) + '; liquid length along the tube l = h / cos α = ' + cm(Math.abs(ph.hc / Math.cos(al * Math.PI / 180))) + '.',
        short: ph.hc > 0 ? 'Tube sticks out only ' + cm(ph.hc * lfrac) + ': liquid reaches the top and stops (no overflow). Meniscus radius grows from R to R·h/ℓ = ' + Sim.sci(ph.R * 1000 / lfrac, 2) + ' mm.' : 'This case is for a liquid that rises (θ < 90°).',
        fall: ph.hc > 0 ? 'In free fall g_eff = 0, so nothing stops the rise: the liquid fills the whole tube (but never overflows).' : 'Shown for a wetting liquid (θ < 90°).'
      };
      note.textContent = notes[P.mode];
      st.redraw();
    });
    root.querySelectorAll('[data-preset]').forEach(b => b.addEventListener('click', () => {
      const v = b.dataset.preset === 'mercury' ? { 'cp-th': 140, 'cp-T': 0.47, 'cp-rho': 13600 } : { 'cp-th': 0, 'cp-T': 0.072, 'cp-rho': 1000 };
      Object.keys(v).forEach(id => { root.querySelector('#' + id).value = v[id]; });
      root.querySelector('#cp-th').dispatchEvent(new Event('input'));
    }));
  }



  function boot() {
    [initVisc, initStokes, initReynolds, initMolecules, initFilm, initContact, initBubbles, initConnect, initCapillary].forEach(f => {
      try { f(); } catch (e) { if (window.console) console.error('[fluids2 sim]', e); }
    });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => stages.forEach(s => s.redraw()));
  }
  boot();
})();
