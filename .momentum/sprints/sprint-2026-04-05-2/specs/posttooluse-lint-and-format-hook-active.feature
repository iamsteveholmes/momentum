Feature: PostToolUse Lint and Format Hook Active

  Background:
    Given the Momentum plugin is installed with hooks active

  Scenario: Lint issues in a Python file are reported after editing
    Given a Python file exists with a lint violation
    When the developer edits the file
    Then a single-line summary prefixed with "[momentum-lint]" appears with the issue count

  Scenario: Clean file edit produces no lint output
    Given a Python file exists with no lint violations
    When the developer edits the file
    Then no momentum-lint output appears

  Scenario: JSON syntax errors are caught after writing a JSON file
    Given a JSON file is written with invalid syntax
    When the hook runs on the file
    Then a "[momentum-lint]" message reports the JSON syntax error

  Scenario: Unsupported file types are silently skipped
    Given a file with an unrecognized extension is edited
    When the hook runs on the file
    Then no output appears and the hook exits cleanly

  Scenario: Modified file is tracked for the stop gate
    Given the developer edits a file during the session
    When the hook completes
    Then the file path appears in the session modified files list
    And duplicate edits to the same file do not create duplicate entries
