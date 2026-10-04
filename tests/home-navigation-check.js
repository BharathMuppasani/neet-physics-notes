/* User journeys for the homepage and shared navigation. Serve site/ on 8766. */
async (page) => {
  const context = await page.context().browser().newContext({viewport:{width:1280,height:900},reducedMotion:'reduce'});
  await context.route('**/*',route=>route.continue());
  const tab = await context.newPage();
  const errors=[],report=[];
  tab.on('pageerror',e=>errors.push(e.message));
  const check=(ok,message)=>{if(!ok)throw new Error(message);};
  const go=async(file)=>{await tab.goto('http://127.0.0.1:8766/'+file);await tab.waitForSelector('.topbar');};
  try{
    for(const width of [320,390,720,768,1024,1280]){
      await tab.setViewportSize({width,height:900});await go('index.html');
      const dimensions=await tab.evaluate(()=>({viewport:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth,nav:[...document.querySelectorAll('.nav > a,.chapter-menu > summary')].map(e=>({text:e.textContent.trim(),clipped:e.scrollWidth>e.clientWidth+1,right:e.getBoundingClientRect().right})),height:document.querySelector('.topbar').getBoundingClientRect().height}));
      check(dimensions.scroll<=dimensions.viewport+1,'homepage overflow at '+width);
      check(dimensions.nav.every(n=>!n.clipped&&n.right<=dimensions.viewport),'clipped navigation at '+width+': '+JSON.stringify(dimensions));
      check(await tab.locator('.home-focus a').count()===4,'original chapter shortcuts');
      check(await tab.locator('.home-volumes li a').count()===18,'full chapter directory');
      check(await tab.locator('.home-progress-group[open]').count()===0,'progress starts compact');
      await tab.locator('.chapter-menu summary').click();
      check(await tab.locator('.chapter-menu-panel').isVisible(),'open chapter menu');
      check(await tab.locator('.chapter-menu-volumes a').count()===18,'all chapters available in menu');
      const panel=await tab.locator('.chapter-menu-panel').boundingBox();
      check(panel.x>=0&&panel.x+panel.width<=dimensions.viewport+1,'menu fits screen');
      await tab.locator('.chapter-menu-volumes a[href="thermodynamics.html"]').scrollIntoViewIfNeeded();
      check(await tab.locator('.chapter-menu-volumes a[href="thermodynamics.html"]').isVisible(),'last chapter reachable');
      await tab.keyboard.press('Escape');
      check(!await tab.locator('.chapter-menu-panel').isVisible(),'escape closes menu');
      check(await tab.locator('.chapter-menu summary').evaluate(e=>e===document.activeElement),'escape restores focus');
      await tab.keyboard.press('Enter');
      check(await tab.locator('.chapter-menu-panel').isVisible(),'keyboard opens menu');
      await tab.mouse.click(2,20);
      check(!await tab.locator('.chapter-menu-panel').isVisible(),'outside click closes menu');
      await tab.evaluate(()=>window.scrollTo(0,0));
      check(await tab.evaluate(()=>window.scrollY)===0,'home starts at top');
      report.push({width,home:'fits',navigation:'all five destinations visible',menu:'18 chapters reachable'});
    }
    await tab.setViewportSize({width:390,height:844});await go('index.html');
    await tab.locator('.chapter-menu summary').click();
    await tab.locator('.chapter-menu-volumes a[href="fluids-1.html"]').click();
    await tab.waitForURL('**/fluids-1.html');
    check(await tab.locator('.chapter-menu summary').getAttribute('aria-current')==='page','chapter navigation active state');
    await tab.locator('[data-study-section="pressure"]').click();
    await tab.locator('.nav > a[href="index.html"]').click();await tab.waitForURL('**/index.html');
    check((await tab.locator('#study-overall').textContent()).startsWith('1 of 144'),'saved progress on home');
    check((await tab.locator('#home-continue').getAttribute('href')).startsWith('fluids-1.html#'),'resume latest chapter');
    await tab.locator('[data-progress-volume="3"] summary').click();
    check((await tab.locator('[data-study-chapter="fluids1"] [data-study-summary]').textContent()).startsWith('1 of 17'),'expanded progress matches saved study');
    await tab.locator('.nav > a[href="practice.html"]').click();await tab.waitForURL('**/practice.html');
    check(await tab.locator('#s-shown').textContent()==='317','practice remains intact');
    await tab.locator('.nav > a[href="formula-sheet.html"]').click();await tab.waitForURL('**/formula-sheet.html');
    await tab.locator('.nav > a[href="syllabus.html"]').click();await tab.waitForURL('**/syllabus.html');
    check(!errors.length,errors.join(';'));
    return {report,journey:'chapter → study mark → home resume → practice → revision → syllabus passed',errors};
  }finally{await context.close();}
}
