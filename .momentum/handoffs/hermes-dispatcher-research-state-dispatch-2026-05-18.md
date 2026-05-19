# Handoff: Hermes Dispatcher Research + State/Dispatch Architecture

**Date:** 2026-05-18  
**Session duration:** ~4 hours (resumed from interrupted prior session)  
**Status:** Research complete. Architecture discussion in progress. One open design decision pending.

---

## What Was Accomplished

### 1. Hermes-as-Dispatcher Research — COMPLETE

Full research pipeline ran against the question: **Can Hermes (Nous Research) serve as a 24/7 dispatcher/delegate with Claude Code as planner/brains, and can Hermes Kanban + worker lanes map onto Momentum?**

**Verdict: DON'T ADOPT**  
**Confidence: High**  
**AVFL score: 68/100 (ADEQUATE_WITH_CONTINGENCIES)**

Key disqualifiers:
- **State-ownership split-brain**: Hermes owns its SQLite Kanban; Momentum owns `index.json` + beads. Two sources of truth with no clean sync path.
- **Lifecycle moat bypassed**: Momentum's sprint-manager enforces FSM transitions (the whole point of the SoW model). Hermes's open Kanban board lets anyone write any status — the enforcer is gone.
- **Maturity mismatch**: Hermes is pre-1.0 with biweekly breaking changes. Not viable for a production practice stack.
- **ACP/MCP inversion**: Hermes is an MCP client, not an MCP server. The "parent-task-wakeup" callback mechanism described in early research **does not exist** — the actual callback is external (Hermes worker posts to Claude Code Channels / fakechat → localhost:8787 after `kanban_complete`).

What Hermes IS good at:
- Fan-out dispatch to independent tasks (confirmed: unlinked tasks run concurrently across OS worker processes)
- Wrapping shell tools with a local SQLite board
- Lightweight multi-agent orchestration with no infra overhead

But those strengths don't address Momentum's actual bottleneck.

**Artifacts:**
- Discovery files: `_bmad-output/research/hermes-claude-dispatcher-momentum-2026-05-18/raw/` (8 specialist files + Gemini outlier)
- AVFL report: `_bmad-output/research/hermes-claude-dispatcher-momentum-2026-05-18/validation/avfl-report.md`
- Final synthesis: `docs/research/hermes-claude-dispatcher-momentum-2026-05-18-final.md` ← canonical location
- All committed to main (13 commits ahead of origin/main at session end, no push approved)

**Key AVFL contingencies to carry forward:**
1. Circuit-breaker defaults (2 vs 3 vs 5) unresolved — don't rely on any specific value without checking `hermes-kanban-v1-spec.pdf`
2. Serial-vs-parallel per same assignee: RESOLVED (fan-out confirmed for unlinked tasks; serial only when you explicitly add parent→child dependency)
3. beads SoT state: `index.json` authoritative now; beads is post-spike target

---

### 2. State/Dispatch Architecture Discussion — IN PROGRESS

**Context**: Existing research (`docs/research/claude-code-background-dispatcher-2026-05-17.md`) proposes a Claude-native dispatcher to replace the "manually trigger sprint-dev" pattern. This session clarified what it actually means.

**The architecture:**

```
intake-queue.jsonl  ←── human/agents append new work events here
        │
        ▼
Agent SDK daemon (persistent, streaming-input mode)
  - reads queue tail; blocks waiting for new lines
  - spawns Claude Code sessions for each event
  - NOT itself doing code work — it's a job router
        │
        ▼
Claude Code session (per work item)
  - runs the actual skill/workflow (create-story, sprint-dev, etc.)
  - on completion: Stop hook appends next event to intake-queue.jsonl
        │
        ▼
Channel (research-preview) ← wake signal for next queue item
```

**Key clarifications from this session:**

- `intake-queue.jsonl`: append-only log. New work items land here when decisions/retros/completions create downstream work. The daemon tails this file as its event source. Already referenced in prior research — this is an existing design element, not new.
- The daemon is NOT an AI agent doing thinking. It's a process router — reads a queue event, spawns a Claude Code session, waits for completion.
- The ~12s Claude Code spawn cost means the daemon should be persistent (don't exit between jobs).
- Channels (MCP server, research-preview): confirmed working via spike 2026-05-17. Wake signal path is viable.
- Loop close: Stop/PostToolUse hooks append the next queue event after a session completes. The daemon picks it up automatically. No manual trigger needed.

**The two dispatcher versions under consideration:**

| | Version A | Version B |
|---|---|---|
| **Granularity** | Sprint-level | Story-step-level |
| **Trigger point** | Sprint planned → auto-trigger sprint-dev | Each story step emits a queue event |
| **Human touchpoint** | Post-sprint verification only | Configurable per step |
| **Queue event shape** | `{ type: "sprint-activated", sprint_slug }` | `{ type: "story-step-complete", story, step, next_step }` |
| **Flexibility** | Low (sprint-dev is monolithic) | High (route different steps to different agents) |
| **Complexity** | Low | High (requires step-level protocol in sprint-dev) |

---

## Open Design Decision

**Where does the human boundary sit?**

The user's mental model (validated in session):
> "Manually I run a session that does Research → Analysis → Decision → Triage/Intake, and then the dispatcher fires up, runs create-story, and then through our current sprint-dev against a single story."

That's roughly Version A. But the actual design question is:

**Everything to the LEFT of this line is manual. Everything to the RIGHT is dispatcher territory.**

```
Research → Analysis → Decision → Triage/Intake → Create-Story → Sprint-Planning → Sprint-Dev → Merge → Retro
                                                               ^
                                                    Where is the line?
```

Candidates:
- **After Triage/Intake**: Dispatcher handles everything from create-story onward
- **After Sprint-Planning**: Human reviews the plan, then dispatcher handles sprint-dev + merge + retro
- **After Sprint activation**: Human explicitly activates a sprint; dispatcher handles dev waves
- **Post-verification only**: Dispatcher handles everything but human confirms merged output before retro

This decision shapes whether Version A or Version B makes more sense, and whether sprint-dev needs to be restructured.

**This decision was NOT made in this session. It is the primary open question for the next session.**

---

## Commits Pending Push

13 commits ahead of origin/main at session end. No push was approved. These include all Hermes research artifacts and the final synthesis. Push when ready.

```
git log origin/main..HEAD --oneline
```

---

## Next Steps

1. **Decide the human boundary** — answer the question above. This is a 5-minute decision that unlocks the dispatcher design.
2. **Draft dispatcher story** — once boundary is decided, create a story for the Agent SDK daemon + intake-queue.jsonl + Channel wake integration. Belongs in the next sprint or as a spike.
3. **Push research commits** — 13 commits ready; just needs `git push` approval.
4. **Consider Hermes Kanban visualization as standalone** — separate question from dispatcher: could beads data drive a visual Kanban board? Not investigated. Low priority until dispatcher is designed.
