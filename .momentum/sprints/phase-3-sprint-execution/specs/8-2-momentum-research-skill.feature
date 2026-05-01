Feature: Momentum Research Skill
  A 6-phase deep research pipeline (SCOPE, EXECUTE, VERIFY, Q&A, SYNTHESIZE, COMMIT)
  that produces validated, provenance-tracked research documents through parallel
  subagents, optional Gemini CLI triangulation, AVFL corpus validation, and
  Momentum provenance patterns.

  Background:
    Given the momentum-research skill is available
    And Claude Code is running in a project with output folder configured

  # --- Skill Package Structure (AC1) ---

  Scenario: Skill package contains required files
    When the skill package is inspected
    Then a SKILL.md exists with model and effort frontmatter
    And a workflow.md exists defining all six phases
    And a references directory contains profile definitions, briefing template, Gemini prompt template, and output structure
    And an evals directory contains behavioral eval files

  # --- Phase 1: SCOPE (AC2) ---

  Scenario: SCOPE elicits topic and decomposes into sub-questions
    When the skill is invoked
    Then the user is asked to provide a research topic
    And the topic is decomposed into sub-questions that collectively cover the topic
    And the user is asked to select a research profile

  Scenario: SCOPE creates project directory structure
    When the user confirms the topic and profile
    Then a dated project directory is created with raw, validation, and final subdirectories
    And a scope document is written recording the topic, goals, sub-questions, profile, and date

  # --- Phase 2: EXECUTE (AC3) ---

  Scenario: EXECUTE spawns parallel subagents scaled by profile
    When the execute phase runs
    Then parallel subagents are spawned with count determined by the selected profile
    And each subagent receives a briefing with its assigned sub-question and date anchoring
    And each subagent is instructed to use primary sources and cite URLs
    And each subagent is instructed to use evidence notation for claim classification

  Scenario: Subagent outputs include provenance metadata
    When a subagent completes its research
    Then its output file includes content origin metadata identifying it as a subagent product
    And the subagent returns a brief inline summary to the orchestrator

  Scenario: Optional Gemini CLI triangulation
    Given the Gemini CLI is available on the system
    When the execute phase reaches the Gemini integration point
    Then the user is asked to confirm before Gemini is invoked
    And the Gemini output is written with content origin metadata identifying it as Gemini-sourced

  Scenario: Resume support for interrupted execution
    Given some subagent output files already exist from a previous run
    When the execute phase runs
    Then only missing subtopics are researched
    And existing output files are not overwritten

  # --- Phase 3: VERIFY (AC4) ---

  Scenario: Light profile skips verification
    Given the light profile is selected
    When the pipeline reaches the verify phase
    Then verification is skipped entirely
    And the pipeline proceeds to synthesis

  Scenario: Medium profile runs checkpoint AVFL corpus validation
    Given the medium profile is selected
    When the verify phase runs
    Then AVFL corpus mode is invoked with checkpoint profile and a reduced lens set
    And the validation report is written to the validation directory

  Scenario: Heavy profile runs full AVFL corpus validation
    Given the heavy profile is selected
    When the verify phase runs
    Then AVFL corpus mode is invoked with full profile and a complete lens set
    And the validation report is written to the validation directory

  # --- Phase 4: Q&A (AC5) ---

  Scenario: Q&A presents AVFL-identified uncertainties
    Given the verify phase produced findings
    When the Q&A phase runs
    Then AVFL-identified uncertainties and gaps are presented as targeted questions
    And user responses are captured interactively
    And responses are written with content origin metadata identifying them as human-sourced

  Scenario: Light profile skips Q&A
    Given the light profile is selected
    When the pipeline reaches the Q&A phase
    Then Q&A is skipped entirely

  Scenario: Q&A is skipped when verification was unavailable
    Given the verify phase was skipped or produced no findings
    When the pipeline reaches the Q&A phase
    Then Q&A is skipped because there are no AVFL findings to present

  # --- Phase 5: SYNTHESIZE (AC6) ---

  Scenario: Synthesis runs as a single subagent with clean context
    When the synthesize phase runs
    Then a single subagent reads all raw files, validation files, and the scope document from disk
    And the subagent produces a final research document in the final directory

  Scenario: Synthesis structure adapts to scope sub-questions
    When the synthesize phase runs
    Then the document structure is driven by the sub-questions defined in the scope phase
    And a default structure template is used as fallback

  Scenario: Final document includes provenance metadata
    When synthesis completes
    Then the final document includes content origin metadata identifying it as a synthesis product
    And the final document records whether human verification occurred

  # --- Phase 6: COMMIT (AC7) ---

  Scenario: Commit is proposed but not auto-executed
    When the commit phase runs
    Then a conventional commit message is proposed to the user
    And the commit is not executed until the user confirms
    And no push is performed

  # --- Provenance Tracking (AC8) ---

  Scenario: Final document traces derivation to all sources
    When synthesis completes
    Then the final document frontmatter includes a derivation chain
    And each raw subagent file is listed as synthesized from
    And the Gemini output is listed as synthesized from if present
    And the AVFL report is listed as validated by if present
    And practitioner notes are listed as informed by if present

  Scenario: Every raw file tracks its content origin
    When the execute phase completes
    Then each subagent output records its content origin as subagent-produced
    And the Gemini output records its content origin as Gemini-sourced if present
    And practitioner notes record their content origin as human-sourced if present

  # --- Evidence Notation Mapping (AC9) ---

  Scenario: Evidence notation maps to provenance levels
    When subagents apply evidence notation to claims
    Then official source claims map to the verified provenance level
    And practitioner source claims map to the cited provenance level
    And unverified claims map to the inferred provenance level
    And claims with no attribution are treated as ungrounded
    And claims flagged by AVFL corpus validation are marked as suspect

  # --- EDD Evals (AC10) ---

  Scenario: Behavioral evals are written before implementation
    When the development process begins
    Then three behavioral evals exist before any skill files are created
    And one eval verifies light profile runs without AVFL or Q&A and produces a final document
    And one eval verifies medium profile runs AVFL corpus checkpoint and Q&A
    And one eval verifies resume support detects existing files and only researches missing subtopics
