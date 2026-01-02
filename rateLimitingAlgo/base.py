from abc import ABC, abstractmethod
from typing import Tuple

class RateLimitingAlgorithm(ABC):
    @abstractmethod
    def allow_request(self, identifier, time_stamp)->Tuple[bool, str]:
        pass
