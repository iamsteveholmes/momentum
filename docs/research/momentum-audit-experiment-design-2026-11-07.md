# Experiment Design — Momentum vs Bare Claude Code on a New Feature

**Status:** awaiting Steve's approval (nothing has run). **Date:** 2026-11-07. **Part of:** the Momentum pivot audit (phases 01–03 in this folder). Phase 4 (Opus verdict report) waits for this experiment's results.

## 1. Question

> On a real, sprint-sized feature Steve wants anyway, which delivers a **working feature** better — Steve + Momentum, or Steve + bare Claude Code — and at what cost in **time, tokens/money, and Steve's attention**? Fine-grained: where exactly does each arm win or lose?

Why a new feature (not a replay of sprint-2026-08-20): a replay mixes in era models and plugin 0.32 behavior. It also carries hindsight (Steve knows the 14 drive defects, and the specs were revised after them), and its spec inputs are Momentum's own output. A forward test removes all of these. Every difference between arms is the process. The replay remains an optional follow-up.

## 2. Arms

| | **Arm M — Momentum** | **Arm B — Bare Claude Code** |
|---|---|---|
| Process | Momentum as practiced: intake/create-story → sprint-planning (plan gate) → `/momentum:conduct` (build, QA, AVFL, E2E) → end-gate | Whatever bare Claude Code does with Steve driving it as a skilled user: plan mode, subagents, native Workflows, `/code-review`, tests. Steve may *ask* for these but may not paste Momentum rules, templates, or specs. |
| Config | Steve's real environment, cloned: user rules, Momentum plugin 0.34.0, nornspun `.claude/`, `.momentum/` | Fresh `CLAUDE_CONFIG_DIR`, `env -i` allowlist, long-lived OAuth token, `--setting-sources user --strict-mcp-config`. Repo stripped of `CLAUDE.md`, `AGENTS.md`, `.claude/`, `.momentum/`, `_bmad*`, process docs. Clones live **outside `~/projects`**. |
| Session model | Opus 5.5, effort high | Opus 5.5, effort high |
| Subagent models | Momentum's own tiering; stale 4.x pins handled per fork F2 | Claude Code defaults; Steve may request tiers |
| Product inputs | PRD, architecture, UX spec, product research (in place) | **Identical copies** of the same product docs + the same brief; Kotlin/Compose build constraints given to both inside the brief |
| Extra tools | Per fork F6 (identical in both) | Per fork F6 (identical in both) |
| Base | backend `0e36288` + client `b83fa62` (last human-verified pairing, still main tips) | same |
| Runtime | own HOME `~/exp/m-home`, Postgres 5432, API 8001 | own HOME `~/exp/b-home`, Postgres 5433, API 8011 |

**Proof-of-bareness gate (every B session):** `/context`, `/memory`, `/hooks`, `/skills`, `/agents`, `/mcp`, `/output-style` show defaults only. A canary question finds no Momentum or Impetus instructions. The `/context` token count is recorded for both arms. A failed gate voids the session.

## 3. Feature (fork F1)

Recommended: **Nornspun — Skuld creature design** (conversational PF2e stat block; no Foundry export).

- **Acceptance:** In the desktop app, Steve taps the newly unlocked Skuld pip and describes a creature (level, role, emotional beat). A stat-block card appears with HP, AC, saves and 3 abilities. He asks to raise the Will save. Skuld states one explicit tradeoff, and the card updates. The numbers must match the PF2e creature-building tables for that level.
- **Size:** about 8–11 stories across the backend (agent, creature model and validator, tools, router unlock) and the client (card, pip unlock, SSE payload).
- **Why this one:**
  - Its base is human-verified.
  - Today it is one-line stubs plus a locked pip, so no solution leaks.
  - The PRD calls it the core differentiator.
  - It has a deterministic oracle (the stat tables), which offsets LLM variance.
- **Alternative:** Chorgi complete character sheet. It is fully deterministic with no LLM involved, but its base is unverified and unmerged and would need freezing first.

## 4. Measurement

### 4.1 Delivery (primary)

| Measure | How |
|---|---|
| **Delivered?** | Steve's fixed acceptance checklist, written and frozen before either run starts. The final acceptance drive runs on both builds at the end, **labeled A/B by the orchestrator** (partial blinding). |
| Fine-grained scorecard | About 10 sub-capabilities scored 0–3 by independent Sonnet judges: agent behavior, validator correctness vs PF2e tables (scripted grader), tools, router unlock, SSE contract, card UI, pip unlock, tradeoff explanation, error handling, tests. |
| Hidden acceptance suite | Authored before the runs by a separate agent, from the brief only. Stored outside both arms' reach and run against both final builds. |
| Defect hunt | `/code-review` plus a fresh Sonnet adversarial reviewer per arm. Escaped defects found in Steve's drive are counted. |
| **False-done count** | Number of times an arm claimed "done" before Steve verified it works (Momentum's historical failure mode). |
| Code health | Tests pass, lint, size and duplication, architecture conformance. |

### 4.2 Time & cost (headline)

| Measure | Source |
|---|---|
| Wall-clock: start → first claimed done → **Steve-verified done** (gross and idle-excluded) | transcript timestamps + acceptance log |
| Agent compute minutes; machine-seconds of API work | `turn_duration`, OTel `active_time{cli}`, `api_request.duration_ms` |
| **Steve's active minutes**, prompts, approvals | OTel `active_time{user}`, transcript gap query (300 s cap) |
| Tokens by model (input, output, cache read, 5 m and 1 h cache write); main vs subagent vs workflow | DuckDB query deduplicated by `message.id` across root + `subagents/**` (tested; a naive sum overcounts ~1.9×) |
| $ cost (API list-price equivalent), plus plan-limit share | one pricing table for both arms; cross-checked with OTel `cost.usage` and `/usage` |
| Momentum overhead share | OTel `skill.name` / `agent.name` attribution |

**Controls:**
- Both arms run with `CLAUDE_CODE_PROMPT_CACHE_TTL=1h` and the same TTL for subagents.
- Background token use (recaps, idle compaction) is disabled or logged.
- `claude --version` and the actual `message.model` IDs are recorded.
- Telemetry is reconciled against the transcripts, within 1–2%, before the run is trusted.

### 4.3 HITL usability

| Measure | How |
|---|---|
| Delivery to the human | count, size and kind of human-facing artifacts (reports, gates, HTML); time from "ready" to Steve's decision |
| Interaction ease | prompts needed, questions asked of Steve, unanswerable or confusing asks, interruptions |
| Comprehension | self-report after each session: 6 questions, 1–5 scale plus free text ("I knew what was happening", "I knew what was needed from me", "the status matched reality", "the effort I spent was worth it", ...) |
| Observer rubric | a Sonnet observer scores each transcript for clarity, honesty of status, jargon and walls of text |
| Tooling use | tool error rate, permission prompts, retries, hook denials, environment incidents, whether the agent ran the app itself |

## 5. Phases

1. **Harness build** (subagents; about 1–2 h; side effects only in `~/exp/`):
   - Create the per-arm HOMEs and clones at the base SHAs, with local bare remotes.
   - Strip arm B, set up its fresh config dir, and write the launcher scripts.
   - Separate ports and database volumes per arm.
   - Install a local OTel collector via mise.
   - Write the acceptance checklist draft, PF2e grader and hidden suite (authored blind to both arms).
   - Make a normalized-pins plugin copy if F2 = normalize.
2. **Steve one-time steps:**
   - Run `claude setup-token`.
   - Stop his own Nornspun dev stack.
   - Approve the brief and the acceptance checklist.
3. **Dry run** (about 20 min): a trivial task in each arm. It validates bareness, telemetry reconciliation, ports and transcript capture.
4. **Runs:** both arms start together in two cmux tabs and Steve alternates between them. Each ends at Steve-verified done or the timebox (F7).
5. **Judging** (subagents): the scorecard, hidden suite, defect hunt, cost and time queries, usability metrics, and Steve's blinded A/B acceptance drive.
6. **Results report** (Sonnet), then **Phase 4 verdict** (Opus) incorporating it.

## 6. Estimates

| Item | Estimate | Basis |
|---|---|---|
| Arm M cost | ~$250–500 list-price | Momentum 08-03 built 8 stories for ~$360 (178 agents; the Fable conductor alone ~$208). Add planning. |
| Arm B cost | ~$30–200 | Unknown. This is the experiment. |
| Harness, judges, reports | ~$50–120 | similar workflows today |
| Steve's time | ~4–8 h over 1–3 days | setup ~20 min, plan gate, supervision, end-gate, 2 acceptance drives, surveys |

## 7. Forks for Steve (see the companion page)

- F1 feature
- F2 Momentum's stale model pins
- F3 HITL protocol in arm B
- F4 concurrent vs sequential
- F5 replicates
- F6 tool parity
- F7 timebox and budget cap

## 8. Known limits

- N=1 per arm is one data point. It gives fine-grained mechanisms, not statistics.
- Steve cannot be fully blinded.
- Steve's Momentum-era habits will shape how he drives arm B. That is accepted, because the real alternative is "Steve + Claude Code", not "Claude Code alone".
- The app's runtime LLM adds variance. The deterministic stat oracle offsets this.

## Sources

The scout outputs are under the session scratchpad `experiment/` folder:
- feature candidates
- model provenance (every model Momentum used is still callable)
- harness isolation
- contamination inventory
- build env
- Momentum-arm feasibility
- HITL usability
- historical cost/time
- measurement protocol
