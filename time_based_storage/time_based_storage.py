from datetime import datetime, timedelta
from typing import List, Dict, Optional, TypeVar, Generic, override
from dataclasses import dataclass
from bisect import bisect_left, bisect_right
from functools import total_ordering

# T = TypeVar('T')

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
        """Enable comparison for bisect operations."""
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

class TimeBasedStorage:
    """
    A simple time-based storage system that stores events and allows querying by time ranges.
    This implementation uses a sorted list for storage and provides basic CRUD operations.
    Optimized for Python 3.12 with improved bisect operations.
    """
    
    def __init__(self):
        self.events: List[Event] = []

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
        # Use bisect for efficient insertion
        idx = bisect_left(self.events, event)
        self.events.insert(idx, event)

    def delete_event(self, event: Event) -> None:
        """
        Delete an event from the storage.
        
        Args:
            event: The event to delete
            
        Raises:
            ValueError: If the event is not found in storage
        """
        try:
            idx = bisect_left(self.events, event)
            if idx < len(self.events) and self.events[idx] == event:
                self.events.pop(idx)
            else:
                raise ValueError("Event not found in storage")
        except ValueError:
            raise ValueError("Event not found in storage")

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
            
        # Create dummy events for range comparison
        start_event = Event(timestamp=start_time)
        end_event = Event(timestamp=end_time)
        
        # Use bisect for efficient range query
        start_idx = bisect_left(self.events, start_event)
        end_idx = bisect_right(self.events, end_event)
        return self.events[start_idx:end_idx]
    
    def get_latest_event(self) -> Optional[Event]:
        """
        Get the most recent event in the storage.
        
        Returns:
            The most recent event, or None if no events exist
        """
        return self.events[-1] if self.events else None
    
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
            
        cutoff_time = self.events[-1].timestamp - duration
        # Create dummy event for cutoff comparison
        cutoff_event = Event(timestamp=cutoff_time)
        # Use bisect for efficient duration query
        start_idx = bisect_left(self.events, cutoff_event)
        return self.events[start_idx:]

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

# Example usage
def main():
    # Create a storage instance
    storage = TimeBasedStorage()
    
    # Add some sample events
    now = datetime.now()
    storage.create_event(now - timedelta(hours=2), "Event 1")
    storage.create_event(now - timedelta(hours=1), "Event 2")
    storage.create_event(now, "Event 3")
    
    # Query events
    print("Latest event:", storage.get_latest_event())
    print("Events in last hour:", storage.get_events_by_duration(timedelta(hours=1)))
    
    # Query by time range
    start_time = now - timedelta(hours=2)
    end_time = now
    print("Events in range:", storage.get_events_in_range(start_time, end_time))

if __name__ == "__main__":
    main() 