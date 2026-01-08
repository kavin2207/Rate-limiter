import os
import redis
from storage.base import RateLimitStorage


def load_lua_script(filename: str) -> str:
    base_dir = os.path.dirname(__file__)
    lua_path = os.path.abspath(os.path.join(base_dir, "..", "lua", filename))

    with open(lua_path, "r") as f:
        return f.read()


class RedisStorage(RateLimitStorage):
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

        # Load Lua scripts atomically
        self.token_bucket_sha = self.redis.script_load(
            load_lua_script("token_bucket.lua")
        )

        self.leaky_bucket_sha = self.redis.script_load(
            load_lua_script("leaky_bucket.lua")
        )

    def token_bucket_allow(
        self,
        key: str,
        capacity: int,
        refill_rate: float,
        now: float,
    ):
        return self.redis.evalsha(
            self.token_bucket_sha,
            1,
            key,
            capacity,
            refill_rate,
            now,
        )

    def leaky_bucket_allow(
        self,
        key: str,
        capacity: int,
        leak_rate: float,
        now: float,
    ):
        return self.redis.evalsha(
            self.leaky_bucket_sha,
            1,
            key,
            capacity,
            leak_rate,
            now,
        )
