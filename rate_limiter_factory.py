from rateLimitingAlgo.tokenBucket import TokenBucket
from rateLimitingAlgo.leakyBucket import LeakyBucket
from storage.redis_storage import RedisStorage
from rate_limit_config import RateLimitRule


class RateLimiterFactory:
    def __init__(self, storage: RedisStorage):
        self.storage = storage
        self._cache = {}

    def get_algorithm(self, rule: RateLimitRule):
        cache_key = (rule.algorithm, rule.capacity, rule.refill_rate)

        if cache_key in self._cache:
            return self._cache[cache_key]

        if rule.algorithm == "token_bucket":
            algo = TokenBucket(self.storage, rule)
        elif rule.algorithm == "leaky_bucket":
            algo = LeakyBucket(self.storage, rule)
        else:
            raise ValueError(f"Unknown algorithm: {rule.algorithm}")

        self._cache[cache_key] = algo
        return algo
