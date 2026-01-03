"""Main CLI application with menu-based interface for Todo management."""

from src.services.todo_service import TodoService
from src.storage.in_memory_storage import InMemoryStorage


def show_menu() -> None:
    """Display the main menu."""
    print("\n" + "=" * 26)
    print("=== TODO CONSOLE APP ===")
    print("=" * 26)
    print("1. View All Tasks")
    print("2. Add New Task")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete")
    print("6. Mark Task Pending")
    print("7. Exit")
    print()


def view_all_tasks(service: TodoService) -> None:
    """Display all tasks."""
    print("\n--- View All Tasks ---")
    tasks = service.get_all_tasks()

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status = "X" if task.is_complete else " "
        print(f"\nID: {task.id}")
        print(f"Title: {task.title}")
        if task.description:
            print(f"Description: {task.description}")
        print(f"Status: [{status}] {'Complete' if task.is_complete else 'Pending'}")


def add_new_task(service: TodoService) -> None:
    """Add a new task with step-by-step prompts."""
    print("\n--- Add New Task ---")

    title = input("Title: ").strip()
    if not title:
        print("X Error: Task title cannot be empty")
        return

    description = input("Description (optional): ").strip()

    success, message, task_id = service.add_task(title, description)
    if success:
        print(f"\nv Task created successfully!")
        print(f"ID: {task_id}")
    else:
        print(f"\nX {message}")


def update_task(service: TodoService) -> None:
    """Update an existing task."""
    print("\n--- Update Task ---")

    task_id_str = input("Enter Task ID: ").strip()
    if not task_id_str:
        print("X Error: Task ID cannot be empty")
        return

    try:
        task_id = int(task_id_str)
    except ValueError:
        print("X Error: Invalid task ID. Please provide a numeric ID.")
        return

    # Check if task exists
    tasks = service.get_all_tasks()
    task_exists = any(t.id == task_id for t in tasks)
    if not task_exists:
        print(f"X Error: Task with ID {task_id} not found")
        return

    print("Leave blank to keep current value")
    title = input("New Title: ").strip()
    description = input("New Description: ").strip()

    # Set to None if empty
    title = title if title else None
    description = description if description else None

    if not title and not description:
        print("X Error: No updates provided")
        return

    success, message = service.update_task(task_id, title, description)
    if success:
        print(f"\nv {message}")
    else:
        print(f"\nX {message}")


def delete_task(service: TodoService) -> None:
    """Delete a task by ID."""
    print("\n--- Delete Task ---")

    task_id_str = input("Enter Task ID to delete: ").strip()
    if not task_id_str:
        print("X Error: Task ID cannot be empty")
        return

    try:
        task_id = int(task_id_str)
    except ValueError:
        print("X Error: Invalid task ID. Please provide a numeric ID.")
        return

    success, message = service.delete_task(task_id)
    if success:
        print(f"\nv {message}")
    else:
        print(f"\nX {message}")


def mark_task_complete(service: TodoService) -> None:
    """Mark a task as complete."""
    print("\n--- Mark Task Complete ---")

    task_id_str = input("Enter Task ID: ").strip()
    if not task_id_str:
        print("X Error: Task ID cannot be empty")
        return

    try:
        task_id = int(task_id_str)
    except ValueError:
        print("X Error: Invalid task ID. Please provide a numeric ID.")
        return

    # Get task and check if already complete
    tasks = service.get_all_tasks()
    task = next((t for t in tasks if t.id == task_id), None)

    if not task:
        print(f"X Error: Task with ID {task_id} not found")
        return

    if task.is_complete:
        print(f"X Task {task_id} is already marked as complete")
        return

    success, message = service.toggle_complete(task_id)
    if success:
        print(f"\nv Task {task_id} marked as complete")
    else:
        print(f"\nX {message}")


def mark_task_pending(service: TodoService) -> None:
    """Mark a task as pending (incomplete)."""
    print("\n--- Mark Task Pending ---")

    task_id_str = input("Enter Task ID: ").strip()
    if not task_id_str:
        print("X Error: Task ID cannot be empty")
        return

    try:
        task_id = int(task_id_str)
    except ValueError:
        print("X Error: Invalid task ID. Please provide a numeric ID.")
        return

    # Get task and check if already pending
    tasks = service.get_all_tasks()
    task = next((t for t in tasks if t.id == task_id), None)

    if not task:
        print(f"X Error: Task with ID {task_id} not found")
        return

    if not task.is_complete:
        print(f"X Task {task_id} is already marked as pending")
        return

    success, message = service.toggle_complete(task_id)
    if success:
        print(f"\nv Task {task_id} marked as pending")
    else:
        print(f"\nX {message}")


def run() -> None:
    """Run the Todo CLI application with menu-based interface."""
    # Initialize storage and service
    storage = InMemoryStorage()
    service = TodoService(storage)

    # Main loop
    while True:
        try:
            # Show menu
            show_menu()

            # Get user choice
            choice = input("Enter choice [1-7]: ").strip()

            # Handle empty input
            if not choice:
                print("X Error: Please enter a valid choice (1-7)")
                continue

            # Validate choice
            if choice not in ["1", "2", "3", "4", "5", "6", "7"]:
                print(f"X Error: Invalid choice '{choice}'. Please enter a number between 1 and 7.")
                continue

            # Dispatch to appropriate handler
            if choice == "1":
                view_all_tasks(service)
            elif choice == "2":
                add_new_task(service)
            elif choice == "3":
                update_task(service)
            elif choice == "4":
                delete_task(service)
            elif choice == "5":
                mark_task_complete(service)
            elif choice == "6":
                mark_task_pending(service)
            elif choice == "7":
                print("\nGoodbye!")
                break

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\n\nGoodbye!")
            break
        except Exception as e:
            # Catch unexpected errors
            print(f"\nX Error: An unexpected error occurred: {e}")


if __name__ == "__main__":
    run()
