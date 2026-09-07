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


# Closures & Functional Thinking

**Links:** [Home](../../README.md) · [N4 architecture](n04.md) ·
[N6 patterns](n06.md)

*Supplementary reading for the build month. Theory under the hood:
"there's nothing more practical than a good theory" (Kurt Lewin).
The claim of the hour: everything you know about objects is a tiny
corner of closures — and half the Gang-of-Four catalog is one idea,
passing functions around, wearing 23 costumes.*

You have been using closures all along: every callback, every
lambda, every `sort(key=...)`. Tonight's read gives the thing its
name, shows why OOP is (mostly) syntactic sugar over it, and turns
several design patterns from N6 into one-liners.

---

## 1. First-class functions

In Python, functions are values — storable, passable, returnable
like any integer:

```python
def add(x, y):      return x + y
def multiply(x, y): return x * y

operation = add
print(operation(3, 4))   # 7
operation = multiply
print(operation(3, 4))   # 12
```

Same call site, different behavior: that is the open-closed
principle (N4) in four lines. The industrial version is the
**higher-order function** — a function taking or returning
functions:

```python
words = ["alice", "bob", "alexandra", "zoe"]
words.sort(key=len)              # by length
words.sort(key=lambda w: w[-1])  # by last letter
```

`sort` is closed (you never modify it) and open (you re-aim it at
will). Now recall N6's **Strategy pattern** — a class hierarchy
whose whole job is to carry one method into a call. In a language
with first-class functions:

```python
# Strategy, the ceremony:
class SortStrategy:            ...
class LengthSort(SortStrategy): def compare(a,b): return len(a)-len(b)
Sorter(LengthSort()).sort(words)

# Strategy, the idea:
words.sort(key=len)
```

Strategy pattern = passing a function. Keep that move; we will do
it to several more patterns below.

---

## 2. Closures: functions that remember

A **closure** is a function bundled with the variables from where
it was born. It "remembers" its birthplace.

```python
def make_counter():
    count = 0                 # closed over
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

counter1 = make_counter()
counter2 = make_counter()
print(counter1())  # 1
print(counter1())  # 2
print(counter2())  # 1   <- its own count!
```

Each `make_counter()` call creates a fresh `count`, and the
returned function keeps it alive — long after `make_counter` has
returned. A thing that does something, carrying its own private
state: hold that thought.

Two more, quickly:

```python
def make_multiplier(factor):
    return lambda x: x * factor

times_two = make_multiplier(2)      # factor rides inside
times_ten = make_multiplier(10)
```

```python
def setup_button(button_id, message):
    def on_click():
        print(f"Button {button_id}: {message}")
    register_callback(button_id, on_click)
```

The callback is the killer app: each `on_click` remembers ITS
button and ITS message. No globals, no lookup table — the state
travels with the function.

---

## 3. The truth about OOP

Claim: objects are closures with pretty syntax. Proof by example:

```python
# The class version
class BankAccount:
    def __init__(self, balance): self._balance = balance
    def deposit(self, amount):   self._balance += amount
    def get_balance(self):       return self._balance

# The closure version
def make_account(balance):
    def deposit(amount):
        nonlocal balance
        balance += amount
    def get_balance():
        return balance
    return {'deposit': deposit, 'get_balance': get_balance}

account = make_account(100)
account['deposit'](50)
print(account['get_balance']())   # 150
```

Same machine. A "method call" `emp.give_raise(1000)` is really
`Employee.give_raise(emp, 1000)` — `self` is the captured state
being passed by hand. Implications:

1. OOP is one pattern among many, not the substrate.
2. Closures are older (Lisp, 1958) and more fundamental.
3. Modern languages lean functional — Rust, Swift, Kotlin,
   JavaScript's arrow-functions-everywhere.
4. You already knew functional programming; you lacked the name.

---

## 4. Patterns are functions

N6 taught patterns as purchases. Several stop costing anything once
functions are first-class:

**Observer = a list of callbacks.**

```python
observers = []
def notify(data):
    for callback in observers: callback(data)

observers.append(lambda x: print(f"Got {x}"))
observers.append(log)
```

No Subject, no Observer interface, no attach/detach ceremony.

**Template Method = a higher-order function.**

```python
def process(data, transform):
    return write(transform(read(data)))

process(data, str.upper)
process(data, str.lower)
```

**Visitor = a dictionary of functions.**

```python
tax = {'clothing': 0.08, 'electronics': 0.12, 'food': 0.0}
def tax_for(item): return item.price * tax[item.type]
```

(The full visitor earns its keep when the walked structure is
recursive — a tree of prunings, say — but for flat dispatch, a
dict beats a hierarchy.)

The pattern behind the patterns: GoF was written for 1994 Java/C++,
languages where functions could NOT travel alone, so each traveling
function needed a class as luggage. First-class functions are the
luggage-free airline.

---

## 5. Python's functional toolkit

Things you already do that are secretly functional:

```python
# comprehension = map + filter
results = [x*2 for x in numbers if x % 2 == 0]

# generator = lazy stream; a closure that remembers between yields
def numbers(n):
    for i in range(n): yield i

# functools: fold and partial application
from functools import reduce, partial
total  = reduce(lambda acc, x: acc + x, [1,2,3,4,5])   # 15
double = partial(multiply, 2)
```

Generators matter most for this course: `yield` is how you stream
a huge file in O(1) memory, and a generator is literally a closure
— it remembers its locals between calls.

Immutability, the other functional habit: data that never mutates
cannot race, cannot surprise, and is trivially testable (N5: pure
functions need no mocks). Python will not force it on you; adopt
it where cheap — pass new values out rather than mutating
arguments in.

**When NOT to go functional**: performance-critical mutation (game
loops), inherently stateful things (UI, connections), and teams
whose shared style is OOP — consistency beats paradigm purity.
Python is multi-paradigm on purpose.

---

## 6. The theory floor: lambda calculus

Alonzo Church, 1930s: three constructs suffice for universal
computation — variables, function abstraction, function
application. Everything else in every language is sugar. That is
why JavaScript could be built in ten days on a lambda-calculus
core, and why Norvig's [Lispy](http://norvig.com/lispy.html) fits
a working Lisp interpreter in ~30 lines of Python.

Historical note worth retelling: McCarthy described Lisp's theory;
his student Steve Russell said "I could implement that"; McCarthy
said "you're confusing theory with practice"; Russell wrote the
first Lisp interpreter anyway (1960). All students should ignore
their supervisors occasionally.

---

## Try this

1. **Class → closures.** Rewrite `ShoppingCart` (items list,
   `add`, `total`) as `make_cart()` returning closures. Which
   version is easier to test? Which to pickle?
2. **If-ladder → dict.** Replace the
   regular/member/vip discount ladder with a dictionary of
   lambdas. Then answer N6's question: what second requirement
   would justify going further, to full Strategy?
3. **Spot the closure.** Find one callback in your proj2 repo and
   name the variables it closes over. If the answer is "none", ask
   what global state it is quietly reading instead.

## References

1. Abelson & Sussman, *Structure and Interpretation of Computer
   Programs*, 1985.
2. Hughes, "Why Functional Programming Matters", 1990.
3. McCarthy, "Recursive Functions of Symbolic Expressions", 1960.
4. Norvig, "Lispy", 2010. Graham, "The Roots of Lisp", 2001.
