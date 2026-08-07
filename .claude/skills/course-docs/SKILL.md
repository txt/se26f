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
- Grade totals (must sum to 100) and NCSU-required sections:
  `docs/lect/policies.md`. Keep it terse — rubric detail lives in
  project files, not policies. Do not add outcome lists to policies.
- Per-project rubrics and marks splits: `docs/submit/*/proj*.md`.
  Policies' per-project totals (5/7/19/21) must match those files.

## Course doctrine (keep consistent when editing)

- Teams of four for projects; talk teams of three (A–Q, 15 min, ≤4/night).
- "Failures are findings": honest failed results score; hidden failures
  cost more than honest low scores. Applies to tests, self-rubrics, and
  M0 evals alike.
- M0 = required business-level eval milestone (proj2, inherited+new in
  proj3): measurable claim (metric, threshold, baseline) + runnable
  instrument in CI. Synthetic data suffices for full marks; real data is
  bonus only. Framed via Boehm's spiral (docs/lect/spiral.pdf).
- D5 prompt reports reward *caught LLM errors*, not prompt cleverness.
- Reports: ACM two-column LaTeX (`\documentclass[sigconf]{acmart}`),
  >4 pages, PDF to Moodle.

## Style

- Plain words, short sentences, no buzzwords. Rubrics say how marks are
  lost, concretely. Colors in schedule: 🟩 + `${\color{green}...}$` for
  holidays, 🟥 + `${\color{#ff9999}...}$` for exams.
