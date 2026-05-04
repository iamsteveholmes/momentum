Feature: Markdown Formatting for Skill Output Templates

  Background:
    Given the Momentum plugin is installed and available

  # AC5 (all 18 workflow.md files updated) is verified by the DoD checklist — not expressed as a behavioral scenario.

  Scenario: Skill completion output renders with visual hierarchy
    Given a sprint-planning workflow has been invoked and has completed successfully
    When the developer reads the completion output in the terminal
    Then the output contains section headers that separate distinct content blocks
    And story slugs and file paths appear in formatted inline code or bold text
    And the output is scannable rather than a flat wall of plain text

  Scenario: Gate failure output stands out visually from surrounding text
    Given a quick-fix workflow is in progress
    When a gate check fails during execution
    Then the warning or failure message appears visually distinguished from surrounding status lines
    And the rest of the output surrounding the warning renders in normal formatting

  Scenario: Skill output preserves all dynamic placeholders intact
    Given a create-story workflow completes with a known story key and file path
    When the developer reads the completion output
    Then the story key value appears in the output in place of the placeholder
    And the file path value appears in the output in place of the placeholder
    And no unresolved template markers are visible in the output

  Scenario: Skill workflow behavior is unchanged after formatting updates
    Given a retro workflow is invoked against a completed sprint
    When the developer invokes the retro workflow against that sprint
    Then the sprint record shows a retro_run_at timestamp
    And a retro findings document exists in the sprint directory

  Scenario: Single-line status messages are not artificially inflated
    Given a skill that emits a brief single-line status acknowledgement
    When the developer reads that status line in the terminal
    Then the output is a concise line without section headers added around it

  Scenario: Shell commands shown in output are visually distinct from prose
    Given a workflow that includes a shell command or skill invocation in its completion output
    When the developer reads the output
    Then the suggested command appears in inline code formatting distinct from the surrounding prose
