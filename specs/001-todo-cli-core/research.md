# Research: Todo CLI Core

**Feature**: 001-todo-cli-core
**Date**: 2025-12-29
**Status**: Complete

## Overview

This document captures research findings and technology decisions for the Todo CLI Core implementation. All technology choices were predetermined by project constitution and specification requirements, focusing on simplicity and stdlib-only runtime dependencies.

## Research Areas

### 1. CLI Argument Parsing Patterns

**Question**: What CLI input pattern best suits a simple REPL-based task manager?

**Options Evaluated**:

1. **argparse with subcommands** (stdlib)
   - Pros: Built-in help, argument validation, professional CLI feel
   - Cons: Requires restart for each command, not interactive, overkill for simple REPL

2. **Click framework** (external)
   - Pros: Elegant API, excellent user experience, composable commands
   - Cons: External dependency (violates simplicity principle), unnecessary for basic REPL

3. **Simple input loop with manual parsing**
   - Pros: Zero dependencies, full control, perfect for REPL, minimal code
   - Cons: Manual validation, less polish than frameworks

**Decision**: Simple input loop with manual parsing

**Rationale**:
- Constitution principle V (Simplicity/YAGNI): No external dependencies needed
- Spec requirement: Interactive CLI session (REPL suits this better than argparse)
- Implementation simplicity: ~50 lines vs ~200+ with argparse subcommands
- User experience: REPL keeps user in session vs running multiple commands

**Implementation Pattern**:
```python
while True:
    command_line = input("todo> ")
    parts = command_line.strip().split(maxsplit=1)
    command = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""
    # Dispatch to command handlers
```

---

### 2. In-Memory Storage Patterns

**Question**: What data structure optimizes for task CRUD operations?

**Options Evaluated**:

1. **List of Task objects**
   - Pros: Simple iteration, preserves insertion order
   - Cons: O(n) lookup by ID for update/delete/toggle

2. **Dictionary keyed by task ID**
   - Pros: O(1) lookup/update/delete, simple implementation
   - Cons: Requires separate tracking of next ID

3. **OrderedDict (stdlib)**
   - Pros: O(1) lookup + insertion order preserved
   - Cons: Unnecessary (dict preserves order in Python 3.7+)

**Decision**: Dictionary keyed by task ID

**Rationale**:
- Performance: O(1) lookup critical for update/delete/toggle operations (FR-005, FR-006, FR-007)
- Simplicity: Dict is simpler than OrderedDict (Python 3.7+ dicts preserve order)
- Scale: Spec assumes < 1000 tasks per session; dict handles this easily
- ID validation: `id in tasks` is O(1) check (required by FR-008)

**Implementation Pattern**:
```python
class InMemoryStorage:
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
```

---

### 3. ID Generation Strategies

**Question**: How should task IDs be generated to meet FR-002 (auto-incrementing integers from 1)?

**Options Evaluated**:

1. **UUID (external or stdlib)**
   - Pros: Globally unique, no collision concerns
   - Cons: Poor UX for CLI (hard to type "delete abc-123-def"), violates FR-002 requirement

2. **Auto-incrementing counter (class variable)**
   - Pros: Simple, deterministic, meets spec exactly (start from 1)
   - Cons: IDs not reused after delete (acceptable for session-based app)

3. **Find max ID + 1**
   - Pros: Deterministic, could reuse IDs if needed
   - Cons: O(n) operation on every add, unnecessary complexity

**Decision**: Auto-incrementing counter

**Rationale**:
- Spec compliance: FR-002 explicitly requires "auto-incrementing integer ID starting from 1"
- Determinism: Constitution principle IV - counter is perfectly deterministic
- Simplicity: Single integer variable, increment on each add
- Performance: O(1) ID generation
- User experience: Sequential IDs easy to remember and type (e.g., "delete 5")

**Implementation Pattern**:
```python
def add_task(self, task: Task) -> int:
    task.id = self._next_id
    self._tasks[self._next_id] = task
    self._next_id += 1
    return task.id
```

---

### 4. Error Handling Best Practices

**Question**: What error handling pattern balances explicitness with usability?

**Options Evaluated**:

1. **Exceptions for all errors**
   - Pros: Pythonic, stack traces for debugging
   - Cons: Control flow via exceptions (anti-pattern), harder to test, obscures error paths

2. **Result/Error tuple pattern**
   - Pros: Explicit error handling, testable, clear success/failure paths
   - Cons: More verbose than exceptions, requires unpacking

3. **Optional/Maybe pattern (external lib)**
   - Pros: Functional style, composable
   - Cons: External dependency, unfamiliar to many Python developers

**Decision**: Result/Error tuple pattern

**Rationale**:
- Explicitness: Constitution principle IV (deterministic behavior) - errors are explicit, not hidden
- Testability: Easy to assert on (success, error_msg) tuples in tests
- No dependencies: Pure Python, no external libs needed
- Clarity: FR-009 requires "clear error messages" - tuples make message handling obvious
- Control flow: Errors are data, not control flow (aligns with functional principles)

**Implementation Pattern**:
```python
def add_task(self, title: str, description: str = "") -> tuple[bool, str, int | None]:
    """Returns (success, message, task_id)"""
    if not title or not title.strip():
        return (False, "Error: Task title cannot be empty", None)
    if len(title) > 500:
        return (False, "Error: Task title cannot exceed 500 characters", None)
    # ... success case
    return (True, f"Task {task_id} added successfully", task_id)
```

---

### 5. Type Annotation Patterns for Python 3.13+

**Question**: What type annotation style maximizes type safety and readability?

**Options Evaluated**:

1. **Legacy typing module (Union, Optional, List, Dict)**
   - Pros: Compatible with older Python versions
   - Cons: Verbose, outdated for Python 3.13+

2. **Modern syntax (| for unions, built-in generics)**
   - Pros: Concise, Pythonic, Python 3.10+ standard
   - Cons: None (target is Python 3.13+)

3. **Minimal typing (only function signatures)**
   - Pros: Less boilerplate
   - Cons: Misses benefits of full type coverage (mypy validation)

**Decision**: Modern syntax with comprehensive annotations

**Rationale**:
- Constitution principle VI: Type hints mandatory for function signatures
- Python 3.13+ target: Can use `|` for unions, built-in generics (list[T], dict[K,V])
- Mypy validation: Full coverage enables catching errors before runtime
- Readability: Modern syntax is more readable (`int | None` vs `Optional[int]`)

**Implementation Pattern**:
```python
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    title: str
    description: str
    is_complete: bool

def get_task_by_id(self, task_id: int) -> Task | None:
    return self._tasks.get(task_id)

def update_task(self, task_id: int, title: str | None, description: str | None) -> tuple[bool, str]:
    # ...
```

---

## Technology Stack Summary

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Language | Python 3.13+ | Specified in constitution and spec requirements |
| Package Manager | UV | Constitution requirement for dependency management |
| Runtime Dependencies | None (stdlib only) | Simplicity principle - no external runtime deps needed |
| CLI Pattern | REPL with input loop | Best fit for interactive session-based usage |
| Storage | dict[int, Task] | O(1) lookup for all ID-based operations |
| ID Generation | Auto-increment counter | Meets FR-002, simple and deterministic |
| Error Handling | Result/Error tuples | Explicit, testable, clear error messages |
| Type Annotations | Modern Python 3.13+ | Built-in generics, union syntax (|) |
| Testing | pytest | Constitution requirement |
| Linting | ruff | Constitution requirement (PEP 8 compliance) |
| Type Checking | mypy | Constitution requirement |

---

## Development Dependencies

**Rationale**: All dev dependencies align with constitution code quality standards

- **pytest** (>= 8.0): Unit and integration testing framework
- **pytest-cov**: Coverage reporting to verify ≥80% target
- **ruff** (>= 0.1.0): Fast Python linter for PEP 8 compliance
- **mypy** (>= 1.8): Static type checker for type hint validation

---

## Open Questions

None - all technology decisions finalized and align with constitution principles.

---

## Next Steps

Proceed to Phase 1 (Design):
1. Create `data-model.md` with Task entity specification
2. Create `contracts/cli-commands.md` with CLI command contracts
3. Create `quickstart.md` with setup and usage instructions
