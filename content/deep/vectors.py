"""Deepening layer for the Vectors chapter. Schema: docs/deepening-schema.md."""
import math

R = str


# ---------- small inline-SVG helpers (local to this module) ----------
def _f(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.')


def _arrow(x1, y1, x2, y2, c='var(--indigo)', w=2.2, h=9, dash=False):
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - h * math.cos(ang), y2 - h * math.sin(ang)
    px, py = -math.sin(ang) * h * 0.45, math.cos(ang) * h * 0.45
    d = ';stroke-dasharray:5 4' if dash else ''
    return (f'<line x1="{_f(x1)}" y1="{_f(y1)}" x2="{_f(bx)}" y2="{_f(by)}" style="stroke:{c};stroke-width:{w}{d}"/>'
            f'<polygon points="{_f(x2)},{_f(y2)} {_f(bx + px)},{_f(by + py)} {_f(bx - px)},{_f(by - py)}" style="fill:{c}"/>')


def _line(x1, y1, x2, y2, c='var(--ink-2)', w=1.4, dash=False):
    d = ';stroke-dasharray:4 4' if dash else ''
    return f'<line x1="{_f(x1)}" y1="{_f(y1)}" x2="{_f(x2)}" y2="{_f(y2)}" style="stroke:{c};stroke-width:{w}{d}"/>'


def _text(x, y, s, c='var(--ink)', size=12, anchor='start', extra=''):
    return f'<text x="{_f(x)}" y="{_f(y)}" font-size="{size}" text-anchor="{anchor}" style="fill:{c}{extra}">{s}</text>'


def _arc(cx, cy, r, a1, a2, c='var(--ink-2)', w=1.2):
    """Arc from math angle a1 to a2 (degrees, counter-clockwise, y up)."""
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
    x2, y2 = cx + r * math.cos(math.radians(a2)), cy - r * math.sin(math.radians(a2))
    large = 1 if (a2 - a1) % 360 > 180 else 0
    return f'<path d="M{_f(x1)} {_f(y1)} A{_f(r)} {_f(r)} 0 {large} 0 {_f(x2)} {_f(y2)}" style="fill:none;stroke:{c};stroke-width:{w}"/>'


def _polar(cx, cy, r, a):
    return cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))


def _svg(w, h, label, *parts):
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}" style="max-width:{int(w * 1.35)}px;margin:0 auto">'
            + ''.join(parts) + '</svg>')


def _sub(base, s):
    return f'{base}<tspan dy="3" font-size="9">{s}</tspan>'


IT = ';font-style:italic;font-weight:600'

# ---------- figures ----------
_ox, _oy = 110, 180
_ax, _ay = _ox + 160, _oy - 120
FIG_COMPONENTS = _svg(
    360, 215, 'Vector A at angle theta above the x-axis with its x and y components drawn along the axes',
    _arrow(_ox - 20, _oy, 340, _oy, 'var(--ink-2)', 1.3, 7), _arrow(_ox, _oy + 18, _ox, 18, 'var(--ink-2)', 1.3, 7),
    _text(334, _oy + 16, 'x', 'var(--ink-2)'), _text(_ox + 8, 26, 'y', 'var(--ink-2)'),
    _line(_ax, _ay, _ax, _oy, dash=True), _line(_ax, _ay, _ox, _ay, dash=True),
    _arrow(_ox, _oy, _ax, _oy, 'var(--teal)', 3), _arrow(_ox, _oy, _ox, _ay, 'var(--coral)', 3),
    _arrow(_ox, _oy, _ax, _ay, 'var(--indigo)', 2.6),
    _arc(_ox, _oy, 34, 0, 36.87), _text(_ox + 40, _oy - 9, 'θ', 'var(--ink-2)', 13),
    _text(_ox + 70, _oy - 70, 'A', 'var(--indigo)', 14, extra=IT),
    _text(_ox + 80, _oy + 22, 'A<tspan dy="3" font-size="9">x</tspan><tspan dy="-3"> = A cos θ</tspan>', 'var(--teal)', 12, 'middle'),
    _text(_ox - 8, _oy - 56, 'A' + '<tspan dy="3" font-size="9">y</tspan><tspan dy="-3"> = A sin θ</tspan>', 'var(--coral)', 12, 'end'),
    _text(_ax + 6, _ay - 6, 'tip of A', 'var(--ink-2)', 11),
)

FIG_DISPLACEMENT = _svg(
    360, 215, 'Position vectors r1 and r2 drawn from the origin and the displacement vector from the first point to the second',
    _arrow(40, 190, 340, 190, 'var(--line-2, #C9CEDA)', 1.2, 7), _arrow(50, 200, 50, 15, 'var(--line-2, #C9CEDA)', 1.2, 7),
    _text(44, 206, 'O', 'var(--ink-2)', 12, 'end'),
    _arrow(50, 190, 205, 165, 'var(--indigo)', 2.6), _arrow(50, 190, 290, 50, 'var(--teal)', 2.6),
    _arrow(205, 165, 290, 50, 'var(--coral)', 2.8),
    f'<circle cx="205" cy="165" r="4" style="fill:var(--ink)"/><circle cx="290" cy="50" r="4" style="fill:var(--ink)"/>',
    _text(212, 180, 'P₁ (x₁, y₁)', 'var(--ink)', 12), _text(298, 46, 'P₂ (x₂, y₂)', 'var(--ink)', 12),
    _text(130, 196, 'r₁', 'var(--indigo)', 14, extra=IT), _text(140, 118, 'r₂', 'var(--teal)', 14, extra=IT),
    _text(256, 116, 'Δr = r₂ − r₁', 'var(--coral)', 13, extra=';font-weight:600'),
)

_px, _py = 40, 150
_bx, _by = _polar(_px, _py, 120, 60)
_rx, _ry = _bx + 200, _by
FIG_PARALLELOGRAM = _svg(
    390, 180, 'Parallelogram law: A along the base, B at angle theta, resultant R along the diagonal, with B cos theta and B sin theta marked',
    _line(_px + 200, _py, _rx, _ry, 'var(--indigo)', 1.3, True), _line(_bx, _by, _rx, _ry, 'var(--teal)', 1.3, True),
    _line(_px + 200, _py, _rx, _py, 'var(--ink-2)', 1.2, True), _line(_rx, _py, _rx, _ry, 'var(--ink-2)', 1.2, True),
    _arrow(_px, _py, _px + 200, _py, 'var(--teal)', 2.8), _arrow(_px, _py, _bx, _by, 'var(--indigo)', 2.8),
    _arrow(_px, _py, _rx, _ry, 'var(--coral)', 3),
    _arc(_px, _py, 26, 0, 60), _text(_px + 22, _py - 26, 'θ', 'var(--ink-2)', 13),
    _arc(_px, _py, 62, 0, math.degrees(math.atan2(_py - _ry, _rx - _px)), 'var(--coral)'),
    _text(_px + 66, _py - 8, 'α', 'var(--coral)', 13),
    _text(_px + 120, _py + 18, 'A', 'var(--teal)', 14, 'middle', IT),
    _text(_bx - 44, _by + 46, 'B', 'var(--indigo)', 14, extra=IT),
    _text(_px + 170, _py - 72, 'R', 'var(--coral)', 14, extra=IT),
    _text(_px + 230, _py + 16, 'B cos θ', 'var(--ink-2)', 11, 'middle'),
    _text(_rx + 6, _py - 46, 'B sin θ', 'var(--ink-2)', 11),
)

_dx, _dy = 50, 150
_tx, _ty = _polar(_dx, _dy, 170, 50)
FIG_PROJECTION = _svg(
    380, 190, 'Projection of A on B: a perpendicular dropped from the tip of A meets B at a distance A cos theta from the common tail',
    _arrow(_dx, _dy, 340, _dy, 'var(--teal)', 2.6), _arrow(_dx, _dy, _tx, _ty, 'var(--indigo)', 2.6),
    _line(_tx, _ty, _tx, _dy, 'var(--ink-2)', 1.3, True),
    f'<rect x="{_f(_tx - 9)}" y="{_dy - 9}" width="9" height="9" style="fill:none;stroke:var(--ink-2);stroke-width:1"/>',
    _line(_dx, _dy + 14, _tx, _dy + 14, 'var(--coral)', 3),
    _line(_dx, _dy + 8, _dx, _dy + 20, 'var(--coral)', 1.5), _line(_tx, _dy + 8, _tx, _dy + 20, 'var(--coral)', 1.5),
    _text((_dx + _tx) / 2, _dy + 32, 'A cos θ = A·B / B', 'var(--coral)', 12, 'middle'),
    _arc(_dx, _dy, 30, 0, 50), _text(_dx + 32, _dy - 12, 'θ', 'var(--ink-2)', 13),
    _text(_tx - 50, _ty + 30, 'A', 'var(--indigo)', 14, extra=IT), _text(330, _dy - 8, 'B', 'var(--teal)', 14, 'end', IT),
)

FIG_CROSS = _svg(
    400, 240, 'A and B in a horizontal plane with the parallelogram they span shaded; A cross B points up out of the plane and B cross A points down',
    '<polygon points="120,150 300,150 370,100 190,100" style="fill:var(--amber-soft);stroke:var(--amber);stroke-width:1"/>',
    _arrow(120, 150, 300, 150, 'var(--teal)', 2.8), _arrow(120, 150, 190, 100, 'var(--indigo)', 2.8),
    _arrow(120, 150, 120, 25, 'var(--coral)', 3), _arrow(120, 150, 120, 228, 'var(--coral)', 1.6, 8, True),
    _text(250, 168, 'A', 'var(--teal)', 14, extra=IT), _text(160, 98, 'B', 'var(--indigo)', 14, extra=IT),
    _text(128, 36, 'A × B', 'var(--coral)', 13, extra=';font-weight:600'),
    _text(128, 226, 'B × A = −A × B', 'var(--coral)', 12),
    _text(250, 128, 'area = |A × B| = AB sin θ', 'var(--amber)', 12, 'middle'),
    _arc(120, 150, 22, 0, 35.5), _text(146, 142, 'θ', 'var(--ink-2)', 12),
    _text(390, 50, 'Curl the fingers of the right hand', 'var(--ink-2)', 11, 'end'),
    _text(390, 65, 'from A toward B: the thumb', 'var(--ink-2)', 11, 'end'),
    _text(390, 80, 'gives the direction of A × B.', 'var(--ink-2)', 11, 'end'),
)

_P = (100, 130)
_F1, _F2 = (90, 0), (-30, -80)
_F3 = (-_F1[0] - _F2[0], -_F1[1] - _F2[1])
_Q = (250, 175)
FIG_TRIANGLE = _svg(
    400, 230, 'Three forces acting at a point (left) redrawn head to tail (right) form a closed triangle, so their resultant is zero',
    _arrow(_P[0], _P[1], _P[0] + _F1[0], _P[1] + _F1[1], 'var(--teal)', 2.6),
    _arrow(_P[0], _P[1], _P[0] + _F2[0], _P[1] + _F2[1], 'var(--indigo)', 2.6),
    _arrow(_P[0], _P[1], _P[0] + _F3[0], _P[1] + _F3[1], 'var(--coral)', 2.6),
    f'<circle cx="{_P[0]}" cy="{_P[1]}" r="3.5" style="fill:var(--ink)"/>',
    _text(_P[0] + 92, _P[1] + 4, 'F₁', 'var(--teal)', 13, extra=IT), _text(_P[0] - 18, _P[1] - 74, 'F₂', 'var(--indigo)', 13, extra=IT),
    _text(_P[0] - 46, _P[1] + 82, 'F₃', 'var(--coral)', 13, extra=IT),
    _text(_P[0], 222, 'forces at one point', 'var(--ink-2)', 11, 'middle'),
    _arrow(_Q[0], _Q[1], _Q[0] + _F1[0], _Q[1] + _F1[1], 'var(--teal)', 2.6),
    _arrow(_Q[0] + _F1[0], _Q[1] + _F1[1], _Q[0] + _F1[0] + _F2[0], _Q[1] + _F1[1] + _F2[1], 'var(--indigo)', 2.6),
    _arrow(_Q[0] + _F1[0] + _F2[0], _Q[1] + _F1[1] + _F2[1], _Q[0], _Q[1], 'var(--coral)', 2.6),
    _text(_Q[0] + 45, _Q[1] + 18, 'F₁', 'var(--teal)', 13, 'middle', IT), _text(_Q[0] + 88, _Q[1] - 44, 'F₂', 'var(--indigo)', 13, extra=IT),
    _text(_Q[0] + 12, _Q[1] - 50, 'F₃', 'var(--coral)', 13, 'end', IT),
    _text(_Q[0] + 45, 222, 'head to tail: triangle closes', 'var(--ink-2)', 11, 'middle'),
)

_K = (200, 125)
_c1 = (_K[0] - 95 / math.tan(math.radians(30)), 30)
_c2 = (_K[0] + 95 / math.tan(math.radians(60)), 30)
FIG_LAMI = _svg(
    400, 225, 'Knot held by two strings at 30 and 60 degrees to the ceiling and loaded by a weight W; angles between the forces are 90, 150 and 120 degrees',
    '<rect x="30" y="18" width="340" height="12" style="fill:var(--surface-2);stroke:var(--ink-2);stroke-width:1"/>',
    _line(_K[0], _K[1], _c1[0], _c1[1], 'var(--ink-2)', 1.5), _line(_K[0], _K[1], _c2[0], _c2[1], 'var(--ink-2)', 1.5),
    _line(_K[0], _K[1], _K[0], 172, 'var(--ink-2)', 1.5),
    '<rect x="180" y="172" width="40" height="30" rx="3" style="fill:var(--water-soft);stroke:var(--water);stroke-width:1.5"/>',
    _text(200, 192, 'W', 'var(--ink)', 12, 'middle'),
    _arrow(_K[0], _K[1], *_polar(_K[0], _K[1], 72, 150), 'var(--teal)', 2.6),
    _arrow(_K[0], _K[1], *_polar(_K[0], _K[1], 72, 60), 'var(--indigo)', 2.6),
    _arrow(_K[0] + 1, _K[1], _K[0] + 1, _K[1] + 44, 'var(--coral)', 2.6),
    _text(118, 92, 'T₁', 'var(--teal)', 13, extra=IT), _text(240, 70, 'T₂', 'var(--indigo)', 13, extra=IT),
    _text(193, 166, 'W', 'var(--coral)', 13, 'end', IT),
    _arc(_K[0], _K[1], 16, 60, 150, 'var(--plum)'), _text(*_polar(_K[0], _K[1] + 4, 28, 105), '90°', 'var(--plum)', 11, 'middle'),
    _arc(_K[0], _K[1], 26, 150, 270, 'var(--plum)'), _text(*_polar(_K[0], _K[1] + 4, 44, 210), '120°', 'var(--plum)', 11, 'middle'),
    _arc(_K[0], _K[1], 36, 270, 420, 'var(--plum)'), _text(*_polar(_K[0], _K[1] + 4, 56, 340), '150°', 'var(--plum)', 11, 'middle'),
    _text(_c1[0] + 30, 46, '30°', 'var(--ink-2)', 11), _text(_c2[0] - 30, 46, '60°', 'var(--ink-2)', 11, 'end'),
)

AR_OPTS = ['Both A and R are true, and R correctly explains A',
           'Both A and R are true, but R does not explain A',
           'A is true but R is false',
           'A is false but R is true']
ST_OPTS = ['Both statements are true', 'Statement I is true, Statement II is false',
           'Statement I is false, Statement II is true', 'Both statements are false']


DEEP = {
    'vectors-components': dict(
        level='basic',
        notes=[
            ('Scalar or vector: the real test', r'''<p>A quantity is a vector only if it has a direction <strong>and</strong> combines by the triangle (or parallelogram) law. Direction alone is not enough.</p>
<ul><li><strong>Vectors:</strong> displacement, velocity, acceleration, force, momentum, impulse, torque, angular momentum, area (its direction is the outward normal), electric field.</li>
<li><strong>Scalars:</strong> distance, speed, mass, time, work, energy, power, pressure, temperature, charge and electric current.</li></ul>
<p>Current flows “in a direction” along a wire, yet two currents meeting at a junction simply add as numbers. They do not obey the triangle law, so current is a scalar. Pressure acts on every surface normally but has no single direction of its own, so it is also a scalar.</p>'''),
            ('Resolving at any angle', r'''<p>A component is the shadow of the vector on an axis. Always ask: “which axis is the angle measured from?”</p>
<ol><li>Angle θ measured from the x-axis: \(A_x = A\cos\theta\), \(A_y = A\sin\theta\).</li>
<li>Angle α measured from the y-axis: \(A_x = A\sin\alpha\), \(A_y = A\cos\alpha\). The cosine always goes with the axis the angle touches.</li>
<li>Component along any line making angle φ with the vector: \(A\cos\varphi\). It is largest (equal to A) for φ = 0, zero for φ = 90° and negative for φ &gt; 90°.</li></ol>
<p>So a component can never be larger in size than the vector itself. Rotating the axes changes the components but never the magnitude \(\sqrt{A_x^2 + A_y^2}\).</p>'''),
            ('Finding direction from components', r'''<p>From the components, \(\tan\theta = A_y/A_x\). A calculator returns an angle between −90° and 90° only, so fix the quadrant from the signs:</p>
<ul><li>(+, +): quadrant I, θ as given.</li><li>(−, +): quadrant II, θ = 180° − reference angle.</li>
<li>(−, −): quadrant III, θ = 180° + reference angle.</li><li>(+, −): quadrant IV, θ = 360° − reference angle.</li></ul>
<p>Example: \((-3, 4)\) has reference angle 53°, so the vector points at 127° from +x.</p>'''),
        ],
        formulas=[
            dict(title='Direction from components', formula=r'\tan\theta=\frac{A_y}{A_x}',
                 symbols='θ is the angle from the +x-axis; Aₓ and Aᵧ are signed components in the same unit. Choose the quadrant from the signs of Aₓ and Aᵧ.'),
            dict(title='Component along any direction', formula=r'A_{\parallel}=A\cos\varphi,\qquad A_{\perp}=A\sin\varphi',
                 symbols='A is the magnitude; φ is the angle between the vector and the chosen line; A∥ lies along the line, A⊥ perpendicular to it, both in the unit of A.'),
        ],
        figure=dict(svg=FIG_COMPONENTS,
                    caption=r'The components are the projections of \(\vec A\) on the axes. The dashed lines drop perpendiculars from the tip; the two components and \(\vec A\) form a right triangle.'),
        traps=[r'Electric current has a magnitude and a sense of flow, but it is a scalar because currents add as numbers at a junction. “Has direction” is not the definition of a vector.',
               r'If the angle is given from the <em>vertical</em>, the horizontal component uses sine. Read where the angle is measured from before writing cos.'],
        exam=r'''<ul><li>“Which of the following is a vector / is not a vector?” (current, pressure, work, impulse, area).</li>
<li>“A force of 20 N acts at 30° with the y-axis. Its x-component is …”</li>
<li>“A vector has components (−5√3, −5). Its direction is …” (quadrant check).</li>
<li>Statement questions: “a component of a vector can be greater than the vector”.</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'A force of 20 N acts in the xy-plane at 30° to the <strong>y-axis</strong>, leaning toward +x. Find its x and y components.',
                 steps=[r'The angle touches the y-axis, so the y-component takes the cosine: \(F_y = 20\cos30^\circ = 10\sqrt3 \approx 17.3\) N.',
                        r'The x-component takes the sine: \(F_x = 20\sin30^\circ = 10\) N.',
                        r'Check: \(\sqrt{10^2 + (10\sqrt3)^2} = \sqrt{400} = 20\) N. The components rebuild the magnitude.'],
                 answer=r'\(F_x = 10\) N, \(F_y = 10\sqrt3 \approx 17.3\) N'),
            dict(tag='Quadrant', q=r'A velocity has components \(v_x = -5\sqrt3\) m/s and \(v_y = -5\) m/s. Find its speed and its direction measured counter-clockwise from +x.',
                 steps=[r'Speed \(= \sqrt{75 + 25} = 10\) m/s.',
                        r'Reference angle: \(\tan^{-1}(5/5\sqrt3) = \tan^{-1}(1/\sqrt3) = 30^\circ\).',
                        r'Both components are negative, so the vector lies in quadrant III: θ = 180° + 30° = 210°.',
                        r'A calculator would give \(\tan^{-1}\!\big((-5)/(-5\sqrt3)\big) = 30^\circ\), which points into quadrant I. That is the wrong direction.'],
                 answer=r'10 m/s at 210° from +x'),
            dict(tag='Concept', q=r'Classify as scalar or vector: electric current, pressure, impulse, area of a flat plate.',
                 steps=[r'Current: scalar. It has a sense of flow but adds algebraically at junctions.',
                        r'Pressure: scalar. The force it produces is normal to whichever surface you choose.',
                        r'Impulse: vector. It equals \(\vec F\Delta t\), along the force.',
                        r'Area: vector. Its direction is along the normal to the plate, which is why flux is written as \(\vec E\cdot\vec A\).'],
                 answer=r'Impulse and area are vectors; current and pressure are scalars'),
        ],
        practice=[
            dict(q=r'Which one of the following is a vector quantity?',
                 options=['Electric current', 'Pressure', 'Impulse', 'Work'], answer=2, type='concept',
                 explanation=r'Impulse \(=\vec F\Delta t\) has the direction of the force and adds by the triangle law. Current has a sense of flow but adds as a number at junctions, so it is a scalar. Pressure and work are scalars too; work is a dot product.'),
            dict(q=r'A vector of magnitude 10 units in the xy-plane makes 120° with the +x-axis. Its components are',
                 options=[r'\((5,\ 5\sqrt3)\)', r'\((-5\sqrt3,\ 5)\)', r'\((5,\ -5\sqrt3)\)', r'\((-5,\ 5\sqrt3)\)'], answer=3, type='numerical',
                 explanation=r'\(A_x = 10\cos120^\circ = -5\) and \(A_y = 10\sin120^\circ = 5\sqrt3\). The vector lies in quadrant II, so x is negative and y is positive. \((5, 5\sqrt3)\) is the 60° vector, and \((-5\sqrt3, 5)\) is the 150° vector.'),
            dict(q=r'Statement I: A rectangular component of a vector can be larger than the vector itself.<br>Statement II: The magnitude of a vector does not change when the coordinate axes are rotated.',
                 options=ST_OPTS, answer=2, type='statement',
                 explanation=r'A component is \(A\cos\varphi\) and \(|\cos\varphi|\le1\), so Statement I is false. The magnitude \(\sqrt{A_x^2+A_y^2}\) is the length of the arrow, which does not depend on how the axes are drawn, so Statement II is true.'),
            dict(q=r'A force has an x-component of 12 N and makes 60° with the x-axis. Its magnitude and y-component are',
                 options=[r'24 N and \(12\sqrt3\) N', r'\(12\sqrt3\) N and 24 N', r'24 N and 12 N', r'\(8\sqrt3\) N and 12 N'], answer=0, type='numerical',
                 explanation=r'\(F\cos60^\circ = 12\) gives F = 24 N. Then \(F_y = 24\sin60^\circ = 12\sqrt3 \approx 20.8\) N. Swapping the two values puts the magnitude smaller than a component, which is impossible.'),
        ],
    ),

    'vectors-addition': dict(
        level='core',
        notes=[
            ('Derivation: magnitude and direction of the resultant', r'''<p>Put \(\vec A\) along the x-axis and let \(\vec B\) make angle θ with it (both drawn from one tail).</p>
<ol><li>Components of the sum: \(R_x = A + B\cos\theta\) and \(R_y = B\sin\theta\).</li>
<li>Square and add: \(R^2 = A^2 + 2AB\cos\theta + B^2\cos^2\theta + B^2\sin^2\theta = A^2 + B^2 + 2AB\cos\theta\).</li>
<li>The angle α of \(\vec R\) with \(\vec A\) follows from \(\tan\alpha = R_y/R_x = \dfrac{B\sin\theta}{A + B\cos\theta}\).</li></ol>
<p>The resultant always leans toward the larger vector. If A = B, it bisects the angle.</p>'''),
            ('Special and limiting cases', r'''<ul><li>θ = 0°: R = A + B (maximum).</li><li>θ = 180°: R = |A − B| (minimum), along the larger vector.</li>
<li>θ = 90°: \(R = \sqrt{A^2+B^2}\).</li>
<li>Equal magnitudes A: \(R = 2A\cos(\theta/2)\). So R = A at 120°, \(R=\sqrt2A\) at 90°, \(R=\sqrt3A\) at 60°.</li>
<li>Always \(|A-B| \le R \le A+B\). Three vectors can add to zero only if each magnitude is no larger than the sum of the other two.</li></ul>
<p>As θ grows from 0° to 180°, R falls steadily from A + B to |A − B|.</p>'''),
            ('Subtraction and the change in a vector', r'''<p>\(\vec A - \vec B = \vec A + (-\vec B)\). Reversing \(\vec B\) changes the angle to 180° − θ, so \(|\vec A-\vec B|^2 = A^2 + B^2 - 2AB\cos\theta\). For equal magnitudes, \(|\vec A-\vec B| = 2A\sin(\theta/2)\).</p>
<p>This is the change in velocity when only the direction turns by θ. It is used again in circular motion and in bouncing-ball impulse questions. A useful consequence: \(|\vec A+\vec B| = |\vec A-\vec B|\) only when \(\cos\theta = 0\), that is, when the vectors are perpendicular.</p>'''),
        ],
        formulas=[
            dict(title='Direction of the resultant', formula=r'\tan\alpha=\frac{B\sin\theta}{A+B\cos\theta}',
                 symbols='α is the angle between R and A; θ is the angle between A and B drawn tail to tail; A and B are magnitudes in the same unit.'),
            dict(title='Two equal vectors', formula=r'|\vec A+\vec B|=2A\cos\frac{\theta}{2},\qquad |\vec A-\vec B|=2A\sin\frac{\theta}{2}',
                 symbols='Valid when |A| = |B| = A; θ is the angle between them (0° to 180°). The sum bisects the angle between the vectors.'),
        ],
        figure=dict(svg=FIG_PARALLELOGRAM,
                    caption=r'Parallelogram law. Extending \(\vec A\) by \(B\cos\theta\) and rising by \(B\sin\theta\) gives the right triangle that leads to \(R^2 = A^2 + B^2 + 2AB\cos\theta\).'),
        traps=[r'The resultant of two vectors can be smaller than either of them. Two 10 N forces at 150° give only about 5.2 N.',
               r'In \(R^2 = A^2 + B^2 + 2AB\cos\theta\), θ is the angle between the vectors drawn <em>tail to tail</em>. If a figure shows them head to tail with an interior angle φ, use θ = 180° − φ.'],
        exam=r'''<ul><li>“The maximum and minimum resultants of two forces are 16 N and 4 N. Find the resultant when they are at 60°.”</li>
<li>“The resultant of two equal vectors equals either vector. The angle between them is …” (120°).</li>
<li>“The resultant is perpendicular to the smaller vector …” (set \(A + B\cos\theta = 0\)).</li>
<li>Possible / impossible resultant values for given magnitudes; three forces that can or cannot give zero resultant.</li></ul>''',
        examples=[
            dict(tag='Ratio', q=r'Two forces have a maximum resultant of 16 N and a minimum resultant of 4 N. Find the resultant when they act at 60° to each other.',
                 steps=[r'A + B = 16 and A − B = 4, so A = 10 N and B = 6 N.',
                        r'\(R^2 = 100 + 36 + 2(10)(6)\cos60^\circ = 136 + 60 = 196\).',
                        r'R = 14 N. Check: 14 lies between 4 and 16, as it must.'],
                 answer=r'14 N'),
            dict(tag='Numerical', q=r'Vectors of magnitude 3 and 5 units make 60° with each other. Find the magnitude of the resultant and its angle with the 3-unit vector.',
                 steps=[r'\(R^2 = 9 + 25 + 2(3)(5)(0.5) = 49\), so R = 7 units.',
                        r'\(\tan\alpha = \dfrac{5\sin60^\circ}{3 + 5\cos60^\circ} = \dfrac{4.33}{5.5} \approx 0.787\).',
                        r'α ≈ 38°. The resultant leans toward the larger (5-unit) vector, since 38° is more than half of 60°.'],
                 answer=r'7 units at about 38° from the 3-unit vector'),
            dict(tag='Assertion–Reason', q=r'Assertion (A): If \(|\vec A+\vec B| = |\vec A-\vec B|\), the vectors are perpendicular.<br>Reason (R): \(|\vec A\pm\vec B|^2 = A^2 + B^2 \pm 2AB\cos\theta\).',
                 steps=[r'Equate the two expressions: \(A^2 + B^2 + 2AB\cos\theta = A^2 + B^2 - 2AB\cos\theta\).',
                        r'This gives \(4AB\cos\theta = 0\). For nonzero vectors, cos θ = 0 and θ = 90°.',
                        r'So A is true, R is true, and R is exactly the reason.'],
                 answer=r'Both true; R correctly explains A'),
        ],
        practice=[
            dict(q=r'The resultant of \(\vec A\) and \(\vec B\) is perpendicular to \(\vec A\), and its magnitude is half that of \(\vec B\). The angle between \(\vec A\) and \(\vec B\) is',
                 options=['120°', '150°', '135°', '60°'], answer=1, type='numerical',
                 explanation=r'Taking A along x, \(R_x = A + B\cos\theta = 0\) and \(R = R_y = B\sin\theta = B/2\). So sin θ = 1/2 and cos θ must be negative, giving θ = 150°. 30° also has sin θ = 1/2 but a positive cosine, which cannot cancel A. 120° would give \(R = (\sqrt3/2)B\).'),
            dict(q=r'Two vectors of equal magnitude A have a resultant of magnitude \(\sqrt3A\). The angle between them is',
                 options=['30°', '90°', '120°', '60°'], answer=3, type='numerical',
                 explanation=r'\(2A\cos(\theta/2) = \sqrt3A\) gives \(\cos(\theta/2) = \sqrt3/2\), so θ/2 = 30° and θ = 60°. At 90° the resultant is \(\sqrt2A\); at 120° it is A.'),
            dict(q=r'Two forces of 5 N and 3 N act on a particle. Which of these can be the magnitude of their resultant? (a) 1 N (b) 2 N (c) 6 N (d) 9 N',
                 options=['(a) and (b) only', '(b) and (c) only', '(c) and (d) only', '(a), (b) and (c)'], answer=1, type='multi',
                 explanation=r'The resultant must lie between 5 − 3 = 2 N and 5 + 3 = 8 N. So 2 N (antiparallel) and 6 N are possible. 1 N is below the minimum and 9 N is above the maximum.'),
            dict(q=r'Two vectors each of magnitude A act at angle θ. Match List I (θ) with List II (resultant).<br>List I: (P) 0° (Q) 60° (R) 90° (S) 120°<br>List II: (1) A (2) \(\sqrt2A\) (3) \(\sqrt3A\) (4) 2A',
                 options=['P-4, Q-3, R-2, S-1', 'P-4, Q-2, R-3, S-1', 'P-1, Q-3, R-2, S-4', 'P-4, Q-3, R-1, S-2'], answer=0, type='match',
                 explanation=r'Use \(R = 2A\cos(\theta/2)\): 0° gives 2A, 60° gives \(\sqrt3A\), 90° gives \(\sqrt2A\), 120° gives A. Swapping 60° and 90° is the common slip; the resultant always shrinks as the angle grows.'),
        ],
    ),

    'vectors-dot': dict(
        level='core',
        notes=[
            ('Properties and the component formula', r'''<ul><li>Commutative: \(\vec A\cdot\vec B = \vec B\cdot\vec A\). Distributive: \(\vec A\cdot(\vec B+\vec C) = \vec A\cdot\vec B + \vec A\cdot\vec C\).</li>
<li>\(\hat i\cdot\hat i = \hat j\cdot\hat j = \hat k\cdot\hat k = 1\) and \(\hat i\cdot\hat j = \hat j\cdot\hat k = \hat k\cdot\hat i = 0\).</li>
<li>\(\vec A\cdot\vec A = A^2\), so a magnitude can always be found as \(\sqrt{\vec A\cdot\vec A}\).</li></ul>
<p>Expanding \((A_x\hat i + A_y\hat j + A_z\hat k)\cdot(B_x\hat i + B_y\hat j + B_z\hat k)\) gives nine terms. Six of them contain a product of different unit vectors and vanish, leaving \(A_xB_x + A_yB_y + A_zB_z\).</p>'''),
            ('Angle, projection and the perpendicular test', r'''<ol><li>Angle: \(\cos\theta = \dfrac{\vec A\cdot\vec B}{AB}\). The sign of the dot product tells you at once whether θ is acute (+), right (0) or obtuse (−).</li>
<li>Scalar projection of \(\vec A\) on \(\vec B\): \(A\cos\theta = \dfrac{\vec A\cdot\vec B}{B}\). Divide by the magnitude of the vector you project <em>onto</em>.</li>
<li>Perpendicular test: set \(\vec A\cdot\vec B = 0\) and solve for the unknown component.</li>
<li>Resultant link: \(|\vec A+\vec B|^2 = (\vec A+\vec B)\cdot(\vec A+\vec B) = A^2 + B^2 + 2\vec A\cdot\vec B\).</li></ol>'''),
            ('Physics written as dot products', r'''<p>Work \(W = \vec F\cdot\vec s\), power \(P = \vec F\cdot\vec v\), flux \(\Phi = \vec E\cdot\vec A\). In each case only the parallel part of one vector matters. A force perpendicular to the motion, such as the tension in a uniformly whirled stone or the normal force on a level road, does zero work.</p>'''),
        ],
        formulas=[
            dict(title='Angle between two vectors', formula=r'\cos\theta=\frac{A_xB_x+A_yB_y+A_zB_z}{AB}',
                 symbols='A and B are magnitudes (nonzero); θ is the angle between the vectors, 0° to 180°.'),
            dict(title='Scalar projection', formula=r'A_{B}=A\cos\theta=\frac{\vec A\cdot\vec B}{B}',
                 symbols='A_B is the signed length of A along B, in the unit of A; B is the magnitude of B (nonzero).'),
            dict(title='Resultant via dot product', formula=r'|\vec A\pm\vec B|^2=A^2+B^2\pm2\,\vec A\cdot\vec B',
                 symbols='A and B are magnitudes; the dot product carries the angle information.'),
        ],
        figure=dict(svg=FIG_PROJECTION,
                    caption=r'The projection of \(\vec A\) on \(\vec B\) is the length \(A\cos\theta\) cut off along \(\vec B\). The dot product is this length multiplied by B.'),
        traps=[r'\(\vec A\cdot\vec A = A^2\), not zero. Only the dot product of <em>perpendicular</em> vectors is zero.',
               r'The projection of A on B is \(\vec A\cdot\vec B/B\), not \(\vec A\cdot\vec B/A\). Dividing by the wrong magnitude gives the projection of B on A instead.'],
        exam=r'''<ul><li>“For what value of a are \(2\hat i + a\hat j + \hat k\) and \(4\hat i - 2\hat j - 2\hat k\) perpendicular?”</li>
<li>“A force \(\vec F\) moves a particle from point P to point Q. Find the work done.”</li>
<li>“The angle between \(\hat i + \hat j + \hat k\) and the z-axis is …” (direction cosine).</li>
<li>“If \(|\vec A| = |\vec B| = 1\) and \(|\vec A + \vec B| = \sqrt3\), find the angle.”</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'Find a so that \(\vec A = 2\hat i + a\hat j + \hat k\) is perpendicular to \(\vec B = 4\hat i - 2\hat j - 2\hat k\).',
                 steps=[r'Perpendicular means \(\vec A\cdot\vec B = 0\).',
                        r'\(\vec A\cdot\vec B = 2(4) + a(-2) + 1(-2) = 6 - 2a\).',
                        r'Set 6 − 2a = 0, so a = 3.'],
                 answer=r'a = 3'),
            dict(tag='Numerical', q=r'A constant force \(\vec F = (3\hat i + 4\hat j - 5\hat k)\) N moves a particle from (1, 0, 2) m to (3, 2, 1) m. Find the work done.',
                 steps=[r'Displacement \(\vec s = (3-1)\hat i + (2-0)\hat j + (1-2)\hat k = 2\hat i + 2\hat j - \hat k\) m.',
                        r'\(W = \vec F\cdot\vec s = 3(2) + 4(2) + (-5)(-1) = 6 + 8 + 5 = 19\) J.',
                        r'The z-parts are both negative, so their product adds positive work. Watch the signs.'],
                 answer=r'19 J'),
            dict(tag='Concept', q=r'Find the angle between \(\vec A = \hat i + \hat j + \hat k\) and the z-axis.',
                 steps=[r'The z-axis direction is \(\hat k\), a unit vector.',
                        r'\(\vec A\cdot\hat k = 1\) and \(|\vec A| = \sqrt3\).',
                        r'\(\cos\theta = 1/\sqrt3\), so \(\theta = \cos^{-1}(1/\sqrt3) \approx 54.7^\circ\). It is <em>not</em> 45°: the body diagonal of a cube is not at 45° to an edge.'],
                 answer=r'\(\cos^{-1}(1/\sqrt3) \approx 54.7^\circ\)'),
        ],
        practice=[
            dict(q=r'A force \(\vec F = (2\hat i + 3\hat j)\) N gives a displacement \(\vec s = (4\hat i - \hat j + 3\hat k)\) m. The work done is',
                 options=['11 J', '5 J', '8 J', '17 J'], answer=1, type='numerical',
                 explanation=r'\(W = 2(4) + 3(-1) + 0(3) = 5\) J. 11 J ignores the negative sign of the y-part. The force has no z-component, so the 3 m along z does no work.'),
            dict(q=r'For two nonzero vectors, \(\vec A\cdot\vec B\) is negative. The angle θ between them satisfies',
                 options=['0° ≤ θ &lt; 90°', 'θ = 90°', '90° &lt; θ ≤ 180°', 'θ = 0° only'], answer=2, type='concept',
                 explanation=r'\(\vec A\cdot\vec B = AB\cos\theta\) and AB &gt; 0, so the sign is the sign of cos θ. Cos θ is negative only for obtuse angles up to 180°. An acute angle gives a positive product and 90° gives zero.'),
            dict(q=r'Unit vectors \(\hat a\) and \(\hat b\) satisfy \(|\hat a + \hat b| = \sqrt3\). The angle between them is',
                 options=['60°', '30°', '90°', '120°'], answer=0, type='numerical',
                 explanation=r'\(|\hat a+\hat b|^2 = 1 + 1 + 2\cos\theta = 3\) gives cos θ = 1/2, so θ = 60°. 120° would give \(|\hat a+\hat b| = 1\), and 90° would give \(\sqrt2\).'),
            dict(q=r'Assertion (A): A body moving in a circle at constant speed has zero work done on it by the centripetal force.<br>Reason (R): The centripetal force is perpendicular to the displacement at every instant, so \(\vec F\cdot d\vec s = 0\).',
                 options=AR_OPTS, answer=0, type='ar',
                 explanation=r'Both are true. Each small displacement is tangential and the force is radial, so every \(\vec F\cdot d\vec s\) term is zero. That is exactly why the total work is zero and the speed stays constant. R therefore explains A.'),
        ],
    ),

    'vectors-cross': dict(
        level='core',
        notes=[
            ('Unit-vector rule and the determinant', r'''<p>Write \(\hat i \to \hat j \to \hat k \to \hat i\) in a circle. Going forward gives +: \(\hat i\times\hat j = \hat k\), \(\hat j\times\hat k = \hat i\), \(\hat k\times\hat i = \hat j\). Going backward gives −. Any unit vector crossed with itself is zero.</p>
<p>The full product is the determinant</p>
\[\vec A\times\vec B=\begin{vmatrix}\hat i&\hat j&\hat k\\A_x&A_y&A_z\\B_x&B_y&B_z\end{vmatrix}=(A_yB_z-A_zB_y)\hat i-(A_xB_z-A_zB_x)\hat j+(A_xB_y-A_yB_x)\hat k\]
<p>Do not forget the minus sign on the middle (\(\hat j\)) term.</p>'''),
            ('Geometric meaning: area and the normal', r'''<ul><li>\(|\vec A\times\vec B| = AB\sin\theta\) is the area of the parallelogram with sides \(\vec A\) and \(\vec B\). Half of it is the area of the triangle they form.</li>
<li>\(\vec A\times\vec B\) is perpendicular to both, so \(\vec A\cdot(\vec A\times\vec B) = 0\) and \(\vec B\cdot(\vec A\times\vec B) = 0\) always.</li>
<li>Unit vector normal to both: \(\hat n = \dfrac{\vec A\times\vec B}{|\vec A\times\vec B|}\). The opposite vector \(-\hat n\) is also normal.</li></ul>'''),
            ('Dot and cross together', r'''<p>Since \(\cos^2\theta + \sin^2\theta = 1\): \((\vec A\cdot\vec B)^2 + |\vec A\times\vec B|^2 = A^2B^2\). Also \(\tan\theta = |\vec A\times\vec B| / (\vec A\cdot\vec B)\).</p>
<ul><li>\(|\vec A\times\vec B| = \vec A\cdot\vec B\) means θ = 45°.</li><li>\(|\vec A\times\vec B| = \sqrt3\,\vec A\cdot\vec B\) means θ = 60°.</li></ul>
<p>Physics that uses the cross product: torque \(\vec\tau = \vec r\times\vec F\), angular momentum \(\vec L = \vec r\times\vec p\), velocity in rotation \(\vec v = \vec\omega\times\vec r\), and the magnetic force \(q\vec v\times\vec B\) in Class 12.</p>'''),
        ],
        formulas=[
            dict(title='Area from the cross product', formula=r'\text{parallelogram}=|\vec A\times\vec B|,\qquad \text{triangle}=\tfrac12|\vec A\times\vec B|',
                 symbols='A and B are the two adjacent sides (as vectors from one corner), in metres; areas are in m².'),
            dict(title='Dot and cross identity', formula=r'(\vec A\cdot\vec B)^2+|\vec A\times\vec B|^2=A^2B^2,\qquad \tan\theta=\frac{|\vec A\times\vec B|}{\vec A\cdot\vec B}',
                 symbols='A and B are magnitudes; θ is the angle between the vectors (0° to 180°).'),
        ],
        figure=dict(svg=FIG_CROSS,
                    caption=r'\(\vec A\times\vec B\) stands perpendicular to the plane of \(\vec A\) and \(\vec B\). Its length equals the shaded parallelogram’s area. Reversing the order flips it to the other side.'),
        traps=[r'The cross product is not associative: \(\hat i\times(\hat i\times\hat j) = \hat i\times\hat k = -\hat j\), but \((\hat i\times\hat i)\times\hat j = 0\).',
               r'The area of the <em>triangle</em> with sides \(\vec A\) and \(\vec B\) is half of \(|\vec A\times\vec B|\). Students often report the parallelogram area instead.'],
        exam=r'''<ul><li>“Find \(\vec A\times\vec B\)” or “a unit vector perpendicular to both \(\vec A\) and \(\vec B\)”.</li>
<li>“If \(|\vec A\times\vec B| = \sqrt3\,\vec A\cdot\vec B\), find θ” and then a follow-up on \(|\vec A + \vec B|\).</li>
<li>“Area of the triangle / parallelogram formed by …”.</li>
<li>Torque from \(\vec r\) and \(\vec F\) in unit-vector form; the value of \((\vec A\times\vec B)\cdot\vec A\).</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'For \(\vec A = 2\hat i + 3\hat j - \hat k\) and \(\vec B = \hat i - \hat j + 2\hat k\), find \(\vec A\times\vec B\) and the area of the parallelogram they span.',
                 steps=[r'\(\hat i\) part: \(A_yB_z - A_zB_y = 3(2) - (-1)(-1) = 6 - 1 = 5\).',
                        r'\(\hat j\) part: \(-(A_xB_z - A_zB_x) = -(2\cdot2 - (-1)(1)) = -5\).',
                        r'\(\hat k\) part: \(A_xB_y - A_yB_x = 2(-1) - 3(1) = -5\).',
                        r'\(\vec A\times\vec B = 5\hat i - 5\hat j - 5\hat k\). Area \(= \sqrt{25+25+25} = 5\sqrt3 \approx 8.66\) square units.',
                        r'Check: \(\vec A\cdot(\vec A\times\vec B) = 10 - 15 + 5 = 0\), as it must be.'],
                 answer=r'\(5\hat i - 5\hat j - 5\hat k\); area \(5\sqrt3\) units²'),
            dict(tag='Ratio', q=r'For two vectors, \(|\vec A\times\vec B| = \sqrt3\,(\vec A\cdot\vec B)\). Find the angle between them and \(|\vec A+\vec B|\).',
                 steps=[r'\(AB\sin\theta = \sqrt3\,AB\cos\theta\), so \(\tan\theta = \sqrt3\) and θ = 60°.',
                        r'\(|\vec A+\vec B|^2 = A^2 + B^2 + 2AB\cos60^\circ = A^2 + B^2 + AB\).'],
                 answer=r'θ = 60°, \(|\vec A+\vec B| = \sqrt{A^2+B^2+AB}\)'),
            dict(tag='Numerical', q=r'A force \(\vec F = (2\hat i + 4\hat j)\) N acts at the point \(\vec r = (3\hat i + \hat j)\) m. Find the torque about the origin.',
                 steps=[r'\(\vec\tau = \vec r\times\vec F\). Only x and y parts exist, so the torque is along \(\hat k\).',
                        r'\(\tau_z = r_xF_y - r_yF_x = 3(4) - 1(2) = 10\).',
                        r'\(\vec\tau = 10\hat k\) N m, out of an xy page drawn with +x right and +y up. Writing \(\vec F\times\vec r\) would give the wrong sign.'],
                 answer=r'\(10\hat k\) N m'),
        ],
        practice=[
            dict(q=r'The area of the triangle whose two sides are \(\vec A = 3\hat i + 4\hat j\) and \(\vec B = -4\hat i + 3\hat j\) (in m) is',
                 options=['25 m²', '5 m²', '12.5 m²', '0'], answer=2, type='numerical',
                 explanation=r'\(\vec A\times\vec B = (3\cdot3 - 4\cdot(-4))\hat k = 25\hat k\). The parallelogram area is 25 m², so the triangle is 12.5 m². 25 m² forgets the half; 0 would need parallel sides, but these two are perpendicular.'),
            dict(q=r'For any two vectors, \((\vec A\times\vec B)\cdot\vec A\) equals',
                 options=[r'\(A^2B\)', r'\(AB\sin\theta\)', r'\(AB\cos\theta\)', '0'], answer=3, type='concept',
                 explanation=r'\(\vec A\times\vec B\) is perpendicular to \(\vec A\), and the dot product of perpendicular vectors is zero. The other options treat the expression as if it kept a component along \(\vec A\).'),
            dict(q=r'Statement I: \(\vec A\times\vec B = \vec B\times\vec A\).<br>Statement II: \(|\vec A\times\vec B| = |\vec B\times\vec A|\).',
                 options=ST_OPTS, answer=2, type='statement',
                 explanation=r'Reversing the order reverses the direction: \(\vec B\times\vec A = -\vec A\times\vec B\). So Statement I is false unless the product is zero. The magnitudes are both \(AB\sin\theta\), so Statement II is true.'),
            dict(q=r'The magnitude of \(\vec A\times\vec B\) equals \(\vec A\cdot\vec B\). The angle between the vectors is',
                 options=['30°', '45°', '60°', '90°'], answer=1, type='numerical',
                 explanation=r'\(AB\sin\theta = AB\cos\theta\) gives tan θ = 1, so θ = 45°. At 90° the dot product is zero while the cross product is AB, so they cannot be equal.'),
        ],
    ),

    'vectors-equilibrium': dict(
        level='core',
        notes=[
            ('Three forces: the closed triangle', r'''<p>When three forces keep a particle in equilibrium, \(\vec F_1 + \vec F_2 + \vec F_3 = 0\). This has three useful consequences.</p>
<ol><li>Drawn head to tail, the three arrows form a closed triangle.</li>
<li>Any one force is equal and opposite to the resultant of the other two: \(\vec F_3 = -(\vec F_1 + \vec F_2)\).</li>
<li>So \(|F_1 - F_2| \le F_3 \le F_1 + F_2\). A set like 2 N, 3 N, 6 N can never be in equilibrium.</li></ol>
<p>Three non-parallel forces in equilibrium on a body must also be coplanar and their lines of action must pass through one point. Otherwise they would produce a net torque.</p>'''),
            ('Choosing the axes', r'''<p>Resolve along directions that remove unknowns. For a block on an incline, take axes along and perpendicular to the slope. For a knot held by two strings, take one axis along a string if you want the other string’s tension directly. The equations are equally valid for any perpendicular pair; a good choice only reduces algebra.</p>'''),
            ('Removing one force', r'''<p>If a particle is in equilibrium under many forces and one force \(\vec F\) is suddenly removed, the rest add up to \(-\vec F\). The particle then accelerates at \(\vec F/m\) in the direction <em>opposite</em> to the removed force. Likewise n equal forces drawn symmetrically from a point (at 360°/n to each other) form a closed regular polygon and sum to zero.</p>'''),
        ],
        formulas=[
            dict(title='Balancing force', formula=r'\vec F_3=-(\vec F_1+\vec F_2),\qquad |F_1-F_2|\le F_3\le F_1+F_2',
                 symbols='F₁, F₂, F₃ are the three forces on the particle (N). Equilibrium is possible only if the inequality holds.'),
        ],
        figure=dict(svg=FIG_TRIANGLE,
                    caption=r'Three forces in equilibrium. Redrawn head to tail they close into a triangle, which is the picture behind \(\sum\vec F = 0\) and behind Lami’s theorem.'),
        traps=[r'If one force F is removed from a body in equilibrium, the net force is F in the <em>opposite</em> direction, not zero and not F in the same direction.',
               r'Equal magnitudes alone do not guarantee balance. Three 10 N forces balance only if they are at 120° to one another.'],
        exam=r'''<ul><li>“Which set of forces can keep a particle in equilibrium?” (triangle inequality).</li>
<li>“A particle is in equilibrium under forces … Find the third force” in î, ĵ, k̂ form.</li>
<li>“A body is in equilibrium under several forces. A force of 10 N acting north is removed. The net force now is …”</li>
<li>A mass pulled aside by a horizontal force: find the force and the string tension.</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'A 2 kg bob hangs by a string. A horizontal force F pulls it aside until the string makes 37° with the vertical, and it rests there. Find F and the tension T (g = 10 m/s², sin 37° = 0.6).',
                 steps=[r'Forces on the bob: weight 20 N down, horizontal F, tension T along the string.',
                        r'Vertical balance: \(T\cos37^\circ = 20\), so T = 20/0.8 = 25 N.',
                        r'Horizontal balance: \(F = T\sin37^\circ = 25 \times 0.6 = 15\) N.',
                        r'Check with the triangle: \(\sqrt{15^2 + 20^2} = 25\). The 3-4-5 triangle closes.'],
                 answer=r'F = 15 N, T = 25 N'),
            dict(tag='Concept', q=r'Which sets of forces can keep a particle in equilibrium? (i) 3, 4, 8 N (ii) 5, 7, 10 N (iii) 6, 6, 12 N.',
                 steps=[r'Test whether the largest force is at most the sum of the other two.',
                        r'(i) 8 &gt; 3 + 4 = 7. Not possible.',
                        r'(ii) 10 ≤ 5 + 7 = 12. Possible.',
                        r'(iii) 12 = 6 + 6. Possible only with the two 6 N forces parallel and the 12 N force opposite: a collinear “flat triangle”.'],
                 answer=r'(ii) and (iii)'),
            dict(tag='Numerical', q=r'A particle is in equilibrium under \(\vec F_1 = (2\hat i - 3\hat j)\) N, \(\vec F_2 = (-\hat i + 5\hat j + \hat k)\) N and a third force. Find the third force and its magnitude.',
                 steps=[r'\(\vec F_1 + \vec F_2 = \hat i + 2\hat j + \hat k\) N.',
                        r'\(\vec F_3 = -(\hat i + 2\hat j + \hat k)\) N.',
                        r'\(|\vec F_3| = \sqrt{1 + 4 + 1} = \sqrt6 \approx 2.45\) N.'],
                 answer=r'\(-\hat i - 2\hat j - \hat k\) N, magnitude \(\sqrt6\) N'),
        ],
        practice=[
            dict(q=r'Which set of three forces <strong>cannot</strong> keep a particle in equilibrium?',
                 options=['4 N, 4 N, 4 N', '2 N, 3 N, 4 N', '2 N, 3 N, 6 N', '5 N, 12 N, 13 N'], answer=2, type='concept',
                 explanation=r'The largest force must not exceed the sum of the other two. 6 &gt; 2 + 3, so the triangle cannot close. Equal forces at 120°, the 2-3-4 triangle and the right-angled 5-12-13 set all close.'),
            dict(q=r'A particle stays in equilibrium under five forces. One of them, 10 N towards north, is removed. The net force on the particle is now',
                 options=['zero', '10 N towards north', '10 N towards south', '40 N towards south'], answer=2, type='concept',
                 explanation=r'The remaining four forces had to cancel the 10 N north force, so their sum is 10 N south. Removing the force does not change them. “Zero” forgets this, and “north” reverses the direction.'),
            dict(q=r'Statement I: For three forces in equilibrium, each one equals the resultant of the other two in magnitude.<br>Statement II: Forces of 4 N and 10 N can be balanced by a third force of 5 N.',
                 options=ST_OPTS, answer=1, type='statement',
                 explanation=r'Statement I is true because \(\vec F_3 = -(\vec F_1 + \vec F_2)\). Statement II is false: the resultant of 4 N and 10 N lies between 6 N and 14 N, so a 5 N force cannot cancel it.'),
            dict(q=r'Forces \(\vec F_1 = (3\hat i + 2\hat j - \hat k)\) N and \(\vec F_2 = (\hat i - 5\hat j + 4\hat k)\) N act on a particle. The force that keeps it in equilibrium is',
                 options=[r'\((4\hat i - 3\hat j + 3\hat k)\) N', r'\((-4\hat i + 3\hat j - 3\hat k)\) N', r'\((-2\hat i - 7\hat j + 5\hat k)\) N', r'\((4\hat i + 3\hat j - 3\hat k)\) N'], answer=1, type='numerical',
                 explanation=r'\(\vec F_1 + \vec F_2 = 4\hat i - 3\hat j + 3\hat k\). The balancing force is its negative, \(-4\hat i + 3\hat j - 3\hat k\). The first option is the resultant itself, which would double the push instead of cancelling it.'),
        ],
    ),
}


NEW_SECTIONS = [
    dict(chapter='vectors', after='vectors-components', id='vectors-unit',
         title='Unit vectors, position and displacement vectors',
         intro=r'A unit vector has magnitude 1 and carries only a direction. Divide any nonzero vector by its own magnitude to get the unit vector along it: \(\hat A = \vec A/A\). The unit vectors \(\hat i\), \(\hat j\), \(\hat k\) point along +x, +y and +z. The position of a point (x, y, z) is the vector \(\vec r = x\hat i + y\hat j + z\hat k\) drawn from the origin.',
         reasoning=r'The displacement from point 1 to point 2 is \(\Delta\vec r = \vec r_2 - \vec r_1\). Position vectors change if you move the origin, but the displacement between two points does not. The magnitude of \(\Delta\vec r\) is the straight-line distance between the points.',
         formula=r'\hat A=\frac{\vec A}{|\vec A|},\qquad \vec r=x\hat i+y\hat j+z\hat k,\qquad \Delta\vec r=(x_2-x_1)\hat i+(y_2-y_1)\hat j+(z_2-z_1)\hat k',
         symbols='Â is a dimensionless unit vector; |A| is the magnitude of A (nonzero); x, y, z are coordinates (m); r is the position vector (m); Δr is displacement (m). Cartesian axes are assumed.',
         trap=r'\(\hat i + \hat j\) is not a unit vector. Its magnitude is \(\sqrt2\), so the unit vector along it is \((\hat i + \hat j)/\sqrt2\).',
         example=r'A particle moves from (1, 2, −1) m to (4, 6, −1) m. Find its displacement vector and the distance between the points.',
         solution=r'\(\Delta\vec r = (4-1)\hat i + (6-2)\hat j + 0\,\hat k = 3\hat i + 4\hat j\) m. Its magnitude is \(\sqrt{9+16} = 5\) m. The unit vector along the displacement is \(0.6\hat i + 0.8\hat j\).',
         question=r'Which of these is a unit vector?',
         options=r'\(\hat i + \hat j\)|\((\hat i + \hat j)/\sqrt2\)|\((\hat i + \hat j)/2\)|\(\sqrt2(\hat i + \hat j)\)', answer=1,
         explanation=r'\(|\hat i + \hat j| = \sqrt2\), so dividing by \(\sqrt2\) gives magnitude 1. Dividing by 2 gives \(1/\sqrt2\), and multiplying by \(\sqrt2\) gives 2.',
         deep=dict(
             level='basic',
             notes=[
                 ('Direction cosines', r'''<p>If \(\vec A\) makes angles α, β, γ with the x, y and z axes, then \(\cos\alpha = A_x/A\), \(\cos\beta = A_y/A\), \(\cos\gamma = A_z/A\). These three numbers are the components of the unit vector \(\hat A\), so</p>
\[\cos^2\alpha+\cos^2\beta+\cos^2\gamma=1\]
<p>This identity is the quick test for “can a vector make these angles with the axes?” For example, 45°, 45°, 45° gives \(3 \times \tfrac12 = \tfrac32 \ne 1\), so no vector does that.</p>'''),
                 ('Building a vector of given size along a direction', r'''<p>To write a vector of magnitude B along \(\vec A\), multiply the unit vector by B: \(\vec B = B\hat A = B\vec A/A\). A 10 N force along \(3\hat i + 4\hat j\) is \(10(3\hat i + 4\hat j)/5 = (6\hat i + 8\hat j)\) N.</p>
<p>In 3D the magnitude is \(A = \sqrt{A_x^2 + A_y^2 + A_z^2}\). Every later chapter (forces, momentum, fields) uses this to switch between “magnitude and direction” and “î, ĵ, k̂ form”.</p>'''),
                 ('Position versus displacement', r'''<ul><li>Position depends on where you put the origin. Displacement does not, because the origin cancels in \(\vec r_2 - \vec r_1\).</li>
<li>Displacement depends only on the end points, not on the path taken. Distance travelled depends on the path.</li>
<li>For a closed path (back to the start), \(\Delta\vec r = 0\) though the distance travelled is not zero.</li></ul>'''),
             ],
             formulas=[
                 dict(title='Magnitude in three dimensions', formula=r'A=\sqrt{A_x^2+A_y^2+A_z^2}',
                      symbols='Aₓ, Aᵧ, A_z are the Cartesian components in the unit of A.'),
                 dict(title='Direction cosines', formula=r'\cos\alpha=\frac{A_x}{A},\ \cos\beta=\frac{A_y}{A},\ \cos\gamma=\frac{A_z}{A},\qquad \cos^2\alpha+\cos^2\beta+\cos^2\gamma=1',
                      symbols='α, β, γ are the angles A makes with +x, +y and +z; A is the magnitude (nonzero).'),
             ],
             figure=dict(svg=FIG_DISPLACEMENT,
                         caption=r'Position vectors start at the origin. The displacement from P₁ to P₂ completes the triangle: \(\vec r_1 + \Delta\vec r = \vec r_2\).'),
             traps=[r'A unit vector has no unit. \(\hat F\) of a force in newtons is a pure number; the newtons stay with the magnitude.',
                    r'The direction cosines are \(A_x/A\), not \(A_x/(A_x + A_y + A_z)\). Divide by the magnitude, not by the sum of components.'],
             exam=r'''<ul><li>“Find the unit vector along \(6\hat i - 8\hat k\).”</li>
<li>“A vector makes 60° with x and 60° with y. Its angle with z is …”</li>
<li>“Write a force of 15 N along \(2\hat i - \hat j + 2\hat k\).”</li>
<li>“A particle goes from A(2, 3, 1) to B(5, −1, 1). Find the displacement / its magnitude.”</li></ul>''',
             examples=[
                 dict(tag='Numerical', q=r'Find the direction cosines of \(\vec A = 2\hat i + \hat j - 2\hat k\).',
                      steps=[r'\(A = \sqrt{4 + 1 + 4} = 3\).',
                             r'\(\cos\alpha = 2/3\), \(\cos\beta = 1/3\), \(\cos\gamma = -2/3\).',
                             r'Check: \(4/9 + 1/9 + 4/9 = 1\). The negative value means the angle with +z is obtuse (about 132°).'],
                      answer=r'\(2/3,\ 1/3,\ -2/3\)'),
                 dict(tag='Numerical', q=r'Write a force of magnitude 15 N acting along \(2\hat i - \hat j + 2\hat k\).',
                      steps=[r'Magnitude of the direction vector: \(\sqrt{4 + 1 + 4} = 3\).',
                             r'Unit vector: \((2\hat i - \hat j + 2\hat k)/3\).',
                             r'\(\vec F = 15 \times (2\hat i - \hat j + 2\hat k)/3 = (10\hat i - 5\hat j + 10\hat k)\) N. Check: \(\sqrt{100+25+100} = 15\).'],
                      answer=r'\((10\hat i - 5\hat j + 10\hat k)\) N'),
                 dict(tag='Concept', q=r'Can a vector make angles of 45° with all three coordinate axes?',
                      steps=[r'Any direction must satisfy \(\cos^2\alpha + \cos^2\beta + \cos^2\gamma = 1\).',
                             r'With all three at 45°: \(3 \times (1/\sqrt2)^2 = 3/2\).',
                             r'3/2 ≠ 1, so no such vector exists. The equal-angle direction \(\hat i + \hat j + \hat k\) makes about 54.7° with each axis.'],
                      answer=r'No; equal angles must be 54.7° each'),
             ],
             practice=[
                 dict(q=r'The unit vector along \(\vec A = 6\hat i - 8\hat k\) is',
                      options=[r'\(0.6\hat i - 0.8\hat k\)', r'\(6\hat i - 8\hat k\)', r'\(0.6\hat i + 0.8\hat k\)', r'\((6\hat i - 8\hat k)/14\)'], answer=0, type='numerical',
                      explanation=r'\(|\vec A| = \sqrt{36 + 64} = 10\), so \(\hat A = 0.6\hat i - 0.8\hat k\). Dividing by 14 (the sum of the numbers) does not give magnitude 1, and the sign of the k̂ part must stay negative.'),
                 dict(q=r'A vector makes 60° with the x-axis and 60° with the y-axis. The angle it makes with the z-axis is',
                      options=['30°', '60°', '90°', '45°'], answer=3, type='numerical',
                      explanation=r'\(\cos^2\gamma = 1 - \tfrac14 - \tfrac14 = \tfrac12\), so cos γ = \(1/\sqrt2\) and γ = 45° (or 135°). 60° would make the sum 3/4, not 1.'),
                 dict(q=r'A particle moves from A(2, 3, 1) m to B(5, −1, 1) m. The magnitude of its displacement is',
                      options=['7 m', '5 m', '√13 m', '25 m'], answer=1, type='numerical',
                      explanation=r'\(\Delta\vec r = 3\hat i - 4\hat j + 0\hat k\), so the magnitude is \(\sqrt{9+16} = 5\) m. 7 m adds the components as numbers; 25 m forgets the square root.'),
                 dict(q=r'Statement I: The position vector of a point depends on the choice of origin.<br>Statement II: The displacement between two points depends on the choice of origin.',
                      options=ST_OPTS, answer=1, type='statement',
                      explanation=r'Moving the origin changes every position vector, so Statement I is true. In \(\vec r_2 - \vec r_1\) the shift of origin cancels, so displacement is independent of the origin and Statement II is false.'),
             ],
         )),

    dict(chapter='vectors', after='vectors-equilibrium', id='vectors-lami',
         title='Lami’s theorem and three-force equilibrium',
         intro=r'When a particle or a knot is in equilibrium under exactly three coplanar, concurrent forces, each force is proportional to the sine of the angle between the other two. This is Lami’s theorem. It is the fastest route for a weight hung from two strings.',
         reasoning=r'The three forces form a closed triangle. Each interior angle of that triangle is 180° minus the angle between two of the forces, and \(\sin(180^\circ - x) = \sin x\). The sine rule for the triangle therefore becomes Lami’s theorem. The three angles between the forces add up to 360°.',
         formula=r'\frac{F_1}{\sin\alpha}=\frac{F_2}{\sin\beta}=\frac{F_3}{\sin\gamma}',
         symbols='F₁, F₂, F₃ are the force magnitudes (N); α is the angle between F₂ and F₃, β between F₃ and F₁, γ between F₁ and F₂, each measured between the force arrows drawn from the common point; α + β + γ = 360°. Exactly three concurrent coplanar forces in equilibrium.',
         trap=r'Pair each force with the angle <em>between the other two</em>, not with the angle the force itself makes with the horizontal.',
         example=r'A 100 N weight hangs from a knot held by two strings that make 30° and 60° with the horizontal ceiling. Find both tensions.',
         solution=r'The angle between the strings is 180° − 30° − 60° = 90°. The angle between the 30° string and the weight is 120°, and between the 60° string and the weight it is 150°. Lami: \(T_1/\sin150^\circ = T_2/\sin120^\circ = 100/\sin90^\circ\). So \(T_1 = 50\) N (30° string) and \(T_2 = 50\sqrt3 \approx 86.6\) N (60° string). The steeper string carries more of the load.',
         question=r'Three forces keep a knot in equilibrium. The angles between pairs of them are 90°, 135° and 135°. If F₁ is the force opposite the 90° angle, the ratio F₁ : F₂ : F₃ is',
         options=r'1 : 1 : 1|√2 : 1 : 1|1 : √2 : √2|2 : 1 : 1', answer=1,
         explanation=r'Lami gives \(F_1/\sin90^\circ = F_2/\sin135^\circ = F_3/\sin135^\circ\), so the ratio is \(1 : 1/\sqrt2 : 1/\sqrt2 = \sqrt2 : 1 : 1\). The force opposite the largest sine is the largest. 1 : √2 : √2 inverts this.',
         deep=dict(
             level='exam',
             notes=[
                 ('Derivation from the triangle of forces', r'''<ol><li>Draw \(\vec F_1\), \(\vec F_2\), \(\vec F_3\) head to tail. Equilibrium means the triangle closes.</li>
<li>If α is the angle between \(\vec F_2\) and \(\vec F_3\) at the knot, the interior angle of the triangle opposite \(F_1\) is 180° − α.</li>
<li>Sine rule: \(\dfrac{F_1}{\sin(180^\circ-\alpha)} = \dfrac{F_2}{\sin(180^\circ-\beta)} = \dfrac{F_3}{\sin(180^\circ-\gamma)}\).</li>
<li>Because \(\sin(180^\circ - x) = \sin x\), this is Lami’s theorem.</li></ol>
<p>The largest force is the one opposite the angle whose sine is largest, which is the angle closest to 90°.</p>'''),
                 ('Symmetric strings and the “taut rope” limit', r'''<p>If a weight W hangs from the middle of a string and each half makes angle θ with the <em>vertical</em>, the vertical parts give \(2T\cos\theta = W\), so</p>
\[T=\frac{W}{2\cos\theta}\]
<p>At θ = 0 each half carries W/2. At θ = 60°, each tension equals W. As the string approaches horizontal (θ → 90°), T grows without limit. That is why a washing line or a power cable always sags: no finite tension can make it perfectly straight with a load on it.</p>'''),
                 ('Lami or components?', r'''<p>Use Lami when there are exactly three forces and the angles between them are easy to read. Use components when there are four or more forces, or when the angles are given with different reference lines. Both methods must give the same answer, so one can check the other.</p>'''),
             ],
             formulas=[
                 dict(title='Weight hung from the middle of a string', formula=r'T=\frac{W}{2\cos\theta}',
                      symbols='T is the tension in each half (N); W is the hanging weight (N); θ is the angle each half makes with the vertical. Light string, symmetric hanging, equilibrium.'),
             ],
             figure=dict(svg=FIG_LAMI,
                         caption=r'Forces on the knot: T₁ (30° string), T₂ (60° string) and W. The angles between the force arrows are 90°, 150° and 120°; they add to 360°.'),
             traps=[r'Lami’s theorem needs exactly three forces meeting at a point. With a fourth force (say a horizontal push on the knot), resolve into components instead.',
                    r'In the symmetric-string formula, θ is measured from the vertical. If the angle is given with the horizontal ceiling, use \(T = W/(2\sin\theta)\).'],
             exam=r'''<ul><li>“A weight hangs from two strings at angles … with the ceiling. Find the tensions.”</li>
<li>“Three forces in equilibrium make angles … with each other. Find their ratio.”</li>
<li>“Why can a horizontal rope never be pulled perfectly straight with a load in the middle?” (assertion–reason).</li>
<li>One string horizontal, the other inclined: find both tensions.</li></ul>''',
             examples=[
                 dict(tag='Numerical', q=r'A 10 kg picture hangs from a wire over a nail. Each half of the wire makes 60° with the vertical. Find the tension (g = 10 m/s²).',
                      steps=[r'W = 100 N. Each half supplies an upward part \(T\cos60^\circ\).',
                             r'\(2T\cos60^\circ = 100\), so \(T = 100/(2 \times 0.5) = 100\) N.',
                             r'Each half carries the full weight. A shorter wire (larger angle) would make the tension even bigger.'],
                      answer=r'100 N in each half'),
                 dict(tag='Numerical', q=r'A 40 N weight hangs from a knot. One string from the knot is horizontal; the other goes up to the ceiling at 30° above the horizontal. Find both tensions.',
                      steps=[r'Let T₁ be the inclined string and T₂ the horizontal one.',
                             r'Vertical: \(T_1\sin30^\circ = 40\), so T₁ = 80 N.',
                             r'Horizontal: \(T_2 = T_1\cos30^\circ = 80 \times 0.866 = 40\sqrt3 \approx 69.3\) N.',
                             r'Lami check: the angles are 90° (T₂ to W), 120° (T₁ to W) and 150° (T₁ to T₂). \(W/\sin150^\circ = 80 = T_1/\sin90^\circ\). It agrees.'],
                      answer=r'Inclined string 80 N, horizontal string \(40\sqrt3 \approx 69.3\) N'),
                 dict(tag='Assertion–Reason', q=r'Assertion (A): A rope stretched perfectly horizontally cannot support a weight hung at its middle.<br>Reason (R): The two halves can push up only through their vertical components, \(2T\sin\theta\), which is zero for a horizontal rope at any finite T.',
                      steps=[r'With the rope at angle θ to the horizontal, equilibrium needs \(2T\sin\theta = W\).',
                             r'For θ = 0, \(2T\sin\theta = 0\) for any finite tension, so it cannot equal W.',
                             r'So the rope must sag. A is true, R is true, and R explains A.'],
                      answer=r'Both true; R correctly explains A'),
             ],
             practice=[
                 dict(q=r'A 60 N weight hangs from a knot held by two strings that make 37° and 53° with the <strong>vertical</strong>. The tensions in the 37° string and the 53° string are (sin 37° = 0.6)',
                      options=['48 N and 36 N', '36 N and 48 N', '30 N and 30√3 N', '60 N and 60 N'], answer=0, type='numerical',
                      explanation=r'The strings are at 90° to each other. Lami (or components) gives T(37°) = W cos 37° = 48 N and T(53°) = W cos 53° = 36 N. Check: horizontal parts 48 × 0.6 = 36 × 0.8 = 28.8 N; vertical parts 38.4 + 21.6 = 60 N. The string nearer the vertical carries more, so swapping the values is wrong.'),
                 dict(q=r'A weight hangs from the middle of a light string tied between two hooks. As the hooks are moved further apart (string still not breaking), the tension in the string',
                      options=['decreases', 'stays the same', 'first decreases, then increases', 'increases'], answer=3, type='concept',
                      explanation=r'\(T = W/(2\cos\theta)\) with θ from the vertical. Moving the hooks apart increases θ, which decreases cos θ and increases T. The weight is fixed, but each half must now pull more sideways to supply the same upward force.'),
                 dict(q=r'Three forces of equal magnitude 10 N keep a particle in equilibrium. The angle between any two of them is',
                      options=['60°', '120°', '90°', '180°'], answer=1, type='numerical',
                      explanation=r'Equal forces need equal sines in Lami, and the angles must add to 360°, so each is 120°. Equivalently, the triangle of forces is equilateral. 60° is the interior angle of that triangle, not the angle between the force arrows.'),
                 dict(q=r'Statement I: Lami’s theorem can be applied to any number of concurrent forces in equilibrium.<br>Statement II: In Lami’s theorem each force is divided by the sine of the angle between the other two forces.',
                      options=ST_OPTS, answer=2, type='statement',
                      explanation=r'Lami’s theorem comes from the sine rule of a <em>triangle</em>, so it holds only for exactly three forces. Statement I is false. Statement II correctly states how the theorem pairs forces with angles.'),
             ],
         )),
]
