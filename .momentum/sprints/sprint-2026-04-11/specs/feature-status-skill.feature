Feature: Feature Status Skill — HTML Planning Artifact with Coverage Gap Analysis

  Background:
    Given features.json exists at the canonical path with at least one feature entry
    And stories/index.json exists with current story statuses

  Scenario: Developer receives an HTML planning artifact when the skill runs
    When the developer invokes momentum:feature-status
    Then a self-contained HTML file is written to .claude/momentum/feature-status.html
    And a browser pane opens displaying the artifact
    And the file renders correctly when opened directly via file protocol

  Scenario: Features with insufficient story coverage are flagged as gaps
    Given a feature whose acceptance condition requires capabilities beyond what its assigned stories deliver
    When the developer invokes momentum:feature-status
    Then that feature displays a GAP indicator in the HTML output
    And the expanded detail for that feature names what the acceptance condition requires that the stories do not cover
    And that feature appears at the top of its type group

  Scenario: A cache file is written after every skill run
    When the developer invokes momentum:feature-status
    Then .claude/momentum/feature-status.md is written or updated
    And the file contains a summary in the form of feature counts for working partial not-started and gap categories

  Scenario: Missing features.json produces a clear actionable error
    Given features.json does not exist
    When the developer invokes momentum:feature-status
    Then the skill reports that features.json was not found
    And the skill tells the developer which story to run to create it
