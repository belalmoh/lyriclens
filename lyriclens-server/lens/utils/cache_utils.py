"""
Caching utilities for the lyriclens application.

This module provides functions for working with Redis cache,
including connection testing, cache key generation, and methods 
for getting and setting cached data.

Usage:
------

1. Test Redis Connection:
   ```python
   from lens.utils.cache_utils import test_redis_connection
   
   # Test if Redis is available
   cache_enabled = test_redis_connection()
   if cache_enabled:
       print("Redis caching is available")
   else:
       print("Redis caching is not available, falling back to non-cached operation")
   ```

2. Generate Cache Keys:
   ```python
   from lens.utils.cache_utils import generate_cache_key
   
   # Generate a cache key for a specific resource
   cache_key = generate_cache_key("my_prefix", "param1", "param2")
   # Returns: "my_prefix:<md5_hash_of_joined_params>"
   ```

3. Get and Set Cache Data:
   ```python
   from lens.utils.cache_utils import get_from_cache, save_to_cache
   
   # Check if data exists in cache
   cached_data = get_from_cache(cache_key, cache_enabled)
   if cached_data:
       # Use cached data
       print(f"Cache hit: {cached_data}")
   else:
       # Generate new data
       data = compute_expensive_operation()
       # Save to cache with 1 hour timeout
       save_to_cache(cache_key, data, timeout=3600, cache_enabled=cache_enabled)
   ```

4. Complete Example:
   ```python
   from lens.utils.cache_utils import (
       test_redis_connection,
       generate_cache_key,
       get_from_cache,
       save_to_cache
   )
   
   def my_service_function(param1, param2):
       # Check if Redis is available
       cache_enabled = test_redis_connection()
       
       # Generate a cache key
       cache_key = generate_cache_key("my_service", param1, param2)
       
       # Try to get from cache
       cached_result = get_from_cache(cache_key, cache_enabled)
       if cached_result:
           return cached_result
           
       # If not in cache, compute the result
       result = compute_expensive_operation(param1, param2)
       
       # Save to cache
       save_to_cache(cache_key, result, timeout=86400, cache_enabled=cache_enabled)
       
       return result
   ```
"""

import hashlib
import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from redis.exceptions import RedisError

# Set up logging
logger = logging.getLogger(__name__)

def test_redis_connection():
    """
    Test the Redis connection to ensure caching will work.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        redis_conn = get_redis_connection("default")
        redis_conn.ping()
        logger.info("Redis connection successful, caching enabled")
        return True
    except RedisError as e:
        logger.error(f"Redis connection error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error testing Redis connection: {e}")
        return False

def generate_cache_key(prefix, *args):
    """
    Generate a cache key based on provided arguments.
    
    Args:
        prefix (str): Prefix for the cache key (e.g., 'lyrics_analysis')
        *args: Variable length arguments to be included in the key
        
    Returns:
        str: A unique cache key
    """
    # Create a string to hash by joining all arguments
    key_string = ':'.join([str(arg).lower().strip() for arg in args])
    
    # Create an MD5 hash of the key string
    hash_obj = hashlib.md5(key_string.encode())
    
    # Return the cache key
    return f"{prefix}:{hash_obj.hexdigest()}"

def get_from_cache(cache_key, cache_enabled=True):
    """
    Get data from cache if available.
    
    Args:
        cache_key (str): The cache key to retrieve
        cache_enabled (bool): Flag to indicate if caching is enabled
        
    Returns:
        dict or None: Cached data or None if not found
    """
    if not cache_enabled:
        return None
        
    try:
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info(f"Cache hit for '{cache_key}'")
            return cached_data
            
        logger.info(f"Cache miss for '{cache_key}'")
        return None
    except Exception as e:
        logger.error(f"Error getting from cache: {e}")
        return None

def save_to_cache(cache_key, data, timeout=60*60*24, cache_enabled=True):
    """
    Save data to cache.
    
    Args:
        cache_key (str): The cache key to use
        data (dict): The data to cache
        timeout (int): Cache timeout in seconds (default: 24 hours)
        cache_enabled (bool): Flag to indicate if caching is enabled
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not cache_enabled:
        return False
        
    try:
        cache.set(cache_key, data, timeout=timeout)
        logger.info(f"Saved to cache: '{cache_key}'")
        return True
    except Exception as e:
        logger.error(f"Error saving to cache: {e}")
        return False 