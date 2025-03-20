from datetime import datetime
from typing import TypeVar, Generic, Optional
from dataclasses import dataclass
from functools import total_ordering

T = TypeVar('T')

@dataclass(kw_only=True)
@total_ordering
class Event(Generic[T]):
    """Represents a time-based event with a timestamp and associated data."""
    timestamp: datetime
    data: Optional[T] = None

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