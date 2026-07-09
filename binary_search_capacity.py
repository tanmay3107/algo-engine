# binary_search_capacity.py
import math

class MLInfrastructureOptimizer:
    def __init__(self):
        pass

    def _can_process_in_time(self, payloads: list[int], batch_size: int, time_limit: int) -> bool:
        """
        Helper function: Simulates if a specific batch size is fast enough 
        to process all payloads within the given time limit.
        """
        hours_needed = 0
        for payload in payloads:
            # If a payload has 7 items and batch size is 3, it takes ceil(7/3) = 3 hours
            hours_needed += math.ceil(payload / batch_size)
            
        return hours_needed <= time_limit

    def find_minimum_batch_size(self, payloads: list[int], time_limit: int) -> int:
        """
        Uses Binary Search on the Answer Space to find the minimum required batch size.
        Time Complexity: O(N * log(MAX_P)) where N is len(payloads) and MAX_P is the max payload.
        Space Complexity: O(1)
        """
        # The absolute minimum batch size is 1 item per hour
        low = 1 
        
        # The absolute maximum batch size we would ever need is the size of the largest single payload
        high = max(payloads) 
        
        optimal_batch_size = high
        
        while low <= high:
            mid = (low + high) // 2
            
            # If this batch size works, we record it, but check if we can go even smaller
            if self._can_process_in_time(payloads, mid, time_limit):
                optimal_batch_size = mid
                high = mid - 1 # Discard the larger half of the answer space
            else:
                # If it's too slow, we MUST increase the batch size
                low = mid + 1 # Discard the smaller half of the answer space
                
        return optimal_batch_size


# --- Quick Test ---
if __name__ == "__main__":
    print("⚙️ Booting Infrastructure Capacity Optimizer...")
    optimizer = MLInfrastructureOptimizer()
    
    # Simulating a queue of inference jobs (e.g., number of tokens per document)
    inference_queue = [3000, 6000, 7000, 11000] 
    
    # The strict SLA: All documents must be processed within exactly 8 server hours
    SLA_HOURS = 8
    
    print(f"📥 Inference Queue Sizes: {inference_queue}")
    print(f"⏱️ Strict Processing Deadline: {SLA_HOURS} hours")
    
    min_batch = optimizer.find_minimum_batch_size(inference_queue, SLA_HOURS)
    
    print(f"\n✅ Optimization Complete!")
    print(f"📉 Absolute Minimum Safe Batch Size: {min_batch} items/hour")