from typing import List, Optional, TypeVar, Generic, Tuple
from datetime import datetime
import heapq
import bisect

T = TypeVar("T")


class TimeBasedStorageHeap(Generic[T]):
    """
    Heap-based implementation of time-based storage.
    This implementation provides efficient range queries by maintaining a sorted heap of timestamps.
    This is a non-thread-safe implementation suitable for single-threaded use.
    """

    def __init__(self):
        self._heap: List[Tuple[datetime, T]] = []

    def add(self, timestamp: datetime, value: T) -> None:
        """
        Add a value with its timestamp.

        Args:
            timestamp: The timestamp of the value
            value: The value to store

        Raises:
            ValueError: If a value already exists at the given timestamp
        """
        # Check for duplicate timestamp
        if self._heap and self._heap[0][0] == timestamp:
            raise ValueError(f"Value already exists at timestamp {timestamp}")
        heapq.heappush(self._heap, (timestamp, value))

    def get_range(self, start_time: datetime, end_time: datetime) -> List[T]:
        """
        Get all values within a time range.

        Args:
            start_time: Start of the time range
            end_time: End of the time range

        Returns:
            List of values within the specified time range
        """
        # Find the start index using binary search
        start_idx = bisect.bisect_left([ts for ts, _ in self._heap], start_time)
        # Find the end index using binary search
        end_idx = bisect.bisect_right([ts for ts, _ in self._heap], end_time)

        # Return values within the range
        return [value for _, value in self._heap[start_idx:end_idx]]

    def get_duration(self, duration: float) -> List[T]:
        """
        Get all values within the last duration seconds.

        Args:
            duration: Number of seconds to look back

        Returns:
            List of values within the specified duration
        """
        now = datetime.now()
        start_time = now.fromtimestamp(now.timestamp() - duration)
        return self.get_range(start_time, now)

    def get_earliest(self) -> Optional[Tuple[datetime, T]]:
        """
        Get the earliest value in the storage.

        Returns:
            Tuple of (timestamp, value) for the earliest entry, or None if empty
        """
        return self._heap[0] if self._heap else None

    def get_latest(self) -> Optional[Tuple[datetime, T]]:
        """
        Get the latest value in the storage.

        Returns:
            Tuple of (timestamp, value) for the latest entry, or None if empty
        """
        if not self._heap:
            return None
        # Find the latest timestamp using binary search
        latest_idx = bisect.bisect_right([ts for ts, _ in self._heap], datetime.max) - 1
        return self._heap[latest_idx] if latest_idx >= 0 else None

    def get_all(self) -> List[T]:
        """
        Get all stored values.

        Returns:
            List of all stored values
        """
        return [value for _, value in self._heap]

    def get_timestamps(self) -> List[datetime]:
        """
        Get all stored timestamps.

        Returns:
            List of all stored timestamps
        """
        return [ts for ts, _ in self._heap]

    def get_value_at(self, timestamp: datetime) -> Optional[T]:
        """
        Get the value at a specific timestamp.

        Args:
            timestamp: The timestamp to look up

        Returns:
            The value at the specified timestamp, or None if not found
        """
        # Use binary search to find the timestamp
        idx = bisect.bisect_left([ts for ts, _ in self._heap], timestamp)
        if idx < len(self._heap) and self._heap[idx][0] == timestamp:
            return self._heap[idx][1]
        return None

    def remove(self, timestamp: datetime) -> bool:
        """
        Remove a value at a specific timestamp.

        Args:
            timestamp: The timestamp of the value to remove

        Returns:
            True if the value was removed, False if not found
        """
        # Use binary search to find the timestamp
        idx = bisect.bisect_left([ts for ts, _ in self._heap], timestamp)
        if idx < len(self._heap) and self._heap[idx][0] == timestamp:
            # Remove the item at the found index
            self._heap.pop(idx)
            # Reheapify the list
            heapq.heapify(self._heap)
            return True
        return False

    def size(self) -> int:
        """
        Get the number of stored values.

        Returns:
            Number of stored values
        """
        return len(self._heap)

    def is_empty(self) -> bool:
        """
        Check if the storage is empty.

        Returns:
            True if the storage is empty, False otherwise
        """
        return len(self._heap) == 0

    def clear(self) -> None:
        """Clear all values from the storage."""
        self._heap.clear()
