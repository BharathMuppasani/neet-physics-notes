"""Independently solved, original-worded adaptations of selected Exemplar patterns.
These are NOT labelled NEET past-year questions. The collector imports metadata,
not solutions. Each record names the exact source question and teaching anchor.
"""
QUESTIONS=[]
def add(ch, no, topic, question, opts, ans, solution):
    QUESTIONS.append(dict(id=f'ex-{ch:02}-{no:02}',src='ex',qno=f'{ch}.{no}',topic=topic,
        type='concept' if not any(x.isdigit() for x in question) else 'numerical',q=question,
        opts=opts.split('|'),ans=ans,sol='<p>'+solution+'</p>',
        reference=dict(url=f'https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep3{ch:02}.pdf',
                       question=f'{ch}.{no}',label='Adapted NCERT Exemplar pattern',review='independently solved')))
add(2,1,'units-significant','How many significant figures are reported in 0.008700?',
    '2|3|4|6',2,'The leading zeros locate the decimal point. The digits 8, 7, 0 and 0 are significant, giving four. Trailing decimal zeros record precision; they are not discarded.')
add(2,6,'units-dimensions','Which pair has different dimensions?',
    'Energy and torque|Impulse and momentum|Force and surface tension|Angular momentum and action',2,'Force has dimensions MLT⁻², while surface tension is force per length with dimensions MT⁻². The other three pairs match dimensionally, although they describe distinct quantities.')
add(3,4,'linear-averages','A runner covers equal distances at 6 and 12 m/s. What is the average speed?',
    '8 m/s|9 m/s|10 m/s|18 m/s',0,'For each leg distance d, total time is d/6+d/12=d/4. Total distance is 2d, so average speed is 8 m/s. The arithmetic mean assumes equal times.')
add(3,5,'linear-position','Position is x=(t−3)² m with t in seconds. Over t=0 to 6 s, what distance is travelled?',
    '0 m|9 m|18 m|36 m',2,'Position starts at 9 m, decreases to 0 at t=3 s, then returns to 9 m. Distance is 9+9=18 m; displacement is zero. The turning time comes from v=2(t−3).')
add(4,1,'vectors-dot',r'The vectors \(\vec A=2\hat i+2\hat j\) and \(\vec B=3\hat i-3\hat j\) make what angle?',
    '0°|45°|90°|180°',2,'Their dot product is 2×3+2×(−3)=0. Both vectors are nonzero, so they are perpendicular. Opposite signs in one component do not mean the whole vectors are antiparallel.')
add(4,5,'plane-projectiles','On level ground a projectile has range 40 m at 15°. At the same speed, what is its range at 45°?',
    '40 m|40√2 m|80 m|160 m',2,'Range scales with sin(2θ). The first sine is sin30°=1/2 and the second is sin90°=1, giving twice the range, 80 m. Equal launch and landing heights are essential.')
add(5,7,'laws-newton','A 2 kg particle has x=2t+3t²+4t³ in SI units. What net force acts at t=1 s?',
    '12 N|24 N|30 N|60 N',3,'Differentiate twice: a=6+24t. At 1 s a=30 m/s² and F=ma=60 N. A single derivative would give velocity, not acceleration.')
add(5,11,'friction-systems','A 1 kg block sits on a 2 kg block on a smooth floor. Their static coefficient is 0.2. With g=10, what is the largest horizontal force on the lower block for motion together?',
    '2 N|4 N|6 N|10 N',2,'The top block can be accelerated at most at μₛg=2 m/s². The combined mass is 3 kg, so maximum external force is 3×2=6 N. Internal friction cancels only for the combined-system equation.')
add(6,7,'work-conservation','Two particles start from rest on smooth straight inclines of equal vertical height. One incline is steeper. What happens at the bottom?',
    'Same speed; steeper path arrives earlier|Same speed and same arrival time|Steeper path has lower speed|Shallower path arrives earlier',0,'Energy gives v=√(2gh) for either path. For a straight incline, a=g sinθ and length=h/sinθ, so time=√(2h/g)/sinθ. The steeper incline arrives earlier.')
add(6,16,'work-conservation','A 2 kg ball is thrown at 3 m/s from 4 m above ground. Ignoring drag with g=10, what is its impact kinetic energy?',
    '9 J|40 J|80 J|89 J',3,'Initial kinetic energy is ½×2×3²=9 J. Falling adds mgh=80 J, so final K=89 J. Launch direction changes the trajectory, not this energy balance.')
add(7,1,'rotation-centre','Which uniform object has its centre of mass in an empty region?',
    'Solid ball|Thin circular ring|Solid cube|Straight solid rod',1,'The ring’s symmetry places its centre of mass at the circle centre, where there is no ring material. The centre of mass need not be inside the matter.')
add(7,4,'rotation-angular','A rigid disc rotates about a fixed axis with constant nonzero angular velocity. Which quantity is zero?',
    'Angular acceleration|Angular speed|Rim speed|Radial acceleration of a rim point',0,'Constant angular velocity gives α=0. Rim speed stays nonzero and its direction changes, requiring radial acceleration ω²r.')
add(8,6,'gravitation-kepler','A small asteroid is gravitationally bound to a dominant star. In the ideal two-body approximation, its small mass means',
    'It cannot orbit|It obeys Kepler’s laws like a planet|Its gravity must be repulsive|Its orbital period is zero',1,'Gravitational acceleration GM/r² does not depend on the asteroid’s mass. Bound inverse-square two-body trajectories and periods obey Kepler’s laws; small mass is not a barrier to orbiting.')
add(8,8,'gravitation-field','Fixed masses 2M and M are separated by 3d. A test mass lies distance d from 2M and 2d from M. Its initial gravitational acceleration points',
    'Toward 2M|Toward M|Nowhere; fields cancel|Perpendicular to the line',0,'The competing field magnitudes are 2GM/d² and GM/(4d²). The first is eight times the second, so the net field points toward 2M. Here source masses are explicitly fixed.')
add(9,1,'shear','An ideal fluid in static equilibrium can sustain what shear stress without flowing?',
    'Any shear stress|A fixed positive shear stress|No shear stress|Only infinite shear stress',2,'An ideal static fluid has zero shear modulus and cannot sustain tangential stress. Pressure can still be nonzero because it is normal stress, not shear.')
add(9,2,'applications','A uniform wire is cut to half its length while retaining its cross-section. Its ideal breaking load is',
    'Halved|Unchanged|Doubled|Quadrupled',1,'Breaking load equals breaking stress times cross-sectional area. The material and area remain the same, so the load threshold is unchanged. Elastic extension, unlike breaking load, depends on length.')
add(10,4,'continuity','An incompressible fluid flows steadily through pipe diameters 2 cm and 4 cm. The speed in the narrow section divided by the wide-section speed is',
    '1/4|1/2|2|4',3,'Av is constant and circular area scales as diameter squared. Thus v_narrow/v_wide=(4/2)²=4. Doubling diameter quadruples area.')
add(10,5,'contact-angle','A capillary liquid surface is convex and its contact angle exceeds 90°. The liquid tends to',
    'Rise above the reservoir|Be depressed below the reservoir|Have zero surface tension|Have zero density',1,'For θ>90°, cosθ<0 in h=2S cosθ/(ρgr), so h is negative: capillary depression. A convex nonwetting meniscus is consistent with this result.')
add(11,1,'thermal-properties-expansion','Bonded metal strips A and B are heated, with A having the larger expansion coefficient. In the resulting bend, A lies on the',
    'Shorter inner side|Longer outer side|Neutral axis only|Same curve length as B',1,'The more-expanding layer wants a greater length and forms the outer convex side. The smaller-expanding layer is on the concave side; bonding forces the pair to bend.')
add(11,4,'thermal-properties-liquids','A fixed-volume fully submerged object displaces pure water at 0°C and at 4°C. Buoyant force is larger at',
    '0°C|4°C|Both equally|Neither because buoyancy vanishes',1,'Buoyancy is ρ_water g V. Pure water is denser near 4°C, so buoyancy is larger there for the stated unchanged displaced volume. This comparison isolates water’s density effect.')
add(12,5,'thermodynamics-adiabatic','Identical ideal gases start at the same state. Each is reversibly compressed to half its volume: A isothermal, B adiabatic with γ=1.4. Final p_B/p_A is',
    '1|2⁰·⁴|2¹·⁴|2',1,'For A, p_A=2p₀. For B, p_B=2^γ p₀. Their ratio is 2^(γ−1)=2^0.4, about 1.32. The adiabatic gas also warms; the isothermal gas rejects heat.')
add(12,8,'thermodynamics-isothermal','For a reversible ideal-gas isothermal expansion, which relation is correct?',
    'Q=0 and W>0|ΔU=0 and Q=W|ΔU=Q and W=0|Temperature increases',1,'For an ideal gas U depends only on temperature, so ΔU=0. The first law then requires supplied heat to equal the positive expansion work. Isothermal is not adiabatic.')
add(13,3,'kinetic-theory-gas-law','A fixed amount of ideal gas obeys pV=constant during a process. That process is',
    'Isothermal|Isochoric heating|Isobaric heating|Necessarily adiabatic',0,'pV=nRT, so at fixed amount a constant product requires constant absolute temperature. An adiabatic process instead generally follows pV^γ=constant when reversible.')
add(13,6,'kinetic-theory-mixtures','In a fixed volume, a diatomic ideal gas completely dissociates into atoms while temperature rises from 300 to 900 K. What is final pressure divided by initial pressure?',
    '2|3|6|9',2,'Each molecule becomes two particles, doubling N. Absolute temperature triples. Since p∝NT at fixed volume, pressure becomes 2×3=6 times the initial value.')
add(14,6,'oscillations-superposition',r'For \(x=6\sin\omega t+8\cos\omega t\) cm, the amplitude is',
    '2 cm|7 cm|10 cm|14 cm',2,'Sine and cosine differ by π/2. The combined amplitude is √(6²+8²)=10 cm. Adding 6+8 would require matching phases.')
add(14,4,'oscillations-superposition','The total liquid length in an ideal U-tube is doubled. Its small-oscillation period changes by',
    'A factor of 2|A factor of √2|A factor of 1/2|No change',1,'T=2π√(L/2g) for a uniform U-tube with negligible viscosity. Doubling total moving liquid length multiplies the period by √2.')
add(15,2,'waves-travelling','A wave enters a stationary new medium where its propagation speed is three times greater. Its wavelength becomes',
    'One third|Unchanged|Three times|Nine times',2,'The frequency is set by the source and is unchanged across a stationary boundary. With λ=v/f, tripling speed triples wavelength.')
add(15,4,'waves-speed','A fixed-frequency sound source remains unchanged while the air warms and sound speed increases. The wavelength',
    'Decreases|Increases|Must stay fixed|Becomes the frequency',1,'The source frequency is fixed; λ=v/f therefore increases when speed increases. Medium temperature changes propagation speed, not the unchanged source’s frequency.')
