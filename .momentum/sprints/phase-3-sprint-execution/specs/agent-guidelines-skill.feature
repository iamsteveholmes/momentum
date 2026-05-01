Feature: Agent Guidelines Skill
  The `momentum-agent-guidelines` skill discovers a project's technology stack,
  researches current state and breaking changes, interactively consults with the
  developer, and generates path-scoped rules, reference docs, and CLAUDE.md
  updates. Implements FR61a (two-layer agent model guideline creation).

  Background:
    Given a project with at least one build file (build.gradle.kts, package.json, or similar)
    And Claude Code is running in the project directory

  # --- Discovery Phase ---

  Scenario: Discovery detects technology stack from build files
    When the agent-guidelines skill is invoked
    Then parallel subagents scan the project for build files
    And a structured technology profile is produced listing detected languages, frameworks, and versions
    And the profile is presented to the user for confirmation

  Scenario: Discovery audits existing guidelines
    When the discovery phase runs
    Then existing `.claude/rules/*.md` files are enumerated
    And existing `CLAUDE.md` content is read
    And a gap analysis identifies technologies with no current guidelines
    And the audit results are presented alongside the technology profile

  Scenario: Discovery detects testing configuration
    When the discovery phase runs
    Then test configuration files are identified (test runners, assertion libraries, config files)
    And detected testing tools are included in the technology profile

  # --- Research Phase ---

  Scenario: Research finds breaking changes for detected technologies
    Given the user confirmed the technology profile
    When the research phase runs
    Then parallel subagents perform focused web searches for each detected technology
    And research outputs include current stable versions
    And research outputs include breaking changes from likely training data cutoffs
    And research outputs are formatted as prohibitions ("NEVER use X -- use Y instead")

  Scenario: Research results include sources
    When research completes for a technology
    Then each finding includes at least one source URL
    And findings are presented to the user before proceeding

  # --- Consultation Phase ---

  Scenario: Consultation presents testing framework recommendations
    Given research has completed
    When the consultation phase begins
    Then the skill recommends testing tools based on community adoption for the detected stack
    And the user can accept, modify, or skip each recommendation

  Scenario: Consultation covers path scope design
    When path scope decisions are presented
    Then each proposed rules file shows its glob patterns
    And the user can adjust which file patterns trigger each rules file

  Scenario: Consultation covers content depth
    When content depth decisions are presented
    Then the user can choose Layer 1 only (rules) or Layer 1+2 (rules + reference docs)
    And the choice determines what the generation phase produces
    And the skill describes Layer 3 (skills) as a future option the user can create manually

  Scenario: User can escalate to full research
    Given the consultation phase is in progress
    When the user requests deeper research on a specific technology
    Then the skill offers to invoke the full research workflow for that technology

  # --- Generation Phase ---

  Scenario: Generated rules files have correct structure
    Given the user approved all consultation decisions
    When the generation phase completes
    Then each generated `.claude/rules/*.md` file has valid YAML frontmatter with `paths:` array
    And each `paths:` entry is a valid glob pattern
    And each rules file is concise enough to stay within the instruction budget

  Scenario: Generated rules follow research-backed ordering
    When a rules file is generated
    Then version pins appear first
    And critical prohibitions ("NEVER use X") appear before correct patterns
    And setup/configuration specifics appear last

  Scenario: Generated rules include version constraints and staleness tracking
    When a rules file is generated
    Then the generated rules include version constraints for each detected technology
    And the generated rules include a verification date for staleness tracking

  Scenario: Reference docs are generated when requested
    Given the user chose Layer 1+2 or all three layers
    When generation completes
    Then reference docs are written to `docs/references/`
    And each reference doc contains annotated code examples showing correct patterns
    And reference docs are focused on patterns the agent's training data gets wrong

  Scenario: CLAUDE.md is updated with pointers
    Given reference docs were generated
    When generation completes
    Then `CLAUDE.md` is updated with pointers to the generated reference docs
    And no existing CLAUDE.md content is removed or overwritten

  # --- Validation Phase ---

  Scenario: AVFL checkpoint validates generated artifacts
    When all artifacts have been generated
    Then AVFL runs with checkpoint profile on all generated files
    And findings are presented to the user
    And the user can accept the artifacts or request fixes

  # --- Edge Cases ---

  Scenario: Project with no build files
    Given a project with no recognizable build files
    When the agent-guidelines skill is invoked
    Then the skill asks the user to describe their technology stack manually
    And the workflow continues from the user's description

  Scenario: Project with existing comprehensive guidelines
    Given a project where `.claude/rules/` already covers all detected technologies
    When the discovery phase completes
    Then the skill reports that existing coverage is comprehensive
    And offers to audit and update existing guidelines rather than generate new ones
