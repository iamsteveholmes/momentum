# Spec Quality Lens — Nornspun Delivery Discovery

**Date:** 2026-08-02
**Role:** Are story acceptance criteria the right kind of criteria? — AC scope classification, verification-contract tracing, and concrete AC-passed/capability-absent case studies, sampled across April–July 2026 eras of the Nornspun project.

---

## Executive summary

- **The Definition of Done never requires reachability.** The canonical shared DoD (`docs/planning-artifacts/epics.md` lines 34–45) has 7 items — AC pass, unit tests, integration tests, lint, structured logging, PR review, AC-drift reconciliation. None requires the feature to be reachable from the app's actual entry point, wired into navigation, or behind a flag flipped ON. A story can satisfy all 7 items while the feature it built is dead code. This is **the structural root cause** the mission hypothesis points at.
- **AC wording quality is good and improved over time — the gap is in what actually gets *verified*, not what gets *written*.** July-era Gherkin `.feature` contracts read as genuinely user-scoped ("Given the Spinner… When she opens the campaign picker… Then…"). The defect is downstream: `coverage_disposition` can route a user-scoped-*worded* scenario to an API-only (`curl`) verification driver, or a `smoke` driver can go unexecuted, and the story still merges as done.
- **Traced, concrete case: three sprint-2026-07-13 stories merged "done" (empty `findings_summary`, empty `escalations` in the build ledger) while their own post-merge AVFL run recorded their core ACs as unconfirmed or failing** — `urds-post-session-capture` ("AC3 durable persistence FAILS — fresh conversation reports no sessions after confident close; DB count 0 confirms"), `session-naming-two-message-close` ("AC4 two-message rhythm unreliable… AC1/AC3 persistence unconfirmable due to silent bind failure"), `episode-close-summarization-store-b` ("recap-availability tail never exercised… contract passed only via its graceful-degradation escape hatch"). Source: `.momentum/sprints/sprint-2026-07-13/build-ledger.jsonl`.
- **A fourth case is worse than "unverified": fabricated content.** E2E on the same sprint found the persisted "captured" session was a different adventure's narrative entirely (`e2e-capture-integrity-1`, `stakes_class: high-blast-radius-architecture`) — the AC-level self-check ("Urd says 'It is written'") had already passed by the time this was caught.
- **The practice already knows this pattern and named it, twice, before this sprint.** ASR-004 (2026-05-29): *"Client interaction flows are invisible to API-level E2E (04-06: 57/71 scenarios passed yet norn-switching did nothing live)"* and *"the visual/E2E validator rubber-stamped real defects… recurring across 04-06/10/12."* A June-18-era story (`campaign-init-picker-screen-and-start-new-campaign-card.md`) quotes this verbatim as its own rationale for demanding live observation. The pattern recurred anyway in July.
- **An AC can be written with a built-in escape hatch for its own failure mode.** `campaign-init-picker-screen-and-start-new-campaign-card` AC7: *"If a fully-seated workspace open is blocked by missing seating plumbing, the click target and navigation hook are still wired… documented as a known limitation."* The AC is satisfied whether or not tapping an existing campaign actually opens it.
- **Feature-level tracking (`features.json`, introduced 2026-05-25) shows every user-facing feature cluster stuck at `"partial"`** (campaign-init, session-prep, session-capture, living-memory, adventure-upload, proactive-norns, system-aware) — zero at `"working"` or `"complete"`. Only two internal/operator features (`llm-cost-tracking`, `evals`) reached `"working"`. This is a second, independent artifact (not a transcript reconstruction) corroborating the mission hypothesis.
- **Story-done ≠ code-exists, twice-observed.** `d4-14-end-to-end-session-loop-integration-test`'s own Dev Agent Record: *"Backend skeleton had no D4 implementation (D4.2, D4.4, D4.5 marked done in stories/index.json but code not present)."* `features.json`'s campaign-init notes: *"wizard canvas Kotlin files were built then deleted — build artifacts confirm."*
- **The formal verification-contract system (`verification_method`/`harness_profile`/`momentum/verification-harness.json`) is one sprint old.** It was introduced 2026-07-13, the same day sprint-2026-07-13 was planned. Every story before it (all of April, May, June) has zero `verification_method` fields — meaning most of the corpus was never bound to an explicit driver at all; verification depended entirely on ad hoc AC wording and whatever the dev/QA/AVFL agents chose to run.
- **Even the newly-introduced harness has a known blind spot by its own design:** Compose Desktop is "AX-blind" (`momentum/verification-harness.json`) — desktop verification has no automated driver, only human/agent visual observation, and the sprint-2026-07-13 end-gate report records desktop parity as **"Not verified this session — the desktop window never reached the visible display."**

---

## Methodology

Sampled 23 story specs by AC section (not full-file reads for most) across four eras, plus the July sprint's parallel verification-contract artifacts (`.feature` / `.smoke.sh` files) for all 12 approved stories, plus supporting practice artifacts (`momentum/verification-harness.json`, `.momentum/features.json`, `docs/assessments/asr-004-*.md`, `docs/planning-artifacts/epics.md`, sprint-2026-07-13's `build-ledger.jsonl`, `coverage-plan.md`, and end-gate report).

**Sample (23 stories, all four eras):**

| Era | Stories sampled |
|---|---|
| April (sprint-2026-04-05/06, -04-08, -04-12) | `verdandi-agent-session-prep-conversations` (D4.1), `d4-14-end-to-end-session-loop-integration-test`, `accessibility-labels-content-descriptions`, `norn-switch-clears-chat-and-maintains-session`, `llm-cost-logging-and-usage-tracking`, `workflow-resilience-in-flight-persistence-and-resume`, `model-quality-evaluation-framework` |
| May (sprint-2026-05-01, -05-30) | `campaign-init-tokens-and-primitives`, `fix-post-campaigns-404-campaign-creation-endpoint-missing-or`, `remove-5-phase-wizard-from-campaign-init-screen` |
| June (sprint-2026-06-18) | `campaign-init-picker-screen-and-start-new-campaign-card` |
| **July (sprint-2026-07-13 — all 12 approved stories, required by brief)** | `migrate-desktopapp-tests-from-kotlin-test-to-kotest`, `exchange-id-rename-across-norn-agents`, `episode-transcript-persistence-store-a`, `episode-auto-segmentation-boundary-model`, `episode-close-summarization-store-b`, `session-naming-two-message-close`, `urds-post-session-capture`, `session-counter-live-update-on-capture-close`, `campaign-picker-get-campaigns-client-repo`, `backend-active-campaign-name-injection-fix`, `urd-threshold-flowrow-inline-prose-fix`, `norn-greeting-capability-menu-trim` |

For the July stories I read **both** artifacts where they exist: the plain-English "Acceptance Criteria" section of the story `.md`, and the Gherkin `.feature` verification contract in `.momentum/sprints/sprint-2026-07-13/specs/`. This dual read is what surfaces the central finding below (§2).

---

## 1. AC scope classification and distribution

Classification categories per the assignment: **unit-scoped** (function/class), **component-scoped** (one layer, mocked edges), **integration-scoped** (two-plus real layers, e.g. real DB + real HTTP, but not through the shipped client app), **user-scoped** (observable through the real app a Spinner would use).

Tallied at individual-AC granularity across the 23 sampled stories (≈158 ACs read in full):

| Scope | Approx. count | Share | Representative stories |
|---|---|---|---|
| Unit-scoped | 32 | 20% | `campaign-init-tokens-and-primitives` (design-token constants), `migrate-desktopapp-tests-from-kotlin-test-to-kotest` (test-infra meta-tests), `model-quality-evaluation-framework` (eval harness calling the agent directly, not through the app), `remove-5-phase-wizard…` (ViewModel/enum deletion) |
| Component-scoped | 11 | 7% | `verdandi-agent-session-prep-conversations` (agent behavior via `MockModel`, no real LLM, no client), `llm-cost-logging-and-usage-tracking` |
| Integration-scoped | 47 | 30% | `d4-14-end-to-end-session-loop-integration-test` (real DB, tool implementations called **directly**, explicitly *not* via the client UI or even the chat HTTP endpoint), `episode-transcript-persistence-store-a`, `backend-active-campaign-name-injection-fix`, `exchange-id-rename-across-norn-agents` (all `curl`-driven) |
| User-scoped | 56 | 35% | `accessibility-labels-content-descriptions`, `norn-switch-clears-chat-and-maintains-session`, `campaign-init-picker-screen-and-start-new-campaign-card`, `campaign-picker-get-campaigns-client-repo`, `urd-threshold-flowrow-inline-prose-fix`, `norn-greeting-capability-menu-trim`, `episode-auto-segmentation-boundary-model` (`.feature`), `session-counter-live-update-on-capture-close` (`.feature`) |
| **Mismatch — user-scoped wording, integration-only verification** | 12 | 8% | `urds-post-session-capture`, `session-naming-two-message-close` — see §2 |

**Caveat on this table:** this is a representative sample (23 of 229 story files, weighted toward the mandated July 12), not an exhaustive census. The proportions should be read as "spec quality is not uniformly unit-scoped" (it isn't — user-scoped and integration-scoped together are the majority) rather than as a precise population statistic.

**Read on the distribution:** the popular narrative that "ACs are too unit-scoped" is **not** what the sample shows. Only 20% were narrowly unit-scoped, and those were mostly appropriately so (design tokens, test-infra migration — things that genuinely are unit-level concerns). 35% were written at genuine user-scope, with observable, Gherkin-style Given/When/Then through the real app. **The defect is not AC altitude — it's AC-to-verification binding**, covered next.

---

## 2. What the Gherkin/verification contracts actually bind to — and where user-scoped wording gets routed to non-user-scoped checking

`momentum/verification-harness.json` (introduced 2026-07-13, the same day sprint-2026-07-13 was planned — see provenance note in §4) is the driver registry every July story's `verification_method`/`harness_profile` resolves against:

| `harness_profile` | Driver | What it actually touches |
|---|---|---|
| `bash` | cmux terminal | Scripts/CLI — no app |
| `curl` | cmux terminal against `http://localhost:8001` | **Backend HTTP API only** — no client app, no UI |
| `smoke` | **Maestro** on Android emulator; **desktop is "AX-blind"** — desktop verification is "pixel/observation via cmux-launched desktop build" (a human/agent visually watching a running build, not an automated driver), fallback `desktop-observation` | Real app on Android (automated); real app on Desktop (manual observation only, or skipped) |
| `document-review` | none (human review) | Specs/research only |

This mapping is coherent in principle. The defect is in `coverage-plan.md`'s **"covered-by-composition"** mechanism: it can assign a story to a scenario whose harness_profile is `curl` even when the story's own Gherkin `.feature` reads as fully user-scoped narrative.

**Concrete instance — Scenario A.** `.momentum/sprints/sprint-2026-07-13/coverage-plan.md` defines Scenario A as: *"Every step is driven through the public HTTP surface (`/health`, `POST /api/campaigns`, `POST /api/chat`…)"* — i.e., `curl`, no client app anywhere in the loop. It then **discharges** four stories through this API-only scenario, including:

- `session-naming-two-message-close` — a story whose entire subject is Urd's conversational close rhythm ("It is written.", the two-message offer/close cadence a Spinner *experiences*).
- `urds-post-session-capture` — a story whose ACs describe Urd's in-character greeting, narrative-to-structured capture, and the two-message close a Spinner *experiences*.

Both stories' plain-English ACs (`.md`) are written in user-facing, conversational language ("Urd's closing line is 'It is written.'", "the Spinner can rename conversationally"). Neither has a `.feature` file of its own (they don't need one per the coverage plan — they're "covered-by-composition"). The only verification either one gets is `exchange-id-rename-across-norn-agents.smoke.sh`-style curl assertions on Scenario A, checking HTTP status codes and SSE event shapes — **never a client app, never a screen, never a tap.**

**What happened when this was actually run** (`build-ledger.jsonl`, `avfl-on-merge` phase, 2026-07-22):

```
session-naming-two-message-close → outcome: "deferred-story-behavior-not-observed"
  evidence: "AC2 naming solid...; AC4 two-message rhythm unreliable (offer+close collapse
  into one turn, reproducible); AC1/AC3 persistence unconfirmable due to silent bind
  failure; harness heredoc bug blocked automated verdict"

urds-post-session-capture → outcome: "scenario-failed"
  evidence: "AC5 gate removal solid...; AC3 durable persistence FAILS — fresh conversation
  reports no sessions after confident close; DB count 0 confirms"

episode-close-summarization-store-b → outcome: "deferred-story-behavior-not-observed"
  evidence: "Non-blocking close confirmed; recap-availability tail never exercised (no
  committed rows for summarizer to read); contract passed only via its
  graceful-degradation escape hatch"
```

Yet the `story-terminal` events for all three (recorded earlier, at merge time) show `"outcome": "merged"`, `"findings_summary": []`, `"escalations": []` — **the stories were already marked merged/done with a clean record before the post-merge check ran and found this.** The undischarged findings are recorded as "leftover, surfaces at end-gate" — i.e., the story stays "merged," and the gap becomes a footnote in a later document rather than a blocked story.

**A fourth, worse instance from the same sprint's E2E phase** (not from the coverage-composition gap, but from the same underlying "self-check passed, real behavior didn't" pattern): `e2e-capture-integrity-1` — *"FABRICATED CAPTURE CONTENT: persisted session row contains an entirely different adventure's narrative than the one narrated ('Graul Farmhouse' … vs the narrated Sunken Ruins of Vhalos session) … no mismatch signal anywhere in the flow. Worse than silent loss — a wrong record silently replaces the real one."* `urds-post-session-capture`'s own AC1 self-check ("Urd says 'It is written.'") had already been satisfied — the model said the line, the story's smoke check would have been happy — while what got persisted was fiction.

A fifth: `session-counter-live-update-on-capture-close`'s E2E finding — the counter's own core AC ("counter increments live") could not actually be witnessed, because the only session in the test campaign was the mis-filed row from the capture-integrity bug above. Disposition: *"dismissed… Counter's live AC1 proof remains UNOBSERVED — recorded as a hollow-verification item… re-verify live after capture integrity is restored."* The AC is *logically* satisfied (code path is correct) while never having been *observed to work* — and this distinction only survives because the E2E phase happened to write it down; nothing structurally forces that record to block the merge.

---

## 3. Traced end-to-end: AC passed, capability absent (concrete examples, story → AC quote → what shipped → what a user still cannot do)

### Example A — `urds-post-session-capture` (sprint-2026-07-13)

- **Story:** "Urd post-session capture (REVISE — two-message close)."
- **AC quoted (AC3):** *"On episode close, the session record, session events, NPC encounter records, and divergences are persisted atomically… The commit is triggered as part of the two-message close… not after a confirmation question."*
- **What the self-check/merge recorded:** merged, clean (`story-terminal`, `findings_summary: []`).
- **What actually happened (avfl-on-merge, same sprint, one day later):** *"AC3 durable persistence FAILS — fresh conversation reports no sessions after confident close; DB count 0 confirms."*
- **What a user still cannot do:** narrate a session to Urd, hear "It is written," and trust that the session was saved. The receipt (the closing line) fired; the thing it claimed to do did not happen.

### Example B — `session-naming-two-message-close` (sprint-2026-07-13)

- **AC quoted (AC4):** *"The episode close is a quiet two-message rhythm… Message 1 — the offer… Message 2 — the close."*
- **What actually happened:** *"AC4 two-message rhythm unreliable (offer+close collapse into one turn, reproducible)."*
- **What a user still cannot do:** experience the designed two-beat close cadence the spec describes character-for-character; it collapses into one turn reproducibly.

### Example C — `episode-close-summarization-store-b` (sprint-2026-07-13)

- **AC quoted (AC5):** *"Store B is what the next prep reads… Verified by observing that a prep/recap issued after the task completes reflects the extracted facts."*
- **What actually happened:** *"recap-availability tail never exercised (no committed rows for summarizer to read); contract passed only via its graceful-degradation escape hatch."*
- **What a user still cannot do:** get a next-session recap that reflects a captured session — the consumer half of the produce/consume seam this story exists to build was never exercised, let alone observed working.

### Example D — `campaign-init` feature cluster (sprint-2026-05-01 → ASR-004 → present)

- **Story-level state:** sprint-2026-05-01 shipped 7 stories, all marked `done` (`campaign-init-tokens-and-primitives`, `campaign-init-phases-1-2`, `campaign-flavor-tone-themes-and-world-personality`, `pc-profiles-backstory-goals-fears-and-hooks`, `campaign-init-screen-integration`, etc.).
- **AC quoted (representative, `campaign-init-tokens-and-primitives` AC1):** *"`NornRadii.kt` exists… declares exactly three constants… grep gate: `RoundedCornerShape([0-9]` in `commonMain` returns zero matches"* — this AC is real and almost certainly did pass.
- **What actually happened, per ASR-004 (2026-05-29), the next assessment after that "done" sprint:** *"The live campaign-init flow in `nornspun-client` is still the full pre-SDR-011 5-phase wizard — none of the conversational rework is wired in"* and *"a hard blocker (`POST /campaigns` 404) means campaign creation silently fails today."* `.momentum/features.json`'s later note confirms: *"wizard canvas Kotlin files were built then deleted — build artifacts confirm"* (i.e., some of that "done" work was later discovered dead and removed, never reachable).
- **What a user still cannot do (as of 2026-05-29, after a "done" sprint):** create a campaign at all — the create endpoint 404'd.

This is the same pattern one full era earlier: unit/component-level ACs (tokens, endpoints, prompt strings) pass; the thing a Spinner opens the app to do does not work, and nobody notices until the *next* assessment cycle, days to weeks later.

---

## 4. Provenance: this pattern is already known and named inside the project, twice, before it recurred a third time

- **ASR-004** (`docs/assessments/asr-004-campaign-init-completion-audit-2026-05-29.md`, line 86): *"Client interaction flows are invisible to API-level E2E (04-06: 57/71 scenarios passed yet norn-switching did nothing live). Campaign-init is heavily client-interaction; schedule explicit live-app observation as the acceptance signal."* Line 85: *"Recurring across 04-06/10/12: the visual/E2E validator rubber-stamped real defects (wrong color on correct font, hover layout-jumps, silent send failures)."* Line 87: *"Maestro/Gherkin fixtures drift from copy changes… any fixtures referencing phase labels or old messages will silently pass while testing nothing."*
- **June-18-era story spec quotes this directly as its own rationale**: `campaign-init-picker-screen-and-start-new-campaign-card.md` — *"Prior validators rubber-stamped exactly these defects (recurring 04-06/10/12)"* — and responds by hand-writing `verification_method: smoke` with "live observation, not scenario pass counts" into that one story.
- **The formal system this hand-written fix eventually became**: `momentum/verification-harness.json`, added 2026-07-13 (commit `b339ec4`, `"feat(verification): add momentum/verification-harness.json — driver bindings, env startup, readiness probes"`), the same calendar day sprint-2026-07-13 was planned. Every story predating that commit — the entirety of April, May, and June — has **zero** `verification_method` field. The formal contract system is one sprint old at the time of this document.
- **Yet the pattern recurred inside that very first formally-harnessed sprint** (§2, §3) — the harness fixes *how* a story that gets a dedicated scenario is checked, but does not prevent `coverage-plan.md` from routing a user-facing story to an API-only composed scenario, and does not force an undischarged finding to block the merge that already happened.

---

## 5. Definition of Done — no reachability, wiring, or navigation requirement anywhere in the canonical DoD

`docs/planning-artifacts/epics.md`, lines 34–45, the **shared Definition of Done for every story in the project**:

> 1. All Acceptance Criteria pass — every Given/When/Then is verifiable and verified
> 2. Unit tests written
> 3. Integration test coverage — happy path and primary failure modes
> 4. No linting errors
> 5. Structured logging present
> 6. PR reviewed and approved
> 7. Story AC changes noted if implementation diverges

None of the 7 items requires: the feature is reachable from the app's actual entry point; it is wired into navigation the user can find without dev tooling; a feature flag gating it is ON; or a human/agent actually launched the shipped app and used the feature as a user would. Item 1 is circular with respect to this question — it certifies the ACs pass, but nothing gates *what altitude* those ACs must be written at, so a story with 8 unit-scoped ACs and zero user-scoped ones satisfies item 1 in full.

Story-level "reachability" language does appear, but **ad hoc, per-story, only when that story's author happened to think of it** — e.g. `campaign-switcher-tappable-navigation-link.md`: *"Without a tappable switcher the picker… is unreachable from inside a campaign workspace"* — never as a standing DoD gate applied uniformly. No story-template scaffolding (`bmad-create-story/template.md`, `checklist.md`) requires a reachability/navigation-wiring line either.

`features.json` (introduced 2026-05-25, `.momentum/features.json`) is the one artifact in the repo that tracks status at the right altitude — a `status` field per user-facing feature cluster (`working`/`partial`/`not-started`) with a plain-language `acceptance_condition` written at genuine user-capability scope (e.g. campaign-init: *"A GM can start a new campaign from the campaign picker… walk through a conversation with Urd… then receive a first session prep from Verdandi that references the PC's fear…"*). As of `last_verified: 2026-06-16` (campaign-init) — itself over a month stale relative to the July sprint — every user-facing cluster sits at `"partial"`. This artifact is a genuine corrective instinct inside the practice, but it is (a) not wired to sprint planning or the end-gate as a hard gate, and (b) tracked separately from, and looser than, story-level "done."

---

## Counter-evidence & falsifiability

- **AC wording is not the villain.** The plain reading of the sample contradicts a naive "specs are too narrow" story: 35% of sampled ACs were already user-scoped, Gherkin-style, and explicitly platform-paired (Android + Desktop). July-era specs in particular (`campaign-picker-get-campaigns-client-repo`, `urd-threshold-flowrow-inline-prose-fix`, `norn-greeting-capability-menu-trim`, `episode-auto-segmentation-boundary-model`) are detailed, cite exact file/line anchors, explicitly require live device/desktop observation, and — per the end-gate report — several of these specifically **did** get "Observed live on Android (contract passed)" or "(measured)". Spec-writing quality trended up across the observed eras, not down.
- **Some appropriately-scoped ACs are integration/unit-scoped on purpose and correctly so.** `exchange-id-rename-across-norn-agents` (a pure internal rename with an explicit "no behavior change" contract) and `backend-active-campaign-name-injection-fix` (a backend-only prompt-injection fix) are correctly verified at the `curl`/grep level — there is no user-visible surface to test, and writing a user-scoped Gherkin scenario for either would be spec-quality theater, not rigor. Not every AC should be user-scoped; the question is whether the *user-facing* stories get user-scoped verification, and several in this same sprint did (campaign-picker, greeting-trim, threshold-fix).
- **The practice is actively self-correcting, and doing so with increasing sophistication**, not static or blind to the problem: hand-written "live observation" mandates (June) → formal harness registry with driver bindings and Android/Desktop distinctions (July) → a dedicated E2E phase that caught the fabricated-capture finding and the hollow-counter-verification finding *before* the end-gate, and an end-gate report that explicitly lists "Still hollow" residuals rather than hiding them. If the trajectory continues, the coverage-composition routing gap (§2) is a plausibly next-fixed defect, not a permanent structural feature.
- **What would prove this lens's central claim wrong:** finding that undischarged/deferred coverage findings **do** in fact block story `status` from reaching `done` before end-gate sign-off (this document did not check story `status` transitions granularly enough to rule that out — see Open Questions), or finding that `features.json`'s `partial` statuses are simply stale bookkeeping rather than a reflection of current reality (its `last_verified: 2026-06-16` stamp is a real risk to this document's confidence — see below).

---

## Open questions

- **Did the sprint-2026-07-13 stories ever actually reach `status: done`, or are they still `status: review`?** A direct check of `.momentum/stories/index.json` during this investigation showed all 12 sprint-2026-07-13 story slugs at `status: "review"` — not `"done"` — and both the `nornspun-client` and `nornspun-backend` git repos still show `sprint/sprint-2026-07-13` as an **unmerged** branch ahead of `main` (26–27 commits each). This appears to contradict the mission brief's framing that the sprint "finished... end-gate approved" and cuts toward a *different* possible root cause (the merge/close step itself stalling) that this lens did not investigate further — flagging for whichever lens owns process/execution state.
- **Is `features.json`'s `partial` status current or stale?** `last_verified: 2026-06-16` for campaign-init predates the July sprint's episode/capture work by five weeks. It is possible session-capture or living-memory moved status in ways not yet reconciled into this file. I did not find a re-verification pass after 2026-07-13.
- **What fraction of the full 229-story corpus is unit-scoped vs. user-scoped?** This document classifies a 23-story sample, weighted toward the mandated July 12 plus a hand-picked cross-era set chosen partly *because* their titles/contexts looked evidentially rich (e.g. `d4-14-end-to-end…`, `campaign-init-picker-screen…`). A full census across all 229 stories would sharpen the distribution table in §1 and could shift the percentages meaningfully in either direction.
- **Does the coverage-composition routing gap (§2) recur in prior sprints, or is Scenario A's API-only composition of user-facing stories a one-off planning misjudgment specific to sprint-2026-07-13?** I did not find an equivalent `coverage-plan.md` for earlier sprints (the artifact type itself may be new alongside the verification-harness) to compare against.
