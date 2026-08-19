---
name: course-docs
description: Use when editing any markdown in this course repo (README, docs/lect, docs/submit) — header propagation rules, make mds, schedule conventions, marks bookkeeping, M0 eval doctrine.
---

# Editing se26f course docs

## Header propagation (make mds)

- `make mds` copies the README header (lines 1 → first blank line: badge
  block + h1 + banner) onto LICENSE.md and every `docs/**/*.md`,
  **deleting each target's first block** (lines 1 → first blank line).
- Therefore every docs md MUST start with the header block ending in a
  blank line, or its first paragraph gets eaten on the next `make mds`.
  New file? Paste the README header + blank line at the top first.
- Change a badge/banner only in README.md, then run `make mds` to
  propagate. Never hand-edit headers in docs files.
- `make mds` is idempotent; run it before every commit that touches
  markdown.

## Single sources of truth

- Dates, due dates, talk slots, marks-per-week: README schedule table.
- Week-1 lectures: n01 (basics) + docs/lect/git101.md (git three ways,
  split out of n01 section 1, which keeps a pointer).
- N1 exercise links the Section-1 poster Drive folder and the shared
  scoring Google Sheet. The repgrid workbooks live in etc/:
  repgrid-sheet.xlsx (phase 1, share), repgrid-phase2.xlsx (supplied
  constructs, share AFTER elicitation), repgrid-anchors-SECRET.xlsx
  (LLM scores on the four Table-1 scales — never share).
- Grade totals (must sum to 100) and NCSU-required sections:
  `docs/lect/policies.md`. Keep it terse — rubric detail lives in
  project files, not policies. Policies lists exactly six learning
  outcomes (four SE + two AI-facing: LLM error-catching, M0 eval).
  Add an outcome ONLY if a graded deliverable provably assesses it;
  long outcome lists are hubris.
- Per-project rubrics and marks splits: `docs/submit/*/proj*.md`.
  Policies' per-project totals (5/7/19/21) must match those files.

## Course doctrine (keep consistent when editing)

- Teams of four, for projects AND talks (teams A–Q = 17; talks 15 min,
  ≤4/night). Talk rubrics live in docs/lect/talk.md: two sections
  (tool talk, task talk), 7 marks each, five live-gradeable rows
  (2+2+1+1+1) — every row decidable as it happens. README talk cells
  read "[tool](talk.md#...) [A](#)·[B](#)…": the word links the
  rubric section; the letters are dead (#) placeholders until team
  pages exist.
- "Failures are findings": honest failed results score; hidden failures
  cost more than honest low scores. Applies to tests, self-rubrics, and
  M0 evals alike.
- M0 = required business-level eval milestone (proj2, inherited+new in
  proj3): measurable claim (metric, threshold, baseline) + runnable
  instrument in CI. Synthetic data suffices for full marks; real data is
  bonus only. Framed via Boehm's spiral (docs/lect/spiral.pdf).
- D5 prompt reports reward *caught LLM errors*, not prompt cleverness.
- Multi-LLM rule (proj1a and 1b): at least THREE different LLMs, plus
  a best-effort local fourth (Ollama-class; no marks lost if absent,
  one honest sentence why). Keeper prompts run on every model;
  disagreement is data. 1a step 8 = prompt × model comparison table.
  1b: market survey + red team on every model; a rival counts only if
  two models name it or one gives a live URL.
- "Rival" is DEFINED at the top of proj1b: a competing software
  product on the market — never one of the LLMs (those are
  "independent analysts"). Keep that usage clean everywhere.
- Rubric-to-marks scaling is stated inside each rubric: 1a D-sum/7.5
  = 2 report marks (demo video = the other 3 of 5); 1b D-sum × 7/15
  = 7 max.
- Proj3 grace: submission online over Thanksgiving break, no late
  marks until Dec 1. Never say "seven-day" (it is not).
- There is NO published cohort quality grid — that promise was
  removed from policies and the N1 exercise. Constructs guide fork
  picks and rubric reading only.
- Reports: ACM two-column LaTeX (`\documentclass[sigconf]{acmart}`),
  PDF to Moodle. Length: 1a has NO minimum ("short and dense beats
  long and padded"); 1b must be more than four pages.

## Style

- Plain words, short sentences, no buzzwords. Rubrics say how marks are
  lost, concretely. Colors in schedule: 🟩 + `${\color{green}...}$` for
  holidays, 🟥 + `${\color{#ff9999}...}$` for exams.
