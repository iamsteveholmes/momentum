Feature: Transcript Query Calibration — Fix Error False Positives and Schema Variants

  Background:
    Given the sprint-2026-04-06 session transcripts are available
    And the transcript query tool is installed

  Scenario: error query reports only structural errors, not string mentions
    When the errors query is run against the sprint corpus
    Then every flagged error corresponds to a tool failure or explicit error indicator
    And no flagged error is merely content that mentions the word "error"

  Scenario: false-positive rate on error detection is below five percent
    When the errors query is run against the sprint corpus
    And a sample of flagged errors is manually verified
    Then fewer than five percent of flagged errors are false positives

  Scenario: all subagent transcripts are parseable regardless of schema shape
    When the agent-summary query is run against all subagent JSONL files
    Then every subagent file produces a summary row
    And no files are skipped or cause a parse failure

  Scenario: error counts are consistent between errors query and agent summary
    When the errors query is run against the sprint corpus
    And the agent-summary query is run against the same corpus
    Then the error count per agent in the summary matches the errors query results

  Scenario: true errors that were previously detected are still caught
    When the errors query is run against the sprint corpus
    Then actual tool failures present in the transcripts are still reported
    And true-positive recall has not regressed compared to the prior version
