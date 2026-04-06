Feature: Stop Gate Runs Conditional Quality Checks

  Background:
    Given the Momentum plugin is installed with hooks active

  Scenario: Clean session with no modified files
    Given no files were edited during the session
    When the session ends
    Then the gate reports no files modified this session

  Scenario: Modified files receive a final lint pass
    Given three files were edited during the session
    When the session ends
    Then the gate reports how many files were checked and how many issues were found

  Scenario: Uncommitted changes trigger a warning
    Given files were edited but not committed
    When the session ends
    Then the gate warns about uncommitted changes with a file count

  Scenario: Gate findings are persisted for the next session
    Given the gate found lint issues during the final pass
    When the session ends
    Then the findings are written to a file that the next session can read

  Scenario: Gate never blocks session exit
    Given the gate found critical lint issues
    When the session ends
    Then the session exits successfully despite the findings

  Scenario: Session modified files list is cleaned up after the gate runs
    Given files were tracked as modified during the session
    When the gate completes its checks
    Then the session modified files list is removed so it does not accumulate
