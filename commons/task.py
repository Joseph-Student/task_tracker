import datetime
from dataclasses import dataclass, field

from .task_status import TaskStatus


@dataclass
class Task:
    id: int
    description: str
    status: TaskStatus
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __str__(self):
        return f"Task ID: {self.id}\nDescription: {self.description}\nStatus: {self.status.value}\n\n"

    def display_details(self):
        return f"""
Task ID: {self.id}
Description: {self.description}
Status: {self.status.value}
Created at: {self.created_at}
Updated at: {self.updated_at}
"""
