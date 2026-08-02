# Verification Lens — What "Verified" Actually Means in Practice

**Date:** 2026-08-02
**Role:** Discovery lens investigating what verification (QA, AVFL, E2E, end-gate) actually
executed vs. inspected in the nornspun delivery pipeline, using sprint-2026-07-13 as the primary
case, with sprint-2026-06-18 and sprint-2026-04-12 as comparison points.

---

## Executive summary

1. **The sprint was never merged to main in either code repo.** `sprint/sprint-2026-07-13` sits
   26 commits ahead of `nornspun-backend:main` and 27 ahead of `nornspun-client:main`; both repos'
   working trees are checked out on `main`. All 12 stories still carry status `review`, not
   `done`. This alone explains "the app can't do the simplest things" independent of any
   story-level quality question — the developer's manual walkthroughs ran against pre-sprint
   `main`/stale worktree state, not the sprint's work. (git log, `.momentum/stories/index.json`)
2. **E2E genuinely caught the sprint's worst bugs — this is a counter-example to pure "theater."**
   Direct Postgres queries during the live E2E run proved Urd's confident "It is written." close
   produced **zero database rows in ~5 of 7 attempts**; a separate capture **persisted a
   completely different adventure's content** under a distinctive campaign's session slot; and
   ordinary non-play conversation **mints numbered "sessions" that count as real play**. All three
   were reproduced with evidence (DB row counts, verbatim narration vs. verbatim persisted
   content) and escalated as high-blast-radius findings, not waved off. (`build-ledger.jsonl`
   events `e2e-stakes-escalation`, `discharge-stakes-capture-receipt-1`, `avfl-finding INTEG-001`)
3. **The end-gate report is unusually honest, not a rubber stamp.** It explicitly states the
   sprint's "core promise... is not yet reliable," lists an 8-item "Still hollow" table, and says
   outright that approving "does not declare the memory loop trustworthy." Six decision cards
   (D1–D6) were left for the developer, three of them (D4/D5/D6) about the exact capture-integrity
   cluster above. This cuts against a naive "gates lie" reading of the practice.
4. **But the honesty didn't fix anything, because closing the gate never happened.** The report's
   own "Approve" sequence (merge to main → transition stories to `done` → run the major-residual
   guard) is unexecuted. Finding #2 (unmerged) means the disclosed, accepted risk in the report
   never became a tracked baseline — it just sits, undecided, 11+ days later (today is 2026-08-02;
   the report is dated 2026-07-22).
5. **One story's own "executed at E2E" verification claim is directly contradicted by later manual
   use — a concrete instance of hollow verification, not just a coverage gap.**
   `backend-active-campaign-name-injection-fix`'s smoke contract asks each Norn "What is this
   campaign called?" directly — a phrasing that lets the model resolve the answer via its
   `get_campaign` tool call, producing a correct-looking reply regardless of whether the intended
   fix (injecting the resolved name into ambient context) actually works. It doesn't: `campaign_name`
   is computed in `urd.py:113` but appears in **zero** prompt templates — the only campaign line
   Urd's system prompt actually carries is a bare `Active campaign: <raw UUID>`. The developer
   independently reproduced this live on both Android and Desktop nine days after the report
   claimed the contract "passed" (see finding narrative below for verbatim diagnosis).
6. **The coverage-plan's own compositional design created this blind spot.** The plan explicitly
   routes this story to a "dedicated-run" isolated test rather than composing it into the organic
   multi-turn Scenario A conversation, with the stated rationale "name-not-UUID elicitation... not
   naturally part of Scenario A's script." Composing it into ambient conversation — the way an
   actual user experiences it — would very likely have surfaced the defect at build time.
7. **Desktop verification is a structural, permanent gap by architecture choice, and it was skipped
   even within that reduced scope this sprint.** `verification-harness.json` and
   `.claude/rules/e2e-validation.md` both encode Desktop as "AX-blind... collaborative walkthrough
   required," never automated. This sprint's own E2E notes record: "Desktop platform parity
   UNVERIFIED this session (window not on visible display; AX-blind)." The one collaborative
   desktop walkthrough that did happen was driven live by the developer after the report shipped,
   and it immediately surfaced the campaign-context bug on desktop too.
8. **The developer's own manual walkthrough found defects no automated layer had a slot for at
   all.** The campaign-creation flow has no back-navigation out of it (a UI dead end); tapping a
   post-creation "›" does nothing; and the entire hero/character persistence layer does not exist
   — the `heroes` table is empty across the whole database and the backend has no
   hero-persistence tool, despite Urd conversationally inviting players to describe a character.
   The Conductor's own diagnosis calls the navigation issue "a coverage gap, not a regression" —
   no story's acceptance criteria ever asked the question.
9. **This is a recurring pattern, not a one-off.** Wave 1 of this very sprint existed because the
   *prior* sprint's (06-18) desktop test suite silently didn't execute at all (missing JUnit
   runtime) — and mid-build, this sprint's own fix for that exact failure mode caught its own
   proof-case file still silently skipped by the same class of bug, one migration away from
   shipping while claiming to have fixed it. Verification-of-verification is itself fragile and
   needed a human-authored guard (per-module minimum executed-test counts) to hold.
10. **Some automated verification infrastructure was simply broken.** Two frozen smoke-test
    scripts had a bash heredoc-in-piped-function bug that broke their first assertion "regardless
    of backend behavior" — real defects existed underneath, but the contract itself could not
    produce a verdict and had to be manually ported to a working script to get a real signal.

---

## 1. What the verification harness actually specifies

`momentum/verification-harness.json` (nornspun repo) defines execution surfaces per change type:
skills/rules run via direct invocation or cmux behavioral triggers; scripts/CLI run in cmux via
bash; backend is `curl` against a live FastAPI on port 8001; `app-ui` maps to driver `smoke` =
Maestro on Android, with an explicit fallback: **"Compose desktop is AX-blind — desktop
verification is pixel/observation via cmux-launched desktop build."** There is no automated
desktop driver, by design — the `driver_bindings.smoke.fallback` field names it
`desktop-observation`, and `human_review_carveouts` covers only `research-spike` and
`specification`, not desktop UI.

`.claude/rules/e2e-validation.md` reinforces this: Desktop is explicitly "NOT automated. It's a
collaborative walkthrough" — developer drives, validator observes, screenshots for layout. It also
sets two mandatory checks applying to *all* UI platforms: **Layout Stability** (before/after
screenshot diff on any state transition) and **Send-Failure User-Facing Error** ("Silent failure
classifies as FAIL, not PASS, even if backend logs... confirm the failure was detected by the
client"). These are well-designed, specific, checkable rules — the rules layer is not naive.

**Historical rigor check (sprint-2026-04-12):** `maestro-audit.md` shows a genuinely careful
audit converting 7 of 13 previously-MANUAL scenarios to AUTOMATABLE Maestro flows, with per-scenario
reasoning (e.g., "Maestro supports `stopApp` + `launchApp clearState:false` to simulate app
restart"), and confirming the remaining 6 as correctly MANUAL (3 Desktop-only, 3 pure backend/DB
tests wrongly routed to a UI tool). This is evidence the verification design overall is deliberate
and self-improving, not lazy — which makes the sprint-07-13 gaps below more a story about
*where the design's edges are* than about carelessness.

---

## 2. Sprint-2026-07-13: what the E2E/AVFL pipeline actually executed

The build ledger (`​.momentum/sprints/sprint-2026-07-13/build-ledger.jsonl`, 156 events) shows a
real pipeline: per-story `dev → code-review (stage-2) → fix/simplify (stage-3)`, then a single
consolidated `avfl-on-merge` pass per repo, then one `e2e-phase-complete` pass covering the whole
integrated branch. The E2E phase ran **34 scenarios: 28 passed, 1 failed, 2 new findings** (one
auto-dismissed as a downstream artifact, one escalated).

The `scenario-a-discharge` agent (a `momentum:e2e-validator` invocation) is the strongest evidence
of genuine, non-theatrical verification in the whole sprint. Its report is not a checklist tick —
it is a transcript-and-database forensic investigation:

> "Direct DB query (`SELECT count(*) FROM sessions WHERE campaign_id = '8d71fefd...'`) returned 0
> rows, confirming the capture never persisted despite the confident conversational receipt."

> "...a brand-new conversation... replied 'No sessions have been written down yet, which means
> we're at the very beginning' — directly contradicting the prior turn's own claim."

> Store B's own frozen contract "printed PASS but only via its own explicit graceful-degradation
> escape hatch"— i.e., it detected it couldn't observe the real behavior and declared a partial
> pass rather than silently claiming success. This is itself an example of a contract being
> honest about its own blind spot.

The `e2e-validator` teammate independently found and reproduced a *second*, distinct bug — a
capture that persisted fabricated content from a wholly different adventure — and refined its own
hypothesis in a follow-up message after a second reproduction ("New working hypothesis... cross-request
context bleed under concurrent load"), correctly flagging that the discriminating test (serial vs.
concurrent reproduction) hadn't been run yet. This is careful, epistemically honest investigative
work, not a rubber stamp.

**Conductor-warning entries corroborate the same picture from the build side**, e.g.: "AVFL
backend consolidation score 51 (Poor): 1 critical escalated (INTEG-001 phantom sessions)... the
Conductor will record NON_CONVERGENT with leftovers=[INTEG-001]... rather than burning 3 further
8-validator iterations" — a documented decision to stop iterating and escalate rather than force a
green result.

### Where the pipeline's own tooling failed

- **Harness bug:** "Scenario A harness bug: `extract_reply_text()` bash-heredoc-in-piped-function
  bug... breaks session-naming and urds smoke contracts' first assertion regardless of backend
  behavior... executor verified via ported standalone script." Two of the sprint's frozen contracts
  could not produce a verdict through their own official script; a human/agent workaround was
  needed to get a real signal at all.
- **The Kotest migration's own proof-case, silently skipped again:** the wave-1 gate story exists
  because the *previous* sprint's ~29 desktop test files silently never ran (missing JUnit
  runtime — noted directly in `sprints/index.json`'s wave-1 note: "desktop tests silently did not
  execute in sprint-2026-06-18"). Mid-build, the adversarial code reviewer caught that this
  story's own named proof-case (`NornApiClientChatTest`) was *still* silently skipped in the
  shared module — the exact defect class the story existed to end — fixed only because a human
  reviewer looked, not because the "zero tests = fail" guard caught it (it stayed green because
  *other* tests ran). The end-gate report itself narrates this: "A green suite that doesn't run is
  worse than a red one — it manufactures false confidence." (§03)

---

## 3. The end-gate report: honest, then inert

`.momentum/handoffs/sprint-2026-07-13-endgate-report.html` (rendered 2026-07-22) is candid to a
degree that undercuts a simple "verification theater" narrative. Verbatim:

> "All 12 stories built and merged — and the live verification run then caught the thing that
> matters most: the sprint's core promise, 'what you tell Urd gets remembered,' is **not yet
> reliable when a real language model drives it**."

Section §06 ("How done is this, really?") is a two-column honesty table: 9 capabilities rated
"Live and working now" against 8 rated "Still hollow" — including "Capture reliability under a
live model," "Desktop platform parity... not verified this session," and "Cross-restart
conversation seating." The closing line: **"[Approving] does not declare the memory loop
trustworthy (D5/D6 are open work)."**

Six decision cards (D1–D6) are presented for developer sign-off, three of them (D4 phantom
sessions, D5 silent capture loss, D6 fabricated/mismatched content) forming one explicitly-flagged
cluster. Every card carries a recommended option, evidence, and stakes — this matches the
practice's own Pause-Ask Surface Contract, and it is inline-context-complete (a reader does not
need to open another file to understand any card).

**What breaks the value of this honesty:** the report's own §07 "exact approve sequence" — merge
sprint branches to main in all three repos, transition stories `review → verify → done`, run the
major-residual guard — never executed. Verified independently via git:

```
nornspun-backend:  git log main..sprint/sprint-2026-07-13 --oneline | wc -l  →  26
nornspun-client:   git log main..sprint/sprint-2026-07-13 --oneline | wc -l  →  27
Both repos' working trees: on branch `main` (not the sprint branch)
.momentum/stories/index.json: all 12 sprint stories at status "review"
.momentum/sprints/index.json: "planning": null  (no next sprint started)
.conduct-wt/{nornspun-backend,nornspun-client}/INTEGRATION worktrees: still present, uncleaned
```

For comparison, `sprint-2026-05-30`'s branch on the backend repo — also never explicitly
deleted — **is** fully merged (0 commits ahead of main), confirming stale branch refs are normal
housekeeping residue in this practice but sprint-07-13's 26/27-commit gap is not that; it is a
gate that was never actually closed. No approval or "Request changes" decision record exists in
`.momentum/practice-ledger.jsonl` for this gate (the ledger only logs intake/decision entities, not
gate outcomes, and no sibling `endgate-decision.md` file exists next to `plan-gate-decision.md` in
the sprint directory).

The session transcript shows the developer reviewing the report live and asking, verbatim: *"I see
a 07-13 report but that can't be it. Where is the report? And shouldn't I be looking at the app
itself?"* (session `2a45301c...`, 2026-07-22T16:38:01). The assistant agreed and launched the
desktop app from the **`.conduct-wt/nornspun-client/INTEGRATION`** worktree for the developer to
drive live — the first time in the entire sprint a human eye looked at the running desktop build.
The session transcript ends moments later, mid-launch.

---

## 4. The concrete "plumbing tested, outcome not" case

`backend-active-campaign-name-injection-fix`'s frozen contract
(`specs/backend-active-campaign-name-injection-fix.smoke.sh`) asks each Norn directly: *"What is
this campaign called? Please state its name,"* then asserts the reply contains a distinctive
invented name and never the raw UUID. It passed. The end-gate report accordingly claims: *"the
live curl contract was **executed at E2E**: both Norns named a distinctively-named campaign
correctly, no UUID leak."*

Nine days later (2026-07-31), the developer manually drove both Android and Desktop and got, on
Desktop: *"I can see you have several campaigns in the chronicle, but I don't have a way to
determine which one is 'current' — that's not information I track automatically."* Live diagnosis
(same session, `20b5f62e...`, 2026-07-31T04:38:44), quoted directly:

> "The code dutifully computes `variables['campaign_name'] = campaign.name` (`urd.py:113`) — but
> `campaign_name` appears in **zero** prompt templates, so the name is computed and silently
> dropped. The only campaign context that actually reaches Urd is `urd.py:190`: a bare `Active
> campaign: <raw UUID>` line... **The story's tests presumably asserted the *variable* got
> populated, never that the *rendered prompt* contained the name — plumbing tested, outcome not.**"

Why the smoke test passed anyway: asking "what is this campaign called?" is a directed question
that plausibly routes the model through its own `get_campaign` tool call, producing a correct
surface answer via a completely different mechanism than the one the story was supposed to fix.
Ordinary ambient chat (the actual user flow — pick a campaign, then just talk) never triggers that
tool call, so the raw-UUID defect is invisible to the smoke test and fully visible to a real user.

The sprint's own `coverage-plan.md` explains why this wasn't caught by composition: the plan
routes this story to a standalone "dedicated-run" test, with the stated reason **"name-not-UUID
elicitation for both Norns plus fallback path; not naturally part of Scenario A's script."**
Scenario A is the one integration scenario that runs an organic multi-turn conversation. Had this
story's verification been composed into that ambient flow instead of tested as an isolated
direct-question script, the defect very plausibly surfaces at build time rather than three weeks
later in the developer's own hands. This is the clearest, single most instructive example in the
whole sprint of *where* a coverage-plan design choice — not laziness, an actual documented
decision — created the exact blind spot a real user walks into first.

The same root cause reappears on Android on both 2026-07-22 and 2026-07-31 diagnoses, compounded by
a second, orthogonal defect: the app was restoring a stale E2E test fixture (`TrimTestCampaign`) as
the active campaign from local storage, so even "campaign selection" itself wasn't taking effect —
Urd's own toolset has no "switch active campaign" tool; the binding lives entirely client-side in
the `campaign_id` field the client sends on `POST /api/chat`, decoupled from whatever campaign name
the user is discussing in-conversation. The diagnosis: *"Conversation says Salt Road; database says
TrimTestCampaign... it *will* save, silently, into the wrong one. That's the D6 failure mechanism...
reachable by design on Android right now, not just as a race condition."*

---

## 5. Defects the pipeline had no slot to catch at all

The developer's manual walkthrough on 2026-07-22 (session `2a45301c...`, 23:12:13) surfaced two
problems no automated layer was ever positioned to find:

> "when I chose choose new campaign from the picker it went to a UI that didn't allow me to go
> back to the campaign picker in any way... Even after I created a name it showed the '>' but
> clicking it did nothing." — the Conductor's own live diagnosis: *"The `campaign-picker` story's
> ACs covered the picker list (newest-first, skeletons, graceful failure) but never create-flow
> return navigation — **a coverage gap, not a regression.**"*

> "when I chose the salt mines campaign that I had already filled in last time it started from
> scratch." — diagnosed via direct DB query: the named campaign ("The Salt Road," created June 12)
> has **zero** heroes, adventures, episodes, or recaps. Wider check: the `heroes` table is **empty
> across the entire database**, and `grep` across `src/tools/` (campaign.py, content.py, foundry.py,
> memory.py, search.py) shows **no hero-persistence tool exists at all**. Urd collects character
> information conversationally but nothing ever writes it down — a gap invisible to any AC because
> no story in this sprint (or, on this evidence, any prior one) owns hero/character persistence.

These are not verification *failures* in the sense of a check that ran and lied — they are areas
where no check was ever specified to run, because the acceptance criteria that would name them
don't exist yet. This is direct, first-hand evidence for the mission's working hypothesis: stories
pass their own acceptance criteria; a full user journey crossing story boundaries (pick a campaign
→ have a real conversation → have it actually save under that campaign → return to it later) was
never anyone's stated AC, and it is exactly where the product breaks for a real user.

---

## Counter-evidence & falsifiability

Evidence that cuts against a simple "the pipeline is theater" reading, in order of strength:

- **E2E and AVFL caught the three worst bugs in the entire sprint via real execution**, not
  inspection — live DB queries, live conversation reproduction, and a second reproduction to test a
  hypothesis. If this were pure theater, these findings would not exist; they would have been
  waved through like the routine items in §05.
- **The end-gate report volunteers its own incompleteness** in explicit, unambiguous language
  ("Still hollow," "does not declare the memory loop trustworthy") rather than presenting a clean
  scorecard. A report optimizing for a rubber-stamp approval would not write this.
- **A contract detected its own inability to observe the real behavior and said so** (Store B's
  smoke script: "Treating environment as summarization-unavailable... without failing the
  closing-call guarantees already verified above") rather than silently asserting success.
- **The practice actively hunts for exactly this failure mode historically**: the maestro-audit
  process (04-12) exists to re-classify and tighten MANUAL/AUTOMATABLE boundaries, and this
  sprint's wave-1 story exists specifically to close a previously-discovered silent-test-skip gap.
  This is a system iterating on its own blind spots, not ignoring them.
- **What would prove the "verification is theater" framing wrong more completely:** if the next
  sprint (not yet planned — `sprints/index.json.planning` is `null`) actually merges sprint-07-13,
  ships the D5/D6 hardening story first as promised, and a subsequent developer walkthrough finds
  the core capture loop reliable, that would show the process — slow, and stalled here — working
  as designed rather than being structurally incapable of closing gaps.
- **What would strengthen the "theater" framing further:** if a future audit found *additional*
  stories whose smoke/curl contracts pass via a confound (as with the campaign-name story) rather
  than this being an isolated instance — I did not have time to audit all 8 dedicated-run contracts
  line-by-line for the same class of confound; I checked one in depth because it was the one the
  developer's own manual walkthrough falsified.

---

## Open questions

- **Was the end-gate ever formally acted on (Approve / Request changes)?** No decision record
  exists in `.momentum/practice-ledger.jsonl` (it only logs intake/decision entities) and no
  `endgate-decision.md` sibling to `plan-gate-decision.md` was found in the sprint directory. The
  git evidence (unmerged branches, stories still `review`) strongly implies "never approved," but I
  could not find an explicit rejection or hold decision either — it appears to have simply been
  left open when the developer's review session ended.
- **Why did the developer's session gap 8–9 days (2026-07-22 → 2026-07-31)** right at the moment
  the desktop app was first being launched for review? The developer's own suspicion, recorded
  verbatim in the next session's opening message, was that "it seemed to get confused with CMUX and
  close its own session tab" — I could not verify this mechanically (no crash/error record found in
  the transcript itself; the file simply ends after the launch command's tool result).
  Session end mechanics are outside this lens's evidence.
- **Is hero/character persistence scoped in any epic at all?** A shallow grep of
  `docs/planning-artifacts/epics.json` found only a passing mention of "adventure ingestion" inside
  the campaign-intelligence epic's description, no dedicated hero/character epic. I did not do a
  full-text audit of all epic bodies or the PRD to confirm this is a genuine unscoped gap versus
  simply not-yet-broken-into-stories work sitting later on a roadmap.
- **Are other "dedicated-run" contracts (of the 8 in this sprint) hiding the same confound class**
  as the campaign-name-injection story? I audited that one in depth because independent evidence
  (the developer's manual walkthrough) falsified its claimed pass. I did not have budget to
  line-by-line audit the other seven dedicated-run contracts against their story's actual intended
  mechanism the same way.
