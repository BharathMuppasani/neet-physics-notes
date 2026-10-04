/* Playwright smoke test. Start site on localhost:8766, then call this function with a Playwright page. */
async (page) => {
  const base = 'http://127.0.0.1:8766/';
  const context = await page.context().browser().newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce' });
  const tab = await context.newPage();
  tab.setDefaultTimeout(6000);
  const errors = [], report = [];
  tab.on('pageerror', e => errors.push(e.message));
  const check = (condition, message) => { if (!condition) throw new Error(message); };
  const go = async file => {
    await tab.goto(base + file);
    await tab.waitForFunction(() => document.readyState === 'complete');
    await tab.evaluate(async () => { if (MathJax.startup?.promise) await MathJax.startup.promise; });
  };
  const number = async selector => parseFloat(await tab.locator(selector).textContent());
  try {
    // Every chapter quiz can show/hide its solution independently, even after answering.
    for (const file of ['solids.html', 'fluids-1.html', 'fluids-2.html']) {
      await go(file);
      const result = await tab.evaluate(() => {
        const failures = [], cards = [...document.querySelectorAll('.qcard')];
        for (const card of cards) {
          const button = card.querySelector('[data-act=show]'), solution = card.querySelector('.sol');
          button.click();
          if (solution.hidden || getComputedStyle(solution).display === 'none' || button.getAttribute('aria-expanded') !== 'true') failures.push(card.id + ': show');
          button.click();
          if (!solution.hidden || getComputedStyle(solution).display !== 'none' || button.getAttribute('aria-expanded') !== 'false') failures.push(card.id + ': hide');
        }
        return { cards: cards.length, failures, models: document.querySelectorAll('.sim canvas').length, mathErrors: document.querySelectorAll('mjx-merror').length };
      });
      check(!result.failures.length && !result.mathErrors, file + ': ' + JSON.stringify(result));
      const example = tab.locator('.eg details').first();
      await example.locator('summary').click();
      await tab.waitForFunction(() => document.querySelector('.eg details summary').textContent === 'Hide solution');
      check(await example.locator('summary').textContent() === 'Hide solution', file + ': example open label');
      await example.locator('summary').click();
      await tab.waitForFunction(() => document.querySelector('.eg details summary').textContent === 'Show solution');
      check(await example.locator('summary').textContent() === 'Show solution', file + ': example close label');
      report.push({ file, ...result });
    }
    await go('fluids-1.html');
    for (const id of ['pascal-law','pressure-depth','connected-vessels']) {
      check(await tab.locator('.toc a[data-id="' + id + '"]').count() === 1, id + ': missing lesson in index');
    }
    // Known worked examples and limiting cases verify the model calculations.
    check(await number('#sim-connected-vessels [data-r=height]') === 5, 'connected-cylinder final depth');
    check(await number('#sim-connected-vessels [data-r=work]') === 20000, 'connected-cylinder gravity work');
    await tab.locator('#sim-connected-vessels [data-v=after]').click();
    await tab.locator('#cv-A2').evaluate(e => { e.value = '4'; e.dispatchEvent(new Event('input', {bubbles:true})); });
    check(Math.abs(await number('#sim-connected-vessels [data-r=height]') - 4.667) < .001, 'unequal-area final depth');
    check(await number('#sim-lift [data-r=dP]') === 780, 'wing pressure');
    check(await number('#sim-lift [data-r=L]') === 15600, 'wing force');
    await tab.locator('#li-vt').evaluate(e => { e.value='60'; e.dispatchEvent(new Event('input')); });
    check(await number('#sim-lift [data-r=L]') === 0, 'equal-speed zero lift');
    await tab.locator('#sim-lift [data-v=ball]').click();
    check((await tab.locator('#sim-lift [data-r=force]').textContent()).startsWith('upward'), 'positive Magnus spin');
    await tab.locator('#li-spin').evaluate(e => { e.value='-0.5'; e.dispatchEvent(new Event('input')); });
    check((await tab.locator('#sim-lift [data-r=force]').textContent()).startsWith('downward'), 'negative Magnus spin');
    await tab.locator('#sim-accel [data-v=v]').click();
    await tab.locator('#ac-a').evaluate(e => { e.value='-9.8'; e.dispatchEvent(new Event('input')); });
    check((await tab.locator('#sim-accel [data-r=pb]').textContent()).startsWith('0'), 'free-fall pressure gradient');
    await tab.locator('[data-study-section=pressure-depth]').click();
    check(await tab.locator('[data-study-section=pressure-depth]').getAttribute('aria-pressed') === 'true', 'mark studied');
    await tab.reload();
    check(await tab.locator('[data-study-section=pressure-depth]').getAttribute('aria-pressed') === 'true', 'study survives reload');
    await go('index.html');
    check((await tab.locator('#study-overall').textContent()).startsWith('1 of 42'), 'home study progress');
    await go('practice.html?chapter=fluids1');
    const expected = await tab.evaluate(() => window.QBANK.filter(q => Site.TOPICS[q.topic]?.page === 'fluids-1.html').length);
    check(await number('#s-shown') === expected, 'chapter filter count');
    const q = await tab.evaluate(() => Quiz.byId('t05-04'));
    const card = tab.locator('#q-t05-04');
    await card.locator('.opt').nth((q.ans + 1) % 4).click();
    check(await number('#s-wrong') === 1, 'filtered wrong score');
    await card.locator('[data-act=show]').click();
    check(!await card.locator('.sol').isVisible(), 'hide answered solution');
    await card.locator('[data-act=show]').click();
    check(await card.locator('.sol').isVisible(), 'show answered solution');
    await card.locator('[data-act=retry]').click();
    check(await number('#s-done') === 0 && await card.locator('.opt').first().isEnabled(), 'retry clears only this answer');
    await card.locator('.opt').nth(q.ans).click();
    await tab.reload();
    check(await number('#s-right') === 1 && await number('#s-done') === 1, 'answer survives reload');
    await tab.locator('#f-chapter').selectOption('solids');
    check(await number('#s-done') === 0 && await number('#s-right') === 0, 'scores follow selected chapter');
    await go('index.html');
    check(await number('#t-done') === 1 && await number('#t-right') === 1, 'home quiz totals');
    // Storage events synchronise open tabs and reset controls.
    const other = await context.newPage();
    await other.goto(base + 'fluids-1.html');
    await other.evaluate(() => Site.study.toggle('fluids1','pascal-law'));
    await tab.waitForFunction(() => document.querySelector('#study-overall').textContent.startsWith('2 of 42'));
    await other.evaluate(() => Site.store.clear());
    await tab.waitForFunction(() => document.querySelector('#t-done').textContent === '0');
    await other.close();
    await go('solids.html');
    check(await number('#sim-combined-wires [data-r=extension]') === 3, 'series extension');
    await tab.locator('#sim-combined-wires [data-v=parallel]').click();
    check(await number('#sim-combined-wires [data-r=extension]') === .667, 'parallel extension');
    // Print preview must not leave interactive solution buttons broken after closing.
    await tab.evaluate(() => dispatchEvent(new Event('beforeprint')));
    await tab.evaluate(() => dispatchEvent(new Event('afterprint')));
    const printCard = tab.locator('.qcard').first();
    check(!await printCard.locator('.sol').isVisible(), 'solution restored after print');
    await printCard.locator('[data-act=show]').click();
    check(await printCard.locator('.sol').isVisible(), 'show solution after print');
    await go('fluids-2.html');
    check(await number('#sim-pipe-flow [data-r=flow]') === .0393, 'Poiseuille flow');
    check(await number('#sim-pipe-flow [data-r=reynolds]') === 25, 'pipe Reynolds number');
    check(await number('#sim-capillary-measurement [data-r=tension]') === .0706, 'capillary measurement');
    check((await tab.locator('#sim-capillary-measurement [data-r=error]').textContent()).startsWith('±5.0%'), 'measurement error');
    await go('fluids-1.html');
    await tab.evaluate(() => Site.CHAPTERS.find(c => c.key==='fluids1').sections.forEach(id => { if(!Site.study.read()['fluids1:'+id]) Site.study.toggle('fluids1',id); }));
    check((await tab.locator('[data-continue-study]').getAttribute('href')) === 'practice.html?chapter=fluids1', 'completed chapter continuation');
    await go('practice.html#printq');
    check(await tab.locator('.answer-key .ak').count() === 157 && await tab.locator('.qcard').count() === 157, 'questions-only print count');
    // Invalid saved JSON must not break the chapter, and normal controls remain usable.
    await go('index.html');
    await tab.evaluate(() => {localStorage.setItem(Site.store.key,'null');localStorage.setItem(Site.study.key,'[]');});
    await go('fluids-1.html');
    check((await tab.locator('[data-study-summary]').textContent()).startsWith('0 of 17'), 'corrupt study state recovery');
    await tab.locator('[data-study-section=pressure]').click();
    check(await tab.locator('[data-study-section=pressure]').getAttribute('aria-pressed') === 'true', 'toggle after corrupt state');
    for (const width of [320,390,768]) {
      await tab.setViewportSize({width,height:844});
      for (const file of ['index.html','solids.html','fluids-1.html','fluids-2.html','practice.html','revise.html']) {
        await go(file);
        const geometry=await tab.evaluate(()=>({viewport:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth,mathErrors:document.querySelectorAll('mjx-merror').length}));
        check(geometry.scroll <= geometry.viewport + 1, file + ' overflow at ' + width + ': '+JSON.stringify(geometry));
        check(!geometry.mathErrors, file + ': malformed maths at '+width);
      }
    }
    report.push({progress:'reload, cross-page, cross-tab, completion and corrupt state passed',quizzes:'all chapter toggles, retries, filters and print recovery passed',models:'worked examples and limiting cases passed',layouts:'all six pages at 320, 390 and 768 px passed'});
    check(!errors.length, 'page errors: '+errors.join('; '));
    return {report,errors};
  } finally {await context.close();}
}
