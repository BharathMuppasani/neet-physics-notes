"""Validate the deepening layer without writing any site files.

Usage: python3 scripts/check_deep.py [chapter-key ...]
Checks field names and types, required keys, MCQ shape, balanced HTML tags and
balanced MathJax delimiters. Prints a per-chapter summary. Exit code 1 on error.
"""
import copy, html.parser, os, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
only = set(sys.argv[1:])
if only:  # import only the named chapter modules, so another chapter mid-edit cannot break this check
    os.environ['DEEP_ONLY'] = ','.join(sorted(only))
from content.physics_lessons import CHAPTERS
from content import deep as deep_layer
errors = []
TYPES = {'numerical', 'concept', 'ar', 'statement', 'multi', 'match', 'graph'}
DEEP_FIELDS = {'level', 'notes', 'formulas', 'figure', 'traps', 'exam', 'tip', 'examples', 'practice'}
BASE_FIELDS = ['chapter', 'after', 'id', 'title', 'intro', 'reasoning', 'formula', 'symbols', 'trap',
               'example', 'solution', 'question', 'options', 'answer', 'explanation']
VOID = {'br', 'hr', 'img', 'input', 'meta', 'link', 'circle', 'line', 'path', 'rect', 'polygon',
        'polyline', 'ellipse', 'stop', 'use'}


class Balance(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.bad = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.bad.append(f'unexpected </{tag}> (open: {self.stack[-3:]})')
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()


def check_text(where, s):
    if not isinstance(s, str) or not s.strip():
        errors.append(f'{where}: empty or non-string text')
        return
    b = Balance()
    b.feed(s)
    b.close()
    if b.bad or b.stack:
        errors.append(f'{where}: unbalanced HTML {b.bad[:2]} unclosed={b.stack}')
    if s.count(r'\(') != s.count(r'\)') or s.count(r'\[') != s.count(r'\]'):
        errors.append(f'{where}: unbalanced MathJax delimiters')
    if '$' in s:
        errors.append(f'{where}: "$" starts inline math in MathJax; write "Rs" or use \\( \\)')
    if 'being written' in s.lower() or 'coming soon' in s.lower():
        errors.append(f'{where}: placeholder text')


def check_deep(sid, d):
    extra = set(d) - DEEP_FIELDS
    if extra:
        errors.append(f'{sid}: unknown deep fields {sorted(extra)}')
    if d.get('level', 'core') not in {'basic', 'core', 'exam'}:
        errors.append(f'{sid}: level must be basic/core/exam')
    for n, item in enumerate(d.get('notes', [])):
        if not (isinstance(item, (tuple, list)) and len(item) == 2):
            errors.append(f'{sid}: notes[{n}] must be (heading, html)')
            continue
        check_text(f'{sid} notes[{n}] heading', item[0])
        check_text(f'{sid} notes[{n}] body', item[1])
    for n, f in enumerate(d.get('formulas', [])):
        for k in ('title', 'formula', 'symbols'):
            if k not in f:
                errors.append(f'{sid}: formulas[{n}] missing {k}')
            else:
                check_text(f'{sid} formulas[{n}].{k}', f[k])
    if 'figure' in d:
        f = d['figure']
        if 'svg' not in f or 'caption' not in f or not f['svg'].lstrip().startswith('<svg'):
            errors.append(f'{sid}: figure needs svg (starting <svg) and caption')
        else:
            check_text(f'{sid} figure.svg', f['svg'])
            check_text(f'{sid} figure.caption', f['caption'])
    for n, t in enumerate(d.get('traps', [])):
        check_text(f'{sid} traps[{n}]', t)
    for k in ('exam', 'tip'):
        if k in d:
            check_text(f'{sid} {k}', d[k])
    for n, e in enumerate(d.get('examples', [])):
        for k in ('q', 'steps', 'answer'):
            if k not in e:
                errors.append(f'{sid}: examples[{n}] missing {k}')
        check_text(f'{sid} examples[{n}].q', e.get('q', ''))
        check_text(f'{sid} examples[{n}].answer', e.get('answer', ''))
        if not isinstance(e.get('steps'), list) or not e.get('steps'):
            errors.append(f'{sid}: examples[{n}].steps must be a non-empty list')
        for m, st in enumerate(e.get('steps') or []):
            check_text(f'{sid} examples[{n}].steps[{m}]', st)
    for n, p in enumerate(d.get('practice', [])):
        where = f'{sid} practice[{n}]'
        opts = p.get('options')
        opts = opts.split('|') if isinstance(opts, str) else opts
        if not isinstance(opts, list) or len(opts) != 4:
            errors.append(f'{where}: needs exactly 4 options')
        elif len(set(o.strip() for o in opts)) != 4:
            errors.append(f'{where}: duplicate options')
        else:
            for m, o in enumerate(opts):
                check_text(f'{where} option {m}', o)
        if not isinstance(p.get('answer'), int) or not 0 <= p['answer'] < 4:
            errors.append(f'{where}: answer must be an int 0–3')
        if p.get('type', 'numerical') not in TYPES:
            errors.append(f'{where}: type must be one of {sorted(TYPES)}')
        check_text(f'{where}.q', p.get('q', ''))
        check_text(f'{where}.explanation', p.get('explanation', ''))
        extra = set(p) - {'q', 'options', 'answer', 'explanation', 'type'}
        if extra:
            errors.append(f'{where}: unknown fields {sorted(extra)}')


chapter_keys = {c['key'] for c in CHAPTERS}
for s in deep_layer.NEW_SECTIONS:
    sid = s.get('id', '?')
    if only and s.get('chapter') not in only:
        continue
    for k in BASE_FIELDS:
        if k not in s:
            errors.append(f'new section {sid}: missing {k}')
    if s.get('chapter') not in chapter_keys:
        errors.append(f'new section {sid}: unknown chapter {s.get("chapter")}')
    elif not sid.startswith(s['chapter'] + '-'):
        errors.append(f'new section {sid}: id must start with "{s["chapter"]}-"')
    for k in BASE_FIELDS[3:13]:
        if k in s and k != 'options':
            check_text(f'{sid}.{k}', s[k])
    opts = s.get('options', '')
    opts = opts.split('|') if isinstance(opts, str) else opts
    if len(opts) != 4 or not isinstance(s.get('answer'), int) or not 0 <= s['answer'] < 4:
        errors.append(f'new section {sid}: options must be 4 and answer 0–3')
    check_text(f'{sid}.explanation', s.get('explanation', ''))
    extra = set(s) - set(BASE_FIELDS) - {'deep'}
    if extra:
        errors.append(f'new section {sid}: unknown fields {sorted(extra)}')

try:
    chapters = deep_layer.apply(copy.deepcopy(CHAPTERS))
except AssertionError as e:
    errors.append(f'apply failed: {e}')
    chapters = CHAPTERS

for c in chapters:
    if only and c['key'] not in only:
        continue
    n_notes = n_ex = n_pr = n_f = 0
    for s in c['sections']:
        d = s.get('deep') or {}
        check_deep(s['id'], d)
        n_notes += len(d.get('notes', []))
        n_ex += len(d.get('examples', []))
        n_pr += len(d.get('practice', []))
        n_f += len(d.get('formulas', []))
    thin = [s['id'] for s in c['sections'] if not (s.get('deep') or {}).get('examples')]
    print(f"{c['key']:20s} sections={len(c['sections']):2d} notes={n_notes:3d} formulas+={n_f:3d} examples+={n_ex:3d} practice+={n_pr:3d}"
          + (f"  [no extra examples: {', '.join(thin)}]" if thin else ''))

if errors:
    print(f'\n{len(errors)} problem(s):')
    for e in errors:
        print(' -', e)
    sys.exit(1)
print('\nDeep layer OK.')
