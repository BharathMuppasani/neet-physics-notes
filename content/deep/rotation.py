"""Deepening layer: System of Particles & Rotational Motion.

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


# Figure: disc with a circular hole
FIG_HOLE = ('<svg viewBox="0 0 360 220" role="img" aria-label="Uniform disc of radius R with a hole of radius R/2 cut out touching its rim; the centre of mass shifts R/6 away from the hole">'
            + '<circle cx="150" cy="110" r="80" style="fill:var(--water-soft);stroke:var(--water);stroke-width:1.6"/>'
            + '<circle cx="190" cy="110" r="40" style="fill:var(--surface);stroke:var(--water);stroke-width:1.4;stroke-dasharray:4 3"/>'
            + _line(60, 110, 240, 110, 'var(--muted)', 1, '3 3')
            + '<circle cx="150" cy="110" r="3.5" style="fill:var(--ink-2)"/>' + _t(150, 128, 'O', 12, anchor='middle')
            + '<circle cx="190" cy="110" r="3" style="fill:var(--muted)"/>' + _t(190, 100, 'hole centre', 10, 'var(--muted)', 'middle')
            + f'<circle cx="{150 - 80 / 6:.1f}" cy="110" r="5" style="fill:var(--coral)"/>'
            + _t(150 - 80 / 6, 96, 'CM', 12, 'var(--coral)', 'middle', 'bold')
            + _line(150 - 80 / 6, 150, 150, 150, 'var(--coral)', 1.4) + _t(143, 165, 'R/6', 11, 'var(--coral)', 'middle')
            + _line(150, 72, 190, 72, 'var(--ink-2)', 1) + _t(170, 66, 'R/2', 11, anchor='middle')
            + _t(255, 60, 'Removed mass M/4', 11, 'var(--ink-2)') + _t(255, 76, 'at distance R/2', 11, 'var(--ink-2)')
            + _t(255, 150, 'x = −(M/4)(R/2)', 11, 'var(--coral)') + _t(270, 166, '÷ (3M/4) = −R/6', 11, 'var(--coral)')
            + '</svg>')

# Figure: torque and lever arm
_O = (70, 170)
_P = (230, 110)
_F_ang = math.radians(-115)  # force direction (screen coords)
_Fx, _Fy = math.cos(_F_ang), math.sin(_F_ang)
_t0 = -1.6
_A = (_P[0] + _t0 * 100 * _Fx, _P[1] + _t0 * 100 * _Fy)
# foot of perpendicular from O onto the line of action
_s = ((_O[0] - _P[0]) * _Fx + (_O[1] - _P[1]) * _Fy)
_foot = (_P[0] + _s * _Fx, _P[1] + _s * _Fy)
FIG_TORQUE = ('<svg viewBox="0 0 360 230" role="img" aria-label="Torque about point O: position vector r to the point where force F acts, the line of action of F, and the perpendicular distance from O to that line">'
              + _line(_A[0], _A[1], _P[0] - 1.0 * 100 * _Fx, _P[1] - 1.0 * 100 * _Fy, 'var(--muted)', 1, '5 4')
              + _arrow(_O[0], _O[1], _P[0], _P[1], 'var(--indigo)') + _t((_O[0] + _P[0]) / 2 - 4, (_O[1] + _P[1]) / 2 - 8, 'r', 13, 'var(--indigo)', 'middle', 'bold')
              + _arrow(_P[0], _P[1], _P[0] + 80 * _Fx, _P[1] + 80 * _Fy, 'var(--coral)') + _t(_P[0] + 80 * _Fx - 10, _P[1] + 80 * _Fy + 4, 'F', 13, 'var(--coral)', 'end', 'bold')
              + _line(_O[0], _O[1], _foot[0], _foot[1], 'var(--green)', 2)
              + _t((_O[0] + _foot[0]) / 2 + 8, (_O[1] + _foot[1]) / 2 + 14, _sub('d', '⊥', ' = r sinθ'), 12, 'var(--green)')
              + f'<circle cx="{_O[0]}" cy="{_O[1]}" r="4" style="fill:var(--ink-2)"/>' + _t(_O[0] - 8, _O[1] + 16, 'O', 12, anchor='end')
              + f'<circle cx="{_P[0]}" cy="{_P[1]}" r="3.5" style="fill:var(--coral)"/>' + _t(_P[0] + 8, _P[1] + 14, 'P', 12)
              + _t(200, 215, 'line of action of F', 11, 'var(--muted)')
              + _t(20, 24, _sub('τ = rF sinθ = F × d', '⊥', ''), 13, weight='bold')
              + '</svg>')

# Figure: ladder against a smooth wall
_fx, _fy, _tx, _ty = 180, 200, 300, 40
_mx, _my = (_fx + _tx) / 2, (_fy + _ty) / 2
FIG_LADDER = ('<svg viewBox="0 0 380 240" role="img" aria-label="Ladder leaning on a smooth wall and rough floor with its weight at the middle, a horizontal wall reaction at the top, and normal force and friction toward the wall at the foot">'
              + '<rect x="300" y="20" width="16" height="180" style="fill:var(--surface-2);stroke:var(--ink-2)"/>'
              + _line(40, 200, 316, 200, 'var(--ink-2)', 2)
              + _line(_fx, _fy, _tx, _ty, 'var(--amber)', 6)
              + '<path d="M215 200 A35 35 0 0 0 201 172" style="fill:none;stroke:var(--ink-2);stroke-width:1.2"/>' + _t(222, 190, 'θ', 12)
              + _arrow(_mx, _my, _mx, _my + 70, 'var(--ink-2)') + _t(_mx + 6, _my + 64, 'mg', 12)
              + _arrow(_tx, _ty, _tx - 70, _ty, 'var(--indigo)') + _t(_tx - 74, _ty + 4, _sub('N', '2', ' (smooth wall)'), 12, 'var(--indigo)', 'end')
              + _arrow(_fx, _fy, _fx, _fy - 80, 'var(--indigo)') + _t(_fx - 6, _fy - 70, _sub('N', '1', ''), 12, 'var(--indigo)', 'end')
              + _arrow(_fx - 70, _fy - 8, _fx - 2, _fy - 8, 'var(--coral)') + _t(_fx - 72, _fy - 14, 'f (toward wall)', 11, 'var(--coral)', 'end')
              + _t(20, 228, _sub('N', '1', ' = mg,  f = N') + _sub('', '2', ' = mg/(2 tanθ)'), 12)
              + '</svg>')

# Figure: axis theorems on a disc (face-on)
FIG_AXES = ('<svg viewBox="0 0 380 240" role="img" aria-label="A flat disc in the x y plane with z axis out of the page, showing the perpendicular axis theorem and a tangent axis parallel to the y axis for the parallel axis theorem">'
            + '<circle cx="150" cy="120" r="80" style="fill:var(--water-soft);stroke:var(--water);stroke-width:1.6"/>'
            + _arrow(50, 120, 260, 120, 'var(--ink-2)', 1.6) + _t(262, 135, 'x', 13)
            + _arrow(150, 220, 150, 20, 'var(--ink-2)', 1.6) + _t(158, 26, 'y', 13)
            + '<circle cx="150" cy="120" r="8" style="fill:none;stroke:var(--coral);stroke-width:1.6"/><circle cx="150" cy="120" r="2.5" style="fill:var(--coral)"/>'
            + _t(136, 112, 'z (out of page)', 11, 'var(--coral)', 'end')
            + _line(230, 25, 230, 215, 'var(--green)', 2, '6 4') + _t(236, 60, 'tangent axis', 11, 'var(--green)')
            + _line(150, 200, 230, 200, 'var(--green)', 1.2) + _t(190, 214, 'd = R', 11, 'var(--green)', 'middle')
            + _t(262, 160, _sub('I', 'z', ' = I') + _sub('', 'x', ' + I') + _sub('', 'y', ''), 12, 'var(--coral)')
            + _t(262, 178, 'so I(diameter) = MR²/4', 11, 'var(--coral)')
            + _t(262, 200, _sub('I', 'tangent', ' = I') + _sub('', 'y', ' + MR²'), 12, 'var(--green)')
            + _t(262, 218, '= 5MR²/4', 11, 'var(--green)')
            + '</svg>')

# Figure: velocities of points on a rolling wheel
_wx, _wy, _wr = 170, 120, 70
FIG_ROLL = ('<svg viewBox="0 0 400 230" role="img" aria-label="Rolling wheel: contact point at rest, centre moving at v, top at 2v, and points at the centre level moving at root 2 v at 45 degrees">'
            + _line(20, _wy + _wr, 380, _wy + _wr, 'var(--ink-2)', 2)
            + f'<circle cx="{_wx}" cy="{_wy}" r="{_wr}" style="fill:var(--surface-2);stroke:var(--ink-2);stroke-width:1.6"/>'
            + _line(_wx, _wy + _wr, _wx, _wy - _wr, 'var(--muted)', 1, '3 3')
            + _line(_wx, _wy + _wr, _wx + _wr, _wy, 'var(--muted)', 1, '3 3') + _line(_wx, _wy + _wr, _wx - _wr, _wy, 'var(--muted)', 1, '3 3')
            + _arrow(_wx, _wy, _wx + 50, _wy, 'var(--indigo)') + _t(_wx + 25, _wy - 8, 'v', 13, 'var(--indigo)', 'middle', 'bold')
            + _arrow(_wx, _wy - _wr, _wx + 100, _wy - _wr, 'var(--coral)') + _t(_wx + 104, _wy - _wr + 4, '2v (top)', 12, 'var(--coral)', weight='bold')
            + _arrow(_wx + _wr, _wy, _wx + _wr + 35, _wy + 35, 'var(--green)') + _t(_wx + _wr + 40, _wy + 40, '√2 v', 12, 'var(--green)', weight='bold')
            + _arrow(_wx - _wr, _wy, _wx - _wr + 35, _wy - 35, 'var(--green)') + _t(_wx - _wr - 4, _wy - 30, '√2 v', 12, 'var(--green)', 'end', weight='bold')
            + f'<circle cx="{_wx}" cy="{_wy + _wr}" r="4.5" style="fill:var(--ink-2)"/>' + _t(_wx + 8, _wy + _wr + 18, 'P: contact point, v = 0', 11)
            + _t(20, 22, 'Each point moves as if rotating about P with ω = v/R:', 11, 'var(--muted)')
            + _t(20, 38, 'speed = ω × (distance from P), direction ⊥ to the line from P', 11, 'var(--muted)')
            + '</svg>')

# Figure: body rolling down an incline (θ = 30°)
_c, _s30 = math.cos(math.radians(30)), 0.5
_ppx, _ppy = 170, 190 - 130 * math.tan(math.radians(30))   # contact point on the slope (x = 170)
_rr = 34
_ccx, _ccy = _ppx - _s30 * _rr, _ppy - _c * _rr            # centre = contact + R × outward normal
FIG_INCL = ('<svg viewBox="0 0 380 240" role="img" aria-label="Ball rolling down a rough incline: weight from the centre, normal force and static friction up the slope at the contact point, acceleration down the slope">'
            + f'<polygon points="40,190 330,190 330,{190 - 290 * math.tan(math.radians(30)):.1f}" style="fill:var(--surface-2);stroke:var(--ink-2);stroke-width:1.5"/>'
            + f'<circle cx="{_ccx:.1f}" cy="{_ccy:.1f}" r="{_rr}" style="fill:var(--water-soft);stroke:var(--water);stroke-width:1.6"/>'
            + f'<circle cx="{_ccx:.1f}" cy="{_ccy:.1f}" r="3" style="fill:var(--ink-2)"/>'
            + _arrow(_ccx, _ccy, _ccx, _ccy + 75, 'var(--ink-2)') + _t(_ccx + 6, _ccy + 72, 'Mg', 12)
            + _arrow(_ppx, _ppy, _ppx - _s30 * 100, _ppy - _c * 100, 'var(--indigo)') + _t(_ppx - _s30 * 100 - 6, _ppy - _c * 100, 'N', 13, 'var(--indigo)', 'end', 'bold')
            + _arrow(_ppx, _ppy, _ppx + _c * 55, _ppy - _s30 * 55, 'var(--coral)') + _t(_ppx + _c * 55 + 4, _ppy - _s30 * 55 - 4, 'f (static, up the slope)', 11, 'var(--coral)')
            + _arrow(_ccx - _c * 20, _ccy + _s30 * 20 - 46, _ccx - _c * 75, _ccy + _s30 * 75 - 46, 'var(--green)', 1.8, 8) + _t(_ccx - _c * 80 - 2, _ccy + _s30 * 80 - 46, 'a', 13, 'var(--green)', 'end', 'bold')
            + '<path d="M90 190 A50 50 0 0 0 83.3 165" style="fill:none;stroke:var(--ink-2);stroke-width:1.2"/>' + _t(98, 182, 'θ', 13)
            + _t(20, 222, 'Friction gives the torque fR that spins the body; it does no work in pure rolling.', 11, 'var(--muted)')
            + '</svg>')


DEEP = {
'rotation-centre': dict(
    level='core',
    notes=[
        ('Centre of mass of continuous bodies', r'''<p>For a continuous body, replace the sum by an integral: \(X=\dfrac{1}{M}\int x\,dm\). Write dm in terms of a coordinate (dm = λ dx for a rod, σ dA for a sheet) and integrate.</p>
<p><strong>Example: non-uniform rod.</strong> A rod of length L has linear density λ = kx (heavier toward x = L). M = ∫₀ᴸ kx dx = kL²/2 and ∫x dm = ∫₀ᴸ kx² dx = kL³/3, so X = 2L/3. The CM moves toward the heavier end.</p>
<p>Standard results (measured along the symmetry axis) are collected in the formula card. For any uniform body with a symmetry axis or centre, the CM lies on it.</p>'''),
        ('Bodies with a piece removed', r'''<p>Treat the removed piece as a "negative mass". If the full body has mass M₁ with CM at x₁, and the removed piece has mass M₂ with CM at x₂, the remainder has</p>
<p>\[X=\frac{M_1x_1-M_2x_2}{M_1-M_2}.\]</p>
<p>For a uniform plate, mass is proportional to area. A disc of radius R with a hole of radius R/2 touching its rim: the hole has ¼ of the mass, centred R/2 from O. The remainder’s CM is at −(¼ × R/2)/(¾) = −R/6, on the side away from the hole (see figure).</p>'''),
        ('Motion of the centre of mass', r'''<ul><li>\(M\vec V_{CM}=\sum m_i\vec v_i=\vec P\) and \(M\vec A_{CM}=\vec F_{\rm ext}\). Internal forces cancel in pairs, so they cannot move the CM.</li>
<li><strong>No external force:</strong> the CM keeps its velocity. A person walking on a boat on still water moves the boat the other way; if the CM was at rest, m × (person’s displacement) = M × (boat’s displacement), measured relative to the ground.</li>
<li><strong>Projectile that explodes:</strong> explosion forces are internal, so the CM continues on the original parabola until a fragment hits the ground.</li>
<li>The CM can accelerate only if there is a net external force (gravity, friction from the ground, and so on).</li></ul>'''),
    ],
    formulas=[
        dict(title='Centre of mass of standard uniform bodies',
             formula=r'\begin{array}{ll}\text{Semicircular ring (wire)} & 2R/\pi\ \text{from centre}\\ \text{Semicircular disc} & 4R/3\pi\ \text{from centre}\\ \text{Hemispherical shell} & R/2\ \text{from centre}\\ \text{Solid hemisphere} & 3R/8\ \text{from centre}\\ \text{Solid cone} & h/4\ \text{from base}\\ \text{Hollow cone (surface)} & h/3\ \text{from base}\end{array}',
             symbols='R radius (m); h height of the cone (m). Each distance is measured along the axis of symmetry, from the centre of the full circle or sphere, or from the base of the cone. Uniform bodies only.'),
        dict(title='Remainder after removing a piece',
             formula=r'X=\frac{M_1x_1-M_2x_2}{M_1-M_2}',
             symbols='M₁ mass of the complete body (kg) with CM at x₁ (m); M₂ mass of the removed part (kg) with CM at x₂ (m); X CM of what remains (m). For uniform plates, use areas in place of masses.'),
    ],
    figure=dict(svg=FIG_HOLE, caption='A disc with a hole of radius R/2 touching its rim. Treating the hole as negative mass M/4 shifts the centre of mass R/6 away from the hole.'),
    traps=[r'When a piece is removed, the CM shifts away from the hole, not toward it. Students often add the hole’s contribution instead of subtracting it.',
           r'Internal forces (an explosion, a person walking on a boat) cannot change the velocity of the CM. Only external forces can.'],
    exam=r'''<ul><li>CM of an L-shaped plate, a disc or square with a hole, or a combination of rods.</li>
<li>Standard positions: semicircular ring 2R/π, semicircular disc 4R/3π, solid hemisphere 3R/8, cone h/4.</li>
<li>Rod with variable density (λ = kx or kx²): CM by integration.</li>
<li>Person walking on a boat or plank: how far the boat moves.</li>
<li>Projectile exploding at the top: where the second fragment lands.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A uniform disc of radius R has a circular hole of radius R/2 cut out, the hole touching the rim. Find the centre of mass of the remaining plate.',
             steps=[r'Mass ∝ area. Full disc: πR² ↔ M. Hole: π(R/2)² = πR²/4 ↔ M/4.',
                    r'Take O at the disc centre. Hole centre at x = +R/2.',
                    r'X = (M × 0 − (M/4)(R/2))/(M − M/4) = (−MR/8)/(3M/4) = −R/6.',
                    r'The CM is R/6 from O, on the side opposite the hole.'],
             answer=r'R/6 from the centre, away from the hole'),
        dict(tag='Numerical', q=r'A 60 kg man stands at one end of a 140 kg boat at rest on still water. He walks 4 m to the other end. How far does the boat move?',
             steps=[r'No horizontal external force, so the CM stays at rest.',
                    r'Let the boat move x backward. The man moves (4 − x) forward relative to the ground.',
                    r'60(4 − x) = 140x, so 240 = 200x and x = 1.2 m.',
                    r'The man moves 2.8 m forward relative to the shore.'],
             answer=r'1.2 m, opposite to the man'),
        dict(tag='Conceptual', q=r'A shell fired with horizontal range R explodes at the top of its path into two equal fragments. One fragment falls straight down from rest. Where does the other land?',
             steps=[r'The CM still lands at R, since the explosion forces are internal and both fragments land at the same time.',
                    r'The first fragment lands below the top, at R/2.',
                    r'(m/2)(R/2) + (m/2)x = mR gives x = 3R/2.',
                    r'Check with momentum: the second fragment gets twice the horizontal velocity, so it covers R (not R/2) in the remaining time.'],
             answer=r'At 3R/2 from the launch point'),
    ],
    practice=[
        dict(q=r'The centre of mass of a uniform solid hemisphere of radius R lies on its axis at a distance from the flat face of',
             options=['R/2', '3R/8', '4R/3π', '2R/π'], answer=1, type='concept',
             explanation=r'Integration over discs gives 3R/8 for the solid hemisphere. R/2 is the hollow hemispherical shell. 4R/3π is the semicircular disc and 2R/π the semicircular ring.'),
        dict(q=r'A uniform square plate of side 2a is divided into four equal squares and the top-right one is removed. The distance of the centre of mass of the rest from the original centre is',
             options=['a/6', 'a√2/6', 'a/3', 'a√2/3'], answer=1, type='numerical',
             explanation=r'The removed square has ¼ of the mass with centre at (a/2, a/2). Remainder: X = Y = −(¼)(a/2)/(¾) = −a/6. Distance = √2 × a/6 = a√2/6. a/6 is only one coordinate. a√2/3 forgets that the remainder has ¾ of the mass.'),
        dict(q=r'A 1 kg particle moves at 6 m/s along +x and a 2 kg particle moves at 3 m/s along +y. The speed of their centre of mass is',
             options=['3 m/s', '4 m/s', '2√2 m/s', '5 m/s'], answer=2, type='numerical',
             explanation=r'V = (1 × 6î + 2 × 3ĵ)/3 = 2î + 2ĵ m/s, so |V| = 2√2 ≈ 2.83 m/s. 4 m/s adds the component magnitudes. 3 m/s averages the speeds without weighting or vectors.'),
        dict(q=r'<strong>Assertion (A):</strong> If a projectile explodes in mid-air, its centre of mass continues along the original parabola until a fragment hits the ground.<br><strong>Reason (R):</strong> The forces of the explosion are internal to the system.',
             options=AR, answer=0, type='ar',
             explanation=r'Internal forces cancel in pairs, so the only external force is still gravity, and the CM keeps its parabolic path. R is the reason for A. After a fragment lands, the ground exerts an extra external force, which is why the "until" matters.'),
    ],
),

'rotation-angular': dict(
    level='basic',
    notes=[
        ('Units, conversions and the angular velocity vector', r'''<ul><li>1 revolution = 2π rad = 360°. A speed of N revolutions per minute (rpm) is ω = 2πN/60 rad/s.</li>
<li>Angular velocity is a vector along the axis. Curl the fingers of your right hand in the sense of rotation; the thumb gives the direction of ω. Linear velocity of a point is \(\vec v=\vec\omega\times\vec r\).</li>
<li>Clock hands: second hand 2π/60 rad/s, minute hand 2π/3600 rad/s, hour hand 2π/43 200 rad/s. Ratios: minute : hour = 12 : 1, second : minute = 60 : 1.</li></ul>'''),
        ('Acceleration of a point on a rotating body', r'''<p>A point at distance r from the axis has two acceleration parts:</p>
<ul><li><strong>Tangential:</strong> a_t = rα, along the velocity. Zero if ω is constant.</li>
<li><strong>Centripetal (radial):</strong> a_c = ω²r = v²/r, toward the axis. Present whenever the body rotates.</li>
<li>They are perpendicular, so the total is \(a=\sqrt{a_t^2+a_c^2}=r\sqrt{\alpha^2+\omega^4}\).</li></ul>
<p>Angle turned in the nth second (constant α): θₙ = ω₀ + α(2n − 1)/2, the rotational copy of the distance in the nth second.</p>'''),
    ],
    formulas=[
        dict(title='Total acceleration of a point',
             formula=r'a=\sqrt{(r\alpha)^2+(\omega^2r)^2}=r\sqrt{\alpha^2+\omega^4}',
             symbols='r distance from the axis (m); α angular acceleration (rad/s²); ω angular velocity (rad/s); a magnitude of the total linear acceleration (m/s²).'),
        dict(title='Conversions and angle in the nth second',
             formula=r'\omega=\frac{2\pi N}{60},\qquad \theta_n=\omega_0+\frac{\alpha}{2}(2n-1)',
             symbols='N speed in rpm; ω in rad/s; θₙ angle turned during the nth second (rad); ω₀ initial angular velocity (rad/s); α constant angular acceleration (rad/s²).'),
    ],
    traps=[r'A point on a body rotating at constant ω still accelerates: its centripetal acceleration ω²r is not zero. Only the tangential part vanishes.',
           r'Convert rpm to rad/s before using ω = ω₀ + αt. Mixing revolutions and radians is the most common numerical slip.'],
    exam=r'''<ul><li>Fan or wheel switched off: angular deceleration and revolutions made before stopping.</li>
<li>Ratio of angular speeds of clock hands.</li>
<li>Net acceleration of a point on a wheel with given α and ω.</li>
<li>Angle described in a particular second.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A fan rotating at 1200 rpm is switched off and stops uniformly in 20 s. Find its angular deceleration and the number of revolutions it makes while stopping.',
             steps=[r'ω₀ = 2π × 1200/60 = 40π rad/s.',
                    r'α = (0 − 40π)/20 = −2π rad/s².',
                    r'θ = average ω × t = (40π/2) × 20 = 400π rad.',
                    r'Revolutions = 400π/2π = 200.'],
             answer=r'2π rad/s² deceleration; 200 revolutions'),
        dict(tag='Numerical', q=r'A wheel starts from rest with α = 2 rad/s². Find the total acceleration of a point 0.5 m from the axis at t = 2 s.',
             steps=[r'ω = αt = 4 rad/s.',
                    r'a_t = rα = 0.5 × 2 = 1 m/s².',
                    r'a_c = ω²r = 16 × 0.5 = 8 m/s².',
                    r'a = √(1² + 8²) = √65 ≈ 8.06 m/s².'],
             answer=r'≈ 8.06 m/s²'),
        dict(tag='Ratio', q=r'Find the ratio of the angular speeds of the minute hand and the hour hand of a clock.',
             steps=[r'The minute hand turns 2π in 1 h; the hour hand turns 2π in 12 h.',
                    r'ω ∝ 1/T, so ω_min : ω_hour = 12 : 1.'],
             answer=r'12 : 1'),
    ],
    practice=[
        dict(q=r'A wheel starts from rest and reaches 4π rad/s in 10 s with uniform angular acceleration. The number of revolutions in this time is',
             options=['20', '40', '5', '10'], answer=3, type='numerical',
             explanation=r'θ = ½(0 + 4π) × 10 = 20π rad = 10 revolutions. 20 leaves the answer in units of π rad rather than revolutions, and 40 doubles it again.'),
        dict(q=r'A body starts from rest with constant α = 2 rad/s². The angle it turns through during the 3rd second is',
             options=['9 rad', '5 rad', '4 rad', '3 rad'], answer=1, type='numerical',
             explanation=r'θ(3) − θ(2) = ½ × 2 × (9 − 4) = 5 rad, matching α(2n − 1)/2. 9 rad is the total in 3 s and 4 rad is the total in 2 s.'),
        dict(q=r'A disc rotates about a fixed axis at constant angular velocity. For a point on its rim,',
             options=['both tangential and centripetal acceleration are zero', 'tangential acceleration is zero but centripetal acceleration is not', 'centripetal acceleration is zero but tangential is not', 'the velocity is constant'], answer=1, type='concept',
             explanation=r'Constant ω means α = 0, so a_t = 0. The point still moves on a circle, so a_c = ω²r ≠ 0. Its speed is constant but its velocity changes direction, so the last option is wrong.'),
        dict(q=r'The ratio of the angular speed of the second hand of a clock to that of the hour hand is',
             options=['60', '720', '3600', '43 200'], answer=1, type='numerical',
             explanation=r'Periods: 60 s and 43 200 s (12 h). The ratio of angular speeds is 43 200/60 = 720. 60 compares the second and minute hands, and 3600 uses a 1 h period for the hour hand.'),
    ],
),

'rotation-torque': dict(
    level='core',
    notes=[
        ('Three ways to compute torque', r'''<ol><li><strong>Formula:</strong> τ = rF sinθ, where θ is the angle between r and F.</li>
<li><strong>Lever arm:</strong> τ = F × d⊥, the force times the perpendicular distance from the point to the line of action (figure). Sliding a force along its line of action does not change its torque.</li>
<li><strong>Cross product:</strong> \(\vec\tau=\vec r\times\vec F\). In the xy-plane, τ_z = xF_y − yF_x. Positive means anticlockwise (along +z).</li></ol>
<p>Torque is zero when F = 0, when r = 0 (force applied at the axis) or when F passes through the axis (θ = 0 or 180°).</p>'''),
        ('Couples and the principle of moments', r'''<p>A couple is two equal, opposite, parallel forces with different lines of action. Net force is zero, so the CM does not accelerate, but the torque is F × (separation) <em>about every point</em>. A couple therefore produces pure rotation. Turning a tap or a steering wheel with two hands applies a couple.</p>
<p><strong>Principle of moments:</strong> for a lever in equilibrium, clockwise moments equal anticlockwise moments about the fulcrum: F₁d₁ = F₂d₂. The weight of a uniform rod acts at its midpoint (centre of gravity). A metre rule balanced on a knife edge is the standard laboratory application.</p>'''),
    ],
    formulas=[
        dict(title='Torque in components',
             formula=r'\vec\tau=\begin{vmatrix}\hat i&\hat j&\hat k\\ x&y&z\\ F_x&F_y&F_z\end{vmatrix},\qquad \tau_z=xF_y-yF_x',
             symbols='x, y, z position of the point of application relative to the chosen origin (m); Fₓ, F_y, F_z force components (N); τ torque (N m). Positive τ_z is anticlockwise when viewed from +z.'),
        dict(title='Principle of moments (lever)',
             formula=r'F_1d_1=F_2d_2',
             symbols='F₁, F₂ forces (N) on opposite sides of the fulcrum; d₁, d₂ their perpendicular distances from the fulcrum (m). The rod’s own weight acts at its centre of gravity.'),
    ],
    figure=dict(svg=FIG_TORQUE, caption='Torque about O equals F times the perpendicular distance d⊥ from O to the line of action, which equals rF sinθ.'),
    traps=[r'The lever arm is the perpendicular distance to the line of action, not the distance to the point where the force is applied.',
           r'A couple has the same torque about every point. Do not look for a "correct" pivot when finding the torque of a couple.'],
    exam=r'''<ul><li>"Find the torque of F = (…) N acting at r = (…) m about the origin." Use the determinant.</li>
<li>Metre-rule balance: find an unknown mass or the rule’s own mass from the balance point.</li>
<li>Rod supported at two points with loads: find the reactions.</li>
<li>Assertion–reason on couples: zero net force, non-zero torque.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A force F = (2î + 3ĵ) N acts at the point r = (î − ĵ) m. Find the torque about the origin.',
             steps=[r'τ_z = xF_y − yF_x = (1)(3) − (−1)(2).',
                    r'τ_z = 3 + 2 = 5 N m.',
                    r'So τ = 5k̂ N m (anticlockwise seen from +z).'],
             answer=r'5k̂ N m'),
        dict(tag='Numerical', q=r'A uniform metre rule balances on a knife edge at the 40 cm mark when a 50 g mass hangs at the 20 cm mark. Find the mass of the rule.',
             steps=[r'The rule’s weight acts at its centre, the 50 cm mark, 10 cm right of the knife edge.',
                    r'The 50 g mass is 20 cm left of the knife edge.',
                    r'Moments: 50 × 20 = m × 10, so m = 100 g.'],
             answer=r'100 g'),
        dict(tag='Conceptual', q=r'Why is a door handle fitted at the edge far from the hinges, and why is it hard to open a door by pushing near the hinge?',
             steps=[r'Torque = F × d⊥. The hinge line is the axis.',
                    r'At the far edge d⊥ is largest, so a small force gives the needed torque.',
                    r'Near the hinge d⊥ is small, so a much larger force is needed for the same torque.'],
             answer=r'A larger lever arm gives more torque for the same force'),
    ],
    practice=[
        dict(q=r'A force F = (3î − ĵ) N acts at r = (î + 2ĵ) m. The torque about the origin is',
             options=['7k̂ N m', '−7k̂ N m', '5k̂ N m', '−5k̂ N m'], answer=1, type='numerical',
             explanation=r'τ_z = xF_y − yF_x = (1)(−1) − (2)(3) = −1 − 6 = −7, so τ = −7k̂ N m (clockwise). 7k̂ reverses the order of the cross product. ±5 comes from adding the wrong products.'),
        dict(q=r'A 10 N force is applied at the end of a 2 m spanner, at 30° to the spanner. The torque about the nut is',
             options=['20 N m', '17.3 N m', '10 N m', '5 N m'], answer=2, type='numerical',
             explanation=r'τ = rF sinθ = 2 × 10 × sin30° = 10 N m. 20 N m treats the force as perpendicular, and 17.3 N m uses cos30° (the component along the spanner, which gives no torque).'),
        dict(q=r'A uniform 1 m rod of mass 2 kg rests on supports at its two ends. A 4 kg mass hangs 25 cm from the left end. The reactions at the left and right supports are (g = 10 m/s²)',
             options=['30 N and 30 N', '20 N and 40 N', '40 N and 20 N', '45 N and 15 N'], answer=2, type='numerical',
             explanation=r'Moments about the left end: R_right × 1 = 20 × 0.5 + 40 × 0.25 = 20, so R_right = 20 N and R_left = 60 − 20 = 40 N. The load is nearer the left end, so the left support carries more. Option 2 swaps them.'),
        dict(q=r'<strong>Assertion (A):</strong> A couple acting on a free rigid body produces rotation but no acceleration of its centre of mass.<br><strong>Reason (R):</strong> The torque of a couple has the same value about every point.',
             options=AR, answer=1, type='ar',
             explanation=r'A is true because the net force of a couple is zero. R is also true. But R does not explain A: the CM stays unaccelerated because the forces cancel, not because the torque is point-independent.'),
    ],
),

'rotation-inertia': dict(
    level='core',
    notes=[
        ('Derivations by integration', r'''<p><strong>Thin rod about its centre (perpendicular axis).</strong> Mass per length λ = M/L. An element dx at distance x has dm = λ dx:
\[I=\int_{-L/2}^{L/2}x^2\lambda\,dx=\lambda\frac{L^3}{12}=\frac{ML^2}{12}.\]
About one end, integrate from 0 to L: I = λL³/3 = ML²/3.</p>
<p><strong>Ring about its central axis.</strong> Every element is at distance R, so I = R²∫dm = MR².</p>
<p><strong>Disc about its central axis.</strong> Split it into rings of radius r and width dr. Area 2πr dr, so dm = (M/πR²)(2πr dr) = (2M/R²) r dr:
\[I=\int_0^R r^2\,\frac{2M}{R^2}r\,dr=\frac{2M}{R^2}\cdot\frac{R^4}{4}=\frac{MR^2}{2}.\]
A solid cylinder about its own axis is a stack of such discs, so it also has MR²/2.</p>'''),
        ('Radius of gyration and what I depends on', r'''<p>Write I = Mk². The radius of gyration k is the distance at which the whole mass could be placed (as a ring) to give the same I. Ring: k = R. Disc: k = R/√2. Solid sphere: k = √(2/5) R. Rod about centre: k = L/(2√3).</p>
<p>I depends on the mass, how the mass is spread, and the axis. It does not depend on the angular velocity or the torque applied. Spreading the same mass farther out (a ring instead of a disc, a hollow sphere instead of a solid one) increases I.</p>'''),
    ],
    formulas=[
        dict(title='Standard moments of inertia (uniform bodies)',
             formula=r'\begin{array}{lll}\text{Body} & \text{Axis} & I\\ \text{Thin ring} & \text{central, }\perp\text{ plane} & MR^2\\ \text{Thin ring} & \text{diameter} & MR^2/2\\ \text{Disc / solid cylinder} & \text{central, }\perp\text{ plane (own axis)} & MR^2/2\\ \text{Disc} & \text{diameter} & MR^2/4\\ \text{Hollow cylinder} & \text{own axis} & MR^2\\ \text{Solid sphere} & \text{diameter} & 2MR^2/5\\ \text{Hollow sphere} & \text{diameter} & 2MR^2/3\\ \text{Rod} & \text{centre, }\perp\text{ rod} & ML^2/12\\ \text{Rod} & \text{end, }\perp\text{ rod} & ML^2/3\\ \text{Rectangular plate } a\times b & \text{centre, }\perp\text{ plate} & M(a^2+b^2)/12\end{array}',
             symbols='M mass (kg); R radius (m); L rod length (m); a, b sides of a rectangular plate (m); I in kg m². Thin ring and hollow sphere have all mass at radius R.'),
        dict(title='Radius of gyration',
             formula=r'I=Mk^2,\qquad k_{\rm ring}=R,\ k_{\rm disc}=\frac{R}{\sqrt2},\ k_{\rm sphere}=\sqrt{\tfrac25}\,R,\ k_{\rm rod,c}=\frac{L}{2\sqrt3}',
             symbols='k radius of gyration (m) about the stated standard axis; M mass (kg); R radius (m); L rod length (m).'),
    ],
    traps=[r'A solid cylinder about its own axis has MR²/2, the same as a disc, whatever its length. Its length matters only for an axis perpendicular to its own axis.',
           r'Moment of inertia is not fixed for a body. It changes with the axis, so "I of a rod" is meaningless without naming the axis.'],
    exam=r'''<ul><li>"Which has the larger moment of inertia: a ring or a disc of the same mass and radius?" and k ratios.</li>
<li>Point masses at the corners of a square or triangle: I about a side, a diagonal or a perpendicular axis.</li>
<li>Two discs of equal mass and thickness but different densities: ratio of I (I ∝ 1/ρ).</li>
<li>Derive I of a rod or disc by integration (subjective and assertion-type).</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'Four particles of 1 kg each sit at the corners of a square of side 1 m. Find I about (a) an axis through one corner perpendicular to the plane, (b) a diagonal.',
             steps=[r'(a) Distances from that corner: 0, 1 m, 1 m and √2 m (the opposite corner).',
                    r'I = 0 + 1 + 1 + 2 = 4 kg m².',
                    r'(b) Two masses lie on the diagonal (distance 0). The other two are at half the other diagonal, √2/2 m.',
                    r'I = 2 × 1 × (1/2) = 1 kg m².'],
             answer=r'(a) 4 kg m² (b) 1 kg m²'),
        dict(tag='Ratio', q=r'Two uniform discs have the same mass and thickness. Disc A has density ρ and disc B has density 2ρ. Find I_A : I_B about their central axes.',
             steps=[r'M = ρπR²t, so R² = M/(ρπt) ∝ 1/ρ for the same M and t.',
                    r'I = ½MR² ∝ R² ∝ 1/ρ.',
                    r'I_A : I_B = (1/ρ) : (1/2ρ) = 2 : 1. The less dense disc is wider.'],
             answer=r'2 : 1'),
        dict(tag='Ratio', q=r'A ring and a disc have the same mass and radius. Find the ratio of their radii of gyration about their central perpendicular axes.',
             steps=[r'Ring: Mk² = MR², so k = R.',
                    r'Disc: Mk² = MR²/2, so k = R/√2.',
                    r'k_ring : k_disc = R : R/√2 = √2 : 1.'],
             answer=r'√2 : 1'),
    ],
    practice=[
        dict(q=r'The radius of gyration of a uniform solid sphere of radius 5 cm about a diameter is about',
             options=['2 cm', '5 cm', '3.16 cm', '3.54 cm'], answer=2, type='numerical',
             explanation=r'k = √(2/5) × R = √0.4 × 5 ≈ 3.16 cm. 3.54 cm is R/√2, the disc value. 2 cm uses 2R/5 without the square root.'),
        dict(q=r'Two discs have equal mass and equal thickness. Disc A is made of a material twice as dense as disc B. I_A/I_B about their central axes is',
             options=['2', '1/2', '4', '1/4'], answer=1, type='numerical',
             explanation=r'R² ∝ 1/ρ for equal mass and thickness, and I ∝ R². The denser disc A is smaller, so I_A/I_B = ρ_B/ρ_A = 1/2. 2 inverts the ratio; 1/4 squares it again.'),
        dict(q=r'The moment of inertia of a rigid body about a given axis does not depend on',
             options=['its mass', 'the distribution of its mass', 'the position of the axis', 'its angular velocity'], answer=3, type='concept',
             explanation=r'I = Σmr² involves only the masses and their distances from the axis. Angular velocity does not appear. The other three all change I.'),
        dict(q=r'<strong>Statement I:</strong> A thin hollow cylinder and a thin ring of the same mass and radius have equal moments of inertia about their own axes.<br><strong>Statement II:</strong> A solid sphere has a larger moment of inertia than a hollow sphere of the same mass and radius about a diameter.',
             options=ST, answer=2, type='statement',
             explanation=r'Statement I is true: in both, all mass is at distance R from the axis, so I = MR². Statement II is false: the hollow sphere has 2MR²/3, more than the solid sphere’s 2MR²/5, because its mass is farther from the axis.'),
    ],
),

'rotation-axis': dict(
    level='exam',
    notes=[
        ('Why the theorems work', r'''<p><strong>Parallel-axis theorem.</strong> Put the CM at the origin and the new axis at distance d. A mass element at (x, y) is at distance² (x − d)² + y² from the new axis. Summing: Σm(x² + y²) − 2dΣmx + d²Σm. The first term is I_CM, the middle term is zero because Σmx = 0 about the CM, and the last is Md². So I = I_CM + Md².</p>
<p><strong>Perpendicular-axis theorem.</strong> For a lamina in the xy-plane, every element has z = 0, so its distance² from the z-axis is x² + y². Thus I_z = Σm(x² + y²) = Σmy² + Σmx² = I_x + I_y. It fails for a 3-D body because then I_x = Σm(y² + z²) contains z terms.</p>'''),
        ('Using both theorems together', r'''<ul><li>Ring about a diameter: I_z = MR² and I_x = I_y by symmetry, so I_diameter = MR²/2.</li>
<li>Disc about a diameter: MR²/4. About a tangent in its plane: MR²/4 + MR² = 5MR²/4. About a tangent perpendicular to its plane: MR²/2 + MR² = 3MR²/2.</li>
<li>Ring about a tangent in its plane: MR²/2 + MR² = 3MR²/2. Perpendicular to its plane: 2MR².</li>
<li>Solid sphere about a tangent: 2MR²/5 + MR² = 7MR²/5. Hollow sphere: 5MR²/3.</li>
<li>Square plate (side a): I_z = Ma²/6 through the centre. Every in-plane axis through the centre, including a diagonal, has Ma²/12.</li></ul>'''),
    ],
    formulas=[
        dict(title='Results from the axis theorems',
             formula=r'\begin{array}{lll}\text{Body} & \text{Axis} & I\\ \text{Ring} & \text{tangent, in plane} & 3MR^2/2\\ \text{Ring} & \text{tangent, }\perp\text{ plane} & 2MR^2\\ \text{Disc} & \text{tangent, in plane} & 5MR^2/4\\ \text{Disc} & \text{tangent, }\perp\text{ plane} & 3MR^2/2\\ \text{Solid sphere} & \text{tangent} & 7MR^2/5\\ \text{Hollow sphere} & \text{tangent} & 5MR^2/3\\ \text{Square plate} & \text{diagonal} & Ma^2/12\end{array}',
             symbols='M mass (kg); R radius (m); a side of the square (m). Each result comes from the central value plus MR² (parallel axis) or from the perpendicular-axis theorem.'),
    ],
    figure=dict(svg=FIG_AXES, caption='Axis theorems on a disc. The perpendicular-axis theorem links the z axis to the two diameters x and y. The parallel-axis theorem shifts the y axis out to the rim to give the tangent axis.'),
    traps=[r'The perpendicular-axis theorem works only for flat bodies (laminas). Using it on a solid sphere gives I_diameter = MR²/5, which is wrong.',
           r'The parallel-axis theorem must start from the CM axis. Going from the end of a rod to an axis at distance d from the end needs two steps: end → centre (subtract), centre → new axis (add).'],
    exam=r'''<ul><li>I of a ring, disc or sphere about a tangent (in-plane or perpendicular).</li>
<li>Rods forming a triangle or square: I about an axis through a vertex or the centre.</li>
<li>Rod about an axis at a given distance from its centre or end.</li>
<li>Assertion–reason on where the perpendicular-axis theorem applies.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A disc of mass 2 kg and radius 0.2 m. Find its moment of inertia about a tangent in its plane.',
             steps=[r'About a diameter (perpendicular axes): I_d = MR²/4.',
                    r'The tangent in the plane is parallel to a diameter, at distance R: I = MR²/4 + MR² = 5MR²/4.',
                    r'I = 1.25 × 2 × 0.04 = 0.1 kg m².'],
             answer=r'0.1 kg m²'),
        dict(tag='Numerical', q=r'Three identical uniform rods, each of mass M and length L, form an equilateral triangle. Find I about an axis through one vertex, perpendicular to the plane.',
             steps=[r'The two rods meeting at that vertex each rotate about an end: 2 × ML²/3.',
                    r'The third rod’s centre is at the triangle’s height from the vertex: L√3/2.',
                    r'Its I = ML²/12 + M(3L²/4) = ML²/12 + 9ML²/12 = 5ML²/6.',
                    r'Total = 2ML²/3 + 5ML²/6 = 4ML²/6 + 5ML²/6 = 3ML²/2.'],
             answer=r'3ML²/2'),
        dict(tag='Statement I / II', q=r'<strong>Statement I:</strong> For a square plate, I about a diagonal equals I about a line through the centre parallel to a side. <strong>Statement II:</strong> I_z = Ma²/6 for the axis through the centre perpendicular to the plate.',
             steps=[r'Through the centre, I_z = M(a² + a²)/12 = Ma²/6. Statement II is true.',
                    r'By symmetry, the two diagonals have equal I, and they are perpendicular in-plane axes, so I_diag = I_z/2 = Ma²/12.',
                    r'The same argument for the two lines parallel to the sides gives Ma²/12 as well. Statement I is true.'],
             answer=r'Both statements are true'),
    ],
    practice=[
        dict(q=r'The moment of inertia of a thin ring of mass M and radius R about a tangent lying in its plane is',
             options=['2MR²', 'MR²/2', '5MR²/4', '3MR²/2'], answer=3, type='numerical',
             explanation=r'I_diameter = MR²/2, then add MR²: 3MR²/2. 2MR² is the tangent perpendicular to the plane. 5MR²/4 is the disc’s in-plane tangent.'),
        dict(q=r'A uniform rod of mass M and length L. Its moment of inertia about a perpendicular axis at a distance L/4 from its centre is',
             options=['7ML²/48', 'ML²/16', 'ML²/3', '5ML²/48'], answer=0, type='numerical',
             explanation=r'I = ML²/12 + M(L/4)² = 4ML²/48 + 3ML²/48 = 7ML²/48. ML²/16 is only the Md² term. ML²/3 is the end axis.'),
        dict(q=r'<strong>Assertion (A):</strong> For a uniform solid sphere, I about a diameter can be found by I_z = I_x + I_y.<br><strong>Reason (R):</strong> The perpendicular-axis theorem applies only to plane bodies.',
             options=AR, answer=3, type='ar',
             explanation=r'R is true. Because a sphere is not a lamina, the theorem does not apply, so A is false. (By symmetry, it would wrongly give I_diameter = I_z/2.)'),
        dict(q=r'The moment of inertia of a uniform solid sphere (mass M, radius R) about a tangent is',
             options=['2MR²/5', '7MR²/5', '5MR²/3', '3MR²/5'], answer=1, type='numerical',
             explanation=r'Parallel axis: 2MR²/5 + MR² = 7MR²/5. 5MR²/3 is the hollow sphere’s tangent value. 2MR²/5 is the diameter.'),
    ],
),

'rotation-dynamics': dict(
    level='exam',
    notes=[
        ('The translation–rotation dictionary', r'''<div class="table-wrap"><table>
<thead><tr><th>Translation</th><th>Rotation (fixed axis)</th></tr></thead>
<tbody>
<tr><td>Displacement x</td><td>Angle θ</td></tr>
<tr><td>Velocity v</td><td>Angular velocity ω</td></tr>
<tr><td>Mass m</td><td>Moment of inertia I</td></tr>
<tr><td>Force F = ma</td><td>Torque τ = Iα</td></tr>
<tr><td>Momentum p = mv</td><td>Angular momentum L = Iω</td></tr>
<tr><td>KE ½mv²</td><td>KE ½Iω²</td></tr>
<tr><td>Work ∫F dx</td><td>Work ∫τ dθ</td></tr>
<tr><td>Power Fv</td><td>Power τω</td></tr>
</tbody></table></div>
<p>Every linear result has a rotational copy. The work–energy theorem becomes W = ½Iω² − ½Iω₀².</p>'''),
        ('Pulleys with mass', r'''<p>A block m hangs from a string wound on a pulley (disc or cylinder) of moment of inertia I and radius R. The string does not slip, so a = Rα.</p>
<ol><li>Block: mg − T = ma.</li>
<li>Pulley: TR = Iα = Ia/R, so T = Ia/R².</li>
<li>Add: mg = (m + I/R²)a, so \(a=\dfrac{mg}{m+I/R^2}\).</li></ol>
<p>For a uniform disc, I/R² = M/2, so a = mg/(m + M/2). The pulley acts like an extra mass I/R² that must be accelerated. With two hanging masses (Atwood machine), a = (m₁ − m₂)g/(m₁ + m₂ + I/R²), and the tensions on the two sides are no longer equal.</p>'''),
        ('Rod pivoted at one end, released from horizontal', r'''<ul><li>Torque about the pivot = Mg(L/2); I = ML²/3. Initial α = 3g/(2L).</li>
<li>The free end starts with acceleration αL = 3g/2, more than g. A coin placed on the free end lifts off.</li>
<li>Energy at the vertical position: Mg(L/2) = ½(ML²/3)ω², so ω = √(3g/L) and the free end moves at √(3gL).</li></ul>'''),
    ],
    formulas=[
        dict(title='Block hanging from a massive pulley',
             formula=r'a=\frac{mg}{m+I/R^2},\qquad T=\frac{I}{R^2}\,a',
             symbols='m hanging mass (kg); I moment of inertia of the pulley (kg m²); R its radius (m); a block acceleration (m/s²); T tension (N); g = 10 m/s². String does not slip; axle frictionless.'),
        dict(title='Rod pivoted at one end, released from horizontal',
             formula=r'\alpha_0=\frac{3g}{2L},\qquad \omega_{\rm vertical}=\sqrt{\frac{3g}{L}},\qquad v_{\rm end}=\sqrt{3gL}',
             symbols='L rod length (m); g = 10 m/s²; α₀ initial angular acceleration (rad/s²); ω angular speed when the rod is vertical (rad/s); v_end speed of the free end then (m/s). Uniform rod, frictionless pivot.'),
    ],
    traps=[r'With a massive pulley, the tensions on the two sides of the pulley are different. Their difference provides the torque that spins the pulley.',
           r'τ = Iα needs torque and I about the same axis. Using I_CM for a rod pivoted at its end gives the wrong α.'],
    exam=r'''<ul><li>Block hanging from a disc pulley: acceleration and tension.</li>
<li>String wound on a cylinder pulled with force F: α, and the length of string unwound.</li>
<li>Rod hinged at one end, released from horizontal: initial α, ω at the vertical, speed of the tip.</li>
<li>Flywheel or wheel brought to rest by a braking torque: torque, work, revolutions.</li>
<li>Power delivered by a motor: P = τω.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A 1 kg block hangs from a light string wound on a uniform disc pulley of mass 2 kg and radius 0.1 m. Find the acceleration of the block and the tension.',
             steps=[r'Disc: I/R² = M/2 = 1 kg.',
                    r'a = mg/(m + I/R²) = 10/(1 + 1) = 5 m/s².',
                    r'T = (I/R²)a = 1 × 5 = 5 N. Check: mg − T = 10 − 5 = 5 = ma.'],
             answer=r'a = 5 m/s², T = 5 N'),
        dict(tag='Numerical', q=r'A uniform rod 1.2 m long is pivoted at one end and released from rest in the horizontal position. Find its initial angular acceleration, its angular speed when vertical, and the speed of the free end then.',
             steps=[r'α₀ = 3g/(2L) = 30/2.4 = 12.5 rad/s².',
                    r'ω = √(3g/L) = √(30/1.2) = √25 = 5 rad/s.',
                    r'v_end = ωL = 5 × 1.2 = 6 m/s (= √(3gL) = √36).'],
             answer=r'12.5 rad/s²; 5 rad/s; 6 m/s'),
        dict(tag='Numerical', q=r'A flywheel with I = 2 kg m² spinning at 50 rad/s is stopped uniformly in 10 s. Find the braking torque, the work done by it, and the angle turned.',
             steps=[r'α = 50/10 = 5 rad/s² (deceleration), so τ = Iα = 10 N m.',
                    r'Work = change in KE = 0 − ½ × 2 × 50² = −2500 J.',
                    r'θ = average ω × t = 25 × 10 = 250 rad (check: τθ = 10 × 250 = 2500 J).'],
             answer=r'10 N m; −2500 J; 250 rad (about 40 revolutions)'),
    ],
    practice=[
        dict(q=r'A light string is wound on a solid cylinder of mass 4 kg and radius 0.5 m, free to rotate about its fixed axis. The string is pulled with a constant 10 N force. The angular acceleration of the cylinder is',
             options=['5 rad/s²', '2.5 rad/s²', '10 rad/s²', '20 rad/s²'], answer=2, type='numerical',
             explanation=r'τ = FR = 5 N m; I = ½MR² = 0.5 kg m²; α = 10 rad/s². 5 rad/s² uses I = MR² (a ring). 20 rad/s² drops the radius from the torque.'),
        dict(q=r'A uniform rod pivoted at one end is released from the horizontal. At the instant of release, the linear acceleration of its free end is',
             options=['g', 'g/2', '3g/2', '2g'], answer=2, type='concept',
             explanation=r'α = τ/I = (MgL/2)/(ML²/3) = 3g/(2L), so the end accelerates at αL = 3g/2, more than g. The CM accelerates at 3g/4. Answering g treats the end as falling freely.'),
        dict(q=r'A motor delivers a torque of 100 N m while rotating at 300 rpm. Its power output is about',
             options=['3.1 kW', '30 kW', '0.5 kW', '1.6 kW'], answer=0, type='numerical',
             explanation=r'ω = 2π × 300/60 = 10π rad/s, so P = τω = 1000π ≈ 3142 W. 30 kW multiplies 100 by 300 without converting rpm. 0.5 kW uses ω = 5 rad/s (rev/s instead of rad/s).'),
        dict(q=r'<strong>Statement I:</strong> In an Atwood machine with a massive pulley, the tensions in the string on the two sides are equal.<br><strong>Statement II:</strong> A massive pulley reduces the acceleration of the hanging masses compared with a light pulley.',
             options=ST, answer=3, type='statement',
             explanation=r'Statement I is false: the pulley needs a net torque (T₁ − T₂)R = Iα, so the tensions differ. Statement II is true: a = (m₁ − m₂)g/(m₁ + m₂ + I/R²) is smaller than for I = 0.'),
    ],
),

'rotation-momentum': dict(
    level='exam',
    notes=[
        ('Angular momentum of a particle in a straight line', r'''<p>A particle moving in a straight line has angular momentum about any point not on that line: L = mv d⊥, where d⊥ is the perpendicular distance from the point to the line. If no force acts, v and d⊥ stay fixed, so L is constant.</p>
<p>This links to Kepler’s second law. A planet moves under a central force, which has zero torque about the Sun, so L is conserved. The area swept per unit time is dA/dt = L/(2m), a constant: equal areas in equal times.</p>'''),
        ('Conservation in action', r'''<ul><li><strong>Skater, diver, dancer:</strong> pulling arms in reduces I and increases ω. Rotational KE = L²/2I rises; the person’s muscles do the extra work.</li>
<li><strong>Person on a rotating platform</strong> walking toward the centre: I falls, ω rises.</li>
<li><strong>Earth shrinking</strong> with the same mass: I ∝ R², so ω ∝ 1/R² and the length of the day ∝ R².</li>
<li><strong>Two discs coupled</strong> on a common axis: ω = (I₁ω₁ + I₂ω₂)/(I₁ + I₂). Kinetic energy is lost, like a perfectly inelastic collision: ΔK = I₁I₂(ω₁ − ω₂)²/[2(I₁ + I₂)].</li></ul>'''),
        ('Angular impulse and collisions with pivoted bodies', r'''<p>Angular impulse is ∫τ dt = ΔL, the rotational copy of impulse = change in momentum.</p>
<p>When a particle hits a rod that is pivoted, the pivot exerts a large force during the impact. So <strong>linear momentum is not conserved</strong>. But the pivot force passes through the pivot and has no torque about it, so <strong>angular momentum about the pivot is conserved</strong>:</p>
<p>\[mvd=(I_{\rm rod}+md^2)\,\omega\quad(\text{particle sticks at distance }d)\]</p>'''),
    ],
    formulas=[
        dict(title='Two discs coupled together',
             formula=r'\omega=\frac{I_1\omega_1+I_2\omega_2}{I_1+I_2},\qquad \Delta K=\frac{I_1I_2(\omega_1-\omega_2)^2}{2(I_1+I_2)}',
             symbols='I₁, I₂ moments of inertia about the common axis (kg m²); ω₁, ω₂ initial angular velocities (rad/s, signed); ω common final value; ΔK kinetic energy lost to friction between the discs (J).'),
        dict(title='Angular impulse and areal velocity',
             formula=r'\int\tau\,dt=\Delta L,\qquad \frac{dA}{dt}=\frac{L}{2m}',
             symbols='τ torque (N m); t time (s); ΔL change in angular momentum (kg m²/s); dA/dt area swept per second by the radius vector of a particle of mass m under a central force (m²/s).'),
    ],
    traps=[r'In a collision with a pivoted rod, do not conserve linear momentum. Conserve angular momentum about the pivot.',
           r'A particle moving in a straight line does have angular momentum about a point off that line. L = 0 only about points on the line itself.'],
    exam=r'''<ul><li>Skater or person on a turntable changes I: new ω and change in KE.</li>
<li>"If Earth contracted to half its radius with the same mass, the length of the day would be …" (6 h).</li>
<li>Two discs brought into contact: common ω and energy lost.</li>
<li>Bullet or particle sticking to a pivoted rod: angular velocity just after impact.</li>
<li>Angular momentum of a particle moving along a line, using r × p.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A disc with I₁ = 2 kg m² spins at 10 rad/s. A second disc, I₂ = 3 kg m², initially at rest, is dropped onto it coaxially and they spin together. Find the common angular velocity and the energy lost.',
             steps=[r'ω = (2 × 10 + 0)/(2 + 3) = 4 rad/s.',
                    r'K before = ½ × 2 × 100 = 100 J. K after = ½ × 5 × 16 = 40 J.',
                    r'Energy lost = 60 J. Formula check: 2 × 3 × 100/(2 × 5) = 60 J.'],
             answer=r'4 rad/s; 60 J lost'),
        dict(tag='Ratio', q=r'If Earth shrank to half its present radius with no change in mass, what would the length of the day become?',
             steps=[r'I = (2/5)MR² ∝ R², so I becomes ¼ of its value.',
                    r'L = Iω is conserved, so ω becomes 4 times larger.',
                    r'T ∝ 1/ω: the day becomes 24/4 = 6 h.'],
             answer=r'6 hours'),
        dict(tag='Numerical', q=r'A uniform rod of mass 3 kg and length 1 m hangs from a pivot at its top end. A 0.5 kg ball moving horizontally at 12 m/s hits its lower end and sticks. Find the angular velocity just after impact.',
             steps=[r'Angular momentum about the pivot before: mvL = 0.5 × 12 × 1 = 6 kg m²/s.',
                    r'I after = ML²/3 + mL² = 1 + 0.5 = 1.5 kg m².',
                    r'ω = 6/1.5 = 4 rad/s.',
                    r'Note: linear momentum after = 3 × 2 + 0.5 × 4 = 8 kg m/s, not 6. The pivot supplied 2 N s of impulse.'],
             answer=r'4 rad/s'),
    ],
    practice=[
        dict(q=r'A platform with I = 120 kg m² carries a 60 kg man standing 2 m from the axis. The system rotates at 1 rad/s. If the man walks to the axis, the new angular velocity is',
             options=['1 rad/s', '2 rad/s', '4 rad/s', '3 rad/s'], answer=3, type='numerical',
             explanation=r'I before = 120 + 60 × 4 = 360 kg m²; I after = 120 kg m². ω = 360 × 1/120 = 3 rad/s. 2 rad/s uses r instead of r² for the man. 1 rad/s ignores the conservation of L.'),
        dict(q=r'If Earth contracted to half its radius with its mass unchanged, the length of a day would become',
             options=['48 h', '12 h', '6 h', '96 h'], answer=2, type='numerical',
             explanation=r'I ∝ R² falls to ¼, so ω rises 4 times and the day becomes 6 h. 12 h assumes I ∝ R. 48 h and 96 h have the change in the wrong direction.'),
        dict(q=r'A 2 kg particle moves with velocity 4î m/s along the line y = 3 m. Its angular momentum about the origin is',
             options=['24k̂ kg m²/s', '−24k̂ kg m²/s', '12k̂ kg m²/s', 'zero'], answer=1, type='numerical',
             explanation=r'L = r × p = (xî + 3ĵ) × (8î) = 24(ĵ × î) = −24k̂. The x part gives î × î = 0, so L is the same everywhere on the line. +24k̂ has the cross-product order reversed. It is not zero because the line misses the origin.'),
        dict(q=r'<strong>Assertion (A):</strong> When a spinning diver pulls in her arms and legs, her rotational kinetic energy increases.<br><strong>Reason (R):</strong> Her angular momentum stays constant while her moment of inertia decreases.',
             options=AR, answer=0, type='ar',
             explanation=r'K = L²/(2I). With L fixed and I smaller, K increases, so R explains A. The extra energy comes from work done by her muscles. Option 3 is tempting if one assumes energy must be conserved, but it is not, because internal forces do work.'),
    ],
),

'rotation-rolling': dict(
    level='core',
    notes=[
        ('Rolling = translation + rotation', r'''<p>Every point of a rolling wheel has the centre’s velocity v plus a rotational velocity of size ωR tangent to the rim. With v = ωR (no slipping):</p>
<ul><li>Bottom (contact) point: v − ωR = 0. It is momentarily at rest.</li>
<li>Top point: v + ωR = 2v.</li>
<li>Points level with the centre: v forward and v vertical, so √2 v at 45°.</li>
<li>In general, a rim point at angle φ from the contact point (measured at the centre) moves at 2v sin(φ/2).</li></ul>
<p>Equivalent picture: the wheel rotates about the contact point P with angular speed ω. Each point’s speed is ω × (distance from P), perpendicular to the line from P (figure).</p>'''),
        ('Energy split between translation and rotation', r'''<p>With I = Mk² and ω = v/R:</p>
<p>\[K=\tfrac12Mv^2+\tfrac12Mk^2\frac{v^2}{R^2}=\tfrac12Mv^2\left(1+\frac{k^2}{R^2}\right).\]</p>
<div class="table-wrap"><table>
<thead><tr><th>Body</th><th>k²/R²</th><th>K_rot : K_trans</th><th>K_rot / K_total</th></tr></thead>
<tbody>
<tr><td>Ring / hollow cylinder</td><td>1</td><td>1 : 1</td><td>1/2</td></tr>
<tr><td>Disc / solid cylinder</td><td>1/2</td><td>1 : 2</td><td>1/3</td></tr>
<tr><td>Hollow sphere</td><td>2/3</td><td>2 : 3</td><td>2/5</td></tr>
<tr><td>Solid sphere</td><td>2/5</td><td>2 : 5</td><td>2/7</td></tr>
</tbody></table></div>'''),
        ('From sliding to pure rolling', r'''<p>A ball thrown along a rough floor sliding without spin (v = u, ω = 0) feels kinetic friction backward. Friction slows the centre and its torque spins the ball up, until v = ωR. Then friction stops acting and the ball rolls.</p>
<p>The contact force passes through the contact point, so angular momentum about a point on the floor is conserved: MuR = MvR + Iv/R. This gives \(v=\dfrac{u}{1+k^2/R^2}\): a ring ends at u/2, a disc at 2u/3, a solid sphere at 5u/7.</p>'''),
    ],
    formulas=[
        dict(title='Kinetic energy of a rolling body',
             formula=r'K=\tfrac12Mv^2\left(1+\frac{k^2}{R^2}\right),\qquad \frac{K_{\rm rot}}{K}=\frac{k^2/R^2}{1+k^2/R^2}',
             symbols='M mass (kg); v centre speed (m/s); k radius of gyration about the centre (m); R rolling radius (m). Rolling without slipping, v = ωR.'),
        dict(title='Final rolling speed after sliding (no initial spin)',
             formula=r'v=\frac{u}{1+k^2/R^2},\qquad t=\frac{u-v}{\mu_kg}',
             symbols='u initial sliding speed (m/s); v final pure-rolling speed (m/s); k, R as above; μₖ kinetic friction coefficient; t time to start pure rolling (s). Level floor.'),
    ],
    figure=dict(svg=FIG_ROLL, caption='Velocities of points on a wheel rolling without slipping. The contact point is at rest, the top moves at 2v, and the points level with the centre move at √2 v at 45°.'),
    traps=[r'The contact point of a rolling wheel has zero velocity but not zero acceleration. It has a centripetal acceleration v²/R toward the centre.',
           r'The rotational share of energy depends only on the shape (k²/R²), not on the mass or the size.'],
    exam=r'''<ul><li>Fraction of total KE that is rotational for a ring, disc or sphere, or ratio K_trans : K_rot.</li>
<li>Speed of the top point, or of a point at the level of the centre.</li>
<li>Total KE of a rolling body with given M and v.</li>
<li>Ball or ring launched sliding: final rolling speed and time taken.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A 2 kg uniform disc rolls without slipping at 3 m/s. Find its total kinetic energy and the fraction that is rotational.',
             steps=[r'K = ½Mv²(1 + ½) = ¾ × 2 × 9 = 13.5 J.',
                    r'K_trans = ½ × 2 × 9 = 9 J, K_rot = 4.5 J.',
                    r'Fraction rotational = 4.5/13.5 = 1/3.'],
             answer=r'13.5 J; one third is rotational'),
        dict(tag='Numerical', q=r'A wheel rolls without slipping with its centre moving at 5 m/s. Find the speed of (a) the top point, (b) a point on the rim level with the centre.',
             steps=[r'(a) Top: v + ωR = 2v = 10 m/s.',
                    r'(b) Level with the centre: forward v plus a vertical v from rotation.',
                    r'Speed = √(5² + 5²) = 5√2 ≈ 7.07 m/s.'],
             answer=r'(a) 10 m/s (b) ≈ 7.07 m/s'),
        dict(tag='Numerical', q=r'A bowling ball (solid sphere) is launched at 7 m/s sliding without spin. μₖ = 0.2. Find its final rolling speed and the time it slides.',
             steps=[r'v = u/(1 + 2/5) = 7 × 5/7 = 5 m/s.',
                    r'The centre decelerates at μₖg = 2 m/s².',
                    r't = (7 − 5)/2 = 1 s.'],
             answer=r'5 m/s after 1 s'),
    ],
    practice=[
        dict(q=r'For a uniform solid sphere rolling without slipping, the ratio of translational to rotational kinetic energy is',
             options=['2 : 5', '5 : 2', '7 : 2', '1 : 1'], answer=1, type='numerical',
             explanation=r'K_rot/K_trans = k²/R² = 2/5, so K_trans : K_rot = 5 : 2. 2 : 5 is the inverse. 7 : 2 is total : rotational. 1 : 1 is the ring.'),
        dict(q=r'For a thin hollow sphere rolling without slipping, the fraction of its total kinetic energy that is rotational is',
             options=['2/5', '2/3', '1/2', '2/7'], answer=0, type='numerical',
             explanation=r'k²/R² = 2/3, so K_rot/K = (2/3)/(5/3) = 2/5. 2/3 is k²/R² itself. 2/7 is the solid sphere and 1/2 the ring.'),
        dict(q=r'A wheel rolls without slipping on level ground with its centre moving at 2 m/s. Which statements are correct?<br>(i) The top point moves at 4 m/s.<br>(ii) The contact point has zero velocity.<br>(iii) The contact point has zero acceleration.<br>(iv) All rim points have the same speed relative to the ground.',
             options=['(i) and (ii) only', '(i), (ii) and (iii)', '(ii) and (iv) only', '(i) and (iv) only'], answer=0, type='multi',
             explanation=r'(i) and (ii) are true. (iii) is false: the contact point has centripetal acceleration v²/R upward. (iv) is false: rim speeds range from 0 at the bottom to 2v at the top; only relative to the centre are they equal.'),
        dict(q=r'A thin ring is placed on a rough floor with speed u and no spin. When it starts rolling without slipping, its speed is',
             options=['u', '2u/3', '5u/7', 'u/2'], answer=3, type='numerical',
             explanation=r'v = u/(1 + k²/R²) = u/2 for a ring. 2u/3 is the disc and 5u/7 the solid sphere. The speed cannot stay u, because kinetic friction acts while it slips.'),
    ],
),
}


NEW_SECTIONS = [
dict(chapter='rotation', after='rotation-torque', id='rotation-equilibrium',
     title='Equilibrium of rigid bodies: ladders, toppling and sliding',
     intro=r'A rigid body is in equilibrium when it neither accelerates nor starts turning. That needs two conditions: the vector sum of the forces is zero, and the sum of the torques about any point is zero.',
     reasoning=r'Choose the pivot for the torque equation where an unknown force acts; that force then drops out. For a ladder leaning on a smooth wall, take torques about the foot. For a box pushed sideways, compare the force needed to slide it with the force needed to tip it about its front edge.',
     formula=r'\sum\vec F=0,\qquad \sum\vec\tau=0,\qquad \mu_{\min}=\frac{1}{2\tan\theta}\ \ (\text{ladder, smooth wall})',
     symbols='F forces (N); τ torques about any one point (N m); μ_min least floor friction coefficient for a uniform ladder resting on a smooth wall; θ angle between ladder and floor.',
     trap=r'The friction on a ladder’s foot points toward the wall. The ladder’s foot tends to slide away from the wall, and friction opposes that.',
     example=r'A uniform 5 m ladder rests against a smooth wall with its foot 3 m from the wall. Find the least coefficient of friction at the floor.',
     solution=r'cosθ = 3/5 and sinθ = 4/5, so tanθ = 4/3. μ_min = 1/(2 tanθ) = 3/8 = 0.375.',
     question=r'A uniform cube of side a stands on a rough floor. A horizontal force is applied at the middle of its top edge and slowly increased. The cube tips over before it slides if μ is greater than',
     options='1/4|1/2|1|2', answer=1,
     explanation=r'Sliding needs F = μmg. Tipping about the front edge needs Fa = mg(a/2), i.e. F = mg/2. It tips first if mg/2 &lt; μmg, i.e. μ &gt; 1/2.',
     deep=dict(
        level='exam',
        notes=[
            ('Derivation: the ladder against a smooth wall', r'''<ol><li>Forces (figure): weight mg at the middle; N₂ horizontal from the smooth wall at the top; N₁ upward and friction f toward the wall at the foot.</li>
<li>Vertical balance: N₁ = mg. Horizontal balance: f = N₂.</li>
<li>Torques about the foot (N₁ and f have no torque there): N₂ × L sinθ = mg × (L/2) cosθ, so N₂ = mg/(2 tanθ).</li>
<li>No slip needs f ≤ μN₁: mg/(2 tanθ) ≤ μmg, so tanθ ≥ 1/(2μ).</li></ol>
<p>A steeper ladder (larger θ) is safer. When a person climbs higher, the torque of the load about the foot grows, so the friction needed grows too; ladders usually slip when someone is near the top.</p>'''),
            ('Toppling versus sliding', r'''<p><strong>Horizontal push at height h on a block</strong> of width b: sliding needs F = μmg; tipping about the front lower edge needs F h = mg(b/2). It tips first if μ &gt; b/(2h).</p>
<p><strong>Block on a tilting incline</strong> (width b, height h, CG at the centre): it topples when the vertical line through the CG passes the lower edge, tanθ = b/h. It slides when tanθ = μ. Whichever angle is smaller happens first.</p>
<p><strong>Vehicle on a level curve:</strong> it skids if v² &gt; μrg, and overturns if v² &gt; grd/(2h), where d is the distance between the wheels and h the height of the CG. A low CG and wide track resist overturning.</p>'''),
        ],
        formulas=[
            dict(title='Toppling conditions',
                 formula=r'\mu>\frac{b}{2h}\ (\text{push at height }h\text{ tips first}),\qquad \tan\theta_{\rm topple}=\frac bh\ (\text{incline})',
                 symbols='b width of the block (m); h height of the push above the floor, or height of the block for the incline case (m); μ static friction coefficient; θ incline angle. Uniform block with CG at its centre.'),
            dict(title='Overturning on a level curve',
                 formula=r'v_{\rm overturn}=\sqrt{\frac{grd}{2h}}',
                 symbols='g = 10 m/s²; r radius of the curve (m); d distance between the left and right wheels (m); h height of the centre of gravity above the road (m). Overturning about the outer wheels; enough friction to prevent skidding.'),
        ],
        figure=dict(svg=FIG_LADDER, caption='Forces on a ladder resting on a smooth wall and a rough floor. Taking torques about the foot removes N₁ and f, leaving N₂ L sinθ = mg (L/2) cosθ.'),
        traps=[r'Torque balance can be taken about any point once the forces balance. Picking a point where unknown forces act saves algebra; it does not change the answer.',
               r'On an incline, a tall narrow block can topple while friction is still holding it. Check both tanθ = μ and tanθ = b/h.'],
        exam=r'''<ul><li>Ladder against a smooth wall: least μ, or least angle with the floor, or the reactions.</li>
<li>Horizontal rod hinged at a wall and held by a string: string tension and hinge reaction.</li>
<li>Box pushed at a height: does it slide or tip first?</li>
<li>Block on an incline that is slowly tilted: topple or slide first.</li>
<li>Maximum speed before a vehicle overturns on a level curve.</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'A uniform ladder of mass 20 kg rests against a smooth wall at 60° to the floor. Find the reaction of the wall, the friction at the floor and the least μ.',
                 steps=[r'N₁ = mg = 200 N.',
                        r'Torques about the foot: N₂ = mg/(2 tan60°) = 200/(2 × 1.732) ≈ 57.7 N.',
                        r'Friction f = N₂ ≈ 57.7 N, toward the wall.',
                        r'μ_min = f/N₁ = 57.7/200 ≈ 0.29 (= 1/(2√3)).'],
                 answer=r'N₂ ≈ 57.7 N; f ≈ 57.7 N; μ_min ≈ 0.29'),
            dict(tag='Numerical', q=r'A 8 kg cube of side 0.4 m rests on a floor with μ = 0.3. A horizontal force is applied at the top edge and increased slowly. Does it slide or tip first?',
                 steps=[r'Slide when F = μmg = 0.3 × 80 = 24 N.',
                        r'Tip about the front edge when F × 0.4 = 80 × 0.2, i.e. F = 40 N.',
                        r'24 N is reached first, so the cube slides. (Check: μ = 0.3 &lt; b/2h = 0.5.)'],
                 answer=r'It slides first (at 24 N)'),
            dict(tag='Numerical', q=r'A truck has its wheels 1.5 m apart and its centre of gravity 0.75 m above the road. Find the speed on a level curve of radius 40 m at which it would begin to overturn (assume it does not skid).',
                 steps=[r'v² = grd/(2h) = 10 × 40 × 1.5/(2 × 0.75).',
                        r'v² = 600/1.5 = 400.',
                        r'v = 20 m/s (72 km/h).'],
                 answer=r'20 m/s'),
        ],
        practice=[
            dict(q=r'A uniform ladder rests against a smooth wall. The coefficient of friction with the floor is 0.5. The smallest angle the ladder can make with the floor without slipping is',
                 options=['30°', '60°', '45°', 'tan⁻¹ 0.5'], answer=2, type='numerical',
                 explanation=r'tanθ ≥ 1/(2μ) = 1, so θ_min = 45°. tan⁻¹ 0.5 is the angle of friction, which belongs to a block on an incline, not a ladder. 30° and 60° do not satisfy tanθ = 1.'),
            dict(q=r'A uniform block, twice as tall as it is wide, stands on a plank whose angle is slowly increased. μ = 0.8. The block',
                 options=['slides when tanθ = 0.8', 'topples when tanθ = 0.5', 'slides and topples at the same angle', 'topples when tanθ = 2'], answer=1, type='concept',
                 explanation=r'Toppling occurs at tanθ = b/h = 1/2 (about 26.6°), before sliding at tanθ = 0.8 (about 38.7°). So it topples first. tanθ = 2 uses h/b instead of b/h.'),
            dict(q=r'A uniform 6 kg rod is hinged at a wall and held horizontal by a string tied to its free end. The string makes 30° with the rod. The tension is (g = 10 m/s²)',
                 options=['30 N', '60 N', '120 N', '52 N'], answer=1, type='numerical',
                 explanation=r'Torques about the hinge: T sin30° × L = mg × L/2, so T = mg = 60 N. 30 N forgets the sin30° factor. 120 N doubles the torque of the weight by placing it at the free end.'),
            dict(q=r'<strong>Statement I:</strong> For a ladder resting against a smooth wall and a rough floor, the friction at the floor acts toward the wall.<br><strong>Statement II:</strong> The normal reaction of the floor on the ladder equals the ladder’s weight.',
                 options=ST, answer=0, type='statement',
                 explanation=r'Statement I is true: the foot tends to slide away from the wall. Statement II is true: the smooth wall pushes horizontally, so only the floor’s normal force balances the weight vertically.'),
        ],
     )),

dict(chapter='rotation', after='rotation-rolling', id='rotation-incline',
     title='Rolling down an incline: the race and the friction needed',
     intro=r'Release a ring, a disc and a solid sphere together from the top of a rough incline. Each rolls without slipping, but they do not reach the bottom together. The one whose mass is closer to its axis (smaller k²/R²) converts less energy into rotation and wins.',
     reasoning=r'The acceleration is g sinθ/(1 + k²/R²). It depends only on the shape, not on the mass or radius. Static friction provides the torque that makes the body spin. Because the contact point does not slide, this friction does no work, so mechanical energy is conserved.',
     formula=r'a=\frac{g\sin\theta}{1+k^2/R^2},\qquad v=\sqrt{\frac{2gh}{1+k^2/R^2}},\qquad f=\frac{Mg\sin\theta\,(k^2/R^2)}{1+k^2/R^2}',
     symbols='a acceleration of the centre down the slope (m/s²); g = 10 m/s²; θ incline angle; k radius of gyration about the centre (m); R radius (m); v speed at the bottom after a vertical drop h (m); f static friction needed (N); M mass (kg). Rolling without slipping from rest.',
     trap=r'On a frictionless incline a body cannot start rolling. It slides with a = g sinθ, and any spin it had stays unchanged.',
     example=r'A solid cylinder rolls down a 30° incline. Find its acceleration and the friction force in terms of its weight.',
     solution=r'k²/R² = 1/2, so a = g sinθ/1.5 = 5/1.5 ≈ 3.33 m/s². Friction f = Mg sinθ × (1/2)/(3/2) = Mg sinθ/3 = Mg/6.',
     question=r'A ring, a disc, a hollow sphere and a solid sphere are released together from the top of the same rough incline and roll without slipping. Which reaches the bottom first?',
     options='Ring|Disc|Solid sphere|All together', answer=2,
     explanation=r'The smallest k²/R² gives the largest acceleration. Solid sphere 2/5 &lt; disc 1/2 &lt; hollow sphere 2/3 &lt; ring 1. Mass and radius do not matter, so "all together" is wrong.',
     deep=dict(
        level='exam',
        notes=[
            ('Derivation by forces and torque, then by energy', r'''<p><strong>Forces and torque</strong> (figure):</p>
<ol><li>Along the slope: Mg sinθ − f = Ma.</li>
<li>Torque about the centre: fR = Iα = Mk²(a/R), so f = Ma(k²/R²).</li>
<li>Add: Mg sinθ = Ma(1 + k²/R²), so a = g sinθ/(1 + k²/R²).</li></ol>
<p><strong>Energy:</strong> after a vertical drop h, Mgh = ½Mv²(1 + k²/R²), so v² = 2gh/(1 + k²/R²). Since v² = 2a(h/sinθ), this gives the same a.</p>'''),
            ('The race', r'''<div class="table-wrap"><table>
<thead><tr><th>Body</th><th>k²/R²</th><th>a (as a fraction of g sinθ)</th><th>Order</th></tr></thead>
<tbody>
<tr><td>Solid sphere</td><td>2/5</td><td>5/7 ≈ 0.71</td><td>1st</td></tr>
<tr><td>Disc / solid cylinder</td><td>1/2</td><td>2/3 ≈ 0.67</td><td>2nd</td></tr>
<tr><td>Hollow sphere</td><td>2/3</td><td>3/5 = 0.60</td><td>3rd</td></tr>
<tr><td>Ring / hollow cylinder</td><td>1</td><td>1/2 = 0.50</td><td>4th</td></tr>
</tbody></table></div>
<p>Time for a slope length L: \(t=\sqrt{\dfrac{2L(1+k^2/R^2)}{g\sin\theta}}\). A block sliding on a frictionless incline (a = g sinθ) beats all of them. With equal masses, all rolling bodies reach the bottom with the same total KE (Mgh); they differ only in how it is split.</p>'''),
            ('How much friction is needed, and rolling uphill', r'''<p>Pure rolling needs f ≤ μN = μMg cosθ, which gives</p>
<p>\[\mu\ \ge\ \tan\theta\,\frac{k^2/R^2}{1+k^2/R^2}:\quad \text{sphere } \tfrac27\tan\theta,\ \text{disc } \tfrac13\tan\theta,\ \text{ring } \tfrac12\tan\theta.\]</p>
<p>If μ is smaller, the body rolls with slipping: kinetic friction μMg cosθ acts, a = g(sinθ − μcosθ), and energy is lost.</p>
<p><strong>Rolling up an incline</strong> with no driving torque, friction again acts <em>up</em> the slope: it must slow the spin as gravity slows the centre. The height reached is h = v²(1 + k²/R²)/(2g), higher than a sliding block’s v²/2g, because the rotational energy is also converted to height.</p>'''),
        ],
        formulas=[
            dict(title='Time to roll down and least friction coefficient',
                 formula=r't=\sqrt{\frac{2L\,(1+k^2/R^2)}{g\sin\theta}},\qquad \mu_{\min}=\tan\theta\,\frac{k^2/R^2}{1+k^2/R^2}',
                 symbols='L length along the incline (m); g = 10 m/s²; θ incline angle; k radius of gyration (m); R radius (m); t time from rest (s); μ_min least static friction coefficient for pure rolling.'),
            dict(title='Height reached when rolling up',
                 formula=r'h=\frac{v^2}{2g}\left(1+\frac{k^2}{R^2}\right)',
                 symbols='v speed of the centre at the bottom (m/s); h vertical height reached (m); g = 10 m/s². Pure rolling throughout, no losses.'),
        ],
        figure=dict(svg=FIG_INCL, caption='A body rolling down a rough incline. Static friction at the contact acts up the slope. It reduces the acceleration below g sinθ and supplies the torque that spins the body.'),
        traps=[r'Friction on a rolling body does not always point down the slope or opposite to motion. Both rolling down and rolling up (freely), it points up the slope.',
               r'Mass and radius cancel. A heavy solid sphere and a light solid sphere roll down together; only the shape matters.'],
        exam=r'''<ul><li>"Which reaches the bottom first?" and ratios of times, accelerations or speeds for two shapes.</li>
<li>Acceleration or speed at the bottom for a given body and angle.</li>
<li>Minimum μ for pure rolling on a given incline.</li>
<li>Body rolling up an incline: height or distance reached.</li>
<li>Frictionless incline: a body slides, does not roll (common assertion–reason).</li></ul>''',
        examples=[
            dict(tag='Ratio', q=r'A ring and a solid sphere roll from rest down the same incline. Find the ratio of their times to reach the bottom, t_ring : t_sphere.',
                 steps=[r't ∝ √(1 + k²/R²).',
                        r'Ring: 1 + 1 = 2. Sphere: 1 + 2/5 = 7/5.',
                        r't_ring/t_sphere = √(2/(7/5)) = √(10/7) ≈ 1.20.'],
                 answer=r'√10 : √7 (the ring takes about 20% longer)'),
            dict(tag='Numerical', q=r'A solid sphere rolls down a 37° incline (tan 37° = 0.75). Find the least coefficient of static friction for pure rolling.',
                 steps=[r'μ_min = tanθ × (2/5)/(7/5) = (2/7) tanθ.',
                        r'μ_min = (2/7) × 0.75 = 3/14 ≈ 0.21.'],
                 answer=r'≈ 0.21'),
            dict(tag='Numerical', q=r'A disc rolls without slipping at 6 m/s onto an incline and rolls up. How high does it rise? Compare with a block sliding up a smooth incline at the same speed.',
                 steps=[r'Disc: h = v²(1 + 1/2)/(2g) = 36 × 1.5/20 = 2.7 m.',
                        r'Block: h = v²/(2g) = 36/20 = 1.8 m.',
                        r'The disc’s rotational energy (one third of its total) is also converted to height.'],
                 answer=r'2.7 m (block: 1.8 m)'),
            dict(tag='Assertion–Reason', q=r'<strong>A:</strong> A solid sphere and a hollow sphere of equal mass, rolling from the same height, reach the bottom with equal total kinetic energy. <strong>R:</strong> Static friction does no work in pure rolling.',
                 steps=[r'Pure rolling: the contact point is at rest, so static friction does no work.',
                        r'Only gravity does work, Mgh, which is the same for equal masses. So A is true.',
                        r'R is the reason energy is conserved, so R explains A. (Their speeds differ because the split differs.)'],
                 answer=r'Both true; R explains A'),
        ],
        practice=[
            dict(q=r'A thin hollow sphere rolls without slipping down a 30° incline (g = 10 m/s²). Its acceleration is',
                 options=['5 m/s²', '3.57 m/s²', '3 m/s²', '2.5 m/s²'], answer=2, type='numerical',
                 explanation=r'a = g sinθ/(1 + 2/3) = 5 × 3/5 = 3 m/s². 3.57 m/s² is the solid sphere, 2.5 m/s² the ring, and 5 m/s² a frictionless slide.'),
            dict(q=r'A disc and a ring roll down the same incline from rest through the same height. The ratio of their speeds at the bottom, v_disc : v_ring, is',
                 options=['2 : √3', '√3 : 2', '1 : 1', '4 : 3'], answer=0, type='numerical',
                 explanation=r'v² = 2gh/(1 + k²/R²). v_disc²/v_ring² = 2/(3/2) = 4/3, so v_disc/v_ring = 2/√3. 4 : 3 forgets the square root, and √3 : 2 inverts it. The disc is faster.'),
            dict(q=r'A ring is released from rest on a perfectly smooth (frictionless) incline. It will',
                 options=['roll with a = g sinθ/2', 'roll with a = g sinθ', 'slide without rotating, a = g sinθ', 'stay at rest'], answer=2, type='concept',
                 explanation=r'Without friction there is no torque about the centre, so the ring cannot start spinning. It slides with a = g sinθ. g sinθ/2 is the rough-incline rolling result.'),
            dict(q=r'<strong>Statement I:</strong> A cylinder rolling up an incline with no driving torque experiences friction directed up the incline.<br><strong>Statement II:</strong> The friction needed for pure rolling down an incline is larger for a ring than for a solid sphere of the same mass.',
                 options=ST, answer=0, type='statement',
                 explanation=r'Statement I is true: gravity slows the centre, and friction up the slope supplies the torque that slows the spin to keep v = ωR. Statement II is true: f = Mg sinθ (k²/R²)/(1 + k²/R²) is Mg sinθ/2 for the ring and 2Mg sinθ/7 for the solid sphere.'),
            dict(q=r'Match each body rolling down an incline with its acceleration as a fraction of g sinθ.<br>(P) Ring (Q) Solid cylinder (R) Solid sphere (S) Hollow sphere<br>(1) 5/7 (2) 3/5 (3) 1/2 (4) 2/3',
                 options=['P-3, Q-4, R-1, S-2', 'P-3, Q-2, R-1, S-4', 'P-4, Q-3, R-1, S-2', 'P-1, Q-4, R-3, S-2'], answer=0, type='match',
                 explanation=r'a/(g sinθ) = 1/(1 + k²/R²): ring 1/2, solid cylinder 2/3, solid sphere 5/7, hollow sphere 3/5. Option 2 swaps the cylinder and the hollow sphere.'),
        ],
     )),
]
