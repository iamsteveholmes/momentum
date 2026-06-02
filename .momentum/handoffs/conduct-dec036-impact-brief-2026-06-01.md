# Advisory Handoff: DEC-036 and Your Conduct Build

**To the session building/revising conduct. From the research/decision lineage. 2026-06-01.**

You have deep context on the conduct spec and the 52-story breakdown — I won't re-explain those. This is a heads-up that a decision landed *on top of* that breakdown, plus my read on what it implies for your 18-slice. Everything below is a **suggestion**. You have the build context; if your judgment says fold where I'd split, or place a story in a different epic, do that. I'm telling you what I know and where I think it points.

---

## 1. What changed and why

**DEC-036 exists** (decided today, `dec-036-conduct-hitl-calibration-2026-06-01.md`). Lineage: the decision-altitude research (`docs/research/hitl-oversight-altitude-2026-05-31`) → assessment **AES-004** graded Momentum's HITL surfaces against it → six decisions captured in DEC-036 (five adopted, one adapted, none rejected).

The verdict on conduct: **legible but stakes-blind.** Conduct gets progressive disclosure and functionality-organization right (that's the win — D6, build on it), but it routes *one undifferentiated altitude* over an uncapped feature, **auto-fixes a security/XSS finding identically to a typo**, renders only the "fixed" half of the auto-fix loop, and offers a one-click pre-checked Approve. AES-004's framing: we overcorrected from `sprint-dev`'s 17-ask **firehose** (over-review) straight past the calibrated middle to conduct's **single undifferentiated gate** (under-review).

The through-line — quote it to yourself when a judgment call gets fuzzy:

> **Don't remove HITL — remove the *safely-handled* decisions so the human isn't overwhelmed, while raising safety and review ability.** Gate the human only for *stakes classes*, routed by what (stakes) **and** when (timing).

**The load-bearing thing you need to know: DEC-036 AMENDS DEC-035 binding decision #1.** DEC-035 declared its binding decisions "not up for relitigation," and #1 was *"No in-between HITL; every intermediate approval gate is removed; legitimate issues are always auto-fixed, no per-finding prompt."* DEC-036 D1+D2 relax that — **narrowly and intent-preservingly**. The anti-firehose intent (no routine asks, no per-finding prompts for ordinary work) is **fully preserved**; only the *absolutism* (literally zero intermediate gates, literally always auto-fix) is relaxed for a high-bar, stakes-gated exception. The DEC-036 Reconciliation table (lines 95–99) spells out exactly which clauses move. I flag this prominently because a "closed" item reopened — you're not free-styling if you reintroduce an intermediate gate; you're implementing a ratified amendment.

The six decisions in one breath each:
- **D1 — stakes-and-timing escalation.** Gate only for stakes classes (security/auth-isolation; irreversible/destructive — migration, delete, force-push, prod deploy; high-blast-radius/architecture). Two timing tiers: **(a)** end-gate-expanded (DEFAULT — flagged + expanded, not collapsed); **(b)** a narrow, high-bar **mid-flight** tier that pauses-and-asks BEFORE acting, reserved for *irreversible-and-imminent OR build-invalidating*. Everything else stays autonomous + collapsed.
- **D2 — stakes finding-class, not silent auto-fix.** Distinct *class* in the finding schema; hold stakes-class findings OUT of silent auto-fix → they become decision cards (or mid-flight escalations if imminent).
- **D3 — render dismissed.** Report shows what the fixer changed AND dismissed (with rationale), in full context.
- **D4 — anti-rubber-stamp.** Drop the pre-checked Approve; when stakes items present, require per-card acknowledgment before Approve enables. Routine items still collapse.
- **D5 — decision-grade presentation + self-sufficiency floor.** Measurable caps (≤N bullets / word budgets), exec-summary-first — but every decision carries what/why/evidence **inline**; never send the human elsewhere. "Tight on the irrelevant, complete on the decision-relevant."
- **D6 — functionality-organized report.** Verbatim DEC-035 D6, reaffirmed unchanged. Already covered; nothing to do.

DEC-036's own Phase 2 also calls out a **spec revision** prerequisite: the conduct spec still says "zero intermediate gates" (§8:587–591) and "ALWAYS auto-fixed" (§4:259). Per DEC-036, §1, §4, §8, §9 of `sprint-dev-redesign-spec.md` should be revised to *design to* the exception before/alongside build. No story in the 52 owns that spec revision — see §5.

---

## 2. What this means for your 18-slice — suggested story changes

Grouped by leg. Each is "what I'd suggest changing, and why (decision)." Concrete where it's load-bearing.

### Epic 02 — fixer-via-directed-dev (the center of gravity; D2 lands here hardest)

- **`directed-fix-finding-schema`** *(D2, D1, D3 — the hard root for the whole chain).* This is the single most load-bearing change, and everything downstream blocks on it landing first. I'd suggest:
  - Add a **stakes finding-class enum** orthogonal to `severity` (security/auth-isolation; irreversible/destructive; high-blast-radius/architecture; default `routine`/none).
  - Add an **`escalated`** disposition. Today the vocab is *exactly* `fixed | dismissed | triaged-out` with an explicit *"no `deferred` disposition"* note at §4:264 — there is **no escalate path** to represent "raised, not silently fixed." Every leg that emits an escalation depends on this value existing.
  - **Relax the invariant at §4:259** (`legitimate: true // legit -> ALWAYS auto-fixed (decision 1)`): a stakes-class legitimate finding is escalated, not auto-fixed.
  - Add a **timing-tier marker** (end-gate-expanded vs. mid-flight) so consumers know whether to render a decision card or escalate mid-flight.
  - **D3 capture:** make the `rationale` field **required/non-empty when `disposition=dismissed`**, so epic 04's report has authored content to render.
- **`directed-fix-invocation-contract`** *(D2, D1, D3).* Add an explicit **"escalate, do not fix" output path**: a stakes-class inbound finding returns disposition `escalated` plus an **escalation payload** (the what/why/evidence the decision card needs, inline per D5; plus the timing-tier flag) instead of a fix-applied commit. Require non-empty rationale on any `dismissed`. The contract does **not** own the mid-flight pause mechanism — it only emits disposition + timing so the Conductor can route.
- **`dev-fix-mode-entry`** *(D2).* `momentum:dev` fix-mode must **branch on the stakes-class field**: a stakes-class legitimate finding returns `escalated` + payload rather than edit+commit. Routine findings keep the always-auto-fix behavior unchanged. Without this the schema change is inert — dev would still fix everything legitimate.
- **`stage3-fix-loop-via-directed-dev`** *(D1, D2).* An `escalated` finding is neither fixed-clean, remaining, nor BLOCKED. Route it **out of the retry-bound-3 loop** onto the escalation channel — to the end-gate decision-card path by default (D1 tier a), or the mid-flight tier if the timing flag marks it irreversible-and-imminent/build-invalidating (D1 tier b). Retry mechanics for routine findings unchanged.

> **Watch this:** the "ALWAYS auto-fix" absolute appears in **three** places — the schema comment (§4:259), the dev executor, and the stage-3 loop branch. The critic flagged that relaxing only one leaves the others silently auto-fixing stakes findings. I'd thread all three.

### Epic 01 — code-review-adapter

- **`code-review-adapter-normalize-triage`** *(D2, D3).* Two touches.
  - **(D2)** The adapter must **populate** the new stakes-class field. But bmad-code-review emits **no** stakes/security signal — its triage (`bmad-code-review/steps/step-03-triage.md:32–36`) only buckets `decision_needed/patch/defer/dismiss`, no severity, no stakes axis. So this story can't propagate a class from bmad; at minimum it emits the field as `routine`/null. The *actual detection* is a new gap (§3). I'd keep #8 to the wiring and consume the classifier, not own it.
  - **(D3 clarification — important, easy to get wrong):** the breakdown says #8 drops bmad's `dismiss` bucket. **That's correct and does NOT conflict with D3.** Bmad's `dismiss` = noise/false-positive/handled-elsewhere, dropped at the bmad layer. DEC-036 D3's "dismissed" is a *different* concept: the conduct **fixer's** `dismissed` disposition — a legitimate-looking finding waved off **with rationale** — which lives in epic 02 + epic 04, downstream of #8. I'd state this distinction in the story spec so the adapter doesn't silently swallow findings the conduct fixer should see-and-dismiss-with-rationale. Only bmad-layer noise gets dropped.
- **`code-review-adapter-noninteractive-driver`**, **`-retire-stub`**, **`-repoint-sprint-dev`**, **`-repoint-quick-fix`** — **unchanged.** The driver is transport, the stub-retire is deletion, the repoints are call-site wiring. None touches schema or HITL semantics. (Honest no-change verdicts — I'd resist inventing work here.)

### Epic 05 — qa-and-dev-rescope (lightest-touch leg)

- **`qa-reviewer-rescope-per-story-contract`** *(D2, D4).* The qa-reviewer is a finding **producer**. For D2 to work end-to-end it must be able to **tag** a finding stakes-class when it encounters one (an auth-isolation AC, a MISSING/PARTIAL finding touching a destructive op). As written, #16 only rescopes the diff window; its verdict vocab stays AC/severity-only (`qa-reviewer.md:118–145`). I'd add a producer-side **tagging instruction** so the downstream fixer-hold (D2) and end-gate forcing function (D4) get a true signal rather than a structural false-negative. This **depends on** `directed-fix-finding-schema` landing the field first.
  - **Fold-vs-split judgment (yours to make):** there's an alternative new story `qa-reviewer-emit-stakes-finding-class` (§3). The critic's recommendation — which I agree with — is **fold the tagging into #16** rather than spawn a story, since the rescope already re-touches qa's finding emission. The two are **alternatives, not additive** — pick one, don't double-count.
- **`dev-read-contract-part-a-header`** — **unchanged.** Part A is plain-language dev self-check; stakes routing never touches what dev consumes from the contract.
- **`dev-strip-merge-cleanup-authority`** — **unchanged**, and in fact *confirmed* by DEC-036. Relocating git-mutation authority from dev to the Conductor is a **precondition** for the Conductor to own mid-flight escalation (D1) — DEC-036 endorses the direction.

### Epic 03 — conductor-skeleton (where D1's mid-flight tier reopens closed invariants)

- **`conduct-skill-scaffold-and-spine`** *(D1).* The spine's stated invariant is *"the Conductor never asks the developer anything during build"* (§3:117), with exactly two touchpoints (§2:75). D1 adds a **third, narrow** developer-facing surface inside the build phase. I'd suggest: add an **escalation control-flow branch** (a pause-ask-resume path the build can enter) and soften the invariant to *"never asks during build EXCEPT the narrow stakes-and-timing escalation tier."* This is a structural acknowledgment in the keystone — not the full mechanism (that's a new story, §3).
- **`conduct-preflight-halts`** *(D1) — the single most direct contradiction with DEC-036.* This story's softened invariant — *"no developer-facing HALT outside Phase 1"* — is exactly what D1's mid-flight tier violates (it pauses-and-asks the developer outside Phase 1). **Note the subtlety:** the breakdown already softened this invariant **once** (badge ✎ at breakdown HTML:161, 255) — but that first carve-out was for the §7 **Conductor-facing** freeze guard. D1 forces a **second, distinct** carve-out for a **developer-facing** pause — the more consequential one. I'd re-soften to: *"no developer-facing HALT outside Phase 1 EXCEPT the stakes-and-timing mid-flight escalation tier (irreversible-and-imminent / build-invalidating only)."*
- **`conduct-build-phase-frontier`** *(D1, D2).* The autonomous heartbeat (*on merged → re-evaluate; on failed → bounded retry, continue; never halt*). I'd add a **consumption hook** between pipeline-terminal-signal and continue: when a per-story pipeline surfaces a stakes-class finding meeting D1's mid-flight bar, the frontier invokes the escalation mechanism and pauses that branch instead of silently continuing or auto-fixing. The frontier *defers to* the mechanism — it doesn't implement detection. Routine path unchanged (anti-firehose preserved).
- **`conduct-merge-and-conflict-resolution`** *(D1).* **Scope nuance worth getting right** — AES-004 Finding 2 names the irreversible **sprint→main merge** as the prime stakes-blind action (spec §6:470–482). **But** the terminal sprint→main merge already sits inside the developer-gated APPROVE sequence (`conduct-approve-sequence-and-push`, epic-03-latter), behind approve + push confirmation — so it is **NOT an unguarded D1 trigger.** What I'd change *here* is narrower: **(a)** the per-story conflict-resolution/quarantine path must **escalate** (not silently auto-resolve + continue) when a semantic resolution touches a stakes class or is build-invalidating; **(b)** the merge machinery exposes the escalation hook the mechanism calls. Trivial conflict auto-resolution and ordinary quarantine-and-continue stay autonomous.
- **`conduct-contract-freeze-check`** — **unchanged.** This is a Conductor-facing integrity check (the one sanctioned non-developer halt), not a DEC-036 stakes class. The escalation acts on findings and irreversible actions, not contract-integrity assertions.
- **`conduct-coverage-disposition-branch`** — **unchanged.** It routes *when* verification runs (dedicated vs. composition), not how findings are classified. A stakes-class finding discharged at AVFL/merge is still routed out of silent auto-fix by the schema and report, not by this branch.

---

## 3. New stories I'd suggest intaking

Listed by importance. The **first one is the single biggest cross-leg gap** — every leg points at it, none builds it.

### ⭐ `conduct-stakes-timing-escalation-mechanism` — epic 03 *(D1 tier b)*
**The escalation ENGINE itself.** The Conductor-side **pause-ask-resume primitive** that:
- reads the stakes finding-class (D2) off a pipeline/AVFL result;
- evaluates D1's narrow, high-bar timing condition (irreversible-and-imminent OR build-invalidating) and **fires only on that bar** — everything else stays autonomous + collapsed (anti-firehose);
- raises a developer-facing mid-flight surface (a single decision card / pause-ask) carrying what/why/evidence **inline** (D5 floor);
- on resolution, resumes the build (proceed / change / abort-that-branch).

This is the shared primitive that `conduct-build-phase-frontier` and `conduct-merge-and-conflict-resolution` both call. It is the new intermediate gate DEC-036 amends DEC-035 #1 to permit. It exists **nowhere** in the 52 stories. It is **distinct from**: the terminal end-gate (`conduct-end-gate-conversation`/`conduct-approve-sequence-and-push`); the stakes finding-class *schema field* (epic 02); and the anti-rubber-stamp forcing function (D4, report/end-gate). Without it, **D1 tier (b) is unrepresentable in code** — the amendment is asserted in the schema but never realized in control flow.
*Suggested deps:* `conduct-skill-scaffold-and-spine`, `conduct-build-phase-frontier`, `directed-fix-finding-schema`. *Consumed by:* `conduct-merge-and-conflict-resolution`, `conduct-preflight-halts` (invariant carve-out).

### ⭐ `stakes-classification-rubric` — epic 02 *(D1 + D2 population logic)*
`directed-fix-finding-schema` adds the **field**; nothing **populates** it. AES-004 Finding 2 grades the heuristic itself *"Missing/unwired … no heuristic flags high-risk"* (aes-004:54–57). Define the shared, referenceable rubric: the concrete signals/patterns that mark a finding as each of D1's three stakes classes, the timing-tier decision (mid-flight only for irreversible-and-imminent/build-invalidating; else end-gate-expanded), and the `routine` fall-through. Authored once; consumed by every producer.
*Suggested deps:* `directed-fix-finding-schema`.

> **De-dup note — this is the one place three legs collided.** The adapter leg, fixer leg, and qa leg each independently proposed a near-identical classifier (`code-review-adapter-stakes-classifier`, `stakes-classification-rubric`, `qa-reviewer-emit-stakes-finding-class`). These are **not three units of work** — they're **one shared rubric** consumed by N producers. My strong suggestion (and the critic's): intake **ONE** rubric story (this one), then each producer leg gets a **small emission-wiring change** (adapter sets it from bmad prose; qa-reviewer sets it from AC/diff signal — folded into #16; AVFL sets it on integration findings). **Do not intake three full classifiers.** You're closer to the build — if you find the bmad-prose detection is heavy enough to warrant its own story under the shared rubric, that's a reasonable split; just don't duplicate the rubric itself.

---

## 4. What lands beyond your slice (heads-up, not your immediate work)

Your 18 are the **core-build slice** (epics 01/02/03-skeleton/05). The **report (epic 04)** and **end-gate conversation/approve (epic 03-latter)** are later slices. Several DEC-036 decisions land there. Flagging so you (a) emit the right signals for them and (b) **don't duplicate what's already well-covered.**

**Already well-covered there — don't rebuild:**
- **D6 (functionality-organized report)** — `functionality-grouped-organization` (epic 04, P0) already carries the exact charter (breakdown HTML:185). DEC-036 D6 is verbatim DEC-035 D6, reaffirmed. **No new work.** The only adjacency: stakes decision cards/escalations must slot into the functionality spine without breaking its collapse-clean/expand-diverged discipline — but that integration is owned by the D1/D2/D4 changes, not D6.
- **D3 rendering** — `legible-autofix-log` (epic 04, P0) already exists with the charter *"what changed AND dismissed, full context"* (breakdown HTML:186). The **rendering half is done.** Your only D3 job upstream is **capture**: guarantee non-empty `dismissed` rationale at the schema/contract boundary (§2, epic 02).
- **D5 floor** — `self-sufficiency-validator` (epic 04, P0) enforces the non-empty what/why/evidence floor. Your job upstream: make sure escalation payloads carry inline context so the floor has something to validate.

**Lands beyond your slice but you feed it (don't build, do emit correctly):**
- **D4 (anti-rubber-stamp)** threads through **three** epic-04/03-latter stories — `report-template-skeleton` (remove the pre-checked Approve at template:450 + pre-checked recommendations at template:360/377), `report-gate-control-wiring` (gate Approve-enable on per-stakes-card acknowledgment), `conduct-end-gate-conversation` (the gate loop must not treat un-acknowledged stakes items as approvable). D4 has a **hard dependency on D1/D2 classification accuracy** — the forcing function is false assurance if the stakes class isn't populated. Your slice's job: populate the class truthfully so D4 knows which cards require acknowledgment.
- **D1 tier (a)** (end-gate-expanded default) is a report/end-gate concern — structurally reachable once stakes findings are classified and rendered as decision cards. Your slice classifies; epic 04/03-latter renders.

**Cross-leg gaps NO leg evaluated — flag to whoever owns them (not your 18):**
- **AVFL (epic 06)** is a stakes-class **producer** DEC-036 D2 names explicitly (*"per-story + AVFL fixer schema"*). `avfl-merge-consolidate-score-classify` and `avfl-merge-code-finding-handoff` must also **stamp/propagate** the stakes class so a merge-only auth-isolation regression isn't silently auto-fixed. Change-existing-story on epic 06.
- **`honor-deep-review-depth`** (epic 01, P2, outside your 18) is left dangling: spec open-Q5 (spec:885) admits `review_depth=deep` is unwired with no high-risk heuristic. **DEC-036's stakes classes ARE that heuristic** — deep-review opt-in should become an *output* of the stakes classifier, not a hand-set flag. P2/later; route to whoever owns epic 01 P2.
- **D5 caps half** (≤N bullets, word budgets, exec-summary-first) has **no owner** — `self-sufficiency-validator` enforces only the floor. Either extend it into a self-sufficiency-**and-concision** validator, or add caps to `report-data-assembly-instructions` + `report-template-skeleton`. Epic 04.
- **D5 practice-wide half** (live skills: assessment, decision, sprint-dev, retro, impetus) is DEC-036 **Phase 4** — *"separable from the conduct build; can proceed in parallel."* Not in the 52 stories at all; **not part of your conduct build.** Needs its own practice-wide intake (a decision-grade-presentation rule + per-skill cap wiring).

---

## 5. Open tensions / judgment calls I'm leaving to you

1. **How narrow is the mid-flight bar?** DEC-036's Decision Gate (line 118) makes this *the* load-bearing definition: "irreversible-and-imminent OR build-invalidating" must stay narrow or it re-becomes a firehose. The decision sets the *intent*; you'll encode the *operational test* in the rubric + the escalation mechanism. If in doubt, bias narrow — D1 tier (a) (end-gate-expanded) is the safety net that catches anything you *don't* escalate mid-flight. Over-escalating mid-flight is the failure DEC-036 explicitly warns against.

2. **Where does stakes-classification authority live — conduct consumes, or the deferred planning epic emits?** The adapter leg noted `honor-deep-review-depth`'s authority sits in a *deferred planning epic*. The cleaner architecture (my read) is: **conduct's stakes classifier is the authority** at build time, and the planning-epic `review_depth` flag becomes an *input hint*, not the source of truth. But that crosses into deferred-epic territory — you may prefer to keep conduct purely consuming a flag and push classification authority upstream. Your call; I'd just make the dependency direction explicit wherever you land.

3. **Fold into existing stories vs. spawn new ones.** My defaults, all overridable by your build context:
   - **Fold** the qa-reviewer stakes-tagging into `qa-reviewer-rescope-per-story-contract` (#16) — don't spawn `qa-reviewer-emit-stakes-finding-class`. One-field tagging instruction; the rescope already re-touches emission.
   - **Fold** the adapter's emission-wiring into `code-review-adapter-normalize-triage` (#8); spawn a separate story only if bmad-prose detection proves heavy.
   - **Spawn** the two new stories in §3 — they're genuinely missing units, not field defaults.
   The principle: spawn when it's a real new mechanism (the escalation engine, the shared rubric); fold when it's a tagging/wiring touch on a story already in the area.

4. **The disposition-vocab amendment is small but absolute.** §4:264 says *"no `deferred` disposition"* — adding `escalated` is a one-line vocab change but it's the keystone the whole escalation chain stands on. Land it **first** (it's already marked foundation/no-deps in the breakdown; DEC-036 raises its criticality, not its position) so the rest of the chain has something real to emit and read.

5. **Spec revision is a prerequisite no story owns.** Per DEC-036 Phase 2, `sprint-dev-redesign-spec.md` §1/§4/§8/§9 still design to "zero intermediate gates" and "ALWAYS auto-fixed." The per-leg agents each saw only their slice of the spec, so none flagged the spec revision as a unit of work. I'd suggest you either intake a `conduct-spec-revision-dec036` story or treat it as explicit pre-build work — your call on whether it's a tracked story or a Phase-2 task. Either way, don't let the stories get built against a spec that still contradicts the decision they implement.

---

## 6. The decisions of record

Read these directly — don't rely on this summary for the load-bearing detail:

- **DEC-036** (the amendment): `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/decisions/dec-036-conduct-hitl-calibration-2026-06-01.md` — note especially the **Reconciliation with DEC-035** table (lines 95–99), the **Phased Implementation Plan** (lines 107–112), and the **Decision Gates** (lines 118–119, the bar-narrowness and false-negative warnings).
- **AES-004** (the assessment that found the gaps): `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/assessments/aes-004-hitl-altitude-design-gaps-2026-06-01.md` — Findings 1–6 map 1:1 to the six recommendations; Finding 2 (stakes-blind auto-fix) and Finding 4 (rubber-stamp) are the sharpest.
- **DEC-035** (the decision being amended): `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/decisions/dec-035-conduct-execution-engine-in-session-workflows-2026-05-30.md` — binding decision #1 is at D1/§Summary; read it next to DEC-036's reconciliation table so the "what moved" is exact.
- **The research** (full altitude reasoning): `docs/research/hitl-oversight-altitude-2026-05-31/final/hitl-oversight-altitude-2026-05-31.md`.
- **Your stories**: `/Users/steve/projects/momentum/.momentum/handoffs/conduct-story-breakdown-2026-05-30.html` (the 18 are the core-build slice; 52/7-epics total). **Reminder:** the 18 are **not yet intaken** into `.momentum/stories/index.json` — they live only in the breakdown, so revising them is editing the breakdown, not a tracked index.
- **The spec**: `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/sprint-dev-redesign-spec.md` (§-refs throughout above).

---

These are suggestions drawn from the research → AES-004 → DEC-036 lineage, written before you had the amendment in hand. You're the one with the build context and the full breakdown in working memory — where my read of a story's scope is off, or where folding/splitting plays differently against the dependency graph you can see, trust your judgment and adapt freely. The decisions of record are binding; my mapping of them onto your 18 is not. Lead on.