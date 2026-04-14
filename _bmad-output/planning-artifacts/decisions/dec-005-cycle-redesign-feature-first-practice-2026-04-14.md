---
id: DEC-005
title: Momentum Cycle Redesign — Feature-First Practice, North Star Floors, Running-App Verification, and Failure as Diagnostic
date: '2026-04-14'
status: decided
source_research:
  - path: _bmad-output/research/adapting-agile-for-gen-ai-development-2026-04-13/synthesis/synthesis.md
    type: gemini-deep-research
    date: '2026-04-13'
  - path: _bmad-output/research/adapting-agile-for-gen-ai-development-2026-04-13/cycle-analysis/analysis-document.md
    type: architecture-analysis
    date: '2026-04-13'
prior_decisions_reviewed:
  - DEC-002 (Feature Visualization and Developer Orientation) — status enum superseded; feature/epic orthogonality claim superseded; schema extended
  - DEC-004 (Feature Schema Value-First Redesign) — value_analysis extended with North Star + Judgment Frame; honest-status principle operationalized; inherited status enum superseded
architecture_decisions_affected:
  - Decision 26 (Two-Layer Agent Model) — clarified; role-specific guidelines must include value-floor orientation and platform-varying verification
  - Decision 27 (Transcript Audit Retro) — superseded-partial; retro gains feature-state hygienist role, failure-naming discipline, gap-check, feature-grain closure
  - Decision 28 (Triage vs Refinement Distinction) — clarified; gap-check formally placed at refinement
  - Decision 29 (Sprint Planning Builds the Team) — superseded-partial; planning commits at feature grain, adds North Star + gap-check + Judgment-Frame inheritance, mixed work types
  - Decision 30 (Gherkin Separation) — clarified; running-app verification extends black-box contract to value-floor level
  - Decision 31 (AVFL at Sprint Level) — clarified; AVFL and E2E both primary gates for distinct concerns
  - Decision 34 (AVFL Scan Profile and Hybrid Resolution Team) — clarified; two-gate split formalized
  - Decision 35 (Agent Definition Files vs SKILL.md Boundary) — clarified; boundary preserved
  - Decision 36 (Sprint Lifecycle State Machine) — superseded-partial; sprints host mixed work types; parallel feature state machine added
  - Decision 39 (Quick-Fix Bypass-Sprint Lifecycle Path) — clarified; quick-fix placed in defect/maintenance story-type frame
  - Decision 40 (Change-Type-Driven Validator Selection) — clarified; running-app behavioral verification is mandatory non-optional
  - Decision 42 (Distill Execution Path and AVFL Profile) — clarified; continuous hook-trigger becomes binding contract
  - Decision 43 (Retro Phase 0 Session Analytics) — clarified; failure-as-diagnostic discipline hardens naming output
  - Decision 44 (Feature Artifact Layer) — superseded-partial; feature_slug on stories; terminal states replace status enum; Judgment Frame fields added
  - Decision 45 (Feature Status Skill Standalone with Dual Output) — superseded-partial; status enum change; retro becomes status-writer
  - Decision 46 (Feature Status Cache Pattern) — clarified; cache summary reflects new enum
  - Decision 47 (Sprint Summary at Retro Boundary) — superseded-partial; feature grain + North Star + ordinal framing + terminal transitions restructure summary
  - Decision 49 (Feature Grooming Skill Orchestrator Pattern) — superseded-partial; DDD epic model + Judgment Frame fields + sub-skill callable from refine
stories_affected:
  - encode-epic-semantic-model
  - develop-epic-command
  - sprint-planning-investigate-first
  - sprint-dev-phase-7-gate
  - verify-skill
  - plugin-dev-e2e-validation-workflow
  - e2e-validator-black-box-hardening
  - status-transition-walk-mode
  - retro-triage-handoff
  - retro-prior-action-item-cross-ref
  - distill-worktree-isolation
  - create-story-update
  - sprint-scope-tracking
  - team-review-with-teamcreate
  - findings-ledger-accumulates-quality-findings-across-stories
---

# DEC-005: Momentum Cycle Redesign — Feature-First Practice, North Star Floors, Running-App Verification, and Failure as Diagnostic

## Summary

This SDR captures fourteen decisions from an owner-conversation held against a research corpus (adapting-agile-for-gen-ai-development, 2026-04-13) and a 10-agent cycle analysis of the Momentum practice. The net direction: Momentum moves from a story-centric, spec-adequacy-gated practice toward a feature-first, value-floor-gated, running-app-verified practice. Features become the primary human-judgment grain. Epics are repositioned from taxonomy into DDD-style sub-domain boundaries that hold features and the full mix of non-feature work. Each sprint on a feature must cross its own value-floor (a North Star for the sprint) with every cycle agent oriented toward that crossing. Running-app behavioral verification becomes mandatory — isolated from code, tool-varying by platform, never substituted by code-reading. Failure becomes a legitimate retro category to be named specifically, not softened into "learning." AVFL is preserved as the primary quality gate and given a clarified role distinct from the new running-app value-gate. Distill is promoted to a continuous hook-triggered primitive but retains developer approval and spec-integration. The Judgment Frame is adopted per-feature with story inheritance. Gap-check placements are restricted to refinement, sprint planning, and retro. The key owner-observed failure mode — five-to-ten sprints of spec-correct stories failing to deliver user value — is diagnosed as the absence of a value-floor discipline at feature grain; the decisions in this SDR collectively install that discipline.

---

## Decisions

### D1: Features as First-Class Value Units — ADOPTED

**Research recommended:** Make features first-class in the Momentum cycle. Stories carry a `feature_slug` link. Sprint-planning commits at feature grain. Retro closes features explicitly. `create-story` reads `features.json`. Feature content (value_analysis, acceptance_condition, system_context) cascades into the stories that inherit from the feature.

**Decision:** Adopted as recommended. Features are the primary human-judgment unit; stories remain the AI's execution unit. The feature layer is wired into every cycle phase that currently ignores it.

**Rationale:**
The focus on value is what has been missing. Sprint after sprint has delivered spec-correct stories without delivering value to the user. The feature is the right concept to carry that value weight — stories are too granular to anchor value judgments, and nothing above the feature layer (PRD, vision) is operational enough to govern sprint decisions.

---

### D2: Epics as DDD Sub-Domain Boundaries — ADOPTED

**Research recommended:** The cycle analysis raised two options for the epic layer: fold epic-grooming into refine (Option 8) since epics were pure taxonomy with no value mapping; or reshape epic-grooming into a new role. The research corpus does not explicitly prescribe an epic concept.

**Decision:** Adopted as a reshape. Epics are repositioned as DDD-style sub-domain boundaries. Features remain value-scoped (user capability); epics become domain-scoped (a cluster of features plus the non-feature work that completes a product sub-domain). Epics provide PRD completeness coverage and domain boundaries that features alone cannot.

**Rationale:**
Features must be the primary focus but they are limited to user-valued stories. Epics give a container for features plus everything else necessary for a domain. Five different story types (feature / maintenance / defect / exploration / practice) exist; only the first type fits inside a feature. The rest are part of a domain and should not be forced into a feature to be legible. Feature is not the only high-level concept the practice needs.

This directly **supersedes DEC-002 D1's claim** that "features and epics are orthogonal — epics group by theme, features group by user-observable capability." Epics are no longer theme-groupings; they are domain boundaries.

---

### D3: North Star Per Sprint on a Feature, with All Agents Oriented Toward It — ADOPTED (with adaptation)

**Research recommended:** Each feature has a single fixed North Star. Sprint 1 on a new feature must cross the value-floor (walking skeleton). Subsequent sprints on the feature deliver incremental refinement. Pre-floor sprints are explicitly labeled as infrastructure, not value delivery.

**Decision:** Adopted with adaptation. Each sprint touching a feature has its own North Star — a value-floor it must cross — not just Sprint 1. Subsequent sprints install new floors as the feature matures. Every cycle agent (SM, dev, QA, architect, validator, any other) is oriented toward the current sprint's floor; it is not just a planning concern.

**Rationale:**
I have spent no fewer than four sprints trying to get a working UI talking to the LLM, and every time that was my focus, we delivered every carefully-speced story and still did not reach the floor. We MUST have that focus or we are not delivering anything of value. Every agent from SM to dev to QA to architect to validator must hold the current floor as the orientation for their work during the sprint. A single-floor-per-feature model is insufficient because subsequent sprints also need a crossing discipline — each sprint is its own "did we move the user?" judgment.

---

### D4: Ordinal Value, Not Cardinal — ADOPTED

**Research recommended:** Value is directional and ordinal, not arithmetic. Do not report "% done" or "X% of feature delivered." Sprint close reports observable user-behavior deltas — what the user can now do that they could not before.

**Decision:** Adopted. Features are never reported as a percentage or fraction of completion. Sprint-close reports enumerate observable capability deltas. Velocity and story-count metrics are not value measurements.

**Rationale:**
Cardinal measurement means nothing to a user and delivers no value. Saying "I delivered the primary or first feature increment" means something; saying "60% done" does not. My experience has always been that cardinal measurements are at best not very useful and at worst wholly misleading.

---

### D5: Sprints Survive as Governance Rhythm with Mixed Work Types — ADOPTED

**Research recommended:** Sprints survive in AI-native practice but their purpose changes from delivery throttle to learning cadence and governance window. Non-feature work (maintenance, defects, exploration, practice/meta-work) is legitimate first-class work that does not need value justification.

**Decision:** Adopted with explicit taxonomy. A sprint accommodates five story types: **feature** (advances a value floor), **maintenance** (e.g., build upgrades, dependency bumps), **defect** (fixing what is broken), **exploration** (research, spikes), and **practice** (meta-work on the Momentum harness itself). Story type determines the evaluation question: features are evaluated against the sprint's North Star; non-feature work is evaluated against its own justification (unblock feature velocity, prevent failure, reduce uncertainty, improve the harness). Epics (D2) are the domain container that holds all five types.

**Rationale:**
Features alone do not capture everything. Organizations that care only about user value move away from doing work that needs to be done — upgrades, bug fixes, utility work. That quickly starts to smell. Sprint planning is the opportunity to determine what rises to current priority even when it is not user-valued.

---

### D6: Feature Terminal States — Done, Shelved, Abandoned, Rejected — ADOPTED (with adaptation)

**Research recommended:** Features need explicit terminal states to prevent drifting into zombie ambiguity. Three states proposed in the cycle-analysis conversation: Done / Shelved / Abandoned.

**Decision:** Adopted with a fourth state added. Four terminal states: **Done** (user satisfied; no further enhancement expected), **Shelved** (paused indefinitely with outstanding stories; may return), **Abandoned** (no further work intended; outstanding stories explicitly closed; the feature remains as-is), **Rejected** (rollback/remove; the feature is actively unmade from the system). All four are reversible — a feature in any terminal state can return to an open state when conditions change.

**Rationale:**
Abandoned means "closing out stories, no more work, but the feature remains." Rejected covers the distinct case where the feature should be removed, not just left alone. Terminal status is an explicit intention of governance, and the four states cover the four intentions I need. Reversibility matters because any terminal judgment may be revisited when new information arrives.

This **supersedes DEC-002 D1's status enum** of working / partial / not-working / not-started (and DEC-004's inherited reliance on that enum). The new enum is Done / Shelved / Abandoned / Rejected for terminal states (plus the existing active states).

---

### D7: Failure as a Legitimate Diagnostic Category — ADOPTED

**Research recommended:** Retro must be willing to name failure specifically. The "everything is learning" softening removes diagnostic signal. Systemic failure (wrong North Star, wrong spec, wrong approach) is diagnosable and nameable; this is distinct from personal blame.

**Decision:** Adopted. Retro is required to name failure explicitly when the sprint or feature fails to cross its floor, when the approach needed a rewrite, or when a feature failed to improve usability despite delivery. The why or solution may be initially unknown; the failure is still named.

**Rationale:**
Failure is explicitly not a blame game. It is the recognition that something went wrong that should be corrected in future sprints. Even when the cause is not understood, multiple failures should be recognized as such and worked on as top priority. If we do not recognize failure, what is there to fix? Successfully learning a lesson is different from learning from a failure — failures stick with an organization and a product in a different way and must be diagnosed specifically to be addressable.

---

### D8: Retro Gains Feature-State Hygienist Role — ADOPTED

**Research recommended:** Retro should be the governance moment where features transition between states explicitly. Features drifting between statuses via background recalculation rather than conscious judgment is the current failure mode; retro is the natural place for explicit transitions.

**Decision:** Adopted. Each retro performs per-feature state transitions for any feature touched by the sprint — confirming floor crossing, or transitioning to Done / Shelved / Abandoned / Rejected (D6). Retro is the feature-state writer, not just a reader of feature-status output.

**Rationale:**
Retro is the natural fit to consider feature state. By the end of a sprint, you have learned something new, and retro is the moment to make your best-educated decision about whether the feature is complete, paused, abandoned, or should be removed.

---

### D9: Judgment Frame per Feature, Inherited by Stories — ADOPTED (with adaptation)

**Research recommended:** A four-part human-readable judgment artifact — Intent / Done-state-for-a-stranger / Anti-goals / Review focus — that exists above the AC as a glanceable review surface. Whether it lives per-story, per-feature, or both was unresolved in the research.

**Decision:** Adopted at the feature layer. The Judgment Frame is produced at feature-grooming. Stories that belong to a feature inherit the frame; non-feature stories (maintenance, defects, exploration, practice) do not have a Judgment Frame (they are justified by their story type, not by value delivery). The Frame is the primary artifact the developer reads for go/no-go judgment at sprint planning approval, sprint close, and feature-state transitions.

**Rationale:**
I do not want to think at the level of stories delivering value. I have had bad experiences with that. A single story is not meant to deliver value and rarely does by itself. The feature is what delivers value, so the judgment artifact belongs at the feature grain.

---

### D10: Gap-Check Placed at Refinement, Sprint Planning, and Retro — ADOPTED (with adaptation)

**Research recommended:** The here-to-there gap check has multiple candidate placements: intake, refinement, sprint planning, sprint close, or above the cycle. The analysis did not converge.

**Decision:** Adopted with specific placements. Gap analysis lives at **refinement** (evaluating backlog shape against floor direction), **sprint planning** (committing sprint scope against the floor it must cross), and **retro** (judging whether the floor was crossed and what comes next). Intake is excluded because stories at intake are too granular for a value-to-customer conversation; every-phase continuous checking is unnecessary once these three gates are in place.

**Rationale:**
It does not make sense to talk about stories removed from value to customer, so intake is the wrong layer. Sprint planning is the main place to ensure the coming sprint is pointed at a floor. Retro is where we consider whether we succeeded or failed and what comes next. Refinement fills the role of keeping the backlog shaped against the floor over time.

---

### D11: Running-App Behavioral Verification Is Mandatory, Isolated, and Tool-Varying — ADOPTED (with adaptation)

**Research recommended:** Adopt the Codecentric pattern — `.claudeignore` + symmetric permissions + tester subagent cannot read `src/` + Playwright MCP against running app + red-phase discipline + self-test of isolation. This addresses CAISI agent-cheating findings and correlated-signal failures in AVFL.

**Decision:** Adopted with platform-appropriate tooling. The principle is absolute: all behavior verification runs against the running app, wholly segregated from code, under no conditions accepting anything less than running-app behavior. Automated verification is preferred; manual is allowed as a fallback; no story finishes without verification. Tooling varies by platform: **cmux + claude-in-terminal** for Momentum-the-practice; **Android emulator + Maestro + iOS simulator (plus connected devices)** for Nornspun; **Playwright** for webapps; other platforms documented as they arise. Verification applies at the value-floor (feature/system) level, not just at story level — this is the correction to the past failure of story-only validation. The LLM's tendency to cheat on behavioral verification is a known hard problem and the ongoing goal is to prevent it.

**Rationale:**
Past sprints focused only on story validation and did not verify actual functioning of the feature or system. That is our gap and we must adopt a mandatory running-app behavioral verification at the floor level. Playwright is likely not appropriate for anything except webapps, so the tool choice has to follow the platform. Manual verification stays as a fallback, but automated is always preferred. The biggest thing here is verifying the floor crossing — which is the scope expansion the past practice missed.

A significant gap flagged: cross-platform running-app verification tooling for non-web cases is under-researched and will likely need its own research spike.

---

### D12: Distill Becomes Continuous with Developer-Approval Gate Preserved — ADOPTED (with adaptation)

**Research recommended:** Move distill from retro sub-step onto continuous hooks (per-story-merge, per-intervention, per-failure). Retro becomes a thin audit of "did we distill everything we should have?"

**Decision:** Adopted with the developer-approval and spec-integration steps preserved. Distill fires continuously on hooks as recommended, but a distillation still requires developer understanding, approval, and integration into specifications — Momentum is a plugin and a distillation is often more than a quick rule edit. The ceremony around distill itself is acknowledged as imperfect (sometimes heavyweight, sometimes over-automated inside retros); further iteration on the distill skill is expected.

**Rationale:**
I agree wholly with distill being continuous — it has already become a crucial part of what we do. But a distillation is not just a rule edit; it often requires human understanding and deliberate integration into specifications because Momentum is a plugin. The current level of ceremony around distillations is not quite right in either direction, so I approve the continuous-firing principle but want the approval gate preserved while we iterate on how distill works.

---

### D13: AVFL as Primary Quality Gate, Distinct from E2E Value Gate — ADOPTED

**Research recommended:** The sprint-dev findings asked whether AVFL's Phase 4 / 4b / 4c / 4d apparatus still earns its cost once the Codecentric isolated harness is built. The challenger argued AVFL produces correlated signal (coherence, not quality); the analyst argued it should be reshaped.

**Decision:** Adopted as a role clarification rather than a reshape. AVFL remains the **primary quality gate** — evaluating inputs and outputs for errors, inconsistencies, duplicates, coding-standard violations, testing anti-patterns, doc freshness, reference integrity — using the enumerator/adversary pattern to reduce variance and guard against hallucination. The new running-app verification (D11) is the **primary value gate**, verifying behavior and floor crossing. Both gates are primary for their distinct concerns; neither supersedes the other.

**Rationale:**
The E2E verifier checks whether functionality and behavior exists and works; AVFL evaluates inputs and outputs for errors, inconsistencies, duplicates, and lens-specific issues using the same inputs the dev used but a different agent context, with enumerator/adversary to improve findings and avoid hallucinations. These serve different purposes. If E2E verifies behavior exists and works, that says nothing about whether coding standards were followed, testing anti-patterns were used, docs were updated, or references still work. AVFL is still the primary quality gate and is wholly separate from the verification of behavior and value.

---

### D14: Epic-Grooming Stays Standalone with DDD Rewrite; Refine Can Call It and Feature-Grooming as Sub-Skills — ADOPTED (with adaptation)

**Research recommended:** Option 8 in the trade-off map proposed folding `epic-grooming` into `refine` as pure-taxonomy cleanup. D2's adoption changes the premise — epics are no longer pure taxonomy.

**Decision:** Adopted as a sub-skill consolidation path with a rewrite. `epic-grooming` remains a standalone skill but is rewritten against the new DDD sub-domain epic semantics (D2). `refine` gains the ability to call both `epic-grooming` and `feature-grooming` as sub-skills. Both remain independently invokable until they stabilize — they can require hours of back-and-forth with the developer. Once stable, a quick pass during `refine` becomes the expected invocation.

**Rationale:**
Epic-grooming still makes sense as a standalone skill, more substantively evaluating domain-completeness under the DDD definition. I do not see using it outside of refine, so it is fine for refine to call it as a sub-skill. The same applies to feature-grooming. Both make sense to call on their own until they are more stable — they can be hours of developer back-and-forth during stabilization. By the time they are stable, a quick pass during refine is just right.

---

## Phased Implementation Plan

These decisions cascade. Their order of implementation matters because later decisions depend on data-model changes earlier decisions introduce.

| Phase | Focus | Enables | Example stories |
|-------|-------|---------|-----------------|
| 1 | **Data model foundation** — features gain `north_star` (D3), Judgment Frame fields (D9), and new terminal-state enum (D6). Stories gain `feature_slug` and story_type (D1, D5). Epic schema rewritten for DDD (D2). | All subsequent phases; nothing else can land without the new data model | `encode-epic-semantic-model`, `create-story-update`, `status-transition-walk-mode` |
| 2 | **Skill updates for new grain** — `feature-grooming` rewrite (D9, D2), `epic-grooming` rewrite (D2, D14), `refine` sub-skill orchestration (D14), `create-story` reads features.json (D1, D9) | Planning and dev to operate at feature grain | `develop-epic-command`, updates to `feature-grooming` and `epic-grooming` |
| 3 | **Sprint-planning restructure** — feature-grain commits, North Star per sprint, mixed-work-type classification, gap-check (D1, D3, D5, D10) | Sprint-dev to be oriented toward floor crossing | `sprint-planning-investigate-first`, `sprint-scope-tracking` |
| 4 | **Running-app verification harness** — isolated tester pattern per platform (D11); start with cmux+claude for Momentum; document non-web platform tooling gap for follow-up research | Stories to have a mandatory floor-level verification gate | `verify-skill`, `plugin-dev-e2e-validation-workflow`, `e2e-validator-black-box-hardening`, `sprint-dev-phase-7-gate` |
| 5 | **Retro restructure** — failure-naming discipline (D7), feature-state hygienist role (D8), gap-check (D10), ordinal framing (D4) | Feature lifecycle governance to complete the loop | `retro-triage-handoff`, `retro-prior-action-item-cross-ref`, sprint-summary changes |
| 6 | **Distill continuous hooks** — per-merge / per-failure / per-intervention triggers with preserved developer-approval gate (D12) | Continuous harness improvement at AI velocity | `distill-worktree-isolation` |
| 7 | **AVFL role clarification** — no mechanical change; documentation and agent-prompt updates reflecting D13's quality/value gate split | Clean separation between AVFL and E2E in practice documentation | AVFL cluster stories (clarifications, not rewrites) |

The walking skeleton of this redesign is Phase 1 + a minimal Phase 3 — enough data model + sprint-planning to commit a feature-first sprint — followed by Phase 4 to prove running-app verification works. Phases 2, 5, 6, 7 elaborate.

---

## Decision Gates

These are re-evaluation points during implementation where the practice should stop and check whether the decisions are playing out as intended.

| Gate | Timing | Question | Criteria |
|------|--------|----------|----------|
| G1 | After Phase 1 lands | Is the new feature schema legible? | The developer can read a feature record and understand Intent / Done-state-for-a-stranger / Anti-goals / Review focus without consulting elsewhere |
| G2 | After first Phase 3 sprint | Did the sprint commit at feature grain with a North Star? | Sprint record shows a `north_star` per touched feature; every agent prompt references it |
| G3 | After first Phase 4 verification | Does the running-app harness actually block completion when behavior is absent? | Deliberately introduce a behavior gap; confirm the verifier fails the story; confirm no escape via code-reading |
| G4 | After first Phase 5 retro | Did retro name a specific failure if one occurred? | Retro output contains a "Failure" section with systemic cause, or explicitly states no failure occurred this sprint |
| G5 | After three sprints on a single feature | Is the value-floor discipline detectable in practice? | At least one sprint closed with a new observable capability delta; no sprint silently punted a floor crossing |
| G6 | After one quarter of the new practice | Has a feature reached Done or a conscious Shelved/Abandoned/Rejected? | Feature state transitions are being made consciously at retro rather than drifting |

---

## Full Story Audit

The `stories_affected` frontmatter lists the load-bearing subset. The complete audit below covers all backlog stories touched by DEC-005, grouped by decision cluster. Ongoing backlog refinement should reconcile each of these against the new model during Phase 1 and Phase 2 of implementation.

### Feature layer (D1, D2, D6, D9)
- `backlog-add-command` — gain `feature_slug` and Judgment Frame inheritance
- `create-story-update` — read features.json; emit feature linkage; inherit Judgment Frame
- `create-story-advanced-elicitation` — probe Intent / Done-state / Anti-goals
- `story-spec-completeness-checklist` — validate feature link and Judgment Frame presence
- `encode-epic-semantic-model` — rewrite for DDD sub-domain semantics
- `propagate-decision-skill-vocabulary` — align with new feature/epic model and terminal states
- `develop-epic-command` — rewrite against DDD sub-domain model
- `triage-skill` — routing must know feature/epic boundaries and terminal states
- `status-transition-walk-mode` — reflect new terminal states and story types

### Sprint planning, sprint-dev, governance rhythm (D1, D3, D4, D5, D10, D11)
- `sprint-planning-investigate-first` — commit at feature grain; North Star; gap-check
- `retro-and-planning-ux-defaults` — both skills gain new phases
- `sprint-scope-tracking` — classify by story type
- `sprint-log-directory-enforcement` — restructure around features + North Star
- `sprint-slug-backfill` — sprint index includes `feature_slug`
- `sprint-dev-phase-7-gate` — running-app behavioral verification at floor level
- `team-review-with-teamcreate` — feature-level smoke tests + behavioral verification mandatory
- `impetus-lifecycle-and-handoff-fix` — feature-state hygienist transitions affect lifecycle display
- `impetus-workflow-state-anchor` — new gap-check placements need anchors

### Verification, E2E, AVFL (D11, D13)
- `verify-skill` — running-app verification mandatory, tool-varying
- `plugin-dev-e2e-validation-workflow` — cmux smoke test for Momentum
- `e2e-validator-black-box-hardening` — zero escape hatches
- `e2e-validator-turn-budget` — budget for E2E validator runs
- `e2e-client-side-coverage` — Layer 2 UI interaction validation
- `avfl-cross-story-integration-lens` — cross-story integration aligns with feature-floor verification
- `avfl-fixer-required-gate` — fixer agent mandatory alongside validators
- `avfl-default-agent-composition` — preconfigured AVFL teams by profile
- `avfl-checkpoint-preview-integration` — Phase 4c human review
- `two-phase-coverage-validation` — AVFL enumerator-then-adversary mechanics
- `validator-targeted-recheck-pattern` — AVFL re-run specific scenarios
- `verify-orchestrator-dedup-guard-coverage` — AVFL/E2E orchestration boundary
- `proactive-scope-recommendations` — interacts with feature-grain commits and North Star
- `retro-extract-preflight-validation` — retro per-feature state hygiene

### Retro (D4, D5, D7, D8, D10, D12)
- `retro-triage-handoff` — feature-state hygienist + failure-as-diagnostic framing
- `retro-upstream-classifier` — failure categorization under D7
- `retro-pipeline-idempotency` — retro phases extended
- `retro-transcript-extraction-hardening` — underpins failure diagnosis and feature-state decisions
- `retro-session-analytics-phase-0` — ordinal reporting + failure diagnostic
- `retro-team-singleton-guard` — retro team scope expansion
- `retro-prior-action-item-cross-ref` — feeds failure specificity and feature hygiene

### Distill (D12)
- `distill-worktree-isolation` — fires on hooks; AVFL-clean merge; preserved developer-approval gate
- `distill-path-classification-redesign` — plugin vs personal rule detection under continuous triggers

### Grooming (D2, D14)
- `encode-epic-semantic-model` — DDD sub-domain semantics (also in Feature layer)
- `propagate-decision-skill-vocabulary` — feature and epic grooming vocabulary (also in Feature layer)
- `develop-epic-command` — epic orchestrator premise changes (also in Feature layer)

### Findings ledger and cross-cutting practice (D4, D7, D10)
- `findings-ledger-accumulates-quality-findings-across-stories` — anchors gap-check at three placements
- `cross-story-pattern-detection-surfaces-systemic-issues` — feeds failure-as-diagnostic and gap-check
- `flywheel-workflow-explains-issues-and-guides-upstream-trace` — adopt D7 naming
- `practice-health-metric-and-fix-level-tracking` — ordinal practice health ties to D4
- `findings-ledger-duckdb` — DuckDB integration for findings ledger

### Dev agent and story lifecycle (D1, D3, D9, D11)
- `dev-previous-story-continuity` — stories inherit Judgment Frame and North Star
- `dev-agent-hook-self-check` — pre-completion running-app verification mandatory
- `dev-agent-executor-not-decider` — feature grain changes what the orchestrator decides
- `dev-skills-guidelines` — encode North Star orientation and feature-grain awareness
- `build-guidelines-skill` — agents oriented toward feature value-floor

Untouched stories (infrastructure/spawn mechanics, provenance tooling, module-upgrade, observability, protocol plumbing, unrelated KB and workflow housekeeping) are omitted from this audit.
