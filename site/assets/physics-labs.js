/* Guided physics experiments. Pure model calculations are also exposed for
   independent numerical checks. Motion is opt-in, pauses offscreen, and leaves
   every experiment usable with its sliders when reduced motion is requested. */
(() => {
  'use strict';
  const G=10, R=8.314, PI=Math.PI;
  const radians=x=>x*PI/180, clamp=(x,a,b)=>Math.min(b,Math.max(a,x));
  const f=(x,n=2)=>Number.isFinite(x)?Number(x.toFixed(n)).toLocaleString('en-US',{maximumFractionDigits:n}):'—';
  const control=(id,label,min,max,step,value,unit='')=>({id,label,min,max,step,value,unit});
  const select=(id,label,options,value)=>({id,label,options,value});
  const time=(max=5,value=0)=>control('t','Time',0,max,0.02,value,'s');
  const models={
    tangent:{controls:[control('t','Instant',0,3,0.1,1,'s'),control('gap','Time interval',0.02,1.5,0.02,1,'s')],calc:x=>({chord:2*x.t+x.gap,tangent:2*x.t})},
    integral:{controls:[control('n','Rectangles',2,40,1,6)],calc:x=>({estimate:16*(1-1/x.n),exact:16})},
    vernier:{controls:[control('length','Jaw opening',2,16,0.1,7.4,'mm')],calc:x=>{const length=Math.round(x.length*10)/10,main=Math.floor(length+1e-9),n=Math.round((length-main)*10);return {main,n,length};}},
    uncertainty:{controls:[control('error','Radius bound',0.5,10,0.5,2,'%')],calc:x=>({linear:2*x.error,upper:100*((1+x.error/100)**2-1),lower:100*(1-(1-x.error/100)**2)})},
    kinematics:{controls:[control('u','Initial velocity',-8,8,0.5,4,'m/s'),control('a','Acceleration',-3,3,0.25,-2,'m/s²'),time(5,1)],animate:'t',calc:x=>({position:x.u*x.t+x.a*x.t*x.t/2,velocity:x.u+x.a*x.t,acceleration:x.a,turn:x.a?-x.u/x.a:null})},
    distance:{controls:[control('out','Outward journey',0,10,0.5,7,'m'),control('back','Return journey',0,10,0.5,4,'m')],calc:x=>({position:x.out-x.back,distance:x.out+x.back,displacement:x.out-x.back})},
    components:{controls:[control('a','Magnitude',1,10,0.5,5,'m'),control('angle','Angle from +x',0,360,1,40,'°')],animate:'angle',rate:35,calc:x=>({x:x.a*Math.cos(radians(x.angle)),y:x.a*Math.sin(radians(x.angle)),magnitude:x.a})},
    projection:{controls:[control('angle','Force angle',0,180,1,60,'°')],calc:x=>({parallel:10*Math.cos(radians(x.angle)),work:30*Math.cos(radians(x.angle))})},
    projectile:{controls:[control('u','Launch speed',8,30,1,20,'m/s'),control('angle','Launch angle',10,80,1,45,'°'),time(6)],animate:'t',duration:x=>2*x.u*Math.sin(radians(x.angle))/G,calc:x=>{const ux=x.u*Math.cos(radians(x.angle)),uy=x.u*Math.sin(radians(x.angle)),duration=2*uy/G,t=Math.min(x.t,duration);return {x:ux*t,y:Math.max(0,uy*t-G*t*t/2),vx:ux,vy:uy-G*t,flight:duration,range:ux*duration,height:uy*uy/(2*G)};}},
    river:{controls:[control('swim','Swim speed',3,8,0.5,5,'m/s'),control('stream','Stream speed',0,6,0.5,3,'m/s'),control('angle','Upstream aim',0,70,1,0,'°'),time(40)],animate:'t',duration:x=>40/(x.swim*Math.cos(radians(x.angle))),calc:x=>{const vx=x.stream-x.swim*Math.sin(radians(x.angle)),vy=x.swim*Math.cos(radians(x.angle)),crossing=40/vy,t=Math.min(x.t,crossing);return {vx,vy,crossing,drift:vx*crossing,x:vx*t,y:vy*t};}},
    circle:{controls:[control('r','Radius',1,5,0.5,3,'m'),control('v','Speed',1,8,0.5,4,'m/s'),time(10)],animate:'t',calc:x=>({omega:x.v/x.r,acceleration:x.v*x.v/x.r,phase:x.v*x.t/x.r,period:2*PI*x.r/x.v})},
    atwood:{controls:[control('m1','Left mass',1,5,0.5,2,'kg'),control('m2','Right mass',1,5,0.5,3,'kg'),time(0.5)],animate:'t',calc:x=>({a:(x.m2-x.m1)*G/(x.m1+x.m2),tension:2*x.m1*x.m2*G/(x.m1+x.m2)})},
    lift:{controls:[control('a','Upward acceleration',-10,6,0.5,2,'m/s²')],calc:x=>({normal:60*(G+x.a),weight:600,net:60*x.a})},
    friction:{controls:[control('force','Horizontal pull',0,20,0.5,5,'N')],calc:x=>({friction:x.force<=12?x.force:8,acceleration:x.force<=12?0:(x.force-8)/2,sliding:x.force>12,limit:12})},
    incline:{controls:[control('angle','Incline angle',0,60,1,20,'°')],calc:x=>{const a=radians(x.angle),down=20*Math.sin(a),normal=20*Math.cos(a),limit=0.5*normal,sliding=down>limit+1e-8;return {down,normal,limit,friction:sliding?0.3*normal:down,sliding,acceleration:sliding?G*(Math.sin(a)-0.3*Math.cos(a)):0,repose:Math.atan(0.5)*180/PI};}},
    'spring-energy':{controls:[time(5)],animate:'t',calc:x=>{const displacement=0.5*Math.cos(Math.sqrt(20)*x.t),potential=10*displacement**2;return {x:displacement,potential,kinetic:2.5-potential,total:2.5,velocity:-0.5*Math.sqrt(20)*Math.sin(Math.sqrt(20)*x.t)};}},
    collision:{controls:[control('e','Restitution e',0,1,0.05,1),time(2.5)],animate:'t',calc:x=>({v1:2-4*x.e,v2:2+2*x.e,momentum:6,initialEnergy:18,finalEnergy:6+12*x.e*x.e,loss:12*(1-x.e*x.e)})},
    loop:{controls:[control('speed','Bottom launch speed',4,10,0.1,7.2,'m/s'),control('angle','Angle from bottom',0,360,1,0,'°')],animate:'angle',rate:45,calc:x=>{const q=x.speed*x.speed/10,c=(2-q)/3;const lossAngle=q>=5?360:q<2?Math.acos(1-q/2)*180/PI:Math.acos(clamp(c,-1,1))*180/PI;const a=Math.min(x.angle,lossAngle),v2=Math.max(0,x.speed*x.speed-20*(1-Math.cos(radians(a)))),tension=Math.max(0,v2+10*Math.cos(radians(a)));return {angle:a,speed:Math.sqrt(v2),tension,fullLoop:q>=5,lossAngle,minimum:Math.sqrt(50),turning:q<2,lost:x.angle>lossAngle&&q>=2,blocked:x.angle>lossAngle};}},
    'centre-mass':{controls:[control('m1','Left mass',1,6,0.5,2,'kg'),control('m2','Right mass',1,6,0.5,4,'kg'),control('x1','Left position',-4,-1,0.25,-3,'m'),control('x2','Right position',1,4,0.25,3,'m')],calc:x=>({centre:(x.m1*x.x1+x.m2*x.x2)/(x.m1+x.m2),total:x.m1+x.m2})},
    rolling:{controls:[time(3)],animate:'t',calc:x=>({bodies:[['Hoop',1,'plum'],['Disc',0.5,'water'],['Sphere',0.4,'green']].map(([name,beta,color])=>{const a=G*Math.sin(radians(20))/(1+beta),s=0.5*a*x.t*x.t,v=a*x.t;return {name,beta,color,a,s,v,translation:v*v/2,rotation:beta*v*v/2};})})},
    orbit:{controls:[control('radius','Orbit radius / Earth radius',1.2,5,0.1,2),time(10)],animate:'t',calc:x=>{const earth=6.4e6,gm=G*earth**2,r=x.radius*earth;return {speed:Math.sqrt(gm/r),period:2*PI*Math.sqrt(r**3/gm),gravity:G/x.radius**2,phase:x.t*0.8/x.radius**1.5};}},
    'gravity-profile':{controls:[control('r','Distance from centre / radius',0,3,0.05,0.5)],calc:x=>({gravity:x.r<=1?x.r:1/x.r**2,enclosed:x.r<=1?x.r**3:1,inside:x.r<1})},
    shm:{controls:[control('f','Frequency',0.5,2,0.1,1,'Hz'),time(4)],animate:'t',calc:x=>{const w=2*PI*x.f,p=w*x.t;return {phase:p,x:0.2*Math.cos(p),v:-0.2*w*Math.sin(p),a:-0.2*w*w*Math.cos(p),period:1/x.f};}},
    pendulum:{controls:[control('length','Length',0.5,2,0.1,1,'m'),control('amplitude','Initial swing',5,60,1,15,'°'),time(6)],animate:'t',calc:x=>{let theta=radians(x.amplitude),omega=0;const steps=Math.max(1,Math.ceil(x.t/0.005)),dt=x.t/steps;for(let i=0;i<steps;i++){const a=-G/x.length*Math.sin(theta);theta+=omega*dt+0.5*a*dt*dt;omega+=0.5*(a-G/x.length*Math.sin(theta))*dt;}const p0=2*PI*Math.sqrt(x.length/G);return {theta,omega,period:p0,correction:100*radians(x.amplitude)**2/16};}},
    'travelling-wave':{controls:[control('v','Wave speed',1,5,0.5,3,'m/s'),control('f','Frequency',0.5,2,0.1,1,'Hz'),time(5)],animate:'t',calc:x=>({wavelength:x.v/x.f,particle:0.15*Math.sin(2*PI*x.f*(2/x.v-x.t)),speed:x.v})},
    'standing-wave':{controls:[control('n','Harmonic number',1,5,1,2),time(5)],animate:'t',calc:x=>({frequency:x.n,wavelength:4/x.n,nodes:x.n+1,internal:x.n-1})},
    beats:{controls:[control('difference','Frequency difference',0,4,0.25,1,'Hz'),time(3)],animate:'t',calc:x=>({beat:x.difference,carrier:20+x.difference/2,envelope:2*Math.cos(PI*x.difference*x.t)})},
    expansion:{controls:[control('temperature','Temperature rise',0,300,5,100,'K')],calc:x=>{const strain=2e-5*x.temperature;return {strain,linear:100*strain,area:100*((1+strain)**2-1),holeRadius:10*(1+strain),visualScale:1+strain*25};}},
    'phase-change':{controls:[control('heat','Energy supplied',0,55000,500,18000,'J')],calc:x=>{const a=2100,b=35500;return {temperature:x.heat<a?-10+x.heat/210:x.heat<=b?0:(x.heat-b)/420,melt:clamp((x.heat-a)/33400,0,1),stage:x.heat<a?'Warming ice':x.heat<b?'Melting at 0°C':'Warming liquid water'};}},
    cooling:{controls:[control('k','Cooling coefficient',0.02,0.2,0.01,0.08,'min⁻¹'),control('t','Time',0,40,0.1,10,'min')],animate:'t',rate:3,calc:x=>({temperature:20+60*Math.exp(-x.k*x.t),rate:-60*x.k*Math.exp(-x.k*x.t),excess:60*Math.exp(-x.k*x.t)})},
    gas:{controls:[control('temperature','Absolute temperature',100,700,20,300,'K'),time(10)],animate:'t',calc:x=>({pressure:0.01*R*x.temperature/0.001,rms:Math.sqrt(3*R*x.temperature/0.028),energy:1.5*1.380649e-23*x.temperature})},
    degrees:{controls:[select('mode','Active modes',[['3','Monatomic: translation'],['5','Diatomic: translation + rotation'],['7','Diatomic: rotation + vibration']],'3')],calc:x=>{const d=Number(x.mode);return {degrees:d,cv:d*R/2,cp:(d/2+1)*R,gamma:1+2/d};}},
    pv:{controls:[select('path','Expansion path',[['isothermal','Isothermal'],['isobaric','Isobaric'],['adiabatic','Reversible adiabatic']],'isothermal'),control('ratio','Final / initial volume',1,3,0.05,2)],calc:x=>{const c=R*300,cv=R/0.4,r=x.ratio,t=x.path==='isothermal'?300:x.path==='isobaric'?300*r:300*r**(-0.4),work=x.path==='isothermal'?c*Math.log(r):x.path==='isobaric'?c*(r-1):c*(1-r**(-0.4))/0.4,du=cv*(t-300);return {temperature:t,work,du,heat:du+work,pressure:x.path==='isobaric'?c/0.01:x.path==='isothermal'?c/(0.01*r):c/0.01/r**1.4};}},
    engine:{controls:[control('hot','Hot reservoir',450,900,10,600,'K'),control('cold','Cold reservoir',150,400,10,300,'K')],calc:x=>({efficiency:1-x.cold/x.hot,rejected:1000*x.cold/x.hot,work:1000*(1-x.cold/x.hot)})},
    mixing:{controls:[control('t1','Left initial temperature',200,600,10,300,'K'),control('t2','Right initial temperature',200,600,10,500,'K'),control('blend','Equilibration progress',0,1,0.02,0)],animate:'blend',rate:0.18,calc:x=>{const final=(x.t1+x.t2)/2;return {final,pressure:2*R*final/0.02,left:x.t1+(final-x.t1)*x.blend,right:x.t2+(final-x.t2)*x.blend};}}
  };
  const colour=name=>`var(--${name})`;
  let labelScale=1;
  const line=(x1,y1,x2,y2,c='ink-2',dash=false,w=2)=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${colour(c)}" stroke-width="${w}"${dash?' stroke-dasharray="5 5"':''}/>`;
  const text=(x,y,s,c='ink-2',anchor='start',size=14)=>{
    const font=size*labelScale,available=anchor==='end'?x-12:anchor==='middle'?Math.min(x,640-x)*2-16:628-x;
    const limit=Math.max(8,Math.floor(available/(font*.53))),words=String(s).split(' '),rows=[''];
    for(const word of words){const last=rows.length-1;if(rows[last]&&(rows[last]+' '+word).length>limit)rows.push(word);else rows[last]+=(rows[last]?' ':'')+word;}
    const baseline=Math.min(y,300-(rows.length-1)*font*1.15);
    return `<text x="${x}" y="${baseline}" fill="${colour(c)}" text-anchor="${anchor}" font-size="${font}" font-family="var(--f-body)">${rows.map((row,i)=>`<tspan x="${x}" dy="${i?font*1.15:0}">${row}</tspan>`).join('')}</text>`;
  };
  const dot=(x,y,r=7,c='indigo')=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${colour(c)}"/>`;
  const rect=(x,y,w,h,c='surface-2',stroke='line',radius=8)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" fill="${colour(c)}" stroke="${colour(stroke)}" stroke-width="2"/>`;
  const ring=(x,y,r,c='indigo',w=2)=>`<circle cx="${x}" cy="${y}" r="${r}" fill="none" stroke="${colour(c)}" stroke-width="${w}"/>`;
  const path=(pts,c='indigo',width=3)=>`<polyline points="${pts.map(p=>p.join(',')).join(' ')}" fill="none" stroke="${colour(c)}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round"/>`;
  const polygon=(pts,c='indigo-soft')=>`<polygon points="${pts.map(p=>p.join(',')).join(' ')}" fill="${colour(c)}"/>`;
  function arrow(x1,y1,x2,y2,c='indigo',label=''){
    if(Math.hypot(x2-x1,y2-y1)<1)return dot(x1,y1,3,c)+(label?text(x1+8,y1-10,label,c):'');
    const a=Math.atan2(y2-y1,x2-x1),l=9;return line(x1,y1,x2,y2,c,false,3)+polygon([[x2,y2],[x2-l*Math.cos(a-.45),y2-l*Math.sin(a-.45)],[x2-l*Math.cos(a+.45),y2-l*Math.sin(a+.45)]],c)+(label?text(x2+8,y2-10,label,c):'');
  }
  const samples=(fn,a,b,n=90)=>Array.from({length:n+1},(_,i)=>{const x=a+(b-a)*i/n;return [x,fn(x)];});
  function plot(curves,{xmin=0,xmax=5,ymin=0,ymax=10,xlabel='x',ylabel='y',box=[65,35,590,235],areas=[],markers=[]}={}){
    const [l,t,r,b]=box,X=x=>l+(x-xmin)/(xmax-xmin)*(r-l),Y=y=>b-(y-ymin)/(ymax-ymin)*(b-t);
    let svg='';
    for(let i=0;i<=4;i++){
      const x=xmin+(xmax-xmin)*i/4,y=ymin+(ymax-ymin)*i/4;
      svg+=line(l,Y(y),r,Y(y),'line',true,1)+text(l-9,Y(y)+5,f(y,1),'muted','end',12)+text(X(x),b+19,f(x,1),'muted','middle',12);
    }
    svg+=line(l,t,l,b)+line(l,b,r,b)+text((l+r)/2,b+42,xlabel,'ink-2','middle')+text(l,t-13,ylabel,'ink-2');
    if(ymin<0&&ymax>0)svg+=line(l,Y(0),r,Y(0),'line-2',false,1.5);
    for(const area of areas)svg+=polygon(area.points.map(([x,y])=>[X(x),Y(y)]),area.color||'water-soft');
    for(const curve of curves)svg+=path(curve.points.map(([x,y])=>[X(x),Y(y)]),curve.color||'indigo',curve.width||3);
    for(const m of markers)svg+=line(X(m.x),t,X(m.x),b,'line-2',true,1)+dot(X(m.x),Y(m.y),6,m.color||'coral');
    return {svg,X,Y};
  }
  function energyBars(values,max,x=400,y=65,w=160){
    return values.map(([name,value,c],i)=>text(x,y+i*57,name,'ink-2','start',13)+rect(x,y+9+i*57,w,14)+rect(x,y+9+i*57,Math.max(0,w*value/max),14,c,c,4)+text(x+w+8,y+21+i*57,f(value)+' J',c,'start',12)).join('');
  }
  function spring(x1,x2,y){return path([[x1,y],[x1+10,y],...Array.from({length:17},(_,i)=>[x1+14+(x2-x1-28)*i/16,y+(i===0||i===16?0:i%2?9:-9)]),[x2-10,y],[x2,y]],'ink-2',2);}
  function scene(key,x,d,width=640){
    labelScale=Math.max(1,Math.min(1.85,640/Math.max(1,width)));
    let b='',stats=[];
    const add=(label,value,unit='')=>stats.push({label,value:f(value),unit});
    switch(key){
      case 'tangent':{
        const q=plot([{points:samples(t=>t*t,0,4.5)}],{xmax:4.5,ymax:22,xlabel:'Time t (s)',ylabel:'Position x (m)'}),a=x.t,z=x.t+x.gap;
        b=q.svg+line(q.X(a),q.Y(a*a),q.X(z),q.Y(z*z),'coral',false,3)+line(q.X(Math.max(0,a-.7)),q.Y(a*a+d.tangent*(Math.max(0,a-.7)-a)),q.X(a+.7),q.Y(a*a+d.tangent*.7),'green',true,2)+dot(q.X(a),q.Y(a*a),6)+dot(q.X(z),q.Y(z*z),6,'coral');add('Average velocity',d.chord,'m/s');add('Instantaneous velocity',d.tangent,'m/s');break;}
      case 'integral':{
        const q=plot([{points:samples(z=>2*z,0,4)}],{xmax:4,ymax:9,xlabel:'Position (m)',ylabel:'Force (N)'});b=q.svg;for(let i=0;i<x.n;i++){const dx=4/x.n,z=i*dx;b+=rect(q.X(z),q.Y(2*z),(q.X(z+dx)-q.X(z)),q.Y(0)-q.Y(2*z),'water-soft','water',0);}b+=path(samples(z=>2*z,0,4).map(([a,c])=>[q.X(a),q.Y(c)]));add('Rectangle estimate',d.estimate,'J');add('Exact work',d.exact,'J');break;}
      case 'vernier':{
        const start=Math.max(0,d.main-3),X=z=>65+(z-start)*30;b=rect(45,85,555,80,'surface','line')+rect(X(x.length),167,280,68,'water-soft','water');for(let i=start;i<=start+17;i++)b+=line(X(i),115,X(i),155)+text(X(i),106,i,'ink-2','middle',12);for(let i=0;i<=10;i++){const xx=X(x.length+i*.9);if(xx>600)continue;b+=line(xx,168,xx,195,i===d.n?'coral':'water',false,i===d.n?3:1.5)+text(xx,215,i,i===d.n?'coral':'water','middle',12);}b+=arrow(X(x.length),265,X(x.length),236,'water')+text(65,270,'Vernier zero → main reading + coincidence × 0.1 mm','ink-2','start',13);add('Main scale',d.main,'mm');add('Coincident division',d.n);add('Observed length',d.length,'mm');break;}
      case 'uncertainty':{
        b=ring(210,150,85*(1+x.error/100),'coral',3)+ring(210,150,85,'indigo',3)+ring(210,150,85*(1-x.error/100),'green',3)+arrow(210,150,295,150,'indigo','r')+text(380,105,'Outer circle: upper bound','coral')+text(380,140,'Nominal circle','indigo')+text(380,175,'Inner circle: lower bound','green');add('First-order area bound',d.linear,'%');add('Exact upper increase',d.upper,'%');add('Exact lower decrease',d.lower,'%');break;}
      case 'kinematics':{
        const vals=samples(t=>x.u*t+x.a*t*t/2,0,5),lo=Math.min(-1,...vals.map(p=>p[1])),hi=Math.max(1,...vals.map(p=>p[1]));const X=z=>65+(z-lo)/(hi-lo)*520;
        b=line(65,78,585,78)+rect(X(d.position)-18,47,36,22,'indigo','indigo')+dot(X(d.position)-11,75,5,'ink')+dot(X(d.position)+11,75,5,'ink')+text(65,29,`Position ${f(d.position)} m`)+arrow(X(d.position),100,X(d.position)+clamp(d.velocity*8,-80,80),100,'water');
        for(const [i,label,fn,colour,low,high] of [[0,'x (m)',t=>x.u*t+x.a*t*t/2,'indigo',lo,hi],[1,'v (m/s)',t=>x.u+x.a*t,'water',-24,24],[2,'a (m/s²)',()=>x.a,'coral',-4,4]]){const q=plot([{points:samples(fn,0,5),color:colour}],{xmax:5,ymin:low,ymax:high,box:[55+i*200,160,210+i*200,248],xlabel:'t (s)',ylabel:label,markers:[{x:x.t,y:fn(x.t)}]});b+=q.svg;}add('Position',d.position,'m');add('Velocity',d.velocity,'m/s');add('Acceleration',d.acceleration,'m/s²');break;}
      case 'distance':{
        const X=z=>100+(z+10)*22;b=line(65,170,590,170);for(let i=-10;i<=10;i+=2)b+=line(X(i),164,X(i),176)+text(X(i),195,i,'muted','middle',12);b+=arrow(X(0),70,X(x.out),70,'water',`out ${f(x.out)} m`)+arrow(X(x.out),120,X(d.position),120,'coral',`back ${f(x.back)} m`)+dot(X(0),170,7,'green')+dot(X(d.position),170,9,'indigo')+text(65,245,'Signed endpoint difference ≠ total path length');add('Displacement',d.displacement,'m');add('Distance',d.distance,'m');break;}
      case 'components':{
        const X=v=>320+v*10,Y=v=>150-v*10;b=line(205,150,435,150,'line-2')+line(320,35,320,265,'line-2')+text(444,155,'+x')+text(329,29,'+y')+line(X(d.x),150,X(d.x),Y(d.y),'water',true)+line(320,Y(d.y),X(d.x),Y(d.y),'coral',true)+arrow(320,150,X(d.x),150,'water')+arrow(X(d.x),150,X(d.x),Y(d.y),'coral')+arrow(320,150,X(d.x),Y(d.y),'indigo')+text(50,75,`A = ${f(x.a)} m`,'indigo')+text(50,105,`θ = ${f(x.angle,0)}°`)+text(50,225,'Blue: x projection','water')+text(50,250,'Coral: y projection','coral');add('x component',d.x,'m');add('y component',d.y,'m');add('Magnitude',d.magnitude,'m');break;}
      case 'projection':{
        const a=radians(x.angle);b=arrow(300,200,570,200,'water','s = 3 m')+arrow(300,200,300+120*Math.cos(a),200-120*Math.sin(a),'indigo','F = 10 N')+arrow(300,230,300+120*Math.cos(a),230,'coral')+line(300+120*Math.cos(a),200-120*Math.sin(a),300+120*Math.cos(a),230,'line-2',true)+text(65,55,'Only the projection along displacement contributes.');add('Parallel force',d.parallel,'N');add('Work',d.work,'J');break;}
      case 'projectile':{
        const q=plot([{points:Array.from({length:91},(_,i)=>{const t=d.flight*i/90;return [d.vx*t,x.u*Math.sin(radians(x.angle))*t-5*t*t];})}],{xmax:Math.ceil(x.u*x.u/G/10)*10+5,ymax:Math.ceil(x.u*x.u/(2*G)/5)*5+5,xlabel:'Horizontal distance (m)',ylabel:'Height (m)'});b=q.svg+dot(q.X(d.x),q.Y(d.y),8,'coral')+arrow(q.X(d.x),q.Y(d.y),q.X(d.x)+d.vx*1.3,q.Y(d.y),'water')+arrow(q.X(d.x),q.Y(d.y),q.X(d.x),q.Y(d.y)-d.vy*1.3,'coral')+text(400,27,'Blue: vₓ · coral: vᵧ','ink-2','start',12);add('Flight time',d.flight,'s');add('Range',d.range,'m');add('Vertical velocity',d.vy,'m/s');break;}
      case 'river':{
        const low=Math.min(-20,d.drift-10),high=Math.max(20,d.drift+10),X=z=>85+(z-low)/(high-low)*480,Y=z=>245-z*4;b=rect(55,80,540,170,'water-soft','water')+text(70,68,'Far bank: y = 40 m')+text(70,275,'Near bank: y = 0');for(let y=115;y<230;y+=40)b+=arrow(75,y,115+x.stream*5,y,'water');b+=line(X(0),Y(0),X(d.drift),Y(40),'indigo',true)+dot(X(d.x),Y(d.y),9,'indigo')+arrow(X(0),Y(0),X(-x.swim*Math.sin(radians(x.angle))*4),Y(x.swim*Math.cos(radians(x.angle))*4),'green')+text(375,285,'Green: swim velocity; dashed: ground route','ink-2','middle',12);add('Crossing time',d.crossing,'s');add('Downstream drift',d.drift,'m');add('Cross-river speed',d.vy,'m/s');break;}
      case 'circle':{
        const rr=x.r*20,c=Math.cos(d.phase),s=Math.sin(d.phase),xx=300+rr*c,yy=155-rr*s;b=ring(300,155,rr,'line-2')+dot(300,155,4,'ink-2')+dot(xx,yy,9)+arrow(xx,yy,xx-x.v*9*s,yy-x.v*9*c,'water')+arrow(xx,yy,xx-clamp(d.acceleration*4,10,85)*c,yy+clamp(d.acceleration*4,10,85)*s,'coral')+text(65,45,'Velocity tangent','water')+text(65,70,'Acceleration inward','coral')+text(65,285,'Arrow scales differ; compare direction and the labelled values.','muted','start',12);add('Angular speed',d.omega,'rad/s');add('Inward acceleration',d.acceleration,'m/s²');add('Period',d.period,'s');break;}
      case 'atwood':{
        const offset=d.a*x.t*x.t/2*90,y1=170-offset,y2=170+offset;b=ring(320,65,28,'ink-2',3)+line(292,65,292,y1)+line(348,65,348,y2)+rect(267,y1,50,38,'water-soft','water')+rect(323,y2,50,38,'coral-soft','coral')+text(292,y1+25,f(x.m1)+' kg','water','middle')+text(348,y2+25,f(x.m2)+' kg','coral','middle')+arrow(235,y1+20,235,y1+20-50,'green','T')+arrow(402,y2+20,402,y2+20-50,'green','T')+arrow(220,y1+20,220,y1+20+40,'water','m₁g')+arrow(417,y2+20,417,y2+20+40,'coral','m₂g');add('Right downward acceleration',d.a,'m/s²');add('String tension',d.tension,'N');break;}
      case 'lift':{
        b=rect(160,55,320,210,'surface','line-2')+line(175,230,465,230)+rect(265,216,110,14,'green-soft','green')+dot(320,110,15,'ink')+line(320,126,320,190,'ink',false,4)+line(320,190,300,215)+line(320,190,340,215)+arrow(250,175,250,175-d.normal/12,'green','N')+arrow(395,160,395,210,'coral','mg')+text(185,80,'Scale reads support, not gravity alone','ink-2','start',12);add('Scale force N',d.normal,'N');add('Gravitational force',d.weight,'N');add('Net upward force',d.net,'N');break;}
      case 'friction':{
        b=line(65,200,585,200)+rect(270,140,95,60,'water-soft','water')+text(317,176,'2 kg','water','middle')+arrow(365,168,365+x.force*7,168,'indigo','F')+arrow(270,180,270-d.friction*7,180,'coral','f')+text(65,70,d.sliding?'Sliding: use kinetic friction':'At rest: static friction adjusts',d.sliding?'coral':'green')+text(65,105,'Static limit 12 N · kinetic value 8 N');add('Actual friction',d.friction,'N');add('Acceleration',d.acceleration,'m/s²');break;}
      case 'incline':{
        const a=radians(x.angle),len=Math.min(460,210/Math.max(.001,Math.sin(a))),ex=100+len*Math.cos(a),ey=260-len*Math.sin(a),xx=100+len*.55*Math.cos(a),yy=260-len*.55*Math.sin(a);b=polygon([[100,260],[ex,ey],[ex,260]],'surface-2')+line(100,260,ex,ey,'ink-2')+`<g transform="translate(${xx} ${yy}) rotate(${-x.angle})">${rect(-35,-45,70,45,'water-soft','water')+arrow(0,-22,60,-22,'coral','f')+arrow(0,-22,0,-80,'green','N')}</g>`+arrow(xx-22*Math.sin(a),yy-22*Math.cos(a),xx-22*Math.sin(a),yy-22*Math.cos(a)+60,'water','mg')+text(65,40,d.sliding?'Downhill sliding':'Static equilibrium',d.sliding?'coral':'green')+text(65,67,`Threshold θᵣ = ${f(d.repose)}°`);add('Downhill weight',d.down,'N');add('Available static friction',d.limit,'N');add('Downhill acceleration',d.acceleration,'m/s²');break;}
      case 'spring-energy':{
        const xx=210+d.x*180;b=line(50,190,350,190)+rect(50,80,10,110,'line-2','line-2',1)+spring(60,xx-20,155)+rect(xx-20,130,40,60,'water-soft','water')+line(210,105,210,210,'line-2',true)+text(210,230,'equilibrium','muted','middle',12)+energyBars([['Potential',d.potential,'coral'],['Kinetic',d.kinetic,'water'],['Total',d.total,'green']],2.5);add('Displacement',d.x,'m');add('Potential energy',d.potential,'J');add('Kinetic energy',d.kinetic,'J');break;}
      case 'collision':{
        const impact=1,before=x.t<=impact,z=x.t-impact,left=before?100+150*x.t:250+d.v1*25*z,right=before?290:290+d.v2*25*z;
        b=line(50,190,590,190)+rect(left,150,40,34,'water-soft','water')+rect(right,140,55,44,'coral-soft','coral')+text(left+20,173,'1 kg','water','middle',12)+text(right+28,168,'2 kg','coral','middle',12)+arrow(left+20,125,left+20+(before?6:d.v1)*12,125,'water')+arrow(right+27,106,right+27+(before?0:d.v2)*12,106,'coral')+text(65,50,before?'Before impact':'After impact')+text(65,260,'Total momentum stays 6 kg m/s.');add('Cart 1 final speed',d.v1,'m/s');add('Cart 2 final speed',d.v2,'m/s');add('Kinetic energy lost',d.loss,'J');break;}
      case 'loop':{
        const a=radians(d.angle),xx=320+100*Math.sin(a),yy=160+100*Math.cos(a);b=ring(320,160,100,'line-2')+dot(320,160,4,'ink')+line(320,160,xx,yy,d.lost?'line-2':'indigo',d.lost)+dot(xx,yy,9,'coral')+arrow(xx,yy,xx+35*Math.cos(a),yy-35*Math.sin(a),'water')+text(65,40,d.fullLoop?'Enough speed for a complete loop':d.turning?'Turns back before reaching the top':'String loses tension before a full loop',d.fullLoop?'green':'coral')+text(65,283,d.blocked?(d.turning?'Stopped at the first turning point; the mass would swing back.':'Stopped at loss of tension: subsequent path is not circular.'):'θ is measured from the bottom.','muted','start',12);add('Speed at shown point',d.speed,'m/s');add('String tension',d.tension,'N');add('Minimum full-loop launch',d.minimum,'m/s');break;}
      case 'centre-mass':{
        const X=z=>320+z*55;b=line(70,170,570,170)+rect(X(x.x1)-22,140,44,30,'water-soft','water')+rect(X(x.x2)-22,140,44,30,'coral-soft','coral')+text(X(x.x1),132,f(x.m1)+' kg','water','middle')+text(X(x.x2),132,f(x.m2)+' kg','coral','middle')+polygon([[X(d.centre),174],[X(d.centre)-20,215],[X(d.centre)+20,215]],'green')+text(X(d.centre),243,'x_CM','green','middle');for(let i=-4;i<=4;i++)b+=line(X(i),165,X(i),175)+text(X(i),190,i,'muted','middle',12);add('Centre of mass',d.centre,'m');add('Total mass',d.total,'kg');break;}
      case 'rolling':{
        for(let i=0;i<3;i++){const z=d.bodies[i],xx=80+z.s*28,yy=90+i*65;b+=line(65,yy+18,590,yy+18,'line')+ring(xx,yy,17,z.color,3)+line(xx,yy,xx+15*Math.cos(z.s/.2),yy+15*Math.sin(z.s/.2),z.color)+text(65,yy-27,z.name+' · β='+z.beta,z.color)+text(590,yy-5,`${f(z.v)} m/s` ,z.color,'end');add(z.name+' acceleration',z.a,'m/s²');}b+=text(65,290,'Lanes straighten the same 20° incline for comparison.','muted','start',12);break;}
      case 'orbit':{
        const rr=x.radius*23,xx=320+rr*Math.cos(d.phase),yy=150-rr*Math.sin(d.phase);b=dot(320,150,23,'water')+ring(320,150,rr,'line-2')+dot(xx,yy,7,'coral')+arrow(xx,yy,xx-35*Math.sin(d.phase),yy-35*Math.cos(d.phase),'green')+arrow(xx,yy,xx-25*Math.cos(d.phase),yy+25*Math.sin(d.phase),'coral')+text(65,35,'Green: orbital velocity · coral: gravity')+text(65,280,'Distance is measured from Earth’s centre. Time is compressed.','muted','start',12);add('Orbital speed',d.speed/1000,'km/s');add('Period',d.period/60,'min');add('Gravity',d.gravity,'m/s²');break;}
      case 'gravity-profile':{
        const fn=r=>r<=1?r:1/r**2,q=plot([{points:samples(fn,0,3)}],{xmax:3,ymax:1.1,xlabel:'Distance from centre r/R',ylabel:'Gravity magnitude g/g₀',markers:[{x:x.r,y:d.gravity}]});b=q.svg+line(q.X(1),35,q.X(1),235,'water',true)+text(q.X(1)+8,52,'surface','water');add('Gravity / surface gravity',d.gravity);add('Enclosed / total mass',d.enclosed);break;}
      case 'shm':{
        const xx=180+85*Math.cos(d.phase),yy=150-85*Math.sin(d.phase);b=ring(180,150,85,'line-2')+dot(xx,yy,7,'coral')+line(xx,yy,xx,260,'coral',true)+line(65,260,295,260)+dot(xx,260,9)+text(180,40,'Uniform phase rotation','muted','middle',12)+text(180,288,'Horizontal projection is SHM','muted','middle',12);const q=plot([{points:samples(t=>.2*Math.cos(2*PI*x.f*t),0,4)}],{xmax:4,ymin:-.22,ymax:.22,box:[375,65,585,235],xlabel:'Time (s)',ylabel:'x (m)',markers:[{x:x.t,y:d.x}]});b+=q.svg;add('Displacement',d.x,'m');add('Velocity',d.v,'m/s');add('Acceleration',d.a,'m/s²');break;}
      case 'pendulum':{
        const len=70+x.length*55,xx=300+len*Math.sin(d.theta),yy=45+len*Math.cos(d.theta);b=line(250,45,350,45)+line(300,45,300,45+len,'line-2',true)+line(300,45,xx,yy,'ink-2',false,3)+dot(xx,yy,13,'water')+arrow(xx,yy,xx,yy+45,'coral')+arrow(xx,yy,xx-70*Math.sin(d.theta)*Math.cos(d.theta),yy+70*Math.sin(d.theta)**2,'green')+text(410,90,'Coral: weight downward','coral')+text(410,110,'Green: restoring part','green')+text(410,140,'Small-angle T₀ shown below','muted','start',12);add('Small-angle period',d.period,'s');add('Current angle',d.theta*180/PI,'°');add('Leading period correction',d.correction,'%');break;}
      case 'travelling-wave':{
        const X=z=>65+z*65,Y=z=>155-z*480;const pts=samples(z=>.15*Math.sin(2*PI*x.f*(z/x.v-x.t)),0,8);b=line(65,155,585,155,'line-2')+path(pts.map(([a,c])=>[X(a),Y(c)]));for(let i=0;i<=32;i++){const z=i/4,y=.15*Math.sin(2*PI*x.f*(z/x.v-x.t));b+=dot(X(z),Y(y),i===8?8:3,i===8?'coral':'water');}b+=line(X(2),50,X(2),245,'coral',true)+arrow(480,45,550,45,'green','v')+text(65,285,'Coral particle keeps x = 2 m; the pattern moves right.','muted','start',12);add('Wavelength',d.wavelength,'m');add('Marked displacement',d.particle,'m');add('Pattern speed',d.speed,'m/s');break;}
      case 'standing-wave':{
        const X=z=>65+z*260,Y=z=>155-z*150;b=line(65,155,585,155,'line-2')+path(samples(z=>Math.sin(x.n*PI*z/2)*Math.cos(2*PI*d.frequency*x.t),0,2).map(([a,c])=>[X(a),Y(c)]));for(let n=0;n<=x.n;n++)b+=dot(X(2*n/x.n),155,6,'coral');b+=text(65,285,'Coral points are nodes; adjacent loops have opposite phase.','muted','start',12);add('Frequency',d.frequency,'Hz');add('Wavelength',d.wavelength,'m');add('Internal nodes',d.internal);break;}
      case 'beats':{
        const fn=t=>2*Math.cos(PI*x.difference*t)*Math.cos(2*PI*(20+x.difference/2)*t);const q=plot([{points:samples(fn,Math.max(0,x.t-.6),Math.max(0,x.t-.6)+1.2,500),color:'water',width:1.4},{points:samples(t=>2*Math.abs(Math.cos(PI*x.difference*t)),Math.max(0,x.t-.6),Math.max(0,x.t-.6)+1.2),color:'coral'},{points:samples(t=>-2*Math.abs(Math.cos(PI*x.difference*t)),Math.max(0,x.t-.6),Math.max(0,x.t-.6)+1.2),color:'coral'}],{xmin:Math.max(0,x.t-.6),xmax:Math.max(0,x.t-.6)+1.2,ymin:-2.3,ymax:2.3,xlabel:'Time (s)' ,ylabel:'Displacement / single-wave amplitude',markers:[{x:x.t,y:fn(x.t)}]});b=q.svg+text(390,30,'Blue: rapid sum · coral: envelope','ink-2','start',12);add('Beat frequency',d.beat,'Hz');add('Carrier frequency',d.carrier,'Hz');add('Current signed envelope',d.envelope,'×A');break;}
      case 'expansion':{
        b=rect(175,70,290,175,'line','line-2')+`<g transform="translate(320 158) scale(${d.visualScale}) translate(-320 -158)">${rect(185,80,270,155,'coral-soft','coral')+`<circle cx="320" cy="158" r="35" fill="var(--surface)" stroke="var(--coral)" stroke-width="2"/>`}</g>`+ring(320,158,35,'ink-2')+text(65,35,'Grey: original plate and hole; coral: heated plate')+text(65,285,'Strain is exaggerated ×25 in the drawing; readouts are actual.','muted','start',12);add('Linear increase',d.linear,'%');add('Area increase',d.area,'%');add('Original 10 mm hole radius',d.holeRadius,'mm');break;}
      case 'phase-change':{
        const fn=q=>q<2100?-10+q/210:q<=35500?0:(q-35500)/420,p=plot([{points:[[0,-10],[2100,0],[35500,0],[55000,fn(55000)]]}],{xmax:55000,ymin:-12,ymax:50,xlabel:'Energy supplied (J)',ylabel:'Temperature (°C)',markers:[{x:x.heat,y:d.temperature}]});b=p.svg+text(230,210,'melting plateau','water');add('Temperature',d.temperature,'°C');add('Melted fraction',100*d.melt,'%');stats.push({label:'Stage',value:d.stage,unit:''});break;}
      case 'cooling':{
        const fn=t=>20+60*Math.exp(-x.k*t),q=plot([{points:samples(fn,0,40)}],{xmax:40,ymin:10,ymax:85,xlabel:'Time (min)',ylabel:'Temperature (°C)',markers:[{x:x.t,y:d.temperature}]});b=q.svg+line(q.X(0),q.Y(20),q.X(40),q.Y(20),'coral',true)+text(370,q.Y(20)-10,'Ambient 20°C','coral');add('Temperature',d.temperature,'°C');add('Cooling rate',d.rate,'°C/min');add('Excess above ambient',d.excess,'K');break;}
      case 'gas':{
        b=rect(130,50,380,200,'surface','line-2');const fold=z=>{const m=((z%2)+2)%2;return m<=1?m:2-m;};for(let i=0;i<28;i++){const a=Math.sin(i*17.1)*PI,scale=Math.sqrt(x.temperature/300)*.34,vx=Math.cos(a)*scale,vy=Math.sin(a)*scale,xx=145+350*fold(i*.137+vx*x.t),yy=65+170*fold(i*.271+vy*x.t);b+=dot(xx,yy,4,i%3?'water':'coral');}b+=text(65,285,'Representative 2D tracers; pressure law uses 3D molecules.','muted','start',12);add('Pressure',d.pressure/1000,'kPa');add('Rms molecular speed',d.rms,'m/s');break;}
      case 'degrees':{
        const terms=[['Translation x','water'],['Translation y','water'],['Translation z','water'],['Rotation 1','plum'],['Rotation 2','plum'],['Vibration kinetic','coral'],['Vibration potential','coral']];terms.slice(0,d.degrees).forEach(([label,c],i)=>{const col=i%2,row=Math.floor(i/2);b+=rect(90+col*250,35+row*60,220,42,c+'-soft',c)+text(105+col*250,61+row*60,label,c);});add('Cᵥ',d.cv,'J/(mol K)');add('Cₚ',d.cp,'J/(mol K)');add('γ',d.gamma);break;}
      case 'pv':{
        const c=R*300,fn=v=>x.path==='isobaric'?c/.01:x.path==='isothermal'?c/v:c/.01*(.01/v)**1.4,pts=samples(fn,.01,.01*x.ratio),q=plot([{points:samples(fn,.01,.03)}],{xmin:.008,xmax:.032,ymax:280000,xlabel:'Volume (m³)',ylabel:'Pressure (Pa)',areas:[{points:[[.01,0],...pts,[.01*x.ratio,0]],color:'water-soft'}],markers:[{x:.01*x.ratio,y:d.pressure}]});b=q.svg;add('Work by gas',d.work,'J');add('Internal energy change',d.du,'J');add('Heat absorbed',d.heat,'J');add('Final temperature',d.temperature,'K');break;}
      case 'engine':{
        const ww=1000*d.efficiency/8,qc=d.rejected/8;b=rect(80,35,170,65,'coral-soft','coral')+text(165,63,'Hot reservoir','coral','middle')+text(165,84,x.hot+' K','coral','middle')+rect(80,210,170,65,'water-soft','water')+text(165,238,'Cold reservoir','water','middle')+text(165,259,x.cold+' K','water','middle')+rect(105,130,120,50,'green-soft','green')+text(165,160,'Engine','green','middle')+arrow(165,100,165,128,'coral')+arrow(165,181,165,208,'water')+arrow(225,155,325,155,'green','W')+energyBars([['Heat in',1000,'coral'],['Work out',d.work,'green'],['Heat rejected',d.rejected,'water']],1000,395,60,150);add('Carnot efficiency',d.efficiency*100,'%');add('Work per cycle',d.work,'J');add('Heat rejected',d.rejected,'J');break;}
      case 'mixing':{
        b=rect(80,85,200,130,'water-soft','water')+rect(360,85,200,130,'coral-soft','coral')+line(280,150,360,150,'ink-2',false,9)+rect(310,140,20,20,x.blend?'green-soft':'surface',x.blend?'green':'ink-2',2)+text(180,120,'1 mol · 10 L','water','middle')+text(460,120,'1 mol · 10 L','coral','middle')+text(180,165,f(d.left)+' K','water','middle',22)+text(460,165,f(d.right)+' K','coral','middle',22)+text(320,260,'Rigid + insulated outer system: Q = 0, W = 0','ink-2','middle');add('Final equilibrium temperature',d.final,'K');add('Final common pressure',d.pressure/1000,'kPa');break;}
    }
    return {svg:`<svg viewBox="0 0 640 310" role="img" aria-label="${key.replaceAll('-',' ')} experiment; numerical values follow below"><title>${key.replaceAll('-',' ')}: change inputs to compare the scene with its equation</title>${b}</svg>`,stats};
  }
  function read(root){return Object.fromEntries([...root.querySelectorAll('[data-lab-input]')].map(el=>[el.dataset.labInput,el.tagName==='SELECT'?el.value:Number(el.value)]));}
  const controllers=[],reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function init(root){
    const key=root.dataset.physicsLab,m=models[key];if(!m)return;
    const controls=root.querySelector('.lab-controls');
    controls.innerHTML=m.controls.map(c=>c.options?`<label class="lab-control" for="lab-${key}-${c.id}"><span>${c.label}</span><select id="lab-${key}-${c.id}" data-lab-input="${c.id}">${c.options.map(([v,t])=>`<option value="${v}"${String(c.value)===v?' selected':''}>${t}</option>`).join('')}</select></label>`:`<label class="lab-control" for="lab-${key}-${c.id}"><span>${c.label}<output for="lab-${key}-${c.id}" data-lab-value="${c.id}">${c.value} ${c.unit}</output></span><input id="lab-${key}-${c.id}" data-lab-input="${c.id}" type="range" min="${c.min}" max="${c.max}" step="${c.step}" value="${c.value}" aria-label="${c.label}${c.unit?' ('+c.unit+')':''}"></label>`).join('');
    const stage=root.querySelector('.lab-stage'),metrics=root.querySelector('.lab-metrics'),play=root.querySelector('[data-lab-play]');
    let playing=false,last=0,clock=0,request=null,visible=true;
    const update=()=>{
      const x=read(root);
      if(m.duration){const el=root.querySelector('[data-lab-input="t"]'),duration=m.duration(x);el.max=duration;if(Number(el.value)>duration){el.value=duration;x.t=duration;}}
      const d=m.calc(x),out=scene(key,x,d,stage.clientWidth);stage.innerHTML=out.svg;
      metrics.innerHTML=out.stats.map(s=>`<div><dt>${s.label}</dt><dd>${s.value}<span>${s.unit}</span></dd></div>`).join('');
      for(const c of m.controls){const el=root.querySelector(`[data-lab-input="${c.id}"]`),label=root.querySelector(`[data-lab-value="${c.id}"]`);if(label)label.textContent=f(Number(el.value),c.id==='n'?0:2)+(c.unit?' '+c.unit:'');}
      root.dataset.modelState=JSON.stringify(d);
    };
    function stop(){playing=false;last=0;if(request)cancelAnimationFrame(request);request=null;play.textContent='Play motion';play.setAttribute('aria-pressed','false');metrics.removeAttribute('aria-live');}
    function frame(now){
      if(!playing||!visible||document.hidden){stop();return;}
      if(!last)last=now;const dt=Math.min((now-last)/1000,.05);last=now;
      const el=root.querySelector(`[data-lab-input="${m.animate}"]`),v=clock+dt*(m.rate||1),max=Number(el.max);clock=v;
      if(v>=max){el.value=max;update();stop();return;}
      // Range elements quantise to step: retain the fractional clock separately.
      el.value=v;update();request=requestAnimationFrame(frame);
    }
    const api={stop,root};controllers.push(api);
    controls.addEventListener('input',()=>{stop();update();});controls.addEventListener('change',()=>{stop();update();});
    if(m.animate&&!reduced){play.hidden=false;play.addEventListener('click',()=>{if(playing){stop();return;}controllers.forEach(c=>c.stop());const el=root.querySelector(`[data-lab-input="${m.animate}"]`);if(Number(el.value)>=Number(el.max)-Number(el.step||0.01))el.value=el.min;playing=true;last=0;clock=Number(el.value);play.textContent='Pause motion';play.setAttribute('aria-pressed','true');request=requestAnimationFrame(frame);});}
    else play.hidden=true;
    root.querySelector('[data-lab-reset]').addEventListener('click',()=>{stop();for(const c of m.controls){root.querySelector(`[data-lab-input="${c.id}"]`).value=c.value;}update();});
    root.querySelector('[data-lab-status]').textContent=reduced&&m.animate?'Reduced motion is on. Use the time or angle slider to inspect each state.':m.animate?'Play, pause, or scrub the slider to inspect a moment.':'Change one input, then connect the result to the equation.';
    if('IntersectionObserver'in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(!visible)stop();},{rootMargin:'120px'}).observe(root);
    if('ResizeObserver'in window){let previous=0;new ResizeObserver(entries=>{const width=entries[0].contentRect.width;if(Math.abs(width-previous)>1){previous=width;update();}}).observe(stage);}
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    root.querySelectorAll('[data-predict-choice]').forEach(button=>button.addEventListener('click',()=>{const correct=Number(button.dataset.predictChoice)===Number(root.dataset.predictionAnswer),feedback=root.querySelector('.lab-prediction-feedback');feedback.hidden=false;feedback.querySelector('strong').textContent=correct?'Yes — connect that prediction to the model.':'Revisit the condition in the question.';root.querySelectorAll('[data-predict-choice]').forEach(b=>{b.setAttribute('aria-pressed',String(b===button));});}));
    update();
  }
  function enhanceNotes(){
    document.querySelectorAll('.lesson-note').forEach((note,index)=>{
      const list=note.querySelector('.prose > ol');if(!list||list.children.length<2)return;
      const items=[...list.children],nav=document.createElement('div');nav.className='derivation-controls';
      const toggle=document.createElement('button');toggle.className='btn small';toggle.textContent='Walk through the steps';toggle.setAttribute('aria-expanded','false');
      const prev=document.createElement('button'),next=document.createElement('button'),count=document.createElement('span');prev.className=next.className='btn small';prev.textContent='← Previous';next.textContent='Next step →';count.className='small muted';count.setAttribute('aria-live','polite');
      let active=false,current=0;const draw=()=>{items.forEach((li,i)=>{li.hidden=active&&i>current;li.classList.toggle('current-step',active&&i===current);});prev.hidden=next.hidden=count.hidden=!active;prev.disabled=current===0;next.disabled=current===items.length-1;count.textContent=`Step ${current+1} of ${items.length}`;toggle.textContent=active?'Show all steps':'Walk through the steps';toggle.setAttribute('aria-expanded',String(active));};
      toggle.addEventListener('click',()=>{active=!active;current=0;draw();});prev.addEventListener('click',()=>{current=Math.max(0,current-1);draw();});next.addEventListener('click',()=>{current=Math.min(items.length-1,current+1);draw();});nav.append(toggle,prev,count,next);list.before(nav);draw();
    });
  }
  window.PhysicsLabs={models,scene};
  document.addEventListener('DOMContentLoaded',()=>{document.querySelectorAll('[data-physics-lab]').forEach(init);enhanceNotes();});
})();
