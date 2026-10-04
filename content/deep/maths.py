"""Deepening layer: Mathematical Review & Physical World (chapter key 'maths')."""
import math

R = str


# ---------- small SVG helpers (light theme, CSS variables) ----------
def _map(xr, yr, box):
    (x0, x1), (y0, y1) = xr, yr
    left, top, right, bottom = box
    return (lambda x: left + (x - x0) / (x1 - x0) * (right - left),
            lambda y: bottom - (y - y0) / (y1 - y0) * (bottom - top))


def _line(x1, y1, x2, y2, color='ink-2', w=1.5, dash=False):
    d = ';stroke-dasharray:4 3' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" style="stroke:var(--{color});stroke-width:{w}{d}"/>'


def _text(x, y, s, color='ink-2', size=12, anchor='start'):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" style="fill:var(--{color});font-size:{size}px">{s}</text>'


def _curve(f, a, b, X, Y, color='indigo', w=2.4, n=80, dash=False):
    pts = ' '.join(f'{X(a + (b - a) * i / n):.1f},{Y(f(a + (b - a) * i / n)):.1f}' for i in range(n + 1))
    d = ';stroke-dasharray:5 4' if dash else ''
    return f'<polyline points="{pts}" style="fill:none;stroke:var(--{color});stroke-width:{w}{d}"/>'


def _dot(x, y, color='coral', r=4):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" style="fill:var(--{color})"/>'


def _svg(w, h, label, body):
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}">{body}</svg>'


# Figure: tangent slopes on a curve x = 4t - t^2
def _fig_tangents():
    X, Y = _map((0, 4.4), (0, 4.6), (50, 30, 360, 190))
    f = lambda t: 4 * t - t * t
    b = _line(50, 190, 365, 190) + _line(50, 190, 50, 22)
    b += _text(365, 208, 'time t (s)', anchor='end') + _text(56, 18, 'position x (m)')
    b += _curve(f, 0, 4, X, Y)
    for t0, col in [(1, 'green'), (2, 'amber'), (3, 'coral')]:
        s = 4 - 2 * t0
        b += _line(X(t0 - 0.6), Y(f(t0) - 0.6 * s), X(t0 + 0.6), Y(f(t0) + 0.6 * s), col, 2)
        b += _dot(X(t0), Y(f(t0)), col)
    b += _text(X(0.05), Y(3.4), 'slope +2', 'green')
    b += _text(X(2), Y(4) - 12, 'slope 0', 'amber', anchor='middle')
    b += _text(X(3.95), Y(3.4), 'slope −2', 'coral', anchor='end')
    return _svg(380, 220, 'Curve x equals 4t minus t squared with tangent lines of slope plus 2, 0 and minus 2', b)


# Figure: signed area under v-t
def _fig_signed_area():
    X, Y = _map((0, 4.5), (-3.6, 3.6), (50, 20, 360, 200))
    b = (f'<polygon points="{X(0):.1f},{Y(0):.1f} {X(0):.1f},{Y(3):.1f} {X(2):.1f},{Y(0):.1f}" style="fill:var(--green-soft);stroke:none"/>'
         f'<polygon points="{X(2):.1f},{Y(0):.1f} {X(4):.1f},{Y(-3):.1f} {X(4):.1f},{Y(0):.1f}" style="fill:var(--coral-soft);stroke:none"/>')
    b += _line(50, Y(0), 365, Y(0)) + _line(50, 200, 50, 16)
    b += _text(365, Y(0) - 6, 't (s)', anchor='end') + _text(56, 14, 'v (m/s)')
    b += _curve(lambda t: 3 - 1.5 * t, 0, 4, X, Y)
    b += _text(X(0.6), Y(0.8), '+3 m', 'green', 13) + _text(X(3.3), Y(-0.9), '−3 m', 'coral', 13)
    for v in (3, -3):
        b += _text(44, Y(v) + 4, f'{v:+d}'.replace('-', '−'), 'muted', 11, 'end')
    for t in (2, 4):
        b += _text(X(t) + (4 if t == 2 else -4), Y(0) - 6, str(t), 'muted', 11, 'start' if t == 2 else 'end')
    b += _text(205, 214, 'displacement = 3 − 3 = 0 m; distance = 3 + 3 = 6 m', 'ink-2', 12, 'middle')
    return _svg(380, 222, 'Velocity time line from plus 3 to minus 3 metres per second with a positive triangle and a negative triangle of area 3 metres each', b)


# Figure: four standard graph shapes
def _fig_shapes():
    b = ''
    panels = [
        ('y = mx + c (straight line)', lambda x: 0.6 + 0.7 * x, (0, 4), (0, 4)),
        ('y = kx² (parabola)', lambda x: 0.22 * x * x, (0, 4), (0, 4)),
        ('xy = k (rectangular hyperbola)', lambda x: 1.2 / x, (0.3, 4), (0, 4)),
        ('y = y₀e^(−kx) (decay)', lambda x: 3.6 * math.exp(-0.8 * x), (0, 4), (0, 4)),
    ]
    for i, (lab, f, xr, yr) in enumerate(panels):
        ox, oy = 20 + (i % 2) * 180, 20 + (i // 2) * 130
        X, Y = _map((0, 4.2), (0, 4.2), (ox + 10, oy + 8, ox + 160, oy + 98))
        b += _line(ox + 10, oy + 98, ox + 162, oy + 98) + _line(ox + 10, oy + 98, ox + 10, oy + 4)
        b += _curve(f, xr[0], xr[1], X, Y, 'indigo', 2.2)
        b += _text(ox + 86, oy + 116, lab, 'ink-2', 11.5, 'middle')
    return _svg(380, 270, 'Four small graphs: straight line, parabola, rectangular hyperbola and exponential decay', b)


# Figure: maxima and minima of y = x^3 - 3x
def _fig_maxmin():
    X, Y = _map((-2.2, 2.2), (-4.2, 4.2), (40, 20, 340, 220))
    f = lambda x: x ** 3 - 3 * x
    b = _line(40, Y(0), 345, Y(0)) + _line(X(0), 222, X(0), 16)
    b += _text(345, Y(0) - 6, 'x', anchor='end') + _text(X(0) + 6, 16, 'y')
    b += _curve(f, -2.2, 2.2, X, Y)
    b += _line(X(-1.6), Y(2), X(-0.4), Y(2), 'green', 2) + _dot(X(-1), Y(2), 'green')
    b += _line(X(0.4), Y(-2), X(1.6), Y(-2), 'coral', 2) + _dot(X(1), Y(-2), 'coral')
    b += _text(X(0) - 8, Y(2) - 14, 'maximum: dy/dx = 0, d²y/dx² &lt; 0', 'green', 11.5, 'end')
    b += _text(X(0) + 10, Y(-2) + 26, 'minimum: dy/dx = 0, d²y/dx² &gt; 0', 'coral', 11.5)
    return _svg(380, 240, 'Graph of y equals x cubed minus 3x with a local maximum at x equals minus 1 and a local minimum at x equals 1, both with horizontal tangents', b)


# Figure: binomial approximation (1+x)^-2 vs 1-2x
def _fig_binomial():
    X, Y = _map((-0.3, 0.3), (0.3, 2.2), (50, 20, 350, 190))
    b = _line(50, 190, 355, 190) + _line(X(0), 192, X(0), 16)
    b += _text(358, 186, 'x', anchor='end') + _text(X(0) + 6, 14, 'value')
    b += _curve(lambda x: (1 + x) ** -2, -0.3, 0.3, X, Y, 'indigo')
    b += _curve(lambda x: 1 - 2 * x, -0.3, 0.3, X, Y, 'coral', 2, dash=True)
    for xv in (-0.3, -0.1, 0.1, 0.3):
        b += _text(X(xv), 205, f'{xv:+.1f}'.replace('-', '−'), 'muted', 11, 'middle')
    b += _text(X(-0.27), Y(2.05), 'exact (1 + x)⁻²', 'indigo', 12)
    b += _text(X(-0.28), Y(1.1), 'approx. 1 − 2x', 'coral', 12)
    b += _text(X(0.03), Y(1.9), 'close agreement only near x = 0', 'ink-2', 11.5)
    return _svg(380, 216, 'Exact curve of one plus x to the power minus 2 and the straight line 1 minus 2x touching near x equals 0 and separating for larger x', b)


# Figure: exponential decay with half-life marks
def _fig_decay():
    X, Y = _map((0, 4.3), (0, 1.1), (50, 20, 360, 190))
    b = _line(50, 190, 365, 190) + _line(50, 190, 50, 16)
    b += _text(205, 222, 'time (in half-lives)', anchor='middle') + _text(56, 14, 'y / y₀')
    b += _curve(lambda t: 0.5 ** t, 0, 4.2, X, Y)
    for n in range(1, 4):
        v = 0.5 ** n
        b += _line(X(n), 190, X(n), Y(v), 'muted', 1, True) + _line(50, Y(v), X(n), Y(v), 'muted', 1, True)
        b += _dot(X(n), Y(v), 'coral') + _text(X(n), 204, str(n), 'muted', 11, 'middle')
        b += _text(44, Y(v) + 4, ['1/2', '1/4', '1/8'][n - 1], 'muted', 11, 'end')
    b += _text(44, Y(1) + 4, '1', 'muted', 11, 'end')
    b += _text(X(1.2), Y(0.75), 'each half-life halves what is left', 'indigo', 12)
    return _svg(380, 230, 'Exponential decay curve falling to one half, one quarter and one eighth after one, two and three half-lives', b)


AR_OPTS = ['Both A and R are true, and R correctly explains A',
           'Both A and R are true, but R does not explain A',
           'A is true but R is false',
           'A is false but R is true']
ST_OPTS = ['Both statements are true',
           'Both statements are false',
           'Statement I is true, Statement II is false',
           'Statement I is false, Statement II is true']


DEEP = {
'maths-models': dict(
    level='basic',
    notes=[
        ('The four fundamental forces', r'''<p>Every force you meet in mechanics comes from one of four fundamental interactions. NCERT compares their strengths relative to the strong force.</p>
<div class="table-wrap"><table><thead><tr><th>Force</th><th>Relative strength</th><th>Range</th><th>Acts between</th></tr></thead><tbody>
<tr><td>Strong nuclear</td><td>1</td><td>Short, about \(10^{-15}\) m (nuclear size)</td><td>Nucleons and heavier elementary particles</td></tr>
<tr><td>Electromagnetic</td><td>\(10^{-2}\)</td><td>Infinite</td><td>Charged particles</td></tr>
<tr><td>Weak nuclear</td><td>\(10^{-13}\)</td><td>Very short, about \(10^{-16}\) m</td><td>Some elementary particles, for example electron and neutrino (beta decay)</td></tr>
<tr><td>Gravitational</td><td>\(10^{-39}\)</td><td>Infinite</td><td>All objects with mass</td></tr>
</tbody></table></div>
<p>Contact forces such as friction, normal reaction, tension and the spring force are all electromagnetic. They come from the electric forces between the atoms of the surfaces in contact. Gravity is the weakest force, yet it rules the motion of planets because large bodies are electrically neutral overall and gravity is always attractive.</p>'''),
        ('Conservation laws and symmetry', r'''<p>Physics rests on a few conservation laws: energy, linear momentum, angular momentum and electric charge. Each one links to a symmetry of nature.</p>
<ul><li>Laws are the same at every place (homogeneity of space) → linear momentum is conserved.</li>
<li>Laws are the same in every direction (isotropy of space) → angular momentum is conserved.</li>
<li>Laws are the same at every time (homogeneity of time) → energy is conserved.</li></ul>
<p>A conservation law tells you what stays fixed. It does not tell you how fast a process happens.</p>'''),
        ('Checking a model before trusting it', r'''<p>After any calculation, run three quick checks.</p>
<ol><li><strong>Units:</strong> both sides must have the same dimensions.</li>
<li><strong>Limiting cases:</strong> set one input to zero or to a very large value. The result must match a case you already know.</li>
<li><strong>Size:</strong> the magnitude must be sensible. A walking speed of 300 m/s signals an error.</li></ol>
<p>A model is good when the effects it ignores are small compared with the effect being asked about.</p>'''),
    ],
    traps=[r'Friction, tension and normal reaction are <strong>electromagnetic</strong> in origin, not "mechanical" or gravitational. Gravity only supplies the weight.',
           r'Weak nuclear force is far stronger than gravity (\(10^{-13}\) against \(10^{-39}\)). Its range is tiny, so it does not act over everyday distances.'],
    exam=r'''<ul><li>"Arrange the fundamental forces in increasing order of strength." Answer: gravitational &lt; weak &lt; electromagnetic &lt; strong.</li>
<li>"Which force is responsible for friction / tension / normal reaction?" Answer: electromagnetic.</li>
<li>"Which force has the shortest range?" Answer: weak nuclear.</li>
<li>Statement-type questions linking conservation laws with symmetries.</li>
<li>"Can this body be treated as a particle?" Compare its size with the distance or scale of the motion.</li></ul>''',
    examples=[
        dict(tag='Concept', q=r'An Atwood machine with masses \(m_1\gt m_2\) has acceleration \(a=\dfrac{(m_1-m_2)g}{m_1+m_2}\). Check this result using two limiting cases.',
             steps=[r'Let \(m_2=0\). Then \(a=m_1g/m_1=g\). With nothing on the other side, \(m_1\) falls freely. This matches.',
                    r'Let \(m_1=m_2\). Then \(a=0\). Equal masses balance. This matches.',
                    r'Let \(m_1\gg m_2\). Then \(a\to g\), never more than \(g\). A pulley system cannot make a mass fall faster than free fall. This matches.'],
             answer=r'The formula passes every limiting check, so it is likely correct.'),
        dict(tag='Concept', q=r'A rope pulls a box across the floor. Name the fundamental force behind (a) the tension in the rope, (b) the friction on the box and (c) the weight of the box.',
             steps=[r'Tension is the pull between neighbouring atoms of the stretched rope. Atomic bonds are electric, so tension is electromagnetic.',
                    r'Friction comes from the interaction of atoms at the two surfaces. It is also electromagnetic.',
                    r'Weight is the pull of the Earth on the mass of the box. It is gravitational.'],
             answer=r'(a) electromagnetic (b) electromagnetic (c) gravitational'),
        dict(tag='Assertion–Reason', q=r'Assertion: The Earth can be treated as a particle when finding its orbit around the Sun. Reason: The Earth&#39;s radius is very small compared with its distance from the Sun.',
             steps=[r'Earth&#39;s radius is about \(6.4\times10^{6}\) m. The Earth–Sun distance is about \(1.5\times10^{11}\) m.',
                    r'The ratio is about \(4\times10^{-5}\), so the size has almost no effect on the orbit. The assertion is true.',
                    r'The reason is true and is exactly why the particle model works.'],
             answer=r'Both A and R are true, and R correctly explains A.'),
    ],
    practice=[
        dict(q=r'The correct order of the fundamental forces in increasing strength is',
             options=['Weak, gravitational, electromagnetic, strong', 'Gravitational, weak, electromagnetic, strong',
                      'Gravitational, electromagnetic, weak, strong', 'Strong, electromagnetic, weak, gravitational'],
             answer=1, type='concept',
             explanation=r'Relative strengths are \(10^{-39}\) (gravity), \(10^{-13}\) (weak), \(10^{-2}\) (electromagnetic) and 1 (strong). Option 1 puts gravity above weak. Option 3 places weak above electromagnetic. Option 4 is the decreasing order.'),
        dict(q=r'The normal reaction exerted by a table on a book is fundamentally',
             options=['Gravitational', 'Weak nuclear', 'Strong nuclear', 'Electromagnetic'],
             answer=3, type='concept',
             explanation=r'The normal force comes from electric repulsion between the atoms of the book and the table when they are pressed together. It is not gravitational: gravity is the weight it balances. Nuclear forces act only inside nuclei.'),
        dict(q=r'Statement I: Conservation of linear momentum is linked to the fact that the laws of physics are the same at every place. Statement II: The weak nuclear force is weaker than the gravitational force.',
             options=ST_OPTS, answer=2, type='statement',
             explanation=r'Statement I is true: homogeneity of space gives momentum conservation. Statement II is false: the weak force (\(10^{-13}\)) is about \(10^{26}\) times stronger than gravity (\(10^{-39}\)). It only seems weak because its range is tiny.'),
        dict(q=r'Assertion: A spinning cricket ball must be treated as an extended body to explain its swing. Reason: A body can be treated as a particle only when its size and rotation do not affect the question being asked.',
             options=AR_OPTS, answer=0, type='ar',
             explanation=r'Swing and spin depend on how air flows around the ball&#39;s surface and on its rotation, so a point model cannot explain them. The reason states the general rule for using a particle model, and it explains the assertion. Option 2 would need a reason unrelated to the assertion.'),
    ],
),

'maths-ratios': dict(
    level='core',
    notes=[
        ('Small changes: the percentage rule', r'''<p>If \(Q\propto x^a y^b\) and each input changes by a <em>small</em> percentage, then</p>
\[\%\ \text{change in } Q \approx a\,(\%\ \text{change in } x) + b\,(\%\ \text{change in } y).\]
<p>This comes from the binomial approximation \((1+\varepsilon)^a\approx1+a\varepsilon\). It works well below about 5%. For large changes, use the exact factor. For example, a 10% rise in radius raises area by exactly \(1.1^2-1=21\%\), close to the approximate 20%. A 50% rise gives exactly 125%, far from the approximate 100%.</p>'''),
        ('Read what is held constant', r'''<p>The same two quantities can scale differently depending on what is fixed. Kinetic energy and momentum are linked by \(K=\dfrac{p^2}{2m}\).</p>
<ul><li>Same momentum: \(K\propto \dfrac1m\). The lighter body has more kinetic energy.</li>
<li>Same kinetic energy: \(p=\sqrt{2mK}\propto\sqrt m\). The heavier body has more momentum.</li>
<li>Same mass: \(K\propto p^2\). If \(p\) doubles, \(K\) becomes four times.</li></ul>
<p>Before taking a ratio, write the formula in terms of the quantities that change, with the fixed ones gathered into the constant.</p>'''),
        ('Graph shapes reveal the power', r'''<ul><li>\(y\propto x\): straight line through the origin.</li>
<li>\(y\propto x^2\): parabola. Plot \(y\) against \(x^2\) to get a straight line.</li>
<li>\(y\propto 1/x\): rectangular hyperbola. Plot \(y\) against \(1/x\) to get a straight line.</li>
<li>\(y=Cx^n\): plot \(\log y\) against \(\log x\). The line has slope \(n\) and intercept \(\log C\).</li></ul>'''),
    ],
    formulas=[
        dict(title='Small percentage changes', formula=r'\frac{\Delta Q}{Q}\times100\approx a\left(\frac{\Delta x}{x}\times100\right)+b\left(\frac{\Delta y}{y}\times100\right)',
             symbols='Q = Cxᵃyᵇ is the dependent quantity; Δx/x and Δy/y are small fractional changes (below about 5%); a and b are the powers with their signs. For large changes use the exact factor (1 + Δx/x)ᵃ.'),
        dict(title='Kinetic energy and momentum', formula=r'K=\frac{p^2}{2m},\qquad p=\sqrt{2mK}',
             symbols='K is kinetic energy (J), p is momentum (kg m/s), m is mass (kg). Valid for any non-relativistic moving body.'),
    ],
    traps=[r'Percentage changes multiply, they do not add. If \(x\) rises 20% and \(y\) rises 20% in \(Q=xy\), the exact change is \(1.2\times1.2=1.44\), a 44% rise, not 40%.',
           r'When comparing kinetic energy and momentum of two bodies, check whether the question fixes \(p\), \(K\) or \(m\). The answer reverses between "same momentum" and "same energy".'],
    exam=r'''<ul><li>"If the momentum increases by 50%, the kinetic energy increases by …" (exact factor needed).</li>
<li>"Two bodies of masses in the ratio 1 : 4 have equal kinetic energies. Ratio of their momenta?"</li>
<li>"A quantity varies as \(x^3/y^2\). Errors / changes of 1% and 2% are made …" (small-change rule).</li>
<li>Graph-match questions: which plot gives a straight line for a given law.</li></ul>''',
    examples=[
        dict(tag='Ratio', q=r'Two bodies of masses in the ratio 1 : 4 have equal kinetic energies. Find the ratio of their momenta.',
             steps=[r'At fixed \(K\), \(p=\sqrt{2mK}\propto\sqrt m\).',
                    r'\(\dfrac{p_1}{p_2}=\sqrt{\dfrac{m_1}{m_2}}=\sqrt{\dfrac14}=\dfrac12\).',
                    r'The heavier body has more momentum even though both have the same energy.'],
             answer=r'1 : 2'),
        dict(tag='Numerical', q=r'The kinetic energy of a body increases by 44%. By what percentage does its momentum increase?',
             steps=[r'Mass is unchanged, so \(p\propto\sqrt K\).',
                    r'\(K_2=1.44K_1\Rightarrow p_2=\sqrt{1.44}\,p_1=1.2\,p_1\).',
                    r'The momentum rises by 20%. The small-change rule (half of 44% = 22%) is not accurate for such a large change.'],
             answer=r'20%'),
        dict(tag='Graph', q=r'For planets, \(T^2\propto r^3\). A student plots \(\log T\) against \(\log r\). What are the shape and slope of the graph?',
             steps=[r'Write \(T=Cr^{3/2}\).',
                    r'Take logs: \(\log T=\tfrac32\log r+\log C\).',
                    r'This is \(y=mx+c\) with \(y=\log T\) and \(x=\log r\).'],
             answer=r'A straight line of slope 3/2 with intercept \(\log C\).'),
    ],
    practice=[
        dict(q=r'The momentum of a body increases by 50%. Its kinetic energy increases by',
             options=['50%', '100%', '125%', '225%'], answer=2, type='numerical',
             explanation=r'At fixed mass \(K\propto p^2\), so \(K_2/K_1=1.5^2=2.25\), an increase of 125%. 100% is the small-change estimate (2 × 50%), which fails for large changes. 225% confuses the new value with the increase.'),
        dict(q=r'A quantity \(Q=x^3/y^2\). If \(x\) increases by 2% and \(y\) decreases by 1%, \(Q\) changes by approximately',
             options=['4% increase', '3% increase', '8% decrease', '8% increase'], answer=3, type='numerical',
             explanation=r'Small-change rule: \(3(+2\%)+(-2)(-1\%)=6\%+2\%=8\%\), an increase. A fall in \(y\) raises \(Q\) because \(y\) is in the denominator. 4% comes from subtracting the \(y\) term with the wrong sign, and 3% ignores the powers (2% + 1%).'),
        dict(q=r'For a law \(y=kx^2\), which plot gives a straight line through the origin?',
             options=[r'\(y\) against \(x\)', r'\(y\) against \(x^2\)', r'\(y\) against \(1/x\)', r'\(\log y\) against \(x\)'],
             answer=1, type='graph',
             explanation=r'With \(X=x^2\), the law becomes \(y=kX\), a line through the origin with slope \(k\). \(y\) against \(x\) is a parabola. \(\log y\) against \(x\) is a curve; only \(\log y\) against \(\log x\) would also be straight.'),
        dict(q=r'Statement I: For two bodies with equal momenta, the lighter body has the larger kinetic energy. Statement II: For two bodies with equal kinetic energies, the heavier body has the larger momentum.',
             options=ST_OPTS, answer=0, type='statement',
             explanation=r'Equal \(p\): \(K=p^2/2m\propto1/m\), so the lighter body has more energy. Equal \(K\): \(p=\sqrt{2mK}\propto\sqrt m\), so the heavier body has more momentum. Both are true. Students who mix the two conditions pick option 3 or 4.'),
    ],
),

'maths-trig': dict(
    level='basic',
    notes=[
        ('Values and identities you must know', r'''<div class="table-wrap"><table><thead><tr><th>θ</th><th>0°</th><th>30°</th><th>37°</th><th>45°</th><th>53°</th><th>60°</th><th>90°</th></tr></thead><tbody>
<tr><td>sin θ</td><td>0</td><td>1/2</td><td>3/5</td><td>1/√2</td><td>4/5</td><td>√3/2</td><td>1</td></tr>
<tr><td>cos θ</td><td>1</td><td>√3/2</td><td>4/5</td><td>1/√2</td><td>3/5</td><td>1/2</td><td>0</td></tr>
<tr><td>tan θ</td><td>0</td><td>1/√3</td><td>3/4</td><td>1</td><td>4/3</td><td>√3</td><td>not defined</td></tr></tbody></table></div>
<p>The 37° and 53° values come from the 3–4–5 triangle and are approximations that coaching tests use freely. Key identities:</p>
<ul><li>\(\sin^2\theta+\cos^2\theta=1\)</li>
<li>\(\sin2\theta=2\sin\theta\cos\theta\) (used in projectile range)</li>
<li>\(\cos2\theta=1-2\sin^2\theta=2\cos^2\theta-1\)</li>
<li>\(\sin(90^\circ-\theta)=\cos\theta\), \(\sin(180^\circ-\theta)=\sin\theta\), \(\cos(180^\circ-\theta)=-\cos\theta\)</li></ul>
<p>Signs by quadrant: all positive in the first, only sine in the second, only tangent in the third, only cosine in the fourth.</p>'''),
        ('Radians and small angles', r'''<p>An angle in radians is arc length divided by radius: \(\theta=s/r\). A full turn is \(2\pi\) rad, so \(1\ \text{rad}\approx57.3^\circ\).</p>
<p>For a small angle the arc and the chord are nearly equal, so \(\sin\theta\approx\tan\theta\approx\theta\). The cosine is flat at zero, so \(\cos\theta\approx1-\theta^2/2\). At 10° (0.1745 rad), \(\sin\theta=0.1736\): the error is only 0.5%. These approximations drive the simple pendulum, parallax and the angular size of distant objects.</p>'''),
    ],
    formulas=[
        dict(title='Double angle and compound angle', formula=r'\sin2\theta=2\sin\theta\cos\theta,\quad \sin(A\pm B)=\sin A\cos B\pm\cos A\sin B',
             symbols='θ, A and B are angles in degrees or radians; the identities hold for all angles.'),
        dict(title='Arc length and small angles', formula=r's=r\theta,\qquad \sin\theta\approx\tan\theta\approx\theta,\quad \cos\theta\approx1-\frac{\theta^2}{2}',
             symbols='s is arc length and r is radius in the same unit (m); θ is in radians. The approximations need |θ| ≪ 1 rad (below about 0.2 rad for 1% accuracy).'),
    ],
    traps=[r'\(\tan37^\circ=0.754\), not exactly 3/4. Use 3/5 and 4/5 only when the question says so or the options are clearly rounded.',
           r'\(\cos(180^\circ-\theta)=-\cos\theta\). A force at 120° to the x-axis has a <em>negative</em> x-component.'],
    exam=r'''<ul><li>Direct value questions: \(\sin37^\circ\), \(\cos120^\circ\), \(\sin2\theta\) given \(\tan\theta\).</li>
<li>Components of a force or velocity at an angle above 90°.</li>
<li>Small-angle estimates: rise of a pendulum bob, angular size, \(\sin\theta\approx\theta\).</li>
<li>Match-the-column on standard values.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'An incline has \(\tan\theta=3/4\). Find \(\sin2\theta\) and \(\cos2\theta\).',
             steps=[r'From the 3–4–5 triangle, \(\sin\theta=3/5\) and \(\cos\theta=4/5\).',
                    r'\(\sin2\theta=2\times\tfrac35\times\tfrac45=\tfrac{24}{25}\).',
                    r'\(\cos2\theta=\cos^2\theta-\sin^2\theta=\tfrac{16}{25}-\tfrac{9}{25}=\tfrac{7}{25}\).'],
             answer=r'\(\sin2\theta=24/25\), \(\cos2\theta=7/25\)'),
        dict(tag='Numerical', q=r'A 10 N force acts at 120° to the positive x-axis. Find its components.',
             steps=[r'\(F_x=10\cos120^\circ=10\times(-\tfrac12)=-5\) N. The cosine is negative in the second quadrant.',
                    r'\(F_y=10\sin120^\circ=10\times\tfrac{\sqrt3}{2}\approx8.66\) N.',
                    r'Check: \(\sqrt{5^2+8.66^2}=10\) N.'],
             answer=r'\(F_x=-5\) N, \(F_y\approx8.66\) N'),
        dict(tag='Numerical', q=r'A 1.0 m pendulum swings to 0.1 rad from the vertical. By how much does the bob rise?',
             steps=[r'The rise is \(h=\ell(1-\cos\theta)\).',
                    r'With \(\cos\theta\approx1-\theta^2/2\), \(h\approx\ell\theta^2/2=1.0\times0.01/2=0.005\) m.',
                    r'The exact value is 0.004996 m, so the approximation is excellent.'],
             answer=r'About 5 mm'),
    ],
    practice=[
        dict(q=r'If \(\sin\theta=0.6\) with \(\theta\) acute, then \(\cos2\theta\) equals',
             options=['0.28', '0.64', '0.36', '0.96'], answer=0, type='numerical',
             explanation=r'\(\cos2\theta=1-2\sin^2\theta=1-0.72=0.28\). 0.64 is \(\cos^2\theta\) and 0.36 is \(\sin^2\theta\). 0.96 is \(\sin2\theta=2(0.6)(0.8)\), not the cosine.'),
        dict(q=r'Using a small-angle approximation, a pendulum of length 2 m displaced by 0.05 rad rises by about',
             options=['0.5 mm', '2.5 mm', '5 mm', '50 mm'], answer=1, type='numerical',
             explanation=r'\(h\approx\ell\theta^2/2=2\times0.0025/2=0.0025\) m = 2.5 mm. 5 mm forgets the factor 1/2. 50 mm would follow from \(h\approx\ell\theta/2\), which uses the wrong power of \(\theta\).'),
        dict(q=r'Statement I: \(\sin\theta\approx\theta\) can be used with \(\theta\) in degrees if the angle is small. Statement II: One radian is about 57.3°.',
             options=ST_OPTS, answer=3, type='statement',
             explanation=r'Statement I is false: the approximation needs radians. For 2°, \(\sin2^\circ=0.0349\), not 2. Statement II is true: \(180/\pi\approx57.3\).'),
        dict(q=r'Match: (a) \(\sin37^\circ\) (b) \(\cos37^\circ\) (c) \(\tan53^\circ\) (d) \(\sin150^\circ\) with (i) 4/5 (ii) 3/5 (iii) 1/2 (iv) 4/3.',
             options=['a-i, b-ii, c-iv, d-iii', 'a-ii, b-i, c-iii, d-iv', 'a-ii, b-i, c-iv, d-iii', 'a-ii, b-iv, c-i, d-iii'],
             answer=2, type='match',
             explanation=r'From the 3–4–5 triangle, \(\sin37^\circ=3/5\), \(\cos37^\circ=4/5\) and \(\tan53^\circ=4/3\). Also \(\sin150^\circ=\sin30^\circ=1/2\). Option 1 swaps sine and cosine of 37°. Option 2 assigns 1/2 to \(\tan53^\circ\).'),
    ],
),

'maths-graphs': dict(
    level='core',
    notes=[
        ('Standard shapes and the laws behind them', r'''<ul><li><strong>Straight line</strong> \(y=mx+c\): uniform motion (x–t), \(v=u+at\) (v–t).</li>
<li><strong>Parabola</strong> \(y=kx^2\): \(s=\tfrac12at^2\) from rest, kinetic energy against speed.</li>
<li><strong>Rectangular hyperbola</strong> \(xy=k\): Boyle&#39;s law (P–V at fixed T), \(\lambda\) against \(f\) at fixed wave speed.</li>
<li><strong>Exponential decay</strong> \(y=y_0e^{-kx}\): radioactive decay, motion with drag proportional to speed.</li></ul>
<p>Recognise the shape first, then read slope, intercept or area.</p>'''),
        ('Slope, intercept and area', r'''<ol><li><strong>Slope</strong> = \(\Delta y/\Delta x\) with units of \(y\) per unit of \(x\). On x–t it is velocity; on v–t it is acceleration; on F–x (spring) it is the spring constant.</li>
<li><strong>Intercept</strong> is the value of \(y\) when \(x=0\). On v–t it is the initial velocity.</li>
<li><strong>Area</strong> has units of \(y\times x\). Area under v–t is displacement; under F–x it is work.</li></ol>
<p>Slope equals \(\tan\theta\) of the drawn angle only when both axes use the same scale. If two lines on the <em>same</em> graph make angles 30° and 60° with the x-axis, their slopes are in the ratio \(\tan30^\circ:\tan60^\circ=1:3\).</p>'''),
        ('Linearising a law to find a constant', r'''<p>Experiments are analysed with straight lines. For the pendulum \(T=2\pi\sqrt{\ell/g}\), squaring gives \(T^2=\dfrac{4\pi^2}{g}\ell\). A plot of \(T^2\) against \(\ell\) is a straight line through the origin with slope \(4\pi^2/g\). Then \(g=4\pi^2/\text{slope}\).</p>'''),
    ],
    formulas=[
        dict(title='Line through two points and intercept form', formula=r'm=\frac{y_2-y_1}{x_2-x_1},\qquad \frac{x}{a}+\frac{y}{b}=1',
             symbols='(x₁, y₁) and (x₂, y₂) are two points on the line; m is the slope (units of y per unit of x); a and b are the x- and y-intercepts in the units of x and y.'),
        dict(title='Linearised pendulum law', formula=r'T^2=\frac{4\pi^2}{g}\,\ell\quad\Rightarrow\quad g=\frac{4\pi^2}{\text{slope of }T^2\text{ vs }\ell}',
             symbols='T is period (s), ℓ is length (m), g is gravitational acceleration (m/s²). Holds for small swings of a simple pendulum.'),
    ],
    figure=dict(svg=_fig_shapes(), caption='The four shapes that appear most in NEET graph questions. Identify the shape, then translate it into a law.'),
    traps=[r'A straight line that does not pass through the origin is <em>not</em> a direct proportion. \(y=mx+c\) with \(c\ne0\) is linear, but doubling \(x\) does not double \(y\).'],
    exam=r'''<ul><li>"Which graph represents Boyle&#39;s law / uniform acceleration from rest?" (shape recognition).</li>
<li>"Two lines make angles 30° and 60° with the time axis. Ratio of velocities?"</li>
<li>"A plot of \(T^2\) against \(\ell\) has slope … Find \(g\)."</li>
<li>"log y against log x is a straight line of slope 2 …" (find the law).</li></ul>''',
    examples=[
        dict(tag='Graph', q=r'In a pendulum experiment, the line of \(T^2\) against \(\ell\) passes through (0.5 m, 2.0 s²) and (1.0 m, 4.0 s²). Find \(g\).',
             steps=[r'Slope = \(\dfrac{4.0-2.0}{1.0-0.5}=4.0\ \text{s}^2/\text{m}\).',
                    r'Slope \(=4\pi^2/g\), so \(g=4\pi^2/4.0=\pi^2\).',
                    r'\(\pi^2\approx9.87\ \text{m/s}^2\).'],
             answer=r'\(g\approx9.87\ \text{m/s}^2\)'),
        dict(tag='Graph', q=r'Two straight x–t lines on the same axes make angles of 30° and 60° with the time axis. Find the ratio of the velocities.',
             steps=[r'On one graph with fixed scales, velocity = slope = \(\tan\theta\).',
                    r'\(v_1:v_2=\tan30^\circ:\tan60^\circ=\tfrac1{\sqrt3}:\sqrt3\).',
                    r'Multiply both by \(\sqrt3\): the ratio is 1 : 3.'],
             answer=r'1 : 3'),
        dict(tag='Numerical', q=r'A line has slope −2 and y-intercept 4. Where does it cut the x-axis?',
             steps=[r'Equation: \(y=-2x+4\).',
                    r'At the x-axis, \(y=0\): \(0=-2x+4\Rightarrow x=2\).'],
             answer=r'At \(x=2\)'),
    ],
    practice=[
        dict(q=r'At constant temperature, the P–V graph of a fixed mass of ideal gas is',
             options=['A straight line through the origin', 'A parabola', 'A rectangular hyperbola', 'A circle'],
             answer=2, type='graph',
             explanation=r'Boyle&#39;s law gives \(PV=\text{constant}\), the equation of a rectangular hyperbola. A line through the origin would mean \(P\propto V\). A parabola would need a squared dependence.'),
        dict(q=r'Two x–t lines on the same graph make angles 30° and 45° with the time axis. The ratio of their velocities is',
             options=[r'\(1:\sqrt3\)', r'\(\sqrt3:1\)', '2 : 3', '1 : 2'], answer=0, type='graph',
             explanation=r'\(\tan30^\circ:\tan45^\circ=\tfrac1{\sqrt3}:1=1:\sqrt3\). \(\sqrt3:1\) inverts the ratio. 2 : 3 compares the angles themselves, but velocity follows \(\tan\theta\), not \(\theta\).'),
        dict(q=r'A graph of \(\log y\) against \(\log x\) is a straight line of slope 2 and intercept \(\log5\). The relation is',
             options=[r'\(y=2x^5\)', r'\(y=5x+2\)', r'\(y=5x^2\)', r'\(y=x^2+5\)'], answer=2, type='graph',
             explanation=r'\(\log y=2\log x+\log5\) means \(y=5x^2\). The slope gives the power and the intercept gives the coefficient. \(y=2x^5\) swaps them. \(y=x^2+5\) would not give a straight log–log line.'),
        dict(q=r'The line \(y=3-2x\) has',
             options=['slope 3, y-intercept −2', 'slope 2, y-intercept 3', 'slope −2, x-intercept 3', 'slope −2, y-intercept 3'],
             answer=3, type='concept',
             explanation=r'Compare with \(y=mx+c\): \(m=-2\), \(c=3\). The x-intercept is 1.5, not 3. Options 1 and 2 swap the slope and intercept or drop the minus sign.'),
    ],
),

'maths-calculus': dict(
    level='core',
    notes=[
        ('Derivatives you must know', r'''<div class="table-wrap"><table><thead><tr><th>Function</th><th>Derivative</th><th>Function</th><th>Derivative</th></tr></thead><tbody>
<tr><td>\(x^n\)</td><td>\(nx^{n-1}\)</td><td>\(\sin x\)</td><td>\(\cos x\)</td></tr>
<tr><td>constant</td><td>0</td><td>\(\cos x\)</td><td>\(-\sin x\)</td></tr>
<tr><td>\(e^x\)</td><td>\(e^x\)</td><td>\(\ln x\)</td><td>\(1/x\)</td></tr></tbody></table></div>
<ul><li><strong>Product rule:</strong> \(\dfrac{d}{dx}(uv)=u\dfrac{dv}{dx}+v\dfrac{du}{dx}\).</li>
<li><strong>Chain rule:</strong> \(\dfrac{d}{dt}f(g(t))=f'(g)\,\dfrac{dg}{dt}\). So \(\dfrac{d}{dt}\sin(\omega t)=\omega\cos(\omega t)\).</li></ul>'''),
        ('Every rate in physics is a derivative', r'''<ul><li>\(v=dx/dt\), \(a=dv/dt=d^2x/dt^2\)</li>
<li>Force \(F=dp/dt\); power \(P=dW/dt\); current \(I=dq/dt\)</li>
<li>Conservative force \(F=-dU/dx\): force points toward lower potential energy.</li></ul>
<p>On a graph, the derivative is the slope of the tangent. A positive slope means the quantity is increasing; zero slope means a turning point; negative slope means decreasing.</p>'''),
        ('Second derivative and curvature', r'''<p>On an x–t curve, the second derivative is the acceleration. A curve bending upward (concave up, like a cup) has \(a\gt0\). A curve bending downward (like a cap) has \(a\lt0\). A straight x–t line has \(a=0\).</p>'''),
    ],
    formulas=[
        dict(title='Chain rule and product rule', formula=r'\frac{d}{dt}\sin(\omega t)=\omega\cos(\omega t),\quad \frac{d}{dx}(uv)=u\frac{dv}{dx}+v\frac{du}{dx}',
             symbols='ω is a constant (rad/s), t is time (s), u and v are differentiable functions of x.'),
        dict(title='Force from potential energy', formula=r'F=-\frac{dU}{dx}',
             symbols='U is potential energy (J) as a function of position x (m); F is the conservative force (N) along x. The minus sign makes F point toward decreasing U.'),
    ],
    figure=dict(svg=_fig_tangents(), caption='The slope of the tangent on an x–t curve is the instantaneous velocity. At the top the tangent is flat, so the body is momentarily at rest.'),
    traps=[r'The derivative of \(\sin(2x)\) is \(2\cos(2x)\), not \(\cos(2x)\). Forgetting the chain-rule factor is the most common calculus slip.',
           r'Velocity is zero where the x–t tangent is flat. That does not make the acceleration zero there.'],
    exam=r'''<ul><li>"Position is \(x=at^3+bt^2+c\). Find velocity / acceleration at time t."</li>
<li>"When does the particle come to rest?" (set \(dx/dt=0\)).</li>
<li>"\(U=\dots\). Find the force at x = …" (\(F=-dU/dx\)).</li>
<li>"Charge \(q=\dots\). Find current at t = …".</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A particle moves as \(x=A\sin(\omega t)\). Find its velocity and acceleration, and show \(a=-\omega^2x\).',
             steps=[r'Chain rule: \(v=\dfrac{dx}{dt}=A\omega\cos(\omega t)\).',
                    r'Again: \(a=\dfrac{dv}{dt}=-A\omega^2\sin(\omega t)\).',
                    r'Since \(x=A\sin(\omega t)\), this is \(a=-\omega^2x\), the defining property of SHM.'],
             answer=r'\(v=A\omega\cos\omega t\), \(a=-\omega^2x\)'),
        dict(tag='Numerical', q=r'The potential energy of a particle is \(U=3x^2-2x\) J, with \(x\) in metres. Find the force at \(x=1\) m.',
             steps=[r'\(\dfrac{dU}{dx}=6x-2\).',
                    r'\(F=-\dfrac{dU}{dx}=-(6x-2)\).',
                    r'At \(x=1\): \(F=-(6-2)=-4\) N, directed toward \(-x\).'],
             answer=r'\(-4\) N'),
        dict(tag='Graph', q=r'On an x–t curve, the tangent at point P is horizontal and the curve is shaped like a cap (bending down). Describe the motion at P.',
             steps=[r'A horizontal tangent means \(dx/dt=0\): the body is momentarily at rest.',
                    r'Cap shape means \(d^2x/dt^2\lt0\): acceleration is negative.',
                    r'The body was moving forward, stops at P, and starts moving backward. P is the farthest forward point.'],
             answer=r'Momentarily at rest with negative acceleration, turning back.'),
    ],
    practice=[
        dict(q=r'For \(x=t^3-6t^2+9t\) (SI units), the particle is at rest at',
             options=['t = 0 only', 't = 1 s and t = 3 s', 't = 2 s only', 't = 3 s only'], answer=1, type='numerical',
             explanation=r'\(v=3t^2-12t+9=3(t-1)(t-3)\), which is zero at 1 s and 3 s. t = 2 s is where acceleration \(6t-12\) is zero. At t = 0 the velocity is 9 m/s, not zero.'),
        dict(q=r'The charge through a wire is \(q=2t^2+3t\) C. The current at t = 2 s is',
             options=['11 A', '14 A', '8 A', '7 A'], answer=0, type='numerical',
             explanation=r'\(I=dq/dt=4t+3=11\) A at 2 s. 14 A is the charge itself at 2 s. 8 A forgets the derivative of the \(3t\) term.'),
        dict(q=r'\(\dfrac{d}{dx}\left(\sin2x\right)\) equals',
             options=[r'\(\cos2x\)', r'\(-2\cos2x\)', r'\(2\sin x\cos x\)', r'\(2\cos2x\)'], answer=3, type='concept',
             explanation=r'The chain rule multiplies by the derivative of the inside, 2. \(\cos2x\) misses this factor. \(2\sin x\cos x\) is \(\sin2x\) itself, not its derivative. The derivative of sine has no minus sign.'),
        dict(q=r'An x–t graph is curved and bends upward like a cup at every point. The acceleration is',
             options=['Zero', 'Positive', 'Negative', 'Changing sign'], answer=1, type='graph',
             explanation=r'Concave-up means the slope (velocity) increases with time, so \(a=d^2x/dt^2\gt0\). The sign of acceleration depends on curvature, not on whether x is positive. A straight line would give zero.'),
    ],
),

'maths-integrals': dict(
    level='core',
    notes=[
        ('Standard integrals and the constant', r'''<ul><li>\(\int x^n\,dx=\dfrac{x^{n+1}}{n+1}+C\) for \(n\ne-1\)</li>
<li>\(\int\dfrac{dx}{x}=\ln x+C\)</li>
<li>\(\int\sin x\,dx=-\cos x+C\), \(\int\cos x\,dx=\sin x+C\), \(\int e^x\,dx=e^x+C\)</li></ul>
<p>The constant \(C\) is fixed by an initial condition. If \(a=6t\), then \(v=3t^2+C\). If \(v=2\) m/s at \(t=0\), then \(C=2\). A definite integral between limits does not need \(C\), because it cancels.</p>'''),
        ('What area means on each graph', r'''<div class="table-wrap"><table><thead><tr><th>Graph</th><th>Area under it</th></tr></thead><tbody>
<tr><td>v–t</td><td>Displacement</td></tr><tr><td>a–t</td><td>Change in velocity</td></tr>
<tr><td>F–t</td><td>Impulse = change in momentum</td></tr><tr><td>F–x</td><td>Work done</td></tr>
<tr><td>P–V</td><td>Work done by a gas</td></tr><tr><td>I–t</td><td>Charge</td></tr></tbody></table></div>
<p>Area below the horizontal axis counts as negative. For total distance, add the magnitudes of all pieces.</p>'''),
        ('Average value of a varying quantity', r'''<p>The time-average of a quantity is its integral divided by the interval: \(\langle f\rangle=\dfrac1T\int_0^T f\,dt\). Average velocity is total displacement over time for this reason. Over a full cycle, \(\langle\sin\rangle=0\) and \(\langle\sin^2\rangle=\tfrac12\).</p>'''),
    ],
    formulas=[
        dict(title='Common integrals', formula=r'\int\frac{dx}{x}=\ln x+C,\quad \int\sin x\,dx=-\cos x+C,\quad \int\cos x\,dx=\sin x+C',
             symbols='x is the variable of integration (x > 0 for ln x); C is a constant fixed by an initial condition.'),
        dict(title='Average value', formula=r'\langle f\rangle=\frac{1}{t_2-t_1}\int_{t_1}^{t_2}f(t)\,dt',
             symbols='f(t) is any quantity varying with time; t₁ and t₂ are the limits (s). Average velocity is the case f = v.'),
    ],
    figure=dict(svg=_fig_signed_area(), caption='Area above the time axis is positive displacement; area below is negative. Displacement adds them with signs; distance adds their sizes.'),
    traps=[r'Integration gives a change, not a value. To get position, add the initial position to the displacement found from the integral.',
           r'For the area under an x–t graph there is no standard meaning. Only areas under rate graphs (v–t, a–t, F–t, F–x) are useful.'],
    exam=r'''<ul><li>"Acceleration \(a=kt\). Starting from rest, find velocity / position at time t."</li>
<li>"Area under the F–t graph gives …" (impulse).</li>
<li>"From the v–t graph find displacement and distance in the first 4 s."</li>
<li>Direct evaluation: \(\int_1^2 3x^2dx\), \(\int_0^\pi\sin x\,dx\).</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A particle has \(a=6t\) m/s². At \(t=0\), \(v=2\) m/s and \(x=0\). Find \(v\) and \(x\) at \(t=2\) s.',
             steps=[r'\(v=\int6t\,dt=3t^2+C_1\). At \(t=0\), \(v=2\), so \(C_1=2\): \(v=3t^2+2\).',
                    r'\(x=\int(3t^2+2)\,dt=t^3+2t+C_2\). At \(t=0\), \(x=0\), so \(C_2=0\).',
                    r'At \(t=2\): \(v=14\) m/s and \(x=8+4=12\) m.'],
             answer=r'\(v=14\) m/s, \(x=12\) m'),
        dict(tag='Graph', q=r'A force on a 0.5 kg ball rises linearly from 0 to 10 N and falls back to 0 over 0.2 s (a triangle on the F–t graph). The ball starts at rest. Find its final speed.',
             steps=[r'Impulse = area of the triangle = \(\tfrac12\times0.2\times10=1.0\) N s.',
                    r'Impulse = change in momentum: \(0.5\,v-0=1.0\).',
                    r'\(v=2.0\) m/s.'],
             answer=r'2 m/s'),
        dict(tag='Numerical', q=r'Evaluate \(\displaystyle\int_0^{\pi}\sin x\,dx\).',
             steps=[r'\(\int\sin x\,dx=-\cos x\).',
                    r'Between the limits: \(-\cos\pi-(-\cos0)=1+1=2\).'],
             answer=r'2'),
    ],
    practice=[
        dict(q=r'\(\displaystyle\int_1^2 3x^2\,dx\) equals',
             options=['8', '3', '7', '12'], answer=2, type='numerical',
             explanation=r'\(\int3x^2dx=x^3\). Between the limits: \(8-1=7\). 8 ignores the lower limit. 12 just puts x = 2 into \(3x^2\); integration is not substitution into the integrand.'),
        dict(q=r'An a–t graph is a rectangle of height 2 m/s² from t = 0 to t = 3 s. The initial velocity is 4 m/s. The velocity at 3 s is',
             options=['6 m/s', '10 m/s', '2 m/s', '12 m/s'], answer=1, type='graph',
             explanation=r'Area = \(2\times3=6\) m/s is the change in velocity, so \(v=4+6=10\) m/s. 6 m/s is only the change. 12 m/s multiplies instead of adding.'),
        dict(q=r'A particle has \(v=3t^2-2t\) m/s. Its displacement from \(t=0\) to \(t=2\) s is',
             options=['4 m', '8 m', '10 m', '6 m'], answer=0, type='numerical',
             explanation=r'\(\Delta x=\int_0^2(3t^2-2t)\,dt=[t^3-t^2]_0^2=8-4=4\) m. 8 m drops the \(-2t\) term. 10 m is \(v\times t\) at t = 2 s, which assumes constant velocity.'),
        dict(q=r'The area under a force–time graph gives',
             options=['Work done', 'Power', 'Kinetic energy', 'Impulse'], answer=3, type='concept',
             explanation=r'\(\int F\,dt=\Delta p\), the impulse. Work is the area under a force–<em>position</em> graph. Power and kinetic energy are not areas under F–t.'),
    ],
),
'maths-logs': dict(
    level='core',
    notes=[
        ('Log rules and base conversion', r"""<ul><li>\(\log(ab)=\log a+\log b\), \(\log(a/b)=\log a-\log b\), \(\log a^n=n\log a\)</li>
<li>\(\log1=0\) in every base; \(\ln e=1\); \(\log_{10}10=1\)</li>
<li>\(\ln x=2.303\log_{10}x\)</li>
<li>Useful values: \(\log_{10}2=0.3010\), \(\log_{10}3=0.4771\), \(\ln2=0.693\)</li></ul>
<p>Write a number in scientific notation before taking its log: \(\log_{10}(2\times10^{3})=0.301+3=3.301\).</p>"""),
        ('Exponential decay and growth', r"""<p>In \(y=y_0e^{-\lambda t}\) the fractional drop in each equal interval is the same. Two time scales matter:</p>
<ul><li>Time constant \(\tau=1/\lambda\): \(y\) falls to \(1/e\approx0.37\) of its start.</li>
<li>Half-life \(t_{1/2}=\ln2/\lambda\approx0.693/\lambda\): \(y\) halves.</li></ul>
<p>After \(n\) half-lives the fraction left is \((1/2)^n\). Taking logs gives \(\ln y=\ln y_0-\lambda t\), so a graph of \(\ln y\) against \(t\) is a straight line with slope \(-\lambda\).</p>"""),
        ('Why the exponent must be dimensionless', r"""<p>\(e^{x}=1+x+x^2/2+\cdots\). Adding 1 to \(x\) and \(x^2\) makes sense only if \(x\) has no dimensions. So in \(e^{-\lambda t}\), \([\lambda]=T^{-1}\). The same rule fixes the dimensions of constants inside \(\sin\), \(\cos\) and \(\log\).</p>"""),
    ],
    formulas=[
        dict(title='Half-life and time constant', formula=r'y=y_0e^{-\lambda t},\quad t_{1/2}=\frac{\ln2}{\lambda}\approx\frac{0.693}{\lambda},\quad \frac{y}{y_0}=\left(\frac12\right)^{t/t_{1/2}}',
             symbols='y₀ is the starting value; λ is the decay constant (s⁻¹); t is time (s); t½ is the half-life (s). Assumes a constant λ.'),
        dict(title='Natural and common logs', formula=r'\ln x=2.303\log_{10}x',
             symbols='x is a positive dimensionless number; ln is base e, log₁₀ is base 10.'),
    ],
    figure=dict(svg=_fig_decay(), caption='Exponential decay never reaches zero. It halves in every half-life: 1/2, 1/4, 1/8 …'),
    traps=[r'After two half-lives, one quarter remains, not zero. "Two halves make a whole" does not apply to decay.',
           r'\(\ln\) and \(\log_{10}\) differ by the factor 2.303. Check which one the formula uses before substituting.'],
    exam=r"""<ul><li>"What fraction remains after 3 half-lives?" or "time to fall to 1/16".</li>
<li>"The graph of ln y against t is a straight line of slope … Find the half-life."</li>
<li>"Dimensions of λ in \(e^{-\lambda t}\)" (dimensions chapter link).</li>
<li>Direct evaluation of logs using \(\log2=0.301\).</li></ul>""",
    examples=[
        dict(tag='Numerical', q=r'A quantity decays exponentially with a half-life of 5 s. What fraction remains after 15 s, and when does it fall to 1/16?',
             steps=[r'15 s is 3 half-lives, so the fraction is \((1/2)^3=1/8\).',
                    r'\(1/16=(1/2)^4\), which needs 4 half-lives.',
                    r'Time = \(4\times5=20\) s.'],
             answer=r'1/8 after 15 s; 1/16 after 20 s'),
        dict(tag='Graph', q=r'A plot of \(\ln y\) against \(t\) is a straight line with slope \(-0.2\ \text{s}^{-1}\). Find the half-life.',
             steps=[r'\(\ln y=\ln y_0-\lambda t\), so the slope is \(-\lambda\) and \(\lambda=0.2\ \text{s}^{-1}\).',
                    r'\(t_{1/2}=0.693/0.2\approx3.47\) s.'],
             answer=r'About 3.5 s'),
        dict(tag='Numerical', q=r'Find \(\log_{10}2000\) and \(\ln1000\).',
             steps=[r'\(\log_{10}(2\times10^3)=0.301+3=3.301\).',
                    r'\(\ln1000=2.303\times\log_{10}1000=2.303\times3\approx6.91\).'],
             answer=r'3.301 and about 6.91'),
    ],
    practice=[
        dict(q=r'For \(y=y_0e^{-\lambda t}\) with \(\lambda=0.1\ \text{s}^{-1}\), the time for \(y\) to fall to \(y_0/e\) is',
             options=['0.1 s', '6.93 s', '10 s', '1 s'], answer=2, type='numerical',
             explanation=r'\(y=y_0/e\) when \(\lambda t=1\), so \(t=1/\lambda=10\) s. 6.93 s is the half-life (\(0.693/\lambda\)), a different time. 0.1 s confuses \(\lambda\) with \(1/\lambda\).'),
        dict(q=r'Given \(\log_{10}2=0.301\), the value of \(\log_{10}0.002\) is',
             options=['−3.301', '−2.699', '−0.301', '2.699'], answer=1, type='numerical',
             explanation=r'\(0.002=2\times10^{-3}\), so the log is \(0.301-3=-2.699\). −3.301 adds the 0.301 with the wrong sign. A number below 1 always has a negative log, so 2.699 is impossible.'),
        dict(q=r'For a quantity decaying exponentially with time, which plot is a straight line?',
             options=[r'\(y\) against \(t\)', r'\(y\) against \(1/t\)', r'\(\ln y\) against \(\ln t\)', r'\(\ln y\) against \(t\)'], answer=3, type='graph',
             explanation=r'\(\ln y=\ln y_0-\lambda t\) is linear in \(t\), with slope \(-\lambda\). \(y\) against \(t\) is the decay curve itself. A log–log straight line belongs to a power law, not an exponential.'),
        dict(q=r'In \(x=x_0e^{-kt}\), the dimensions of \(k\) are',
             options=[r'\(T\)', r'\(T^{-1}\)', r'\(LT^{-1}\)', 'Dimensionless'], answer=1, type='concept',
             explanation=r'The exponent \(kt\) must be dimensionless, so \([k]=T^{-1}\). \(k\) itself is not dimensionless; only the product \(kt\) is. \(LT^{-1}\) would make \(kt\) a length.'),
    ],
),
}


NEW_SECTIONS = [
dict(chapter='maths', after='maths-trig', id='maths-binomial',
     title='Binomial approximation and small changes',
     intro=r'When a number is close to 1, its powers are easy to estimate. For a small dimensionless \(x\), \((1+x)^n\approx1+nx\). This works for any power \(n\): positive, negative or fractional.',
     reasoning=r'Physics uses this whenever one quantity is much smaller than another, such as a height compared with Earth&#39;s radius or a small stretch compared with a length. First write the expression in the form \((1+\text{small})^n\), then apply the rule.',
     formula=r'(1+x)^n\approx1+nx\qquad(|x|\ll1)',
     symbols='x is a small dimensionless number (often h/R, Δℓ/ℓ or v/c); n is any real exponent. The first neglected term is n(n − 1)x²/2, so the error is tiny when |x| is below about 0.05.',
     trap=r'You cannot apply the rule to \((R+h)^{-2}\) directly. Factor out \(R\) first: \((R+h)^{-2}=R^{-2}(1+h/R)^{-2}\).',
     example=r'Find \(g\) at a height of 32 km above Earth. Take Earth&#39;s radius as 6400 km.',
     solution=r'\(g_h=g(1+h/R)^{-2}\approx g(1-2h/R)\). Here \(h/R=32/6400=0.005\), so \(g_h\approx g(1-0.01)=0.99g\). The exact value is \(0.9901g\).',
     question=r'Using the binomial approximation, \(\sqrt{1.02}\) is about',
     options='1.01|1.02|1.04|1.002', answer=0,
     explanation=r'\(\sqrt{1.02}=(1+0.02)^{1/2}\approx1+\tfrac12(0.02)=1.01\). 1.02 forgets the power 1/2; 1.04 squares instead of square-rooting.',
     deep=dict(
         level='exam',
         notes=[
             ('Why (1 + x)ⁿ ≈ 1 + nx works', r'''<p>The binomial series is</p>
\[(1+x)^n=1+nx+\frac{n(n-1)}{2!}x^2+\frac{n(n-1)(n-2)}{3!}x^3+\cdots\]
<p>When \(|x|\ll1\), each term is far smaller than the one before. Keeping only the first two gives \(1+nx\). For \(n=\tfrac12\) and \(x=0.02\), the dropped \(x^2\) term is \(-\tfrac18(0.02)^2=-0.00005\), negligible next to 0.01.</p>
<p>Calculus gives the same result. Near \(x=0\), any smooth \(f(x)\approx f(0)+f'(0)\,x\). With \(f=(1+x)^n\), \(f(0)=1\) and \(f'(0)=n\).</p>'''),
             ('Forms used in physics', r'''<ul><li>\(\dfrac{1}{1+x}\approx1-x\), \(\dfrac{1}{1-x}\approx1+x\)</li>
<li>\(\sqrt{1+x}\approx1+\dfrac x2\), \(\dfrac1{\sqrt{1-x}}\approx1+\dfrac x2\)</li>
<li>\((1+x)^m(1+y)^n\approx1+mx+ny\) when both are small</li>
<li>\(e^x\approx1+x\), \(\ln(1+x)\approx x\)</li></ul>
<p>Uses: \(g\) at small height \(g(1-2h/R)\); a 2% longer pendulum has a period about 1% longer; percentage errors in \(x^ay^b\); small changes in volume with temperature.</p>'''),
             ('When the rule fails', r'''<p>The rule is a linear fit near \(x=0\). As \(x\) grows, the curve and the line separate. For \(x=0.2\), \((1.2)^2=1.44\) while \(1+2(0.2)=1.40\). For \(x=0.5\), \((1.5)^{-2}=0.444\) while \(1-2(0.5)=0\), which is useless. Use the exact form when \(x\) is not small.</p>'''),
         ],
         formulas=[
             dict(title='Two small factors together', formula=r'(1+x)^m(1+y)^n\approx1+mx+ny',
                  symbols='x and y are small dimensionless numbers; m and n are real powers. The neglected terms are of order x², y² and xy.'),
             dict(title='g at small height', formula=r'g_h=\frac{g}{(1+h/R)^2}\approx g\left(1-\frac{2h}{R}\right)',
                  symbols='g is surface value (m/s²), h is height above the surface (m), R is Earth’s radius (m). Valid for h ≪ R.'),
         ],
         figure=dict(svg=_fig_binomial(), caption=r'The straight line 1 − 2x touches the curve (1 + x)⁻² at x = 0. They agree closely only for small x.'),
         traps=[r'The rule needs \(|x|\ll1\). Using it for \(h=R/2\) gives \(g(1-1)=0\), which is absurd. The true value is \(4g/9\).',
                r'Keep the sign of \(n\). For \((1+x)^{-1/2}\), the answer is \(1-x/2\), not \(1+x/2\).'],
         exam=r'''<ul><li>"Find \(g\) at a height \(h\ll R\)" or "At what height does \(g\) fall by 1%?"</li>
<li>"Decrease in \(g\) at height \(h\) equals the decrease at depth \(d\). Relation between \(d\) and \(h\)?"</li>
<li>"Length of a pendulum increases by 2%. Percentage change in period?"</li>
<li>Pure estimates: \(\sqrt{1.02}\), \((0.998)^{-3}\), \(1/\sqrt{0.98}\).</li></ul>''',
         examples=[
             dict(tag='Numerical', q=r'The length of a simple pendulum increases by 2%. By what percentage does its period change?',
                  steps=[r'\(T\propto\ell^{1/2}\), so \(T_2/T_1=(1.02)^{1/2}\).',
                         r'\((1+0.02)^{1/2}\approx1+\tfrac12(0.02)=1.01\).',
                         r'The period increases by about 1%.'],
                  answer=r'About 1% increase'),
             dict(tag='Ratio', q=r'The decrease in \(g\) at a small height \(h\) equals the decrease at depth \(d\). Find \(d\) in terms of \(h\). (At depth \(d\), \(g_d=g(1-d/R)\) exactly.)',
                  steps=[r'At height: \(g_h\approx g(1-2h/R)\), so the decrease is \(2gh/R\).',
                         r'At depth: the decrease is \(gd/R\).',
                         r'Equate: \(gd/R=2gh/R\Rightarrow d=2h\).'],
                  answer=r'\(d=2h\)'),
             dict(tag='Numerical', q=r'Estimate \(\dfrac{1}{\sqrt{0.98}}\).',
                  steps=[r'Write it as \((1-0.02)^{-1/2}\).',
                         r'\(\approx1+\left(-\tfrac12\right)(-0.02)=1+0.01=1.01\).',
                         r'The exact value is 1.0102.'],
                  answer=r'About 1.01'),
         ],
         practice=[
             dict(q=r'Using the binomial approximation, \((0.998)^{-3}\) is about',
                  options=['0.994', '1.002', '1.006', '1.003'], answer=2, type='numerical',
                  explanation=r'\((1-0.002)^{-3}\approx1+(-3)(-0.002)=1.006\). 0.994 gets one sign wrong. 1.002 forgets the power 3.'),
             dict(q=r'A frequency varies as \(1/\sqrt\ell\). If \(\ell\) increases by 4%, the frequency',
                  options=['increases by 2%', 'decreases by 2%', 'decreases by 4%', 'decreases by 8%'], answer=1, type='numerical',
                  explanation=r'\((1.04)^{-1/2}\approx1-\tfrac12(0.04)=0.98\), a 2% decrease. The power \(-\tfrac12\) halves the change and flips its sign. 4% ignores the square root; "increases" ignores the inverse dependence.'),
             dict(q=r'Statement I: \((1+x)^n\approx1+nx\) is valid only when \(n\) is a positive integer. Statement II: The approximation requires \(|x|\) to be much smaller than 1.',
                  options=ST_OPTS, answer=3, type='statement',
                  explanation=r'Statement I is false: the rule works for negative and fractional \(n\), which is how it is used for \(1/r^2\) and square roots. Statement II is true: the dropped terms are of order \(x^2\).'),
             dict(q=r'A body weighs 72 N on Earth&#39;s surface. Using the binomial approximation, its weight at a height \(R/100\) (R = Earth&#39;s radius) is about',
                  options=['70.6 N', '71.3 N', '69.1 N', '36 N'], answer=0, type='numerical',
                  explanation=r'\(W_h\approx W(1-2h/R)=72(1-0.02)=70.56\approx70.6\) N. 71.3 N uses a 1% drop, forgetting the factor 2 from the inverse square. 36 N is the weight at a height of about 0.41R, not R/100.'),
         ],
     )),

dict(chapter='maths', after='maths-calculus', id='maths-maxima',
     title='Maxima and minima with derivatives',
     intro=r'At the top of a hill or the bottom of a valley on a smooth graph, the tangent is flat. So a maximum or minimum of \(y(x)\) occurs where \(dy/dx=0\).',
     reasoning=r'The second derivative tells which one it is. If \(d^2y/dx^2\lt0\), the curve bends down and the point is a maximum. If \(d^2y/dx^2\gt0\), the point is a minimum. Physics uses this for the highest point of a throw, the angle for maximum range, the least force to drag a block and the closest approach of two bodies.',
     formula=r'\frac{dy}{dx}=0;\qquad \frac{d^2y}{dx^2}\lt0\Rightarrow\text{maximum},\quad \frac{d^2y}{dx^2}\gt0\Rightarrow\text{minimum}',
     symbols='y(x) is a smooth function of x; the derivatives are evaluated at the point where dy/dx = 0. On a restricted range, also check the end points.',
     trap=r'\(dy/dx=0\) alone does not prove a maximum or minimum. For \(y=x^3\) the slope is zero at \(x=0\), but it is neither: the curve just flattens and keeps rising.',
     example=r'A ball&#39;s height is \(y=20t-5t^2\) m. Find the maximum height.',
     solution=r'\(dy/dt=20-10t=0\) gives \(t=2\) s. \(d^2y/dt^2=-10\lt0\), so it is a maximum. \(y_{\max}=40-20=20\) m.',
     question=r'The minimum value of \(y=x^2-4x+7\) is',
     options='7|3|2|4', answer=1,
     explanation=r'\(dy/dx=2x-4=0\) at \(x=2\), and \(d^2y/dx^2=2\gt0\). So \(y_{\min}=4-8+7=3\). The value 2 is where the minimum occurs, not the minimum itself.',
     deep=dict(
         level='exam',
         notes=[
             ('The recipe and why it works', r'''<ol><li>Write the quantity to be optimised as a function of one variable.</li>
<li>Differentiate and set the derivative to zero. Solve for the variable.</li>
<li>Check the second derivative, or check the sign of the first derivative on each side.</li>
<li>Substitute back to get the maximum or minimum value.</li></ol>
<p>Just before a maximum the function rises (\(dy/dx\gt0\)); just after, it falls (\(dy/dx\lt0\)). So the slope passes through zero while decreasing. That is what \(d^2y/dx^2\lt0\) says.</p>'''),
             ('Standard results worth remembering', r'''<ul><li>Range \(R=\dfrac{u^2\sin2\theta}{g}\) is maximum at \(\theta=45^\circ\).</li>
<li>\(a\sin\theta+b\cos\theta\) has maximum value \(\sqrt{a^2+b^2}\).</li>
<li>If \(x+y\) is fixed, the product \(xy\) is largest when \(x=y\).</li>
<li>Least force to drag a block on a rough floor: \(F_{\min}=\dfrac{\mu mg}{\sqrt{1+\mu^2}}\), applied at \(\tan\theta=\mu\) above the horizontal.</li></ul>'''),
             ('Closest approach of two moving bodies', r'''<p>Write the separation squared, \(s^2(t)\), as a function of time. Minimising \(s^2\) is easier than minimising \(s\) and gives the same time. Set \(d(s^2)/dt=0\).</p>'''),
         ],
         formulas=[
             dict(title='Maximum of a sin θ + b cos θ', formula=r'\left(a\sin\theta+b\cos\theta\right)_{\max}=\sqrt{a^2+b^2}\quad\text{at }\tan\theta=\frac ab',
                  symbols='a and b are constants with the same units; θ is an angle. The minimum value is −√(a² + b²).'),
             dict(title='Least pulling force on a rough floor', formula=r'F(\theta)=\frac{\mu mg}{\cos\theta+\mu\sin\theta},\qquad F_{\min}=\frac{\mu mg}{\sqrt{1+\mu^2}}\ \text{at}\ \tan\theta=\mu',
                  symbols='μ is the coefficient of friction, m is mass (kg), g is 10 m/s², θ is the angle of the pull above the horizontal. Assumes the block is just about to slide (limiting friction).'),
         ],
         figure=dict(svg=_fig_maxmin(), caption='At a maximum and a minimum the tangent is horizontal. The sign of the second derivative tells them apart.'),
         traps=[r'A maximum on a restricted range may sit at an end point, where \(dy/dx\ne0\). Check the end points too.',
                r'Find the value of the variable, then substitute back. Many students stop at "\(x=2\)" when the question asks for the minimum <em>value</em> of \(y\).'],
         exam=r'''<ul><li>"Find the maximum height" or "the time when velocity is maximum" (set \(a=0\)).</li>
<li>"At what angle is the range maximum?"</li>
<li>"Minimum force needed to move a block on a rough floor" and its angle.</li>
<li>"Minimum distance between two particles moving on perpendicular roads".</li>
<li>Pure maths: maximum of \(3\sin\theta+4\cos\theta\).</li></ul>''',
         examples=[
             dict(tag='Numerical', q=r'Show that the range \(R=\dfrac{u^2\sin2\theta}{g}\) is maximum at 45°.',
                  steps=[r'\(\dfrac{dR}{d\theta}=\dfrac{2u^2\cos2\theta}{g}=0\Rightarrow\cos2\theta=0\Rightarrow\theta=45^\circ\).',
                         r'\(\dfrac{d^2R}{d\theta^2}=-\dfrac{4u^2\sin2\theta}{g}\), which is negative at 45°.',
                         r'So 45° gives a maximum, \(R_{\max}=u^2/g\).'],
                  answer=r'\(\theta=45^\circ\), \(R_{\max}=u^2/g\)'),
             dict(tag='Numerical', q=r'A 4 kg block rests on a floor with \(\mu=0.75\). A rope pulls it at angle \(\theta\) above the horizontal. Find the least force that just moves it, and the angle. Use \(g=10\ \text{m/s}^2\).',
                  steps=[r'Normal force: \(N=mg-F\sin\theta\). Just sliding: \(F\cos\theta=\mu N\).',
                         r'So \(F=\dfrac{\mu mg}{\cos\theta+\mu\sin\theta}\). F is least when the denominator is largest.',
                         r'Largest value of \(\cos\theta+\mu\sin\theta\) is \(\sqrt{1+\mu^2}=\sqrt{1.5625}=1.25\), at \(\tan\theta=0.75\), so \(\theta\approx37^\circ\).',
                         r'\(F_{\min}=\dfrac{0.75\times4\times10}{1.25}=24\) N. A horizontal pull would need 30 N.'],
                  answer=r'24 N at about 37° above the horizontal'),
             dict(tag='Numerical', q=r'Car A is 100 m east of a crossing and drives west toward it at 8 m/s. At the same moment car B leaves the crossing heading north at 6 m/s. Find the minimum distance between them.',
                  steps=[r'At time \(t\): A is \(100-8t\) m east, B is \(6t\) m north.',
                         r'\(s^2=(100-8t)^2+(6t)^2\).',
                         r'\(\dfrac{d(s^2)}{dt}=-16(100-8t)+72t=0\Rightarrow200t=1600\Rightarrow t=8\) s.',
                         r'Then A is 36 m east and B is 48 m north: \(s=\sqrt{36^2+48^2}=60\) m.'],
                  answer=r'60 m, at t = 8 s'),
         ],
         practice=[
             dict(q=r'For \(y=2x^3-3x^2\), the local minimum value of \(y\) is',
                  options=['0', '−1', '1', '−2'], answer=1, type='numerical',
                  explanation=r'\(dy/dx=6x^2-6x=0\) at \(x=0\) and \(x=1\). \(d^2y/dx^2=12x-6\) is negative at 0 (maximum, \(y=0\)) and positive at 1 (minimum). \(y(1)=2-3=-1\). The value 0 is the local maximum. 1 is the position of the minimum, not its value.'),
             dict(q=r'The maximum value of \(3\sin\theta+4\cos\theta\) is',
                  options=['5', '7', '1', '12'], answer=0, type='numerical',
                  explanation=r'\(\sqrt{3^2+4^2}=5\). 7 adds the two maxima, but \(\sin\theta\) and \(\cos\theta\) cannot both be 1 at the same angle. 1 is the difference; 12 is the product.'),
             dict(q=r'Two positive numbers add to 20. Their largest possible product is',
                  options=['96', '75', '100', '200'], answer=2, type='numerical',
                  explanation=r'\(P=x(20-x)\). \(dP/dx=20-2x=0\) gives \(x=10\), and \(P=100\). 96 (12 × 8) and 75 (15 × 5) are smaller products. 200 does not satisfy the sum condition.'),
             dict(q=r'Assertion: At the highest point of a vertical throw, \(dy/dt=0\). Reason: At a maximum of a smooth function, its first derivative is zero.',
                  options=AR_OPTS, answer=0, type='ar',
                  explanation=r'Height is maximum at the top, so its derivative (vertical velocity) is zero there. The reason is the general rule that produces the assertion, so it is the correct explanation.'),
         ],
     )),
]
