from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class RateLimitDecision:
    allowed: bool
    limit: int
    remaining: float
    retry_after: float | None #in sec
    error_code: Optional[str] = None
    error_message: Optional[str] = None