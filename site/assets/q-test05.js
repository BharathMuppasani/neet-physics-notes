/* Narayana NEET Jr Star — Module Test-05 (26.09.2026), Physics Q1–45
   Mechanical Properties of Fluids, part 1: pressure, Pascal, buoyancy, flow, Bernoulli, Torricelli.
   `flagged: true` = the question carries a ✗ mark on the photographed paper. */
(function () {
  const R = String.raw;
  window.QBANK = window.QBANK || [];

  /* ---------- tiny SVG helpers (light theme tokens via CSS vars) ---------- */
  const W = 'style="fill:none;stroke:var(--ink-2);stroke-width:2;stroke-linejoin:round"';
  const WATER = 'style="fill:var(--water-soft);stroke:none"';
  const SURF = 'style="fill:none;stroke:var(--water);stroke-width:1.5"';
  const T = (x, y, s, o = '') => `<text x="${x}" y="${y}" font-size="12" style="fill:var(--ink-2);font-family:var(--f-body)" ${o}>${s}</text>`;
  const ARW = (x1, y1, x2, y2, c = 'var(--coral)') => {
    const a = Math.atan2(y2 - y1, x2 - x1), h = 8;
    const p1 = [x2 - h * Math.cos(a - .45), y2 - h * Math.sin(a - .45)], p2 = [x2 - h * Math.cos(a + .45), y2 - h * Math.sin(a + .45)];
    return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" style="stroke:${c};stroke-width:2"/><polygon points="${x2},${y2} ${p1} ${p2}" style="fill:${c}"/>`;
  };
  /* small graph for options: axes + curve path, origin at (16,70) */
  const GRAPH = (path, ylab, xlab, mark = '') => `<svg viewBox="0 0 130 86" width="130" height="86" role="img" aria-label="graph">
    <path d="M16 6 V70 H122" ${W}/>
    <path d="${path}" style="fill:none;stroke:var(--accent);stroke-width:2.5;stroke-linecap:round"/>
    ${T(20, 12, ylab, 'font-size="11"')}${T(112, 82, xlab, 'font-size="11"')}${T(6, 80, '0', 'font-size="10"')}${mark}</svg>`;

  QBANK.push(
  {
    id: 't05-01', src: 't05', qno: 1, topic: 'pascal', type: 'numerical',
    q: R`<p>Two syringes (without needles) of different cross-sections are connected with a tightly fitted rubber tube filled with water. Diameters of the smaller piston and larger piston are 1 cm and 3 cm respectively. Find the force exerted on the larger piston when a force of 10 N is applied to the smaller piston.</p>`,
    opts: ['30 N', '60 N', '90 N', '120 N'], ans: 2,
    sol: R`<ol class="steps">
      <li>Pascal's law: the extra pressure is the same on both pistons, so \( \dfrac{F_1}{A_1} = \dfrac{F_2}{A_2} \).</li>
      <li>Area \( \propto d^2 \), so \( \dfrac{A_2}{A_1} = \left(\dfrac{3}{1}\right)^2 = 9 \).</li>
      <li>\( F_2 = 10 \times 9 = 90 \text{ N} \).</li></ol>`,
    trap: R`Using the diameter ratio (3) instead of the area ratio (9) gives 30 N, which is option 1. Always square the diameter ratio.`,
  },
  {
    id: 't05-02', src: 't05', qno: 2, topic: 'pascal', type: 'statement',
    q: R`<div class="ar"><p><strong>Statement 1:</strong> Whenever external pressure is applied on any part of a fluid contained in a vessel, the pressure is transmitted until the pressure becomes equal throughout the fluid.</p><p><strong>Statement 2:</strong> A number of devices, such as hydraulic lift and hydraulic brakes, are based on Pascal's law.</p></div>`,
    opts: ['Both statement 1 and 2 are correct.', 'Statement 1 is correct but statement 2 is incorrect.', 'Statement 1 is incorrect but statement 2 is correct.', 'Both statement 1 &amp; 2 are incorrect.'], ans: 0,
    sol: R`<p>Statement 1 is Pascal's law: extra pressure applied to an enclosed fluid is transmitted undiminished to every part of it (gravity aside, the pressure evens out everywhere). Statement 2 is also true: hydraulic lifts, presses and brakes all multiply force using Pascal's law.</p>`,
  },
  {
    id: 't05-03', src: 't05', qno: 3, topic: 'pascal-law', type: 'ar', flagged: true,
    q: R`<div class="ar"><p><strong>Assertion (A):</strong> The pressure at a point in a fluid contained in a vessel placed on a table acts in the downward direction.</p><p><strong>Reason (R):</strong> The force exerted by a fluid at rest on any surface is always normal to that surface.</p></div>`,
    opts: ['Both A and R are true and R is the correct explanation of A.', 'Both A and R are true but R is not the correct explanation of A.', 'A is true but R is false.', 'A is false but R is true.'], ans: 3,
    sol: R`<p><strong>A is false.</strong> Pressure is a <em>scalar</em>. At a point in a fluid at rest it is the same in every direction, so it has no direction of its own, not even "downward".</p>
      <p><strong>R is true.</strong> A fluid at rest cannot exert a tangential force: if it did, the layers would slide and the fluid would flow. So its force on any surface is normal (perpendicular) to that surface.</p>`,
    trap: R`It is the <em>force</em> due to pressure that has a direction (normal to the surface). Pressure itself has no direction.`,
  },
  {
    id: 't05-04', src: 't05', qno: 4, topic: 'connected-vessels', type: 'numerical',
    q: R`<p>Two cylindrical vessels of equal cross-sectional area of 2 m² contain water up to 6 m and 4 m, respectively. If the vessels are connected at their bottom, then the work done by the force of gravity is (density of water = 10³ kg/m³, g = 10 m/s²):</p>`,
    opts: ['1 × 10⁴ J', '2 × 10⁴ J', '4 × 10⁴ J', '8 × 10⁴ J'], ans: 1,
    sol: R`<ol class="steps">
      <li>The areas are equal, so the levels settle at the average: \( \frac{6+4}{2} = 5 \text{ m} \) each.</li>
      <li>Effectively a 1 m layer moves from the top of vessel A (between 5 m and 6 m, centre at 5.5 m) to vessel B (between 4 m and 5 m, centre at 4.5 m). Its centre of mass falls by 1 m.</li>
      <li>Mass of that layer: \( m = \rho A h = 1000 \times 2 \times 1 = 2000 \text{ kg} \).</li>
      <li>\( W_g = mg\,\Delta h = 2000 \times 10 \times 1 = 2 \times 10^4 \text{ J} \).</li></ol>
      <p class="small muted">Check with energies: \( U = \tfrac12 \rho A g h^2 \) per vessel. Before: \( \tfrac12(1000)(2)(10)(36+16) = 5.2\times10^5 \text{ J} \); after: \( \tfrac12(1000)(2)(10)(25+25) = 5.0\times10^5 \text{ J} \). The drop of \( 2\times10^4 \text{ J} \) is the work done by gravity.</p>`,
  },
  {
    id: 't05-05', src: 't05', qno: 5, topic: 'pascal', type: 'numerical', flagged: true,
    q: R`<p>A hydraulic press containing water has two arms with diameters 1.4 cm and 7 cm. A force of 20 N is applied on the surface of water in the thinner arm. The force required to be applied on the surface of water in the thicker arm to maintain equilibrium of water is ____ N.</p>`,
    fig: `<svg viewBox="0 0 320 170" role="img" aria-label="Hydraulic press with a wide 7 cm arm and a narrow 1.4 cm arm">
      <rect x="40" y="62" width="90" height="62" ${WATER}/><rect x="40" y="118" width="222" height="28" ${WATER}/><rect x="240" y="62" width="22" height="60" ${WATER}/>
      <path d="M40 30 V146 H262 V30 M130 30 V118 H240 V30" ${W}/>
      <line x1="40" y1="62" x2="130" y2="62" style="stroke:var(--ink);stroke-width:4"/><line x1="240" y1="62" x2="262" y2="62" style="stroke:var(--ink);stroke-width:4"/>
      ${ARW(251, 18, 251, 58)}${T(268, 26, '20 N')}${ARW(85, 18, 85, 58, 'var(--indigo)')}${T(96, 26, 'F = ?')}
      ${T(66, 96, '7 cm')}${T(268, 100, '1.4 cm')}</svg>`,
    opts: ['100 N', '500 N', '4 N', '0.8 N'], ans: 1,
    sol: R`<ol class="steps">
      <li>Equal pressure on both surfaces: \( \dfrac{F_\text{thick}}{A_\text{thick}} = \dfrac{F_\text{thin}}{A_\text{thin}} \).</li>
      <li>\( \dfrac{A_\text{thick}}{A_\text{thin}} = \left(\dfrac{7}{1.4}\right)^2 = 5^2 = 25 \).</li>
      <li>\( F_\text{thick} = 20 \times 25 = 500 \text{ N} \).</li></ol>`,
    trap: R`100 N (option 1) comes from multiplying by the diameter ratio 5. Pressure is force per <em>area</em>, and area goes as \( d^2 \).`,
  },
  {
    id: 't05-06', src: 't05', qno: 6, topic: 'buoyancy', type: 'concept',
    q: R`<p>A candle of diameter d is floating on a liquid in a cylindrical container of diameter D (D ≫ d). If it is burning at a rate of 4 cm/hour, then the bottom of the candle will (initially, total length of the candle is 2L, L immersed in fluid):</p>`,
    fig: `<svg viewBox="0 0 300 170" role="img" aria-label="Candle of length 2L floating with length L under the liquid in a wide container">
      <rect x="30" y="70" width="240" height="80" ${WATER}/><line x1="30" y1="70" x2="270" y2="70" ${SURF}/>
      <path d="M30 30 V150 H270 V30" ${W}/>
      <rect x="140" y="30" width="18" height="80" style="fill:var(--amber-soft);stroke:var(--amber);stroke-width:1.5"/>
      <path d="M149 14 q6 8 0 14 q-6 -6 0 -14" style="fill:var(--coral)"/>
      ${T(166, 52, 'L')}${T(166, 94, 'L')}${T(122, 128, 'd')}
      ${ARW(150, 162, 268, 162, 'var(--muted)')}${ARW(150, 162, 32, 162, 'var(--muted)')}${T(144, 158, 'D')}</svg>`,
    opts: ['Remain at the same height', 'Fall at the rate of 1 cm/hour', 'Fall at the rate of 2 cm/hour', 'Go up at the rate of 2 cm/hour'], ans: 3,
    sol: R`<ol class="steps">
      <li>Floating with L of 2L submerged means \( \rho_\text{candle}/\rho_\text{liquid} = \tfrac12 \). The candle always floats with half its <em>current</em> length under the liquid.</li>
      <li>Length after time t: \( \ell = 2L - 4t \), so the submerged length is \( \ell/2 = L - 2t \) (cm, h).</li>
      <li>Since \( D \gg d \), the liquid level hardly changes. The bottom is at depth \( L - 2t \) below a fixed surface, so it <strong>rises at 2 cm/h</strong>.</li></ol>`,
    key: R`A floating body keeps the same <em>fraction</em> submerged, \( \rho_\text{body}/\rho_\text{liquid} \), whatever its size.`,
  },
  {
    id: 't05-07', src: 't05', qno: 7, topic: 'buoyancy', type: 'numerical',
    q: R`<p>A solid sphere of volume V and density d floats at the interface of two immiscible liquids of densities \( \frac{d}{3} \) and \( \frac{4d}{3} \) respectively. The ratio of volume of parts of the sphere in lower and upper liquid is:</p>`,
    opts: ['1 : 2', '2 : 1', '1 : 3', '3 : 1'], ans: 1,
    sol: R`<ol class="steps">
      <li>Let a fraction x of the volume be in the lower (denser, \( 4d/3 \)) liquid and \( 1-x \) in the upper (\( d/3 \)) liquid.</li>
      <li>Weight = total buoyancy: \( V d g = xV\frac{4d}{3}g + (1-x)V\frac{d}{3}g \).</li>
      <li>\( 3 = 4x + 1 - x \Rightarrow x = \tfrac23 \). Lower : upper = \( \tfrac23 : \tfrac13 = 2:1 \).</li></ol>`,
  },
  {
    id: 't05-08', src: 't05', qno: 8, topic: 'buoyancy', type: 'numerical',
    q: R`<p>A cubical block of density \( \rho_b = 900\ \text{kg/m}^3 \) floats in a liquid of density \( \rho_\ell = 1000\ \text{kg/m}^3 \). If the height of the block is H = 8 m, then the volume of the submerged part is (in m³):</p>`,
    opts: ['230.4', '512', '51.2', '460.8'], ans: 3,
    sol: R`<ol class="steps"><li>Volume of the cube \( = 8^3 = 512 \text{ m}^3 \).</li>
      <li>Fraction submerged \( = \rho_b/\rho_\ell = 0.9 \).</li>
      <li>Submerged volume \( = 0.9 \times 512 = 460.8 \text{ m}^3 \).</li></ol>`,
  },
  {
    id: 't05-09', src: 't05', qno: 9, topic: 'buoyancy', type: 'numerical',
    q: R`<p>A sphere of relative density 2 and diameter D has a concentric cavity of diameter d. The ratio of \( \frac{d}{D} \), if it just floats in a tank of water, is:</p>`,
    opts: [R`\( 2^{1/3} \)`, R`\( 2^{2/3} \)`, R`\( 2^{4/3} \)`, R`\( 2^{-1/3} \)`], ans: 3,
    sol: R`<ol class="steps">
      <li>"Just floats" means it is fully submerged with weight = buoyancy.</li>
      <li>Mass of material \( = 2\rho_w \cdot \frac{\pi}{6}(D^3 - d^3) \). Water displaced \( = \rho_w \cdot \frac{\pi}{6} D^3 \).</li>
      <li>\( 2(D^3 - d^3) = D^3 \Rightarrow d^3 = \frac{D^3}{2} \Rightarrow \dfrac{d}{D} = 2^{-1/3} \).</li></ol>`,
  },
  {
    id: 't05-10', src: 't05', qno: 10, topic: 'buoyancy', type: 'numerical',
    q: R`<p>A uniform cylinder of length 1 m, mass 10 kg, density 4000 kg/m³ is suspended vertically from a fixed point by a massless spring such that it is fully submerged in a liquid of density 2000 kg/m³ at equilibrium. The extension \( x_0 \) of the spring is (k = 1000 N/m, g = 10 m/s²):</p>`,
    opts: ['2 cm', '3 cm', '5 cm', '4 cm'], ans: 2,
    sol: R`<ol class="steps">
      <li>Volume \( V = m/\rho = 10/4000 = 2.5\times10^{-3} \text{ m}^3 \).</li>
      <li>Buoyancy \( = 2000 \times 2.5\times10^{-3} \times 10 = 50 \text{ N} \). Weight = 100 N.</li>
      <li>Spring force \( kx_0 = 100 - 50 = 50 \text{ N} \Rightarrow x_0 = 50/1000 = 0.05 \text{ m} = 5 \text{ cm} \).</li></ol>`,
  },
  {
    id: 't05-11', src: 't05', qno: 11, topic: 'buoyancy', type: 'numerical',
    q: R`<p>A cubical block of side 1 m floats on water with 50% of its volume under water. What is the maximum weight that can be put on the block without fully submerging it under water? [density of water = 1000 kg/m³]</p>`,
    opts: ['500 kg', '400 kg', '250 kg', '125 kg'], ans: 0,
    sol: R`<ol class="steps"><li>Block mass = water displaced at half submersion \( = 0.5 \times 1 \times 1000 = 500 \text{ kg} \).</li>
      <li>Fully submerged, it can displace \( 1000 \text{ kg} \) of water.</li>
      <li>Extra load \( = 1000 - 500 = 500 \text{ kg} \).</li></ol>`,
  },
  {
    id: 't05-12', src: 't05', qno: 12, topic: 'buoyancy', type: 'concept', flagged: true,
    q: R`<p>A wooden block, with a coin placed on its top, floats in water as shown. The distance L indicates the length of the block outside water and h indicates the water level. After some time, the coin falls into water. Then (\( \rho_\text{coin} > \rho_\text{water} \)):</p>`,
    fig: `<svg viewBox="0 0 300 170" role="img" aria-label="Floating wooden block with a coin on top; L is the height above water, h the water level">
      <rect x="40" y="70" width="220" height="80" ${WATER}/><line x1="40" y1="70" x2="260" y2="70" ${SURF}/>
      <path d="M40 30 V150 H260 V30" ${W}/>
      <rect x="80" y="50" width="60" height="50" style="fill:var(--amber-soft);stroke:var(--amber);stroke-width:1.5"/>
      <rect x="100" y="43" width="22" height="7" rx="2" style="fill:var(--ink-2)"/>${T(128, 40, 'coin')}
      ${T(146, 64, 'L')}${ARW(230, 110, 230, 72, 'var(--muted)')}${ARW(230, 110, 230, 148, 'var(--muted)')}${T(238, 114, 'h')}</svg>`,
    opts: ['L decreases and h increases', 'L increases and h decreases', 'Both L and h increase', 'Both L and h decrease'], ans: 1,
    sol: R`<ol class="steps">
      <li><strong>L:</strong> the block loses the coin's weight, so it needs less buoyancy and floats higher. L <strong>increases</strong>.</li>
      <li><strong>h:</strong> on the block, the coin is effectively floating, so it displaces water equal to its <em>weight</em>: volume \( m/\rho_w \).</li>
      <li>In the water it sinks and displaces only its own <em>volume</em> \( m/\rho_c \), which is smaller because \( \rho_c > \rho_w \).</li>
      <li>Less water is displaced in total, so the level h <strong>decreases</strong>.</li></ol>`,
    trap: R`This is the classic "stone thrown out of a boat" problem. Floating objects displace their <em>weight</em> of water; sunk objects displace only their <em>volume</em>.`,
  },
  {
    id: 't05-13', src: 't05', qno: 13, topic: 'buoyancy', type: 'numerical', flagged: true,
    q: R`<p>Consider a solid sphere of radius R and density \( \rho(r) = \rho_0\left(1 - \frac{r}{R}\right),\ 0 < r \le R \). The minimum density of a liquid in which it will float is (r is the distance from the centre of the sphere):</p>`,
    opts: [R`\( \frac{2\rho_0}{3} \)`, R`\( \frac{2\rho_0}{5} \)`, R`\( \frac{\rho_0}{5} \)`, R`\( \frac{\rho_0}{4} \)`], ans: 3,
    sol: R`<ol class="steps">
      <li>It floats if the liquid density is at least the sphere's <em>average</em> density.</li>
      <li>Mass: \( M = \int_0^R \rho_0\left(1-\frac rR\right)4\pi r^2\,dr = 4\pi\rho_0\left[\frac{R^3}{3} - \frac{R^3}{4}\right] = \frac{\pi\rho_0 R^3}{3} \).</li>
      <li>Average density \( = \dfrac{M}{\frac43\pi R^3} = \dfrac{\pi\rho_0R^3/3}{4\pi R^3/3} = \dfrac{\rho_0}{4} \).</li></ol>`,
    trap: R`Don't take the density at the middle radius (\( \rho_0/2 \)). Most of the volume is near the surface, where the density is lowest, so you must integrate.`,
  },
  {
    id: 't05-14', src: 't05', qno: 14, topic: 'buoyancy', type: 'numerical',
    q: R`<p>An air bubble of radius 1 cm in water has an upward acceleration \( g/100 \) m s⁻². The density of water is 1000 kg/m³ and water offers negligible drag force. The weight of the bubble is (g = 10 m/s²):</p>`,
    opts: ['15.5 × 10⁻³ N', '25 × 10⁻³ N', '31.5 × 10⁻³ N', '41.5 × 10⁻³ N'], ans: 3,
    sol: R`<ol class="steps">
      <li>Buoyancy \( B = \rho_w V g = 1000 \times \frac43\pi(0.01)^3 \times 10 = 4.19\times10^{-2} \text{ N} \).</li>
      <li>Newton's 2nd law (upward): \( B - mg = m\frac{g}{100} \Rightarrow B = mg(1.01) \).</li>
      <li>\( mg = \dfrac{4.19\times10^{-2}}{1.01} \approx 4.15\times10^{-2} \text{ N} = 41.5\times10^{-3} \text{ N} \).</li></ol>`,
  },
  {
    id: 't05-15', src: 't05', qno: 15, topic: 'buoyancy', type: 'concept', flagged: true,
    q: R`<p>A body of density greater than water is completely immersed in water. The buoyant force acting on the body is equal to:</p>`,
    opts: ['Weight of the body', 'Weight of water displaced by the body', 'Mass of the body', 'Zero'], ans: 1,
    sol: R`<p>By Archimedes' principle, buoyancy always equals the weight of the fluid displaced, whether the body floats or sinks. Here it is less than the body's weight (that's why it sinks), but it is certainly not zero.</p>
      <ul><li>Option 1 holds only for a floating body.</li><li>Option 3 is a mass, not a force.</li><li>Option 4: buoyancy acts on every immersed body.</li></ul>`,
  },
  {
    id: 't05-16', src: 't05', qno: 16, topic: 'flow', type: 'ar', flagged: true,
    q: R`<div class="ar"><p><strong>Assertion (A):</strong> In a steady flow, two different fluid particles passing through the same point at different times must have the same velocity at that point.</p><p><strong>Reason (R):</strong> Steady flow means that the velocity of each fluid particle remains constant throughout its motion.</p></div>`,
    opts: ['Both A and R are true, and R is correct explanation of A.', 'Both A and R are true, but R is not correct explanation of A.', 'A is true, but R is false.', 'A is false, but R is true.'], ans: 2,
    sol: R`<p><strong>A is true.</strong> Steady flow means the velocity at each <em>point in space</em> does not change with time. Every particle passing through point P has the same velocity there.</p>
      <p><strong>R is false.</strong> A particle's velocity can change as it moves from point to point. In a narrowing pipe it speeds up, even in perfectly steady flow.</p>`,
    trap: R`"Steady" is about fixed points in space, not about following one particle.`,
  },
  {
    id: 't05-17', src: 't05', qno: 17, topic: 'flow', type: 'ar',
    q: R`<div class="ar"><p><strong>Assertion (A):</strong> The formation of small whirlpool-like regions called 'white water rapids' can be associated with turbulent flow.</p><p><strong>Reason (R):</strong> A fast-flowing stream can become turbulent when it encounters obstacles such as rocks.</p></div>`,
    opts: ['Both A and R are true, and R is the correct explanation of A.', 'Both A and R are true, but R is not correct explanation of A.', 'A is true, but R is false.', 'A is false, but R is true.'], ans: 0,
    sol: R`<p>Rapids are whirlpools and eddies, the signature of turbulence (A true). Turbulence appears when fast flow meets obstacles such as rocks: high speed means high Reynolds number (R true). R is exactly why rapids form, so R explains A.</p>`,
  },
  {
    id: 't05-18', src: 't05', qno: 18, topic: 'flow', type: 'statement',
    q: R`<div class="ar"><p><strong>Statement I:</strong> For a fluid in a steady state, the increase in flow speed at a constriction follows conservation of mass.</p><p><strong>Statement II:</strong> For the model of a plane in a wind tunnel, turbulence occurs at a smaller speed than the required speed for turbulence for an actual plane.</p></div>`,
    opts: ['Both statement I and II are correct.', 'Statement I is correct but statement II is incorrect.', 'Statement I is incorrect but statement II is correct.', 'Both statement I &amp; II are incorrect.'], ans: 1,
    sol: R`<p><strong>I is correct.</strong> \( A_1v_1 = A_2v_2 \) (equation of continuity) is conservation of mass for an incompressible fluid.</p>
      <p><strong>II is incorrect.</strong> Turbulence starts at a critical Reynolds number \( R_e = \rho v d/\eta \approx 2000 \). The model is smaller (smaller d), so it needs a <em>larger</em> speed v to reach the same \( R_e \).</p>`,
  },
  {
    id: 't05-19', src: 't05', qno: 19, topic: 'continuity', type: 'numerical',
    q: R`<p>The cylindrical tube of a spray pump has a cross-section of 8.0 cm², one end of which has 20 fine holes each of area 1 mm². If the liquid flow inside the tube is 1.0 m min⁻¹, the speed of ejection of the liquid through the holes is:</p>`,
    opts: [R`\( \frac23 \) m s⁻¹`, '40 m s⁻¹', '13.33 m s⁻¹', '1 m s⁻¹'], ans: 0,
    sol: R`<ol class="steps">
      <li>Continuity: \( A_\text{tube} v_\text{tube} = n\,a\,v_\text{hole} \).</li>
      <li>\( A = 8\times10^{-4} \text{ m}^2,\ v = \frac{1}{60} \text{ m/s},\ n a = 20 \times 10^{-6} = 2\times10^{-5} \text{ m}^2 \).</li>
      <li>\( v_\text{hole} = \dfrac{8\times10^{-4} \times (1/60)}{2\times10^{-5}} = \dfrac{40}{60} = \dfrac23 \text{ m/s} \).</li></ol>`,
    trap: R`Convert everything first: 1 mm² = 10⁻⁶ m², and 1 m/min = 1/60 m/s. Forgetting the /60 gives 40, which is option 2.`,
  },
  {
    id: 't05-20', src: 't05', qno: 20, topic: 'bernoulli', type: 'concept',
    q: R`<p>The venturi-meter works on:</p>`,
    opts: ["Bernoulli's principle", 'The principle of parallel axes', 'The principle of perpendicular axes', 'Magnus effect'], ans: 0,
    sol: R`<p>A venturimeter measures flow speed from the pressure drop at its throat. Faster flow at the narrow part means lower pressure there (Bernoulli), and continuity links the two speeds.</p>`,
  },
  {
    id: 't05-21', src: 't05', qno: 21, topic: 'bernoulli', type: 'concept', flagged: true,
    q: R`<p>Correct Bernoulli's equation is (symbols have their usual meaning):</p>`,
    opts: [R`\( P + \tfrac12\rho g h + \tfrac12\rho v^2 = \text{constant} \)`, R`\( P + mgh + \tfrac12 m v^2 = \text{constant} \)`, R`\( P + \rho g h + \rho v^2 = \text{constant} \)`, R`\( P + \rho g h + \tfrac12\rho v^2 = \text{constant} \)`], ans: 3,
    sol: R`<p>Every term must be an <em>energy per unit volume</em> (units Pa = J/m³):</p>
      <ul><li>\( P \): pressure energy per volume</li><li>\( \rho g h \): potential energy per volume (that's \( mgh/V \))</li><li>\( \tfrac12\rho v^2 \): kinetic energy per volume (\( \tfrac12mv^2/V \))</li></ul>
      <p>Option 1 has a stray ½ on \( \rho g h \); option 2 mixes energy with pressure (wrong units); option 3 drops the ½ on the KE term.</p>`,
    trap: R`Only the kinetic term has a ½. Remember it as "P + ρgh + ½ρv²" by analogy with \( mgh + \tfrac12mv^2 \).`,
  },
  {
    id: 't05-22', src: 't05', qno: 22, topic: 'continuity', type: 'numerical',
    q: R`<p>An ideal fluid flows (laminar flow) through a pipe of non-uniform diameter. The maximum and minimum diameters of the pipe are 6.4 cm and 3.2 cm, respectively. The ratio of minimum and maximum velocities of fluid in this pipe is:</p>`,
    opts: [R`\( \frac34 \)`, R`\( \frac14 \)`, R`\( \frac{9}{16} \)`, R`\( \frac{81}{256} \)`], ans: 1,
    sol: R`<ol class="steps"><li>\( Av = \) const, so \( v \propto 1/d^2 \).</li>
      <li>Minimum velocity is at the widest part (6.4 cm); maximum is at the narrowest (3.2 cm).</li>
      <li>\( \dfrac{v_\text{min}}{v_\text{max}} = \left(\dfrac{3.2}{6.4}\right)^2 = \dfrac14 \).</li></ol>`,
  },
  {
    id: 't05-23', src: 't05', qno: 23, topic: 'lift', type: 'numerical',
    q: R`<p>A fully loaded aircraft has mass of \( 2\times10^5 \) kg. Its total wing area is 500 m². It is in level flight with a speed of 900 km/h. The fractional increase in the speed of air on the upper surface relative to the lower surface is (density of air = 1 kg m⁻³; g = 10 m s⁻²):</p>`,
    opts: ['0.084', '0.32', '0.064', '0.016'], ans: 2,
    sol: R`<ol class="steps">
      <li>Level flight: lift = weight, so \( \Delta P = \dfrac{mg}{A} = \dfrac{2\times10^6}{500} = 4000 \text{ Pa} \).</li>
      <li>Bernoulli: \( \Delta P = \tfrac12\rho(v_u^2 - v_l^2) = \tfrac12\rho(v_u+v_l)(v_u-v_l) \approx \rho\, v\, \Delta v \), with \( v = 900 \text{ km/h} = 250 \text{ m/s} \).</li>
      <li>\( \dfrac{\Delta v}{v} = \dfrac{\Delta P}{\rho v^2} = \dfrac{4000}{1 \times 250^2} = 0.064 \).</li></ol>`,
    key: R`For a small speed difference: \( \Delta P \approx \rho v\,\Delta v \), so \( \dfrac{\Delta v}{v} = \dfrac{\Delta P}{\rho v^2} \).`,
  },
  {
    id: 't05-24', src: 't05', qno: 24, topic: 'lift', type: 'numerical',
    q: R`<p>In a test experiment on a model aeroplane in a wind tunnel, the flow speeds on the upper and lower surfaces of the wing are 50 m s⁻¹ and 44 m s⁻¹ respectively. The lift force on the wing of area 2 m² is (density of air = 1 kg/m³):</p>`,
    opts: ['464 N', '564 N', '664 N', '764 N'], ans: 1,
    sol: R`<ol class="steps"><li>\( \Delta P = \tfrac12\rho(v_1^2 - v_2^2) = \tfrac12(1)(2500 - 1936) = 282 \text{ Pa} \).</li>
      <li>Lift \( = \Delta P \times A = 282 \times 2 = 564 \text{ N} \).</li></ol>`,
  },
  {
    id: 't05-25', src: 't05', qno: 25, topic: 'continuity', type: 'numerical',
    q: R`<p>Water falls from a tap with an initial velocity of 1.0 m/s. The cross-sectional area of the tap is \( 10^{-4} \) m². Assuming steady flow and taking g = 10 m/s², the cross-sectional area of the stream 0.15 m below the tap is:</p>`,
    opts: ['5.0 × 10⁻⁴ m²', '1.0 × 10⁻⁵ m²', '5.0 × 10⁻⁵ m²', '2.0 × 10⁻⁵ m²'], ans: 2,
    sol: R`<ol class="steps"><li>Speed after falling 0.15 m: \( v^2 = 1^2 + 2(10)(0.15) = 4 \Rightarrow v = 2 \text{ m/s} \).</li>
      <li>Continuity: \( A_2 = \dfrac{A_1v_1}{v_2} = \dfrac{10^{-4}\times1}{2} = 5\times10^{-5} \text{ m}^2 \).</li></ol>`,
    key: R`This is why a falling stream of water narrows: it speeds up, so its area must shrink.`,
  },
  {
    id: 't05-26', src: 't05', qno: 26, topic: 'bernoulli', type: 'numerical',
    q: R`<p>Water flows in a streamline motion through a horizontal pipe of circular cross-section. The difference of pressure between P and Q is 15 N/m². The cross-sectional areas at P and Q are 20 cm² and 10 cm², respectively. The rate of flow of water through the pipe in cm³/s is (density of water = 1000 kg/m³):</p>`,
    fig: `<svg viewBox="0 0 320 110" role="img" aria-label="Horizontal pipe, wide at P, narrow at Q">
      <path d="M10 25 H90 C130 25 130 42 160 42 C190 42 190 25 230 25 H310 V85 H230 C190 85 190 68 160 68 C130 68 130 85 90 85 H10 Z" ${WATER}/>
      <path d="M10 25 H90 C130 25 130 42 160 42 C190 42 190 25 230 25 H310 M10 85 H90 C130 85 130 68 160 68 C190 68 190 85 230 85 H310" ${W}/>
      ${ARW(20, 55, 70, 55, 'var(--water)')}${ARW(250, 55, 300, 55, 'var(--water)')}
      <line x1="60" y1="20" x2="60" y2="90" style="stroke:var(--ink-2);stroke-dasharray:3 3"/><line x1="160" y1="36" x2="160" y2="74" style="stroke:var(--ink-2);stroke-dasharray:3 3"/>
      ${T(55, 14, 'P')}${T(156, 30, 'Q')}${T(30, 104, '20 cm²')}${T(140, 104, '10 cm²')}</svg>`,
    opts: ['400', '100', '200', '300'], ans: 2,
    sol: R`<ol class="steps">
      <li>Continuity: \( 20 v_P = 10 v_Q \Rightarrow v_Q = 2v_P \).</li>
      <li>Bernoulli (horizontal): \( P_P - P_Q = \tfrac12\rho(v_Q^2 - v_P^2) = \tfrac12(1000)(3v_P^2) = 1500\,v_P^2 \).</li>
      <li>\( 1500\,v_P^2 = 15 \Rightarrow v_P = 0.1 \text{ m/s} = 10 \text{ cm/s} \).</li>
      <li>Rate \( Q = A_Pv_P = 20 \times 10 = 200 \text{ cm}^3/\text{s} \).</li></ol>`,
  },
  {
    id: 't05-27', src: 't05', qno: 27, topic: 'bernoulli', type: 'numerical',
    q: R`<p>An ideal fluid flows through a pipe of circular cross-section made of two sections with diameters 2.5 cm and 3.75 cm. The ratio of the kinetic energy per unit volume at the two sections is:</p>`,
    opts: ['9 : 4', '81 : 16', '3 : 2', '1 : 2'], ans: 1,
    sol: R`<ol class="steps"><li>KE per unit volume \( = \tfrac12\rho v^2 \propto v^2 \), and \( v \propto 1/d^2 \), so KE/volume \( \propto 1/d^4 \).</li>
      <li>\( \dfrac{K_1}{K_2} = \left(\dfrac{d_2}{d_1}\right)^4 = \left(\dfrac{3.75}{2.5}\right)^4 = (1.5)^4 = \dfrac{81}{16} \).</li></ol>`,
    trap: R`Two powers stack up here: area gives d², then KE gives v². That makes the 4th power of the diameter ratio.`,
  },
  {
    id: 't05-28', src: 't05', qno: 28, topic: 'lift', type: 'numerical',
    q: R`<p>Wind with a speed of 40 m/s blows horizontally over the roof of a house. The area of the roof is 250 m². The density of air is 1.2 kg/m³. The net force acting on the roof due to the pressure difference is:</p>`,
    opts: ['4.8 × 10⁵ N downward', '2.4 × 10⁵ N upward', '2.4 × 10⁵ N downward', '4.8 × 10⁵ N upward'], ans: 1,
    sol: R`<ol class="steps"><li>Air inside the house is still; air above the roof moves at 40 m/s, so the pressure above is lower.</li>
      <li>\( \Delta P = \tfrac12\rho v^2 = \tfrac12(1.2)(1600) = 960 \text{ Pa} \).</li>
      <li>\( F = \Delta P\cdot A = 960 \times 250 = 2.4\times10^5 \text{ N} \), <strong>upward</strong> (from high pressure inside to low pressure outside).</li></ol>`,
  },
  {
    id: 't05-29', src: 't05', qno: 29, topic: 'torricelli', type: 'numerical',
    q: R`<p>A large tank filled with water has a small hole situated at a depth of 5 m below the free surface of water. The velocity of efflux of water from the hole is (g = 10 m/s²):</p>`,
    opts: ['10 m/s', '20 m/s', '50 m/s', '100 m/s'], ans: 0,
    sol: R`<p>Torricelli: \( v = \sqrt{2gh} = \sqrt{2 \times 10 \times 5} = 10 \text{ m/s} \). Here h is the depth below the <em>free surface</em>.</p>`,
  },
  {
    id: 't05-30', src: 't05', qno: 30, topic: 'torricelli', type: 'concept', flagged: true,
    q: R`<p>A tank of height H is completely filled with water. A small hole is punched in the side wall of the tank at a depth h from the top. The horizontal range of the water jet on the ground is maximum when:</p>`,
    opts: ['h = H/4', 'h = H/2', 'h = 3H/4', 'h = H'], ans: 1,
    sol: R`<ol class="steps">
      <li>Exit speed \( v = \sqrt{2gh} \). The hole is at height \( H - h \) above the ground, so the fall time is \( t = \sqrt{2(H-h)/g} \).</li>
      <li>Range \( R = vt = 2\sqrt{h(H-h)} \).</li>
      <li>The product \( h(H-h) \) is maximum when \( h = H - h \), i.e. \( h = H/2 \). Then \( R_\text{max} = H \).</li></ol>`,
    key: R`Holes at depths h and \( H-h \) give the <em>same</em> range. The maximum range is H, from the hole at the middle.`,
  },
  {
    id: 't05-31', src: 't05', qno: 31, topic: 'torricelli', type: 'concept', flagged: true,
    q: R`<p>A cylindrical tank of cross-sectional area A is filled with water to height H. A hole of area a is made at the bottom. The time taken to completely empty the tank is proportional to:</p>`,
    opts: ['H', R`\( \sqrt{H} \)`, 'H²', R`\( H^{3/2} \)`], ans: 1,
    sol: R`<ol class="steps">
      <li>Level falls as \( -A\dfrac{dh}{dt} = a\sqrt{2gh} \).</li>
      <li>Separate and integrate: \( \displaystyle\int_H^0 \frac{-A\,dh}{a\sqrt{2gh}} = t \Rightarrow t = \frac{A}{a}\sqrt{\frac{2H}{g}} \).</li>
      <li>So \( t \propto \sqrt{H} \).</li></ol>`,
    key: R`Emptying from H to H/2 is <em>faster</em> than from H/2 to 0, because the outflow slows as the level drops.`,
  },
  {
    id: 't05-32', src: 't05', qno: 32, topic: 'lift', type: 'concept', flagged: true,
    q: R`<p>When a spinning ball is thrown, it deviates from its parabolic trajectory. This phenomenon is known as:</p>`,
    opts: ["Pascal's Law", 'Magnus effect', "Torricelli's Law", 'Venturi effect'], ans: 1,
    sol: R`<p>The spin drags air faster past one side of the ball. Faster air means lower pressure (Bernoulli), so the ball feels a sideways force and swerves. This is the <strong>Magnus effect</strong> (swing and spin in cricket, curve in football).</p>`,
  },
  {
    id: 't05-33', src: 't05', qno: 33, topic: 'bernoulli', type: 'numerical',
    q: R`<p>Water flows through a horizontal tube. The difference in height between water columns in vertical tubes is 5 cm and area of cross-sections at A and B are 6 cm² and 3 cm² respectively. The rate of flow will be ____ cm³/s (take g = 10 m/s²):</p>`,
    fig: `<svg viewBox="0 0 320 150" role="img" aria-label="Venturi tube with vertical tubes at A (wide) and B (narrow); water levels differ by 5 cm">
      <path d="M10 80 H110 C140 80 140 95 165 95 C190 95 190 80 220 80 H310 V130 H220 C190 130 190 115 165 115 C140 115 140 130 110 130 H10 Z" ${WATER}/>
      <path d="M10 80 H110 C140 80 140 95 165 95 C190 95 190 80 220 80 H310 M10 130 H110 C140 130 140 115 165 115 C190 115 190 130 220 130 H310" ${W}/>
      <rect x="62" y="22" width="12" height="58" ${WATER}/><rect x="159" y="42" width="12" height="53" ${WATER}/>
      <path d="M62 10 V80 M74 10 V80 M159 10 V95 M171 10 V95" ${W}/>
      <line x1="62" y1="22" x2="74" y2="22" ${SURF}/><line x1="159" y1="42" x2="171" y2="42" ${SURF}/>
      <line x1="80" y1="22" x2="196" y2="22" style="stroke:var(--muted);stroke-dasharray:3 3"/>${ARW(190, 26, 190, 40, 'var(--coral)')}${T(198, 36, '5 cm')}
      ${T(63, 112, 'A')}${T(160, 108, 'B')}${ARW(240, 105, 290, 105, 'var(--water)')}</svg>`,
    opts: [R`\( 100\sqrt3 \)`, R`\( \frac{200}{\sqrt3} \)`, R`\( 200\sqrt6 \)`, R`\( 200\sqrt3 \)`], ans: 3,
    sol: R`<ol class="steps">
      <li>Continuity: \( 6v_A = 3v_B \Rightarrow v_B = 2v_A \).</li>
      <li>Bernoulli + manometer: \( P_A - P_B = \rho g\Delta h = \tfrac12\rho(v_B^2 - v_A^2) \Rightarrow g\Delta h = \tfrac12(3v_A^2) \).</li>
      <li>\( 10 \times 0.05 = 1.5\,v_A^2 \Rightarrow v_A^2 = \tfrac13 \Rightarrow v_A = \tfrac{1}{\sqrt3} \text{ m/s} = \tfrac{100}{\sqrt3} \text{ cm/s} \).</li>
      <li>Rate \( = 6 \times \dfrac{100}{\sqrt3} = \dfrac{600}{\sqrt3} = 200\sqrt3 \text{ cm}^3/\text{s} \).</li></ol>`,
  },
  {
    id: 't05-34', src: 't05', qno: 34, topic: 'torricelli', type: 'numerical',
    q: R`<p>A cylindrical vessel of height 105 cm and 40 cm radius is placed on a solid block of exactly the same height. If a small hole is made at 70 cm below the top water level, the horizontal range of water falling on the ground in the beginning is ____ cm.</p>`,
    opts: [R`\( 120\sqrt2 \)`, R`\( 140\sqrt2 \)`, R`\( 140\sqrt3 \)`, R`\( 120\sqrt3 \)`], ans: 1,
    sol: R`<ol class="steps">
      <li>Vessel is full: the hole is 70 cm below the surface, so it is \( 105 - 70 = 35 \) cm above the vessel's base.</li>
      <li>Height of hole above the ground \( = 35 + 105 = 140 \) cm.</li>
      <li>\( R = 2\sqrt{(\text{depth})(\text{height above ground})} = 2\sqrt{70 \times 140} = 2 \times 70\sqrt2 = 140\sqrt2 \text{ cm} \).</li></ol>`,
    key: R`General shortcut: \( R = 2\sqrt{h_\text{depth}\cdot h_\text{fall}} \), the same as the \( 2\sqrt{h(H-h)} \) formula when the tank sits on the ground.`,
  },
  {
    id: 't05-35', src: 't05', qno: 35, topic: 'torricelli', type: 'numerical',
    q: R`<p>Consider a completely full cylindrical water tank of height 1.6 m and cross-sectional area 0.5 m². It has a small hole in its side at a height 90 cm from the bottom. Assume the cross-sectional area of the hole to be negligibly small compared to that of the tank. If a load of 100 kg is applied at the top surface of the water in the tank, then the velocity of water coming out at the instant when the hole is opened is (g = 10 m/s²):</p>`,
    opts: [R`\( 2\sqrt2 \) m s⁻¹`, '5 m s⁻¹', R`\( 3\sqrt2 \) m s⁻¹`, '4 m s⁻¹'], ans: 2,
    sol: R`<ol class="steps">
      <li>Depth of the hole: \( h = 1.6 - 0.9 = 0.7 \text{ m} \).</li>
      <li>Extra pressure from the load: \( \Delta P = \dfrac{mg}{A} = \dfrac{1000}{0.5} = 2000 \text{ Pa} \).</li>
      <li>Bernoulli: \( \tfrac12\rho v^2 = \rho g h + \Delta P \Rightarrow v^2 = 2gh + \dfrac{2\Delta P}{\rho} = 14 + 4 = 18 \).</li>
      <li>\( v = 3\sqrt2 \text{ m/s} \).</li></ol>`,
  },
  {
    id: 't05-36', src: 't05', qno: 36, topic: 'buoyancy', type: 'graph',
    q: R`<p>A solid body is gradually immersed in a liquid. Which graph correctly represents the variation of buoyant force \( F_B \) with submerged volume V?</p>`,
    opts: [GRAPH('M16 30 H112', 'F_B', 'V'), GRAPH('M16 70 L110 14', 'F_B', 'V'), GRAPH('M16 14 L110 70', 'F_B', 'V'), GRAPH('M16 70 Q80 68 110 12', 'F_B', 'V')], ans: 1,
    sol: R`<p>\( F_B = \rho_\text{liquid}\, g\, V_\text{sub} \). Density and g are constant, so \( F_B \propto V \): a straight line through the origin (graph 2).</p>`,
  },
  {
    id: 't05-37', src: 't05', qno: 37, topic: 'torricelli', type: 'graph',
    q: R`<p>A tank is filled with liquid of density ρ up to height H and has a small hole at height h above the bottom. Which graph correctly represents the speed of efflux v with height h above the bottom?</p>`,
    opts: [GRAPH('M16 70 L110 30', 'v', 'h', T(100, 82, 'H', 'font-size="10"')), GRAPH('M16 14 L104 70', 'v', 'h', T(98, 82, 'H', 'font-size="10"')), GRAPH('M16 16 Q70 18 104 70', 'v', 'h', T(98, 82, 'H', 'font-size="10"')), GRAPH('M16 70 Q80 68 110 14', 'v', 'h', T(100, 82, 'H', 'font-size="10"'))], ans: 2,
    sol: R`<ol class="steps"><li>The depth below the surface is \( H - h \), so \( v = \sqrt{2g(H-h)} \).</li>
      <li>At h = 0, v is maximum (\( \sqrt{2gH} \)); at h = H, v = 0. So v decreases.</li>
      <li>It is a square-root curve, not a straight line: \( v^2 = 2g(H-h) \) is a sideways parabola. It falls slowly at first and steeply near h = H, which is graph 3.</li></ol>`,
  },
  {
    id: 't05-38', src: 't05', qno: 38, topic: 'bernoulli', type: 'match', flagged: true,
    q: R`<p>Match Column-I with Column-II:</p>
      <div class="table-wrap"><table class="mtc"><tr><th>Column-I</th><th>Column-II</th></tr>
      <tr><td>A. Person standing near a fast-moving train is pulled towards the train</td><td>P. Pressure decreases where the speed of the flowing fluid increases</td></tr>
      <tr><td>B. An aeroplane wing experiences an upward force while moving through air</td><td>Q. The buoyant force equals weight of displaced fluid when the body is in equilibrium</td></tr>
      <tr><td>C. A ship made of iron floats on water</td><td>R. Difference in pressure on opposite sides of the body is produced because of different fluid speeds</td></tr>
      <tr><td>D. A liquid jet emerging from a small opening becomes narrower as it moves away from the opening</td><td>S. For steady incompressible flow, AV = constant</td></tr></table></div>`,
    opts: ['A-P, B-Q, C-R, D-S', 'A-P, B-R, C-Q, D-S', 'A-S, B-Q, C-R, D-P', 'A-Q, B-P, C-R, D-S'], ans: 1,
    sol: R`<ul><li><strong>A → P:</strong> air between the person and the train moves fast, so the pressure there drops and the higher pressure behind pushes the person in.</li>
      <li><strong>B → R:</strong> air moves faster over the wing than under it. The pressure difference across the wing gives lift.</li>
      <li><strong>C → Q:</strong> the hollow hull displaces water equal to the ship's weight (Archimedes, floating).</li>
      <li><strong>D → S:</strong> the falling jet speeds up, so by continuity its area shrinks.</li></ul>`,
    trap: R`B and A both involve Bernoulli. "Pressure <em>difference on opposite sides</em> of a body" is the wording for lift (R). P is the general statement and fits the train.`,
  },
  {
    id: 't05-39', src: 't05', qno: 39, topic: 'bernoulli', type: 'concept',
    q: R`<p>A vertical pipe with its lower end open is fixed in a horizontal stream of water flowing with uniform speed v. The open end of the pipe faces directly against the direction of flow, so that water enters the pipe, comes to rest at the opening and rises inside. The water overflows from the top of the pipe and emerges as a vertical jet, rising to a maximum height h above the top of the pipe. Assuming steady, incompressible, non-viscous flow, which of the following correctly gives h in terms of v and g?</p>`,
    fig: `<svg viewBox="0 0 320 130" role="img" aria-label="L-shaped pipe facing a horizontal stream; a vertical jet rises h above it">
      <rect x="10" y="50" width="300" height="70" ${WATER}/><line x1="10" y1="50" x2="310" y2="50" ${SURF}/>
      <path d="M190 18 V92 H150 M202 18 V104 H150" ${W}/>
      <path d="M196 16 C190 4 184 2 180 12 M196 16 C202 4 208 2 212 12" style="fill:none;stroke:var(--water);stroke-width:2;stroke-dasharray:3 3"/>
      ${ARW(30, 80, 80, 80, 'var(--water)')}${ARW(30, 95, 80, 95, 'var(--water)')}${T(40, 70, 'v')}
      ${ARW(230, 18, 230, 4, 'var(--muted)')}${T(238, 14, 'h')}</svg>`,
    opts: [R`\( h = \frac{v}{g} \)`, R`\( h = \frac{v^2}{4g} \)`, R`\( h = \frac{v^2}{2g} \)`, R`\( h = \frac{2v^2}{g} \)`], ans: 2,
    sol: R`<ol class="steps">
      <li>Apply Bernoulli between a point far upstream (speed v, pressure P) and the mouth of the pipe, where the water is brought to rest (stagnation point).</li>
      <li>\( P + \tfrac12\rho v^2 = P_\text{mouth} \): the pressure at the mouth rises by \( \tfrac12\rho v^2 \).</li>
      <li>This extra pressure supports (or launches) a water column of height h where \( \rho g h = \tfrac12\rho v^2 \Rightarrow h = \dfrac{v^2}{2g} \).</li></ol>`,
    key: R`Kinetic energy turns into height, just like a ball thrown up at speed v: \( h = v^2/2g \).`,
  },
  {
    id: 't05-40', src: 't05', qno: 40, topic: 'torricelli', type: 'numerical',
    q: R`<p>A tank containing a liquid of density ρ has two identical small holes, each of cross-sectional area a, on opposite vertical sides. The holes are at different heights and the vertical separation between them is h (the upper hole is at a higher level). The tank is kept at rest on a smooth horizontal surface. The liquid issues out horizontally from both holes. What is the magnitude of the horizontal external force that must be applied on the tank to keep it in equilibrium? (Assume steady flow, and take the atmospheric pressure to be the same on both sides.)</p>`,
    fig: `<svg viewBox="0 0 300 150" role="img" aria-label="Tank with an upper hole on the left wall and a lower hole on the right wall, separated by h">
      <rect x="80" y="30" width="140" height="100" ${WATER}/><line x1="80" y1="30" x2="220" y2="30" ${SURF}/>
      <path d="M80 14 V130 H220 V14" ${W}/><line x1="60" y1="134" x2="240" y2="134" style="stroke:var(--line-2);stroke-width:3"/>
      ${ARW(80, 58, 40, 58, 'var(--water)')}${T(30, 50, 'v₁')}${ARW(220, 108, 262, 108, 'var(--water)')}${T(258, 100, 'v₂')}
      <line x1="120" y1="58" x2="120" y2="108" style="stroke:var(--muted);stroke-dasharray:3 3"/>${T(126, 86, 'h')}</svg>`,
    opts: ['ρgha', R`\( \frac{2gh}{\rho a} \)`, '2ρagh', R`\( \frac{\rho g h}{a} \)`], ans: 2,
    sol: R`<ol class="steps">
      <li>A jet of speed v from a hole of area a carries momentum away at the rate \( \rho a v \cdot v = \rho a v^2 \). That is the reaction force on the tank.</li>
      <li>If the upper hole is at depth y: \( v_1^2 = 2gy \), and \( v_2^2 = 2g(y+h) \).</li>
      <li>The jets point in opposite directions, so the net force on the tank is \( \rho a(v_2^2 - v_1^2) = \rho a\cdot 2gh \).</li>
      <li>The external force needed to hold it is \( 2\rho a g h \).</li></ol>`,
  },
  {
    id: 't05-41', src: 't05', qno: 41, topic: 'bernoulli', type: 'concept',
    q: R`<p>A fluid is in streamline flow across a horizontal pipe of variable area of cross section. Which statement is correct?</p>`,
    opts: ['Velocity is maximum at narrowest part and pressure is maximum at widest part of the pipe', 'Velocity and pressure both maximum at narrowest part of the pipe', 'Velocity and pressure both maximum at widest part of the pipe', 'Velocity minimum at narrowest part and pressure minimum at widest part of the pipe'], ans: 0,
    sol: R`<p>Continuity: narrow means fast. Bernoulli (horizontal, \( P + \tfrac12\rho v^2 \) = const): fast means low pressure. So velocity is maximum at the narrowest part, and pressure is maximum where velocity is minimum, at the widest part.</p>`,
  },
  {
    id: 't05-42', src: 't05', qno: 42, topic: 'bernoulli', type: 'concept', flagged: true,
    q: R`<p>Bernoulli's equation is a consequence of conservation of:</p>`,
    opts: ['Energy', 'Linear momentum', 'Angular momentum', 'Mass'], ans: 0,
    sol: R`<p>Bernoulli's equation comes from the work–energy theorem applied to a fluid element. Work done by pressure forces = change in KE + PE. Each term is an energy per unit volume, so it is conservation of <strong>energy</strong>.</p>
      <p class="small muted">Conservation of <em>mass</em> gives the equation of continuity (\( Av \) = const), the other half of fluid-flow problems.</p>`,
    trap: R`Continuity → mass. Bernoulli → energy. Keep the pair straight.`,
  },
  {
    id: 't05-43', src: 't05', qno: 43, topic: 'bernoulli', type: 'concept',
    q: R`<p>Water flows in a horizontal pipe whose one end is closed with a valve. The reading of the pressure gauge attached to the pipe is \( P_1 \). The reading of the pressure gauge falls to \( P_2 \) when the valve is opened. The speed of water flowing in the pipe is proportional to:</p>`,
    opts: [R`\( (P_1 - P_2)^2 \)`, R`\( \sqrt{P_1 - P_2} \)`, R`\( P_1 - P_2 \)`, R`\( (P_1 - P_2)^4 \)`], ans: 1,
    sol: R`<p>With the valve closed the water is at rest, so the gauge reads \( P_1 \). Once it flows: \( P_2 + \tfrac12\rho v^2 = P_1 \Rightarrow v = \sqrt{\dfrac{2(P_1 - P_2)}{\rho}} \propto \sqrt{P_1 - P_2} \).</p>`,
  },
  {
    id: 't05-44', src: 't05', qno: 44, topic: 'continuity', type: 'numerical',
    q: R`<p>An incompressible liquid flows through a horizontal tube L, M, N as shown. The cross-section areas of L, M, N are 2A, \( \frac{A}{2} \), A respectively; velocity of liquid in L, M, N are 4 m/s, 4 m/s, V m/s respectively. Then the velocity V of the liquid through the tube N is:</p>`,
    fig: `<svg viewBox="0 0 320 130" role="img" aria-label="Pipe L of area 2A splitting into branch M (area A/2) and branch N (area A)">
      <path d="M20 45 H140 L230 15 L238 30 L160 60 L238 90 L230 108 L140 80 H20 Z" ${WATER}/>
      <path d="M20 45 H140 L230 15 M20 80 H140 L230 108 M238 30 L160 60 L238 90" ${W}/>
      ${ARW(40, 63, 90, 63, 'var(--water)')}${T(50, 56, '4 m/s')}${T(26, 100, 'L: 2A')}
      ${ARW(180, 38, 218, 25, 'var(--water)')}${T(244, 22, 'M: A/2, 4 m/s')}
      ${ARW(180, 86, 218, 98, 'var(--water)')}${T(244, 106, 'N: A, V = ?')}</svg>`,
    opts: ['1 m s⁻¹', '2 m s⁻¹', '4.5 m s⁻¹', '6 m s⁻¹'], ans: 3,
    sol: R`<ol class="steps"><li>Volume flowing in = volume flowing out: \( A_Lv_L = A_Mv_M + A_Nv_N \).</li>
      <li>\( 2A(4) = \tfrac{A}{2}(4) + A\cdot V \Rightarrow 8 = 2 + V \Rightarrow V = 6 \text{ m/s} \).</li></ol>`,
  },
  {
    id: 't05-45', src: 't05', qno: 45, topic: 'buoyancy', type: 'numerical',
    q: R`<p>Two non-mixing liquids of densities ρ and nρ (n &gt; 1) are put in a container. The height of each liquid is h. A solid cylinder of length L and density d is put in this container. The cylinder floats with its axis vertical and length pL (p &lt; 1) in the denser liquid. The density d is equal to:</p>`,
    opts: [R`\( \{2 + (n-1)p\}\rho \)`, R`\( \{1 + (n-1)p\}\rho \)`, R`\( \{1 + (n+1)p\}\rho \)`, R`\( \{2 + (n+1)p\}\rho \)`], ans: 1,
    sol: R`<ol class="steps"><li>Length pL is in the denser liquid (nρ); the remaining \( (1-p)L \) is in the lighter liquid (ρ).</li>
      <li>Weight = total buoyancy (cross-section A cancels): \( dL = n\rho\,pL + \rho(1-p)L \).</li>
      <li>\( d = \rho(np + 1 - p) = \{1 + (n-1)p\}\rho \).</li></ol>`,
  }
  );
})();
