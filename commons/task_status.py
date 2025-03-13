from enum import StrEnum

class TaskStatus(StrEnum):
    """
    An enumeration representing the status of a task.

    Attributes:
        TODO: Indicates that the task is yet to be started.
        IN_PROGRESS: Indicates that the task is currently being worked on.
        DONE: Indicates that the task has been completed.
    """
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"
