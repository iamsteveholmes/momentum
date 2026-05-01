Feature: Journal Status Tool — Deterministic Open Thread Detection

  Scenario: No journal file returns exists false
    Given the journal file does not exist
    When the developer runs the journal status command
    Then the result indicates the journal does not exist
    And the open thread count is zero

  Scenario: Empty journal returns zero open threads
    Given the journal file exists but contains no entries
    When the developer runs the journal status command
    Then the result indicates the journal exists
    And the open thread count is zero

  Scenario: Open threads are counted correctly
    Given the journal contains entries for three threads and one has a closing event
    When the developer runs the journal status command
    Then the open thread count is two
    And the thread summary shows each thread with its status

  Scenario: Malformed journal lines are skipped gracefully
    Given the journal contains valid entries mixed with corrupted lines
    When the developer runs the journal status command
    Then the valid entries are processed normally
    And the result includes a count of parse errors
