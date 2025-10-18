# app/utils/rate_limit_storage.py

from abc import ABC, abstractmethod
from datetime import datetime

class BaseStorage(ABC):
    @abstractmethod
    def get_requests(self, key: str, window_start: datetime) -> int:
        pass

    @abstractmethod
    def add_request(self, key: str, timestamp: datetime):
        pass

# app/utils/memory_storage.py

from collections import defaultdict
# from datetime import datetime, timedelta
# from app.utils.rate_limit_storage import BaseStorage

class MemoryStorage(BaseStorage):
    def __init__(self):
        self.data = defaultdict(list)  # key -> list of timestamps

    def get_requests(self, key: str, window_start: datetime) -> int:
        # Only count requests within the current window
        self.data[key] = [t for t in self.data[key] if t >= window_start]
        return len(self.data[key])

    def add_request(self, key: str, timestamp: datetime):
        self.data[key].append(timestamp)

# app/utils/rate_limit.py

from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, storage):
        if storage is None:
            raise ValueError("RateLimiter storage backend is not initialized.")
        self.storage = storage

    def check_rate_limit(self, key: str, limit: int, period: int):
        """
        key: unique identifier (e.g., user_id or IP)
        limit: max requests
        period: window in seconds
        """
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=period)

        # Number of requests in current window
        requests = self.storage.get_requests(key, window_start)

        if requests >= limit:
            # Rate limit exceeded
            reset_time = (self.storage.data[key][0] + timedelta(seconds=period)) if self.storage.data.get(key) else now
            return False, 0, reset_time
        else:
            self.storage.add_request(key, now)
            remaining = limit - requests - 1
            return True, remaining, now + timedelta(seconds=period)
