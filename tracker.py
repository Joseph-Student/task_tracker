import datetime
from dataclasses import dataclass, field

from commons import StoreProtocol, Task, TaskStatus


@dataclass
class Tracker:
    """
    A class for managing tasks using an asynchronous interface with a storage backend.

    Attributes:
        store (StoreProtocol): The storage backend for managing task data.
        tasks (list[Task]): A list of tasks currently managed by the tracker.
        _last_id (int): The ID of the last task added, used for generating new task IDs.

    Methods:
        __post_init__(): Initializes the tracker by loading tasks from the store.
        add_task(task_description: str) -> Task: Adds a new task with the given description.
        update_task(task_id: int, description: str) -> Task: Updates the description of an existing task.
        delete_task(task_id: int) -> Task: Deletes a task by its ID.
        list_tasks(status: TaskStatus | None = None) -> list[Task]: Lists tasks, optionally filtered by status.
        change_status(task_id: int, status: TaskStatus) -> Task: Changes the status of a task.
        mark_in_progress(task_id: int) -> Task: Marks a task as in progress.
        mark_done(task_id: int) -> Task: Marks a task as done.
    """
    store: StoreProtocol
    tasks: list[Task] = field(default_factory=list)
    _last_id: int = field(init=False, repr=False)

    def __post_init__(self):
        self.tasks = self.store.load()
        self._last_id = max((task.id for task in self.tasks), default=0)

    async def add_task(self, task_description: str) -> Task:
        new_id = self._last_id + 1
        new_task = Task(
            id=new_id,
            description=task_description,
            status=TaskStatus.TODO
        )
        self.tasks.append(new_task)
        self.store.update_file(self.tasks)
        self._last_id = new_id
        return new_task

    async def update_task(self, task_id: int, description: str) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                task.description = description
                task.updated_at = datetime.datetime.now()
                self.store.update_file(self.tasks)
                return task
        raise ValueError(f"Task with ID {task_id} not found")

    async def delete_task(self, task_id: int) -> Task:
        task_eliminated = next((task for task in self.tasks if task.id == task_id), None)

        if not task_eliminated:
            raise ValueError(f"Task with ID {task_id} not found")
        self.tasks.remove(task_eliminated)
        self.store.update_file(self.tasks)
        return task_eliminated

    async def list_tasks(self, status: TaskStatus | None = None) -> list[Task]:
        if status is None:
            return self.tasks
        return [task for task in self.tasks if task.status == status]

    async def change_status(self, task_id: int, status: TaskStatus) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                task.status = status
                task.updated_at = datetime.datetime.now()
                self.store.update_file(self.tasks)
                return task

    async def mark_in_progress(self, task_id: int) -> Task:
        return await self.change_status(task_id, TaskStatus.IN_PROGRESS)

    async def mark_done(self, task_id: int) -> Task:
        return await self.change_status(task_id, TaskStatus.DONE)
