import time
from limiter import Limiter
from rate_limit_config import RateLimitConfig
from rate_limiter_factory import RateLimiterFactory
from rate_limit_key_builder import RateLimiterBuilder

rate_limit_config = RateLimitConfig()
rate_limiter_factor = RateLimiterFactory()
rate_limiter_key_builder = RateLimiterBuilder()

request = {
  "user_id": "123",
  "api_key": "abc",
  "ip": "10.0.0.1",
  "endpoint": "/orders",
  "method": "POST",
  "metadata": {}
}

limiter = Limiter(rate_limiter_key_builder, rate_limit_config, rate_limiter_factor)

for _ in range(2):
    allowed = limiter.allow_request(request)
    time.sleep(0.5)
    print(allowed)
