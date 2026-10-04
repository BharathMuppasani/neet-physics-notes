/* =====================================================================
   Simulations — Mechanical Properties of Solids (solids.html)
   Each sim initialises only if its host <figure> exists.
   Colours come from Sim.C; animation respects Sim.reduced.
   ===================================================================== */
(function () {
  'use strict';
  if (typeof Sim === 'undefined') return;

  /* ---------------- shared helpers ---------------- */
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, t) => a + (b - a) * t;
  const ease = (cur, tgt, dt, k = 9) => (Sim.reduced ? tgt : cur + (tgt - cur) * (1 - Math.exp(-k * dt)));
  const hexRGB = (h) => {
    h = String(h).trim().replace('#', '');
    if (h.length === 3) h = h.split('').map(c => c + c).join('');
    const n = parseInt(h, 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  };
  const mix = (a, b, t) => {
    try {
      const A = hexRGB(a), B = hexRGB(b);
      if (A.some(isNaN) || B.some(isNaN)) return t < 0.5 ? a : b;
      return `rgb(${A.map((v, i) => Math.round(lerp(v, B[i], clamp(t, 0, 1)))).join(',')})`;
    } catch (e) { return t < 0.5 ? a : b; }
  };
  const alpha = (h, a) => {
    try { const [r, g, b] = hexRGB(h); if ([r, g, b].some(isNaN)) return h; return `rgba(${r},${g},${b},${a})`; } catch (e) { return h; }
  };
  const fs = (w) => (w < 420 ? 11.5 : 13);
  const sup = (n) => String(n).replace(/-/g, '⁻').replace(/\d/g, d => '⁰¹²³⁴⁵⁶⁷⁸⁹'[d]);
  /* "2.0×10¹¹" style, always scientific */
  const sciF = (x, dp = 1) => {
    if (x === 0) return '0';
    const e = Math.floor(Math.log10(Math.abs(x)));
    let m = x / Math.pow(10, e);
    if (+m.toFixed(dp) >= 10) { m /= 10; return `${m.toFixed(dp)}×10${sup(e + 1)}`; }
    return `${m.toFixed(dp)}×10${sup(e)}`;
  };
  /* readout setter that skips unchanged text */
  const outCache = (root) => {
    const cache = {};
    return (k, t) => { if (cache[k] !== t) { cache[k] = t; Sim.out(root, k, t); } };
  };
  function setup(id, fn) {
    const root = document.getElementById(id);
    if (!root) return;
    const host = root.querySelector('.sim-stage');
    if (!host) return;
    try { fn(root, host); } catch (e) { if (window.console) console.error('[sim]', id, e); }
  }
  function hatch(ctx, x, y, w, h, color, gap = 7) {
    ctx.save();
    ctx.beginPath(); ctx.rect(x, y, w, h); ctx.clip();
    ctx.strokeStyle = color; ctx.lineWidth = 1;
    for (let i = -h; i < w + h; i += gap) { ctx.beginPath(); ctx.moveTo(x + i, y + h); ctx.lineTo(x + i + h, y); ctx.stroke(); }
    ctx.restore();
  }
  function spring(ctx, x1, y1, x2, y2, o = {}) {
    const coils = o.coils || 5, amp = o.amp || 5;
    const len = Math.hypot(x2 - x1, y2 - y1); if (len < 1) return;
    const ux = (x2 - x1) / len, uy = (y2 - y1) / len, nx = -uy, ny = ux;
    const lead = Math.min(4, len * 0.15);
    ctx.save();
    ctx.strokeStyle = o.color || Sim.C.ink2; ctx.lineWidth = o.width || 1.6; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(x1, y1);
    ctx.lineTo(x1 + ux * lead, y1 + uy * lead);
    const n = coils * 2, body = len - 2 * lead;
    for (let i = 1; i < n; i++) {
      const s = lead + body * i / n, side = i % 2 ? 1 : -1;
      ctx.lineTo(x1 + ux * s + nx * amp * side, y1 + uy * s + ny * amp * side);
    }
    ctx.lineTo(x2 - ux * lead, y2 - uy * lead); ctx.lineTo(x2, y2);
    ctx.stroke(); ctx.restore();
  }
  function dot(ctx, x, y, r, fill, stroke) {
    ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = fill; ctx.fill();
    if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = 1.5; ctx.stroke(); }
  }
  /* dimension marker: horizontal (y fixed) */
  function dimH(ctx, x1, x2, y, label, color, size = 12, above = true) {
    if (Math.abs(x2 - x1) < 2) return;
    ctx.save();
    ctx.strokeStyle = color; ctx.lineWidth = 1.3;
    ctx.beginPath(); ctx.moveTo(x1, y); ctx.lineTo(x2, y);
    ctx.moveTo(x1, y - 5); ctx.lineTo(x1, y + 5); ctx.moveTo(x2, y - 5); ctx.lineTo(x2, y + 5); ctx.stroke();
    ctx.restore();
    if (label) Sim.text(ctx, label, (x1 + x2) / 2, y + (above ? -11 : 12), { size, color, align: 'center', weight: 650 });
  }
  function dimV(ctx, x, y1, y2, label, color, size = 12, side = 'right') {
    if (Math.abs(y2 - y1) < 2) return;
    ctx.save();
    ctx.strokeStyle = color; ctx.lineWidth = 1.3;
    ctx.beginPath(); ctx.moveTo(x, y1); ctx.lineTo(x, y2);
    ctx.moveTo(x - 5, y1); ctx.lineTo(x + 5, y1); ctx.moveTo(x - 5, y2); ctx.lineTo(x + 5, y2); ctx.stroke();
    ctx.restore();
    if (label) Sim.text(ctx, label, x + (side === 'right' ? 9 : -9), (y1 + y2) / 2, { size, color, align: side === 'right' ? 'left' : 'right', weight: 650 });
  }
  function roundedRect(ctx, x, y, w, h, r, fill, stroke, lw = 1.5) {
    Sim.rrect(ctx, x, y, w, h, r);
    if (fill) { ctx.fillStyle = fill; ctx.fill(); }
    if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = lw; ctx.stroke(); }
  }

  /* =================================================================
     1. Atoms & springs lattice — elasticity / plasticity
     ================================================================= */
  setup('sim-lattice', (root, host) => {
    const LIMIT = 0.55, BOND = 0.2, PERMK = 1.5;
    const S = { f: 0.4, fmax: 0.4, perm: 0, e: 0.4, v: 0, released: false, mode: 'elastic' };
    const inp = root.querySelector('#lat-F');
    const out = outCache(root);
    let releasing = false;
    const target = () => S.f + S.perm;

    function physics(dt) {
      if (Sim.reduced) { S.e = target(); S.v = 0; return; }
      if (dt <= 0) return;
      const K = S.released ? 150 : 300;
      const c = S.released ? 3.4 : 2 * Math.sqrt(300);
      const n = 6, h = dt / n;
      for (let i = 0; i < n; i++) {
        const a = K * (target() - S.e) - c * S.v;
        S.v += a * h; S.e += S.v * h;
      }
      if (Math.abs(S.v) < 0.002 && Math.abs(target() - S.e) < 0.002) { S.e = target(); S.v = 0; }
    }

    function draw(ctx, w, h, t, dt) {
      physics(dt);
      const c = Sim.C, f = fs(w);
      const N = w < 460 ? 5 : 7, R = 4;
      const tmax = S.mode === 'plastic' ? 1 + PERMK * (1 - LIMIT) : 1;
      const left = 34, right = w < 460 ? 96 : 130;
      const a = Math.min(52, (w - left - right) / ((N - 1) * (1 + BOND * tmax) + 0.6));
      const gy0 = Math.max(44, h / 2 - 1.5 * a - 10);
      const x0 = left + 0.45 * a;
      const elastic = S.e - S.perm;
      const stretch = BOND * S.e;
      const X = i => x0 + i * a * (1 + stretch);
      const Yr = j => gy0 + j * a;
      const r = Math.max(5, a * 0.19);

      // wall
      const wallTop = gy0 - a * 0.6, wallH = 3 * a + a * 1.2;
      ctx.fillStyle = c.surface2; ctx.fillRect(left - 22, wallTop, 22, wallH);
      hatch(ctx, left - 22, wallTop, 22, wallH, c.line2);
      Sim.line(ctx, [[left, wallTop], [left, wallTop + wallH]], { color: c.ink2, width: 2 });

      // original outline (unstretched lattice)
      Sim.line(ctx, [[x0 - a * 0.4, gy0 - a * 0.4], [x0 + (N - 1) * a + a * 0.4, gy0 - a * 0.4], [x0 + (N - 1) * a + a * 0.4, Yr(R - 1) + a * 0.4], [x0 - a * 0.4, Yr(R - 1) + a * 0.4]], { color: c.muted, width: 1.2, dash: [5, 5], close: true });

      // bonds from wall to first column
      for (let j = 0; j < R; j++) Sim.line(ctx, [[left, Yr(j)], [X(0), Yr(j)]], { color: c.ink2, width: 2 });
      // vertical bonds
      for (let i = 0; i < N; i++) for (let j = 0; j < R - 1; j++) Sim.line(ctx, [[X(i), Yr(j) + r], [X(i), Yr(j + 1) - r]], { color: c.line2, width: 1.6 });
      // horizontal springs
      const sCol = elastic >= 0 ? mix(c.ink2, c.coral, elastic / 1.0) : mix(c.ink2, c.water, -elastic / 0.6);
      const yielded = S.perm > 0.001;
      for (let j = 0; j < R; j++) for (let i = 0; i < N - 1; i++) {
        spring(ctx, X(i) + r, Yr(j), X(i + 1) - r, Yr(j), { coils: 4, amp: Math.max(3, a * 0.11), color: sCol, width: 1.7 });
      }
      // atoms
      for (let i = 0; i < N; i++) for (let j = 0; j < R; j++) {
        dot(ctx, X(i), Yr(j), r, yielded && i > 0 && (i + j) % 3 === 0 ? c.amber : c.accent);
        dot(ctx, X(i) - r * 0.3, Yr(j) - r * 0.3, r * 0.28, 'rgba(255,255,255,0.55)');
      }
      // grip bar
      const gx = X(N - 1) + a * 0.45;
      Sim.line(ctx, [[X(N - 1) + r, Yr(0)], [gx, Yr(0)]], { color: c.ink2, width: 1.5 });
      for (let j = 1; j < R; j++) Sim.line(ctx, [[X(N - 1) + r, Yr(j)], [gx, Yr(j)]], { color: c.ink2, width: 1.5 });
      roundedRect(ctx, gx, Yr(0) - a * 0.35, 7, 3 * a + a * 0.7, 3, c.ink2);

      // deforming force
      const midY = Yr(1.5);
      if (S.f > 0.01) {
        const L = 18 + S.f * (right - 40);
        Sim.arrow(ctx, gx + 9, midY, gx + 9 + L, midY, { color: c.coral, width: 3 });
        Sim.text(ctx, 'F (deforming)', Math.min(w - 6, gx + 9 + L), midY - 16, { size: f, color: c.coral, weight: 650, align: 'right' });
      }
      // restoring forces on the right-most atoms
      if (Math.abs(elastic) > 0.02) {
        const L = clamp(elastic, -1.2, 1.4) * a * 0.75;
        for (let j = 0; j < R; j++) {
          const ax = X(N - 1);
          Sim.arrow(ctx, ax - r - 2, Yr(j) - r - 4, ax - r - 2 - L, Yr(j) - r - 4, { color: c.green, width: 2, head: 7 });
        }
        Sim.text(ctx, elastic > 0 ? 'restoring force' : 'restoring force (now pushes out)', X(N - 1) - r, gy0 - a * 0.4 - 12, { size: f - 0.5, color: c.green, weight: 650, align: 'right' });
      }
      // permanent set bracket
      if (yielded) {
        const xOrig = x0 + (N - 1) * a, xPerm = x0 + (N - 1) * a * (1 + BOND * S.perm);
        dimH(ctx, xOrig, xPerm, Yr(R - 1) + a * 0.4 + 16, 'permanent set', c.amber, f - 0.5, false);
      }

      // force gauge with elastic limit
      const by = h - 18, bx = left, bw = w - left - 20;
      roundedRect(ctx, bx, by - 4, bw, 8, 4, c.surface2);
      roundedRect(ctx, bx, by - 4, Math.max(8, bw * S.f), 8, 4, S.mode === 'plastic' && S.f > LIMIT ? c.amber : c.coral);
      Sim.text(ctx, 'applied force', bx, by - 15, { size: 11, color: c.muted, weight: 600 });
      if (S.mode === 'plastic') {
        const lx = bx + bw * LIMIT;
        Sim.line(ctx, [[lx, by - 10], [lx, by + 10]], { color: c.ink, width: 2 });
        Sim.text(ctx, 'elastic limit', lx, by - 18, { size: 11, color: c.ink, weight: 650, align: 'center' });
      }

      // status
      let msg;
      if (S.released && Math.abs(S.v) > 0.01) msg = 'Released: stretched bonds pull the atoms back';
      else if (S.released && yielded) msg = 'Back at rest, but not at the original length';
      else if (S.released) msg = 'Back to the original shape: elastic';
      else if (S.f < 0.01 && !yielded) msg = 'No force: atoms at equilibrium spacing';
      else if (S.mode === 'plastic' && S.f > LIMIT) msg = 'Past the elastic limit: atoms slip to new positions';
      else msg = 'Bonds stretched: restoring force = applied force';
      Sim.text(ctx, msg, 10, 16, { size: f, color: c.ink, weight: 650 });

      out('strain', (BOND * S.e * 100).toFixed(1) + ' %');
      out('perm', (BOND * S.perm * 100).toFixed(1) + ' %');
      out('force', Math.round(S.f * 100) + ' units');
    }

    const st = Sim.stage(host, { aspect: 16 / 8.2, minH: 250, maxH: 360, animate: true, draw });
    Sim.controls(root, (v) => {
      if (v.mode !== S.mode) {
        S.mode = v.mode; S.perm = 0; S.fmax = 0; S.released = false;
      }
      S.f = (v['lat-F'] || 0) / 100;
      if (!releasing) S.released = false;
      S.fmax = Math.max(S.fmax, S.f);
      if (S.mode === 'plastic') S.perm = PERMK * Math.max(0, S.fmax - LIMIT);
      st.redraw();
    });
    const rel = root.querySelector('#lat-release');
    const reset = root.querySelector('#lat-reset');
    if (rel) rel.addEventListener('click', () => {
      releasing = true; S.released = true;
      inp.value = 0; inp.dispatchEvent(new Event('input'));
      releasing = false; st.redraw();
    });
    if (reset) reset.addEventListener('click', () => {
      S.perm = 0; S.fmax = 0; S.released = false; S.v = 0;
      inp.value = 40; inp.dispatchEvent(new Event('input'));
      S.e = target(); st.redraw();
    });
    S.e = target();
  });

  /* =================================================================
     2. Types of stress — tensile / compressive / shear / hydraulic
     ================================================================= */
  setup('sim-stress', (root, host) => {
    const S = { type: 'tensile', mag: 0.6, m: 0.6 };
    const INFO = {
      tensile: { strain: 'Longitudinal strain = ΔL / L', changes: 'Length increases', stress: 'Tensile (pull, normal to face)', note: 'Equal and opposite pulls normal to the end faces. The length grows (and the bar gets a little thinner).' },
      compressive: { strain: 'Longitudinal strain = ΔL / L', changes: 'Length decreases', stress: 'Compressive (push, normal to face)', note: 'Equal and opposite pushes normal to the end faces. The length shrinks. Tensile + compressive = longitudinal stress.' },
      shear: { strain: 'Shear strain = Δx / L = tan θ ≈ θ', changes: 'Shape only (volume same)', stress: 'Shearing (force along face)', note: 'The force acts along (tangential to) the top face while the bottom is held. Layers slide; the face turns through θ.' },
      hydraulic: { strain: 'Volume strain = ΔV / V', changes: 'Volume only (shape same)', stress: 'Hydraulic (= pressure p)', note: 'Equal normal push from every side, as for a body inside a fluid. Size shrinks, shape stays the same.' },
    };
    const out = outCache(root);

    function draw(ctx, w, h, t, dt) {
      S.m = ease(S.m, S.mag, dt, 7);
      const c = Sim.C, f = fs(w), m = S.m;
      const s = Math.min(w * 0.3, h * 0.42);
      const cx = w / 2, cy = h * 0.47;
      const ox = cx - s / 2, oy = cy - s / 2;
      const fill = alpha(c.accent, 0.14);
      let pts, arrows = [];

      if (S.type === 'shear') {
        const yb = oy + s;
        ctx.fillStyle = c.surface2; ctx.fillRect(ox - 40, yb, s + 80 + s * 0.4, 16);
        hatch(ctx, ox - 40, yb, s + 80 + s * 0.4, 16, c.line2);
        Sim.line(ctx, [[ox - 40, yb], [ox + s + 40 + s * 0.4, yb]], { color: c.ink2, width: 2 });
      }
      // original outline
      Sim.line(ctx, [[ox, oy], [ox + s, oy], [ox + s, oy + s], [ox, oy + s]], { color: c.muted, width: 1.3, dash: [6, 5], close: true });

      if (S.type === 'tensile' || S.type === 'compressive') {
        const sign = S.type === 'tensile' ? 1 : -1;
        const W = s * (1 + sign * 0.36 * m), H = s * (1 - sign * 0.08 * m);
        const x1 = cx - W / 2, y1 = cy - H / 2;
        pts = [[x1, y1], [x1 + W, y1], [x1 + W, y1 + H], [x1, y1 + H]];
        Sim.line(ctx, pts, { color: c.accent, width: 2.2, fill, close: true });
        const L = 18 + 34 * m;
        for (const k of [-0.25, 0.25]) {
          const yy = cy + k * H;
          if (sign > 0) {
            Sim.arrow(ctx, x1 + W + 4, yy, x1 + W + 4 + L, yy, { color: c.coral, width: 2.5 });
            Sim.arrow(ctx, x1 - 4, yy, x1 - 4 - L, yy, { color: c.coral, width: 2.5 });
          } else {
            Sim.arrow(ctx, x1 + W + 4 + L, yy, x1 + W + 4, yy, { color: c.coral, width: 2.5 });
            Sim.arrow(ctx, x1 - 4 - L, yy, x1 - 4, yy, { color: c.coral, width: 2.5 });
          }
        }
        Sim.text(ctx, 'F', x1 + W + 10 + L, cy, { size: f + 1, color: c.coral, weight: 700, align: 'left' });
        Sim.text(ctx, 'F', x1 - 10 - L, cy, { size: f + 1, color: c.coral, weight: 700, align: 'right' });
        dimH(ctx, ox, ox + s, oy + s + 18, 'L', c.muted, f, false);
        if (m > 0.04) {
          const yB = oy - 14;
          if (sign > 0) dimH(ctx, ox + s, x1 + W, yB, 'ΔL', c.coral, f);
          else dimH(ctx, x1 + W, ox + s, yB, 'ΔL', c.coral, f);
        }
      } else if (S.type === 'shear') {
        const dx = s * 0.42 * m;
        const yb = oy + s;
        pts = [[ox, yb], [ox + s, yb], [ox + s + dx, oy], [ox + dx, oy]];
        Sim.line(ctx, pts, { color: c.accent, width: 2.2, fill, close: true });
        for (let k = 1; k < 6; k++) {
          const yy = yb - s * k / 6, off = dx * k / 6;
          Sim.line(ctx, [[ox + off + 3, yy], [ox + s + off - 3, yy]], { color: alpha(c.accent, 0.35), width: 1 });
        }
        const L = 22 + 40 * m;
        Sim.arrow(ctx, ox + dx + s * 0.25, oy - 10, ox + dx + s * 0.25 + L, oy - 10, { color: c.coral, width: 2.8 });
        Sim.text(ctx, 'F', ox + dx + s * 0.25 + L + 8, oy - 10, { size: f + 1, color: c.coral, weight: 700 });
        Sim.text(ctx, 'bottom held fixed', ox + s / 2, yb + 30, { size: 11, color: c.muted, align: 'center', weight: 600 });
        if (m > 0.04) {
          dimH(ctx, ox, ox + dx, oy - 30, 'Δx', c.coral, f);
          const th = Math.atan2(dx, s), R = Math.min(34, s * 0.35);
          ctx.save(); ctx.strokeStyle = c.amber; ctx.lineWidth = 2;
          ctx.beginPath(); ctx.arc(ox, yb, R, -Math.PI / 2, -Math.PI / 2 + th); ctx.stroke(); ctx.restore();
          Sim.text(ctx, 'θ', ox + R * Math.tan(th) + 9, yb - R + 6, { size: f + 1, color: c.amber, weight: 700 });
        }
        dimV(ctx, ox - 16, oy, yb, 'L', c.muted, f, 'left');
      } else {
        const k = 1 - 0.22 * m, W = s * k;
        const x1 = cx - W / 2, y1 = cy - W / 2;
        ctx.fillStyle = alpha(c.water, 0.10);
        Sim.rrect(ctx, cx - s / 2 - 46, cy - s / 2 - 46, s + 92, s + 92, 14); ctx.fill();
        pts = [[x1, y1], [x1 + W, y1], [x1 + W, y1 + W], [x1, y1 + W]];
        Sim.line(ctx, pts, { color: c.accent, width: 2.2, fill, close: true });
        const L = 14 + 18 * m;
        for (const q of [-0.3, 0, 0.3]) {
          const px = cx + q * W, py = cy + q * W;
          Sim.arrow(ctx, px, y1 - 6 - L, px, y1 - 4, { color: c.water, width: 2.2, head: 8 });
          Sim.arrow(ctx, px, y1 + W + 6 + L, px, y1 + W + 4, { color: c.water, width: 2.2, head: 8 });
          Sim.arrow(ctx, x1 - 6 - L, py, x1 - 4, py, { color: c.water, width: 2.2, head: 8 });
          Sim.arrow(ctx, x1 + W + 6 + L, py, x1 + W + 4, py, { color: c.water, width: 2.2, head: 8 });
        }
        Sim.text(ctx, 'p on every face', cx, cy + s / 2 + 36, { size: f, color: c.water, weight: 650, align: 'center' });
      }

      // live formula strip
      const I = INFO[S.type];
      Sim.text(ctx, I.strain, w / 2, h - 16, { size: f + 0.5, color: c.ink, weight: 650, align: 'center', bg: c.surface2 });
      out('stype', I.stress); out('changes', I.changes); out('note', I.note);
    }

    const st = Sim.stage(host, { aspect: 16 / 9, minH: 270, maxH: 380, animate: true, draw });
    Sim.controls(root, (v) => {
      if (v.type !== S.type) { S.type = v.type; S.m = 0; }
      S.mag = (v['st-mag'] || 0) / 100;
      st.redraw();
    });
  });

  /* =================================================================
     3. Stress–strain curve explorer (drag, unload, material types)
     ================================================================= */
  setup('sim-curve', (root, host) => {
    const hermite = (keys) => (x) => {
      if (x <= keys[0][0]) return keys[0][1];
      for (let i = 0; i < keys.length - 1; i++) {
        const [x0, y0, m0] = keys[i], [x1, y1, m1] = keys[i + 1];
        if (x <= x1) {
          const hh = x1 - x0, t = (x - x0) / hh, t2 = t * t, t3 = t2 * t;
          return (2 * t3 - 3 * t2 + 1) * y0 + (t3 - 2 * t2 + t) * hh * m0 + (-2 * t3 + 3 * t2) * y1 + (t3 - t2) * hh * m1;
        }
      }
      return keys[keys.length - 1][1];
    };
    const MATS = {
      ductile: { keys: [[0, 0, 5], [0.10, 0.50, 5], [0.16, 0.62, 0.6], [0.38, 0.86, 0.9], [0.60, 0.95, 0], [0.76, 0.80, -1.6]],
        xmax: 0.86, ymax: 1.12, Y: 5, xB: 0.16, labels: { A: 1, B: 2, D: 4, E: 5 } },
      brittle: { keys: [[0, 0, 7], [0.10, 0.70, 7], [0.13, 0.80, 0], [0.142, 0.775, -3]],
        xmax: 0.86, ymax: 1.12, Y: 7, xB: 0.115, labels: { A: 1, D: 2, E: 3 } },
      elastomer: { keys: [[0, 0, 0.32], [1.5, 0.32, 0.08], [4.5, 0.48, 0.1], [6.5, 0.95, 0.45]],
        xmax: 7.2, ymax: 1.12, elast: true, labels: { E: 3 } },
    };
    Object.values(MATS).forEach(M => { M.f = hermite(M.keys); M.xE = M.keys[M.keys.length - 1][0]; });

    const inp = root.querySelector('#cv-x');
    const out = outCache(root);
    const S = { mat: 'ductile', x: 0.3 * MATS.ductile.xE, xs: 0.3 * MATS.ductile.xE, un: null, box: null };

    function regionOf(M, x) {
      const L = M.labels, K = M.keys;
      if (x >= M.xE - 1e-6) return ['Fractured (E)', M.elast ? 'The rubber finally snaps. Up to here every stretch was recoverable: a huge elastic range with no plastic region.' : 'The wire breaks at E. Breaking stress is a property of the material.'];
      if (M.elast) return ['Elastic, non-linear', 'Rubber-like elastomer: strain can be several hundred %, yet it returns. Stress is NOT proportional to strain (no Hooke region), and there is no plastic region.'];
      if (x <= K[L.A][0]) return ['Hooke region (O–A)', 'Stress ∝ strain. The slope of this straight line is Young\'s modulus Y. Unloading retraces the line back to O.'];
      if (L.B && x <= K[L.B][0]) return ['Elastic, non-linear (A–B)', 'Past the proportional limit A, but still elastic up to the yield point B: removing the load returns the wire to O.'];
      if (x <= M.xB) return ['Near elastic limit', 'Brittle material: almost no plastic region beyond this.'];
      if (x <= K[L.D][0]) return ['Plastic (B–D)', 'Beyond the yield point B. Unloading now follows a line parallel to OA and leaves a permanent set.'];
      return ['Necking (D–E)', 'Past the ultimate tensile strength D: a neck forms and the wire breaks soon after, even under smaller load.'];
    }

    function draw(ctx, w, h, t, dt) {
      const c = Sim.C, f = fs(w), M = MATS[S.mat];
      S.xs = ease(S.xs, S.x, dt, 12);
      const box = { x: 46, y: 34, w: w - 46 - 18, h: h - 34 - 46 };
      S.box = box;
      const xticks = M.elast ? [1, 2, 3, 4, 5, 6, 7] : [];
      const ax = Sim.axes(ctx, box, { xmin: 0, xmax: M.xmax, ymin: 0, ymax: M.ymax, xticks, yticks: [], grid: M.elast,
        xfmt: v => v * 100 + '%', xlabel: M.elast ? 'Strain' : 'Strain →', ylabel: 'Stress' });
      const { X, Y } = ax;
      const yB = M.labels.B !== undefined ? M.keys[M.labels.B] : null;

      // ghost of the other metal curve for comparison
      if (!M.elast) {
        const G = MATS[S.mat === 'ductile' ? 'brittle' : 'ductile'];
        const gp = [];
        for (let i = 0; i <= 120; i++) { const xx = G.xE * i / 120; gp.push([X(xx), Y(G.f(xx))]); }
        Sim.line(ctx, gp, { color: c.line2, width: 1.5, dash: [4, 4] });
        const ex = G.keys[G.keys.length - 1];
        Sim.text(ctx, S.mat === 'ductile' ? 'brittle' : 'ductile', X(ex[0]) + 6, Y(ex[1]) - 10, { size: 11, color: c.muted, weight: 600 });
      }

      // region shading under the full curve
      const shade = (xa, xb, col) => {
        const p = [[X(xa), Y(0)]];
        for (let i = 0; i <= 80; i++) { const xx = lerp(xa, xb, i / 80); p.push([X(xx), Y(M.f(xx))]); }
        p.push([X(xb), Y(0)]);
        Sim.line(ctx, p, { color: 'none', fill: col, close: true });
      };
      const xEl = M.elast ? M.xE : M.xB;
      shade(0, xEl, alpha(c.green, 0.13));
      if (!M.elast) shade(M.xB, M.xE, alpha(c.amber, 0.14));

      // full curve (light) and traced part (bold)
      const full = [], traced = [];
      for (let i = 0; i <= 240; i++) {
        const xx = M.xE * i / 240;
        full.push([X(xx), Y(M.f(xx))]);
        if (xx <= S.xs) traced.push([X(xx), Y(M.f(xx))]);
      }
      traced.push([X(S.xs), Y(M.f(S.xs))]);
      Sim.line(ctx, full, { color: c.line2, width: 2 });
      Sim.line(ctx, traced, { color: c.accent, width: 3 });

      // sigma_y / sigma_u guide lines
      if (!M.elast) {
        const D = M.keys[M.labels.D];
        Sim.line(ctx, [[X(0), Y(D[1])], [X(D[0]), Y(D[1])]], { color: c.muted, width: 1, dash: [3, 4] });
        Sim.text(ctx, 'σu', X(0) - 6, Y(D[1]), { size: 12, color: c.ink2, align: 'right', weight: 650 });
        if (yB) {
          Sim.line(ctx, [[X(0), Y(yB[1])], [X(yB[0]), Y(yB[1])]], { color: c.muted, width: 1, dash: [3, 4] });
          Sim.text(ctx, 'σy', X(0) - 6, Y(yB[1]), { size: 12, color: c.ink2, align: 'right', weight: 650 });
        }
      }
      // key points
      const place = { A: [-12, -2, 'right'], B: [-4, -14, 'right'], D: [0, -14, 'center'], E: [8, -10, 'left'] };
      Object.entries(M.labels).forEach(([k, idx]) => {
        const p = M.keys[idx];
        dot(ctx, X(p[0]), Y(p[1]), 4, c.surface, c.ink);
        const [dx, dy, al] = place[k];
        Sim.text(ctx, k, X(p[0]) + dx, Y(p[1]) + dy, { size: 12.5, color: c.ink, weight: 750, align: al });
      });
      Sim.text(ctx, 'O', X(0) - 6, Y(0) + 10, { size: 12, color: c.ink, weight: 700, align: 'right' });

      // legend
      const lgx = w - 18, lgy = 14;
      if (M.elast) {
        Sim.text(ctx, 'elastic (whole curve)', lgx, lgy, { size: 11, color: c.muted, weight: 600, align: 'right' });
      } else {
        ctx.font = `600 11px ${c.font}`;
        const wp = ctx.measureText('plastic').width, we = ctx.measureText('elastic').width;
        Sim.text(ctx, 'plastic', lgx, lgy, { size: 11, color: c.muted, weight: 600, align: 'right' });
        roundedRect(ctx, lgx - wp - 13, lgy - 4, 8, 8, 2, alpha(c.amber, 0.55));
        const ex2 = lgx - wp - 22;
        Sim.text(ctx, 'elastic', ex2, lgy, { size: 11, color: c.muted, weight: 600, align: 'right' });
        roundedRect(ctx, ex2 - we - 13, lgy - 4, 8, 8, 2, alpha(c.green, 0.55));
      }

      // unloading animation
      let px = S.xs, py = M.f(S.xs), perm = 0;
      if (S.un) {
        const U = S.un;
        U.t = Sim.reduced ? 1 : Math.min(1, U.t + dt * 0.7);
        const path = [];
        for (let i = 0; i <= 40; i++) path.push(U.at(U.t * i / 40));
        Sim.line(ctx, path.map(p => [X(p[0]), Y(p[1])]), { color: c.coral, width: 2.5, dash: [6, 4] });
        [px, py] = U.at(U.t);
        if (U.t >= 1 && U.xp > 0.002) {
          perm = U.xp;
          dimH(ctx, X(0), X(U.xp), Y(0) - 12, 'permanent set', c.coral, 11.5);
        }
      }
      // current point and drop lines
      const broken = !S.un && S.xs >= M.xE - 1e-4;
      Sim.line(ctx, [[X(px), Y(py)], [X(px), Y(0)]], { color: c.muted, width: 1, dash: [2, 4] });
      Sim.line(ctx, [[X(px), Y(py)], [X(0), Y(py)]], { color: c.muted, width: 1, dash: [2, 4] });
      if (broken) {
        Sim.text(ctx, '✕', X(px), Y(py), { size: 18, color: c.coral, weight: 800, align: 'center' });
        Sim.text(ctx, 'fracture', X(px) - 10, Y(py) + 18, { size: 12, color: c.coral, weight: 700, align: 'right' });
      } else {
        dot(ctx, X(px), Y(py), 7, c.coral, c.surface);
      }
      if (!S.un) Sim.text(ctx, 'drag along the curve ↔', box.x + box.w, box.y + box.h - 12, { size: 11, color: c.muted, align: 'right', weight: 600 });

      const [rg, ex] = S.un ? (S.un.t >= 1 ? [perm > 0.002 ? 'Unloaded: permanent set' : 'Unloaded: back to O',
        perm > 0.002 ? 'The unloading line is parallel to OA (same slope Y). It meets the strain axis at a non-zero strain: the wire stays longer. This leftover strain is the permanent set.'
          : (M.elast ? 'The rubber returns to zero strain, but along a lower path. The loop area is energy lost as heat (elastic hysteresis).' : 'Unloaded from inside the elastic range, so the wire retraces its path and returns to O. No permanent set.')]
        : ['Unloading…', 'Watch the path the point takes back to zero stress.']) : regionOf(M, S.xs);
      out('region', rg); out('explain', ex);
      out('stress', (py / M.ymax * 100).toFixed(0) + ' % of max');
      out('perm', perm > 0.002 ? (M.elast ? '—' : (perm / M.xE * 100).toFixed(0) + ' % of fracture strain') : 'none');
    }

    const st = Sim.stage(host, { aspect: 16 / 10, minH: 270, maxH: 420, animate: true, draw });
    Sim.controls(root, (v) => {
      const M = MATS[v.mat];
      if (v.mat !== S.mat) { S.mat = v.mat; S.xs = 0; }
      S.x = (v['cv-x'] || 0) / 100 * M.xE;
      S.un = null;
      st.redraw();
    });
    const unload = root.querySelector('#cv-unload');
    if (unload) unload.addEventListener('click', () => {
      const M = MATS[S.mat];
      const x0 = S.x, y0 = M.f(x0);
      S.xs = x0;
      if (x0 >= M.xE - 1e-4 || x0 < 1e-4) return;
      let at, xp = 0;
      if (M.elast) at = (u) => { const x = x0 * (1 - u); return [x, M.f(x) * Math.pow(x / x0, 2.5)]; };
      else if (x0 <= M.xB) at = (u) => { const x = x0 * (1 - u); return [x, M.f(x)]; };
      else { xp = x0 - y0 / M.Y; at = (u) => [lerp(x0, xp, u), lerp(y0, 0, u)]; }
      S.un = { t: 0, at, xp };
      st.redraw();
    });
    const reset = root.querySelector('#cv-reset');
    if (reset) reset.addEventListener('click', () => { inp.value = 0; inp.dispatchEvent(new Event('input')); });

    // drag on canvas
    let drag = false;
    const setFromEvt = (e) => {
      if (!S.box) return;
      const M = MATS[S.mat];
      const p = st.toLocal(e);
      const x = clamp((p.x - S.box.x) / S.box.w * M.xmax, 0, M.xE);
      inp.value = (x / M.xE * 100).toFixed(1);
      inp.dispatchEvent(new Event('input'));
    };
    st.canvas.addEventListener('pointerdown', (e) => { drag = true; try { st.canvas.setPointerCapture(e.pointerId); } catch (_) {} setFromEvt(e); });
    st.canvas.addEventListener('pointermove', (e) => { if (drag) setFromEvt(e); });
    ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(n => st.canvas.addEventListener(n, () => { drag = false; }));
  });

  /* =================================================================
     4. Wire lab — Young's modulus, real numbers
     ================================================================= */
  setup('sim-wire', (root, host) => {
    const MAT = {
      steel: { name: 'Steel', Y: 2.0e11, sy: 2.5e8, col: 'ink2' },
      copper: { name: 'Copper', Y: 1.1e11, sy: 2.0e8, col: 'coral' },
      aluminium: { name: 'Aluminium', Y: 7.0e10, sy: 0.95e8, col: 'muted' },
      brass: { name: 'Brass', Y: 9.1e10, sy: 2.0e8, col: 'amber' },
    };
    const g = 9.8;
    const S = { mat: 'steel', L: 2, d: 0.5, M: 4, dlPx: 0 };
    const out = outCache(root);

    function calc() {
      const m = MAT[S.mat];
      const r = S.d / 2 * 1e-3, A = Math.PI * r * r, F = S.M * g;
      const stress = F / A, strain = stress / m.Y, dL = strain * S.L;
      return { m, r, A, F, stress, strain, dL };
    }

    function draw(ctx, w, h, t, dt) {
      const c = Sim.C, f = fs(w), R = calc();
      const top = 26, wx = Math.round(w * 0.36);
      const maxWire = Math.max(80, h - top - 16 - 60 - 92);
      const pxPerM = maxWire / 3;
      const Lpx = S.L * pxPerM;
      const PXMM = 15;
      const dlMm = R.dL * 1000;
      const over = dlMm * PXMM > 90;
      const dlTarget = Math.min(90, dlMm * PXMM);
      S.dlPx = ease(S.dlPx, dlTarget, dt, 8);
      const endY = top + Lpx + S.dlPx;

      // ceiling
      ctx.fillStyle = c.surface2; ctx.fillRect(wx - 70, 6, 140, top - 6);
      hatch(ctx, wx - 70, 6, 140, top - 6, c.line2);
      Sim.line(ctx, [[wx - 70, top], [wx + 70, top]], { color: c.ink2, width: 2 });

      // wire (uniformly stretched: marks spread evenly)
      const yielded = R.stress > R.m.sy;
      const wcol = yielded ? c.coral : c[R.m.col];
      const thick = 1.4 + S.d * 3.2;
      Sim.line(ctx, [[wx, top], [wx, endY]], { color: wcol, width: thick });
      for (let i = 1; i < 10; i++) {
        const yy = top + (endY - top) * i / 10;
        Sim.line(ctx, [[wx - thick / 2 - 3, yy], [wx + thick / 2 + 3, yy]], { color: alpha(c.ink, 0.35), width: 1 });
      }
      // original end marker
      const origY = top + Lpx;
      Sim.line(ctx, [[wx - 30, origY], [wx + 30, origY]], { color: c.muted, width: 1.2, dash: [4, 4] });
      Sim.text(ctx, 'original end', wx - 34, origY, { size: 11, color: c.muted, align: 'right', weight: 600 });

      // mass
      const mw = 26 + 34 * Math.sqrt(S.M / 20), mh = 16 + 24 * Math.sqrt(S.M / 20);
      Sim.line(ctx, [[wx, endY], [wx, endY + 8]], { color: c.ink2, width: 2 });
      if (S.M > 0) {
        roundedRect(ctx, wx - mw / 2, endY + 8, mw, mh, 5, c.ink2);
        Sim.text(ctx, S.M.toFixed(1) + ' kg', wx, endY + 8 + mh / 2, { size: 11.5, color: '#fff', weight: 700, align: 'center' });
        Sim.arrow(ctx, wx + mw / 2 + 10, endY + 8 + mh / 2 - 12, wx + mw / 2 + 10, endY + 8 + mh / 2 + 18, { color: c.coral, width: 2.2, head: 8 });
        Sim.text(ctx, 'Mg', wx + mw / 2 + 16, endY + 8 + mh / 2 + 8, { size: 12, color: c.coral, weight: 700 });
      }

      // dimensions
      const dx = wx + 46;
      dimV(ctx, dx, top, origY, `L = ${S.L.toFixed(1)} m`, c.ink2, f);
      if (S.dlPx > 2) dimV(ctx, dx + 2, origY, endY, `ΔL = ${dlMm < 10 ? dlMm.toFixed(2) : dlMm.toFixed(0)} mm${over ? ' (off scale)' : ''}`, c.coral, f);
      const exag = PXMM / (pxPerM / 1000);
      Sim.text(ctx, `elongation drawn ≈ ×${Math.round(exag / 10) * 10}`, w - 10, h - 12, { size: 11, color: c.muted, align: 'right', weight: 600 });
      Sim.text(ctx, `d = ${S.d.toFixed(2)} mm`, wx - 12, top + Math.min(Lpx, 60) / 2 + 6, { size: 11.5, color: c.ink2, align: 'right', weight: 600 });
      if (yielded) Sim.text(ctx, 'Stress > yield strength: permanent stretch', w / 2, h - 30, { size: f, color: c.coral, weight: 700, align: 'center', bg: c.coralSoft });

      out('stress', sciF(R.stress, 2) + ' Pa');
      out('strain', sciF(R.strain, 2));
      out('dL', (dlMm < 0.01 ? dlMm.toFixed(4) : dlMm < 10 ? dlMm.toFixed(3) : dlMm.toFixed(1)) + ' mm');
      out('formula', `ΔL = MgL/(πr²Y) = (${S.M.toFixed(1)}×9.8×${S.L.toFixed(1)}) / (π×(${(S.d / 2).toFixed(3)}×10⁻³)²×${sciF(R.m.Y, 1)}) = ${dlMm.toFixed(3)} mm`);
    }
    const st = Sim.stage(host, { aspect: 1.25, minH: 320, maxH: 460, animate: true, draw });
    Sim.controls(root, (v) => {
      S.mat = v.mat; S.L = v['wl-L']; S.d = v['wl-d']; S.M = v['wl-M'];
      st.redraw();
    });
  });

  /* =================================================================
     5. Shear — block with fixed base
     ================================================================= */
  setup('sim-shear', (root, host) => {
    const MAT = {
      rubber: { G: 6e5, ex: 1, label: 'drawn to true scale' },
      lead: { G: 5.6e9, ex: 1e4, label: 'angle drawn ×10 000' },
      aluminium: { G: 2.5e10, ex: 1e4, label: 'angle drawn ×10 000' },
      steel: { G: 8.4e10, ex: 1e4, label: 'angle drawn ×10 000' },
    };
    const S = { mat: 'rubber', F: 800, th: 0 };
    const side = 0.1, A = side * side;
    const out = outCache(root);

    function draw(ctx, w, h, t, dt) {
      const c = Sim.C, f = fs(w), M = MAT[S.mat];
      const theta = S.F / (A * M.G);
      const tv = Math.min(0.5, theta * M.ex);
      S.th = ease(S.th, tv, dt, 8);
      const s = Math.min(w * 0.36, h * 0.52);
      const ox = w / 2 - s / 2 - s * 0.12, yb = h * 0.5 + s / 2;
      const dx = s * Math.tan(S.th);

      ctx.fillStyle = c.surface2; ctx.fillRect(ox - 50, yb, s + 140, 18);
      hatch(ctx, ox - 50, yb, s + 140, 18, c.line2);
      Sim.line(ctx, [[ox - 50, yb], [ox + s + 90, yb]], { color: c.ink2, width: 2 });
      Sim.line(ctx, [[ox, yb - s], [ox + s, yb - s], [ox + s, yb], [ox, yb]], { color: c.muted, width: 1.3, dash: [6, 5] });
      const pts = [[ox, yb], [ox + s, yb], [ox + s + dx, yb - s], [ox + dx, yb - s]];
      Sim.line(ctx, pts, { color: c.accent, width: 2.2, fill: alpha(c.accent, 0.14), close: true });
      for (let k = 1; k < 7; k++) {
        const yy = yb - s * k / 7, off = dx * k / 7;
        Sim.line(ctx, [[ox + off + 3, yy], [ox + s + off - 3, yy]], { color: alpha(c.accent, 0.35), width: 1 });
      }
      const L = 18 + 50 * (S.F / 2000);
      if (S.F > 0) {
        Sim.arrow(ctx, ox + dx + s * 0.2, yb - s - 12, ox + dx + s * 0.2 + L, yb - s - 12, { color: c.coral, width: 2.8 });
        Sim.text(ctx, 'F', ox + dx + s * 0.2 + L + 8, yb - s - 12, { size: f + 1, color: c.coral, weight: 700 });
        Sim.arrow(ctx, ox + s * 0.7, yb + 30, ox + s * 0.7 - L * 0.8, yb + 30, { color: c.muted, width: 2 });
        Sim.text(ctx, 'floor holds the base', ox + s * 0.7 + 8, yb + 30, { size: 11, color: c.muted, weight: 600 });
      }
      if (S.th > 0.004) {
        const Rr = Math.min(40, s * 0.4);
        ctx.save(); ctx.strokeStyle = c.amber; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(ox, yb, Rr, -Math.PI / 2, -Math.PI / 2 + S.th); ctx.stroke(); ctx.restore();
        Sim.text(ctx, 'θ', ox + Rr * Math.tan(S.th) + 9, yb - Rr + 6, { size: f + 1, color: c.amber, weight: 700 });
        dimH(ctx, ox, ox + dx, yb - s - 34, 'Δx', c.coral, f);
      }
      dimV(ctx, ox - 16, yb - s, yb, 'L = 10 cm', c.muted, 11.5, 'left');
      Sim.text(ctx, M.label, w - 10, 14, { size: 11, color: c.muted, align: 'right', weight: 600 });

      const dxm = side * theta;
      out('sstress', sciF(S.F / A, 1) + ' Pa');
      out('theta', (theta >= 0.01 ? theta.toFixed(3) : sciF(theta, 2)) + ' rad' + (theta >= 0.01 ? ` (${(theta * 180 / Math.PI).toFixed(1)}°)` : ''));
      out('dx', dxm >= 1e-3 ? (dxm * 1000).toFixed(1) + ' mm' : (dxm * 1e6).toFixed(2) + ' µm');
    }
    const st = Sim.stage(host, { aspect: 16 / 10, minH: 260, maxH: 380, animate: true, draw });
    Sim.controls(root, (v) => { S.mat = v.mat; S.F = v['sh-F']; st.redraw(); });
  });

  /* =================================================================
     6. Bulk modulus — sphere under pressure + log comparison bars
     ================================================================= */
  setup('sim-bulk', (root, host) => {
    const ATM = 1.013e5;
    const MAT = {
      water: { name: 'Water', B: 2.2e9, ex: 10 },
      glass: { name: 'Glass', B: 3.7e10, ex: 200 },
      steel: { name: 'Steel', B: 1.6e11, ex: 200 },
      air: { name: 'Air', B: ATM, ex: 1, gas: true },
    };
    const ORDER = ['air', 'water', 'glass', 'steel'];
    const S = { mat: 'water', p: 300, r: 1 };
    const out = outCache(root);
    const frac = (k, pAtm) => {
      const m = MAT[k], dp = pAtm * ATM;
      if (dp <= 0) return 0;
      return m.gas ? dp / (ATM + dp) : dp / m.B;   // gas: isothermal (Boyle) from 1 atm
    };

    function draw(ctx, w, h, t, dt) {
      const c = Sim.C, f = fs(w), M = MAT[S.mat];
      const wide = w >= 560;
      const fv = frac(S.mat, S.p);
      const vis = Math.min(0.97, fv * M.ex);
      S.r = ease(S.r, Math.cbrt(1 - vis), dt, 6);

      // sphere area
      const sx = wide ? w * 0.27 : w / 2, sy = wide ? h / 2 : h * 0.29;
      const R0 = wide ? Math.min(h * 0.27, w * 0.15) : Math.min(h * 0.17, w * 0.2);
      ctx.fillStyle = alpha(c.water, 0.08);
      ctx.beginPath(); ctx.arc(sx, sy, R0 + 44, 0, Math.PI * 2); ctx.fill();
      ctx.save(); ctx.setLineDash([5, 5]); ctx.strokeStyle = c.muted; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.arc(sx, sy, R0, 0, Math.PI * 2); ctx.stroke(); ctx.restore();
      const Rn = R0 * S.r;
      const grd = ctx.createRadialGradient(sx - Rn * 0.35, sy - Rn * 0.35, Rn * 0.1, sx, sy, Rn);
      grd.addColorStop(0, alpha(c.accent, 0.12)); grd.addColorStop(1, alpha(c.accent, 0.38));
      ctx.fillStyle = grd; ctx.beginPath(); ctx.arc(sx, sy, Math.max(2, Rn), 0, Math.PI * 2); ctx.fill();
      ctx.strokeStyle = c.accent; ctx.lineWidth = 2; ctx.stroke();
      if (S.p > 0) {
        const L = 10 + 18 * Math.min(1, S.p / 1100);
        for (let i = 0; i < 12; i++) {
          const a = i / 12 * Math.PI * 2;
          const r1 = R0 + 12 + L, r2 = Math.max(Rn, 4) + 4;
          Sim.arrow(ctx, sx + Math.cos(a) * r1, sy + Math.sin(a) * r1, sx + Math.cos(a) * r2, sy + Math.sin(a) * r2, { color: c.water, width: 2, head: 7 });
        }
      }
      Sim.text(ctx, M.ex === 1 ? 'true scale' : `shrink drawn ×${M.ex}`, wide ? sx : w - 10, wide ? Math.min(h - 10, sy + R0 + 56) : 14, { size: 11, color: c.muted, align: wide ? 'center' : 'right', weight: 600 });

      // log bars
      const bx = wide ? w * 0.55 : 70, bw = wide ? w * 0.42 - 70 : w - 70 - 70;
      const by0 = wide ? h * 0.24 : h * 0.62, rowH = wide ? Math.min(34, h * 0.13) : Math.min(28, (h - by0 - 30) / 4);
      Sim.text(ctx, 'ΔV/V at this pressure (log scale)', bx - 60, by0 - 18, { size: 11.5, color: c.ink2, weight: 650 });
      const lg = v => clamp((Math.log10(Math.max(v, 1e-7)) + 6) / 6, 0, 1);
      ORDER.forEach((k, i) => {
        const v = frac(k, S.p), yy = by0 + i * rowH, sel = k === S.mat;
        Sim.text(ctx, MAT[k].name, bx - 8, yy + rowH * 0.4, { size: 12, color: sel ? c.accent : c.ink2, weight: sel ? 750 : 600, align: 'right' });
        roundedRect(ctx, bx, yy + rowH * 0.4 - 6, bw, 12, 6, c.surface2);
        if (v > 0) roundedRect(ctx, bx, yy + rowH * 0.4 - 6, Math.max(6, bw * lg(v)), 12, 6, sel ? c.accent : c.line2);
        const txt = v <= 0 ? '0' : v >= 0.01 ? (v * 100).toFixed(1) + '%' : sciF(v, 1);
        Sim.text(ctx, txt, bx + bw + 6, yy + rowH * 0.4, { size: 11, color: sel ? c.accent : c.muted, weight: 650, mono: true });
      });
      const ty = by0 + 4 * rowH + 2;
      [[0, '10⁻⁶'], [1 / 3, '10⁻⁴'], [2 / 3, '10⁻²'], [1, '1']].forEach(([q, s]) => {
        Sim.line(ctx, [[bx + bw * q, ty - 4], [bx + bw * q, ty + 2]], { color: c.line2, width: 1 });
        Sim.text(ctx, s, bx + bw * q, ty + 10, { size: 11, color: c.muted, align: 'center', mono: true });
      });

      const dp = S.p * ATM;
      out('dp', S.p + ' atm = ' + sciF(dp, 2) + ' Pa');
      out('dvv', fv === 0 ? '0' : fv >= 0.01 ? (fv * 100).toFixed(2) + ' %' : sciF(fv, 2));
      out('drr', fv === 0 ? '0' : M.gas ? ((1 - Math.cbrt(1 - fv)) * 100).toFixed(1) + ' %' : sciF(fv / 3, 2));
      out('depth', '≈ ' + Math.round(dp / (1030 * 9.8)).toLocaleString('en-IN') + ' m of sea water');
      out('bnote', M.gas ? 'For a gas the "small change" formula fails at large Δp: Boyle\'s law (pV = const) is used here. Isothermal B of a gas = its pressure, about 10⁵ Pa at 1 atm, so air is about 20 000× more compressible than water.'
        : `B(${M.name.toLowerCase()}) = ${sciF(M.B, 1)} Pa, so ΔV/V = Δp/B. Δr/r = Δp/3B.`);
    }
    const st = Sim.stage(host, { aspect: 16 / 9, minH: 330, maxH: 400, animate: true, draw });
    Sim.controls(root, (v) => { S.mat = v.mat; S.p = v['bk-p']; st.redraw(); });
  });

  /* =================================================================
     7. Poisson's ratio — stretch and thin
     ================================================================= */
  setup('sim-poisson', (root, host) => {
    const S = { s: 0.3, e: 0.1, ce: 0.1, cs: 0.3 };
    const out = outCache(root);
    function draw(ctx, w, h, t, dt) {
      const c = Sim.C, f = fs(w);
      S.ce = ease(S.ce, S.e, dt, 9); S.cs = ease(S.cs, S.s, dt, 9);
      const L0 = Math.min(w * 0.5, 420), D0 = Math.min(h * 0.32, 90);
      const L = L0 * (1 + S.ce), D = D0 * (1 - S.cs * S.ce);
      const cx = w / 2, cy = h * 0.48;
      // original
      Sim.rrect(ctx, cx - L0 / 2, cy - D0 / 2, L0, D0, 8);
      ctx.save(); ctx.setLineDash([6, 5]); ctx.strokeStyle = c.muted; ctx.lineWidth = 1.3; ctx.stroke(); ctx.restore();
      // stretched
      roundedRect(ctx, cx - L / 2, cy - D / 2, L, D, 8, alpha(c.accent, 0.16), c.accent, 2.2);
      const AL = 18 + 120 * S.ce;
      Sim.arrow(ctx, cx + L / 2 + 6, cy, cx + L / 2 + 6 + AL * 0.5 + 14, cy, { color: c.coral, width: 2.8 });
      Sim.arrow(ctx, cx - L / 2 - 6, cy, cx - L / 2 - 6 - AL * 0.5 - 14, cy, { color: c.coral, width: 2.8 });
      // lateral contraction arrows
      const dd = (D0 - D) / 2;
      if (dd > 0.6) {
        Sim.arrow(ctx, cx, cy - D0 / 2 - 22, cx, cy - D / 2 - 3, { color: c.green, width: 2, head: 7 });
        Sim.arrow(ctx, cx, cy + D0 / 2 + 22, cx, cy + D / 2 + 3, { color: c.green, width: 2, head: 7 });
        Sim.text(ctx, 'thins: Δd/d = −σ·ΔL/L', cx, cy + D0 / 2 + 36, { size: f, color: c.green, weight: 650, align: 'center' });
      }
      dimH(ctx, cx - L / 2, cx + L / 2, cy - D0 / 2 - 34, `L(1 + ${(S.ce * 100).toFixed(1)}%)`, c.ink2, f);
      dimV(ctx, cx + L / 2 - 26, cy - D / 2, cy + D / 2, 'd', c.ink2, f, 'left');
      Sim.text(ctx, 'strain exaggerated for visibility', w - 10, h - 12, { size: 11, color: c.muted, align: 'right', weight: 600 });

      const lat = S.s * S.e, dv = (1 + S.e) * Math.pow(1 - S.s * S.e, 2) - 1;
      out('long', (S.e * 100).toFixed(1) + ' %');
      out('lat', '−' + (lat * 100).toFixed(2) + ' %');
      out('dv', (dv >= 0 ? '+' : '') + (dv * 100).toFixed(2) + ' %');
      out('dvapprox', '(1−2σ)ε = ' + ((1 - 2 * S.s) * S.e * 100).toFixed(2) + ' %');
    }
    const st = Sim.stage(host, { aspect: 16 / 8, minH: 230, maxH: 320, animate: true, draw });
    const vals = Sim.controls(root, (v) => { S.s = v['po-s']; S.e = v['po-e'] / 100; st.redraw(); });
    root.querySelectorAll('[data-sigma]').forEach(b => b.addEventListener('click', () => {
      const inp = root.querySelector('#po-s');
      inp.value = b.dataset.sigma; inp.dispatchEvent(new Event('input'));
    }));
    void vals;
  });

  /* =================================================================
     8. Elastic energy — area under the force–extension line
     ================================================================= */
  setup('sim-energy', (root, host) => {
    const K = { steel: 2.0e5, copper: 1.1e5 };   // k = YA/L with A = 1 mm², L = 1 m
    const S = { mat: 'steel', x: 0.6, cx: 0.6, show: 'tri' };
    const out = outCache(root);
    function draw(ctx, w, h, t, dt) {
      const c = Sim.C, f = fs(w);
      S.cx = ease(S.cx, S.x, dt, 10);
      const box = { x: 52, y: 30, w: w - 52 - 22, h: h - 30 - 48 };
      const ax = Sim.axes(ctx, box, { xmin: 0, xmax: 1, ymin: 0, ymax: 220, xticks: [0, 0.25, 0.5, 0.75, 1], yticks: [0, 50, 100, 150, 200],
        xfmt: v => v === 0 ? '0' : v.toFixed(2), xlabel: 'Extension Δl (mm)', ylabel: 'Force F (N)' });
      const { X, Y } = ax;
      const k = K[S.mat], other = S.mat === 'steel' ? 'copper' : 'steel';
      const ko = K[other];
      Sim.line(ctx, [[X(0), Y(0)], [X(1), Y(ko * 1e-3)]], { color: c.line2, width: 1.8, dash: [5, 4] });
      Sim.text(ctx, other, X(1) - 4, Y(ko * 1e-3) + 13, { size: 11, color: c.muted, align: 'right', weight: 600 });
      const x = S.cx, F = k * x * 1e-3;
      if (S.show === 'rect' && x > 0.01) {
        Sim.line(ctx, [[X(0), Y(F)], [X(x), Y(F)], [X(x), Y(0)]], { color: c.coral, width: 1.6, dash: [5, 4] });
        ctx.save(); ctx.beginPath(); ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(0), Y(F)); ctx.lineTo(X(x), Y(F)); ctx.closePath();
        ctx.fillStyle = alpha(c.coral, 0.12); ctx.fill(); ctx.restore();
        if (X(x) - X(0) > 80) Sim.text(ctx, 'lost as heat', X(x * 0.3), Y(F * 0.82), { size: 11, color: c.coral, weight: 650, align: 'center' });
      }
      Sim.line(ctx, [[X(0), Y(0)], [X(x), Y(F)], [X(x), Y(0)]], { color: 'none', fill: alpha(c.accent, 0.25), close: true });
      Sim.line(ctx, [[X(0), Y(0)], [X(1), Y(k * 1e-3)]], { color: c.accent, width: 2.6 });
      Sim.text(ctx, S.mat, X(1) - 4, Y(k * 1e-3) - 12, { size: 11.5, color: c.accent, align: 'right', weight: 700 });
      Sim.line(ctx, [[X(x), Y(F)], [X(x), Y(0)]], { color: c.accent, width: 1.5 });
      dot(ctx, X(x), Y(F), 6, c.accent, c.surface);
      if (X(x) - X(0) > 70) Sim.text(ctx, 'U = ½ F Δl', X(x * 0.66), Y(F * 0.3), { size: f, color: c.ink, weight: 700, align: 'center' });

      const U = 0.5 * F * x * 1e-3, V = 1e-6;
      out('F', F.toFixed(0) + ' N');
      out('U', U >= 0.001 ? U.toFixed(4) + ' J' : sciF(U, 2) + ' J');
      out('u', sciF(Math.max(U / V, 1e-9), 2) + ' J m⁻³');
      out('W', S.show === 'rect' ? (F * x * 1e-3).toFixed(4) + ' J' : '—');
    }
    const st = Sim.stage(host, { aspect: 16 / 10, minH: 260, maxH: 400, animate: true, draw });
    Sim.controls(root, (v) => { S.mat = v.mat; S.show = v.show; S.x = v['en-x']; st.redraw(); });
  });

  /* =================================================================
     9. Beam bending — δ = W l³ / (4 b d³ Y)
     ================================================================= */
  setup('sim-beam', (root, host) => {
    const YM = { wood: 1.3e10, steel: 2.0e11 };
    const IFAC = 6.4375; // I-beam with the same area as the b×d rectangle: depth 2d, flanges b × 3d/8, web b/5
    const S = { W: 1000, l: 2, b: 10, d: 5, mat: 'wood', sec: 'rect', vis: 0 };
    const out = outCache(root);
    function delta() {
      const b = S.b / 100, d = S.d / 100;
      const rect = S.W * Math.pow(S.l, 3) / (4 * b * Math.pow(d, 3) * YM[S.mat]);
      return S.sec === 'ibeam' ? rect / IFAC : rect;
    }
    function draw(ctx, w, h, t, dt) {
      const c = Sim.C, f = fs(w);
      const dl = delta(), dmm = dl * 1000;
      const visT = Math.min(h * 0.3, dmm * 3);
      S.vis = ease(S.vis, visT, dt, 7);
      const margin = 30, span = (w - 2 * margin) * (0.45 + 0.55 * (S.l - 1) / 3);
      const x0 = w / 2 - span / 2, y0 = h * 0.36;
      const th = 6 + S.d * 1.3 * (S.sec === 'ibeam' ? 1.5 : 1);
      // supports
      [x0, x0 + span].forEach(px => {
        Sim.line(ctx, [[px, y0 + th / 2], [px - 12, y0 + th / 2 + 20], [px + 12, y0 + th / 2 + 20]], { color: c.ink2, width: 1.5, fill: c.surface2, close: true });
        hatch(ctx, px - 18, y0 + th / 2 + 20, 36, 8, c.line2, 5);
      });
      // deflected beam
      const N = 60, top = [], bot = [];
      for (let i = 0; i <= N; i++) {
        const u = i / N, q = u <= 0.5 ? u : 1 - u;
        const y = S.vis * q * (3 - 4 * q * q);
        top.push([x0 + span * u, y0 - th / 2 + y]);
        bot.push([x0 + span * u, y0 + th / 2 + y]);
      }
      Sim.line(ctx, [[x0, y0], [x0 + span, y0]], { color: c.muted, width: 1.2, dash: [5, 5] });
      Sim.line(ctx, top.concat(bot.reverse()), { color: S.mat === 'steel' ? c.ink2 : c.amber, width: 1.8, fill: alpha(S.mat === 'steel' ? c.ink2 : c.amber, 0.25), close: true });
      // load
      const mx = x0 + span / 2, my = y0 + th / 2 + S.vis;
      Sim.line(ctx, [[mx, my], [mx, my + 18]], { color: c.ink2, width: 2 });
      roundedRect(ctx, mx - 22, my + 18, 44, 24, 4, c.ink2);
      Sim.text(ctx, 'W', mx, my + 30, { size: 12, color: '#fff', weight: 700, align: 'center' });
      if (S.vis > 6) dimV(ctx, mx + 34, y0, y0 + S.vis, 'δ', c.coral, f + 1);
      dimH(ctx, x0, x0 + span, y0 - th / 2 - 16, `l = ${S.l.toFixed(1)} m`, c.ink2, f);
      Sim.text(ctx, 'sag exaggerated ×' + Math.max(1, Math.round(3 / ((span / S.l) / 1000))), 10, h - 12, { size: 11, color: c.muted, weight: 600 });

      // cross-section inset
      const ix = w - 70, iy = h - 62, sc = 2.6;
      const bw = Math.min(60, S.b * sc), dh = Math.min(44, S.d * sc);
      Sim.text(ctx, S.sec === 'ibeam' ? 'I-section (same area)' : 'cross-section b × d', ix, iy - 34, { size: 11, color: c.muted, align: 'center', weight: 600 });
      ctx.fillStyle = alpha(c.accent, 0.3); ctx.strokeStyle = c.accent; ctx.lineWidth = 1.5;
      if (S.sec === 'rect') {
        ctx.fillRect(ix - bw / 2, iy - dh / 2 + 6, bw, dh); ctx.strokeRect(ix - bw / 2, iy - dh / 2 + 6, bw, dh);
      } else {
        const D = Math.min(56, dh * 2), tf = D * 0.1875, tw = Math.max(3, bw / 5);
        const yT = iy - D / 2 + 6;
        ctx.beginPath();
        ctx.moveTo(ix - bw / 2, yT); ctx.lineTo(ix + bw / 2, yT); ctx.lineTo(ix + bw / 2, yT + tf); ctx.lineTo(ix + tw / 2, yT + tf);
        ctx.lineTo(ix + tw / 2, yT + D - tf); ctx.lineTo(ix + bw / 2, yT + D - tf); ctx.lineTo(ix + bw / 2, yT + D); ctx.lineTo(ix - bw / 2, yT + D);
        ctx.lineTo(ix - bw / 2, yT + D - tf); ctx.lineTo(ix - tw / 2, yT + D - tf); ctx.lineTo(ix - tw / 2, yT + tf); ctx.lineTo(ix - bw / 2, yT + tf);
        ctx.closePath(); ctx.fill(); ctx.stroke();
      }
      if (dl > 0.05 * S.l) Sim.text(ctx, 'Such a sag is unrealistic: the beam would break', w / 2, 16, { size: f, color: c.coral, weight: 700, align: 'center', bg: c.coralSoft });

      out('delta', dmm >= 100 ? dmm.toFixed(0) + ' mm' : dmm >= 1 ? dmm.toFixed(2) + ' mm' : (dmm * 1000).toFixed(1) + ' µm');
      out('bd3', S.sec === 'ibeam' ? '6.4× stiffer than b×d' : sciF((S.b / 100) * Math.pow(S.d / 100, 3), 2) + ' m⁴');
      out('formula', `δ = Wl³/(4bd³Y) = ${S.W}×${S.l.toFixed(1)}³ / (4×${(S.b / 100).toFixed(2)}×${(S.d / 100).toFixed(2)}³×${sciF(YM[S.mat], 1)})${S.sec === 'ibeam' ? ' ÷ 6.4 (I-section)' : ''} = ${dmm >= 1 ? dmm.toFixed(2) + ' mm' : (dmm * 1000).toFixed(1) + ' µm'}`);
    }
    const st = Sim.stage(host, { aspect: 16 / 9, minH: 260, maxH: 380, animate: true, draw });
    Sim.controls(root, (v) => {
      S.W = v['bm-W']; S.l = v['bm-l']; S.b = v['bm-b']; S.d = v['bm-d']; S.mat = v.mat; S.sec = v.sec;
      st.redraw();
    });
    const set = (k) => root.querySelector(k);
    const dbl = set('#bm-double'), half = set('#bm-half');
    const change = (fac) => {
      const inp = set('#bm-d');
      const nv = clamp(Math.round(+inp.value * fac), +inp.min, +inp.max);
      inp.value = nv; inp.dispatchEvent(new Event('input'));
    };
    if (dbl) dbl.addEventListener('click', () => change(2));
    if (half) half.addEventListener('click', () => change(0.5));
  });
})();
