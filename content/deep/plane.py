"""Deepening layer for Motion in a Plane. Schema: docs/deepening-schema.md."""
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
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
    x2, y2 = cx + r * math.cos(math.radians(a2)), cy - r * math.sin(math.radians(a2))
    large = 1 if (a2 - a1) % 360 > 180 else 0
    return f'<path d="M{_f(x1)} {_f(y1)} A{_f(r)} {_f(r)} 0 {large} 0 {_f(x2)} {_f(y2)}" style="fill:none;stroke:{c};stroke-width:{w}"/>'


def _polar(cx, cy, r, a):
    return cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))


def _curve(pts, c='var(--ink-2)', w=2, dash=False):
    d = ';stroke-dasharray:6 5' if dash else ''
    return '<polyline points="' + ' '.join(f'{_f(x)},{_f(y)}' for x, y in pts) + f'" style="fill:none;stroke:{c};stroke-width:{w}{d}"/>'


def _svg(w, h, label, *parts):
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}" style="max-width:{int(w * 1.35)}px;margin:0 auto">'
            + ''.join(parts) + '</svg>')


def _lab(*parts):
    """Alternate normal and subscript text: _lab('a', 't', ' = dv/dt')."""
    out = ''
    for i, t in enumerate(parts):
        if i % 2:
            out += f'<tspan dy="3" font-size="9">{t}</tspan>'
        else:
            t = t.replace(' ', '&#160;')
            out += f'<tspan dy="-3">{t}</tspan>' if i else t
    return out


def _dot(x, y, c='var(--ink)', r=3.5):
    return f'<circle cx="{_f(x)}" cy="{_f(y)}" r="{r}" style="fill:{c}"/>'


def _parabola(x0, y0, rng, h, n=48):
    return [(x0 + rng * k / n, y0 - 4 * h * (k / n) * (1 - k / n)) for k in range(n + 1)]


IT = ';font-style:italic;font-weight:600'

# ---------- figures ----------
_B0, _B1, _B2 = (80, 175), (190, 20), (390, 110)


def _bz(t):
    return tuple((1 - t) ** 2 * _B0[i] + 2 * (1 - t) * t * _B1[i] + t * t * _B2[i] for i in range(2))


def _dbz(t):
    return tuple(2 * (1 - t) * (_B1[i] - _B0[i]) + 2 * t * (_B2[i] - _B1[i]) for i in range(2))


_P, _Q = _bz(0.3), _bz(0.6)
_dv = _dbz(0.3)
_dl = math.hypot(*_dv)
_O = (40, 215)
FIG_PATH = _svg(
    420, 230, 'Curved path with position vectors r1 and r2 from the origin, the chord displacement between them, and the velocity tangent to the path',
    _curve([_bz(k / 40) for k in range(41)], 'var(--line-2, #C9CEDA)', 3),
    _arrow(*_O, *_P, 'var(--indigo)', 2.4), _arrow(*_O, *_Q, 'var(--teal)', 2.4),
    _arrow(*_P, *_Q, 'var(--coral)', 2.6),
    _arrow(*_P, _P[0] + 75 * _dv[0] / _dl, _P[1] + 75 * _dv[1] / _dl, 'var(--amber)', 2.8),
    _dot(*_P), _dot(*_Q), _dot(*_O),
    _text(_O[0] - 6, _O[1] + 4, 'O', 'var(--ink-2)', 12, 'end'),
    _text(_P[0] - 40, _P[1] + 70, 'r(t)', 'var(--indigo)', 13, extra=IT),
    _text(_Q[0] - 40, _Q[1] + 80, 'r(t + Δt)', 'var(--teal)', 13, extra=IT),
    _text((_P[0] + _Q[0]) / 2 + 4, (_P[1] + _Q[1]) / 2 + 22, 'Δr', 'var(--coral)', 13, extra=IT),
    _text(_P[0] + 46, _P[1] - 66, 'v (tangent)', 'var(--amber)', 12, extra=';font-weight:600'),
    _text(410, 150, 'As Δt → 0 the chord Δr', 'var(--ink-2)', 11, 'end'),
    _text(410, 165, 'turns into the tangent,', 'var(--ink-2)', 11, 'end'),
    _text(410, 180, 'so v = dr/dt is along the path.', 'var(--ink-2)', 11, 'end'),
)

_G, _L0, _RP, _HP = 200, 40, 320, 130
_th = math.degrees(math.atan(4 * _HP / _RP))
_uc, _us = 70 * math.cos(math.radians(_th)), 70 * math.sin(math.radians(_th))
FIG_PROJECTILE = _svg(
    420, 235, 'Projectile path on level ground showing velocity components at launch, at the top and at landing, with maximum height H and range R',
    _line(15, _G, 405, _G, 'var(--ink-2)', 1.5),
    _curve(_parabola(_L0, _G, _RP, _HP), 'var(--line-2, #C9CEDA)', 2.5),
    _arrow(_L0, _G, _L0 + _uc, _G - _us, 'var(--indigo)', 2.6),
    _arrow(_L0, _G, _L0 + _uc, _G, 'var(--teal)', 2), _arrow(_L0, _G, _L0, _G - _us, 'var(--coral)', 2),
    _arc(_L0, _G, 22, 0, _th), _text(_L0 + 24, _G - 8, 'θ', 'var(--ink-2)', 12),
    _text(_L0 + _uc + 4, _G - _us - 2, 'u', 'var(--indigo)', 13, extra=IT),
    _text(_L0 - 4, _G - _us / 2, 'u sin θ', 'var(--coral)', 11, 'end'),
    _text(_L0 + 6, _G + 16, 'u cos θ', 'var(--teal)', 11),
    _arrow(_L0 + _RP / 2, _G - _HP, _L0 + _RP / 2 + _uc, _G - _HP, 'var(--teal)', 2.4),
    _dot(_L0 + _RP / 2, _G - _HP), _text(_L0 + _RP / 2 + 2, _G - _HP - 10, 'top: vertical part 0, v = u cos θ', 'var(--teal)', 11),
    _line(_L0 + _RP / 2, _G - _HP, _L0 + _RP / 2, _G, 'var(--ink-2)', 1.1, True),
    _text(_L0 + _RP / 2 + 5, _G - _HP / 2, 'H', 'var(--ink)', 13, extra=IT),
    _arrow(_L0 + _RP, _G, _L0 + _RP + _uc * 0.75, _G, 'var(--teal)', 2),
    _arrow(_L0 + _RP, _G, _L0 + _RP, _G + 32, 'var(--coral)', 2),
    _text(_L0 + _RP - 4, _G + 32, 'u sin θ (down)', 'var(--coral)', 11, 'end'),
    _line(_L0, _G + 18, _L0 + _RP - 4, _G + 18, 'var(--ink-2)', 1),
    _text(_L0 + _RP / 2, _G + 30, 'R', 'var(--ink)', 13, 'middle', IT),
    _text(410, 24, 'a = g downward at every point', 'var(--ink-2)', 11, 'end'),
)

_TR = 300
_curves = []
for _a, _c, _d in ((30, 'var(--teal)', False), (60, 'var(--indigo)', False), (45, 'var(--ink-2)', True)):
    _rng = _TR * math.sin(math.radians(2 * _a)) / math.sin(math.radians(60))
    _curves.append(_curve(_parabola(30, 200, _rng, _rng * math.tan(math.radians(_a)) / 4), _c, 2.4 if not _d else 1.4, _d))
FIG_COMPLEMENT = _svg(
    420, 240, 'Trajectories at 30 and 60 degrees with the same speed land at the same point; the 45 degree path goes further',
    _line(15, 200, 410, 200, 'var(--ink-2)', 1.5), *_curves,
    _dot(30 + _TR, 200, 'var(--coral)', 4.5),
    _text(30 + _TR, 218, 'same range', 'var(--coral)', 12, 'middle'),
    _text(30 + _TR / 2, 200 - _TR * math.tan(math.radians(60)) / 4 - 8, '60°: high, long flight', 'var(--indigo)', 12, 'middle'),
    _text(30 + _TR / 2, 200 - _TR * math.tan(math.radians(30)) / 4 + 18, '30°: low, short flight', 'var(--teal)', 12, 'middle'),
    _text(415, 236, 'dashed: 45°, the largest range', 'var(--ink-2)', 11, 'end'),
)

_hx, _hy, _hR, _hH = 90, 50, 240, 150
_xp = 0.6 * _hR
_P2 = (_hx + _xp, _hy + _hH * (_xp / _hR) ** 2)
_slope = 2 * _hH * _xp / _hR ** 2
FIG_HORIZONTAL = _svg(
    420, 235, 'Ball launched horizontally from a cliff of height h; at a later point its velocity has horizontal part u and vertical part gt',
    '<rect x="24" y="50" width="66" height="150" style="fill:var(--surface-2);stroke:var(--ink-2);stroke-width:1.2"/>',
    _line(15, 200, 410, 200, 'var(--ink-2)', 1.5),
    _curve([(_hx + _hR * k / 40, _hy + _hH * (k / 40) ** 2) for k in range(41)], 'var(--line-2, #C9CEDA)', 2.5),
    _arrow(_hx, _hy, _hx + 55, _hy, 'var(--indigo)', 2.6), _text(_hx + 30, _hy - 8, 'u', 'var(--indigo)', 13, 'middle', IT),
    _dot(_hx, _hy),
    _arrow(*_P2, _P2[0] + 60, _P2[1], 'var(--teal)', 2.2), _arrow(*_P2, _P2[0], _P2[1] + 60 * _slope, 'var(--coral)', 2.2),
    _arrow(*_P2, _P2[0] + 60, _P2[1] + 60 * _slope, 'var(--indigo)', 2.6),
    _text(_P2[0] + 62, _P2[1] - 4, _lab('v', 'x', ' = u'), 'var(--teal)', 11), _text(_P2[0] - 6, _P2[1] + 40, _lab('v', 'y', ' = gt'), 'var(--coral)', 11, 'end'),
    _text(_P2[0] + 64, _P2[1] + 50, 'v', 'var(--indigo)', 13, extra=IT),
    _arc(_P2[0], _P2[1], 22, -math.degrees(math.atan(_slope)), 0), _text(_P2[0] + 26, _P2[1] + 16, 'φ', 'var(--ink-2)', 12),
    _line(14, 50, 14, 200, 'var(--ink-2)', 1), _text(10, 128, 'h', 'var(--ink)', 13, 'end', IT),
    _line(_hx, 214, _hx + _hR, 214, 'var(--ink-2)', 1), _text(_hx + _hR / 2, 228, 'R = u√(2h/g)', 'var(--ink)', 12, 'middle'),
    _text(410, 40, 'tan φ = gt/u', 'var(--ink-2)', 12, 'end'),
)

_al = 20
_ix0, _iy0 = 30, 215
_lx, _ly = 50, _iy0 - 20 * math.tan(math.radians(_al))
_phi = 55
_u2 = 280 / (2 * math.cos(math.radians(_phi)) * (math.sin(math.radians(_phi)) - math.tan(math.radians(_al)) * math.cos(math.radians(_phi))))
_uu = math.sqrt(_u2)
_tf = 2 * _uu * (math.sin(math.radians(_phi)) - math.tan(math.radians(_al)) * math.cos(math.radians(_phi)))
_traj = [(_lx + _uu * math.cos(math.radians(_phi)) * t, _ly - (_uu * math.sin(math.radians(_phi)) * t - t * t / 2))
         for t in [_tf * k / 48 for k in range(49)]]
_land = _traj[-1]
_gx, _gy = 330, 40
FIG_INCLINE = _svg(
    420, 230, 'Projectile launched at angle theta to an incline of angle alpha, with axes along and perpendicular to the incline and the components of g',
    f'<polygon points="{_ix0},{_iy0} 410,{_iy0} 410,{_f(_iy0 - 380 * math.tan(math.radians(_al)))}" style="fill:var(--surface-2);stroke:var(--ink-2);stroke-width:1.2"/>',
    _curve(_traj, 'var(--line-2, #C9CEDA)', 2.5), _dot(*_land, 'var(--coral)', 4),
    _arrow(_lx, _ly, *_polar(_lx, _ly, 70, _phi), 'var(--indigo)', 2.6),
    _arrow(_lx, _ly, *_polar(_lx, _ly, 95, _al), 'var(--ink-2)', 1.3, 7, True),
    _arrow(_lx, _ly, *_polar(_lx, _ly, 60, _al + 90), 'var(--ink-2)', 1.3, 7, True),
    _text(*_polar(_lx, _ly, 102, _al), "x′", 'var(--ink-2)', 12), _text(*_polar(_lx - 14, _ly, 62, _al + 90), "y′", 'var(--ink-2)', 12),
    _text(*_polar(_lx + 4, _ly, 76, _phi), 'u', 'var(--indigo)', 13, extra=IT),
    _arc(_lx, _ly, 30, _al, _phi, 'var(--indigo)'), _text(*_polar(_lx, _ly + 3, 38, (_al + _phi) / 2), 'θ', 'var(--indigo)', 12),
    _arc(_ix0, _iy0, 40, 0, _al), _text(_ix0 + 46, _iy0 - 4, 'α', 'var(--ink-2)', 12),
    _text(_land[0] - 8, _land[1] + 22, 'lands here: range L along the slope', 'var(--coral)', 11, 'end'),
    _arrow(_gx, _gy, _gx, _gy + 55, 'var(--plum)', 2.2), _text(_gx + 5, _gy + 50, 'g', 'var(--plum)', 13, extra=IT),
    _arrow(_gx, _gy, *_polar(_gx, _gy, 55 * math.sin(math.radians(_al)), 180 + _al), 'var(--plum)', 1.6, 7, True),
    _arrow(_gx, _gy, *_polar(_gx, _gy, 55 * math.cos(math.radians(_al)), _al - 90), 'var(--plum)', 1.6, 7, True),
    _text(_gx - 22, _gy - 6, 'g sin α', 'var(--plum)', 11, 'end'), _text(_gx + 26, _gy + 30, 'g cos α', 'var(--plum)', 11),
)

_A = (130, 190)
_uend = _polar(*_A, 120, 120)
FIG_RIVER = _svg(
    420, 220, 'River crossing: the swimmer heads upstream at angle theta from the perpendicular so that the current cancels the upstream part and the resultant is straight across',
    '<rect x="15" y="40" width="395" height="150" style="fill:var(--water-soft);stroke:none"/>',
    _line(15, 40, 410, 40, 'var(--ink-2)', 2), _line(15, 190, 410, 190, 'var(--ink-2)', 2),
    _arrow(300, 130, 380, 130, 'var(--water)', 2), _arrow(300, 160, 380, 160, 'var(--water)', 2),
    _text(340, 120, 'current w', 'var(--water)', 12, 'middle'),
    _arrow(*_A, *_uend, 'var(--indigo)', 2.6),
    _arrow(*_uend, _A[0], _uend[1], 'var(--water)', 2.2),
    _arrow(*_A, _A[0], _uend[1] + 2, 'var(--coral)', 2.8),
    _line(_A[0], _uend[1], _A[0], 40, 'var(--coral)', 1.3, True),
    _dot(*_A), _dot(_A[0], 40), _text(_A[0] + 8, 205, 'A', 'var(--ink)', 12), _text(_A[0] + 8, 32, 'B (directly opposite A)', 'var(--ink)', 12),
    _text(_uend[0] - 6, _uend[1] + 30, 'u', 'var(--indigo)', 13, 'end', IT),
    _text((_uend[0] + _A[0]) / 2, _uend[1] - 6, 'w', 'var(--water)', 13, 'middle', IT),
    _text(_A[0] + 8, (_A[1] + _uend[1]) / 2, 'v = √(u² − w²)', 'var(--coral)', 12),
    _arc(*_A, 30, 90, 120), _text(*_polar(_A[0], _A[1], 40, 106), 'θ', 'var(--ink-2)', 12, 'middle'),
    _text(250, 70, 'sin θ = w/u', 'var(--ink-2)', 12), _text(250, 86, 'time = d / (u cos θ)', 'var(--ink-2)', 12),
)

_C, _rc = (110, 120), 80
_p1, _p2 = _polar(*_C, _rc, 65), _polar(*_C, _rc, 115)
_v1, _v2 = _polar(0, 0, 62, 155), _polar(0, 0, 62, 205)
_T = (320, 55)
FIG_DELTAV = _svg(
    420, 220, 'Velocities at two nearby points on a circle and the triangle showing that the change in velocity points toward the centre',
    f'<circle cx="{_C[0]}" cy="{_C[1]}" r="{_rc}" style="fill:none;stroke:var(--line-2, #C9CEDA);stroke-width:2"/>',
    _dot(*_C), _text(_C[0] + 6, _C[1] + 14, 'centre', 'var(--ink-2)', 11),
    _line(*_C, *_p1, 'var(--ink-2)', 1, True), _line(*_C, *_p2, 'var(--ink-2)', 1, True),
    _arc(*_C, 22, 65, 115), _text(_C[0], _C[1] - 28, 'Δθ', 'var(--ink-2)', 11, 'middle'),
    _arrow(*_p1, _p1[0] + _v1[0], _p1[1] + _v1[1], 'var(--teal)', 2.6), _arrow(*_p2, _p2[0] + _v2[0], _p2[1] + _v2[1], 'var(--indigo)', 2.6),
    _dot(*_p1), _dot(*_p2),
    _text(_p1[0] + 4, _p1[1] - 6, 'v₁', 'var(--teal)', 13, extra=IT), _text(_p2[0] - 50, _p2[1] + 34, 'v₂', 'var(--indigo)', 13, extra=IT),
    _arrow(*_T, _T[0] + _v1[0] * 1.6, _T[1] + _v1[1] * 1.6, 'var(--teal)', 2.4),
    _arrow(*_T, _T[0] + _v2[0] * 1.6, _T[1] + _v2[1] * 1.6, 'var(--indigo)', 2.4),
    _arrow(_T[0] + _v1[0] * 1.6, _T[1] + _v1[1] * 1.6, _T[0] + _v2[0] * 1.6, _T[1] + _v2[1] * 1.6, 'var(--coral)', 2.8),
    _text(_T[0] - 56, _T[1] - 6, 'v₁', 'var(--teal)', 13, extra=IT), _text(_T[0] - 40, _T[1] + 50, 'v₂', 'var(--indigo)', 13, extra=IT),
    _text(_T[0] - 100, _T[1] + 36, 'Δv', 'var(--coral)', 13, 'end', IT),
    _text(410, 160, '|Δv| = 2v sin(Δθ/2) ≈ v Δθ', 'var(--ink)', 12, 'end'),
    _text(410, 178, 'Δv points toward the centre', 'var(--coral)', 12, 'end'),
    _text(410, 196, 'so a = v·(dθ/dt) = v²/r inward', 'var(--ink)', 12, 'end'),
)

_Cn, _rn = (140, 125), 85
_pn = _polar(*_Cn, _rn, 25)
_at = _polar(0, 0, 45, 115)
_ar = _polar(0, 0, 70, 205)
FIG_NONUNIFORM = _svg(
    420, 230, 'Non-uniform circular motion: tangential acceleration along the velocity and radial acceleration toward the centre combine to a total acceleration at angle beta to the radius',
    f'<circle cx="{_Cn[0]}" cy="{_Cn[1]}" r="{_rn}" style="fill:none;stroke:var(--line-2, #C9CEDA);stroke-width:2"/>',
    _dot(*_Cn), _line(*_Cn, *_pn, 'var(--ink-2)', 1, True),
    _arrow(*_pn, _pn[0] + _at[0], _pn[1] + _at[1], 'var(--teal)', 2.6),
    _arrow(*_pn, _pn[0] + _ar[0], _pn[1] + _ar[1], 'var(--coral)', 2.6),
    _arrow(*_pn, _pn[0] + _at[0] + _ar[0], _pn[1] + _at[1] + _ar[1], 'var(--indigo)', 3),
    _line(_pn[0] + _at[0], _pn[1] + _at[1], _pn[0] + _at[0] + _ar[0], _pn[1] + _at[1] + _ar[1], 'var(--ink-2)', 1, True),
    _line(_pn[0] + _ar[0], _pn[1] + _ar[1], _pn[0] + _at[0] + _ar[0], _pn[1] + _at[1] + _ar[1], 'var(--ink-2)', 1, True),
    _dot(*_pn),
    _text(_pn[0] + _at[0] + 6, _pn[1] + _at[1] - 2, _lab('a', 't', ' = dv/dt'), 'var(--teal)', 12),
    _text(_pn[0] + _ar[0] / 2 - 4, _pn[1] + _ar[1] / 2 + 34, _lab('a', 'r', ' = v²/r'), 'var(--coral)', 12, 'middle'),
    _text(_pn[0] + _at[0] + _ar[0] - 6, _pn[1] + _at[1] + _ar[1] - 6, 'a', 'var(--indigo)', 14, 'end', IT),
    _arc(*_pn, 34, 205 - math.degrees(math.atan(45 / 70)), 205), _text(*_polar(_pn[0], _pn[1] + 4, 46, 189), 'β', 'var(--ink-2)', 12, 'middle'),
    _text(410, 70, 'speed increasing:', 'var(--ink-2)', 12, 'end'), _text(410, 86, _lab('a', 't', ' points along v'), 'var(--ink-2)', 12, 'end'),
    _text(410, 120, _lab('a = √(a', 't', '² + a', 'r', '²)'), 'var(--ink)', 12, 'end'), _text(410, 138, _lab('tan β = a', 't', ' / a', 'r'), 'var(--ink)', 12, 'end'),
)

AR_OPTS = ['Both A and R are true, and R correctly explains A',
           'Both A and R are true, but R does not explain A',
           'A is true but R is false',
           'A is false but R is true']
ST_OPTS = ['Both statements are true', 'Statement I is true, Statement II is false',
           'Statement I is false, Statement II is true', 'Both statements are false']


DEEP = {
    'plane-kinematics': dict(
        level='core',
        notes=[
            ('Average and instantaneous quantities in a plane', r'''<ul><li>Average velocity \(= \Delta\vec r/\Delta t\). It points along the chord joining the two positions.</li>
<li>Instantaneous velocity \(\vec v = d\vec r/dt = \dfrac{dx}{dt}\hat i + \dfrac{dy}{dt}\hat j\). As Δt shrinks, the chord turns into the tangent, so \(\vec v\) is always tangent to the path.</li>
<li>Acceleration \(\vec a = d\vec v/dt\). It need not be along the path or along \(\vec v\).</li>
<li>Average speed (path length ÷ time) is never less than the magnitude of average velocity. They are equal only for straight-line motion without turning back.</li></ul>'''),
            ('Is the speed rising or falling? Is the path straight?', r'''<p>Split \(\vec a\) into a part along \(\vec v\) and a part across it.</p>
<ul><li>\(\vec v\cdot\vec a &gt; 0\): speed increasing. \(\vec v\cdot\vec a &lt; 0\): speed decreasing. \(\vec v\cdot\vec a = 0\) at every instant: speed constant (only the direction changes).</li>
<li>The along-velocity part has size \(a_t = \vec v\cdot\vec a / v\). The across part bends the path.</li>
<li>With constant \(\vec a\): if \(\vec u\) is zero or parallel to \(\vec a\), the path is a straight line. Otherwise it is a parabola.</li></ul>'''),
            ('Calculus recipe for r(t) questions', r'''<ol><li>Write x(t) and y(t) separately.</li><li>Differentiate once for \(v_x, v_y\); again for \(a_x, a_y\).</li>
<li>Substitute the time only at the end, then combine with Pythagoras.</li>
<li>For the path, eliminate t between x and y. For example \(x = 3t,\ y = 4t^2\) gives \(y = 4x^2/9\), a parabola.</li></ol>'''),
        ],
        formulas=[
            dict(title='Velocity and acceleration from r(t)', formula=r'\vec v=\frac{dx}{dt}\hat i+\frac{dy}{dt}\hat j,\qquad \vec a=\frac{d^2x}{dt^2}\hat i+\frac{d^2y}{dt^2}\hat j',
                 symbols='x, y are coordinates (m) as functions of time t (s); v in m/s; a in m/s².'),
            dict(title='Rate of change of speed', formula=r'a_t=\frac{dv}{dt}=\frac{\vec v\cdot\vec a}{v}',
                 symbols='aₜ is the tangential acceleration (m/s²); v is the speed (m/s), nonzero; a is the full acceleration vector.'),
        ],
        figure=dict(svg=FIG_PATH,
                    caption=r'The displacement \(\Delta\vec r\) is the chord between two positions. In the limit Δt → 0 it lines up with the tangent, which is why velocity is always along the path.'),
        traps=[r'A zero y-acceleration does not mean a zero y-velocity. In a horizontal projectile, \(a_x = 0\) but \(v_x = u\) throughout.',
               r'Speed is \(\sqrt{v_x^2 + v_y^2}\), not \(v_x + v_y\). With \(v_x = 3\) and \(v_y = 4\) m/s the speed is 5 m/s, not 7 m/s.'],
        exam=r'''<ul><li>“\(\vec r = 3t\hat i + 2t^2\hat j\). Find the speed / acceleration at t = 1 s.”</li>
<li>“\(v_x\)–t and \(v_y\)–t graphs are given. Find the displacement after 2 s.”</li>
<li>“The path of a particle with x = at, y = bt² is a …” (parabola).</li>
<li>“The angle between velocity and acceleration is obtuse. The speed is …” (decreasing).</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'A particle has \(\vec r = (2t^2\hat i + 3t\hat j)\) m. Find its velocity, speed and acceleration at t = 1 s.',
                 steps=[r'\(\vec v = d\vec r/dt = 4t\hat i + 3\hat j\). At t = 1 s, \(\vec v = (4\hat i + 3\hat j)\) m/s.',
                        r'Speed \(= \sqrt{16 + 9} = 5\) m/s.',
                        r'\(\vec a = d\vec v/dt = 4\hat i\) m/s², constant and along x.',
                        r'Because \(\vec u = 3\hat j\) is not parallel to \(\vec a\), the path curves: it is a parabola.'],
                 answer=r'\(\vec v = 4\hat i + 3\hat j\) m/s, speed 5 m/s, \(\vec a = 4\hat i\) m/s²'),
            dict(tag='Graph', q=r'For a particle starting at the origin, the \(v_x\)–t graph is a horizontal line at 3 m/s. The \(v_y\)–t graph is a straight line rising from 0 to 8 m/s in 2 s. Find the displacement after 2 s.',
                 steps=[r'x-displacement = area under \(v_x\)–t = 3 × 2 = 6 m.',
                        r'y-displacement = area of the triangle under \(v_y\)–t = ½ × 2 × 8 = 8 m.',
                        r'\(|\Delta\vec r| = \sqrt{36 + 64} = 10\) m, at \(\tan^{-1}(8/6) \approx 53^\circ\) to the x-axis.'],
                 answer=r'10 m at 53° to the x-axis'),
            dict(tag='Concept', q=r'Find the path of a particle with x = 2t and y = 4t − t² (SI units).',
                 steps=[r'From x = 2t, t = x/2.',
                        r'Substitute: \(y = 4(x/2) - (x/2)^2 = 2x - x^2/4\).',
                        r'This is a downward-opening parabola, like a projectile: constant \(a_y = -2\) m/s² with an initial velocity that is not along it.'],
                 answer=r'\(y = 2x - x^2/4\), a parabola'),
        ],
        practice=[
            dict(q=r'A particle moves with \(\vec r = 3t\hat i + 2t^2\hat j + 5\hat k\) (SI units). Its speed at t = 1 s is',
                 options=['7 m/s', '5 m/s', '4 m/s', '3 m/s'], answer=1, type='numerical',
                 explanation=r'\(\vec v = 3\hat i + 4t\hat j\), which is \(3\hat i + 4\hat j\) at t = 1 s, so speed = 5 m/s. 7 m/s adds the components as numbers. The constant 5k̂ does not contribute to velocity.'),
            dict(q=r'At some instant the angle between a particle’s velocity and acceleration is 120°. At that instant its speed is',
                 options=['increasing', 'constant', 'decreasing', 'zero'], answer=2, type='concept',
                 explanation=r'The component of \(\vec a\) along \(\vec v\) is \(a\cos120^\circ &lt; 0\), so it opposes the motion and the speed falls. A constant speed needs exactly 90°. Nothing says the speed is zero; it is only decreasing.'),
            dict(q=r'For a particle, the x–t graph is a straight line through the origin with slope 4 m/s and the y–t graph is the curve \(y = t^2\) (SI units). The path in the xy-plane is',
                 options=['a straight line', 'a circle', 'a hyperbola', 'a parabola'], answer=3, type='graph',
                 explanation=r'x = 4t and y = t², so \(y = x^2/16\), a parabola. The x-motion is uniform and the y-motion has constant acceleration, which is exactly the projectile pattern. A straight line would need both coordinates linear in t.'),
            dict(q=r'A particle starts at the origin with \(\vec u = 4\hat i\) m/s and constant \(\vec a = 2\hat j\) m/s². When its x-coordinate is 8 m, its y-coordinate and speed are',
                 options=[r'4 m and \(4\sqrt2\) m/s', r'8 m and 8 m/s', r'4 m and 8 m/s', r'2 m and \(4\sqrt2\) m/s'], answer=0, type='numerical',
                 explanation=r'x = 4t = 8 gives t = 2 s. Then \(y = \tfrac12(2)(4) = 4\) m and \(\vec v = 4\hat i + 4\hat j\), so speed \(= 4\sqrt2 \approx 5.7\) m/s. 8 m/s adds the components; 8 m forgets the ½.'),
        ],
    ),

    'plane-projectiles': dict(
        level='exam',
        notes=[
            ('Derivation: T, H and R from components', r'''<p>Take +y upward. Initial components: \(u_x = u\cos\theta\), \(u_y = u\sin\theta\). Accelerations: \(a_x = 0\), \(a_y = -g\).</p>
<ol><li><strong>Time to the top.</strong> \(v_y = u\sin\theta - gt = 0\) gives \(t_{\rm up} = u\sin\theta/g\).</li>
<li><strong>Time of flight.</strong> On level ground the fall mirrors the rise, so \(T = 2t_{\rm up} = 2u\sin\theta/g\). (Or set y = 0 in \(y = u\sin\theta\,t - \tfrac12gt^2\).)</li>
<li><strong>Maximum height.</strong> \(v_y^2 = u_y^2 - 2gy\) with \(v_y = 0\): \(H = u^2\sin^2\theta/2g\).</li>
<li><strong>Range.</strong> Horizontal speed is constant, so \(R = u\cos\theta \cdot T = 2u^2\sin\theta\cos\theta/g = u^2\sin2\theta/g\).</li></ol>'''),
            ('Velocity at any instant and at the top', r'''<ul><li>\(v_x = u\cos\theta\) always; \(v_y = u\sin\theta - gt\). The direction is \(\tan\varphi = v_y/v_x\).</li>
<li>At the top, \(v = u\cos\theta\) (not zero), and kinetic energy is \(K\cos^2\theta\), where K is the launch KE.</li>
<li>At height h on the way up or down, \(v^2 = u^2 - 2gh\), whatever the angle.</li>
<li>Over the full flight on level ground, \(\Delta\vec v = 2u\sin\theta\) downward and \(\Delta\vec p = 2mu\sin\theta\) downward. Over half the flight it is \(u\sin\theta\) downward.</li>
<li>Velocity and acceleration are perpendicular only at the top.</li></ul>'''),
            ('Standard relations between T, H and R', r'''<ul><li>\(R_{\max} = u^2/g\) at θ = 45°. Then \(H = R_{\max}/4\).</li>
<li>\(\dfrac{H}{R} = \dfrac{\tan\theta}{4}\), so \(R = 4H\cot\theta\). R = H when tan θ = 4 (θ ≈ 76°).</li>
<li>\(H = gT^2/8\). This links height to flight time with no angle or speed needed.</li>
<li>Scaling at a fixed angle: T ∝ u, while H and R ∝ u². Doubling the speed doubles T but makes H and R four times larger.</li></ul>'''),
        ],
        formulas=[
            dict(title='Height and range ratio', formula=r'R=4H\cot\theta,\qquad H=\frac{gT^2}{8}',
                 symbols='R range (m), H maximum height (m), T time of flight (s), θ launch angle above horizontal; level ground, no drag.'),
            dict(title='Maximum range', formula=r'R_{\max}=\frac{u^2}{g}\ \ (\theta=45^\circ),\qquad H_{45^\circ}=\frac{u^2}{4g}=\frac{R_{\max}}{4}',
                 symbols='u launch speed (m/s); g = 10 m/s² unless stated. Same launch and landing level.'),
            dict(title='Kinetic energy at the top', formula=r'K_{\rm top}=K\cos^2\theta',
                 symbols='K is the launch kinetic energy (J); θ the launch angle. Only the horizontal component survives at the top.'),
        ],
        figure=dict(svg=FIG_PROJECTILE,
                    caption=r'The horizontal component \(u\cos\theta\) is the same at launch, at the top and at landing. The vertical component shrinks to zero at the top and returns as \(u\sin\theta\) downward on landing.'),
        traps=[r'At the highest point the speed is \(u\cos\theta\), not zero. Only the vertical component is zero. The acceleration is still g downward.',
               r'The momentum change over the whole flight is not zero: the vertical momentum reverses, so \(|\Delta\vec p| = 2mu\sin\theta\), directed downward.'],
        exam=r'''<ul><li>“Find T, H and R” for given u and θ (often 37°/53° with g = 10).</li>
<li>“The KE at the highest point is one-fourth of the launch KE. Find θ.”</li>
<li>“For what angle is R = H?” or “R = 4√3 H?”</li>
<li>“Change in momentum between launch and landing / between launch and the top.”</li>
<li>Graph questions: \(v_y\)–t is a straight line of slope −g; \(v_x\)–t is flat; y–t is a downward parabola.</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'A ball is launched at 50 m/s at 37° above level ground. Find the time of flight, maximum height and range (g = 10 m/s², sin 37° = 0.6).',
                 steps=[r'\(u_x = 50 \times 0.8 = 40\) m/s and \(u_y = 50 \times 0.6 = 30\) m/s.',
                        r'\(T = 2u_y/g = 60/10 = 6\) s.',
                        r'\(H = u_y^2/2g = 900/20 = 45\) m.',
                        r'\(R = u_xT = 40 \times 6 = 240\) m. Check: \(u^2\sin74^\circ/g = 250 \times 0.96 = 240\) m.'],
                 answer=r'T = 6 s, H = 45 m, R = 240 m'),
            dict(tag='Ratio', q=r'The kinetic energy of a projectile at its highest point is one-fourth of its kinetic energy at launch. Find the launch angle.',
                 steps=[r'At the top only \(u\cos\theta\) remains, so \(K_{\rm top} = K\cos^2\theta\).',
                        r'\(\cos^2\theta = 1/4\), so cos θ = 1/2.',
                        r'θ = 60°. A common slip is to set cos θ = 1/4 by forgetting the square.'],
                 answer=r'60°'),
            dict(tag='Numerical', q=r'A 0.5 kg ball is thrown at 20 m/s at 30° above level ground. Find the change in its momentum (a) from launch to the top, (b) from launch to landing.',
                 steps=[r'Only the vertical component changes. \(u_y = 20\sin30^\circ = 10\) m/s.',
                        r'(a) At the top, \(v_y = 0\): \(\Delta p = m(0 - 10) = -5\) kg m/s, so 5 kg m/s downward.',
                        r'(b) On landing, \(v_y = -10\) m/s: \(\Delta p = 0.5(-10 - 10) = -10\) kg m/s, so 10 kg m/s downward.',
                        r'Check with impulse: \(mgT = 0.5 \times 10 \times 2 = 10\) N s downward.'],
                 answer=r'(a) 5 kg m/s downward, (b) 10 kg m/s downward'),
            dict(tag='Concept', q=r'At what launch angle are the range and maximum height equal?',
                 steps=[r'\(R = 4H\cot\theta\). Setting R = H gives \(\cot\theta = 1/4\).',
                        r'\(\theta = \tan^{-1}4 \approx 76^\circ\).'],
                 answer=r'\(\tan^{-1}4 \approx 76^\circ\)'),
        ],
        practice=[
            dict(q=r'A projectile on level ground stays in the air for 4 s. Its maximum height is (g = 10 m/s²)',
                 options=['40 m', '20 m', '80 m', '10 m'], answer=1, type='numerical',
                 explanation=r'\(H = gT^2/8 = 10 \times 16/8 = 20\) m. Equivalently it rises for 2 s, so \(H = \tfrac12 g(2)^2 = 20\) m. 80 m uses the full 4 s as the rise time.'),
            dict(q=r'For a projectile, the range is \(4\sqrt3\) times the maximum height. The launch angle is',
                 options=['60°', '45°', '37°', '30°'], answer=3, type='numerical',
                 explanation=r'\(R = 4H\cot\theta\), so \(\cot\theta = \sqrt3\) and θ = 30°. 60° would give \(R = 4H/\sqrt3\), which is the reciprocal relation.'),
            dict(q=r'Taking upward as positive, which graph correctly shows the vertical velocity of a projectile against time from launch to landing on level ground?',
                 options=[r'A horizontal line at \(u\sin\theta\)', r'A straight line of slope −g, crossing zero at T/2 and ending at \(-u\sin\theta\)', 'A downward parabola with its peak at T/2', r'A straight line from \(u\sin\theta\) to zero at T'], answer=1, type='graph',
                 explanation=r'\(v_y = u\sin\theta - gt\) is linear with slope −g. It is zero at the top (t = T/2) and reaches \(-u\sin\theta\) on landing. The horizontal line describes \(v_x\); the parabola describes y–t; reaching zero only at T ignores the descent.'),
            dict(q=r'For a projectile launched and landing on level ground, which quantities are the same at launch and at landing? (a) speed (b) horizontal velocity (c) vertical velocity (d) kinetic energy',
                 options=['(a) and (b) only', '(b) and (c) only', '(a), (b) and (d)', 'all four'], answer=2, type='multi',
                 explanation=r'The horizontal velocity never changes and the vertical velocity has the same size but reversed sign. So the speed and KE match, while the vertical velocity (a vector component) does not. “All four” misses that sign reversal.'),
        ],
    ),

    'plane-horizontal': dict(
        level='core',
        notes=[
            ('Path, impact speed and impact angle', r'''<p>Launch horizontally at speed u from height h, with the origin at the launch point and y measured downward.</p>
<ol><li>x = ut and y = ½gt². Eliminating t: \(y = \dfrac{g x^2}{2u^2}\), half of a parabola.</li>
<li>At impact, \(v_x = u\) and \(v_y = \sqrt{2gh}\), so \(v = \sqrt{u^2 + 2gh}\).</li>
<li>Angle of velocity below the horizontal: \(\tan\varphi = gt/u\). Angle of the displacement: \(\tan\alpha = y/x = gt/2u\). Hence \(\tan\varphi = 2\tan\alpha\) at every instant.</li></ol>'''),
            ('Launch at an angle from a height', r'''<p>Keep one origin at the launch point and one sign convention. For a launch at θ above the horizontal from height h:</p>
\[-h = u\sin\theta\,t - \tfrac12gt^2\]
<p>Solve the quadratic and keep the positive root. The horizontal distance is then \(u\cos\theta\,t\). The impact speed is \(\sqrt{u^2 + 2gh}\) for <em>any</em> launch angle, because energy conservation does not care about direction.</p>'''),
            ('Objects released from moving carriers', r'''<p>A packet released from a plane flying horizontally at constant velocity keeps the plane’s horizontal velocity. With no drag it stays vertically below the plane while it falls. A passenger sees it fall straight down; a person on the ground sees a parabola. It lands ahead of the point above which it was released, by a distance \(u\sqrt{2h/g}\).</p>'''),
        ],
        formulas=[
            dict(title='Impact speed and direction', formula=r'v=\sqrt{u^2+2gh},\qquad \tan\varphi=\frac{\sqrt{2gh}}{u}',
                 symbols='u horizontal launch speed (m/s); h height fallen (m); φ angle of the velocity below the horizontal at impact. No drag, constant g.'),
            dict(title='Path and angle relation', formula=r'y=\frac{gx^2}{2u^2},\qquad \tan\varphi=2\tan\alpha',
                 symbols='x horizontal and y downward distance from the launch point (m); φ angle of velocity and α angle of displacement, both below the horizontal.'),
        ],
        figure=dict(svg=FIG_HORIZONTAL,
                    caption=r'After a horizontal launch, \(v_x\) stays equal to u while \(v_y = gt\) grows. The velocity tilts more steeply as the ball falls.'),
        traps=[r'A packet dropped from a moving plane does not fall straight down relative to the ground. It moves forward with the plane’s speed and lands ahead of the release point.',
               r'Doubling the height does not double the range. Range ∝ \(\sqrt h\), so doubling h increases it by a factor \(\sqrt2\).'],
        exam=r'''<ul><li>“A ball rolls off a table of height … and lands … away. Find its speed on leaving the table.”</li>
<li>“A bomb is released from a plane at height h flying at v. Where does it land relative to the plane?”</li>
<li>“Two balls are thrown horizontally from heights h and 4h with the same speed. Ratio of ranges / times.”</li>
<li>“The angle of the velocity with the horizontal on impact is …”</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'A plane flies horizontally at 100 m/s at an altitude of 500 m and releases a packet. Where does the packet land, and where is the plane at that moment? (g = 10 m/s², no drag)',
                 steps=[r'Fall time: \(t = \sqrt{2h/g} = \sqrt{1000/10} = 10\) s.',
                        r'Horizontal distance covered by the packet: 100 × 10 = 1000 m ahead of the release point.',
                        r'The plane also moves 1000 m in 10 s, so it is directly above the packet when it lands.'],
                 answer=r'1000 m ahead of the release point, directly below the plane'),
            dict(tag='Numerical', q=r'A ball is thrown from the top of a 20 m tower at 25 m/s, 37° above the horizontal. Find when and how far from the base it lands (g = 10 m/s², sin 37° = 0.6).',
                 steps=[r'Components: \(u_x = 20\) m/s, \(u_y = 15\) m/s.',
                        r'Vertical, origin at the launch point, up positive: \(-20 = 15t - 5t^2\), so \(t^2 - 3t - 4 = 0\).',
                        r'\((t - 4)(t + 1) = 0\). Keep t = 4 s; the negative root has no meaning here.',
                        r'Horizontal distance: \(20 \times 4 = 80\) m. Impact speed: \(\sqrt{25^2 + 2(10)(20)} = \sqrt{1025} \approx 32\) m/s.'],
                 answer=r'After 4 s, 80 m from the base'),
            dict(tag='Ratio', q=r'Ball P is thrown horizontally at speed u from height h. Ball Q is thrown horizontally at speed u from height 4h. Find the ratios of their flight times and ranges.',
                 steps=[r'\(t = \sqrt{2h/g}\), so \(t \propto \sqrt h\): \(t_P : t_Q = 1 : 2\).',
                        r'Range \(= u t\) with the same u, so \(R_P : R_Q = 1 : 2\) as well.',
                        r'Four times the height gives only twice the time and twice the range.'],
                 answer=r'Times 1 : 2, ranges 1 : 2'),
        ],
        practice=[
            dict(q=r'A ball rolls off a horizontal table 1.25 m high and lands 2 m from the foot of the table. Its speed on leaving the table was (g = 10 m/s²)',
                 options=['2 m/s', '4 m/s', '1.6 m/s', '8 m/s'], answer=1, type='numerical',
                 explanation=r'Fall time \(= \sqrt{2 \times 1.25/10} = 0.5\) s. Then u = 2/0.5 = 4 m/s. 1.6 m/s divides the distance by the height, which has no physical basis.'),
            dict(q=r'Two stones are thrown horizontally with the same speed, one from height h and the other from 4h. The ratio of their horizontal ranges is',
                 options=['1 : 4', '1 : √2', '2 : 1', '1 : 2'], answer=3, type='numerical',
                 explanation=r'Range \(= u\sqrt{2h/g} \propto \sqrt h\). With heights in the ratio 1 : 4, the ranges are 1 : 2. 1 : 4 assumes range ∝ h, and 2 : 1 inverts the ratio.'),
            dict(q=r'A plane flies horizontally at constant velocity and drops a packet. Ignoring air resistance, the path of the packet as seen by the pilot is',
                 options=['a vertical straight line', 'a parabola curving forward', 'a parabola curving backward', 'a horizontal straight line'], answer=0, type='concept',
                 explanation=r'The packet keeps the plane’s horizontal velocity, so relative to the pilot it has no horizontal motion and simply falls vertically. The forward parabola is the ground observer’s view. A backward curve would need air drag.'),
            dict(q=r'A ball is thrown horizontally at 10 m/s from a height of 20 m. The angle its velocity makes with the horizontal just before it lands is (g = 10 m/s²)',
                 options=[r'\(\tan^{-1}(1/2)\)', r'45°', r'\(\tan^{-1}2\)', '60°'], answer=2, type='numerical',
                 explanation=r'Fall time = 2 s, so \(v_y = 20\) m/s while \(v_x = 10\) m/s. \(\tan\varphi = 20/10 = 2\). \(\tan^{-1}(1/2)\) is the angle of the displacement (\(\tan\alpha = \tfrac12\tan\varphi\)), not of the velocity.'),
        ],
    ),

    'plane-relative': dict(
        level='core',
        notes=[
            ('Rain and the umbrella', r'''<p>The rain’s velocity as seen by a moving person is \(\vec v_{R/M} = \vec v_R - \vec v_M\). Hold the umbrella against this relative velocity.</p>
<ul><li>Rain falling vertically at \(v_R\), person walking at \(v_M\): the rain appears to come from the front at \(\tan\theta = v_M/v_R\) to the vertical. Tilt the umbrella forward.</li>
<li>If the rain itself is slanted, the person can make it appear vertical by walking with the rain’s horizontal component.</li>
<li>Two-condition questions (“appears vertical at 3 km/h, at 45° at 6 km/h”) are solved by writing the rain’s velocity as \(a\hat i - b\hat j\) and using each condition once.</li></ul>'''),
            ('River crossing at a general heading', r'''<p>Let the river (width d) flow at w along +x and the swimmer’s speed relative to water be u, aimed at angle θ upstream from the straight-across direction.</p>
<ol><li>Across component: \(u\cos\theta\), so the crossing time is \(t = d/(u\cos\theta)\).</li>
<li>Along the bank: \(w - u\sin\theta\), so the drift is \(x = (w - u\sin\theta)\,d/(u\cos\theta)\).</li>
<li>θ = 0: least time \(d/u\), drift \(wd/u\).</li>
<li>\(\sin\theta = w/u\): zero drift (needs u &gt; w), time \(d/\sqrt{u^2 - w^2}\).</li>
<li>If u &lt; w the swimmer cannot reach the point opposite. The least drift is \(d\sqrt{w^2-u^2}/u\), found with \(\sin\theta = u/w\).</li></ol>'''),
            ('Two moving bodies', r'''<p>For two bodies, work in the frame of one of them. The relative velocity tells you the direction of approach; closest approach and “will they collide?” questions become straight-line problems. Two projectiles launched at the same time have the same acceleration g, so their relative acceleration is zero. Each sees the other move in a straight line at constant velocity.</p>'''),
        ],
        formulas=[
            dict(title='Rain seen by a moving person', formula=r'\vec v_{R/M}=\vec v_R-\vec v_M,\qquad \tan\theta=\frac{v_M}{v_R}\ \ (\text{vertical rain})',
                 symbols='v_R rain velocity, v_M person’s velocity (m/s); θ angle of the apparent rain from the vertical. The umbrella is tilted toward the direction of walking.'),
            dict(title='Drift for a general heading', formula=r'x=\frac{(w-u\sin\theta)\,d}{u\cos\theta},\qquad x_{\min}=\frac{d\sqrt{w^2-u^2}}{u}\ \ (u<w)',
                 symbols='d river width (m); u swimmer speed relative to water (m/s); w current speed (m/s); θ heading measured upstream from the perpendicular.'),
        ],
        figure=dict(svg=FIG_RIVER,
                    caption=r'To land directly opposite, the swimmer heads upstream so that the upstream part of \(\vec u\) cancels the current. The remaining across-river speed is \(\sqrt{u^2 - w^2}\).'),
        traps=[r'For vertical rain the umbrella is tilted <em>forward</em>, toward the direction of walking, because the rain appears to come from the front.',
               r'Check whether the heading angle is measured from the bank or from the perpendicular. “120° with the current” and “30° upstream from the perpendicular” are the same heading.'],
        exam=r'''<ul><li>“Rain falls vertically at … A man walks at … At what angle should he hold his umbrella?”</li>
<li>“To a man walking at 3 km/h rain appears vertical; at 6 km/h it appears at 45°. Find the true velocity of rain.”</li>
<li>“In which direction should the swimmer head to reach the point directly opposite? Find the time.”</li>
<li>“If the river flows faster than the swimmer, what is the least drift?”</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'Rain falls vertically at 6 m/s. A cyclist rides east at 8 m/s. How fast does the rain hit her, and at what angle should she hold her umbrella?',
                 steps=[r'\(\vec v_{R/C} = \vec v_R - \vec v_C = (-8\hat i - 6\hat j)\) m/s, with east as +x and up as +y.',
                        r'Relative speed \(= \sqrt{64 + 36} = 10\) m/s.',
                        r'Angle with the vertical: \(\tan\theta = 8/6\), so θ = 53°.',
                        r'The rain comes from the front (east), so the umbrella tilts forward by 53° from the vertical.'],
                 answer=r'10 m/s; tilt the umbrella forward at 53° to the vertical'),
            dict(tag='Two conditions', q=r'To a man walking east at 3 km/h, rain appears to fall vertically. When he walks east at 6 km/h, it appears to fall at 45° to the vertical. Find the actual velocity of the rain.',
                 steps=[r'Let the rain’s velocity be \(a\hat i - b\hat j\) (east +x, up +y).',
                        r'At 3 km/h: relative velocity \((a - 3)\hat i - b\hat j\) is vertical, so a = 3 km/h.',
                        r'At 6 km/h: relative velocity \(-3\hat i - b\hat j\) makes 45° with the vertical, so b = 3 km/h.',
                        r'Rain speed \(= \sqrt{9 + 9} = 3\sqrt2 \approx 4.24\) km/h, moving east and down at 45° to the vertical.'],
                 answer=r'\(3\sqrt2\) km/h at 45° to the vertical, toward the east'),
            dict(tag='Assertion–Reason', q=r'Assertion (A): Two balls thrown at the same time from the same point with different velocities move apart along a straight line as seen from either ball.<br>Reason (R): Both have the same acceleration g, so their relative acceleration is zero.',
                 steps=[r'Relative acceleration: \(\vec g - \vec g = 0\).',
                        r'So the relative velocity stays equal to the initial difference \(\vec u_1 - \vec u_2\).',
                        r'Constant relative velocity from a common start means the separation vector grows along one straight line. A and R are true and R explains A.'],
                 answer=r'Both true; R correctly explains A'),
        ],
        practice=[
            dict(q=r'A swimmer can swim at 4 m/s in still water. A 100 m wide river flows at 2 m/s. To reach the point directly opposite, she should head',
                 options=['at 30° upstream from the perpendicular to the bank', 'straight across', 'at 60° upstream from the perpendicular', 'at 30° downstream from the perpendicular'], answer=0, type='numerical',
                 explanation=r'She needs \(u\sin\theta = w\), so sin θ = 2/4 and θ = 30° upstream. That is 120° to the direction of flow. Heading straight across gives drift; 60° would over-correct; heading downstream adds to the drift.'),
            dict(q=r'Rain is falling vertically. A man walking at 5 m/s sees the rain falling at 30° to the vertical. The speed of the rain relative to the ground is',
                 options=['5 m/s', r'\(5/\sqrt3\) m/s', r'\(5\sqrt3\) m/s', '10 m/s'], answer=2, type='numerical',
                 explanation=r'\(\tan30^\circ = v_M/v_R\), so \(v_R = 5/\tan30^\circ = 5\sqrt3 \approx 8.7\) m/s. \(5/\sqrt3\) uses tan 60° by mistake, and 10 m/s is the apparent speed seen by the man, not the rain’s ground speed.'),
            dict(q=r'Assertion (A): For the shortest crossing time, a swimmer should head perpendicular to the current.<br>Reason (R): The current has no component across the river, so only the swimmer’s across-river velocity decides the crossing time.',
                 options=AR_OPTS, answer=0, type='ar',
                 explanation=r'Crossing time is \(d/(u\cos\theta)\), smallest when cos θ = 1. The current only shifts the landing point. So A is true and R gives exactly the reason.'),
            dict(q=r'A man who swims at 3 m/s in still water wants to cross a 60 m wide river flowing at 5 m/s. The least possible drift downstream is',
                 options=['100 m', '60 m', '80 m', '36 m'], answer=2, type='numerical',
                 explanation=r'Since u &lt; w, zero drift is impossible. The least drift is \(d\sqrt{w^2-u^2}/u = 60 \times 4/3 = 80\) m, obtained by heading so that sin θ = u/w = 0.6 upstream from the perpendicular. 100 m is the drift when heading straight across (60 × 5/3).'),
        ],
    ),

    'plane-circular': dict(
        level='core',
        notes=[
            ('Derivation: a = v²/r', r'''<ol><li>In a short time Δt the particle turns through Δθ. Its speed stays v, so \(\vec v_1\) and \(\vec v_2\) have equal length and differ in direction by Δθ.</li>
<li>Draw them from one point: \(|\Delta\vec v| = 2v\sin(\Delta\theta/2) \approx v\,\Delta\theta\) for small Δθ.</li>
<li>Divide by Δt: \(a = v\,\dfrac{\Delta\theta}{\Delta t} = v\omega = \dfrac{v^2}{r}\), using ω = v/r.</li>
<li>As Δθ → 0, \(\Delta\vec v\) becomes perpendicular to \(\vec v\) and points to the centre. That is why it is called centripetal (centre-seeking).</li></ol>'''),
            ('What stays constant in uniform circular motion', r'''<ul><li><strong>Constant:</strong> speed, kinetic energy, angular speed ω, the magnitude of acceleration, the magnitude of momentum.</li>
<li><strong>Changing:</strong> velocity, momentum and acceleration, all as vectors, because their directions turn.</li>
<li>Over half a revolution: displacement 2r, distance πr, \(|\Delta\vec v| = 2v\). Average velocity \(= 2r/(T/2) = 4r/T\); average speed \(= 2\pi r/T\).</li>
<li>Over a full revolution: displacement, \(\Delta\vec v\) and average velocity are all zero.</li></ul>'''),
            ('Using frequency and period', r'''<p>ω = 2π/T = 2πf. So \(a_c = \omega^2r = 4\pi^2r/T^2 = 4\pi^2f^2r\). For the hands of a clock: second hand T = 60 s, minute hand T = 3600 s, hour hand T = 43 200 s. The ratio of the angular speeds of the minute and hour hands is 12 : 1.</p>'''),
        ],
        formulas=[
            dict(title='Change in velocity after turning by θ', formula=r'|\Delta\vec v|=2v\sin\frac{\theta}{2}',
                 symbols='v constant speed (m/s); θ angle turned. θ = 90° gives v√2, θ = 180° gives 2v, θ = 360° gives 0.'),
            dict(title='Centripetal acceleration from T or f', formula=r'a_c=\omega^2r=\frac{4\pi^2r}{T^2}=4\pi^2f^2r',
                 symbols='r radius (m); T period (s); f frequency (Hz = rev/s); ω angular speed (rad/s).'),
        ],
        figure=dict(svg=FIG_DELTAV,
                    caption=r'Velocities at two nearby points have equal length but different directions. Their difference \(\Delta\vec v\) points toward the centre, giving \(a = v^2/r\) inward.'),
        traps=[r'Average acceleration over a finite arc is not \(v^2/r\). Over a quarter turn it is \(v\sqrt2/(T/4)\), which works out to \(2\sqrt2\,v^2/(\pi r) \approx 0.9\,v^2/r\).',
               r'Revolutions per minute must be converted: ω (rad/s) = 2π × rpm / 60. Forgetting the 2π is the commonest numerical slip.'],
        exam=r'''<ul><li>“A stone tied to a string of length … is whirled at … rev/s. Find its centripetal acceleration.”</li>
<li>“The change in velocity after half a revolution / a quarter revolution is …”</li>
<li>“Ratio of angular speeds of the hour and minute hands.”</li>
<li>Multi-select: which quantities remain constant in uniform circular motion.</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'A stone on a 0.5 m string is whirled in a horizontal circle at 2 revolutions per second. Find its speed and centripetal acceleration.',
                 steps=[r'ω = 2πf = 4π ≈ 12.6 rad/s.',
                        r'v = ωr = 4π × 0.5 = 2π ≈ 6.28 m/s.',
                        r'\(a_c = \omega^2r = 16\pi^2 \times 0.5 = 8\pi^2 \approx 79\) m/s², about 8g, toward the centre.'],
                 answer=r'v ≈ 6.28 m/s, \(a_c = 8\pi^2 \approx 79\) m/s²'),
            dict(tag='Ratio', q=r'Particles A and B move in circles of radii r and 2r. Find \(a_A : a_B\) if (i) their periods are equal, (ii) their speeds are equal.',
                 steps=[r'(i) Same period means same ω. \(a = \omega^2r \propto r\), so \(a_A : a_B = 1 : 2\).',
                        r'(ii) Same speed: \(a = v^2/r \propto 1/r\), so \(a_A : a_B = 2 : 1\).',
                        r'Always fix which quantity is held constant before choosing \(v^2/r\) or \(\omega^2r\).'],
                 answer=r'(i) 1 : 2, (ii) 2 : 1'),
            dict(tag='Concept', q=r'A particle moves uniformly in a circle of radius r with speed v. Find the magnitude of its average acceleration over a quarter revolution.',
                 steps=[r'After a quarter turn the velocity has turned by 90°: \(|\Delta\vec v| = 2v\sin45^\circ = v\sqrt2\).',
                        r'Time for a quarter turn: \(\Delta t = (2\pi r/v)/4 = \pi r/2v\).',
                        r'Average acceleration \(= v\sqrt2 \times 2v/(\pi r) = 2\sqrt2\,v^2/(\pi r) \approx 0.90\,v^2/r\). It is slightly less than the instantaneous value.'],
                 answer=r'\(2\sqrt2\,v^2/(\pi r)\)'),
        ],
        practice=[
            dict(q=r'A particle moves uniformly in a circle at 10 m/s. The magnitude of the change in its velocity after half a revolution is',
                 options=['0', '10 m/s', r'\(10\sqrt2\) m/s', '20 m/s'], answer=3, type='numerical',
                 explanation=r'After half a turn the velocity is reversed: \(|\Delta\vec v| = |-\vec v - \vec v| = 2v = 20\) m/s. Zero is the change in <em>speed</em>; \(10\sqrt2\) belongs to a quarter turn.'),
            dict(q=r'The ratio of the angular speed of the minute hand of a clock to that of the hour hand is',
                 options=['1 : 12', '12 : 1', '60 : 1', '1 : 60'], answer=1, type='numerical',
                 explanation=r'The minute hand turns once in 1 h and the hour hand once in 12 h. ω = 2π/T, so the ratio is 12 : 1. 60 : 1 compares the second hand with the minute hand.'),
            dict(q=r'For a particle in uniform circular motion, which of these remain constant? (a) speed (b) velocity (c) kinetic energy (d) magnitude of acceleration',
                 options=['(a) and (c) only', '(a), (c) and (d)', '(a), (b) and (c)', '(b) and (d) only'], answer=1, type='multi',
                 explanation=r'Speed, KE and the size \(v^2/r\) of the acceleration stay fixed. The velocity vector turns continuously, so (b) changes. Leaving out (d) confuses the constant magnitude of acceleration with its changing direction.'),
            dict(q=r'A particle goes round a circle of radius 2 m once every π seconds. Its centripetal acceleration is',
                 options=[r'2 m/s²', r'4 m/s²', r'8 m/s²', r'\(8\pi^2\) m/s²'], answer=2, type='numerical',
                 explanation=r'ω = 2π/T = 2 rad/s, so \(a = \omega^2r = 4 \times 2 = 8\) m/s². \(8\pi^2\) appears if T is taken as 1 s instead of π s.'),
        ],
    ),

    'plane-nonuniform': dict(
        level='exam',
        notes=[
            ('Direction of the total acceleration', r'''<p>The total acceleration makes angle β with the inward radius, where \(\tan\beta = a_t/a_r\).</p>
<ul><li>Speed increasing: the acceleration leans forward of the radius (toward the velocity).</li>
<li>Speed decreasing: it leans backward.</li>
<li>Uniform motion: β = 0, purely radial. A straight line (r → ∞): purely tangential.</li></ul>
<p>The angle between \(\vec a\) and \(\vec v\) is 90° − β when speeding up and 90° + β when slowing down.</p>'''),
            ('Speeding up from rest: radial part grows', r'''<p>With constant \(a_t\) from rest: \(v = a_t t\), so \(a_r = a_t^2t^2/r\) grows with time. In terms of the angle covered, \(v^2 = 2a_t(r\theta)\) gives</p>
\[a_r=2\theta\,a_t\]
<p>So the two parts are equal after half a radian, and after one full revolution (θ = 2π) the radial part is \(4\pi a_t\). The total acceleration changes direction continuously even though \(a_t\) is constant.</p>'''),
            ('Angular kinematics', r'''<p>For constant angular acceleration α the straight-line equations carry over with θ for s, ω for v and α for a:</p>
<ul><li>\(\omega = \omega_0 + \alpha t\)</li><li>\(\theta = \omega_0t + \tfrac12\alpha t^2\)</li><li>\(\omega^2 = \omega_0^2 + 2\alpha\theta\)</li></ul>
<p>Number of revolutions = θ/2π. The links to linear motion are \(v = r\omega\) and \(a_t = r\alpha\).</p>'''),
        ],
        formulas=[
            dict(title='Constant angular acceleration', formula=r'\omega=\omega_0+\alpha t,\quad \theta=\omega_0t+\tfrac12\alpha t^2,\quad \omega^2=\omega_0^2+2\alpha\theta',
                 symbols='ω₀, ω initial and final angular speed (rad/s); α angular acceleration (rad/s²), constant; θ angle turned (rad); t time (s).'),
            dict(title='Radial acceleration when starting from rest', formula=r'a_r=2\theta\,a_t',
                 symbols='aₜ constant tangential acceleration (m/s²); θ angle turned from rest (rad); aᵣ radial acceleration (m/s²) at that angle.'),
        ],
        figure=dict(svg=FIG_NONUNIFORM,
                    caption=r'When the speed changes, \(\vec a\) is the sum of a tangential part (changes the speed) and a radial part (turns the velocity). It no longer points at the centre.'),
        traps=[r'A body that starts from rest on a circle has zero radial acceleration at that instant, but it is not in “uniform” motion. Its acceleration is purely tangential at t = 0.',
               r'The tangential part changes the speed only; it does not turn the velocity. The radial part turns the velocity only; it does not change the speed.'],
        exam=r'''<ul><li>“A car moves on a circular track at … and its speed increases at … Find the net acceleration.”</li>
<li>“v = kt on a circle of radius r. Find the acceleration at time t.”</li>
<li>“A particle starts from rest with constant tangential acceleration. Ratio \(a_r/a_t\) after one revolution.” (4π)</li>
<li>Statement questions on which component changes speed and which changes direction.</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'A car moves on a circular track of radius 100 m. At one instant its speed is 20 m/s and is increasing at 3 m/s². Find its acceleration.',
                 steps=[r'\(a_r = v^2/r = 400/100 = 4\) m/s², toward the centre.',
                        r'\(a_t = 3\) m/s², along the velocity.',
                        r'\(a = \sqrt{16 + 9} = 5\) m/s².',
                        r'Direction: \(\tan\beta = 3/4\), so β = 37° from the radius, leaning forward.'],
                 answer=r'5 m/s² at 37° to the inward radius'),
            dict(tag='Ratio', q=r'A particle starts from rest on a circle and has constant tangential acceleration. Through what angle has it turned when its radial and tangential accelerations become equal? What is \(a_r/a_t\) after one revolution?',
                 steps=[r'\(v^2 = 2a_t s = 2a_t r\theta\), so \(a_r = v^2/r = 2\theta a_t\).',
                        r'\(a_r = a_t\) when 2θ = 1, that is θ = 0.5 rad (about 29°).',
                        r'After one revolution θ = 2π, so \(a_r/a_t = 4\pi \approx 12.6\).'],
                 answer=r'0.5 rad; 4π after one revolution'),
            dict(tag='Numerical', q=r'A wheel speeds up uniformly from rest to 20 rad/s in 4 s. Find its angular acceleration and the number of revolutions it makes.',
                 steps=[r'α = (20 − 0)/4 = 5 rad/s².',
                        r'θ = ½ × 5 × 4² = 40 rad.',
                        r'Revolutions = 40/2π ≈ 6.4.'],
                 answer=r'α = 5 rad/s², about 6.4 revolutions'),
        ],
        practice=[
            dict(q=r'A particle moves on a circle of radius 1 m with speed v = 2t (SI units). Its acceleration at t = 1 s has magnitude',
                 options=[r'2 m/s²', r'4 m/s²', r'6 m/s²', r'\(2\sqrt5\) m/s²'], answer=3, type='numerical',
                 explanation=r'\(a_t = dv/dt = 2\) m/s² and \(a_r = v^2/r = 4\) m/s² at t = 1 s. The total is \(\sqrt{4 + 16} = 2\sqrt5 \approx 4.5\) m/s². 6 m/s² adds perpendicular components as numbers; 2 or 4 keep only one part.'),
            dict(q=r'A particle starts from rest on a circular path with constant tangential acceleration. After one complete revolution, the ratio of its radial acceleration to its tangential acceleration is',
                 options=['1', '2π', '4π', 'π'], answer=2, type='numerical',
                 explanation=r'\(a_r = 2\theta a_t\) with θ = 2π, so the ratio is 4π. Using \(v^2 = a_t s\) instead of \(2a_t s\) gives 2π.'),
            dict(q=r'In non-uniform circular motion, the tangential and radial accelerations are equal in magnitude at some instant. The angle between the total acceleration and the velocity at that instant can be',
                 options=['0°', '45°', '90°', '180°'], answer=1, type='numerical',
                 explanation=r'The total acceleration is at 45° to both the radius and the tangent when \(a_t = a_r\). If the speed is rising this is 45° to \(\vec v\) (135° if falling). 90° would need \(a_t = 0\), and 0° or 180° would need \(a_r = 0\).'),
            dict(q=r'Statement I: In non-uniform circular motion, the net acceleration does not point toward the centre.<br>Statement II: The tangential component of acceleration changes the direction of the velocity.',
                 options=ST_OPTS, answer=1, type='statement',
                 explanation=r'With a nonzero tangential part, the net acceleration leans away from the radius, so Statement I is true. The tangential part changes only the speed; the radial part turns the velocity. Statement II is false.'),
        ],
    ),
}


NEW_SECTIONS = [
    dict(chapter='plane', after='plane-projectiles', id='plane-trajectory',
         title='Equation of trajectory and complementary angles',
         intro=r'Eliminate time between \(x = u\cos\theta\,t\) and \(y = u\sin\theta\,t - \tfrac12gt^2\). The result \(y = x\tan\theta - \dfrac{gx^2}{2u^2\cos^2\theta}\) has the form \(y = bx - cx^2\): the path is a parabola.',
         reasoning=r'Using \(R = 2u^2\sin\theta\cos\theta/g\), the same equation becomes \(y = x\tan\theta\,(1 - x/R)\), which shows the roots x = 0 and x = R at once. Because \(\sin2\theta = \sin(180^\circ - 2\theta)\), launch angles θ and 90° − θ at the same speed give the same range.',
         formula=r'y=x\tan\theta-\frac{gx^2}{2u^2\cos^2\theta}=x\tan\theta\left(1-\frac{x}{R}\right)',
         symbols='x horizontal and y vertical (upward) displacement from the launch point (m); θ launch angle; u launch speed (m/s); g gravity (m/s²); R level-ground range (m). Constant g, no drag.',
         trap=r'Complementary angles give the same range only. Heights and flight times differ: the steeper launch goes higher and stays up longer.',
         example=r'A projectile follows \(y = \sqrt3x - x^2/20\) (SI units, g = 10 m/s²). Find the launch angle, launch speed and range.',
         solution=r'Comparing with the standard form, tan θ = √3, so θ = 60°. Then \(g/(2u^2\cos^2\theta) = 1/20\) gives \(10/(2u^2 \times \tfrac14) = 1/20\), so u² = 400 and u = 20 m/s. Setting y = 0: \(x = 20\sqrt3 \approx 34.6\) m, which matches \(u^2\sin120^\circ/g\).',
         question=r'Two projectiles are launched at the same speed at 20° and 70° to the horizontal. They have equal',
         options=r'ranges|maximum heights|times of flight|speeds at the highest point', answer=0,
         explanation=r'20° and 70° are complementary, and \(\sin40^\circ = \sin140^\circ\), so the ranges match. The 70° projectile rises higher and stays up longer, while its speed at the top \(u\cos70^\circ\) is smaller.',
         deep=dict(
             level='core',
             notes=[
                 ('Derivation of the trajectory', r'''<ol><li>From the horizontal motion, \(t = x/(u\cos\theta)\).</li>
<li>Substitute into \(y = u\sin\theta\,t - \tfrac12gt^2\): \(y = x\tan\theta - \dfrac{g x^2}{2u^2\cos^2\theta}\).</li>
<li>Factor out \(x\tan\theta\): \(y = x\tan\theta\left(1 - \dfrac{gx}{2u^2\sin\theta\cos\theta}\right) = x\tan\theta\left(1 - \dfrac{x}{R}\right)\).</li></ol>
<p>Reading a given path \(y = bx - cx^2\): \(\tan\theta = b\), range \(R = b/c\), and maximum height \(H = b^2/4c\) (at x = R/2).</p>'''),
                 ('Complementary angles: what matches and what does not', r'''<p>For launch angles θ and 90° − θ at the same speed u:</p>
<ul><li>Ranges are equal.</li>
<li>Heights: \(H_1 = u^2\sin^2\theta/2g\), \(H_2 = u^2\cos^2\theta/2g\). So \(H_1 + H_2 = u^2/2g\) and \(H_1H_2 = R^2/16\), giving \(R = 4\sqrt{H_1H_2}\).</li>
<li>Times: \(T_1T_2 = \dfrac{4u^2\sin\theta\cos\theta}{g^2} = \dfrac{2R}{g}\).</li>
<li>At 45° the two angles coincide and the range is the maximum, \(u^2/g\).</li></ul>'''),
                 ('Clearing a wall', r'''<p>To check whether a ball clears a wall at horizontal distance d, put x = d into the trajectory and compare y with the wall’s height. This avoids finding the time separately. The form \(y = x\tan\theta(1 - x/R)\) is the quickest when R is already known.</p>'''),
             ],
             formulas=[
                 dict(title='Complementary-angle results', formula=r'H_1+H_2=\frac{u^2}{2g},\qquad R=4\sqrt{H_1H_2},\qquad T_1T_2=\frac{2R}{g}',
                      symbols='Subscripts 1 and 2 refer to launch angles θ and 90° − θ at the same speed u (m/s); H heights (m), T flight times (s), R the common range (m).'),
                 dict(title='Reading y = bx − cx²', formula=r'\tan\theta=b,\qquad R=\frac{b}{c},\qquad H=\frac{b^2}{4c}',
                      symbols='b is dimensionless; c has unit 1/m; R and H in metres. Level ground, upward y.'),
             ],
             figure=dict(svg=FIG_COMPLEMENT,
                         caption=r'At the same speed, 30° and 60° launches land at the same point. The 60° path is higher and slower to land. The dashed 45° path has the largest range.'),
             traps=[r'In \(y = x\tan\theta - gx^2/(2u^2\cos^2\theta)\) the denominator has \(\cos^2\theta\), not \(\cos\theta\). Missing the square gives the wrong speed.',
                    r'“Same range” does not fix the angle. Except at 45°, there are always two angles that give a range below the maximum.'],
             exam=r'''<ul><li>“The trajectory is y = ax − bx². Find the range / maximum height / launch angle.”</li>
<li>“Two projectiles with the same speed have the same range. Their heights are H₁ and H₂. Find R.” (\(4\sqrt{H_1H_2}\))</li>
<li>“Ratio of heights / times for 30° and 60° launches.”</li>
<li>“Will the ball clear a wall of height … at distance …?”</li></ul>''',
             examples=[
                 dict(tag='Ratio', q=r'Two balls are launched at 20 m/s, one at 30° and one at 60°. Find their common range, their heights and their flight times, and check \(T_1T_2 = 2R/g\).',
                      steps=[r'\(R = 400\sin60^\circ/10 = 20\sqrt3 \approx 34.6\) m for both.',
                             r'\(H_{30} = 400 \times \tfrac14/20 = 5\) m and \(H_{60} = 400 \times \tfrac34/20 = 15\) m. Sum = 20 m = u²/2g.',
                             r'\(T_{30} = 2(10)/10 = 2\) s and \(T_{60} = 2(10\sqrt3)/10 = 2\sqrt3 \approx 3.46\) s.',
                             r'\(T_1T_2 = 4\sqrt3 \approx 6.93\) s² and \(2R/g = 2(20\sqrt3)/10 = 4\sqrt3\). They agree.'],
                      answer=r'R ≈ 34.6 m; H = 5 m and 15 m; T = 2 s and 3.46 s'),
                 dict(tag='Numerical', q=r'A ball is launched at 20 m/s at 45°. A wall 10 m away is 7 m high. Does the ball clear it? (g = 10 m/s²)',
                      steps=[r'Range \(R = 400/10 = 40\) m.',
                             r'At x = 10 m: \(y = 10\tan45^\circ(1 - 10/40) = 10 \times 0.75 = 7.5\) m.',
                             r'7.5 m &gt; 7 m, so the ball clears the wall by 0.5 m.'],
                      answer=r'Yes; it is 7.5 m high at the wall'),
                 dict(tag='Assertion–Reason', q=r'Assertion (A): Projectiles launched at the same speed at θ and (90° − θ) have equal ranges.<br>Reason (R): \(\sin2\theta = \sin(180^\circ - 2\theta)\).',
                      steps=[r'For 90° − θ, the range uses \(\sin(180^\circ - 2\theta)\).',
                             r'This equals \(\sin2\theta\), so the two ranges are equal.',
                             r'A is true and R is the exact reason.'],
                      answer=r'Both true; R correctly explains A'),
             ],
             practice=[
                 dict(q=r'A projectile follows \(y = x - x^2/40\) (SI units, g = 10 m/s²). Its launch speed is',
                      options=['10 m/s', '20 m/s', r'\(20\sqrt2\) m/s', '40 m/s'], answer=1, type='numerical',
                      explanation=r'tan θ = 1, so θ = 45° and cos²θ = 1/2. Then \(g/(2u^2\cos^2\theta) = 10/u^2 = 1/40\), so u = 20 m/s. Check: R = b/c = 40 m = u²/g. \(20\sqrt2\) comes from dropping the cos²θ.'),
                 dict(q=r'Two projectiles launched at the same speed have the same range. Their maximum heights are 5 m and 20 m. The range is',
                      options=['25 m', '50 m', '40 m', '100 m'], answer=2, type='numerical',
                      explanation=r'Equal ranges at equal speed means complementary angles, so \(R = 4\sqrt{H_1H_2} = 4\sqrt{100} = 40\) m. 25 m adds the heights, and 100 m is \(H_1H_2\) without the square root and factor.'),
                 dict(q=r'Statement I: The path of a projectile is a parabola when air resistance is neglected and g is constant.<br>Statement II: An object thrown horizontally from a height also follows a parabolic path under the same conditions.',
                      options=ST_OPTS, answer=0, type='statement',
                      explanation=r'Both are true. Uniform horizontal motion plus uniformly accelerated vertical motion always gives a parabola. A horizontal launch is the special case θ = 0, giving \(y = -gx^2/2u^2\).'),
                 dict(q=r'A projectile on level ground follows \(y = ax - bx^2\), where a and b are positive constants. Its range is',
                      options=[r'\(a^2/4b\)', r'\(b/a\)', r'\(2a/b\)', r'\(a/b\)'], answer=3, type='concept',
                      explanation=r'y = 0 at x = 0 and x = a/b, so R = a/b. \(a^2/4b\) is the maximum height, reached at x = a/2b.'),
             ],
         )),

    dict(chapter='plane', after='plane-horizontal', id='plane-incline',
         title='Projectile on an inclined plane',
         intro=r'When a projectile is launched from an incline of angle α, take the x′-axis along the incline and the y′-axis perpendicular to it. Gravity then has two components: \(g\sin\alpha\) along the slope (downhill) and \(g\cos\alpha\) into the slope. Measure the launch angle θ from the incline.',
         reasoning=r'Perpendicular to the incline the motion is like a vertical throw under “gravity” \(g\cos\alpha\). The time of flight is when y′ returns to zero. Along the incline the motion is uniformly decelerated (going up) or accelerated (going down) by \(g\sin\alpha\), which gives the range along the slope.',
         formula=r'T=\frac{2u\sin\theta}{g\cos\alpha},\qquad R_{\rm up}=\frac{2u^2\sin\theta\cos(\theta+\alpha)}{g\cos^2\alpha}',
         symbols='u launch speed (m/s); θ angle between the launch velocity and the incline; α incline angle with the horizontal; g gravity (m/s²); T time of flight (s); R_up distance along the incline (m) when thrown up the slope. For a throw down the slope replace θ + α by θ − α. No drag.',
         trap=r'θ is measured from the incline, not from the horizontal. If the angle is given with the horizontal (say φ), use θ = φ − α for a throw up the slope.',
         example=r'A ball is thrown at 20 m/s up a 30° incline, making 30° with the incline (60° with the horizontal). Find the time of flight and the distance along the incline at which it lands (g = 10 m/s²).',
         solution=r'\(T = 2(20)\sin30^\circ/(10\cos30^\circ) = 20/8.66 \approx 2.31\) s. \(R = 2(400)\sin30^\circ\cos60^\circ/(10 \times 0.75) = 200/7.5 \approx 26.7\) m. Check: horizontal distance \(= 20\cos60^\circ \times 2.31 = 23.1\) m, and \(23.1/\cos30^\circ = 26.7\) m.',
         question=r'A particle is projected with speed u at angle θ to an inclined plane of inclination α. Its time of flight is',
         options=r'\(2u\sin\theta/g\)|\(2u\sin\theta/(g\cos\alpha)\)|\(2u\cos\theta/(g\sin\alpha)\)|\(2u\sin(\theta+\alpha)/g\)', answer=1,
         explanation=r'Perpendicular to the incline, the initial velocity is \(u\sin\theta\) and the deceleration is \(g\cos\alpha\). It returns to the incline after \(2u\sin\theta/(g\cos\alpha)\). The level-ground formula \(2u\sin\theta/g\) ignores the tilt of the axes.',
         deep=dict(
             level='exam',
             notes=[
                 ('Setting up the axes', r'''<ol><li>x′ along the incline (up the slope positive), y′ perpendicular to it.</li>
<li>Initial velocity: \(u\cos\theta\) along x′, \(u\sin\theta\) along y′.</li>
<li>Acceleration: \(-g\sin\alpha\) along x′ (when thrown up the slope), \(-g\cos\alpha\) along y′.</li>
<li>Landing: y′ = 0, so \(u\sin\theta\,T - \tfrac12g\cos\alpha\,T^2 = 0\), giving \(T = 2u\sin\theta/(g\cos\alpha)\). The same T holds for a throw down the slope.</li>
<li>Range: \(R = u\cos\theta\,T - \tfrac12g\sin\alpha\,T^2\), which simplifies to \(2u^2\sin\theta\cos(\theta+\alpha)/(g\cos^2\alpha)\). Down the slope, \(+\tfrac12g\sin\alpha T^2\) gives \(\cos(\theta-\alpha)\).</li></ol>
<p>Setting α = 0 recovers the level-ground results. That is a good check on any incline formula.</p>'''),
                 ('Maximum range and special landings', r'''<ul><li>Up the incline: \(R_{\max} = \dfrac{u^2}{g(1+\sin\alpha)}\) at \(\theta = 45^\circ - \alpha/2\) from the incline.</li>
<li>Down the incline: \(R_{\max} = \dfrac{u^2}{g(1-\sin\alpha)}\) at \(\theta = 45^\circ + \alpha/2\).</li>
<li>The best direction bisects the angle between the incline and the vertical.</li>
<li><strong>Strikes the incline perpendicularly</strong> (thrown up the slope): the velocity along the incline must be zero at landing, \(u\cos\theta = g\sin\alpha\,T\). This gives \(\cot\theta = 2\tan\alpha\).</li></ul>'''),
                 ('The most common form: horizontal throw from the top of an incline', r'''<p>A ball is thrown horizontally at u from the top of an incline of angle α. It lands when the drop equals the horizontal distance times tan α:</p>
<ol><li>\(\tfrac12gt^2 = ut\tan\alpha\), so \(t = 2u\tan\alpha/g\).</li>
<li>Horizontal distance \(x = ut = 2u^2\tan\alpha/g\).</li>
<li>Distance along the incline \(L = x/\cos\alpha = 2u^2\tan\alpha/(g\cos\alpha)\).</li></ol>
<p>Here θ = α measured from the incline, and the general formula gives the same answer.</p>'''),
             ],
             formulas=[
                 dict(title='Maximum range on an incline', formula=r'R_{\max,\rm up}=\frac{u^2}{g(1+\sin\alpha)},\qquad R_{\max,\rm down}=\frac{u^2}{g(1-\sin\alpha)}',
                      symbols='u launch speed (m/s); α incline angle; R measured along the incline (m). Best launch at 45° ∓ α/2 from the incline.'),
                 dict(title='Horizontal throw from the top of an incline', formula=r't=\frac{2u\tan\alpha}{g},\qquad L=\frac{2u^2\tan\alpha}{g\cos\alpha}',
                      symbols='u horizontal launch speed (m/s); α incline angle; t time to land (s); L distance down the incline (m).'),
                 dict(title='Hitting the incline at right angles', formula=r'\cot\theta=2\tan\alpha',
                      symbols='θ launch angle measured from the incline, thrown up the slope; α incline angle.'),
             ],
             figure=dict(svg=FIG_INCLINE,
                         caption=r'Tilted axes: x′ along the incline, y′ perpendicular. Gravity splits into \(g\sin\alpha\) down the slope and \(g\cos\alpha\) into it. The launch angle θ is measured from the incline.'),
             traps=[r'The range on an incline is measured along the slope. If you find the horizontal distance x, divide by cos α to get the distance along the incline.',
                    r'Maximum range on an incline is not at 45° to the incline. It is at 45° − α/2 (up) or 45° + α/2 (down) from the incline.'],
             exam=r'''<ul><li>“A ball is thrown horizontally from the top of an incline of 37°/45° … Find where / when it lands.”</li>
<li>“Time of flight of a particle projected at θ to an incline of angle α.”</li>
<li>“Ratio of maximum ranges up and down an incline.”</li>
<li>“Condition for the particle to hit the incline perpendicularly.”</li></ul>''',
             examples=[
                 dict(tag='Numerical', q=r'A ball is thrown horizontally at 10 m/s from the top of a 45° incline. Find when it lands and how far down the incline (g = 10 m/s²).',
                      steps=[r'Landing condition: \(\tfrac12gt^2 = ut\tan45^\circ\), so \(t = 2u/g = 2\) s.',
                             r'Horizontal distance = 10 × 2 = 20 m; vertical drop = ½ × 10 × 4 = 20 m.',
                             r'Distance along the incline \(= \sqrt{20^2 + 20^2} = 20\sqrt2 \approx 28.3\) m.'],
                      answer=r'After 2 s, \(20\sqrt2 \approx 28.3\) m down the incline'),
                 dict(tag='Ratio', q=r'For a launch speed u on a 37° incline (sin 37° = 0.6), find the ratio of the maximum range up the incline to the maximum range down it.',
                      steps=[r'\(R_{\rm up} = u^2/[g(1 + 0.6)] = u^2/1.6g\).',
                             r'\(R_{\rm down} = u^2/[g(1 - 0.6)] = u^2/0.4g\).',
                             r'Ratio = 0.4/1.6 = 1 : 4. Throwing downhill gains a lot because gravity helps along the slope.'],
                      answer=r'1 : 4'),
                 dict(tag='Concept', q=r'A particle is thrown up a 45° incline. At what angle to the incline must it be launched so that it strikes the incline at right angles?',
                      steps=[r'Striking perpendicularly means the velocity along the incline is zero on impact: \(u\cos\theta - g\sin\alpha\,T = 0\).',
                             r'Substitute \(T = 2u\sin\theta/(g\cos\alpha)\): \(u\cos\theta = 2u\sin\theta\tan\alpha\), so \(\cot\theta = 2\tan\alpha\).',
                             r'With α = 45°: cot θ = 2, so \(\theta = \tan^{-1}(1/2) \approx 26.6^\circ\) to the incline.'],
                      answer=r'\(\tan^{-1}(1/2) \approx 26.6^\circ\) to the incline'),
             ],
             practice=[
                 dict(q=r'A ball is thrown horizontally at 20 m/s from the top of an incline of 37° (tan 37° = 3/4). The distance along the incline at which it lands is (g = 10 m/s²)',
                      options=['45 m', '60 m', '75 m', '100 m'], answer=2, type='numerical',
                      explanation=r'\(t = 2u\tan\alpha/g = 2(20)(0.75)/10 = 3\) s. Horizontal distance = 60 m and drop = 45 m, so the distance along the incline is \(\sqrt{60^2 + 45^2} = 75\) m. 60 m and 45 m are only the horizontal and vertical parts.'),
                 dict(q=r'For a given launch speed, the ratio of the maximum range up a 30° incline to the maximum range down it is',
                      options=['1 : 3', '1 : 2', '3 : 1', r'\(1 : \sqrt3\)'], answer=0, type='numerical',
                      explanation=r'\(R_{\rm up} : R_{\rm down} = (1 - \sin30^\circ) : (1 + \sin30^\circ) = 0.5 : 1.5 = 1 : 3\). 3 : 1 inverts it: the downhill range is the larger one.'),
                 dict(q=r'A particle is projected with speed 10 m/s at 30° to an incline of 30°. Its time of flight is (g = 10 m/s²)',
                      options=['1 s', r'\(2/\sqrt3\) s', r'\(\sqrt3\) s', '2 s'], answer=1, type='numerical',
                      explanation=r'\(T = 2u\sin\theta/(g\cos\alpha) = 2(10)(0.5)/(10 \times \sqrt3/2) = 2/\sqrt3 \approx 1.15\) s. 1 s is the level-ground value that ignores the cos α.'),
                 dict(q=r'Statement I: For the same speed and the same angle θ measured from the incline, the time of flight is the same whether the particle is thrown up or down the incline.<br>Statement II: Maximum range up an incline is obtained at 45° to the incline.',
                      options=ST_OPTS, answer=1, type='statement',
                      explanation=r'T depends only on motion perpendicular to the incline (\(u\sin\theta\) and \(g\cos\alpha\)), which is the same both ways, so Statement I is true. The maximum range up the slope needs θ = 45° − α/2, so Statement II is false.'),
             ],
         )),
]
