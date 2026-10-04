# Class 11 physics expansion — 4 October 2026

## Scope and organisation

The uploaded images contain four Class 11 physics volume indices, three chemistry volume indices and two biology contents pages. Original images were renamed into subject folders, preserving bytes and recording filename mappings/SHA-256 in the local `papers/syllabus/file-manifest.json`. The exact duplicate of chemistry volume 3 is retained under `duplicates/`; the exam schedule has its own folder.

`content/syllabus.json` and `docs/syllabus-catalogue.md` transcribe these contents. The public syllabus page lists chemistry and biology as well as physics. Their legacy textbook topics are not presented as an official current NEET syllabus.

## Teaching coverage

| Volume | Added chapters |
| --- | --- |
| I | Maths & Physical World; Units and Measurements; Straight-Line Motion; Vectors; Motion in a Plane; Laws of Motion Part 1 |
| II | Friction; Work, Energy & Power; System of Particles & Rotational Motion |
| III | Gravitation; Oscillations; existing Solids and both Fluids parts retained |
| IV | Waves; Thermal Properties; Kinetic Theory; Thermodynamics |

15 new chapters add 102 studied sections to the existing 42. Each new section has two explanatory paragraphs, a formula card with local symbols/units/assumptions, a misconception, a separately solved example and a retrieval question. The text is authored for this site. The coaching maths, vectors and friction modules retain their own pages even where NCERT groups them differently.

Additional connections include signed motion and graph area, pulley constraints, apparent weight, rolling without slipping, angular-momentum energy changes, spherical fields, U-tube oscillations, gas mixtures and connected rigid insulated cylinders. The cylinder explanation introduces the system and energy balance before asking questions; valve-opening mixing is distinguished from reversible adiabatic compression.

Twelve new labelled interactive models cover uncertainties, vector components, motion graphs, projectiles, kinetic energy, spin conservation, altitude-dependent gravity, SHM, wavelengths, conduction, molecular speeds and isothermal work. Together with the existing 33 models, there are 45.

The all-chapter formula reference contains 179 formula cards, including the existing Solids/Fluids cards with their definitions. The concise older Solids/Fluids revision sheet remains available.

## Practice and provenance

The bank grows from 157 to 317 questions:

- 102 original topic retrieval checks.
- 30 original mixed-step challenges, selectable with the practice filter.
- 28 independently solved adaptations of selected NCERT Exemplar patterns.

`collect_exemplar.py` retrieves the 14 official publicly available Exemplar PDFs and extracts question identifiers. Its public manifest includes URLs and SHA-256 values; raw PDF/text stays local. The collector does not import answer keys. Selected adaptations record the exact source question and use original wording, changed values where appropriate and independent explanations. No adaptations are labelled NEET PYQs and no unverified exam year is attached.

The SATHEE collection was useful for discovery but its lift-sign solution contradicted the stated ground-origin/upward-positive convention. It was not copied into the bank. Official NCERT PDFs are the attribution targets. A spot check also corrected an initially mismatched thermodynamics source reference before publication: Q12.5 now adapts the actual isothermal-versus-adiabatic compression comparison.

The original question IDs and storage keys are preserved. New option rotations depend on stable topic IDs rather than section order, protecting stored choices from a future chapter reordering. Reading progress covers all 18 teaching pages; practice filters and source attribution route every question to an existing introduction.

## Validation

- Structural checks: 317 unique four-option questions, 144 registered ordered sections, all teaching anchors and resources, all chapter formula definitions, script syntax, saved-state compatibility and corrupt/blocked-storage recovery.
- Physics checks: 71 independently specified answer fixtures, elastic-collision momentum/energy invariants, and all 28 source question identifiers.
- Browser checks: answer disclosure controls on every inline chapter card; example disclosure labels; saved reading and answer state; retries and cross-tab updates; source/chapter/challenge filter intersections; print recovery; 317 questions and answer-key entries in questions-only mode.
- Model checks: twelve new default calculations and input updates, plus the existing connected-vessel, wire, lift, viscous-flow and capillary worked cases.
- Layout checks: all 24 learning/library pages at 320, 390 and 768 px, with no page-level horizontal overflow or MathJax error elements. Long question topic chips now wrap without expanding the card.

The structural and numerical fixtures do not claim to re-solve every old module-test question. PDF export remains paused; existing local PDF files are not published.
