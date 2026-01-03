"""CLI command handlers for the Todo application."""

from src.services.todo_service import TodoService


def handle_add(service: TodoService, args: str) -> None:
    """Handle the 'add' command to create a new task.

    Syntax:
        add <title>
        add <title> | <description>

    Args:
        service: TodoService instance for business logic
        args: Command arguments (title and optional description)
    """
    if not args or not args.strip():
        print("Error: Task title cannot be empty")
        return

    # Parse title and description using pipe separator
    if " | " in args:
        parts = args.split(" | ", 1)
        title = parts[0].strip()
        description = parts[1].strip() if len(parts) > 1 else ""
    else:
        title = args.strip()
        description = ""

    # Call service and display result
    success, message, task_id = service.add_task(title, description)
    print(message)


def handle_list(service: TodoService) -> None:
    """Handle the 'list' command to display all tasks.

    Displays tasks in a formatted table with ID, Status, Title, and Description.

    Args:
        service: TodoService instance for business logic
    """
    tasks = service.get_all_tasks()

    # Handle empty list
    if not tasks:
        print("No tasks found. Use 'add <title>' to create a task.")
        return

    # Print table header
    print("ID | Status | Title                                    | Description")
    print(
        "---+--------+------------------------------------------+-------------------------------------------------------------"
    )

    # Print each task
    for task in tasks:
        # Format status: [ ] for incomplete, [✓] for complete
        status = "[✓]" if task.is_complete else "[ ]"

        # Truncate title if >40 chars
        title = task.title if len(task.title) <= 40 else task.title[:37] + "..."

        # Truncate description if >60 chars
        description = (
            task.description if len(task.description) <= 60 else task.description[:57] + "..."
        )

        # Print row with alignment
        print(f"{task.id:<2} | {status:<6} | {title:<40} | {description}")


def handle_toggle(service: TodoService, args: str) -> None:
    """Handle the 'toggle' command to mark a task complete/incomplete.

    Syntax:
        toggle <id>

    Args:
        service: TodoService instance for business logic
        args: Command arguments (task ID)
    """
    if not args or not args.strip():
        print("Error: Invalid task ID. Please provide a numeric ID.")
        return

    # Parse and validate ID
    try:
        task_id = int(args.strip())
    except ValueError:
        print("Error: Invalid task ID. Please provide a numeric ID.")
        return

    # Call service and display result
    success, message = service.toggle_complete(task_id)
    print(message)


def handle_update(service: TodoService, args: str) -> None:
    """Handle the 'update' command to modify a task's title and/or description.

    Syntax:
        update <id> <new_title>
        update <id> | <new_description>
        update <id> <new_title> | <new_description>

    Args:
        service: TodoService instance for business logic
        args: Command arguments (task ID and update values)
    """
    if not args or not args.strip():
        print("Error: No updates provided. Specify title and/or description.")
        return

    # Parse ID from first part
    parts = args.strip().split(maxsplit=1)
    if len(parts) < 2:
        print("Error: No updates provided. Specify title and/or description.")
        return

    # Parse and validate ID
    try:
        task_id = int(parts[0])
    except ValueError:
        print("Error: Invalid task ID. Please provide a numeric ID.")
        return

    # Parse title and description using pipe separator
    update_args = parts[1]
    title = None
    description = None

    if " | " in update_args:
        # Both title and description or just description
        split_parts = update_args.split(" | ", 1)
        if split_parts[0].strip():
            title = split_parts[0].strip()
        if len(split_parts) > 1:
            description = split_parts[1].strip()
    else:
        # Just title
        title = update_args.strip()

    # Call service and display result
    success, message = service.update_task(task_id, title, description)
    print(message)


def handle_delete(service: TodoService, args: str) -> None:
    """Handle the 'delete' command to remove a task.

    Syntax:
        delete <id>

    Args:
        service: TodoService instance for business logic
        args: Command arguments (task ID)
    """
    if not args or not args.strip():
        print("Error: Invalid task ID. Please provide a numeric ID.")
        return

    # Parse and validate ID
    try:
        task_id = int(args.strip())
    except ValueError:
        print("Error: Invalid task ID. Please provide a numeric ID.")
        return

    # Call service and display result
    success, message = service.delete_task(task_id)
    print(message)
