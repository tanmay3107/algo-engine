# lru_cache.py

class Node:
    """A Node in our Doubly Linked List."""
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # Map key -> Node pointer for O(1) lookups
        
        # We use dummy Head and Tail nodes to eliminate edge cases 
        # (like inserting into an empty list or deleting the last node).
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        """Helper to physically detach a node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _insert_right_after_head(self, node: Node):
        """Helper to insert a node at the Most Recently Used (MRU) position."""
        next_node = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = next_node
        next_node.prev = node

    def get(self, key: int) -> int:
        """
        Retrieves a value. If found, it becomes the most recently used.
        Time Complexity: O(1)
        """
        if key in self.cache:
            node = self.cache[key]
            # Since we just accessed it, pull it out and put it at the front (MRU)
            self._remove(node)
            self._insert_right_after_head(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        """
        Inserts or updates a value. Evicts the LRU item if capacity is breached.
        Time Complexity: O(1)
        """
        if key in self.cache:
            # If it already exists, remove the old node before updating
            self._remove(self.cache[key])
            
        new_node = Node(key, value)
        self.cache[key] = new_node
        self._insert_right_after_head(new_node)
        
        # If we exceed our physical memory limit, trigger the eviction policy
        if len(self.cache) > self.capacity:
            # The Least Recently Used item is always right before the dummy tail
            lru_node = self.tail.prev
            self._remove(lru_node)
            del self.cache[lru_node.key]


# --- Quick Test ---
if __name__ == "__main__":
    print("🧠 Booting LRU Cache (Capacity: 3)...")
    cache = LRUCache(3)
    
    # 1. Fill the cache
    cache.put(1, 100) # List: [1]
    cache.put(2, 200) # List: [2, 1]
    cache.put(3, 300) # List: [3, 2, 1]
    print("📥 Pushed keys 1, 2, 3.")
    
    # 2. Access an old key to refresh its status
    print(f"\n🔍 GET Key 1: {cache.get(1)} -> (Moved to Most Recently Used)") 
    # List is now: [1, 3, 2]
    
    # 3. Breach capacity to force an eviction
    print("\n📥 Pushing Key 4 (Breaching capacity)...")
    cache.put(4, 400) 
    # List becomes [4, 1, 3]. Key 2 is evicted!
    
    # 4. Verify eviction
    print(f"🔍 GET Key 2: {cache.get(2)} -> (Expected -1, it was evicted)")
    print(f"🔍 GET Key 3: {cache.get(3)} -> (Found, now moved to MRU)")