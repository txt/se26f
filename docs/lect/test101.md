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
mechanics, two exercises. Anything under *explore in your own
time* ships with the notes, not the clock.

## 0. Twelve heuristics for writing software tests ▪▪▪▪▪▪▪▪▪▪

*(~10 min.)* Before any code: what is even worth testing? Keep
this list beside you for Exercise 1.

1. **No oracle, no test.** If you can't state what "correct"
   means, you're running code, not testing it.
2. **When the exact answer is unknowable, test relations, not
   values.** Metamorphic: shuffle rows → same score ±ε; double
   the budget → cost never worse. Essential for
   stochastic/optimizer/ML code.
3. **Partition, then probe twice.** Cluster inputs by behavior
   signature (coverage bitmap, output vector), not numeric
   nearness. Sample 2 per class — disagreement means the
   partition is wrong; split on the feature that separated them.
   A class probed once is a hypothesis, not a partition.
4. **Order the budget: breadth → edges → mass.**
   Breadth across classes first — one rep per class, max-min
   distance apart (adaptive random testing); diversity buys more
   bug-detection per test than depth. Then boundaries between
   adjacent classes — pairs differing in one condition; most
   defects are off-by-one at partition edges. Then weight by
   size(class) × risk(class) — big classes are common paths,
   small classes are usually the weird ones. (Invert the first
   two only for mature code: fresh code fails mid-class, mature
   code fails at edges.)
5. **Assert invariants, not internals.** Tests coupled to
   structure die at the first refactor.
6. **One failure reason per test.** A test that can fail three
   ways diagnoses nothing.
7. **Fast or ignored.** Whole unit suite under ~10s, or people
   stop running it.
8. **Seed everything, print the seed.** Failure output should be
   a paste-able repro.
9. **Bug report → regression test → then fix.** The test is the
   proof the bug was real. Flaky is a defect in the test:
   quarantine, fix, or delete — never retry-loop.
10. **Coverage is a floor, not a target.** 100% coverage of weak
    assertions tests nothing.
11. **Every knob on the command line, defaulted from the
    docstring.** One config object (`the`), one parse, no hidden
    globals. Tests then differ only in flags — and a failing CI
    run is a copy-paste-able command line. Corollary: the test
    runner is just another flag; exit status = number of
    failures.
12. **Parallelism is a for loop you didn't write.** Tests are
    the embarrassingly parallel case — independent,
    side-effect-free, seed-carried. Don't build a framework;
    shell out:

    ```bash
    seq 20 | xargs -P8 -I{} python3 test_brooks.py -seed {} -all
    ```

    Two rules make it safe: each test owns its temp dir, and
    each carries its own seed. Break either and you've bought
    flakiness that only appears at `-P8`. (11 and 12 are one
    heuristic seen twice: once a test configuration is a command
    line, `xargs` already knows how to run it.)

The shape of a test, in one line:

```python
def eg__sym(): # test = tiny named demo, self-checking, greppable
  s = SYM(["a","a","b"]); assert abs(s.ent() - 0.918) < 0.01
```

### Finding the classes (skim now, use in Proj1a)

True equivalence ("same input class ⟺ same behavior") is
undecidable, so approximate with a surrogate signature, then
refine:

| source | signature | tool |
|---|---|---|
| spec | category × choice tuples | category-partition (Ostrand & Balcer) |
| code | path condition | concolic/symbolic exec (KLEE); or a branch vector |
| behavior | coverage bitmap or output vector | AFL-style feedback; clustering |

For config-vector inputs the behavior route is the practical one:
two configs are equivalent if they produce the same signature —
not if they are numerically near. The refinement loop (the part
people skip):

```python
def classes(pool, sig, k=2):
  D = {}                       # signature -> [inputs]
  for x in pool: D.setdefault(sig(x), []).append(x)
  for s, xs in D.items():      # trust, then verify
    probe = shuffle(xs)[:k]    # 2 reps, not 1
    if len(set(map(oracle, probe))) > 1:
      yield from classes(xs, finer(sig))   # class was wrong: split
    else: yield probe[0]
```

## 1. Case study: Brooks' Law in 69 lines ▪▪▪▪▪▪▪▪▪▪▪▪

*(~12 min.)* "Adding staff to a late software project makes it
later" (Brooks, 1975). [sd0.py](brooks/sd0.py) is the smallest
compartmental simulator that can ask if that is true: a
24-line engine (`o`, `run`, `verdict` — states are stocks with
`[now, lo, hi]` bounds, clamped every tick) plus one model.
The model, every line commented:

```python
def step(dt,t,u,v):
  comm  = u.D*(u.D-1)/2 * 0.0002              # n^2 talk cost, grows with team
  train = u.N * 0.2                           # each newbie steals mentor time
  prod  = max(0, u.D*(1-comm-train)) * 0.5    # net output of the veterans
  v.R   = u.R - dt*min(prod, u.R)             # burn down the backlog
  v.W   = u.W + dt*min(prod, u.R)             # ..and bank it as work done
  v.N   = u.N - dt*0.1*u.N + (u.HIRE if t==u.WHEN else 0)  # hire once, then age
  v.D   = u.D + dt*0.1*u.N                    # 10%/tick of newbies turn veteran
```

The research question is an experiment: same world, one knob
moved. Baseline `HIRE=0` vs treatment `HIRE=10` at tick 10,
scored by work banked at the horizon, judged in the claim's
direction:

```python
def y(out):
  "score a run. higher=better. work banked by tmax, so slower => smaller y."
  return out[-1][1].W                         # last row, its W stock

def rq(bg=None, **kw):
  "the experiment: same world, one knob moved. HIRE is ctrl. kw = run opts."
  bi    = init if bg is None else bg
  base  = {**bi, 'HIRE':[0, 0,50]}            # rx0: nobody added
  treat = {**bi, 'HIRE':[10,0,50]}            # rx1: 10 added at WHEN
  return verdict("adding staff makes it later",
                 y(run(base ,step,**kw)),
                 y(run(treat,step,**kw)), "down")
```

Run it, sweeping the horizon (`python3 sd0.py`):

| tmax | y0 | y1 | gap | verdict |
|-----:|-----:|-----:|------:|---------|
| 10 | 96.2 | 96.2 | +0.0 | refute |
| 20 | 192.4 | 106.8 | −85.6 | confirm |
| 40 | 384.8 | 273.5 | −111.3 | confirm |
| 60 | 577.2 | 533.6 | −43.6 | confirm |
| 70 | 673.4 | 669.3 | −4.1 | confirm |
| 80 | 769.6 | 805.8 | +36.2 | refute |

Same model, same parameters, opposite verdicts. Brooks' Law is a
statement about *when you take the photograph*: the newbies are a
drag until they mature, then they pay you back — the flip is
near tmax≈71.

Two of these rows are lessons in oracle design (heuristic #1):

- **tmax=10 is a false refute.** The hire lands at `WHEN=10`; the
  run stops before any effect exists. The gap is exactly 0.0 —
  yet `verdict()` has no null category, so a not-yet-measurable
  difference reads the same as a genuine contradiction.
- **tmax=70 is a confirm on noise**: gap −4.1 is 0.6% of y0. A
  threshold ("neutral if `abs(gap) < eps`") would catch both.

## Exercise 1: what would you test? ▪▪▪▪▪

*(~5 min, pairs, paper.)* You have the twelve heuristics and 69
lines of simulator. Write down five tests — name, one line each,
tagged with the heuristic each uses. No code yet. Then compare
with the eight in [test_brooks.py](brooks/test_brooks.py):
W+R=1000 and D+N-changes-only-by-HIRE are #5 invariants; the
clamp check is #5 again; monotone W is a #2 relation; the
crossover is a #2 relation over the horizon knob; the
false-refute test is a #4 edge (and a #9 regression: a known
blind spot, pinned).

## 2. Forrester's rules ▪▪▪▪▪

*(~5 min.)* Testing simulations is old wisdom. Forrester & Senge
("Tests for building confidence in system dynamics models",
1980) gave the canonical checklist — much of it is our
heuristics wearing 1980s clothes:

1. **Boundary adequacy** — is everything that drives the
   behavior inside the model?
2. **Structure verification** — does each equation match
   something real (n² channels really is how meetings grow)?
3. **Dimensional consistency** — units balance in every
   equation.
4. **Parameter verification** — every constant means something
   measurable (0.1/tick maturation ≈ a ten-tick
   apprenticeship).
5. **Extreme conditions** — zero staff must mean zero work; a
   burned-down backlog must stop producing (that is the
   `min(prod, u.R)`).
6. **Behavior reproduction** — does it reproduce the known story
   (the late-project dip)?
7. **Surprise behavior** — when the model does something odd
   (the crossover), is that a bug, or a discovery?
8. **Sensitivity** — which parameters flip the verdict? Those
   are the ones to measure carefully in the real world.
9. **Policy sensitivity** — does the recommendation survive
   reasonable parameter changes? (Ours does not survive tmax.)

## 3. Mechanics: Python, pytest, CI ▪▪▪▪▪▪▪▪▪▪

*(~12 min.)* The constructs that carry all of the above:

| construct | testing job |
|---|---|
| `assert` | the check itself (`python -O` strips asserts — tests only, never input-validation) |
| `try/except` + `traceback.print_exc()` | the harness survives red |
| `random.seed(the["seed"])` | replayable stochastic tests (heuristic #8) |
| `sys.exit(n)` | **the only thing CI ever sees** |
| `globals()` + `startswith("test_")` | test discovery |
| `f.__doc__` | the test's description, for free |
| `math.isclose` | float compare: near enough is good enough |

The whole engine of [test_brooks.py](brooks/test_brooks.py) —
heuristic #11, executable — with the four lines students ask
about:

```python
eg = {"-" + k[5:]: f for k, f in globals().items()
      if k.startswith("test_")}

def run1(f):
  random.seed(the["seed"])
  try:    f(); return 0
  except Exception:
    traceback.print_exc(); return 1

if __name__ == "__main__":
  fails = 0
  for j, s in enumerate(sys.argv):
    if s == "-all":                   fails += sum(run1(f) for f in eg.values())
    elif f := eg.get(s):              fails += run1(f)
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
- `sys.exit(fails)` — without this line, automation cannot see
  your tests at all.

Watch the shell change the science:

```
$ python3 test_brooks.py -all              # 8 PASS, exit 0
$ python3 test_brooks.py -tmax 80 -brooks  # FAIL, exit 1
```

**pytest is this engine, industrialized.** Same discovery rule
(`test_*` in `test_*.py`), bare asserts with rich failure
output, its own exit code:

```
pytest -q            # run everything
pytest -x            # stop at first red
pytest -k crossover  # run tests matching a name
pytest --lf          # rerun last failures
```

Our file runs under both engines unchanged:
`python3 -m pytest -q test_brooks.py` → `8 passed`.

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
lines of yaml test any language ever. And because heuristic #11
made every configuration one command line, heuristic #12 is free
in CI too: `xargs -P` fans those command lines across cores, no
framework required.

## Exercise 2: extend and wire ▪▪▪▪▪

*(~5 min start in class, finish at home.)* On your Proj1a fork:

1. Add one test born from a heuristic nobody used yet — e.g.
   #4 edges: `WHEN` after `tmax`; or fix the false refute by
   giving `verdict` an eps band, then pin it with a test (#9).
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
  meaning (heuristic #10).
