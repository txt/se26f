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

# Project 2: Build

**Links:** [Home](../../../README.md) · [Project 1a](../1/proj1a.md) ·
[Project 1b](../1/proj1b.md) · [Project 3](../3/proj3.md) ·
[Poster rules](../1/poster.md) · [Policies](../lect/policies.md)

**Due:** see the [schedule](../../../README.md).
**Hand in:**

1. One PDF to Moodle: your poster, your repo URL, and your self-assessed
   repo rubric (below). No report. The repo is the evidence.
2. Also drop your poster PDF into the shared
   [Project 2 poster folder](https://drive.google.com/drive/folders/1sl6olGqGQmaa9V4D2iFsTbfB2f1lza1Q?usp=drive_link).
   This folder is the catalog: other teams shop there to pick their
   Project 3 codebase. No poster in the folder = nobody picks your repo.

## Goal

Build a product that boasts your skills to employers. Make it professional.
Make it so good that another team will demand to extend it in Project 3.

1. Deliver four (or more) major, impressive milestones.
2. Build a framework that lets others deliver four more milestones in
   Project 3.
3. Sell it: poster, demo video, and a clean public repo.

## Scope

You are not bound by your Project 1b proposal. Teams often get halfway in,
then see that the real problem is different. That is not failure. That is
learning. Change the milestones and keep going.

Milestones need not be user-level. A systems milestone (a pipeline, an API,
a test harness) can mean nothing to an end user, yet enable the impressive
functions that come later.

## M0: the risk-killer eval (a required milestone)

[Boehm's spiral model](../../lect/spiral.pdf) asks, every loop: what could
kill this project, and what is the cheapest evidence that would tell us?
Your product rides on one hypothesis — the "so what" of your 1b mission
statement. M0 tests it.

Required, and it earns full marks even if the numbers disappoint:

1. State the hypothesis as a measurable claim: metric, threshold, baseline.
2. Build the instrument: a runnable eval script in the repo, wired to CI,
   demonstrated on sample or synthetic data. No users yet? Simulate them,
   and say how.

**Bonus: real evidence.** Point the instrument at reality — pilot users, a
questionnaire, collected traces. Any honest sample beats none. Real data is
how milestone and demo marks reach the top of their range.

**If the eval fails:** that is a spiral review, not a failure. Report the
number, hold the review, record the decision — persevere, re-plan, or
descope — in an issue, and continue. Marks are lost only three ways: no
eval, an eval that cannot possibly fail, or a number the tutor cannot
reproduce.

## The repo

Your repo is public (not NCSU-hosted). It holds no keys or passwords.

Commit often, and merge often. Branches are fine — tools like worktrees
and coding agents make many. But merge that work back promptly: tutors
mark the merged history of the repo, and unmerged work is invisible work.
The merged history must show everyone's contribution.

Tests must exist, covering expected cases and failure cases. 50 tests is
good. 100 is better.

## The bling

The top of your README boasts, with badges. Each badge is live: it comes
from a real service, it shows a real number, and a click leads to the
proof. A dead badge is worse than no badge.

Wanted at the top of README.md:

- Build badge: the build passes.
- Test badge: N tests, passing (e.g. "78% tests passing").
- Coverage badge: the coverage tool's number.
- Style checker badge, code formatter badge, syntax checker badge — one
  each, with the config files for each tool visible in the repo.
- Any other automated analysis tool you run: badge it.
- The teaser video (see "The two videos"), right under the badges.
- DOI badge: register the repo at
  [Zenodo](https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content).
  It looks like this:
  ![Zenodo DOI badge](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.1234567-blue.svg)

**Exemplar:** [Epicourier-Web](https://github.com/sdxshuai/Epicourier-Web),
from Fall '25. Four badges, all informative. Demo video right at the top.
467 commits, 93 test files, and it was so inheritable that the next team
built their Project 3 on it. Make your repo look like that by week one.

## The repo rubric (self-assessed)

Score each row yourself: 0 (none), 1 (a little), 2 (somewhat), 3 (a lot).
Give evidence (a link) for each score. Sum the scores at the bottom.

During the demo, the tutor spot-checks five random rows. A self-score the
evidence does not support costs more marks than an honest low score.

**Teamwork, visible in GitHub:**

| Item | Evidence | Score 0-3 |
|---|---|---|
| Many commits: hundreds by the end is normal for teams that commit small (the exemplar has 467) | GH insights | |
| Commits come from different people | GH insights | |
| Workload is spread over the whole team. One member is often 3x more productive than the rest — fine, but show a track record that everyone contributes a lot | GH insights | |
| Team members work across many parts of the code, not one silo each | GH | |
| Short release cycles: frequent small commits, merged promptly, so everyone can get everyone's work | GH | |
| Whole team uses the same tools: config files in the repo, updated by many different people | repo | |
| Whole team can run the system: the tutor can ask anyone to share a screen and demo on their machine | demo | |

**Issues and discussion:**

| Item | Evidence | Score 0-3 |
|---|---|---|
| Issue reports: there are many | GH | |
| Issues are being closed | GH | |
| Issues are discussed before they are closed (if the talk happened in chat, add a summary to the issue) | GH | |
| A large share of issues relate to handling failing cases: a test fails, an issue opens, a fix closes it | GH | |
| Chat channel / discussion forum exists and is active; the poster QR points at it | link or screenshots | |

**Tests:**

| Item | Evidence | Score 0-3 |
|---|---|---|
| Tests exist: 50 is good, 100 is better; expected cases and failure cases both | repo | |
| Tests are a serious share of the code base (30 percent is common) | repo | |
| Tests run automatically on every commit (CI: GitHub Actions or similar) | badge | |
| Coverage is measured; the badge shows the number | badge | |

**Docs:**

| Item | Evidence | Score 0-3 |
|---|---|---|
| Docs are generated, and the format is not ugly | doc pages | |
| Docs, the WHAT: point descriptions of each class/function, in isolation | doc pages | |
| Docs, the HOW: mini-tutorials with worked examples for the common use cases X, Y, Z | doc pages | |
| Docs, the WHY: the docs tell a story — motivate the whole thing, land a punchline that makes a reader want to use it | doc pages | |
| Teaser video (12–30 s), prominent at the TOP of README beside the badges, showing the features at a glance | README top | |
| Feature walk-through video (2–5 min), linked in README: every major feature, working | README | |

**Standard files and bling:**

| Item | Evidence | Score 0-3 |
|---|---|---|
| README.md: all the badges above, all working when clicked | README | |
| .gitignore: lists what must not enter the repo ([examples](https://github.com/github/gitignore)) | repo | |
| INSTALL.md: how to install | repo | |
| LICENSE.md: rules of use | repo | |
| CODE-OF-CONDUCT.md: rules of behavior ([example](https://github.com/probot/template/blob/master/CODE_OF_CONDUCT.md)) | repo | |
| CONTRIBUTING.md: coding standards, plus tips on how to extend the system without breaking it ([example](https://github.com/probot/template/blob/master/CONTRIBUTING.md)) | repo | |
| Style checker, formatter, syntax checker: config files in repo, badges in README | repo + badges | |
| DOI badge from Zenodo | badge | |
| THIRD_PARTY_LIBRARIES.md (or similar): every dependency, with its license | repo | |
| AI use is visible and disclosed: agent plans, bot configs (e.g. .coderabbit.yaml) live in the repo, plus evidence a human checked the AI's output | repo | |
| **Sum** | | |

## The two videos

1. **Teaser** (12 to 30 seconds): the quick guide to your features. It
   sits prominently at the TOP of the README, beside the badges — the
   first thing a visitor sees. One glance shows what the product does.
   Good repos everywhere carry one — copy that pattern.
2. **Feature walk-through** (2 to 5 minutes): every major feature, shown
   working. Linked in the README, and by QR from the poster.

## The demo

- One live demo (5 minutes) with a tutor. The operator plays the feature
  walk-through video and narrates it, live. The tutor asks questions as
  it plays.
- Keep the software installed and running anyway. If the tutor says
  "show me that for real" — you run it, straight away.
- Scheduling rules: see the [policies](../lect/policies.md).

## The poster

Follow the [poster rules](../1/poster.md). Sell Project 2 to the teams who
must pick a Project 3 codebase: what works today, what four milestones come
next, why this repo is the one to inherit.

## Marks (19 total)

| Marks | For |
|---|---|
| 5 | Live demo: how major, how impressive, does it run |
| 8 | Repo rubric: self-assessment confirmed by spot-checks |
| 4 | Milestones: four or more, major, done. M0 (the eval) must be one of them |
| 2 | Poster |

Also: each student completes a short individual questionnaire on group
work. The link comes via Discord.

## Ways to lose marks

- Not enough tests.
- A badge that does not work when clicked.
- A self-score the evidence does not support.
- A demo that needs setup time.
- Milestones that are dull. Milestones that are impossible.
- No M0 eval; an M0 that cannot possibly fail; an M0 number the tutor
  cannot reproduce.
