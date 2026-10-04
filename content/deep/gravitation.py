"""Deepening layer for the Gravitation chapter (see docs/deepening-schema.md)."""
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


def _pts(f, a, b, sx, sy, n=60):
    out = []
    for i in range(n + 1):
        x = a + (b - a) * i / n
        out.append(f'{sx(x):.1f},{sy(f(x)):.1f}')
    return ' '.join(out)


def _arrow_defs(mid):
    return (f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" markerUnits="userSpaceOnUse" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--ink-2)"/></marker></defs>')


# ---------- Figure: g versus distance from Earth's centre ----------
def _fig_g_vs_r():
    sx = lambda r: 50 + 85 * r          # r in units of R
    sy = lambda g: 170 - 120 * g        # g in units of g0
    inside = _pts(lambda r: r, 0, 1, sx, sy, 2)
    outside = _pts(lambda r: 1 / r ** 2, 1, 3.3, sx, sy)
    return ('<svg viewBox="0 0 360 210" role="img" aria-label="Graph of g against distance r from Earth centre">'
            + _arrow_defs('gv-a') +
            f'<line x1="50" y1="170" x2="345" y2="170" style="{AX}" marker-end="url(#gv-a)"/>'
            f'<line x1="50" y1="170" x2="50" y2="25" style="{AX}" marker-end="url(#gv-a)"/>'
            f'<polyline points="{inside}" style="fill:none;stroke:var(--coral);stroke-width:2.4"/>'
            f'<polyline points="{outside}" style="fill:none;stroke:var(--teal);stroke-width:2.4"/>'
            f'<line x1="135" y1="50" x2="135" y2="170" style="stroke:var(--line-2);stroke-dasharray:4 3"/>'
            f'<line x1="50" y1="50" x2="135" y2="50" style="stroke:var(--line-2);stroke-dasharray:4 3"/>'
            f'<text x="135" y="186" text-anchor="middle" style="{TX}">R</text>'
            f'<text x="220" y="186" text-anchor="middle" style="{TX}">2R</text>'
            f'<line x1="220" y1="170" x2="220" y2="140" style="stroke:var(--line-2);stroke-dasharray:4 3"/>'
            f'<text x="40" y="54" text-anchor="end" style="{TX}">g₀</text>'
            f'<text x="40" y="144" text-anchor="end" style="{TX}">g₀/4</text>'
            f'<text x="340" y="200" text-anchor="end" style="{TX}">r (from centre)</text>'
            f'<text x="58" y="30" style="{TX}">g</text>'
            f'<text x="58" y="80" style="font-size:12px;fill:var(--coral)">g ∝ r</text>'
            f'<text x="58" y="94" style="font-size:12px;fill:var(--coral)">inside</text>'
            f'<text x="200" y="90" style="font-size:12px;fill:var(--teal)">g ∝ 1/r² (outside)</text>'
            '</svg>')


# ---------- Figure: satellite energies versus orbit radius ----------
def _fig_orbit_energy():
    sx = lambda r: 60 + 70 * (r - 1)    # r in units of R, from 1 to 5
    sy = lambda e: 115 - 85 * e          # energy in units of GMm/R
    K = _pts(lambda r: 0.5 / r, 1, 4.1, sx, sy)
    U = _pts(lambda r: -1 / r, 1, 4.1, sx, sy)
    E = _pts(lambda r: -0.5 / r, 1, 4.1, sx, sy)
    return ('<svg viewBox="0 0 360 220" role="img" aria-label="Kinetic, potential and total energy of a satellite against orbit radius">'
            + _arrow_defs('oe-a') +
            f'<line x1="60" y1="115" x2="345" y2="115" style="{AX}" marker-end="url(#oe-a)"/>'
            f'<line x1="60" y1="210" x2="60" y2="15" style="{AX}" marker-end="url(#oe-a)"/>'
            f'<polyline points="{K}" style="fill:none;stroke:var(--teal);stroke-width:2.4"/>'
            f'<polyline points="{E}" style="fill:none;stroke:var(--indigo);stroke-width:2.4"/>'
            f'<polyline points="{U}" style="fill:none;stroke:var(--coral);stroke-width:2.4"/>'
            f'<line x1="220" y1="26" x2="244" y2="26" style="stroke:var(--teal);stroke-width:2.4"/>'
            f'<text x="250" y="30" style="font-size:12px;fill:var(--teal)">K = +GMm/2r</text>'
            f'<line x1="220" y1="44" x2="244" y2="44" style="stroke:var(--indigo);stroke-width:2.4"/>'
            f'<text x="250" y="48" style="font-size:12px;fill:var(--indigo)">E = −GMm/2r</text>'
            f'<line x1="220" y1="62" x2="244" y2="62" style="stroke:var(--coral);stroke-width:2.4"/>'
            f'<text x="250" y="66" style="font-size:12px;fill:var(--coral)">U = −GMm/r</text>'
            f'<text x="66" y="22" style="{TX}">Energy</text>'
            f'<text x="345" y="108" text-anchor="end" style="{TX}">r</text>'
            f'<text x="64" y="130" style="{TM}">r = R</text>'
            f'<text x="52" y="119" text-anchor="end" style="{TM}">0</text>'
            '</svg>')


# ---------- Figure: Kepler ellipse ----------
def _fig_kepler():
    # ellipse centre (180,112), a=140, b=100 -> focus at x = 180 - 98 = 82; e = 0.7
    # the two sectors were sized numerically to have equal areas
    return ('<svg viewBox="0 0 360 235" role="img" aria-label="Elliptical orbit with the Sun at one focus and two equal swept areas">'
            '<ellipse cx="180" cy="112" rx="140" ry="100" style="fill:none;stroke:var(--ink-2);stroke-width:1.6"/>'
            '<path d="M82,112 L72.9,176.4 A140,100 0 0 1 72.9,47.6 Z" style="fill:var(--amber-soft);stroke:var(--amber);stroke-width:1"/>'
            '<path d="M82,112 L318.5,126.6 A140,100 0 0 0 318.5,97.4 Z" style="fill:var(--water-soft);stroke:var(--water);stroke-width:1"/>'
            '<circle cx="82" cy="112" r="8" style="fill:var(--amber);stroke:none"/>'
            '<text x="92" y="150" style="font-size:12px;fill:var(--ink)">Sun at a focus</text>'
            '<circle cx="40" cy="112" r="4" style="fill:var(--teal)"/>'
            '<circle cx="320" cy="112" r="4" style="fill:var(--teal)"/>'
            '<text x="33" y="116" text-anchor="end" style="font-size:12px;fill:var(--ink)">P</text>'
            '<text x="327" y="116" style="font-size:12px;fill:var(--ink)">A</text>'
            '<text x="6" y="230" style="font-size:11px;fill:var(--muted)">P (perihelion): fastest</text>'
            '<text x="354" y="230" text-anchor="end" style="font-size:11px;fill:var(--muted)">A (aphelion): slowest</text>'
            '<text x="190" y="45" text-anchor="middle" style="font-size:11px;fill:var(--muted)">a = (r_min + r_max)/2</text>'
            '<text x="200" y="175" style="font-size:11px;fill:var(--water)">equal areas swept</text>'
            '<text x="200" y="189" style="font-size:11px;fill:var(--water)">in equal times</text>'
            '</svg>')


# ---------- Figure: field and potential for shell and solid sphere ----------
def _fig_shell_sphere():
    # left panel: field; right panel: potential. r in units of R.
    sxL = lambda r: 60 + 70 * r
    syL = lambda g: 160 - 110 * g
    shellE_out = _pts(lambda r: 1 / r ** 2, 1, 3, sxL, syL)
    solid_in = _pts(lambda r: r, 0, 1, sxL, syL, 2)
    sxR = lambda r: 330 + 70 * r
    syR = lambda v: 30 - 70 * v          # v in units of GM/R (negative)
    shellV_in = _pts(lambda r: -1.0, 0, 1, sxR, syR, 2)
    V_out = _pts(lambda r: -1 / r, 1, 3, sxR, syR)
    solidV_in = _pts(lambda r: -(3 - r * r) / 2, 0, 1, sxR, syR, 30)
    return ('<svg viewBox="0 0 570 215" role="img" aria-label="Field and potential against r for a thin shell and a solid sphere">'
            + _arrow_defs('ss-a') +
            # left axes
            f'<line x1="60" y1="160" x2="282" y2="160" style="{AX}" marker-end="url(#ss-a)"/>'
            f'<line x1="60" y1="160" x2="60" y2="20" style="{AX}" marker-end="url(#ss-a)"/>'
            f'<polyline points="{shellE_out}" style="fill:none;stroke:var(--ink-2);stroke-width:2"/>'
            f'<line x1="60" y1="158" x2="130" y2="158" style="stroke:var(--coral);stroke-width:3"/>'
            f'<line x1="130" y1="158" x2="130" y2="50" style="stroke:var(--coral);stroke-width:1.2;stroke-dasharray:3 3"/>'
            f'<polyline points="{solid_in}" style="fill:none;stroke:var(--teal);stroke-width:2.4"/>'
            f'<text x="130" y="176" text-anchor="middle" style="{TX}">R</text>'
            f'<text x="54" y="54" text-anchor="end" style="{TX}">GM/R²</text>'
            f'<text x="68" y="26" style="{TX}">field E</text>'
            f'<text x="278" y="176" text-anchor="end" style="{TX}">r</text>'
            f'<text x="76" y="150" style="font-size:11px;fill:var(--coral)">shell: 0</text>'
            f'<text x="88" y="124" style="font-size:11px;fill:var(--teal)">solid</text>'
            f'<text x="88" y="137" style="font-size:11px;fill:var(--teal)">∝ r</text>'
            f'<text x="180" y="110" style="font-size:11px;fill:var(--ink-2)">both ∝ 1/r²</text>'
            # right axes
            f'<line x1="330" y1="30" x2="552" y2="30" style="{AX}" marker-end="url(#ss-a)"/>'
            f'<line x1="330" y1="200" x2="330" y2="15" style="{AX}" marker-end="url(#ss-a)"/>'
            f'<polyline points="{V_out}" style="fill:none;stroke:var(--ink-2);stroke-width:2"/>'
            f'<polyline points="{shellV_in}" style="fill:none;stroke:var(--coral);stroke-width:2.4"/>'
            f'<polyline points="{solidV_in}" style="fill:none;stroke:var(--teal);stroke-width:2.4"/>'
            f'<line x1="400" y1="30" x2="400" y2="135" style="stroke:var(--line-2);stroke-dasharray:3 3"/>'
            f'<text x="400" y="22" text-anchor="middle" style="{TX}">R</text>'
            f'<text x="548" y="22" text-anchor="end" style="{TX}">r</text>'
            f'<text x="336" y="14" style="{TX}">V</text>'
            f'<text x="324" y="104" text-anchor="end" style="{TM}">−GM/R</text>'
            f'<text x="324" y="139" text-anchor="end" style="{TM}">−3GM/2R</text>'
            f'<text x="336" y="94" style="font-size:11px;fill:var(--coral)">shell: flat</text>'
            f'<text x="336" y="152" style="font-size:11px;fill:var(--teal)">solid: parabola</text>'
            f'<text x="450" y="80" style="font-size:11px;fill:var(--ink-2)">both −GM/r</text>'
            '</svg>')


# ---------- Figure: latitude and the rotating Earth ----------
def _fig_latitude():
    # centre (150,110), radius 80; latitude 40 deg: point P at (150+80cos40, 110-80sin40)
    return ('<svg viewBox="0 0 340 220" role="img" aria-label="Point at latitude lambda on rotating Earth moving in a circle of radius R cos lambda">'
            + _arrow_defs('lt-a') +
            '<circle cx="150" cy="110" r="80" style="fill:var(--water-soft);stroke:var(--water);stroke-width:1.6"/>'
            '<line x1="150" y1="15" x2="150" y2="205" style="stroke:var(--ink-2);stroke-width:1.2;stroke-dasharray:5 3"/>'
            '<line x1="70" y1="110" x2="230" y2="110" style="stroke:var(--line-2);stroke-width:1"/>'
            '<line x1="150" y1="110" x2="211.3" y2="58.6" style="stroke:var(--ink-2);stroke-width:1.4"/>'
            '<line x1="150" y1="58.6" x2="211.3" y2="58.6" style="stroke:var(--coral);stroke-width:1.6"/>'
            '<circle cx="211.3" cy="58.6" r="4" style="fill:var(--ink)"/>'
            '<line x1="211.3" y1="58.6" x2="176" y2="58.6" style="stroke:var(--coral);stroke-width:2" marker-end="url(#lt-a)"/>'
            '<line x1="211.3" y1="58.6" x2="173" y2="90.7" style="stroke:var(--teal);stroke-width:2" marker-end="url(#lt-a)"/>'
            '<path d="M178,110 A28,28 0 0 0 171.5,92" style="fill:none;stroke:var(--ink-2)"/>'
            '<text x="182" y="100" style="font-size:12px;fill:var(--ink)">λ</text>'
            '<text x="218" y="54" style="font-size:12px;fill:var(--ink)">P</text>'
            '<text x="156" y="22" style="font-size:12px;fill:var(--ink)">axis (ω)</text>'
            '<text x="152" y="47" style="font-size:11px;fill:var(--coral)">R cos λ</text>'
            '<text x="236" y="82" style="font-size:11px;fill:var(--coral)">ω²R cos λ needed</text>'
            '<text x="236" y="96" style="font-size:11px;fill:var(--coral)">toward the axis</text>'
            '<text x="158" y="135" style="font-size:11px;fill:var(--teal)">g (toward centre)</text>'
            '<text x="240" y="114" style="font-size:11px;fill:var(--muted)">equator</text>'
            '</svg>')


DEEP = {
# =====================================================================
'gravitation-field': dict(
    level='basic',
    notes=[
        ('What the law really says', r'''<p>Newton’s law \(F = Gm_1m_2/r^2\) has five features that NEET tests directly.</p>
<ol>
<li><strong>Always attractive and central.</strong> The force acts along the line joining the two centres.</li>
<li><strong>Equal and opposite.</strong> The Earth pulls an apple with the same force the apple pulls the Earth. The accelerations differ because \(a = F/m\): the apple accelerates a lot, the Earth almost not at all.</li>
<li><strong>Independent of the medium.</strong> Placing a third body or a wall between two masses does not shield or change the force between them. Each pair interacts on its own.</li>
<li><strong>Universal constant.</strong> \(G = 6.67\times10^{-11}\ \text{N m}^2\,\text{kg}^{-2}\), with dimensions \([M^{-1}L^3T^{-2}]\). \(G\) is the same everywhere. The acceleration \(g\) is not; it depends on where you are.</li>
<li><strong>Very weak.</strong> Two 1 kg masses 1 m apart attract with only about \(6.7\times10^{-11}\) N. Gravity dominates in astronomy only because planets are huge and electrically neutral.</li>
</ol>'''),
        ('Superposition patterns that repeat in tests', r'''<p>Fields and forces from several masses add as vectors. A few set-ups appear again and again.</p>
<ul>
<li><strong>Null point between two masses.</strong> Between masses \(m_1\) and \(m_2\) a distance \(d\) apart, the fields cancel where \(Gm_1/x^2 = Gm_2/(d-x)^2\). This gives \(x = d\sqrt{m_1}/(\sqrt{m_1}+\sqrt{m_2})\) from \(m_1\). The null point sits closer to the smaller mass.</li>
<li><strong>Symmetric arrangements.</strong> Equal masses at the corners of an equilateral triangle, square or regular polygon give zero field at the centre. The field at the centre of a uniform ring is also zero.</li>
<li><strong>Remove one mass.</strong> If one mass is taken away from a symmetric set, the field at the centre equals the field of the missing mass, but pointing away from where it was. The remaining masses no longer have a partner to cancel them.</li>
<li><strong>Force on one corner mass.</strong> For three equal masses at the corners of an equilateral triangle of side \(a\), each pair force is \(Gm^2/a^2\) at 60° to each other, so the net force on one mass is \(\sqrt3\,Gm^2/a^2\).</li>
</ul>'''),
        ('Linking g to G, mass and density', r'''<p>At the surface, the weight \(mg\) is the gravitational force \(GMm/R^2\). So \(g = GM/R^2\). Writing \(M = \tfrac43\pi R^3\rho\) gives \(g = \tfrac43\pi G\rho R\).</p>
<p>Use this to compare planets. If two planets have the same density, \(g \propto R\). If they have the same mass, \(g \propto 1/R^2\). Pick the form that holds the given quantity fixed, then take the ratio.</p>'''),
    ],
    formulas=[
        dict(title='Null point between two masses', formula=r'x=\frac{d\sqrt{m_1}}{\sqrt{m_1}+\sqrt{m_2}}',
             symbols='x distance of the zero-field point from m₁ (m); d separation of the two masses (m); m₁, m₂ point or spherical masses (kg). The point lies on the line between them, closer to the smaller mass.'),
        dict(title='Surface gravity from density', formula=r'g=\frac{GM}{R^2}=\frac43\pi G\rho R',
             symbols='g surface field (m/s²); G = 6.67×10⁻¹¹ N m²/kg²; M planet mass (kg); R planet radius (m); ρ mean density (kg/m³). Assumes a spherically symmetric planet and ignores rotation.'),
        dict(title='Net force on a corner of an equilateral triangle', formula=r'F_{\rm net}=\sqrt3\,\frac{Gm^2}{a^2}',
             symbols='F_net net force on one mass (N); m each of three equal masses (kg); a side of the triangle (m); G gravitational constant. The force points toward the centroid.'),
    ],
    traps=[r'“The Earth attracts the apple more strongly than the apple attracts the Earth” is false. The forces are equal by Newton’s third law; only the accelerations differ.',
           r'Do not add field magnitudes from different masses. Draw the direction of each field first, then add as vectors.'],
    exam=r'''<ul>
<li>“Find the point between masses M and 4M where the gravitational field is zero.” (null point, use square roots of masses)</li>
<li>“Three/four equal masses at the corners of a triangle/square. Find the net force on one mass or the field at the centre.”</li>
<li>“One of the masses is removed. Find the field at the centre now.”</li>
<li>Ratio questions: “A planet has twice the radius and the same density as Earth. Find g there.”</li>
<li>Concept checks: dimensions of G, whether gravity depends on the medium, Newton’s third law for unequal masses.</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'Masses 1 kg and 4 kg are fixed 0.9 m apart. Where on the line joining them is the net gravitational field zero?',
             steps=[r'At the null point the two fields are equal and opposite: \(G(1)/x^2 = G(4)/(0.9-x)^2\), with \(x\) measured from the 1 kg mass.',
                    r'Take square roots: \(1/x = 2/(0.9-x)\), so \(0.9 - x = 2x\).',
                    r'Solve: \(x = 0.3\) m. Check with the shortcut \(x = d\sqrt{m_1}/(\sqrt{m_1}+\sqrt{m_2}) = 0.9\times1/(1+2) = 0.3\) m.',
                    r'The point is nearer the smaller mass, as expected: the larger mass needs more distance to weaken its field to match.'],
             answer=r'0.3 m from the 1 kg mass (0.6 m from the 4 kg mass).'),
        dict(tag='Ratio', q=r'Planet X has the same mean density as Earth but twice its radius. Compare its surface gravity and its mass with Earth’s.',
             steps=[r'Use \(g = \tfrac43\pi G\rho R\). With equal \(\rho\), \(g \propto R\).',
                    r'So \(g_X/g_E = 2\).',
                    r'Mass is \(\tfrac43\pi R^3\rho\), so \(M \propto R^3\) at fixed density: \(M_X/M_E = 2^3 = 8\).',
                    r'Check with \(g = GM/R^2\): \(8/2^2 = 2\). The two routes agree.'],
             answer=r'\(g_X = 2g_E\) and \(M_X = 8M_E\).'),
        dict(tag='Conceptual', q=r'Four equal masses \(m\) sit at the corners of a square of side \(a\). One mass is removed. Find the gravitational field at the centre.',
             steps=[r'With all four present, opposite corners cancel in pairs, so the field at the centre is zero.',
                    r'Removing one mass leaves its diagonal partner unbalanced. The other pair still cancels.',
                    r'The centre is \(a/\sqrt2\) from each corner, so the leftover field is \(Gm/(a/\sqrt2)^2 = 2Gm/a^2\).',
                    r'It points toward the corner opposite the removed mass, that is, away from the empty corner.'],
             answer=r'\(2Gm/a^2\), directed toward the corner diagonally opposite the removed mass.'),
    ],
    practice=[
        dict(q=r'Three equal masses \(m\) are placed at the corners of an equilateral triangle of side \(a\). The magnitude of the net gravitational force on any one mass is',
             options=[r'\(Gm^2/a^2\)', r'\(2Gm^2/a^2\)', r'\(\sqrt3\,Gm^2/a^2\)', r'Zero'], answer=2, type='numerical',
             explanation=r'Each of the two forces is \(Gm^2/a^2\) and they make 60° with each other. The resultant is \(2F\cos30° = \sqrt3\,Gm^2/a^2\). The value \(2Gm^2/a^2\) adds them as if parallel. Zero is the field at the centroid, not the force on a corner.'),
        dict(q=r'Two planets have the same mean density. Their radii are in the ratio 1 : 2. The ratio of their surface gravities is',
             options=['1 : 4', '1 : 2', '2 : 1', '1 : 8'], answer=1, type='numerical',
             explanation=r'\(g = \tfrac43\pi G\rho R\), so at equal density \(g \propto R\) and the ratio is 1 : 2. The choice 1 : 8 is the mass ratio. The choice 1 : 4 wrongly uses \(g \propto 1/R^2\), which holds only at fixed mass, and even then would give 4 : 1.'),
        dict(q=r'Assertion (A): The gravitational field at the centre of a uniform circular ring is zero.<br>Reason (R): Every small element of the ring has a diametrically opposite element whose field at the centre is equal and opposite.',
             options=AR_OPTS, answer=0, type='ar',
             explanation=r'Both statements are true, and the pairing of opposite elements is exactly why the field cancels. The potential at the centre is not zero (it is \(-GM/R\)), but the assertion speaks only of the field, so A is not false.'),
        dict(q=r'Statement I: The force exerted by the Earth on a falling apple equals the force exerted by the apple on the Earth.<br>Statement II: The acceleration of the Earth towards the apple equals the acceleration of the apple towards the Earth.',
             options=ST_OPTS, answer=1, type='statement',
             explanation=r'Statement I is Newton’s third law and is true. Statement II is false: with equal forces, acceleration is \(F/m\), so the Earth’s acceleration is smaller by the factor \(m_{\rm apple}/M_{\rm Earth}\), which is tiny. Mixing up “equal force” with “equal acceleration” is the trap.'),
    ],
),
# =====================================================================
'gravitation-variation': dict(
    level='exam',
    notes=[
        ('Derivation: g at a height h', r'''<p>At height \(h\) the body is \(R+h\) from the centre, and all of Earth’s mass lies inside that radius.</p>
<ol>
<li>\(g_h = \dfrac{GM}{(R+h)^2}\) and \(g = \dfrac{GM}{R^2}\), so \(g_h = g\left(\dfrac{R}{R+h}\right)^2 = g\left(1+\dfrac hR\right)^{-2}\).</li>
<li>For \(h \ll R\), the binomial approximation \((1+x)^{-2}\approx 1-2x\) gives \(g_h \approx g\left(1-\dfrac{2h}{R}\right)\).</li>
<li>The fractional decrease is \(\Delta g/g \approx 2h/R\). At 64 km above Earth (\(R = 6400\) km) this is 2%.</li>
</ol>
<p>Use the exact form when \(h\) is comparable to \(R\). At \(h = R\) the exact value is \(g/4\); the approximation would give \(-g\), which is nonsense.</p>'''),
        ('Derivation: g at a depth d', r'''<p>Picture a body in a mine at depth \(d\). Model Earth as a uniform sphere.</p>
<ol>
<li>The shell of rock above the body (outer thickness \(d\)) gives zero net field inside it (shell theorem).</li>
<li>Only the inner sphere of radius \(R-d\) pulls. Its mass is \(M' = M\dfrac{(R-d)^3}{R^3}\), because mass scales with volume at fixed density.</li>
<li>\(g_d = \dfrac{GM'}{(R-d)^2} = \dfrac{GM(R-d)}{R^3} = g\left(1-\dfrac dR\right)\). This result is exact for a uniform sphere, not an approximation.</li>
<li>At the centre (\(d = R\)), \(g = 0\).</li>
</ol>'''),
        ('Comparing height with depth, and the g–r graph', r'''<p>For the same small distance, going up reduces \(g\) twice as fast as going down: \(2h/R\) against \(d/R\). So \(g\) at a small height \(h\) equals \(g\) at depth \(d = 2h\).</p>
<p>Plot \(g\) against distance \(r\) from the centre. Inside, \(g = gr/R\) rises as a straight line from zero. Outside, \(g = gR^2/r^2\) falls as an inverse square. The peak is at the surface. Moving from the surface in either direction lowers \(g\).</p>
<p>The mass of a body never changes with location. Only its weight \(mg\) changes.</p>'''),
    ],
    formulas=[
        dict(title='Small-height approximation', formula=r'g_h\approx g\left(1-\frac{2h}{R}\right),\qquad \frac{\Delta g}{g}\approx\frac{2h}{R}',
             symbols='g surface gravity (m/s²); h height above surface (m); R Earth radius (m). Valid only for h ≪ R; use the exact (R/(R+h))² form otherwise.'),
        dict(title='Equal g at a height and a depth', formula=r'd = 2h\quad(h,\,d\ll R)',
             symbols='d depth (m) and h height (m) at which g has the same value; R Earth radius. Uses both first-order formulas, so both distances must be small compared with R.'),
    ],
    figure=dict(svg=_fig_g_vs_r(),
                caption=r'g against distance r from Earth’s centre for a uniform Earth. It rises linearly inside, peaks at the surface, and falls as 1/r² outside. At r = 2R it is g₀/4.'),
    traps=[r'The approximation \(g(1-2h/R)\) is for small heights only. When \(h\) is a sizeable fraction of \(R\) (such as \(R/2\) or \(R\)), use \(g(R/(R+h))^2\).',
           r'At equal small height and depth, \(g\) does not decrease by the same amount. The decrease at height is twice that at depth.'],
    exam=r'''<ul>
<li>“At what height does g become 64% (or 1/4, or 1/9) of its surface value?” (exact formula, take square roots)</li>
<li>“A body weighs 63 N on the surface. Find its weight at height R/2.” (exact formula)</li>
<li>“At what depth is g the same as at a height of 32 km?” (d = 2h)</li>
<li>“Which graph shows g against distance from the centre of the Earth?” (linear rise, then 1/r²)</li>
<li>Percentage change questions: “By what percent does g decrease at a height of 1% of R?” (2%)</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'At what height above the Earth’s surface does \(g\) fall to 64% of its surface value? Take \(R = 6400\) km.',
             steps=[r'64% is too large a change for the small-height formula, so use the exact form: \((R/(R+h))^2 = 0.64\).',
                    r'Take the square root: \(R/(R+h) = 0.8\).',
                    r'So \(R + h = R/0.8 = 1.25R\), giving \(h = 0.25R\).',
                    r'\(h = 0.25\times6400 = 1600\) km.'],
             answer=r'1600 km'),
        dict(tag='Ratio', q=r'Find the ratio of \(g\) at a height \(R\) above the surface to \(g\) at a depth \(R/2\) below the surface.',
             steps=[r'At height \(R\): \(g_h = g(R/2R)^2 = g/4\).',
                    r'At depth \(R/2\): \(g_d = g(1 - \tfrac12) = g/2\).',
                    r'Ratio: \((g/4)/(g/2) = 1/2\).'],
             answer=r'1 : 2'),
        dict(tag='Numerical', q=r'At what depth below the surface is \(g\) reduced by 1%? At what height is it reduced by 1%? Take \(R = 6400\) km.',
             steps=[r'Depth: \(\Delta g/g = d/R = 0.01\), so \(d = 64\) km. This is exact for a uniform Earth.',
                    r'Height: \(\Delta g/g \approx 2h/R = 0.01\), so \(h = 32\) km. The approximation holds because \(32 \ll 6400\).',
                    r'The height is half the depth, matching the rule \(d = 2h\).'],
             answer=r'Depth 64 km; height 32 km.'),
    ],
    practice=[
        dict(q=r'A body weighs 63 N on the surface of the Earth. Its weight at a height equal to half the Earth’s radius is',
             options=['31.5 N', '28 N', '42 N', '47.25 N'], answer=1, type='numerical',
             explanation=r'Use the exact formula: \(g_h = g(R/1.5R)^2 = 4g/9\). Weight \(= 63\times4/9 = 28\) N. The value 31.5 N halves the weight, which treats \(g\) as falling linearly. 47.25 N comes from \(g(1-h/R)\)-type thinking, and the small-height formula \(1-2h/R\) would give zero, which shows it fails here.'),
        dict(q=r'Which description matches the graph of \(g\) against distance \(r\) from the centre of a uniform spherical Earth?',
             options=[r'Constant inside, then falls as \(1/r^2\) outside',
                      r'Rises linearly from zero to a maximum at the surface, then falls as \(1/r^2\)',
                      r'Falls as \(1/r^2\) everywhere, infinite at the centre',
                      r'Rises linearly everywhere'], answer=1, type='graph',
             explanation=r'Inside, only the enclosed mass pulls, which gives \(g \propto r\) with \(g = 0\) at the centre. Outside, all the mass pulls like a point mass, so \(g \propto 1/r^2\). A constant inside would describe nothing physical here (a shell has zero field inside, not constant non-zero). An infinite value at the centre forgets that the enclosed mass shrinks to zero.'),
        dict(q=r'Statement I: For small equal distances \(x\), the decrease in \(g\) at height \(x\) equals the decrease at depth \(x\).<br>Statement II: The value of \(g\) is greatest at the Earth’s surface.',
             options=ST_OPTS, answer=2, type='statement',
             explanation=r'Statement I is false: at height the fractional decrease is \(2x/R\), at depth only \(x/R\). Statement II is true for a uniform Earth: moving either up or down from the surface lowers \(g\).'),
        dict(q=r'The ratio of \(g\) at depth \(d\) to \(g\) at the surface is 0.75. Taking \(R = 6400\) km, the depth is',
             options=['1600 km', '800 km', '4800 km', '3200 km'], answer=0, type='numerical',
             explanation=r'\(g_d/g = 1 - d/R = 0.75\), so \(d = R/4 = 1600\) km. 4800 km is the value of \(R - d\), the distance from the centre. 800 km would follow from wrongly using \(1 - 2d/R\), the height formula.'),
    ],
),
# =====================================================================
'gravitation-potential': dict(
    level='core',
    notes=[
        ('Derivation: potential energy is −GMm/r', r'''<p>Potential energy at distance \(r\) is the work done by an external agent to bring \(m\) slowly from infinity to \(r\).</p>
<ol>
<li>Measure \(x\) outward from \(M\). Gravity on \(m\) is \(-GMm/x^2\) (inward), so the agent applies \(+GMm/x^2\) (outward) to move it without speeding up.</li>
<li>\(W = \displaystyle\int_\infty^r \frac{GMm}{x^2}\,dx = \left[-\frac{GMm}{x}\right]_\infty^r = -\frac{GMm}{r}\). So \(U(r) = -\dfrac{GMm}{r}\).</li>
<li>A quicker check: gravity does positive work as \(m\) falls inward, so the system loses potential energy. Starting from zero at infinity, \(U\) must be negative everywhere else.</li>
</ol>
<p>The potential is \(V = U/m = -GM/r\) (J/kg). It is a scalar, so for several masses you simply add \(-Gm_i/r_i\) with signs; no directions are needed.</p>'''),
        ('Where mgh comes from', r'''<p>Lift a mass \(m\) from the surface to height \(h\):</p>
<p>\(\Delta U = GMm\left(\dfrac1R-\dfrac1{R+h}\right) = \dfrac{GMm\,h}{R(R+h)} = \dfrac{mgh}{1+h/R}\).</p>
<p>For \(h\ll R\) this reduces to \(mgh\). For \(h = R\) it gives \(mgR/2\), not \(mgR\). The familiar \(mgh\) is a near-surface approximation that assumes \(g\) stays constant.</p>'''),
        ('Systems of masses and the link to field', r'''<p>For several particles, the potential energy of the system is the sum over every pair: \(U = -\sum Gm_im_j/r_{ij}\). Three equal masses on an equilateral triangle of side \(a\) have three pairs, so \(U = -3Gm^2/a\). The work needed to pull them apart to infinity is \(+3Gm^2/a\).</p>
<p>Field is the negative slope of potential: \(E = -dV/dr\). Where \(V\) is flat (inside a shell, or at a maximum or minimum of \(V\)), the field is zero, even though \(V\) itself is not zero. On the axis of a ring of mass \(M\) and radius \(a\), \(V = -GM/\sqrt{a^2+x^2}\); at the centre \(V = -GM/a\) while the field is zero.</p>'''),
    ],
    formulas=[
        dict(title='Potential energy change on lifting through h', formula=r'\Delta U=\frac{mgh}{1+h/R}',
             symbols='ΔU increase in potential energy (J); m mass (kg); g surface gravity (m/s²); h height above surface (m); R Earth radius (m). Exact for a spherical Earth; becomes mgh when h ≪ R.'),
        dict(title='Potential energy of a system of particles', formula=r'U=-\sum_{\text{pairs}}\frac{Gm_im_j}{r_{ij}}',
             symbols='U total gravitational potential energy (J), zero when all particles are infinitely far apart; m_i, m_j masses (kg); r_ij separation of each pair (m). Count each pair once.'),
        dict(title='Potential on the axis of a ring', formula=r'V=-\frac{GM}{\sqrt{a^2+x^2}}',
             symbols='V potential (J/kg); M ring mass (kg); a ring radius (m); x distance from the ring centre along its axis (m). At x = 0, V = −GM/a while the field is zero.'),
    ],
    traps=[r'Raising a body to a height \(h = R\) needs \(mgR/2\), not \(mgR\). The formula \(mgh\) assumes \(g\) is constant over the climb.',
           r'Potential is a scalar. At the midpoint of two equal masses the fields cancel, but the potentials add: \(V = -2GM/(d/2)\), not zero.'],
    exam=r'''<ul>
<li>“Find the work done to raise a body of mass m from the surface to a height R (or 2R, 3R).” (use GMm(1/r₁ − 1/r₂))</li>
<li>“Find the gravitational potential energy of three/four masses at the corners of a triangle/square.” (sum over pairs)</li>
<li>“At the midpoint between two masses, which is zero: field, potential, both or neither?”</li>
<li>Graph questions: V against r, and reading field as the negative slope.</li>
<li>Dimensions or units of potential (J/kg, [L²T⁻²]).</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'Find the minimum work needed to raise a 100 kg body from the Earth’s surface to a height equal to the Earth’s radius. Take \(g = 10\) m/s² and \(R = 6.4\times10^6\) m.',
             steps=[r'\(W = \Delta U = GMm\left(\dfrac1R-\dfrac1{2R}\right) = \dfrac{GMm}{2R}\).',
                    r'Replace \(GM\) by \(gR^2\): \(W = \dfrac{mgR}{2}\).',
                    r'\(W = \dfrac{100\times10\times6.4\times10^6}{2} = 3.2\times10^9\) J.',
                    r'Using \(mgh\) would give \(6.4\times10^9\) J, double the true value, because \(g\) weakens during the climb.'],
             answer=r'\(3.2\times10^9\) J'),
        dict(tag='Numerical', q=r'Three particles of mass 1 kg each sit at the corners of an equilateral triangle of side 1 m. How much work is needed to separate them to infinite distances from each other? (\(G = 6.67\times10^{-11}\) N m² kg⁻²)',
             steps=[r'There are three pairs, each at separation 1 m.',
                    r'\(U = -3\,G(1)(1)/1 = -3G = -2.0\times10^{-10}\) J.',
                    r'Final energy at infinity is zero, so the work needed is \(0 - U = 2.0\times10^{-10}\) J.'],
             answer=r'\(2.0\times10^{-10}\) J (that is, \(3G\) joules)'),
        dict(tag='Conceptual', q=r'Two equal masses \(M\) are a distance \(d\) apart. At the midpoint, find the field and the potential.',
             steps=[r'Field: each mass pulls toward itself with \(GM/(d/2)^2\). The pulls are opposite, so the field is zero.',
                    r'Potential: each contributes \(-GM/(d/2) = -2GM/d\). Scalars add with sign.',
                    r'Total \(V = -4GM/d\). Zero field does not mean zero potential.'],
             answer=r'Field zero; potential \(-4GM/d\).'),
    ],
    practice=[
        dict(q=r'The work done to move a body of mass \(m\) from the Earth’s surface to a height \(3R\) above the surface is',
             options=[r'\(3mgR\)', r'\(\tfrac34 mgR\)', r'\(\tfrac13 mgR\)', r'\(\tfrac14 mgR\)'], answer=1, type='numerical',
             explanation=r'Final distance from the centre is \(4R\). \(W = GMm(1/R - 1/4R) = \tfrac34 GMm/R = \tfrac34 mgR\). \(3mgR\) applies \(mgh\) with constant \(g\). \(\tfrac14 mgR\) uses only the final term \(GMm/4R\).'),
        dict(q=r'Which of these statements about gravitational potential \(V\) are correct?<br>(a) \(V\) is a scalar.<br>(b) The field equals \(-dV/dr\).<br>(c) \(V\) is zero at infinity by the usual convention.<br>(d) \(V\) is positive near the Earth.',
             options=['(a), (b) and (c) only', '(a) and (d) only', '(b) and (d) only', 'All four'], answer=0, type='multi',
             explanation=r'(a), (b) and (c) are standard. (d) is wrong: with zero at infinity and an attractive force, \(V = -GM/r\) is negative everywhere at finite distance. Any option containing (d) is therefore wrong.'),
        dict(q=r'The gravitational potential on the Earth’s surface is \(V_0\). The potential at a height equal to the Earth’s radius is',
             options=[r'\(V_0/4\)', r'\(2V_0\)', r'\(V_0/2\)', r'\(V_0\)'], answer=2, type='numerical',
             explanation=r'\(V = -GM/r\), so doubling \(r\) halves \(V\): \(V_0/2\) (less negative). \(V_0/4\) is the answer for the field \(g\), which goes as \(1/r^2\). \(2V_0\) would make the potential more negative farther out, which is backwards.'),
        dict(q=r'Four particles, each of mass \(m\), are at the corners of a square of side \(a\). The gravitational potential energy of the system is',
             options=[r'\(-\dfrac{Gm^2}{a}\left(4+\sqrt2\right)\)', r'\(-\dfrac{4Gm^2}{a}\)', r'\(-\dfrac{Gm^2}{a}\left(4+2\sqrt2\right)\)', r'\(-\dfrac{6Gm^2}{a}\)'], answer=0, type='numerical',
             explanation=r'There are 6 pairs: 4 sides of length \(a\) and 2 diagonals of length \(\sqrt2a\). \(U = -Gm^2(4/a + 2/(\sqrt2a)) = -(Gm^2/a)(4+\sqrt2)\). \(-4Gm^2/a\) forgets the diagonals. \(-6Gm^2/a\) treats the diagonals as length \(a\). \(4+2\sqrt2\) multiplies by \(\sqrt2\) instead of dividing.'),
    ],
),
# =====================================================================
'gravitation-orbits': dict(
    level='exam',
    notes=[
        ('Derivation: orbital speed and period', r'''<p>For a circular orbit of radius \(r = R + h\), gravity provides the centripetal force:</p>
<ol>
<li>\(\dfrac{mv^2}{r} = \dfrac{GMm}{r^2}\), so \(v_o = \sqrt{\dfrac{GM}{r}} = \sqrt{\dfrac{gR^2}{R+h}}\).</li>
<li>Period: \(T = \dfrac{2\pi r}{v_o} = 2\pi\sqrt{\dfrac{r^3}{GM}}\).</li>
<li>Close to the surface (\(h \ll R\)): \(v_o \approx \sqrt{gR}\approx 8\) km/s and \(T \approx 2\pi\sqrt{R/g}\approx 84\) minutes with \(g = 10\) m/s² and \(R = 6400\) km.</li>
</ol>
<p>The satellite mass \(m\) cancels. Two satellites in the same orbit have the same speed and period whatever their masses.</p>'''),
        ('Energies of a satellite', r'''<p>With \(v_o^2 = GM/r\):</p>
<ul>
<li>Kinetic energy \(K = \tfrac12mv_o^2 = +\dfrac{GMm}{2r}\).</li>
<li>Potential energy \(U = -\dfrac{GMm}{r}\).</li>
<li>Total energy \(E = K + U = -\dfrac{GMm}{2r}\).</li>
</ul>
<p>So \(K : U : E = 1 : -2 : -1\). The binding energy (energy needed to free the satellite from its orbit) is \(+GMm/2r = K\).</p>
<p>A higher orbit has <em>less</em> kinetic energy but <em>more</em> total energy (\(E\) is less negative). That is why moving a satellite outward needs energy: \(\Delta E = \dfrac{GMm}{2}\left(\dfrac1{r_1}-\dfrac1{r_2}\right)\). Launching from the surface (ignoring Earth’s rotation) into an orbit of radius \(r\) needs \(E_{\rm orbit} - U_{\rm surface} = GMm\left(\dfrac1R - \dfrac1{2r}\right)\).</p>'''),
        ('Dependence on r and what changes the orbit', r'''<p>Scaling rules for circular orbits around the same planet: \(v_o \propto r^{-1/2}\), \(T \propto r^{3/2}\), \(K \propto 1/r\), \(|E| \propto 1/r\), angular momentum \(L = m\sqrt{GMr} \propto r^{1/2}\).</p>
<ul>
<li>If gravity were switched off, the satellite would fly off along the tangent with speed \(v_o\).</li>
<li>If its speed is raised to \(\sqrt2\,v_o\) (about 41.4% more), it escapes.</li>
<li>Speed between \(v_o\) and \(\sqrt2\,v_o\): an ellipse, with the starting point as the nearest point. Speed less than \(v_o\): an ellipse with the starting point as the farthest point; near the Earth it may hit the ground.</li>
</ul>'''),
    ],
    formulas=[
        dict(title='Orbit just above the surface', formula=r'v_o\approx\sqrt{gR}\approx 8\ \text{km/s},\qquad T_0=2\pi\sqrt{R/g}\approx 84\ \text{min}',
             symbols='v_o orbital speed (m/s); T₀ period (s); g surface gravity (m/s²); R Earth radius (m). Numbers use g = 10 m/s² and R = 6.4×10⁶ m, and ignore air drag.'),
        dict(title='Energy to shift between circular orbits', formula=r'\Delta E=\frac{GMm}{2}\left(\frac1{r_1}-\frac1{r_2}\right)',
             symbols='ΔE energy that must be supplied (J); G constant; M planet mass and m satellite mass (kg); r₁ initial and r₂ final orbit radii (m), measured from the planet’s centre. Positive when r₂ > r₁.'),
        dict(title='Angular momentum in a circular orbit', formula=r'L=mv_or=m\sqrt{GMr}',
             symbols='L angular momentum about the planet’s centre (kg m²/s); m satellite mass (kg); v_o orbital speed (m/s); r orbit radius (m); G constant; M planet mass (kg).'),
    ],
    figure=dict(svg=_fig_orbit_energy(),
                caption=r'Energies of a satellite against orbit radius r. K is positive, U is negative and twice as large, and E = −K. As r grows, all three approach zero, so E increases (becomes less negative) even though K falls.'),
    traps=[r'A higher orbit has lower speed and lower kinetic energy, but higher (less negative) total energy. “Higher orbit, less energy” is wrong.',
           r'Orbital speed and period do not depend on the satellite’s mass, but its energies and angular momentum do.'],
    exam=r'''<ul>
<li>“Find the orbital speed and period of a satellite at height h = R (or h = 3R).” (use r = R + h)</li>
<li>“The kinetic energy of a satellite is K. Find its total energy, potential energy, or the energy needed to make it escape.” (1 : −2 : −1)</li>
<li>Ratio questions: “Two satellites at radii r and 4r. Find the ratio of speeds, periods, kinetic energies.”</li>
<li>“What happens if the satellite’s speed is suddenly increased by 41.4% / gravity disappears?”</li>
<li>Match-the-column questions linking v, T, K, E and L with powers of r.</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A satellite orbits at a height equal to the Earth’s radius. Find its orbital speed and period. Take \(g = 10\) m/s² and \(R = 6.4\times10^6\) m.',
             steps=[r'Orbit radius \(r = 2R\).',
                    r'\(v_o = \sqrt{gR^2/2R} = \sqrt{gR/2} = \sqrt{3.2\times10^7} \approx 5.66\times10^3\) m/s.',
                    r'\(T = 2\pi\sqrt{r^3/(gR^2)} = 2\pi\sqrt{8R/g} = 2\pi\sqrt{5.12\times10^6}\approx 1.42\times10^4\) s.',
                    r'That is about 3.95 hours, roughly \(2\sqrt2\) times the 84-minute near-surface period, as \(T\propto r^{3/2}\) predicts.'],
             answer=r'About 5.66 km/s and about 1.42×10⁴ s (3.95 h).'),
        dict(tag='Ratio', q=r'Satellite A (mass \(m\)) orbits at radius \(r\). Satellite B (mass \(2m\)) orbits the same planet at radius \(2r\). Compare their kinetic energies and their speeds.',
             steps=[r'\(K = GMm/2r\), so \(K\propto m/r\).',
                    r'\(K_A/K_B = (m/r)/(2m/2r) = 1\). Their kinetic energies are equal.',
                    r'Speed depends only on \(r\): \(v_A/v_B = \sqrt{2r/r} = \sqrt2\).',
                    r'Equal kinetic energy does not mean equal speed when the masses differ.'],
             answer=r'\(K_A = K_B\); \(v_A/v_B = \sqrt2\).'),
        dict(tag='Numerical', q=r'How much energy is needed to move a 1000 kg satellite from a circular orbit of radius \(2R\) to one of radius \(3R\)? Take \(g = 10\) m/s², \(R = 6.4\times10^6\) m.',
             steps=[r'\(\Delta E = \dfrac{GMm}{2}\left(\dfrac1{2R}-\dfrac1{3R}\right) = \dfrac{GMm}{12R}\).',
                    r'Use \(GM = gR^2\): \(\Delta E = mgR/12\).',
                    r'\(\Delta E = 1000\times10\times6.4\times10^6/12 \approx 5.33\times10^9\) J.'],
             answer=r'About \(5.33\times10^9\) J'),
    ],
    practice=[
        dict(q=r'A satellite in a circular orbit has kinetic energy \(K\). The minimum extra energy that must be given to it so that it escapes the planet’s gravity is',
             options=[r'\(K/2\)', r'\(2K\)', r'\(3K\)', r'\(K\)'], answer=3, type='numerical',
             explanation=r'Total energy in orbit is \(E = -K\). To escape, total energy must reach zero, so the energy needed is \(K\). \(2K\) is the size of the potential energy, which is the answer only for a body at rest at that radius.'),
        dict(q=r'Match each quantity for a circular orbit (List I) with how it depends on the orbit radius \(r\) (List II).<br>List I: (P) orbital speed (Q) period (R) kinetic energy (S) angular momentum<br>List II: (1) \(r^{-1}\) (2) \(r^{1/2}\) (3) \(r^{-1/2}\) (4) \(r^{3/2}\)',
             options=['P-3, Q-4, R-1, S-2', 'P-2, Q-4, R-1, S-3', 'P-3, Q-2, R-4, S-1', 'P-1, Q-4, R-3, S-2'], answer=0, type='match',
             explanation=r'\(v = \sqrt{GM/r}\propto r^{-1/2}\); \(T\propto r^{3/2}\); \(K = GMm/2r\propto r^{-1}\); \(L = m\sqrt{GMr}\propto r^{1/2}\). The second option swaps speed and angular momentum, a common slip because both involve a square root.'),
        dict(q=r'Two satellites orbit the Earth at radii \(r\) and \(4r\). The ratio of their orbital speeds \(v_1 : v_2\) is',
             options=['1 : 2', '2 : 1', '4 : 1', '1 : 4'], answer=1, type='numerical',
             explanation=r'\(v\propto r^{-1/2}\), so \(v_1/v_2 = \sqrt{4r/r} = 2\). The inner satellite is faster. 4 : 1 forgets the square root, and the reversed ratios put the faster satellite outside.'),
        dict(q=r'If the gravitational pull on a satellite in a circular orbit suddenly disappeared, the satellite would',
             options=['Fall vertically to the Earth', 'Continue in the same orbit', 'Move along the tangent to its orbit with its orbital speed', 'Spiral outward slowly'], answer=2, type='concept',
             explanation=r'With no force, Newton’s first law applies: it keeps the velocity it had, which is tangential. It cannot fall because nothing pulls it, and it cannot keep circling because the circle needs a centripetal force. Spiralling outward would need a continuous force.'),
    ],
),
# =====================================================================
'gravitation-escape': dict(
    level='exam',
    notes=[
        ('Derivation: escape speed from energy', r'''<p>A body launched with speed \(v\) from a planet’s surface just escapes if it reaches infinity with zero speed. Total energy at infinity is then zero, so at launch:</p>
<ol>
<li>\(\tfrac12mv_e^2 - \dfrac{GMm}{R} = 0\).</li>
<li>\(v_e = \sqrt{\dfrac{2GM}{R}} = \sqrt{2gR}\).</li>
<li>For Earth with \(g = 9.8\) m/s² and \(R = 6.4\times10^6\) m, \(v_e = 11.2\) km/s. With \(g = 10\) it is about 11.3 km/s.</li>
<li>Using \(M = \tfrac43\pi R^3\rho\): \(v_e = R\sqrt{\dfrac{8\pi G\rho}{3}}\), so at equal density \(v_e\propto R\).</li>
</ol>
<p>The launch direction does not matter (ignoring air and rotation), because energy is a scalar. The mass of the body cancels.</p>'''),
        ('Launched slower or faster than escape speed', r'''<ul>
<li><strong>Slower (vertical launch).</strong> It rises to height \(h\) where its speed is zero: \(\tfrac12mv^2 - \dfrac{GMm}{R} = -\dfrac{GMm}{R+h}\). This gives \(h = \dfrac{Rv^2}{v_e^2 - v^2}\). At \(v = v_e/2\), \(h = R/3\). At \(v = v_e/\sqrt2\), \(h = R\).</li>
<li><strong>Faster.</strong> It escapes with leftover speed \(v_\infty = \sqrt{v^2 - v_e^2}\) far away. Launched at \(2v_e\), it keeps \(\sqrt3\,v_e\).</li>
<li><strong>From an orbit.</strong> At radius \(r\), \(v_e = \sqrt{2GM/r} = \sqrt2\,v_o\). A satellite needs only \(\sqrt2 - 1\approx 41.4\%\) more speed to escape.</li>
</ul>'''),
        ('Why the Moon has no atmosphere', r'''<p>Escape speed on the Moon is only about 2.4 km/s. Gas molecules at the Moon’s daytime temperatures move with average speeds that are a sizeable fraction of this, and the fastest molecules in the distribution exceed it. Over long times, the gas leaks away. Earth’s larger escape speed keeps nitrogen and oxygen, though even Earth has lost most of its light hydrogen and helium.</p>'''),
    ],
    formulas=[
        dict(title='Escape speed in terms of density', formula=r'v_e=R\sqrt{\frac{8\pi G\rho}{3}}',
             symbols='v_e escape speed (m/s); R planet radius (m); G gravitational constant; ρ mean density (kg/m³). Assumes a spherical planet, no air resistance and no rotation.'),
        dict(title='Maximum height for a vertical launch below escape speed', formula=r'h=\frac{Rv^2}{v_e^2-v^2}\qquad(v<v_e)',
             symbols='h greatest height above the surface (m); R planet radius (m); v launch speed (m/s); v_e surface escape speed (m/s). Exact for a spherical planet without air; reduces to v²/2g when v ≪ v_e.'),
        dict(title='Speed left far away', formula=r'v_\infty=\sqrt{v^2-v_e^2}\qquad(v>v_e)',
             symbols='v_∞ speed at a very large distance (m/s); v launch speed (m/s); v_e escape speed from the launch point (m/s). Energy conservation with only the planet’s gravity acting.'),
    ],
    traps=[r'Escape speed does not depend on the angle of projection. A body thrown at 45° with \(v_e\) still escapes (ignoring air and rotation).',
           r'Do not use \(v^2 = 2gh\) to find how high a body rises when \(v\) is comparable to \(v_e\). Gravity weakens with height; use energy with \(-GMm/r\).'],
    exam=r'''<ul>
<li>Ratio questions: “Planet with twice the mass and half the radius of Earth. Find escape speed.” (v_e ∝ √(M/R))</li>
<li>“Same density, twice the radius.” (v_e ∝ R)</li>
<li>“A body is projected vertically with half the escape speed. How high does it go?” (R/3)</li>
<li>“A body is projected with twice the escape speed. Find its speed far away.” (√3 v_e)</li>
<li>Concept checks: dependence on mass and angle, relation v_e = √2 v_o, why the Moon has no atmosphere.</li>
</ul>''',
    examples=[
        dict(tag='Ratio', q=r'A planet has the same mean density as Earth but twice its radius. Find the escape speed from its surface. Earth’s escape speed is 11.2 km/s.',
             steps=[r'\(v_e = R\sqrt{8\pi G\rho/3}\), so at equal density \(v_e\propto R\).',
                    r'\(v_e = 2\times11.2 = 22.4\) km/s.',
                    r'Check another way: \(M\propto R^3\) gives \(M = 8M_E\), and \(v_e\propto\sqrt{M/R} = \sqrt{8/2} = 2\). Same answer.'],
             answer=r'22.4 km/s'),
        dict(tag='Numerical', q=r'A body is projected vertically upward from the Earth’s surface with half the escape speed. How high does it rise? Take \(R = 6400\) km.',
             steps=[r'Energy: \(\tfrac12m(v_e/2)^2 - GMm/R = -GMm/(R+h)\).',
                    r'With \(\tfrac12mv_e^2 = GMm/R\), the first term is \(\tfrac14\,GMm/R\). So \(-\tfrac34\,GMm/R = -GMm/(R+h)\).',
                    r'\(R + h = \tfrac43R\), so \(h = R/3\approx 2133\) km.',
                    r'The constant-\(g\) formula \(v^2/2g\) would give \(R/4 = 1600\) km, an underestimate, because it ignores the weakening of gravity.'],
             answer=r'\(R/3\), about 2133 km'),
        dict(tag='Numerical', q=r'A probe is launched from Earth’s surface with twice the escape speed (\(v_e = 11.2\) km/s). Ignoring air and other bodies, what is its speed far from Earth?',
             steps=[r'Energy conservation between the surface and infinity: \(\tfrac12mv^2 - GMm/R = \tfrac12mv_\infty^2\).',
                    r'Since \(GMm/R = \tfrac12mv_e^2\): \(v_\infty^2 = v^2 - v_e^2 = 4v_e^2 - v_e^2 = 3v_e^2\).',
                    r'\(v_\infty = \sqrt3\times11.2\approx 19.4\) km/s. Not \(v_e\): the subtraction is of squares, not speeds.'],
             answer=r'About 19.4 km/s (\(\sqrt3\,v_e\))'),
    ],
    practice=[
        dict(q=r'A planet has 8 times the mass and twice the radius of the Earth. If the escape speed from Earth is 11.2 km/s, the escape speed from the planet is',
             options=['11.2 km/s', '22.4 km/s', '44.8 km/s', '5.6 km/s'], answer=1, type='numerical',
             explanation=r'\(v_e = \sqrt{2GM/R}\propto\sqrt{M/R} = \sqrt{8/2} = 2\), giving 22.4 km/s. 44.8 km/s forgets the square root. 11.2 km/s would hold only if \(M/R\) were unchanged.'),
        dict(q=r'A body is projected vertically upward from the Earth’s surface with speed \(v_e/\sqrt2\), where \(v_e\) is the escape speed. Neglecting air resistance, it rises to a height of',
             options=[r'\(R/2\)', r'\(2R\)', r'\(R/4\)', r'\(R\)'], answer=3, type='numerical',
             explanation=r'\(h = Rv^2/(v_e^2 - v^2) = R(v_e^2/2)/(v_e^2/2) = R\). \(R/2\) comes from the constant-\(g\) formula \(v^2/2g = (2gR/2)/2g\), which fails at such large heights.'),
        dict(q=r'The escape speed of a body projected vertically from the Earth is \(v_e\). If it is instead projected at 60° to the vertical, the escape speed is',
             options=[r'\(v_e/2\)', r'\(v_e\)', r'\(2v_e\)', r'\(v_e\sqrt3/2\)'], answer=1, type='concept',
             explanation=r'Escape depends only on total energy, a scalar. The same launch speed gives the same kinetic energy in any direction, so the threshold is still \(v_e\). The other options wrongly resolve the speed into components.'),
        dict(q=r'Assertion (A): The Moon has practically no atmosphere.<br>Reason (R): The escape speed on the Moon is small, so gas molecules there can escape over time.',
             options=AR_OPTS, answer=0, type='ar',
             explanation=r'Both are true and R explains A. The Moon’s escape speed (about 2.4 km/s) is low enough that a significant share of gas molecules exceeds it, so any atmosphere leaks away. Option 2 would be right only if the reason were true but unrelated.'),
    ],
),
# =====================================================================
'gravitation-kepler': dict(
    level='core',
    notes=[
        ('The three laws in plain words', r'''<ol>
<li><strong>Law of orbits.</strong> Each planet moves in an ellipse with the Sun at one focus (not at the centre).</li>
<li><strong>Law of areas.</strong> The line from the Sun to the planet sweeps equal areas in equal times. The planet moves fastest at perihelion (nearest point) and slowest at aphelion (farthest point).</li>
<li><strong>Law of periods.</strong> \(T^2\propto a^3\), where \(a\) is the semi-major axis, \(a = (r_{\min}+r_{\max})/2\).</li>
</ol>'''),
        ('Derivations NEET expects', r'''<p><strong>Third law for a circular orbit.</strong> Gravity provides the centripetal force: \(\dfrac{GMm}{r^2} = m\left(\dfrac{2\pi}{T}\right)^2r\). Rearranging, \(T^2 = \dfrac{4\pi^2}{GM}r^3\). For an ellipse, the same result holds with \(r\) replaced by \(a\).</p>
<p><strong>Second law from angular momentum.</strong> In a short time \(dt\), the radius sweeps a thin triangle of area \(dA = \tfrac12 r\,(v\,dt)\sin\theta\). So \(\dfrac{dA}{dt} = \dfrac{|\vec r\times\vec v|}{2} = \dfrac{L}{2m}\). Gravity is a central force, so its torque about the Sun is zero and \(L\) is constant. Hence the areal speed is constant. At perihelion and aphelion the velocity is perpendicular to the radius, giving \(v_pr_p = v_ar_a\).</p>'''),
        ('Geostationary and polar satellites', r'''<p>A geostationary satellite appears fixed in the sky. It needs all of these: a circular orbit in the equatorial plane, a period of 24 h (strictly one sidereal day, about 23 h 56 min), and motion from west to east, like the Earth’s spin. From \(T^2\propto r^3\) its orbit radius is about 42,000 km (about 6.6 Earth radii), a height of about 36,000 km, with speed about 3.1 km/s. It is used for communication and weather monitoring.</p>
<p>A polar satellite passes over the poles at a low height (roughly 500–800 km) with a period of about 100 minutes. The Earth turns beneath it, so it scans the whole surface. It is used for remote sensing and mapping.</p>'''),
    ],
    formulas=[
        dict(title='Perihelion and aphelion speeds', formula=r'v_pr_p=v_ar_a\quad\Rightarrow\quad\frac{v_p}{v_a}=\frac{r_a}{r_p}',
             symbols='v_p, v_a speeds at the nearest and farthest points (m/s); r_p, r_a distances of those points from the Sun (m). Uses conservation of angular momentum; velocity is perpendicular to the radius only at these two points.'),
        dict(title='Areal velocity', formula=r'\frac{dA}{dt}=\frac{L}{2m}=\text{constant}',
             symbols='dA/dt area swept per unit time (m²/s); L angular momentum about the Sun (kg m²/s); m planet mass (kg). Holds for any central force.'),
        dict(title='Comparing two orbits', formula=r'\frac{T_2}{T_1}=\left(\frac{a_2}{a_1}\right)^{3/2}',
             symbols='T₁, T₂ periods (any consistent unit); a₁, a₂ semi-major axes (or circular radii) (any consistent unit). Both bodies must orbit the same central mass.'),
    ],
    figure=dict(svg=_fig_kepler(),
                caption=r'An elliptical orbit with the Sun at one focus. The two shaded regions have equal area and are swept in equal times, so the planet covers a longer arc near perihelion P than near aphelion A.'),
    traps=[r'Use the semi-major axis \(a = (r_{\min}+r_{\max})/2\) in \(T^2\propto a^3\), not the largest distance.',
           r'Equal areas in equal times does not mean constant speed. The areal speed is constant; the actual speed changes along an ellipse.'],
    exam=r'''<ul>
<li>“The distance of a planet from the Sun is doubled. Find the new period.” (2^(3/2) = 2√2 times)</li>
<li>“Speeds at perihelion and aphelion are in what ratio?” (inverse of the distances)</li>
<li>Graph: “log T against log r is a straight line of slope 3/2.”</li>
<li>Statement or assertion–reason: “Kepler’s second law is a consequence of conservation of angular momentum.”</li>
<li>Conditions for a geostationary satellite; period of a satellite at a given fraction of the geostationary radius.</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A comet’s nearest distance from the Sun is \(1.0\times10^{11}\) m and its farthest is \(1.5\times10^{11}\) m. Its speed at the nearest point is \(3\times10^4\) m/s. Find its speed at the farthest point.',
             steps=[r'At these two points the velocity is perpendicular to the radius, so angular momentum gives \(v_pr_p = v_ar_a\).',
                    r'\(v_a = v_p\,r_p/r_a = 3\times10^4\times1.0/1.5\).',
                    r'\(v_a = 2\times10^4\) m/s.'],
             answer=r'\(2\times10^4\) m/s'),
        dict(tag='Ratio', q=r'A geostationary satellite has a period of 24 h. Find the period of a satellite whose orbit radius is one quarter of the geostationary radius.',
             steps=[r'Both orbit the Earth, so \(T\propto r^{3/2}\).',
                    r'\(T = 24\times(1/4)^{3/2} = 24\times1/8\).',
                    r'\(T = 3\) h.'],
             answer=r'3 hours'),
        dict(tag='Graph', q=r'For the planets of the Solar System, \(\log T\) is plotted against \(\log a\). What shape is the graph and what is its slope?',
             steps=[r'Kepler’s third law: \(T = Ca^{3/2}\) with \(C = 2\pi/\sqrt{GM}\).',
                    r'Take logs: \(\log T = \tfrac32\log a + \log C\).',
                    r'This is a straight line with slope 3/2 and intercept \(\log C\). A plot of \(T^2\) against \(a^3\) is a straight line through the origin.'],
             answer=r'A straight line of slope 3/2.'),
    ],
    practice=[
        dict(q=r'For satellites orbiting the same planet, a graph of \(\log T\) (vertical) against \(\log r\) (horizontal) is a straight line with slope',
             options=['2/3', '3/2', '2', '3'], answer=1, type='graph',
             explanation=r'\(T\propto r^{3/2}\), so \(\log T = \tfrac32\log r + \text{constant}\). The slope 2/3 belongs to \(\log r\) against \(\log T\). Slopes 2 and 3 come from mistaking the exponents in \(T^2\propto r^3\).'),
        dict(q=r'A planet’s nearest and farthest distances from a star are 2 AU and 6 AU. The Earth orbits the same star at 1 AU in 1 year (circular orbit). The planet’s period is',
             options=['8 years', r'\(6\sqrt6\) years', '64 years', r'\(2\sqrt2\) years'], answer=0, type='numerical',
             explanation=r'Semi-major axis \(a = (2+6)/2 = 4\) AU. \(T = 1\times4^{3/2} = 8\) years. Using the farthest distance gives \(6^{3/2} = 6\sqrt6\). 64 years is \(4^3\), forgetting the square root.'),
        dict(q=r'Statement I: Kepler’s second law follows from conservation of angular momentum.<br>Statement II: The gravitational force of the Sun on a planet has zero torque about the Sun.',
             options=ST_OPTS, answer=0, type='statement',
             explanation=r'Both are true. The force acts along the line joining the planet and the Sun, so \(\vec r\times\vec F = 0\). Zero torque conserves \(L\), and \(dA/dt = L/2m\) is then constant.'),
        dict(q=r'Which set of conditions is required for a geostationary satellite?<br>(a) Orbit in the equatorial plane (b) Period of about 24 h (c) Motion from west to east (d) Orbit passing over both poles',
             options=['(a) and (b) only', '(b), (c) and (d)', '(a), (b) and (c)', '(b) only'], answer=2, type='multi',
             explanation=r'It must be equatorial, have the Earth’s rotation period and move in the same sense as the Earth (west to east). A 24 h period alone is not enough: a tilted 24 h orbit drifts north and south in the sky. A polar orbit (d) is the opposite case.'),
    ],
),
# =====================================================================
'gravitation-spherical': dict(
    level='exam',
    notes=[
        ('Thin shell: field and potential', r'''<p>For a uniform thin shell of mass \(M\) and radius \(R\):</p>
<ul>
<li><strong>Outside</strong> (\(r > R\)): it acts like a point mass at the centre. \(E = GM/r^2\), \(V = -GM/r\).</li>
<li><strong>Inside</strong> (\(r < R\)): \(E = 0\) everywhere. The potential is constant and equal to its surface value, \(V = -GM/R\).</li>
</ul>
<p>The field jumps from 0 just inside to \(GM/R^2\) just outside. The potential is continuous, with a flat piece inside joined to the \(-GM/r\) curve outside. A body inside a shell feels no force from the shell, but work is still needed to take it to infinity.</p>'''),
        ('Uniform solid sphere: field and potential', r'''<ul>
<li><strong>Outside</strong>: same as a point mass, \(E = GM/r^2\), \(V = -GM/r\).</li>
<li><strong>Inside</strong>: only the mass within radius \(r\) pulls, \(M r^3/R^3\). So \(E = GMr/R^3\), rising linearly from zero at the centre to \(GM/R^2\) at the surface.</li>
<li>Inside potential: \(V = -\dfrac{GM}{2R^3}(3R^2 - r^2)\). It is a downward parabola, most negative at the centre, \(V_{\rm centre} = -\dfrac{3GM}{2R} = 1.5\,V_{\rm surface}\).</li>
</ul>
<p>Unlike the shell, the solid sphere’s field graph is continuous with a peak at the surface. The field equals half its surface value at two places: \(r = R/2\) inside and \(r = \sqrt2R\) outside.</p>'''),
        ('Energy for moving inside a sphere', r'''<p>Moving a mass \(m\) from the centre of a uniform sphere to its surface raises its energy by \(m(V_{\rm surface} - V_{\rm centre}) = m\left(-\dfrac{GM}{R}+\dfrac{3GM}{2R}\right) = \dfrac{GMm}{2R}\). Reverse it: a body dropped from the surface down a frictionless tunnel through the centre reaches the centre with \(\tfrac12mv^2 = GMm/2R\), so \(v = \sqrt{GM/R} = \sqrt{gR}\), about 8 km/s for Earth. The Oscillations chapter shows this motion is simple harmonic.</p>
<p>Earth’s rotation and latitude also change the measured \(g\). That is treated in its own section, “Earth’s rotation and latitude”.</p>'''),
    ],
    formulas=[
        dict(title='Uniform thin shell', formula=r'r<R:\ E=0,\ V=-\frac{GM}{R};\qquad r\ge R:\ E=\frac{GM}{r^2},\ V=-\frac{GM}{r}',
             symbols='E field magnitude (N/kg); V potential (J/kg), zero at infinity; G constant; M shell mass (kg); R shell radius (m); r distance from centre (m). Thin uniform shell.'),
        dict(title='Potential at the centre of a solid sphere', formula=r'V_{\rm centre}=-\frac{3GM}{2R}=\frac32V_{\rm surface}',
             symbols='V potential (J/kg); G constant; M sphere mass (kg); R radius (m). Uniform density assumed.'),
    ],
    figure=dict(svg=_fig_shell_sphere(),
                caption=r'Left: field against r. A shell (coral) has zero field inside and a jump at R; a solid sphere (teal) rises linearly to a peak at R. Outside, both follow GM/r². Right: potential against r. The shell’s potential is flat inside at −GM/R; the solid sphere’s is a parabola reaching −3GM/2R at the centre.'),
    traps=[r'Inside a shell the potential is not zero. It is constant and equal to the surface value \(-GM/R\). Zero field means zero slope of \(V\), not zero \(V\).',
           r'A shell’s field graph jumps at \(r = R\); a solid sphere’s field graph is continuous with a peak at \(R\). Do not mix the two shapes.'],
    exam=r'''<ul>
<li>“Which graph shows the gravitational field (or potential) of a spherical shell / solid sphere against r?”</li>
<li>“At what distances from the centre is the field half its surface value?” (R/2 and √2 R for a solid sphere)</li>
<li>“Find the ratio of potential at the centre to that at the surface.” (3 : 2)</li>
<li>Assertion–reason on why the field inside a shell is zero while the potential is not.</li>
<li>“A particle is dropped into a tunnel through the centre. Find its speed at the centre.”</li>
</ul>''',
    examples=[
        dict(tag='Ratio', q=r'For a uniform solid sphere of mass \(M\) and radius \(R\), find the ratio of the field at \(r = R/2\) to the field at \(r = 2R\).',
             steps=[r'Inside: \(E(R/2) = GM(R/2)/R^3 = GM/(2R^2)\).',
                    r'Outside: \(E(2R) = GM/(2R)^2 = GM/(4R^2)\).',
                    r'Ratio: \((1/2)/(1/4) = 2\).'],
             answer=r'2 : 1'),
        dict(tag='Graph', q=r'A student draws the potential of a thin spherical shell as zero inside and \(-GM/r\) outside. What is wrong, and what does the correct graph look like?',
             steps=[r'The potential must be continuous at \(r = R\), because a finite amount of work moves a body across the surface. A jump from 0 to \(-GM/R\) is impossible.',
                    r'Inside, the field is zero, so \(dV/dr = 0\): the potential is constant.',
                    r'That constant must match the surface value \(-GM/R\).',
                    r'Correct graph: a horizontal line at \(-GM/R\) from \(r = 0\) to \(R\), then the curve \(-GM/r\) rising toward zero.'],
             answer=r'Inside, V is constant at −GM/R (not zero), joining smoothly to −GM/r outside.'),
        dict(tag='Numerical', q=r'How much work is needed to move a 2 kg mass from the centre of a uniform planet to its surface? The planet has \(GM/R = 6.4\times10^7\) J/kg.',
             steps=[r'\(V_{\rm centre} = -\tfrac32\,GM/R\) and \(V_{\rm surface} = -GM/R\).',
                    r'Work \(= m(V_{\rm surface} - V_{\rm centre}) = m\times\tfrac12\,GM/R\).',
                    r'\(W = 2\times\tfrac12\times6.4\times10^7 = 6.4\times10^7\) J.'],
             answer=r'\(6.4\times10^7\) J'),
    ],
    practice=[
        dict(q=r'Which describes the gravitational potential \(V\) against distance \(r\) from the centre of a uniform thin spherical shell?',
             options=[r'Zero inside, \(-GM/r\) outside',
                      r'Constant at \(-GM/R\) inside, \(-GM/r\) outside',
                      r'A parabola inside reaching \(-3GM/2R\) at the centre, \(-GM/r\) outside',
                      r'Increasing linearly inside, \(-GM/r\) outside'], answer=1, type='graph',
             explanation=r'Zero field inside means \(V\) is constant there, equal to its surface value. Option 1 confuses zero field with zero potential and breaks continuity. Option 3 describes a solid sphere, not a shell.'),
        dict(q=r'For a uniform solid sphere of radius \(R\), the gravitational field equals half its surface value at distances from the centre of',
             options=[r'\(R/2\) only', r'\(\sqrt2R\) only', r'\(R/2\) and \(2R\)', r'\(R/2\) and \(\sqrt2R\)'], answer=3, type='numerical',
             explanation=r'Inside: \(E\propto r\), so \(E = E_s/2\) at \(r = R/2\). Outside: \(E\propto1/r^2\), so \(E = E_s/2\) when \(r^2 = 2R^2\), \(r = \sqrt2R\). \(2R\) gives a quarter, not a half.'),
        dict(q=r'Assertion (A): A particle inside a uniform spherical shell experiences no gravitational force due to the shell.<br>Reason (R): The gravitational potential inside the shell is the same at every point.',
             options=AR_OPTS, answer=0, type='ar',
             explanation=r'Both are true, and R explains A: the field is \(-dV/dr\), and a constant potential has zero slope, so the field and force are zero. The potential being nonzero does not create a force; only its change does.'),
        dict(q=r'A particle is released from rest at the surface of a uniform planet into a smooth tunnel along a diameter. Its speed on reaching the centre is (\(g\) is the surface gravity, \(R\) the radius)',
             options=[r'\(\sqrt{2gR}\)', r'\(\sqrt{gR}\)', r'\(\sqrt{gR/2}\)', r'Zero'], answer=1, type='numerical',
             explanation=r'Energy: \(\tfrac12mv^2 = m(V_s - V_c) = GMm/2R\), so \(v = \sqrt{GM/R} = \sqrt{gR}\). \(\sqrt{2gR}\) uses \(v^2 = 2gR\), which assumes constant \(g\) all the way down, but \(g\) falls to zero at the centre.'),
    ],
),
}


NEW_SECTIONS = [
# =====================================================================
dict(chapter='gravitation', after='gravitation-variation', id='gravitation-rotation',
     title='Earth’s rotation and latitude',
     intro=r'Stand on a spinning roundabout and you feel thrown outward. The Earth spins too, once a day. A person at the equator travels in a large circle, so part of the Earth’s pull is used up keeping them on that circle. The scale under their feet reads a little less than the full gravitational pull. At the poles there is no circle to follow, so nothing is used up.',
     reasoning=r'A point at latitude \(\lambda\) moves in a circle of radius \(R\cos\lambda\) around the axis. It needs a centripetal acceleration \(\omega^2R\cos\lambda\) toward the axis. The part of this along the vertical, \(\omega^2R\cos^2\lambda\), is taken from \(g\). So the measured \(g\) is smallest at the equator and largest at the poles. The Earth’s bulge at the equator lowers it further there.',
     formula=r"g'=g-\omega^2R\cos^2\lambda",
     symbols='g′ effective (measured) gravity (m/s²); g gravity of a non-rotating spherical Earth (m/s²); ω Earth’s angular speed, 7.27×10⁻⁵ rad/s; R Earth radius (m); λ latitude (0° at the equator, 90° at the poles). The small ω⁴ term is neglected; at the equator the result is exact.',
     trap=r'Latitude is measured from the equator. At the equator \(\lambda = 0\), \(\cos\lambda = 1\), and the reduction is largest; at the poles it is zero.',
     example=r'By how much is \(g\) at the equator less than at the poles because of rotation alone? Take \(R = 6.4\times10^6\) m.',
     solution=r'\(\omega = 2\pi/86400 = 7.27\times10^{-5}\) rad/s. The reduction is \(\omega^2R = (7.27\times10^{-5})^2\times6.4\times10^6\approx0.034\) m/s², about 0.34% of \(g\).',
     question='If the Earth stopped rotating, the value of g would',
     options='Increase at the equator and stay the same at the poles|Decrease everywhere|Increase equally everywhere|Stay the same at the equator and increase at the poles',
     answer=0,
     explanation=r'The rotation term \(\omega^2R\cos^2\lambda\) would vanish. At the equator it is largest, so \(g\) rises there. At the poles \(\cos90° = 0\), so nothing changes.',
     deep=dict(
         level='core',
         notes=[
             ('Derivation: the latitude formula', r'''<ol>
<li>A point P at latitude \(\lambda\) is a distance \(r = R\cos\lambda\) from the spin axis.</li>
<li>To move in that circle, it needs a centripetal acceleration \(\omega^2R\cos\lambda\), directed toward the axis (horizontally inward in the figure).</li>
<li>Resolve this along the line to the Earth’s centre: the component is \(\omega^2R\cos\lambda\times\cos\lambda = \omega^2R\cos^2\lambda\).</li>
<li>Gravity \(g\) must supply this. What is left to press on the scale is \(g' \approx g - \omega^2R\cos^2\lambda\). A small sideways part (and an \(\omega^4\) term) is neglected.</li>
</ol>
<p>Checks: at the equator \(g' = g - \omega^2R\), at the poles \(g' = g\). With \(\omega^2R\approx0.034\) m/s², the effect is small but measurable.</p>'''),
             ('Shape of the Earth adds to the effect', r'''<p>The Earth bulges at the equator: the equatorial radius is about 21 km more than the polar radius. A point at the equator is therefore farther from the centre, which lowers \(GM/R^2\) as well. Both effects work the same way: measured \(g\) is about 9.78 m/s² at the equator and about 9.83 m/s² at the poles.</p>
<p>So a body weighs slightly more at the poles. Its mass is the same everywhere.</p>'''),
             ('How fast would Earth need to spin?', r'''<p>A body at the equator would feel weightless if \(\omega^2R = g\), that is, \(\omega = \sqrt{g/R}\). With \(g = 10\) m/s² and \(R = 6.4\times10^6\) m, \(\omega = 1.25\times10^{-3}\) rad/s, giving a day of \(2\pi/\omega\approx5030\) s, about 1.4 h, roughly 17 times faster than now. This is the same as the period of a satellite skimming the surface: a body at the equator would then be “in orbit” while standing on the ground.</p>
<p>For other latitudes the approximate formula is not reliable at such large \(\omega\), so NEET uses only the equator for this question.</p>'''),
         ],
         formulas=[
             dict(title='Reduction in g at latitude λ', formula=r'\Delta g=\omega^2R\cos^2\lambda',
                  symbols='Δg decrease in effective gravity due to rotation (m/s²); ω Earth’s angular speed (rad/s); R Earth radius (m); λ latitude. At the equator Δg = ω²R ≈ 0.034 m/s².'),
             dict(title='Spin rate for weightlessness at the equator', formula=r'\omega=\sqrt{\frac gR},\qquad T=2\pi\sqrt{\frac Rg}\approx 84\ \text{min}',
                  symbols='ω required angular speed (rad/s); T length of the day (s); g gravity (m/s²); R Earth radius (m). Uses g = 10 m/s² and R = 6.4×10⁶ m for the numerical value.'),
         ],
         figure=dict(svg=_fig_latitude(),
                     caption=r'A point P at latitude λ moves in a circle of radius R cos λ about the axis. It needs a centripetal acceleration ω²R cos λ toward the axis; its component along the radius, ω²R cos²λ, is taken out of g.'),
         traps=[r'Do not use \(\cos\lambda\) instead of \(\cos^2\lambda\). One cosine sets the circle’s radius; the second resolves the needed acceleration along the vertical.',
                r'Rotation does not change the true gravitational pull \(GMm/R^2\). It changes the apparent weight (the scale reading), because part of the pull provides centripetal force.'],
         exam=r'''<ul>
<li>“Where on Earth is g maximum / minimum?” (poles / equator)</li>
<li>“What happens to g at the equator and poles if the Earth stops rotating?”</li>
<li>“How fast must the Earth spin for bodies at the equator to feel weightless? Find the length of the day.” (about 84 min)</li>
<li>“Find the change in weight of a 60 kg person at the equator due to rotation.”</li>
<li>“At what latitude is the reduction one quarter of its equatorial value?” (cos²λ = 1/4, λ = 60°)</li>
</ul>''',
         examples=[
             dict(tag='Numerical', q=r'A 60 kg person stands at the equator. By how much does the Earth’s rotation reduce the reading of a weighing scale? Take \(R = 6.4\times10^6\) m and a day of 86,400 s.',
                  steps=[r'\(\omega = 2\pi/86400 = 7.27\times10^{-5}\) rad/s.',
                         r'\(\omega^2R = (7.27\times10^{-5})^2\times6.4\times10^6\approx0.0338\) m/s².',
                         r'Reduction in reading \(= m\omega^2R = 60\times0.0338\approx2.0\) N.',
                         r'Out of about 600 N, this is about 0.34%, small but real.'],
                  answer=r'About 2.0 N'),
             dict(tag='Ratio', q=r'At what latitude is the reduction in \(g\) due to rotation one quarter of its value at the equator?',
                  steps=[r'Reduction \(\propto\cos^2\lambda\); at the equator it is \(\omega^2R\).',
                         r'Set \(\cos^2\lambda = 1/4\), so \(\cos\lambda = 1/2\).',
                         r'\(\lambda = 60°\).'],
                  answer=r'60°'),
             dict(tag='Numerical', q=r'How long would a day be if bodies at the equator were to feel weightless? Take \(g = 10\) m/s², \(R = 6.4\times10^6\) m.',
                  steps=[r'Weightlessness at the equator: \(\omega^2R = g\), so \(\omega = \sqrt{10/6.4\times10^6} = 1.25\times10^{-3}\) rad/s.',
                         r'\(T = 2\pi/\omega\approx5027\) s.',
                         r'That is about 84 minutes, about 1/17 of the present day.'],
                  answer=r'About 5.0×10³ s (about 1.4 h)'),
         ],
         practice=[
             dict(q=r'The reduction in effective \(g\) due to Earth’s rotation at latitude 60° compared with that at the equator is',
                  options=['1/2', '1/4', r'\(\sqrt3/2\)', '3/4'], answer=1, type='numerical',
                  explanation=r'Reduction \(\propto\cos^2\lambda = \cos^260° = 1/4\). The choice 1/2 uses \(\cos\lambda\) only. \(\sqrt3/2\) and 3/4 use \(\sin\) instead of \(\cos\), mixing up latitude with the angle from the axis.'),
             dict(q=r'Statement I: A body weighs slightly more at the poles than at the equator.<br>Statement II: The mass of a body is slightly larger at the poles.',
                  options=ST_OPTS, answer=1, type='statement',
                  explanation=r'Statement I is true: rotation and the equatorial bulge both make \(g\) larger at the poles. Statement II is false: mass is the amount of matter and does not depend on location.'),
             dict(q=r'Because of the Earth’s rotation alone, the value of \(g\) at the equator is less than at the poles by about (\(R = 6.4\times10^6\) m, one day = 86,400 s)',
                  options=[r'\(3.4\times10^{-3}\) m/s²', r'0.34 m/s²', r'0.034 m/s²', r'9.8 m/s²'], answer=2, type='numerical',
                  explanation=r'\(\omega = 2\pi/86400 = 7.27\times10^{-5}\) rad/s and \(\omega^2R\approx0.034\) m/s², about 0.34% of \(g\). 0.34 m/s² confuses the percentage with the value. 9.8 m/s² is \(g\) itself, as if the Earth spun fast enough for weightlessness.'),
             dict(q=r'Assertion (A): If the Earth stopped rotating, the value of \(g\) at the poles would not change.<br>Reason (R): A body at a pole lies on the axis of rotation and needs no centripetal acceleration.',
                  options=AR_OPTS, answer=0, type='ar',
                  explanation=r'Both are true and R explains A. The rotation term \(\omega^2R\cos^2\lambda\) is zero at \(\lambda = 90°\) because the body moves in a circle of zero radius. At the equator, by contrast, stopping the rotation would raise \(g\) by about 0.034 m/s².'),
         ],
     )),
# =====================================================================
dict(chapter='gravitation', after='gravitation-orbits', id='gravitation-weightless',
     title='Weightlessness and apparent weight',
     intro=r'Jump off a wall and, for a moment, your stomach feels light. You are not losing gravity; you have simply stopped pushing on anything. The weight you feel is the push of the floor or a scale on you. When you and the floor fall together, that push disappears. Astronauts in orbit feel weightless for the same reason: they and their spacecraft are falling around the Earth together.',
     reasoning=r'Apparent weight is the normal force from the support. In a lift accelerating downward with \(a\), \(N = m(g-a)\). In free fall, \(a = g\) and \(N = 0\). In a circular orbit, gravity \(g_h\) at that height provides exactly the centripetal acceleration of both the craft and the astronaut. Neither pushes on the other, so the astronaut is weightless, even though gravity there is still about 89% of its surface value at 400 km.',
     formula=r'N=m(g_{\rm local}-a),\qquad a=g_{\rm local}\ \Rightarrow\ N=0',
     symbols='N apparent weight, the normal force from the support (N); m mass (kg); g_local gravitational field at that place (m/s²); a downward (or centre-directed) acceleration of the support (m/s²). Weightlessness means N = 0, not zero gravity.',
     trap=r'Astronauts in orbit are not weightless because gravity is absent. Gravity is what keeps them in orbit. They feel weightless because they are in free fall.',
     example=r'Find the value of \(g\) at the height of a space station 400 km above the Earth (\(R = 6400\) km), as a fraction of its surface value.',
     solution=r'\(g_h/g = (R/(R+h))^2 = (6400/6800)^2\approx0.886\). Gravity is still about 89% of its surface value; the astronauts feel weightless only because they are falling freely.',
     question='An astronaut floats inside an orbiting spacecraft because',
     options='There is no gravity in space|The astronaut and the spacecraft fall with the same acceleration|The Moon pulls the astronaut upward|The air inside supports the astronaut',
     answer=1,
     explanation=r'Both are in free fall with acceleration \(g_h\) toward the Earth, so the floor exerts no normal force. Gravity is still strong at that height, so “no gravity” is wrong.',
     deep=dict(
         level='core',
         notes=[
             ('What a weighing scale actually measures', r'''<p>A scale measures the normal force \(N\) between you and it. For a person in a lift with upward acceleration \(a\) (taking up as positive):</p>
<ul>
<li>At rest or moving at constant velocity: \(N = mg\).</li>
<li>Accelerating up (or slowing while moving down): \(N = m(g+a)\), you feel heavier.</li>
<li>Accelerating down (or slowing while moving up): \(N = m(g-a)\), you feel lighter.</li>
<li>Cable snaps, free fall: \(a = g\) down, \(N = 0\), weightless.</li>
<li>Accelerating down faster than \(g\): you would be pressed against the ceiling.</li>
</ul>'''),
             ('Weightlessness in orbit and its consequences', r'''<p>Inside an orbiting satellite, every object falls with the same acceleration as the satellite. So:</p>
<ul>
<li>A spring balance hung from the ceiling reads zero for any object.</li>
<li>A simple pendulum does not oscillate; with no effective gravity it stays wherever it is put.</li>
<li>Water does not pour out of a tilted glass, and a candle flame becomes nearly spherical because hot gases no longer rise.</li>
<li>A body released from the satellite does not fall to the Earth. It keeps the satellite’s velocity, so it stays in the same orbit alongside.</li>
<li>Mass can still be measured, by an inertial method: put the body on a spring and time its oscillations, then use \(m = kT^2/4\pi^2\).</li>
</ul>'''),
             ('Artificial gravity', r'''<p>A rotating space station can press astronauts against its outer wall. The wall provides the centripetal force: \(N = m\omega^2r\). Choosing \(\omega^2r = g\) makes the reading the same as on Earth. For a station of radius 100 m, \(\omega = \sqrt{10/100}\approx0.32\) rad/s, about one turn every 20 s.</p>'''),
         ],
         formulas=[
             dict(title='Apparent weight in a lift', formula=r'N=m(g+a)\ \text{(accelerating up)},\qquad N=m(g-a)\ \text{(accelerating down)}',
                  symbols='N scale reading (N); m mass (kg); g gravity (m/s²); a magnitude of the lift’s acceleration (m/s²). Free fall is a = g downward, giving N = 0.'),
             dict(title='Artificial gravity in a rotating station', formula=r'g_{\rm art}=\omega^2r',
                  symbols='g_art apparent gravity at the rim (m/s²); ω angular speed of the station (rad/s); r distance from the rotation axis to the floor (m). The floor is the outer wall.'),
         ],
         traps=[r'A spring balance in an orbiting satellite reads zero, but a body’s mass is unchanged. Use an oscillating spring (inertial balance), not weighing, to find mass there.',
                r'An object released from an orbiting satellite does not fall toward the Earth. It already has the orbital speed for that radius, so it continues in the same orbit.'],
         exam=r'''<ul>
<li>“A person stands on a scale in a lift accelerating down at g/4 (or up at 2 m/s²). Find the reading.”</li>
<li>“The lift cable breaks. What does the scale read?” (zero)</li>
<li>“Which of these can be used in an orbiting satellite: pendulum clock, spring balance, inertial balance?”</li>
<li>“A packet is released from a satellite. What path does it follow?” (same orbit)</li>
<li>Statement-type: “Astronauts are weightless because gravity is zero at that height.” (false)</li>
</ul>''',
         examples=[
             dict(tag='Numerical', q=r'A 50 kg student stands on a scale in a lift. Find the reading when the lift (a) accelerates upward at 2 m/s², (b) accelerates downward at 2 m/s², (c) falls freely. Take \(g = 10\) m/s².',
                  steps=[r'(a) \(N = m(g+a) = 50\times12 = 600\) N.',
                         r'(b) \(N = m(g-a) = 50\times8 = 400\) N.',
                         r'(c) Free fall: \(a = g\), so \(N = 50\times0 = 0\).',
                         r'The scale reads force, not mass. The student’s mass is 50 kg in all three cases.'],
                  answer=r'600 N, 400 N, 0 N'),
             dict(tag='Conceptual', q=r'Which of these work normally inside a satellite orbiting the Earth: (i) a pendulum clock, (ii) a spring balance for weighing, (iii) a mass oscillating on a spring to measure its mass, (iv) a thermometer?',
                  steps=[r'(i) A pendulum needs effective gravity to restore it. In free fall, \(g_{\rm eff} = 0\), so it does not oscillate. It fails.',
                         r'(ii) A spring balance reads the force needed to hold the body up. Nothing needs holding, so it reads zero. It fails for weighing.',
                         r'(iii) The spring still exerts \(-kx\), and the period \(T = 2\pi\sqrt{m/k}\) depends on mass, not on \(g\). It works.',
                         r'(iv) A thermometer depends on thermal expansion, not on gravity. It works.'],
                  answer=r'(iii) and (iv) work; (i) and (ii) do not.'),
         ],
         practice=[
             dict(q=r'A person of mass 60 kg stands on a weighing scale in a lift that accelerates downward at \(g/4\). The reading of the scale is (\(g = 10\) m/s²)',
                  options=['600 N', '750 N', '450 N', '150 N'], answer=2, type='numerical',
                  explanation=r'\(N = m(g - g/4) = 60\times7.5 = 450\) N. 750 N adds the acceleration as if the lift went up. 150 N is \(m\times g/4\), the force producing the acceleration, not the scale reading.'),
             dict(q=r'A small packet is gently released from a satellite in a circular orbit around the Earth. The packet will',
                  options=['Fall vertically to the Earth', 'Move along a spiral toward the Earth', 'Fly off along the tangent', 'Continue in the same orbit as the satellite'], answer=3, type='concept',
                  explanation=r'At release, the packet has the same velocity as the satellite, which is exactly the orbital speed for that radius. Its motion depends only on \(GM\) and its velocity, not on its mass, so it stays in the same orbit. Falling or spiralling would need it to lose speed.'),
             dict(q=r'Statement I: An astronaut in a satellite orbiting 400 km above the Earth is weightless because the gravitational field there is zero.<br>Statement II: The astronaut and the satellite have the same acceleration toward the Earth.',
                  options=ST_OPTS, answer=2, type='statement',
                  explanation=r'Statement I is false: at 400 km, \(g\) is still about 89% of its surface value. Statement II is true, and it is the real reason for weightlessness: with equal accelerations, the floor exerts no normal force.'),
         ],
     )),
]
