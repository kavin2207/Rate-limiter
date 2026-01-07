from rateLimitingAlgo.tokenBucket import TokenBucket
from rateLimitingAlgo.leakyBucket import LeakyBucket
from storage.redis_storage import RedisStorage
from rate_limit_config import RateLimitRule

class RateLimiterFactory:
    """
    Creates & caches algorithm instances.
    Ensures bucket state is preserved.
    """
    def __init__(self):
        self.storage = RedisStorage()

    def get_algorithm(self, rule: RateLimitRule):
        if rule.algorithm == "token_bucket":
            return TokenBucket(self.storage, rule)
        elif rule.algorithm == "leaky_bucket":
            return LeakyBucket(self.storage, rule)
        else:
            raise ValueError(f"Unknown algorithm: {rule.algorithm}")

