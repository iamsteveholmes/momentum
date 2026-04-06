Feature: Epic Grooming — Holistic Epic Taxonomy and Story Organization

  Background:
    Given the momentum workspace has stories with various epic slugs assigned
    And epics.md contains a registered set of epic definitions
    And some stories reference epic slugs that are not registered in epics.md

  Scenario: Skill is independently invocable and enters data collection
    When the developer invokes epic-grooming
    Then the skill starts without errors
    And the skill enters the data collection phase
    And the skill outputs the set of epic slugs found in stories/index.json

  Scenario: Skill surfaces orphaned and unregistered epic slugs before proposing changes
    When the developer invokes epic-grooming
    Then the skill outputs a list of story epic slugs that have no matching entry in epics.md
    And the skill does not modify any files at this stage

  Scenario: Skill proposes a revised taxonomy with rationale before making any changes
    When the developer invokes epic-grooming
    Then the skill outputs a proposed epic taxonomy
    And each proposed change includes a stated rationale
    And the skill prompts the developer for approval before proceeding
    And no stories are reassigned until the developer responds

  Scenario: Skill does not mutate state when developer declines the proposal
    Given the skill has presented a proposed taxonomy and is awaiting approval
    When the developer rejects the proposal
    Then epics.md is not modified
    And no story epic assignments are changed
    And the skill exits without making any mutations

  Scenario: Skill updates epics and reassigns stories after developer approves
    Given the skill has presented a proposed taxonomy and is awaiting approval
    When the developer approves the proposal
    Then epics.md is updated to reflect the approved taxonomy
    And each story that referenced a renamed or reorganized slug is updated to the new slug

  Scenario: Skill logs taxonomy decisions after approval and execution
    Given the skill has presented a proposed taxonomy and is awaiting approval
    When the developer approves the proposal
    And the skill completes its reassignment work
    Then a log entry is written recording each taxonomy decision that was applied
    And the log captures which slugs were added, removed, or renamed
    And the log captures which stories were reassigned and to which epic
