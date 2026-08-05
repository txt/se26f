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

# AI and SE Productivity: Peer-Reviewed Evidence (Aug 2026)

## Results

| Study | Venue | Design | Result |
|---|---|---|---|
| Cui et al. 2026 [[doi](https://doi.org/10.1287/mnsc.2025.00535)] [[pdf](https://demirermert.github.io/Papers/Demirer_AI_productivity.pdf)] | Management Science | 3 RCTs, 4,867 devs | +26.08% completed tasks (SE 10.3%) |
| Daniotti et al. 2026 [[doi](https://doi.org/10.1126/science.adz9311)] [[arXiv](https://arxiv.org/abs/2506.08945)] | Science 391:831 | 30M commits, 160k devs | AI writes 29% of US Python; output +3.6% |
| He et al. 2026 [[doi](https://doi.org/10.1145/3793302.3793349)] [[arXiv](https://arxiv.org/abs/2511.04427)] | MSR '26 | DiD, 806 Cursor repos | +28.6% LOC (transient); +30.3% warnings, +41.6% complexity (persistent) |
| Paradis et al. 2025 [[doi](https://doi.org/10.1109/ICSE-SEIP66354.2025.00060)] [[arXiv](https://arxiv.org/abs/2410.12944)] | ICSE-SEIP '25 | RCT, 96 Google devs | 21% faster, p=0.086 adjusted |
| Mohamed et al. 2026 [[doi](https://doi.org/10.1145/3809494)] [[arXiv](https://arxiv.org/abs/2507.03156)] | TOSEM | SLR, 39 studies | quality effect unresolved |
| Butler et al. 2025 [[doi](https://doi.org/10.1109/ICSE-SEIP66354.2025.00034)] | ICSE-SEIP '25 | diary RCT | no change in merged PRs |
| Kumar et al. 2025 [[doi](https://doi.org/10.1109/ASE63991.2025.00043)] | ASE '25 | agents in the wild | ~half of real tasks resolved |

Not peer-reviewed, cite as preprints: METR's 19% slowdown
[[arXiv](https://arxiv.org/abs/2507.09089)] and Peng's 55.8%
[[arXiv](https://arxiv.org/abs/2302.06590)] -- the two most-quoted numbers in
the field.

## Paradis: faster, not better

Sole dependent variable was time-on-task; the paper states outright that code
quality was not explored. Raw 96 vs 114 min is significant (p=.038); adjusted,
21-26% with CI [-0.51, +0.03], **p=0.086**, adjusted R^2=0.095. Hours-coded-
per-day is a bigger predictor (32%) than AI. All moderator hypotheses failed.
Their follow-up (CHI '25 EA, *Creating Benchmarkable Components...*) concedes
the quality instrument doesn't exist.

## SPACE

Forsgren et al. 2021, ACM Queue 19(1) [[doi](https://doi.org/10.1145/3454122.3454124)]
[[free](https://queue.acm.org/detail.cfm?id=3454124)]:
**S**atisfaction, **P**erformance, **A**ctivity, **C**ommunication, **E**fficiency.

Mohamed et al.'s audit: 90% of studies touch >=2 dimensions, only 15% exceed
three; Satisfaction/Performance/Efficiency dominate, Communication and Activity
underexplored, 59% exploratory. So "multi-dimensional" mostly means the two
cheapest -- a survey and a stopwatch. And METR's finding is that the first is
systematically wrong about the second.

## What faster costs

- **Deferred, not avoided.** He et al.: velocity decays, complexity persists.
- **Volume != delivery.** +26% tasks (Cui) vs +3.6% output (Daniotti).
- **Deskilling.** Raised unprompted by Paradis, in a paper reporting a speedup.

Microsoft's CLI telemetry study [[arXiv](https://arxiv.org/abs/2607.01418)]
(+24% merged PRs, sustained 4 months) closes by saying the open question is
quality and the field lacks agreed measures for it.

## The line

Everyone measures Activity and Efficiency because those are the two dimensions
you can instrument without first agreeing what "better" means. So productivity
is being defined by whoever's telemetry is cheapest to collect -- the vendors,
whose logs those are. Same shape as the openness argument.

## Organizational ROI: the null results

Individual gains do not aggregate. Nothing here is peer-reviewed -- flag it.

- **MIT Project NANDA (Jul 2025)**, *The GenAI Divide: State of AI in Business
  2025* [[pdf](https://mlq.ai/media/quarterly_decks/v0.1_State_of_AI_in_Business_2025_Report.pdf)].
  95% of pilots showed zero measurable P&L return against $30-40B invested.
  Basis: 52 interviews, 153 executive surveys, 300 public deployments. A
  preliminary report, not a paper; executives self-reporting on their own
  projects. Widely over-cited.
- **DORA 2025** [[report](https://dora.dev/dora-report-2025/)]
  [[pdf](https://services.google.com/fh/files/misc/2025_state_of_ai_assisted_software_development.pdf)],
  ~5,000 respondents. 2024: AI associated with *reduced* throughput and
  stability. 2025: throughput flips positive, **instability stays negative**.
  They tested "fail fast, fix fast" explicitly -- not supported; instability
  keeps damaging product performance and burnout, potentially negating the
  throughput gain.
- **Faros AI telemetry**, 10,000+ developers: +21% tasks, +98% merged PRs,
  organizational delivery metrics flat. Vendor data, but the shape matches
  He et al. and DORA independently.
- **Demirer, Musolff & Yang (2026)**, *Writing Code vs. Shipping Code*,
  NBER WP 35275 [[link](http://www.nber.org/papers/w35275)].

Mechanism is queueing, not mystery: generation capacity roughly doubled,
review/test/integration capacity did not. The surplus becomes WIP, then
instability (DORA), then complexity (He et al.).
