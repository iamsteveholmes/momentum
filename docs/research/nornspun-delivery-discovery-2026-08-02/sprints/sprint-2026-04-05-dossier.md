# Sprint Dossier — sprint-2026-04-05

**Date compiled:** 2026-08-02
**Role:** Evidence dossier for the earliest code-build sprint in the nornspun delivery-discovery investigation — the first sprint to ship substantial backend feature code (the "D4 session loop" cluster: Verdandi agent, adventure ingestion, session recap, Urd's post-session capture, living memory).

---

## Executive summary

1. **Real code shipped, and it was substantial.** 20 commits landed on `nornspun-backend` between 2026-04-06 00:38 and 07:51 (single overnight session), covering all 5 planned stories: 3,099+2,330+2,070+562+809 lines of new source and tests across the D4.1–D4.5 stories, adding ~280 new tests. This is not a "stories passed, nothing built" sprint — it is the opposite: heavy, verifiable delivery. (git log, commit stats below.)
2. **The epic was framed as user capability, not task list.** `epics.json`'s `session-loop` epic states its acceptance condition in second person: *"A Spinner can prep an upcoming session with Verdandi... A Spinner can capture a completed session with Urd."* All 5 story files use "As a Spinner, I want X, so that Y" framing. Intent-framing was correct from the start — the gap (see below) is elsewhere.
3. **Story tracking diverged from code reality immediately, in both directions.** 4 of 5 story `.md` files still say `Status: draft` and have every Dev Agent Record field empty (`*(To be filled after implementation)*`) — despite the code being committed same-day. Conversely `stories/index.json` currently shows one of the five (`when-last-our-heroes-met-session-recap-generation`) as `backlog`, not done, even though its 12-scenario Gherkin spec was fully implemented in commit `8dd85f3`. The tracking system and the git history disagree, and neither was corrected for 4 months.
4. **The one story a later assessment reopened (`urds-post-session-capture`, D4.4) shipped a UX pattern that was later rejected — and the rejection still hasn't reached `main` today.** The April capture code included a "Shall I bind these memories to the record?" confirmation gate. ASR-006 (2026-06-16, 10 weeks later) flagged this as a live design-divergence spanning 4 files. A `sprint-2026-07-13` story revised it (`5fe8754`, merged into branch `sprint/sprint-2026-07-13`) — but **that branch is not merged into `main`** as of 2026-08-02 (`git merge-base --is-ancestor` returns false). The rejected phrase ("Shall I bind these memories to the record?" / "It is bound") is still live in `src/prompts/urd_system.md` on `main` today.
5. **The client (user-facing app) received almost none of this in the same window.** `nornspun-client` has zero commits referencing D4.1–D4.5 in the 04-05/04-06 window; the client repo's activity that week was a *different* epic (D3, client polish). Verdandi was not selectable in the app until `75afe4f` (2026-04-09, unlock-verdandi-in-client, a *later* sprint). The recap and living-memory backends had **no client surface at all**, and still didn't as of the most recent project-wide assessment (2026-06-16): *"Client has ZERO prep rendering (SurfaceType enum intentionally empty)"* / *"ZERO client ledger UI"* (ASR-006, F1/session-prep notes).
6. **A dedicated retro exists and is unusually candid** (`.momentum/sprints/sprint-2026-04-06/retro-transcript-audit.md` — folder name does not match the sprint's `started` date, see Open Questions). It reports 57/71 Gherkin scenarios passing after 8 real runtime bugs were found and fixed same-day, **and** that the developer's own manual testing immediately afterward found norn-switching broken, duplicate Urd replies, and a dead Verdandi button — bugs invisible to the passing automated suite. Those bugs were filed to backlog, not fixed in-sprint.
7. **The most authoritative later judgment on this sprint's work is ASR-006** (2026-06-16 assessment, AVFL-verified by 8 independent reviewers): *"D4.4 staging+bind infra solid (443 tests) but design-divergent"* and *"False 'done': ... `when-last-our-heroes-met-session-recap-generation` is actually `draft` with a blank dev record."* This is a project-internal, cross-checked confirmation of the tracking/reality gap found independently in this dossier.
8. **`features.json`'s own acceptance conditions for the features this sprint touched were still only "partial" as of 2026-06-16** — 10 weeks after the code landed — not because the backend was insufficient but because no client surface existed to exercise it (session-prep, session-capture, living-memory, adventure-upload all show `"status": "partial"` with explicit "ZERO client UI" language).
9. **One capability did become genuinely user-reachable within days**: Urd's chat interface pre-dated this sprint (client bootstrapped 2026-04-01, Urd unlocked from day one), so once the capture backend merged (04-06), a Spinner narrating a session to Urd through the *existing* chat UI would trigger real structured persistence — this is the strongest candidate for actual delivered functionality from this sprint (see VERDICT).
10. **Two commits with nearly identical messages both claim to "implement Urd's post-session capture (D4.4)"** (`b45ac78` then `08851b0`, 3 minutes apart) — the second only extends tests on 3 files. This looks like an AVFL/QA follow-up commit rather than duplicate work, but the identical framing in the commit message is a minor process-hygiene flag worth noting.

---

## 1. INTENT — what was this sprint for?

**Source of truth:** `docs/planning-artifacts/epics.json`, epic `session-loop`; the 5 story files in `.momentum/stories/`.

The epic this sprint drew from is explicitly framed as a user capability, not an infrastructure task:

> **Title:** "A Spinner can prep with Verdandi and capture with Urd, completing the core value loop."
> **Value analysis:** "The session loop is the primary repeating ritual that retains users. A Spinner who preps once and captures once understands the full value proposition. Everything before this epic is setup; everything after is enhancement."
> **Acceptance conditions:**
> - "A Spinner can prep an upcoming session with Verdandi, sourcing what happened last time."
> - "A Spinner can capture a completed session with Urd, persisting it into living memory."
> - "The loop is resumable and atomic — no data loss across interruptions."

(`docs/planning-artifacts/epics.json`, `session-loop` object)

Each of the 5 story files opens with a "As a Spinner... so that..." user-story block, not a task description:

- **D4.1 Verdandi:** "As a Spinner, I want to talk to Verdandi about tonight's session and feel like I'm working with a practical, capable artisan who knows my campaign, So that I can get oriented and confident before game time." (`verdandi-agent-session-prep-conversations.md:14-16`)
- **D4.2 Adventure Ingestion:** "As a Spinner, I want to upload my adventure PDF so the Norns can reference it during conversations, So that prep is grounded in the actual source material instead of generic advice." (`adventure-ingestion-feed-the-living-memory.md`)
- **D4.3 Recap:** "As a Spinner, I want Verdandi to generate a narrative recap of last session that I can read aloud to my players, So that everyone starts the session grounded in what happened." (`when-last-our-heroes-met-session-recap-generation.md:14-16`)
- **D4.4 Capture:** "As a Spinner, I want to tell Urd what happened at tonight's session through natural conversation and have her quietly close the episode into living memory..." (this is the *revised* July framing; the original April framing, preserved verbatim at the bottom of the same file, describes the same user-facing capture flow with a binding-confirmation close instead)
- **D4.5 Living Memory:** "As a Spinner, I want Verdandi's prep to automatically reflect what Urd captured after the last session, So that the prep-play-capture loop compounds in value without me manually connecting the dots." (`living-memory-the-loop-connects.md`)

**Finding:** the sprint's *stated* intent was consistently capability-level, at both the epic and story layer. This sprint is not a case of the plan itself being mis-framed as tasks — the divergence this dossier documents happened downstream of a correctly-framed plan.

---

## 2. PLAN — stories, waves, and story-type breakdown

**Sources:** `.momentum/sprints/index.json` (`completed[2]`, the entry with `started: "2026-04-05"`, `completed: "2026-04-06"`, no `slug` field — see Open Questions); `.momentum/stories/index.json`; the 5 `.feature` files in `.momentum/sprints/sprint-2026-04-05/specs/`.

5 stories, all in the `session-loop` epic, all backend-only (`nornspun-backend`), no client-side story in this sprint:

| Story | Epic | Story key | Gherkin scenarios | Current index status |
|---|---|---|---|---|
| verdandi-agent-session-prep-conversations (D4.1) | session-loop | d4-1 | 13 | `done` |
| adventure-ingestion-feed-the-living-memory (D4.2) | session-loop | d4-2 | 18 | `done` |
| when-last-our-heroes-met-session-recap-generation (D4.3) | session-loop | d4-3 | 12 | `backlog` |
| urds-post-session-capture (D4.4) | session-loop | d4-4 | 14 | `review` (was reopened/REVISEd in sprint-2026-07-13) |
| living-memory-the-loop-connects (D4.5) | session-loop | d4-5 | 14 | `done` |

Total Gherkin scenarios across the 5 `.feature` files: **71** (18+14+14+13+12), matching exactly the "71 scenarios" figure the sprint's retro reports as validated by the E2E agent — strong cross-confirmation these are the actual specs used, not a stale snapshot.

**Waves** (from `index.json`, this entry has no explicit `waves` array unlike later sprints — it lists only `stories`, `started`, `completed`, `retro_run_at`). The story `Depends On` fields imply a sequence: D4.1 (Verdandi foundation) → D4.2/D4.4 (parallel: ingestion / capture) → D4.3 (recap, depends on D4.1+D4.4) → D4.5 (living memory, depends on D4.3+D4.4). Commit timestamps (see EXECUTION) confirm this order was followed: `f2dbfd7` (D4.1, 00:38) → `70d4309`/`b45ac78`/`08851b0`/`a17bc6e` (D4.4, D4.2 tasks 1-8, 00:40–00:46) → `f9a6b59` (D4.2 tasks 9-10, 07:32) → `8dd85f3` (D4.3, 07:41) → `ce97fba` (D4.5, 07:51), followed by a run of 10 bug-fix commits through 12:04.

**Story-type breakdown:** all 5 stories are 100% product-capability stories (backend feature work directly serving the session-loop epic's user-facing acceptance conditions). **Zero** were process/tooling/refactor/test-infra stories. This sprint is a clean counter-example to any claim that early sprints were dominated by infrastructure busywork — the stated plan was pure feature delivery.

**Team composition:** this sprint predates the `team_composition.md` / per-wave team tracking convention used by later sprints — no such file exists for sprint-2026-04-05. The retro (see below) reveals the actual execution used a `momentum:sprint-dev`-style workflow that initially spawned **per-story team agents** (`dev-d4-1`, `dev-d4-2`, `dev-d4-4`, `wave1-d4-1`, `wave1-d4-2`, `wave1-d4-4`) before the developer intervened to shut most of them down as an oversized team (see EXECUTION).

---

## 3. EXECUTION — what happened during the build

**Primary source:** `.momentum/sprints/sprint-2026-04-06/retro-transcript-audit.md` (28KB; audit-extracts present: `agent-summaries.jsonl`, `errors.jsonl`, `team-messages.jsonl`, `user-messages.jsonl`, totalling ~2.3MB). Retro date 2026-04-10; sprint completed 2026-04-06 — dates match the `completed[2]` entry in `sprints/index.json` exactly, confirming this retro folder documents our sprint despite the folder-name mismatch (see Open Questions).

**Scale:** 220 user messages, 129 subagents, 595 tool errors, 451 team messages, 4 sessions, 10,405 total assistant turns, 89,441KB of transcript.

**What was built and verified, in sequence** (git-confirmed commit hashes cross-referenced against the retro's own citations):
- 8 real runtime bugs found and fixed same-day via a dev+E2E collaborative loop: datetime-timezone mismatch on POSTs (fix `6c41bc0`), tools not invoking because `end_strategy` wasn't set to `'exhaustive'` (`d6837b4`), ContentChunk field-mapping error (`2c63c5c`), `run_stream` vs `run()` preventing full tool execution (`4f89a94`), SessionEvent/NpcEncounter dict coercion (`6999d3d`), `bind_all` double-transaction bug (`086ef80`), and a `bind_recap` FK violation plus recap fabrication bug (`87d502a`). The retro: *"E2E found BUG-3 (datetime timezone mismatch on all POSTs), backend-dev fixed it in one commit (6c41bc0), E2E re-validated and found BUG-4..."* — this cycle is independently confirmed by the commit log's exact timestamps and file targets.
- Final E2E result: **57 PASS, 6 FAIL, 8 INCONCLUSIVE across 71 scenarios** (retro, "Metrics" table cross-references message 139).
- QA passed a 558-test full suite clean at one checkpoint mid-sprint (retro, "What Worked Well").
- **After** the automated cycles completed, the developer manually tested the running app (Android emulator + desktop) and found bugs invisible to the Gherkin/API-level suite: *"How do I switch to verdandi? Is it the button on the top right? When I click it nothing happens"* (message 148); *"The problem I see is that Urd repeated herself"* (message 155); *"I switched to Verdandi but it seemed to maintain the same text, output, context as Urd"* (message 156). These were **filed to the backlog, not fixed in this sprint** (retro: *"These bugs were added to the backlog (message 157)"*). Note: the "Verdandi button does nothing" observation is explained by cross-repo evidence — Verdandi was not yet unlocked in the client at this point (unlock lands 2026-04-09, a later sprint) — so a silent no-op tap, while a genuine UX gap (no "locked" affordance shown), was not itself a capture/prep regression.
- Process failure, independently confirmed by commit-message evidence: the lead initially spawned per-story team agents (`dev-d4-1`, `dev-d4-2`, `dev-d4-4`, `wave1-d4-1`, `wave1-d4-2`, `wave1-d4-4`) rather than a shared dev pool; the developer intervened: *"Okay now you've got a massive team. I think you messed this up. Shut them all down"* (message 46). 38 of 129 agents (29%) recorded zero assistant turns — largely attributable to this incident.
- Error profile: 595 total errors, dominated by `exit_code_nonzero` (424, 71%) — consistent with genuine iterative TDD (tests failing before fixes), not systemic tooling breakage, though the retro flags a suspicious uniform "19 errors per backend-dev agent" pattern as unexplained.
- Sprint scope expanded well beyond the 5 planned stories mid-session: E2E/emulator/cmux guideline creation, a BMad Builder version upgrade (which caused unexpected git changes the developer had to investigate — *"What the heck just happened to my git?"*), and UX discovery work. The retro estimates *"the actual code implementation was roughly 40% of the sprint's activity."*

---

## 4. CLAIM — what did the sprint say it delivered?

There is **no `sprint-summary.md` or end-gate report for sprint-2026-04-05** — the folder contains only the `specs/` snapshot (5 `.feature` files), no `coverage-plan.md`, `build-ledger.jsonl`, or `plan-gate-decision.md`. This sprint predates those artifact conventions; the closest thing to a completion claim is the retro's own Executive Summary, written 4 days later (2026-04-10):

> "Sprint-2026-04-06 (D3) was the project's first major code sprint — implementing D4 stories (Verdandi agent, adventure ingestion, session recap foundation) with real backend Python/FastAPI code, team-based dev/qa/e2e validation cycles, and live bug discovery. This was a dramatic shift from the prior planning sprint, producing 24+ commits of production code, discovering and fixing 8 runtime bugs... and culminating in the user manually testing the running app on Android emulator and desktop."

This claim is honest and well-hedged relative to later sprints' claims examined elsewhere in this investigation — it explicitly surfaces the manual-testing bugs and the process failures rather than only reporting the 57/71 pass rate. It does **not** claim the 5 stories delivered end-to-end user-facing functionality in the client app; it correctly scopes the claim to backend code + API-level validation + a partial manual pass.

`stories/index.json` at the time (inferred, since no historical snapshot survives) presumably marked all 5 `done` — 3 of the 5 (`verdandi-agent-session-prep-conversations`, `adventure-ingestion-feed-the-living-memory`, `living-memory-the-loop-connects`) show `done` **today**, but the story `.md` files for those same 3 still carry `Status: draft` (2 of them) or an unfilled Dev Agent Record (all 3), meaning the "done" claim in the index was never reconciled with the story files themselves — an internal consistency gap independent of anything client-side.

---

## 5. REALITY — what actually landed in the two code repos

**`nornspun-backend`** (git log, `--since="2026-04-05" --until="2026-04-08"`): 20 commits, all authored 2026-04-06 between 00:38 and 12:04 local time (single continuous overnight/morning session):

| Commit | Story | Files changed | Lines added |
|---|---|---|---|
| `f2dbfd7` | D4.1 Verdandi agent | 6 files | 809 |
| `70d4309` | fix: pre-D4.1 routing tests | — | — |
| `b45ac78` | D4.4 capture (models/migration/repo/tools/agent/tests) | 14 files | 3,099 |
| `a17bc6e` | D4.2 ingestion tasks 1-8 | 8+ files | ~600+ |
| `b77ade5` | chore: test `__init__.py` | 1 file | small |
| `08851b0` | D4.4 capture — test extension pass | 3 files | 108 |
| `f9a6b59` | D4.2 tasks 9-10 (content search tools on Verdandi) | 5 files | 562 |
| `8dd85f3` | D4.3 recap generation | 11 files | 2,330 |
| `ce97fba` | D4.5 living memory loop | 11 files | 2,070 |
| `97ab5f8`, `43d8694`, `0d974bd`, `6c41bc0`, `3deac3c`, `401f48a`, `d6837b4`, `2c63c5c`, `4f89a94`, `6999d3d`, `086ef80`, `87d502a` | Bug fixes found by E2E (BUG-3 through BUG-8) | multiple | — |

All 5 stories' acceptance-criteria-adjacent code paths (agents, prompts, tools, repos, migrations, tests) are directly traceable to a commit. This is real, substantial, tested backend delivery — verified independently of any story-tracking artifact.

**`nornspun-client`**: **zero commits** reference D4.1–D4.5 or Verdandi/capture/recap/living-memory in the 2026-04-05/04-06 window. The client repo's commits that week (`4c795ff` through `9bd01ce`, 2026-04-06 through 04-09) are exclusively D3-epic client-polish work (norn switching, conversation persistence, fonts, accessibility, window sizing) — a different epic entirely. Verdandi is not unlocked in the client until `75afe4f` (2026-04-09) and adventure-upload UI lands the same day (`a39fac0`) — **3 days after** this sprint, in what `sprints/index.json` records as the separate `sprint-2026-04-08` (`planned: "2026-04-09"`, `started: "2026-04-08"`).

**Consequence:** for the 4 of 5 stories that depend on Verdandi being reachable in the client (D4.1, D4.2's tool-registration half, D4.3, D4.5), **no user could exercise the new capability through the app until sprint-2026-04-08 landed**, 3 days later. Only D4.4 (Urd's capture) sat behind an agent that was already unlocked in the client from day one (see VERDICT).

---

## 6. AFTERMATH — did this sprint's work survive, get revised, or get reverted?

**`when-last-our-heroes-met-session-recap-generation` (D4.3):** code shipped (`8dd85f3`, 2,330 lines, 57 tests per the commit message), but the story file was never updated post-implementation — `Status: draft`, all tasks unchecked `[ ]`, every Dev Agent Record field `*(empty — populated after implementation)*`. `stories/index.json` currently (2026-08-02) shows this story as `backlog`. **ASR-006 (2026-06-16) independently caught this exact gap**: *"False 'done': session-prep's `when-last-our-heroes-met-session-recap-generation` is actually `draft` with a blank dev record (`features.json` still counts it in `stories_done: 3`)"* (ASR-006 §F3, line 54). This is a project-internal, AVFL-verified (8 independent reviewers) confirmation of the same divergence found independently here.

**`urds-post-session-capture` (D4.4):** the strongest aftermath story of the sprint. The original April implementation (443 tests, real DB schema, atomic `bind_all` transaction) is confirmed **still structurally intact** — `002_create_session_tables.py` and its downstream migrations (003–006) are all present in `alembic/versions/` today, and `src/tools/memory.py`'s history shows no reverts. But the *design* shipped with it — a "Shall I bind these memories to the record?" confirmation gate before persistence, with the closing line "It is bound" — was later rejected. ASR-006 (2026-06-16): *"The binding-ritual 'Shall I bind…' gate survives in 4 locations... and is encoded in the D4.3 story spec (AC + DoD). Removing it is a multi-file change plus a story-spec revision — not a quick win."* (§F4). The story was reopened as a REVISE in sprint-2026-07-13 (story file rewritten 2026-07-13, "Not yet implemented in code" per its own Dev Agent Record at reopen time), and **was** implemented — commit `5fe8754` ("strip binding-confirmation gate — two-message close with 'It is written.' receipt") exists, merged into branch `sprint/sprint-2026-07-13` (merge commit `aab6add`). **However, as of 2026-08-02, that branch is not merged into `main`**: `git merge-base --is-ancestor sprint/sprint-2026-07-13 main` returns false, and `main`'s current `src/prompts/urd_system.md` still contains the literal rejected phrases — line 417: `Ask: "Shall I bind these memories to the record?"`; line 419: `Respond: "It is bound."` The corresponding test (`tests/agents/test_urd_capture.py:153-156`) still asserts these exact phrases must be present. **The rejected UX pattern from this April sprint is still live in the actual codebase four months later, despite a completed fix sitting on an unmerged branch.**

**`adventure-ingestion-feed-the-living-memory` (D4.2) / `verdandi-agent-session-prep-conversations` (D4.1) / `living-memory-the-loop-connects` (D4.5):** all show `done` in `stories/index.json` today and their backend code is present and untouched by reverts. But per ASR-006, the *feature-level* acceptance conditions these stories were meant to serve remained only "partial" as of 2026-06-16 (10 weeks later) — not due to backend defects but because the client never got a surface: *"Client has ZERO prep rendering (SurfaceType enum intentionally empty)"* (session-prep feature notes); *"ZERO client ledger UI (ToolSurface base exists; ledger composable does not)"* (living-memory feature notes); adventure-upload is *"done" but desktop is an unwired TODO* (only Android got the file-picker UI, in the 04-08 sprint — desktop upload remained a backlog stub, `adventure-upload-desktop`, as of 2026-06-16).

**Downstream story creation confirms the gap was never closed quickly:** `client-when-last-our-heroes-met-recap-surface` (a dedicated client UI for the D4.3 recap) was not even captured into the backlog until **2026-07-06** — three months after the backend shipped — and remains `status: backlog` today (2026-08-02).

---

## 7. VERDICT

*"After sprint-2026-04-05, a user could ___ which they could not do before."*

**The strongest defensible completion: "...narrate what happened in a completed session to Urd, in the same chat interface the Spinner was already using, and have that session's events, NPC encounters, and divergences durably persisted to a real Postgres database — instead of that information vanishing when the conversation ended."**

This is defensible because:
- Urd's chat interface was live in the client from the very first client commit (2026-04-01), unconditionally — no unlock gate applied to Urd.
- Campaign creation via Urd conversation had already shipped weeks earlier (`448b480`, 2026-03-27) — a Spinner could already have a campaign to attach a session to.
- The capture backend (D4.4) merged same-day (`b45ac78`/`08851b0`, 2026-04-06 00:43-00:46) with a real schema, atomic transaction, and 5 registered tools — not a stub.
- The 8 same-day bug fixes (timezone, `end_strategy`, FK violations) indicate the developer actually exercised this path live and found it working end-to-end well enough to fix real bugs in it, not merely unit-tested in isolation.

**What does NOT clear the "user could do X" bar, and why:**
- Talking to **Verdandi** about anything (session prep, recap, adventure content, living memory) required the client unlock that didn't land until 3 days later (sprint-2026-04-08) — so D4.1, D4.3, D4.5, and half of D4.2 were **not reachable by any user through the app** at the close of this sprint.
- The session capture UX that *was* reachable shipped with a confirmation-gate pattern ("Shall I bind these memories to the record?") that was later formally rejected by the product owner (per ASR-006) as inconsistent with the intended "continuous, ambient" capture design — meaning even the one capability that *was* immediately usable was, by the project's own later judgment, delivering the wrong experience.
- Recap generation and living-memory querying had a working backend within a day, but **no user could ever see a rendered recap or a living-memory ledger in the app** — as of the most recent whole-project assessment (2026-06-16, 10 weeks after this sprint), those client surfaces literally did not exist ("SurfaceType enum intentionally empty").

**Net verdict:** this sprint shipped real, tested, non-trivial backend functionality precisely as scoped — a genuine counter-example to "stories pass, nothing works" taken as a blanket claim. But the functionality a user could *actually reach through the running app* at sprint-close was narrower than "5 stories done" implies (1 of 5 immediately, the rest gated 3 days later on a different sprint), and even that one reachable capability shipped a UX pattern later reversed — a reversal that, 4 months on, has been coded but not yet merged to `main`.

---

## Counter-evidence & falsifiability

Evidence that cuts against the "sprints ship stories, not functionality" framing, specific to this sprint:

- **This sprint's own retro is unusually rigorous and self-critical** — it explicitly reports the gap between automated pass rate (57/71) and manual-test reality (norn-switch broken, duplicate replies) in the same document, rather than only celebrating the pass rate. If sprints systematically hid this gap, we would not expect the retro itself to surface it this clearly, four sprints before the practice's later, more formalized retro-audit tooling existed.
- **All 5 stories' backend code is real, extensive, and tested** (280+ new tests across the 5 commits), and none of it has been reverted — it remains the load-bearing foundation that later sprints (including the July 13 sprint) build directly on top of (e.g., `Already-Built Foundation... must NOT be rebuilt` in the `urds-post-session-capture` REVISE story). This is evidence of durable, compounding delivery, not wasted work.
- **The 3-day gap to client-unlock is short**, not indefinite — sprint-2026-04-08 (the very next tracked sprint) closed most of the backend/client gap for Verdandi and adventure upload within days, suggesting the practice was, at this early stage, reasonably good at sequencing backend-then-client work across adjacent sprints rather than leaving it open indefinitely.
- **What would prove this dossier wrong:** if a session transcript or commit could be found showing the client actually calling the recap/living-memory endpoints through some interim mechanism (a curl-based manual smoke test the developer ran, or a debug UI) before the 06-16 assessment, that would mean the "ZERO client UI" framing in ASR-006 overstates the gap. I searched `nornspun-client` git log for any commit referencing `recap`, `living memory`, or `session_recap` before 2026-06-16 and found none in the window checked (04-01 through 04-10); a fuller scan of the entire April–June client history was not performed and could surface an interim manual test path this dossier missed.

## Open questions

- **Sprint slug/folder-name mismatch, unresolved.** `sprints/index.json`'s `completed` entry for this sprint has **no `slug` field** at all (every other entry does); its `started`/`completed` dates (2026-04-05/04-06) match the task brief's "sprint-2026-04-05" naming. But the only retro/specs folder with matching dates and matching story content is named `.momentum/sprints/sprint-2026-04-06/` — one day off, and that same folder's `specs/` directory contains 11 **D3 client-story** `.feature` files (onboarding-cta-visibility, norn-switch-clears-chat, etc.) that belong to the *next* sprint (`sprint-2026-04-08`) rather than this one's 5 D4 stories. I could not determine whether this is a single mis-filed artifact, two sprints' retro material merged into one folder by an early, less mature version of the retro tooling, or an intentional combined retro covering both 04-05 and 04-08. This dossier used the retro's *body text* (which explicitly discusses D4.1/D4.2/D4.4 by name and reports "71 scenarios," matching this sprint's 71 Gherkin scenarios exactly) as the basis for attributing it to this sprint, while flagging the folder-level ambiguity here rather than silently resolving it.
- **Whether the 8 same-day bug fixes were themselves later re-broken** was not checked beyond confirming the fix commits exist; a full regression check against the current `main` HEAD for each of the 8 specific bugs (timezone handling, `end_strategy`, FK constraints, etc.) was out of scope for this pass.
- **Why 4 story `.md` files were left with empty Dev Agent Records / stale `Status: draft` headers for 4 months** — whether this is a one-time tooling gap from before the practice enforced a "close the loop" step, or a recurring pattern — is a question for the cross-sprint synthesis, not answerable from this sprint's evidence alone.
- **Whether the developer ever actually exercised the D4.4 capture path live via the app in this window**, versus the 8 bug fixes being found through the E2E agent's automated harness alone (not manual chat use) — the retro attributes the 8 bugs to the "dev-e2e collaborative bug fix loop," which appears to be automated/API-level, not the developer's own manual test (that came later, and found *different* bugs). This softens the VERDICT's confidence that a human specifically experienced working capture in this exact sprint window, though the code path is confirmed functional against the automated harness.
