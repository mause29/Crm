# Synchronous wrapper functions for backward compatibility
from typing import Any, Optional
import asyncio

# Import the cache manager from the async cache module
from .cache import cache_manager

def get_cache(key: str) -> Optional[Any]:
    """Synchronous wrapper for cache get operation."""
    try:
        # For synchronous calls, we need to run the async function in a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(cache_manager.get(key))
        loop.close()
        return result
    except Exception as e:
        print(f"Cache get error: {e}")
        return None

def set_cache(key: str, value: Any, ttl: int = 300) -> None:
    """Synchronous wrapper for cache set operation."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(cache_manager.set(key, value, ttl))
        loop.close()
    except Exception as e:
        print(f"Cache set error: {e}")
