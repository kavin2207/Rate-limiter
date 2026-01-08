from rateLimitingAlgo.rate_limiter_decision import RateLimitDecision
from storage.base import RateLimitStorage
from rate_limit_config import RateLimitRule


class LeakyBucket:
    """
    Distributed Leaky Bucket using Redis + Lua (atomic).
    """

    def __init__(self, storage: RateLimitStorage, rule: RateLimitRule):
        self.storage = storage
        self.capacity = rule.capacity
        self.leak_rate = rule.refill_rate

    def evaluate(self, identifier: str, current_time: float) -> RateLimitDecision:
        allowed, water = self.storage.leaky_bucket_allow(
            key=identifier,
            capacity=self.capacity,
            leak_rate=self.leak_rate,
            now=current_time,
        )

        remaining = max(0, int(self.capacity - water))

        if allowed:
            return RateLimitDecision(
                allowed=True,
                limit=self.capacity,
                remaining=remaining,
                retry_after=None,
            )

        retry_after = 1 / self.leak_rate

        return RateLimitDecision(
            allowed=False,
            limit=self.capacity,
            remaining=remaining,
            retry_after=retry_after,
        )
