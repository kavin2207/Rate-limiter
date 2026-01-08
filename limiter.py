import time
import logging
from storage.redis_storage import RedisStorage
from rate_limiter_factory import RateLimiterFactory
from rate_limit_config import RateLimitConfig
from rate_limit_key_builder import RateLimiterBuilder
from rateLimitingAlgo.rate_limiter_decision import RateLimitDecision
import os
import logging

logging.getLogger("rl").info(f"PID={os.getpid()}")


class Limiter:
    def __init__(
        self,
        identifier_builder: RateLimiterBuilder,
        config: RateLimitConfig,
        storage: RedisStorage,
        clock=time.time,
    ):

        self.identifier_builder = identifier_builder
        self.config = config
        self.clock = clock

        self.storage = storage
        self.factory = RateLimiterFactory(storage)

    def allow_request(self, request: dict):
        logging.info("Handling request in PID=%s", os.getpid())
        id_result = self.identifier_builder.key_builder(request)

        if not id_result.success:
            return RateLimitDecision(
                allowed=False,
                limit=0,
                remaining=0,
                retry_after=None,
                error_code=id_result.error_code,
                error_message=id_result.error_message,
            )

        _, principal, endpoint, method = id_result.key.split(":")

        rule = self.config.resolve_rule(
            principal=principal, endpoint=endpoint, method=method
        )
        algorithm = self.factory.get_algorithm(rule)

        return algorithm.evaluate(id_result.key, self.clock())
