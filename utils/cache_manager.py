"""
Cache management utilities for gcPanel.

This module provides functions for caching frequently accessed data,
implementing cache expiration, and managing cache size.
"""

import os
import logging
import pickle
import hashlib
import time
from functools import wraps
from datetime import datetime, timedelta
import threading
import streamlit as st

# Setup logging
logger = logging.getLogger(__name__)

# Constants
CACHE_DIR = os.environ.get("CACHE_DIR", "cache")
CACHE_ENABLED = os.environ.get("CACHE_ENABLED", "true").lower() == "true"
CACHE_TTL = int(os.environ.get("CACHE_TTL", "3600"))  # Default 1 hour
CACHE_MAX_SIZE = int(os.environ.get("CACHE_MAX_SIZE", "104857600"))  # Default 100MB
CACHE_CLEANUP_INTERVAL = int(os.environ.get("CACHE_CLEANUP_INTERVAL", "3600"))  # Default 1 hour

# In-memory cache
memory_cache = {}
memory_cache_metadata = {}

# Thread for background cache cleanup
cleanup_thread = None
cleanup_thread_running = False

def ensure_cache_dir():
    """Ensure cache directory exists."""
    os.makedirs(CACHE_DIR, exist_ok=True)

def generate_cache_key(func_name, args, kwargs):
    """
    Generate a cache key for a function call.
    
    Args:
        func_name: Function name
        args: Function arguments
        kwargs: Function keyword arguments
        
    Returns:
        str: Cache key
    """
    # Create a unique representation of the function call
    key_parts = [func_name]
    
    # Add args
    for arg in args:
        key_parts.append(str(arg))
    
    # Add kwargs (sorted for consistency)
    for key in sorted(kwargs.keys()):
        key_parts.append(f"{key}={kwargs[key]}")
    
    # Join and hash
    key_str = "_".join(key_parts)
    return hashlib.md5(key_str.encode()).hexdigest()

def get_disk_cache_path(cache_key):
    """
    Get the file path for a disk cache item.
    
    Args:
        cache_key: Cache key
        
    Returns:
        str: File path
    """
    ensure_cache_dir()
    return os.path.join(CACHE_DIR, f"{cache_key}.cache")

def get_from_memory_cache(cache_key):
    """
    Get an item from the memory cache.
    
    Args:
        cache_key: Cache key
        
    Returns:
        tuple: (item, found)
    """
    if not CACHE_ENABLED:
        return None, False
    
    if cache_key not in memory_cache:
        return None, False
    
    # Check if expired
    metadata = memory_cache_metadata.get(cache_key, {})
    expires_at = metadata.get("expires_at")
    
    if expires_at and datetime.now() > expires_at:
        # Expired
        del memory_cache[cache_key]
        del memory_cache_metadata[cache_key]
        return None, False
    
    # Update access time
    memory_cache_metadata[cache_key]["accessed_at"] = datetime.now()
    
    return memory_cache[cache_key], True

def set_in_memory_cache(cache_key, item, ttl=None):
    """
    Set an item in the memory cache.
    
    Args:
        cache_key: Cache key
        item: Item to cache
        ttl: Time to live in seconds
    """
    if not CACHE_ENABLED:
        return
    
    if ttl is None:
        ttl = CACHE_TTL
    
    # Set item
    memory_cache[cache_key] = item
    
    # Set metadata
    now = datetime.now()
    memory_cache_metadata[cache_key] = {
        "created_at": now,
        "accessed_at": now,
        "expires_at": now + timedelta(seconds=ttl)
    }
    
    # Check if we need to do cleanup
    cleanup_memory_cache_if_needed()

def get_from_disk_cache(cache_key):
    """
    Get an item from the disk cache.
    
    Args:
        cache_key: Cache key
        
    Returns:
        tuple: (item, found)
    """
    if not CACHE_ENABLED:
        return None, False
    
    cache_path = get_disk_cache_path(cache_key)
    
    if not os.path.exists(cache_path):
        return None, False
    
    # Check if expired
    modified_time = os.path.getmtime(cache_path)
    if time.time() - modified_time > CACHE_TTL:
        # Expired
        os.remove(cache_path)
        return None, False
    
    try:
        with open(cache_path, "rb") as f:
            return pickle.load(f), True
    except Exception as e:
        logger.error(f"Error loading from disk cache: {str(e)}")
        return None, False

def set_in_disk_cache(cache_key, item):
    """
    Set an item in the disk cache.
    
    Args:
        cache_key: Cache key
        item: Item to cache
    """
    if not CACHE_ENABLED:
        return
    
    ensure_cache_dir()
    cache_path = get_disk_cache_path(cache_key)
    
    try:
        with open(cache_path, "wb") as f:
            pickle.dump(item, f)
    except Exception as e:
        logger.error(f"Error saving to disk cache: {str(e)}")
    
    # Check if we need to do cleanup
    cleanup_disk_cache_if_needed()

def cleanup_memory_cache_if_needed():
    """Clean up memory cache if it's too large."""
    if len(memory_cache) <= 100:
        return
    
    # Sort by last access time
    items = sorted(
        memory_cache_metadata.items(),
        key=lambda x: x[1].get("accessed_at", datetime.min)
    )
    
    # Remove oldest 20% of items
    items_to_remove = items[:int(len(items) * 0.2)]
    
    for key, _ in items_to_remove:
        if key in memory_cache:
            del memory_cache[key]
        if key in memory_cache_metadata:
            del memory_cache_metadata[key]
    
    logger.info(f"Cleaned up {len(items_to_remove)} items from memory cache")

def cleanup_disk_cache_if_needed():
    """Clean up disk cache if it's too large."""
    ensure_cache_dir()
    
    # Get cache size
    total_size = 0
    cache_files = []
    
    for filename in os.listdir(CACHE_DIR):
        if filename.endswith(".cache"):
            file_path = os.path.join(CACHE_DIR, filename)
            file_size = os.path.getsize(file_path)
            modified_time = os.path.getmtime(file_path)
            total_size += file_size
            cache_files.append((file_path, modified_time, file_size))
    
    if total_size <= CACHE_MAX_SIZE:
        return
    
    # Sort by last modified time
    cache_files.sort(key=lambda x: x[1])
    
    # Remove oldest files until we're under the limit
    size_to_remove = total_size - CACHE_MAX_SIZE
    removed = 0
    
    for file_path, _, file_size in cache_files:
        os.remove(file_path)
        removed += 1
        size_to_remove -= file_size
        
        if size_to_remove <= 0:
            break
    
    logger.info(f"Cleaned up {removed} files from disk cache")

def background_cleanup():
    """Run cache cleanup in the background."""
    global cleanup_thread_running
    
    while cleanup_thread_running:
        try:
            # Clean up expired items from memory cache
            now = datetime.now()
            expired_keys = [
                key for key, metadata in memory_cache_metadata.items()
                if metadata.get("expires_at") and metadata["expires_at"] < now
            ]
            
            for key in expired_keys:
                if key in memory_cache:
                    del memory_cache[key]
                if key in memory_cache_metadata:
                    del memory_cache_metadata[key]
            
            if expired_keys:
                logger.info(f"Cleaned up {len(expired_keys)} expired items from memory cache")
            
            # Clean up expired items from disk cache
            ensure_cache_dir()
            now_time = time.time()
            removed = 0
            
            for filename in os.listdir(CACHE_DIR):
                if filename.endswith(".cache"):
                    file_path = os.path.join(CACHE_DIR, filename)
                    modified_time = os.path.getmtime(file_path)
                    
                    if now_time - modified_time > CACHE_TTL:
                        os.remove(file_path)
                        removed += 1
            
            if removed:
                logger.info(f"Cleaned up {removed} expired items from disk cache")
            
            # Sleep until next cleanup
            time.sleep(CACHE_CLEANUP_INTERVAL)
            
        except Exception as e:
            logger.error(f"Error in background cleanup: {str(e)}")
            time.sleep(60)  # Sleep shorter time on error

def start_background_cleanup():
    """Start background cleanup thread."""
    global cleanup_thread, cleanup_thread_running
    
    if cleanup_thread and cleanup_thread.is_alive():
        return
    
    cleanup_thread_running = True
    cleanup_thread = threading.Thread(target=background_cleanup)
    cleanup_thread.daemon = True
    cleanup_thread.start()
    
    logger.info("Started background cache cleanup")

def stop_background_cleanup():
    """Stop background cleanup thread."""
    global cleanup_thread_running
    
    cleanup_thread_running = False
    logger.info("Stopped background cache cleanup")

def cached(ttl=None, use_memory=True, use_disk=False):
    """
    Decorator for caching function results.
    
    Args:
        ttl: Time to live in seconds
        use_memory: Whether to use memory cache
        use_disk: Whether to use disk cache
        
    Returns:
        Function decorator
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not CACHE_ENABLED:
                return func(*args, **kwargs)
            
            # Generate cache key
            cache_key = generate_cache_key(func.__name__, args, kwargs)
            
            # Try memory cache
            if use_memory:
                result, found = get_from_memory_cache(cache_key)
                if found:
                    return result
            
            # Try disk cache
            if use_disk:
                result, found = get_from_disk_cache(cache_key)
                if found:
                    # Also store in memory for faster access next time
                    if use_memory:
                        set_in_memory_cache(cache_key, result, ttl)
                    return result
            
            # Call function
            result = func(*args, **kwargs)
            
            # Store in cache
            if use_memory:
                set_in_memory_cache(cache_key, result, ttl)
            if use_disk:
                set_in_disk_cache(cache_key, result)
            
            return result
        
        return wrapper
    
    return decorator

def streamlit_cache(ttl=None):
    """
    Decorator for caching Streamlit function results using @st.cache_data.
    
    Args:
        ttl: Time to live in seconds
        
    Returns:
        Function decorator
    """
    if ttl is None:
        ttl = CACHE_TTL
    
    def decorator(func):
        cached_func = st.cache_data(ttl=ttl)(func)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return cached_func(*args, **kwargs)
        
        return wrapper
    
    return decorator

def initialize_cache():
    """Initialize the cache system."""
    ensure_cache_dir()
    
    if CACHE_ENABLED:
        start_background_cleanup()
        logger.info("Cache system initialized")
    else:
        logger.info("Cache system disabled")