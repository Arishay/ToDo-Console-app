"""Business logic service for todo operations."""

from src.models.task import Task
from src.storage.in_memory_storage import InMemoryStorage


class TodoService:
    """Service layer for todo task management.

    Encapsulates business logic and validation separate from storage and CLI.
    """

    def __init__(self, storage: InMemoryStorage) -> None:
        """Initialize service with storage dependency.

        Args:
            storage: Storage implementation for task persistence
        """
        self._storage = storage

    def add_task(self, title: str, description: str = "") -> tuple[bool, str, int | None]:
        """Add a new task with validation.

        Args:
            title: Task title (required, max 500 characters)
            description: Task description (optional, max 2000 characters)

        Returns:
            Tuple of (success, message, task_id):
            - success: True if task was added, False on validation error
            - message: Success or error message
            - task_id: The new task ID if successful, None on error
        """
        # Validate title
        if not title or not title.strip():
            return (False, "Error: Task title cannot be empty", None)

        title = title.strip()
        if len(title) > 500:
            return (False, "Error: Task title cannot exceed 500 characters", None)

        # Validate description
        description = description.strip()
        if len(description) > 2000:
            return (False, "Error: Task description cannot exceed 2000 characters", None)

        # Create and store task (id will be reassigned by storage)
        task = Task(id=1, title=title, description=description, is_complete=False)
        task_id = self._storage.add(task)

        return (True, f"Task {task_id} added successfully", task_id)

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks from storage.

        Returns:
            List of all tasks in insertion order
        """
        return self._storage.get_all()

    def toggle_complete(self, task_id: int) -> tuple[bool, str]:
        """Toggle a task's completion status.

        Args:
            task_id: ID of task to toggle

        Returns:
            Tuple of (success, message):
            - success: True if toggled, False if task not found
            - message: Success or error message
        """
        # Validate task exists
        task = self._storage.get_by_id(task_id)
        if task is None:
            return (False, f"Error: Task with ID {task_id} not found")

        # Toggle status
        task.is_complete = not task.is_complete
        self._storage.update(task)

        # Return appropriate message
        status = "complete" if task.is_complete else "incomplete"
        return (True, f"Task {task_id} marked as {status}")

    def update_task(
        self, task_id: int, title: str | None = None, description: str | None = None
    ) -> tuple[bool, str]:
        """Update a task's title and/or description.

        Args:
            task_id: ID of task to update
            title: New title (optional, max 500 characters)
            description: New description (optional, max 2000 characters)

        Returns:
            Tuple of (success, message):
            - success: True if updated, False on validation error or not found
            - message: Success or error message
        """
        # Validate at least one field provided
        if title is None and description is None:
            return (False, "Error: No updates provided. Specify title and/or description.")

        # Validate task exists
        task = self._storage.get_by_id(task_id)
        if task is None:
            return (False, f"Error: Task with ID {task_id} not found")

        # Update title if provided
        if title is not None:
            title = title.strip()
            if not title:
                return (False, "Error: Task title cannot be empty")
            if len(title) > 500:
                return (False, "Error: Task title cannot exceed 500 characters")
            task.title = title

        # Update description if provided
        if description is not None:
            description = description.strip()
            if len(description) > 2000:
                return (False, "Error: Task description cannot exceed 2000 characters")
            task.description = description

        # Save updates
        self._storage.update(task)
        return (True, f"Task {task_id} updated successfully")

    def delete_task(self, task_id: int) -> tuple[bool, str]:
        """Delete a task by ID.

        Args:
            task_id: ID of task to delete

        Returns:
            Tuple of (success, message):
            - success: True if deleted, False if task not found
            - message: Success or error message
        """
        # Validate task exists before attempting delete
        if self._storage.get_by_id(task_id) is None:
            return (False, f"Error: Task with ID {task_id} not found")

        # Delete task
        self._storage.delete(task_id)
        return (True, f"Task {task_id} deleted successfully")
