from datetime import datetime, timedelta
from typing import List, Dict, Optional, TypeVar, Generic, override
from dataclasses import dataclass
import heapq
from operator import attrgetter
from bisect import bisect_left, bisect_right
from functools import total_ordering

#T = TypeVar('T')

@dataclass(kw_only=True)
@total_ordering
class Event[T]:
    """Represents a time-based event with a timestamp and associated data."""
    timestamp: datetime
    data: Optional[T] = None

    def __init__(self, timestamp: datetime, data: Optional[T] = None):
        self.timestamp = timestamp
        self.data = data

    def __post_init__(self):
        """Validate timestamp after initialization."""
        if not isinstance(self.timestamp, datetime):
            raise TypeError(f"timestamp must be datetime, got {type(self.timestamp)}")

    def __lt__(self, other):
        """Enable comparison for heapq and bisect operations."""
        if isinstance(other, datetime):
            return self.timestamp < other
        if isinstance(other, Event):
            return self.timestamp < other.timestamp
        return NotImplemented

    def __eq__(self, other):
        """Enable equality comparison."""
        if isinstance(other, datetime):
            return self.timestamp == other
        if isinstance(other, Event):
            return self.timestamp == other.timestamp and self.data == other.data
        return NotImplemented

class TimeBasedStorageHeap:
    """
    An optimized time-based storage system using heapq for efficient operations.
    This implementation is better suited for large datasets as it maintains
    events in a heap structure, providing O(log n) insertions and O(1) access
    to the earliest event. Optimized for Python 3.12.
    """
    
    def __init__(self):
        self.events: List[Event] = []
        heapq.heapify(self.events)
        # Cache for sorted events to optimize range queries
        self._sorted_cache: Optional[List[Event]] = None
        self._cache_valid: bool = True

    def add_event(self, event: Event) -> None:
        """
        Add a new event to the storage.
        
        Args:
            event: The event to add
        """
        if not isinstance(event, Event):
            raise TypeError("event must be an instance of Event")
        self.create_event(event.timestamp, event.data)

    def create_event(self, timestamp: datetime, data: str) -> None:
        """
        Create and add a new event to the storage.
        
        Args:
            timestamp: The datetime when the event occurred
            data: The data associated with the event
        """
        event = Event(timestamp=timestamp, data=data)
        heapq.heappush(self.events, event)
        self._cache_valid = False

    def delete_event(self, event: Event) -> None:
        """
        Delete an event from the storage.
        
        Args:
            event: The event to delete
            
        Raises:
            ValueError: If the event is not found in storage
        """
        try:
            self.events.remove(event)
            heapq.heapify(self.events)
            self._cache_valid = False
        except ValueError:
            raise ValueError("Event not found in storage")

    def _get_sorted_events(self) -> List[Event]:
        """Get sorted events, using cache if available."""
        if not self._cache_valid:
            self._sorted_cache = sorted(self.events, key=attrgetter('timestamp'))
            self._cache_valid = True
        return self._sorted_cache

    def get_events_in_range(self, start_time: datetime, end_time: datetime) -> List[Event]:
        """
        Retrieve all events that occurred within the specified time range.
        
        Args:
            start_time: The start of the time range
            end_time: The end of the time range
            
        Returns:
            List of events within the specified time range
        """
        if not isinstance(start_time, datetime) or not isinstance(end_time, datetime):
            raise TypeError("start_time and end_time must be datetime objects")
        if start_time > end_time:
            raise ValueError("start_time must be before end_time")
            
        sorted_events = self._get_sorted_events()
        # Create dummy events for range comparison
        start_event = Event(timestamp=start_time)
        end_event = Event(timestamp=end_time)
        # Use bisect for efficient range query
        start_idx = bisect_left(sorted_events, start_event)
        end_idx = bisect_right(sorted_events, end_event)
        return sorted_events[start_idx:end_idx]
    
    def get_latest_event(self) -> Optional[Event]:
        """
        Get the most recent event in the storage.
        
        Returns:
            The most recent event, or None if no events exist
        """
        if not self.events:
            return None
        sorted_events = self._get_sorted_events()
        return sorted_events[-1]
    
    def get_events_by_duration(self, duration: timedelta) -> List[Event]:
        """
        Get all events that occurred within the last specified duration.
        
        Args:
            duration: The time duration to look back
            
        Returns:
            List of events within the specified duration
        """
        if not isinstance(duration, timedelta):
            raise TypeError("duration must be a timedelta object")
            
        if not self.events:
            return []
            
        sorted_events = self._get_sorted_events()
        cutoff_time = sorted_events[-1].timestamp - duration
        # Create dummy event for cutoff comparison
        cutoff_event = Event(timestamp=cutoff_time)
        # Use bisect for efficient duration query
        start_idx = bisect_left(sorted_events, cutoff_event)
        return sorted_events[start_idx:]

    def get_events_by_day_of_week(self, day_of_week: int) -> List[Event]:
        """
        Get all events that occurred on a specific day of the week.
        
        Args:
            day_of_week: The day of the week (0 = Monday, 6 = Sunday)
            
        Returns:
            List of events that occurred on the specified day of the week
            
        Raises:
            ValueError: If day_of_week is not between 0 and 6
        """
        if not 0 <= day_of_week <= 6:
            raise ValueError("day_of_week must be between 0 and 6")
            
        return [event for event in self.events 
                if event.timestamp.weekday() == day_of_week]

    def get_earliest_event(self) -> Optional[Event]:
        """
        Get the earliest event in the storage.
        
        Returns:
            The earliest event, or None if no events exist
        """
        return heapq.nsmallest(1, self.events)[0] if self.events else None

# Example usage
def main():
    # Create a storage instance
    storage = TimeBasedStorageHeap()
    
    # Add some sample events
    now = datetime.now()
    storage.create_event(now - timedelta(hours=2), "Event 1")
    storage.create_event(now - timedelta(hours=1), "Event 2")
    storage.create_event(now, "Event 3")
    
    # Query events
    print("Earliest event:", storage.get_earliest_event())
    print("Latest event:", storage.get_latest_event())
    print("Events in last hour:", storage.get_events_by_duration(timedelta(hours=1)))
    
    # Query by time range
    start_time = now - timedelta(hours=2)
    end_time = now
    print("Events in range:", storage.get_events_in_range(start_time, end_time))

if __name__ == "__main__":
    main() 