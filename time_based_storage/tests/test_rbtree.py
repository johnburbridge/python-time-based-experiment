import unittest
from datetime import datetime, timedelta
import time
import threading
from time_based_storage import (
    TimeBasedStorageRBTree,
    ThreadSafeTimeBasedStorageRBTree,
)


class TestTimeBasedStorageRBTree(unittest.TestCase):
    def setUp(self):
        self.storage = TimeBasedStorageRBTree[str]()
        self.now = datetime.now()

    def test_add_and_get(self):
        self.storage.add(self.now, "test value")
        self.assertEqual(self.storage.get_value_at(self.now), "test value")

    def test_range_query(self):
        # Add some values
        self.storage.add(self.now - timedelta(minutes=10), "value1")
        self.storage.add(self.now - timedelta(minutes=5), "value2")
        self.storage.add(self.now, "value3")
        self.storage.add(self.now + timedelta(minutes=5), "value4")

        # Test range query
        values = self.storage.get_range(self.now - timedelta(minutes=7), self.now + timedelta(minutes=1))
        self.assertEqual(set(values), {"value2", "value3"})

    def test_duplicate_timestamp(self):
        self.storage.add(self.now, "value1")
        with self.assertRaises(ValueError):
            self.storage.add(self.now, "value2")

    def test_add_unique_timestamp(self):
        # Add first value
        ts1 = self.storage.add_unique_timestamp(self.now, "value1")
        self.assertEqual(ts1, self.now)

        # Add second value with same timestamp
        ts2 = self.storage.add_unique_timestamp(self.now, "value2")
        self.assertNotEqual(ts1, ts2)

        # Verify both values are stored
        self.assertEqual(self.storage.size(), 2)

    def test_duration_query(self):
        # Add values with timestamps in the past
        old_time = datetime.now() - timedelta(seconds=10)
        self.storage.add(old_time, "old value")

        # Add recent value
        recent_time = datetime.now() - timedelta(seconds=1)
        self.storage.add(recent_time, "recent value")

        # Get values from last 5 seconds
        values = self.storage.get_duration(5)
        self.assertIn("recent value", values)
        self.assertNotIn("old value", values)


class TestThreadSafeTimeBasedStorageRBTree(unittest.TestCase):
    def setUp(self):
        self.storage = ThreadSafeTimeBasedStorageRBTree[str]()
        self.now = datetime.now()

    def test_concurrent_add(self):
        # Define a function to add values from a thread
        def add_values(start_idx, count):
            for i in range(start_idx, start_idx + count):
                timestamp = self.now + timedelta(microseconds=i)
                self.storage.add(timestamp, f"value{i}")

        # Create and start threads
        threads = []
        for i in range(5):
            t = threading.Thread(target=add_values, args=(i * 100, 100))
            threads.append(t)
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

        # Verify all values were added
        self.assertEqual(self.storage.size(), 500)

    def test_wait_for_data(self):
        # Thread to add data after a delay
        def delayed_add():
            time.sleep(0.1)
            self.storage.add(self.now, "delayed value")

        # Start thread to add data with delay
        t = threading.Thread(target=delayed_add)
        t.start()

        # Wait for data to be available
        result = self.storage.wait_for_data(timeout=1.0)
        t.join()

        # Verify data is available and wait was successful
        self.assertTrue(result)
        self.assertEqual(self.storage.get_value_at(self.now), "delayed value")

    def test_wait_timeout(self):
        # Wait with a short timeout when no data is available
        result = self.storage.wait_for_data(timeout=0.01)

        # Verify wait timed out
        self.assertFalse(result)
        self.assertTrue(self.storage.is_empty())


if __name__ == "__main__":
    unittest.main()
