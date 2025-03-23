#!/usr/bin/env python3
"""
Simple example demonstrating the Red-Black Tree implementation for time-based storage.
This example shows the basic usage and advantages of the RB-Tree implementation.
"""

from datetime import datetime, timedelta
from time_based_storage import (
    TimeBasedStorage,
    TimeBasedStorageRBTree,
    ThreadSafeTimeBasedStorageRBTree
)


def basic_example():
    """Demonstrates basic usage of the RB-Tree implementation."""
    print("Basic RB-Tree implementation example")
    print("====================================")
    
    # Create RB-Tree storage instance
    storage = TimeBasedStorageRBTree[str]()
    
    # Add some events
    now = datetime.now()
    storage.add(now - timedelta(minutes=30), "Event from 30 minutes ago")
    storage.add(now - timedelta(minutes=20), "Event from 20 minutes ago")
    storage.add(now - timedelta(minutes=10), "Event from 10 minutes ago")
    storage.add(now, "Current event")
    
    print(f"Total events: {storage.size()}")
    
    # Retrieve events in a time range
    start = now - timedelta(minutes=25)
    end = now - timedelta(minutes=5)
    range_events = storage.get_range(start, end)
    
    print("\nEvents between 25 and 5 minutes ago:")
    for event in range_events:
        print(f"- {event}")
    
    # Get most recent events (last 15 minutes)
    recent_events = storage.get_duration(15 * 60)  # 15 minutes in seconds
    
    print("\nEvents in the last 15 minutes:")
    for event in recent_events:
        print(f"- {event}")


def thread_safe_example():
    """Demonstrates the thread-safe RB-Tree implementation."""
    print("\nThread-safe RB-Tree implementation")
    print("=================================")
    
    # Create thread-safe storage
    storage = ThreadSafeTimeBasedStorageRBTree[str]()
    
    # Add some events
    now = datetime.now()
    storage.add(now - timedelta(minutes=5), "Event A")
    storage.add(now - timedelta(minutes=3), "Event B")
    storage.add(now - timedelta(minutes=1), "Event C")
    
    print(f"Total events: {storage.size()}")
    print("All events:")
    for event in storage.get_all():
        print(f"- {event}")


def collision_handling_example():
    """Demonstrates timestamp collision handling with the RB-Tree implementation."""
    print("\nTimestamp collision handling with RB-Tree")
    print("=======================================")
    
    storage = TimeBasedStorageRBTree[str]()
    
    # Create a timestamp
    now = datetime.now()
    
    # Add first event
    storage.add(now, "First event")
    print("First event added successfully")
    
    # Handle collision with add_unique_timestamp
    modified_ts = storage.add_unique_timestamp(now, "Second event")
    print(f"Second event added with modified timestamp (offset: {(modified_ts - now).microseconds} microseconds)")
    
    # Add a third event with the same base timestamp
    modified_ts2 = storage.add_unique_timestamp(now, "Third event")
    print(f"Third event added with modified timestamp (offset: {(modified_ts2 - now).microseconds} microseconds)")
    
    # Verify all events are stored
    print(f"\nTotal events: {storage.size()}")
    for event in storage.get_all():
        print(f"- {event}")


if __name__ == "__main__":
    basic_example()
    thread_safe_example()
    collision_handling_example() 