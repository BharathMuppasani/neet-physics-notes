"""Deepening layer: Work, Energy & Power.

g = 10 m/s² throughout unless a question says otherwise. Every number was checked with python3.
"""
import math

R = str

AR = ['Both A and R are true, and R correctly explains A',
      'Both A and R are true, but R does not explain A',
      'A is true but R is false',
      'A is false but R is true']
ST = ['Both Statement I and Statement II are true',
      'Both Statement I and Statement II are false',
      'Statement I is true but Statement II is false',
      'Statement I is false but Statement II is true']


# ---------- small SVG helpers (figures use CSS colour variables) ----------
def _arrow(x1, y1, x2, y2, color='var(--coral)', w=2.2, head=9):
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * math.cos(ang), y2 - head * math.sin(ang)
    hx, hy = head * 0.45 * math.sin(ang), head * 0.45 * math.cos(ang)
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}" style="stroke:{color};stroke-width:{w}"/>'
            f'<polygon points="{x2:.1f},{y2:.1f} {bx + hx:.1f},{by - hy:.1f} {bx - hx:.1f},{by + hy:.1f}" style="fill:{color}"/>')


def _t(x, y, s, size=12, color='var(--ink-2)', anchor='start', weight='normal'):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" '
            f'style="fill:{color}">{s}</text>')


def _line(x1, y1, x2, y2, color='var(--ink-2)', w=1.5, dash=''):
    d = f';stroke-dasharray:{dash}' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" style="stroke:{color};stroke-width:{w}{d}"/>'


def _sub(base, sub, rest=''):
    return f'{base}<tspan dy="3" font-size="0.75em">{sub}</tspan><tspan dy="-3">{rest}</tspan>'


def _sup(base, sup, rest=''):
    return f'{base}<tspan dy="-5" font-size="0.75em">{sup}</tspan><tspan dy="5">{rest}</tspan>'


# Figure: F–x graph with signed areas. x: px = 60 + 50x ; F: py = 120 − 8F
def _fx(x, F):
    return 60 + 50 * x, 120 - 8 * F


_P = [_fx(*p) for p in [(0, 0), (2, 10), (4, 10), (5, 0)]]
_N = [_fx(*p) for p in [(5, 0), (6, -10), (6, 0)]]
FIG_FX = ('<svg viewBox="0 0 400 240" role="img" aria-label="Force against position graph: force rises from 0 to 10 N over 2 m, stays at 10 N to 4 m, then falls to minus 10 N at 6 m. Area above the axis is positive work, area below is negative work.">'
          + '<polygon points="' + ' '.join(f'{x:.0f},{y:.0f}' for x, y in _P) + '" style="fill:var(--green-soft);stroke:none"/>'
          + '<polygon points="' + ' '.join(f'{x:.0f},{y:.0f}' for x, y in _N) + '" style="fill:var(--coral-soft);stroke:none"/>'
          + _line(60, 120, 380, 120) + _line(60, 30, 60, 210)
          + '<polyline points="60,120 160,40 260,40 360,200" style="fill:none;stroke:var(--indigo);stroke-width:2.6"/>'
          + ''.join(_line(60 + 50 * i, 117, 60 + 50 * i, 123) + _t(60 + 50 * i, 136, str(i), 11, 'var(--muted)', 'middle') for i in range(1, 7))
          + _t(54, 44, '10', 11, 'var(--muted)', 'end') + _t(54, 204, '−10', 11, 'var(--muted)', 'end') + _t(54, 124, '0', 11, 'var(--muted)', 'end')
          + _line(60, 40, 160, 40, 'var(--muted)', 1, '3 3')
          + _t(380, 112, 'x (m)', 12, anchor='end') + _t(66, 26, 'F (N)', 12)
          + _t(190, 92, '+35 J', 13, 'var(--green)', 'middle', 'bold') + _t(366, 168, '−5 J', 13, 'var(--coral)', 'start', 'bold')
          + _t(200, 230, 'Net work from 0 to 6 m = 35 − 5 = 30 J', 12, anchor='middle')
          + '</svg>')


# Figure: potential-energy curve
def _U(x):
    return 3.4 - 2.6 * math.exp(-(x - 2.6) ** 2 / 1.1) + 2.2 * math.exp(-(x - 5.6) ** 2 / 0.9) + 1.6 * math.exp(-(x - 0.2) * 2.2)


def _ux(x):
    return 40 + 34 * x


def _uy(u):
    return 220 - 36 * u


_xs = [0.3 + i * 0.05 for i in range(int((9.6 - 0.3) / 0.05) + 1)]
_curve = ' '.join(f'{_ux(x):.1f},{_uy(_U(x)):.1f}' for x in _xs)
_E = 2.6
_turn = [a for a, b in zip(_xs, _xs[1:]) if (_U(a) - _E) * (_U(b) - _E) < 0 and a < 5]
assert len(_turn) == 2, _turn
_xmin = min((x for x in _xs if 1.5 < x < 4), key=_U)
_xmax = max((x for x in _xs if 4.5 < x < 7), key=_U)
FIG_U = ('<svg viewBox="0 -12 400 262" role="img" aria-label="Potential energy curve with a well (stable equilibrium) and a hump (unstable equilibrium), a flat region at large x, and a total energy line crossing the well at two turning points">'
         + _line(40, 220, 385, 220) + _line(40, 220, 40, 20)
         + _t(385, 238, 'x', 12, anchor='end') + _t(46, 18, 'U(x)', 12)
         + f'<polyline points="{_curve}" style="fill:none;stroke:var(--indigo);stroke-width:2.6"/>'
         + _line(40, _uy(_E), 385, _uy(_E), 'var(--coral)', 1.4, '6 4') + _t(380, _uy(_E) - 6, 'total energy E', 11, 'var(--coral)', 'end')
         + ''.join(f'<circle cx="{_ux(x):.1f}" cy="{_uy(_E):.1f}" r="4" style="fill:var(--coral)"/>' for x in _turn)
         + _t(_ux(_turn[0]) - 6, _uy(_E) - 8, 'turning point', 10, 'var(--coral)', 'end')
         + _t(_ux(_turn[1]) + 6, _uy(_E) + 16, 'turning point', 10, 'var(--coral)'))
FIG_U += (f'<circle cx="{_ux(_xmin):.1f}" cy="{_uy(_U(_xmin)):.1f}" r="4" style="fill:var(--green)"/>'
          + _t(_ux(_xmin), _uy(_U(_xmin)) + 18, 'A: minimum, stable', 11, 'var(--green)', 'middle')
          + _line(_ux(_xmin), _uy(_U(_xmin)), _ux(_xmin), _uy(_E), 'var(--green)', 1.2, '2 3')
          + _t(_ux(_xmin) - 5, (_uy(_U(_xmin)) + _uy(_E)) / 2 + 4, 'K largest', 10, 'var(--green)', 'end')
          + f'<circle cx="{_ux(_xmax):.1f}" cy="{_uy(_U(_xmax)):.1f}" r="4" style="fill:var(--amber)"/>'
          + _t(_ux(_xmax), _uy(_U(_xmax)) - 10, 'B: maximum, unstable', 11, 'var(--amber)', 'middle')
          + _t(_ux(8.6), _uy(_U(8.6)) - 10, 'C: flat, neutral', 11, 'var(--plum)', 'middle')
          + _t(200, 246, 'F = −dU/dx: force points downhill on the curve', 11, 'var(--muted)', 'middle')
          + '</svg>')


# Figure: block compressing a spring + spring F–x graph
def _zigzag(x1, x2, y, n=8, amp=9):
    pts = [(x1, y)]
    step = (x2 - x1) / (2 * n)
    for i in range(1, 2 * n):
        pts.append((x1 + i * step, y + (amp if i % 2 else -amp)))
    pts.append((x2, y))
    return '<polyline points="' + ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts) + '" style="fill:none;stroke:var(--ink-2);stroke-width:1.6"/>'


FIG_SPRING = ('<svg viewBox="0 0 440 210" role="img" aria-label="Left: a block moving toward a spring fixed to a wall. Right: spring force against compression is a straight line; the triangle under it is the stored energy one half k x squared.">'
              + '<rect x="20" y="70" width="12" height="80" style="fill:var(--surface-2);stroke:var(--ink-2)"/>'
              + _line(20, 150, 215, 150, 'var(--ink-2)', 2)
              + _zigzag(32, 120, 125)
              + '<rect x="120" y="105" width="44" height="45" style="fill:var(--water-soft);stroke:var(--water);stroke-width:1.5"/>'
              + _t(142, 132, 'm', 13, anchor='middle', weight='bold')
              + _arrow(170, 95, 210, 95, 'var(--coral)') + _t(190, 86, 'v', 13, 'var(--coral)', 'middle', 'bold')
              + _t(30, 180, 'Max compression: ½mv² = ½kx²', 11) + _t(30, 196, 'so x = v√(m/k)', 11)
              + _line(250, 170, 425, 170) + _line(250, 170, 250, 30)
              + '<polygon points="250,170 390,170 390,50" style="fill:var(--amber-soft);stroke:none"/>'
              + _line(250, 170, 400, 41.4, 'var(--indigo)', 2.4)
              + _line(390, 50, 390, 170, 'var(--muted)', 1, '3 3') + _line(250, 50, 390, 50, 'var(--muted)', 1, '3 3')
              + _t(244, 54, 'kx', 11, anchor='end') + _t(390, 186, 'x', 11, anchor='middle')
              + _t(425, 204, 'compression', 11, 'var(--muted)', 'end') + _t(256, 26, 'spring force', 11)
              + _t(345, 140, 'area = ½kx²', 12, 'var(--amber)', 'middle', 'bold')
              + _t(300, 92, 'slope = k', 11, 'var(--indigo)', 'end')
              + '</svg>')

# Figure: vertical circle (limiting case)
_cx, _cy, _r = 190, 125, 78
FIG_LOOP = ('<svg viewBox="0 0 420 260" role="img" aria-label="Vertical circle on a string in the limiting case: at the bottom speed root 5gr and tension 6mg, at the side speed root 3gr and tension 3mg, at the top speed root gr and tension zero">'
            + f'<circle cx="{_cx}" cy="{_cy}" r="{_r}" style="fill:none;stroke:var(--line-2);stroke-width:1.5;stroke-dasharray:5 4"/>'
            + f'<circle cx="{_cx}" cy="{_cy}" r="3" style="fill:var(--ink-2)"/>'
            + _line(_cx, _cy, _cx, _cy + _r, 'var(--ink-2)', 1.4) + _line(_cx, _cy, _cx + _r, _cy, 'var(--ink-2)', 1.4) + _line(_cx, _cy, _cx, _cy - _r, 'var(--ink-2)', 1, '2 3')
            + _t(_cx + 4, _cy + 40, 'r', 12)
            + ''.join(f'<circle cx="{x}" cy="{y}" r="7" style="fill:var(--water);stroke:var(--ink-2)"/>' for x, y in [(_cx, _cy + _r), (_cx + _r, _cy), (_cx, _cy - _r)])
            + _arrow(_cx, _cy + _r, _cx + 60, _cy + _r, 'var(--coral)') + _arrow(_cx + _r, _cy, _cx + _r, _cy - 42, 'var(--coral)') + _arrow(_cx, _cy - _r, _cx - 34, _cy - _r, 'var(--coral)')
            + _t(_cx + 66, _cy + _r + 4, 'v = √(5gr)', 12, 'var(--coral)') + _t(_cx + 66, _cy + _r + 20, 'T = 6mg', 12, 'var(--indigo)', weight='bold')
            + _t(_cx + _r + 12, _cy - 4, 'v = √(3gr)', 12, 'var(--coral)') + _t(_cx + _r + 12, _cy + 12, 'T = 3mg', 12, 'var(--indigo)', weight='bold')
            + _t(_cx - 40, _cy - _r - 14, 'v = √(gr)', 12, 'var(--coral)', 'end') + _t(_cx + 14, _cy - _r - 14, 'T = 0', 12, 'var(--indigo)', weight='bold')
            + _t(20, 250, 'Limiting complete circle on a light string: T(bottom) − T(top) = 6mg always.', 11, 'var(--muted)')
            + '</svg>')


# Figure: bouncing ball heights
def _bounce_svg(e=0.6):
    g0, h0 = 200, 150
    out = [_line(20, g0, 410, g0, 'var(--ink-2)', 2), _line(50, g0 - h0, 50, g0, 'var(--water)', 1.6, '5 4'),
           f'<circle cx="50" cy="{g0 - h0}" r="6" style="fill:var(--water)"/>', _t(58, g0 - h0 + 4, 'h', 13, weight='bold')]
    x = 50
    labels = [_sup('e', '2', 'h'), _sup('e', '4', 'h'), _sup('e', '6', 'h')]
    for n in range(1, 4):
        H = h0 * e ** (2 * n)
        w = 170 * e ** n
        out.append(f'<path d="M{x:.1f} {g0} Q{x + w / 2:.1f} {g0 - 2 * H:.1f} {x + w:.1f} {g0}" style="fill:none;stroke:var(--water);stroke-width:1.8"/>')
        out.append(_line(x + w / 2, g0 - H, x + w / 2, g0, 'var(--muted)', 1, '2 3'))
        out.append(_t(x + w / 2, g0 - H - 6, _sub('h', str(n), ' = ') + labels[n - 1], 11, 'var(--indigo)', 'middle'))
        x += w
    out.append(_t(20, 230, 'Each bounce multiplies speed by e and height by e². Here e = 0.6.', 11, 'var(--muted)'))
    return '<svg viewBox="0 0 420 240" role="img" aria-label="A ball dropped from height h bounces to heights e squared h, e to the fourth h and e to the sixth h">' + ''.join(out) + '</svg>'


FIG_BOUNCE = _bounce_svg()


DEEP = {
'work-work': dict(
    level='basic',
    notes=[
        ('Sign of work and the zero-work cases', r'''<p>W = Fs cosθ, where θ is the angle between the force and the displacement.</p>
<ul><li><strong>Positive (0 ≤ θ &lt; 90°):</strong> the force helps the motion. Gravity on a falling ball, the pull on a dragged box.</li>
<li><strong>Zero (θ = 90°, or no displacement):</strong> centripetal force in uniform circular motion, tension in a swinging pendulum string, the normal force on a block sliding on a fixed surface, a porter holding a load still or carrying it horizontally at steady speed (his upward force is perpendicular to the motion).</li>
<li><strong>Negative (90° &lt; θ ≤ 180°):</strong> the force opposes the motion. Friction on a block sliding over a fixed floor, gravity on a ball going up, brakes.</li></ul>
<p>Work is a scalar, measured in joules: 1 J = 1 N m = 10⁷ erg. Other units: 1 kWh = 3.6 × 10⁶ J and 1 eV = 1.6 × 10⁻¹⁹ J.</p>'''),
        ('Variable forces and the F–x graph', r'''<p>When F changes with position, split the path into tiny steps dx. On each step the force is nearly constant, so dW = F dx. Adding them gives W = ∫F dx, which is the area under the F–x graph.</p>
<ul><li>Area above the x-axis counts as positive work; area below counts as negative.</li>
<li>Break the graph into triangles, rectangles and trapeziums and add the signed areas.</li>
<li>In vector form, \(W=\int(F_x\,dx+F_y\,dy+F_z\,dz)\). For a constant force this is simply \(F_x\Delta x+F_y\Delta y+F_z\Delta z\).</li></ul>
<p>Work done by gravity depends only on the vertical drop: \(W_g=mgh\) for a fall through h, along any path.</p>'''),
    ],
    formulas=[
        dict(title='Work by a constant force in components',
             formula=r'W=\vec F\cdot\Delta\vec r=F_x\Delta x+F_y\Delta y+F_z\Delta z',
             symbols='Fₓ, F_y, F_z components of the constant force (N); Δx, Δy, Δz components of the displacement (m); W work (J).'),
        dict(title='Energy unit conversions',
             formula=r'1\ \text{J}=10^7\ \text{erg},\quad 1\ \text{kWh}=3.6\times10^6\ \text{J},\quad 1\ \text{eV}=1.6\times10^{-19}\ \text{J}',
             symbols='erg is the CGS unit (dyne cm); kWh is the commercial "unit" of electrical energy; eV is the energy gained by an electron through 1 volt.'),
    ],
    figure=dict(svg=FIG_FX, caption='Work from an F–x graph. Area above the axis (green) is positive work, area below (coral) is negative. Here 10 + 20 + 5 = 35 J positive, 5 J negative, so 30 J net.'),
    traps=[r'When a graph dips below the x-axis, subtract that area. Adding all areas as positive overestimates the work.',
           r'Work done by a person holding a heavy bag still is zero in physics, even though the person gets tired. Muscles use energy internally, but the bag does not move.'],
    exam=r'''<ul><li>"F = (… î + … ĵ) N moves a body from point A to point B. Find the work." Use the dot product with the displacement.</li>
<li>F–x graph with parts above and below the axis: find the net work or the speed at the end.</li>
<li>F = f(x) given as a polynomial: integrate between limits.</li>
<li>"Work done by the centripetal force / tension / normal force is …" (zero).</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A constant force F = (3î + 4ĵ − 2k̂) N moves a particle from (1, 0, 2) m to (3, 2, 1) m. Find the work done.',
             steps=[r'Displacement Δr = (3 − 1)î + (2 − 0)ĵ + (1 − 2)k̂ = 2î + 2ĵ − k̂ m.',
                    r'W = F·Δr = 3 × 2 + 4 × 2 + (−2)(−1).',
                    r'W = 6 + 8 + 2 = 16 J.'],
             answer=r'16 J'),
        dict(tag='Graph', q=r'Use the F–x graph in the figure: F rises from 0 to 10 N over the first 2 m, stays at 10 N up to 4 m, then falls linearly to −10 N at 6 m. Find the work done from x = 0 to x = 6 m.',
             steps=[r'0 to 2 m: triangle ½ × 2 × 10 = 10 J.',
                    r'2 to 4 m: rectangle 2 × 10 = 20 J.',
                    r'The line from (4, 10) to (6, −10) crosses zero at x = 5 m. From 4 to 5 m: triangle ½ × 1 × 10 = +5 J.',
                    r'From 5 to 6 m: triangle below the axis, −5 J.',
                    r'Net work = 10 + 20 + 5 − 5 = 30 J.'],
             answer=r'30 J'),
        dict(tag='Numerical', q=r'A force F = (3x² − 2x) N acts along the x-axis. Find the work it does as the particle moves from x = 1 m to x = 3 m.',
             steps=[r'W = ∫ from 1 to 3 of (3x² − 2x) dx = [x³ − x²] from 1 to 3.',
                    r'At 3: 27 − 9 = 18. At 1: 1 − 1 = 0.',
                    r'W = 18 J.'],
             answer=r'18 J'),
    ],
    practice=[
        dict(q=r'A constant force F = (2î − ĵ + 3k̂) N produces a displacement d = (4î + 2ĵ − k̂) m. The work done is',
             options=['13 J', '3 J', '9 J', '−3 J'], answer=1, type='numerical',
             explanation=r'W = F·d = 2 × 4 + (−1)(2) + 3(−1) = 8 − 2 − 3 = 3 J. 13 J adds the magnitudes of the products and ignores the signs. 9 J drops the last term only.'),
        dict(q=r'Which forces do zero work?<br>(i) Centripetal force on a body in uniform circular motion<br>(ii) Tension in the string of a swinging simple pendulum<br>(iii) Kinetic friction on a block sliding on a fixed floor<br>(iv) Normal force on a block sliding down a fixed incline',
             options=['(i) and (ii) only', '(i), (ii) and (iv)', '(iii) and (iv) only', 'All four'], answer=1, type='multi',
             explanation=r'In (i), (ii) and (iv) the force is perpendicular to the velocity at every instant, so W = 0. Kinetic friction in (iii) opposes the sliding and does negative work. Options containing (iii) are wrong; option 1 misses (iv).'),
        dict(q=r'A force is 5 N from x = 0 to x = 3 m, then decreases linearly to zero at x = 5 m. The work done from 0 to 5 m is',
             options=['15 J', '25 J', '20 J', '12.5 J'], answer=2, type='graph',
             explanation=r'Rectangle: 5 × 3 = 15 J. Triangle: ½ × 2 × 5 = 5 J. Total 20 J. 25 J treats the force as constant all the way to 5 m. 15 J leaves out the triangle.'),
        dict(q=r'A 2 kg block is pulled slowly up a smooth 30° incline through a distance of 4 m along the incline (g = 10 m/s²). The work done by the pulling force is',
             options=['80 J', '69 J', '0 J', '40 J'], answer=3, type='numerical',
             explanation=r'Pulling slowly means no change in kinetic energy, so the pull does work equal to the gain in potential energy: mgh = 2 × 10 × (4 sin30°) = 40 J. 80 J uses the length 4 m as the height. 69 J uses cos30° instead of sin30°.'),
    ],
),

'work-theorem': dict(
    level='core',
    notes=[
        ('Derivation from Newton’s second law', r'''<ol><li>For a particle moving along x under a net force F: \(F=ma=m\dfrac{dv}{dt}\).</li>
<li>Use the chain rule: \(\dfrac{dv}{dt}=\dfrac{dv}{dx}\dfrac{dx}{dt}=v\dfrac{dv}{dx}\). So \(F=mv\dfrac{dv}{dx}\).</li>
<li>Multiply by dx and integrate: \(\displaystyle\int_{x_i}^{x_f}F\,dx=\int_{u}^{v}mv\,dv=\tfrac12mv^2-\tfrac12mu^2\).</li>
<li>The left side is the net work. So W_net = ΔK.</li></ol>
<p>Nothing in the derivation assumed F was constant or conservative. The theorem holds for any forces, as long as you include all of them and work in an inertial frame.</p>'''),
        ('Kinetic energy and momentum', r'''<p>Since p = mv, \(K=\dfrac{p^2}{2m}\) and \(p=\sqrt{2mK}\). This link drives most ratio questions:</p>
<ul><li><strong>Same momentum:</strong> K ∝ 1/m. The lighter body has more kinetic energy.</li>
<li><strong>Same kinetic energy:</strong> p ∝ √m. The heavier body has more momentum.</li>
<li><strong>Percentage changes:</strong> if p rises by 20%, K rises by a factor 1.2² = 1.44, i.e. 44%. If K rises by 300% (becomes 4K), p doubles (rises by 100%).</li>
<li>For small changes only: ΔK/K ≈ 2Δp/p (so a 1% rise in p gives about 2% rise in K).</li></ul>'''),
        ('Stopping problems: bullets and planks', r'''<p>A resistive force that is constant removes kinetic energy in proportion to distance. If a bullet loses half its speed after penetrating a distance d, it has lost ¾ of its kinetic energy. The remaining ¼ needs only d/3 more. In general, the number of identical planks a bullet can cross is proportional to its initial kinetic energy.</p>'''),
    ],
    formulas=[
        dict(title='Kinetic energy and momentum',
             formula=r'K=\frac{p^2}{2m},\qquad p=\sqrt{2mK}',
             symbols='K kinetic energy (J); p momentum magnitude (kg m/s); m mass (kg).'),
        dict(title='Work–energy theorem for a variable force',
             formula=r'\int_{x_i}^{x_f}F_{\rm net}\,dx=\tfrac12mv^2-\tfrac12mu^2',
             symbols='F_net net force along the path (N); u, v initial and final speeds (m/s); m mass (kg). Valid in an inertial frame for any forces.'),
    ],
    traps=[r'A 20% increase in speed does not mean a 20% increase in kinetic energy. K ∝ v², so it rises by 44%.',
           r'The work–energy theorem is not limited to conservative forces. Friction, air drag and muscle forces all enter W_net.'],
    exam=r'''<ul><li>"If the momentum of a body is increased by n%, its kinetic energy increases by …"</li>
<li>Two bodies with equal kinetic energy (or equal momentum): ratio of momenta (or of kinetic energies).</li>
<li>Bullet into a block or planks: further penetration after losing part of its speed.</li>
<li>A body dropped into sand: average resistive force from h and the penetration depth.</li>
<li>Graphs: K against v (parabola), K against p² (straight line), √K against v (straight line).</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A bullet loses half its speed after penetrating 3 cm into a wooden block. Assuming constant resistance, how much farther will it penetrate?',
             steps=[r'Half the speed means K becomes ¼ of the original. So ¾K is lost in 3 cm.',
                    r'Constant resistance F: F × 3 cm = ¾K, so F = K/(4 cm).',
                    r'The remaining ¼K needs a distance (¼K)/F = 1 cm.'],
             answer=r'1 cm more (4 cm in total)'),
        dict(tag='Ratio', q=r'The kinetic energy of a body increases by 300%. By what percentage does its momentum increase?',
             steps=[r'An increase of 300% means K becomes K + 3K = 4K.',
                    r'p = √(2mK), so p becomes √4 = 2 times its value.',
                    r'An increase from p to 2p is a 100% increase.'],
             answer=r'100%'),
        dict(tag='Numerical', q=r'A 2 kg stone falls from rest through 5 m into sand and stops after sinking 5 cm. Find the average resistive force of the sand.',
             steps=[r'Initial and final kinetic energies are both zero, so W_net = 0.',
                    r'Gravity acts through the whole 5.05 m: W_g = 20 × 5.05 = 101 J.',
                    r'Sand acts through 0.05 m: W_sand = −F × 0.05.',
                    r'0 = 101 − 0.05F, so F = 2020 N (about 100 times the weight).'],
             answer=r'About 2020 N'),
    ],
    practice=[
        dict(q=r'The momentum of a body is increased by 20%. Its kinetic energy increases by',
             options=['20%', '40%', '44%', '120%'], answer=2, type='numerical',
             explanation=r'K = p²/2m, so K scales by 1.2² = 1.44, an increase of 44%. 40% is the small-change approximation 2 × 20%, which is not accurate for a 20% change. 20% assumes K ∝ p.'),
        dict(q=r'Bodies of mass 1 kg and 4 kg have equal kinetic energies. The ratio of their momenta p₁ : p₂ is',
             options=['1 : 2', '1 : 4', '2 : 1', '1 : 16'], answer=0, type='numerical',
             explanation=r'p = √(2mK) ∝ √m for equal K. So p₁ : p₂ = √1 : √4 = 1 : 2. 1 : 4 forgets the square root, and 2 : 1 is the ratio of their speeds, not their momenta.'),
        dict(q=r'<strong>Statement I:</strong> The work–energy theorem holds only when all the forces are conservative.<br><strong>Statement II:</strong> The work–energy theorem follows from Newton’s second law.',
             options=ST, answer=3, type='statement',
             explanation=r'The derivation uses only F = ma integrated along the path, so it holds for all forces, including friction. Statement I is false and Statement II is true.'),
        dict(q=r'For a body of fixed mass, which graph is a straight line through the origin?',
             options=['K against p', 'K against v', 'K against p²', '√K against p²'], answer=2, type='graph',
             explanation=r'K = p²/(2m), so K against p² is a straight line through the origin with slope 1/(2m). K against p and K against v are parabolas. √K is proportional to p, so √K against p² is a curve.'),
    ],
),

'work-potential': dict(
    level='core',
    notes=[
        ('Testing whether a force is conservative', r'''<p>A force is conservative if any one of these equivalent statements holds:</p>
<ul><li>The work it does between two points does not depend on the path.</li>
<li>The work it does around any closed path is zero.</li>
<li>It can be written as \(F_x=-dU/dx\) for some potential-energy function U.</li></ul>
<p>Gravity, the spring force and the electrostatic force are conservative. Friction, air drag and viscous forces are not: their work around a closed loop is always negative, because they oppose the motion everywhere.</p>
<p>Near Earth’s surface U = mgh is valid only for h much smaller than Earth’s radius; for large heights use the gravitation chapter’s −GMm/r.</p>'''),
        ('Reading a potential-energy curve', r'''<p>Use F = −dU/dx: the force is minus the slope. A particle is pushed "downhill" on the U–x graph.</p>
<ul><li><strong>Equilibrium:</strong> F = 0, so dU/dx = 0 (flat points of the curve).</li>
<li><strong>Stable</strong> (point A, a minimum, d²U/dx² &gt; 0): a small displacement brings a restoring force back toward A. The particle oscillates.</li>
<li><strong>Unstable</strong> (point B, a maximum, d²U/dx² &lt; 0): a small displacement gives a force pushing it further away.</li>
<li><strong>Neutral</strong> (region C, flat, d²U/dx² = 0): displaced, it stays put.</li></ul>
<p>With total energy E, the kinetic energy at any x is K = E − U(x). Motion is possible only where E ≥ U. The points where E = U are <em>turning points</em>: the particle stops there and turns back. K (and speed) is largest where U is smallest.</p>'''),
    ],
    formulas=[
        dict(title='Equilibrium from U(x)',
             formula=r'\frac{dU}{dx}=0;\quad \frac{d^2U}{dx^2}>0\ \text{stable},\quad <0\ \text{unstable},\quad =0\ \text{neutral}',
             symbols='U potential energy (J) as a function of position x (m). The second-derivative test classifies each equilibrium point.'),
        dict(title='Kinetic energy from the energy line',
             formula=r'K(x)=E-U(x)\ge 0',
             symbols='E total mechanical energy (J), constant when only conservative forces act; U(x) potential energy (J); K kinetic energy (J). Turning points are where U(x) = E.'),
    ],
    figure=dict(svg=FIG_U, caption='A potential-energy curve. Force is minus the slope. A (minimum) is stable, B (maximum) is unstable, C (flat) is neutral. With total energy E, the particle is trapped between the two turning points and moves fastest at A.'),
    traps=[r'Where U is zero, the force is not necessarily zero. Force depends on the slope of U, not its value.',
           r'"Equilibrium" means zero net force, not zero speed. A particle can pass through a stable equilibrium point at its maximum speed.'],
    exam=r'''<ul><li>"U(x) = … Find the equilibrium position(s) and state whether stable or unstable."</li>
<li>Molecular potential U = a/r¹² − b/r⁶: equilibrium separation r = (2a/b)^(1/6).</li>
<li>U–x graph with an energy line: find turning points, region of motion, where speed is maximum, or the force direction at a point.</li>
<li>Assertion–reason on conservative forces and closed-path work.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'U(x) = x³/3 − 4x (SI units). Find the equilibrium points and classify them.',
             steps=[r'dU/dx = x² − 4 = 0, so x = +2 m or x = −2 m.',
                    r'd²U/dx² = 2x.',
                    r'At x = +2: d²U/dx² = 4 &gt; 0, a minimum, so stable.',
                    r'At x = −2: d²U/dx² = −4 &lt; 0, a maximum, so unstable.'],
             answer=r'x = 2 m stable; x = −2 m unstable'),
        dict(tag='Numerical', q=r'The potential energy between two atoms is U(r) = a/r¹² − b/r⁶, with a, b &gt; 0. Find the equilibrium separation.',
             steps=[r'F = −dU/dr = 12a/r¹³ − 6b/r⁷.',
                    r'Equilibrium: 12a/r¹³ = 6b/r⁷, so r⁶ = 2a/b.',
                    r'r₀ = (2a/b)^(1/6). This is a minimum of U, so the bond is stable.'],
             answer=r'r₀ = (2a/b)^(1/6)'),
        dict(tag='Graph', q=r'In the figure, the particle has total energy E (dashed line). Where is it fastest, where does it turn back, and which way does the force push it just to the right of A?',
             steps=[r'K = E − U is largest where U is smallest, at A. So it is fastest at A.',
                    r'It turns back at the two points where the curve meets the energy line (E = U, K = 0).',
                    r'Just right of A the curve rises (positive slope), so F = −dU/dx is negative: the force points back toward A.'],
             answer=r'Fastest at A; turns at the two marked points; force points back toward A'),
    ],
    practice=[
        dict(q=r'A particle moves along x with U = (x² − 4x) J, x in metres. Its equilibrium position and type are',
             options=['x = 2 m, unstable', 'x = 4 m, stable', 'x = 2 m, stable', 'x = 0, neutral'], answer=2, type='numerical',
             explanation=r'dU/dx = 2x − 4 = 0 gives x = 2 m. d²U/dx² = 2 &gt; 0, so it is a minimum and stable. x = 0 and x = 4 m are where U = 0, but the force there is not zero.'),
        dict(q=r'The potential energy of a particle is U(r) = a/r² − b/r (a, b &gt; 0). The equilibrium distance is',
             options=['r = a/b, stable', 'r = 2a/b, stable', 'r = 2a/b, unstable', 'r = b/2a, stable'], answer=1, type='numerical',
             explanation=r'dU/dr = −2a/r³ + b/r² = 0 gives r = 2a/b. d²U/dr² = 6a/r⁴ − 2b/r³ = (6a − 2br)/r⁴ = 2a/r⁴ &gt; 0 there, so it is stable. r = a/b is where U = 0, not where F = 0.'),
        dict(q=r'<strong>Assertion (A):</strong> The work done by friction on a block taken around a closed path on a rough floor is not zero.<br><strong>Reason (R):</strong> Friction is a non-conservative force.',
             options=AR, answer=0, type='ar',
             explanation=r'Friction opposes motion at every point, so every part of the loop contributes negative work; the total is negative, not zero. That is exactly what it means to be non-conservative, so R explains A.'),
        dict(q=r'For a particle in one dimension, at a point where the potential-energy curve U(x) has a maximum,',
             options=['the force is maximum and the equilibrium is stable', 'the force is zero and the equilibrium is unstable', 'the force is zero and the equilibrium is stable', 'the kinetic energy is necessarily maximum'], answer=1, type='graph',
             explanation=r'At a maximum dU/dx = 0, so F = 0, and any displacement gives a force pushing the particle further away: unstable. Kinetic energy is smallest there, not largest, because K = E − U.'),
    ],
),

'work-conservation': dict(
    level='core',
    notes=[
        ('Setting up an energy equation', r'''<ol><li>Choose the system and the start and end states.</li>
<li>Write K + U for each state, using one fixed reference level for potential energy.</li>
<li>Add the work of all forces not written as potential energy (friction, applied pushes, air drag): K_i + U_i + W_nc = K_f + U_f.</li>
<li>Friction makes W_nc negative; a motor or a person pushing can make it positive.</li></ol>
<p>On any smooth track, the speed after falling through height h is √(2gh) whatever the shape of the track. The time taken does depend on the shape.</p>'''),
        ('Simple pendulum: speed and tension', r'''<p>A bob on a string of length L is released from rest at angle θ₀ from the vertical. It falls a height L(1 − cosθ₀) to the lowest point.</p>
<ul><li>Speed at the bottom: \(v=\sqrt{2gL(1-\cos\theta_0)}\).</li>
<li>Tension at the bottom: T − mg = mv²/L gives \(T=mg(3-2\cos\theta_0)\).</li>
<li>Released from the horizontal (θ₀ = 90°): v = √(2gL) and T = 3mg.</li></ul>'''),
        ('Hanging chains: work and centre of mass', r'''<p>For a uniform chain of mass M and length L with a fraction 1/n hanging over the edge of a smooth table, the hanging part has mass M/n and its centre of mass is L/(2n) below the table. Pulling it back on the table needs</p>
<p>\[W=\frac{M}{n}\,g\,\frac{L}{2n}=\frac{MgL}{2n^2}.\]</p>
<p>Use the centre of mass of each piece whenever an extended body changes height.</p>'''),
    ],
    formulas=[
        dict(title='Pendulum released from angle θ₀',
             formula=r'v_{\rm bottom}=\sqrt{2gL(1-\cos\theta_0)},\qquad T_{\rm bottom}=mg(3-2\cos\theta_0)',
             symbols='L string length (m); θ₀ release angle from the vertical; g = 10 m/s²; m bob mass (kg); v speed (m/s); T tension (N). Light string, no air resistance.'),
        dict(title='Pulling a hanging part of a chain onto a table',
             formula=r'W=\frac{MgL}{2n^2}',
             symbols='M total mass (kg); L total length (m); 1/n fraction hanging; W work (J) needed to pull it back slowly onto a smooth table.'),
    ],
    traps=[r'For an extended object, use the rise of its centre of mass, not the rise of its end or top.',
           r'"Mechanical energy is conserved" needs only that non-conservative forces do no work. A normal force that is always perpendicular to the motion does not spoil it.'],
    exam=r'''<ul><li>Ball thrown from a height with speed u: speed on hitting the ground is √(u² + 2gh) in every direction of throw.</li>
<li>Pendulum: speed and tension at the lowest point for a given release angle.</li>
<li>Work against air resistance from the observed final speed.</li>
<li>Chain hanging over a table: work to pull it up, or speed as it slides off.</li>
<li>Rough incline: speed at the bottom using K_i + U_i + W_friction = K_f + U_f.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A pendulum of length 2 m is released from rest at 60° to the vertical. Find the speed at the lowest point and the tension there in terms of mg.',
             steps=[r'Drop in height: L(1 − cos60°) = 2 × 0.5 = 1 m.',
                    r'v = √(2 × 10 × 1) = √20 ≈ 4.47 m/s.',
                    r'T = mg(3 − 2cos60°) = mg(3 − 1) = 2mg.'],
             answer=r'v ≈ 4.47 m/s, T = 2mg'),
        dict(tag='Numerical', q=r'A uniform chain of mass 4 kg and length 2 m lies on a smooth table with one third of its length hanging over the edge. Find the work needed to pull it slowly back onto the table.',
             steps=[r'Hanging mass = 4/3 kg; its centre is (2/3)/2 = 1/3 m below the table.',
                    r'W = (4/3) × 10 × (1/3) = 40/9 ≈ 4.44 J.',
                    r'Check with the formula: MgL/(2n²) = 4 × 10 × 2/(2 × 9) = 4.44 J.'],
             answer=r'≈ 4.44 J'),
        dict(tag='Numerical', q=r'A 2 kg block slides from rest down a 5 m long incline at 37° (sin 37° = 0.6). μₖ = 0.25. Find its speed at the bottom.',
             steps=[r'Height h = 5 × 0.6 = 3 m, so U_i = 2 × 10 × 3 = 60 J.',
                    r'Friction = μmg cos37° = 0.25 × 20 × 0.8 = 4 N; work = −4 × 5 = −20 J.',
                    r'K_f = 60 − 20 = 40 J = ½ × 2 × v², so v² = 40.',
                    r'v ≈ 6.32 m/s.'],
             answer=r'√40 ≈ 6.32 m/s'),
    ],
    practice=[
        dict(q=r'A 1 kg ball falls from rest from a height of 20 m and reaches the ground at 18 m/s (g = 10 m/s²). The work done by air resistance is',
             options=['−38 J', '−162 J', '+38 J', '−200 J'], answer=0, type='numerical',
             explanation=r'Initial energy mgh = 200 J. Final K = ½ × 1 × 18² = 162 J. Air resistance removed 200 − 162 = 38 J, so its work is −38 J. −162 J is the final kinetic energy, and +38 J has the wrong sign: drag opposes motion.'),
        dict(q=r'A uniform chain of mass M and length L lies on a smooth table with half its length hanging. The work needed to pull the hanging part back onto the table is',
             options=['MgL/2', 'MgL/4', 'MgL/16', 'MgL/8'], answer=3, type='numerical',
             explanation=r'Hanging mass M/2, centre of mass L/4 below the table: W = (M/2)g(L/4) = MgL/8. MgL/4 uses the bottom end’s depth for the mass M/2 (or the centre depth for mass M). MgL/16 squares the wrong factor.'),
        dict(q=r'Three identical balls are thrown from the top of a tower with the same speed: one upward, one downward, one horizontally. Ignoring air resistance, their speeds on reaching the ground are',
             options=['greatest for the one thrown downward', 'greatest for the one thrown upward', 'equal for all three', 'greatest for the one thrown horizontally'], answer=2, type='concept',
             explanation=r'Each starts with the same kinetic energy ½mu² and falls through the same height. Energy conservation gives v = √(u² + 2gh) for all three. They take different times to land, which is what tempts the other options.'),
        dict(q=r'A simple pendulum bob is released from rest with the string horizontal. The tension in the string at the lowest point is',
             options=['mg', '2mg', '3mg', '5mg'], answer=2, type='numerical',
             explanation=r'v² = 2gL at the bottom. T − mg = mv²/L = 2mg, so T = 3mg. mg ignores the centripetal requirement, and 2mg is only the centripetal part.'),
    ],
),

'work-power': dict(
    level='core',
    notes=[
        ('Constant force versus constant power', r'''<p><strong>Constant force from rest:</strong> a = F/m is constant, v = at, so P = Fv = (F²/m)t. Power grows linearly with time.</p>
<p><strong>Constant power from rest</strong> (e.g. an engine at full throttle, no losses):</p>
<ol><li>The work done equals the kinetic energy gained: Pt = ½mv², so \(v=\sqrt{2Pt/m}\propto t^{1/2}\).</li>
<li>Distance: \(x=\int v\,dt\propto t^{3/2}\).</li>
<li>Force F = P/v ∝ t^(−1/2), so the force falls as the body speeds up.</li></ol>'''),
        ('Pumps, cranes and vehicles', r'''<ul><li><strong>Lifting water:</strong> power = (mass per second) × g × h. If the water also leaves with speed v, add (mass per second) × ½v².</li>
<li><strong>Vehicle at constant speed on a level road:</strong> engine force = resistance f, so P = fv. The top speed with maximum power is v_max = P/f.</li>
<li><strong>Up an incline:</strong> P = (mg sinθ + f)v.</li>
<li><strong>Efficiency:</strong> input power = useful power/η. The difference becomes heat.</li></ul>
<p>Units: 1 W = 1 J/s; 1 horsepower (hp) = 746 W.</p>'''),
    ],
    formulas=[
        dict(title='Motion under constant power from rest',
             formula=r'v=\sqrt{\frac{2Pt}{m}}\propto t^{1/2},\qquad x\propto t^{3/2},\qquad F=\frac{P}{v}\propto t^{-1/2}',
             symbols='P constant power delivered to the body (W); m mass (kg); t time (s); v speed (m/s); x distance (m); F force (N). No losses, motion along a straight line.'),
        dict(title='Vehicle power',
             formula=r'P=(mg\sin\theta+f)\,v,\qquad v_{\max}=\frac{P}{f}\ \ (\text{level road})',
             symbols='m mass (kg); g = 10 m/s²; θ incline angle (0 on level ground); f resistive force (N); v constant speed (m/s); P engine power (W). 1 hp = 746 W.'),
    ],
    traps=[r'Under constant power the force is not constant. Using v = u + at with a fixed acceleration gives wrong answers.',
           r'Kilowatt-hour is a unit of energy, not power. 1 kWh = 3.6 × 10⁶ J.'],
    exam=r'''<ul><li>Pump lifting water to a tank: find power, then input power for a given efficiency.</li>
<li>Machine gun firing n bullets per minute: power = (n/60) × ½mv².</li>
<li>Body under constant power: how v or x depends on t.</li>
<li>Car on a level road or an incline: power at a speed, or maximum speed for a given power.</li>
<li>F = f(t) on a body from rest: instantaneous power at time t.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A pump lifts 600 kg of water per minute to a tank 20 m high. Find the useful power and the input power if the pump is 80% efficient.',
             steps=[r'Work per minute = mgh = 600 × 10 × 20 = 1.2 × 10⁵ J.',
                    r'Useful power = 1.2 × 10⁵/60 = 2000 W.',
                    r'Input power = 2000/0.8 = 2500 W = 2.5 kW.'],
             answer=r'2 kW useful; 2.5 kW input'),
        dict(tag='Ratio', q=r'A car starts from rest and its engine delivers constant power. Compare its speeds and distances at t = 1 s and t = 4 s.',
             steps=[r'v ∝ t^(1/2): v(4)/v(1) = √4 = 2.',
                    r'x ∝ t^(3/2): x(4)/x(1) = 4^(3/2) = 8.',
                    r'Under constant force instead, v would scale as t (4×) and x as t² (16×).'],
             answer=r'Speed doubles; distance becomes 8 times'),
        dict(tag='Numerical', q=r'A 1000 kg car climbs a slope with sinθ = 1/20 at a steady 20 m/s against a resistance of 500 N. Find the engine power.',
             steps=[r'Down-slope weight component: mg sinθ = 10000/20 = 500 N.',
                    r'At constant speed, engine force = 500 + 500 = 1000 N.',
                    r'P = Fv = 1000 × 20 = 20 000 W = 20 kW.'],
             answer=r'20 kW'),
    ],
    practice=[
        dict(q=r'A machine gun fires 360 bullets per minute. Each bullet has mass 20 g and leaves at 500 m/s. The power of the gun is',
             options=['15 kW', '2.5 kW', '150 kW', '7.5 kW'], answer=0, type='numerical',
             explanation=r'Energy per bullet = ½ × 0.02 × 500² = 2500 J. Six bullets per second, so P = 6 × 2500 = 15 000 W. 2.5 kW is the energy of one bullet per second, and 7.5 kW drops the factor of 2 the wrong way (uses ¼mv²).'),
        dict(q=r'A body starts from rest and moves in a straight line under a constant power source. Its displacement s varies with time t as',
             options=['s ∝ t', 's ∝ t²', 's ∝ t^(3/2)', 's ∝ t^(1/2)'], answer=2, type='concept',
             explanation=r'Pt = ½mv² gives v ∝ t^(1/2), and integrating gives s ∝ t^(3/2). s ∝ t² is the constant-force (constant acceleration) result, and t^(1/2) is how the speed varies.'),
        dict(q=r'A car’s engine delivers at most 30 kW. Total resistance is constant at 1500 N. Its maximum speed on a level road is',
             options=['5 m/s', '45 m/s', '50 m/s', '20 m/s'], answer=3, type='numerical',
             explanation=r'At top speed the engine force equals resistance, so P = fv and v = 30 000/1500 = 20 m/s. 45 and 50 come from multiplying or mixing up units, and 5 m/s inverts the ratio.'),
        dict(q=r'A force F = 2t N (t in seconds) acts on a 1 kg body initially at rest. The power delivered at t = 2 s is',
             options=['8 W', '16 W', '4 W', '32 W'], answer=1, type='numerical',
             explanation=r'a = 2t, so v = t² and v(2) = 4 m/s. F(2) = 4 N. P = Fv = 16 W. 8 W uses v = 2t (treating a as constant 2), and 4 W uses only the force.'),
    ],
),

'work-collisions': dict(
    level='exam',
    notes=[
        ('Types of collision: what is conserved', r'''<div class="table-wrap"><table>
<thead><tr><th>Type</th><th>Momentum</th><th>Kinetic energy</th><th>e</th><th>Example</th></tr></thead>
<tbody>
<tr><td>Elastic</td><td>Conserved</td><td>Conserved</td><td>1</td><td>Collisions of atoms, nearly for steel balls</td></tr>
<tr><td>Inelastic</td><td>Conserved</td><td>Partly lost</td><td>0 to 1</td><td>Most real collisions</td></tr>
<tr><td>Perfectly inelastic</td><td>Conserved</td><td>Maximum loss</td><td>0</td><td>Bodies stick: bullet in a block, mud on a wall</td></tr>
</tbody></table></div>
<p>Total energy is always conserved; "lost" kinetic energy becomes heat, sound and deformation. Momentum is conserved because the collision forces are internal and act for a very short time. External forces such as gravity or friction are finite, so their impulse during the short impact is negligible (the impulse approximation).</p>'''),
        ('Perfectly inelastic collisions and the ballistic pendulum', r'''<p>When the bodies stick, the common velocity follows from momentum alone, and the kinetic energy lost is</p>
<p>\[\Delta K=\frac12\,\frac{m_1m_2}{m_1+m_2}\,(u_1-u_2)^2.\]</p>
<p>With the target at rest, the fraction lost is m₂/(m₁ + m₂). Two equal masses lose half their kinetic energy. Not all kinetic energy can be lost: the centre of mass keeps moving, and its kinetic energy (P²/2M) must remain.</p>
<p><strong>Ballistic pendulum:</strong> a bullet m embeds in a hanging block M, and the pair rises a height h. Use momentum for the collision, then energy for the swing: \(v=\dfrac{m+M}{m}\sqrt{2gh}\). Do not use energy conservation across the collision itself.</p>
<p><strong>In two dimensions</strong>, add the momenta as vectors: the combined body moves along the direction of the total momentum.</p>'''),
        ('Explosions and recoil', r'''<p>An explosion is a collision run backward. A body at rest that splits into two pieces has zero total momentum, so the pieces move in opposite directions with m₁v₁ = m₂v₂. Their kinetic energies share as K₁/K₂ = m₂/m₁: the lighter piece carries more energy. A gun and its bullet are the standard example: the gun recoils slowly but the bullet gets almost all the kinetic energy.</p>'''),
    ],
    formulas=[
        dict(title='Kinetic energy lost when bodies stick',
             formula=r'\Delta K=\frac{m_1m_2\,(u_1-u_2)^2}{2(m_1+m_2)},\qquad \frac{\Delta K}{K_i}=\frac{m_2}{m_1+m_2}\ (u_2=0)',
             symbols='m₁, m₂ masses (kg); u₁, u₂ velocities before the collision (m/s); K_i initial kinetic energy (J); ΔK kinetic energy converted to other forms (J).'),
        dict(title='Ballistic pendulum',
             formula=r'v=\frac{m+M}{m}\sqrt{2gh}',
             symbols='m bullet mass and M block mass (kg); h height the block rises after the bullet embeds (m); v bullet speed (m/s); g = 10 m/s².'),
        dict(title='Body at rest splitting into two pieces',
             formula=r'm_1v_1=m_2v_2,\qquad \frac{K_1}{K_2}=\frac{m_2}{m_1}',
             symbols='m₁, m₂ masses of the pieces (kg); v₁, v₂ their speeds (m/s), in opposite directions; K₁, K₂ their kinetic energies (J).'),
    ],
    traps=[r'Energy is not conserved across a perfectly inelastic collision. In the ballistic pendulum, use momentum for the impact and energy only for the swing afterwards.',
           r'"Perfectly inelastic" does not mean all kinetic energy is lost. Only the part associated with relative motion is lost; the centre of mass keeps its kinetic energy.'],
    exam=r'''<ul><li>Bullet embeds in a block: common velocity, height risen, energy lost.</li>
<li>"Fraction of kinetic energy lost when a moving body sticks to an identical body at rest" (½).</li>
<li>Two bodies moving at right angles stick together: speed and direction of the combination.</li>
<li>A body at rest explodes into two pieces in a given mass ratio: ratio of speeds or kinetic energies.</li>
<li>Assertion–reason on whether momentum or kinetic energy is conserved in each type of collision.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A 10 g bullet embeds in a 990 g block hanging on a string. The block rises 20 cm. Find the bullet’s speed and the fraction of kinetic energy lost.',
             steps=[r'Swing after impact: V = √(2gh) = √(2 × 10 × 0.2) = 2 m/s.',
                    r'Momentum in the impact: 0.01v = 1.0 × 2, so v = 200 m/s.',
                    r'Fraction of KE lost = M/(m + M) = 990/1000 = 0.99, i.e. 99%.'],
             answer=r'200 m/s; 99% of the kinetic energy is lost'),
        dict(tag='Numerical', q=r'A 2 kg ball moving east at 3 m/s collides with a 1 kg ball moving north at 6 m/s, and they stick. Find the velocity of the combination and the kinetic energy lost.',
             steps=[r'Momentum: east 2 × 3 = 6 kg m/s; north 1 × 6 = 6 kg m/s.',
                    r'Velocity components: 6/3 = 2 m/s east and 2 m/s north. Speed = 2√2 ≈ 2.83 m/s at 45° north of east.',
                    r'K before = ½ × 2 × 9 + ½ × 1 × 36 = 9 + 18 = 27 J. K after = ½ × 3 × 8 = 12 J.',
                    r'Kinetic energy lost = 15 J.'],
             answer=r'2√2 m/s at 45° north of east; 15 J lost'),
        dict(tag='Ratio', q=r'A 3 kg body at rest explodes into pieces of 1 kg and 2 kg. The 1 kg piece moves at 8 m/s. Find the speed of the other piece and the ratio of their kinetic energies.',
             steps=[r'Total momentum stays zero: 1 × 8 = 2 × v, so v = 4 m/s in the opposite direction.',
                    r'K₁ = ½ × 1 × 64 = 32 J; K₂ = ½ × 2 × 16 = 16 J.',
                    r'K₁ : K₂ = 2 : 1 = m₂ : m₁, as expected.'],
             answer=r'4 m/s opposite; K₁ : K₂ = 2 : 1'),
    ],
    practice=[
        dict(q=r'A ball moving with speed u hits an identical ball at rest and sticks to it. The fraction of kinetic energy lost is',
             options=['1/4', '1/2', '3/4', 'zero'], answer=1, type='numerical',
             explanation=r'Common velocity u/2. Final K = ½(2m)(u/2)² = ¼mu², half of the initial ½mu². The fraction lost is m₂/(m₁ + m₂) = 1/2. Zero would be an elastic collision, and 3/4 assumes the speed falls to u/4.'),
        dict(q=r'A 20 g bullet embeds in a 980 g block hanging as a pendulum, which then rises 5 cm (g = 10 m/s²). The speed of the bullet was',
             options=['1 m/s', '49 m/s', '100 m/s', '50 m/s'], answer=3, type='numerical',
             explanation=r'After impact V = √(2 × 10 × 0.05) = 1 m/s. Momentum: 0.02v = 1.0 × 1, so v = 50 m/s. 1 m/s is the block’s speed, and 49 m/s uses only the block mass 0.98 kg instead of the combined 1.0 kg.'),
        dict(q=r'A bomb at rest explodes into two pieces whose masses are in the ratio 1 : 3. The ratio of their kinetic energies (lighter : heavier) is',
             options=['1 : 3', '3 : 1', '1 : 9', '9 : 1'], answer=1, type='numerical',
             explanation=r'Equal and opposite momenta p. K = p²/2m, so K ∝ 1/m and the lighter piece has 3 times the energy. 1 : 3 inverts the ratio. 9 : 1 is the ratio of the squares of their speeds.'),
        dict(q=r'<strong>Assertion (A):</strong> In a perfectly inelastic collision, all the initial kinetic energy is converted into other forms.<br><strong>Reason (R):</strong> Linear momentum is conserved in a perfectly inelastic collision.',
             options=AR, answer=3, type='ar',
             explanation=r'R is true. Because momentum is conserved, the combined body must keep moving if the total momentum is not zero, so some kinetic energy remains. A is false, except in the special case of zero total momentum.'),
    ],
),

'work-vertical-loop': dict(
    level='exam',
    notes=[
        ('Derivation: tension at any point and the minimum speeds', r'''<ol><li>Let the bob have speed u at the bottom and be at angle θ measured from the lowest point. It has risen r(1 − cosθ), so \(v^2=u^2-2gr(1-\cos\theta)\).</li>
<li>Radial equation (toward the centre): T − mg cosθ = mv²/r.</li>
<li>Combine: \(T=\dfrac{mu^2}{r}+mg(3\cos\theta-2)\).</li>
<li>At the top (θ = 180°): T_top = mu²/r − 5mg. The string stays taut if T_top ≥ 0, so u² ≥ 5gr and v_top² ≥ gr.</li>
<li>T_bottom − T_top = (mu²/r + mg) − (mu²/r − 5mg) = 6mg, for any u that completes the circle.</li></ol>
<p>In the limiting case (u = √(5gr)): bottom T = 6mg; side (θ = 90°) v = √(3gr), T = 3mg; top v = √(gr), T = 0. The kinetic energy at the bottom is 5 times that at the top.</p>'''),
        ('What happens for smaller launch speeds', r'''<ul><li>u ≤ √(2gr): the bob does not rise above the centre level. It swings back and forth like a pendulum; the string stays taut.</li>
<li>√(2gr) &lt; u &lt; √(5gr): the bob rises above the centre, but the tension becomes zero somewhere in the upper half. The string slackens and the bob follows a parabola.</li>
<li>u ≥ √(5gr): complete circles.</li></ul>'''),
        ('Rod, track and sphere variations', r'''<ul><li><strong>Light rigid rod</strong> (or a bead on a ring): the rod can push, so the bob only needs to reach the top with speed ≥ 0. Minimum bottom speed is √(4gr) = 2√(gr).</li>
<li><strong>Block released on a smooth loop-the-loop track:</strong> it needs v_bottom² ≥ 5gR, so the release height must be at least 5R/2.</li>
<li><strong>Body sliding off the top of a smooth sphere</strong> (from rest at the top): it leaves the surface when cosθ = 2/3, i.e. at a height 2R/3 above the centre (R/3 below the top).</li></ul>'''),
    ],
    formulas=[
        dict(title='Tension at angle θ from the lowest point',
             formula=r'T=\frac{mu^2}{r}+mg(3\cos\theta-2),\qquad T_{\rm bottom}-T_{\rm top}=6mg',
             symbols='m mass (kg); u speed at the lowest point (m/s); r radius (m); θ angle from the lowest point; g = 10 m/s²; T tension (N). Light string, no losses.'),
        dict(title='Minimum conditions in other set-ups',
             formula=r'u_{\rm rod}=\sqrt{4gr},\qquad h_{\rm loop}=\tfrac52R,\qquad \cos\theta_{\rm leave}=\tfrac23\ (\text{sphere})',
             symbols='u_rod minimum bottom speed for a light rigid rod (m/s); h_loop minimum release height above the bottom of a smooth loop of radius R (m); θ_leave angle from the vertical at which a body starting at rest on top of a smooth sphere leaves it.'),
    ],
    figure=dict(svg=FIG_LOOP, caption='Limiting complete vertical circle on a light string. Speed squared falls by 2gr from bottom to top; tension falls from 6mg to zero.'),
    traps=[r'At the top, the minimum speed is √(gr), not zero. Zero is the rod (or bead) answer.',
           r'Release height for a loop-the-loop is 5R/2 above the lowest point, not 2R. Reaching the top needs speed as well as height.'],
    exam=r'''<ul><li>"Minimum speed at the lowest point to complete the circle" for a string (√(5gr)) or a rod (√(4gr)).</li>
<li>Ratio of maximum to minimum tension, or T_bottom − T_top = 6mg.</li>
<li>Ratio of kinetic energies at the bottom and top in the limiting case (5 : 1).</li>
<li>Minimum release height on a loop-the-loop track (5R/2).</li>
<li>Body sliding from the top of a smooth hemisphere: height at which it leaves.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A 0.5 kg stone on a 1 m string is whirled in a vertical circle. Find the minimum speed at the bottom and the tension there in that case.',
             steps=[r'u_min = √(5gr) = √50 ≈ 7.07 m/s.',
                    r'At the bottom, T − mg = mu²/r = 0.5 × 50/1 = 25 N.',
                    r'T = 25 + 5 = 30 N = 6mg.'],
             answer=r'≈ 7.07 m/s; T = 30 N'),
        dict(tag='Ratio', q=r'In the limiting complete circle on a string, find the ratio of kinetic energy at the lowest point to that at the highest point.',
             steps=[r'Bottom: v² = 5gr. Top: v² = gr.',
                    r'K ∝ v², so K_bottom : K_top = 5gr : gr.'],
             answer=r'5 : 1'),
        dict(tag='Numerical', q=r'A small block starts from rest at the top of a smooth fixed hemisphere of radius 0.9 m. At what height above the centre does it leave the surface, and with what speed?',
             steps=[r'At angle θ from the vertical: v² = 2gR(1 − cosθ). Radial: mg cosθ − N = mv²/R.',
                    r'It leaves when N = 0: g cosθ = 2g(1 − cosθ), so cosθ = 2/3.',
                    r'Height above centre = R cosθ = 0.6 m (0.3 m below the top).',
                    r'v² = 2 × 10 × 0.3 = 6, so v = √6 ≈ 2.45 m/s.'],
             answer=r'0.6 m above the centre; √6 ≈ 2.45 m/s'),
        dict(tag='Numerical', q=r'A block slides from rest down a smooth track that ends in a vertical loop of radius 2 m. Find the minimum release height above the bottom of the loop.',
             steps=[r'To stay on the track at the top, v_top² ≥ gR, so v_bottom² ≥ 5gR.',
                    r'Energy from release: 2gh = v_bottom² ≥ 5gR.',
                    r'h ≥ 5R/2 = 5 m.'],
             answer=r'5 m'),
    ],
    practice=[
        dict(q=r'A small block is released on a smooth loop-the-loop track of radius 0.4 m. The least height above the lowest point of the loop from which it must start to go round the loop is',
             options=['0.8 m', '1.0 m', '2.0 m', '0.4 m'], answer=1, type='numerical',
             explanation=r'h_min = 5R/2 = 1.0 m. 0.8 m (= 2R) only lifts the block to the top level with zero speed, so it would fall off before the top. 2.0 m is more than needed.'),
        dict(q=r'A bob on a light string of length r is given a speed √(3gr) at the lowest point. It will',
             options=['complete the vertical circle', 'oscillate without rising above the centre level', 'rise above the centre level, then the string slackens', 'stop exactly at the top'], answer=2, type='concept',
             explanation=r'√(2gr) &lt; √(3gr) &lt; √(5gr), so the bob goes above the centre level but the tension reaches zero before the top. The string slackens and the bob leaves the circle. Completing needs √(5gr); staying below the centre needs at most √(2gr).'),
        dict(q=r'A bob on a string is given speed √(6gr) at the bottom of a vertical circle. The ratio of the maximum to minimum tension is',
             options=['6', '5', '3', '7'], answer=3, type='numerical',
             explanation=r'Bottom: T = m(6g) + mg = 7mg. Top: v² = 6gr − 4gr = 2gr, so T = 2mg − mg = mg. Ratio = 7. The answer 6 confuses the ratio with the difference T_bottom − T_top = 6mg.'),
        dict(q=r'A bob is attached to a light rigid rod of length 0.9 m pivoted at one end. The minimum speed at the lowest point for it to complete a vertical circle is (g = 10 m/s²)',
             options=['6 m/s', '√45 m/s', '3 m/s', '√18 m/s'], answer=0, type='numerical',
             explanation=r'A rod can push, so the bob may reach the top with zero speed: u² = 4gr = 36, u = 6 m/s. √45 m/s is the string answer √(5gr). 3 m/s is √(gr), the string’s minimum top speed.'),
    ],
),


'work-elastic-results': dict(
    level='exam',
    notes=[
        ('Derivation: final velocities in a 1-D elastic collision', r'''<ol><li>Momentum: m₁(u₁ − v₁) = m₂(v₂ − u₂).</li>
<li>Kinetic energy: m₁(u₁² − v₁²) = m₂(v₂² − u₂²), i.e. m₁(u₁ − v₁)(u₁ + v₁) = m₂(v₂ − u₂)(v₂ + u₂).</li>
<li>Divide the second by the first: u₁ + v₁ = v₂ + u₂, so v₂ − v₁ = u₁ − u₂. The relative velocity just reverses (e = 1).</li>
<li>Solve the two linear equations to get the boxed results in the formula card above.</li></ol>
<p>Shortcut in practice: write momentum conservation and "separation speed = approach speed". Two linear equations are easier than squaring.</p>'''),
        ('Special cases with the target at rest (u₂ = 0)', r'''<div class="table-wrap"><table>
<thead><tr><th>Case</th><th>v₁</th><th>v₂</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td>m₁ = m₂</td><td>0</td><td>u₁</td><td>Velocities exchange</td></tr>
<tr><td>m₁ ≫ m₂</td><td>≈ u₁</td><td>≈ 2u₁</td><td>Heavy body barely slows; light one flies off at twice its speed</td></tr>
<tr><td>m₁ ≪ m₂</td><td>≈ −u₁</td><td>≈ 0</td><td>Light body bounces back, like a ball off a wall</td></tr>
</tbody></table></div>
<p>Fraction of kinetic energy transferred to the target: \(\dfrac{4m_1m_2}{(m_1+m_2)^2}\). It is 100% only for equal masses. This is why materials rich in light nuclei (water, heavy water, graphite) are used to slow neutrons in reactors.</p>
<p><strong>Moving wall:</strong> a ball hitting a massive wall that approaches at speed V rebounds with speed u + 2V (relative velocity reverses in the wall’s frame).</p>'''),
    ],
    formulas=[
        dict(title='Energy transferred to a target at rest (elastic)',
             formula=r'\frac{K_2}{K_1}=\frac{4m_1m_2}{(m_1+m_2)^2},\qquad \frac{K_1^{\prime}}{K_1}=\left(\frac{m_1-m_2}{m_1+m_2}\right)^2',
             symbols='m₁ moving body and m₂ target (kg); K₁ initial kinetic energy of m₁ (J); K₂ energy given to the target and K₁′ energy kept by m₁ (J). Head-on elastic collision with u₂ = 0.'),
        dict(title='Relative velocity reverses',
             formula=r'v_2-v_1=-(u_2-u_1)',
             symbols='u, v signed velocities before and after (m/s). Valid for every head-on elastic collision; together with momentum conservation it fixes both final velocities.'),
    ],
    traps=[r'During an elastic collision the kinetic energy dips while the bodies are compressed. It is equal before and after the impact, not at every instant.',
           r'Keep signs. When the bodies approach each other, one initial velocity is negative; using speeds without signs gives wrong final velocities.'],
    exam=r'''<ul><li>"A body of mass m moving with u collides elastically with a stationary body of mass nm. Find the velocities or the fraction of KE transferred."</li>
<li>Neutron moderator questions: fraction of energy kept by a neutron after hitting a nucleus of mass number A.</li>
<li>Matching the special cases (equal masses, heavy on light, light on heavy).</li>
<li>Head-on collision of two bodies moving toward each other: final velocities with signs.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A 2 kg ball moving at 6 m/s collides head-on and elastically with a 1 kg ball at rest. Find both final velocities.',
             steps=[r'v₁ = (2 − 1)/(2 + 1) × 6 = 2 m/s.',
                    r'v₂ = 2 × 2/(2 + 1) × 6 = 8 m/s.',
                    r'Check momentum: 12 = 2 × 2 + 1 × 8. Check energy: 36 J = 4 J + 32 J.'],
             answer=r'2 m/s and 8 m/s, both forward'),
        dict(tag='Ratio', q=r'A neutron (mass 1 u) hits a stationary carbon-12 nucleus head-on and elastically. What fraction of its kinetic energy does it lose?',
             steps=[r'Fraction transferred = 4m₁m₂/(m₁ + m₂)² = 4 × 1 × 12/13² = 48/169.',
                    r'48/169 ≈ 0.28, so about 28% is lost.',
                    r'Fraction kept = ((1 − 12)/13)² = 121/169 ≈ 0.72. The two add to 1.'],
             answer=r'48/169 ≈ 28%'),
        dict(tag='Numerical', q=r'A 1 kg ball moving at +4 m/s collides head-on and elastically with a 3 kg ball moving at −2 m/s. Find the final velocities.',
             steps=[r'v₁ = [(1 − 3)(4) + 2 × 3 × (−2)]/4 = (−8 − 12)/4 = −5 m/s.',
                    r'v₂ = [(3 − 1)(−2) + 2 × 1 × 4]/4 = (−4 + 8)/4 = +1 m/s.',
                    r'Check: momentum 4 − 6 = −2 before and −5 + 3 = −2 after. Separation 1 − (−5) = 6 = approach 4 − (−2).',
                    r'Energy: 8 + 6 = 14 J before; 12.5 + 1.5 = 14 J after.'],
             answer=r'v₁ = −5 m/s (rebounds), v₂ = +1 m/s'),
    ],
    practice=[
        dict(q=r'A body of mass m moving at u collides head-on and elastically with a stationary body of mass 2m. The fraction of kinetic energy transferred to the second body is',
             options=['1/9', '2/3', '8/9', '1/3'], answer=2, type='numerical',
             explanation=r'4m₁m₂/(m₁ + m₂)² = 4 × 2/9 = 8/9. The first body rebounds at −u/3 and keeps 1/9 of its energy, which is the tempting distractor. 2/3 is the mass ratio, not an energy fraction.'),
        dict(q=r'<strong>Assertion (A):</strong> In an elastic collision, the kinetic energy of the system is the same at every instant during the collision.<br><strong>Reason (R):</strong> Total momentum of the system is conserved throughout the collision.',
             options=AR, answer=3, type='ar',
             explanation=r'A is false: while the bodies are squeezed, part of the kinetic energy is stored as elastic energy and returned later. R is true because only internal forces act during the impact.'),
        dict(q=r'Match the head-on collision (target initially at rest) with the result.<br>(P) Equal masses, elastic (Q) Very heavy body hits a light one, elastic (R) Light body hits a very heavy one, elastic (S) Equal masses stick together<br>(1) Light body moves at about 2u (2) Velocities exchange (3) Light body rebounds at about u (4) Common velocity u/2',
             options=['P-2, Q-1, R-3, S-4', 'P-2, Q-3, R-1, S-4', 'P-4, Q-1, R-3, S-2', 'P-1, Q-2, R-3, S-4'], answer=0, type='match',
             explanation=r'Equal masses exchange velocities (P-2). A heavy projectile gives the light target about 2u (Q-1). A light projectile bounces back from a heavy target at about u (R-3). Sticking equal masses share momentum: u/2 (S-4). Option 2 swaps Q and R.'),
        dict(q=r'A ball moving at 10 m/s hits a massive wall head-on and elastically. The wall is moving toward the ball at 2 m/s. The ball’s rebound speed is',
             options=['10 m/s', '12 m/s', '14 m/s', '8 m/s'], answer=2, type='numerical',
             explanation=r'In the wall’s frame the ball approaches at 12 m/s and leaves at 12 m/s. Adding the wall’s 2 m/s back gives 14 m/s (u + 2V). 12 m/s forgets to convert back to the ground frame, and 10 m/s treats the wall as stationary.'),
    ],
),
}


NEW_SECTIONS = [
dict(chapter='work', after='work-potential', id='work-spring',
     title='Spring force, spring energy and spring combinations',
     intro=r'An ideal spring pulls back with a force proportional to its extension or compression: F = −kx. Because the force changes with x, the work it does must be found from the area under the F–x graph, which is a triangle.',
     reasoning=r'Stretching from x₁ to x₂ against the spring needs work ½k(x₂² − x₁²), and the spring itself does the negative of that. The stored energy is ½kx². When a moving block hits a spring, its kinetic energy is stored as spring energy at maximum compression.',
     formula=r'F=-kx,\qquad W_{\rm spring}=-\tfrac12k\left(x_2^2-x_1^2\right),\qquad U=\tfrac12kx^2=\frac{F^2}{2k}',
     symbols='k spring constant (N/m); x extension or compression from natural length (m); x₁, x₂ initial and final deformations (m); W_spring work done by the spring (J); U stored energy (J); F spring force magnitude (N). Ideal massless spring obeying Hooke’s law.',
     trap=r'Work to stretch from x₁ to x₂ is ½k(x₂² − x₁²), not ½k(x₂ − x₁)². The spring is already resisting at x₁, so the second centimetre costs more than the first.',
     example=r'A spring with k = 800 N/m is stretched from 5 cm to 15 cm. How much work is needed?',
     solution=r'W = ½ × 800 × (0.15² − 0.05²) = 400 × (0.0225 − 0.0025) = 400 × 0.02 = 8 J. Using ½k(0.10)² would give only 4 J.',
     question=r'A 1 kg block moving at 2 m/s on a smooth floor hits a spring with k = 100 N/m. The maximum compression is',
     options='0.1 m|0.2 m|0.4 m|0.02 m', answer=1,
     explanation=r'½mv² = ½kx² gives x = v√(m/k) = 2 × √(1/100) = 0.2 m. 0.4 m forgets the square root; 0.02 m divides by k without the root.',
     deep=dict(
        level='core',
        notes=[
            ('Derivation: spring work from the F–x graph', r'''<ol><li>To stretch the spring slowly, you apply F_ext = +kx (equal and opposite to the spring force).</li>
<li>Work by you from 0 to x: \(\int_0^x kx\,dx=\tfrac12kx^2\). This is the triangle under the F–x line (base x, height kx).</li>
<li>From x₁ to x₂: \(\tfrac12k(x_2^2-x_1^2)\), the area of a trapezium.</li>
<li>The spring force is the opposite, so its work is \(-\tfrac12k(x_2^2-x_1^2)\). Moving back toward natural length, the spring does positive work.</li></ol>
<p>Since U = ½kx² and F = kx, the stored energy can also be written U = F²/(2k) = ½Fx. These forms are handy when the force, not the extension, is given.</p>'''),
            ('Block meets spring, with and without friction', r'''<ul><li><strong>Smooth floor:</strong> ½mv² = ½kx_max², so x_max = v√(m/k).</li>
<li><strong>Rough floor:</strong> friction acts during compression: ½mv² = ½kx² + μmgx. Solve this quadratic for x.</li>
<li><strong>Dropped from height h onto a vertical spring:</strong> the block falls a total h + x, so mg(h + x) = ½kx².</li>
<li><strong>Two blocks joined by a spring</strong> on a smooth floor: at maximum compression they move with the same velocity. Use momentum for that velocity and the kinetic energy difference for ½kx².</li></ul>'''),
            ('Cutting and combining springs', r'''<ul><li><strong>Cutting:</strong> k is inversely proportional to the natural length (kL = constant). Cut into n equal parts, each has spring constant nk. Cut in the ratio of lengths L₁ : L₂, the parts have k₁ = k(L/L₁) and k₂ = k(L/L₂).</li>
<li><strong>Series</strong> (end to end): same force in each, extensions add. \(\dfrac{1}{k_s}=\dfrac{1}{k_1}+\dfrac{1}{k_2}\).</li>
<li><strong>Parallel</strong> (side by side, same extension): forces add. \(k_p=k_1+k_2\).</li>
<li><strong>Energy sharing:</strong> in series (same F), U = F²/2k, so the softer spring stores more. In parallel (same x), U = ½kx², so the stiffer spring stores more.</li></ul>'''),
        ],
        formulas=[
            dict(title='Combining and cutting springs',
                 formula=r'\frac1{k_s}=\frac1{k_1}+\frac1{k_2},\qquad k_p=k_1+k_2,\qquad kL=\text{constant}',
                 symbols='k₁, k₂ individual spring constants (N/m); k_s series and k_p parallel equivalents (N/m); L natural length (m). Ideal massless springs.'),
            dict(title='Block hitting a spring',
                 formula=r'x_{\max}=v\sqrt{\frac mk}\ \ (\text{smooth}),\qquad \tfrac12mv^2=\tfrac12kx^2+\mu mgx\ \ (\text{rough})',
                 symbols='m block mass (kg); v speed when it touches the spring (m/s); k spring constant (N/m); x compression (m); μ kinetic friction coefficient; g = 10 m/s².'),
        ],
        figure=dict(svg=FIG_SPRING, caption='A block compressing a spring (left). The spring force grows linearly with compression (right), so the work stored is the triangle ½kx², not kx × x.'),
        traps=[r'Cutting a spring in half doubles its spring constant; it does not halve it. Shorter springs are stiffer.',
               r'For springs in series with the same force, the softer spring stores more energy. Students often assume the stiffer spring always stores more.'],
        exam=r'''<ul><li>"Work done to stretch a spring from x to 2x" (3 times the work from 0 to x).</li>
<li>Block on a smooth or rough floor hitting a spring: maximum compression.</li>
<li>Spring cut into pieces, or pieces combined in series and parallel: new k.</li>
<li>Ratio of energies in two springs stretched by the same force, or by the same extension.</li>
<li>F–x graph of a spring: find k from the slope and energy from the triangle.</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'A 2 kg block moving at 4 m/s on a rough floor (μₖ = 0.5) hits a spring with k = 700 N/m. Find the maximum compression.',
                 steps=[r'Initial kinetic energy = ½ × 2 × 16 = 16 J. Friction = 0.5 × 20 = 10 N.',
                        r'Energy: 16 = ½ × 700 × x² + 10x, so 350x² + 10x − 16 = 0.',
                        r'x = [−10 + √(100 + 22 400)]/700 = (−10 + 150)/700 = 0.2 m.',
                        r'Check: spring energy 14 J + friction work 2 J = 16 J.'],
                 answer=r'0.2 m'),
            dict(tag='Ratio', q=r'A spring with k = 120 N/m is cut into three pieces whose lengths are in the ratio 1 : 2 : 3. Find their spring constants.',
                 steps=[r'kL is constant. The pieces have lengths L/6, 2L/6 and 3L/6.',
                        r'k₁ = 120 × 6 = 720 N/m; k₂ = 120 × 3 = 360 N/m; k₃ = 120 × 2 = 240 N/m.',
                        r'Check: in series, 1/720 + 1/360 + 1/240 = 6/720 = 1/120. They rebuild the original spring.'],
                 answer=r'720, 360 and 240 N/m'),
            dict(tag='Ratio', q=r'Spring A has twice the spring constant of spring B. Find U_A : U_B when they are stretched (a) by the same force, (b) by the same extension.',
                 steps=[r'(a) Same force: U = F²/2k ∝ 1/k. U_A : U_B = k_B : k_A = 1 : 2.',
                        r'(b) Same extension: U = ½kx² ∝ k. U_A : U_B = 2 : 1.'],
                 answer=r'(a) 1 : 2 (b) 2 : 1'),
        ],
        practice=[
            dict(q=r'Stretching a spring from its natural length by x stores energy U. The extra work needed to stretch it further from x to 2x is',
                 options=['U', '2U', '3U', '4U'], answer=2, type='numerical',
                 explanation=r'At 2x the energy is ½k(2x)² = 4U. The extra work is 4U − U = 3U. 4U is the total from zero, and U treats the second stretch as costing the same as the first.'),
            dict(q=r'Springs of 200 N/m and 300 N/m are joined end to end. The equivalent spring constant is',
                 options=['500 N/m', '250 N/m', '60 N/m', '120 N/m'], answer=3, type='numerical',
                 explanation=r'Series: 1/k = 1/200 + 1/300 = 5/600, so k = 120 N/m. 500 N/m is the parallel result. A series combination is always softer than the softest spring.'),
            dict(q=r'A spring of spring constant k is cut into two equal halves, and the halves are then connected in parallel. The new spring constant is',
                 options=['k', '2k', '4k', 'k/2'], answer=2, type='numerical',
                 explanation=r'Each half has 2k (half the length). In parallel the constants add: 2k + 2k = 4k. k/2 wrongly assumes cutting softens the spring.'),
            dict(q=r'The spring force against extension for a spring is a straight line through the origin, reading 20 N at 0.1 m. The energy stored at 0.1 m is',
                 options=['1 J', '2 J', '20 J', '0.5 J'], answer=0, type='graph',
                 explanation=r'Energy is the triangle under the line: ½ × 0.1 × 20 = 1 J. (k = 200 N/m and ½kx² = 1 J.) 2 J uses force × extension without the ½. 20 J ignores the extension.'),
            dict(q=r'A 1 kg block is dropped from 0.4 m above the top of a vertical spring (k = 1000 N/m). The maximum compression is (g = 10 m/s²)',
                 options=['0.04 m', '0.1 m', '0.09 m', '0.2 m'], answer=1, type='numerical',
                 explanation=r'The block falls 0.4 + x in total: 10(0.4 + x) = 500x². So 500x² − 10x − 4 = 0, giving x = 0.1 m. 0.09 m ignores the extra fall through x (½kx² = mgh), and 0.04 m wrongly uses x = mgh/k-type scaling.'),
        ],
     )),

dict(chapter='work', after='work-collisions', id='work-restitution',
     title='Coefficient of restitution, bouncing and oblique collisions',
     intro=r'Real collisions lie between perfectly elastic and perfectly inelastic. The coefficient of restitution e measures how "bouncy" a collision is: it compares how fast the bodies separate with how fast they approached, along the line joining them at impact.',
     reasoning=r'e = 1 for an elastic collision, e = 0 when the bodies stick, and 0 &lt; e &lt; 1 otherwise. A ball dropped on a hard floor leaves with e times its arrival speed, so it rises to e² times its previous height. In an oblique collision, only the velocity components along the line of impact change.',
     formula=r'e=\frac{v_2-v_1}{u_1-u_2},\qquad h_n=e^{2n}h,\qquad v_n=e^n\sqrt{2gh}',
     symbols='e coefficient of restitution (no unit, 0 to 1); u₁, u₂ velocities before and v₁, v₂ after, along the line of impact (m/s); h drop height (m); hₙ height after the nth bounce (m); vₙ rebound speed after the nth bounce (m/s). Floor fixed, no air resistance.',
     trap=r'e applies to the components along the line of impact (the normal). In an oblique impact with a smooth surface, the component along the surface does not change.',
     example=r'A ball is dropped from 10 m onto a floor with e = 0.5. How high does it rise after the first bounce?',
     solution=r'It arrives at √(2 × 10 × 10) = √200 m/s and leaves at 0.5√200 m/s. The height is e²h = 0.25 × 10 = 2.5 m.',
     question=r'A ball dropped from 16 m bounces on a floor with e = 0.5. The height it reaches after the second bounce is',
     options='4 m|1 m|2 m|0.5 m', answer=1,
     explanation=r'hₙ = e²ⁿh = 0.5⁴ × 16 = 1 m. 4 m is the height after the first bounce, and 2 m wrongly uses eⁿ instead of e²ⁿ.',
     deep=dict(
        level='exam',
        notes=[
            ('General 1-D collision with restitution', r'''<p>Momentum conservation plus the definition of e give, for a head-on collision,</p>
<p>\[v_1=\frac{(m_1-em_2)u_1+(1+e)m_2u_2}{m_1+m_2},\qquad v_2=\frac{(m_2-em_1)u_2+(1+e)m_1u_1}{m_1+m_2}\]</p>
<p>Putting e = 1 recovers the elastic formulas; e = 0 gives the common velocity. The kinetic energy lost is</p>
<p>\[\Delta K=\frac12\,\frac{m_1m_2}{m_1+m_2}\,(1-e^2)(u_1-u_2)^2.\]</p>
<p>For equal masses with one at rest: v₁ = u(1 − e)/2 and v₂ = u(1 + e)/2.</p>'''),
            ('Bouncing ball: heights, total distance and total time', r'''<ul><li>Each bounce multiplies the speed by e, so the height is multiplied by e²: h₁ = e²h, h₂ = e⁴h, hₙ = e²ⁿh.</li>
<li>e can be measured from two heights: e = √(h₁/h).</li>
<li>Fraction of kinetic energy lost in each bounce = 1 − e².</li>
<li>Total distance before it stops: h + 2(e²h + e⁴h + …) = \(h\dfrac{1+e^2}{1-e^2}\).</li>
<li>Total time: with t₀ = √(2h/g), each bounce takes 2eⁿt₀, so T = \(t_0\dfrac{1+e}{1-e}\).</li></ul>'''),
            ('Oblique collisions', r'''<p><strong>Ball hitting a smooth fixed wall or floor:</strong> resolve the velocity into a normal part and a tangential part. The tangential part is unchanged (no friction). The normal part reverses and is multiplied by e. If the ball arrives at angle θ to the normal, it leaves at θ′ with tanθ′ = tanθ/e. For e &lt; 1 the rebound is flatter (θ′ &gt; θ).</p>
<p><strong>Two equal smooth spheres, one at rest, elastic oblique collision:</strong> after the collision they move at right angles to each other (θ₁ + θ₂ = 90°). This follows from momentum (a vector triangle) and energy (Pythagoras) together.</p>'''),
        ],
        formulas=[
            dict(title='Bouncing ball totals',
                 formula=r'H_{\rm total}=h\,\frac{1+e^2}{1-e^2},\qquad T_{\rm total}=\sqrt{\frac{2h}{g}}\;\frac{1+e}{1-e}',
                 symbols='h initial drop height (m); e coefficient of restitution with the floor; g = 10 m/s²; H_total total distance travelled (m); T_total total time until it stops (s). No air resistance.'),
            dict(title='Kinetic energy lost in a 1-D collision',
                 formula=r'\Delta K=\frac{m_1m_2}{2(m_1+m_2)}\,(1-e^2)\,(u_1-u_2)^2',
                 symbols='m₁, m₂ masses (kg); u₁, u₂ approach velocities (m/s); e coefficient of restitution; ΔK kinetic energy converted to heat, sound and deformation (J).'),
            dict(title='Oblique impact on a smooth wall',
                 formula=r"v_t'=v_t,\quad v_n'=e\,v_n,\quad \tan\theta'=\frac{\tan\theta}{e}",
                 symbols='v_t, v_n tangential and normal velocity components before impact (m/s); primes mean after impact; θ, θ′ angles of incidence and rebound measured from the normal.'),
        ],
        figure=dict(svg=FIG_BOUNCE, caption='A ball dropped from height h. Each bounce multiplies the rebound speed by e, so the heights fall as h, e²h, e⁴h, … and each flight time shrinks by the factor e.'),
        traps=[r'Height ratio is e², not e. If a ball rises to one quarter of its drop height, e = 1/2.',
               r'The fraction of kinetic energy lost per bounce is 1 − e², not 1 − e.'],
        exam=r'''<ul><li>"A ball dropped from h rebounds to h′. Find e" (e = √(h′/h)), or the height after n bounces.</li>
<li>Total distance or total time before the ball stops.</li>
<li>Percentage of kinetic energy lost in a bounce.</li>
<li>Two bodies with a given e: final velocities and energy loss.</li>
<li>Ball striking a smooth floor at an angle: speed and angle after impact.</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'A ball dropped from 9 m rises to 4 m after one bounce. Find e and the fraction of kinetic energy lost.',
                 steps=[r'e = √(h₁/h) = √(4/9) = 2/3.',
                        r'Fraction kept = e² = 4/9, so fraction lost = 1 − 4/9 = 5/9 ≈ 56%.',
                        r'Check with heights: energy just before impact ∝ 9, just after ∝ 4; lost 5 out of 9.'],
                 answer=r'e = 2/3; 5/9 of the kinetic energy is lost'),
            dict(tag='Numerical', q=r'A ball is dropped from 5 m on a floor with e = 0.5. Find the total distance travelled and the total time before it comes to rest.',
                 steps=[r'Distance: h(1 + e²)/(1 − e²) = 5 × 1.25/0.75 ≈ 8.33 m.',
                        r'First fall time t₀ = √(2 × 5/10) = 1 s.',
                        r'Total time = t₀(1 + e)/(1 − e) = 1 × 1.5/0.5 = 3 s.'],
                 answer=r'≈ 8.33 m; 3 s'),
            dict(tag='Numerical', q=r'A 1 kg ball moving at 6 m/s hits a 2 kg ball at rest head-on with e = 0.5. Find the final velocities and the kinetic energy lost.',
                 steps=[r'v₁ = (m₁ − em₂)u₁/(m₁ + m₂) = (1 − 1) × 6/3 = 0.',
                        r'v₂ = (1 + e)m₁u₁/(m₁ + m₂) = 1.5 × 6/3 = 3 m/s.',
                        r'Check: momentum 6 = 0 + 2 × 3; separation 3 = 0.5 × 6.',
                        r'K before = 18 J, after = ½ × 2 × 9 = 9 J, so 9 J is lost.'],
                 answer=r'0 and 3 m/s; 9 J lost'),
            dict(tag='Numerical', q=r'A ball strikes a smooth floor at 45° to the vertical with speed 10√2 m/s. e = 0.5. Find its speed and direction just after impact.',
                 steps=[r'Components: normal (vertical) 10 m/s, tangential (horizontal) 10 m/s.',
                        r'After: tangential stays 10 m/s; normal becomes 0.5 × 10 = 5 m/s upward.',
                        r'Speed = √(10² + 5²) = √125 ≈ 11.2 m/s.',
                        r'Angle with the vertical: tanθ′ = 10/5 = 2, so θ′ ≈ 63.4° (flatter than the 45° approach).'],
                 answer=r'≈ 11.2 m/s at about 63.4° to the vertical'),
        ],
        practice=[
            dict(q=r'A ball is dropped from 25 m on a floor with e = 0.6. The height it reaches after the first bounce is',
                 options=['15 m', '9 m', '3.24 m', '21 m'], answer=1, type='numerical',
                 explanation=r'h₁ = e²h = 0.36 × 25 = 9 m. 15 m multiplies by e instead of e². 3.24 m is e⁴h, the height after the second bounce.'),
            dict(q=r'In each bounce on a floor with e = 0.8, the percentage of kinetic energy lost is',
                 options=['20%', '64%', '80%', '36%'], answer=3, type='numerical',
                 explanation=r'The rebound speed is 0.8 times the arrival speed, so the kinetic energy kept is 0.64. The loss is 1 − e² = 0.36, i.e. 36%. 20% is 1 − e, which uses speed instead of energy. 64% is the fraction kept.'),
            dict(q=r'A ball moving at u hits an identical ball at rest head-on with e = 1/3. The ratio of their final speeds v₁ : v₂ is',
                 options=['1 : 2', '1 : 3', '2 : 1', '1 : 1'], answer=0, type='numerical',
                 explanation=r'For equal masses: v₁ = u(1 − e)/2 = u/3 and v₂ = u(1 + e)/2 = 2u/3. Ratio 1 : 2. 1 : 3 confuses the ratio with e itself. 1 : 1 would be a perfectly inelastic collision.'),
            dict(q=r'<strong>Statement I:</strong> When a ball hits a smooth floor obliquely, the component of its velocity parallel to the floor does not change.<br><strong>Statement II:</strong> For e &lt; 1, the ball rebounds at a larger angle from the normal than the angle at which it arrived.',
                 options=ST, answer=0, type='statement',
                 explanation=r'Statement I is true: a smooth floor exerts no tangential force. Statement II is true: tanθ′ = tanθ/e is larger when e &lt; 1, so the rebound is flatter. Both are correct.'),
        ],
     )),
]
