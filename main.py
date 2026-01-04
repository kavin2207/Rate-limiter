from fastapi import FastAPI, Depends
import time

from limiter import Limiter
from rate_limiter_factory import RateLimiterFactory
from rate_limit_config import RateLimitConfig
from rate_limit_key_builder import RateLimiterBuilder
from rate_limiter_dependency import rate_limit_dependency

app = FastAPI()

limiter = Limiter(
    identifier_builder=RateLimiterBuilder(),
    config=RateLimitConfig(),
    factory=RateLimiterFactory(),
    clock=time.time
)

rate_limit = rate_limit_dependency(limiter)

@app.post("/orders", dependencies=[Depends(rate_limit)])
def create_order():
    return {"status": "order created"}
