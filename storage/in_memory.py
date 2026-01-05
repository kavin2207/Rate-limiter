import time
from typing import Any, Optional
from .base import RateLimitStorage

class InMemoryStorage(RateLimitStorage):
    def __init__(self):
        self._store = {}

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if not entry:
            return None

        value, expiry = entry
        if expiry and expiry < time.time():
            del self._store[key]
            return None

        return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        expiry = time.time() + ttl if ttl else None
        self._store[key] = (value, expiry)
