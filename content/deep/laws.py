"""Deepening layer for Laws of Motion Part 1. Schema: docs/deepening-schema.md."""
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


def _rect(x, y, w, h, fill='var(--water-soft)', stroke='var(--water)', rx=3):
    return f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" rx="{rx}" style="fill:{fill};stroke:{stroke};stroke-width:1.5"/>'


def _circle(cx, cy, r, fill='var(--surface)', stroke='var(--ink-2)', w=1.5):
    return f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{_f(r)}" style="fill:{fill};stroke:{stroke};stroke-width:{w}"/>'


def _poly(pts, fill='var(--surface-2)', stroke='var(--ink-2)'):
    return '<polygon points="' + ' '.join(f'{_f(x)},{_f(y)}' for x, y in pts) + f'" style="fill:{fill};stroke:{stroke};stroke-width:1.2"/>'


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


def _svg(w, h, label, *parts):
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}" style="max-width:{int(w * 1.35)}px;margin:0 auto">'
            + ''.join(parts) + '</svg>')


IT = ';font-style:italic;font-weight:600'

# ---------- figures ----------
FIG_PAIRS = _svg(
    420, 235, 'Book on a table: weight and normal force act on the book; their third-law partners act on Earth and on the table',
    _rect(40, 120, 150, 14, 'var(--surface-2)', 'var(--ink-2)', 2), _line(60, 134, 60, 205), _line(170, 134, 170, 205),
    _rect(85, 92, 60, 28, 'var(--amber-soft)', 'var(--amber)'), _text(115, 111, 'book', 'var(--ink)', 11, 'middle'),
    _arrow(115, 106, 115, 50, 'var(--teal)', 2.6), _text(122, 58, _lab('N', 'table on book')),
    _arrow(108, 106, 108, 168, 'var(--coral)', 2.6), _text(100, 170, _lab('W', 'Earth on book'), 'var(--coral)', 12, 'end'),
    f'<path d="M20 225 Q210 195 400 225" style="fill:var(--green-soft);stroke:var(--green);stroke-width:1.5"/>',
    _text(390, 228, 'Earth', 'var(--green)', 11, 'end'),
    _arrow(250, 215, 250, 160, 'var(--coral)', 2.2, 8, True), _text(258, 176, 'book pulls Earth up', 'var(--coral)', 11),
    _text(258, 190, '(partner of W)', 'var(--coral)', 11),
    _arrow(150, 122, 150, 150, 'var(--teal)', 2.2, 8, True), _text(200, 150, 'book presses table down', 'var(--teal)', 11),
    _text(200, 164, '(partner of N)', 'var(--teal)', 11),
    _text(410, 40, 'On the book: N and W only.', 'var(--ink)', 12, 'end'),
    _text(410, 56, 'They balance, but they are', 'var(--ink-2)', 11, 'end'),
    _text(410, 70, 'not an action–reaction pair.', 'var(--ink-2)', 11, 'end'),
)

_ia = 30
_x0, _y0, _len = 30, 210, 360
_top = (_x0 + _len, _y0 - _len * math.tan(math.radians(_ia)))
_bc = (_x0 + 220 * math.cos(math.radians(_ia)) * 1.0, 0)
_s = 220
_cx, _cy = _x0 + _s * math.cos(math.radians(_ia)), _y0 - _s * math.sin(math.radians(_ia))
_nx, _ny = -math.sin(math.radians(_ia)), -math.cos(math.radians(_ia))  # outward normal (svg coords)
_ux, _uy = math.cos(math.radians(_ia)), -math.sin(math.radians(_ia))   # up-slope unit (svg coords)
_bw, _bh = 50, 32
_corner = lambda a, b: (_cx + a * _ux + b * _nx, _cy + a * _uy + b * _ny)
_blk = [_corner(-_bw / 2, 0), _corner(_bw / 2, 0), _corner(_bw / 2, _bh), _corner(-_bw / 2, _bh)]
_G = _corner(0, _bh / 2)
_mg = 70
FIG_INCLINE = _svg(
    420, 225, 'Free-body diagram of a block on a smooth incline: weight mg straight down, its components mg sin theta down the slope and mg cos theta into the slope, and the normal force',
    _poly([(_x0, _y0), (_x0 + _len, _y0), (_x0 + _len, _y0 - _len * math.tan(math.radians(_ia)))]),
    _poly(_blk, 'var(--amber-soft)', 'var(--amber)'),
    _arrow(*_G, _G[0], _G[1] + _mg, 'var(--coral)', 2.8),
    _arrow(*_G, _G[0] - _mg * math.sin(math.radians(_ia)) * _ux, _G[1] - _mg * math.sin(math.radians(_ia)) * _uy, 'var(--coral)', 1.8, 8, True),
    _arrow(*_G, _G[0] - _mg * math.cos(math.radians(_ia)) * _nx, _G[1] - _mg * math.cos(math.radians(_ia)) * _ny, 'var(--coral)', 1.8, 8, True),
    _arrow(*_G, _G[0] + 66 * _nx, _G[1] + 66 * _ny, 'var(--teal)', 2.8),
    _text(_G[0] + 4, _G[1] + _mg + 12, 'mg', 'var(--coral)', 13, extra=IT),
    _text(_G[0] - 58, _G[1] + 30, 'mg sin θ', 'var(--coral)', 11, 'end'),
    _text(_G[0] + 34, _G[1] + 58, 'mg cos θ', 'var(--coral)', 11),
    _text(_G[0] + 66 * _nx - 4, _G[1] + 66 * _ny - 4, 'N', 'var(--teal)', 13, 'end', IT),
    _arc(_x0, _y0, 46, 0, _ia), _text(_x0 + 52, _y0 - 8, 'θ', 'var(--ink-2)', 12),
    _text(410, 30, 'Along the slope: ma = mg sin θ', 'var(--ink)', 12, 'end'),
    _text(410, 46, 'Across the slope: N = mg cos θ', 'var(--ink)', 12, 'end'),
)

FIG_BALANCE = _svg(
    420, 215, 'A spring balance in the middle of a string that passes over two pulleys with a 5 kg mass hanging at each end',
    _circle(60, 50, 20), _circle(360, 50, 20), _circle(60, 50, 3, 'var(--ink-2)'), _circle(360, 50, 3, 'var(--ink-2)'),
    _line(60, 50, 60, 18, 'var(--ink-2)', 2), _line(360, 50, 360, 18, 'var(--ink-2)', 2),
    _line(60, 30, 160, 30, 'var(--ink-2)', 1.6), _line(260, 30, 360, 30, 'var(--ink-2)', 1.6),
    _rect(160, 18, 100, 24, 'var(--indigo-soft)', 'var(--indigo)'),
    f'<path d="M170 30 l6 -7 l8 14 l8 -14 l8 14 l8 -14 l8 14 l8 -14 l8 14 l8 -7" style="fill:none;stroke:var(--indigo);stroke-width:1.4"/>',
    _text(210, 60, 'spring balance reads T', 'var(--indigo)', 12, 'middle'),
    _line(40, 50, 40, 140, 'var(--ink-2)', 1.6), _line(380, 50, 380, 140, 'var(--ink-2)', 1.6),
    _rect(22, 140, 36, 36, 'var(--water-soft)', 'var(--water)'), _rect(362, 140, 36, 36, 'var(--water-soft)', 'var(--water)'),
    _text(40, 163, '5 kg', 'var(--ink)', 11, 'middle'), _text(380, 163, '5 kg', 'var(--ink)', 11, 'middle'),
    _arrow(150, 30, 110, 30, 'var(--coral)', 2.2), _arrow(270, 30, 310, 30, 'var(--coral)', 2.2),
    _text(130, 22, 'T', 'var(--coral)', 13, 'middle', IT), _text(290, 22, 'T', 'var(--coral)', 13, 'middle', IT),
    _text(210, 110, 'Each mass is in equilibrium, so T = 50 N.', 'var(--ink)', 12, 'middle'),
    _text(210, 128, 'The balance reads 50 N (5 kg-wt), not 100 N, not 0.', 'var(--ink-2)', 12, 'middle'),
    _text(210, 200, 'A balance always reads the tension on one side of its spring.', 'var(--ink-2)', 11, 'middle'),
)

FIG_TABLE_PULLEY = _svg(
    420, 235, 'Block of mass m1 on a smooth table tied by a string over a pulley at the edge to a hanging mass m2, with tension and weight arrows',
    _rect(20, 110, 290, 14, 'var(--surface-2)', 'var(--ink-2)', 1), _line(40, 124, 40, 225), _line(290, 124, 290, 225),
    _circle(318, 104, 14), _circle(318, 104, 2.5, 'var(--ink-2)'), _line(304, 117, 304, 112, 'var(--ink-2)', 1.5),
    _rect(90, 78, 70, 32, 'var(--amber-soft)', 'var(--amber)'), _text(125, 99, _lab('m', '1'), 'var(--ink)', 12, 'middle'),
    _line(160, 92, 318, 90, 'var(--ink-2)', 1.5), _line(332, 104, 332, 160, 'var(--ink-2)', 1.5),
    _rect(312, 160, 40, 40, 'var(--water-soft)', 'var(--water)'), _text(332, 184, _lab('m', '2'), 'var(--ink)', 12, 'middle'),
    _arrow(160, 92, 215, 91, 'var(--coral)', 2.4), _text(190, 84, 'T', 'var(--coral)', 13, 'middle', IT),
    _arrow(332, 160, 332, 128, 'var(--coral)', 2.4), _text(340, 146, 'T', 'var(--coral)', 13, extra=IT),
    _arrow(342, 200, 342, 232, 'var(--teal)', 2.4), _text(350, 226, _lab('m', '2', 'g'), 'var(--teal)', 12),
    _arrow(105, 72, 105, 40, 'var(--teal)', 1.8, 8, True), _arrow(145, 110, 145, 140, 'var(--teal)', 1.8, 8, True),
    _text(100, 44, 'N', 'var(--teal)', 12, 'end', IT), _text(151, 140, _lab('m', '1', 'g'), 'var(--teal)', 12),
    _text(20, 22, _lab('System: a = m', '2', 'g / (m', '1', ' + m', '2', ')'), 'var(--ink)', 12),
    _text(20, 40, _lab('Block alone: T = m', '1', 'a'), 'var(--ink)', 12),
    _arrow(200, 60, 250, 60, 'var(--plum)', 1.6, 7), _text(256, 64, 'a', 'var(--plum)', 12, extra=IT),
)

_gx0, _gy0, _sx, _sy = 50, 170, 32, 28
_vt = [(0, 0), (2, 4), (6, 4), (10, 0)]
FIG_LIFT_GRAPH = _svg(
    420, 225, 'Velocity-time graph of a lift moving up: speeding up for 2 s, steady until 6 s, slowing until 10 s, with the scale reading in each phase',
    _arrow(_gx0, _gy0, _gx0 + 11 * _sx, _gy0, 'var(--ink-2)', 1.3, 7), _arrow(_gx0, _gy0, _gx0, _gy0 - 5 * _sy, 'var(--ink-2)', 1.3, 7),
    _text(_gx0 + 11 * _sx, _gy0 + 18, 't (s)', 'var(--ink-2)', 11, 'end'), _text(_gx0 - 6, _gy0 - 5 * _sy + 6, 'v (m/s)', 'var(--ink-2)', 11, 'end'),
    '<polyline points="' + ' '.join(f'{_f(_gx0 + t * _sx)},{_f(_gy0 - v * _sy)}' for t, v in _vt) + '" style="fill:none;stroke:var(--indigo);stroke-width:2.6"/>',
    *[_text(_gx0 + t * _sx, _gy0 + 16, str(t), 'var(--ink-2)', 11, 'middle') for t in (0, 2, 6, 10)],
    _text(_gx0 - 6, _gy0 - 4 * _sy + 4, '4', 'var(--ink-2)', 11, 'end'),
    _line(_gx0, _gy0 - 4 * _sy, _gx0 + 2 * _sx, _gy0 - 4 * _sy, 'var(--ink-2)', 1, True),
    _text(_gx0 + 1 * _sx, _gy0 - 4.6 * _sy, 'a = +2', 'var(--coral)', 11, 'middle'),
    _text(_gx0 + 4 * _sx, _gy0 - 4.6 * _sy, 'a = 0', 'var(--ink-2)', 11, 'middle'),
    _text(_gx0 + 8 * _sx, _gy0 - 4.6 * _sy, 'a = −1', 'var(--teal)', 11, 'middle'),
    _text(_gx0 + 1 * _sx, 205, 'N = m(g + 2)', 'var(--coral)', 11, 'middle'),
    _text(_gx0 + 4 * _sx, 205, 'N = mg', 'var(--ink-2)', 11, 'middle'),
    _text(_gx0 + 8 * _sx, 205, 'N = m(g − 1)', 'var(--teal)', 11, 'middle'),
    _text(_gx0 + 4 * _sx, 221, 'scale reading in each phase (up positive)', 'var(--ink-2)', 11, 'middle'),
)

_wa = 37
_wx0, _wy0, _wb = 90, 200, 230
_wh = _wb * math.tan(math.radians(_wa))
_wedge = [(_wx0, _wy0), (_wx0 + _wb, _wy0), (_wx0 + _wb, _wy0 - _wh)]
_d = 120
_ux2, _uy2 = math.cos(math.radians(_wa)), -math.sin(math.radians(_wa))
_nx2, _ny2 = -math.sin(math.radians(_wa)), -math.cos(math.radians(_wa))
_bc2 = (_wx0 + _d * _ux2, _wy0 + _d * _uy2)
_b2 = lambda a, b: (_bc2[0] + a * _ux2 + b * _nx2, _bc2[1] + a * _uy2 + b * _ny2)
_blk2 = [_b2(-20, 0), _b2(20, 0), _b2(20, 26), _b2(-20, 26)]
_G2 = _b2(0, 13)
FIG_WEDGE = _svg(
    420, 230, 'Block on a smooth wedge that accelerates to the left; in the wedge frame the block feels weight, normal force and a pseudo force to the right',
    _line(20, _wy0, 410, _wy0, 'var(--ink-2)', 1.5),
    _poly(_wedge), _poly(_blk2, 'var(--amber-soft)', 'var(--amber)'),
    _arrow(*_G2, _G2[0], _G2[1] + 62, 'var(--coral)', 2.6), _text(_G2[0] - 6, _G2[1] + 66, 'mg', 'var(--coral)', 13, 'end', IT),
    _arrow(*_G2, _G2[0] + 70 * _nx2, _G2[1] + 70 * _ny2, 'var(--teal)', 2.6), _text(_G2[0] + 70 * _nx2 - 4, _G2[1] + 70 * _ny2, 'N', 'var(--teal)', 13, 'end', IT),
    _arrow(*_G2, _G2[0] + 58, _G2[1], 'var(--plum)', 2.6, 9, True), _text(_G2[0] + 62, _G2[1] - 6, _lab('m a', '0', ' (pseudo)'), 'var(--plum)', 12),
    _arrow(330, 120, 270, 120, 'var(--indigo)', 2.6), _text(300, 112, _lab('wedge acceleration a', '0'), 'var(--indigo)', 12, 'middle'),
    _arc(_wx0, _wy0, 40, 0, _wa), _text(_wx0 + 46, _wy0 - 8, 'θ', 'var(--ink-2)', 12),
    _text(20, 22, _lab('Block at rest on the wedge when a', '0', ' = g tan θ'), 'var(--ink)', 12),
    _text(20, 38, 'Then N = mg / cos θ', 'var(--ink)', 12),
)

_fx0, _fy0, _fsx, _fsy = 60, 180, 9000, 0.34
FIG_FT = _svg(
    420, 220, 'Force-time graph of an impact: force rises linearly to 400 N at 0.01 s and falls to zero at 0.03 s; the shaded area is the impulse',
    _poly([(_fx0, _fy0), (_fx0 + 0.01 * _fsx, _fy0 - 400 * _fsy), (_fx0 + 0.03 * _fsx, _fy0)], 'var(--indigo-soft)', 'var(--indigo)'),
    _arrow(_fx0, _fy0, _fx0 + 0.036 * _fsx, _fy0, 'var(--ink-2)', 1.3, 7), _arrow(_fx0, _fy0, _fx0, _fy0 - 470 * _fsy, 'var(--ink-2)', 1.3, 7),
    _text(_fx0 + 0.036 * _fsx, _fy0 + 18, 't (s)', 'var(--ink-2)', 11, 'end'), _text(_fx0 - 6, _fy0 - 450 * _fsy, 'F (N)', 'var(--ink-2)', 11, 'end'),
    _line(_fx0, _fy0 - 400 * _fsy, _fx0 + 0.01 * _fsx, _fy0 - 400 * _fsy, 'var(--ink-2)', 1, True),
    _text(_fx0 - 6, _fy0 - 400 * _fsy + 4, '400', 'var(--ink-2)', 11, 'end'),
    _text(_fx0, _fy0 + 16, '0', 'var(--ink-2)', 11, 'middle'),
    _text(_fx0 + 0.01 * _fsx, _fy0 + 16, '0.01', 'var(--ink-2)', 11, 'middle'),
    _text(_fx0 + 0.03 * _fsx, _fy0 + 16, '0.03', 'var(--ink-2)', 11, 'middle'),
    _text(_fx0 + 0.013 * _fsx, _fy0 - 40, 'area = impulse', 'var(--indigo)', 12, 'middle'),
    _text(_fx0 + 0.013 * _fsx, _fy0 - 24, '= ½ × 0.03 × 400 = 6 N s', 'var(--indigo)', 12, 'middle'),
    _text(410, 50, 'Average force over the contact:', 'var(--ink-2)', 11, 'end'),
    _text(410, 66, '6 N s ÷ 0.03 s = 200 N', 'var(--ink-2)', 11, 'end'),
    _text(_fx0 + 0.015 * _fsx, 210, 'Same impulse spread over a longer time means a smaller peak force.', 'var(--ink-2)', 11, 'middle'),
)

_ba = 20
_rx0, _ry0, _rl = 70, 175, 300
_rtop = (_rx0 + _rl, _ry0 - _rl * math.tan(math.radians(_ba)))
_cc = (_rx0 + 170, _ry0 - 170 * math.tan(math.radians(_ba)))
_ncx, _ncy = -math.sin(math.radians(_ba)), -math.cos(math.radians(_ba))
_car = [(_cc[0] + a * math.cos(math.radians(_ba)) + b * _ncx, _cc[1] - a * math.sin(math.radians(_ba)) + b * _ncy)
        for a, b in ((-28, 0), (28, 0), (28, 24), (-28, 24))]
_Gc = (_cc[0] + 12 * _ncx, _cc[1] + 12 * _ncy)
_Nl = 100
FIG_BANK = _svg(
    420, 225, 'Car on a road banked at angle theta, seen from behind: the normal force tilts toward the centre of the turn; its vertical part balances mg and its horizontal part supplies mv squared over r',
    _poly([(_rx0, _ry0), (_rtop[0], _ry0), _rtop]), _poly(_car, 'var(--amber-soft)', 'var(--amber)'),
    _arrow(*_Gc, _Gc[0] + _Nl * _ncx, _Gc[1] + _Nl * _ncy, 'var(--teal)', 2.8),
    _arrow(*_Gc, _Gc[0], _Gc[1] + _Nl * math.cos(math.radians(_ba)) * 0.85, 'var(--coral)', 2.6),
    _line(_Gc[0] + _Nl * _ncx, _Gc[1] + _Nl * _ncy, _Gc[0] + _Nl * _ncx, _Gc[1], 'var(--teal)', 1.1, True),
    _line(_Gc[0], _Gc[1] + _Nl * _ncy, _Gc[0] + _Nl * _ncx, _Gc[1] + _Nl * _ncy, 'var(--teal)', 1.1, True),
    _arrow(*_Gc, _Gc[0] + _Nl * _ncx, _Gc[1], 'var(--teal)', 1.8, 8),
    _arrow(*_Gc, _Gc[0], _Gc[1] + _Nl * _ncy, 'var(--teal)', 1.8, 8),
    _text(_Gc[0] + _Nl * _ncx - 4, _Gc[1] + _Nl * _ncy - 6, 'N', 'var(--teal)', 14, 'end', IT),
    _text(_Gc[0] + 6, _Gc[1] + _Nl * _ncy + 6, 'N cos θ', 'var(--teal)', 11),
    _text(_Gc[0] + _Nl * _ncx / 2, _Gc[1] + 16, 'N sin θ', 'var(--teal)', 11, 'middle'),
    _text(_Gc[0] + 6, _Gc[1] + 80, 'mg', 'var(--coral)', 13, extra=IT),
    _arrow(60, 60, 20, 60, 'var(--plum)', 2, 8), _text(64, 64, 'toward the centre of the turn', 'var(--plum)', 11),
    _arc(_rx0, _ry0, 50, 0, _ba), _text(_rx0 + 56, _ry0 - 6, 'θ', 'var(--ink-2)', 12),
    _text(410, 196, 'N cos θ = mg,  N sin θ = mv²/r', 'var(--ink)', 12, 'end'),
    _text(410, 213, '⇒ tan θ = v²/(rg)', 'var(--ink)', 12, 'end'),
)

AR_OPTS = ['Both A and R are true, and R correctly explains A',
           'Both A and R are true, but R does not explain A',
           'A is true but R is false',
           'A is false but R is true']
ST_OPTS = ['Both statements are true', 'Statement I is true, Statement II is false',
           'Statement I is false, Statement II is true', 'Both statements are false']


DEEP = {
    'laws-newton': dict(
        level='basic',
        notes=[
            ('Inertia in everyday situations', r'''<ul><li>A bus starts suddenly: your feet move with the floor but your upper body tends to stay at rest, so you lean backward.</li>
<li>A bus brakes: your upper body tends to keep moving, so you lurch forward.</li>
<li>Beating a carpet: the carpet moves, the dust tends to stay at rest and falls out.</li>
<li>A larger mass has more inertia: it needs more force for the same acceleration.</li></ul>
<p>Newton’s first law holds only in an <strong>inertial frame</strong>, one that is not accelerating. The ground is a good enough inertial frame for most NEET problems.</p>'''),
            ('Second law in momentum form', r'''<p>\(\vec F_{\rm net} = d\vec p/dt\) is the general law. For a body whose mass changes it gives</p>
\[\vec F = m\frac{d\vec v}{dt} + \vec v\frac{dm}{dt}\]
<ul><li>Sand falling on a moving belt at rate dm/dt: the extra force to keep the belt at constant speed v is \(v\,dm/dt\).</li>
<li>A machine gun firing n bullets per second, each of mass m at speed v: the average recoil force is \(nmv\).</li>
<li>If momentum is given as a function of time, differentiate it: the slope of a p–t graph is the force.</li></ul>'''),
            ('Spotting a third-law pair', r'''<p>A genuine action–reaction pair always:</p>
<ol><li>acts on two <em>different</em> bodies;</li><li>is of the same type (both gravitational, both contact, both tension);</li>
<li>is equal in size and opposite in direction, at every instant, whether the bodies accelerate or not.</li></ol>
<p>The weight of a book and the normal force on it act on the same body and are of different types, so they are not a pair. The horse–cart puzzle is resolved the same way: the cart’s pull on the horse acts on the horse. What moves the horse forward is the ground’s push on its hooves.</p>'''),
        ],
        formulas=[
            dict(title='Force from a mass flow', formula=r'F=v\frac{dm}{dt}',
                 symbols='F force needed (N); v speed given to or carried by the moving mass (m/s); dm/dt mass per second (kg/s). For a gun, F = nmv with n shots per second.'),
            dict(title='Average force from momentum change', formula=r'\vec F_{\rm av}=\frac{\Delta\vec p}{\Delta t}',
                 symbols='Δp change in momentum (kg m/s), a vector difference; Δt time interval (s).'),
        ],
        figure=dict(svg=FIG_PAIRS,
                    caption=r'Only N and W act on the book. Each has its own partner on another body: the book pulls the Earth up and presses the table down.'),
        traps=[r'Action and reaction never cancel each other, because they act on different bodies. Forces cancel only when they act on the same body.',
               r'A body moving at constant velocity has zero net force on it. “Moving, so there must be a forward force” is the classic misconception.'],
        exam=r'''<ul><li>“The reaction to the weight of a book on a table is …” (the book’s pull on Earth).</li>
<li>“A machine gun fires n bullets per second … force to hold the gun.”</li>
<li>“Sand drops on a conveyor belt at … kg/s. Extra power / force to keep it moving.”</li>
<li>“The momentum of a body is p = … Find the force at t = …” or “find F from the p–t graph”.</li>
<li>Assertion–reason on inertia examples (passenger in a bus, dusting a carpet).</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'Sand falls vertically onto a conveyor belt at 2 kg/s. The belt moves horizontally at a constant 3 m/s. What extra force must the motor apply to keep it at that speed?',
                 steps=[r'Each second, 2 kg of sand must be given a horizontal speed of 3 m/s.',
                        r'Rate of change of horizontal momentum \(= v\,dm/dt = 3 \times 2 = 6\) kg m/s per second.',
                        r'So the extra force is 6 N. (The motor’s extra power is Fv = 18 W.)'],
                 answer=r'6 N'),
            dict(tag='Graph', q=r'The momentum of a 2 kg body varies as \(p = 2t^2 + 3\) (SI units). Find the force on it at t = 2 s, and say what a straight-line p–t graph would mean.',
                 steps=[r'\(F = dp/dt = 4t\). At t = 2 s, F = 8 N.',
                        r'The constant 3 is the initial momentum; it does not affect the force.',
                        r'A straight p–t line has a constant slope, so the force would be constant. A horizontal line would mean zero force.'],
                 answer=r'8 N; a straight line means a constant force'),
            dict(tag='Concept', q=r'A horse pulls a cart. By the third law the cart pulls back on the horse equally. How can they move forward at all?',
                 steps=[r'The forward pull on the cart and the backward pull on the horse act on different bodies, so they cannot cancel.',
                        r'For the cart: the horse’s pull exceeds the friction on its wheels, so it accelerates.',
                        r'For the horse: the ground’s forward push on its hooves (the reaction to the horse pushing the ground back) exceeds the cart’s backward pull.',
                        r'For the horse + cart system the pulls are internal, and the net external force is ground push minus wheel friction.'],
                 answer=r'The pair acts on different bodies; the ground’s push on the horse drives the system'),
        ],
        practice=[
            dict(q=r'A machine gun fires 10 bullets per second, each of mass 20 g, at 500 m/s. The average force needed to hold the gun steady is',
                 options=['10 N', '50 N', '100 N', '1000 N'], answer=2, type='numerical',
                 explanation=r'Momentum given per second \(= nmv = 10 \times 0.02 \times 500 = 100\) N. 1000 N comes from using 20 g as 0.2 kg; 10 N forgets the number of bullets.'),
            dict(q=r'A book rests on a table. Which pair is an action–reaction pair?',
                 options=['Weight of the book and normal force of the table on the book', 'Normal force of the table on the book and the push of the book on the table', 'Weight of the book and the push of the book on the table', 'Normal force on the book and the pull of the book on Earth'], answer=1, type='concept',
                 explanation=r'The table pushes the book up and the book pushes the table down: same contact interaction, two bodies. Weight and normal force both act on the book and are of different types, so they only balance. The other mixtures combine forces from different interactions.'),
            dict(q=r'Assertion (A): A passenger standing in a bus falls forward when the bus brakes suddenly.<br>Reason (R): The upper body tends to continue moving forward because of its inertia of motion, while the feet are stopped with the bus.',
                 options=AR_OPTS, answer=0, type='ar',
                 explanation=r'Friction stops the feet with the bus, but nothing acts at once on the upper body, so it keeps moving forward. R is exactly the reason for A.'),
            dict(q=r'Statement I: A body moving in a circle at constant speed must have a net force acting on it.<br>Statement II: If the net force on a body is zero, its velocity cannot change.',
                 options=ST_OPTS, answer=0, type='statement',
                 explanation=r'In uniform circular motion the velocity direction changes, so there is an acceleration and hence a net (centripetal) force. Statement II is the first law. Both are true; “constant speed” is not the same as “constant velocity”.'),
        ],
    ),

    'laws-fbd': dict(
        level='basic',
        notes=[
            ('A recipe for every free-body diagram', r'''<ol><li>Choose one body (or one system) and draw it alone.</li>
<li>Draw the weight mg from its centre, straight down.</li>
<li>Go round the boundary. At each contact add a normal force (perpendicular to the surface) and, if needed, friction (along the surface). At each string add a tension pulling away from the body.</li>
<li>Add applied forces. Do not add “force of motion”, “centripetal force” or ma as extra forces.</li>
<li>Pick axes, ideally along the acceleration, and write \(\sum F = ma\) along each.</li></ol>'''),
            ('The normal force is whatever the contact needs', r'''<ul><li>Pull F at angle θ above the horizontal on a level floor: \(N = mg - F\sin\theta\).</li>
<li>Push F at angle θ below the horizontal: \(N = mg + F\sin\theta\).</li>
<li>Smooth incline: \(N = mg\cos\theta\). Smooth incline with a horizontal force holding the block at rest: \(F = mg\tan\theta\) and \(N = mg/\cos\theta\).</li>
<li>A block pressed against a wall by a horizontal force F: N = F, unrelated to mg.</li></ul>'''),
            ('Contact force between blocks', r'''<p>Two blocks \(m_1\) and \(m_2\) on a smooth floor, pushed by F applied to \(m_1\):</p>
<ol><li>System: \(a = F/(m_1+m_2)\).</li><li>Only the contact force accelerates \(m_2\): \(N = m_2a = \dfrac{m_2F}{m_1+m_2}\).</li></ol>
<p>Pushing from the other side changes the contact force to \(m_1F/(m_1+m_2)\). The contact force equals the force needed to accelerate everything <em>ahead</em> of the contact.</p>'''),
        ],
        formulas=[
            dict(title='Contact force between pushed blocks', formula=r'N_{12}=\frac{m_2F}{m_1+m_2}',
                 symbols='F horizontal push on m₁ (N); m₁ pushed block, m₂ the block ahead (kg); smooth floor. N₁₂ is the force between them (N).'),
            dict(title='Normal force with an inclined pull', formula=r'N=mg-F\sin\theta\ \ (\text{pull up}),\qquad N=mg+F\sin\theta\ \ (\text{push down})',
                 symbols='F applied force (N) at angle θ to the horizontal; m mass (kg); level floor, no vertical acceleration.'),
        ],
        figure=dict(svg=FIG_INCLINE,
                    caption=r'On a smooth incline only two forces act: mg and N. The dashed components of mg replace it in the equations; they are not extra forces.'),
        traps=[r'The contact force between two blocks depends on which side is pushed. Pushing the lighter block gives the larger contact force.',
               r'Pulling a box upward at an angle reduces the normal force below mg. Using N = mg here gives the wrong friction later in Part 2.'],
        exam=r'''<ul><li>“Two/three blocks in contact on a smooth floor are pushed by F. Find the force between …”</li>
<li>“A box is pulled by F at θ above the horizontal. Find the normal reaction / acceleration.”</li>
<li>“What horizontal force keeps a block at rest on a smooth incline?”</li>
<li>“How many forces act on …?” (count only real interactions).</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'Blocks of 2 kg and 3 kg touch each other on a smooth floor. A 10 N horizontal force pushes the 2 kg block. Find the contact force. What if the 10 N pushes the 3 kg block instead?',
                 steps=[r'a = 10/(2 + 3) = 2 m/s² in both cases.',
                        r'Push on 2 kg: the contact force must accelerate the 3 kg block: N = 3 × 2 = 6 N.',
                        r'Push on 3 kg: it must accelerate the 2 kg block: N = 2 × 2 = 4 N.',
                        r'The two answers add to 10 N, the applied force. That is a quick check.'],
                 answer=r'6 N; 4 N when pushed from the other side'),
            dict(tag='Numerical', q=r'A 10 kg box on a smooth floor is pulled by a 50 N rope at 37° above the horizontal. Find the normal force and the acceleration (g = 10 m/s², sin 37° = 0.6).',
                 steps=[r'Vertical: N + 50 sin 37° = 100, so N = 100 − 30 = 70 N.',
                        r'Horizontal: 50 cos 37° = 40 N = 10a, so a = 4 m/s².',
                        r'The box stays on the floor because 30 N &lt; 100 N.'],
                 answer=r'N = 70 N, a = 4 m/s²'),
            dict(tag='Concept', q=r'A block rests on a rough incline. How many forces act on it, and which force balances which?',
                 steps=[r'Weight (Earth), normal force (incline surface), static friction (incline surface, up the slope). Three forces.',
                        r'Across the slope: N balances mg cos θ.',
                        r'Along the slope: friction balances mg sin θ.',
                        r'The incline’s total force (N plus friction) is therefore exactly mg upward.'],
                 answer=r'Three forces; the incline’s total push equals mg upward'),
        ],
        practice=[
            dict(q=r'Three blocks of 1 kg, 2 kg and 3 kg in a row on a smooth floor are pushed by 12 N applied to the 1 kg block. The force between the 2 kg and 3 kg blocks is',
                 options=['10 N', '4 N', '2 N', '6 N'], answer=3, type='numerical',
                 explanation=r'a = 12/6 = 2 m/s². The 2–3 contact must accelerate only the 3 kg block: 3 × 2 = 6 N. 10 N is the 1–2 contact force (it pushes 5 kg).'),
            dict(q=r'A 2 kg block is held at rest on a smooth 45° incline by a horizontal force. The normal force on the block is (g = 10 m/s²)',
                 options=['20 N', r'\(20\sqrt2\) N', r'\(10\sqrt2\) N', '40 N'], answer=1, type='numerical',
                 explanation=r'Along the slope: F cos 45° = mg sin 45°, so F = 20 N. Across: N = mg cos 45° + F sin 45° = \(10\sqrt2 + 10\sqrt2 = 20\sqrt2 \approx 28.3\) N, i.e. mg/cos θ. \(10\sqrt2\) is mg cos θ, which ignores the horizontal force pressing into the slope.'),
            dict(q=r'A 5 kg block on a level floor is pushed by a 20 N force directed 30° below the horizontal. The normal force is (g = 10 m/s²)',
                 options=['60 N', '40 N', '50 N', r'\(50 + 10\sqrt3\) N'], answer=0, type='numerical',
                 explanation=r'The push has a downward part 20 sin 30° = 10 N, so N = 50 + 10 = 60 N. 40 N treats the force as pulling upward; \(10\sqrt3\) is the horizontal part.'),
            dict(q=r'Statement I: The normal force on a body resting on a horizontal surface is always equal to its weight.<br>Statement II: The normal force acts perpendicular to the surface of contact.',
                 options=ST_OPTS, answer=2, type='statement',
                 explanation=r'N adjusts to whatever is needed: an extra push, an upward pull or vertical acceleration changes it. So Statement I is false. Statement II is the definition of the normal force.'),
        ],
    ),

    'laws-connected': dict(
        level='exam',
        notes=[
            ('Method: system first, then one body', r'''<ol><li>Treat all connected bodies as one system moving with a common acceleration a. Internal tensions cancel. \(a = \dfrac{\text{net external driving force}}{\text{total mass}}\).</li>
<li>Isolate the simplest single body and apply \(\sum F = ma\) to find the tension.</li>
<li>Check with another body.</li></ol>
<p>Block \(m_1\) on a smooth table, pulled by a hanging \(m_2\): \(a = \dfrac{m_2g}{m_1+m_2}\) and \(T = \dfrac{m_1m_2g}{m_1+m_2}\). In a chain of blocks pulled by F, the tension at any joint equals the force needed to accelerate everything behind that joint.</p>'''),
            ('Movable pulleys: derive the constraint', r'''<p>Write the total string length in terms of the positions and differentiate twice.</p>
<ul><li>A load hanging from a movable pulley, with the string fixed at one end and pulled at the other: if the free end moves by x, the load moves by x/2. So \(a_{\rm load} = a_{\rm end}/2\).</li>
<li>The movable pulley has two segments pulling up, so \(2T - Mg = Ma_{\rm load}\).</li>
<li>Energy check: the tension does equal and opposite work at the two ends, so T times the end’s displacement must equal 2T times the load’s displacement.</li></ul>'''),
            ('Limiting cases and the force on the pulley', r'''<ul><li>Atwood with \(m_1 = m_2\): a = 0 and T = mg.</li>
<li>\(m_2 \gg m_1\): a → g and \(T \to 2m_1g\).</li>
<li>Tension always lies between \(m_1g\) and \(m_2g\).</li>
<li>The clamp of a fixed pulley carries the resultant of the two tensions: 2T when both strings hang vertically, \(T\sqrt2\) when they are at right angles. It is not \((m_1+m_2)g\) while the masses accelerate.</li>
<li>Atwood machine in a lift accelerating up at \(a_0\): replace g by \(g + a_0\) everywhere.</li></ul>'''),
        ],
        formulas=[
            dict(title='Block on a table pulled by a hanging mass', formula=r'a=\frac{m_2g}{m_1+m_2},\qquad T=\frac{m_1m_2g}{m_1+m_2}',
                 symbols='m₁ block on a smooth table (kg); m₂ hanging mass (kg); light string, light smooth pulley.'),
            dict(title='Force on a fixed pulley', formula=r'F_{\rm clamp}=2T\cos\frac{\phi}{2}',
                 symbols='T string tension (N); φ angle between the two string segments leaving the pulley. φ = 0 (both vertical) gives 2T; φ = 90° gives T√2.'),
            dict(title='Atwood machine in an accelerating lift', formula=r'a_{\rm rel}=\frac{(m_2-m_1)(g+a_0)}{m_1+m_2},\qquad T=\frac{2m_1m_2(g+a_0)}{m_1+m_2}',
                 symbols='a₀ upward acceleration of the lift (m/s²; negative if downward); a_rel acceleration of the masses relative to the lift.'),
        ],
        figure=dict(svg=FIG_TABLE_PULLEY,
                    caption=r'The same tension T pulls \(m_1\) along the table and holds back \(m_2\). Treating both as one system gives a; one body alone gives T.'),
        traps=[r'The force on a pulley’s clamp is 2T (for vertical strings), not \((m_1 + m_2)g\). While the masses accelerate, 2T is less than the total weight.',
               r'With a movable pulley the two masses do not have equal accelerations. Use the string-length constraint before writing the equations.'],
        exam=r'''<ul><li>“Find the acceleration and tension” for an Atwood machine, a block on a table with a hanging mass, or a block on an incline with a hanging mass.</li>
<li>“If the acceleration is g/8, find the ratio of the masses.”</li>
<li>“Tension between blocks 2 and 3 in a chain pulled by F.”</li>
<li>“Force exerted by the pulley on the clamp.”</li>
<li>Movable pulley constraints; Atwood machine in a lift.</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'Blocks of 1 kg, 2 kg and 3 kg on a smooth floor are tied in a line by light strings. An 18 N force pulls the 3 kg block. Find the acceleration and both tensions.',
                 steps=[r'a = 18/(1 + 2 + 3) = 3 m/s².',
                        r'String between 2 kg and 3 kg pulls the 1 kg and 2 kg blocks: T = (1 + 2) × 3 = 9 N.',
                        r'String between 1 kg and 2 kg pulls only the 1 kg block: T = 1 × 3 = 3 N.',
                        r'Check on the 3 kg block: 18 − 9 = 9 = 3 × 3. It agrees.'],
                 answer=r'a = 3 m/s²; tensions 9 N and 3 N'),
            dict(tag='Constraint', q=r'A 2 kg block on a smooth table is tied to a string that passes over a fixed pulley at the edge, goes down under a movable pulley carrying a 4 kg load, and is fixed to the ceiling. Find the accelerations and the tension (g = 10 m/s², light pulleys).',
                 steps=[r'Constraint: if the block moves x, the load drops x/2. So \(a_{\rm block} = 2a\) where a is the load’s acceleration.',
                        r'Block: T = 2(2a) = 4a.',
                        r'Load (two segments up): 40 − 2T = 4a, so 40 − 8a = 4a and a = 10/3 ≈ 3.33 m/s².',
                        r'Block: 2a = 20/3 ≈ 6.67 m/s². Tension T = 4a = 40/3 ≈ 13.3 N.'],
                 answer=r'Load 10/3 m/s², block 20/3 m/s², T = 40/3 N'),
            dict(tag='Ratio', q=r'In an ideal Atwood machine the acceleration is g/4. Find the ratio of the masses.',
                 steps=[r'\(\dfrac{m_2 - m_1}{m_2 + m_1} = \dfrac14\).',
                        r'\(4m_2 - 4m_1 = m_2 + m_1\), so \(3m_2 = 5m_1\).',
                        r'\(m_2 : m_1 = 5 : 3\).'],
                 answer=r'5 : 3'),
            dict(tag='Numerical', q=r'An Atwood machine with 2 kg and 3 kg masses hangs in a lift that accelerates upward at 2 m/s². Find the acceleration of the masses relative to the lift and the tension.',
                 steps=[r'Effective gravity in the lift: \(g + a_0 = 12\) m/s².',
                        r'\(a_{\rm rel} = (3 - 2) \times 12/5 = 2.4\) m/s².',
                        r'\(T = 2(2)(3)(12)/5 = 28.8\) N, more than the 24 N in a stationary lift.'],
                 answer=r'2.4 m/s² relative to the lift; T = 28.8 N'),
        ],
        practice=[
            dict(q=r'In an ideal Atwood machine the masses accelerate at g/8. The ratio of the larger mass to the smaller is',
                 options=['8 : 7', '9 : 7', '9 : 8', '2 : 1'], answer=1, type='numerical',
                 explanation=r'\((m_2 - m_1)/(m_2 + m_1) = 1/8\) gives \(7m_2 = 9m_1\), so 9 : 7. 9 : 8 sets \(m_2/m_1 = 1 + 1/8\), which is not the Atwood relation.'),
            dict(q=r'An ideal Atwood machine has masses 2 kg and 3 kg hanging over a pulley fixed to the ceiling. The force on the ceiling from the pulley clamp (light pulley) is (g = 10 m/s²)',
                 options=['50 N', '24 N', '48 N', '10 N'], answer=2, type='numerical',
                 explanation=r'T = 2(2)(3)(10)/5 = 24 N. Both strings pull the pulley down, so the clamp carries 2T = 48 N. 50 N would be the total weight, which applies only if the masses were not accelerating.'),
            dict(q=r'In an Atwood machine, \(m_1\) is kept fixed and \(m_2\) is made very large. The string tension approaches',
                 options=[r'\(m_1g\)', r'\(m_2g\)', r'infinity', r'\(2m_1g\)'], answer=3, type='concept',
                 explanation=r'\(T = 2m_1m_2g/(m_1 + m_2) \to 2m_1g\) as \(m_2 \to \infty\). Physically \(m_1\) is then dragged up at nearly g, needing \(T - m_1g = m_1g\). The tension does not grow without limit.'),
            dict(q=r'Blocks of 2 kg, 4 kg and 6 kg on a smooth floor are connected in a line by light strings and pulled by 24 N applied to the 2 kg block. The tension in the string between the 4 kg and 6 kg blocks is',
                 options=['4 N', '20 N', '12 N', '24 N'], answer=2, type='numerical',
                 explanation=r'a = 24/12 = 2 m/s². The 4–6 string pulls only the 6 kg block: T = 6 × 2 = 12 N. 20 N is the 2–4 string, which pulls 10 kg; 4 N assumes the string pulls 2 kg.'),
        ],
    ),

    'laws-lift': dict(
        level='core',
        notes=[
            ('All the lift cases in one table', r'''<p>Take up as positive. For a person of mass m on a scale, \(N - mg = ma\), so \(N = m(g + a)\).</p>
<ul><li>At rest or moving at constant velocity (up or down): a = 0, N = mg.</li>
<li>Moving up and speeding up, or moving down and slowing down: a upward, N = m(g + a) &gt; mg.</li>
<li>Moving up and slowing down, or moving down and speeding up: a downward, N = m(g − a) &lt; mg.</li>
<li>Free fall (cable broken): a = g downward, N = 0 (weightlessness).</li>
<li>Downward acceleration greater than g: the person would press against the ceiling instead.</li></ul>
<p>The scale reading depends on the direction of the <em>acceleration</em>, never on the direction of the velocity.</p>'''),
            ('Effective gravity inside the lift', r'''<p>Everything inside a lift with upward acceleration \(a_0\) behaves as if gravity were \(g_{\rm eff} = g + a_0\) (or \(g - a_0\) for downward acceleration).</p>
<ul><li>A pendulum’s period becomes \(T = 2\pi\sqrt{L/g_{\rm eff}}\).</li><li>A ball dropped from height h inside the lift reaches the floor in \(\sqrt{2h/g_{\rm eff}}\).</li>
<li>The cable tension for a lift of total mass M (cage plus load) is \(M(g + a_0)\).</li>
<li>A beam (pan) balance still balances, because both pans feel the same \(g_{\rm eff}\). A spring balance changes its reading.</li></ul>'''),
        ],
        formulas=[
            dict(title='Effective gravity in a lift', formula=r'g_{\rm eff}=g+a_0,\qquad T_{\rm pend}=2\pi\sqrt{\frac{L}{g_{\rm eff}}}',
                 symbols='a₀ lift acceleration (m/s²), positive upward, negative downward; L pendulum length (m); T_pend period (s).'),
            dict(title='Cable tension', formula=r'T_{\rm cable}=M(g+a_0)',
                 symbols='M total mass of the cage and everything in it (kg); a₀ upward acceleration (m/s²).'),
        ],
        figure=dict(svg=FIG_LIFT_GRAPH,
                    caption=r'A lift going up: speeding up, steady, slowing down. The slope of the v–t graph is the acceleration, and that alone decides the scale reading in each phase.'),
        traps=[r'A beam balance reads the same in an accelerating lift, because the effective gravity acts equally on both pans. Only a spring balance changes.',
               r'“The lift is moving down” does not tell you the reading. You need to know whether it is speeding up or slowing down.'],
        exam=r'''<ul><li>“A man of mass … stands on a scale in a lift accelerating up/down at … The reading is …”</li>
<li>Graph question: a v–t (or reading–t) graph of a lift journey; find the reading in each phase.</li>
<li>“The scale reads 48 kg for a 60 kg man. Find the lift’s acceleration.”</li>
<li>“Time period of a pendulum in a lift / in a freely falling lift.”</li>
<li>“Tension in the cable of a lift.”</li></ul>''',
        examples=[
            dict(tag='Graph', q=r'A lift carrying a 60 kg man goes up. Its speed rises uniformly from 0 to 4 m/s in 2 s, stays at 4 m/s until t = 6 s, then falls uniformly to 0 at t = 10 s. Find the scale reading in each phase (g = 10 m/s²).',
                 steps=[r'0–2 s: a = 4/2 = 2 m/s² upward. N = 60(10 + 2) = 720 N.',
                        r'2–6 s: a = 0. N = 600 N.',
                        r'6–10 s: a = −4/4 = −1 m/s². N = 60(10 − 1) = 540 N.',
                        r'Distance travelled = area under the graph = ½(2)(4) + 4(4) + ½(4)(4) = 4 + 16 + 8 = 28 m.'],
                 answer=r'720 N, 600 N, 540 N'),
            dict(tag='Numerical', q=r'A pendulum has a period of 2 s in a stationary lift. What is its period when the lift accelerates downward at 7.5 m/s²?',
                 steps=[r'\(g_{\rm eff} = 10 - 7.5 = 2.5\) m/s².',
                        r"\(T \propto 1/\sqrt{g_{\rm eff}}\): \(T^{\prime} = 2\sqrt{10/2.5} = 2 \times 2 = 4\) s.",
                        r'In free fall \(g_{\rm eff} = 0\) and the pendulum would not oscillate at all.'],
                 answer=r'4 s'),
            dict(tag='Concept', q=r'A man in a freely falling lift lets go of an apple at shoulder height. What does he see, and why?',
                 steps=[r'The man, the apple and the lift all accelerate downward at g.',
                        r'Relative to the lift the apple has zero acceleration, so it stays where it was released.',
                        r'Gravity still acts on the apple. It only appears weightless because nothing needs to support it.'],
                 answer=r'The apple floats beside him'),
        ],
        practice=[
            dict(q=r'A lift cage of 500 kg carries a 100 kg passenger and accelerates upward at 2 m/s². The tension in the cable is (g = 10 m/s²)',
                 options=['6000 N', '7200 N', '4800 N', '1200 N'], answer=1, type='numerical',
                 explanation=r'T − (600)(10) = 600 × 2, so T = 600 × 12 = 7200 N. 6000 N ignores the acceleration and 4800 N uses g − a, which applies to downward acceleration.'),
            dict(q=r'During a lift ride, a scale under a passenger first reads more than mg, then exactly mg, then less than mg, and the lift ends at rest. The lift was',
                 options=['going down throughout', 'going up and then down', 'going up throughout', 'in free fall at the end'], answer=2, type='graph',
                 explanation=r'Reading &gt; mg means upward acceleration; mg means steady; &lt; mg means downward acceleration. Speeding up, then steady, then slowing, while going up, ends at rest. A downward trip would show &lt; mg first, then &gt; mg.'),
            dict(q=r'A beam balance and a spring balance both read 5 kg for the same object in a stationary lift. When the lift accelerates upward,',
                 options=['both readings increase', 'both stay the same', 'the beam balance increases, the spring balance stays the same', 'the beam balance stays the same, the spring balance increases'], answer=3, type='concept',
                 explanation=r'The beam balance compares two masses that feel the same \(g_{\rm eff}\), so it still balances at 5 kg. The spring balance reads the force \(m(g + a)\), which increases.'),
            dict(q=r'A 60 kg man stands on a scale in a lift. The scale reads 480 N. The lift is (g = 10 m/s²)',
                 options=['accelerating downward at 2 m/s²', 'accelerating upward at 2 m/s²', 'moving at a constant 2 m/s', 'in free fall'], answer=0, type='numerical',
                 explanation=r'60(10 − a) = 480 gives a = 2 m/s² downward. The lift may be going down and speeding up, or going up and slowing down. Constant velocity would give 600 N; free fall would give zero.'),
        ],
    ),

    'laws-impulse': dict(
        level='core',
        notes=[
            ('Impulse from a force–time graph', r'''<p>Impulse is the area under the F–t graph. For a triangle use ½ × base × height; for a rectangle, base × height. Areas below the time axis count as negative.</p>
<p>The same impulse can be delivered as a large force for a short time or a small force for a long time. Average force = impulse ÷ contact time.</p>'''),
            ('Why soft landings work', r'''<ul><li>A fielder pulls the hands back while catching: the ball’s momentum change is fixed, but the stopping time grows, so the force on the hands falls.</li>
<li>Jumping onto sand or bending the knees on landing, air bags, packing material, shock absorbers: all increase Δt.</li>
<li>A ball that bounces back suffers a larger Δp (up to twice) than one that stops, so it needs a larger impulse.</li></ul>'''),
            ('Using conservation of momentum', r'''<ul><li><strong>Recoil:</strong> a gun of mass M fires a bullet m at v. Total momentum stays zero: \(MV = mv\), so \(V = mv/M\), opposite to the bullet.</li>
<li><strong>Explosion at rest:</strong> fragment momenta add to zero. For two pieces they are equal and opposite. For three pieces, any one is opposite to the vector sum of the other two.</li>
<li><strong>Ball hitting a wall at an angle:</strong> only the component normal to the wall reverses, so \(|\Delta p| = 2mv\cos\theta\) with θ measured from the normal.</li></ul>'''),
        ],
        formulas=[
            dict(title='Recoil velocity', formula=r'V=\frac{mv}{M}',
                 symbols='m bullet mass, M gun mass (kg); v bullet speed (m/s); V recoil speed of the gun (m/s), opposite to v. System initially at rest, no external horizontal impulse.'),
            dict(title='Oblique bounce from a wall', formula=r'|\Delta\vec p|=2mv\cos\theta',
                 symbols='m mass (kg); v speed (m/s) before and after an elastic bounce; θ angle with the normal to the wall. Direction of Δp: along the normal, away from the wall.'),
        ],
        figure=dict(svg=FIG_FT,
                    caption=r'The impulse of a blow is the area under its F–t curve. Here it is 6 N s, delivered in 0.03 s, so the average force is 200 N.'),
        traps=[r'For an oblique bounce, use the component along the normal. θ measured from the wall surface (not the normal) turns cos into sin.',
               r'Kinetic energy is not conserved in an explosion; it increases because chemical energy is released. Only momentum is conserved.'],
        exam=r'''<ul><li>F–t graph: find impulse, final velocity or average force.</li>
<li>“A ball of mass … hits a wall at … with the normal and rebounds with the same speed. Change in momentum.”</li>
<li>“A gun of mass … fires a bullet … recoil speed / recoil KE.”</li>
<li>“A bomb at rest explodes into pieces … find the velocity / KE of the third piece.”</li>
<li>Assertion–reason on catching a ball, jumping on sand, air bags.</li></ul>''',
        examples=[
            dict(tag='Graph', q=r'A force on a 0.2 kg ball at rest rises linearly from 0 to 400 N in 0.01 s and then falls linearly to 0 at 0.03 s. Find the impulse and the ball’s final speed.',
                 steps=[r'Impulse = area of the triangle = ½ × 0.03 × 400 = 6 N s.',
                        r'\(\Delta p = 6\) kg m/s, so v = 6/0.2 = 30 m/s.',
                        r'Average force = 6/0.03 = 200 N, half the peak, as expected for a triangle.'],
                 answer=r'6 N s; 30 m/s'),
            dict(tag='Numerical', q=r'A 4 kg gun fires a 20 g bullet at 400 m/s. Find the recoil speed of the gun and compare the kinetic energies.',
                 steps=[r'\(V = mv/M = 0.02 \times 400/4 = 2\) m/s, backward.',
                        r'KE of the bullet = ½ × 0.02 × 400² = 1600 J. KE of the gun = ½ × 4 × 2² = 8 J.',
                        r'Equal momenta, but KE = p²/2m, so the lighter body gets almost all the energy.'],
                 answer=r'2 m/s; bullet 1600 J, gun 8 J'),
            dict(tag='Numerical', q=r'A shell at rest explodes into three equal pieces. Two fly off at right angles to each other at 30 m/s each. Find the velocity of the third piece.',
                 steps=[r'Each piece has mass m. The two known momenta are perpendicular, each 30m.',
                        r'Their resultant is \(30m\sqrt2\), at 45° to each.',
                        r'The third piece must cancel this: speed \(30\sqrt2 \approx 42.4\) m/s, opposite to the resultant, i.e. at 135° to each of the other two.'],
                 answer=r'\(30\sqrt2 \approx 42.4\) m/s at 135° to each of the other pieces'),
            dict(tag='Numerical', q=r'A 0.1 kg ball hits a wall at 10 m/s, making 60° with the normal, and rebounds at the same speed and angle. Find the change in its momentum.',
                 steps=[r'Along the wall: \(v\sin60^\circ\) is unchanged.',
                        r'Along the normal: \(v\cos60^\circ = 5\) m/s reverses.',
                        r'\(|\Delta p| = 2 \times 0.1 \times 5 = 1\) kg m/s, along the normal, away from the wall.'],
                 answer=r'1 kg m/s, normal to the wall'),
        ],
        practice=[
            dict(q=r'A 3 kg body at rest feels a force of 10 N for 2 s, after which the force decreases linearly to zero at t = 4 s. Its final speed is',
                 options=['10 m/s', '6.7 m/s', '13.3 m/s', '20 m/s'], answer=0, type='graph',
                 explanation=r'Impulse = rectangle + triangle = 10 × 2 + ½ × 2 × 10 = 30 N s, so v = 30/3 = 10 m/s. 6.7 m/s counts only the rectangle; 13.3 m/s counts the triangle as a full rectangle.'),
            dict(q=r'A 0.5 kg ball strikes a wall at 10 m/s at 45° to the normal and rebounds elastically at the same angle. The magnitude of the change in its momentum is',
                 options=['0', '5 kg m/s', r'\(5\sqrt2\) kg m/s', '10 kg m/s'], answer=2, type='numerical',
                 explanation=r'Only the normal component \(10\cos45^\circ\) reverses: \(|\Delta p| = 2 \times 0.5 \times 10 \times (1/\sqrt2) = 5\sqrt2 \approx 7.1\) kg m/s. 10 kg m/s would be a head-on bounce; zero confuses equal speeds with equal velocities.'),
            dict(q=r'A 12 kg bomb at rest explodes into two pieces of 4 kg and 8 kg. The 8 kg piece moves at 6 m/s. The kinetic energy of the 4 kg piece is',
                 options=['72 J', '144 J', '216 J', '288 J'], answer=3, type='numerical',
                 explanation=r'Momentum: 4v = 8 × 6, so v = 12 m/s. KE = ½ × 4 × 144 = 288 J. 144 J is that of the 8 kg piece; 72 J uses 6 m/s for the light piece.'),
            dict(q=r'Assertion (A): A cricketer moves his hands backward while catching a fast ball.<br>Reason (R): Moving the hands back reduces the change in momentum of the ball.',
                 options=AR_OPTS, answer=2, type='ar',
                 explanation=r'The ball must be stopped either way, so Δp is the same. Moving the hands back increases the stopping time, which reduces the average force. A is true but R is false.'),
        ],
    ),

    'laws-circular': dict(
        level='exam',
        notes=[
            ('Derivation: banking angle, with and without friction', r'''<p>Car on a road banked at θ, moving in a horizontal circle of radius r.</p>
<ol><li>Without friction: vertical \(N\cos\theta = mg\); horizontal (toward the centre) \(N\sin\theta = mv^2/r\). Divide: \(\tan\theta = v^2/rg\). Note \(N = mg/\cos\theta\), larger than mg.</li>
<li>With friction μ, at the maximum speed friction acts down the slope: \(N\cos\theta - \mu N\sin\theta = mg\) and \(N\sin\theta + \mu N\cos\theta = mv^2/r\). Dividing:</li></ol>
\[v_{\max}^2=rg\,\frac{\mu+\tan\theta}{1-\mu\tan\theta},\qquad v_{\min}^2=rg\,\frac{\tan\theta-\mu}{1+\mu\tan\theta}\]
<p>At the minimum speed friction acts up the slope. On a level road (θ = 0), \(v_{\max} = \sqrt{\mu rg}\).</p>'''),
            ('Cyclists, conical pendulums and bridges', r'''<ul><li>A cyclist leans at θ from the vertical with \(\tan\theta = v^2/rg\), the same as the banking angle.</li>
<li>Conical pendulum (string L at θ to the vertical): \(T\cos\theta = mg\), \(T\sin\theta = mv^2/r\), period \(2\pi\sqrt{L\cos\theta/g}\).</li>
<li>Car over the top of a convex bridge (hump) of radius r: \(mg - N = mv^2/r\), so N falls as v rises. Contact is lost at \(v = \sqrt{gr}\).</li>
<li>Car at the bottom of a dip: \(N - mg = mv^2/r\), so the passengers feel heavier.</li></ul>'''),
            ('Vertical circle: the two key equations', r'''<p>Mass on a string of length r in a vertical circle:</p>
<ul><li>Top: \(T + mg = mv^2/r\). The string stays taut only if \(v_{\rm top} \ge \sqrt{gr}\).</li>
<li>Bottom: \(T - mg = mv^2/r\). Energy conservation gives \(v_{\rm bottom}^2 = v_{\rm top}^2 + 4gr\), so the minimum speed at the bottom is \(\sqrt{5gr}\).</li>
<li>With the minimum speeds, the tension is 0 at the top and 6mg at the bottom.</li></ul>'''),
        ],
        formulas=[
            dict(title='Banked road with friction', formula=r'v_{\max}=\sqrt{rg\,\frac{\mu+\tan\theta}{1-\mu\tan\theta}}',
                 symbols='r radius of the turn (m); θ banking angle; μ coefficient of static friction; g gravity (m/s²). For the minimum speed replace μ by −μ.'),
            dict(title='Level road and convex bridge', formula=r'v_{\max}=\sqrt{\mu rg}\ \ (\text{level road}),\qquad v_{\max}=\sqrt{gr}\ \ (\text{top of a hump})',
                 symbols='μ static friction coefficient; r radius of the turn or of the hump (m). Above these speeds the car skids or leaves the road.'),
            dict(title='Vertical circle on a string', formula=r'v_{\rm top,min}=\sqrt{gr},\qquad v_{\rm bottom,min}=\sqrt{5gr}',
                 symbols='r radius = string length (m); g gravity (m/s²). Light string, no air resistance.'),
        ],
        figure=dict(svg=FIG_BANK,
                    caption=r'On a frictionless banked road the normal force tilts toward the centre. Its vertical part balances mg and its horizontal part supplies \(mv^2/r\).'),
        traps=[r'On a banked road at the design speed, \(N = mg/\cos\theta\), not \(mg\cos\theta\). The block-on-incline result does not apply because here the acceleration is horizontal.',
               r'“Centrifugal force” is not a real force in the ground frame. If you are working from the ground, the only forces are mg, N, friction and tension.'],
        exam=r'''<ul><li>“Maximum speed on a level road with μ …” and “banking angle for speed …”</li>
<li>“Maximum safe speed on a banked road with friction.”</li>
<li>“Angle at which a cyclist must lean.”</li>
<li>“Minimum speed at the top of a vertical circle” and “tension at the top / bottom”.</li>
<li>“Normal force on a car at the top of a hump / bottom of a dip.”</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'A cyclist rides at 10 m/s round a curve of radius 10 m. At what angle to the vertical must he lean? (g = 10 m/s²)',
                 steps=[r'\(\tan\theta = v^2/rg = 100/100 = 1\).',
                        r'θ = 45° from the vertical.',
                        r'The same formula gives the frictionless banking angle for that speed and radius.'],
                 answer=r'45°'),
            dict(tag='Numerical', q=r'A car goes over a hump of radius 40 m. What is the greatest speed at which it stays in contact? At 10 m/s, what fraction of its weight does the road support?',
                 steps=[r'At the top, \(mg - N = mv^2/r\). Contact is lost when N = 0: \(v = \sqrt{gr} = \sqrt{400} = 20\) m/s.',
                        r'At 10 m/s: \(N = m(10 - 100/40) = 7.5m\).',
                        r'N/mg = 7.5/10 = 0.75. The car feels 25% lighter.'],
                 answer=r'20 m/s; 75% of its weight'),
            dict(tag='Ratio', q=r'A road is banked for a design speed v. By what factor must tan θ change to make the design speed 2v on the same curve?',
                 steps=[r'\(\tan\theta = v^2/rg \propto v^2\).',
                        r'Doubling v multiplies tan θ by 4.',
                        r'The angle itself does not quadruple. For example, tan θ going from 0.1 to 0.4 changes θ from about 5.7° to about 21.8°.'],
                 answer=r'tan θ becomes 4 times larger'),
            dict(tag='Numerical', q=r'A 0.5 kg stone on a 1 m string moves in a vertical circle. At the top its speed is 4 m/s. Find the tension there. Is 4 m/s enough to keep the string taut?',
                 steps=[r'Minimum speed at the top \(= \sqrt{gr} = \sqrt{10} \approx 3.16\) m/s. 4 m/s is enough.',
                        r'\(T + mg = mv^2/r\): \(T = 0.5 \times 16/1 - 0.5 \times 10 = 8 - 5 = 3\) N.'],
                 answer=r'3 N; yes, the string stays taut'),
        ],
        practice=[
            dict(q=r'The maximum speed at which a car can take a level curve of radius 40 m without skidding, if μ = 0.4, is (g = 10 m/s²)',
                 options=['8 m/s', '16 m/s', '20 m/s', r'\(4\sqrt{10}\) m/s'], answer=3, type='numerical',
                 explanation=r'Friction supplies the centripetal force: \(\mu mg = mv^2/r\), so \(v = \sqrt{0.4 \times 40 \times 10} = \sqrt{160} = 4\sqrt{10} \approx 12.6\) m/s. 16 m/s forgets the square root of μrg.'),
            dict(q=r'A stone on a 2.5 m string is whirled in a vertical circle. The minimum speed at the top for the string to stay taut is (g = 10 m/s²)',
                 options=['5 m/s', '25 m/s', r'\(5\sqrt5\) m/s', '2.5 m/s'], answer=0, type='numerical',
                 explanation=r'At the top with T = 0, gravity alone gives the centripetal force: \(v = \sqrt{gr} = \sqrt{25} = 5\) m/s. \(5\sqrt5\) is \(\sqrt{5gr}\), the minimum speed at the <em>bottom</em>.'),
            dict(q=r'A curve of radius 100 m is banked at 37° (tan 37° = 0.75), and μ = 0.5. The maximum safe speed is (g = 10 m/s²)',
                 options=['25 m/s', r'\(20\sqrt5\) m/s', r'\(5\sqrt{30}\) m/s', '50 m/s'], answer=1, type='numerical',
                 explanation=r'\(v^2 = rg(\mu + \tan\theta)/(1 - \mu\tan\theta) = 1000 \times 1.25/0.625 = 2000\), so \(v = 20\sqrt5 \approx 44.7\) m/s. \(5\sqrt{30} \approx 27.4\) m/s is the frictionless design speed \(\sqrt{rg\tan\theta}\).'),
            dict(q=r'Statement I: On a frictionless banked road, a car moving at the design speed experiences a normal force \(mg\cos\theta\).<br>Statement II: At the design speed, no friction is needed to take the turn.',
                 options=ST_OPTS, answer=2, type='statement',
                 explanation=r'Vertical balance gives \(N\cos\theta = mg\), so \(N = mg/\cos\theta\), and Statement I is false. At the design speed the horizontal part of N supplies all of \(mv^2/r\), so Statement II is true.'),
        ],
    ),
}


NEW_SECTIONS = [
    dict(chapter='laws', after='laws-fbd', id='laws-tension',
         title='Strings, springs and concurrent-force equilibrium',
         intro=r'A string can only pull, and only along its length. If it is light (massless) and passes over nothing rough, the tension is the same all along it. A spring pushes or pulls along its axis with force kx. A spring balance simply reads the tension in its own spring.',
         reasoning=r'A massive rope is different: each piece must also be accelerated or supported, so the tension changes along it. In a hanging rope the tension at a point equals the weight of everything below that point. For a rope pulled across a smooth floor, the tension at a point equals the force needed to accelerate everything behind it.',
         formula=r'T(x)=\frac{M}{L}xg\ \ (\text{hanging rope}),\qquad T(x)=\frac{x}{L}F\ \ (\text{rope pulled on a smooth floor}),\qquad F_s=kx',
         symbols='M rope mass (kg); L rope length (m); x distance from the free (lower or trailing) end (m); F pull on the leading end (N); g gravity (m/s²); k spring constant (N/m); x in F_s is the spring’s extension (m).',
         trap=r'A spring balance with equal 5 kg masses hanging from both ends (over pulleys) reads 5 kg-wt, not 10 kg-wt and not zero. One end must be held for the balance to read anything, and the other mass is doing exactly that.',
         example=r'A spring balance hangs in the middle of a string that runs over two pulleys, with a 5 kg mass on each end. What does it read?',
         solution=r'Each mass is at rest, so the tension on each side is mg = 50 N. The spring is pulled by 50 N at each end, which is exactly the situation of a balance hung from a hook with 5 kg on it. It reads 50 N (5 kg-wt).',
         question=r'A uniform rope of mass 2 kg and length 4 m hangs vertically from a ceiling. The tension at its midpoint is (g = 10 m/s²)',
         options=r'0|10 N|20 N|5 N', answer=1,
         explanation=r'The midpoint supports the lower half, of mass 1 kg, so T = 10 N. 20 N is the tension at the top, and 0 is at the bottom end.',
         deep=dict(
             level='core',
             notes=[
                 ('Massless versus massive rope', r'''<ul><li><strong>Massless string:</strong> the net force on any piece must be zero (zero mass × finite acceleration), so the tension is the same at both ends of every piece.</li>
<li><strong>Hanging rope of mass M with a load m at the bottom:</strong> at distance x from the bottom, \(T = (m + Mx/L)g\). So the top carries \((m + M)g\).</li>
<li><strong>Rope of mass M pulling a block m on a smooth floor with force F:</strong> a = F/(M + m). The tension at the block end is ma, which is less than F. A massless rope would transmit the full F.</li></ul>'''),
                 ('Springs: combinations and the “cut” problem', r'''<ul><li>Series: \(1/k = 1/k_1 + 1/k_2\). Parallel: \(k = k_1 + k_2\).</li>
<li>Cutting a spring into n equal pieces: each has constant nk (k ∝ 1/length).</li>
<li>A spring force cannot change instantly, because the extension needs time to change. A string tension can change instantly.</li>
<li>So just after a string is cut, any body still attached to a spring feels the old spring force. This gives non-obvious instantaneous accelerations, such as g upward.</li></ul>'''),
                 ('Equilibrium of a knot', r'''<p>Where several strings meet at a light knot, the knot has no mass, so the forces on it must add to zero. Resolve along two axes, or use Lami’s theorem from the Vectors chapter when exactly three strings meet. The tension in each string is then fixed by geometry and the hanging weight.</p>'''),
             ],
             formulas=[
                 dict(title='Hanging rope with a load', formula=r'T(x)=\left(m+\frac{M}{L}x\right)g',
                      symbols='m load at the bottom (kg); M rope mass (kg); L rope length (m); x distance above the bottom end (m). Equilibrium.'),
                 dict(title='Spring combinations', formula=r'\frac{1}{k_s}=\frac{1}{k_1}+\frac{1}{k_2},\qquad k_p=k_1+k_2,\qquad k_{\rm piece}=nk',
                      symbols='k spring constants (N/m); k_s series, k_p parallel; k_piece for each of n equal pieces cut from a spring of constant k. Light springs.'),
             ],
             figure=dict(svg=FIG_BALANCE,
                         caption=r'Equal 5 kg masses over two pulleys. The spring balance reads the tension T = 50 N: one side acts like the hook, the other like the load.'),
             traps=[r'The tension in a massive hanging rope is not the same everywhere. It is largest at the top and equals zero at a free bottom end.',
                    r'Immediately after a supporting string is cut, a spring keeps its old force. Do not set the spring force to zero at that instant.'],
             exam=r'''<ul><li>“A spring balance has 5 kg hung on each side over pulleys. Its reading is …”</li>
<li>“Tension at the midpoint / at distance x of a uniform hanging rope.”</li>
<li>“A rope of mass M pulls a block … find the tension at the block end / at the midpoint.”</li>
<li>“The string between two hanging blocks is cut. Find the accelerations just after cutting.”</li>
<li>Spring cut in halves / combined in series and parallel.</li></ul>''',
             examples=[
                 dict(tag='Numerical', q=r'A 3 kg block on a smooth floor is pulled by a uniform 2 kg rope. A 50 N force acts on the free end of the rope. Find the tension at the block end and at the midpoint of the rope.',
                      steps=[r'a = 50/(3 + 2) = 10 m/s².',
                             r'Block end: the rope pulls only the block, so T = 3 × 10 = 30 N.',
                             r'Midpoint: it pulls the block and half the rope: T = (3 + 1) × 10 = 40 N.',
                             r'The tension rises from 30 N to 50 N along the rope. A massless rope would carry 50 N everywhere.'],
                      answer=r'30 N at the block, 40 N at the midpoint'),
                 dict(tag='Cut string', q=r'Block A (mass m) hangs from the ceiling by a spring. Block B (mass m) hangs from A by a string. The system is at rest. The string is cut. Find the accelerations of A and B just after the cut.',
                      steps=[r'Before the cut the spring supports both blocks, so its force is 2mg upward on A.',
                             r'Just after the cut the spring still pulls A up with 2mg. Its weight is mg. Net force mg upward, so \(a_A = g\) upward.',
                             r'B has only its weight acting: \(a_B = g\) downward.'],
                      answer=r'A: g upward; B: g downward'),
                 dict(tag='Numerical', q=r'A spring of constant 100 N/m is cut into two equal halves, and the halves are joined side by side (in parallel). What extension does a 20 N load produce?',
                      steps=[r'Each half has twice the constant: 200 N/m.',
                             r'In parallel: k = 200 + 200 = 400 N/m.',
                             r'Extension = 20/400 = 0.05 m = 5 cm. The original spring would have stretched 20 cm.'],
                      answer=r'5 cm'),
             ],
             practice=[
                 dict(q=r'A spring balance is attached to a string that passes over two smooth pulleys, with a 10 kg mass hanging from each end. The balance reads',
                      options=['zero', '10 kg-wt', '20 kg-wt', '5 kg-wt'], answer=1, type='concept',
                      explanation=r'The tension on each side is 10g, and the balance reads the tension in its spring: 10 kg-wt. Zero assumes the pulls cancel, but cancelling forces are what keep the balance in equilibrium; they still stretch the spring. 20 kg-wt adds the two pulls.'),
                 dict(q=r'A uniform rope of mass M hangs vertically with a block of mass M tied to its lower end. The ratio of the tension at the top of the rope to that at its midpoint is',
                      options=['2 : 1', '3 : 2', '4 : 3', '1 : 1'], answer=2, type='numerical',
                      explanation=r'Top: (M + M)g = 2Mg. Midpoint: (M + M/2)g = 1.5Mg. Ratio 2 : 1.5 = 4 : 3. 2 : 1 is the answer for a rope with no load at the bottom.'),
                 dict(q=r'A spring of constant 100 N/m is cut into two equal halves, which are then connected in parallel. The constant of the combination is',
                      options=['50 N/m', '100 N/m', '200 N/m', '400 N/m'], answer=3, type='numerical',
                      explanation=r'Each half has k = 200 N/m (k ∝ 1/length). In parallel the constants add: 400 N/m. 50 N/m treats the halves as if they were in series without accounting for the cut.'),
                 dict(q=r'Assertion (A): Immediately after the string holding a block to a spring-supported block is cut, the spring force on the upper block is unchanged.<br>Reason (R): A spring’s force depends on its extension, which cannot change instantly.',
                      options=AR_OPTS, answer=0, type='ar',
                      explanation=r'The spring force is kx. Changing x needs the block to move, which takes time, so just after the cut the spring force is the same. R explains A. (A string’s tension, by contrast, can drop to zero instantly.)'),
             ],
         )),

    dict(chapter='laws', after='laws-lift', id='laws-pseudo',
         title='Pseudo force in accelerating frames: trucks, cars and wedges',
         intro=r'In a frame that accelerates at \(\vec a_0\) (a truck, a car, a wedge), Newton’s laws work only if every body is given an extra pseudo force \(-m\vec a_0\), opposite to the frame’s acceleration. No other body exerts this force, so it has no reaction partner.',
         reasoning=r'You may solve any problem from the ground (real forces only) or from the accelerating frame (real forces plus the pseudo force), but never mix the two. A pendulum in a car accelerating at \(a_0\) hangs back at \(\tan\theta = a_0/g\) to the vertical. A block on a smooth wedge stays at rest on it only if the wedge accelerates at \(g\tan\theta\).',
         formula=r'\vec F_{\rm pseudo}=-m\vec a_0,\qquad \tan\theta=\frac{a_0}{g}\ \ (\text{pendulum in an accelerating car})',
         symbols='m mass of the body (kg); a₀ acceleration of the reference frame (m/s²); θ angle of the pendulum string from the vertical, tilted backward. Use only in the accelerating frame.',
         trap=r'Do not add a pseudo force when you write equations in the ground frame. In the ground frame the body simply has acceleration \(a_0\) and the real forces must supply \(ma_0\).',
         example=r'A 0.4 kg bob hangs from the roof of a car that accelerates at 7.5 m/s². Find the string’s angle with the vertical and its tension (g = 10 m/s²).',
         solution=r'In the car frame, mg (down), \(ma_0\) (backward) and T balance. \(\tan\theta = 7.5/10 = 0.75\), so θ = 37° backward from the vertical. \(T = m\sqrt{g^2 + a_0^2} = 0.4 \times 12.5 = 5\) N. From the ground the same result follows from \(T\sin\theta = ma_0\) and \(T\cos\theta = mg\).',
         question=r'A block rests on the smooth inclined face (angle θ) of a wedge. With what horizontal acceleration must the wedge move so that the block does not slide on it?',
         options=r'\(g\sin\theta\)|\(g\cos\theta\)|\(g\tan\theta\)|\(g\cot\theta\)', answer=2,
         explanation=r'In the wedge frame the pseudo force \(ma_0\) has an up-slope component \(ma_0\cos\theta\) that must balance \(mg\sin\theta\). So \(a_0 = g\tan\theta\). \(g\sin\theta\) is the sliding acceleration on a stationary smooth incline, not the required wedge acceleration.',
         deep=dict(
             level='exam',
             notes=[
                 ('One problem, two frames', r'''<p>A 2 kg box sits on the smooth floor of a truck that accelerates forward at 3 m/s².</p>
<ul><li><strong>Ground frame:</strong> no horizontal real force acts on the box, so it stays at rest. The truck slides forward beneath it.</li>
<li><strong>Truck frame:</strong> the box feels a pseudo force 2 × 3 = 6 N backward, so it accelerates backward at 3 m/s² relative to the truck.</li></ul>
<p>Both descriptions agree on what happens. If the floor is rough enough, static friction (6 N forward) keeps the box moving with the truck; Part 2 treats the limit of this.</p>'''),
                 ('Effective gravity in an accelerating vehicle', r'''<p>In a frame with horizontal acceleration \(a_0\), real gravity and the pseudo force combine into an effective gravity \(g_{\rm eff} = \sqrt{g^2 + a_0^2}\), tilted backward at \(\tan\theta = a_0/g\).</p>
<ul><li>A plumb line or pendulum hangs along \(g_{\rm eff}\).</li>
<li>The water surface in a tank on an accelerating truck tilts at the same angle, rising at the back.</li>
<li>A pendulum’s period in the car becomes \(2\pi\sqrt{L/g_{\rm eff}}\), a little shorter than at rest.</li></ul>'''),
                 ('Block on an accelerating smooth wedge', r'''<p>Let the wedge be pushed horizontally at \(a_0\) so that its sloping face moves into the block. In the wedge frame the pseudo force \(ma_0\) acts on the block, away from the face.</p>
<ul><li>Perpendicular to the slope: \(N = m(g\cos\theta + a_0\sin\theta)\).</li>
<li>Along the slope (down positive): \(a_{\rm rel} = g\sin\theta - a_0\cos\theta\).</li>
<li>No sliding when \(a_0 = g\tan\theta\); then \(N = mg/\cos\theta\).</li>
<li>For \(a_0 &gt; g\tan\theta\) the block slides <em>up</em> the slope.</li></ul>'''),
             ],
             formulas=[
                 dict(title='Effective gravity in a horizontally accelerating frame', formula=r'g_{\rm eff}=\sqrt{g^2+a_0^2},\qquad T=m\sqrt{g^2+a_0^2}',
                      symbols='a₀ horizontal acceleration of the frame (m/s²); T tension in a pendulum string at rest relative to the frame (N); m bob mass (kg).'),
                 dict(title='Block on an accelerating smooth wedge', formula=r'a_{\rm rel}=g\sin\theta-a_0\cos\theta,\qquad N=m(g\cos\theta+a_0\sin\theta)',
                      symbols='θ wedge angle; a₀ wedge acceleration (m/s²) with the sloping face moving into the block; a_rel block’s acceleration down the slope relative to the wedge; N normal force (N).'),
             ],
             figure=dict(svg=FIG_WEDGE,
                         caption=r'In the frame of a wedge accelerating to the left, the block feels mg, N and a pseudo force \(ma_0\) to the right. The three balance when \(a_0 = g\tan\theta\).'),
             traps=[r'The pseudo force points opposite to the frame’s acceleration, not opposite to its velocity. A braking car (accelerating backward) gives a forward pseudo force, which is why passengers lurch forward.',
                    r'A pseudo force has no reaction partner. Do not look for “the body that exerts it”.'],
             exam=r'''<ul><li>“A pendulum hangs at angle θ in an accelerating car / train. Find the acceleration or the tension.”</li>
<li>“With what acceleration must a smooth wedge move so that a block on it stays at rest?” (g tan θ)</li>
<li>“A block lies on the smooth floor of an accelerating truck. Describe its motion relative to the truck and the ground.”</li>
<li>“Angle of the water surface in an accelerating tank.”</li>
<li>Statement questions comparing inertial and non-inertial frames.</li></ul>''',
             examples=[
                 dict(tag='Two frames', q=r'A 2 kg box rests on the smooth floor of a truck. The truck accelerates forward at 3 m/s². Describe the box’s motion from the ground and from the truck.',
                      steps=[r'Ground frame: the only forces are mg and N, both vertical. Net horizontal force is zero, so the box stays at rest relative to the ground.',
                             r'Truck frame: add a pseudo force \(ma_0 = 6\) N backward. The box accelerates backward at 3 m/s² relative to the truck.',
                             r'The two views agree: the truck moves forward under a box that stays put.'],
                      answer=r'At rest relative to the ground; 3 m/s² backward relative to the truck'),
                 dict(tag='Numerical', q=r'A 2 kg block sits on the smooth face of a 37° wedge. The wedge is accelerated so that the block stays at rest on it. Find the wedge’s acceleration and the normal force (g = 10 m/s², tan 37° = 0.75).',
                      steps=[r'Required acceleration: \(a_0 = g\tan37^\circ = 7.5\) m/s².',
                             r'Ground frame check: horizontal \(N\sin37^\circ = ma_0 = 15\) N, vertical \(N\cos37^\circ = mg = 20\) N.',
                             r'Both give N = 25 N, which equals \(mg/\cos37^\circ\), more than the weight.'],
                      answer=r'7.5 m/s²; N = 25 N'),
                 dict(tag='Assertion–Reason', q=r'Assertion (A): The water surface in a tank on a truck accelerating forward slopes down toward the front.<br>Reason (R): In the truck frame, the effective gravity is tilted backward, and a liquid surface settles perpendicular to the effective gravity.',
                      steps=[r'In the truck frame each water element feels mg down and \(ma_0\) backward.',
                             r'Their sum points down and backward, at \(\tan\theta = a_0/g\) from the vertical.',
                             r'The surface is perpendicular to this, so it rises at the back and falls at the front. A and R are true, and R explains A.'],
                      answer=r'Both true; R correctly explains A'),
             ],
             practice=[
                 dict(q=r'A pendulum hanging in a train that accelerates on a straight level track makes 45° with the vertical. The train’s acceleration is (g = 10 m/s²)',
                      options=['5 m/s²', r'\(10\sqrt2\) m/s²', '10 m/s²', r'\(5\sqrt2\) m/s²'], answer=2, type='numerical',
                      explanation=r'\(\tan45^\circ = a_0/g = 1\), so \(a_0 = 10\) m/s². \(10\sqrt2\) is \(g_{\rm eff}\), the size of the effective gravity, not the train’s acceleration.'),
                 dict(q=r'A 0.4 kg bob hangs from the roof of a car accelerating at 5 m/s². The tension in the string is (g = 10 m/s²)',
                      options=['4 N', r'\(2\sqrt5\) N', '6 N', '2 N'], answer=1, type='numerical',
                      explanation=r'\(T = m\sqrt{g^2 + a_0^2} = 0.4\sqrt{125} = 2\sqrt5 \approx 4.47\) N. 4 N ignores the horizontal acceleration; 6 N adds g and \(a_0\) as numbers.'),
                 dict(q=r'Which statement about a pseudo force is correct?',
                      options=['It acts in the direction of the frame’s acceleration', 'It must be included in ground-frame equations', 'It has an equal and opposite reaction on another body', 'It has no reaction partner because no body exerts it'], answer=3, type='concept',
                      explanation=r'A pseudo force is a bookkeeping term for an accelerating frame. No body exerts it, so the third law gives it no partner. It points opposite to the frame’s acceleration and must be left out in the ground frame.'),
                 dict(q=r'Statement I: Seen from the ground, a block on the smooth floor of a truck accelerating forward stays at rest.<br>Statement II: Seen from the truck, the same block accelerates backward, which is explained by a pseudo force.',
                      options=ST_OPTS, answer=0, type='statement',
                      explanation=r'With no horizontal real force, the block keeps its state of rest in the ground frame. In the truck frame it slides backward at \(a_0\), and the pseudo force \(-ma_0\) accounts for that. Both statements are true descriptions of one motion.'),
             ],
         )),
]
