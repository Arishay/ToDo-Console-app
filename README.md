# Todo CLI Core

A simple, in-memory Python CLI task management application implementing five core operations: Add, View, Update, Delete, and Mark Complete.

## Features

- **Add Tasks**: Create tasks with a title and optional description
- **View Tasks**: Display all tasks with ID, title, description, and status
- **Mark Complete**: Toggle task completion status
- **Update Tasks**: Modify task title and/or description
- **Delete Tasks**: Remove tasks from your list

## Requirements

- Python 3.13 or higher
- UV package manager

## Setup

### 1. Install UV

```bash
pip install uv
```

### 2. Create Virtual Environment

```bash
uv venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell)**:
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt)**:
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux**:
```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
uv pip install -e ".[dev]"
```

## Running the Application

```bash
python -m src.cli.app
```

You should see the todo prompt:
```
Welcome to Todo CLI!
Type 'help' for available commands.

todo>
```

## Usage

### Available Commands

- `add <title> [| <description>]` - Create a new task
- `list` - View all tasks
- `toggle <id>` - Mark task complete/incomplete
- `update <id> <title|description>` - Update task details
- `delete <id>` - Delete a task
- `help` - Show available commands
- `quit` or `exit` - Exit the application

### Examples

```
todo> add Buy groceries
Task 1 added successfully

todo> add Review PR | Check tests and security
Task 2 added successfully

todo> list
ID | Status | Title            | Description
---+--------+------------------+-------------------------
1  | [ ]    | Buy groceries    |
2  | [ ]    | Review PR        | Check tests and security

todo> toggle 1
Task 1 marked as complete

todo> delete 2
Task 2 deleted successfully

todo> quit
Goodbye!
```

## Development

### Run Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

### Linting

```bash
ruff check src/ tests/
```

### Type Checking

```bash
mypy src/
```

### Format Code

```bash
ruff format src/ tests/
```

## Important Notes

- **In-Memory Storage**: All data is lost when you exit the application
- **Single Session**: No data persistence between runs
- **Character Limits**: Titles max 500 characters, descriptions max 2000 characters

## Project Structure

```
src/
├── models/          # Data models (Task)
├── services/        # Business logic (TodoService)
├── storage/         # In-memory storage
└── cli/             # CLI interface and commands

tests/
├── unit/            # Unit tests
└── integration/     # Integration tests
```

## License

MIT
