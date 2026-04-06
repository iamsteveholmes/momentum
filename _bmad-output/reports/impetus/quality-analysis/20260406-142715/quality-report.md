# BMad Method · Quality Analysis: Impetus

**Impetus** -- Momentum practice orchestrator
**Analyzed:** 2026-04-06T14:27Z | **Path:** skills/momentum/skills/impetus
**Interactive report:** quality-report.html

## Agent Portrait

Impetus is a practice partner in the KITT mold -- dry, confident, and quietly proud of clean engineering state. He owns the session lifecycle for the Momentum practice: greeting developers with sprint awareness, managing installs and upgrades, dispatching workflows, and synthesizing subagent results in a single consistent voice. His personality is defined by what he refuses to do -- no generic praise, no visible machinery, no step counts -- as much as by what he delivers: forward-moving, substantive guidance with genuine satisfaction when discipline holds and a raised eyebrow when it slips.

## Capabilities

| Capability | Status | Observations |
| --- | --- | --- |
| Startup routing & preflight | Good | Clean conditional dispatch; single-tool-call happy path |
| First-install consent & execution | Needs attention | 4 findings (path standards, onboarding gap) |
| Session orientation & greeting | Needs attention | 3 findings (dual source of truth, help command gap) |
| Version upgrade | Needs attention | 2 findings (sequential I/O, upgrade chain scriptable) |
| Hash drift detection | Needs attention | 1 finding (no permanent accept option) |
| Journal display & thread management | Needs attention | 3 findings (hygiene scriptable, corruption, thread skip) |
| Completion signals | Good | Well-defined format, agency return |
| Review dispatch | Good | Background dispatch with productive waiting |
| Productive waiting | Good | Substantive engagement during waits |
| Subagent result synthesis | Good | Hub-and-spoke rigorously enforced |
| Behavioral patterns (cross-cutting) | Good | Exceptional quality; domain-specific, guiding |
| Input interpretation | Good | Comprehensive 5-category system |

## Assessment

**Good** -- Impetus is a structurally sound, identity-rich orchestrator with excellent prompt craft and one of the strongest persona definitions analyzed. The agent's primary strengths -- performance-conscious progressive disclosure, rigorous hub-and-spoke enforcement, and sophisticated UX patterns like proactive-offer-with-no-re-offer -- represent mature engineering. The main opportunities are path-standards compliance (home directory paths in evals and workflow), moving deterministic journal hygiene computations into scripts (~800-1200 tokens/session), and bridging the onboarding gap between first-install and first-productive-session.

## Opportunities

### 1. Home Directory Paths Throughout Workflow and Evals (high -- 16 observations)

The path-standards scanner flagged 16 instances of `~/` home directory paths across workflow.md and eval files. These paths are environment-specific and would break in non-standard home directory configurations or CI environments. The workflow references `~/.claude/momentum/global-installed.json`, `~/.claude/rules/`, and similar paths directly rather than using `$HOME` or environment variables consistently.

**Impact:** Portability across environments; CI/headless compatibility.

**Action:** Replace all `~/` references with `$HOME` expansion or have the momentum-tools.py script resolve paths internally, keeping hardcoded paths out of the workflow prompt.

**Constituent findings:**
- path-standards: workflow.md:159 -- `~/.claude/momentum/global-installed.json` in Step 1
- path-standards: workflow.md:212, 224 -- `~/.claude/rules/` in install output templates
- path-standards: workflow.md:305, 306, 308 -- `~/.claude/momentum/` in Step 4 state writing
- path-standards: workflow.md:597, 599 -- `~/.claude/momentum/global-installed.json` in Step 10
- path-standards: evals/eval-decline-path.md:5
- path-standards: evals/eval-first-install-consent-and-execution.md:5, 10, 14
- path-standards: evals/eval-hash-drift-warning.md:5, 5, 8
- path-standards: evals/eval-version-match-skip.md:5
- Plus 4 additional eval file references

### 2. Journal Hygiene Should Be Deterministic Script, Not LLM Computation (high -- 5 observations)

Workflow Step 11 instructs the LLM to perform timestamp arithmetic, elapsed-time computation, concurrent-tab detection, dormant-thread flagging, dependency satisfaction checks, and context-hash matching for No-Re-Offer suppression. Every one of these operations is deterministic. The LLM currently reads the journal schema, parses JSONL, and evaluates multiple conditional branches -- costing 800-1200 tokens per session on the open-threads path (the common case for active developers).

**Impact:** 800-1200 token savings per session; eliminates non-deterministic variance in timestamp arithmetic.

**Action:** Create a `momentum-tools session journal-hygiene` command that returns structured JSON with sorted threads, warnings (concurrent, dormant, dependency-satisfied, unwieldy), and suppressed offers. The LLM then only formats and presents.

**Constituent findings:**
- script-opportunities: workflow.md:390-479 -- Journal thread hygiene computations (800-1200 tokens)
- script-opportunities: workflow.md:503-512 -- Journal view regeneration (300-500 tokens)
- script-opportunities: workflow.md:420-422, 447-448 -- Context hash computation for No-Re-Offer
- enhancement-opportunities: Journal corruption recovery -- no error handling for malformed JSONL lines
- enhancement-opportunities: Concurrent session safety for journal writes

### 3. SKILL.md Template Compliance -- Content Exists in Non-Standard Locations (medium -- 6 observations)

The structure scanner flagged five missing standard sections (Overview, Identity, Communication Style, Principles, On Activation). The content for all five exists -- Identity is in Voice & Input and workflow.md, Communication Style is in Voice & Input and workflow.md Voice Rules, Principles are the Behavioral Patterns, On Activation is the Startup section. The issue is structural alignment with the BMad agent template, not missing content.

**Impact:** Tooling compatibility; consistent agent scanning; new-contributor readability.

**Action:** This is a judgment call. Options: (a) Add brief canonical section headers to SKILL.md that reference the existing content, (b) Rename existing sections (e.g., Startup to On Activation), or (c) Accept as intentional bootloader pattern and document the deviation. The lean bootloader design is defensible -- adding sections would increase SKILL.md token cost on every invocation.

**Constituent findings:**
- structure-prepass: SKILL.md:1 -- Missing ## Overview section (high)
- structure-prepass: SKILL.md:1 -- Missing ## Identity section (high)
- structure-prepass: SKILL.md:1 -- Missing ## Communication Style section (high)
- structure-prepass: SKILL.md:1 -- Missing ## Principles section (high)
- structure-prepass: SKILL.md:1 -- Missing ## On Activation section (high)
- structure-analysis: SKILL.md + workflow.md -- Identity content duplicated across files (low)

### 4. Missing Fallback, Onboarding, and Help Paths (medium -- 5 observations)

Several user journeys have undefined behavior: unexpected preflight results with no fallback, first-time users dropped into a sprint menu with no onboarding, and "help" or "?" input with no dedicated response. These gaps affect different user archetypes but share a root cause -- the workflow optimizes for the happy path without covering edge entry points.

**Impact:** First-session retention; error recovery; team-member onboarding.

**Action:** Add three items: (1) A fallback check at the end of SKILL.md startup routing for unrecognized preflight results, (2) A post-install onboarding fork offering a quick walkthrough or jump-to-planning, (3) A "help" / "?" command in input interpretation that outputs a brief self-description and menu explanation.

**Constituent findings:**
- agent-cohesion: SKILL.md Startup -- No fallback route for unexpected preflight results (high)
- enhancement-opportunities: Steps 2-5 into Step 7 -- No onboarding path for brand-new users (high-opportunity)
- enhancement-opportunities: Steps 7, 11 -- No help command or self-description capability (high-opportunity)
- enhancement-opportunities: Step 6 into Step 7 -- Decline path degraded mode is invisible (medium-opportunity)
- enhancement-opportunities: Step 10 -- Hash drift [K] creates recurring warning with no escape (medium-opportunity)

### 5. Frontmatter and Workflow File Placement (medium -- 5 observations)

Three frontmatter fields (model, effort, allowed-tools) are flagged as non-standard, and both workflow.md and workflow-runtime.md are at the skill root instead of in a references/ directory. These are path-standards and structure findings.

**Impact:** Consistency with BMad skill conventions; scanner compatibility.

**Action:** The frontmatter fields are functional configuration for the Claude Code harness -- moving them to the SKILL.md body is a reasonable alternative. Moving workflow files to references/ would require updating all references in SKILL.md.

**Constituent findings:**
- path-standards: SKILL.md:4 -- Invalid frontmatter key: model (high)
- path-standards: SKILL.md:5 -- Invalid frontmatter key: effort (high)
- path-standards: SKILL.md:6 -- Invalid frontmatter key: allowed-tools (high)
- path-standards: workflow.md:0 -- Prompt file at skill root (high)
- path-standards: workflow-runtime.md:0 -- Prompt file at skill root (high)

## Strengths

- **Exemplary persona definition.** The "servant-partner in the KITT sense" identity is specific, evocative, and functionally load-bearing. It drives real UX decisions -- deference with dignity, words with mass, earned emotion. The voice rules enforce this through concrete anti-patterns rather than vague "be professional" guidance.

- **Gold-standard happy-path optimization.** The SKILL.md preflight script pre-renders the entire greeting in a single tool call, avoiding workflow.md loading, reference file reads, and template computation for the most common session start. This is mature prompt engineering.

- **Rigorous hub-and-spoke enforcement.** The developer never learns which subagent ran. This is not just stated as a principle -- it is backed by synthesis rules, voice prohibitions, and workflow steps that transform structured JSON into Impetus-voice output.

- **Sophisticated UX patterns.** The proactive-offer-with-no-re-offer pattern (including context_hash for material-change detection), expertise-adaptive orientation, and configuration gap detection represent a level of agent UX sophistication that most designs never reach.

- **Well-architected progressive disclosure.** Three tiers (SKILL.md ~1K tokens, workflow.md ~10K tokens, workflow-runtime.md ~2K tokens) with genuine demand-loading. The happy path touches only the first tier.

- **Comprehensive eval coverage.** 60+ eval files covering first-install, menu interaction, thread management, voice compliance, completion signals, and edge cases. This is an unusually thorough test surface.

- **Intentional compaction-survival mechanisms.** Voice rule reminders in workflow-runtime.md and input interpretation duplication in SKILL.md serve real architectural purposes -- they ensure critical behavioral constraints survive context compaction.

## Detailed Analysis

### Structure & Capabilities

Impetus uses a lean bootloader architecture that diverges from the standard BMad agent template. SKILL.md functions as a startup router (84 lines, ~1036 tokens) that dispatches to workflow.md for complex paths and handles the happy path inline. The content for all "missing" standard sections exists in non-standard locations -- Identity in Voice & Input and workflow.md, Communication Style across voice rules in all three files, Principles as Behavioral Patterns in workflow.md. All workflow files exist and are structurally valid with no orphaned references. The skill has no references/ directory despite workflow-runtime.md referencing `${CLAUDE_SKILL_DIR}/references/` paths -- these resolve to the parent plugin's references directory, which needs verification.

### Persona & Voice

Persona context quality is excellent across the system. The identity paragraph in workflow.md is one of the strongest persona definitions analyzed -- evocative, concise, and functionally load-bearing. Voice rules are specific, enforceable, and anti-pattern-focused. The three-file architecture maintains voice consistency through deliberate redundancy: SKILL.md carries the core identity and voice rules, workflow.md carries the full behavioral pattern set, and workflow-runtime.md carries a condensed voice reminder. The SKILL.md has no Overview section, which risks mechanical execution after context compaction drops workflow.md. The missing Overview is the one prompt-craft gap in an otherwise exemplary persona implementation.

### Identity Cohesion

Impetus is one of the most cohesive agent designs analyzed. Every capability traces cleanly to the persona -- session orientation is the guardian checking the perimeter, install management is the steward maintaining infrastructure, journal hygiene is proactive housekeeping, hub-and-spoke synthesis is the partner who shields the developer from machinery. The one tension is scope breadth: Impetus is simultaneously a session greeter, install manager, journal tracker, workflow dispatcher, background narrator, and UX personality layer. Each role fits the persona individually, but together they create a large cognitive surface. Capability granularity passes the Goldilocks test -- nothing too micro, nothing too mega.

### Execution Efficiency

The happy path is excellently optimized -- one preflight tool call pre-renders the entire greeting. Subagent delegation is clean (no source-file reads before dispatch), runtime behaviors are demand-loaded, and reference files are loaded per-capability. The install/upgrade path (Steps 1-4) has sequential I/O that could be batched (three independent file reads, per-action shell execution, sequential state writes), saving 2-6 tool-call round trips on that infrequent path. Step 7's workflow-path greeting performs 2-3 sequential reads that could be parallelized.

### Conversation Experience

The first-timer journey has a significant onboarding cliff: installation is well-crafted, but the moment it ends, a new user faces a sprint-aware menu with no mental model of Momentum's concepts. The expert journey is well-optimized on the happy path but forces mandatory thread-list interaction when open threads exist, with no skip shortcut. The confused-user journey lacks a help command. The automator journey confirms Impetus is fundamentally interactive -- automation callers correctly bypass it via momentum-tools.py directly. The edge-case analysis identified undefined behavior for out-of-range menu selections, empty journal files, and momentum-tools.py failures.

### Script Opportunities

Impetus is well ahead of most agents on the script-vs-prompt spectrum. The startup-preflight command is a textbook example of deterministic pre-processing. The primary remaining opportunities are: (1) journal hygiene computations (800-1200 tokens/session, high frequency), (2) journal view regeneration (300-500 tokens, multiple times per session), (3) upgrade chain resolution (300-500 tokens on upgrade path), (4) install action execution combined with state writing (400-800 tokens on install path). Total estimated savings: 2,000-3,400 tokens per session depending on path.

## Recommendations

1. **Create `journal-hygiene` and `journal-append` script commands** -- Resolves the highest-token-cost finding (800-1200 tokens/session) and addresses journal corruption resilience. Consolidates findings from script-opportunities (F1, F2, F6, F8) and enhancement-opportunities (corruption, concurrency). Resolves ~8 findings. Effort: medium.

2. **Replace `~/` paths with `$HOME` or script-resolved paths** -- Resolves all 16 path-standards findings in one pass. Improves portability and CI compatibility. Resolves 16 findings. Effort: low.

3. **Add fallback routing, help command, and post-install onboarding** -- Addresses the three user-journey gaps (unexpected preflight, confused user, first-timer onboarding cliff). Resolves 5 findings. Effort: medium.

4. **Decide on SKILL.md template compliance strategy** -- Either add brief canonical section headers, rename existing sections, or document the lean bootloader pattern as an intentional deviation. Resolves 5-6 structure findings. Effort: low.

5. **Add description trigger clause** -- Change frontmatter description to include "Use when starting a Momentum session, invoking '/momentum', or managing sprint workflows." Resolves 2 findings. Effort: low.

6. **Consolidate install/upgrade I/O into script** -- Batch Steps 3-4 file operations into a single `session install-actions` command. Resolves 3 efficiency findings. Effort: medium.

7. **Add hash-drift [A]ccept option and out-of-range input handling** -- Small UX improvements that prevent recurring warnings and undefined behavior. Resolves 2 findings. Effort: low.
