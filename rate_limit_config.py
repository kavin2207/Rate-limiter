from dataclasses import dataclass


@dataclass(frozen=True)
class RateLimitRule:
    capacity: int
    refill_rate: float
    algorithm: str  # "token_bucket" | "leaky_bucket"


class RateLimitConfig:
    """
    Resolves WHICH rule applies.
    Order of precedence:
    1. Endpoint-specific overrides (highest)
    2. Principal-based defaults
    """

    def resolve_rule(
        self, *, principal: str, endpoint: str, method: str
    ) -> RateLimitRule:

        # ---- 1️⃣ Endpoint + method overrides (TOP PRIORITY) ----
        if endpoint == "/login" and method == "POST":
            return RateLimitRule(
                capacity=50,
                refill_rate=0.1,
                algorithm="token_bucket",
            )

        if endpoint == "/health" and method == "GET":
            return RateLimitRule(
                capacity=100,
                refill_rate=20,
                algorithm="leaky_bucket",
            )

        # ---- 2️⃣ Principal-based defaults ----
        if principal in ("user", "api_key"):
            return RateLimitRule(
                capacity=200,
                refill_rate=0.1,
                algorithm="token_bucket",
            )

        # ---- 3️⃣ Anonymous / IP fallback ----
        return RateLimitRule(
            capacity=10,
            refill_rate=1,
            algorithm="leaky_bucket",
        )
