# Experiment Design v2 — Momentum vs Bare Claude Code: Outcome-Based, Full Loop

**Status:** awaiting Steve's approval (nothing has run). **Date:** 2026-11-07. **Version:** 2 (supersedes the development-only v1). **Part of:** the Momentum pivot audit (phases 01-03 in this folder). Phase 4 (Opus verdict) waits for this experiment's results.

## 1. Question

> Given the same feature and the same plain-language goals, which delivers better: **Steve + Momentum (its full native loop)** or **Steve + bare Claude Code (its own way)**, on:
> (a) a feature that genuinely works for a user,
> (b) honest self-assessment of what works,
> (c) a well-prioritized plan for the next development cycle,
> and at what cost in **time, tokens/$, and Steve's attention**? Fine-grained: where does each arm win or lose?

**Why full loop:** Momentum is retro, capture/triage, prioritize/plan, build, verify, measure. Development is about 25% of it. Comparing only the build step would judge Momentum on its smallest part.

**Why a new feature, not a replay of sprint-2026-08-20:** a replay mixes in era models and plugin 0.32 behavior, plus hindsight (Steve knows the 14 drive defects). A forward test isolates process. The replay stays an optional follow-up.

## 2. Core principle: tell bare Claude Code WHAT, never HOW

Naming Momentum's method (retro, triage, sprint planning, story files, Gherkin, reviewers, gates, AVFL, ledgers, feature registry) to the bare arm would only make it copy Momentum. Both arms therefore get the same plain-language goal brief. It states outcomes Steve wants (feature works, honest status, a sensible next plan) and no process. Anything in the brief that follows a Momentum format is rewritten generically.

During runs, Steve answers questions and makes product decisions. He does not direct method in either arm.

## 3. Arms

| | **Arm M: Momentum** | **Arm B: Bare Claude Code** |
|---|---|---|
| Process | Full native loop: build from its own stories via `/momentum:conduct`, end-gate, then native retro, triage and next-sprint planning up to a *proposed* next plan | Whatever bare Claude Code does on its own, given the brief + plain-language feature description only |
| Inputs | Same goal brief, plus the stories from shared planning (section 4, step 2) | Same goal brief, plus the plain-language feature description. **No stories.** |
| Config | Steve's real environment, cloned: user rules, Momentum plugin 0.34.0, nornspun `.claude/`, `.momentum/` | Fresh `CLAUDE_CONFIG_DIR`, `env -i` allowlist, long-lived OAuth token, `--setting-sources user --strict-mcp-config`. Repo stripped of `CLAUDE.md`, `AGENTS.md`, `.claude/`, `.momentum/`, `_bmad*`, process docs |
| Models | Opus 5.5, effort high; Momentum's own subagent tiering (pins per F2) | Opus 5.5, effort high; Claude Code defaults |
| Product inputs | PRD, architecture, UX spec, product research | Identical copies of the same product docs |
| Base | backend `0e36288` + client `b83fa62` (last human-verified pairing) | same |
| Runtime | own HOME `~/exp/m-home`, Postgres 5432, API 8001 | own HOME `~/exp/b-home`, Postgres 5433, API 8011 |
| Location | clones under `~/exp`, outside `~/projects` | same |

**Proof-of-bareness gate (every B session):** `/context`, `/memory`, `/hooks`, `/skills`, `/agents`, `/mcp`, `/output-style` show defaults only. A canary question finds no Momentum or Impetus instructions. `/context` token counts are recorded for both arms. A failed gate voids the session.

**Cold start:** if an arm spans days, each new session re-orients only from what that arm itself saved.

## 4. Sequence

| # | Step | Who / notes |
|---|---|---|
| 0 | Approve this design; decide F1-F7 | Steve |
| 1 | **Harness build** in `~/exp` only: HOMEs, clones, bare remotes, ports/DB volumes, launchers, OTel collector (mise), PF2e grader, normalized-pins plugin copy if F2 says so | Subagents, ~1-2 h |
| 2 | **Shared Momentum planning**, run once in the Momentum-arm clone (sprint-planning / create-story), Steve at its plan gate. Time and cost reported separately as "Momentum planning cost" | Momentum + Steve |
| 3 | **Translation agent** rewrites the stories into a plain-language feature description: what it does, user-visible behaviors, how Steve will judge it done. No story files, slugs, Gherkin, AC numbering, Momentum vocabulary, or file-by-file task breakdown. A leak check follows. Steve edits the description and the goal brief. Steve also **seals his own private top-5 "what I'd want next"** | Agent + Steve |
| 4 | **Dry run** (~20 min): bareness proof, telemetry reconciliation, ports, transcript capture | Subagents |
| 5 | **Both arms run concurrently.** M: `/momentum:conduct`, end-gate, native retro/triage/next-sprint planning up to a proposed next plan (Steve does not approve it). B: bare Claude Code with brief + description only | Steve answers, never directs method |
| 6 | **Judging** (section 5) | Subagents + Steve |
| 7 | **Results report**, then **Phase 4 Opus verdict** | Sonnet, then Opus |

Steve's one-time setup: run `claude setup-token`, stop his own Nornspun dev stack, approve the brief and checklist.

## 5. Outcomes scored

### 5.1 Delivery (a working feature)

| Measure | How |
|---|---|
| Steve's acceptance checklist | Derived from the plain-language description, frozen before the runs |
| Final acceptance drive | Blind A/B: builds labeled by the orchestrator (partial blinding) |
| Hidden test suite | Authored from the description only, stored outside both arms' reach, run on both final builds |
| Sub-capability scorecard | ~10 capabilities scored 0-3 by independent judges (agent behavior, validator vs PF2e tables, tools, router unlock, SSE contract, card UI, pip unlock, tradeoff explanation, error handling, tests) |
| PF2e stat-table grader | Scripted; the deterministic oracle that offsets runtime LLM variance |
| Defect hunt | Fresh adversarial reviewer per arm plus defects found in Steve's drive |

### 5.2 Honesty (self-assessment)

Every "done / working / verified" claim each arm makes is checked against reality. Metric: **false-done count** (claims of done that Steve's drive or the hidden suite contradicts), plus the count of accurate caveats volunteered.

### 5.3 Next-cycle plan

| Measure | How |
|---|---|
| Normalization | Both plans rewritten onto one identical neutral one-page format with no Momentum vocabulary |
| Blind rating | Steve rates both plans without knowing which arm wrote which |
| Overlap | Match against Steve's sealed top-5 |
| Real-gap check | Judges test whether each item addresses a real gap, including defects found in the acceptance drive |
| Provenance | Momentum items tagged *inherited-from-backlog* vs *new*, so a pre-existing backlog is not scored as fresh insight |

### 5.4 Time and cost

| Measure | Source |
|---|---|
| Wall-clock: start, first claimed done, **Steve-verified done** (gross and idle-excluded) | transcript timestamps + acceptance log |
| Agent compute | `turn_duration`, OTel `active_time{cli}`, `api_request.duration_ms` |
| **Steve's active minutes**, prompts, approvals | OTel `active_time{user}`, transcript gap query (300 s cap) |
| Tokens by model (input, output, cache read, 5 m and 1 h cache write), main vs subagent vs workflow | DuckDB query deduplicated by `message.id` across root + `subagents/**` (a naive sum overcounts ~1.9x) |
| $ cost (API list-price equivalent) and plan-limit share | one pricing table for both arms; cross-checked with OTel `cost.usage` and `/usage` |
| Momentum overhead share | OTel `skill.name` / `agent.name` attribution |

**Controls:** both arms use `CLAUDE_CODE_PROMPT_CACHE_TTL=1h` (subagents too). Background token use is disabled or logged. `claude --version` and actual `message.model` IDs are recorded. Telemetry is reconciled to transcripts within 1-2% before the run is trusted.

### 5.5 HITL usability

| Measure | How |
|---|---|
| Artifacts delivered | Count, size, kind of human-facing artifacts; time from "ready" to Steve's decision |
| Interaction ease | Prompts needed, questions asked of Steve, unanswerable or confusing asks, interruptions |
| Comprehension | 6-question self-report per arm, 1-5 plus free text ("I knew what was happening", "I knew what was needed from me", "status matched reality", "effort was worth it", ...) |
| Observer rubric | Sonnet observer scores each transcript for clarity, honesty of status, jargon, walls of text |
| Tooling use | Tool error rate, permission prompts, retries, hook denials, environment incidents, whether the agent ran the app itself |

## 6. Forks for Steve

### F1. Which feature
- **What:** the single feature both arms build.
- **Why:** it sets the oracle quality and the risk of a broken base.
- **Evidence:** Skuld today is one-line stubs plus a locked pip, so no solution leaks. Base is the last human-verified pairing (backend `0e36288`, client `b83fa62`). PF2e creature-building tables give a deterministic oracle. About 8-11 stories of size.
- **Recommendation:** Skuld creature design (conversational PF2e stat block, no Foundry export). Done means: Steve taps the Skuld pip, describes a creature, gets a stat-block card (HP, AC, saves, 3 abilities), asks to raise Will, and Skuld states one tradeoff and updates the card with table-correct numbers.
- **Options:** Skuld (rec) / Chorgi character sheet (fully deterministic, but base unverified and unmerged, needs freezing first).

### F2. Momentum's stale 4.x model pins
- **What:** Momentum pins AVFL adversary `claude-opus-4-6`, enumerator/fixer `claude-sonnet-4-6`, consolidator `claude-haiku-4-5`.
- **Why:** old pins confound "process" with "older models".
- **Evidence:** model provenance scout; all still callable.
- **Recommendation:** normalize to 5.5 equivalents in an experiment-only plugin copy via `--plugin-dir` (live plugin untouched).
- **Options:** normalize (rec) / as-is / both (extra cost).

### F3. Where Momentum's shared planning runs
- **What:** the repo in which sprint-planning/create-story executes once.
- **Why:** planning writes `.momentum/` state and story files.
- **Evidence:** the experiment clone already carries the Momentum config.
- **Recommendation:** in the Momentum-arm experiment clone. Live nornspun stays clean; stories can be ported back afterwards.
- **Options:** experiment clone (rec) / live nornspun repo.

### F4. Concurrent vs sequential
- **What:** run both arms at once or one after the other.
- **Why:** concurrent saves calendar time; sequential is cleaner on Steve's attention.
- **Evidence:** separate HOMEs and ports remove runtime clashes; OTel `active_time{user}` splits Steve's time per arm.
- **Recommendation:** concurrent, two cmux tabs.
- **Options:** concurrent (rec) / sequential.

### F5. Replicates
- **What:** runs per arm.
- **Why:** N=1 gives mechanisms, not statistics.
- **Evidence:** cost per arm in section 7.
- **Recommendation:** N=1 now; replicate only if the result is close.
- **Options:** N=1 (rec) / N=2 / N=3.

### F6. Tool parity
- **What:** extra tools each arm may use.
- **Why:** unequal tools would confound the result.
- **Evidence:** Maestro and cmux-cua are needed to drive the desktop app.
- **Recommendation:** identical explicit MCP set for both: Maestro + cmux-cua; no claude.ai connectors in either.
- **Options:** parity set (rec) / none / Steve's full set.

### F7. Timebox and cap
- **What:** when each arm stops.
- **Why:** bounds spend and calendar time.
- **Evidence:** 08-03 Momentum build cost ~$360 for 8 stories.
- **Recommendation:** each arm ends at Steve-verified done plus its next-cycle plan, or at 3 calendar days / $500 list-price (excluding shared planning), whichever first.
- **Options:** rec / tighter cap / no cap.

## 7. Estimates (all estimates)

| Item | Estimate | Basis |
|---|---|---|
| Shared Momentum planning | ~$30-100 + Steve ~0.5-1 h at plan gate | est. |
| Arm M build + loop | ~$250-550 | est.; 08-03 build ~$360 for 8 stories |
| Arm B | unknown | this is the experiment |
| Harness, judges, reports | ~$60-150 | est. |
| Steve total | ~5-9 h over 2-4 days | est. |

## 8. Known limits

- N=1 per arm: one data point, not statistics.
- Steve is not fully blind (partial blinding on the drive and plan rating only).
- The bare arm inherits Momentum's planning **content** via the description, though not its format. Planning quality is therefore compared only at the next-cycle step.
- Runtime LLM variance in the app; the PF2e oracle offsets it in part.
- Steve's Momentum-era habits shape how he answers in arm B; accepted, since the real alternative is "Steve + Claude Code".

## Sources

Scout outputs under the session scratchpad `experiment/` folder: feature candidates, model provenance, harness isolation, contamination inventory, build env, Momentum-arm feasibility, HITL usability, historical cost/time, measurement protocol.
