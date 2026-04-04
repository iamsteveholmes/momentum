# Phase 3 PRD Discovery — Findings Report

**Date:** 2026-04-02
**Scope:** 4 Phase 3 stories reviewed against current prd.md
**Stories reviewed:** agent-logging-tool, momentum-dev-simplify, momentum-sprint-planning, momentum-sprint-dev

---

## 1. New Functional Requirements Needed

### FR-NEW-1: Agent Logging Tool

The PRD has zero coverage for structured agent logging. The agent-logging-tool story introduces a foundational capability that all Phase 3 workflows depend on.

**Needed FR:** Every agent (Impetus, dev, QA, E2E Validator, verifiers) must write structured JSONL logs via `momentum-tools log` throughout execution. The tool accepts `--agent`, `--event`, `--detail`, `--story` (optional), and `--sprint` (required) arguments. Valid event types: decision, error, retry, assumption, finding, ambiguity. Logs are append-only, stored at `.claude/momentum/sprint-logs/{sprint-slug}/`. Per-agent exclusive write authority on log files.

**Where in prd.md:** New FR after FR55 (line 686). Belongs in a new "Agent Observability" subsection, or appended to Enforcement & Quality Governance (line 554).

### FR-NEW-2: Gherkin Separation (Specs vs. Story Files)

The PRD mentions Gherkin in FR39/FR40 (lines 601-602) for ATDD, but does not specify the architectural separation between story-file ACs and sprint-scoped Gherkin specs. This is a core design decision (plan decision 30).

**Needed FR:** Story markdown files contain plain English acceptance criteria only. Detailed Gherkin `.feature` specs are generated during sprint planning and written to `sprints/{sprint-slug}/specs/{story-slug}.feature`. Dev agents never access the specs directory. Verifier agents read Gherkin specs exclusively from this path. This enforces black-box behavioral validation.

**Where in prd.md:** New FR in the Specification & Development Workflow section (after FR40, line 602). Also requires updating FR39 to clarify it describes the story-level behavioral ACs, not the full Gherkin specs used for verification.

### FR-NEW-3: Sprint-Level AVFL (Replaces Per-Story/Per-Wave AVFL)

Plan decision 31 moves AVFL from per-story to sprint level. The PRD currently describes AVFL per story wave in FR51 (line 577).

**Needed FR:** AVFL validates the complete sprint plan during sprint-planning (all stories together as one validation pass). During sprint execution, a single AVFL pass runs after ALL stories have merged — not per-story, not per-wave. This catches cross-story integration issues.

**Where in prd.md:** New FR in Verification & Review section (after FR48, line 569), or update FR48 to cover sprint-level AVFL scope.

### FR-NEW-4: Team Composition in Sprint Planning

No existing FR covers team composition. Plan decision 26 (two-layer agent model) and decision 29 (sprint planning builds the team) need FR coverage.

**Needed FR:** Sprint planning determines team composition: which agent roles the sprint needs (based on story change_type and touches), what project-specific guidelines each role receives, and which stories can run concurrently based on the dependency graph. Team composition is stored in the sprint record and read by sprint-dev for execution.

**Where in prd.md:** New FR in a "Sprint Planning & Execution" subsection, or extend the Epic Orchestration section (line 571).

### FR-NEW-5: Dependency-Driven Concurrency

Plan decision 25 replaces wave-based execution with dependency-driven concurrency. No FR covers this model.

**Needed FR:** Sprint execution spawns one agent per unblocked story (stories with no unmet dependencies). When a story completes and merges, sprint-dev checks whether previously blocked stories are now unblocked and spawns agents for those. Dependency ordering is strict — stories never start before all blockers have merged. This replaces rigid wave tiers.

**Where in prd.md:** New FR in Sprint Planning & Execution. Directly contradicts FR51's "tier-sequential DAG" and "wave" model.

### FR-NEW-6: Two-Layer Agent Model

Plan decision 26. No existing FR.

**Needed FR:** Agent guidance uses a two-layer model. Momentum provides generic agent roles (Dev, QA, E2E Validator, Architect Guard) with orchestration patterns, logging requirements, and quality gates. Projects provide role-specific guidelines per role (e.g., stack, conventions, TDD requirements). Sprint planning wires the two layers together for each story based on change_type and touches.

**Where in prd.md:** New FR, likely in a new "Agent Model" subsection or alongside the orchestrating agent FRs (line 536).

### FR-NEW-7: Two-Output Retrospective

Plan decision 27. No existing FR.

**Needed FR:** The retrospective workflow analyzes all agent logs from the sprint and produces two triage outputs: (1) Momentum triage — practice-level issues feeding back into Momentum's own refinement cycle, (2) Project triage — project-level issues feeding back into the project's refinement cycle. Both outputs derive from the same evidence base (agent JSONL logs).

**Where in prd.md:** New FR, potentially in Evaluation Flywheel section (after FR33, line 589) or in a new Sprint Lifecycle section.

### FR-NEW-8: Sprint Planning Workflow

No existing FR covers the sprint planning workflow as a complete process.

**Needed FR:** Sprint planning workflow includes: backlog presentation (grouped by epic, excluding terminal states), story selection (3-8 stories with dependency warnings), story fleshing-out (spawn momentum-create-story for stubs), Gherkin spec generation, team composition, AVFL validation of complete plan, developer review, and sprint activation. Planning decisions logged throughout via agent logging tool.

**Where in prd.md:** New FR in Sprint Planning & Execution section.

### FR-NEW-9: Sprint Execution Workflow

No existing FR covers the sprint execution loop.

**Needed FR:** Sprint execution reads the activated sprint record, creates a task list for progress tracking, spawns momentum-dev agents for unblocked stories (each in its own worktree), tracks completion via tasks, handles dependency-driven sequencing, runs post-merge AVFL, executes black-box verification against Gherkin specs (Phase 3: developer-confirmation checklist), and surfaces a sprint summary. Every merge requires explicit developer confirmation.

**Where in prd.md:** New FR in Sprint Planning & Execution section.

---

## 2. Existing FRs That Need Updates

### FR48 (line 569): AVFL Skill — Scope Update

**Current:** Describes AVFL as spawning parallel reviewers with gate/checkpoint/full profiles. Silent on when/how often AVFL runs relative to stories/sprints.

**Needed change:** Add language clarifying that AVFL runs at sprint level (during planning: validates complete plan; during execution: single pass after all stories merge). Remove any implication of per-story invocation. The profiles (gate/checkpoint/full) remain valid but the invocation context changes.

### FR51 (line 577): `/develop-epic` — Wave Model Obsolete

**Current:** "tier-sequential DAG across the epic's stories... Stories with satisfied dependencies execute in parallel within each tier (wave); AVFL validation is included per story wave."

**Needed change:** This FR uses the wave-based execution model that decision 25 replaces with dependency-driven concurrency. The "wave" concept, "tier-sequential" language, and "per story wave" AVFL all need to be updated. FR51 describes the `/develop-epic` command which is an Epic Orchestration FR (Epic Y) — the sprint-dev workflow module is the Phase 3 equivalent. FR51 may need to be either updated to reflect the new model or marked as superseded, with the sprint-dev workflow covered by new FRs.

**Key conflict:** FR51 says "AVFL validation is included per story wave" — decision 31 says AVFL is sprint-level only.

### FR53 (line 579): `momentum-dev-auto` — Superseded by Simplified momentum-dev

**Current:** Describes `momentum-dev-auto` as "a stripped-down variant of `momentum-dev` with all interactive ask gates removed."

**Needed change:** The momentum-dev-simplify story makes the base momentum-dev into a pure executor (no AVFL, no status transitions, no DoD supplement, no code review offer). This is effectively what `momentum-dev-auto` was supposed to be. FR53 either needs to be updated to reflect that momentum-dev itself is now the stripped-down executor, or needs a note that the simplification story absorbs the intent of momentum-dev-auto. The merge gate still requires developer confirmation (not fully auto), so the distinction between "auto" and "standard" may need rethinking.

### FR54 (line 580): Session Open — `sprint-status.yaml` Reference

**Current:** "Impetus reads `sprint-status.yaml` and renders a 3-line epic progress bar."

**Needed change:** The data source is now `stories/index.json` and `sprints/index.json`, not `sprint-status.yaml`. This was a Phase 1 change (Story 0.2) that should already have been updated. Verify this is current.

### FR55 (line 684-686): Sprint-Manager Write Authority — Tool Model

**Current:** "All writes to sprint-status.yaml go through `momentum-sprint-manager`, an executor subagent spawned by Impetus."

**Needed change:** Sprint-manager is now a Python CLI tool (momentum-tools.py), not an executor subagent. The exclusive write authority principle is correct, but the mechanism is a tool invoked via Bash, not a subagent spawned via Agent. Also, the target files are now `stories/index.json` and `sprints/index.json`, not `sprint-status.yaml`. (Note: this may already be partially addressed by Phase 1/2 work — verify.)

### FR41 (line 603): Story Cycle — Epic-Level Orchestration Language

**Current:** "The epic is the primary unit of planned work — stories are created in bulk by `/create-epic` and executed as a DAG by `/develop-epic`."

**Needed change:** Phase 3 introduces sprint as the primary execution unit (stories pulled from across epics). The `/create-epic` and `/develop-epic` model is the Epic Y orchestration model. FR41 needs to also acknowledge the sprint-based execution model where stories are selected from across epics during sprint planning. The story cycle itself (spec review, implement, review) remains, but the orchestration wrapper changes.

### FR6 (line 538): Impetus as Pure Orchestrator — Menu Items

**Current:** "At the epic orchestration level, the primary menu items are `/create-epic` and `/develop-epic`."

**Needed change:** Phase 3 adds sprint-level menu items: "Plan a sprint" and "Continue sprint" (from the sprint-dev and sprint-planning stories). FR6 should acknowledge both epic-level and sprint-level dispatch.

### Story Status Table (line 665): `review` Status Definition

**Current:** "`review` — Worktree merged to main; awaiting wave AVFL."

**Needed change:** Replace "wave AVFL" with "sprint AVFL" or "post-merge AVFL" to align with decision 25 (teams over waves) and decision 31 (sprint-level AVFL).

### Sprint Status Definitions (line 656): `sprint-status.yaml` Reference

**Current:** References `sprint-status.yaml` as the authoritative state file.

**Needed change:** The data model was decomposed in Story 0.2 into `stories/index.json` and `sprints/index.json`. The section header and description should reference the current file structure. (May already be partially addressed.)

---

## 3. User Journey Updates

### Journey 1 (lines 169-182): First Install and First Sprint

**Current journey describes:** spec review, ATDD, implement, review, flywheel — a single-story cycle. Status graphic shows `[Spec Review] -> ATDD -> Implement -> [Review] -> Flywheel`.

**Needed updates:**
- Sprint planning is now a distinct workflow step before execution. The journey should mention story selection and team composition if it covers sprint-level flow.
- AVFL runs at sprint level, not per-story. The journey's flywheel step at the end of a single story doesn't align with sprint-level AVFL — though the flywheel itself is a separate concept from AVFL.
- The code-reviewer launch is still valid but should note it is part of the sprint-dev verification phase, not a standalone per-story step.
- **Impact: Low.** Journey 1 is about first install UX, not sprint mechanics. Minor language adjustments only.

### Journey Requirements Summary (lines 239-260)

**Missing capabilities that should be added:**
- Agent logging / observability
- Sprint planning workflow (team composition, story selection, Gherkin generation)
- Sprint execution workflow (dependency-driven concurrency, post-merge AVFL)
- Two-output retrospective
- Black-box verification (Gherkin separation)

### No Existing Sprint Planning or Sprint Execution Journey

The current journeys cover: first install (J1), flywheel (J2), stack adaptation (J3), team onboarding (J4). None covers the sprint planning or sprint execution experience.

**Recommendation:** Consider adding a Journey 5 covering sprint planning and execution — or extend Journey 1 to include the full sprint lifecycle. This is not strictly required for PRD completeness but would provide traceability for the 9 new FRs.

---

## 4. Sprint Lifecycle Definition Updates

### Story Stages (lines 658-669)

**Current stages:** backlog, ready-for-dev, in-progress, review, verify, done, dropped, closed-incomplete

**Assessment:** The stage set is correct and does not need changes. The momentum-dev-simplify story removes status-transition calls from momentum-dev but the stages themselves remain. Sprint-dev now manages transitions (in-progress, review, done) via momentum-tools.

**One wording fix needed:** Line 665 — `review` definition says "awaiting wave AVFL." Change to "awaiting sprint AVFL" or "awaiting post-merge AVFL."

### Sprint Lifecycle

**Current in PRD:** Not explicitly defined as a lifecycle. FR52 (line 578) defines the epic lifecycle (Triage, Create-epic, Develop-epic, Retro, Triage). No equivalent sprint lifecycle.

**Needed:** Add a sprint lifecycle definition:
1. **Plan** — story selection, story fleshing-out, Gherkin generation, team composition, AVFL validation, developer approval, activation
2. **Execute** — dependency-driven agent spawning, implementation, merges, progress tracking
3. **Verify** — post-merge AVFL, black-box verification against Gherkin specs
4. **Complete** — sprint archival, summary
5. **Retro** — agent log analysis, two-output triage (Momentum + project)

**Where in prd.md:** Either in the Sprint Status Definitions section (after line 682) or as a new Sprint Lifecycle section.

### Team Composition as Planning Step

**Not currently in any lifecycle definition.** Sprint planning now includes determining which agent roles are needed, assigning project-specific guidelines, and building the dependency graph. This should be reflected in the sprint lifecycle definition.

---

## 5. Gaps — Requirements Implied by Stories with No FR Coverage

### Gap 1: Task-Based Progress Tracking

The sprint-dev story heavily relies on TaskCreate/TaskUpdate/TaskList for tracking sprint progress. Plan decision 23 establishes task tracking as the primary position mechanism. No FR covers this. The PRD should have an FR stating that multi-step workflows use task-based tracking for position and progress that survives context compression.

**Implied by:** momentum-sprint-dev (Phase 2 init, Phase 3 progress loop), plan decision 23.

### Gap 2: Structured Completion Signal from momentum-dev

The momentum-dev-simplify story specifies that momentum-dev emits a structured JSON completion signal (status, files modified, test results). No FR covers the interface contract between executor agents and the orchestration layer.

**Implied by:** momentum-dev-simplify AC "The completion output emits a structured signal (JSON) that the caller can parse."

### Gap 3: Sprint Record Schema (Team Composition + Dependency Graph)

Sprint-dev expects the sprint record in `sprints/index.json` to contain team composition and dependency graph (see sprint-dev dev notes, "Sprint record structure"). No FR defines this schema or requires sprint-planning to produce it.

**Implied by:** momentum-sprint-dev (reads team/dependencies from sprint record), momentum-sprint-planning (writes team composition to sprint record).

### Gap 4: Developer-Confirmation Checklist as Phase 3 Verification

Sprint-dev specifies that Phase 3 verification takes the form of a developer-confirmation checklist derived from Gherkin scenarios — full automated verification is deferred. No FR covers this interim verification mechanism.

**Implied by:** momentum-sprint-dev Phase 5 (Verification), plan decision 11 ("developer-confirmation in Phase 3, cmux-based in Epic 3").

### Gap 5: Error Handling and Recovery in Sprint Execution

Sprint-dev specifies error handling: no active sprint, sprint not locked, agent failure (offer retry/skip), merge conflicts, AVFL critical issues, developer declining verification items. No FR covers graceful degradation or error recovery in sprint execution.

**Implied by:** momentum-sprint-dev error handling section.

### Gap 6: Graceful Log Failures

The momentum-dev-simplify story states: "log calls should not fail if no sprint context exists... Wrap in best-effort execution." This implies that agent logging must be non-blocking and fault-tolerant. No FR covers this resilience requirement.

**Implied by:** momentum-dev-simplify dev notes on graceful log failures.

### Gap 7: Sprint Slug Convention

Sprint-planning defines the slug format as `sprint-YYYY-MM-DD` with sequence suffix for same-day multiples. No FR covers sprint naming/slug conventions.

**Implied by:** momentum-sprint-planning dev notes on sprint slug convention.

### Gap 8: Relationship Between Epic Orchestration (FR49-FR53) and Sprint Model

The PRD has FR49-FR53 for the epic orchestration model (`/create-epic`, `/develop-epic`, epic lifecycle). Phase 3 introduces a sprint-based model that overlaps significantly. The PRD does not clarify: Are these complementary? Does sprint execution supersede `/develop-epic`? Can both coexist? The plan's Phase 3 section says triage/refinement/retro are deferred to Phase 5 and "can be done manually until then" — but the epic FRs describe a complete lifecycle that doesn't mention sprints.

**This is the largest structural gap.** The PRD needs to either: (a) reconcile the epic model with the sprint model, showing how they coexist, or (b) mark the epic orchestration FRs (FR49-FR53) as partially superseded by the sprint model with a clear note about what remains valid.

---

## Summary of Changes by PRD Section

| Section | Line Range | Changes Needed |
|---|---|---|
| Functional Requirements — new subsection | after 569 | FR-NEW-1 through FR-NEW-9 (9 new FRs) |
| FR6 | 538 | Add sprint-level menu items |
| FR41 | 603 | Acknowledge sprint-based execution alongside epic model |
| FR48 | 569 | Clarify sprint-level AVFL scope |
| FR51 | 577 | Replace wave model with dependency-driven concurrency |
| FR53 | 579 | Reconcile momentum-dev-auto with simplified momentum-dev |
| FR54 | 580 | Update data source reference (index.json not sprint-status.yaml) |
| FR55 | 684-686 | Update mechanism (tool not subagent) and file references |
| Story Status Table | 665 | "wave AVFL" -> "sprint AVFL" |
| Sprint Status Definitions | 652-656 | Update sprint-status.yaml references to index.json |
| User Journeys | 239-260 | Add new capabilities to Journey Requirements Summary |
| Sprint Lifecycle | after 682 | Add sprint lifecycle definition |
| Epic vs Sprint | 571-580 | Reconcile epic orchestration model with sprint model |
