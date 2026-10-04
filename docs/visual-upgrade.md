# Physics visual and teaching upgrade — 4 October 2026

The user’s final direction is a short, problem-oriented lesson: simple concept → visual → when to use the formula → worked question → independent practice. Extra theory and derivations are optional. The existing homepage cards, direct navigation, and Solids/Fluids teaching are the design references.

## Integrated content

The workspace already contained a deepening draft for the 15 newer chapters. Syntax errors in linear motion, laws of motion and waves prevented a full build; these were corrected and the layer was integrated through the renderer. All 131 new-chapter sections have deeper notes and additional examples available. This includes 29 additional topics, 399 extra worked examples, and 521 additional MCQs. Together with the earlier bank, the site has 173 sections and 867 questions.

The default view keeps the core explanation and main formula, then shows a visual and worked problems. Extra formula cards, derivations, additional examples and extended question-pattern notes sit in disclosures. New short application notes replace long derivations in the introductions of the added topics. Content is still edited at its source, rather than in generated HTML.

The 35 new experiments cover every newer chapter, with at least two per chapter:

- Maths: tangent/velocity and integration/area.
- Units: vernier reading and uncertainty in area.
- Linear motion: a cart with connected graphs and distance/displacement.
- Vectors: components and force projection/work.
- Plane motion: projectile, river crossing and circular motion.
- Laws: ideal pulley and lift scale.
- Friction: adjustable static friction and an inclined block.
- Work/energy: spring energy, restitution and vertical-loop constraints.
- Rotation: centre of mass and rolling-body comparison.
- Gravitation: circular orbit and interior/exterior gravity.
- Oscillations: SHM projection and a pendulum with nonlinear dynamics.
- Waves: travelling particles, standing modes and beats.
- Thermal properties: hole expansion, melting and cooling.
- Kinetic theory: representative molecular motion and degrees of freedom.
- Thermodynamics: process-dependent P–V work, Carnot energy accounting and connected rigid insulated vessels.

Seven earlier graph explorers and 33 existing Solids/Fluids models remain, giving 75 interactive tools. Five redundant graph explorers were replaced by their guided counterparts.

Every experiment states its model and conditions. Animated motion requires an explicit click, pauses when offscreen or when the tab is hidden, and respects reduced-motion preference. Sliders remain usable without animation. Labels scale with screen width; numerical readouts remain HTML. The scenes are illustrative where noted: gas tracers are not a molecular-dynamics pressure calculation, vessel equilibration is not a flow solver, and vertical-loop motion stops at the first turning/slack-string event rather than drawing an invalid circular continuation.

## Validation and practical limits

- Deep-layer schema: all 15 chapter modules validate, including HTML and math delimiters.
- Structural checks: 867 unique questions, 173 ordered sections, formula definitions, anchors, assets and compatibility with all published question IDs.
- Existing physics fixtures: 71 answers plus source references and collision conservation.
- New experiment checks: 35 models, 173 default/boundary input states, independent numerical identities, energy/momentum conservation and limiting cases. Pendulum energy is checked against its numerical integration.
- New browser journeys: all 35 experiments, predictions, reset, optional theory, play/pause, responsive widths and reduced-motion scrubbing.
- Existing browser journeys: chapter answer toggles, examples, practice filtering, print recovery, reading/answer persistence, cross-tab updates and all 24 pages at 320, 390 and 768 pixels.
- Homepage/navigation: all 18 original-style chapter cards and eight direct links at six widths.

These checks do not independently re-solve every inherited or newly drafted MCQ. The syllabus images provide coaching chapter indices, not a detailed official current NEET syllabus. The coverage and tests should not be described as a proof of complete official-exam coverage.

Primary textbook references used during the thermal review: [NCERT Thermal Properties](https://ncert.nic.in/textbook/pdf/keph203.pdf) and [NCERT Thermodynamics](https://ncert.nic.in/textbook/pdf/keph204.pdf). Teaching text and experiment explanations are authored for this site.

## Editing and deployment

`content/deep/` supplies the extended material; `content/problem_briefs.py` supplies concise application notes; `content/visual_lessons.py` supplies experiment teaching. `assets/physics-labs.js` supplies pure calculations, responsive SVG scenes and controls. `assets/physics-labs.css` is scoped to the newer chapter pages. `scripts/render_physics.py` assembles the pages.

Run `python3 scripts/check_deep.py`, `python3 scripts/render_physics.py`, the three Node checks, then `python3 site/build.py --web`. GitHub Actions also validates the deep layer and experiment calculations before publishing. PDF work remains paused.
