# Sprint Dossier — sprint-2026-04-06

**Date compiled:** 2026-08-02
**Role:** Evidence dossier for one sprint (nornspun's first major code sprint) within the "why doesn't anything work end-to-end" discovery investigation.

---

## Executive Summary

1. **Sprint-2026-04-06 was a 100%-backend sprint** — 5 stories (D4.1–D4.5: Verdandi agent, adventure ingestion, session recap generation, Urd's post-session capture, living-memory loop-connect), all in `nornspun-backend`, zero client-side stories in scope. Confirmed by `.momentum/sprints/index.json` (stories list has no client story) and by `nornspun-client` git log for 2026-04-04→04-12 showing zero D4-related commits.
2. **The code genuinely landed and was genuinely tested.** 7 commits, ~2,330+ lines in the recap commit alone, 443 tests for capture, 57/71 (80%) Gherkin scenarios passing after a real dev↔E2E bug-fix loop (8 runtime bugs found and fixed live). This was not a "fake done" sprint in the shallow sense — it is the retro's own "gold standard" example of team-based validation.
3. **The developer said it himself, same day:** *"When do we work on ios? When do I get to see the stuff that's implemented in the backend?"* and *"I thought D4 didn't give us any UI"* (2026-04-06, 19:09 UTC, session `7f4a255a…`). The gap between story-complete and user-usable was visible and named in real time — not a retrospective realization.
4. **~23 minutes later, in a separate session, the developer manually tested the app and found bugs** (Verdandi pip unresponsive, Urd repeating herself, norn-switch context bleed). These bugs are almost certainly **pre-existing client behavior from an earlier client epic** (the Norn selector UI shipped before this sprint; Verdandi's own client unlock didn't land until sprint-2026-04-08), not anything this sprint touched — the retro's "What Worked Well" write-up credits this testing episode as validating *this sprint's* work, which the evidence does not support.
5. **Two-plus months later, an independent assessment (ASR-006, 2026-06-16) reclassified the sprint's "done" work as design-divergent and partly false-done:** the recap-generation story (D4.3) is "actually `draft` with a blank dev record" despite `features.json` counting it as shipped; the capture story (D4.4) has "solid infra (443 tests) but is design-divergent" because its core UX mechanic (the "Shall I bind these memories?" confirmation gate) was later rejected by product design; living-memory has "Store A absent; zero client ledger UI."
6. **As of today (2026-08-02), the client-facing surfaces that would let a user see any of this sprint's work still do not exist.** `client-when-last-our-heroes-met-recap-surface`, `client-tonight-prep-ledger-surface`, and `backend-prep-ledger-assembly-model` are all `status: backlog` in the current story index.
7. **The capture story was finally revised in sprint-2026-07-13** (the sprint whose broken end-user experience triggered this whole investigation) — and its own build ledger records the revision **still doesn't work**: "SILENT CAPTURE LOSS... ~5 of 7 live closes produced the receipt with zero DB rows" and "FABRICATED CAPTURE CONTENT: persisted session row contains an entirely different adventure's narrative than the one narrated." Three and a half months after D4.4 first shipped, session capture is still not reliably functional.
8. **The sprint's own retro (retro-transcript-audit.md) correctly diagnosed structural process problems** (oversized team, 29% zero-turn agents, E2E initially read source instead of running black-box tests) but its "What Worked Well" section frames the sprint's story completion and E2E pass rate as success without noting that none of it was reachable by a user — the retro measured process health, not capability delivery.
9. **Data-integrity anomaly (does not change the above):** the `specs/` snapshot under `.momentum/sprints/sprint-2026-04-06/specs/` contains 11 Gherkin `.feature` files for unrelated UI stories (norn-switch, norn-pip, onboarding-cta, etc.) that belong to a different sprint window, not the 5 backend stories this sprint actually built. This was introduced by a later archival migration (commit `8bb9e15`, 2026-05-03) and is a bookkeeping error, not evidence about what was built. I relied on `.momentum/sprints/index.json` + git history + `retro-transcript-audit.md` (all three agree) as ground truth instead.
10. **INTENT was capability-framed at the epic level** ("A Spinner can prep with Verdandi and capture with Urd, completing the core value loop" — `epics.json`, `session-loop`), and each story used standard "As a Spinner, I want X, so that Y" framing. But the sprint's actual *scope selection* made end-to-end delivery structurally impossible from the start: with zero client stories in the wave plan, there was no way this sprint could produce a user-observable capability regardless of execution quality.

---

## 1. INTENT — What was this sprint for?

**No `coverage-plan.md` or `plan-gate-decision.md` exists for this sprint** — these artifact types postdate it; the practice's own tooling matured after sprint-2026-04-06. The intent has to be reconstructed from the epic definition, the story specs, and the in-session sprint-planning conversation (captured only in `audit-extracts/user-messages.jsonl`, no separate handoff doc survives).

**Epic-level framing** (`docs/planning-artifacts/epics.json`, `session-loop` epic — the epic all 5 of this sprint's stories belong to):
> `"title": "A Spinner can prep with Verdandi and capture with Urd, completing the core value loop."`
> `"value_analysis": "The session loop is the primary repeating ritual that retains users. A Spinner who preps once and captures once understands the full value proposition. Everything before this epic is setup; everything after is enhancement."`

This is unambiguously a **USER CAPABILITY** framing, not a task/infrastructure framing.

**Story-level framing** — each of the 5 stories opens with the standard user-story template. Example, `verdandi-agent-session-prep-conversations.md`:
> "As a Spinner, I want Verdandi to help me prepare an upcoming session..."

So individually, every story *reads* as capability-oriented. The disconnect is not in how the stories were worded — it's in what was selected into this sprint's wave plan. The sprint-planning conversation (`audit-extracts/user-messages.jsonl`, msg indices ~9–19) shows the developer walking through backlog triage and getting lost in a technical storage tangent ("Woof I'm getting lost… Where does all this get stored?"), then approving a plan that turned out to be **5 backend-only stories** with **no corresponding client story** to expose any of them. Nothing in the transcript shows the developer being told "this sprint will not be visible in the app when it's done" — the capability framing at the story level created an expectation the wave plan didn't fulfill.

**Sprint composition per `.momentum/sprints/index.json`:**
```
"stories": [
  "verdandi-agent-session-prep-conversations",       (D4.1, backend)
  "adventure-ingestion-feed-the-living-memory",       (D4.2, backend)
  "when-last-our-heroes-met-session-recap-generation",(D4.3, backend)
  "urds-post-session-capture",                        (D4.4, backend)
  "living-memory-the-loop-connects"                   (D4.5, backend)
]
```
All touch only `nornspun-backend` files (`src/agents/`, `src/tools/`, `src/data/repositories/`, `src/models/`, `alembic/versions/`). Verified against `nornspun-client` git log for 2026-04-04→04-12 (below) — zero overlap.

---

## 2. PLAN — Stories, waves, team composition, product-capability fraction

**Waves** (`.momentum/sprints/index.json`):
- **Wave 1:** `verdandi-agent-session-prep-conversations`, `adventure-ingestion-feed-the-living-memory` [tasks 1–8], `urds-post-session-capture`
- **Wave 2a:** `adventure-ingestion-feed-the-living-memory` [tasks 9–10], `when-last-our-heroes-met-session-recap-generation`
- **Wave 2b:** `living-memory-the-loop-connects` (depends on 2a's two stories both merging first)

Sequencing notes cite genuine technical coupling (shared files: `verdandi.py`, `verdandi_system.md`, `session.py`, `session_repo.py`, `memory.py`) — the wave structure itself was sound engineering sequencing, not busywork.

**Product-capability vs. process/infra fraction:** **5 of 5 stories (100%) are backend product-capability stories** by story-template standards (all are "As a Spinner, I want X" features, not refactors or test-infra). By that narrow measure this was a *maximally* product-focused sprint. The gap is not story-type composition — it's platform coverage: **0 of 5 touch the client**, so "product capability" here means "capability a backend engineer can verify with `curl`/pytest," not "capability a Spinner can use."

**Team composition:** No `team-composition.md` survives (predates that artifact). Reconstructed from the retro and transcripts: the lead initially spawned an oversized, per-story team (`dev-d4-1`, `dev-d4-2`, `dev-d4-4`, `wave1-d4-1`, `wave1-d4-2`, `wave1-d4-4` — 6+ agent types for what should have been 2–3 shared roles), which the developer ordered shut down mid-sprint ("Okay now you've got a massive team. I think you messed this up. Shut them all down." — `retro-transcript-audit.md` msg 46 citation). The sprint then converged on a **dev + QA + E2E team-cycle pattern** (TeamCreate-based) that the retro calls "the gold standard for team-based code validation" — 6 fix→validate iterations in ~40 minutes, closing BUG-3 through BUG-8.

**Data-integrity note on the specs snapshot:** `.momentum/sprints/sprint-2026-04-06/specs/` contains 11 `.feature` files (`accessibility-labels-content-descriptions`, `back-button-navigation-safety`, `bundle-custom-fonts-source-sans-3-and-cinzel`, `client-conversation-history-persistence`, `desktop-window-sizing-and-scroll`, `fix-skuld-pip-touch-target`, `norn-greeting-on-first-entry`, `norn-pip-discoverability-and-locked-state`, `norn-switch-clears-chat-and-maintains-session`, `onboarding-cta-visibility`, `speaker-attribution-and-message-styling`) — **none of which match the 5 D4 stories this sprint actually shipped.** 5 of the 11 filenames match stories that belong to `sprint-2026-04-08` (the next sprint, a client UI-polish sprint), but file contents differ from `sprint-2026-04-08/specs/`'s versions of the same filenames (`diff -rq` confirms both same-named-but-different-content and files unique to each side) — so this isn't simply "the two sprints share a specs folder," it's a corrupted/wrong snapshot. All files in both `sprint-2026-04-06/specs/` and `sprint-2026-04-08/specs/` carry the identical mtime `May 26 11:27`, and `git log` shows they were introduced in a single bulk commit, `8bb9e15 chore(momentum): migrate stories and sprints to .momentum/` (2026-05-03) — a later archival migration, not anything from the sprint itself. **I did not use this specs/ directory as evidence for this dossier's PLAN or REALITY sections** — `.momentum/sprints/index.json`, the story files in `.momentum/stories/`, and `nornspun-backend` git history are mutually consistent and used instead.

---

## 3. EXECUTION — What happened during the build

Source: `retro-transcript-audit.md` (comprehensive, written 2026-04-10) cross-checked against `audit-extracts/user-messages.jsonl` (220 lines) and `nornspun-backend` git log.

**Scale:** 4 sessions, 129 subagents, 10,405 total assistant turns, 89,441 KB transcript size, 595 tool errors, 451 team messages.

**What worked:**
- **Dev↔E2E bug-fix loop** — E2E ran the 71 Gherkin scenarios as real black-box tests (after the developer forced a correction — see below), found BUG-3 through BUG-8 (datetime timezone mismatch, missing `end_strategy` blocking tool calls, `ContentChunk` field-mapping bug, `run_stream` vs `run()` preventing multi-tool completion, FK violation on recap bind, fabricated recap content), and backend-dev fixed each within the same session. Final report: **57 PASS / 6 FAIL / 8 INCONCLUSIVE across 71 scenarios** (`audit-extracts/user-messages.jsonl` line 152, teammate `e2e`, "Final E2E validation report after all fixes").
- QA gate passed 5 fixes with one advisory; 558-test full suite ran clean at that checkpoint.

**What struggled (all from `retro-transcript-audit.md`, cross-checked against transcripts):**
- **Oversized team required emergency shutdown** — lead spawned 6+ per-story agent types instead of a shared 2–3-agent pool; developer intervened directly ("Shut them all down").
- **38 of 129 agents (29%) had zero assistant turns** — pure spawn waste.
- **E2E initially read source code instead of running the app** — developer caught this explicitly: *"I thought we had ABSOLUTE blocking of the E2E validator from reading source code."* This forced an unplanned detour (msgs ~71–91, ~2.5 hours) to write cmux/emulator/E2E black-box guidelines before validation could be trusted.
- **Exit-code errors dominated (424/595, 71%)** — expected for iterative dev, but a suspiciously uniform "19 errors per backend-dev agent" pattern was flagged as INVESTIGATE, never root-caused within this sprint.
- **Idle-notification spam** — 451 team messages, a large fraction pure keepalive noise.
- Sprint scope expanded mid-flight to include E2E guideline creation, emulator guideline creation, a BMad Builder upgrade (which caused an unexplained git state change the developer had to ask about), and next-sprint planning — the retro estimates **actual D4 code implementation was ~40% of the sprint's total activity.**

**The capability-visibility gap surfaced live, not just in retrospect.** Two direct developer quotes from the raw transcript, both on 2026-04-06:
- 19:09 (`audit-extracts/user-messages.jsonl` line 154, session `7f4a255a-7093-4c8f-9907-72e9c8314e60.jsonl`): *"When do we work on ios? When do I get to see the stuff that's implemented in the backend?"*
- Immediately after (line 155, same session): *"I thought D4 didn't give us any UI"*

~23 minutes later, in a **different** session (`ca243db3-c190-4dbf-969f-31bfc750d474.jsonl`, 19:32–20:06), the developer manually tested the running app and reported:
- 19:32: *"How do I switch to verdandi? Is it the button on the top right? WHen I click it nothing happens"*
- 20:04: *"That's not the problem. The problem I see is that Urd repeated herself. I did not switch to Verdandi yet"*
- 20:06: *"I switched to Verdandi but it seemed to maintain the same text, output, context as Urd"*

**These two episodes are in tension, and the second is very likely testing pre-existing client behavior, not this sprint's output.** The Norn selector UI (the pip row including a Verdandi button) shipped in an earlier client epic — `norn-selector-and-ratatoskr-first-launch` is `status: done` in `.momentum/stories/index.json`, touching `NornSelector.kt`, predating this sprint. Verdandi's client-side *unlock* (making the pip tappable/functional rather than a locked placeholder) is a **separate, later** story, `unlock-verdandi-in-client`, which landed in `nornspun-client` as commit `75afe4f` — part of **sprint-2026-04-08**, not this sprint. Given this sprint touched zero client files, the Verdandi-pip-does-nothing and norn-switch-context-bleed bugs the developer found by hand almost certainly pre-existed this sprint and were incidentally discovered while the developer looked for something — anything — to test after being told there was nothing new to see. **`retro-transcript-audit.md`'s "What Worked Well" section ("User manual testing found real UX bugs not caught by automated validation," citing this same episode) credits this testing as validating the sprint's own work; the timeline evidence does not support that framing** — it looks more like the developer testing the wrong thing because there was nothing right to test.

---

## 4. CLAIM — What did the sprint claim at completion?

**No `sprint-summary.md` or end-gate report survives for this sprint** (both artifact types postdate it). The closest thing to a completion claim is:
1. The E2E validator's final report (57/71 PASS, quoted above) — a **test-scenario claim**, scoped to API-level Gherkin behavior, not a user-capability claim.
2. `.momentum/sprints/index.json`'s terminal state: `"status": "done"`, `"completed": "2026-04-06"`.
3. `.momentum/stories/index.json` marking 3 of the 5 stories `status: done` (`verdandi-agent-session-prep-conversations`, `adventure-ingestion-feed-the-living-memory`, `living-memory-the-loop-connects`) at some point after the sprint — though `when-last-our-heroes-met-session-recap-generation` is `status: backlog` in the *current* index (see §6, this was later re-opened/found incomplete) and `urds-post-session-capture` is `status: review` with a `(REVISE)` title (also §6).

No artifact from this sprint asserts "a Spinner can now prep or capture" — the claim, such as it is, is scoped entirely to backend test-passing, consistent with the sprint's actual (backend-only) scope.

---

## 5. REALITY — What actually landed (git evidence)

**`nornspun-backend`**, all 2026-04-06, same calendar day as planning:
```
f2dbfd7 07:38:23 -0700  feat(agents): implement Verdandi agent — session prep conversations (D4.1)
70d4309 (same window) fix(tests): update pre-D4.1 routing tests for live Verdandi agent
b45ac78 00:43:27 -0700  feat(capture): implement Urd's post-session capture with living memory (D4.4)
a17bc6e 00:44:29 -0700  feat(ingestion): implement D4.2 adventure ingestion — Tasks 1-8
08851b0 00:46:41 -0700  feat(capture): implement D4.4 Urd's post-session capture — living memory data layer
f9a6b59 (same window) feat(agents): register adventure content tools on Verdandi (D4.2 tasks 9-10)
8dd85f3 07:41:47 -0700  feat(recap): implement session recap generation — "When Last Our Heroes Met" (D4.3)
   — 2,330 insertions across 11 files, 57 new tests (verified via `git show --stat`)
ce97fba 07:51:44 -0700  feat(memory): implement living memory loop — the loop connects (D4.5)
87d502a 12:04:29 -0700  fix(agents): resolve bind_recap FK violation and recap fabrication
+ 9 more `fix(*)` commits same day resolving BUG-3 through BUG-8 (datetime tz, end_strategy,
  ContentChunk mapping, run_stream vs run(), reserved logging attrs, transaction nesting)
```
This is real, substantial, tested backend code — not a stub. Confirmed independently by `git show --stat`.

**`nornspun-client`**, 2026-04-04 → 04-12 (the surrounding window): **24 commits, all unrelated to D4.** Titles: `NornPip` sizing, CTA-visibility contract tests, accessibility-label tests, window-sizing tests, Material 2→3 migration, campaign-UUID wiring, `unlock-verdandi-in-client`, adventure-upload file picker. These are the sprint-2026-04-08 stories (confirmed against that sprint's `stories` list in `index.json`). **Zero client commits reference D4, Verdandi's session-prep behavior, recap rendering, or Urd's capture flow.**

**Did the landed code change what a user could DO?** No. Immediately after this sprint closed (2026-04-06), a Spinner using the app could do exactly what they could do before it — the entire delta is server-side and reachable only via direct API calls (`curl`, pytest), which is how the E2E validator itself verified the 57/71 pass rate.

---

## 6. AFTERMATH — Did this sprint's stories get dropped, reverted, or reopened?

This is the richest section of evidence, and it directly answers the mission's central question.

**`docs/assessments/asr-006-design-to-implementation-reconciliation-2026-06-16.md`** (an independent, AVFL-verified assessment, ~2.5 months after this sprint) re-examined every "done" claim in `features.json` against actual code and design state. Direct findings about this sprint's stories:

> **F3** — "`features.json` is systematically stale and partly fictional... **False 'done':** session-prep's `when-last-our-heroes-met-session-recap-generation` is actually `draft` with a blank dev record (`features.json` still counts it in `stories_done: 3`)."

> **F4** — "The binding-ritual 'Shall I bind…' gate survives in 4 locations — `urd_system.md`... `verdandi_system.md`... `verdandi.py`, `memory.py` — **and is encoded in the D4.3 story spec (AC + DoD).** Removing it is a multi-file change plus a story-spec revision — not a quick win."

> Session-capture section: "**Build reality:** D4.4 staging+bind infra solid (443 tests) but **design-divergent**... **REVISE:** `urds-post-session-capture` — strip the AC5 binding-ritual gate; add session naming + two-message close... the binding-ritual UI ritual is rejected by the **2026-06-16 hi-fi design** (no SDR uses the term 'binding ritual')."

> Living-memory section: "**Build reality:** Store B done; **Store A absent**; **zero client ledger UI**."

**`.momentum/features.json`, live entries (read 2026-08-02), corroborate ASR-006's conclusions and are still current:**
- `session-prep` feature: `"notes": "...Client has ZERO prep rendering (SurfaceType enum intentionally empty)."`
- `session-capture` feature: `"notes": "...urds-post-session-capture (D4.4) infra built (443 tests) but DESIGN-DIVERGENT."`
- `adventure-upload` feature: backend pipeline (D4.2) marked done, but "'working' was overstated: ... desktop ABSENT (MainWindow.kt TODO — no JFileChooser)."
- `living-memory` feature: "Store A (episodic transcript) ABSENT — the keystone unblock... ZERO client ledger UI."

**Story-status drift confirms this in the tracker itself.** `.momentum/stories/index.json` (current, 2026-08-02):
- `when-last-our-heroes-met-session-recap-generation` → `status: backlog` (was counted as one of this sprint's completed stories in `sprints/index.json`, but is now back in the backlog — i.e., the sprint's own claim that this shipped did not hold up).
- `urds-post-session-capture` → `status: review`, title now carries `(REVISE — strip binding gate, align to two-message close)`. The story file's own preamble states: *"This is a REVISION of an already-implemented story. The full post-session capture feature (D4.4) shipped on `nornspun-backend/main`... The database schema, repositories, staging tools, and the atomic `bind_memories` transaction are built and working... This revision's scope is a narrow delta: remove the rejected 'Shall I bind these memories to the record?' confirmation gate."*
- The client stories that would actually **expose** any of D4's backend work — `client-when-last-our-heroes-met-recap-surface`, `client-tonight-prep-ledger-surface`, `backend-prep-ledger-assembly-model` — are **all `status: backlog`**, four months after D4 shipped.
- `binding-ritual-context-summarization` (the story that was going to build the confirmation-gate UI D4.4's backend was built to support) is `status: dropped`.

**The revision was finally attempted in sprint-2026-07-13** — the sprint that triggered this entire discovery investigation. Per that sprint's `build-ledger.jsonl`:
- `urds-post-session-capture` (REVISE) was built and merged (2026-07-21, commit `5fe8754 feat(urds-post-session-capture): strip binding-confirmation gate`).
- But E2E/AVFL validation during that same sprint found the revision **still doesn't reliably work**:
  > `coverage-deferral-undischarged`, severity `major`: "AC3 durable persistence FAILS — fresh conversation reports no sessions after confident close; DB count 0 confirms."
  > `avfl-finding`, severity `critical`, id `discharge-stakes-capture-receipt-1`: **"SILENT CAPTURE LOSS: Urd narrates 'It is written.'... without the underlying `bind_memories` tool call executing — ~5 of 7 live closes produced the receipt with zero DB rows and zero logged errors."**
  > `e2e-stakes-escalation`, id `e2e-capture-integrity-1`: **"FABRICATED CAPTURE CONTENT: persisted session row contains an entirely different adventure's narrative than the one narrated... stored as session_number 0... with no mismatch signal anywhere in the flow."**

So: the feature this sprint (2026-04-06) built — Urd's post-session capture — was reclassified as design-divergent two months later, revised three and a half months later, and **as of the revision's own validation, still silently loses or corrupts what a GM tells it roughly 5 times out of 7.** This is not a UI-visibility gap anymore at this point — it's a core data-integrity defect in the write path, still open as of the most recent sprint this investigation covers.

---

## 7. VERDICT

> **"After sprint-2026-04-06, a user could ___ which they could not do before."**

**This sentence cannot be completed with anything a real user could observe.** Strictly:

- The sprint shipped zero client-facing code (§5) — nothing changed about what a Spinner could see, tap, or read in the app.
- The one thing a technically-inclined observer *could* newly do — call the backend API directly and get Verdandi/Urd/recap/living-memory behavior — fails the mission's evaluation standard ("mocked/unreachable/flag-off does not count") on reachability grounds: it required bypassing the client entirely.
- Even judged purely as backend capability with a hypothetical future client, the capability was itself wrong: ASR-006 (2.5 months later) found the capture story's core UX mechanic design-divergent, and the July revision of that same story is still measurably broken (silent data loss ~5/7 of the time, fabricated content in the remaining cases).

**The honest completion of the sentence is:** *After sprint-2026-04-06, a developer could exercise new Verdandi/Urd/recap/living-memory behavior via direct backend API calls and automated Gherkin scenarios (57/71 passing) — but a Spinner using the actual app could do nothing differently, and the one feature in this batch that did eventually get a UX revision (session capture) is still not reliably capturing data as of the most recent sprint on record (2026-07-13).*

---

## Counter-evidence & falsifiability

Evidence that cuts against, or complicates, the findings above:

- **This was not a "fake done" sprint by the shallow definition.** 443+57+other tests were real, ran, and the dev↔E2E loop found and fixed 8 genuine runtime bugs through live iteration — a materially higher execution-quality bar than a rubber-stamped sprint. If the working hypothesis were "agents fabricate passing status," this sprint would be strong counter-evidence: the retro explicitly documents real bugs being found and really fixed.
- **The epic and story framing were capability-oriented**, not task-oriented — so if the hypothesis is "the practice writes tasks, not capabilities," this sprint's specs contradict that at the wording level. The failure here is in wave/scope selection (an all-backend wave with no client counterpart), not in how stories were written.
- **The developer *did* notice the gap in real time** ("I thought D4 didn't give us any UI") — so this is not solely a blind spot that only surfaced at retro or in a later assessment; the practice had a live opportunity to course-correct mid-sprint and the sprint continued to close as "done" anyway.
- **What would prove this dossier wrong:** if a `nornspun-client` commit between 2026-04-06 and 2026-04-08 could be found that wires any D4 backend endpoint into a rendered screen, the "zero client capability" claim would be falsified. I checked via `git log --since=2026-04-04 --until=2026-04-12 --oneline --all` in `nornspun-client` and found none; a wider window search would strengthen or falsify this further.
- **The retro-transcript-audit.md's framing is not fabricated** — it accurately describes the process events (team-size incident, E2E source-reading bug, manual testing episode) — my disagreement is narrower: it credits the manual-testing episode as validating *this sprint's* work, when the timeline (different session, 23 minutes after "I thought D4 didn't give us any UI," bugs in a pre-existing client component) suggests the developer was testing something else.

## Open questions

- **Exact retro message-numbering scheme is unclear.** `retro-transcript-audit.md` cites "message 148," "message 46," etc., but these numbers do not correspond 1:1 to line positions in `audit-extracts/user-messages.jsonl` as extracted for this dossier (e.g., the audit's "message 148" quote appears at line 164 in my extraction, in a different session file than line 154). I could not determine whether the retro used a merged, differently-filtered, or differently-indexed transcript. This doesn't change any conclusion here (I cite by content, timestamp, and session file instead of message number) but means a reader cross-referencing this dossier against the retro by message number should expect an offset.
- **Whether the developer was told, before or during sprint planning, that this sprint would be backend-only and invisible in the app.** The surviving transcript starts mid-triage (technical-storage confusion) and I could not find an explicit "heads up, nothing will be visible after this one" moment — only the after-the-fact reaction. If such a moment exists in a part of the session not captured in `audit-extracts/user-messages.jsonl` (or in the pre-04-06 sprint-2026-04-05 planning session, which is out of this dossier's scope), it would soften finding §3 (the gap being "surfaced live" rather than "anticipated and accepted").
- **Whether the Verdandi-pip/norn-switch bugs the developer found manually (§3) were later filed, fixed, and by which story** — I traced the *existence* of the pre-04-06 Norn-selector component but did not trace the specific bug-fix commits for "Urd repeated herself" / context-bleed-on-switch, since those belong to the client repo's separate epic timeline, out of this sprint's scope.
