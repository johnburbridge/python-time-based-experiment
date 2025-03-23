from typing import List, Optional, TypeVar, Generic
from datetime import datetime
import threading
from ..core import TimeBasedStorageRBTree

T = TypeVar("T")


class ThreadSafeTimeBasedStorageRBTree(TimeBasedStorageRBTree[T], Generic[T]):
    """
    Thread-safe implementation of TimeBasedStorageRBTree using Python's threading module.
    This implementation provides safe concurrent access to the Red-Black Tree storage using read-write locks.
    
    Benefits over the standard ThreadSafeTimeBasedStorage:
    - Better insertion performance: O(log n) vs O(n)
    - Better range query performance: O(log n + k) vs O(n) where k is the number of items in range
    """

    def __init__(self):
        super().__init__()
        # Read-write lock for thread-safe operations
        self._lock = threading.RLock()
        # Condition variable for waiting on events
        self._condition = threading.Condition(self._lock)

    def add(self, timestamp: datetime, value: T) -> None:
        """
        Thread-safe method to add a value with its timestamp.

        Args:
            timestamp: The timestamp of the value
            value: The value to store
        """
        with self._lock:
            super().add(timestamp, value)
            # Notify any waiting threads that new data is available
            self._condition.notify_all()

    def add_unique_timestamp(self, timestamp: datetime, value: T, max_offset_microseconds: int = 1000000) -> datetime:
        """
        Thread-safe method to add a value with a guaranteed unique timestamp.

        Args:
            timestamp: The desired timestamp
            value: The value to store
            max_offset_microseconds: Maximum random offset to add (default: 1 second)

        Returns:
            The actual timestamp used (may be different from input if offset was added)
        """
        with self._lock:
            result = super().add_unique_timestamp(timestamp, value, max_offset_microseconds)
            # Notify any waiting threads that new data is available
            self._condition.notify_all()
            return result

    def get_range(self, start_time: datetime, end_time: datetime) -> List[T]:
        """
        Thread-safe method to get all values within a time range.

        Args:
            start_time: Start of the time range
            end_time: End of the time range

        Returns:
            List of values within the specified time range
        """
        with self._lock:
            return super().get_range(start_time, end_time)

    def get_duration(self, duration: float) -> List[T]:
        """
        Thread-safe method to get all values within the last duration seconds.

        Args:
            duration: Number of seconds to look back

        Returns:
            List of values within the specified duration
        """
        with self._lock:
            return super().get_duration(duration)

    def clear(self) -> None:
        """Thread-safe method to clear all stored values."""
        with self._lock:
            super().clear()

    def get_all(self) -> List[T]:
        """
        Thread-safe method to get all stored values.

        Returns:
            List of all stored values
        """
        with self._lock:
            return super().get_all()

    def get_timestamps(self) -> List[datetime]:
        """
        Thread-safe method to get all stored timestamps.

        Returns:
            List of all stored timestamps
        """
        with self._lock:
            return super().get_timestamps()

    def get_value_at(self, timestamp: datetime) -> Optional[T]:
        """
        Thread-safe method to get the value at a specific timestamp.

        Args:
            timestamp: The timestamp to look up

        Returns:
            The value at the specified timestamp, or None if not found
        """
        with self._lock:
            return super().get_value_at(timestamp)

    def remove(self, timestamp: datetime) -> bool:
        """
        Thread-safe method to remove a value at a specific timestamp.

        Args:
            timestamp: The timestamp of the value to remove

        Returns:
            True if the value was removed, False if not found
        """
        with self._lock:
            return super().remove(timestamp)

    def size(self) -> int:
        """
        Thread-safe method to get the number of stored values.

        Returns:
            Number of stored values
        """
        with self._lock:
            return super().size()

    def is_empty(self) -> bool:
        """
        Thread-safe method to check if the storage is empty.

        Returns:
            True if the storage is empty, False otherwise
        """
        with self._lock:
            return super().is_empty()

    def wait_for_data(self, timeout: float = None) -> bool:
        """
        Wait for data to be available in the storage.

        Args:
            timeout: Maximum time to wait in seconds, or None to wait indefinitely

        Returns:
            True if data is available, False if timeout occurred
        """
        with self._lock:
            if not self.is_empty():
                return True
            return self._condition.wait(timeout=timeout)

    def notify_data_available(self) -> None:
        """
        Notify waiting threads that data is available.
        This is automatically called by add() and add_unique_timestamp().
        """
        with self._lock:
            self._condition.notify_all() 