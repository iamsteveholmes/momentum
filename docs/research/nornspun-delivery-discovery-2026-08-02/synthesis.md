# Synthesis — Why Ten Sprints of Nornspun Delivered Stories but Not Features

**Date:** 2026-08-02
**Author:** Claude (Fable 5), synthesizing a 32-document discovery corpus: 26 discovery/research
documents, 3 adversarial council position papers, and 3 cross-examination rebuttals. All claims below
cite corpus documents (which cite raw sources) or were verified directly. Corrections the council
falsified are listed in §7 — several widely-quotable corpus claims are **wrong** and must not be cited.

---

## 1. The verdict on the hypothesis

Your hypothesis — *"our sprints focus on delivering stories rather than delivering functionality; story
ACs pass but nothing is functional"* — is **directionally correct, mechanically incomplete, and wrong
in three specific places that change what you should do about it.**

**Where you are right:**
- "A user can now do X" exists nowhere as a mechanical checkpoint. `features.json` carries
  well-written per-feature acceptance conditions and is wired to nothing: zero references in the
  sprint-planning workflow (both installed versions, grep-verified), no feature field in any sprint
  state schema, stale twice (always optimistically), its only consuming skill deprecated and halted.
  **0 of 15 features have ever reached done while story throughput rose 3→9 per sprint.** Story
  throughput is fine; it never converts. (backlog-economics-lens, planning-lens, PM position)
- The Definition of Done (epics.md, 7 items) has no reachability requirement. This retired-as-a-class:
  the settings gear (`onOpenSettings = {}`, 3 sprints), the empty `SurfaceType` enum, a complete
  heroes API + repository + prompt assembler with **zero callers on either side**, desktop upload.
- Verification routes by `change_type` (a property of the diff) not by where a user meets the
  behavior — so conversational user-facing stories were verified via curl-only composed scenarios.
  All three council seats independently converged on this as a real structural defect.

**Where you are wrong, and it matters:**
1. **The latest sprint never shipped at all.** All 12 sprint-2026-07-13 stories merged only to the
   sprint branch; 26 backend + 27 client commits have never reached main; the end-gate was never
   decided (no decision record exists — the "approved" in this investigation's own brief was false);
   the retro never ran; the sprint is still `active/locked` with all 12 stories at `review`. When you
   opened the app you were running **pre-sprint code** — and on Jul 22/31, a **chimera**: sprint-branch
   client against a main backend missing all 26 commits. Part of "couldn't do the simplest things" is
   release mechanics, not story quality. (sprint-2026-07-13-dossier, ground-truth, all three seats)
2. **The pipeline did not lie to you — it told the truth and nothing could act on it.** The end-gate
   *led* with "the sprint's core promise… is not yet reliable"; E2E did live `SELECT count(*)`
   forensics and caught silent capture loss (~5 of 7 closes → zero rows) and a fabricated capture
   before any human looked. The field's canonical failure is pipelines lying ("premature completion");
   yours is honest disclosure with no enforcement point downstream ("premature abandonment" — a
   variant the external literature does not name). Spec quality is good and improving; no
   reward-hacking fraud was found anywhere (0/20 sampled done stories fabricated).
3. **Part of "broken" is the product's runtime LLM, not the dev process.** The shipped product runs
   openrouter hy3-preview (~$0.06/M); it narrates "It is written." while failing to call its save
   tools. No dev-process fix closes that class. (ground-truth §4; council flagged an open aggravator —
   see §6, the UUID-strip question.)

Also: **planning is not where your time goes.** The full sprint-2026-07-13 planning arc took 89
minutes of machine wall-clock. The calendar sink is untracked 7–18-day human gaps between plan-ready
and build, an 11-day (and counting) undecided end-gate, and thin contact during builds (3 substantive
turns across 7 days; retro run in "yolo mode" at your request). The scarce resource in this system is
your attention, and the practice spends it on documents about the product rather than the product:
you launched the app on **5–6 days out of 54**, and your dev database after 4 months contains
0 heroes, 0 adventures, 0 real sessions.

## 2. The causal chain (the council's reconciled model)

Each seat named a different load-bearing cause; the rebuttal round reconciled them into a dependency
chain rather than a contest. Each term is worthless without its predecessor:

**REFERENT → CADENCE → REFUSAL**, sitting on top of **RUNTIME RELIABILITY**.

1. **Referent (Architect):** There is no artifact that *is* the product. Two independently-versioned
   repos, hand-assembled at every launch, composition recorded nowhere; no contract at the seam; no
   test in either repo crosses the process boundary; client repo has **no CI at all**, backend CI is a
   stub that has never run. Consequence: observations about the product — including yours on Jul 22/31,
   and two of this corpus's own audit documents — were made against compositions that never existed in
   version control. Until the referent exists, every other fix operates on noise.
2. **Cadence (Senior dev):** Delivery terminates in one manual human ask with no expiry, retry, or
   fallback, and an unmerged branch is an **unfalsifiable** branch — the only tree you can run is
   stale, so the product is never used, so integration defects have no discovery mechanism (seven
   quality instruments walked over a one-segment 404 URL bug for 116 days; your walkthrough found
   top-tier defects within minutes on every one of the ~5 occasions it ran).
3. **Refusal (PM):** Nothing is obligated to ask "can a user do X." The outcome instrument exists at
   both ends and is connected at neither: features.json orphaned at the output; your own bug report
   entered intake as `priority: low, feature_slug: null, verification: curl` (position #10 in the
   sprint) at the input. The roadmap converts the vacuum into a schedule: cut along the backend
   dependency spine, first feature completion possible at Sprint C, MVP gate at Sprint E — signed, but
   nobody said "nothing you can see will change for two sprints" out loud at approval time.
4. **Runtime reliability (no seat owned it; all conceded it):** a cheap model that doesn't reliably
   call tools is a product-architecture problem (transactional write receipts, read-back verification,
   model selection) that would remain after a perfect process.

The apparatus itself is an **amplifier, not the root**: it produced the best diagnostics in the
corpus (honest end-gate, forensic E2E) *and* consumed the attention needed to act on them. Momentum
practice commits are falling month over month (597→399→347→139→7), so "the apparatus is a second
product" is partially self-falsifying as a flow claim — but the stock (30 skills, ~36k lines of skill
markdown) imposes a standing read-tax, and 65+ retro findings across 5 retros produced 100%
process-shaped stories of which **0 of 29 ever shipped**.

## 3. What is actually true about the product (better and worse than believed)

**Works, live-verified on main (2026-08-02):** backend health, campaign list/create, SSE chat with
Urd and Verdandi, conversational campaign creation writing real rows, adventure PDF ingest → retrieval
→ Verdandi citing an NPC by name, honest refusal when retrieval is empty; desktop client builds in
27s, launches, renders, completes a live chat round-trip in ~2s. **A walking skeleton exists.** The
field's greenfield "build Slice 0 first" advice misdiagnoses us; the deficit is wiring, closure, and
usage — not absence.

**Broken, concentrated at specific seams (not uniform):** adventure upload has 404'd since 2026-04-09
on every branch (`NornApiClient.kt:320` missing `/api`; no test exercises the real call);
conversation-history reload is an empty-body stub; settings gear is a no-op with no screen behind it;
heroes API complete with zero writers; session-prep has real backend and zero client surface
(`SurfaceType` intentionally empty). 14/20 randomly-sampled done stories are cleanly reachable; 0/20
fabricated. The desktop E2E launcher has **never worked on any commit in repo history**, and the
golden-path test drives a synthetic composition and is silently never discovered by the runner.

## 4. Ours vs. the field (last 12 months)

- The symptom is field-canonical: Anthropic hit it building a claude.ai clone ("fail to recognize the
  feature didn't work end-to-end"); spec-kit users: "great specs — no MVP"; a BMAD pipeline
  "erroneously flagged as complete" a nonfunctional auth system. SpecBench quantified the mechanism:
  agents saturate visible AC suites while failing held-out tests, and the gap "arises from test suite
  structure, not model capability" — adding more same-spec reviewers adds correlated, not independent,
  verification. Your only held-out test was you opening the app.
- The convergent fixes are exactly three: **(a)** hold done-ness to a user-journey check on the
  running product; **(b)** walking-skeleton / vertical slices; **(c)** single-writer + fresh-context
  review. You already own (b) (the skeleton walks) and (c) (conduct is single-writer per story with
  fresh reviewers — Cognition's production evidence validates that part of Momentum). You own the
  *artifacts* of (a) — features.json is precisely Anthropic's "failing-by-default feature registry,"
  and maestro/ flows exist — but neither gates anything.
- Our three failure modes the field does not name: the unclosed loop (honest gate, no actor), build
  identity (chimera reviews), and runtime-LLM tool reliability as a shipped-product defect. One field
  gap flagged twice: nobody has a journey-driving answer for Compose **desktop** (all published
  fixes are browser-based); Android/Maestro is our only proven real-app driver.
- Nobody at or above Momentum's ceremony level has a published success; the 2026 survivor trend is
  simplification + E2E gating. The heaviness didn't cause the gap (the gap is at merge/outcome, which
  ceremony never touched) — but it prices every future fix in attention you don't have.

## 5. What to do (council consensus, in dependency order)

Unanimous across three adversarial seats, ordered by the causal chain:

**This week — Referent:**
1. **Decide sprint-2026-07-13 in writing** (`endgate-decision.md`, the sibling plan-gate has and
   end-gate has never had) and **land or abandon the branches**. If landing: resolve `urd.py` by
   keeping the hotfix's implementation (name **and** UUID — see §6) and deleting the governed story's
   `assert str(campaign_id) not in result`; merge both repos; push (backend main is 23 commits
   unpushed since Jun 11); remove both `.conduct-wt` worktrees; move the 12 stories out of `review`.
2. **One command that IS the product:** a mise task that starts DB + migrations + backend + client
   from one explicit pair of SHAs, refuses a mismatched pair, prints both SHAs, writes RUNNING.json.
   Rule with teeth: a walkthrough that didn't start from it is inadmissible; every bug report cites
   the two SHAs.

**Next 30 days — Cadence:**
3. **Scheduled tasting** — the only oracle with a 100% hit rate: 10 minutes daily (senior dev) or
   2×30min/week (PM); findings to one flat file; paid for by deleting equivalent end-gate
   document-review time. Plus fix the hour-scale seams as the first tasting targets: upload URL
   `/api`, hero-write tool for Urd, desktop upload TODO (note: flips no board condition — Android is
   the AC), history-reload stub.
4. **End-gate terminal state becomes a state transition, not a document:** the gate is not complete
   until merge + push + story transitions execute, or it FAILS loudly with an expiry (48h →
   escalation). (The senior dev's stronger "silence means ship" auto-merge was contested and
   *refuted* for this sprint — auto-merge on Jul 22 would have shipped a 2-of-7 keystone; the PM's
   counter stands. Record a decision, don't remove it.)
5. **CI floor:** turn client CI on, un-stub backend CI, minimum-executed-test-count per module (the
   silent-skip class shipped green three sprints running).

**Structural — Refusal:**
6. **Re-key verification routing from `change_type` to assembled surface** (one table in
   verification-standard.md): behavior a user meets in the chat UI is driven through the chat UI or
   declares at plan time that it cannot be.
7. **Wire the outcome instrument at both ends:** features.json writable only by
   `momentum-tools feature verify --verdict --evidence --build <sha>:<sha>` recording a **human**
   PASS/FAIL against a running paired build; `sprint complete` refuses to close without one; every
   sprint is titled by the acceptance condition it will flip; the plan gate's first fork becomes
   "after this sprint a GM will be able to ___". At intake: an observation sourced from the product
   owner driving the app enters as critical with a mandatory feature_slug — never `low/null/curl`.
8. **DoD +1 item:** "reachable from the application's entry point by a user who has read no code."

## 6. Open questions with decisive tests

- **Does the UUID-strip aggravate D5/D6?** The governed fix removed the campaign UUID from Urd's
  prompt while four Urd tools require `campaign_id` as an argument. Fits D6 (fabricated capture via
  guessed/stale UUID) exactly; only partially fits D5. **Test (1 hour, run before writing another
  story):** five capture closes on merged trunk with tool-call logging, counting tool invocations by
  argument. (senior-dev rebuttal §4)
- **Model reliability floor:** hy3-preview's tool-calling failure rate vs. a mid-tier model on the
  same five-close protocol. If the cheap model can't reliably call `save_session_events`, no process
  fix matters until the model or the write path (transactional receipts, read-back verify) changes.
- **Does the Capability Board actually move?** PM predicts ≥4 of 15 conditions flip within a day
  each; the architect's audit says only the upload URL confidently flips. Running §5 items 1–3
  settles it empirically.
- **Compose desktop journey driving** remains an unsolved field-wide problem; decide deliberately
  whether to invest (custom driver) or accept human-tasted desktop + Maestro-gated Android.

## 7. Corrections — corpus claims the council falsified (do not cite)

The discovery corpus is retained verbatim for posterity, including its errors. The council's
spot-checks (each verified against raw source, several confirmed independently by two seats):

1. **"backend-active-campaign-name-injection-fix is hollow verification / campaign_name appears in
   zero prompt templates" (verification-lens §4/#5; comparison §1.1–1.2) — FALSE.** On the sprint
   branch, `urd.py:189-193` consumes the variable and the story's test (2eef2bf) asserts the rendered
   prompt contains the name and not the raw UUID. The live diagnosis that spawned this claim ran
   against main. The comparison document's "Anthropic's sentence, re-enacted" headline inherits the
   error. (The sprint-2026-07-13 dossier has the correct version.)
2. **Inverted:** the same governed fix is a **tested regression** — stripping the UUID four tools
   need. The "ungoverned" hotfix (append name, keep UUID) is the only correct implementation, and its
   own commit message ("the assertion the original story lacked") is false — which one council seat
   initially propagated and then retracted. Faithful implementation of a wrong AC survived dev,
   review, AVFL, and the end-gate — the sharpest single specimen of the practice's real failure mode.
3. **The end-gate D5 note "not a regression" was asserted with no bisect** 29 hours after a same-sprint
   commit modified that code path — honest symptoms, unevidenced causation, fed to the sole
   decision-maker.
4. sessionCount=0 "afternoon fix" was **already fixed** on the sprint branch (95ccb35) — stranded, not
   missing. "Client trunk is stalest" inverted — client is the *only* repo in sync with its remote.
   "Hero persistence tool doesn't exist" — the API/repository/prompt-assembler all exist; what's
   missing is any caller. "Three-plus months stuck" → 11 days. Walkthrough date Jul 31, not Aug 2.
5. **This investigation's own brief was wrong twice:** the end-gate was never "approved" (no decision
   record exists), and "couldn't do even the simplest things" appears nowhere in the transcripts
   (paraphrase from outside the corpus window). Chimera-corrupted evidence reached six layers deep —
   from your live diagnosis through the corpus to the council's brief — which is itself the strongest
   demonstration of the Referent problem.

## 8. What this means for Momentum and the broader strategy

1. **Keep:** single-writer conduct, fresh-context reviewers, forensic E2E, honest end-gates,
   AVFL-on-merge — each has a verified kill in this corpus, and the field independently validates the
   pattern. The diagnostic organs work.
2. **Build the motor organs:** the practice has no mechanism that *executes consequences* — merge,
   push, status transition, feature verdict, intake priority. Every consensus fix in §5 is a
   forcing function, not a new document. The unclosed loop is Momentum's design gap, not nornspun's
   quirk: gates emit HTML; nothing emits state.
3. **Measure outcomes, not artifacts:** the only number that should appear in a session greeting or
   sprint report is features PASS/FAIL by a human against a paired build. Story counts actively
   misled here (91 "done" contained ~4 registries' worth of contradictions).
4. **Respect the attention budget as the system's scarcest resource:** the practice must spend your
   minutes on the app, not on reading about the app. Decision-grade surfaces, tasting slots, and
   auto-executing gates all serve that one constraint.
5. **Never review a build that version control can't name.** The admissibility rule generalizes
   beyond nornspun to every multi-repo project this practice touches.

*Depth-on-demand: sprint dossiers (`sprints/`), lens audits (`lenses/`), ground truth
(`ground-truth-app-state.md`), external research (`research/`), council record (`council/`),
session cartography (`00-session-cartography.md`).*
