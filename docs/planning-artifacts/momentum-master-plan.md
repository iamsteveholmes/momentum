# Momentum Master Plan

**Last updated:** 2026-04-04
**Source plans:** `~/.claude/plans/ethereal-popping-sun.md` (redesign), `~/.claude/plans/dapper-scribbling-hejlsberg.md` (Phase 3 execution)
**Authoritative for:** model, status, architecture decisions, and roadmap

---

## Part 1: The Model

### Core Distinction: Epics vs Sprints

**Epic = Category** -- themed container for related stories. Long-lived, evolves via backlog refinement. A sprint does NOT complete an epic -- it pulls some stories from it. Multiple epics exist simultaneously, always.

**Sprint = Unit of Work** -- N stories pulled from across epics based on priority, dependencies, or low-hanging fruit. One active sprint at a time. Active sprint is **immutable** once activated. Planning sprint is fully mutable until activated.

**Story backlog inside epics** -- stories exist within epics as backlog entries before having story files. Story files are created during sprint planning (or on demand).

### Story Stages

```
backlog           exists in epics.md / stories/index.json, no story file yet
ready-for-dev     story file created, waiting to be picked into a sprint
in-progress       dev agent actively working it
review            merged to main -- awaiting AVFL quality gate
verify            AVFL passed -- behavioral verification running
done              verified, complete
dropped           removed -- obsolete or duplicate
closed-incomplete sprint force-closed before completion; migrated to next sprint or dropped
```

### Story IDs

Globally unique kebab-case slugs. No epic encoding.

```
Good:  posttooluse-lint-hook
Good:  impetus-identity-redesign
Bad:   3-1-posttooluse-lint-hook   (encodes epic, breaks on triage moves)
```

Collision resolution: add short qualifier suffix (`auth-refresh-api` vs `auth-refresh-ui`). Sprint and epic have both name (display label) and slug (key).

### 16-Block Fill Bar

```
backlog       ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  (hatched -- not in sprint)
ready-for-dev ░░░░░░░░░░░░░░░░  (empty -- waiting)
in-progress   ████████░░░░░░░░
review        ████████████░░░░
verify        ██████████████░░
done          ████████████████
```

### Plugin Model (adopted 2026-04-03)

Momentum is a Claude Code plugin. The plugin manifest lives at `.claude-plugin/plugin.json` in the plugin root. The `name` field (`"momentum"`) determines the namespace prefix for all skills.

**Plugin root layout:**

```
skills/momentum/                     <- Plugin root
├── .claude-plugin/
│   └── plugin.json                  <- { "name": "momentum" }
├── skills/
│   ├── impetus/SKILL.md            <- Orchestrator (/momentum:impetus)
│   ├── sprint-planning/SKILL.md    <- /momentum:sprint-planning
│   ├── sprint-dev/SKILL.md         <- /momentum:sprint-dev
│   ├── dev/SKILL.md                <- /momentum:dev
│   ├── avfl/SKILL.md               <- + sub-skills/ and references/
│   ├── create-story/SKILL.md
│   ├── plan-audit/SKILL.md
│   ├── sprint-manager/SKILL.md
│   ├── agent-guidelines/SKILL.md
│   ├── code-reviewer/SKILL.md      <- context: fork, allowed-tools: Read
│   ├── architecture-guard/SKILL.md  <- context: fork, allowed-tools: Read
│   └── upstream-fix/SKILL.md
├── hooks/
│   └── hooks.json                   <- Always-on hooks (active on install)
├── scripts/
│   └── momentum-tools.py
└── references/
    ├── rules/                       <- Written to ~/.claude/rules/ by Impetus
    ├── practice-overview.md
    ├── phase-guide.md
    └── momentum-versions.json
```

**Install experience:**

```bash
claude plugin add momentum
/momentum:impetus              # Primary entry point -- session orientation, first-run setup
```

Plugin install delivers all skills, hooks, scripts, and references. Hooks activate immediately. Rules require Impetus to write them to `~/.claude/rules/` and `.claude/rules/` on first invocation (plugins cannot write outside their own directory).

### User-Facing Skills

| Skill | Purpose |
|-------|---------|
| `/momentum:impetus` | Session start -- orient, route to appropriate workflow |
| `/momentum:sprint-planning` | Pick stories, build team, activate sprint |
| `/momentum:sprint-dev` | Execute sprint -- dependency-driven story execution with Agent Teams |
| `/momentum:retro` | Sprint retrospective -- review logs, close sprint (Phase 5) |
| `/momentum:triage` | Log observations or run triage session (Phase 5) |
| `/momentum:refine` | Expert backlog grooming with PM + Architect (Phase 5) |

All skills are invocable directly or through Impetus menu routing. Direct invocation skips session orientation.

### Orchestration Architecture

Impetus is the sole orchestrator. His role: **Communicate, Orchestrate, Delegate.** Hub-and-spoke voice model -- Impetus is the only agent that speaks to the user. Subagents return structured JSON; Impetus synthesizes into his own voice.

**Two kinds of things in the architecture:**

1. **Skills** -- proper SKILL.md files that Impetus invokes or the user invokes directly. Multi-step workflows with their own state management.
2. **Executor subagents** -- spawned by skills via Agent tool. Each has exclusive write authority over designated files. Always first-level -- no nesting.

**Write authority model:**
- Impetus reads but NEVER writes files (Phase 4: `allowed-tools: Read, Glob, Grep, Agent, Bash`)
- Each executor subagent has exclusive write authority over designated files
- Reads are free -- any agent reads anything

**Executor subagent roster:**

| Subagent | Writes | Responsibility |
|----------|--------|---------------|
| `momentum:dev` | Code in working directory | Story implementation via bmad-dev-story + logging |
| `momentum:sprint-manager` | `stories/index.json`, `sprints/index.json` | Status transitions, sprint lifecycle (via momentum-tools CLI) |
| `momentum:create-story` | Story files in `_bmad-output/` | Creates story files from backlog entries |
| `momentum:avfl` | Validation reports | Sprint-level AVFL on merged codebase |
| `momentum:code-reviewer` | Findings report | Adversarial code review (context:fork, read-only) |
| `momentum:architecture-guard` | Drift report | Pattern drift detection (context:fork, read-only) |

### Agent Teams Model (adopted 2026-04-03)

Sprint execution uses Claude Code Agent Teams. Key properties:

- **Teams over waves** -- dependency-driven concurrency replaces rigid wave tiers
- **Sequential within a team** -- stories execute one at a time within a single team session
- **Commit-as-sync-point** -- each story completes with a git commit before the next begins; no worktree needed within a team
- **Parallel execution** of independent stories requires separate terminal sessions
- **Two-layer agent model** -- Momentum provides generic roles (Dev, QA, E2E Validator, Architect Guard); projects provide stack-specific guidelines per role
- **Skill loading** -- teammates get workflow instructions through spawn prompts (not SKILL.md frontmatter)
- **Sprint planning wires the layers** -- for each story, determine which roles apply based on `change_type` and `touches`, then attach the project's guidelines

### intake-queue.jsonl Event Log

Append-only event log for observations and issues. Events escalate to stories when patterns emerge.

```jsonl
{"id":"evt-20260331-001","timestamp":"2026-03-31T14:23:00Z","type":"observation","description":"...","context":"session-open","status":"open","escalated_to":null}
```

| Field | Values |
|-------|--------|
| `type` | `observation`, `issue`, `escalation` |
| `status` | `open`, `watching`, `escalated` |
| Sole writer | `momentum:triage` |
| Path | `_bmad-output/implementation-artifacts/intake-queue.jsonl` |

### Task Tracking

All workflows with 3+ steps MUST create tasks at entry. Claude Code's TaskCreate/TaskUpdate/TaskList provide structural state that survives context compression.

- **Tasks** answer "where am I?" -- structural, session-scoped, survives compression
- **Journal** answers "what happened and why?" -- narrative, persists across sessions
- Use `activeForm` for status line clarity (present continuous: "Building wave plan...")
- Use `blockedBy` for sequential phases
- Call `TaskList` at session-open to detect interrupted workflows

### Data Flow: Who Reads/Writes What

| File | Reads | Sole Writer |
|------|-------|-------------|
| `stories/index.json`, `sprints/index.json` | Impetus, all skills | `momentum-tools.py sprint` CLI |
| `intake-queue.jsonl` | `momentum:triage`, `momentum:refine` | `momentum:triage` |
| Story files (`_bmad-output/`) | All skills | `momentum:create-story` |
| Agent logs (`.claude/momentum/sprint-logs/`) | Impetus, `momentum:retro` | Each agent writes own log via `momentum-tools log` |
| `journal.jsonl` | Impetus | Impetus |
| `epics.md`, `prd.md`, `architecture.md` | Impetus, `momentum:refine` | `momentum:refine` |

### Sprint Lifecycle

```
backlog (mutable)
  -> /momentum:sprint-planning (story selection + team composition + Gherkin specs + AVFL)
  -> /momentum:sprint-dev (dependency-driven execution + post-merge AVFL + team review + verification)
  -> /momentum:retro (structured handoff from agent logs)
  -> backlog (next cycle)
```

**Sprint immutability rule:** Once `momentum-tools sprint activate` is called, the sprint is locked. No patching in-place. Recovery: close sprint (`closed-incomplete`), migrate incomplete stories to next sprint backlog.

---

## Part 2: What's Done

### Phase 1 -- Epic 0 Redesign Foundation (Complete, 2026-04-02)

| Story | What |
|-------|------|
| `story-id-migration` | 70 story keys renamed from `N-N-slug` to kebab-case slugs. 34 files renamed. Zero collisions. |
| `sprint-status-decomposition` | Monolithic sprint-status.yaml decomposed into `stories/index.json` (68 entries), `sprints/index.json`, epics.md trimmed to 595 lines. |
| `sprint-manager-skill` | `momentum-sprint-manager/` executor with 5 actions, state machine reference, 3 evals. |

### Phase 2 -- Impetus Core (Complete, in review)

| Story | What |
|-------|------|
| `momentum-tooling` | Python CLI (`momentum-tools.py`) with 5 sprint subcommands + version check. 95 tests. Supersedes sprint-manager agent -- deterministic logic moved from agent to tool. |
| `impetus-identity-redesign` | KITT-like servant-partner character. Identity section + refined greeting. |
| `session-open-sprint-view` | 3-mode sprint detection, 16-block fill bars, context menus. |

Key architecture decision from Phase 2: **deterministic logic goes to tools/scripts; judgment-requiring work goes to agents.**

### Phase 3 -- Sprint Execution

**Round 1 (Complete, in review):**

| Story | What | QA/Validator |
|-------|------|--------------|
| `agent-logging-tool` | `log` subcommand added to momentum-tools.py. 6 event types (decision, error, retry, assumption, finding, ambiguity). 95 tests (65 sprint + 30 log). | QA 8/8, Validator 17/17 |

**Round 2 (Complete, in review):**

| Story | What | QA/Validator |
|-------|------|--------------|
| `momentum-dev-simplify` | Stripped AVFL, status transitions, DoD, code review from momentum-dev. Added agent logging. 314 to 210 lines. Pure executor. | QA 8/8, Validator 19/20 |
| `momentum-sprint-planning` | New skill (342 lines, 8 steps). Backlog display, story selection, create-story on stubs, Gherkin spec generation, team composition, AVFL on plan, developer review, sprint activation. | QA 16/16, Validator 29/30 |

**Round 3 (In progress, separate session):**

| Story | What |
|-------|------|
| `momentum-sprint-dev` | Sprint execution skill. 7-phase model: initialization, team spawn, progress tracking, post-merge AVFL, team review, verification, sprint completion. Story file + 28 Gherkin scenarios exist. |

**Round 4 (Pending):**
- Post-merge AVFL on full codebase
- Transition all Phase 3 stories to `done`

### Plugin Model Adoption (Complete, 2026-04-03)

Architecture and PRD updated for Claude Code plugin model. All skill names use `momentum:` namespace. AVFL 2-lens checkpoint: 8 findings found and fixed. Committed as `d3d011a`.

### Agent Guidelines Skill (Complete, 2026-04-03)

`momentum:agent-guidelines` -- 5-phase technology guidelines generator with 4 discovery subagents. Creates path-scoped rules and reference docs for the two-layer agent model. Evidence-based instruction budget (~100-150 slots). Committed as `0de3abd`.

### AVFL Corpus Mode (Complete, 2026-04-03)

AVFL corpus mode for multi-document cross-validation. Committed as `924d4ef`.

### Sprint-Dev Team Review Phase (Complete, 2026-04-04)

Option C adopted: 7-phase execution model with Team Review phase between AVFL and Verification. QA, E2E Validator, and Architect Guard run in parallel on integrated codebase post-merge. Committed as `45dc0a0`.

### Gherkin Specs

Location: `_bmad-output/implementation-artifacts/sprints/phase-3-sprint-execution/specs/`

| Spec | Scenarios |
|------|-----------|
| `agent-logging-tool.feature` | 17 |
| `momentum-dev-simplify.feature` | 20 |
| `momentum-sprint-planning.feature` | 30 |
| `momentum-sprint-dev.feature` | 28 |

---

## Part 3: What's Next

### Immediate

1. **Phase 3 Round 3:** `momentum-sprint-dev` implementation (in progress in separate session)
2. **Plugin Migration:** Restructure `skills/` directory to match plugin model

### Plugin Migration Plan (6 phases)

1. Create plugin skeleton (`.claude-plugin/plugin.json`) + relocate Impetus content into `skills/impetus/`
2. Move 9 satellite skills into plugin (strip `momentum-` prefix from directory names)
3. Consolidate scripts and hooks at plugin root
4. Update all cross-references (SKILL.md name fields, workflow paths, convention docs)
5. Clean up symlinks and plugin registration
6. Update eval references

### After Plugin Migration

- **Phase 3 Round 4:** Post-merge AVFL, transition all Phase 3 stories to done
- **Phase 4:** `allowed-tools` restriction on Impetus (`Read, Glob, Grep, Agent, Bash`)

### Deferred to Phase 5

| Item | Type |
|------|------|
| `momentum:triage` | Intake workflow (manual until then) |
| `momentum:refine` | Backlog grooming with PM + Architect (manual until then) |
| `momentum:retro` | Sprint retrospective (manual until then) |
| `momentum-triage-writer-tool` | Triage subcommands for momentum-tools.py |
| `momentum-create-story-update` | Remove AVFL checkpoint, add Gherkin generation |
| `momentum-verify-skill` | Automated behavioral verification (Phase 3 uses developer-confirmation) |

### Future Epics

| Epic | Focus |
|------|-------|
| Epic 3 | Quality hooks -- PostToolUse lint, PreToolUse file protection, stop-gate |
| Epic 4 | Complete story cycles -- code review, architecture guard, full verify |
| Epic 6 | Findings MCP -- structured query over findings-ledger.jsonl |
| Epic 7 | Bring your own tools -- extensible tool integration |
| Epic 8 | AVFL corpus mode + momentum-research skill |
| Epic 9 | momentum-research skill |

---

## Part 4: Architecture Decisions

### Storage and State (Decisions 1a-1d)

| # | Decision | Summary |
|---|----------|---------|
| 1a | Provenance graph | Pure YAML frontmatter. `derives_from` in each doc, `referenced_by` computed on demand. Content hashes via `git hash-object`. One-hop propagation, human-gated. |
| 1b | Session journal | `.claude/momentum/journal.jsonl`. JSONL append-only. Auto-generated `journal-view.md` for readability. Concurrency-safe (POSIX atomic append). |
| 1c | Findings ledger | `~/.claude/momentum/findings-ledger.jsonl`. Global JSONL. Cross-project pattern detection. Fields: severity, pattern_tags, upstream_fix_level. |
| 1d | Installed state | `.claude/momentum/installed.json` (project) + `~/.claude/momentum/global-installed.json` (machine). Per-component-group versioning. |

### Security and Integrity (Decisions 2a-2b)

| # | Decision | Summary |
|---|----------|---------|
| 2a | File protection targets | PreToolUse blocks on: `tests/acceptance/`, `**/*.feature`, `_bmad-output/planning-artifacts/*.md`, `.claude/rules/`. |
| 2b | Provenance integrity | Agents may not remove `derives_from` frontmatter. Claims classified as SOURCED / DERIVED / ADDED / UNGROUNDED. |

### Agent Communication and Orchestration (Decisions 3a-3d)

| # | Decision | Summary |
|---|----------|---------|
| 3a | VFL parallel execution | Main context orchestration. AVFL flat skill spawns up to 8 concurrent validators (2 per lens x 4 lenses). Sub-skills: validator-enum (sonnet/medium), validator-adv (opus/high), consolidator (haiku/low), fixer (sonnet/medium). |
| 3b | Hub-and-spoke voice | Impetus is the only agent that speaks to the user. Subagents return structured JSON. Confidence weighting on synthesis. |
| 3c | MCP servers | Deferred to Epic 6. Findings MCP provides structured query over ledger. |
| 3d | Orchestrator purity | Impetus MUST NOT perform development, evaluation, testing, or validation. Prohibited: code writing, test execution, eval running, code review, findings generation. |

### Workflow and UX (Decisions 4a-4c)

| # | Decision | Summary |
|---|----------|---------|
| 4a | Visual progress format | `checkmark Built / arrow Now / circle Next`. Never `Step N/M`. Always narrative. |
| 4b | Session orientation | Impetus reads journal and within two exchanges surfaces: active story, current phase, last action, suggested next. |
| 4c | Productive waiting | Behavioral, not mechanical. Impetus briefs before subagent launch, synthesizes after. No inter-agent messaging API exists. `run_in_background: true` for shell commands only. |

### Packaging and Deployment (Decisions 5a-5c)

| # | Decision | Summary |
|---|----------|---------|
| 5a | Global rules deployment | Bundled in plugin `references/rules/`. Impetus writes to `~/.claude/rules/` and `.claude/rules/` on first run. |
| 5b | BMAD enhancement touch points | Gate: dev-story acceptance tests. Proposals: `derives_from` frontmatter, code-reviewer pass, findings in retro. |
| 5c | Installation and upgrade manifest | `momentum-versions.json` (bundled actions), `global-installed.json` (machine state), `installed.json` (project state). Action types: add, replace, delete, migration. Per-component-group versioning. |

### Phase 3 Decisions (24-33)

| # | Decision | Phase | Summary |
|---|----------|-------|---------|
| 24 | Agent logging | Phase 3 | Every agent writes JSONL logs via `momentum-tools log`. 6 event types. Primary input for retrospectives. |
| 25 | Teams over waves | Phase 3 | Dependency-driven concurrency. Sprint-dev spawns agents for unblocked stories, spawns more as dependencies complete. Wave assignments are informational. |
| 26 | Two-layer agent model | Phase 3, updated 2026-04-03 | Momentum generic roles + project stack guidelines. Teammates get instructions via spawn prompt. Agent Teams: shared working directory, sequential execution, commit-as-sync-point. |
| 27 | Two-output retro | Phase 3 | Retro produces Momentum triage (practice improvements) + Project triage (project findings) from agent logs. |
| 28 | Triage vs refinement | Phase 3 | Triage = intake (analyze, create stubs, initial priority). Refinement = organization (classify, prioritize, gap-analyze). |
| 29 | Sprint planning builds the team | Phase 3 | Story selection, create-story, team composition, dependency graph, execution plan. Sprint record stores team + dependencies. |
| 30 | Gherkin separation | Phase 3 | Plain English ACs in story files (dev). Detailed `.feature` files in `sprints/{slug}/specs/` (verifiers only). Black-box validation. |
| 31 | AVFL at sprint level | Phase 3 | Single AVFL pass after ALL stories merge. Per-story AVFL removed from create-story and dev. Catches cross-story integration issues. |
| 32 | Plugin model | 2026-04-03 | Momentum is a Claude Code plugin with `momentum:` namespace. `.claude-plugin/plugin.json` manifest. All skills, hooks, scripts delivered by plugin install. |
| 33 | Agent Teams for sprint execution | 2026-04-03 | Shared working directory. Commit-as-sync-point. No worktree within team. Parallel execution requires separate terminal sessions. |

---

## Part 5: Sprint Execution Detail

### Sprint Planning (8 steps)

1. **Backlog presentation** -- read stories/index.json, group by epic, exclude terminal states
2. **Story selection** -- developer selects 3-8 stories
3. **Story fleshing-out** -- spawn `momentum:create-story` for each stub; developer approves each
4. **Gherkin spec generation** -- write `.feature` files to `sprints/{sprint-slug}/specs/`
5. **Execution plan and team composition** -- analyze stories for roles, guidelines, dependency graph
6. **AVFL validation** -- single pass on complete sprint plan (Decision 31)
7. **Developer review** -- present full plan for approval
8. **Sprint activation** -- `momentum-tools sprint activate`

### Sprint Execution (7 phases)

**Phase 1: Initialization**
- Read active sprint from `sprints/index.json`; validate locked state
- Build dependency graph from story `depends_on` fields
- Create tasks via TaskCreate for progress tracking

**Phase 2: Team Spawn**
- Identify unblocked stories
- Transition each to `in-progress` via `momentum-tools sprint status-transition`
- Execute sequentially within a team session (commit-as-sync-point)
- Parallel execution of independent stories requires separate terminal sessions

**Phase 3: Progress Tracking Loop**
- Monitor via task status
- On completion: propose merge to developer (merge gate -- never auto-execute)
- After merge: transition to `review`, re-evaluate dependency graph, spawn newly unblocked stories

**Phase 4: Post-Merge Quality Gate (Decision 31)**
- Single AVFL pass on full codebase (all sprint changes together)
- Catches cross-story integration issues
- If findings: present to developer, iterate fixes

**Phase 5: Team Review**
- QA Agent -- reviews merged code against all sprint story ACs
- E2E Validator -- validates behavior against Gherkin specs (black-box)
- Architect Guard -- checks pattern drift against architecture decisions
- All three run in parallel on integrated codebase (main branch, no worktrees)
- Findings consolidated as fix queue; targeted dev fix agents address issues
- Fix loop: re-run affected reviewers after fixes until clean or developer accepts

**Phase 6: Verification (Decision 30)**
- Developer-confirmation checklist derived from Gherkin scenarios (Phase 3 form)
- Future: automated verification via momentum-verify skill
- On full confirmation: transition all stories to `done`

**Phase 7: Sprint Completion**
- `momentum-tools sprint complete` to archive sprint
- Surface summary: stories completed, merge order, AVFL findings, verification results
- Suggest retrospective

### Pre-Flight Checks

Before sprint execution:
1. Active sprint exists and is locked
2. Topological sort validity / cycle detection
3. Dangling reference detection (every `depends_on` must exist in sprint story list)
4. Story file existence for all sprint stories
5. Correct story status (unblocked stories must be `ready-for-dev`)

---

## Part 6: Session-Open Mockups

### Mode 1 -- Active Sprint, Stories In Progress

```
  Active sprint -- Quality Hooks Sprint

    ████████░░░░░░░░  posttooluse-lint-hook        in review
    ████████████████  pretooluse-file-protection   done
    ░░░░░░░░░░░░░░░░  stop-gate-quality-checks     ready

  [1] Continue sprint -- pick up where we left off
  [2] Sprint status -- full story breakdown
  [3] Triage a new story
```

### Mode 2 -- Active Sprint Complete

```
  Quality Hooks Sprint -- all stories done

  Planning sprint ready: "Impetus UX Sprint" -- 3 stories.

  [1] Start sprint -- activate and begin development
  [2] Adjust plan -- modify story selection
  [3] Run retro first -- review completed sprint
```

### Mode 3 -- No Active Sprint

```
  No active sprint -- 18 stories across 4 epics.

  [1] Plan a sprint
  [2] Refine backlog
  [3] Triage a new story
```

### Epic Overview (shown on request or after sprint completion)

Each epic displayed with story count by status and fill bar summary. Example:

```
  Epics

    Quality Enforcement         3 done  2 backlog
    Impetus UX & Orchestration  1 done  4 backlog
    Sprint Orchestration        2 review  2 in-progress
    Quality Hooks               0 done  5 backlog
```

---

## Part 7: File Structure Reference

### Runtime File Locations

```
_bmad-output/implementation-artifacts/
  stories/
    index.json                              <- Story registry
    {slug}.md                               <- Story files (plain English ACs)
  sprints/
    index.json                              <- Sprint tracking
    {sprint-slug}/
      specs/
        {story-slug}.feature                <- Gherkin specs (verifier-only)

.claude/momentum/
  journal.jsonl                             <- Session journal
  journal-view.md                           <- Auto-generated readable view
  installed.json                            <- Project install state
  sprint-logs/
    {sprint-slug}/
      impetus.jsonl                         <- Impetus log (no --story flag)
      {agent-role}-{story-slug}.jsonl       <- Per-agent per-story logs

~/.claude/momentum/
  global-installed.json                     <- Machine install state
  findings-ledger.jsonl                     <- Cross-project findings
```

### Agent Log Event Types

| Type | When |
|------|------|
| `decision` | Significant choice made during execution |
| `error` | Something went wrong |
| `retry` | Retrying a failed operation |
| `assumption` | Making an assumption about ambiguous input |
| `finding` | Quality or consistency finding |
| `ambiguity` | Unresolvable ambiguity surfaced for human review |

---

## Superseded Concepts

| Old Concept | Replaced By | When |
|-------------|-------------|------|
| Wave-sequential execution | Dependency-driven concurrency (Decision 25) | Phase 3 |
| Worktrees per story | Commit-as-sync-point within Agent Teams (Decision 33) | 2026-04-03 |
| Workflow modules (instruction docs Impetus reads inline) | Proper skills with SKILL.md | 2026-04-03 |
| `momentum-sprint-manager` agent | `momentum-tools.py sprint` CLI | Phase 2 |
| `sprint-status.yaml` monolith | `stories/index.json` + `sprints/index.json` | Phase 1 |
| `N-N-slug` story IDs | Kebab-case slugs (no epic encoding) | Phase 1 |
| `npx skills add` installation | `claude plugin add momentum` | 2026-04-03 |
| Per-story AVFL | Sprint-level AVFL (Decision 31) | Phase 3 |
| 6-phase sprint-dev | 7-phase sprint-dev with Team Review | 2026-04-04 |
