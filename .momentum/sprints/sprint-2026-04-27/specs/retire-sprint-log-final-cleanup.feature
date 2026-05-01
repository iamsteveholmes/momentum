Feature: Retire sprint-log infrastructure end-to-end

  Background:
    Given the sprint-log infrastructure has been retired and DuckDB transcript audit is the sole evidence source for retros

  Scenario: Retro halts when no Claude Code sessions match the sprint date range
    Given a sprint exists whose started and completed dates match no Claude Code session files on disk
    When the developer invokes the retro workflow on that sprint
    Then the retro halts before any auditor analysis is produced
    And the developer sees an error naming the sprint slug and the date range that produced zero matches
    And the developer is not prompted to continue against an empty dataset

  Scenario: Deprecated sprint-log stub stories no longer surface as actionable backlog work
    Given the developer is preparing the next sprint from the active backlog
    When the developer asks the sprint-planning workflow to list backlog stories available for selection
    Then the listing does not offer retro-extract-preflight-validation as selectable work
    And the listing does not offer sprint-log-directory-enforcement as selectable work
    And each of those two stories is reported as dropped with a provenance note pointing to the sprint-log retirement

  Scenario: The retired sprint-logs directory is absent from disk
    Given the developer is on a clean working tree of the project
    When the developer lists the path .claude/momentum/sprint-logs
    Then the path does not exist on disk
    And sibling artifacts under .claude/momentum such as journal.jsonl and the hooks directory are still present

  Scenario: Recreating a file under the retired path produces no git tracking
    Given the developer is on a clean working tree of the project
    When the developer creates a file at .claude/momentum/sprint-logs/probe.txt and runs git status
    Then git reports no changes to be committed for that path
