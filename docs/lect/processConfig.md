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


# N7: Process + Config Mgmt

**Links:** [Home](../../README.md) · [Project 2](../submit/project.md) ·
[git101](git101.md) · [N5 testing](n05.md) · [N6 patterns](n06.md)

Build month, week two. You asked for "git beyond push and pull".
Tonight delivers that — but wrapped in the bigger idea it belongs
to. **Process** is the set of rules a team runs by: who may change
what, when work is reviewed, when it ships. **Configuration
management** is the machinery that remembers and enforces those
rules: version control, branches, protections, and the pipelines
that test every change. Process is the law; config management is
the police.

N6 taught that every design is a purchase. Same for process: every
rule you adopt buys you something (safety, speed, evidence) and
bills you for it (delay, ceremony, merge pain). Tonight: the
classic purchases, what they cost, and the exact process a
four-person team with coding agents should run for proj2 — where,
recall from N5, the marks are for HISTORY: CI green from day one,
pull requests moving, commits from every member.

The 2026 twist: LLM agents write branches faster than you can read
them. That does not make process optional. It makes process the
only thing standing between you and a repo full of confident slop.

---

## 0. Waterfall vs Agile (15 min) ▪▪▪▪▪▪

Two extremes of process. One emphasizes planning and control, the
other adaptation and feedback.

![image](https://github.com/txt/se23/assets/29195/52c259a7-f480-422e-8f0a-b0acb33cfc8f)

**Waterfall**: a linear sequence — requirements, analysis, design,
code, test — with feedback flowing only backward, one step at a
time. Strong fit for long, predictable projects. Benefits:
efficiency, predictable costs, payment milestones the accountants
can sign. Weaknesses: rigidity, costly pivots, analysis paralysis.

**Agile** (Scrum as the example): short cycles called *sprints* —
weeks, not years. Each sprint the team reviews the backlog, picks
the tasks of highest value, delivers fast. Daily stand-ups ask
three questions: what did you finish, what is next, what is
blocking you? Benefits: flexibility, early feedback, visible
progress. Weaknesses: risk of losing direction, messy
architecture, budget creep.

When to pick:

- Waterfall: big government and military contracts; well-defined
  requirements; staged payments.
- Agile: small trusted teams; evolving requirements; when feedback
  is allowed to change the goals.

Warning signs:

- Waterfall failing: a mid-project pivot forces re-engineering of
  signed-off stages; testing at the end reveals flaws that were
  cheap to fix in month two and ruinous in month nine.
- Agile failing: endless churn; an architecture collapsing under
  too many fast changes (N6's smells, at team scale).

![image](https://github.com/txt/se23/assets/29195/78ceea76-1e54-44fa-9cbd-b333870545b2)

Notice where this course sits: proj1 was a mini-waterfall
(requirements, then proposal, then build) and proj2 is a month of
sprints with a weekly stand-up — your team meetings. You are
running both, which is what most real teams do, whatever label
they put on it.

---

## 1. Release cycles: short vs long (10 min) ▪▪▪▪

Release cadence is the same trade-off wearing a calendar.

**Short cycles**: frequent updates, quick feedback, customers see
progress often. Danger: rushed code, technical debt piling up
(your DEBT.md from N6 exists to track exactly this), APIs breaking
under users' feet.

**Long cycles**: years between major versions; big integrated
features; careful planning. Danger: feedback arrives too late,
"big bang" releases full of bugs, the market drifts away while you
polish.

When to pick:

- Short: requirements evolve, users want frequent updates.
- Long: requirements are fixed, or the system is safety-critical.
- Mixed — the common industrial answer: frequent internal
  releases, slower external milestones.

Warning signs:

- Short failing: debt piles up, no refactoring time, brittle
  design.
- Long failing: giant buggy releases; users lose interest before
  you ship.

Safety-critical adaptation: careful release branches, strong local
checks before anything leaves a developer's machine, broad test
environments, canary releases (ship to a small slice of users
first, watch, then widen). Slow is a feature when a bug is a
lawsuit.

For proj2: your external cycle is fixed (demo Oct 21). Run a short
internal cycle inside it — something merged and green every few
days. A team that integrates weekly discovers merge hell with two
weeks to spare; a team that integrates in the last week discovers
it on stage.

---

## 2. Branching: Git Flow vs commit-to-main (10 min) ▪▪▪▪

Version control strategy is process made executable. Two classic
camps:

![image](https://user-images.githubusercontent.com/29195/130551409-89d30647-a72f-4321-b58f-f519c77235ce.png)

**Git Flow**: every feature gets a branch; branches merge only
after vetting; main is protected from mistakes. Benefits: trust
but verify, a clear history, nothing lands unreviewed. Weaknesses:
bottlenecks — work queues up behind reviews; long-lived branches
drift from main and merge day becomes archaeology.

**Commit to main** (trunk-based): all work merges quickly into the
main branch — the "trunk" — and automated testing guards
stability. Benefits: fast iteration, no merge hell, everyone sees
everyone's work within hours. Weaknesses: demands a strong test
culture; one untested commit breaks everybody.

When to pick:

- Git Flow: large projects, many strangers contributing — most big
  open-source repos.
- Trunk-based: fast-moving teams with testing pipelines they
  actually trust — Google famously runs most of its code in one
  trunk.

Warning signs:

- Git Flow failing: stalled pull requests; a branch two weeks old
  (its merge will be a second implementation effort).
- Trunk failing: flaky builds, red main, people afraid to pull.

The honest middle, and the one this course mandates (git101, stage
2): **short-lived branches plus pull-request review** — branches
measured in days not weeks, merged into a protected main. That is
Git Flow's safety with trunk-based speed, and it is what most
industrial teams actually run.

---

## 3. Branching in the agent era (10 min) ▪▪▪▪

Here is what changed since those two camps formed: coding agents
made branches nearly free to *produce*. One prompt, one worktree,
and an agent commits for an hour without you. Recall git101 stage
3 — a **worktree** is a second working directory on its own
branch, sharing one repository, so several lines of work proceed
at once without collisions:

```
git worktree add ../wt-a1 -b agent1    # sandbox + branch for agent 1
git worktree add ../wt-a2 -b agent2    # a second, in parallel
...                                    # agents work; you work on main
git diff main...agent1                 # YOU review before anything merges
```

What agents change about branching practice:

1. **Branches multiply.** Four students could run eight agent
   branches before lunch. The scarce resource is no longer writing
   code; it is reviewing it. Design your process around review
   bandwidth.
2. **Branch lifetime must shrink.** A human can rebase a stale
   branch thoughtfully; an agent asked to fix conflicts will
   happily regenerate half the file (N6: duplicated code is the
   smell LLMs mass-produce). Merge small, merge often, delete the
   branch after merging.
3. **CI becomes the first reviewer.** Do not spend human eyes on a
   branch until the machine says the tests pass. Red branch, no
   review — send it back to the agent with the failing output.
4. **Agents never touch main.** An agent with your credentials can
   run `git push` as easily as you can. The protection rules of
   section 5 are the fence that holds even when the author is a
   process running at 2 a.m. — which is precisely when you want a
   fence.
5. **Name branches so the history reads.** `agent1` tells the
   tutor nothing; `agent/fix-pricing-rounding` is an audit trail.

The discipline has not changed since git101: branch, diff, review,
merge. The agent is the author; you are the reviewer; never skip
the diff. An agent that grades its own work converges on slop.

---

## 4. Team boundaries (7 min) ▪▪▪

Who may change what?

**Zero internal boundaries**: everyone uses the same tools and may
modify any code. Great for open projects and shared
responsibility. Danger: chaos when tools and configs are not
consistently available — "works on my machine", four times over.

**Specialized teams**: deep experts own small subsystems.
Efficient while nobody needs to cross a boundary. Danger:
developers blocked, waiting on another owner's queue just to make
their own code work.

When to pick:

- Zero boundaries: public and open projects, shared tooling,
  flexible contributors.
- Specialized: genuine super-specialists exist and the interfaces
  between subsystems are stable.

Warning signs:

- Zero boundaries failing: missing tools, config chaos, two people
  silently rewriting the same module.
- Specialized failing: progress stalls on cross-dependencies; the
  pester count (N4's one-question architecture check) goes through
  the roof.

For four people: zero boundaries for reading and reviewing —
anyone reviews anything — but one *owner* per module for writing
(git101 rule 1: one directory, one owner). That is Conway's law
run on purpose: four work-streams, thin agreed interfaces, and the
interfaces are where the pestering is allowed.

---

## 5. CI/CD basics (15 min) ▪▪▪▪▪▪

Three terms, often blurred, worth keeping sharp:

- **Continuous integration (CI)**: every pushed change is
  automatically built and tested, and the result is visible to the
  whole team within minutes.
- **Continuous delivery (CD)**: the code is kept permanently
  releasable; shipping is a button press, not a project.
- **Continuous deployment**: no button — every change that passes
  the pipeline goes straight to users.

Proj2 requires the first; understand all three.

You met the machinery in N2. GitHub Actions knows nothing about
your project except one number — the exit code of a command. Zero
means green; anything else means red:

```yaml
# .github/workflows/test.yml
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install pytest
      - run: pytest -q
```

Get the mechanics exactly right, because exam questions live here:

- **Actions run AFTER the push**, on GitHub's servers — a fresh
  virtual machine per run that checks out your code, runs your
  commands, and reports the exit code. CI cannot stop a bad commit
  from being pushed; it can only make the badness visible, fast,
  and (next section) block it from *merging*.
- **Hooks run BEFORE, on your machine.** A pre-commit or pre-push
  hook is a local script in your repo's `.git/hooks/` directory
  that runs when you commit or push and can abort the action.
  Hooks are not copied by `git clone` — each teammate (and each
  agent sandbox) must install them — which is why teams trust
  server-side CI as the real gate and treat hooks as a personal
  convenience that saves round-trips.
- **The pipeline is itself versioned.** The yaml lives in the
  repo, so process changes go through the same review as code
  changes. That is configuration management eating its own cooking.

Rules of CI hygiene, learned expensively everywhere:

1. Red main is a stop-the-line event. Whoever broke it fixes or
   reverts within the hour; everyone else stops pulling.
2. Keep the pipeline fast — under ten minutes, or people stop
   waiting for it and start ignoring it (N5's budgeted-testing
   lesson: prioritize, and quarantine flaky tests rather than
   letting them train the team that red means nothing).
3. A red run on a *branch* is not shame; it is the system working.
   Failures are findings — CI exists to find them before your
   users, your teammates, or your tutor do.

---

## 6. Branch protection + code review as process (15 min) ▪▪▪▪▪▪

CI makes failure visible. **Branch protection** makes the rules
mechanical: settings on the server that constrain what may land on
a branch, no matter who pushes — tired human, confident agent, or
you at 2 a.m. On GitHub: repo Settings, then Branches, then add a
rule for `main` (free for public repos):

| Setting | What it enforces |
|---|---|
| Require a pull request before merging | Nothing lands on main directly; all work arrives via PR |
| Require one approving review | A human who is not the author read the diff |
| Require status checks to pass | The CI workflow above must be green before merge |
| Block force pushes | History cannot be silently rewritten |

Ten minutes of clicking turns your team's stated process into
physics. "We always review" is a hope; a protected branch is a
fact. And it is tutor-visible fact: a blocked merge in your
history proves the process ran.

**Live exercise (10 min of this section).** Volunteer team, on
screen: add the protection rule to your proj2 repo; open a PR from
a branch with a deliberately failing test; watch the merge button
lock; fix the test; watch it unlock; teammate approves; merge.
Everyone else: do this on your own repo this week — the
screenshots are the "before next class" work.

**Code review as process.** Review is not a favor between friends;
it is a pipeline stage with known mechanics:

- **Small diffs or no review.** Past a few hundred changed lines,
  approval rates stay high while defect-finding drops — reviewers
  skim what they cannot hold in their head. Big change? Split the
  PR.
- **Review the behavior, not the formatting.** A linter in CI
  argues about style so humans do not have to. Human eyes go where
  machines cannot: wrong requirement, missing test, hidden
  coupling (N4), a pattern wearing a costume (N6).
- **Author prepares the review.** PR description says what changed
  and why, points at the risky part, links the issue. A reviewer
  spending ten minutes reconstructing intent is process waste.
- **Agent code gets the same gate, applied harder.** The N2 rule —
  never accept claimed execution — is now team law: the PR shows
  the tests running in CI, or the PR waits. Reviewing agent output
  is a skill your projects grade: the D5 prompt reports reward
  caught LLM errors, and review is where you catch them.

---

## 7. Strange but sensible process decisions (5 min) ▪▪

When you reach industry you will meet process that looks insane.
Some of it is. Some of it survives for reasons nobody wrote down:

- **AgileFall**: companies that *say* agile but *do* waterfall —
  sprints on the wall, signed-off requirements in the drawer.
- **Payment milestones**: accountants demand staged sign-offs, so
  a waterfall skeleton persists inside an agile shop, because
  invoices need stages.
- **Paperwork overload**: documents that exist for contracts and
  accountability, not engineering love.

Lesson: process often follows politics, money, and risk — not
textbook merit. Before you mock an old rule, find out what it is
load-bearing for. Then, sometimes, mock it anyway.

---

## 8. Research corner (READ AT HOME)

Two honest data points. (1) The DORA studies ("Accelerate",
Forsgren, Humble, Kim 2018, and yearly reports since): across
thousands of organizations, teams that deploy *more* often also
break *less* often and recover faster — speed and stability
correlate, they do not trade off. Short cycles with strong
pipelines beat careful-and-slow on both axes. (2) Bacchelli and
Bird (ICSE 2013), studying code review at Microsoft: developers
say review is for finding defects, but measured outcomes are
mostly knowledge transfer, shared ownership, and better designs —
fewer bug-catches than expected. Moral for your team: review
still pays, but its biggest dividend is four people who each
understand all of the repo. Budget review time as learning time,
not just defect hunting.

---

## Before next class

N8 (Oct 07) opens with a live repo triage — a volunteer team's
proj2 repo on screen, read the way a tutor reads it. Arrive with:

1. Branch protection on your proj2 main: PR required, one
   approving review, status checks required. Screenshot the
   settings page.
2. The CI workflow from section 5 (adapt the install line to your
   project) green on main. Then break a test on a branch, open a
   PR, screenshot the blocked merge, fix, merge. That PR is your
   evidence the pipeline gates for real.
3. A `PROCESS.md` in your repo, under ten lines: your branch
   naming rule, who reviews, your definition of "done" (tests?
   issue linked? CI green?), and your red-main rule. Write the
   process you will actually follow, not the one that sounds
   grand.
4. Run one coding agent in a worktree on a real proj2 task. Merge
   its work through a PR a teammate reviews. In the PR
   description, one sentence: what the agent got wrong before you
   caught it. (Nothing wrong? Say what you checked. "I did not
   look" is the only failing answer.)

## Review questions

1. (a) Define continuous integration, and state where and when a
   GitHub Actions workflow runs relative to a `git push`.
   (b) A team's CI badge has been green for three weeks, yet
   bugs their tests should catch keep reaching main. Their
   workflow is below. Find the line that makes the badge lie, and
   explain what GitHub sees because of it. (Recall: Actions judges
   a run by one thing — the exit code of each step, where zero
   means success.)

```yaml
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install pytest
      - run: pytest -q || true
```

2. (a) Name two things branch protection can require before a pull
   request merges into main.
   (b) A teammate proposes: "Skip branch protection — we are
   disciplined, and it slows the agents down." Using section 3,
   give the one scenario where discipline cannot substitute for
   the server-side rule.

## Reflection

1. Your team is behind with ten days to the proj2 demo. One member
   wants to drop reviews and commit straight to main "just until
   the demo". Price that purchase both ways: what it buys this
   week, what it can cost on demo night — then write the rule you
   would actually adopt.
2. Google runs trunk-based; the Linux kernel runs long-vetted
   branches through maintainer review. Both are elite. Name the
   difference in their situations (who contributes, what testing
   they trust) that makes each choice right where it stands.
3. Agents made writing branches cheap and left reviewing them
   expensive. Which single rule from tonight protects the scarce
   resource best on YOUR team — and what would you measure in two
   weeks to know if it worked?
