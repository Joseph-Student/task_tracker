import unittest
from pathlib import Path

from commons.store import StoreJSON
from commons.task import Task
from commons.task_status import TaskStatus
from tracker import Tracker


class TestTracker(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = [
            Task(id=1, description="Task 1", status=TaskStatus.TODO),
            Task(id=2, description="Task 2", status=TaskStatus.IN_PROGRESS),
            Task(id=3, description="Task 3", status=TaskStatus.DONE)
        ]
        self.store = StoreJSON(Path("test_store.json"))
        self.store.update_file(self.tasks)
        self.tracker = Tracker(self.store)

    async def asyncTearDown(self):
        self.store.file_path.unlink(True)
        Path("test_store2.json").unlink(True)

    def test_init_tracker_without_tasks(self):
        store = StoreJSON(Path("test_store2.json"))
        tracker = Tracker(store)
        self.assertEqual(tracker.tasks, [])
        self.assertEqual(tracker._last_id, 0)

    def test_init_tracker_with_tasks(self):
        tracker = Tracker(self.store)
        self.assertEqual(tracker.tasks, self.tasks)
        self.assertEqual(tracker._last_id, 3)

    async def test_add_task(self):
        task = await self.tracker.add_task("Task 4")
        self.assertEqual(task.id, 4)
        self.assertEqual(task.description, "Task 4")
        self.assertEqual(task.status, TaskStatus.TODO)
        self.assertEqual(self.tracker.tasks, self.tasks + [task])

    async def test_update_task(self):
        task = await self.tracker.update_task(2, "Task 2 Updated")
        self.assertEqual(task.description, "Task 2 Updated")
        self.assertEqual(self.tracker.tasks[1], task)
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)
        self.assertNotEqual(task.updated_at, task.created_at)
        self.assertGreater(task.updated_at, task.created_at)

    async def test_delete_task(self):
        task = await self.tracker.delete_task(2)
        self.assertEqual(task.id, 2)
        self.assertEqual(len(self.tracker.tasks), 2)
        for task_ in self.tracker.tasks:
            if task_.id == 2:
                self.fail("Task with ID 2 should not be in the list")

    async def test_list_tasks(self):
        tasks = await self.tracker.list_tasks()
        self.assertEqual(tasks, self.tasks)
        self.assertEqual(len(tasks), 3)

        todo_tasks = await self.tracker.list_tasks(TaskStatus.TODO)
        for todo_task in todo_tasks:
            self.assertEqual(todo_task.status, TaskStatus.TODO)

        in_progress_tasks = await self.tracker.list_tasks(TaskStatus.IN_PROGRESS)
        for in_progress_task in in_progress_tasks:
            self.assertEqual(in_progress_task.status, TaskStatus.IN_PROGRESS)

        done_tasks = await self.tracker.list_tasks(TaskStatus.DONE)
        for done_task in done_tasks:
            self.assertEqual(done_task.status, TaskStatus.DONE)

    async def test_change_status(self):
        task = await self.tracker.change_status(1, TaskStatus.IN_PROGRESS)
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)
        self.assertNotEqual(task.updated_at, task.created_at)
        self.assertGreater(task.updated_at, task.created_at)

    async def test_mark_in_progress(self):
        task = await self.tracker.mark_in_progress(1)
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)
        self.assertNotEqual(task.updated_at, task.created_at)
        self.assertGreater(task.updated_at, task.created_at)

    async def test_mark_done(self):
        task = await self.tracker.mark_done(1)
        self.assertEqual(task.status, TaskStatus.DONE)
        self.assertNotEqual(task.updated_at, task.created_at)
        self.assertGreater(task.updated_at, task.created_at)
