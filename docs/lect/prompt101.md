<p align="center">
  <a href="https://github.com/txt/se26f/blob/main/README.md"><img 
     src="https://img.shields.io/badge/Home-%23ff5733?style=flat-square&logo=home&logoColor=white" /></a>
  <a href="https://github.com/txt/se26f/blob/main/docs/lect/policies.md"><img 
      src="https://img.shields.io/badge/Policies-%230055ff?style=flat-square&logo=openai&logoColor=white" /></a>
  <a href="#"><img
      src="https://img.shields.io/badge/Teams-%23ffd700?style=flat-square&logo=users&logoColor=white" /></a>
  <a href="https://ncsu.hosted.panopto.com/Panopto/Pages/Sessions/List.aspx#folderID=d778d356-94d2-48b1-a25f-b4a401818991"><img 
      src="https://img.shields.io/badge/Lectures-%238a2be2?style=flat-square&logo=panopto&logoColor=white" /></a>
  <a href="https://moodle-courses2527.wolfware.ncsu.edu/course/view.php?id=12082&bp=s"><img 
      src="https://img.shields.io/badge/Moodle-%23dc143c?style=flat-square&logo=moodle&logoColor=white" /></a>
  <a href="https://discord.gg/zrsW8F2V9"><img 
      src="https://img.shields.io/badge/Chat-%23008080?style=flat-square&logo=discord&logoColor=white" /></a>
  <a href="https://github.com/txt/se26f/blob/main/LICENSE.md"><img 
      src="https://img.shields.io/badge/©%20timm%202026-%234b4b4b?style=flat-square&logoColor=white" /></a></p>
<h1 align="center">:cyclone: CSC510: Software Engineering <br>NC State, Fall '26</h1>
<img src="https://raw.githubusercontent.com/txt/se26f/refs/heads/main/etc/img/se26f.png">

# Prompt 101: growing a model you can half-trust

**Links:** [Home](../../README.md) ·
[diapers.py](https://github.com/txt/se26f/blob/main/docs/lect/brooks/diapers.py) ·
[sd0.py](https://github.com/txt/se26f/blob/main/docs/lect/brooks/sd0.py) ·
[test101](test101.md) · [Proj1a](../submit/1/proj1a.md)

This lecture comes *before* [test101](test101.md), and builds
test101's raw material: we prompt an LLM into writing the Brooks'
Law model, step by disciplined step. The output is code you
half-trust. Turning half-trust into trust is the next lecture's
job.

## 0. Twenty prompting heuristics for SE ▪▪▪▪▪▪▪▪▪▪▪▪

*(~12 min.)*

1. **State the contract.** Signature, types, pre/post-conditions,
   error behavior. 1 input→output example beats 3 paragraphs.
2. **Convert the ask into tests first.** "Fix the bug" → "write
   the test that reproduces it, then make it pass." Aim for 3–5
   tests: 1 happy path, 2–3 edge, 1 failure.
3. **Emit a step→verify plan for anything over ~50 LOC.** 3–7
   steps, each with its check. It's your progress meter, not just
   a grade.
4. **Paste real artifacts, not summaries**: the function, its
   callers, the failing trace. Verbatim.
5. **One task per prompt.** Refactor or feature or tests.
6. **Bound the diff.** Every changed line must trace to the
   request. No tidying adjacent code.
7. **Bound the size.** "≤ 50 lines, stdlib only, no new
   abstractions." If it writes 200 where 50 would do, reject.
8. **Force assumptions up front.** "List ≤3 assumptions and any
   ambiguity before coding; if unclear, stop and ask."
9. **Demand provenance.** Every finding cites the
   requirement/standard/line that triggered it. No citation →
   drop it.
10. **Allow abstention.** "If grounding is thin, output
    INSUFFICIENT and stop." Cheaper than a confident wrong
    answer.
11. **Ask a question, not a score.** "Security: 2/5" teaches
    checkboxes; naming the tension ("assumes always-on
    connectivity, but your users are rural") gets acted on.
12. **Ask for the minimal delta.** "Smallest change that moves
    this from level 2→3" beats a grade or a rewrite.
13. **Self-falsify.** "Give 3 inputs that break this."
14. **Calibrate before trusting a review prompt.** ~50
    human-labeled cases, target κ > 0.6, then iterate the prompt.
15. **Iterate on error text, not the request.** Paste the
    traceback; say "fix."
16. **Fresh context per topic; 2–3 models for high-stakes calls.**
17. **Demand a fixed output format.** Table, JSON, unified diff,
    one fenced file — an answer with a declared shape is
    checkable, diffable, parseable.
18. **Never accept claimed execution.** "All tests pass" from a
    model is a claim, not an observation. You run it; your
    transcript is the evidence.
19. **Prompts are code.** Keeper prompts live in the repo,
    versioned; log every wrong output and how you caught it (the
    D5 habit); rerun keepers when the model changes.
20. **Cross-examine high-stakes answers.** A second model,
    prompted to *refute*. Agreement is cheap confirmation;
    disagreement is data.

## 1. Case study: prompting Brooks' Law into existence ▪▪▪▪▪▪▪▪▪▪▪▪

*(~18 min.)* The goal: an LLM writes the `brooks()` model for
[sd0.py](brooks/sd0.py)'s engine. We already have the perfect
few-shot exemplar: [diapers](brooks/diapers.py). Nine steps, each
tagged with the heuristics doing the work.

**Step 1 — contract by example** *(#1, #4, #7, #17)*:

```
Here is a compartmental-model engine and one worked model,
verbatim. [paste sd0's o/run/verdict + all of diapers.py]

In EXACTLY this shape — a closure returning
o(init=..., step=..., y=..., rq=..., ctrl=...), stocks as
[now,lo,hi] triples, step(dt,t,u,v) — write brooks():
Brooks' Law, "adding staff to a late project makes it later."
≤ 35 lines. Same engine, no new abstractions, every model
line commented. Output: one fenced Python block, nothing else.
```

The diapers paste does more work than any specification prose:
it fixes the API, the commenting style, the bounds convention,
and the y/rq shape, all at once.

**Step 2 — assumptions before code** *(#8, #10)*:

```
Before writing it: list at most 3 assumptions you must make
(what are the stocks? what makes hiring costly? what makes it
eventually pay off?). If Brooks' mechanism is unclear to you,
output INSUFFICIENT and stop.
```

What you want back: D/N/W/R-ish stocks; a communication tax that
grows ~n²; mentoring that taxes veterans. If its assumptions miss
the n² term, stop — the code after a wrong assumption is wasted
tokens.

**Step 3 — ask it how we would test, BEFORE it codes** *(#2, #11)*:

```
Still no code. How would we test this model? List checks.
```

Here is the beautiful part: **you already own the oracle for
this answer — Forrester.** A good reply rediscovers
Forrester & Senge on its own: conservation (W+R constant, D+N
changes only by HIRE), extreme conditions (no devs → no work),
behavior reproduction (the late-project dip), sensitivity. Grade
the reply against that checklist; if extremes and conservation
are missing, say so and ask again. A model that cannot plan the
tests should not be trusted to write the code.

**Step 4 — plan, then build** *(#3, #5)*:

```
Now a 5-step build plan, each step with its check. Then the
code, one fenced block.
```

One task per prompt still holds: the plan and the code are one
task (the plan is the code's scaffold); the *tests* were the
previous task and the *review* is the next one.

**Step 5 — you run it** *(#18, #15)*:

```
$ python3 sd0.py        # the horizon sweep, on ITS brooks()
```

Its "this should work" is a claim. Your terminal is the
evidence. If it crashes: paste the traceback verbatim, say
"fix" — nothing else. The traceback is a better prompt than any
sentence you could write about the traceback.

**Step 6 — self-falsify** *(#13)*:

```
Give 3 inputs that break your model.
```

The real sd0 has a genuine answer hiding here: `WHEN=7.5` — the
hire silently vanishes, because `t == u.WHEN` never fires on
integer ticks. If the model finds that class of bug in its own
code, that is worth more than ten passing runs. (test101's
Forrester harness later catches the same bug from the outside,
via sensitivity analysis.)

**Step 7 — cross-examine** *(#16, #20)*:

```
[to a second model] Here is a Brooks' Law model. Refute it:
what does it get wrong about Brooks' actual argument?
```

Disagreement is data. One likely finding: Brooks' book also
blames task divisibility ("nine women, one month"), which this
model omits — a boundary-adequacy point (Forrester rule 1) no
single-model conversation surfaced.

**Step 8 — keep the keepers** *(#19)*:

The prompts from steps 1–4 go in the repo next to the code they
built. They are the model's build script. When the LLM version
changes, rerun them: same contract, same test plan expected —
that is regression testing for the *model*, not the code.

**Step 9 — hand off.** You now have `brooks()` and a test plan
it wrote under supervision. You half-trust both. Making that
trust real — harnesses, conservation checks, horizon sweeps,
the verdict flip — is [test101](test101.md), which starts
exactly where this lecture ends.

## Exercise 1: your turn at the wheel ▪▪▪▪▪

*(~5 min start in class.)* Run the nine steps yourself, but for
a DIFFERENT model: pick one of `bugs` (defects found vs
remaining), `rework` (done vs done-badly-redo), or `sir`
(susceptible-infected-recovered). Diapers stays your step-1
exemplar. Keep your step-2 assumptions and step-3 test plan —
they are Proj1a D5 material, and next lecture you will test
what you grew.

## 2. Keeper prompts are code ▪▪▪▪

*(~5 min.)* The through-line of heuristic #19, said once more
with feeling: a prompt that worked is an asset. Version it.
Rerun it on model upgrades. Log its failures (D5: wrong outputs
+ how caught; zero caught errors reads as zero checking). The
[proj1a starter prompts](../submit/1/proj1a.md) are keeper
prompts — note that every one of them uses #1, #4, #10 and #17
(role, verbatim artifacts, forbid guessing, fixed format).

## Explore in your own time

- Heuristic #14 in practice: build a 50-case labeled set from
  your fork's issues; measure a review-prompt's κ before
  believing it.
- Chain-of-verification: ask for the answer, then ask the same
  model to list checks on its answer, then apply them.
- Prompt-diffing: when a keeper prompt starts failing after a
  model upgrade, bisect the prompt like you would bisect code.
- The economics: tokens ≈ money; #12's minimal-delta and #7's
  size bounds are cost controls, not just quality controls.
