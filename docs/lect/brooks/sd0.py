#!/usr/bin/env python3 -B
"""sd0.py: smallest compartmental simulator + brooks. UPPER=input, lower=param."""

the = dict(dt=1, tmax=30)

class o:
  "js-style object. i, not self."
  def __init__(i,**d): i.__dict__.update(d)
  def __repr__(i): return "o"+str(i.__dict__)

def run(init, step, **kw):
  "init={k:[now,lo,hi]}. returns [(t,state)]. clamps every var to its bounds."
  d  = the | kw
  u  = o(**{k:v[0] for k,v in init.items()})
  out, t = [], 0
  while t < d["tmax"]:
    v = o(**u.__dict__)                            # v = next state, u = now
    step(d["dt"], t, u, v)
    for k,(_,lo,hi) in init.items():
      setattr(v, k, max(lo, min(hi, getattr(v,k))))
    out += [(t,v)]; t,u = t+d["dt"], v
  return out

def verdict(txt, y0, y1, want):
  "want='down' means treatment should lower y."
  gap = y1 - y0
  ok  = gap < 0 if want=="down" else gap > 0
  return o(y0=round(y0,1), y1=round(y1,1), gap=round(gap,1),
           verdict="confirm" if ok else "refute", rq=txt)

#--------------------------------------------------------------- brooks -------
def brooks():
  "Brooks' Law: adding people to a late project makes it later."
  # D=experienced devs, N=newbies, W=work done, R=work remaining (all stocks).
  # HIRE=how many newbies arrive at t=WHEN (inputs: state of the world).
  init = {'D':[20,0,100], 'N':[0,0,100], 'W':[0,0,1000], 'R':[1000,0,1000],
          'HIRE':[0,0,50], 'WHEN':[10,0,30]}

  def step(dt,t,u,v):
    comm  = u.D*(u.D-1)/2 * 0.0002              # n^2 talk cost, grows with team
    train = u.N * 0.2                           # each newbie steals mentor time
    prod  = max(0, u.D*(1-comm-train)) * 0.5    # net output of the veterans
    v.R   = u.R - dt*min(prod, u.R)             # burn down the backlog
    v.W   = u.W + dt*min(prod, u.R)             # ..and bank it as work done
    v.N   = u.N - dt*0.1*u.N + (u.HIRE if t==u.WHEN else 0)  # hire once, then age
    v.D   = u.D + dt*0.1*u.N                    # 10%/tick of newbies turn veteran

  def y(out):
    "score a run. higher=better. work banked by tmax, so slower => smaller y."
    return out[-1][1].W                         # last row, its W stock

  def rq(bg=None, **kw):
    "the experiment: same world, one knob moved. HIRE is ctrl. kw = run opts."
    bi    = init if bg is None else bg          # bg = calibrated background, if any
    base  = {**bi, 'HIRE':[0, 0,50]}            # rx0: nobody added
    treat = {**bi, 'HIRE':[10,0,50]}            # rx1: 10 added at WHEN
    return verdict("adding staff makes it later",   # Brooks predicts..
                   y(run(base ,step,**kw)),         # ..y under no hiring
                   y(run(treat,step,**kw)), "down") # ..beats y under hiring

  return o(init=init, step=step, y=y, rq=rq, ctrl="HIRE")

#--------------------------------------------------------------- main ---------
if __name__ == "__main__":
  m = brooks()
  for tmax in (10,20,40,60,70,80):              # horizon sweep: when does it flip?
    v = m.rq(tmax=tmax)                         # one verdict per horizon
    print(f"tmax={tmax:3} {v}")
