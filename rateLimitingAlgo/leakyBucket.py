from typing import Dict, Tuple
from rateLimitingAlgo.rate_limiter_decision import RateLimitDecision
from storage.base import RateLimitStorage
from rate_limit_config import RateLimitConfig
import logging

class LeakyBucket:
    def __init__(self, storage: RateLimitStorage, config: RateLimitConfig):
        self.capacity = config.capacity  # max bucket size
        self.leak_rate = config.refill_rate  # rate at which water leaks per second
        self.storage= storage

    def _leak(self, identifier: str, current_time: float):
        state = self.storage.get(identifier)

        if not state:
            water = 0
            last_time = current_time
        else:
            water = state["water"]
            last_time = state["last_time"]

            elapsed = current_time - last_time
            if elapsed > 0:
                water = max(0, water - elapsed * self.leak_rate)
                last_time = current_time

        self.storage.set(identifier, {
            "water": water,
            "last_time": last_time
        })

        return water, last_time

    def allow_request(self, identifier: str, current_time: float):
        water, last_time = self._leak(identifier, current_time)

        if water < self.capacity:
            water += 1
            self.storage.set(identifier, {
                "water": water,
                "last_time": last_time
            })
            return True, water

        return False, water

    def evaluate(self, identifier, current_time):
        allowed, water = self.allow_request(identifier, current_time)
        
        if allowed:
            retry_after = None
        else:
            excess = water - self.capacity
            retry_after = excess / self.leak_rate

        result = RateLimitDecision(
            allowed=allowed,
            limit=self.capacity,
            remaining=max(0, self.capacity - water),
            retry_after=retry_after
        )
        return result
