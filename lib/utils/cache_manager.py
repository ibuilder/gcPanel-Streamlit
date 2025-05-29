"""
Cache Manager for gcPanel.

This module provides caching utilities to improve application performance:
- Function-level caching with TTL (Time To Live)
- Session-based caching for user-specific data
- Data prefetching mechanisms for frequently accessed information
"""

import streamlit as st
import functools
import time
import hashlib
import json
from datetime import datetime, timedelta

class CacheManager:
    """
    Cache manager for improved application performance.
    """
    
    @staticmethod
    def initialize_cache():
        """Initialize application cache in session state."""
        if "data_cache" not in st.session_state:
            st.session_state.data_cache = {}
        
        if "cache_metadata" not in st.session_state:
            st.session_state.cache_metadata = {
                "size": 0,
                "hits": 0,
                "misses": 0,
                "last_cleanup": datetime.now().timestamp()
            }
    
    @staticmethod
    def cached(ttl_seconds=300, max_size=100, user_specific=False):
        """
        Decorator for caching function results.
        
        Args:
            ttl_seconds (int): Time to live in seconds
            max_size (int): Maximum number of items in cache
            user_specific (bool): Whether cache depends on user identity
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Initialize cache if needed
                CacheManager.initialize_cache()
                
                # Create a cache key
                key_parts = [func.__name__]
                
                # Add user-specific info if needed
                if user_specific and "user" in st.session_state:
                    key_parts.append(st.session_state.user.get("username", "anonymous"))
                
                # Add args and kwargs to key
                for arg in args:
                    key_parts.append(str(arg))
                
                sorted_kwargs = sorted(kwargs.items())
                for k, v in sorted_kwargs:
                    key_parts.append(f"{k}={v}")
                
                # Create a hash-based key
                key = hashlib.md5(json.dumps(key_parts).encode()).hexdigest()
                
                # Check if result in cache and not expired
                if key in st.session_state.data_cache:
                    entry = st.session_state.data_cache[key]
                    if entry["expire_time"] > time.time():
                        # Update hit counter
                        st.session_state.cache_metadata["hits"] += 1
                        return entry["data"]
                
                # Not in cache or expired, call the function
                st.session_state.cache_metadata["misses"] += 1
                result = func(*args, **kwargs)
                
                # Store in cache
                st.session_state.data_cache[key] = {
                    "data": result,
                    "expire_time": time.time() + ttl_seconds
                }
                
                # Update cache size
                st.session_state.cache_metadata["size"] = len(st.session_state.data_cache)
                
                # Check if cleanup needed
                if len(st.session_state.data_cache) > max_size:
                    CacheManager.cleanup_cache()
                
                return result
            return wrapper
        return decorator
    
    @staticmethod
    def user_data_cache(key, value=None, ttl_minutes=60):
        """
        Get or set user-specific cached data.
        
        Args:
            key (str): Cache key
            value (any, optional): Value to cache (if None, just retrieves)
            ttl_minutes (int): Cache TTL in minutes
            
        Returns:
            any: Cached value or None if not found
        """
        # Initialize cache if needed
        CacheManager.initialize_cache()
        
        # Prefix the key with username for isolation
        if "user" in st.session_state:
            username = st.session_state.user.get("username", "anonymous")
            full_key = f"user_{username}_{key}"
        else:
            full_key = f"user_anonymous_{key}"
        
        # Set value if provided
        if value is not None:
            st.session_state.data_cache[full_key] = {
                "data": value,
                "expire_time": time.time() + (ttl_minutes * 60)
            }
            return value
            
        # Get value if in cache and not expired
        if full_key in st.session_state.data_cache:
            entry = st.session_state.data_cache[full_key]
            if entry["expire_time"] > time.time():
                st.session_state.cache_metadata["hits"] += 1
                return entry["data"]
        
        # Not found or expired
        st.session_state.cache_metadata["misses"] += 1
        return None
    
    @staticmethod
    def invalidate_user_cache():
        """Invalidate all user-specific cache entries."""
        if "data_cache" not in st.session_state:
            return
            
        if "user" in st.session_state:
            username = st.session_state.user.get("username", "anonymous")
            prefix = f"user_{username}_"
            
            # Find all keys for this user
            keys_to_remove = [k for k in st.session_state.data_cache.keys() 
                             if k.startswith(prefix)]
            
            # Remove them
            for key in keys_to_remove:
                del st.session_state.data_cache[key]
                
            # Update cache size
            st.session_state.cache_metadata["size"] = len(st.session_state.data_cache)
    
    @staticmethod
    def invalidate_cache(pattern=None):
        """
        Invalidate cache entries matching a pattern.
        
        Args:
            pattern (str, optional): Pattern to match keys. If None, clears all.
        """
        if "data_cache" not in st.session_state:
            return
            
        if pattern is None:
            # Clear all
            st.session_state.data_cache = {}
            st.session_state.cache_metadata["size"] = 0
        else:
            # Clear matching pattern
            keys_to_remove = [k for k in st.session_state.data_cache.keys() 
                             if pattern in k]
            
            for key in keys_to_remove:
                del st.session_state.data_cache[key]
                
            # Update cache size
            st.session_state.cache_metadata["size"] = len(st.session_state.data_cache)
    
    @staticmethod
    def cleanup_cache(force=False):
        """
        Remove expired items and enforce size limits.
        
        Args:
            force (bool): Force cleanup regardless of timing
        """
        # Check if we need to run cleanup
        now = datetime.now().timestamp()
        last_cleanup = st.session_state.cache_metadata.get("last_cleanup", 0)
        
        # Only run cleanup every 5 minutes unless forced
        if not force and (now - last_cleanup < 300):
            return
            
        # Update last cleanup time
        st.session_state.cache_metadata["last_cleanup"] = now
        
        # Remove expired entries
        current_time = time.time()
        keys_to_remove = []
        
        for key, entry in st.session_state.data_cache.items():
            if entry["expire_time"] < current_time:
                keys_to_remove.append(key)
                
        for key in keys_to_remove:
            del st.session_state.data_cache[key]
        
        # Update cache size
        st.session_state.cache_metadata["size"] = len(st.session_state.data_cache)
    
    @staticmethod
    def get_cache_stats():
        """
        Get cache statistics.
        
        Returns:
            dict: Cache statistics
        """
        if "cache_metadata" not in st.session_state:
            return {
                "size": 0,
                "hits": 0, 
                "misses": 0,
                "hit_ratio": 0,
                "last_cleanup": "Never"
            }
            
        stats = st.session_state.cache_metadata.copy()
        
        # Calculate hit ratio
        total_requests = stats["hits"] + stats["misses"]
        if total_requests > 0:
            stats["hit_ratio"] = stats["hits"] / total_requests
        else:
            stats["hit_ratio"] = 0
            
        # Format last cleanup
        if "last_cleanup" in stats:
            stats["last_cleanup"] = datetime.fromtimestamp(
                stats["last_cleanup"]
            ).strftime("%Y-%m-%d %H:%M:%S")
            
        return stats


# Export the decorator for easy use
cached = CacheManager.cached