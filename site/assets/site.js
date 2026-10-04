/* =====================================================================
   NEET Physics Notes — shared engine
   - top navigation + "On this page" index
   - MathJax (SVG output; config must exist before MathJax loads)
   - Quiz engine over window.QBANK
   - Sim helpers for canvas simulations
   ===================================================================== */

window.MathJax = {
  tex: { inlineMath: [['\\(', '\\)'], ['$', '$']], displayMath: [['\\[', '\\]']] },
  svg: { fontCache: 'global' },
  options: { skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'canvas'] },
  startup: {
    ready() {
      MathJax.startup.defaultReady();
      MathJax.startup.promise.then(() => Site._flushTypeset());
    }
  }
};

window.QBANK = window.QBANK || [];

const Site = {
  PAGES: [
    { href: 'index.html', key: 'home', label: 'Home' },
    { href: 'solids.html', key: 'solids', label: 'Solids' },
    { href: 'fluids-1.html', key: 'fluids1', label: 'Fluids I' },
    { href: 'fluids-2.html', key: 'fluids2', label: 'Fluids II' },
    { href: 'practice.html', key: 'practice', label: 'Practice' },
    { href: 'revise.html', key: 'revise', label: 'Revise' },
  ],

  CHAPTERS: [
    { key: 'solids', page: 'solids.html', label: 'Solids', sections: ['elasticity', 'stress', 'curve', 'youngs', 'wire-combinations', 'shear', 'bulk', 'poisson', 'energy', 'thermal', 'applications', 'problem-types', 'checklist'] },
    { key: 'fluids1', page: 'fluids-1.html', label: 'Fluids I', sections: ['intro', 'pressure', 'pascal-law', 'pressure-depth', 'connected-vessels', 'atmospheric', 'pascal', 'buoyancy', 'flow', 'continuity', 'bernoulli', 'torricelli', 'venturi', 'lift', 'accelerating-fluids', 'problem-types', 'checklist'] },
    { key: 'fluids2', page: 'fluids-2.html', label: 'Fluids II', sections: ['viscosity', 'pipe-flow', 'stokes', 'reynolds', 'surface-tension', 'surface-energy', 'contact-angle', 'drops-bubbles', 'capillarity', 'capillary-experiment', 'problem-types', 'checklist'] },
  ],

  /* topic id → where it is taught. Question objects use these ids in `topic`. */
  TOPICS: {
    // Mechanical properties of solids — solids.html
    'elasticity':   { label: 'Elasticity basics', page: 'solids.html' },
    'stress':       { label: 'Stress & strain', page: 'solids.html' },
    'curve':        { label: 'Stress–strain curve', page: 'solids.html' },
    'youngs':       { label: "Young's modulus", page: 'solids.html' },
    'wire-combinations': { label: 'Combined wires & own weight', page: 'solids.html' },
    'shear':        { label: 'Shear modulus', page: 'solids.html' },
    'bulk':         { label: 'Bulk modulus', page: 'solids.html' },
    'poisson':      { label: "Poisson's ratio", page: 'solids.html' },
    'energy':       { label: 'Elastic energy', page: 'solids.html' },
    'thermal':      { label: 'Thermal stress', page: 'solids.html' },
    'applications': { label: 'Applications of elasticity', page: 'solids.html' },
    // Fluids I — fluids-1.html
    'pressure':     { label: 'Pressure & depth', page: 'fluids-1.html' },
    'pascal-law':   { label: "Pascal's law · equal pressure", page: 'fluids-1.html' },
    'pressure-depth': { label: 'Variation of pressure with depth', page: 'fluids-1.html' },
    'connected-vessels': { label: 'Connected vessels & energy', page: 'fluids-1.html' },
    'atmospheric':  { label: 'Atmospheric pressure & manometers', page: 'fluids-1.html' },
    'pascal':       { label: "Pascal's law & hydraulics", page: 'fluids-1.html' },
    'buoyancy':     { label: 'Buoyancy & floating', page: 'fluids-1.html' },
    'flow':         { label: 'Streamline & turbulent flow', page: 'fluids-1.html' },
    'continuity':   { label: 'Equation of continuity', page: 'fluids-1.html' },
    'bernoulli':    { label: "Bernoulli's principle", page: 'fluids-1.html' },
    'torricelli':   { label: 'Speed of efflux (Torricelli)', page: 'fluids-1.html' },
    'lift':         { label: 'Dynamic lift & Magnus effect', page: 'fluids-1.html' },
    'accelerating-fluids': { label: 'Accelerating containers', page: 'fluids-1.html' },
    // Fluids II — fluids-2.html
    'viscosity':    { label: 'Viscosity', page: 'fluids-2.html' },
    'pipe-flow':    { label: 'Viscous pipe flow', page: 'fluids-2.html' },
    'stokes':       { label: "Stokes' law & terminal velocity", page: 'fluids-2.html' },
    'reynolds':     { label: 'Reynolds number', page: 'fluids-2.html' },
    'surface-tension': { label: 'Surface tension', page: 'fluids-2.html' },
    'surface-energy':  { label: 'Surface energy', page: 'fluids-2.html' },
    'contact-angle':   { label: 'Angle of contact', page: 'fluids-2.html' },
    'drops-bubbles':   { label: 'Drops & bubbles (excess pressure)', page: 'fluids-2.html' },
    'capillarity':     { label: 'Capillary rise', page: 'fluids-2.html' },
    'capillary-experiment': { label: 'Capillary-rise experiment', page: 'fluids-2.html' },
  },

  TYPES: {
    numerical:  { label: 'Numerical', cls: 'water' },
    concept:    { label: 'Concept', cls: 'green' },
    ar:         { label: 'Assertion–Reason', cls: 'plum' },
    statement:  { label: 'Statement I / II', cls: 'indigo' },
    multi:      { label: 'Multi-statement', cls: 'indigo' },
    match:      { label: 'Match the columns', cls: 'amber' },
    graph:      { label: 'Graph', cls: 'coral' },
  },

  SOURCES: {
    t05: 'Module Test-05 · 26 Sep',
    t06: 'Module Test-06 · 03 Oct',
    xs:  'Solids practice set',
    xf:  'Fluids practice set',
    xc:  'Chapter completion set',
  },

  /* Print mode: '#print' (solutions shown) or '#printq' (questions only + answer key).
     Also applied automatically when someone prints from the browser. */
  printKind: null,
  enterPrint(kind) {
    if (this.printKind) return;
    this._printSnapshot = {
      details: [...document.querySelectorAll('details')].map(el => ({ el, open: el.open })),
      cards: [...document.querySelectorAll('.qcard')].map(el => ({
        el, cls: el.className, hidden: el.querySelector('.sol').hidden,
        options: [...el.querySelectorAll('.opt')].map(option => option.className),
      })),
    };
    this.printKind = kind || 'full';
    document.documentElement.classList.add('print', 'print-' + this.printKind);
    document.querySelectorAll('details').forEach(d => { d.open = true; });
    document.querySelectorAll('.qcard').forEach(card => Quiz.printCard(card));
  },

  leavePrint() {
    if (['#print', '#printq'].includes(location.hash) || !this.printKind) return;
    document.documentElement.classList.remove('print', 'print-full', 'print-questions');
    this.printKind = null;
    this._printSnapshot?.details.forEach(({ el, open }) => { el.open = open; });
    this._printSnapshot?.cards.forEach(({ el, cls, hidden, options }) => {
      el.className = cls;
      el.querySelector('.sol').hidden = hidden;
      el.querySelectorAll('.opt').forEach((option, i) => { option.className = options[i]; });
    });
    this._printSnapshot = null;
    this.refreshProgress();
  },

  init() {
    const h = location.hash.slice(1);
    if (h === 'print' || h === 'printq') this.enterPrint(h === 'print' ? 'full' : 'questions');
    window.addEventListener('beforeprint', () => this.enterPrint('full'));
    window.addEventListener('afterprint', () => this.leavePrint());
    this.buildNav();
    this.buildToc();
    document.querySelectorAll('.eg details').forEach(details => {
      const summary = details.querySelector('summary');
      if (!summary || !/^Show (solution|answer)$/.test(summary.textContent.trim())) return;
      const noun = summary.textContent.trim().split(' ')[1];
      details.addEventListener('toggle', () => {
        summary.textContent = `${details.open ? 'Hide' : 'Show'} ${noun}`;
      });
    });
    document.querySelectorAll('.quiz[data-topic], .quiz[data-ids]').forEach(el => Quiz.autoMount(el));
    this.initProgress();
    this.typeset();
  },

  buildNav() {
    const page = document.body.dataset.page;
    const bar = document.createElement('header');
    bar.className = 'topbar';
    bar.innerHTML = `
      <div class="topbar-inner">
        <a class="brand" href="index.html" aria-label="NEET Physics Notes home">
          <span class="brand-mark">Φ</span>
          <span class="brand-name">NEET Physics Notes<small>Jr Star · CUT-6 preparation</small></span>
        </a>
        <nav class="nav" aria-label="Chapters">
          ${this.PAGES.map(p => `<a href="${p.href}"${p.key === page ? ' aria-current="page"' : ''}>${p.label}</a>`).join('')}
        </nav>
      </div>`;
    document.body.prepend(bar);
    const cur = bar.querySelector('[aria-current]');
    if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: 'nearest', inline: 'center' });
  },

  buildToc() {
    const toc = document.querySelector('.toc');
    const secs = [...document.querySelectorAll('.content > section[id]')];
    if (!toc || !secs.length) return;
    const items = secs.map(s => {
      const h = s.querySelector('h2');
      const label = s.dataset.toc || (h ? h.textContent : s.id);
      const num = s.dataset.num || '';
      return `<li><a href="#${s.id}" data-id="${s.id}"><span class="n">${num}</span><span>${label}</span></a></li>`;
    }).join('');
    toc.innerHTML = `<details ${window.innerWidth >= 1100 ? 'open' : ''}><summary>On this page</summary><ol>${items}</ol></details>`;
    const links = new Map([...toc.querySelectorAll('a')].map(a => [a.dataset.id, a]));
    toc.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      if (window.innerWidth < 1100) toc.querySelector('details').open = false;
    }));
    if (!('IntersectionObserver' in window)) return;
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          links.forEach(a => a.classList.remove('active'));
          const a = links.get(e.target.id);
          if (a) a.classList.add('active');
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    secs.forEach(s => io.observe(s));
  },

  /* MathJax typesetting, queued until MathJax is ready */
  _pending: [],
  typeset(el) {
    const target = el || document.body;
    if (window.MathJax && MathJax.typesetPromise && MathJax.startup && MathJax.startup.document) {
      MathJax.typesetPromise([target]).catch(() => {});
    } else {
      this._pending.push(target);
    }
  },
  _flushTypeset() {
    const list = this._pending.splice(0);
    if (list.length) MathJax.typesetPromise(list).catch(() => {});
  },

  initProgress() {
    const chapter = this.CHAPTERS.find(c => c.key === document.body.dataset.page);
    if (chapter) {
      const panel = document.createElement('div');
      panel.className = 'chapter-progress';
      panel.innerHTML = `<strong>Your progress in ${chapter.label}</strong><p data-study-summary></p><progress data-study-meter max="${chapter.sections.length}" value="0" aria-label="Sections studied"></progress><p class="small" data-practice-summary></p><a data-continue-study></a><p class="small muted">Mark a section studied when you understand it. Reading progress and quiz answers are saved in this browser.</p>`;
      document.querySelector('.hero')?.after(panel);
      for (const id of chapter.sections) {
        const section = document.getElementById(id);
        if (!section) continue;
        const control = document.createElement('div');
        control.className = 'section-study';
        const button = document.createElement('button');
        button.className = 'btn';
        button.type = 'button';
        button.dataset.studySection = id;
        button.addEventListener('click', () => this.study.toggle(chapter.key, id));
        control.append(button);
        section.append(control);
      }
    }
    const home = document.getElementById('study-progress');
    if (home) {
      home.innerHTML = this.CHAPTERS.map(c => `<article class="card study-card" data-study-chapter="${c.key}"><h3><a href="${c.page}">${c.label}</a></h3><p data-study-summary></p><progress data-study-meter max="${c.sections.length}" value="0" aria-label="${c.label} sections studied"></progress><p class="small" data-practice-summary></p><a data-continue-study></a></article>`).join('');
    }
    this.refreshProgress();
    document.addEventListener('progress:change', () => this.refreshProgress());
    window.addEventListener('pageshow', () => this.refreshProgress());
    window.addEventListener('storage', e => {
      if (e.key === null || [this.store.key, this.study.key].includes(e.key)) {
        this.refreshProgress();
        document.dispatchEvent(new CustomEvent('progress:change'));
      }
    });
  },

  questionStats(questions = window.QBANK) {
    const attempts = this.store.read();
    const answered = questions.filter(q => Number.isInteger(attempts[q.id]));
    const correct = answered.filter(q => q.ans === attempts[q.id]).length;
    return { total: questions.length, answered: answered.length, correct, wrong: answered.length - correct };
  },

  refreshProgress() {
    if (!this.printKind) document.querySelectorAll('.qcard').forEach(card => card._sync?.());
    const studied = this.study.read();
    const stats = this.questionStats();
    for (const [id, value] of Object.entries({ 't-total': stats.total, 't-done': stats.answered, 't-right': stats.correct, 't-flag': window.QBANK.filter(q => q.flagged).length })) {
      const el = document.getElementById(id);
      if (el) el.textContent = value;
    }
    let totalStudied = 0;
    for (const chapter of this.CHAPTERS) {
      const completed = chapter.sections.filter(id => studied[`${chapter.key}:${id}`]);
      totalStudied += completed.length;
      const current = chapter.key === document.body.dataset.page;
      const panel = current ? document.querySelector('.chapter-progress') : document.querySelector(`[data-study-chapter="${chapter.key}"]`);
      const questions = window.QBANK.filter(q => this.TOPICS[q.topic]?.page === chapter.page);
      const quiz = this.questionStats(questions);
      if (panel) {
        panel.querySelector('[data-study-summary]').textContent = `${completed.length} of ${chapter.sections.length} sections studied`;
        panel.querySelector('[data-study-meter]').value = completed.length;
        panel.querySelector('[data-practice-summary]').textContent = `${quiz.answered} of ${quiz.total} questions attempted · ${quiz.correct} correct${quiz.answered ? ` · ${Math.round(100 * quiz.correct / quiz.answered)}% accuracy` : ''}`;
        const next = chapter.sections.find(id => !completed.includes(id));
        const link = panel.querySelector('[data-continue-study]');
        link.href = next ? `${current ? '' : chapter.page}#${next}` : `practice.html?chapter=${chapter.key}`;
        link.textContent = next ? (completed.length ? 'Continue with the next section' : 'Start this chapter') : 'All sections studied · practise this chapter';
      }
      if (current) {
        for (const id of chapter.sections) {
          const done = completed.includes(id);
          const button = document.querySelector(`[data-study-section="${id}"]`);
          if (button) {
            button.textContent = done ? 'Studied ✓ · mark unread' : 'Mark this section studied';
            button.setAttribute('aria-pressed', String(done));
          }
          const tocLink = document.querySelector(`.toc [data-id="${id}"]`);
          if (tocLink) {
            tocLink.classList.toggle('studied', done);
            tocLink.setAttribute('aria-label', `${this.sectionLabel(id)}${done ? ', studied' : ', not yet studied'}`);
          }
        }
      }
    }
    const summary = document.getElementById('study-overall');
    if (summary) summary.textContent = `${totalStudied} of ${this.CHAPTERS.reduce((n, c) => n + c.sections.length, 0)} sections studied across Solids and Fluids.`;
  },

  sectionLabel(id) {
    return document.getElementById(id)?.querySelector('h2')?.textContent || id;
  },

  study: {
    key: 'phy-notes-study-v1',
    _fallback: null,
    read() {
      if (this._fallback) return { ...this._fallback };
      try {
        const raw = JSON.parse(localStorage.getItem(this.key) || '{}');
        if (!raw || Array.isArray(raw) || typeof raw !== 'object') return {};
        const allowed = new Set(Site.CHAPTERS.flatMap(c => c.sections.map(id => `${c.key}:${id}`)));
        return Object.fromEntries(Object.entries(raw).filter(([key, value]) => allowed.has(key) && value === true));
      } catch { return {}; }
    },
    toggle(chapter, section) {
      if (!Site.CHAPTERS.find(c => c.key === chapter)?.sections.includes(section)) return;
      const data = this.read(), key = `${chapter}:${section}`;
      if (data[key]) delete data[key]; else data[key] = true;
      try { localStorage.setItem(this.key, JSON.stringify(data)); this._fallback = null; }
      catch { this._fallback = data; Site.showStorageNotice(); }
      document.dispatchEvent(new CustomEvent('progress:change'));
    },
  },

  showStorageNotice() {
    if (document.getElementById('storage-notice')) return;
    const notice = document.createElement('p');
    notice.id = 'storage-notice';
    notice.className = 'callout trap';
    notice.setAttribute('role', 'status');
    notice.textContent = 'This browser is blocking saved progress. Your changes may be lost when you leave this page.';
    document.querySelector('main')?.prepend(notice);
  },

  store: {
    key: 'phy-notes-attempts-v1',
    _fallback: null,
    read() {
      if (this._fallback) return { ...this._fallback };
      try {
        const raw = JSON.parse(localStorage.getItem(this.key) || '{}');
        if (!raw || Array.isArray(raw) || typeof raw !== 'object') return {};
        return Object.fromEntries(Object.entries(raw).filter(([, value]) => Number.isInteger(value) && value >= 0 && value < 4));
      } catch { return {}; }
    },
    write(obj) {
      try { localStorage.setItem(this.key, JSON.stringify(obj)); this._fallback = null; }
      catch { this._fallback = { ...obj }; Site.showStorageNotice(); }
      document.dispatchEvent(new CustomEvent('progress:change'));
    },
    set(id, choice) {
      if (!Number.isInteger(choice) || choice < 0 || choice >= 4) return;
      const o = this.read(); o[id] = choice; this.write(o);
    },
    remove(id) { const o = this.read(); delete o[id]; this.write(o); },
    clear() { this.write({}); },
  },
};

/* =====================================================================
   Quiz engine
   Question object:
   { id, src: 't05'|'t06'|'xs'|'xf'|'xc', qno, topic, type, flagged?,
     q: html, fig?: svg html, opts: [html x4], ans: 0-based index,
     sol: html, trap?: html, key?: html }
   ===================================================================== */
const Quiz = {
  byId(id) { return window.QBANK.find(q => q.id === id); },

  autoMount(el) {
    let list;
    if (el.dataset.ids) {
      list = el.dataset.ids.split(',').map(s => this.byId(s.trim())).filter(Boolean);
    } else {
      const topics = el.dataset.topic.split(',').map(s => s.trim());
      list = window.QBANK.filter(q => topics.includes(q.topic));
    }
    const limit = +el.dataset.limit || 0;
    const total = list.length;
    if (limit) list = list.slice(0, limit);
    if (!list.length) { el.hidden = true; return; }
    const wrap = document.createElement('div');
    wrap.className = 'quiz-list';
    el.appendChild(wrap);
    this.mount(wrap, list);
    if (el.dataset.topic && total > list.length) {
      const more = document.createElement('p');
      more.className = 'small';
      more.innerHTML = `<a href="practice.html#${el.dataset.topic.split(',')[0].trim()}">See all ${total} questions on this topic in Practice →</a>`;
      el.appendChild(more);
    }
  },

  mount(container, list) {
    container.innerHTML = '';
    const frag = document.createDocumentFragment();
    list.forEach(q => frag.appendChild(this.card(q)));
    container.appendChild(frag);
    Site.typeset(container);
  },

  srcLabel(q) {
    if (q.src === 't05') return `Test-05 · Q${q.qno}`;
    if (q.src === 't06') return `Test-06 · Q${q.qno}`;
    if (q.src === 'xs') return `Solids set · ${q.qno}`;
    if (q.src === 'xf') return `Fluids set · ${q.qno}`;
    if (q.src === 'xc') return `Completion set · ${q.qno}`;
    return q.id;
  },

  card(q) {
    const el = document.createElement('article');
    el.className = 'qcard';
    el.id = 'q-' + q.id;
    const t = Site.TYPES[q.type] || { label: q.type, cls: '' };
    const topic = Site.TOPICS[q.topic];
    const short = q.opts.every(o => o.replace(/<[^>]+>/g, '').length < 34);
    el.innerHTML = `
      <div class="qmeta">
        <span class="src">${this.srcLabel(q)}</span>
        <span class="chip ${t.cls}">${t.label}</span>
        ${topic ? `<span class="chip">${topic.label}</span>` : ''}
        ${q.flagged ? `<span class="chip coral" title="This question has a ✗ mark on the paper photo">✗ marked on your paper</span>` : ''}
      </div>
      <div class="qtext">${q.q}${q.fig ? `<div class="qfig">${q.fig}</div>` : ''}</div>
      ${topic ? `<p class="concept small"><a href="${topic.page}#${q.topic}">Review this concept first: ${topic.label} →</a></p>` : ''}
      <div class="opts ${short ? 'short' : ''}">
        ${q.opts.map((o, i) => `<button class="opt" data-i="${i}" type="button"><span class="on">${i + 1})</span><span class="ot">${o}</span></button>`).join('')}
      </div>
      <div class="qactions">
        <button class="btn" type="button" data-act="show" aria-expanded="false" aria-controls="sol-${q.id}">Show solution</button>
        <button class="btn" type="button" data-act="retry" hidden>Try again</button>
        <span class="verdict" aria-live="polite"></span>
      </div>
      <div class="sol" id="sol-${q.id}" hidden>
        <h5>Solution · Answer: option ${q.ans + 1}</h5>
        <div class="stack">${q.sol}</div>
        ${q.trap ? `<div class="callout trap"><span class="label">Exam trap</span><div>${q.trap}</div></div>` : ''}
        ${q.key ? `<div class="callout tip"><span class="label">Remember</span><div>${q.key}</div></div>` : ''}
        ${topic ? `<p class="concept muted">Concept: <a href="${topic.page}#${q.topic}">${topic.label} →</a></p>` : ''}
      </div>`;

    const opts = [...el.querySelectorAll('.opt')];
    const sol = el.querySelector('.sol');
    const verdict = el.querySelector('.verdict');
    const showBtn = el.querySelector('[data-act="show"]');
    const retryBtn = el.querySelector('[data-act="retry"]');

    const reveal = () => {
      if (sol.hidden) { sol.hidden = false; showBtn.textContent = 'Hide solution'; showBtn.setAttribute('aria-expanded', 'true'); Site.typeset(sol); }
    };
    const answer = (i, save) => {
      opts.forEach(b => b.classList.remove('right', 'wrong'));
      el.classList.remove('done-right', 'done-wrong');
      opts.forEach((b, j) => {
        b.disabled = true;
        if (j === q.ans) b.classList.add('right');
        if (j === i && i !== q.ans) b.classList.add('wrong');
      });
      const ok = i === q.ans;
      verdict.textContent = ok ? 'Correct' : `Not quite. The answer is option ${q.ans + 1}.`;
      verdict.className = 'verdict ' + (ok ? 'ok' : 'no');
      el.classList.add(ok ? 'done-right' : 'done-wrong');
      retryBtn.hidden = false;
      reveal();
      if (save) { Site.store.set(q.id, i); document.dispatchEvent(new CustomEvent('quiz:answer', { detail: { id: q.id, ok } })); }
    };
    opts.forEach((b, i) => b.addEventListener('click', () => answer(i, true)));
    showBtn.addEventListener('click', () => {
      if (sol.hidden) reveal(); else { sol.hidden = true; showBtn.textContent = 'Show solution'; showBtn.setAttribute('aria-expanded', 'false'); }
    });
    el._q = q;
    if (Site.printKind) { this.printCard(el); return el; }
    let previous;
    el._sync = () => {
      const choice = Site.store.read()[q.id];
      if (choice === previous) return;
      previous = choice;
      if (Number.isInteger(choice)) answer(choice, false);
      else {
        opts.forEach(b => { b.disabled = false; b.classList.remove('right', 'wrong'); });
        el.classList.remove('done-right', 'done-wrong');
        sol.hidden = true; showBtn.textContent = 'Show solution';
        showBtn.setAttribute('aria-expanded', 'false');
        retryBtn.hidden = true; verdict.textContent = '';
      }
    };
    retryBtn.addEventListener('click', () => {
      Site.store.remove(q.id);
      document.dispatchEvent(new CustomEvent('quiz:answer', { detail: { id: q.id, retry: true } }));
      opts[0].focus();
    });
    el._sync();
    return el;
  },

  /* static print rendering: full = correct option + solution; questions = clean card */
  printCard(el) {
    const q = el._q;
    if (!q) return;
    const opts = el.querySelectorAll('.opt');
    opts.forEach(b => b.classList.remove('wrong', 'right'));
    el.classList.remove('done-right', 'done-wrong');
    const sol = el.querySelector('.sol');
    if (Site.printKind === 'full') {
      if (opts[q.ans]) opts[q.ans].classList.add('right');
      if (sol) sol.hidden = false;
    } else if (sol) sol.hidden = true;
  },

  /* compact answer key table for the questions-only print */
  answerKey(list) {
    const cells = list.map(q => `<span class="ak"><b>${this.srcLabel(q)}</b> ${q.ans + 1}</span>`).join('');
    return `<section class="answer-key"><h2>Answer key</h2><div class="ak-grid">${cells}</div></section>`;
  },
};

/* =====================================================================
   Sim helpers — canvas stages, control wiring, drawing utilities
   ===================================================================== */
const Sim = {
  reduced: window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches,

  /* palette read from CSS tokens so canvases match the page */
  get C() {
    if (this._c) return this._c;
    const cs = getComputedStyle(document.documentElement);
    const g = n => cs.getPropertyValue(n).trim();
    const accent = getComputedStyle(document.body).getPropertyValue('--accent').trim();
    this._c = {
      ink: g('--ink'), ink2: g('--ink-2'), muted: g('--muted'), line: g('--line'), line2: g('--line-2'),
      surface: g('--surface'), surface2: g('--surface-2'), bg: g('--bg'),
      teal: g('--teal'), indigo: g('--indigo'), coral: g('--coral'), amber: g('--amber'),
      plum: g('--plum'), green: g('--green'), water: g('--water'),
      tealSoft: g('--teal-soft'), indigoSoft: g('--indigo-soft'), coralSoft: g('--coral-soft'),
      amberSoft: g('--amber-soft'), plumSoft: g('--plum-soft'), greenSoft: g('--green-soft'), waterSoft: g('--water-soft'),
      accent: accent || g('--teal'),
      liquid: 'rgba(58,140,203,0.22)', liquidEdge: 'rgba(58,140,203,0.55)',
      font: getComputedStyle(document.body).fontFamily, mono: g('--f-mono'),
    };
    return this._c;
  },

  /* Create a responsive HiDPI canvas inside `host`.
     opts: { aspect: w/h (default 16/9), minH, maxH, draw(ctx, w, h, t, dt), animate: bool }
     Returns { canvas, ctx, redraw(), get w(), get h(), toLocal(evt) } */
  stage(host, opts = {}) {
    const canvas = document.createElement('canvas');
    host.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    const st = { canvas, ctx, w: 0, h: 0, t: 0, running: false, visible: true };
    const aspect = opts.aspect || 16 / 9;
    const size = () => {
      const w = host.clientWidth || 600;
      let h = w / aspect;
      if (opts.minH) h = Math.max(h, opts.minH);
      if (opts.maxH) h = Math.min(h, opts.maxH);
      const dpr = Math.min(window.devicePixelRatio || 1, 2.5);
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      canvas.style.height = h + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      st.w = w; st.h = h;
      st.redraw();
    };
    st.redraw = () => {
      if (!st.w) return;
      ctx.clearRect(0, 0, st.w, st.h);
      ctx.save();
      opts.draw && opts.draw(ctx, st.w, st.h, st.t, 0);
      ctx.restore();
    };
    st.toLocal = (e) => {
      const r = canvas.getBoundingClientRect();
      const p = e.touches ? e.touches[0] : e;
      return { x: p.clientX - r.left, y: p.clientY - r.top };
    };
    if ('ResizeObserver' in window) new ResizeObserver(size).observe(host);
    else window.addEventListener('resize', size);
    size();

    if (opts.animate && !Sim.reduced) {
      let last = performance.now();
      const loop = (now) => {
        const dt = Math.min(0.05, (now - last) / 1000);
        last = now;
        if (st.visible && !document.hidden) {
          st.t += dt;
          ctx.clearRect(0, 0, st.w, st.h);
          ctx.save();
          opts.draw(ctx, st.w, st.h, st.t, dt);
          ctx.restore();
        }
        requestAnimationFrame(loop);
      };
      requestAnimationFrame(loop);
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(es => es.forEach(e => { st.visible = e.isIntersecting; })).observe(canvas);
      }
    }
    return st;
  },

  /* Wire every input[type=range] and .seg inside `root`.
     Range markup: <input type="range" id="x" data-unit=" m" data-dp="2"> + <output data-for="x">
     Segmented:    <div class="seg" data-k="mode"><button data-v="a" aria-pressed="true">A</button>...</div>
     Calls onChange(values) on every change; values keyed by input id / seg data-k. */
  controls(root, onChange) {
    const vals = {};
    const fmt = (inp) => {
      const dp = inp.dataset.dp !== undefined ? +inp.dataset.dp : 2;
      const v = +inp.value;
      const shown = inp.dataset.map ? Sim.maps[inp.dataset.map](v) : v.toFixed(dp);
      return shown + (inp.dataset.unit || '');
    };
    const ranges = [...root.querySelectorAll('input[type="range"]')];
    const sync = () => {
      ranges.forEach(inp => {
        vals[inp.id] = +inp.value;
        const out = root.querySelector(`output[data-for="${inp.id}"]`);
        if (out) out.textContent = fmt(inp);
      });
      onChange && onChange(vals);
    };
    ranges.forEach(inp => inp.addEventListener('input', sync));
    root.querySelectorAll('.seg[data-k]').forEach(seg => {
      const k = seg.dataset.k;
      const btns = [...seg.querySelectorAll('button')];
      const on = btns.find(b => b.getAttribute('aria-pressed') === 'true') || btns[0];
      btns.forEach(b => b.setAttribute('aria-pressed', b === on ? 'true' : 'false'));
      vals[k] = on.dataset.v;
      btns.forEach(b => b.addEventListener('click', () => {
        btns.forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
        vals[k] = b.dataset.v;
        sync();
      }));
    });
    sync();
    return vals;
  },
  maps: {},

  /* set text of a readout: <div class="readout"><span class="k">..</span><span class="v" data-r="name"></span></div> */
  out(root, name, text) {
    const el = root.querySelector(`[data-r="${name}"]`);
    if (el) el.textContent = text;
  },

  /* number formatting: sci(0.000123) → "1.23 × 10⁻⁴" */
  sci(x, dp = 2) {
    if (x === 0 || !isFinite(x)) return String(x);
    const e = Math.floor(Math.log10(Math.abs(x)));
    if (e >= -2 && e <= 4) return (+x.toFixed(Math.max(0, dp - e))).toString();
    const m = x / Math.pow(10, e);
    const sup = String(e).replace(/-/g, '⁻').replace(/\d/g, d => '⁰¹²³⁴⁵⁶⁷⁸⁹'[d]);
    return `${m.toFixed(dp)} × 10${sup}`;
  },

  /* drawing utilities */
  text(ctx, str, x, y, o = {}) {
    ctx.save();
    ctx.font = `${o.weight || 500} ${o.size || 13}px ${o.mono ? Sim.C.mono : Sim.C.font}`;
    ctx.fillStyle = o.color || Sim.C.ink;
    ctx.textAlign = o.align || 'left';
    ctx.textBaseline = o.base || 'middle';
    if (o.bg) {
      const m = ctx.measureText(str);
      const pad = 4, w = m.width + pad * 2, h = (o.size || 13) + pad * 2;
      let bx = x - pad; if (ctx.textAlign === 'center') bx = x - w / 2; if (ctx.textAlign === 'right') bx = x - w + pad;
      ctx.fillStyle = o.bg;
      Sim.rrect(ctx, bx, y - h / 2, w, h, 5); ctx.fill();
      ctx.fillStyle = o.color || Sim.C.ink;
    }
    ctx.fillText(str, x, y);
    ctx.restore();
  },
  arrow(ctx, x1, y1, x2, y2, o = {}) {
    const color = o.color || Sim.C.ink, lw = o.width || 2, hs = o.head || 8 + lw;
    const a = Math.atan2(y2 - y1, x2 - x1), len = Math.hypot(x2 - x1, y2 - y1);
    if (len < 1) return;
    ctx.save();
    ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = lw; ctx.lineCap = 'round';
    if (o.dash) ctx.setLineDash(o.dash);
    ctx.beginPath(); ctx.moveTo(x1, y1);
    ctx.lineTo(x2 - Math.cos(a) * hs * 0.7, y2 - Math.sin(a) * hs * 0.7); ctx.stroke();
    ctx.setLineDash([]);
    ctx.beginPath(); ctx.moveTo(x2, y2);
    ctx.lineTo(x2 - hs * Math.cos(a - 0.4), y2 - hs * Math.sin(a - 0.4));
    ctx.lineTo(x2 - hs * Math.cos(a + 0.4), y2 - hs * Math.sin(a + 0.4));
    ctx.closePath(); ctx.fill();
    if (o.label) Sim.text(ctx, o.label, x2 + (o.lx || 0), y2 + (o.ly || 0), { color, size: o.size || 12.5, weight: 650, align: o.align || 'center' });
    ctx.restore();
  },
  rrect(ctx, x, y, w, h, r) {
    r = Math.min(r, Math.abs(w) / 2, Math.abs(h) / 2);
    ctx.beginPath();
    ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  },
  line(ctx, pts, o = {}) {
    ctx.save();
    ctx.strokeStyle = o.color || Sim.C.ink; ctx.lineWidth = o.width || 2; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    if (o.dash) ctx.setLineDash(o.dash);
    ctx.beginPath(); pts.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]));
    if (o.close) ctx.closePath();
    if (o.fill) { ctx.fillStyle = o.fill; ctx.fill(); }
    if (o.color !== 'none') ctx.stroke();
    ctx.restore();
  },
  /* Axes in box {x,y,w,h}; returns { X(v), Y(v) } mapping data → px.
     o: {xmin,xmax,ymin,ymax,xlabel,ylabel,xticks:[...],yticks:[...],grid:true} */
  axes(ctx, box, o) {
    const X = v => box.x + (v - o.xmin) / (o.xmax - o.xmin) * box.w;
    const Y = v => box.y + box.h - (v - o.ymin) / (o.ymax - o.ymin) * box.h;
    ctx.save();
    if (o.grid !== false) {
      ctx.strokeStyle = Sim.C.line; ctx.lineWidth = 1;
      (o.xticks || []).forEach(v => { ctx.beginPath(); ctx.moveTo(X(v), box.y); ctx.lineTo(X(v), box.y + box.h); ctx.stroke(); });
      (o.yticks || []).forEach(v => { ctx.beginPath(); ctx.moveTo(box.x, Y(v)); ctx.lineTo(box.x + box.w, Y(v)); ctx.stroke(); });
    }
    ctx.strokeStyle = Sim.C.ink2; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(box.x, box.y - 6); ctx.lineTo(box.x, box.y + box.h); ctx.lineTo(box.x + box.w + 6, box.y + box.h); ctx.stroke();
    (o.xticks || []).forEach(v => Sim.text(ctx, o.xfmt ? o.xfmt(v) : String(v), X(v), box.y + box.h + 12, { size: 11, color: Sim.C.muted, align: 'center', mono: true }));
    (o.yticks || []).forEach(v => Sim.text(ctx, o.yfmt ? o.yfmt(v) : String(v), box.x - 6, Y(v), { size: 11, color: Sim.C.muted, align: 'right', mono: true }));
    if (o.xlabel) Sim.text(ctx, o.xlabel, box.x + box.w, box.y + box.h + 28, { size: 12, color: Sim.C.ink2, align: 'right', weight: 600 });
    if (o.ylabel) Sim.text(ctx, o.ylabel, box.x + 4, box.y - 14, { size: 12, color: Sim.C.ink2, align: 'left', weight: 600 });
    ctx.restore();
    return { X, Y };
  },
};

document.addEventListener('DOMContentLoaded', () => Site.init());
