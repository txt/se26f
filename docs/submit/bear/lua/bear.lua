-- bear.lua  ── agent factories.  uncomment one block per week.
-- ─────────────────────────────────────────────────────
local M = require "fsm"

-- ── tiny print shorthand (S1 only; replaced by say() in S4) ──
local function p(s) return function(_) print(s) end end

-- S1 ── bare action stubs (replaced by say() at S4) ──
local function make_bear(name, hunger, energy)
  local id = M.new_id()
  name = name or ("Bear#"..id)
  return {
    id      = id,
    name    = name,
    hunger  = hunger or 80,
    energy  = energy or 100,
    -- S2: hunger_tok = M.make("hunger_"..id),
    -- S2: energy_tok = M.make("energy_"..id),
    start   = "sleep",
    current = "sleep",
    queue   = {"wake","smell","done"},
    -- S10:
    -- trace = {},
    states  = {
      sleep = {
        --S1:
        action = p(name.." sleeps."),
        --S4: action = M.say("{name} sleeps."),
        --S5: update = M.now(energy_tok, +5),
        guard       = nil,   -- S6: when{...}
        exit        = nil,   -- S6: function
        transitions = { wake="sniff" },
      },
      sniff = {
        action = p(name.." sniffs around."),
        --S4: action = M.say("{name} sniffs. hunger={hunger}"),
        --S6: guard = {{ M.over(hunger_tok,70), {target="gorge"} },
        --             { M.over(hunger_tok,30), {target="nibble"} }},
        guard       = nil,
        exit        = nil,
        transitions = { smell="eat", nothing="sleep" },
      },
      eat = {
        action = p(name.." eats!"),
        --S4: action = M.say("{name} eats! hunger={hunger}"),
        --S5: update = function(ag)
        --               M.now(hunger_tok,-30)(ag)
        --               M.now(energy_tok,+20)(ag) end,
        guard       = nil,
        exit        = nil,
        transitions = { done="sleep" },
      },
      -- S6: gorge, nibble states added here
      -- S9: drive_to_store added here
      -- S10:
      -- flee = {
      --   action = M.say("{name} flees!"),
      --   terminal = true,
      --   transitions = {} },
    }
  }
end

local function make_plant(kind, yield, grow_time)
  local id = M.new_id()
  kind = kind or "Plant"
  local name = kind.."#"..id
  return {
    id         = id,
    name       = name,
    yield      = yield     or 10,
    grow_time  = grow_time or 3,
    berries    = 0,
    start      = "budding",
    current    = "budding",
    queue      = {"ripen"},
    -- S10: trace = {},
    states     = {
      budding = {
        action = p(name.." is budding."),
        --S4: action = M.say("{name} budding. (grow_time={grow_time})"),
        guard       = nil,
        exit        = nil,
        transitions = { ripen="ripe" },
      },
      ripe = {
        action = p(name.." is RIPE!"),
        --S4: action = M.say("{name} ripe! yield={yield}"),
        --S5: update = M.now(berries_tok, yield),
        guard       = nil,
        exit        = nil,
        transitions = { eaten="bare", drought="dormant" },
      },
      bare = {
        action = p(name.." is bare."),
        terminal    = true,
        transitions = {},
      },
      dormant = {
        action = p(name.." is dormant."),
        --S10: wildcard "*" -> "dormant" skips ripe phase
        terminal    = true,
        transitions = {},
      },
    }
  }
end

-- ── S1: one bear, run to completion ──────────────────
local bear1 = make_bear("Yogi", 80, 100)
print("=== S1: one bear ===")
M.start(bear1)

-- ── S8+: multi-agent ecosystem (uncomment at S8) ─────
-- local MAX_TICKS = 20
-- local bears  = { make_bear("Yogi",90,60),
--                  make_bear("Boo",50,80) }
-- local plants = { make_plant("berry",15,2),
--                  make_plant("nut",8,4),
--                  make_plant("berry",20,1) }
-- local agents = {}
-- for _,b in ipairs(bears)  do agents[#agents+1]=b end
-- for _,p in ipairs(plants) do agents[#agents+1]=p end
--
-- print("=== ECOSYSTEM ===")
-- for tick=1,MAX_TICKS do
--   io.write(string.format("-- tick %d\n", tick))
--   for _,agent in ipairs(M.shuffle({table.unpack(agents)})) do
--     M.step(agent) end end
--
-- ── S9: generated ecosystem (uncomment at S9) ────────
-- local N_PLANTS, N_BEARS = 5, 3
-- local bears2, plants2 = {}, {}
-- for i=1,N_BEARS  do
--   bears2[i]  = make_bear(nil, math.random(40,90), math.random(50,100)) end
-- for i=1,N_PLANTS do
--   local kinds = {"berry","nut"}
--   plants2[i] = make_plant(kinds[math.random(#kinds)],
--                            math.random(5,25), math.random(1,5)) end
