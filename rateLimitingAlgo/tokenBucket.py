from typing import Dict, Tuple
from rateLimitingAlgo.rate_limiter_decision import RateLimitDecision
from storage.base import RateLimitStorage
from rate_limit_config import RateLimitConfig

class TokenBucket:
    def __init__(self, storage: RateLimitStorage, config: RateLimitConfig):
        self.capacity = config.capacity
        self.refill_rate = config.refill_rate
        self.storage = storage

    def _refill(self, identifier, current_time):
        state = self.storage.get(identifier)

        if not state:
            tokens = self.capacity
            last_refill_time = current_time
        else:
            tokens = state["tokens"]
            last_refill_time = state["last_refill"]

            elapsed = current_time - last_refill_time
            if elapsed > 0:
                tokens = min(
                    self.capacity,
                    tokens + elapsed * self.refill_rate
                )
                last_refill_time = current_time

        self.storage.set(identifier, {
            "tokens": tokens,
            "last_refill": last_refill_time
        })

        return tokens, last_refill_time


    def allow_request(self, identifier: str, current_time: float):
        tokens, last_refill_time = self._refill(identifier, current_time)

        allowed = False
        if tokens >= 1:
            tokens -= 1
            allowed = True

        self.storage.set(identifier, {
            "tokens": tokens,
            "last_refill": last_refill_time
        })

        return allowed, tokens


    def evaluate(self, identifier, current_time):
        allowed, tokens = self.allow_request(identifier, current_time)

        retry_after = None if allowed else max(
            0, (1 - tokens) / self.refill_rate
        )

        return RateLimitDecision(
            allowed=allowed,
            limit=self.capacity,
            remaining=tokens,
            retry_after=retry_after
        )
