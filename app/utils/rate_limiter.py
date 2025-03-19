from flask import request
from functools import wraps
from cachetools import TTLCache
import time

class RateLimiter:
    def __init__(self, calls=30, period=60):
        self.calls = calls  # Number of calls allowed
        self.period = period  # Time period in seconds
        self.cache = TTLCache(maxsize=10000, ttl=period)
    
    def is_rate_limited(self, key):
        current = time.time()
        if key in self.cache:
            timestamps = self.cache[key]
            # Clean old timestamps
            timestamps = [ts for ts in timestamps if current - ts < self.period]
            
            if len(timestamps) >= self.calls:
                return True
                
            timestamps.append(current)
            self.cache[key] = timestamps
        else:
            self.cache[key] = [current]
        
        return False

def rate_limit(calls=30, period=60):
    limiter = RateLimiter(calls, period)
    
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            key = f"{request.remote_addr}:{f.__name__}"
            if limiter.is_rate_limited(key):
                return {"error": "Rate limit exceeded"}, 429
            return f(*args, **kwargs)
        return wrapped
    return decorator