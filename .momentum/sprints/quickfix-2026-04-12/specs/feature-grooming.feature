Feature: Feature Grooming Skill — Holistic Feature Taxonomy Discovery and Refinement

  Background:
    Given the developer is in a Momentum-managed project

  Scenario: Skill announces mode and presents synthesis covering both product and architecture sources
    Given no features.json exists in the project's planning artifacts
    When the developer invokes momentum:feature-grooming
    Then the skill announces "bootstrap" mode before any analysis output appears
    And the synthesis output references content drawn from both the PRD and epics as well as the architecture and stories
    And between 8 and 25 candidate features are presented
    And a warning indicator appears if the candidate count falls outside the 8 to 25 range
    And each candidate includes a multi-paragraph value description covering current value, future vision, and known gaps
    And each candidate includes a system context description explaining how it fits the overall product

  Scenario: Candidate set is shown in full with value detail before any per-feature gate is opened
    Given no features.json exists in the project's planning artifacts
    When the developer invokes momentum:feature-grooming
    Then all candidate features with their value descriptions and system context descriptions appear in a single holistic presentation
    And three review questions appear after the full candidate set — asking about coverage, value accuracy, and deferred-value confirmation
    And no approval prompt requesting a write decision appears before the holistic review questions

  Scenario: Features marked as deferred-value require explicit developer confirmation before inclusion
    Given no features.json exists in the project's planning artifacts
    And the synthesized candidates include at least one feature with no current delivery
    When the developer invokes momentum:feature-grooming
    Then each feature with no current delivery is marked with a warning indicator in the candidate presentation
    And the developer is asked to explicitly confirm each such feature before the approval gate is reached

  Scenario: features.json is not written when the developer does not confirm the approval gate
    Given no features.json exists in the project's planning artifacts
    When the developer invokes momentum:feature-grooming
    And the developer does not provide confirmation at the approval gate
    Then features.json does not exist after the skill exits

  Scenario: Post-write output includes a hash and reports any unmapped stories
    Given a Momentum-managed project with an existing features.json and a set of stories
    And at least one non-dropped non-done story is not assigned to any feature
    When the developer invokes momentum:feature-grooming and confirms the approval gate
    Then the skill's final output includes a hash string for the written features
    And the final output reports the count and identifiers of stories not assigned to any feature

  Scenario: Bootstrap run produces foundation documents and a conventional commit before completing
    Given no features.json exists in the project's planning artifacts
    When the developer invokes momentum:feature-grooming and confirms the approval gate
    Then a value gap assessment document is present in the project's assessments directory
    And a value-first schema decision document is present in the project's decisions directory
    And a commit exists with a message matching the pattern "docs(features): feature-grooming bootstrap — N features, M proposals applied"

  Scenario: Discovery phase uses exactly two parallel subagents before any synthesis output is shown
    Given no features.json exists in the project's planning artifacts
    When the developer invokes momentum:feature-grooming
    Then the mode announcement appears before any synthesis content
    And the synthesis output contains evidence that the PRD and epics source contributed candidates
    And the synthesis output contains evidence that the architecture and stories source contributed candidates
    And no additional discovery subagents are spawned beyond the initial two

  Scenario: Refine mode reports all six signal types including zero counts
    Given a Momentum-managed project with an existing features.json
    When the developer invokes momentum:feature-grooming
    Then the refine report includes a MERGE signal with a count
    And the refine report includes a SPLIT signal with a count
    And the refine report includes a DEDUP signal with a count
    And the refine report includes a NEW signal with a count
    And the refine report includes a RETIRE signal with a count
    And the refine report includes an UPDATE signal with a count
    And signals with zero detected changes show a count of zero rather than being omitted
