Feature: Quick Fix Skill — Single-Story Tactical Workflow

  Background:
    Given the momentum practice module is installed

  Scenario: Skill starts immediately without an active sprint or Impetus
    Given no active sprint exists
    When the developer invokes "/momentum:quick-fix"
    Then the developer is prompted to describe the fix
    And no backlog is displayed
    And no story selection menu appears

  Scenario: Developer reviews and approves the story before specification begins
    Given the developer has described a fix and the story has been generated
    When the story is ready for review
    Then the story opens in a rendered surface for the developer to read
    And the workflow waits for explicit developer approval before proceeding
    And if the developer requests revisions, a revised story is generated and re-presented

  Scenario: Developer reviews and approves the Gherkin spec before implementation begins
    Given the story is approved
    When the Gherkin spec is generated
    Then the spec opens in a rendered surface for the developer to read
    And the workflow waits for explicit developer approval before creating the implementation branch
    And if the developer requests revisions, a revised spec is generated and re-presented

  Scenario: Workflow warns the developer when the current branch is not main
    Given the story and spec are both approved
    And the current branch is not "main"
    When implementation is about to begin
    Then the developer sees a warning that the current branch is not main
    And the developer is offered the choice to continue or switch branches first

  Scenario: Behavioral verification runs for a skill-instruction change
    Given implementation has completed and changes are on main
    And the story change type is "skill-instruction"
    When Phase 4 runs
    Then behavioral verification runs against the merged changes
    And any failures are surfaced to the developer before proceeding to Phase 5

  Scenario: Functional verification runs for a script-code change
    Given implementation has completed and changes are on main
    And the story change type is "script-code"
    When Phase 4 runs
    Then test coverage and functional verification runs against the merged changes
    And any failures are surfaced to the developer before proceeding to Phase 5

  Scenario: Both validators run and the dev agent fixes failures until clean
    Given implementation has completed and changes are on main
    And the story change type includes both "skill-instruction" and "script-code"
    When Phase 4 runs
    Then behavioral verification and functional verification both run
    And the dev agent addresses reported failures
    And verification reruns after each fix until all validators report clean or the developer halts

  Scenario: Developer is shown a push summary and asked to push at completion
    Given the full workflow has completed successfully
    When Phase 5 runs
    Then the developer sees a list of commits that will be pushed
    And the developer is asked whether to push
    And a quickfix record appears in sprints/index.json with a started date and a completed date

  Scenario: Workflow completes without multi-story or sprint lifecycle ceremony
    Given the developer completes the full quick-fix workflow
    Then no dependency graph was computed or displayed
    And no wave planning output was produced
    And no sprint activation or completion lifecycle was triggered
