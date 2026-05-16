Feature: Researcher Base Body — Universal Agent Role Contract for Researcher

  Background:
    Given the Momentum plugin is installed and the researcher agent is available for spawning

  Scenario: Researcher produces a structured investigation report with a mandatory Evidence Inventory
    Given a research question with a defined scope of sources to consult
    When the developer spawns the researcher agent with that question
    Then the agent emits a RESEARCHER_OUTPUT_START / RESEARCHER_OUTPUT_END block
    And the block contains an Investigation Report with Scope, Verdict, Findings, Evidence Inventory, Unverified / Gaps, and Inference Log sections
    And the Evidence Inventory lists every source the agent consulted, including sources that yielded no useful result

  Scenario: Researcher surfaces conflicts and gaps rather than resolving them with invented evidence
    Given a research question where available sources are contradictory or incomplete
    When the developer spawns the researcher agent with that question
    Then the Unverified / Gaps section lists every claim the agent could not source
    And the Verdict is PARTIAL, INCONCLUSIVE, or BLOCKED rather than ANSWERED
    And no entry in the Findings section asserts a fact without a corresponding source in the Evidence Inventory

  Scenario: Researcher distinguishes direct evidence from inference in its output
    Given a research question that requires synthesis across multiple sources
    When the developer spawns the researcher agent with that question
    Then any conclusion that goes beyond what a single source directly states appears in the Inference Log
    And each Findings entry carrying a LOW or MEDIUM confidence is traceable to either an incomplete source or an inferential step in the Inference Log
