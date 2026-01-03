# CLI Commands Contract: Todo CLI Core

**Feature**: 001-todo-cli-core
**Date**: 2025-12-29
**Status**: Complete

## Overview

This document defines the command-line interface contracts for the Todo CLI Core application. The CLI uses a REPL (Read-Eval-Print Loop) pattern where users enter commands interactively at a prompt.

## General CLI Behavior

**Prompt**: `todo> `

**Command Format**: `<command> [arguments]`

**Common Responses**:
- Success operations: Confirmation message + updated state (if applicable)
- Error operations: Error message prefixed with "Error: " + no state change
- Empty list operations: Informational message (e.g., "No tasks found")

**Error Handling**:
- Invalid command: "Error: Unknown command '<command>'. Type 'help' for available commands."
- Invalid arguments: Command-specific error message
- Invalid task ID: "Error: Task with ID <id> not found"

## Commands

### 1. add

**Purpose**: Create a new task with title and optional description

**Syntax**:
```
add <title>
add <title> | <description>
```

**Arguments**:
- `<title>` (required): Task title, max 500 characters
- `<description>` (optional): Task description, max 2000 characters
- Separator: Pipe character `|` separates title from description

**Success Response**:
```
Task <id> added successfully
```

**Error Responses**:
```
Error: Task title cannot be empty
Error: Task title cannot exceed 500 characters
Error: Task description cannot exceed 2000 characters
```

**Examples**:
```
todo> add Buy groceries
Task 1 added successfully

todo> add Review PR #47 | Check security and test coverage
Task 2 added successfully

todo> add
Error: Task title cannot be empty

todo> add <501 character string>
Error: Task title cannot exceed 500 characters
```

**Maps to**: FR-001, FR-002, FR-003, FR-009

---

### 2. list

**Purpose**: Display all tasks with their details

**Syntax**:
```
list
```

**Arguments**: None

**Success Response** (tasks exist):
```
ID | Status | Title | Description
---+--------+-------+------------
1  | [ ]    | Buy groceries |
2  | [✓]    | Review PR #47 | Check security and test coverage
3  | [ ]    | Implement auth | Research OAuth2 providers...
```

**Success Response** (no tasks):
```
No tasks found. Use 'add <title>' to create a task.
```

**Format Details**:
- `ID`: Task identifier (right-aligned integer)
- `Status`: `[ ]` for incomplete, `[✓]` for complete
- `Title`: Task title (truncated if > 40 chars with "...")
- `Description`: Task description (truncated if > 60 chars with "...")

**Examples**:
```
todo> list
ID | Status | Title             | Description
---+--------+-------------------+-------------------------
1  | [ ]    | Buy groceries     |
2  | [✓]    | Review PR #47     | Check security and test...

todo> list
No tasks found. Use 'add <title>' to create a task.
```

**Maps to**: FR-004, FR-010

---

### 3. update

**Purpose**: Update a task's title and/or description

**Syntax**:
```
update <id> <new_title>
update <id> | <new_description>
update <id> <new_title> | <new_description>
```

**Arguments**:
- `<id>` (required): Task ID to update
- `<new_title>` (optional): New title, max 500 characters
- `<new_description>` (optional): New description, max 2000 characters
- Separator: Pipe character `|` separates title from description
- At least one of title or description MUST be provided

**Success Response**:
```
Task <id> updated successfully
```

**Error Responses**:
```
Error: Task with ID <id> not found
Error: Task title cannot be empty
Error: Task title cannot exceed 500 characters
Error: Task description cannot exceed 2000 characters
Error: No updates provided. Specify title and/or description.
```

**Examples**:
```
todo> update 1 Buy groceries and cook dinner
Task 1 updated successfully

todo> update 2 | Check security, test coverage, and docs
Task 2 updated successfully

todo> update 3 Implement OAuth2 | Research providers, design flow, implement endpoints
Task 3 updated successfully

todo> update 999 New title
Error: Task with ID 999 not found

todo> update 1
Error: No updates provided. Specify title and/or description.
```

**Maps to**: FR-006, FR-008, FR-009

---

### 4. delete

**Purpose**: Delete a task by ID

**Syntax**:
```
delete <id>
```

**Arguments**:
- `<id>` (required): Task ID to delete

**Success Response**:
```
Task <id> deleted successfully
```

**Error Responses**:
```
Error: Task with ID <id> not found
Error: Invalid task ID. Please provide a numeric ID.
```

**Examples**:
```
todo> delete 1
Task 1 deleted successfully

todo> delete 999
Error: Task with ID 999 not found

todo> delete abc
Error: Invalid task ID. Please provide a numeric ID.
```

**Maps to**: FR-007, FR-008, FR-009

---

### 5. toggle

**Purpose**: Toggle a task's completion status (incomplete ↔ complete)

**Syntax**:
```
toggle <id>
```

**Arguments**:
- `<id>` (required): Task ID to toggle

**Success Response**:
```
Task <id> marked as complete
Task <id> marked as incomplete
```

**Error Responses**:
```
Error: Task with ID <id> not found
Error: Invalid task ID. Please provide a numeric ID.
```

**Examples**:
```
todo> toggle 1
Task 1 marked as complete

todo> toggle 1
Task 1 marked as incomplete

todo> toggle 999
Error: Task with ID 999 not found
```

**Maps to**: FR-005, FR-008, FR-009

---

### 6. help

**Purpose**: Display available commands and usage instructions

**Syntax**:
```
help
```

**Arguments**: None

**Success Response**:
```
Available Commands:
  add <title> [| <description>]     Create a new task
  list                               View all tasks
  update <id> <title|desc>          Update task details
  delete <id>                        Delete a task
  toggle <id>                        Mark task complete/incomplete
  help                               Show this help message
  quit                               Exit the application

Examples:
  add Buy groceries
  add Review PR | Check tests and security
  list
  update 1 Buy groceries and milk
  delete 2
  toggle 1
```

**Examples**:
```
todo> help
Available Commands:
  ...
```

**Maps to**: General usability (not explicitly in FRs)

---

### 7. quit

**Purpose**: Exit the application

**Syntax**:
```
quit
exit
```

**Arguments**: None

**Success Response**:
```
Goodbye!
```
(Application terminates)

**Examples**:
```
todo> quit
Goodbye!
```

**Maps to**: FR-011 (data loss on exit is expected behavior)

---

## Command Parsing Rules

1. **Case Insensitivity**: Commands are case-insensitive (`ADD`, `add`, `Add` all accepted)
2. **Whitespace Handling**:
   - Leading/trailing whitespace ignored
   - Multiple spaces between command and args collapsed to single space
3. **Pipe Separator**: `|` separates title from description in `add` and `update` commands
4. **ID Parsing**: Task IDs must be positive integers; non-numeric input triggers error
5. **Empty Input**: Pressing Enter without input shows error: "Error: No command entered"

## Input Validation Order

For all commands with task IDs:
1. Validate ID format (numeric)
2. Validate ID exists in storage
3. Validate command-specific arguments (title length, etc.)
4. Execute operation

This ensures consistent error messages and prevents partial state updates.

## Error Message Standards

All error messages MUST:
- Start with "Error: " prefix
- Be specific and actionable (tell user what's wrong and how to fix it)
- Reference the failed operation (e.g., task ID, constraint violated)
- Use proper grammar and punctuation
- Avoid technical jargon (e.g., "Task not found" not "Key error: 999")

## Response Time Requirements

Per SC-007 (Success Criteria), all commands MUST:
- Execute in < 100ms
- Display results immediately (synchronous)
- Provide feedback for every operation (no silent failures)

## Session Behavior

Per FR-011, the application:
- Stores all data in memory during session
- Loses all data when `quit` or `exit` command executed
- Starts with empty task list on each launch
- Does NOT persist tasks between sessions

## Mapping to User Stories

| Command | User Story | Priority |
|---------|-----------|----------|
| add | US1 - Add New Tasks | P1 |
| list | US2 - View All Tasks | P1 |
| toggle | US3 - Mark Complete/Incomplete | P2 |
| update | US4 - Update Task Details | P3 |
| delete | US5 - Delete Tasks | P3 |

## Future Considerations (Out of Scope)

The following enhancements are noted for potential future phases:

- **Search/Filter**: `list --status complete`, `search <keyword>`
- **Sorting**: `list --sort-by priority`, `list --sort-by created`
- **Batch Operations**: `delete 1,2,3`, `toggle 4-7`
- **Undo/Redo**: Command history with undo support
- **Export**: `export tasks.json`, `export tasks.csv`

These are intentionally excluded per the specification's "Out of Scope" section.
