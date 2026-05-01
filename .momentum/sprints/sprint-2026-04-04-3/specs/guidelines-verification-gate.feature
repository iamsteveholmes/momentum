Feature: Guidelines Verification Gate — Sprint Planning Checks for Missing Guidelines

  Background:
    Given specialist agents have been assigned to stories in sprint planning Step 5
    And the guidelines verification gate is about to run

  Scenario: Gate passes silently when all specialist domains have guidelines
    Given every specialist domain assigned in this sprint has a matching rules file present
    When sprint planning Step 5 runs
    Then no warning output is produced for missing guidelines
    And no developer interaction is required before wave building begins

  Scenario: Gate detects a missing guidelines file for an assigned specialist
    Given a specialist domain is assigned to at least one story
    And no matching rules file exists in the project rules directory for that domain
    When sprint planning Step 5 runs
    Then a warning is shown naming the specialist domain and the affected story

  Scenario: Warnings for the same missing domain are consolidated across stories
    Given two or more stories share a specialist domain that has no guidelines
    When sprint planning Step 5 runs
    Then a single consolidated warning is shown for that domain
    And all affected stories are listed within that single warning

  Scenario: Developer is offered three options for each missing domain
    Given a missing guidelines domain has been detected
    When the warning is presented to the developer
    Then the developer is offered the option to generate guidelines now
    And the option to proceed without guidelines
    And the option to downgrade affected stories to the base dev agent

  Scenario: Choosing to generate guidelines completes before planning continues
    Given the developer selects the generate option for a missing domain
    When the guidelines generation skill completes
    Then sprint planning confirms the guidelines file now exists
    And sprint planning continues to wave building without further prompting about that domain

  Scenario: Choosing to proceed records the missing guidelines status
    Given the developer selects the proceed option for a missing domain
    When planning continues
    Then affected stories show a missing guidelines status in the sprint record
    And the specialist assignment for those stories is retained

  Scenario: Choosing to downgrade replaces the specialist with the base dev agent
    Given the developer selects the downgrade option for a missing domain
    When planning continues
    Then affected stories show the base dev agent in the team composition output
    And the sprint record reflects the base dev agent assignment for those stories

  Scenario: Guidelines status per story is recorded in the sprint record
    Given the verification gate has finished processing all specialist domains
    When the sprint record is written
    Then each story entry contains a guidelines status of present, missing, or skipped
    And stories assigned to the base dev agent with no specialist record a status of n/a
