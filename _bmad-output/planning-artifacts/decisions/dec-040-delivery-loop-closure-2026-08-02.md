---
id: DEC-040
title: Delivery Loop Closure — Feature Verification Registry, Two-Tier Gates, and Nights-and-Weekends HITL Cadence
date: '2026-08-02'
status: decided
source_research:
  - path: docs/research/nornspun-delivery-discovery-2026-08-02/synthesis.md
    type: research corpus (26-agent discovery + 6-seat adversarial council + synthesis)
    date: '2026-08-02'
  - path: docs/research/nornspun-delivery-discovery-2026-08-02/decision-surface.html
    type: developer-conversation (F1–F7 verdicts + follow-on design conversation)
    date: '2026-08-02'
prior_decisions_reviewed:
  - DEC-029 (Method-Routed Acceptance Validation — harness profile and verification routing)
  - DEC-030 (Dependency-Driven Execution — frozen-scope sprints, amended by DEC-039)
  - DEC-034 (Epic-Layer Consolidation — unified features into epics; amended by this decision's D1)
  - DEC-035 (Conduct Execution Engine — end-gate design)
  - DEC-036 (Conduct HITL Calibration — escalation tiers, decision-grade presentation)
  - DEC-039 (Sprint Goal + Goal-Criticality Scope Mutability — completed and amended by this decision)
architecture_decisions_affected:
  - DEC-034 — AMENDED (D1): the outcome layer separates back out of epics.json. features.json returns as a standalone ACCEPTANCE-TESTING registry (not a work-tracking layer). Epic unification stands for work organization; the dual-layer coordination cost DEC-034 killed does not return because features touch exactly three seams (plan-time goal declaration, close-time human verdict, Impetus reporting) and no epic-facing skill reads them.
  - DEC-039 — COMPLETED + AMENDED (D2, D3): the sprint goal now binds to named feature acceptance conditions; the dual end-gate verdict splits into two independent gates (merge ≠ closure); closure gains a refusal mechanism and an honest FAILED terminal state. The D2 goal-criticality routing matrix is reaffirmed; condition-serving discovered work defaults to joining the sprint.
  - DEC-035 — AMENDED (D2): the merge gate's terminal state is an executed state transition (merge + push + status updates), not a rendered report.
  - DEC-036 — AMENDED (D5): gate-pending surfaces adopt the resume-card contract; expiry-FAIL is rejected in favor of session-start re-surfacing; wall-of-text gate surfaces are a defect.
  - DEC-029 — AMENDED (D7): verification routing re-keys from change_type (property of the diff) to assembled surface (where a user meets the behavior); Definition of Done gains a reachability item.
stories_affected:
  - sprint-2026-07-13 (nornspun) — all 12 stories remain open under D10 until the sprint's conditions verify; the sprint does not close on merge
  - implementation stories to be created via momentum:intake referencing DEC-040
---

# DEC-040: Delivery Loop Closure — Feature Verification Registry, Two-Tier Gates, and Nights-and-Weekends HITL Cadence

## Summary

A 26-agent discovery over ten nornspun sprints, five external research sweeps, and a three-seat
adversarial council established why 91 done stories produced 0 verifiably working features: the
practice's diagnostic organs work (honest end-gates, forensic E2E) but it has no **motor organs** —
nothing executes merges, records gate decisions, verifies outcomes, or refuses closure. The causal
chain is Referent (no artifact IS the product) → Cadence (no forcing function to trunk or into use) →
Refusal (nothing may refuse until "a user can do X" passes), resting on runtime-LLM reliability.
Prior decisions DEC-034 and DEC-039 anticipated much of this; their enforcement wiring was never
built, and sprint-2026-07-13 was planned three days after DEC-039 with none of its machinery in
place. This decision completes that wiring, resolves the feature-vs-epic oscillation permanently
(features are acceptance-testing entities, not work-tracking entities), splits the merge decision
from sprint closure, and reshapes HITL touchpoints around a nights-and-weekends developer whose
attention is the system's scarcest resource. Verdicts were given by Steve against the discovery's
decision surface (F1–F7) and the follow-on design conversation, 2026-08-02.

---

## Decisions

### D1: features.json returns as the standalone acceptance-testing registry — ADOPTED (amends DEC-034)

**Research recommended:** Track outcomes in a failing-by-default feature registry with per-feature
acceptance conditions, human-only verdicts, and minimal integration surface. Two candidate homes
were presented: complete DEC-034 (conditions live on user-facing finite-lived epics in epics.json)
or a separate features.json.

**Decision:** Separate `features.json`, kept per-project as the single outcome registry. It is an
**acceptance-testing entity, not a work-tracking entity**: epics remain the unified work organizer
exactly as DEC-034 left them, untouched in every epic-facing skill. Features integrate at exactly
three seams and no others: (1) sprint planning declares `goal_conditions` (0..n feature slugs whose
acceptance conditions this sprint intends to flip; maintenance sprints declare a verified-fix list
instead); (2) sprint closure records a human PASS/FAIL per named condition against a paired build;
(3) Impetus reports N passing as the practice's headline number. Schema: slug, name,
acceptance_condition, status (`absent | failing | passing` — failing-by-default), last_verified
{date, build SHAs, verdict}, optional informational `epic_slugs` (many-to-many, never validated,
never blocking) and `design_ref` links. Sole writer: the `momentum-tools feature verify` command
recording a human verdict. As part of implementation, nornspun's features.json is **carefully
reconciled with everything in the current design** (Claude Design / UX specification) so the
registry reflects the designed product, not the April feature list.

**Rationale:** Steve: "I think the separate features.json, and we should also make sure it has been
updated carefully with everything from the design." Earlier: "at least the CONCEPT of features needs
to exist. But again a Sprint is not always a single feature, it might be a set of related features
or even just a bunch of required bug fixes or configuration changes… I'd rather we not keep going
back and forth on this." The DEC-034 dual-layer cost does not return because no epic skill reads
features — the prior failure was making features a peer of epics inside every skill; this design
gives them three seams total.

### D2: Two-tier gate — merge and sprint closure are separate decisions — ADOPTED (amends DEC-035, DEC-039)

**Research recommended:** Make the end-gate's terminal state a merge (state transition), not a
report, with an expiry.

**Decision:** Two gates, two questions, decided independently and possibly days apart. **Merge
gate:** "is this code something we are comfortable keeping on trunk?" — fast, decidable async,
completes only by executing merge + push + story status transitions (it FAILS loudly rather than
emitting a report and stalling). **Sprint closure:** "have the sprint goals been met — do the named
conditions verifiably work in the app?" — stays open until the human verdict per D3. DEC-039's dual
verdict (stories delivered AND goal delivered) maps onto these two tiers rather than one combined
gate.

**Rationale:** Steve: "merging branches and finishing a sprint do NOT have to be married… For a
merge we just need to be sure that the code is something we are comfortable keeping. With the sprint
closure we need to feel comfortable that the sprint goals have been met. Essentially that the
planned features work." Discovery receipt: 53 finished commits sat stranded 11 days because the one
gate bundled both questions and neither got answered; an unmerged branch is an unfalsifiable branch.

### D3: Closure refusal — a sprint closes only on recorded human verdicts, or closes FAILED — ADOPTED (completes DEC-039)

**Research recommended:** `sprint complete` refuses to close without a recorded human PASS/FAIL
against the sprint's named conditions; discovered work serving the named conditions joins the
sprint rather than punting to backlog.

**Decision:** Adopted. The sprint goal (DEC-039 D1) binds to `goal_conditions`; closure requires a
human verdict per condition against a correctly-paired build. Condition-serving discovered work
defaults into the sprint (loud absorption per DEC-039 D2 — cited, linked discovered-from, end-gate
reported); non-serving discoveries still route to intake. A sprint that cannot reach PASS in
reasonable time closes **FAILED** — an honest, recorded terminal state, not a shame state. Punting
goal-critical work to a future sprint requires an explicit recorded decision, never a default.

**Rationale:** Steve: "If you always punt problems to the next sprint then you never have a
functional sprint, right?… I rely very heavily on the sprint goal as the ultimate requirement…
I feel we still need to implement the rest of the sprint goals before we close it." Discovery
receipt: the punt was institutionalized — the end-gate's own recommendation for a broken keystone
was approve-and-defer, the recommended hardening story was never created, and retro findings
produced 65+ stories (100% process-shaped, 0 shipped). The one sprint that added unplanned stories
to fix its assembled feature before re-gating (sprint-2026-05-30's CR-wave) is the only sprint where
the assembled feature got fixed before the gate closed.

### D4: Daily tasting — ≥10 minutes, reminded, briefed with expected-vs-reality — ADOPTED

**Research recommended:** Scheduled human walkthroughs (the only oracle with a 100% defect hit
rate), paid for by reducing document-review time.

**Decision:** No less than 10 minutes daily. Claude Code (a) reminds Steve on schedule and (b)
prepares a daily **tasting brief** generated from features.json plus whatever merged since the last
walkthrough: what should work today, what changed, 2–3 specific probes — model expectations tested
against reality. Concise decision-grade documents are NOT deleted; the rebalance moves attention
toward the app, not away from reporting. Findings enter intake under D6's owner-priority rule.

**Rationale:** Steve: "I absolutely agree that the HITL should spend WAY more time looking at the
app and way LESS time reading through docs. But concise docs of what is happening is also key…
no less than 10 min daily, and that means I need Claude Code to remind me AND prepare a document for
what we would expect today. Let's see if the model's expectations stand up to reality." Discovery
receipt: 5–6 app-launch days in 54; every walkthrough found a top-tier defect within minutes; the
dev database after 4 months held zero real user data.

### D5: Resume cards and session-start re-surfacing replace expiry-FAIL — ADOPTED (amends DEC-036)

**Research recommended:** A 48h gate expiry that escalates to FAIL.

**Decision:** Rejected as shaped; replaced. This practice serves a nights-and-weekends developer:
a gate may legitimately wait days. The contract instead: a gate never silently hangs and never
greets the developer with a wall of text. When a conduct finishes, it emits a **resume card** —
where we were, what merged, the one question pending — and Impetus leads the next session, whenever
it happens, with that card as the agenda. Escalation is re-surfacing at every session start with
rising prominence, never automatic failure. Combined with D2, the async-blocking decision shrinks:
the merge question is small and quick; closure waits for a tasting session already on the calendar.
Massive walls of text on any gate surface are a defect under the Decision-Grade Presentation
Standard.

**Rationale:** Steve: "Sadly this is not an 8 hour/day job for me. It's nights and weekends…
when I finally get back I need to be reminded where we were… We must do better than massive walls
of text that lead to complete demoralization and procrastination." Discovery receipt: the
sprint-2026-07-13 gate hung undecided for 11 days; the corpus's unexplained 7–18-day calendar gaps
were demoralized withdrawal, which makes gate ergonomics a delivery mechanism, not a nicety.

### D6: Intake owner-priority rule — ADOPTED

**Research recommended:** Observations sourced from the product owner driving the app must enter
intake at critical priority with a mandatory feature link, verified on the surface where the owner
met the behavior — never downgraded to `priority: low, feature_slug: null, verification: curl`.

**Decision:** Adopted as a validator rule in intake/triage.

**Rationale:** The discovery's sharpest intake specimen: Steve's twice-reported top defect
(campaign-context) entered the sprint as priority `low`, position #10, unattached to any feature,
routed to curl verification. The owner's direct outcome signal is the system's most expensive input
and was mechanically discounted at the door.

### D7: Verification re-keyed to assembled surface; DoD gains reachability — ADOPTED (amends DEC-029)

**Research recommended:** Re-key verification-standard.md's routing table from `change_type` (which
files the diff touches) to assembled surface (where a user meets the behavior); add one Definition
of Done item: "the capability is reachable from the application's entry point by a user who has read
no code."

**Decision:** Adopted as recommended. A story whose behavior a user meets in the chat UI is driven
through the chat UI regardless of its diff — or declares at plan time, out loud, that it cannot be.

**Rationale:** Steve: "Adopt with rec." All three council seats converged on this independently.
Receipt: `backend → curl` routed user-facing conversational stories to API-only verification; the
DoD's missing reachability item let a settings gear, an empty SurfaceType enum, and a heroes API
with no callers all count as done.

### D8: One command that IS the product + SHA admissibility — ADOPTED

**Research recommended:** A mise task per product that starts DB + migrations + backend + client
from one explicit pair of commits, refuses a mismatched pair, prints both SHAs, writes RUNNING.json;
a walkthrough that did not start from it is inadmissible as evidence, and every bug report cites the
two SHAs.

**Decision:** Adopted as recommended ("YES, Yes, yes").

**Rationale:** The chimera-build episode corrupted six layers of knowledge — Steve's live diagnosis,
a duplicate hotfix straight to main, a manufactured merge divergence, two audit documents, and the
council's own brief. Nobody may again review a build version control cannot name.

### D9: Runtime-model policy — test before building; context-defect hypothesis first — ADOPTED (adapted)

**Research recommended:** Before the next story: (a) five capture closes on merged trunk with
tool-call logging (does the UUID-strip regression starve Urd's tools?); (b) the same protocol
comparing hy3-preview against a mid-tier model. If the model fails, route Urd's write path to a
stronger model and add transactional receipts (read-back verify before "It is written.").

**Decision:** Adopted, with the hypothesis ordering set by Steve: the context/prompt explanation is
tested first and hy3-preview is retained pending results — it has tested well in tool use before,
and the council's UUID-strip finding (the governed fix removed the campaign UUID that four Urd tools
require as an argument) is itself a context defect, consistent with Steve's suspicion.

**Rationale:** Steve: "Agree it must be tested. But Hy3 tested very well in tool use in the past.
I suspect this is a context/prompt issue." The test protocol distinguishes never-called from
called-with-guessed-arguments, which separates the two hypotheses cleanly.

### D10: sprint-2026-07-13 disposition — merge now, sprint stays open — ADOPTED

**Research recommended:** Land or abandon the stranded branches this week; keep one implementation
of the campaign-name fix.

**Decision:** Merge both `sprint/sprint-2026-07-13` branches to main now under the D2 merge-gate
critique (code we are comfortable keeping), resolving `urd.py` by keeping the hotfix implementation
(campaign name AND UUID in the prompt) and deleting the governed test's
`assert str(campaign_id) not in result` — that assertion is the regression. Remove both
`.conduct-wt` worktrees; push both repos. The sprint does **not** close: it remains open under D3
until its goal conditions (capture persists reliably; Urd knows the campaign) verifiably pass in
the app, absorbing whatever condition-serving stories that requires.

**Rationale:** Steve: "we could merge all the branches from the sprint without closing the sprint…
I feel we still need to implement the rest of the sprint goals before we close it." This is the
first live exercise of D2/D3.

---

## Phased Implementation Plan

1. **Document** (this commit + follow-ons): DEC-040; architecture.md amendments; README delivery-loop
   section.
2. **Momentum skill/tooling changes:** `momentum-tools feature verify` + closure refusal;
   sprint-planning goal_conditions + plan-gate first fork ("after this sprint a GM can ___");
   conduct merge-gate execution semantics + resume card; verification-standard re-key + DoD item;
   intake owner-priority validator; Impetus N-passing report + pending-gate agenda; daily tasting
   reminder + brief generator.
3. **Nornspun execution:** D10 merge + worktree cleanup; features.json design reconciliation (D1);
   D8 launcher; D9 tests; then resume sprint-2026-07-13 under D3 to closure.

## Decision Gates

- **D9 gate:** if tool-call logging shows correct calls with the UUID restored, hy3 stays; if the
  model fails to call tools with correct context, Urd's write path moves to a stronger model and
  transactional receipts become a story before any new feature work.
- **D1 gate:** the features.json design reconciliation is complete only when every acceptance
  condition traces to the current design (or is explicitly marked design-independent) and the
  ground-truth baseline verdict (initially failing across the board) is recorded with build SHAs.
