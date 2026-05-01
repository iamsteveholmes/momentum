Feature: E2E Validator Pre-loads SendMessage Schema Before Reporting

  Scenario: E2E validator sends report without schema error
    Given an E2E validator agent has been spawned for a story
    And the agent has completed its validation
    When the agent sends its validation report
    Then the report is delivered successfully on the first attempt
    And no InputValidationError occurs for SendMessage

  Scenario: E2E validator loads SendMessage schema proactively
    Given an E2E validator agent has been spawned for a story
    And the agent has completed its validation
    When the agent prepares to return its results
    Then the agent calls ToolSearch to load the SendMessage schema
    And the agent sends its report after the schema is loaded
