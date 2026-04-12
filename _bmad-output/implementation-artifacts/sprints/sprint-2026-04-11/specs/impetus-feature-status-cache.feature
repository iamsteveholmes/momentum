Feature: Impetus Feature Status Cache — Hash-Based Staleness Detection in Greeting

  Background:
    Given the Impetus skill is installed and functional

  Scenario: Greeting shows cached feature status when features and stories are unchanged
    Given features.json exists and momentum:feature-status has been run at least once
    And neither features.json nor stories/index.json has changed since that run
    When the developer starts a new session and Impetus greets them
    Then the greeting displays the feature status summary
    And no staleness indicator appears in the greeting

  Scenario: Greeting flags stale cache when inputs have changed since last run
    Given features.json exists and momentum:feature-status has been run at least once
    And features.json or stories/index.json has changed since that run
    When the developer starts a new session and Impetus greets them
    Then the greeting displays the cached summary with a staleness indicator
    And the greeting suggests running feature-status to refresh

  Scenario: Greeting prompts to plan features when no features artifact exists
    Given features.json does not exist in the project
    When the developer starts a new session and Impetus greets them
    Then the greeting prompts the developer to plan features

  Scenario: Greeting prompts to generate feature status when cache has never been created
    Given features.json exists but momentum:feature-status has never been run
    When the developer starts a new session and Impetus greets them
    Then the greeting prompts the developer to run feature-status

