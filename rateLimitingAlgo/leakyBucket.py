from typing import Dict, Tuple

class LeakyBucket:
    def __init__(self, capacity, leak_rate):
        self.capacity = capacity  # max bucket size
        self.leak_rate = leak_rate  # rate at which water leaks per second
        self.bucket: Dict[str,Tuple[float,float]] = {}

    def _leak(self, identifier: str, current_time: float):
        if identifier not in self.bucket:
            self.bucket[identifier] = (0,current_time)
            return
        water, last_time = self.bucket[identifier]

        elapsed_time = current_time - last_time
        new_water = max(0, water - elapsed_time * self.leak_rate)
        
        self.bucket[identifier] = (new_water, current_time)

    def allow_request(self, identifier, current_time):
        self._leak(identifier, current_time)
        water, last_time = self.bucket[identifier]
        if water < self.capacity:
            water += 1  # Add 1 unit of "water" for each request
            self.bucket[identifier] = (water, last_time)
            return True
        return False