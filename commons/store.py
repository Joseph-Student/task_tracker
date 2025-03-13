import datetime
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol

from .task import Task
from .task_status import TaskStatus


class StoreProtocol(Protocol):
    """
    A protocol defining the interface for a store that manages task data.

    Attributes:
        file_path (Path): The path to the file where tasks are stored.

    Methods:
        create_file() -> None:
            Creates a new file for storing tasks.

        update_file(tasks: list[Task]) -> None:
            Updates the file with the provided list of tasks.

        load() -> list[Task]:
            Loads and returns a list of tasks from the file.
    """
    file_path: Path

    def create_file(self) -> None: ...

    def update_file(self, tasks: list[Task]) -> None: ...

    def load(self) -> list[Task]: ...


@dataclass
class StoreJSON(StoreProtocol):
    """
    A JSON-based implementation of the StoreProtocol for managing task data.

    Attributes:
        file_path (Path): The path to the JSON file where tasks are stored.

    Methods:
        __post_init__(): Initializes the store by creating the file if it doesn't exist.
        create_file() -> None: Creates a new JSON file for storing tasks.
        update_file(tasks: list[Task]) -> None: Updates the JSON file with the provided list of tasks.
        _dump_task(task: Task) -> dict: Converts a Task object into a dictionary suitable for JSON serialization.
        _load_task(response_dict: dict) -> Task: Converts a dictionary back into a Task object.
        load() -> list[Task]: Loads and returns a list of tasks from the JSON file.
    """
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
