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

# Test 101: testing a model, from assert to CI

**Links:** [Home](../../README.md) ·
[live code: sd0.py](https://github.com/txt/se26f/blob/main/docs/lect/brooks/sd0.py) ·
[test_brooks.py](https://github.com/txt/se26f/blob/main/docs/lect/brooks/test_brooks.py) ·
[useCaseTesting](n02.md) · [Proj1a](../submit/1/proj1a.md)

One 50-minute pass: twelve heuristics, one case study, one set of
mechanics, two exercises. Anything marked *explore on your own
time* ships with the notes but not the clock.

## 0. Twelve test-design heuristics ▪▪▪▪▪▪▪▪

*(~8 min.)* Before any code: what is even worth testing? Twelve
generic answers. Keep the list beside you for Exercise 1.

1. **Boundaries.** Test at, just below, and just above every edge.
2. **Zero, one, many.** Empty input, single input, lots of input.
3. **Round trips.** Do, then undo: `(a+b)-b == a`.
4. **Invariants.** Things that must hold after ANY operation
   (totals conserved, counts non-negative, output sorted).
5. **Extreme conditions.** Set a parameter to 0 or huge; predict
   the answer from first principles; check it.
6. **Known answers.** Tiny cases you can compute by hand.
7. **A second opinion.** Another implementation, or a formula,
   as the oracle.
8. **Golden runs.** Fix the seed, bless one output, diff forever
   after.
9. **Error paths.** The extensions of your use cases — most real
   requirements hide there.
10. **Monotonicity / direction.** More load never speeds things
    up; work-done never decreases.
11. **Same-seed determinism.** Two runs, same seed, byte-equal.
12. **Crash-free floor.** At absolute minimum: it ran, on every
    input class you claim to accept.

## 1. Case study: Brooks' Law in 70 lines ▪▪▪▪▪▪▪▪▪▪▪▪

*(~12 min.)* "Adding staff to a late software project makes it
later" (Brooks, 1975). [sd0.py](brooks/sd0.py) is the smallest
compartmental simulator that can ask if that is true: an engine
(`o`, `run`, `verdict`) plus one model. The model, every line
commented:

```python
def brooks(d, t, u, v):
  comm  = d["COMM"] * u.D * (u.D - 1) / 2       # n^2 channels: Brooks' core claim
  train = d["TRAIN"] * u.N                      # mentors pulled off the line
  prod  = u.D * max(0, 1 - comm - train)        # net output of the veterans
  v.W  += d["dt"] * prod                        # bank today's work
  v.N  += -d["dt"] * d["MATURE"] * u.N \
          + (d["HIRE"] if t == d["WHEN"] else 0)  # the intervention lands here
  v.D  +=  d["dt"] * d["MATURE"] * u.N          # newbies mature into devs
```

The research question is an experiment: baseline (`HIRE=0`) vs
treatment (`HIRE=10` at tick 10), scored by work banked at the
horizon, judged in the claim's direction:

```python
def y(out):  return out[-1][1].W          # score: work done by tmax

def rq(**kw):
  base  = {**the, **kw, "HIRE": 0}
  treat = {**the, **kw, "HIRE": 10}
  return verdict("adding staff to a late project makes it later",
                 y(run(base, brooks)), y(run(treat, brooks)), "down")
```

Run it, sweeping the horizon:

| tmax | gap (y1−y0) | verdict |
|-----:|------:|---------|
| 10 | +0.0 | neutral |
| 30 | −88.9 | confirm |
| 60 | −32.1 | confirm |
| 70 | −1.2 | neutral |
| 90 | +63.4 | refute |

Same model, same parameters, opposite verdicts. Brooks' Law is a
statement about *when you take the photograph* — the newbies are a
drag until they mature, then they pay you back. And tmax=10 is a
false neutral: the hire lands at tick 10, so the run ends before
the effect exists. A verdict function with no "neutral" band would
score that 0.0 as a confirmation of nothing.

## Exercise 1: what would you test? ▪▪▪▪▪

*(~5 min, pairs, paper.)* You have the twelve heuristics and 70
lines of simulator. Write down five tests — name, one line each,
tagged with the heuristic it uses. Do not write code yet. (Then
compare with the seven in
[test_brooks.py](brooks/test_brooks.py): conservation is #4,
extreme-conditions is #5, monotone work is #10, the crossover is
the case study itself.)

## 2. Forrester's rules ▪▪▪▪▪

*(~5 min.)* Testing simulations is old wisdom. Forrester & Senge
("Tests for building confidence in system dynamics models", 1980)
gave the canonical checklist — note how much of it is our
heuristics wearing 1980s clothes:

1. **Boundary adequacy** — is everything that drives the behavior
   inside the model?
2. **Structure verification** — does each equation match something
   in the real system (n² channels really is how meetings grow)?
3. **Dimensional consistency** — units balance in every equation.
4. **Parameter verification** — every constant means something
   measurable (MATURE=0.08 ≈ a 12-tick apprenticeship).
5. **Extreme conditions** — zero staff must mean zero work; no
   taxes must mean hiring always helps.
6. **Behavior reproduction** — does it reproduce the known story
   (the late-project dip)?
7. **Surprise behavior** — when the model does something odd (the
   crossover), is that a bug, or a discovery?
8. **Sensitivity** — which parameters flip the verdict? Those are
   the ones to measure carefully in the real world.
9. **Policy sensitivity** — does the recommendation survive
   reasonable parameter changes? (Ours does not survive tmax.)

## 3. Mechanics: Python, pytest, CI ▪▪▪▪▪▪▪▪▪▪

*(~12 min.)* The constructs that carry all of the above:

| construct | testing job |
|---|---|
| `assert` | the check itself (`python -O` strips asserts — tests only, never input-validation) |
| `try/except` + `traceback.print_exc()` | the harness survives red |
| `random.seed(the.seed)` | replayable stochastic tests |
| `sys.exit(n)` | **the only thing CI ever sees** |
| `globals()` + `startswith("test_")` | test discovery |
| `f.__doc__` | the test's description, for free |
| `math.isclose` | float compare: near enough is good enough |

The whole engine of [test_brooks.py](brooks/test_brooks.py), with
the four lines students ask about:

```python
eg = {"-" + k[5:]: f for k, f in globals().items()
      if k.startswith("test_")}

def run1(f):
  random.seed(the.seed)
  try:    f(); return 0
  except Exception:
    traceback.print_exc(); return 1

if __name__ == "__main__":
  fails = 0
  for j, s in enumerate(sys.argv):
    if s == "-all":                 fails += sum(run1(f) for f in eg.values())
    elif f := eg.get(s):            fails += run1(f)
    elif (k := s.lstrip("-")) in the: the[k] = atom(sys.argv[j + 1])
  sys.exit(fails)
```

- `globals()` — a module's namespace is a dict; code can read
  itself. The comprehension harvests every `test_*` function
  (`k[5:]` slices the prefix off; `f` is the function, a value).
- `if f := eg.get(s)` — the walrus: test and bind in one step.
- `s.lstrip("-")` — strips a *character set*, not a prefix, so
  `-tmax` and `--tmax` both work; `sys.argv[j+1]` pairs the flag
  with its value.
- `stop0, the.stop = the.stop, 10` (seen in bigger suites) —
  tuple assignment as save/patch; restore after: setup and
  teardown in one line each.
- `sys.exit(fails)` — without this line, automation cannot see
  your tests at all.

Watch the shell change the science:

```
$ python3 test_brooks.py -all              # 7 PASS, exit 0
$ python3 test_brooks.py -tmax 80 -brooks  # FAIL, exit 1
```

**pytest is this engine, industrialized.** Same discovery rule
(`test_*` in `test_*.py`), bare asserts with rich failure output,
and its own exit code:

```
pytest -q            # run everything
pytest -x            # stop at first red
pytest -k crossover  # run tests matching a name
pytest --lf          # rerun last failures
```

Our file runs under both engines unchanged: `python3 -m pytest -q
test_brooks.py` → `7 passed`.

**CI in seven lines.** GitHub knows nothing about your tests
except one process exit code:

```yaml
# .github/workflows/test.yml
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make test
```

and the `make test` rule it calls
([brooks/Makefile](brooks/Makefile)):

```make
test: ## run all tests; exit nonzero on any failure
	python3 test_brooks.py -all
```

`make test` can be pytest, this engine, a Lua suite, a diff of
golden files — anything that exits 0 on green. That is why seven
lines of yaml test any language ever.

## Exercise 2: extend and wire ▪▪▪▪▪

*(~5 min start in class, finish at home.)* On your Proj1a fork:

1. Add one test born from a heuristic nobody used yet (e.g. #1
   boundaries: `WHEN` after `tmax`; or #11: two `-all` runs,
   identical output).
2. Add a `make test` rule and the seven-line workflow. Push.
   Watch the Actions tab go green — then break a test on a
   branch and watch it go red.

## Explore in your own time

- `doctest`: the examples in your docstrings, run as tests —
  SSOT taken to its logical end.
- `pytest.raises`, fixtures (`tmp_path`, `capsys`),
  `@pytest.mark.parametrize`.
- `unittest.mock`: fake the expensive collaborator.
- Golden-file testing: fix the seed, bless a transcript, `diff`.
- Property-based testing (`hypothesis`): the machine invents
  inputs; you state the invariant.
- Coverage — and its limits: touching a line is not checking its
  meaning.
