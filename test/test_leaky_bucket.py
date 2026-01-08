import time
import redis

from storage.redis_storage import RedisStorage
from rateLimitingAlgo.leakyBucket import LeakyBucket
from rate_limit_config import RateLimitRule


def main():
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    storage = RedisStorage(r)

    rule = RateLimitRule(
        capacity=3,
        refill_rate=1,  # leak 1 req / second
        algorithm="leaky_bucket",
    )

    bucket = LeakyBucket(storage, rule)
    key = "test:leaky:user123"

    print("---- LEAKY BUCKET TEST ----")

    for i in range(6):
        decision = bucket.evaluate(key, time.time())
        print(i, decision)
        time.sleep(0.2)

    print("\nSleeping 2 seconds to allow leak...\n")
    time.sleep(2)

    for i in range(3):
        decision = bucket.evaluate(key, time.time())
        print("after leak", i, decision)


if __name__ == "__main__":
    main()
