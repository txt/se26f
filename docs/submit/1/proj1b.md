<p align="center">
  <a href="https://github.com/txt/se26f/blob/main/README.md"><img 
     src="https://img.shields.io/badge/Home-%23ff5733?style=flat-square&logo=home&logoColor=white" /></a>
  <a href="https://github.com/txt/se26f/blob/main/docs/lect/policies.md"><img 
      src="https://img.shields.io/badge/Policies-%230055ff?style=flat-square&logo=openai&logoColor=white" /></a>
  <a href="#"><img
      src="https://img.shields.io/badge/Teams-%23ffd700?style=flat-square&logo=users&logoColor=white" /></a>
  <a href="#"><img 
      src="https://img.shields.io/badge/Moodle-%23dc143c?style=flat-square&logo=moodle&logoColor=white" /></a>
  <a href="https://discord.gg/zrsW8F2V9"><img 
      src="https://img.shields.io/badge/Chat-%23008080?style=flat-square&logo=discord&logoColor=white" /></a>
  <a href="https://github.com/txt/se26f/blob/main/LICENSE.md"><img 
      src="https://img.shields.io/badge/©%20timm%202026-%234b4b4b?style=flat-square&logoColor=white" /></a></p>
<h1 align="center">:cyclone: CSC510: Software Engineering <br>NC State, Fall '26</h1>
<img src="https://raw.githubusercontent.com/txt/se26f/refs/heads/main/etc/img/se26f.png">

**Links:** [Home](../../../README.md) · [Project 1a](proj1a.md) ·
[Poster rules](poster.md) · [Use case format](usecases0.md) ·
[Prior projects](https://drive.google.com/drive/u/2/folders/1dGGQNCWC3BakD-nUZn5vPecPdm0KAhXA)

**Due:** see the [schedule](../../../README.md).
**Hand in:** two PDFs, uploaded to Moodle: one report, one poster.

## Goal

You know the product now (Project 1a). Propose a better one. Make it different
from everything else on the market.

You are free to dump the Project 1a product and strike out in a completely
new direction. New product, new language, new stack — all allowed. Project 1a
taught you how to read a system and test it. Spend that skill wherever you
want.

## What to do

1. Survey the market. Find the products most similar to yours. List what they
   do, and what none of them do.
2. Propose version i+1: a better product that fills that gap.
3. Say why your version is better. The **why** (the challenge), the **what**
   (the thing you build), the **so what** (the benefits).
4. Make one poster that sells it. Full requirements: [poster.md](poster.md).

Use an LLM as your analyst. But you steer. It brainstorms; you decide.

## Twelve starter prompts

Twelve prompts that can give insight. Note the pattern in all of them: give
the LLM a role, paste real evidence, demand a fixed output format, and forbid
guessing. In every prompt, also state the hard constraint: **we have one
month to build AND test this new thing.** An LLM that does not know the
budget will design you a two-year product. **Warning: these are not
enough.** They are starters. The higher scores go to teams that invent
better prompts of their own. Be creative.

**1. Map the competition.**

```
You are a market analyst. Our product, in one paragraph:

<paste your one-paragraph product description>

List the ten closest competing products. Output a table: product | who uses
it | main strength | main weakness | price | evidence URL.

Rules: no invented products. If you are not sure a product exists, leave it
out. If you cannot support a claim, write "unknown" — do not fill the cell
with something plausible.
```

**2. Mine the complaints.**

```
Below are real user complaints about products like ours: top issues from
their trackers, review excerpts, forum posts.

Cluster these complaints into themes. Rank the themes by frequency times
severity. For each theme: quote one complaint verbatim as evidence, and say
whether any current product has fixed it. The unfixed themes are our
opportunity list.

<paste issues / reviews / forum posts you collected>
```

**3. Table stakes or differentiator?**

```
Here are our 20 use cases from Project 1a:

<paste the 20 use case names, one line of summary each>

Classify each: TABLE STAKES (every rival has it; we must too) or
DIFFERENTIATOR (rare or absent in rivals). One sentence of justification
each — name the rival that has it, or state that none does.

Then propose two use cases that appear in NO current product but follow
naturally from ours. For each: who wants it, and why nobody has built it yet.
```

**4. The support material we have not read yet.**

```
We are designing <product X> for <domain>. We know the code. We do not yet
know the world around it.

What support material would change this design if we read it? Make a LONG
list. Consider at least:
- Laws and regulations: privacy/data protection, consumer protection, tax,
  labor law (gig workers?), food/health codes, financial rules.
- Standards: accessibility (WCAG/ADA), security (OWASP), safety standards,
  relevant ISO/IEEE standards.
- Licenses: of our dependencies, of the data we use.
- Domain knowledge: medical, legal, or professional practice guides that
  govern our users' work.
- Human factors: advice on managing people, teams, and on-call load that
  our product will impose on its operators.

For each item: name a real, findable source; one sentence on which of our
use cases it touches; and rate it MUST-READ / SHOULD-READ / SKIM. We will
read the must-reads and cite them in the report.
```

**5. Who else is in the room?**

```
Our stakeholders so far: customer, staff, admin.

That list is lazy. Extend it. Consider: who pays, who profits, who is
harmed, who is ignored, who regulates, who maintains this at 3 a.m., who
gets sued when it fails, whose job changes because it exists.

For each new stakeholder: what they fear about our product, and one design
decision that would win them over. Output as a table.
```

**6. Three futures.**

```
Our product: <one paragraph>.

Propose three versions: SAFE (obvious next step), BOLD (a real bet), and
WILD (probably wrong, but instructive). For each:
- Elevator pitch, two sentences.
- What four students could build AND test of it in one month.
- The biggest risk.
- The kill signal: "we abandon this version if we see ___."

Do not blend them into one compromise. Keep the three futures distinct.
```

**7. The gap, with receipts.**

```
We claim this market gap: <state the gap in one sentence>.

Interrogate the claim.
- What evidence would CONFIRM the gap is real? List five findable items
  (reviews begging for it, dead products that tried, forum threads,
  competitor roadmaps that dodge it).
- What evidence would REFUTE it (an existing product we missed, evidence
  that nobody wants it)?
- For each item, mark FOUND (with source) or NOT FOUND.

If the refuting evidence wins, say so plainly. A dead gap found this week is
cheaper than one found at the poster session.
```

**8. Mission statement, minus the buzzwords.**

```
A mission statement gives the WHY (the challenge), the WHAT (the thing we
build), and the SO WHAT (the benefit). Example of the form:

<paste the Sentiment Analyzer example from poster.md>

Facts about our product:
<paste bullet-point facts: users, problem, features, stack>

Write three candidate mission statements, five sentences each. Banned words:
leverage, empower, seamless, revolutionize, cutting-edge, innovative,
solution. Each candidate must contain one concrete detail a rival could not
copy-paste. We will pick one and edit it.
```

**9. Milestone reality check.**

```
The team: four graduate students, one month to build AND test, roughly ten
hours per person per week. Skills: <list them honestly>.

Our draft milestones:
<paste the milestone list>

Classify each: REALISTIC / STRETCH / FANTASY, with one sentence of why,
judged against the hours above — not against a startup with funding. For
every FANTASY, propose the largest slice of it that would be REALISTIC.
Remember: dull milestones lose marks, impossible ones lose more.
```

**10. Red team.**

```
You are hostile to our proposal. Below: our mission statement, milestones,
and market survey.

Attack on three fronts:
1. Nobody wants it — the need is imagined.
2. They cannot build it — the month is too short, the team too green.
3. Someone does it better — name who.

Make each attack as strong as you honestly can; no strawmen. Then, for each
attack, state what evidence would defeat it. We will go collect that
evidence — or concede the point and change the plan.

<paste mission statement, milestones, market survey>
```

**11. Play to the team.**

```
Here are the skills of the current team members, stated honestly:

- Member A: <languages, frameworks, domains, what they have actually shipped>
- Member B: <...>
- Member C: <...>
- Member D: <...>

Candidate directions for our product:
<paste the directions you are considering — including "dump the old product
and start fresh in a new language">

Given these skills — not the skills we wish we had — what is a good approach?
Answer:
- Which direction lets this team build and test the most in one month? Why?
- Which direction is a trap for this team (needs a skill nobody has)?
- Where one needed skill is missing: is it learnable in a weekend, or should
  we redesign around it?
- Who should own what, so nobody is a bottleneck?
```

**12. The pivot question.**

```
Forget our current plan for a moment. Here are the facts, nothing else:
- The team: four graduate students, skills below, ten hours each per week.
- The budget: one month to build AND test a working product.
- What we learned in Project 1a: <one paragraph — the domain, the code, the
  bugs we found>

Team skills, stated honestly:
<paste the skills list>

Question: is there a DIFFERENT kind of project we should be exploring — one
we have not considered because we anchored on the Project 1a product?

Propose three genuinely different project kinds (different domain, different
user, or different form: CLI vs web vs library vs bot). For each:
- Why THIS team, specifically, would be unusually good at it.
- What one-month build-and-test slice looks like.
- What we lose by walking away from our current plan.

Then answer plainly: stay the course, or pivot? One paragraph. No hedging.
```

## The poster, in short

One standard page (letter or A4). Small fonts OK (4–6 pt). No large empty
areas. Exciting, but professional. It must show:

- Group number and member names.
- Mission statement paragraph (why / what / so what) and the stakeholders.
- URLs or QR codes: repo, discussion forum, live demo.
- Tech stack icons. Small screen snaps.
- Milestones, three groups of 3–5 each:
  - **Before:** what was done before (Project 1a).
  - **Now:** the plan for this month (Project 2).
  - **Future:** what comes after (Project 3).
- A boast about your test cases from Project 1a.

## What to hand in (two PDFs to Moodle)

**PDF 1 — the report**, containing:

| # | Deliverable |
|---|---|
| D1 | Market survey: 3+ rival products, and the gap none of them fill. |
| D2 | Mission statement: why / what / so what, plus stakeholders. |
| D3 | Milestones: before / now / future, 3–5 each, clear goals. Plus the support material (regulations, standards, licenses) your design must respect, with sources. |
| D5 | Prompt report: "the most useful prompts were..." and "the least useful prompts were..." — with the why, for both. |

**PDF 2 — the poster** ([requirements](poster.md)):

| # | Deliverable |
|---|---|
| D4 | Poster quality: sells the project in 15 seconds; all required parts on the page. |

## Report format

- LaTeX only. Use the [ACM template](https://www.overleaf.com/latex/templates/association-for-computing-machinery-acm-generic-journal-manuscript-template/yffvrvzbhhpt).
- Use the two-column header:

```latex
\documentclass[sigconf]{acmart}
```

- The report must be more than four pages.
- Compile to PDF. Submit to Moodle.

## Rubric

Score each deliverable D1–D5:

| Score | Meaning |
|---|---|
| 0 | Missing, or major issues. |
| 1 | Present, but has issues. |
| 2 | Well done. |
| 3 | Exceptional. Rare. |

Fast checks for the marker:

- D1: are the rivals real? Is the gap real, or invented?
- D3: ambitious but codeable? Dull milestones lose marks. Impossible ones too.
- D4: after 15 seconds, do you know what the project is? Would the tech stack
  make a student pick this project?
- D5: prompts beyond the ten starters? Real reflection, or padding?
- Format: ACM two-column LaTeX? More than four pages? If not, cap all scores at 1.
