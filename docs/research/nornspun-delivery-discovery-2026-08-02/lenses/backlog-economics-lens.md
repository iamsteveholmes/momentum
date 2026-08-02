# Backlog Economics Lens — Nornspun Delivery Discovery

**Date:** 2026-08-02
**Role:** Quantitative flow accounting of the 302-story backlog across ~4 months (Apr–Jul 2026), 10 sprints + 2 quickfixes, `.momentum/stories/index.json` + `.momentum/features.json` + `.momentum/sprints/index.json` as primary sources, cross-checked against `nornspun-client` git history.

---

## Executive Summary

1. **Zero of 15 tracked features have ever reached "done."** `.momentum/features.json` status distribution: `partial`=7, `not-started`=6, `working`=2 — and both "working" features (`llm-cost-tracking`, `evals`) are internal/dev tooling, not GM-facing capability. Every player-facing feature (campaign-init, session-prep, session-capture, living-memory, adventure-upload, proactive-norns, creature-design, etc.) sits at `partial` or `not-started` after 91+ completed stories.
2. **Feature completion is not a field that exists anywhere in sprint state.** `.momentum/sprints/index.json` schema (`active`/`completed` sprint objects) contains only `slug, status, stories, waves, approvals, team` — no feature reference at all. A sprint can complete with all stories "done" and there is no mechanism, field, or gate that asks "did any feature move forward."
3. **`features.json` is structurally stale — 2 sprints behind and missing stories outright.** Last modified 2026-06-16 (commit `0b6b064`). Of the 8 stories in sprint-2026-07-13 that declare a `feature_slug`, 7 of 8 are not even present in that feature's `stories` array in `features.json` — the file doesn't know they exist, let alone whether they shipped.
4. **Sprint-2026-07-13's own story-completion bookkeeping is internally contradictory.** All 12 of its stories are `status: review` in `stories/index.json` (one story file even reads `status: ready-for-dev`), while `.momentum/handoffs/sprint-2026-07-13-endgate-report.html` shows `shipped-merged` pills for all of them and `sprints/index.json.active.status` is still `"active"`/`locked: true` — never moved to the `completed` list. The canonical "91 done" story count undercounts actual delivered work by (at least) these 12, and no single source of truth agrees on whether this sprint is over.
5. **A whole UI subsystem was built, then deleted 5 weeks later, by design reversal — not a bug.** Five canvas components (`PartyFoundationCanvas`, `HeroProfileCanvas`, `CampaignFlavorCanvas`, `SessionZeroSeedCanvas`, `CampaignIdentityCanvas`) were built across sprint-2026-05-01 (commits `70e2f55`, `871d33a`, `5d0d7fb`, `b17f12e`, 2026-05-03) then torn out in one commit (`b559f9b`, 2026-06-07): **-3,888 / +233 lines**. Cause: SDR-011 D1 rejected the "5-phase wizard" model outright. This single reversal obsoleted/dropped/parked **20 stories** (the wizard-canvas cluster) — of sprint-2026-05-01's 7 stories, 4 (57%) were later marked obsolete.
6. **The waste ledger is 47 stories (28 dropped + 19 obsolete) = 15.6% of the whole backlog**, and roughly half of them (23/47) had a full spec written before being killed — real spec-writing effort discarded, not just triage.
7. **The `impetus-core` epic (Momentum practice tooling itself) has shipped 0 of 29 stories in nornspun's own pipeline**, despite being the 4th-largest epic by volume. At least 3 of its "obsolete" stories were satisfied by direct edits to the momentum plugin repo instead ("Already shipped in momentum repo 4d25642" / "Designed out in AVFL 0.28.0" / "Delivered by conduct engine DEC-035 D4") — the story-tracking mechanism and the actual work location are structurally decoupled for this class of change.
8. **Two whole epics — `client-platform-consolidation` (14 stories) and `cloud-platform` (13 stories) — are 0% done**, matching `content-creation` (10 stories, 0% done). Combined, 37 stories / 12% of the backlog sit in epics that have never shipped a single item.
9. **Throughput by raw story count is flat-to-rising (3→7→3→5→3→2→15→8→9 product-capability-class stories shipped per sprint across the 9 tracked sprints)** — the practice is not visibly slowing on a per-story basis. The disconnect is that this steady story throughput has never once translated into a completed feature (Finding 1), which is the central mechanism behind the developer's "stories ship, functionality doesn't" experience.
10. **The backlog is not thin — it's overstocked with ready-to-build inventory.** 100 of 150 backlog stories (67%) already have a full spec file written (`story_file: true`) and are simply unscheduled, against a throughput of ~8–15 stories per sprint. The bottleneck is not spec production; it's what gets pulled off that shelf and whether pulling it forward a feature.

---

## Body

### A. Classification methodology and full table

`.momentum/stories/index.json` has 302 entries. 154 stories carry an explicit `story_type` field (`feature`/`defect`/`bug`/`maintenance`/`exploration`/`practice`); 148 predate that field (mostly stories from the untracked pre-2026-04-05 bootstrap phase and later backlog stubs) and required slug/epic-based classification. Classification rules, in priority order:

1. `epic_slug == 'impetus-core'`, or slug/notes clearly about Momentum tooling itself (e.g. `create-momentum-*-standalone-skill`, `migrate-sdrs-from-bmad-output`, `epic-story-taxonomy-migration`) → **process-meta**
2. `story_type == 'practice'` → **process-meta**
3. Slug matches test-harness/QA-infrastructure vocabulary (Maestro, mobile-mcp, ws-scrcpy, Kotest migration, compose-driver e2e, ktor mock tests, etc.) → **test-infra**
4. Slug matches library-upgrade / cross-platform-consolidation / rename-refactor vocabulary, or the entire `consolidation-*` family (client-platform-consolidation epic) → **refactor**
5. `story_type in ('exploration',)` → **test-infra** (spikes/research, not shipped capability)
6. `story_type in ('defect','bug')` → **product-fix**
7. `story_type == 'maintenance'` (remaining) → **refactor**
8. `story_type == 'feature'` → **product-capability**
9. Fallback for `story_type is None`: slug-pattern match for `fix-*` → product-fix, `spike-*` → test-infra, else → **product-capability** (this fallback captures most of the pre-04-05 foundational agent/client bootstrap stories, which are genuinely new-capability work, not fixes or process)

Full script and per-class listing saved for audit at `/private/tmp/claude-501/-Users-steve-projects-momentum/0e9dc8d6-48c0-46d0-9396-3ef86305d045/scratchpad/{classify.py,by_class.txt,classified_rows.json}` (scratchpad — not part of the permanent record, reproducible from the rules above against the live index).

**Class × status (all 302 stories):**

| class | done | backlog | review | dropped | obsolete | parked | TOTAL |
|---|---:|---:|---:|---:|---:|---:|---:|
| process-meta | 3 | 30 | 0 | 0 | 6 | 0 | **39** |
| product-capability | 60 | 67 | 9 | 17 | 6 | 0 | **159** |
| product-fix | 14 | 10 | 1 | 8 | 7 | 2 | **42** |
| refactor | 5 | 27 | 1 | 1 | 0 | 0 | **34** |
| test-infra | 9 | 16 | 1 | 2 | 0 | 0 | **28** |
| **TOTAL** | **91** | **150** | **12** | **28** | **19** | **2** | **302** |

Notable ratios: of all **product-fix** stories ever created (42), only 14 (33%) were actually fixed — 15 (36%) were dropped or obsoleted (a defect identified, then written off rather than resolved). Of **refactor** stories (34), only 5 (15%) are done; 27 (79%) sit in backlog, dominated by the 13 still-backlog `consolidation-*` stories.

One caveat worth flagging plainly: "product-capability" as classed here is generous — it includes backend/agent-infra plumbing (e.g. `norn-routing-and-cost-observability`, `llm-cost-logging-and-usage-tracking`, `model-quality-evaluation-framework`) alongside genuinely user-facing surfaces. That plumbing is legitimately product-adjacent work, not process-meta or waste, but it is not itself a thing a GM can see or touch — which is exactly why Section D (features.json) rather than this story-class table is the more direct read on "did a human-usable capability land."

### B. The waste ledger — 47 stories dropped or obsoleted

**Tiering by story_file presence** (proxy for how much effort was sunk before the kill):

| status | story_file=false (stub, no spec written) | story_file=true (full spec written) |
|---|---:|---:|
| dropped (28) | 18 | 10 |
| obsolete (19) | 6 | 13 |

23 of 47 (49%) had a full spec — Gherkin ACs, touches list, verification method — written before being killed. The other 24 were backlog stubs killed at triage, before spec-writing cost was incurred.

**Reasons, where recorded** (`dedup_reason` field, present on 15 of the 47 — the rest have empty `notes`/`dedup_reason`, so their kill rationale is not machine-readable from the index and would require reading individual story files or SDR documents):

- **Design reversal (the wizard):** see case study below.
- **Consolidated into a different story:** `session-cost-enforcement-and-graceful-degradation` and `subscription-activation-patreon-to-in-app-tiers` both folded into a single credits/tiers/BYOK story. `sf2e-npc-mechanics-in-agent-context` folded into `sf2e-agent-conditional-prompt-sections`.
- **Superseded by a different architectural decision:** `cross-agent-awareness-rag-infrastructure-and-semantic-search` and its two sibling stories dropped per SDR-007 D3–D5 (RAG routes through `wiki-query`, not a bespoke store) — three stories' worth of spec effort invalidated by one architecture decision made after they were written.
- **Delivered by the momentum tool directly, not via nornspun's story pipeline** (see Section C, impetus-core).
- **Target file already deleted by a different story:** `session-zero-canvas-hifi-conformance-pass` and `party-foundation-complete-offered-lists` obsoleted because `remove-5-phase-wizard-from-campaign-init-screen` had already deleted `SessionZeroSeedCanvas.kt` / `PartyFoundationCanvas.kt`.

**Case study — the campaign-init wizard build-and-teardown (quantified):**

`git log --diff-filter=A` in `nornspun-client` shows the five wizard canvas components (`CampaignIdentityCanvas`, `PartyFoundationCanvas`, `HeroProfileCanvas`, `CampaignFlavorCanvas`, `SessionZeroSeedCanvas`) added across commits `70e2f55`, `871d33a`, `5d0d7fb`, `b17f12e` on **2026-05-03**, delivered by sprint-2026-05-01 stories `campaign-init-phases-1-2`, `campaign-init-screen-integration`, `campaign-flavor-tone-themes-and-world-personality`, `pc-profiles-backstory-goals-fears-and-hooks`. SDR-011 (D1) subsequently rejected the "5-phase wizard" model as a design pattern. On **2026-06-07** (5 weeks later), commit `b559f9b` ("remove 5-phase wizard from CampaignInitScreen — reduce to threshold + suggestion list") deleted them: `git show --stat b559f9b` shows **19 files changed, 233 insertions(+), 3,888 deletions(-)** — five component files and their five test files deleted outright, plus heavy rewrites to `CampaignInitScreen.kt`, `CampaignInitViewModel.kt`, and `ConversationList.kt`.

Tracing the slug family (`party-foundation-*`, `hero-canvas-*`, `session-zero-*`, `flavor-canvas-*`, `campaign-init-phases/screen-integration`, `campaign-flavor-tone-*`, `pc-profiles-backstory-*`, `fix-canvas-eyebrow-*`) turns up **20 stories total**: 10 obsolete, 7 dropped, 2 parked, and 1 (`fix-canvas-eyebrow-all-caps-remove-uppercase-transform`) still sitting in `backlog` today with `touches` pointing at four files that no longer exist in the repo (`HeroProfileCanvas.kt` and three deleted test files — confirmed absent via `ls` on the live `nornspun-client` tree) — a phantom backlog item that can never be actioned as written but is still counted among the "150 backlog" stories.

Net effect on sprint-2026-05-01: of its 7 stories, 4 (57%) were later marked obsolete by this single downstream design decision.

### C. Epic distribution — who ships, who accumulates

| epic | done | backlog | review | dropped | obsolete | parked | TOTAL | done% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fantasy-client | 57 | 44 | 4 | 9 | 10 | 2 | 126 | 45% |
| session-loop | 6 | 19 | 3 | 6 | 1 | 0 | 35 | 17% |
| impetus-core | 0 | 24 | 0 | 0 | 5 | 0 | 29 | **0%** |
| campaign-intelligence | 2 | 9 | 4 | 9 | 2 | 0 | 26 | 8% |
| agent-foundation | 18 | 6 | 1 | 0 | 0 | 0 | 25 | 72% |
| ad-hoc | 4 | 12 | 0 | 0 | 0 | 0 | 16 | 25% |
| client-platform-consolidation | 0 | 13 | 0 | 1 | 0 | 0 | 14 | **0%** |
| cloud-platform | 0 | 11 | 0 | 2 | 0 | 0 | 13 | **0%** |
| content-creation | 0 | 9 | 0 | 1 | 0 | 0 | 10 | **0%** |
| local-data-platform | 4 | 2 | 0 | 0 | 0 | 0 | 6 | 67% |
| (none) | 0 | 1 | 0 | 0 | 1 | 0 | 2 | — |

Three epics — `client-platform-consolidation`, `cloud-platform`, `content-creation` — total 37 stories (12% of the whole backlog) and have **never shipped a single story**. This lines up exactly with `features.json`'s `not-started` features (`cloud-deployment`, `user-accounts`, `creature-design`, `foundry-export`).

`agent-foundation` (72% done) and `fantasy-client` (45% done) are where nearly all delivered work concentrates — both backend agent plumbing and client UI shell, i.e. foundational/infrastructural layers, not the differentiated GM-facing journeys (`campaign-intelligence` sits at 8% done with the heaviest waste rate of any epic: 11 of 26 stories, 42%, dropped or obsolete).

**`impetus-core` — the practice epic that never ships in-repo:** 0 of 29 stories done via nornspun's pipeline, yet at least three of its five obsoleted stories carry `dedup_reason` text confirming the underlying change *did* happen — just not as a nornspun story:
- `impetus-remove-military-metaphors`: *"Already shipped in momentum repo 4d25642 (2026-04-26); grep clean across all plugin versions."*
- `avfl-reviewer-prompt-differentiation`: *"Designed out in AVFL 0.28.0 (hard-coded sub-skill framings + skepticism floor of 2)."*
- `sprint-dev-parallel-execution-default`: *"Delivered by conduct engine (DEC-035 D4); sprint-dev wave loop retired by DEC-037."*

These are genuine changes to the practice tooling, made directly in the momentum plugin repo (this repo, not nornspun) — but they were intake'd as nornspun stories, sat in nornspun's backlog for weeks, and were only closed out retroactively as "obsolete" once someone noticed the actual work had already happened elsewhere. The story-tracking system and the place where this class of work actually gets done are structurally decoupled.

### D. features.json — feature-level completion is neither achieved nor tracked

`.momentum/features.json` holds 15 features. Status distribution:

| status | count | features |
|---|---:|---|
| working | 2 | `llm-cost-tracking` (3/3 stories), `evals` (1/1) — both internal/dev-facing, not GM-facing |
| partial | 7 | `campaign-init` (3/10), `session-prep` (2/3), `session-capture` (1/2), `living-memory` (3/9), `adventure-upload` (1/2), `proactive-norns` (4/9), `system-aware` (2/5) |
| not-started | 6 | `source-citations`, `creature-design`, `foundry-export`, `ios`, `cloud-deployment`, `user-accounts` |

**Zero GM-facing features have ever reached `working`/done status.** `session-prep` — described in its own `acceptance_condition` as *"the primary user journey that Nornspun exists to serve"* — sits at 2/3 stories with an explicit note: *"Client has ZERO prep rendering (SurfaceType enum intentionally empty)."* Backend work completes; the surface a GM would actually see does not exist.

**Schema check — does sprint state track features at all?** `.momentum/sprints/index.json`'s `active` object has exactly these keys: `locked, status, stories, waves, approvals, team, slug, planned, started`. The 8 `completed` sprint objects have: `slug, planned, started, completed, status, locked, retro_run_at, avfl, stories, waves` (schema varies slightly across sprints, e.g. `avfl: "CHECKPOINT_WARNING"` appears once). **No sprint object anywhere references a feature slug, a feature status, or a feature-level acceptance condition.** A sprint's only recorded outcome is its story list and each story's per-story approval. There is no mechanical linkage from "sprint completed" to "feature progressed" — feature tracking, such as it is, lives entirely in the separate, manually-maintained `features.json`, updated only when someone runs an assessment (`ASR-006`, `last_verified: 2026-06-16`) — not automatically, not per-sprint, not per-story.

**Staleness, quantified:** `git log -1 --format=%ci -- .momentum/features.json` → **2026-06-16 17:38:38 -0700**, commit `0b6b064` ("reconcile features.json to ASR-006 for the 7 MVP clusters"). This predates sprint-2026-06-18 (started two days later) and sprint-2026-07-13 entirely. Direct check: of the 8 sprint-2026-07-13 stories carrying a `feature_slug`, 7 (`exchange-id-rename-across-norn-agents`, `episode-transcript-persistence-store-a`, `episode-auto-segmentation-boundary-model`, `episode-close-summarization-store-b`, `session-naming-two-message-close`, `session-counter-live-update-on-capture-close`, `campaign-picker-get-campaigns-client-repo`) **do not appear in that feature's `stories` array in `features.json` at all** — only `urds-post-session-capture` does. The file is not merely out of date on status; it is missing knowledge that these stories exist.

### E. Throughput trend — story count is flat-to-rising; feature completion never moves

Per-sprint story counts, chronological, from `.momentum/sprints/index.json` (`stories` list) cross-referenced against `stories/index.json` status. Sprint-2026-07-13's 12 stories are `status: review` in the index but shown `shipped-merged` in the end-gate report (Section F) — counted here as shipped since that is what the evidence supports, with the status-desync flagged separately.

| sprint | planned | stories in sprint | shipped | product-capability shipped | product-fix shipped | refactor shipped | test-infra shipped | process-meta shipped |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| sprint-2026-04-05 | 2026-04-05 | 5 | 3 | 3 | 0 | 0 | 0 | 0 |
| sprint-2026-04-08 | 2026-04-09 | 10 | 10 | 7 | 1 | 0 | 2 | 0 |
| sprint-2026-04-10 | 2026-04-10 | 3 | 3 | 0 | 1 | 2 | 0 | 0 |
| sprint-2026-04-12 | 2026-04-12 | 6 | 6 | 5 | 0 | 1 | 0 | 0 |
| sprint-2026-05-01 | 2026-05-01 | 7 | 3 | 3 | 0 | 0 | 0 | 0 |
| sprint-2026-05-25 | 2026-05-25 | 2 | 2 | 0 | 0 | 0 | 0 | 2 |
| sprint-2026-05-30 | 2026-05-30 | 15 | 15 | 5 | 8 | 2 | 0 | 0 |
| sprint-2026-06-18 | 2026-06-18 | 8 | 8 | 8 | 0 | 0 | 0 | 0 |
| sprint-2026-07-13 | 2026-07-13 | 12 | 12 | 9 | 1 | 1 | 1 | 0 |

Product-capability-class stories shipped per sprint: 3, 7, 0, 5, 3, 0, 5, 8, 9 — **rising over the second half of the series**, not declining. Raw per-sprint throughput does not show the practice slowing down. What it cannot show — because nothing in this data structure tracks it — is whether any of that shipped capability accumulated into a usable feature (Section D says: no, not once).

**Important caveat on the pre-tracking period:** 41 of the 91 "done" stories (45%) — nearly all the `agent-foundation` and early `fantasy-client` bootstrap stories (`initialize-backend-project-from-starter-template`, `urd-speaks-first-agent-conversation`, `plant-the-first-seed-campaign-init-through-conversation`, etc.) — appear in **no** sprint's `stories` list at all. These predate `sprints/index.json` tracking (raw transcripts for this period are confirmed gone per the mission brief) and were most likely delivered in an initial untracked bootstrap phase before sprint-level tracking existed. They are included in the "91 done" total but cannot be attributed to a specific sprint for trend purposes — the throughput table above only covers the 68 stories that do appear in a tracked sprint's list.

### F. Sprint-2026-07-13's status bookkeeping does not agree with itself

This finding sits at the intersection of "backlog economics" and "process health," but it directly undermines the reliability of every count in this document, so it is reported plainly:

- `.momentum/stories/index.json`: all 12 sprint-2026-07-13 stories show `status: "review"`.
- `.momentum/stories/urds-post-session-capture.md` frontmatter: `status: ready-for-dev` — a *third*, even-earlier-stage value for the same story.
- `.momentum/handoffs/sprint-2026-07-13-endgate-report.html`: contains `<span class="pill ok">shipped-merged</span>` for `urds-post-session-capture` (and, per the report's narrative text, all 12 stories were reviewed for merge/gate approval — the report's radio-button gate offers `Approve — merge to main` / `Request changes`).
- `.momentum/sprints/index.json`: the sprint is still keyed under `active` (`"locked": true, "status": "active"`), not present in the `completed` array (which holds the prior 8 sprints).

Four artifacts, four different completion states, for the same 12 stories. The `status_synced` field (present on only 16 of 302 stories total, and populated inconsistently across all sprints — not specifically absent for 07-13) is not a reliable tell here; the direct field values are. **Practical consequence for this document:** the canonical "91 done" figure used throughout undercounts real delivered work by at least 12 stories, and no file in the repository currently agrees on whether sprint-2026-07-13 is over.

---

## Counter-evidence & falsifiability

- **Throughput is not declining** (Section E) — if the hypothesis were "the practice is grinding to a halt," the story-count data contradicts that; product-capability-class stories shipped per sprint trend *up* (3→9) across the back half of the series. The failure mode this document documents is not slowing velocity — it's velocity decoupled from feature-level outcome.
- **Not every epic is 0%.** `agent-foundation` (72% done) and `local-data-platform` (67% done) show real, substantial completion — the practice does finish work in the epics closest to backend/agent infrastructure. The stall is concentrated in GM-facing journey epics (`campaign-intelligence` 8%, `session-loop` 17%) and in epics nobody has started yet (`cloud-platform`, `content-creation`, `client-platform-consolidation`, all 0%) — not uniform across the board.
- **Some obsoleted stories represent good process, not waste.** `enhance-create-story-design-fidelity-ac-pass-for-ui-stories` was marked obsolete because *"All 6 draft ACs shipped in momentum:create-story 0.28.0"* — the underlying need was met, just not via that story. Not every one of the 47 dropped/obsolete stories is a loss; several are legitimate consolidation or supersession. The 20-story wizard-canvas cluster (Section B) is the clearest unambiguous waste case because it has hard commit evidence of code built-then-deleted; the rest of the 47 vary in how much was actually lost.
- **Sample of `dedup_reason`/`notes` coverage is thin.** Only 15 of 47 dropped/obsolete stories carry a machine-readable kill rationale in the index; the other 32 have empty `notes`. This document's "why" claims are limited to that 15-story sample plus the wizard case study (traced independently via slug pattern + git history) — a full accounting of all 47 would require reading each story file and any linked SDR/ASR documents individually, which was out of scope for this lens's time budget.
- **What would prove this analysis wrong:** if `features.json` had been kept current and showed features flipping to `working` after each sprint (it does not — Section D); if sprint-2026-07-13's stories showed consistent `done` status across all four artifacts checked (they do not — Section F); if the wizard teardown commit showed a small, cosmetic diff rather than -3,888/+233 lines (it does not).

## Open questions

- **What fraction of the other 32 dropped/obsolete stories (without a `dedup_reason`) represent genuine built-then-discarded code vs. pre-build triage?** Would require reading each story file individually and checking `nornspun-client`/`nornspun-backend` git history per slug — not done here beyond the wizard-canvas cluster and the RAG/cross-agent-awareness trio.
- **Why does `sprints/index.json` still show sprint-2026-07-13 as `active` three weeks after its end-gate report was generated (2026-07-22)?** Is there a missing "close sprint" step in the conduct/retro pipeline, or was this deliberately left open pending a decision? Not determinable from state files alone — would need the retro skill's own workflow definition and whatever handoff/session artifact records why it stopped short of flipping this flag.
- **Is `features.json` updated by any automated process, or purely by manual `momentum:assessment` runs?** The evidence (two update dates, both tied to assessment docs `ASR-006` and an earlier one, four-plus-week gaps) suggests purely manual/on-demand, but no skill/workflow file was inspected to confirm there is *no* automated trigger — that would require reading the `assessment`/`conductor`/`retro` skill definitions in the momentum plugin, out of scope for this data-focused lens.
- **For the 148 stories with `story_type: None`, is my slug/epic-based classification reliable at the individual-story level, or only in aggregate?** Spot-checked roughly 20 of the ambiguous cases by inspection; the full 148 were not individually read against their story files. Aggregate class totals (Section A) should be treated as accurate to within a few stories per class, not exact to the story.
