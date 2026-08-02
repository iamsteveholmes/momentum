# Nornspun Ground Truth — What the Product Can Actually Do Today

**Date:** 2026-08-02
**Role:** Empirical "ground truth" discovery agent — built, ran, and probed the real backend, database, and desktop client to establish the product's actual runtime state, independent of story/sprint records.

---

## Executive summary

1. **The entire sprint-2026-07-13 output is unmerged.** 26 backend commits and 27 client commits sit on `sprint/sprint-2026-07-13` branches in `.conduct-wt` worktrees; `main` in both repos contains none of it. All 12 sprint stories are status `review`; the sprint is still `active`/locked. If the developer launched the app from `main`, they were running **pre-sprint** code.
2. **The backend on `main` works far better than the "nothing works" framing suggests.** Verified live: health, campaign list/create, SSE chat with both Urd and Verdandi, conversational campaign creation (`campaign.created` event + DB row), session-capture binding (session row written), Verdandi session prep that reads real living-memory events, and the full adventure loop (PDF upload → ingestion → chunking → tool search → Verdandi citing "Ser Marrow" by name from the PDF).
3. **The developer's own dev database is almost empty after ~4 months of development**: 2 campaigns, 1 session (seeded during sprint E2E on Jul 22), 0 heroes, 0 adventures, 0 recaps, 0 NPC encounters, 0 divergences, 0 episodes, 0 transcript turns. The product has essentially never been used for real play.
4. **The desktop client on `main` builds clean, launches, renders a working chat workspace, and its production ChatViewModel completes a live chat round-trip in ~2s** (verified by driving the real class against the live backend). "The app is broken" is not literally true at the chat-loop level.
5. **The documented desktop E2E path has never worked in the repo's entire history.** `COMPOSE_UI_TEST_SERVER_ENABLED=true ./gradlew :desktopApp:run` (docs/acceptance-testing-runbook.md:43) crashes with `NoClassDefFoundError` on **both** `main` and the sprint branch, because `ui-test-junit4` has been test-classpath-only since the initial client commit (`cebf6b6`).
6. **The "golden path E2E" test doesn't test the app** — it drives a synthetic 3-widget composition — **and it never runs**: it is a JUnit4 class under `useJUnitPlatform()` with no vintage engine, which the repo's own KDoc admits silently discovers zero JUnit4 tests.
7. **Session capture has a real integrity defect on `main`**: the capture staging buffer is per-HTTP-request; in a two-call capture-then-bind sequence without resent history, Urd wrote a session with **0 events and a fabricated summary** while confidently announcing *"It is bound."*
8. **What a user genuinely cannot do today on desktop `main`**: upload an adventure (UI is a TODO), see any session history/recap/prep surface (no UI, no GET endpoint), see real session counts (`sessionCount = 0` hardcoded), talk to Skuld (disabled both ends), or trust that a capture actually persisted what they said.
9. **The dev runtime is rotted**: `README.md` is empty (zero documented startup), Docker Desktop is broken on the machine (backend exits status 150), and the real container runtime is `finch` with containers created 4 months ago — the pgvector DB container held the only living state.
10. **The Norns run on `openrouter:tencent/hy3-preview`** (a ~$0.06/M-token model, per SDR-003 revision 2026-07-07), not Claude, and SSE replies arrive as **one single `message.delta`** — no incremental streaming.

---

## 1. Versions and branches tested

| Repo | Branch tested | HEAD |
|---|---|---|
| nornspun-backend | `main` | `ab2e5794271dba0134ed96a2062df5831e2b8596` |
| nornspun-client | `main` | `704e63c8dccf7c183bbb1a0b8476490a4339d249` |
| backend sprint worktree | `sprint/sprint-2026-07-13` at `/Users/steve/projects/.conduct-wt/nornspun-backend/INTEGRATION` | `b6a72b0` |
| client sprint worktree | `sprint/sprint-2026-07-13` at `/Users/steve/projects/.conduct-wt/nornspun-client/INTEGRATION` | `2e4e721` |

**Unmerged sprint work (OBSERVED):**
- Backend: `git log --oneline main..sprint/sprint-2026-07-13 | wc -l` → **26 commits** (episodes/transcript persistence, session naming, episode-close summarization, session-counter, exchange-id rename, campaign-name injection…). `main` is 1 commit ahead of the sprint branch (divergence).
- Client: same comparison → **27 commits** (campaign picker GET /campaigns repo, kotest migration, greeting trim, FlowRow fix, foreground tracking, 3 `fix(endgate)` capture-integrity commits…). `main` is 0 ahead — the sprint branch strictly contains main.
- Planning state (`/Users/steve/projects/nornspun/.momentum/stories/index.json`): status counts `{backlog: 150, done: 91, dropped: 28, obsolete: 19, review: 12, parked: 2}`. The 12 `review` stories are exactly the 12 sprint-2026-07-13 stories. `/Users/steve/projects/nornspun/.momentum/sprints/index.json` still shows the sprint `"active", "locked": true`.

**Consequence:** the sprint's end-gate approval did not result in a merge to `main`. Any launch of the app from the main checkouts (`/Users/steve/projects/nornspun-client`, `/Users/steve/projects/nornspun-backend`) runs pre-sprint code. Everything in sections 3–6 below was tested on `main` unless stated.

---

## 2. Environment: how the product actually gets run (and what's broken)

- **`nornspun-backend/README.md` is empty** (0 bytes, OBSERVED via Read). There is no documented way to start the product. `docker-compose.yml` defines a `pgvector/pgvector:pg17` db + an api container.
- **Docker Desktop is broken on this machine.** Three launch attempts: `open -a Docker` starts `com.docker.backend`, which logs `returning error: unmarshaling start request: unexpected EOF` and `monitor exited: exit status 150` (`~/Library/Containers/com.docker.docker/Data/log/host/com.docker.backend.log`), then all processes exit. The docker socket never appears. **Environment failure — documented, not fought further.**
- **The real runtime is finch** (`brew list` shows `finch`; no postgres, no colima/podman). `finch ps -a` shows both nornspun containers **created 4 months ago**: `nornspun-backend-api-1` (status Created — apparently never/rarely run) and `nornspun-backend-db-1` (pgvector, holds the persistent volume `nornspun-backend_postgres_data`). I started the finch VM + db container, ran the API on the host via `uv run uvicorn src.main:app` (Python 3.14.3, started clean, prompts loaded, `app_env: development`).
- Backend `.env` provides `DATABASE_URL=postgresql+asyncpg://nornspun:nornspun@localhost:5432/nornspun_dev`, an Anthropic key, and an OpenRouter key.

---

## 3. Database ground truth (the developer's actual data)

Schema at Alembic head `015` — i.e. **the DB was migrated by the sprint branch** (migrations 013–016 exist only there; main tops out at 012). Sprint tables `episodes` and `transcript_turns` exist. This confirms the sprint-branch backend ran against this DB at some point (consistent with E2E on Jul 20–22).

Contents on 2026-08-02, before my probes (OBSERVED via psql):

| Table | Rows | Notes |
|---|---|---|
| campaigns | 2 | "The Salt Road" (2026-06-12), "Ashen Vale" (2026-07-07) |
| sessions | 1 | session_number **0**, date 2024-01-15, created **2026-07-22 22:45** (sprint E2E window), rich Chapter-One summary + 5-PC party snapshot — seeded, not real play |
| session_events | 59 | all attached to that one seeded session |
| heroes | 0 | **no PC profile has ever been persisted** |
| adventures / content_chunks | 0 / 0 | **no adventure has ever been ingested** (two orphaned adventure dirs from April exist on disk under `data/storage/adventures/` for campaign UUIDs that are no longer in the DB) |
| recaps | 0 | no recap ever bound |
| npc_encounters / session_divergences | 0 / 0 | capture has never persisted an NPC update or divergence |
| episodes / transcript_turns | 0 / 0 | sprint Store-A/episode model: tables exist, never used |
| llm_usage_logs | 105 (incl. ~9 from my probes) | cost tracking is real |

**INFERRED:** after ~4 months and 91 "done" stories, the data layer shows a product that has never accumulated real user data. The "living memory moat" contains one seeded session.

---

## 4. Backend probes on `main` — request → response

Full route table (OBSERVED via `GET /openapi.json`): campaigns CRUD+flavor, heroes GET/POST/PATCH, adventures POST/GET/GET-one/DELETE, `POST /api/chat`, `POST /api/sessions/{id}/resume`, `GET /api/tasks/{id}`, `/dev/costs/summary`, `/dev/reload-prompts`, `/health`. **There is no session-history list, no recap GET, no episode list endpoint on `main`** (search: full route dump above; the sessions router defines only `/resume`). The sprint branch adds **zero** new endpoints (`git diff main sprint/sprint-2026-07-13 -- src/routers/` → only chat.py internals changed).

| Probe | Result |
|---|---|
| `GET /health` | `{"status":"ok","database":"connected"}` HTTP 200 in 0.028s |
| `GET /api/campaigns` | 200; both real campaigns returned |
| `POST /api/campaigns` | 201; row created (probe row deleted afterwards) |
| `POST /api/chat` (urd, "say ready") | SSE `message.delta` with in-character prose + `message.complete` `{"usage": {"input_tokens": 8381, "output_tokens": 31}, "cost": 0.000564}` |
| Urd capture turn ("record: party defeated the Bandit King, Sister Mercy wounded") | 200; 17,148 input tokens, 560 out; **no `tool.start`/`tool.result` SSE events surfaced** |
| Urd bind turn ("Yes, bind it", same session_id, **no history resent**) | Urd replied *"It is bound, Spinner. Session 1 of The Salt Road…"* — a session row **was** created, **but with 0 events and a fabricated summary** ("the party traveled the Salt Road, encountering the salt flats…" — none of which I said). See §7. |
| Verdandi prep ("what happened last time / what should I prep?") | Long in-character reply that **correctly read living memory**: cited "session zero" foundation, and real open threads from the 59 seeded events — "Jafar's secret", "the Salt Citadel", "The Salt Lord was defeated but not destroyed". The read path works. |
| Adventure upload (valid 1-page PDF) | 201, status `ready`, 1 content chunk in DB |
| Verdandi retrieval from that PDF | Correctly answered "the ghoul-knight **Ser Marrow** guards the entrance to the crypt beneath Karn Hill" — upload → ingest → ILIKE search → cited answer works end-to-end |
| Anti-hallucination check | With a (my error) truncated PDF, Verdandi searched, found nothing, and **refused to invent**: "I won't fill that gap with invention." Honest-empty behavior works. |
| Conversational campaign creation (urd, campaign_id null) | SSE stream contained `event: campaign.created`; row "GROUND TRUTH PROBE CAMPAIGN"/PF2e appeared in DB (deleted afterwards) |
| `GET /dev/costs/summary` | 200; per-agent/per-model rollup; all 9 probe calls on `openrouter:tencent/hy3-preview`, total $0.0094 |

**Notable runtime characteristics (OBSERVED):**
- All Norn traffic routes to `openrouter:tencent/hy3-preview` (config: `src/core/config.py:76-80`, "both Norn agents via OpenRouter — SDR-003 revision 2026-07-07"). The Anthropic key in `.env` is unused by chat.
- Every SSE reply arrived as **a single `message.delta`** carrying the whole message, then `message.complete`. There is no token-level streaming in practice — a user watches a blank state for the full generation (1–11s in my probes), then the entire reply appears.
- Skuld: `NORN_REGISTRY` has urd + verdandi; skuld is commented out ("uncomment when D7 implements skuld", `src/routers/chat.py:64-68`) and returns a graceful "not available" stream.

---

## 5. Desktop client on `main` — build, launch, render, interact

- `./gradlew :desktopApp:build -x test` → **BUILD SUCCESSFUL in 27s**.
- `./gradlew :desktopApp:run` (backend up) → window "Nornspun" launched (verified via System Events window list + full-screen screenshot). Rendered: campaign switcher "The Salt Road ›", Norn pips (U active; V available; S dashed/disabled), Urd's greeting **with the untrimmed capability menu** ("Session recap / NPC history / Campaign timeline / What happened with…" — the sprint story `norn-greeting-capability-menu-trim` that trims unbacked bullets is unmerged), composer with per-Norn placeholder and SEND. No startup crash, no stacktrace in logs.
- **Direct UI interaction was blocked by the environment** (osascript: "not allowed assistive access"; no cliclick). Two workarounds executed:
  1. **Compose-test probe of the real `MainWindow()`** (injected via Gradle init-script from scratchpad; no repo edits): typing into `composer_text_field` and clicking `composer_send_button` **did** dispatch a real `POST /api/chat` — backend log shows the request for campaign The Salt Road and `llm_call_complete` (25 tokens, 1,079ms) — but the reply never rendered within 90s under the test clock (message count stayed at user+greeting).
  2. **Production `ChatViewModel` probe, no Compose harness** (real Swing EDT `Dispatchers.Main`): `sendMessage(...)` → **`StreamingState.Complete` at t=2s** with reply "I am the Weavekeeper, the chronicler who records your campaign's threads into living memory." — the full client networking/SSE/state pipeline works.
- **INFERRED:** the UI-probe non-render was a compose-ui-test virtual-clock artifact (real-thread → `Dispatchers.Main` hops don't pump under `waitUntil`), not a product bug. The convergent evidence (visual render of greeting + working ViewModel + backend receiving the UI's real click-dispatched request) says the desktop chat loop works live.
- Desktop campaign picker on `main` **is** backed by real data (`AppStateViewModel.kt:146` calls `NornApiClient.listCampaigns`) — but **every campaign card shows "0 sessions": `sessionCount = 0` hardcoded at `shared/src/commonMain/.../CampaignPickerScreen.kt:87`** (the fix is the unmerged sprint story `session-counter-live-update-on-capture-close`).
- Desktop adventure upload: **absent** — `desktopApp/src/desktopMain/kotlin/ui/MainWindow.kt:40`: `// TODO [DESKTop-UPLOAD]: Adventure upload not yet wired on desktop — requires JFileChooser integration`.
- Android: upload UI code exists (`composeApp/src/androidMain/.../AdventureUploadViewModel.kt`, `MainActivity.kt` ActivityResult wiring; maestro flow `upload-adventure-smoke.yaml`). **Not runtime-tested** (no emulator run in this discovery).

---

## 6. E2E infrastructure ground truth — the tooling that was supposed to catch all this

1. **The documented desktop E2E launch has never worked.** `docs/acceptance-testing-runbook.md:43` documents `COMPOSE_UI_TEST_SERVER_ENABLED=true ./gradlew :desktopApp:run`. Executed on `main`: `NoClassDefFoundError: androidx/compose/ui/test/ComposeUiTest_skikoKt` (RunApplication.kt:45). Executed on the sprint worktree: **identical crash** (RunApplication.kt:49). Cause: `ui-test-junit4` is declared only in `desktopTest`, never in `desktopMain`, so the run classpath can't load `runComposeUiTest`. Negative-claim search: `git log --all -S "ui-test-junit4" -- desktopApp/build.gradle.kts` returns exactly one commit — the initial client commit `cebf6b6` — and at that commit the dependency is already inside the `desktopTest` block (verified via `git show cebf6b6:desktopApp/build.gradle.kts`). **The compose-driver HTTP control plane has therefore never been startable against the real app via the documented command, on any commit.**
2. **The "golden path E2E" is synthetic.** `desktopApp/src/desktopTest/kotlin/ComposeDriverGoldenPathTest.kt` builds its own throwaway composition (an `OutlinedTextField`, a `Button`, a hardcoded "Norn responded." Text) and drives that. It validates the driver library, not Nornspun.
3. **And it never executes anyway.** It is a JUnit4 `@Test` class; `desktopApp/build.gradle.kts:45` sets `useJUnitPlatform()` with no vintage engine. The repo's own `MainWindowTest.kt` KDoc states: "plain JUnit4 `@Test` classes are silently never discovered/run by Gradle (confirmed: the prior version of this file produced no `TEST-*.xml` …)". On the sprint branch the migrated Kotest version is tagged `e2e` and **excluded from the default test run** (`-PkotestTags="e2e"` required — build file comment).
4. The sprint planning record knew about the class of problem: wave-1 note in `/Users/steve/projects/nornspun/.momentum/sprints/index.json`: "desktop tests silently did not execute in sprint-2026-06-18 (missing JUnit runtime)".

**INFERRED:** whatever "E2E" the sprint end-gate consumed on desktop, it cannot have been the documented compose-driver flow against the real app. (Corroborating trace for other agents: the seeded session row and the DB migration stamp both date to Jul 22 — something ran, but the documented UI-driving path was not launchable.)

---

## 7. The capture-integrity defect (worst single finding at product level)

`src/core/dependencies.py:53` — `capture_buffer: object | None = None` lives on per-request `NornDeps`; `src/agents/urd.py:363-365` lazily creates a fresh `CaptureBuffer()` inside each request. Staged events from a capture turn are **discarded when the HTTP request ends**.

Observed two-call sequence (no client history resent — I called the API the way any thin client might):
1. Turn 1 (capture): "…the party defeated the Bandit King at the old mill, and the cleric Sister Mercy was gravely wounded. Please record these events." → 200, in-character acknowledgment.
2. Turn 2 (bind): "Yes, bind it. It is confirmed." → Urd: *"It is bound, Spinner. Session 1 of The Salt Road — the thread is caught, and the loom holds it fast."*
3. DB reality: new session row `3080c7a3…` with **0 session_events** and summary *"Session 1: The party traveled the Salt Road, encountering the salt flats and the first signs of the trade route's dangers…"* — **entirely fabricated; neither the Bandit King nor Sister Mercy appears anywhere.**

Mitigating caveat (INFERRED): the real client resends full conversation history each turn (`ChatViewModel.dispatchMessage` maps `_conversationMessages` into the request), so on a real bind turn the model *can* re-stage events from history before binding in the same request. Whether it reliably does so is unverified. The observed failure mode remains: the architecture permits a confident "It is written" receipt over an empty, fabricated bind — precisely the trust failure the binding ritual exists to prevent.

---

## 8. Feature walk — every feature in `.momentum/features.json` vs. today's reality

Verdicts: **WORKS** = acceptance condition achievable today; **PARTIAL** = some steps work, named step breaks; **ABSENT** = not achievable.

| Feature | Verdict | Exactly where it breaks (evidence) |
|---|---|---|
| **campaign-init** | PARTIAL | Works: picker with real campaigns (desktop main), "start new campaign" card, conversational create → `campaign.created` + DB row (probe §4). Breaks: full 5-phase capture unproven; **0 heroes rows ever** (§3) means no PC-with-fear has ever been persisted, so the acceptance tail ("first prep references the PC's fear") has never been reachable with real data. |
| **session-prep** | PARTIAL | Works: Verdandi prep-in-chat reads real memory and surfaces open threads (§4). Breaks: acceptance needs "2 prior captured sessions" — only 1 seeded session exists; **client has zero prep/recap rendering surface** (features.json ASR-006 note; no recap GET endpoint on main §4); prep exists only as chat prose. |
| **session-capture** | PARTIAL | Works: capture conversation runs; bind creates a session row. Breaks: per-request CaptureBuffer + fabricated-summary bind with confident receipt (§7); 0 npc_encounters and 0 divergences ever persisted (§3) — the acceptance's "NPC status changes + at least one divergence" has never been achieved in this DB. |
| **living-memory** | PARTIAL | Works: read tools (session history, unfinished business) feed Verdandi correctly (§4). Breaks: Store A/episodes empty and sprint-only (§1, §3); no ledger/history UI of any kind in the client; cross-agent value exists only inside chat replies. |
| **adventure-upload** | PARTIAL | Works fully at API level incl. Verdandi citing an NPC by name from the PDF (§4). Breaks: **desktop UI absent** (MainWindow.kt:40 TODO); Android UI exists in code, untested here; 0 adventures in the real DB (§3). |
| **proactive-norns** | PARTIAL | SSE contract + client indicator code exist; but no `tool.start`/`tool.result` events surfaced in any probe, and single-delta streaming (§4) means "visual indicator while she works" has nothing to animate against; re-entry states B/C/D unbuilt (features.json). |
| **system-aware** | ABSENT | Infra (campaign_system var, conditional blocks) done per features.json, but "ZERO SF2e content written → acceptance condition UNMET" (features.json, confirmed no SF2e content stories merged; not runtime-probed). |
| **source-citations** | ABSENT | status not-started; no citation markup in any probed reply (§4). |
| **creature-design** | ABSENT | Skuld commented out of `NORN_REGISTRY` (chat.py:67); client `isComingSoon = true` for SKULD (NornSelectorViewModel.kt:102). |
| **foundry-export** | ABSENT | `src/tools/foundry.py` is 1 line: `# stub — Foundry VTT tools (D7/D8, Phase 2)`. |
| **ios** | ABSENT | No iOS module/target in `settings.gradle.kts` or shared build (grep `iosMain|iosApp` → no matches). |
| **llm-cost-tracking** | **WORKS** | 105 `llm_usage_logs` rows; per-request cost in every `message.complete`; `/dev/costs/summary` returns per-agent/per-model rollup (§4). |
| **evals** | WORKS (repo evidence) | `tests/evals/` with fresh `baseline_results/*_20260414.json` files (present/modified in git status at discovery start); not re-run here (hits live APIs). |
| **cloud-deployment** | ABSENT | No terraform/infra dirs in backend (grep → none); local-only. |
| **user-accounts** | ABSENT | `src/core/auth.py` is a stub: `# stub — Cognito JWT authentication (D6+ only, do NOT implement before then)`. |

**Zero user-facing flow features are at WORKS.** The only two WORKS features are operator-facing quality features — consistent with `features.json`'s own statuses, which are honest about this.

---

## 9. "The simplest things" — precise failure points by layer

What a user **can** do today (desktop, main, backend up): launch the app → see their campaigns → open one → chat with Urd or Verdandi and get in-character, memory-aware replies → conversationally create a campaign → run a capture conversation.

What fails, and exactly where:

| Basic operation | Layer that breaks | Evidence |
|---|---|---|
| Start the product at all | Ops/docs: empty README, broken Docker Desktop, 4-month-old finch containers | §2 |
| Upload an adventure (desktop) | Client UI missing (TODO) | MainWindow.kt:40 |
| See what sessions/episodes exist | No endpoint on main + no client surface | route table §4; SurfaceType/ledger notes features.json |
| See a recap/prep artifact | No client rendering; chat prose only | §8 session-prep |
| See real session counts on picker | Client hardcode | CampaignPickerScreen.kt:87 `sessionCount = 0` |
| Watch the Norn "think"/stream | Backend sends one monolithic delta | §4 |
| Trust a capture was saved | Fabricated-bind integrity defect | §7 |
| Use Skuld / creature design / export | Not built (honest stubs) | §8 |
| Benefit from the 12 finished sprint stories | **Never merged** — sits on integration branch | §1 |

**INFERRED overall:** the "delivering stories ≠ delivering functionality" hypothesis is *partially* right but misses the sharper facts: (a) the finished sprint's functionality was never merged/released at all; (b) the backend feature spine largely works — the void is concentrated in client-side surfaces (upload, history, recap, counters) and in integration/verification machinery (E2E that can't launch, tests that silently don't run); (c) nobody — including the developer — has ever exercised the product enough to put real data in it, so features that depend on accumulated memory (prep with 2+ sessions, PC-fear callbacks, NPC tracking) have never been reachable.

---

## 10. Counter-evidence & falsifiability

Evidence **against** my findings, and what would prove me wrong:

- **"Chat works" rests partly on probes, not full GUI interaction.** I could not click the real window (no assistive access). If someone with GUI access sends a message and the reply fails to render, my harness-artifact interpretation of the UI-probe timeout (§5) is wrong and there is a real desktop rendering bug. Falsifier: run the app, send one message, watch.
- **The developer may have launched the sprint worktree build, not main.** If so, "what they saw" includes the 27 unmerged client commits and my main-branch UI observations (hardcoded 0, untrimmed greeting) don't describe their experience. Falsifier: shell history / transcript evidence of which directory `./gradlew :desktopApp:run` ran from during their session.
- **The capture-integrity defect (§7) may not manifest through the real client**, since it resends history and the model may re-stage events on the bind turn. My probe deliberately omitted history. Falsifier: run capture→bind through the actual client UI and count `session_events` rows.
- **The E2E driver may have worked via an undocumented path** — e.g., a test-classpath launcher invoked with `-PkotestTags=e2e`, or maestro-on-Android carrying the whole E2E load. My "never launchable" claim is scoped to the *documented* `:desktopApp:run` command (search basis: `git log --all -S "ui-test-junit4"`; also `grep -rn COMPOSE_UI_TEST_SERVER_ENABLED` across the repo showing no alternative launcher). Falsifier: a transcript showing a passing compose-driver session against the real app.
- **The empty DB could reflect a different DB being used for real play** (another machine, another volume). I found exactly one postgres volume in finch and its alembic stamp matches sprint E2E; but a falsifier would be another DATABASE_URL in shell profiles or a second volume.
- **Sprint merge may be intentionally gated** on the retro/quality process rather than forgotten — the momentum repo shows an active retro. That changes the interpretation ("process in flight" vs. "delivery failure") but not the ground truth that no user-runnable artifact contains the sprint work.

## 11. Open questions

1. **Which build did the developer actually open** when they "couldn't do even the simplest things" — main or the sprint worktree — and with which backend running? (Transcript agents are better placed to answer.)
2. **How did the sprint-2026-07-13 desktop E2E gate actually execute** given §6? What did the end-gate report claim as E2E evidence? (I did not audit the end-gate HTML in `.momentum/handoffs/`.)
3. **Does the real client's capture→bind flow persist events**, given history resend? (Not testable here without GUI interaction or an Android emulator.)
4. **Is single-delta SSE a backend regression or by design** (pydantic-ai non-streaming run)? I observed it consistently but did not trace `_event_generator` internals.
5. **Android runtime state** — the composeApp has richer wiring (upload, maestro flows); untested without an emulator.
6. Why does `nornspun-backend-api-1` (the containerized API) sit at status Created since April — has the API only ever been run via `uv run` ad hoc?

## Appendix: probe residue & environment restoration

- All probe rows deleted (campaign ×2, session ×1, adventures ×2 with 204s; chunk counts verified 0). Residue: ~9 rows in append-only `llm_usage_logs` (~$0.0094 total spend), two empty per-campaign dirs under `data/storage/`, and the finch db container now status Exited (was Created). DB otherwise as found (campaigns=2, sessions=1).
- Processes: uvicorn killed, Gradle daemons stopped, desktop app processes killed, finch container stopped, finch VM stopped (as found), no Docker Desktop processes left (it never successfully started). Ports 8000/5432/54345 verified free.
- Probe artifacts (logs, screenshots, probe sources) in the session scratchpad, not in any repo.
