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

class Limiter:
    def __init__(self, identifier_builder: RateLimiterBuilder, config: RateLimitConfig, factory: RateLimiterFactory, clock=time.time):
        self.identifier_builder = identifier_builder
        self.config = config
        self.factory = factory
        self.clock = clock

    def allow_request(self, request: dict):
        success, identifier = self.identifier_builder.key_builder(request)
        if not success:
            return "InValid Request"

        principle_type, principal, endpoint, method = identifier.split(":")

        rule = self.config.resolve_rule(
            principal=principal,
            endpoint=endpoint,
            method=method
        )

        algorithm = self.factory.get_algorithm(identifier, rule)
        decision = algorithm.evaluate(identifier, self.clock())
        return decision


