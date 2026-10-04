"""Original mixed-step NEET-style practice, separate from retrieval checks."""
QUESTIONS=[]
def add(topic,q,opts,ans,sol,type='numerical'):
    QUESTIONS.append(dict(id='c11-'+topic+'-challenge',src='c11',qno='Challenge',topic=topic,type=type,difficulty='challenge',q=q,opts=opts.split('|'),ans=ans,sol='<p>'+sol+'</p>'))
add('maths-ratios','A quantity scales as Q ∝ x²/√y. If x increases by 20% and y becomes four times its original value, the new Q/Q₀ is',
    '0.60|0.72|1.20|2.88',1,'x becomes 1.2x₀, giving a squared factor 1.44. The denominator grows by √4=2. Thus Q/Q₀=1.44/2=0.72, a 28% decrease. Percentage changes cannot be added directly.')
add('maths-integrals','A force follows F=2x N, with x in metres. What is the area under the force–position curve between x=1 and x=3 m?',
    '4 J|6 J|8 J|12 J',2,'Integrate 2x from 1 to 3: x² evaluated at the limits gives 9−1=8 J. The initial lower limit is not zero; using only the final value gives too much work.')
add('units-propagation','For T=2π√(ℓ/g), worst-case uncertainties in ℓ and g are 2% and 4%. The first-order uncertainty in T is',
    '1%|2%|3%|6%',2,'The powers are +1/2 and −1/2. Sum their absolute-weight contributions: ½×2%+½×4%=3%. The minus sign in the exponent does not subtract uncertainties.')
add('units-significant','A measured mass of 5.43 g is divided by a measured volume of 2.1 cm³. The appropriately reported density is',
    '2.5857 g/cm³|2.586 g/cm³|2.59 g/cm³|2.6 g/cm³',3,'The unrounded ratio is 2.5857… g/cm³. Volume has two significant figures, so the final product/quotient should have two: 2.6 g/cm³.')
add('linear-equations','A particle starts at x=0 with velocity +12 m/s and constant acceleration −4 m/s². In the first 5 s, distance and displacement are',
    '10 m, 10 m|26 m, 10 m|18 m, 26 m|26 m, −10 m',1,'Velocity vanishes at 3 s. Position there is 18 m. At 5 s position is 12×5−2×25=10 m. The return distance is 8 m, so total distance is 18+8=26 m, while displacement is +10 m.')
add('linear-relative','A walker takes 30 s to climb a stationary escalator. The escalator alone takes 60 s to carry a standing person. At the same walking rate on the moving escalator, climb time is',
    '15 s|20 s|30 s|45 s',1,'For escalator length L, walking speed is L/30 and escalator speed L/60. They add to L/20, so the climb takes 20 s. Times themselves do not add.')
add('vectors-addition','Vectors of magnitudes 3 and 4 units have resultant magnitude 5 units. Their included angle is',
    '0°|60°|90°|180°',2,'Use 25=9+16+24 cosθ. Thus cosθ=0 and θ=90°. The 3–4–5 values reflect perpendicular components, not parallel addition.')
add('vectors-dot',r'The projection of \(\vec A=6\hat i+8\hat j\) m along the direction of \(\vec B=\hat i\) is',
    '6 m|8 m|10 m|14 m',0,'The signed projection is A·B/|B|. Here it is 6 m. The 10 m magnitude contains both components and is not the projection onto +x.')
add('plane-relative','A swimmer moves at 4 m/s relative to water across a 60 m river flowing at 3 m/s. For the shortest crossing time, the downstream drift is',
    '0 m|15 m|45 m|60 m',2,'Shortest time uses the entire swimming speed across: 60/4=15 s. The current carries the swimmer 3×15=45 m downstream. A directly opposite crossing needs an upstream component and takes longer.')
add('plane-horizontal','A particle launches horizontally at 15 m/s from height 20 m, with g=10 m/s² and no drag. Impact speed is',
    '15 m/s|20 m/s|25 m/s|35 m/s',2,'Fall time is 2 s, so vertical impact speed is 20 m/s. Horizontal speed remains 15 m/s. Combining perpendicular components gives √(225+400)=25 m/s.')
add('laws-connected','A 2 kg block on a smooth horizontal table is tied over an ideal fixed pulley to a hanging 3 kg mass. Use g=10. The acceleration and tension are',
    '6 m/s², 12 N|10 m/s², 20 N|6 m/s², 30 N|2 m/s², 24 N',0,'The only driving force for the combined system is the hanging weight 30 N, so a=30/(2+3)=6 m/s². For the table block T=2a=12 N. This is not the two-hanging-mass Atwood formula.')
add('laws-impulse','A 0.1 kg ball approaches a bat at 20 m/s and returns at 30 m/s. Contact lasts 0.005 s. Average force magnitude on the ball is',
    '200 N|400 N|600 N|1000 N',3,'Use signed velocities +20 and −30 m/s. Momentum change is 0.1(−30−20)=−5 N s. Dividing its magnitude by 0.005 s gives 1000 N; subtracting speed magnitudes would miss reversal.')
add('friction-pulling','A 5 kg block on a horizontal floor is pulled by 25 N at an angle with cosθ=0.8 and sinθ=0.6. With μₖ=0.2 and g=10, its acceleration while sliding in the pull direction is',
    '1.4 m/s²|2.6 m/s²|4.0 m/s²|5.0 m/s²',1,'Vertical pull is 15 N, so N=50−15=35 N. Sliding friction is 7 N. Horizontal pull is 20 N; net force is 13 N, giving a=13/5=2.6 m/s².')
add('friction-static','A stationary 2 kg block has μₛ=0.4 and μₖ=0.3 on a level floor. With g=10, a 7 N horizontal pull acts. Its acceleration is',
    '0|0.5 m/s²|3.5 m/s²|4 m/s²',0,'The static limit is 0.4×20=8 N. The 7 N pull can be balanced by 7 N static friction, so acceleration is zero. Kinetic friction is inappropriate because sliding has not begun.')
add('work-collisions','A 2 kg mass moving at 6 m/s catches and sticks to a 1 kg mass moving at 3 m/s in the same direction. Kinetic energy lost is',
    '0 J|3 J|9 J|12 J',1,'Momentum is 2×6+1×3=15 kg m/s, so common speed is 5 m/s. Initial K=36+4.5=40.5 J; final K=½×3×25=37.5 J. Loss is 3 J. Both initial momenta have the same sign.')
add('work-theorem','A 1 kg particle starts from rest under force F=4x N along a straight path. At x=2 m, its speed is',
    '2 m/s|4 m/s|8 m/s|16 m/s',1,'Work from 0 to 2 m is ∫4x dx=2x² evaluated at 2, or 8 J. By work–energy, ½v²=8 and v=4 m/s. Using the final force as constant overestimates work.')
add('rotation-rolling','A uniform disc rolls without slipping from rest through a vertical drop of 3 m. Use g=10 and neglect dissipation. Its centre speed at the bottom is',
    '√20 m/s|√40 m/s|√60 m/s|√90 m/s',1,'For a disc, K=3Mv²/4. Set Mgh=3Mv²/4, giving v²=4gh/3=40. Rotational energy makes centre speed lower than a purely sliding particle’s √60 m/s.')
add('rotation-momentum','With zero external torque, a rotor’s inertia decreases from 6 to 2 kg m². Initially ω=2 rad/s. Final angular speed and final kinetic energy are',
    '2 rad/s, 4 J|6 rad/s, 12 J|6 rad/s, 36 J|4 rad/s, 16 J',2,'Initial angular momentum is 12 kg m²/s. Final ω=12/2=6 rad/s and K=½×2×36=36 J. Initial K was 12 J; the rearrangement supplies the 24 J increase.')
add('gravitation-orbits','Two circular satellites orbit the same planet at radii r and 4r. The outer satellite’s period divided by the inner’s is',
    '2|4|8|16',2,'Circular period scales as r³/². Thus (4r/r)³/²=8. Speed decreases with radius while orbit circumference increases, so period grows faster than linearly.')
add('gravitation-escape','At a planet’s surface, circular orbital speed is 8 km/s. Ignoring atmosphere and rotation, escape speed is',
    '4√2 km/s|8 km/s|8√2 km/s|16 km/s',2,'At the same radius, escape speed is √2 times circular speed. Thus it is 8√2 km/s, approximately 11.3 km/s; escape is not merely maintaining a bound orbit.')
add('oscillations-velocity','In SHM with amplitude A and angular frequency ω, speed at x=A/2 divided by maximum speed is',
    '1/2|1/√2|√3/2|1',2,'Speed is ω√(A²−x²). At x=A/2 this is ωA√3/2; divide by maximum speed ωA to get √3/2. Half displacement does not imply half speed.')
add('oscillations-springs','Two identical springs k each support the same mass first in series and then in parallel. Period in series divided by period in parallel is',
    '1/2|1|√2|2',3,'Effective constants are k/2 and 2k. Since T∝1/√k_eff, the ratio is √[(2k)/(k/2)]=2. The two arrangements differ in stiffness by four.')
add('waves-modes','At sound speed 340 m/s, a closed pipe and an open pipe have the same fundamental frequency 170 Hz. Their effective lengths (closed, open) are',
    '0.5 m, 1 m|1 m, 0.5 m|1 m, 1 m|0.25 m, 0.5 m',0,'Closed-pipe fundamental is v/(4L), giving L=340/(4×170)=0.5 m. Open-pipe fundamental is v/(2L), giving 1 m. Boundary conditions change the allowed fundamental wavelength.')
add('waves-doppler','A stationary 600 Hz source is heard by an observer approaching at 30 m/s. Sound speed is 330 m/s. Observed frequency is',
    '550 Hz|600 Hz|650 Hz|600×12/11 Hz',3,'For a moving observer and stationary source, f′=f(v+v_o)/v=600×360/330=600×12/11≈654.5 Hz. A moving-source denominator would describe a different problem.')
add('thermal-properties-calorimetry','Equal masses of materials with specific heats c and 3c start at 80°C and 20°C respectively. In an insulated negligible-capacity container, final temperature is',
    '35°C|50°C|65°C|70°C',0,'Heat balance gives c(80−T)=3c(T−20), so 80−T=3T−60 and T=35°C. The colder sample has three times the heat capacity, so the final temperature lies closer to 20°C.')
add('thermal-properties-latent','An insulated mixture has 0.1 kg ice at 0°C and 0.1 kg water at 50°C. Use water c=4200 J/kg K and ice fusion latent heat 336000 J/kg. What happens?',
    'All ice melts and final temperature is positive|All ice melts exactly at 0°C|Some ice remains at 0°C|All water freezes',2,'Cooling water to 0°C supplies 0.1×4200×50=21000 J. Melting all ice needs 33600 J. Only 21000/336000=0.0625 kg melts, leaving 0.0375 kg ice at 0°C.')
add('kinetic-theory-speeds','At equal temperature, compare rms molecular speeds of hydrogen (2 g/mol) and oxygen (32 g/mol). The ratio v_H₂/v_O₂ is',
    '2|4|8|16',1,'v_rms∝1/√M at fixed T, so ratio is √(32/2)=4. The molar masses can be used as a ratio in the same units; the lighter molecules are faster.')
add('kinetic-theory-equipartition','At ordinary temperatures with rotations active and vibrations inactive, 2 mol of a diatomic ideal gas at 300 K has internal energy',
    '900R J|1200R J|1500R J|2100R J',2,'With f=5, U=(5/2)nRT=(5/2)×2×R×300=1500R J. Using 3RT/2 per mole counts translational energy only and misses active rotations.')
add('thermodynamics-cycles','A cyclic engine absorbs 1200 J and rejects 900 J each cycle. Running at 4 cycles per second, useful power is',
    '300 W|900 W|1200 W|4800 W',2,'Net work per cycle is 1200−900=300 J. Four cycles per second give 1200 J/s=1200 W. Efficiency is 25%; heat input rate is not useful output power.')
add('thermodynamics-second-law','A reversible refrigerator operates between 270 K and 300 K and receives 100 J of work per cycle. Maximum heat removed from the cold side is',
    '100 J|300 J|900 J|1000 J',2,'Carnot refrigerator COP=270/(300−270)=9. Therefore Q_c=COP×W=900 J. It rejects Q_h=Q_c+W=1000 J to the hot side; that is not the removed cold-side heat.')
