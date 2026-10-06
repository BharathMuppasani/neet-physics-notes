/* User journeys for the homepage chapter cards and direct navigation. Serve dist/ on 8766. */
async (page) => {
  const context = await page.context().browser().newContext({viewport:{width:1280,height:900},reducedMotion:'reduce'});
  await context.route('**/*',route=>route.continue());
  const tab = await context.newPage();
  const errors=[],report=[];
  tab.on('pageerror',e=>errors.push(e.message));
  const check=(ok,message)=>{if(!ok)throw new Error(message);};
  const go=async(file)=>{await tab.goto('http://127.0.0.1:8766/'+file);await tab.waitForSelector('.topbar');};
  const clickNav=async(file)=>{await tab.locator('.nav > a[href="'+file+'"]').click();await tab.waitForURL('**/'+file);};
  try{
    for(const width of [320,390,720,768,1024,1280]){
      await tab.setViewportSize({width,height:900});await go('index.html');
      const dimensions=await tab.evaluate(()=>({viewport:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth,nav:[...document.querySelectorAll('.nav > a')].map(e=>({text:e.textContent.trim(),clipped:e.scrollWidth>e.clientWidth+1,right:e.getBoundingClientRect().right})),height:document.querySelector('.topbar').getBoundingClientRect().height}));
      check(dimensions.scroll<=dimensions.viewport+1,'homepage overflow at '+width);
      check(dimensions.nav.length===9&&dimensions.nav.every(n=>!n.clipped&&n.right<=dimensions.viewport),'clipped navigation at '+width+': '+JSON.stringify(dimensions));
      check(await tab.locator('.ch-card').count()===18,'every chapter uses the home card design');
      check(await tab.locator('.chapter-volume').count()===4,'chapters grouped in syllabus order');
      check(await tab.locator('.ch-card .chips').count()===18,'each chapter has concept highlights');
      check(await tab.locator('.weights .wrow').count()===8,'exam topic breakdown restored');
      check(await tab.locator('.plan li').count()===4,'revision plan restored');
      check(await tab.locator('#study-progress [data-study-chapter]').count()===3,'original chapter progress visible');
      check(await tab.locator('.nav [aria-current="page"]').innerText()==='Home','home active tab');
      report.push({width,home:'fits',navigation:'all nine direct tabs visible'});
    }
    await tab.setViewportSize({width:390,height:844});await go('index.html');
    await clickNav('fluids-1.html');
    check(await tab.locator('.nav a[href="fluids-1.html"]').getAttribute('aria-current')==='page','direct chapter active state');
    await tab.locator('[data-study-section="pressure"]').click();
    await clickNav('index.html');
    check((await tab.locator('#study-overall').textContent()).startsWith('1 of 173'),'saved progress on home');
    check((await tab.locator('#home-continue').getAttribute('href')).startsWith('fluids-1.html#'),'resume latest chapter');
    check((await tab.locator('[data-study-chapter="fluids1"] [data-study-summary]').textContent()).startsWith('1 of 17'),'featured chapter saved progress');
    await clickNav('chapters.html');
    check(await tab.locator('.ch-card[data-study-chapter]').count()===18,'library uses the same card design with progress');
    await tab.locator('a[href="thermodynamics.html"]').first().click();await tab.waitForURL('**/thermodynamics.html');
    check(await tab.locator('.nav a[href="chapters.html"]').getAttribute('aria-current')==='page','library active for added chapters');
    await clickNav('solids.html');await clickNav('fluids-2.html');
    await clickNav('practice.html');
    check(await tab.locator('#s-shown').textContent()==='867','practice remains intact');
    await clickNav('revise.html');await clickNav('syllabus.html');await clickNav('index.html');
    await tab.locator('a[href="formula-sheet.html"]').click();await tab.waitForURL('**/formula-sheet.html');
    check(!errors.length,errors.join(';'));
    return {report,journey:'direct tabs, saved progress, full chapter library, practice, revision and syllabus passed',errors};
  }finally{await context.close();}
}
