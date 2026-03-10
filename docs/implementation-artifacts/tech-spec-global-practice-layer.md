---
title: 'Global Agentic Engineering Practice Layer'
slug: 'global-practice-layer'
created: '2026-03-08'
status: 'ready-for-dev'
stepsCompleted: [1, 2, 3, 4]
tech_stack: [] # Intentionally empty — this spec produces markdown config files, not product code
files_to_modify:
  - '~/.claude/CLAUDE.md'
  - '~/.claude/rules/anti-patterns.md'
  - '~/.claude/rules/testing-philosophy.md'
  - '~/.claude/rules/architecture.md'
  - '~/.claude/rules/security.md'
  - 'docs/process/process-backlog.json'
code_patterns: [] # Intentionally empty — no product code patterns
test_patterns: [] # Intentionally empty — no automated tests for markdown config
---

# Tech-Spec: Global Agentic Engineering Practice Layer

**Created:** 2026-03-08

## Overview

### Problem Statement

No universal AI development standards exist across projects. Each new project starts with a blank enforcement layer, and practice-level principles (authority hierarchy, Producer-Verifier, anti-pattern prevention, debt type mitigation) must be manually re-established. Without a global `~/.claude/CLAUDE.md` and `~/.claude/rules/`, Claude Code sessions lack the foundational guardrails that prevent the four AI-induced debt types (verification debt, cognitive debt, pattern drift, technical debt).

### Solution

Create `~/.claude/CLAUDE.md` with cross-cutting practice philosophy (authority hierarchy, Producer-Verifier, evaluation flywheel) plus `~/.claude/rules/` with four modular rule files, each targeting specific debt types: `anti-patterns.md` (pattern drift + technical debt), `testing-philosophy.md` (verification debt), `architecture.md` (cognitive debt + pattern drift), `security.md` (standalone).

### Scope

**In Scope:**
- `~/.claude/CLAUDE.md` — practice-level philosophy, under 50 non-blank lines, no project-specific content
- `~/.claude/rules/anti-patterns.md` — Corrective rules named after the 7 Ox Security AI anti-patterns
- `~/.claude/rules/testing-philosophy.md` — verification discipline, authority hierarchy for tests
- `~/.claude/rules/architecture.md` — cognitive debt prevention, explain-it-or-reject-it
- `~/.claude/rules/security.md` — Common security vulnerabilities in AI-generated code
- Update `docs/process/process-backlog.json` PT-001a status to "in-progress"

**Out of Scope:**
- Project-level `CLAUDE.md` (PT-001b — deferred until product codebase exists)
- `@import` of project-context.md (project-level concern)
- Build/test/lint command references (project-level concern)
- Nornspun or campaign-specific rules
- Hook infrastructure (PT-002)
- Sub-agent definitions (PT-003)

## Context for Development

### Codebase Patterns

This is process infrastructure, not product code. The files are markdown documents that Claude Code loads automatically:
- `~/.claude/CLAUDE.md` is auto-loaded into every Claude Code session across all projects
- `~/.claude/rules/*.md` files are auto-loaded into every session as additional rule context
- Both global and project-level files are loaded additively into the LLM context. There is no formal override mechanism — the LLM receives both and resolves any contradictions through context weighting. Avoid contradictions between global and project rules rather than relying on precedence semantics.

### Files to Reference

| File | Summary |
| ---- | ------- |
| Plan §1.1 | Elevator pitch — specs are the product, code is verified output, four debt types, authority hierarchy, evaluation flywheel |
| Plan §2.2 | Four debt types: verification (unreviewed output), cognitive (understanding gap), pattern drift (AI amplifies bad patterns), technical (compounds exponentially) |
| Plan §2.3 | Ox Security catalog: Comments Everywhere (90-100%), By-the-Book Fixation (80-90%), Avoidance of Refactors (80-90%), Over-Specification (80-90%), Bugs Deja-Vu (80-90%), Return of Monoliths (no rate), Vanilla-Style Code (no rate) |
| Plan §4.1 | Authority Hierarchy: specs are immutable, tests are read-only to coding agents, code is disposable |
| Plan §4.2 | Producer-Verifier: creation and verification must be structurally isolated, verifiers are read-only |
| Plan §4.3 | Evaluation Flywheel: trace failures upstream — fix workflows/specs/rules, not just code |
| Plan §4.4 | Three Tiers: (1) deterministic hooks/linters, (2) structured BMAD workflow steps, (3) advisory CLAUDE.md/rules |
| Plan §4.6 | Standards Placement: each standard lives in exactly one place, 150-instruction ceiling, what does NOT go in CLAUDE.md |
| Plan §4.7 | Impermanence Principle: adaptability over permanence — processes that grow are better than those that stay unchanged. Governs process evolution, not agent behavior. |
| Plan §5.3 | Debt mitigations: layered verification for verification debt, explain-it-or-reject-it for cognitive debt, CLAUDE.md rules for pattern drift, adversarial review for tech debt |
| Plan §5.5 | Findings ledger: structured record of quality failures for cross-story pattern detection (PT-008, not yet implemented) |
| Plan §6.1.2 | CLAUDE.md architecture: root file under 50-100 lines plus imports, modular .claude/rules/ one per concern |
| `docs/process/process-backlog.json` | Process task backlog — PT-001a status to update |

(Plan = `docs/planning-artifacts/AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md`)

### Technical Decisions

- **Global scope (user-level):** These files apply to ALL projects. They encode practice philosophy, not project specifics.
- **Authority hierarchy in root CLAUDE.md:** Specifications > tests > code is cross-cutting and belongs at the highest level.
- **One file per concern in rules/:** Modular, maintainable, each clearly tied to the debt types it addresses.
- **50-line ceiling for CLAUDE.md (tightened from plan's 50-100 range):** Plan §6.1.2 says "50-100 lines plus imports." We target the low end (under 50 non-blank lines) because this is the global layer — project-level CLAUDE.md (PT-001b) will add project-specific content, and the combined total must stay within the 150-instruction ceiling. Starting lean leaves maximum headroom.
- **No project-specific content:** No build commands, no `@import`, no tech stack references. Those belong in PT-001b.
- **Design principle — actionable rules only:** Each rule should describe something Claude would plausibly get wrong without the rule. Obvious guidance wastes instruction budget. (This is a design constraint for the implementor, not a testable AC.)
- **Additive composition, not override:** Global and project-level rules are both loaded. Avoid contradictions rather than relying on precedence.
- **Corrective rules named after anti-patterns:** `anti-patterns.md` contains corrective rules (what to do), named after the Ox Security anti-patterns they counteract (what AI does wrong). The file prescribes behavior, not describes problems.
- **"Explain it or reject it" deduplication:** The actionable rule lives in `architecture.md`. CLAUDE.md references the principle at philosophy level only (one sentence) without restating the full rule. This avoids instruction budget duplication.
- **Overlap acknowledgment — Bugs Deja-Vu vs Follow established patterns:** "Bugs Deja-Vu" in anti-patterns.md targets code-level duplication (search before writing, extract shared abstractions). "Follow established patterns" in architecture.md targets architectural-level convention adherence (read existing code, extend don't reinvent). Different scope, complementary concerns.
- **Overlap acknowledgment — Over-Specification vs Don't over-abstract:** "Over-Specification" in anti-patterns.md targets unnecessary implementation-level code (edge cases that can't happen, validation the caller prevents, configurability nobody asked for). "Don't over-abstract" in architecture.md targets unnecessary structural layers (interfaces with one implementation, factories for single-use objects, base classes for single hierarchies). Implementation-level vs architectural-level, complementary concerns.
- **Impermanence Principle excluded from CLAUDE.md:** Plan §4.7 ("Adaptability over Permanence") governs how the *process itself* evolves — it instructs the human practitioner to manage change, not the AI agent to behave differently. It has no actionable agent instruction form. Including it would waste instruction budget on a principle the AI cannot act on. It remains in the plan as a governing philosophy for process decisions.
- **Instruction count methodology:** Each imperative sentence or clause that directs agent behavior counts as one instruction (e.g., "Don't test private methods" = 1 instruction). Compound sentences with multiple directives count each directive separately. Estimated per-file counts based on spec content: anti-patterns ~15, testing ~10, architecture ~10, security ~10, CLAUDE.md ~10 = ~55 total. The 60-80 target is aspirational — landing in the 50-80 range is acceptable. The hard constraint is staying well under 150 to leave headroom for project-level additions. If below 60, the implementor may add minor elaboration to existing rules but should not invent new rules beyond what the spec defines.

## Implementation Plan

### Pre-flight Check

Before creating any files, verify the target directory state:
- Check if `~/.claude/CLAUDE.md` already exists. If so, back it up to `~/.claude/CLAUDE.md.backup-{date}` before proceeding.
- Check if `~/.claude/rules/` directory already exists. If so, back up any existing rule files to `~/.claude/backup-rules-{date}/` (outside the rules directory) before proceeding.
- The pre-flight backup is advisory — it protects against accidental data loss but is not AC-gated. If no pre-existing files exist (clean slate), skip backups and proceed.

### Tasks

Task ordering and dependencies:
- **Task 7 runs first** — marks PT-001a as "in-progress" to reflect work has begun.
- **Task 1** must complete before Tasks 2-5 (creates the directory).
- **Tasks 2-5** are independent and may run in parallel.
- **Task 6** depends on Tasks 2-5 being complete (to verify no content duplication with rules files).

- [ ] Task 7: Update process backlog PT-001a status
  - File: `docs/process/process-backlog.json`
  - Action: Update PT-001a status from "open" to "in-progress"
  - Notes: The PT-001 → PT-001a/PT-001b split was already completed during spec creation. This task only updates the status field. Run this first to reflect that implementation has begun.

- [ ] Task 1: Create `~/.claude/rules/` directory
  - File: `~/.claude/rules/` (new directory)
  - Action: `mkdir -p ~/.claude/rules`
  - Pre-flight: Run the pre-flight check above before this step
  - Notes: Must exist before writing rule files

- [ ] Task 2: Create `~/.claude/rules/anti-patterns.md`
  - File: `~/.claude/rules/anti-patterns.md` (new)
  - Action: Create corrective rule file targeting pattern drift and technical debt. Every rule section must contain imperative directives (do/don't), not problem descriptions.
  - Content must include:
    - Header stating: "Corrective rules for AI code generation anti-patterns. Each rule is named after the Ox Security anti-pattern it counteracts. Addresses: pattern drift, technical debt."
    - **Comments Everywhere** — Do not add comments that restate what code does. Comments explain *why*, not *what*. No inline comments on obvious lines. No docstrings on self-evident functions. If the user didn't ask for comments, don't add them.
    - **By-the-Book Fixation** — The project's architecture document is the first authority for style and patterns. Read it before writing new code. Surrounding code is evidence of conventions, not law — it may replicate anti-patterns. When architecture docs and surrounding code conflict, follow the architecture docs.
    - **Avoidance of Refactors** — When touching code, improve what you touch. If adding a feature reveals duplication, extract it. If a function is too long, split it. Don't leave code worse than you found it.
    - **Over-Specification** — Don't handle edge cases that can't happen. Don't add validation for scenarios the caller prevents. Don't build configurability nobody asked for. Three similar lines are better than a premature abstraction. (Scope: implementation-level unnecessary code. For architectural-level unnecessary structure, see architecture.md "Don't over-abstract".)
    - **Bugs Deja-Vu** — Before writing new code, search for existing implementations of the same logic. Reuse and extend, don't duplicate. If you find yourself writing nearly-identical code, extract a shared abstraction. (Scope: code-level duplication. For architectural-level pattern adherence, see architecture.md "Follow established patterns".)
    - **Return of Monoliths** — Respect module boundaries. Don't add cross-cutting concerns to a single file. If a change touches 5+ unrelated files, reconsider the approach.
    - **Vanilla-Style Code** — Use the project's established libraries. Don't reimplement what a dependency already provides. Check the project's dependency manifest before writing utility functions.

- [ ] Task 3: Create `~/.claude/rules/testing-philosophy.md`
  - File: `~/.claude/rules/testing-philosophy.md` (new)
  - Action: Create rule file targeting verification debt. Every rule section must contain imperative directives (do/don't), not problem descriptions.
  - Content must include:
    - Header stating: "Testing standards to prevent verification debt — the accumulation of unreviewed or inadequately tested AI-generated output."
    - **Authority of pre-existing tests** — Never modify a test to make code pass. If a test fails, the code is wrong, not the test. If the test is genuinely incorrect, stop and report why — do not silently fix it.
    - **Acceptance tests are immutable** — Files in `tests/acceptance/` (or equivalent acceptance test directory) are read-only. You may run them. You may read them. You may not edit, delete, or move them.
    - **Test what matters** — Tests verify behavior, not implementation. Don't test private methods. Don't assert on internal state. Test the contract: given these inputs, expect these outputs/effects.
    - **No tautological tests** — Every assertion must be capable of failing. Don't assert that a mock returns what you told it to return. Don't test that a constructor sets fields you just passed in. If removing the implementation wouldn't break the test, the test is worthless.
    - **Red before green** — When writing tests, confirm they fail before writing the implementation. If a test passes before you write any code, the test isn't testing anything. If the implementation is built but the test still fails, delete the code and rewrite the test from scratch.
    - **Tests must pass before completion** — The entire test suite must pass, not just your tests. Pre-existing failures must be fixed before writing new code. Do not mark work as done if any tests are failing. If you cannot make tests pass, stop and report.

- [ ] Task 4: Create `~/.claude/rules/architecture.md`
  - File: `~/.claude/rules/architecture.md` (new)
  - Action: Create rule file targeting cognitive debt and pattern drift. Every rule section must contain imperative directives (do/don't), not problem descriptions.
  - Content must include:
    - Header stating: "Architectural standards to prevent cognitive debt (code the developer cannot explain) and pattern drift (AI amplifying suboptimal patterns)."
    - **Explain it or reject it** — If the developer asks you to explain how generated code works and you cannot give a clear, accurate explanation, the code should be rewritten until it can be explained. Code the developer cannot understand is a liability, not an asset.
    - **No black boxes** — Prefer straightforward implementations over clever ones. Every layer of abstraction must earn its keep. If a simpler approach works, use it.
    - **Follow established patterns** — Before creating new patterns (new base classes, new utility modules, new architectural layers), verify that the project doesn't already have one. Read existing code first. Extend, don't reinvent. (Scope: architectural-level convention adherence. For code-level duplication prevention, see anti-patterns.md "Bugs Deja-Vu".)
    - **Dependency direction matters** — Higher-level modules depend on lower-level modules, not the reverse. Domain logic does not import from infrastructure. If you're importing from a layer above you, reconsider.
    - **ADRs for significant decisions** — When making a non-obvious architectural choice, document why. A brief comment or doc explaining the tradeoff prevents future agents (or future you) from undoing the decision.
    - **Don't over-abstract** — Don't create interfaces with one implementation. Don't create factories for objects created in one place. Don't create base classes for single hierarchies. Build for what exists, not what might exist. (Scope: architectural-level unnecessary structure. For implementation-level unnecessary code, see anti-patterns.md "Over-Specification".)

- [ ] Task 5: Create `~/.claude/rules/security.md`
  - File: `~/.claude/rules/security.md` (new)
  - Action: Create rule file for security standards (standalone, not debt-type-specific). Every rule section must contain imperative directives (do/don't), not problem descriptions.
  - Content must include:
    - Header stating: "Security standards. Standalone — not tied to a specific AI-induced debt type but critical for all AI-generated code."
    - **Never commit secrets** — No API keys, tokens, passwords, or credentials in code or config files committed to version control. Use environment variables or secret management. If you see a hardcoded secret, flag it immediately.
    - **Validate at system boundaries** — All external input (user input, API responses, file uploads, URL parameters) must be validated and sanitized. Internal function calls between trusted modules do not need redundant validation.
    - **No SQL/command injection** — Always use parameterized queries, never string concatenation for SQL. When applicable, use array-form arguments for shell commands rather than string interpolation, and use ORM methods or prepared statements for database access.
    - **No XSS in output** — All user-provided content rendered in HTML must be escaped. Use framework-provided escaping (React JSX, template engine auto-escape). Never use `dangerouslySetInnerHTML` or equivalent without explicit justification.
    - **Principle of least privilege** — Request minimum permissions. Don't use admin credentials when user credentials suffice. Don't grant write access when read-only works. File permissions should be as restrictive as possible.
    - **Dependencies are attack surface** — Don't add dependencies for trivial functionality. Verify that new dependencies are actively maintained and widely used. Check for known vulnerabilities before adding.

- [ ] Task 6: Create `~/.claude/CLAUDE.md`
  - File: `~/.claude/CLAUDE.md` (new)
  - Action: Create root practice philosophy file, under 50 non-blank lines
  - Content must include:
    - Title: "Agentic Engineering Practice"
    - **Authority Hierarchy** (from Plan §4.1): Specifications > tests > code. Agents never modify specifications or pre-existing tests to make code pass. If a test fails, the code is wrong. If a spec is ambiguous, ask — don't assume.
    - **Producer-Verifier Separation** (from Plan §4.2): The agent that writes code does not review it. Review happens in a separate context. Verification agents produce findings only — they never modify code.
    - **Evaluation Flywheel** (from Plan §4.3): When output fails quality standards, trace the failure upstream. Fix the workflow/spec/rule that caused it, not just the code. Every upstream fix prevents a class of errors permanently.
    - **Cognitive Debt Gate**: Reference only — "Code the developer cannot explain must be rewritten. See `rules/architecture.md` for the full rule." (One sentence. The actionable rule lives in architecture.md to avoid instruction duplication.)
    - **Three Tiers of Enforcement** (from Plan §4.4): Context for how standards are enforced. (1) Deterministic — hooks and linters, always execute. (2) Structured — BMAD workflow steps, enforced during workflow execution. (3) Advisory — CLAUDE.md and rules/, always loaded but may be deprioritized under context pressure. When enforcement tiers are available in a project (hooks, workflows), prefer pushing standards to the highest tier possible rather than relying on advisory rules alone.
    - **Note**: This file must NOT contain project-specific content (no build commands, no framework references, no paths). Project-specific standards belong in each project's root `CLAUDE.md`.
  - Notes: Keep under 50 non-blank lines. Every line must earn its place — if Claude already does it right without being told, don't include it.

### Acceptance Criteria

- [ ] AC1: Given the files `~/.claude/CLAUDE.md` and `~/.claude/rules/{anti-patterns,testing-philosophy,architecture,security}.md` exist at the correct paths with non-empty content, then they will be auto-loaded per Claude Code's documented behavior for user-level configuration files.
- [ ] AC2: Given `~/.claude/CLAUDE.md`, when non-blank lines are counted (using `grep -cve '^\s*$'`), then it contains fewer than 50 non-blank lines.
- [ ] AC3: Given each rules file, when reviewed, then it explicitly states which debt type(s) it addresses (or "standalone" for security) in its header.
- [ ] AC4: Given `~/.claude/rules/anti-patterns.md`, when reviewed, then it contains corrective rules for all 7 Ox Security anti-patterns (Comments Everywhere, By-the-Book Fixation, Avoidance of Refactors, Over-Specification, Bugs Deja-Vu, Return of Monoliths, Vanilla-Style Code).
- [ ] AC5: Given `~/.claude/rules/testing-philosophy.md`, when reviewed, then it contains the rule that pre-existing tests must never be modified to make code pass.
- [ ] AC6: Given `~/.claude/rules/testing-philosophy.md`, when reviewed, then it contains the rule that acceptance test files are read-only.
- [ ] AC7: Given `~/.claude/rules/architecture.md`, when reviewed, then it contains the "explain it or reject it" rule for cognitive debt prevention.
- [ ] AC8: Given `~/.claude/CLAUDE.md`, when reviewed, then it contains the Authority Hierarchy (specs > tests > code), Producer-Verifier Separation, and Evaluation Flywheel principles.
- [ ] AC9: Given `~/.claude/CLAUDE.md`, when reviewed, then it contains NO project-specific content (no build commands, no file paths, no framework references, no `@import` directives).
- [ ] AC10: Given all 5 files combined, when each imperative sentence or clause that directs agent behavior is counted as one instruction, then the total is between 50-80 instructions (leaving headroom for project-level additions under the 150-instruction ceiling). The hard ceiling is "well under 150"; the floor of 50 ensures meaningful coverage.
- [ ] AC11: Given `docs/process/process-backlog.json`, when reviewed, then PT-001a has status "in-progress".
- [ ] AC12: Given `~/.claude/CLAUDE.md`, when reviewed for the "explain it or reject it" concept, then it contains only a brief reference pointing to `rules/architecture.md` — the full actionable rule is not duplicated in CLAUDE.md.
- [ ] AC13: Given each rules file, when reviewed, then every rule section contains imperative directives (do/don't) rather than problem descriptions. The files prescribe behavior, not catalog anti-patterns.

## Additional Context

### Dependencies

- No code dependencies. Pure markdown files.
- Content derived from `docs/planning-artifacts/AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md`.
- No other process tasks must be completed first — this is foundational.

### Testing Strategy

- **File existence check:** After creation, verify all 5 files exist at the specified paths with non-empty content: `ls -la ~/.claude/CLAUDE.md ~/.claude/rules/*.md`
- **Content audit:** Each rule file must trace back to specific sections of the plan document. The debt type headers in each file provide this traceability.
- **Line count check:** Count non-blank lines in `~/.claude/CLAUDE.md`: `grep -cve '^\s*$' ~/.claude/CLAUDE.md` — must be under 50.
- **Instruction count:** Count each imperative sentence or clause that directs agent behavior across all 5 files. Target: 50-80 total (~55 estimated). One instruction = one "do this" or "don't do that" directive. Compound sentences with multiple directives count each directive separately.
- **Prescriptive check:** Verify each rule section uses imperative voice (do/don't) rather than describing problems.
- **Duplication check:** Verify the "explain it or reject it" rule appears in full only in `architecture.md`, with CLAUDE.md containing only a brief reference.
- **Differential behavior test (optional):** In a fresh session, ask Claude to write a function. Verify it doesn't add excessive comments (anti-patterns rule working). Compare against a session without the rules if available.

### Rollback Procedure

If the created files cause degraded LLM behavior or conflicts:

**If pre-flight backups exist** (restoring to previous state):
1. `mv ~/.claude/CLAUDE.md.backup-{date} ~/.claude/CLAUDE.md`
2. `rm ~/.claude/rules/anti-patterns.md ~/.claude/rules/testing-philosophy.md ~/.claude/rules/architecture.md ~/.claude/rules/security.md`
3. `cp ~/.claude/backup-rules-{date}/* ~/.claude/rules/ && rm -rf ~/.claude/backup-rules-{date}/`
4. If `~/.claude/rules/` is now empty: `rmdir ~/.claude/rules/`

**If no backups exist** (clean removal):
1. `rm ~/.claude/CLAUDE.md ~/.claude/rules/anti-patterns.md ~/.claude/rules/testing-philosophy.md ~/.claude/rules/architecture.md ~/.claude/rules/security.md`
2. If `~/.claude/rules/` is now empty: `rmdir ~/.claude/rules/`

**Then:**
3. Start a fresh Claude Code session to confirm clean state.
4. Diagnose which rule caused the issue by re-adding files one at a time.

### Notes

- **Instruction ceiling risk:** The 150-instruction ceiling (Plan §4.6) applies to ALL instructions Claude receives, including project-level CLAUDE.md and rules. The global layer targets 50-80 instructions (~55 estimated), leaving headroom for project-level additions.
- **Additive composition:** Global and project-level rules are both loaded into context. They do not have a formal override mechanism. Design global rules as universal truths no project would contradict.
- **Evolution:** These files will grow through the Evaluation Flywheel. When retrospectives identify systemic issues, new rules may be added here. The initial set is the minimum viable practice layer.
- **PT-001b scope (deferred):** Project-level CLAUDE.md will add: build/test/lint command references, `@import project-context.md`, project-specific coding conventions. Created when the first product codebase is established.
