import unittest
from argparse import ArgumentParser
from io import StringIO
from unittest.mock import MagicMock, patch

from command_interface import CommandInterface
from commons import Task, TaskStatus
from tracker import Tracker


class TestCommandInterface(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.parser = ArgumentParser()
        self.task_test = Task(id=1, description="Test task", status=TaskStatus.TODO)
        self.mocker_tracker = MagicMock(spec=Tracker)

    async def asyncTearDown(self):
        del self.mocker_tracker

    # Adding a new task with a description
    async def test_add_task_with_description(self):
        # Arrange
        self.mocker_tracker.add_task.return_value = self.task_test
        command_interface = CommandInterface(parser=self.parser, tracker=self.mocker_tracker)

        # Act
        with patch('sys.argv', ['program', 'add', 'Test task']):
            await command_interface.execute()

        # Assert
        self.mocker_tracker.add_task.assert_called_once_with("Test task")
        self.assertEqual(self.mocker_tracker.add_task.call_count, 1)

    # Updating an existing task's description
    async def test_update_existing_task_description(self):
        # Arrange
        self.mocker_tracker.update_task.return_value = Task(
            id=1,
            description="Updated description",
            status=TaskStatus.TODO
        )
        command_interface = CommandInterface(parser=self.parser, tracker=self.mocker_tracker)

        # Act
        with patch('sys.argv', ['program', 'update', '1', 'Updated description']):
            with patch('command_interface.stdout', new_callable=StringIO) as mock_stdout:
                await command_interface.execute()

        # Assert
        self.mocker_tracker.update_task.assert_called_once_with(1, "Updated description")
        self.assertIn("Task (ID: 1) updated successfully", mock_stdout.getvalue())

    # Deleting an existing task
    async def test_delete_existing_task(self):
        # Arrange
        self.mocker_tracker.delete_task.return_value = Task(id=1, description="Task to delete", status=TaskStatus.TODO)
        command_interface = CommandInterface(parser=self.parser, tracker=self.mocker_tracker)

        # Act
        with patch('sys.argv', ['program', 'delete', '1']):
            with patch('command_interface.stdout', new_callable=StringIO) as mock_stdout:
                await command_interface.execute()

        # Assert
        self.mocker_tracker.delete_task.assert_called_once_with(1)
        self.assertIn("Task (ID: 1) deleted successfully", mock_stdout.getvalue())

    # Listing all tasks
    async def test_list_all_tasks(self):
        # Arrange
        task1 = Task(id=1, description="Task 1", status=TaskStatus.TODO)
        task2 = Task(id=2, description="Task 2", status=TaskStatus.IN_PROGRESS)
        self.mocker_tracker.list_tasks.return_value = [task1, task2]
        command_interface = CommandInterface(parser=self.parser, tracker=self.mocker_tracker)

        # Act
        with patch('sys.argv', ['program', 'list']):
            with patch('command_interface.stdout', new_callable=StringIO) as mock_stdout:
                await command_interface.execute()

        # Assert
        self.mocker_tracker.list_tasks.assert_called_once_with(None)
        self.assertIn("Task ID: 1", mock_stdout.getvalue())
        self.assertIn("Task ID: 2", mock_stdout.getvalue())

    # Listing tasks filtered by status
    async def test_list_tasks_filtered_by_status(self):
        # Arrange
        task = Task(id=1, description="Task 1", status=TaskStatus.TODO)
        self.mocker_tracker.list_tasks.return_value = [task]
        command_interface = CommandInterface(parser=self.parser, tracker=self.mocker_tracker)

        # Act
        with patch('sys.argv', ['program', 'list', 'todo']):
            with patch('command_interface.stdout', new_callable=StringIO) as mock_stdout:
                await command_interface.execute()

        # Assert
        self.mocker_tracker.list_tasks.assert_called_once_with('todo')
        self.assertIn("Task ID: 1", mock_stdout.getvalue())
        self.assertIn("Status: todo", mock_stdout.getvalue())

    # Updating a non-existent task ID
    async def test_update_nonexistent_task(self):
        # Arrange
        self.mocker_tracker.update_task.side_effect = ValueError("Task with ID 999 not found")
        command_interface = CommandInterface(parser=self.parser, tracker=self.mocker_tracker)

        # Act
        with patch('sys.argv', ['program', 'update', '999', 'Updated description']):
            with patch('command_interface.stderr', new_callable=StringIO) as mock_stderr:
                await command_interface.execute()

        # Assert
        self.mocker_tracker.update_task.assert_called_once_with(999, "Updated description")
        self.assertIn("Task (ID: 999) not found", mock_stderr.getvalue())

    # Deleting a non-existent task ID
    async def test_delete_nonexistent_task(self):
        # Arrange
        self.mocker_tracker.delete_task.side_effect = ValueError("Task with ID 999 not found")
        command_interface = CommandInterface(parser=self.parser, tracker=self.mocker_tracker)

        # Act
        with patch('sys.argv', ['program', 'delete', '999']):
            with patch('command_interface.stderr', new_callable=StringIO) as mock_stderr:
                await command_interface.execute()

        # Assert
        self.mocker_tracker.delete_task.assert_called_once_with(999)
        self.assertIn("Task (ID: 999) not found", mock_stderr.getvalue())

    # Marking a non-existent task as in-progress
    async def test_mark_nonexistent_task_in_progress(self):
        # Arrange
        self.mocker_tracker.mark_in_progress.side_effect = ValueError("Task with ID 999 not found")
        command_interface = CommandInterface(parser=self.parser, tracker=self.mocker_tracker)

        # Act
        with patch('sys.argv', ['program', 'mark-in-progress', '999']):
            with patch('command_interface.stderr', new_callable=StringIO) as mock_stderr:
                await command_interface.execute()

        # Assert
        self.mocker_tracker.mark_in_progress.assert_called_once_with(999)
        self.assertIn("Task (ID: 999) not found", mock_stderr.getvalue())

    # Marking a non-existent task as done
    async def test_mark_nonexistent_task_done(self):
        # Arrange
        self.mocker_tracker.mark_done.side_effect = ValueError("Task with ID 999 not found")
        command_interface = CommandInterface(parser=self.parser, tracker=self.mocker_tracker)

        # Act
        with patch('sys.argv', ['program', 'mark-done', '999']):
            with patch('command_interface.stderr', new_callable=StringIO) as mock_stderr:
                await command_interface.execute()

        # Assert
        self.mocker_tracker.mark_done.assert_called_once_with(999)
        self.assertIn("Task (ID: 999) not found", mock_stderr.getvalue())

    # Listing tasks when no tasks exist
    async def test_list_empty_tasks(self):
        # Arrange
        self.mocker_tracker.list_tasks.return_value = []
        command_interface = CommandInterface(parser=self.parser, tracker=self.mocker_tracker)

        # Act
        with patch('sys.argv', ['program', 'list']):
            with patch('command_interface.stderr', new_callable=StringIO) as mock_stderr:
                await command_interface.execute()

        # Assert
        self.mocker_tracker.list_tasks.assert_called_once_with(None)
        self.assertIn("No tasks found", mock_stderr.getvalue())
