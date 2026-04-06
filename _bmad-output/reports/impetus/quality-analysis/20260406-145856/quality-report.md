# BMad Method · Quality Analysis: Impetus

**Impetus** — Momentum practice orchestrator
**Analyzed:** 2026-04-06T14:58:56Z | **Path:** `/Users/steve/projects/momentum/skills/momentum/skills/impetus`
**Interactive report:** quality-report.html

## Agent Portrait

Impetus is the guardian of Momentum's engineering discipline — a servant-partner in the KITT sense, dry and confident, who handles the machinery of sprints, quality gates, and story lifecycle so the developer can focus on building. Its voice carries Optimus Prime's gravitas paired with KITT's loyalty: direct without being terse, satisfied in clean state, displeased when discipline lapses, and never performing enthusiasm. This is an agent whose personality is not cosmetic but structural — the KITT archetype informs every interaction pattern from proactive offers to dormant-thread hygiene.

## Capabilities

| Capability | Status | Observations |
| --- | --- | --- |
| First-install consent + execution | Good | Clean consent UX, deterministic actions |
| Version upgrade chain | Good | Sequential upgrade with per-version consent |
| Hash drift detection | Good | Preflight detects, workflow resolves |
| Session greeting (9-state machine) | Needs attention | Missing sprint health summary (EG-4), no express mode for power users (EC-1) |
| Journal thread management | Needs attention | Hygiene signals accumulate without triage (EC-3), no session-level dormant opt-out (EC-2) |
| Thread hygiene (dormant, concurrent, unwieldy) | Needs attention | Dense wall-of-text presentation, all signals at equal visual weight |
| Proactive offer + no-re-offer | Good | Sophisticated context-hash comparison prevents nagging |
| Config gap detection | Good | Non-blocking by default, well-designed ask-one-question flow |
| Completion signals | Good | Templates with confidence-directed language |
| Productive waiting | Good | Anti-dead-air pattern, background dispatch |
| Subagent synthesis | Good | Hub-and-spoke purity, tiered review depth |
| Expertise-adaptive orientation | Good | Walkthrough for first-timers, abbreviated for experts |
| Spec contextualization (JIT) | Good | Motivated disclosure grounded in artifacts |
| Dispatch to sprint-dev/planning/refine | Needs attention | Refine dispatch target mismatch across files |

## Assessment

**Good** — Impetus is a well-architected orchestrator with one of the strongest agent identities in the ecosystem. Its happy-path startup optimization (single tool call, no workflow.md load) is best-in-class prompt engineering, and its voice specification is concrete enough to prevent common orchestrator failure modes. The primary opportunities are structural alignment with BMad conventions (non-standard section names in SKILL.md), scripting deterministic operations that the LLM currently performs manually (install actions, journal management), and UX refinements for power users and messy journal states.

## What's Broken

No critical issues. All high-severity findings are structural convention deviations, not functional breakage.

## Opportunities

### 1. SKILL.md Section Structure Deviates from BMad Conventions (high — 10 observations)

SKILL.md uses non-standard section headings (Startup, Voice & Input, Runtime Behaviors) instead of the canonical Overview, Identity, Communication Style, Principles, On Activation sections. The content exists and is high quality — it lives under different names or has been relocated to workflow.md. Any tooling or contributor that expects standard section names will not find them. The frontmatter also contains extra keys (model, effort, allowed-tools) that are valid Momentum extensions but flagged by the path standards scanner.

**Impact:** Tooling compatibility, contributor discoverability, ecosystem consistency.

**Fix:** Add thin canonical sections to SKILL.md: a brief Overview (3-5 sentences pulling mission framing from workflow.md Identity), rename "Voice & Input" to include Identity and Communication Style concepts, add a Principles section extracting judgment priorities from workflow.md, and rename "Startup" to "On Activation". This is additive — the current structure remains, wrapped in canonical names.

**Observations:**
- Missing ## Overview section (structure-capabilities-prepass, SKILL.md:1)
- Missing ## Identity section (structure-capabilities-prepass, SKILL.md:1)
- Missing ## Communication Style section (structure-capabilities-prepass, SKILL.md:1)
- Missing ## Principles section (structure-capabilities-prepass, SKILL.md:1)
- Missing ## On Activation section (structure-capabilities-prepass, SKILL.md:1)
- Invalid frontmatter key: model (path-standards, SKILL.md:4)
- Invalid frontmatter key: effort (path-standards, SKILL.md:5)
- Invalid frontmatter key: allowed-tools (path-standards, SKILL.md:6)
- Name missing "agent" prefix convention (structure-capabilities-prepass, SKILL.md:1)
- Description missing "Use when..." trigger phrase (structure-capabilities-prepass, SKILL.md:1)

### 2. Deterministic Operations Still Performed by LLM (high — 8 observations)

Install/upgrade action execution (file copies, state file writes), journal view regeneration (JSONL parsing, markdown table rendering), and journal hygiene checks (timestamp arithmetic, context-hash computation, declined-offers matching) are all entirely deterministic but currently performed by the LLM through multiple sequential Bash tool calls. The preflight script demonstrates the right architecture — these remaining operations should follow the same pattern.

**Impact:** 800-1300 tokens saved on install/upgrade paths, 850-1300 tokens on sessions with open threads. More importantly, eliminates the most fragile LLM behavior (JSONL parsing + markdown table rendering from parsed data).

**Fix:** Add three commands to momentum-tools.py: (1) `session install-actions` for file copy execution + state file writes serving both install and upgrade paths, (2) `session journal-write` for append + view regeneration, (3) extend `session journal-status --hygiene` to include all hygiene checks with pre-computed results. The LLM then renders results in voice rather than performing the computation.

**Observations:**
- Install action execution loop: 7+ sequential Bash calls per install (script-opportunities, workflow.md:248-300)
- State file writes with inline python3 one-liners (script-opportunities, workflow.md:302-328)
- Journal view regeneration: full JSONL re-parse on every write (script-opportunities, workflow.md:503-512)
- Journal thread hygiene: inline timestamp arithmetic (script-opportunities, workflow.md:403-478)
- Upgrade chain resolution: linked-list traversal by LLM (script-opportunities, workflow.md:516-593)
- Hash drift resolution execution: manual file copy loop (script-opportunities, workflow.md:596-627)
- Context hash computation repeated across steps (script-opportunities, workflow.md:420, 447)
- .gitignore check via inline python3 regex (script-opportunities, workflow.md:330-337)

### 3. Greeting Lacks Quantitative Sprint Context (high — 3 observations)

The greeting narrative has exceptional voice ("steady ground", "let's face it together") but provides no quantitative sprint health signal. The developer's most urgent question at session start — "where are things?" — is deferred behind a dispatch to sprint-dev. Meanwhile, power users who invoke `/momentum` multiple times daily see the full greeting ceremony every time with no express mode option.

**Impact:** Every session start misses the orientation moment. Daily power users experience accumulated friction.

**Fix:** Include a one-line sprint health summary in the preflight greeting data (e.g., "2 of 4 stories done, 1 in progress, 1 ready"). When `momentum_completions >= 10` and exactly one obvious action exists, offer an express greeting: single-line state + single-key dispatch, with full menu one keystroke away.

**Observations:**
- No sprint progress summary in greeting (enhancement-opportunities, session-greeting.md)
- Greeting ceremony friction for power users at 50+ sessions (enhancement-opportunities, SKILL.md happy path)
- "What changed since last session?" digest not available for returning users (enhancement-opportunities, SKILL.md happy path)

### 4. Hygiene Signals Accumulate Without Triage (medium — 3 observations)

Step 11 presents concurrent-tab warnings, dormant thread offers, dependency-satisfied notifications, and unwieldy-triage offers all at once, inline, before the selection prompt. For messy journals with 6+ threads, this creates an overwhelming wall of text with no priority differentiation — safety warnings (concurrent tabs) appear at the same visual weight as convenience suggestions (dormant cleanup).

**Impact:** Signal dilution in the most complex journal states. Developers with messy state learn to ignore hygiene outputs.

**Fix:** Prioritize and batch hygiene signals. Lead with safety (concurrent-tab warning), display the thread list, then surface one hygiene observation — the most impactful — before the selection prompt. Offer remaining items behind a "more hygiene items?" soft gate. Also add a session-level "stop offering dormant cleanup" preference after 3 consecutive declines.

**Observations:**
- Wall-of-text hygiene output for messy journals (enhancement-opportunities, workflow.md:403-478)
- No session-level "stop asking about dormant threads" escape hatch (enhancement-opportunities, workflow.md Step 11)
- Dense paragraph blocks in workflow.md hygiene sections (prompt-craft, workflow.md:416-459)

### 5. Path References Use Home Directory Tilde Notation (high — 16 observations)

Workflow.md and multiple eval files use `~/` paths (e.g., `~/.claude/momentum/global-installed.json`, `~/.claude/rules/authority-hierarchy.md`) which are environment-specific. The path standards scanner flagged 16 instances across workflow.md and eval files.

**Impact:** Portability concern for environments where `~` expansion behaves differently. The eval files are particularly affected since they embed these paths in Given/When/Then assertions.

**Fix:** In workflow.md, the `~/` paths are instructions to the LLM which will resolve them correctly via `$HOME`. In eval files, the paths are test context descriptions where `~/` is natural shorthand. Evaluate whether the path standards rule should exempt `~/` in behavioral evals (which describe scenarios, not execute paths) while keeping the flag for prompt files.

**Observations:**
- 5 instances in workflow.md (lines 159, 212, 224, 305, 306, 308, 597, 599)
- 8 instances across eval files (eval-decline-path, eval-first-install-consent-and-execution, eval-hash-drift-warning, eval-version-match-skip)
- 2 prompt files at skill root instead of references/ (workflow.md, workflow-runtime.md)

## Strengths

**Voice-as-architecture.** The KITT/Optimus Prime archetype is not decorative — it is structural. The greeting templates, proactive-offer pattern, hub-and-spoke synthesis, and "raised eyebrow" hygiene checks are capabilities designed from the voice outward. Most agents bolt personality onto functionality; Impetus builds functionality from personality. The banned-phrase list and symbol vocabulary are concrete enough to enforce in evals.

**Best-in-class startup optimization.** The `startup-preflight` script consolidates 6+ file reads and a state machine into a single Bash call that returns pre-rendered greeting fields. The happy path (greeting, no open threads) reaches the developer with exactly one tool call — no workflow.md load, no reference file reads. This is performance engineering applied to agent design.

**Sophisticated no-re-offer pattern.** The context-hash comparison prevents the common anti-pattern of nagging agents while re-surfacing offers when conditions materially change. The hash includes story ref, phase, and git hash — it re-offers when the answer might be different, not when the clock ticks.

**Production-grade input interpretation.** Five tiers (number, letter command, fuzzy continue, natural language with confirmation gate, ambiguous with clarifying question) cover the full input spectrum. The structural gate for natural language dispatch prevents accidental workflow triggers — a subtle but important safety mechanism.

**Consent at every gate.** Install asks before writing. Upgrades ask per version. Hash drift asks restore vs. keep. Dormant threads ask before closing. This is the "deference with dignity" personality principle made structural in every interaction.

**63 behavioral evals.** The eval coverage is extensive and specific — each eval targets a single behavioral contract. This is eval-driven development applied to an orchestrator agent and represents serious investment in quality assurance.

**Zero waste detected.** Pre-pass found zero defensive padding, zero back-references, and zero meta-explanation patterns across all files. The prompt writing is clean and direct throughout.

## Detailed Analysis

### Structure & Capabilities

Impetus uses a non-standard but internally consistent structure: SKILL.md handles hot-path routing and persona, workflow.md handles session lifecycle (install, upgrade, journal, greeting), and workflow-runtime.md handles mid-session behaviors (completion signals, productive waiting, review dispatch, subagent synthesis). All capabilities are embedded in workflow steps rather than separate prompt files — appropriate for an orchestrator that dispatches to other skills rather than performing domain work. The dispatch model is disciplined: 5 named skill targets, no ad-hoc delegation, placeholder messages for unbuilt features. Two prompt files (workflow.md, workflow-runtime.md) sit at the skill root rather than in references/, which deviates from the BMad path convention.

### Persona & Voice

The persona is exceptionally well-differentiated. The "servant-partner in the KITT sense" identity creates a decision framework that applies to every interaction. Voice rules are concrete (6 banned patterns, defined symbol vocabulary, input interpretation categories) and enforced across three files for context-compaction survival. The session-greeting reference elevates the persona with evocative templates that demonstrate the voice in practice. The voice specification across SKILL.md (lines 64-71), workflow.md (lines 79-89), and workflow-runtime.md (line 8) is consistent — repetition serves self-containment, not drift. The missing Overview in SKILL.md means the always-loaded file lacks a mission framing paragraph — on the happy path (which never loads workflow.md), the agent operates without its mission understanding.

### Identity Cohesion

Impetus is one of the most coherent agent designs analyzed. Every capability maps naturally to the identity: hash drift detection embodies "professional displeasure when discipline lapses," consent-before-action embodies the servant-partner role, and hub-and-spoke synthesis embodies the guardian who shields the developer from complexity. The persona-capability alignment is strong across all 16 capabilities inventoried. One minor mismatch: the retro dispatch placeholder surfaces a raw CLI command (`momentum-tools sprint retro-complete`), violating the voice rule against exposing backstage machinery. The "Refine backlog" dispatch target shows inconsistency between SKILL.md (momentum:refine) and session-greeting.md (momentum:create-story) — an audit is needed to determine the canonical target.

### Execution Efficiency

The happy path is near-optimal (1 tool call to first output). Non-happy paths have redundant file reads: Step 1 re-reads files already computed by preflight, Step 9 re-reads momentum-versions.json, and Step 7 re-reads journal.jsonl despite preflight having checked it. The primary optimization is enriching the preflight payload to carry the full data for each route, not just the routing decision — estimated 3-5 fewer tool calls on install/upgrade paths. Install actions execute sequentially (7+ Bash calls for a typical install) where independent file copies could be batched. No circular dependencies or subagent chaining issues detected.

### Conversation Experience

The first-timer experience is strong (ASCII art introduction, consent-based install, emotional weight in greeting) but lacks practice education — the menu assumes familiarity with Momentum concepts. The expert experience is fast but encounters greeting ceremony friction on repeated invocations. The confused user who declines setup has no "what is Momentum?" off-ramp. The edge-case user with messy journals faces accumulated hygiene signals without prioritization. The hostile environment (missing files, broken JSON) is handled gracefully by preflight, but broken momentum-tools.py or missing versions manifest produce silent failures with no guidance. Headless operation is partially adaptable — the CLI tools already return structured JSON, but the interactive skill itself has zero headless support.

### Script Opportunities

Impetus has already demonstrated the right architecture with `startup-preflight`. The remaining script opportunities are concentrated in three areas: install/upgrade action execution (800-1200 tokens saved), journal write + view regeneration (500-700 tokens per write), and journal hygiene checks (300-500 tokens per session). Combined estimated savings: 850-1300 tokens per session with threads, 850-1280 for first install, 1700-2500 for upgrade sessions. The journal-write command has the highest ROI — it fires multiple times per session and eliminates the most fragile LLM behavior.

## Recommendations

1. **Add three momentum-tools.py commands** (install-actions, journal-write, journal-status --hygiene) — resolves 8 script opportunity findings across install, upgrade, and journal paths. High effort, high impact.
2. **Add canonical section wrappers to SKILL.md** (Overview, Identity/Communication Style, Principles, On Activation) — resolves 5 structure findings plus 2 frontmatter naming findings. Low effort, high consistency impact.
3. **Add sprint health summary to preflight greeting data** — resolves the highest-opportunity enhancement finding (EG-4) and transforms the greeting from identity moment to orientation moment. Low effort, high daily-use impact.
4. **Implement hygiene signal triage in Step 11** — resolves 3 findings about signal accumulation and wall-of-text presentation. Medium effort, high impact for complex journal states.
5. **Audit and fix dispatch target for "Refine backlog"** — resolves the cross-reference mismatch between SKILL.md, workflow.md, and session-greeting.md. Low effort.
6. **Add express mode for high-frequency users** — resolves power-user friction finding. Medium effort, medium impact but high satisfaction for daily users.
7. **Add error handling for preflight failure** — resolves the hostile-environment finding about broken momentum-tools.py. Low effort.
8. **Fix retro placeholder to not expose CLI command** — resolves the voice rule violation in dispatch table. Low effort.
