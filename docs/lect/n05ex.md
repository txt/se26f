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


# N5 Exercise: Test the Tests

Homework, with your team, before next class (~30 quiet minutes).
Next week you report, three minutes: your table from Part 2, your
disagreement input from Part 3, and your one-sentence verdict.

The setup: a startup ships this pricing function, and their LLM
wrote them a test suite. It is green. Coverage is 100%. Management
is delighted.

```python
def price(total, coupon):            # total in dollars
    if total > 100:                  # big orders: 10% off
        total = total * 0.9
    if coupon == "SAVE5":            # coupon: $5 off
        total = total - 5
    return max(total, 0)
```

```python
def test_big_order():   assert price(200, "")      < 200
def test_coupon():      assert price(50, "SAVE5")  < 50
def test_no_negative(): assert price(2, "SAVE5")   >= 0
```

## Part 1: coverage says yes (5 min)

Check the brag: which lines and branches do the three tests visit?
Is the 100% claim true? (It nearly is. Note anything unvisited.)

## Part 2: mutation says no (10 min)

Play the mutation tool, by hand. For each mutant below: which of
the three tests fails? If none fails, the mutant SURVIVES — write
the missing assertion that would kill it.

| # | mutant (one token) | killed by? | if survived: killing test |
|---|---|---|---|
| M1 | `total > 100` → `total >= 100` | | |
| M2 | `total * 0.9` → `total * 0.5` | | |
| M3 | `total - 5` → `total - 50` | | |
| M4 | `total > 100` → `total > 10` | | |
| M5 | `max(total, 0)` → `total` | | |

Then compute the suite's mutation score (killed/5) and compare it
to its coverage. One sentence: what disease do weak assertions like
`< 200` have?

## Part 3: differential says which (10 min)

A teammate "cleans up" the function:

```python
def price2(total, coupon):
    if coupon == "SAVE5":            # coupon first "reads better"
        total = total - 5
    if total > 100:
        total = total * 0.9
    return max(total, 0)
```

No oracle needed: `price` and `price2` disagree for some inputs,
and every disagreement is a bug in at least one of them.

1. Find a disagreeing input by hand (hint: think about orders near
   the $100 boundary, with the coupon).
2. Which is RIGHT? Trick question — the spec never said whether the
   discount applies before or after the coupon. You have found a
   requirements bug with a diff (N3 says hello: E2, ambiguity).
3. Write the one-line grammar-fuzzer loop that would have found
   this automatically:
   `for _ in range(1000): t = random(...); assert price(t,c) == price2(t,c)`

## Verdict

One sentence, on the sheet: what do you now tell the delighted
management about their green, 100%-covered, LLM-written suite?

## If your team finishes early

Ask your LLM to write five MORE tests for `price`. Run them (in
your head) against M1-M5. Did the machine's tests raise the
mutation score, or just the coverage?

---

## Tutor's answer key

**Part 1 (coverage).** The claim holds: test_big_order takes
branch 1 true / branch 2 false; test_coupon takes 1-false /
2-true; test_no_negative drives `max` to its 0 arm, the others to
its total arm. All lines, all branch outcomes visited. (Sharp
teams may note the untested INTERACTION big-order+coupon — the
same du-path lesson as lecture segment 2; praise it, it previews
Part 3.)

**Part 2 (mutation).** Only M5 dies. Score 1/5 = 20%, against
~100% coverage.

| # | verdict | why | a killing test |
|---|---|---|---|
| M1 `>=100` | SURVIVES | behavior differs only at total=100 exactly; no test there | `assert price(100,"") == 100` |
| M2 `*0.5` | SURVIVES | price(200,"")=100, still `< 200` — assertion too weak | `assert price(200,"") == 180` |
| M3 `-50` | SURVIVES | price(50,"SAVE5")=0, still `< 50`; the max() clamp hides the damage | `assert price(50,"SAVE5") == 45` |
| M4 `>10` | SURVIVES | price(50,"SAVE5") becomes 40, still `< 50` | `assert price(50,"") == 50` |
| M5 drop max | KILLED | price(2,"SAVE5") = -3, fails `>= 0` | (test_no_negative) |

The disease, one sentence: inequality assertions check direction,
not amount — they pass for the right answer and for a thousand
wrong ones. Exact-value assertions (== 180, == 45) kill M2-M4
immediately.

**Part 3 (differential).** Any total in (100, 105] with the
coupon disagrees. E.g. total=104: `price` = 104*0.9 - 5 = 88.60;
`price2` = (104-5)=99, not > 100, so 99.00. Also total=105:
89.50 vs 100.00. Neither is "right": the spec never fixed the
order of discount and coupon — an E2 ambiguity (N3) surfaced by a
diff, no oracle required. The fuzzer loop:

```python
for _ in range(1000):
    t, c = random.uniform(0,300), random.choice(["","SAVE5"])
    assert price(t,c) == price2(t,c), (t,c)
```

**Verdict to expect:** "Green and 100% covered means the tests
ran the code, not that they checked it: mutation score 20%, and
one diff found a requirements bug. Coverage is a smoke alarm, not
a certificate."

**Early finishers:** typical LLM tests assert types, non-nullness
and directions — coverage rises, M1-M4 usually still survive.
The point lands harder when the machine's forty tests move the
score not at all.
