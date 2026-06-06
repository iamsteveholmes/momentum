# Coverage Plan — sprint-2026-06-05-conduct-runnable

**Principle: Never validate in isolation what an integrated scenario already exercises.**

A dedicated verification run is justified only when no integrated scenario already observes a
story's acceptance behavior. Where one story's verification invocation drives the *same system
boundary* another story's behavior depends on — and genuinely *observes* that behavior, not
merely touches the same code — the second story is discharged `covered-by-composition` under the
integrated scenario. This plan is deliberately conservative: a story is folded into a composition
ONLY when the composition's own observable clauses would FAIL if the folded story's behavior were
absent. Where the integrated run would still pass while the story's distinguishing behavior is
broken (negative paths, escalation routing, edge cases the fixture does not seed), the story stays
`dedicated-run`.

The dominant integration scenario in this sprint is the **end-to-end fixture run**
(`conduct-e2e-validation-and-test-fixture`), which invokes the real Conductor against an activated
fixture sprint and drives the whole pipeline: preparation → per-story build + review → merged-result
review → end-to-end validation → single end-gate report → approve/push offer. Its Part-B clauses
require observing real file changes, real commits, a per-story review stream, a merged-result review
over the integrated diff, an E2E validation pass, and a single decision-grade end-gate report. That
single run necessarily exercises several other stories' boundaries — but only some of them are
*observed* to acceptance depth by its clauses. The rest remain dedicated.

---

## Integration Scenario 1 — End-to-End Fixture Build Run

**Driver story:** `conduct-e2e-validation-and-test-fixture`

**Description.** The developer invokes the in-session Conductor against the activated fixture sprint
and lets it run to the final approve/push gate without building or committing by hand. They then
inspect the repository (real edited/added files per story), the git history (the run's commits), the
per-story review streams surfaced during the run, the merged-result review over the integrated diff,
the end-to-end validation pass, and the single self-contained end-gate report — confirming the run
reached the gate with no mid-run question and offered push as a separate confirmation.

**File/behavior spans exercised.** The Conductor orchestrator skill + workflow; the per-story
build→review→fix dispatch path; the merged-result review step (the merge-review workflow over the
sprint-vs-main diff); the end-gate report renderer (single self-contained HTML report); the
planning-to-build handoff (the sprint record the run consumes — contract files present,
fingerprint-matched, runnable verification method, recognized coverage disposition).

**Discharges:**

- **`conduct-e2e-validation-and-test-fixture`** — *(driver; dedicated-run carrier, listed here for
  completeness, counted once below).* This is the dedicated run itself; its own clauses are the
  integration scenario.
- **`conduct-per-story-build-review-dispatch`** — The fixture run's clauses require that *each story
  is implemented and committed by the orchestrator* and that *a per-story review stream is surfaced
  before acceptance*; the run cannot pass unless this dispatch path actually carried every fixture
  story through build → review. The happy-path acceptance behavior is fully observed by the
  integrated run.
- **`avfl-merge-review-as-workflow`** — The fixture run's "merged-result validation" clause requires
  the build's merged-result review step to run the merge-review over the *precise integrated diff of
  the sprint branch against main*. That is exactly this story's own clause 5 ("the build's
  merged-result review step runs this review over the precise integrated diff"). The fixture run with
  more than one merged story observes the merge-review executing in its real build position; the
  story's headline integration claim is observed end to end.

**Rationale per discharged story.** `conduct-per-story-build-review-dispatch`: the fixture run will
not reach a clean end-gate unless the per-story build/review/commit dispatch produced real files and
commits for every story — its happy path is fully observed. `avfl-merge-review-as-workflow`: the
fixture run's merged-result-validation clause IS the merge-review's in-build integration clause, so
running the fixture over a multi-story branch observes the merge-review in situ.

> **Held back to dedicated-run (not folded), with reason — be rigorous:**
> - `conduct-endgate-decision-card-rendering` stays dedicated: the fixture sprint is arranged to reach
>   the gate *with nothing requiring a decision*, so the fixture run never observes a populated
>   decision card, the anti-rubber-stamp forcing function, or the routine-collapse/waved-off-reason
>   behavior. Those are the story's load-bearing clauses and the fixture does not seed them.
> - `conduct-coverage-disposition-discharge-consumer` stays dedicated: the fixture's handoff clause
>   confirms the record is *consumable* (contracts present, method runnable, disposition recognized),
>   but it does NOT seed a deferred-coverage story, so the discharge/leftover behavior is never
>   observed.
> - `conduct-e2e-finding-normalization-escalation` stays dedicated: the fixture E2E pass is arranged
>   to be *clean*; it never seeds a routine vs. high-stakes vs. urgent E2E finding, so normalization
>   and the escalation routing are not observed.
> - `conduct-endgate-request-changes-redispatch` and `reconcile-fix-disposition-with-conductor-scope-reverts`
>   stay dedicated: both depend on negative/edge paths (a change-request at the gate; a fix reverted
>   under scope discipline) the clean fixture run does not trigger.

---

## Integration Scenario 2 — Invocation Cluster: Conduct Drives a Build From a Fresh Session

**Driver story:** `conduct-wire-caller-and-discovery`

**Description.** In a fresh session the developer (a) asks the practice's always-on companion in
plain language to "run the sprint build" and observes it route to the Conductor rather than the old
wave loop, (b) types the canonical `/momentum:conduct` slash command directly and observes it bring
up the Conductor as the top-level session driver, and (c) lets the Conductor begin processing the
sprint's stories — proving the discovery path reaches a *live* engine, not dead code. Reaching a
live engine requires `momentum-tools` to resolve as a bare command so the Conductor's build
operations launch.

**File/behavior spans exercised.** The companion's routing/dispatch entry (front-door wiring); the
`/momentum:conduct` command registration and its dispatch to the Conductor skill; the Conductor's
begin-build path far enough to start processing stories; bare-`momentum-tools` PATH resolution used
by the build operations the started run invokes.

**Discharges:**

- **`conduct-wire-caller-and-discovery`** — *(driver; dedicated-run carrier; counted once below).*
  This scenario IS this story's dedicated run; its clauses cover front-door routing, direct dispatch,
  reaching a live engine, and sprint-dev coexistence.
- **`conduct-momentum-tools-path-resolution`** — *(folded as covered-by-composition).* This story's
  acceptance is that bare `momentum-tools` resolves and runs from any working directory in a
  non-interactive shell. The discovery scenario's clause "the conduct path actually drives a sprint
  build (leads to a live engine)" cannot pass unless the Conductor's build operations — which invoke
  `momentum-tools` as a bare command — resolve and run. Starting the build and seeing it process
  stories *observes* bare-`momentum-tools` resolution in the exact context that matters.

**Rationale per discharged story.** `conduct-momentum-tools-path-resolution`: the "leads to a live
engine, not dead code" clause is observably satisfied only if bare `momentum-tools` resolves when
the started build calls it; the smoke checks (resolves from any dir, no command-not-found) are a
strict subset of what "the build begins processing stories" demonstrates.

> **Held back to dedicated-run (not folded), with reason:**
> - `conduct-entry-point-command` stays dedicated: although typing `/momentum:conduct` appears in
>   this scenario, its own acceptance includes the *command-listing discoverability* clause and the
>   *single-canonical-name / no-ambiguous-duplicate* clause, which the discovery scenario does not
>   enumerate or observe. Resolution alone is shared; discoverability and name-uniqueness are not.
> - `conduct-register-skill-and-refresh-cache` stays dedicated: its acceptance is about the skill
>   appearing in the *live invocable-skill list after a refresh + fresh session* and being invocable
>   via both paths with a clean load — a registration/cache property the build-driving scenario does
>   not observe (a session can drive conduct without the skill being correctly listed for *every*
>   invocation path, and without the refresh having taken effect for a peer).

---

## Stories Not Covered by Any Composition — `dedicated-run`

Each of the following requires verification the compositions above do not observe. They keep their
own dedicated run.

| Story | Why a dedicated run is required |
|---|---|
| `conduct-e2e-validation-and-test-fixture` | The driver/carrier of Scenario 1; its skill-invoke run IS the integrated build. |
| `conduct-wire-caller-and-discovery` | The driver/carrier of Scenario 2; routing + live-engine + sprint-dev coexistence are its own clauses. |
| `conduct-entry-point-command` | Command-listing discoverability and single-canonical-name uniqueness are not observed by the build-driving scenario. |
| `conduct-register-skill-and-refresh-cache` | Post-refresh live-invocable-skill listing, dual invocation paths, and clean load are registration/cache properties no build run observes. |
| `conduct-momentum-tools-path-resolution` | *(Covered by Scenario 2 — listed here only for the checklist; counted as covered-by-composition.)* |
| `conduct-planning-emit-contract-schema` | Runs *planning* (not a build): ordered nine-field header, closed-enum method = harness_profile, frozen checksum match, merge-independence flag, one-contract-per-story counts. Upstream of any build; not observed by the fixture run. |
| `conduct-endgate-decision-card-rendering` | Requires a sprint that *produces a stakes escalation* to observe populated decision cards, the anti-rubber-stamp forcing function, routine-collapse, and waved-off reasons. The clean fixture seeds none of these. |
| `conduct-coverage-disposition-discharge-consumer` | Requires a *deferred-coverage* story to observe the named integration scenario being run, the discharge-on-pass, and the leftover-on-fail. The fixture does not seed a deferral. |
| `conduct-e2e-finding-normalization-escalation` | Requires *seeded* routine vs. high-stakes vs. urgent E2E findings to observe normalization to self-contained items and escalation routing. The fixture E2E pass is clean. |
| `conduct-verification-method-enum-alignment` | Document-correction + story-creation-skill behavior: routing table → closed-enum tokens matching harness driver keys, contract-format guide cleanup, no free-text method stamped. Not exercised by any build run. |
| `conduct-planning-reconcile-gherkin-and-specs-rule` | Planning-time invariant: exactly one contract of record per non-app story (no duplicate `.feature`), and the dev-never-accesses-specs prohibition removed. Observed at planning, not build. |
| `avfl-merge-review-as-workflow` | *(Covered by Scenario 1 — listed here only for the checklist; counted as covered-by-composition.)* |
| `conduct-endgate-request-changes-redispatch` | Requires *submitting a change request at the gate* and observing act-then-re-render-then-return — a negative/edge path the clean fixture run never enters. |
| `conduct-simplify-and-convergence-questions` | Static workflow-text properties: cleanup pass as a runnable step, single cleanup-trigger rule, one canonical retry bound, named deeper-review owner, every terminal state reachable. Read from the skill, not observed in a run. |
| `conduct-cleanup-dead-agent-paths-and-validate-resolve` | Bash smoke over `momentum-tools agent resolve`: dead roles removed or fail loudly, build-critical roles resolve to existing files, no success-pointing-at-missing-file. A targeted negative-path sweep no build run performs. |
| `conduct-per-project-verification-harness-config` | Document review of `verification-harness.json`: per-project override, real runners (not `skip`) for app/backend/script surfaces, startup/readiness populated, all-skip carve-out stated. Config-file inspection, not a build. |
| `contract-seam-stories-two-sided-review-scope` | Requires a *seam story* and a *deliberate producer/consumer field-shape mismatch* to observe two-sided scoping and the cross-side gate failure. The fixture seeds no mismatch. |
| `reconcile-fix-disposition-with-conductor-scope-reverts` | Requires a *fix reverted under scope discipline* to observe the not-fixed status, the non-overstated scorecard, and the re-routed follow-up. The clean fixture produces no revert. |
| `decision-grade-presentation-standard` | A cross-surface standard over five live surfaces (greeting, decision-walk, assessment, retro, build report) including a tight-vs-complete boundary probe and a work-depth-invariance probe. The fixture observes at most one surface, not the standard across all five. |
| `conduct-per-story-build-review-dispatch` | *(Covered by Scenario 1 — listed here only for the checklist; counted as covered-by-composition.)* |

---

## Validation Checklist — all 20 slugs accounted for exactly once

| # | Story slug | Disposition |
|---|---|---|
| 1 | `conduct-momentum-tools-path-resolution` | covered-by-composition (Scenario 2) |
| 2 | `conduct-entry-point-command` | dedicated-run |
| 3 | `conduct-register-skill-and-refresh-cache` | dedicated-run |
| 4 | `conduct-wire-caller-and-discovery` | dedicated-run (driver, Scenario 2) |
| 5 | `conduct-planning-emit-contract-schema` | dedicated-run |
| 6 | `conduct-per-story-build-review-dispatch` | covered-by-composition (Scenario 1) |
| 7 | `conduct-endgate-decision-card-rendering` | dedicated-run |
| 8 | `conduct-coverage-disposition-discharge-consumer` | dedicated-run |
| 9 | `conduct-e2e-finding-normalization-escalation` | dedicated-run |
| 10 | `conduct-e2e-validation-and-test-fixture` | dedicated-run (driver, Scenario 1) |
| 11 | `conduct-verification-method-enum-alignment` | dedicated-run |
| 12 | `conduct-planning-reconcile-gherkin-and-specs-rule` | dedicated-run |
| 13 | `avfl-merge-review-as-workflow` | covered-by-composition (Scenario 1) |
| 14 | `conduct-endgate-request-changes-redispatch` | dedicated-run |
| 15 | `conduct-simplify-and-convergence-questions` | dedicated-run |
| 16 | `conduct-cleanup-dead-agent-paths-and-validate-resolve` | dedicated-run |
| 17 | `conduct-per-project-verification-harness-config` | dedicated-run |
| 18 | `contract-seam-stories-two-sided-review-scope` | dedicated-run |
| 19 | `reconcile-fix-disposition-with-conductor-scope-reverts` | dedicated-run |
| 20 | `decision-grade-presentation-standard` | dedicated-run |

**Tally:** 20 stories. 3 covered-by-composition (slugs 1, 6, 13). 17 dedicated-run (including the two
composition drivers, slugs 4 and 10). Every slug appears exactly once. ✅
