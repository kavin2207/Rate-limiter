import time
import redis

from limiter import Limiter
from rate_limit_key_builder import RateLimiterBuilder
from rate_limit_config import RateLimitConfig
from storage.redis_storage import RedisStorage
from fake_request import FakeRequest


def run_test(name, request, sleep=0.1, iterations=10):
    print(f"\n---- {name} ----")
    for i in range(iterations):
        decision = limiter.allow_request(request)
        print(i, decision)
        time.sleep(sleep)


# ---- Redis ----
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
storage = RedisStorage(r)

# ---- Limiter ----
limiter = Limiter(
    identifier_builder=RateLimiterBuilder(),
    config=RateLimitConfig(),
    storage=storage,
)

# ---- TOKEN BUCKET (user → token_bucket) ----
token_bucket_request = FakeRequest(
    method="POST",
    path="/orders",
    headers={"X-User-Id": "user-123"},
)

run_test(
    "TOKEN BUCKET (user /orders POST)",
    token_bucket_request,
    sleep=0.05,
    iterations=15,
)

# ---- LEAKY BUCKET (ip → leaky_bucket) ----
leaky_bucket_request = FakeRequest(
    method="GET",
    path="/health",
)

run_test(
    "LEAKY BUCKET (ip /health GET)",
    leaky_bucket_request,
    sleep=0.05,
    iterations=15,
)
