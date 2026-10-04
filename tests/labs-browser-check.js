/* Run against the built site on localhost:8767 using Playwright. */
async page => {
 const browser=page.context().browser(),context=await browser.newContext({viewport:{width:1280,height:900},reducedMotion:'no-preference'});
 const tab=await context.newPage(),errors=[],report=[];
 await context.route('**/*',r=>r.continue());tab.on('pageerror',e=>errors.push(e.message));tab.setDefaultTimeout(10000);
 const check=(ok,message)=>{if(!ok)throw Error(message);};
 const go=async file=>{await tab.goto('http://127.0.0.1:8767/'+file);await tab.evaluate(async()=>{await MathJax.startup.promise;await Site._typesetChain;});};
 try{
  await go('index.html');const files=await tab.evaluate(()=>Site.CHAPTERS.filter(c=>!['solids','fluids1','fluids2'].includes(c.key)).map(c=>c.page));
  let total=0;
  for(const file of files){
   await go(file);const labs=tab.locator('[data-physics-lab]'),count=await labs.count();check(count>=2,file+': needs multiple experiments');total+=count;
   check(await tab.locator('.theory-depth[open],.lab-equation-depth[open]').count()===0,file+': extra theory should start collapsed');
   for(let i=0;i<count;i++){
    const lab=labs.nth(i),key=await lab.getAttribute('data-physics-lab');await lab.scrollIntoViewIfNeeded();
    check(await lab.locator('.lab-stage svg').count()===1,key+': scene');check(await lab.locator('.lab-problem-guide ol li').count()===3,key+': solving recipe');
    const before=await lab.getAttribute('data-model-state'),input=lab.locator('[data-lab-input]').first();
    await input.evaluate(el=>{el.value=el.tagName==='SELECT'?el.options[el.options.length-1].value:el.value===el.max?el.min:el.max;el.dispatchEvent(new Event('input',{bubbles:true}));});
    check(await lab.getAttribute('data-model-state')!==before,key+': input must update');
    await lab.locator('[data-lab-reset]').click();check(await lab.getAttribute('data-model-state')===before,key+': reset');
    await lab.locator('.lab-prediction summary').click();await lab.locator('[data-predict-choice]').first().click();check(await lab.locator('.lab-prediction-feedback').isVisible(),key+': prediction feedback');
    await lab.locator('.lab-equation-depth summary').click();check(await lab.locator('.equation-story').isVisible(),key+': optional explanation');await lab.locator('.lab-equation-depth summary').click();
    const play=lab.locator('[data-lab-play]');
    if(await play.isVisible()){
     const valueBefore=await lab.locator('.lab-stage').innerHTML();await play.click();await tab.waitForTimeout(120);await play.click();check(await lab.locator('.lab-stage').innerHTML()!==valueBefore,key+': motion must advance');
     const paused=await lab.locator('.lab-stage').innerHTML();await tab.waitForTimeout(70);check(await lab.locator('.lab-stage').innerHTML()===paused,key+': pause must stop');await lab.locator('[data-lab-reset]').click();
    }
   }
   for(const width of [320,390,768]){await tab.setViewportSize({width,height:844});const overflow=await tab.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth+1);check(!overflow,file+' overflow '+width);check(await tab.locator('mjx-merror').count()===0,file+' invalid maths');}
   await tab.setViewportSize({width:1280,height:900});report.push({file,experiments:count,status:'controls, reset, predictions, optional theory, motion and responsive layouts passed'});
  }
  check(total===35,'all 35 experiments present');
  await go('linear.html');const walkthrough=tab.locator('.derivation-controls').first();await walkthrough.evaluate(el=>{el.closest('details').open=true;});check(await walkthrough.count()===1,'guided optional derivation');await walkthrough.locator('button').first().click();check(await walkthrough.locator('span').innerText()==='Step 1 of 2'||(await walkthrough.locator('span').innerText()).startsWith('Step 1 of '),'step count');await walkthrough.locator('button').last().click();check((await walkthrough.locator('span').innerText()).startsWith('Step 2 of '),'next step');
  const reduced=await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'}),small=await reduced.newPage();await small.goto('http://127.0.0.1:8767/plane.html');await small.waitForSelector('#lab-projectile .lab-stage svg');check(!await small.locator('#lab-projectile [data-lab-play]').isVisible(),'reduced motion suppresses play');const initial=await small.locator('#lab-projectile').getAttribute('data-model-state');await small.locator('#lab-projectile [data-lab-input=t]').evaluate(el=>{el.value=1;el.dispatchEvent(new Event('input',{bubbles:true}));});check(await small.locator('#lab-projectile').getAttribute('data-model-state')!==initial,'reduced motion supports scrubbing');await reduced.close();
  check(errors.length===0,errors.join('; '));return {report,total,errors};
 }finally{await context.close();}
}
