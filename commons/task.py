import datetime
from dataclasses import dataclass, field

from .task_status import TaskStatus


@dataclass
class Task:
    """
    A class representing a Task with an ID, description, status, and timestamps.

    Attributes:
        id (int): The unique identifier for the task.
        description (str): A brief description of the task.
        status (TaskStatus): The current status of the task, represented by a TaskStatus enum.
        created_at (datetime.datetime): The timestamp when the task was created, defaults to the current time.
        updated_at (datetime.datetime): The timestamp when the task was last updated, defaults to the current time.

    Methods:
        __str__(): Returns a string representation of the task with its ID, description, and status.
        display_details(): Returns a detailed string representation of the task including timestamps.
    """
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
