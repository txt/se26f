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
