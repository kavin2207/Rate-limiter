from fastapi import FastAPI, Depends
import time
import logging

from limiter import Limiter
from rate_limit_config import RateLimitConfig
from rate_limit_key_builder import RateLimiterBuilder
from rate_limiter_dependency import rate_limit_dependency

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

app = FastAPI()

limiter = Limiter(
    identifier_builder=RateLimiterBuilder(),
    config=RateLimitConfig(),
    clock=time.time,
)

rate_limit = rate_limit_dependency(limiter)

@app.post("/orders", dependencies=[Depends(rate_limit)])
def create_order():
    return {"status": "order created"}
