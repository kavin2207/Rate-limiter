from limiter import Limiter
from rate_limit_config import RateLimitConfig
from rate_limit_key_builder import RateLimiterBuilder
from storage.redis_storage import RedisStorage
import redis
import time

r = redis.Redis(host="localhost", port=6379)
storage = RedisStorage(r)

limiter = Limiter(
    identifier_builder=RateLimiterBuilder(),
    config=RateLimitConfig(),
    storage=storage,
)

fake_request = {
    "user_id": "123",
    "path": "/orders",
    "method": "POST",
}

for i in range(5):
    decision = limiter.allow_request(fake_request)
    print(i, decision)
    time.sleep(0.1)
