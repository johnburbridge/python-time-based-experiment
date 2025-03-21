# Time-Based Storage System

[![CI](https://github.com/johnburbridge/python-time-based-experiment/actions/workflows/ci.yml/badge.svg)](https://github.com/johnburbridge/python-time-based-experiment/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/johnburbridge/python-time-based-experiment/branch/main/graph/badge.svg)](https://codecov.io/gh/johnburbridge/python-time-based-experiment)

A Python package providing two implementations of a time-based storage system for managing events with timestamps. This library is useful for applications that need to efficiently store and query time-based data, such as event logs, time series data, monitoring systems, and schedulers.

## Features

- Two storage implementations:
  - `TimeBasedStorage`: Uses a sorted list for efficient range queries
  - `TimeBasedStorageHeap`: Uses a heap for efficient insertion and earliest event access
- Thread-safe variants:
  - `ThreadSafeTimeBasedStorage`: Thread-safe version of TimeBasedStorage
  - `ThreadSafeTimeBasedStorageHeap`: Thread-safe version of TimeBasedStorageHeap
- Support for:
  - Event creation and deletion
  - Range queries
  - Duration-based queries
  - Day-of-week queries
  - Earliest/latest event access
  - Timestamp collision handling
  - Generic typing (store any data type)

## Documentation

Comprehensive documentation is available to help you get the most out of this library:

- [**Architecture Guide**](docs/architecture.md) - Design principles, implementation details, and performance considerations
- [**Code Examples**](docs/examples.py) - Practical usage examples and patterns
- [**Concurrent Use Cases**](docs/concurrent_use_cases.md) - Real-world scenarios for concurrent access
- [**Alternative Approaches**](docs/alternatives.md) - Limitations of current implementation and alternative storage strategies

The rest of this README provides an overview of installation, basic usage, and API reference.

## Installation

```bash
pip install time_based_storage
```

## Basic Usage

```python
from datetime import datetime, timedelta
from time_based_storage import TimeBasedStorage, TimeBasedStorageHeap

# Create storage instances
storage = TimeBasedStorage[str]()  # Type annotation for stored values
heap_storage = TimeBasedStorageHeap[str]()

# Add events with timestamps
storage.add(datetime(2024, 1, 1, 10, 0), "Event 1")
storage.add(datetime(2024, 1, 1, 11, 0), "Event 2")
storage.add(datetime(2024, 1, 1, 12, 0), "Event 3")

# Query events in a time range
start_time = datetime(2024, 1, 1, 10, 30)
end_time = datetime(2024, 1, 1, 11, 30)
events_in_range = storage.get_range(start_time, end_time)  # Returns ["Event 2"]

# Query events within a duration (last hour)
duration = 3600  # seconds
recent_events = storage.get_duration(duration)

# Get all events and timestamps
all_events = storage.get_all()
all_timestamps = storage.get_timestamps()

# Remove an event
storage.remove(datetime(2024, 1, 1, 11, 0))  # Removes "Event 2"

# Clear all events
storage.clear()
```

## Thread-Safe Usage

For multithreaded applications, use the thread-safe variants:

```python
from time_based_storage import ThreadSafeTimeBasedStorage, ThreadSafeTimeBasedStorageHeap
import threading

# Create thread-safe storage
storage = ThreadSafeTimeBasedStorage[int]()

# Use in multiple threads
def producer():
    for i in range(10):
        storage.add(datetime.now(), i)
        
def consumer():
    # Wait for data with timeout
    if storage.wait_for_data(timeout=1.0):
        data = storage.get_all()
        print(f"Received: {data}")

# Start threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)
producer_thread.start()
consumer_thread.start()
```

## Choosing the Right Implementation

### TimeBasedStorage
- **Best for**: Applications with frequent range queries or sorted access patterns
- **Advantages**: Efficient range queries, direct index access
- **Trade-offs**: Slower insertion (O(n))

### TimeBasedStorageHeap
- **Best for**: Applications needing fast insertion or frequent access to earliest events
- **Advantages**: Fast insertion, efficient earliest event access
- **Trade-offs**: Less efficient for range queries

## API Reference

### Common Methods (Both Implementations)

| Method | Description | Time Complexity |
|--------|-------------|-----------------|
| `add(timestamp, value)` | Add a value at a specific timestamp | O(n) / O(log n) |
| `get_value_at(timestamp)` | Get value at a specific timestamp | O(1) / O(n) |
| `get_range(start, end)` | Get values in a time range | O(log n) / O(n log n) |
| `get_duration(seconds)` | Get values within a duration | O(log n) / O(n log n) |
| `remove(timestamp)` | Remove value at a timestamp | O(n) / O(log n) |
| `clear()` | Remove all values | O(1) |
| `size()` | Get number of stored events | O(1) |
| `is_empty()` | Check if storage is empty | O(1) |
| `get_all()` | Get all stored values | O(1) |
| `get_timestamps()` | Get all timestamps | O(1) |
| `add_unique_timestamp()` | Add with timestamp collision handling | Varies |

### Thread-Safe Additional Methods

| Method | Description | Notes |
|--------|-------------|-------|
| `wait_for_data(timeout)` | Wait for data to be available | Blocks until data or timeout |
| `notify_data_available()` | Notify waiting threads | Called automatically on add |

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

## Use Cases

This library is well-suited for:

- Event logging and analysis
- Time series data storage
- Monitoring systems
- Event scheduling
- Message queues with time-based priorities
- Session tracking

For more detailed information about using this library in various scenarios, see:

- [**Architecture Guide**](docs/architecture.md) - Learn about the design principles and implementation details
- [**Code Examples**](docs/examples.py) - See practical examples of how to use the library
- [**Concurrent Use Cases**](docs/concurrent_use_cases.md) - Explore real-world concurrent access scenarios
- [**Alternative Approaches**](docs/alternatives.md) - Understand limitations and alternative storage strategies for larger datasets

## Testing

Run the complete test suite:

```bash
# From the project root
cd time_based_storage
python -m pytest tests/ -v
```

Run tests with code coverage:

```bash
cd time_based_storage
python -m pytest tests/ -v --cov=src/time_based_storage --cov-report=html
```

This will generate an HTML coverage report in the `htmlcov` directory.

## Development

### Setup Development Environment

```bash
git clone https://github.com/johnburbridge/python-time-based-experiment.git
cd python-time-based-experiment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e time_based_storage/
pip install -r time_based_storage/requirements-dev.txt
```

### Code Style

This project uses:
- Black for code formatting
- Flake8 for linting

Apply formatting:

```bash
black time_based_storage/src time_based_storage/tests
```

Check style:

```bash
flake8 time_based_storage/src time_based_storage/tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.