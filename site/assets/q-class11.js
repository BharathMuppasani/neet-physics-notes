/* Original concept checks + reviewed NCERT Exemplar adaptations. */
window.QBANK = window.QBANK || [];
window.QBANK.push(...[
  {
    "id": "c11-maths-models",
    "src": "c11",
    "qno": "maths · 1",
    "topic": "maths-models",
    "type": "concept",
    "q": "Which task requires treating a wheel as an extended body?",
    "opts": [
      "Converting its speed to SI",
      "Timing a straight journey",
      "Finding its centre’s displacement",
      "Calculating its rotational kinetic energy"
    ],
    "ans": 3,
    "sol": "<p>Rotational energy depends on the mass distribution through the moment of inertia. Centre motion, unit conversion and elapsed time do not require that distribution.</p>"
  },
  {
    "id": "c11-maths-ratios",
    "src": "c11",
    "qno": "maths · 2",
    "topic": "maths-ratios",
    "type": "numerical",
    "q": "A quantity obeys Q ∝ r²/L. If r doubles and L triples, Q becomes",
    "opts": [
      "2/3 of Q",
      "4/3 of Q",
      "6Q",
      "12Q"
    ],
    "ans": 1,
    "sol": "<p>The radius contributes a factor of four and the length contributes one-third, so the total factor is 4/3. Adding the changes would ignore the multiplicative relationship.</p>"
  },
  {
    "id": "c11-maths-trig",
    "src": "c11",
    "qno": "maths · 3",
    "topic": "maths-trig",
    "type": "numerical",
    "q": "At a small angle of 0.04 rad, sin θ is approximately",
    "opts": [
      "0.04",
      "4",
      "0.0008",
      "1"
    ],
    "ans": 0,
    "sol": "<p>In radians, the small-angle sine is approximately the angle itself. The correction starts at order θ³; 1 is instead the approximate cosine.</p>"
  },
  {
    "id": "c11-maths-graphs",
    "src": "c11",
    "qno": "maths · 4",
    "topic": "maths-graphs",
    "type": "concept",
    "q": "The slope of a force-versus-extension graph has units",
    "opts": [
      "J/s",
      "N m",
      "N/m",
      "m/N"
    ],
    "ans": 2,
    "sol": "<p>Slope divides the vertical force by the horizontal extension, giving N/m. It is the spring constant for a Hookean spring; multiplying gives work units instead.</p>"
  },
  {
    "id": "c11-maths-calculus",
    "src": "c11",
    "qno": "maths · 5",
    "topic": "maths-calculus",
    "type": "numerical",
    "q": "If x = 4t² + 7 in SI units, acceleration is",
    "opts": [
      "7 m/s²",
      "8t m/s²",
      "4 m/s²",
      "8 m/s²"
    ],
    "ans": 3,
    "sol": "<p>One derivative gives v = 8t; a second gives a = 8 m/s². The constant offset does not affect either derivative.</p>"
  },
  {
    "id": "c11-maths-integrals",
    "src": "c11",
    "qno": "maths · 6",
    "topic": "maths-integrals",
    "type": "numerical",
    "q": "A velocity is −3 m/s for 2 s, then +3 m/s for 2 s. Displacement and distance are",
    "opts": [
      "0 m and 0 m",
      "0 m and 12 m",
      "12 m and 0 m",
      "6 m and 6 m"
    ],
    "ans": 1,
    "sol": "<p>The signed areas cancel, giving zero displacement. Their magnitudes add to 6+6=12 m, which is the distance travelled.</p>"
  },
  {
    "id": "c11-maths-logs",
    "src": "c11",
    "qno": "maths · 7",
    "topic": "maths-logs",
    "type": "numerical",
    "q": "ln(e³) equals",
    "opts": [
      "9",
      "1",
      "3",
      "e"
    ],
    "ans": 2,
    "sol": "<p>Natural logarithm is the inverse of the exponential, so it returns the exponent 3.</p>"
  },
  {
    "id": "c11-units-si",
    "src": "c11",
    "qno": "units · 1",
    "topic": "units-si",
    "type": "numerical",
    "q": "72 km/h expressed in SI is",
    "opts": [
      "10 m/s",
      "20 m/s",
      "72 m/s",
      "259.2 m/s"
    ],
    "ans": 1,
    "sol": "<p>Multiply by 5/18: 72×5/18=20 m/s. Using 18/5 would perform the reverse conversion.</p>"
  },
  {
    "id": "c11-units-dimensions",
    "src": "c11",
    "qno": "units · 2",
    "topic": "units-dimensions",
    "type": "numerical",
    "q": "The coefficient k in F = kv² has dimensions",
    "opts": [
      "ML",
      "M/T",
      "ML/T²",
      "M/L"
    ],
    "ans": 3,
    "sol": "<p>k = F/v². Dividing MLT⁻² by L²T⁻² gives ML⁻¹. The coefficient is not a spring constant because its defining equation is different.</p>"
  },
  {
    "id": "c11-units-analysis",
    "src": "c11",
    "qno": "units · 3",
    "topic": "units-analysis",
    "type": "concept",
    "q": "If a time depends only on distance ℓ and acceleration a, its dimensional form is",
    "opts": [
      "Cℓa",
      "C√(ℓ/a)",
      "C√(a/ℓ)",
      "Cℓ/a"
    ],
    "ans": 1,
    "sol": "<p>ℓ/a has dimension T²; its square root is a time. C cannot be fixed from dimensions.</p>"
  },
  {
    "id": "c11-units-significant",
    "src": "c11",
    "qno": "units · 4",
    "topic": "units-significant",
    "type": "numerical",
    "q": "How many significant figures are in 0.02040?",
    "opts": [
      "5",
      "2",
      "3",
      "4"
    ],
    "ans": 3,
    "sol": "<p>The leading zeros are placeholders. The digits 2, 0, 4 and the final decimal zero are significant, so there are four.</p>"
  },
  {
    "id": "c11-units-errors",
    "src": "c11",
    "qno": "units · 5",
    "topic": "units-errors",
    "type": "numerical",
    "q": "An instrument consistently reads 0.5 cm too high. Repeating the reading mainly fails to remove",
    "opts": [
      "Systematic error",
      "Sample count",
      "Unit conversion",
      "Random fluctuations"
    ],
    "ans": 0,
    "sol": "<p>A fixed calibration bias shifts every reading. Averaging can reduce independent random scatter, but the bias needs a correction.</p>"
  },
  {
    "id": "c11-units-propagation",
    "src": "c11",
    "qno": "units · 6",
    "topic": "units-propagation",
    "type": "numerical",
    "q": "If the radius uncertainty is 3%, the approximate area uncertainty is",
    "opts": [
      "1.5%",
      "3%",
      "6%",
      "9%"
    ],
    "ans": 2,
    "sol": "<p>Area varies as r², so the first-order fractional error doubles to 6%. Squaring 3% is not the propagation rule.</p>"
  },
  {
    "id": "c11-units-instruments",
    "src": "c11",
    "qno": "units · 7",
    "topic": "units-instruments",
    "type": "numerical",
    "q": "An observed length is 5.12 cm and zero error is −0.03 cm. The corrected length is",
    "opts": [
      "5.09 cm",
      "5.12 cm",
      "5.15 cm",
      "5.03 cm"
    ],
    "ans": 2,
    "sol": "<p>Subtract the signed error: 5.12−(−0.03)=5.15 cm. The negative zero error means the instrument underreads.</p>"
  },
  {
    "id": "c11-linear-position",
    "src": "c11",
    "qno": "linear · 1",
    "topic": "linear-position",
    "type": "concept",
    "q": "A descending lift above the ground slows before stopping. With upward positive and ground as origin, the signs of x, v, a are",
    "opts": [
      "+, −, +",
      "−, −, −",
      "+, −, −",
      "+, +, +"
    ],
    "ans": 0,
    "sol": "<p>The position is above the origin, velocity is downward, and acceleration is upward because the downward motion is slowing. None of these signs is inferred from another alone.</p>"
  },
  {
    "id": "c11-linear-averages",
    "src": "c11",
    "qno": "linear · 2",
    "topic": "linear-averages",
    "type": "numerical",
    "q": "For equal times at 3 and 9 m/s in the same direction, average speed is",
    "opts": [
      "3 m/s",
      "9 m/s",
      "4.5 m/s",
      "6 m/s"
    ],
    "ans": 3,
    "sol": "<p>Each speed acts for the same time, so the average is (3+9)/2=6 m/s. The harmonic mean would apply to equal distances.</p>"
  },
  {
    "id": "c11-linear-acceleration",
    "src": "c11",
    "qno": "linear · 3",
    "topic": "linear-acceleration",
    "type": "numerical",
    "q": "An object has v=−5 m/s and a=−2 m/s². Its speed is",
    "opts": [
      "Constant",
      "Necessarily zero",
      "Increasing",
      "Decreasing"
    ],
    "ans": 2,
    "sol": "<p>Both signs are negative, so va is positive. The velocity becomes more negative and its magnitude increases.</p>"
  },
  {
    "id": "c11-linear-equations",
    "src": "c11",
    "qno": "linear · 4",
    "topic": "linear-equations",
    "type": "concept",
    "q": "Doubling the initial speed with the same constant braking magnitude changes stopping distance by a factor",
    "opts": [
      "2",
      "4",
      "8",
      "1"
    ],
    "ans": 1,
    "sol": "<p>Stopping distance is u²/(2|a|), so doubling u quadruples it. Stopping time only doubles.</p>"
  },
  {
    "id": "c11-linear-graphs",
    "src": "c11",
    "qno": "linear · 5",
    "topic": "linear-graphs",
    "type": "concept",
    "q": "A horizontal line above zero on a velocity–time graph represents",
    "opts": [
      "Constant positive velocity",
      "Increasing acceleration",
      "Increasing speed",
      "Rest"
    ],
    "ans": 0,
    "sol": "<p>Its height is a positive velocity and its slope is zero acceleration. Rest would require the line to lie on the time axis.</p>"
  },
  {
    "id": "c11-linear-gravity",
    "src": "c11",
    "qno": "linear · 6",
    "topic": "linear-gravity",
    "type": "concept",
    "q": "Ignoring drag, the acceleration of a vertically thrown ball at its highest point is",
    "opts": [
      "g downward",
      "Dependent on its mass",
      "Zero",
      "g upward"
    ],
    "ans": 0,
    "sol": "<p>Gravity does not switch off when velocity vanishes. The mass cancels from F=ma for the gravitational force mg.</p>"
  },
  {
    "id": "c11-linear-relative",
    "src": "c11",
    "qno": "linear · 7",
    "topic": "linear-relative",
    "type": "numerical",
    "q": "Two vehicles move in the same direction at 18 and 12 m/s. Their relative speed is",
    "opts": [
      "30 m/s",
      "6 m/s",
      "18 m/s",
      "12 m/s"
    ],
    "ans": 1,
    "sol": "<p>Subtract same-direction velocities: 18−12=6 m/s. Adding is appropriate for opposing directions.</p>"
  },
  {
    "id": "c11-vectors-components",
    "src": "c11",
    "qno": "vectors · 1",
    "topic": "vectors-components",
    "type": "numerical",
    "q": "A vector has components −3 and +4 m. Its magnitude is",
    "opts": [
      "5 m",
      "7 m",
      "−5 m",
      "1 m"
    ],
    "ans": 0,
    "sol": "<p>The magnitude is √(9+16)=5 m. Negative x places the direction in quadrant II; it does not make the magnitude negative.</p>"
  },
  {
    "id": "c11-vectors-addition",
    "src": "c11",
    "qno": "vectors · 2",
    "topic": "vectors-addition",
    "type": "numerical",
    "q": "Two 5 N vectors at 120° have a resultant magnitude",
    "opts": [
      "5√3 N",
      "0 N",
      "5 N",
      "10 N"
    ],
    "ans": 2,
    "sol": "<p>R²=25+25+50 cos120°=25, hence R=5 N. Adding the magnitudes would assume parallel forces.</p>"
  },
  {
    "id": "c11-vectors-dot",
    "src": "c11",
    "qno": "vectors · 3",
    "topic": "vectors-dot",
    "type": "concept",
    "q": "The dot product of nonzero perpendicular vectors is",
    "opts": [
      "0",
      "A+B",
      "AB",
      "−AB"
    ],
    "ans": 0,
    "sol": "<p>cos90°=0. AB and −AB instead correspond to parallel and antiparallel directions.</p>"
  },
  {
    "id": "c11-vectors-cross",
    "src": "c11",
    "qno": "vectors · 4",
    "topic": "vectors-cross",
    "type": "concept",
    "q": "If A×B points along +z, B×A points",
    "opts": [
      "Along −z",
      "Along +x",
      "Nowhere because it vanishes",
      "Along +z"
    ],
    "ans": 0,
    "sol": "<p>The cross product is antisymmetric. Changing the order changes the sign, not the magnitude.</p>"
  },
  {
    "id": "c11-vectors-equilibrium",
    "src": "c11",
    "qno": "vectors · 5",
    "topic": "vectors-equilibrium",
    "type": "numerical",
    "q": "For forces 4î N and −3ĵ N, a balancing force is",
    "opts": [
      "3î−4ĵ N",
      "4î−3ĵ N",
      "−4î+3ĵ N",
      "−4î−3ĵ N"
    ],
    "ans": 2,
    "sol": "<p>Negate both components of the resultant. Balancing one component while leaving the other nonzero would still accelerate the object.</p>"
  },
  {
    "id": "c11-plane-kinematics",
    "src": "c11",
    "qno": "plane · 1",
    "topic": "plane-kinematics",
    "type": "numerical",
    "q": "For v = 6î+8ĵ m/s, speed is",
    "opts": [
      "10 m/s",
      "14 m/s",
      "48 m/s",
      "2 m/s"
    ],
    "ans": 0,
    "sol": "<p>Speed is the magnitude √(6²+8²)=10 m/s, not the sum of perpendicular components.</p>"
  },
  {
    "id": "c11-plane-projectiles",
    "src": "c11",
    "qno": "plane · 2",
    "topic": "plane-projectiles",
    "type": "concept",
    "q": "At a projectile’s highest point, its acceleration is",
    "opts": [
      "Horizontal",
      "Vertically downward",
      "Along its velocity",
      "Zero"
    ],
    "ans": 1,
    "sol": "<p>Gravity remains downward throughout the flight. Velocity is horizontal at the top, so acceleration and velocity are perpendicular there.</p>"
  },
  {
    "id": "c11-plane-horizontal",
    "src": "c11",
    "qno": "plane · 3",
    "topic": "plane-horizontal",
    "type": "concept",
    "q": "Two balls are released from the same height, one dropped and one launched horizontally. Neglecting drag, they reach the ground",
    "opts": [
      "According to their masses",
      "At the same time",
      "Dropped ball first",
      "Launched ball first"
    ],
    "ans": 1,
    "sol": "<p>Both have zero initial vertical velocity and the same vertical acceleration. Their horizontal velocities affect only horizontal travel.</p>"
  },
  {
    "id": "c11-plane-relative",
    "src": "c11",
    "qno": "plane · 4",
    "topic": "plane-relative",
    "type": "concept",
    "q": "For the same swimmer and river, the shortest crossing time is",
    "opts": [
      "10 s",
      "13.3 s",
      "20 s",
      "8 s"
    ],
    "ans": 3,
    "sol": "<p>Point entirely across to use the full 5 m/s across the 40 m width. Time is 8 s; current creates drift but does not change that crossing time.</p>"
  },
  {
    "id": "c11-plane-circular",
    "src": "c11",
    "qno": "plane · 5",
    "topic": "plane-circular",
    "type": "concept",
    "q": "If speed doubles on the same circle, centripetal acceleration becomes",
    "opts": [
      "Four times",
      "Unchanged",
      "Half",
      "Twice"
    ],
    "ans": 0,
    "sol": "<p>a_c scales with v² at fixed radius. Doubling speed therefore gives a factor of four.</p>"
  },
  {
    "id": "c11-plane-nonuniform",
    "src": "c11",
    "qno": "plane · 6",
    "topic": "plane-nonuniform",
    "type": "concept",
    "q": "For constant nonzero speed on a circle, tangential acceleration is",
    "opts": [
      "Zero",
      "v²/r",
      "v/r",
      "Equal to radial acceleration"
    ],
    "ans": 0,
    "sol": "<p>No speed change means dv/dt=0. The radial component remains nonzero because the direction still changes.</p>"
  },
  {
    "id": "c11-laws-newton",
    "src": "c11",
    "qno": "laws · 1",
    "topic": "laws-newton",
    "type": "concept",
    "q": "The reaction to Earth’s gravitational pull on a book is",
    "opts": [
      "Air pushing the book",
      "The table pushing the book",
      "The book pulling Earth",
      "The book pushing the table"
    ],
    "ans": 2,
    "sol": "<p>The gravitational pair acts between Earth and book. The normal force from the table belongs to a different contact interaction.</p>"
  },
  {
    "id": "c11-laws-fbd",
    "src": "c11",
    "qno": "laws · 2",
    "topic": "laws-fbd",
    "type": "numerical",
    "q": "A downward applied force of 8 N acts on a stationary 2 kg block on a horizontal table, with g=10. Normal force is",
    "opts": [
      "12 N",
      "20 N",
      "28 N",
      "8 N"
    ],
    "ans": 2,
    "sol": "<p>The table supports both the 20 N weight and the additional 8 N push. Vertical equilibrium gives N=28 N.</p>"
  },
  {
    "id": "c11-laws-connected",
    "src": "c11",
    "qno": "laws · 3",
    "topic": "laws-connected",
    "type": "concept",
    "q": "Two masses in an ideal fixed-pulley Atwood machine have",
    "opts": [
      "Identical weights",
      "Equal velocities as vectors",
      "Equal acceleration magnitudes",
      "Zero tension"
    ],
    "ans": 2,
    "sol": "<p>The fixed total string length makes the magnitudes of their accelerations equal, but their vertical directions are opposite.</p>"
  },
  {
    "id": "c11-laws-lift",
    "src": "c11",
    "qno": "laws · 4",
    "topic": "laws-lift",
    "type": "concept",
    "q": "In an ideal freely falling lift, apparent weight is",
    "opts": [
      "mg/2",
      "mg",
      "2mg",
      "Zero"
    ],
    "ans": 3,
    "sol": "<p>Lift and person both accelerate downward at g, so no normal force is needed. Gravitational force still acts; only the scale reading vanishes.</p>"
  },
  {
    "id": "c11-laws-impulse",
    "src": "c11",
    "qno": "laws · 5",
    "topic": "laws-impulse",
    "type": "concept",
    "q": "In a collision with negligible external impulse, which is always conserved?",
    "opts": [
      "Individual momentum",
      "Individual speeds",
      "Total momentum",
      "Total kinetic energy"
    ],
    "ans": 2,
    "sol": "<p>Total momentum follows from zero external impulse. Internal forces change individual momenta, and inelastic collisions change total kinetic energy.</p>"
  },
  {
    "id": "c11-laws-circular",
    "src": "c11",
    "qno": "laws · 6",
    "topic": "laws-circular",
    "type": "concept",
    "q": "For a frictionless banked road, centripetal force is supplied by",
    "opts": [
      "The horizontal normal-force component",
      "Gravity alone horizontally",
      "A tangential push",
      "A separate new force"
    ],
    "ans": 0,
    "sol": "<p>The normal force is tilted by the bank angle. Its inward horizontal component turns the vehicle while its vertical component balances weight.</p>"
  },
  {
    "id": "c11-friction-static",
    "src": "c11",
    "qno": "friction · 1",
    "topic": "friction-static",
    "type": "numerical",
    "q": "If the applied force is 5 N and maximum static friction is 15 N, actual friction at equilibrium is",
    "opts": [
      "20 N",
      "0 N",
      "5 N",
      "15 N"
    ],
    "ans": 2,
    "sol": "<p>Static friction adjusts to the required 5 N. It reaches 15 N only at the threshold of slipping.</p>"
  },
  {
    "id": "c11-friction-kinetic",
    "src": "c11",
    "qno": "friction · 2",
    "topic": "friction-kinetic",
    "type": "concept",
    "q": "On a horizontal surface with no extra vertical force, sliding deceleration magnitude is",
    "opts": [
      "g/μₖ",
      "μₖ/m",
      "μₖmg",
      "μₖg"
    ],
    "ans": 3,
    "sol": "<p>Friction μₖmg divided by mass gives μₖg. The mass cancels; μₖmg is the force, not the acceleration.</p>"
  },
  {
    "id": "c11-friction-inclines",
    "src": "c11",
    "qno": "friction · 3",
    "topic": "friction-inclines",
    "type": "numerical",
    "q": "A block slides downhill on a 30° plane with μₖ=1/√3. Its acceleration is",
    "opts": [
      "g/2",
      "g",
      "Zero",
      "g√3/2"
    ],
    "ans": 2,
    "sol": "<p>g(sin30°−μₖcos30°)=g(1/2−1/2)=0. It can continue downhill at constant speed; zero acceleration does not mean no motion.</p>"
  },
  {
    "id": "c11-friction-pulling",
    "src": "c11",
    "qno": "friction · 4",
    "topic": "friction-pulling",
    "type": "concept",
    "q": "An upward-angled pull generally changes normal force by",
    "opts": [
      "Leaving it at mg",
      "Making it always zero",
      "Increasing it",
      "Decreasing it"
    ],
    "ans": 3,
    "sol": "<p>The upward component carries part of the load. Normal force falls by that component until contact is lost.</p>"
  },
  {
    "id": "c11-friction-systems",
    "src": "c11",
    "qno": "friction · 5",
    "topic": "friction-systems",
    "type": "numerical",
    "q": "For μₛ=0.25, r=40 m and g=10, maximum speed on a level circular road is",
    "opts": [
      "100 m/s",
      "5 m/s",
      "10 m/s",
      "20 m/s"
    ],
    "ans": 2,
    "sol": "<p>v_max=√(0.25×40×10)=10 m/s. The quantity inside the root has units m²/s², so 100 is not a speed.</p>"
  },
  {
    "id": "c11-work-work",
    "src": "c11",
    "qno": "work · 1",
    "topic": "work-work",
    "type": "numerical",
    "q": "A force increases linearly from 0 to 12 N over 3 m. Its work is",
    "opts": [
      "72 J",
      "4 J",
      "18 J",
      "36 J"
    ],
    "ans": 2,
    "sol": "<p>The F–x area is a triangle: ½×3×12=18 J. Multiplying final force by distance would incorrectly treat the force as constant.</p>"
  },
  {
    "id": "c11-work-theorem",
    "src": "c11",
    "qno": "work · 2",
    "topic": "work-theorem",
    "type": "concept",
    "q": "If a body’s speed triples, its kinetic energy becomes",
    "opts": [
      "3 times",
      "6 times",
      "9 times",
      "Unchanged"
    ],
    "ans": 2,
    "sol": "<p>K scales as v² at fixed mass. Tripling speed gives nine times the energy.</p>"
  },
  {
    "id": "c11-work-potential",
    "src": "c11",
    "qno": "work · 3",
    "topic": "work-potential",
    "type": "numerical",
    "q": "If U(x)=3x² in SI units, force at x=2 m is",
    "opts": [
      "+12 N",
      "−12 N",
      "+6 N",
      "−6 N"
    ],
    "ans": 1,
    "sol": "<p>Fₓ=−dU/dx=−6x, so at 2 m it is −12 N. The force points toward the lower potential near x=0.</p>"
  },
  {
    "id": "c11-work-conservation",
    "src": "c11",
    "qno": "work · 4",
    "topic": "work-conservation",
    "type": "concept",
    "q": "A freely falling body in vacuum has constant",
    "opts": [
      "Vertical momentum",
      "Kinetic energy",
      "Potential energy",
      "Total mechanical energy"
    ],
    "ans": 3,
    "sol": "<p>Gravity decreases potential and increases kinetic energy by equal amounts. Momentum changes under the external gravitational force.</p>"
  },
  {
    "id": "c11-work-power",
    "src": "c11",
    "qno": "work · 5",
    "topic": "work-power",
    "type": "numerical",
    "q": "A parallel force of 50 N moves its application point at 4 m/s. Power is",
    "opts": [
      "46 W",
      "200 W",
      "800 W",
      "12.5 W"
    ],
    "ans": 1,
    "sol": "<p>Instantaneous power is Fv=50×4=200 W. Dividing force by speed has the wrong dimensions.</p>"
  },
  {
    "id": "c11-work-collisions",
    "src": "c11",
    "qno": "work · 6",
    "topic": "work-collisions",
    "type": "concept",
    "q": "Two identical masses collide elastically head-on, one initially at rest. After collision they",
    "opts": [
      "Both keep their original velocities",
      "Stick together",
      "Exchange velocities",
      "Both stop"
    ],
    "ans": 2,
    "sol": "<p>Momentum and kinetic-energy conservation give the moving mass’s speed to the initially stationary mass. Sticking would be inelastic.</p>"
  },
  {
    "id": "c11-work-vertical-loop",
    "src": "c11",
    "qno": "work · 7",
    "topic": "work-vertical-loop",
    "type": "concept",
    "q": "At the top in the limiting complete string circle, tension is",
    "opts": [
      "2mg",
      "Zero",
      "5mg",
      "mg"
    ],
    "ans": 1,
    "sol": "<p>At the threshold, mg=mv²/r and no extra inward tension is needed. Below that speed the string would slacken.</p>"
  },
  {
    "id": "c11-work-elastic-results",
    "src": "c11",
    "qno": "work · 8",
    "topic": "work-elastic-results",
    "type": "concept",
    "q": "A very light ball reflects elastically from a stationary effectively immovable wall. Its final velocity is approximately",
    "opts": [
      "u",
      "−u",
      "0",
      "u/2"
    ],
    "ans": 1,
    "sol": "<p>The wall-mass limit gives velocity reversal with the same speed. Its momentum changes even though its kinetic energy does not.</p>"
  },
  {
    "id": "c11-rotation-centre",
    "src": "c11",
    "qno": "rotation · 1",
    "topic": "rotation-centre",
    "type": "numerical",
    "q": "Two equal masses are at x=−4 and +2 m. Their centre is",
    "opts": [
      "−2 m",
      "+3 m",
      "−1 m",
      "+1 m"
    ],
    "ans": 2,
    "sol": "<p>For equal masses the centre is the average coordinate: (−4+2)/2=−1 m. Averaging distances from the origin would lose the signs.</p>"
  },
  {
    "id": "c11-rotation-angular",
    "src": "c11",
    "qno": "rotation · 2",
    "topic": "rotation-angular",
    "type": "concept",
    "q": "For a rigid rotating disc, the point at twice the radius has",
    "opts": [
      "The same linear speed",
      "Twice the angular speed",
      "Half the linear speed",
      "Twice the linear speed"
    ],
    "ans": 3,
    "sol": "<p>v=rω and all points share ω, so doubling radius doubles linear speed.</p>"
  },
  {
    "id": "c11-rotation-torque",
    "src": "c11",
    "qno": "rotation · 3",
    "topic": "rotation-torque",
    "type": "numerical",
    "q": "Equal opposite forces separated by 0.4 m, each 10 N, form a couple with torque",
    "opts": [
      "2 N m",
      "4 N m",
      "8 N m",
      "0 N m"
    ],
    "ans": 1,
    "sol": "<p>Couple torque is one force magnitude times the perpendicular separation: 10×0.4=4 N m. The forces cancel translationally but their turning effects add.</p>"
  },
  {
    "id": "c11-rotation-inertia",
    "src": "c11",
    "qno": "rotation · 4",
    "topic": "rotation-inertia",
    "type": "concept",
    "q": "For equal mass and radius, a thin ring’s central-axis inertia is how many times a disc’s?",
    "opts": [
      "Equal",
      "Twice",
      "Four times",
      "Half"
    ],
    "ans": 1,
    "sol": "<p>The ring has MR² and the disc has MR²/2, so the ratio is 2.</p>"
  },
  {
    "id": "c11-rotation-axis",
    "src": "c11",
    "qno": "rotation · 5",
    "topic": "rotation-axis",
    "type": "numerical",
    "q": "A body has I_CM=2 kg m², M=3 kg and a parallel axis 2 m away. Its inertia is",
    "opts": [
      "14 kg m²",
      "20 kg m²",
      "5 kg m²",
      "8 kg m²"
    ],
    "ans": 0,
    "sol": "<p>Add Md²=3×4=12 to 2, giving 14 kg m². The distance must be squared.</p>"
  },
  {
    "id": "c11-rotation-dynamics",
    "src": "c11",
    "qno": "rotation · 6",
    "topic": "rotation-dynamics",
    "type": "numerical",
    "q": "A rotor with I=2 kg m² spins at 3 rad/s. Its rotational kinetic energy is",
    "opts": [
      "6 J",
      "9 J",
      "18 J",
      "3 J"
    ],
    "ans": 1,
    "sol": "<p>K=½Iω²=½×2×9=9 J. Multiplying I by ω gives angular momentum instead.</p>"
  },
  {
    "id": "c11-rotation-momentum",
    "src": "c11",
    "qno": "rotation · 7",
    "topic": "rotation-momentum",
    "type": "concept",
    "q": "With angular momentum fixed, halving I makes rotational kinetic energy",
    "opts": [
      "Four times",
      "Half",
      "Unchanged",
      "Twice"
    ],
    "ans": 3,
    "sol": "<p>K=L²/(2I), so halving I doubles K. The increased energy must come from work by the mechanism changing the mass distribution.</p>"
  },
  {
    "id": "c11-rotation-rolling",
    "src": "c11",
    "qno": "rotation · 8",
    "topic": "rotation-rolling",
    "type": "concept",
    "q": "A disc rolling at centre speed v has total kinetic energy",
    "opts": [
      "Mv²/2",
      "3Mv²/4",
      "Mv²",
      "3Mv²/2"
    ],
    "ans": 1,
    "sol": "<p>Translation gives Mv²/2. With I=MR²/2 and ω=v/R, rotation gives Mv²/4. Sum is 3Mv²/4.</p>"
  },
  {
    "id": "c11-gravitation-field",
    "src": "c11",
    "qno": "gravitation · 1",
    "topic": "gravitation-field",
    "type": "concept",
    "q": "Two equal masses lie equally far on opposite sides of a midpoint. The field there is",
    "opts": [
      "Twice one field",
      "Half one field",
      "Infinite",
      "Zero"
    ],
    "ans": 3,
    "sol": "<p>Equal field magnitudes point in opposite directions at the midpoint. Their vector sum is zero even though the gravitational potential there is negative.</p>"
  },
  {
    "id": "c11-gravitation-variation",
    "src": "c11",
    "qno": "gravitation · 2",
    "topic": "gravitation-variation",
    "type": "numerical",
    "q": "Inside a uniform sphere at depth R/2, gravity is",
    "opts": [
      "2g₀",
      "4g₀",
      "g₀/4",
      "g₀/2"
    ],
    "ans": 3,
    "sol": "<p>Use the uniform-sphere depth relation: g_d=g₀(1−1/2)=g₀/2. The enclosed source mass has decreased.</p>"
  },
  {
    "id": "c11-gravitation-potential",
    "src": "c11",
    "qno": "gravitation · 3",
    "topic": "gravitation-potential",
    "type": "concept",
    "q": "Inside a uniform thin spherical shell, gravitational field and potential are",
    "opts": [
      "Zero field and constant negative potential",
      "Nonzero field and zero potential",
      "Both varying with radius",
      "Both zero"
    ],
    "ans": 0,
    "sol": "<p>Opposite shell contributions cancel in the field. Their negative scalar potentials add to the constant −GM/R inside.</p>"
  },
  {
    "id": "c11-gravitation-orbits",
    "src": "c11",
    "qno": "gravitation · 4",
    "topic": "gravitation-orbits",
    "type": "concept",
    "q": "For a circular gravitational orbit, total energy E relative to kinetic energy K is",
    "opts": [
      "E=K",
      "E=−K",
      "E=−2K",
      "E=0"
    ],
    "ans": 1,
    "sol": "<p>Potential energy is −2K, so E=K−2K=−K. Zero total energy instead describes the escape threshold.</p>"
  },
  {
    "id": "c11-gravitation-escape",
    "src": "c11",
    "qno": "gravitation · 5",
    "topic": "gravitation-escape",
    "type": "concept",
    "q": "At the same radius, escape speed divided by circular orbital speed is",
    "opts": [
      "√2",
      "2",
      "1/√2",
      "1"
    ],
    "ans": 0,
    "sol": "<p>The escape expression has 2GM/r under the root while circular speed has GM/r, giving √2.</p>"
  },
  {
    "id": "c11-gravitation-kepler",
    "src": "c11",
    "qno": "gravitation · 6",
    "topic": "gravitation-kepler",
    "type": "concept",
    "q": "In an elliptical orbit, a satellite’s speed is greatest",
    "opts": [
      "Farthest from the source",
      "Nearest the source",
      "At every point equally",
      "Only when its acceleration vanishes"
    ],
    "ans": 1,
    "sol": "<p>Conserved swept-area rate and angular momentum require higher speed near the source. Gravity remains nonzero throughout the orbit.</p>"
  },
  {
    "id": "c11-gravitation-spherical",
    "src": "c11",
    "qno": "gravitation · 7",
    "topic": "gravitation-spherical",
    "type": "concept",
    "q": "Rotation alone makes apparent surface gravity smallest at the",
    "opts": [
      "North pole",
      "South pole",
      "Equator",
      "Same at all latitudes"
    ],
    "ans": 2,
    "sol": "<p>Equatorial points require the greatest centripetal acceleration for Earth’s rotation, leaving a smaller normal force per mass.</p>"
  },
  {
    "id": "c11-oscillations-periodic",
    "src": "c11",
    "qno": "oscillations · 1",
    "topic": "oscillations-periodic",
    "type": "concept",
    "q": "Which acceleration law represents stable SHM?",
    "opts": [
      "a=+4x",
      "a=−4x",
      "a=−4x²",
      "a=−4"
    ],
    "ans": 1,
    "sol": "<p>a=−4x has ω²=4 with the required proportionality and restoring sign. Positive proportional acceleration drives the body away.</p>"
  },
  {
    "id": "c11-oscillations-phase",
    "src": "c11",
    "qno": "oscillations · 2",
    "topic": "oscillations-phase",
    "type": "concept",
    "q": "Two oscillations with the same frequency differing in phase by π are",
    "opts": [
      "A quarter cycle apart",
      "Of different period",
      "In phase",
      "In opposite phase"
    ],
    "ans": 3,
    "sol": "<p>π is half a full 2π cycle. Their displacements have opposite signs at corresponding times if amplitudes and equilibrium references match.</p>"
  },
  {
    "id": "c11-oscillations-velocity",
    "src": "c11",
    "qno": "oscillations · 3",
    "topic": "oscillations-velocity",
    "type": "concept",
    "q": "At equilibrium in ideal SHM, speed and acceleration are",
    "opts": [
      "Both zero",
      "Maximum speed and zero acceleration",
      "Zero speed and maximum acceleration",
      "Both maximum"
    ],
    "ans": 1,
    "sol": "<p>At x=0 the restoring acceleration vanishes, while all mechanical energy is kinetic and speed is maximal.</p>"
  },
  {
    "id": "c11-oscillations-energy",
    "src": "c11",
    "qno": "oscillations · 4",
    "topic": "oscillations-energy",
    "type": "concept",
    "q": "If an SHM amplitude doubles at fixed k, total energy becomes",
    "opts": [
      "Unchanged",
      "Twice",
      "Four times",
      "Half"
    ],
    "ans": 2,
    "sol": "<p>E depends on A². Doubling amplitude quadruples energy while leaving the ideal linear-spring period unchanged.</p>"
  },
  {
    "id": "c11-oscillations-springs",
    "src": "c11",
    "qno": "oscillations · 5",
    "topic": "oscillations-springs",
    "type": "concept",
    "q": "For the same spring, quadrupling the attached mass changes period by",
    "opts": [
      "A factor of 1/2",
      "No change",
      "A factor of 2",
      "A factor of 4"
    ],
    "ans": 2,
    "sol": "<p>T∝√m at fixed k, so four times the mass gives twice the period.</p>"
  },
  {
    "id": "c11-oscillations-pendulum",
    "src": "c11",
    "qno": "oscillations · 6",
    "topic": "oscillations-pendulum",
    "type": "concept",
    "q": "An upward-accelerating lift makes a small-angle pendulum’s period",
    "opts": [
      "Independent of length",
      "Longer",
      "Shorter",
      "Unchanged"
    ],
    "ans": 2,
    "sol": "<p>Effective gravity is g+a, increasing the restoring acceleration. Since T∝1/√g_eff, the period decreases.</p>"
  },
  {
    "id": "c11-oscillations-resonance",
    "src": "c11",
    "qno": "oscillations · 7",
    "topic": "oscillations-resonance",
    "type": "concept",
    "q": "Compared with weak damping, strong damping usually makes a resonance peak",
    "opts": [
      "Independent of driving frequency",
      "Higher and narrower",
      "Lower and broader",
      "Infinitely high"
    ],
    "ans": 2,
    "sol": "<p>More damping dissipates energy more rapidly, reducing peak amplitude and spreading the response over a wider frequency range.</p>"
  },
  {
    "id": "c11-oscillations-superposition",
    "src": "c11",
    "qno": "oscillations · 8",
    "topic": "oscillations-superposition",
    "type": "concept",
    "q": "For ideal U-tube oscillations with fixed liquid length, doubling density changes period by",
    "opts": [
      "A factor of √2",
      "No change",
      "A factor of 1/2",
      "A factor of 2"
    ],
    "ans": 1,
    "sol": "<p>Both restoring force and moving mass scale with density; it cancels, leaving T=2π√(L/2g).</p>"
  },
  {
    "id": "c11-waves-travelling",
    "src": "c11",
    "qno": "waves · 1",
    "topic": "waves-travelling",
    "type": "concept",
    "q": "A wave y=A sin(kx+ωt) with k, ω positive travels",
    "opts": [
      "In neither direction",
      "Toward +x",
      "Toward −x",
      "Only vertically"
    ],
    "ans": 2,
    "sol": "<p>Keeping kx+ωt constant requires x to decrease as t increases. The oscillation direction is not the propagation direction.</p>"
  },
  {
    "id": "c11-waves-speed",
    "src": "c11",
    "qno": "waves · 2",
    "topic": "waves-speed",
    "type": "numerical",
    "q": "For the same ideal gas, increasing temperature from 300 to 1200 K changes sound speed by",
    "opts": [
      "A factor of 4",
      "A factor of 2",
      "A factor of 1/2",
      "No change"
    ],
    "ans": 1,
    "sol": "<p>Sound speed is proportional to √T. The absolute temperature quadruples, so speed doubles.</p>"
  },
  {
    "id": "c11-waves-superposition",
    "src": "c11",
    "qno": "waves · 3",
    "topic": "waves-superposition",
    "type": "concept",
    "q": "Two equal-amplitude coherent waves with phase difference π produce resultant amplitude",
    "opts": [
      "√2A",
      "0",
      "A",
      "2A"
    ],
    "ans": 1,
    "sol": "<p>cosπ=−1, so A_R²=A²+A²−2A²=0 at that point. This is destructive interference.</p>"
  },
  {
    "id": "c11-waves-standing",
    "src": "c11",
    "qno": "waves · 4",
    "topic": "waves-standing",
    "type": "concept",
    "q": "At a standing-wave displacement node, the particle has",
    "opts": [
      "A moving node position",
      "Maximum displacement",
      "Zero displacement at all times",
      "Maximum amplitude"
    ],
    "ans": 2,
    "sol": "<p>The spatial sine factor vanishes at a node, making displacement zero throughout the cycle.</p>"
  },
  {
    "id": "c11-waves-modes",
    "src": "c11",
    "qno": "waves · 5",
    "topic": "waves-modes",
    "type": "numerical",
    "q": "An ideal closed pipe with fundamental 200 Hz has first overtone",
    "opts": [
      "800 Hz",
      "300 Hz",
      "400 Hz",
      "600 Hz"
    ],
    "ans": 3,
    "sol": "<p>Only odd harmonics occur, so the first overtone is 3×200=600 Hz.</p>"
  },
  {
    "id": "c11-waves-beats",
    "src": "c11",
    "qno": "waves · 6",
    "topic": "waves-beats",
    "type": "numerical",
    "q": "Sources at 300 and 306 Hz produce",
    "opts": [
      "303 beats/s",
      "606 beats/s",
      "3 beats/s",
      "6 beats/s"
    ],
    "ans": 3,
    "sol": "<p>The beat rate is the absolute difference 6 Hz, not the average or the sum.</p>"
  },
  {
    "id": "c11-waves-doppler",
    "src": "c11",
    "qno": "waves · 7",
    "topic": "waves-doppler",
    "type": "concept",
    "q": "A source receding from a stationary observer gives observed frequency",
    "opts": [
      "Lower than emitted",
      "Always equal",
      "Zero for every speed",
      "Higher than emitted"
    ],
    "ans": 0,
    "sol": "<p>Recession increases wavelength: f′=fv/(v+v_s), which is less than f for positive recession speed.</p>"
  },
  {
    "id": "c11-thermal-properties-temperature",
    "src": "c11",
    "qno": "thermal-properties · 1",
    "topic": "thermal-properties-temperature",
    "type": "numerical",
    "q": "A 25°C temperature increase equals",
    "opts": [
      "298.15 K",
      "−25 K",
      "25 K",
      "248.15 K"
    ],
    "ans": 2,
    "sol": "<p>Kelvin and Celsius intervals have the same size. The offset is used only when converting an actual temperature value.</p>"
  },
  {
    "id": "c11-thermal-properties-expansion",
    "src": "c11",
    "qno": "thermal-properties · 2",
    "topic": "thermal-properties-expansion",
    "type": "concept",
    "q": "When a uniformly heated metal plate has a circular hole, the hole diameter generally",
    "opts": [
      "Increases",
      "Stays exactly fixed",
      "Becomes zero",
      "Decreases"
    ],
    "ans": 0,
    "sol": "<p>All distances in a freely expanding isotropic plate grow, including the hole diameter. A hypothetical plug of the same material would also expand.</p>"
  },
  {
    "id": "c11-thermal-properties-liquids",
    "src": "c11",
    "qno": "thermal-properties · 3",
    "topic": "thermal-properties-liquids",
    "type": "numerical",
    "q": "Pure water warmed from 0°C to 4°C approximately",
    "opts": [
      "Boils",
      "Expands and becomes less dense",
      "Contracts and becomes denser",
      "Keeps fixed density"
    ],
    "ans": 2,
    "sol": "<p>This interval exhibits anomalous contraction. Maximum density is near 4°C, after which ordinary expansion dominates.</p>"
  },
  {
    "id": "c11-thermal-properties-calorimetry",
    "src": "c11",
    "qno": "thermal-properties · 4",
    "topic": "thermal-properties-calorimetry",
    "type": "numerical",
    "q": "Two samples of the same material have masses m and 2m. Their heat capacities are in ratio",
    "opts": [
      "1:4",
      "1:1",
      "1:2",
      "2:1"
    ],
    "ans": 2,
    "sol": "<p>C=mc, so doubling mass doubles sample heat capacity. Their specific heats remain equal.</p>"
  },
  {
    "id": "c11-thermal-properties-latent",
    "src": "c11",
    "qno": "thermal-properties · 5",
    "topic": "thermal-properties-latent",
    "type": "concept",
    "q": "During melting at a fixed transition pressure, supplied heat mainly increases",
    "opts": [
      "Temperature",
      "Phase-conversion energy",
      "Mass",
      "Cooling rate"
    ],
    "ans": 1,
    "sol": "<p>Temperature remains at the melting point while the phase conversion proceeds. Energy changes internal arrangement rather than immediately raising temperature.</p>"
  },
  {
    "id": "c11-thermal-properties-conduction",
    "src": "c11",
    "qno": "thermal-properties · 6",
    "topic": "thermal-properties-conduction",
    "type": "concept",
    "q": "Two identical slabs placed in series have thermal resistance",
    "opts": [
      "Twice one slab",
      "Four times one slab",
      "Half one slab",
      "Equal to one slab"
    ],
    "ans": 0,
    "sol": "<p>The same heat rate crosses both and the temperature drops add, so the combined resistance is 2R.</p>"
  },
  {
    "id": "c11-thermal-properties-convection",
    "src": "c11",
    "qno": "thermal-properties · 7",
    "topic": "thermal-properties-convection",
    "type": "concept",
    "q": "Heat can cross empty space by",
    "opts": [
      "Conduction alone",
      "Convection alone",
      "Thermal radiation",
      "Bulk fluid motion"
    ],
    "ans": 2,
    "sol": "<p>Radiation needs no material medium. Conduction and convection require matter.</p>"
  },
  {
    "id": "c11-thermal-properties-cooling",
    "src": "c11",
    "qno": "thermal-properties · 8",
    "topic": "thermal-properties-cooling",
    "type": "concept",
    "q": "Under Newton cooling, as a body approaches room temperature its cooling rate magnitude",
    "opts": [
      "Changes sign every second",
      "Increases",
      "Decreases",
      "Stays nonzero and constant"
    ],
    "ans": 2,
    "sol": "<p>The rate is proportional to the temperature excess, which shrinks toward zero.</p>"
  },
  {
    "id": "c11-kinetic-theory-gas-law",
    "src": "c11",
    "qno": "kinetic-theory · 1",
    "topic": "kinetic-theory-gas-law",
    "type": "concept",
    "q": "Boyle’s law pV=constant requires constant",
    "opts": [
      "Temperature and gas amount",
      "Pressure only",
      "Volume only",
      "Temperature in Celsius numerically"
    ],
    "ans": 0,
    "sol": "<p>For a fixed gas amount, pV=nRT stays fixed at constant absolute temperature. It is an isothermal relation.</p>"
  },
  {
    "id": "c11-kinetic-theory-pressure",
    "src": "c11",
    "qno": "kinetic-theory · 2",
    "topic": "kinetic-theory-pressure",
    "type": "concept",
    "q": "A sealed equilibrium gas container moving at constant velocity has pressure determined by",
    "opts": [
      "Random molecular motion relative to the walls",
      "The sum of all molecular velocities",
      "The sign of its height",
      "Its ground-frame speed alone"
    ],
    "ans": 0,
    "sol": "<p>A uniform translation adds the same velocity to walls and molecules. Relative collision speeds, temperature and pressure are unchanged.</p>"
  },
  {
    "id": "c11-kinetic-theory-speeds",
    "src": "c11",
    "qno": "kinetic-theory · 3",
    "topic": "kinetic-theory-speeds",
    "type": "concept",
    "q": "For an ideal equilibrium gas, the characteristic speed ordering is",
    "opts": [
      "v_mp > v_rms > mean",
      "v_rms > mean > v_mp",
      "All equal",
      "Mean > v_rms > v_mp"
    ],
    "ans": 1,
    "sol": "<p>The squared-speed weighting raises rms above the ordinary mean. The most probable speed is √(2RT/M), the smallest of the three.</p>"
  },
  {
    "id": "c11-kinetic-theory-equipartition",
    "src": "c11",
    "qno": "kinetic-theory · 4",
    "topic": "kinetic-theory-equipartition",
    "type": "concept",
    "q": "A diatomic ideal gas with rotations active and vibrations inactive has γ",
    "opts": [
      "5/3",
      "2",
      "1",
      "7/5"
    ],
    "ans": 3,
    "sol": "<p>f=5, so γ=(f+2)/f=7/5. The monatomic value 5/3 uses only three degrees of freedom.</p>"
  },
  {
    "id": "c11-kinetic-theory-mixtures",
    "src": "c11",
    "qno": "kinetic-theory · 5",
    "topic": "kinetic-theory-mixtures",
    "type": "concept",
    "q": "If molecular dissociation doubles total particle count at unchanged T and V, pressure",
    "opts": [
      "Doubles",
      "Stays fixed",
      "Quadruples",
      "Halves"
    ],
    "ans": 0,
    "sol": "<p>pV=Nk_BT, so doubling N at fixed T and V doubles p. Conserved mass does not mean conserved molecule count.</p>"
  },
  {
    "id": "c11-kinetic-theory-mean-free-path",
    "src": "c11",
    "qno": "kinetic-theory · 6",
    "topic": "kinetic-theory-mean-free-path",
    "type": "concept",
    "q": "If effective molecular diameter doubles at fixed number density, mean free path becomes",
    "opts": [
      "Twice",
      "Four times",
      "Half",
      "One quarter"
    ],
    "ans": 3,
    "sol": "<p>The denominator contains d²; doubling d quadruples the collision cross section and reduces the path to one quarter.</p>"
  },
  {
    "id": "c11-thermodynamics-first-law",
    "src": "c11",
    "qno": "thermodynamics · 1",
    "topic": "thermodynamics-first-law",
    "type": "numerical",
    "q": "A gas is compressed adiabatically with 100 J of work done on it. Its ΔU is",
    "opts": [
      "0",
      "+100 J",
      "+200 J",
      "−100 J"
    ],
    "ans": 1,
    "sol": "<p>Q=0 and work by gas W=−100 J. Thus ΔU=0−(−100)=+100 J.</p>"
  },
  {
    "id": "c11-thermodynamics-work",
    "src": "c11",
    "qno": "thermodynamics · 2",
    "topic": "thermodynamics-work",
    "type": "concept",
    "q": "A gas held at fixed volume does boundary expansion work",
    "opts": [
      "Equal to pV",
      "Equal to Q",
      "Equal to ΔU",
      "Zero"
    ],
    "ans": 3,
    "sol": "<p>dV=0 throughout, so ∫p_ext dV=0. Heat can still change internal energy and pressure.</p>"
  },
  {
    "id": "c11-thermodynamics-isochoric-isobaric",
    "src": "c11",
    "qno": "thermodynamics · 3",
    "topic": "thermodynamics-isochoric-isobaric",
    "type": "concept",
    "q": "For the same ideal-gas temperature rise, heat required at fixed pressure is",
    "opts": [
      "Less than at fixed volume",
      "More than at fixed volume",
      "Always zero",
      "Always the same"
    ],
    "ans": 1,
    "sol": "<p>C_P=C_V+R, so fixed-pressure heating requires additional heat to supply expansion work.</p>"
  },
  {
    "id": "c11-thermodynamics-isothermal",
    "src": "c11",
    "qno": "thermodynamics · 4",
    "topic": "thermodynamics-isothermal",
    "type": "concept",
    "q": "An insulated ideal gas expands freely into vacuum. Work by the gas is",
    "opts": [
      "nRT ln(V_f/V_i)",
      "Zero",
      "p_iV_i",
      "Always negative"
    ],
    "ans": 1,
    "sol": "<p>The external resisting pressure is zero, so boundary work vanishes. The reversible logarithmic formula describes a different path.</p>"
  },
  {
    "id": "c11-thermodynamics-adiabatic",
    "src": "c11",
    "qno": "thermodynamics · 5",
    "topic": "thermodynamics-adiabatic",
    "type": "concept",
    "q": "In a reversible adiabatic ideal-gas expansion, temperature",
    "opts": [
      "Must remain fixed",
      "Becomes zero immediately",
      "Increases",
      "Decreases"
    ],
    "ans": 3,
    "sol": "<p>Q=0 and W>0 imply ΔU<0. Since ideal-gas U depends on T, temperature falls.</p>"
  },
  {
    "id": "c11-thermodynamics-cycles",
    "src": "c11",
    "qno": "thermodynamics · 6",
    "topic": "thermodynamics-cycles",
    "type": "concept",
    "q": "A gas completing a cycle has net internal-energy change",
    "opts": [
      "Equal to heat rejected",
      "Equal to net heat",
      "Equal to work",
      "Zero"
    ],
    "ans": 3,
    "sol": "<p>Internal energy is a state function. Returning to the same state makes its change zero, even though heat and work around the cycle can be nonzero.</p>"
  },
  {
    "id": "c11-thermodynamics-second-law",
    "src": "c11",
    "qno": "thermodynamics · 7",
    "topic": "thermodynamics-second-law",
    "type": "numerical",
    "q": "A Carnot engine between 500 and 300 K has maximum efficiency",
    "opts": [
      "40%",
      "60%",
      "80%",
      "20%"
    ],
    "ans": 0,
    "sol": "<p>η=1−300/500=0.4. Using Celsius instead of absolute reservoir temperatures would give an incorrect ratio.</p>"
  },
  {
    "id": "c11-maths-ratios-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "maths-ratios",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "A quantity scales as Q ∝ x²/√y. If x increases by 20% and y becomes four times its original value, the new Q/Q₀ is",
    "opts": [
      "0.60",
      "0.72",
      "1.20",
      "2.88"
    ],
    "ans": 1,
    "sol": "<p>x becomes 1.2x₀, giving a squared factor 1.44. The denominator grows by √4=2. Thus Q/Q₀=1.44/2=0.72, a 28% decrease. Percentage changes cannot be added directly.</p>"
  },
  {
    "id": "c11-maths-integrals-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "maths-integrals",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "A force follows F=2x N, with x in metres. What is the area under the force–position curve between x=1 and x=3 m?",
    "opts": [
      "4 J",
      "6 J",
      "8 J",
      "12 J"
    ],
    "ans": 2,
    "sol": "<p>Integrate 2x from 1 to 3: x² evaluated at the limits gives 9−1=8 J. The initial lower limit is not zero; using only the final value gives too much work.</p>"
  },
  {
    "id": "c11-units-propagation-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "units-propagation",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "For T=2π√(ℓ/g), worst-case uncertainties in ℓ and g are 2% and 4%. The first-order uncertainty in T is",
    "opts": [
      "1%",
      "2%",
      "3%",
      "6%"
    ],
    "ans": 2,
    "sol": "<p>The powers are +1/2 and −1/2. Sum their absolute-weight contributions: ½×2%+½×4%=3%. The minus sign in the exponent does not subtract uncertainties.</p>"
  },
  {
    "id": "c11-units-significant-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "units-significant",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "A measured mass of 5.43 g is divided by a measured volume of 2.1 cm³. The appropriately reported density is",
    "opts": [
      "2.5857 g/cm³",
      "2.586 g/cm³",
      "2.59 g/cm³",
      "2.6 g/cm³"
    ],
    "ans": 3,
    "sol": "<p>The unrounded ratio is 2.5857… g/cm³. Volume has two significant figures, so the final product/quotient should have two: 2.6 g/cm³.</p>"
  },
  {
    "id": "c11-linear-equations-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "linear-equations",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "A particle starts at x=0 with velocity +12 m/s and constant acceleration −4 m/s². In the first 5 s, distance and displacement are",
    "opts": [
      "10 m, 10 m",
      "26 m, 10 m",
      "18 m, 26 m",
      "26 m, −10 m"
    ],
    "ans": 1,
    "sol": "<p>Velocity vanishes at 3 s. Position there is 18 m. At 5 s position is 12×5−2×25=10 m. The return distance is 8 m, so total distance is 18+8=26 m, while displacement is +10 m.</p>"
  },
  {
    "id": "c11-linear-relative-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "linear-relative",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "A walker takes 30 s to climb a stationary escalator. The escalator alone takes 60 s to carry a standing person. At the same walking rate on the moving escalator, climb time is",
    "opts": [
      "15 s",
      "20 s",
      "30 s",
      "45 s"
    ],
    "ans": 1,
    "sol": "<p>For escalator length L, walking speed is L/30 and escalator speed L/60. They add to L/20, so the climb takes 20 s. Times themselves do not add.</p>"
  },
  {
    "id": "c11-vectors-addition-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "vectors-addition",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "Vectors of magnitudes 3 and 4 units have resultant magnitude 5 units. Their included angle is",
    "opts": [
      "0°",
      "60°",
      "90°",
      "180°"
    ],
    "ans": 2,
    "sol": "<p>Use 25=9+16+24 cosθ. Thus cosθ=0 and θ=90°. The 3–4–5 values reflect perpendicular components, not parallel addition.</p>"
  },
  {
    "id": "c11-vectors-dot-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "vectors-dot",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "The projection of \\(\\vec A=6\\hat i+8\\hat j\\) m along the direction of \\(\\vec B=\\hat i\\) is",
    "opts": [
      "6 m",
      "8 m",
      "10 m",
      "14 m"
    ],
    "ans": 0,
    "sol": "<p>The signed projection is A·B/|B|. Here it is 6 m. The 10 m magnitude contains both components and is not the projection onto +x.</p>"
  },
  {
    "id": "c11-plane-relative-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "plane-relative",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "A swimmer moves at 4 m/s relative to water across a 60 m river flowing at 3 m/s. For the shortest crossing time, the downstream drift is",
    "opts": [
      "0 m",
      "15 m",
      "45 m",
      "60 m"
    ],
    "ans": 2,
    "sol": "<p>Shortest time uses the entire swimming speed across: 60/4=15 s. The current carries the swimmer 3×15=45 m downstream. A directly opposite crossing needs an upstream component and takes longer.</p>"
  },
  {
    "id": "c11-plane-horizontal-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "plane-horizontal",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "A particle launches horizontally at 15 m/s from height 20 m, with g=10 m/s² and no drag. Impact speed is",
    "opts": [
      "15 m/s",
      "20 m/s",
      "25 m/s",
      "35 m/s"
    ],
    "ans": 2,
    "sol": "<p>Fall time is 2 s, so vertical impact speed is 20 m/s. Horizontal speed remains 15 m/s. Combining perpendicular components gives √(225+400)=25 m/s.</p>"
  },
  {
    "id": "c11-laws-connected-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "laws-connected",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "A 2 kg block on a smooth horizontal table is tied over an ideal fixed pulley to a hanging 3 kg mass. Use g=10. The acceleration and tension are",
    "opts": [
      "6 m/s², 12 N",
      "10 m/s², 20 N",
      "6 m/s², 30 N",
      "2 m/s², 24 N"
    ],
    "ans": 0,
    "sol": "<p>The only driving force for the combined system is the hanging weight 30 N, so a=30/(2+3)=6 m/s². For the table block T=2a=12 N. This is not the two-hanging-mass Atwood formula.</p>"
  },
  {
    "id": "c11-laws-impulse-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "laws-impulse",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "A 0.1 kg ball approaches a bat at 20 m/s and returns at 30 m/s. Contact lasts 0.005 s. Average force magnitude on the ball is",
    "opts": [
      "200 N",
      "400 N",
      "600 N",
      "1000 N"
    ],
    "ans": 3,
    "sol": "<p>Use signed velocities +20 and −30 m/s. Momentum change is 0.1(−30−20)=−5 N s. Dividing its magnitude by 0.005 s gives 1000 N; subtracting speed magnitudes would miss reversal.</p>"
  },
  {
    "id": "c11-friction-pulling-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "friction-pulling",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "A 5 kg block on a horizontal floor is pulled by 25 N at an angle with cosθ=0.8 and sinθ=0.6. With μₖ=0.2 and g=10, its acceleration while sliding in the pull direction is",
    "opts": [
      "1.4 m/s²",
      "2.6 m/s²",
      "4.0 m/s²",
      "5.0 m/s²"
    ],
    "ans": 1,
    "sol": "<p>Vertical pull is 15 N, so N=50−15=35 N. Sliding friction is 7 N. Horizontal pull is 20 N; net force is 13 N, giving a=13/5=2.6 m/s².</p>"
  },
  {
    "id": "c11-friction-static-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "friction-static",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "A stationary 2 kg block has μₛ=0.4 and μₖ=0.3 on a level floor. With g=10, a 7 N horizontal pull acts. Its acceleration is",
    "opts": [
      "0",
      "0.5 m/s²",
      "3.5 m/s²",
      "4 m/s²"
    ],
    "ans": 0,
    "sol": "<p>The static limit is 0.4×20=8 N. The 7 N pull can be balanced by 7 N static friction, so acceleration is zero. Kinetic friction is inappropriate because sliding has not begun.</p>"
  },
  {
    "id": "c11-work-collisions-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "work-collisions",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "A 2 kg mass moving at 6 m/s catches and sticks to a 1 kg mass moving at 3 m/s in the same direction. Kinetic energy lost is",
    "opts": [
      "0 J",
      "3 J",
      "9 J",
      "12 J"
    ],
    "ans": 1,
    "sol": "<p>Momentum is 2×6+1×3=15 kg m/s, so common speed is 5 m/s. Initial K=36+4.5=40.5 J; final K=½×3×25=37.5 J. Loss is 3 J. Both initial momenta have the same sign.</p>"
  },
  {
    "id": "c11-work-theorem-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "work-theorem",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "A 1 kg particle starts from rest under force F=4x N along a straight path. At x=2 m, its speed is",
    "opts": [
      "2 m/s",
      "4 m/s",
      "8 m/s",
      "16 m/s"
    ],
    "ans": 1,
    "sol": "<p>Work from 0 to 2 m is ∫4x dx=2x² evaluated at 2, or 8 J. By work–energy, ½v²=8 and v=4 m/s. Using the final force as constant overestimates work.</p>"
  },
  {
    "id": "c11-rotation-rolling-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "rotation-rolling",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "A uniform disc rolls without slipping from rest through a vertical drop of 3 m. Use g=10 and neglect dissipation. Its centre speed at the bottom is",
    "opts": [
      "√20 m/s",
      "√40 m/s",
      "√60 m/s",
      "√90 m/s"
    ],
    "ans": 1,
    "sol": "<p>For a disc, K=3Mv²/4. Set Mgh=3Mv²/4, giving v²=4gh/3=40. Rotational energy makes centre speed lower than a purely sliding particle’s √60 m/s.</p>"
  },
  {
    "id": "c11-rotation-momentum-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "rotation-momentum",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "With zero external torque, a rotor’s inertia decreases from 6 to 2 kg m². Initially ω=2 rad/s. Final angular speed and final kinetic energy are",
    "opts": [
      "2 rad/s, 4 J",
      "6 rad/s, 12 J",
      "6 rad/s, 36 J",
      "4 rad/s, 16 J"
    ],
    "ans": 2,
    "sol": "<p>Initial angular momentum is 12 kg m²/s. Final ω=12/2=6 rad/s and K=½×2×36=36 J. Initial K was 12 J; the rearrangement supplies the 24 J increase.</p>"
  },
  {
    "id": "c11-gravitation-orbits-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "gravitation-orbits",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "Two circular satellites orbit the same planet at radii r and 4r. The outer satellite’s period divided by the inner’s is",
    "opts": [
      "2",
      "4",
      "8",
      "16"
    ],
    "ans": 2,
    "sol": "<p>Circular period scales as r³/². Thus (4r/r)³/²=8. Speed decreases with radius while orbit circumference increases, so period grows faster than linearly.</p>"
  },
  {
    "id": "c11-gravitation-escape-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "gravitation-escape",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "At a planet’s surface, circular orbital speed is 8 km/s. Ignoring atmosphere and rotation, escape speed is",
    "opts": [
      "4√2 km/s",
      "8 km/s",
      "8√2 km/s",
      "16 km/s"
    ],
    "ans": 2,
    "sol": "<p>At the same radius, escape speed is √2 times circular speed. Thus it is 8√2 km/s, approximately 11.3 km/s; escape is not merely maintaining a bound orbit.</p>"
  },
  {
    "id": "c11-oscillations-velocity-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "oscillations-velocity",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "In SHM with amplitude A and angular frequency ω, speed at x=A/2 divided by maximum speed is",
    "opts": [
      "1/2",
      "1/√2",
      "√3/2",
      "1"
    ],
    "ans": 2,
    "sol": "<p>Speed is ω√(A²−x²). At x=A/2 this is ωA√3/2; divide by maximum speed ωA to get √3/2. Half displacement does not imply half speed.</p>"
  },
  {
    "id": "c11-oscillations-springs-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "oscillations-springs",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "Two identical springs k each support the same mass first in series and then in parallel. Period in series divided by period in parallel is",
    "opts": [
      "1/2",
      "1",
      "√2",
      "2"
    ],
    "ans": 3,
    "sol": "<p>Effective constants are k/2 and 2k. Since T∝1/√k_eff, the ratio is √[(2k)/(k/2)]=2. The two arrangements differ in stiffness by four.</p>"
  },
  {
    "id": "c11-waves-modes-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "waves-modes",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "At sound speed 340 m/s, a closed pipe and an open pipe have the same fundamental frequency 170 Hz. Their effective lengths (closed, open) are",
    "opts": [
      "0.5 m, 1 m",
      "1 m, 0.5 m",
      "1 m, 1 m",
      "0.25 m, 0.5 m"
    ],
    "ans": 0,
    "sol": "<p>Closed-pipe fundamental is v/(4L), giving L=340/(4×170)=0.5 m. Open-pipe fundamental is v/(2L), giving 1 m. Boundary conditions change the allowed fundamental wavelength.</p>"
  },
  {
    "id": "c11-waves-doppler-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "waves-doppler",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "A stationary 600 Hz source is heard by an observer approaching at 30 m/s. Sound speed is 330 m/s. Observed frequency is",
    "opts": [
      "550 Hz",
      "600 Hz",
      "650 Hz",
      "600×12/11 Hz"
    ],
    "ans": 3,
    "sol": "<p>For a moving observer and stationary source, f′=f(v+v_o)/v=600×360/330=600×12/11≈654.5 Hz. A moving-source denominator would describe a different problem.</p>"
  },
  {
    "id": "c11-thermal-properties-calorimetry-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "thermal-properties-calorimetry",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "Equal masses of materials with specific heats c and 3c start at 80°C and 20°C respectively. In an insulated negligible-capacity container, final temperature is",
    "opts": [
      "35°C",
      "50°C",
      "65°C",
      "70°C"
    ],
    "ans": 0,
    "sol": "<p>Heat balance gives c(80−T)=3c(T−20), so 80−T=3T−60 and T=35°C. The colder sample has three times the heat capacity, so the final temperature lies closer to 20°C.</p>"
  },
  {
    "id": "c11-thermal-properties-latent-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "thermal-properties-latent",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "An insulated mixture has 0.1 kg ice at 0°C and 0.1 kg water at 50°C. Use water c=4200 J/kg K and ice fusion latent heat 336000 J/kg. What happens?",
    "opts": [
      "All ice melts and final temperature is positive",
      "All ice melts exactly at 0°C",
      "Some ice remains at 0°C",
      "All water freezes"
    ],
    "ans": 2,
    "sol": "<p>Cooling water to 0°C supplies 0.1×4200×50=21000 J. Melting all ice needs 33600 J. Only 21000/336000=0.0625 kg melts, leaving 0.0375 kg ice at 0°C.</p>"
  },
  {
    "id": "c11-kinetic-theory-speeds-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "kinetic-theory-speeds",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "At equal temperature, compare rms molecular speeds of hydrogen (2 g/mol) and oxygen (32 g/mol). The ratio v_H₂/v_O₂ is",
    "opts": [
      "2",
      "4",
      "8",
      "16"
    ],
    "ans": 1,
    "sol": "<p>v_rms∝1/√M at fixed T, so ratio is √(32/2)=4. The molar masses can be used as a ratio in the same units; the lighter molecules are faster.</p>"
  },
  {
    "id": "c11-kinetic-theory-equipartition-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "kinetic-theory-equipartition",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "At ordinary temperatures with rotations active and vibrations inactive, 2 mol of a diatomic ideal gas at 300 K has internal energy",
    "opts": [
      "900R J",
      "1200R J",
      "1500R J",
      "2100R J"
    ],
    "ans": 2,
    "sol": "<p>With f=5, U=(5/2)nRT=(5/2)×2×R×300=1500R J. Using 3RT/2 per mole counts translational energy only and misses active rotations.</p>"
  },
  {
    "id": "c11-thermodynamics-cycles-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "thermodynamics-cycles",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "A cyclic engine absorbs 1200 J and rejects 900 J each cycle. Running at 4 cycles per second, useful power is",
    "opts": [
      "300 W",
      "900 W",
      "1200 W",
      "4800 W"
    ],
    "ans": 2,
    "sol": "<p>Net work per cycle is 1200−900=300 J. Four cycles per second give 1200 J/s=1200 W. Efficiency is 25%; heat input rate is not useful output power.</p>"
  },
  {
    "id": "c11-thermodynamics-second-law-challenge",
    "src": "c11",
    "qno": "Challenge",
    "topic": "thermodynamics-second-law",
    "type": "numerical",
    "difficulty": "challenge",
    "q": "A reversible refrigerator operates between 270 K and 300 K and receives 100 J of work per cycle. Maximum heat removed from the cold side is",
    "opts": [
      "100 J",
      "300 J",
      "900 J",
      "1000 J"
    ],
    "ans": 2,
    "sol": "<p>Carnot refrigerator COP=270/(300−270)=9. Therefore Q_c=COP×W=900 J. It rejects Q_h=Q_c+W=1000 J to the hot side; that is not the removed cold-side heat.</p>"
  },
  {
    "id": "ex-02-01",
    "src": "ex",
    "qno": "2.1",
    "topic": "units-significant",
    "type": "numerical",
    "q": "How many significant figures are reported in 0.008700?",
    "opts": [
      "2",
      "3",
      "4",
      "6"
    ],
    "ans": 2,
    "sol": "<p>The leading zeros locate the decimal point. The digits 8, 7, 0 and 0 are significant, giving four. Trailing decimal zeros record precision; they are not discarded.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep302.pdf",
      "question": "2.1",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-02-06",
    "src": "ex",
    "qno": "2.6",
    "topic": "units-dimensions",
    "type": "concept",
    "q": "Which pair has different dimensions?",
    "opts": [
      "Energy and torque",
      "Impulse and momentum",
      "Force and surface tension",
      "Angular momentum and action"
    ],
    "ans": 2,
    "sol": "<p>Force has dimensions MLT⁻², while surface tension is force per length with dimensions MT⁻². The other three pairs match dimensionally, although they describe distinct quantities.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep302.pdf",
      "question": "2.6",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-03-04",
    "src": "ex",
    "qno": "3.4",
    "topic": "linear-averages",
    "type": "numerical",
    "q": "A runner covers equal distances at 6 and 12 m/s. What is the average speed?",
    "opts": [
      "8 m/s",
      "9 m/s",
      "10 m/s",
      "18 m/s"
    ],
    "ans": 0,
    "sol": "<p>For each leg distance d, total time is d/6+d/12=d/4. Total distance is 2d, so average speed is 8 m/s. The arithmetic mean assumes equal times.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep303.pdf",
      "question": "3.4",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-03-05",
    "src": "ex",
    "qno": "3.5",
    "topic": "linear-position",
    "type": "numerical",
    "q": "Position is x=(t−3)² m with t in seconds. Over t=0 to 6 s, what distance is travelled?",
    "opts": [
      "0 m",
      "9 m",
      "18 m",
      "36 m"
    ],
    "ans": 2,
    "sol": "<p>Position starts at 9 m, decreases to 0 at t=3 s, then returns to 9 m. Distance is 9+9=18 m; displacement is zero. The turning time comes from v=2(t−3).</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep303.pdf",
      "question": "3.5",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-04-01",
    "src": "ex",
    "qno": "4.1",
    "topic": "vectors-dot",
    "type": "numerical",
    "q": "The vectors \\(\\vec A=2\\hat i+2\\hat j\\) and \\(\\vec B=3\\hat i-3\\hat j\\) make what angle?",
    "opts": [
      "0°",
      "45°",
      "90°",
      "180°"
    ],
    "ans": 2,
    "sol": "<p>Their dot product is 2×3+2×(−3)=0. Both vectors are nonzero, so they are perpendicular. Opposite signs in one component do not mean the whole vectors are antiparallel.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep304.pdf",
      "question": "4.1",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-04-05",
    "src": "ex",
    "qno": "4.5",
    "topic": "plane-projectiles",
    "type": "numerical",
    "q": "On level ground a projectile has range 40 m at 15°. At the same speed, what is its range at 45°?",
    "opts": [
      "40 m",
      "40√2 m",
      "80 m",
      "160 m"
    ],
    "ans": 2,
    "sol": "<p>Range scales with sin(2θ). The first sine is sin30°=1/2 and the second is sin90°=1, giving twice the range, 80 m. Equal launch and landing heights are essential.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep304.pdf",
      "question": "4.5",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-05-07",
    "src": "ex",
    "qno": "5.7",
    "topic": "laws-newton",
    "type": "numerical",
    "q": "A 2 kg particle has x=2t+3t²+4t³ in SI units. What net force acts at t=1 s?",
    "opts": [
      "12 N",
      "24 N",
      "30 N",
      "60 N"
    ],
    "ans": 3,
    "sol": "<p>Differentiate twice: a=6+24t. At 1 s a=30 m/s² and F=ma=60 N. A single derivative would give velocity, not acceleration.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep305.pdf",
      "question": "5.7",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-05-11",
    "src": "ex",
    "qno": "5.11",
    "topic": "friction-systems",
    "type": "numerical",
    "q": "A 1 kg block sits on a 2 kg block on a smooth floor. Their static coefficient is 0.2. With g=10, what is the largest horizontal force on the lower block for motion together?",
    "opts": [
      "2 N",
      "4 N",
      "6 N",
      "10 N"
    ],
    "ans": 2,
    "sol": "<p>The top block can be accelerated at most at μₛg=2 m/s². The combined mass is 3 kg, so maximum external force is 3×2=6 N. Internal friction cancels only for the combined-system equation.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep305.pdf",
      "question": "5.11",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-06-07",
    "src": "ex",
    "qno": "6.7",
    "topic": "work-conservation",
    "type": "concept",
    "q": "Two particles start from rest on smooth straight inclines of equal vertical height. One incline is steeper. What happens at the bottom?",
    "opts": [
      "Same speed; steeper path arrives earlier",
      "Same speed and same arrival time",
      "Steeper path has lower speed",
      "Shallower path arrives earlier"
    ],
    "ans": 0,
    "sol": "<p>Energy gives v=√(2gh) for either path. For a straight incline, a=g sinθ and length=h/sinθ, so time=√(2h/g)/sinθ. The steeper incline arrives earlier.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep306.pdf",
      "question": "6.7",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-06-16",
    "src": "ex",
    "qno": "6.16",
    "topic": "work-conservation",
    "type": "numerical",
    "q": "A 2 kg ball is thrown at 3 m/s from 4 m above ground. Ignoring drag with g=10, what is its impact kinetic energy?",
    "opts": [
      "9 J",
      "40 J",
      "80 J",
      "89 J"
    ],
    "ans": 3,
    "sol": "<p>Initial kinetic energy is ½×2×3²=9 J. Falling adds mgh=80 J, so final K=89 J. Launch direction changes the trajectory, not this energy balance.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep306.pdf",
      "question": "6.16",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-07-01",
    "src": "ex",
    "qno": "7.1",
    "topic": "rotation-centre",
    "type": "concept",
    "q": "Which uniform object has its centre of mass in an empty region?",
    "opts": [
      "Solid ball",
      "Thin circular ring",
      "Solid cube",
      "Straight solid rod"
    ],
    "ans": 1,
    "sol": "<p>The ring’s symmetry places its centre of mass at the circle centre, where there is no ring material. The centre of mass need not be inside the matter.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep307.pdf",
      "question": "7.1",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-07-04",
    "src": "ex",
    "qno": "7.4",
    "topic": "rotation-angular",
    "type": "concept",
    "q": "A rigid disc rotates about a fixed axis with constant nonzero angular velocity. Which quantity is zero?",
    "opts": [
      "Angular acceleration",
      "Angular speed",
      "Rim speed",
      "Radial acceleration of a rim point"
    ],
    "ans": 0,
    "sol": "<p>Constant angular velocity gives α=0. Rim speed stays nonzero and its direction changes, requiring radial acceleration ω²r.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep307.pdf",
      "question": "7.4",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-08-06",
    "src": "ex",
    "qno": "8.6",
    "topic": "gravitation-kepler",
    "type": "concept",
    "q": "A small asteroid is gravitationally bound to a dominant star. In the ideal two-body approximation, its small mass means",
    "opts": [
      "It cannot orbit",
      "It obeys Kepler’s laws like a planet",
      "Its gravity must be repulsive",
      "Its orbital period is zero"
    ],
    "ans": 1,
    "sol": "<p>Gravitational acceleration GM/r² does not depend on the asteroid’s mass. Bound inverse-square two-body trajectories and periods obey Kepler’s laws; small mass is not a barrier to orbiting.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep308.pdf",
      "question": "8.6",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-08-08",
    "src": "ex",
    "qno": "8.8",
    "topic": "gravitation-field",
    "type": "numerical",
    "q": "Fixed masses 2M and M are separated by 3d. A test mass lies distance d from 2M and 2d from M. Its initial gravitational acceleration points",
    "opts": [
      "Toward 2M",
      "Toward M",
      "Nowhere; fields cancel",
      "Perpendicular to the line"
    ],
    "ans": 0,
    "sol": "<p>The competing field magnitudes are 2GM/d² and GM/(4d²). The first is eight times the second, so the net field points toward 2M. Here source masses are explicitly fixed.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep308.pdf",
      "question": "8.8",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-09-01",
    "src": "ex",
    "qno": "9.1",
    "topic": "shear",
    "type": "concept",
    "q": "An ideal fluid in static equilibrium can sustain what shear stress without flowing?",
    "opts": [
      "Any shear stress",
      "A fixed positive shear stress",
      "No shear stress",
      "Only infinite shear stress"
    ],
    "ans": 2,
    "sol": "<p>An ideal static fluid has zero shear modulus and cannot sustain tangential stress. Pressure can still be nonzero because it is normal stress, not shear.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep309.pdf",
      "question": "9.1",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-09-02",
    "src": "ex",
    "qno": "9.2",
    "topic": "applications",
    "type": "concept",
    "q": "A uniform wire is cut to half its length while retaining its cross-section. Its ideal breaking load is",
    "opts": [
      "Halved",
      "Unchanged",
      "Doubled",
      "Quadrupled"
    ],
    "ans": 1,
    "sol": "<p>Breaking load equals breaking stress times cross-sectional area. The material and area remain the same, so the load threshold is unchanged. Elastic extension, unlike breaking load, depends on length.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep309.pdf",
      "question": "9.2",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-10-04",
    "src": "ex",
    "qno": "10.4",
    "topic": "continuity",
    "type": "numerical",
    "q": "An incompressible fluid flows steadily through pipe diameters 2 cm and 4 cm. The speed in the narrow section divided by the wide-section speed is",
    "opts": [
      "1/4",
      "1/2",
      "2",
      "4"
    ],
    "ans": 3,
    "sol": "<p>Av is constant and circular area scales as diameter squared. Thus v_narrow/v_wide=(4/2)²=4. Doubling diameter quadruples area.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep310.pdf",
      "question": "10.4",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-10-05",
    "src": "ex",
    "qno": "10.5",
    "topic": "contact-angle",
    "type": "numerical",
    "q": "A capillary liquid surface is convex and its contact angle exceeds 90°. The liquid tends to",
    "opts": [
      "Rise above the reservoir",
      "Be depressed below the reservoir",
      "Have zero surface tension",
      "Have zero density"
    ],
    "ans": 1,
    "sol": "<p>For θ>90°, cosθ<0 in h=2S cosθ/(ρgr), so h is negative: capillary depression. A convex nonwetting meniscus is consistent with this result.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep310.pdf",
      "question": "10.5",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-11-01",
    "src": "ex",
    "qno": "11.1",
    "topic": "thermal-properties-expansion",
    "type": "concept",
    "q": "Bonded metal strips A and B are heated, with A having the larger expansion coefficient. In the resulting bend, A lies on the",
    "opts": [
      "Shorter inner side",
      "Longer outer side",
      "Neutral axis only",
      "Same curve length as B"
    ],
    "ans": 1,
    "sol": "<p>The more-expanding layer wants a greater length and forms the outer convex side. The smaller-expanding layer is on the concave side; bonding forces the pair to bend.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep311.pdf",
      "question": "11.1",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-11-04",
    "src": "ex",
    "qno": "11.4",
    "topic": "thermal-properties-liquids",
    "type": "numerical",
    "q": "A fixed-volume fully submerged object displaces pure water at 0°C and at 4°C. Buoyant force is larger at",
    "opts": [
      "0°C",
      "4°C",
      "Both equally",
      "Neither because buoyancy vanishes"
    ],
    "ans": 1,
    "sol": "<p>Buoyancy is ρ_water g V. Pure water is denser near 4°C, so buoyancy is larger there for the stated unchanged displaced volume. This comparison isolates water’s density effect.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep311.pdf",
      "question": "11.4",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-12-05",
    "src": "ex",
    "qno": "12.5",
    "topic": "thermodynamics-adiabatic",
    "type": "numerical",
    "q": "Identical ideal gases start at the same state. Each is reversibly compressed to half its volume: A isothermal, B adiabatic with γ=1.4. Final p_B/p_A is",
    "opts": [
      "1",
      "2⁰·⁴",
      "2¹·⁴",
      "2"
    ],
    "ans": 1,
    "sol": "<p>For A, p_A=2p₀. For B, p_B=2^γ p₀. Their ratio is 2^(γ−1)=2^0.4, about 1.32. The adiabatic gas also warms; the isothermal gas rejects heat.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep312.pdf",
      "question": "12.5",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-12-08",
    "src": "ex",
    "qno": "12.8",
    "topic": "thermodynamics-isothermal",
    "type": "concept",
    "q": "For a reversible ideal-gas isothermal expansion, which relation is correct?",
    "opts": [
      "Q=0 and W>0",
      "ΔU=0 and Q=W",
      "ΔU=Q and W=0",
      "Temperature increases"
    ],
    "ans": 1,
    "sol": "<p>For an ideal gas U depends only on temperature, so ΔU=0. The first law then requires supplied heat to equal the positive expansion work. Isothermal is not adiabatic.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep312.pdf",
      "question": "12.8",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-13-03",
    "src": "ex",
    "qno": "13.3",
    "topic": "kinetic-theory-gas-law",
    "type": "concept",
    "q": "A fixed amount of ideal gas obeys pV=constant during a process. That process is",
    "opts": [
      "Isothermal",
      "Isochoric heating",
      "Isobaric heating",
      "Necessarily adiabatic"
    ],
    "ans": 0,
    "sol": "<p>pV=nRT, so at fixed amount a constant product requires constant absolute temperature. An adiabatic process instead generally follows pV^γ=constant when reversible.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep313.pdf",
      "question": "13.3",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-13-06",
    "src": "ex",
    "qno": "13.6",
    "topic": "kinetic-theory-mixtures",
    "type": "numerical",
    "q": "In a fixed volume, a diatomic ideal gas completely dissociates into atoms while temperature rises from 300 to 900 K. What is final pressure divided by initial pressure?",
    "opts": [
      "2",
      "3",
      "6",
      "9"
    ],
    "ans": 2,
    "sol": "<p>Each molecule becomes two particles, doubling N. Absolute temperature triples. Since p∝NT at fixed volume, pressure becomes 2×3=6 times the initial value.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep313.pdf",
      "question": "13.6",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-14-06",
    "src": "ex",
    "qno": "14.6",
    "topic": "oscillations-superposition",
    "type": "numerical",
    "q": "For \\(x=6\\sin\\omega t+8\\cos\\omega t\\) cm, the amplitude is",
    "opts": [
      "2 cm",
      "7 cm",
      "10 cm",
      "14 cm"
    ],
    "ans": 2,
    "sol": "<p>Sine and cosine differ by π/2. The combined amplitude is √(6²+8²)=10 cm. Adding 6+8 would require matching phases.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep314.pdf",
      "question": "14.6",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-14-04",
    "src": "ex",
    "qno": "14.4",
    "topic": "oscillations-superposition",
    "type": "concept",
    "q": "The total liquid length in an ideal U-tube is doubled. Its small-oscillation period changes by",
    "opts": [
      "A factor of 2",
      "A factor of √2",
      "A factor of 1/2",
      "No change"
    ],
    "ans": 1,
    "sol": "<p>T=2π√(L/2g) for a uniform U-tube with negligible viscosity. Doubling total moving liquid length multiplies the period by √2.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep314.pdf",
      "question": "14.4",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-15-02",
    "src": "ex",
    "qno": "15.2",
    "topic": "waves-travelling",
    "type": "concept",
    "q": "A wave enters a stationary new medium where its propagation speed is three times greater. Its wavelength becomes",
    "opts": [
      "One third",
      "Unchanged",
      "Three times",
      "Nine times"
    ],
    "ans": 2,
    "sol": "<p>The frequency is set by the source and is unchanged across a stationary boundary. With λ=v/f, tripling speed triples wavelength.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep315.pdf",
      "question": "15.2",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  },
  {
    "id": "ex-15-04",
    "src": "ex",
    "qno": "15.4",
    "topic": "waves-speed",
    "type": "concept",
    "q": "A fixed-frequency sound source remains unchanged while the air warms and sound speed increases. The wavelength",
    "opts": [
      "Decreases",
      "Increases",
      "Must stay fixed",
      "Becomes the frequency"
    ],
    "ans": 1,
    "sol": "<p>The source frequency is fixed; λ=v/f therefore increases when speed increases. Medium temperature changes propagation speed, not the unchanged source’s frequency.</p>",
    "reference": {
      "url": "https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep315.pdf",
      "question": "15.4",
      "label": "Adapted NCERT Exemplar pattern",
      "review": "independently solved"
    }
  }
]);
