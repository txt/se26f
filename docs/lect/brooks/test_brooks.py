"""
test_brooks.py: a roll-your-own test engine for sd0.py.
Runs two ways:

   python3 test_brooks.py -all              # everything; exit = #fails
   python3 test_brooks.py -crossover        # just one test
   python3 test_brooks.py -tmax 80 -brooks  # change a knob, then test
   python3 -m pytest -q test_brooks.py      # same tests, via pytest
"""
import sys, random, traceback
from sd0 import the, o, run, brooks, y, rq

the.seed = 1                      # no randomness in sd0 (yet); doctrine anyway

def atom(s):
  "string -> int | float | string"
  for f in (int, float):
    try: return f(s)
    except ValueError: pass
  return s

# --------------------------- the tests --------------------------
def test_runs():
  "the model runs, for exactly tmax ticks"
  assert len(run(the, brooks)) == the.tmax

def test_work_grows():
  "work banked never goes down"
  out = run(the, brooks)
  assert all(a[1].W <= b[1].W for a, b in zip(out, out[1:]))

def test_conserve():
  "staff is conserved: D+N only ever changes by HIRE"
  out = run({**the, "HIRE": 10}, brooks)
  assert abs(out[-1][1].D + out[-1][1].N - (10 + 10)) < 1e-9

def test_extreme():
  "extreme condition: with no comm tax and no training tax, hiring can only help"
  r = rq(COMM=0, TRAIN=0, tmax=60)
  assert r.verdict == "refute"

def test_brooks():
  "at the default horizon, Brooks' Law holds"
  assert rq().verdict == "confirm"

def test_neutral():
  "photograph taken before the hire lands: no verdict either way"
  assert rq(tmax=10).verdict == "neutral"

def test_crossover():
  "the verdict flips somewhere past the default horizon"
  early, late = rq(tmax=30).verdict, rq(tmax=120).verdict
  assert early == "confirm" and late == "refute"

# ------------------------- the engine ---------------------------
eg = {"-" + k[5:]: f for k, f in globals().items()
      if k.startswith("test_")}

def run1(f):
  "reseed, run one test, survive its crash; return 0=pass 1=fail"
  random.seed(the.seed)
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
