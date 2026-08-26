"""
forrester.py: Forrester & Senge's confidence tests (1980), as a
harness over any sd0-style model m = o(init, step, y, rq, ctrl).

Five of the nine tests mechanize; four do not — boundary adequacy,
dimensional consistency, parameter verification, and matching real-
world data all need a human who knows the world. That split is the
point: run what can be run, and know what you still owe.
"""
import sys
from sd0 import the, run, o, brooks

# ---- F&S 2: structure verification (the dynamic half) ----------
def moving(m, **kw):
  "which stocks actually change over a run? inputs should not."
  out = run(m.init, m.step, **kw)
  a, b = out[0][1].__dict__, out[-1][1].__dict__
  return {k for k in a if a[k] != b[k]}

def check_structure(m):
  "every stock moves; every input (like the ctrl) holds still"
  mv = moving(m)
  return m.ctrl not in mv and mv >= {"W", "R"}

# ---- F&S 2/3, the accounting half: conservation ----------------
def check_conserved(m, keys, total, **patch):
  "the named stocks always sum to the same total"
  init = {**m.init, **patch}
  return all(abs(sum(getattr(s, k) for k in keys) - total) < 1e-9
             for t, s in run(init, m.step))

# ---- F&S 5: extreme conditions ---------------------------------
def check_extremes(m, cases):
  "patch the world to an extreme; a first-principles law must hold"
  return [name for name, patch, law in cases
          if not law(run({**m.init, **patch}, m.step))]

# ---- F&S 6: behavior reproduction ------------------------------
def check_reproduce(m, expect="confirm", **kw):
  "the model retells the story it was built to tell"
  return m.rq(**kw).verdict == expect

# ---- F&S 7: surprise behavior ----------------------------------
def check_flips(m, knob="tmax", vals=range(10, 121, 10)):
  "sweep one knob; report every verdict change (bug, or discovery?)"
  vs = [(v, m.rq(**{knob: v}).verdict) for v in vals]
  return [(a[0], b[0], a[1] + "->" + b[1])
          for a, b in zip(vs, vs[1:]) if a[1] != b[1]]

# ---- F&S 8/9: sensitivity, and policy sensitivity --------------
def check_sensitivity(m, delta=0.25, **kw):
  "nudge every initial stock +-25%; which nudges flip the verdict?"
  want = m.rq(**kw).verdict
  out = []
  for k, (v, lo, hi) in m.init.items():
    if k == m.ctrl or v == 0: continue
    for f in (1 - delta, 1 + delta):
      bg = {**m.init, k: [max(lo, min(hi, v * f)), lo, hi]}
      if m.rq(bg=bg, **kw).verdict != want: out.append((k, f))
  return out

# ---------------------------------------------------------------
if __name__ == "__main__":
  m, fails = brooks(), 0
  extreme_cases = [
    ("no devs, no work",    {'D': [0, 0, 100]},
       lambda out: out[-1][1].W == 0),
    ("no backlog, no work", {'R': [0, 0, 1000]},
       lambda out: out[-1][1].W == 0),
    ("hire after horizon changes nothing", {'WHEN': [29, 0, 30]},
       lambda out: True)]  # verdict check below instead
  checks = [
    ("2 structure: stocks move, inputs do not", check_structure(m)),
    ("2 conservation: W+R is always 1000",
       check_conserved(m, ["W", "R"], 1000)),
    ("2 conservation: D+N constant when nobody is hired",
       check_conserved(m, ["D", "N"], 20)),
    ("2 conservation: after a hire of 10, D+N ends at 30",
       abs(sum(getattr(run({**m.init, 'HIRE': [10, 0, 50]},
                           m.step)[-1][1], k) for k in ("D", "N"))
           - 30) < 1e-9),
    ("5 extremes hold", check_extremes(m, extreme_cases) == []),
    ("5 extreme, via rq: hire at the last tick is a no-op",
       m.rq(bg={**m.init, 'WHEN': [29, 0, 30]}).gap == 0),
    ("6 reproduction: Brooks' story at the default horizon",
       check_reproduce(m)),
  ]
  for name, ok in checks:
    print(("PASS " if ok else "FAIL "), "F&S", name)
    fails += 0 if ok else 1
  print("\nF&S 7 surprise: verdict flips at",
        check_flips(m) or "none")
  print("F&S 8/9 sensitivity: verdict flipped by",
        check_sensitivity(m) or "nothing (robust to +-25% nudges)")
  print("\nStill owed to a human: 1 boundary adequacy,",
        "3 dimensional consistency, 4 parameter meaning,",
        "6b match to real project data.")
  sys.exit(fails)
