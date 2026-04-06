Feature: Quick Fix Skill — Single-Story Tactical Workflow

  Background:
    Given the momentum practice module is installed

  Scenario: Developer completes a quick fix from description to push
    Given the developer invokes "/momentum:quick-fix" without an active sprint
    When the developer describes the fix and approves the generated story
    And the developer approves the generated Gherkin spec
    And the dev agent implements the fix and the changes merge to main
    And validation passes cleanly
    Then the developer sees a list of commits that will be pushed
    And the developer is asked whether to push
    And a quickfix record appears in sprints/index.json with a started date and a completed date

  Scenario: Skill starts immediately without Impetus or an active sprint
    Given no active sprint exists and Impetus is not running
    When the developer invokes "/momentum:quick-fix"
    Then Phase 1 begins and the developer is prompted to describe the fix
    And no backlog is displayed
    And no story selection menu appears

  Scenario: Phase 1 presents the story for review before proceeding
    Given the developer has described a fix
    When the story is generated
    Then the story opens in a rendered markdown surface for the developer to read
    And the workflow waits for explicit approval before moving to Phase 2

  Scenario: Developer requests revisions to the story before approving
    Given the story has been generated and is open for review
    When the developer requests revisions
    Then a revised story is generated and opened in the review surface
    And the workflow again waits for explicit approval before proceeding

  Scenario: Phase 2 presents the Gherkin spec for review before implementation
    Given the story is approved
    When Phase 2 runs and the Gherkin spec is generated
    Then the spec opens in a rendered markdown surface for the developer to read
    And the workflow waits for explicit approval before creating the worktree

  Scenario: Developer requests revisions to the Gherkin spec before approving
    Given the Gherkin spec has been generated and is open for review
    When the developer requests revisions
    Then a revised spec is generated and opened in the review surface
    And the workflow again waits for explicit approval before proceeding

  Scenario: Phase 3 creates a worktree from main when the current branch is main
    Given the story and Gherkin spec are both approved
    And the current branch is "main"
    When Phase 3 begins
    Then implementation runs in a worktree branched from main
    And the changes are merged to main on completion
    And no worktree artifacts remain after the merge

  Scenario: Phase 3 warns when the developer is not on main and offers a choice
    Given the story and Gherkin spec are both approved
    And the current branch is not "main"
    When Phase 3 begins
    Then the developer sees a warning that the current branch is not main
    And the developer is offered the choice to continue or switch branches first
    And if the developer chooses to continue, the worktree branches from main regardless of the current branch

  Scenario: Phase 4 runs behavioral verification for a skill-instruction change
    Given the changes have merged to main
    And the story change type includes "skill-instruction"
    When Phase 4 runs
    Then behavioral verification runs against the merged changes
    And any failures are reported to the developer before Phase 5 begins

  Scenario: Phase 4 runs functional verification for a script-code change
    Given the changes have merged to main
    And the story change type includes "script-code"
    When Phase 4 runs
    Then test coverage and functional verification runs against the merged changes
    And any failures are reported to the developer before Phase 5 begins

  Scenario: Phase 4 runs both validators when the story has mixed change types
    Given the changes have merged to main
    And the story change type includes both "skill-instruction" and "script-code"
    When Phase 4 runs
    Then both behavioral verification and functional verification run
    And the dev agent addresses any reported failures
    And validation reruns after each fix until all validators report clean or the developer halts

  Scenario: Workflow completes without multi-story or sprint ceremony
    Given the developer completes the full quick-fix workflow
    Then no backlog was displayed at any point
    And no dependency graph was computed or shown
    And no wave planning output was produced
    And no sprint activation or completion lifecycle was triggered
    And the quickfix record in sprints/index.json does not contain sprint activation fields
