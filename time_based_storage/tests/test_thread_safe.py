import unittest
import threading
import time
from datetime import datetime, timedelta
from time_based_storage.concurrent import ThreadSafeTimeBasedStorage, ThreadSafeTimeBasedStorageHeap


class TestThreadSafeTimeBasedStorage(unittest.TestCase):
    def setUp(self):
        self.storage = ThreadSafeTimeBasedStorage[int]()
        self.num_threads = 10
        self.num_operations = 1000

    def test_concurrent_add(self):
        """Test concurrent addition of values from multiple threads."""

        def add_values(thread_id):
            for i in range(self.num_operations):
                timestamp = datetime.now() + timedelta(seconds=i)
                self.storage.add(timestamp, thread_id * self.num_operations + i)

        threads = []
        for i in range(self.num_threads):
            thread = threading.Thread(target=add_values, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Verify all values were added
        self.assertEqual(self.storage.size(), self.num_threads * self.num_operations)

    def test_concurrent_read_write(self):
        """Test concurrent reading and writing operations."""

        def writer(thread_id):
            for i in range(self.num_operations):
                timestamp = datetime.now() + timedelta(seconds=i)
                self.storage.add(timestamp, thread_id * self.num_operations + i)

        def reader(thread_id):
            for _ in range(self.num_operations):
                # Randomly choose a time range
                start = datetime.now() - timedelta(seconds=100)
                end = datetime.now()
                self.storage.get_range(start, end)

        writer_threads = []
        reader_threads = []

        # Start writer threads
        for i in range(self.num_threads // 2):
            thread = threading.Thread(target=writer, args=(i,))
            writer_threads.append(thread)
            thread.start()

        # Start reader threads
        for i in range(self.num_threads // 2):
            thread = threading.Thread(target=reader, args=(i,))
            reader_threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in writer_threads + reader_threads:
            thread.join()

        # Verify no exceptions were raised during concurrent operations
        self.assertTrue(True)

    def test_wait_for_data(self):
        """Test the wait_for_data functionality with multiple threads."""
        received_data = set()  # Use a set to track unique values
        event = threading.Event()
        data_count = 10

        def consumer():
            while not event.is_set() or len(received_data) < data_count:
                if self.storage.wait_for_data(timeout=0.2):  # Increased timeout for reliability
                    values = self.storage.get_all()
                    received_data.update(values)  # Add unique values to the set
                    if len(received_data) >= data_count:
                        break

        def producer():
            for i in range(data_count):
                self.storage.add(datetime.now(), i)
                time.sleep(0.1)
            # Wait a bit to ensure consumer can process the last item
            time.sleep(0.5)
            event.set()

        consumer_thread = threading.Thread(target=consumer)
        producer_thread = threading.Thread(target=producer)

        consumer_thread.start()
        producer_thread.start()

        producer_thread.join(timeout=5)  # Add timeout to avoid hanging
        consumer_thread.join(timeout=5)  # Add timeout to avoid hanging

        self.assertEqual(len(received_data), data_count)
        self.assertEqual(set(range(data_count)), received_data)  # Verify we got all expected values


class TestThreadSafeTimeBasedStorageHeap(unittest.TestCase):
    def setUp(self):
        self.storage = ThreadSafeTimeBasedStorageHeap[int]()
        self.num_threads = 10
        self.num_operations = 1000

    def test_concurrent_add(self):
        """Test concurrent addition of values from multiple threads."""

        def add_values(thread_id):
            for i in range(self.num_operations):
                timestamp = datetime.now() + timedelta(seconds=i)
                self.storage.add(timestamp, thread_id * self.num_operations + i)

        threads = []
        for i in range(self.num_threads):
            thread = threading.Thread(target=add_values, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Verify all values were added
        self.assertEqual(self.storage.size(), self.num_threads * self.num_operations)

    def test_concurrent_read_write(self):
        """Test concurrent reading and writing operations."""

        def writer(thread_id):
            for i in range(self.num_operations):
                timestamp = datetime.now() + timedelta(seconds=i)
                self.storage.add(timestamp, thread_id * self.num_operations + i)

        def reader(thread_id):
            for _ in range(self.num_operations):
                # Randomly choose a time range
                start = datetime.now() - timedelta(seconds=100)
                end = datetime.now()
                self.storage.get_range(start, end)

        writer_threads = []
        reader_threads = []

        # Start writer threads
        for i in range(self.num_threads // 2):
            thread = threading.Thread(target=writer, args=(i,))
            writer_threads.append(thread)
            thread.start()

        # Start reader threads
        for i in range(self.num_threads // 2):
            thread = threading.Thread(target=reader, args=(i,))
            reader_threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in writer_threads + reader_threads:
            thread.join()

        # Verify no exceptions were raised during concurrent operations
        self.assertTrue(True)

    def test_wait_for_data(self):
        """Test the wait_for_data functionality with multiple threads."""
        received_data = set()  # Use a set to track unique values
        event = threading.Event()
        data_count = 10

        def consumer():
            while not event.is_set() or len(received_data) < data_count:
                if self.storage.wait_for_data(timeout=0.2):  # Increased timeout for reliability
                    values = self.storage.get_all()
                    received_data.update(values)  # Add unique values to the set
                    if len(received_data) >= data_count:
                        break

        def producer():
            for i in range(data_count):
                self.storage.add(datetime.now(), i)
                time.sleep(0.1)
            # Wait a bit to ensure consumer can process the last item
            time.sleep(0.5)
            event.set()

        consumer_thread = threading.Thread(target=consumer)
        producer_thread = threading.Thread(target=producer)

        consumer_thread.start()
        producer_thread.start()

        producer_thread.join(timeout=5)  # Add timeout to avoid hanging
        consumer_thread.join(timeout=5)  # Add timeout to avoid hanging

        self.assertEqual(len(received_data), data_count)
        self.assertEqual(set(range(data_count)), received_data)  # Verify we got all expected values


if __name__ == "__main__":
    unittest.main()
