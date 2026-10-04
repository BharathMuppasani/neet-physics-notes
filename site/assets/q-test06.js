/* Narayana NEET Jr Star — Module Test-06 (03.10.2026), Physics Q1–45
   Mechanical Properties of Fluids, part 2: viscosity, Stokes, Reynolds, surface tension, capillarity.
   The paper numbers two questions "20"; the second one is stored as qno '20b'.
   `flagged: true` = the question carries a ✗ mark on the photographed paper. */
(function () {
  const R = String.raw;
  window.QBANK = window.QBANK || [];
  const W = 'style="fill:none;stroke:var(--ink-2);stroke-width:2;stroke-linejoin:round"';
  const WATER = 'style="fill:var(--water-soft);stroke:none"';
  const T = (x, y, s, o = '') => `<text x="${x}" y="${y}" font-size="12" style="fill:var(--ink-2);font-family:var(--f-body)" ${o}>${s}</text>`;
  const ARW = (x1, y1, x2, y2, c = 'var(--coral)') => {
    const a = Math.atan2(y2 - y1, x2 - x1), h = 8;
    const p1 = [x2 - h * Math.cos(a - .45), y2 - h * Math.sin(a - .45)], p2 = [x2 - h * Math.cos(a + .45), y2 - h * Math.sin(a + .45)];
    return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" style="stroke:${c};stroke-width:2"/><polygon points="${x2},${y2} ${p1} ${p2}" style="fill:${c}"/>`;
  };
  const ST_OPTS = ['Both statements are correct', 'Statement 1 correct but Statement 2 is not correct', 'Statement 1 not correct but Statement 2 is correct', 'Both statements are incorrect'];

  QBANK.push(
  {
    id: 't06-01', src: 't06', qno: 1, topic: 'viscosity', type: 'numerical',
    q: R`<p>A cubical block of side 'a' and density 'ρ' slides over a fixed inclined plane with constant velocity v. There is a thin film of viscous fluid of thickness 't' between the plane and the block. Then the coefficient of viscosity of the thin film will be:</p>`,
    fig: `<svg viewBox="0 0 260 130" role="img" aria-label="Cube sliding down an incline of angle theta on a thin film">
      <path d="M20 115 H230 V20 Z" style="fill:var(--surface-2);stroke:var(--ink-2);stroke-width:2"/>
      <g transform="translate(120 65) rotate(-24.3)"><rect x="-16" y="-31" width="30" height="30" style="fill:var(--amber-soft);stroke:var(--amber);stroke-width:1.5"/><rect x="-16" y="-2" width="30" height="3" style="fill:var(--water)"/></g>
      ${T(48, 110, 'θ')}${T(150, 50, 'film t', 'font-size="11"')}</svg>`,
    opts: [R`\( \eta = \dfrac{\rho a g t\sin\theta}{v} \)`, R`\( \dfrac{\rho g t \sin\theta}{a v} \)`, R`\( \dfrac{v}{\rho g t\sin\theta} \)`, 'None of these'], ans: 0,
    sol: R`<ol class="steps">
      <li>Constant velocity means the net force is zero, so the viscous drag balances the component of weight down the slope.</li>
      <li>Viscous force (Newton's law of viscosity): \( F = \eta A \dfrac{v}{t} = \eta a^2 \dfrac{v}{t} \).</li>
      <li>\( \eta a^2 \dfrac{v}{t} = mg\sin\theta = \rho a^3 g\sin\theta \Rightarrow \eta = \dfrac{\rho a g t \sin\theta}{v} \).</li></ol>`,
  },
  {
    id: 't06-02', src: 't06', qno: 2, topic: 'stokes', type: 'concept',
    q: R`<p>Spherical balls of radius R are falling in a viscous fluid of viscosity η with a velocity v. The retarding viscous force acting on the spherical ball is:</p>`,
    opts: ['directly proportional to radius R but inversely proportional to velocity v', 'directly proportional to both radius R and velocity v', 'inversely proportional to both radius R and velocity v', 'inversely proportional to radius R but directly proportional to velocity v'], ans: 1,
    sol: R`<p>Stokes' law: \( F = 6\pi\eta R v \). F is directly proportional to both R and v (and to η).</p>`,
  },
  {
    id: 't06-03', src: 't06', qno: 3, topic: 'stokes', type: 'numerical',
    q: R`<p>The terminal speed of a sphere of gold (density = 19.5 kg/m³) is 0.2 m/s in a viscous liquid (density = 1.5 kg/m³). Find the terminal speed of a sphere of silver (density = 10.5 kg/m³) of the same size in the same liquid.</p>`,
    opts: ['0.4 m/s', '0.133 m/s', '0.1 m/s', '0.2 m/s'], ans: 2,
    sol: R`<ol class="steps"><li>\( v_t = \dfrac{2r^2(\rho - \sigma)g}{9\eta} \). Same r, same liquid, so \( v_t \propto (\rho - \sigma) \).</li>
      <li>\( \dfrac{v_\text{Ag}}{v_\text{Au}} = \dfrac{10.5 - 1.5}{19.5 - 1.5} = \dfrac{9}{18} = \dfrac12 \).</li>
      <li>\( v_\text{Ag} = 0.2 \times \tfrac12 = 0.1 \text{ m/s} \).</li></ol>`,
    trap: R`Use the <em>difference</em> \( \rho - \sigma \), not the ratio of densities. Using 10.5/19.5 gives a wrong value.`,
  },
  {
    id: 't06-04', src: 't06', qno: 4, topic: 'surface-tension', type: 'concept',
    q: R`<p>A thin metal disc of radius r floats on a water surface and bends the surface downwards along the perimeter, making an angle θ with the vertical edge of the disc. If the disc displaces a weight of water W and the surface tension of water is T, then the weight of the metal disc is:</p>`,
    fig: `<svg viewBox="0 0 260 110" role="img" aria-label="Disc floating in a dip of the water surface; surface tension pulls along the surface at angle theta to the vertical">
      <rect x="10" y="50" width="240" height="55" ${WATER}/>
      <path d="M10 50 H70 Q90 50 95 70 H165 Q170 50 190 50 H250" style="fill:var(--surface);stroke:var(--water);stroke-width:1.5"/>
      <rect x="95" y="66" width="70" height="6" style="fill:var(--ink-2)"/>
      ${ARW(96, 68, 84, 40)}${ARW(164, 68, 176, 40)}${T(64, 36, 'T')}${T(182, 36, 'T')}${T(102, 92, 'buoyancy W', 'font-size="11"')}</svg>`,
    opts: [R`\( 2\pi rT + W \)`, R`\( 2\pi rT\cos\theta - W \)`, R`\( 2\pi rT\cos\theta + W \)`, R`\( W - 2\pi rT\cos\theta \)`], ans: 2,
    sol: R`<ol class="steps">
      <li>Two upward forces hold the disc up: buoyancy W (weight of water displaced) and surface tension acting all along the rim.</li>
      <li>Surface-tension force = T × length of contact = \( T(2\pi r) \), directed along the bent surface at angle θ to the vertical. Its vertical part is \( 2\pi r T\cos\theta \).</li>
      <li>Equilibrium: weight \( = W + 2\pi r T\cos\theta \).</li></ol>`,
  },
  {
    id: 't06-05', src: 't06', qno: 5, topic: 'surface-tension', type: 'numerical',
    q: R`<p>A square frame of side L is dipped in a liquid. On taking it out, a membrane is formed. If the surface tension of the liquid is T, the force acting on the frame will be:</p>`,
    opts: ['2TL', '4TL', '8TL', '10TL'], ans: 2,
    sol: R`<ol class="steps"><li>Perimeter of the frame = 4L.</li>
      <li>A film has <strong>two</strong> surfaces (front and back), and each pulls on the whole perimeter.</li>
      <li>\( F = T \times 2 \times 4L = 8TL \).</li></ol>`,
    trap: R`4TL forgets the second surface of the film. Any soap film or membrane has two surfaces.`,
  },
  {
    id: 't06-06', src: 't06', qno: 6, topic: 'contact-angle', type: 'concept',
    q: R`<p>A liquid does not wet the sides of a solid, if the angle of contact is:</p>`,
    opts: ['Zero', 'Obtuse (more than 90°)', 'Acute (less than 90°)', '90°'], ans: 1,
    sol: R`<p>When cohesion beats adhesion, the liquid pulls into itself, beads up, and the contact angle is <strong>obtuse</strong> (e.g. mercury on glass ≈ 140°). Acute angles mean wetting (water on clean glass ≈ 0°).</p>`,
  },
  {
    id: 't06-07', src: 't06', qno: 7, topic: 'surface-energy', type: 'concept', flagged: true,
    q: R`<p>Two droplets merge with each other and form a large droplet. In this process:</p>`,
    opts: ['Energy is liberated', 'Energy is absorbed', 'Neither liberated nor absorbed', 'Some mass is converted into energy'], ans: 0,
    sol: R`<ol class="steps">
      <li>The volume is conserved but the total surface area <em>decreases</em> (one big sphere has less area than two small ones of the same total volume).</li>
      <li>Surface energy = T × area, so surface energy drops.</li>
      <li>The difference is <strong>released</strong>, usually as heat, slightly warming the drop.</li></ol>`,
    trap: R`"Mass converted into energy" is nuclear physics, not surface tension. Merging drops releases energy; splitting a drop needs energy.`,
  },
  {
    id: 't06-08', src: 't06', qno: 8, topic: 'contact-angle', type: 'concept',
    q: R`<p>The liquid meniscus in a capillary tube will be convex, if the angle of contact is:</p>`,
    opts: ['Greater than 90°', 'Less than 90°', 'Equal to 90°', 'Equal to 0°'], ans: 0,
    sol: R`<p>θ > 90° (non-wetting, like mercury in glass) gives a convex meniscus and a capillary <em>fall</em>. θ &lt; 90° gives concave and rise; θ = 90° gives flat and no rise.</p>`,
  },
  {
    id: 't06-09', src: 't06', qno: 9, topic: 'capillarity', type: 'numerical',
    q: R`<p>Water rises in a vertical capillary tube up to a height of 2.0 cm. If the tube is inclined at an angle of 60° with the vertical, then up to what length the water will rise in the tube?</p>`,
    opts: ['2.0 cm', '4.0 cm', R`\( \frac{4}{\sqrt3} \) cm`, R`\( 2\sqrt2 \) cm`], ans: 1,
    sol: R`<ol class="steps"><li>The <em>vertical height</em> h is fixed by \( h = \dfrac{2T\cos\theta}{r\rho g} \). Tilting doesn't change it.</li>
      <li>Length along a tube tilted at α to the vertical: \( \ell = \dfrac{h}{\cos\alpha} = \dfrac{2}{\cos60^\circ} = 4 \text{ cm} \).</li></ol>`,
    trap: R`Read the angle carefully. "With the vertical" → divide by cos α. If it were "with the horizontal", divide by sin.`,
  },
  {
    id: 't06-10', src: 't06', qno: 10, topic: 'capillarity', type: 'concept',
    q: R`<p>In a capillary tube experiment, a vertical 30 cm long capillary tube is dipped in water. The water rises up to a height of 10 cm due to capillary action. If this experiment is conducted in a freely falling elevator, the length of the water column becomes:</p>`,
    opts: ['10 cm', '20 cm', '30 cm', 'zero'], ans: 2,
    sol: R`<p>\( h = \dfrac{2T\cos\theta}{r\rho g_\text{eff}} \). In free fall \( g_\text{eff} = 0 \), so nothing limits the rise and water fills the <strong>entire tube</strong>: 30 cm. It doesn't spill out, for the same reason as in Q14.</p>`,
  },
  {
    id: 't06-11', src: 't06', qno: 11, topic: 'capillarity', type: 'numerical',
    q: R`<p>Radius of a capillary is \( 2\times10^{-3} \) m. A liquid of weight \( 6.28\times10^{-4} \) N may remain in the capillary; then the surface tension of the liquid will be:</p>`,
    opts: ['5 × 10⁻³ N/m', '5 × 10⁻² N/m', '5 N/m', '50 N/m'], ans: 1,
    sol: R`<ol class="steps"><li>The column is held up by surface tension around the inner circumference: \( W = 2\pi r T \) (taking θ = 0).</li>
      <li>\( T = \dfrac{W}{2\pi r} = \dfrac{6.28\times10^{-4}}{2\pi \times 2\times10^{-3}} = \dfrac{6.28\times10^{-4}}{1.256\times10^{-2}} = 5\times10^{-2} \text{ N/m} \).</li></ol>`,
  },
  {
    id: 't06-12', src: 't06', qno: 12, topic: 'viscosity', type: 'multi',
    q: R`<p>Choose the <strong>incorrect</strong> statement:</p>`,
    opts: ['With the rise in temperature of gas, viscosity decreases.', 'Viscosity of liquid increases with increase in pressure but in case of water, viscosity decreases with rise in pressure.', 'Viscosity of liquid is about 100 times greater than that of gases.', 'Viscosity of gases is independent of pressure.'], ans: 0,
    sol: R`<p>Gas viscosity <strong>increases</strong> with temperature: faster molecules carry more momentum between layers. Liquid viscosity is the one that decreases with temperature (warm honey flows easily). The other three are standard textbook facts, so option 1 is the incorrect one.</p>`,
    trap: R`Liquids: T↑ → η↓. Gases: T↑ → η↑. They behave oppositely.`,
  },
  {
    id: 't06-13', src: 't06', qno: 13, topic: 'stokes', type: 'concept',
    q: R`<p>The viscous force acting on a solid ball of surface area A moving with terminal velocity v is proportional to:</p>`,
    opts: ['A²', R`\( A^{1/2} \)`, 'v²', R`\( v^{1/2} \)`], ans: 1,
    sol: R`<p>\( F = 6\pi\eta r v \). Surface area \( A = 4\pi r^2 \), so \( r \propto A^{1/2} \) and \( F \propto A^{1/2} \) (and \( F \propto v \), which isn't offered as v¹).</p>`,
  },
  {
    id: 't06-14', src: 't06', qno: 14, topic: 'capillarity', type: 'concept',
    q: R`<p>When a capillary tube is dipped in a liquid, the liquid rises up to a height h in the tube. The free liquid surface inside the tube is hemispherical in shape. The tube is now pushed down so that the height of the tube outside the liquid is less than h.</p>`,
    opts: ['The liquid will ooze out of the tube slowly', 'The liquid will come out of the tube like in a small fountain', 'The liquid will fill the tube but not come out of its upper end', 'None of these'], ans: 2,
    sol: R`<ol class="steps"><li>The rise satisfies \( hR = \dfrac{2T}{\rho g} \), where R is the radius of curvature of the meniscus.</li>
      <li>When the tube is shorter than h, the liquid reaches the top and the meniscus simply flattens (R increases) so that \( h'R' = hR \).</li>
      <li>Nothing pushes the liquid out, so there is <strong>no overflow</strong>. (Otherwise we'd have a perpetual-motion fountain!)</li></ol>`,
  },
  {
    id: 't06-15', src: 't06', qno: 15, topic: 'surface-energy', type: 'numerical',
    q: R`<p>Two water drops each of radius r coalesce to form a bigger drop. If T is the surface tension, the surface energy released in this process is:</p>`,
    opts: [R`\( 4\pi r^2T\left[2 - 2^{2/3}\right] \)`, R`\( 4\pi r^2T\left[2 - 2^{1/3}\right] \)`, R`\( 4\pi r^2T\left[1 + \sqrt2\right] \)`, R`\( 4\pi r^2T\left[\sqrt2 - 1\right] \)`], ans: 0,
    sol: R`<ol class="steps"><li>Volume conserved: \( \tfrac43\pi R^3 = 2\cdot\tfrac43\pi r^3 \Rightarrow R = 2^{1/3}r \).</li>
      <li>Area before \( = 2(4\pi r^2) \); area after \( = 4\pi R^2 = 4\pi r^2\cdot 2^{2/3} \).</li>
      <li>Energy released \( = T\,\Delta A = 4\pi r^2 T\,(2 - 2^{2/3}) \).</li></ol>`,
    key: R`n drops merging: \( E = 4\pi r^2 T\,(n - n^{2/3}) = 4\pi R^2 T\,(n^{1/3} - 1) \).`,
  },
  {
    id: 't06-16', src: 't06', qno: 16, topic: 'capillarity', type: 'concept', flagged: true,
    q: R`<p>The capillary rise of water in a tube depends on:</p>`,
    opts: ['the outer radius of the tube', 'the inner radius of the tube', 'the mass of the tube', 'None of these'], ans: 1,
    sol: R`<p>\( h = \dfrac{2T\cos\theta}{r\rho g} \). Here r is the radius of the bore, the <strong>inner</strong> radius where the liquid touches the glass. The tube's wall thickness, outer radius and mass play no part.</p>`,
  },
  {
    id: 't06-17', src: 't06', qno: 17, topic: 'drops-bubbles', type: 'ar',
    q: R`<div class="ar"><p><strong>Assertion:</strong> A large soap bubble expands while a small bubble shrinks, when they are connected to each other by a capillary tube.</p><p><strong>Reason:</strong> The excess pressure inside a bubble (or drop) is inversely proportional to the radius.</p></div>`,
    opts: ['Both Assertion and Reason are correct and Reason is the correct explanation for Assertion', 'Both Assertion and Reason are correct but Reason is not the correct explanation for Assertion', 'Assertion is correct but Reason is incorrect', 'Both Assertion and Reason are incorrect'], ans: 0,
    sol: R`<p>Excess pressure \( = 4T/r \): the <em>smaller</em> bubble has the <em>higher</em> pressure. When connected, air flows from small to large, so the small one shrinks further and the large one grows. R is exactly the reason, so option 1.</p>`,
  },
  {
    id: 't06-18', src: 't06', qno: 18, topic: 'drops-bubbles', type: 'numerical',
    q: R`<p>Two soap bubbles A and B are kept in a closed chamber where the air is maintained at pressure 8 N/m². The radii of bubbles A and B are 2 cm and 4 cm, respectively. Surface tension of the soap-water used to make bubbles is 0.04 N/m. Find the ratio \( n_B/n_A \), where \( n_A \) and \( n_B \) are the number of moles of air in bubbles A and B, respectively. [Neglect the effect of gravity.]</p>`,
    opts: ['2', '9', '8', '6'], ans: 3,
    sol: R`<ol class="steps">
      <li>Inside pressure of a soap bubble: \( P = P_0 + \dfrac{4T}{r} \).</li>
      <li>A: \( 8 + \dfrac{4(0.04)}{0.02} = 8 + 8 = 16 \text{ N/m}^2 \). B: \( 8 + \dfrac{0.16}{0.04} = 12 \text{ N/m}^2 \).</li>
      <li>\( n = \dfrac{PV}{RT} \), same temperature: \( \dfrac{n_B}{n_A} = \dfrac{P_B r_B^3}{P_A r_A^3} = \dfrac{12 \times 64}{16 \times 8} = 6 \).</li></ol>`,
  },
  {
    id: 't06-19', src: 't06', qno: 19, topic: 'drops-bubbles', type: 'concept',
    q: R`<p>A glass tube of uniform internal radius r has a valve separating the two identical ends. Initially, the valve is in a tightly closed position. End 1 has a hemispherical soap bubble of radius r. End 2 has a sub-hemispherical soap bubble (more than that for a hemispherical bubble) as shown. Just after opening the valve:</p>`,
    fig: `<svg viewBox="0 0 280 120" role="img" aria-label="Tube with a valve on top; end 2 on the left has a shallow bubble, end 1 on the right has a hemispherical bubble">
      <path d="M40 95 V30 H240 V95 M56 95 V46 H224 V95" ${W}/>
      <line x1="140" y1="18" x2="140" y2="46" style="stroke:var(--ink);stroke-width:3"/><line x1="128" y1="18" x2="152" y2="18" style="stroke:var(--ink);stroke-width:3"/>
      <path d="M40 95 Q48 104 56 95" style="fill:var(--plum-soft);stroke:var(--plum);stroke-width:1.5"/>
      <path d="M224 95 A8 8 0 0 0 240 95" style="fill:var(--plum-soft);stroke:var(--plum);stroke-width:1.5"/>
      ${T(26, 104, '2')}${T(248, 104, '1')}${T(150, 14, 'valve', 'font-size="11"')}</svg>`,
    opts: ['Air from end 1 flows towards end 2. No change in the volume of the soap bubbles', 'Air from end 1 flows towards end 2. Volume of the soap bubble at end 1 decreases', 'No change occurs', 'Air from end 2 flows towards end 1. Volume of the soap bubble at end 1 increases'], ans: 1,
    sol: R`<ol class="steps">
      <li>A hemispherical cap has the <em>smallest</em> possible radius of curvature (= tube radius r). The flatter, sub-hemispherical cap at end 2 has a larger radius of curvature, R > r.</li>
      <li>Excess pressure \( 4T/R \): end 1 has the higher pressure.</li>
      <li>Air flows from 1 → 2, and the bubble at end 1 loses air, so its volume decreases.</li></ol>`,
  },
  {
    id: 't06-20', src: 't06', qno: 20, topic: 'reynolds', type: 'ar',
    q: R`<div class="ar"><p><strong>Assertion:</strong> For Reynolds number Re &gt; 2000, the flow of fluid is turbulent.</p><p><strong>Reason:</strong> Inertial forces are dominant compared to the viscous forces at such high Reynolds numbers.</p></div>`,
    opts: ['If both assertion and reason are true and reason is the correct explanation of assertion', 'If both assertion and reason are true but reason is not the correct explanation of assertion', 'If assertion is true but reason is false', 'If both assertion and reason are false'], ans: 0,
    sol: R`<p>\( R_e = \dfrac{\rho v d}{\eta} \) is the ratio of inertial force to viscous force. Above about 2000, inertia wins: small disturbances grow instead of being damped out by viscosity, and the flow turns turbulent. Both are true and R explains A.</p>`,
  },
  {
    id: 't06-20b', src: 't06', qno: '20b', topic: 'surface-tension', type: 'numerical',
    q: R`<p>Drops of liquid of density ρ are floating half immersed in a liquid of density σ. If the surface tension of the liquid is T, the radius of the drop will be:</p>`,
    opts: [R`\( \sqrt{\dfrac{3T}{g(3\rho-\sigma)}} \)`, R`\( \sqrt{\dfrac{6T}{g(2\rho-\sigma)}} \)`, R`\( \sqrt{\dfrac{3T}{g(2\rho-\sigma)}} \)`, R`\( \sqrt{\dfrac{3T}{g(4\rho-3\sigma)}} \)`], ans: 2,
    sol: R`<ol class="steps">
      <li>Up forces: buoyancy on the submerged half \( = \tfrac23\pi r^3\sigma g \), plus surface tension along the circle of contact (the equator), \( 2\pi r T \), acting vertically up.</li>
      <li>Down: weight \( = \tfrac43\pi r^3\rho g \).</li>
      <li>\( \tfrac43\pi r^3\rho g = \tfrac23\pi r^3\sigma g + 2\pi rT \Rightarrow \tfrac23 r^2 g(2\rho - \sigma) = 2T \Rightarrow r = \sqrt{\dfrac{3T}{g(2\rho - \sigma)}} \).</li></ol>`,
  },
  {
    id: 't06-21', src: 't06', qno: 21, topic: 'surface-energy', type: 'numerical',
    q: R`<p>The work done in increasing the size of a soap film from 10 cm × 6 cm to 10 cm × 11 cm is \( 3\times10^{-4} \) J. The surface tension of the film is:</p>`,
    opts: ['1.5 × 10⁻² N/m', '3.0 × 10⁻² N/m', '6.0 × 10⁻² N/m', '11.0 × 10⁻² N/m'], ans: 1,
    sol: R`<ol class="steps"><li>Increase in area of one face: \( 110 - 60 = 50 \text{ cm}^2 = 5\times10^{-3} \text{ m}^2 \).</li>
      <li>Two faces: \( \Delta A = 2 \times 5\times10^{-3} = 10^{-2} \text{ m}^2 \).</li>
      <li>\( T = \dfrac{W}{\Delta A} = \dfrac{3\times10^{-4}}{10^{-2}} = 3\times10^{-2} \text{ N/m} \).</li></ol>`,
    trap: R`Forgetting the two faces gives 6 × 10⁻² (option 3).`,
  },
  {
    id: 't06-22', src: 't06', qno: 22, topic: 'stokes', type: 'numerical',
    q: R`<p>A spherical ball of radius \( 1\times10^{-4} \) m and density \( 10^5 \) kg/m³ falls freely under gravity through a distance h before entering a tank of water. If after entering the water the velocity of the ball does not change, then the value of h is approximately (coefficient of viscosity of water is \( 9.8\times10^{-6} \) N s/m², g = 10 m s⁻²):</p>`,
    opts: ['2296 m', '2249 m', '2518 m', '2396 m'], ans: 2,
    sol: R`<ol class="steps">
      <li>"Velocity doesn't change in water" means it enters already at terminal velocity.</li>
      <li>\( v_t = \dfrac{2r^2(\rho - \sigma)g}{9\eta} = \dfrac{2(10^{-8})(10^5 - 10^3)(10)}{9 \times 9.8\times10^{-6}} = \dfrac{1.98\times10^{-2}}{8.82\times10^{-5}} \approx 224.5 \text{ m/s} \).</li>
      <li>Free fall: \( v^2 = 2gh \Rightarrow h = \dfrac{(224.5)^2}{20} \approx 2520 \text{ m} \approx 2518 \text{ m} \).</li></ol>`,
  },
  {
    id: 't06-23', src: 't06', qno: 23, topic: 'viscosity', type: 'statement',
    q: R`<div class="ar"><p><strong>Statement 1:</strong> Viscosity of gas increases with increase in temperature.</p><p><strong>Statement 2:</strong> With increase in temperature, collisions between the molecules of gas increase.</p></div>`,
    opts: ST_OPTS, ans: 0,
    sol: R`<p>Both are correct. Hotter gas molecules move faster and collide more often, transferring more momentum between neighbouring layers. That momentum transfer <em>is</em> gas viscosity, so η rises with temperature.</p>`,
  },
  {
    id: 't06-24', src: 't06', qno: 24, topic: 'stokes', type: 'statement', flagged: true,
    q: R`<div class="ar"><p><strong>Statement 1:</strong> A bigger rain drop falls faster than a smaller one.</p><p><strong>Statement 2:</strong> Terminal velocity of the drop is proportional to radius of the drop.</p></div>`,
    opts: ST_OPTS, ans: 1,
    sol: R`<p>Statement 1 is correct. Statement 2 is wrong: \( v_t = \dfrac{2r^2(\rho-\sigma)g}{9\eta} \propto r^2 \), the <em>square</em> of the radius, not r.</p>`,
    trap: R`Viscous force ∝ r, but terminal velocity ∝ r². The weight grows as r³ while the drag grows only as r·v.`,
  },
  {
    id: 't06-25', src: 't06', qno: 25, topic: 'surface-tension', type: 'match', flagged: true,
    q: R`<p>Match the following columns for the minimum force required (in addition to the weight of the body) to pull out the body from the surface of a liquid having surface tension T.</p>
      <div class="table-wrap"><table class="mtc"><tr><th>Column-I</th><th>Column-II</th></tr>
      <tr><td>1) Needle of length l</td><td>p) 2πRT</td></tr><tr><td>2) Disc of radius R with a hole of radius r</td><td>q) 8lT</td></tr>
      <tr><td>3) Circular plate of radius R</td><td>r) 2π(R + r)T</td></tr><tr><td>4) Square frame of side l</td><td>s) 2lT</td></tr><tr><td></td><td>t) 2π(R − r)T</td></tr></table></div>`,
    opts: ['1-s, 2-t, 3-p, 4-q', '1-s, 2-r, 3-p, 4-q', '1-s, 2-p, 3-p, 4-q', '1-s, 2-p, 3-p, 4-s'], ans: 1,
    sol: R`<p>Force = T × (total length of liquid in contact). Count every edge that touches the liquid:</p>
      <ul><li><strong>Needle:</strong> liquid along both long sides → 2l → <strong>2lT (s)</strong>.</li>
      <li><strong>Disc with a hole:</strong> outer edge 2πR <em>plus</em> inner edge 2πr → <strong>2π(R + r)T (r)</strong>.</li>
      <li><strong>Plate:</strong> only the outer rim → <strong>2πRT (p)</strong>.</li>
      <li><strong>Square wire frame:</strong> inside and outside of all four sides → 2 × 4l → <strong>8lT (q)</strong>.</li></ul>`,
    trap: R`For the disc with a hole, the edges <em>add</em>: 2π(R + r)T. Both rims pull down, so don't subtract.`,
  },
  {
    id: 't06-26', src: 't06', qno: 26, topic: 'surface-tension', type: 'multi', flagged: true,
    q: R`<p>Pick the correct statement(s) from the following.</p><ol type="i"><li>Addition of salt (sodium chloride) increases surface tension of water</li><li>Addition of soap decreases surface tension of water</li><li>At critical temperature surface tension of liquid becomes zero</li></ol>`,
    opts: ['i and ii', 'ii and iii', 'i and iii', 'i, ii and iii'], ans: 3,
    sol: R`<ul><li>(i) True: a highly soluble impurity like NaCl <em>raises</em> T.</li><li>(ii) True: soaps and detergents (sparingly soluble, surface-active) <em>lower</em> T. That's how they clean.</li>
      <li>(iii) True: T falls as temperature rises and becomes zero at the critical temperature, where liquid and vapour become indistinguishable.</li></ul>`,
  },
  {
    id: 't06-27', src: 't06', qno: 27, topic: 'surface-tension', type: 'multi', flagged: true,
    q: R`<p>Pick the <strong>wrong</strong> statement:</p>`,
    opts: ['With the increase in temperature surface tension of water decreases', 'Surface tension does not depend on the area of the surface', 'Surface tension is a vector', 'The molecules lying in surface film experience a net downward force'], ans: 2,
    sol: R`<p>Surface tension is a <strong>scalar</strong>: it is force per unit length (or energy per unit area), a property of the liquid with no direction of its own. The <em>force</em> it produces has a direction (along the surface, perpendicular to the edge), but T itself does not. The other three are true. Statement 2 is a common confusion: T is a material property, and stretching a film doesn't change T (unlike a rubber sheet).</p>`,
  },
  {
    id: 't06-28', src: 't06', qno: 28, topic: 'surface-tension', type: 'numerical',
    q: R`<p>A thin soap film formed between a U-shaped wire and a light slider supports a weight of \( 1.5\times10^{-2} \) N. The length of the slider is 30 cm and its weight is negligible. The surface tension of the liquid film is:</p>`,
    fig: `<svg viewBox="0 0 200 140" role="img" aria-label="U-shaped wire with soap film and a slider at the bottom holding a weight W">
      <rect x="50" y="22" width="100" height="70" style="fill:var(--plum-soft)"/>
      <path d="M50 92 V22 H150 V92" ${W}/><line x1="44" y1="92" x2="156" y2="92" style="stroke:var(--ink);stroke-width:3"/>
      <line x1="100" y1="92" x2="100" y2="112" style="stroke:var(--ink-2);stroke-width:1.5"/><rect x="90" y="112" width="20" height="14" style="fill:var(--ink-2)"/>${T(116, 124, 'W')}${T(80, 60, 'film')}${T(160, 96, '30 cm', 'font-size="11"')}</svg>`,
    opts: ['0.125 N m⁻¹', '0.1 N m⁻¹', '0.05 N m⁻¹', '0.025 N m⁻¹'], ans: 3,
    sol: R`<ol class="steps"><li>The film pulls the slider up with \( F = 2TL \) (two surfaces).</li>
      <li>\( 2T(0.30) = 1.5\times10^{-2} \Rightarrow T = \dfrac{1.5\times10^{-2}}{0.6} = 0.025 \text{ N/m} \).</li></ol>`,
  },
  {
    id: 't06-29', src: 't06', qno: 29, topic: 'surface-tension', type: 'numerical',
    q: R`<p>Maximum diameter of a wire made of a material of density ρ that can float on the surface of a liquid of surface tension T is:</p>`,
    opts: [R`\( \sqrt{\dfrac{8T}{\pi g\rho}} \)`, R`\( \sqrt{\dfrac{4T}{\pi g\rho}} \)`, R`\( \sqrt{\dfrac{2T}{\pi g\rho}} \)`, R`\( \sqrt{\dfrac{T}{\pi g\rho}} \)`], ans: 0,
    sol: R`<ol class="steps"><li>For a length ℓ of wire: weight \( = \rho\cdot\dfrac{\pi d^2}{4}\ell\cdot g \).</li>
      <li>Maximum surface-tension support (liquid along both sides, pulling vertically): \( 2T\ell \).</li>
      <li>\( \dfrac{\pi d^2\rho g}{4} = 2T \Rightarrow d = \sqrt{\dfrac{8T}{\pi\rho g}} \).</li></ol>`,
  },
  {
    id: 't06-30', src: 't06', qno: 30, topic: 'stokes', type: 'numerical',
    q: R`<p>A small spherical ball falling through a viscous medium of negligible density has terminal velocity v. Another ball of the same mass but of radius twice that of the earlier falling through the same viscous medium will have terminal velocity (ignore buoyancy):</p>`,
    opts: ['v', 'v/4', 'v/2', 'v/8'], ans: 2,
    sol: R`<ol class="steps"><li>At terminal velocity (no buoyancy): \( mg = 6\pi\eta r v \Rightarrow v = \dfrac{mg}{6\pi\eta r} \).</li>
      <li>Same mass, so \( v \propto 1/r \). Doubling r gives \( v/2 \).</li></ol>`,
    trap: R`\( v \propto r^2 \) is only for the <em>same density</em>. Here the mass is fixed, so go back to the force balance.`,
  },
  {
    id: 't06-31', src: 't06', qno: 31, topic: 'viscosity', type: 'numerical',
    q: R`<p>The velocity of the surface layer of water in a river of depth 10 m is 5 m s⁻¹. The shearing stress between the surface layer and the bottom layer is (coefficient of viscosity of water η = 10⁻³ SI units):</p>`,
    opts: ['0.6 × 10⁻³ N m⁻²', '0.8 × 10⁻³ N m⁻²', '0.5 × 10⁻³ N m⁻²', '10⁻³ N m⁻²'], ans: 2,
    sol: R`<p>Bottom layer is at rest. Velocity gradient \( = \dfrac{5}{10} = 0.5 \text{ s}^{-1} \). Stress \( = \eta\dfrac{dv}{dy} = 10^{-3}\times0.5 = 0.5\times10^{-3} \text{ N/m}^2 \).</p>`,
  },
  {
    id: 't06-32', src: 't06', qno: 32, topic: 'stokes', type: 'numerical',
    q: R`<p>Eight drops of a liquid of density ρ and each of radius a are falling through air with a constant velocity 3.75 cm s⁻¹. When the eight drops coalesce to form a single drop, the terminal velocity of the new drop will be:</p>`,
    opts: ['15 × 10⁻² m s⁻¹', '2.4 × 10⁻² m s⁻¹', '0.75 × 10⁻² m s⁻¹', '25 × 10⁻² m s⁻¹'], ans: 0,
    sol: R`<ol class="steps"><li>Volume conserved: \( R^3 = 8a^3 \Rightarrow R = 2a \).</li>
      <li>\( v_t \propto r^2 \Rightarrow v' = 4 \times 3.75 = 15 \text{ cm/s} = 15\times10^{-2} \text{ m/s} \).</li></ol>`,
    key: R`n drops merge → \( v' = n^{2/3}v \). For n = 8, that's 4v; for n = 27, 9v; for n = 64, 16v.`,
  },
  {
    id: 't06-33', src: 't06', qno: 33, topic: 'surface-energy', type: 'numerical',
    q: R`<p>How much work will be done in increasing the diameter of a soap bubble from 2 cm to 5 cm? Surface tension of soap solution is \( 3\times10^{-2} \) N m⁻¹.</p>`,
    opts: ['3.96 × 10⁻⁴ J', '39.6 × 10⁻⁴ J', '0.396 × 10⁻⁴ J', '396 × 10⁻⁴ J'], ans: 0,
    sol: R`<ol class="steps"><li>Radii: 1 cm → 2.5 cm. A bubble has two surfaces: \( \Delta A = 2 \times 4\pi(R_2^2 - R_1^2) \).</li>
      <li>\( \Delta A = 8\pi(6.25 - 1)\times10^{-4} = 8\pi(5.25)\times10^{-4} \approx 1.32\times10^{-2} \text{ m}^2 \).</li>
      <li>\( W = T\Delta A = 3\times10^{-2}\times1.32\times10^{-2} \approx 3.96\times10^{-4} \text{ J} \).</li></ol>`,
    trap: R`The question gives diameters, so halve them. Forgetting the factor 2 (two surfaces) halves the answer.`,
  },
  {
    id: 't06-34', src: 't06', qno: 34, topic: 'capillarity', type: 'numerical',
    q: R`<p>A capillary tube of radius R is immersed in water and water rises in it to a height H. The mass of water in the capillary tube is M. Another capillary tube of radius 2R is immersed in water. The mass of water that will rise in this tube is:</p>`,
    opts: ['M', '2M', 'M/2', '4M'], ans: 1,
    sol: R`<ol class="steps"><li>The weight of the raised column is balanced by surface tension: \( Mg = 2\pi R T\cos\theta \), so \( M \propto R \).</li>
      <li>Or: \( M = \rho\pi R^2 h \) with \( h \propto 1/R \), so \( M \propto R \).</li>
      <li>Doubling R doubles the mass: 2M.</li></ol>`,
  },
  {
    id: 't06-35', src: 't06', qno: 35, topic: 'drops-bubbles', type: 'numerical',
    q: R`<p>An air bubble of radius 0.1 cm lies at a depth of 20 cm below the free surface of a liquid of density 1000 kg/m³. If the pressure inside the bubble is 2100 N/m² greater than the atmospheric pressure, then the surface tension of the liquid in SI units is (g = 10 m/s²):</p>`,
    opts: ['0.02', '0.1', '0.25', '0.05'], ans: 3,
    sol: R`<ol class="steps"><li>Inside an air bubble in a liquid (one surface): \( P_\text{in} = P_0 + \rho g h + \dfrac{2T}{r} \).</li>
      <li>\( 2100 = 1000(10)(0.2) + \dfrac{2T}{10^{-3}} = 2000 + 2000T \).</li>
      <li>\( T = 0.05 \text{ N/m} \).</li></ol>`,
  },
  {
    id: 't06-36', src: 't06', qno: 36, topic: 'viscosity', type: 'numerical',
    q: R`<p>A plate of area 100 cm² is placed on the upper surface of castor oil, 2 mm thick. Taking the coefficient of viscosity to be 15.5 poise, calculate the horizontal force necessary to move the plate with a velocity 3 cm s⁻¹.</p>`,
    opts: ['232.5 N', '23.25 N', '0.2325 N', '2.325 N'], ans: 2,
    sol: R`<ol class="steps"><li>SI units: η = 15.5 poise = 1.55 Pa·s; A = 10⁻² m²; v = 0.03 m/s; d = 2×10⁻³ m.</li>
      <li>\( F = \eta A\dfrac{v}{d} = 1.55 \times 10^{-2} \times \dfrac{0.03}{0.002} = 1.55\times10^{-2}\times15 = 0.2325 \text{ N} \).</li></ol>`,
    trap: R`1 poise = 0.1 Pa·s. Forgetting this conversion gives 2.325 N (option 4).`,
  },
  {
    id: 't06-37', src: 't06', qno: 37, topic: 'stokes', type: 'numerical',
    q: R`<p>One spherical ball of radius R, density d released in a liquid of density d/2 attains a terminal velocity V. Another ball of radius 2R and density 1.5d, released in the same liquid, will attain a terminal velocity:</p>`,
    opts: ['2V', '4V', '6V', '8V'], ans: 3,
    sol: R`<ol class="steps"><li>\( v_t \propto r^2(\rho - \sigma) \).</li>
      <li>\( \dfrac{V'}{V} = \dfrac{(2R)^2(1.5d - 0.5d)}{R^2(d - 0.5d)} = \dfrac{4 \times d}{0.5d} = 8 \).</li></ol>`,
  },
  {
    id: 't06-38', src: 't06', qno: 38, topic: 'reynolds', type: 'multi',
    q: R`<p>Consider the following statements:</p><ol><li>Surface tension arises due to extra energy of the molecules at the interior as compared to the molecules at the surface of a liquid.</li><li>As the temperature of liquid rises, the coefficient of viscosity increases.</li><li>As the temperature of gas increases, the coefficient of viscosity increases.</li><li>The onset of turbulence is determined by Reynold's number.</li><li>In a steady flow two streamlines never intersect.</li></ol><p>Choose the correct answer from the options given below:</p>`,
    opts: ['1, 4, 5 only', '3, 4, 5 only', '2, 3, 4 only', '1, 2, 3 only'], ans: 1,
    sol: R`<ul><li>1. False: it's the <em>surface</em> molecules that have extra energy (they lose half their neighbours).</li>
      <li>2. False: liquid viscosity <em>decreases</em> as temperature rises.</li><li>3. True.</li><li>4. True: turbulence sets in above a critical Re.</li>
      <li>5. True: if two streamlines crossed, a particle there would have two velocities at once.</li></ul>`,
  },
  {
    id: 't06-39', src: 't06', qno: 39, topic: 'stokes', type: 'numerical',
    q: R`<p>A metal ball of radius 'r' and density 'd' travels with a terminal velocity 'v' in a liquid of density d/4. The terminal velocity of another ball of radius '2r' and density '3d' in the same liquid is:</p>`,
    opts: [R`\( \frac{44v}{3} \)`, R`\( \frac{22v}{3} \)`, R`\( \frac{11v}{3} \)`, R`\( \frac{3v}{44} \)`], ans: 0,
    sol: R`<ol class="steps"><li>\( v \propto r^2(\rho - \sigma) \).</li>
      <li>\( \dfrac{v'}{v} = \dfrac{4r^2(3d - d/4)}{r^2(d - d/4)} = \dfrac{4 \times 11d/4}{3d/4} = \dfrac{44}{3} \).</li></ol>`,
  },
  {
    id: 't06-40', src: 't06', qno: 40, topic: 'stokes', type: 'numerical',
    q: R`<p>A solid sphere of radius R acquires a terminal velocity \( v_1 \) when falling (due to gravity) through a viscous fluid having coefficient of viscosity η. The sphere is broken into 27 identical solid spheres. If each of these spheres acquires a terminal velocity \( v_2 \) when falling through the same fluid, the ratio \( v_1/v_2 \) equals:</p>`,
    opts: ['9', '1/27', '1/9', '27'], ans: 0,
    sol: R`<ol class="steps"><li>Volume: \( 27r^3 = R^3 \Rightarrow r = R/3 \).</li>
      <li>\( v \propto r^2 \Rightarrow \dfrac{v_1}{v_2} = \left(\dfrac{R}{R/3}\right)^2 = 9 \).</li></ol>`,
  },
  {
    id: 't06-41', src: 't06', qno: 41, topic: 'stokes', type: 'numerical',
    q: R`<p>An air bubble of negligible weight having radius r rises steadily through a solution of density σ at speed v. The coefficient of viscosity of the solution is given by:</p>`,
    opts: [R`\( \eta = \dfrac{4r\sigma g}{9v} \)`, R`\( \eta = \dfrac{4r^2\sigma g}{9v} \)`, R`\( \eta = \dfrac{2r^2\sigma g}{9v} \)`, R`\( \eta = \dfrac{2r^2\sigma g}{3\pi v} \)`], ans: 2,
    sol: R`<ol class="steps"><li>Steady rise: buoyancy = viscous drag (weight negligible).</li>
      <li>\( \tfrac43\pi r^3\sigma g = 6\pi\eta r v \Rightarrow \eta = \dfrac{4r^2\sigma g}{18v} = \dfrac{2r^2\sigma g}{9v} \).</li></ol>`,
  },
  {
    id: 't06-42', src: 't06', qno: 42, topic: 'viscosity', type: 'concept', flagged: true,
    q: R`<p>For an ideal fluid, viscosity is:</p>`,
    opts: ['zero', 'infinity', 'finite but small', 'unity'], ans: 0,
    sol: R`<p>An ideal fluid is defined as incompressible and <strong>non-viscous</strong> (η = 0). That's the assumption behind Bernoulli's equation.</p>`,
  },
  {
    id: 't06-43', src: 't06', qno: 43, topic: 'viscosity', type: 'concept', flagged: true,
    q: R`<p>A good lubricant must have:</p>`,
    opts: ['high viscosity', 'low viscosity', 'high density', 'low surface tension'], ans: 0,
    sol: R`<p>A lubricant has to stay between moving parts as a film and carry the load without being squeezed out. That needs <strong>high viscosity</strong> (machine oils and grease are thick for this reason).</p>`,
    trap: R`"Lubricant = slippery = low viscosity" feels right but is the wrong reasoning. A thin liquid would be squeezed out and the metal surfaces would touch.`,
  },
  {
    id: 't06-44', src: 't06', qno: 44, topic: 'stokes', type: 'numerical',
    q: R`<p>A solid steel ball of diameter 3.6 mm acquired terminal velocity \( 2.45\times10^{-2} \) m/s while falling under gravity through an oil of density 925 kg m⁻³. Take the density of steel as 7825 kg m⁻³ and g as 9.8 m/s². The viscosity of the oil in SI unit is:</p>`,
    opts: ['2.18', '2.38', '1.68', '1.99'], ans: 3,
    sol: R`<ol class="steps"><li>\( r = 1.8\times10^{-3} \text{ m},\ \rho - \sigma = 7825 - 925 = 6900 \text{ kg/m}^3 \).</li>
      <li>\( \eta = \dfrac{2r^2(\rho-\sigma)g}{9v} = \dfrac{2(3.24\times10^{-6})(6900)(9.8)}{9(2.45\times10^{-2})} = \dfrac{0.4382}{0.2205} \approx 1.99 \text{ Pa·s} \).</li></ol>`,
    trap: R`It's a diameter, so halve it to get r.`,
  },
  {
    id: 't06-45', src: 't06', qno: 45, topic: 'stokes', type: 'numerical',
    q: R`<p>A small rigid spherical ball of mass M is dropped in a long vertical tube containing glycerine. The velocity of the ball becomes constant after some time. If the density of glycerine is half of the density of the ball, then the viscous force acting on the ball will be (consider g as acceleration due to gravity):</p>`,
    opts: [R`\( \frac32 Mg \)`, R`\( \frac{Mg}{2} \)`, 'Mg', '2Mg'], ans: 1,
    sol: R`<ol class="steps"><li>Constant velocity: weight = buoyancy + viscous force.</li>
      <li>Buoyancy \( = V\sigma g = V\frac{\rho}{2}g = \frac{Mg}{2} \).</li>
      <li>Viscous force \( = Mg - \frac{Mg}{2} = \frac{Mg}{2} \).</li></ol>`,
  }
  );
})();
