from dataclasses import dataclass

@dataclass(frozen=True)
class RateLimitRule:
    capacity: int
    refill_rate: float
    algorithm: str   # "token_bucket" | "leaky_bucket"
    

class RateLimitConfig:
    """
    Resolves WHICH rule applies.
    No algorithm instantiation.
    No state.
    """

    def resolve_rule(self, *, principal: str, endpoint: str, method: str) -> RateLimitRule:
        # ---- Base rule by principal ----
        if principal in ("user", "api_key"):
            rule = RateLimitRule(
                capacity=20,
                refill_rate=5,
                algorithm="token_bucket"
            )
        else:  # anonymous / ip
            rule = RateLimitRule(
                capacity=5,
                refill_rate=1,
                algorithm="leaky_bucket"
            )

        # ---- Endpoint + method overrides ----
        if endpoint == "/login" and method == "POST":
            rule = RateLimitRule(
                capacity=5,
                refill_rate=0.5,
                algorithm="token_bucket"
            )

        if endpoint == "/health" and method == "GET":
            rule = RateLimitRule(
                capacity=100,
                refill_rate=20,
                algorithm="token_bucket"
            )

        return rule
