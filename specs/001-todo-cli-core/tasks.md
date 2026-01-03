# Tasks: Todo CLI Core

**Input**: Design documents from `specs/001-todo-cli-core/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Tests are NOT required for this feature based on user input - tasks focus on implementation only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Repository structure: `src/models/`, `src/services/`, `src/storage/`, `src/cli/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project folder structure: src/, src/models/, src/services/, src/storage/, src/cli/, tests/, tests/unit/, tests/integration/
- [x] T002 Create __init__.py files in src/, src/models/, src/services/, src/storage/, src/cli/, tests/, tests/unit/, tests/integration/
- [x] T003 Create pyproject.toml with UV configuration for Python 3.13+, pytest>=8.0, pytest-cov, ruff>=0.1.0, mypy>=1.8
- [x] T004 [P] Setup virtual environment using UV: uv venv
- [x] T005 [P] Create .gitignore with .venv/, __pycache__/, *.pyc, .pytest_cache/, .coverage, .mypy_cache/
- [x] T006 [P] Update README.md with project description, setup instructions for UV and Python 3.13+, and how to run the CLI app

**Checkpoint**: Basic project structure ready - can begin foundational implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 [P] Create Task model dataclass in src/models/task.py with attributes: id (int), title (str), description (str), is_complete (bool)
- [x] T008 [P] Add validation to Task model in src/models/task.py: title non-empty and ≤500 chars, description ≤2000 chars, whitespace normalization
- [x] T009 Create InMemoryStorage class in src/storage/in_memory_storage.py with dict[int, Task] storage and next_id counter
- [x] T010 Implement InMemoryStorage.add() method in src/storage/in_memory_storage.py to store task with auto-generated ID
- [x] T011 [P] Implement InMemoryStorage.get_by_id() method in src/storage/in_memory_storage.py for O(1) lookup
- [x] T012 [P] Implement InMemoryStorage.get_all() method in src/storage/in_memory_storage.py to return all tasks as list
- [x] T013 [P] Implement InMemoryStorage.delete() method in src/storage/in_memory_storage.py to remove task by ID
- [x] T014 Create TodoService class in src/services/todo_service.py with InMemoryStorage dependency injection

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks with a title and optional description so that they can capture todos they need to complete.

**Independent Test**: Launch the CLI, add a task with only a title, add a task with title and description, list tasks to verify both were stored correctly with unique IDs and incomplete status.

**Acceptance Scenarios**:
1. Add task with only title → task created with unique ID, title, empty description, incomplete status
2. Add task with title and description → task created with unique ID, both fields populated, incomplete status
3. Attempt to add task without title → error message displayed, task not created

### Implementation for User Story 1

- [x] T015 [US1] Implement TodoService.add_task() method in src/services/todo_service.py accepting title and description with validation
- [x] T016 [US1] Add title validation in TodoService.add_task() in src/services/todo_service.py: non-empty, ≤500 chars, return (success, message, task_id | None) tuple
- [x] T017 [US1] Add description validation in TodoService.add_task() in src/services/todo_service.py: ≤2000 chars, default to empty string
- [x] T018 [US1] Implement add command handler in src/cli/commands.py to parse "add <title>" and "add <title> | <description>" syntax
- [x] T019 [US1] Connect add command to TodoService.add_task() in src/cli/commands.py with error handling and success message display
- [x] T020 [US1] Add type annotations to all functions in src/services/todo_service.py and src/cli/commands.py using modern Python 3.13+ syntax

**Checkpoint**: At this point, User Story 1 should be fully functional - users can add tasks with titles and optional descriptions

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Enable users to view all their tasks with ID, title, description, and completion status so that they can see what needs to be done.

**Independent Test**: Pre-populate tasks using add command, run list command, verify all task details are displayed in a readable table format with status indicators.

**Acceptance Scenarios**:
1. View tasks when several exist → see list showing ID, title, description (or empty indicator), and status
2. View tasks when none exist → see message indicating task list is empty
3. View tasks with mix of complete/incomplete → easily distinguish between statuses

### Implementation for User Story 2

- [x] T021 [US2] Implement TodoService.get_all_tasks() method in src/services/todo_service.py to return list of all tasks from storage
- [x] T022 [US2] Create list command handler in src/cli/commands.py to display tasks in table format
- [x] T023 [US2] Implement table formatting in src/cli/commands.py: columns for ID, Status, Title, Description with proper alignment
- [x] T024 [US2] Add status display formatting in src/cli/commands.py: [ ] for incomplete, [✓] for complete
- [x] T025 [US2] Implement text truncation in src/cli/commands.py: title >40 chars with "...", description >60 chars with "..."
- [x] T026 [US2] Add empty list handling in src/cli/commands.py to display "No tasks found. Use 'add <title>' to create a task."

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can add and view tasks

---

## Phase 5: User Story 3 - Mark Tasks Complete/Incomplete (Priority: P2)

**Goal**: Enable users to mark tasks as complete or incomplete so that they can track their progress and focus on remaining work.

**Independent Test**: Create tasks using add command, toggle their completion status using toggle command, verify status changes persist and are reflected in list command output.

**Acceptance Scenarios**:
1. Mark incomplete task as complete → task status changes to complete
2. Mark complete task as incomplete → task status changes back to incomplete
3. Attempt to mark non-existent task → error message displayed, no state changes

### Implementation for User Story 3

- [x] T027 [US3] Implement InMemoryStorage.update() method in src/storage/in_memory_storage.py to update task by ID
- [x] T028 [US3] Implement TodoService.toggle_complete() method in src/services/todo_service.py to flip is_complete boolean
- [x] T029 [US3] Add ID validation in TodoService.toggle_complete() in src/services/todo_service.py: check task exists, return (success, message) tuple
- [x] T030 [US3] Create toggle command handler in src/cli/commands.py to parse "toggle <id>" syntax
- [x] T031 [US3] Add ID parsing validation in src/cli/commands.py for toggle command: validate numeric, handle parse errors
- [x] T032 [US3] Connect toggle command to TodoService.toggle_complete() in src/cli/commands.py with appropriate success messages ("marked as complete" vs "marked as incomplete")
- [x] T033 [US3] Add error handling in src/cli/commands.py for toggle command: "Task with ID <id> not found", "Invalid task ID. Please provide a numeric ID."

**Checkpoint**: All P1 and P2 stories should now be independently functional - users can add, view, and toggle tasks

---

## Phase 6: User Story 4 - Update Task Details (Priority: P3)

**Goal**: Enable users to update a task's title or description so that they can refine or correct task information.

**Independent Test**: Create a task, update its title using update command, verify change is reflected in list output, then update description and verify again.

**Acceptance Scenarios**:
1. Update existing task's title → task retains ID and status but shows new title
2. Update existing task's description → task retains ID and status but shows new description
3. Update both title and description → both fields updated while preserving ID and status
4. Attempt to update non-existent task → error message displayed

### Implementation for User Story 4

- [x] T034 [US4] Implement TodoService.update_task() method in src/services/todo_service.py accepting task_id, optional title, optional description
- [x] T035 [US4] Add validation in TodoService.update_task() in src/services/todo_service.py: at least one field must be provided, title/description constraints
- [x] T036 [US4] Add ID validation in TodoService.update_task() in src/services/todo_service.py: check task exists, return (success, message) tuple
- [x] T037 [US4] Create update command handler in src/cli/commands.py to parse "update <id> <title>", "update <id> | <description>", "update <id> <title> | <description>"
- [x] T038 [US4] Add parsing logic in src/cli/commands.py for update command to separate title and description using pipe character
- [x] T039 [US4] Connect update command to TodoService.update_task() in src/cli/commands.py with error handling for all validation failures
- [x] T040 [US4] Add error messages in src/cli/commands.py for update command: "No updates provided. Specify title and/or description."

**Checkpoint**: User Stories 1-4 should now be independently functional - users can add, view, toggle, and update tasks

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P3)

**Goal**: Enable users to delete tasks they no longer need so that their task list stays relevant and uncluttered.

**Independent Test**: Create several tasks, delete specific ones by ID using delete command, verify they no longer appear in list output.

**Acceptance Scenarios**:
1. Delete task by ID → task removed and no longer appears in task list
2. Attempt to delete non-existent task → error message displayed, other tasks unaffected
3. Delete all tasks one by one → empty task list message displayed

### Implementation for User Story 5

- [x] T041 [US5] Implement TodoService.delete_task() method in src/services/todo_service.py to remove task by ID from storage
- [x] T042 [US5] Add ID validation in TodoService.delete_task() in src/services/todo_service.py: check task exists, return (success, message) tuple
- [x] T043 [US5] Create delete command handler in src/cli/commands.py to parse "delete <id>" syntax
- [x] T044 [US5] Add ID parsing validation in src/cli/commands.py for delete command: validate numeric, handle parse errors
- [x] T045 [US5] Connect delete command to TodoService.delete_task() in src/cli/commands.py with success message "Task <id> deleted successfully"
- [x] T046 [US5] Add error handling in src/cli/commands.py for delete command: "Task with ID <id> not found", "Invalid task ID. Please provide a numeric ID."

**Checkpoint**: All user stories should now be independently functional - complete feature set available

---

## Phase 8: CLI Application Shell

**Purpose**: Create the main REPL loop and command dispatcher to tie all user stories together

- [x] T047 Create main CLI app class in src/cli/app.py with REPL loop using input("todo> ")
- [x] T048 Implement command parsing in src/cli/app.py: split on whitespace, extract command and arguments, case-insensitive
- [x] T049 Create command dispatcher in src/cli/app.py to route commands to appropriate handlers from src/cli/commands.py
- [x] T050 Implement help command in src/cli/app.py displaying all available commands with syntax and examples per contracts/cli-commands.md
- [x] T051 Implement quit/exit commands in src/cli/app.py to exit REPL with "Goodbye!" message
- [x] T052 Add error handling in src/cli/app.py for unknown commands: "Error: Unknown command '<command>'. Type 'help' for available commands."
- [x] T053 Add error handling in src/cli/app.py for empty input: "Error: No command entered"
- [x] T054 Add welcome message in src/cli/app.py: "Welcome to Todo CLI! Type 'help' for available commands."
- [x] T055 Create main entry point in src/cli/app.py with if __name__ == "__main__" to initialize TodoService and start REPL

**Checkpoint**: Complete CLI application functional - all user stories accessible through interactive prompt

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [x] T056 [P] Add comprehensive docstrings to all public classes and methods in src/models/task.py, src/services/todo_service.py, src/storage/in_memory_storage.py
- [x] T057 [P] Run ruff linting on all source files: ruff check src/ --fix for PEP 8 compliance
- [x] T058 [P] Run mypy type checking on all source files: mypy src/ to ensure type annotation correctness
- [x] T059 [P] Run ruff formatting on all source files: ruff format src/ for consistent code style
- [x] T060 Validate all commands from quickstart.md against implementation: add, list, update, delete, toggle, help, quit
- [x] T061 Test complete workflow from quickstart.md: add → view → update → toggle → delete sequence
- [x] T062 Verify all success criteria from spec.md: operations <100ms, clear error messages, complete workflows work
- [x] T063 Verify all functional requirements from spec.md: FR-001 through FR-011 all satisfied
- [x] T064 Update CLAUDE.md with instructions for Claude Code to follow Constitution and Spec history references
- [x] T065 Create initial git commit with message: "Initial implementation of Todo CLI Core - Phase I complete"

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion - can run in parallel with US1
- **User Story 3 (Phase 5)**: Depends on Foundational phase completion - can run in parallel with US1/US2
- **User Story 4 (Phase 6)**: Depends on Foundational phase completion - can run in parallel with US1/US2/US3
- **User Story 5 (Phase 7)**: Depends on Foundational phase completion - can run in parallel with US1/US2/US3/US4
- **CLI Shell (Phase 8)**: Depends on at least US1 and US2 completion for MVP - best after all user stories complete
- **Polish (Phase 9)**: Depends on CLI Shell completion - final validation phase

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- **US1**: T015-T017 (service methods) before T018-T019 (CLI handlers)
- **US2**: T021 (service method) before T022-T026 (CLI handlers and formatting)
- **US3**: T027 (storage update) before T028-T029 (service method) before T030-T033 (CLI handlers)
- **US4**: T034-T036 (service method) before T037-T040 (CLI handlers)
- **US5**: T041-T042 (service method) before T043-T046 (CLI handlers)

### Parallel Opportunities

- **Phase 1**: T004, T005, T006 can run in parallel (different files, no dependencies)
- **Phase 2**: T007-T008 (Task model) parallel with T009-T013 (Storage), then T014 (Service) depends on both
- **User Stories (after Phase 2 complete)**: All user stories (US1-US5) can be implemented in parallel by different developers
- **Within US2**: T023, T024, T025, T026 are all formatting tasks in same file, sequential
- **Within US3**: T030, T031, T032, T033 are all CLI handler tasks, sequential
- **Phase 9**: T056, T057, T058, T059 can run in parallel (different tools)

---

## Parallel Example: Foundational Phase

```bash
# Launch Task model and Storage tasks in parallel:
Task T007: "Create Task model dataclass in src/models/task.py"
Task T009: "Create InMemoryStorage class in src/storage/in_memory_storage.py"

# After T007, T008 can run:
Task T008: "Add validation to Task model in src/models/task.py"

# After T009, these can run in parallel:
Task T010: "Implement InMemoryStorage.add() in src/storage/in_memory_storage.py"
Task T011: "Implement InMemoryStorage.get_by_id() in src/storage/in_memory_storage.py"
Task T012: "Implement InMemoryStorage.get_all() in src/storage/in_memory_storage.py"
Task T013: "Implement InMemoryStorage.delete() in src/storage/in_memory_storage.py"
```

---

## Parallel Example: User Stories After Foundation

```bash
# After Phase 2 complete, all user stories can start in parallel:
Developer A: Phase 3 (US1 - Add Tasks)
Developer B: Phase 4 (US2 - View Tasks)
Developer C: Phase 5 (US3 - Toggle Tasks)
Developer D: Phase 6 (US4 - Update Tasks)
Developer E: Phase 7 (US5 - Delete Tasks)

# Each developer can work independently on their story
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T014) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 - Add Tasks (T015-T020)
4. Complete Phase 4: User Story 2 - View Tasks (T021-T026)
5. Complete Phase 8: CLI Shell (T047-T055) - Just add, list, help, quit commands
6. **STOP and VALIDATE**: Test add and list commands independently
7. Deploy/demo if ready - minimal viable product complete

### Incremental Delivery (Recommended)

1. Complete Setup + Foundational → Foundation ready (T001-T014)
2. Add User Story 1 + User Story 2 + CLI Shell → Test independently → Deploy/Demo (MVP!)
3. Add User Story 3 → Test toggle independently → Deploy/Demo
4. Add User Story 4 → Test update independently → Deploy/Demo
5. Add User Story 5 → Test delete independently → Deploy/Demo
6. Complete Polish phase → Final validation → Release

### Full Feature Strategy

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T014)
3. Complete Phase 3-7: All User Stories (T015-T046) - can parallelize if team capacity allows
4. Complete Phase 8: CLI Shell (T047-T055)
5. Complete Phase 9: Polish & Validation (T056-T065)
6. Git commit and tag release

---

## Notes

- [P] tasks = different files, no dependencies - can execute in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each phase or after completing each user story
- Stop at any checkpoint to validate story independently
- All tasks include exact file paths for clarity
- Tasks follow strict checklist format: - [ ] [ID] [P?] [Story?] Description with file path
- Total task count: 65 tasks across 9 phases
- MVP scope: Phases 1-4 + minimal Phase 8 (US1 & US2 only) = ~30 tasks
- User stories are organized in priority order per spec.md (P1, P2, P3)
