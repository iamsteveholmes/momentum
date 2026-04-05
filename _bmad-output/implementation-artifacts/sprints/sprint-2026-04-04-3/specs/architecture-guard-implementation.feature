Feature: Architecture Guard Implementation — Replace Stub with Real Agent Definition

  Background:
    Given an architecture decisions document exists for the project
    And the sprint-dev workflow is executing the Team Review phase

  Scenario: Architecture guard reads and extracts decisions from the architecture document
    Given the architecture guard agent is spawned with an architecture document path
    When the agent begins its review
    Then it reads the architecture document
    And it builds a checklist of the key decisions it will check against

  Scenario: Architecture guard analyzes sprint changes against extracted decisions
    Given the architecture guard has extracted decisions from the architecture document
    And a set of sprint changes is provided
    When the agent performs its analysis
    Then it checks each changed file or pattern against the decision checklist
    And it identifies any places where changes do not honor a decision

  Scenario: Architecture guard produces structured findings with required fields
    Given the architecture guard has completed its analysis
    When it produces its output
    Then each finding contains the decision that was violated, the file or pattern involved, evidence from the change, and a severity level
    And severity levels are drawn from CRITICAL, HIGH, MEDIUM, and LOW

  Scenario: Architecture guard report follows the team review output format
    Given the architecture guard has completed its review
    When the report is produced
    Then it has a header identifying the sprint and the overall verdict
    And findings are grouped by severity
    And it ends with a summary section

  Scenario: Architecture guard focuses only on architectural decisions, not code quality
    Given a sprint change that has code style issues but no architecture violations
    When the architecture guard reviews that change
    Then it produces no findings for the style issues
    And it only flags violations of structural decisions, naming conventions, or separation-of-concerns rules

  Scenario: Sprint-dev Team Review spawns the architecture guard via the Agent tool
    Given Phase 5 of sprint-dev is running Team Review
    When the architecture guard is launched
    Then it is spawned via the Agent tool using the architecture guard agent definition file
    And it receives the sprint slug, sprint branch, architecture document path, and list of touched files

  Scenario: Architecture guard SKILL.md works for standalone ad-hoc invocations
    Given a developer invokes the architecture guard skill directly outside of a sprint
    When the skill is executed
    Then it performs the same architecture review logic as the agent definition
    And no placeholder or stub text appears in the output

  Scenario: Architecture guard agent definition is read-only
    Given the architecture guard agent is active during a review
    When it performs its analysis
    Then it does not modify any source files, story files, or architecture documents
