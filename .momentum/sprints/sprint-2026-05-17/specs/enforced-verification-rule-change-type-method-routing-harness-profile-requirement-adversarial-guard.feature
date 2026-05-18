Feature: Enforced verification standard rule

  As a developer using Momentum,
  I want a verification rule that routes by change-type, mandates a harness profile,
  and blocks insider-knowledge shortcuts,
  so that the verification pipeline is actively enforced rather than advisory.

  Scenario: Story produced by create-story carries a routed verification method
    Given a story stub with change-type skill-instruction
    When create-story processes the stub into a ready-for-dev story
    Then the story file contains a verification_method field in its YAML frontmatter
    And the verification_method value matches the method mapped to skill-instruction in the routing table

  Scenario: Verification is non-compliant when no harness profile is declared
    Given a story is marked ready-for-dev with no harness_profile field declared
    When the verification pipeline evaluates the story
    Then the verification is reported as non-compliant
    And the reported reason states that a harness profile declaration is required

  Scenario: Adversarial guard rejects a contract clause that requires source code knowledge
    Given a verification contract contains the clause "When sprint-planning delegates to the bmad-create-story subskill"
    When the adversarial guard evaluates the contract
    Then the guard flags that clause as failing the Outsider Test
    And the output identifies implementation knowledge as the reason for failure

  Scenario: The acceptance-testing-standard document forwards readers to the new rule
    Given the file docs/process/acceptance-testing-standard.md is opened
    When its contents are read
    Then the document shows a Status of Retired
    And it contains a forwarding note pointing to DEC-029 and to skills/momentum/references/rules/verification-standard.md
