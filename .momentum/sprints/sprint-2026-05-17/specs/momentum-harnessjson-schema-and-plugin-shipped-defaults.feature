Feature: momentum/verification-harness.json schema and plugin-shipped defaults

  As a developer using Momentum on any project,
  I want a verification-harness.json file that ships with safe opt-in defaults
  and accepts project-level overrides,
  so that the e2e-validator can determine execution surfaces and drivers
  without hard-coded stack assumptions.

  Scenario: Plugin ships verification-harness.json alongside agents.json with required top-level structure
    Given the Momentum plugin is installed in a project
    When the file momentum/verification-harness.json is read
    Then it contains a top-level "defaults" object
    And it contains a top-level "project" array that is empty

  Scenario: Plugin defaults opt all surfaces out until a project overrides them
    Given verification-harness.json has only plugin-shipped defaults and no project entries
    When the e2e-validator reads the execution_surfaces section
    Then every change-type surface entry resolves to "skip"
    And no execution driver reports itself as enabled

  Scenario: Running agent-builder for a new agent adds a project entry without removing existing ones
    Given verification-harness.json already contains one entry in the project array
    When agent-builder runs and creates a new agent not already present in the project array
    Then verification-harness.json contains two entries in the project array
    And the previously existing entry is unchanged

  Scenario: Running agent-guidelines leaves an existing project entry untouched
    Given verification-harness.json contains a project entry for a specific agent role
    When agent-guidelines runs for that same role
    Then verification-harness.json still contains exactly one entry for that role
    And the entry content is identical to what was present before
