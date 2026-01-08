import time
import redis
from storage.redis_storage import RedisStorage

r = redis.Redis(host="localhost", port=6379)
storage = RedisStorage(r)

key = "rate:test:user1"

print("---- TOKEN BUCKET TEST ----")
for i in range(7):
    allowed, remaining = storage.token_bucket_allow(
        key=key,
        capacity=5,
        refill_rate=1,  # 1 token/sec
        now=time.time(),
    )
    print(i, allowed, remaining)
    time.sleep(0.1)
