import json
import redis
from typing import Optional
from storage.base import RateLimitStorage

class RedisStorage(RateLimitStorage):

    def __init__(self, host="localhost", port=6379):
        self.client = redis.Redis(
            host=host,
            port=port,
            decode_responses=True
        )

    def get(self, key: str) -> Optional[dict]:
        data = self.client.get(key)
        if data is None:
            return None
        return json.loads(data)

    def set(self, key: str, value: dict, ttl: int):
        self.client.setex(
            key,
            ttl,
            json.dumps(value)
        )
