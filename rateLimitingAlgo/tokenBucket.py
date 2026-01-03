from typing import Dict, Tuple
from rateLimitingAlgo.rate_limiter_decision import RateLimitDecision

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.bucket: Dict[str,Tuple[float,float]] = {}

    def _refill(self, identifier, current_time):
        
        if(identifier not in self.bucket):
            self.bucket[identifier] = (self.capacity, current_time)
            return
        
        tokens, last_refill_time = self.bucket[identifier]
        
        elapsed = current_time - last_refill_time
        if elapsed > 0:
            tokens = min(
                self.capacity,
                tokens + elapsed * self.refill_rate
            )
        
        self.bucket[identifier]=(tokens, current_time)

    def allow_request(self, identifier:str, current_time:float):
        
        self._refill(identifier, current_time)
        tokens, last_refil_time = self.bucket[identifier]
        if tokens >= 1:
            tokens -= 1
            self.bucket[identifier] = (tokens, last_refil_time)
            return True
        return False

    def evaluate(self, identifier, current_time):
        resp = self.allow_request(identifier, current_time)
        tokens, last_refill_time = self.bucket[identifier]
        if resp:
            retry_after = None
        else:
            retry_after = (1 - tokens) / self.refill_rate
        result = RateLimitDecision(
            allowed=resp,
            limit=self.capacity,
            remaining=tokens,
            retry_after=retry_after
        )
        return result