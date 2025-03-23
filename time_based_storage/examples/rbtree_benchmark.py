#!/usr/bin/env python3
"""
Benchmark for comparing performance characteristics of different TimeBasedStorage implementations.
This focuses on comparing the standard dict-based implementation with the Red-Black Tree implementation.

Results will vary based on hardware, but the relative performance differences should be consistent.
"""

import time
import random
from datetime import datetime, timedelta
import statistics
import numpy as np
from time_based_storage import TimeBasedStorage, TimeBasedStorageRBTree

# Number of runs for each benchmark to get more stable results
BENCHMARK_RUNS = 3

def measure_time(func):
    """Measure the execution time of a function."""
    start_time = time.time()
    result = func()
    end_time = time.time()
    return result, end_time - start_time

def benchmark_insertion(n, timestamps, label="random"):
    """Benchmark insertion performance for both implementations."""
    regular_times = []
    rbtree_times = []
    
    print(f"Insertion benchmark ({label}, {n:,} items)...")
    
    for run in range(BENCHMARK_RUNS):
        # Standard implementation
        regular_storage = TimeBasedStorage[str]()
        start_time = time.time()
        for i, ts in enumerate(timestamps):
            regular_storage.add(ts, f"Event {i}")
        regular_time = time.time() - start_time
        regular_times.append(regular_time)
        
        # Red-Black Tree implementation
        rbtree_storage = TimeBasedStorageRBTree[str]()
        start_time = time.time()
        for i, ts in enumerate(timestamps):
            rbtree_storage.add(ts, f"Event {i}")
        rbtree_time = time.time() - start_time
        rbtree_times.append(rbtree_time)
    
    # Calculate average times
    avg_regular = statistics.mean(regular_times)
    avg_rbtree = statistics.mean(rbtree_times)
    
    # Print results
    print(f"  Standard: {avg_regular:.4f} seconds (avg of {BENCHMARK_RUNS} runs)")
    print(f"  RB-Tree:  {avg_rbtree:.4f} seconds (avg of {BENCHMARK_RUNS} runs)")
    
    # Calculate speedup
    speedup = avg_regular / avg_rbtree if avg_rbtree > 0 else float('inf')
    print(f"  Speedup:  {speedup:.2f}x")
    
    return regular_storage, rbtree_storage, avg_regular, avg_rbtree, speedup

def benchmark_range_queries(regular_storage, rbtree_storage, sorted_timestamps, n):
    """Benchmark range query performance for both implementations."""
    print("\nRange query benchmarks...")
    
    # Define range test configurations
    range_configs = [
        ("tiny", 0.0001, "0.01%"),  # 0.01% of data
        ("small", 0.001, "0.1%"),   # 0.1% of data
        ("medium", 0.01, "1%"),     # 1% of data
        ("large", 0.1, "10%"),      # 10% of data
        ("xlarge", 0.5, "50%")      # 50% of data
    ]
    
    results = []
    for range_name, range_size, range_label in range_configs:
        regular_times = []
        rbtree_times = []
        
        # Choose start index for range to be in the middle of the dataset
        start_idx = n // 2 - int(n * range_size) // 2
        end_idx = start_idx + int(n * range_size)
        
        start_time = sorted_timestamps[start_idx]
        end_time = sorted_timestamps[end_idx]
        
        for run in range(BENCHMARK_RUNS):
            # Standard implementation
            start = time.time()
            regular_result = regular_storage.get_range(start_time, end_time)
            regular_times.append(time.time() - start)
            
            # Red-Black Tree implementation
            start = time.time()
            rbtree_result = rbtree_storage.get_range(start_time, end_time)
            rbtree_times.append(time.time() - start)
            
            # Verify results
            assert len(regular_result) == len(rbtree_result), f"Result size mismatch: {len(regular_result)} vs {len(rbtree_result)}"
        
        # Calculate average times
        avg_regular = statistics.mean(regular_times)
        avg_rbtree = statistics.mean(rbtree_times)
        
        # Calculate speedup
        speedup = avg_regular / avg_rbtree if avg_rbtree > 0 else float('inf')
        
        # Store results
        results.append((range_name, range_label, len(regular_result), avg_regular, avg_rbtree, speedup))
        
        # Print results
        print(f"  Range query ({range_label} of data, {len(regular_result):,} items):")
        print(f"    Standard: {avg_regular:.6f} seconds")
        print(f"    RB-Tree:  {avg_rbtree:.6f} seconds")
        print(f"    Speedup:  {speedup:.2f}x")
    
    # Calculate average speedup
    speedups = [r[5] for r in results]
    avg_speedup = statistics.mean(speedups)
    print(f"\nAverage range query speedup: {avg_speedup:.2f}x")
    
    return results

def main():
    """Run the complete benchmark suite."""
    print("Red-Black Tree Time-Based Storage Performance Benchmark\n")
    
    # Number of elements
    n = 100000  # Default to 100K for quick runs
    
    # Check if command line args contain a size parameter
    import sys
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        n = int(sys.argv[1])
    
    print(f"Running benchmarks with {n:,} elements")
    print(f"Averaging results over {BENCHMARK_RUNS} runs for stability\n")
    
    # Generate unique timestamps spread over the last day
    now = datetime.now()
    base_time = now - timedelta(days=1)
    
    # Create unique timestamps with microsecond precision
    timestamps = []
    for i in range(n):
        timestamp = base_time + timedelta(microseconds=i)
        timestamps.append(timestamp)
    
    # Random insertion benchmark
    random.shuffle(timestamps)
    regular_storage, rbtree_storage, _, _, _ = benchmark_insertion(n, timestamps, "random order")
    
    # Sorted insertion benchmark (worst case for regular storage)
    sorted_timestamps = sorted(timestamps)
    benchmark_insertion(n, sorted_timestamps, "sorted order")
    
    # Range query benchmark
    benchmark_range_queries(regular_storage, rbtree_storage, sorted_timestamps, n)
    
    print("\nWhen to use the Red-Black Tree implementation:")
    print("- For large datasets with frequent insertions")
    print("- When data might be inserted in sorted order")
    print("- When range queries are common")
    print("- When balanced performance across operations is needed")

if __name__ == "__main__":
    main() 