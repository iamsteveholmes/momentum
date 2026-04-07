Feature: Sprint Planning Synthesis-First — Lead with Recommendations Not Data Dumps

  Background:
    Given a project with a backlog containing stories in multiple epics
    And a sprint planning session is started

  Scenario: Recommendations appear before the full backlog
    When sprint planning presents its output
    Then the first content section is titled "Recommendations"
    And the full backlog appears in a later section
    And each recommendation includes a rationale explaining why the story matters now

  Scenario: Recommendations are limited to a focused shortlist
    When sprint planning presents its output
    Then the recommendations section contains between 3 and 5 stories
    And each recommendation shows the story priority, slug, and title

  Scenario: Stale stories are separated from recommendations
    Given a story with status "ready-for-dev" whose target files have recent commits
    When sprint planning presents its output
    Then that story does not appear in the recommendations section
    And a "Potentially stale" section lists the story with commit evidence

  Scenario: Stale evidence includes commit details
    Given a story with status "ready-for-dev" whose target files have recent commits
    When sprint planning presents its output
    Then the stale section entry for that story includes commit hashes and messages

  Scenario: Stories with satisfied dependencies are preferred
    Given a story whose dependencies are all completed
    And a story whose dependencies are still pending
    When sprint planning presents its output
    Then the story with satisfied dependencies appears in recommendations
    And the recommendation rationale mentions dependency readiness

  Scenario: Fallback when master plan documents are missing
    Given the master plan documents do not exist
    When sprint planning presents its output
    Then a warning indicates that recommendations require a master plan
    And the full backlog is presented as the primary content

  Scenario: Developer can still select stories after recommendations
    When sprint planning presents its output
    Then the output ends with a prompt to select stories for the sprint
