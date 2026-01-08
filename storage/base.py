from abc import ABC, abstractmethod


class RateLimitStorage(ABC):

    @abstractmethod
    def token_bucket_allow(self, key, capacity, refill_rate, now):
        pass

    @abstractmethod
    def leaky_bucket_allow(self, key, capacity, leak_rate, now):
        pass
