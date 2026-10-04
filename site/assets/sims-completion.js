/* Models for combined wires, viscous pipe flow and capillary measurements. */
(function () {
  'use strict';
  function model(id, draw, update) {
    const root = document.getElementById(id);
    if (!root) return;
    const panel = root.querySelector('.sim-panel');
    let values = null, stage;
    stage = Sim.stage(root.querySelector('.sim-stage'), {
      aspect: 4 / 3, minH: 300, maxH: 400,
      draw(ctx, w, h) { if (values) draw(ctx, w, h, values); }
    });
    Sim.controls(panel, next => {
      values = next;
      update(panel, values);
      stage.redraw();
    });
    document.fonts?.ready.then(() => stage.redraw());
  }

  function wires(v) {
    const k1 = v['wc-k1'], k2 = v['wc-k2'], F = v['wc-F'];
    const parallel = v.connection === 'parallel';
    const k = parallel ? k1 + k2 : k1 * k2 / (k1 + k2);
    return { parallel, k, extension: F / k,
      f1: parallel ? F * k1 / k : F, f2: parallel ? F * k2 / k : F };
  }
  function vesselValues(v) {
    const A1 = v['cv-A1'], A2 = v['cv-A2'], h1 = v['cv-h1'], h2 = v['cv-h2'];
    const final = (A1 * h1 + A2 * h2) / (A1 + A2);
    return { A1, A2, h1, h2, final,
      work: 1000 * 10 * A1 * A2 * (h1 - h2) ** 2 / (2 * (A1 + A2)),
      transferred: Math.abs(A1 * (h1 - final)) };
  }
  model('sim-connected-vessels', (ctx, w, h, v) => {
    const c = Sim.C, p = vesselValues(v), bottom = h - 65, top = 40;
    const scale = (bottom - top) / 9;
    const widths = [p.A1, p.A2].map(A => (w * 0.15) * Math.sqrt(A));
    const centers = [w * 0.26, w * 0.74];
    const heights = v.state === 'after' ? [p.final, p.final] : [p.h1, p.h2];
    for (let i = 0; i < 2; i++) {
      const left = centers[i] - widths[i] / 2, right = centers[i] + widths[i] / 2;
      const surface = bottom - heights[i] * scale;
      ctx.fillStyle = c.waterSoft;
      ctx.fillRect(left, surface, widths[i], bottom - surface);
      Sim.line(ctx, [[left, top], [left, bottom], [right, bottom], [right, top]], { color: c.ink2, width: 2 });
      Sim.line(ctx, [[left, surface], [right, surface]], { color: c.water, width: 2 });
      Sim.text(ctx, `${heights[i].toFixed(1)} m`, centers[i], surface - 8, { align: 'center', size: 12, color: c.water });
      Sim.text(ctx, `A${i + 1} = ${[p.A1, p.A2][i]} m²`, centers[i], bottom + 42, { align: 'center', size: 12 });
    }
    const a = centers[0] + widths[0] / 2, b = centers[1] - widths[1] / 2;
    Sim.line(ctx, [[a, bottom - 7], [b, bottom - 7]], { color: c.water, width: 6 });
    if (v.state === 'before') {
      Sim.line(ctx, [[w / 2, bottom - 20], [w / 2, bottom + 6]], { color: c.coral, width: 4 });
      Sim.text(ctx, 'valve closed', w / 2, 18, { align: 'center', size: 12 });
    } else {
      Sim.text(ctx, 'same pressure at the bottom', w / 2, 18, { align: 'center', size: 12 });
    }
  }, (panel, v) => {
    const p = vesselValues(v);
    Sim.out(panel, 'height', `${p.final.toFixed(3)} m`);
    Sim.out(panel, 'work', `${p.work.toFixed(0)} J`);
    Sim.out(panel, 'volume', `${p.transferred.toFixed(3)} m³`);
  });
  model('sim-combined-wires', (ctx, w, h, v) => {
    const c = Sim.C, p = wires(v), cx = w / 2;
    const top = 40, bottom = h - 60;
    const extra = Math.min(35, p.extension * 5);
    Sim.line(ctx, [[w * 0.18, top], [w * 0.82, top]], { color: c.ink2, width: 5 });
    if (p.parallel) {
      const left = cx - w * 0.18, right = cx + w * 0.18, end = bottom + extra / 2;
      Sim.line(ctx, [[left, top], [left, end]], { color: c.indigo, width: 5 });
      Sim.line(ctx, [[right, top], [right, end]], { color: c.water, width: 5 });
      Sim.line(ctx, [[left - 12, end], [right + 12, end]], { color: c.ink2, width: 6 });
      Sim.text(ctx, 'k₁', left - 18, (top + end) / 2, { color: c.indigo, weight: 700 });
      Sim.text(ctx, 'k₂', right + 18, (top + end) / 2, { color: c.water, weight: 700 });
      Sim.text(ctx, 'equal extension', cx, 18, { align: 'center', size: 12 });
      Sim.arrow(ctx, cx, end + 7, cx, end + 32, { color: c.coral, width: 2 });
    } else {
      const middle = (top + bottom) / 2, end = bottom + extra / 2;
      Sim.line(ctx, [[cx, top], [cx, middle]], { color: c.indigo, width: 5 });
      Sim.line(ctx, [[cx, middle], [cx, end]], { color: c.water, width: 5 });
      Sim.text(ctx, 'k₁', cx - 25, (top + middle) / 2, { color: c.indigo, weight: 700 });
      Sim.text(ctx, 'k₂', cx - 25, (middle + end) / 2, { color: c.water, weight: 700 });
      Sim.text(ctx, 'equal tension', cx, 18, { align: 'center', size: 12 });
      Sim.arrow(ctx, cx, end + 6, cx, end + 30, { color: c.coral, width: 2 });
    }
    Sim.text(ctx, `${v['wc-F']} N total load`, cx, h - 13, { align: 'center', color: c.coral, size: 12 });
  }, (panel, v) => {
    const p = wires(v);
    Sim.out(panel, 'extension', `${p.extension.toFixed(3)} mm`);
    Sim.out(panel, 'stiffness', `${p.k.toFixed(1)} N/mm`);
    Sim.out(panel, 'force1', `${p.f1.toFixed(1)} N`);
    Sim.out(panel, 'force2', `${p.f2.toFixed(1)} N`);
  });

  function pipe(v) {
    const r = v['pf-r'] / 1000, eta = v['pf-eta'] / 1000;
    const Q = Math.PI * r ** 4 * v['pf-dP'] / (8 * eta * v['pf-L']);
    const mean = Q / (Math.PI * r * r);
    return { Q, mean, maximum: 2 * mean, Re: 1000 * mean * 2 * r / eta };
  }
  model('sim-pipe-flow', (ctx, w, h, v) => {
    const c = Sim.C, p = pipe(v), left = 22, right = w - 22;
    const top = 62, bottom = h - 56, mid = (top + bottom) / 2;
    const extent = Math.max(25, Math.min(w * 0.5, 40 + p.maximum * 150));
    ctx.fillStyle = c.waterSoft;
    ctx.fillRect(left, top, right - left, bottom - top);
    Sim.line(ctx, [[left, top], [right, top]], { color: c.ink2, width: 4 });
    Sim.line(ctx, [[left, bottom], [right, bottom]], { color: c.ink2, width: 4 });
    const points = [];
    for (let n = 0; n <= 40; n++) {
      const s = -1 + n / 20, y = mid + s * (bottom - top) / 2;
      points.push([left + 20 + extent * (1 - s * s), y]);
    }
    Sim.line(ctx, points, { color: c.accent, width: 2.5 });
    for (let n = -4; n <= 4; n++) {
      const s = n / 5, y = mid + s * (bottom - top) / 2;
      Sim.arrow(ctx, left + 20, y, left + 20 + extent * (1 - s * s), y, { color: c.water, width: 1.7, head: 6 });
    }
    Sim.text(ctx, 'stationary wall: v = 0', w / 2, top - 14, { align: 'center', size: 12 });
    Sim.text(ctx, 'parabolic velocity profile', w / 2, bottom + 21, { align: 'center', size: 12 });
    Sim.text(ctx, `ΔP = ${v['pf-dP']} Pa`, w / 2, 20, { align: 'center', color: c.accent, weight: 700 });
  }, (panel, v) => {
    const p = pipe(v);
    Sim.out(panel, 'flow', `${(p.Q * 1e6).toFixed(4)} mL/s`);
    Sim.out(panel, 'mean', `${p.mean.toFixed(4)} m/s`);
    Sim.out(panel, 'maximum', `${p.maximum.toFixed(4)} m/s`);
    Sim.out(panel, 'reynolds', p.Re.toFixed(0));
    Sim.out(panel, 'validity', p.Re >= 1000
      ? 'The predicted Reynolds number is leaving the low-Re range used in your coaching convention. Check the flow regime: this curve remains a laminar-model prediction.'
      : 'A low Reynolds number supports the laminar-flow assumption. Entrance effects, non-Newtonian fluids and turbulence are outside this model.');
  });

  model('sim-capillary-measurement', (ctx, w, h, v) => {
    const c = Sim.C, cx = w * 0.4, level = h - 65;
    const rise = v['ce-h'] * Math.min(14, (h - 130) / 10);
    const meniscus = level - rise, tubeWidth = 12 + v['ce-r'] * 16;
    ctx.fillStyle = c.waterSoft;
    ctx.fillRect(20, level, w - 40, 45);
    Sim.line(ctx, [[20, level], [w - 20, level]], { color: c.water, width: 2 });
    ctx.fillStyle = c.waterSoft;
    ctx.fillRect(cx - tubeWidth / 2, meniscus, tubeWidth, level - meniscus);
    Sim.line(ctx, [[cx - tubeWidth / 2, 42], [cx - tubeWidth / 2, level + 25]], { color: c.ink2, width: 2 });
    Sim.line(ctx, [[cx + tubeWidth / 2, 42], [cx + tubeWidth / 2, level + 25]], { color: c.ink2, width: 2 });
    ctx.beginPath(); ctx.moveTo(cx - tubeWidth / 2, meniscus - 5);
    ctx.quadraticCurveTo(cx, meniscus + 5, cx + tubeWidth / 2, meniscus - 5);
    ctx.strokeStyle = c.water; ctx.lineWidth = 2; ctx.stroke();
    const x = Math.min(w - 50, cx + 65);
    Sim.arrow(ctx, x, meniscus, x, level, { color: c.coral, width: 2 });
    Sim.text(ctx, `h = ${v['ce-h'].toFixed(1)} cm`, x + 9, (meniscus + level) / 2, { size: 11, color: c.coral });
    Sim.text(ctx, 'outside water level', w / 2, level + 57, { align: 'center', size: 12 });
    Sim.text(ctx, `inner radius = ${v['ce-r'].toFixed(2)} mm`, w / 2, 20, { align: 'center', size: 12, weight: 700 });
  }, (panel, v) => {
    const T = 1000 * 9.8 * (v['ce-r'] / 1000) * (v['ce-h'] / 100) / 2;
    const error = v['ce-er'] + v['ce-eh'];
    Sim.out(panel, 'tension', `${T.toFixed(4)} N/m`);
    Sim.out(panel, 'error', `±${error.toFixed(1)}% (±${(T * error / 100).toFixed(4)} N/m)`);
  });
})();
