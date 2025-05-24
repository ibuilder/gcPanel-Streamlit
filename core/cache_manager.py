"""
Enterprise Caching System for gcPanel Highland Tower Development

Implements Redis caching, lazy loading, and performance optimization
for high-performance construction management operations.
"""

import redis
import json
import pickle
import hashlib
from typing import Any, Optional, Dict, List
from functools import wraps
from datetime import datetime, timedelta
import streamlit as st
import logging
import os

class CacheManager:
    """Enterprise caching manager with Redis and in-memory fallback"""
    
    def __init__(self):
        self.redis_client = None
        self.local_cache = {}
        self.cache_stats = {"hits": 0, "misses": 0}
        self.setup_logging()
        self.initialize_redis()
    
    def setup_logging(self):
        """Setup cache operation logging"""
        self.logger = logging.getLogger('CacheManager')
    
    def initialize_redis(self):
        """Initialize Redis connection with fallback to local cache"""
        try:
            redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379')
            self.redis_client = redis.from_url(redis_url, decode_responses=False)
            self.redis_client.ping()
            self.logger.info("Redis cache initialized successfully")
        except Exception as e:
            self.logger.warning(f"Redis unavailable, using local cache: {e}")
            self.redis_client = None
    
    def _generate_key(self, key: str, params: Dict = None) -> str:
        """Generate cache key with optional parameters"""
        if params:
            param_str = json.dumps(params, sort_keys=True)
            key_data = f"{key}:{param_str}"
        else:
            key_data = key
        
        return f"gcpanel:highland_tower:{hashlib.md5(key_data.encode()).hexdigest()}"
    
    def get(self, key: str, params: Dict = None) -> Optional[Any]:
        """Get value from cache"""
        cache_key = self._generate_key(key, params)
        
        try:
            if self.redis_client:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    self.cache_stats["hits"] += 1
                    return pickle.loads(cached_data)
            else:
                if cache_key in self.local_cache:
                    entry = self.local_cache[cache_key]
                    if entry["expires"] > datetime.now():
                        self.cache_stats["hits"] += 1
                        return entry["data"]
                    else:
                        del self.local_cache[cache_key]
            
            self.cache_stats["misses"] += 1
            return None
            
        except Exception as e:
            self.logger.error(f"Cache get error: {e}")
            self.cache_stats["misses"] += 1
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600, params: Dict = None):
        """Set value in cache with TTL"""
        cache_key = self._generate_key(key, params)
        
        try:
            if self.redis_client:
                serialized_data = pickle.dumps(value)
                self.redis_client.setex(cache_key, ttl, serialized_data)
            else:
                expires = datetime.now() + timedelta(seconds=ttl)
                self.local_cache[cache_key] = {
                    "data": value,
                    "expires": expires
                }
                
        except Exception as e:
            self.logger.error(f"Cache set error: {e}")
    
    def delete(self, key: str, params: Dict = None):
        """Delete value from cache"""
        cache_key = self._generate_key(key, params)
        
        try:
            if self.redis_client:
                self.redis_client.delete(cache_key)
            else:
                self.local_cache.pop(cache_key, None)
                
        except Exception as e:
            self.logger.error(f"Cache delete error: {e}")
    
    def clear_pattern(self, pattern: str):
        """Clear cache entries matching pattern"""
        try:
            if self.redis_client:
                keys = self.redis_client.keys(f"gcpanel:highland_tower:{pattern}*")
                if keys:
                    self.redis_client.delete(*keys)
            else:
                keys_to_delete = [k for k in self.local_cache.keys() 
                                if pattern in k]
                for key in keys_to_delete:
                    del self.local_cache[key]
                    
        except Exception as e:
            self.logger.error(f"Cache clear error: {e}")
    
    def get_stats(self) -> Dict:
        """Get cache performance statistics"""
        total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
        hit_rate = (self.cache_stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "hits": self.cache_stats["hits"],
            "misses": self.cache_stats["misses"],
            "hit_rate": f"{hit_rate:.2f}%",
            "cache_type": "Redis" if self.redis_client else "Local"
        }

def cache_result(ttl: int = 3600, key_prefix: str = ""):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_manager = get_cache_manager()
            
            # Generate cache key from function name and arguments
            func_key = f"{key_prefix}{func.__name__}"
            params = {"args": str(args), "kwargs": str(kwargs)}
            
            # Try to get from cache
            cached_result = cache_manager.get(func_key, params)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(func_key, result, ttl, params)
            
            return result
        return wrapper
    return decorator

@st.cache_resource
def get_cache_manager():
    """Get cached cache manager instance"""
    return CacheManager()

class LazyDataLoader:
    """Lazy loading system for large datasets with pagination"""
    
    def __init__(self, data_source_func, page_size: int = 50):
        self.data_source_func = data_source_func
        self.page_size = page_size
        self.cache_manager = get_cache_manager()
    
    def load_page(self, page: int, filters: Dict = None) -> Dict:
        """Load a specific page of data with caching"""
        cache_key = f"lazy_data_{self.data_source_func.__name__}_page_{page}"
        
        # Try cache first
        cached_data = self.cache_manager.get(cache_key, filters)
        if cached_data:
            return cached_data
        
        # Load from source
        offset = page * self.page_size
        data = self.data_source_func(offset=offset, limit=self.page_size, filters=filters)
        
        # Cache the result
        self.cache_manager.set(cache_key, data, ttl=1800, params=filters)
        
        return data
    
    def render_paginated_table(self, data_func, filters: Dict = None):
        """Render paginated table with lazy loading"""
        # Initialize pagination state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 0
        
        # Load current page
        page_data = self.load_page(st.session_state.current_page, filters)
        
        # Display data
        if page_data.get('data'):
            st.dataframe(page_data['data'], use_container_width=True)
            
            # Pagination controls
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("⏮️ First", disabled=st.session_state.current_page == 0):
                    st.session_state.current_page = 0
                    st.rerun()
            
            with col2:
                if st.button("⬅️ Previous", disabled=st.session_state.current_page == 0):
                    st.session_state.current_page -= 1
                    st.rerun()
            
            with col3:
                total_pages = page_data.get('total_pages', 1)
                if st.button("➡️ Next", disabled=st.session_state.current_page >= total_pages - 1):
                    st.session_state.current_page += 1
                    st.rerun()
            
            with col4:
                if st.button("⏭️ Last", disabled=st.session_state.current_page >= total_pages - 1):
                    st.session_state.current_page = total_pages - 1
                    st.rerun()
            
            # Page info
            st.caption(f"Page {st.session_state.current_page + 1} of {total_pages} | "
                      f"Total records: {page_data.get('total_count', 0)}")
        
        else:
            st.info("No data available")

def preload_critical_data():
    """Preload critical Highland Tower Development data"""
    cache_manager = get_cache_manager()
    
    # List of critical data to preload
    critical_datasets = [
        "active_rfis",
        "daily_reports_summary", 
        "quality_metrics",
        "clash_detection_summary",
        "project_metrics"
    ]
    
    for dataset in critical_datasets:
        if not cache_manager.get(dataset):
            # This would load actual data in production
            st.info(f"Preloading {dataset} for Highland Tower Development...")