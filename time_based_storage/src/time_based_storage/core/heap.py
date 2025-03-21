from typing import List, Optional, TypeVar, Generic, Dict, Tuple
from datetime import datetime
import heapq
from .base import TimeBasedStorage

T = TypeVar('T')

class TimeBasedStorageHeap(TimeBasedStorage[T], Generic[T]):
    """
    Heap-based implementation of time-based storage.
    This implementation provides efficient range queries by maintaining a sorted heap of timestamps.
    This is a non-thread-safe implementation suitable for single-threaded use.
    """
    
    def __init__(self):
        super().__init__()
        self._heap: List[Tuple[datetime, T]] = []
    
    def add(self, timestamp: datetime, value: T) -> None:
        """
        Add a value with its timestamp.
        
        Args:
            timestamp: The timestamp of the value
            value: The value to store
        """
        super().add(timestamp, value)
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
        result = []
        heap_copy = self._heap.copy()
        
        while heap_copy:
            ts, value = heapq.heappop(heap_copy)
            if ts > end_time:
                break
            if start_time <= ts <= end_time:
                result.append(value)
        
        return result
    
    def clear(self) -> None:
        """Clear all stored values."""
        super().clear()
        self._heap.clear()
    
    def remove(self, timestamp: datetime) -> bool:
        """
        Remove a value at a specific timestamp.
        
        Args:
            timestamp: The timestamp of the value to remove
            
        Returns:
            True if the value was removed, False if not found
        """
        if super().remove(timestamp):
            # Find and remove the item from the heap
            for i, (ts, _) in enumerate(self._heap):
                if ts == timestamp:
                    self._heap.pop(i)
                    heapq.heapify(self._heap)
                    break
            return True
        return False 