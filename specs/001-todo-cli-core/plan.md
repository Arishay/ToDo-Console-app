# Implementation Plan: Todo CLI Core

**Branch**: `001-todo-cli-core` | **Date**: 2025-12-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-todo-cli-core/spec.md`

## Summary

Implement an in-memory Python CLI application for basic task management supporting five core operations: Add, View, Update, Delete, and Mark Complete. The application follows clean architecture principles with strict separation between models, services, CLI interface, and in-memory storage. Implementation uses Python 3.13+ with UV for dependency management, pytest for testing, and adheres to PEP 8 with full type annotations.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: No external runtime dependencies (stdlib only); pytest for testing, ruff for linting, mypy for type checking
**Storage**: In-memory (Python dict/list) - no persistence
**Testing**: pytest with 80%+ coverage target
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)
**Project Type**: Single project (CLI application)
**Performance Goals**: < 100ms response time for all operations (Add, View, Update, Delete, Toggle)
**Constraints**: Single-user synchronous operation, session-based (data lost on exit), max 500 chars for title, max 2000 chars for description
**Scale/Scope**: Single session, expected < 1000 tasks per session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Specification-First Development ✅
- **Status**: PASS
- **Evidence**: Feature specification complete in `specs/001-todo-cli-core/spec.md` with 5 user stories, 11 functional requirements, 8 success criteria

### Principle II: Clean Architecture ✅
- **Status**: PASS
- **Evidence**: Plan enforces separation: models/ (Task entity), services/ (TodoService business logic), cli/ (user interaction), storage/ (in-memory storage)
- **Boundaries**: Models are pure data structures, Services operate on models with no I/O, CLI handles user interaction, Storage manages task collection

### Principle III: Test-Driven Development (TDD) ✅
- **Status**: PASS
- **Evidence**: pytest configured, unit tests required for all service operations before implementation, 80%+ coverage target
- **Scope**: Unit tests for models and services (mandatory), integration tests for CLI workflows (recommended)

### Principle IV: Deterministic Behavior ✅
- **Status**: PASS
- **Evidence**: All operations synchronous, auto-incrementing IDs (deterministic), no external dependencies, clear error messages for all failure modes

### Principle V: Simplicity and YAGNI ✅
- **Status**: PASS
- **Evidence**: Zero external runtime dependencies, in-memory storage (simplest option), no premature abstractions, implements only specified features

### Principle VI: Code Quality Standards ✅
- **Status**: PASS
- **Evidence**: PEP 8 compliance via ruff, type hints mandatory (mypy), docstrings for public APIs, clear naming conventions

**Gate Result**: ✅ **PASS** - All principles satisfied, proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-cli-core/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── cli-commands.md  # CLI command contracts
└── spec.md              # Feature specification (already created)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── __init__.py
│   └── task.py          # Task entity (id, title, description, is_complete)
├── services/
│   ├── __init__.py
│   └── todo_service.py  # Business logic (add, get_all, update, delete, toggle_complete)
├── storage/
│   ├── __init__.py
│   └── in_memory_storage.py  # In-memory task storage (dict-based)
├── cli/
│   ├── __init__.py
│   ├── app.py           # CLI loop and command dispatcher
│   └── commands.py      # Command implementations (add_cmd, view_cmd, etc.)
└── __init__.py

tests/
├── unit/
│   ├── __init__.py
│   ├── test_task_model.py
│   ├── test_todo_service.py
│   └── test_storage.py
└── integration/
    ├── __init__.py
    └── test_cli_workflows.py

pyproject.toml           # UV project configuration
README.md                # Setup and usage instructions
```

**Structure Decision**: Using Option 1 (Single project) as this is a standalone CLI application with no frontend/backend split. The structure follows constitution's prescribed layout with models/, services/, cli/, and storage/ separation to enforce clean architecture boundaries.

## Complexity Tracking

> No violations - all constitution principles satisfied without exceptions.

## Phase 0: Research

### Research Tasks

No external research required - all technology choices are predetermined:
- Python 3.13+ (specified in constitution and user requirements)
- UV package manager (specified in constitution)
- pytest testing framework (standard Python testing, specified in constitution)
- In-memory storage (specified in spec - no database research needed)
- stdlib-only runtime (simplicity principle - no external dependencies)

### Research Findings

See [research.md](./research.md) for detailed findings on:
1. CLI argument parsing patterns (stdlib argparse vs simple input loop)
2. In-memory storage patterns (dict vs list performance characteristics)
3. ID generation strategies (counter vs UUID trade-offs)
4. Error handling best practices for CLI applications
5. Type annotation patterns for Python 3.13+

## Phase 1: Design

### Data Model

See [data-model.md](./data-model.md) for complete entity definitions.

**Summary**:
- **Task**: id (int), title (str), description (str), is_complete (bool)
- **Validation Rules**: title non-empty and ≤500 chars, description ≤2000 chars
- **ID Strategy**: Auto-incrementing integer starting from 1

### CLI Contracts

See [contracts/cli-commands.md](./contracts/cli-commands.md) for command specifications.

**Summary of Commands**:
1. `add <title> [description]` - Create new task
2. `list` - View all tasks
3. `update <id> [--title <title>] [--description <desc>]` - Update task
4. `delete <id>` - Delete task
5. `toggle <id>` - Mark complete/incomplete
6. `quit` - Exit application

### Quickstart Guide

See [quickstart.md](./quickstart.md) for setup and usage instructions.

## Implementation Notes

### Architectural Decisions

1. **CLI Interface Pattern**: Simple REPL (Read-Eval-Print Loop) with command parsing
   - **Rationale**: Simplest approach for single-user CLI, no need for argparse complexity
   - **Alternative Rejected**: Click/argparse frameworks add unnecessary dependencies

2. **Storage Pattern**: Dictionary keyed by task ID
   - **Rationale**: O(1) lookup by ID for update/delete/toggle operations
   - **Alternative Rejected**: List with linear search (O(n)) slower for larger task counts

3. **ID Generation**: Class-level counter in TodoService
   - **Rationale**: Simple, deterministic, meets requirements (auto-increment from 1)
   - **Alternative Rejected**: UUID (overkill for single-session in-memory use)

4. **Error Handling**: Return Result/Error tuple pattern
   - **Rationale**: Explicit error handling without exceptions for control flow
   - **Alternative Rejected**: Exception-based (makes testing harder, less explicit)

### Testing Strategy

1. **Unit Tests** (models, services, storage):
   - Test Task validation (empty title, length limits)
   - Test TodoService operations in isolation
   - Test storage CRUD operations

2. **Integration Tests** (CLI workflows):
   - Test complete user journeys from spec
   - Test error message clarity
   - Test empty list handling

### Dependencies

**Runtime**: None (stdlib only)

**Development**:
- pytest >= 8.0
- pytest-cov (coverage reporting)
- ruff >= 0.1.0 (linting)
- mypy >= 1.8 (type checking)

### Success Validation

Implementation complete when:
1. All 11 functional requirements (FR-001 to FR-011) pass acceptance tests
2. All 5 user stories validated with Given/When/Then scenarios
3. All 8 success criteria (SC-001 to SC-008) verified
4. Unit test coverage ≥ 80% for models and services
5. PEP 8 compliance verified via ruff
6. Type checking passes via mypy
7. Integration tests pass for complete workflows
