"""
test_brooks.py: a roll-your-own test engine for sd0.py.
Runs four ways:

   python3 test_brooks.py -all              # everything; exit = #fails
   python3 test_brooks.py -crossover        # just one test
   python3 test_brooks.py -tmax 80 -brooks  # change a knob, then test
   python3 -m pytest -q test_brooks.py      # same tests, via pytest
"""
import sys, random, traceback
import sd0
from sd0 import the, brooks, run, verdict

the.setdefault("seed", 1)          # sd0 is deterministic (so far); doctrine anyway
m = brooks()

def atom(s):
  "string -> int | float | string"
  for f in (int, float):
    try: return f(s)
    except ValueError: pass
  return s

# --------------------------- the tests --------------------------
def test_runs():
  "the model runs, for exactly tmax ticks"
  assert len(run(m.init, m.step)) == the["tmax"]

def test_bounds():
  "the clamp holds: every stock stays inside its [lo,hi]"
  for t, s in run(m.init, m.step):
    for k, (_, lo, hi) in m.init.items():
      assert lo <= getattr(s, k) <= hi

def test_backlog():
  "conservation: work done + work remaining is always 1000"
  for t, s in run(m.init, m.step):
    assert abs(s.W + s.R - 1000) < 1e-9

def test_staff():
  "conservation: D+N only ever changes by HIRE"
  hire = {**m.init, 'HIRE': [10, 0, 50]}
  out  = run(hire, m.step)
  assert abs(out[-1][1].D + out[-1][1].N - (20 + 10)) < 1e-9

def test_work_grows():
  "work banked never goes down"
  out = run(m.init, m.step)
  assert all(a[1].W <= b[1].W for a, b in zip(out, out[1:]))

def test_brooks():
  "at the default horizon, Brooks' Law holds"
  assert m.rq().verdict == "confirm"

def test_crossover():
  "the verdict flips somewhere past the default horizon"
  assert m.rq(tmax=40).verdict == "confirm"
  assert m.rq(tmax=80).verdict == "refute"

def test_false_refute():
  "photograph taken before the hire lands: gap is exactly zero,\n  yet the binary verdict scores it 'refute' -- a known blind spot"
  v = m.rq(tmax=10)
  assert v.gap == 0.0 and v.verdict == "refute"

# ------------------------- the engine ---------------------------
eg = {"-" + k[5:]: f for k, f in globals().items()
      if k.startswith("test_")}

def run1(f):
  "reseed, run one test, survive its crash; return 0=pass 1=fail"
  random.seed(the["seed"])
  try:
    f(); print("PASS", f.__name__, "::", f.__doc__); return 0
  except Exception:
    traceback.print_exc()
    print("FAIL", f.__name__, "::", f.__doc__); return 1

if __name__ == "__main__":
  fails = 0
  for j, s in enumerate(sys.argv):
    if s == "-all":
      fails += sum(run1(f) for f in eg.values())
    elif f := eg.get(s):
      fails += run1(f)
    elif (k := s.lstrip("-")) in the:
      the[k] = atom(sys.argv[j + 1])
  sys.exit(fails)                  # the only thing CI will ever see
