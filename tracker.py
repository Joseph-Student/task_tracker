import datetime
from dataclasses import dataclass, field

from commons.store import StoreProtocol
from commons.task import Task
from commons.task_status import TaskStatus


@dataclass
class Tracker:
    store: StoreProtocol
    tasks: list[Task] = field(default_factory=list)
    _last_id: int = field(init=False, repr=False)

    def __post_init__(self):
        self.tasks = self.store.load()
        self._last_id = self.tasks[-1].id if len(self.tasks) > 0 else 0

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
        task_eliminated: Task | None = None

        for task in self.tasks:
            if task.id == task_id:
                task_eliminated = task

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
