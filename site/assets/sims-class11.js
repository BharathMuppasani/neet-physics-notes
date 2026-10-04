/* Small, labelled explorations: predictions are recomputed from the same stated
   laws as the lesson. Graphs use explicit axes and physical units. */
(() => {
  const models = {
    units: {
      controls: [['e','Radius uncertainty',0.1,5,0.1,2,'%']],
      note: 'Area is proportional to radius squared. For small uncertainties, the first-order worst-case percentage uncertainty in area is twice that in radius.',
      result: x => ({ text: `Radius uncertainty ${x.e.toFixed(1)}% → area uncertainty ≈ ${(2*x.e).toFixed(1)}%`, points: [[0,0],[x.e,2*x.e]], xmax:5,ymax:10,xlabel:'Radius uncertainty (%)',ylabel:'Area uncertainty (%)' })
    },
    vectors: {
      controls: [['a','Vector magnitude',1,10,1,5,'m'],['theta','Angle from +x',0,360,5,40,'°']],
      note: 'A vector’s magnitude stays positive while its components change sign across quadrants. x=A cosθ and y=A sinθ; angle here is measured counterclockwise from +x.',
      result: x => {const t=x.theta*Math.PI/180; const a=x.a*Math.cos(t),b=x.a*Math.sin(t);return {text:`x component ${a.toFixed(2)} m · y component ${b.toFixed(2)} m · magnitude ${x.a} m`,points:[[0,0],[a,b]],xmin:-10,xmax:10,ymin:-10,ymax:10,xlabel:'x (m)',ylabel:'y (m)'};}
    },
    linear: {
      controls: [['u','Initial velocity',-10,10,1,4,'m/s'],['a','Constant acceleration',-4,4,0.5,-2,'m/s²']],
      note: 'The velocity–time slope is acceleration. Where the line crosses zero, motion reverses. Signed area gives displacement; the sum of absolute areas gives distance.',
      result: x => ({text:`At 5 s: v=${(x.u+5*x.a).toFixed(1)} m/s · displacement=${(5*x.u+12.5*x.a).toFixed(1)} m`,points:[[0,x.u],[5,x.u+5*x.a]],xmax:5,ymin:-30,ymax:30,xlabel:'Time (s)',ylabel:'Velocity (m/s)'})
    },
    plane: {
      controls: [['u','Launch speed',5,30,1,20,'m/s'],['theta','Launch angle',5,85,5,30,'°']],
      note: 'Horizontal velocity stays constant while gravity changes vertical velocity. This model assumes no air drag, g=10 m/s² and equal launch/landing heights. Compare complementary launch angles.',
      result: x => {const a=x.theta*Math.PI/180,T=2*x.u*Math.sin(a)/10;return {text:`Flight time ${T.toFixed(2)} s · maximum rise ${(x.u*x.u*Math.sin(a)**2/20).toFixed(2)} m · range ${(x.u*Math.cos(a)*T).toFixed(2)} m`,points:Array.from({length:61},(_,i)=>{const t=i*T/60;return[x.u*Math.cos(a)*t,x.u*Math.sin(a)*t-5*t*t];}),xmax:90,ymax:45,xlabel:'Horizontal distance (m)',ylabel:'Height (m)'};}
    },
    work: {
      controls: [['m','Mass',1,5,0.5,2,'kg'],['v','Speed',0,10,0.5,4,'m/s']],
      note: 'Translational kinetic energy is K=mv²/2. Doubling speed quadruples energy at fixed mass. This model excludes rotation.',
      result: x => ({text:`Kinetic energy ${(0.5*x.m*x.v*x.v).toFixed(2)} J`,points:Array.from({length:41},(_,i)=>[i/4,0.5*x.m*(i/4)**2]),xmax:10,ymax:250,xlabel:'Speed (m/s)',ylabel:'Kinetic energy (J)'})
    },
    rotation: {
      controls: [['i','Moment of inertia',0.2,4,0.2,2,'kg m²']],
      note: 'With zero external torque, angular momentum is conserved. Here L=4 kg m²/s, so ω=L/I and K=L²/(2I). An inward rearrangement needs work even though angular momentum stays fixed.',
      result: x => ({text:`Angular speed ${(4/x.i).toFixed(2)} rad/s · kinetic energy ${(8/x.i).toFixed(2)} J`,points:Array.from({length:39},(_,i)=>{const I=0.2+i*0.1;return[I,4/I];}),xmax:4,ymax:20,xlabel:'Inertia (kg m²)',ylabel:'Angular speed (rad/s)'})
    },
    gravitation: {
      controls: [['h','Height / Earth radius',0,3,0.1,1,'']],
      note: 'For a spherical source, g/g₀=1/(1+h/R)². The source distance is R+h, not h. This plot is for height above the surface, not depth inside Earth.',
      result: x => ({text:`At h/R=${x.h.toFixed(1)}, g/g₀=${(1/(1+x.h)**2).toFixed(3)}`,points:Array.from({length:61},(_,i)=>[i/20,1/(1+i/20)**2]),xmax:3,ymax:1,xlabel:'Height / radius',ylabel:'Gravity / surface gravity'})
    },
    oscillations: {
      controls: [['a','Amplitude',0.02,0.2,0.02,0.1,'m'],['f','Frequency',0.5,3,0.5,1,'Hz']],
      note: 'For x=A cos(2πft), a cycle takes 1/f seconds and maximum speed is 2πfA. Changing amplitude does not change this ideal oscillator’s period.',
      result: x => ({text:`Period ${(1/x.f).toFixed(2)} s · maximum speed ${(2*Math.PI*x.f*x.a).toFixed(2)} m/s`,points:Array.from({length:201},(_,i)=>[i/100,x.a*Math.cos(2*Math.PI*x.f*i/100)]),xmax:2,ymin:-0.2,ymax:0.2,xlabel:'Time (s)',ylabel:'Displacement (m)'})
    },
    waves: {
      controls: [['v','Propagation speed',1,10,1,4,'m/s'],['f','Source frequency',1,5,0.5,2,'Hz']],
      note: 'This is a snapshot at t=0 of a transverse wave of amplitude 0.1 m. Wavelength λ=v/f is the distance between adjacent equal-phase points. Particle displacement is vertical; propagation is along x.',
      result: x => ({text:`Wavelength ${(x.v/x.f).toFixed(2)} m · frequency ${x.f.toFixed(1)} Hz`,points:Array.from({length:401},(_,i)=>[i/50,0.1*Math.sin(2*Math.PI*x.f*(i/50)/x.v)]),xmax:8,ymin:-0.15,ymax:0.15,xlabel:'Position (m)',ylabel:'Displacement (m)'})
    },
    'thermal-properties': {
      controls: [['l','Slab thickness',0.05,0.5,0.05,0.1,'m'],['dt','Face temperature difference',5,50,5,20,'K']],
      note: 'For steady one-dimensional conduction, heat rate κAΔT/L. Here κ=0.5 W/(m K), area=2 m² and side losses are neglected. Increasing thickness raises thermal resistance.',
      result: x => ({text:`Heat rate ${(x.dt/x.l).toFixed(1)} W · resistance ${x.l.toFixed(2)} K/W`,points:Array.from({length:46},(_,i)=>{const L=0.05+i/100;return[L,x.dt/L];}),xmax:0.5,ymax:1000,xlabel:'Thickness (m)',ylabel:'Heat rate (W)'})
    },
    'kinetic-theory': {
      controls: [['t','Absolute temperature',100,1000,50,300,'K'],['m','Molar mass',4,40,4,28,'g/mol']],
      note: 'Rms speed √(3RT/M) uses molar mass in kg/mol. R=8.314 J/(mol K). Lighter gases at the same temperature have higher speeds but equal mean translational energy per molecule.',
      result: x => ({text:`Rms speed ${(Math.sqrt(3*8.314*x.t/(x.m/1000))).toFixed(1)} m/s`,points:Array.from({length:51},(_,i)=>{const T=i*20;return[T,Math.sqrt(3*8.314*T/(x.m/1000))];}),xmax:1000,ymax:2500,xlabel:'Temperature (K)',ylabel:'Rms speed (m/s)'})
    },
    thermodynamics: {
      controls: [['r','Final / initial volume',1,4,0.1,2,'']],
      note: 'Reversible isothermal expansion of 1 mol at 300 K: p=nRT/V, ΔU=0 and Q=W=nRT ln(Vf/Vi). Initial volume is 0.01 m³. The shaded area is work by the gas. This is not free expansion into vacuum.',
      result: x => {const a=0.01,b=a*x.r,C=8.314*300;return {text:`Work by gas ${(C*Math.log(x.r)).toFixed(1)} J · heat input equals work · ΔU=0`,points:Array.from({length:61},(_,i)=>{const V=a+(b-a)*i/60;return[V,C/V];}),xmin:0.005,xmax:0.04,ymax:260000,xlabel:'Volume (m³)',ylabel:'Pressure (Pa)',area:true};}
    }
  };
  const format = n => Math.abs(n)>=10000 ? n.toExponential(1) : Number(n.toFixed(3)).toString();
  function graph(g) {
    const W=640,H=290,left=85,right=15,top=25,bottom=60;
    const xmin=g.xmin??0,ymin=g.ymin??0;
    const px=x=>left+(x-xmin)/(g.xmax-xmin)*(W-left-right);
    const py=y=>H-bottom-(y-ymin)/(g.ymax-ymin)*(H-top-bottom);
    const points=g.points.map(([x,y])=>`${px(x).toFixed(2)},${py(y).toFixed(2)}`).join(' ');
    const area=g.area?`<polygon points="${px(g.points[0][0])},${py(0)} ${points} ${px(g.points.at(-1)[0])},${py(0)}" fill="#d7dcf5"/>`:'';
    return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${g.ylabel} versus ${g.xlabel}"><title>${g.ylabel} versus ${g.xlabel}</title>
      ${area}<path d="M${left},${top}V${H-bottom}H${W-right}" fill="none" stroke="#68728b"/>
      ${ymin<0?`<path d="M${left},${py(0)}H${W-right}" stroke="#c8cede"/>`:''}
      <polyline points="${points}" fill="none" stroke="#485dc4" stroke-width="3"/>
      <g fill="#424e68" font-family="sans-serif" font-size="14"><text x="${left-8}" y="${top+5}" text-anchor="end">${format(g.ymax)}</text><text x="${left-8}" y="${H-bottom}" text-anchor="end">${format(ymin)}</text><text x="${left}" y="${H-bottom+23}">${format(xmin)}</text><text x="${W-right}" y="${H-bottom+23}" text-anchor="end">${format(g.xmax)}</text><text x="${W/2}" y="${H-12}" text-anchor="middle">${g.xlabel}</text><text transform="translate(18,${H/2}) rotate(-90)" text-anchor="middle">${g.ylabel}</text></g></svg>`;
  }
  document.addEventListener('DOMContentLoaded',()=>{
    document.querySelectorAll('[data-model]').forEach(el=>{
      const key=el.dataset.model,m=models[key],box=el.querySelector('.model-content');
      if(!m) return;
      box.innerHTML=`<div class="controls">${m.controls.map(([id,label,min,max,step,value,unit])=>`<label for="model-${key}-${id}"><span>${label} (<span data-value="${id}">${value}</span> ${unit})</span><input id="model-${key}-${id}" type="range" min="${min}" max="${max}" step="${step}" value="${value}" data-name="${id}"></label>`).join('')}</div><div class="model-graph"></div><p class="model-readout" aria-live="polite"></p><p class="sim-note">${m.note}</p>`;
      const update=()=>{
        const values={};box.querySelectorAll('input').forEach(input=>{values[input.dataset.name]=Number(input.value);box.querySelector(`[data-value="${input.dataset.name}"]`).textContent=input.value;});
        const g=m.result(values);box.querySelector('.model-graph').innerHTML=graph(g);box.querySelector('.model-readout').textContent=g.text;
      };
      box.querySelectorAll('input').forEach(input=>input.addEventListener('input',update));update();
    });
  });
})();
