-- fsm.lua  ── the engine.  uncomment one block per week.
-- never rewrite; only reveal.
-- ─────────────────────────────────────────────────────

-- S1 ── seed + random ─────────────────────────────────
local SEED = tonumber(arg[1])
         or  tonumber(os.getenv("SEED"))
         or  os.time()
math.randomseed(SEED)
io.write(string.format("-- seed %d  (replay: lua bear.lua %d)\n",
  SEED, SEED))

-- S1 ── shuffle (Fisher-Yates) ────────────────────────
local function shuffle(t)
  for i = #t, 2, -1 do
    local j = math.random(i)
    t[i], t[j] = t[j], t[i] end
  return t end

-- S1 ── global id counter ─────────────────────────────
local _id = 0
local function new_id() _id = _id + 1; return _id end

-- S2 ── token registry ────────────────────────────────
-- local _tokens = {}
-- local function make(name)
--   if _tokens[name] then
--     io.write("WARNING: duplicate token '"..name.."'\n")
--     return _tokens[name] end
--   local t = {name=name, id=new_id()}
--   _tokens[name] = t
--   return t end

-- S4 ── say(): interpolating action strings ───────────
-- local function say(msg)
--   return function(p)
--     local s = msg:gsub("{(%w+)}", function(k)
--       local v = p[k]
--       if v == nil then
--         io.write("WARNING: unknown key '"..k.."' in say()\n")
--         return "<"..k.."?>" end
--       return tostring(v) end)
--     print(s) end end

-- S5 ── now(): mutate payload tokens ──────────────────
-- local function now(token, delta)
--   return function(p)
--     if delta == nil then p[token.name]=true; return true end
--     if delta == 0   then p[token.name]=false; return false end
--     p[token.name] = (p[token.name] or 0) + delta
--     return p[token.name] end end

-- S3 ── comparators (pure, no side-effects) ───────────
-- local function over(token, n)
--   return function(p) return (p[token.name] or 0) > n end end
-- local function to(token, n)
--   return function(p) return (p[token.name] or 0) <= n end end
-- local function eq(token, n)
--   return function(p) return p[token.name] == n end end

-- S6 ── eval_when(): or-of-ands guard evaluation ──────
-- local function eval_when(clauses, p)
--   for _, conjunct in ipairs(clauses) do
--     local ok = true
--     for _, pred in ipairs(conjunct) do
--       if not pred(p) then ok=false; break end end
--     if ok then return conjunct.target end end
--   return nil end

-- S7 ── lint(): static analysis ───────────────────────
-- local function lint(agent)
--   local rules, start = agent.states, agent.start
--   local reachable = {}
--   -- ghost states + build reachable set
--   for sname, state in pairs(rules) do
--     for _, tgt in pairs(state.transitions or {}) do
--       reachable[tgt] = true
--       if not rules[tgt] then
--         io.write(string.format(
--           "LINT [%s]: ghost state '%s' from '%s'\n",
--           agent.name, tgt, sname)) end end end
--   -- dead ends
--   for sname, state in pairs(rules) do
--     local t = state.transitions or {}
--     local n = 0
--     for _ in pairs(t) do n=n+1 end
--     if n==0 and not state.terminal then
--       io.write(string.format(
--         "LINT [%s]: dead end '%s'\n", agent.name, sname)) end end
--   -- unreachable
--   for sname in pairs(rules) do
--     if sname ~= start and not reachable[sname] then
--       io.write(string.format(
--         "LINT [%s]: unreachable state '%s'\n",
--         agent.name, sname)) end end end

-- S1 ── core run (TCO) ────────────────────────────────
local function run(rules, s, p)
  local state = rules[s]
  if not state then return p end

  -- S1: action always fires
  if state.action then state.action(p) end

  -- S5: update/now mutations  [uncomment S5]
  -- if state.update then state.update(p) end

  -- S6: guard selects next state  [uncomment S6]
  -- (used in transition lookup below)

  -- S6: exit fires before leaving  [uncomment S6]
  -- local function depart(next_s)
  --   if state.exit then state.exit(s, p) end
  --   return next_s end

  local e = table.remove(p.queue, 1)
  if not e then return p end

  -- S10: wildcard fallback  [uncomment S10]
  -- local target = (state.transitions or {})[e]
  --             or (state.transitions or {})["*"]
  --             or s
  local target = (state.transitions or {})[e] or s  -- S1 version

  -- S10: trace log  [uncomment S10]
  -- p.trace = p.trace or {}
  -- p.trace[#p.trace+1] =
  --   string.format("[%s] %s -> %s", e, s, target)

  return run(rules, target, p) end  -- TCO

-- S8 ── step(): one event per tick ────────────────────
-- local function step(agent)
--   if #agent.queue == 0 then return end
--   run(agent.states, agent.current, agent) end

-- S1 ── start(): run to completion ────────────────────
local function start(agent)
  agent.current = agent.current or agent.start
  return run(agent.states, agent.current, agent) end

-- S10 ── print_trace() ────────────────────────────────
-- local function print_trace(agent)
--   for _, line in ipairs(agent.trace or {}) do
--     print("  "..line) end end

return {
  new_id      = new_id,
  start       = start,
  shuffle     = shuffle,
  -- S2: make   = make,
  -- S3: over   = over, to=to, eq=eq,
  -- S4: say    = say,
  -- S5: now    = now,
  -- S6: eval_when = eval_when,
  -- S7: lint   = lint,
  -- S8: step   = step,
  -- S10: print_trace = print_trace,
}
