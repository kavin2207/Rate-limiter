from dataclasses import dataclass

@dataclass(frozen=True)
class RateLimitDecision:
    allowed: bool
    limit: int
    remaining: float
    retry_after: float | None #in sec