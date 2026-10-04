/* Independent answer fixtures for cross-chapter numerical relationships.
   IDs locate questions; expected answer text is independent of option ordering. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const ctx={window:{QBANK:[]}};vm.createContext(ctx);
vm.runInContext(fs.readFileSync('site/assets/q-class11.js','utf8'),ctx);
const Q=ctx.window.QBANK;
const fixture={
 'c11-maths-ratios':'4/3 of Q',
 'c11-maths-calculus':'8 m/s²',
 'c11-maths-integrals':'0 m and 12 m',
 'c11-units-si':'20 m/s',
 'c11-units-dimensions':'M/L',
 'c11-units-propagation':'6%',
 'c11-units-instruments':'5.15 cm',
 'c11-linear-averages':'6 m/s',
 'c11-linear-relative':'6 m/s',
 'c11-vectors-addition':'5 N',
 'c11-plane-kinematics':'10 m/s',
 'c11-plane-relative':'8 s',
 'c11-laws-fbd':'28 N',
 'c11-friction-static':'5 N',
 'c11-friction-systems':'10 m/s',
 'c11-work-work':'18 J',
 'c11-work-power':'200 W',
 'c11-rotation-torque':'4 N m',
 'c11-rotation-axis':'14 kg m²',
 'c11-rotation-dynamics':'9 J',
 'c11-gravitation-variation':'g₀/2',
 'c11-oscillations-energy':'Four times',
 'c11-waves-modes':'600 Hz',
 'c11-waves-beats':'6 beats/s',
 'c11-thermal-properties-temperature':'25 K',
 'c11-thermal-properties-conduction':'Twice one slab',
 'c11-kinetic-theory-equipartition':'7/5',
 'c11-thermodynamics-first-law':'+100 J',
 'c11-thermodynamics-second-law':'40%',
 'c11-maths-ratios-challenge':'0.72',
 'c11-maths-integrals-challenge':'8 J',
 'c11-units-propagation-challenge':'3%',
 'c11-units-significant-challenge':'2.6 g/cm³',
 'c11-linear-equations-challenge':'26 m, 10 m',
 'c11-linear-relative-challenge':'20 s',
 'c11-vectors-addition-challenge':'90°',
 'c11-vectors-dot-challenge':'6 m',
 'c11-plane-relative-challenge':'45 m',
 'c11-plane-horizontal-challenge':'25 m/s',
 'c11-laws-connected-challenge':'6 m/s², 12 N',
 'c11-laws-impulse-challenge':'1000 N',
 'c11-friction-pulling-challenge':'2.6 m/s²',
 'c11-friction-static-challenge':'0',
 'c11-work-collisions-challenge':'3 J',
 'c11-work-theorem-challenge':'4 m/s',
 'c11-rotation-rolling-challenge':'√40 m/s',
 'c11-rotation-momentum-challenge':'6 rad/s, 36 J',
 'c11-gravitation-orbits-challenge':'8',
 'c11-gravitation-escape-challenge':'8√2 km/s',
 'c11-oscillations-velocity-challenge':'√3/2',
 'c11-oscillations-springs-challenge':'2',
 'c11-waves-modes-challenge':'0.5 m, 1 m',
 'c11-waves-doppler-challenge':'600×12/11 Hz',
 'c11-thermal-properties-calorimetry-challenge':'35°C',
 'c11-thermal-properties-latent-challenge':'Some ice remains at 0°C',
 'c11-kinetic-theory-speeds-challenge':'4',
 'c11-kinetic-theory-equipartition-challenge':'1500R J',
 'c11-thermodynamics-cycles-challenge':'1200 W',
 'c11-thermodynamics-second-law-challenge':'900 J',
 'ex-02-01':'4', 'ex-03-04':'8 m/s', 'ex-03-05':'18 m',
 'ex-04-01':'90°', 'ex-04-05':'80 m', 'ex-05-07':'60 N',
 'ex-05-11':'6 N', 'ex-06-16':'89 J', 'ex-10-04':'4',
 'ex-12-05':'2⁰·⁴', 'ex-13-06':'6', 'ex-14-06':'10 cm',
};
for(const [id,expected] of Object.entries(fixture)){
 const q=Q.find(q=>q.id===id);assert(q,'Missing '+id);assert.equal(q.opts[q.ans],expected,id);
}
const sources=JSON.parse(fs.readFileSync('content/exemplar_sources.json','utf8'));
for(const q of Q.filter(q=>q.reference)){
 const source=sources.find(s=>s.url===q.reference.url);
 assert(source?.question_ids.includes(q.reference.question),q.id+': source question was collected');
 assert(!/NEET.*20\d\d|past.year/i.test(q.reference.label),q.id+': adaptation must not masquerade as a PYQ');
}
// Energy/momentum check independent of the taught collision example.
const m1=1,m2=2,u1=6,u2=0,v1=-2,v2=4;
assert.equal(m1*u1+m2*u2,m1*v1+m2*v2);
assert.equal(m1*u1**2+m2*u2**2,m1*v1**2+m2*v2**2);
console.log(`Passed ${Object.keys(fixture).length} numerical/concept answer fixtures, collision invariants and all 28 source identifiers.`);
