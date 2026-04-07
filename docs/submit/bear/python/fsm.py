# fsm.py  ── Python port of the engine.
# Same week tags as fsm.lua. Uncomment one block per week.
# ─────────────────────────────────────────────────────
import sys, os, random, time

# S1 ── seed ──────────────────────────────────────────
SEED = int(sys.argv[1]) if len(sys.argv)>1 else \
       int(os.getenv("SEED","0")) or int(time.time())
random.seed(SEED)
print(f"-- seed {SEED}  (replay: python bear.py {SEED})")

# S1 ── id counter ────────────────────────────────────
_id = 0
def new_id():
    global _id; _id += 1; return _id

# S1 ── shuffle ───────────────────────────────────────
def shuffle(lst):
    import random as r
    lst = list(lst); r.shuffle(lst); return lst

# S2 ── token registry ────────────────────────────────
# from dataclasses import dataclass, field
# from enum import Enum
# _tokens: dict[str, "Token"] = {}
#
# @dataclass
# class Token:
#     name: str
#     id:   int
#     def __repr__(self): return f"Token({self.name})"
#
# def make(name: str) -> Token:
#     if name in _tokens:
#         print(f"WARNING: duplicate token '{name}'")
#         return _tokens[name]
#     t = Token(name=name, id=new_id())
#     _tokens[name] = t
#     return t

# S3 ── comparators ───────────────────────────────────
# from functools import partial
# import operator as op
#
# def _cmp(fn, token, n):
#     return lambda p: fn(getattr(p, token.name, 0), n)
#
# def over(token, n): return _cmp(op.gt,  token, n)
# def to  (token, n): return _cmp(op.le,  token, n)
# def eq  (token, n): return _cmp(op.eq,  token, n)

# S4 ── say() ─────────────────────────────────────────
# def say(msg: str):
#     def _action(p):
#         def replacer(k):
#             v = getattr(p, k, None)
#             if v is None:
#                 print(f"WARNING: unknown key '{k}' in say()")
#                 return f"<{k}?>"
#             return str(v)
#         import re
#         print(re.sub(r"\{(\w+)\}",
#               lambda m: replacer(m.group(1)), msg))
#     return _action

# S5 ── now() ─────────────────────────────────────────
# def now(token, delta=None):
#     def _update(p):
#         if delta is None:
#             setattr(p, token.name, True); return True
#         if delta == 0:
#             setattr(p, token.name, False); return False
#         v = getattr(p, token.name, 0) + delta
#         setattr(p, token.name, v); return v
#     return _update

# S6 ── eval_when(): or-of-ands ───────────────────────
# def eval_when(clauses, p):
#     for conjunct in clauses:
#         preds = conjunct.get("preds", [])
#         if all(pred(p) for pred in preds):
#             return conjunct.get("target")
#     return None

# S7 ── lint() ────────────────────────────────────────
# def lint(agent):
#     rules, start = agent.states, agent.start
#     reachable = set()
#     for sname, state in rules.items():
#         for tgt in (state.get("transitions") or {}).values():
#             reachable.add(tgt)
#             if tgt not in rules:
#                 print(f"LINT [{agent.name}]: ghost state "
#                       f"'{tgt}' from '{sname}'")
#     for sname, state in rules.items():
#         t = state.get("transitions") or {}
#         if len(t)==0 and not state.get("terminal"):
#             print(f"LINT [{agent.name}]: dead end '{sname}'")
#     for sname in rules:
#         if sname != start and sname not in reachable:
#             print(f"LINT [{agent.name}]: "
#                   f"unreachable state '{sname}'")

# S1 ── core run (iterative; Python has no TCO) ───────
def _run(agent):
    rules = agent.states
    while True:
        s     = agent.current
        state = rules.get(s)
        if not state: return agent

        # S1: action
        action = state.get("action")
        if action: action(agent)

        # S5: update  [uncomment S5]
        # update = state.get("update")
        # if update: update(agent)

        # S6: exit    [uncomment S6]
        # exit_fn = state.get("exit")

        if not agent.queue: return agent
        e = agent.queue.pop(0)

        # S6: guard override  [uncomment S6]
        # guard_target = eval_when(state.get("guard") or [], agent)

        # S10: wildcard  [uncomment S10]
        # target = ((state.get("transitions") or {}).get(e)
        #        or (state.get("transitions") or {}).get("*")
        #        or s)
        target = (state.get("transitions") or {}).get(e, s)

        # S10: trace  [uncomment S10]
        # agent.trace.append(f"[{e}] {s} -> {target}")

        # S6: fire exit before move  [uncomment S6]
        # if exit_fn: exit_fn(s, agent)

        agent.current = target

def start(agent):
    agent.current = agent.current or agent.start
    return _run(agent)

# S8 ── step(): one event per tick  [uncomment S8] ────
# def step(agent):
#     if not agent.queue: return
#     _run_one(agent)   # variant of _run that pops one event

# S10 ── print_trace()  [uncomment S10] ───────────────
# def print_trace(agent):
#     for line in getattr(agent, "trace", []):
#         print("  " + line)
