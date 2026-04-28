# Benchmark Capture — Session 621fb06b (Impetus → Refine → Epic-Grooming)

> **Important framing note.** The benchmark target named this run as a "sprint-planning session," but the transcript shows that `/momentum:sprint-planning` was **never actually invoked**. The session ran `/momentum:impetus`, the assistant proposed and the developer approved a `/momentum:refine` pass first, refine delegated mid-flow into `/momentum:epic-grooming`, then refine completed and the assistant returned to Impetus orientation offering to dispatch sprint-planning. The developer did not respond before the session closed. This document captures what actually ran. A faithful replay must reproduce that sequence — including the conversational decision to refine before sprint-planning — not synthesize a sprint-planning invocation.

---

## 1. Session Metadata

| Field | Value |
|---|---|
| `session_id` | `621fb06b-aa6b-445f-854e-56733b5d6cf7` |
| `parent_session_id` | none (root session — no cross-session parent: the first user message's `parentUuid` resolves to an in-session attachment record, and only one `sessionId` appears in the entire transcript) |
| `start_ts` | `2026-04-27T02:45:06.643Z` |
| `end_ts (last user/assistant message)` | `2026-04-27T04:09:25.819Z` |
| `end_ts (last system record)` | `2026-04-27T04:34:34.071Z` |
| `active conversation duration` | ~1h 24m (02:45 → 04:09) |
| `wall-clock session duration` | ~1h 49m (02:45 → 04:34) |
| Claude Code version | `2.1.119` |
| Models used | `claude-opus-4-7` (176 assistant turns), `claude-sonnet-4-6` (32 assistant turns) |
| `cwd` | `/Users/steve/projects/momentum` |
| `gitBranch` | `main` |
| Total transcript rows | 559 (208 assistant, 153 user, 104 attachment, 28 system, 28 permission-mode, 22 last-prompt, 14 file-history-snapshot, 2 queue-operation) — verified via DuckDB¹ |
| Total tool calls | 135 |
| Distinct tools | 8: `Bash` (67), `TaskUpdate` (30), `TaskCreate` (15), `Read` (14), `Agent` (4), `Skill` (3), `Edit` (1), `ToolSearch` (1) |

---

## 2. Original Repo State (for reproduction)

### Pre-session commit (closest commit before `start_ts`)

```
4d25642d4717eb1a3b890a211ca7cfb23120fd1d 2026-04-26 13:46:38 -0700 feat(skills): distill — remove military language from Impetus
```

This is the HEAD checkpoint a replay should `git checkout` before starting. Note: commit `4d25642d` is also the commit where `plugin.json` was bumped from `0.17.0` to `0.17.1` (no separate "bump version to 0.17.1" commit exists; the bump was included in this distill commit). There is no git tag for `v0.17.1`; only `v0.17.0` is tagged.

### Git branch at session start

`main`

### `git status` captured during session (at `2026-04-27T02:48:35Z`)

```
 M .claude/momentum/feature-status.html
 M .claude/momentum/feature-status.md
 M .claude/momentum/installed.json
 M _bmad-output/implementation-artifacts/intake-queue.jsonl
 M _bmad-output/implementation-artifacts/stories/index.json
 M _bmad-output/skills/impetus/SKILL.md
 M _bmad-output/skills/impetus/references/first-breath.md
 M skills/momentum/.claude-plugin/plugin.json
 M skills/momentum/skills/quick-fix/workflow.md
?? .claude/scheduled_tasks.lock
?? _bmad-output/implementation-artifacts/stories/canvas-features-lens.md
?? _bmad-output/implementation-artifacts/stories/canvas-flywheel-lens.md
?? _bmad-output/implementation-artifacts/stories/canvas-level-2-feature-detail.md
?? _bmad-output/implementation-artifacts/stories/canvas-level-3-story-detail.md
?? _bmad-output/implementation-artifacts/stories/canvas-reading-mode-polish.md
?? _bmad-output/implementation-artifacts/stories/canvas-sprints-lens.md
?? _bmad-output/implementation-artifacts/stories/canvas-vite-scaffold.md
?? _bmad-output/implementation-artifacts/stories/retire-feature-status-html-directory-dashboard.md
```

A faithful replay must restore both this set of working-tree edits and the eight untracked story stubs. Seven are canvas-feature stubs (`canvas-features-lens.md`, `canvas-flywheel-lens.md`, `canvas-level-2-feature-detail.md`, `canvas-level-3-story-detail.md`, `canvas-reading-mode-polish.md`, `canvas-sprints-lens.md`, `canvas-vite-scaffold.md`); the eighth is `retire-feature-status-html-directory-dashboard.md`. Without the canvas stubs, Impetus orientation will not produce the same "next sprint waiting to be born" reading. The retire stub is not directly load-bearing for the orientation signal but is part of the working-tree state and must be restored for a faithful replay.

### Plugin / skill versions active

- Momentum plugin: `momentum/momentum/0.17.1` (path observed: `/Users/steve/.claude/plugins/cache/momentum/momentum/0.17.1/skills/...`)
- Skills resolved from the cache at this version: `momentum:impetus`, `momentum:refine`, `momentum:epic-grooming`
- The transcript contains a reference to `0.17.0` in `git log` output (record 68, a Bash tool result showing `chore(plugin): bump version to 0.17.0 — Impetus memory agent rebuild`). No read of `installed.json` occurred in this session; the `0.17.0` string is in commit-history context only.
- The transcript also references `momentum/0.14.0` (record 404, a user record containing an assessment document excerpt about a prior retro using a stale 0.14.0 plugin cache). The live invocations all used `0.17.1`.

### Pre-existing artifacts at session start

The following artifacts existed at session start and a faithful replay must restore them before running:

| Artifact | Notes |
|---|---|
| All 9 modified files listed in the `git status` block above | Modified vs HEAD but not committed — required for accurate orientation signals |
| `_bmad-output/implementation-artifacts/stories/canvas-features-lens.md` | Canvas stub — orientation-critical; Impetus reads untracked stories |
| `_bmad-output/implementation-artifacts/stories/canvas-flywheel-lens.md` | Canvas stub — orientation-critical |
| `_bmad-output/implementation-artifacts/stories/canvas-level-2-feature-detail.md` | Canvas stub — orientation-critical |
| `_bmad-output/implementation-artifacts/stories/canvas-level-3-story-detail.md` | Canvas stub — orientation-critical |
| `_bmad-output/implementation-artifacts/stories/canvas-reading-mode-polish.md` | Canvas stub — orientation-critical |
| `_bmad-output/implementation-artifacts/stories/canvas-sprints-lens.md` | Canvas stub — orientation-critical |
| `_bmad-output/implementation-artifacts/stories/canvas-vite-scaffold.md` | Canvas stub — orientation-critical |
| `_bmad-output/implementation-artifacts/stories/retire-feature-status-html-directory-dashboard.md` | Present at session start; not orientation-critical but part of accurate working-tree state |

The canvas stubs are load-bearing for the Impetus orientation — they inform the "next sprint waiting to be born" reading. Without them, the orientation will produce a different signal and the session's conversational sequence (6 shape items, piling discussion) will not reproduce faithfully.

---

## 3. Inputs

### Slash command invocation (verbatim, in transcript order)

| Timestamp | Channel | Verbatim content |
|---|---|---|
| `2026-04-27T02:45:11.297Z` | command-message | `<command-message>momentum:impetus</command-message>` |
| `2026-04-27T02:45:11.297Z` | command-name | `<command-name>/momentum:impetus</command-name>` |
| `2026-04-27T02:45:11.297Z` | user text | `Invoke the momentum:impetus skill and follow it exactly.` |

This was the only user-typed slash command. **No `/momentum:sprint-planning` was invoked as a slash command** — no `<command-name>/momentum:sprint-planning</command-name>` envelope exists anywhere in the transcript. The string `sprint-planning` appears in 16 transcript records (tool result data, file reads, assistant prose proposing dispatch), but none of those constitute a slash-command invocation. The string `/momentum:sprint-planning` appears in 3 records, all in assistant prose offering to dispatch it, not as a received command.

### Skill-loader auto-injected user messages (auto-emitted when a Skill tool fires)

| Timestamp | Skill |
|---|---|
| `2026-04-27T03:04:42.474Z` | `Base directory for this skill: /Users/steve/.claude/plugins/cache/momentum/momentum/0.17.1/skills/refine\nLoad and follow ./workflow.md from Step 0.` |
| `2026-04-27T03:22:12.634Z` | `Base directory for this skill: /Users/steve/.claude/plugins/cache/momentum/momentum/0.17.1/skills/epic-grooming\nFollow the instructions in ./workflow.md` |

### All subsequent human-typed messages (verbatim, ordered)

| # | Timestamp | Verbatim |
|---|---|---|
| 1 | `2026-04-27T02:50:41.763Z` | `Tell me about the six shape items?` |
| 2 | `2026-04-27T02:53:35.412Z` | `Drop 1 and 2, and for 3 - 6 I agree with your suggestions` |
| 3 | `2026-04-27T02:58:45.809Z` | `How do we let them pile?  Do we create an analysis that suggests these?` |
| 4 | `2026-04-27T03:03:27.754Z` | `Let them pile then.  I wonder if we should do refinement before we do sprint planning?` |
| 5 | `2026-04-27T03:04:36.022Z` | `Yes please` |
| 6 | `2026-04-27T03:12:08.524Z` | `A and A` |
| 7 | `2026-04-27T03:40:36.688Z` | `Nope just use your own recommendatioins` |
| 8 | `2026-04-27T03:58:14.628Z` | `1 approved, 2 Not yet I suppose.  Canvas is pretty high priority to me but what else might you consider to be higher?` |
| 9 | `2026-04-27T04:02:06.820Z` | `Probably Reliability first.  I'd also like to do the momentum state migration.  Is that a critical?` |
| 10 | `2026-04-27T04:03:58.734Z` | `My thinking was that it may be high but it's necessary before we can do canvas because canvas reads from it.  It also holds up impetus updates.` |
| 11 | `2026-04-27T04:04:31.941Z` | `Nope that's good` |
| 12 | `2026-04-27T04:08:25.857Z` | `A` |

---

## 4. Workflow Trace

### Skill invocations (ordered)

| # | Timestamp | Skill | Args |
|---|---|---|---|
| 1 | `2026-04-27T02:45:16.802Z` | `momentum:impetus` | `{}` |
| 2 | `2026-04-27T03:04:42.468Z` | `momentum:refine` | `{}` |
| 3 | `2026-04-27T03:22:12.621Z` | `momentum:epic-grooming` | `{}` (called from inside refine Step 5) |

### Subagent spawns (ordered)

All spawned via the `Agent` tool. Two read-only `Explore` agents (drift discovery), two `general-purpose` agents (drift application).

| # | Timestamp | `subagent_type` | `description` | Prompt summary |
|---|---|---|---|---|
| 1 | `2026-04-27T03:06:31.719Z` | `Explore` | "PRD coverage discovery agent" | Read `_bmad-output/planning-artifacts/prd.md` and `stories/index.json`; compare; return JSON list of FRs that are missing/outdated/no-longer-accurate. Return `[]` if no drift. One sentence per finding. |
| 2 | `2026-04-27T03:07:56.033Z` | `Explore` | "Architecture coverage discovery agent" | Same protocol against `architecture.md` vs `stories/index.json`; return JSON list of architectural decisions/components that are missing/outdated/no-longer-accurate. |
| 3 | `2026-04-27T03:12:28.048Z` | `general-purpose` | "PRD update agent" | Sole writer of `prd.md`. Apply 8 approved drift findings (`prd-drift-1` through `prd-drift-8`) preserving existing format. Return a 3-line diff summary. |
| 4 | `2026-04-27T03:16:37.974Z` | `general-purpose` | "Architecture update agent" | Sole writer of `architecture.md`. Apply 5 approved drift findings (`arch-1` through `arch-5`) at next available decision numbers. Return a 3-line diff summary. |

**Note — sequential execution in baseline:** The two discovery agents were spawned in separate messages ~85s apart (PRD at `03:06:31Z`, Architecture at `03:07:56Z`). The TaskCreate description says "in parallel" but actual execution was sequential. A replay that spawns both in a single message is a quality improvement, not a divergence.

For replay, the prompts must be reconstructed by the orchestrator from the refine workflow — they are deterministic outputs of the workflow given the discovered drift findings.

### TaskCreate/TaskUpdate activity

15 `TaskCreate` calls, 30 `TaskUpdate` calls. The orchestrator created an explicit task plan covering refine Steps 1–11 plus the four parallel epic-grooming sub-steps:

**Refine task plan (created `2026-04-27T03:04:54Z` – `2026-04-27T03:05:35Z`):**
1. Read stories/index.json, filter active stories, group by epic, display with priority badges and status.
2. Spawn PRD and architecture coverage agents in parallel to detect drift.
3. Present drift findings, get approval, spawn update agents for approved documents.
4. Scan active stories with story files for completed DoD checklists that haven't been transitioned to done.
5. Invoke momentum:epic-grooming for epic-level structural analysis.
6. Identify low-priority backlog stories with no story file and evaluate each for keep/drop.
7. Run four heuristics (recurrence, workaround burden, forgetting risk, dependency promotion) and discuss priority changes.
8. Review assessment documents and decision documents for staleness, coverage gaps, and ready decision gates.
9. Present all findings grouped by category with batch approval UX.
10. Apply status transitions, drops, epic reassignments, priority changes, and new stories via momentum-tools CLI.
11. Compute post-refine priority distribution and present changes applied summary.

**Epic-grooming sub-tasks (created `2026-04-27T03:22:18Z` – `2026-04-27T03:22:27Z`):**
- Read all sources, enumerate slugs.
- Identify overlaps, draft proposals.
- Present proposals, collect approval per change.
- Update epics.md, reassign stories, log decisions.

### Subagent model parameters

None of the 4 `Agent` tool calls carried an explicit `model:` parameter — all 4 spawns used harness defaults and auto-routing. At the time of this session, the default model was `claude-opus-4-7`; Sonnet 4.6 turns in the session came from the harness's auto-routing, not from explicit per-spawn model parameters.

**Replay caveat:** A bare alias resolves to whatever the harness considers current at replay time. If the default model changes between capture and replay, agent routing may differ. All 4 spawns are model-unspecified — a replay that introduces explicit model params is adding new constraints that were not present in the captured run.

### Notable file reads (in order, deduped)

| Path | Purpose |
|---|---|
| `/Users/steve/projects/momentum/skills/momentum/skills/impetus/SKILL.md` | Locate Impetus skill (devved version, not plugin cache) |
| `/Users/steve/projects/momentum/_bmad/memory/impetus/INDEX.md` | Sanctum entry |
| `/Users/steve/projects/momentum/_bmad/memory/impetus/PERSONA.md` | Sanctum |
| `/Users/steve/projects/momentum/_bmad/memory/impetus/CREED.md` | Sanctum |
| `/Users/steve/projects/momentum/_bmad/memory/impetus/BOND.md` | Sanctum |
| `/Users/steve/projects/momentum/_bmad/memory/impetus/MEMORY.md` | Sanctum |
| `/Users/steve/projects/momentum/_bmad/memory/impetus/CAPABILITIES.md` | Sanctum |
| `/Users/steve/projects/momentum/_bmad/memory/impetus/references/orient.md` | Impetus orientation playbook |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/sprints/index.json` | Sprint state |
| `/Users/steve/projects/momentum/_bmad/memory/impetus/references/dispatch.md` | Dispatch playbook |
| `/Users/steve/.claude/plugins/cache/momentum/momentum/0.17.1/skills/refine/workflow.md` | Refine workflow |
| `/Users/steve/.claude/plugins/cache/momentum/momentum/0.17.1/skills/epic-grooming/workflow.md` | Epic-grooming workflow |
| `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` (twice — different offsets) | Discover insertion site for ad-hoc epic |

### Edits performed by the orchestrator (1 direct Edit)

| Timestamp | File | Change |
|---|---|---|
| `2026-04-27T03:41:37.133Z` | `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` | Inserted a new `### Epic Ad-Hoc: Ad-Hoc Work` section (catch-all bucket for quickfix and one-off stories) immediately after Epic 13 and before "## Epic 1: Foundation & Bootstrap" |

Edits performed by spawned subagents (PRD agent, Architecture agent) are not visible as orchestrator-level Edit calls; they happened inside the agent contexts. The assistant summary at `2026-04-27T03:20:47Z` describes the cumulative result:

> "PRD: 5 section-level backlog notes + FR22/FR43/FR91 specifics. Architecture: 2 new decisions (51/52), `momentum_version` schema additions, structure-tree updates for `agent-guidelines` and `intake-queue.jsonl`, sprint folder tree."

### Mutating CLI calls (`momentum-tools.py`)

| Timestamp | Action |
|---|---|
| `2026-04-27T02:54:24.257Z` | `intake-queue consume --id iq-20260416054847-c13fce79 --outcome-ref "dropped: test smoke item"` and `--id iq-20260416055621-bf7d037f --outcome-ref "dropped: vague seed, no further context"` |
| `2026-04-27T03:41:09.011Z` | Bash loop: `sprint epic-membership --story <slug> --epic performance-validation` for 16 stories → `performance-validation` epic |
| `2026-04-27T03:41:21.192Z` | Bash loop: `sprint epic-membership --story <slug> --epic <canonical>` for 15 stories across 7 remaining merge targets (`sprint-dev-workflow`, `quality-enforcement`, `practice-compounds`, `story-cycles`, `artifact-provenance`, `agent-team-model`, `stay-oriented-impetus`) |
| `2026-04-27T04:08:50.860Z` | `sprint status-transition --story <slug> --target dropped` for `develop-epic-command`, `guidelines-research-recency-gate`, `verify-skill`, `backlog-add-command`, `dashboard-ux-wireframes`, `feature-dependency-graph-ux-wireframes` |
| `2026-04-27T04:08:55.657Z` | `sprint set-priority --story plugin-cache-staleness-detection --priority critical`; `sprint set-priority --story impetus-momentum-state-migration --priority high` |

---

## 5. Outputs

### Files created / modified during the session

| Path | Action | Purpose |
|---|---|---|
| `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` | modified (1 direct Edit by orchestrator) | Add Epic Ad-Hoc section |
| `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/prd.md` | modified (via PRD update subagent) | Apply 8 drift findings — backlog status notes for FR12–17, FR28–33, FR34–38, FR39–41, FR102–109; specifics for FR22/FR43/FR91 |
| `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/architecture.md` | modified (via Architecture update subagent) | Add Decisions 51 and 52 (formalizing DEC-005/DEC-007); add `momentum_version` to ledger schema; add `agent-guidelines`, `intake-queue.jsonl`, and `sprint-summary.md` to structure trees |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/stories/index.json` | modified (via momentum-tools.py CLI) | 31 epic reassignments, 6 status transitions to `dropped`, 2 priority changes |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/intake-queue.jsonl` | modified (via momentum-tools.py CLI) | 2 shape items consumed (`iq-20260416054847-c13fce79`, `iq-20260416055621-bf7d037f`) |

### Sprint planning artifacts produced

**None.** No file was written under `_bmad-output/implementation-artifacts/sprints/`. No new sprint folder was created. No `sprint-plan.md` or `sprint-summary.md` was emitted. The session ended with a *proposal* of an 8-story reliability sprint composition; no sprint was activated.

### Commits made during the session

Transcript scan: 0 `git commit` invocations in 67 Bash tool calls — verified via DuckDB query against the JSONL (`SELECT count(*) WHERE type='assistant' AND tool_name='Bash' AND command LIKE '%git commit%'` → 0).

**No commits were made during the session.** All file changes remained uncommitted in the working tree.

Note: The window `--since='2026-04-27T02:45:00Z' --until='2026-04-27T05:00:00Z'` does return commits (3 commits from a concurrent session running in parallel), but those commits originated from other sessions, not this one. The transcript evidence — zero `git commit` Bash calls — is the correct proof.

### Final assistant turn (verbatim, `2026-04-27T04:09:25.819Z`)

```
✓ **Refinement complete.**

**Changes applied:**
- · Status transitions: 0 (none needed)
- · Stories dropped: 6
- · Epic reassignments: 31 (across 8 merges + 1 create from epic-grooming)
- · Priority changes: 2
- · New stories created: 0
- · Findings rejected: 0
- · Planning artifacts updated: PRD ✓, Architecture ✓

**Priority distribution (before → after):**
| | before | after | Δ |
|---|---|---|---|
| [C] critical | 14 | **15** | +1 |
| [H] high | 55 | **53** | -2 |
| [M] medium | 70 | **69** | -1 |
| [L] low | 55 | **51** | -4 |

Net: 6 stories left active backlog (drops); 1 promoted into critical, 1 demoted from H to (already-counted) C, 1 promoted M→H. Active backlog: 188 (was 194).

**Epic taxonomy now clean:** 18 registered, 0 orphans.

The backlog is ready for sprint planning.

---

**Returning to Impetus orientation.** Given everything we just learned: my reliability-first recommendation is now sharper. The next sprint shape:

**Reliability sprint (suggested ~6-8 stories):**
- `plugin-cache-staleness-detection` [C] — newly elevated
- `retro-extract-preflight-validation` [C]
- `retro-transcript-extraction-hardening` [C]
- `retro-team-singleton-guard` [C]
- `fix-retro-documenter-replication-defect` [C]
- `sprint-log-directory-enforcement` [C]
- `harden-sprint-dev-phase5-spawn-prompts` [C]
- `sprint-planning-adds-per-story-approval-gate` [C]

Could optionally include `impetus-momentum-state-migration` [H] to clear the canvas runway in one shot.

Want me to dispatch `/momentum:sprint-planning` with this composition?
```

The developer did not respond. The session closed ~25 minutes later with a system-only event.

---

## 6. Reproduction Recipe

1. **Restore working tree to pre-session state.**
   - `git -C /Users/steve/projects/momentum checkout 4d25642d4717eb1a3b890a211ca7cfb23120fd1d`
   - Restore the 9 modified files and 8 untracked story stubs listed in §2's `git status` block. Without the canvas stubs (7 canvas-feature stubs) and modified `intake-queue.jsonl`/`stories/index.json`, the Impetus orientation will produce different signals. The eighth stub (`retire-feature-status-html-directory-dashboard.md`) is not orientation-critical but must be present for a faithful working-tree reproduction.
2. **Install Momentum plugin v0.17.1.** There is no git tag for `v0.17.1`; pin to commit `4d25642d4717eb1a3b890a211ca7cfb23120fd1d` and rebuild the plugin cache from that tree, or pin `~/.claude/plugins/cache/momentum/momentum/0.17.1/` from a clean install against that commit. **Do NOT use `0.17.2` as a replay base** — the current `plugin.json` is `0.17.2` (bumped in commit `ec6c44b`), which adds the quick-fix Phase 5 mandatory guard and is not a valid replica of the session state.
3. **Start a fresh Claude Code session** (v2.1.119) in `/Users/steve/projects/momentum` on `main`. Default model: `claude-opus-4-7` (the session predominantly used Opus 4.7 with occasional Sonnet 4.6 routing for sub-steps). None of the 4 `Agent` spawns carried explicit `model:` parameters — all routing was harness-default plus auto-routing. **Replay caveat:** If the harness's default model or alias resolution changes, agent routing will differ. The bare aliases in this session resolve to whatever the harness considers current at replay time — there is no pinning mechanism for the subagent models used here.
4. **Send the opening prompt verbatim:** `/momentum:impetus`. (The harness will expand this into the system text recorded in §3.)
5. **Reply to Impetus turns in order, verbatim**, using messages 1–12 from §3 at the conversational beats indicated. Critical decision points to preserve:
   - After the 6-shape-item walkthrough: drop #1 and #2, agree with suggestions for #3–#6.
   - When asked about piling: confirm "Let them pile then" and pivot to refinement before sprint planning.
   - In refine: approve PRD + Architecture drift via `A and A`.
   - In epic-grooming developer-review: `Nope just use your own recommendatioins` (skip the agent-team-model split, accept all 8 merges + 1 create).
   - In the priority-change conversation: approve `plugin-cache-staleness-detection` H→C; argue `impetus-momentum-state-migration` should be H (not C); confirm "Nope that's good".
   - In the consolidated approval gate: `A` (approve all 8 findings).
6. **Stop when the assistant offers `/momentum:sprint-planning` dispatch.** This run did not proceed past that offer.

### Decision-point coupling

The following user messages are conditional on specific orchestrator-output shapes. A replay producing a different shape at that turn will receive a non-sequitur user message:

| Msg # | Message | Trigger condition | Replay guidance |
|---|---|---|---|
| 2 | `Drop 1 and 2, and for 3 - 6 I agree with your suggestions` | Orchestrator presented exactly 6 shape items | Feed only if the replay produces a 6-item shape presentation. If the replay produces fewer or more items, the numbering will not match. |
| 6 | `A and A` | Orchestrator presented a 2-document batch approval format (PRD + Architecture as separate approval targets in a single message) | Feed only if the replay's drift-approval UX presents exactly 2 documents for approval. |
| 7 | `Nope just use your own recommendatioins` | Orchestrator presented epic-grooming proposals and asked whether to apply the agent-team-model split | Feed only if the replay's epic-grooming Step 3 includes an agent-team-model split proposal. |
| 9 | `Probably Reliability first. I'd also like to do the momentum state migration.` | Orchestrator proposed a sprint composition that included Reliability as one of the named options | Feed only if the replay's sprint composition proposal includes Reliability as a named candidate. |

---

## 7. Benchmark Comparison Hooks

Compare a replay run against this baseline on:

- **Skill invocation set and order.** Did the replay invoke `momentum:impetus` → `momentum:refine` → `momentum:epic-grooming`, in that order? Did it (incorrectly) jump straight to `momentum:sprint-planning` without the developer-prompted refine detour?
- **Subagent spawns.** Did refine spawn exactly 4 subagents (2 Explore for discovery, 2 general-purpose for application)? Were the discovery agents launched in parallel? (In the baseline they were NOT launched in parallel — each was spawned in a separate message ~85s apart. A replay that spawns both in a single message is a quality improvement, not a divergence.)
- **Drift findings produced.** Did PRD discovery surface exactly 8 findings (FR43, FR39–41, FR12–17, FR22, FR28–33, FR34–38, FR102–109, FR91)? Did Architecture discovery surface exactly 5 (DEC-005/DEC-007 missing, agent-guidelines missing from tree, momentum_version field gap, intake-queue.jsonl path gap, sprint-summary.md path gap)?
- **Epic taxonomy outcome.** Did epic-grooming detect 8 orphan legacy-duplicate slugs and propose 8 merges + 1 CREATE for the intentional `ad-hoc` bucket (9 proposals total)? Did it land at 18 registered epics with 0 orphans?
- **Stale-story drops.** Did Step 6 surface the same 4 candidates (`develop-epic-command`, `guidelines-research-recency-gate`, `verify-skill`, `backlog-add-command`) and the assessment review surface the same 2 (`dashboard-ux-wireframes`, `feature-dependency-graph-ux-wireframes`)?
- **Priority-change recommendations.** Did Step 7 surface `plugin-cache-staleness-detection` H→C as a top promotion? Did the assistant correctly negotiate `impetus-momentum-state-migration` to H (not C)?
- **Files written.** Were the same 5 files modified (`epics.md`, `prd.md`, `architecture.md`, `stories/index.json`, `intake-queue.jsonl`)? Was the Epic Ad-Hoc insertion placed at the same location?
- **Final priority distribution.** Did the post-refine numbers match (C:15, H:53, M:69, L:51; total active 188, down from 194)?
- **Sprint composition proposal.** Did the closing summary recommend the same 8-story reliability sprint with the optional state-migration add-on?
- **Wall-clock duration.** Active conversation was ~1h 24m; full wall-clock ~1h 49m. Compare a replay against both numbers.
- **Tool-call shape.** 135 tool calls total; ratio Bash:TaskUpdate:TaskCreate:Read = 67:30:15:14. A replay producing dramatically different counts (e.g. 2x more Bash) suggests verification overhead or a different navigation strategy.
- **Model routing mix.** 176 Opus 4.7 turns vs 32 Sonnet 4.6 turns (~85/15 split). Compare routing distribution.

### Replay variability — non-deterministic outcomes

The following comparison hooks may produce legitimate divergence between replays and should be calibrated accordingly — divergence here does NOT indicate a quality regression:

1. **Exact drift finding count (emergent).** The precise set of 8 PRD drift findings and 5 architecture drift findings depends on the discovery agents' reading of the artifacts at replay time. If upstream planning documents have changed since the benchmark run, different findings will surface. Compare the categories (FR ranges, decision gaps) rather than exact finding text.

2. **Specific story drops (emergent).** The 4 stale-story candidates from Step 6 and 2 from the assessment review depend on the story file and priority data at replay time. If stories have been added, dropped, or modified since the benchmark run, different candidates may surface. The categories (no-story-file, low-priority, no-forward-action) should match even if specific slugs differ.

3. **Sprint composition recommendation (emergent).** The 8-story reliability sprint recommendation is based on the backlog state at session time. The specific slugs and counts will differ if the backlog has changed. The decision class (reliability-first, clear retro blockers) should be consistent across replays even if the exact story list changes.

**Deterministic hooks** (should match closely): skill invocation set and order, subagent spawn count and types, files written and their locations, final priority distribution (if backlog is restored to pre-session state), and the Epic Ad-Hoc insertion location.

---

> ¹ **Transcript source:** `/Users/steve/.claude/projects/-Users-steve-projects-momentum/621fb06b-aa6b-445f-854e-56733b5d6cf7.jsonl`
>
> DuckDB query used to derive per-type row counts: `SELECT type, COUNT(*) AS cnt FROM read_json('<path>', format='newline_delimited', ignore_errors=true) GROUP BY type ORDER BY cnt DESC` — verified total 559 rows (208 assistant, 153 user, 104 attachment, 28 system, 28 permission-mode, 22 last-prompt, 14 file-history-snapshot, 2 queue-operation).
>
> DuckDB query used to verify zero `git commit` Bash calls: tool name and command content extracted from the `message` field of `type=assistant` records; no `git commit` string found in any Bash tool input.
