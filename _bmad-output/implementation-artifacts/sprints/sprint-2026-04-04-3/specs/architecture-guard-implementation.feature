Feature: Architecture Guard Implementation — Replace Stub with Real Agent Definition

  Background:
    Given an architecture decisions document exists for the project
    And the sprint-dev workflow is executing the Team Review phase

  Scenario: Architecture guard produces findings when decisions are violated
    Given the architecture guard agent is spawned with an architecture document path and a set of sprint changes
    When the agent performs its review
    Then it produces one or more findings for changes that violate architectural decisions
    And each finding identifies the decision violated, the file or pattern involved, evidence from the change, and a severity level
    And severity levels are drawn from CRITICAL, HIGH, MEDIUM, and LOW

  Scenario: Architecture guard produces no findings for non-architectural issues
    Given a sprint change that has code style issues but no architecture violations
    When the architecture guard reviews that change
    Then it produces no findings
    And the overall verdict indicates no architectural violations were found

  Scenario: Architecture guard report follows the team review output format
    Given the architecture guard has completed its review
    When the report is produced
    Then it has a header identifying the sprint and the overall verdict
    And findings are grouped by severity
    And it ends with a summary section

  Scenario: Sprint-dev Team Review spawns the architecture guard via the Agent tool
    Given Phase 5 of sprint-dev is running Team Review
    When the architecture guard is launched
    Then it is spawned via the Agent tool using the architecture guard agent definition file
    And it receives the sprint slug, sprint branch, architecture document path, and list of touched files

  Scenario: Architecture guard does not modify any files during review
    Given the architecture guard agent is active during a review
    When it performs its analysis
    Then it does not modify any source files, story files, or architecture documents

  Scenario: Architecture guard SKILL.md works for standalone ad-hoc invocations
    Given a developer invokes the architecture guard skill directly outside of a sprint
    When the skill is executed
    Then it performs the same architecture review logic as the agent definition
    And no placeholder or stub text appears in the output
