"""Deepening layer: Units and Measurements (chapter key 'units')."""
R = str


# ---------- small SVG helpers (light theme, CSS variables) ----------
def _line(x1, y1, x2, y2, color='ink-2', w=1.5, dash=False):
    d = ';stroke-dasharray:4 3' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" style="stroke:var(--{color});stroke-width:{w}{d}"/>'


def _text(x, y, s, color='ink-2', size=12, anchor='start', weight='normal'):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" style="fill:var(--{color});font-size:{size}px;font-weight:{weight}">{s}</text>'


def _dot(x, y, color='coral', r=4):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" style="fill:var(--{color})"/>'


def _rect(x, y, w, h, fill='surface-2', stroke='line-2', rx=0):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" style="fill:var(--{fill});stroke:var(--{stroke});stroke-width:1.2"/>'


def _svg(w, h, label, body):
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}">{body}</svg>'


def _fig_parallax():
    ax, ay, bx, by, sx, sy = 40, 40, 40, 200, 350, 120
    b = _line(ax, ay, sx, sy, 'indigo', 1.8) + _line(bx, by, sx, sy, 'indigo', 1.8)
    b += _line(ax, ay, bx, by, 'coral', 2.4)
    b += _dot(ax, ay, 'coral') + _dot(bx, by, 'coral') + _dot(sx, sy, 'amber', 6)
    b += _text(ax - 6, ay - 8, 'A', anchor='middle') + _text(bx - 6, by + 18, 'B', anchor='middle')
    b += _text(sx + 8, sy + 26, 'S (distant object)', 'ink-2', 12, 'end')
    b += _text(ax - 12, 124, 'b', 'coral', 14, 'end', 'bold')
    b += '<path d="M 312 110.3 A 40 40 0 0 0 312 129.7" style="fill:none;stroke:var(--ink-2);stroke-width:1.4"/>'
    b += _text(300, 125, 'θ', 'ink-2', 14, 'end')
    b += _line(60, 120, 290, 120, 'muted', 1, True)
    b += _text(175, 114, 'D', 'muted', 13, 'middle')
    b += _text(195, 230, 'D = b / θ  (θ in radians, D ≫ b)', 'ink-2', 12.5, 'middle')
    return _svg(380, 240, 'Parallax: two observation points A and B a baseline b apart see a distant object S along lines that meet at a small angle theta', b)


def _fig_sigfig():
    digits = list('0.0040500')
    kinds = ['lead', 'pt', 'lead', 'lead', 'sig', 'mid', 'sig', 'trail', 'trail']
    col = {'lead': ('surface-2', 'muted'), 'pt': ('surface', 'ink-2'), 'sig': ('green-soft', 'green'),
           'mid': ('green-soft', 'green'), 'trail': ('amber-soft', 'amber')}
    b = ''
    x = 30
    for d, k in zip(digits, kinds):
        w = 18 if k == 'pt' else 36
        fill, ink = col[k]
        if k != 'pt':
            b += _rect(x, 50, w - 4, 46, fill, 'line-2', 6)
        b += _text(x + (w - 4) / 2, 82, d, ink, 24, 'middle', 'bold')
        x += w
    b += _line(30, 108, 136, 108, 'muted', 1.2) + _text(83, 124, 'leading zeros: only', 'muted', 11.5, 'middle') + _text(83, 138, 'place the decimal', 'muted', 11.5, 'middle')
    b += _text(83, 152, '(not significant)', 'muted', 11.5, 'middle')
    b += _line(140, 108, 246, 108, 'green', 1.2) + _text(193, 124, '4, 5 and the zero', 'green', 11.5, 'middle') + _text(193, 138, 'between them', 'green', 11.5, 'middle')
    b += _line(248, 108, 318, 108, 'amber', 1.2) + _text(284, 124, 'trailing zeros', 'amber', 11.5, 'middle') + _text(284, 138, 'after the point', 'amber', 11.5, 'middle')
    b += _text(284, 152, '(significant)', 'amber', 11.5, 'middle')
    b += _text(175, 30, '0.0040500 = 4.0500 × 10⁻³ → 5 significant figures', 'ink-2', 13, 'middle')
    return _svg(350, 168, 'The number 0.0040500 with three leading zeros marked not significant and the digits 4 0 5 0 0 marked significant', b)


def _fig_targets():
    import random
    rnd = random.Random(7)
    sets = [('Accurate|and precise', 0, 0, 5), ('Precise,|not accurate', 18, -14, 5),
            ('Accurate,|not precise', 0, 0, 22), ('Neither accurate|nor precise', 16, 12, 22)]
    b = ''
    for i, (lab, dx, dy, spread) in enumerate(sets):
        cx, cy = 52 + i * 96, 70
        for r, fill in [(40, 'surface-2'), (27, 'surface'), (14, 'surface-2')]:
            b += f'<circle cx="{cx}" cy="{cy}" r="{r}" style="fill:var(--{fill});stroke:var(--line-2);stroke-width:1.2"/>'
        b += _dot(cx, cy, 'ink-2', 2)
        import math
        for k in range(5):
            ang = 6.283 * k / 5 + 0.4 + rnd.uniform(-0.2, 0.2)
            rad = spread * (0.65 + 0.35 * (k % 2))
            b += _dot(cx + dx + rad * math.cos(ang), cy + dy + rad * math.sin(ang), 'coral', 3.2)
        l1, l2 = lab.split('|')
        b += _text(cx, 126, l1, 'ink-2', 11, 'middle') + _text(cx, 140, l2, 'ink-2', 11, 'middle')
    b += _text(196, 162, 'centre = true value; dots = repeated readings', 'muted', 11.5, 'middle')
    return _svg(392, 172, 'Four targets showing readings that are accurate and precise, precise but not accurate, accurate but not precise, and neither', b)


def _fig_vernier():
    X = lambda mm: 30 + (mm - 19) * 20
    b = _rect(20, 30, 340, 46, 'surface-2', 'line-2')
    b += _rect(X(23.7) - 10, 78, 208, 46, 'water-soft', 'line-2')
    for mm in range(19, 36):
        h = 22 if mm % 10 == 0 else (16 if mm % 5 == 0 else 10)
        col = 'coral' if mm == 30 else 'ink-2'
        b += _line(X(mm), 76, X(mm), 76 - h, col, 2.2 if mm == 30 else 1.2)
    b += _text(X(20), 44, '2', 'ink-2', 13, 'middle', 'bold') + _text(X(30), 44, '3', 'ink-2', 13, 'middle', 'bold')
    b += _text(352, 44, 'main scale (cm)', 'muted', 11, 'end')
    for k in range(11):
        x = X(23.7 + 0.9 * k)
        h = 18 if k % 5 == 0 else 11
        col = 'coral' if k == 7 else 'ink-2'
        b += _line(x, 78, x, 78 + h, col, 2.2 if k == 7 else 1.2)
    for k in (0, 5, 10):
        b += _text(X(23.7 + 0.9 * k), 112, str(k), 'ink-2', 12, 'middle')
    b += _text(X(23.7) - 14, 104, 'vernier', 'muted', 11, 'end')
    b += _text(X(30), 140, '7th vernier mark lines up', 'coral', 11.5, 'middle')
    b += _text(190, 160, 'Reading = 2.3 cm + 7 × 0.01 cm = 2.37 cm', 'ink-2', 12.5, 'middle')
    return _svg(380, 170, 'Vernier calipers: vernier zero just past 2.3 cm on the main scale, and the seventh vernier mark lines up with a main scale mark', b)


def _fig_screw():
    X = lambda mm: 34 + mm * 40
    edge = X(4.78)
    b = _rect(20, 70, edge - 20, 60, 'surface-2', 'line-2')
    b += _line(20, 100, edge, 100, 'ink-2', 1.6)
    for mm in range(0, 5):
        b += _line(X(mm), 100, X(mm), 82, 'ink-2', 1.4) + _text(X(mm), 78, str(mm), 'ink-2', 12, 'middle')
    for k in range(5):
        b += _line(X(k + 0.5), 100, X(k + 0.5), 114, 'ink-2', 1.2)
    b += _line(X(4.5), 100, X(4.5), 116, 'coral', 2.2)
    b += _rect(edge, 30, 110, 140, 'water-soft', 'line-2', 4)
    for d in range(22, 35):
        y = 100 - (d - 28) * 8
        long_ = d % 5 == 0
        col = 'coral' if d == 28 else 'ink-2'
        b += _line(edge, y, edge + (18 if long_ or d == 28 else 11), y, col, 2.2 if d == 28 else 1.2)
        if long_ or d == 28:
            b += _text(edge + 22, y + 4, str(d), col, 11.5)
    b += _text(edge + 104, 54, 'thimble', 'muted', 11, 'end')
    b += _text(26, 148, 'sleeve: mm above, half-mm below', 'muted', 11)
    b += _text(190, 196, 'pitch 0.5 mm, 50 divisions → LC = 0.01 mm', 'ink-2', 12, 'middle')
    b += _text(190, 214, 'Reading = 4.5 mm + 28 × 0.01 mm = 4.78 mm', 'ink-2', 12.5, 'middle')
    return _svg(380, 224, 'Screw gauge: the thimble edge is just past the 4.5 millimetre mark and circular division 28 lies on the reference line', b)


AR_OPTS = ['Both A and R are true, and R correctly explains A',
           'Both A and R are true, but R does not explain A',
           'A is true but R is false',
           'A is false but R is true']
ST_OPTS = ['Both statements are true',
           'Both statements are false',
           'Statement I is true, Statement II is false',
           'Statement I is false, Statement II is true']


DEEP = {
'units-si': dict(
    level='basic',
    notes=[
        ('Base units, prefixes and practical units', r'''<div class="table-wrap"><table><thead><tr><th>Base quantity</th><th>SI unit</th><th>Symbol</th></tr></thead><tbody>
<tr><td>Length</td><td>metre</td><td>m</td></tr><tr><td>Mass</td><td>kilogram</td><td>kg</td></tr><tr><td>Time</td><td>second</td><td>s</td></tr>
<tr><td>Electric current</td><td>ampere</td><td>A</td></tr><tr><td>Thermodynamic temperature</td><td>kelvin</td><td>K</td></tr>
<tr><td>Amount of substance</td><td>mole</td><td>mol</td></tr><tr><td>Luminous intensity</td><td>candela</td><td>cd</td></tr></tbody></table></div>
<p>The radian (plane angle) and steradian (solid angle) were once called supplementary units. Both are dimensionless.</p>
<p><strong>Prefixes:</strong> femto \(10^{-15}\), pico \(10^{-12}\), nano \(10^{-9}\), micro \(10^{-6}\), milli \(10^{-3}\), centi \(10^{-2}\), kilo \(10^{3}\), mega \(10^{6}\), giga \(10^{9}\), tera \(10^{12}\).</p>
<p><strong>Practical length units:</strong> 1 fermi = \(10^{-15}\) m; 1 ångström = \(10^{-10}\) m; 1 micron = \(10^{-6}\) m; 1 AU = \(1.496\times10^{11}\) m; 1 light year = \(9.46\times10^{15}\) m; 1 parsec = \(3.08\times10^{16}\) m = 3.26 light years.</p>'''),
        ('Energy and other everyday conversions', r'''<ul><li>1 kWh = 1000 W × 3600 s = \(3.6\times10^{6}\) J</li>
<li>1 eV = \(1.6\times10^{-19}\) J</li>
<li>1 erg = \(10^{-7}\) J; 1 dyne = \(10^{-5}\) N</li>
<li>1 calorie ≈ 4.2 J; 1 atm ≈ \(1.013\times10^{5}\) Pa</li>
<li>1 amu ≈ \(1.66\times10^{-27}\) kg</li></ul>
<p>Write symbols correctly: 5 kg, not 5 kgs or 5 Kg. A unit named after a person is lower case in words (newton) and capital in symbol (N).</p>'''),
    ],
    formulas=[
        dict(title='Astronomical distance units', formula=r'1\ \text{ly}=9.46\times10^{15}\ \text{m},\quad 1\ \text{AU}=1.496\times10^{11}\ \text{m},\quad 1\ \text{pc}=3.08\times10^{16}\ \text{m}=3.26\ \text{ly}',
             symbols='ly is the light year (distance light travels in one year), AU is the mean Earth–Sun distance, pc is the parsec (distance at which 1 AU subtends 1 arc second). All three are lengths.'),
        dict(title='Energy units', formula=r'1\ \text{kWh}=3.6\times10^{6}\ \text{J},\quad 1\ \text{eV}=1.6\times10^{-19}\ \text{J},\quad 1\ \text{erg}=10^{-7}\ \text{J}',
             symbols='kWh is the commercial unit of electrical energy; eV is the energy gained by an electron through 1 V; erg is the CGS unit of energy.'),
    ],
    traps=[r'A light year is a unit of <strong>distance</strong>, not time. So are the parsec and the astronomical unit.',
           r'The kilowatt-hour is a unit of energy, while the kilowatt is a unit of power. Electricity bills charge for energy.'],
    exam=r'''<ul><li>"Which of the following is not a unit of length / energy / an SI base unit?"</li>
<li>"1 kWh equals … J" or "… eV".</li>
<li>Match-the-column of fermi, ångström, AU and light year with their values.</li>
<li>"Parsec is a unit of …" (distance).</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'Express 1 kWh in joules and in electron-volts.',
             steps=[r'1 kW = 1000 W = 1000 J/s and 1 h = 3600 s.',
                    r'1 kWh = 1000 × 3600 = \(3.6\times10^{6}\) J.',
                    r'In eV: \(\dfrac{3.6\times10^{6}}{1.6\times10^{-19}}=2.25\times10^{25}\) eV.'],
             answer=r'\(3.6\times10^{6}\) J = \(2.25\times10^{25}\) eV'),
        dict(tag='Concept', q=r'Which of these is not a unit of energy: erg, electron-volt, kilowatt-hour, watt?',
             steps=[r'erg is the CGS energy unit; eV and kWh are energy units too.',
                    r'The watt is J/s, a rate of energy transfer. It is a unit of power.'],
             answer=r'Watt'),
        dict(tag='Numerical', q=r'How many astronomical units make one light year?',
             steps=[r'\(\dfrac{1\ \text{ly}}{1\ \text{AU}}=\dfrac{9.46\times10^{15}}{1.496\times10^{11}}\).',
                    r'This is about \(6.3\times10^{4}\).'],
             answer=r'About 63 000 AU'),
    ],
    practice=[
        dict(q=r'Which of the following is not an SI base unit?',
             options=['kelvin', 'candela', 'newton', 'mole'], answer=2, type='concept',
             explanation=r'The newton is derived: 1 N = 1 kg m s⁻². Kelvin, candela and mole are three of the seven base units, even though they are less familiar than the metre or second.'),
        dict(q=r'1 kWh expressed in electron-volts is about',
             options=[r'\(5.8\times10^{-13}\) eV', r'\(3.6\times10^{6}\) eV', r'\(2.25\times10^{19}\) eV', r'\(2.25\times10^{25}\) eV'], answer=3, type='numerical',
             explanation=r'\(3.6\times10^{6}\ \text{J}\div1.6\times10^{-19}\ \text{J/eV}=2.25\times10^{25}\) eV. \(3.6\times10^{6}\) is the value in joules, not eV. \(5.8\times10^{-13}\) multiplies by the eV value instead of dividing.'),
        dict(q=r'Match: (a) fermi (b) ångström (c) astronomical unit (d) light year with (i) \(1.5\times10^{11}\) m (ii) \(9.46\times10^{15}\) m (iii) \(10^{-15}\) m (iv) \(10^{-10}\) m.',
             options=['a-iii, b-iv, c-i, d-ii', 'a-iv, b-iii, c-i, d-ii', 'a-iii, b-iv, c-ii, d-i', 'a-i, b-ii, c-iii, d-iv'], answer=0, type='match',
             explanation=r'The fermi is nuclear scale (\(10^{-15}\) m) and the ångström is atomic scale (\(10^{-10}\) m). The AU is the Earth–Sun distance and the light year is far larger. Option 2 swaps the two small units; option 3 swaps the two large ones.'),
        dict(q=r'A parsec is a unit of',
             options=['Time', 'Distance', 'Angle', 'Speed'], answer=1, type='concept',
             explanation=r'A parsec is the distance at which 1 AU subtends an angle of one arc second, about \(3.08\times10^{16}\) m. It is defined using an angle but measures distance. The word "year" in light year misleads students the same way.'),
    ],
),

'units-dimensions': dict(
    level='core',
    notes=[
        ('Dimensions you must know by heart', r'''<div class="table-wrap"><table><thead><tr><th>Quantity</th><th>Dimensions</th><th>Quantity</th><th>Dimensions</th></tr></thead><tbody>
<tr><td>Velocity</td><td>\(LT^{-1}\)</td><td>Acceleration</td><td>\(LT^{-2}\)</td></tr>
<tr><td>Force</td><td>\(MLT^{-2}\)</td><td>Momentum, impulse</td><td>\(MLT^{-1}\)</td></tr>
<tr><td>Work, energy, torque</td><td>\(ML^2T^{-2}\)</td><td>Power</td><td>\(ML^2T^{-3}\)</td></tr>
<tr><td>Pressure, stress, modulus, energy density</td><td>\(ML^{-1}T^{-2}\)</td><td>Surface tension, spring constant</td><td>\(MT^{-2}\)</td></tr>
<tr><td>Angular momentum, Planck constant</td><td>\(ML^2T^{-1}\)</td><td>Viscosity \(\eta\)</td><td>\(ML^{-1}T^{-1}\)</td></tr>
<tr><td>Gravitational constant G</td><td>\(M^{-1}L^3T^{-2}\)</td><td>Frequency, angular velocity</td><td>\(T^{-1}\)</td></tr>
<tr><td>Specific heat</td><td>\(L^2T^{-2}K^{-1}\)</td><td>Latent heat</td><td>\(L^2T^{-2}\)</td></tr>
<tr><td>Thermal conductivity</td><td>\(MLT^{-3}K^{-1}\)</td><td>Strain, angle, refractive index</td><td>dimensionless</td></tr></tbody></table></div>'''),
        ('Homogeneity and the arguments of functions', r'''<p>Only like quantities can be added, subtracted or equated. So every term in a correct equation has the same dimensions. Arguments of \(\sin\), \(\cos\), \(e^x\) and \(\log\) must be dimensionless.</p>
<ul><li>In \(y=A\sin(\omega t-kx)\): \([\omega]=T^{-1}\), \([k]=L^{-1}\), so \(\omega/k\) has dimensions \(LT^{-1}\), a speed.</li>
<li>In van der Waals&#39; equation \(\left(P+\dfrac{a}{V^2}\right)(V-b)=RT\): \(b\) is a volume (\(L^3\)) and \(a/V^2\) is a pressure, so \([a]=ML^{-1}T^{-2}\times L^6=ML^5T^{-2}\).</li></ul>'''),
        ('Uses and limits of dimensional analysis', r'''<p><strong>Uses:</strong> checking equations, converting units between systems, and finding how a quantity depends on others.</p>
<p><strong>Limits:</strong></p>
<ol><li>Pure numbers such as \(\tfrac12\) or \(2\pi\) cannot be found.</li>
<li>Relations with \(\sin\), \(\cos\), \(e^x\) or \(\log\) cannot be derived.</li>
<li>Equations with added terms, like \(s=ut+\tfrac12at^2\), cannot be derived (only checked).</li>
<li>In mechanics only three equations (M, L, T) exist, so at most three unknown powers can be found.</li>
<li>Quantities with the same dimensions (work and torque) cannot be told apart.</li></ol>'''),
    ],
    formulas=[
        dict(title='Constants in van der Waals equation', formula=r'\left(P+\frac{a}{V^2}\right)(V-b)=RT:\quad [a]=ML^5T^{-2},\ [b]=L^3',
             symbols='P is pressure (Pa), V is volume (m³), a and b are van der Waals constants, R is the gas constant, T is temperature (K). Dimensions follow from adding like quantities.'),
    ],
    traps=[r'Same dimensions do not mean the same quantity. Work and torque are both \(ML^2T^{-2}\); torque is written in N m, never in joules.',
           r'Dimensionless is not the same as unitless. An angle is dimensionless but has a unit, the radian. Strain is dimensionless and unitless.'],
    exam=r'''<ul><li>"Which pair has the same dimensions?" (energy density and pressure, Planck constant and angular momentum, work and torque).</li>
<li>"In \(F=a\sqrt x+bt^2\), find the dimensions of a/b."</li>
<li>"Dimensions of \(a\) and \(b\) in van der Waals&#39; equation."</li>
<li>Statement questions on what dimensional analysis can and cannot do.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'In \(x=at+bt^2\), \(x\) is distance and \(t\) is time. Find the dimensions of \(a\), \(b\) and \(a/b\).',
             steps=[r'Each term must be a length. \([at]=L\Rightarrow[a]=LT^{-1}\).',
                    r'\([bt^2]=L\Rightarrow[b]=LT^{-2}\).',
                    r'\([a/b]=\dfrac{LT^{-1}}{LT^{-2}}=T\).'],
             answer=r'\([a]=LT^{-1}\), \([b]=LT^{-2}\), \([a/b]=T\)'),
        dict(tag='Concept', q=r'A wave is \(y=A\sin(\omega t-kx)\). Find the dimensions of \(\omega/k\) and name the quantity.',
             steps=[r'The argument of sine is dimensionless.',
                    r'So \([\omega]=T^{-1}\) and \([k]=L^{-1}\).',
                    r'\([\omega/k]=LT^{-1}\). This is the wave speed.'],
             answer=r'\(LT^{-1}\), the wave speed'),
        dict(tag='Statement', q=r'Statement I: \(s=ut+\tfrac14at^2\) is dimensionally correct. Statement II: It is the correct equation of motion. Judge both.',
             steps=[r'Each term has dimension L, so statement I is true.',
                    r'The correct coefficient is \(\tfrac12\), so statement II is false.',
                    r'Dimensional checks cannot catch a wrong number.'],
             answer=r'I true, II false'),
    ],
    practice=[
        dict(q=r'Which pair of quantities has the same dimensions?',
             options=['Momentum and energy', 'Torque and power', 'Pressure and energy per unit volume', 'Surface tension and force'], answer=2, type='concept',
             explanation=r'Pressure is \(ML^{-1}T^{-2}\). Energy per volume is \(ML^2T^{-2}/L^3=ML^{-1}T^{-2}\). Momentum (\(MLT^{-1}\)) differs from energy. Torque lacks the extra \(T^{-1}\) of power. Surface tension (\(MT^{-2}\)) is force per length.'),
        dict(q=r'In \(F=a\sqrt x+bt^2\), F is force, x is distance and t is time. The dimensions of \(a/b\) are',
             options=[r'\(L^{1/2}T^{-2}\)', r'\(L^{-1/2}T^{2}\)', r'\(ML^{1/2}T^{-2}\)', r'\(L^{-1/2}T^{-2}\)'], answer=1, type='numerical',
             explanation=r'\([a]=MLT^{-2}/L^{1/2}=ML^{1/2}T^{-2}\). \([b]=MLT^{-2}/T^2=MLT^{-4}\). Dividing: \(L^{-1/2}T^{2}\). Option 1 inverts the result. Option 3 is \([a]\) alone, not the ratio.'),
        dict(q=r'Using Stokes&#39; law \(F=6\pi\eta rv\), the dimensions of viscosity \(\eta\) are',
             options=[r'\(MLT^{-1}\)', r'\(ML^{-1}T^{-2}\)', r'\(ML^{-2}T^{-1}\)', r'\(ML^{-1}T^{-1}\)'], answer=3, type='numerical',
             explanation=r'\(\eta=F/(6\pi rv)\). \(MLT^{-2}\div(L\cdot LT^{-1})=ML^{-1}T^{-1}\). \(ML^{-1}T^{-2}\) is pressure. \(MLT^{-1}\) is momentum.'),
        dict(q=r'Assertion: Angle is a dimensionless quantity, yet it has a unit. Reason: A dimensionless quantity can still have a unit.',
             options=AR_OPTS, answer=0, type='ar',
             explanation=r'Angle = arc/radius, a ratio of lengths, so it is dimensionless. Its unit, the radian, expresses that ratio. The reason states the general idea that covers the assertion, so it explains it.'),
    ],
),

'units-analysis': dict(
    level='exam',
    notes=[
        ('The method step by step', r'''<ol><li>List every quantity the result may depend on. Leave out none and add none.</li>
<li>Write \(Q=k\,a^xb^yc^z\) with \(k\) a dimensionless constant.</li>
<li>Write the dimensions of each side and equate the powers of M, L and T.</li>
<li>Solve the three equations for \(x\), \(y\), \(z\).</li>
<li>Get \(k\) from theory or experiment.</li></ol>'''),
        ('Results NEET expects you to derive', r'''<ul><li>Stokes&#39; drag \(F\propto\eta rv\) (viscosity, radius, speed).</li>
<li>Centripetal force \(F\propto mv^2/r\).</li>
<li>Mass on a spring \(T\propto\sqrt{m/k}\).</li>
<li>Orbital period \(T\propto r^{3/2}(GM)^{-1/2}\).</li>
<li>Energy of an oscillator \(E\propto m\omega^2A^2\).</li>
<li>Planck length \(\ell\propto\sqrt{hG/c^3}\).</li></ul>'''),
    ],
    formulas=[
        dict(title='Stokes drag and spring period', formula=r'F=6\pi\eta rv,\qquad T=2\pi\sqrt{\frac{m}{k}}',
             symbols='F drag force (N), η viscosity (Pa s), r sphere radius (m), v speed (m/s); T period (s), m mass (kg), k spring constant (N/m). Dimensions give the powers; 6π and 2π come from theory.'),
        dict(title='Planck length from h, c and G', formula=r'\ell_P=\sqrt{\frac{hG}{c^3}}',
             symbols='h is Planck’s constant (J s), G the gravitational constant (N m² kg⁻²), c the speed of light (m/s). The only combination of these with dimension L.'),
    ],
    traps=[r'With four unknown powers and only M, L, T, the method fails. You need an extra physical argument, or the problem is badly posed.'],
    exam=r'''<ul><li>"The time period of a planet depends on G, M and r. Find the relation."</li>
<li>"Velocity of ripples depends on surface tension, density and wavelength."</li>
<li>"Using h, c and G as base quantities, find the dimension of length / time / mass."</li>
<li>"Which relation cannot be derived by dimensional analysis?"</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'The drag force on a small sphere depends on viscosity \(\eta\), radius \(r\) and speed \(v\). Find the relation.',
             steps=[r'Let \(F=k\eta^ar^bv^c\). Dimensions: \(MLT^{-2}=(ML^{-1}T^{-1})^a L^b(LT^{-1})^c\).',
                    r'M: \(a=1\). T: \(-a-c=-2\Rightarrow c=1\).',
                    r'L: \(-a+b+c=1\Rightarrow b=1\).',
                    r'So \(F=k\eta rv\). Theory gives \(k=6\pi\).'],
             answer=r'\(F\propto\eta rv\)'),
        dict(tag='Numerical', q=r'Find the combination of \(h\), \(c\) and \(G\) that has the dimensions of length.',
             steps=[r'\([h]=ML^2T^{-1}\), \([c]=LT^{-1}\), \([G]=M^{-1}L^3T^{-2}\). Let \(\ell=h^ac^bG^d\).',
                    r'M: \(a-d=0\). L: \(2a+b+3d=1\). T: \(-a-b-2d=0\).',
                    r'With \(d=a\): \(b=-3a\) and \(5a+b=1\Rightarrow2a=1\Rightarrow a=\tfrac12\).',
                    r'So \(a=d=\tfrac12\), \(b=-\tfrac32\).'],
             answer=r'\(\ell\propto\sqrt{hG/c^3}\)'),
        dict(tag='Concept', q=r'Why can dimensional analysis check \(s=ut+\tfrac12at^2\) but not derive it?',
             steps=[r'Checking only needs every term to have dimension L, which they do.',
                    r'Deriving assumes a single product of powers. Here the answer is a sum of two different products.',
                    r'The method also cannot give the factor \(\tfrac12\).'],
             answer=r'The equation is a sum of terms with a numerical coefficient.'),
    ],
    practice=[
        dict(q=r'The period of a planet depends on G, the Sun&#39;s mass M and orbit radius r. Dimensional analysis gives T proportional to',
             options=[r'\(r^{3/2}G^{-1/2}M^{-1/2}\)', r'\(r^{3/2}G^{1/2}M^{-1/2}\)', r'\(r^{2/3}G^{-1/2}M^{-1/2}\)', r'\(r^{-3/2}G^{1/2}M^{1/2}\)'], answer=0, type='numerical',
             explanation=r'Let \(T=G^aM^br^c\). M: \(-a+b=0\). T: \(-2a=1\Rightarrow a=-\tfrac12\), so \(b=-\tfrac12\). L: \(3a+c=0\Rightarrow c=\tfrac32\). This is Kepler&#39;s third law. Option 3 swaps the power of r; option 2 has the wrong sign on G.'),
        dict(q=r'The energy of an oscillator depends on mass m, angular frequency ω and amplitude A. Then E is proportional to',
             options=[r'\(m\omega A\)', r'\(m\omega^2A\)', r'\(m\omega^2A^2\)', r'\(m^2\omega A^2\)'], answer=2, type='numerical',
             explanation=r'M: power of m is 1. T: \(-2=-b\) so ω is squared. L: A must be squared. \(E\propto m\omega^2A^2\). Option 2 has dimensions of force, not energy.'),
        dict(q=r'Which relation can NOT be obtained by dimensional analysis alone?',
             options=[r'\(T\propto\sqrt{\ell/g}\)', r'\(v\propto\sqrt{F/\mu}\)', r'\(y=A\sin\omega t\)', r'\(F\propto mv^2/r\)'], answer=2, type='concept',
             explanation=r'The sine function cannot come out of matching powers of M, L and T. The other three are single products of powers, which the method can find, apart from the numerical constant.'),
        dict(q=r'The speed of ripples on a liquid depends on surface tension S, density ρ and wavelength λ. Then v is proportional to',
             options=[r'\(\sqrt{S\lambda/\rho}\)', r'\(\sqrt{S/(\rho\lambda)}\)', r'\(\sqrt{\rho\lambda/S}\)', r'\(S/(\rho\lambda)\)'], answer=1, type='numerical',
             explanation=r'\([S]=MT^{-2}\), \([\rho]=ML^{-3}\). M: \(a+b=0\). T: \(-2a=-1\Rightarrow a=\tfrac12\), \(b=-\tfrac12\). L: \(-3b+c=1\Rightarrow c=-\tfrac12\). So \(v\propto\sqrt{S/(\rho\lambda)}\). Option 1 has λ in the numerator, giving dimensions \(L^2T^{-1}\). Option 4 has no square root and is \(L^2T^{-2}\).'),
    ],
),

'units-significant': dict(
    level='core',
    notes=[
        ('Counting rules in one place', r'''<ol><li>All non-zero digits are significant.</li>
<li>Zeros between non-zero digits are significant (2.005 has 4).</li>
<li>Leading zeros are never significant (0.0032 has 2).</li>
<li>Trailing zeros after a decimal point are significant (3.200 has 4).</li>
<li>Trailing zeros in a whole number are ambiguous (4700 m). Scientific notation removes the doubt: \(4.7\times10^3\) has 2, \(4.700\times10^3\) has 4.</li>
<li>A change of unit does not change the count: 2.308 cm = 23.08 mm = 0.02308 m, all four figures.</li>
<li>Exact numbers (counts, the 2 in \(2\pi r\), defined conversions) have unlimited significant figures.</li></ol>'''),
        ('Rounding off (NCERT rule)', r'''<ul><li>Dropped digit more than 5: raise the last kept digit (2.746 → 2.75).</li>
<li>Dropped digit less than 5: keep it (2.743 → 2.74).</li>
<li>Dropped digit exactly 5: leave the kept digit unchanged if it is even, raise it if it is odd. So 2.745 → 2.74 and 2.735 → 2.74.</li></ul>
<p>Keep one extra digit in intermediate steps. Round only the final answer.</p>'''),
        ('Combining measurements', r'''<p>Multiplication and division: the answer keeps as many significant figures as the least precise input. Addition and subtraction: the answer keeps as many decimal places as the input with the fewest decimal places.</p>
<p>Example: a box of mass 2.3 kg gets two gold pieces of 20.15 g and 20.17 g. Total = 2.3403 kg, reported as 2.3 kg. The difference between the gold pieces is 0.02 g, reported as 0.02 g.</p>'''),
    ],
    figure=dict(svg=_fig_sigfig(), caption='Leading zeros only locate the decimal point. Zeros between digits and trailing zeros after the decimal point are measured digits.'),
    traps=[r'Converting 2.30 kg to grams as "2300 g" hides the precision. Write \(2.30\times10^3\) g to keep three significant figures.',
           r'For addition, do not count significant figures. 12.11 + 0.3 is limited by decimal places, giving 12.4.'],
    exam=r'''<ul><li>"Number of significant figures in 0.06900 / 6.320 × 10⁴ / 4700."</li>
<li>"Area of a plate of 2.0 cm × 3.15 cm to correct significant figures."</li>
<li>"Round 2.745 / 2.735 to three significant figures."</li>
<li>Mixed operations: sum then product, or a cube&#39;s volume and surface area.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A cube has edge \(1.2\times10^{-2}\) m. Find its volume and total surface area with correct significant figures.',
             steps=[r'Volume \(a^3=(1.2\times10^{-2})^3=1.728\times10^{-6}\) m³.',
                    r'Surface area \(6a^2=6\times1.44\times10^{-4}=8.64\times10^{-4}\) m². The 6 is exact.',
                    r'The edge has 2 significant figures, so round both to 2.'],
             answer=r'\(1.7\times10^{-6}\) m³ and \(8.6\times10^{-4}\) m²'),
        dict(tag='Numerical', q=r'Round 2.745 and 2.735 to three significant figures.',
             steps=[r'In both, the dropped digit is exactly 5.',
                    r'2.745: the kept digit 4 is even, so it stays: 2.74.',
                    r'2.735: the kept digit 3 is odd, so it rises: 2.74.'],
             answer=r'2.74 and 2.74'),
        dict(tag='Numerical', q=r'Evaluate \(\dfrac{4.0\times3.267}{1.20}\) to the correct significant figures.',
             steps=[r'Unrounded: \(13.068/1.20=10.89\).',
                    r'Inputs have 2, 4 and 3 significant figures. The least is 2.',
                    r'Round to 2 significant figures: 11.'],
             answer=r'11'),
    ],
    practice=[
        dict(q=r'The product 6.4 × 3.255, reported to correct significant figures, is',
             options=['20.832', '20.8', '21', '20'], answer=2, type='numerical',
             explanation=r'6.4 has two significant figures, so the product 20.832 is rounded to 21. 20.8 keeps three figures. 20 keeps only one significant figure and rounds the wrong way.'),
        dict(q=r'Which of these numbers has the most significant figures?',
             options=['0.00300', r'\(3.0\times10^{-5}\)', '300.0', '30'], answer=2, type='concept',
             explanation=r'300.0 has 4: the zero after the decimal point is significant, so the two zeros before the point are too. 0.00300 has 3 (leading zeros do not count). \(3.0\times10^{-5}\) has 2. 30 has at most 2.'),
        dict(q=r'Using the NCERT rounding rule, 9.865 rounded to three significant figures is',
             options=['9.87', '9.86', '9.9', '9.865'], answer=1, type='numerical',
             explanation=r'The dropped digit is exactly 5 and the kept digit 6 is even, so it stays: 9.86. 9.87 follows the "always round 5 up" habit, which NCERT does not use. 9.9 has only two figures.'),
        dict(q=r'The result of 15.36 + 4.2 − 0.025 with correct precision is',
             options=['19.535', '19.54', '20', '19.5'], answer=3, type='numerical',
             explanation=r'4.2 has only one decimal place, so the answer keeps one decimal place: 19.535 → 19.5. 19.54 keeps two decimals. 20 rounds too far: the rule for sums is about decimal places, not significant figures.'),
    ],
),

'units-errors': dict(
    level='core',
    notes=[
        ('Kinds of error', r'''<ul><li><strong>Systematic errors</strong> push every reading the same way. They come from the instrument (zero error, faulty calibration), the method (ignoring heat loss) or the observer (always reading from one side, parallax). Repeating does not remove them. They need a correction.</li>
<li><strong>Random errors</strong> scatter readings above and below the true value. Averaging many readings reduces them.</li>
<li><strong>Least count error</strong> comes from the resolution of the instrument. A finer instrument reduces it.</li></ul>'''),
        ('Absolute, mean, relative and percentage error', r'''<ol><li>Mean value: \(\bar a=\dfrac{1}{n}\sum a_i\), taken as the best estimate.</li>
<li>Absolute error of each reading: \(\Delta a_i=|a_i-\bar a|\).</li>
<li>Mean absolute error: \(\overline{\Delta a}=\dfrac1n\sum|\Delta a_i|\).</li>
<li>Relative error: \(\overline{\Delta a}/\bar a\); percentage error: \(\times100\%\).</li>
<li>Report as \(\bar a\pm\overline{\Delta a}\).</li></ol>'''),
        ('Accuracy is not precision', r'''<p>Accuracy is how close the result is to the true value. Precision is how close repeated readings are to each other, and how fine the instrument&#39;s resolution is. A precise instrument with a zero error gives readings that agree with one another but are all wrong.</p>'''),
    ],
    formulas=[
        dict(title='Reporting a measured value', formula=r'a=\bar a\pm\overline{\Delta a},\qquad \text{percentage error}=\frac{\overline{\Delta a}}{\bar a}\times100\%',
             symbols='ā is the mean of the readings, Δā is the mean absolute error, in the unit of a. The percentage error is a pure number.'),
    ],
    figure=dict(svg=_fig_targets(), caption='Accuracy is about the centre; precision is about the spread. A zero error gives the second target: tight but off-centre.'),
    traps=[r'Averaging many readings cannot remove a systematic error. Ten readings from a ruler with a worn end are all short by the same amount.',
           r'Personal error, such as always reading a scale at an angle, is a systematic error, not a random one.'],
    exam=r'''<ul><li>"Find the mean value, mean absolute error and percentage error" from a list of readings.</li>
<li>"Zero error of an instrument is a … error."</li>
<li>"Which can be reduced by taking more readings?" (random error).</li>
<li>Statement questions on accuracy versus precision.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'The period of a pendulum is read as 2.63 s, 2.56 s, 2.42 s, 2.71 s and 2.80 s. Find the mean, the mean absolute error and the percentage error.',
             steps=[r'Mean: \((2.63+2.56+2.42+2.71+2.80)/5=2.624\approx2.62\) s.',
                    r'Absolute errors from 2.624: 0.006, 0.064, 0.204, 0.086, 0.176 s.',
                    r'Mean absolute error: \(0.536/5=0.107\approx0.11\) s.',
                    r'Percentage error: \(0.11/2.62\times100\approx4\%\).'],
             answer=r'\(T=2.62\pm0.11\) s, about 4%'),
        dict(tag='Concept', q=r'The true length of a rod is 10.00 cm. Student A reads 9.62, 9.61, 9.63 cm. Student B reads 9.8, 10.3, 10.1 cm. Compare accuracy and precision.',
             steps=[r'A&#39;s readings agree within 0.01 cm, so A is precise. Their mean (9.62 cm) is 0.38 cm off, so A is not accurate. A systematic error is likely.',
                    r'B&#39;s readings spread over 0.5 cm, so B is not precise. Their mean (10.07 cm) is close to the true value, so B is fairly accurate.'],
             answer=r'A is precise but not accurate; B is accurate but not precise.'),
    ],
    practice=[
        dict(q=r'Readings of a length are 1.20, 1.22, 1.24 and 1.26 cm. The percentage error is about',
             options=['1.6%', '2.4%', '0.8%', '4.9%'], answer=0, type='numerical',
             explanation=r'Mean = 1.23 cm. Deviations: 0.03, 0.01, 0.01, 0.03, mean 0.02 cm. \(0.02/1.23\times100\approx1.6\%\). 2.4% uses the largest deviation (0.03 cm) instead of the mean. 4.9% uses the full range of 0.06 cm. 0.8% halves the correct value.'),
        dict(q=r'An error caused by a vernier that does not read zero when its jaws are closed is a',
             options=['Random error', 'Systematic error', 'Gross error (blunder)', 'Error that averaging removes'], answer=1, type='concept',
             explanation=r'Zero error shifts every reading by the same amount in the same direction, so it is systematic. Random errors scatter both ways and average out; this one does not. It is not a blunder, since it is predictable and correctable.'),
        dict(q=r'Statement I: Random errors can be reduced by taking many readings and averaging. Statement II: An instrument with a smaller least count gives more precise readings.',
             options=ST_OPTS, answer=0, type='statement',
             explanation=r'Both are true. Averaging reduces random scatter. A smaller least count gives finer resolution, which is what precision of an instrument means. Neither statement claims anything about systematic error.'),
        dict(q=r'A stopwatch has least count 0.1 s. The time for 20 oscillations is 20.0 s. The percentage error in the period is',
             options=['0.25%', '5%', '0.05%', '0.5%'], answer=3, type='numerical',
             explanation=r'Fractional error \(=0.1/20.0=0.005\), or 0.5%. Dividing by 20 to get the period divides both the value and the error, so the percentage stays 0.5%. 5% divides the 0.1 s error by the 1 s period without scaling the error down. 0.25% wrongly halves it, and 0.05% misplaces the decimal.'),
    ],
),

'units-propagation': dict(
    level='exam',
    notes=[
        ('Where the rules come from', r'''<p><strong>Sum or difference.</strong> If \(Z=A\pm B\), the worst case is \((A\pm\Delta A)\pm(B\pm\Delta B)\), so \(\Delta Z=\Delta A+\Delta B\). Errors always add.</p>
<p><strong>Product.</strong> If \(Z=AB\), then \((A\pm\Delta A)(B\pm\Delta B)\approx AB\pm(B\Delta A+A\Delta B)\), dropping the tiny \(\Delta A\Delta B\). Dividing by \(Z=AB\): \(\Delta Z/Z=\Delta A/A+\Delta B/B\). Quotients give the same result.</p>
<p><strong>Power.</strong> \(Z=A^n\) is a product of \(n\) copies of \(A\), so \(\Delta Z/Z=n\,\Delta A/A\). This holds for fractional and negative \(n\) using \(|n|\).</p>'''),
        ('Which measurement deserves the most care', r'''<p>The quantity with the largest power dominates. In \(g=4\pi^2\ell/T^2\), the error in T counts twice. In the volume of a sphere, the radius error counts three times. So time the pendulum over many oscillations and measure the radius with the finest instrument.</p>'''),
        ('Differences of nearly equal numbers', r'''<p>Subtraction keeps absolute errors but shrinks the value, so the percentage error can blow up. Temperatures 20.0 ± 0.5 °C and 50.0 ± 0.5 °C differ by 30 ± 1 °C (3.3%). If they were 49.0 and 50.0 °C, the difference 1 ± 1 °C would be 100% uncertain.</p>'''),
    ],
    formulas=[
        dict(title='General power law error', formula=r'Z=\frac{A^pB^q}{C^r}\ \Rightarrow\ \frac{\Delta Z}{Z}=p\frac{\Delta A}{A}+q\frac{\Delta B}{B}+r\frac{\Delta C}{C}',
             symbols='A, B, C are measured quantities with absolute errors ΔA, ΔB, ΔC; p, q, r are the magnitudes of their powers. Worst-case, first-order estimate for small errors.'),
        dict(title='Resistors in parallel', formula=r'\frac{\Delta R}{R^2}=\frac{\Delta R_1}{R_1^2}+\frac{\Delta R_2}{R_2^2}',
             symbols='R is the parallel combination of R₁ and R₂ (Ω); Δ denotes absolute error. Comes from differentiating 1/R = 1/R₁ + 1/R₂.'),
    ],
    traps=[r'In \(Z=A-B\), the error is \(\Delta A+\Delta B\), never \(\Delta A-\Delta B\).',
           r'A power in the denominator still adds its error. In \(\rho=m/V\), the error in V adds to the error in m.'],
    exam=r'''<ul><li>"\(P=a^3b^2/(cd)\). Errors in a, b, c, d are 1%, 2%, 3%, 4%. Percentage error in P?"</li>
<li>"Error in kinetic energy if mass and speed have errors …"</li>
<li>"Two resistors with errors are joined in series / parallel. Find the error."</li>
<li>"Which quantity should be measured most accurately?" (the one with the highest power).</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'Two resistors, \(R_1=100\pm3\ \Omega\) and \(R_2=200\pm4\ \Omega\), are joined (a) in series and (b) in parallel. Find the combined resistance with its error.',
             steps=[r'Series: \(R=300\ \Omega\), \(\Delta R=3+4=7\ \Omega\).',
                    r'Parallel: \(R=\dfrac{100\times200}{300}=66.7\ \Omega\).',
                    r'\(\Delta R=R^2\left(\dfrac{3}{100^2}+\dfrac{4}{200^2}\right)=4444\times(3\times10^{-4}+1\times10^{-4})=1.8\ \Omega\).'],
             answer=r'(a) \(300\pm7\ \Omega\) (b) \(66.7\pm1.8\ \Omega\)'),
        dict(tag='Numerical', q=r'In a pendulum experiment, \(\ell=100.0\pm0.1\) cm and \(T=2.00\pm0.01\) s. Find the percentage error in \(g=4\pi^2\ell/T^2\).',
             steps=[r'\(\Delta\ell/\ell=0.1/100.0=0.1\%\).',
                    r'\(\Delta T/T=0.01/2.00=0.5\%\), counted twice: 1.0%.',
                    r'Total: \(0.1+1.0=1.1\%\).'],
             answer=r'1.1%'),
        dict(tag='Numerical', q=r'Temperatures are \(\theta_1=20.0\pm0.5\)°C and \(\theta_2=50.0\pm0.5\)°C. Find the temperature rise and its percentage error.',
             steps=[r'Rise: \(50.0-20.0=30.0\)°C.',
                    r'Error: \(0.5+0.5=1.0\)°C. Errors add in a difference.',
                    r'Percentage: \(1.0/30.0\times100\approx3.3\%\).'],
             answer=r'\(30\pm1\)°C, about 3.3%'),
    ],
    practice=[
        dict(q=r'Errors of 2% in mass and 3% in speed are made. The maximum error in kinetic energy is',
             options=['5%', '8%', '11%', '6%'], answer=1, type='numerical',
             explanation=r'\(K=\tfrac12mv^2\): \(2\%+2\times3\%=8\%\). 5% ignores the square on v. 11% uses \(3\times3\%\) for the speed, as if v were cubed. The \(\tfrac12\) is exact and adds nothing.'),
        dict(q=r'The radius of a sphere is measured with a 2% error. The error in its volume is',
             options=['2%', '4%', '8%', '6%'], answer=3, type='numerical',
             explanation=r'\(V\propto r^3\), so the error is \(3\times2\%=6\%\). 8% is \(2^3\), cubing the error instead of multiplying by the power. 4% is the error in surface area.'),
        dict(q=r'\(P=\dfrac{a^3b^2}{cd}\). The percentage errors in a, b, c and d are 1%, 2%, 3% and 4%. The percentage error in P is',
             options=['10%', '4%', '14%', '7%'], answer=2, type='numerical',
             explanation=r'\(3(1)+2(2)+1(3)+1(4)=14\%\). 10% adds the errors without their powers. 4% subtracts the denominator errors, but errors in a quotient still add.'),
        dict(q=r'Two lengths are \(L_1=20.0\pm0.2\) cm and \(L_2=10.0\pm0.1\) cm. Their difference is',
             options=[r'\(10.0\pm0.1\) cm', r'\(10.0\pm0.3\) cm', r'\(10.0\pm0.2\) cm', r'\(10.0\pm0.15\) cm'], answer=1, type='numerical',
             explanation=r'In a difference, absolute errors add: \(0.2+0.1=0.3\) cm. \(\pm0.1\) subtracts the errors, which would make subtraction more precise than either reading. \(\pm0.15\) averages them.'),
    ],
),

'units-instruments': dict(
    level='exam',
    notes=[
        ('Why a vernier works', r'''<p>Suppose \(N\) vernier divisions span \((N-1)\) main-scale divisions. Then</p>
\[1\ \text{VSD}=\frac{N-1}{N}\ \text{MSD},\qquad LC=1\ \text{MSD}-1\ \text{VSD}=\frac{1\ \text{MSD}}{N}.\]
<p>With 10 vernier divisions over 9 mm, LC = 0.1 mm = 0.01 cm. Each vernier mark is 0.1 mm shorter than a main mark, so the mark that lines up tells you how many tenths of a millimetre to add.</p>
<p><strong>Reading:</strong> main-scale reading (the last main mark before the vernier zero) + (number of the coinciding vernier mark × LC).</p>'''),
        ('Screw gauge: pitch and least count', r'''<p>One full turn of the thimble moves the spindle by one <strong>pitch</strong>. With \(N\) divisions on the circular scale, LC = pitch/N. A pitch of 0.5 mm and 50 divisions give LC = 0.01 mm.</p>
<p><strong>Reading:</strong> linear-scale reading (last visible mark on the sleeve) + (circular division on the reference line × LC).</p>
<p><strong>Backlash error:</strong> a worn screw can turn a little without moving the spindle. Always turn in one direction while measuring. The ratchet stops you from over-tightening.</p>'''),
    ],
    formulas=[
        dict(title='Instrument readings', formula=r'\text{Vernier: } x=\text{MSR}+n\times LC,\qquad \text{Screw gauge: } x=\text{LSR}+n\times\frac{p}{N}',
             symbols='MSR main-scale reading; LSR linear (sleeve) scale reading; n the coinciding vernier mark or the circular division on the reference line; p pitch; N divisions on the circular scale. All lengths in the same unit. Subtract the zero error afterwards.'),
        dict(title='Vernier least count, general form', formula=r'N\ \text{VSD}=(N-1)\ \text{MSD}\ \Rightarrow\ LC=\frac{1\ \text{MSD}}{N}',
             symbols='N is the number of vernier divisions; MSD and VSD are the sizes of one main-scale and one vernier-scale division. For other designs, use LC = 1 MSD − 1 VSD directly.'),
    ],
    figure=dict(svg=_fig_vernier(), caption='Vernier reading: the vernier zero lies just past 2.3 cm, and the 7th vernier mark coincides with a main mark. With LC = 0.01 cm, the reading is 2.37 cm.'),
    traps=[r'The main-scale reading is the main mark just <em>before</em> the vernier zero, not the main mark that coincides with a vernier mark.',
           r'Least count of a screw gauge uses the pitch, not 1 mm. If the pitch is 0.5 mm and there are 50 divisions, LC = 0.01 mm, not 0.02 mm.'],
    exam=r'''<ul><li>"10 VSD = 9 MSD and 1 MSD = 1 mm. Least count?"</li>
<li>"Pitch 0.5 mm, 50 circular divisions, linear reading … circular reading …. Find the diameter."</li>
<li>Figure-reading questions with a vernier or screw gauge.</li>
<li>"Backlash error is reduced by …"</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A vernier has 20 divisions that equal 19 main-scale divisions, and 1 MSD = 0.5 mm. Find its least count.',
             steps=[r'\(1\ \text{VSD}=\tfrac{19}{20}\times0.5=0.475\) mm.',
                    r'\(LC=0.5-0.475=0.025\) mm.',
                    r'Check with the shortcut: \(LC=\text{MSD}/N=0.5/20=0.025\) mm.'],
             answer=r'0.025 mm'),
        dict(tag='Graph', q=r'Read the vernier in the figure above. The main scale is in cm with mm divisions, and 10 vernier divisions equal 9 mm.',
             steps=[r'LC = 1 mm/10 = 0.1 mm = 0.01 cm.',
                    r'The vernier zero is just past the 2.3 cm mark, so MSR = 2.3 cm.',
                    r'The 7th vernier mark lines up, so add \(7\times0.01=0.07\) cm.'],
             answer=r'2.37 cm'),
        dict(tag='Numerical', q=r'A screw gauge has pitch 1 mm and 100 circular divisions. The sleeve shows 3 mm and division 47 is on the reference line. There is no zero error. Find the reading.',
             steps=[r'LC = 1 mm/100 = 0.01 mm.',
                    r'Reading = \(3+47\times0.01=3.47\) mm.'],
             answer=r'3.47 mm'),
    ],
    practice=[
        dict(q=r'50 vernier divisions equal 49 main-scale divisions of 1 mm each. The least count is',
             options=['0.01 mm', '0.02 mm', '0.049 mm', '0.98 mm'], answer=1, type='numerical',
             explanation=r'\(LC=1\ \text{mm}/50=0.02\) mm. 0.98 mm is the size of one vernier division, not the least count. 0.01 mm would need 100 vernier divisions.'),
        dict(q=r'A screw gauge has pitch 0.5 mm and 50 circular divisions. The sleeve reading is 3.5 mm and division 23 is on the reference line. The reading is',
             options=['3.523 mm', '3.73 mm', '4.65 mm', '3.615 mm'], answer=1, type='numerical',
             explanation=r'LC = 0.5/50 = 0.01 mm. Reading = \(3.5+23\times0.01=3.73\) mm. 3.615 mm uses LC = 0.005 mm. 4.65 mm treats each division as 0.05 mm. 3.523 mm uses LC = 0.001 mm.'),
        dict(q=r'Backlash error in a screw gauge is minimised by',
             options=['Taking the mean of many readings', 'Turning the screw in one direction only', 'Using a vernier instead', 'Subtracting the zero error'], answer=1, type='concept',
             explanation=r'Backlash is play in the worn thread when the turning direction reverses. Approaching the final position from one direction avoids it. Averaging handles random error; zero correction handles zero error, a different fault.'),
        dict(q=r'For a vernier, 1 MSD = 1 mm and 10 VSD = 9 MSD. The main scale reads 4.2 cm and the 6th vernier mark coincides. With no zero error, the length is',
             options=['4.26 cm', '4.206 cm', '4.8 cm', '4.32 cm'], answer=0, type='numerical',
             explanation=r'LC = 0.01 cm, so the reading is \(4.2+6\times0.01=4.26\) cm. 4.206 cm uses LC = 0.001 cm. 4.8 cm treats each vernier mark as 1 mm.'),
    ],
),
}


NEW_SECTIONS = [
dict(chapter='units', after='units-si', id='units-distances',
     title='Measuring large and small distances: parallax',
     intro=r'Very large distances cannot be measured with a tape. Instead, view the object from two points a known distance \(b\) apart. The lines of sight meet at the object at a small angle \(\theta\), the parallax angle. Then the distance is \(D=b/\theta\).',
     reasoning=r'For a small angle, the baseline is almost an arc of a circle of radius \(D\) centred on the object, so \(b\approx D\theta\). The same idea gives the size of a distant object from its angular size: \(d=\alpha D\). Very small lengths, such as molecular sizes, are found from thin films or with electron microscopes.',
     formula=r'D=\frac{b}{\theta},\qquad d=\alpha D',
     symbols='D is the distance to the object (m), b the baseline (m), θ the parallax angle (rad); d is the size of the object (m) and α its angular diameter (rad). Valid when θ and α are small (D ≫ b).',
     trap=r'The angles must be in radians. Convert first: \(1^\circ=\pi/180\) rad, \(1^{\prime}=2.91\times10^{-4}\) rad and \(1^{\prime\prime}=4.85\times10^{-6}\) rad.',
     example=r'The Moon is viewed from two points on opposite sides of the Earth (baseline = Earth&#39;s diameter, \(1.276\times10^{7}\) m). The parallax angle is 1°54&#39;. Find the Moon&#39;s distance.',
     solution=r'\(\theta=1.9^\circ=1.9\times\pi/180=3.32\times10^{-2}\) rad. \(D=b/\theta=1.276\times10^{7}/3.32\times10^{-2}\approx3.85\times10^{8}\) m.',
     question=r'A star shows a parallax angle of 0.5 arc second against a baseline of 1 AU. Its distance is',
     options='0.5 parsec|1 parsec|2 parsec|4 parsec', answer=2,
     explanation=r'By definition 1 AU subtends 1″ at 1 parsec. Distance is inversely proportional to the angle, so half the angle means twice the distance: 2 parsec.',
     deep=dict(
         level='basic',
         notes=[
             ('Parallax and the parsec', r'''<p>Hold a pencil at arm&#39;s length and close each eye in turn. The pencil appears to jump against the background. The jump is parallax, and it is smaller for farther objects. Astronomers use two positions of the Earth, or two observatories, as the two "eyes".</p>
<p>A <strong>parsec</strong> is the distance at which 1 AU subtends 1 arc second: \(D=\dfrac{1.496\times10^{11}}{4.85\times10^{-6}}\approx3.08\times10^{16}\) m. A star with parallax \(p\) arc seconds (baseline 1 AU) is at \(1/p\) parsec.</p>'''),
             ('Echo methods and small lengths', r'''<p><strong>RADAR and SONAR:</strong> a pulse goes to the object and comes back. If the round trip takes \(t\), the distance is \(D=vt/2\). The factor 2 accounts for the return journey.</p>
<p><strong>Size of a molecule (oleic acid film):</strong> a known tiny volume \(V\) of oleic acid spreads on water into a film one molecule thick, of area \(A\). The thickness is \(t=V/A\), about \(10^{-9}\) m.</p>
<p>Lengths in nature span from about \(10^{-15}\) m (a nucleus) to \(10^{26}\) m (the observable universe).</p>'''),
             ('Order of magnitude', r'''<p>Write the number as \(a\times10^{b}\) with \(0.5\lt a\le5\). Then \(b\) is its order of magnitude. If \(a\) is above 5, round up to \(10^{b+1}\). So \(3\times10^8\) m/s has order 8, while the Earth&#39;s mass, \(5.97\times10^{24}\) kg, has order 25.</p>'''),
         ],
         formulas=[
             dict(title='Echo and film thickness', formula=r'D=\frac{vt}{2},\qquad t_{\text{film}}=\frac{V}{A}',
                  symbols='v is the pulse speed (m/s) and t the round-trip time (s); V is the volume of oleic acid in the film (m³) and A the film area (m²).'),
             dict(title='Angle conversions', formula=r'1^\circ=\frac{\pi}{180}\ \text{rad},\quad 1^{\prime\prime}=\frac{\pi}{180\times3600}\ \text{rad}\approx4.85\times10^{-6}\ \text{rad}',
                  symbols='° is degree, ″ is arc second (1/3600 of a degree). Parallax formulas need radians.'),
         ],
         figure=dict(svg=_fig_parallax(), caption='Parallax: from A and B, a baseline b apart, the lines of sight to S meet at the small angle θ. Then D ≈ b/θ.'),
         traps=[r'In echo problems the measured time is for the round trip. Forgetting to halve it doubles the distance.',
                r'Parallax angle and distance are inversely related. A smaller parallax means a farther star.'],
         exam=r'''<ul><li>"The Sun&#39;s angular diameter is 1920″ and its distance … Find its diameter."</li>
<li>"A RADAR / SONAR pulse returns after t seconds. Find the distance."</li>
<li>"1 parsec equals …" and "parallax of 0.5″ means …".</li>
<li>"Order of magnitude of …"</li></ul>''',
         examples=[
             dict(tag='Numerical', q=r'The Sun&#39;s angular diameter is 1920″ and its distance is \(1.496\times10^{11}\) m. Find its diameter.',
                  steps=[r'\(\alpha=1920\times4.85\times10^{-6}=9.31\times10^{-3}\) rad.',
                         r'\(d=\alpha D=9.31\times10^{-3}\times1.496\times10^{11}\).',
                         r'\(d\approx1.39\times10^{9}\) m.'],
                  answer=r'About \(1.39\times10^{9}\) m'),
             dict(tag='Numerical', q=r'A RADAR pulse sent to the Moon returns after 2.56 s. Find the Moon&#39;s distance. Take \(c=3\times10^{8}\) m/s.',
                  steps=[r'The pulse travels to the Moon and back, so \(2D=ct\).',
                         r'\(D=\dfrac{3\times10^{8}\times2.56}{2}=3.84\times10^{8}\) m.'],
                  answer=r'\(3.84\times10^{8}\) m'),
             dict(tag='Numerical', q=r'1 cm³ of oleic acid is dissolved in alcohol to make 20 cm³. Then 1 cm³ of this is diluted to 20 cm³. One drop (1/20 cm³) of the final solution spreads into a film of area 1250 cm². Estimate the molecular size.',
                  steps=[r'Concentration of oleic acid: \(\tfrac1{20}\times\tfrac1{20}=\tfrac1{400}\).',
                         r'Oleic acid in one drop: \(\tfrac1{20}\times\tfrac1{400}=1.25\times10^{-4}\) cm³.',
                         r'Thickness \(=V/A=1.25\times10^{-4}/1250=1\times10^{-7}\) cm \(=1\times10^{-9}\) m.'],
                  answer=r'About \(10^{-9}\) m'),
         ],
         practice=[
             dict(q=r'A SONAR pulse returns from the sea bed after 4 s. Sound travels at 1500 m/s in water. The depth is',
                  options=['6000 m', '3000 m', '1500 m', '375 m'], answer=1, type='numerical',
                  explanation=r'\(D=vt/2=1500\times4/2=3000\) m. 6000 m forgets that the pulse makes a round trip. 1500 m halves twice.'),
             dict(q=r'An object 100 m away subtends an angle of 1°. Its size is about',
                  options=['1.75 m', '100 m', '0.017 m', '5730 m'], answer=0, type='numerical',
                  explanation=r'\(d=\alpha D=(\pi/180)\times100=1.75\) m. 100 m treats 1° as 1 rad. 0.017 m is the angle in radians, without multiplying by the distance. 5730 m multiplies by 57.3 instead of dividing.'),
             dict(q=r'The order of magnitude of \(8.5\times10^{-3}\) is',
                  options=['−3', '−2', '3', '2'], answer=1, type='numerical',
                  explanation=r'8.5 is greater than 5, so the number rounds to \(10^{-2}\), order −2. −3 ignores the rounding step. The positive values ignore the negative exponent.'),
             dict(q=r'Statement I: A star with a larger parallax angle is farther away. Statement II: 1 parsec is about 3.26 light years.',
                  options=ST_OPTS, answer=3, type='statement',
                  explanation=r'Statement I is false: \(D=b/\theta\), so a larger angle means a nearer star. Statement II is true: \(3.08\times10^{16}/9.46\times10^{15}\approx3.26\).'),
         ],
     )),

dict(chapter='units', after='units-dimensions', id='units-conversion',
     title='Converting between unit systems: n₁u₁ = n₂u₂',
     intro=r'A physical quantity does not change when you change units. Only its number changes: \(n_1u_1=n_2u_2\). A bigger unit gives a smaller number.',
     reasoning=r'If the quantity has dimensions \(M^aL^bT^c\), its unit is built from base units as \(u=M^aL^bT^c\). So \(n_2=n_1\left(\frac{M_1}{M_2}\right)^a\left(\frac{L_1}{L_2}\right)^b\left(\frac{T_1}{T_2}\right)^c\). This converts SI to CGS and handles made-up systems with new base units.',
     formula=r'n_2=n_1\left(\frac{M_1}{M_2}\right)^a\left(\frac{L_1}{L_2}\right)^b\left(\frac{T_1}{T_2}\right)^c',
     symbols='n₁, n₂ are the numerical values in systems 1 and 2; M₁, L₁, T₁ and M₂, L₂, T₂ are the base units of mass, length and time in each system, expressed in a common unit; a, b, c are the dimensional exponents of the quantity.',
     trap=r'The ratios are (old unit / new unit). Inverting them is the commonest mistake. Check: a bigger new unit must give a smaller number.',
     example=r'Convert 1 joule into ergs.',
     solution=r'For energy, \(a=1\), \(b=2\), \(c=-2\). \(n_2=1\times\left(\frac{1\ \text{kg}}{1\ \text{g}}\right)\left(\frac{1\ \text{m}}{1\ \text{cm}}\right)^2\left(\frac{1\ \text{s}}{1\ \text{s}}\right)^{-2}=10^3\times10^4=10^7\). So 1 J = \(10^7\) erg.',
     question=r'1 newton expressed in dynes is',
     options='10³|10⁵|10⁷|10⁻⁵', answer=1,
     explanation=r'Force is \(MLT^{-2}\): \(n_2=(10^3)(10^2)(1)^{-2}=10^5\). \(10^7\) is the joule-to-erg factor, which has \(L^2\). \(10^{-5}\) inverts the ratios: a dyne is smaller than a newton, so the number must grow.',
     deep=dict(
         level='exam',
         notes=[
             ('Why the number scales inversely with the unit', r'''<p>A length of 2 m is 200 cm. The centimetre is 100 times smaller, so the number is 100 times larger. In general \(Q=n_1u_1=n_2u_2\), so \(n_2/n_1=u_1/u_2\).</p>
<p>For a quantity of dimensions \(M^aL^bT^c\), \(u_1/u_2=(M_1/M_2)^a(L_1/L_2)^b(T_1/T_2)^c\). Each base unit enters with the power it has in the dimensional formula.</p>'''),
             ('A new system with scaled base units', r'''<p>Suppose the new unit of mass is \(\alpha\) kg, the unit of length \(\beta\) m and the unit of time \(\gamma\) s. Then the new unit of a quantity \(M^aL^bT^c\) is \(\alpha^a\beta^b\gamma^c\) times its SI unit, and</p>
\[n_{\text{new}}=\frac{n_{\text{SI}}}{\alpha^a\beta^b\gamma^c}.\]
<p>Example: if length and time units both double, \(g=9.8\ \text{m/s}^2\) (\(LT^{-2}\)) becomes \(9.8/(2\times2^{-2})=19.6\) new units.</p>'''),
             ('Choosing different base quantities', r'''<p>Some questions make, say, force F, velocity V and time T the base quantities. Then express mass using a known formula: \(F=ma=m\,V/T\), so \([M]=[FV^{-1}T]\). Length is \([VT]\). Any other quantity follows by substitution. If energy E, velocity V and time T are base: \(E=\tfrac12mv^2\) gives \([M]=[EV^{-2}]\).</p>'''),
         ],
         formulas=[
             dict(title='New units built from scaled base units', formula=r'u_{\text{new}}=\alpha^a\beta^b\gamma^c\,u_{\text{SI}},\qquad n_{\text{new}}=\frac{n_{\text{SI}}}{\alpha^a\beta^b\gamma^c}',
                  symbols='α, β, γ are the new units of mass, length and time expressed in kg, m and s; a, b, c are the dimensional exponents of the quantity; n is its numerical value.'),
             dict(title='Useful SI–CGS factors', formula=r'1\ \text{N}=10^5\ \text{dyne},\quad 1\ \text{J}=10^7\ \text{erg},\quad 1\ \text{Pa}=10\ \text{dyne cm}^{-2},\quad 1\ \text{kg m}^{-3}=10^{-3}\ \text{g cm}^{-3}',
                  symbols='dyne and erg are the CGS units of force and energy (g, cm, s). Each follows from n₁u₁ = n₂u₂.'),
         ],
         traps=[r'If both length and time units double, acceleration in new units is <em>larger</em>, not smaller: \(n_2=n_1\times2^{-1}\times2^{2}=2n_1\). Check the sign of each exponent.',
                r'Changing the unit never changes the dimensions of a quantity, only its numerical value.'],
         exam=r'''<ul><li>"Convert G = \(6.67\times10^{-11}\) N m² kg⁻² into CGS units."</li>
<li>"In a new system the unit of mass is α kg, length β m, time γ s. 1 J equals …"</li>
<li>"If force, velocity and time are fundamental quantities, the dimensions of mass are …"</li>
<li>"The value of g is 9.8 m/s². What is it if the units of length and time are doubled?"</li></ul>''',
         examples=[
             dict(tag='Numerical', q=r'Convert \(G=6.67\times10^{-11}\ \text{N m}^2\text{kg}^{-2}\) into CGS units.',
                  steps=[r'\([G]=M^{-1}L^3T^{-2}\).',
                         r'\(n_2=6.67\times10^{-11}\times\left(\frac{1000\ \text{g}}{1\ \text{g}}\right)^{-1}\left(\frac{100\ \text{cm}}{1\ \text{cm}}\right)^{3}\left(\frac{1\ \text{s}}{1\ \text{s}}\right)^{-2}\).',
                         r'\(=6.67\times10^{-11}\times10^{-3}\times10^{6}=6.67\times10^{-8}\).'],
                  answer=r'\(6.67\times10^{-8}\ \text{dyne cm}^2\text{g}^{-2}\)'),
             dict(tag='Numerical', q=r'In a new system, the unit of mass is 10 kg, length 10 m and time 10 s. Express 100 J in the new unit of energy.',
                  steps=[r'Energy is \(ML^2T^{-2}\). New unit = \(10\times10^2\times10^{-2}=10\) J.',
                         r'\(n_{\text{new}}=100/10=10\).'],
                  answer=r'10 new units'),
             dict(tag='Concept', q=r'If energy E, velocity V and time T are taken as base quantities, find the dimensions of mass, length and momentum.',
                  steps=[r'From \(E=\tfrac12mv^2\): \([M]=[EV^{-2}]\).',
                         r'From \(v=\)distance/time: \([L]=[VT]\).',
                         r'Momentum \(=mv\): \([EV^{-2}][V]=[EV^{-1}]\).'],
                  answer=r'\([M]=EV^{-2}\), \([L]=VT\), \([p]=EV^{-1}\)'),
         ],
         practice=[
             dict(q=r'A density of 1 g cm⁻³ is expressed in a system whose unit of mass is 100 g and unit of length is 10 cm. Its new numerical value is',
                  options=['0.1', '10', '100', '1000'], answer=1, type='numerical',
                  explanation=r'Density is \(ML^{-3}\): \(n_2=1\times(1/100)^1\times(1/10)^{-3}=1000/100=10\). Check: the new density unit is 100 g/1000 cm³ = 0.1 g cm⁻³, so 1 g cm⁻³ is 10 units. 0.1 inverts the answer; 1000 ignores the mass change.'),
             dict(q=r'If force F, velocity V and time T are taken as fundamental quantities, the dimensions of mass are',
                  options=[r'\([FVT^{-1}]\)', r'\([FVT]\)', r'\([FV^{-1}T]\)', r'\([F^{-1}VT]\)'], answer=2, type='concept',
                  explanation=r'\(F=ma=m\,V/T\), so \(m=FT/V\), i.e. \([FV^{-1}T]\). \([FVT^{-1}]\) has dimensions of power, not mass. The other two do not reduce to M.'),
             dict(q=r'A pressure of \(10^6\) dyne cm⁻² in SI units is',
                  options=[r'\(10^5\) Pa', r'\(10^7\) Pa', r'\(10^6\) Pa', r'\(10^4\) Pa'], answer=0, type='numerical',
                  explanation=r'1 dyne cm⁻² = \(10^{-5}\) N/\(10^{-4}\) m² = 0.1 Pa, so \(10^6\) dyne cm⁻² = \(10^5\) Pa. \(10^7\) Pa multiplies by 10 instead of dividing.'),
             dict(q=r'The units of length and time are both doubled. The numerical value of an acceleration of 9.8 m/s² becomes',
                  options=['4.9', '9.8', '1.225', '19.6'], answer=3, type='numerical',
                  explanation=r'Acceleration is \(LT^{-2}\): \(n_2=9.8\times(1/2)^1\times(1/2)^{-2}=9.8\times\tfrac12\times4=19.6\). 4.9 only accounts for length. 1.225 uses the wrong sign on the time exponent.'),
         ],
     )),

dict(chapter='units', after='units-instruments', id='units-reading',
     title='Zero error and instrument reading practice',
     intro=r'An instrument has a zero error when it does not read zero with its jaws or studs closed. Find that error first, then correct every reading: true value = observed reading − zero error.',
     reasoning=r'For a vernier: if the vernier zero lies to the right of the main zero, the error is positive, \(+n\times LC\), where \(n\) is the coinciding vernier mark. If it lies to the left, the error is negative, \(-(N-n)\times LC\). A screw gauge works the same way with its circular scale.',
     formula=r'e_{+}=+n\,LC,\qquad e_{-}=-(N-n)\,LC,\qquad x_{\text{true}}=x_{\text{obs}}-e',
     symbols='n is the coinciding vernier mark (or circular division on the reference line) with the jaws closed; N is the total number of vernier or circular divisions; LC is the least count; e is the signed zero error.',
     trap=r'For a negative zero error, the coinciding mark \(n\) is counted from the vernier zero, but the error is \((N-n)\) divisions, not \(n\).',
     example=r'A vernier (LC = 0.01 cm, 10 divisions) has its zero to the left of the main zero when the jaws are closed, with the 6th vernier mark coinciding. A rod reads 2.53 cm. Find its true length.',
     solution=r'Zero error \(e=-(10-6)\times0.01=-0.04\) cm. True length \(=2.53-(-0.04)=2.57\) cm.',
     question=r'A screw gauge (LC = 0.01 mm) reads +0.05 mm with its studs touching. A wire reads 3.47 mm. Its true diameter is',
     options='3.52 mm|3.47 mm|3.42 mm|3.37 mm', answer=2,
     explanation=r'True = observed − zero error = 3.47 − 0.05 = 3.42 mm. A positive zero error means the gauge over-reads, so the correction is negative. 3.52 mm adds the error instead.',
     deep=dict(
         level='exam',
         notes=[
             ('Positive and negative zero error on a vernier', r'''<ul><li><strong>Positive:</strong> jaws closed, vernier zero to the right of the main zero. The instrument already reads a little. If the 4th vernier mark coincides (LC 0.1 mm), \(e=+0.4\) mm.</li>
<li><strong>Negative:</strong> vernier zero to the left of the main zero. If the 6th mark coincides on a 10-division vernier, the vernier zero is \((10-6)\times0.1=0.4\) mm short of zero, so \(e=-0.4\) mm.</li></ul>
<p>Zero <em>correction</em> is minus the zero error. Add the correction, or subtract the error. Both give the same true value.</p>'''),
             ('Zero error on a screw gauge', r'''<p>Close the studs gently with the ratchet. Look at the circular scale.</p>
<ul><li>If its zero has passed the reference line, so that division \(n\) sits on the line, the gauge reads \(+n\times LC\) with nothing between the studs. This is a positive error. On a standard gauge, the circular zero then lies below the reference line.</li>
<li>If its zero has not reached the line, so that division \(n\) near the end of the scale sits on it, the error is \(-(N-n)\times LC\). The circular zero lies above the line.</li></ul>'''),
             ('A full reading routine', r'''<ol><li>Find the least count.</li>
<li>Close the jaws or studs and find the signed zero error.</li>
<li>Take the main or linear scale reading.</li>
<li>Add the vernier or circular division × LC.</li>
<li>Subtract the zero error.</li>
<li>Repeat at different positions and take the mean.</li></ol>'''),
         ],
         formulas=[
             dict(title='Corrected reading', formula=r'x_{\text{true}}=(\text{MSR}+n\times LC)-e_0',
                  symbols='MSR is the main or linear scale reading; n the coinciding vernier mark or circular division; LC the least count; e₀ the signed zero error (positive if the instrument over-reads). All in the same unit.'),
         ],
         figure=dict(svg=_fig_screw(), caption='Screw gauge reading: the thimble edge has passed the 4.5 mm mark and division 28 is on the reference line. With LC = 0.01 mm, the reading is 4.78 mm.'),
         traps=[r'A negative zero error means the instrument under-reads, so the correction is <em>added</em>. 5.12 cm with error −0.03 cm gives 5.15 cm.',
                r'In a screw gauge with pitch 0.5 mm, check whether the half-millimetre mark below the reference line is visible. Missing it puts the answer 0.5 mm too low.'],
         exam=r'''<ul><li>"Jaws closed: vernier zero to the right / left and the nth mark coincides. Find the zero error and the corrected reading."</li>
<li>"Screw gauge reads … when the studs touch. Find the diameter of a wire."</li>
<li>Figure-based reading of a screw gauge or vernier.</li>
<li>"Zero correction for a negative zero error is …"</li></ul>''',
         examples=[
             dict(tag='Numerical', q=r'A vernier (LC = 0.1 mm) has a positive zero error with the 4th mark coinciding. A rod gives MSR = 3.2 cm and the 7th mark coinciding. Find the true length.',
                  steps=[r'Zero error \(e=+4\times0.01=+0.04\) cm.',
                         r'Observed reading \(=3.2+7\times0.01=3.27\) cm.',
                         r'True length \(=3.27-0.04=3.23\) cm.'],
                  answer=r'3.23 cm'),
             dict(tag='Numerical', q=r'A screw gauge has pitch 0.5 mm and 50 divisions. With the studs closed, the circular zero is above the reference line and division 46 is on the line. A wire gives a linear reading of 2.5 mm and circular reading 12. Find the diameter.',
                  steps=[r'LC = 0.5/50 = 0.01 mm.',
                         r'Zero error \(=-(50-46)\times0.01=-0.04\) mm.',
                         r'Observed \(=2.5+12\times0.01=2.62\) mm.',
                         r'True \(=2.62-(-0.04)=2.66\) mm.'],
                  answer=r'2.66 mm'),
             dict(tag='Graph', q=r'Read the screw gauge in the figure. Pitch 0.5 mm, 50 divisions, no zero error.',
                  steps=[r'Whole millimetres visible on the sleeve: 4 mm. The half-millimetre mark after it is also visible, so the linear reading is 4.5 mm.',
                         r'Division 28 is on the reference line: \(28\times0.01=0.28\) mm.',
                         r'Total \(=4.5+0.28=4.78\) mm.'],
                  answer=r'4.78 mm'),
         ],
         practice=[
             dict(q=r'In the screw gauge figure, suppose the gauge also has a zero error of +0.03 mm. The true reading is',
                  options=['4.81 mm', '4.78 mm', '4.75 mm', '4.25 mm'], answer=2, type='graph',
                  explanation=r'Observed 4.78 mm; true \(=4.78-0.03=4.75\) mm. 4.81 mm adds the error. 4.25 mm misses the visible half-millimetre mark and then subtracts.'),
             dict(q=r'A vernier with 10 divisions and LC 0.1 mm has its zero to the left of the main zero when closed, with the 3rd vernier mark coinciding. The zero error is',
                  options=['+0.3 mm', '−0.3 mm', '−0.7 mm', '+0.7 mm'], answer=2, type='numerical',
                  explanation=r'Left of zero means negative. The error is \(-(10-3)\times0.1=-0.7\) mm. −0.3 mm uses \(n\) instead of \(N-n\). The positive options ignore the side on which the zero lies.'),
             dict(q=r'A screw gauge has pitch 1 mm and 100 divisions. With the studs touching it reads +5 divisions. A wire gives 3 mm on the sleeve and 47 on the circular scale. The diameter is',
                  options=['3.52 mm', '3.47 mm', '3.42 mm', '3.05 mm'], answer=2, type='numerical',
                  explanation=r'LC = 0.01 mm, zero error +0.05 mm. Observed 3.47 mm; true 3.42 mm. 3.47 mm ignores the zero error and 3.52 mm adds it.'),
             dict(q=r'Statement I: A negative zero error means the instrument reads less than the true value. Statement II: For a negative zero error, the zero correction is subtracted from the observed reading.',
                  options=ST_OPTS, answer=2, type='statement',
                  explanation=r'Statement I is true: with a negative error the scale starts below zero. Statement II is false: the correction is positive, so it is added (equivalently, the negative error is subtracted).'),
         ],
     )),
]
