
# Task Tracker CLI

Task Tracker CLI is a task tracker application with a command-line interface for managing tasks.
[Roadmap.sh Project](https://roadmap.sh/projects/task-tracker)


## Installation

Install with poetry

```bash
  poetry install
```
    
## Run Locally

Clone the project

```bash
  git clone https://github.com/devpjoseph/task_tracker
```

Go to the project directory

```bash
  cd task_tracker
```

Install dependencies

```bash
  poetry install
```

Enter to environment
```bash
  poetry run
```


## Usage/Examples

```bash
  python main.py add "Buy groceries"
  # Output: Task added successfully (ID: 1).

  python main.py update 1 "Buy groceries and cook dinner"
  # Output: Task (ID: 1) updated successfully.

  python main.py delete 1
  # Output: Task (ID: 1) deleted successfully.

  python main.py mark-in-progress 1
  # Output: Task (ID: 1) marked as in-progress successfully.

  python main.py mark-done 1
  # Output: Task (ID: 1) marked as done successfully.

  python main.py list
  # Output: 
    Task ID: 1
    Description: Buy groceries
    Status: todo
    Created at: 2025-03-09 22:00:00.000000
    Updated at: 2025-03-09 22:01:00.000000
    .
    .
    .

  python main.py list done
  # Output: 
    Task ID: 2
    Description: Buy groceries and cook dinner
    Status: done
    Created at: 2025-03-09 21:00:00.000000
    Updated at: 2025-03-09 21:01:00.000000
    .
    .
    .

  python main.py list todo
  # Output:
    Task ID: 1
    Description: Buy groceries
    Status: todo
    Created at: 2025-03-09 22:00:00.000000
    Updated at: 2025-03-09 22:01:00.000000
    .
    .
    .

  python main.py list in-progress
  # Output: 
    Task ID: 3
    Description: New task
    Status: in-progress
    Created at: 2025-03-09 20:00:00.000000
    Updated at: 2025-03-09 20:01:00.000000
    .
    .
    .
  
```


## Running Tests

To run tests, run the following command

```bash
  python -m unittest
```


## Authors

- [Joseph Perez](https://github.com/devpjoseph)


## License

[GNU](https://github.com/devpjoseph/task_tracker/blob/main/LICENSE)

