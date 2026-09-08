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


# N6 Exercise: One Spec, Rival Systems

Homework, with your team, before next class (~40 quiet minutes).
Bring one sheet: your weighting row, your derived design (boxes
and arrows, ~6 boxes), your receipt (the two minuses you
accepted), and one LLM hallucination you caught. Sheets go up
side by side at the top of next lecture.

## The one-page spec (same for everyone)

Food delivery, the domain you know from proj1. The system must:

- take orders (customer ↔ restaurant menu)
- dispatch couriers (assign, track, reroute)
- move money (charge, refund, courier pay)
- notify everyone when anything changes
- survive Friday 6pm (10× weekday load, briefly)
- change fast: pricing rules and promo logic change weekly

And the trade-off sheet — you cannot have all six; weight them:

| goal | weight (H/M/L) |
|---|---|
| G1 simplicity (4 people can hold it in their heads) | |
| G2 responsiveness (courier sees reroute in <1s) | |
| G3 peak scale (Friday survives) | |
| G4 changeability (weekly pricing changes stay one-module) | |
| G5 debuggability (one person can trace one order end-to-end) | |
| G6 partial failure (payments down ≠ ordering down) | |

## Part 1: weight, then derive

Your priority profile was assigned in class (teams differ on
purpose):

- **Team profile A**: G1, G5 high; G3 low. (The seed-stage bet)
- **Team profile B**: G3, G6 high; G1 low. (The we-got-funded bet)
- **Team profile C**: G2, G4 high; G3 medium. (The ops-heavy bet)

Now do the Shaw move: DERIVE the architecture from the weights.
Use the N4 catalog (layered monolith, event-driven, microkernel,
client-server, pipe-filter, microservices). Expect roughly:

- A-ish weights → a layered monolith derives itself
- B-ish weights → events and service seams derive themselves
- C-ish weights → a monolith with a plug-in pricing microkernel

If your derivation surprises you, good — argue from the columns,
not the fashion. Draw it: ~6 boxes, arrows labeled with WHAT
crosses them (data, events, money).

## Part 2: the receipt

Shaw's law: every design is a purchase. Write the receipt — the
two goals your design scores WORST on, and the concrete symptom
("G5: an order touches 4 services; tracing needs correlation IDs
we have not built"). A design with no admitted minuses is a design
nobody analyzed.

## Part 3: LLM as opposing counsel

N1 prompt pattern (role + evidence + format + no-guess). Paste your
weights, your boxes, your receipt:

> You are an architect who has killed three systems like this one.
> Attack this design: for each goal G1-G6, state whether this
> architecture helps or hurts, in one sentence citing a specific
> box or arrow. Then name the design's most dangerous arrow. Cite
> the diagram or write UNKNOWN. No generalities.

Your job is NOT to accept the critique — it is to grade it. Mark
each of the LLM's sentences: TRUE (cites a real box, real
consequence), VAGUE (true of any design — "microservices add
complexity"), or WRONG (misreads the diagram, invents a trade-off).
At least one hallucinated or vague trade-off goes on your sheet.
(N3's rule, standing: verify citations. The table argues back; you
still preside.)

## Part 4: the reveal (in class, next week)

Sheets go up side by side. The point appears by comparison: SAME spec,
different weights, different — defensible — systems. There was
never one right answer; there was only ever the trade-off sheet.
Ask: which minuses did every team accept without noticing? That
one is the course-wide blind spot; expect it on the exam.

## If your team finishes early

Re-run Part 3 with the robot spec (sense, plan, act, do not fall
down stairs) and your same weights. Which of control loop, layered,
blackboard falls out? You have now used one method on two domains —
that method, not any diagram, is tonight's takeaway.
