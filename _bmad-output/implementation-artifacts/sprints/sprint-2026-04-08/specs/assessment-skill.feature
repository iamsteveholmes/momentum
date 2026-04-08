Feature: Assessment Skill — Guided Product State Evaluation

  Background:
    Given the developer has the Momentum plugin installed

  Scenario: Developer scopes the assessment collaboratively before any discovery begins
    Given the developer invokes momentum:assessment
    When the skill starts
    Then the skill asks what the developer wants to assess before taking any action
    And the skill waits for the developer to describe the scope before spawning agents

  Scenario: Discovery agents run in parallel based on agreed scope
    Given the developer has agreed on a scope with the skill
    When the skill proceeds to discovery
    Then parallel discovery agents run against actual codebase and artifact state
    And each agent returns findings with evidence such as file paths and status assessments

  Scenario: Developer validates each finding before it is written to the assessment
    Given discovery agents have returned their findings
    When the skill presents findings to the developer
    Then findings are presented section by section
    And after each section the skill asks whether the finding matches the developer's understanding
    And no finding is written to the ASR document until the developer confirms it

  Scenario: Developer and skill collaboratively draft recommended next steps
    Given all findings have been confirmed by the developer
    When the skill moves to the next steps phase
    Then the skill drafts next steps collaboratively with the developer
    And the developer approves the final next steps list before the skill writes anything

  Scenario: Completed assessment is written and committed as a durable artifact
    Given the developer has confirmed all findings and approved next steps
    When the skill writes the assessment
    Then an ASR document appears in _bmad-output/planning-artifacts/assessments/
    And the document contains frontmatter with id, title, date, status, and method fields
    And the assessments index is updated with the new entry
    And both files are committed together

  Scenario: Skill offers to bridge findings into a decision record
    Given an ASR document has been written and committed
    When the assessment workflow completes
    Then the skill offers to feed the findings into a decision record
