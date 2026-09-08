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


# N6 Exercise: Same Spec, Same Designs, Different Verdicts

Homework, with your team, before next class (~30 quiet minutes).
Bring one sheet: your two scorecards, your verdict, and one LLM
hallucination you caught. Sheets go up side by side at the top of
next lecture.

Everyone judges the SAME two designs. Teams differ only in their
assigned weights — so when verdicts differ next week, we will know
exactly why. That is Shaw's point in its purest form: the systems
stand still; the trade-offs move.

## The one-page spec (same for everyone)

Food delivery, the domain you know from proj1. The system must:

- take orders (customer <-> restaurant menu)
- dispatch couriers (assign, track, reroute)
- move money (charge, refund, courier pay)
- notify everyone when anything changes
- survive Friday 6pm (10x weekday load, briefly)
- change fast: pricing rules and promo logic change weekly

The goals you will weigh:

| goal | means |
|---|---|
| G1 simplicity | 4 people can hold the whole design in their heads |
| G2 responsiveness | courier sees a reroute in under a second |
| G3 peak scale | Friday 6pm survives |
| G4 changeability | weekly pricing changes stay inside one module |
| G5 debuggability | one person can trace one order end-to-end |
| G6 partial failure | payments down does not mean ordering down |

## The two candidate designs (given; do not redesign them)

**Design M — the layered monolith.** One deployable. Requests flow
down, data flows back up. Pricing is a module inside Business
Logic.

```
[ Web/Mobile UI ]
       |
[ Business Logic: orders | dispatch | pricing | notify ]
       |
[ Data Access ]
       |
[ one database ]
```

**Design E — the event bus.** Five small services that never call
each other; every state change is an event on the bus; each
service owns its own data.

```
[UI] -> [Orders] -> ((event bus)) <- [Dispatch]
                     ^   ^    ^
              [Payments] [Pricing] [Notify]
        (each service: own small database)
```

## Part 1: your weights

Your priority profile was assigned in class (teams differ on
purpose):

- **Profile A**: G1, G5 high; G3 low. (The seed-stage bet)
- **Profile B**: G3, G6 high; G1 low. (The we-got-funded bet)
- **Profile C**: G2, G4 high; G3 medium. (The ops-heavy bet)

## Part 2: the scorecards

Fill this table TWICE, once per design. Every cell needs a
one-line evidence phrase that cites a box or arrow in the diagram
— "monoliths are simple" cites nothing; "one database = one place
to look (G5+)" cites a box.

| goal | + / − / 0 | evidence (cite a box or arrow) |
|---|---|---|
| G1 | | |
| G2 | | |
| G3 | | |
| G4 | | |
| G5 | | |
| G6 | | |

Then the verdict, two sentences: under YOUR weights, which design
wins, and which single goal decided it. (A tie is a legal verdict
if you argue the deciding goal honestly.)

## Part 3: LLM as opposing counsel

N1 prompt pattern (role + evidence + format + no-guess). Paste the
spec, both diagrams, and your weights:

> You are an architect who has killed three systems like these.
> Score each design against goals G1-G6 under these weights: one
> sentence per cell, each citing a specific box or arrow. Then
> declare a winner. Cite the diagram or write UNKNOWN. No
> generalities.

Your job is NOT to accept the critique — it is to grade it. Mark
each LLM sentence TRUE (cites a real box, real consequence),
VAGUE (true of any design — "microservices add complexity"), or
WRONG (misreads a diagram, invents a trade-off). At least one
VAGUE or WRONG goes on your sheet, quoted. Did the LLM's winner
match yours? If not, whose evidence was better?

## Part 4: the reveal (in class, next week)

The scorecards go up as a grid — same designs, same rows, three
weight profiles. The comparisons are now mechanical:

- Read across one goal row: where teams disagree on the SAME cell
  of the SAME design, someone's evidence is wrong — find out
  whose, live.
- Compare verdicts: when profile A picks M and profile B picks E,
  nothing about the designs changed. Only the weights did. Say
  that sentence out loud; it is the whole lecture.
- Hunt the blind spot: any goal every team scored − without
  flagging it in their verdict is the class-wide blind spot.
  Expect it on the exam.

## If your team finishes early

Sketch a Design H (hybrid) that beats BOTH under your weights —
usually a monolith with one seam stolen from E (which seam?). You
have just discovered why real systems are never pure patterns.
