from abc import ABC, abstractmethod
from typing import Dict

class RateLimitingAlgorithm(ABC):
    @abstractmethod
    def evaluate(self, identifier, time_stamp)->Dict:
        pass
