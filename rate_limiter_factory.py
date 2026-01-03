from rateLimitingAlgo.tokenBucket import TokenBucket
from rateLimitingAlgo.leakyBucket import LeakyBucket
from rate_limit_config import RateLimitRule

class RateLimiterFactory:
    """
    Creates & caches algorithm instances.
    Ensures bucket state is preserved.
    """

    def __init__(self):
        self._cache = {}

    def get_algorithm(self, identifier, rule: RateLimitRule):
        cache_key = (identifier, rule.algorithm, rule.capacity, rule.refill_rate)

        if cache_key in self._cache:
            return self._cache[cache_key]

        if rule.algorithm == "token_bucket":
            algo = TokenBucket(rule.capacity, rule.refill_rate)
        elif rule.algorithm == "leaky_bucket":
            algo = LeakyBucket(rule.capacity, rule.refill_rate)
        else:
            raise ValueError(f"Unknown algorithm: {rule.algorithm}")

        self._cache[cache_key] = algo
        return algo
