from rateLimitingAlgo.rate_limiter_decision import RateLimitDecision
from storage.base import RateLimitStorage
from rate_limit_config import RateLimitRule


class TokenBucket:
    """
    Distributed Token Bucket using Redis + Lua (atomic).
    """

    def __init__(self, storage: RateLimitStorage, rule: RateLimitRule):
        self.storage = storage
        self.capacity = rule.capacity
        self.refill_rate = rule.refill_rate

    def evaluate(self, identifier: str, current_time: float) -> RateLimitDecision:
        allowed, tokens = self.storage.token_bucket_allow(
            key=identifier,
            capacity=self.capacity,
            refill_rate=self.refill_rate,
            now=current_time,
        )

        remaining = max(0, int(tokens))

        if allowed:
            return RateLimitDecision(
                allowed=True,
                limit=self.capacity,
                remaining=remaining,
                retry_after=None,
            )

        retry_after = 1 / self.refill_rate

        return RateLimitDecision(
            allowed=False,
            limit=self.capacity,
            remaining=remaining,
            retry_after=retry_after,
        )
