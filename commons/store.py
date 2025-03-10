import datetime
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol

from commons.task import Task
from commons.task_status import TaskStatus


class StoreProtocol(Protocol):
    file_path: Path

    def create_file(self) -> None: ...

    def update_file(self, tasks: list[Task]) -> None: ...

    def load(self) -> list[Task]: ...


@dataclass
class StoreJSON(StoreProtocol):
    file_path: Path

    def __post_init__(self):
        if not self.file_path.exists():
            self.create_file()

    def create_file(self) -> None:
        self.file_path.touch()

    def update_file(self, tasks: list[Task]) -> None:
        self.file_path.write_text(
            json.dumps([self._dump_task(task) for task in tasks]),
            encoding="utf-8"
        )

    def _dump_task(self, task: Task) -> dict:
        response_dict = asdict(task)
        response_dict["created_at"] = task.created_at.isoformat()
        response_dict["updated_at"] = task.updated_at.isoformat()
        response_dict["status"] = task.status.value
        return response_dict

    def _load_task(self, response_dict: dict) -> Task:
        response_dict["created_at"] = datetime.datetime.fromisoformat(response_dict["created_at"])
        response_dict["updated_at"] = datetime.datetime.fromisoformat(response_dict["updated_at"])
        response_dict["status"] = TaskStatus(response_dict["status"])
        return Task(**response_dict)

    def load(self) -> list[Task]:
        text = self.file_path.read_text(encoding="utf-8")
        if not text:
            return []
        return [self._load_task(task) for task in json.loads(text)]
