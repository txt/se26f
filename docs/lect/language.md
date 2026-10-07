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

# Language Comparisons: One Idea, Many Tongues

**Links:** [Home](../../README.md) · [Desugaring](desugar.md) ·
[Closures](closures.md) · [patterns](n06.md)

[Desugaring](desugar.md) showed every language melts down to the
same core: a variable, a function, a call. So why thousands of
languages? Because a language is not its core. A language is a
**stack of opinions**: what to make easy, what to make impossible,
when to catch your mistakes, and who pays when nobody does.
Tonight: the same small ideas run through six languages; read the
opinions off the diffs.

You know Python and some JavaScript. Every other language here
gets a three-line introduction before it gets used. The goal is
not fluency in six languages; it is reading unfamiliar code and
seeing which decisions the language already made for its author.

---

## 0. Why bother, in the LLM age

Your LLM writes passable code in every language in this lecture.
So why study them? Because in 2026 **reviewing code is the power
skill**, and you cannot review what you cannot read.

Three stories set the stakes:

- **CrowdStrike, July 2024.** One bad update, in low-level C++
  inside the Windows kernel: airlines grounded, hospitals on
  paper, ~$5.4B lost. The fix needed people who could read all
  the way down the stack.
- **Cloudflare, November 2025.** Three-hour outage, a large slice
  of the web dark (~$1.6B lost trading volume). When it breaks,
  someone reads the actual code, in whatever language. "The LLM
  wrote it" is not an incident report.
- **left-pad, March 2016.** One developer deleted an 11-line
  JavaScript function from npm and thousands of projects stopped
  compiling. The lesson is **supply chains**: every dependency is
  code you own but did not read, written under opinions you may
  not share. npm today: 3.1 million packages.

Counter-story: Richard Hipp built SQLite — the most deployed
database on Earth, in every phone in this room — with a tiny
team, few dependencies, and tests outnumbering code hundreds to
one. He calls the style "backpacking": carry only what you can
check yourself. Knowing more languages shrinks your pack: you
learn which features are load-bearing and which are luggage.

Closer to your projects: **your LLM has a house style per
language.** Java gets factories, Python gets dataclasses, Rust
gets ten lines of error handling you did not request. Know one
language only and you cannot tell the LLM's habits from the
language's requirements — and you will review both badly.

---

## 1. The map: three axes of difference

The floor is shared (lambda calculus — [desugaring](desugar.md));
objects are closures in pretty syntax ([closures](closures.md)).
So the differences live upstairs. Three axes cover most of it:

| Axis | The question | Tonight's examples |
|---|---|---|
| **Dispatch** | When you write `a + b`, how does the machine find the code to run? | Python dunders vs Lua metamethods (§2) |
| **Checking** | When are your mistakes caught — compile time, run time, or production? | JS → TypeScript → Rust (§3) |
| **Control** | Who drives — your statements, a search engine, or the objects themselves? | Prolog, Smalltalk (§4) |

One diagonal axis across all three: **general-purpose vs
domain-specific** — how much of the problem the language already
knows (§5, §6).

Keep the [patterns lecture](n06.md) rule in hand all night: *no
design is best; every design is a purchase* — and a language is
the purchase you make before all the others.

---

## 2. Dispatch: Python dunders, Lua metamethods

Start with code you know. Python overloads operators with
**dunder methods**:

```python
class Wallet:
    def __init__(self, money): self.money = money
    def __repr__(self):        return f"${self.money}"
    def __add__(self, other):  return Wallet(self.money + other.money)

w1, w2 = Wallet(50), Wallet(20)
print(w1 + w2)                 # $70
```

`w1 + w2` desugars to `type(w1).__add__(w1, w2)`. The operator is
a fixed spelling; the dunder is the hook. Everything "magic" in
Python objects — printing, indexing, iteration, context managers
— is one of about eighty such hooks.

The comparison language. **Lua**: a famously small scripting
language (~30k lines of C; runs inside games, Redis, nginx, your
TV). Syntax tour:

- One data structure: the **table** — a hash map that also acts
  as an array. `{money = 50}` is a table.
- Functions are values. `--` starts a comment.
- `setmetatable(t, m)` attaches table `m` to `t`; when an
  operation on `t` has no obvious meaning, Lua consults `m` for a
  handler — a **metamethod**.

The same Wallet:

```lua
Wallet = {}
Wallet.__index = Wallet          -- "look here for missing keys"

function Wallet.new(m)
  return setmetatable({money = m}, Wallet)
end

function Wallet.__tostring(w)    return "$" .. w.money end
function Wallet.__add(w1, w2)    return Wallet.new(w1.money + w2.money) end

w1, w2 = Wallet.new(50), Wallet.new(20)
print(w1 + w2)                   -- $70
```

Same behavior, nearly the same hook names:

| You write | Python hook | Lua metamethod |
|---|---|---|
| `print(x)` | `__repr__` / `__str__` | `__tostring` |
| `x + y` | `__add__` | `__add` |
| `x == y` | `__eq__` | `__eq` |
| `x < y` | `__lt__` | `__lt` |
| `len(x)` / `#x` | `__len__` | `__len` |
| `x(args)` | `__call__` | `__call` |
| `x.missing` | `__getattr__` | `__index` |
| `x.k = v` (intercepted) | `__setattr__` | `__newindex` |

Two languages, independently maintained, converged on one design:
**an object system is a dispatch protocol — a fixed set of named
hooks — not a `class` keyword.** Python hides the protocol behind
the keyword; Lua hands you only the protocol.

So watch Lua build inheritance from one hook — the desugaring
table's row *method dispatch = lookup in a chain of dictionaries*,
constructed by hand:

```lua
function isa(parent, t) parent.__index = parent
                        return setmetatable(t, parent) end

Person = {}
function Person.new(name, born)
  return isa(Person, {name = name, born = born})
end
function Person.__tostring(p)
  return p.name .. " is " .. (2026 - p.born) .. " years old"
end

Employee = isa(Person, {})       -- Employee inherits from Person
function Employee.new(name, born, job)
  local e = Person.new(name, born)
  e.job = job
  return isa(Employee, e)
end
function Employee.__tostring(e)  -- override
  return e.name .. " (" .. e.job .. ")"
end

print(Person.new("Tim", 2000))          -- Tim is 26 years old
print(Employee.new("Jane", 1995, "programmer"))  -- Jane (programmer)
```

Lookup on an `Employee` misses, falls through `__index` to
`Employee`, misses, falls through to `Person`. That IS Python's
method resolution order with the curtain removed — the closures
lecture's claim made literal: no class machinery, just tables,
functions, one lookup rule.

**Lesson.** Languages differ in which layer you may touch:
Python's protocol is semi-open (overload `+`, but not lookup
itself), Lua's fully open (lookup is a table entry you can
replace), C++ and Java welded shut. None is "right": an open
protocol is power for framework authors, rope for everyone else.
First review question in any new language: *which hooks does it
expose, and is this codebase using them or abusing them?*

**Try it** (in pairs): without running it, predict what
`Wallet.new(50) + 20` does in the Lua version. Then check the
`__add` body. What would you add so a plain number works on
either side? (Python has the same problem; its answer is
`__radd__`.)

### The reflected-dunder trick: a pipeline language in ten lines

Every binary operator has a reflected twin (`__radd__`, `__ror__`,
`__rmul__`, ...). For `x op y`, Python asks `x`'s dunder first;
on `NotImplemented` it retries `y`'s *reflected* dunder, operands
swapped. Built for mixed arithmetic. Read it as a hook: **the
right-hand object may define the operator even when the left-hand
object is a built-in you cannot edit.** That is enough to bolt a
Unix-style pipeline onto Python:

```python
class Pipe:
    def __init__(self, f): self.f = f
    def __ror__(self, x):  return self.f(x)              # x | p
    def __call__(self, *args):
        return Pipe(lambda x: self.f(x, *args))          # p(args)

@Pipe
def where(xs, ok): return [x for x in xs if ok(x)]
@Pipe
def select(xs, f): return [f(x) for x in xs]
@Pipe
def total(xs):     return sum(xs)

[1, 2, 3, 4] | where(lambda x: x % 2 == 0) \
             | select(lambda x: x * x)     \
             | total                               # 20
```

Trace the first `|`: `list` has no `|` for a `Pipe`, so Python
falls back to `Pipe.__ror__` — our code runs with the list as
`x`. Each stage returns a plain value, so the next `|` repeats,
left to right: a shell pipeline. Ten lines, no new syntax, and
built-ins we never touched now speak a small functional language.
(§5's awk is this idea grown into a whole language; §6 names what
we built: an internal DSL.)

The dispatch lesson: single dispatch asks only the left operand;
this trick works *because* the fallback asks the right one. Next
idea — what if every call asked all its arguments, all the time?

### Multiple dispatch: Julia and CLOS

The Try-it exposed **single dispatch**: `w + 20` becomes
`type(w).__add__(w, 20)` — the method is chosen by the first
argument's type only. Python, Lua, Java, C++ all share this;
`__radd__` is a patch, not a design.

Some problems need the method chosen by **all** argument types.
The classic: collisions in a simulation, where what happens
depends on *both* parties —

| | hits Asteroid | hits Ship |
|---|---|---|
| **Asteroid** | merge into one bigger rock | ship takes damage |
| **Ship** | ship takes damage | both explode |

**Julia** (a numerical language built on this idea) calls the
answer **multiple dispatch**: one function, a family of methods,
and the call picks the method matching the concrete types of
every argument:

```julia
abstract type Body end
struct Asteroid <: Body; size::Float64 end
struct Ship     <: Body; hp::Float64   end

collide(a::Asteroid, b::Asteroid) = Asteroid(a.size + b.size)
collide(a::Ship,     b::Asteroid) = Ship(a.hp - b.size)
collide(a::Asteroid, b::Ship)     = collide(b, a)
collide(a::Ship,     b::Ship)     = "both explode"

collide(Ship(100.0), Asteroid(30.0))   # picks method 2: Ship(70.0)
```

The pair of types at the call site picks the row and column of
the table. A new body type means new methods, no edits to old
code — the open-closed rule of the [patterns lecture](n06.md),
delivered by the dispatcher itself. Julia's arithmetic runs on
the same machinery: `+` is one function with hundreds of methods;
`int + float` selects on both sides, no `__radd__` anywhere.

**CLOS** (the Common Lisp Object System, 1980s) did it first —
methods belong to *generic functions*, not classes:

```lisp
(defclass asteroid () ((size :initarg :size)))
(defclass ship     () ((hp   :initarg :hp)))

(defmethod collide ((a ship) (b asteroid))
  (decf (slot-value a 'hp) (slot-value b 'size)))
(defmethod collide ((a asteroid) (b ship))
  (collide b a))
```

Single-dispatch languages fake this with the visitor pattern from
the [patterns lecture](n06.md): two chained single dispatches, a
class per case, two edit sites per new type. One language's
design pattern is another language's built-in — Norvig's point
from the readings, live.

**Price it.** Buys: the collision table, extensibility in both
directions. Bills: behavior scatters across generic functions —
you can no longer read one class top to bottom and know
everything it does. No design is best; every design is a
purchase.

---

## 3. Checking: the typing ladder, JS → TypeScript → Rust

Same axis, three rungs, one question answered differently at
each: **when do you find out you were wrong?**

### Rung 1: JavaScript — trust, then surprise

Dynamically typed with **implicit coercion**: mismatched operand
types convert silently, by fixed rules. The rules are memorable:

```js
"10" + 1    // "101"   (+ prefers strings: concatenation)
"10" - 1    // 9       (- only works on numbers: coercion)
1 == "1"    // true    (== coerces before comparing)
1 === "1"   // false   (=== compares type AND value)
[] + []     // ""      (yes, really)
```

Every JS style guide bans `==` in favor of `===` — a community
outlawing a core operator of its own language, the opinion "be
forgiving at run time" overruled by experience: forgiving means
silently wrong.

A real function in that world — the incremental mean-and-variance
updater from this course's data tools (Welford's algorithm; `c` a
column summary, `v` a new value):

```js
let add = (c, v) => {
  if (v == "?") return v                 // "?" marks missing data
  c.n++
  if (c.it == "NUM") {
    let d = v - c.mu
    c.mu += d / c.n
    c.m2 += d * (v - c.mu)
  } else c.has[v] = 1 + (c.has[v] || 0)
  return v }
```

Ten lines, fast to write, runs anywhere. Also: `add(numCol,
"3.5")` coerces and "works"; `add(numCol, true)` computes with
`1`; `add(numCol, undefined)` poisons `mu` with `NaN`, which
spreads through every later mean without raising an error. The
user finds that bug in production, as a weird number in a report.

### Rung 2: TypeScript — the same code, annotated

TypeScript is JS plus a **static type checker**: types declared
or inferred, checked before the program runs, then erased — the
output is plain JS:

```typescript
type V = string | number | boolean          // a legal cell value
interface Col { it: "NUM" | "SYM"; n: number; mu: number;
                m2: number; has: Record<string, number> }

const add = (c: Col, v: V): V => {
  if (v == "?") return v
  c.n++
  if (c.it == "NUM") {
    let d = (v as number) - c.mu
    c.mu += d / c.n
    c.m2 += d * ((v as number) - c.mu)
  } else c.has[v as string] = (c.has[v as string] || 0) + 1
  return v }
```

Now `add(5, v)` and `add(c, {})` are compile errors — found at
your desk, not the user's. `it: "NUM" | "SYM"` lists the two
legal strings, so the typo `"NUm"` dies before the program runs.
But see the `as number` casts: we *assert* what the checker
cannot prove. Gradual typing is a retrofit, and the seams show.

How checking-before-running works: the compiler builds a parse
tree and lets types flow up it —

```
     2 + "hello"

        +   <- ERROR: int + str. Stop. Generate no code.
       / \
      2  "hello"
     int  str
```

A static checker proves properties of **all** executions without
running any; tests (the [prompts-and-tests lecture](n02.md))
sample *some* runs — types cover every run, for the narrow class
of errors types can see.

### Rung 3: Rust — make the illegal unrepresentable

Rust's type system is mandatory and strict: no coercion, no null,
and a value that might be absent or multi-typed must say so in
its type. The cell value becomes an **enum** — a type listing its
legal shapes — and every use must `match` all shapes:

```rust
enum V { Str(String), Num(f64), Bool(bool) }

fn add(c: &mut Col, v: &V) {
    if let V::Str(s) = v { if s == "?" { return } }   // missing
    c.n += 1;
    match (&c.it, v) {
        (ColType::NUM, V::Num(x)) => {
            let d = x - c.mu;
            c.mu += d / c.n as f64;
            c.m2 += d * (x - c.mu);
        }
        (ColType::SYM, V::Str(s)) => {
            *c.has.entry(s.clone()).or_insert(0) += 1;
        }
        _ => {}    // the compiler FORCES us to say what else means
    }
}
```

Rung 1's `"3.5"`-into-a-number bug is not caught here — it is
**unwritable**: a string and a number are different arms of `V`,
and no operation confuses them. The compiler also forced the
`_ => {}` arm: "a SYM value arrives at a NUM column" became a
conscious decision, where JS decided silently for us.

The bill: roughly 2–3x the code, a slower edit-compile loop, a
famously steep learning curve. The receipt: entire bug classes
dead before the first run, plus raw machine speed, because:

> **Types let the compiler do at compile time what would
> otherwise happen at run time.**

No boxing, no per-operation type tests, tight memory layout. One
row per opinion:

| | Dynamic (JS, Python, Lua) | Static (TS, Rust) |
|---|---|---|
| **Errors** | the user finds them | the compiler finds them |
| **Speed** | runtime checks everywhere | raw machine code |
| **Proof** | tests cover some runs | types cover all runs |
| **Docs** | read the README, hope | the signatures are the docs |

**Choosing a rung is risk management, not fashion.** A weekend
prototype that mislabels a column costs a weekend: rung 1 is
fine, and fastest. Flight software that mislabels a unit costs a
Mars orbiter: buy every static proof on sale. Course projects sit
between — which is why TypeScript and Python's optional hints
exist. Python is a ladder in one language:

```python
def add(c, v): ...                      # rung 1: nothing checked
def add(c: Col, v: float) -> float: ... # rung 1.5: mypy checks it,
                                        # the run time still ignores it
```

Start loose, tighten the load-bearing seams. Every design is a
purchase; the compiler is the cashier.

**Aside — JS differs from Python on a second axis too.** Its I/O
is **asynchronous** by default: `readFile`/`fetch` return before
results arrive, so this prints `1` first:

```js
fs.readFile("data.txt", "utf8", (err, s) => console.log(s))
console.log(1)              // runs first!
```

`await` makes it look sequential — and the desugaring lecture
told you what it is: a generator plus a scheduler. Different
default, same core. When a language surprises you, ask what
default it changed, not what magic it added.

---

## 4. Control: two paradigm outliers, two small tastes

Everything so far is imperative: you give steps, the machine
takes them. Two languages refuse that deal. The point is the
contrast, not the syntax.

### Taste 1: Prolog — state facts, let the machine search

No steps. You write **facts** and **rules** (what follows from
what), then ask questions; a built-in search engine finds every
answer. Lowercase = constants (`tim`), uppercase = variables
(`X`), `:-` reads "is true if":

```prolog
parent(tim, pat).                % facts: Tim is a parent of Pat
parent(pat, ann).
parent(pat, bob).

grandparent(X, Z) :-             % a rule
  parent(X, Y),
  parent(Y, Z).
```

Ask; the engine backtracks through every combination:

```prolog
?- grandparent(tim, Who).
Who = ann ;
Who = bob.
```

Now the part with no Python equivalent. List membership, defined
by the two shapes a list can have (`[X|_]` = "first element X,
rest ignored"):

```prolog
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).
```

Run it forward, it tests. Run it with a variable, **the same two
lines generate**:

```prolog
?- member(b, [a, b, c]).      % test:     true
?- member(X, [a, b, c]).      % generate: X = a ; X = b ; X = c.
```

The trick scales. `append` run backwards enumerates every way to
split a list — a free generator of test inputs:

```prolog
?- append(X, Y, [1, 2]).
X = [],     Y = [1, 2] ;
X = [1],    Y = [2]    ;
X = [1, 2], Y = [].
```

One relation, many directions; Python's `in` only ever runs one
way. And the habit — *describe the shape of a solution, let
search find instances* — is not exotic. It is SQL (`SELECT`
describes, the planner searches), it is your Makefile (rules
describe, `make` chases dependencies), it is every package
resolver. A `WHERE` clause is Prolog's opinion in work clothes.

### Taste 2: Smalltalk — everything is a message send

Smalltalk (Alan Kay's team, 1970s; gave us "object-oriented",
the GUI, the IDE) has essentially one construct: send an object a
message; the object decides how to respond.

```smalltalk
3 + 4                 "send message '+ 4' to the object 3"
'hello' size          "send 'size' to a string -> 5"
```

Even arithmetic is dispatch — §2's axis at the limit. The shock:
**no if statement**. Conditionals are messages sent to booleans,
carrying **blocks** — deferred code in square brackets, which
[closures](closures.md) lets you recognize as lambdas:

```smalltalk
x > 0
  ifTrue:  [ 'positive' ]
  ifFalse: [ 'not positive' ]
```

`x > 0` evaluates to the object `true` or `false`; each boolean
class has its own `ifTrue:ifFalse:` method that runs the right
block. Loops are the same trick — collections own iteration:

```smalltalk
#(1 2 3 4) select: [ :x | x even ]     "-> (2 4)"
#(1 2 3 4) collect: [ :x | x * 2 ]     "-> (2 4 6 8)"
```

So a **new kind of iterator is trivial** — it is just a method.
Here is one Smalltalk does not ship: walk consecutive pairs.

```smalltalk
Collection >> pairsDo: aBlock
    "run aBlock on each consecutive pair of elements"
    | prev |
    prev := nil.
    self do: [ :x |
        prev ifNotNil: [ aBlock value: prev value: x ].
        prev := x ]

#(3 7 12 20) pairsDo: [ :a :b | Transcript show: (b - a) printString ]
"-> 4 5 8"
```

Note who owns what. The collection owns traversal — **data is
primary**; callers hand in a block — **control is a peripheral
detail** you pass as an argument. That is inversion of control as
the language's default posture, not a framework trick. Compare
Python, where a new iterator means the generator/`__iter__`
protocol, or classic Java, where it means writing an `Iterator`
class: machinery for what is, here, four lines.

Since control flow is library code, **the language extends from
inside itself**: `pairsDo:` and `retryThreeTimes:` look exactly
as built-in as `ifTrue:`. Python seals `if`; Smalltalk seals
almost nothing. You have met the descendants — Ruby blocks,
Rust's `iterator.filter()` chains, every fluent API — and the
closures lecture already priced the move: less boilerplate,
harder stack traces.

---

## 5. Minimalism: why awk wins

From two big paradigms to one tiny language. **awk** (1977;
`gawk` is the GNU version) processes text streams. The entire
program model:

```awk
pattern { action }
```

Each input line is tested against each pattern; matches run the
action. No pattern = every line; no action = print. Variables
appear on first use (as `0` or `""`); every array is a map. That
is nearly the whole language, and it fits in one-liners:

```sh
gawk '$3 > 100'  data.txt                    # lines whose 3rd field > 100
gawk '/ERROR/ { n++ } END { print n }' app.log   # count ERROR lines
```

Word frequency:

```sh
gawk '{ for (i=1; i<=NF; i++) Count[$i]++ }
      END { for (w in Count) print w, Count[w] }' file.txt
```

Two lines: no imports, no file-open ceremony, streaming on any
input size (`NF` = fields on this line, `$i` = field `i`, `END` =
after input ends). Proper Python: 10–15 lines. Java: a class.

Real machine learning in 20 lines: Naive Bayes — learn with
`Freq[class, col, value]++`, classify by summing log-likelihoods.
Benchmarked against WEKA (the industrial Java data-mining
workbench) on 15 standard datasets: accuracy equal or better on
11, faster on 10, zero dependencies versus megabytes of
framework.

Twenty lines cannot beat a framework in general. The narrow,
useful lesson: **a language that already knows your domain makes
whole programs disappear** — awk programs approach the size of
their own specification. §0's backpack question, made practical:
before importing the 3.1-million-package ecosystem, ask what the
twenty-line version fails to do. Sometimes the answer is "nothing
I need this month" — then you own all the code you run, and (the
[first lecture](n01.md)'s aislop evidence in reverse) there is
less of it to rot.

---

## 6. The far end of the axis: DSLs and the elbow test

awk is domain-specific but still general-ish. At the axis's end
sits the **domain-specific language (DSL)**: a notation fitted so
tightly to one problem that a domain expert learns it in under a
day. SQL, regex, Makefiles, YAML: you use five DSLs before lunch.

Fowler's domain-fit test, in this course's sharper phrasing: the
**elbow test**. Show your code to the domain expert. Do they
*elbow you out of the way* to fix what is obviously wrong? Yes:
your notation speaks their language, and the only people who know
what the system should do just became reviewers. No: the domain
logic is buried under infrastructure — Brooks's **accidental
complexity** — and only you can maintain it.

Two flavors:

| Style | Mechanism | Examples |
|---|---|---|
| **External** | parse your own little syntax, interpret it | SQL, regex, Graphviz dot |
| **Internal** | bend a host language until code reads domain-like | pytest fixtures, Rails routes, the model below |

Internal is far cheaper, and you have already written one — the
[prompts-and-tests lecture](n02.md)'s diapers simulator:

```python
class Diapers(Model):
    def have(i):
        return o(C=S(100), D=S(0), q=F(0), r=F(8), s=F(0))

    def step(i, dt, t, u, v):
        def saturday(x): return int(x) % 7 == 6
        v.C += dt * (u.q - u.r)      # clean: washed in, worn out
        v.D += dt * (u.r - u.s)      # dirty: worn in, washed out
        v.q  = 70 if saturday(t) else 0
        v.s  = u.D if saturday(t) else 0
```

The split: `Model.run()` is the **engine** — time, state vectors,
the loop, zero domain knowledge. `have()` and `step()` are the
**rules** — stocks, flows, laundry day, zero infrastructure. A
parent who has never programmed reads `v.C += dt*(u.q - u.r)` as
"clean diapers go up by what's washed, down by what's used" and
can argue with it. Elbow test passed, in Python, no parser
written.

Engine/rules is the cut you have been making all month: the
[architecture lecture](n04.md)'s microkernel, the [patterns
lecture](n06.md)'s open-closed registries, the desugaring
lecture's shipped-rule brokers. A DSL takes it one step further:
*the plug-in layer gets so clean that non-programmers own it.*
And because rules are plain data/code, they can generate other
artifacts — diagrams, linters, tests. The rules become the
documentation.

The discipline in one line (James Martin, 1967, still
undefeated): the analyst's job is not to write the application
but to **build tools that let the user community write and
maintain their own knowledge.** When your proj3 pitch says "a
framework others extend", this is the bar.

---

## 7. Close: the comparison habit

Six languages, one spine:

| Language | Its loudest opinion | What it costs |
|---|---|---|
| Python | one obvious way; protocol half-hidden | magic you use before you understand |
| Lua | give them one structure and all the hooks | you build (or download) your own object system |
| JavaScript | never stop, coerce and continue | errors surface far from their cause |
| TypeScript | prove what you can, erase, ship JS | cast-shaped seams where proof runs out |
| Rust | if it compiles, big bug classes are gone | 2–3x the code; the compiler argues back |
| Prolog | say what is true; search does the rest | performance and debugging live in the search you don't see |
| Smalltalk | everything, even `if`, is a message | nothing is sealed, so nothing is guaranteed |
| awk | know one domain completely | leave the domain and it fights you |

The habit is the Shaw move (the [patterns lecture](n06.md)) one
level down: same spec, rival languages, read the trade-offs off
the diff — then choose on the columns, not the fashion. The LLM
will happily write your system in any of these; *it* does not pay
for the opinions it picks. You do: in review time, in debugging,
in the 3 a.m. incident where someone reads down the stack.
Engineers know their tools better than anyone else. That job has
not changed just because machines write the first draft.

---

## Before next class

1. **Run the Lua.** Install Lua (`brew install lua` or
   `apt install lua5.4`, or use an online REPL). Type in the
   Wallet from §2. Add `__sub`. Then make `Wallet.new(50) + 20`
   work with a plain number on the right. Three lines; bring them.
2. **Climb one rung.** Take one load-bearing function from your
   proj2 repo and add Python type hints, then run
   `mypy yourfile.py`. Report: one real bug or near-bug the
   checker found, or an honest "nothing — and here is why this
   function was already safe."
3. **Ask your LLM for the same function in two languages** (e.g.
   your §3 `add` in Python and Rust). Diff them. List two things
   the LLM did that the *language* required, and one thing that
   was just the LLM's habit. (This is the [prompts-and-tests lecture](n02.md) cross-examination
   move, aimed at code.)
4. **Elbow-test your project.** Find the one file in your proj2
   repo a domain expert (a non-programmer who knows your app's
   domain) would most need to change. Could they? If not, name the
   accidental complexity standing in their way, in one sentence,
   in your DEBT.md.

## Review questions

**Q1.**
(a) Define "metamethod" in Lua, in one sentence.
(b) The Lua below is meant to make wallets print as `$50`, but
`print(w)` outputs something like `table: 0x7f8...`. Name the one
missing line and state why Lua needs it when Python's class
version does not.

```lua
Wallet = {}
function Wallet.new(m) return {money = m} end
function Wallet.__tostring(w) return "$" .. w.money end
w = Wallet.new(50)
print(w)
```

**Q2.**
(a) State the difference between `==` and `===` in JavaScript, in
one sentence.
(b) A teammate's JS dashboard shows every average as `NaN` after
one CSV row had an empty cell, yet no error was ever raised.
Using the `add` function of §3, explain the causal chain from
empty cell to silent `NaN` — and say which rung of the typing
ladder would have stopped it, and where (compile time or run
time).

**Q3.**
(a) What does Prolog's `:-` mean, in one sentence?
(b) Your build tool resolves package versions by trying
combinations and abandoning dead ends — and a teammate calls that
"just brute force, nothing like a language feature." Using
`member/2` from §4, explain the one Prolog idea (name it) that
both systems share, and why "runs in more than one direction"
describes it.

**Q4.**
(a) State the elbow test, in one sentence.
(b) Your team's pricing rules live in a Python dict that the
business owner edits by pull request — and her last PR broke the
site because she deleted a comma. Does this design pass the elbow
test? Say which half of the engine/rules split (§6) failed her,
and the single change you would make first.

## References

1. Hipp, R., interviewed on SQLite, CoRecursive podcast #66
   ("backpacking" software).
2. The Register, "How one developer just broke Node, Babel and
   thousands of projects in 11 lines of JavaScript", March 2016.
3. Ierusalimschy, R., *Programming in Lua*, 4th ed. Chapter on
   metatables and metamethods.
4. Shaw, M. & Garlan, D., *Software Architecture: Perspectives on
   an Emerging Discipline*, 1996 (the one-spec-many-systems move).
5. Kay, A., "Microelectronics and the Personal Computer",
   *Scientific American*, 1977.
6. Fowler, M., *Domain-Specific Languages*, 2010. Martin, J.,
   *Design of Real-Time Computer Systems*, 1967.
7. Aho, Kernighan & Weinberger, *The AWK Programming Language*,
   1988 (2nd ed. 2023).
8. Norvig, P., "Design Patterns in Dynamic Programming", 1996 —
   why 16 of 23 patterns shrink when the language changes (the
   bridge between this lecture and the [patterns lecture](n06.md)).
