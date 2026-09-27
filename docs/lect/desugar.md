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


# Desugaring: What Runs Under Your Code

**Links:** [Home](../../README.md) · [Closures](closures.md) ·
[N4 architecture](n04.md) · [N6 patterns](n06.md)

Think about what happens inside a computer. If you thought "stack
and heap", then welcome to 1945.

Every language gives you big, friendly constructs: loops,
comprehensions, objects, `async/await`. Each one **desugars** into
a smaller construct. The small set is old: Church defined it in the
1930s as a variable, a function, and a call. Tonight we desugar the
familiar things down to that set, and then use that set to do
things the 1945 machine cannot.

---

## 1. Welcome to 1945

In June 1945, John von Neumann circulated *First Draft of a Report
on the EDVAC*. It is 101 pages, unfinished, and it fixed the shape
of computing for the next eighty years. (It also carries only his
name, which annoyed the ENIAC engineers, Eckert and Mauchly, who
had the ideas too.)

The memo divides a machine into five organs:

| Organ | Job |
|---|---|
| **M** memory | holds numbers **and** instructions, in one address space |
| **CA** arithmetic | adds, multiplies, compares |
| **CC** control | reads the next instruction, tells CA what to do |
| **I**, **O** | input, output |
| **R** recording | outside storage |

Two decisions in there matter more than the rest:

1. **One memory for code and data.** So a program is just numbers.
   So programs can read and write programs. Compilers, linkers,
   interpreters, JITs, and your LLM writing Python all stand on
   that one line.
2. **One control unit, one step at a time.** Fetch, decode,
   execute, repeat. The machine has exactly one place where it is
   "up to".

Everything you call "how a computer works" follows from those two:

```
   +-----------------+
   |  code           |   instructions, loaded once
   +-----------------+
   | static, globals |   lifetime = whole program
   +-----------------+
   |  stack          |   one frame per active call: locals,
   |       |         |   arguments, return address.
   |       v         |   grows down, dies on return
   |                 |
   |       ^         |
   |       |         |
   |  heap           |   grows up: objects you allocate,
   +-----------------+   lifetime up to you
```

Note what the stack is: **one frame per call, released on return**.
That convention is not even in the 1945 memo. It arrived in the
1950s, when Algol wanted recursion (Samelson and Bauer). Fortran
had no stack, so it had no recursion until Fortran 90.

So when you picture "the computer", you picture one design from one
memo, plus one 1950s patch. Other designs exist. They ship today,
and they are why your language has features this machine cannot
support.

---

## 2. Where the 1945 machine pinches

One instruction pointer, one control stack, flat memory. Fast, and
limited in three ways you have already hit:

- **Recursion has a ceiling.** CPython stops near depth 1000,
  because every call burns a real frame. Scheme mandates tail-call
  elimination, so the same loop written as recursion uses *one*
  frame forever. Same algorithm, same source, different machine
  underneath.
- **A frame dies on return.** So a plain stack cannot store "the
  rest of the work, to resume later". Every generator, coroutine,
  and `await` in your stack needs a frame that outlives its
  return, which means the heap.
- **The bottleneck is the wire.** Backus named it in his 1978
  Turing lecture: the CPU pulls one word at a time through a
  narrow channel, so your program becomes a long list of
  assignments that shuffle words. He asked whether programming
  could be "liberated from the von Neumann style".

So what do we get if we leave? The options under the hood include
graph reduction, continuation-passing style, trampolines, and
coroutines. Each option adds constructs you can write in your
source. Next section shows the first prize: an algorithm that gets
cheaper because the machine decides *when* to compute, not you.

---

## 3. Lazy sort: pay only for what you read

Here is quicksort in Haskell. Read it as a definition, not as a
procedure.

```haskell
qsort []     = []
qsort (x:xs) = qsort smaller ++ [x] ++ qsort larger
  where smaller = [a | a <- xs, a <= x]
        larger  = [a | a <- xs, a >  x]
```

Now ask for the best 10% of a million rows:

```haskell
best :: [Int] -> [Int]
best xs = take (length xs `div` 10) (qsort xs)
```

A stack machine sorts one million rows, then throws 900,000 away.
Haskell does not. `take` pulls one element at a time. `++` hands
back its left side lazily. So `qsort larger` at the top level is
never split at all, and `smaller` is scanned only as far as the
elements you actually read.

Measured — lazy quicksort over 20,000 random numbers, comparisons
counted:

| you ask for | comparisons | share of a full sort |
|---|---|---|
| `take 1` | 25,277 | 3.7% |
| `take 10` | 25,308 | 3.7% |
| `take 100` | 28,285 | 4.1% |
| `take (n/10)` | 77,888 | 11% |
| the whole list | 688,018 | 100% |

The curve is `O(n + k log k)`, not `O(n log n)`: one pass to find
the k smallest, then a sort of just those k. Note row 1. `head
(qsort xs)` is a linear-time minimum, and nobody wrote a `minimum`
function.

The source never says "be lazy". The source says *what* the answer
is. The machine chooses *when*. That gap is the whole lecture.

Python makes you ask, explicitly:

```python
import heapq
top = heapq.nsmallest(len(xs) // 10, xs)   # partial sort only
```

---

## 4. A lambda body is inert text

Why can a machine delay work? Because a function body is data
until something calls it. Lisp shows this with no syntax in the
way.

```lisp
(defparameter f (lambda (x) (list x x 'done)))
```

Nothing ran. `(list x x 'done)` is a stored body plus one
parameter name. Supply an argument, and the machine substitutes it
into the body, then evaluates:

```lisp
(funcall f 10)
;; substitute x := 10   -> (list 10 10 'done)
;; evaluate             -> (10 10 DONE)

(funcall f 'cat)
;; substitute x := cat  -> (list 'cat 'cat 'done)
;; evaluate             -> (CAT CAT DONE)
```

Two calls, two answers, one body. That substitution step has a
name: **beta reduction**. It is the only computation rule in lambda
calculus. No program counter, no stack, no memory cells.

A lambda with no parameters is therefore a *delay button*:

```lisp
(defparameter slow (lambda () (expensive-thing)))  ; nothing happens
(funcall slow)                                     ; now it happens
```

A zero-argument lambda is a **thunk**. Lazy evaluation is thunks,
plus a rule about calling them late.

---

## 5. An infinite list is a thunk

Haskell writes `[0,2..]` and means every even number. That is
sugar. Under it, a list is two things:

1. the value **now**;
2. a thunk that returns the **next** list.

No storage, no end, no loop. Common Lisp returns both with
`values`:

```lisp
(defun evens (n)
  (lambda () (values n (evens (+ n 2)))))
```

`(evens 0)` builds a thunk. Call it and you get `0`, plus a thunk
for `(evens 2)`. Take three:

```lisp
(multiple-value-bind (now next) (funcall (evens 0))
  (print now)                              ; 0
  (multiple-value-bind (now2 next2) (funcall next)
    (print now2)                           ; 2
    (print (funcall next2))))              ; 4 (and another thunk)
```

The list of all even numbers exists. Three cells were built. This
shape is a **continuation**: a value, plus the rest of the work
held as a function. A stack frame cannot do this, because a stack
frame dies on return (section 2). A closure survives.

---

## 6. A `for` loop is a drained generator

Add an end marker. A finished stream returns `nil`:

```lisp
(defun evens (n limit)
  (lambda ()
    (if (> n limit)
        nil                                      ; end of stream
        (values n (evens (+ n 2) limit)))))
```

One lambda, with the test inside it. So the check happens when the
caller pulls, not when the stream is built. Hold that shape: the
Lua and JavaScript versions below are the same three lines.

Now the loop. It calls, it uses, it repeats, it stops on `nil`:

```lisp
(defun each (stream f)
  (multiple-value-bind (now next) (funcall stream)
    (when now
      (funcall f now)
      (each next f))))

(each (evens 0 20) #'print)   ; 0 2 4 6 8 10 12 14 16 18 20
```

That is `for`, in five lines. Every `for` loop you have written is
this: ask the source for one item, stop at the end marker.

One warning about markers. Here `nil` means "no more", but `nil` is
also a legal value, so a stream that yields `nil` ends early. Real
languages use a marker no value can fake: Python raises
`StopIteration`, Rust returns `Option::None`, Go returns a second
boolean.

Lua makes the rule explicit. Generic `for` calls a function until
it returns `nil`:

```lua
local function evens(limit)
  local n = -2
  return function()                  -- the closure holds n
    n = n + 2
    if n <= limit then return n end  -- nil ends the loop
  end
end

for n in evens(20) do print(n) end
```

JavaScript, same stream, hand-built:

```js
const evens = (n, limit) => () =>
  n > limit ? null : [n, evens(n + 2, limit)];

for (let s = evens(0, 20), cell; (cell = s()); s = cell[1])
  console.log(cell[0]);
```

JavaScript also ships the sugar. `yield` builds that thunk chain
for you:

```js
function* evens(limit) {
  for (let n = 0; n <= limit; n += 2) yield n;
}
for (const n of evens(20)) console.log(n);
```

Python ships the same sugar, and lets you see the machine:

```python
def evens(limit):
    n = 0
    while n <= limit:
        yield n
        n += 2

it = iter(evens(20))              # for-loop, desugared
while True:
    try: print(next(it))          # ask for one
    except StopIteration: break   # the end marker
```

---

## 7. Python's sad lambda (read at home)

Python restricts `lambda` to one expression. No statement, no
assignment. You can still build the whole stream, and the result
shows why Python added generators:

```python
evens = lambda n, limit: (
    lambda: None if n > limit else (n, evens(n + 2, limit)))

s = evens(0, 20)
while (cell := s()):
    print(cell[0])
    s = cell[1]
```

Python's lambdas work but they are a little ugly and restrictive.
So Python moved the power out of `lambda` and into two other
constructs: generators (section 6) and comprehensions (section 8).

---

## 8. Comprehensions: run the function in place

A comprehension is a fused `map` and `filter`. The lambda is
written inline, so it needs no name:

```python
out = [x * x for x in range(5) if x % 2 == 0]

# same thing, lambdas visible
out = list(map(lambda x: x * x, filter(lambda x: x % 2 == 0, range(5))))
```

Change the brackets and section 5 comes back — a lazy stream of
thunks, with no list in memory:

```python
out = (x * x for x in range(1_000_000_000))
next(out)     # 0     one cell built, not a billion
```

Same expression. Square brackets buy storage. Round brackets buy a
continuation.

---

## 9. The desugaring table

| You write | Machine runs |
|---|---|
| `for x in xs` | call a thunk until it returns the end marker |
| `[f(x) for x in xs]` | `map` + `filter`, fused |
| `(f(x) for x in xs)` | value now + thunk for the rest |
| infinite list | thunk that returns `(now, next)` |
| object with fields | closure over local variables ([closures](closures.md)) |
| method dispatch | lookup in a chain of dictionaries |
| `async`/`await` | generator + a scheduler that resumes it |
| `try`/`except` | jump to a saved continuation |

Row 7 deserves a second look. `await` marks a pause point. The
compiler splits your function at each pause and stores the rest as
a thunk on the heap. Your "sequential" async code is section 5 with
better syntax.

---

## 10. What a shipped body buys you

A lambda body is a value. So you can **send a rule to the place
that needs it**, instead of dragging data back to the place that
holds the rule.

### 10.1 The model tells the dialog what is valid

The dialog layer must reject a bad person. The dialog layer must
not know what a person is. So the model ships a checker. That
checker returns error strings for the dialog, or nothing, in which
case the dialog passes the record on:

```python
# model layer: the rule, as a value
def person_check(min_age=18):
    def check(rec):
        errs = []
        if not rec.get("name"):          errs.append("name is required")
        if rec.get("age", 0) < min_age:  errs.append(f"age must be >= {min_age}")
        return errs                      # [] means valid
    return check

# dialog layer: knows nothing about people
def dialog(fields, check):
    errs = check(fields)
    return ("redraw", errs) if errs else ("send", fields)

dialog({"name": "",    "age": 12}, person_check())
# ('redraw', ['name is required', 'age must be >= 18'])
dialog({"name": "Ada", "age": 36}, person_check())
# ('send', {'name': 'Ada', 'age': 36})
dialog({"name": "Kid", "age": 12}, person_check(min_age=10))
# ('send', {'name': 'Kid', 'age': 12})
```

Note the third call. The rule changed and the dialog code did not.
The closure holds `min_age`, so the policy travels with the
function. Three N4 principles arrive at once: one source of truth
for the rule, dependency inversion (the dialog depends on a
function type, not on the model), and open-closed (a new rule needs
no new dialog code).

Web frameworks do exactly this. Validators, route guards,
permission checks, and form widgets are all shipped bodies.

### 10.2 One body, N cores

A pure body needs no shared memory. So you can copy it to many
workers and run it over many rows at once:

```python
from multiprocessing import Pool

def work(row): return row * row      # the body that gets copied

if __name__ == "__main__":
    with Pool(4) as p:
        print(p.map(work, range(8)))  # [0, 1, 4, 9, ..., 49]
```

That is map-reduce, and it is why Amazon's function service is
called Lambda. The pattern scales from 4 cores to 4000 machines,
because nothing in `work` points at anything local.

One hard constraint: the body must be **shippable**. CPython
pickles a function by name, so a lambda cannot cross a process
boundary:

```python
with Pool(2) as p: p.map(lambda r: r + 1, range(4))
# PicklingError: Can't pickle <function <lambda>>
```

The constraint bites harder when a body closes over mutable state.
Then each worker gets its own copy and the answers diverge. Purity
is not style advice here. Purity is what makes a body portable.

Machine-learning stacks push this hardest. JAX traces your lambda
into a graph, then `jit` compiles it, `vmap` batches it, and `pmap`
replicates it across N accelerators. One body, many devices.

### 10.3 The rest of the catalogue (read at home)

| Use | The body is... |
|---|---|
| Callbacks, event handlers, routes | code to run when something happens |
| Strategy / dependency injection | the policy, passed in, not a flag |
| Retry, timeout, circuit breaker | work to attempt again |
| Transactions, locks, `with` blocks | work to wrap in setup and teardown |
| Job queues (Celery, Sidekiq) | a serialized thunk in a database |
| Caching, memoization, lazy config | work to run once, at most |
| ORMs and query builders (LINQ) | data, inspected and compiled to SQL |
| Undo stacks | the inverse action, saved |
| Property-based tests | a generator plus a law to check |
| Capability security | limited access, handed to untrusted code |
| React hooks, effects | work the framework schedules later |

Read the middle column. Nine of eleven rows are the sentence from
section 5: a value, plus the rest of the work.

---

## 11. Case study: JavaScript in ten days

Brendan Eich wrote the first JavaScript in about ten days, in May
1995. Ten days is not enough time to invent a language. It was
enough because he did not invent one.

- The **semantics** came from decades of work on lambda bodies:
  Church (1936), Lisp (1960), Scheme (1975), and the Steele and
  Sussman papers showing that closures express everything
  imperative languages built special forms for. Eich was hired to
  "put Scheme in the browser". First-class functions and closures
  arrived already proven.
- The **syntax** came from Java and C, because management wanted a
  familiar look.
- The **objects** came from Self: prototypes, not classes.

Everything JavaScript grew later is sugar on that 1995 core.
Callbacks are closures. Promises are closures holding a state
machine. Generators are continuations. `async/await` is a generator
plus a driver. `class` is a prototype chain wearing keywords. The
core held for 30 years because the theory under it was settled
before the deadline started.

The engineering claim: your design survives when it sits on a
theory somebody already proved. Your schedule survives for the same
reason.

---

## 12. Where to go next (read at home)

1. **Continuations in your own stack.** Read how `async/await`
   desugars in your language. Then describe a race condition in
   proj3 as two continuations resuming in the wrong order.
2. **CPS and trampolines.** Rewrite a deep recursion as a loop over
   thunks. That is how compilers beat the recursion ceiling from
   section 2.
3. **Streams as architecture.** Unix pipes, RxJS, and Kafka are
   section 5 at three scales: value now, the rest on demand.
4. **Immutability.** Persistent trees give cheap history. Git is
   one. CRDTs are another.
5. **Macros.** Lisp lets you write the sugar yourself. Then a
   design pattern becomes a language feature instead of a page of
   boilerplate.

---

## Try this

1. **Find the drain.** Take one `for` loop from your proj2 repo.
   Rewrite it with `iter` and `next` and an explicit stop. State
   what the end marker is.
2. **Lazy top-k.** Sort 1,000,000 random numbers and slice the
   first 100. Then use `heapq.nsmallest`. Time both. Report the
   ratio, and compare it to the table in section 3.
3. **Build one stream.** Write the `(now, next)` thunk for the
   Fibonacci numbers in any language here. Do not use `yield`.
4. **Ship a rule.** Find one validation check in your proj2 UI
   code. Move it into the model as a function returning a list of
   error strings. Count the lines you deleted from the UI.
5. **Break a body.** Run `Pool.map` over a function that closes
   over a mutable counter. Report the answer you get, and why it is
   wrong.
6. **Hit the ceiling.** Write a recursive sum over a list of
   100,000 items. Report the error. Then name the machine from
   section 2 that would run it.
7. **Spot the sugar.** Name one construct in your stack that you
   cannot desugar. Bring it to class.

## References

1. von Neumann, "First Draft of a Report on the EDVAC", June 1945.
2. Samelson & Bauer, "Sequential Formula Translation", 1960. The
   stack, added later.
3. Church, "An Unsolvable Problem of Elementary Number Theory",
   1936.
4. Backus, "Can Programming Be Liberated from the von Neumann
   Style?", 1978 Turing Award lecture.
5. Hughes, "Why Functional Programming Matters", 1990. The lazy
   evaluation argument, with alpha-beta search as the example.
6. Steele & Sussman, "Lambda: The Ultimate Imperative", 1976.
7. Norvig, [Lispy](http://norvig.com/lispy.html), 2010. A working
   Lisp in ~30 lines of Python.
8. Eich, "A Brief History of JavaScript", 2010.
