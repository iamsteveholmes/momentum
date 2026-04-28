# Benchmark Capture — Session cdb7de2f (Sprint-Planning → Mid-Flight Research → Sprint Activation)

> **Important framing note.** This run started as a single-shot `/momentum:sprint-planning` invocation but mid-flow the developer interrupted to relaunch a `momentum:research` spike (light profile) when the sprint plan turned out to depend on undecided artifact-design questions. Research → DEC-003 → story rewrite → return to sprint-planning Phase 5 → AVFL → activation. The session crossed three auto-compaction boundaries (~00:32, ~04:32, ~05:10 UTC). A faithful replay must reproduce the developer's mid-flow pivot, not jump straight from sprint-planning Phase 4 to Phase 5.

---

## 1. Session Metadata

| Field | Value |
|---|---|
| `session_id` | `cdb7de2f-43d8-4a87-95a3-af5f72a3ff24` |
| `parent_session_id` | none (root session — `parentUuid` is null on the first record) |
| `start_ts` | `2026-04-11T23:57:14.193Z` |
| `end_ts` (last user/assistant message) | `2026-04-12T05:53:22.990Z` |
| `end_ts` (last system record) | `2026-04-12T05:53:23.118Z` |
| Wall-clock duration | ~5h 56m |
| Auto-compaction boundaries | 3 (`2026-04-12T00:32:06Z`, `2026-04-12T04:32:07Z`, `2026-04-12T05:10:51Z`) |
| Claude Code version | `2.1.101` |
| Models used | `claude-sonnet-4-6` (555 assistant turns), `claude-opus-4-6` (5 assistant turns) |
| Model split | ~99.1% Sonnet 4.6 / ~0.9% Opus 4.6 |
| `cwd` | `/Users/steve/projects/momentum` |
| `gitBranch` (start) | `main` |
| `gitBranch` (end) | `sprint/sprint-2026-04-11` (branch flipped at ~00:18 UTC with first `sprint plan add` mutation — ~5.5h before sprint activation) |
| Total transcript rows | 1374 (560 assistant, 373 user, 314 attachment, 58 system, 48 file-history-snapshot, 12 queue-operation, 5 permission-mode, 4 last-prompt) |
| Total tool calls | 331 |
| Distinct tool names | 11 |

### Tool call shape

| Tool | Calls |
|---|---:|
| `Bash` | 121 |
| `Read` | 82 |
| `Edit` | 37 |
| `Agent` | 23 |
| `TaskUpdate` | 20 |
| `Write` | 13 |
| `Glob` | 12 |
| `TaskCreate` | 10 |
| `Grep` | 5 |
| `ToolSearch` | 4 |
| `Skill` | 4 |

### Bash sub-shape

| Category | Calls |
|---|---:|
| cmux (browser/pane) | 63 |
| filesystem (cat/ls/find/wc) | 20 |
| git | 16 |
| other | 9 |
| momentum-tools.py | 9 |
| python (other) | 4 |

The cmux load is unusual for a sprint-planning run. Counting unit: Bash invocations (some Bash calls chain `&&`/`;` multiple cmux invocations — the table counts Bash calls, not chained invocations). Verified breakdown by DuckDB query against transcript JSONL (see footnote¹):

| cmux subcommand | Bash calls |
|---|---:|
| `browser --surface <N> <op>` (chained click/eval/wait/goto/snapshot on existing surface) | 10 |
| `browser snapshot` | 8 |
| `browser click` | 7 |
| `browser screenshot` | 4 |
| `markdown open` | 4 |
| `browser open` | 3 |
| `browser press` | 3 |
| `new-split right` | 3 |
| `browser eval` | 3 |
| `send --surface` | 3 |
| `close-surface --surface` | 2 |
| `rename-tab --surface` | 2 |
| `browser wait` | 2 |
| `browser goto` | 2 |
| `respawn-pane --surface` | 1 |
| `identify` | 1 |
| `browser state` | 1 |
| `list-panels` | 1 |
| `browser --help` | 1 |
| `browser fill` | 1 |
| `capture-pane --surface` | 1 |
| **Total** | **63** |

All driven by the developer's "show me the mockup" detour mid-session (msgs 12–26).

> ¹ DuckDB counting query: `SELECT regexp_extract(cmd, 'cmux ([a-z_-]+(?:\s+[a-z_-]+)?)', 1) AS sub, COUNT(*) FROM (... WHERE name='Bash' AND cmd LIKE '%cmux %') WHERE cmd LIKE 'cmux %' GROUP BY 1`. One Bash call (`sleep 2; cmux browser snapshot`) starts with `sleep` and was not matched by the leading `cmux %` filter — counted separately and added to the `browser snapshot` total to reach the correct aggregate of 63.

---

## 2. Original Repo State (for reproduction)

### Pre-session commit (closest commit before `start_ts`)

```
be1ce241231d69636670889b3e3c10cc7c3943cd 2026-04-11 16:50:02 -0700 docs(decisions): add DEC-002 — Feature Visualization and Developer Orientation
```

This is the HEAD a replay should `git checkout` before starting.

### Git branch at session start

`main`. The session also wrote into `sprint/sprint-2026-04-11` once the sprint was activated near the end of the run; a faithful replay should not assume the branch flip — let the activation step create it.

### `git status` captured during session

The earliest `git status` invocation was deferred until `2026-04-12T04:58:04Z` — long after the session had already created files. At that point the working tree showed:

```
On branch sprint/sprint-2026-04-11
Your branch is ahead of 'origin/sprint/sprint-2026-04-11' by 6 commits.

Changes not staged for commit:
	modified:   .claude/momentum/gate-findings.txt
	modified:   .claude/momentum/installed.json
	modified:   .claude/momentum/sprint-logs/_unsorted/hooks-observability.jsonl
	modified:   .claude/momentum/sprint-logs/_unsorted/impetus.jsonl
	modified:   _bmad-output/implementation-artifacts/sprints/index.json
	modified:   _bmad-output/implementation-artifacts/stories/index.json
	modified:   _bmad-output/implementation-artifacts/stories/sprint-boundary-compression.md

Untracked files:
	.claude/momentum/feature-status-mockup.html
	.claude/momentum/journal-view.md
	.claude/momentum/sprint-logs/sprint-2026-04-08/
	_bmad-output/implementation-artifacts/sprints/quickfix-implement-momentum-distill-skill/
	_bmad-output/implementation-artifacts/stories/impetus-feature-status-cache.md
	_bmad-output/research/agent-communication-patterns-2026-04-09/
	_bmad-output/research/ai-dev-workflow-metrics-2026-04-11/
```

This snapshot is **mid-session state**, not pre-session state. No early-session `git status` was captured — a replay cannot use this output to reconstruct the starting working tree. Reproduction guidance: check out the pre-session commit and run from a clean tree; the mid-flow detour artifacts (mockup HTML, quickfix sprint dir, agent-communication research) were already present at session start and need to be staged separately if a high-fidelity replay is needed.

### Pre-existing artifacts at session start

The following artifacts were read by the session but were NOT created by it — they existed at session start and a faithful replay must restore them before running:

| Artifact | Notes |
|---|---|
| `_bmad-output/planning-artifacts/decisions/dec-002-feature-visualization-and-orientation-2026-04-11.md` | Referenced in opening prompt; pre-existing research decision |
| `_bmad-output/research/project-knowledge-visualization-ai-2026-04-11/final/project-knowledge-visualization-ai-final-2026-04-11.md` | Pre-existing research corpus; referenced by DEC-002 and read 6× |
| `_bmad-output/implementation-artifacts/stories/index.json` | Pre-existing; modified during session |
| `_bmad-output/planning-artifacts/epics.md` | Pre-existing; modified during session |
| `_bmad-output/planning-artifacts/prd.md` | Pre-existing; modified during session |
| `_bmad-output/planning-artifacts/architecture.md` | Pre-existing; modified during session |
| `_bmad-output/implementation-artifacts/sprints/index.json` | Pre-existing; modified during session |
| `_bmad-output/research/agent-communication-patterns-2026-04-09/` | Shown as untracked in mid-session git status — pre-existing at session start |
| `_bmad-output/research/ai-dev-workflow-metrics-2026-04-11/` | Shown as untracked in mid-session git status — pre-existing at session start |
| `_bmad-output/implementation-artifacts/sprints/quickfix-implement-momentum-distill-skill/` | Shown as untracked in mid-session git status — pre-existing at session start |

All of the above can be restored by checking out commit `be1ce241` and restoring the untracked directories separately. The mid-flow detour artifacts (`.claude/momentum/feature-status-mockup.html`, etc.) were created during the session and should NOT be pre-seeded.

### Plugin / skill versions active

- Momentum plugin: `momentum/momentum/0.12.0` (path observed: `/Users/steve/.claude/plugins/cache/momentum/momentum/0.12.0/skills/...`)
- **v0.12.0 is no longer in the local plugin cache.** Current cache contains only: `0.16.0`, `0.17.0`, `0.17.1`, `0.17.2`.
- v0.12.0 was released at commit `1f6d0737f64a3446b86b3c150e6dd407a8750a07` (`chore(plugin): bump version to 0.12.0 — add momentum:distill skill`, `2026-04-11 14:47:29 -0700`). There is no git tag for v0.12.0; only `v0.17.0` is tagged.
- **Replay limitation:** A faithful replay requires checking out commit `1f6d073` (or the state just after it) and rebuilding the plugin cache from that tree. Simply using the current cache (`0.17.x`) is NOT a valid replay base — the skill catalog has materially drifted: `sprint-boundary-compression` is now a deployed skill; `momentum:distill`, `momentum:triage`, `momentum:feature-grooming`, and several others have been added or substantially modified since v0.12.0.
- Skills resolved from the cache at v0.12.0: `momentum:sprint-planning`, `momentum:research`, `momentum:decision`, `momentum:avfl`, `momentum:create-story` (referenced via subagents)

---

## 3. Inputs

### Slash command invocation (verbatim, opening prompt)

The user's opening prompt — fenced verbatim:

```
<command-message>momentum:sprint-planning</command-message>
<command-name>/momentum:sprint-planning</command-name>
<command-args>/momentum:sprint-planning

  Context for this sprint: We just completed research and captured DEC-002
  (Feature Visualization and Developer Orientation) at:
  _bmad-output/planning-artifacts/decisions/dec-002-feature-visualization-and-orientation-2026-04-11.md

  The decisions produce 5 story areas — all new work, no existing backlog stories:

  D1 — Feature artifact schema: define features.json schema; populate initial
       instances for Nornspun and Momentum
  D2 — momentum:feature-status skill: reads features.json, cross-references
       stories/index.json, evaluates coverage gaps (not just counts), produces
       per-project-type rendering; SUPERSEDES the prior DRIFT-006 decision that
       momentum:status would be absorbed into Impetus/momentum-tools
  D3 — Impetus greeting cache: hash-based staleness detection for feature status,
       cached summary in greeting with staleness flag; DEPENDS ON D2
  D4 — Sprint-boundary context compression: at retro completion, produce structured
       sprint summary artifact (features advanced, stories done vs. planned, key
       decisions, open issues, narrative); INDEPENDENT of D1/D2/D3
  D5 — Practice project rendering path: skill topology + SDLC coverage map for
       Momentum within feature-status; EXTENDS D2

  Hard dependencies: D1 before D2, D2 before D3, D2 before D5. D4 is parallel.

  Key design constraints from DEC-002:
  - Feature-status must evaluate whether the assigned story set is sufficient to
    deliver the acceptance condition (gap analysis, not just status reporting)
  - Impetus startup must not get slower — feature status is cached, never live-computed
  - Two rendering paths: product projects (Nornspun) vs practice projects (Momentum)
  - Build order beyond hard dependencies is sprint planning's call

  Research corpus if you need it:
  _bmad-output/research/project-knowledge-visualization-ai-2026-04-11/final/project-knowledge-visualization-ai-final-2026-04-11.md</command-args>
```

### All subsequent human-typed messages (verbatim, ordered)

| # | Timestamp | Verbatim |
|---|---|---|
| 1 | `2026-04-12T00:07:03.783Z` | `Why are they named like this?  Have we not converted to the name slugs and epics?  What's happening here?` |
| 2 | `2026-04-12T00:14:03.894Z` | `A` |
| 3 | `2026-04-12T00:17:50.368Z` | `Let's go!` |
| 4 | `2026-04-12T00:32:53.502Z` | `You're supposed to fire them up in a cmux window on the right` |
| 5 | `2026-04-12T00:37:37.462Z` | `feature-status-practice approved, but regarding impetus-feature-status-cache why would the cache just not be the feature status file with hash inputs?` |
| 6 | `2026-04-12T00:40:51.550Z` | `Yes that matches what I have in mind.  Also, If features.json is absent it shouldn't be silent.  It should suggest to the user that they plan features.` |
| 7 | `2026-04-12T00:51:10.780Z` | `Approve that story` |
| 8 | `2026-04-12T00:53:19.512Z` | `Regarding the sprint-boundary-compression story, I thought the retro would run a feature-status and update that.  Am I misunderstanding?` |
| 9 | `2026-04-12T00:59:37.856Z` | `I'm still not understanding what sprint-boundary-compression does.  Can you explain this to me?` |
| 10 | `2026-04-12T01:40:52.218Z` | `Please open it on Android also` |
| 11 | `2026-04-12T01:45:26.676Z` | `The android comment was meant for another session, the compress story is approved.  Regarding features status skill, I think we might want to see some outputs.  Maybe you could create the template for me for each of the projects right now?  So I CAN SEE SORt of a mockup?  Also, how can the output be compact and scannable, really?  These might be very complex features, and I mentioned screenshots and such.  That might end up being pretty big.` |
| 12 | `2026-04-12T01:57:51.737Z` | `Even the practice path I don't see the point of being compact.  If the attempt is to prevent Spec Fatigue I appreciate that.  But a picture is worth a thousand words.  And this tells me very little.  Frankly I'd rather they be larger fonts and easier to scan if anything.  Regarding the product I'm not even sure what it's trying to tell me let alone what it is telling me.  Where are the screenshots?  Or some sort of diagram?  Where does it show me in a picture what my feature needs?  Where even are the features?  I don't get it at all.` |
| 13 | `2026-04-12T02:02:23.713Z` | `"The real question is: what artifact are you imagining when you think about feature-status?" - We did a bunch of research on this question.  Did it produce nothing?  Are we saying that I am the first person to ever want to see a visual diagram of what it was going to take to get something finished?` |
| 14 | `2026-04-12T02:13:59.047Z` | `Okay it seems we need to do a bunch of work here, my intention was NEVER to only have output.  We could show a summary in output, like feature: in-process, feature: finished, etc.  But the purpose of the feature diagram is to help with planning, a serious full blown working sheet to help with planning.  A full map of features and what they need, the status of each story, probably the importance of stories, and gaps.  I don't know what it's going to take to build this.  That was the purpose of the prior research.  I did some discovery, are you telling me that we need to stop this planning?  Or should we interupt it and start a new set of research?  What about a light research?` |
| 15 | `2026-04-12T02:17:03.085Z` | `No I don't want a worthless sprint.  I want something accomplished.  Let's stop now and do that sprint.  Let's get this research done. Should we do light or medium do you think?` |
| 16 | `2026-04-12T02:18:44.136Z` | `How do we render it?  How do we template it?  Do we need tools?  Does this reasearch answer those questions?` |
| 17 | `2026-04-12T02:21:47.198Z` | `Yes` |
| 18 | `2026-04-12T02:30:03.210Z` | `Do it` |
| 19 | `2026-04-12T02:49:45.837Z` | `I thought light research didn't use gemini...` |
| 20 | `2026-04-12T04:13:15.968Z` | `Ssorry can you ask your questions again please?` |
| 21 | `2026-04-12T04:15:44.249Z` | `Q3 is taking forever, are you certain it's not stalled?` |
| 22 | `2026-04-12T04:24:51.411Z` | `yes` |
| 23 | `2026-04-12T04:26:21.047Z` | `Do it` |
| 24 | `2026-04-12T04:38:37.791Z` | `I'd like to see examples and I'm not seeing them` |
| 25 | `2026-04-12T04:41:08.119Z` | `I'm still not seeing any diagrams.  This isn't bad but I'd like to see some picture` |
| 26 | `2026-04-12T04:46:25.022Z` | `That looks great let's go` |
| 27 | `2026-04-12T05:50:11.429Z` | `yes` |
| 28 | `2026-04-12T05:52:52.464Z` | `What is the agent running in the background?` |

Note: Non-user-typed messages in the user channel (not listed in the table above):
- **3 compaction preambles** — auto-injected "This session is being continued from a previous conversation…" summaries that follow each of the 3 `compact_boundary` events (`~00:32`, `~04:32`, `~05:10 UTC`).
- **4 `<task-notification>` envelopes** — background-task completion events (verified by DuckDB count; the original doc stated 2, which was an undercount).
- **1 skill-loader injection** — the opening `<command-message>momentum:sprint-planning</command-message>` envelope injected when the user typed `/momentum:sprint-planning`.
- **1 `[Request interrupted by user]`** — at `2026-04-12T01:40:56.203Z`, 4 seconds after msg 10 ("Please open it on Android also"). The developer cancelled the assistant's response to msg 10 before it completed, then sent msg 11 recanting the Android request.

### Slash commands invoked

Only one user slash command: `/momentum:sprint-planning` (the opening prompt). No further user-issued slash commands. All other skills (`research`, `decision`, `avfl`) were invoked by the orchestrator on the user's behalf in response to plain-English requests.

---

## 4. Workflow Trace

### Skill invocations (ordered)

| # | Timestamp | Skill | Args (head) |
|---|---|---|---|
| 1 | `2026-04-11T23:57:21.169Z` | `momentum:sprint-planning` | `/momentum:sprint-planning` + the verbatim opening prompt arguments (DEC-002 D1–D5 context, 5 story areas, hard dependencies). |
| 2 | `2026-04-12T02:22:18.134Z` | `research` | `Feature planning artifact visualization — light research spike` with Q1/Q2 (artifact layout & design / useful vs overwhelming).² Q3 (CLI-generated rich visual artifacts) was spawned separately as an Agent call at `02:34:50Z`, not as part of this Skill invocation. |
| 3 | `2026-04-12T04:26:48.219Z` | `decision` | `DEC-003 — Feature Status Artifact Design`. Captures the artifact-design conclusions from the research spike — HTML report, layout, signals. |
| 4 | `2026-04-12T05:00:26.504Z` | `momentum:avfl` | Sprint plan validation — `sprint-2026-04-11` (feature-orientation epic), 5 stories, 3 execution waves. |

### Subagent spawns (ordered)

23 spawns via the `Agent` tool. Mix of `momentum:create-story`, `general-purpose`, `Explore`, and `momentum:dev-skills`.

| # | Timestamp | `subagent_type` | `description` | Prompt intent |
|---|---|---|---|---|
| 1 | `2026-04-12T00:18:39.956Z` | `momentum:create-story` | Create story: feature-artifact-schema | Write full story file at `…/stories/feature-artifact-schema.md` from the DEC-002 D1 stub (slug, title, epic, priority, change_type, depends_on, touches). |
| 2 | `2026-04-12T00:18:55.241Z` | `momentum:create-story` | Create story: feature-status-skill | Same protocol for D2 stub. |
| 3 | `2026-04-12T00:19:08.246Z` | `momentum:create-story` | Create story: sprint-boundary-compression | Same protocol for D4 stub (independent of D1/D2/D3/D5). |
| 4 | `2026-04-12T00:19:24.602Z` | `momentum:create-story` | Create story: impetus-feature-status-cache | Same protocol for D3 stub. |
| 5 | `2026-04-12T00:19:38.237Z` | `momentum:create-story` | Create story: feature-status-practice-path | Same protocol for D5 stub. |
| 6–10 | `2026-04-12T00:20:19Z`–`00:20:48Z` | `general-purpose` | Create story: (each of 5 above) | Re-spawn pattern: orchestrator wrapped each create-story call inside a general-purpose agent that invokes the `momentum:create-story` skill. (This duplicate spawn pattern is itself notable — see comparison hooks.) |
| 11 | `2026-04-12T02:34:22.139Z` | `general-purpose` | Research Q1: Feature planning artifact layout and design | Light-profile sub-question: layout/visual structure for a developer-facing feature planning artifact (Linear/Productboard/Aha!/FigJam comparators, prominent signals, "stories needed" representation). |
| 12 | `2026-04-12T02:34:34.642Z` | `general-purpose` | Research Q2: Useful vs. overwhelming — practitioner lessons | Practitioner accounts and case studies on noise vs decision-driving information, cognitive overload patterns. |
| 13 | `2026-04-12T02:34:50.824Z` | `general-purpose` | Research Q3: CLI-generated rich visual artifacts — rendering patterns | Patterns for "generated from code, rendered as rich visual" (Istanbul/nyc, Codecov, pytest-html, dependency graph renderers, webpack-bundle-analyzer); templating for a static-HTML artifact opened in browser. |
| 14 | `2026-04-12T04:18:33.525Z` | `general-purpose` | Research Q3 relaunch | Q3 was relaunched after the developer flagged it as stalled (~1h44m elapsed since initial spawn at `02:34:50Z`). Re-prompted with "research as you go and write incrementally." |
| 15 | `2026-04-12T04:20:30.626Z` | `general-purpose` | Synthesis: feature status visualization research | Read the 3 raw research files and produce final synthesis at `…/research/feature-status-visualization-2026-04-11/final/…`. **Explicit `model: "opus"` parameter.** |
| 16 | `2026-04-12T04:49:50.081Z` | `Explore` | Architecture impact discovery | Read architecture.md + 5 story files; return list of new/modified architectural decisions for the feature-orientation epic. |
| 17 | `2026-04-12T04:49:53.501Z` | `Explore` | PRD impact discovery | Read prd.md + 5 story files; return list of new/modified FRs. |
| 18 | `2026-04-12T04:51:13.930Z` | `general-purpose` | Architecture.md update | Sole writer of architecture.md. Apply Decisions 44–48 from impact analysis (feature artifact layer, HTML rendering, practice-path detection, cache schema). |
| 19 | `2026-04-12T04:51:32.154Z` | `general-purpose` | PRD.md update | Sole writer of prd.md. Add new feature-orientation FRs from impact analysis. |
| 20 | `2026-04-12T05:03:23.117Z` | `general-purpose` | AVFL structural validator | Lens: structural integrity — mechanical verification, every field/reference/required element. **Explicit `model: "sonnet"` parameter.** |
| 21 | `2026-04-12T05:03:42.738Z` | `general-purpose` | AVFL accuracy validator | Lens: factual accuracy — every claim traced to source material. **Explicit `model: "sonnet"` parameter.** |
| 22 | `2026-04-12T05:04:06.099Z` | `general-purpose` | AVFL domain validator | Lens: domain fitness — would a Momentum sprint-planning practitioner accept the plan. **Explicit `model: "sonnet"` parameter.** |
| 23 | `2026-04-12T05:15:26.179Z` | `momentum:dev-skills` | AVFL fixer — EDD scaffold for feature-status-practice-path | Resolve 2 confirmed AVFL findings: missing EDD scaffold and one cross-reference. Sole writer of the affected story file. |

Notable patterns:
- The 5 create-story agents were spawned twice (once as `momentum:create-story` direct subagent, then immediately as `general-purpose` wrappers calling the skill). This is a 2x spawn cost on Phase 2.
- AVFL ran the **3-lens** composition (Structural + Accuracy + Domain) — not the standard 4-lens scan profile. This matches the "checkpoint" sprint-planning AVFL profile.
- Q3 of the research spike stalled and had to be relaunched ~1h44m after initial spawn.

> ² Note on Q3: The `research` Skill invocation at `02:22:18Z` contained only Q1 and Q2. Q3 ("CLI-generated rich visual artifacts — rendering patterns") was spawned by the orchestrator directly as an `Agent` call at `02:34:50Z`, following the research workflow's subagent-per-question pattern. This is consistent with the workflow — the Skill set up the scope; Q3 spawning was driven by the orchestrator.

> Note on skill name prefix: Rows 2 and 3 in the Skill invocations table show `research` and `decision` without the `momentum:` prefix — this is how the `source` field appears as-invoked in the transcript. `§7 Benchmark Comparison Hooks` uses the fully-qualified form `momentum:research` and `momentum:decision`. Both forms resolve to the same skill.

### Subagent model parameters

4 of the 23 `Agent` tool calls carried explicit `model` parameters. A bare alias resolves to whatever the harness considers current at replay time — not pinned to the models used in the captured run.

| Spawn # | Timestamp | Description | `model` param |
|---|---|---|---|
| 15 | `2026-04-12T04:20:30.626Z` | Synthesis: feature status visualization research | `"opus"` |
| 20 | `2026-04-12T05:03:23.117Z` | AVFL structural validator | `"sonnet"` |
| 21 | `2026-04-12T05:03:42.738Z` | AVFL accuracy validator | `"sonnet"` |
| 22 | `2026-04-12T05:04:06.099Z` | AVFL domain validator | `"sonnet"` |

**Replay caveat:** At the time of this session, `"opus"` resolved to `claude-opus-4-6` and `"sonnet"` resolved to `claude-sonnet-4-6`. If the harness's default model changes between capture and replay, these aliases will resolve differently. The research synthesis was deliberately routed to Opus; a replay should verify this routing is preserved.

### TaskCreate / TaskUpdate activity

10 `TaskCreate`, 20 `TaskUpdate`. The orchestrator created at least three task plans across the session (one per skill phase: sprint-planning Phase 1–8, research Q1–Q3 + synthesis, AVFL Phase 1–4).

### Notable file reads (deduped, top 20 by frequency)

| Path | Reads | Purpose |
|---|---:|---|
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/stories/index.json` | 11 | Backlog state — checked across phase transitions |
| `/Users/steve/.claude/plugins/cache/momentum/momentum/0.12.0/skills/avfl/references/framework.json` | 7 | AVFL lens framework |
| `/Users/steve/projects/momentum/_bmad-output/research/project-knowledge-visualization-ai-2026-04-11/final/project-knowledge-visualization-ai-final-2026-04-11.md` | 6 | Pre-existing research corpus referenced by DEC-002 |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/stories/impetus-feature-status-cache.md` | 6 | Story under iteration during developer Q&A |
| `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` | 5 | Epic 13 (feature-orientation) registration check |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/stories/feature-status-skill.md` | 4 | Story rewritten after DEC-003 |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/stories/sprint-boundary-compression.md` | 4 | Story discussed extensively in developer Q&A (msgs 8, 9) |
| `/Users/steve/projects/momentum/skills/momentum/skills/avfl/references/framework.json` | 2 | Local skills tree (devved version) cross-check |
| `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/prd.md` | 2 | PRD impact discovery input |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/stories/feature-artifact-schema.md` | 2 | Wave-1 story verification |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/stories/feature-status-practice-path.md` | 2 | EDD-scaffold AVFL fix target |
| `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/decisions/dec-002-feature-visualization-and-orientation-2026-04-11.md` | 2 | DEC-002 source-of-truth re-read |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/sprints/index.json` | 2 | Sprint state for activation |
| `/Users/steve/.claude/plugins/cache/momentum/momentum/0.12.0/skills/research/workflow.md` | 1 | Research skill workflow |
| `/Users/steve/.claude/plugins/cache/momentum/momentum/0.12.0/skills/avfl/workflow.md` | 1 | AVFL workflow |
| `/Users/steve/.claude/plugins/cache/momentum/momentum/0.12.0/skills/avfl/SKILL.md` | 1 | AVFL skill loader |
| `/Users/steve/.claude/plugins/cache/momentum/momentum/0.12.0/skills/research/references/profiles.md` | 1 | Light vs medium profile lookup |
| `/Users/steve/.claude/plugins/cache/momentum/momentum/0.12.0/skills/research/references/gemini-prompt-template.md` | 1 | Gemini-prompt template |
| `/Users/steve/projects/momentum/_bmad/bmm/config.yaml` | 1 | BMM config |
| `/Users/steve/projects/momentum/.claude/momentum/gate-findings.txt` | 1 | Gate findings stream |

### Mutating CLI calls (`momentum-tools.py`)

| Timestamp | Action |
|---|---|
| `2026-04-12T00:18:07.220Z` | `sprint plan --operation add --stories feature-artifact-schema,feature-status-skill,sprint-boundary-compression,impetus-feature-status-cache,feature-status-practice-path` — initial sprint composition (5 stories, no wave assignment) |
| `2026-04-12T04:59:33.467Z` | `sprint plan --help` — re-discover wave option after auto-compaction |
| `2026-04-12T04:59:38.866Z` | Three `sprint plan --operation add` calls assigning the 5 stories to waves 1, 2, and 3 |
| `2026-04-12T05:50:20.590Z`–`05:50:34.927Z` | Multiple `sprint activate` exploratory invocations (wrong python binary, missing slug, --help) |
| `2026-04-12T05:50:40.568Z` | `sprint status-transition --help` followed by reading `sprints/index.json` to diagnose missing slug field |
| `2026-04-12T05:51:22.721Z` | `git commit` with the activated sprint state — sprint goes live |

### CMUX usage (63 calls, unusual for sprint-planning)

The developer asked for HTML mockups mid-flow ("a picture is worth a thousand words", msg 12). The orchestrator opened a browser pane and iterated on a mockup file. Full breakdown in §1 Bash sub-shape table. Highlights: 8 `browser snapshot`, 7 `browser click`, 4 `browser screenshot`, 4 `markdown open`, 3 `browser open`, 3 `browser press`, 3 `new-split right`, plus 10 chained browser operations on an existing surface (`browser --surface N <op>`). This is a meaningful divergence from a standard sprint-planning run (which typically has 0–5 cmux calls).

**Replay variability — non-deterministic mid-flow paths:** The cmux-Gemini browser detour (opening a browser surface to check the Gemini interface in response to msg 19, "I thought light research didn't use gemini…") was emergent behavior, not specified by the research skill workflow. A replay against a different model version or with different timing may not reach the same state (opening a Gemini browser surface) even when given identical inputs. Per-message comparison in the cmux section should be calibrated accordingly — cmux call counts may diverge without indicating a quality regression.

---

## 5. Outputs

### Files created or modified during the session

#### Sprint planning artifacts (`/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/sprints/sprint-2026-04-11/`)

| Path | Action | Purpose |
|---|---|---|
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/sprints/sprint-2026-04-11/specs/feature-artifact-schema.feature` | created | Gherkin spec — Wave 1 |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/sprints/sprint-2026-04-11/specs/feature-status-skill.feature` | created | Gherkin spec — Wave 2 |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/sprints/sprint-2026-04-11/specs/sprint-boundary-compression.feature` | created | Gherkin spec — Wave 3 |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/sprints/sprint-2026-04-11/specs/impetus-feature-status-cache.feature` | created (then edited once) | Gherkin spec — Wave 3 |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/sprints/sprint-2026-04-11/specs/feature-status-practice-path.feature` | created | Gherkin spec — Wave 3 |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/sprints/index.json` | modified | Sprint registered + activated |

This is the headline output of the run: 5 Gherkin specs + index.json activation. **No `sprint-plan.md` or `sprint-summary.md` was emitted at the sprint root** — only the `specs/` subdirectory was populated.

#### Story files (`/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/stories/`)

| Path | Action | Purpose |
|---|---|---|
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/stories/feature-artifact-schema.md` | created (via subagent) | Full story for Wave-1 schema work |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/stories/feature-status-skill.md` | created (via subagent), then completely rewritten after DEC-003 | Story for the feature-status skill — rewritten to reflect HTML-artifact decision |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/stories/sprint-boundary-compression.md` | created (via subagent), heavily edited (5 edits) | Story for D4 — substantial Q&A iteration with developer (msgs 8–9) |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/stories/impetus-feature-status-cache.md` | created (via subagent), heavily edited (~20 edits) | Story for D3 — most-edited file in the run; absorbed multiple developer clarifications (msgs 5–6). Edit count verified by DuckDB query (Edit + Write calls on this path = 20). |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/stories/feature-status-practice-path.md` | created (via subagent), edited once for AVFL fix | Story for D5 — practice-path rendering |
| `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/stories/index.json` | modified (3 edits) | Story registration + status transitions to ready-for-dev |

#### Planning artifacts

| Path | Action | Purpose |
|---|---|---|
| `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` | modified (3 edits) | Epic 13 (feature-orientation) registered with 5 stories |
| `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/decisions/dec-003-feature-status-artifact-design-2026-04-11.md` | created | DEC-003 — feature-status as HTML report (signals, layout, gap analysis) |
| `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/decisions/index.md` | modified | DEC-003 entry added |
| `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/prd.md` | modified (via subagent) | Add feature-orientation FRs |
| `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/architecture.md` | modified (via subagent) | Add Decisions 44–48 |

#### Research artifacts (mid-flow detour)

| Path | Action | Purpose |
|---|---|---|
| `/Users/steve/projects/momentum/_bmad-output/research/feature-status-visualization-2026-04-11/scope.md` | created | Research scope (Q1/Q2/Q3) |
| `/Users/steve/projects/momentum/_bmad-output/research/feature-status-visualization-2026-04-11/raw/gemini-prompt.md` | created | Gemini prompt template |
| `/Users/steve/projects/momentum/_bmad-output/research/feature-status-visualization-2026-04-11/raw/q1-*.md`, `q2-*.md`, `q3-*.md` | created (via subagents — exact filenames not all in transcript) | Three sub-question research outputs |
| `/Users/steve/projects/momentum/_bmad-output/research/feature-status-visualization-2026-04-11/final/feature-status-visualization-final-2026-04-11.md` | created (via synthesis subagent) | Final research synthesis (referenced by DEC-003) |

#### Mockup / scratch artifacts

| Path | Action | Purpose |
|---|---|---|
| `/tmp/feature-status-mockups/nornspun-product-path.md` | created | First mockup attempt (markdown) — rejected by developer (msg 12) |
| `/tmp/feature-status-mockups/momentum-practice-path.md` | created | First mockup attempt (markdown) — also rejected |
| `/Users/steve/projects/momentum/.claude/momentum/feature-status-mockup.html` | created (2 writes), then edited (2 edits) | HTML mockup that ultimately satisfied developer ("That looks great let's go", msg 26) |

### Sprint planning artifacts produced — summary

5 Gherkin spec files written under `/Users/steve/projects/momentum/_bmad-output/implementation-artifacts/sprints/sprint-2026-04-11/specs/`, plus the sprint index activation. **No top-level `sprint-plan.md`** was emitted in the sprint directory — sprint composition (waves, team) was carried in `stories/index.json` + `sprints/index.json` only.

### Commits made during the session

Filtered by session window (`2026-04-11 16:57 PDT` — `2026-04-11 22:53 PDT`). Working-tree timestamps in PDT; transcript timestamps in UTC. (Window end derived from `end_ts` `2026-04-12T05:53:22.990Z` UTC → `2026-04-11 22:53 PDT`.)

| Hash | Time (PDT) | Subject |
|---|---|---|
| `b9d3b8975640ed75246a41eb98ec954d1ad6015e` | 2026-04-11 17:15:56 | docs(stories,epics): register Epic 13 (feature-orientation) and 5 DEC-002 story stubs |
| `2a735596fd34229d76ff4af3352e557c8651b2e3` | 2026-04-11 17:22:32 | docs(stories): add feature-status-practice-path story |
| `72c8885098bb435a13f7720da7f176fca8773f5b` | 2026-04-11 17:22:57 | docs(stories): add feature-artifact-schema story file |
| `86a33738adfe20621bc6f2ab936ca9c081b2da57` | 2026-04-11 17:25:28 | docs(stories): add sprint-boundary-compression story — structured sprint summary at retro close |
| `cc3b36e6990e23ea0772f2b2f5ebbc559b69e739` | 2026-04-11 17:34:05 | feat(references): distill — add GUI app launch troubleshooting checklist to cmux |
| `5f73e5aef5f3e8bc7c736314545e2a6d48c344a2` | 2026-04-11 17:34:05 | feat(references): distill — add GUI app launch troubleshooting checklist to cmux (duplicate) |
| `f3f6719b47c0c0d0a886b6efc51fc4b696f6d66d` | 2026-04-11 21:24:54 | docs(research): feature planning artifact visualization — light profile, 3 sources |
| `f2d7812b55a7d14f52f986e6ce63c11da556acf1` | 2026-04-11 21:28:04 | docs(decisions): add DEC-003 — Feature Status Artifact Design (HTML report, layout, signals) |
| `46cc3ec3b7b3623d446ffdfe8b11176ccbb74e79` | 2026-04-11 21:32:12 | docs(story): rewrite feature-status-skill — HTML planning artifact per DEC-003 |
| `1b2c268d296cb934f8c8ec4fddb9dbc962c884d6` | 2026-04-11 21:49:30 | docs(specs): add Gherkin specs for sprint-2026-04-11 — 5 feature-orientation stories |
| `ddca1901a50d5b89b626fcd680a0b0cd00a16eff` | 2026-04-11 21:54:47 | docs(prd): add feature-orientation FRs from sprint-2026-04-11 spec impact |
| `02a5e31f5360a2abda103dbba1bcaa4a9fe5f4ca` | 2026-04-11 21:57:32 | docs(architecture): apply feature-orientation epic decisions 44-48 |
| `49caab79377bcd7dd8817bb755a06d3cdd8682ac` | 2026-04-11 22:00:11 | docs(sprint): team composition, wave assignments, feature-status-practice-path to ready-for-dev |
| `8aafe40e19282ddd285f82de37d1ddc68e3dac5e` | 2026-04-11 22:16:30 | fix(stories): resolve AVFL findings in feature-orientation sprint plan |
| `b4761051dd657c82e3ac5d534ee7a991aef7213e` | 2026-04-11 22:51:22 | chore(sprint): activate sprint-2026-04-11 — feature-orientation epic, 5 stories in 3 waves |

**15 commits** during the session. The orchestrator made 7 `git commit` Bash calls visible in the transcript; the remaining 8 commits were performed by spawned subagents (create-story, research, decision, AVFL fixer) operating inside their own contexts.

Note the `cc3b…/5f73…` distill commits: same author-date (`2026-04-11 17:34:05 -0700`) and same subject line, but **different parents and different commit-times**: `cc3b36e` has parent `b9d3b89` and commit-time `2026-04-11 18:48:30 -0700`; `5f73e5a` has parent `86a3373` and commit-time `2026-04-11 17:34:05 -0700`. These are two independent worktree commits made on different branches by parallel subagents running during the sprint-planning Phase 2 create-story wave — both happened to commit the same distill reference update. The identical author-date is expected (both used the same wall-clock read); the different parents confirm they were never on the same branch at commit time. One was later merged into the sprint branch and the other was orphaned. This is NOT a hook double-fire.

### Final assistant message — verbatim (timestamp `2026-04-12T05:51:36.227Z`, the sprint-activation summary)

```
Sprint activated. Here's the final state:

---

**Sprint sprint-2026-04-11 is live.**

```
Wave 1  feature-artifact-schema          (config-structure)
  ↓
Wave 2  feature-status-skill             (skill-instruction, EDD)
  ↓
Wave 3  sprint-boundary-compression      (skill-instruction, EDD)      ┐
        impetus-feature-status-cache     (skill-instruction + code)    ├─ parallel
        feature-status-practice-path     (skill-instruction, EDD)      ┘
```

All 5 stories `ready-for-dev`. Gherkin specs written and locked. Architecture and PRD updated. AVFL checkpoint passed with 2 medium findings fixed.

To begin: `momentum:sprint-dev`
```

After this, the developer asked one tail-end question (msg 28: "What is the agent running in the background?"), and the assistant explained the leftover Q3 research agent (`2026-04-12T05:53:22.990Z`):

```
It's a leftover research agent from before sprint planning began — it was researching **Q3: How CLI tools solve the "generated from code, rendered as rich visual" problem** (Istanbul/pytest-html pattern, Mermaid.js, webpack-bundle-analyzer, etc.).

That research question was already answered and incorporated into DEC-003 (the feature-status artifact design decisions). The sprint plan is fully committed and the sprint is active — this agent's output is no longer needed for the current sprint.

You can safely ignore it. It'll complete on its own and the output will be saved, but nothing is waiting on it.
```

---

## 6. Reproduction Recipe

1. **Restore working tree to pre-session state.**
   - `git -C /Users/steve/projects/momentum checkout be1ce241231d69636670889b3e3c10cc7c3943cd`
   - This run did not capture a clean pre-session `git status`, so a high-fidelity replay should run from a fully clean tree at this commit. See §2 "Pre-existing artifacts at session start" for the list of artifacts that were already on disk and must be restored separately.
2. **Install Momentum plugin v0.12.0.** v0.12.0 is no longer in the local plugin cache (current cache contains only `0.16.0`, `0.17.0`, `0.17.1`, `0.17.2`). Replay requires checking out commit `1f6d0737f64a3446b86b3c150e6dd407a8750a07` from the momentum repo and rebuilding the plugin cache from that tree. **Do NOT use the current `0.17.x` cache as a replay base** — the skill catalog has materially drifted since v0.12.0 (sprint-boundary-compression is now a deployed skill; momentum:distill, momentum:triage, momentum:feature-grooming added or substantially changed).
3. **Start a fresh Claude Code session** (v2.1.101) in `/Users/steve/projects/momentum` on `main`. Default model: `claude-sonnet-4-6` (this session ran ~99% Sonnet 4.6 with rare Opus 4.6 fallbacks). Note that 4 Agent calls carried explicit model aliases (`"opus"` for synthesis, `"sonnet"` for AVFL validators) — these resolve to the harness's current model at replay time, not to the pinned models from the captured run.
4. **Send the verbatim opening prompt from §3** (the `<command-args>` block — DEC-002 D1–D5 context, hard dependencies, design constraints, research-corpus pointer).
5. **Reply at decision points using messages 1–28 from §3 in order.**

   **Decision-point coupling — conditional messages:**

   | Msg # | Message | Trigger condition | Replay guidance |
   |---|---|---|---|
   | 10 | `Please open it on Android also` | Developer accidentally sent to wrong session | **Skip.** Msg 11 recanted it; feeding msg 10 introduces noise. |
   | 11 | `The android comment was meant for another session…` | Developer sent msg 10 then interrupted the response | Feed as-is; absorbs the cancellation. |
   | 19 | `I thought light research didn't use gemini…` | Orchestrator opened a cmux browser pane to the Gemini interface (emergent detour, not specified by the research skill) | Feed only if the replay reaches the same cmux-Gemini state. If the orchestrator doesn't open a Gemini browser pane, skip msg 19 — it becomes a non-sequitur. |
   | 21 | `Q3 is taking forever, are you certain it's not stalled?` | Q3 agent stalled for ~1h44m without output | Feed only if Q3 spawned and no completion notification arrives within ~2h of Q3 spawn. |

   Other critical pivots:
   - After Phase 1 (epic/registration): clarification on slug naming (msg 1) → `A` to approve (msg 2).
   - After story stubs registered: `Let's go!` (msg 3) → triggers create-story spawning.
   - **Mid-flow research pivot at msgs 12–17.** Developer rejects markdown mockups, demands visual artifact research. Replay must invoke `momentum:research` (light profile) with Q1/Q2 scope; Q3 spawned separately by orchestrator.
   - After Q3 relaunch completes: `Do it` (msg 23) → triggers `momentum:decision` to capture DEC-003.
   - HTML mockup iteration (msgs 24–26): developer rejects two iterations, accepts third.
   - Sprint activation (msg 27: `yes`) → triggers `sprint activate sprint-2026-04-11`.

6. **Stop after the sprint-activation summary turn** (`2026-04-12T05:51:36Z`). The 28th user message ("What is the agent running in the background?") is post-completion housekeeping — optional for replay.

---

## 7. Benchmark Comparison Hooks

Compare a replay run against this baseline on:

- **Skill invocation set and order.** Did the replay invoke `momentum:sprint-planning` → `momentum:research` → `momentum:decision` → `momentum:avfl`, in that order? Or did it complete sprint planning without the mid-flow research detour? (A short-circuit replay that skips research is a different outcome class — the developer's concerns about "Where are the screenshots?" should force a research detour on a faithful replay.)
- **Subagent spawn count and types.** Did the replay produce 23 spawns? Same composition: 5 create-story (twice — direct + general-purpose wrapper), 5 research (Q1/Q2/Q3 + Q3-relaunch + synthesis), 2 Explore (PRD/Architecture impact), 2 general-purpose (PRD/Architecture update), 3 AVFL validators, 1 AVFL fixer? (Total: 5+5+2+2+3+1 = 18 + 5 wrapper re-spawns = 23.) In particular:
  - Did the replay double-spawn create-story (5×2)? **The double-spawn is a defect baseline, not a target.** A replay producing 18 spawns (5 create-story invoked once each, not wrapped, + 13 others) represents a quality improvement and should NOT be flagged as divergence.
  - Did Q3 stall and require relaunch?
- **Sprint files written.** Were the same 5 Gherkin specs created under `…/sprints/sprint-2026-04-11/specs/`? Did the replay (incorrectly) emit a `sprint-plan.md` at the sprint root, or follow the actual pattern of carrying composition only via `stories/index.json` + `sprints/index.json`?
- **DEC-003 capture.** Was a separate decision document created mid-flow? Same slug? Same scope (HTML report, layout, signals)?
- **AVFL composition.** Did the replay run AVFL with 3 lenses (structural + accuracy + domain) at the checkpoint profile, or 4 lenses (full scan)? How many findings were generated and how many were fixed?
- **Story selection.** Did all 5 DEC-002 stories (D1–D5) make it into the sprint, or did the replay defer one as out-of-scope?
- **Wave assignment.** Did the replay produce the same 3-wave layout (D1→D2→{D3,D4,D5})? Different wave splits (e.g. D4 in Wave 1) are valid alternatives but worth flagging.
- **Commit count and shape.** This run produced 15 commits (with one duplicate). A replay producing dramatically fewer (say, 3–5) suggests subagent contexts didn't commit autonomously.
- **Tool-call shape.** 331 tool calls total; ratio Bash:Read:Edit:Agent:TaskUpdate = 121:82:37:23:20. A replay with dramatically different ratios — particularly higher Edit counts (story re-iteration) or lower Bash counts (less cmux/git activity) — suggests different navigation strategy.
- **CMUX usage.** This run had 63 cmux calls driven by the developer's mockup-iteration request. A replay reaching the same conclusion (HTML mockup approved) without the cmux-browser detour would be more efficient; a replay producing many more cmux calls without satisfying the developer would be regression.
- **Auto-compaction count.** This session crossed 3 auto-compaction boundaries (~00:32, ~04:32, ~05:10 UTC). Compare against replay — fewer crossings indicate tighter context management.
- **Wall-clock duration.** Active: ~5h 56m. A faster replay is a clear win unless it skips the research detour (which is a different outcome class).
- **Model routing mix.** ~99% Sonnet 4.6 / ~1% Opus 4.6. Compare a replay's mix; pure-Sonnet replays should produce comparable artifact quality.
- **Specific decisions to reach the same conclusion on:**
  - Should sprint planning pause for a research spike when the artifact design is undefined? (Yes — this run did.)
  - Should DEC-003 be authored mid-sprint-planning, before stories are finalized? (Yes — this run did.)
  - Should the practice-path rendering be a separate story, or a sub-task of feature-status-skill? (Separate story — this run committed to D5 as standalone.)
  - Should `feature-status-skill` be CLI text or HTML? (HTML — DEC-003 conclusion.)
  - Should the impetus cache be a derived artifact or the feature-status file itself with hash inputs? (Latter — answered in msg 5–6 dialogue.)
- **Final state.** Did the sprint activate cleanly with all 5 stories at `ready-for-dev` and the AVFL checkpoint passing? Did the branch flip to `sprint/sprint-2026-04-11` by end of session?

### Replay variability — non-deterministic mid-flow paths

The following comparison hooks may produce legitimate divergence between replays and should be calibrated accordingly — divergence here does NOT indicate a quality regression:

1. **cmux-Gemini browser detour (msgs 19+).** The orchestrator opened a browser surface to the Gemini interface in response to detecting the light research profile uses Gemini. This was emergent — not specified by the research skill workflow step. A different model version or timing may skip this browser detour entirely. Compare cmux browser call counts only after confirming whether the Gemini detour was reached.

2. **Q3 stall and relaunch (msg 21).** Whether Q3 stalls depends on agent runtime, model state, and load — not the inputs. A replay where Q3 completes normally (no stall) is not a regression.

3. **create-story double-spawn pattern (spawns 6–10).** The 5×2 spawn pattern (direct `momentum:create-story` + `general-purpose` wrapper per story) is a skill orchestration defect captured in this baseline. A replay that spawns create-story once per story (5 total, no wrappers) is a quality improvement. Do not flag 18-total-spawn replays as spawn-count mismatches unless the missing spawns are from the non-defect categories.
