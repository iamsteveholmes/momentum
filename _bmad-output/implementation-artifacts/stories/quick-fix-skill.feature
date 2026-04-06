Feature: Quick Fix Skill — Single-Story Tactical Workflow

  Background:
    Given the momentum practice module is installed
    And stories/index.json is accessible

  # AC 1: /momentum:quick-fix is independently invocable — does not require Impetus or an active sprint

  Scenario: Skill starts Phase 1 when invoked directly without Impetus
    Given no active sprint exists
    And Impetus is not running
    When the developer invokes "/momentum:quick-fix"
    Then the skill begins Phase 1 (Define) without error
    And the developer is prompted to describe the fix

  # AC 2: Phase 1 creates a story from the user's prompt, registers it, and opens it for review

  Scenario: Phase 1 creates a story and surfaces it for developer review
    Given the developer invokes "/momentum:quick-fix"
    When the developer provides a description of the fix and an epic slug
    Then a story file is created under the implementation artifacts directory
    And the story slug is registered in stories/index.json
    And the story spec opens in a markdown review surface for the developer
    And the developer can approve or request revisions before proceeding

  Scenario: Phase 1 allows the developer to revise the story before approval
    Given the developer has described a fix and a story draft has been generated
    When the developer requests revisions to the story
    Then a revised story draft is presented
    And the developer can approve or request further revisions

  # AC 3 (behavioral portion only): Phase 2 generates a Gherkin .feature file and surfaces it for review
  # Internals (which tool generated Gherkin, AVFL invocation mechanism) are QA concerns — not tested here

  Scenario: Phase 2 produces a Gherkin spec and surfaces it for developer review
    Given Phase 1 is complete and the story is approved
    When Phase 2 (Specify) runs
    Then a Gherkin .feature file exists for the story
    And the Gherkin spec opens in a markdown review surface for the developer
    And the developer can approve or request revisions before implementation begins

  # AC 4 (cmux surfaces open during review — observable via AC 2 and AC 3 scenarios above)
  # Already covered: story spec and Gherkin spec both open in review surfaces (see Phase 1 and Phase 2 scenarios)

  # AC 5: Phase 3 creates a worktree off main, warns if not on main, merges on completion

  Scenario: Phase 3 creates a worktree from main when already on main
    Given Phase 2 is complete and the Gherkin spec is approved
    And the current branch is "main"
    When Phase 3 (Implement) begins
    Then a worktree is created branching from main
    And a specialist dev agent runs implementation in that worktree
    And on completion the worktree changes are merged to main
    And no worktree artifacts remain after merge

  Scenario: Phase 3 warns the developer when not on main and offers a choice
    Given Phase 2 is complete and the Gherkin spec is approved
    And the current branch is not "main"
    When Phase 3 (Implement) begins
    Then the developer sees a warning that the current branch is not main
    And the developer is offered the choice to continue from main or switch branches first
    And if the developer chooses to continue, a worktree is created from main regardless of current branch

  # AC 6 (Phase 4 validation loop — observable portion): validators run and findings are reported
  # Internals (TeamCreate setup, task list collaboration mechanism) are QA concerns — not tested here

  Scenario: Phase 4 runs validation and surfaces findings for the dev agent to fix
    Given Phase 3 is complete and changes are merged to main
    When Phase 4 (Validate) runs
    Then validation agents run against the merged changes
    And any validation failures are reported to the developer
    And the dev agent addresses reported failures
    And validation reruns after fixes until the result is clean or the developer halts

  Scenario: Phase 4 runs E2E Validator for skill-instruction change type
    Given the story change_type includes "skill-instruction"
    When Phase 4 (Validate) runs
    Then behavioral verification runs against the Gherkin spec
    And the validation result is reported before proceeding to Phase 5

  Scenario: Phase 4 runs QA for script-code change type
    Given the story change_type includes "script-code"
    When Phase 4 (Validate) runs
    Then test coverage and functional verification runs
    And the validation result is reported before proceeding to Phase 5

  Scenario: Phase 4 runs both E2E Validator and QA when both change types are present
    Given the story change_type includes both "skill-instruction" and "script-code"
    When Phase 4 (Validate) runs
    Then both behavioral verification and functional verification run
    And both validation results are reported before proceeding to Phase 5

  # AC 7: Phase 5 merges to main and shows push summary

  Scenario: Phase 5 shows push summary and asks to push
    Given Phase 4 validation is clean
    When Phase 5 (Ship) runs
    Then the developer sees a list of commits that will be pushed
    And the developer is asked whether to push
    And if confirmed, the commits are pushed to the remote

  # AC 8: Workflow never presents backlog, multiple stories, waves, dependency graphs, or sprint activation

  Scenario: Workflow completes without presenting backlog or multi-story ceremony
    Given the developer invokes "/momentum:quick-fix" and completes the full workflow
    Then no backlog is displayed at any point
    And no story selection menu is displayed
    And no dependency graph is computed or shown
    And no wave planning output is produced
    And no sprint activation or sprint completion lifecycle is triggered

  # AC 9: Lightweight quickfix entry is registered in sprints/index.json

  Scenario: A quickfix entry is recorded in sprints/index.json on completion
    Given the developer has completed the full quick-fix workflow for a story
    When Phase 5 (Ship) completes
    Then sprints/index.json contains an entry for this quickfix
    And the entry includes the quickfix slug, the story key, a started date, and a completed date
    And no sprint activation or sprint complete lifecycle fields are present on the entry
