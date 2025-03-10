import unittest
from pathlib import Path

from commons.store import StoreJSON
from commons.task import Task
from commons.task_status import TaskStatus


class TestStoreJSON(unittest.TestCase):
    def setUp(self):
        self.file_test = Path("test_store.json")

    def tearDown(self):
        self.file_test.unlink(missing_ok=True)

    def test_init_store(self):
        self.assertFalse(self.file_test.exists())
        store = StoreJSON(self.file_test)
        self.assertTrue(self.file_test.exists())
        self.assertEqual(store.file_path, self.file_test)

    def test_create_file(self):
        self.assertFalse(self.file_test.exists())
        store = StoreJSON(self.file_test)
        store.create_file()
        self.assertTrue(self.file_test.exists())

    def test_update_file(self):
        tasks = [
            Task(id=1, description="Task 1", status=TaskStatus.TODO),
            Task(id=2, description="Task 2", status=TaskStatus.IN_PROGRESS)
        ]
        store = StoreJSON(self.file_test)
        store.update_file(tasks)
        loaded_tasks = store.load()
        self.assertEqual(loaded_tasks, tasks)

    def test_load(self):
        tasks = [
            Task(id=1, description="Task 1", status=TaskStatus.TODO),
            Task(id=2, description="Task 2", status=TaskStatus.IN_PROGRESS)
        ]
        store = StoreJSON(self.file_test)
        store.update_file(tasks)
        loaded_tasks = store.load()
        self.assertEqual(loaded_tasks, tasks)
