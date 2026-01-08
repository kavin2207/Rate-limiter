-- TOKEN BUCKET LUA SCRIPT
-- ======================
-- KEYS[1] = bucket key
--
-- ARGV[1] = capacity (max tokens)
-- ARGV[2] = refill_rate (tokens per second)
-- ARGV[3] = now (current timestamp in seconds)

local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

-- Fetch existing state
local data = redis.call("HMGET", KEYS[1], "tokens", "last_refill")
local tokens = tonumber(data[1])
local last_refill = tonumber(data[2])

-- Initialize bucket if missing
if tokens == nil or last_refill == nil then
    tokens = capacity
    last_refill = now
end

-- Refill tokens
local elapsed = math.max(0, now - last_refill)
local refill = elapsed * refill_rate
tokens = math.min(capacity, tokens + refill)

-- Decide allow / reject
local allowed = 0
if tokens >= 1 then
    allowed = 1
    tokens = tokens - 1
end

-- Persist updated state
redis.call(
    "HMSET",
    KEYS[1],
    "tokens", tokens,
    "last_refill", now
)

-- Optional TTL safety (avoids stale keys forever)
redis.call("EXPIRE", KEYS[1], math.ceil(capacity / refill_rate * 2))

-- Return decision
-- [1] = allowed (1 or 0)
-- [2] = remaining tokens
return { allowed, tokens }
