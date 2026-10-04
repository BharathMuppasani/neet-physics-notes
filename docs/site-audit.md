# Chapter completion review — 4 October 2026

This is the earlier Solids/Fluids checkpoint. The subsequent full Class 11 expansion supersedes its coverage and totals; see [class11-expansion.md](class11-expansion.md).

The scope is the existing Mechanical Properties of Solids and Mechanical Properties of Fluids chapters. The homepage explicitly identifies the other CUT-6 chapters as outside this site's current coverage.

## Content findings and repairs

| Area | Finding | Result |
| --- | --- | --- |
| Fluids I 9.2.1 / 9.2.2 | Material was folded into one pressure section, obscuring NCERT coverage | Separate indexed lessons for Pascal's law and variation of pressure with depth; equilibrium derivations and conditions |
| Connected cylinders | A gravitational-work numerical introduced its shortcut only inside the solution | Dedicated lesson before the question: bottom-pressure balance, conservation of volume, unequal-area final level, centre-of-mass energy calculation, general and equal-area work formulas, interactive before/after model |
| Dynamic lift | Section was an unfinished placeholder; existing canvas code had no controls | Wing-pressure model, Magnus effect, roof/atomiser applications, level-flight small-speed approximation, two examples and working simulation controls |
| Fluids I problem patterns / checklist | Two unfinished placeholders | Eight problem patterns, jet-momentum example, checklist and formula reference |
| Accelerating containers | Questions existed with only brief remarks | Effective gravity, horizontal slope, vertical pressure, floating fraction and free-fall limit; working model and dedicated question routing |
| Combined wires and own weight | Rules were mentioned briefly in shortcuts | Series/parallel constraints, stiffness versus modulus, equivalent modulus, varying-tension integral, maximum top stress, model and practice |
| Viscous pipe flow | Absent | Optional coaching extension: assumptions, Poiseuille law, velocity profile, unit conversions, worked example and low-Re validity note |
| Capillary-rise experiment | One calculation but no full method | Apparatus, procedure, inner-radius and height measurements, errors, precautions, meniscus correction, calculator and practice |
| Advanced buoyancy | Hollow bodies and variable-density sphere questions relied on one-line hints | Sealed-cavity mass/volume distinction; shell-volume integral; burning-candle geometry explained before questions |
| Formula notation | Many cards used undefined symbols or omitted limits | All 77 main chapter formula cards have local symbol/unit/assumption explanations; all 49 revision cards link to the relevant explanation |
| Physics precision | Outdated NCERT labels and overly broad statements | Corrected section numbering, restored core status of Poisson's ratio/elastic energy, signed radius compression, Bernoulli streamline conditions, free-fall exceptions, lubricant qualification and geometry-dependent Reynolds conventions |

## Progress and controls

- The original `phy-notes-attempts-v1` key and question IDs are retained, preserving existing valid answers.
- A separate study record tracks 13 Solids, 17 Fluids I and 12 Fluids II sections. Completion is deliberately marked by the reader, and can be reversed.
- Homepage, chapter progress panels and section index show consistent saved state. Continue links lead to the next unstudied section or chapter practice after completion.
- Practice scores follow the selected chapter/source/topic. Each question can be retried without resetting the entire bank. Existing paper flags remain separate from saved attempt results.
- Storage events and page restoration refresh displayed progress. Corrupt saved JSON is ignored; blocked storage retains changes for the current page session and shows a persistence notice.
- A global `[hidden]` CSS rule fixes the conflict with the solution panel's grid display. Quiz toggle labels and accessibility states match visibility; worked-example disclosure labels change between Show and Hide.
- Closing print preview restores the original interactive state instead of leaving print formatting/answer visibility active.

## Validation

`node tests/check-site.cjs` passed: 157 unique, well-formed questions; 42 ordered study sections; local links and teaching anchors; formula labels; JavaScript syntax; old answer compatibility; corrupt and blocked storage recovery.

`tests/browser-check.js` passed in Chromium using a fresh browser context:

- Show/hide controls on all 114 inline chapter question cards, with no visibility or accessibility-state failures; native worked-example disclosures checked on each chapter.
- Mark/unmark, reload persistence, homepage continuation, cross-page quiz counts, cross-tab study updates/reset, complete-chapter routing and corrupted-state recovery.
- Wrong answer → retry → correct answer, chapter filtering and accurate chapter scores.
- Print-preview restoration and all 157 questions/answer-key entries in questions-only mode.
- Connected vessels: equal-area 6 m / 4 m gives 5 m final depth and 20,000 J work; unequal-area final height checked.
- Series/parallel wire extensions, wing pressure/lift, equal-speed zero lift, reversed Magnus force, vertical free-fall pressure, Poiseuille flow and capillary tension/error checked against worked examples.
- All six pages at widths 320, 390 and 768 px: no page-level horizontal overflow and no MathJax error elements. No JavaScript page errors.
- Desktop connected-cylinder model and phone pressure lesson visually inspected.

These checks cover the implemented models and sample calculations. They do not claim a fresh numerical re-solution of every original test question.

## Reference sources

The NCERT core coverage/section numbers were checked against the [2026–27 Solids chapter](https://ncert.nic.in/textbook/pdf/keph201.pdf) and [2026–27 Fluids chapter](https://ncert.nic.in/textbook/pdf/keph202.pdf). The capillary measurement is also listed in the [NCERT senior-secondary physics syllabus](https://www.ncert.nic.in/desm/pdf/desm_s_physics.pdf). Explanations are written for this site rather than copied from the textbooks.

The pipe-flow extension uses the model described by [OpenStax: viscosity and turbulence](https://openstax.org/books/university-physics-volume-1/pages/14-7-viscosity-and-turbulence). The wing lesson's lift explanation and equal-transit-time correction agree with [NASA: Bernoulli and Newton](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/bernoulli-and-newton/).
