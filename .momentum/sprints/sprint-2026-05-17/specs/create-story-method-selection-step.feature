Feature: create-story selects and records the verification method

  As a developer,
  I want create-story to consult the verification routing rule and record the
  selected verification method on every story it creates,
  so that I never arrive at validation time with an unresolved method.

  Scenario: Unambiguous change type resolves silently and writes to frontmatter
    Given a story stub is classified as change-type skill-instruction
    And verification-standard.md is present with a routing table
    When create-story processes the story
    Then verification_method appears in the story's YAML frontmatter
    And the value equals the method mapped to skill-instruction in the routing table
    And no developer prompt for method selection was issued

  Scenario: Conflicting change types surface candidates and await developer selection
    Given a story stub has change types skill-instruction and script-code
    And those change types map to different methods in the routing table
    When create-story processes the story
    Then the developer is shown the mapped method candidates for each change type
    And create-story waits for the developer to select the governing method
    And after selection verification_method is written to the story's YAML frontmatter

  Scenario: Method selection step halts with a clear message when the rule file is absent
    Given verification-standard.md does not exist on disk
    When create-story attempts to process a story stub
    Then the method-selection step halts before the guide injection step runs
    And the output states that verification-standard.md was not found
    And no verification_method field is written to the story file

  Scenario: Completed story output includes the selected verification method
    Given a story stub has been processed by create-story with an unambiguous change type
    When create-story reaches its completion signal step
    Then the completion output includes the selected verification_method value alongside the change types
