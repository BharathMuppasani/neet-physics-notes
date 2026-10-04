# Deepening layer: schema

`content/physics_lessons.py` holds the first teaching pass: each section has two paragraphs, one formula, one trap, one example and one concept question. The deepening layer adds depth without touching that file, so existing section IDs, question IDs (`c11-<section-id>`) and saved progress stay valid.

One file per chapter: `content/deep/<chapter-key>.py` (e.g. `content/deep/linear.py`). It may define:

```python
R = str  # use raw strings r'...' for anything containing MathJax backslashes

DEEP = {
  '<existing-section-id>': dict(
      level='core',              # optional: 'basic' | 'core' | 'exam' (badge on the section)
      notes=[                    # extra teaching blocks rendered after the two intro paragraphs
          ('Derivation: v² = u² + 2as', r'<p>…</p><ol><li>…</li></ol>'),
          ('Why the sign matters', r'<p>…</p>'),
      ],
      formulas=[                 # extra formula cards (symbols are REQUIRED by the tests)
          dict(title='Distance in the nth second', formula=r's_n = u + \tfrac{a}{2}(2n-1)',
               symbols='u initial velocity (m/s), a constant acceleration (m/s²), n the second counted from t = 0.'),
      ],
      figure=dict(svg='<svg viewBox="0 0 320 160" role="img" aria-label="…">…</svg>',
                  caption='What the figure shows.'),
      traps=[r'Extra common mistake…'],          # each becomes an "Exam trap" callout
      exam=r'<ul><li>How NEET phrases it…</li></ul>',   # "How NEET asks it" callout
      tip=r'<p>Shortcut…</p>',                    # "Shortcut" callout
      examples=[                                  # extra worked examples (solution hidden behind a toggle)
          dict(tag='Numerical', q=r'<question html>', steps=[r'step 1', r'step 2'], answer=r'12 m'),
          dict(tag='Graph', q=..., steps=[...], answer=...),
      ],
      practice=[                                  # extra MCQs → IDs c11-<section-id>-p1, -p2, … (append only!)
          dict(q=r'…', options=['…', '…', '…', '…'], answer=2,
               explanation=r'Why 3 is right and why the tempting wrong options are wrong.',
               type='numerical'),   # numerical | concept | ar | statement | multi | match | graph
      ],
  ),
}

NEW_SECTIONS = [                 # whole new sections for missing subtopics
  dict(chapter='linear', after='linear-graphs', id='linear-variable',   # id must start with '<chapter>-'
       title='Variable acceleration',
       intro=r'…', reasoning=r'…',
       formula=r'a = v\frac{dv}{dx}', symbols='…',
       trap=r'…', example=r'…', solution=r'…',
       question=r'…', options='opt A|opt B|opt C|opt D', answer=1, explanation=r'…',
       deep=dict(notes=[…], examples=[…], practice=[…])),   # same fields as DEEP
]
```

## Rules

- Strings are HTML fragments. Close every tag. Inline math `\( … \)`, display math `\[ … \]` (MathJax). Never use a bare `$`; it starts inline math.
- In formula fields, give the LaTeX only, without delimiters (the card wraps it in `\[ \]`).
- Figures: inline SVG with explicit fills, colours from CSS variables (`style="fill:var(--water-soft);stroke:var(--ink-2)"`), text at 11–13 px, `viewBox` sized so labels stay inside. Light theme only.
- Practice IDs come from list position. Only ever **append** to a section's `practice` list; never reorder or delete, because saved answers are keyed by ID.
- Vary the correct-option position across questions. Explanations must say why the tempting wrong options are wrong.
- Never label anything a NEET past-year question or attach an exam year.
- Verify every number with a quick calculation (`python3 -c …`).
- Check a chapter with `python3 scripts/check_deep.py <chapter-key>`. It writes nothing. `python3 scripts/render_physics.py` regenerates the site; run it only after your module validates.
