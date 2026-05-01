Feature: Impetus Journal Hygiene Script — Move Deterministic Thread Computations to momentum-tools

  Background:
    Given a Momentum project with a journal at .claude/momentum/journal.jsonl

  Scenario: Impetus displays open threads instantly on session open without in-context computation
    Given one or more open threads exist in the journal
    When the developer invokes /momentum and the open-threads path is taken
    Then Impetus displays the thread list and any hygiene warnings
    And the display phase completes within 15 seconds wall-clock using fewer than 10 tool calls

  Scenario: Journal hygiene command returns structured display data for all open threads
    Given the journal contains a mix of open and closed threads with varying last_active timestamps
    When the developer runs momentum-tools session journal-hygiene
    Then the command returns a single JSON object containing a threads array sorted by last_active descending
    And each thread entry includes an elapsed_label such as "2h ago", "yesterday", or "5d ago"

  Scenario: Hygiene command warns about concurrent sessions
    Given a thread with a last_active timestamp within the last 30 minutes exists in the journal
    When the developer runs momentum-tools session journal-hygiene
    Then the returned JSON includes that thread in the concurrent warnings array with a minutes_ago field
    And a pre-composed suggested prompt for the concurrent warning is present in the response

  Scenario: Hygiene command warns about dormant threads
    Given a thread with a last_active timestamp more than 3 days ago exists in the journal
    When the developer runs momentum-tools session journal-hygiene
    Then the returned JSON includes that thread in the dormant warnings array with a days_inactive field

  Scenario: Hygiene command warns when a blocking dependency is now resolved
    Given a thread whose depends_on_thread target has status "closed" exists in the journal
    When the developer runs momentum-tools session journal-hygiene
    Then the returned JSON includes that thread in the dependency_satisfied warnings array
    And the entry includes the context_summary_short of the dependency that was unblocked

  Scenario: Hygiene command warns when too many threads are open
    Given more than 5 open threads exist in the journal
    When the developer runs momentum-tools session journal-hygiene
    Then the returned JSON includes an unwieldy warning with the open_count field set

  Scenario: Hygiene command suppresses a dormant offer the developer previously declined
    Given a dormant thread exists whose context_hash matches an entry in its declined_offers array
    When the developer runs momentum-tools session journal-hygiene
    Then that thread is absent from the dormant warnings array
    And it appears in the suppressed_offers array with a reason indicating the offer was declined

  Scenario: Hygiene command re-offers when the thread context has changed since the developer declined
    Given a dormant thread exists whose story_ref or phase has changed since the developer last declined
    When the developer runs momentum-tools session journal-hygiene
    Then the thread appears in the dormant warnings array rather than in suppressed_offers

  Scenario: Journal append command safely writes an entry and updates the human-readable view
    Given the journal exists with at least one prior entry
    When the developer runs momentum-tools session journal-append with a valid JSON entry
    Then the new entry is appended to journal.jsonl
    And journal-view.md is regenerated showing all open threads and threads closed within the last 7 days

  Scenario: Journal append command rejects malformed input before touching the journal
    Given the journal exists with prior entries
    When the developer runs momentum-tools session journal-append with a non-JSON string as the entry
    Then the command exits with an error and the journal file is left unchanged
