---
id: DEC-029
title: Method-Routed Acceptance Validation — Harness Profile, Per-Sprint E2E Coverage, and the Unified Validate-Fix Loop
date: '2026-05-17'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-17'
prior_decisions_reviewed:
  - DEC-020 (Universal Agent Role Taxonomy — e2e-validator is one of the nine roles; its body is rewritten here)
  - DEC-021 (Document Ownership Map — extended: harness.json, frozen contracts, and the sprint E2E coverage plan gain owners)
  - DEC-023 (Agent Routing Table — harness.json co-locates as a sibling using the same defaults/project pattern; agent-resolve is reused for fixer routing)
  - DEC-025 (Fixer Role Resolution — the validate-fix loop's fixer routing builds on document-owner resolution)
  - DEC-027 (Skill/Agent Development + Change-Type Routing in Sprint-Dev — extended from agent selection to verification-method selection)
  - DEC-028 (Beads Substrate Adoption — reviewed; the loop must not hard-depend on beads pre-verdict; beads is ledger, not trigger)
architecture_decisions_affected:
  - DEC-020 — e2e-validator role body is de-Gherkin'd, de-stack-leaked, and made harness-driven
  - DEC-021 — ownership map gains momentum/harness.json (agent-builder/agent-guidelines), the per-story frozen contract and the sprint E2E coverage plan (sprint-planning)
  - DEC-023 — harness.json adopts the same defaults/project schema shape; the agent-resolve helper is reused for failure-to-fixer routing
  - DEC-027 — change-type routing extended from agent selection to verification-method selection at create-story time
  - acceptance-testing-standard.md — retired; the "process document" artifact class is dissolved
stories_affected:
  - routing-table-schema-and-implementation
  - change-type-routing-in-sprint-dev
  - acceptance-testing-process-and-standards
  - e2e-validator-black-box-hardening
  - e2e-validator-toolsearch-fix
  - e2e-and-qa-validator-prompts-branch-standalone-vs-team
  - e2e-client-side-coverage
  - e2e-validator-fixture-spec-sync-stale-reference-detection
---

# DEC-029: Method-Routed Acceptance Validation — Harness Profile, Per-Sprint E2E Coverage, and the Unified Validate-Fix Loop

## Summary

A working session reconsidered how Momentum performs acceptance/E2E validation, prompted by the observation that Gherkin is the wrong universal format and that validation is wildly project-dependent (Momentum validates skills/rules/hooks; a Compose app validates Android/iOS/desktop runtime; a web app uses Selenium/Playwright; some stories just need to run once). Three discovery agents audited the corpus and the existing design: Gherkin meaningfully fits under 5% of the 312-story corpus, the `e2e-validator` agent is hardwired to Gherkin in direct contradiction of `acceptance-testing-standard.md`'s own five-method matrix, a consumer project's stack (`finch`/PostgreSQL/FastAPI) is hardcoded into the supposedly-generic agent, no per-project harness abstraction exists, and no automated pre-human fix loop exists. The net direction: acceptance validation becomes **method-routed by story change-type** (Gherkin demoted to one rare method); the per-story verification contract is a **frozen spec of done**, not necessarily a per-story execution unit; project specifics move into a **per-project `momentum/harness.json`** mirroring the `agents.json` defaults/project pattern; E2E is **per-sprint, post-merge, and holistic** with transitive coverage credited; and code-review, AVFL, and E2E are recognized as **configured instances of one unified validate-fix loop**. The "process document" artifact class is dissolved — a governing standard with no enforcement is dead documentation, contrary to Momentum's thesis — so outputs compile into an enforced rule plus agent/workflow edits, with this decision carrying the rationale. The full sprint-dev rewrite the new pipeline implies is deliberately sequenced as a separate downstream decision/epic, not scoped here.

---

## Decisions

### D1: Method-routed verification; Gherkin demoted to one rare method — ADOPTED

**Developer framing:** Question whether Gherkin is the right E2E format across all stories, and route verification by what the story actually produces instead.

**Decision:** Acceptance validation is routed by story change-type to a method: skill-instruction → EDD eval; agent-definition → run-once; rule/hook → behavioral trigger; script/CLI and backend → execution test; app-UI (Compose/web) → smoke (build+launch+drive via Maestro/Playwright) then human residual; research/spike → document review. Gherkin remains available only for the rare deterministic-CLI/install case. A story may override its default method only with a written justification in the frozen contract, which the validator reads but cannot author.

**Rationale:**
Discovery confirmed Gherkin meaningfully fits well under 5% of the corpus, and the corpus itself repeatedly flags forced AC-by-AC Gherkin as a recurring anti-pattern. The five-method routing already existed in `acceptance-testing-standard.md`; the defect was the validator ignoring it. Verification weight should scale with change-type — most Momentum stories are light-tier; heavy machinery fires only for app-UI change-types.

---

### D2: Per-story frozen contract is the spec of done, not a per-story execution unit — ADOPTED (refined)

**Developer framing:** Keep an upstream, frozen, anti-gaming contract per story — but recognize it states what must be true, not necessarily how or when it is executed.

**Decision:** `sprint-planning` authors a frozen, method-polymorphic contract per story in `.momentum/sprints/{slug}/specs/` (`.eval.yaml` / `.trigger.md` / `.smoke.sh` / `.review.md` / `.feature`), hook-immutable after sprint activation. The contract is the immutable spec of done. It is explicitly not assumed to be a per-story execution unit — its verification may be discharged by a sprint-level scenario (see D8).

**Rationale:**
The author must be neither the dev agent nor the validator (anti-gaming). But "end-to-end" is inherently integration-level; treating every contract as its own isolated run is a category error that forces redundant testing. Separating "what must be true" (per-story) from "how the sprint proves it" (per-sprint) resolves that.

---

### D3: Per-project harness profile = sibling `momentum/harness.json` — ADOPTED

**Developer framing:** Project specifics shouldn't live in the generic agent. Co-locate a per-project harness with the agent-mapping document, in the format normal for `.momentum`-style config.

**Decision:** Per-project harness lives in `momentum/harness.json`, a sibling to `momentum/agents.json`, JSON, with the same `defaults` (plugin-shipped) / `project` (per-project) split, written by `agent-builder`/`agent-guidelines`. It declares environment startup + readiness probes, execution surface per change-type, driver binding (cmux / Skill-invoke / Maestro / Playwright / curl), platform/target matrix, human-review carve-outs, and a trivial-smoke escape.

**Rationale:**
A separate file keeps routing and validation-harness concerns each focused while reusing the proven `agents.json` schema pattern and writer. This removes the hardcoded `finch`/PostgreSQL/FastAPI leak from the generic agent and gives every consumer project (Momentum, Nornspun, web, REST) a first-class way to declare how it is driven.

---

### D4: Pre-human fix loop = AVFL extended with an E2E lens; sprint-dev rewrite sequenced downstream — ADAPTED

**Developer framing:** A human shouldn't have to discover that the app won't start or a button does nothing. Machines should catch 50–80% before any human verification, in an E2E→fix→E2E loop.

**Decision:** The pre-human fix loop is not a new engine — it is AVFL extended with an E2E behavioral lens: post-merge batch validation, PASS is sticky (passed scenarios are quarantined and never re-tested), failures are routed via `agents.json` to owning specialist agent(s) with independent failures fanned out in parallel, re-validate only the still-failing set plus a regression sweep, bound at 3 iterations, then escalate the residual to the developer. The model is decided here; the full sprint-dev rewrite required to realize it is sequenced as a separate, explicitly-dependent downstream decision/epic — not scoped into this decision.

**Rationale:**
Reusing AVFL's loop machinery collapses the build dramatically and keeps the existing post-merge practice intact. Sequencing the sprint-dev rewrite separately keeps the first increment (rule + harness + validator) small and the staging clear, while still locking the target model now.

---

### D5: create-story owns the verification-method decision with developer escalation — ADOPTED

**Developer framing:** The verification approach should be settled at story-creation time and surfaced to me when it's ambiguous — not silently chosen or blocked at validation time.

**Decision:** `momentum:create-story` owns selecting the verification method (from the change-type routing of D1) and escalates to the developer when ambiguous. It is not a validator-time fallback or block.

**Rationale:**
The method choice is a human-in-the-loop call best made when the story is shaped and its change-type and harness coverage are known, not deferred to a validator that would otherwise have to guess or hard-block.

---

### D6: sprint-planning authors contracts + an adversarial anti-insider-knowledge guard — ADOPTED

**Developer framing:** A real E2E test must be passable with no more knowledge than any ordinary user has. Contracts that need application insider knowledge are gameable.

**Decision:** `sprint-planning` authors the frozen contracts (confirming D2's authorship), and an adversarial guard rejects any contract whose verification requires insider/application knowledge — the contract must be verifiable with no more knowledge than an ordinary user of the system has.

**Rationale:**
This is the AVFL-adversary pattern applied to the contract itself. Insider-knowledge contracts smuggle implementation assumptions into the success criteria, defeating the black-box property that makes E2E meaningful.

---

### D7: Dissolve the "process document" artifact class; retire `acceptance-testing-standard.md` — ADOPTED

**Developer framing:** Momentum *is* the process. A standard that only governs agents but isn't loaded or enforced does nothing — that's the dead documentation Momentum exists to eliminate.

**Decision:** The "process document" artifact class is dissolved. There is no `momentum:process-doc` skill. A governing standard becomes an enforced rule (concise, obeyed by the validator and sprint-dev), cascading global → project → path-scoped per the authority hierarchy. The decision records the rationale; deep rationale may live as a lazily-loaded reference. `acceptance-testing-standard.md` is retired: its enforceable content moves into the rule, its rationale into this decision.

**Rationale:**
`acceptance-testing-standard.md` is the proof: it specified a five-method matrix the validator entirely ignored, precisely because the standard had no teeth. A standard with no enforcement inevitably drifts from the mechanism that should obey it. Encoding the practice as an enforced rule is the whole point of Momentum.

---

### D8: Per-sprint holistic E2E coverage plan; transitive coverage credited — ADOPTED

**Developer framing:** Don't validate in isolation what an integrated test already exercises. If a skill's E2E exercises its script, the script story needs no separate E2E; if the frontend calls the backend, validating the frontend covers the backend. So E2E is a per-sprint plan, not per-story.

**Decision:** E2E is per-sprint, post-merge, and holistic. `sprint-planning` authors a sprint E2E coverage plan: the minimal set of integrated scenarios, an explicit map of each scenario → the set of story contracts and files/spans it discharges, with transitively-covered stories credited ("covered by scenario X — rationale") and given no dedicated run. Anti-redundancy is the governing principle: never validate in isolation what an integrated scenario already exercises. Trivial stories may keep a tiny standalone check by exception only; the default is coverage-by-composition. Multi-type stories are covered by the highest-level scenario spanning their aspects rather than one check per type.

**Rationale:**
"End-to-end" is integration-level by definition; per-story E2E was a category error. Planning coverage at the sprint level — where the whole story set is known — exploits transitive coverage and eliminates redundant testing. The one risk, weaker failure localization, is handled by D4: the coverage plan records each scenario's story/file span so the routed fixer loop has its candidate set. Coverage (D8) and attribution (D4) compose with no gap.

---

### D9: Three-tier quality pipeline + four-step sprint-dev flow — ADOPTED

**Developer framing:** Code-review/QA is story-level before merge; AVFL is post-merge and validates merge correctness, not behavior; E2E is last and tells you if it works; E2E pass merges the sprint to main.

**Decision:** Adopt a three-tier pipeline separated by what each gate answers — code-review/QA (story-scoped, pre-merge, "correct in isolation"), AVFL (post-merge corpus, "coherent and correct in composition"), E2E (post-AVFL, whole system, "behaviorally correct"). Sprint-dev runs as: (1) sprint branches off main; (2) each story concurrently — git worktree off the branch → dev → code-review/QA → merge back to branch; (3) all merged → AVFL on the branch corpus; (4) E2E on the whole system; E2E pass → sprint merges to main, stories done. This relocates QA/code-review earlier (pre-merge per-story), superseding the current post-merge "Team Review" placement of qa-reviewer and e2e-validator. It is realized via the sequenced sprint-dev rewrite of D4.

**Rationale:**
The ordering is fail-fast and each gate is load-bearing and non-overlapping: correctness-in-isolation → correctness-in-composition → behavior-in-execution. Catching isolation defects before they pollute the branch, and corpus incoherence before expensive E2E, is the cheapest correct ordering.

---

### D10: Unified validate-fix loop primitive — ADOPTED

**Developer framing:** Code-review, AVFL, and E2E are all the same loop — validator finds issues, sends to fixers, fixers fix, re-validate, repeat.

**Decision:** Code-review, AVFL, and E2E are configured instances of one validate-fix loop primitive parameterized by lens (what is checked), scope (worktree / merged corpus / running system), fixer routing (the `agents.json` owner map / `agent-resolve`), quarantine (PASS-sticky), and bound (3 then escalate). The differing fix-application context — pre-merge fixes are isolated in worktrees and safely parallel, while post-merge AVFL/E2E fixes edit the shared branch and need coordination — is noted as a design constraint for the sprint-dev rewrite.

**Rationale:**
Collapsing three bespoke loops into one engine plus three lens configs is a strong simplification and keeps fixer-routing, quarantine, and bound behavior consistent across all three gates.

---

### D11: Loop driven by an abstracted state ledger; beads as optional substrate, not trigger — ADOPTED

**Developer framing:** Can beads pass stories between states, and can a state transition trigger the validator or fixer?

**Decision:** The validate-fix loop is driven by an abstracted state ledger. Beads MAY back it (work-item states/transitions, the `validates` edge type, `bd ready` + `--claim` for dependency-eligible scheduling), but the loop must not hard-depend on beads before the DEC-028 spike verdict — beads-backed if the spike lands, JSON-backed otherwise. Beads is the state ledger and scheduler input, not an autonomous trigger: beads has no event/webhook mechanism, so the trigger remains the sprint-dev loop reading ledger state and dispatching the validator/fixer. Orchestration stays in Momentum, on top of the substrate.

**Rationale:**
This matches the DEC-028 boundary exactly — beads as substrate under Momentum, enforced orchestration on top. Abstracting the ledger keeps D4/D8/D10 decoupled from the unresolved beads gamble while still allowing beads to provide state, dependency, and history if the spike succeeds.

---

## Phased Implementation Plan

| Phase | Focus | Timing | Key Stories |
|-------|-------|--------|-------------|
| 1 | Enforced verification rule (replacing `acceptance-testing-standard.md`) with method-routing, harness-profile requirement, and the anti-insider-knowledge guard; `momentum/harness.json` schema + defaults block; `e2e-validator` body rewrite (de-Gherkin, de-stack-leak, harness-driven); create-story method-selection step; sprint-planning contract + coverage-plan authoring | After `routing-table-schema-and-implementation` lands `agents.json` | routing-table-schema-and-implementation, acceptance-testing-process-and-standards, change-type-routing-in-sprint-dev |
| 2 | Full sprint-dev rewrite — four-step flow, three-tier pipeline, unified validate-fix loop primitive, PASS-sticky post-merge batch, abstracted state ledger (separate downstream decision/epic) | After Phase 1 stable | (new epic — to be defined) |
| 3 | Bind the state ledger to beads as substrate | Gated on DEC-028 spike verdict | (per DEC-028) |

---

## Decision Gates

| Gate | Timing | Question | Criteria |
|------|--------|----------|----------|
| Gate 1 | Before Phase 1 build | Does `agents.json` exist? | `routing-table-schema-and-implementation` merged; `momentum/agents.json` present with defaults/project schema |
| Gate 2 | Phase 1 complete | Is the rule + harness + rewritten validator stable on Momentum's own corpus? | Method-routed validation runs green on a real Momentum sprint with no Gherkin dependency and no hardcoded stack |
| Gate 3 | Before Phase 3 | Did the DEC-028 beads spike return go? | DEC-028 gate criteria met; beads authoritative decision recorded |
