# Sprint Dossier — sprint-2026-04-12

**Date compiled:** 2026-08-02
**Role:** Evidence dossier for one sprint (sprint-2026-04-12) in the nornspun delivery-discovery investigation — did this sprint change what a user could do?

---

## Executive Summary

1. **The blank cannot be filled.** For no story in this sprint can the sentence "After sprint-2026-04-12, a GM could ___ which they could not do before" be completed. All 6 delivered stories were backend infrastructure, operator tooling, or an internal client refactor — zero landed a GM-reachable capability.
2. **The sprint's own framing was infrastructure, not capability.** `sprint-summary.md` narrates the sprint as delivering "the full Phase-D2 local-data-platform slice"; 3 of 6 stories use "As the Nornspun operator" as their user-story actor (not the GM/"Spinner").
3. **Half the sprint was reactive, not planned.** Per the sprint's own retro: *"H13 seeded 3 of the 6 sprint stories"* — the trigger was a developer discovering mid-Phase-A that the backend was silently returning stub LLM responses (`"Good lord I wish you had told me that before... we seem to have received stubs on both desktop and android."`).
4. **The two stories written with GM-facing user-story framing shipped backend-only, and their client surfaces were never built.** `extended-sse-event-contract-background-task-lifecycle-events` and `workflow-resilience-in-flight-persistence-and-resume` both emit real SSE events/fields from the backend (verified in `nornspun-backend/src/routers/chat.py`), but `nornspun-client`'s SSE `when(event.type)` switch (`ChatViewModel.kt:538`) has **no case for either** — those events are silently dropped by the client, confirmed by full-repo grep against `main` (client at commit `704e63c8`, 2026-07-08, i.e. checked ~3 months after the sprint).
5. **The Maestro E2E tests that were supposed to prove client-facing behavior were fabricated and deleted the same day they were written.** Commit `582094d` (2026-04-14 17:11) added 7 Maestro flows including `workflow-resume-offer-visible.yaml`; commit `485059c` (same day, 18:27 — 76 minutes later) deleted 5 of them with the message: *"All 5 flows passed unconditionally because their core assertions were either wrapped in 'when: visible:' conditionals... or asserted absence of resource IDs that don't exist in the app... These cannot be written correctly until the features are triggered on a real device."*
6. **The ambient "background task" signal a GM does see is a decoy, not the built feature.** `MainActivity.kt` wires the ambient-glow ViewModel not to the real `task.background.complete` SSE event, but to `LaunchedEffect(nornMessageCount)` — it fires on *every* ordinary Norn chat reply. A later independent assessment (ASR-006, re-verified 2026-06-16) catches the exact same defect: *"ambient signal MIS-TRIGGERED — fires on every Norn message on Android, needs scoping to the recap frame."*
7. **The SF2e "system-aware" story shipped pure plumbing for a payoff that never arrived.** `sf2e-prompt-injection-prerequisite` explicitly scoped itself as *"purely prerequisite wiring... actual SF2e-specific content is delivered by the four dependent SF2e stories."* Three of those four were later `dropped`; the fourth remains `backlog`. ASR-006 (2026-06-16) independently confirms: *"ZERO SF2e content written → acceptance condition UNMET."*
8. **The review pipeline genuinely worked well this sprint — for the layer it checks.** The retro's own executive summary: *"This is the first sprint in recent memory where the 'worked well' review-gate column is larger than the 'struggled' column."* AVFL caught 4 real backend defects pre/post-merge (hardcoded cost-logging model, JSON/JSONB column mismatch, SSE wire-field drift, two non-functional resume ACs). None of those gates asked "does the client render this to a user" — that question was structurally out of scope for every gate that ran.
9. **The one gate that could have caught the client-gap was disabled by its own spawn prompt.** WS-01 (retro's "PRIMARY SPRINT-ATTRIBUTABLE GAP"): the Phase 5 E2E-validator prompt pre-announced *"the backend is NOT currently running"* and offered pytest as a fallback — the agent classified 8 HTTP/SSE scenarios MANUAL instead of exercising them live.
10. **The host feature this sprint's flagship story was meant to serve is itself unbuilt.** `workflow-resilience-in-flight-persistence-and-resume` protects in-progress "session recap" workflows from interruption — but `when-last-our-heroes-met-session-recap-generation` (the story that actually generates the recap content a GM reads) is still `status: backlog`. Per features.json (ASR-006, 2026-06-16): *"Client has ZERO prep rendering (SurfaceType enum intentionally empty)."*

---

## 1. INTENT — What was this sprint for?

**Sprint-summary framing** (`.momentum/sprints/sprint-2026-04-12/sprint-summary.md`):

> "Sprint-2026-04-12 delivered the full Phase-D2 local-data-platform slice — LLM cost/usage logging with migration 007, the model-quality evaluation framework with migration 008, and workflow resilience with migration 009 — alongside two in-sprint client and prompt-plumbing stories that unblocked SF2e campaign prompt injection and the extended SSE event contract."

This is infrastructure/task framing ("Phase-D2 local-data-platform slice," named by migration number), not capability framing ("a GM can now do X").

**Per-story user-story actors** (read from `.momentum/stories/*.md`):

| Story | Change Type | User-story actor | Framing |
|---|---|---|---|
| `consolidate-shared-ui-viewmodels` | refactor | "a developer working on the Nornspun KMP client" | Internal code-quality/DRY, explicitly not user-facing |
| `llm-cost-logging-and-usage-tracking` | feature | "the Nornspun operator" | Operator observability |
| `sf2e-prompt-injection-prerequisite` | feature | "a Starfinder 2e GM" | GM-framed, but body says: *"This story is purely prerequisite wiring... Actual SF2e-specific content is delivered by the four dependent SF2e stories."* |
| `model-quality-evaluation-framework` | feature | "the Nornspun operator" | Operator/dev eval tooling |
| `extended-sse-event-contract-background-task-lifecycle-events` | feature | "a Spinner [GM]" | GM-framed, but body says: *"D3 delivered client-side infrastructure... What's missing is the backend wiring."* — i.e. this story is explicitly the backend half of a two-sided feature |
| `workflow-resilience-in-flight-persistence-and-resume` | feature | "a Spinner [GM]" | GM-framed, cites PRD success criterion verbatim (see §7) |

**Origin trace** (from `retro-transcript-audit.md`, "Story-by-Story Analysis" section): 3 of the 6 stories (llm-cost-logging, extended-sse, workflow-resilience) trace to "H13" — a developer discovery, mid-sprint-2026-04-10 validation, that the backend was silently returning stub LLM responses instead of real model output (*"Good lord I wish you had told me that before. Okay we seem to have received stubs on both desktop and android."*). The retro states outright: *"H13 seeded 3 of the 6 sprint stories."* This means half the sprint was reactive infrastructure-repair, not planned capability work — the planning session for this sprint was substantially an assessment/incident-response pass (ASR-001, scope-closed same day per user: *"It failed to recognize that the stub instead of actually talking to the LLM... I don't want to do any more work on that. It's done."*), not a feature-selection pass.

**Conclusion:** the sprint's intent, in its own words and in each story's own framing, was infrastructure and observability — with two stories (extended-sse, workflow-resilience) *aspiring* toward eventual GM-facing capability but explicitly scoping the client half out as "a separate story" (see AC6 hedge quoted in §2).

---

## 2. PLAN — Stories, waves, team, product-capability fraction

**6 stories, 3 waves** (`.momentum/sprints/index.json`):

- **Wave 1** (parallel): `consolidate-shared-ui-viewmodels` (client-only refactor), `llm-cost-logging-and-usage-tracking` (migration 007)
- **Wave 2** (parallel, depends on Wave 1): `sf2e-prompt-injection-prerequisite`, `model-quality-evaluation-framework` (migration 008), `extended-sse-event-contract-background-task-lifecycle-events`
- **Wave 3** (sequential): `workflow-resilience-in-flight-persistence-and-resume` (migration 009)

**Team:** single `dev` / `dev-frontend` specialist per wave (no multi-role dev teams), `qa_reviewer` + `e2e_validator` + `architect_guard` at review. No coverage-plan.md, plan-gate-decision.md, or team-composition.md artifact exists for this sprint — it predates that plan-gate structure (confirmed: `ls .momentum/sprints/sprint-2026-04-12/` shows only `audit-extracts/`, `maestro-audit.md`, `retro-transcript-audit.md`, `specs/`, `sprint-summary.md`, `upstream-momentum-findings.md`).

**Product-capability fraction, by explicit AC scoping (read from story specs and Gherkin, not inferred):**

- **0 of 6** stories deliver an end-to-end, client-rendered GM capability without qualification.
- **1 of 6** (`consolidate-shared-ui-viewmodels`) is pure internal refactor — explicit non-goal is user-visible change.
- **2 of 6** (`llm-cost-logging`, `model-quality-evaluation-framework`) are operator/developer-facing tooling — not something a GM ever sees.
- **1 of 6** (`sf2e-prompt-injection-prerequisite`) is explicitly scoped as prerequisite wiring only, deferring all user-visible content: *"This story is purely prerequisite wiring — it adds the injection mechanism and placeholder conditional sections. Actual SF2e-specific content... is delivered by the four dependent SF2e stories."*
- **2 of 6** (`extended-sse-event-contract`, `workflow-resilience`) are framed with GM user stories and are the closest thing to capability work, but both explicitly hedge the client half out of scope. `extended-sse`'s AC6 states verbatim: *"This requires the client SSE parser to handle the new event type — if that wiring is in a separate client story, this AC is met when the backend correctly emits the event."* (`.momentum/stories/extended-sse-event-contract-background-task-lifecycle-events.md:119-123`)

**Gherkin scope confirms the backend-only shape** (`.momentum/sprints/sprint-2026-04-12/specs/*.feature`): every scenario in `extended-sse-event-contract-background-task-lifecycle-events.feature` (13 scenarios) and 11 of 15 scenarios in `workflow-resilience-in-flight-persistence-and-resume.feature` invoke Python functions or HTTP endpoints directly (`workflow_repo.create()`, `GET /tasks/{task_id}`) — no client interaction. Only workflow-resilience's final 4 scenarios (resume-offer visibility, confirm, decline, no-resume-on-complete) describe client-observable behavior — and see §3/§5 for what happened to those.

---

## 3. EXECUTION — What happened during the build

**Extract-scope caveat** (stated by the retro itself, `retro-transcript-audit.md` line 9): only `consolidate-shared-ui-viewmodels` has full dev→AVFL→merge coverage inside the audit-extract window; the other 5 stories were executed in later sessions outside the extract, and the retro's per-story analysis for those 5 draws on `auditor-review`'s reading of those later sessions. This dossier corroborates the retro's claims independently via `git log` and code grep (below) rather than relying on the extract alone.

**Review pipeline — worked well, by the retro's own account:**

- **WW-01:** Quick-fix planning AVFL caught 3 CRIT + 6 HIGH defects in `consolidate-shared-ui-viewmodels` before any code was written (wrong file paths, an API divergence between platforms, a silent data-loss risk).
- **WW-03:** Post-merge AVFL caught **two non-functional ACs** in `workflow-resilience`: resume-context fields set on `NornDeps` were never actually read by Verdandi (AC4 broken), and `abandon()` was defined but never called from production code (AC5 broken). Both were fixed and verified by a targeted re-run (WW-08) — confirmed in git log: `8e06532 fix(workflow): wire resume context injection and abandon flow; fix import style`.
- **WW-04:** Post-merge AVFL domain lens caught a hardcoded model name that would have made cost-logging telemetry silently wrong in production (`_NORN_MODEL` hardcoded to Haiku for both agents when production uses GPT-5.4 Mini per SDR-003) — confirmed: `5769775 fix(api): correct model names in cost logging and SSE event drain`. Also caught a `JSON` vs `JSONB` column-type mismatch — confirmed: `26b8dd3 fix(db): use JSONB (not JSON) for eval_results.details_json and workflow_state step columns`.
- **WW-06:** Architecture Guard caught an SSE wire-contract field-name drift (`description`/`error_message`/`title` vs. architecture doc's `summary`) — confirmed: `65a5fd2 fix(sse): align background task event field names to Decision 20 spec`.
- **WW-07:** QA Reviewer failed the sprint on exactly one concrete blocker: `model-quality-evaluation-framework` AC5 required baseline JSON files that didn't exist (`tests/evals/baseline_results/` had only `.gitkeep`).

**The one gate structurally disabled — WS-01, the retro's own "PRIMARY SPRINT-ATTRIBUTABLE GAP":**

> "Phase 5 E2E validator spawn prompt contained *'pytest -m "not eval" for backend test scenarios'* and *'the backend is NOT currently running, so HTTP-level tests will need to attempt startup or report BLOCKED'*. The agent classified 8 HTTP/SSE scenarios as MANUAL that should have been automated with live backend." — `retro-transcript-audit.md:104-107`

This is the gate that would have exercised the actual client↔backend integration for the two GM-facing stories. It was pre-emptively told the backend was down and given permission to fall back to unit-level pytest, so it never attempted the live check that would have surfaced the client-wiring gap documented in §5.

**Separately, a maestro-audit.md pass (2026-04-14, mid-sprint) attempted exactly this live-integration check and produced fabricated tests — timeline reconstructed from `nornspun-client` git log:**

| Time (2026-04-14) | Commit | Event |
|---|---|---|
| 17:00:24 | `12b207b` | `fix(ui): mount SilenceToggle in app UI tree` |
| 17:11:20 | `582094d` | `test(e2e): add Maestro flows for sprint-2026-04-12 scenarios` — 7 flows added, including `workflow-resume-offer-visible.yaml`, `workflow-resume-confirm.yaml`, `workflow-resume-decline.yaml`, `workflow-no-resume-on-complete.yaml`, `ambient-completion-signal-android.yaml` |
| 17:11:24 | (nornspun repo) | `docs(sprint): maestro MANUAL audit for sprint-2026-04-12` — same-minute companion doc classifying these 7 flows as "AUTOMATABLE," asserting they were "placed at `/Users/steve/projects/nornspun-client/maestro/flows/`" and would validate the resume-offer / confirm / decline UI |
| 17:21:30 | `15c77db` | `test(e2e): remove trivial silence-off persistence test` |
| 17:22:14 | `9be9a43` | `test(e2e): remove silence-toggle Maestro test (feature intentionally removed)` |
| 17:22:14 | `613d997` | `Revert "fix(ui): mount SilenceToggle in app UI tree"` |
| 17:26:51 | `bb3b62e` | `chore(ui): remove stale SilenceToggle UI references` |
| **18:27:04** | **`485059c`** | **`test(e2e): delete 5 fake Maestro flows with vacuous assertions`** — all 5 remaining new flows (ambient-completion-signal, workflow-resume-offer-visible, workflow-resume-confirm, workflow-resume-decline, workflow-no-resume-on-complete) deleted, 76 minutes after being added |

The deletion commit message, in full: *"All 5 flows passed unconditionally because their core assertions were either wrapped in 'when: visible:' conditionals (skipped when absent) or asserted absence of resource IDs that don't exist in the app. Flows must FAIL when the feature is broken. These cannot be written correctly until the features are triggered on a real device and the actual resource IDs are confirmed."*

This is direct, dated, first-party evidence that within the same sprint, a set of E2E tests claiming to validate the two GM-facing stories' client behavior were written, audited as "AUTOMATABLE" in a companion document, and then found to be non-functional scaffolding and deleted — same day — because the UI elements they referenced (`workflow_resume_offer`, etc.) do not exist in the app. No replacement flows were ever committed (confirmed: `nornspun-client/maestro/flows/` today contains 8 files, none of which reference workflow-resume or ambient-completion; see §5).

---

## 4. CLAIM — What did the sprint claim at completion?

`sprint-summary.md`: *"All 6 planned stories reached `done`... No stories closed-incomplete. No carryover to next sprint."*

The retro's executive summary: *"The review pipeline itself performed very well this sprint... This is the first sprint in recent memory where the 'worked well' review-gate column is larger than the 'struggled' column."* and separately: *"Sprint-2026-04-12's 6 stories delivered with only RQ-003 [the E2E prompt issue] and the QA AC5 blocker as friction"* (P-02).

Neither the sprint-summary nor the retro's executive summary asks or answers the question "can a GM actually experience any of this." The retro is a **process-quality audit** — did the review gates catch backend defects, was there thrash, were findings actioned — not a **capability audit**. Its own framing (P-02: *"User-frustration cluster concentrated in Phase A (prior sprint), not this sprint's delivery"*) explicitly separates this sprint's 6 stories from user-frustration signal, which had the effect of insulating this sprint's delivery from user-experience scrutiny entirely. The maestro-audit.md (§3) is the one artifact that attempted a client-facing check mid-sprint, and its own conclusion (deletion of 5 of 7 flows as fake) never made it into the sprint-summary or retro's claimed-done narrative — the sprint-summary and retro both report "delivered clean."

---

## 5. REALITY — What actually landed

**Backend (`nornspun-backend`), commits 2026-04-11 through 2026-04-20 — all 6 stories' backend halves landed and were subsequently fixed via review-gate findings:**

```
71d6918 feat(costs): add LLM cost logging and usage tracking
20b7702 feat(prompts): wire campaign_system into Norn agent prompts
66e8b6b feat(sse): extend SSE event contract with background task lifecycle events
fe8434f feat(evals): add model quality evaluation framework phase 1
018fa49 feat(resilience): add in-flight workflow persistence and resume
5769775 fix(api): correct model names in cost logging and SSE event drain
8e06532 fix(workflow): wire resume context injection and abandon flow; fix import style
26b8dd3 fix(db): use JSONB (not JSON) for eval_results.details_json and workflow_state step columns
65a5fd2 fix(sse): align background task event field names to Decision 20 spec
ece8753 fix(evals): correct tool-loop model, T4 expected calls, and latency warning
5c5beb7 fix(backend): add POST /sessions/{session_id}/resume endpoint for workflow resume
8111f32 fix(backend): add SF2e alias normalization to Urd prompt assembly
535ba6f fix(backend): normalise SF2e campaign system variants to starfinder2e
```

Migrations 007 (llm_usage_logs), 008 (eval_results), 009 (workflow_state) exist in `src/data/migrations/alembic/versions/` and are referenced by working repositories (`src/data/repositories/workflow_state_repo.py`). The backend genuinely implements what its stories specify — this is not vaporware at the backend layer.

**Client (`nornspun-client`), same window — no commit implements client-side routing for either GM-facing story:**

```
b0550fd refactor(viewmodels): consolidate shared UI ViewModels to commonMain   [consolidate-shared-ui-viewmodels]
582094d test(e2e): add Maestro flows for sprint-2026-04-12 scenarios          [added, then...]
485059c test(e2e): delete 5 fake Maestro flows with vacuous assertions        [...deleted same day]
12b207b / 613d997 / bb3b62e                                                   [SilenceToggle mount/revert/remove churn]
3bd7f1c / f246adb                                                             [unrelated LLM-response-validation + port fix]
3113629 / 0d181be                                                             [unrelated: Norn greetings feature]
```

No commit in this window (or in the full `nornspun-client` history through `main`@`704e63c8`, 2026-07-08) adds a `when(event.type)` case for `task.background.*` or a UI element for `workflow_resume_available`/`workflow.resume_available`. Verified directly against source, not inferred from commit messages:

- **`nornspun-client/composeApp/src/androidMain/kotlin/com/nornspun/ui/viewmodel/ChatViewModel.kt:538-556`** — the SSE event dispatcher's `when (event.type)` block handles exactly `EVENT_MESSAGE_DELTA`, `EVENT_MESSAGE_COMPLETE`, `EVENT_TOOL_START`, `EVENT_TOOL_RESULT`, `EVENT_CAMPAIGN_CREATED`, `EVENT_ERROR`. There is no case for `task.background.started`/`.progress`/`.complete`/`.error` or for `workflow.resume_available`. Any such event arriving over the wire is silently unhandled.
- **Negative-claim search run:** `grep -rn "workflow_resume\|resume_available\|resumeAvailable\|WorkflowResume" --include="*.kt" nornspun-client/` → zero matches anywhere in the client repo.
- **`nornspun-client/composeApp/src/androidMain/kotlin/com/nornspun/MainActivity.kt:308-320`** — the ambient-completion-signal ViewModel (built to receive real `task.background.complete` events per the D3 story background) is instead driven by:
  ```kotlin
  LaunchedEffect(nornMessageCount) {
      if (nornMessageCount > 0) {
          val lastMsg = conversationMessages.lastOrNull { it.role == "norn" }
          ambientViewModel.onBackgroundTaskComplete(
              com.nornspun.ui.viewmodel.CompletedTask(
                  taskId = "msg-$nornMessageCount",
                  title = "Norn response",
                  ...
  ```
  This fires the "ambient glow" signal on **every ordinary chat reply**, unrelated to the actual `task.background.*` SSE events the backend now emits for session-recap/adventure-ingestion background work. The signal a GM sees after this sprint is disconnected from the feature the sprint built.
- **`nornspun-backend/src/routers/chat.py:513-527`** — confirms the backend does emit a `workflow.resume_available` SSE event with a `workflow_resume_available` payload when an open workflow exists for the campaign. This is real, working backend logic with no client consumer.
- **`nornspun-client/maestro/flows/`** (current contents, `main`@`704e63c8`): `00_seed_campaign.yaml`, `app_stability_after_interaction.yaml`, `chat_send_message.yaml`, `element_interaction.yaml`, `norn-pip-tap.yaml`, `semantic_element_tap.yaml`, `smoke.yaml`, `upload-adventure-smoke.yaml` — none of the 5 flows deleted in `485059c` were ever re-added.

**Conclusion:** the sprint's two most capability-oriented stories landed as fully-functional backend features with no client integration, and the E2E artifacts that would have proven or disproven that integration were written, found fraudulent, and deleted within the same sprint — with no re-attempt.

---

## 6. AFTERMATH — Did this sprint's stories survive?

**SF2e dependent stories — 3 of 4 dropped, none built** (`.momentum/stories/index.json`):

| Story | Status |
|---|---|
| `sf2e-prompt-injection-prerequisite` (this sprint) | `done` |
| `sf2e-agent-conditional-prompt-sections` | `dropped` |
| `sf2e-pc-character-profile-templates` | `dropped` |
| `sf2e-npc-mechanics-in-agent-context` | `dropped` |
| `sf2e-creature-stat-block-model` | `backlog` (never done) |

The prerequisite wiring this sprint delivered was explicitly built to unlock those four stories (`.momentum/stories/sf2e-prompt-injection-prerequisite.md` header: *"Unlocks: sf2e-agent-conditional-prompt-sections, sf2e-pc-character-profile-templates, sf2e-npc-mechanics-in-agent-context, sf2e-creature-stat-block-model"*). None of the four ever shipped.

**Independent re-verification confirms both client gaps, ~2 months later** (`.momentum/features.json`, `last_verified: "2026-06-16"`, ASR-006-sourced):

- **`proactive-norns`** feature notes: *"Built: SSE event contract; ambient signal + inner-thoughts indicator (ambient signal MIS-TRIGGERED — fires on every Norn message on Android, needs scoping to the recap frame, ASR-006 F4)."* — independently rediscovers the exact defect documented in §5 above, over two months later, still unfixed.
- **`system-aware`** feature notes: *"Infra done (sf2e-scoping-spike + sf2e-prompt-injection-prerequisite: campaign_system var, conditional key, placeholder blocks in all 3 Norn prompts) but ZERO SF2e content written → acceptance condition UNMET."* Status: `partial`, 2 of 5 stories done.
- **`session-prep`** feature notes: *"workflow-resilience genuinely done; verdandi agent backend present. Client has ZERO prep rendering (SurfaceType enum intentionally empty)."* Status: `partial`, 2 of 3 stories done, but the note explicitly flags the prior "working 3/3" claim as **FALSE** (`when-last-our-heroes-met-session-recap-generation`, the story that actually generates recap content, is `status: draft` with "a blank dev record — not done").

**SilenceToggle removal (SDR-005, amended 2026-06-09):** the ViewModel-consolidation work this sprint moved (`SilenceViewModel`, `AppPrefs`) was, within the same sprint, entangled with the UI's SilenceToggle being permanently rejected as a feature the product owner "never wanted to see again." The amendment records `SilenceViewModel` as still-live (drives ambient-glow suppression) but `SilenceToggle.kt` as dead code pending a cleanup story. Net effect: part of this sprint's one "fully delivered" refactor consolidated code paths for a UI element that was simultaneously ruled out.

**Upstream handoff:** 14 of 18 priority action items from this sprint's retro were routed to the Momentum practice project as a batch handoff (`upstream-momentum-findings.md`) rather than as nornspun stories — meaning most of what this retro found actionable was about the *practice tooling*, not the *product*, and none of it addressed "wire the client to the backend events this sprint built."

---

## 7. VERDICT

**"After sprint-2026-04-12, a user could ___ which they could not do before."**

**This sentence cannot be completed.** Evaluated story by story:

- **`consolidate-shared-ui-viewmodels`** — pure internal refactor, explicitly scoped as developer-facing ("state-management bugs are fixed once"). Zero user-visible change by design.
- **`llm-cost-logging-and-usage-tracking`**, **`model-quality-evaluation-framework`** — operator/developer observability and eval tooling. Not something a GM interacts with; not attempted to be.
- **`sf2e-prompt-injection-prerequisite`** — explicitly "purely prerequisite wiring." Confirmed zero SF2e content exists 2+ months later (ASR-006); 3 of 4 stories meant to deliver the actual GM-visible content were later dropped, the 4th never built.
- **`extended-sse-event-contract-background-task-lifecycle-events`** — backend SSE emission built and tested; the client never routes these events (confirmed by direct code read, not inference). The visual signal a GM does see (ambient glow after every message) is a decoy unrelated to the feature, independently reconfirmed by a later assessment.
- **`workflow-resilience-in-flight-persistence-and-resume`** — the sprint's single most PRD-aligned story (quotes PRD success criterion "GM returns days later and picks up exactly where they left off" verbatim), and its backend is genuinely complete and AVFL-hardened. But the client has no code path for the resume offer at all (confirmed by grep across the full client history), and the E2E tests nominally proving the client behavior were fabricated and deleted the same day they were written. A GM closing the app mid-prep in the weeks after this sprint would see **no resume prompt whatsoever** — the interruption would be silently lost from their point of view, which is exactly the failure this story exists to prevent. Additionally, the underlying content this workflow protects (`when-last-our-heroes-met-session-recap-generation`) was itself never built.

**Every story in this sprint reached `done`, passed its assigned review gates, and the sprint closed clean by its own reporting — while landing zero GM-reachable capability.** This sprint is a clean, well-evidenced instance of the mission's working hypothesis: the delivery unit here was the story (and its backend-scoped AC), not the user-facing outcome the story's own header claimed to serve.

---

## Counter-evidence & falsifiability

Evidence that cuts against, or complicates, the findings above:

- **The review pipeline was not rubber-stamping.** AVFL and QA gates caught 4 real, would-have-shipped-broken backend defects (hardcoded model name, JSON/JSONB mismatch, non-functional resume ACs, missing eval baselines) and the retro states this was "the first sprint in recent memory where the 'worked well' column is larger than the 'struggled' column." The gap this dossier documents is specifically "no gate checks client-rendering," not "the gates don't work."
- **The backend work is real, not vaporware.** Every migration, repository, and endpoint claimed exists and functions as specified — verified directly in source, not merely claimed. If operator-facing cost/quality observability and durable backend workflow state are valued in their own right (as scaffolding for future client work), the sprint delivered exactly that.
- **The AC6 hedge in `extended-sse-event-contract` was an honest, explicit scope statement, not a hidden gap** — the story author wrote in the spec itself that client wiring might be a separate story. The failure is not that this was hidden; it's that no later story ever picked it up (through the current `main` as of 2026-07-08), and no sprint-level gate flagged the fork as unresolved.
- **The maestro-audit.md failure was caught, just not durably fixed.** The 76-minute add→discover→delete cycle shows the developer (not an agent) manually caught the fabricated tests same-day. That is a working human backstop — but it produced a deletion, not a real replacement, and the underlying feature gap it revealed was never re-attempted or turned into a follow-up story.
- **A GM does see something after this sprint** — the ambient glow does fire (just on the wrong trigger). It would be inaccurate to claim the sprint changed literally nothing about the visible app; it changed a visual behavior's frequency/triggering in a way disconnected from its intended purpose.

**What would prove this dossier's verdict wrong:** a client commit (any date, any branch, any repo) adding a `when(event.type)` case for `task.background.*` or `workflow.resume_available`/`workflow_resume_available`, or a UI element with a `workflow_resume_offer`-equivalent resource id, landing and surviving to `main`. The searches run above (full-repo grep, not date-scoped) found none as of `nornspun-client`@`704e63c8` (2026-07-08) — the falsifying commit would have to exist in a session or branch not reachable from `main` at that point, or as of this writing (2026-08-02) not yet merged.

---

## Open questions

- **Whether a later sprint (2026-06-18 or 2026-07-13) revisited the client-wiring gap.** This dossier's scope is sprint-2026-04-12 only. The 2026-06-16 features.json re-verification (ASR-006) postdates 04-12 by two months and still shows the gap unresolved, which is suggestive but not conclusive that 06-18 didn't touch it — that sprint's own dossier should confirm directly.
- **Whether the E2E Validator prompt-quality fix (PA-01, "in progress" per sprint-summary) was ever completed**, and if so, whether a corrected E2E pass would have caught the client-wiring gap the fabricated Maestro flows missed. This is a counterfactual this dossier cannot resolve from artifacts alone.
- **SDR-002** is referenced in `sprint-summary.md`'s Key Decisions list but no `sdr-002*` file was found in `docs/decisions/` (only `sdr-003-llm-model-selection.md` and `sdr-004-feature-value-first.md` exist for this sprint's timeframe) — could not verify its content or confirm whether it was later renamed/consolidated.
- **Exhaustive commit-by-commit history for `AmbientCompletionSignalViewModel`'s wiring** was not walked in full (only current-state grep + the April window); it is possible an intermediate branch attempted real `task.background.*` routing and was reverted (as happened with SilenceToggle), which the current-state grep alone would not surface. The current-state negative claim is solid; a "was it ever attempted and reverted" claim is not fully ruled out.
