"""Deepening layer: Laws of Motion Part 2, Friction.

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
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" '
            f'style="fill:{color}">{s}</text>')


def _line(x1, y1, x2, y2, color='var(--ink-2)', w=1.5, dash=''):
    d = f';stroke-dasharray:{dash}' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="stroke:{color};stroke-width:{w}{d}"/>'


def _sub(base, sub, rest=''):
    """Subscript inside SVG text without relying on Unicode subscript glyphs."""
    return f'{base}<tspan dy="3" font-size="0.75em">{sub}</tspan><tspan dy="-3">{rest}</tspan>'


# Figure 1: friction against applied force
FIG_GRAPH = ('<svg viewBox="0 0 380 230" role="img" aria-label="Graph of friction against applied force: a 45 degree line up to the limiting value, a drop, then a flat kinetic level">'
             + _line(50, 190, 360, 190) + _line(50, 190, 50, 20)
             + _t(360, 210, 'Applied force F', 12, anchor='end') + _t(56, 18, 'Friction f', 12)
             + _line(50, 60, 180, 60, 'var(--muted)', 1, '4 3') + _line(50, 95, 360, 95, 'var(--muted)', 1, '4 3')
             + _line(180, 60, 180, 190, 'var(--muted)', 1, '4 3')
             + '<path d="M50 190 L180 60 L190 95 L355 95" style="fill:none;stroke:var(--indigo);stroke-width:2.6"/>'
             + '<circle cx="180" cy="60" r="4" style="fill:var(--coral)"/>'
             + _t(44, 64, _sub('μ', 's', 'N'), 12, anchor='end') + _t(44, 99, _sub('μ', 'k', 'N'), 12, anchor='end')
             + _t(180, 206, _sub('F = μ', 's', 'N'), 11, 'var(--coral)', 'middle')
             + _t(112, 160, 'static: f = F', 12, 'var(--indigo)') + _t(112, 176, '(slope 1, block at rest)', 11, 'var(--muted)')
             + _t(230, 85, _sub('kinetic: f = μ', 'k', 'N'), 12, 'var(--indigo)') + _t(230, 120, 'block slides,', 11, 'var(--muted)')
             + _t(230, 135, _sub('a = (F − μ', 'k', 'N)/m'), 11, 'var(--muted)')
             + _t(188, 52, 'limiting friction', 11, 'var(--coral)')
             + '</svg>')

# Figure 2: block on an incline (θ = 30°)
_c = math.cos(math.radians(30)); _s = 0.5
_cx, _cy = 180 - 18 * _s, 109 - 18 * _c   # block centre
FIG_INCLINE = ('<svg viewBox="0 0 360 230" role="img" aria-label="Block resting on a rough incline with weight, normal force, friction and the weight components">'
               + '<polygon points="40,190 320,190 320,28.3" style="fill:var(--surface-2);stroke:var(--ink-2);stroke-width:1.5"/>'
               + '<g transform="translate(180,109) rotate(-30)"><rect x="-30" y="-36" width="60" height="36" style="fill:var(--water-soft);stroke:var(--water);stroke-width:1.5"/></g>'
               + '<path d="M90 190 A50 50 0 0 0 83.3 165" style="fill:none;stroke:var(--ink-2);stroke-width:1.2"/>'
               + _t(98, 182, 'θ', 13)
               + _arrow(_cx, _cy, _cx, _cy + 78, 'var(--ink-2)') + _t(_cx + 4, _cy + 92, 'mg', 12, anchor='middle')
               + _arrow(_cx, _cy, _cx - 0.5 * 62, _cy - _c * 62, 'var(--indigo)') + _t(_cx - 38, _cy - 58, 'N', 13, 'var(--indigo)', weight='bold')
               + _arrow(206, 94, 206 + 52 * _c, 94 - 52 * _s, 'var(--coral)') + _t(196, 50, 'f (up the slope)', 12, 'var(--coral)')
               + _arrow(_cx, _cy, _cx - _c * 40, _cy + _s * 40, 'var(--green)', 1.6, 7) + _t(100, 128, 'mg sinθ', 11, 'var(--green)')
               + _arrow(_cx, _cy, _cx + _s * 52, _cy + _c * 52, 'var(--green)', 1.6, 7) + _t(206, 150, 'mg cosθ', 11, 'var(--green)')
               + _t(20, 222, _sub('At rest: f = mg sinθ, N = mg cosθ. Limiting: tanθ = μ', 's', '.'), 11, 'var(--muted)')
               + '</svg>')

# Figure 3: pulling at an angle
FIG_PULL = ('<svg viewBox="0 50 360 190" role="img" aria-label="Block on a floor pulled by a force P at angle theta above the horizontal, with its components, normal force, weight and friction">'
            + _line(20, 170, 340, 170, 'var(--ink-2)', 2)
            + '<rect x="120" y="110" width="100" height="60" style="fill:var(--water-soft);stroke:var(--water);stroke-width:1.5"/>'
            + _arrow(220, 125, 220 + 95 * math.cos(math.radians(30)), 125 - 95 * 0.5, 'var(--coral)')
            + _t(306, 74, 'P', 13, 'var(--coral)', weight='bold')
            + _line(220, 125, 302, 125, 'var(--coral)', 1.2, '4 3') + _line(302, 125, 302, 77.5, 'var(--coral)', 1.2, '4 3')
            + _t(262, 141, 'P cosθ', 11, 'var(--coral)', 'middle') + _t(308, 104, 'P sinθ', 11, 'var(--coral)')
            + '<path d="M250 125 A30 30 0 0 0 246 110" style="fill:none;stroke:var(--coral);stroke-width:1"/>' + _t(253, 118, 'θ', 11, 'var(--coral)')
            + _arrow(145, 150, 145, 72, 'var(--indigo)') + _t(150, 80, 'N = mg − P sinθ', 11, 'var(--indigo)')
            + _arrow(195, 150, 195, 225, 'var(--ink-2)') + _t(201, 222, 'mg', 12)
            + _arrow(120, 162, 58, 162, 'var(--green)') + _t(30, 154, 'f ≤ μN', 12, 'var(--green)')
            + '</svg>')

# Figure 4: block on block
FIG_STACK = ('<svg viewBox="0 0 380 220" role="img" aria-label="Upper block m on lower block M on a smooth floor. A force F acts on the lower block. Friction on the upper block points forward and friction on the lower block points backward.">'
             + _line(20, 180, 360, 180, 'var(--ink-2)', 2) + _t(24, 198, 'smooth floor', 11, 'var(--muted)')
             + '<rect x="60" y="130" width="240" height="50" style="fill:var(--surface-2);stroke:var(--ink-2);stroke-width:1.5"/>'
             + '<rect x="110" y="80" width="100" height="50" style="fill:var(--water-soft);stroke:var(--water);stroke-width:1.5"/>'
             + _t(160, 100, 'm', 14, anchor='middle', weight='bold') + _t(250, 165, 'M', 14, anchor='middle', weight='bold')
             + _arrow(300, 155, 360, 155, 'var(--coral)') + _t(332, 146, 'F', 13, 'var(--coral)', weight='bold')
             + _arrow(130, 120, 195, 120, 'var(--green)') + _t(214, 118, 'f on m (forward)', 11, 'var(--green)')
             + _arrow(195, 142, 130, 142, 'var(--indigo)') + _t(70, 172, 'f on M (backward)', 11, 'var(--indigo)')
             + _t(20, 30, _sub('No slip while f needed = mF/(m+M) ≤ μ', 's', 'mg'), 12)
             + _t(20, 48, _sub('so F ≤ μ', 's', '(m+M)g when F acts on the lower block.'), 12)
             + '</svg>')


DEEP = {
'friction-static': dict(
    level='basic',
    notes=[
        ('Why friction exists and the laws of limiting friction', r'''<p>Even polished surfaces are rough on a microscopic scale. They touch only at a few high points, and the real contact area is a tiny fraction of the apparent area. At these points the atoms are so close that they bond (a kind of "cold welding"). Friction is the force needed to shear these bonds and to plough the high points through each other.</p>
<p>The laws of limiting friction follow from this picture:</p>
<ol><li>Limiting friction acts along the surface, opposite to the direction in which the body is about to slip.</li>
<li>It is proportional to the normal force: \(f_{s,\max}=\mu_sN\). A larger N squeezes more high points into contact.</li>
<li>It does not depend on the apparent area of contact. Spreading the same N over a larger area lowers the pressure, so each high point flattens less. The real contact area stays about the same.</li>
<li>It depends on the nature and condition of the two surfaces, which is what \(\mu_s\) describes.</li></ol>
<p>Kinetic friction obeys the same laws with \(\mu_k\). Usually \(\mu_k&lt;\mu_s\), because sliding surfaces do not get time to form as many bonds. This is why it is harder to start a heavy box moving than to keep it moving.</p>'''),
        ('Reading the friction–applied-force graph', r'''<p>Push a block with a horizontal force F that grows slowly from zero (see the figure).</p>
<ul><li><strong>Static region:</strong> the block stays at rest, so friction exactly balances the push, f = F. The graph is a straight line through the origin with slope 1 (45° when both axes use the same scale).</li>
<li><strong>Limiting point:</strong> at F = μₛN the block is just about to move. This is the peak of the graph.</li>
<li><strong>Kinetic region:</strong> once the block slides, friction drops to μₖN and stays almost constant, whatever F is. The extra force F − μₖN now produces acceleration.</li></ul>
<p>If a question gives the graph and the mass, read μₛ from the peak and μₖ from the flat level, each divided by N = mg.</p>'''),
        ('Total contact force and the angle of friction', r'''<p>The surface exerts one contact force on the block. Its two components are N (perpendicular) and f (along the surface). Its magnitude is \(\sqrt{N^2+f^2}\).</p>
<p>On a horizontal surface with only a horizontal push, N = mg while f can be anything from 0 to μₛmg. So the contact force lies between <strong>mg</strong> (no friction needed) and <strong>mg√(1+μₛ²)</strong> (limiting friction). It is never less than mg.</p>
<p>At the limit, the contact force tilts away from the normal by an angle λ with \(\tan\lambda=f_{\max}/N=\mu_s\). This λ is the <em>angle of friction</em>. It returns in the incline section as the angle of repose.</p>'''),
    ],
    formulas=[
        dict(title='Range of the total contact force (level surface, horizontal push)',
             formula=r'mg\;\le\;\sqrt{N^2+f^2}\;\le\;mg\sqrt{1+\mu_s^2}',
             symbols='m mass (kg); g = 10 m/s²; N = mg normal force (N); f friction (N), from 0 up to μₛmg; μₛ static coefficient (no unit). Holds while the block is at rest and the push is horizontal.'),
        dict(title='Angle of friction',
             formula=r'\tan\lambda=\frac{f_{s,\max}}{N}=\mu_s',
             symbols='λ angle between the resultant contact force and the normal at the point of slipping (degrees or rad); μₛ static coefficient (no unit). λ is a property of the pair of surfaces.'),
    ],
    figure=dict(svg=FIG_GRAPH, caption='Friction against applied force. While the block is at rest friction equals the push (slope 1). It peaks at μₛN, then drops to the steady kinetic value μₖN once sliding starts.'),
    traps=[r'Friction does not depend on the area of contact. A brick has the same limiting friction lying flat or standing on its end, because N and the surfaces are unchanged.',
           r'μ is not limited to values below 1. Rubber on dry concrete and very clean metals can have μ greater than 1. Only "μ ≥ 0" is guaranteed.'],
    exam=r'''<ul><li>"A block of mass m is at rest on a rough floor and a force F (less than μₛmg) acts on it. Friction is …" Answer: F, not μₛmg.</li>
<li>Graph of friction against applied force: identify the static line, the peak (limiting friction) and the kinetic level.</li>
<li>"The contact force exerted by the floor on the block lies between …" Answer: mg and mg√(1+μ²).</li>
<li>Block pressed against a vertical wall: find the minimum horizontal force to hold it, then the friction when the force is larger.</li>
<li>Assertion–reason on why friction is independent of the area of contact.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A 5 kg block rests on a floor with μₛ = 0.4 and μₖ = 0.3. A horizontal force of (a) 10 N, (b) 20 N, (c) 25 N acts on it. Find the friction and the acceleration in each case.',
             steps=[r'Normal force N = mg = 50 N. Limiting static friction = 0.4 × 50 = 20 N. Kinetic friction = 0.3 × 50 = 15 N.',
                    r'(a) 10 N &lt; 20 N, so the block stays at rest. Static friction adjusts to 10 N and a = 0.',
                    r'(b) 20 N equals the limit. The block is on the verge of moving. Friction = 20 N and a = 0.',
                    r'(c) 25 N &gt; 20 N, so it slides. Friction is now kinetic, 15 N. a = (25 − 15)/5 = 2 m/s².'],
             answer=r'(a) 10 N, 0 (b) 20 N, 0 (c) 15 N, 2 m/s²'),
        dict(tag='Graph', q=r'For a 6 kg block, the friction–applied-force graph rises along a 45° line to a peak of 30 N, then drops and stays at 24 N. Find μₛ and μₖ.',
             steps=[r'N = mg = 60 N on a level floor with a horizontal push.',
                    r'The peak is limiting static friction: μₛ = 30/60 = 0.5.',
                    r'The flat level is kinetic friction: μₖ = 24/60 = 0.4.',
                    r'Check: μₖ &lt; μₛ, as expected for the drop after the peak.'],
             answer=r'μₛ = 0.5, μₖ = 0.4'),
        dict(tag='Conceptual', q=r'A 2 kg book is held against a vertical wall by a horizontal push F. μₛ = 0.5. (a) Find the least F that holds it. (b) If F = 100 N, what is the friction on the book?',
             steps=[r'The push F is perpendicular to the wall, so the normal force is N = F. Friction acts vertically and must balance the weight, 20 N.',
                    r'(a) Holding needs mg ≤ μₛF, so F ≥ 20/0.5 = 40 N.',
                    r'(b) With F = 100 N, the friction available is up to 50 N. But only 20 N is needed for equilibrium, so friction = 20 N upward.',
                    r'Pressing harder raises the limit, not the actual friction.'],
             answer=r'(a) 40 N (b) 20 N upward'),
    ],
    practice=[
        dict(q=r'A 3 kg block on a rough horizontal floor (μₛ = 0.75) is pushed horizontally with a slowly increasing force until it is just about to slide. The magnitude of the total force exerted by the floor on the block at that moment is (g = 10 m/s²)',
             options=['30 N', '37.5 N', '22.5 N', '52.5 N'], answer=1, type='numerical',
             explanation=r'N = 30 N and limiting friction = 0.75 × 30 = 22.5 N. The floor exerts both, so the contact force is √(30² + 22.5²) = 37.5 N. 30 N is the normal force alone and 22.5 N is friction alone. 52.5 N adds two perpendicular components as if they were parallel.'),
        dict(q=r'A 1 kg block is pressed against a vertical wall by a horizontal force of 50 N. μₛ = 0.5 and g = 10 m/s². The friction on the block is',
             options=['5 N', '25 N', '10 N', '50 N'], answer=2, type='concept',
             explanation=r'The block stays at rest because the maximum friction 0.5 × 50 = 25 N exceeds its weight. Static friction only supplies what equilibrium needs: 10 N upward. 25 N is the limit, not the actual value. 50 N is the normal force, and 5 N would leave the weight unbalanced.'),
        dict(q=r'<strong>Assertion (A):</strong> The limiting friction between two surfaces does not depend on the apparent area of contact.<br><strong>Reason (R):</strong> The real (microscopic) area of contact depends mainly on the normal force, not on the apparent area.',
             options=AR, answer=0, type='ar',
             explanation=r'Both are true. A larger apparent area spreads the load, so each high point is pressed less and the real contact area stays nearly the same. Friction depends on the real contact area, so R explains A. Option 2 is wrong because R is the reason, not a separate fact.'),
        dict(q=r'A block on a level floor has μₛ = 0.5 and μₖ = 0.4. A horizontal force F is increased slowly from zero. Which statements are correct?<br>(i) For F below μₛmg, friction equals F.<br>(ii) Just after sliding starts, friction falls to 0.4 mg.<br>(iii) After sliding, friction keeps rising with F.<br>(iv) The friction–F graph starts as a straight line of slope 1 through the origin.',
             options=['(i) and (iii) only', '(ii) and (iii) only', '(i), (ii) and (iv) only', 'All four'], answer=2, type='graph',
             explanation=r'Before sliding, static friction matches F, so the graph is f = F (slope 1). After sliding, friction is kinetic, μₖmg = 0.4 mg, and stays constant. Statement (iii) is false: extra force produces acceleration, not more friction. Any option containing (iii) is wrong.'),
    ],
),

'friction-kinetic': dict(
    level='core',
    notes=[
        ('Stopping distance and stopping time on a rough floor', r'''<p>A body sliding on a level floor with no other horizontal force slows down only because of kinetic friction.</p>
<ol><li>Friction = μₖmg, so the deceleration is a = μₖg. The mass cancels.</li>
<li>From v² = u² − 2as with v = 0: stopping distance s = u²/(2μₖg).</li>
<li>From v = u − at: stopping time t = u/(μₖg).</li>
<li>The same result comes from the work–energy theorem: friction work −μₖmg·s removes the whole kinetic energy ½mu².</li></ol>
<p>Proportional reasoning: s ∝ u² and t ∝ u. Doubling the speed makes the stopping distance four times larger but the time only twice as long. For the same <em>kinetic energy</em> K, s = K/(μₖmg), so the lighter body slides farther.</p>'''),
        ('Work done by kinetic friction: which body and which frame', r'''<p>Kinetic friction opposes the <em>relative</em> sliding of the two surfaces. On a fixed floor that is the same as opposing the body's motion, so its work is negative. If the other surface moves, look at each body in the ground frame:</p>
<ul><li>A box dropped on a moving conveyor belt slides backward relative to the belt. Friction on the box points forward and does <strong>positive</strong> work on the box, speeding it up.</li>
<li>Friction on the belt points backward and does negative work on the belt. The motor must supply that energy.</li>
<li>The two works add to −f × (relative sliding distance). This net negative amount is the heat produced at the contact.</li></ul>'''),
    ],
    formulas=[
        dict(title='Stopping distance and time (level floor)',
             formula=r's=\frac{u^2}{2\mu_kg},\qquad t=\frac{u}{\mu_kg}',
             symbols='u initial speed (m/s); μₖ kinetic coefficient (no unit); g = 10 m/s²; s stopping distance (m); t stopping time (s). Only friction acts horizontally and the floor is level.'),
        dict(title='Heat produced by a sliding contact',
             formula=r'Q=\mu_kN\,s_{\rm rel}',
             symbols='Q heat (J); μₖ kinetic coefficient; N normal force (N); s_rel distance one surface slides relative to the other (m). Valid for constant kinetic friction.'),
    ],
    traps=[r'Kinetic friction opposes the relative velocity of the surfaces, not the applied force. A box on an accelerating conveyor receives friction in its direction of motion.',
           r'Once sliding begins, use μₖ even if the question also gives μₛ. Using μₛ for a moving body is a common error in numerical answers.'],
    exam=r'''<ul><li>"A car moving at u is braked with locked wheels. Find the stopping distance." Then: "If the speed is doubled …" (×4).</li>
<li>Ratio questions: two bodies with the same speed (same s) or the same kinetic energy (s ∝ 1/m) on the same surface.</li>
<li>Work done by friction on a box placed on a moving belt, and the heat produced.</li>
<li>Statement-type: "Kinetic friction always does negative work" (false).</li></ul>''',
    examples=[
        dict(tag='Ratio', q=r'Blocks A (m) and B (2m) slide on the same rough floor. Find the ratio of their stopping distances s_A : s_B when they start (a) with the same speed, (b) with the same kinetic energy.',
             steps=[r'Deceleration is μₖg for both, independent of mass.',
                    r'(a) s = u²/(2μₖg) depends only on u. Same u gives s_A : s_B = 1 : 1.',
                    r'(b) Work–energy: μₖmg·s = K, so s = K/(μₖmg) ∝ 1/m.',
                    r'With equal K, s_A : s_B = 2m : m = 2 : 1.'],
             answer=r'(a) 1 : 1 (b) 2 : 1'),
        dict(tag='Numerical', q=r'A 4 kg block starts from rest and is pulled 5 m across a floor by a horizontal 30 N force. μₖ = 0.25. Find its speed using the work–energy theorem.',
             steps=[r'Friction = 0.25 × 40 = 10 N.',
                    r'Work by the pull = 30 × 5 = 150 J. Work by friction = −10 × 5 = −50 J.',
                    r'Net work = 100 J = ½ × 4 × v².',
                    r'v² = 50, so v ≈ 7.07 m/s. (Check: a = 20/4 = 5 m/s² and v² = 2 × 5 × 5 = 50.)'],
             answer=r'√50 ≈ 7.07 m/s'),
        dict(tag='Conceptual', q=r'A 5 kg box is gently placed on a belt moving steadily at 2 m/s. μₖ = 0.2. Find (a) the time before the box moves with the belt, (b) the work done by friction on the box, (c) the heat produced.',
             steps=[r'The box slides backward relative to the belt, so friction on it is forward: f = 0.2 × 50 = 10 N, a = 2 m/s².',
                    r'(a) It reaches 2 m/s after t = 2/2 = 1 s. In that time the box moves ½ × 2 × 1² = 1 m and the belt moves 2 m.',
                    r'(b) Work on the box = +10 × 1 = 10 J, which equals its kinetic energy ½ × 5 × 2².',
                    r'(c) Relative sliding = 2 − 1 = 1 m, so heat = 10 × 1 = 10 J. The motor supplies 10 × 2 = 20 J in total.'],
             answer=r'(a) 1 s (b) +10 J (c) 10 J'),
    ],
    practice=[
        dict(q=r'A car moving at 72 km/h brakes with its wheels locked. μₖ between tyres and road is 0.5 (g = 10 m/s²). Its stopping distance is',
             options=['20 m', '80 m', '4 m', '40 m'], answer=3, type='numerical',
             explanation=r'72 km/h = 20 m/s. s = u²/(2μₖg) = 400/10 = 40 m. 80 m forgets the factor 2 in the denominator, and 20 m doubles μₖg by mistake. 4 is the stopping time in seconds, not a distance.'),
        dict(q=r'On the same rough road, a car’s speed is doubled before braking (wheels locked). Its stopping distance and stopping time become',
             options=['4 times and 2 times', '2 times and 2 times', '4 times and 4 times', '2 times and 4 times'], answer=0, type='concept',
             explanation=r'Deceleration μₖg does not change. s = u²/(2μₖg) ∝ u², so it becomes 4 times. t = u/(μₖg) ∝ u, so it becomes 2 times. Options that scale both the same way miss that distance depends on the square of speed.'),
        dict(q=r'A box is placed at rest on a conveyor belt moving to the right. While the box is slipping on the belt, the kinetic friction on the box',
             options=['acts to the left and does negative work on the box', 'acts to the right and does positive work on the box', 'is zero because the box starts at rest', 'acts to the right but does zero work'], answer=1, type='concept',
             explanation=r'Relative to the belt the box slides to the left, so friction on it points right. The box moves right in the ground frame, so the work is positive and the box speeds up. Option 1 assumes friction always opposes motion. Friction is not zero, because the surfaces are sliding.'),
        dict(q=r'<strong>Statement I:</strong> Kinetic friction always does negative work on the body it acts on.<br><strong>Statement II:</strong> For a pair of surfaces sliding over each other, the total work done by the two kinetic friction forces is negative.',
             options=ST, answer=3, type='statement',
             explanation=r'Statement I is false: friction on a box on a moving belt does positive work. Statement II is true: the total is −f × (relative sliding distance), which is the heat produced. So "I false, II true".'),
    ],
),

'friction-inclines': dict(
    level='exam',
    notes=[
        ('Derivation: angle of repose equals angle of friction', r'''<ol><li>Tilt a plane slowly until the block is just about to slide. Call this angle θᵣ, the angle of repose.</li>
<li>Along the plane: friction balances the downhill pull, f = mg sinθᵣ. Perpendicular: N = mg cosθᵣ.</li>
<li>At the limit f = μₛN, so mg sinθᵣ = μₛ mg cosθᵣ, giving tanθᵣ = μₛ.</li>
<li>Only two forces now act: the weight and the total contact force. So the contact force must be vertical. It makes angle θᵣ with the normal to the plane.</li>
<li>But the angle between the limiting contact force and the normal is, by definition, the angle of friction λ. Hence θᵣ = λ, and tanθᵣ = tanλ = μₛ.</li></ol>
<p>Below θᵣ the block stays at rest and friction is only mg sinθ. Above θᵣ it slides with a = g(sinθ − μₖcosθ).</p>'''),
        ('Forces needed along the incline', r'''<p>A force F pushes the block along the incline (parallel to the surface). Friction always points opposite to the way the block would slip.</p>
<ul><li><strong>To start moving it up (or move it up at constant speed with μₖ):</strong> friction acts down, so F = mg(sinθ + μcosθ).</li>
<li><strong>To just stop it sliding down</strong> (only needed when tanθ &gt; μ): friction acts up, so F = mg(sinθ − μcosθ).</li>
<li>For any F between these two values the block stays at rest, and static friction takes whatever value and direction is needed.</li></ul>'''),
        ('Projected up a rough incline, and the "n times longer" result', r'''<p><strong>Going up:</strong> gravity and friction both act down the slope, so the deceleration is g(sinθ + μₖcosθ). <strong>Coming down</strong> (if tanθ &gt; μₛ): a = g(sinθ − μₖcosθ). The trip down is slower, so it takes longer than the trip up over the same distance: t_down/t_up = √(a_up/a_down).</p>
<p><strong>Rough vs smooth:</strong> if sliding down a rough incline takes n times as long as down the same smooth incline (same length L from rest), then L = ½ a t² gives a_smooth/a_rough = n². So sinθ = n²(sinθ − μcosθ), which rearranges to μ = tanθ(1 − 1/n²). At 45° this is simply μ = 1 − 1/n².</p>'''),
    ],
    formulas=[
        dict(title='Holding a block on an incline with a force along it',
             formula=r'mg(\sin\theta-\mu_s\cos\theta)\;\le\;F\;\le\;mg(\sin\theta+\mu_s\cos\theta)',
             symbols='F force parallel to the incline, pointing up the slope (N); m mass (kg); g = 10 m/s²; θ incline angle; μₛ static coefficient. The lower limit applies when tanθ > μₛ; otherwise it is zero.'),
        dict(title='Rough slide takes n times as long as smooth slide',
             formula=r'\mu_k=\tan\theta\left(1-\frac{1}{n^2}\right)',
             symbols='μₖ kinetic coefficient; θ incline angle; n = t_rough / t_smooth for the same length, both starting from rest.'),
        dict(title='Block projected up a rough incline',
             formula=r'a_{\rm up}=g(\sin\theta+\mu_k\cos\theta),\qquad a_{\rm down}=g(\sin\theta-\mu_k\cos\theta)',
             symbols='a magnitudes of acceleration (m/s²) while moving up and while sliding back down; θ incline angle; μₖ kinetic coefficient. The block slides back only if tanθ > μₛ.'),
    ],
    figure=dict(svg=FIG_INCLINE, caption='Forces on a block at rest on a rough incline. The weight splits into mg sinθ down the slope and mg cosθ into the surface. Friction balances the first and the normal force balances the second.'),
    traps=[r'A block at rest on an incline below the angle of repose has friction mg sinθ, not μₛmg cosθ. Use μN only at the limit or while sliding.',
           r'The incline angle is θ, but the normal force is mg cosθ only when no other force has a component perpendicular to the incline. A horizontal push changes N.'],
    exam=r'''<ul><li>"Find the angle of repose if μ = …", or "a block just begins to slide at 30°; find μ".</li>
<li>Minimum and maximum force along the incline to keep a block at rest.</li>
<li>"Time to slide down a rough incline is n times that on a smooth one. Find μ." (Answer μ = tanθ(1 − 1/n²).)</li>
<li>Block projected up a rough incline: distance travelled, and the ratio of times for the upward and downward trips.</li>
<li>Graph of friction against incline angle as θ increases from 0 to 90°.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A 10 kg block lies on a 37° incline (sin 37° = 0.6, cos 37° = 0.8). μₛ = 0.5. Find the force along the incline needed (a) to just start it moving up, (b) to just stop it sliding down.',
             steps=[r'mg = 100 N. Down-slope pull mg sinθ = 60 N. Normal force mg cosθ = 80 N, so limiting friction = 0.5 × 80 = 40 N.',
                    r'Check: tan 37° = 0.75 &gt; 0.5, so without help the block would slide down.',
                    r'(a) Moving up, friction acts down the slope: F = 60 + 40 = 100 N.',
                    r'(b) About to slide down, friction acts up the slope: F = 60 − 40 = 20 N.'],
             answer=r'(a) 100 N (b) 20 N. Any force from 20 N to 100 N keeps it at rest.'),
        dict(tag='Ratio', q=r'A block takes twice as long to slide down a rough 45° incline as down the same incline when it is smooth. Find μₖ.',
             steps=[r'Same length L from rest: L = ½at², so a ∝ 1/t². With t_rough = 2t_smooth, a_rough = a_smooth/4.',
                    r'g(sin45° − μcos45°) = ¼ g sin45°.',
                    r'Divide by g cos45°: 1 − μ = ¼, so μ = 0.75.',
                    r'Formula check: μ = tan45°(1 − 1/2²) = 0.75.'],
             answer=r'μₖ = 0.75'),
        dict(tag='Conceptual', q=r'A 2 kg block rests on a 30° incline with μₛ = 0.8. A student says friction = μₛmg cos30° ≈ 13.9 N. Is the student right?',
             steps=[r'First check whether the block can stay at rest: tan30° ≈ 0.577 &lt; 0.8, so it does.',
                    r'At rest, friction balances the down-slope pull: f = mg sin30° = 20 × 0.5 = 10 N.',
                    r'13.9 N is the maximum friction available, not the friction acting. The student has used the limit when the block is not at the limit.'],
             answer=r'No. Friction is 10 N up the slope.'),
        dict(tag='Numerical', q=r'A block is projected up a 30° incline at 10 m/s. μₖ = 1/(2√3). How far up does it go, and how do the times up and down compare?',
             steps=[r'μₖcos30° = (1/(2√3)) × (√3/2) = 0.25.',
                    r'Going up: a = 10(0.5 + 0.25) = 7.5 m/s². Distance = 10²/(2 × 7.5) ≈ 6.67 m.',
                    r'tan30° ≈ 0.577 &gt; μ, so it slides back. Coming down: a = 10(0.5 − 0.25) = 2.5 m/s².',
                    r'Same distance: t ∝ 1/√a, so t_down/t_up = √(7.5/2.5) = √3.'],
             answer=r'About 6.67 m. The return trip takes √3 times as long.'),
    ],
    practice=[
        dict(q=r'The time taken to slide down a rough 30° incline is twice the time taken to slide down the same incline when smooth. μₖ is',
             options=['3/4', '√3/4', '1/(2√3)', '√3/2'], answer=1, type='numerical',
             explanation=r'μ = tanθ(1 − 1/n²) = (1/√3)(3/4) = √3/4 ≈ 0.43. The value 3/4 is the 45° answer, where tanθ = 1. 1/(2√3) uses (1 − 1/n) instead of (1 − 1/n²).'),
        dict(q=r'A block is projected up a rough incline, stops, and slides back. Its acceleration going up is 3 times its acceleration coming down. The ratio of time taken to come down to time taken to go up is',
             options=['1/3', '3', '1/√3', '√3'], answer=3, type='numerical',
             explanation=r'Both trips cover the same distance and one end has zero speed, so s = ½at² for each. t ∝ 1/√a, giving t_down/t_up = √(a_up/a_down) = √3. The answer 3 forgets the square root, and the fractions invert the ratio: the slower trip (down) takes longer.'),
        dict(q=r'A block sits on a plank whose angle θ is raised slowly from 0 to 90°. μₛ &gt; μₖ. Which description of the friction on the block is correct?',
             options=['Constant at μₛmg throughout', 'Rises as mg cosθ, then falls', 'Rises as mg sinθ up to the angle of repose, then falls as μₖmg cosθ', 'Falls steadily as μₖmg cosθ from θ = 0'], answer=2, type='graph',
             explanation=r'Before slipping, static friction balances mg sinθ, which rises with θ. Once θ passes the angle of repose the block slides, and friction becomes μₖmg cosθ, which drops toward zero at 90°. The other options use a limiting or kinetic value while the block is still at rest.'),
        dict(q=r'<strong>Assertion (A):</strong> A block placed gently on an incline with μₛ &gt; tanθ stays at rest.<br><strong>Reason (R):</strong> The friction on such a block equals μₛmg cosθ.',
             options=AR, answer=2, type='ar',
             explanation=r'A is true: the limit μₛmg cosθ exceeds the down-slope pull mg sinθ, so friction can hold the block. R is false: the actual friction is only mg sinθ, the amount equilibrium needs. Choose "A true, R false".'),
    ],
),

'friction-pulling': dict(
    level='exam',
    notes=[
        ('Derivation: the best angle to pull a block', r'''<ol><li>Pull with P at angle θ above the horizontal (figure). Vertical balance: N = mg − P sinθ.</li>
<li>At the point of sliding: P cosθ = μN = μ(mg − P sinθ).</li>
<li>So \(P=\dfrac{\mu mg}{\cos\theta+\mu\sin\theta}\).</li>
<li>P is least when the denominator is greatest. Write cosθ + μ sinθ = √(1 + μ²) cos(θ − λ), where tanλ = μ. Its maximum, √(1 + μ²), occurs at θ = λ.</li>
<li>So the best angle is the angle of friction, tanθ = μ, and \(P_{\min}=\dfrac{\mu mg}{\sqrt{1+\mu^2}}=mg\sin\lambda\).</li></ol>
<p>Physical picture: tilting the pull upward does two things. Its horizontal part shrinks (bad), but it lifts some weight off the floor, cutting friction (good). The best balance is at θ = λ.</p>'''),
        ('Pulling versus pushing', r'''<p>A push directed <em>downward</em> at θ below the horizontal presses the block into the floor: N = mg + P sinθ. At the point of sliding P cosθ = μ(mg + P sinθ), so</p>
<p>\[P_{\rm push}=\frac{\mu mg}{\cos\theta-\mu\sin\theta}.\]</p>
<p>The denominator is smaller than for a pull, so pushing always needs more force. If cosθ ≤ μ sinθ (that is, tanθ ≥ 1/μ), no push however large can start the block: every extra newton of push adds at least as much friction as driving force. This is why a lawn roller is pulled rather than pushed.</p>'''),
    ],
    formulas=[
        dict(title='Pull at angle θ above horizontal (point of sliding)',
             formula=r'P=\frac{\mu mg}{\cos\theta+\mu\sin\theta},\qquad P_{\min}=\frac{\mu mg}{\sqrt{1+\mu^2}}\ \text{at}\ \tan\theta=\mu',
             symbols='P pull (N); m mass (kg); g = 10 m/s²; μ static coefficient for starting (kinetic for constant velocity); θ angle above horizontal. Assumes the block stays on the floor (N ≥ 0).'),
        dict(title='Push at angle θ below horizontal',
             formula=r'P=\frac{\mu mg}{\cos\theta-\mu\sin\theta}\qquad(\text{no motion possible if }\tan\theta\ge 1/\mu)',
             symbols='P push (N) directed downward at θ below the horizontal; μ friction coefficient; m mass (kg); g = 10 m/s².'),
    ],
    figure=dict(svg=FIG_PULL, caption='Pulling at an angle. The vertical part P sinθ lifts some weight off the floor, so N = mg − P sinθ and the friction limit drops. Only P cosθ drives the block forward.'),
    traps=[r'"Pulling at an angle always helps" is false. Near 90° almost all the pull is vertical. With μ &lt; 1, a vertical pull needs P = mg to make N zero, far more than the horizontal pull μmg.',
           r'If the block is not sliding, friction equals P cosθ, not μ(mg − P sinθ). Check the limit before using μN.'],
    exam=r'''<ul><li>"Find the minimum force needed to move a block on a rough floor, and the angle at which it acts." Answer: μmg/√(1 + μ²) at tan⁻¹μ.</li>
<li>Pulling vs pushing at the same angle: which needs more force, or find both.</li>
<li>Acceleration of a block pulled at an angle (normal force is not mg).</li>
<li>Statement questions on why a lawn roller is easier to pull than push.</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A 10 kg block lies on a floor with μₛ = 0.75. Find the smallest force that can start it moving, and its direction. Compare with a horizontal pull.',
             steps=[r'Best angle: tanθ = μ = 0.75, so θ = 37°.',
                    r'P_min = μmg/√(1 + μ²) = 0.75 × 100/1.25 = 60 N.',
                    r'Check: N = 100 − 60 × 0.6 = 64 N; μN = 48 N; P cosθ = 60 × 0.8 = 48 N. Balanced at the limit.',
                    r'A horizontal pull needs μmg = 75 N, which is 25% more.'],
             answer=r'60 N at 37° above the horizontal (horizontal pull would need 75 N)'),
        dict(tag='Ratio', q=r'A 10 kg block (μₛ = 0.5) is to be started either by a pull at 37° above the horizontal or a push at 37° below the horizontal. Find both forces.',
             steps=[r'μmg = 50 N, cos37° = 0.8, sin37° = 0.6.',
                    r'Pull: P = 50/(0.8 + 0.5 × 0.6) = 50/1.1 ≈ 45.5 N.',
                    r'Push: P = 50/(0.8 − 0.5 × 0.6) = 50/0.5 = 100 N.',
                    r'The push presses the block down, raising N to 100 + 60 = 160 N and the friction limit to 80 N.'],
             answer=r'Pull ≈ 45.5 N; push = 100 N. Pushing needs about 2.2 times as much.'),
        dict(tag='Statement I / II', q=r'<strong>Statement I:</strong> A person pushing a lawn roller at an angle below the horizontal needs less force than one pulling it at the same angle above the horizontal.<br><strong>Statement II:</strong> Pulling at an angle above the horizontal reduces the normal force.',
             steps=[r'A downward push adds P sinθ to the normal force, increasing friction. An upward pull subtracts it.',
                    r'So pulling needs less force. Statement I is false.',
                    r'Statement II is true: N = mg − P sinθ for an upward pull.'],
             answer=r'Statement I false, Statement II true.'),
    ],
    practice=[
        dict(q=r'A 4 kg block lies on a floor with μₛ = 1/√3 (g = 10 m/s²). The minimum force that can start it sliding and the angle it makes with the horizontal are',
             options=['20 N at 60°', '40/√3 N at 0°', '20 N at 30°', '10 N at 30°'], answer=2, type='numerical',
             explanation=r'Best angle: tanθ = μ = 1/√3, so θ = 30°. P_min = μmg/√(1 + μ²) = (40/√3)/(2/√3) = 20 N. 40/√3 ≈ 23.1 N is the horizontal pull, which is larger. 60° is the complement of the right angle, and 10 N is half the correct value.'),
        dict(q=r'A 5 kg block on a floor (μₛ = 0.5) is pulled by 20 N at 37° above the horizontal (sin 37° = 0.6). The friction acting on it is',
             options=['19 N', '25 N', '0 N', '16 N'], answer=3, type='numerical',
             explanation=r'N = 50 − 20 × 0.6 = 38 N, so the limit is 19 N. The horizontal pull is 20 × 0.8 = 16 N, below the limit, so the block stays at rest and static friction is 16 N. 19 N is the limit, not the actual friction. 25 N uses N = mg.'),
        dict(q=r'A block on a rough floor (μ = 0.5) is pushed by a force directed downward at θ below the horizontal. The block cannot be moved by any push, however large, when',
             options=['tanθ ≥ 0.5', 'tanθ ≥ 2', 'θ ≥ 30°', 'θ ≥ 45°'], answer=1, type='concept',
             explanation=r'Sliding needs P cosθ &gt; μ(mg + P sinθ). For large P the condition becomes cosθ &gt; μ sinθ, that is tanθ &lt; 1/μ = 2. For tanθ ≥ 2 (θ ≥ 63.4°) the extra friction always wins. tanθ ≥ 0.5 is the angle of friction, which gives the best pulling angle instead.'),
        dict(q=r'<strong>Statement I:</strong> Pulling a block at any angle above the horizontal always needs less force than pulling it horizontally.<br><strong>Statement II:</strong> The pull needed to start a block is smallest when the pull makes an angle tan⁻¹μ with the horizontal.',
             options=ST, answer=3, type='statement',
             explanation=r'Statement I is false. At steep angles the horizontal component becomes tiny; at 90° you need P = mg, which exceeds μmg when μ &lt; 1. Statement II is true: it follows from maximising cosθ + μ sinθ.'),
    ],
),

'friction-systems': dict(
    level='exam',
    notes=[
        ('Block on a rough table pulled by a hanging mass', r'''<p>A block m₁ lies on a rough table and is tied over a light pulley to a hanging block m₂.</p>
<ol><li><strong>Will it move?</strong> The pull available is m₂g. The most static friction can supply is μₛm₁g. Motion starts only if m₂g &gt; μₛm₁g, i.e. m₂ &gt; μₛm₁.</li>
<li><strong>If it moves:</strong> treat the two blocks as one system along the string. Driving force m₂g, opposing force μₖm₁g, total mass m₁ + m₂:
\[a=\frac{(m_2-\mu_km_1)g}{m_1+m_2}\]</li>
<li><strong>Tension:</strong> from the hanging block, T = m₂(g − a).</li>
<li><strong>If it does not move:</strong> a = 0, T = m₂g, and friction = m₂g (not μₛm₁g).</li></ol>'''),
        ('Banked road with friction', r'''<p>On a road banked at θ, friction can act down the slope (car tending to skid outward at high speed) or up the slope (car tending to slide inward at low speed). Resolving forces gives the safe range of speeds:</p>
<p>\[v_{\max}=\sqrt{rg\,\frac{\tan\theta+\mu_s}{1-\mu_s\tan\theta}},\qquad v_{\min}=\sqrt{rg\,\frac{\tan\theta-\mu_s}{1+\mu_s\tan\theta}}\]</p>
<p>Special cases: θ = 0 gives v_max = √(μₛrg), the level-road result. μₛ = 0 gives v = √(rg tanθ), the design speed of a frictionless bank. If μₛ ≥ tanθ, v_min = 0 and a car can even stand still on the bank.</p>'''),
        ('Friction limits a vehicle’s acceleration', r'''<p>Driving and braking forces on a car come from static friction between tyres and road. If all wheels are driven or braked, the largest acceleration or deceleration is μₛg. A box on a truck floor can only be accelerated by friction too, so the truck must not accelerate or brake harder than μₛg (box–floor) or the box slides.</p>'''),
    ],
    formulas=[
        dict(title='Rough table with hanging mass',
             formula=r'a=\frac{(m_2-\mu_km_1)g}{m_1+m_2},\qquad T=m_2(g-a),\qquad \text{moves only if } m_2>\mu_sm_1',
             symbols='m₁ block on the table (kg); m₂ hanging block (kg); μₛ, μₖ table coefficients; g = 10 m/s²; a acceleration (m/s²); T tension (N). Light string, ideal pulley.'),
        dict(title='Banked road with friction',
             formula=r'v_{\max}=\sqrt{rg\,\frac{\tan\theta+\mu_s}{1-\mu_s\tan\theta}},\qquad v_{\min}=\sqrt{rg\,\frac{\tan\theta-\mu_s}{1+\mu_s\tan\theta}}',
             symbols='r radius of the turn (m); g = 10 m/s²; θ bank angle; μₛ static coefficient between tyres and road; v in m/s. If μₛ ≥ tanθ, v_min = 0.'),
    ],
    traps=[r'For a block on a rough table with a hanging mass, do not write a = (m₂ − μm₁)g/(m₁ + m₂) before checking that m₂ &gt; μₛm₁. Otherwise you get a negative or false acceleration for a system that is at rest.',
           r'On a banked road the friction direction depends on speed. Below the design speed √(rg tanθ), friction acts up the slope.'],
    exam=r'''<ul><li>Block on a rough table with a hanging mass: find a and T, or the minimum μ to keep it at rest.</li>
<li>Two blocks in contact pushed along a rough floor: find the contact force.</li>
<li>Maximum speed on a banked road with friction (often with μ = tanθ or simple angles).</li>
<li>"A box is on the floor of a truck … find the maximum deceleration / minimum stopping distance so the box does not slide."</li></ul>''',
    examples=[
        dict(tag='Numerical', q=r'A 4 kg block on a rough table (μₛ = 0.3, μₖ = 0.25) is tied over a smooth pulley to a hanging 2 kg block. Find the acceleration and the tension.',
             steps=[r'Check motion: m₂g = 20 N; μₛm₁g = 0.3 × 40 = 12 N. 20 &gt; 12, so the system moves.',
                    r'Kinetic friction = 0.25 × 40 = 10 N. a = (20 − 10)/(4 + 2) = 10/6 ≈ 1.67 m/s².',
                    r'Tension: T = m₂(g − a) = 2(10 − 1.67) ≈ 16.7 N.',
                    r'Check with the table block: T − 10 = 4 × 1.67 ≈ 6.67 N. Correct.'],
             answer=r'a ≈ 1.67 m/s², T ≈ 16.7 N'),
        dict(tag='Numerical', q=r'A curve of radius 30 m is banked at θ with tanθ = 0.5. μₛ = 0.5. Find the maximum and minimum safe speeds.',
             steps=[r'v_max² = rg(tanθ + μ)/(1 − μtanθ) = 300 × 1/(1 − 0.25) = 400, so v_max = 20 m/s.',
                    r'v_min²: numerator tanθ − μ = 0, so v_min = 0.',
                    r'Meaning: friction alone can hold a parked car on this bank, because μₛ = tanθ.'],
             answer=r'v_max = 20 m/s, v_min = 0'),
        dict(tag='Conceptual', q=r'A truck carries a crate on its flat floor. The truck speeds up from rest. Which force accelerates the crate, and in which direction does it act?',
             steps=[r'The crate tends to stay behind as the floor moves forward, so relative to the floor it tends to slip backward.',
                    r'Static friction opposes that tendency, so it acts forward on the crate.',
                    r'That forward friction is the only horizontal force on the crate, so it causes the crate’s acceleration. It does positive work on the crate.'],
             answer=r'Static friction from the floor, acting forward (in the direction of the truck’s acceleration)'),
    ],
    practice=[
        dict(q=r'A 5 kg block on a rough table is tied over a smooth pulley to a hanging 2 kg block. The least coefficient of static friction that keeps the system at rest is',
             options=['0.2', '0.4', '0.5', '2.5'], answer=1, type='numerical',
             explanation=r'At rest, friction on the table block must equal the hanging weight, 20 N. This needs μₛ × 50 ≥ 20, so μₛ ≥ 0.4. 0.2 uses the total mass 7 kg wrongly, and 2.5 inverts the ratio.'),
        dict(q=r'Blocks of 2 kg and 4 kg touch on a rough floor (μₖ = 0.2 for both). A 30 N horizontal force pushes the 2 kg block, which pushes the 4 kg block. The contact force between them is',
             options=['10 N', '12 N', '20 N', '30 N'], answer=2, type='numerical',
             explanation=r'System: friction = 0.2 × 60 = 12 N, so a = (30 − 12)/6 = 3 m/s². For the 4 kg block: contact force − 0.2 × 40 = 4 × 3, so contact force = 8 + 12 = 20 N. 12 N forgets the friction on the 4 kg block. 10 N splits the push by mass but gives the 2 kg block’s share, and 30 N ignores both friction and acceleration.'),
        dict(q=r'A crate lies on a truck floor with μₛ = 0.3 (g = 10 m/s²). The truck moves at 15 m/s. The shortest distance in which it can stop without the crate sliding is',
             options=['37.5 m', '75 m', '25 m', '50 m'], answer=0, type='numerical',
             explanation=r'Friction can decelerate the crate by at most μₛg = 3 m/s². The truck must not stop faster than that: s = 15²/(2 × 3) = 37.5 m. 75 m forgets the factor 2. 25 m and 50 m use the wrong deceleration.'),
        dict(q=r'Match each situation with the force that provides the needed horizontal acceleration.<br>(P) Car taking a turn on a level road (Q) Car taking a turn on a frictionless banked road at design speed (R) Crate on an accelerating truck floor (S) Coin on a rotating turntable<br>(1) Horizontal component of the normal force (2) Static friction toward the centre (3) Static friction in the direction of acceleration',
             options=['P-2, Q-1, R-3, S-2', 'P-1, Q-2, R-3, S-2', 'P-2, Q-1, R-2, S-3', 'P-3, Q-1, R-2, S-1'], answer=0, type='match',
             explanation=r'A level turn and a coin on a turntable both rely on static friction toward the centre (P-2, S-2). A frictionless bank uses the tilted normal force (Q-1). The crate is accelerated forward by static friction (R-3). Options that give the car on a level road the normal force miss that N is vertical there.'),
    ],
),
}


NEW_SECTIONS = [
dict(chapter='friction', after='friction-systems', id='friction-blocks',
     title='Block on block: moving together or slipping',
     intro=r'A small block m sits on a larger block M. A horizontal force acts on one of them. The only horizontal force between them is friction, so friction decides whether they move together or the top block slips.',
     reasoning=r'Always start by assuming no slipping. Find the common acceleration from the whole system, then find the friction the block <em>without</em> the applied force needs. If this is at most μₛmg, they move together. If not, they slip, and each block gets its own acceleration with kinetic friction μₖmg between them.',
     formula=r'F_{\max}=\mu_s(m+M)g\ \ (\text{force on lower block}),\qquad F_{\max}=\mu_smg\,\frac{m+M}{M}\ \ (\text{force on upper block})',
     symbols='m upper block (kg); M lower block (kg); μₛ static coefficient between the blocks; g = 10 m/s²; F_max largest force (N) for which they move together. Smooth floor in both results.',
     trap=r'When the force acts on the upper block, the limit is not μₛ(m + M)g. Friction now has to drag the lower block, so the limit is μₛmg(m + M)/M.',
     example=r'A 2 kg block sits on a 4 kg block on a smooth floor. μₛ between them is 0.3. What is the largest horizontal force on the upper block for which they move together?',
     solution=r'The lower block is driven only by friction, at most 0.3 × 20 = 6 N, so its largest acceleration is 6/4 = 1.5 m/s². Both move with 1.5 m/s², so F = 6 × 1.5 = 9 N. The formula gives μₛmg(m + M)/M = 6 × 6/4 = 9 N.',
     question=r'A 1 kg block rests on a 3 kg block on a smooth floor. μₛ between them is 0.5. The largest horizontal force on the lower block for which they move together is',
     options='5 N|15 N|20 N|40 N', answer=2,
     explanation=r'The upper block can be accelerated at most at μₛg = 5 m/s². Both blocks then need F = 4 × 5 = 20 N. 5 N is only the friction on the upper block, and 15 N uses the lower mass alone.',
     deep=dict(
        level='exam',
        notes=[
            ('Method: assume together, then check', r'''<ol><li><strong>Assume no slip.</strong> Common acceleration a = F/(m + M) (smooth floor).</li>
<li><strong>Isolate the block without F.</strong> Friction is the only horizontal force on it, so the friction needed is its mass times a.</li>
<li><strong>Compare</strong> with the limit μₛmg.
<ul><li>If needed ≤ limit: they move together, and friction equals the needed value (not μₛmg).</li>
<li>If needed &gt; limit: they slip. Use kinetic friction μₖmg on each block, in opposite directions.</li></ul></li></ol>'''),
            ('Derivation of the two limits', r'''<p><strong>Force F on the lower block.</strong> The upper block is carried by friction: m a ≤ μₛmg, so a ≤ μₛg. The pair then needs F = (m + M)a, giving F_max = μₛ(m + M)g.</p>
<p><strong>Force F on the upper block.</strong> Now the lower block is carried by friction: M a ≤ μₛmg, so a ≤ μₛmg/M. Hence F_max = (m + M)μₛmg/M.</p>
<p>Below either limit, the friction on the carried block is a fraction of F: f = mF/(m + M) in the first case and f = MF/(m + M) in the second.</p>'''),
            ('After slipping: separate accelerations and time to fall off', r'''<p>Take F on the lower block, smooth floor, F above the limit.</p>
<ul><li>Upper block: only kinetic friction acts, forward: a_m = μₖg (independent of F).</li>
<li>Lower block: a_M = (F − μₖmg)/M.</li>
<li>Relative acceleration a_rel = a_M − a_m. The upper block slides backward relative to the lower one (but still moves forward relative to the ground).</li>
<li>If it must slide a length L to fall off, starting from rest relative to M: t = √(2L/a_rel).</li></ul>
<p>With a rough floor (coefficient μ₂), add the floor friction μ₂(m + M)g on the lower block. Its normal force from the floor is the weight of both blocks.</p>'''),
        ],
        formulas=[
            dict(title='After slipping (force on lower block, smooth floor)',
                 formula=r'a_m=\mu_kg,\qquad a_M=\frac{F-\mu_kmg}{M},\qquad t_{\rm off}=\sqrt{\frac{2L}{a_M-a_m}}',
                 symbols='a_m, a_M ground-frame accelerations of the upper and lower blocks (m/s²); μₖ kinetic coefficient between blocks; F applied force (N); L distance the top block must slide relative to the lower one (m); t_off time (s).'),
            dict(title='Lower block on a rough floor, force on lower block',
                 formula=r'F_{\max}=(\mu_1+\mu_2)(m+M)g',
                 symbols='μ₁ static coefficient between the blocks; μ₂ coefficient between lower block and floor; m, M masses (kg); g = 10 m/s². Largest force for which both move together.'),
        ],
        figure=dict(svg=FIG_STACK, caption='Friction between stacked blocks is an action–reaction pair. With F on the lower block, friction pulls the upper block forward and the lower block backward.'),
        traps=[r'While the blocks move together, the friction between them is not μₛmg. It is only what the carried block needs, m × a.',
               r'After slipping, the upper block still moves forward in the ground frame. It only slides backward relative to the lower block.'],
        exam=r'''<ul><li>"Find the maximum force on the lower (or upper) block so that the blocks move together."</li>
<li>"F = … N acts on the lower block. Find the friction between the blocks." (Check slip first.)</li>
<li>Find both accelerations after slipping, and the time for the top block to fall off a plank of length L.</li>
<li>Graph of friction on the upper block against F: a rising line, then a flat kinetic level.</li></ul>''',
        examples=[
            dict(tag='Numerical', q=r'A 2 kg block sits at the front end of a 4 kg plank 1.5 m long on a smooth floor. μₛ = μₖ = 0.3 between them. A 30 N force pulls the plank forward. Find the two accelerations and the time for the block to slide off the back.',
                 steps=[r'Limit for moving together: μ(m + M)g = 0.3 × 6 × 10 = 18 N. 30 N &gt; 18 N, so they slip.',
                        r'Block: a_m = μg = 3 m/s² (forward).',
                        r'Plank: a_M = (30 − 0.3 × 20)/4 = 24/4 = 6 m/s².',
                        r'Relative acceleration 3 m/s². t = √(2 × 1.5/3) = 1 s.'],
                 answer=r'3 m/s² and 6 m/s²; the block falls off after 1 s'),
            dict(tag='Graph', q=r'A force F on the lower block grows from zero. Describe the graph of friction on the upper block against F (m on M, smooth floor).',
                 steps=[r'Moving together: f = m × F/(m + M). This is a straight line through the origin with slope m/(m + M), less than 1.',
                        r'The line ends at F = μₛ(m + M)g, where f = μₛmg.',
                        r'Beyond that the blocks slip, and f = μₖmg, a constant horizontal line (a small drop if μₖ &lt; μₛ).'],
                 answer=r'A rising line of slope m/(m + M), then a flat line at μₖmg'),
            dict(tag='Numerical', q=r'A 1 kg block sits on a 2 kg block. μ₁ = 0.4 between them and μ₂ = 0.1 between the lower block and the floor. Find the largest horizontal force on the lower block for which they move together.',
                 steps=[r'The upper block can accelerate at most at μ₁g = 4 m/s².',
                        r'Floor friction on the lower block = μ₂(1 + 2)g = 3 N (both blocks press on the floor).',
                        r'Whole system: F − 3 = 3 × 4, so F = 15 N.',
                        r'Formula check: (μ₁ + μ₂)(m + M)g = 0.5 × 30 = 15 N.'],
                 answer=r'15 N'),
        ],
        practice=[
            dict(q=r'A 1 kg block lies on a 4 kg block on a smooth floor. μₛ between them is 0.5 (g = 10 m/s²). The largest horizontal force on the <em>upper</em> block for which they move together is',
                 options=['5 N', '25 N', '20 N', '6.25 N'], answer=3, type='numerical',
                 explanation=r'The lower block is carried only by friction, at most 5 N, so a ≤ 5/4 = 1.25 m/s². Then F = 5 × 1.25 = 6.25 N. 25 N wrongly uses μ(m + M)g, which applies only when the force acts on the lower block. 5 N is just the friction limit; it forgets that F must also accelerate the upper block itself.'),
            dict(q=r'A 2 kg block lies on a 4 kg block on a smooth floor; μₛ = 0.4 between them. A 12 N horizontal force acts on the lower block. The friction on the upper block is',
                 options=['8 N', '4 N', '12 N', '0 N'], answer=1, type='numerical',
                 explanation=r'Limit for moving together: 0.4 × 6 × 10 = 24 N, more than 12 N, so no slip. Common a = 12/6 = 2 m/s². The upper block needs 2 × 2 = 4 N of friction. 8 N is the maximum, μₛmg, which is not reached. Friction cannot be zero because the upper block accelerates.'),
            dict(q=r'Force F on the lower block is large enough for the blocks to slip (smooth floor). Which statements are correct?<br>(i) The upper block’s acceleration is μₖg, whatever the value of F.<br>(ii) Friction on the lower block from the upper block acts forward.<br>(iii) The upper block moves backward relative to the lower block.<br>(iv) Increasing F increases the friction between the blocks.',
                 options=['(i) and (iii) only', '(ii) and (iv) only', '(i), (ii) and (iii)', '(iii) and (iv) only'], answer=0, type='multi',
                 explanation=r'Kinetic friction μₖmg is the only horizontal force on the upper block, so (i) is true and (iv) is false. The lower block runs ahead, so the upper block slides back relative to it (iii true), and the friction on the lower block acts backward (ii false).'),
            dict(q=r'<strong>Assertion (A):</strong> When blocks slip because a large force acts on the lower block, the upper block moves backward relative to the ground.<br><strong>Reason (R):</strong> The friction on the upper block acts in the direction of the applied force.',
                 options=AR, answer=3, type='ar',
                 explanation=r'R is true: friction drags the upper block forward. Because of that forward friction, the upper block accelerates forward at μₖg in the ground frame. It moves backward only relative to the lower block. So A is false and R is true.'),
        ],
     )),

dict(chapter='friction', after='friction-blocks', id='friction-rolling',
     title='Rolling friction, lubrication and why we need friction',
     intro=r'A wheel rolling on a road meets far less resistance than a box sliding on it. Rolling friction comes from the small dent the wheel and road make at the contact. The material in front is squashed and does not spring back fully, so a little energy is lost each turn.',
     reasoning=r'Typical coefficients: sliding friction 0.1 to 1, rolling friction about 0.001 to 0.01. That is why the wheel, ball bearings and roller bearings are such powerful inventions. Friction is still essential: without it we could not walk, drive, brake, hold a pen or tie a knot.',
     formula=r'f_{\rm roll}=\mu_rN,\qquad \mu_r\ll\mu_k<\mu_s',
     symbols='f_roll rolling resistance (N); μᵣ coefficient of rolling friction (no unit, typically 0.001 to 0.01); N normal force (N); μₖ, μₛ sliding coefficients. Rolling friction also falls as the wheel radius increases.',
     trap=r'Rolling friction is not the static friction at the contact of an ideal rolling wheel. In ideal pure rolling on rigid surfaces, static friction does no work. Rolling resistance appears only because real surfaces deform.',
     example=r'A 50 kg trolley has μᵣ = 0.02. The same load dragged on its base would have μₖ = 0.4. Compare the forces needed to keep it moving at constant speed.',
     solution=r'Rolling: 0.02 × 500 = 10 N. Sliding: 0.4 × 500 = 200 N. Wheels reduce the force 20 times.',
     question=r'Ball bearings reduce friction in machines mainly because they',
     options='make the surfaces smoother|replace sliding friction by rolling friction|reduce the normal force|increase the contact area',
     answer=1,
     explanation=r'Steel balls roll between the races, so the parts no longer slide over each other. Rolling friction is far smaller. The normal force is unchanged, and contact area does not set friction.',
     deep=dict(
        level='basic',
        notes=[
            ('Ways to reduce friction', r'''<ul><li><strong>Lubrication:</strong> oil or grease puts a thin fluid layer between the surfaces. Solid–solid friction is replaced by the much smaller fluid (viscous) friction.</li>
<li><strong>Ball and roller bearings:</strong> replace sliding by rolling.</li>
<li><strong>Air cushion:</strong> a hovercraft or air-track glider floats on a thin layer of air.</li>
<li><strong>Polishing:</strong> reduces the high points, but only up to a point. Very highly polished flat surfaces can have <em>more</em> friction, because more atoms come close enough to bond (adhesion).</li>
<li><strong>Streamlining:</strong> reduces fluid friction (drag) on vehicles and aircraft.</li></ul>'''),
            ('Friction as a helper: walking, cycles and cars', r'''<ul><li><strong>Walking:</strong> your foot pushes backward on the ground. The ground’s static friction on the foot points forward and drives you ahead.</li>
<li><strong>Bicycle being pedalled:</strong> the rear wheel is driven, its bottom tends to slip backward, so friction on the rear wheel acts forward. The front wheel is pushed along, so friction on it acts backward and simply makes it turn.</li>
<li><strong>Bicycle freewheeling</strong> (no pedalling): friction on both wheels acts backward.</li>
<li><strong>Car tyres</strong> have treads so water is pushed out, keeping contact and friction on wet roads.</li>
<li>Friction is also why nails and screws hold, why brakes work, and why belts drive pulleys.</li></ul>'''),
        ],
        traps=[r'Friction does not always oppose motion of the body. When you walk, friction on your foot acts forward, in your direction of motion.',
               r'Making surfaces extremely smooth does not always reduce friction. Very flat polished surfaces can stick together strongly.'],
        exam=r'''<ul><li>"Direction of friction on the front and rear wheels of a bicycle being pedalled" (rear forward, front backward).</li>
<li>"Friction is a necessary evil": statement or multiple-correct questions on its uses.</li>
<li>"Why are ball bearings used?" and "Why does lubrication reduce friction?"</li>
<li>Comparing rolling, kinetic and static coefficients: μᵣ &lt; μₖ &lt; μₛ.</li></ul>''',
        examples=[
            dict(tag='Conceptual', q=r'A person walks forward on a level road. What is the direction of the friction force on the person’s foot, and what does it do?',
                 steps=[r'To walk, the foot pushes the ground backward.',
                        r'Without friction the foot would slip backward, so static friction on the foot acts forward.',
                        r'This forward friction is the external force that accelerates the person. On ice, friction is small and the foot slips.'],
                 answer=r'Forward; it is the external force that moves the person ahead'),
            dict(tag='Assertion–Reason', q=r'<strong>A:</strong> It is easier to roll a heavy drum than to drag it.<br><strong>R:</strong> Rolling friction is much smaller than sliding friction.',
                 steps=[r'Both statements are true.',
                        r'Dragging needs μₖN with μₖ around 0.3 to 0.5; rolling needs μᵣN with μᵣ around 0.01.',
                        r'R gives the reason for A.'],
                 answer=r'Both true; R correctly explains A'),
        ],
        practice=[
            dict(q=r'A bicycle is being pedalled forward on a level road. The friction forces on the rear and front wheels act',
                 options=['both forward', 'both backward', 'rear backward, front forward', 'rear forward, front backward'], answer=3, type='concept',
                 explanation=r'The pedals turn the rear wheel, whose contact point tends to slip backward, so friction on it is forward and drives the cycle. The front wheel is pushed by the frame and tends to skid forward, so friction on it acts backward and makes it spin. "Both backward" is the freewheeling case.'),
            dict(q=r'Which of the following methods reduce friction?<br>(i) Lubricating with oil (ii) Using ball bearings (iii) Increasing the normal force (iv) Streamlining a car body',
                 options=['(i) and (ii) only', '(i), (ii) and (iv)', '(ii) and (iii) only', 'All four'], answer=1, type='multi',
                 explanation=r'Oil, bearings and streamlining all reduce friction or drag. Increasing the normal force raises friction, since f ∝ N, so (iii) is wrong and any option containing it is wrong.'),
            dict(q=r'A 200 kg cart moves at constant speed on a level road. The rolling friction coefficient is 0.005 (g = 10 m/s²). The horizontal force needed is',
                 options=['1 N', '10 N', '100 N', '1000 N'], answer=1, type='numerical',
                 explanation=r'At constant speed the pull balances rolling friction: 0.005 × 2000 = 10 N. 100 N and 1000 N are what much larger sliding coefficients would give. 1 N slips a factor of ten.'),
            dict(q=r'<strong>Statement I:</strong> Polishing two metal surfaces always reduces the friction between them.<br><strong>Statement II:</strong> Lubricants reduce friction by replacing solid–solid contact with a fluid layer.',
                 options=ST, answer=3, type='statement',
                 explanation=r'Statement I is false: beyond a point, very flat clean surfaces show increased friction because adhesion between atoms grows. Statement II is true.'),
        ],
     )),
]
