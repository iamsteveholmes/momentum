Feature: Sprint-planning frozen contracts, holistic coverage plan, and adversarial guard

  As a developer,
  I want sprint-planning to produce an immutable per-story verification contract,
  a sprint-wide coverage plan, and an adversarially-clean set of contracts,
  so that each story has an unambiguous spec-of-done before the sprint activates.

  Scenario: A contract file exists for every approved story after the contract step runs
    Given a sprint has five approved stories with different change types
    When sprint-planning completes the contract authoring phase
    Then one contract file exists in the sprint specs directory for each story
    And each contract file is named after its story slug with an extension matching the story's change type

  Scenario: Coverage plan lists every story exactly once
    Given a sprint has five stories and their contracts have been authored
    When sprint-planning produces the coverage-plan.md
    Then every story in the sprint appears exactly once in the plan
    And each story is marked either covered-by-composition or dedicated-run
    And the plan states the anti-redundancy principle as a header note

  Scenario: Adversarial guard flags an insider-knowledge clause and triggers a rewrite
    Given a drafted contract contains the clause "When sprint-planning delegates to the bmad-create-story subskill"
    When the adversarial guard reviews all drafted contracts
    Then that clause is flagged as failing the Outsider Test
    And sprint-planning rewrites the flagged clause to describe an observable outcome
    And the guard is re-run against the revised contract before the sprint proceeds

  Scenario: Sprint activation is blocked when contracts have not been authored
    Given a sprint has approved stories but the contract authoring phase has not run
    When sprint-planning attempts to activate the sprint
    Then activation does not proceed
    And the output identifies which stories are missing contract files
