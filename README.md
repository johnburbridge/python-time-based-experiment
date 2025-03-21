# Time-Based Storage System

[![CI](https://github.com/johnburbridge/python-time-based-experiment/actions/workflows/ci.yml/badge.svg)](https://github.com/johnburbridge/python-time-based-experiment/actions/workflows/ci.yml)

A Python package providing two implementations of a time-based storage system for managing events with timestamps.

## Features

- Two storage implementations:
  - `TimeBasedStorage`: Uses a sorted list for efficient range queries
  - `TimeBasedStorageHeap`: Uses a heap for efficient insertion and earliest event access
- Support for:
  - Event creation and deletion
  - Range queries
  - Duration-based queries
  - Day-of-week queries
  - Earliest/latest event access

## Installation

```bash
pip install time_based_storage
```

## Usage

```python
from datetime import datetime, timedelta
from time_based_storage import TimeBasedStorage, TimeBasedStorageHeap, Event

# Create storage instances
storage = TimeBasedStorage()
heap_storage = TimeBasedStorageHeap()

# Create events
event1 = Event(timestamp=datetime(2024, 1, 1, 10, 0), data="Event 1")
event2 = Event(timestamp=datetime(2024, 1, 1, 11, 0), data="Event 2")

# Add events
storage.create_event(event1.timestamp, event1.data)
heap_storage.create_event(event1.timestamp, event1.data)

# Query events
start_time = datetime(2024, 1, 1, 10, 30)
end_time = datetime(2024, 1, 1, 11, 30)
events_in_range = storage.get_events_in_range(start_time, end_time)

# Get events within duration
duration = timedelta(hours=1)
recent_events = storage.get_events_by_duration(duration)

# Get events by day of week (0 = Monday, 6 = Sunday)
monday_events = storage.get_events_by_day_of_week(0)

# Get earliest/latest events
earliest = heap_storage.get_earliest_event()
latest = storage.get_latest_event()
```

## Performance Characteristics

### TimeBasedStorage
- Insertion: O(n)
- Range Queries: O(log n)
- Duration Queries: O(log n)
- Earliest/Latest: O(1)

### TimeBasedStorageHeap
- Insertion: O(log n)
- Range Queries: O(n log n)
- Duration Queries: O(n log n)
- Earliest Event: O(1)
- Latest Event: O(n log n)

## Testing

Run the test suite:

```bash
python -m unittest time_based_storage/tests/test_storage.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 