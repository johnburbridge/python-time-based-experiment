import unittest
from datetime import datetime, timedelta
from time_based_storage import TimeBasedStorage, TimeBasedStorageHeap, Event

class TestTimeBasedStorage(unittest.TestCase):
    def setUp(self):
        self.storage = TimeBasedStorage()
        self.heap_storage = TimeBasedStorageHeap()
        self.test_events = [
            Event(timestamp=datetime(2024, 1, 1, 10, 0), data="Event 1"),
            Event(timestamp=datetime(2024, 1, 1, 11, 0), data="Event 2"),
            Event(timestamp=datetime(2024, 1, 1, 12, 0), data="Event 3"),
        ]

    def test_create_event(self):
        """Test creating events in both storage implementations."""
        for event in self.test_events:
            self.storage.create_event(event.timestamp, event.data)
            self.heap_storage.create_event(event.timestamp, event.data)
        
        self.assertEqual(len(self.storage.events), 3)
        self.assertEqual(len(self.heap_storage._heap), 3)

    def test_get_events_in_range(self):
        """Test retrieving events within a time range."""
        for event in self.test_events:
            self.storage.create_event(event.timestamp, event.data)
            self.heap_storage.create_event(event.timestamp, event.data)
        
        start_time = datetime(2024, 1, 1, 10, 30)
        end_time = datetime(2024, 1, 1, 11, 30)
        
        range_events = self.storage.get_events_in_range(start_time, end_time)
        heap_range_events = self.heap_storage.get_events_in_range(start_time, end_time)
        
        self.assertEqual(len(range_events), 1)
        self.assertEqual(len(heap_range_events), 1)
        self.assertEqual(range_events[0].data, "Event 2")
        self.assertEqual(heap_range_events[0].data, "Event 2")

    def test_get_events_by_duration(self):
        """Test retrieving events within a duration."""
        for event in self.test_events:
            self.storage.create_event(event.timestamp, event.data)
            self.heap_storage.create_event(event.timestamp, event.data)
        
        duration = timedelta(hours=1)
        
        duration_events = self.storage.get_events_by_duration(duration)
        heap_duration_events = self.heap_storage.get_events_by_duration(duration)
        
        self.assertEqual(len(duration_events), 2)
        self.assertEqual(len(heap_duration_events), 2)
        self.assertEqual(duration_events[-1].data, "Event 3")
        self.assertEqual(heap_duration_events[-1].data, "Event 3")

    def test_get_events_by_day_of_week(self):
        """Test retrieving events by day of week."""
        for event in self.test_events:
            self.storage.create_event(event.timestamp, event.data)
            self.heap_storage.create_event(event.timestamp, event.data)
        
        # All events are on Monday (0)
        monday_events = self.storage.get_events_by_day_of_week(0)
        heap_monday_events = self.heap_storage.get_events_by_day_of_week(0)
        
        self.assertEqual(len(monday_events), 3)
        self.assertEqual(len(heap_monday_events), 3)

    def test_delete_event(self):
        """Test deleting events."""
        for event in self.test_events:
            self.storage.create_event(event.timestamp, event.data)
            self.heap_storage.create_event(event.timestamp, event.data)
        
        # Get the event to delete from the storage
        event_to_delete = self.storage.events[1]  # Get the actual event instance from storage
        heap_event_to_delete = self.heap_storage._heap[1]  # Get the actual event instance from heap
        
        self.storage.delete_event(event_to_delete)
        self.heap_storage.delete_event(heap_event_to_delete)
        
        self.assertEqual(len(self.storage.events), 2)
        self.assertEqual(len(self.heap_storage._heap), 2)
        
        # Verify event was deleted
        range_events = self.storage.get_events_in_range(
            event_to_delete.timestamp,
            event_to_delete.timestamp
        )
        heap_range_events = self.heap_storage.get_events_in_range(
            event_to_delete.timestamp,
            event_to_delete.timestamp
        )
        
        self.assertEqual(len(range_events), 0)
        self.assertEqual(len(heap_range_events), 0)

    def test_get_earliest_latest(self):
        """Test getting earliest and latest events."""
        for event in self.test_events:
            self.storage.create_event(event.timestamp, event.data)
            self.heap_storage.create_event(event.timestamp, event.data)
        
        earliest = self.heap_storage.get_earliest_event()
        latest = self.storage.get_latest_event()
        heap_latest = self.heap_storage.get_latest_event()
        
        self.assertEqual(earliest.data, "Event 1")
        self.assertEqual(latest.data, "Event 3")
        self.assertEqual(heap_latest.data, "Event 3")

if __name__ == '__main__':
    unittest.main() 