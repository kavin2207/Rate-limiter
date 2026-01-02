"""
    This is the domain controller of this project request go through this controller this will decide weather to accept the request or not
    this is going to call the actual algo for rateLimiter and based on that make a decision.

    Input: Identifier: str
    Output: tuple, contain (boolean,string)
"""

import time
from rateLimitConfig import RateLimitConfig
from rateLimiterFactory import RateLimiterFactory

class Limiter:
    def __init__(self, identifier_builder, config: RateLimitConfig, factory: RateLimiterFactory):
        self.identifier_builder = identifier_builder
        self.config = config
        self.factory = factory

    def allow_request(self, request: dict):
        identifier = self.identifier_builder.build(request)

        principal, endpoint, method = identifier.split(":")

        rule = self.config.resolve_rule(
            principal=principal,
            endpoint=endpoint,
            method=method
        )

        algorithm = self.factory.get_algorithm(rule)
        return algorithm.allow_request(identifier, time.time())


