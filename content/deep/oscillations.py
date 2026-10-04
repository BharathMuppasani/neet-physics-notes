"""Deepening layer for the Oscillations chapter (see docs/deepening-schema.md)."""
import math

R = str

AR_OPTS = ['Both A and R are true, and R correctly explains A',
           'Both A and R are true, but R does not explain A',
           'A is true, but R is false',
           'A is false, but R is true']
ST_OPTS = ['Both Statement I and Statement II are true',
           'Statement I is true, but Statement II is false',
           'Statement I is false, but Statement II is true',
           'Both Statement I and Statement II are false']

AX = 'stroke:var(--ink-2);stroke-width:1.4;fill:none'
TX = 'font-size:12px;fill:var(--ink)'
TM = 'font-size:11px;fill:var(--muted)'


def _pts(f, a, b, sx, sy, n=80):
    out = []
    for i in range(n + 1):
        x = a + (b - a) * i / n
        out.append(f'{sx(x):.1f},{sy(f(x)):.1f}')
    return ' '.join(out)


def _arrow_defs(mid):
    return (f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" markerUnits="userSpaceOnUse" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--ink-2)"/></marker></defs>')


def _spring(x1, x2, y, coils=7, amp=7):
    """Horizontal zigzag spring from x1 to x2 at height y."""
    lead = 8
    pts = [f'{x1:.1f},{y:.1f}', f'{x1 + lead:.1f},{y:.1f}']
    span = (x2 - x1 - 2 * lead) / (2 * coils)
    for i in range(2 * coils):
        xx = x1 + lead + span * (i + 0.5)
        pts.append(f'{xx:.1f},{y + (amp if i % 2 == 0 else -amp):.1f}')
    pts += [f'{x2 - lead:.1f},{y:.1f}', f'{x2:.1f},{y:.1f}']
    return f'<polyline points="{" ".join(pts)}" style="fill:none;stroke:var(--ink-2);stroke-width:1.5"/>'


# ---------- Figure: reference circle ----------
def _fig_reference_circle():
    cx, cy, r = 110, 110, 70
    th = math.radians(50)
    px, py = cx + r * math.cos(th), cy - r * math.sin(th)
    return ('<svg viewBox="0 0 360 220" role="img" aria-label="Reference circle: SHM as the projection of uniform circular motion">'
            + _arrow_defs('rc-a') +
            f'<circle cx="{cx}" cy="{cy}" r="{r}" style="fill:var(--indigo-soft);stroke:var(--indigo);stroke-width:1.6"/>'
            f'<line x1="20" y1="{cy}" x2="215" y2="{cy}" style="{AX}" marker-end="url(#rc-a)"/>'
            f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" style="stroke:var(--ink-2);stroke-width:1.6"/>'
            f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px:.1f}" y2="{cy}" style="stroke:var(--coral);stroke-width:1.2;stroke-dasharray:4 3"/>'
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" style="fill:var(--indigo)"/>'
            f'<circle cx="{px:.1f}" cy="{cy}" r="5" style="fill:var(--coral)"/>'
            f'<path d="M{cx + 24},{cy} A24,24 0 0 0 {cx + 24 * math.cos(th):.1f},{cy - 24 * math.sin(th):.1f}" style="fill:none;stroke:var(--ink-2)"/>'
            f'<text x="{cx + 28}" y="{cy - 6}" style="{TX}">θ</text>'
            f'<text x="{px + 8:.1f}" y="{py - 6:.1f}" style="{TX}">P</text>'
            f'<text x="{px - 4:.1f}" y="{cy + 18}" style="font-size:12px;fill:var(--coral)">N</text>'
            f'<text x="{cx - 4}" y="{cy + 18}" style="{TM}">O</text>'
            f'<text x="{cx + r - 6}" y="{cy + 34}" style="{TM}">+A</text>'
            f'<text x="{cx - r - 10}" y="{cy + 34}" style="{TM}">−A</text>'
            f'<text x="{cx + 8}" y="{cy - 36}" style="{TM}">A</text>'
            f'<text x="225" y="70" style="{TX}">P moves round the</text>'
            f'<text x="225" y="86" style="{TX}">circle at steady ω.</text>'
            f'<text x="225" y="112" style="font-size:12px;fill:var(--coral)">Its shadow N on the</text>'
            f'<text x="225" y="128" style="font-size:12px;fill:var(--coral)">diameter does SHM:</text>'
            f'<text x="225" y="148" style="font-size:12px;fill:var(--coral)">x = A cos θ,</text>'
            f'<text x="225" y="164" style="font-size:12px;fill:var(--coral)">θ = ωt + φ</text>'
            '</svg>')


# ---------- Figure: x, v, a against time ----------
def _fig_xva():
    sx = lambda t: 60 + 270 * t          # t in periods, 0..1
    rows = [('x', 45, lambda t: math.cos(2 * math.pi * t), 'var(--teal)', 'x = A cos ωt', 200),
            ('v', 115, lambda t: -math.sin(2 * math.pi * t), 'var(--indigo)', 'v = −Aω sin ωt', 75),
            ('a', 185, lambda t: -math.cos(2 * math.pi * t), 'var(--coral)', 'a = −Aω² cos ωt', 75)]
    out = ['<svg viewBox="0 0 360 225" role="img" aria-label="Displacement, velocity and acceleration against time in SHM">']
    for name, y0, f, col, lab, lx in rows:
        sy = lambda v, y0=y0: y0 - 24 * v
        out.append(f'<line x1="60" y1="{y0}" x2="340" y2="{y0}" style="stroke:var(--line-2);stroke-width:1"/>')
        out.append(f'<line x1="60" y1="{y0 - 30}" x2="60" y2="{y0 + 30}" style="stroke:var(--ink-2);stroke-width:1.2"/>')
        out.append(f'<polyline points="{_pts(f, 0, 1, sx, sy)}" style="fill:none;stroke:{col};stroke-width:2.2"/>')
        out.append(f'<text x="48" y="{y0 + 4}" text-anchor="end" style="font-size:13px;fill:var(--ink)">{name}</text>')
        out.append(f'<text x="{lx}" y="{y0 - 26}" style="font-size:11px;fill:{col}">{lab}</text>')
    for t, lab in [(0.25, 'T/4'), (0.5, 'T/2'), (0.75, '3T/4'), (1.0, 'T')]:
        out.append(f'<line x1="{sx(t):.1f}" y1="15" x2="{sx(t):.1f}" y2="210" style="stroke:var(--line-2);stroke-dasharray:3 3"/>')
        out.append(f'<text x="{sx(t):.1f}" y="222" text-anchor="middle" style="{TM}">{lab}</text>')
    out.append('</svg>')
    return ''.join(out)


# ---------- Figure: energy against displacement ----------
def _fig_energy():
    sx = lambda x: 180 + 120 * x          # x in units of A
    sy = lambda e: 180 - 140 * e          # e in units of E
    U = _pts(lambda x: x * x, -1, 1, sx, sy)
    K = _pts(lambda x: 1 - x * x, -1, 1, sx, sy)
    xe = 1 / math.sqrt(2)
    return ('<svg viewBox="0 0 360 215" role="img" aria-label="Potential and kinetic energy against displacement in SHM">'
            + _arrow_defs('en-a') +
            f'<line x1="40" y1="180" x2="335" y2="180" style="{AX}" marker-end="url(#en-a)"/>'
            f'<line x1="180" y1="190" x2="180" y2="18" style="{AX}" marker-end="url(#en-a)"/>'
            f'<line x1="60" y1="40" x2="300" y2="40" style="stroke:var(--ink);stroke-width:1.6;stroke-dasharray:6 3"/>'
            f'<polyline points="{U}" style="fill:none;stroke:var(--coral);stroke-width:2.4"/>'
            f'<polyline points="{K}" style="fill:none;stroke:var(--teal);stroke-width:2.4"/>'
            f'<line x1="{sx(xe):.1f}" y1="110" x2="{sx(xe):.1f}" y2="180" style="stroke:var(--line-2);stroke-dasharray:3 3"/>'
            f'<line x1="{sx(-xe):.1f}" y1="110" x2="{sx(-xe):.1f}" y2="180" style="stroke:var(--line-2);stroke-dasharray:3 3"/>'
            f'<text x="60" y="196" text-anchor="middle" style="{TM}">−A</text>'
            f'<text x="300" y="196" text-anchor="middle" style="{TM}">+A</text>'
            f'<text x="{sx(xe):.1f}" y="196" text-anchor="middle" style="{TM}">A/√2</text>'
            f'<text x="{sx(-xe):.1f}" y="196" text-anchor="middle" style="{TM}">−A/√2</text>'
            f'<text x="334" y="196" text-anchor="end" style="{TX}">x</text>'
            f'<text x="306" y="44" style="{TX}">E</text>'
            f'<text x="296" y="70" style="font-size:12px;fill:var(--coral)">U = ½kx²</text>'
            f'<text x="190" y="32" style="font-size:12px;fill:var(--teal)">K = ½k(A² − x²)</text>'
            f'<text x="186" y="175" style="{TM}">0</text>'
            '</svg>')


# ---------- Figure: spring combinations ----------
def _fig_springs():
    wall = 'fill:var(--surface-2);stroke:var(--ink-2);stroke-width:1'
    blk = 'fill:var(--water-soft);stroke:var(--water);stroke-width:1.4'
    return ('<svg viewBox="0 0 360 250" role="img" aria-label="Springs in series, in parallel and on both sides of a block">'
            # series
            f'<text x="10" y="18" style="{TX}">Series: same force, extensions add</text>'
            f'<rect x="10" y="28" width="10" height="40" style="{wall}"/>'
            + _spring(20, 110, 48) + _spring(110, 200, 48) +
            f'<circle cx="110" cy="48" r="2.5" style="fill:var(--ink-2)"/>'
            f'<rect x="200" y="33" width="34" height="30" style="{blk}"/>'
            f'<text x="65" y="74" text-anchor="middle" style="{TM}">k₁</text><text x="155" y="74" text-anchor="middle" style="{TM}">k₂</text>'
            f'<text x="250" y="53" style="font-size:12px;fill:var(--coral)">1/k = 1/k₁ + 1/k₂</text>'
            # parallel
            f'<text x="10" y="100" style="{TX}">Parallel: same extension, forces add</text>'
            f'<rect x="10" y="112" width="10" height="56" style="{wall}"/>'
            + _spring(20, 160, 124, 8, 6) + _spring(20, 160, 156, 8, 6) +
            f'<line x1="160" y1="118" x2="160" y2="162" style="stroke:var(--ink-2);stroke-width:2"/>'
            f'<line x1="160" y1="140" x2="180" y2="140" style="stroke:var(--ink-2);stroke-width:1.5"/>'
            f'<rect x="180" y="125" width="34" height="30" style="{blk}"/>'
            f'<text x="90" y="114" text-anchor="middle" style="{TM}">k₁</text><text x="90" y="176" text-anchor="middle" style="{TM}">k₂</text>'
            f'<text x="250" y="140" style="font-size:12px;fill:var(--coral)">k = k₁ + k₂</text>'
            # block between two walls
            f'<text x="10" y="192" style="{TX}">Block between two walls: also parallel</text>'
            f'<rect x="10" y="200" width="10" height="40" style="{wall}"/>'
            + _spring(20, 120, 220) +
            f'<rect x="120" y="205" width="34" height="30" style="{blk}"/>'
            + _spring(154, 254, 220) +
            f'<rect x="254" y="200" width="10" height="40" style="{wall}"/>'
            f'<text x="70" y="246" text-anchor="middle" style="{TM}">k₁</text><text x="204" y="246" text-anchor="middle" style="{TM}">k₂</text>'
            f'<text x="272" y="225" style="font-size:12px;fill:var(--coral)">k = k₁ + k₂</text>'
            '</svg>')


# ---------- Figure: simple pendulum forces ----------
def _fig_pendulum():
    px, py, L = 160, 20, 140
    th = math.radians(25)
    bx, by = px + L * math.sin(th), py + L * math.cos(th)
    # tangential component of mg: magnitude mg sin(theta), direction toward equilibrium along the arc
    tx, ty = -math.cos(th), math.sin(th)
    return ('<svg viewBox="0 0 360 230" role="img" aria-label="Simple pendulum with weight resolved into radial and tangential parts">'
            + _arrow_defs('pd-a') +
            f'<line x1="110" y1="{py}" x2="210" y2="{py}" style="stroke:var(--ink-2);stroke-width:3"/>'
            f'<line x1="{px}" y1="{py}" x2="{px}" y2="{py + L + 20}" style="stroke:var(--line-2);stroke-dasharray:4 3"/>'
            f'<line x1="{px}" y1="{py}" x2="{bx:.1f}" y2="{by:.1f}" style="stroke:var(--ink);stroke-width:1.4"/>'
            f'<path d="M{px},{py + 40} A40,40 0 0 0 {px + 40 * math.sin(th):.1f},{py + 40 * math.cos(th):.1f}" style="fill:none;stroke:var(--ink-2)"/>'
            f'<text x="{px + 6}" y="{py + 56}" style="{TX}">θ</text>'
            f'<text x="{px + 44}" y="{py + 76}" style="{TX}">ℓ</text>'
            f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{bx:.1f}" y2="{by + 55:.1f}" style="stroke:var(--coral);stroke-width:2" marker-end="url(#pd-a)"/>'
            f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{bx + 45 * tx:.1f}" y2="{by + 45 * ty:.1f}" style="stroke:var(--teal);stroke-width:2" marker-end="url(#pd-a)"/>'
            f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{bx - 32 * math.sin(th):.1f}" y2="{by - 32 * math.cos(th):.1f}" style="stroke:var(--indigo);stroke-width:2" marker-end="url(#pd-a)"/>'
            f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="9" style="fill:var(--amber-soft);stroke:var(--amber);stroke-width:1.6"/>'
            f'<text x="{bx + 6:.1f}" y="{by + 66:.1f}" style="font-size:12px;fill:var(--coral)">mg</text>'
            f'<text x="{bx - 120:.1f}" y="{by + 36:.1f}" style="font-size:12px;fill:var(--teal)">mg sin θ (restoring)</text>'
            f'<text x="{bx - 28:.1f}" y="{by - 12:.1f}" style="font-size:12px;fill:var(--indigo)">T</text>'
            f'<text x="240" y="60" style="{TX}">Along the arc:</text>'
            f'<text x="240" y="78" style="{TX}">F = −mg sin θ</text>'
            f'<text x="240" y="96" style="{TX}">≈ −mg θ (small θ)</text>'
            f'<text x="240" y="114" style="{TX}">= −(mg/ℓ) s</text>'
            '</svg>')


# ---------- Figure: resonance curves ----------
def _fig_resonance():
    sx = lambda w: 50 + 140 * w           # w = drive / natural frequency, 0..2.1
    def amp(w, g):
        return 1 / math.sqrt((1 - w * w) ** 2 + (g * w) ** 2)
    sy = lambda a: 175 - 22 * a
    low = _pts(lambda w: amp(w, 0.15), 0, 2.05, sx, sy, 200)
    high = _pts(lambda w: amp(w, 0.6), 0, 2.05, sx, sy, 120)
    return ('<svg viewBox="0 0 360 210" role="img" aria-label="Amplitude of forced oscillation against driving frequency for light and heavy damping">'
            + _arrow_defs('rs-a') +
            f'<line x1="50" y1="175" x2="345" y2="175" style="{AX}" marker-end="url(#rs-a)"/>'
            f'<line x1="50" y1="175" x2="50" y2="10" style="{AX}" marker-end="url(#rs-a)"/>'
            f'<polyline points="{low}" style="fill:none;stroke:var(--coral);stroke-width:2.2"/>'
            f'<polyline points="{high}" style="fill:none;stroke:var(--teal);stroke-width:2.2"/>'
            f'<line x1="190" y1="175" x2="190" y2="20" style="stroke:var(--line-2);stroke-dasharray:4 3"/>'
            f'<text x="190" y="190" text-anchor="middle" style="{TX}">ω₀</text>'
            f'<text x="340" y="200" text-anchor="end" style="{TX}">driving frequency ω_d</text>'
            f'<text x="58" y="18" style="{TX}">amplitude</text>'
            f'<text x="214" y="50" style="font-size:12px;fill:var(--coral)">light damping:</text>'
            f'<text x="214" y="64" style="font-size:12px;fill:var(--coral)">tall, sharp peak</text>'
            f'<text x="62" y="110" style="font-size:12px;fill:var(--teal)">heavy damping:</text>'
            f'<text x="62" y="124" style="font-size:12px;fill:var(--teal)">low, broad peak</text>'
            '</svg>')


# ---------- Figure: tunnel through the Earth ----------
def _fig_tunnel():
    return ('<svg viewBox="0 0 340 210" role="img" aria-label="Straight tunnel through the Earth with the restoring force on a body">'
            + _arrow_defs('tn-a') +
            '<circle cx="120" cy="105" r="90" style="fill:var(--water-soft);stroke:var(--water);stroke-width:1.6"/>'
            '<line x1="30" y1="105" x2="210" y2="105" style="stroke:var(--ink-2);stroke-width:5;stroke-opacity:0.25"/>'
            '<line x1="30" y1="105" x2="210" y2="105" style="stroke:var(--ink-2);stroke-width:1"/>'
            '<circle cx="120" cy="105" r="3" style="fill:var(--ink)"/>'
            '<circle cx="175" cy="105" r="6" style="fill:var(--amber)"/>'
            '<line x1="175" y1="105" x2="140" y2="105" style="stroke:var(--coral);stroke-width:2.2" marker-end="url(#tn-a)"/>'
            '<line x1="120" y1="112" x2="175" y2="112" style="stroke:var(--ink-2);stroke-width:1"/>'
            '<text x="147" y="126" text-anchor="middle" style="font-size:12px;fill:var(--ink)">x</text>'
            '<text x="112" y="98" style="font-size:11px;fill:var(--muted)">O</text>'
            '<text x="128" y="88" style="font-size:12px;fill:var(--coral)">F = −(mg/R)x</text>'
            '<text x="226" y="160" style="font-size:11px;fill:var(--muted)">(tunnel along a diameter)</text>'
            '<text x="226" y="70" style="font-size:12px;fill:var(--ink)">Inside a uniform</text>'
            '<text x="226" y="86" style="font-size:12px;fill:var(--ink)">Earth, g ∝ x, so</text>'
            '<text x="226" y="102" style="font-size:12px;fill:var(--ink)">the body does SHM:</text>'
            '<text x="226" y="122" style="font-size:12px;fill:var(--coral)">T = 2π√(R/g)</text>'
            '<text x="226" y="138" style="font-size:12px;fill:var(--coral)">≈ 84 min</text>'
            '</svg>')


DEEP = {
# =====================================================================
'oscillations-periodic': dict(
    level='basic',
    notes=[
        ('Periodic, oscillatory and simple harmonic', r'''<p>These are three nested ideas.</p>
<ul>
<li><strong>Periodic motion</strong> repeats after a fixed time \(T\). The Earth going round the Sun is periodic.</li>
<li><strong>Oscillatory motion</strong> is periodic motion back and forth about an equilibrium point. A swing is oscillatory; the Earth’s orbit is periodic but not oscillatory.</li>
<li><strong>Simple harmonic motion</strong> is the special oscillation where the restoring force is proportional to displacement: \(F = -kx\). Its displacement is a single sine or cosine of time.</li>
</ul>
<p>Every SHM is oscillatory, and every oscillation is periodic. The reverse is not true.</p>'''),
        ('Testing a function for SHM', r'''<p>A function of time is SHM if it can be written as \(A\sin(\omega t+\phi)\) plus, at most, a constant (which only shifts the mean position).</p>
<ul>
<li>\(\sin\omega t + \cos\omega t = \sqrt2\sin(\omega t + \pi/4)\): SHM with amplitude \(\sqrt2\).</li>
<li>\(\sin^2\omega t = \tfrac12 - \tfrac12\cos2\omega t\): SHM about the mean \(\tfrac12\), with angular frequency \(2\omega\) and period \(\pi/\omega\).</li>
<li>\(\sin\omega t + \sin2\omega t\): periodic (period \(2\pi/\omega\)) but not SHM, because two frequencies are mixed.</li>
<li>\(\sin^3\omega t\): periodic but not SHM (it contains \(\sin3\omega t\)).</li>
<li>\(e^{-\omega t}\) or \(\log\omega t\): not periodic at all.</li>
</ul>
<p>For a force law, check that \(F\) is proportional to \(-x\). A force like \(F = -kx^3\) is restoring and gives periodic motion, but it is not SHM, and its period depends on the amplitude.</p>'''),
        ('SHM from a potential energy curve', r'''<p>If a body has potential energy \(U(x)\), equilibrium is where \(dU/dx = 0\), and it is stable at a minimum. Near that minimum, \(U\) looks like a parabola, so the force is approximately \(F = -k(x-x_0)\) with \(k = d^2U/dx^2\) at \(x_0\). This is why almost any stable system makes SHM for small displacements. Then \(\omega = \sqrt{k/m}\).</p>'''),
    ],
    formulas=[
        dict(title='Effective spring constant from U(x)', formula=r'k=\left.\frac{d^2U}{dx^2}\right|_{x_0},\qquad \omega=\sqrt{\frac km}',
             symbols='k effective stiffness (N/m); U potential energy (J); x position (m); x₀ stable equilibrium where dU/dx = 0 and U is a minimum; ω angular frequency (rad/s); m mass (kg). Valid for small oscillations about x₀.'),
        dict(title='Period of sin² and cos² motion', formula=r'\sin^2\omega t=\tfrac12-\tfrac12\cos2\omega t\quad\Rightarrow\quad T=\frac{\pi}{\omega}',
             symbols='ω angular frequency of the original sine (rad/s); t time (s); T period of the squared function (s). The motion is SHM about the mean value ½, at angular frequency 2ω.'),
    ],
    traps=[r'Every periodic motion is not oscillatory, and every oscillation is not SHM. Uniform circular motion is periodic but not to-and-fro.',
           r'\(\sin^2\omega t\) has period \(\pi/\omega\), not \(2\pi/\omega\). Squaring doubles the frequency.'],
    exam=r'''<ul>
<li>“Which of the following functions represents SHM / periodic but not SHM / non-periodic motion?”</li>
<li>“The potential energy of a particle is U = ax² + bx + c. Find the angular frequency of small oscillations.”</li>
<li>“A particle moves with F = −kx³. Is the motion SHM?”</li>
<li>Graph: “Which force–displacement graph represents SHM?” (straight line through origin, negative slope)</li>
<li>Statement-type questions on periodic versus oscillatory motion.</li>
</ul>''',
    examples=[
        dict(tag='Conceptual', q=r'Classify each function as SHM, periodic but not SHM, or non-periodic: (a) \(\sin\omega t - \cos\omega t\) (b) \(\sin^2\omega t\) (c) \(\sin\omega t + \sin2\omega t\) (d) \(e^{-\omega t}\).',
             steps=[r'(a) \(\sin\omega t - \cos\omega t = \sqrt2\sin(\omega t - \pi/4)\): a single sinusoid, so SHM with amplitude \(\sqrt2\) and period \(2\pi/\omega\).',
                    r'(b) \(\sin^2\omega t = \tfrac12 - \tfrac12\cos2\omega t\): SHM about the mean \(\tfrac12\), amplitude \(\tfrac12\), period \(\pi/\omega\).',
                    r'(c) Two different frequencies cannot combine into one sinusoid. The sum repeats every \(2\pi/\omega\), so it is periodic but not SHM.',
                    r'(d) An exponential decay never repeats, so it is non-periodic.'],
             answer=r'(a) SHM, (b) SHM, (c) periodic but not SHM, (d) non-periodic.'),
        dict(tag='Numerical', q=r'A 0.1 kg particle has potential energy \(U = 5x^2 - 20x + 30\) J (x in metres). Find its equilibrium position and the angular frequency of small oscillations.',
             steps=[r'Equilibrium: \(dU/dx = 10x - 20 = 0\), so \(x_0 = 2\) m.',
                    r'Stiffness: \(k = d^2U/dx^2 = 10\) N/m, which is positive, so the equilibrium is stable.',
                    r'\(\omega = \sqrt{k/m} = \sqrt{10/0.1} = 10\) rad/s.',
                    r'The linear term only shifts the mean position; the constant 30 J plays no role.'],
             answer=r'\(x_0 = 2\) m; \(\omega = 10\) rad/s.'),
    ],
    practice=[
        dict(q=r'Which of these displacements represents simple harmonic motion?',
             options=[r'\(x = \sin\omega t + \sin2\omega t\)', r'\(x = \sin^3\omega t\)', r'\(x = e^{-\omega t}\sin\omega t\)', r'\(x = 3\sin\omega t + 4\cos\omega t\)'], answer=3, type='concept',
             explanation=r'\(3\sin\omega t + 4\cos\omega t = 5\sin(\omega t + \phi)\), a single sinusoid. The first mixes two frequencies, the second contains a \(\sin3\omega t\) term, and the third has a shrinking amplitude, so it is damped, not SHM.'),
        dict(q=r'A 0.25 kg body moves under a force \(F = -16x\) (SI units). Its period is',
             options=[r'\(\pi/4\) s', r'\(\pi/2\) s', r'\(\pi/8\) s', r'\(4\pi\) s'], answer=0, type='numerical',
             explanation=r'\(\omega = \sqrt{16/0.25} = 8\) rad/s, so \(T = 2\pi/8 = \pi/4\) s (about 0.79 s). \(\pi/8\) forgets the \(2\pi\) in the period, and \(\pi/2\) uses \(\omega = 4\), which would be \(\sqrt{16}\) without dividing by the mass.'),
        dict(q=r'Statement I: The motion of the Earth around the Sun is periodic but not oscillatory.<br>Statement II: In SHM the restoring force is always directed toward the mean position.',
             options=ST_OPTS, answer=0, type='statement',
             explanation=r'Both are true. The orbit repeats every year (periodic) but is not a to-and-fro motion about an equilibrium point. In SHM, \(F = -kx\) always points toward \(x = 0\).'),
        dict(q=r'For a body in SHM, a graph of restoring force \(F\) (vertical) against displacement \(x\) (horizontal) is',
             options=['A parabola opening downward', 'A straight line through the origin with negative slope', 'A straight line through the origin with positive slope', 'A horizontal line'], answer=1, type='graph',
             explanation=r'\(F = -kx\) is linear with slope \(-k\). A positive slope would push the body away from equilibrium (unstable). A parabola is the shape of the potential energy graph, not the force graph.'),
    ],
),
# =====================================================================
'oscillations-phase': dict(
    level='core',
    notes=[
        ('The reference circle', r'''<p>Imagine a point P moving round a circle of radius \(A\) at steady angular speed \(\omega\). Drop a perpendicular from P to a diameter. The foot of that perpendicular, N, moves back and forth along the diameter in SHM: \(x = A\cos(\omega t+\phi)\).</p>
<p>The angle \(\omega t+\phi\) is the phase. One full turn is \(2\pi\) and takes one period. The circle makes time questions easy: the time to go from one position to another is the angle turned by P divided by \(\omega\).</p>'''),
        ('Finding amplitude and phase from the start', r'''<p>If at \(t = 0\) the body is at \(x_0\) with velocity \(v_0\), then for \(x = A\cos(\omega t+\phi)\):</p>
<ol>
<li>\(x_0 = A\cos\phi\) and \(v_0 = -A\omega\sin\phi\).</li>
<li>Square and add: \(A = \sqrt{x_0^2 + (v_0/\omega)^2}\).</li>
<li>Divide: \(\tan\phi = -v_0/(\omega x_0)\). Check the signs of \(x_0\) and \(v_0\) to pick the right quadrant.</li>
</ol>
<p>The same position with opposite velocity gives a different phase. At \(x = A/2\) moving toward the mean, \(\phi = \pi/3\); moving away from the mean, \(\phi = -\pi/3\).</p>'''),
        ('Standard time intervals', r'''<p>Measured from the mean position, the phase angle \(\theta\) satisfies \(x = A\sin\theta\). The time taken is \(t = \theta/\omega = \theta T/2\pi\).</p>
<ul>
<li>Mean to \(A/2\): \(\theta = \pi/6\), \(t = T/12\).</li>
<li>Mean to \(A/\sqrt2\): \(\theta = \pi/4\), \(t = T/8\).</li>
<li>Mean to \(\sqrt3A/2\): \(\theta = \pi/3\), \(t = T/6\).</li>
<li>\(A/2\) to \(A\): \(T/4 - T/12 = T/6\).</li>
</ul>
<p>The body takes less time to cover the half of the path near the mean, because it moves fastest there.</p>'''),
    ],
    formulas=[
        dict(title='Amplitude and phase from initial conditions', formula=r'A=\sqrt{x_0^2+\frac{v_0^2}{\omega^2}},\qquad \tan\phi=-\frac{v_0}{\omega x_0}',
             symbols='A amplitude (m); x₀ initial displacement (m); v₀ initial velocity (m/s); ω angular frequency (rad/s); φ initial phase of x = A cos(ωt + φ) (rad). Choose the quadrant of φ from the signs of x₀ and v₀.'),
        dict(title='Time from the mean position', formula=r't=\frac{T}{2\pi}\sin^{-1}\!\left(\frac xA\right)',
             symbols='t shortest time to go from x = 0 to x (s); T period (s); x displacement (m); A amplitude (m). Gives T/12 for A/2, T/8 for A/√2 and T/6 for √3A/2.'),
    ],
    figure=dict(svg=_fig_reference_circle(),
                caption=r'The reference circle. P goes round at constant ω; its projection N on the diameter moves in SHM with x = A cos(ωt + φ). The angle of P is the phase.'),
    traps=[r'Going from the mean to \(A/2\) takes \(T/12\), not \(T/8\). The second half of the path (\(A/2\) to \(A\)) takes twice as long, \(T/6\), because the body is slower there.',
           r'The phase depends on both position and direction of motion. \(x = A/2\) moving inward and \(x = A/2\) moving outward are different phases.'],
    exam=r'''<ul>
<li>“Find the minimum time to go from the mean position to half the amplitude (or from A to A/2).”</li>
<li>“At t = 0, x = 3 cm and v = 8 cm/s with ω = 2 rad/s. Find the amplitude.”</li>
<li>“Write the equation of SHM from this x–t graph.” (find A, T and the starting phase)</li>
<li>“Find the phase difference between x₁ = A sin ωt and x₂ = A cos ωt.”</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A body in SHM has a period of 2.4 s. Find the shortest time it takes to go from the mean position to half the amplitude, and from half the amplitude to the extreme.',
             steps=[r'From the mean: \(x = A\sin\theta\). At \(x = A/2\), \(\theta = \pi/6\).',
                    r'\(t_1 = (\pi/6)/(2\pi)\times T = T/12 = 0.2\) s.',
                    r'Mean to extreme takes \(T/4 = 0.6\) s, so \(A/2\) to \(A\) takes \(0.6 - 0.2 = 0.4\) s.',
                    r'Equal distances, unequal times: the body is slower near the extreme.'],
             answer=r'0.2 s and 0.4 s'),
        dict(tag='Numerical', q=r'At \(t = 0\), a particle in SHM with \(\omega = 2\) rad/s is at \(x = 3\) cm moving with velocity \(+8\) cm/s. Find the amplitude.',
             steps=[r'\(A = \sqrt{x_0^2 + (v_0/\omega)^2}\).',
                    r'\(v_0/\omega = 8/2 = 4\) cm.',
                    r'\(A = \sqrt{9+16} = 5\) cm.'],
             answer=r'5 cm'),
        dict(tag='Graph', q=r'An x–t graph of SHM starts at \(x = -A\) at \(t = 0\), rises to \(+A\) at \(t = 0.5\) s and returns to \(-A\) at \(t = 1\) s. Write the equation.',
             steps=[r'One full cycle takes 1 s, so \(T = 1\) s and \(\omega = 2\pi\) rad/s.',
                    r'At \(t = 0\) the body is at the negative extreme, at rest.',
                    r'\(x = A\cos(\omega t + \phi)\) with \(\cos\phi = -1\) gives \(\phi = \pi\).',
                    r'So \(x = A\cos(2\pi t + \pi) = -A\cos2\pi t\).'],
             answer=r'\(x = -A\cos(2\pi t)\), i.e. phase constant π in the cosine form.'),
    ],
    practice=[
        dict(q=r'A particle in SHM has a period of 3 s. The minimum time it takes to go from an extreme position to half the amplitude is',
             options=['0.25 s', '0.375 s', '0.75 s', '0.5 s'], answer=3, type='numerical',
             explanation=r'From the extreme, \(x = A\cos\omega t\); \(x = A/2\) when \(\omega t = \pi/3\), giving \(t = T/6 = 0.5\) s. 0.25 s is \(T/12\), the time from the mean to \(A/2\). 0.75 s is \(T/4\), the time to reach the mean.'),
        dict(q=r'An x–t graph of SHM passes through \(x = 0\) at \(t = 0\) and then goes negative. Its equation is',
             options=[r'\(x = A\sin\omega t\)', r'\(x = -A\sin\omega t\)', r'\(x = A\cos\omega t\)', r'\(x = -A\cos\omega t\)'], answer=1, type='graph',
             explanation=r'At \(t = 0\), \(x = 0\) rules out both cosine forms (they start at an extreme). \(A\sin\omega t\) rises first; \(-A\sin\omega t\) falls first, matching the graph.'),
        dict(q=r'Assertion (A): The SHMs \(x_1 = A\sin\omega t\) and \(x_2 = A\cos\omega t\) differ in phase by \(\pi/2\).<br>Reason (R): \(\cos\omega t = \sin(\omega t + \pi/2)\).',
             options=AR_OPTS, answer=0, type='ar',
             explanation=r'Both are true and R gives the reason directly: writing both as sines shows the phase constants 0 and \(\pi/2\). The second SHM leads by a quarter cycle.'),
        dict(q=r'At \(t = 0\), a particle in SHM (\(\omega = 4\) rad/s) is at \(x = 0.3\) m with speed 1.6 m/s. Its amplitude is',
             options=['0.3 m', '0.4 m', '0.7 m', '0.5 m'], answer=3, type='numerical',
             explanation=r'\(A = \sqrt{0.3^2 + (1.6/4)^2} = \sqrt{0.09+0.16} = 0.5\) m. 0.7 m adds 0.3 and 0.4 directly. 0.3 m wrongly assumes the body starts at the extreme, but it is moving.'),
    ],
),
# =====================================================================
'oscillations-velocity': dict(
    level='core',
    notes=[
        ('Derivation and the maximum values', r'''<p>Start from \(x = A\sin(\omega t+\phi)\).</p>
<ol>
<li>\(v = dx/dt = A\omega\cos(\omega t+\phi)\). Using \(\cos^2 = 1-\sin^2\), \(v = \pm\omega\sqrt{A^2-x^2}\).</li>
<li>\(a = dv/dt = -A\omega^2\sin(\omega t+\phi) = -\omega^2x\).</li>
<li>Maximum speed \(v_{\max} = A\omega\) at the mean. Maximum acceleration \(a_{\max} = A\omega^2\) at the extremes.</li>
<li>Two handy combinations: \(a_{\max}/v_{\max} = \omega\) and \(v_{\max}^2/a_{\max} = A\).</li>
</ol>'''),
        ('Reading the graphs', r'''<ul>
<li><strong>Against time:</strong> \(x\), \(v\) and \(a\) are all sinusoids of the same period. \(v\) leads \(x\) by \(\pi/2\); \(a\) leads \(v\) by \(\pi/2\), so \(a\) is opposite in phase to \(x\).</li>
<li><strong>\(v\) against \(x\):</strong> an ellipse, \(\dfrac{x^2}{A^2}+\dfrac{v^2}{A^2\omega^2} = 1\). Its horizontal semi-axis is \(A\) and its vertical semi-axis is \(A\omega\). It becomes a circle if the axes are scaled so that \(A\omega\) and \(A\) look equal, or if \(\omega = 1\).</li>
<li><strong>\(a\) against \(x\):</strong> a straight line through the origin with slope \(-\omega^2\).</li>
<li><strong>\(v^2\) against \(x^2\):</strong> a straight line with slope \(-\omega^2\) and intercept \(A^2\omega^2\).</li>
</ul>'''),
        ('Two positions, two speeds', r'''<p>If the speeds \(v_1\) and \(v_2\) at displacements \(x_1\) and \(x_2\) are known, write \(v_1^2 = \omega^2(A^2-x_1^2)\) and \(v_2^2 = \omega^2(A^2-x_2^2)\). Subtract to remove \(A\):</p>
<p>\(\omega^2 = \dfrac{v_1^2 - v_2^2}{x_2^2 - x_1^2}\), then \(A^2 = \dfrac{v_1^2x_2^2 - v_2^2x_1^2}{v_1^2 - v_2^2}\).</p>'''),
    ],
    formulas=[
        dict(title='Maximum speed and acceleration', formula=r'v_{\max}=A\omega,\quad a_{\max}=A\omega^2,\quad \frac{a_{\max}}{v_{\max}}=\omega',
             symbols='v_max speed at the mean position (m/s); a_max acceleration magnitude at the extremes (m/s²); A amplitude (m); ω angular frequency (rad/s).'),
        dict(title='Velocity–displacement ellipse', formula=r'\frac{x^2}{A^2}+\frac{v^2}{A^2\omega^2}=1',
             symbols='x displacement (m); v velocity (m/s); A amplitude (m); ω angular frequency (rad/s). The v–x graph is an ellipse with semi-axes A and Aω.'),
        dict(title='ω from two positions', formula=r'\omega^2=\frac{v_1^2-v_2^2}{x_2^2-x_1^2}',
             symbols='v₁, v₂ speeds (m/s) at displacements x₁, x₂ (m) of the same SHM; ω angular frequency (rad/s).'),
    ],
    figure=dict(svg=_fig_xva(),
                caption=r'Displacement, velocity and acceleration over one period, starting at x = +A. Velocity is zero where x is extreme; acceleration is always opposite to x.'),
    traps=[r'Maximum speed and maximum acceleration never occur together. Speed peaks at the mean, where acceleration is zero; acceleration peaks at the extremes, where speed is zero.',
           r'Velocity leads displacement by \(\pi/2\), not lags. Acceleration is in antiphase (\(\pi\)) with displacement, not in phase.'],
    exam=r'''<ul>
<li>“Maximum velocity is 0.5 m/s and maximum acceleration is 2.5 m/s². Find the amplitude and period.”</li>
<li>“Speeds at x = 3 cm and 4 cm are 8 cm/s and 6 cm/s. Find A and T.”</li>
<li>Graph shape: “v against x is a(n) ___”, “a against x is a(n) ___”. (ellipse; straight line, negative slope)</li>
<li>Phase relations: “Phase difference between velocity and acceleration / displacement and acceleration.”</li>
<li>“At what displacement is the speed half its maximum value?” (√3A/2)</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A particle in SHM has speed 8 cm/s at \(x = 3\) cm and 6 cm/s at \(x = 4\) cm. Find the amplitude and the period.',
             steps=[r'\(\omega^2 = (v_1^2 - v_2^2)/(x_2^2 - x_1^2) = (64 - 36)/(16 - 9) = 4\), so \(\omega = 2\) rad/s.',
                    r'From \(v_1^2 = \omega^2(A^2 - x_1^2)\): \(64 = 4(A^2 - 9)\), so \(A^2 = 25\), \(A = 5\) cm.',
                    r'\(T = 2\pi/\omega = \pi\) s, about 3.14 s.'],
             answer=r'A = 5 cm, T = π s'),
        dict(tag='Graph', q=r'The velocity–displacement graph of an SHM is an ellipse crossing the x-axis at ±0.2 m and the v-axis at ±2 m/s. Find \(\omega\) and the maximum acceleration.',
             steps=[r'The x-intercepts give the amplitude: \(A = 0.2\) m.',
                    r'The v-intercepts give the maximum speed: \(A\omega = 2\) m/s.',
                    r'\(\omega = 2/0.2 = 10\) rad/s.',
                    r'\(a_{\max} = A\omega^2 = 0.2\times100 = 20\) m/s².'],
             answer=r'ω = 10 rad/s; a_max = 20 m/s²'),
        dict(tag='Ratio', q=r'At what displacement is the speed of a particle in SHM half its maximum speed?',
             steps=[r'\(v = \omega\sqrt{A^2 - x^2}\) and \(v_{\max} = A\omega\).',
                    r'Set \(\omega\sqrt{A^2 - x^2} = A\omega/2\): \(A^2 - x^2 = A^2/4\).',
                    r'\(x^2 = 3A^2/4\), so \(x = \pm\sqrt3A/2\approx\pm0.87A\).',
                    r'Half the speed occurs much nearer the extreme than the middle.'],
             answer=r'\(x = \pm\dfrac{\sqrt3}{2}A\)'),
    ],
    practice=[
        dict(q=r'A body in SHM has maximum speed 0.5 m/s and maximum acceleration 2.5 m/s². Its amplitude is',
             options=['0.1 m', '0.2 m', '5 m', '1.25 m'], answer=0, type='numerical',
             explanation=r'\(\omega = a_{\max}/v_{\max} = 5\) rad/s and \(A = v_{\max}/\omega = 0.1\) m (or \(v_{\max}^2/a_{\max} = 0.25/2.5\)). 5 m is \(\omega\) mistaken for \(A\). 1.25 m multiplies the two maxima.'),
        dict(q=r'The graph of velocity (vertical) against displacement (horizontal) for a particle in SHM is',
             options=['A straight line with negative slope', 'A parabola', 'An ellipse', 'A hyperbola'], answer=2, type='graph',
             explanation=r'\(x^2/A^2 + v^2/(A\omega)^2 = 1\) is an ellipse. The straight line with negative slope is the acceleration–displacement graph. A parabola is the energy–displacement graph.'),
        dict(q=r'Match each pair (List I) with its phase difference (List II).<br>List I: (P) velocity and displacement (Q) acceleration and displacement (R) acceleration and velocity<br>List II: (1) \(\pi\) (2) \(\pi/2\) (3) 0',
             options=['P-2, Q-1, R-2', 'P-1, Q-2, R-2', 'P-2, Q-3, R-1', 'P-3, Q-1, R-2'], answer=0, type='match',
             explanation=r'Velocity leads displacement by \(\pi/2\); acceleration leads velocity by another \(\pi/2\), so acceleration and displacement differ by \(\pi\). Option 3 wrongly puts acceleration in phase with displacement, forgetting the minus sign in \(a = -\omega^2x\).'),
        dict(q=r'For a particle in SHM, a graph of \(v^2\) (vertical) against \(x^2\) (horizontal) is a straight line. Its slope equals',
             options=[r'\(\omega^2\)', r'\(-\omega^2\)', r'\(A^2\omega^2\)', r'\(-A^2\)'], answer=1, type='graph',
             explanation=r'\(v^2 = \omega^2A^2 - \omega^2x^2\): slope \(-\omega^2\), intercept \(A^2\omega^2\). \(A^2\omega^2\) is the intercept, not the slope. A positive slope would mean speed grows away from the mean, which is wrong.'),
    ],
),
# =====================================================================
'oscillations-energy': dict(
    level='core',
    notes=[
        ('Derivation: the energy expressions', r'''<ol>
<li>Potential energy: work done against \(F = -kx\) to stretch from 0 to \(x\) is \(U = \int_0^x kx\,dx = \tfrac12kx^2\).</li>
<li>Kinetic energy: \(K = \tfrac12mv^2 = \tfrac12m\omega^2(A^2 - x^2) = \tfrac12k(A^2 - x^2)\), using \(k = m\omega^2\).</li>
<li>Total: \(E = K + U = \tfrac12kA^2 = \tfrac12m\omega^2A^2 = 2\pi^2mf^2A^2\). It does not depend on \(x\) or \(t\).</li>
</ol>
<p>At fixed mass, \(E\propto A^2\) and \(E\propto f^2\). Doubling both amplitude and frequency multiplies the energy by 16.</p>'''),
        ('How the energies change with time', r'''<p>With \(x = A\sin\omega t\): \(U = E\sin^2\omega t\) and \(K = E\cos^2\omega t\). Since \(\sin^2\omega t = \tfrac12(1-\cos2\omega t)\), each energy oscillates at angular frequency \(2\omega\), that is, at twice the frequency of the motion. Its period is \(T/2\).</p>
<p>Averaged over a cycle, \(\langle K\rangle = \langle U\rangle = E/2\). Energy never goes negative, so it peaks twice per cycle: \(U\) at both extremes, \(K\) at each pass through the mean.</p>'''),
        ('Useful fractions', r'''<ul>
<li>At \(x = A/2\): \(U = E/4\), \(K = 3E/4\).</li>
<li>\(K = U\) at \(x = A/\sqrt2\).</li>
<li>\(K = nU\) at \(x = A/\sqrt{n+1}\). For \(K = 3U\), \(x = A/2\); for \(K = 8U\), \(x = A/3\).</li>
</ul>'''),
    ],
    formulas=[
        dict(title='Total energy in terms of frequency', formula=r'E=\tfrac12m\omega^2A^2=2\pi^2mf^2A^2',
             symbols='E total mechanical energy (J); m mass (kg); ω angular frequency (rad/s); f frequency (Hz); A amplitude (m). Ideal undamped SHM.'),
        dict(title='Position where K = nU', formula=r'x=\frac{A}{\sqrt{n+1}}',
             symbols='x displacement magnitude (m); A amplitude (m); n ratio of kinetic to potential energy (pure number). n = 1 gives A/√2.'),
        dict(title='Frequency of energy oscillation', formula=r'f_{K}=f_{U}=2f',
             symbols='f_K, f_U frequencies at which kinetic and potential energy vary (Hz); f frequency of the SHM itself (Hz).'),
    ],
    figure=dict(svg=_fig_energy(),
                caption=r'Potential energy U (coral) and kinetic energy K (teal) against displacement. They always add to the constant E (dashed). The curves cross at x = ±A/√2, where K = U = E/2.'),
    traps=[r'Kinetic and potential energy vary with frequency \(2f\), not \(f\). If the body oscillates at 4 Hz, its kinetic energy peaks 8 times per second.',
           r'At half the amplitude, potential energy is \(E/4\), not \(E/2\). Energies go as \(x^2\).'],
    exam=r'''<ul>
<li>“At what displacement is KE equal to PE / three times PE?”</li>
<li>“What fraction of the total energy is kinetic at x = A/2?”</li>
<li>“If the frequency of SHM is f, the frequency of oscillation of its KE is ___.”</li>
<li>Graph: “Which graph shows PE (or KE) against displacement / time?”</li>
<li>“The amplitude is doubled and the frequency halved. How does the energy change?”</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A 0.5 kg body oscillates with amplitude 0.1 m and \(\omega = 10\) rad/s. Find its total energy, and its potential and kinetic energies at \(x = 0.05\) m.',
             steps=[r'\(E = \tfrac12m\omega^2A^2 = \tfrac12\times0.5\times100\times0.01 = 0.25\) J.',
                    r'\(U = \tfrac12m\omega^2x^2 = \tfrac12\times0.5\times100\times0.0025 = 0.0625\) J.',
                    r'\(K = E - U = 0.1875\) J.',
                    r'Check: at \(x = A/2\), \(U = E/4\) and \(K = 3E/4\).'],
             answer=r'E = 0.25 J; U = 0.0625 J; K = 0.1875 J'),
        dict(tag='Graph', q=r'A body does SHM with period 2 s. Sketch in words the graph of its potential energy against time, and give the period of that graph.',
             steps=[r'\(U = \tfrac12kx^2 = E\sin^2\omega t\) if it starts at the mean.',
                    r'\(\sin^2\omega t\) is never negative. It rises from 0 to \(E\) and back to 0 twice per cycle of motion.',
                    r'So the graph is a row of identical humps between 0 and \(E\), never dipping below the time axis.',
                    r'Its period is \(T/2 = 1\) s.'],
             answer=r'Humps between 0 and E repeating every 1 s (half the SHM period).'),
        dict(tag='Ratio', q=r'The amplitude of an SHM is doubled and its frequency is halved, with the same mass. How does the total energy change?',
             steps=[r'\(E = 2\pi^2mf^2A^2\), so \(E\propto f^2A^2\).',
                    r'New factor: \((1/2)^2\times2^2 = 1\).',
                    r'The energy is unchanged.'],
             answer=r'No change'),
    ],
    practice=[
        dict(q=r'In SHM, the kinetic energy is 8 times the potential energy at a displacement of',
             options=[r'\(A/8\)', r'\(A/\sqrt8\)', r'\(A/2\)', r'\(A/3\)'], answer=3, type='numerical',
             explanation=r'\(K = nU\) at \(x = A/\sqrt{n+1} = A/\sqrt9 = A/3\). Check: \(U = E/9\), \(K = 8E/9\). \(A/\sqrt8\) uses \(n\) instead of \(n+1\). \(A/2\) is where \(K = 3U\).'),
        dict(q=r'A particle performs SHM with frequency 4 Hz. Its kinetic energy varies periodically with frequency',
             options=['2 Hz', '4 Hz', '8 Hz', '16 Hz'], answer=2, type='numerical',
             explanation=r'\(K = E\cos^2\omega t = \tfrac E2(1+\cos2\omega t)\), which oscillates at \(2f = 8\) Hz. 4 Hz is the frequency of the displacement itself. 16 Hz would be four times, with no basis.'),
        dict(q=r'Which of these statements about ideal SHM are correct?<br>(a) Total energy is proportional to the square of amplitude.<br>(b) The average kinetic energy over a cycle equals the average potential energy.<br>(c) Potential energy is maximum at the mean position.<br>(d) Kinetic and potential energies are equal at \(x = A/\sqrt2\).',
             options=['(a) and (c) only', '(a), (b) and (d) only', '(b) and (c) only', 'All four'], answer=1, type='multi',
             explanation=r'(a) \(E = \tfrac12kA^2\). (b) Both averages are \(E/2\). (d) \(\tfrac12kx^2 = \tfrac14kA^2\) gives \(x = A/\sqrt2\). (c) is false: at the mean, \(U = 0\) and \(K\) is maximum, so any option including (c) is wrong.'),
        dict(q=r'A 1 kg body oscillates with amplitude 0.2 m and period \(\pi\) s. Its total energy is',
             options=['0.04 J', '0.08 J', '0.16 J', '0.4 J'], answer=1, type='numerical',
             explanation=r'\(\omega = 2\pi/T = 2\) rad/s. \(E = \tfrac12m\omega^2A^2 = \tfrac12\times1\times4\times0.04 = 0.08\) J. 0.16 J drops the ½. 0.04 J uses \(\omega = \sqrt2\) by mistake.'),
    ],
),
# =====================================================================
'oscillations-springs': dict(
    level='exam',
    notes=[
        ('Derivation: series and parallel', r'''<p><strong>Parallel.</strong> Both springs stretch by the same \(x\). Their forces add: \(F = k_1x + k_2x\), so \(k_p = k_1 + k_2\). Stiffer.</p>
<p><strong>Series.</strong> The same force \(F\) passes through both springs. Their extensions add: \(x = F/k_1 + F/k_2\), so \(1/k_s = 1/k_1 + 1/k_2\), or \(k_s = k_1k_2/(k_1+k_2)\). Softer than either spring.</p>
<p>A block tied between two springs fixed to opposite walls is a parallel arrangement: displacing the block stretches one spring and compresses the other by the same \(x\), and both forces point back toward equilibrium.</p>
<p>Period rules: in series \(T_s^2 = T_1^2 + T_2^2\); in parallel \(1/T_p^2 = 1/T_1^2 + 1/T_2^2\), where \(T_1, T_2\) are the periods of the same mass on each spring alone.</p>'''),
        ('Cutting a spring', r'''<p>For a given material and coil, \(k\propto1/L\): a shorter spring stretches less under the same force. So:</p>
<ul>
<li>Cut into \(n\) equal parts, each piece has stiffness \(nk\).</li>
<li>Cut in the ratio \(l_1 : l_2\), the pieces have \(k_1 = k(l_1+l_2)/l_1\) and \(k_2 = k(l_1+l_2)/l_2\).</li>
</ul>
<p>Joining the pieces back in series restores \(k\); joining them in parallel gives a much stiffer system.</p>'''),
        ('Vertical springs, two bodies and spring mass', r'''<ul>
<li><strong>Vertical spring.</strong> At equilibrium \(kx_0 = mg\), so \(m/k = x_0/g\) and \(T = 2\pi\sqrt{x_0/g}\). The static extension alone gives the period. On a smooth incline, the period is the same \(2\pi\sqrt{m/k}\).</li>
<li><strong>Two bodies joined by a spring</strong> on a smooth floor oscillate about their centre of mass with \(T = 2\pi\sqrt{\mu/k}\), where \(\mu = m_1m_2/(m_1+m_2)\) is the reduced mass.</li>
<li><strong>Mass of the spring.</strong> A spring of mass \(m_s\) adds about \(m_s/3\) to the moving mass: \(T = 2\pi\sqrt{(m+m_s/3)/k}\).</li>
</ul>'''),
    ],
    formulas=[
        dict(title='Pieces of a cut spring', formula=r'k_i=k\,\frac{L}{l_i}',
             symbols='k_i stiffness of a piece (N/m); k original stiffness (N/m); L original length (m); l_i length of that piece (m). Assumes uniform coiling.'),
        dict(title='Two bodies on a spring', formula=r'T=2\pi\sqrt{\frac{\mu}{k}},\qquad \mu=\frac{m_1m_2}{m_1+m_2}',
             symbols='T period (s); μ reduced mass (kg); m₁, m₂ the two masses (kg); k spring constant (N/m). Smooth floor, no external horizontal force.'),
        dict(title='Period from static extension', formula=r'T=2\pi\sqrt{\frac{x_0}{g}}',
             symbols='T period (s); x₀ extension at equilibrium when the mass hangs at rest (m); g gravity (m/s²). Light, ideal spring.'),
    ],
    figure=dict(svg=_fig_springs(),
                caption=r'Series springs share one force, so their extensions add and the system is softer. Parallel springs share one extension, so their forces add. A block between two walls stretches one spring and compresses the other by the same amount, which is also parallel.'),
    traps=[r'A block between two springs attached to opposite walls is a parallel arrangement (\(k_1 + k_2\)), even though the springs look like they are “in a line”.',
           r'Cutting a spring in half doubles its spring constant. It does not halve it.'],
    exam=r'''<ul>
<li>“A spring of constant k is cut into n equal parts. Find the constant of each / of two pieces in parallel.”</li>
<li>“Periods on two springs are T₁ and T₂. Find the period with both springs in series / parallel.”</li>
<li>“A mass hangs on a spring and stretches it by 2.5 cm. Find the period.”</li>
<li>“Two masses joined by a spring on a smooth table. Find the period.”</li>
<li>“Does the period change if the spring-mass system is taken to the Moon / placed on an incline?” (no)</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A mass hung from a spring stretches it by 2.5 cm at equilibrium. Find the period of vertical oscillation. Take \(g = 10\) m/s².',
             steps=[r'At equilibrium \(kx_0 = mg\), so \(m/k = x_0/g\).',
                    r'\(T = 2\pi\sqrt{x_0/g} = 2\pi\sqrt{0.025/10} = 2\pi\times0.05\).',
                    r'\(T = 0.1\pi\approx0.314\) s.'],
             answer=r'About 0.31 s'),
        dict(tag='Numerical', q=r'A spring of constant \(k\) is cut into two pieces with lengths in the ratio 1 : 2. The pieces are joined in parallel. Find the effective constant.',
             steps=[r'Original length \(L = 3l\). Pieces are \(l\) and \(2l\).',
                    r'\(k_1 = k(3l/l) = 3k\) and \(k_2 = k(3l/2l) = 1.5k\).',
                    r'Parallel: \(k_{\rm eff} = 3k + 1.5k = 4.5k\).',
                    r'Check: in series they give \(3k\times1.5k/(4.5k) = k\), the original spring.'],
             answer=r'\(4.5k\)'),
        dict(tag='Ratio', q=r'A mass oscillates with period 3 s on spring A and 4 s on spring B. Find the period when the same mass hangs from A and B joined in series.',
             steps=[r'\(T\propto1/\sqrt k\), so \(1/k\propto T^2\).',
                    r'Series: \(1/k_s = 1/k_A + 1/k_B\), hence \(T_s^2 = T_A^2 + T_B^2\).',
                    r'\(T_s = \sqrt{9+16} = 5\) s.',
                    r'In parallel instead: \(1/T_p^2 = 1/9 + 1/16 = 25/144\), \(T_p = 2.4\) s.'],
             answer=r'5 s (series); 2.4 s if in parallel'),
    ],
    practice=[
        dict(q=r'A spring of constant \(k\) is cut into four equal parts, and two of these parts are joined in parallel to carry a mass. Compared with the period on the original spring, the new period is',
             options=[r'\(1/(2\sqrt2)\) times', r'\(1/2\) times', r'\(1/4\) times', r'\(2\sqrt2\) times'], answer=0, type='numerical',
             explanation=r'Each quarter has \(4k\); two in parallel give \(8k\). \(T\propto1/\sqrt k\), so the period becomes \(1/\sqrt8 = 1/(2\sqrt2)\) times. \(1/2\) treats each piece as \(2k\). \(2\sqrt2\) inverts the dependence.'),
        dict(q=r'Two masses of 2 kg each are joined by a light spring of constant 100 N/m and placed on a smooth floor. The period of their oscillation is',
             options=[r'\(0.4\pi\) s', r'\(0.2\pi\sqrt2\) s', r'\(0.2\pi\) s', r'\(0.1\pi\) s'], answer=2, type='numerical',
             explanation=r'Reduced mass \(\mu = 2\times2/4 = 1\) kg. \(T = 2\pi\sqrt{1/100} = 0.2\pi\approx0.63\) s. \(0.4\pi\) uses the total mass 4 kg; \(0.2\pi\sqrt2\) uses one mass of 2 kg as if the other were fixed.'),
        dict(q=r'A block of mass \(m\) on a smooth floor is attached to two springs, \(k_1\) on its left (fixed to a wall) and \(k_2\) on its right (fixed to another wall). Its period is',
             options=[r'\(2\pi\sqrt{m(k_1+k_2)/(k_1k_2)}\)', r'\(2\pi\sqrt{m/(k_1+k_2)}\)', r'\(2\pi\sqrt{m/(k_1k_2)}\)', r'\(2\pi\sqrt{m/|k_1-k_2|}\)'], answer=1, type='concept',
             explanation=r'Displacing the block by \(x\) stretches one spring and compresses the other by \(x\); both push it back, so the force is \(-(k_1+k_2)x\). The first option is the series result, the classic error for this set-up. The difference \(|k_1 - k_2|\) would mean the springs oppose each other, which they do not.'),
        dict(q=r'Statement I: A spring–mass system has the same period on the Moon as on the Earth.<br>Statement II: The period of a vertical spring–mass system depends on its static extension, which is smaller on the Moon.',
             options=ST_OPTS, answer=0, type='statement',
             explanation=r'Both are true. \(T = 2\pi\sqrt{m/k}\) has no \(g\). On the Moon, \(x_0 = mg/k\) is smaller, but \(T = 2\pi\sqrt{x_0/g}\) also has the smaller \(g\), and the ratio \(x_0/g = m/k\) is unchanged. Statement II does not contradict Statement I.'),
    ],
),
# =====================================================================
'oscillations-pendulum': dict(
    level='exam',
    notes=[
        ('Derivation: period of a simple pendulum', r'''<ol>
<li>Displace the bob by angle \(\theta\). Gravity \(mg\) splits into \(mg\cos\theta\) along the string (balanced with tension plus the centripetal need) and \(mg\sin\theta\) along the arc, toward the lowest point.</li>
<li>Torque about the pivot: \(\tau = -mg\ell\sin\theta\). For small \(\theta\) in radians, \(\sin\theta\approx\theta\), so \(\tau\approx-mg\ell\theta\).</li>
<li>With \(I = m\ell^2\): \(\alpha = \tau/I = -(g/\ell)\theta\). This is SHM with \(\omega^2 = g/\ell\).</li>
<li>\(T = 2\pi\sqrt{\ell/g}\). The bob’s mass cancels. The approximation is good to about 0.5% for amplitudes up to about 15°.</li>
</ol>
<p>A <strong>seconds pendulum</strong> has \(T = 2\) s (one second per swing). Its length is \(g/\pi^2\), about 0.99 m with \(g = 9.8\) m/s².</p>'''),
        ('Effective gravity: the master rule', r'''<p>In a non-inertial frame or with buoyancy, replace \(g\) by the effective \(g_{\rm eff}\) that the bob feels when at rest relative to the support. Then \(T = 2\pi\sqrt{\ell/g_{\rm eff}}\).</p>
<ul>
<li>Lift accelerating up at \(a\): \(g_{\rm eff} = g + a\), period shorter.</li>
<li>Lift accelerating down at \(a\): \(g_{\rm eff} = g - a\), period longer. Free fall: \(g_{\rm eff} = 0\), no oscillation.</li>
<li>Vehicle accelerating horizontally at \(a\): \(g_{\rm eff} = \sqrt{g^2 + a^2}\); the string hangs tilted at \(\tan^{-1}(a/g)\).</li>
<li>Bob of density \(\rho\) swinging in a non-viscous liquid of density \(\sigma\): buoyancy gives \(g_{\rm eff} = g(1 - \sigma/\rho)\).</li>
<li>Inside an orbiting satellite: \(g_{\rm eff} = 0\).</li>
</ul>'''),
        ('Length matters: effective length and very long pendulums', r'''<ul>
<li>\(\ell\) is measured from the pivot to the bob’s centre of mass. A hollow bob filled with water that slowly drains: the centre of mass first drops (period rises), then returns to the centre once empty (period falls back).</li>
<li>Small length changes: \(\Delta T/T = \tfrac12\,\Delta\ell/\ell\). A metal pendulum lengthens when hot, so the clock runs slow in summer.</li>
<li>For a length comparable to the Earth’s radius, \(T = 2\pi\sqrt{\dfrac{1}{g(1/\ell + 1/R)}}\). As \(\ell\to\infty\), \(T\to2\pi\sqrt{R/g}\approx84\) min, the same as a satellite skimming the surface.</li>
</ul>'''),
    ],
    formulas=[
        dict(title='Pendulum in a horizontally accelerating vehicle', formula=r'T=2\pi\sqrt{\frac{\ell}{\sqrt{g^2+a^2}}}',
             symbols='T period (s); ℓ length (m); g gravity (m/s²); a horizontal acceleration of the vehicle (m/s²). Small oscillations about the tilted equilibrium.'),
        dict(title='Bob oscillating in a liquid', formula=r'T=2\pi\sqrt{\frac{\ell}{g(1-\sigma/\rho)}}',
             symbols='T period (s); ℓ length (m); g gravity (m/s²); σ liquid density and ρ bob density (kg/m³), with ρ > σ. Viscous drag neglected.'),
        dict(title='Pendulum of very large length', formula=r'T=2\pi\sqrt{\frac{1}{g\left(\frac1\ell+\frac1R\right)}}\ \xrightarrow{\ \ell\to\infty\ }\ 2\pi\sqrt{\frac Rg}',
             symbols='T period (s); ℓ length (m); R Earth radius (m); g surface gravity (m/s²). Accounts for the changing direction of g along the swing.'),
    ],
    figure=dict(svg=_fig_pendulum(),
                caption=r'Weight mg resolved at angle θ. The part mg sin θ acts along the arc toward the lowest point and is the restoring force. For small θ it is proportional to the arc length s = ℓθ, which gives SHM.'),
    traps=[r'In a horizontally accelerating vehicle, use \(g_{\rm eff} = \sqrt{g^2 + a^2}\), not \(g + a\). The two accelerations are perpendicular.',
           r'Pendulum length runs to the centre of mass of the bob, not to its top or bottom.'],
    exam=r'''<ul>
<li>“A pendulum’s length is increased by 21%. By what percent does the period change?” (10%)</li>
<li>“Period in a lift accelerating up/down at a; in a freely falling lift; in a car accelerating horizontally.”</li>
<li>“A bob of density ρ oscillates in water. Find the new period.”</li>
<li>“A hollow sphere filled with water is used as a bob; water drains out. How does the period change?” (increases, then decreases)</li>
<li>“A pendulum clock is taken up a mountain. Does it gain or lose time?” (loses)</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A simple pendulum hangs in a car accelerating horizontally at 7.5 m/s². By what factor does its period change? Take \(g = 10\) m/s².',
             steps=[r'Effective gravity: \(g_{\rm eff} = \sqrt{10^2 + 7.5^2} = \sqrt{156.25} = 12.5\) m/s².',
                    r'\(T\propto1/\sqrt{g_{\rm eff}}\), so \(T^{\prime}/T = \sqrt{10/12.5} = \sqrt{0.8}\approx0.894\).',
                    r'The period decreases by about 10.6%. Using \(g + a = 17.5\) would overstate the change.'],
             answer=r'About 0.894 times the original'),
        dict(tag='Numerical', q=r'A pendulum bob has density 5 times that of water. Find the ratio of its period when it swings in water to its period in air (neglect drag).',
             steps=[r'Buoyancy reduces the restoring weight: \(g_{\rm eff} = g(1 - \sigma/\rho) = g(1 - 1/5) = 0.8g\).',
                    r'\(T_{\rm water}/T_{\rm air} = \sqrt{g/g_{\rm eff}} = 1/\sqrt{0.8}\approx1.118\).',
                    r'The bob’s inertia is unchanged; only the restoring force falls, so the period grows.'],
             answer=r'About 1.12 (that is, √5/2)'),
        dict(tag='Ratio', q=r'The length of a simple pendulum is increased by 21%. Find the percentage change in its period.',
             steps=[r'\(T\propto\sqrt\ell\), so \(T^{\prime}/T = \sqrt{1.21} = 1.1\).',
                    r'The period increases by 10%.',
                    r'The rule \(\Delta T/T = \tfrac12\Delta\ell/\ell\) would give 10.5%; it is only approximate for a 21% change. The exact ratio gives a clean 10%.'],
             answer=r'An increase of 10%'),
    ],
    practice=[
        dict(q=r'A simple pendulum has period \(T\) in a stationary lift. When the lift accelerates downward at \(g/4\), the period becomes',
             options=[r'\(\dfrac{2T}{\sqrt3}\)', r'\(\dfrac{\sqrt3T}{2}\)', r'\(\dfrac{2T}{\sqrt5}\)', r'\(\dfrac{4T}{3}\)'], answer=0, type='numerical',
             explanation=r'\(g_{\rm eff} = g - g/4 = 3g/4\), so \(T^{\prime} = T\sqrt{4/3} = 2T/\sqrt3\approx1.15T\). \(\sqrt3T/2\) inverts the ratio (that would be a shorter period). \(2T/\sqrt5\) uses \(g + g/4\), the upward case.'),
        dict(q=r'The length of a simple pendulum is decreased by 19%. Its period',
             options=['Decreases by 19%', 'Decreases by 9.5%', 'Decreases by 10%', 'Increases by 10%'], answer=2, type='numerical',
             explanation=r'\(T^{\prime}/T = \sqrt{0.81} = 0.9\), a 10% decrease. 9.5% comes from the small-change rule \(\tfrac12\times19\%\), which is not exact for so large a change. 19% ignores the square root.'),
        dict(q=r'A hollow metal sphere filled with water is the bob of a pendulum. Water slowly drains out through a small hole at the bottom. The period of oscillation',
             options=['Keeps increasing', 'Keeps decreasing', 'Stays constant', 'First increases, then decreases to its original value'], answer=3, type='concept',
             explanation=r'As water drains, the centre of mass of bob plus water moves down, lengthening the effective pendulum, so \(T\) rises. When nearly empty, the centre of mass returns to the sphere’s centre and \(T\) returns to the original value. The mass itself does not matter, which rules out reasoning based on weight.'),
        dict(q=r'Assertion (A): A pendulum clock taken to a mountain top loses time.<br>Reason (R): The value of \(g\) is smaller at a height, so the period of the pendulum is larger.',
             options=AR_OPTS, answer=0, type='ar',
             explanation=r'Both are true and R explains A. A longer period means fewer swings per real hour, and the clock counts swings, so it shows less time than has passed. A spring-driven watch, by contrast, would not be affected.'),
    ],
),
# =====================================================================
'oscillations-resonance': dict(
    level='core',
    notes=[
        ('Damped oscillations', r'''<p>With a resistive force \(-bv\), the solution for light damping is</p>
<p>\(x = A_0e^{-bt/2m}\cos(\omega' t + \phi)\), with \(\omega' = \sqrt{\dfrac km - \dfrac{b^2}{4m^2}}\).</p>
<ul>
<li>The amplitude decays exponentially: \(A(t) = A_0e^{-bt/2m}\). It falls by the same fraction in each equal time interval.</li>
<li>Energy goes as amplitude squared: \(E(t) = E_0e^{-bt/m}\), so energy decays twice as fast (in rate constant).</li>
<li>The time for the amplitude to halve is \(t_{1/2} = 2m\ln2/b\).</li>
<li>Damping slightly lowers the frequency (\(\omega' < \omega_0\)). Very heavy damping stops oscillation altogether.</li>
</ul>'''),
        ('Forced oscillations and resonance', r'''<p>A periodic force \(F_0\cos\omega_dt\) drives the oscillator. After the starting transients die away, it oscillates at the driving frequency \(\omega_d\), with steady amplitude</p>
<p>\(A = \dfrac{F_0/m}{\sqrt{(\omega_0^2 - \omega_d^2)^2 + (b\omega_d/m)^2}}\).</p>
<ul>
<li>If \(\omega_d\) is far from \(\omega_0\), the amplitude is small.</li>
<li>Near \(\omega_d = \omega_0\), the first term vanishes and the amplitude is limited only by damping: \(A\approx F_0/(b\omega_0)\). This is resonance.</li>
<li>Light damping gives a tall, narrow peak; heavy damping gives a low, broad one.</li>
</ul>'''),
        ('Resonance in everyday life', r'''<ul>
<li>Soldiers break step when crossing a bridge so that their marching does not drive the bridge at its natural frequency.</li>
<li>A radio is tuned by changing its circuit’s natural frequency to match the station.</li>
<li>A singer’s note at the natural frequency of a wine glass can make it vibrate strongly enough to crack.</li>
<li>Pushing a swing at the right moment each cycle builds a large amplitude with small pushes.</li>
</ul>'''),
    ],
    formulas=[
        dict(title='Exponential decay of a damped oscillator', formula=r'A(t)=A_0e^{-bt/2m},\qquad E(t)=E_0e^{-bt/m}',
             symbols='A amplitude (m) and E energy (J) at time t (s); A₀, E₀ initial values; b damping constant (kg/s); m mass (kg). Light damping assumed.'),
        dict(title='Amplitude of forced oscillation', formula=r'A=\frac{F_0/m}{\sqrt{(\omega_0^2-\omega_d^2)^2+(b\omega_d/m)^2}}',
             symbols='A steady-state amplitude (m); F₀ driving force amplitude (N); m mass (kg); ω₀ natural and ω_d driving angular frequencies (rad/s); b damping constant (kg/s).'),
    ],
    figure=dict(svg=_fig_resonance(),
                caption=r'Amplitude of a driven oscillator against driving frequency. Light damping gives a tall, narrow peak near the natural frequency ω₀; heavy damping gives a low, broad response.'),
    traps=[r'The energy of a damped oscillator falls faster than its amplitude. If the amplitude halves, the energy falls to a quarter.',
           r'Once steady, a forced oscillator vibrates at the driver’s frequency, not its own natural frequency.'],
    exam=r'''<ul>
<li>“The amplitude falls to 0.9 of its value in 5 oscillations. What is it after 15 oscillations?” (0.9³ = 0.729)</li>
<li>“Amplitude halves in time t. In what time does the energy halve?” (t/2)</li>
<li>“Why do soldiers break step on a bridge?” and other resonance examples.</li>
<li>Graph: “Which curve shows amplitude against driving frequency for heavier damping?”</li>
<li>“A system with natural frequency f₀ is driven at f. At what frequency does it oscillate?” (f)</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'The amplitude of a damped oscillator falls to half its initial value in 10 s. What fractions of the initial amplitude and energy remain after 30 s?',
             steps=[r'Exponential decay: each 10 s multiplies the amplitude by \(\tfrac12\).',
                    r'After 30 s (three halvings): \(A = A_0/8\).',
                    r'Energy \(\propto A^2\): \(E = E_0/64\).'],
             answer=r'Amplitude 1/8; energy 1/64'),
        dict(tag='Numerical', q=r'A 0.2 kg mass on a spring has damping constant \(b = 0.04\) kg/s. How long does its amplitude take to halve?',
             steps=[r'\(A = A_0e^{-bt/2m}\). Set \(A/A_0 = \tfrac12\): \(bt/2m = \ln2\).',
                    r'\(t = 2m\ln2/b = 2\times0.2\times0.693/0.04\).',
                    r'\(t\approx6.9\) s.'],
             answer=r'About 6.9 s'),
        dict(tag='Assertion–reason', q=r'Assertion: Soldiers are asked to break step while crossing a bridge. Reason: The frequency of marching may match the natural frequency of the bridge. Decide whether each is true and whether the reason explains the assertion.',
             steps=[r'The assertion describes a real safety practice: true.',
                    r'Regular footsteps form a periodic driving force. If its frequency is close to a natural frequency of the bridge, resonance builds a large amplitude.',
                    r'So the reason is true and is the correct explanation.'],
             answer=r'Both true; the reason explains the assertion.'),
    ],
    practice=[
        dict(q=r'The amplitude of a damped oscillator becomes 0.9 times its initial value after 5 oscillations. After 15 oscillations it will be',
             options=['0.7 times', '0.81 times', '0.729 times', '0.6 times'], answer=2, type='numerical',
             explanation=r'Exponential decay multiplies by the same factor in each equal interval: \(0.9^3 = 0.729\). Subtracting 0.1 each time (0.7) treats the decay as linear. 0.81 counts only two intervals.'),
        dict(q=r'A body of natural frequency 5 Hz is acted on by a periodic force of frequency 3 Hz. In the steady state, the body oscillates with frequency',
             options=['5 Hz', '3 Hz', '4 Hz', '8 Hz'], answer=1, type='concept',
             explanation=r'Forced oscillations settle at the driving frequency, 3 Hz. Its natural frequency (5 Hz) only affects how large the amplitude is. 4 Hz and 8 Hz (average and sum) have no physical basis here.'),
        dict(q=r'Statement I: Increasing the damping lowers and broadens the resonance peak.<br>Statement II: With zero damping, the ideal steady-state amplitude at exact resonance would be infinite.',
             options=ST_OPTS, answer=0, type='statement',
             explanation=r'Both are true. More damping dissipates more energy each cycle, so the peak is lower and spread out. In the formula, at \(\omega_d = \omega_0\) the denominator is \(b\omega_0/m\); with \(b = 0\) it is zero. Real systems always have some damping or break first.'),
        dict(q=r'The amplitude of a damped oscillator halves in 4 s. The time for its energy to halve is',
             options=['8 s', '4 s', '1 s', '2 s'], answer=3, type='numerical',
             explanation=r'Energy decays with rate constant \(b/m\), twice that of amplitude (\(b/2m\)). So the energy half-life is half the amplitude half-life: 2 s. In 4 s the energy falls to a quarter, not a half. 8 s reverses the relation.'),
    ],
),
# =====================================================================
'oscillations-superposition': dict(
    level='core',
    notes=[
        ('Adding two SHMs along one line', r'''<p>Two SHMs of the same frequency along the same line, \(x_1 = A_1\sin\omega t\) and \(x_2 = A_2\sin(\omega t+\delta)\), add like vectors (phasors) of lengths \(A_1, A_2\) with angle \(\delta\) between them:</p>
<p>\(A = \sqrt{A_1^2 + A_2^2 + 2A_1A_2\cos\delta}\), \(\tan\phi = \dfrac{A_2\sin\delta}{A_1 + A_2\cos\delta}\).</p>
<ul>
<li>\(\delta = 0\): \(A = A_1 + A_2\). \(\delta = \pi\): \(A = |A_1 - A_2|\). \(\delta = \pi/2\): \(A = \sqrt{A_1^2 + A_2^2}\).</li>
<li>Equal amplitudes \(a\) with phase difference \(\delta\): \(A = 2a\cos(\delta/2)\). At \(\delta = 2\pi/3\), \(A = a\).</li>
<li>Different frequencies do not give SHM.</li>
</ul>'''),
        ('Perpendicular SHMs', r'''<p>For \(x = a\sin\omega t\) and \(y = b\sin(\omega t + \delta)\) of the same frequency:</p>
<ul>
<li>\(\delta = 0\) or \(\pi\): a straight line \(y = \pm(b/a)x\). The motion is SHM along a slanted line with amplitude \(\sqrt{a^2+b^2}\).</li>
<li>\(\delta = \pi/2\): an ellipse \(x^2/a^2 + y^2/b^2 = 1\); a circle if \(a = b\) (uniform circular motion).</li>
<li>Other \(\delta\): a tilted ellipse.</li>
</ul>'''),
        ('Derivation: the U-tube', r'''<ol>
<li>Push the liquid down by \(x\) on one side; it rises by \(x\) on the other. The level difference is \(2x\).</li>
<li>The unbalanced pressure \(\rho g(2x)\) acts on the cross-section \(A\): restoring force \(F = -2\rho gAx\).</li>
<li>The whole liquid column moves: mass \(m = \rho AL\), where \(L\) is the total length of liquid.</li>
<li>\(a = F/m = -(2g/L)x\), so \(\omega^2 = 2g/L\) and \(T = 2\pi\sqrt{L/2g}\). Density and area cancel.</li>
<li>If \(h\) is the height of liquid in each arm at rest (with negligible bottom length), \(L = 2h\) and \(T = 2\pi\sqrt{h/g}\).</li>
</ol>
<p>Floating bodies and a tunnel through the Earth are treated in “Other SHM systems”.</p>'''),
    ],
    formulas=[
        dict(title='Resultant phase', formula=r'\tan\phi=\frac{A_2\sin\delta}{A_1+A_2\cos\delta}',
             symbols='φ phase of the resultant relative to the first SHM (rad); A₁, A₂ amplitudes (m); δ phase difference of the second relative to the first (rad). Same frequency and line.'),
        dict(title='Equal amplitudes', formula=r'A=2a\cos\frac{\delta}{2}',
             symbols='A resultant amplitude (m); a each amplitude (m); δ phase difference (rad). Gives 2a at δ = 0, √2 a at δ = π/2, a at δ = 2π/3 and 0 at δ = π.'),
    ],
    traps=[r'Amplitudes add as phasors, not as numbers. Two 4 cm SHMs with a phase difference \(\pi/3\) give \(4\sqrt3\approx6.9\) cm, not 8 cm.',
           r'In the U-tube formula, \(L\) is the total length of the liquid column, not the height in one arm.'],
    exam=r'''<ul>
<li>“Find the amplitude of x = 3 sin ωt + 4 cos ωt” or “of x₁ = A sin ωt and x₂ = A sin(ωt + π/3).”</li>
<li>“Two equal-amplitude SHMs combine to give the same amplitude. Find the phase difference.” (2π/3)</li>
<li>“Perpendicular SHMs x = a sin ωt, y = a cos ωt. What is the path?” (circle)</li>
<li>“Find the period of liquid in a U-tube with total length L.” Ratio questions when L or ρ changes.</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'Find the amplitude of the motion produced by \(x_1 = 4\sin\omega t\) cm and \(x_2 = 4\sin(\omega t + \pi/3)\) cm.',
             steps=[r'\(A = \sqrt{A_1^2 + A_2^2 + 2A_1A_2\cos\delta} = \sqrt{16+16+2\times16\times0.5}\).',
                    r'\(A = \sqrt{48} = 4\sqrt3\approx6.93\) cm.',
                    r'Check with \(A = 2a\cos(\delta/2) = 8\cos30° = 4\sqrt3\) cm.'],
             answer=r'\(4\sqrt3\approx6.93\) cm'),
        dict(tag='Numerical', q=r'A U-tube contains a liquid column of total length 40 cm. Find the period of small oscillations. Take \(g = 10\) m/s².',
             steps=[r'\(T = 2\pi\sqrt{L/2g} = 2\pi\sqrt{0.40/20}\).',
                    r'\(\sqrt{0.02}\approx0.1414\).',
                    r'\(T\approx0.89\) s. Changing the liquid (density) would not change this.'],
             answer=r'About 0.89 s'),
        dict(tag='Conceptual', q=r'A particle moves with \(x = 3\sin\omega t\) and \(y = 3\cos\omega t\). Describe its path and speed.',
             steps=[r'\(x^2 + y^2 = 9(\sin^2\omega t + \cos^2\omega t) = 9\).',
                    r'The path is a circle of radius 3 centred at the origin.',
                    r'Speed: \(\sqrt{\dot x^2 + \dot y^2} = 3\omega\), constant. So it is uniform circular motion, clockwise in the usual axes (at \(t = 0\) it is at (0, 3) moving toward +x).'],
             answer=r'Uniform circular motion, radius 3, speed 3ω.'),
    ],
    practice=[
        dict(q=r'Two SHMs of equal amplitude \(a\) and the same frequency along one line combine to give a resultant of amplitude \(a\). Their phase difference is',
             options=[r'\(\pi/3\)', r'\(\pi/2\)', r'\(2\pi/3\)', r'\(\pi\)'], answer=2, type='numerical',
             explanation=r'\(2a\cos(\delta/2) = a\) gives \(\cos(\delta/2) = 1/2\), \(\delta/2 = \pi/3\), \(\delta = 2\pi/3\). \(\pi/3\) gives \(\sqrt3a\). \(\pi/2\) gives \(\sqrt2a\). \(\pi\) gives zero.'),
        dict(q=r'A particle is acted on simultaneously by \(x = a\sin\omega t\) and \(y = a\sin\omega t\) along perpendicular axes. Its path is',
             options=['A circle', 'An ellipse', 'A straight line at 45° to the x-axis', 'A parabola'], answer=2, type='concept',
             explanation=r'With \(\delta = 0\), \(y = x\) at every instant: a straight line at 45°, along which the particle does SHM of amplitude \(\sqrt2a\). A circle needs \(\delta = \pi/2\); an ellipse needs \(\delta = \pi/2\) with unequal amplitudes or a general phase.'),
        dict(q=r'The liquid in a U-tube oscillates with period \(T\). The tube is replaced by one of double the cross-section, holding liquid of half the density, with the same total liquid length. The new period is',
             options=[r'\(T\)', r'\(2T\)', r'\(T/2\)', r'\(\sqrt2T\)'], answer=0, type='numerical',
             explanation=r'\(T = 2\pi\sqrt{L/2g}\) depends only on the liquid length \(L\). Both force and moving mass are proportional to \(\rho A\), which cancels. The other options try to use area or density.'),
    ],
),
}


NEW_SECTIONS = [
dict(chapter='oscillations', after='oscillations-pendulum', id='oscillations-systems',
     title='Other SHM systems: floating body and tunnel through the Earth',
     intro=r'Push a floating log down into water and let go. It bobs up and down. Drop a stone into an imaginary tunnel drilled straight through the Earth and it would swing from one end to the other and back. Both are SHM, and you can find their periods with one recipe: find the restoring force for a small displacement, show it is \(-kx\), and read off \(\omega = \sqrt{k/m}\).',
     reasoning=r'For a floating body, pushing it down by \(x\) displaces extra liquid, so the buoyant force rises by \(\sigma Agx\) and pushes it back. For the tunnel, the body inside a uniform Earth at distance \(x\) from the centre feels a field \(gx/R\), so the force is \(-(mg/R)x\). In both cases the force is proportional to displacement and opposite to it.',
     formula=r'T_{\rm float}=2\pi\sqrt{\frac{m}{\sigma Ag}}=2\pi\sqrt{\frac hg},\qquad T_{\rm tunnel}=2\pi\sqrt{\frac Rg}',
     symbols='T periods (s); m floating body’s mass (kg); σ liquid density (kg/m³); A cross-sectional area of the body at the waterline (m²); h depth of the body below the surface when floating at rest (m); g gravity (m/s²); R Earth radius (m). Floating body: vertical sides, no drag. Tunnel: uniform Earth, smooth tunnel, no rotation.',
     trap=r'For the floating body, \(h\) is the submerged depth at equilibrium, not the full height of the body.',
     example=r'A wooden cylinder floats upright with 10 cm of its length under water. Find the period of its small vertical oscillations. Take \(g = 10\) m/s².',
     solution=r'\(T = 2\pi\sqrt{h/g} = 2\pi\sqrt{0.10/10} = 2\pi\times0.1\approx0.63\) s.',
     question='The period of a body dropped into a straight smooth tunnel through the centre of the Earth is about',
     options='84 minutes|24 hours|42 minutes|It never returns',
     answer=0,
     explanation=r'\(T = 2\pi\sqrt{R/g} = 2\pi\sqrt{6.4\times10^6/10}\approx5030\) s, about 84 minutes. 42 minutes is the time to reach the far end (half a period).',
     deep=dict(
         level='exam',
         notes=[
             ('Derivation: floating body', r'''<ol>
<li>A body of mass \(m\) with uniform cross-section \(A\) floats at rest with depth \(h\) submerged: \(mg = \sigma Ahg\).</li>
<li>Push it down by an extra \(x\). The buoyant force becomes \(\sigma A(h+x)g\), so the net upward force is \(\sigma Agx\).</li>
<li>Net force \(F = -\sigma Ag\,x\), which is SHM with \(k = \sigma Ag\).</li>
<li>\(T = 2\pi\sqrt{m/(\sigma Ag)}\). Substituting \(m = \sigma Ah\): \(T = 2\pi\sqrt{h/g}\).</li>
</ol>
<p>If the body has height \(L\) and density \(\rho\), then \(h = L\rho/\sigma\) and \(T = 2\pi\sqrt{L\rho/(\sigma g)}\).</p>'''),
             ('Derivation: tunnel through the Earth', r'''<ol>
<li>Inside a uniform Earth, at distance \(r\) from the centre, \(g(r) = gr/R\), directed to the centre.</li>
<li>Along a diametral tunnel, \(r = x\), so \(F = -(mg/R)x\). This is SHM with \(\omega = \sqrt{g/R}\).</li>
<li>\(T = 2\pi\sqrt{R/g}\approx84\) min with \(R = 6.4\times10^6\) m and \(g = 10\) m/s².</li>
<li>Speed at the centre \(= A\omega = R\sqrt{g/R} = \sqrt{gR}\approx8\) km/s, the same as the speed of a satellite skimming the surface.</li>
</ol>
<p>For a straight tunnel along a chord (not through the centre), only the component of gravity along the tunnel acts. It is \(-(mg/R)\,s\), where \(s\) is the distance from the tunnel’s midpoint. So the period is the same 84 minutes for every chord.</p>'''),
             ('The general recipe', r'''<p>To show any system does SHM and find its period:</p>
<ol>
<li>Find the equilibrium position.</li>
<li>Displace by a small \(x\) and write the net restoring force (or torque).</li>
<li>Simplify for small \(x\) to the form \(F = -kx\) (or \(\tau = -C\theta\)).</li>
<li>Write \(T = 2\pi\sqrt{m/k}\) (or \(2\pi\sqrt{I/C}\)), with \(m\) the total moving mass.</li>
</ol>
<p>A small ball rolling without slipping at the bottom of a bowl, a liquid in a U-tube and a pendulum all fit this pattern.</p>'''),
         ],
         formulas=[
             dict(title='Floating body in terms of density', formula=r'T=2\pi\sqrt{\frac{L\rho}{\sigma g}}',
                  symbols='T period (s); L height of the body (m); ρ density of the body (kg/m³); σ density of the liquid (kg/m³), with ρ < σ; g gravity (m/s²). Uniform vertical-sided body floating upright.'),
             dict(title='Speed at the centre of a tunnel', formula=r'v_{\max}=\sqrt{gR}\approx8\ \text{km/s}',
                  symbols='v_max speed when passing the centre (m/s); g surface gravity (m/s²); R Earth radius (m). Body released from rest at the surface, uniform Earth, no friction.'),
         ],
         figure=dict(svg=_fig_tunnel(),
                     caption=r'A body in a tunnel through a uniform Earth. At distance x from the centre, the field is gx/R toward O, so the force is −(mg/R)x. The body moves in SHM with period 2π√(R/g).'),
         traps=[r'The tunnel period does not depend on the length or direction of the tunnel (any straight chord gives 84 minutes). The time to travel through is half the period, about 42 minutes.',
                r'The period of a floating body does not depend on the liquid’s density on its own once \(h\) is fixed. If the body is moved to a denser liquid, \(h\) shrinks and so does the period.'],
         exam=r'''<ul>
<li>“A cylinder of height L and density ρ floats in a liquid of density σ. Find its period.”</li>
<li>“A body is dropped into a tunnel along a diameter / along a chord. Find its period, the time to reach the other end and its speed at the centre.”</li>
<li>Comparisons: “tunnel period equals the period of a satellite near the surface.”</li>
<li>Show-that questions: “Prove that the motion is simple harmonic.”</li>
</ul>''',
         examples=[
             dict(tag='Numerical', q=r'A body is dropped from rest into a smooth tunnel dug along a diameter of the Earth. Find (a) the time to reach the other end and (b) its speed at the centre. Take \(g = 10\) m/s², \(R = 6.4\times10^6\) m.',
                  steps=[r'\(T = 2\pi\sqrt{R/g} = 2\pi\sqrt{6.4\times10^5} = 2\pi\times800\approx5027\) s.',
                         r'(a) Reaching the other end is half an oscillation: \(T/2\approx2513\) s, about 42 minutes.',
                         r'(b) \(v_{\max} = A\omega = R\sqrt{g/R} = \sqrt{gR} = \sqrt{6.4\times10^7} = 8000\) m/s.'],
                  answer=r'(a) about 42 min; (b) 8 km/s'),
             dict(tag='Ratio', q=r'A uniform wooden block floats in water with 60% of its height submerged. It is then floated in a liquid of density 1.2 g/cm³. Find the ratio of its new period of vertical oscillation to its period in water.',
                  steps=[r'\(T = 2\pi\sqrt{h/g}\), where \(h\) is the submerged depth.',
                         r'Floating: \(\rho L = \sigma h\), so \(h\propto1/\sigma\). In water \(h_1 = 0.6L\); in the new liquid \(h_2 = 0.6L/1.2 = 0.5L\).',
                         r'\(T_2/T_1 = \sqrt{h_2/h_1} = \sqrt{0.5/0.6}\approx0.913\).'],
                  answer=r'About 0.91 (that is, √(5/6))'),
         ],
         practice=[
             dict(q=r'A cylinder of height 20 cm and density 0.5 g/cm³ floats upright in water. The period of its small vertical oscillations is (\(g = 10\) m/s²)',
                  options=[r'\(0.2\pi\) s', r'\(0.1\pi\) s', r'\(0.4\pi\) s', r'\(0.2\pi\sqrt2\) s'], answer=0, type='numerical',
                  explanation=r'Submerged depth \(h = 20\times0.5 = 10\) cm. \(T = 2\pi\sqrt{0.1/10} = 0.2\pi\approx0.63\) s. \(0.2\pi\sqrt2\) uses the full height 20 cm instead of the submerged depth.'),
             dict(q=r'A body is released into a smooth straight tunnel along a chord of the Earth (not through the centre). Compared with a tunnel along a diameter, its period is',
                  options=['Longer', 'Shorter', 'The same', 'Undefined, as it does not oscillate'], answer=2, type='concept',
                  explanation=r'Along the chord, the component of the field is \(-(g/R)s\), where \(s\) is the distance from the chord’s midpoint. The constant \(g/R\) is the same, so \(\omega = \sqrt{g/R}\) and the period (84 min) are unchanged. The amplitude and maximum speed are smaller, which is what tempts “shorter”.'),
             dict(q=r'Assertion (A): The time period of a body in a tunnel through the Earth equals that of a satellite orbiting just above the Earth’s surface.<br>Reason (R): Both periods equal \(2\pi\sqrt{R/g}\).',
                  options=AR_OPTS, answer=0, type='ar',
                  explanation=r'Both are true. A near-surface satellite has \(T = 2\pi R/\sqrt{gR} = 2\pi\sqrt{R/g}\). The tunnel motion has \(\omega = \sqrt{g/R}\), the same. In fact the tunnel motion is the projection of the satellite’s circular motion, so R explains A.'),
         ],
     )),
]
