"""Task model for the Todo CLI application."""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a todo task.

    Attributes:
        id: Unique auto-generated identifier (≥ 1)
        title: Short task description (required, max 500 chars)
        description: Detailed task information (optional, max 2000 chars)
        is_complete: Completion status (default: False)
    """

    id: int
    title: str
    description: str
    is_complete: bool

    def __post_init__(self) -> None:
        """Validate task attributes after initialization."""
        # Validate and normalize title
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")

        self.title = self.title.strip()

        if len(self.title) > 500:
            raise ValueError("Task title cannot exceed 500 characters")

        # Validate and normalize description
        self.description = self.description.strip()

        if len(self.description) > 2000:
            raise ValueError("Task description cannot exceed 2000 characters")

        # Validate ID
        if self.id < 1:
            raise ValueError("Task ID must be >= 1")
