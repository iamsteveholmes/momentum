Feature: Sprint Index Schema Migration — Add Status and Retro Fields

  The sprint lifecycle state machine requires status, slug, and retro_run_at
  fields that are currently missing from sprints/index.json. This migration
  adds those fields without modifying or removing any existing data.

  Note: active is null in the current index — there is no active sprint object
  to migrate. This migration only touches the planning sprint and completed entries.

  Background:
    Given the file "sprints/index.json" exists and contains valid JSON

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

  Scenario: Existing planning sprint fields are present and unchanged after migration
    When I read the "planning" object from "sprints/index.json"
    Then the object has a "locked" field that is present and retains its pre-migration value
    And the object has a "stories" array that is present and non-empty
    And the object has a "waves" array that is present and non-empty

  Scenario: Existing completed sprint fields are present and unchanged after migration
    When I read the first entry in the "completed" array from "sprints/index.json"
    Then the entry has a "locked" field that is present and retains its pre-migration value
    And the entry has a "slug" field that is present and non-empty
    And the entry has a "started" field that is present and non-empty
    And the entry has a "completed" field that is present and non-empty
    And the entry has a "stories" array that is present and non-empty
    And the entry has a "team_composition" object that is present

  Scenario: The migrated file is valid JSON
    When I parse "sprints/index.json" with a JSON parser
    Then parsing succeeds without errors
