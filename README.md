# NEET Physics Notes

Class 11 physics lessons organised around the uploaded coaching syllabus: four volumes, 17 module entries and 18 teaching pages (Fluids remains in two parts).

Live website: https://bharathmuppasani.github.io/neet-physics-notes/

The site has 173 study sections, 75 interactive models/experiments and 867 solved questions. The 15 newer chapters use a short concept → visual → formula application → solved problem → practice flow. They include 35 guided experiments with labelled readouts, play/pause or scrubbing, predictions and three practical solving steps. Derivations, additional formulas and extra problem patterns are optional disclosures. The integrated deepening layer adds 29 topics, 399 extra worked examples and 521 additional practice questions. Practice includes 30 original mixed-step challenges and 28 independently solved adaptations of NCERT Exemplar patterns. Adaptations link to their exact source question and are not labelled NEET past-year questions.

The chapter catalogue, syllabus library and formula reference cover the full uploaded Class 11 physics sequence. Chemistry and biology contents are organised in the syllabus library; lessons currently focus on physics. Original paper images stay local under `papers/syllabus/`, with a filename/checksum manifest and a separate folder retaining one exact duplicate.

## Run locally

Requires Python 3.9+ and no additional packages for rendering or serving.

```sh
python3 scripts/render_physics.py
python3 site/build.py --web
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. Section progress and answers are saved in the visitor's browser. Existing valid answers and study marks remain compatible. Fonts and MathJax load from external services.

## Content and sources

- `content/physics_lessons.py`: base lesson text, definitions, examples and retrieval questions.
- `content/deep/`: additional topics, explanations, formulas and problem patterns.
- `content/problem_briefs.py`: concise application notes for the additional topics.
- `content/visual_lessons.py`: experiment introductions, assumptions, predictions and solving recipes.
- `site/assets/physics-labs.js` and `physics-labs.css`: responsive experiments and scoped chapter styling.
- `content/challenge_practice.py`: original mixed-step NEET-style questions.
- `content/exemplar_practice.py`: reviewed, rewritten NCERT Exemplar adaptations.
- `content/syllabus.json`: transcription of the uploaded subject/volume contents.
- `content/exemplar_sources.json`: official PDF URLs, checksums and extracted question identifiers.
- `scripts/render_physics.py`: deterministic static-page and question-bank renderer.
- `site/_home-body.html`: homepage layout, kept separate from generated lessons.
- `scripts/collect_exemplar.py`: optional public-source collector; requires `pypdf`. Downloaded PDFs and extracted text stay in ignored `papers/references/`. Answer keys are not automatically imported.

The syllabus catalogue describes the uploaded books; it is not a claim that every legacy book topic is in the current official exam syllabus. See [docs/syllabus-catalogue.md](docs/syllabus-catalogue.md) and [docs/class11-expansion.md](docs/class11-expansion.md).

## Verification

```sh
node tests/check-site.cjs
node tests/check-physics.cjs
python3 scripts/check_deep.py
node tests/check-labs.cjs
```

Checks cover question/section integrity, formula labels, links, saved-state compatibility and recovery, 71 answer fixtures, collision conservation and source identifiers. `tests/browser-check.js` is a Playwright function for a local server on port 8766. It covers solution controls, progress persistence, cross-tab updates, practice filters, print recovery, model calculations and all 24 learning/library pages at phone/tablet widths.

`tests/home-navigation-check.js` checks all 18 homepage chapter cards and nine direct navigation tabs at six widths from 320 to 1280 px, saved progress, chapter links and revision. The homepage and chapter library share the original chapter card design: coloured borders, explanations and concept chips, organised by the four syllabus volumes. The library cards also show saved study and practice progress. The exam overview remains on the homepage. Publishing adds content hashes to asset URLs so updates reach returning readers.

`tests/labs-browser-check.js` checks all 35 new experiments against a built site on port 8767: input updates, reset, prediction feedback, optional theory, play/pause, reduced motion and phone/tablet layouts. See [docs/visual-upgrade.md](docs/visual-upgrade.md) for the teaching approach and verification limits.

The earlier Solids/Fluids review is retained in [docs/site-audit.md](docs/site-audit.md).

## Deployment

Pushing to `main` validates, builds and deploys through `.github/workflows/pages.yml`. `site/` contains the published source. Generated `dist/`, original paper photos and local PDF exports are excluded from Git. PDF work is paused.

The original embedded-artifact build is still available with `python3 site/build.py`.
