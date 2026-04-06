Feature: Add Priority to All Story Index Entries

  Background:
    Given the momentum workspace is configured
    And stories exist in stories/index.json

  Scenario: Stories in the index carry a priority level
    When the developer runs "sprint stories"
    Then every story in the output displays a priority indicator

  Scenario: Newly added story defaults to low priority
    When the developer adds a new story to the sprint
    And the developer runs "sprint stories"
    Then the new story shows a priority of "low"

  Scenario: Setting priority on a story succeeds
    Given a story with slug "add-login" exists in the sprint
    When the developer runs "sprint set-priority --story add-login --priority high"
    Then the output is valid JSON
    And the JSON contains an "old" field with the previous priority
    And the JSON contains a "new" field with "high"

  Scenario: Priority change is reflected in subsequent story listings
    Given a story with slug "add-login" exists in the sprint
    And the developer has run "sprint set-priority --story add-login --priority critical"
    When the developer runs "sprint stories"
    Then the story "add-login" displays a priority of "critical"

  Scenario: Setting an invalid priority level fails gracefully
    Given a story with slug "add-login" exists in the sprint
    When the developer runs "sprint set-priority --story add-login --priority urgent"
    Then the command exits with a non-zero status
    And the output contains an error message indicating valid priority levels

  Scenario: Setting priority on a non-existent story fails gracefully
    When the developer runs "sprint set-priority --story no-such-story --priority high"
    Then the command exits with a non-zero status
    And the output contains an error message indicating the story was not found

  Scenario: Filtering stories by a specific priority level
    Given stories exist at multiple priority levels including "medium"
    When the developer runs "sprint stories --priority medium"
    Then only stories with priority "medium" appear in the output
    And stories with other priority levels do not appear

  Scenario: Requesting all stories grouped by priority
    Given stories exist at multiple priority levels
    When the developer runs "sprint stories --priority all"
    Then the output groups stories under priority headings
    And each group contains only stories matching that priority level

  Scenario: Sprint planning displays priority indicators
    Given stories exist at multiple priority levels
    When the developer runs the sprint-planning skill through step one
    Then each story in the planning display shows a priority indicator using [C], [H], [M], or [L]

  Scenario: Sprint planning lists higher-priority stories before lower-priority ones
    Given a story with slug "low-task" exists with priority "low"
    And a story with slug "critical-task" exists with priority "critical"
    When the developer runs the sprint-planning skill through step one
    Then "critical-task" appears before "low-task" in the planning output

  Scenario: All four priority levels are accepted by the set-priority command
    Given a story with slug "sample-story" exists in the sprint
    When the developer runs "sprint set-priority --story sample-story --priority critical"
    Then the command exits successfully
    When the developer runs "sprint set-priority --story sample-story --priority high"
    Then the command exits successfully
    When the developer runs "sprint set-priority --story sample-story --priority medium"
    Then the command exits successfully
    When the developer runs "sprint set-priority --story sample-story --priority low"
    Then the command exits successfully
