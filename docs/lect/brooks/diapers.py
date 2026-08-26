"""
diapers.py: the gentlest possible compartmental model.

  q ──▶ [ C:clean ] ──r──▶ [ D:dirty ] ──s──▶ ⊘
         buy 70/Sat   use 8/day    dump Sat (miss t=27)

One baby, one weekly shop, one forgotten laundry day.
"""
from sd0 import the, run, o

def saturday(t): return int(t) % 7 == 6

def diapers():
  # C=clean stock, D=dirty stock; q,r,s = the three flows;
  # BUY = input: how big is the Saturday shopping trip?
  init = dict(C=[100,0,100], D=[0,0,100],
              q=[0,0,100], r=[8,0,20], s=[0,0,100],
              BUY=[70,0,100])
  def step(dt,t,u,v):
    v.C += dt*(u.q - u.r)               # clean: bought minus used
    v.D += dt*(u.r - u.s)               # dirty: used minus dumped
    v.q  = u.BUY if saturday(t) else 0  # flows are state too:
    v.s  = u.D   if saturday(t) else 0  #   set now, felt NEXT tick
    if t == 27: v.s = 0                 # the forgotten Saturday
  def y(out):
    "higher = better: minus the days caught short"
    return -sum(1 for t,s in out if s.C <= 0)
  def rq(bg=None, **kw):
    "did we ever run out, and how high did the pile get?"
    out = run(init if bg is None else bg, step, **kw)
    return o(ran_out=any(s.C <= 0 for t,s in out),
             peak_D=max(s.D for t,s in out), y=y(out))
  return o(init=init, step=step, y=y, rq=rq, ctrl="BUY")

if __name__ == "__main__":
  m = diapers()
  for buy in (70, 56, 40):
    bg = {**m.init, "BUY": [buy, 0, 100]}
    print("BUY =", buy, m.rq(bg=bg, tmax=35))
