from typing import List, Optional, TypeVar, Generic, Dict
from datetime import datetime, timedelta
import random

T = TypeVar('T')

class TimeBasedStorage(Generic[T]):
    """
    Base class for time-based storage implementations.
    This is a non-thread-safe implementation suitable for single-threaded use.
    
    Note:
        Timestamps have microsecond precision (0.000001 seconds).
        When adding items rapidly, consider using add_unique_timestamp() to avoid collisions.
    """
    
    def __init__(self):
        self._storage: Dict[datetime, T] = {}
    
    def add(self, timestamp: datetime, value: T) -> None:
        """
        Add a value with its timestamp.
        
        Args:
            timestamp: The timestamp of the value
            value: The value to store
            
        Raises:
            ValueError: If a value already exists at the given timestamp
        """
        if timestamp in self._storage:
            raise ValueError(f"Value already exists at timestamp {timestamp}")
        self._storage[timestamp] = value
    
    def add_unique_timestamp(self, timestamp: datetime, value: T, max_offset_microseconds: int = 1000000) -> datetime:
        """
        Add a value with a guaranteed unique timestamp.
        If the timestamp already exists, adds a random microsecond offset.
        
        Args:
            timestamp: The desired timestamp
            value: The value to store
            max_offset_microseconds: Maximum random offset to add (default: 1 second)
            
        Returns:
            The actual timestamp used (may be different from input if offset was added)
        """
        if timestamp not in self._storage:
            self._storage[timestamp] = value
            return timestamp
            
        # Add random offset in microseconds
        offset = random.randint(0, max_offset_microseconds)
        unique_timestamp = timestamp + timedelta(microseconds=offset)
        self._storage[unique_timestamp] = value
        return unique_timestamp
    
    def get_range(self, start_time: datetime, end_time: datetime) -> List[T]:
        """
        Get all values within a time range.
        
        Args:
            start_time: Start of the time range
            end_time: End of the time range
            
        Returns:
            List of values within the specified time range
        """
        return [
            value for ts, value in self._storage.items()
            if start_time <= ts <= end_time
        ]
    
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
    
    def clear(self) -> None:
        """Clear all stored values."""
        self._storage.clear()
    
    def get_all(self) -> List[T]:
        """
        Get all stored values.
        
        Returns:
            List of all stored values
        """
        return list(self._storage.values())
    
    def get_timestamps(self) -> List[datetime]:
        """
        Get all stored timestamps.
        
        Returns:
            List of all stored timestamps
        """
        return list(self._storage.keys())
    
    def get_value_at(self, timestamp: datetime) -> Optional[T]:
        """
        Get the value at a specific timestamp.
        
        Args:
            timestamp: The timestamp to look up
            
        Returns:
            The value at the specified timestamp, or None if not found
        """
        return self._storage.get(timestamp)
    
    def remove(self, timestamp: datetime) -> bool:
        """
        Remove a value at a specific timestamp.
        
        Args:
            timestamp: The timestamp of the value to remove
            
        Returns:
            True if the value was removed, False if not found
        """
        if timestamp in self._storage:
            del self._storage[timestamp]
            return True
        return False
    
    def size(self) -> int:
        """
        Get the number of stored values.
        
        Returns:
            Number of stored values
        """
        return len(self._storage)
    
    def is_empty(self) -> bool:
        """
        Check if the storage is empty.
        
        Returns:
            True if the storage is empty, False otherwise
        """
        return len(self._storage) == 0 