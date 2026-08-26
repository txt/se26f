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

# Project 1a: Testing

**In one line:** using LLMs, extract test cases from the artifacts
of a prior project.

**Links:** [Home](../../../README.md) · [Project 1b](proj1b.md) ·
[Poster rules](poster.md) · [Use case format](usecases0.md) ·
[Prior projects](https://drive.google.com/drive/u/2/folders/1dGGQNCWC3BakD-nUZn5vPecPdm0KAhXA)

**Due:** see the [schedule](../../../README.md).
**Hand in:** one PDF report, uploaded to Moodle. No poster for Project 1a.
Keep it short: say what you did, show the evidence, stop.

## How to start

1. Check out a repo of prior code: fork one past project, clone your fork.
2. Give **at least three different LLMs** access to all of it — e.g.
   Claude Code, Gemini CLI, and Codex/Copilot, each fired up in that
   directory. If you can, add a fourth running locally (Ollama-class).

On cost: free tiers exist for all the big vendors, and the local
model costs nothing but disk. The local fourth is best-effort — no
marks lost for its absence, one honest sentence on why it is absent.
You repeat only the designated steps and your keeper prompts across
models, not every interaction — otherwise the month does not fit.

The point: you now own a large space of artifacts from prior work — code,
docs, tests, commit history. You cannot read it all. Your LLM can. Use it as
a librarian that runs around all that material for you: ask it where things
are, what matters, and what to read next.

## Goal

Take one prior project. Understand it. Reverse engineer its high-level design
as use cases. Design tests. Show that your tests cover that design. Then judge
the tests the project already had.

For sample projects to work on, see the past posters:
https://drive.google.com/drive/u/2/folders/1dGGQNCWC3BakD-nUZn5vPecPdm0KAhXA

Use an LLM as your guide. Learn the prior software with it. Then learn how to
write that code better.

## Report, do not repair

You do **not** fix, patch, or extend the software in Project 1a. You report on
the health of that software, as-is. But you must try to run it.

## Reality checks

- Old code rots. Your first pick may not build. It may not run.
- Start early. Try to build and run the product on day one.
- Set a deadline for yourself. If the product does not run after two days of
  honest effort, switch to another product.
- A late switch kills a team. An early switch costs one afternoon.

## What to do

(For pasts 3,5,6,7 you will need to do a little technical writing. Use the
latex format described below.)

Do the steps in order. First form your own view of the design (steps 1–6).
Only then judge their tests (step 7). Steps 2 and 7 are LLM-heavy:
run them with **each** of your models, then reconcile in step 8.

1. Select one prior project (see the sample posters above). Fork it. Build
   it. Try to run it. If it will not run, pick again — now, not next week.
2. Understand the project. Reverse engineer its high-level design as the 20
   main use cases.
   - Use the format shown in [usecases0.md](usecases0.md).
   - Main scenario stays clean. All branching goes in the extensions.
3. Design your own test cases for those use cases.
4. Run your tests. Keep samples of the raw output.
5. Make a results table: for each test, what you expected, what happened,
   and why you tried it.
6. Make a traceability table. Each row connects one test to one use case.
   This shows your tests cover the reverse-engineered design.
7. Now look at the tests the project already has. Comment: do those tests
   cover the use cases? Where are they blind?
8. Cross-model comparison. Run your keeper prompts on every LLM
   (three or more; plus the local fourth if you have one). Make a
   table: prompt × model → verdict. Where models disagree, say which
   one you believed and what evidence settled it. Disagreement is
   data: a use case only one model found is either a gem or a
   hallucination, and you must say which.

**Expect some failures.** Old code has bugs, and code rots. A failing test on
a real fault is a finding, not a mistake. Report it with pride, and explain
why it fails. Be suspicious of a report where every test passes on old code.
Honest failures are better.

Example results table:

| Test | Why we tried it | Expected | What happened |
|---|---|---|---|
| `test_rejects_empty_cart` | UC1 extension 3a says items required | Order refused | PASS |
| `test_refund_on_no_response` | UC3 ext 2b: auto-cancel after N min | Refund issued | **FAIL** — no timeout exists; customer charged, no food. Real bug. |
| `test_gps_fallback` | UC2 ext 3a: status without map | Status shown | PASS |

More tests are better. One past group wrote 130+ test cases. Those tests let
them change the code and keep the old functions safe.

## Ten starter prompts

Ten prompts that can give insight. Note the pattern in all of them: give the
LLM a role, paste real evidence, demand a fixed output format, and forbid
guessing. **Warning: these ten are not enough.** They are starters. The higher
scores go to teams that invent better prompts of their own. Be creative.
Run each keeper prompt on all your models: agreement is cheap
confirmation; disagreement is where the marks are.

**1. First contact with the repo.**

```
You are a senior engineer who joined this project one hour ago. Below is the
output of `tree -L 3` and the full README.

In 300 words or less:
1. Name the main components and what each one does.
2. List the five files that matter most, ranked. One sentence each on why.
3. Name one directory we can safely ignore this month.

Do not guess. If the tree does not show enough, tell me exactly which file to
paste next.

<paste tree output>
<paste README>
```

**2. From module to user goals.**

```
Below is one module from a system you have never seen. Work only from this
code. Use no outside knowledge of the product.

List every user goal this module serves. For each goal give:
- Actor
- Trigger
- Main flow: numbered steps, six steps maximum
- One failure the code visibly handles (cite the line)

Then list any dead code: functions that no goal seems to need.

<paste module>
```

**3. Write a use case, then find its edges.**

```
Here is our use case format, with one worked example:

<paste the format and UC1 from usecases0.md>

Write the use case for <feature X> in exactly this format, from the code
below. Then:
- List three extensions the code already handles. Cite file and line.
- List three extensions the code does NOT handle. For each, say what a user
  would see when it goes wrong today.

<paste the relevant code>
```

**4. The undocumented product.**

```
Below: the README, and a list of every public function/endpoint/command in
the code.

What does this code do that the README never mentions? List each hidden
feature with the file and line that proves it exists. Rank the list by how
much a real user would care. Say which hidden features deserve a use case in
our top 20.

<paste README>
<paste function/endpoint list>
```

**5. Where the code is rotten.**

```
Below: `git log --stat` for the last two years, plus the dates each file was
last touched.

Which part of this code breaks first if we start changing things? Give a
ranked list of the three most fragile areas. For each, cite your evidence:
churn, age, TODO/FIXME density, functions over 50 lines, or anything else
you can see in the data. Do not use folklore about this product — only the
evidence below.

<paste git log --stat output>
```

**6. Triage a broken build.**

```
I am trying to build this product and it fails. Facts:
- OS and version: <...>
- Language/runtime version: <...>
- Exact command I ran: <...>
- Exact, complete error output: <paste>
- Date of last commit to the repo: <...>

Classify the failure: (a) code rot (depends on something the world no longer
provides), (b) my setup, or (c) a real bug. Give your confidence for each.
Then give the three cheapest experiments, in order, that would settle it.
If it is probably code rot, estimate the repair cost and say at what point
we should abandon this product for another.
```

**7. Tests for naked code.**

```
The function below has no tests. Its callers are also below.

Write tests for the happy path plus two edge cases you can defend from the
code. Rules:
- Test names must read as sentences ("test_rejects_empty_cart").
- After each test, one line: "This proves ...".
- If you must assume something about the environment, state the assumption
  instead of hiding it in the test.

<paste function>
<paste callers>
```

**8. Traceability, both directions.**

```
Below: our 20 use case names, and our full list of test names.

Build the traceability table: one row per test, columns = test name, use
case(s) it covers, what it proves. Then flag orphans in BOTH directions:
- Use cases with no test (our real gaps).
- Tests that map to no use case (what are they for?).

Do not invent coverage. If the mapping is unclear from the names, mark it "?"
and list what you would need to see.

<paste use case names>
<paste test names>
```

**9. Then versus now.**

```
Below is how this code does <X>. It was written in <year>.

Show how a current mainstream library or language feature would do the same
job. Then answer, with no diplomacy:
- What is genuinely better now?
- What did the old way do better (performance, dependencies, clarity)?
- What would migration cost, and would you pay it? Why or why not?

<paste code>
```

**10. The honest rewrite.**

```
Rewrite the function below in a cleaner style. Hard constraint: behavior must
be identical — same inputs, same outputs, same errors.

Then, for each change you made:
- One line: what changed and why the old way was worse.
- One line: which of our tests would catch it if this change silently broke
  the behavior. If no test would catch it, say "UNCOVERED" — that is a test
  we still need to write.

<paste function>
<paste our current test list>
```

## What to hand in (one PDF to Moodle)

| # | Deliverable |
|---|---|
| D1 | Product choice: name, repo URL, one paragraph on why you picked it. Note any product you tried first and abandoned, and why. |
| D2 | 20 use cases, in the [usecases0.md](usecases0.md) format. |
| D3 | Tests: code link, samples of raw test output, and a results table (test / why we tried it / expected / what happened). Failures are fine — explain them. |
| D4 | Traceability table: your tests ↔ use cases. Plus your comment on the project's own tests: do they cover the use cases? Where are they blind? |
| D5 | Prompt notes. A very simple document — a half-page bullet list is fine: per model, the outputs that were **wrong**, and how you caught each one; which prompts earned their keep, which did not, one line of why each; the step-8 prompt × model table; one strengths/weaknesses line per model **on this repo specifically**; and the local-model result (or the one sentence on why none ran). Zero caught errors reads as zero checking. |

## The demo video

There is no live demo for Project 1a. Instead, make a short video (2–5
minutes) of the software running. Show real runs: your tests executing,
passes and failures both. Put the video link in your report. The video is
3 of the 5 marks.

## Report format

- LaTeX only. Use the [ACM template](https://www.overleaf.com/latex/templates/association-for-computing-machinery-acm-generic-journal-manuscript-template/yffvrvzbhhpt).
- Use the two-column header:

```latex
\documentclass[sigconf]{acmart}
```

- No minimum length. Short and dense beats long and padded.
- Compile to PDF. Submit to Moodle.

## Rubric

Score each deliverable D1–D5. Your report mark = the five D-scores
summed, divided by 7.5 (so 15/7.5 = **2 report marks max**; the demo
video is the other 3 of this project's 5).

| Score | Meaning |
|---|---|
| 0 | Missing, or major issues. |
| 1 | Present, but has issues. |
| 2 | Well done. |
| 3 | Exceptional. Rare. |

Fast checks for the marker:

- D2: 20 use cases present? Extensions non-trivial (not "1a: error → show message")?
- D3: do the tests actually run? Raw output samples present? Results table
  with expected-vs-happened? Failures explained, or hidden?
- D4: does every use case have at least one test? Gaps explained? Honest
  verdict on the project's own tests?
- D5: real caught-error stories, with evidence? Prompts beyond the ten
  starters? Real reflection, or padding? Evidence of three or more
  models actually used (transcripts or screenshots, not claims)?
  Disagreements shown? "All models agreed on everything" reads as one
  model used three times.
- Fork history: commits from every member, small and steady?
  (git101's promise, checked here.) One giant midnight commit, or a
  member with no commits, loses marks.
- Format: ACM two-column LaTeX? If not, cap all scores at 1.
