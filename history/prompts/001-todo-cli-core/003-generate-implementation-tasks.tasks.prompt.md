---
id: 003
title: Generate implementation tasks for Todo CLI Core
stage: tasks
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5
feature: 001-todo-cli-core
branch: 001-todo-cli-core
user: affil
command: /sp.tasks
labels: ["task-generation", "implementation-planning", "user-stories"]
links:
  spec: specs/001-todo-cli-core/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-todo-cli-core/tasks.md
tests:
---

## Prompt

Phase I: In-Memory Python Todo CLI App

Objective:
Guide Claude to implement the in-memory Python CLI Todo app step-by-step, strictly following spec-driven development, using the Constitution, /sp.specify, and /sp.plan as references.

Tasks:

1. Project Initialization
   - Create the project folder structure:
       /src
       /specs/history
       Constitution.md
       README.md
       CLAUDE.md
   - Setup Python 3.13+ virtual environment using UV
   - Initialize Git repository for version control

2. Specification Handling
   - Review /sp.specify and ensure all five basic features are covered
   - Write initial versioned specification: v1_todo_spec.md
   - Save the specification in /specs/history
   - Ensure spec covers: Task model, Task ID generation, status handling, CLI inputs/outputs, and error handling

3. Data Modeling
   - Define Task model in Python with attributes:
       - id (unique, auto-increment)
       - title (string)
       - description (string)
       - completed (boolean)
   - Ensure Task model is modular and separate from CLI and business logic

4. Business Logic Implementation (TodoService)
   - Implement Add Task:
       - Accept title and description
       - Auto-generate unique task ID
       - Default status: Pending
   - Implement View Tasks:
       - Display all tasks with ID, title, description, and status
   - Implement Update Task:
       - Update title and/or description by ID
       - Handle invalid IDs gracefully
   - Implement Delete Task:
       - Delete task by ID
       - Confirm deletion
       - Handle invalid IDs gracefully
   - Implement Mark Complete/Incomplete:
       - Toggle task status by ID
       - Confirm status change
       - Handle invalid IDs gracefully

5. CLI Interface
   - Create main.py as the entry point
   - Implement a menu-driven loop:
       - Options: Add, View, Update, Delete, Mark Complete/Incomplete, Exit
       - Accept user input for option selection
       - Call corresponding TodoService methods
   - Ensure input validation (non-numeric, out-of-range, empty titles)

6. Testing & Validation
   - Test each feature individually against the specification
   - Test multiple tasks, including edge cases (no tasks, duplicate titles)
   - Ensure in-memory storage works across operations
   - Ensure all outputs match the expected CLI format
   - Confirm behavior is deterministic and matches the specification

7. Documentation
   - Update README.md with:
       - Project description
       - Setup instructions for UV and Python 3.13+
       - How to run the CLI app
   - Update CLAUDE.md with instructions for Claude Code to follow Constitution and Spec history

8. Versioning & Commit Management
   - Commit code after implementing each feature with descriptive messages
   - Save spec updates in /specs/history after any behavioral change
   - Maintain clear mapping between specs and code commits

9. Review & Success Verification
   - Verify all five features work correctly in console
   - Ensure code matches specification without deviations
   - Confirm fo

## Response snapshot

Successfully generated comprehensive tasks.md for Todo CLI Core feature with 65 tasks organized across 9 phases:

**Phase Structure**:
1. **Phase 1: Setup** (T001-T006) - Project initialization and structure
2. **Phase 2: Foundational** (T007-T014) - Core models, storage, and service infrastructure (BLOCKS all user stories)
3. **Phase 3: User Story 1 - Add Tasks** (T015-T020) - P1, MVP critical
4. **Phase 4: User Story 2 - View Tasks** (T021-T026) - P1, MVP critical
5. **Phase 5: User Story 3 - Toggle Complete** (T027-T033) - P2
6. **Phase 6: User Story 4 - Update Tasks** (T034-T040) - P3
7. **Phase 7: User Story 5 - Delete Tasks** (T041-T046) - P3
8. **Phase 8: CLI Shell** (T047-T055) - REPL loop and command dispatcher
9. **Phase 9: Polish** (T056-T065) - Documentation, validation, code quality

**Key Design Decisions**:
- Tasks organized by user story to enable independent implementation and testing
- Each user story phase includes clear goal, independent test criteria, and acceptance scenarios
- Tests are NOT included (user input indicated implementation focus, not TDD)
- All tasks follow strict checklist format: - [ ] [ID] [P?] [Story?] Description with file path
- Foundational phase (Phase 2) clearly marked as blocking all user stories
- User stories can be implemented in parallel after foundation complete
- MVP scope clearly identified: Phases 1-4 + minimal Phase 8 (~30 tasks for US1 & US2)

**Parallel Opportunities**:
- Phase 1: 3 tasks can run in parallel
- Phase 2: Task model and Storage class can be built in parallel
- Phases 3-7: All user stories can be implemented in parallel by different developers
- Phase 9: 4 linting/validation tasks can run in parallel

**Implementation Strategies Provided**:
1. MVP First (US1 & US2 only) - minimal viable product
2. Incremental Delivery (add one story at a time) - recommended approach
3. Full Feature (all stories in parallel) - team-based approach

**Dependency Graph**:
- Clear phase dependencies documented
- User story independence verified (all depend only on Foundation, not each other)
- Within-story task sequences specified
- Parallel execution examples provided

File created at: C:\Users\affil\Desktop\todo-console-app\specs\001-todo-cli-core\tasks.md

## Outcome

- ✅ Impact: Generated actionable, dependency-ordered tasks.md with 65 tasks across 9 phases, organized by 5 user stories from spec.md
- 🧪 Tests: Tests not included per user input - focus on implementation tasks only
- 📁 Files: Created specs/001-todo-cli-core/tasks.md
- 🔁 Next prompts: User can now execute tasks sequentially or use /sp.implement to begin implementation; suggest starting with MVP (Phases 1-4)
- 🧠 Reflection: Successfully mapped all 5 user stories to independent, testable implementation phases; foundational phase correctly identified as blocking prerequisite; parallel opportunities clearly marked

## Evaluation notes (flywheel)

- Failure modes observed: None - all design documents were available and complete
- Graders run and results (PASS/FAIL): PASS - tasks follow strict checklist format, include file paths, organized by user story, clear dependencies
- Prompt variant (if applicable): Standard /sp.tasks workflow
- Next experiment (smallest change to try): Consider adding optional test tasks in future iterations if TDD is requested
