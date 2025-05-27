"""
Pure Python Caching Layer for Highland Tower Development
In-memory and Redis caching system independent of Streamlit

This eliminates framework-specific caching and provides sustainable performance optimization
"""

import time
import json
import hashlib
from typing import Any, Optional, Dict, Callable
from functools import wraps
from datetime import datetime, timedelta
import threading


class InMemoryCache:
    """Pure Python in-memory cache with TTL support"""
    
    def __init__(self, default_ttl: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
        self._lock = threading.Lock()
    
    def _generate_key(self, key: str) -> str:
        """Generate consistent cache key"""
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        with self._lock:
            cache_key = self._generate_key(key)
            
            if cache_key not in self.cache:
                return None
            
            entry = self.cache[cache_key]
            
            # Check if expired
            if time.time() > entry['expires']:
                del self.cache[cache_key]
                return None
            
            entry['hits'] = entry.get('hits', 0) + 1
            entry['last_accessed'] = time.time()
            return entry['value']
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with TTL"""
        with self._lock:
            cache_key = self._generate_key(key)
            ttl = ttl or self.default_ttl
            
            self.cache[cache_key] = {
                'value': value,
                'expires': time.time() + ttl,
                'created': time.time(),
                'hits': 0,
                'last_accessed': time.time()
            }
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        with self._lock:
            cache_key = self._generate_key(key)
            if cache_key in self.cache:
                del self.cache[cache_key]
                return True
            return False
    
    def clear(self) -> None:
        """Clear all cache entries"""
        with self._lock:
            self.cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self._lock:
            total_entries = len(self.cache)
            total_hits = sum(entry.get('hits', 0) for entry in self.cache.values())
            memory_usage = sum(len(str(entry['value'])) for entry in self.cache.values())
            
            return {
                'total_entries': total_entries,
                'total_hits': total_hits,
                'memory_usage_bytes': memory_usage,
                'cache_keys': list(self.cache.keys())
            }
    
    def cleanup_expired(self) -> int:
        """Remove expired entries and return count removed"""
        with self._lock:
            current_time = time.time()
            expired_keys = [
                key for key, entry in self.cache.items()
                if current_time > entry['expires']
            ]
            
            for key in expired_keys:
                del self.cache[key]
            
            return len(expired_keys)


class HighlandTowerCache:
    """Highland Tower Development specific caching layer"""
    
    def __init__(self):
        self.cache = InMemoryCache(default_ttl=1800)  # 30 minutes default
        
        # Cache TTLs for different data types
        self.ttl_config = {
            'rfi_data': 900,        # 15 minutes - frequently updated
            'project_health': 1800,  # 30 minutes - moderate updates
            'subcontractors': 3600,  # 1 hour - stable data
            'analytics': 1800,       # 30 minutes - computed data
            'dashboard': 600,        # 10 minutes - real-time updates
            'reports': 3600          # 1 hour - static reports
        }
    
    def cache_rfi_data(self, rfis: list) -> None:
        """Cache RFI data with appropriate TTL"""
        self.cache.set(
            'highland_tower_rfis',
            rfis,
            self.ttl_config['rfi_data']
        )
    
    def get_rfi_data(self) -> Optional[list]:
        """Get cached RFI data"""
        return self.cache.get('highland_tower_rfis')
    
    def cache_project_health(self, health_data: dict) -> None:
        """Cache project health metrics"""
        self.cache.set(
            'highland_tower_health',
            health_data,
            self.ttl_config['project_health']
        )
    
    def get_project_health(self) -> Optional[dict]:
        """Get cached project health"""
        return self.cache.get('highland_tower_health')
    
    def cache_analytics_data(self, analytics: dict) -> None:
        """Cache analytics computation results"""
        self.cache.set(
            'highland_tower_analytics',
            analytics,
            self.ttl_config['analytics']
        )
    
    def get_analytics_data(self) -> Optional[dict]:
        """Get cached analytics data"""
        return self.cache.get('highland_tower_analytics')
    
    def invalidate_rfi_cache(self) -> None:
        """Invalidate RFI-related cache entries"""
        self.cache.delete('highland_tower_rfis')
        self.cache.delete('highland_tower_health')
        self.cache.delete('highland_tower_analytics')
    
    def get_cache_summary(self) -> dict:
        """Get Highland Tower cache summary"""
        stats = self.cache.get_stats()
        
        return {
            'highland_tower_cache_status': 'active',
            'total_cached_items': stats['total_entries'],
            'cache_hits': stats['total_hits'],
            'memory_usage': f"{stats['memory_usage_bytes']} bytes",
            'cached_data_types': [
                'RFI Data', 'Project Health', 'Analytics', 
                'Subcontractors', 'Dashboard Metrics'
            ]
        }


def cache_result(cache_instance: InMemoryCache, key_prefix: str, ttl: int = 3600):
    """Decorator for caching function results"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = f"{key_prefix}_{func.__name__}_{hash((args, tuple(sorted(kwargs.items()))))}"
            
            # Try to get from cache first
            cached_result = cache_instance.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_instance.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator


# Global Highland Tower cache instance
highland_cache = HighlandTowerCache()


# Decorators for Highland Tower specific caching
def cache_rfi_operation(ttl: int = 900):
    """Cache RFI operations for 15 minutes"""
    return cache_result(highland_cache.cache, "highland_rfi", ttl)


def cache_analytics_operation(ttl: int = 1800):
    """Cache analytics operations for 30 minutes"""
    return cache_result(highland_cache.cache, "highland_analytics", ttl)


def cache_dashboard_data(ttl: int = 600):
    """Cache dashboard data for 10 minutes"""
    return cache_result(highland_cache.cache, "highland_dashboard", ttl)