Feature: momentum-dev Simplified Executor
  The momentum-dev skill operates as a pure executor: worktree setup,
  bmad-dev-story delegation, agent logging, and merge-ready output.
  It does not invoke AVFL, manage sprint status, or run DoD checks.

  Background:
    Given a project with momentum-dev skill installed
    And stories/index.json contains at least one story with status "ready-for-dev"
    And all dependencies for that story have status "done"

  # --- AVFL Removal ---

  Scenario: No AVFL invocation during story execution
    Given the user invokes momentum-dev for a story
    When bmad-dev-story completes successfully
    Then momentum-dev does not invoke momentum-avfl
    And momentum-dev does not reference AVFL profiles or domain experts
    And no AVFL result is written to the story's Dev Agent Record

  Scenario: Workflow contains no AVFL step
    Given the momentum-dev workflow.md file
    When a verifier inspects the workflow steps
    Then no step mentions "AVFL", "momentum-avfl", or "avfl_profile"
    And no step mentions "GATE_FAILED" or "CHECKPOINT_WARNING"
    And no critical directive references AVFL changeset validation

  # --- Sprint Status Removal ---

  Scenario: No status transition calls during execution
    Given the user invokes momentum-dev for a story
    When momentum-dev executes from start to completion
    Then momentum-dev does not call "momentum-tools.py sprint status-transition"
    And momentum-dev does not write to stories/index.json status fields
    And no step transitions the story to "in-progress", "review", or "done"

  Scenario: Lock file still created without status transition
    Given the user invokes momentum-dev for story "example-story"
    When momentum-dev reaches the in-progress step
    Then a lock file is created at ".worktrees/story-example-story.lock"
    And the lock file contains a session timestamp
    But no status-transition command is executed

  # --- DoD and Code Review Removal ---

  Scenario: No Momentum DoD supplement step
    Given the momentum-dev workflow.md file
    When a verifier inspects the workflow steps
    Then no step references "Momentum-specific DoD" or "dod-checklist.md"
    And no step checks for eval files, SKILL.md size, or skill name prefixes
    And no step loads "./references/dod-checklist.md"

  Scenario: No code review offer
    Given the user invokes momentum-dev for a story
    When momentum-dev completes and proposes merge
    Then momentum-dev does not offer bmad-code-review
    And no step asks about reviewing script changes

  # --- Agent Logging ---

  Scenario: Log emitted on story selection
    Given the user invokes momentum-dev without an explicit story path
    When momentum-dev selects story "feature-x" from the index
    Then a log call is made with --agent dev --story feature-x --event decision
    And the detail mentions story selection

  Scenario: Log emitted on worktree creation
    Given momentum-dev creates a worktree for story "feature-x"
    When the worktree is created successfully
    Then a log call is made with --agent dev --story feature-x --event decision
    And the detail mentions worktree creation

  Scenario: Log emitted on implementation start
    Given momentum-dev is about to invoke bmad-dev-story
    When the invocation begins
    Then a log call is made with --agent dev --event decision
    And the detail mentions starting implementation via bmad-dev-story

  Scenario: Log emitted on implementation complete
    Given bmad-dev-story has completed for story "feature-x"
    When momentum-dev captures the file list and completion output
    Then a log call is made with --agent dev --story feature-x --event decision
    And the detail includes the file list or file count

  Scenario: Log emitted on merge proposal
    Given momentum-dev proposes merging story/feature-x into main
    When the merge proposal is presented to the user
    Then a log call is made with --agent dev --story feature-x --event decision
    And the detail mentions the merge proposal and target branch

  Scenario: Error logged on stale branch discovery
    Given branch "story/feature-x" exists without a corresponding worktree
    When momentum-dev detects the stale branch during crash recovery
    Then a log call is made with --agent dev --story feature-x --event error
    And the detail mentions the stale branch cleanup

  Scenario: Error logged on merge conflict
    Given momentum-dev attempts to merge story/feature-x into main
    When the merge reports conflicts
    Then a log call is made with --agent dev --story feature-x --event error
    And the detail mentions the merge conflict

  Scenario: Log calls use correct format
    Given any momentum-dev log call
    When the call is executed
    Then the command format is "momentum-tools log --agent dev --story <slug> --event <type> --detail <message>"
    And the event type is one of: decision, error, retry, assumption, finding, ambiguity

  Scenario: Log failure does not block execution
    Given momentum-tools log command is unavailable or fails
    When momentum-dev attempts to write a log entry
    Then the log failure is silently ignored
    And momentum-dev continues with the next workflow step

  # --- Preserved Behavior ---

  Scenario: Worktree lifecycle unchanged
    Given the user invokes momentum-dev for story "feature-x"
    When momentum-dev executes the full workflow
    Then a worktree is created at ".worktrees/story-feature-x"
    And bmad-dev-story runs inside the worktree context
    And after merge, the worktree is removed
    And the story branch is deleted

  Scenario: Crash recovery still functional
    Given branch "story/feature-x" and worktree ".worktrees/story-feature-x" both exist
    When the user invokes momentum-dev for story "feature-x"
    Then momentum-dev offers Resume or Clean up options
    And choosing Resume continues in the existing worktree
    And choosing Clean up removes the worktree and branch before recreating

  Scenario: Merge gate requires user confirmation
    Given momentum-dev has completed implementation for a story
    When the merge proposal is presented
    Then momentum-dev waits for explicit user confirmation
    And does not auto-execute the merge
    And displays the target branch, story branch, and touches overlap summary

  Scenario: Completion signal emitted
    Given momentum-dev completes a story and merge succeeds
    When the final output is generated
    Then a structured JSON completion signal is emitted
    And it contains "status", "result.files_modified", "result.tests_run", and "result.test_result"
    And "status" is "complete"

  Scenario: Standalone invocation works without sprint context
    Given no active sprint exists in sprints/index.json
    And stories/index.json has a ready-for-dev story
    When the user invokes momentum-dev directly
    Then momentum-dev selects and implements the story normally
    And log calls that reference sprint context degrade gracefully
    And no error is thrown about missing sprint data

  # --- Step Structure ---

  Scenario: Workflow has correct step count after simplification
    Given the momentum-dev workflow.md file
    When a verifier counts the workflow steps
    Then the workflow contains exactly 7 steps
    And the steps cover: branch capture, story resolution, crash recovery,
        worktree creation, lock file, bmad-dev-story invocation, merge and cleanup
