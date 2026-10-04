/* =====================================================================
   Practice bank — Mechanical Properties of Solids (src: 'xs')
   Every numerical answer below has been checked by direct calculation.
   Strings use String.raw so MathJax backslashes need no doubling.
   ===================================================================== */
window.QBANK = window.QBANK || [];
(function () {
  'use strict';
  const R = String.raw;
  const AR = [
    'Both A and R are true and R is the correct explanation of A',
    'Both A and R are true but R is NOT the correct explanation of A',
    'A is true but R is false',
    'A is false but R is true',
  ];
  const ST = [
    'Both Statement I and Statement II are true',
    'Both Statement I and Statement II are false',
    'Statement I is true but Statement II is false',
    'Statement I is false but Statement II is true',
  ];

  const list = [
    /* ---------------- elasticity ---------------- */
    { topic: 'elasticity', type: 'concept',
      q: R`<p>A rubber band and a steel wire are both stretched. Which one is <em>more elastic</em> in the physics sense?</p>`,
      opts: [
        'Rubber, because it stretches a lot and still returns',
        R`Steel, because for the same stress it shows far less strain (larger \(Y\))`,
        'Both are equally elastic since both regain their shape',
        'They cannot be compared without knowing the load',
      ],
      ans: 1,
      sol: R`<ol class="steps">
        <li>In physics, "more elastic" means <strong>stronger restoring tendency</strong>: a bigger stress is needed to produce a given strain. That is measured by the modulus, \(Y = \text{stress}/\text{strain}\).</li>
        <li>\(Y_\text{steel} \approx 2\times10^{11}\ \text{Pa}\); \(Y_\text{rubber} \sim 10^{6}\text{–}10^{7}\ \text{Pa}\). Steel's \(Y\) is about \(10^{4}\)–\(10^{5}\) times larger.</li>
        <li>So steel is more elastic.</li></ol>
        <p class="why-opts">Option 1 confuses "stretches easily" with "elastic"; easy stretching means a <em>small</em> \(Y\). Option 3: both returning to shape only says both are elastic, not equally so. Option 4: \(Y\) is a material constant, so no load is needed to compare.</p>`,
      trap: 'Everyday language says rubber is "elastic". In physics, larger modulus = more elastic, so steel wins.',
      key: R`More elastic \(\Leftrightarrow\) larger \(Y\) \(\Leftrightarrow\) less strain for the same stress.` },

    { topic: 'elasticity', type: 'concept',
      q: R`<p>The Young's modulus of a <em>perfectly rigid</em> body is</p>`,
      opts: ['zero', 'unity', 'infinite', 'equal to the applied stress'],
      ans: 2,
      sol: R`<ol class="steps">
        <li>A perfectly rigid body shows no change in length for any force: \(\Delta L = 0\), so strain \(= 0\).</li>
        <li>\(Y = \dfrac{\text{stress}}{\text{strain}} = \dfrac{F/A}{0} \to \infty\).</li>
        <li>For the same reason, \(G\) and \(B\) of a rigid body are also infinite.</li></ol>
        <p class="why-opts">Zero would mean the body deforms with no stress at all (the opposite of rigid). "Unity" and "equal to stress" have no basis; \(Y\) is a ratio with units of Pa.</p>`,
      key: 'Perfectly rigid: Y = G = B = ∞. (Real bodies are never perfectly rigid.)' },

    { topic: 'elasticity', type: 'ar',
      q: R`<div class="ar"><p><strong>Assertion (A):</strong> Rubber is more elastic than steel.</p>
        <p><strong>Reason (R):</strong> For the same stress, the strain produced in rubber is much larger than in steel.</p></div>`,
      opts: AR, ans: 3,
      sol: R`<ol class="steps">
        <li><strong>R is true:</strong> rubber's \(Y\) is tiny, so a given stress gives a large strain.</li>
        <li><strong>A is false:</strong> because rubber has the larger strain for the same stress, its \(Y\) is smaller, so it is <em>less</em> elastic than steel.</li></ol>
        <p class="why-opts">So option 4: A false, R true. Options 1–3 all need A to be true.</p>`,
      trap: 'Students mark option 1 because the Reason is a true fact. Check the Assertion on its own first.' },

    /* ---------------- stress & strain ---------------- */
    { topic: 'stress', type: 'numerical',
      q: R`<p>A load of 10 kg hangs from a wire of diameter 2 mm. The tensile stress in the wire is about \((g = 9.8\ \text{m s}^{-2})\)</p>`,
      opts: [R`\(7.8\times10^{6}\ \text{N m}^{-2}\)`, R`\(2.5\times10^{7}\ \text{N m}^{-2}\)`, R`\(3.1\times10^{7}\ \text{N m}^{-2}\)`, R`\(1.2\times10^{8}\ \text{N m}^{-2}\)`],
      ans: 2,
      sol: R`<ol class="steps">
        <li>\(F = mg = 10\times9.8 = 98\ \text{N}\).</li>
        <li>Radius \(r = 1\ \text{mm} = 10^{-3}\ \text{m}\), so \(A = \pi r^2 = 3.14\times10^{-6}\ \text{m}^2\).</li>
        <li>\(\text{Stress} = F/A = 98/(3.14\times10^{-6}) \approx 3.1\times10^{7}\ \text{N m}^{-2}\).</li></ol>`,
      trap: R`Using the diameter (2 mm) as the radius gives \(7.8\times10^{6}\), which is four times too small. Halve the diameter first.` },

    { topic: 'stress', type: 'statement',
      q: R`<p><strong>Statement I:</strong> Under hydraulic stress, the shape of a body changes but its volume stays the same.</p>
        <p><strong>Statement II:</strong> Shearing strain is measured by the angle \(\theta\) (in radian) through which a face turns, \(\theta \approx \Delta x/L\).</p>`,
      opts: ST, ans: 3,
      sol: R`<ol class="steps">
        <li>Hydraulic stress is an equal normal push from all sides. It changes the <strong>volume</strong> and keeps the <strong>shape</strong>, which is the reverse of Statement I. So I is false.</li>
        <li>Shear stress turns a face through \(\theta\); for small deformations \(\tan\theta \approx \theta = \Delta x/L\). Statement II is true.</li></ol>`,
      key: 'Tensile/compressive: length changes. Shear: shape changes, volume does not. Hydraulic: volume changes, shape does not.' },

    { topic: 'stress', type: 'match',
      q: R`<p>Match List I with List II.</p>
        <div class="table-wrap"><table class="mtc"><thead><tr><th>List I</th><th>List II</th></tr></thead><tbody>
        <tr><td>(A) Young's modulus</td><td>(P) \(-V\,\Delta p/\Delta V\)</td></tr>
        <tr><td>(B) Shear modulus</td><td>(Q) \(FL/(A\,\Delta L)\)</td></tr>
        <tr><td>(C) Bulk modulus</td><td>(R) \(F/(A\,\theta)\)</td></tr>
        <tr><td>(D) Compressibility</td><td>(S) \(-\Delta V/(V\,\Delta p)\)</td></tr>
        </tbody></table></div>`,
      opts: ['A-Q, B-P, C-R, D-S', 'A-Q, B-R, C-P, D-S', 'A-R, B-Q, C-S, D-P', 'A-Q, B-R, C-S, D-P'],
      ans: 1,
      sol: R`<ol class="steps">
        <li>\(Y = \dfrac{F/A}{\Delta L/L} = \dfrac{FL}{A\,\Delta L}\) → A-Q.</li>
        <li>\(G = \dfrac{F/A}{\theta} = \dfrac{F}{A\theta}\) → B-R.</li>
        <li>\(B = -\dfrac{\Delta p}{\Delta V/V} = -\dfrac{V\Delta p}{\Delta V}\) → C-P. The minus sign makes \(B\) positive, because \(\Delta V &lt; 0\) when \(\Delta p &gt; 0\).</li>
        <li>Compressibility \(k = 1/B = -\dfrac{\Delta V}{V\,\Delta p}\) → D-S.</li></ol>` },

    /* ---------------- stress–strain curve ---------------- */
    { topic: 'curve', type: 'graph',
      q: R`<p>Stress–strain graphs for two materials P and Q are drawn to the same scale. Which statement is correct?</p>`,
      fig: R`<svg viewBox="0 0 320 210" role="img" aria-label="Stress–strain curves of materials P and Q">
        <line x1="40" y1="180" x2="300" y2="180" stroke="#454F66" stroke-width="1.5"/>
        <line x1="40" y1="180" x2="40" y2="14" stroke="#454F66" stroke-width="1.5"/>
        <text x="300" y="198" font-size="12" text-anchor="end" fill="#454F66">Strain</text>
        <text x="46" y="20" font-size="12" fill="#454F66">Stress</text>
        <path d="M40 180 L100 72 Q112 52 124 50 L132 56" fill="none" stroke="#4B5BD0" stroke-width="2.5"/>
        <text x="134" y="46" font-size="13" font-weight="700" fill="#4B5BD0">P</text>
        <path d="M40 180 L92 128 Q110 112 150 100 Q200 86 228 88 Q252 92 272 104" fill="none" stroke="#D6604A" stroke-width="2.5"/>
        <text x="276" y="100" font-size="13" font-weight="700" fill="#D6604A">Q</text>
        <text x="128" y="62" font-size="12" fill="#1B2233">×</text>
        <text x="269" y="110" font-size="12" fill="#1B2233">×</text>
      </svg>`,
      opts: [
        'P has the larger Young\'s modulus; Q is more ductile',
        'Q has the larger Young\'s modulus; P is more ductile',
        'P has the larger Young\'s modulus and is also more ductile',
        'Both have the same Young\'s modulus; Q is stronger',
      ],
      ans: 0,
      sol: R`<ol class="steps">
        <li>In the straight (Hooke's law) part, the slope is \(Y\). P's initial line is steeper, so \(Y_P &gt; Y_Q\).</li>
        <li>Ductility is the size of the plastic region, from the end of the elastic part to fracture (×). Q stretches a long way before breaking, so Q is more ductile. P breaks soon after its elastic limit, which is brittle-like.</li>
        <li>P also reaches a higher maximum stress, so P has the larger ultimate strength (it is "stronger").</li></ol>
        <p class="why-opts">Option 2 swaps both properties. Option 3: P's short plastic region means low ductility. Option 4: the slopes clearly differ, and P, not Q, reaches the higher stress.</p>`,
      key: 'Steeper initial slope → larger Y. Longer curve after the elastic limit → more ductile. Higher peak → stronger.' },

    { topic: 'curve', type: 'concept',
      q: R`<p>On the stress–strain curve of a ductile metal, the point beyond which the wire does <em>not</em> return to its original length when the load is removed is the</p>`,
      opts: ['proportional limit', 'elastic limit (yield point)', 'ultimate tensile strength point', 'fracture point'],
      ans: 1,
      sol: R`<ol class="steps">
        <li>Up to the <strong>elastic limit / yield point (B)</strong>, removing the load brings the wire back to zero strain.</li>
        <li>Beyond B, the wire unloads along a line parallel to the original slope and is left with a <strong>permanent set</strong>.</li></ol>
        <p class="why-opts">Proportional limit (A): beyond it, stress is no longer proportional to strain, but the wire can still be elastic up to B. Ultimate point (D) and fracture (E) are far into the plastic region; permanent set has already appeared before them.</p>`,
      trap: 'Proportional limit ≠ elastic limit. Between A and B the body is still elastic but no longer obeys Hooke\'s law.' },

    { topic: 'curve', type: 'statement',
      q: R`<p><strong>Statement I:</strong> Substances like rubber and the tissue of the aorta can be stretched to large strains and still return to their original length; they have no well-defined plastic region.</p>
        <p><strong>Statement II:</strong> Rubber obeys Hooke's law over most of its elastic region.</p>`,
      opts: ST, ans: 2,
      sol: R`<ol class="steps">
        <li>Statement I is the NCERT description of <strong>elastomers</strong>, so it is true.</li>
        <li>An elastomer's stress–strain curve is curved almost everywhere: the elastic region is large, but stress is <em>not</em> proportional to strain. Statement II is false.</li></ol>`,
      key: 'Elastomers: large elastic range, but Hooke\'s law is NOT obeyed over most of it.' },

    { topic: 'curve', type: 'match',
      q: R`<p>Match each material with its typical behaviour.</p>
        <div class="table-wrap"><table class="mtc"><thead><tr><th>List I</th><th>List II</th></tr></thead><tbody>
        <tr><td>(A) Glass</td><td>(P) Elastomer: very large elastic strain, no proportional region</td></tr>
        <tr><td>(B) Copper</td><td>(Q) Brittle: breaks soon after the elastic limit</td></tr>
        <tr><td>(C) Rubber / aorta</td><td>(R) Ductile: long plastic region, can be drawn into wires</td></tr>
        <tr><td>(D) Quartz fibre</td><td>(S) Very nearly perfectly elastic</td></tr>
        </tbody></table></div>`,
      opts: ['A-R, B-Q, C-P, D-S', 'A-Q, B-R, C-S, D-P', 'A-Q, B-P, C-R, D-S', 'A-Q, B-R, C-P, D-S'],
      ans: 3,
      sol: R`<ol class="steps">
        <li>Glass fractures with almost no plastic flow, so it is brittle: A-Q.</li>
        <li>Copper has a large plastic region, which is why it is drawn into wires: B-R.</li>
        <li>Rubber and aorta tissue are elastomers: C-P.</li>
        <li>A quartz fibre is the textbook example of a nearly perfectly elastic body: D-S.</li></ol>` },

    /* ---------------- Young's modulus ---------------- */
    { topic: 'youngs', type: 'numerical',
      q: R`<p>Young's modulus of steel is twice that of brass. Two wires, one of steel and one of brass, have the same length and the same area of cross-section. What should be the ratio of the weights added to the steel and brass wires to produce the same elongation?</p>`,
      opts: ['1 : 2', '2 : 1', '4 : 1', '1 : 1'],
      ans: 1,
      sol: R`<ol class="steps">
        <li>\(F = \dfrac{YA\,\Delta L}{L}\). With \(A\), \(L\) and \(\Delta L\) the same, \(F \propto Y\).</li>
        <li>\(W_\text{steel} : W_\text{brass} = Y_s : Y_b = 2 : 1\).</li></ol>`,
      key: R`Same \(L, A, \Delta L\) → load \(\propto Y\). Same load → \(\Delta L \propto 1/Y\).` },

    { topic: 'youngs', type: 'numerical',
      q: R`<p>Two wires are made of the same material and have the same volume. Their areas of cross-section are \(A\) and \(3A\). If a force \(F\) produces an extension \(\Delta x\) in the first wire, the force needed to produce the same extension in the second wire is</p>`,
      opts: [R`\(3F\)`, R`\(6F\)`, R`\(9F\)`, R`\(F/3\)`],
      ans: 2,
      sol: R`<ol class="steps">
        <li>Same volume: \(A L_1 = 3A\,L_2 \Rightarrow L_2 = L_1/3\).</li>
        <li>\(F = \dfrac{YA\,\Delta x}{L}\), so for the same \(Y\) and \(\Delta x\): \(F \propto \dfrac{A}{L}\).</li>
        <li>\(\dfrac{F_2}{F_1} = \dfrac{3A}{A}\cdot\dfrac{L_1}{L_1/3} = 3\times3 = 9\), so \(F_2 = 9F\).</li></ol>`,
      trap: R`Answering \(3F\) forgets that the thicker wire is also 3 times shorter. With fixed volume, \(A/L \propto A^2\).`,
      key: R`Same volume: \(F \propto A^2\) for equal extension, and \(\Delta L \propto L^2\) for equal force.` },

    { topic: 'youngs', type: 'graph',
      q: R`<p>The graph shows extension (\(\Delta l\)) against load (\(F\)) for two wires A and B of the <em>same material</em> and the <em>same length</em>. Line A makes 60° and line B makes 30° with the load axis. Then</p>`,
      fig: R`<svg viewBox="0 0 300 200" role="img" aria-label="Extension versus load lines at 60 and 30 degrees">
        <line x1="40" y1="170" x2="280" y2="170" stroke="#454F66" stroke-width="1.5"/>
        <line x1="40" y1="170" x2="40" y2="14" stroke="#454F66" stroke-width="1.5"/>
        <text x="280" y="190" font-size="12" text-anchor="end" fill="#454F66">Load F</text>
        <text x="46" y="20" font-size="12" fill="#454F66">Extension Δl</text>
        <line x1="40" y1="170" x2="125" y2="22.8" stroke="#4B5BD0" stroke-width="2.5"/>
        <text x="130" y="30" font-size="13" font-weight="700" fill="#4B5BD0">A</text>
        <line x1="40" y1="170" x2="270" y2="37.2" stroke="#D6604A" stroke-width="2.5"/>
        <text x="272" y="34" font-size="13" font-weight="700" fill="#D6604A">B</text>
        <path d="M80 170 A40 40 0 0 0 74.6 150" fill="none" stroke="#D6604A" stroke-width="1.5"/>
        <text x="86" y="160" font-size="11" fill="#D6604A">30°</text>
        <path d="M62 170 A22 22 0 0 0 51 151" fill="none" stroke="#4B5BD0" stroke-width="1.5"/>
        <text x="50" y="140" font-size="11" fill="#4B5BD0">60°</text>
      </svg>`,
      opts: [
        R`A is thicker; \(A_A/A_B = 3\)`,
        R`B is thicker; \(A_B/A_A = 3\)`,
        R`B is thicker; \(A_B/A_A = \sqrt{3}\)`,
        R`A is thicker; \(A_A/A_B = \sqrt{3}\)`,
      ],
      ans: 1,
      sol: R`<ol class="steps">
        <li>\(\Delta l = \dfrac{L}{AY}\,F\). On a \(\Delta l\)–\(F\) graph the slope is \(\dfrac{L}{AY} \propto \dfrac{1}{A}\) (same \(L\), same \(Y\)).</li>
        <li>\(\dfrac{\text{slope}_A}{\text{slope}_B} = \dfrac{\tan 60^\circ}{\tan 30^\circ} = \dfrac{\sqrt3}{1/\sqrt3} = 3 = \dfrac{A_B}{A_A}\).</li>
        <li>B has the gentler slope, so it stretches less per newton and is the thicker wire: \(A_B = 3A_A\).</li></ol>`,
      trap: R`Check which quantity is on which axis. If the axes were swapped (load vs extension), the slope would be \(AY/L\) and the steeper line would be the thicker wire.` },

    { topic: 'youngs', type: 'numerical',
      q: R`<p>A piece of copper of fixed volume \(V\) is drawn into a wire of length \(l\). When this wire is pulled by a constant force \(F\), its extension is proportional to</p>`,
      opts: [R`\(l\)`, R`\(1/l\)`, R`\(l^{2}\)`, R`\(1/l^{2}\)`],
      ans: 2,
      sol: R`<ol class="steps">
        <li>\(A = V/l\).</li>
        <li>\(\Delta l = \dfrac{Fl}{AY} = \dfrac{Fl}{(V/l)Y} = \dfrac{F\,l^{2}}{VY}\).</li>
        <li>With \(F, V, Y\) fixed, \(\Delta l \propto l^{2}\).</li></ol>`,
      trap: R`Treating \(A\) as constant gives \(\Delta l \propto l\). Drawing the wire longer also makes it thinner.` },

    { topic: 'youngs', type: 'numerical',
      q: R`<p>A wire breaks when a load \(W\) is hung from it. Another wire of the same material, with twice the radius and twice the length, will break under a load of</p>`,
      opts: [R`\(2W\)`, R`\(4W\)`, R`\(W\)`, R`\(8W\)`],
      ans: 1,
      sol: R`<ol class="steps">
        <li>Breaking happens when stress reaches the <strong>breaking stress</strong>, a property of the material: \(W_\text{break} = \sigma_\text{break}\times \pi r^{2}\).</li>
        <li>Length does not appear. Doubling \(r\) gives \(4\times\) the area, so the breaking load is \(4W\).</li></ol>`,
      trap: 'Length is a distractor: breaking load depends only on material and area (∝ r²).',
      key: 'Breaking stress = material property. Breaking load ∝ r², independent of length.' },

    { topic: 'youngs', type: 'numerical',
      q: R`<p>A rubber cord 8 m long hangs vertically from a ceiling. Its density is \(1.5\times10^{3}\ \text{kg m}^{-3}\) and Young's modulus is \(5\times10^{6}\ \text{N m}^{-2}\). The extension of the cord due to its own weight is \((g = 10\ \text{m s}^{-2})\)</p>`,
      opts: [R`\(9.6\times10^{-2}\ \text{m}\)`, R`\(19.2\times10^{-2}\ \text{m}\)`, R`\(9.6\times10^{-3}\ \text{m}\)`, R`\(4.8\times10^{-2}\ \text{m}\)`],
      ans: 0,
      sol: R`<ol class="steps">
        <li>Tension grows from 0 at the bottom to \(Mg\) at the top, so the average tension is \(Mg/2\) and \(\Delta l = \dfrac{MgL}{2AY}\).</li>
        <li>With \(M = \rho A L\): \(\Delta l = \dfrac{\rho g L^{2}}{2Y}\). The area cancels.</li>
        <li>\(\Delta l = \dfrac{1.5\times10^{3}\times10\times 64}{2\times5\times10^{6}} = \dfrac{9.6\times10^{5}}{10^{7}} = 9.6\times10^{-2}\ \text{m}\).</li></ol>`,
      trap: R`Forgetting the factor ½ gives \(19.2\times10^{-2}\) m. The whole weight does not act on every part of the cord.` },

    { topic: 'youngs', type: 'numerical',
      q: R`<p>Two wires of the same length \(L\) and the same area of cross-section, with Young's moduli \(Y_1\) and \(Y_2\), are joined end to end. The composite wire of length \(2L\) behaves like a single wire whose Young's modulus is</p>`,
      opts: [R`\(\dfrac{Y_1+Y_2}{2}\)`, R`\(\dfrac{Y_1Y_2}{Y_1+Y_2}\)`, R`\(\sqrt{Y_1Y_2}\)`, R`\(\dfrac{2Y_1Y_2}{Y_1+Y_2}\)`],
      ans: 3,
      sol: R`<ol class="steps">
        <li>In series, the same force \(F\) acts in both wires. Total extension \(= \dfrac{FL}{AY_1} + \dfrac{FL}{AY_2}\).</li>
        <li>For the equivalent wire: \(\dfrac{F(2L)}{AY} = \dfrac{FL}{A}\left(\dfrac1{Y_1}+\dfrac1{Y_2}\right)\).</li>
        <li>\(\dfrac{2}{Y} = \dfrac{1}{Y_1}+\dfrac{1}{Y_2} \Rightarrow Y = \dfrac{2Y_1Y_2}{Y_1+Y_2}\).</li></ol>`,
      key: R`Wire = spring with \(k = YA/L\). Series: add \(1/k\). Parallel: add \(k\).` },

    { topic: 'youngs', type: 'numerical',
      q: R`<p>In a Searle's-type experiment, a wire 2 m long and 0.5 mm in diameter extends by 0.8 mm when a 2 kg load is added. Young's modulus of the wire is about \((g = 9.8\ \text{m s}^{-2})\)</p>`,
      opts: [R`\(6.2\times10^{10}\ \text{N m}^{-2}\)`, R`\(1.25\times10^{11}\ \text{N m}^{-2}\)`, R`\(2.5\times10^{11}\ \text{N m}^{-2}\)`, R`\(2.5\times10^{8}\ \text{N m}^{-2}\)`],
      ans: 2,
      sol: R`<ol class="steps">
        <li>\(r = 0.25\ \text{mm} = 2.5\times10^{-4}\ \text{m}\), so \(A = \pi r^2 = 1.96\times10^{-7}\ \text{m}^2\).</li>
        <li>\(F = 2\times9.8 = 19.6\ \text{N}\); \(\Delta L = 8\times10^{-4}\ \text{m}\).</li>
        <li>\(Y = \dfrac{FL}{A\,\Delta L} = \dfrac{19.6\times2}{1.96\times10^{-7}\times8\times10^{-4}} \approx 2.5\times10^{11}\ \text{N m}^{-2}\).</li></ol>`,
      trap: R`Using 0.5 mm as the radius gives \(6.2\times10^{10}\). Leaving \(\Delta L\) in mm gives \(2.5\times10^{8}\).` },

    { topic: 'youngs', type: 'numerical',
      q: R`<p>A steel wire of length 2 m and cross-sectional area 1 mm² \((Y = 2\times10^{11}\ \text{N m}^{-2})\) behaves like a spring. Its force constant is</p>`,
      opts: [R`\(1\times10^{5}\ \text{N m}^{-1}\)`, R`\(2\times10^{5}\ \text{N m}^{-1}\)`, R`\(4\times10^{5}\ \text{N m}^{-1}\)`, R`\(1\times10^{11}\ \text{N m}^{-1}\)`],
      ans: 0,
      sol: R`<ol class="steps">
        <li>\(F = \dfrac{YA}{L}\,\Delta L\) has the form \(F = k\,\Delta L\), so \(k = \dfrac{YA}{L}\).</li>
        <li>\(k = \dfrac{2\times10^{11}\times10^{-6}}{2} = 1\times10^{5}\ \text{N m}^{-1}\).</li>
        <li>For example, a 10 kg load (98 N) would stretch it by \(98/10^{5} \approx 0.98\ \text{mm}\).</li></ol>`,
      trap: R`1 mm² \(= 10^{-6}\ \text{m}^2\), not \(10^{-3}\).` },

    { topic: 'youngs', type: 'numerical',
      q: R`<p>Wires P and Q are made of the same material. Their lengths are in the ratio 1 : 2 and their diameters in the ratio 1 : 2. When the same load is hung from each, the ratio of their extensions \(\Delta L_P : \Delta L_Q\) is</p>`,
      opts: ['1 : 2', '2 : 1', '1 : 4', '1 : 8'],
      ans: 1,
      sol: R`<ol class="steps">
        <li>\(\Delta L = \dfrac{FL}{AY} = \dfrac{4FL}{\pi d^{2}Y} \Rightarrow \Delta L \propto \dfrac{L}{d^{2}}\).</li>
        <li>\(\dfrac{\Delta L_P}{\Delta L_Q} = \dfrac{L_P}{L_Q}\cdot\left(\dfrac{d_Q}{d_P}\right)^{2} = \dfrac12\times 4 = 2\).</li></ol>`,
      trap: 'Square the diameter ratio. Using d instead of d² gives 1 : 1.' },

    { topic: 'youngs', type: 'concept',
      q: R`<p>A wire of Young's modulus \(Y\) is replaced by a wire of the same material with double the length and the same cross-section. Its Young's modulus becomes</p>`,
      opts: [R`\(Y/2\)`, R`\(Y\)`, R`\(2Y\)`, R`\(4Y\)`],
      ans: 1,
      sol: R`<ol class="steps">
        <li>\(Y\) is a property of the <strong>material</strong> (it depends on interatomic forces), not of the wire's dimensions.</li>
        <li>Doubling \(L\) doubles the <em>extension</em> for the same load, but strain \(\Delta L/L\) stays the same, so \(Y\) stays the same.</li></ol>
        <p class="why-opts">\(Y/2\), \(2Y\) and \(4Y\) all wrongly treat \(Y\) as depending on size. What does change is the spring constant \(k = YA/L\), which halves.</p>`,
      key: 'Y, G, B change with material (and temperature), never with L, A or load.' },

    /* ---------------- shear ---------------- */
    { topic: 'shear', type: 'numerical',
      q: R`<p>A cube of side 10 cm has its lower face fixed. A tangential force of 100 N on the upper face shifts it by 0.02 cm relative to the lower face. The modulus of rigidity of the material is</p>`,
      opts: [R`\(2.5\times10^{6}\ \text{N m}^{-2}\)`, R`\(5\times10^{6}\ \text{N m}^{-2}\)`, R`\(5\times10^{8}\ \text{N m}^{-2}\)`, R`\(1\times10^{4}\ \text{N m}^{-2}\)`],
      ans: 1,
      sol: R`<ol class="steps">
        <li>Shear stress \(= F/A = 100/(0.1\times0.1) = 10^{4}\ \text{N m}^{-2}\).</li>
        <li>Shear strain \(\theta = \Delta x/L = 0.02/10 = 2\times10^{-3}\).</li>
        <li>\(G = \dfrac{10^{4}}{2\times10^{-3}} = 5\times10^{6}\ \text{N m}^{-2}\).</li></ol>`,
      trap: R`\(10^{4}\ \text{N m}^{-2}\) is only the stress. Divide by the strain to get \(G\).` },

    { topic: 'shear', type: 'concept',
      q: R`<p>Which of the following has a shear modulus equal to zero?</p>`,
      opts: ['Steel', 'Glass', 'Water', 'Wood'],
      ans: 2,
      sol: R`<ol class="steps">
        <li>A fluid cannot resist a steady tangential force; it keeps flowing. No restoring force means \(G = 0\).</li>
        <li>Liquids and gases therefore have <strong>only a bulk modulus</strong>. They have no \(Y\) or \(G\).</li></ol>
        <p class="why-opts">Steel (\(G \approx 8.4\times10^{10}\) Pa), glass (\(2.3\times10^{10}\)) and wood (\(\sim10^{10}\)) are solids that do resist shear.</p>`,
      key: 'Fluids: only B. Solids: Y, G and B. For most solids G ≈ Y/3.' },

    { topic: 'shear', type: 'numerical',
      q: R`<p>A rubber block has a square top face of side 10 cm and a height of 5 cm. Its bottom is glued to a table. A horizontal force of 400 N acts on the top face. If \(G_\text{rubber} = 2\times10^{6}\ \text{N m}^{-2}\), the top face moves sideways by</p>`,
      opts: ['1 mm', '2 mm', '0.5 mm', '0.2 mm'],
      ans: 0,
      sol: R`<ol class="steps">
        <li>The force acts on the top face, so \(A = 0.1\times0.1 = 10^{-2}\ \text{m}^2\).</li>
        <li>\(\theta = \dfrac{F}{AG} = \dfrac{400}{10^{-2}\times2\times10^{6}} = 0.02\ \text{rad}\).</li>
        <li>\(\Delta x = \theta \times h = 0.02\times0.05\ \text{m} = 1\ \text{mm}\). Here \(h\) is the height, the distance between the fixed face and the moving face.</li></ol>`,
      trap: 'In Δx = Lθ, L is the height between the two faces (5 cm), not the side of the face (10 cm). Using 10 cm gives 2 mm.' },

    /* ---------------- bulk ---------------- */
    { topic: 'bulk', type: 'numerical',
      q: R`<p>A solid sphere of bulk modulus \(B\) is subjected to a uniform pressure \(p\). The fractional decrease in its radius is</p>`,
      opts: [R`\(\dfrac{p}{B}\)`, R`\(\dfrac{3p}{B}\)`, R`\(\dfrac{p}{3B}\)`, R`\(\dfrac{B}{3p}\)`],
      ans: 2,
      sol: R`<ol class="steps">
        <li>\(\dfrac{\Delta V}{V} = \dfrac{p}{B}\) (magnitude).</li>
        <li>\(V = \tfrac43\pi r^3 \Rightarrow \dfrac{\Delta V}{V} = 3\,\dfrac{\Delta r}{r}\). Fractional changes multiply by the power.</li>
        <li>\(\dfrac{\Delta r}{r} = \dfrac{1}{3}\cdot\dfrac{p}{B} = \dfrac{p}{3B}\).</li></ol>`,
      key: 'Volume strain = 3 × linear strain (sphere or cube). Δr/r = p/3B.' },

    { topic: 'bulk', type: 'numerical',
      q: R`<p>At what depth in the sea will water be compressed by 0.1%? Take \(B_\text{water} = 2.2\times10^{9}\ \text{N m}^{-2}\), density \(10^{3}\ \text{kg m}^{-3}\), \(g = 10\ \text{m s}^{-2}\), and ignore atmospheric pressure.</p>`,
      opts: ['22 m', '220 m', '2.2 km', '22 km'],
      ans: 1,
      sol: R`<ol class="steps">
        <li>Required pressure: \(p = B\,\dfrac{\Delta V}{V} = 2.2\times10^{9}\times10^{-3} = 2.2\times10^{6}\ \text{Pa}\).</li>
        <li>\(p = h\rho g \Rightarrow h = \dfrac{2.2\times10^{6}}{10^{3}\times10} = 220\ \text{m}\).</li></ol>`,
      trap: R`0.1% means \(10^{-3}\), not \(10^{-1}\).` },

    { topic: 'bulk', type: 'statement',
      q: R`<p><strong>Statement I:</strong> Gases are the most compressible and solids the least compressible.</p>
        <p><strong>Statement II:</strong> Bulk modulus of water is about \(2.2\times10^{9}\) Pa and that of steel about \(1.6\times10^{11}\) Pa, so water is roughly 70 times more compressible than steel.</p>`,
      opts: ST, ans: 0,
      sol: R`<ol class="steps">
        <li>Typical bulk moduli: solids \(\sim10^{10}\text{–}10^{11}\) Pa, liquids \(\sim10^{9}\) Pa, air \(\sim10^{5}\) Pa. Compressibility \(=1/B\) is largest for gases. Statement I is true.</li>
        <li>\(\dfrac{k_\text{water}}{k_\text{steel}} = \dfrac{B_\text{steel}}{B_\text{water}} = \dfrac{1.6\times10^{11}}{2.2\times10^{9}} \approx 73\). Statement II is true.</li></ol>` },

    /* ---------------- Poisson's ratio ---------------- */
    { topic: 'poisson', type: 'numerical',
      q: R`<p>A wire is stretched so that its longitudinal strain is \(2\times10^{-3}\). If Poisson's ratio of the material is 0.25, the percentage change in its volume is about</p>`,
      opts: ['0.1% increase', '0.1% decrease', '0.05% increase', '0.2% increase'],
      ans: 0,
      sol: R`<ol class="steps">
        <li>\(V = \tfrac{\pi}{4}d^2 L \Rightarrow \dfrac{\Delta V}{V} = \dfrac{\Delta L}{L} + 2\dfrac{\Delta d}{d}\).</li>
        <li>\(\dfrac{\Delta d}{d} = -\sigma\dfrac{\Delta L}{L}\), so \(\dfrac{\Delta V}{V} = (1-2\sigma)\dfrac{\Delta L}{L}\).</li>
        <li>\(= (1-0.5)\times2\times10^{-3} = 1\times10^{-3} = 0.1\%\) <strong>increase</strong>.</li></ol>`,
      key: R`\(\Delta V/V = (1-2\sigma)\,\varepsilon\). It is zero only when \(\sigma = 0.5\).` },

    { topic: 'poisson', type: 'concept',
      q: R`<p>When a certain material is stretched, its volume does not change at all. Its Poisson's ratio is</p>`,
      opts: ['0', '0.25', '0.5', '1'],
      ans: 2,
      sol: R`<ol class="steps">
        <li>\(\dfrac{\Delta V}{V} = (1-2\sigma)\dfrac{\Delta L}{L} = 0\) for a non-zero stretch \(\Rightarrow 1-2\sigma = 0 \Rightarrow \sigma = 0.5\).</li>
        <li>Rubber is close to this (\(\sigma \approx 0.49\)).</li></ol>
        <p class="why-opts">\(\sigma = 0\) means the wire does not get thinner at all, so its volume <em>increases</em> by the full strain. \(\sigma = 0.25\) gives a volume increase of half the strain. \(\sigma = 1\) is impossible for a stable isotropic material (the upper limit is 0.5).</p>`,
      key: 'Practical range of σ: 0 to 0.5 (theory allows −1 to 0.5). Incompressible: σ = 0.5.' },

    { topic: 'poisson', type: 'ar',
      q: R`<div class="ar"><p><strong>Assertion (A):</strong> When a metal wire is stretched, its volume increases slightly.</p>
        <p><strong>Reason (R):</strong> For metals, Poisson's ratio is less than 0.5, so \((1-2\sigma)\) is positive.</p></div>`,
      opts: AR, ans: 0,
      sol: R`<ol class="steps">
        <li>\(\Delta V/V = (1-2\sigma)\varepsilon\). For steel \(\sigma \approx 0.3\), so \(\Delta V/V \approx 0.4\varepsilon &gt; 0\). A is true.</li>
        <li>R is true, and it is exactly the reason \(\Delta V\) is positive. So option 1.</li></ol>` },

    /* ---------------- elastic energy ---------------- */
    { topic: 'energy', type: 'numerical',
      q: R`<p>A mass \(M\) is hung from a wire and produces an extension \(l\) (within the elastic limit). The elastic potential energy stored in the wire is</p>`,
      opts: [R`\(Mgl\)`, R`\(\dfrac{Mgl}{2}\)`, R`\(2Mgl\)`, R`\(\dfrac{Mgl}{4}\)`],
      ans: 1,
      sol: R`<ol class="steps">
        <li>The restoring force grows linearly from 0 to \(Mg\) as the extension goes from 0 to \(l\).</li>
        <li>\(U = \) area under the force–extension line \(= \tfrac12 \times Mg \times l\).</li>
        <li>Gravity does work \(Mgl\). The other half is lost as heat (the mass overshoots and the oscillation dies out) or is taken by the hand that lowers it slowly.</li></ol>`,
      trap: R`\(Mgl\) is the work done by gravity, not the energy stored. Stored energy \(= \tfrac12 F\,\Delta l\).` },

    { topic: 'energy', type: 'numerical',
      q: R`<p>A steel wire \((Y = 2\times10^{11}\ \text{N m}^{-2})\) is stretched to a strain of \(10^{-3}\). The elastic energy stored per unit volume is</p>`,
      opts: [R`\(1\times10^{5}\ \text{J m}^{-3}\)`, R`\(2\times10^{5}\ \text{J m}^{-3}\)`, R`\(1\times10^{8}\ \text{J m}^{-3}\)`, R`\(2\times10^{8}\ \text{J m}^{-3}\)`],
      ans: 0,
      sol: R`<ol class="steps">
        <li>\(u = \tfrac12\,\text{stress}\times\text{strain} = \tfrac12 Y\varepsilon^{2}\).</li>
        <li>\(u = \tfrac12\times2\times10^{11}\times(10^{-3})^{2} = 1\times10^{5}\ \text{J m}^{-3}\).</li></ol>`,
      trap: R`\(2\times10^{5}\) forgets the ½. \(2\times10^{8}\) is the stress, not an energy density.` },

    { topic: 'energy', type: 'ar',
      q: R`<div class="ar"><p><strong>Assertion (A):</strong> When a mass \(M\) hung from a wire produces an extension \(l\), the energy stored in the wire is only \(Mgl/2\).</p>
        <p><strong>Reason (R):</strong> The restoring force in the wire increases linearly from zero to \(Mg\), so the average force during stretching is \(Mg/2\).</p></div>`,
      opts: AR, ans: 0,
      sol: R`<ol class="steps">
        <li>A is true (area of the triangle under the \(F\)–\(\Delta l\) graph).</li>
        <li>R is true and is the reason: work done against a force that grows linearly = average force × extension = \(\tfrac{Mg}{2}\,l\).</li></ol>` },

    /* ---------------- thermal stress ---------------- */
    { topic: 'thermal', type: 'numerical',
      q: R`<p>A steel rod is clamped between two rigid walls at 20 °C. It is heated to 70 °C. If \(Y = 2\times10^{11}\ \text{N m}^{-2}\) and \(\alpha = 1.2\times10^{-5}\ ^\circ\text{C}^{-1}\), the thermal stress developed is</p>`,
      opts: [R`\(1.2\times10^{6}\ \text{N m}^{-2}\)`, R`\(2.4\times10^{8}\ \text{N m}^{-2}\)`, R`\(6\times10^{7}\ \text{N m}^{-2}\)`, R`\(1.2\times10^{8}\ \text{N m}^{-2}\)`],
      ans: 3,
      sol: R`<ol class="steps">
        <li>If the rod were free, it would expand by \(L\alpha\Delta T\). The walls push it back by exactly this amount, so the compressive strain is \(\alpha\Delta T\).</li>
        <li>Stress \(= Y\alpha\Delta T = 2\times10^{11}\times1.2\times10^{-5}\times50 = 1.2\times10^{8}\ \text{N m}^{-2}\) (compressive).</li></ol>`,
      key: R`Thermal stress \(= Y\alpha\Delta T\); thermal force \(= YA\alpha\Delta T\). Neither depends on the length.` },

    { topic: 'thermal', type: 'concept',
      q: R`<p>A rod clamped between rigid supports is heated through \(\Delta T\) and the force on the supports is \(F\). A second rod of the same material and cross-section, but twice as long, is heated through the same \(\Delta T\). The force on its supports is</p>`,
      opts: [R`\(2F\)`, R`\(F/2\)`, R`\(F\)`, R`\(4F\)`],
      ans: 2,
      sol: R`<ol class="steps">
        <li>Prevented expansion \(= L\alpha\Delta T\), so strain \(= \alpha\Delta T\). The length cancels.</li>
        <li>\(F = YA\alpha\Delta T\) has no \(L\) in it, so the force is still \(F\).</li></ol>
        <p class="why-opts">\(2F\) assumes a longer rod pushes harder. It does expand twice as much, but it also has twice the length to share the compression, so the strain is unchanged. \(F/2\) and \(4F\) have no basis.</p>` },

    /* ---------------- applications ---------------- */
    { topic: 'applications', type: 'numerical',
      q: R`<p>The elastic limit of a typical rock is about \(3\times10^{8}\ \text{N m}^{-2}\) and its density is about \(3\times10^{3}\ \text{kg m}^{-3}\). Estimate the maximum possible height of a mountain on Earth \((g = 10\ \text{m s}^{-2})\).</p>`,
      opts: ['1 km', '10 km', '30 km', '100 km'],
      ans: 1,
      sol: R`<ol class="steps">
        <li>The stress at the base is about \(h\rho g\). It must stay below the elastic limit, or the rock at the base flows.</li>
        <li>\(h_\text{max} = \dfrac{3\times10^{8}}{3\times10^{3}\times10} = 10^{4}\ \text{m} = 10\ \text{km}\).</li>
        <li>Mount Everest (about 8.8 km) fits under this limit.</li></ol>` },

    { topic: 'applications', type: 'numerical',
      q: R`<p>A beam of rectangular cross-section is supported at its ends and loaded at the middle. If its breadth is doubled and its depth is halved (same material, same length, same load), the sag at the middle becomes</p>`,
      opts: ['2 times', '1/4 times', '4 times', '16 times'],
      ans: 2,
      sol: R`<ol class="steps">
        <li>\(\delta = \dfrac{W l^{3}}{4 b d^{3} Y} \Rightarrow \delta \propto \dfrac{1}{b\,d^{3}}\).</li>
        <li>New \(b d^3 = (2b)(d/2)^3 = \dfrac{b d^3}{4}\).</li>
        <li>So \(\delta\) becomes \(4\) times. The beam bends <em>more</em> even though it uses the same amount of material.</li></ol>`,
      key: 'Depth matters as d³, breadth only as b. Increase depth, not breadth, to stop bending.' },

    { topic: 'applications', type: 'concept',
      q: R`<p>Steel girders in bridges and buildings are given an I-shaped cross-section mainly because</p>`,
      opts: [
        'it increases the breadth b, which reduces bending the most',
        R`it gives a large depth (bending \(\propto 1/d^{3}\)) with much less material, so the beam is stiff but light`,
        'it increases the Young\'s modulus of steel',
        'it reduces the length of the beam',
      ],
      ans: 1,
      sol: R`<ol class="steps">
        <li>Sag \(\delta \propto 1/(b d^{3})\): depth is by far the most effective dimension.</li>
        <li>An I-section puts metal in the top and bottom flanges, far from the middle, joined by a thin web. This gives the stiffness of a deep beam with much less weight. The flanges also give a wide load-bearing surface.</li></ol>
        <p class="why-opts">Option 1: breadth enters only to the first power. Option 3: \(Y\) depends on the material, not the shape. Option 4: the shape of the cross-section does not change the span.</p>` },
  ];

  list.forEach((q, i) => {
    q.qno = i + 1;
    q.id = 'xs-' + String(i + 1).padStart(2, '0');
    q.src = 'xs';
    window.QBANK.push(q);
  });
})();
