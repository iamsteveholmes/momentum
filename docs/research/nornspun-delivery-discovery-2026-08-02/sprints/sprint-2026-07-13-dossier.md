# Sprint Dossier — sprint-2026-07-13 ("Memory Foundation")

**Date of this dossier:** 2026-08-02
**Role:** Evidence dossier for one sprint (sprint-2026-07-13, nornspun's "Sprint A — Memory foundation"), built for the discovery investigation into why no complete user-facing feature works end-to-end after 10 sprints. All evidence is cited by file path, commit SHA, or direct transcript quote. OBSERVED = the agent read/ran/saw it directly. INFERRED = the agent concluded it from combining observations.

---

## Executive summary

1. **Nothing from this sprint has ever reached `main`.** In both `nornspun-backend` and `nornspun-client`, the branch `sprint/sprint-2026-07-13` is strictly ahead of `main` (26 unique backend commits, 27 unique client commits) and `main` is not a descendant of it. `git merge-base --is-ancestor sprint/sprint-2026-07-13 main` returns false in both repos, confirmed 2026-08-02. (OBSERVED)
2. **The end-gate was never decided.** The report was rendered 2026-07-22 (commit `7192448`, "6 decision cards, honesty tables, anti-rubber-stamp gate"); no subsequent commit in the planning repo (`nornspun`) records an approve/reject/D1–D6 verdict. `.momentum/sprints/sprint-2026-07-13/` has a `plan-gate-decision.md` (pre-sprint) but no equivalent end-gate decision file. The sprint stayed `"status": "active", "locked": true` in `sprints/index.json` and all 12 stories stayed at status `"review"` (not `"done"`) through 2026-08-02 — the only sprint in the registry in this state. (OBSERVED)
3. **The sprint's own automated verification — before any human looked at it — found the keystone capability unreliable.** Running against the live INTEGRATION backend (the correct sprint-branch build), the build's own coverage-discharge and E2E phases found: post-session capture's "It is written." receipt was narrated ~7 times but produced a database row only ~2 times (silent capture loss); one capture persisted an entirely different, fabricated adventure's content; capture-less conversations mint phantom numbered "sessions" that inflate the session counter. These are documented in `build-ledger.jsonl` and became end-gate decision cards D4–D6. (OBSERVED)
4. **The end-gate report's own header contradicts itself:** "0 blocked / broken stories" sits directly beside the report's lead sentence: *"the sprint's core promise, 'what you tell Urd gets remembered,' is not yet reliable when a real language model drives it."* All 12 stories are marked `shipped-merged` in the same report. (OBSERVED)
5. **When the developer actually drove the app (2026-08-02, 11 days after the report), the exact capability the sprint's stated AC targeted was still broken**: "the agent doesn't know what campaign I've chosen. If it doesn't know the campaign I've chosen how can it save anything to that campaign?" and, from Urd itself, "I don't have a way to determine which one is 'current' — that's not information I track automatically." (OBSERVED, direct quotes, session `20b5f62e`)
6. **A confounding, separate operational defect was found during this same review**: the assistant driving the developer's manual walkthrough repeatedly read code from and restarted the backend server at `~/projects/nornspun-backend` — the **`main`** checkout, missing all 26 sprint commits — while the client app was correctly built from the sprint's INTEGRATION worktree. This mismatched pairing (old backend + new client) means at least some of what the developer personally experienced conflates "sprint code is broken" with "reviewer used the wrong build." (OBSERVED via transcript + git worktree inspection)
7. **A real, confirmed sprint-native code defect independent of the above**: `backend-active-campaign-name-injection-fix` — a story whose entire stated purpose is "inject campaign name (not UUID) into agent prompts" — was fixed correctly on the sprint branch (commit `2eef2bf`, verified by reading the diff) but that fix never reached `main`; when the developer's session diagnosed a still-broken "Active campaign: <uuid>" prompt line 8 days later, the actual root cause traced to querying the `main` checkout, not the sprint branch. The rushed same-day patch (`ab2e579`, 2026-07-30) was applied **directly to `main`, outside any sprint or story process**, bypassing planning, code review, and the conduct pipeline entirely.
8. **INTENT was legitimately capability-framed, not task-framed.** The MVP roadmap explicitly calls this "the keystone sprint" for "Campaign init → adventure ingestion → session prep → post-session capture → living memory → campaign identity," and story ACs are written as user-observable invariants (e.g., "The model should never ask what campaign I want to use"). This sprint is **not** a case of stories substituting for capability language at the planning layer — the failure is downstream of planning. (OBSERVED)
9. **7 of 12 stories were genuine capability-building work** (Store A/B, segmentation, session naming, urds-post-session-capture, session-counter, campaign-picker); 1 was test infrastructure (kotest migration), 1 was an internal rename refactor (exchange_id), and 3 were quick-fix-class bug/copy fixes folded in by product-owner decision. Real code landed on the branches: +6,993/−202 lines across 46 files (backend), +3,882/−2,146 across 81 files (client). The work is not vaporware — it is real, tested, reviewed code that never crossed the trunk line. (OBSERVED)
10. **The developer's own review session surfaced the practice gap directly**: *"Don't we now have the concept when using momentum:compose of fixing the sprint inline when it's not meeting its goals?"* — no such skill exists in the installed plugin (`ls ~/.claude/plugins/cache/momentum/momentum/0.31.0/skills/` has no `compose`); the assistant improvised an ad hoc dynamic `Workflow` script to patch main directly instead. (OBSERVED)

---

## 1. INTENT

The sprint's goal was captured in `docs/planning-artifacts/mvp-roadmap-sprints-a-e-2026-07-09.md`, adopted by the product owner 2026-07-09:

> **MVP gate being closed:** Campaign init → adventure ingestion → session prep → post-session capture → living memory → campaign identity — "Friends & Family Ready", without Foundry VTT integration.

> **Sprint A — Memory foundation (12 stories)** — "The keystone sprint. Backend-heavy; two-repo (nornspun-backend + nornspun-client)."

This is capability language, not task language — the roadmap explicitly frames the sprint around a chain of things a Spinner (player) or GM can do, and names `episode-transcript-persistence-store-a` as "the single highest-leverage unblock in the MVP" whose acceptance criterion is stated as a **user-observable invariant, verbatim** in the roadmap:

> AC (product invariant, verbatim): "The model should never ask what campaign I want to use. The campaign should have been chosen prior to speaking with the Norn."

The story spec itself (`~/projects/nornspun/.momentum/stories/episode-transcript-persistence-store-a.md`) frames its purpose the same way:

> "As the Spinner whose campaign thread must hold across sessions, I want the full conversation with each Norn durably persisted server-side as an episodic transcript scoped to my campaign, so that the human-facing memory loop can finally close — capture has a transcript to bind, the returning-greeting can source what happened last time, and the Living Memory ledger has data to read."

**Finding:** at the planning-intent layer, this sprint is squarely capability-framed, and its central story is explicitly a "keystone" chosen for maximum end-user leverage, not an arbitrary task. This is a meaningful data point against a naive version of the "sprints optimize for stories, not capability" hypothesis — the plan itself did not commit that sin. The failure, as detailed below, is downstream: in execution reliability and in the practice's missing "get this onto trunk and confirm a human can use it" step.

The plan-gate decision (`plan-gate-decision.md`, approved 2026-07-13 via `.momentum/handoffs/sprint-2026-07-13-plan-gate.html`) ratified the full 12-story keystone chain in one sprint and five specific design forks (capture-close line "It is written.", session-naming copy, greeting-trim direction, campaign-picker scope as "verify-and-close-gaps").

---

## 2. PLAN — stories, waves, team, capability fraction

12 stories, 7 waves, two repos. From `sprints/index.json` (`active.waves`) and `.momentum/stories/*.md` frontmatter `change_type`:

| # | Story | change_type | Capability class |
|---|---|---|---|
| 1 | `migrate-desktopapp-tests-from-kotlin-test-to-kotest` | config-structure, script-code | Test infrastructure |
| 2 | `exchange-id-rename-across-norn-agents` | backend | Internal rename (no user-visible behavior change) |
| 3 | `episode-transcript-persistence-store-a` | script-code, app-ui | **Keystone product capability** |
| 4 | `episode-auto-segmentation-boundary-model` | script-code, app-ui | Product capability (backend model, feeds capability) |
| 5 | `episode-close-summarization-store-b` | backend | Product capability |
| 6 | `session-naming-two-message-close` | backend, script-code | Product capability (UX) |
| 7 | `urds-post-session-capture` (REVISE) | script-code | Product capability (core capture UX) |
| 8 | `session-counter-live-update-on-capture-close` | app-ui, backend | Product capability (small, UI receipt) |
| 9 | `campaign-picker-get-campaigns-client-repo` | app-ui | Product capability |
| 10 | `backend-active-campaign-name-injection-fix` | backend | Ex-quick-fix, folded in |
| 11 | `urd-threshold-flowrow-inline-prose-fix` | app-ui | Ex-quick-fix, folded in |
| 12 | `norn-greeting-capability-menu-trim` | app-ui | Ex-quick-fix, folded in |

**Fraction:** 7/12 (58%) genuine capability-building stories, 1/12 test infra, 1/12 pure refactor, 3/12 folded-in quick-fixes. This is a healthier capability fraction than the "stories vs. process" hypothesis would predict for a sprint that later failed this badly — the plan was not thin gruel.

**Waves** (from `sprints/index.json`): Wave 1 was a hard gate (kotest migration, "no memory-backbone story merges before it is green" — because desktop tests silently didn't execute in sprint-2026-06-18, a carried-forward defect). Waves 2–7 sequenced the keystone chain: exchange-id rename → Store A → segmentation → Store B → session-naming/urds-post-session-capture (explicit **co-land wave 6**, "the wave is not green until both are merged") → session-counter. The dependency reasoning is explicit and sound in the coverage-plan and story frontmatter (`depends_on` fields).

**Coverage plan** (`.momentum/sprints/sprint-2026-07-13/coverage-plan.md`): one integration scenario ("Scenario A — Post-session capture close, naming, and recap over the chat API") discharges 4 stories by composition; the other 8 are dedicated-run. All 12 stories accounted for exactly once — the coverage bookkeeping is internally consistent.

---

## 3. EXECUTION — what happened during the build

Evidence: `.momentum/sprints/sprint-2026-07-13/build-ledger.jsonl` (156 lines), git history of both product repos, and session transcript `2a45301c-e57a-4695-96b8-6ddd94d13bb4.jsonl` (5.7MB, spans 2026-07-21 08:40 → 2026-07-22 16:38 UTC).

**Story-level build:** all 12 stories reached `story-terminal` with `outcome: merged` (merged into the sprint branch, not main — see §5). Real commits landed per story, each following the pattern feat → fix (auto-fix from code review) → occasional refactor (simplify pass) → merge. Example, backend: `9ce8eaa feat(episode-transcript-persistence-store-a): Alembic 013 transcript_turns, TranscriptRepository, append-on-chat wiring` → `f31a64b fix(...): auto-fix persist-before-yield so client disconnect cannot drop a generated turn` → `42376e4 refactor(...): simplify cleanup pass` → merge `d51c933`.

**AVFL-on-merge** (event `avfl-on-merge-complete`, 2026-07-22T15:06:30Z): `result_status: NON_CONVERGENT`, `reason: escalated-and-residual-leftovers`. Backend score 51→85 (post-fix; one escalated critical remains — INTEG-001 phantom sessions), client 69→92 (post-fix; one triaged-out major remains). 17 findings total, 12 fixed, 2 leftover (escalated + residual). A `conductor-warning` logged that 3 of 16 validators never returned findings after two pings over ~10 hours, so the run consolidated on 13/16 lens coverage — a real gap in the validation's own completeness, disclosed rather than hidden.

**Coverage discharge** (2026-07-22T15:23:07Z): of the 4 stories nominally covered-by-composition via Scenario A, only 1 (`exchange-id-rename-across-norn-agents`) was cleanly discharged. The other 3 came back **undischarged**:
- `session-naming-two-message-close`: "AC4 two-message rhythm unreliable (offer+close collapse into one turn, reproducible); AC1/AC3 persistence unconfirmable due to silent bind failure."
- `urds-post-session-capture`: "AC3 durable persistence FAILS — fresh conversation reports no sessions after confident close; DB count 0 confirms."
- `episode-close-summarization-store-b`: "recap-availability tail never exercised (no committed rows for summarizer to read); contract passed only via its graceful-degradation escape hatch."

A harness bug (`extract_reply_text()` bash-heredoc-in-piped-function bug) also independently broke two frozen smoke contracts regardless of backend behavior — a real, disclosed tooling defect that further degraded the reliability of what the sprint's own contracts could confirm.

**The critical finding, `discharge-stakes-capture-receipt-1`** (2026-07-22T15:23:07Z, severity `critical`, `stakes_class: high-blast-radius-architecture`):

> "SILENT CAPTURE LOSS: Urd narrates 'It is written.' (and even rename confirmations) without the underlying bind_memories tool call executing — ~5 of 7 live closes produced the receipt with zero DB rows and zero logged errors. The conversational receipt is not coupled to the commit."

**E2E phase** (2026-07-22T15:33–15:57 UTC): 34 scenarios checked, 28 passed, 1 failed, 2 findings, 1 escalated to end-gate. The escalated finding, `e2e-capture-integrity-1`:

> "FABRICATED CAPTURE CONTENT: persisted session row contains an entirely different adventure's narrative than the one narrated ('Graul Farmhouse' slave-pens/Vankor/giant-ape content vs the narrated Sunken Ruins of Vhalos session)... pattern consistent with the newly-adopted openrouter:tencent/hy3-preview model narrating/mis-executing tool calls."

A follow-up reproduction on a fresh, isolated campaign found the mismatch **in the live reply itself, not only the stored row** — Urd described an unrelated sci-fi scene for a fantasy narration — leading the validator to flag a working hypothesis of cross-request context bleed under concurrent load, a potential escalation to a security/isolation stakes class (recorded as a `conductor-warning`, not fully resolved).

Separately, `session-counter-live-update-on-capture-close`'s own live AC1 proof was recorded as **"UNOBSERVED — recorded as a hollow-verification item"** because the only session row present was corrupted by the capture-integrity bug; the counter's code was verified correct by unit test, but its live behavior was never actually confirmed end-to-end.

Also disclosed at E2E: Android hardcodes `10.0.2.2:8000` vs the harness's port 8001 (needs a config story); a new, unowned bug where mid-session Norn-pip tap changes header tint but doesn't rebind the message list/composer; desktop platform parity **unverified this session** ("window not on visible display; AX-blind" — 4 stories' desktop-side ACs were never actually watched by a human or the validator).

**Finding: the sprint's own quality pipeline worked as designed and caught severe defects.** AVFL and E2E did their job — the problem is not that verification was absent; the six decision cards (§4) are the pipeline correctly surfacing the truth. The gap is what happened *after* the pipeline surfaced it (§5, §6).

---

## 4. CLAIM — what the sprint said at completion

The end-gate report (`.momentum/handoffs/sprint-2026-07-13-endgate-report.html`, rendered 2026-07-22, commit `7192448` "6 decision cards, honesty tables, anti-rubber-stamp gate") opens with:

> "All 12 stories built and merged — and the live verification run then caught the thing that matters most: the sprint's core promise, 'what you tell Urd gets remembered,' is not yet reliable when a real language model drives it. Three related live findings (sessions minted without play, captures narrated but never saved, and one capture saved with the wrong content entirely) all sit at the same seam: whether the model actually calls its save tools when it says it did... **Nothing here blocks the merge itself** — the question each card asks is what to do next about a known, documented gap."

Header stat line: **"12 stories built & merged · 8 high-risk divergences caught & fixed · 6 decisions for you · 43 routine findings auto-fixed · 17 waved off with rationale · 0 blocked / broken stories."**

All 12 stories are individually listed with outcome `shipped-merged` (including `episode-transcript-persistence-store-a`, `urds-post-session-capture`, `episode-close-summarization-store-b` — the three whose behavioral coverage deferrals were, per §3, explicitly undischarged or failed).

Six decision cards were presented, asking the developer to rule on:

- **D1** — a race condition where two simultaneous messages in one campaign can silently lose a saved exchange (sequence-number collision, swallowed error).
- **D2** — episode "overnight" boundary computed in UTC ("London's midnight"), not the player's local time.
- **D3** — an architectural layering precedent: the persistence layer now launches background AI jobs directly (Store B).
- **D4** — ordinary (non-play) conversation mints phantom numbered "sessions" that the counter counts as real.
- **D5** — "It is written." is sometimes a lie: the capture-receipt/persistence decoupling (§3).
- **D6** — one capture saved entirely wrong content; live replies also showed cross-conversation content.

**Finding: the report is honest about the defects but frames them as decisions to ratify around a merge it recommends proceeding with**, not as blockers. The self-contradiction is structural: the same document states both "0 blocked / broken stories" and "the sprint's core promise... is not yet reliable." Whether that framing is itself a defect of the end-gate report's design (optimizing for "nothing here blocks the merge" language when the substance says otherwise) is a fair question for the practice's report-format standards, separate from this sprint's specific facts.

---

## 5. REALITY — what actually landed

**Backend** (`/Users/steve/projects/nornspun-backend`, checked 2026-08-02):
- `main` HEAD: `ab2e579` (2026-07-30, see §6).
- `sprint/sprint-2026-07-13` HEAD: `b6a72b0`.
- `git rev-list --left-right --count main...sprint/sprint-2026-07-13` → **`1  26`**: main has 1 commit not on the sprint branch (the 2026-07-30 hotfix); the sprint branch has 26 commits not on main.
- `git merge-base --is-ancestor sprint/sprint-2026-07-13 main` → **false**.
- `git diff --stat main sprint/sprint-2026-07-13`: 46 files changed, +6,993/−202 (mostly new tests + migrations 013–016 + repositories + agent tool wiring).

**Client** (`/Users/steve/projects/nornspun-client`):
- `main` HEAD: `704e63c` (a sprint-2026-06-18 merge commit, predates this sprint entirely).
- `sprint/sprint-2026-07-13` HEAD: `2e4e721`.
- `git rev-list --left-right --count main...sprint/sprint-2026-07-13` → **`0  27`**: main has zero unique commits; the sprint branch is a strict superset.
- `git diff --stat`: 81 files changed, +3,882/−2,146.

Both repos are **currently checked out on `main`** (`git branch --show-current` → `main` in both), i.e. `main` is what a normal `./gradlew :desktopApp:run` or backend launch would build from absent explicit action to check out the sprint branch or its INTEGRATION worktree. **None of this sprint's 12 stories' code is present in either repo's trunk.** The one exception, ironically, is a partial, rushed re-implementation of one story's fix applied 8 days late (§6).

Two dedicated Conductor worktrees do hold the correct, fully-integrated sprint code: `/Users/steve/projects/.conduct-wt/nornspun-backend/INTEGRATION` at `b6a72b0` and `/Users/steve/projects/.conduct-wt/nornspun-client/INTEGRATION` at `1c4e7d3`. These are the build artifacts the sprint's own AVFL/E2E validation correctly exercised (confirmed by ledger evidence text: "Frozen contract ran clean vs live INTEGRATION backend").

**Did the landed code (on the sprint branch, in isolation) change what a user could do?** Partially, and unreliably, per the sprint's own E2E findings (§3): capture persistence worked roughly 2 of 7 times in the live verification run; one persisted capture had fabricated content; ordinary conversation inflated the session count with phantom entries. Even judged purely on its own branch, in isolation from the main-merge question, the keystone capability was not reliable.

**Did the developer's own hands-on walkthrough confirm or contradict this?** Both — with an important confound. Two review sessions exist:

- **2026-07-22, session `2a45301c...` (tail end).** The developer, looking at the viewer pane, asked: *"I see a 07-13 report but that can't be it. Where is the report? And shouldn't I be looking at the app itself?"* The assistant responded "yes — you absolutely should look at the app itself," closed a stale tab, and launched the desktop app from the INTEGRATION worktree. **The transcript file ends here, mid-launch, at 2026-07-22T16:38:28Z** — no further record exists of what the developer actually saw that day in this file.
- **2026-08-02, session `20b5f62e...`.** The developer resumed: *"Well that's not exactly right is it. I'm supposed to run through the entire app and see what I see for both desktop and android, right? It's not just about the end-gate document it's about my review."* Confirmed: *"your review was mid-flight when you left — you'd exercised the campaign picker and found two real defects; the rest of the walkthrough never happened."* Driving the app now:
  - **"Multiple things were problems. First, when I chose choose new campaign from the picker it went to a UI that didn't allow me to go back to the campaign picker in any way... Even after I created a name it showed the '>' but clicking it did nothing."** The assistant diagnosed this as a genuine **client-side defect in the sprint's own new code** ("the create flow has no [way back]") — not a pre-existing issue, not an environment artifact.
  - **"Another major issue is when I chose the salt mines campaign that I had already filled in last time it started from scratch."** Diagnosed by the assistant as a **pre-existing, unrelated gap**: heroes/PC content was never persisted by any story, in this sprint or before (`SELECT count(*) FROM heroes WHERE campaign_id=...` → 0 rows; 0 heroes system-wide). This part of the complaint is **not** attributable to sprint-2026-07-13.
  - **"So the first thing I notice at least on Android, is that the agent doesn't know what campaign I've chosen. If it doesn't know the campaign I've chosen how can it save anything to that campaign?"** — root-caused to the Android emulator restoring a stale E2E-fixture campaign ("TrimTestCampaign," left over from 2026-07-22 automated test runs) from local device state; the actual wire request carried a `campaign_id` throughout.
  - **"Same on desktop. I had chosen a campaign and got this: Urd — I can see you have several campaigns in the chronicle, but I don't have a way to determine which one is 'current' — that's not information I track automatically."** This is the direct, in-app manifestation of the sprint's targeted AC failing ("the model should never ask what campaign") — and root-caused, on investigation, to reading `~/projects/nornspun-backend/src/agents/urd.py` (**`main`**, not the sprint branch) where the "Active campaign:" line still appended the raw UUID unconditionally — because `main` never received the sprint's fix.

**Finding: the review environment itself served a version-mismatched app** — client from the sprint's INTEGRATION worktree, backend restarted from `main`. This is confirmed directly: the assistant's own diagnostic greps and file reads used `~/projects/nornspun-backend/...` paths, and the eventual hotfix restart command was `cd /Users/steve/projects/nornspun-backend && uv run uvicorn src.main:app --port 8001` — main, not the INTEGRATION worktree. This means the developer's 2026-08-02 walkthrough is not a clean test of "does the sprint's delivered code work" — it is a test of a Frankenstein pairing that nobody intended. Some of what the developer saw (campaign context not surfacing) is explained by this mismatch and would very plausibly not reproduce against the correct INTEGRATION backend; other things the developer saw (picker back-navigation dead-end) were independently diagnosed as real client-side sprint-code defects, unrelated to the backend mismatch.

---

## 6. The 2026-07-30 out-of-process hotfix

While diagnosing the "agent doesn't know current campaign" symptom on 2026-08-02, the assistant found the currently-running backend was `main`, not the sprint's INTEGRATION branch, and that `main`'s `urd.py`/`verdandi.py` still appended the raw campaign UUID unconditionally (the code that predates the sprint's fix entirely, since main never received it). The developer authorized an inline fix ("Feel free to... Don't we now have the concept when using momentum:compose of fixing the sprint inline when it's not meeting its goals?"). Checking the installed plugin (`~/.claude/plugins/cache/momentum/momentum/0.31.0/skills/`) found no `compose` skill — the assistant instead built an ad hoc dynamic `Workflow` script (`endgate-binding-chain-fixes`) and ran three parallel fixes:

- **F1 (backend)**: committed directly to `main` as `ab2e579` ("fix(agents): active-campaign prompt line carries resolved name, not raw UUID," 2026-07-30, `Co-Authored-By: Claude Fable 5`). This commit's own message notes: *"the assertion the original story lacked (variable was populated but no template consumed it)"* — worth flagging as a claim not fully verified by this dossier: comparing the sprint branch's own `667b3ea` state (which this dossier read directly) shows the sprint's own fix **did** correctly build and use a local `campaign_name` variable in the appended line; the defect that actually manifested for the developer was that `main` had never received that fix at all, not that the sprint's fix was itself incomplete. The commit message's "original story lacked" framing may overstate the story's own defect and understate the true root cause (nothing had been merged).
- **F2 (client)**: rebind observer + wire-level tests confirming `POST /api/chat` carries the newly-selected `campaign_id` on both platforms. The fix agent's own report flagged an honest caveat: *"static analysis of the tip found the picker tap path ALREADY rebinding campaignId (commit 6028149, Jul 21) — I could not reproduce a code path at tip that sends the stale id after a picker tap."* I.e., part of what looked broken may have already been fixed by the sprint itself; the observed symptom may have come from stale app/device state, not a live code defect. Landed on the **sprint branch** (`41b59bb`), not main.
- **F3 (client)**: "ghost-buster" — validates a persisted active-campaign id at startup and falls back to the picker if invalid. Landed on the **sprint branch** (`a05fde5`, `2e4e721`), not main.

**Aftermath of the hotfix**: F1 is on `main` alone (not integrated back into the sprint branch or vice versa — the two histories remain fully divergent). F2/F3 are on the sprint branch alone (still not on `main`). The database was also manually purged during this session: 17 of 19 campaigns (mostly 2026-07-22 E2E/validator fixtures such as "TrimTestCampaign," "Persistence Test Alpha," "Naming Contract ...") were deleted in a single transaction, along with 16 fixture episodes, 120 transcript turns, and ~110 test session/log rows — cleanup of debris the sprint's own automated E2E validators had left in the shared development database for over a week, undiscovered until the developer's manual review surfaced it.

**Finding:** the practice, when confronted with a stuck, undecided sprint blocking the developer's ability to use the app, resorted to an unplanned, ungoverned same-day patch directly to trunk — no story, no plan gate, no code review pipeline, no AVFL, no coverage contract — while the properly-governed sprint branch carrying the same defect sat untouched and still unmerged. This is a second, distinct failure mode from "stories pass but capability doesn't materialize": here, the *response* to that failure bypassed the practice's own quality machinery entirely.

---

## 7. AFTERMATH

- **Story statuses**: all 12 stories remain `"review"` in `.momentum/stories/index.json` as of 2026-08-02 (checked directly) — not `"done"`, not `"dropped"`, not `"obsolete"`. Compare: every other completed sprint (e.g., `sprint-2026-05-01`, `sprint-2026-04-08`) shows `"status": "done"` in `sprints/index.json`'s `completed` list. Sprint-2026-07-13 is the only sprint still in `active`/locked state.
- **features.json**: `session-capture`, `campaign-init`, `session-prep`, and `living-memory` are all still `status: "partial"` — none flipped to a higher completion status after this sprint's work, consistent with none of it having landed to a shippable trunk.
- **New backlog entries generated from this sprint's own failures**: `.momentum/practice-ledger.jsonl` and `git log` in the planning repo show a wave of `docs(stories): intake stub` commits dated 2026-07-21/22 capturing the sprint's own deferred findings as new backlog stories (e.g., `store-a-wire-sqldelight-cross-restart-seating`, `store-b-cost-guard-ceiling-re-drive-path`, `fix-nornapiclientchattest-noclassdeffounderror`) — the sprint generated more backlog than it closed.
- **A decision was queued, not resolved**: a `momentum:decision` entry (`greeting-injection-contract-decision`, created 2026-07-21T22:04:14Z) was explicitly deferred "post-sprint... could not run interactively during the conduct build," itself sourced from this sprint's kotest-migration masked-failure batch.
- **No later sprint has started.** `sprints/index.json`'s `active` key is still sprint-2026-07-13 as of this writing; there is no sprint-2026-07-20 or later in the registry.
- **The 2026-07-30/08-02 sessions are, functionally, the retro** — except no `retro-transcript-audit.md` was ever generated for this sprint in the nornspun repo (confirmed absent: `find /Users/steve/projects/nornspun -iname "*retro*"` lists retro artifacts for every other sprint — 04-06, 04-08, 04-10, 04-12, 05-01, 05-25, 06-18 — but none for 07-13). The formal retro workflow has not run for this sprint.

---

## 8. VERDICT

**"After sprint-2026-07-13, a user could ___ which they could not do before."**

**This sentence cannot be completed on `main`/trunk — because none of the sprint's code is on `main` in either repo.** Nothing changed about what a user can do in the shipped, running-from-trunk application, because the application a user would actually run is unchanged from before the sprint (backend) or from the prior sprint's merge (client, `sprint-2026-06-18`).

**On the sprint's own isolated INTEGRATION branch — the best-case, most charitable reading — the sentence can be partially completed but immediately fails a strict reading:** a user *could attempt* to have a session captured and durably remembered (new tables, new agent tool wiring, new client UI all present), but the sprint's own live verification found this succeeded roughly 2 times out of 7 attempts, with at least one of those "successes" persisting fabricated content unrelated to what was actually narrated. Per the mission's strictness standard ("mocked/unreachable/flag-off does not count"), a capability that fails on the majority of real attempts, verified by the sprint's own E2E process, does not meet the bar of "a user could do X." The one thing a user genuinely could rely on — that Urd's response text sometimes claims "It is written" — is actively a **regression in trustworthiness**, since it manufactures unearned confidence about a save that may not have happened.

**Both explanatory hypotheses are partially true and layered, not either/or:**
1. **Stories-not-capability, refined**: this sprint's *planning* was capability-framed and its coverage bookkeeping was rigorous — the gap is not that the plan reduced to task-completion. The gap is that **passing a story's AVFL/code-review/QA bar is not the same claim as "the capability works reliably under a real model,"** and the sprint's own E2E phase proved this by finding the keystone capability unreliable *after* all 12 stories were individually `shipped-merged`. The end-gate report's own header ("0 blocked / broken stories") actively obscures this by conflating "no story is blocked" with "the feature works."
2. **A second, independent, arguably larger gap**: **the practice has no forcing function that gets a sprint's work onto trunk and confirmed-in-the-user's-hands before the next sprint starts** — or, in this case, before 11+ days pass with the app effectively frozen mid-review. The end-gate decision step is a single unattended HTML artifact with no enforcement if the developer doesn't act on it; nothing re-prompts, expires, or blocks. The eventual "fix" that did reach `main` came 8 days later as an ungoverned, ad hoc patch — not through the practice's own gate resolution.

---

## Counter-evidence & falsifiability

Evidence that cuts against parts of this dossier's findings, stated plainly:

- **The plan itself was not the problem.** 58% of stories were genuine capability work with explicit, user-observable ACs; the roadmap and story specs are capability-framed, not task-framed. If the working hypothesis were "sprints always plan around tasks instead of capability," this sprint would be a clean counterexample at the planning layer.
- **The sprint's own quality process is not absent or theatrical.** AVFL-on-merge and E2E both ran, both found real, severe defects, and both disclosed their own coverage gaps honestly (3 of 16 validators non-responsive; harness bugs named; desktop parity marked unverified rather than silently assumed passing). This is the opposite of a rubber stamp.
- **Not all of what the developer experienced on 2026-08-02 is attributable to this sprint.** The "started from scratch" campaign complaint traces to a pre-existing gap (heroes/PC content was never persisted by any sprint, ever — 0 rows system-wide) unrelated to sprint-2026-07-13. The "agent doesn't know campaign" symptom on Android traces to stale local E2E fixture state on the test emulator, not a live code defect. Some of the "agent doesn't know campaign" symptom on desktop traces to the reviewer restarting the wrong backend build (`main`), not to a defect in the sprint's actual delivered code.
- **What would prove the "reliability, not planning" framing wrong**: if the sprint's own E2E findings (silent capture loss, fabricated content) turn out — on someone re-running Scenario A cleanly against the correct INTEGRATION backend, with the harness heredoc bug fixed — to reproduce at a much lower rate than "5 of 7," the severity of the core finding would need to be revised down substantially. This dossier did not re-run that verification; it relies entirely on the sprint's own recorded ledger findings.
- **What would prove the "nothing merged" framing wrong**: if a reader finds evidence that `sprint/sprint-2026-07-13` was merged to main via a route this dossier didn't check (e.g., a squash-merge under a different commit that lost the branch-ancestry relationship, or a deploy pipeline that builds from a non-`main` ref), the "zero capability delivered to trunk" claim would need revision. This dossier checked `git merge-base --is-ancestor` and full commit-diff in both repos directly and found no such evidence, and confirmed both repos are currently checked out on `main`.

---

## Open questions

- **What did the developer actually see in the desktop app on 2026-07-22, right after the end-gate report was rendered?** The session transcript (`2a45301c...`) cuts off mid-launch at 2026-07-22T16:38:28Z with no further record. Whether the session crashed, the developer closed it, or a continuation exists somewhere unindexed could not be determined from available transcripts.
- **Was the desktop backend actually running from the INTEGRATION worktree at any point during the 2026-07-22 evening review, before the confirmed 2026-08-02 mismatch?** Not directly confirmed either way from this dossier's evidence; inferred plausible given the desktop app launch command explicitly used the INTEGRATION client worktree at that moment, but the backend launch command in that specific window was not captured in the available transcript before it cut off.
- **Did the cross-request "context bleed" hypothesis for D6 (fabricated content appearing in live replies, not just stored rows) ever get formally investigated?** The build ledger records it as a live, unresolved working hypothesis with a suggested discriminating test (single-request-at-a-time reproduction); no evidence was found that this test was ever run.
- **Will this sprint ever be formally closed** (retro run, end-gate decision recorded, branches actually merged or explicitly abandoned)? As of 2026-08-02 the sprint sits open with no forcing mechanism visible in the tooling to resolve that state.
