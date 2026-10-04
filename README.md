# NEET Physics Notes

Interactive physics notes, simulations, solved questions, practice quizzes, and a revision sheet covering mechanical properties of solids and fluids.

Live website: https://bharathmuppasani.github.io/neet-physics-notes/

## Run locally

Requires Python 3. No package installation is needed.

```sh
python3 site/build.py --web
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. Practice answers are saved in the visitor's browser. Fonts and MathJax load from external services.

## Deployment

Pushing to `main` builds the website and deploys it to GitHub Pages using `.github/workflows/pages.yml`. GitHub Pages uses GitHub Actions as its publishing source.

The `site/` folder contains the source HTML, CSS, JavaScript, question banks, and build script. Generated output in `dist/`, original paper photos, and local PDF exports are excluded from Git.

The original embedded-artifact build is still available with `python3 site/build.py`.
