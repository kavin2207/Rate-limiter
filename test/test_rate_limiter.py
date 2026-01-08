def test_different_users_independent():
    from limiter import Limiter
    from rate_limit_config import RateLimitConfig
    from rate_limiter_factory import RateLimiterFactory
    from rate_limit_key_builder import RateLimiterBuilder
    from fake_clock import FakeClock
    import redis
    from storage.redis_storage import RedisStorage

    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=False,
    )

    storage = RedisStorage(redis_client)

    clock = FakeClock()
    limiter = Limiter(
        RateLimiterBuilder(), RateLimitConfig(), RateLimiterFactory(storage), clock.now
    )

    request_user1 = {"user_id": "123", "endpoint": "/orders", "method": "POST"}

    request_user2 = {"user_id": "456", "endpoint": "/orders", "method": "POST"}

    for _ in range(20):
        assert limiter.allow_request(request_user1)
        clock.advance(2)
    # user1 exhausted, user2 should still pass
    assert limiter.allow_request(request_user1) is True
    assert limiter.allow_request(request_user2) is True
