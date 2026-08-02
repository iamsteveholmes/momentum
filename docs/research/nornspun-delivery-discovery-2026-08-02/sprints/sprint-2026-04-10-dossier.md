# Sprint Dossier — sprint-2026-04-10

**Date:** 2026-08-02
**Role:** Definitive evidence dossier for one sprint (sprint-2026-04-10) in the nornspun delivery-discovery investigation — intent, plan, execution, claim, reality, aftermath, verdict.

---

## Executive Summary

1. **The sprint's own "done" timestamp is a single calendar day** (`started: 2026-04-11`, `completed: 2026-04-11` in `.momentum/sprints/index.json`), and git history shows why that's alarming: 23 commits landed in `nornspun-client` on that one day, with the three stories' actual code merging inside a 43-minute window (10:28–11:11am PDT).
2. **The one story that restored a genuinely broken user capability — "fix-api-connection" — was reverted twice, same day, by uninvestigated follow-up commits, before being fixed again days later.** The client's chat POST URL was corrected from `/api/chat`→`/chat` at 10:28am, then reverted back to `/api/chat` at 5:54pm with the commit message "correct /chat URL back to /api/chat to match backend route" — a claim contradicted by the backend source, which had no `/api` prefix at all until three days later. The Norn-selection field fix (`@SerialName("norn")`) was similarly reverted to `"norn_id"` at 6:52pm the same day, then flipped back on 2026-04-14. (Evidence: commits `266c76f`, `3100af0`, `151ffb8`, `5f6508e`, backend `src/main.py` history.)
3. **None of this thrashing is visible anywhere in Momentum's own artifacts.** The retro doc for this sprint explicitly states its corpus contains "no dev-wave agents" for sprint-04-10 execution — confirmed independently here: the audit-extracts contain zero non-notification user messages in the 14-hour window (2026-04-11 17:00 UTC–2026-04-12 07:00 UTC) during which all the thrashing commits landed. The only surviving record of what actually happened is raw git history across two separate app repos.
4. **The story's own acceptance-testing task was explicitly deferred to "manual"**, and the manual pass that followed (the same evening) got the diagnosis wrong twice before landing right. The story file for `fix-api-connection` contains the developer/agent's own note: *"Task 3 (live E2E) deferred — unit tests confirm both bugs are fixed... Live service validation is a manual step."*
5. **The ripple effect broke a different, more foundational capability for roughly two months.** To reconcile with the (incorrectly) reverted client URL, the backend added an `/api` prefix to *every* router on 2026-04-14 (`61b59a0`) — including `/campaigns`. A partial client-side fix landed 2026-05-19 (`da22145`), but a formal assessment on 2026-05-29 (ASR-004) still found `POST /campaigns` returning 404, **blocking campaign creation entirely** on both platforms. The dedicated defect story wasn't merged until sprint-2026-05-30 (commit `8d71f09`, end-gate approved, `status_synced_at: 2026-06-12`) — over two months after sprint-2026-04-10 shipped.
6. **Two of the sprint's three stories were framed as developer/infrastructure work, not user capability**, despite being motivated by direct user observation. `desktop-m3-migration` and `shared-ui-consolidation` are both `change_type: refactor`, and their User Story sections read "As a developer working on the Nornspun desktop app... so that the desktop and Android apps share a unified design system" — not "As a Spinner." Only `fix-api-connection` (priority `critical`) is framed as restoring a GM/Spinner-facing capability.
7. **The sprint's planning-phase quality gate genuinely worked.** A 3-lens AVFL checkpoint against the three story files caught 15 real defects pre-merge (2 CRITICAL Gherkin-syntax violations, a wrong Gradle artifact coordinate that would have broken the desktop build, a wrong port), converged in a single 44-turn fix pass, and the developer approved with a one-letter "A". This is the one part of the sprint with complete, high-quality evidence — and it is upstream of code, not a substitute for verifying the code actually ran.
8. **No end-gate report, sprint-summary.md, coverage-plan.md, plan-gate-decision.md, build-ledger.jsonl, or team-composition.md exists for this sprint.** These artifacts either weren't invented yet (practice-ledger.jsonl's earliest entry is 2026-06-10, nearly two months later) or weren't produced for this sprint — the observability apparatus that might have caught the thrashing simply didn't exist at this point in the practice's evolution.
9. **All three stories remain `"status": "done"` in `stories/index.json` today** — none were later dropped, obsoleted, or explicitly reverted, despite the same-day regressions and two-month downstream outage.
10. **The chat capability does work correctly as of the current codebase** (`HEAD` on both repos shows `/api/chat` + `@SerialName("norn")` matching consistent backend routing) — but it reached that state through roughly a week of uncoordinated, untracked patch-and-revert cycles across two repos, not through the sprint's tracked process.

---

## 1. INTENT — what was this sprint for?

The sprint's three stories trace directly to specific user complaints raised during the immediately preceding sprint-2026-04-08 retro and the sprint-2026-04-10 planning session itself (per `.momentum/sprints/sprint-2026-04-10/retro-transcript-audit.md`, User Interventions section):

- **HF-08:** *"Why is the desktop and android version so inconsistent?"* — motivated `desktop-m3-migration` (paired with `shared-ui-consolidation`).
- **HF-01/HF-03:** *"don't we need to add M3 stories? Also, what about ios? And last I checked we're STILL not hooked into the API, it's just stubbed"* — the developer had to inject this gap into planning manually; the retro doc's own root-cause note (S-4/CP-4) states the prior retro's finding about the M3 inconsistency did **not** get pulled forward into this sprint's planning automatically.
- **HF-02:** *"I hate when you ask me this without doing a bit of research: 2. API stub — what specifically is still stubbed?... I don't know, but it just returns a scripted speech every time I send a message."* — the developer rejected a multiple-choice diagnostic prompt and pushed the planning agent to properly scope `fix-api-connection` only after pushback.

So the **trigger** for the sprint was unambiguously a user-observed capability failure — the chat feature returned scripted, non-live responses and the desktop/Android apps looked inconsistent. That is a USER CAPABILITY framing at the trigger level.

However, **story framing diverges from that**:
- `fix-api-connection.md` (priority Critical/P0, `change_type: bug-fix`): User Story is *"As a Spinner chatting with any Norn, I want my messages to actually reach the AI backend... so that I get real responses."* — genuine capability framing.
- `desktop-m3-migration.md` (priority High/P1, `change_type: refactor`): User Story is *"As a developer working on the Nornspun desktop app, I want the desktopApp to use Material 3 (M3) instead of Material 2 (M2), so that the desktop and Android apps share a unified design system and the app no longer looks like a Material 2 prototype."* — developer-facing framing, though the Gherkin `.feature` scenarios are written observably ("Spinner views the chat screen... buttons display with rounded corners").
- `shared-ui-consolidation.md` (priority Medium/P2, `change_type: refactor`, `depends_on: [desktop-m3-migration]`): similarly refactor-framed, code-consolidation motivated ("moving common screens to commonMain... cannot happen until both platforms use the same design system").

**Verdict on Q1:** The sprint's origin was a real, user-observed capability gap (chat doesn't work; UI is visibly inconsistent). One of three stories (the P0 bug fix) preserved that framing end to end. The other two — which consumed 2 of 3 stories and were sequenced as a dependency chain — were reframed as internal refactor/consolidation work, with user-visible outcomes expressed only in the Gherkin `.feature` files, not in the story's own problem statement.

---

## 2. PLAN — stories, waves, team, fraction product vs. process

From `.momentum/sprints/index.json` (`completed[]` entry for `sprint-2026-04-10`):

```
stories: [fix-api-connection, desktop-m3-migration, shared-ui-consolidation]
waves:
  wave 1: [fix-api-connection, desktop-m3-migration]   (parallel, independent)
  wave 2: [shared-ui-consolidation]                     (depends on wave 1's M3 migration)
team:
  wave_1: dev → fix-api-connection ; dev-frontend → desktop-m3-migration
  wave_2: dev-frontend → shared-ui-consolidation
  review: qa_reviewer, e2e_validator, architect_guard (architect_guard scoped to desktop-m3-migration + shared-ui-consolidation)
started: 2026-04-11   completed: 2026-04-11   retro_run_at: 2026-04-12
```

**Fraction product-capability vs. process/infra:** 1 of 3 stories (`fix-api-connection`) is a pure user-capability bug fix. The other 2 (`desktop-m3-migration`, `shared-ui-consolidation`) are `change_type: refactor` — technically infrastructure/consolidation work, though both carry user-observable Gherkin acceptance criteria (visual M3 styling, cross-platform parity, no regressions). No story in this sprint is pure tooling/test-infra with zero user-facing surface.

**Planning-phase quality gate — genuinely strong, with full evidence:** A 3-lens AVFL checkpoint (Factual: 40 turns/0 errs; Structural: 14 turns/2 errs; Domain Fitness: 11 turns/0 errs) ran against the three story files and produced 13 unique findings (zero duplicate findings across lenses), scoring 21/100 (lower = more issues found). Critical catches per the retro doc (W-1):
- DOMAIN-001/002 (CRITICAL): all ACs in `fix-api-connection.md` and `shared-ui-consolidation.md` were written as Gherkin Given/When/Then syntax in the plain-English AC section — violating the project convention that story ACs are plain English and Gherkin lives only in `.feature` files.
- ACCURACY-005 (HIGH): the story spec's Gradle coordinate `libs.compose.material3.android` (an Android-only artifact) was specified for the **desktop** build — this would have broken the build across 3 desktop modules had it shipped as written.
- DOMAIN-005 (HIGH): story referenced port 8000 where the E2E harness requires port 8001.

A single 44-turn fix agent pass resolved all 15 issues in severity order with no regressions, and the developer approved with a one-letter **"A"** (audit-extracts, HF-17). This is the one part of the sprint with complete corpus evidence, and it worked as designed.

---

## 3. EXECUTION — what actually happened during the build

### 3.1 The corpus gap (confirmed independently, not just asserted by the retro doc)

The retro doc's own "Scope Note" states the audit-extracts for this sprint contain sprint-04-08 execution, sprint-04-06/04-08 retro tails, and sprint-04-10 **planning** — but explicitly **not** sprint-04-10's dev execution ("no dev-wave agents, no post-wave QA/E2E/Architecture Guard, no post-sprint AVFL"). I verified this directly: querying `.momentum/sprints/sprint-2026-04-10/audit-extracts/user-messages.jsonl` for any non-task-notification message between `2026-04-11T17:00Z` and `2026-04-12T07:00Z` (the window in which, per git commit timestamps below, all of the sprint's actual coding happened) returns **zero results**. The last user message in that session before it ended is the approval `"A"` at `2026-04-11T16:11:12Z` followed immediately by `/exit`.

This means the entire dev-execution episode described below is reconstructed **exclusively from git commit history in the two app repos** — it does not exist in any Momentum-side audit trail. (Mission-context note: raw session transcripts for this era are confirmed gone; only audit-extracts survive, and the audit-extracts themselves never captured this window.)

### 3.2 The single-day commit timeline (nornspun-client, all times PDT / `-0700`, from `git log`)

| Time (04-11) | Commit | What it did |
|---|---|---|
| 10:28:21 | `266c76f7` | **fix-api-connection lands**: `preparePost("$baseUrl/api/chat")` → `preparePost("$baseUrl/chat")`; adds `@SerialName("norn")` to `ChatRequest.nornId`; updates/adds serialization tests. This is exactly the story's diagnosed fix. |
| 10:42:54 | `3b6f9d18` | **desktop-m3-migration lands**: M2→M3 theme migration in one commit. |
| 10:59:37–11:11:22 | `4db9adde`, `49b78bdd`, `0bbeaf10` | **shared-ui-consolidation** (tasks 1–11): theme/components, FirstLaunchScreen, ConversationList moved to `commonMain`. |
| 12:18:46 | `ec1db035` | KDoc/dead-code cleanup on `NornApiClient`. |
| 12:39:33 | `b66ffbc8` | **Regression fix**: `ChatMessage.Companion` reference broken by the `commonMain` migration. |
| 17:39:06 | `df560457` | **Regression fix**: "correct visual regressions found during manual verification" — the first evidence of a live manual pass, ~7 hours after merge. |
| **17:54:04** | **`3100af04`** | **Reverts the chat URL fix**: *"fix(api): correct /chat URL back to /api/chat to match backend route."* Bundled with unrelated desktop layout fixes not in scope of any of the 3 stories. |
| 18:00:59 | `6e2e2d1f` | Pip sizing, hover-state, and a genuine new fix (non-2xx response now calls `onError` instead of silently completing). |
| 18:39:54 | `e001ca8f` | Ktor compatibility follow-up to the previous commit. |
| **18:52:59** | **`151ffb87`** | **Reverts the norn-field fix**: *"fix(api): correct ChatRequest norn field name to norn_id to match backend schema."* One-line diff, no test update. |
| 21:21:19 | `49462486` | InMemoryAppPrefs removed from Android production classpath (consolidate-shared-ui-viewmodels quickfix scope). |
| 21:53:06 | `56ce04dc` | "address AVFL scan findings — import, docs, and comment accuracy." |
| 22:44:19 | `64ba9678` | HTTP/2 → CIO ktor-client swap (desktop). |
| next day 23:52:31 (04-12) | `b0550fdd` | `consolidate-shared-ui-viewmodels` quickfix merges. |

**23 total commits landed in `nornspun-client` on 2026-04-11** (`git log --oneline --since --until` count).

### 3.3 Both reverts were factually wrong when made — verified against the other repo

I checked the backend source directly rather than trusting the revert commit messages:

- **Chat URL:** `nornspun-backend/src/main.py` shows `app.include_router(chat.router)` with **no** `prefix=` argument continuously from 2026-03-26 initialization through **2026-04-14** — the `/api` prefix wasn't added to any router until `61b59a0` ("fix(api): add /api prefix to all app routers for industry-standard routing", 2026-04-14 18:35:22). So when `3100af04` claimed at 17:54 on 04-11 that reverting to `/api/chat` would "match backend route," the backend still had **no** `/api` prefix — the revert was wrong, and it re-broke every chat request for the ~3 days until the backend itself changed.
- **Norn field:** `nornspun-backend/src/models/messages.py` shows `norn: str = "urd"` unchanged from 2026-03-30 through at least 2026-07-22 (checked via `git log -p`) — the backend field was never `norn_id` at any point. `151ffb87`'s claim ("to match backend schema") was also wrong when made, and it silently re-broke Verdandi/Skuld voice selection (defaulting every request back to Urd) for the same ~3 days, until `5f6508e4` (2026-04-14 13:15:44, commit message: *"Fixes NornApiClientChatTest assertion failures"*) flipped it back to `@SerialName("norn")`.

Both incorrect reverts happened on the same calendar day as the correct fix, both were undone only days later, and neither the story file nor any Momentum artifact records that this happened — it is recoverable only by diffing commit SHAs against the other repo's history.

### 3.4 The story's own deferred-verification note

`fix-api-connection.md`, Task 3 subtask list, carries this inline note verbatim:

> `<!-- NOTE: Task 3 (live E2E) deferred — unit tests confirm both bugs are fixed. Wire format correctness verified by NornApiClientChatTest (13 tests, 0 failures). Live service validation is a manual step. -->`

Task 3's four checkboxes (Android POST /chat verification, Android Verdandi switch verification, Desktop equivalents, "confirm no 404 errors") are all **unchecked** `[ ]` in the story file. `desktop-m3-migration.md`'s Definition of Done also leaves two boxes unchecked: "Visual inspection: app launches on desktop, colors and typography render correctly" and "dark mode works correctly." Both stories reached `status: done` in `stories/index.json` with these items still open — the manual verification that was deferred is exactly the step that, when finally performed that evening, produced two incorrect diagnoses before landing correctly three days later.

---

## 4. CLAIM — what did the sprint say it delivered?

No `sprint-summary.md`, end-gate report, or coverage-plan.md exists for this sprint (these artifacts either postdate this point in the practice's history or weren't produced here — confirmed by directory listing: only `audit-extracts/`, `retro-transcript-audit.md`, and `specs/` exist under `.momentum/sprints/sprint-2026-04-10/`).

The two places anything is "claimed":
1. **`sprints/index.json`**: `status: "done"`, all three stories listed, `completed: "2026-04-11"`.
2. **`stories/index.json`**: all three stories `status: "done"`, no caveats recorded.
3. **The retro doc** (produced 2026-04-12, the only completion-adjacent artifact) frames the sprint's **planning phase** as "the one bright spot" and states plainly that dev execution is outside its evidence window — it does not claim the delivered code was verified working, and is explicit that it cannot make that claim from its corpus.

There is no artifact anywhere that asserts "the chat feature was confirmed working end-to-end" — the closest thing is the unit-test pass count cited in the story's own Dev Agent Record ("All 13 tests in NornApiClientChatTest pass").

---

## 5. REALITY — what actually landed, and did it change user capability?

- **Chat (fix-api-connection):** Landed correctly at 10:28am, broken again by 6:52pm (both bugs), corrected again by 2026-04-14. As of current `HEAD` in `nornspun-client`, `NornApiClient.kt` calls `"$baseUrl/api/chat"` and `ChatMessage.kt` carries `@SerialName("norn")` — internally consistent with the backend's current `/api`-prefixed routing. **The capability does work today**, but not continuously since the sprint, and not because the sprint's own process caught and held the fix.
- **Desktop M3 migration + shared-ui-consolidation:** Code merged same day; build reported green (`BUILD SUCCESSFUL`, 325/326 tests) per the story's own Dev Agent Record, but real regressions were found and fixed only via same-evening manual testing (`df560457` "visual regressions found during manual verification"; `b66ffbc8` "fix ChatMessage.Companion reference after commonMain migration") — i.e., defects that a tracked QA/E2E pass should catch were caught by the developer manually poking the running app after hours, not by the pipeline (whose output isn't in this sprint's corpus at all).
- **Downstream (campaigns, not part of this sprint but a direct consequence of it):** The backend's blanket `/api` prefix change (`61b59a0`, 2026-04-14) — made specifically to reconcile with the client's incorrectly-reverted chat URL — silently moved every other router (`/campaigns`, `/tasks`, `/sessions`, `/adventures`) behind the same prefix at once. The client's `createCampaign` call wasn't fixed until 2026-05-19 (`da22145`, "correct POST /campaigns path to /api/campaigns"), and **even after that fix, a formal assessment on 2026-05-29 (ASR-004) still recorded `POST /campaigns` returning 404**, blocking campaign creation on both platforms:
  > *"BLOCKER: POST /campaigns returns 404 — campaign creation currently fails silently at name entry (Android + Desktop). Story exists: fix-post-campaigns-404-campaign-creation-endpoint-missing-or."* (`docs/assessments/asr-004-campaign-init-completion-audit-2026-05-29.md`, line 44)

  That defect story (`fix-post-campaigns-404-campaign-creation-endpoint-missing-or`, priority critical) shows `status_synced: "merged-to-main sprint-2026-05-30 (commit 8d71f09, end-gate APPROVED)"`, `status_synced_at: "2026-06-12"` in `stories/index.json` — i.e., campaign creation, arguably the single most foundational action in the entire app, was broken end-to-end for somewhere between 3 weeks (from the 05-19 partial fix, which didn't work) and over 6 weeks (from the 04-14 backend change that started it), formally closed roughly **two months** after sprint-2026-04-10 shipped.

---

## 6. AFTERMATH — did these stories get revisited, dropped, or reverted?

- All three stories (`fix-api-connection`, `desktop-m3-migration`, `shared-ui-consolidation`) remain `status: "done"` in `.momentum/stories/index.json` today — none were later marked dropped, obsolete, or reverted.
- The same **class** of bug (client/backend route-prefix mismatch) recurred at least three distinct times traceable to this sprint's aftermath: chat (04-11, same-day thrash), campaigns (04-14 onset → partial fix 05-19 → confirmed still-broken 05-29 → formally fixed sprint-05-30/merged 06-12).
- The retro doc for sprint-2026-04-10 itself (RV-01 through RV-11, CP-1 through CP-7) contains **no mention** of the same-day thrashing or the eventual campaign-creation outage — because, as shown in §3.1, the corpus it was built from never captured that execution window. The only place any of this is documented at all is the 2026-05-29 assessment (ASR-004) noting the still-open campaigns 404, and the git history itself.
- `.momentum/sprints/index.json` also registers a quickfix slug `quickfix-2026-04-11` for this period, but no directory of that name exists under `.momentum/sprints/` — the closest match, `quickfix-consolidate-shared-ui-viewmodels`, is a differently-named artifact. This is a minor index/artifact naming drift, noted for completeness but not load-bearing to the verdict.
- ASR-004 does independently corroborate the planning-phase AVFL's value: *"Multi-lens AVFL → dev/QA/E2E team cycle caught real defects pre-merge (04-10: 15 defects incl. a /api/campaigns 404 via structural cross-referencing)"* — confirming the planning-time catch was real and useful, even though it didn't prevent the subsequent execution-time thrashing.

---

## 7. VERDICT

**"After sprint-2026-04-10, a user could send a chat message and receive a real AI response in the correct Norn's voice on both Android and Desktop, which they could not do before (every prior chat POST 404'd, and Norn selection was silently ignored, defaulting every conversation to Urd)."**

This sentence **can be completed** — the underlying two-bug diagnosis in `fix-api-connection.md` was accurate, and the fix that ultimately stuck (as of current `HEAD`) does restore real, non-stubbed AI chat with correct Norn routing on both platforms. It does not fail the "mocked/unreachable/flag-off" strictness test in the mission brief — the capability is genuinely live in the current codebase.

**But the sentence cannot honestly be completed with the implied corollary "...as of the sprint's `completed: 2026-04-11` timestamp."** On that exact date, both halves of the fix were shipped, reverted by uninvestigated same-day follow-up commits, and left broken until 2026-04-14 — three days after the sprint's own registry says it was done. And the sprint's uncoordinated recovery effort (the backend-side blanket `/api` prefix change made to reconcile with a wrong client revert) is what broke campaign creation — a more foundational capability than chat — for roughly two months afterward, a fact recorded nowhere in Momentum's own artifacts and discoverable only by cross-referencing a later, unrelated assessment (ASR-004) against raw git history.

The other two stories (`desktop-m3-migration`, `shared-ui-consolidation`) changed what the desktop app *looks like* (M3 styling, consistent theming) and *how the code is organized* (shared `commonMain`), which is a real and legitimate improvement, but neither unlocked a new user action — they made an existing screen look different and consolidated code paths. Whether the user could reliably use the desktop app immediately after 2026-04-11 is not fully resolvable from this evidence alone, since the Definition-of-Done "visual inspection" and "dark mode" checkboxes were left unchecked and no dedicated verification artifact exists — see Open Questions.

---

## Counter-evidence & falsifiability

Evidence that cuts against the headline finding, and what would overturn it:

- **The planning-phase AVFL genuinely worked as designed** (§2) — this is a clear counter-example to "review gates never work" and should not be lost in the emphasis on execution-time failure. If someone wants to argue the whole practice is broken, this sprint's planning phase is a data point against that.
- **The chat capability is correctly implemented in the current codebase.** This is not a case of a permanently-broken feature — the underlying diagnosis and fix were both right; the failure mode here is specifically about **verification timing and observability**, not about the fix being wrong in substance.
- **The developer (not just an autonomous agent) was actively present and hand-fixing bugs the same evening** — commits are authored as `Steve <iamsteveholmes@gmail.com>` with `Co-Authored-By: Claude Sonnet 4.6` trailers throughout, consistent with this project's stated commit-attribution convention (agents commit under the developer's git identity). This means the thrashing was a **human-in-the-loop, live-testing session**, not an unsupervised agent going rogue — a materially different risk profile than "the agent silently shipped a regression and nobody looked." The developer *was* looking; the process just didn't capture what they found or fed it back into the story/retro record.
- **What would prove this dossier's headline wrong:** discovery of a session transcript or artifact (not found in this investigation) showing the 2026-04-11 evening work *was* run through a tracked Momentum pipeline (e.g., a dev-wave agent session with QA/E2E in the loop) rather than ad hoc — that would mean the "invisible to Momentum" claim is a corpus-completeness artifact rather than evidence the work genuinely bypassed the practice. I did not find such a session, and the retro doc's own scope note independently agrees none exists in the retained corpus, but the underlying raw transcript for that exact window is confirmed deleted (per mission context, only audit-extracts survive for this era), so absence-of-evidence has a real limit here.

---

## Open questions

- **Was the 2026-04-11 evening thrashing session run through any Momentum skill at all** (e.g., `momentum:quick-fix` or a direct dev-agent invocation), or was it entirely ad hoc Claude Code usage outside the practice? Commit messages carry no story-slug references (unlike later sprints, e.g. sprint-2026-07-13's `feat(session-counter-live-update-on-capture-close): ...` convention) and are not present in `stories/index.json` as their own entries, which suggests "ad hoc" — but this convention may simply not have existed yet in April, so the absence of a slug in the commit message is not conclusive proof by itself.
- **Was the desktop app or Android app actually visually verified working** after the M3 migration and shared-ui-consolidation merges, beyond the "correct visual regressions found during manual verification" commit? The Definition-of-Done checkboxes for both stories remain unchecked in the story files, and no screenshot, E2E run, or QA sign-off artifact for this sprint's execution survives to confirm or deny.
- **What exactly closed the gap between `da22145` (2026-05-19, partial campaigns fix) and the still-broken state recorded in ASR-004 (2026-05-29)?** I did not trace the specific commit(s) in the 2026-05-30 sprint that finally resolved `fix-post-campaigns-404-campaign-creation-endpoint-missing-or` — that lies in a later sprint outside this dossier's assigned scope, and is flagged here only because it is directly downstream of this sprint's events.
- **The `quickfix-2026-04-11` slug registered in `sprints/index.json` has no corresponding directory** — whether it's a rename of `quickfix-consolidate-shared-ui-viewmodels` or a separate, lost artifact was not resolved.
