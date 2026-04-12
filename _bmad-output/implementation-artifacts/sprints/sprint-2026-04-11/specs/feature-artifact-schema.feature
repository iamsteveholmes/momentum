Feature: Feature Artifact Schema — Define features.json and Populate Initial Instances

  Background:
    Given the feature-artifact-schema story has been implemented

  Scenario: Developer finds a valid parseable features artifact at the canonical path
    When the developer reads _bmad-output/planning-artifacts/features.json
    Then the file exists and parses as valid JSON without error
    And the file contains at least six feature entries

  Scenario: Features cover both Nornspun and Momentum projects
    When the developer inspects the feature entries in features.json
    Then at least three entries represent Nornspun product features
    And at least three entries represent Momentum practice features
    And each entry includes a concrete working or not-working acceptance condition

  Scenario: Feature type taxonomy spans all three types across the entries
    When the developer lists the feature types present in features.json
    Then at least one entry has type flow
    And at least one entry has type connection
    And at least one entry has type quality
