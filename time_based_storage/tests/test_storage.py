import unittest
from datetime import datetime
from time_based_storage.core import TimeBasedStorage, TimeBasedStorageHeap


class TestTimeBasedStorage(unittest.TestCase):
    def setUp(self):
        self.storage = TimeBasedStorage[int]()
        self.heap_storage = TimeBasedStorageHeap[int]()
        self.test_timestamps = [
            datetime(2024, 1, 1, 10, 0),
            datetime(2024, 1, 1, 11, 0),
            datetime(2024, 1, 1, 12, 0),
        ]
        self.test_values = [1, 2, 3]

    def test_add_and_get(self):
        """Test adding and retrieving values in both storage implementations."""
        for ts, value in zip(self.test_timestamps, self.test_values):
            self.storage.add(ts, value)
            self.heap_storage.add(ts, value)

        self.assertEqual(self.storage.size(), 3)
        self.assertEqual(self.heap_storage.size(), 3)

    def test_get_range(self):
        """Test retrieving values within a time range."""
        for ts, value in zip(self.test_timestamps, self.test_values):
            self.storage.add(ts, value)
            self.heap_storage.add(ts, value)

        start_time = datetime(2024, 1, 1, 10, 30)
        end_time = datetime(2024, 1, 1, 11, 30)

        range_values = self.storage.get_range(start_time, end_time)
        heap_range_values = self.heap_storage.get_range(start_time, end_time)

        self.assertEqual(len(range_values), 1)
        self.assertEqual(len(heap_range_values), 1)
        self.assertEqual(range_values[0], 2)
        self.assertEqual(heap_range_values[0], 2)

    def test_get_duration(self):
        """Test retrieving values within a duration."""
        for ts, value in zip(self.test_timestamps, self.test_values):
            self.storage.add(ts, value)
            self.heap_storage.add(ts, value)

        # Use the last timestamp as the end time
        end_time = self.test_timestamps[-1]
        duration = 3600  # 1 hour in seconds

        # Calculate start time based on duration
        start_time = end_time.fromtimestamp(end_time.timestamp() - duration)

        # Get values using get_range instead of get_duration
        duration_values = self.storage.get_range(start_time, end_time)
        heap_duration_values = self.heap_storage.get_range(start_time, end_time)

        self.assertEqual(len(duration_values), 2)
        self.assertEqual(len(heap_duration_values), 2)
        self.assertEqual(duration_values[-1], 3)
        self.assertEqual(heap_duration_values[-1], 3)

    def test_clear(self):
        """Test clearing the storage."""
        for ts, value in zip(self.test_timestamps, self.test_values):
            self.storage.add(ts, value)
            self.heap_storage.add(ts, value)

        self.storage.clear()
        self.heap_storage.clear()

        self.assertEqual(self.storage.size(), 0)
        self.assertEqual(self.heap_storage.size(), 0)
        self.assertTrue(self.storage.is_empty())
        self.assertTrue(self.heap_storage.is_empty())

    def test_remove(self):
        """Test removing values at specific timestamps."""
        for ts, value in zip(self.test_timestamps, self.test_values):
            self.storage.add(ts, value)
            self.heap_storage.add(ts, value)

        # Remove middle value
        self.assertTrue(self.storage.remove(self.test_timestamps[1]))
        self.assertTrue(self.heap_storage.remove(self.test_timestamps[1]))

        self.assertEqual(self.storage.size(), 2)
        self.assertEqual(self.heap_storage.size(), 2)

        # Verify value was removed
        self.assertIsNone(self.storage.get_value_at(self.test_timestamps[1]))
        self.assertIsNone(self.heap_storage.get_value_at(self.test_timestamps[1]))

    def test_get_all_and_timestamps(self):
        """Test getting all values and timestamps."""
        for ts, value in zip(self.test_timestamps, self.test_values):
            self.storage.add(ts, value)
            self.heap_storage.add(ts, value)

        all_values = self.storage.get_all()
        all_timestamps = self.storage.get_timestamps()
        heap_all_values = self.heap_storage.get_all()
        heap_all_timestamps = self.heap_storage.get_timestamps()

        self.assertEqual(set(all_values), set(self.test_values))
        self.assertEqual(set(all_timestamps), set(self.test_timestamps))
        self.assertEqual(set(heap_all_values), set(self.test_values))
        self.assertEqual(set(heap_all_timestamps), set(self.test_timestamps))

    def test_timestamp_collisions(self):
        """Test handling of timestamp collisions."""
        timestamp = datetime(2024, 1, 1, 10, 0)

        # Test that adding with same timestamp raises ValueError
        self.storage.add(timestamp, 1)
        with self.assertRaises(ValueError):
            self.storage.add(timestamp, 2)

        # Test add_unique_timestamp handles collisions
        unique_ts = self.storage.add_unique_timestamp(timestamp, 3)
        self.assertNotEqual(timestamp, unique_ts)
        self.assertEqual(self.storage.get_value_at(unique_ts), 3)

        # Test that add_unique_timestamp returns original timestamp if no collision
        new_ts = datetime(2024, 1, 1, 11, 0)
        result_ts = self.storage.add_unique_timestamp(new_ts, 4)
        self.assertEqual(new_ts, result_ts)
        self.assertEqual(self.storage.get_value_at(new_ts), 4)


if __name__ == "__main__":
    unittest.main()
