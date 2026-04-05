Feature: Guidelines Verification Gate — Sprint Planning Checks for Missing Guidelines

  Background:
    Given specialist agents have been assigned to stories in sprint planning Step 5
    And the guidelines verification gate is about to run

  Scenario: Gate passes silently when all specialist domains have guidelines
    Given every specialist domain assigned in this sprint has a matching rules file present
    When the verification gate runs
    Then it produces no output and no developer interaction is required
    And planning continues to wave building without interruption

  Scenario: Gate detects a missing guidelines file for an assigned specialist
    Given a specialist domain is assigned to at least one story
    And no matching rules file exists in the project rules directory for that domain
    When the verification gate runs
    Then a warning is surfaced naming the specialist domain and the affected story

  Scenario: Warnings for the same missing domain are consolidated across stories
    Given two or more stories share a specialist domain that has no guidelines
    When the verification gate runs
    Then a single consolidated warning is shown for that domain
    And all affected stories are listed within that single warning

  Scenario: Developer is offered three options for each missing domain
    Given a missing guidelines domain has been detected
    When the warning is presented to the developer
    Then the developer is offered the option to generate guidelines now
    And the option to proceed without guidelines
    And the option to downgrade affected stories to the base dev agent

  Scenario: Choosing to generate guidelines pauses planning until generation completes
    Given the developer selects the generate option for a missing domain
    When the guidelines generation skill runs
    Then sprint planning waits for it to complete
    And after completion the gate re-checks that guidelines now exist
    And planning resumes from where it paused

  Scenario: Choosing to proceed records the missing guidelines status
    Given the developer selects the proceed option for a missing domain
    When planning continues
    Then affected stories are recorded as having missing guidelines in the sprint record
    And the specialist assignment is retained

  Scenario: Choosing to downgrade replaces the specialist with the base dev agent
    Given the developer selects the downgrade option for a missing domain
    When planning continues
    Then affected stories have their specialist assignment replaced with the base dev agent
    And the sprint record reflects the downgrade

  Scenario: Guidelines status per story is recorded in the sprint record
    Given the verification gate has finished processing all specialist domains
    When the sprint record is written
    Then each story entry contains a guidelines status of present, missing, or skipped
    And stories assigned to the base dev agent with no specialist record a status of n/a
