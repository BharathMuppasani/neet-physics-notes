"""Deepening layer for the Waves chapter (see docs/deepening-schema.md)."""
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


def _pts(f, a, b, sx, sy, n=100):
    out = []
    for i in range(n + 1):
        x = a + (b - a) * i / n
        out.append(f'{sx(x):.1f},{sy(f(x)):.1f}')
    return ' '.join(out)


def _arrow_defs(mid, colour='var(--ink-2)'):
    return (f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" markerUnits="userSpaceOnUse" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:{colour}"/></marker></defs>')


# ---------- Figure: snapshot of a travelling wave with particle velocities ----------
def _fig_snapshot():
    sx = lambda x: 30 + 290 * x / 1.5    # x in wavelengths, 0..1.5
    sy = lambda y: 100 - 45 * y
    f = lambda x: math.sin(2 * math.pi * x)
    out = ['<svg viewBox="0 0 360 200" role="img" aria-label="Snapshot of a wave moving to the right with particle velocity arrows">',
           _arrow_defs('sn-a'), _arrow_defs('sn-b', 'var(--coral)'),
           f'<line x1="30" y1="100" x2="330" y2="100" style="stroke:var(--line-2);stroke-width:1"/>',
           f'<polyline points="{_pts(f, 0, 1.5, sx, sy, 150)}" style="fill:none;stroke:var(--teal);stroke-width:2.4"/>']
    # particle velocity v_p = -v dy/dx (wave moving +x)
    for x in [0.0, 0.125, 0.375, 0.5, 0.625, 0.875, 1.0, 1.125, 1.375]:
        slope = 2 * math.pi * math.cos(2 * math.pi * x)
        vp = -slope / (2 * math.pi)            # scaled so the largest arrow is one unit
        if abs(vp) < 0.05:
            continue
        x0, y0 = sx(x), sy(f(x))
        out.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x0:.1f}" y2="{y0 - 30 * vp:.1f}" '
                   f'style="stroke:var(--coral);stroke-width:1.8" marker-end="url(#sn-b)"/>')
    for x in [0.25, 0.75, 1.25]:
        out.append(f'<circle cx="{sx(x):.1f}" cy="{sy(f(x)):.1f}" r="3.5" style="fill:var(--ink)"/>')
    out += [f'<line x1="230" y1="22" x2="300" y2="22" style="stroke:var(--ink-2);stroke-width:2" marker-end="url(#sn-a)"/>',
            f'<text x="226" y="26" text-anchor="end" style="{TX}">wave moves</text>',
            f'<text x="30" y="190" style="font-size:11px;fill:var(--coral)">Arrows: particle velocity. Dots at crests and troughs are momentarily at rest.</text>',
            f'<text x="{sx(0.25):.1f}" y="{sy(1) - 8:.1f}" text-anchor="middle" style="{TM}">crest</text>',
            f'<text x="{sx(0.75):.1f}" y="{sy(-1) + 18:.1f}" text-anchor="middle" style="{TM}">trough</text>',
            '</svg>']
    return ''.join(out)


# ---------- Figure: string modes ----------
def _fig_string_modes():
    out = ['<svg viewBox="0 0 360 245" role="img" aria-label="First three standing-wave modes of a string fixed at both ends">']
    x0, x1 = 40, 250
    L = x1 - x0
    for i, n in enumerate([1, 2, 3]):
        yc = 45 + 75 * i
        up = _pts(lambda x, n=n: math.sin(n * math.pi * x), 0, 1, lambda x: x0 + L * x, lambda y, yc=yc: yc - 22 * y)
        dn = _pts(lambda x, n=n: -math.sin(n * math.pi * x), 0, 1, lambda x: x0 + L * x, lambda y, yc=yc: yc - 22 * y)
        out.append(f'<polyline points="{up}" style="fill:none;stroke:var(--indigo);stroke-width:2"/>')
        out.append(f'<polyline points="{dn}" style="fill:none;stroke:var(--indigo);stroke-width:1.4;stroke-dasharray:4 3"/>')
        out.append(f'<line x1="{x0}" y1="{yc - 26}" x2="{x0}" y2="{yc + 26}" style="stroke:var(--ink-2);stroke-width:3"/>')
        out.append(f'<line x1="{x1}" y1="{yc - 26}" x2="{x1}" y2="{yc + 26}" style="stroke:var(--ink-2);stroke-width:3"/>')
        for k in range(n + 1):
            xn = x0 + L * k / n
            out.append(f'<circle cx="{xn:.1f}" cy="{yc}" r="3" style="fill:var(--coral)"/>')
        for k in range(n):
            xa = x0 + L * (k + 0.5) / n
            out.append(f'<text x="{xa:.1f}" y="{yc - 27}" text-anchor="middle" style="font-size:10px;fill:var(--teal)">A</text>')
        names = {1: 'n = 1: fundamental', 2: 'n = 2: 2nd harmonic', 3: 'n = 3: 3rd harmonic'}
        extra = {1: 'λ = 2L, f₁ = v/2L', 2: 'λ = L, f = 2f₁', 3: 'λ = 2L/3, f = 3f₁'}
        out.append(f'<text x="262" y="{yc - 4}" style="{TX}">{names[n]}</text>')
        out.append(f'<text x="262" y="{yc + 12}" style="{TM}">{extra[n]}</text>')
    out.append(f'<text x="40" y="240" style="font-size:11px;fill:var(--coral)">● nodes (including both fixed ends)</text>')
    out.append(f'<text x="230" y="240" style="font-size:11px;fill:var(--teal)">A antinodes</text>')
    out.append('</svg>')
    return ''.join(out)


# ---------- Figure: closed and open pipes ----------
def _fig_pipes():
    out = ['<svg viewBox="0 0 380 250" role="img" aria-label="Displacement patterns in a pipe closed at one end and a pipe open at both ends">']
    cols = [(20, 'Closed at one end', [(1, 'f₁ = v/4L'), (3, 'f₃ = 3v/4L = 3f₁')], True),
            (210, 'Open at both ends', [(1, 'f₁ = v/2L'), (2, 'f₂ = 2v/2L = 2f₁')], False)]
    W = 150
    for xl, title, rows, closed in cols:
        out.append(f'<text x="{xl}" y="16" style="font-size:12px;fill:var(--ink);font-weight:600">{title}</text>')
        for i, (n, lab) in enumerate(rows):
            yc = 65 + 100 * i
            out.append(f'<rect x="{xl}" y="{yc - 25}" width="{W}" height="50" style="fill:var(--water-soft);stroke:var(--water);stroke-width:1.2"/>')
            if closed:
                out.append(f'<line x1="{xl}" y1="{yc - 25}" x2="{xl}" y2="{yc + 25}" style="stroke:var(--ink);stroke-width:4"/>')
                fn = lambda x, n=n: math.sin(n * math.pi * x / 2)
            else:
                fn = lambda x, n=n: math.cos(n * math.pi * x)
            sxx = lambda x, xl=xl: xl + W * x
            out.append(f'<polyline points="{_pts(fn, 0, 1, sxx, lambda y, yc=yc: yc - 19 * y)}" style="fill:none;stroke:var(--coral);stroke-width:2"/>')
            out.append(f'<polyline points="{_pts(lambda x, fn=fn: -fn(x), 0, 1, sxx, lambda y, yc=yc: yc - 19 * y)}" style="fill:none;stroke:var(--coral);stroke-width:2"/>')
            out.append(f'<text x="{xl + W / 2}" y="{yc + 44}" text-anchor="middle" style="{TX}">{lab}</text>')
    out.append(f'<text x="20" y="245" style="{TM}">Closed end: displacement node. Open end: displacement antinode.</text>')
    out.append('</svg>')
    return ''.join(out)


# ---------- Figure: beats ----------
def _fig_beats():
    f1, f2 = 20.0, 22.0
    sx = lambda t: 30 + 310 * t        # t from 0 to 1 s (2 beats)
    sy = lambda y: 85 - 30 * y
    y = lambda t: math.cos(2 * math.pi * f1 * t) + math.cos(2 * math.pi * f2 * t)
    env = lambda t: 2 * abs(math.cos(math.pi * (f2 - f1) * t))
    return ('<svg viewBox="0 0 360 185" role="img" aria-label="Superposition of two close frequencies showing beats">'
            + _arrow_defs('bt-a') +
            f'<line x1="30" y1="85" x2="345" y2="85" style="stroke:var(--line-2);stroke-width:1"/>'
            f'<polyline points="{_pts(y, 0, 1, sx, sy, 900)}" style="fill:none;stroke:var(--teal);stroke-width:1.3"/>'
            f'<polyline points="{_pts(env, 0, 1, sx, sy, 200)}" style="fill:none;stroke:var(--coral);stroke-width:1.6;stroke-dasharray:5 3"/>'
            f'<polyline points="{_pts(lambda t: -env(t), 0, 1, sx, sy, 200)}" style="fill:none;stroke:var(--coral);stroke-width:1.6;stroke-dasharray:5 3"/>'
            f'<line x1="{sx(0):.1f}" y1="160" x2="{sx(0.5):.1f}" y2="160" style="stroke:var(--ink-2);stroke-width:1.2" marker-start="url(#bt-a)" marker-end="url(#bt-a)"/>'
            f'<text x="{sx(0.25):.1f}" y="176" text-anchor="middle" style="{TX}">one beat: 1/|f₁ − f₂|</text>'
            f'<text x="{sx(0.5):.1f}" y="30" text-anchor="middle" style="{TM}">waxing</text>'
            f'<text x="{sx(0.25):.1f}" y="30" text-anchor="middle" style="{TM}">waning</text>'
            f'<text x="{sx(0.62):.1f}" y="160" style="font-size:11px;fill:var(--coral)">dashed: slowly varying amplitude</text>'
            '</svg>')


# ---------- Figure: Doppler wavefronts ----------
def _fig_doppler():
    v, u = 1.0, 0.5
    xs_now, cy = 200, 95
    out = ['<svg viewBox="0 0 360 200" role="img" aria-label="Wavefronts from a source moving to the right are crowded ahead and spread out behind">',
           _arrow_defs('dp-a')]
    for k, tau in enumerate([4, 3, 2, 1]):
        r = 22 * v * tau
        cx = xs_now - 22 * u * tau
        out.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="{r:.1f}" style="fill:none;stroke:var(--indigo);stroke-width:1.4"/>')
        out.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="2" style="fill:var(--muted)"/>')
    out += [f'<circle cx="{xs_now}" cy="{cy}" r="6" style="fill:var(--amber)"/>',
            f'<line x1="{xs_now + 8}" y1="{cy}" x2="{xs_now + 40}" y2="{cy}" style="stroke:var(--ink-2);stroke-width:2" marker-end="url(#dp-a)"/>',
            f'<text x="{xs_now + 4}" y="{cy - 10}" style="{TX}">S</text>',
            f'<text x="{xs_now + 16}" y="{cy + 18}" style="{TM}">v_s</text>',
            f'<text x="300" y="40" style="font-size:12px;fill:var(--coral)">ahead: shorter λ,</text>',
            f'<text x="300" y="54" style="font-size:12px;fill:var(--coral)">higher f</text>',
            f'<text x="6" y="40" style="font-size:12px;fill:var(--teal)">behind: longer λ,</text>',
            f'<text x="6" y="54" style="font-size:12px;fill:var(--teal)">lower f</text>',
            f'<text x="180" y="192" text-anchor="middle" style="{TM}">Grey dots: where S was when each wavefront left it.</text>',
            '</svg>']
    return ''.join(out)


DEEP = {
# =====================================================================
'waves-travelling': dict(
    level='basic',
    notes=[
        ('Reading a wave equation', r'''<p>Any function of the form \(y = f(x - vt)\) is a wave moving toward \(+x\) with speed \(v\); \(f(x + vt)\) moves toward \(-x\). The shape stays the same and slides along. For example, \(y = \dfrac{1}{1+(x-2t)^2}\) is a pulse moving toward \(+x\) at 2 m/s.</p>
<p>For the harmonic wave \(y = A\sin(kx - \omega t + \phi)\):</p>
<ul>
<li>the coefficient of \(x\) is \(k = 2\pi/\lambda\); the coefficient of \(t\) is \(\omega = 2\pi f\);</li>
<li>the wave speed is \(v = \omega/k\) (ratio of the coefficients, with signs dropped);</li>
<li>opposite signs of the \(x\) and \(t\) terms mean motion toward \(+x\); the same sign means \(-x\).</li>
</ul>
<p>If the equation is written as \(y = A\sin2\pi(x/\lambda - t/T)\), read \(\lambda\) and \(T\) directly.</p>'''),
        ('Particle velocity is not wave velocity', r'''<p>Each particle oscillates up and down; the wave pattern moves sideways. Particle velocity is \(v_p = \partial y/\partial t = -A\omega\cos(kx - \omega t)\), with maximum \(A\omega\). The wave speed is \(v = \omega/k\), fixed by the medium.</p>
<ul>
<li>A useful link: \(v_p = -v\,\dfrac{\partial y}{\partial x}\). Where the snapshot slopes upward (in the direction of travel), the particle is moving down, and vice versa.</li>
<li>\(v_{p,\max}/v = Ak = 2\pi A/\lambda\). The two are equal only if \(\lambda = 2\pi A\).</li>
<li>Particle acceleration is \(-\omega^2y\): each particle does SHM.</li>
</ul>'''),
        ('Phase difference and path difference', r'''<p>Two points a distance \(\Delta x\) apart along the wave differ in phase by \(\Delta\phi = \dfrac{2\pi}{\lambda}\Delta x\). One point at two times \(\Delta t\) apart differs by \(\Delta\phi = \dfrac{2\pi}{T}\Delta t\).</p>
<p>Points \(\lambda\) apart are in phase. Points \(\lambda/2\) apart are in opposite phase. Points \(\lambda/4\) apart are a quarter cycle apart.</p>'''),
    ],
    formulas=[
        dict(title='Phase difference from path and time', formula=r'\Delta\phi=\frac{2\pi}{\lambda}\Delta x,\qquad \Delta\phi=\frac{2\pi}{T}\Delta t',
             symbols='Δφ phase difference (rad); λ wavelength (m); Δx separation along the direction of travel (m); T period (s); Δt time interval (s).'),
        dict(title='Particle velocity and wave slope', formula=r'v_p=-v\,\frac{\partial y}{\partial x},\qquad \frac{v_{p,\max}}{v}=Ak=\frac{2\pi A}{\lambda}',
             symbols='v_p particle velocity (m/s); v wave speed (m/s), positive for travel toward +x; ∂y/∂x slope of the snapshot; A amplitude (m); k wave number (rad/m); λ wavelength (m).'),
    ],
    figure=dict(svg=_fig_snapshot(),
                caption=r'A snapshot of a wave moving to the right. Particles just ahead of a crest are moving up, and those just behind are moving down. Crests and troughs are momentarily at rest; particles on the mean line move fastest.'),
    traps=[r'In a transverse wave the particles do not travel with the wave. They oscillate about fixed mean positions; only energy and the pattern move.',
           r'In \(y = A\sin(\omega t - kx)\) the wave still moves toward \(+x\). What matters is that \(x\) and \(t\) have opposite signs, not which comes first.'],
    exam=r'''<ul>
<li>“For y = 0.03 sin(0.5πx − 100πt), find the wave speed, the maximum particle speed and the phase difference between points 1 m apart.”</li>
<li>“Which of these functions represents a travelling wave?” (only f(x ± vt) forms)</li>
<li>“Find the phase difference between two points 15 cm apart when f = 500 Hz and v = 300 m/s.”</li>
<li>Graph: “In this snapshot of a wave moving to the right, what is the direction of motion of particle P?”</li>
<li>“If the maximum particle speed is four times the wave speed, find λ in terms of A.”</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A wave is \(y = 0.03\sin(0.5\pi x - 100\pi t)\) in SI units. Find the wave speed, the maximum particle speed, and the phase difference between two points 1 m apart.',
             steps=[r'\(k = 0.5\pi\) rad/m and \(\omega = 100\pi\) rad/s.',
                    r'Wave speed: \(v = \omega/k = 100\pi/0.5\pi = 200\) m/s, toward \(+x\).',
                    r'Maximum particle speed: \(A\omega = 0.03\times100\pi\approx9.42\) m/s, much less than the wave speed.',
                    r'Phase difference: \(\Delta\phi = k\Delta x = 0.5\pi\times1 = \pi/2\).'],
             answer=r'200 m/s; about 9.4 m/s; π/2'),
        dict(tag='Graph', q=r'A snapshot shows a transverse wave moving to the right. Point P is on the rising slope just in front of a crest (between a trough and the next crest ahead of it, on the side facing the direction of travel). Is P moving up or down?',
             steps=[r'Use \(v_p = -v\,\partial y/\partial x\) with \(v > 0\).',
                    r'Just in front of a crest, the shape slopes downward as \(x\) increases, so \(\partial y/\partial x < 0\) and \(v_p > 0\): moving up.',
                    r'A quicker way: shift the whole snapshot slightly to the right. The crest arrives at P a moment later, so P must be rising toward the crest.'],
             answer=r'P is moving up.'),
        dict(tag='Ratio', q=r'For a wave \(y = A\sin(kx - \omega t)\), the maximum particle speed is four times the wave speed. Find \(\lambda\) in terms of \(A\).',
             steps=[r'\(A\omega = 4\,\omega/k\), so \(Ak = 4\).',
                    r'\(k = 2\pi/\lambda\), so \(2\pi A/\lambda = 4\).',
                    r'\(\lambda = \pi A/2\).'],
             answer=r'\(\lambda = \pi A/2\)'),
    ],
    practice=[
        dict(q=r'A wave of frequency 500 Hz travels at 300 m/s. The phase difference between two points 15 cm apart along its path is',
             options=[r'\(\pi/4\)', r'\(\pi\)', r'\(\pi/2\)', r'\(2\pi\)'], answer=2, type='numerical',
             explanation=r'\(\lambda = v/f = 0.6\) m. \(\Delta\phi = 2\pi\times0.15/0.6 = \pi/2\). \(\pi\) would need a separation of \(\lambda/2 = 30\) cm; \(\pi/4\) would need 7.5 cm.'),
        dict(q=r'Which of these does NOT represent a travelling wave?',
             options=[r'\(y = A\sin(kx - \omega t)\)', r'\(y = A\sin kx\cos\omega t\)', r'\(y = Ae^{-(x+vt)^2}\)', r'\(y = A\cos(\omega t + kx)\)'], answer=1, type='concept',
             explanation=r'\(A\sin kx\cos\omega t\) is a standing wave: \(x\) and \(t\) appear in separate factors, so it cannot be written as \(f(x\pm vt)\). The Gaussian is a pulse moving toward \(-x\), and the cosine form moves toward \(-x\) as well.'),
        dict(q=r'For \(y = 0.02\sin(2\pi x - 400\pi t)\) (SI units), the ratio of the maximum particle speed to the wave speed is',
             options=[r'\(0.04\pi\)', r'\(0.02\)', r'\(25/\pi\)', r'\(400\pi\)'], answer=0, type='numerical',
             explanation=r'\(v_{p,\max}/v = Ak = 0.02\times2\pi = 0.04\pi\approx0.126\). Check: \(A\omega = 8\pi\) m/s and \(v = 400\pi/2\pi = 200\) m/s, ratio \(8\pi/200 = 0.04\pi\). \(25/\pi\) is the inverse.'),
        dict(q=r'Statement I: In a transverse wave on a string, every particle of the string moves along the direction of propagation.<br>Statement II: A wave transfers energy without transferring the medium as a whole.',
             options=ST_OPTS, answer=2, type='statement',
             explanation=r'Statement I is false: in a transverse wave particles move perpendicular to the direction of travel and stay near their mean positions. Statement II is true: only energy and momentum are carried along.'),
    ],
),
# =====================================================================
'waves-speed': dict(
    level='core',
    notes=[
        ('Why v = √(T/μ) for a string', r'''<p><strong>Dimensional check.</strong> Tension has units N = kg m s⁻²; linear density has kg m⁻¹. Their ratio has units m² s⁻², so \(\sqrt{T/\mu}\) is a speed. No other combination of \(T\) and \(\mu\) gives a speed.</p>
<p><strong>Physical argument.</strong> Ride along with a pulse. A small piece of string of length \(\Delta l\) at the top of the pulse moves on a circular arc of radius \(R\) at speed \(v\). The two tension forces, each at a small angle, give a net inward force \(T\Delta l/R\). This must equal \(\mu\Delta l\,v^2/R\). So \(v^2 = T/\mu\).</p>
<p>For a wire of density \(\rho\) and cross-section \(A\): \(\mu = \rho A\), so \(v = \sqrt{T/(\rho A)} = \sqrt{\text{stress}/\rho}\).</p>'''),
        ('Variable tension: a hanging rope', r'''<p>A uniform rope of length \(L\) hangs from the ceiling. At height \(x\) above its lower end, it supports the rope below it: \(T = \mu gx\). So \(v = \sqrt{gx}\), zero at the bottom and \(\sqrt{gL}\) at the top.</p>
<p>The time for a pulse to travel the full length is \(t = \int_0^L dx/\sqrt{gx} = 2\sqrt{L/g}\). It does not depend on the rope’s mass.</p>
<p>If a block hangs from a string and is then dipped in a liquid, buoyancy lowers the tension, which lowers the wave speed and the string’s frequencies.</p>'''),
        ('Waves in solids, liquids and gases', r'''<p>Wave speed always has the form \(\sqrt{\text{elastic property}/\text{inertial property}}\).</p>
<ul>
<li>Longitudinal waves in a thin rod: \(v = \sqrt{Y/\rho}\).</li>
<li>Sound in a liquid or gas: \(v = \sqrt{B/\rho}\), with \(B\) the bulk modulus.</li>
<li>Solids are far stiffer than gases, so sound typically travels fastest in solids (steel about 5000 m/s), then liquids (water about 1500 m/s), then gases (air about 340 m/s).</li>
<li>Transverse waves need a shear stiffness, so they cannot travel through the bulk of a liquid or gas.</li>
</ul>
<p>The details for gases (Newton’s formula and Laplace’s correction) are in the next section.</p>'''),
    ],
    formulas=[
        dict(title='Wire in terms of stress', formula=r'v=\sqrt{\frac{T}{\rho A}}=\sqrt{\frac{\text{stress}}{\rho}}',
             symbols='v transverse wave speed (m/s); T tension (N); ρ density of the wire material (kg/m³); A cross-sectional area (m²); stress = T/A (Pa).'),
        dict(title='Hanging rope', formula=r'v=\sqrt{gx},\qquad t_{\rm total}=2\sqrt{\frac Lg}',
             symbols='v wave speed at height x above the free lower end (m/s); g gravity (m/s²); x height above the lower end (m); t_total time for a pulse to run the whole rope (s); L rope length (m). Uniform rope.'),
        dict(title='Elastic waves in a rod and a fluid', formula=r'v_{\rm rod}=\sqrt{\frac{Y}{\rho}},\qquad v_{\rm fluid}=\sqrt{\frac{B}{\rho}}',
             symbols='v speeds (m/s); Y Young’s modulus (Pa); B bulk modulus (Pa); ρ density (kg/m³). Rod formula is for longitudinal waves in a thin rod.'),
    ],
    traps=[r'Doubling the tension increases the speed by \(\sqrt2\), not 2. Speed goes as \(\sqrt T\).',
           r'Two wires of the same material under the same tension can have different speeds: the thinner wire has smaller \(\mu\) and carries waves faster.'],
    exam=r'''<ul>
<li>“Find the wave speed on a wire of density ρ and radius r under tension T.”</li>
<li>Ratio: “Two wires of the same material, radii in the ratio 1 : 2, same tension. Compare wave speeds.”</li>
<li>“A block hanging from a string is immersed in water. How does the wave speed change?”</li>
<li>“A rope hangs from a ceiling. Find the time a pulse takes to travel from bottom to top.” (2√(L/g))</li>
<li>Concept: “Can transverse waves travel through air?”</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A steel wire has density 8000 kg/m³ and cross-section 1 mm². It is stretched with a tension of 80 N. Find the speed of transverse waves on it.',
             steps=[r'\(\mu = \rho A = 8000\times1\times10^{-6} = 8\times10^{-3}\) kg/m.',
                    r'\(v = \sqrt{T/\mu} = \sqrt{80/(8\times10^{-3})} = \sqrt{10^4}\).',
                    r'\(v = 100\) m/s.'],
             answer=r'100 m/s'),
        dict(tag='Ratio', q=r'Two wires of the same material carry the same tension. Their radii are \(r\) and \(2r\). Compare the wave speeds on them.',
             steps=[r'\(\mu = \rho\pi r^2\), so \(v = \sqrt{T/(\rho\pi r^2)}\propto1/r\).',
                    r'\(v_1/v_2 = 2r/r = 2\).',
                    r'The thinner wire carries waves twice as fast.'],
             answer=r'2 : 1'),
        dict(tag='Numerical', q=r'A uniform rope 10 m long hangs freely from a ceiling. How long does a small pulse take to travel from its lower end to the top? Take \(g = 10\) m/s².',
             steps=[r'At height \(x\) above the lower end, \(v = \sqrt{gx}\), so the pulse speeds up as it climbs.',
                    r'\(t = \int_0^L dx/\sqrt{gx} = 2\sqrt{L/g}\).',
                    r'\(t = 2\sqrt{10/10} = 2\) s.'],
             answer=r'2 s'),
    ],
    practice=[
        dict(q=r'A string carries a block whose density is twice that of water. When the block is fully immersed in water, the speed of transverse waves on the string becomes',
             options=[r'\(v/2\)', r'\(v/\sqrt2\)', r'\(\sqrt2\,v\)', r'\(v\)'], answer=1, type='numerical',
             explanation=r'Buoyancy is half the block’s weight, so the tension halves. \(v\propto\sqrt T\) gives \(v/\sqrt2\). \(v/2\) forgets the square root. \(\sqrt2v\) assumes tension rises.'),
        dict(q=r'Two wires A and B are under the same tension. Their diameters are in the ratio 1 : 2 and their densities in the ratio 1 : 4. The ratio of wave speeds \(v_A : v_B\) is',
             options=['1 : 4', '1 : 1', '2 : 1', '4 : 1'], answer=3, type='numerical',
             explanation=r'\(v\propto1/(r\sqrt\rho)\). \(v_A/v_B = (r_B/r_A)\sqrt{\rho_B/\rho_A} = 2\times2 = 4\). 1 : 4 inverts the ratio; 2 : 1 includes only one of the two factors.'),
        dict(q=r'A uniform rope hangs vertically from a ceiling. The speed of a transverse pulse at the midpoint of the rope compared with that at the top is',
             options=[r'\(1/2\)', r'\(1/\sqrt2\)', r'\(\sqrt2\)', r'1'], answer=1, type='numerical',
             explanation=r'\(v = \sqrt{gx}\), with \(x\) measured from the lower end. The midpoint has \(x = L/2\), the top \(x = L\): ratio \(\sqrt{1/2}\). Tension is not uniform, so 1 is wrong; \(1/2\) forgets the square root.'),
        dict(q=r'Assertion (A): Transverse mechanical waves cannot travel through the bulk of air.<br>Reason (R): Air does not resist a change of shape, so it has no shear modulus.',
             options=AR_OPTS, answer=0, type='ar',
             explanation=r'Both are true and R explains A. Transverse waves need a restoring force against sideways shear. Gases (and liquids) only resist compression, which is why sound in air is longitudinal.'),
    ],
),
# =====================================================================
'waves-superposition': dict(
    level='core',
    notes=[
        ('Resultant amplitude and intensity', r'''<p>Two waves of the same frequency meeting with phase difference \(\delta\) give \(A_R^2 = A_1^2 + A_2^2 + 2A_1A_2\cos\delta\). Since \(I\propto A^2\):</p>
<p>\(I_R = I_1 + I_2 + 2\sqrt{I_1I_2}\cos\delta\).</p>
<ul>
<li>Maximum (\(\delta = 0, 2\pi, \ldots\)): \(A_{\max} = A_1 + A_2\), \(I_{\max} = (\sqrt{I_1}+\sqrt{I_2})^2\).</li>
<li>Minimum (\(\delta = \pi, 3\pi, \ldots\)): \(A_{\min} = |A_1 - A_2|\), \(I_{\min} = (\sqrt{I_1}-\sqrt{I_2})^2\).</li>
<li>\(\dfrac{I_{\max}}{I_{\min}} = \left(\dfrac{A_1+A_2}{A_1-A_2}\right)^2\).</li>
<li>For equal intensities \(I_0\): \(I_{\max} = 4I_0\), \(I_{\min} = 0\), and the average is \(2I_0\). Energy is redistributed, not created.</li>
</ul>'''),
        ('Path difference decides the result', r'''<p>Two sources vibrating in phase send waves to a point P. If the path difference is \(\Delta x\), the phase difference is \(\delta = 2\pi\Delta x/\lambda\).</p>
<ul>
<li>Constructive at P: \(\Delta x = n\lambda\) (\(n = 0, 1, 2, \ldots\)).</li>
<li>Destructive at P: \(\Delta x = (2n+1)\lambda/2\).</li>
</ul>
<p>If the sources themselves are in opposite phase, swap the two conditions.</p>'''),
        ('Coherence', r'''<p>A steady pattern of loud and quiet spots needs a constant phase difference, so the sources must have the same frequency and a fixed phase relation (coherent). Two independent sources change their phase randomly; the \(\cos\delta\) term averages to zero, and intensities simply add: \(I = I_1 + I_2\).</p>'''),
    ],
    formulas=[
        dict(title='Resultant intensity', formula=r'I_R=I_1+I_2+2\sqrt{I_1I_2}\cos\delta',
             symbols='I_R resultant intensity (W/m²); I₁, I₂ intensities of the two waves (W/m²); δ phase difference at the point (rad). Coherent waves of the same frequency in the same medium.'),
        dict(title='Ratio of maximum to minimum intensity', formula=r'\frac{I_{\max}}{I_{\min}}=\left(\frac{\sqrt{I_1}+\sqrt{I_2}}{\sqrt{I_1}-\sqrt{I_2}}\right)^2=\left(\frac{A_1+A_2}{A_1-A_2}\right)^2',
             symbols='I_max, I_min extreme intensities (W/m²); I₁, I₂ individual intensities; A₁, A₂ amplitudes (m), with A₁ > A₂.'),
        dict(title='Interference conditions (sources in phase)', formula=r'\Delta x=n\lambda\ \text{(max)},\qquad \Delta x=\left(n+\tfrac12\right)\lambda\ \text{(min)}',
             symbols='Δx path difference (m); λ wavelength (m); n = 0, 1, 2, … Swap the conditions if the sources are in antiphase.'),
    ],
    traps=[r'Given an intensity ratio, take square roots before using the amplitude formula. A 9 : 4 intensity ratio means amplitudes 3 : 2, so \(I_{\max}/I_{\min} = (5/1)^2 = 25\), not \(13/5\).',
           r'At a point of constructive interference, two equal waves give 4 times one intensity, not 2 times. The average over the pattern is still 2 times.'],
    exam=r'''<ul>
<li>“Intensities in the ratio 9 : 4 (or amplitudes 3 : 1) interfere. Find I_max/I_min.”</li>
<li>“Two speakers in phase, λ = 0.5 m. Is a point with path difference 0.75 m loud or quiet?”</li>
<li>“Two equal waves interfere with phase difference π/2 (or 2π/3). Find the resultant intensity in terms of I₀.”</li>
<li>Concept: “Why do two independent sources not give a steady interference pattern?”</li>
</ul>''',
    examples=[
        dict(tag='Ratio', q=r'Two coherent waves with intensities in the ratio 9 : 4 interfere. Find the ratio of maximum to minimum intensity.',
             steps=[r'Amplitude ratio \(= \sqrt{9/4} = 3/2\).',
                    r'\(A_{\max} : A_{\min} = (3+2) : (3-2) = 5 : 1\).',
                    r'\(I_{\max}/I_{\min} = 5^2 = 25\).'],
             answer=r'25 : 1'),
        dict(tag='Numerical', q=r'Two loudspeakers driven in phase emit sound of 680 Hz (speed 340 m/s). A listener is 4.25 m from one speaker and 5.00 m from the other. Is the sound loud or quiet there?',
             steps=[r'\(\lambda = 340/680 = 0.5\) m.',
                    r'Path difference \(= 5.00 - 4.25 = 0.75\) m \(= 1.5\lambda\).',
                    r'An odd number of half-wavelengths with sources in phase means destructive interference.',
                    r'If the speakers are equal and the distances similar, the sound there is very weak.'],
             answer=r'Quiet (destructive interference)'),
        dict(tag='Numerical', q=r'Two waves of equal intensity \(I_0\) meet with a phase difference of \(2\pi/3\). Find the resultant intensity.',
             steps=[r'\(I_R = I_0 + I_0 + 2I_0\cos(2\pi/3)\).',
                    r'\(\cos(2\pi/3) = -1/2\), so \(I_R = 2I_0 - I_0 = I_0\).',
                    r'The resultant amplitude is also \(A_0\), matching \(2A_0\cos(\delta/2) = 2A_0\times\tfrac12\).'],
             answer=r'\(I_0\)'),
    ],
    practice=[
        dict(q=r'Two coherent sources have amplitudes in the ratio 3 : 1. The ratio of maximum to minimum intensity in their interference pattern is',
             options=['3 : 1', '9 : 1', '4 : 1', '16 : 1'], answer=2, type='numerical',
             explanation=r'\(I_{\max}/I_{\min} = ((3+1)/(3-1))^2 = (4/2)^2 = 4\). 9 : 1 is just the ratio of the individual intensities. 16 : 1 squares the sum but forgets to divide by the squared difference.'),
        dict(q=r'Two sources vibrating in phase emit waves of wavelength 40 cm. At a point P the path difference is 60 cm. The interference at P is',
             options=['Constructive', 'Destructive', 'Neither, as the phase difference is π/2', 'Constructive only if the amplitudes are equal'], answer=1, type='numerical',
             explanation=r'60 cm \(= 1.5\lambda\), an odd number of half-wavelengths, so the phase difference is \(3\pi\): destructive. A phase difference of \(\pi/2\) would need a path difference of 10 cm. Equal amplitudes affect how complete the cancellation is, not whether it is constructive.'),
        dict(q=r'Statement I: Where two coherent waves of equal intensity \(I_0\) interfere constructively, the intensity is \(4I_0\).<br>Statement II: Interference creates extra energy at the bright points.',
             options=ST_OPTS, answer=1, type='statement',
             explanation=r'Statement I is true: amplitude doubles, so intensity becomes four times. Statement II is false: energy taken from the dark points (zero intensity) appears at the bright points, and the average over the pattern is \(2I_0\), the sum of the two intensities.'),
    ],
),
# =====================================================================
'waves-standing': dict(
    level='core',
    notes=[
        ('Derivation: the standing-wave equation', r'''<p>Add two equal waves travelling in opposite directions:</p>
<p>\(y = A\sin(kx - \omega t) + A\sin(kx + \omega t) = 2A\sin kx\cos\omega t\).</p>
<ul>
<li>Every point oscillates at the same \(\omega\), but with its own amplitude \(2A|\sin kx|\).</li>
<li>Nodes (amplitude zero): \(\sin kx = 0\), \(x = 0, \lambda/2, \lambda, \ldots\)</li>
<li>Antinodes (amplitude \(2A\)): \(x = \lambda/4, 3\lambda/4, \ldots\)</li>
<li>All points between two neighbouring nodes move in phase. Points on opposite sides of a node are in antiphase.</li>
<li>No energy flows past a node, so the wave does not transport energy; energy sloshes between kinetic and potential forms within each loop.</li>
</ul>
<p>If the waves are \(A\sin(kx - \omega t)\) and \(-A\sin(kx+\omega t)\) instead, the result is \(-2A\cos kx\sin\omega t\), with an antinode at \(x = 0\). The origin’s nature depends on the boundary.</p>'''),
        ('Reflection rules', r'''<ul>
<li><strong>Fixed end or denser medium:</strong> the reflected wave is inverted (phase change \(\pi\)). A crest returns as a trough. The end is a node.</li>
<li><strong>Free end or rarer medium:</strong> no phase change. A crest returns as a crest. The end is an antinode.</li>
<li>Frequency never changes on reflection or transmission. Wavelength changes only in the transmitted wave if the speed changes.</li>
</ul>'''),
        ('Pressure and displacement in sound', r'''<p>In a sound standing wave, a displacement node is a pressure antinode, and vice versa. Air molecules on both sides of a displacement node move toward it and away from it together, so the pressure there swings the most. At the closed end of a pipe, the air cannot move (displacement node), but the pressure varies most. At an open end, the pressure stays close to atmospheric (pressure node), while the air moves most.</p>'''),
    ],
    formulas=[
        dict(title='Positions of nodes and antinodes', formula=r'x_{\rm N}=\frac{n\lambda}{2},\qquad x_{\rm A}=\frac{(2n+1)\lambda}{4}\qquad(n=0,1,2,\ldots)',
             symbols='x_N node positions and x_A antinode positions (m), measured from a node at x = 0; λ wavelength (m). For y = 2A sin kx cos ωt.'),
        dict(title='Amplitude at a point', formula=r'A(x)=2A|\sin kx|',
             symbols='A(x) amplitude of the particle at position x (m); A amplitude of each travelling wave (m); k wave number (rad/m). Origin at a node.'),
    ],
    figure=dict(svg=_fig_string_modes(),
                caption=r'The first three modes of a string fixed at both ends. Solid and dashed curves show the string at its two extremes. The nth harmonic has n loops and n + 1 nodes, with λ = 2L/n.'),
    traps=[r'Adjacent nodes are \(\lambda/2\) apart, not \(\lambda\). One full wavelength holds two loops.',
           r'Particles in a standing wave do not all have the same amplitude, but those within one loop are in the same phase. In a travelling wave it is the reverse: same amplitude, different phases.'],
    exam=r'''<ul>
<li>“For y = 4 sin(πx/15) cos(96πt) cm, find the amplitude at x = 5 cm, the node positions, and the speed of the component waves.”</li>
<li>“Distance between a node and the next antinode is 10 cm. Find λ.” (40 cm)</li>
<li>“What is the phase difference between particles in adjacent loops?” (π)</li>
<li>Reflection: “A pulse reflects from a fixed end / free end. Draw the reflected pulse.”</li>
<li>Statement-type: “Energy is not transported in a standing wave.”</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A standing wave on a string is \(y = 4\sin(\pi x/15)\cos(96\pi t)\), with \(x\) and \(y\) in cm and \(t\) in s. Find (a) the amplitude at \(x = 5\) cm, (b) the node positions, (c) the amplitude and speed of the component travelling waves.',
             steps=[r'(a) \(A(5) = 4\sin(\pi/3) = 4\times0.866\approx3.46\) cm.',
                    r'(b) Nodes where \(\sin(\pi x/15) = 0\): \(x = 0, 15, 30, \ldots\) cm. So \(\lambda/2 = 15\) cm and \(\lambda = 30\) cm.',
                    r'(c) The standing-wave amplitude \(2A = 4\) cm, so each travelling wave has \(A = 2\) cm.',
                    r'Speed \(= \omega/k = 96\pi/(\pi/15) = 1440\) cm/s \(= 14.4\) m/s. The frequency is 48 Hz.'],
             answer=r'(a) about 3.46 cm; (b) x = 0, 15, 30 cm …; (c) 2 cm each, 14.4 m/s'),
        dict(tag='Conceptual', q=r'A wave pulse with a crest travels along a light string tied to a heavy rope. Describe the reflected and transmitted pulses.',
             steps=[r'The heavy rope is the denser medium, so it behaves partly like a fixed end.',
                    r'The reflected pulse returns inverted (as a trough), with phase change \(\pi\).',
                    r'The transmitted pulse continues as a crest (never inverted), but moves more slowly in the heavy rope.',
                    r'Both pulses keep the original frequency content; the transmitted pulse is shorter because its speed is lower.'],
             answer=r'Reflected: inverted. Transmitted: upright, slower and shorter.'),
    ],
    practice=[
        dict(q=r'In a standing wave, the distance between a node and the nearest antinode is 10 cm. The wavelength is',
             options=['20 cm', '10 cm', '80 cm', '40 cm'], answer=3, type='numerical',
             explanation=r'Node to the next antinode is \(\lambda/4\), so \(\lambda = 40\) cm. 20 cm treats it as \(\lambda/2\), the node-to-node distance.'),
        dict(q=r'In a stationary wave, particles in two adjacent loops (on either side of a node) oscillate with a phase difference of',
             options=['0', r'\(\pi/2\)', r'\(\pi\)', r'\(2\pi\)'], answer=2, type='concept',
             explanation=r'\(\sin kx\) changes sign across a node, so when one loop goes up, the next goes down: phase difference \(\pi\). Within one loop the phase difference is 0.'),
        dict(q=r'Assertion (A): In a standing wave, there is no net flow of energy along the string.<br>Reason (R): Particles at the nodes are always at rest.',
             options=AR_OPTS, answer=0, type='ar',
             explanation=r'Both are true and R explains A: a node never moves, so no work is done across it and no energy can pass from one loop to the next. Each loop holds its own energy, which changes form during the cycle.'),
        dict(q=r'A pulse travelling on a string reaches a free end (a light ring on a smooth rod). The reflected pulse is',
             options=['Inverted, with the same shape', 'Upright, with the same shape', 'Absent, as all energy is absorbed', 'Upright, but with double the speed'], answer=1, type='concept',
             explanation=r'A free end is a displacement antinode, so reflection happens with no phase change: the pulse returns upright. Inversion happens at a fixed end. The speed is set by the string, so it is unchanged.'),
    ],
),
# =====================================================================
'waves-modes': dict(
    level='exam',
    notes=[
        ('String fixed at both ends', r'''<p>Both ends must be nodes, so a whole number of half-wavelengths fits: \(L = n\lambda/2\).</p>
<ul>
<li>\(\lambda_n = 2L/n\), \(f_n = \dfrac{n}{2L}\sqrt{\dfrac{T}{\mu}}\), with \(n = 1, 2, 3, \ldots\). All harmonics are present.</li>
<li>The nth harmonic is the \((n-1)\)th overtone. It has \(n\) loops, \(n+1\) nodes and \(n\) antinodes.</li>
<li>Laws of a sonometer: \(f\propto1/L\) (fixed \(T, \mu\)), \(f\propto\sqrt T\) (fixed \(L, \mu\)), \(f\propto1/\sqrt\mu\) (fixed \(L, T\)).</li>
<li>Consecutive harmonics differ by \(f_1\). If two consecutive resonances are known, their difference gives the fundamental.</li>
</ul>'''),
        ('Pipes: closed and open', r'''<p><strong>Closed at one end</strong> (node at the closed end, antinode at the open end): \(L = (2n-1)\lambda/4\), so \(f = (2n-1)\dfrac{v}{4L}\). Only odd harmonics: \(f_1, 3f_1, 5f_1, \ldots\) Consecutive resonances differ by \(2f_1\).</p>
<p><strong>Open at both ends</strong> (antinodes at both ends): \(L = n\lambda/2\), so \(f = n\dfrac{v}{2L}\). All harmonics.</p>
<p>For the same length, the open pipe’s fundamental is twice the closed pipe’s. If an open pipe is closed at one end, its fundamental halves. An open pipe sounds richer because it has all harmonics.</p>'''),
        ('End correction and the resonance tube', r'''<p>The antinode at an open end forms slightly outside the pipe, at a distance \(e\approx0.6r\) (\(r\) is the pipe’s inner radius). So the effective length is \(L + e\) for a closed pipe and \(L + 2e\) for an open pipe.</p>
<p>In a resonance-tube experiment with a tuning fork, the first two resonating lengths satisfy \(l_1 + e = \lambda/4\) and \(l_2 + e = 3\lambda/4\). Subtracting removes \(e\):</p>
<p>\(\lambda = 2(l_2 - l_1)\), \(v = 2f(l_2 - l_1)\), and \(e = \dfrac{l_2 - 3l_1}{2}\).</p>'''),
    ],
    formulas=[
        dict(title='End correction', formula=r'f_{\rm closed}=\frac{v}{4(L+e)},\qquad f_{\rm open}=\frac{v}{2(L+2e)},\qquad e\approx0.6r',
             symbols='f fundamental frequencies (Hz); v speed of sound (m/s); L physical pipe length (m); e end correction at each open end (m); r inner radius of the pipe (m).'),
        dict(title='Resonance tube', formula=r'v=2f(l_2-l_1),\qquad e=\frac{l_2-3l_1}{2}',
             symbols='v speed of sound (m/s); f tuning-fork frequency (Hz); l₁, l₂ first and second resonating lengths of the air column (m); e end correction (m).'),
        dict(title='Fundamental from two consecutive resonances', formula=r'f_1=f_{n+1}-f_n\ \text{(string or open pipe)},\qquad f_1=\frac{f_{\rm next}-f_{\rm prev}}{2}\ \text{(closed pipe)}',
             symbols='f₁ fundamental (Hz); f_n, f_(n+1) consecutive resonant frequencies (Hz). In a closed pipe consecutive resonances are odd harmonics, so they differ by 2f₁.'),
    ],
    figure=dict(svg=_fig_pipes(),
                caption=r'Displacement envelopes of air in pipes. A closed end is a displacement node and an open end an antinode. The closed pipe fits odd quarter-wavelengths (f₁, 3f₁, 5f₁ …); the open pipe fits whole half-wavelengths (f₁, 2f₁, 3f₁ …).'),
    traps=[r'Do not count the closed pipe’s overtones as 2f₁, 3f₁. Its first overtone is the 3rd harmonic, its second overtone the 5th harmonic.',
           r'If two consecutive resonances of an unknown pipe differ by \(\Delta f\), check whether the lower one is an odd multiple of \(\Delta f/2\). If yes, it may be a closed pipe with \(f_1 = \Delta f/2\).'],
    exam=r'''<ul>
<li>“A string vibrates at 420 Hz and 490 Hz in two consecutive modes. Find the fundamental.” (70 Hz)</li>
<li>“Consecutive resonances of a pipe are 425 Hz and 595 Hz. Is the pipe open or closed? Find its fundamental.”</li>
<li>“The third harmonic of a closed pipe equals the fundamental of an open pipe. Find the ratio of their lengths.”</li>
<li>“In a resonance tube, l₁ = 16 cm and l₂ = 50 cm with a 500 Hz fork. Find v and the end correction.”</li>
<li>“An open pipe is suddenly closed at one end. How does its fundamental change?” (halves)</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'In a resonance-tube experiment with a 500 Hz tuning fork, the first and second resonances occur at air-column lengths 16 cm and 50 cm. Find the speed of sound and the end correction.',
             steps=[r'\(\lambda/2 = l_2 - l_1 = 34\) cm, so \(\lambda = 68\) cm.',
                    r'\(v = f\lambda = 500\times0.68 = 340\) m/s.',
                    r'\(e = (l_2 - 3l_1)/2 = (50 - 48)/2 = 1\) cm.',
                    r'Check: \(l_1 + e = 17\) cm \(= \lambda/4\). Correct.'],
             answer=r'340 m/s; 1 cm'),
        dict(tag='Ratio', q=r'The third harmonic of a pipe closed at one end has the same frequency as the fundamental of an open pipe. Find the ratio of the open pipe’s length to the closed pipe’s length.',
             steps=[r'Closed pipe third harmonic: \(3v/(4L_c)\).',
                    r'Open pipe fundamental: \(v/(2L_o)\).',
                    r'Equate: \(3/(4L_c) = 1/(2L_o)\), so \(L_o = 2L_c/3\).',
                    r'Ratio \(L_o : L_c = 2 : 3\).'],
             answer=r'2 : 3'),
        dict(tag='Numerical', q=r'A pipe has consecutive resonant frequencies 425 Hz and 595 Hz. Is it open or closed at one end? Find its fundamental and, if \(v = 340\) m/s, its length.',
             steps=[r'Difference \(= 170\) Hz.',
                    r'If open, \(f_1 = 170\) Hz and 425 would be \(2.5f_1\), not a whole number. So it is not open.',
                    r'If closed, \(f_1 = 85\) Hz: \(425 = 5f_1\) and \(595 = 7f_1\), both odd. It is closed at one end.',
                    r'\(L = v/(4f_1) = 340/340 = 1\) m (ignoring end correction).'],
             answer=r'Closed at one end; f₁ = 85 Hz; L = 1 m'),
    ],
    practice=[
        dict(q=r'A stretched string fixed at both ends vibrates at 420 Hz and 490 Hz in two consecutive harmonics. Its fundamental frequency is',
             options=['35 Hz', '70 Hz', '140 Hz', '455 Hz'], answer=1, type='numerical',
             explanation=r'Consecutive harmonics of a string differ by \(f_1\): \(490 - 420 = 70\) Hz. Check: 420 = 6×70 and 490 = 7×70. 35 Hz would apply to a closed pipe, which a string fixed at both ends is not. 455 Hz is the average.'),
        dict(q=r'An open organ pipe has fundamental frequency 300 Hz. If one end is closed, the frequencies of its fundamental and first overtone become',
             options=['150 Hz and 300 Hz', '150 Hz and 450 Hz', '600 Hz and 1800 Hz', '300 Hz and 900 Hz'], answer=1, type='numerical',
             explanation=r'Closing one end halves the fundamental: \(v/4L = 150\) Hz. The first overtone of a closed pipe is the third harmonic, \(3\times150 = 450\) Hz. 300 Hz would be the second harmonic, which a closed pipe cannot produce.'),
        dict(q=r'Match each system (List I) with its allowed harmonics (List II).<br>List I: (P) string fixed at both ends (Q) pipe open at both ends (R) pipe closed at one end<br>List II: (1) odd harmonics only (2) all harmonics',
             options=['P-2, Q-2, R-1', 'P-1, Q-2, R-2', 'P-2, Q-1, R-1', 'P-1, Q-1, R-2'], answer=0, type='match',
             explanation=r'A fixed–fixed string (node–node) and an open–open pipe (antinode–antinode) both fit \(L = n\lambda/2\), so all harmonics are allowed. A closed pipe (node–antinode) fits only odd quarter-wavelengths, so only odd harmonics.'),
        dict(q=r'A pipe of length 50 cm and inner radius 2 cm is open at both ends. Taking the end correction as \(0.6r\) and \(v = 340\) m/s, its fundamental frequency is about',
             options=['340 Hz', '324 Hz', '332 Hz', '680 Hz'], answer=1, type='numerical',
             explanation=r'\(e = 0.6\times2 = 1.2\) cm at each end, so \(L_{\rm eff} = 50 + 2.4 = 52.4\) cm. \(f = 340/(2\times0.524)\approx324\) Hz. 340 Hz ignores the end correction. 332 Hz adds only one end correction, which applies to a closed pipe.'),
    ],
),
# =====================================================================
'waves-beats': dict(
    level='core',
    notes=[
        ('Derivation: why the beat rate is f₁ − f₂', r'''<p>At one place, two sound waves of equal amplitude give</p>
<p>\(y = A\sin2\pi f_1t + A\sin2\pi f_2t = \left[2A\cos\pi(f_1 - f_2)t\right]\sin\pi(f_1 + f_2)t\).</p>
<ul>
<li>The fast factor \(\sin\pi(f_1+f_2)t\) oscillates at the average frequency \((f_1+f_2)/2\). That is the pitch you hear.</li>
<li>The slow factor \(2A\cos\pi(f_1-f_2)t\) is the varying amplitude. Loudness depends on its size, not its sign.</li>
<li>\(|\cos\pi\Delta f\,t|\) peaks every \(1/\Delta f\) seconds. So there are \(|f_1 - f_2|\) loud moments (beats) per second.</li>
</ul>'''),
        ('When beats can be heard', r'''<p>The ear holds a sound impression for about 0.1 s. If the loud–soft cycles come faster than about 10 per second, they blur together. So beats are clearly heard only for small frequency differences, up to roughly 10 Hz. Larger differences are heard as a rough or a combined tone.</p>'''),
        ('Finding an unknown frequency', r'''<p>Suppose a known fork of frequency \(f_0\) gives \(b\) beats per second with an unknown fork X. Then \(f_X = f_0\pm b\). To decide the sign, change X slightly:</p>
<ul>
<li><strong>Waxing</strong> (loading the prongs) lowers \(f_X\). <strong>Filing</strong> the prongs raises \(f_X\).</li>
<li>If lowering \(f_X\) makes the beats fewer, \(f_X\) was above \(f_0\): \(f_X = f_0 + b\).</li>
<li>If lowering \(f_X\) makes the beats more, \(f_X\) was below: \(f_X = f_0 - b\).</li>
<li>Reverse the reasoning for filing. For a string, more tension raises the frequency.</li>
</ul>
<p>If the beats stay the same after the change, the frequency crossed over \(f_0\) (for example, from \(f_0 + b\) to \(f_0 - b\)).</p>'''),
    ],
    formulas=[
        dict(title='Resultant of two close frequencies', formula=r'y=2A\cos\left(\pi\Delta f\,t\right)\sin\left(2\pi\bar f\,t\right),\quad \Delta f=f_1-f_2,\ \bar f=\frac{f_1+f_2}{2}',
             symbols='y displacement (m); A amplitude of each wave (m); Δf frequency difference (Hz); f̄ average frequency, the pitch heard (Hz); t time (s).'),
        dict(title='Beat period', formula=r'T_{\rm beat}=\frac{1}{|f_1-f_2|}',
             symbols='T_beat time between successive loudest sounds (s); f₁, f₂ the two frequencies (Hz).'),
    ],
    figure=dict(svg=_fig_beats(),
                caption=r'Two waves of 20 Hz and 22 Hz added together over one second. The amplitude (dashed envelope) swells and fades twice, giving 2 beats per second, while the fast oscillation runs at about 21 Hz.'),
    traps=[r'Wax lowers a fork’s frequency; filing raises it. Students often reverse these.',
           r'Beats per second equal the difference \(|f_1 - f_2|\), not half of it, even though the envelope factor contains \(\pi\Delta f\). The envelope has two loud peaks per cycle of the cosine.'],
    exam=r'''<ul>
<li>“A fork of 256 Hz gives 6 beats with X. On waxing X, the beats become 4. Find the original frequency of X.”</li>
<li>“Filing X increases the beats. What was X’s frequency?”</li>
<li>“Two identical strings at 400 Hz. The tension in one is raised by 2%. How many beats per second?”</li>
<li>“How many beats are heard in 5 s from 300 Hz and 304 Hz sources?”</li>
<li>Beats combined with Doppler or with pipes and strings.</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A tuning fork of 256 Hz and an unknown fork X produce 6 beats per second. When X is loaded with a little wax, the beat rate drops to 4 per second. Find the original frequency of X.',
             steps=[r'Possible values: \(256 \pm 6\), that is 262 Hz or 250 Hz.',
                    r'Wax lowers the frequency of X.',
                    r'If X were 262 Hz, lowering it (to, say, 260 Hz) brings it closer to 256 Hz: beats drop to 4. This matches.',
                    r'If X were 250 Hz, lowering it moves it farther away, so beats would increase. This does not match.'],
             answer=r'262 Hz'),
        dict(tag='Ratio', q=r'Two identical wires vibrate in unison at 400 Hz. The tension of one is increased by 2%. How many beats per second are heard?',
             steps=[r'\(f\propto\sqrt T\), so for a small change \(\Delta f/f = \tfrac12\,\Delta T/T = 1\%\).',
                    r'\(\Delta f = 0.01\times400 = 4\) Hz.',
                    r'An exact calculation gives \(400(\sqrt{1.02} - 1)\approx3.98\) Hz, so about 4 beats per second.'],
             answer=r'About 4 beats per second'),
    ],
    practice=[
        dict(q=r'A 512 Hz fork gives 4 beats per second with fork B. When B is filed slightly, the beat rate increases to 6 per second. The original frequency of B was',
             options=['508 Hz', '510 Hz', '516 Hz', '518 Hz'], answer=2, type='numerical',
             explanation=r'B is 508 or 516 Hz. Filing raises B. From 516 Hz, raising moves it away from 512, so beats increase, as observed. From 508 Hz, raising it would bring it closer and reduce the beats. 518 Hz is the value after filing, not before.'),
        dict(q=r'Sources of 300 Hz and 304 Hz sound together. The number of beats heard in 5 s is',
             options=['4', '8', '20', '1520'], answer=2, type='numerical',
             explanation=r'Beat frequency \(= 4\) per second, so 20 beats in 5 s. 4 is the rate per second, not the count in 5 s. 1520 multiplies the average frequency by 5.'),
        dict(q=r'Statement I: Two tuning forks of 256 Hz and 320 Hz sounded together produce clearly audible beats at 64 per second.<br>Statement II: The heard pitch during beats is the average of the two frequencies.',
             options=ST_OPTS, answer=2, type='statement',
             explanation=r'Statement I is false: 64 loud–soft cycles per second are far too fast for the ear to follow (the limit is about 10 per second). Statement II is true for close frequencies: the fast oscillation is at \((f_1 + f_2)/2\).'),
    ],
),
# =====================================================================
'waves-doppler': dict(
    level='exam',
    notes=[
        ('Deriving the two effects separately', r'''<p><strong>Moving source.</strong> A source of frequency \(f\) moves toward the observer at \(v_s\). In one period \(1/f\), a wavefront travels \(v/f\) but the source follows it by \(v_s/f\). So the wavelength ahead shrinks to \(\lambda' = (v - v_s)/f\). The observer receives \(f^{\prime} = v/\lambda' = f\dfrac{v}{v - v_s}\).</p>
<p><strong>Moving observer.</strong> The wavelength is unchanged, \(\lambda = v/f\), but an observer moving toward the source at \(v_o\) meets the waves at relative speed \(v + v_o\). So \(f^{\prime} = (v + v_o)/\lambda = f\dfrac{v + v_o}{v}\).</p>
<p>Combining: \(f^{\prime} = f\dfrac{v \pm v_o}{v \mp v_s}\). Sign rule: use the upper signs for motion toward the other party (each raises \(f'\)), the lower signs for motion away.</p>'''),
        ('Special cases', r'''<ul>
<li><strong>Same velocity.</strong> Source and observer moving together in still air: \(f^{\prime} = f\) (the factors cancel).</li>
<li><strong>Wind</strong> blowing at \(w\) from source to observer: replace \(v\) by \(v + w\) (or \(v - w\) if it blows the other way). If nothing moves except the air, there is no shift.</li>
<li><strong>Motion at an angle.</strong> Use only the component of velocity along the line joining source and observer. At the moment of closest approach (motion perpendicular to the line), there is no shift.</li>
<li><strong>Reflection from a moving object.</strong> Treat it in two steps: the object first acts as a moving observer, then as a moving source. A car approaching a wall at \(u\) hears its own echo at \(f\dfrac{v+u}{v-u}\).</li>
<li><strong>Source passing by.</strong> The pitch drops suddenly from \(f\dfrac{v}{v - v_s}\) to \(f\dfrac{v}{v + v_s}\).</li>
</ul>'''),
        ('Why source and observer motion are not symmetric', r'''<p>A source approaching at 100 m/s (with \(v = 340\) m/s) gives \(f^{\prime} = f\times340/240 = 1.42f\). An observer approaching at 100 m/s gives \(f^{\prime} = f\times440/340 = 1.29f\). The results differ because sound moves relative to the air, so “who is moving” relative to the air matters. Only the relative velocity matters for light, which needs no medium.</p>'''),
    ],
    formulas=[
        dict(title='General Doppler formula', formula=r"f'=f\,\frac{v\pm v_o}{v\mp v_s}",
             symbols='f′ observed and f emitted frequency (Hz); v speed of sound in still air (m/s); v_o observer speed and v_s source speed along the line joining them (m/s). Upper signs for motion toward the other; lower signs for motion away. Subsonic speeds.'),
        dict(title='Echo from a moving reflector', formula=r"f''=f\,\frac{v+u}{v-u}",
             symbols='f″ frequency of the echo heard by the moving source (Hz); f emitted frequency (Hz); v speed of sound (m/s); u speed of the source approaching a fixed wall, or of a reflector approaching a fixed source (m/s).'),
        dict(title='Approaching and receding source', formula=r"\frac{f'_{\rm app}}{f'_{\rm rec}}=\frac{v+v_s}{v-v_s}",
             symbols='f′_app, f′_rec frequencies heard by a stationary observer as the source approaches and recedes (Hz); v speed of sound (m/s); v_s source speed (m/s).'),
    ],
    figure=dict(svg=_fig_doppler(),
                caption=r'Wavefronts from a source S moving to the right at half the speed of sound. Each circle is centred where S was when it was emitted. Ahead of S the wavefronts crowd together (shorter wavelength, higher frequency); behind it they spread out.'),
    traps=[r'Do not put the observer’s speed in the denominator or the source’s speed in the numerator. A moving observer changes the encounter rate (numerator); a moving source changes the wavelength (denominator).',
           r'When the source and observer move with the same velocity in still air, the frequency does not change, even though both are “moving”.'],
    exam=r'''<ul>
<li>“A train whistle of 640 Hz approaches at 20 m/s and then recedes. Find both frequencies heard on the platform.”</li>
<li>“A car sounding its horn approaches a wall. Find the frequency of the echo heard by the driver and the beats with the direct sound.”</li>
<li>“At what speed must a source approach for the frequency heard to double?” (v/2)</li>
<li>“Source and observer both move.” Choose signs carefully.</li>
<li>Assertion–reason on why the formulas for a moving source and a moving observer differ.</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A train whistle of 640 Hz approaches a platform at 20 m/s and then moves away at the same speed. Find the frequencies heard by a person on the platform. Speed of sound 340 m/s.',
             steps=[r"Approaching: \(f^{\prime} = 640\times340/(340 - 20) = 640\times340/320 = 680\) Hz.",
                    r"Receding: \(f^{\prime} = 640\times340/(340 + 20) = 640\times340/360\approx604\) Hz.",
                    r'Ratio: \(680/604.4 = 360/320 = 1.125\), as the formula \((v+v_s)/(v-v_s)\) predicts.'],
             answer=r'680 Hz approaching, about 604 Hz receding'),
        dict(tag='Numerical', q=r'A car approaches a large wall at 10 m/s, sounding a 500 Hz horn. Speed of sound 340 m/s. Find the frequency of the echo heard by the driver and the beat frequency with the direct sound.',
             steps=[r'Step 1, wall as a stationary observer of a moving source: \(f_1 = 500\times340/330\).',
                    r'Step 2, wall as a stationary source and driver as a moving observer approaching it: \(f_2 = f_1\times350/340 = 500\times350/330\).',
                    r'\(f_2\approx530.3\) Hz.',
                    r'Beats with the 500 Hz horn: about 30 per second (too fast to hear clearly as beats).'],
             answer=r'About 530 Hz; about 30 beats per second'),
        dict(tag='Ratio', q=r'At what speed must a sound source approach a stationary observer for the observed frequency to be double the emitted frequency?',
             steps=[r'\(v/(v - v_s) = 2\).',
                    r'\(v = 2v - 2v_s\), so \(v_s = v/2\).',
                    r'For comparison, an observer would have to approach at \(v\) (the speed of sound) to double the frequency: \((v + v_o)/v = 2\).'],
             answer=r'Half the speed of sound'),
    ],
    practice=[
        dict(q=r'A source of 900 Hz approaches a stationary observer at 34 m/s. If sound travels at 340 m/s, the observed frequency is',
             options=['990 Hz', '1000 Hz', '810 Hz', '818 Hz'], answer=1, type='numerical',
             explanation=r'\(f^{\prime} = 900\times340/(340 - 34) = 900\times340/306 = 1000\) Hz. 990 Hz uses the moving-observer formula \(900\times374/340\). 818 Hz is the receding-source value.'),
        dict(q=r'A source and an observer move in the same direction with the same speed (still air, speed below that of sound). The frequency heard by the observer is',
             options=['Greater than emitted', 'Less than emitted', 'Equal to emitted', 'Zero'], answer=2, type='concept',
             explanation=r'With the observer ahead: \(f^{\prime} = f(v - u)/(v - u) = f\). The rise from the source approaching is exactly cancelled by the observer moving away. Only relative motion along the line changes the result here, and there is none.'),
        dict(q=r'A bat flies toward a wall at 10 m/s, emitting sound of 40 kHz. Speed of sound 340 m/s. The frequency of the echo it hears is about',
             options=['40.0 kHz', '41.2 kHz', '43.6 kHz', '42.4 kHz'], answer=3, type='numerical',
             explanation=r'Echo from a fixed wall heard by a moving source: \(f'' = f(v + u)/(v - u) = 40\times350/330\approx42.4\) kHz. 41.2 kHz includes only one of the two Doppler steps. 40 kHz ignores motion.'.replace("f''", r"f^{\prime\prime}")),
        dict(q=r'Assertion (A): For sound, a source moving toward a stationary observer and an observer moving toward a stationary source at the same speed give different observed frequencies.<br>Reason (R): Sound travels through a medium, so motion relative to the medium matters.',
             options=AR_OPTS, answer=0, type='ar',
             explanation=r'Both are true and R explains A. A moving source changes the wavelength in the air; a moving observer changes the rate at which it meets waves. With \(v = 340\) m/s and 100 m/s, they give \(1.42f\) and \(1.29f\).'),
    ],
),
}


NEW_SECTIONS = [
# =====================================================================
dict(chapter='waves', after='waves-speed', id='waves-sound',
     title='Speed of sound: Newton, Laplace and what changes it',
     intro=r'Sound in air is a train of squeezes and stretches. How fast it moves depends on how hard the air pushes back when squeezed and how heavy it is. Newton first assumed the air stays at the same temperature while it is squeezed. His answer came out about 15% too low. Laplace fixed it by noting that the squeezes happen so fast that heat has no time to flow out.',
     reasoning=r'Sound speed in a gas is \(\sqrt{B/\rho}\). For an isothermal change \(B = p\) (Newton); for a fast adiabatic change \(B = \gamma p\) (Laplace). Air is compressed and released hundreds of times a second, and air conducts heat poorly, so the adiabatic value is correct. Writing \(p/\rho = RT/M\) shows that the speed depends on temperature and on the kind of gas, but not on pressure alone.',
     formula=r'v_{\rm Newton}=\sqrt{\frac p\rho},\qquad v_{\rm Laplace}=\sqrt{\frac{\gamma p}{\rho}}=\sqrt{\frac{\gamma RT}{M}}',
     symbols='v speed of sound (m/s); p gas pressure (Pa); ρ gas density (kg/m³); γ = C_p/C_v (1.4 for air); R = 8.314 J/(mol K); T absolute temperature (K); M molar mass (kg/mol). Ideal gas, small-amplitude sound.',
     trap=r'Doubling the pressure of a gas at constant temperature does not change the speed of sound. Density doubles too, so \(p/\rho\) is unchanged.',
     example=r'Find the speed of sound in air at STP from Newton’s formula and from Laplace’s formula. Take \(p = 1.013\times10^5\) Pa, \(\rho = 1.293\) kg/m³ and \(\gamma = 1.4\).',
     solution=r'Newton: \(v = \sqrt{1.013\times10^5/1.293}\approx280\) m/s. Laplace: \(v = \sqrt{1.4}\times280\approx331\) m/s, which matches the measured value of about 332 m/s.',
     question='The speed of sound in a gas at 0 °C is v. It becomes 2v at',
     options='273 °C|546 °C|819 °C|1092 °C',
     answer=2,
     explanation=r'\(v\propto\sqrt T\), so doubling \(v\) needs \(T = 4\times273 = 1092\) K, which is 819 °C. 1092 °C mistakes kelvin for Celsius; 273 °C only doubles \(T\).',
     deep=dict(
         level='core',
         notes=[
             ('Newton’s formula and why it failed', r'''<p>Newton treated the compressions in a sound wave as isothermal. For an isothermal ideal gas, \(pV = \text{constant}\), so \(B = -V\,dp/dV = p\). That gives \(v = \sqrt{p/\rho}\approx280\) m/s at STP. The measured value is about 332 m/s, roughly 18% higher.</p>
<p>Laplace pointed out that compressions and rarefactions alternate very fast, and air is a poor conductor of heat. A compressed region warms up and cannot lose that heat before it expands again. The process is adiabatic: \(pV^\gamma = \text{constant}\), so \(B = \gamma p\). The speed rises by \(\sqrt\gamma = \sqrt{1.4}\approx1.18\), giving about 331 m/s.</p>'''),
             ('What changes the speed of sound in a gas', r'''<ul>
<li><strong>Temperature:</strong> \(v\propto\sqrt T\) (absolute). Near room temperature, \(v_t\approx v_0 + 0.61\,t\) m/s, with \(t\) in °C and \(v_0\approx332\) m/s.</li>
<li><strong>Pressure:</strong> no effect at constant temperature, because \(p/\rho = RT/M\).</li>
<li><strong>Humidity:</strong> moist air is less dense (water vapour, \(M = 18\) g/mol, replaces heavier N₂ and O₂), so sound travels slightly faster on a humid day.</li>
<li><strong>Nature of the gas:</strong> \(v\propto\sqrt{\gamma/M}\) at the same temperature. Sound in hydrogen is 4 times as fast as in oxygen (same \(\gamma\), \(M\) ratio 1 : 16).</li>
<li><strong>Wind:</strong> adds its component along the direction of travel.</li>
<li><strong>Frequency, wavelength and amplitude:</strong> no effect. All audible frequencies travel together, which is why music from far away still sounds in tune.</li>
</ul>'''),
             ('Link to molecular speeds', r'''<p>Kinetic theory gives \(v_{\rm rms} = \sqrt{3RT/M}\). Dividing, \(v_{\rm sound}/v_{\rm rms} = \sqrt{\gamma/3}\), about 0.68 for air. Sound cannot outrun the molecules that carry it, and both scale as \(\sqrt{T/M}\).</p>'''),
         ],
         formulas=[
             dict(title='Temperature dependence near room temperature', formula=r'v_t\approx v_0+0.61\,t',
                  symbols='v_t speed at t °C (m/s); v₀ ≈ 332 m/s at 0 °C; t Celsius temperature. Linear approximation of v ∝ √T for air, good for ordinary temperatures.'),
             dict(title='Comparing two gases or temperatures', formula=r'\frac{v_1}{v_2}=\sqrt{\frac{\gamma_1T_1M_2}{\gamma_2T_2M_1}}',
                  symbols='v₁, v₂ sound speeds (m/s); γ₁, γ₂ heat-capacity ratios; T₁, T₂ absolute temperatures (K); M₁, M₂ molar masses (any consistent unit).'),
             dict(title='Sound speed and rms speed', formula=r'\frac{v_{\rm sound}}{v_{\rm rms}}=\sqrt{\frac\gamma3}',
                  symbols='v_sound speed of sound (m/s); v_rms root-mean-square molecular speed (m/s); γ = C_p/C_v of the gas. Same gas and temperature.'),
         ],
         traps=[r'Use absolute temperature in \(v\propto\sqrt T\). Going from 27 °C to 54 °C does not double \(T\); it changes it from 300 K to 327 K.',
                r'Humid air carries sound faster, not slower. Water vapour is lighter than the nitrogen and oxygen it replaces.'],
         exam=r'''<ul>
<li>“Find the speed of sound at STP by Newton’s formula. Why is it wrong? What correction did Laplace make?”</li>
<li>“At what temperature is the speed of sound double (or 1.5 times) its value at 0 °C / 27 °C?”</li>
<li>“How does the speed of sound change with pressure, humidity, temperature?”</li>
<li>“Compare the speed of sound in hydrogen and oxygen at the same temperature.” (4 : 1)</li>
<li>Ratio of v_sound to v_rms.</li>
</ul>''',
         examples=[
             dict(tag='Numerical', q=r'The speed of sound in air is 332 m/s at 0 °C. Find it at 27 °C.',
                  steps=[r'\(v\propto\sqrt T\): \(v = 332\sqrt{300/273}\).',
                         r'\(\sqrt{300/273} = \sqrt{1.0989}\approx1.0483\).',
                         r'\(v\approx348\) m/s. The rule \(v_0 + 0.61t\) gives \(332 + 16.5 = 348.5\) m/s, in close agreement.'],
                  answer=r'About 348 m/s'),
             dict(tag='Ratio', q=r'At what temperature is the speed of sound in hydrogen equal to its speed in oxygen at 100 °C? Both are diatomic.',
                  steps=[r'Same \(\gamma\), so \(v\propto\sqrt{T/M}\). Set \(T_H/M_H = T_O/M_O\).',
                         r'\(T_H = 373\times2/32\approx23.3\) K.',
                         r'In Celsius: \(23.3 - 273\approx-250\) °C. Hydrogen must be very cold to slow sound down to oxygen’s level.'],
                  answer=r'About 23 K (about −250 °C)'),
         ],
         practice=[
             dict(q=r'The pressure of a gas is doubled while its temperature is kept constant. The speed of sound in it',
                  options=['Doubles', r'Increases by \(\sqrt2\)', 'Halves', 'Does not change'], answer=3, type='concept',
                  explanation=r'\(v = \sqrt{\gamma p/\rho}\). At constant temperature, density doubles along with pressure, so \(p/\rho\) is unchanged. The other options treat \(\rho\) as fixed.'),
             dict(q=r'Laplace’s correction raises Newton’s value of the speed of sound in air by a factor of about',
                  options=['1.40', '1.67', '0.85', '1.18'], answer=3, type='numerical',
                  explanation=r'The factor is \(\sqrt\gamma = \sqrt{1.4}\approx1.18\). 1.40 is \(\gamma\) itself, forgetting the square root. 1.67 is \(\gamma\) for a monatomic gas. 0.85 is the inverse.'),
             dict(q=r'Statement I: Sound travels slightly faster in humid air than in dry air at the same temperature and pressure.<br>Statement II: The density of humid air is less than that of dry air at the same temperature and pressure.',
                  options=ST_OPTS, answer=0, type='statement',
                  explanation=r'Both are true, and II is the reason for I. Water vapour (18 g/mol) replaces nitrogen and oxygen (about 29 g/mol on average), so the density falls and \(v = \sqrt{\gamma p/\rho}\) rises.'),
             dict(q=r'The speed of sound in air at 27 °C is \(v\). It becomes \(1.5v\) at',
                  options=['402 °C', '675 °C', '40.5 °C', '127 °C'], answer=0, type='numerical',
                  explanation=r'\(T_2 = 1.5^2\times300 = 675\) K \(= 402\) °C. 675 °C forgets to convert kelvin to Celsius. 40.5 °C multiplies the Celsius temperature by 1.5, ignoring both the square and absolute temperature.'),
         ],
     )),
# =====================================================================
dict(chapter='waves', after='waves-sound', id='waves-intensity',
     title='Intensity, energy and loudness',
     intro=r'A wave carries energy without carrying matter. Stand close to a loudspeaker and you can feel the air push on you; walk away and the sound fades. The energy a wave delivers each second to each square metre is its intensity. It grows with the square of the amplitude and the square of the frequency.',
     reasoning=r'Each particle of the medium does SHM with energy \(\tfrac12m\omega^2A^2\). Per unit volume this is \(\tfrac12\rho\omega^2A^2\). The wave moves this energy along at speed \(v\), so the power through each square metre is \(I = \tfrac12\rho v\omega^2A^2\). As sound spreads out from a small source, the same power covers a larger area, so intensity falls with distance.',
     formula=r'I=\tfrac12\rho v\omega^2A^2=2\pi^2\rho vf^2A^2',
     symbols='I intensity (W/m²); ρ density of the medium (kg/m³); v wave speed (m/s); ω angular frequency (rad/s); f frequency (Hz); A displacement amplitude (m). Harmonic wave in a uniform medium.',
     trap=r'Intensity depends on both amplitude and frequency. Two waves with the same amplitude but different frequencies do not have the same intensity.',
     example=r'Two sound waves in the same air have amplitudes in the ratio 2 : 1 and frequencies in the ratio 1 : 2. Compare their intensities.',
     solution=r'\(I\propto f^2A^2\), so \(I_1/I_2 = (1/2)^2\times2^2 = 1\). The intensities are equal.',
     question='The distance from a small sound source is doubled (no absorption). The intensity becomes',
     options='Half|One quarter|Double|Unchanged',
     answer=1,
     explanation=r'A point source spreads its power over a sphere of area \(4\pi r^2\). Doubling \(r\) quadruples the area, so \(I\) falls to a quarter. The amplitude halves, which is where “half” comes from.',
     deep=dict(
         level='core',
         notes=[
             ('Derivation: intensity of a wave', r'''<ol>
<li>A particle of mass \(\Delta m\) in SHM has total energy \(\tfrac12\Delta m\,\omega^2A^2\).</li>
<li>Energy per unit volume (energy density): \(u = \tfrac12\rho\omega^2A^2\).</li>
<li>In time \(\Delta t\), the energy in a column of length \(v\Delta t\) and area \(S\) crosses the area \(S\): energy \(= u\,Sv\Delta t\).</li>
<li>Intensity \(= \dfrac{\text{energy}}{S\Delta t} = uv = \tfrac12\rho v\omega^2A^2\).</li>
</ol>
<p>At fixed medium, \(I\propto A^2\omega^2\), or \(I\propto A^2f^2\).</p>'''),
             ('How intensity falls with distance', r'''<ul>
<li><strong>Point source</strong> (spherical waves): power \(P\) spreads over \(4\pi r^2\). \(I = P/4\pi r^2\propto1/r^2\), and amplitude \(A\propto1/r\).</li>
<li><strong>Line source</strong> (cylindrical waves, such as a long busy road): \(I\propto1/r\) and \(A\propto1/\sqrt r\).</li>
<li><strong>Plane waves</strong> (far from the source, ideal): \(I\) and \(A\) stay constant.</li>
</ul>
<p>Absorption in the medium makes real sound fade faster than these ideal laws.</p>'''),
             ('Loudness, decibels, pitch and quality', r'''<p>The ear responds to an enormous range of intensities, from about \(10^{-12}\) W/m² (threshold of hearing) to about 1 W/m² (threshold of pain). Its sense of loudness grows roughly with the logarithm of intensity. So we use the sound level</p>
<p>\(\beta = 10\log_{10}(I/I_0)\) dB, with \(I_0 = 10^{-12}\) W/m².</p>
<ul>
<li>10 times the intensity adds 10 dB; 100 times adds 20 dB; doubling adds about 3 dB.</li>
<li>Typical levels: whisper about 20–30 dB, conversation about 60 dB, busy traffic about 80 dB, pain about 120 dB.</li>
<li><strong>Loudness</strong> is the listener’s sensation and depends mainly on intensity (and also on frequency).</li>
<li><strong>Pitch</strong> depends on frequency. A female voice usually has a higher pitch than a male voice.</li>
<li><strong>Quality (timbre)</strong> depends on which overtones are present and how strong they are. It lets you tell a violin from a flute playing the same note.</li>
<li>Humans hear about 20 Hz to 20 kHz. Below is infrasound; above is ultrasound.</li>
</ul>'''),
         ],
         formulas=[
             dict(title='Spreading from point and line sources', formula=r'I_{\rm point}=\frac{P}{4\pi r^2}\propto\frac1{r^2},\qquad I_{\rm line}\propto\frac1r',
                  symbols='I intensity (W/m²); P power of the source (W); r distance from the source (m). No absorption; amplitude goes as 1/r for a point source and 1/√r for a line source.'),
             dict(title='Sound level in decibels', formula=r'\beta=10\log_{10}\frac{I}{I_0},\qquad \beta_2-\beta_1=10\log_{10}\frac{I_2}{I_1}',
                  symbols='β sound level (dB); I intensity (W/m²); I₀ = 10⁻¹² W/m², the reference threshold of hearing; I₁, I₂ two intensities being compared.'),
         ],
         traps=[r'Doubling the distance from a point source halves the amplitude but quarters the intensity. Keep \(A\propto1/r\) and \(I\propto1/r^2\) apart.',
                r'Loudness and pitch are different. Turning up the volume raises loudness (intensity) without changing pitch (frequency).'],
         exam=r'''<ul>
<li>“Two waves have amplitude ratio 2 : 1 and frequency ratio 1 : 2. Compare intensities.”</li>
<li>“The distance from a point source is tripled. Find the new intensity / amplitude.”</li>
<li>“The intensity of a sound increases 100 times. By how many decibels does the level rise?” (20 dB)</li>
<li>Match the column: loudness–intensity, pitch–frequency, quality–overtones.</li>
<li>“What is the audible range? What are infrasonic and ultrasonic waves?”</li>
</ul>''',
         examples=[
             dict(tag='Numerical', q=r'A conversation has a sound level of 60 dB and a whisper 40 dB. How many times more intense is the conversation?',
                  steps=[r'\(\beta_2 - \beta_1 = 10\log_{10}(I_2/I_1)\), so \(20 = 10\log_{10}(I_2/I_1)\).',
                         r'\(\log_{10}(I_2/I_1) = 2\), so \(I_2/I_1 = 100\).',
                         r'The conversation is 100 times as intense, though it does not sound 100 times as loud. The ear compresses the range.'],
                  answer=r'100 times'),
             dict(tag='Ratio', q=r'A listener moves from 5 m to 10 m away from a small loudspeaker (no echoes or absorption). Find the change in intensity, amplitude and sound level.',
                  steps=[r'Point source: \(I\propto1/r^2\), so \(I\) becomes \((5/10)^2 = 1/4\) of its value.',
                         r'\(A\propto1/r\), so the amplitude halves.',
                         r'Level change \(= 10\log_{10}(1/4)\approx-6\) dB.'],
                  answer=r'Intensity ÷ 4, amplitude ÷ 2, level drops by about 6 dB'),
             dict(tag='Conceptual', q=r'A violin and a flute play the same note at the same loudness. Why can a listener still tell them apart?',
                  steps=[r'Same note means the same fundamental frequency, so the pitch is the same.',
                         r'Same loudness means similar intensity.',
                         r'The instruments produce different sets of overtones with different strengths, so the waveforms differ in shape.',
                         r'This property is called quality or timbre.'],
                  answer=r'They differ in quality (timbre), set by their overtones.'),
         ],
         practice=[
             dict(q=r'The intensity of a sound increases by a factor of 1000. The sound level increases by',
                  options=['3 dB', '30 dB', '1000 dB', '300 dB'], answer=1, type='numerical',
                  explanation=r'\(\Delta\beta = 10\log_{10}1000 = 10\times3 = 30\) dB. 3 dB is just \(\log_{10}1000\) without the factor 10. 1000 dB treats decibels as proportional to intensity.'),
             dict(q=r'Two waves travel in the same medium. Wave A has twice the amplitude and half the frequency of wave B. The ratio \(I_A : I_B\) is',
                  options=['1 : 1', '4 : 1', '1 : 4', '2 : 1'], answer=0, type='numerical',
                  explanation=r'\(I\propto A^2f^2\): \(I_A/I_B = 2^2\times(1/2)^2 = 1\). 4 : 1 considers only amplitude. 1 : 4 considers only frequency.'),
             dict(q=r'Match each property of a sound (List I) with what it mainly depends on (List II).<br>List I: (P) loudness (Q) pitch (R) quality<br>List II: (1) frequency (2) overtones present (3) intensity',
                  options=['P-1, Q-3, R-2', 'P-3, Q-1, R-2', 'P-3, Q-2, R-1', 'P-2, Q-1, R-3'], answer=1, type='match',
                  explanation=r'Loudness follows intensity, pitch follows frequency and quality follows the mix of overtones. The first option swaps loudness and pitch, the most common confusion.'),
             dict(q=r'Waves spread out from a long straight line source (such as a busy road). If the distance from the source is quadrupled, the amplitude becomes',
                  options=['One quarter', 'One sixteenth', 'One half', 'Unchanged'], answer=2, type='numerical',
                  explanation=r'For a line source, \(I\propto1/r\), so \(A\propto1/\sqrt r\). Quadrupling \(r\) halves \(A\). One quarter is the intensity ratio; one sixteenth would apply to the intensity from a point source.'),
         ],
     )),
]
