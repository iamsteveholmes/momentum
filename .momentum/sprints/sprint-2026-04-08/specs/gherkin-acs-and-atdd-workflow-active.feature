Feature: Gherkin ACs and ATDD Workflow Active

  Background:
    Given a Momentum project with sprint planning and sprint-dev workflows configured

  Scenario: Generated specs describe behavior that an outsider can verify
    Given a story is selected for a sprint
    When the developer runs sprint planning
    Then each generated Gherkin scenario can be verified by invoking skills, running commands, and reading outputs
    And no scenario names reference AC numbers or internal implementation details

  Scenario: Malformed specs are caught and corrected before development begins
    Given sprint planning has generated Gherkin specs for a story
    When a generated scenario is missing a Given, When, or Then clause
    Then sprint planning surfaces the specific failing clause with an explanation
    And the spec is regenerated before the planning phase proceeds to team composition

  Scenario: Dev agents produce correct implementations without accessing spec files
    Given a sprint is in progress and Gherkin specs exist under the sprint specs directory
    When the dev agent begins implementing a story
    Then the implementation is complete and correct
    And the sprint specs directory files retain their original content unchanged

  Scenario: E2E Validator findings about untestable scenarios are tagged for future aggregation
    Given the E2E Validator runs against Gherkin specs during team review
    When a scenario is found to be untestable or fails the outsider test
    Then the finding appears in validator output with a spec-quality tag
