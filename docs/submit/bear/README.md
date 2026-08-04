<p align="center">
  <a href="https://github.com/txt/se26f/blob/main/README.md"><img 
     src="https://img.shields.io/badge/Home-%23ff5733?style=flat-square&logo=home&logoColor=white" /></a>
  <a href="https://github.com/txt/se26f/blob/main/docs/lect/policies.md"><img 
      src="https://img.shields.io/badge/Policies-%230055ff?style=flat-square&logo=openai&logoColor=white" /></a>
  <a href="#"><img
      src="https://img.shields.io/badge/Teams-%23ffd700?style=flat-square&logo=users&logoColor=white" /></a>
  <a href="#"><img 
      src="https://img.shields.io/badge/Moodle-%23dc143c?style=flat-square&logo=moodle&logoColor=white" /></a>
  <a href="#"><img 
      src="https://img.shields.io/badge/Chat-%23008080?style=flat-square&logo=discord&logoColor=white" /></a>
  <a href="https://github.com/txt/se26f/blob/main/LICENSE.md"><img 
      src="https://img.shields.io/badge/©%20timm%202026-%234b4b4b?style=flat-square&logoColor=white" /></a></p>
<h1 align="center">:cyclone: CSC510: Software Engineering <br>NC State, Fall '26</h1>
<img src="https://raw.githubusercontent.com/txt/se26f/refs/heads/main/etc/img/se26f.png">

# CSC491/591 — The Bear Project

Ten weeks. One bear. One forest. N plants, M bears by the end.

## The Arc

| Weeks | Mode    | Question                              |
|-------|---------|---------------------------------------|
| 1–4   | BUILD   | Does it do anything?                  |
| 5–6   | HARDEN  | Does it do the right thing?           |
| 7–8   | STRESS  | Can we break it?                      |
| 9–10  | CERTIFY | Can we prove it cannot break?         |

## Files

    lua/fsm.lua       engine, grows week by week (uncomment to unlock)
    lua/bear.lua      bear + plant factories, same pattern
    python/fsm.py     port of the engine
    python/bear.py    port of the factories
    weeks/w01.md      
    ...               one file per week: bear output + TLAs +
    weeks/w10.md      anti-patterns + python idioms

## Running

    lua lua/bear.lua            # random seed
    lua lua/bear.lua 42         # fixed seed
    lua lua/bear.lua $RANDOM    # shell picks, seed is printed

    python python/bear.py 42

## The Seed Contract

The seed is always printed. Any run can be replayed exactly.
A bug you cannot reproduce is not a fixed bug.

## Week Tags

Every feature in fsm.lua and bear.lua is tagged `--S1` through
`--S10`. Lines for future weeks are commented out. Each week you
uncomment the next block — you never rewrite, only reveal.
