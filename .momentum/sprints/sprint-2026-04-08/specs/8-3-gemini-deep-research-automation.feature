Feature: Gemini Deep Research Automation via cmux-browser

  Background:
    Given the momentum-research skill is installed and a research project directory exists

  Scenario: Deep Research runs automatically when cmux-browser and auth state are available
    Given cmux-browser is available on the system
    And a saved Google auth state file exists at ~/.claude/browser-state/google-auth.json
    When the developer invokes the momentum-research skill
    Then the skill opens a browser surface to gemini.google.com
    And the skill enables Deep Research, fills the prompt, and auto-approves the research plan
    And a completed report is written to raw/gemini-deep-research-output.md with provenance frontmatter

  Scenario: Follow-up questions deepen the report after initial extraction
    Given a Deep Research report has been extracted into raw/gemini-deep-research-output.md
    And the browser surface is wide enough for the chat input to be visible
    When the skill generates follow-up questions based on thinly covered sub-questions
    Then follow-up responses are appended to raw/gemini-deep-research-output.md under a Follow-Up section

  Scenario: Skill prompts the developer to log in when no valid auth state exists
    Given cmux-browser is available on the system
    And no saved Google auth state file exists at ~/.claude/browser-state/google-auth.json
    When the developer invokes the momentum-research skill
    Then the skill prompts the developer to log in manually in the browser pane
    And after successful login the auth state is saved to ~/.claude/browser-state/google-auth.json

  Scenario: Skill falls back to basic Gemini when Deep Research stalls after retries
    Given cmux-browser is available on the system
    And a saved Google auth state file exists at ~/.claude/browser-state/google-auth.json
    When the research plan generation fails to produce a Start Research button after retries
    Then the skill falls back to gemini -p basic mode
    And a warning is displayed to the developer
    And output is written to raw/gemini-output.md instead

  Scenario: Skill falls back to basic Gemini when cmux-browser is unavailable
    Given cmux is not installed or not found on the system
    When the developer invokes the momentum-research skill
    Then the skill skips Deep Research entirely
    And falls back to gemini -p basic mode with output written to raw/gemini-output.md
