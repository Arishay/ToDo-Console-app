# Quickstart Guide: Todo CLI Core

**Feature**: 001-todo-cli-core
**Date**: 2025-12-29
**Audience**: Developers setting up and using the Todo CLI application

## Overview

This guide provides step-by-step instructions for setting up, running, and using the Todo CLI Core application. The application is a simple, in-memory task manager with five core operations: Add, View, Update, Delete, and Toggle Complete.

## Prerequisites

**Required**:
- Python 3.13 or higher
- UV package manager (for dependency management)

**Verification**:
```bash
python --version  # Should show Python 3.13.x or higher
uv --version      # Should show uv version
```

If Python 3.13+ is not installed:
- Download from [python.org](https://www.python.org/downloads/)
- Or use pyenv: `pyenv install 3.13`

If UV is not installed:
```bash
pip install uv
```

## Setup

### 1. Clone or Navigate to Project

```bash
cd /path/to/todo-console-app
```

### 2. Create Virtual Environment with UV

```bash
uv venv
```

This creates a `.venv` directory with Python 3.13+ virtual environment.

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

You should see `(.venv)` prefix in your prompt.

### 4. Install Development Dependencies

```bash
uv pip install -e ".[dev]"
```

This installs:
- pytest (testing framework)
- pytest-cov (coverage reporting)
- ruff (linting)
- mypy (type checking)

### 5. Verify Installation

```bash
pytest --version
ruff --version
mypy --version
```

All commands should succeed without errors.

## Running the Application

### Standard Execution

From the project root (with virtual environment activated):

```bash
python -m src.cli.app
```

You should see the todo prompt:
```
Welcome to Todo CLI!
Type 'help' for available commands.

todo>
```

### Alternative Execution Methods

**Direct module execution**:
```bash
python src/cli/app.py
```

**Using UV run** (without activating venv):
```bash
uv run python -m src.cli.app
```

## Basic Usage

### Creating Your First Task

```
todo> add Buy groceries
Task 1 added successfully
```

### Viewing All Tasks

```
todo> list
ID | Status | Title            | Description
---+--------+------------------+------------
1  | [ ]    | Buy groceries    |
```

### Adding Task with Description

```
todo> add Review pull request | Check tests, security, and documentation
Task 2 added successfully

todo> list
ID | Status | Title                 | Description
---+--------+-----------------------+---------------------------
1  | [ ]    | Buy groceries         |
2  | [ ]    | Review pull request   | Check tests, security,...
```

### Marking Task Complete

```
todo> toggle 1
Task 1 marked as complete

todo> list
ID | Status | Title                 | Description
---+--------+-----------------------+---------------------------
1  | [✓]    | Buy groceries         |
2  | [ ]    | Review pull request   | Check tests, security,...
```

### Updating Task Details

```
todo> update 1 Buy groceries and cook dinner
Task 1 updated successfully

todo> update 2 | Add integration tests and update docs
Task 2 updated successfully
```

### Deleting a Task

```
todo> delete 1
Task 1 deleted successfully

todo> list
ID | Status | Title                 | Description
---+--------+-----------------------+---------------------------
2  | [ ]    | Review pull request   | Add integration tests...
```

### Getting Help

```
todo> help
Available Commands:
  add <title> [| <description>]     Create a new task
  list                               View all tasks
  update <id> <title|desc>          Update task details
  delete <id>                        Delete a task
  toggle <id>                        Mark task complete/incomplete
  help                               Show this help message
  quit                               Exit the application
```

### Exiting the Application

```
todo> quit
Goodbye!
```

## Complete Workflow Example

Here's a complete task management session:

```
todo> add Write spec document
Task 1 added successfully

todo> add Implement feature | Follow TDD approach
Task 2 added successfully

todo> add Write tests | Unit and integration tests
Task 3 added successfully

todo> list
ID | Status | Title              | Description
---+--------+--------------------+-------------------------
1  | [ ]    | Write spec document|
2  | [ ]    | Implement feature  | Follow TDD approach
3  | [ ]    | Write tests        | Unit and integration...

todo> toggle 1
Task 1 marked as complete

todo> update 2 | Follow TDD, implement in src/services/
Task 2 updated successfully

todo> toggle 3
Task 3 marked as complete

todo> list
ID | Status | Title              | Description
---+--------+--------------------+-------------------------
1  | [✓]    | Write spec document|
2  | [ ]    | Implement feature  | Follow TDD, implement...
3  | [✓]    | Write tests        | Unit and integration...

todo> delete 3
Task 3 deleted successfully

todo> quit
Goodbye!
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

Target: ≥80% coverage for all business logic (models, services, storage).

### Run Specific Test File

```bash
pytest tests/unit/test_todo_service.py
```

### Run Tests Matching Pattern

```bash
pytest -k "test_add"
```

## Code Quality Checks

### Linting (PEP 8 Compliance)

```bash
ruff check src/ tests/
```

Fix auto-fixable issues:
```bash
ruff check --fix src/ tests/
```

### Type Checking

```bash
mypy src/
```

All type checks should pass before committing code.

### Format Check

```bash
ruff format --check src/ tests/
```

Auto-format code:
```bash
ruff format src/ tests/
```

## Troubleshooting

### Issue: "Module not found" error

**Solution**: Ensure virtual environment is activated and dependencies installed:
```bash
source .venv/bin/activate  # or appropriate activation command
uv pip install -e ".[dev]"
```

### Issue: Python version too old

**Solution**: Install Python 3.13+ or use pyenv:
```bash
pyenv install 3.13
pyenv local 3.13
```

### Issue: UV not found

**Solution**: Install UV package manager:
```bash
pip install uv
```

### Issue: Tests failing

**Solution**: Check that you're in the project root and venv is activated:
```bash
pwd  # Should show project root
which python  # Should show .venv/bin/python (or .venv\Scripts\python.exe on Windows)
pytest -v  # Run with verbose output to see specific failures
```

### Issue: Type checking errors

**Solution**: Ensure all function signatures have type hints:
```python
# ❌ Bad - no type hints
def add_task(title, description):
    pass

# ✅ Good - complete type hints
def add_task(title: str, description: str = "") -> tuple[bool, str, int | None]:
    pass
```

## Important Notes

### Data Persistence

⚠️ **WARNING**: This is an in-memory application. All data is lost when you exit.

- Tasks are NOT saved to disk
- Restarting the app starts with an empty task list
- This is intentional for Phase I (per specification)

### Input Limits

- **Task Title**: Maximum 500 characters (required, non-empty)
- **Task Description**: Maximum 2000 characters (optional)
- Exceeding limits triggers validation error

### Command Format

- Commands are case-insensitive (`add`, `ADD`, `Add` all work)
- Use `|` (pipe) to separate title from description
- Task IDs must be positive integers
- Leading/trailing whitespace is automatically trimmed

## Next Steps

### For Users

1. Start the application: `python -m src.cli.app`
2. Type `help` to see available commands
3. Create your first task with `add <title>`
4. Manage your tasks using the five core commands

### For Developers

1. Read the constitution: `.specify/memory/constitution.md`
2. Review the spec: `specs/001-todo-cli-core/spec.md`
3. Study the implementation plan: `specs/001-todo-cli-core/plan.md`
4. Run tests before making changes: `pytest`
5. Follow TDD: Write failing tests, then implement
6. Verify code quality: `ruff check src/` and `mypy src/`

## Support

For issues or questions:
1. Check this quickstart guide
2. Review error messages (they're designed to be actionable)
3. Consult the specification: `specs/001-todo-cli-core/spec.md`
4. Check the CLI contracts: `specs/001-todo-cli-core/contracts/cli-commands.md`

## Success Criteria Validation

Per the specification, verify that:
- ✅ Tasks can be added and viewed within 1 second
- ✅ All operations execute in < 100ms
- ✅ Invalid operations produce clear error messages
- ✅ Complete workflow (add → view → update → toggle → delete) works without errors
- ✅ Empty task list displays appropriate message
- ✅ Task status (complete/incomplete) is clearly distinguishable

All criteria must pass for feature to be considered complete.
