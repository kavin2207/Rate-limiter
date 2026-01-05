import logging
from fastapi import Request, HTTPException
from limiter import Limiter

def rate_limit_dependency(limiter: Limiter):
    """
    FastAPI dependency that enforces rate limiting.

    - Evaluates rate limit once per request
    - Stores decision in request.state
    - Raises HTTP 429 with proper headers if blocked
    """

    def dependency(request: Request):

        decision = limiter.allow_request(request)

        # Make decision available to downstream handlers
        request.state.rate_limit_decision = decision

        if not decision.allowed:
            headers = {
                "X-RateLimit-Limit": str(decision.limit),
                "X-RateLimit-Remaining": "0",
            }

            if decision.retry_after is not None:
                headers["Retry-After"] = str(int(decision.retry_after))

            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded",
                headers=headers,
            )

    return dependency
