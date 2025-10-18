# backend/app/utils/rate_limit.py

from functools import wraps
from flask import request, jsonify, current_app, g
from datetime import datetime, timedelta
import time
import redis
from threading import Lock
from app.models import db, RateLimit
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """Rate limiting implementation with multiple storage backends"""
    
    def __init__(self, app=None):
        self.storage = None
        self.lock = Lock()
        self.default_limit = 100  # requests per hour
        self.default_period = 3600  # seconds
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize rate limiter with Flask app"""
        storage_type = app.config.get('RATE_LIMIT_STORAGE', 'memory')
        
        if storage_type == 'redis':
            redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
            try:
                self.storage = RedisStorage(redis_url)
                logger.info("Rate limiting using Redis storage")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}. Falling back to memory storage.")
                self.storage = MemoryStorage()
        elif storage_type == 'database':
            self.storage = DatabaseStorage()
            logger.info("Rate limiting using database storage")
        else:
            self.storage = MemoryStorage()
            logger.info("Rate limiting using memory storage")
        
        # Set default limits from config
        self.default_limit = app.config.get('RATE_LIMIT_DEFAULT', 100)
        self.default_period = app.config.get('RATE_LIMIT_PERIOD', 3600)
        
        # Register teardown
        app.teardown_appcontext(self.teardown)
    
    def teardown(self, exception):
        """Clean up resources"""
        if hasattr(self.storage, 'close'):
            self.storage.close()
    
    def get_client_identifier(self):
        """Get unique identifier for client based on IP and user agent"""
        client_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')
        
        # If user is authenticated, use user ID for more accurate rate limiting
        if hasattr(g, 'user') and g.user and hasattr(g.user, 'id'):
            return f"user:{g.user.id}"
        
        # Fallback to IP + User-Agent for anonymous users
        return f"ip:{client_ip}:{hash(user_agent) % 1000}"
    
    def check_rate_limit(self, key, limit=None, period=None):
        """
        Check if request is within rate limit
        
        Args:
            key: Rate limit key
            limit: Maximum number of requests
            period: Time period in seconds
            
        Returns:
            tuple: (is_allowed, remaining, reset_time)
        """
        limit = limit or self.default_limit
        period = period or self.default_period
        
        current_time = time.time()
        window_start = current_time - period
        
        # Get requests in current window
        requests = self.storage.get_requests(key, window_start)
        
        # Count requests and filter old ones
        recent_requests = [req_time for req_time in requests if req_time >= window_start]
        request_count = len(recent_requests)
        
        # Check if limit exceeded
        if request_count >= limit:
            # Find the oldest request to calculate reset time
            oldest_request = min(recent_requests) if recent_requests else current_time
            reset_time = oldest_request + period
            return False, 0, reset_time
        
        # Add current request
        self.storage.add_request(key, current_time, period)
        
        # Calculate remaining requests and reset time
        remaining = limit - request_count - 1
        reset_time = current_time + period
        
        return True, remaining, reset_time
    
    def rate_limit(self, limit=None, period=None, scope=None):
        """
        Decorator for rate limiting endpoints
        
        Args:
            limit: Maximum number of requests
            period: Time period in seconds
            scope: Additional scope for rate limiting key
        """
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Generate rate limit key
                client_id = self.get_client_identifier()
                endpoint = f"{request.endpoint or 'unknown'}"
                
                if scope:
                    key = f"ratelimit:{scope}:{client_id}:{endpoint}"
                else:
                    key = f"ratelimit:{client_id}:{endpoint}"
                
                # Check rate limit
                allowed, remaining, reset_time = self.check_rate_limit(key, limit, period)
                
                if not allowed:
                    retry_after = int(reset_time - time.time())
                    response = jsonify({
                        "error": "Rate limit exceeded",
                        "message": "Too many requests. Please try again later.",
                        "retry_after": retry_after,
                        "limit": limit,
                        "period": period
                    })
                    response.headers['X-RateLimit-Limit'] = str(limit)
                    response.headers['X-RateLimit-Remaining'] = '0'
                    response.headers['X-RateLimit-Reset'] = str(int(reset_time))
                    response.headers['Retry-After'] = str(retry_after)
                    return response, 429
                
                # Add rate limit headers to successful responses
                response = f(*args, **kwargs)
                if isinstance(response, tuple):
                    response = response[0]  # Get response object from (response, status) tuple
                
                response.headers['X-RateLimit-Limit'] = str(limit)
                response.headers['X-RateLimit-Remaining'] = str(remaining)
                response.headers['X-RateLimit-Reset'] = str(int(reset_time))
                
                return response
            
            return decorated_function
        return decorator


# ===== Storage Backends =====

class BaseStorage:
    """Base class for storage backends"""
    
    def get_requests(self, key, since):
        """Get requests since given timestamp"""
        raise NotImplementedError
    
    def add_request(self, key, timestamp, ttl):
        """Add a request timestamp with TTL"""
        raise NotImplementedError
    
    def cleanup(self):
        """Clean up expired entries"""
        pass
    
    def close(self):
        """Close connections"""
        pass


class MemoryStorage(BaseStorage):
    """In-memory storage for rate limiting"""
    
    def __init__(self):
        self.requests = {}
        self.last_cleanup = time.time()
    
    def get_requests(self, key, since):
        """Get requests since given timestamp"""
        self._cleanup_if_needed()
        
        with Lock():
            if key not in self.requests:
                return []
            
            # Return requests newer than 'since'
            return [req_time for req_time in self.requests[key] if req_time >= since]
    
    def add_request(self, key, timestamp, ttl):
        """Add a request timestamp with TTL"""
        with Lock():
            if key not in self.requests:
                self.requests[key] = []
            
            self.requests[key].append(timestamp)
            
            # Schedule cleanup for this key
            if f"{key}:expiry" not in self.requests:
                self.requests[f"{key}:expiry"] = timestamp + ttl
    
    def _cleanup_if_needed(self):
        """Clean up expired entries if needed"""
        current_time = time.time()
        
        # Clean up every 5 minutes
        if current_time - self.last_cleanup < 300:
            return
        
        with Lock():
            keys_to_delete = []
            for key, expiry in [(k, v) for k, v in self.requests.items() if k.endswith(':expiry')]:
                if expiry < current_time:
                    main_key = key.replace(':expiry', '')
                    keys_to_delete.extend([main_key, key])
            
            for key in keys_to_delete:
                if key in self.requests:
                    del self.requests[key]
            
            self.last_cleanup = current_time


class RedisStorage(BaseStorage):
    """Redis storage for rate limiting"""
    
    def __init__(self, redis_url):
        self.redis = redis.from_url(redis_url)
        self.prefix = "ratelimit:"
    
    def get_requests(self, key, since):
        """Get requests since given timestamp using Redis sorted set"""
        try:
            # Use sorted set with timestamps as scores
            full_key = f"{self.prefix}{key}"
            requests = self.redis.zrangebyscore(full_key, since, '+inf')
            return [float(score) for score in requests]
        except redis.RedisError as e:
            logger.error(f"Redis error in get_requests: {e}")
            return []
    
    def add_request(self, key, timestamp, ttl):
        """Add a request timestamp with TTL using Redis"""
        try:
            full_key = f"{self.prefix}{key}"
            
            # Add to sorted set
            self.redis.zadd(full_key, {str(timestamp): timestamp})
            
            # Remove old entries and set TTL
            self.redis.zremrangebyscore(full_key, 0, timestamp - ttl)
            self.redis.expire(full_key, ttl)
            
        except redis.RedisError as e:
            logger.error(f"Redis error in add_request: {e}")
    
    def close(self):
        """Close Redis connection"""
        if self.redis:
            self.redis.close()


class DatabaseStorage(BaseStorage):
    """Database storage for rate limiting"""
    
    def get_requests(self, key, since):
        """Get requests since given timestamp from database"""
        try:
            requests = RateLimit.query.filter(
                RateLimit.key == key,
                RateLimit.timestamp >= since
            ).all()
            
            return [req.timestamp for req in requests]
        except Exception as e:
            logger.error(f"Database error in get_requests: {e}")
            return []
    
    def add_request(self, key, timestamp, ttl):
        """Add a request timestamp with TTL to database"""
        try:
            # Create new rate limit record
            rate_limit = RateLimit(
                key=key,
                timestamp=timestamp,
                expires_at=timestamp + ttl
            )
            
            db.session.add(rate_limit)
            db.session.commit()
            
            # Clean up expired records
            self.cleanup()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Database error in add_request: {e}")
    
    def cleanup(self):
        """Clean up expired database records"""
        try:
            # Delete records that have expired
            expired = RateLimit.query.filter(
                RateLimit.expires_at < time.time()
            ).delete()
            
            db.session.commit()
            
            if expired:
                logger.debug(f"Cleaned up {expired} expired rate limit records")
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"Database error in cleanup: {e}")


# ===== Global Rate Limiter Instance =====
rate_limiter = RateLimiter()

# ===== Convenience Decorators =====
def rate_limit(limit=None, period=None, scope=None):
    """Convenience decorator for rate limiting"""
    return rate_limiter.rate_limit(limit, period, scope)

def auth_rate_limit(limit=5, period=60):
    """Special rate limit for authentication endpoints"""
    return rate_limit(limit=limit, period=period, scope="auth")

def api_rate_limit(limit=100, period=3600):
    """General API rate limit"""
    return rate_limit(limit=limit, period=period, scope="api")

def strict_rate_limit(limit=10, period=60):
    """Strict rate limit for sensitive endpoints"""
    return rate_limit(limit=limit, period=period, scope="strict")

# ===== Utility Functions =====
def get_rate_limit_info(key):
    """Get current rate limit information for a key"""
    return rate_limiter.storage.get_requests(key, time.time() - 3600)

def reset_rate_limit(key):
    """Reset rate limit for a key (admin function)"""
    if hasattr(rate_limiter.storage, 'redis') and isinstance(rate_limiter.storage, RedisStorage):
        rate_limiter.storage.redis.delete(f"ratelimit:{key}")
    elif hasattr(rate_limiter.storage, 'requests') and isinstance(rate_limiter.storage, MemoryStorage):
        with rate_limiter.lock:
            if key in rate_limiter.storage.requests:
                del rate_limiter.storage.requests[key]
            if f"{key}:expiry" in rate_limiter.storage.requests:
                del rate_limiter.storage.requests[f"{key}:expiry"]
    elif isinstance(rate_limiter.storage, DatabaseStorage):
        RateLimit.query.filter_by(key=key).delete()
        db.session.commit()

# ===== Request Logging Middleware =====
def init_rate_limit_middleware(app):
    """Initialize rate limiting middleware"""
    @app.before_request
    def log_rate_limit_info():
        """Log rate limit information for debugging"""
        if app.debug or app.testing:
            client_id = rate_limiter.get_client_identifier()
            endpoint = request.endpoint or 'unknown'
            key = f"ratelimit:{client_id}:{endpoint}"
            
            current_time = time.time()
            window_start = current_time - 3600  # 1 hour window
            
            requests = rate_limiter.storage.get_requests(key, window_start)
            recent_requests = [req_time for req_time in requests if req_time >= window_start]
            
            logger.debug(f"Rate limit info for {key}: {len(recent_requests)} requests in last hour")
