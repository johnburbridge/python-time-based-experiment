import time
import random
import psutil
import os
from datetime import datetime, timedelta
from time_based_storage import TimeBasedStorage, TimeBasedStorageHeap

def generate_random_events(num_events: int) -> list:
    """Generate a list of random events for testing."""
    base_time = datetime.now()
    events = []
    for i in range(num_events):
        # Generate random time within the last 24 hours with microsecond precision
        random_hours = random.uniform(0, 24)
        random_minutes = random.uniform(0, 60)
        random_seconds = random.uniform(0, 60)
        random_microseconds = random.randint(0, 1000000)
        timestamp = base_time - timedelta(
            hours=random_hours,
            minutes=random_minutes,
            seconds=random_seconds,
            microseconds=random_microseconds
        )
        events.append((timestamp, i))
    return events

def get_memory_usage():
    """Get current memory usage of the process."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # Convert to MB

def benchmark_insertion(storage: TimeBasedStorage, heap_storage: TimeBasedStorageHeap, num_events: int):
    """Benchmark event insertion performance."""
    events = generate_random_events(num_events)
    
    # Test TimeBasedStorage
    start_time = time.time()
    for timestamp, value in events:
        storage.add(timestamp, value)
    storage_time = time.time() - start_time
    
    # Test TimeBasedStorageHeap
    start_time = time.time()
    for timestamp, value in events:
        heap_storage.add(timestamp, value)
    heap_time = time.time() - start_time
    
    return storage_time, heap_time

def benchmark_range_queries(storage: TimeBasedStorage, heap_storage: TimeBasedStorageHeap, num_queries: int):
    """Benchmark range query performance."""
    # Generate random time ranges
    ranges = []
    for _ in range(num_queries):
        start = datetime.now() - timedelta(hours=random.uniform(0, 24))
        end = start + timedelta(hours=random.uniform(1, 12))
        ranges.append((start, end))
    
    # Test TimeBasedStorage
    start_time = time.time()
    for start, end in ranges:
        storage.get_range(start, end)
    storage_time = time.time() - start_time
    
    # Test TimeBasedStorageHeap
    start_time = time.time()
    for start, end in ranges:
        heap_storage.get_range(start, end)
    heap_time = time.time() - start_time
    
    return storage_time, heap_time

def benchmark_duration_queries(storage: TimeBasedStorage, heap_storage: TimeBasedStorageHeap, num_queries: int):
    """Benchmark duration query performance."""
    # Generate random durations
    durations = [3600 * random.uniform(1, 24) for _ in range(num_queries)]  # Duration in seconds
    
    # Test TimeBasedStorage
    start_time = time.time()
    for duration in durations:
        storage.get_duration(duration)
    storage_time = time.time() - start_time
    
    # Test TimeBasedStorageHeap
    start_time = time.time()
    for duration in durations:
        heap_storage.get_duration(duration)
    heap_time = time.time() - start_time
    
    return storage_time, heap_time

def benchmark_earliest_latest(storage: TimeBasedStorage, heap_storage: TimeBasedStorageHeap, num_queries: int):
    """Benchmark earliest/latest event retrieval performance."""
    # Test TimeBasedStorage
    start_time = time.time()
    for _ in range(num_queries):
        storage.get_all()  # Get all values to simulate latest event access
    storage_time = time.time() - start_time
    
    # Test TimeBasedStorageHeap
    start_time = time.time()
    for _ in range(num_queries):
        heap_storage.get_all()  # Get all values to simulate earliest/latest event access
    heap_time = time.time() - start_time
    
    return storage_time, heap_time

def benchmark_timestamp_collisions(storage: TimeBasedStorage, num_events: int):
    """Benchmark handling of timestamp collisions."""
    base_time = datetime.now()
    collisions = 0
    start_time = time.time()
    
    for i in range(num_events):
        try:
            storage.add(base_time, i)
        except ValueError:
            collisions += 1
    
    end_time = time.time()
    return end_time - start_time, collisions

def main():
    """Run all benchmarks with different dataset sizes."""
    sizes = [1000, 10000, 100000, 1000000]
    num_queries = 1000
    
    print("Starting benchmarks...")
    print("-" * 80)
    
    for size in sizes:
        print(f"\nDataset size: {size:,} events")
        print("-" * 40)
        
        # Initialize storage systems
        storage = TimeBasedStorage[int]()
        heap_storage = TimeBasedStorageHeap[int]()
        
        # Run benchmarks
        print("Running insertion benchmark...")
        storage_insert, heap_insert = benchmark_insertion(storage, heap_storage, size)
        
        print("Running range queries benchmark...")
        storage_range, heap_range = benchmark_range_queries(storage, heap_storage, num_queries)
        
        print("Running duration queries benchmark...")
        storage_duration, heap_duration = benchmark_duration_queries(storage, heap_storage, num_queries)
        
        print("Running earliest/latest benchmark...")
        storage_earliest, heap_earliest = benchmark_earliest_latest(storage, heap_storage, num_queries)
        
        print("Running timestamp collision benchmark...")
        collision_time, collisions = benchmark_timestamp_collisions(TimeBasedStorage[int](), size)
        
        # Get memory usage
        memory_usage = get_memory_usage()
        
        # Print results
        print("\nResults:")
        print(f"Insertion: TimeBasedStorage ({storage_insert:.4f}s) vs TimeBasedStorageHeap ({heap_insert:.4f}s)")
        print(f"Range Queries: TimeBasedStorage ({storage_range:.4f}s) vs TimeBasedStorageHeap ({heap_range:.4f}s)")
        print(f"Duration Queries: TimeBasedStorage ({storage_duration:.4f}s) vs TimeBasedStorageHeap ({heap_duration:.4f}s)")
        print(f"Earliest/Latest: TimeBasedStorage ({storage_earliest:.4f}s) vs TimeBasedStorageHeap ({heap_earliest:.4f}s)")
        print(f"Timestamp Collisions: {collisions:,} collisions in {collision_time:.4f}s")
        print(f"Memory Usage: {memory_usage:.2f}MB")
        
        print("-" * 40)
    
    print("\nBenchmark completed successfully!")

if __name__ == "__main__":
    main() 