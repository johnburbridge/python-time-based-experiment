"""
Examples for using the time_based_storage package in various scenarios.
"""

import time
import threading
from datetime import datetime, timedelta
from time_based_storage import (
    TimeBasedStorage,
    TimeBasedStorageHeap,
    TimeBasedStorageRBTree,
    ThreadSafeTimeBasedStorage,
    ThreadSafeTimeBasedStorageHeap,
    ThreadSafeTimeBasedStorageRBTree
)


def example_basic_usage():
    """Demonstrate basic usage of TimeBasedStorage."""
    print("\n=== Basic Usage ===")
    
    # Create a storage instance with string values
    storage = TimeBasedStorage[str]()
    
    # Add events
    now = datetime.now()
    storage.add(now - timedelta(minutes=30), "Event from 30 minutes ago")
    storage.add(now - timedelta(minutes=20), "Event from 20 minutes ago")
    storage.add(now - timedelta(minutes=10), "Event from 10 minutes ago")
    storage.add(now, "Current event")
    
    # Get all events
    print(f"Total events: {storage.size()}")
    all_events = storage.get_all()
    print(f"All events: {all_events}")
    
    # Get range of events
    start_time = now - timedelta(minutes=25)
    end_time = now - timedelta(minutes=5)
    range_events = storage.get_range(start_time, end_time)
    print(f"Events between 25 and 5 minutes ago: {range_events}")
    
    # Get recent events (within last 15 minutes)
    duration = 15 * 60  # 15 minutes in seconds
    recent_events = storage.get_duration(duration)
    print(f"Events in the last 15 minutes: {recent_events}")
    
    # Remove an event
    removal_time = now - timedelta(minutes=20)
    storage.remove(removal_time)
    print(f"After removal, events: {storage.get_all()}")


def example_timestamp_collision_handling():
    """Demonstrate handling of timestamp collisions."""
    print("\n=== Timestamp Collision Handling ===")
    
    storage = TimeBasedStorage[str]()
    
    # Try to add events with identical timestamps
    now = datetime.now()
    
    # First event will succeed
    storage.add(now, "First event")
    print(f"First event added successfully at {now}")
    
    # Second event with same timestamp will fail
    try:
        storage.add(now, "Second event")
        print("Second event added successfully (unexpected)")
    except ValueError as e:
        print(f"Expected error: {e}")
    
    # Use add_unique_timestamp to handle collisions
    actual_timestamp = storage.add_unique_timestamp(now, "Second event")
    print(f"Second event added with modified timestamp: {actual_timestamp}")
    
    # Verify both events are stored
    print(f"Total events: {storage.size()}")
    for event in storage.get_all():
        print(f"- {event}")


def example_thread_safe_storage():
    """Demonstrate thread-safe storage with multiple threads."""
    print("\n=== Thread-Safe Storage ===")
    
    storage = ThreadSafeTimeBasedStorage[str]()
    
    def producer():
        """Add events to the storage."""
        print("Producer: Starting")
        for i in range(5):
            timestamp = datetime.now()
            value = f"Event {i} at {timestamp}"
            storage.add(timestamp, value)
            print(f"Producer: Added {value}")
            time.sleep(0.2)
        print("Producer: Finished")
    
    def consumer():
        """Wait for and retrieve events from storage."""
        print("Consumer: Starting")
        count = 0
        while count < 5:
            # Wait for data with timeout
            if storage.wait_for_data(timeout=1.0):
                data = storage.get_all()
                print(f"Consumer: Received {len(data)} events")
                for event in data:
                    print(f"- {event}")
                count = len(data)
            else:
                print("Consumer: Timeout waiting for data")
        print("Consumer: Finished")
    
    # Start threads
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    # Wait for threads to complete
    producer_thread.join()
    consumer_thread.join()


def example_rbtree_implementation():
    """Demonstrate the Red-Black Tree implementation for time-based storage."""
    print("\n=== Red-Black Tree Implementation ===")
    
    # Create a Red-Black Tree storage instance
    rbtree_storage = TimeBasedStorageRBTree[str]()
    
    # Add events with timestamps
    now = datetime.now()
    for i in range(10):
        timestamp = now - timedelta(minutes=i*10)
        rbtree_storage.add(timestamp, f"Event {i}")
    
    print(f"Total events: {rbtree_storage.size()}")
    
    # Efficient range query
    start_time = now - timedelta(minutes=45)
    end_time = now - timedelta(minutes=15)
    range_events = rbtree_storage.get_range(start_time, end_time)
    print(f"Events between 45 and 15 minutes ago: {range_events}")
    
    # Compare with standard implementation
    std_storage = TimeBasedStorage[str]()
    for i in range(10):
        timestamp = now - timedelta(minutes=i*10)
        std_storage.add(timestamp, f"Event {i}")
    
    # Measure range query performance
    start_time_benchmark = time.time()
    std_result = std_storage.get_range(now - timedelta(minutes=45), now - timedelta(minutes=15))
    std_time = time.time() - start_time_benchmark
    
    start_time_benchmark = time.time()
    rbtree_result = rbtree_storage.get_range(now - timedelta(minutes=45), now - timedelta(minutes=15))
    rbtree_time = time.time() - start_time_benchmark
    
    print("\nRange Query Performance:")
    print(f"Standard: {std_time:.8f} seconds")
    print(f"RB-Tree:  {rbtree_time:.8f} seconds")
    print(f"Speedup:  {std_time/rbtree_time if rbtree_time > 0 else 'inf'}x")
    
    # Verify results match
    print(f"Results match: {sorted(std_result) == sorted(rbtree_result)}")


def example_thread_safe_rbtree():
    """Demonstrate thread-safe Red-Black Tree implementation."""
    print("\n=== Thread-Safe Red-Black Tree Implementation ===")
    
    # Create a thread-safe RB-Tree storage
    storage = ThreadSafeTimeBasedStorageRBTree[str]()
    
    # Create threads to add data concurrently
    def add_data(thread_id, count):
        base_time = datetime.now()
        for i in range(count):
            # Ensure unique timestamps by using microsecond offsets
            timestamp = base_time + timedelta(microseconds=thread_id*1000 + i)
            storage.add(timestamp, f"Thread {thread_id}, Event {i}")
        print(f"Thread {thread_id}: Added {count} events")
    
    # Start multiple threads
    threads = []
    for i in range(5):
        t = threading.Thread(target=add_data, args=(i, 10))
        threads.append(t)
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    # Check storage
    print(f"Total events in storage: {storage.size()}")
    print("Events from Thread 0:")
    for event in storage.get_all():
        if event.startswith("Thread 0"):
            print(f"- {event}")


def example_event_monitoring_system():
    """Demonstrate using time-based storage for a simple event monitoring system."""
    print("\n=== Event Monitoring System Example ===")
    
    # Create storage instances with different implementations
    standard_storage = TimeBasedStorage[dict]()
    heap_storage = TimeBasedStorageHeap[dict]()
    rbtree_storage = TimeBasedStorageRBTree[dict]()
    
    # Generate some sample monitoring events
    now = datetime.now()
    events = [
        {"type": "warning", "message": "CPU usage > 80%", "node": "server1"},
        {"type": "error", "message": "Disk space < 10%", "node": "server2"},
        {"type": "info", "message": "Service restarted", "node": "server3"},
        {"type": "warning", "message": "Memory usage > 90%", "node": "server1"},
        {"type": "critical", "message": "Database connection lost", "node": "server2"},
    ]
    
    # Add events with different timestamps
    for i, event in enumerate(events):
        # Spread events over the last hour
        timestamp = now - timedelta(minutes=i*15)
        standard_storage.add(timestamp, event)
        heap_storage.add(timestamp, event)
        rbtree_storage.add(timestamp, event)
    
    # Query for recent critical/error events (within last 30 minutes)
    recent_events = rbtree_storage.get_duration(30 * 60)  # 30 minutes in seconds
    critical_errors = [event for event in recent_events if event["type"] in ("critical", "error")]
    
    print("Recent critical/error events:")
    for event in critical_errors:
        print(f"- [{event['type']}] {event['message']} ({event['node']})")
    
    # Compare implementation performance for a more realistic dataset size
    print("\nComparing performance with 1000 events...")
    
    # Create new storage instances
    large_standard = TimeBasedStorage[dict]()
    large_heap = TimeBasedStorageHeap[dict]()
    large_rbtree = TimeBasedStorageRBTree[dict]()
    
    # Generate 1000 events with random timestamps in the last 24 hours
    large_events = []
    for i in range(1000):
        random_minutes = i * 1.44  # Spread over 24 hours
        timestamp = now - timedelta(minutes=random_minutes)
        event = {
            "type": ["info", "warning", "error", "critical"][i % 4],
            "message": f"Event {i}",
            "node": f"server{i % 10 + 1}"
        }
        large_events.append((timestamp, event))
    
    # Measure insertion time
    start_time = time.time()
    for timestamp, event in large_events:
        large_standard.add(timestamp, event)
    std_insert_time = time.time() - start_time
    
    start_time = time.time()
    for timestamp, event in large_events:
        large_heap.add(timestamp, event)
    heap_insert_time = time.time() - start_time
    
    start_time = time.time()
    for timestamp, event in large_events:
        large_rbtree.add(timestamp, event)
    rbtree_insert_time = time.time() - start_time
    
    # Measure range query time
    query_start = now - timedelta(hours=12)
    query_end = now - timedelta(hours=6)
    
    start_time = time.time()
    std_range = large_standard.get_range(query_start, query_end)
    std_query_time = time.time() - start_time
    
    start_time = time.time()
    heap_range = large_heap.get_range(query_start, query_end)
    heap_query_time = time.time() - start_time
    
    start_time = time.time()
    rbtree_range = large_rbtree.get_range(query_start, query_end)
    rbtree_query_time = time.time() - start_time
    
    # Print performance results
    print("\nInsertion Time (1000 events):")
    print(f"Standard: {std_insert_time:.6f} seconds")
    print(f"Heap:     {heap_insert_time:.6f} seconds")
    print(f"RB-Tree:  {rbtree_insert_time:.6f} seconds")
    
    print("\nRange Query Time (6-hour range):")
    print(f"Standard: {std_query_time:.6f} seconds for {len(std_range)} events")
    print(f"Heap:     {heap_query_time:.6f} seconds for {len(heap_range)} events")
    print(f"RB-Tree:  {rbtree_query_time:.6f} seconds for {len(rbtree_range)} events")
    
    # Calculate and print speedup
    rb_vs_std_speedup = std_query_time / rbtree_query_time if rbtree_query_time > 0 else float('inf')
    rb_vs_heap_speedup = heap_query_time / rbtree_query_time if rbtree_query_time > 0 else float('inf')
    
    print(f"\nRB-Tree vs Standard speedup: {rb_vs_std_speedup:.2f}x")
    print(f"RB-Tree vs Heap speedup: {rb_vs_heap_speedup:.2f}x")


def run_all_examples():
    """Run all examples in sequence."""
    example_basic_usage()
    example_timestamp_collision_handling()
    example_rbtree_implementation()
    example_thread_safe_storage()
    example_thread_safe_rbtree()
    example_event_monitoring_system()
    
    print("\nAll examples completed successfully!")


if __name__ == "__main__":
    run_all_examples() 