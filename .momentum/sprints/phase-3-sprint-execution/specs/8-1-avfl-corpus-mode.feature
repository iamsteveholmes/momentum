Feature: AVFL Corpus Mode
  Extends `momentum-avfl` with corpus mode: the ability to validate a set of
  related documents together, catching cross-document contradictions, consistency
  gaps, and corpus-level completeness issues. Backward compatible -- single-document
  behavior is unchanged when corpus mode is not activated.

  Background:
    Given a set of related documents that form a corpus
    And the momentum-avfl skill is available

  # --- Corpus Mode Activation (AC1, AC2) ---

  Scenario: Corpus mode accepts an array of file paths
    When the skill is invoked with corpus mode enabled
    Then the validation input accepts multiple file paths as a collection
    And all provided files are included in the validation pipeline

  Scenario: Default behavior is single-document mode
    When the skill is invoked without specifying corpus mode
    Then only single-document validation behavior is active
    And no corpus-specific dimensions or behaviors are triggered

  # --- Validator Behavior in Corpus Mode (AC3, AC4, AC5) ---

  Scenario: All validators receive the full corpus
    When corpus mode validation runs
    Then every validator receives all files in the corpus
    And validators produce findings that reference relationships across documents

  Scenario: Cross-document consistency dimension is active in corpus mode
    When corpus mode validation runs
    Then the cross-document consistency dimension detects contradictions between files
    And conflicting definitions or version references across files are reported as findings

  Scenario: Corpus completeness dimension is active in corpus mode
    When corpus mode validation runs
    Then the corpus completeness dimension identifies coverage gaps
    And topics that no file in the corpus addresses are reported as findings

  Scenario: Corpus-only dimensions are inactive in single-document mode
    When the skill is invoked without corpus mode
    Then the cross-document consistency dimension is not evaluated
    And the corpus completeness dimension is not evaluated
    And scoring behavior is identical to pre-corpus-mode behavior

  Scenario: Finding locations use filename-qualified format in corpus mode
    When corpus mode validation produces findings
    Then each finding location identifies both the file and the section within that file

  # --- Fixer Behavior in Corpus Mode (AC6, AC7, AC8) ---

  Scenario: Fixer produces per-file output in corpus mode
    When the fixer runs in corpus mode
    Then the fixer output contains a separate block for each file in the corpus
    And each block is clearly delimited so the caller can identify which content belongs to which file

  Scenario: Fixer resolves contradictions using authority hierarchy
    Given an authority hierarchy is provided ordering files from highest to lowest authority
    When the fixer encounters a cross-document contradiction
    Then the contradiction is resolved in favor of the higher-authority file
    And the fix is annotated as resolved by the authority hierarchy

  Scenario: Fixer flags unresolved contradictions when no authority hierarchy is provided
    Given no authority hierarchy is provided
    When the fixer encounters a cross-document contradiction
    Then the contradiction is flagged as an unresolved contradiction in the fix log
    And the fixer does not invent a resolution

  # --- Backward Compatibility (AC9) ---

  Scenario: Existing single-document callers are unaffected
    Given a caller that invokes the skill with a single document and no corpus parameter
    When the validation pipeline runs
    Then the behavior is identical to the pre-corpus-mode version of the skill
    And no new dimensions, parameters, or output formats appear

  # --- EDD Evals (AC10) ---

  Scenario: Behavioral evals are written before implementation
    When the development process begins
    Then three behavioral evals exist before any skill file is modified
    And one eval verifies cross-document dimensions produce cross-file findings
    And one eval verifies single-document invocation is unchanged
    And one eval verifies fixer authority resolution and annotation
