Feature: E2E validator — harness-driven, method-polymorphic execution

  As a developer,
  I want the e2e-validator to load a project harness and dispatch the right execution
  strategy by contract file type,
  so that it validates any project and change-type without hard-coded stack assumptions.

  Scenario: Validator reports BLOCKED when verification-harness.json is absent
    Given a sprint directory contains spec files ready for validation
    And no momentum/verification-harness.json file exists in the project root
    When the e2e-validator runs against the sprint
    Then it reports BLOCKED
    And the output states that momentum/verification-harness.json was not found
    And no scenario execution is attempted

  Scenario: Validator executes EDD eval strategy for an .eval.yaml contract
    Given verification-harness.json is present in the project root
    And the sprint specs directory contains a contract file with the .eval.yaml extension
    When the e2e-validator processes the sprint
    Then the validator applies the EDD eval execution strategy to that contract
    And the result is recorded as PASS or FAIL based on observable behavior

  Scenario: Validator applies human-review carve-out declared in the harness
    Given verification-harness.json declares a change-type in its human_review_carveouts list
    And a contract exists in the sprint specs directory for a story of that change-type
    When the e2e-validator processes the sprint
    Then that contract's scenario is marked MANUAL
    And no automated execution is attempted for that scenario

  Scenario: Existing Gherkin validation path produces no regressions
    Given verification-harness.json is present with default settings
    And the sprint specs directory contains only .feature contract files
    When the e2e-validator processes the sprint
    Then each .feature scenario is evaluated using the Gherkin execution strategy
    And the results match what the validator would have produced before this rewrite
