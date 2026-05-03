Feature: Migrate implementation-artifacts path references to .momentum/

  Background:
    Given all implementation-artifacts path fixes have been applied to the skills/momentum/ directory

  Scenario: No stale implementation-artifacts paths remain in skill files after the fix
    Given the skills/momentum/ directory contains eval files, workflow files, and scripts
    When a developer runs: grep -rn "_bmad-output/implementation-artifacts" skills/momentum/ | grep -v "eval-impetus-reads-momentum-state.md" | grep -v "orient.md"
    Then the grep produces zero output lines

  Scenario: Intentional anti-pattern eval retains its old-path references unchanged
    Given eval-impetus-reads-momentum-state.md exists at skills/momentum/skills/impetus/evals/
    When a developer reads the file contents
    Then the file still contains _bmad-output/implementation-artifacts/ references

  Scenario: plan-audit eval uses the correct .momentum/stories/ path after the fix
    Given skills/momentum/skills/plan-audit/evals/eval-substantive-spec-audit.md exists
    When a developer reads the file
    Then the file references .momentum/stories/p1-1-add-momentum-code-review-skill.md
    And the file does not contain the path .momentum/p1-1-add-momentum-code-review-skill.md without the stories/ segment

  Scenario: Planning-artifacts references are untouched across all skill files
    Given the skills/momentum/ directory contains files referencing _bmad-output/planning-artifacts/
    When a developer counts all occurrences of _bmad-output/planning-artifacts/ with grep -rn across skills/momentum/
    Then the count is at least 61

  Scenario: orient.md uses correct .momentum/ paths for live state and contains a single negation of the old path
    Given skills/momentum/skills/impetus/references/orient.md exists
    When a developer reads orient.md
    Then lines 17-19 contain .momentum/ paths for live state sources (sprints/index.json, stories/index.json, and signals/)
    And line 21 contains a negation statement prohibiting fallback to _bmad-output/implementation-artifacts/
    And no other occurrences of _bmad-output/implementation-artifacts/ appear in the file

  Scenario: Plugin patch version is incremented after all path fixes are applied
    Given skills/momentum/.claude-plugin/plugin.json shows version 0.18.0 before the fix
    When a developer reads the version field
    Then the version is 0.18.1
