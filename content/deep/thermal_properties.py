"""Deepening layer: Thermal Properties of Matter (chapter key 'thermal-properties').

Adds derivations, exam notes, figures, worked examples and practice MCQs to the
existing sections, plus new sections on thermal stress, mixing problems and the
radiation laws. Every number was checked with a short Python calculation.
"""

_FIGS = {
    'bimetal': '<svg viewBox="0 0 360 215" role="img" aria-label="Bimetallic strip straight before heating and curved after heating with brass on the outer side"><text x="20" y="20" font-size="12" style="fill:var(--ink-2)">Before heating (room temperature)</text><rect x="60" y="32" width="240" height="7" style="fill:var(--amber-soft);stroke:var(--ink-2);stroke-width:1"/><rect x="60" y="39" width="240" height="7" style="fill:var(--indigo-soft);stroke:var(--ink-2);stroke-width:1"/><text x="306" y="40" font-size="11" style="fill:var(--muted)">brass</text><text x="306" y="51" font-size="11" style="fill:var(--muted)">steel</text><text x="20" y="82" font-size="12" style="fill:var(--ink-2)">After heating: bends towards steel</text><path d="M57.0 140.0 A263.5 263.5 0 0 1 303.0 140.0 L300.0 145.7 A257 257 0 0 0 60.0 145.7 Z" style="fill:var(--amber-soft);stroke:var(--ink-2);stroke-width:1"/><path d="M60.0 145.7 A257 257 0 0 1 300.0 145.7 L297.0 151.5 A250.5 250.5 0 0 0 63.0 151.5 Z" style="fill:var(--indigo-soft);stroke:var(--ink-2);stroke-width:1"/><text x="120" y="104" font-size="11" style="fill:var(--muted)">brass: larger α, outer (convex) side</text><text x="112" y="176" font-size="11" style="fill:var(--muted)">steel: smaller α, inner (concave) side</text><text x="20" y="204" font-size="11" style="fill:var(--muted)">On cooling below room temperature it bends the other way.</text></svg>',
    'clamped': '<svg viewBox="0 0 360 165" role="img" aria-label="A free rod expands by delta L; the same rod clamped between rigid walls is pushed back by the walls"><text x="20" y="18" font-size="12" style="fill:var(--ink-2)">Free rod: expands by ΔL = LαΔθ</text><rect x="50" y="28" width="240" height="14" style="fill:var(--indigo-soft);stroke:var(--ink-2);stroke-width:1"/><rect x="290" y="28" width="30" height="14" style="fill:none;stroke:var(--coral);stroke-width:1.2;stroke-dasharray:4 3"/><text x="296" y="58" font-size="11" style="fill:var(--coral)">ΔL</text><text x="20" y="80" font-size="12" style="fill:var(--ink-2)">Clamped rod: walls push it back by ΔL</text><rect x="34" y="90" width="16" height="64" style="fill:var(--amber-soft);stroke:var(--ink-2);stroke-width:1"/><rect x="290" y="90" width="16" height="64" style="fill:var(--amber-soft);stroke:var(--ink-2);stroke-width:1"/><rect x="50" y="115" width="240" height="14" style="fill:var(--indigo-soft);stroke:var(--ink-2);stroke-width:1"/><line x1="54" y1="104" x2="94" y2="104" style="stroke:var(--coral);stroke-width:1.6"/><polygon points="94.0,104.0 87.0,107.5 87.0,100.5" style="fill:var(--coral)"/><line x1="286" y1="104" x2="246" y2="104" style="stroke:var(--coral);stroke-width:1.6"/><polygon points="246.0,104.0 253.0,100.5 253.0,107.5" style="fill:var(--coral)"/><text x="98" y="108" font-size="12" style="fill:var(--coral)">F</text><text x="232" y="108" font-size="12" style="fill:var(--coral)">F</text><text x="70" y="146" font-size="11" style="fill:var(--muted)">strain = αΔθ, stress = YαΔθ, F = YAαΔθ</text></svg>',
    'water': '<svg viewBox="0 0 340 205" role="img" aria-label="Volume of a fixed mass of water against temperature from 0 to 10 degrees Celsius, with a minimum at 4 degrees"><line x1="55" y1="165" x2="325" y2="165" style="fill:none;stroke:var(--ink-2);stroke-width:1.4"/><line x1="55" y1="165" x2="55" y2="20" style="fill:none;stroke:var(--ink-2);stroke-width:1.4"/><path d="M55.0 98.0 L57.6 100.6 L60.2 103.0 L62.8 105.4 L65.4 107.7 L68.0 110.0 L70.6 112.1 L73.2 114.3 L75.8 116.3 L78.4 118.3 L81.0 120.2 L83.6 122.1 L86.2 123.9 L88.8 125.6 L91.4 127.3 L94.0 128.9 L96.6 130.4 L99.2 131.9 L101.8 133.3 L104.4 134.6 L107.0 135.9 L109.6 137.1 L112.2 138.2 L114.8 139.3 L117.4 140.4 L120.0 141.3 L122.6 142.2 L125.2 143.0 L127.8 143.8 L130.4 144.5 L133.0 145.2 L135.6 145.7 L138.2 146.3 L140.8 146.7 L143.4 147.1 L146.0 147.5 L148.6 147.7 L151.2 147.9 L153.8 148.1 L156.4 148.2 L159.0 148.2 L161.6 148.2 L164.2 148.1 L166.8 147.9 L169.4 147.7 L172.0 147.4 L174.6 147.1 L177.2 146.7 L179.8 146.2 L182.4 145.7 L185.0 145.1 L187.6 144.5 L190.2 143.8 L192.8 143.0 L195.4 142.2 L198.0 141.3 L200.6 140.4 L203.2 139.4 L205.8 138.4 L208.4 137.2 L211.0 136.1 L213.6 134.8 L216.2 133.6 L218.8 132.2 L221.4 130.8 L224.0 129.3 L226.6 127.8 L229.2 126.3 L231.8 124.6 L234.4 122.9 L237.0 121.2 L239.6 119.4 L242.2 117.5 L244.8 115.6 L247.4 113.6 L250.0 111.6 L252.6 109.5 L255.2 107.4 L257.8 105.2 L260.4 102.9 L263.0 100.6 L265.6 98.2 L268.2 95.8 L270.8 93.3 L273.4 90.8 L276.0 88.2 L278.6 85.5 L281.2 82.8 L283.8 80.1 L286.4 77.3 L289.0 74.4 L291.6 71.5 L294.2 68.5 L296.8 65.5 L299.4 62.4 L302.0 59.3 L304.6 56.1 L307.2 52.9 L309.8 49.6 L312.4 46.2 L315.0 42.8" style="fill:none;stroke:var(--water);stroke-width:2.2"/><line x1="159.0" y1="165" x2="159.0" y2="148.2" style="stroke:var(--coral);stroke-width:1.2;stroke-dasharray:4 3"/><circle cx="159.0" cy="148.2" r="3.5" style="fill:var(--coral)"/><text x="51.0" y="180" font-size="11" style="fill:var(--muted)">0</text><text x="103.0" y="180" font-size="11" style="fill:var(--muted)">2</text><text x="155.0" y="180" font-size="11" style="fill:var(--muted)">4</text><text x="207.0" y="180" font-size="11" style="fill:var(--muted)">6</text><text x="259.0" y="180" font-size="11" style="fill:var(--muted)">8</text><text x="311.0" y="180" font-size="11" style="fill:var(--muted)">10</text><text x="150" y="198" font-size="12" style="fill:var(--ink-2)">Temperature (°C)</text><text x="14" y="14" font-size="12" style="fill:var(--ink-2)">Volume of 1 kg of water</text><text x="119.0" y="114.2" font-size="11" style="fill:var(--coral)">minimum volume</text><text x="119.0" y="128.2" font-size="11" style="fill:var(--coral)">maximum density</text><text x="64" y="44" font-size="11" style="fill:var(--muted)">contracts on warming</text><text x="232" y="44" font-size="11" style="fill:var(--muted)">normal expansion</text></svg>',
    'heating': '<svg viewBox="0 0 420 215" role="img" aria-label="Heating curve of water from ice at minus 20 degrees to steam at 120 degrees with flat melting and boiling plateaus"><line x1="50" y1="178" x2="410" y2="178" style="fill:none;stroke:var(--ink-2);stroke-width:1.4"/><line x1="50" y1="178" x2="50" y2="15" style="fill:none;stroke:var(--ink-2);stroke-width:1.4"/><line x1="50" y1="150.0" x2="140" y2="150.0" style="stroke:var(--line-2);stroke-width:1;stroke-dasharray:3 3"/><line x1="50" y1="50.0" x2="240" y2="50.0" style="stroke:var(--line-2);stroke-width:1;stroke-dasharray:3 3"/><path d="M50.0 170.0 L60.0 150.0 L140.0 150.0 L240.0 50.0 L300.0 50.0" style="fill:none;stroke:var(--coral);stroke-width:2.4"/><path d="M320.0 50.0 L380.0 50.0 L390.0 30.0" style="fill:none;stroke:var(--coral);stroke-width:2.4"/><line x1="300" y1="44.0" x2="306" y2="56.0" style="stroke:var(--ink-2);stroke-width:1.4"/><line x1="314" y1="44.0" x2="320" y2="56.0" style="stroke:var(--ink-2);stroke-width:1.4"/><text x="28" y="154.0" font-size="11" style="fill:var(--muted)">0</text><text x="22" y="54.0" font-size="11" style="fill:var(--muted)">100</text><text x="20" y="174.0" font-size="11" style="fill:var(--muted)">−20</text><text x="8" y="12" font-size="12" style="fill:var(--ink-2)">T (°C)</text><text x="300" y="200" font-size="12" style="fill:var(--ink-2)">heat supplied Q →</text><text x="64" y="142.0" font-size="11" style="fill:var(--muted)">ice + water</text><text x="94" y="166.0" font-size="11" style="fill:var(--muted)">(melting)</text><text x="64" y="164.0" font-size="11" style="fill:var(--muted)">ice</text><text x="196" y="100.0" font-size="11" style="fill:var(--muted)">water</text><text x="250" y="68.0" font-size="11" style="fill:var(--muted)">water + steam (boiling)</text><text x="340" y="34.0" font-size="11" style="fill:var(--muted)">steam</text><text x="66" y="200" font-size="11" style="fill:var(--muted)">plateau ∝ L, slope ∝ 1/(mc)</text></svg>',
    'slab': '<svg viewBox="0 0 360 215" role="img" aria-label="Two slabs in series with conductivities 3k and k; temperature falls 25 degrees across the first and 75 degrees across the second"><rect x="70" y="40" width="110" height="130" style="fill:var(--coral-soft);stroke:var(--ink-2);stroke-width:1"/><rect x="180" y="40" width="110" height="130" style="fill:var(--water-soft);stroke:var(--ink-2);stroke-width:1"/><path d="M70.0 45.0 L180.0 73.8 L290.0 160.0" style="fill:none;stroke:var(--ink);stroke-width:2.2"/><circle cx="70" cy="45.0" r="3.5" style="fill:var(--ink)"/><circle cx="180" cy="73.8" r="3.5" style="fill:var(--ink)"/><circle cx="290" cy="160.0" r="3.5" style="fill:var(--ink)"/><text x="22" y="49.0" font-size="12" style="fill:var(--ink-2)">100 °C</text><text x="186" y="67.8" font-size="12" style="fill:var(--ink-2)">75 °C</text><text x="298" y="164.0" font-size="12" style="fill:var(--ink-2)">0 °C</text><text x="100" y="186" font-size="12" style="fill:var(--ink-2)">κ₁ = 3κ</text><text x="216" y="186" font-size="12" style="fill:var(--ink-2)">κ₂ = κ</text><text x="96" y="30" font-size="11" style="fill:var(--muted)">small drop</text><text x="200" y="30" font-size="11" style="fill:var(--muted)">large drop</text><line x1="130" y1="203" x2="230" y2="203" style="stroke:var(--coral);stroke-width:1.6"/><polygon points="230.0,203.0 223.0,206.5 223.0,199.5" style="fill:var(--coral)"/><text x="240" y="207" font-size="11" style="fill:var(--coral)">same H through both</text></svg>',
    'breeze': '<svg viewBox="0 0 360 200" role="img" aria-label="Sea breeze by day: warm air rises over land, flows to the sea aloft, sinks over the sea and returns to land along the surface"><rect x="20" y="150" width="160" height="35" style="fill:var(--water-soft);stroke:var(--water);stroke-width:1"/><rect x="180" y="140" width="160" height="45" style="fill:var(--amber-soft);stroke:var(--amber);stroke-width:1"/><text x="70" y="172" font-size="12" style="fill:var(--ink-2)">Sea (cooler)</text><text x="216" y="166" font-size="12" style="fill:var(--ink-2)">Land (hotter)</text><circle cx="320" cy="30" r="14" style="fill:var(--amber);stroke:none"/><path d="M100 135 C 100 60, 120 50, 160 50 L 220 50 C 260 50, 260 70, 260 125" style="fill:none;stroke:var(--coral);stroke-width:1.8;stroke-dasharray:5 3"/><line x1="260" y1="90" x2="260" y2="62" style="stroke:var(--coral);stroke-width:1.6"/><polygon points="260.0,62.0 263.5,69.0 256.5,69.0" style="fill:var(--coral)"/><line x1="200" y1="50" x2="150" y2="50" style="stroke:var(--coral);stroke-width:1.6"/><polygon points="150.0,50.0 157.0,46.5 157.0,53.5" style="fill:var(--coral)"/><line x1="100" y1="70" x2="100" y2="110" style="stroke:var(--water);stroke-width:1.6"/><polygon points="100.0,110.0 96.5,103.0 103.5,103.0" style="fill:var(--water)"/><line x1="120" y1="138" x2="230" y2="128" style="stroke:var(--water);stroke-width:1.6"/><polygon points="230.0,128.0 223.3,132.1 222.7,125.1" style="fill:var(--water)"/><text x="266" y="104" font-size="11" style="fill:var(--muted)">warm air rises</text><text x="150" y="40" font-size="11" style="fill:var(--muted)">returns aloft</text><text x="26" y="94" font-size="11" style="fill:var(--muted)">cool air sinks</text><text x="128" y="122" font-size="11" style="fill:var(--water)">sea breeze</text></svg>',
    'bb': '<svg viewBox="0 0 360 215" role="img" aria-label="Black-body spectra at 5000 K and 4000 K; the hotter curve is higher everywhere and peaks at a shorter wavelength"><rect x="86.8" y="25" width="27.6" height="145" style="fill:var(--plum-soft);stroke:none"/><text x="88.8" y="22" font-size="11" style="fill:var(--plum)">visible</text><line x1="50" y1="170" x2="340" y2="170" style="fill:none;stroke:var(--ink-2);stroke-width:1.4"/><line x1="50" y1="170" x2="50" y2="15" style="fill:none;stroke:var(--ink-2);stroke-width:1.4"/><path d="M54.6 170.0 L55.5 170.0 L56.4 170.0 L57.4 170.0 L58.3 170.0 L59.2 170.0 L60.1 170.0 L61.0 170.0 L62.0 170.0 L62.9 170.0 L63.8 169.9 L64.7 169.8 L65.6 169.6 L66.6 169.2 L67.5 168.7 L68.4 167.8 L69.3 166.5 L70.2 164.9 L71.2 162.8 L72.1 160.2 L73.0 157.1 L73.9 153.5 L74.8 149.4 L75.8 144.8 L76.7 139.9 L77.6 134.7 L78.5 129.1 L79.4 123.4 L80.4 117.5 L81.3 111.6 L82.2 105.6 L83.1 99.8 L84.0 94.0 L85.0 88.3 L85.9 82.9 L86.8 77.7 L87.7 72.8 L88.6 68.1 L89.6 63.8 L90.5 59.8 L91.4 56.0 L92.3 52.6 L93.2 49.6 L94.2 46.8 L95.1 44.4 L96.0 42.3 L96.9 40.4 L97.8 38.9 L98.8 37.6 L99.7 36.6 L100.6 35.9 L101.5 35.4 L102.4 35.1 L103.4 35.0 L104.3 35.1 L105.2 35.4 L106.1 35.8 L107.0 36.4 L108.0 37.2 L108.9 38.1 L109.8 39.1 L110.7 40.2 L111.6 41.4 L112.6 42.6 L113.5 44.0 L114.4 45.4 L115.3 46.9 L116.2 48.5 L117.2 50.1 L118.1 51.7 L119.0 53.4 L119.9 55.0 L120.8 56.8 L121.8 58.5 L122.7 60.2 L123.6 62.0 L124.5 63.8 L125.4 65.5 L126.4 67.3 L127.3 69.0 L128.2 70.8 L129.1 72.5 L130.0 74.3 L131.0 76.0 L131.9 77.7 L132.8 79.4 L133.7 81.0 L134.6 82.7 L135.6 84.3 L136.5 85.9 L137.4 87.5 L138.3 89.1 L139.2 90.6 L140.2 92.2 L141.1 93.7 L142.0 95.1 L142.9 96.6 L143.8 98.0 L144.8 99.4 L145.7 100.8 L146.6 102.1 L147.5 103.5 L148.4 104.8 L149.4 106.0 L150.3 107.3 L151.2 108.5 L152.1 109.7 L153.0 110.9 L154.0 112.1 L154.9 113.2 L155.8 114.3 L156.7 115.4 L157.6 116.5 L158.6 117.5 L159.5 118.5 L160.4 119.5 L161.3 120.5 L162.2 121.5 L163.2 122.4 L164.1 123.4 L165.0 124.3 L165.9 125.1 L166.8 126.0 L167.8 126.9 L168.7 127.7 L169.6 128.5 L170.5 129.3 L171.4 130.1 L172.4 130.8 L173.3 131.6 L174.2 132.3 L175.1 133.0 L176.0 133.7 L177.0 134.4 L177.9 135.1 L178.8 135.7 L179.7 136.4 L180.6 137.0 L181.6 137.6 L182.5 138.2 L183.4 138.8 L184.3 139.4 L185.2 139.9 L186.2 140.5 L187.1 141.0 L188.0 141.5 L188.9 142.1 L189.8 142.6 L190.8 143.1 L191.7 143.5 L192.6 144.0 L193.5 144.5 L194.4 144.9 L195.4 145.4 L196.3 145.8 L197.2 146.2 L198.1 146.7 L199.0 147.1 L200.0 147.5 L200.9 147.9 L201.8 148.3 L202.7 148.6 L203.6 149.0 L204.6 149.4 L205.5 149.7 L206.4 150.1 L207.3 150.4 L208.2 150.7 L209.2 151.1 L210.1 151.4 L211.0 151.7 L211.9 152.0 L212.8 152.3 L213.8 152.6 L214.7 152.9 L215.6 153.2 L216.5 153.4 L217.4 153.7 L218.4 154.0 L219.3 154.2 L220.2 154.5 L221.1 154.7 L222.0 155.0 L223.0 155.2 L223.9 155.5 L224.8 155.7 L225.7 155.9 L226.6 156.2 L227.6 156.4 L228.5 156.6 L229.4 156.8 L230.3 157.0 L231.2 157.2 L232.2 157.4 L233.1 157.6 L234.0 157.8 L234.9 158.0 L235.8 158.2 L236.8 158.4 L237.7 158.5 L238.6 158.7 L239.5 158.9 L240.4 159.0 L241.4 159.2 L242.3 159.4 L243.2 159.5 L244.1 159.7 L245.0 159.8 L246.0 160.0 L246.9 160.1 L247.8 160.3 L248.7 160.4 L249.6 160.6 L250.6 160.7 L251.5 160.8 L252.4 161.0 L253.3 161.1 L254.2 161.2 L255.2 161.4 L256.1 161.5 L257.0 161.6 L257.9 161.7 L258.8 161.8 L259.8 162.0 L260.7 162.1 L261.6 162.2 L262.5 162.3 L263.4 162.4 L264.4 162.5 L265.3 162.6 L266.2 162.7 L267.1 162.8 L268.0 162.9 L269.0 163.0 L269.9 163.1 L270.8 163.2 L271.7 163.3 L272.6 163.4 L273.6 163.5 L274.5 163.6 L275.4 163.6 L276.3 163.7 L277.2 163.8 L278.2 163.9 L279.1 164.0 L280.0 164.1 L280.9 164.1 L281.8 164.2 L282.8 164.3 L283.7 164.4 L284.6 164.4 L285.5 164.5 L286.4 164.6 L287.4 164.6 L288.3 164.7 L289.2 164.8 L290.1 164.8 L291.0 164.9 L292.0 165.0 L292.9 165.0 L293.8 165.1 L294.7 165.2 L295.6 165.2 L296.6 165.3 L297.5 165.3 L298.4 165.4 L299.3 165.5 L300.2 165.5 L301.2 165.6 L302.1 165.6 L303.0 165.7 L303.9 165.7 L304.8 165.8 L305.8 165.8 L306.7 165.9 L307.6 165.9 L308.5 166.0 L309.4 166.0 L310.4 166.1 L311.3 166.1 L312.2 166.2 L313.1 166.2 L314.0 166.3 L315.0 166.3 L315.9 166.4 L316.8 166.4 L317.7 166.4 L318.6 166.5 L319.6 166.5 L320.5 166.6 L321.4 166.6 L322.3 166.6 L323.2 166.7 L324.2 166.7 L325.1 166.8 L326.0 166.8" style="fill:none;stroke:var(--coral);stroke-width:2.2"/><line x1="103.3" y1="170" x2="103.3" y2="35.0" style="stroke:var(--coral);stroke-width:1;stroke-dasharray:3 3"/><path d="M54.6 170.0 L55.5 170.0 L56.4 170.0 L57.4 170.0 L58.3 170.0 L59.2 170.0 L60.1 170.0 L61.0 170.0 L62.0 170.0 L62.9 170.0 L63.8 170.0 L64.7 170.0 L65.6 170.0 L66.6 170.0 L67.5 170.0 L68.4 169.9 L69.3 169.9 L70.2 169.8 L71.2 169.7 L72.1 169.5 L73.0 169.3 L73.9 169.0 L74.8 168.6 L75.8 168.1 L76.7 167.5 L77.6 166.8 L78.5 166.0 L79.4 165.1 L80.4 164.1 L81.3 163.0 L82.2 161.8 L83.1 160.5 L84.0 159.1 L85.0 157.7 L85.9 156.2 L86.8 154.7 L87.7 153.2 L88.6 151.6 L89.6 150.1 L90.5 148.5 L91.4 147.0 L92.3 145.5 L93.2 144.0 L94.2 142.5 L95.1 141.1 L96.0 139.8 L96.9 138.5 L97.8 137.2 L98.8 136.0 L99.7 134.9 L100.6 133.9 L101.5 132.9 L102.4 132.0 L103.4 131.1 L104.3 130.4 L105.2 129.6 L106.1 129.0 L107.0 128.4 L108.0 127.9 L108.9 127.4 L109.8 127.0 L110.7 126.7 L111.6 126.4 L112.6 126.2 L113.5 126.0 L114.4 125.9 L115.3 125.8 L116.2 125.8 L117.2 125.8 L118.1 125.8 L119.0 125.9 L119.9 126.0 L120.8 126.2 L121.8 126.3 L122.7 126.5 L123.6 126.8 L124.5 127.0 L125.4 127.3 L126.4 127.6 L127.3 127.9 L128.2 128.3 L129.1 128.6 L130.0 129.0 L131.0 129.4 L131.9 129.8 L132.8 130.2 L133.7 130.6 L134.6 131.0 L135.6 131.4 L136.5 131.9 L137.4 132.3 L138.3 132.8 L139.2 133.2 L140.2 133.7 L141.1 134.1 L142.0 134.6 L142.9 135.1 L143.8 135.5 L144.8 136.0 L145.7 136.5 L146.6 136.9 L147.5 137.4 L148.4 137.8 L149.4 138.3 L150.3 138.7 L151.2 139.2 L152.1 139.6 L153.0 140.1 L154.0 140.5 L154.9 141.0 L155.8 141.4 L156.7 141.8 L157.6 142.2 L158.6 142.7 L159.5 143.1 L160.4 143.5 L161.3 143.9 L162.2 144.3 L163.2 144.7 L164.1 145.1 L165.0 145.5 L165.9 145.8 L166.8 146.2 L167.8 146.6 L168.7 147.0 L169.6 147.3 L170.5 147.7 L171.4 148.0 L172.4 148.4 L173.3 148.7 L174.2 149.0 L175.1 149.4 L176.0 149.7 L177.0 150.0 L177.9 150.3 L178.8 150.6 L179.7 150.9 L180.6 151.2 L181.6 151.5 L182.5 151.8 L183.4 152.1 L184.3 152.4 L185.2 152.7 L186.2 152.9 L187.1 153.2 L188.0 153.5 L188.9 153.7 L189.8 154.0 L190.8 154.2 L191.7 154.5 L192.6 154.7 L193.5 155.0 L194.4 155.2 L195.4 155.4 L196.3 155.6 L197.2 155.9 L198.1 156.1 L199.0 156.3 L200.0 156.5 L200.9 156.7 L201.8 156.9 L202.7 157.1 L203.6 157.3 L204.6 157.5 L205.5 157.7 L206.4 157.9 L207.3 158.1 L208.2 158.2 L209.2 158.4 L210.1 158.6 L211.0 158.8 L211.9 158.9 L212.8 159.1 L213.8 159.3 L214.7 159.4 L215.6 159.6 L216.5 159.7 L217.4 159.9 L218.4 160.0 L219.3 160.2 L220.2 160.3 L221.1 160.5 L222.0 160.6 L223.0 160.7 L223.9 160.9 L224.8 161.0 L225.7 161.1 L226.6 161.3 L227.6 161.4 L228.5 161.5 L229.4 161.6 L230.3 161.8 L231.2 161.9 L232.2 162.0 L233.1 162.1 L234.0 162.2 L234.9 162.3 L235.8 162.4 L236.8 162.5 L237.7 162.6 L238.6 162.7 L239.5 162.8 L240.4 162.9 L241.4 163.0 L242.3 163.1 L243.2 163.2 L244.1 163.3 L245.0 163.4 L246.0 163.5 L246.9 163.6 L247.8 163.7 L248.7 163.8 L249.6 163.9 L250.6 163.9 L251.5 164.0 L252.4 164.1 L253.3 164.2 L254.2 164.3 L255.2 164.3 L256.1 164.4 L257.0 164.5 L257.9 164.6 L258.8 164.6 L259.8 164.7 L260.7 164.8 L261.6 164.8 L262.5 164.9 L263.4 165.0 L264.4 165.0 L265.3 165.1 L266.2 165.2 L267.1 165.2 L268.0 165.3 L269.0 165.3 L269.9 165.4 L270.8 165.5 L271.7 165.5 L272.6 165.6 L273.6 165.6 L274.5 165.7 L275.4 165.7 L276.3 165.8 L277.2 165.8 L278.2 165.9 L279.1 166.0 L280.0 166.0 L280.9 166.1 L281.8 166.1 L282.8 166.1 L283.7 166.2 L284.6 166.2 L285.5 166.3 L286.4 166.3 L287.4 166.4 L288.3 166.4 L289.2 166.5 L290.1 166.5 L291.0 166.5 L292.0 166.6 L292.9 166.6 L293.8 166.7 L294.7 166.7 L295.6 166.7 L296.6 166.8 L297.5 166.8 L298.4 166.9 L299.3 166.9 L300.2 166.9 L301.2 167.0 L302.1 167.0 L303.0 167.0 L303.9 167.1 L304.8 167.1 L305.8 167.1 L306.7 167.2 L307.6 167.2 L308.5 167.2 L309.4 167.3 L310.4 167.3 L311.3 167.3 L312.2 167.4 L313.1 167.4 L314.0 167.4 L315.0 167.5 L315.9 167.5 L316.8 167.5 L317.7 167.5 L318.6 167.6 L319.6 167.6 L320.5 167.6 L321.4 167.6 L322.3 167.7 L323.2 167.7 L324.2 167.7 L325.1 167.7 L326.0 167.8" style="fill:none;stroke:var(--indigo);stroke-width:2.2"/><line x1="116.7" y1="170" x2="116.7" y2="125.8" style="stroke:var(--indigo);stroke-width:1;stroke-dasharray:3 3"/><text x="47.0" y="184" font-size="11" style="fill:var(--muted)">0</text><text x="139.0" y="184" font-size="11" style="fill:var(--muted)">1</text><text x="231.0" y="184" font-size="11" style="fill:var(--muted)">2</text><text x="323.0" y="184" font-size="11" style="fill:var(--muted)">3</text><text x="150" y="204" font-size="12" style="fill:var(--ink-2)">wavelength λ (μm)</text><text x="8" y="12" font-size="12" style="fill:var(--ink-2)">emitted power per unit wavelength</text><line x1="190" y1="46" x2="212" y2="46" style="stroke:var(--coral);stroke-width:2.2"/><text x="218" y="50" font-size="12" style="fill:var(--coral)">5000 K, peak 0.58 μm</text><line x1="190" y1="66" x2="212" y2="66" style="stroke:var(--indigo);stroke-width:2.2"/><text x="218" y="70" font-size="12" style="fill:var(--indigo)">4000 K, peak 0.72 μm</text></svg>',
    'cooling': '<svg viewBox="0 0 360 210" role="img" aria-label="Cooling curve: the excess temperature above the room halves every 5 minutes and the curve approaches room temperature"><line x1="50" y1="170" x2="350" y2="170" style="fill:none;stroke:var(--ink-2);stroke-width:1.4"/><line x1="50" y1="170" x2="50" y2="15" style="fill:none;stroke:var(--ink-2);stroke-width:1.4"/><line x1="50" y1="138.0" x2="350" y2="138.0" style="stroke:var(--teal);stroke-width:1.2;stroke-dasharray:5 3"/><path d="M50.0 35.6 L53.1 39.1 L56.2 42.5 L59.4 45.7 L62.5 48.9 L65.6 51.9 L68.8 54.8 L71.9 57.7 L75.0 60.4 L78.1 63.0 L81.2 65.6 L84.4 68.1 L87.5 70.4 L90.6 72.7 L93.8 75.0 L96.9 77.1 L100.0 79.2 L103.1 81.2 L106.2 83.1 L109.4 85.0 L112.5 86.8 L115.6 88.5 L118.8 90.2 L121.9 91.9 L125.0 93.4 L128.1 94.9 L131.2 96.4 L134.4 97.8 L137.5 99.2 L140.6 100.5 L143.8 101.8 L146.9 103.0 L150.0 104.2 L153.1 105.4 L156.2 106.5 L159.4 107.6 L162.5 108.6 L165.6 109.6 L168.8 110.6 L171.9 111.5 L175.0 112.4 L178.1 113.3 L181.2 114.1 L184.4 114.9 L187.5 115.7 L190.6 116.5 L193.8 117.2 L196.9 117.9 L200.0 118.6 L203.1 119.3 L206.2 119.9 L209.4 120.5 L212.5 121.1 L215.6 121.7 L218.8 122.2 L221.9 122.8 L225.0 123.3 L228.1 123.8 L231.2 124.3 L234.4 124.7 L237.5 125.2 L240.6 125.6 L243.8 126.1 L246.9 126.5 L250.0 126.9 L253.1 127.2 L256.2 127.6 L259.4 128.0 L262.5 128.3 L265.6 128.6 L268.8 128.9 L271.9 129.3 L275.0 129.6 L278.1 129.8 L281.2 130.1 L284.4 130.4 L287.5 130.6 L290.6 130.9 L293.8 131.1 L296.9 131.4 L300.0 131.6 L303.1 131.8 L306.2 132.0 L309.4 132.2 L312.5 132.4 L315.6 132.6 L318.8 132.8 L321.9 133.0 L325.0 133.1 L328.1 133.3 L331.2 133.5 L334.4 133.6 L337.5 133.8 L340.6 133.9 L343.8 134.1 L346.9 134.2 L350.0 134.3" style="fill:none;stroke:var(--coral);stroke-width:2.2"/><circle cx="50.0" cy="35.6" r="3.2" style="fill:var(--coral)"/><text x="57.0" y="30.6" font-size="11" style="fill:var(--muted)">84 °C</text><circle cx="112.5" cy="86.8" r="3.2" style="fill:var(--coral)"/><text x="119.5" y="81.8" font-size="11" style="fill:var(--muted)">52 °C</text><circle cx="175.0" cy="112.4" r="3.2" style="fill:var(--coral)"/><text x="182.0" y="107.4" font-size="11" style="fill:var(--muted)">36 °C</text><circle cx="237.5" cy="125.2" r="3.2" style="fill:var(--coral)"/><text x="244.5" y="120.2" font-size="11" style="fill:var(--muted)">28 °C</text><text x="46.0" y="184" font-size="11" style="fill:var(--muted)">0</text><text x="108.5" y="184" font-size="11" style="fill:var(--muted)">5</text><text x="171.0" y="184" font-size="11" style="fill:var(--muted)">10</text><text x="233.5" y="184" font-size="11" style="fill:var(--muted)">15</text><text x="296.0" y="184" font-size="11" style="fill:var(--muted)">20</text><text x="150" y="202" font-size="12" style="fill:var(--ink-2)">time t (min)</text><text x="8" y="12" font-size="12" style="fill:var(--ink-2)">T (°C)</text><text x="240" y="153.0" font-size="11" style="fill:var(--teal)">room T₀ = 20 °C</text><text x="170" y="70" font-size="11" style="fill:var(--muted)">excess 64 → 32 → 16 → 8 °C</text><text x="170" y="84" font-size="11" style="fill:var(--muted)">in equal 5 min steps</text></svg>',
}

ST = ['Both Statement I and Statement II are correct',
      'Both Statement I and Statement II are incorrect',
      'Statement I is correct but Statement II is incorrect',
      'Statement I is incorrect but Statement II is correct']
AR = ['Both A and R are true, and R is the correct explanation of A',
      'Both A and R are true, but R is not the correct explanation of A',
      'A is true but R is false',
      'A is false but R is true']


DEEP = {

# ---------------------------------------------------------------- temperature
'thermal-properties-temperature': dict(
    level='basic',
    notes=[
        ('Building any temperature scale', r'''<p>A thermometer uses a property that changes steadily with temperature: the length of a mercury thread, the pressure of a gas held at fixed volume, or the resistance of a platinum wire. Two fixed points calibrate it. The lower fixed point (LFP) is the ice point and the upper fixed point (UFP) is the steam point, both at 1 atm.</p>
<p>If the property changes linearly, a reading that sits the same fraction of the way from LFP to UFP means the same temperature on every scale:</p>
<p>\[ \frac{\text{reading}-\text{LFP}}{\text{UFP}-\text{LFP}}\ \text{is the same on every scale.} \]</p>
<div class="table-wrap"><table>
<thead><tr><th>Scale</th><th>Ice point</th><th>Steam point</th><th>Divisions between them</th></tr></thead>
<tbody>
<tr><td>Celsius</td><td>0 °C</td><td>100 °C</td><td>100</td></tr>
<tr><td>Fahrenheit</td><td>32 °F</td><td>212 °F</td><td>180</td></tr>
<tr><td>Kelvin</td><td>273.15 K</td><td>373.15 K</td><td>100</td></tr>
<tr><td>Réaumur</td><td>0 °R</td><td>80 °R</td><td>80</td></tr>
</tbody></table></div>
<p>So \(\frac{C}{100}=\frac{F-32}{180}=\frac{K-273.15}{100}=\frac{R}{80}\). The same rule converts readings of a faulty or home-made thermometer: use its own marks for LFP and UFP.</p>'''),
        ('Readings worth remembering', r'''<ul>
<li>Celsius and Fahrenheit agree at <strong>−40°</strong>. Put \(F=C\) in \(F=\tfrac95C+32\).</li>
<li>Fahrenheit and Kelvin agree at about <strong>574.6</strong> (that is 301.4 °C).</li>
<li>The Fahrenheit reading is twice the Celsius reading at 160 °C (320 °F).</li>
<li>Temperature <em>differences</em>: \(\Delta F=1.8\,\Delta C\) and \(\Delta K=\Delta C\). A 1 °C rise is a 1.8 °F rise, not a 33.8 °F rise.</li>
</ul>'''),
        ('Gas thermometer, absolute zero and the zeroth law', r'''<p>Hold a gas at fixed volume and plot its pressure against Celsius temperature. Every dilute gas gives a straight line. Extend the lines backwards: they all reach zero pressure at the same point, −273.15 °C. This common point is <strong>absolute zero</strong>, and it does not depend on which gas you use. That is why the gas scale is a good standard.</p>
<p>The Kelvin scale assigns 273.16 K to the triple point of water, where ice, water and vapour coexist. A constant-volume gas thermometer then reads \(T=273.16\ \text{K}\times P/P_{\rm tr}\).</p>
<p>The <strong>zeroth law</strong> says: if A and B are each in thermal equilibrium with C, then A and B are in thermal equilibrium with each other. It lets us define temperature as the property that is equal for bodies in equilibrium. The thermometer is the body C.</p>'''),
    ],
    formulas=[
        dict(title='Converting between any two linear scales',
             formula=r'\frac{X-\text{LFP}_X}{\text{UFP}_X-\text{LFP}_X}=\frac{Y-\text{LFP}_Y}{\text{UFP}_Y-\text{LFP}_Y}',
             symbols='X, Y readings of the same temperature on two scales; LFP and UFP lower and upper fixed points of each scale, in that scale’s own units. Valid when both scales vary linearly with the same thermometric property.'),
        dict(title='Constant-volume gas thermometer',
             formula=r'T=273.16\ \text{K}\times\frac{P}{P_{\rm tr}}',
             symbols='T absolute temperature (K); P gas pressure at that temperature (Pa); P_tr pressure of the same gas at the triple point of water (Pa). Fixed volume and fixed amount of a dilute gas.'),
    ],
    traps=[r'Converting a temperature <em>change</em> with the full formula. A rise of 10 °C is a rise of 18 °F and of 10 K. The offsets 32 and 273.15 belong only to actual readings.',
           r'Saying a hot body “contains more heat”. A body has internal energy. Heat is the energy that flows because of a temperature difference.'],
    exam=r'''<ul>
<li>“At what temperature do the Celsius and Fahrenheit scales read the same?” (−40)</li>
<li>A faulty thermometer reads x at the ice point and y at the steam point. Find the true temperature for a given reading.</li>
<li>A temperature change in one scale converted to another (no offset).</li>
<li>Constant-volume gas thermometer: pressure ratio gives kelvin ratio.</li>
<li>Statement questions on the zeroth law and on the meaning of heat and temperature.</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A faulty thermometer reads 5° in melting ice and 95° in steam at 1 atm. What is the true temperature when it reads 60°?',
             steps=[r'Use the fraction rule. On this thermometer the LFP is 5 and the UFP is 95, so there are 90 divisions.',
                    r'\(\frac{C-0}{100}=\frac{60-5}{95-5}=\frac{55}{90}\).',
                    r'\(C=\frac{55}{90}\times100=61.1\ ^\circ\mathrm{C}\).'],
             answer=r'About 61.1 °C'),
        dict(tag='Concept', q=r'At what temperature is the Fahrenheit reading exactly twice the Celsius reading?',
             steps=[r'Write \(F=\tfrac95C+32\) and set \(F=2C\).',
                    r'\(2C=1.8C+32\), so \(0.2C=32\).',
                    r'\(C=160\ ^\circ\mathrm{C}\) and \(F=320\ ^\circ\mathrm{F}\).'],
             answer=r'160 °C, which is 320 °F'),
        dict(tag='Ratio', q=r'The temperature of a room rises by 45 °F during a day. What is the rise in kelvin?',
             steps=[r'This is a change, so no offset is used.',
                    r'180 Fahrenheit divisions match 100 kelvin divisions, so \(\Delta K=\frac{100}{180}\Delta F=\frac59\times45\).',
                    r'\(\Delta K=25\ \mathrm{K}\).'],
             answer=r'25 K'),
    ],
    practice=[
        dict(q=r'At what temperature do the Celsius and Fahrenheit scales show the same numerical reading?',
             options=['0°', '−32°', '−40°', '273°'], answer=2, type='numerical',
             explanation=r'Put \(F=C\) in \(F=\tfrac95C+32\): \(-0.8C=32\), so \(C=-40\). 0° fails because 0 °C is 32 °F. −32° comes from dropping the 9/5 factor. 273° is the Celsius–Kelvin offset, not a common reading.'),
        dict(q=r'A home-made scale X marks the ice point as 20 °X and the steam point as 180 °X. A reading of 100 °X corresponds to',
             options=['40 °C', '50 °C', '62.5 °C', '80 °C'], answer=1, type='numerical',
             explanation=r'\(\frac{C}{100}=\frac{100-20}{180-20}=\frac{80}{160}\), so C = 50 °C. 62.5 °C uses 100/160 and ignores the offset 20. 80 °C takes the reading minus 20 as Celsius directly.'),
        dict(q=r'Statement I: A body at a higher temperature always contains more heat than a body at a lower temperature. Statement II: Heat can flow from a small hot body to a large cold body that has more internal energy.',
             options=list(ST), answer=3, type='statement',
             explanation=r'Statement I is wrong: bodies do not contain heat, and a large cool body can have more internal energy than a small hot one. Statement II is right: the direction of heat flow depends only on temperature, not on total internal energy.'),
        dict(q=r'A constant-volume gas thermometer shows a pressure of 6.0×10⁴ Pa at the triple point of water and 8.0×10⁴ Pa in a hot bath. The bath temperature is',
             options=['364 K', '205 K', '273 K', '91 K'], answer=0, type='numerical',
             explanation=r'\(T=273.16\times\frac{8.0}{6.0}=364\ \mathrm{K}\) (91 °C). 205 K inverts the pressure ratio. 273 K ignores the pressure change. 91 K writes the Celsius value with a kelvin unit.'),
    ],
),

# ---------------------------------------------------------------- expansion
'thermal-properties-expansion': dict(
    level='core',
    notes=[
        ('Why solids expand on heating', r'''<p>Atoms in a solid vibrate about their equilibrium positions. The potential energy between two neighbouring atoms is not symmetric: it rises steeply if they are pushed together and gently if they are pulled apart. When you heat the solid, the vibrations grow. Because the energy curve is lopsided, the atoms spend more time at larger separations, so the <em>average</em> spacing grows. A perfectly symmetric (spring-like) potential would give no expansion at all.</p>'''),
        ('Derivation: β = 2α and γ = 3α', r'''<p>Take a square plate of side \(L_0\) and heat it by \(\Delta T\).</p>
<ol>
<li>Each side becomes \(L_0(1+\alpha\Delta T)\).</li>
<li>Area \(A=L_0^2(1+\alpha\Delta T)^2=A_0\left(1+2\alpha\Delta T+\alpha^2\Delta T^2\right)\).</li>
<li>\(\alpha\Delta T\) is about \(10^{-3}\) or smaller, so \((\alpha\Delta T)^2\) is about \(10^{-6}\). Drop it. Then \(\Delta A=2\alpha A_0\Delta T\), so \(\beta=2\alpha\).</li>
<li>For a cube, \(V=L_0^3(1+\alpha\Delta T)^3\approx V_0(1+3\alpha\Delta T)\), so \(\gamma=3\alpha\).</li>
</ol>
<p>Hence \(\alpha:\beta:\gamma=1:2:3\) for an isotropic solid. For a crystal with different coefficients along three axes, the same algebra gives \(\gamma=\alpha_x+\alpha_y+\alpha_z\). The percentage form is quick: if every length grows by p %, area grows by 2p % and volume by 3p %, while density falls by about 3p %.</p>'''),
        ('Consequences to connect', r'''<ul>
<li><strong>Holes and cavities</strong> expand exactly like the material that could fill them. A tight ring is heated so it slips over a shaft.</li>
<li><strong>Density</strong> falls: \(\rho=\rho_0/(1+\gamma\Delta T)\approx\rho_0(1-\gamma\Delta T)\).</li>
<li><strong>Moment of inertia</strong> depends on (size)², so \(\Delta I/I=2\alpha\Delta T\). A freely spinning disc that is heated slows down, because \(L=I\omega\) stays constant: \(\Delta\omega/\omega=-2\alpha\Delta T\).</li>
<li><strong>Bimetallic strip</strong>: two metals bonded together bend on heating, with the metal of larger α on the outer (convex) side. Thermostats, fire alarms and flashers use this.</li>
</ul>'''),
    ],
    formulas=[
        dict(title='Anisotropic solid',
             formula=r'\gamma=\alpha_x+\alpha_y+\alpha_z,\qquad \beta_{xy}=\alpha_x+\alpha_y',
             symbols='α_x, α_y, α_z linear coefficients along three perpendicular axes (K⁻¹); γ volume coefficient (K⁻¹); β_xy area coefficient of a face in the x–y plane (K⁻¹). Small αΔT; for an isotropic solid all α are equal.'),
        dict(title='Heating a spinning body',
             formula=r'\frac{\Delta I}{I}=2\alpha\Delta T,\qquad \frac{\Delta\omega}{\omega}=-2\alpha\Delta T',
             symbols='I moment of inertia about a fixed axis (kg m²); ω angular speed (rad/s); α linear coefficient (K⁻¹); ΔT temperature rise (K). Second result needs zero external torque so that Iω is conserved; small αΔT.'),
        dict(title='Radius of a bimetallic strip',
             formula=r'R\approx\frac{d}{(\alpha_1-\alpha_2)\Delta T}',
             symbols='R radius of curvature of the common interface (m); d thickness of each strip (m); α₁ > α₂ linear coefficients of the two metals (K⁻¹); ΔT temperature rise above the straight state (K). Strips of equal thickness, small αΔT.'),
    ],
    figure=dict(svg=None, caption='A bimetallic strip is straight at room temperature. On heating, the brass (larger α) becomes longer than the steel, so the strip curves with brass on the outside.'),
    traps=[r'Mixing up the factors: area has two lengths, so β = 2α; volume has three, so γ = 3α. Writing β = 3α is a common slip under time pressure.',
           r'Thinking the higher-α metal ends up on the inside of a heated bimetallic strip. The longer strip must lie on the longer, outer arc.'],
    exam=r'''<ul>
<li>“The length of a rod increases by 0.1 %. Find the percentage change in area or volume.”</li>
<li>Ratio α : β : γ, or γ of an anisotropic crystal from three given α values.</li>
<li>Behaviour of a hole, a ring or a cavity on heating.</li>
<li>Which way a bimetallic strip bends on heating and on cooling.</li>
<li>Change in angular speed or moment of inertia of a heated rotating disc.</li>
<li>Fractional change in density on heating.</li>
</ul>''',
    examples=[
        dict(tag='Ratio', q=r'When a metal sphere is heated, its radius increases by 0.2 %. Find the percentage changes in its surface area, volume and density.',
             steps=[r'Small fractional changes multiply into sums: area ∝ r², volume ∝ r³.',
                    r'Surface area rises by 2 × 0.2 = 0.4 %.',
                    r'Volume rises by 3 × 0.2 = 0.6 %.',
                    r'Mass is fixed, so density ∝ 1/V and falls by about 0.6 %.'],
             answer=r'Area +0.4 %, volume +0.6 %, density −0.6 %'),
        dict(tag='Numerical', q=r'A steel ring has an inner diameter of 5.000 cm at 20 °C. It must slide onto a shaft of diameter 5.005 cm. To what temperature must the ring be heated? Take \(\alpha=1.2\times10^{-5}\ \mathrm{K^{-1}}\).',
             steps=[r'The hole grows like the steel: \(\Delta d=d\,\alpha\,\Delta T\).',
                    r'\(\Delta T=\frac{\Delta d}{d\alpha}=\frac{0.005}{5.000\times1.2\times10^{-5}}=83.3\ \mathrm{K}\).',
                    r'Final temperature \(=20+83.3\approx103\ ^\circ\mathrm{C}\).'],
             answer=r'About 103 °C'),
        dict(tag='Concept', q=r'A thin metal disc spins freely about its axis with no friction. It is heated by 50 K. If \(\alpha=2\times10^{-5}\ \mathrm{K^{-1}}\), by what fraction does its angular speed change?',
             steps=[r'No external torque acts, so angular momentum \(I\omega\) is conserved.',
                    r'\(I\propto MR^2\), so \(\Delta I/I=2\alpha\Delta T=2\times2\times10^{-5}\times50=2\times10^{-3}\).',
                    r'\(\omega\) must fall by the same fraction to keep \(I\omega\) fixed: \(\Delta\omega/\omega=-2\times10^{-3}\).'],
             answer=r'Angular speed decreases by 0.2 %'),
    ],
    practice=[
        dict(q=r'The edge of a metal cube increases by 0.1 % on heating. The percentage increase in its volume is',
             options=['0.1 %', '0.2 %', '0.3 %', '0.03 %'], answer=2, type='numerical',
             explanation=r'Volume ∝ (edge)³, so the fractional change triples: 0.3 %. 0.1 % ignores the other two directions. 0.2 % is the area change. 0.03 % divides instead of multiplies.'),
        dict(q=r'A crystal has linear expansion coefficients 1×10⁻⁵, 2×10⁻⁵ and 3×10⁻⁵ K⁻¹ along three perpendicular axes. Its volume expansion coefficient is',
             options=['2×10⁻⁵ K⁻¹', '6×10⁻⁵ K⁻¹', '1.8×10⁻⁴ K⁻¹', '3×10⁻⁵ K⁻¹'], answer=1, type='numerical',
             explanation=r'For an anisotropic solid γ = α_x + α_y + α_z = 6×10⁻⁵ K⁻¹. 1.8×10⁻⁴ K⁻¹ wrongly multiplies the sum by 3 again. 2×10⁻⁵ K⁻¹ is the mean of the three, and 3×10⁻⁵ K⁻¹ uses only the largest.'),
        dict(q=r'Assertion (A): A heated brass–steel bimetallic strip bends with brass on the convex side. Reason (R): Brass has a larger coefficient of linear expansion than steel.',
             options=list(AR), answer=0, type='ar',
             explanation=r'Both are true. Brass expands more, so it must lie on the longer outer arc, which is the convex side. R gives exactly this cause, so it explains A.'),
        dict(q=r'A metal has \(\alpha=2\times10^{-5}\ \mathrm{K^{-1}}\). When heated by 100 K, its density decreases by about',
             options=['0.2 %', '0.4 %', '0.06 %', '0.6 %'], answer=3, type='numerical',
             explanation=r'Density falls by the volume fraction γΔT = 3αΔT = 3×2×10⁻⁵×100 = 6×10⁻³ = 0.6 %. 0.2 % uses α instead of γ. 0.4 % uses β. 0.06 % slips a power of ten.'),
    ],
),

# ---------------------------------------------------------------- liquids
'thermal-properties-liquids': dict(
    level='core',
    notes=[
        ('Real and apparent expansion', r'''<p>Fill a flask of capacity \(V_0\) to the brim with a liquid, then heat both by \(\Delta T\).</p>
<ol>
<li>The liquid’s volume becomes \(V_0(1+\gamma_l\Delta T)\).</li>
<li>The flask’s capacity becomes \(V_0(1+\gamma_v\Delta T)\), because the cavity expands like the glass.</li>
<li>The overflow is the difference: \(\Delta V=V_0(\gamma_l-\gamma_v)\Delta T\). So the observed (apparent) coefficient is \(\gamma_{\rm app}=\gamma_l-\gamma_v\).</li>
</ol>
<p>If \(\gamma_l>\gamma_v\) the level rises; if they are equal it stays put; if the vessel expands more, the level falls. When a flask is first dipped into hot water, the level <em>dips</em> for a moment: the glass warms and expands before heat reaches the liquid. Using two vessels of known coefficients, \(\gamma_l=\gamma_{\rm app,1}+\gamma_{v1}=\gamma_{\rm app,2}+\gamma_{v2}\) gives the true coefficient.</p>'''),
        ('Density, upthrust and floating bodies', r'''<p>Mass is fixed, so \(\rho=\rho_0/(1+\gamma\Delta T)\). For a solid fully immersed in a liquid, upthrust is \(V_s\rho_lg\). On heating, \(V_s\) grows by \(\gamma_s\Delta T\) while \(\rho_l\) falls by \(\gamma_l\Delta T\):</p>
<p>\[ F_B\approx F_{B0}\,[1+(\gamma_s-\gamma_l)\Delta T]. \]</p>
<p>Liquids usually expand much more than solids, so upthrust decreases and the apparent weight of a sunken body <em>increases</em> on heating. A floating body sinks a little deeper in a warmer liquid, because the submerged volume \(m/\rho_l\) must grow.</p>'''),
        ('Anomalous expansion of water and frozen lakes', r'''<ul>
<li>From 0 °C to 4 °C, water contracts on warming. Its density is greatest, about 1000 kg/m³, near 4 °C. Above 4 °C it expands normally.</li>
<li>Ice (about 917 kg/m³) is less dense than water because hydrogen bonds hold the molecules in an open lattice. So ice floats.</li>
<li>In winter, surface water cools and sinks until the whole lake is near 4 °C. Further cooling makes the surface water <em>lighter</em>, so it stays on top and freezes there.</li>
<li>Ice is a poor conductor, so it insulates the water below. The bottom stays near 4 °C and aquatic life survives.</li>
<li>Water pipes burst in severe winters because water expands about 9 % on freezing. Water is also unsuitable as a thermometric liquid near 4 °C, since one volume corresponds to two temperatures.</li>
</ul>'''),
    ],
    formulas=[
        dict(title='Overflow from a full vessel',
             formula=r'\Delta V_{\rm overflow}=V_0(\gamma_l-\gamma_v)\Delta T',
             symbols='V₀ initial liquid volume = vessel capacity (m³); γ_l liquid and γ_v vessel volume coefficients (K⁻¹), with γ_v = 3α for an isotropic vessel; ΔT common temperature rise (K). Small γΔT.'),
        dict(title='Upthrust on an immersed solid after heating',
             formula=r'F_B\approx F_{B0}\,[1+(\gamma_s-\gamma_l)\Delta T]',
             symbols='F_B, F_B0 upthrust after and before heating (N); γ_s solid and γ_l liquid volume coefficients (K⁻¹); ΔT temperature rise (K). Body fully immersed; small γΔT.'),
    ],
    figure=dict(svg=None, caption='Volume of a fixed mass of water between 0 °C and 10 °C (vertical scale exaggerated). The minimum near 4 °C is the point of maximum density.'),
    traps=[r'Saying the water at the bottom of a frozen lake is at 0 °C. It stays near 4 °C, the temperature of maximum density.',
           r'Assuming the upthrust on a sunken solid is unchanged on heating. The liquid’s density usually falls faster than the solid’s volume rises, so upthrust decreases.'],
    exam=r'''<ul>
<li>Overflow volume when a full flask of mercury or oil is heated.</li>
<li>Find the true coefficient of a liquid, or the α of a vessel, from apparent expansion in two vessels.</li>
<li>Change in apparent weight or in the submerged fraction of a body when the liquid is heated.</li>
<li>Graph of volume or density of water against temperature from 0 to 10 °C.</li>
<li>Assertion–reason on why lakes freeze from the top and fish survive.</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A glass flask of volume 500 cm³ is filled to the brim with mercury at 20 °C. Both are heated to 100 °C. How much mercury overflows? Take \(\gamma_{\rm Hg}=1.82\times10^{-4}\ \mathrm{K^{-1}}\) and \(\alpha_{\rm glass}=9\times10^{-6}\ \mathrm{K^{-1}}\).',
             steps=[r'Vessel volume coefficient: \(\gamma_v=3\alpha=2.7\times10^{-5}\ \mathrm{K^{-1}}\).',
                    r'Apparent coefficient: \(1.82\times10^{-4}-0.27\times10^{-4}=1.55\times10^{-4}\ \mathrm{K^{-1}}\).',
                    r'Overflow \(=500\times1.55\times10^{-4}\times80=6.2\ \mathrm{cm^3}\).'],
             answer=r'6.2 cm³'),
        dict(tag='Concept', q=r'A steel block hangs from a spring balance, fully immersed in oil. The oil and block are slowly heated. Does the balance reading rise or fall?',
             steps=[r'Reading = weight − upthrust. The weight does not change.',
                    r'Upthrust \(=V_s\rho_lg\) changes by the factor \(1+(\gamma_s-\gamma_l)\Delta T\).',
                    r'Oil expands far more than steel (\(\gamma_l\gg\gamma_s\)), so upthrust decreases.',
                    r'Less upthrust means a larger reading.'],
             answer=r'The reading rises'),
        dict(tag='Graph', q=r'Sketch how the volume of 1 kg of water changes as it is warmed from 0 °C to 10 °C, and mark where its density is greatest.',
             steps=[r'From 0 °C to 4 °C the volume decreases (anomalous contraction).',
                    r'At 4 °C the volume is a minimum, so the density is a maximum.',
                    r'Above 4 °C the volume rises again, at first slowly and then faster.',
                    r'The curve is a shallow U with its lowest point at 4 °C, as in the figure above.'],
             answer=r'A U-shaped curve with minimum volume (maximum density) at 4 °C'),
    ],
    practice=[
        dict(q=r'A liquid fills a vessel whose volume expansion coefficient equals that of the liquid. When both are heated equally, the liquid level',
             options=['Rises', 'Falls', 'Stays at the same mark', 'First rises, then falls'], answer=2, type='concept',
             explanation=r'Overflow ∝ (γ_l − γ_v) = 0, so the liquid and the cavity grow by the same volume. It rises only if the liquid expands more, and falls only if the vessel expands more.'),
        dict(q=r'A liquid’s apparent volume coefficient is 1.40×10⁻⁴ K⁻¹ in a copper vessel (α_Cu = 1.7×10⁻⁵ K⁻¹) and 1.34×10⁻⁴ K⁻¹ in a silver vessel. The linear coefficient of silver is',
             options=['1.9×10⁻⁵ K⁻¹', '5.7×10⁻⁵ K⁻¹', '1.7×10⁻⁵ K⁻¹', '2.0×10⁻⁶ K⁻¹'], answer=0, type='numerical',
             explanation=r'True γ_l = 1.40×10⁻⁴ + 3×1.7×10⁻⁵ = 1.91×10⁻⁴ K⁻¹. In silver, 3α_Ag = 1.91×10⁻⁴ − 1.34×10⁻⁴ = 5.7×10⁻⁵, so α_Ag = 1.9×10⁻⁵ K⁻¹. 5.7×10⁻⁵ is γ of silver, not α. 2.0×10⁻⁶ forgets the copper vessel’s own expansion.'),
        dict(q=r'Assertion (A): Ice floats on water. Reason (R): Liquid water has its maximum density at 4 °C.',
             options=list(AR), answer=1, type='ar',
             explanation=r'Both statements are true. Ice floats because solid ice (about 917 kg/m³) is less dense than liquid water at 0 °C, due to its open hydrogen-bonded lattice. R is about liquid water between 0 and 10 °C and does not explain why the solid is lighter.'),
        dict(q=r'An oil has density 800 kg/m³ at 0 °C and \(\gamma=5\times10^{-4}\ \mathrm{K^{-1}}\). Its density at 100 °C is about',
             options=['840 kg/m³', '800 kg/m³', '720 kg/m³', '762 kg/m³'], answer=3, type='numerical',
             explanation=r'\(\rho=\rho_0/(1+\gamma\Delta T)=800/1.05\approx762\) kg/m³ (the approximate form 800(1 − 0.05) gives 760). 840 kg/m³ multiplies instead of divides. 720 kg/m³ uses 10 % instead of 5 %.'),
    ],
),

# ---------------------------------------------------------------- calorimetry
'thermal-properties-calorimetry': dict(
    level='core',
    notes=[
        ('Heat capacity, specific heat and water equivalent', r'''<ul>
<li><strong>Heat capacity</strong> \(C=Q/\Delta T\) belongs to a whole object (J/K).</li>
<li><strong>Specific heat</strong> \(c=Q/(m\Delta T)\) belongs to a material (J/kg K).</li>
<li><strong>Molar heat capacity</strong> \(C_m=Mc\) is per mole (J/mol K). For gases it depends on the process, which the thermodynamics chapter uses.</li>
<li><strong>Water equivalent</strong> \(W=mc/c_w\) of a calorimeter is the mass of water that would need the same heat for the same temperature rise. Add it to the water mass in the heat balance.</li>
<li>Units: 1 cal = 4.186 J (often 4.2 J). Water: \(c_w=4186\ \mathrm{J/kg\,K}=1\ \mathrm{cal/g\,^\circ C}\). Ice: about 2100 J/kg K = 0.5 cal/g °C.</li>
</ul>
<p>Water has an unusually large specific heat. It warms and cools slowly, which keeps coastal climates mild and makes it a good coolant in car radiators and hot-water bottles.</p>'''),
        ('Method of mixtures as a weighted average', r'''<p>With no phase change and no heat loss, heat lost by the hot bodies equals heat gained by the cold ones. Solving gives</p>
<p>\[ T_f=\frac{\sum m_ic_iT_i}{\sum m_ic_i}. \]</p>
<p>So the final temperature is an average weighted by heat capacity. It always lies between the extreme starting temperatures, and closer to the body with the larger \(mc\). A simple average is correct only when the heat capacities are equal. Treat the calorimeter as one more body with its own \(mc\).</p>'''),
        ('When specific heat changes with temperature', r'''<p>If \(c\) depends on \(T\), add up small steps: \(Q=\int_{T_1}^{T_2}m\,c(T)\,dT\). For \(c=a+bT\), this gives \(Q=m\left[a(T_2-T_1)+\tfrac b2\left(T_2^2-T_1^2\right)\right]\). The mean specific heat over the range is \(Q/(m\Delta T)\).</p>'''),
    ],
    formulas=[
        dict(title='Final temperature of a mixture (no phase change)',
             formula=r'T_f=\frac{\sum_i m_ic_iT_i}{\sum_i m_ic_i}',
             symbols='m_i masses (kg); c_i specific heats (J/kg K); T_i initial temperatures (°C or K, same scale for all); T_f final common temperature. Insulated system, no phase change, no chemical reaction.'),
        dict(title='Water equivalent of a container',
             formula=r'W=\frac{m\,c}{c_w}',
             symbols='W water equivalent (kg); m container mass (kg); c its specific heat (J/kg K); c_w specific heat of water (J/kg K). Add W to the water mass in heat-balance equations.'),
        dict(title='Heat with temperature-dependent specific heat',
             formula=r'Q=\int_{T_1}^{T_2}m\,c(T)\,dT',
             symbols='Q heat supplied (J); m mass (kg); c(T) specific heat as a function of temperature (J/kg K); T₁, T₂ initial and final temperatures (K or °C consistently). No phase change in the range.'),
    ],
    traps=[r'Leaving out the calorimeter. If its mass and specific heat (or its water equivalent) are given, it gains or loses heat too.',
           r'Mixing unit systems: c in cal/g °C with masses in kg, or J with cal. Pick one system and convert everything before solving.'],
    exam=r'''<ul>
<li>Final temperature of two or three liquids mixed, given masses and specific heats.</li>
<li>Specific heat of a metal from a calorimeter experiment, with the calorimeter included.</li>
<li>Three liquids A, B, C mixed in pairs: find the temperature of the third pair.</li>
<li>Ratio of specific heats from equal heat supplied to two bodies.</li>
<li>Heat needed when c varies with T (integration).</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A copper calorimeter of mass 0.1 kg (c = 400 J/kg K) holds 0.2 kg of water at 20 °C. A 0.1 kg metal block at 135 °C is dropped in. The final temperature is 25 °C. Find the specific heat of the metal (c_w = 4200 J/kg K).',
             steps=[r'Heat gained by water and calorimeter: \((0.2\times4200+0.1\times400)\times5=880\times5=4400\ \mathrm{J}\).',
                    r'Heat lost by the block: \(0.1\times c\times(135-25)=11c\).',
                    r'Equate: \(11c=4400\), so \(c=400\ \mathrm{J/kg\,K}\).'],
             answer=r'400 J/kg K (the block is copper-like)'),
        dict(tag='Ratio', q=r'Three liquids A, B and C of equal mass are at 12 °C, 19 °C and 28 °C. Mixing A and B gives 16 °C; mixing B and C gives 23 °C. What is the final temperature when A and C are mixed?',
             steps=[r'A + B: \(c_A(16-12)=c_B(19-16)\), so \(4c_A=3c_B\) and \(c_A=0.75c_B\).',
                    r'B + C: \(c_B(23-19)=c_C(28-23)\), so \(4c_B=5c_C\) and \(c_C=0.8c_B\).',
                    r'A + C: \(0.75(T-12)=0.8(28-T)\).',
                    r'\(1.55T=9+22.4=31.4\), so \(T\approx20.3\ ^\circ\mathrm{C}\).'],
             answer=r'About 20.3 °C'),
        dict(tag='Numerical', q=r'The specific heat of a material is \(c=(100+2T)\ \mathrm{J/kg\,K}\), with T in °C. How much heat raises 2 kg of it from 0 °C to 10 °C?',
             steps=[r'\(Q=m\int_0^{10}(100+2T)\,dT=2\left[100T+T^2\right]_0^{10}\).',
                    r'\(=2\,(1000+100)=2200\ \mathrm{J}\).',
                    r'Check: the mean specific heat is \(2200/(2\times10)=110\), the value at the mid-temperature 5 °C, as expected for a linear c.'],
             answer=r'2200 J'),
    ],
    practice=[
        dict(q=r'A calorimeter of mass 200 g is made of a material with specific heat 0.1 cal/g °C. Its water equivalent is',
             options=['2 g', '20 g', '200 g', '2000 g'], answer=1, type='numerical',
             explanation=r'W = mc/c_w = 200 × 0.1 / 1 = 20 g. 200 g is the actual mass, which ignores the lower specific heat. 2 g and 2000 g misplace the factor of 0.1.'),
        dict(q=r'Equal masses of A and B receive equal amounts of heat. A warms by 10 K and B by 25 K. The ratio of specific heats c_A : c_B is',
             options=['2 : 5', '1 : 1', '25 : 4', '5 : 2'], answer=3, type='numerical',
             explanation=r'With Q and m equal, c ∝ 1/ΔT, so c_A/c_B = 25/10 = 5 : 2. A warms less, so it has the larger specific heat. 2 : 5 inverts the ratio; 25 : 4 squares it.'),
        dict(q=r'Statement I: Coastal places have milder climates partly because water has a high specific heat. Statement II: Equal masses of water and dry sand given equal heat warm by the same amount.',
             options=list(ST), answer=2, type='statement',
             explanation=r'Statement I is correct: the sea stores and releases large amounts of heat with small temperature change. Statement II is wrong: sand has a much smaller specific heat, so it warms several times more for the same heat.'),
        dict(q=r'1 kg of a liquid of specific heat c at 90 °C is mixed with 2 kg of another liquid of specific heat 2c at 30 °C. With no heat loss, the final temperature is',
             options=['42 °C', '50 °C', '60 °C', '70 °C'], answer=0, type='numerical',
             explanation=r'Weight by mc: T = (1·c·90 + 2·2c·30)/(1·c + 2·2c) = 210/5 = 42 °C. 50 °C weights by mass only and ignores c. 60 °C is the plain average. 70 °C would need the hot liquid to dominate, but it has the smaller heat capacity.'),
    ],
),

# ---------------------------------------------------------------- latent heat
'thermal-properties-latent': dict(
    level='core',
    notes=[
        ('Reading a heating curve', r'''<p>Heat a block of ice at −20 °C with a heater of constant power P and plot temperature against time (or heat supplied). The graph has five parts:</p>
<ol>
<li><strong>Ice warms</strong> from −20 °C to 0 °C. Slope \(dT/dt=P/(mc_{\rm ice})\).</li>
<li><strong>Melting plateau</strong> at 0 °C. Ice and water coexist. Length \(=mL_f/P\).</li>
<li><strong>Water warms</strong> from 0 °C to 100 °C. Slope \(P/(mc_w)\), about half the ice slope because \(c_w\approx2c_{\rm ice}\).</li>
<li><strong>Boiling plateau</strong> at 100 °C. It is about 6.7 times longer than the melting plateau, because \(L_v/L_f=2.26\times10^6/3.36\times10^5\approx6.7\).</li>
<li><strong>Steam warms</strong> above 100 °C, again steeply because \(c_{\rm steam}\approx2000\ \mathrm{J/kg\,K}\).</li>
</ol>
<p>Two rules read any heating curve: a <em>steeper</em> sloping part means a <em>smaller</em> heat capacity, and a <em>longer</em> flat part means a <em>larger</em> latent heat.</p>'''),
        ('Where the energy goes during a phase change', r'''<p>During melting or boiling, the supplied energy pulls molecules apart against their attraction. Potential energy rises while average kinetic energy, and so temperature, stays the same. Freezing and condensation release the same latent heat back.</p>
<p>This is why steam burns are worse than boiling-water burns. One gram of steam at 100 °C gives 540 cal as it condenses and up to 100 cal more as the water cools to 0 °C: 640 cal in total, against 100 cal from water at 100 °C.</p>'''),
        ('Effect of pressure on melting and boiling points', r'''<ul>
<li>Boiling point rises with pressure. A pressure cooker at about 2 atm boils water near 120 °C, so food cooks faster. At high altitude water boils below 100 °C and food cooks slowly.</li>
<li>The melting point of ice falls when pressure rises, because ice shrinks on melting. A loaded wire passes slowly through an ice block, and the ice refreezes above it (regelation).</li>
<li>For most substances, such as wax, the solid is denser than the liquid, so their melting point rises with pressure.</li>
<li>Some solids, like camphor and dry ice, change straight to vapour at ordinary pressure (sublimation). At the triple point of water (273.16 K, about 611 Pa) all three phases coexist.</li>
</ul>'''),
    ],
    formulas=[
        dict(title='Heating curve with a constant-power heater',
             formula=r'\frac{dT}{dt}=\frac{P}{mc},\qquad t_{\rm plateau}=\frac{mL}{P}',
             symbols='dT/dt slope of a sloping part (K/s); P heater power absorbed by the sample (W); m mass (kg); c specific heat of the phase present (J/kg K); t_plateau duration of a flat part (s); L latent heat of that change (J/kg). No heat loss.'),
        dict(title='Standard latent heats of water at 1 atm',
             formula=r'L_f=3.36\times10^5\ \mathrm{J/kg}=80\ \mathrm{cal/g},\qquad L_v=2.26\times10^6\ \mathrm{J/kg}=540\ \mathrm{cal/g}',
             symbols='L_f latent heat of fusion of ice at 0 °C; L_v latent heat of vaporisation of water at 100 °C. Use the value the question gives if it differs slightly (for example 3.34×10⁵ J/kg).'),
    ],
    figure=dict(svg=None, caption='Heating curve of water at constant power. Sloping parts heat one phase; flat parts are phase changes. The boiling plateau is drawn with a break: at scale it is about 6.7 times the melting plateau.'),
    traps=[r'Reading a heating-curve slope backwards. A steeper rise means a <em>smaller</em> heat capacity mc, not a larger one.',
           r'Forgetting that condensing steam gives latent heat <em>and then</em> sensible heat as the condensed water cools to the final temperature.'],
    exam=r'''<ul>
<li>Total heat to turn ice at a negative temperature into steam above 100 °C.</li>
<li>From a heating curve, compare specific heats (slopes) or latent heats (plateau lengths).</li>
<li>With a constant heater, “ice melts in t minutes; how long to boil the water away?”</li>
<li>Why steam burns more than boiling water; effect of pressure on boiling point.</li>
<li>Multiple-statement questions on what stays constant during a phase change.</li>
</ul>''',
    examples=[
        dict(tag='Graph', q=r'A constant heater melts a block of ice at 0 °C in 2 minutes. How long does it take to (a) warm the water from 0 °C to 100 °C, and (b) boil all of it away? Use \(c_w=4200\ \mathrm{J/kg\,K}\), \(L_f=3.36\times10^5\) and \(L_v=2.26\times10^6\ \mathrm{J/kg}\).',
             steps=[r'Time is proportional to heat at constant power, and the mass is the same throughout.',
                    r'(a) \(\frac{t}{2\ \text{min}}=\frac{4200\times100}{3.36\times10^5}=1.25\), so \(t=2.5\) min.',
                    r'(b) \(\frac{t}{2\ \text{min}}=\frac{2.26\times10^6}{3.36\times10^5}=6.73\), so \(t\approx13.5\) min.',
                    r'This is why the boiling plateau dominates any heating curve drawn to scale.'],
             answer=r'(a) 2.5 min (b) about 13.5 min'),
        dict(tag='Numerical', q=r'How much heat converts 10 g of ice at −10 °C into steam at 100 °C? Use \(c_{\rm ice}=0.5\), \(c_w=1\ \mathrm{cal/g\,^\circ C}\), \(L_f=80\), \(L_v=540\ \mathrm{cal/g}\).',
             steps=[r'Warm ice to 0 °C: \(10\times0.5\times10=50\) cal.',
                    r'Melt: \(10\times80=800\) cal.',
                    r'Warm water to 100 °C: \(10\times1\times100=1000\) cal.',
                    r'Boil: \(10\times540=5400\) cal.',
                    r'Total \(=50+800+1000+5400=7250\) cal (about 30.4 kJ).'],
             answer=r'7250 cal'),
        dict(tag='Concept', q=r'Why does a scald from steam at 100 °C hurt more than one from water at 100 °C?',
             steps=[r'Both start at 100 °C, but the steam must first condense on the skin.',
                    r'Condensing 1 g of steam releases 540 cal of latent heat.',
                    r'The condensed water then cools like ordinary hot water, releasing up to 100 cal more.',
                    r'So each gram of steam delivers several times more energy to the skin.'],
             answer=r'Steam releases its large latent heat of vaporisation on condensing, in addition to the heat that water gives'),
    ],
    practice=[
        dict(q=r'In the heating curve of a pure substance at constant power, the sloping part for the solid is steeper than the sloping part for the liquid. This shows that',
             options=['Specific heat of the solid is greater than that of the liquid',
                      'Specific heat of the solid is less than that of the liquid',
                      'Latent heat of fusion is greater than latent heat of vaporisation',
                      'The substance absorbs no heat while it melts'], answer=1, type='graph',
             explanation=r'Slope = P/(mc). Same P and m, so a steeper slope means a smaller c: the solid’s specific heat is less. Slopes say nothing about latent heats, which set plateau lengths. Heat is absorbed during melting; only the temperature stays fixed.'),
        dict(q=r'5 g of steam at 100 °C condenses and the water cools to 40 °C. The heat released is (L_v = 540 cal/g, c_w = 1 cal/g °C)',
             options=['300 cal', '2700 cal', '3200 cal', '3000 cal'], answer=3, type='numerical',
             explanation=r'Condensing gives 5×540 = 2700 cal and cooling 100 → 40 °C gives 5×60 = 300 cal: 3000 cal in all. 2700 cal stops after condensation. 3200 cal cools to 0 °C instead of 40 °C. 300 cal ignores latent heat.'),
        dict(q=r'Which statements about a pure substance at its melting point are correct? (a) Temperature stays constant while it melts. (b) The heat supplied increases the potential energy of the molecules. (c) The average kinetic energy of the molecules increases during melting. (d) The boiling point of water rises when the pressure on it increases.',
             options=['(a), (b) and (d) only', '(a) and (c) only', '(b), (c) and (d) only', '(a), (b), (c) and (d)'], answer=0, type='multi',
             explanation=r'Constant temperature means constant average kinetic energy, so (c) is false. The energy goes into potential energy, so (b) is true. (a) is true, and (d) is true (pressure cooker). Any option including (c) is wrong.'),
        dict(q=r'A heater of fixed power first melts some ice at 0 °C. Later it boils away the same mass of water at 100 °C. The ratio of melting time to boiling time is (L_f = 80 cal/g, L_v = 540 cal/g)',
             options=['27 : 4', '1 : 5', '4 : 27', '1 : 1'], answer=2, type='numerical',
             explanation=r'At fixed power, time ∝ heat = mL, so t_melt : t_boil = 80 : 540 = 4 : 27. 27 : 4 inverts it. 1 : 1 would hold only if the latent heats were equal.'),
    ],
),

# ---------------------------------------------------------------- conduction
'thermal-properties-conduction': dict(
    level='exam',
    notes=[
        ('Steady state and the temperature profile', r'''<p>Fourier’s law in differential form is \(H=\frac{dQ}{dt}=-\kappa A\frac{dT}{dx}\). The minus sign says heat flows down the temperature gradient. When one end of a rod is first heated, each part absorbs heat to warm up. Later the temperatures stop changing: this is the <strong>steady state</strong>. Then no part stores heat, so the same heat current H crosses every cross-section. For a uniform rod the temperature then falls linearly along its length.</p>
<p>Conduction behaves like current in a resistor:</p>
<div class="table-wrap"><table>
<thead><tr><th>Heat conduction</th><th>Electric current</th></tr></thead>
<tbody>
<tr><td>Heat current H (W)</td><td>Current I (A)</td></tr>
<tr><td>Temperature difference ΔT (K)</td><td>Potential difference V (V)</td></tr>
<tr><td>\(R_{th}=L/(\kappa A)\) (K/W)</td><td>\(R=\rho L/A\) (Ω)</td></tr>
<tr><td>\(H=\Delta T/R_{th}\)</td><td>\(I=V/R\)</td></tr>
</tbody></table></div>
<p>κ has unit W m⁻¹ K⁻¹ and dimensions [M L T⁻³ K⁻¹].</p>'''),
        ('Composite slabs: series and parallel', r'''<p><strong>Series</strong> (layers one after another): the same H flows through each layer and the temperature drops add. So \(R=R_1+R_2\). The larger drop occurs across the layer with the larger resistance, which for equal L and A is the poorer conductor. The equivalent conductivity is</p>
<p>\[ \kappa_{\rm eq}=\frac{L_1+L_2}{L_1/\kappa_1+L_2/\kappa_2},\qquad \kappa_{\rm eq}=\frac{2\kappa_1\kappa_2}{\kappa_1+\kappa_2}\ \text{for equal thickness.} \]</p>
<p><strong>Parallel</strong> (side by side between the same two faces): each path has the same ΔT and the heat currents add. So \(1/R=1/R_1+1/R_2\) and, for equal lengths, \(\kappa_{\rm eq}=\frac{\kappa_1A_1+\kappa_2A_2}{A_1+A_2}\).</p>
<p>Two identical rods carry 4 times as much heat side by side as end to end, because the resistance changes from 2R to R/2.</p>'''),
        ('Growth of ice on a lake', r'''<p>Air above a lake is at −θ °C. A layer of ice of thickness x has formed; the water below it is at 0 °C.</p>
<ol>
<li>Heat conducted up through the ice in time dt: \(\frac{\kappa A\theta}{x}\,dt\).</li>
<li>This heat comes from water freezing at the bottom of the ice. A new layer dx has mass \(\rho A\,dx\) and releases \(\rho A L\,dx\).</li>
<li>Equate: \(\frac{\kappa A\theta}{x}dt=\rho AL\,dx\), so \(dt=\frac{\rho L}{\kappa\theta}x\,dx\).</li>
<li>Integrate: \(t=\frac{\rho L}{2\kappa\theta}\left(x_2^2-x_1^2\right)\).</li>
</ol>
<p>Time grows as the <em>square</em> of thickness. Going from 0 to 2x takes four times as long as 0 to x, so 2x after x takes three times as long. Thick ice insulates the water and slows further freezing.</p>
<p><strong>Ingenhousz’s experiment</strong>: identical rods coated with wax are dipped into hot water. In the steady state, the length along which wax melts satisfies \(\ell^2\propto\kappa\), so \(\kappa_1/\kappa_2=\ell_1^2/\ell_2^2\).</p>'''),
    ],
    formulas=[
        dict(title='Equivalent conductivity of composite slabs',
             formula=r'\kappa_{\rm series}=\frac{L_1+L_2}{L_1/\kappa_1+L_2/\kappa_2},\qquad \kappa_{\rm parallel}=\frac{\kappa_1A_1+\kappa_2A_2}{A_1+A_2}',
             symbols='κ₁, κ₂ conductivities (W/m K); L₁, L₂ thicknesses in series (m), equal cross-section; A₁, A₂ areas side by side (m²), equal length. Steady state, no side losses.'),
        dict(title='Junction temperature of two slabs in series',
             formula=r'T_J=\frac{\frac{\kappa_1}{L_1}T_1+\frac{\kappa_2}{L_2}T_2}{\frac{\kappa_1}{L_1}+\frac{\kappa_2}{L_2}}',
             symbols='T_J junction temperature; T₁, T₂ outer face temperatures (°C or K consistently); κ conductivities (W/m K); L thicknesses (m). Equal areas, steady state.'),
        dict(title='Time for lake ice to thicken',
             formula=r't=\frac{\rho L}{2\kappa\theta}\left(x_2^2-x_1^2\right)',
             symbols='t time (s); ρ density of ice (kg/m³); L latent heat of fusion (J/kg); κ conductivity of ice (W/m K); θ magnitude of air temperature below 0 °C (K); x₁, x₂ initial and final ice thickness (m). Water below at 0 °C; steady conduction at each instant.'),
    ],
    figure=dict(svg=None, caption='Two equal slabs in series, κ₁ = 3κ₂. The same heat current crosses both, so the temperature drop is three times larger across the poorer conductor: 100 °C → 75 °C → 0 °C.'),
    traps=[r'Adding conductivities for slabs in series. Resistances add in series. Two equal-thickness slabs have κ_eq = 2κ₁κ₂/(κ₁ + κ₂), not κ₁ + κ₂.',
           r'Assuming the temperature gradient is the same in every layer. In series the heat current is the same; the gradient is larger in the poorer conductor.'],
    exam=r'''<ul>
<li>Junction temperature of two or three slabs in series.</li>
<li>Equivalent conductivity of series and parallel combinations; ratio of heat currents.</li>
<li>“Two rods conduct a given heat in 12 min in series. How long in parallel?”</li>
<li>Time for ice on a pond to grow from x₁ to x₂ (t ∝ x²).</li>
<li>Ingenhousz wax-melting lengths to compare conductivities.</li>
<li>Graph of temperature along a composite rod: steeper part means smaller κ.</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'Two slabs of equal thickness and area are joined face to face. Conductivities are 3κ and κ. The outer faces are at 100 °C and 0 °C. Find the junction temperature.',
             steps=[r'Same heat current through both: \(\frac{3\kappa A(100-T)}{L}=\frac{\kappa A(T-0)}{L}\).',
                    r'\(300-3T=T\), so \(T=75\ ^\circ\mathrm{C}\).',
                    r'Check: drop of 25 K in the good conductor and 75 K in the poor one, in the ratio 1 : 3 of their resistances.'],
             answer=r'75 °C'),
        dict(tag='Ratio', q=r'Two identical rods joined end to end conduct a certain amount of heat between two reservoirs in 12 min. How long do they take when placed side by side between the same reservoirs?',
             steps=[r'Each rod has resistance R. End to end: 2R. Side by side: R/2.',
                    r'Heat current \(H=\Delta T/R_{\rm total}\), so it becomes 4 times larger.',
                    r'Time for the same heat \(\propto1/H\): \(12/4=3\) min.'],
             answer=r'3 min'),
        dict(tag='Numerical', q=r'On a cold night the ice on a pond grows from zero to 5 cm thick in 2 hours. With the same air temperature, how much longer will it take to become 10 cm thick?',
             steps=[r'\(t\propto x^2\) when starting from zero thickness.',
                    r'Time to reach 10 cm from zero: \(2\times(10/5)^2=8\) h.',
                    r'Extra time \(=8-2=6\) h.'],
             answer=r'6 hours more'),
    ],
    practice=[
        dict(q=r'Two slabs of equal thickness and area, with conductivities κ and 3κ, are placed in series. The equivalent conductivity is',
             options=['4κ', '1.5κ', '2κ', '0.75κ'], answer=1, type='numerical',
             explanation=r'κ_eq = 2κ₁κ₂/(κ₁ + κ₂) = 2·3κ²/4κ = 1.5κ. 4κ simply adds the two conductivities. 2κ is the simple average, the parallel result. 0.75κ forgets the factor 2 from the doubled thickness.'),
        dict(q=r'Ice on a pond grows from 0 to 1 cm thick in 1 hour. Under the same conditions, it grows from 1 cm to 2 cm in',
             options=['3 h', '1 h', '2 h', '4 h'], answer=0, type='numerical',
             explanation=r't ∝ x₂² − x₁², so the time is 1 h × (2² − 1²)/1² = 3 h. 4 h is the total time from zero to 2 cm. 1 h assumes steady growth. 2 h assumes time ∝ thickness.'),
        dict(q=r'Statement I: In the steady state, the temperature at each point of a conducting rod stays constant in time. Statement II: In the steady state, no heat flows through the rod.',
             options=list(ST), answer=2, type='statement',
             explanation=r'Statement I defines the steady state, so it is correct. Statement II is wrong: heat flows at a constant rate. It is only that no part of the rod stores any of it.'),
        dict(q=r'In an Ingenhousz experiment, wax melts along 5 cm of rod A and 10 cm of rod B in the steady state. The ratio κ_A : κ_B is',
             options=['1 : 2', '2 : 1', '1 : √2', '1 : 4'], answer=3, type='numerical',
             explanation=r'κ ∝ ℓ², so κ_A/κ_B = (5/10)² = 1 : 4. 1 : 2 assumes κ ∝ ℓ. 2 : 1 inverts the ratio. 1 : √2 uses ℓ ∝ κ².'),
    ],
),

# ---------------------------------------------------------------- convection
'thermal-properties-convection': dict(
    level='basic',
    notes=[
        ('How convection currents form', r'''<p>Heat a pan of water from below. The bottom layer warms, expands and becomes less dense. Buoyancy lifts it, and cooler, denser water sinks to take its place. The result is a circulating current that carries energy with the moving fluid. This is <strong>natural convection</strong>.</p>
<p>Natural convection needs gravity, because buoyancy needs weight. In an orbiting spacecraft or a freely falling lift there is no natural convection: a candle flame there becomes a dim sphere, starved of fresh air. <strong>Forced convection</strong> uses a fan or pump instead: a room fan, a car’s radiator coolant, blood pumped by the heart.</p>
<p>The rate of convective loss from a surface is roughly \(H=hA(T-T_0)\), where h depends on the fluid and how fast it moves. This linear form is one basis of Newton’s law of cooling.</p>'''),
        ('Convection in daily life and nature', r'''<ul>
<li><strong>Sea breeze</strong> (day): land heats faster than the sea because of its lower specific heat. Air over the land rises and cooler air from the sea flows in along the surface.</li>
<li><strong>Land breeze</strong> (night): land cools faster, so the sea is warmer. The flow reverses and air moves from land to sea.</li>
<li><strong>Trade winds and monsoons</strong>: large-scale convection driven by unequal heating of the Earth.</li>
<li>Heating elements sit at the bottom of a kettle. Freezers and air conditioners sit high up, so cooled air sinks through the space.</li>
<li>A chimney works because hot gases inside are lighter than outside air.</li>
</ul>'''),
        ('Comparing the three modes', r'''<div class="table-wrap"><table>
<thead><tr><th>Mode</th><th>Needs a medium?</th><th>Matter moves in bulk?</th><th>Needs gravity?</th><th>Typical example</th></tr></thead>
<tbody>
<tr><td>Conduction</td><td>Yes</td><td>No</td><td>No</td><td>Spoon handle warming in hot tea</td></tr>
<tr><td>Convection</td><td>Yes, a fluid</td><td>Yes</td><td>Yes, for natural convection</td><td>Sea breeze, boiling water</td></tr>
<tr><td>Radiation</td><td>No</td><td>No</td><td>No</td><td>Sunlight reaching Earth, at the speed of light</td></tr>
</tbody></table></div>'''),
    ],
    formulas=[
        dict(title='Convective heat loss (approximate)',
             formula=r'H=hA\,(T-T_0)',
             symbols='H heat loss rate (W); h convective heat-transfer coefficient (W/m² K), set by the fluid and its speed; A exposed area (m²); T surface temperature and T₀ fluid temperature far away (K or °C differences). Empirical; valid for moderate temperature differences.'),
    ],
    figure=dict(svg=None, caption='Sea breeze by day. Land heats faster, so air rises over it; cooler sea air flows in along the surface, and the loop closes higher up.'),
    traps=[r'Saying the sea breeze blows because the sea is warmer by day. By day the land is warmer; air rises over the land and cooler sea air moves in to replace it.',
           r'Claiming convection happens in solids. Particles of a solid cannot flow, so solids conduct and radiate but do not convect.'],
    exam=r'''<ul>
<li>Direction of sea and land breezes, and the reason (specific heat of land vs water).</li>
<li>Why natural convection stops in a satellite or a freely falling frame.</li>
<li>Match-the-column: process and mode of heat transfer.</li>
<li>Where to place a heater or an air conditioner in a room.</li>
<li>Which mode needs no medium, or is fastest.</li>
</ul>''',
    examples=[
        dict(tag='Concept', q=r'Why is the freezer compartment placed at the top of an ordinary refrigerator?',
             steps=[r'Air near the freezer is cooled, becomes denser and sinks.',
                    r'Warmer air from the lower shelves rises to take its place, is cooled in turn, and sinks.',
                    r'This natural convection current cools the whole cabinet without a fan.'],
             answer=r'So that cooled, denser air sinks and sets up a convection current through the cabinet'),
        dict(tag='Assertion–reason', q=r'Assertion (A): During the day, a breeze blows from the sea towards the land. Reason (R): Land has a lower specific heat than water, so it heats up faster in sunlight. Decide whether A and R are true and whether R explains A.',
             steps=[r'A is true: this is the sea breeze.',
                    r'R is true: dry land warms several times faster than water for the same sunlight.',
                    r'Because land is warmer, air over it expands and rises, and sea air flows in. So R is the cause of A.'],
             answer=r'Both A and R are true, and R correctly explains A'),
        dict(tag='Concept', q=r'An astronaut lights a candle inside an orbiting spacecraft cabin full of air. How does the flame differ from one on Earth?',
             steps=[r'On Earth, hot gases rise by buoyancy, drawing fresh air in from below. This gives the tall, pointed flame.',
                    r'In orbit everything is in free fall, so there is no effective gravity and no buoyancy.',
                    r'Hot gases do not rise. Oxygen reaches the flame only by slow diffusion.',
                    r'The flame becomes nearly spherical, small and dim, and may go out.'],
             answer=r'It becomes a small, dim, roughly spherical flame, because natural convection does not occur'),
    ],
    practice=[
        dict(q=r'At night near a coast, the breeze usually blows',
             options=['From sea to land, because the sea is cooler', 'From land to sea, because the land cools faster',
                      'From land to sea, because the land is warmer', 'Nowhere, because convection stops at night'], answer=1, type='concept',
             explanation=r'At night land loses heat faster than the sea, so the air over the sea is warmer and rises. Cooler air from the land flows out to sea. The sea is warmer at night, not cooler, and the land is cooler, not warmer.'),
        dict(q=r'Statement I: Heat can be transferred by convection through a solid copper block. Statement II: Natural convection needs gravity.',
             options=list(ST), answer=3, type='statement',
             explanation=r'Statement I is false: convection needs bulk flow, which a solid cannot do. Copper transfers heat by conduction. Statement II is true: buoyancy, and so natural convection, depends on gravity.'),
        dict(q=r'Match each process with its main mode of heat transfer. (A) A metal spoon handle warms in hot tea (B) Sea breeze (C) Sunlight warms the Earth (D) A pumped coolant cools a car engine. Modes: (1) radiation (2) conduction (3) natural convection (4) forced convection.',
             options=['A-3, B-2, C-1, D-4', 'A-2, B-4, C-1, D-3', 'A-2, B-3, C-1, D-4', 'A-1, B-3, C-2, D-4'], answer=2, type='match',
             explanation=r'Spoon: conduction (2). Sea breeze: natural convection (3). Sunlight: radiation (1), since space has no medium. Pumped coolant: forced convection (4). The other codes swap conduction with convection, or natural with forced convection.'),
        dict(q=r'To warm a room evenly with a single heater, it is best placed',
             options=['Near the ceiling', 'Anywhere, since radiation dominates', 'Outside the window', 'Near the floor'], answer=3, type='concept',
             explanation=r'Warm air rises. A heater near the floor sets up a convection current through the whole room. Near the ceiling the hot air stays at the top. Radiation alone does not mix the air.'),
    ],
),

# ---------------------------------------------------------------- cooling
'thermal-properties-cooling': dict(
    level='exam',
    notes=[
        ('From Stefan’s law to Newton’s law', r'''<p>A body at T in surroundings at \(T_0\) loses heat by radiation at the net rate \(\varepsilon\sigma A(T^4-T_0^4)\).</p>
<ol>
<li>Factorise: \(T^4-T_0^4=(T^2+T_0^2)(T+T_0)(T-T_0)\).</li>
<li>If T is close to \(T_0\), the first two brackets are about \(2T_0^2\times2T_0=4T_0^3\).</li>
<li>So the loss rate is about \(4\varepsilon\sigma AT_0^3\,(T-T_0)\): proportional to the excess temperature.</li>
<li>Divide by the heat capacity mc: \(\frac{dT}{dt}=-k(T-T_0)\) with \(k=\frac{4\varepsilon\sigma AT_0^3}{mc}\).</li>
</ol>
<p>So k is larger for a larger surface and a smaller heat capacity. The law holds only for small excess temperatures (a few tens of kelvin), though forced convection also gives a roughly linear loss.</p>'''),
        ('Exact form and average-temperature form', r'''<p><strong>Exact form.</strong> Integrating gives \(\ln\frac{T_1-T_0}{T_2-T_0}=kt\). Equal time intervals give equal <em>fractional</em> drops in the excess, as in the figure.</p>
<p><strong>Average form</strong> (the one used in most NEET problems). Replace the changing rate by its value at the mean temperature of the interval:</p>
<p>\[ \frac{T_1-T_2}{t}=K\left[\frac{T_1+T_2}{2}-T_0\right]. \]</p>
<p>The two forms agree closely when the drop \(T_1-T_2\) is small compared with the excess. Use the average form unless the question asks for the logarithmic one or gives ln values.</p>'''),
        ('Cooling graphs and comparing specific heats', r'''<ul>
<li>T against t: an exponential decay that approaches \(T_0\) and never crosses it. Steepest at the start.</li>
<li>\(\ln(T-T_0)\) against t: a straight line of slope −k.</li>
<li>Rate of cooling against \((T-T_0)\): a straight line through the origin.</li>
<li>Rate of cooling against T: a straight line that meets the T axis at \(T_0\).</li>
</ul>
<p><strong>Specific heat by cooling.</strong> Put equal volumes of water and another liquid in identical calorimeters and let them cool through the same range. Same surface and same temperatures give the same rate of heat loss, so \(\frac{m_1c_1+W}{t_1}=\frac{m_2c_2+W}{t_2}\), where W is the calorimeter’s heat capacity.</p>'''),
    ],
    formulas=[
        dict(title='Newton’s law: average-temperature form',
             formula=r'\frac{T_1-T_2}{t}=K\left[\frac{T_1+T_2}{2}-T_0\right]',
             symbols='T₁, T₂ temperatures at the start and end of the interval (°C or K); t time taken (s or min); T₀ surroundings temperature; K cooling constant (per unit time) for that body. Small excess, constant surroundings.'),
        dict(title='Newton’s law: exact form',
             formula=r'\ln\frac{T_1-T_0}{T_2-T_0}=kt',
             symbols='T₁, T₂ temperatures at the start and end; T₀ surroundings temperature; k cooling constant (s⁻¹); t time (s). From dT/dt = −k(T − T₀) with constant k.'),
        dict(title='Comparing specific heats by cooling',
             formula=r'\frac{m_1c_1+W}{t_1}=\frac{m_2c_2+W}{t_2}',
             symbols='m₁, m₂ masses of the two liquids (kg); c₁, c₂ specific heats (J/kg K); W heat capacity of the identical calorimeters (J/K); t₁, t₂ times to cool through the same temperature range (s). Same surface, same surroundings.'),
    ],
    figure=dict(svg=None, caption='Cooling of a body in a room at 20 °C. The excess temperature halves every 5 minutes, so the curve flattens as it approaches room temperature.'),
    traps=[r'Using the starting temperature, instead of the mean of the two temperatures, in the average form.',
           r'Expecting the second 10 °C drop to take as long as the first. The excess is smaller, so cooling is slower and the second drop takes longer.'],
    exam=r'''<ul>
<li>“A body cools from 60 °C to 50 °C in 10 min. How long from 50 °C to 40 °C?” (average form)</li>
<li>Graph matching: which plot is a straight line (ln(T − T₀) vs t, or rate vs excess)?</li>
<li>Specific heat of a liquid from cooling times in identical vessels.</li>
<li>Assertion–reason on the limits of Newton’s law.</li>
<li>Rate of cooling of two bodies of different size or material at the same temperature.</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A body cools from 60 °C to 50 °C in 10 min in a room at 25 °C. How long will it take to cool from 50 °C to 40 °C?',
             steps=[r'First interval: \(\frac{60-50}{10}=K\left(55-25\right)\), so \(K=\frac{1}{30}\) per min.',
                    r'Second interval: \(\frac{50-40}{t}=\frac{1}{30}\left(45-25\right)=\frac{2}{3}\).',
                    r'\(t=10\div\frac23=15\) min.'],
             answer=r'15 min'),
        dict(tag='Concept', q=r'A body cools from 80 °C to 60 °C in 5 min in a room at 20 °C. Find the time to cool from 60 °C to 40 °C using (a) the exact form and (b) the average form.',
             steps=[r'(a) Excess goes 60 → 40 in 5 min, so \(k=\frac{\ln1.5}{5}\). Next, excess 40 → 20: \(t=\frac{\ln2}{k}=5\times\frac{0.693}{0.405}\approx8.55\) min.',
                    r'(b) \(\frac{20}{5}=K(70-20)\) gives \(K=0.08\) per min. Then \(\frac{20}{t}=0.08\times(50-20)=2.4\), so \(t\approx8.33\) min.',
                    r'The average form is slightly off because these drops are large compared with the excess.'],
             answer=r'(a) about 8.5 min (b) about 8.3 min'),
        dict(tag='Graph', q=r'For a body obeying Newton’s law of cooling, which of these plots is a straight line: T vs t, ln(T − T₀) vs t, or rate of cooling vs T?',
             steps=[r'T − T₀ = (T_i − T₀)e^{−kt}, so T vs t is a curve.',
                    r'Taking logs: ln(T − T₀) = ln(T_i − T₀) − kt, a straight line with slope −k.',
                    r'Rate = k(T − T₀) is linear in T, a straight line meeting the T axis at T₀.'],
             answer=r'ln(T − T₀) vs t and rate vs T are straight lines; T vs t is an exponential curve'),
    ],
    practice=[
        dict(q=r'A body cools from 70 °C to 60 °C in 5 min in a room at 30 °C. The time it takes to cool from 60 °C to 50 °C is',
             options=['5 min', '6 min', '7 min', '10 min'], answer=2, type='numerical',
             explanation=r'10/5 = K(65 − 30) gives K = 2/35 per min. Then 10/t = (2/35)(55 − 30) = 50/35, so t = 7 min. 5 min ignores the smaller excess. 10 min doubles the time without calculation.'),
        dict(q=r'For a body cooling according to Newton’s law, the graph of rate of cooling against excess temperature (T − T₀) is',
             options=['A straight line through the origin', 'A parabola opening upward', 'An exponentially decaying curve', 'A horizontal straight line'], answer=0, type='graph',
             explanation=r'Rate = k(T − T₀): directly proportional, so a straight line through the origin. The exponential curve is T against time, not rate against excess. A horizontal line would mean a constant rate.'),
        dict(q=r'Equal masses of water and of a liquid are placed in two identical vessels of negligible heat capacity. Both cool from 50 °C to 40 °C in the same surroundings, taking 10 min and 5 min respectively. If c_water = 4200 J/kg K, the liquid’s specific heat is',
             options=['8400 J/kg K', '2100 J/kg K', '4200 J/kg K', '1050 J/kg K'], answer=1, type='numerical',
             explanation=r'Equal rates of heat loss: mc_w/10 = mc_l/5, so c_l = 4200 × 5/10 = 2100 J/kg K. 8400 J/kg K inverts the time ratio. The liquid cools faster, so its specific heat must be smaller than water’s.'),
        dict(q=r'Assertion (A): In the same room, a body cools from 80 °C to 70 °C faster than from 50 °C to 40 °C. Reason (R): The rate of cooling is proportional to the absolute temperature of the body.',
             options=list(AR), answer=2, type='ar',
             explanation=r'A is true because the excess over the room is larger in the first interval. R is false: the rate is proportional to the excess T − T₀ (for small excess), not to the absolute temperature T.'),
    ],
),
}


NEW_SECTIONS = [

# ---------------------------------------------------------------- thermal stress
dict(chapter='thermal-properties', after='thermal-properties-expansion', id='thermal-properties-stress',
     title='Thermal stress, pendulum clocks and metal scales',
     intro=r'When a heated rod is not free to expand, its supports push back on it. The rod stays at its original length but is now stressed, as if it had been compressed by the amount it wanted to expand. The same small expansion makes pendulum clocks lose time in summer and metal scales read short.',
     reasoning=r'Thermal strain is the expansion that is prevented: αΔθ. Hooke’s law turns that strain into stress YαΔθ, which does not depend on the rod’s length. For a pendulum, period ∝ √L, so a fractional length change αΔθ gives half that fractional change in period.',
     formula=r'\sigma_{\rm th}=Y\alpha\Delta\theta,\quad F=YA\alpha\Delta\theta,\quad \frac{\Delta T}{T}=\tfrac12\alpha\Delta\theta',
     symbols='σ_th thermal stress (Pa); Y Young’s modulus (Pa); α linear coefficient (K⁻¹); Δθ temperature change (K); F force on the supports (N); A cross-section (m²); T pendulum period (s) and ΔT its change. Rigid supports, small αΔθ, stress within the elastic limit.',
     trap=r'Thermal stress does not depend on length. A long rail and a short rail of the same steel, clamped and heated by the same amount, carry the same stress.',
     example=r'A steel rail is clamped at both ends at 20 °C. Find the stress in it at 50 °C. Take Y = 2×10¹¹ Pa and α = 1.2×10⁻⁵ K⁻¹.',
     solution=r'σ = YαΔθ = 2×10¹¹ × 1.2×10⁻⁵ × 30 = 7.2×10⁷ Pa, compressive. Rails are laid with small gaps so that this stress does not buckle them.',
     question=r'Two rods of the same material are clamped between rigid walls and heated equally. Rod P is twice as long and has twice the diameter of rod Q. The ratio of the forces they exert on the walls (P : Q) is',
     options='1 : 1|2 : 1|4 : 1|1 : 4', answer=2,
     explanation=r'F = YAαΔθ does not depend on length. Twice the diameter means four times the area, so the force is four times. The stress YαΔθ is equal in both: 1 : 1 compares stress, not force. 2 : 1 wrongly uses length or diameter linearly.',
     deep=dict(
        level='exam',
        notes=[
            ('Derivation: stress in a clamped rod', r'''<ol>
<li>Imagine one wall removed. The rod would expand freely by \(\Delta L=L\alpha\Delta\theta\).</li>
<li>The wall must push it back by \(\Delta L\) to keep the length fixed.</li>
<li>Compressive strain \(=\Delta L/L=\alpha\Delta\theta\), independent of L.</li>
<li>Stress \(=Y\times\text{strain}=Y\alpha\Delta\theta\). Force on each wall \(F=YA\alpha\Delta\theta\).</li>
</ol>
<p>Cooling a rod that is fixed at both ends gives <em>tension</em> of the same size. The elastic energy stored per unit volume is \(\tfrac12\,\text{stress}\times\text{strain}=\tfrac12Y(\alpha\Delta\theta)^2\). This links this chapter with the elasticity chapter.</p>'''),
            ('Pendulum clocks', r'''<p>A pendulum’s period is \(T=2\pi\sqrt{L/g}\). Heating stretches the rod to \(L(1+\alpha\Delta\theta)\), so \(T\) grows to about \(T(1+\tfrac12\alpha\Delta\theta)\).</p>
<ul>
<li>Hot: longer period, fewer swings per day, so the clock runs <strong>slow</strong> and loses time.</li>
<li>Cold: shorter period, so the clock gains time.</li>
<li>Time lost or gained per day \(=\tfrac12\alpha\,|\Delta\theta|\times86400\) s.</li>
<li>If a clock loses at one temperature and gains at another, you can find both the temperature at which it keeps correct time and α.</li>
<li>A compensated pendulum uses two metals so their expansions cancel: \(L_1\alpha_1=L_2\alpha_2\) keeps the difference \(L_1-L_2\) fixed.</li>
</ul>'''),
            ('Metal scales and everyday stresses', r'''<p>A metal scale is correct at its calibration temperature \(\theta_0\). At a higher temperature each marked centimetre is really a little longer, so the scale <strong>reads too small</strong>. The true length is \(L_{\rm true}=L_{\rm read}\,[1+\alpha_s(\theta-\theta_0)]\). If the scale and the object are the same material and at the same temperature, the reading stays correct.</p>
<p>Other examples: gaps in railway tracks and bridges, telephone wires that sag in summer, and thick glass that cracks when hot water is poured in, because the inner surface expands before the outer one. Borosilicate (Pyrex) glass has a small α, so it resists such cracking.</p>'''),
        ],
        formulas=[
            dict(title='Time lost or gained by a pendulum clock',
                 formula=r'\Delta t=\tfrac12\,\alpha\,|\Delta\theta|\times86400\ \text{s per day}',
                 symbols='Δt time lost (if hotter) or gained (if colder) per day (s); α linear coefficient of the pendulum rod (K⁻¹); Δθ temperature change from the temperature at which the clock is correct (K); 86400 seconds in a day. Small αΔθ.'),
            dict(title='Correcting a metal-scale reading',
                 formula=r'L_{\rm true}=L_{\rm read}\,[1+\alpha_s(\theta-\theta_0)]',
                 symbols='L_true actual length (m); L_read scale reading (m); α_s linear coefficient of the scale (K⁻¹); θ temperature at measurement and θ₀ calibration temperature (°C or K). The object is measured at θ.'),
            dict(title='Constant length difference (compensation)',
                 formula=r'L_1\alpha_1=L_2\alpha_2',
                 symbols='L₁, L₂ lengths of two rods (m); α₁, α₂ their linear coefficients (K⁻¹). Then both expand by the same amount, so L₁ − L₂ is the same at all temperatures.'),
        ],
        figure=dict(svg=None, caption='Top: a free rod expands by ΔL. Bottom: rigid walls push the same rod back by ΔL, giving a compressive strain αΔθ and a stress YαΔθ.'),
        traps=[r'Saying a hot pendulum clock gains time because “longer means more”. A longer pendulum has a longer period, so it makes fewer ticks per day and <em>loses</em> time.',
               r'Correcting a hot metal-scale reading the wrong way. The scale’s marks have spread apart, so the true length is <em>larger</em> than the reading.'],
        exam=r'''<ul>
<li>Thermal stress or force in a rod clamped between walls; ratio for rods of different size.</li>
<li>Time lost per day by a pendulum clock when the temperature rises.</li>
<li>Clock loses at one temperature and gains at another: find the correct-time temperature.</li>
<li>Reading of a steel scale at a different temperature; true length.</li>
<li>Lengths of iron and brass rods whose difference stays constant.</li>
</ul>''',
        examples=[
            dict(tag='Numerical', q=r'A pendulum clock with a brass rod (\(\alpha=2\times10^{-5}\ \mathrm{K^{-1}}\)) keeps correct time at 20 °C. How much time does it lose per day at 40 °C?',
                 steps=[r'Fractional change in period \(=\tfrac12\alpha\Delta\theta=\tfrac12\times2\times10^{-5}\times20=2\times10^{-4}\).',
                        r'Time lost per day \(=2\times10^{-4}\times86400\approx17.3\) s.',
                        r'The period is longer when hot, so the clock runs slow.'],
                 answer=r'About 17.3 s per day'),
            dict(tag='Numerical', q=r'A clock with a metal pendulum loses 12 s a day at 35 °C and gains 8 s a day at 15 °C. At what temperature does it keep correct time, and what is α?',
                 steps=[r'Let it be correct at \(\theta_0\). Loss: \(\tfrac12\alpha(35-\theta_0)\times86400=12\). Gain: \(\tfrac12\alpha(\theta_0-15)\times86400=8\).',
                        r'Divide: \(\frac{35-\theta_0}{\theta_0-15}=1.5\), so \(35-\theta_0=1.5\theta_0-22.5\) and \(\theta_0=23\ ^\circ\mathrm{C}\).',
                        r'Then \(\tfrac12\alpha\times12\times86400=12\), so \(\alpha=\frac{24}{12\times86400}\approx2.3\times10^{-5}\ \mathrm{K^{-1}}\).'],
                 answer=r'23 °C; α ≈ 2.3×10⁻⁵ K⁻¹'),
            dict(tag='Numerical', q=r'A steel scale is correct at 0 °C. At 40 °C it shows the length of a rod as 50.000 cm. What is the true length? (\(\alpha_{\rm steel}=1.2\times10^{-5}\ \mathrm{K^{-1}}\))',
                 steps=[r'At 40 °C each scale centimetre has stretched to \(1+1.2\times10^{-5}\times40=1.00048\) true cm.',
                        r'True length \(=50.000\times1.00048=50.024\) cm.',
                        r'The scale under-reads by 0.024 cm because its own marks have spread apart.'],
                 answer=r'50.024 cm'),
            dict(tag='Ratio', q=r'An iron rod and a brass rod must differ in length by 10 cm at every temperature. Given \(\alpha_{\rm iron}=1.2\times10^{-5}\) and \(\alpha_{\rm brass}=1.8\times10^{-5}\ \mathrm{K^{-1}}\), find their lengths.',
                 steps=[r'Equal expansions: \(L_i\alpha_i=L_b\alpha_b\), so \(L_i/L_b=1.8/1.2=1.5\).',
                        r'The iron rod is the longer one: \(L_i-L_b=10\) cm gives \(0.5L_b=10\).',
                        r'\(L_b=20\) cm and \(L_i=30\) cm.'],
                 answer=r'Iron 30 cm, brass 20 cm'),
        ],
        practice=[
            dict(q=r'A rod of cross-section 2 cm² is clamped between rigid walls and heated by 50 K. With Y = 2×10¹¹ Pa and α = 1×10⁻⁵ K⁻¹, the force on each wall is',
                 options=['2×10³ N', '2×10⁴ N', '2×10⁵ N', '10⁴ N'], answer=1, type='numerical',
                 explanation=r'F = YAαΔθ = 2×10¹¹ × 2×10⁻⁴ × 10⁻⁵ × 50 = 2×10⁴ N. 2×10⁵ N forgets to convert cm² to m² correctly (uses 2×10⁻³). 10⁴ N halves the result, as if the strain were shared between the two walls.'),
            dict(q=r'On a hot summer day, a pendulum clock that is correct in winter',
                 options=['Gains time because its period decreases', 'Keeps correct time because the bob’s mass is unchanged',
                          'Loses time because its period increases', 'Gains time because the rod becomes stiffer'], answer=2, type='concept',
                 explanation=r'Heat lengthens the rod, and T = 2π√(L/g) grows, so the clock makes fewer swings per day and loses time. The period does not depend on the bob’s mass, and stiffness of the rod does not enter the period of a simple pendulum.'),
            dict(q=r'Statement I: The thermal stress in a rod clamped between rigid walls is larger for a longer rod. Statement II: For the same temperature rise, a rod with larger Young’s modulus develops larger thermal stress.',
                 options=list(ST), answer=3, type='statement',
                 explanation=r'Stress = YαΔθ has no length in it, so Statement I is false: a longer rod wants to expand more but its strain αΔθ is the same. Statement II is true, since stress is proportional to Y.'),
            dict(q=r'A clock with a pendulum of α = 2×10⁻⁵ K⁻¹ is correct at 25 °C. At 35 °C, the time it loses in one day is about',
                 options=['8.64 s', '17.28 s', '4.32 s', '86.4 s'], answer=0, type='numerical',
                 explanation=r'Δt = ½ × 2×10⁻⁵ × 10 × 86400 = 8.64 s. 17.28 s forgets the factor ½ from T ∝ √L. 4.32 s halves twice. 86.4 s slips a power of ten.'),
        ],
     )),

# ---------------------------------------------------------------- mixing problems
dict(chapter='thermal-properties', after='thermal-properties-latent', id='thermal-properties-mixing',
     title='Mixing ice, water and steam: finding the final state',
     intro=r'When ice, water or steam are mixed, you cannot write one heat-balance equation straight away. You first need to know which phases remain at the end. The safe method compares the heat the hot part can give with the heat the cold part needs to reach the transition temperature and change phase completely.',
     reasoning=r'Bring everything to the transition temperature in your head. If the hot side can give more heat than the cold side needs to melt all the ice, the final temperature is above 0 °C. If it can give less, the mixture stays at 0 °C with some ice left. Only then write the balance equation with the correct unknown: a final temperature or a mass that changed phase.',
     formula=r'Q_{\rm avail}=m_wc_w(T_w-0),\qquad Q_{\rm need}=m_ic_i(0-T_i)+m_iL_f',
     symbols='Q_avail heat the water can give while cooling to 0 °C (J); Q_need heat the ice needs to warm to 0 °C and melt completely (J); m_w, m_i masses (kg); c_w, c_i specific heats (J/kg K); T_w water temperature and T_i ice temperature (°C, T_i ≤ 0); L_f latent heat of fusion (J/kg). Insulated container of negligible heat capacity unless stated.',
     trap=r'Writing m_wc_w(T_w − T) = m_iL_f + m_ic_wT before checking that all the ice melts. If the hot water cannot supply enough heat, this equation gives a negative T, which is impossible with ice still present.',
     example=r'100 g of ice at 0 °C is mixed with 100 g of water at 80 °C in an insulated container. Find the final state (c_w = 1 cal/g °C, L_f = 80 cal/g).',
     solution=r'The water can give 100 × 1 × 80 = 8000 cal while cooling to 0 °C. Melting all the ice needs 100 × 80 = 8000 cal. These are exactly equal, so all the ice just melts and the final state is 200 g of water at 0 °C.',
     question=r'Equal masses of ice at 0 °C and water at T °C are mixed. The lowest T that melts all the ice is (c_w = 1 cal/g °C, L_f = 80 cal/g)',
     options='40 °C|80 °C|100 °C|160 °C', answer=1,
     explanation=r'Water cooling to 0 °C gives m × 1 × T; melting needs m × 80. So T ≥ 80 °C. 40 °C would melt only half the ice. 160 °C would leave the mixture above 0 °C, so it is more than needed.',
     deep=dict(
        level='exam',
        notes=[
            ('A four-step method for any mixing problem', r'''<ol>
<li><strong>List</strong> every body: mass, phase and starting temperature. Include the calorimeter if given.</li>
<li><strong>Heat available</strong>: how much heat the hot part releases on reaching the transition temperature (0 °C for ice and water, 100 °C for steam and water), including condensation for steam.</li>
<li><strong>Heat needed</strong>: how much the cold part needs to reach that temperature and change phase completely.</li>
<li><strong>Compare and finish</strong>: decide the final state, then write one balance equation with the right unknown.</li>
</ol>
<div class="table-wrap"><table>
<thead><tr><th>Comparison (ice + water)</th><th>Final state</th><th>Unknown to find</th></tr></thead>
<tbody>
<tr><td>Q_avail &gt; Q_need</td><td>All water, above 0 °C</td><td>Final temperature</td></tr>
<tr><td>Q_avail = Q_need</td><td>All water at exactly 0 °C</td><td>Nothing more</td></tr>
<tr><td>Q_avail &lt; Q_need (but enough to warm the ice to 0 °C)</td><td>Ice + water at 0 °C</td><td>Mass of ice melted</td></tr>
<tr><td>Not even enough to warm the ice to 0 °C</td><td>Water may freeze; temperature can end below 0 °C</td><td>Mass frozen or final temperature</td></tr>
</tbody></table></div>'''),
            ('Steam in the mix', r'''<p>One gram of steam at 100 °C gives 540 cal on condensing and up to 100 cal more on cooling to 0 °C: 640 cal in total. One gram of ice at 0 °C needs 80 cal to melt. So <strong>1 g of steam can melt 8 g of ice</strong>, leaving 9 g of water at 0 °C.</p>
<p>For steam + cold water, check the other end. The water can absorb at most \(m_wc_w(100-T_w)\) before it reaches 100 °C. If the steam’s latent heat is larger than that, only part of the steam condenses and the final temperature is 100 °C.</p>'''),
            ('Can a mixture end below 0 °C?', r'''<p>Yes, if the ice is very cold and there is little water. Example: 100 g of ice at −50 °C with 10 g of water at 0 °C (\(c_{\rm ice}=0.5\) cal/g °C).</p>
<ul>
<li>Warming all the ice to 0 °C needs \(100\times0.5\times50=2500\) cal.</li>
<li>Freezing all the water releases only \(10\times80=800\) cal. So all the water freezes.</li>
<li>Now 110 g of ice settles at T: \(800+10\times0.5\times(0-T)=100\times0.5\times(T+50)\), giving \(T\approx-30.9\ ^\circ\mathrm{C}\).</li>
</ul>'''),
        ],
        formulas=[
            dict(title='Steam needed to just melt ice',
                 formula=r'm_s\,(L_v+c_w\times100)=m_iL_f',
                 symbols='m_s mass of steam at 100 °C (kg); m_i mass of ice at 0 °C (kg); L_v, L_f latent heats of vaporisation and fusion (J/kg); c_w specific heat of water (J/kg K); 100 is the temperature drop in K. Final state all water at 0 °C, no losses.'),
            dict(title='Mass of ice melted when not all of it melts',
                 formula=r'm_{\rm melt}=\frac{Q_{\rm avail}-m_ic_i(0-T_i)}{L_f}',
                 symbols='m_melt mass of ice that melts (kg); Q_avail heat the hot water gives in cooling to 0 °C (J); m_i, c_i, T_i mass, specific heat and starting temperature of the ice; L_f latent heat of fusion (J/kg). Valid when 0 ≤ m_melt ≤ m_i; the final temperature is then 0 °C.'),
        ],
        traps=[r'Forgetting the extra 100 cal/g that condensed steam gives as it cools from 100 °C. Steam brings 640 cal/g down to 0 °C water, not 540.',
               r'Assuming the final temperature is the average of the starting temperatures. With a phase change present, check the heat budget first.'],
        exam=r'''<ul>
<li>Ice + water: final temperature, or mass of ice left.</li>
<li>Steam passed into water or onto ice: final temperature, or mass of steam left.</li>
<li>“How much ice must be added to cool the water to 0 °C?” or “minimum steam to melt the ice”.</li>
<li>Statement questions on whether a mixture can end below 0 °C or above 100 °C.</li>
<li>The same problems with a calorimeter of given water equivalent.</li>
</ul>''',
        examples=[
            dict(tag='Numerical', q=r'50 g of ice at −10 °C is added to 100 g of water at 30 °C in an insulated vessel. Find the final state. (c_ice = 0.5, c_w = 1 cal/g °C, L_f = 80 cal/g)',
                 steps=[r'Heat available from the water down to 0 °C: \(100\times1\times30=3000\) cal.',
                        r'Heat to warm the ice to 0 °C: \(50\times0.5\times10=250\) cal. To melt it all: \(50\times80=4000\) cal. Total need: 4250 cal.',
                        r'3000 &lt; 4250, so not all the ice melts and the final temperature is 0 °C.',
                        r'After warming the ice, 3000 − 250 = 2750 cal is left for melting: \(2750/80=34.4\) g melts.',
                        r'Ice left \(=50-34.4=15.6\) g.'],
                 answer=r'0 °C, with about 15.6 g of ice and 134.4 g of water'),
            dict(tag='Numerical', q=r'10 g of steam at 100 °C is passed into an insulated vessel containing 50 g of ice at 0 °C. Find the final temperature. (L_v = 540, L_f = 80 cal/g, c_w = 1 cal/g °C)',
                 steps=[r'Heat the steam can give down to 0 °C: \(10\times(540+100)=6400\) cal.',
                        r'Heat to melt all the ice: \(50\times80=4000\) cal. Since 6400 &gt; 4000, all the ice melts and T is above 0 °C.',
                        r'Balance: \(10\times540+10\times(100-T)=50\times80+50\times T\).',
                        r'\(6400-10T=4000+50T\), so \(60T=2400\) and \(T=40\ ^\circ\mathrm{C}\).'],
                 answer=r'40 °C, all water (60 g)'),
            dict(tag='Numerical', q=r'10 g of steam at 100 °C is passed into 20 g of water at 20 °C. Find the final state. (L_v = 540 cal/g, c_w = 1 cal/g °C)',
                 steps=[r'The water can absorb at most \(20\times1\times80=1600\) cal before reaching 100 °C.',
                        r'All the steam condensing would give \(10\times540=5400\) cal, which is more than 1600 cal.',
                        r'So the final temperature is 100 °C and only \(1600/540=2.96\) g of steam condenses.',
                        r'Steam left \(=10-2.96=7.04\) g; water \(=22.96\) g.'],
                 answer=r'100 °C, with about 7.0 g of steam left over'),
        ],
        practice=[
            dict(q=r'The mass of ice at 0 °C that 1 g of steam at 100 °C can just melt (final state: water at 0 °C) is (L_v = 540, L_f = 80 cal/g)',
                 options=['1 g', '6.75 g', '8 g', '80 g'], answer=2, type='numerical',
                 explanation=r'Steam gives 540 + 100 = 640 cal down to 0 °C, and 640/80 = 8 g of ice melts. 6.75 g uses only the 540 cal of latent heat and forgets the cooling of the condensed water. 80 g confuses heat with mass.'),
            dict(q=r'0.1 kg of water at 50 °C is mixed with 0.05 kg of ice at 0 °C. The final temperature is (c_w = 4200 J/kg K, L_f = 3.36×10⁵ J/kg)',
                 options=['0 °C with some ice left', '6.7 °C', '16.7 °C', '33.3 °C'], answer=1, type='numerical',
                 explanation=r'Water gives 21000 J down to 0 °C; melting needs 16800 J, so all the ice melts. Then 0.1×4200×(50 − T) = 16800 + 0.05×4200×T gives T = 6.7 °C. 33.3 °C ignores latent heat. The first option fails because 21000 J exceeds 16800 J.'),
            dict(q=r'Statement I: A mixture of ice and water in an insulated container can never end at a temperature below 0 °C. Statement II: At 1 atm, if some steam remains after mixing with water, the final temperature is 100 °C.',
                 options=list(ST), answer=3, type='statement',
                 explanation=r'Statement I is false: very cold ice can freeze all the water and the mixture can end below 0 °C. Statement II is true: steam and water can coexist at 1 atm only at 100 °C.'),
            dict(q=r'How much ice at 0 °C must be added to 300 g of water at 40 °C so that the final state is all water at 0 °C? (c_w = 1 cal/g °C, L_f = 80 cal/g)',
                 options=['150 g', '120 g', '300 g', '240 g'], answer=0, type='numerical',
                 explanation=r'The water gives 300 × 40 = 12000 cal on cooling to 0 °C, which melts 12000/80 = 150 g of ice. 300 g assumes equal masses. 120 g divides by 100 instead of 80. 240 g doubles the answer without reason.'),
        ],
     )),

# ---------------------------------------------------------------- radiation laws
dict(chapter='thermal-properties', after='thermal-properties-convection', id='thermal-properties-radiation',
     title='Radiation laws: Stefan–Boltzmann, Wien and Kirchhoff',
     intro=r'Every body above absolute zero emits electromagnetic radiation, and the amount rises steeply with temperature. A perfect black body absorbs all radiation that falls on it and, at a given temperature, emits the most any body can. Real surfaces emit a fraction ε, the emissivity, of the black-body amount.',
     reasoning=r'Two laws describe black-body radiation. The total power per unit area grows as T⁴ (Stefan–Boltzmann). The wavelength at which the spectrum peaks varies as 1/T (Wien). A body also absorbs radiation from its surroundings, so its net loss depends on T⁴ − T₀⁴.',
     formula=r'E=\varepsilon\sigma T^4,\quad P_{\rm net}=\varepsilon\sigma A\,(T^4-T_0^4),\quad \lambda_mT=b',
     symbols='E power emitted per unit area (W/m²); ε emissivity (0 to 1; 1 for a black body); σ = 5.67×10⁻⁸ W m⁻² K⁻⁴; T body and T₀ surroundings temperatures (K); A surface area (m²); λ_m wavelength of peak emission (m); b ≈ 2.9×10⁻³ m K (Wien constant). Kelvin is essential.',
     trap=r'Using Celsius in T⁴. Heating a black body from 27 °C to 327 °C multiplies its emitted power by (600/300)⁴ = 16, not by (327/27)⁴.',
     example=r'The spectrum of a star peaks at λ_m = 480 nm. Estimate its surface temperature (b = 2.9×10⁻³ m K).',
     solution=r'T = b/λ_m = 2.9×10⁻³ / 4.8×10⁻⁷ ≈ 6.0×10³ K. This is close to the surface temperature of the Sun.',
     question=r'The spectra of two black bodies peak at 400 nm and 800 nm. The ratio of the power they emit per unit area (first : second) is',
     options='2 : 1|4 : 1|16 : 1|1 : 16', answer=2,
     explanation=r'Wien: T ∝ 1/λ_m, so T₁/T₂ = 800/400 = 2. Stefan: E ∝ T⁴, so the ratio is 2⁴ = 16 : 1. 2 : 1 compares temperatures only. 1 : 16 inverts the ratio by using wavelengths directly.',
     deep=dict(
        level='exam',
        notes=[
            ('Absorptivity, emissivity and Kirchhoff’s law', r'''<p>Radiation falling on a surface is partly absorbed (fraction a), reflected (r) and transmitted (t), with \(a+r+t=1\). A <strong>black body</strong> has \(a=1\). Emissivity \(\varepsilon\) compares a surface’s emission with a black body’s at the same temperature.</p>
<p><strong>Kirchhoff’s law</strong>: at a given temperature and wavelength, the ratio of emissive power to absorptivity is the same for all bodies and equals the black-body emissive power. So \(\varepsilon=a\): <em>good absorbers are good emitters, and good reflectors are poor emitters</em>.</p>
<ul>
<li>A plate with a black pattern on white china, heated in a dark room, shows the black pattern glowing brighter.</li>
<li>A thermos flask has silvered walls: they reflect radiation and emit little.</li>
<li>Light-coloured clothes are cooler in summer because they absorb less sunlight.</li>
<li>A small hole in a blackened cavity behaves as a near-perfect black body (Ferry’s black body). Inside a furnace, all objects glow alike and their details vanish.</li>
</ul>'''),
            ('Stefan–Boltzmann law and the rate of cooling', r'''<p>A body emits \(\varepsilon\sigma AT^4\) and absorbs \(\varepsilon\sigma AT_0^4\) from surroundings at \(T_0\). Even at \(T=T_0\) it still emits; it simply absorbs the same amount, so the net power is zero (Prevost’s theory of exchanges).</p>
<p>The rate of fall of temperature is \(-\frac{dT}{dt}=\frac{\varepsilon\sigma A}{mc}(T^4-T_0^4)\). Two common comparisons:</p>
<ul>
<li>Solid spheres of the same material at the same T: \(A/m=\frac{4\pi r^2}{\rho\cdot\frac43\pi r^3}=\frac{3}{\rho r}\), so the cooling rate \(\propto1/r\). The smaller sphere cools faster.</li>
<li>A hollow and a solid sphere of the same radius and material: same emission at first, but the hollow one has less mass, so it cools faster.</li>
</ul>
<p>A star of radius R radiates a total power (luminosity) \(L=4\pi R^2\sigma T^4\). For a small excess, \(T^4-T_0^4\approx4T_0^3(T-T_0)\), which leads to Newton’s law of cooling in the next section.</p>'''),
            ('Wien’s law and the shape of the spectrum', r'''<p>Plot the power emitted per unit wavelength against wavelength (see the figure). At a higher temperature:</p>
<ul>
<li>the curve lies higher at <em>every</em> wavelength, so curves at different temperatures never cross;</li>
<li>the peak moves to a shorter wavelength, \(\lambda_m\propto1/T\);</li>
<li>the area under the curve, which is the total power per unit area, grows as \(T^4\).</li>
</ul>
<p>So heated iron glows dull red, then orange, then yellow-white. Blue stars are hotter than red stars. The Sun peaks near 500 nm, giving about 5800 K. The human body at 310 K peaks near 9.4 μm, in the infrared, which is why thermal cameras work in the infrared.</p>'''),
        ],
        formulas=[
            dict(title='Kirchhoff’s law',
                 formula=r'\frac{E_\lambda}{a_\lambda}=E_{\lambda,\rm black},\qquad \varepsilon=a',
                 symbols='E_λ emissive power of a body at wavelength λ (W/m² per m); a_λ its absorptivity at λ (0 to 1); E_λ,black black-body emissive power at the same λ and T; ε emissivity and a absorptivity of a grey surface. Same temperature for the comparison.'),
            dict(title='Rate of cooling by radiation',
                 formula=r'-\frac{dT}{dt}=\frac{\varepsilon\sigma A}{mc}\left(T^4-T_0^4\right)',
                 symbols='dT/dt rate of change of temperature (K/s); ε emissivity; σ Stefan–Boltzmann constant (W m⁻² K⁻⁴); A area (m²); m mass (kg); c specific heat (J/kg K); T, T₀ body and surroundings temperatures (K). Uniform body temperature; radiation only.'),
            dict(title='Luminosity of a star',
                 formula=r'L=4\pi R^2\sigma T^4',
                 symbols='L total power radiated (W); R radius of the star (m); σ Stefan–Boltzmann constant; T surface temperature (K). Star treated as a spherical black body.'),
        ],
        figure=dict(svg=None, caption='Black-body spectra at 5000 K and 4000 K, calculated from Planck’s law. The hotter curve lies higher everywhere and peaks at a shorter wavelength; its area is (5/4)⁴ ≈ 2.4 times larger.'),
        traps=[r'Thinking a body at the same temperature as its surroundings stops radiating. It still emits εσAT⁴; it absorbs exactly as much, so only the <em>net</em> power is zero.',
               r'Treating λ_m as the only wavelength emitted. A hot body emits a continuous spread of wavelengths; λ_m is just where the curve peaks.'],
        exam=r'''<ul>
<li>Ratio of power radiated when the temperature changes (convert to kelvin first).</li>
<li>Temperature of a star or the Sun from λ_m; ratio of temperatures from two λ_m values.</li>
<li>Net power lost to surroundings, εσA(T⁴ − T₀⁴).</li>
<li>Rate of cooling of spheres of different radius, or hollow vs solid spheres.</li>
<li>Graph: identify the hotter body from spectrum curves; what happens to the peak and the area.</li>
<li>Assertion–reason on Kirchhoff’s law: good absorbers are good emitters.</li>
</ul>''',
        examples=[
            dict(tag='Ratio', q=r'A black body is heated from 27 °C to 327 °C. By what factor does its emitted power increase, and how does λ_m change?',
                 steps=[r'Convert: 27 °C = 300 K and 327 °C = 600 K. The absolute temperature doubles.',
                        r'Power \(\propto T^4\): factor \(2^4=16\).',
                        r'\(\lambda_m\propto1/T\): the peak wavelength halves.'],
                 answer=r'Power becomes 16 times; λ_m becomes half'),
            dict(tag='Numerical', q=r'A person with skin area 1.5 m² and skin temperature 310 K sits in a room at 300 K. Treating the skin as a black body (ε ≈ 1), estimate the net power lost by radiation. (σ = 5.67×10⁻⁸ W m⁻² K⁻⁴)',
                 steps=[r'\(P_{\rm net}=\sigma A(T^4-T_0^4)=5.67\times10^{-8}\times1.5\times(310^4-300^4)\).',
                        r'\(310^4-300^4\approx1.135\times10^9\ \mathrm{K^4}\).',
                        r'\(P_{\rm net}\approx97\ \mathrm{W}\). The small-excess form \(4\sigma AT_0^3\Delta T\) gives about 92 W, close because 10 K is small compared with 300 K.'],
                 answer=r'About 97 W'),
            dict(tag='Ratio', q=r'Two solid spheres of the same material have radii r and 2r and are at the same temperature in the same surroundings. Compare (a) the power they radiate and (b) their initial rates of fall of temperature.',
                 steps=[r'(a) Power \(\propto A\propto r^2\): ratio \(1:4\).',
                        r'(b) Rate of cooling \(\propto\frac{A}{mc}\propto\frac{r^2}{r^3}=\frac1r\): ratio \(2:1\).',
                        r'The larger sphere radiates more in total but cools more slowly, because its mass grows faster than its area.'],
                 answer=r'(a) 1 : 4 (b) 2 : 1'),
            dict(tag='Graph', q=r'The spectra of two black bodies peak at 1.0 μm (body 1) and 1.5 μm (body 2). Which is hotter, and what is the ratio of the total power per unit area they emit?',
                 steps=[r'Wien: \(T\propto1/\lambda_m\), so \(T_1/T_2=1.5/1.0=1.5\). Body 1 is hotter.',
                        r'Stefan: \(E\propto T^4\), so \(E_1/E_2=1.5^4\approx5.06\).',
                        r'On the graph, body 1’s curve peaks further left and encloses about five times the area.'],
                 answer=r'Body 1 is hotter; E₁ : E₂ ≈ 5.1 : 1'),
        ],
        practice=[
            dict(q=r'Assertion (A): A polished silver surface is a poor emitter of thermal radiation. Reason (R): A good reflector is a poor absorber, and by Kirchhoff’s law a poor absorber is a poor emitter.',
                 options=list(AR), answer=0, type='ar',
                 explanation=r'Both are true, and R explains A: silver reflects most radiation, so its absorptivity is small, and Kirchhoff’s law makes its emissivity equally small. This is why thermos flasks are silvered.'),
            dict(q=r'A black body radiates 20 W at 227 °C. At 727 °C it radiates',
                 options=['40 W', '80 W', '2.1×10³ W', '320 W'], answer=3, type='numerical',
                 explanation=r'In kelvin the temperature goes from 500 K to 1000 K, a factor 2, so the power rises by 2⁴ = 16: 320 W. 2.1×10³ W uses (727/227)⁴ with Celsius values. 40 W and 80 W use powers 1 and 2 instead of 4.'),
            dict(q=r'The spectral curves of two black bodies at temperatures T₁ > T₂ are compared. Which statement is correct?',
                 options=['The T₁ curve peaks at a longer wavelength and encloses a smaller area',
                          'Both curves peak at the same wavelength',
                          'The T₁ curve peaks at a shorter wavelength and encloses a larger area',
                          'The T₁ curve lies below the T₂ curve at long wavelengths'], answer=2, type='graph',
             explanation=r'Wien: the hotter body peaks at a shorter wavelength. Stefan: the area (total power) grows as T⁴. Black-body curves at different temperatures never cross, so the hotter curve is higher at every wavelength, which rules out the last option.'),
            dict(q=r'Two solid copper spheres of radii 1 cm and 2 cm are heated to the same temperature and left in the same room. The ratio of their initial rates of fall of temperature (small : large) is',
                 options=['1 : 4', '1 : 2', '4 : 1', '2 : 1'], answer=3, type='numerical',
                 explanation=r'Rate ∝ A/(mc) ∝ r²/r³ = 1/r, so the ratio is 2 : 1. 1 : 4 compares radiated power (∝ r²), not the rate of temperature fall. 1 : 2 inverts the answer.'),
        ],
     )),
]


# Attach the figures (generated with computed curves; see module docstring).
DEEP['thermal-properties-expansion']['figure']['svg'] = _FIGS['bimetal']
DEEP['thermal-properties-liquids']['figure']['svg'] = _FIGS['water']
DEEP['thermal-properties-latent']['figure']['svg'] = _FIGS['heating']
DEEP['thermal-properties-conduction']['figure']['svg'] = _FIGS['slab']
DEEP['thermal-properties-convection']['figure']['svg'] = _FIGS['breeze']
DEEP['thermal-properties-cooling']['figure']['svg'] = _FIGS['cooling']
NEW_SECTIONS[0]['deep']['figure']['svg'] = _FIGS['clamped']
NEW_SECTIONS[2]['deep']['figure']['svg'] = _FIGS['bb']
