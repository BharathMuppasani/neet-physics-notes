"""Deepening layer: Motion in a Straight Line (chapter key 'linear')."""
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


def _text(x, y, s, color='ink-2', size=12, anchor='start', weight='normal'):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" style="fill:var(--{color});font-size:{size}px;font-weight:{weight}">{s}</text>'


def _curve(f, a, b, X, Y, color='indigo', w=2.4, n=80, dash=False):
    pts = ' '.join(f'{X(a + (b - a) * i / n):.1f},{Y(f(a + (b - a) * i / n)):.1f}' for i in range(n + 1))
    d = ';stroke-dasharray:5 4' if dash else ''
    return f'<polyline points="{pts}" style="fill:none;stroke:var(--{color});stroke-width:{w}{d}"/>'


def _dot(x, y, color='coral', r=4):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" style="fill:var(--{color})"/>'


def _poly(pts, fill):
    p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return f'<polygon points="{p}" style="fill:var(--{fill});stroke:none"/>'


def _arrow(x1, y1, x2, y2, color='ink-2', w=2):
    ang = math.atan2(y2 - y1, x2 - x1)
    h = 8
    p1 = (x2 - h * math.cos(ang - 0.4), y2 - h * math.sin(ang - 0.4))
    p2 = (x2 - h * math.cos(ang + 0.4), y2 - h * math.sin(ang + 0.4))
    return (_line(x1, y1, x2 - 4 * math.cos(ang), y2 - 4 * math.sin(ang), color, w)
            + f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" style="fill:var(--{color})"/>')


def _svg(w, h, label, body):
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}">{body}</svg>'


def _axes(X, Y, xr, yr, xl, yl):
    b = _line(X(xr[0]), Y(0), X(xr[1]) + 6, Y(0)) + _line(X(0), Y(yr[0]), X(0), Y(yr[1]) - 6)
    b += _text(X(xr[1]) + 6, Y(0) + 16, xl, anchor='end') + _text(X(0) + 6, Y(yr[1]) - 6, yl)
    return b


def _fig_numberline():
    X = lambda x: 40 + (x + 3) * 34
    b = _line(X(-3), 110, X(6.5), 110)
    for x in range(-3, 7):
        b += _line(X(x), 104, X(x), 116, 'ink-2', 1.2) + _text(X(x), 132, str(x).replace('-', '−'), 'muted', 11, 'middle')
    b += _text(X(0), 148, 'origin', 'muted', 11, 'middle')
    b += _arrow(X(-2), 78, X(5), 78, 'indigo') + _text((X(-2) + X(5)) / 2, 70, 'first leg: +7 m', 'indigo', 12, 'middle')
    b += _arrow(X(5), 92, X(1), 92, 'amber') + _text(X(5) + 6, 96, 'back: 4 m', 'amber', 12)
    b += _arrow(X(-2), 166, X(1), 166, 'coral', 2.6) + _text(X(1) + 8, 170, 'displacement = +3 m', 'coral', 12)
    b += _dot(X(-2), 110, 'green') + _text(X(-2), 30, 'start x = −2 m', 'green', 11.5, 'middle')
    b += _line(X(-2), 36, X(-2), 104, 'green', 1, True)
    b += _text(190, 200, 'distance = 7 + 4 = 11 m', 'ink-2', 12.5, 'middle')
    return _svg(380, 210, 'Number line: a particle moves from minus 2 to 5 and back to 1. Distance 11 metres, displacement plus 3 metres', b)


def _fig_chord_tangent():
    X, Y = _map((0, 5), (0, 13), (50, 20, 350, 190))
    f = lambda t: 0.4 * t * t + 0.5 * t
    b = _axes(X, Y, (0, 5), (0, 13), 't (s)', 'x (m)')
    b += _curve(f, 0, 5, X, Y)
    t1, t2, tm = 1, 4, 2.5
    b += _line(X(t1), Y(f(t1)), X(t2), Y(f(t2)), 'coral', 2)
    s = 0.8 * tm + 0.5
    b += _line(X(tm - 1.3), Y(f(tm) - 1.3 * s), X(tm + 1.3), Y(f(tm) + 1.3 * s), 'green', 2, True)
    b += _dot(X(t1), Y(f(t1)), 'coral') + _dot(X(t2), Y(f(t2)), 'coral') + _dot(X(tm), Y(f(tm)), 'green')
    b += _text(X(t2) + 8, Y(f(t2)) + 14, 'chord: average velocity', 'coral', 11.5)
    b += _text(X(tm) - 10, Y(f(tm)) - 34, 'tangent: instantaneous', 'green', 11.5, 'end')
    b += _text(X(tm) - 10, Y(f(tm)) - 20, 'velocity at t = 2.5 s', 'green', 11.5, 'end')
    return _svg(380, 210, 'Position time curve with a chord between t equals 1 and 4 seconds and the tangent at t equals 2.5 seconds, which is parallel to the chord', b)


def _fig_vt_cross():
    X, Y = _map((0, 6.4), (-9, 6), (50, 20, 350, 200))
    b = _poly([(X(0), Y(0)), (X(0), Y(-8)), (X(4), Y(0))], 'coral-soft')
    b += _poly([(X(4), Y(0)), (X(6), Y(4)), (X(6), Y(0))], 'green-soft')
    b += _axes(X, Y, (0, 6.4), (-9, 6), 't (s)', 'v (m/s)')
    b += _curve(lambda t: -8 + 2 * t, 0, 6, X, Y)
    b += _text(44, Y(-8) + 4, '−8', 'muted', 11, 'end') + _text(44, Y(4) + 4, '4', 'muted', 11, 'end')
    b += _text(X(4), Y(0) - 8, '4', 'muted', 11, 'middle')
    b += _text(X(1.2), Y(-6.2), 'v &lt; 0, a &gt; 0: slowing', 'coral', 11.5)
    b += _text(X(4.1), Y(5.2), 'v &gt; 0, a &gt; 0: speeding up', 'green', 11.5)
    return _svg(380, 214, 'Velocity time line rising from minus 8 to plus 4 metres per second with constant positive acceleration; speed falls until t equals 4 seconds then rises', b)


def _fig_trapezium():
    X, Y = _map((0, 5.6), (0, 11), (50, 20, 350, 190))
    u, a, t = 4, 1.2, 5
    v = u + a * t
    b = _poly([(X(0), Y(0)), (X(0), Y(u)), (X(t), Y(u)), (X(t), Y(0))], 'water-soft')
    b += _poly([(X(0), Y(u)), (X(t), Y(v)), (X(t), Y(u))], 'amber-soft')
    b += _axes(X, Y, (0, 5.6), (0, 11), 't', 'v')
    b += _curve(lambda s: u + a * s, 0, t, X, Y)
    b += _line(X(t), Y(0), X(t), Y(v), 'muted', 1, True)
    b += _text(44, Y(u) + 4, 'u', 'ink-2', 13, 'end') + _text(X(t) + 6, Y(v) + 4, 'v = u + at', 'ink-2', 12)
    b += _text(X(t / 2), Y(u / 2) + 4, 'rectangle = ut', 'water', 13, 'middle', 'bold')
    b += _text(X(t * 0.66), Y(u + 1.2), '½(at)t = ½at²', 'amber', 12.5, 'middle', 'bold')
    b += _text(X(t), Y(0) + 15, 't', 'ink-2', 12, 'middle')
    return _svg(380, 210, 'Velocity time graph for constant acceleration: the area splits into a rectangle u t and a triangle half a t squared', b)


def _fig_stack():
    b = ''
    rows = [('y (m)', lambda t: 20 * t - 5 * t * t, (0, 22), '20'),
            ('v (m/s)', lambda t: 20 - 10 * t, (-22, 22), '±20'),
            ('a (m/s²)', lambda t: -10, (-12, 4), '−10')]
    for i, (lab, f, yr, tick) in enumerate(rows):
        top = 14 + i * 100
        X, Y = _map((0, 4.4), yr, (60, top, 340, top + 78))
        b += _line(X(0), Y(0), X(4.4), Y(0)) + _line(X(0), top - 2, X(0), top + 80)
        b += _text(X(0) - 6, top + 8, lab, 'ink-2', 11.5, 'end')
        b += _curve(f, 0, 4, X, Y, 'indigo', 2.2)
        for tt in (2, 4):
            b += _line(X(tt), top, X(tt), top + 78, 'line-2', 1, True)
        b += _text(X(4.4), Y(0) - 5, 't (s)', 'muted', 10.5, 'end')
    b += _text(X(2), 316, 'top at 2 s', 'muted', 11, 'middle') + _text(X(4), 316, 'back at 4 s', 'muted', 11, 'middle')
    b += _text(X(2.6), 34, 'parabola', 'indigo', 11) + _text(X(2.6), 150, 'straight line, slope −g', 'indigo', 11) + _text(X(1.0), 288, 'constant −g, even at the top', 'indigo', 11)
    return _svg(380, 326, 'Three stacked graphs for a ball thrown up at 20 metres per second: height is a parabola, velocity a straight line from plus 20 to minus 20, acceleration constant at minus 10', b)


def _fig_vx():
    b = ''
    X, Y = _map((0, 22), (0, 11), (50, 20, 180, 150))
    b += _axes(X, Y, (0, 22), (0, 11), 'x (m)', 'v (m/s)')
    b += _curve(lambda x: 10 - 0.5 * x, 0, 20, X, Y)
    b += _text(44, Y(10) + 4, '10', 'muted', 11, 'end') + _text(X(20), Y(0) + 14, '20', 'muted', 11, 'middle')
    X2, Y2 = _map((0, 22), (-6, 1), (230, 20, 360, 150))
    b += _line(X2(0), Y2(0), X2(22) + 6, Y2(0)) + _line(X2(0), Y2(-6), X2(0), Y2(1) - 6)
    b += _text(X2(22) + 6, Y2(0) - 6, 'x (m)', anchor='end') + _text(X2(0) + 6, Y2(1) - 8, 'a (m/s²)')
    b += _curve(lambda x: -5 + 0.25 * x, 0, 20, X2, Y2, 'coral')
    b += _text(X2(0) - 6, Y2(-5) + 4, '−5', 'muted', 11, 'end') + _text(X2(20), Y2(0) - 6, '20', 'muted', 11, 'middle')
    b += _text(205, 178, 'a = v (dv/dx) = −0.5 v: retardation shrinks as the body slows', 'ink-2', 11.5, 'middle')
    return _svg(380, 190, 'Left: velocity falls linearly with position from 10 to 0 over 20 metres. Right: the acceleration rises linearly from minus 5 to 0', b)


def _fig_height_times():
    X, Y = _map((0, 4.3), (0, 24), (50, 24, 350, 190))
    f = lambda t: 20 * t - 5 * t * t
    b = _axes(X, Y, (0, 4.3), (0, 24), 't (s)', 'height (m)')
    b += _curve(f, 0, 4, X, Y)
    b += _line(X(0), Y(15), X(4.1), Y(15), 'coral', 1.4, True)
    for t in (1, 3):
        b += _dot(X(t), Y(15)) + _line(X(t), Y(15), X(t), Y(0), 'muted', 1, True)
        b += _text(X(t), Y(0) + 15, f't{"₁" if t == 1 else "₂"} = {t} s', 'coral', 11.5, 'middle')
    b += _text(44, Y(15) + 4, 'h = 15', 'coral', 11, 'end') + _text(44, Y(20) + 4, '20', 'muted', 11, 'end')
    b += _text(X(2), Y(20) - 10, 'H = 20 m at t = 2 s', 'indigo', 11.5, 'middle')
    return _svg(380, 214, 'Height time parabola for a ball thrown up at 20 metres per second. It passes 15 metres at 1 second going up and 3 seconds coming down', b)


def _fig_chase():
    X, Y = _map((0, 24), (0, 560), (55, 20, 350, 190))
    b = _axes(X, Y, (0, 24), (0, 560), 't (s)', 'x (m)')
    b += _curve(lambda t: 20 * t, 0, 24, X, Y, 'amber')
    b += _curve(lambda t: t * t, 0, 23.5, X, Y, 'indigo')
    b += _dot(X(20), Y(400)) + _line(X(20), Y(400), X(20), Y(0), 'muted', 1, True) + _line(X(0), Y(400), X(20), Y(400), 'muted', 1, True)
    b += _text(X(20), Y(0) + 15, '20', 'muted', 11, 'middle') + _text(49, Y(400) + 4, '400', 'muted', 11, 'end')
    b += _text(X(6), Y(190), 'car: x = 20t', 'amber', 12) + _text(X(13), Y(80), 'police: x = t²', 'indigo', 12)
    b += _text(X(20) - 6, Y(400) - 10, 'meet', 'coral', 12, 'end')
    return _svg(380, 210, 'Position time graphs of a car at constant 20 metres per second and a police jeep starting from rest with 2 metres per second squared. They meet at 20 seconds and 400 metres', b)


def _fig_odd():
    b = ''
    vals = [5, 15, 25, 35]
    for i, v in enumerate(vals):
        x = 70 + i * 72
        h = v * 4
        b += f'<rect x="{x}" y="{170 - h}" width="44" height="{h}" style="fill:var(--water-soft);stroke:var(--water);stroke-width:1.4"/>'
        b += _text(x + 22, 164 - h, f'{v} m', 'ink-2', 12, 'middle', 'bold')
        b += _text(x + 22, 186, f'{i + 1}{["st", "nd", "rd", "th"][i]} s', 'muted', 11.5, 'middle')
    b += _line(56, 170, 350, 170)
    b += _text(190, 204, 'from rest, g = 10 m/s²: 5 : 15 : 25 : 35 = 1 : 3 : 5 : 7', 'ink-2', 12, 'middle')
    return _svg(380, 214, 'Bar chart: a body falling from rest covers 5, 15, 25 and 35 metres in the first four seconds, in the ratio 1 to 3 to 5 to 7', b)


AR_OPTS = ['Both A and R are true, and R correctly explains A',
           'Both A and R are true, but R does not explain A',
           'A is true but R is false',
           'A is false but R is true']
ST_OPTS = ['Both statements are true',
           'Both statements are false',
           'Statement I is true, Statement II is false',
           'Statement I is false, Statement II is true']


DEEP = {
'linear-position': dict(
    level='basic',
    notes=[
        ('Frame of reference: rest and motion are relative', r'''<p>A passenger sitting in a moving train is at rest relative to the train and moving relative to the platform. Every statement about position, velocity or rest needs a frame of reference: an origin, a positive direction and a clock. In one dimension, a single signed coordinate \(x\) is enough.</p>
<p>We treat the body as a point object when its size is small compared with the distance it moves.</p>'''),
        ('Distance versus displacement: the key facts', r'''<ul><li>Distance is a scalar and never negative. Displacement is a vector and can be positive, negative or zero.</li>
<li>\(|\text{displacement}|\le\text{distance}\). They are equal only when the body never reverses.</li>
<li>Distance never decreases with time. Displacement can decrease.</li>
<li>Zero displacement with non-zero distance is common (a round trip). Zero distance forces zero displacement.</li></ul>
<p>For a position function \(x(t)\): find where \(v=dx/dt=0\) inside the interval, split there, and add the size of each piece.</p>'''),
        ('A circular-path comparison', r'''<p>Although this chapter is one-dimensional, questions often compare distance and displacement on a circle of radius \(R\). Half a circle: distance \(\pi R\), displacement \(2R\). Quarter circle: \(\pi R/2\) and \(\sqrt2R\). Full circle: \(2\pi R\) and zero.</p>'''),
    ],
    formulas=[
        dict(title='Distance from a position function', formula=r'd=\sum_k\left|x(t_k)-x(t_{k-1})\right|,\quad t_k=\text{times where }v=0',
             symbols='x(t) is position (m); the interval is split at every time t_k where velocity changes sign; d is total distance (m). Without a reversal there is one piece and d = |Δx|.'),
    ],
    figure=dict(svg=_fig_numberline(), caption='Moving from −2 m to 5 m and back to 1 m: distance adds both legs, displacement only compares the start and end.'),
    traps=[r'Do not compute distance as \(|x(t_2)-x(t_1)|\) when the body turns back in between. Always check for \(v=0\) inside the interval first.',
           r'Negative position does not mean negative velocity. A body at \(x=-5\) m can be moving in the \(+x\) direction.'],
    exam=r'''<ul><li>"x = t² − 4t + 3. Find distance and displacement in the first 5 s."</li>
<li>"Ratio of distance to displacement for half / three-quarter revolution."</li>
<li>"Which can be zero when the other is not?"</li>
<li>Statement questions on the properties of distance and displacement.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A particle moves as \(x=t^2-4t+3\) (SI units). Find its distance and displacement from \(t=0\) to \(t=5\) s.',
             steps=[r'\(v=2t-4\), which is zero at \(t=2\) s. Split the interval there.',
                    r'\(x(0)=3\) m, \(x(2)=-1\) m, \(x(5)=8\) m.',
                    r'Distance \(=|{-1}-3|+|8-(-1)|=4+9=13\) m.',
                    r'Displacement \(=8-3=5\) m.'],
             answer=r'Distance 13 m, displacement 5 m'),
        dict(tag='Ratio', q=r'A runner goes once round half of a circular track of radius 70 m. Find the ratio of distance to displacement. Use \(\pi=22/7\).',
             steps=[r'Distance = half the circumference = \(\pi R=220\) m.',
                    r'Displacement = diameter = \(2R=140\) m.',
                    r'Ratio \(=220/140=11/7=\pi/2\).'],
             answer=r'11 : 7 (that is, π : 2)'),
        dict(tag='Statement', q=r'Statement I: The distance travelled by a body can never be less than the magnitude of its displacement. Statement II: The displacement of a body can be zero while the distance is not.',
             steps=[r'The straight line is the shortest path between two points, so distance ≥ |displacement|. Statement I is true.',
                    r'A round trip ends where it began, so displacement is zero while distance is positive. Statement II is true.'],
             answer=r'Both statements are true.'),
    ],
    practice=[
        dict(q=r'A particle covers three-quarters of a circle of radius 7 m. Its distance and the magnitude of its displacement are (use \(\pi=22/7\))',
             options=['33 m and 14 m', '22 m and 9.9 m', '33 m and 9.9 m', '44 m and 0 m'], answer=2, type='numerical',
             explanation=r'Distance \(=\tfrac34\times2\pi R=33\) m. The start and end points are a quarter-circle apart, joined by a chord \(\sqrt2R\approx9.9\) m. 14 m is the diameter, which belongs to a half circle. 44 m and 0 m describe a full circle.'),
        dict(q=r'For \(x=6t-t^2\) (SI units), the distance covered in the first 4 s is',
             options=['8 m', '10 m', '9 m', '16 m'], answer=1, type='numerical',
             explanation=r'\(v=6-2t=0\) at 3 s. \(x(0)=0\), \(x(3)=9\), \(x(4)=8\). Distance \(=9+1=10\) m. 8 m is the displacement, which misses the turn. 9 m stops at the turning point.'),
        dict(q=r'Statement I: Displacement can be negative. Statement II: Distance travelled can decrease with time.',
             options=ST_OPTS, answer=2, type='statement',
             explanation=r'Displacement is signed, so it can be negative: statement I is true. Distance only adds the size of each step, so it never decreases: statement II is false.'),
        dict(q=r'A ball is thrown up and caught at the same point. Which statement is correct for the whole flight?',
             options=['Distance and displacement are both zero', 'Displacement is zero but distance is not', 'Distance is zero but displacement is not', 'Both are equal and non-zero'], answer=1, type='concept',
             explanation=r'The ball returns to its start, so displacement is zero. It travelled up and down, so distance is twice the height. Distance can never be zero while displacement is non-zero.'),
    ],
),

'linear-averages': dict(
    level='core',
    notes=[
        ('Equal times and equal distances', r'''<p><strong>Equal time intervals</strong> at speeds \(v_1\) and \(v_2\): total distance \(=(v_1+v_2)t\) in time \(2t\), so \(\bar v=\dfrac{v_1+v_2}{2}\) (arithmetic mean).</p>
<p><strong>Equal distances</strong> \(d\) each: times are \(d/v_1\) and \(d/v_2\), so \(\bar v=\dfrac{2d}{d/v_1+d/v_2}=\dfrac{2v_1v_2}{v_1+v_2}\) (harmonic mean). The slower leg takes more time and pulls the average down.</p>
<p>For three equal distances: \(\bar v=\dfrac{3v_1v_2v_3}{v_1v_2+v_2v_3+v_3v_1}\). The harmonic mean is always less than or equal to the arithmetic mean.</p>'''),
        ('Chord and tangent on an x–t graph', r'''<p>Average velocity between two times is the slope of the <strong>chord</strong> joining the two points. Instantaneous velocity is the slope of the <strong>tangent</strong>. As the interval shrinks, the chord turns into the tangent: \(v=\lim_{\Delta t\to0}\Delta x/\Delta t=dx/dt\).</p>
<p>For constant acceleration only, the average velocity equals \((u+v)/2\), and it equals the instantaneous velocity at the middle of the time interval.</p>'''),
        ('Average speed versus average velocity', r'''<p>Average speed \(\ge|\text{average velocity}|\), because distance \(\ge|\text{displacement}|\). For a round trip, average velocity is zero but average speed is not. Instantaneous speed always equals the magnitude of instantaneous velocity, because over a tiny interval there is no time to turn back.</p>'''),
    ],
    formulas=[
        dict(title='Three equal distances', formula=r'\bar v=\frac{3v_1v_2v_3}{v_1v_2+v_2v_3+v_3v_1}',
             symbols='v₁, v₂, v₃ are the constant speeds (m/s) over three equal distances in the same direction.'),
        dict(title='Weighted average speed', formula=r'\bar v=\frac{\sum v_it_i}{\sum t_i}=\frac{\sum d_i}{\sum d_i/v_i}',
             symbols='vᵢ is the speed on part i (m/s), tᵢ its duration (s), dᵢ its distance (m). Use the first form when times are given and the second when distances are given.'),
    ],
    figure=dict(svg=_fig_chord_tangent(), caption='The chord gives the average velocity over 1–4 s. For constant acceleration, the tangent at the mid-time 2.5 s is parallel to the chord.'),
    traps=[r'If a car does the first half of a trip at 20 km/h, no speed on the second half can make the average 40 km/h. That would need the second half to take zero time.',
           r'Average velocity \((u+v)/2\) is valid only for constant acceleration. For other motion use total displacement divided by total time.'],
    exam=r'''<ul><li>"First half distance at v₁, second half at v₂. Average speed?" (harmonic mean).</li>
<li>"First third / half of the time …" (arithmetic mean).</li>
<li>"Half the distance at v₀; of the remaining, half the time at v₁ and half at v₂."</li>
<li>"What speed is needed on the second half to average …?" (including impossible cases).</li>
<li>Average velocity from x(t) over an interval.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A car covers three equal parts of a straight road at 10, 20 and 60 m/s. Find its average speed.',
             steps=[r'Use \(\bar v=\dfrac{3v_1v_2v_3}{v_1v_2+v_2v_3+v_3v_1}\).',
                    r'Numerator: \(3\times10\times20\times60=36000\). Denominator: \(200+1200+600=2000\).',
                    r'\(\bar v=18\) m/s. The arithmetic mean, 30 m/s, would be wrong.'],
             answer=r'18 m/s'),
        dict(tag='Numerical', q=r'A body covers the first half of a distance at 10 m/s. For the second half, it moves at 20 m/s for half the time and 40 m/s for the other half. Find the average speed for the whole trip.',
             steps=[r'Second half: equal times, so its average speed is \((20+40)/2=30\) m/s.',
                    r'Now the two halves are equal distances at 10 and 30 m/s.',
                    r'\(\bar v=\dfrac{2\times10\times30}{10+30}=15\) m/s.'],
             answer=r'15 m/s'),
        dict(tag='Numerical', q=r'For \(x=3t^2+2\) (SI units), find the average velocity between \(t=1\) s and \(t=3\) s, and the instantaneous velocity at \(t=2\) s.',
             steps=[r'\(x(1)=5\) m, \(x(3)=29\) m. Average velocity \(=24/2=12\) m/s.',
                    r'\(v=6t\), so \(v(2)=12\) m/s.',
                    r'They match because acceleration is constant and 2 s is the mid-time.'],
             answer=r'Both 12 m/s'),
    ],
    practice=[
        dict(q=r'A car covers the first half of a distance at 30 km/h. What speed on the second half gives an average of 40 km/h?',
             options=['50 km/h', '60 km/h', '45 km/h', '70 km/h'], answer=1, type='numerical',
             explanation=r'\(\dfrac{2\times30\times v}{30+v}=40\Rightarrow60v=1200+40v\Rightarrow v=60\) km/h. 50 km/h assumes the arithmetic mean, which applies only to equal times. Check: 60 km/h gives times in the ratio 2 : 1, and the average is indeed 40.'),
        dict(q=r'A car covers the first half of a trip at 20 km/h. Statement I: It cannot average 40 km/h over the whole trip, however fast it goes on the second half. Statement II: For equal distances, the average speed is always less than twice the speed on either half.',
             options=ST_OPTS, answer=0, type='statement',
             explanation=r'\(\bar v=\dfrac{2v_1v_2}{v_1+v_2}=2v_1\dfrac{v_2}{v_1+v_2}\lt2v_1\), since the fraction is below 1. With \(v_1=20\), the average stays below 40 however large \(v_2\) is. Both statements are true.'),
        dict(q=r'A body moves with \(x=2t^2\) (SI units). Its average velocity over the first 3 s is',
             options=['12 m/s', '18 m/s', '9 m/s', '6 m/s'], answer=3, type='numerical',
             explanation=r'\(\Delta x=18-0=18\) m in 3 s, so 6 m/s. 12 m/s is the instantaneous velocity at 3 s. 18 m/s is the displacement read as a velocity.'),
        dict(q=r'On an x–t graph, the average velocity between two instants is the',
             options=['Slope of the tangent at the later instant', 'Area under the curve between them', 'Slope of the chord joining the two points', 'Average of the two positions'], answer=2, type='graph',
             explanation=r'Average velocity \(=\Delta x/\Delta t\), the slope of the chord. The tangent gives the instantaneous value. Area under an x–t graph has no standard physical meaning.'),
    ],
),

'linear-acceleration': dict(
    level='core',
    notes=[
        ('The four sign cases', r'''<div class="table-wrap"><table><thead><tr><th>v</th><th>a</th><th>Speed</th><th>Example</th></tr></thead><tbody>
<tr><td>+</td><td>+</td><td>increases</td><td>car speeding up forward</td></tr>
<tr><td>+</td><td>−</td><td>decreases</td><td>car braking while moving forward</td></tr>
<tr><td>−</td><td>+</td><td>decreases</td><td>ball falling while you take up as positive... no: ball rising with down as positive</td></tr>
<tr><td>−</td><td>−</td><td>increases</td><td>ball falling, with up as positive</td></tr></tbody></table></div>
<p>Rule: speed increases when \(v\) and \(a\) have the same sign and decreases when they have opposite signs.</p>'''),
        ('Average and instantaneous acceleration', r'''<p>Average acceleration \(=\Delta v/\Delta t\), the slope of the chord on a v–t graph. Instantaneous acceleration \(a=dv/dt=d^2x/dt^2\), the slope of the tangent. On an x–t graph, acceleration shows as curvature: bending up means \(a\gt0\), bending down means \(a\lt0\), straight means \(a=0\).</p>
<p>Velocity is a vector, so a change of direction alone is an acceleration. A body that reverses from +10 m/s to −10 m/s in 4 s has average acceleration −5 m/s² even though its speed is the same at both ends.</p>'''),
        ('Retardation', r'''<p>"Retardation" or "deceleration" means acceleration opposite to velocity, so the speed falls. It does not mean a negative sign. With a different choice of positive direction, the same retardation can have a positive sign.</p>'''),
    ],
    formulas=[
        dict(title='Average acceleration and curvature', formula=r'\bar a=\frac{v_2-v_1}{t_2-t_1},\qquad a=\frac{d^2x}{dt^2}',
             symbols='v₁, v₂ are signed velocities (m/s) at times t₁, t₂ (s); x(t) is position (m). Velocity changes direction count as acceleration.'),
    ],
    figure=dict(svg=_fig_vt_cross(), caption='Acceleration is +2 m/s² throughout. Speed falls until the line crosses zero at 4 s, then rises. The sign of a alone does not decide speeding up or slowing down.'),
    traps=[r'At the turning point, velocity is zero but acceleration usually is not. A ball at the top of its flight still has \(a=-g\).',
           r'"Uniform acceleration" means constant acceleration, not constant velocity.'],
    exam=r'''<ul><li>"x = t³ − 3t² + … . Is the particle speeding up or slowing down at t = …?"</li>
<li>"A body has negative acceleration. Is its speed necessarily decreasing?"</li>
<li>"Velocity changes from +10 to −10 m/s in 4 s. Average acceleration?"</li>
<li>Assertion–reason on zero velocity with non-zero acceleration.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'For \(x=t^3-3t^2+5\) (SI units), decide whether the particle is speeding up or slowing down at \(t=0.5\) s and at \(t=1.5\) s.',
             steps=[r'\(v=3t^2-6t\), \(a=6t-6\).',
                    r'At 0.5 s: \(v=-2.25\) m/s, \(a=-3\) m/s². Same sign, so it is speeding up.',
                    r'At 1.5 s: \(v=-2.25\) m/s, \(a=+3\) m/s². Opposite signs, so it is slowing down.'],
             answer=r'Speeding up at 0.5 s; slowing down at 1.5 s'),
        dict(tag='Graph', q=r'A v–t graph is a straight line from −8 m/s at \(t=0\) to +4 m/s at \(t=6\) s. Describe the motion.',
             steps=[r'Slope \(=12/6=2\) m/s², constant and positive.',
                    r'From 0 to 4 s, \(v\lt0\) and \(a\gt0\): the body moves backward and slows down.',
                    r'At 4 s it stops for an instant and reverses. After that, \(v\gt0\) and \(a\gt0\): it speeds up forward.'],
             answer=r'Slows down, turns at 4 s, then speeds up; a = +2 m/s² throughout'),
        dict(tag='Assertion–Reason', q=r'Assertion: A body can have zero velocity and non-zero acceleration at the same instant. Reason: Acceleration depends on how fast velocity is changing, not on the value of velocity.',
             steps=[r'At the top of a vertical throw, \(v=0\) while \(a=-g\). The assertion is true.',
                    r'The reason is true and it is exactly why the assertion holds: velocity is passing through zero while still changing.'],
             answer=r'Both true, and R correctly explains A.'),
    ],
    practice=[
        dict(q=r'A particle has \(v=4t-t^2\) (SI units). At \(t=3\) s it is',
             options=['speeding up, with a = −2 m/s²', 'slowing down, with a = −2 m/s²', 'slowing down, with a = +2 m/s²', 'at rest'], answer=1, type='numerical',
             explanation=r'\(v(3)=12-9=3\) m/s and \(a=4-2t=-2\) m/s². Opposite signs, so it is slowing down. "Speeding up" ignores the sign of v. It is not at rest: v = 0 only at t = 0 and t = 4 s.'),
        dict(q=r'Velocity changes from +10 m/s to −10 m/s in 4 s. The average acceleration is',
             options=['0', '−5 m/s²', '+5 m/s²', '−2.5 m/s²'], answer=1, type='numerical',
             explanation=r'\(\bar a=(-10-10)/4=-5\) m/s². Zero comes from comparing speeds instead of velocities. −2.5 m/s² divides only 10 m/s by 4 s.'),
        dict(q=r'Assertion: A body with negative acceleration can be speeding up. Reason: Speed increases when velocity and acceleration have the same sign.',
             options=AR_OPTS, answer=0, type='ar',
             explanation=r'If the velocity is also negative, the body speeds up in the negative direction, so the assertion is true. The reason gives the rule that makes it true, so it is the correct explanation.'),
        dict(q=r'The x–t graph of a particle is a curve that bends downward (like an upside-down bowl) throughout. The particle has',
             options=['Positive acceleration', 'Zero acceleration', 'Negative acceleration', 'Increasing speed in all cases'], answer=2, type='graph',
             explanation=r'Bending down means the slope (velocity) decreases with time, so \(a\lt0\). Zero acceleration would need a straight line. Whether speed increases depends on the sign of v too, so the last option is not always true.'),
    ],
),

'linear-equations': dict(
    level='core',
    notes=[
        ('Deriving the equations from a v–t graph', r'''<ol><li>The v–t graph is a straight line of slope \(a\) and intercept \(u\): \(v=u+at\).</li>
<li>Displacement is the area under it: a rectangle \(ut\) plus a triangle \(\tfrac12(at)t\). So \(s=ut+\tfrac12at^2\).</li>
<li>The area is also a trapezium: \(s=\tfrac12(u+v)t\). Put \(t=(v-u)/a\) to get \(v^2=u^2+2as\).</li></ol>
<p>Calculus gives the same results: integrate \(a=dv/dt\) once for \(v\), and \(v=dx/dt\) again for \(s\).</p>'''),
        ('Stopping distance and reaction time', r'''<p>A driver first reacts for a time \(t_r\), during which the car keeps its speed. Then the brakes give retardation \(a\).</p>
\[d=ut_r+\frac{u^2}{2a}\]
<p>Without reaction time, stopping distance \(\propto u^2\) and stopping time \(\propto u\). Doubling speed makes the braking distance four times as long.</p>'''),
        ('Ratios from rest (Galileo)', r'''<p>Starting from rest with constant \(a\):</p>
<ul><li>Distances in 1, 2, 3 … seconds (total): 1 : 4 : 9 …</li>
<li>Distances in the 1st, 2nd, 3rd … seconds: 1 : 3 : 5 … (odd numbers)</li>
<li>Times to cover successive equal distances: \(1:(\sqrt2-1):(\sqrt3-\sqrt2)\) …</li>
<li>Velocities after successive equal distances: \(1:\sqrt2:\sqrt3\) …</li></ul>'''),
    ],
    formulas=[
        dict(title='Stopping distance with reaction time', formula=r'd=ut_r+\frac{u^2}{2a}',
             symbols='u is initial speed (m/s), t_r the reaction time (s), a the magnitude of constant retardation (m/s²), d the total stopping distance (m).'),
        dict(title='Using the final velocity', formula=r's=vt-\tfrac12at^2',
             symbols='v final velocity (m/s), a constant acceleration (m/s²), t time (s), s displacement (m). Useful when u is unknown.'),
    ],
    figure=dict(svg=_fig_trapezium(), caption='The area under a straight v–t line splits into a rectangle ut and a triangle ½at². Together they give s = ut + ½at².'),
    traps=[r'Plugging a negative time from the quadratic \(s=ut+\tfrac12at^2\) is meaningless. Choose the root that fits the physical situation.',
           r'With braking, use \(a\) as negative when \(u\) is positive. Writing \(v^2=u^2+2as\) with \(a=+4\) for braking gives an impossible answer.'],
    exam=r'''<ul><li>"Stopping distance if speed is doubled" (four times).</li>
<li>"A bullet loses half its speed in penetrating 3 cm. How much farther will it go?"</li>
<li>"From rest, ratio of distances in successive equal intervals" (1 : 3 : 5).</li>
<li>Reaction time plus braking distance problems.</li>
<li>"Which equation fails when the acceleration is not constant?"</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A car moves at 20 m/s. The driver reacts in 0.5 s and the brakes give 5 m/s². Find the stopping distance.',
             steps=[r'Reaction distance: \(20\times0.5=10\) m.',
                    r'Braking distance: \(u^2/2a=400/10=40\) m.',
                    r'Total: 50 m.'],
             answer=r'50 m'),
        dict(tag='Numerical', q=r'A bullet loses half its speed in passing 3 cm into a wooden block. How much farther will it go before stopping? Assume constant retardation.',
             steps=[r'First 3 cm: \(v^2\) drops from \(u^2\) to \(u^2/4\), a fall of \(3u^2/4\).',
                    r'\(v^2\) falls in proportion to distance, since \(\Delta(v^2)=2as\).',
                    r'The remaining \(u^2/4\) is one third of \(3u^2/4\), so it needs one third of 3 cm.'],
             answer=r'1 cm more'),
        dict(tag='Ratio', q=r'A body starts from rest with constant acceleration. Find the ratio of distances covered in the first 2 s and the next 2 s.',
             steps=[r'\(s\propto t^2\) from rest. In 2 s: \(\propto4\). In 4 s: \(\propto16\).',
                    r'The next 2 s cover \(16-4=12\).',
                    r'Ratio \(4:12=1:3\).'],
             answer=r'1 : 3'),
    ],
    practice=[
        dict(q=r'A body starts from rest with constant acceleration. The times taken to cover the first metre and the second metre are in the ratio',
             options=[r'\(1:\sqrt2\)', r'\(1:(\sqrt2-1)\)', '1 : 3', '1 : 2'], answer=1, type='numerical',
             explanation=r'\(t\propto\sqrt s\): 1 m takes \(\propto1\), 2 m take \(\propto\sqrt2\). The second metre takes \(\sqrt2-1\). \(1:\sqrt2\) compares total times, not the second metre alone. 1 : 3 is the ratio of distances in equal times.'),
        dict(q=r'A bullet&#39;s speed falls from 200 m/s to 100 m/s on passing through one plank. Assuming the same constant retardation, in which plank does it stop?',
             options=['First', 'Second', 'Third', 'Fourth'], answer=1, type='numerical',
             explanation=r'Each plank removes \(\Delta(v^2)=200^2-100^2=30000\). The bullet has \(v^2=40000\) at the start, so it needs \(40000/30000\approx1.33\) planks: it stops inside the second. "Third" comes from using speed losses (100 m/s per plank) instead of \(v^2\).'),
        dict(q=r'Statement I: \(s=ut+\tfrac12at^2\) gives the distance travelled even if the body reverses during the interval. Statement II: \(v^2=u^2+2as\) holds only for constant acceleration.',
             options=ST_OPTS, answer=3, type='statement',
             explanation=r'Statement I is false: the equation gives net displacement, so a reversal makes distance larger than \(s\). Statement II is true: all these equations assume constant acceleration.'),
        dict(q=r'A car accelerates from rest at 2 m/s² for 5 s, then brakes uniformly to rest in 2 s. The total distance is',
             options=['25 m', '45 m', '35 m', '30 m'], answer=2, type='numerical',
             explanation=r'Top speed 10 m/s. First part: \(\tfrac12\times2\times25=25\) m. Braking: average speed 5 m/s for 2 s = 10 m. Total 35 m. 25 m ignores braking. 45 m treats braking as 2 s at the full 10 m/s.'),
    ],
),

'linear-graphs': dict(
    level='exam',
    notes=[
        ('A catalogue of standard shapes', r'''<div class="table-wrap"><table><thead><tr><th>Motion</th><th>x–t</th><th>v–t</th><th>a–t</th></tr></thead><tbody>
<tr><td>Rest</td><td>horizontal line</td><td>on the t-axis</td><td>on the t-axis</td></tr>
<tr><td>Uniform velocity</td><td>straight sloping line</td><td>horizontal line</td><td>on the t-axis</td></tr>
<tr><td>Uniform acceleration from rest</td><td>parabola bending up</td><td>straight line through origin</td><td>horizontal line above axis</td></tr>
<tr><td>Uniform retardation to rest</td><td>parabola bending down, flattening</td><td>straight line falling to the axis</td><td>horizontal line below axis</td></tr>
<tr><td>Ball thrown up (up +)</td><td>inverted parabola</td><td>straight line of slope −g crossing the axis</td><td>constant −g</td></tr></tbody></table></div>'''),
        ('Graphs that cannot happen', r'''<ul><li>An x–t curve that doubles back in time (two positions at one instant).</li>
<li>A vertical segment on x–t (infinite velocity) or on v–t (infinite acceleration).</li>
<li>A distance–time graph that decreases, or a speed–time graph below the axis.</li>
<li>Total path length less than the size of the displacement.</li></ul>'''),
        ('Converting one graph into another', r'''<p>From v–t to x–t: where v is positive, x rises; where v is zero, x has a flat point; a straight v–t line gives a parabolic x–t piece. From v–t to a–t: read the slope of each straight piece. From a–t to v–t: add the area of each piece to the starting velocity.</p>
<p>A ball dropped onto a hard floor that bounces back to the same height gives a sawtooth v–t graph: straight lines of slope −g, with sudden jumps from −v to +v at each bounce.</p>'''),
    ],
    formulas=[
        dict(title='Average speed from a v–t graph', formula=r'\bar v_{\text{speed}}=\frac{\sum|\text{areas}|}{\text{total time}},\qquad \bar v=\frac{\sum\text{signed areas}}{\text{total time}}',
             symbols='Areas are measured between the v–t curve and the time axis, in m; total time in s. Pieces below the axis count as negative for displacement and positive for distance.'),
    ],
    figure=dict(svg=_fig_stack(), caption='A ball thrown up at 20 m/s (g = 10 m/s², up positive). The x–t parabola peaks where the v–t line crosses zero, while a stays at −g all the time.'),
    traps=[r'On a v–t graph, the point where the line crosses the time axis is where the body turns, not where it returns to the start.',
           r'Two x–t lines crossing means the bodies are at the same place. Two v–t lines crossing only means they have the same velocity at that instant.'],
    exam=r'''<ul><li>"From the v–t graph, find displacement / distance / average speed."</li>
<li>"Which of these x–t graphs is not possible?"</li>
<li>"An a–t graph is given. Find the maximum velocity" (area).</li>
<li>"The v–t graph of a ball dropped on the floor that rebounds is …"</li>
<li>"Two x–t lines cross at P. What does P represent?"</li></ul>''',
    examples=[
        dict(tag='Graph', q=r'A v–t graph is a straight line from +10 m/s at \(t=0\) to −10 m/s at \(t=4\) s. Find the displacement, distance and average speed.',
             steps=[r'The line crosses zero at \(t=2\) s.',
                    r'Area 0–2 s: \(\tfrac12\times2\times10=+10\) m. Area 2–4 s: \(-10\) m.',
                    r'Displacement \(=0\). Distance \(=20\) m.',
                    r'Average speed \(=20/4=5\) m/s. Average velocity is zero.'],
             answer=r'0 m, 20 m, 5 m/s'),
        dict(tag='Graph', q=r'Using the stacked graphs above, describe what happens at \(t=2\) s.',
             steps=[r'The x–t curve is at its peak: height 20 m.',
                    r'The v–t line crosses zero: the ball is momentarily at rest and turning.',
                    r'The a–t line is still at −10 m/s². Gravity has not switched off.'],
             answer=r'Highest point; v = 0 but a = −g'),
        dict(tag='Concept', q=r'A ball is dropped on a hard floor and rebounds to the same height each time. Sketch its v–t graph in words (up positive).',
             steps=[r'While falling, v goes from 0 down to −u along a line of slope −g.',
                    r'At the bounce, v jumps suddenly from −u to +u.',
                    r'While rising, v falls from +u to 0 along the same slope −g, and the pattern repeats.'],
             answer=r'A sawtooth: parallel lines of slope −g joined by vertical jumps at each bounce'),
    ],
    practice=[
        dict(q=r'A body starts from rest. Its a–t graph shows +2 m/s² for 0–4 s and −2 m/s² for 4–8 s. Its maximum velocity and its displacement in 8 s are',
             options=['8 m/s and 32 m', '8 m/s and 64 m', '16 m/s and 32 m', '8 m/s and 0 m'], answer=0, type='graph',
             explanation=r'Area 0–4 s gives v = 8 m/s, the maximum. Then it slows to 0 at 8 s, without reversing. Displacement = area of the v–t triangle = \(\tfrac12\times8\times8=32\) m. 0 m wrongly assumes it returns. 64 m treats the v–t graph as a rectangle.'),
        dict(q=r'Which x–t graph is physically impossible for a single body?',
             options=['A horizontal line', 'A straight line sloping down', 'A curve with two values of x at the same t', 'A parabola opening downward'], answer=2, type='graph',
             explanation=r'A body cannot be in two places at once, so x must have one value at each t. A horizontal line is rest, a falling line is uniform motion in the −x direction and a downward parabola is a vertical throw.'),
        dict(q=r'An x–t graph is a parabola opening downward with its peak at \(t=3\) s. The velocity at \(t=3\) s is',
             options=['Maximum', 'Zero', 'Negative and maximum in size', 'Equal to the acceleration'], answer=1, type='graph',
             explanation=r'The tangent at the peak is horizontal, so v = 0. The acceleration there is negative and non-zero. The velocity is largest in size at the ends of the interval, not at the peak.'),
        dict(q=r'The area under an acceleration–time graph gives',
             options=['Displacement', 'Change in velocity', 'Distance', 'Change in acceleration'], answer=1, type='concept',
             explanation=r'\(\int a\,dt=\Delta v\). Displacement is the area under a v–t graph, one step further. The slope of the a–t graph, not its area, would relate to the change in acceleration.'),
    ],
),

'linear-gravity': dict(
    level='exam',
    notes=[
        ('Standard results for a vertical throw', r'''<p>Take up as positive, so \(a=-g\). For launch speed \(u\):</p>
<ul><li>Time to top \(=u/g\); maximum height \(H=u^2/2g\); total time back \(=2u/g\).</li>
<li>The ball passes every height with the same speed going up and coming down: \(v=\sqrt{u^2-2gh}\).</li>
<li>It returns to the launch point with speed \(u\), pointing down.</li>
<li>If it is at height \(h\) at times \(t_1\) and \(t_2\): \(t_1+t_2=2u/g\) and \(t_1t_2=2h/g\). So \(u=g(t_1+t_2)/2\) and \(h=gt_1t_2/2\).</li></ul>'''),
        ('Released from a moving balloon or lift', r'''<p>An object released from a rising balloon keeps the balloon&#39;s upward velocity at that instant. It first rises, then falls. Write one equation with the launch point as origin: \(-H=ut-\tfrac12gt^2\), where \(H\) is the height of release. Solve the quadratic and keep the positive root.</p>'''),
        ('Free fall from rest', r'''<p>\(h=\tfrac12gt^2\), \(v=gt=\sqrt{2gh}\). Distances in successive seconds: 5, 15, 25, 35 m (ratio 1 : 3 : 5 : 7) with \(g=10\) m/s². Time to fall varies as \(\sqrt h\) and impact speed varies as \(\sqrt h\). Without air resistance, mass does not matter.</p>'''),
    ],
    formulas=[
        dict(title='Two times at the same height', formula=r't_1+t_2=\frac{2u}{g},\qquad t_1t_2=\frac{2h}{g},\qquad h=\tfrac12gt_1t_2',
             symbols='u is the upward launch speed (m/s), h the height above the launch point (m), t₁ and t₂ the times (s) when the body is at h going up and coming down; g = 10 m/s².'),
        dict(title='Impact speed from a height', formula=r'v=\sqrt{u^2+2gH}',
             symbols='u is the launch speed in any vertical direction (m/s), H the height of the launch point above the ground (m). The same for a throw up or down.'),
    ],
    figure=dict(svg=_fig_height_times(), caption='A ball thrown up at 20 m/s is 15 m high at 1 s (going up) and at 3 s (coming down). The two times are symmetric about the top at 2 s.'),
    traps=[r'A stone dropped from a rising balloon does not start from rest. It starts with the balloon&#39;s upward velocity.',
           r'Thrown up or thrown down at the same speed from the same tower, both stones hit the ground at the same speed, but the one thrown up takes longer.'],
    exam=r'''<ul><li>"A stone thrown up from a tower of height … hits the ground after …"</li>
<li>"A body is at the same height at t₁ and t₂. Find u and h."</li>
<li>"Ratio of maximum heights for launch speeds in the ratio …"</li>
<li>"A body falls from rest and covers … m in the last second. Find the height."</li>
<li>"A packet is dropped from a balloon rising at … m/s."</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A balloon rises at 10 m/s. A packet is released when the balloon is 40 m above the ground. When does it reach the ground?',
             steps=[r'The packet starts with \(u=+10\) m/s (up). Taking the release point as origin, it lands at \(y=-40\) m.',
                    r'\(-40=10t-5t^2\Rightarrow5t^2-10t-40=0\Rightarrow t^2-2t-8=0\).',
                    r'\((t-4)(t+2)=0\), so \(t=4\) s. The negative root is not physical.'],
             answer=r'4 s'),
        dict(tag='Numerical', q=r'A ball thrown up is at the same height at \(t_1=1\) s and \(t_2=3\) s. Find its launch speed and that height.',
             steps=[r'\(u=g(t_1+t_2)/2=10\times4/2=20\) m/s.',
                    r'\(h=gt_1t_2/2=10\times3/2=15\) m.',
                    r'Check at 1 s: \(20-5=15\) m. At 3 s: \(60-45=15\) m.'],
             answer=r'20 m/s, 15 m'),
        dict(tag='Assertion–Reason', q=r'Assertion: Two stones thrown from the top of a tower with the same speed, one up and one down, hit the ground with the same speed. Reason: Both have the same \(u^2\) and fall through the same net height, so \(v^2=u^2+2gH\) is the same.',
             steps=[r'The upward stone returns to the tower top with the same speed \(u\), now moving down. From there, its motion copies the other stone.',
                    r'The reason states the same thing using \(v^2=u^2+2gH\). It is true and explains the assertion.'],
             answer=r'Both true, and R correctly explains A.'),
    ],
    practice=[
        dict(q=r'A stone is thrown up at 20 m/s from the top of a 25 m tower. It hits the ground after',
             options=['4 s', '2.5 s', '1 s', '5 s'], answer=3, type='numerical',
             explanation=r'\(-25=20t-5t^2\Rightarrow t^2-4t-5=0\Rightarrow t=5\) s. 4 s is the time to return to the tower top; 1 s is the unphysical root\'s size. Forgetting the extra 25 m drop gives 4 s.'),
        dict(q=r'A body falls freely from rest and covers 45 m in the last second of its fall. The height it fell from is',
             options=['80 m', '125 m', '100 m', '180 m'], answer=1, type='numerical',
             explanation=r'Distance in the nth second \(=\tfrac g2(2n-1)=5(2n-1)=45\Rightarrow n=5\) s. Height \(=\tfrac12\times10\times25=125\) m. 80 m is the height for 4 s; 180 m for 6 s.'),
        dict(q=r'Two balls are thrown straight up with speeds in the ratio 1 : 2. Their maximum heights are in the ratio',
             options=['1 : 2', '1 : 4', r'\(1:\sqrt2\)', '2 : 1'], answer=1, type='numerical',
             explanation=r'\(H=u^2/2g\propto u^2\), so 1 : 4. 1 : 2 is the ratio of times to the top, which vary as \(u\).'),
        dict(q=r'Statement I: A ball thrown up and an identical ball thrown down at the same speed from the same height reach the ground with the same speed. Statement II: They take the same time to reach the ground.',
             options=ST_OPTS, answer=2, type='statement',
             explanation=r'Both have \(v^2=u^2+2gH\), so statement I is true. The upward ball first rises and returns to the top, taking an extra \(2u/g\), so statement II is false.'),
    ],
),

'linear-relative': dict(
    level='exam',
    notes=[
        ('Relative velocity in one dimension', r'''<p>\(v_{AB}=v_A-v_B\) is the velocity of A as seen by B. Also \(v_{BA}=-v_{AB}\). With a common positive direction:</p>
<ul><li>Same direction: relative speed \(=|v_A-v_B|\).</li>
<li>Opposite directions: relative speed \(=|v_A|+|v_B|\).</li></ul>
<p><strong>Crossing trains:</strong> to pass completely, one train must move its whole length plus the other&#39;s length relative to the other. Time \(=\dfrac{L_1+L_2}{v_{\text{rel}}}\).</p>'''),
        ('Relative motion with acceleration', r'''<p>Use relative initial separation, relative initial velocity and relative acceleration in one equation: \(s_{\text{rel}}=u_{\text{rel}}t+\tfrac12a_{\text{rel}}t^2\).</p>
<ul><li>Two bodies in free fall have \(a_{\text{rel}}=0\), so their relative velocity stays constant. A stone dropped from a tower and another thrown up from the ground meet after \(t=H/u\).</li>
<li><strong>Chase:</strong> a car at constant \(v\) passes a jeep at rest that starts with acceleration \(a\). They meet when \(vt=\tfrac12at^2\), so \(t=2v/a\). The jeep then has speed \(2v\).</li>
<li><strong>Avoiding a collision:</strong> a faster car behind a slower one brakes. It avoids hitting it if \(u_{\text{rel}}^2\le2a\,d\), where \(d\) is the gap.</li></ul>'''),
        ('Inside a lift', r'''<p>For an object dropped inside a lift, use the lift as the frame. If the lift moves at constant velocity, the object falls as if the lift were at rest. If the lift accelerates upward at \(a\), the object falls relative to the floor with \(g+a\). If downward at \(a\), with \(g-a\).</p>'''),
    ],
    formulas=[
        dict(title='Crossing and overtaking time', formula=r't=\frac{L_1+L_2}{v_1\pm v_2}',
             symbols='L₁, L₂ are the lengths of the two bodies (m); v₁, v₂ their speeds (m/s). Use + for opposite directions and − (with v₁ > v₂) for the same direction. A pole or a person has L = 0.'),
        dict(title='Collision avoidance with braking', formula=r'a_{\min}=\frac{(v_1-v_2)^2}{2d}',
             symbols='v₁ is the speed of the car behind (m/s), v₂ the speed of the car ahead (m/s, constant), d the initial gap (m), a_min the least braking retardation (m/s²).'),
    ],
    figure=dict(svg=_fig_chase(), caption='A car at a steady 20 m/s and a police jeep starting from rest at 2 m/s². Where the x–t graphs cross, the two are at the same place: t = 20 s, x = 400 m.'),
    traps=[r'Relative velocity is not "the bigger minus the smaller" for opposite directions. With signs, \(v_A-v_B=(+20)-(-30)=50\) m/s.',
           r'A ball dropped in a lift moving up at constant speed takes the same time to hit the floor as in a lift at rest. Only acceleration of the lift changes the time.'],
    exam=r'''<ul><li>"Two trains of lengths … cross each other in … s. Find the speed."</li>
<li>"A stone is dropped from a tower; another is thrown up from the ground at the same instant. When and where do they meet?"</li>
<li>"A car passes a police jeep at rest. The jeep starts with acceleration a. When does it catch the car?"</li>
<li>"Minimum retardation to avoid a collision."</li>
<li>"Two balls dropped 1 s apart. How does their separation change?"</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'Trains of length 100 m and 150 m move at 20 m/s and 30 m/s. How long do they take to cross each other if they move (a) in opposite directions (b) in the same direction?',
             steps=[r'Total length to clear: 250 m.',
                    r'Opposite: relative speed 50 m/s, time 5 s.',
                    r'Same direction: relative speed 10 m/s, time 25 s.'],
             answer=r'(a) 5 s (b) 25 s'),
        dict(tag='Numerical', q=r'A car moving at a constant 20 m/s passes a police jeep at rest. The jeep starts at once with 2 m/s². When and where does it catch the car, and at what speed?',
             steps=[r'Car: \(x=20t\). Jeep: \(x=\tfrac12(2)t^2=t^2\).',
                    r'Meet: \(t^2=20t\Rightarrow t=20\) s.',
                    r'Position \(=400\) m. Jeep speed \(=2\times20=40\) m/s, twice the car&#39;s.'],
             answer=r'20 s, 400 m, 40 m/s'),
        dict(tag='Numerical', q=r'A stone is dropped from a 100 m tower. At the same instant another is thrown up from the ground at 25 m/s along the same line. When and where do they meet?',
             steps=[r'Both have acceleration g, so the relative acceleration is zero.',
                    r'Relative speed is 25 m/s, closing a 100 m gap: \(t=100/25=4\) s.',
                    r'Dropped stone has fallen \(5\times16=80\) m, so they meet 20 m above the ground. Check: \(25\times4-80=20\) m.'],
             answer=r'After 4 s, 20 m above the ground'),
        dict(tag='Numerical', q=r'A bolt falls from the ceiling of a lift 2.5 m high. Find the fall time when the lift (a) moves up at a constant 5 m/s (b) accelerates up at 2.5 m/s².',
             steps=[r'(a) Constant velocity: relative acceleration is g. \(t=\sqrt{2\times2.5/10}=\sqrt{0.5}\approx0.71\) s.',
                    r'(b) Relative acceleration \(g+a=12.5\) m/s². \(t=\sqrt{5/12.5}=\sqrt{0.4}\approx0.63\) s.'],
             answer=r'(a) 0.71 s (b) 0.63 s'),
    ],
    practice=[
        dict(q=r'A stone is dropped from an 80 m tower. At the same instant a second stone is thrown up from the ground at 40 m/s along the same line. They meet at a height of',
             options=['20 m', '40 m', '60 m', '75 m'], answer=2, type='numerical',
             explanation=r'Relative acceleration is zero, so \(t=80/40=2\) s. The dropped stone falls \(5\times4=20\) m, meeting at 60 m. Check: \(40\times2-20=60\) m. 20 m is the distance fallen, not the height of the meeting.'),
        dict(q=r'A 200 m train moves at 20 m/s. A man runs at 2 m/s in the same direction alongside it. The train passes him in about',
             options=['9.1 s', '10 s', '11.1 s', '100 s'], answer=2, type='numerical',
             explanation=r'Relative speed \(=20-2=18\) m/s, so \(t=200/18\approx11.1\) s. 9.1 s uses 22 m/s, which is for opposite directions. 10 s ignores the man&#39;s motion.'),
        dict(q=r'Car B, 50 m behind car A, moves at 25 m/s while A moves at a steady 15 m/s in the same direction. The least retardation B needs to avoid hitting A is',
             options=['1 m/s²', '2 m/s²', '0.5 m/s²', '4 m/s²'], answer=0, type='numerical',
             explanation=r'Relative speed 10 m/s must fall to zero within 50 m: \(a=10^2/(2\times50)=1\) m/s². 4 m/s² would use B&#39;s own speed 25 m/s in a different way; using 25² gives 6.25 m/s², which is more than needed because only the relative speed matters.'),
        dict(q=r'Assertion: Two bodies falling freely near the Earth have zero relative acceleration. Reason: The relative velocity of two freely falling bodies is always zero.',
             options=AR_OPTS, answer=2, type='ar',
             explanation=r'Both accelerate at g, so their relative acceleration is zero: the assertion is true. Their relative velocity is constant but need not be zero. A stone thrown down and one dropped have different velocities, so the reason is false.'),
    ],
),
}


NEW_SECTIONS = [
dict(chapter='linear', after='linear-equations', id='linear-nth',
     title='Distance in the nth second',
     intro=r'The displacement during the nth second is the displacement in n seconds minus that in (n − 1) seconds. For constant acceleration this gives \(s_n=u+\tfrac a2(2n-1)\).',
     reasoning=r'Derivation: \(s_n=\left[un+\tfrac12an^2\right]-\left[u(n-1)+\tfrac12a(n-1)^2\right]=u+\tfrac a2(2n-1)\). The formula looks dimensionally wrong, but each term is really multiplied by a hidden interval of 1 s. It gives displacement, so check for a reversal inside that second before calling it distance.',
     formula=r's_n=u+\frac{a}{2}(2n-1)',
     symbols='u is the initial velocity at t = 0 (m/s), a the constant acceleration (m/s²), n the second being counted (1st, 2nd, …), sₙ the displacement during that one second (m). The hidden factor of 1 s makes it dimensionally correct.',
     trap=r'If the body turns around within the nth second, \(s_n\) is displacement, not distance. In a vertical throw this can even give zero.',
     example=r'A body starts from rest with acceleration 4 m/s². How far does it go in the 5th second?',
     solution=r'\(s_5=0+\tfrac42(2\times5-1)=2\times9=18\) m. Check: in 5 s it covers 50 m and in 4 s, 32 m; the difference is 18 m.',
     question=r'A body starts from rest with uniform acceleration. The distances it covers in the 2nd and 3rd seconds are in the ratio',
     options='2 : 3|3 : 5|4 : 9|1 : 3', answer=1,
     explanation=r'From rest, \(s_n\propto(2n-1)\): the 2nd and 3rd seconds give 3 and 5. 4 : 9 compares total distances in 2 s and 3 s. 2 : 3 just uses n.',
     deep=dict(
         level='exam',
         notes=[
             ('Derivation and the hidden "1 second"', r'''<ol><li>Displacement in \(n\) s: \(un+\tfrac12an^2\).</li>
<li>Displacement in \((n-1)\) s: \(u(n-1)+\tfrac12a(n-1)^2\).</li>
<li>Subtract: \(u+\tfrac12a\left[n^2-(n-1)^2\right]=u+\tfrac a2(2n-1)\).</li></ol>
<p>Written fully, \(s_n=u(1\,\text{s})+\tfrac a2(2n-1)(1\,\text{s})^2\). The "1 s" is the length of the interval, so the formula is dimensionally fine.</p>'''),
             ('Useful consequences', r'''<ul><li>From rest: \(s_1:s_2:s_3\ldots=1:3:5\ldots\) (Galileo&#39;s odd numbers).</li>
<li>Consecutive seconds always differ by \(a\times(1\,\text{s})^2\): \(s_{n+1}-s_n=a\). So two such distances give the acceleration directly.</li>
<li>From rest, the ratio of the distance in the nth second to the distance in n seconds is \((2n-1)/n^2\).</li></ul>'''),
             ('Vertical throws', r'''<p>With up positive, \(s_n=u-\tfrac g2(2n-1)\). In the last second before reaching the top, any upward throw rises \(g/2=5\) m. That second mirrors the first second of a free fall from rest. If the top falls inside the nth second, split the second at the top to get the distance.</p>'''),
         ],
         formulas=[
             dict(title='Difference of consecutive seconds', formula=r's_{n+1}-s_n=a,\qquad s_m-s_n=(m-n)\,a',
                  symbols='sₙ is the displacement in the nth second (m), a the constant acceleration (m/s²); m and n are whole numbers. The result has a hidden factor of (1 s)².'),
             dict(title='Vertical throw, nth second', formula=r's_n=u-\frac{g}{2}(2n-1)',
                  symbols='u is the upward launch speed (m/s), g = 10 m/s², up positive. Gives displacement; split the second at the top if the turn falls inside it.'),
         ],
         figure=dict(svg=_fig_odd(), caption='A body falling from rest covers 5, 15, 25 and 35 m in the 1st to 4th seconds. Consecutive bars differ by g × (1 s)² = 10 m.'),
         traps=[r'"Distance in 3 s" and "distance in the 3rd second" are different questions. The first is \(\tfrac12a(9)\), the second is \(\tfrac a2(5)\) from rest.',
                r'The formula measures from \(t=0\). If the motion starts at some other time, count n from the start of the motion.'],
         exam=r'''<ul><li>"A body covers x m in the nth second and y m in the (n + 1)th second. Find a and u."</li>
<li>"Ratio of distances in the 2nd and 3rd seconds / in the nth second and in n seconds."</li>
<li>"A ball is thrown up at … m/s. Distance in the 3rd second?" (check for a turn).</li>
<li>"A body falls from rest and covers … in the last second. Find the height."</li></ul>''',
         examples=[
             dict(tag='Numerical', q=r'A body covers 10 m in the 3rd second and 14 m in the 5th second. Find its acceleration and initial velocity.',
                  steps=[r'\(s_5-s_3=2a\), so \(14-10=2a\) and \(a=2\) m/s².',
                         r'\(s_3=u+\tfrac22(5)=u+5=10\), so \(u=5\) m/s.',
                         r'Check: \(s_5=5+\tfrac22(9)=14\) m.'],
                  answer=r'\(a=2\) m/s², \(u=5\) m/s'),
             dict(tag='Numerical', q=r'A ball is thrown up at 25 m/s. Find its displacement and the distance it covers in the 3rd second. Use g = 10 m/s².',
                  steps=[r'Displacement: \(s_3=25-5(5)=0\).',
                         r'The ball reaches the top at \(t=2.5\) s, inside the 3rd second, so split it there.',
                         r'From 2 s to 2.5 s it rises \(\tfrac12\times10\times0.5^2=1.25\) m, and from 2.5 s to 3 s it falls 1.25 m.',
                         r'Distance \(=2.5\) m.'],
                  answer=r'Displacement 0, distance 2.5 m'),
             dict(tag='Ratio', q=r'From rest, find the ratio of the distance covered in the 3rd second to that covered in the first 3 seconds.',
                  steps=[r'\(s_3=\tfrac a2(5)\) and \(s(3)=\tfrac a2(9)\).',
                         r'Ratio \(=5:9\). In general it is \((2n-1):n^2\).'],
                  answer=r'5 : 9'),
         ],
         practice=[
             dict(q=r'A body starts from rest and covers 14 m in the 4th second. Its acceleration is',
                  options=['2 m/s²', '3.5 m/s²', '4 m/s²', '7 m/s²'], answer=2, type='numerical',
                  explanation=r'\(s_4=\tfrac a2(7)=14\Rightarrow a=4\) m/s². 3.5 m/s² divides 14 by 4, treating 14 m as the distance in 4 s divided by time. 7 m/s² forgets the factor 1/2.'),
             dict(q=r'From rest with uniform acceleration, the distance in the 5th second divided by the distance in the first 5 seconds is',
                  options=['1/5', '9/25', '5/9', '2/5'], answer=1, type='numerical',
                  explanation=r'\((2n-1)/n^2=9/25\). 1/5 assumes uniform speed. 5/9 is the answer for n = 3.'),
             dict(q=r'A ball is thrown straight up. Ignoring air resistance, the distance it rises in the last second before reaching the top',
                  options=['depends on the launch speed', 'is 10 m', 'is zero', 'is 5 m for any launch speed'], answer=3, type='concept',
                  explanation=r'The last second of the rise is the time-reverse of the first second of a fall from rest: \(\tfrac12g(1)^2=5\) m. It does not depend on u, as long as the flight up lasts at least 1 s. 10 m would be \(g\times1\) s, a speed, not a distance.'),
             dict(q=r'Statement I: \(s_n=u+\tfrac a2(2n-1)\) looks dimensionally inconsistent but is correct. Statement II: \(s_n\) always equals the distance covered in the nth second.',
                  options=ST_OPTS, answer=2, type='statement',
                  explanation=r'Statement I is true: a hidden interval of 1 s fixes the dimensions. Statement II is false: \(s_n\) is displacement, and a reversal inside that second makes the distance larger.'),
         ],
     )),

dict(chapter='linear', after='linear-graphs', id='linear-variable',
     title='Variable acceleration: a(t), a(x) and a(v)',
     intro=r'When acceleration changes, \(v=u+at\) and the other constant-acceleration equations fail. Go back to the definitions \(a=dv/dt\) and \(v=dx/dt\), and use \(a=v\,dv/dx\) when acceleration depends on position.',
     reasoning=r'If a is given as a function of t, integrate \(dv=a\,dt\). If a depends on x, separate \(v\,dv=a\,dx\). If a depends on v, use \(dt=dv/a\) for time or \(dx=v\,dv/a\) for distance. Initial conditions fix the constants of integration.',
     formula=r'a=\frac{dv}{dt}=v\frac{dv}{dx}=\frac{d}{dx}\left(\frac{v^2}{2}\right)',
     symbols='a is acceleration (m/s²), v velocity (m/s), t time (s), x position (m). a = v dv/dx follows from the chain rule; valid for any motion along a line.',
     trap=r'Do not put the final value of a varying acceleration into \(v=u+at\). That treats it as constant all the way and gives a wrong answer.',
     example=r'A particle starts from rest at the origin with \(a=6t\) m/s². Find its velocity and position at \(t=2\) s.',
     solution=r'\(v=\int_0^t6t\,dt=3t^2\), so \(v(2)=12\) m/s. \(x=\int_0^t3t^2dt=t^3\), so \(x(2)=8\) m.',
     question=r'A particle moves so that \(v^2=4x\) (SI units). Its acceleration is',
     options='1 m/s²|2 m/s²|4 m/s²|2√x m/s²', answer=1,
     explanation=r'\(a=\tfrac12\,d(v^2)/dx=\tfrac12\times4=2\) m/s², constant. 4 m/s² forgets the factor 1/2. \(2\sqrt x\) is the velocity, not the acceleration.',
     deep=dict(
         level='exam',
         notes=[
             ('Three cases and how to integrate each', r'''<ol><li><strong>a = f(t):</strong> \(v=u+\int_0^tf(t)\,dt\), then \(x=x_0+\int_0^tv\,dt\).</li>
<li><strong>a = f(x):</strong> \(v\,dv=f(x)\,dx\Rightarrow\tfrac12v^2-\tfrac12u^2=\int_{x_0}^{x}f(x)\,dx\).</li>
<li><strong>a = f(v):</strong> for time, \(\int\dfrac{dv}{f(v)}=t\); for distance, \(\int\dfrac{v\,dv}{f(v)}=x\).</li></ol>
<p>Maximum or minimum velocity occurs where \(a=0\).</p>'''),
             ('Where a = v dv/dx comes from', r'''<p>By the chain rule, \(a=\dfrac{dv}{dt}=\dfrac{dv}{dx}\dfrac{dx}{dt}=v\dfrac{dv}{dx}\). Also \(v\dfrac{dv}{dx}=\dfrac{d}{dx}\left(\tfrac12v^2\right)\). So on a graph of \(v^2\) against \(x\), the slope is \(2a\). On a v–x graph, \(a\) at a point is the velocity times the slope there.</p>'''),
             ('Standard results', r'''<ul><li>\(v=k\sqrt x\) means \(v^2=k^2x\): constant acceleration \(a=k^2/2\).</li>
<li>\(v=kx\) gives \(a=k^2x\): acceleration grows with distance.</li>
<li>\(a=-kv\) (drag proportional to speed): \(v=ue^{-kt}\). The body never quite stops, but its total distance is finite, \(u/k\).</li>
<li>\(a=-kv^2\): \(1/v=1/u+kt\).</li>
<li>Position given as \(t=\alpha\sqrt x+\beta\): rewrite as \(x=\left(\frac{t-\beta}{\alpha}\right)^2\), then differentiate.</li></ul>'''),
         ],
         formulas=[
             dict(title='Retardation proportional to speed', formula=r'a=-kv\ \Rightarrow\ v=ue^{-kt},\qquad x_{\max}=\frac{u}{k}',
                  symbols='k is a positive constant (s⁻¹), u the initial speed (m/s), t time (s), x_max the total distance before the body comes to rest (m).'),
             dict(title='Velocity proportional to √x', formula=r'v=k\sqrt x\ \Rightarrow\ a=\frac{k^2}{2}\ (\text{constant})',
                  symbols='k is a constant (m^½ s⁻¹), x position (m) measured from where v = 0. The motion is uniformly accelerated from rest.'),
         ],
         figure=dict(svg=_fig_vx(), caption='If v falls linearly with x, a = v(dv/dx) is proportional to v. The retardation is largest at the start and fades to zero as the body stops.'),
         traps=[r'For a v–x graph, the slope is \(dv/dx\), not the acceleration. Multiply by \(v\) at that point.',
                r'Maximum velocity occurs where acceleration is zero, not where acceleration is maximum.'],
         exam=r'''<ul><li>"a = (α − βt). Find the maximum velocity" or "velocity when acceleration becomes zero".</li>
<li>"v = β√x. Find the acceleration / displacement as a function of time."</li>
<li>"t = √x + 3. Find the displacement when velocity is zero."</li>
<li>"The v–x graph is a straight line … Find a at x = …" or "which a–x graph is correct".</li>
<li>"A retarding force proportional to velocity acts. Find the maximum distance."</li></ul>''',
         examples=[
             dict(tag='Numerical', q=r'A particle starts from rest at the origin with \(a=(4-2t)\) m/s². Find its maximum velocity and its position at that moment.',
                  steps=[r'\(v=\int_0^t(4-2t)\,dt=4t-t^2\).',
                         r'Velocity is maximum when \(a=0\): \(t=2\) s, giving \(v_{\max}=8-4=4\) m/s.',
                         r'\(x=\int_0^2(4t-t^2)\,dt=\left[2t^2-\tfrac{t^3}{3}\right]_0^2=8-\tfrac83=\tfrac{16}{3}\approx5.3\) m.'],
                  answer=r'4 m/s at t = 2 s, at x ≈ 5.3 m'),
             dict(tag='Numerical', q=r'A particle has \(a=-4x\) m/s² and is momentarily at rest at \(x=2\) m. Find its speed as it passes \(x=0\).',
                  steps=[r'\(v\,dv=-4x\,dx\). Integrate from \(x=2\) (where \(v=0\)) to \(x\).',
                         r'\(\tfrac12v^2=-2x^2+2(2)^2\Rightarrow v^2=4(4-x^2)\).',
                         r'At \(x=0\): \(v^2=16\), so \(v=4\) m/s.'],
                  answer=r'4 m/s'),
             dict(tag='Numerical', q=r'A boat moving at 20 m/s cuts its engine. Water drag gives \(a=-0.5v\) m/s². How far does it glide?',
                  steps=[r'Use \(a=v\,dv/dx\): \(v\,dv/dx=-0.5v\Rightarrow dv/dx=-0.5\).',
                         r'So \(v=20-0.5x\). It stops when \(v=0\): \(x=40\) m.',
                         r'In time, \(v=20e^{-0.5t}\), which never reaches zero exactly. The distance is still finite.'],
                  answer=r'40 m'),
             dict(tag='Graph', q=r'A v–x graph is a straight line from 10 m/s at \(x=0\) to 0 at \(x=20\) m. Find the acceleration at \(x=10\) m.',
                  steps=[r'Slope \(dv/dx=-10/20=-0.5\ \text{s}^{-1}\).',
                         r'At \(x=10\) m, \(v=5\) m/s.',
                         r'\(a=v\,dv/dx=5\times(-0.5)=-2.5\) m/s².'],
                  answer=r'−2.5 m/s²'),
         ],
         practice=[
             dict(q=r'A particle moves with \(v=3x\) (SI units). Its acceleration at \(x=2\) m is',
                  options=['6 m/s²', '9 m/s²', '18 m/s²', '3 m/s²'], answer=2, type='numerical',
                  explanation=r'\(a=v\,dv/dx=(3x)(3)=9x=18\) m/s² at x = 2 m. 3 m/s² is just dv/dx. 6 m/s² is the velocity. 9 m/s² forgets to multiply by x.'),
             dict(q=r'A particle has \(a=2t\) m/s² and starts with \(u=1\) m/s. Its velocity at \(t=3\) s is',
                  options=['19 m/s', '10 m/s', '7 m/s', '9 m/s'], answer=1, type='numerical',
                  explanation=r'\(v=1+\int_0^32t\,dt=1+9=10\) m/s. 19 m/s comes from \(v=u+at\) with the final value a = 6 m/s², which wrongly treats a as constant. 9 m/s forgets the initial velocity.'),
             dict(q=r'The time and position of a particle are related by \(t=\sqrt x+3\) (SI units). Its displacement when its velocity becomes zero is',
                  options=['9 m', '3 m', '0 m', '6 m'], answer=2, type='numerical',
                  explanation=r'\(x=(t-3)^2\), so \(v=2(t-3)\), zero at t = 3 s, where x = 0. 9 m is the value of x at t = 0, not when v = 0. 3 m confuses the time with the position.'),
             dict(q=r'A graph of \(v^2\) against \(x\) is a straight line of slope 6 m/s². The acceleration is',
                  options=['6 m/s²', '3 m/s²', '12 m/s²', '1.5 m/s²'], answer=1, type='graph',
                  explanation=r'\(v^2=u^2+2ax\), so the slope is \(2a=6\) and \(a=3\) m/s², constant. 6 m/s² forgets the factor 2. 12 m/s² doubles instead of halving.'),
         ],
     )),
]
