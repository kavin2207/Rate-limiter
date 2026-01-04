"""
    This is the domain controller of this project request go through this controller this will decide weather to accept the request or not
    this is going to call the actual algo for rateLimiter and based on that make a decision.

    Input: Identifier: str
    Output: tuple, contain (boolean,string)
"""

import time
from rate_limit_config import RateLimitConfig
from rate_limiter_factory import RateLimiterFactory
from rate_limit_key_builder import RateLimiterBuilder
from rateLimitingAlgo.rate_limiter_decision import RateLimitDecision
import logging

class Limiter:
    def __init__(self, identifier_builder: RateLimiterBuilder, config: RateLimitConfig, factory: RateLimiterFactory, clock=time.time):
        self.identifier_builder = identifier_builder
        self.config = config
        self.factory = factory
        self.clock = clock

    def allow_request(self, request: dict):
        id_result = self.identifier_builder.key_builder(request)
        logging.info("id _result %s",id_result)

        if not id_result.success:
            return RateLimitDecision(
                allowed=False,
                limit=0,
                remaining=0,
                retry_after=None,
                error_code=id_result.error_code,
                error_message=id_result.error_message
            )

        principle_type, principal, endpoint, method = id_result.key.split(":")

        rule = self.config.resolve_rule(
            principal=principal,
            endpoint=endpoint,
            method=method
        )
        logging.info("RULE: %s", rule)

        algorithm = self.factory.get_algorithm(id_result.key, rule)
        decision = algorithm.evaluate(id_result.key, self.clock())
        return decision


