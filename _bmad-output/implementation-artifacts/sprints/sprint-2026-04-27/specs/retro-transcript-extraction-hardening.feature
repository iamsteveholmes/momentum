Feature: Retro Transcript Extraction Hardening — Worktree Path Resolution and UTC Boundary Fix

  Background:
    Given the developer is preparing to run a retrospective on a completed sprint

  Scenario: Retro corpus includes sessions from worktrees alongside the main checkout
    Given the developer worked on sprint stories across the main checkout and one or more git worktrees of the same project
    When the developer runs the retro extraction for that sprint
    Then the consolidated session list contains sessions originating from each worktree path
    And the same session does not appear more than once in the extracted corpus

  Scenario: Sessions on either side of UTC midnight land in the right sprint
    Given a sprint completes on a given UTC date
    And one session closes shortly before UTC midnight on the final sprint day
    And another session opens shortly after UTC midnight on the day following sprint completion
    When the developer runs the retro extraction scoped to the sprint date range
    Then the late-night session on the final sprint day is included in the corpus
    And the early-morning session from the next UTC day is excluded from the corpus

  Scenario: Same-day sprint extraction filters by story slug membership
    Given two sprints started and completed on the same UTC date
    And sessions from both sprints fall inside that single-day window
    When the developer runs the retro extraction for one of those sprints
    Then only sessions referencing that sprint's story slugs appear in the corpus
    And the extraction output reports the session count before and after slug filtering

  Scenario: Extracted JSONL records round-trip cleanly through a JSON parser
    Given the developer has run the retro extraction on a completed sprint
    When the developer parses each line of the extract files as JSON
    Then every line parses without error
    And no record contains Python-style single-quoted strings or Python literals where JSON booleans or null are expected

  Scenario: Retro extraction discovers its tooling from a downstream project
    Given the developer is running the retro from a project that consumes Momentum via the plugin cache
    And multiple plugin-cache versions of Momentum are installed on disk
    When the developer runs the retro extraction
    Then the extraction succeeds without the developer supplying a script path
    And the resolved tooling path corresponds to the highest installed version
