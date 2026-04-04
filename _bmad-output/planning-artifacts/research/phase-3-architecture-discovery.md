# Phase 3 Architecture Discovery — Findings Report

**Date:** 2026-04-02
**Scope:** 4 Phase 3 stories reviewed against architecture.md
**Stories reviewed:** agent-logging-tool, momentum-dev-simplify, momentum-sprint-planning, momentum-sprint-dev

---

## 1. Write Authority Table Updates

**Location:** architecture.md lines 953-966 (Read/Write Authority table)

### New rows needed

| Component | Reads | Writes |
|---|---|---|
| momentum-tools log | (none — write-only append) | `.claude/momentum/sprint-logs/{sprint-slug}/*.jsonl` (sole writer per agent file) |
| sprint-planning workflow | stories/index.json, sprints/index.json, story files | `sprints/{sprint-slug}/specs/*.feature` (Gherkin specs), sprint record team composition (via momentum-tools sprint) |
| sprint-dev workflow | sprints/index.json (active sprint, team, deps), stories/index.json, `sprints/{sprint-slug}/specs/*.feature` | Task state (via TaskCreate/TaskUpdate); status transitions (via momentum-tools sprint); sprint completion (via momentum-tools sprint complete) |

### Existing rows that need modification

- **momentum-dev (line 959):** Currently reads "Specs, story files, code" and writes "Code in worktree only." The simplify story removes AVFL invocation, status transitions, DoD supplement, and code review offer. The row needs updating:
  - Reads: remove "Specs" (momentum-dev no longer reads Gherkin specs — it never accesses `sprints/{sprint-slug}/specs/`)
  - Writes: add "sprint-logs (via momentum-tools log)" — momentum-dev now logs decisions throughout execution
  - Writes: remove any implied status-transition capability — momentum-dev no longer writes to stories/index.json or sprints/index.json
  - The row should clarify that momentum-dev emits structured JSON completion output (not just "code in worktree")

- **Impetus (line 957):** Currently reads "sprint-status.yaml, journal.jsonl, specs, findings-ledger.jsonl" and writes "journal.jsonl, journal-view.md." Updates needed:
  - Reads: change "sprint-status.yaml" to "stories/index.json, sprints/index.json" (already partially addressed by Phase 1, but verify)
  - Reads: add "sprint-logs/{sprint-slug}/" (Impetus reads agent logs for retro)
  - Writes: add "sprint-logs (via momentum-tools log)" — Impetus logs its own orchestration decisions per Decision 24
  - Sprint-dev and sprint-planning are Impetus workflow modules (not separate agents) — their writes are effectively Impetus writes via tools

- **momentum-sprint-manager (line 958):** References "sprint-status.yaml" which is deprecated. Should read "stories/index.json, sprints/index.json" — verify this was already updated in Phase 1.

- **momentum-create-story (line 960):** Currently reads "sprint-status.yaml, epics.md." Verify deprecated reference was updated. Also note: create-story no longer runs its own AVFL (per Decision 31 — AVFL at sprint level).

### Rows that may be obsolete or need revision

- **momentum-dev-auto (lines 1254-1272):** The entire momentum-dev-auto section describes a "stripped-down variant of momentum-dev with all ask gates removed." With the Phase 3 redesign, momentum-dev itself is being stripped down to a pure executor. The relationship between momentum-dev (simplified) and momentum-dev-auto needs clarification — are they converging? The momentum-dev-simplify story makes momentum-dev very close to what momentum-dev-auto was designed to be.

---

## 2. New Architectural Components to Document

### 2a. Agent Logging Infrastructure
**Not currently documented in architecture.md.** The plan file (lines 876-887) describes this architecture decision but it has no corresponding section in architecture.md.

Needs a new section documenting:
- **Storage location:** `.claude/momentum/sprint-logs/{sprint-slug}/`
- **File naming:** `{agent-role}.jsonl` (Impetus orchestration log), `{agent-role}-{story-slug}.jsonl` (per-story agent logs)
- **JSONL entry schema:** `{timestamp, agent, story, event, detail}`
- **Event type vocabulary:** decision, error, retry, assumption, finding, ambiguity
- **Write authority model:** Each agent file has exclusive write authority by the agent that created it. Append-only, no reads/modifications.
- **CLI interface:** `momentum-tools log --agent <role> --story <slug> --sprint <slug> --event <type> --detail "..."`
- **Relationship to retrospectives:** Agent logs are the primary input for the retro workflow

**Suggested placement:** New subsection under "Sprint Story Lifecycle" (after line 1150), or as a new top-level section alongside the Sprint Tracking Schema.

### 2b. Gherkin Specs Directory
**Not currently documented in architecture.md.** The specs separation is a new architectural pattern.

Needs documentation of:
- **Location:** `sprints/{sprint-slug}/specs/{story-slug}.feature`
- **Access control:** Verifier agents only — dev agents NEVER access this path
- **Write timing:** Written during sprint planning (Step 4 of sprint-planning workflow), before any code exists
- **Relationship to story ACs:** Story files retain plain English ACs only; Gherkin is never written back to story files
- **Black-box validation pattern:** Specs written pre-implementation, validated post-implementation, by different agents

**Suggested placement:** Under "Sprint Tracking Schema — Folder-Based Model" (after line 1150), extending the folder model to include `sprints/{sprint-slug}/specs/`.

### 2c. Workflow Modules Directory
**Not currently in repo structure tree (lines 840-911).** The sprint-planning and sprint-dev stories both create files under `skills/momentum/workflows/`.

The repo structure tree needs:
```
skills/momentum/
├── SKILL.md
├── workflow.md
├── workflows/                    ← NEW: Workflow modules loaded by Impetus
│   ├── sprint-planning.md
│   └── sprint-dev.md
├── scripts/
│   └── momentum-tools.py
└── references/
```

**Location to update:** Lines 848-859 (Repository Structure, skills/momentum/ subtree)

### 2d. Team Composition in Sprint Records
**Partially documented.** The sprint record schema at lines 1121-1145 shows `waves` but does NOT show `team` composition. The sprint-dev story (lines 166-191) shows an expected sprint record structure with `team.roles`, `team.story_assignments`, and `dependencies` — none of which are in the current architecture schema.

The sprint record schema needs extending:
```json
{
  "team": {
    "roles": [{"role": "dev", "guidelines": "path/to/guidelines.md"}],
    "story_assignments": {"story-slug": {"role": "dev"}}
  },
  "dependencies": {
    "story-slug": ["dependency-slug"]
  }
}
```

**Location to update:** Lines 1121-1145 (Sprint Tracking Schema, sprints/ folder)

### 2e. momentum-tools.py in Component Inventory
**Partially documented.** The architecture references momentum-sprint-manager as an "executor subagent" (line 958, line 1082) but the Phase 2 decision converted it to a CLI tool. The Phase 1 plan file documents this transition (lines 815-830), but architecture.md still says "executor subagent" in multiple places. Additionally, the `log` subcommand is not documented.

**Locations referencing sprint-manager as subagent:**
- Line 958: "momentum-sprint-manager" row in write authority table
- Line 1082: "momentum-sprint-manager — an executor subagent with exclusive write authority"
- Line 1152: "momentum-sprint-manager is the sole writer"

These should reference `momentum-tools.py sprint` (a CLI tool) rather than `momentum-sprint-manager` (an executor subagent).

---

## 3. Existing Sections That Need Updates

### 3a. Epic Orchestration Architecture (lines 1206-1293)
**Major revision needed.** This entire section describes the pre-redesign model:

- **Lines 1210-1217 (lifecycle):** Shows `/create-epic` and `/develop-epic` commands which are replaced by `momentum:plan-sprint` and `momentum:sprint-dev` workflow modules. The lifecycle model changes from epic-centric to sprint-centric.

- **Lines 1221-1231 (DAG Topology):** Describes "tier-sequential execution" with rigid wave-based tiers. Per Decision 25, this is replaced by dependency-driven concurrency ("teams over waves"). Stories are spawned based on dependency resolution, not wave numbers. The wave concept in the sprint record may be informational but execution is dependency-driven.

- **Lines 1234-1250 (Agent Pool Governance):** References "AVFL embedding" within each story agent. Per Decision 31 and the momentum-dev-simplify story, AVFL no longer runs per-story — it runs once after ALL sprint stories merge. The "pool cap" concept may still apply but the model is different.

- **Lines 1254-1272 (momentum-dev-auto):** Describes a background-safe variant with AVFL GATE_FAILED handling. With momentum-dev simplified (no AVFL, no status writes), the distinction between momentum-dev and momentum-dev-auto narrows significantly. This section needs either removal or reconciliation.

- **Lines 1276-1292 (dag-executor Integration):** References `sprint-status.yaml` and tier-based execution. The dag-executor concept may still be relevant but the integration model changes with the teams-over-waves approach.

### 3b. Sprint Execution Flow
**No dedicated section exists.** The sprint-dev workflow introduces a 6-phase execution model (Initialization, Team spawn, Progress tracking loop, Post-merge quality gate, Verification, Sprint completion) that has no architectural documentation. The closest thing is the "Parallel Story Execution Model" at lines 1188-1202, which describes worktree mechanics but not the orchestration flow.

**Needed:** A new section (or major revision of lines 1206-1293) documenting the sprint execution lifecycle as implemented by sprint-dev.

### 3c. Next-Story Selection Rule (lines 1154-1161)
**Obsolete.** References `sprint-status.yaml` and a priority-ordering model where momentum-dev autonomously selects its next story. In the new model, momentum-dev does NOT select stories — sprint-dev (an Impetus workflow) reads the active sprint, resolves dependencies, and spawns momentum-dev with a specific story. Story selection moves from momentum-dev to the sprint-dev workflow.

### 3d. Story State Machine (lines 1051-1082)
**Partially stale.** Line 1062 says `review` is "awaiting wave AVFL (automated batch after all wave merges)" — should say "awaiting sprint-level AVFL (after all sprint stories merge)" per Decision 25/31. The `verify` description at line 1063 references "momentum-verify" which is a deferred skill — Phase 3 uses developer-confirmation checklist.

### 3e. Subsystem 5 — Subagent Composition (line 71)
**Needs update.** Currently lists only code-reviewer and architecture-guard as subagents. momentum-dev is also a subagent (spawned by Impetus via sprint-dev workflow). The two-layer agent model (Decision 26) with generic roles + project guidelines is not reflected here.

### 3f. Subsystem 7 — Impetus (line 75)
**Needs update.** Does not mention workflow modules, sub-command dispatch (`momentum:plan-sprint`, `momentum:sprint-dev`), or that Impetus loads and follows workflow module documents. Decision 19 establishes this pattern but it's not in the subsystem description.

### 3g. Repository Structure — Installed Structure (lines 922-947)
**Needs sprint-logs directory.** The `.claude/momentum/` subtree currently shows only `journal.jsonl`, `journal-view.md`, and `installed.json`. It needs:
```
.claude/momentum/
├── journal.jsonl
├── journal-view.md
├── installed.json
└── sprint-logs/                  ← NEW
    └── {sprint-slug}/
        ├── impetus.jsonl
        ├── dev-{story-slug}.jsonl
        └── ...
```

### 3h. Protection Boundaries (lines 970-974)
**May need addition.** `sprints/{sprint-slug}/specs/` should potentially be a protected path — dev agents must never write to it (only sprint-planning writes; only verifiers read). This is an access control rule, not just a convention.

---

## 4. New Architecture Decisions to Document

The architecture.md does not have a numbered "Architecture Decisions" registry, but it does embed decisions inline. The plan file (lines 758-791) documents Decisions 24-31 which need architectural representation:

### Decision 24: Agent Logging as Foundational Infrastructure
- Every agent writes JSONL logs via momentum-tools log
- Logs are primary input for retrospectives
- Per-agent exclusive write authority
- Storage: `.claude/momentum/sprint-logs/{sprint-slug}/`
- **Not yet in architecture.md.** Needs a new section.

### Decision 25: Teams Over Waves
- Dependency-driven concurrency replaces rigid wave tiers
- Impetus spawns agents for unblocked stories, spawns more as dependencies complete
- Conflicts with: DAG Topology section (lines 1221-1231), Agent Pool Governance (lines 1234-1250)
- **Requires rewrite** of the Epic Orchestration Architecture section.

### Decision 26: Two-Layer Agent Model
- Momentum provides generic roles (Dev, QA, E2E Validator, Architect Guard)
- Projects provide role-specific stack guidelines
- Sprint planning wires layers together
- **Not in architecture.md.** Needs a new section, likely under or replacing Agent Pool Governance.

### Decision 27: Two-Output Retro
- Retro produces Momentum triage + Project triage from agent logs
- **Not in architecture.md.** Could be deferred since retro is Phase 5, but the architectural pattern should be noted since sprint-logs infrastructure (Phase 3) is designed to support it.

### Decision 29: Sprint Planning Builds the Team
- Story selection, create-story, team composition, dependency graph, execution plan
- Sprint record stores team + dependencies (not just wave assignments)
- **Not in architecture.md** beyond the basic sprint record schema.

### Decision 30: Gherkin Separation
- Story files: plain English ACs (dev sees intent)
- Sprint specs: detailed Gherkin .feature files (verifiers only)
- Black-box behavioral validation
- **Not in architecture.md.** Needs a new section documenting the separation pattern and its rationale.

### Decision 31: AVFL at Sprint Level
- AVFL validates complete sprint plan during planning (all stories together)
- AVFL runs once after ALL stories merge (not per-story)
- Per-story AVFL removed from create-story and momentum-dev
- **Conflicts with:** AVFL embedding in Agent Pool Governance (line 1239), momentum-dev-auto GATE_FAILED handling (lines 1263-1267)
- **Requires revision** of multiple sections.

---

## 5. Gaps and Conflicts Between Stories and Existing Architecture

### 5a. CONFLICT: Wave-based vs. dependency-driven execution
**Architecture says (lines 1221-1231):** "Tier-sequential execution" — dispatch tier-0 wave, wait for ALL stories + AVFL, advance to tier-1.
**Stories say:** Dependency-driven concurrency. Stories spawn as their specific deps complete. No waiting for an entire tier.
**Resolution:** Rewrite the DAG Topology and Epic Orchestration sections to reflect the teams-over-waves model.

### 5b. CONFLICT: AVFL per-story vs. per-sprint
**Architecture says (line 1239):** "Each story's AVFL runs within that story's agent execution context before the story emits its completion signal."
**Stories say:** momentum-dev has NO AVFL. AVFL runs once after ALL sprint stories merge (sprint-dev Phase 4).
**Resolution:** Remove AVFL embedding from Agent Pool Governance. Document AVFL as a sprint-dev post-merge step.

### 5c. CONFLICT: momentum-sprint-manager as subagent vs. CLI tool
**Architecture says (line 958, 1082):** "momentum-sprint-manager — an executor subagent with exclusive write authority."
**Stories say:** Sprint operations go through `momentum-tools.py sprint` CLI (a Python script, not a subagent). The sprint-manager executor subagent was superseded in Phase 2.
**Resolution:** Update all references from "momentum-sprint-manager subagent" to "momentum-tools.py sprint subcommand." Write authority is preserved but the mechanism changed.

### 5d. CONFLICT: momentum-dev-auto vs. simplified momentum-dev
**Architecture says (lines 1254-1272):** momentum-dev-auto is a separate stripped-down variant for background execution.
**Stories say:** momentum-dev itself is being stripped of AVFL, status transitions, DoD supplement, and code review. It becomes a pure executor that returns structured JSON.
**Gap:** The stories don't mention momentum-dev-auto at all. After simplification, momentum-dev and momentum-dev-auto have heavily overlapping scope. The architecture needs to clarify whether momentum-dev-auto is still needed or has been subsumed.

### 5e. CONFLICT: Next-Story Selection Rule
**Architecture says (lines 1154-1161):** momentum-dev reads sprint-status.yaml and autonomously selects the highest-priority ready story.
**Stories say:** momentum-dev receives its story assignment from sprint-dev (which resolves dependencies and spawns agents). momentum-dev does not select stories.
**Resolution:** The Next-Story Selection Rule section should be revised or removed. Story selection moves to the sprint-dev workflow.

### 5f. GAP: Workflow module loading pattern not documented
The stories reference Impetus loading workflow module documents (`skills/momentum/workflows/sprint-planning.md`, `skills/momentum/workflows/sprint-dev.md`) — a pattern where Impetus reads a markdown instruction file and follows it step by step. This pattern has no architectural documentation. It needs a section explaining:
- What a workflow module is (instruction document, not a skill)
- How Impetus loads them (Read tool on the file path)
- How they differ from skills (no SKILL.md, no frontmatter, no separate agent context)
- Where they live (`skills/momentum/workflows/`)

### 5g. GAP: sprint-logs not in .gitignore or protection boundaries
Agent logs at `.claude/momentum/sprint-logs/` are runtime artifacts. The architecture should note:
- Whether sprint-logs should be gitignored (likely yes — they're per-execution, not committed artifacts)
- Whether they need protection boundaries (agents should only write their own logs)

### 5h. GAP: Sprint record schema incomplete
The sprint record schema at lines 1121-1145 shows only `stories`, `locked`, `started`, `completed`, and `waves`. The sprint-dev story expects `team` (roles + story_assignments) and `dependencies` in the record. The schema needs extending.

### 5i. GAP: `--sprint` argument in logging tool
The agent-logging-tool story requires `--sprint` as a mandatory argument, but momentum-dev-simplify says "momentum-dev can still be invoked standalone — the logging calls should not fail if no sprint context exists." These two stories have a minor tension: the tool requires `--sprint`, but standalone invocation has no sprint. The logging tool story's AC says "--sprint is rejected with a clear error" but the simplify story says logging "should not fail." Resolution: the simplify story wraps log calls in best-effort execution (its own AC covers this), so the tension is handled at the caller level, not the tool level.

### 5j. GAP: `sprints/{sprint-slug}/specs/` directory not in repo or installed structure trees
The Gherkin specs directory is a new runtime artifact location that doesn't appear in either the repository structure (lines 840-911) or the installed structure (lines 922-947). It's written during sprint planning and read during sprint verification. Needs placement in the structure trees.

### 5k. STALE REFERENCE: sprint-status.yaml throughout
Multiple sections still reference `sprint-status.yaml` which was deprecated in Phase 1:
- Line 957 (Impetus reads row)
- Line 958 (sprint-manager reads row)
- Line 1082 (status update authority)
- Lines 1156-1157 (Next-Story Selection Rule)
- Line 1222 (DAG Topology)
- Line 1280 (dag-executor Integration)

These should all reference `stories/index.json` and `sprints/index.json` instead. Some may have been addressed in Phase 1 updates — verify before changing.
