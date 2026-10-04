# NEET Physics Notes

Interactive physics notes, simulations, solved questions, practice quizzes, and a revision sheet covering mechanical properties of solids and fluids.

Live website: https://bharathmuppasani.github.io/neet-physics-notes/

## Run locally

Requires Python 3. No package installation is needed.

```sh
python3 site/build.py --web
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. Section reading progress and practice answers are saved in the visitor's browser. Existing quiz answers remain compatible. Fonts and MathJax load from external services.

The three teaching pages contain 42 study sections, 33 interactive models, and a bank of 157 solved questions. Every chapter formula card defines its symbols and assumptions. Questions link directly to the lesson that introduces their concept; practice can be filtered by chapter and individual questions can be retried.

## Verification

Run the dependency-free checks with Node.js:

```sh
node tests/check-site.cjs
```

The build workflow runs these checks before publishing. `tests/browser-check.js` contains a Playwright function for a local server on port 8766. It checks answer toggles, saved progress, cross-tab updates, retries, filters, print-preview recovery, model calculations and phone/tablet layouts. The coverage review and reference sources are documented in [docs/site-audit.md](docs/site-audit.md).

## Deployment

Pushing to `main` builds the website and deploys it to GitHub Pages using `.github/workflows/pages.yml`. GitHub Pages uses GitHub Actions as its publishing source.

The `site/` folder contains the source HTML, CSS, JavaScript, question banks, and build script. Generated output in `dist/`, original paper photos, and local PDF exports are excluded from Git.

The original embedded-artifact build is still available with `python3 site/build.py`.
