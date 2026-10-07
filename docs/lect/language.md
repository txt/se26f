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

[Desugaring](desugar.md) showed that every language melts down to
the same core: a variable, a function, a call. So why are there
thousands of languages? Because a language is not its core. A
language is a **stack of opinions**: what to make easy, what to
make impossible, when to catch your mistakes, and who pays when
nobody does. Tonight we run the same small ideas through six
languages and read the opinions off the diffs.

You know Python well and some JavaScript. You do not need to know
Lua, TypeScript, Rust, Prolog, or Smalltalk — each gets a
three-line introduction before it gets used. The goal is not
fluency in six languages. The goal is the engineer's skill
underneath: looking at unfamiliar code and seeing which decisions
the language already made for its author.

---

## 0. Why bother, in the LLM age

Your LLM writes passable code in every language in this lecture.
So why study them? Because in 2026, **reviewing code is the power
skill**, and you cannot review what you cannot read.

Three stories set the stakes:

- **CrowdStrike, July 2024.** One bad update, in low-level C++
  running inside the Windows kernel, crashed machines worldwide:
  airlines grounded, hospitals on paper, roughly $5.4B lost. The
  fix required people who could read all the way down the stack.
- **Cloudflare, November 2025.** A three-hour outage took a large
  slice of the web offline (~$1.6B in lost trading volume alone).
  Again: when it breaks, someone must read the actual code, in
  whatever language it is in. "The LLM wrote it" is not an
  incident report.
- **left-pad, March 2016.** One developer deleted an 11-line
  JavaScript function (pad a string on the left) from the npm
  registry, and thousands of projects — including major build
  systems — stopped compiling. Eleven lines. The lesson is about
  **supply chains**: every dependency is code you now own but did
  not read, written under opinions you may not share. npm today
  holds over three million packages.

Against that, a minimalist counter-story. Richard Hipp built
SQLite — now the most deployed database on Earth, in every phone
in this room — with a tiny team, few dependencies, and tests that
outnumber the code by hundreds to one. He calls the style
"backpacking": carry only what you can check yourself. Knowing
more languages is how you shrink your pack: you learn which
features are load-bearing and which are luggage.

One more reason, closer to your projects: **your LLM has a house
style per language.** Ask for Java and get factories; ask for
Python and get dataclasses; ask for Rust and get ten lines of
error handling you did not request. If you only know one language,
you cannot tell the LLM's habits from the language's requirements
— and you will review both badly.

---

## 1. The map: three axes of difference

[Desugaring](desugar.md) gave you the floor: Church's lambda
calculus, 1930s, three constructs. [Closures](closures.md) gave
you the bridge: objects are closures with pretty syntax. If all
languages share that floor, their differences must live upstairs.
Three axes cover most of it:

| Axis | The question | Tonight's examples |
|---|---|---|
| **Dispatch** | When you write `a + b`, how does the machine find the code to run? | Python dunders vs Lua metamethods (§2) |
| **Checking** | When are your mistakes caught — compile time, run time, or production? | JS → TypeScript → Rust (§3) |
| **Control** | Who drives the program — your statements, or a search engine, or the objects themselves? | Prolog, Smalltalk (§4) |

And one diagonal axis across all three: **general-purpose vs
domain-specific** — how much of the problem the language already
knows (§5, §6).

Keep the [patterns lecture](n06.md) rule in hand all night: *no design is best; every
design is a purchase.* That was true of architectures and
patterns. It is truest of languages, because a language is the
purchase you make before all the others.

---

## 2. Dispatch: Python dunders, Lua metamethods

Start with code you know. Python classes can overload operators
with **dunder methods** (double-underscore, "magic" methods):

```python
class Wallet:
    def __init__(self, money): self.money = money
    def __repr__(self):        return f"${self.money}"
    def __add__(self, other):  return Wallet(self.money + other.money)

w1, w2 = Wallet(50), Wallet(20)
print(w1 + w2)                 # $70
```

`w1 + w2` is sugar. Python desugars it to
`type(w1).__add__(w1, w2)`. The operator is a fixed spelling; the
dunder is the hook where your code plugs in. Every "magic" feature
of Python objects — printing, indexing, iteration, context
managers — is one of about eighty such hooks.

Now the comparison language. **Lua** is a scripting language of
famous smallness (the whole implementation is ~30k lines of C; it
runs inside games, Redis, nginx, your TV). Minimal syntax tour:

- One data structure: the **table** — a hash map that also acts
  as an array. `{money = 50}` is a table.
- Functions are values, like Python. `--` starts a comment.
- `setmetatable(t, m)` attaches a second table `m` to `t`. When
  an operation on `t` has no obvious meaning, Lua consults `m`
  for a handler, called a **metamethod**.

Here is the same Wallet:

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

Same behavior, and nearly the same hook names:

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

Two different languages, independently maintained, converged on
the same design: **an object system is a dispatch protocol — a
fixed set of named hooks — not a `class` keyword.** Python gives
you the keyword and hides the protocol; Lua gives you only the
protocol and lets you build the keyword.

Watch Lua build inheritance from one hook. Recall the desugaring
table's row: *method dispatch = lookup in a chain of
dictionaries*. In Python, `class Employee(Person)` constructs
that chain invisibly. In Lua you construct it by hand, and the
chain is just `__index` twice:

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
`Employee`, misses again, falls through to `Person`. That IS
Python's method resolution order, with the curtain removed. And it
is the closures lecture's claim made literal: no class machinery
anywhere, just tables, functions, and one lookup rule.

**The engineering lesson.** Languages differ in which layer they
let you touch. Python's protocol is semi-open (you can overload
`+`, you cannot redefine lookup itself without pain). Lua's is
fully open (lookup is a table entry you can replace). C++ and
Java weld the hood shut. None of these is "right": an open
protocol is power for framework authors and rope for everyone
else. When you review code in a new language, your first question
is now: *which hooks does this language expose, and is this
codebase using them or abusing them?*

**Try it** (in pairs): without running it, predict what
`Wallet.new(50) + 20` does in the Lua version. Then check the
`__add` body. What would you add so a plain number works on
either side? (Python has the same problem; its answer is
`__radd__`.)

### Multiple dispatch: Julia and CLOS

Notice what the Try-it exposed. `w + 20` desugars to
`type(w).__add__(w, 20)` — the method is chosen by the type of
the **first** argument only. That is **single dispatch**, and
Python, Lua, Java, and C++ all share it. `__radd__` exists
because single dispatch cannot see the right-hand type; it is a
patch, not a design.

Some problems genuinely need the method chosen by **all** the
argument types at once. The classic: collisions in a simulation.
What happens depends on *both* parties —

| | hits Asteroid | hits Ship |
|---|---|---|
| **Asteroid** | merge into one bigger rock | ship takes damage |
| **Ship** | ship takes damage | both explode |

**Julia** (a numerical language built on this idea) calls the
answer **multiple dispatch**: a function is a family of methods,
and a call picks the method matching the concrete types of every
argument:

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

Four methods, one name; the pair of types at the call site picks
the row and column of that table. Adding a new body type means
adding methods, touching no existing code — the open-closed rule
from the [patterns lecture](n06.md), delivered by the dispatcher
itself. Julia's arithmetic runs on the same machinery: `+` is one
function with hundreds of methods, and `int + float` selects on
both sides — no `__radd__` anywhere.

**CLOS** (the Common Lisp Object System, 1980s) did it first.
Methods belong to *generic functions*, not to classes:

```lisp
(defclass asteroid () ((size :initarg :size)))
(defclass ship     () ((hp   :initarg :hp)))

(defmethod collide ((a ship) (b asteroid))
  (decf (slot-value a 'hp) (slot-value b 'size)))
(defmethod collide ((a asteroid) (b ship))
  (collide b a))
```

How do single-dispatch languages cope? The visitor pattern from
the [patterns lecture](n06.md) *is* the workaround: two chained
single dispatches faking one double dispatch, at the price of a
class-per-case and edits in two places per new type. One
language's design pattern is another language's built-in — the
Norvig point from the readings, live.

**Price it.** Multiple dispatch buys you the collision table and
extensibility in both directions. The bill: you can no longer
look at one class and read everything it does — behavior lives
in the generic functions, spread across files. Single dispatch
keeps behavior findable under the class; multiple dispatch keeps
it honest when two types genuinely share the decision. No design
is best; every design is a purchase.

---

## 3. Checking: the typing ladder, JS → TypeScript → Rust

Same axis, three rungs. The question each rung answers
differently: **when do you find out you were wrong?**

### Rung 1: JavaScript — trust, then surprise

JavaScript is dynamically typed with **implicit coercion**: when
operand types do not match, it converts them silently by fixed
rules. The rules are... memorable:

```js
"10" + 1    // "101"   (+ prefers strings: concatenation)
"10" - 1    // 9       (- only works on numbers: coercion)
1 == "1"    // true    (== coerces before comparing)
1 === "1"   // false   (=== compares type AND value)
[] + []     // ""      (yes, really)
```

Every JS style guide bans `==` in favor of `===`. Pause on what
that means: the community routinely outlaws a core operator of
its own language. That is a language opinion ("be forgiving at
run time") being overruled by engineering experience ("forgiving
means silently wrong").

Here is a real function in that world — the incremental
mean-and-variance updater from this course's data tools (Welford's
algorithm; `c` is a column summary, `v` a new value):

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
`1`; `add(numCol, undefined)` poisons `mu` with `NaN`, which then
spreads through every later mean without ever raising an error.
The user finds that bug, in production, as a weird number in a
report.

### Rung 2: TypeScript — the same code, annotated

TypeScript is JavaScript plus a **static type checker**: types
are declared (or inferred), checked before the program runs, then
erased — the output is plain JS. It exists because large teams
kept hitting rung-1 bugs at scale:

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
your desk, not the user's. Note `it: "NUM" | "SYM"`: the type is
a list of the two legal strings, so a typo like `"NUm"` dies
before the program runs. But see also the `as number` casts: we
*assert* that a NUM column gets numbers, because the checker
cannot prove it. Gradual typing is a retrofit, and the seams show.

How does checking-before-running work? The compiler builds a
parse tree and lets types flow up it:

```
     2 + "hello"

        +   <- ERROR: int + str. Stop. Generate no code.
       / \
      2  "hello"
     int  str
```

This is the deal in one picture: a static checker proves
properties of **all** executions without running any of them.
Tests (the [prompts-and-tests lecture](n02.md)) sample some runs; types cover every run — for the
narrow class of errors types can see.

### Rung 3: Rust — make the illegal unrepresentable

Rust is a compiled systems language whose type system is
mandatory and strict: no coercion, no null, and any value that
might be absent or multi-typed must say so in its type. Our cell
value becomes an **enum** — a type listing its legal shapes —
and every use must `match` all shapes:

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

The `"3.5"`-into-a-number bug of rung 1 is not caught here — it
is **unwritable**. A string and a number are different arms of
`V`; there is no operation that confuses them. The compiler also
made us write the `_ => {}` arm: "a SYM value arrives at a NUM
column" is a case we must consciously decide about, where JS
decided silently for us.

The bill: the full program this came from is ~390 lines of JS and
~240 of Rust boilerplate *more* than that — roughly 2–3x the
code, plus a slower edit-compile loop and a famously steep
learning curve. The receipt: entire bug classes gone before the
first run, and raw machine speed, because:

> **Types let the compiler do at compile time what would
> otherwise happen at run time.**

No boxing, no per-operation type tests, tight memory layout. The
summary, one row per opinion:

| | Dynamic (JS, Python, Lua) | Static (TS, Rust) |
|---|---|---|
| **Errors** | the user finds them | the compiler finds them |
| **Speed** | runtime checks everywhere | raw machine code |
| **Proof** | tests cover some runs | types cover all runs |
| **Docs** | read the README, hope | the signatures are the docs |

**Choosing a rung is risk management, not fashion.** A weekend
prototype that mislabels a column costs you a weekend: rung 1 is
fine, and fastest. Flight software that mislabels a unit costs a
Mars orbiter: you want every static proof you can buy. Most
course projects sit between — which is exactly why TypeScript and
Python's optional type hints exist: start loose, tighten the
load-bearing seams. (That is "every design is a purchase" again,
with the compiler as the cashier.)

**One aside before we leave JS** — it differs from Python on a
second axis too. JS I/O is **asynchronous** by default: calls
like `fetch` return immediately and deliver results later, so
this prints `1` *before* the file arrives:

```js
fs.readFile("data.txt", "utf8", (err, s) => console.log(s))
console.log(1)              // runs first!
```

`await` makes it look sequential again — and the desugaring
lecture told you what it really is: a generator plus a scheduler.
Different default, same core. That is this lecture's whole method
in one example: when a language surprises you, ask what default
it changed, not what magic it added.

---

## 4. Control: two paradigm outliers, two small tastes

Everything so far — Python, Lua, JS, TS, Rust — is imperative:
you give steps, the machine takes them. Two languages refuse that
deal entirely. The point is the contrast, not
the syntax.

### Taste 1: Prolog — state facts, let the machine search

In Prolog you do not write steps. You write **facts** and
**rules** (what follows from what), then ask questions; a built-in
search engine finds every answer. Conventions: lowercase names
are constants (`tim`), uppercase are variables (`X`), `:-` reads
"is true if".

```prolog
parent(tim, pat).                % facts: Tim is a parent of Pat
parent(pat, ann).
parent(pat, bob).

grandparent(X, Z) :-             % a rule
  parent(X, Y),
  parent(Y, Z).
```

Ask, and the engine backtracks through every combination:

```prolog
?- grandparent(tim, Who).
Who = ann ;
Who = bob.
```

Now the part with no Python equivalent at all. Here is list
membership, defined by the two shapes a list can have (`[X|_]` is
"first element X, rest ignored"):

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

One relation, multiple directions of use. A Python `in` only ever
runs one way; you would write a separate loop to enumerate. The
Prolog habit — *describe the shape of a solution, let search find
instances* — is not exotic. It is SQL (`SELECT` describes, the
planner searches), it is your Makefile (rules describe, `make`
chases dependencies), it is every constraint solver and package
resolver you use. When you next read a `WHERE` clause, you are
reading Prolog's opinion wearing work clothes.

### Taste 2: Smalltalk — everything is a message send

Smalltalk (Alan Kay's team, 1970s; the language that gave us
"object-oriented", the GUI, and the IDE) has essentially one
construct: send an object a message; the object decides how to
respond.

```smalltalk
3 + 4                 "send message '+ 4' to the object 3"
'hello' size          "send 'size' to a string -> 5"
```

Even arithmetic is dispatch (§2's axis, pushed to the limit).
But here is the shock. Smalltalk has **no if statement**.
Conditionals are messages sent to booleans, carrying **blocks** —
chunks of deferred code in square brackets, which you will
recognize from [closures](closures.md) as lambdas:

```smalltalk
x > 0
  ifTrue:  [ 'positive' ]
  ifFalse: [ 'not positive' ]
```

`x > 0` evaluates to the object `true` or the object `false`.
Each CLASS of boolean has its own `ifTrue:ifFalse:` method:
`true` runs the first block, `false` runs the second. Loops are
the same trick — collections own their own iteration:

```smalltalk
#(1 2 3 4) select: [ :x | x even ]     "-> (2 4)"
#(1 2 3 4) collect: [ :x | x * 2 ]     "-> (2 4 6 8)"
```

The consequence: since control flow is library code, **you can
extend the language from inside it**, in the language itself.
Want a `retryThreeTimes:` construct? Write a method; it looks
exactly as built-in as `ifTrue:`. Python lets you overload `+`
but `if` is sealed syntax; Smalltalk seals almost nothing. You
have met the descendants: Ruby blocks, Rust's `iterator.filter()`
chains, every fluent API that "reads like English" — and §2's
closures lecture already showed you the price and the prize of
handing control to the callee (inversion of control: less
boilerplate, harder stack traces).

---

## 5. Minimalism: why awk wins

From two big paradigms to one tiny language. **awk** (1977;
`gawk` is the GNU version) processes text streams. Its entire
program model is:

```awk
pattern { action }
```

Every input line is tested against each pattern; matches run the
action. No pattern means "every line". No action means "print".
Variables need no declaration (they appear, as `0` or `""`), and
every array is an associative map. That is nearly the whole
language. Now watch it work. Word frequency:

```sh
gawk '{ for (i=1; i<=NF; i++) Count[$i]++ }
      END { for (w in Count) print w, Count[w] }' file.txt
```

Two lines: no imports, no file-open ceremony, no declarations,
streaming (constant memory on any size input). `NF` is the number
of fields on the line, `$i` is field `i`, `END` runs after input
ends. The same program in "proper" Python is 10–15 lines; in Java,
a class.

Toy-sized tricks? A Naive Bayes classifier — a real machine
learning algorithm — is about 20 lines of awk (count value
frequencies per class with `Freq[class, col, value]++`; classify
by summing log-likelihoods). Benchmarked against WEKA, the
industrial Java data-mining workbench, on 15 standard datasets:
equal or better accuracy on 11, faster on 10, zero dependencies
versus megabytes of framework.

Twenty lines cannot beat a framework in general — big data and
rich pipelines eventually need the framework. The honest lesson
is narrower and more useful: **a language that already knows your
domain makes whole programs disappear.** awk knows "stream of
lines, split into fields, counted in maps" so well that programs
in that domain approach the size of their own specification. Your
backpack question from §0, turned practical: before importing the
3.1-million-package ecosystem, ask what the twenty-line version
fails to do. Sometimes the answer is "nothing I need this month"
— and then you own all the code you run, and (the [first lecture](n01.md)'s aislop
evidence in reverse) there is less of it to rot.

---

## 6. The far end of the axis: DSLs and the elbow test

awk is domain-specific but still general-purpose-ish. Push the
axis to its end: the **domain-specific language (DSL)** — a
notation fitted so tightly to one problem that a domain expert
can learn it in under a day. SQL, regex, Makefiles, YAML configs:
you use five DSLs before lunch.

Fowler's test for whether a notation is domain-fit, in this
course's sharper phrasing: the **elbow test**. Show your code to
the domain expert. Do they *elbow you out of the way* to fix what
is obviously wrong? If yes, your notation speaks their language,
and you have just recruited the only people who actually know
what the system should do as reviewers. If no, the domain logic
is buried under infrastructure — what Brooks called **accidental
complexity** — and only you can maintain it.

Two flavors:

| Style | Mechanism | Examples |
|---|---|---|
| **External** | parse your own little syntax, interpret it | SQL, regex, Graphviz dot |
| **Internal** | bend a host language until code reads domain-like | pytest fixtures, Rails routes, the model below |

Internal is far cheaper, and you have already written one. Recall
the [prompts-and-tests lecture](n02.md)'s diapers simulator. Its heart:

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

Look at the split. `Model.run()` is the **engine**: it owns time,
state vectors, the simulation loop — and no domain knowledge.
`have()` and `step()` are the **rules**: pure domain knowledge —
stocks, flows, laundry day — and no infrastructure. A parent who
has never programmed reads `v.C += dt*(u.q - u.r)` as "clean
diapers go up by what's washed, down by what's used" and can
argue with it. That is the elbow test passing, in Python, with no
parser written.

Engine/rules is the same cut you have been making all month:
the [architecture lecture](n04.md)'s microkernel (core + plug-ins), the [patterns lecture](n06.md)'s open-closed registries,
the desugaring lecture's shipped-rule brokers. A DSL is that
architecture taken one step further: *the plug-in layer gets so
clean that non-programmers own it.* And because the rules are
plain data/code, you can generate other artifacts from them —
diagrams, linters, tests. The rules become the documentation.

The one-line discipline (James Martin, 1967, still undefeated):
the analyst's job is not to write the application; it is to
**write tools that let the user community write and maintain
their own knowledge.** When your proj3 pitch says "a framework
others extend", this is the standard to beat.

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

The habit to take away is the Shaw move (the [patterns lecture](n06.md)) applied one level
down: same spec, rival languages, read the trade-offs off the
diff — then choose on the columns, not the fashion. In the LLM
age this is no longer optional culture. The model will happily
write your system in any of these; *it* does not pay for the
opinions it picks. You do: in review time, in debugging, in the
3 a.m. incident where someone has to read down the stack. Engineers
know their tools better than anyone else. That is the whole job
description, and it has not changed since before the machines
started writing the first draft.

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
