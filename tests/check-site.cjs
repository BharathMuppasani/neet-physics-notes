/* No dependencies: node tests/check-site.cjs */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { spawnSync } = require('node:child_process');
const root = path.resolve(__dirname, '..');
const site = path.join(root, 'site');
const saved = new Map();
let blocked = false;
const sandbox = {
  window: { matchMedia: () => ({ matches: false }) },
  document: { addEventListener() {}, dispatchEvent() {}, getElementById() { return {}; } },
  localStorage: {
    getItem: key => { if (blocked) throw new Error('blocked'); return saved.get(key) ?? null; },
    setItem: (key, value) => { if (blocked) throw new Error('blocked'); saved.set(key, value); },
  },
  CustomEvent: class {},
};
sandbox.window.window = sandbox.window;
sandbox.matchMedia = sandbox.window.matchMedia;
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(path.join(site, 'assets/catalog.js'), 'utf8'), sandbox);
vm.runInContext(fs.readFileSync(path.join(site, 'assets/site.js'), 'utf8') + '\nglobalThis.engine = Site;', sandbox);
sandbox.QBANK = sandbox.window.QBANK;
for (const file of fs.readdirSync(path.join(site, 'assets')).filter(f => /^q-.*\.js$/.test(f))) {
  vm.runInContext(fs.readFileSync(path.join(site, 'assets', file), 'utf8'), sandbox);
}
const engine = sandbox.engine;
const questions = sandbox.window.QBANK;
assert.equal(questions.length, 317);
assert.equal(engine.CHAPTERS.length, 18);
assert.equal(new Set(questions.map(q => q.id)).size, questions.length, 'question IDs must be unique');
const pages = new Map();
for (const file of fs.readdirSync(site).filter(f => f.endsWith('.html') && !f.startsWith('_') && f !== 'print-cover.html')) {
  const html = fs.readFileSync(path.join(site, file), 'utf8');
  const ids = [...html.matchAll(/\bid="([^"{}$]+)"/g)].map(m => m[1]);
  assert.equal(new Set(ids).size, ids.length, `${file}: duplicate static IDs`);
  assert(!/This section is being written|coming soon/i.test(html), `${file}: unfinished placeholder`);
  pages.set(file, { html, ids: new Set(ids) });
}
for (const chapter of engine.CHAPTERS) {
  const page = pages.get(chapter.page);
  const sections = [...page.html.matchAll(/<section\b[^>]*\bid="([^"]+)"/g)].map(m => m[1]);
  assert.deepEqual([...chapter.sections], sections, `${chapter.key}: registered progress sections must match teaching order`);
  const formulas = [...page.html.matchAll(/<div class="f-title">/g)];
  const definitions = [...page.html.matchAll(/<strong>Symbols and assumptions:<\/strong>/g)];
  assert.equal(formulas.length, definitions.length, `${chapter.key}: every formula card needs symbol definitions`);
  for (const bank of ['q-test05.js','q-test06.js','q-solids.js','q-fluids-extra.js','q-completion.js','q-class11.js']) {
    assert.equal(page.html.split(`src="assets/${bank}"`).length - 1, 1, `${chapter.key}: question bank loaded once`);
  }
}
for (const q of questions) {
  assert.equal(q.opts.length, 4, q.id);
  assert(Number.isInteger(q.ans) && q.ans >= 0 && q.ans < 4, `${q.id}: invalid answer`);
  assert(q.q && q.sol, `${q.id}: question and solution required`);
  assert(engine.SOURCES[q.src], `${q.id}: unknown source`);
  assert(engine.TYPES[q.type], `${q.id}: unknown question type`);
  const topic = engine.TOPICS[q.topic];
  assert(topic && pages.get(topic.page).ids.has(q.topic), `${q.id}: concept link must target an existing lesson`);
}
for (const [file, page] of pages) {
  for (const match of page.html.matchAll(/\s(?:href|src)="([^"]+)"/g)) {
    const url = match[1];
    if (/^(?:https?:|data:|mailto:)/.test(url) || url.includes('${')) continue;
    const [route, hash] = url.split('#');
    const target = route.split('?')[0] || file;
    assert(fs.existsSync(path.join(site, target)), `${file}: missing resource ${url}`);
    if (hash && pages.has(target)) {
      assert(pages.get(target).ids.has(hash) || target === 'practice.html', `${file}: broken anchor ${url}`);
    }
  }
  for (const match of page.html.matchAll(/data-ids="([^"]+)"/g)) {
    for (const id of match[1].split(',')) assert(questions.some(q => q.id === id.trim()), `${file}: missing inline question ${id}`);
  }
}
// Keep existing attempts readable and isolate corrupted or stale progress.
saved.set(engine.store.key, JSON.stringify({ 't05-04': 1, 'xs-01': 1, 'deleted-question': 2, bad: -1, bad2: 4, bad3: null, bad4: '1' }));
let stats = engine.questionStats();
assert.equal(stats.answered, 2);
assert.equal(stats.correct, questions.filter(q => ['t05-04','xs-01'].includes(q.id) && q.ans === 1).length);
assert.equal(Object.keys(engine.store.read()).length, 3);
for (const corrupt of ['null', '[]', '"string"', '{bad json']) {
  saved.set(engine.store.key, corrupt);
  assert.equal(Object.keys(engine.store.read()).length, 0, 'corrupt attempt data');
  saved.set(engine.study.key, corrupt);
  assert.equal(Object.keys(engine.study.read()).length, 0, 'corrupt study data');
}
saved.set(engine.study.key, JSON.stringify({ 'fluids1:pressure': true, 'fluids1:pressure-depth': false, 'fluids1:invented': true }));
assert.equal(Object.keys(engine.study.read()).length, 1);
engine.study.toggle('fluids1', 'pressure-depth');
assert.equal(engine.study.read()['fluids1:pressure-depth'], true);
engine.study.toggle('fluids1', 'pressure-depth');
assert.equal(engine.study.read()['fluids1:pressure-depth'], undefined);
engine.study.toggle('fluids1', 'unknown');
assert.equal(Object.keys(engine.study.read()).length, 1);
engine.store.clear();
engine.store.set('t05-04', 1);
engine.store.remove('t05-04');
assert.equal(engine.store.read()['t05-04'], undefined);
engine.store.set('t05-04', 5);
assert.equal(engine.questionStats().answered, 0);
// Blocked storage still permits quizzes and section toggles for the current session.
blocked = true;
engine.store.set('t05-04', 1);
assert.equal(engine.store.read()['t05-04'], 1);
engine.store.clear();
assert.equal(engine.questionStats().answered, 0);
engine.study.toggle('solids', 'elasticity');
assert.equal(engine.study.read()['solids:elasticity'], true);
engine.study.toggle('solids', 'elasticity');
assert.equal(engine.study.read()['solids:elasticity'], undefined);
for (const file of fs.readdirSync(path.join(site, 'assets')).filter(f => f.endsWith('.js'))) {
  const result = spawnSync(process.execPath, ['--check', path.join(site, 'assets', file)], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
}
console.log(`Passed: ${questions.length} questions; ${engine.CHAPTERS.reduce((n,c) => n+c.sections.length,0)} sections; formula labels, links, syntax, saved-state compatibility and recovery.`);
