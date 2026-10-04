/* Model checks use independent physical identities and limiting cases. */
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const context={window:{},document:{addEventListener(){}},matchMedia:()=>({matches:true})};vm.createContext(context);
vm.runInContext(fs.readFileSync('site/assets/physics-labs.js','utf8'),context);
const {models,scene}=context.window.PhysicsLabs;
const near=(actual,expected,tolerance=1e-8)=>assert(Math.abs(actual-expected)<=tolerance,`${actual} differs from ${expected}`);
const defaults=m=>Object.fromEntries(m.controls.map(c=>[c.id,c.value]));
let states=0;
for(const [key,m] of Object.entries(models)){
 const base=defaults(m),cases=[base];
 for(const c of m.controls){if(c.options)for(const [v] of c.options)cases.push({...base,[c.id]:v});else for(const v of [c.min,c.max])cases.push({...base,[c.id]:v});}
 for(const x of cases){const d=m.calc(x),out=scene(key,x,d);assert(!/NaN|Infinity|undefined/.test(out.svg),key+' invalid geometry');assert(out.svg.includes('<title>'),key+' accessible scene');assert(out.stats.length,key+' readouts');states++;}
}
near(models.tangent.calc({t:2,gap:0.02}).chord,4.02);
near(models.integral.calc({n:4}).estimate,12);
near(models.vernier.calc({length:7.4}).main,7);near(models.vernier.calc({length:7.4}).n,4);
near(models.uncertainty.calc({error:2}).upper,4.04);
const kin=models.kinematics.calc({u:4,a:-2,t:3});near(kin.position,3);near(kin.velocity,-2);near(kin.turn,2);
const dist=models.distance.calc({out:7,back:7});near(dist.displacement,0);near(dist.distance,14);
near(models.components.calc({a:5,angle:120}).x,-2.5);near(models.projection.calc({angle:90}).work,0);
const shot=models.projectile.calc({u:20,angle:45,t:Math.sqrt(2)});near(shot.vy,0);near(shot.height,10);near(shot.range,40);
const river=models.river.calc({swim:5,stream:3,angle:Math.asin(3/5)*180/Math.PI,t:0});near(river.drift,0);near(river.crossing,10);
near(models.circle.calc({r:2,v:4,t:0}).acceleration,8);
const pulley=models.atwood.calc({m1:2,m2:3,t:0});near(pulley.a,2);near(pulley.tension,24);
near(models.lift.calc({a:-10}).normal,0);
near(models.friction.calc({force:5}).friction,5);near(models.friction.calc({force:13}).acceleration,2.5);
assert(!models.incline.calc({angle:20}).sliding);assert(models.incline.calc({angle:30}).sliding);
for(const t of [0,.3,1,2]){const d=models['spring-energy'].calc({t});near(d.kinetic+d.potential,2.5);}
for(const e of [0,.25,.5,1]){const d=models.collision.calc({e,t:0});near(d.v1+2*d.v2,6);near((d.v1*d.v1+2*d.v2*d.v2)/2+d.loss,18);}
const loop=models.loop.calc({speed:Math.sqrt(50),angle:180});near(loop.tension,0);near(loop.speed,Math.sqrt(10));
const turn=models.loop.calc({speed:4,angle:180});assert(turn.turning&&!turn.lost);near(turn.speed,0);assert(turn.tension>0);
near(models['centre-mass'].calc({m1:2,m2:4,x1:-3,x2:3}).centre,1);
const race=models.rolling.calc({t:1}).bodies;assert(race[2].a>race[1].a&&race[1].a>race[0].a);
const o1=models.orbit.calc({radius:2,t:0}),o2=models.orbit.calc({radius:4,t:0});near(o2.period/o1.period,2*Math.sqrt(2));
near(models['gravity-profile'].calc({r:0}).gravity,0);near(models['gravity-profile'].calc({r:2}).gravity,.25);
const shm=models.shm.calc({f:1,t:.25});near(shm.x,0);near(shm.v,-.4*Math.PI);
for(const amplitude of [5,30,60]){const l=1.3,t=4,d=models.pendulum.calc({length:l,amplitude,t});const initial=10*l*(1-Math.cos(amplitude*Math.PI/180));const final=.5*l*l*d.omega*d.omega+10*l*(1-Math.cos(d.theta));near(final,initial,.001);}
near(models['travelling-wave'].calc({v:4,f:2,t:0}).wavelength,2);
near(models['standing-wave'].calc({n:3,t:0}).internal,2);near(models.beats.calc({difference:0,t:1}).envelope,2);
near(models.expansion.calc({temperature:100}).holeRadius,10.02);
near(models['phase-change'].calc({heat:18800}).melt,.5);near(models['phase-change'].calc({heat:35500}).temperature,0);
near(models.cooling.calc({k:.1,t:Math.log(2)/.1}).temperature,50);
near(models.gas.calc({temperature:600,t:0}).pressure/models.gas.calc({temperature:300,t:0}).pressure,2);
near(models.degrees.calc({mode:'5'}).gamma,1.4);
for(const path of ['isothermal','isobaric','adiabatic']){const d=models.pv.calc({path,ratio:2});near(d.heat,d.du+d.work);if(path==='adiabatic')near(d.heat,0,.00001);if(path==='isothermal')near(d.du,0);}
near(models.engine.calc({hot:600,cold:300}).work,500);
const mix=models.mixing.calc({t1:300,t2:500,blend:1});near(mix.final,400);near(mix.left+mix.right,800);
console.log(`Passed ${Object.keys(models).length} experiment models, ${states} input states, conservation identities and limiting cases.`);
