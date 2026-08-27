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

# Project 3: Maintain

**Links:** [Home](../../../README.md) · [Project 2](../2/proj2.md) ·
[Poster rules](../1/poster.md) · [Policies](../lect/policies.md)

**Due:** see the [schedule](../../../README.md). Submission is
online, over Thanksgiving break — and no late marks are lost until
Dec 1.
**Hand in:**

1. One PDF to Moodle: your poster, plus the URLs of (a) the Project 2 repo
   you extended and (b) your fork with the new work.
2. Also drop your poster PDF into the shared
   [Project 3 poster folder](https://drive.google.com/drive/folders/14dyoBNX7DY6IIdb8vIo9loqiPqagiBop?usp=drive_link).
   These posters become the sample library for future classes.

## Goal

Extend another team's Project 2 code. Deliver four (or more) additional
major, impressive milestones.

Most of software engineering is this: make someone else's code do new
things, without breaking the old things. Project 3 is that skill, marked.

## Scope

- You must build on another team's Project 2. Part of your mark is how
  well you extended *their* work.
- You are not bound by their roadmap. If you see a better direction, go
  there. But extend — do not rewrite from zero.
- Commit often, and merge often, on your fork. Branches are fine —
  worktrees and coding agents make many. Merge that work back promptly:
  tutors mark the merged history, and unmerged work is invisible work.
  The fork point separates their work from yours.
- Old tests keep passing. Add new tests for the new work: 50 is good,
  100 is better.
- Their M0 eval (the business-level acceptance test from
  [Project 2](../2/proj2.md)) must still run, and its number reported.
- State one new M0 claim for your delta — same rules as Project 2:
  instrument required, real data is bonus.

## Warning: trust nothing

We anticipate that half of the Project 2 projects will not work as
advertised. Posters oversell. Demo videos show the one path that works.

So assess your chosen Project 2 code as soon as possible: build it, run
it, run its tests, poke its dark corners. If it cannot carry your
milestones, decide fast — pick another Project 2, now, not in week three.
An early switch costs one afternoon. A late switch kills the project.

## First week

1. Pick a Project 2 repo. Shop in the
   [Project 2 poster folder](https://drive.google.com/drive/folders/1sl6olGqGQmaa9V4D2iFsTbfB2f1lza1Q?usp=drive_link)
   and watch the demo videos.
2. Fork it. Build it. Run it. Run their tests.
3. Triage: what is solid, what is fragile, what do their tests miss?
4. Then plan your four milestones.

## The two videos

1. **Teaser** (12 to 30 seconds) at the TOP of the README: one glance
   tells a stranger what the product is now.
2. **Feature walk-through** (2 to 5 minutes), linked in the README: the
   delta since the fork — what works now that did not work before.

## The demo

- One live demo (5 minutes) with a tutor. The operator plays the
  walk-through video and narrates it, live: what we inherited, what we
  added, how we know the old parts still work. The tutor asks questions
  as it plays.
- Keep the software installed and running anyway. If the tutor says
  "show me that for real" — you run it, straight away.
- Scheduling rules: see the [policies](../lect/policies.md).

## The poster

Follow the [poster rules](../1/poster.md). Show the before and the after:
what you inherited, what you added, what could come next.

## Marks (21 total)

| Marks | For |
|---|---|
| 5 | Live demo: does it run, is the delta visible |
| 10 | Extension quality: old code respected, old tests still pass, the delta since the fork point is clear, their design understood |
| 4 | Milestones: four or more new ones, major, done |
| 2 | Poster |

No repo rubric for Project 3. The Project 2 rubric already shaped the
repo; the tutor checks only the delta.

Also: each student completes a short individual questionnaire on group
work. The link comes via Discord.


## The four dimensions (announced Aug 26)

Markers read this project through four class-derived dimensions
(built, via repertory grids, from your own poster reviews):

1. **Presentation** — does the poster/report sell it in 15
   seconds?
2. **Engineering evidence** — tests, coverage, runs shown, not
   claimed.
3. **Audience & market** — who is this for, and is that stated
   and plausible?
4. **Originality & impact** — what here is new, and who benefits?

Marks and components stay as printed above; these dimensions are
how the quality rows are interpreted.

## Ways to lose marks

- An unimpressive extension: Project 2 plus a few small touches. The new
  milestones must matter.
- Not enough tests.
- Old tests that no longer pass.
- New work tangled into old code, so nobody can tell what you added.
- A rewrite wearing an extension's clothes.
- The inherited M0 eval abandoned, or no M0 claim for the new work.
- A demo that needs setup time.
