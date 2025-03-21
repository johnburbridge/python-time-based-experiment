"""
Examples for using the time_based_storage package in various scenarios.
"""

import time
import threading
from datetime import datetime, timedelta
from time_based_storage import (
    TimeBasedStorage,
    TimeBasedStorageHeap,
    ThreadSafeTimeBasedStorage,
    ThreadSafeTimeBasedStorageHeap
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
    """Demonstrate how to handle timestamp collisions."""
    print("\n=== Timestamp Collision Handling ===")
    
    storage = TimeBasedStorage[str]()
    
    # Create a timestamp
    timestamp = datetime(2024, 1, 1, 12, 0, 0)
    
    # Add first event
    storage.add(timestamp, "First event")
    print(f"Added event at {timestamp}")
    
    try:
        # Try to add another event with the same timestamp
        storage.add(timestamp, "Second event")
    except ValueError as e:
        print(f"Error: {e}")
    
    # Use add_unique_timestamp to handle collisions
    unique_timestamp = storage.add_unique_timestamp(timestamp, "Second event")
    print(f"Added with unique timestamp: {unique_timestamp}")
    
    # Get all timestamps
    all_timestamps = storage.get_timestamps()
    print(f"All timestamps: {all_timestamps}")
    
    # Get all values
    all_values = storage.get_all()
    print(f"All values: {all_values}")


def example_thread_safe_storage():
    """Demonstrate usage of thread-safe storage with multiple threads."""
    print("\n=== Thread-Safe Storage ===")
    
    # Create thread-safe storage
    storage = ThreadSafeTimeBasedStorage[int]()
    event = threading.Event()
    
    def producer():
        """Add values to the storage."""
        for i in range(5):
            timestamp = datetime.now()
            storage.add(timestamp, i)
            print(f"Producer: Added {i} at {timestamp}")
            time.sleep(0.5)
        event.set()  # Signal consumer to stop
    
    def consumer():
        """Read values from the storage."""
        while not event.is_set():
            if storage.wait_for_data(timeout=0.2):
                values = storage.get_all()
                timestamps = storage.get_timestamps()
                print(f"Consumer: Current values: {values}")
                print(f"Consumer: Total entries: {len(timestamps)}")
            else:
                print("Consumer: No new data")
    
    # Start threads
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    # Wait for threads to complete
    producer_thread.join()
    consumer_thread.join()


def example_event_monitoring_system():
    """Demonstrate a practical use case: event monitoring system."""
    print("\n=== Event Monitoring System Example ===")
    
    monitor = TimeBasedStorageHeap[dict]()
    
    # Simulate monitoring events with different priorities
    events = [
        {"type": "INFO", "message": "System started", "priority": 1},
        {"type": "WARNING", "message": "High CPU usage", "priority": 2},
        {"type": "ERROR", "message": "Database connection failed", "priority": 3},
        {"type": "INFO", "message": "User logged in", "priority": 1},
        {"type": "CRITICAL", "message": "Out of memory", "priority": 4},
    ]
    
    # Add events with timestamps
    now = datetime.now()
    for i, event in enumerate(events):
        # Simulate events happening at different times
        timestamp = now - timedelta(minutes=10) + timedelta(minutes=i*2)
        monitor.add(timestamp, event)
        
    # Get all events
    all_events = monitor.get_all()
    print("All monitoring events:")
    for event in all_events:
        print(f"- [{event['type']}] {event['message']} (Priority: {event['priority']})")
    
    # Get high priority events (WARNING, ERROR, CRITICAL)
    high_priority = [e for e in all_events if e['priority'] >= 2]
    print("\nHigh priority events:")
    for event in high_priority:
        print(f"- [{event['type']}] {event['message']} (Priority: {event['priority']})")
    
    # Get most recent event (last 2 minutes)
    duration = 2 * 60  # 2 minutes in seconds
    recent = monitor.get_duration(duration)
    print("\nMost recent events (last 2 minutes):")
    for event in recent:
        print(f"- [{event['type']}] {event['message']}") 


if __name__ == "__main__":
    example_basic_usage()
    example_timestamp_collision_handling()
    example_thread_safe_storage()
    example_event_monitoring_system() 