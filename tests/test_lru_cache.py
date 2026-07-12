import pytest
from lru_cache import LRUCache

def test_lru_cache_initialization():
    """Verifies the cache initializes with the correct capacity."""
    cache = LRUCache(2)
    assert cache.capacity == 2
    assert cache.get(1) == -1 # Empty cache should return -1

def test_lru_cache_eviction_policy():
    """
    Forces the cache to breach capacity and verifies the 
    Least Recently Used item is physically evicted from memory.
    """
    cache = LRUCache(2)
    
    # Fill to capacity
    cache.put(1, 100)
    cache.put(2, 200)
    assert cache.get(1) == 100 # Key 1 is now Most Recently Used
    
    # Breach capacity (should evict Key 2)
    cache.put(3, 300)
    assert cache.get(2) == -1 # Key 2 must be deleted
    assert cache.get(1) == 100 # Key 1 must still exist
    assert cache.get(3) == 300 # Key 3 must exist

def test_lru_cache_update_existing_key():
    """Verifies that updating an existing key refreshes its MRU status."""
    cache = LRUCache(2)
    cache.put(1, 100)
    cache.put(2, 200)
    
    # Update key 1 (moves to MRU)
    cache.put(1, 999) 
    
    # Push key 3 (evicts key 2, NOT key 1)
    cache.put(3, 300)
    
    assert cache.get(2) == -1 # Evicted
    assert cache.get(1) == 999 # Updated and kept