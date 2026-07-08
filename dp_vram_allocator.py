# dp_vram_allocator.py

class MLModel:
    def __init__(self, name: str, vram_cost_gb: int, business_value: int):
        self.name = name
        self.vram = vram_cost_gb
        self.value = business_value

def optimize_gpu_allocation(capacity: int, models: list[MLModel]) -> int:
    """
    Solves the 0/1 Knapsack problem to maximize business value under a strict VRAM limit.
    Time Complexity: O(N * W) where N is len(models) and W is capacity.
    Space Complexity: O(W) highly optimized 1D array.
    """
    # dp[w] will store the maximum value achievable with exactly 'w' GB of VRAM
    dp = [0] * (capacity + 1)
    
    # We also want to track WHICH models were chosen, not just the max value.
    # To do this in a 1D array, we maintain a parallel array of selection sets.
    selections = [set() for _ in range(capacity + 1)]
    
    for model in models:
        # We must iterate backward to avoid using the same model multiple times (0/1 constraint)
        for w in range(capacity, model.vram - 1, -1):
            
            # Value if we EXCLUDE this model (just keep whatever we had for this capacity)
            exclude_value = dp[w]
            
            # Value if we INCLUDE this model (value of this model + best value of remaining space)
            include_value = model.value + dp[w - model.vram]
            
            # If including it yields a better total value, update the DP table
            if include_value > exclude_value:
                dp[w] = include_value
                # Update our tracking to include the new model and previous models that fit
                selections[w] = selections[w - model.vram] | {model.name}
                
    return dp[capacity], selections[capacity]


# --- Quick Test ---
if __name__ == "__main__":
    print("🧠 Booting Dynamic Programming VRAM Allocator...")
    
    # Simulating an NVIDIA A10G with 24GB of VRAM
    GPU_VRAM_LIMIT = 24 
    
    # The queue of models waiting to be deployed
    model_queue = [
        MLModel("Fraud_Detection", vram_cost_gb=10, business_value=100),
        MLModel("Realtime_OCR", vram_cost_gb=8, business_value=75),
        MLModel("LLM_Chat_Agent", vram_cost_gb=16, business_value=120),
        MLModel("Recommendation_Engine", vram_cost_gb=6, business_value=50),
        MLModel("Spam_Filter", vram_cost_gb=4, business_value=40)
    ]
    
    print(f"\n📊 Total Models in Queue: {len(model_queue)}")
    print(f"🖥️ Total VRAM Available: {GPU_VRAM_LIMIT} GB")
    
    max_value, optimal_models = optimize_gpu_allocation(GPU_VRAM_LIMIT, model_queue)
    
    print(f"\n✅ Optimal Allocation Found!")
    print(f"💰 Maximum Business Value: {max_value}")
    print(f"📦 Models Loaded into Memory: {optimal_models}")