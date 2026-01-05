from abc import ABC, abstractmethod
from typing import Any, Optional

class RateLimitStorage(ABC):

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        pass
