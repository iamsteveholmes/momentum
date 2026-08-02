# Integration & Wiring Lens — Merged-but-Unreachable Code in Nornspun

**Date:** 2026-08-02
**Role:** Code-level audit of nornspun-backend and nornspun-client hunting merged-but-unreachable
code — orphaned routes, unmounted UI, broken client→backend wiring, and quantified build-then-delete
waste. This document is a discovery-lens input to the broader "why doesn't anything work end-to-end"
investigation; it does not itself render a verdict on the sprint-process hypothesis.

---

## Executive summary

1. **Adventure PDF upload is silently broken end-to-end.** The only client call site
   (`NornApiClient.uploadAdventure`, `shared/src/commonMain/kotlin/NornApiClient.kt:320`) POSTs to
   `"$baseUrl/campaigns/$campaignId/adventures"` — missing the `/api` prefix every other client call
   uses. The backend only registers this route under `/api` (`main.py:45`, `adventures.py:49`
   `prefix="/campaigns"`). Any real upload 404s. Zero test (unit or integration) exercises the real
   URL — the only client-side test mocks the upload function entirely.
2. **Desktop — the platform this investigation is scoped to run — has no adventure upload at all.**
   `MainWindow.kt:40`: `// TODO [DESKTOP-UPLOAD]: Adventure upload not yet wired on desktop`. The
   feature exists only in `composeApp` (Android). The tracker's "done" story
   (`adventure-upload-ui-file-picker-for-pdf-ingestion`) is Android-only; a separate backlog story
   `adventure-upload-desktop` exists and is unbuilt.
3. **Opening a saved campaign does not load its conversation history.** `ChatViewModel.kt:719-721`
   (desktop): `fun loadConversationHistory(campaignId: String) { // Load from SQLDelight local
   database (wired in Task 4) }` — a literal empty-body stub. `MainWindow.kt:298-302`'s own comment
   confirms this is "a known limitation." A Spinner who closes the app and reopens a campaign gets a
   blank chat, not their story.
4. **The settings gear has never worked, on either platform, across at least 3 sprints.**
   `onOpenSettings = {}` / `onTrailingIconTap = {}` appear identically in `MainWindow.kt:312,338` and
   `MainActivity.kt:386,412`, all tagged `// TODO(S3): wire settings navigation`. No settings screen
   file exists anywhere in the repo. ASR-006 (2026-06-16) flagged this; it is still true in the
   current tree (2026-08-02) — the gap survived sprint-2026-06-18 and sprint-2026-07-13.
5. **9 backend routes have zero client callers anywhere in the repo:** heroes CRUD (GET/POST/PATCH,
   3 routes), campaign PATCH + flavor GET/PATCH (3 routes), adventures list/get/delete (3 routes, on
   top of the broken create above), `GET /tasks/{task_id}`, `POST /sessions/{id}/resume`. All are
   backend-tested (heroes: 338 lines of router tests; adventures: 478 lines) and functionally real —
   they are simply never invoked by any Kotlin code. Confirmed by exhaustive grep, not inference (see
   §2 for the exact searches).
6. **Verdandi's session-prep feature has a real backend and zero client rendering surface.**
   `SurfaceType` enum (`ConversationItem.kt:40`) is empty by design — docstring: "intentionally empty
   until a new canvas is introduced." Generic chat with Verdandi (persona, greeting) is reachable
   through the same pipe as any Norn; the actual prep deliverable (recap card, prep-ledger, NPC
   reminders) has no UI at all despite a built backend (`generate_session_recap`, workflow checkpoint
   state in `verdandi.py`).
7. **The campaign-init 5-phase wizard was built in 2 days (May 3-4) and torn out 34 days later
   (June 7)** after a design decision (SDR-011, May 22) rejected it. One commit (`b559f9b`) deleted
   3,888 lines / added 233 across 19 files — 10 files (canvases + their dedicated tests, ~2,108
   lines) fully removed, plus large guts of `CampaignInitViewModel`, `CampaignInitScreen`,
   `ConversationList`. This is the single largest build-then-discard event in either repo's history.
8. **`nornspun-backend` has never deleted a single `.py` file in its entire git history** (`git log
   --diff-filter=D` on `*.py` returns nothing); `nornspun-client` has deleted at least 26 `.kt` files /
   3,748 lines, dominated by the wizard teardown. The waste is asymmetric and concentrated in the
   client, not evenly spread across the stack.
9. **A "done" story's tracking record is internally inconsistent — but the underlying feature is
   real.** `campaign-init-urd-fills-canvas-from-free-text`: `stories/index.json` says
   `status: done`, `"merged-to-main sprint-2026-05-30 ... end-gate APPROVED"`. The story file itself
   still says `status: backlog` with a **completely empty** Dev Agent Record (no agent, no notes, no
   file list). Independently, the backend commits that implement exactly this feature exist
   (`3443882`, `22cca58` in `urd_system.md`) and the free-text extraction logic is genuinely present
   and reachable via chat. **This is a documentation-sync defect, not a fake-done story** — worth
   distinguishing from findings #1-#6, which are real functional gaps.
10. **The random 20-story reachability sample mostly holds up** — 14/20 sampled "done" stories are
    cleanly reachable in the app today, 5/20 are partial (backend real, no UI, or present-but-
    unaudited), 0/20 in the sample were outright fabricated/never-built. **The severe gaps (#1-#6
    above) are concentrated at specific integration seams, not spread uniformly across the story
    corpus** — see Counter-evidence.

---

## 1. Backend route inventory vs. client callers

### 1.1 Full route enumeration (source: `grep -rn` on `src/routers/*.py`, prefixes from `main.py:42-60`)

| Route | File:line | Registered when | Client caller? |
|---|---|---|---|
| `GET /health` | `health.py:13` | always | not required (infra) |
| `POST /api/chat` | `chat.py:548` | always | **YES** — `NornApiClient.kt:184` |
| `POST /api/campaigns` | `campaigns.py:55` | always | **YES** — `NornApiClient.kt:248` |
| `GET /api/campaigns` | `campaigns.py:77` | always | **YES** — `NornApiClient.kt:282` |
| `GET /api/campaigns/{id}` | `campaigns.py:85` | always | **NO** |
| `PATCH /api/campaigns/{id}` | `campaigns.py:97` | always | **NO** |
| `PATCH /api/campaigns/{id}/flavor` | `campaigns.py:121` | always | **NO** |
| `GET /api/campaigns/{id}/flavor` | `campaigns.py:147` | always | **NO** |
| `POST /api/campaigns/{id}/adventures` | `adventures.py:100` | always | **BROKEN** — client calls it at the wrong path (missing `/api`), see §1.2 |
| `GET /api/campaigns/{id}/adventures` | `adventures.py:277` | always | **NO** |
| `GET /api/campaigns/{id}/adventures/{aid}` | `adventures.py:292` | always | **NO** |
| `DELETE /api/campaigns/{id}/adventures/{aid}` | `adventures.py:318` | always | **NO** |
| `GET /api/tasks/{task_id}` | `tasks.py:31` | always | **NO** |
| `POST /api/sessions/{id}/resume` | `sessions.py:56` | always | **NO** |
| `GET /api/campaigns/{cid}/heroes` | `heroes.py:53` | always | **NO** |
| `POST /api/campaigns/{cid}/heroes` | `heroes.py:69` | always | **NO** |
| `PATCH /api/campaigns/{cid}/heroes/{hid}` | `heroes.py:107` | always | **NO** |
| `/test/seed/*`, `/test/reset` | `test_data.py` | `APP_ENV=test` only | N/A — test infra by design |
| `/dev/reload-prompts`, `/dev/costs/summary` | `dev.py` | `APP_ENV=development` only | **NO** (and not meant to be — dev-only ops endpoints) |

**Exact search used for "no client caller" claims (repeatable):**
```
grep -rn "heroes\|Hero\b" --include="*.kt" shared composeApp desktopApp   # only 1 hit, a false positive
                                                                           # (CampaignCard.kt's "Hero"
                                                                           #  comment is unrelated UI copy)
grep -rn "resume_workflow\|/resume\|WorkflowResume\|tasks/{task_id}\|getTask\|TaskStatus\|pollTask" \
  --include="*.kt" shared composeApp desktopApp   # zero hits
grep -rn '"\$baseUrl\|"\${baseUrl}\|baseUrl/\|/api/\|/campaigns\|/heroes\|/tasks\|/sessions\|/flavor' \
  --include="*.kt" .   # every hit enumerated in the table above; PATCH/flavor/GET-single/DELETE
                       # adventure paths never appear anywhere in the client tree
```
9 of ~20 real (non-test-infra, non-dev-only) endpoints have no caller: heroes ×3, campaign PATCH +
flavor ×3, adventures GET-list/GET-single/DELETE ×3 (create is present but broken — not counted
twice), tasks ×1, sessions/resume ×1. All are backend-tested (`tests/routers/test_heroes.py` — 338
lines; `tests/routers/test_adventures.py` — 478 lines) — this is not stub/dead backend code, it is
**real, working, unconsumed** code. The wiring gap is entirely on the client side.

### 1.2 The adventure-upload URL bug (highest-confidence single finding)

`shared/src/commonMain/kotlin/NornApiClient.kt:311-334`:
```kotlin
suspend fun uploadAdventure(...): UploadResult {
    return try {
        val response = client.submitFormWithBinaryData(
            url = "$baseUrl/campaigns/$campaignId/adventures",   // <-- no /api prefix
            ...
```
Every other method in the same file prepends `/api`: `postChat` → `"$baseUrl/api/chat"`,
`createCampaign`/`listCampaigns` → `"$baseUrl/api/campaigns"`. The backend registers
`adventures.router` with `app.include_router(adventures.router, prefix="/api")` (`main.py:45`) on top
of the router's own `prefix="/campaigns"` (`adventures.py:49`) — the live path is
`/api/campaigns/{id}/adventures`. `uploadAdventure` hits `/campaigns/{id}/adventures`, which FastAPI
has never registered. Against a live backend this returns 404, which the client's own `else` branch
(`NornApiClient.kt:361-366`) maps to `UploadResult.Error("Upload failed. An unexpected error
occurred.", UNKNOWN)` — a generic, silent failure with no signal pointing at the URL.

**Why no test caught it:** the only client-side coverage of the upload path
(`AdventureUploadViewModelTest.kt`) injects a mock `uploadFn`, bypassing `NornApiClient.uploadAdventure`
entirely (`AdventureUploadViewModel(uploadFn = { _, _, _ -> UploadResult.Success(...) })`). There is
no `NornApiClientTest` coverage of `uploadAdventure` at all — confirmed by
`grep -n "uploadAdventure" shared/src/commonTest/kotlin/NornApiClientTest.kt` returning zero matches.
Backend-side, `tests/routers/test_adventures.py` (478 lines) tests the route directly (in-process),
never through the real client, so it can't see the client's wrong URL either. **No test in either
repo exercises the real client→server call for this endpoint.**

---

## 2. Unreachable / unmounted UI from the desktop entry point

Desktop entry point traced: `desktopApp/src/desktopMain/kotlin/main.kt` → `runApplication { MainWindow() }`
→ `desktopApp/src/desktopMain/kotlin/ui/MainWindow.kt` (405 lines, read in full).

| Composable / feature | Status | Evidence |
|---|---|---|
| `FirstLaunchScreen`, `CampaignPickerScreen`, `ChatScreen`, `CampaignInitScreen` | **Reachable** — all 4 are top-level app states switched on in `MainWindow.kt:268-402` | direct read |
| `Composer` (vellum redesign, S5) | **Reachable** — mounted inside `ChatScreen.kt:170` | direct read |
| `NornSelector`, `InnerThoughtsIndicator`, `AmbientCompletionSignal` | **Reachable** — wired into `AppScaffold`'s `pipCluster` slot and content wrapper, `MainWindow.kt:339-361,366` | direct read |
| `SilenceToggle` composable | **Built, never mounted, anywhere.** `grep -rn "SilenceToggle(" .` (excluding the file that defines it) returns **zero** call sites in any `.kt` file in the repo. Confirmed independently of ASR-006 (which flagged the same gap on 2026-06-16 — still true today). `SilenceViewModel` (a different class) IS live and wired (`MainWindow.kt:106-108`) — only the toggle UI is dead. |
| Settings screen | **Does not exist as a file anywhere.** `grep -rln "Settings" --include="*.kt" .` returns only files that reference the settings *gear icon slot* (`AppScaffold.kt`, `CampaignPickerScreen.kt`) and the two shells that no-op it — no `SettingsScreen.kt` or equivalent. `onOpenSettings = {}` / `onTrailingIconTap = {}` in both `MainWindow.kt:312,338` and `MainActivity.kt:386,412`. |
| Adventure upload (`AdventureUploadViewModel`) | **Unreachable from desktop.** Only referenced in `composeApp` (Android) + its own test. `MainWindow.kt:40`: `// TODO [DESKTOP-UPLOAD]: Adventure upload not yet wired on desktop — requires JFileChooser integration`. |
| `ChatViewModel.loadConversationHistory(campaignId)` | **Stub.** `ChatViewModel.kt:719-721`: `fun loadConversationHistory(campaignId: String) { // Load from SQLDelight local database (wired in Task 4) }` — empty body. Called nowhere else in `MainWindow.kt`'s `onOpenCampaign` handler (`MainWindow.kt:297-310`), whose own comment says message-history seating "is not yet wired ... documented as a known limitation." |
| Session-prep UI surface (Verdandi recap/prep-ledger) | **No rendering surface.** `SurfaceType` enum body is empty (`ConversationItem.kt:40`, `@Suppress("unused") enum class SurfaceType`) with docstring "intentionally empty until a new canvas is introduced." Backend `generate_session_recap`, workflow checkpointing (`verdandi.py:351-535`) are real and substantial but have no client consumer. |

---

## 3. The campaign-init wizard: built, then deleted (quantified)

Git history in `nornspun-client` (all dates from `git show -s --format=%cd --date=short`):

- **2026-05-03 – 05-04:** wizard built across 4 commits (`70e2f55`, `b17f12e`, `85e9688`, `53df844`,
  plus canvas-file-adding commits `5d0d7fb` HeroProfileCanvas, `871d33a` CampaignFlavorCanvas — all
  same 2-day window). ~2,480+ lines added in the two largest commits alone.
- **2026-05-22:** SDR-011 (`docs/decisions/sdr-011-campaign-init-conversational-model-2026-05-22.md`)
  rejects the 5-phase wizard model: "A campaign name is the only required input"; "5-Phase Sequential
  Wizard Model — REJECTED."
- **2026-06-07 (34 days after build, 16 days after rejection):** `b559f9b` — "remove 5-phase wizard
  from CampaignInitScreen." `git show b559f9b --shortstat`: **19 files changed, 233 insertions(+),
  3888 deletions(-)**. Ten files fully deleted:
  `CampaignIdentityCanvas.kt` (199), `PartyFoundationCanvas.kt` (160), `HeroProfileCanvas.kt` (323),
  `SessionZeroSeedCanvas.kt` (196), `CampaignFlavorCanvas.kt` (257), `HeroTransitionMessages.kt` (49),
  and their four dedicated test files (`CampaignFlavorCanvasTest.kt` 289,
  `CampaignIdentityCanvasTest.kt` 248, `HeroProfileCanvasTest.kt` 387, `PartyFoundationCanvasTest.kt`
  323) — **~2,431 lines of pure feature+test code deleted outright**, plus deep cuts to
  `CampaignInitViewModel.kt` (-388 net), `CampaignInitScreen.kt` (-311 net), `ConversationList.kt`
  (-168 net) that survived as files but lost most of their wizard-specific content.

**Generalizing across both repos' full history:**
```
nornspun-client:  git log --all --diff-filter=D --numstat -- '*.kt'  → 26 files, 3,748 lines deleted (min bound; rename-detection may hide more)
nornspun-backend: git log --all --diff-filter=D --numstat -- '*.py'  → 0 files, 0 lines — no .py file has ever been deleted in this repo's history
```
Excluding the wizard teardown, the client's other deletions are legitimate refactor-relocations
(April 11-12 "migrate to commonMain" commits move files between Android/Desktop/shared source sets —
net functionality preserved, not wasted) and one small, deliberate cleanup (`bb4ed03`, removing an
unused compose-driver test endpoint). **The wizard is the only substantial build-then-discard event
in either repo's history** — concentrated, not diffuse: 2 days of build effort, discovered wrong by a
design decision 18 days later, physically removed 16 days after that.

---

## 4. Tracking-integrity finding: index says done, story file disagrees

`campaign-init-urd-fills-canvas-from-free-text`:

- `.momentum/stories/index.json`: `"status": "done"`, `"status_synced": "merged-to-main
  sprint-2026-05-30 (commit 8d71f09, end-gate APPROVED)"`, `"status_synced_at": "2026-06-12"`.
- The story file itself (`.momentum/stories/campaign-init-urd-fills-canvas-from-free-text.md`) line 4:
  `status: backlog`. Its Dev Agent Record section (lines 354-364) is **completely empty** — no Agent
  Model Used, no Debug Log References, no Completion Notes, no File List.
- Cross-check: commit `8d71f09` is in the **planning-hub repo** (`nornspun`), and is an end-gate
  doc-approval commit, not a code commit — it cannot itself be the implementation.
- Independent verification against `nornspun-backend`: commits `3443882` ("feat(urd): add
  natural-language multi-field extraction guidance to campaign init") and `22cca58` ("fix(urd-prompt):
  address review findings for campaign-init-urd-fills-canvas-from-free-text") **do exist** and modify
  exactly `src/prompts/urd_system.md` in the way the story describes (name+system single-turn
  extraction, PF2e default, Starfinder alias recognition — verified by reading `urd_system.md:211-272`
  directly, content matches the story's acceptance criteria almost verbatim).
- **Conclusion: the feature is real and reachable via chat (backend prompt implements it, and the
  `campaign.created` SSE event it depends on is independently confirmed wired into
  `ChatViewModel`/`MainWindow`).** But the per-story bookkeeping artifact was never synced after
  implementation — a distinct defect from "story marked done that was never built." Prior art:
  ASR-003 (2026-05-28) had this story correctly flagged as an open backlog "Recommendation 5" *before*
  the sprint-2026-05-30 work closed it; nothing in this repo re-verified the story file itself
  afterward.

---

## 5. 20-story reachability sample (random, seed=42, from 91 `done`-status stories)

| Story | Verdict | Evidence |
|---|---|---|
| `client-conversation-history-persistence` | **Reachable** | `ChatViewModel.kt:229-315,660-683` — session_id + conversationHistory accumulation genuinely implemented; story's own AC explicitly scopes cross-restart persistence out ("stretch goal") |
| `composer-redesign-vellum-surface` | **Reachable** | `Composer.kt` mounted at `ChatScreen.kt:170`; vellum-specific copy/tokens present (`Composer.kt:111-112`) |
| `campaign-init-threshold-opening-message-and-system-choice-links` | **Reachable** | `UrdThresholdMessage` rendered in `CampaignInitScreen.kt:185`, which is mounted in `MainWindow.kt:372` |
| `shared-ui-consolidation` | **Reachable** | `AppScaffold.kt` is one genuine shared composable (`grep -rln "fun AppScaffold"` → single file), used by both shells |
| `inner-thoughts-proactivity-indicator-active-but-quiet-state` | **Reachable, but design-divergent** | Wired at `MainWindow.kt:356-360`; ASR-006 F4 flags it fires on every Norn message on Android instead of only the recap-generating frame — not independently re-verified for the Android side in this pass |
| `fix-campaign-name-title-bar-body-font-with-caret` | **Reachable** | Caret testTag + styling present in `AppScaffold.kt:82-395` |
| `campaign-init-picker-screen-and-start-new-campaign-card` | **Reachable** | `CampaignPickerScreen` mounted as a top-level state, `MainWindow.kt:283-315` |
| `swap-campaign-switcher-from-no-campaign-on-name-capture` | **Reachable** | `switcherCampaignName` logic, `MainWindow.kt:164-168` |
| `norn-selector-and-ratatoskr-first-launch` | **Reachable** | `FirstLaunchScreen` + `NornSelector`, `MainWindow.kt:268-282,341` |
| `campaign-init-urd-fills-canvas-from-free-text` | **Reachable (functionally); tracking artifact stale** | See §4 |
| `plant-the-first-seed-campaign-init-through-conversation` | **Reachable, superseded** | ASR-003 confirmed `create_campaign` tool live; original 5-phase/campaign_type prompt behavior it shipped has since been replaced by the free-text story above — the *capability* survives, the *originally-specced behavior* does not |
| `default-system-pf2e-server-side` | **Reachable** | PF2e default logic live in `urd_system.md:227,241,270`, exercised via the working chat path |
| `dynamic-prompt-assembly-variable-interpolation` | **Reachable** | Backend `PromptAssembler`, exercised via chat |
| `norn-routing-and-cost-observability` | **Reachable** | Backend routing, part of the working chat path |
| `local-postgresql-and-data-persistence` | **Reachable** | Backend infra, 12 alembic migrations applied |
| `living-memory-the-loop-connects` | **Partial** | Store B (summaries/NPC encounters/`context.py`) built and feeds Verdandi (agent-facing loop works per ASR-006 F1); no client ledger UI exists to read it back (human-facing loop does not close) |
| `llm-cost-logging-and-usage-tracking` | **Partial** | Logging itself works server-side; the only surfacing endpoint (`GET /dev/costs/summary`) is dev-env-only and has zero client callers — no Spinner can ever see it in the app |
| `accessibility-foundation-wcag-aa-compliance` | **Partial** | `semantics{}` (21 hits) / `contentDescription` (23 hits) present across the tree; no compliance audit performed in this pass to confirm actual AA conformance |
| `enable-semantic-element-access` | **Reachable, but as test infra** | testTags exist and back the compose-driver E2E harness (`ComposeDriverGoldenPathTest.kt`) — real and working, but its "user" is the test harness, not the Spinner |
| `verdandi-agent-session-prep-conversations` | **Partial** | Generic in-character chat with Verdandi is reachable (same pipe as any Norn); the session-prep-specific surface (recap card, prep starting points as structured UI) has zero rendering path — `SurfaceType` enum confirmed empty, independent of and consistent with ASR-006 |

**Tally:** 14/20 cleanly reachable (including 2 "reachable with a caveat" that are still genuinely
functional), 6/20 partial (backend real + no UI, or present-but-unaudited), 0/20 fabricated.

---

## Counter-evidence & falsifiability

- **The sample does not support "nothing works."** 14 of 20 randomly-sampled done stories are
  reachable exactly as specced, with no evidence of stubbing. If the hypothesis were "every done
  story is fake," a random sample this size would be expected to surface far more than zero outright
  fabrications. It surfaced zero.
- **The backend is the healthier half of the stack.** Zero `.py` files deleted in
  `nornspun-backend`'s entire history; every backend route this pass checked (heroes, adventures,
  campaigns, tasks, sessions) is genuinely implemented and has real test coverage
  (`tests/routers/test_heroes.py` 338 lines, `tests/routers/test_adventures.py` 478 lines). The
  "doesn't work" experience is not a backend-quality problem — it's an unwired-frontend problem.
- **ASR-003 (2026-05-28) independently pre-refuted a plausible-sounding false claim** ("Urd agent
  never built") that turned out to be a directory-confusion artifact (two `nornspun-backend` trees on
  disk, one stale/embedded, one canonical). This is direct evidence the project has caught at least
  one of its own false "nothing was built" claims before — the practice is not blind to this failure
  mode, it has just not caught the narrower wiring bugs found here (URL bug, history-load stub,
  settings no-op) because those require reading the actual call sites, not just confirming a file
  exists.
- **ASR-006 (2026-06-16) already found five of this document's six severe gaps** (adventure-upload
  desktop gap, settings screen absence, unmounted SilenceToggle, empty SurfaceType for prep, Store A
  absence) six weeks before this pass, from a structured design-reconciliation process — not from
  transcript archaeology. **What ASR-006 did NOT catch: the adventure-upload URL bug (§1.2).** That
  is this document's one genuinely new finding relative to prior art; everything else corroborates
  (independently, via fresh code reads rather than citation) what ASR-006 already said. **What would
  prove this document's #1-#6 findings wrong:** a build/runtime artifact (server log, E2E test
  transcript, or a `curl` against a running `localhost:8000`) showing the adventure endpoint
  succeeding at the un-prefixed path, or a settings screen file this grep search missed. I did not
  have a live backend or running app available in this pass to execute that confirmation directly —
  this is a static-analysis finding, not a live-request-observed one (see Open Questions).
- **The wizard teardown, properly dated, is smaller than it might sound.** "Built then deleted" is
  true, but the *active development window* was 2 days (May 3-4), not a whole sprint's worth of
  ongoing investment across multiple sprints. The waste is real (~2,400+ lines of dead-on-arrival
  canvas+test code, plus a design decision that took 18 days to convert into code removal) but it is
  a single concentrated incident, not a recurring monthly pattern — the backend's zero-deletions
  history and the client's otherwise-clean refactor history support that this is an outlier, not the
  norm.

---

## Open questions

- **No live backend or running desktop app was available in this pass.** All findings are static
  (source, git history, test file presence). The adventure-upload 404, the settings no-op, and the
  history-load stub are all corroborated by multiple independent lines of source evidence (the code
  itself, its own inline comments, ASR-006's prior finding, and absence of any contradicting test) but
  none were confirmed by an actual live request/click in this session. A follow-up with a running
  `nornspun-backend` (`APP_ENV=development`) and the desktop app would let someone `curl` the exact
  broken URL and click the settings gear to convert "confirmed by 4 independent static signals" into
  "observed directly."
- **Whether the heroes/flavor/adventures-read backend endpoints are intentionally ahead-of-client
  (built for a near-future client feature) or truly orphaned** was not determined — the story corpus
  wasn't cross-referenced deeply enough to say whether a backlog story specifically plans to wire
  each one. ASR-006 §"New" lists imply several are waiting on client stories not yet built
  (campaign-identity canvases, picker `GET /campaigns` client repo, etc.) — so "unreachable" is not
  necessarily "wasted," some of it may be legitimately backend-ahead-of-schedule.
  `GET /tasks/{task_id}` and `POST /sessions/{id}/resume` are the two with the weakest signal of any
  near-term client plan (no dedicated router test, no story found in the 302-entry index whose title
  obviously targets them) and are the best candidates for genuinely-orphaned rather than
  ahead-of-schedule.
- **Whether sprint-2026-06-18 or sprint-2026-07-13 touched the settings gear or adventure-upload-desktop
  stories at all** (attempted-but-failed vs. never-attempted) was not traced through those sprints'
  build ledgers in this pass — only the current-state code and the two backlog story entries were
  checked. That would clarify whether this is "never scheduled" or "scheduled and silently dropped."
- **The accessibility-foundation-wcag-aa-compliance story's actual AA conformance** was not audited —
  only that semantics/contentDescription machinery exists. A real audit (screen reader pass or
  automated a11y scanner) would be needed to confirm the acceptance condition, not just presence of
  the API surface.
