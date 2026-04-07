# bear.py  ── Python agent factories.
# Week tags mirror bear.lua.
# ─────────────────────────────────────────────────────
from fsm import new_id, start, shuffle
# S2: from fsm import make
# S3: from fsm import over, to, eq
# S4: from fsm import say
# S5: from fsm import now
# S7: from fsm import lint

# S2: from dataclasses import dataclass, field
# S2: @dataclass
# S2: class BearState:
# S2:     id:     int
# S2:     name:   str
# S2:     hunger: int = 80
# S2:     energy: int = 100
# S2:     start:  str = "sleep"
# S2:     current:str = "sleep"
# S2:     queue:  list = field(default_factory=list)
# S2:     states: dict = field(default_factory=dict)
#          ^^^ field(default_factory=list) is the S2 idiom fix
#              for the classic mutable-default-arg trap

# S1: plain dict agent (replaced by dataclass at S2)
def make_bear(name=None, hunger=80, energy=100):
    aid  = new_id()
    name = name or f"Bear#{aid}"

    def _p(s): return lambda _: print(s)   # S1 stub; gone at S4

    return dict(
        id      = aid,
        name    = name,
        hunger  = hunger,
        energy  = energy,
        start   = "sleep",
        current = "sleep",
        queue   = ["wake","smell","done"],
        # S10: trace = [],
        states  = {
            "sleep": {
                "action": _p(f"{name} sleeps."),
                # S4: "action": say("{name} sleeps."),
                # S5: "update": now(energy_tok, +5),
                "guard":  None,
                "exit":   None,
                "transitions": {"wake": "sniff"},
            },
            "sniff": {
                "action": _p(f"{name} sniffs."),
                # S4: "action": say("{name} sniffs. hunger={hunger}"),
                # S6: "guard":  [{"preds":[over(hunger_tok,30)],
                #                 "target":"eat"},
                #                {"preds":[], "target":"sleep"}],
                "guard":  None,
                "exit":   None,
                "transitions": {"smell":"eat", "nothing":"sleep"},
            },
            "eat": {
                "action": _p(f"{name} eats!"),
                # S4: "action": say("{name} eats! hunger={hunger}"),
                # S5: "update": lambda p: (now(hunger_tok,-30)(p),
                #                          now(energy_tok,+20)(p)),
                "guard":  None,
                "exit":   None,
                "transitions": {"done":"sleep"},
            },
        }
    )

def make_plant(kind=None, yield_=10, grow_time=3):
    pid  = new_id()
    kind = kind or "Plant"
    name = f"{kind}#{pid}"

    def _p(s): return lambda _: print(s)

    return dict(
        id         = pid,
        name       = name,
        yield_     = yield_,
        grow_time  = grow_time,
        berries    = 0,
        start      = "budding",
        current    = "budding",
        queue      = ["ripen"],
        # S10: trace = [],
        states     = {
            "budding": {
                "action": _p(f"{name} budding."),
                # S4: "action": say("{name} budding."),
                "guard":  None,
                "exit":   None,
                "transitions": {"ripen": "ripe"},
            },
            "ripe": {
                "action": _p(f"{name} RIPE!"),
                # S4: "action": say("{name} ripe! yield={yield_}"),
                "guard":  None,
                "exit":   None,
                "transitions": {"eaten":"bare","drought":"dormant"},
            },
            "bare":    {"action":_p(f"{name} bare."),
                        "terminal":True, "transitions":{}},
            "dormant": {"action":_p(f"{name} dormant."),
                        "terminal":True, "transitions":{}},
        }
    )

# ── S1: one bear ──────────────────────────────────────
if __name__ == "__main__":
    print("=== S1: one bear ===")
    start(make_bear("Yogi", 80, 100))

# ── S8+: ecosystem (uncomment at S8) ─────────────────
# MAX_TICKS = 20
# bears  = [make_bear("Yogi",90,60), make_bear("Boo",50,80)]
# plants = [make_plant("berry",15,2), make_plant("nut",8,4)]
# agents = bears + plants
# for tick in range(MAX_TICKS):
#     print(f"-- tick {tick}")
#     for agent in shuffle(agents):
#         step(agent)

# ── S9: generated ecosystem (uncomment at S9) ─────────
# import random
# N_PLANTS, N_BEARS = 5, 3
# bears2  = [make_bear(hunger=random.randint(40,90))
#            for _ in range(N_BEARS)]
# plants2 = [make_plant(kind=random.choice(["berry","nut"]),
#                        yield_=random.randint(5,25))
#            for _ in range(N_PLANTS)]
# ↑ list comprehension: the S9 idiom replacing for+append
