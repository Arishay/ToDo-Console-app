"""In-memory storage implementation for tasks."""

from src.models.task import Task


class InMemoryStorage:
    """In-memory storage for tasks using a dictionary.

    Provides O(1) lookup, update, and delete operations by task ID.
    """

    def __init__(self) -> None:
        """Initialize empty storage with auto-incrementing ID counter."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task: Task) -> int:
        """Add a task to storage with auto-generated ID.

        Args:
            task: Task to add (ID will be assigned)

        Returns:
            The auto-generated task ID
        """
        task.id = self._next_id
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task.id

    def get_by_id(self, task_id: int) -> Task | None:
        """Retrieve a task by ID.

        Args:
            task_id: The task ID to lookup

        Returns:
            The task if found, None otherwise (O(1) lookup)
        """
        return self._tasks.get(task_id)

    def get_all(self) -> list[Task]:
        """Retrieve all tasks.

        Returns:
            List of all tasks in insertion order
        """
        return list(self._tasks.values())

    def delete(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The task ID to delete

        Returns:
            True if task was deleted, False if not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def update(self, task: Task) -> bool:
        """Update an existing task.

        Args:
            task: The task with updated values (must have valid ID)

        Returns:
            True if task was updated, False if not found
        """
        if task.id in self._tasks:
            self._tasks[task.id] = task
            return True
        return False
