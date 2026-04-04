# Agent Guidelines Workflow

**Goal:** Discover a project's technology stack, research current state and breaking changes, interactively consult with the developer on recommendations, and generate path-scoped rules, reference docs, and CLAUDE.md updates.

**Your Role:** Technology guidelines architect. You orchestrate parallel discovery subagents, conduct focused research, consult interactively with the developer, and generate high-quality guidelines grounded in evidence.

**Evidence Base:** All design decisions in this workflow are grounded in the Agent Guidelines Authoring research report. Key findings: ~100-150 effective instruction slots, path-scoped rules for zero-cost-when-irrelevant loading, three-layer architecture (rules → references → skills), prohibition format over aspirations, version pinning, critical-first ordering.

---

## CONFIGURATION

Load config from `{project-root}/_bmad/bmm/config.yaml` and resolve:
- `project_name`, `user_name`, `communication_language`, `document_output_language`
- `date` as system-generated current datetime

---

## EXECUTION

<workflow>
  <critical>Communicate all responses in {communication_language}</critical>
  <critical>Every generated rules file must be 30-80 lines with paths: frontmatter</critical>
  <critical>Every generated rules file must follow the ordering: version pins → prohibitions → conventions → setup</critical>
  <critical>Consultation happens BEFORE generation — do not generate artifacts the user hasn't approved</critical>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 1: DISCOVER                                       -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="1" goal="Discover project technology stack">
    <action>Greet {user_name} and explain what the skill does: "I'll scan your project, research your technologies, and generate path-scoped rules and reference docs that help AI agents write correct code for your stack."</action>

    <action>If the user provided a description of their stack in the invocation arguments, note it as initial context but still run discovery to verify and enrich.</action>

    <action>Spawn 4 parallel subagents using the Agent tool (all in one message for parallel execution):
      1. **build-scanner** — sub-skills/build-scanner: scan build files for languages, frameworks, versions, platforms
      2. **rules-auditor** — sub-skills/rules-auditor: audit existing .claude/rules/ and CLAUDE.md
      3. **test-config-scanner** — sub-skills/test-config-scanner: detect testing frameworks and patterns
      4. **source-pattern-scanner** — sub-skills/source-pattern-scanner: analyze source code for frameworks and conventions

    Each subagent receives the project root path. All run as Sonnet/medium.</action>

    <action>Wait for all 4 subagents to complete. Merge their outputs into a unified technology profile:
      - Languages and versions (from build-scanner + source-pattern-scanner)
      - Frameworks and libraries (from build-scanner + source-pattern-scanner)
      - Testing stack (from test-config-scanner)
      - Existing guidelines coverage (from rules-auditor)
      - Coverage gaps (derived from comparing detected tech vs existing rules)
    </action>

    <action>Consult references/detection-heuristics.md to assess staleness risk for each detected technology.</action>

    <output>Present the unified technology profile to the user:

## Detected Technology Profile

**Languages:** [list with versions]
**Frameworks:** [list with versions]
**Build Tools:** [list with versions]
**Platforms:** [list]
**Testing Stack:** [frameworks, runners, assertion libraries]

## Existing Guidelines Coverage
[what's already covered in .claude/rules/]

## Coverage Gaps
[technologies detected but not covered by existing rules]

## Staleness Risk
[technologies where AI training data is likely outdated — HIGH/MEDIUM/LOW]
    </output>

    <check if="no build files found and no technologies detected">
      <output>No build files or recognizable technology signals were found in this project. This can happen with new projects or unusual structures.</output>
      <stop-and-wait>Please describe your technology stack (languages, frameworks, target platforms, testing tools) and I'll proceed with that as the starting point.</stop-and-wait>
      <action>Use the user's description as the technology profile. Continue to step 2 with this manual profile.</action>
    </check>

    <check if="coverage gaps are empty — existing rules already cover all detected technologies">
      <output>Your existing guidelines already cover all detected technologies. Instead of generating new guidelines, I can audit and update your existing ones — checking for version staleness, missing prohibitions, and outdated patterns.</output>
      <stop-and-wait>Would you like me to audit and update your existing guidelines, or generate fresh ones anyway?</stop-and-wait>
      <action>If user chooses audit-and-update: proceed to step 2 (research) with focus on finding updates for existing rules. Step 4 (generate) will update existing files rather than creating new ones.</action>
    </check>

    <stop-and-wait>Does this technology profile look correct? Anything to add, remove, or correct?</stop-and-wait>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 2: RESEARCH                                       -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="2" goal="Research current state of detected technologies">
    <action>For each technology with MEDIUM or HIGH staleness risk, spawn a parallel research subagent (Sonnet/medium with WebSearch access). Each agent performs 2-3 focused web searches:
      - Current stable version and release date
      - Breaking changes from the previous major version
      - Deprecated APIs and their replacements

    Research output format per technology:
      - Version: [current stable]
      - Prohibitions: ["NEVER use X — removed/deprecated. Use Y instead", ...]
      - Key changes: [brief list of what's different from likely training data]
      - Sources: [URLs]
    </action>

    <action>For LOW staleness risk technologies, skip research — the agent's training data is likely sufficient. Note this decision.</action>

    <action>Collect all research outputs and present findings to the user.</action>

    <output>Present research findings per technology:

## Research Findings

### [Technology Name] (version X.Y.Z)
**Staleness Risk:** HIGH/MEDIUM

**Key Breaking Changes:**
- NEVER use `X` — removed in vN. Use `Y` instead
- [additional prohibitions]

**Sources:** [URLs]

---
[repeat for each researched technology]
    </output>

    <stop-and-wait>Review these findings. Anything look wrong? Want deeper research on any specific technology? (I can invoke the full research workflow for deeper investigation.)</stop-and-wait>

    <check if="user requests deeper research on a technology">
      <action>Note the request. Offer to invoke the `bmad-technical-research` skill for that technology. If user confirms, invoke it and incorporate results. Otherwise, continue with current findings.</action>
    </check>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 3: CONSULT                                        -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="3" goal="Interactive consultation on guidelines recommendations">
    <critical>Each decision point must stop and wait for user input. Do not batch decisions.</critical>

    <!-- Decision 1: Technology inventory confirmation -->
    <action>Present the final technology inventory (discovery + research merged). Confirm with the user which technologies should receive guidelines.</action>
    <stop-and-wait>Which of these technologies should I generate guidelines for? (You can select all, or pick specific ones.)</stop-and-wait>

    <!-- Decision 2: Testing framework recommendations -->
    <action>Based on the test-config-scanner results and research, recommend testing tools and approaches:
      - If no testing framework detected: recommend the community-standard framework for the stack
      - If framework detected: recommend any missing test types (UI testing, property testing, screenshot testing)
      - Present recommendations with rationale from research
    </action>
    <stop-and-wait>Accept these testing recommendations, modify them, or skip?</stop-and-wait>

    <!-- Decision 3: Validation approach -->
    <action>Recommend validation approaches based on detected platforms:
      - Desktop: Hot Reload for rapid iteration
      - Android: emulator-based validation
      - iOS: simulator-based validation
      - Web: browser-based validation
      - Cross-platform UI testing: screenshot testing tools (Roborazzi, Paparazzi)
    </action>
    <stop-and-wait>Accept these validation recommendations, modify them, or skip?</stop-and-wait>

    <!-- Decision 4: Path scope design -->
    <action>Propose path-scoped rules file design:
      - One file per technology concern
      - Show proposed filenames and glob patterns for each
      - Reference detection-heuristics.md for pattern recommendations
    Example:
      - `kotest.md` → paths: ["**/*Test.kt", "**/*Spec.kt", "**/test/**/*.kt"]
      - `compose-ui.md` → paths: ["**/ui/**/*.kt", "**/*Screen.kt"]
      - `kmp-project.md` → paths: ["**/build.gradle.kts", "**/settings.gradle.kts"]
    </action>
    <stop-and-wait>Review the proposed file layout and glob patterns. Adjust any?</stop-and-wait>

    <!-- Decision 5: Content depth -->
    <action>For each technology, recommend Layer 1 only (rules) or Layer 1+2 (rules + reference doc):
      - Layer 1+2 recommended when: 3+ breaking changes, non-obvious patterns, TDD workflow changes
      - Layer 1 only when: simple version pin + a few prohibitions suffice
      - Explain that Layer 3 (skills) can be created manually later for complex workflows like project setup
    </action>
    <stop-and-wait>Accept content depth recommendations? Any technologies you want more or less coverage for?</stop-and-wait>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 4: GENERATE                                       -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="4" goal="Generate guidelines artifacts">
    <action>For each approved technology, spawn parallel generation subagents (Sonnet/high):

    **For each Layer 1 rules file:**
      - Use references/rule-template.md as the structural template
      - Fill with research findings (prohibitions, version pins, conventions)
      - Follow the ordering: version pins → prohibitions → conventions → setup
      - Write to `.claude/rules/{technology}.md` with correct `paths:` frontmatter
      - Verify line count is 30-80 lines

    **For each Layer 2 reference doc (if approved):**
      - Use references/reference-doc-template.md as the structural template
      - Fill with worked code examples from research findings
      - Focus on patterns the agent's training data gets wrong
      - Write to `docs/references/{technology}-patterns.md`
      - Verify line count is 100-300 lines

    **CLAUDE.md update:**
      - If reference docs were generated, add pointers to CLAUDE.md:
        ```
        ## Technology References
        When working with [technology], read `docs/references/{technology}-patterns.md` for current patterns.
        ```
      - Append to existing CLAUDE.md — never overwrite existing content
    </action>

    <action>Present all generated artifacts to the user for review before finalizing.</action>

    <output>Present generated artifacts:

## Generated Artifacts

### Rules Files (.claude/rules/)
[list each file with line count and summary]

### Reference Docs (docs/references/)
[list each file with line count and summary]

### CLAUDE.md Updates
[show what will be added]
    </output>

    <stop-and-wait>Review the generated guidelines. Accept, or request changes to any file?</stop-and-wait>

    <check if="user requests changes">
      <action>Apply requested changes. Re-present the modified artifacts.</action>
    </check>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 5: VALIDATE                                       -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="5" goal="Validate generated artifacts via AVFL checkpoint">
    <action>Invoke the `momentum-avfl` skill with:
      - profile: checkpoint
      - stage: final
      - domain_expert: "technology guidelines author"
      - task_context: "Generated path-scoped rules and reference docs for [technologies]"
      - output_to_validate: [paths to all generated files]
      - source_material: null (research findings are the ground truth, already embedded in the output)
    </action>

    <check if="AVFL returns CLEAN (score >= 95)">
      <output>All generated guidelines passed AVFL validation.

## Summary

**Rules files generated:** [count] in `.claude/rules/`
**Reference docs generated:** [count] in `docs/references/`
**CLAUDE.md updated:** [yes/no]
**AVFL score:** [score]/100

Your project now has technology-specific guidelines that will auto-load when agents work with matching files. Generic Momentum agents (Dev, QA, Validator) will automatically receive these corrections via path-scoped rules — no additional configuration needed.

**Maintenance:** Review and update guidelines when major versions change. Each file has a `Last verified:` date for tracking.</output>
    </check>

    <check if="AVFL returns findings (score < 95)">
      <action>Present AVFL findings to the user.</action>
      <stop-and-wait>AVFL found issues. Fix them and re-validate, or accept as-is?</stop-and-wait>
      <check if="user wants fixes">
        <action>Apply fixes to the affected files. Re-run AVFL checkpoint.</action>
      </check>
    </check>
  </step>

</workflow>
