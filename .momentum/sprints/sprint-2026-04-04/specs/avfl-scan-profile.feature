Feature: AVFL Scan Profile — Discovery-Only Validation for Team Handoff

  Background:
    Given the AVFL skill is installed with framework.json containing validation profiles
    And the existing profiles gate, checkpoint, and full are unchanged

  # AC1: Scan profile exists alongside existing profiles
  Scenario: Scan profile is available as a fourth profile option
    When a caller invokes AVFL with profile "scan"
    Then AVFL accepts the invocation without error
    And the gate, checkpoint, and full profiles still function identically

  Scenario: Scan profile composes with corpus mode
    When a caller invokes AVFL with profile "scan" and corpus true
    Then AVFL runs scan-intensity validation across all corpus files
    And cross_document_consistency and corpus_completeness dimensions are active

  # AC2: Dual reviewers and all lenses
  Scenario: Scan activates all lenses with dual reviewers
    When AVFL runs in scan mode on a target artifact
    Then all available lenses are activated
    And each lens spawns both an Enumerator and an Adversary reviewer
    And findings from both reviewers are collected per lens

  # AC3: Maximum skepticism
  Scenario: Scan uses maximum skepticism level
    When AVFL runs in scan mode
    Then skepticism is set to level 3
    And reviewers follow aggressive evaluation: look for what feels off, follow hunches

  # AC4: Cross-check confidence tagging and severity scoring
  Scenario: Consolidation applies cross-check confidence
    When both Enumerator and Adversary find the same issue
    Then the finding is tagged with HIGH confidence
    When only one reviewer finds an issue
    Then the finding is tagged with MEDIUM confidence and the consolidator investigates

  Scenario: Consolidator assigns severity levels to scan findings
    Given AVFL scan has produced a set of findings from dual reviewers
    When the consolidator produces the final findings list
    Then each finding is assigned a severity level of critical, high, medium, or low
    And severity assignment follows the framework's severity_weights definitions

  # AC5: Zero fix iterations
  Scenario: Scan produces findings without invoking fixer
    When AVFL runs in scan mode and findings are produced
    Then the fixer sub-skill is NOT spawned
    And the consolidated findings list is returned as the final output
    And no files are modified by the scan

  Scenario: Scan with zero findings returns clean result
    When AVFL runs in scan mode and no findings are produced
    Then the output indicates a clean scan with zero findings
    And no fixer is spawned

  # AC6: Findings list includes all required fields
  Scenario: Findings list includes all required fields
    Given AVFL scan has produced findings
    Then each finding includes id, severity, confidence, lens, dimension, location, description, evidence, and suggestion
    And findings are ordered by severity descending then confidence descending

  # AC7: Output format is designed for team handoff
  Scenario: Output format is suitable for team consumption
    Given AVFL scan has produced a findings list
    Then the findings are structured as actionable items with clear locations
    And each finding can be independently addressed by a fix agent

  # AC8: Hybrid model — fixer agents + E2E Validator + Architect Guard spawn concurrently
  Scenario: After AVFL scan, team agents spawn concurrently with findings as context
    Given AVFL scan has completed and produced a structured findings list
    When sprint-dev spawns the concurrent resolution team
    Then fixer agents spawn in parallel each receiving the AVFL findings list
    And the E2E Validator spawns concurrently receiving the AVFL findings list
    And the Architect Guard spawns concurrently receiving the AVFL findings list
    And each agent also receives the story ACs and Gherkin spec references for their scope

  # AC9: Sprint-dev invokes AVFL with scan profile
  Scenario: Sprint-dev invokes AVFL with scan profile in post-merge gate
    Given sprint-dev reaches the post-merge quality gate phase
    When sprint-dev invokes AVFL
    Then it passes profile "scan" as the profile parameter
    And the full post-merge codebase is the validation target

  # AC10: Team receives AVFL findings
  Scenario: Team spawn prompt includes AVFL findings list
    Given AVFL scan has completed with findings
    When sprint-dev spawns the concurrent team
    Then each team agent's spawn prompt includes the AVFL findings list
    And each agent also receives story ACs and Gherkin spec references

  # AC11: E2E Validator distinguished from AVFL
  Scenario: E2E Validator tests running behavior not file content
    Given the concurrent team is spawned after AVFL scan
    When the E2E Validator agent executes
    Then it runs behavioral tests against Gherkin scenarios using external tools
    And it does NOT review file content or source code
    And its output is a scenario-by-scenario pass/fail report

  Scenario: AVFL scan validates file content not running behavior
    When AVFL runs in scan mode
    Then it validates file content against source material
    And it does NOT execute external tools or test running behavior

  # Edge cases
  Scenario: Existing gate profile unchanged by scan addition
    When a caller invokes AVFL with profile "gate"
    Then behavior is identical to before the scan profile was added
    And only the structural lens is active with a single reviewer

  Scenario: Existing full profile unchanged by scan addition
    When a caller invokes AVFL with profile "full"
    Then behavior is identical to before the scan profile was added
    And the fix loop runs up to 4 iterations as before

  Scenario: Scan with corpus false validates single document
    When a caller invokes AVFL with profile "scan" and corpus false
    Then AVFL validates the single document with all lenses and dual reviewers
    And corpus-only dimensions are NOT active
