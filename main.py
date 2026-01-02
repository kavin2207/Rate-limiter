import time
from limiter import Limiter
from rateLimitingAlgo.leakyBucket import LeakyBucket
from rateLimitingAlgo.tokenBucket import TokenBucket

using_algo = "TokenBucket"

if using_algo == "TokenBucket":
    algorithm = TokenBucket(capacity=10, refill_rate=2)
else:
    algorithm = LeakyBucket(capacity=10,leak_rate=1)

limiter = Limiter(algorithm)

identifier = "abhijeet"

for _ in range(20):
    allowed, reason = limiter.process_request(identifier, time.time())
    time.sleep(1)
    print(allowed, reason)
