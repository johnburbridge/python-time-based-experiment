import time
import random
import sys
import psutil
from datetime import datetime, timedelta
from typing import List, Tuple
from time_based_storage import TimeBasedStorage, Event
from time_based_storage_heap import TimeBasedStorageHeap

def get_memory_usage() -> float:
    """Get current memory usage in MB."""
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024

def generate_random_events(count: int) -> List[Tuple[datetime, str]]:
    """Generate random events for testing."""
    now = datetime.now()
    events = []
    for i in range(count):
        # Generate random time within last 30 days
        random_days = random.uniform(0, 30)
        random_hours = random.uniform(0, 24)
        random_minutes = random.uniform(0, 60)
        timestamp = now - timedelta(days=random_days, hours=random_hours, minutes=random_minutes)
        events.append((timestamp, f"Event {i}"))
    return sorted(events, key=lambda x: x[0])

def benchmark_insertion(events: List[Tuple[datetime, str]], storage_class) -> float:
    """Benchmark event insertion."""
    storage = storage_class()
    start = time.time()
    for timestamp, data in events:
        storage.create_event(timestamp, data)
    return time.time() - start

def benchmark_range_queries(storage, num_queries: int = 1000) -> float:
    """Benchmark range queries."""
    if not storage.events:
        return 0.0
    
    start = time.time()
    for _ in range(num_queries):
        # Generate random time range
        random_days = random.uniform(0, 30)
        random_hours = random.uniform(0, 24)
        end = datetime.now()
        start_dt = end - timedelta(days=random_days, hours=random_hours)
        storage.get_events_in_range(start_dt, end)
    return time.time() - start

def benchmark_duration_queries(storage, num_queries: int = 1000) -> float:
    """Benchmark duration-based queries."""
    if not storage.events:
        return 0.0
    
    start = time.time()
    for _ in range(num_queries):
        # Generate random duration
        random_hours = random.uniform(1, 24)
        duration = timedelta(hours=random_hours)
        storage.get_events_by_duration(duration)
    return time.time() - start

def benchmark_earliest_latest(storage, num_queries: int = 1000) -> float:
    """Benchmark earliest/latest event queries."""
    start = time.time()
    for _ in range(num_queries):
        if isinstance(storage, TimeBasedStorageHeap):
            storage.get_earliest_event()
        storage.get_latest_event()
    return time.time() - start

def run_benchmark(event_counts: List[int] = [1000, 10000, 100000, 1000000]):
    """Run comprehensive benchmark for different dataset sizes."""
    print("\nBenchmark Results:")
    print("=" * 80)
    print(f"{'Dataset Size':<15} {'Operation':<20} {'TimeBasedStorage':<20} {'TimeBasedStorageHeap':<20}")
    print("-" * 80)

    for count in event_counts:
        print(f"\nTesting with {count:,} events:")
        print("-" * 80)
        
        # Generate test data
        events = generate_random_events(count)
        
        # Test insertion
        list_time = benchmark_insertion(events, TimeBasedStorage)
        heap_time = benchmark_insertion(events, TimeBasedStorageHeap)
        print(f"{count:<15} {'Insertion':<20} {list_time:>8.4f}s{'':<12} {heap_time:>8.4f}s")
        
        # Create storage instances for query testing
        list_storage = TimeBasedStorage()
        heap_storage = TimeBasedStorageHeap()
        for timestamp, data in events:
            list_storage.create_event(timestamp, data)
            heap_storage.create_event(timestamp, data)
        
        # Test range queries
        list_time = benchmark_range_queries(list_storage)
        heap_time = benchmark_range_queries(heap_storage)
        print(f"{'':<15} {'Range Queries':<20} {list_time:>8.4f}s{'':<12} {heap_time:>8.4f}s")
        
        # Test duration queries
        list_time = benchmark_duration_queries(list_storage)
        heap_time = benchmark_duration_queries(heap_storage)
        print(f"{'':<15} {'Duration Queries':<20} {list_time:>8.4f}s{'':<12} {heap_time:>8.4f}s")
        
        # Test earliest/latest queries
        list_time = benchmark_earliest_latest(list_storage)
        heap_time = benchmark_earliest_latest(heap_storage)
        print(f"{'':<15} {'Earliest/Latest':<20} {list_time:>8.4f}s{'':<12} {heap_time:>8.4f}s")
        
        # Memory usage
        list_memory = get_memory_usage()
        heap_memory = get_memory_usage()
        print(f"{'':<15} {'Memory Usage':<20} {list_memory:>8.2f}MB{'':<12} {heap_memory:>8.2f}MB")

def main():
    print("Starting Time-Based Storage Benchmark")
    print("=" * 80)
    
    # Test with different dataset sizes
    event_counts = [1000, 10000, 100000, 1000000]
    run_benchmark(event_counts)
    
    print("\nBenchmark completed!")

if __name__ == "__main__":
    main() 