"""
sd0.py: the smallest compartmental-model simulator, plus one model:
Brooks' Law ("adding staff to a late software project makes it
later", Mythical Man-Month, 1975). Engine = o, run, verdict.
"""

class o(dict):
  "a dict you can dot: x.W == x['W']"
  __getattr__ = dict.get
  __setattr__ = dict.__setitem__
  def __repr__(i):
    return "o" + str({k: round(v,1) if isinstance(v,float) else v
                      for k,v in i.items() if str(k)[0] != "_"})

def run(d, step):
  "euler-integrate `step` from t=0 to d.tmax; return the trajectory"
  u, t, out = o(**d["init"]), 0, []
  while t < d["tmax"]:
    v = o(**u)                 # tomorrow starts as a copy of today
    step(d, t, u, v)           # the model updates tomorrow
    u = v; t += d["dt"]; out += [(t, u)]
  return out

def verdict(claim, y0, y1, want, eps=0.05):
  "compare baseline y0 to treatment y1, in the claim's direction"
  gap = y1 - y0
  v = ("neutral" if abs(gap) < eps * abs(y0 or 1) else
       "confirm" if (gap < 0) == (want == "down") else "refute")
  return o(rq=claim, y0=y0, y1=y1, gap=gap, verdict=v)

# ---------------------------------------------------------------
# Brooks' Law, four compartments:
#   D = experienced devs   N = newbies (unproductive, need mentors)
#   W = work done          (R, work remaining, left implicit)
init = dict(D=10, N=0, W=0)

the = o(init=init,
        tmax = 30,     # how long we run (the horizon)
        dt   = 1,      # tick size
        HIRE = 0,      # how many newbies arrive...
        WHEN = 10,     # ...and on which tick
        MATURE = 0.08,  # fraction of newbies becoming devs per tick
        COMM   = 0.0020,# communication tax per dev-pair
        TRAIN  = 0.10) # productivity lost per newbie (mentoring)

def brooks(d, t, u, v):
  comm  = d["COMM"] * u.D * (u.D - 1) / 2       # n^2 channels: Brooks' core claim
  train = d["TRAIN"] * u.N                      # mentors pulled off the line
  prod  = u.D * max(0, 1 - comm - train)        # net output of the veterans
  v.W  += d["dt"] * prod                        # bank today's work
  v.N  += -d["dt"] * d["MATURE"] * u.N \
          + (d["HIRE"] if t == d["WHEN"] else 0)  # the intervention lands here
  v.D  +=  d["dt"] * d["MATURE"] * u.N          # newbies mature into devs

def y(out):
  "score one run: work banked by the end (higher = better)"
  return out[-1][1].W

def rq(**kw):
  "the research question, as an experiment: no-hire vs hire-10"
  base  = {**the, **kw, "HIRE": 0}              # rx0: no reinforcements
  treat = {**the, **kw, "HIRE": 10}             # rx1: add 10 at WHEN
  return verdict("adding staff to a late project makes it later",
                 y(run(base, brooks)), y(run(treat, brooks)), "down")

if __name__ == "__main__":
  print(rq())
  for tmax in [10, 20, 40, 60, 70, 80, 100]:
    print("tmax=", tmax, rq(tmax=tmax))
