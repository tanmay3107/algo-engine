# dijkstra_shortest_path.py
import heapq

class NetworkGraph:
    def __init__(self):
        # Adjacency list: map node -> list of (neighbor, weight)
        self.graph = {}

    def add_edge(self, source: str, destination: str, latency_ms: int):
        """
        Adds a bi-directional network link with a specific latency (weight).
        """
        if source not in self.graph:
            self.graph[source] = []
        if destination not in self.graph:
            self.graph[destination] = []
            
        self.graph[source].append((destination, latency_ms))
        self.graph[destination].append((source, latency_ms))

    def find_fastest_route(self, start_node: str, target_node: str):
        """
        Executes Dijkstra's Algorithm using a Min-Heap.
        Returns the shortest time and the exact path taken.
        """
        # Dictionary to track the minimum latency to reach each node
        min_latencies = {node: float('inf') for node in self.graph}
        min_latencies[start_node] = 0
        
        # Priority Queue stores tuples of (cumulative_latency, current_node)
        pq = [(0, start_node)]
        
        # Dictionary to track the path so we can reconstruct the route
        previous_nodes = {node: None for node in self.graph}
        
        while pq:
            current_latency, current_node = heapq.heappop(pq)
            
            # If we reached the target, we can stop searching early
            if current_node == target_node:
                break
                
            # If we found a slower path to a node we've already optimized, skip it
            if current_latency > min_latencies[current_node]:
                continue
                
            # Check all connected neighbors
            for neighbor, edge_latency in self.graph[current_node]:
                new_latency = current_latency + edge_latency
                
                # If we found a faster way to reach the neighbor, update it
                if new_latency < min_latencies[neighbor]:
                    min_latencies[neighbor] = new_latency
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (new_latency, neighbor))
                    
        # Reconstruct the optimal path
        path = []
        current = target_node
        while current is not None:
            path.append(current)
            current = previous_nodes[current]
        path.reverse()
        
        return min_latencies[target_node], path


# --- Quick Test ---
if __name__ == "__main__":
    print("🌐 Booting Network Routing Engine...")
    network = NetworkGraph()
    
    # Building a simulated server topology
    network.add_edge("API_Gateway", "Auth_Server", 10)
    network.add_edge("API_Gateway", "Cache_A", 50)
    network.add_edge("Auth_Server", "Cache_A", 20)
    network.add_edge("Auth_Server", "DB_Primary", 60)
    network.add_edge("Cache_A", "DB_Primary", 15)
    network.add_edge("DB_Primary", "ML_Inference", 5)
    
    start = "API_Gateway"
    target = "ML_Inference"
    
    print(f"\n🔍 Calculating optimal route from {start} to {target}...")
    optimal_time, optimal_path = network.find_fastest_route(start, target)
    
    print(f"\n✅ Fastest Route Found: {optimal_time}ms")
    print(f"🛣️  Path Taken: {' -> '.join(optimal_path)}")