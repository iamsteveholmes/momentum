Feature: Sprint Index Schema Migration — Add Status and Retro Fields

  The sprint lifecycle state machine requires status, slug, and retro_run_at
  fields that are currently missing from sprints/index.json. This migration
  adds those fields without modifying or removing any existing data.

  Background:
    Given the file "sprints/index.json" exists and contains valid JSON

  Scenario: Active sprint has an explicit status field
    When I read the "active" object from "sprints/index.json"
    Then the object has a "status" field with value "active"

  Scenario: Planning sprint has an explicit status field
    When I read the "planning" object from "sprints/index.json"
    Then the object has a "status" field with value "planning"

  Scenario: Planning sprint has a slug field
    When I read the "planning" object from "sprints/index.json"
    Then the object has a "slug" field
    And the "slug" value starts with "sprint-" followed by a date

  Scenario: Completed sprint entry has a retro_run_at field
    When I read the first entry in the "completed" array from "sprints/index.json"
    Then the entry has a "retro_run_at" field with value "2026-04-04"
    And the entry still has a "completed" field with value "2026-04-04"

  Scenario: Existing active sprint fields are unchanged after migration
    When I read the "active" object from "sprints/index.json"
    Then the object has a "locked" field with value true
    And the object has a "slug" field with value "sprint-2026-04-04-3"
    And the object has a "started" field with value "2026-04-04"
    And the object has a "stories" array with 4 entries
    And the object has a "waves" array
    And the object has a "team_composition" object

  Scenario: Existing planning sprint fields are unchanged after migration
    When I read the "planning" object from "sprints/index.json"
    Then the object has a "locked" field with value false
    And the object has a "stories" array with 4 entries
    And the object has a "waves" array with 3 entries

  Scenario: Existing completed sprint fields are unchanged after migration
    When I read the first entry in the "completed" array from "sprints/index.json"
    Then the entry has a "locked" field with value true
    And the entry has a "slug" field with value "sprint-2026-04-04"
    And the entry has a "started" field with value "2026-04-04"
    And the entry has a "completed" field with value "2026-04-04"
    And the entry has a "stories" array with 1 entry
    And the entry has a "team_composition" object

  Scenario: The migrated file is valid JSON
    When I parse "sprints/index.json" with a JSON parser
    Then parsing succeeds without errors
