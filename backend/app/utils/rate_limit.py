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
        self._app = None
        self._initialized = False
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize rate limiter with Flask app"""
        self._app = app
        storage_type = app.config.get('RATE_LIMIT_STORAGE', 'memory')
        
        if storage_type == 'redis':
            redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
            try:
                self.storage = RedisStorage(redis_url)
                logger.info("✅ Rate limiting using Redis storage")
            except Exception as e:
                logger.error(f"❌ Failed to connect to Redis: {e}. Falling back to memory storage.")
                self.storage = MemoryStorage()
        elif storage_type == 'database':
            self.storage = DatabaseStorage()
            logger.info("✅ Rate limiting using database storage")
        else:
            self.storage = MemoryStorage()
            logger.info("✅ Rate limiting using memory storage")
        
        # Set default limits from config
        self.default_limit = app.config.get('RATE_LIMIT_DEFAULT', 100)
        self.default_period = app.config.get('RATE_LIMIT_PERIOD', 3600)
        
        self._initialized = True
        
        # Register teardown
        app.teardown_appcontext(self.teardown)
        
        logger.info(f"✅ Rate limiter initialized: {storage_type} storage, {self.default_limit} req/{self.default_period}s")
    
    def _ensure_initialized(self):
        """Ensure storage is initialized before use"""
        if self.storage is None:
            if self._app is not None:
                # Try to initialize with the existing app
                self.init_app(self._app)
            else:
                # Fallback to memory storage if no app is available
                logger.warning("⚠️ Rate limiter not initialized with Flask app. Using memory storage.")
                self.storage = MemoryStorage()
                self._initialized = True
    
    def teardown(self, exception):
        """Clean up resources"""
        if self.storage and hasattr(self.storage, 'close'):
            self.storage.close()
    
    def get_client_identifier(self):
        """Get unique identifier for client based on IP and user agent"""
        try:
            client_ip = request.remote_addr or 'unknown'
            user_agent = request.headers.get('User-Agent', '')[:50]  # Limit length
            
            # If user is authenticated, use user ID for more accurate rate limiting
            if hasattr(g, 'user') and g.user and hasattr(g.user, 'id'):
                return f"user:{g.user.id}"
            
            # Fallback to IP + User-Agent hash for anonymous users
            user_agent_hash = hash(user_agent) % 10000
            return f"ip:{client_ip}:{user_agent_hash}"
            
        except Exception as e:
            logger.error(f"Error getting client identifier: {e}")
            return f"unknown:{int(time.time())}"
    
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
        # Ensure storage is initialized before use
        self._ensure_initialized()
        
        limit = limit or self.default_limit
        period = period or self.default_period
        
        current_time = time.time()
        window_start = current_time - period
        
        try:
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
            remaining = max(0, limit - request_count - 1)
            reset_time = current_time + period
            
            return True, remaining, reset_time
            
        except Exception as e:
            logger.error(f"Error in rate limit check for key {key}: {e}")
            # If there's an error with rate limiting, allow the request
            return True, limit - 1, current_time + period
    
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
                try:
                    client_id = self.get_client_identifier()
                    endpoint = f"{request.endpoint or 'unknown'}"
                    
                    if scope:
                        key = f"ratelimit:{scope}:{client_id}:{endpoint}"
                    else:
                        key = f"ratelimit:{client_id}:{endpoint}"
                    
                    # Check rate limit
                    allowed, remaining, reset_time = self.check_rate_limit(key, limit, period)
                    
                    if not allowed:
                        retry_after = max(1, int(reset_time - time.time()))
                        response = jsonify({
                            "error": "rate_limit_exceeded",
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
                    
                    # Call the original function
                    response = f(*args, **kwargs)
                    
                    # Add rate limit headers to successful responses
                    if isinstance(response, tuple) and len(response) == 2:
                        resp_obj, status_code = response
                        resp_obj.headers['X-RateLimit-Limit'] = str(limit)
                        resp_obj.headers['X-RateLimit-Remaining'] = str(remaining)
                        resp_obj.headers['X-RateLimit-Reset'] = str(int(reset_time))
                        return resp_obj, status_code
                    else:
                        response.headers['X-RateLimit-Limit'] = str(limit)
                        response.headers['X-RateLimit-Remaining'] = str(remaining)
                        response.headers['X-RateLimit-Reset'] = str(int(reset_time))
                        return response
                        
                except Exception as e:
                    logger.error(f"Rate limit decorator error: {e}")
                    # If rate limiting fails, allow the request but log the error
                    return f(*args, **kwargs)
            
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
        self.lock = Lock()
    
    def get_requests(self, key, since):
        """Get requests since given timestamp"""
        self._cleanup_if_needed()
        
        with self.lock:
            if key not in self.requests:
                return []
            
            # Return requests newer than 'since'
            return [req_time for req_time in self.requests[key] if req_time >= since]
    
    def add_request(self, key, timestamp, ttl):
        """Add a request timestamp with TTL"""
        with self.lock:
            if key not in self.requests:
                self.requests[key] = []
            
            self.requests[key].append(timestamp)
            
            # Remove requests older than TTL to prevent memory leaks
            cutoff = timestamp - ttl
            self.requests[key] = [req_time for req_time in self.requests[key] if req_time > cutoff]
            
            # Schedule cleanup for this key
            self.requests[f"{key}:expiry"] = timestamp + ttl
    
    def _cleanup_if_needed(self):
        """Clean up expired entries if needed"""
        current_time = time.time()
        
        # Clean up every 5 minutes
        if current_time - self.last_cleanup < 300:
            return
        
        with self.lock:
            keys_to_delete = []
            for key in list(self.requests.keys()):
                if key.endswith(':expiry'):
                    expiry = self.requests[key]
                    if expiry < current_time:
                        main_key = key.replace(':expiry', '')
                        keys_to_delete.extend([main_key, key])
            
            for key in keys_to_delete:
                if key in self.requests:
                    del self.requests[key]
            
            self.last_cleanup = current_time
    
    def cleanup(self):
        """Force cleanup"""
        self._cleanup_if_needed()


class RedisStorage(BaseStorage):
    """Redis storage for rate limiting"""
    
    def __init__(self, redis_url):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.prefix = "ratelimit:"
        
        # Test connection
        try:
            self.redis.ping()
            logger.info("✅ Redis connection successful")
        except redis.ConnectionError as e:
            logger.error(f"❌ Redis connection failed: {e}")
            raise
    
    def get_requests(self, key, since):
        """Get requests since given timestamp using Redis sorted set"""
        try:
            # Use sorted set with timestamps as scores
            full_key = f"{self.prefix}{key}"
            requests = self.redis.zrangebyscore(full_key, since, '+inf', withscores=True)
            return [score for _, score in requests]
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
    
    def cleanup(self):
        """Clean up expired keys (Redis handles this automatically)"""
        pass
    
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
            
            # Clean up expired records periodically
            if timestamp % 300 < 60:  # Cleanup every ~5 minutes
                self.cleanup()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Database error in add_request: {e}")
    
    def cleanup(self):
        """Clean up expired database records"""
        try:
            # Delete records that have expired
            expired_count = RateLimit.query.filter(
                RateLimit.expires_at < time.time()
            ).delete()
            
            db.session.commit()
            
            if expired_count > 0:
                logger.debug(f"🧹 Cleaned up {expired_count} expired rate limit records")
                
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
    """Special rate limit for authentication endpoints (5 requests per minute)"""
    return rate_limit(limit=limit, period=period, scope="auth")

def api_rate_limit(limit=100, period=3600):
    """General API rate limit (100 requests per hour)"""
    return rate_limit(limit=limit, period=period, scope="api")

def strict_rate_limit(limit=10, period=60):
    """Strict rate limit for sensitive endpoints (10 requests per minute)"""
    return rate_limit(limit=limit, period=period, scope="strict")

def public_rate_limit(limit=1000, period=3600):
    """Liberal rate limit for public endpoints (1000 requests per hour)"""
    return rate_limit(limit=limit, period=period, scope="public")

# ===== Utility Functions =====
def get_rate_limit_info(key):
    """Get current rate limit information for a key"""
    rate_limiter._ensure_initialized()
    return rate_limiter.storage.get_requests(key, time.time() - 3600)

def reset_rate_limit(key):
    """Reset rate limit for a key (admin function)"""
    rate_limiter._ensure_initialized()
    
    try:
        if isinstance(rate_limiter.storage, RedisStorage):
            full_key = f"ratelimit:{key}"
            rate_limiter.storage.redis.delete(full_key)
        elif isinstance(rate_limiter.storage, MemoryStorage):
            with rate_limiter.lock:
                if key in rate_limiter.storage.requests:
                    del rate_limiter.storage.requests[key]
                if f"{key}:expiry" in rate_limiter.storage.requests:
                    del rate_limiter.storage.requests[f"{key}:expiry"]
        elif isinstance(rate_limiter.storage, DatabaseStorage):
            RateLimit.query.filter_by(key=key).delete()
            db.session.commit()
        
        logger.info(f"✅ Rate limit reset for key: {key}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error resetting rate limit for {key}: {e}")
        return False

def get_rate_limit_status(client_id, endpoint):
    """Get current rate limit status for a client and endpoint"""
    rate_limiter._ensure_initialized()
    
    key = f"ratelimit:{client_id}:{endpoint}"
    current_time = time.time()
    window_start = current_time - 3600  # 1 hour window
    
    requests = rate_limiter.storage.get_requests(key, window_start)
    recent_requests = [req_time for req_time in requests if req_time >= window_start]
    
    return {
        'key': key,
        'requests_count': len(recent_requests),
        'limit': rate_limiter.default_limit,
        'period': rate_limiter.default_period,
        'remaining': max(0, rate_limiter.default_limit - len(recent_requests))
    }

# ===== Configuration Helper =====
def configure_rate_limiter(app):
    """Configure rate limiter with Flask app"""
    rate_limiter.init_app(app)
    
    # Add rate limit headers to all responses
    @app.after_request
    def add_rate_limit_headers(response):
        if not hasattr(request, 'rate_limit_headers'):
            return response
        
        headers = getattr(request, 'rate_limit_headers', {})
        for key, value in headers.items():
            response.headers[key] = str(value)
        
        return response
    
    return rate_limiter