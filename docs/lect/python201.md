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


# Python 201: Seventeen Things That Bite

**Links:** [Home](../../README.md) · [Desugaring](desugar.md) ·
[Closures](closures.md) · [N6 patterns](n06.md)

Python 101 teaches syntax. Then you hit a bug that makes no sense,
and the fix looks like superstition. This reading names seventeen
constructs that bite, and gives each one a reason.

Most of the seventeen have the same root. Python holds **names** that
point at **objects**, and it holds **function bodies that have not
run yet**. Once you can say which of the two you are looking at,
the surprises stop. Tie back to [desugaring](desugar.md): a body is
inert text until somebody calls it.

Every output below was produced by running the code (Python 3.14).

---

## Part A. Names and objects

### 1. A name is a label, not a box

Assignment never copies. It points a second label at the same
object:

```python
a = [1, 2]
b = a
b.append(3)
print(a)             # [1, 2, 3]   one list, two labels

b = b + [4]          # builds a NEW list, relabels b
print(a, b)          # [1, 2, 3] [1, 2, 3, 4]
```

`append` mutates the object. `+` builds a new one. So "did my
change show up over there?" always reduces to: did I mutate, or
did I rebind?

Lambda tie: a closure captures the **name**, not the value at
capture time. Bug 7 below is that sentence, biting.

### 2. Default arguments run once, at definition time

```python
def add(item, bag=[]):
    bag.append(item)
    return bag

print(add(1))        # [1]
print(add(2))        # [1, 2]   the same bag, still there
print(add(3))        # [1, 2, 3]
```

`def` is a statement. When Python executes it, Python evaluates the
default expression **then**, once, and staples the result to the
function. Watch it happen:

```python
def f(x=print("default runs at def time")): pass
# prints immediately, before any call
```

So the body is lazy and the defaults are eager. Fix with a
sentinel:

```python
def add(item, bag=None):
    bag = [] if bag is None else bag
    bag.append(item)
    return bag
```

Lambda tie: this is the exact split from [desugar §4](desugar.md) —
the body waits, everything around it does not.

### 3. `is` compares identity, `==` compares value

```python
print([1] == [1])    # True    same contents
print([1] is [1])    # False   two objects
```

`is` asks "same object?". Only use it for singletons: `None`,
`True`, `False`. Small integers confuse people because CPython
caches them:

```python
p = int("256"); q = int("256"); print(p is q)   # True   cached
x = int("257"); y = int("257"); print(x is y)   # False  not cached
```

Nothing in the language promises either answer. `==` is what you
meant.

### 4. `*` on a list copies the pointer, not the thing

```python
grid = [[0] * 3] * 3
grid[0][0] = 9
print(grid)          # [[9, 0, 0], [9, 0, 0], [9, 0, 0]]
```

Three labels, one inner list. The comprehension version runs its
body three times, so you get three lists:

```python
grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 9
print(grid)          # [[9, 0, 0], [0, 0, 0], [0, 0, 0]]
```

Lambda tie: `[0] * 3` is one value, computed once. `[... for _ in
...]` is a body, called once per item. Repeated calls are how you
get distinct objects.

### 5. Class attributes are shared; instance attributes are not

```python
class Dog:
    tricks = []                        # ONE list, for all dogs
    def __init__(self, name): self.name = name

d1, d2 = Dog("rex"), Dog("ada")
d1.tricks.append("sit")
print(d2.tricks)                       # ['sit']
```

The class body runs once, at import. So `tricks` belongs to the
class. Per-dog state must be built per call, in `__init__`:

```python
class Dog:
    def __init__(self, name):
        self.name, self.tricks = name, []
```

Same lesson as bug 4: one evaluation gives one object.

---

## Part B. Scope and closures

### 6. You may read a global, but you may not write one

Python adds a **compile-time** rule, on purpose, to stop you from
confusing locals with globals. Reading a global is free. Writing
one needs a declaration.

```python
n = 0

def show():
    print(n)         # reading the global: fine
show()               # 0
```

Now assign to it:

```python
def bump():
    n = n + 1        # n is now LOCAL, and has no value yet
bump()
# UnboundLocalError: cannot access local variable 'n'
#                    where it is not associated with a value
```

Python compiles the function before running it. One assignment
*anywhere* in the body marks that name local for the *whole* body.
So the rule is not "it depends on the order of the lines":

```python
def sneaky():
    print(n)         # looks like a read of the global...
    n = 99           # ...but this line made n local up above too
sneaky()
# UnboundLocalError: cannot access local variable 'n'
```

That error is the feature. Silent global mutation is one of the
great bug factories, so Python makes you sign for it. Lookup order
is LEGB: Local, Enclosing, Global, Builtins — and writing to a
non-local level needs a keyword. Use `global` for module level,
`nonlocal` for an enclosing function:

```python
def bump_ok():
    global n
    n = n + 1
bump_ok()
print(n)             # 1
```

`nonlocal` is the interesting one, because it gives a closure
private, writable state:

```python
def counter():
    k = 0
    def up():
        nonlocal k
        k += 1
        return k
    return up

c = counter()
print(c(), c(), c())        # 1 2 3
```

Lambda tie: `up` is an object with private state, built from a
function and a captured variable. See [closures](closures.md) —
that is the whole trick behind objects.

### 7. Closures capture the variable, not its value

The classic. Three lambdas, one `i`:

```python
fs = [lambda: i for i in range(3)]
print([f() for f in fs])     # [2, 2, 2]     not [0, 1, 2]
```

Every lambda points at the same `i`. By the time you call them, the
loop is over and `i` is 2.

That matters the moment the lambdas decide something. Build one
threshold check per limit, then ask all three whether 15 passes:

```python
def checks_broken(limits):
    out = []
    for lim in limits:
        out.append(lambda x: x <= lim)         # captures the VARIABLE
    return out

def checks_fixed(limits):
    return [lambda x, lim=lim: x <= lim        # captures the VALUE
            for lim in limits]

print("broken:", [f(15) for f in checks_broken([10, 20, 30])])
print("fixed :", [f(15) for f in checks_fixed([10, 20, 30])])
```

```
broken: [True, True, True]
fixed : [False, True, True]
```

Read the two lines. The broken version says 15 is under a limit of
10, because all three checks are reading the last value of `lim`.
The fixed version gets the right answer, and only the fixed version
changes behavior when you change the list of limits. In a
validation layer, that difference is a shipped bug that no test
catches unless the test uses more than one limit.

`functools.partial` does the same capture without the fake
parameter:

```python
from functools import partial
def le(lim, x): return x <= lim
print([f(15) for f in [partial(le, lim) for lim in [10, 20, 30]]])
# [False, True, True]
```

Look at what just happened. Bug 2 said "defaults are eager, bodies
are lazy", and there it was the bug. Here the same fact is the cure:
`lim=lim` is evaluated at definition time, so each lambda gets its
own frozen copy. A Python gotcha becomes a tool once you know which
part waits.

### 8. The walrus, `:=`, in sixty seconds

Plain `=` is a **statement**: it assigns, and it has no value, so
you cannot put it in an `if` or a `while`. `:=` is an **assignment
expression** (Python 3.8 and later). It assigns *and* hands the
value back, so you can name something and test it in one place.

Three places it earns its keep. First, name a computed value you
are about to test:

```python
line = "  name: Ada  "
if (t := line.strip()):
    print(repr(t), len(t))       # 'name: Ada' 9
```

Without `:=` you either call `strip()` twice, or you assign on a
line above and clutter the scope.

Second, a match object, the most common use in real code:

```python
import re
if (m := re.search(r"(\d+)", "order 4471 shipped")):
    print("order", m.group(1))   # order 4471
```

Third, the read-until-empty loop. This is the drained-generator
shape from [desugar §6](desugar.md), written in one line:

```python
data = iter(["a", "b", ""])
while (chunk := next(data, "")):
    print("chunk", chunk)        # chunk a
                                 # chunk b
```

Two rules of use. Keep the parentheses: they are not always
required, but they stop the reader from misreading `:=` as `==`.
And do not use it to be clever. One name, tested once, is the whole
point.

### 9. A comprehension has its own scope; the walrus escapes it

```python
z = "safe"
[z for z in range(3)]
print(z)                     # 'safe'     the loop name is local

[w := v for v in range(3)]
print(w)                     # 2          walrus writes outward
```

A comprehension compiles to a hidden function, so its loop variable
cannot leak. `:=` deliberately assigns in the *enclosing* scope, so
it jumps straight out of that hidden function. That is handy in a
`while`, and rude inside a comprehension. Where it does read well
is when you need a value for both the test and the result:

```python
words = ["alpha", "be", "gamma"]
print([n for w in words if (n := len(w)) > 3])   # [5, 5]
```

One call to `len`, used twice.

---

## Part C. Laziness

### 10. An iterator is one-shot

```python
g = (x * x for x in range(3))
print(list(g))               # [0, 1, 4]
print(list(g))               # []           it is spent
```

A generator holds "where I am up to". Reading it moves that
position forward and nothing rewinds it. So a generator passed to
two functions gives the second one nothing.

Lambda tie: from [desugar §5](desugar.md), `g` is a value plus a
thunk for the rest. Calling the thunk consumes the cell. If you
need two passes, keep a list, or rebuild the generator.

### 11. `map`, `filter`, `zip`, `open` are lazy

```python
m = map(print, ["one", "two"])
print("nothing yet")         # nothing yet
list(m)                      # one
                             # two
```

Nothing runs until something pulls. Two consequences: a `map` whose
function raises will raise *later*, somewhere confusing; and a
`map` you never consume is a bug that fails silently.

### 12. An `async def` call is a thunk you forgot to call

```python
async def go(): print("ran")

co = go()                    # nothing printed
print(type(co).__name__)     # coroutine
# RuntimeWarning: coroutine 'go' was never awaited

import asyncio
asyncio.run(go())            # ran
```

`async def` does not make a function that runs concurrently. It
makes a function that returns *a thing to be run*. `await` or
`asyncio.run` is the `funcall`. Same shape as a Lisp thunk, with a
scheduler attached.

---

## Part D. Functions are values

### 13. A method is a function plus a captured `self`

```python
class Greeter:
    def __init__(self, name): self.name = name
    def hi(self, other):      return f"{self.name} greets {other}"

g = Greeter("Ada")
print(g.hi("Bob"))            # Ada greets Bob   <- sugar
print(Greeter.hi(g, "Bob"))   # Ada greets Bob   <- what runs

f = g.hi                      # a bound method: a closure over g
print(f.__self__.name)        # Ada
print(f("Cy"))                # Ada greets Cy
```

`g.hi` desugars to `Greeter.hi` with the first argument already
supplied. That is partial application, which is why `self` is
explicit in the definition and invisible at the call. You can pass
`f` anywhere a one-argument function is wanted, and it drags `g`
along with it.

### 14. A decorator is a function that returns a function

```python
import functools

def traced(fn):
    @functools.wraps(fn)                 # keep __name__, __doc__
    def wrapper(*args, **kw):
        print(f"-> {fn.__name__}{args}")
        out = fn(*args, **kw)
        print(f"<- {out}")
        return out
    return wrapper

@traced
def area(w, h): return w * h

area(3, 4)              # -> area(3, 4)
                        # <- 12
print(area.__name__)    # area   (without wraps, this says 'wrapper')
```

The `@` line is pure sugar:

```python
area = traced(area)
```

Lambda tie: retry, timing, caching, authentication, and rate limits
are all this one shape — take a body, return a bigger body. Half of
[N6](n06.md)'s pattern catalogue is here.

### 15. `with` ships your block to somebody else's setup

```python
from contextlib import contextmanager

@contextmanager
def tag(name):
    print(f"<{name}>")
    try:     yield            # your block runs HERE
    finally: print(f"</{name}>")

with tag("b"): print("hi")
# <b>
# hi
# </b>
```

The generator splits at `yield`: everything before is setup,
everything after is teardown, and the `finally` guarantees the
teardown even if your block raises. You are handing your code to a
framework, in the same way [desugar §10](desugar.md) hands a
validator to a dialog layer.

### 16. Functions in, functions out: the standard toolkit

```python
rows = [("b", 2), ("a", 3), ("c", 1)]
print(sorted(rows, key=lambda r: r[1]))      # [('c',1),('b',2),('a',3)]

import operator
print(sorted(rows, key=operator.itemgetter(1)))   # same, faster, no lambda

from functools import reduce, lru_cache
print(reduce(lambda a, b: a + b, [1, 2, 3, 4]))   # 10

@lru_cache(maxsize=None)
def fib(n): return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(100))          # 354224848179261915075
print(fib.cache_info())  # hits=98, misses=101
```

`key=` is Strategy. `reduce` is a fold. `lru_cache` turns a body
into a body-that-remembers, which is how a 30-year exponential
classroom example becomes instant.

### 17. To send a function to another process, Python sends its name

A separate process has separate memory. So Python cannot hand it a
function: it must *describe* the function, send the description
down a pipe, and let the other side rebuild it. Look at the
description:

```python
import pickle
def work(row): return row * row

print(pickle.dumps(work))
# b'\x80\x05\x95\x15\x00\x00\x00\x00\x00\x00\x00
#   \x8c\x08__main__\x94\x8c\x04work\x94\x93\x94.'
```

Two readable strings in there: `__main__` and `work`. That is the
whole message — "import that module, look up that name". The body
never travels. The worker already has the code, because it imports
your file.

So an anonymous function cannot be sent. There is no name to look
up:

```python
print(pickle.dumps(lambda r: r + 1))
# PicklingError: Can't pickle <function <lambda> at 0x107643320>:
#                it's not found as __main__.<lambda>
```

That is the rule behind every "why won't multiprocessing take my
lambda" question. Top-level `def` works; lambdas, nested functions,
and closures do not:

```python
from multiprocessing import Pool

def work(row): return row * row      # top-level, so it has a name

if __name__ == "__main__":
    with Pool(4) as p:
        print(p.map(work, range(8)))   # [0, 1, 4, ..., 49]
```

Second consequence: since each worker is a fresh import of your
module, each worker gets its **own copy** of module state. Eight
rows, four workers, one counter per worker:

```python
import os, time
from multiprocessing import Pool
seen = 0

def bump(row):
    global seen
    seen += 1
    time.sleep(0.05)
    return (os.getpid(), seen)

if __name__ == "__main__":
    with Pool(4) as p:
        for pid, n in p.map(bump, range(8), chunksize=1):
            print(f"worker {pid}: count={n}")
```

```
worker 2458: count=1      worker 2458: count=2
worker 2456: count=1      worker 2456: count=2
worker 2457: count=1      worker 2457: count=2
worker 2459: count=1      worker 2459: count=2
```

Eight calls, and the highest count is 2. Four private counters, no
shared total, no error message. That is why a body meant for
parallel work must be **pure**: take arguments, return a value,
touch nothing global. Purity is what makes a body portable
([desugar §10.2](desugar.md)).

Third fact, for completeness: threads avoid the pickling problem,
because they share memory. They will still not speed up
pure-Python CPU work, because the GIL lets one thread run
bytecode at a time. Threads for waiting, processes for computing.

---

## The small stuff, in one table

| You write | What happens | Why |
|---|---|---|
| `x = mylist.sort()` | `x` is `None` | mutators return `None`; `sorted()` returns the list |
| `x = mylist.append(1)` | `x` is `None` | same rule |
| `port = cfg or 8080` | `0` becomes `8080` | `or` tests truth, not presence; use `if cfg is None` |
| `t = ([1],); t[0] += [2]` | `TypeError`, **and** the list grew | `+=` mutates, then fails to rebind |
| `zip([1,2,3], [9])` | one pair | `zip` stops at the shortest input |
| `0.1 + 0.2 == 0.3` | `False` | binary floats; compare with `math.isclose` |
| `-7 // 2` | `-4`, and `-7 % 2` is `1` | floor division, sign follows the divisor |
| `s += "x"` in a loop | quadratic time | strings are immutable; use `"".join(parts)` |
| `except:` bare | swallows `KeyboardInterrupt` | catch `Exception`, or the specific class |
| `def f(): return [] if x else None` | mixed return types | pick one shape; your caller cannot branch on surprises |

---

## Try this

1. **Predict, then run.** Before executing anything, write down your
   expected output for bugs 2, 4, 7 and 10. Run them. Count how many
   you got right.
2. **One root cause.** Bugs 2, 4 and 5 are the same sentence about
   evaluation. Write that sentence in one line, in your own words.
3. **Turn a bug into a tool.** Use the eager-default trick from bug
   7 to build a list of ten functions that each print a different
   number.
4. **Decorate something real.** Add a `@traced` decorator to one
   function in your proj2 repo. Then add `@lru_cache` and report the
   hit rate.
5. **Ship a body.** Convert one `for` loop over independent rows in
   your project into `Pool.map`. If it will not pickle, say which
   rule from bug 17 you broke.
6. **Grep for the table.** Search your repo for `.sort()` used as an
   expression, or `or` used to supply a default. Report what you
   find.

## References

1. Ramalho, *Fluent Python*, 2nd ed., 2022. Chapters 6 to 9 cover
   names, objects, and closures in depth.
2. Beazley & Jones, *Python Cookbook*, 3rd ed., 2013.
3. Hettinger, "Transforming Code into Beautiful, Idiomatic Python",
   PyCon 2013.
4. CPython docs: *The Python Language Reference*, sections 4
   (execution model) and 7 (simple statements).
5. This course: [Desugaring](desugar.md), [Closures](closures.md).
