-- LEAKY BUCKET LUA SCRIPT
-- ======================
-- KEYS[1] = bucket key
--
-- ARGV[1] = capacity (max queue size)
-- ARGV[2] = leak_rate (units per second)
-- ARGV[3] = now (current timestamp in seconds)

local capacity = tonumber(ARGV[1])
local leak_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

-- Fetch existing state
local data = redis.call("HMGET", KEYS[1], "water_level", "last_leak")
local water = tonumber(data[1])
local last_leak = tonumber(data[2])

-- Initialize bucket if missing
if water == nil or last_leak == nil then
    water = 0
    last_leak = now
end

-- Leak water
local elapsed = math.max(0, now - last_leak)
local leaked = elapsed * leak_rate
water = math.max(0, water - leaked)

-- Decide allow / reject
local allowed = 0
if water + 1 <= capacity then
    allowed = 1
    water = water + 1
end

-- Persist updated state
redis.call(
    "HMSET",
    KEYS[1],
    "water_level", water,
    "last_leak", now
)

-- TTL safety
redis.call("EXPIRE", KEYS[1], math.ceil(capacity / leak_rate * 2))

-- Return decision
-- [1] = allowed (1 or 0)
-- [2] = current water level
return { allowed, water }
