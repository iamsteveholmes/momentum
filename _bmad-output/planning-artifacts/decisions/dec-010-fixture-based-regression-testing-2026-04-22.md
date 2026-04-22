---
id: DEC-010
title: Fixture-Based Regression Testing as Practice Primitive — Schema, Lifecycle, Skills, and Pruning
date: '2026-04-22'
status: decided
source_research:
  - path: _bmad-output/research/forgecode-agentic-tools-eval-2026-04-21/analysis/retro-microeval-loop-analysis-2026-04-21.md
    type: prior-research
    date: '2026-04-21'
stories_affected:
  - micro-eval-fixture-yaml-schema-schemamd
  - micro-eval-workflow-fidelity-meta-fixture
  - plan-audit-promote-eval-scenarios-to-yaml-fixtures
  - intake-fixture-provenance-capture
  - triage-fixture-routing-accuracy
  - distill-fixture-correct-layer-targeting
  - research-fixture-recency-enforcement
  - research-fixture-source-grounded-synthesis
  - create-story-fixture-change-type-classification
  - decision-fixture-sdr-cites-source-research
  - feature-breakdown-fixture-enumeration-recall
  - sprint-planning-fixture-gherkin-behavioral-generality
  - sprint-planning-fixture-team-composition-matches-story-type-mix
  - sprint-dev-fixture-autonomous-commit-per-story
  - sprint-dev-fixture-parallel-spawning-for-independent-stories
  - dev-skills-fixture-skill-md-frontmatter-conformance
  - quick-fix-fixture-epic-slug-ad-hoc-used-silently
  - avfl-fixture-enumeration-completeness-recall
  - avfl-fixture-declining-skepticism-convergence
  - e2e-validator-fixture-spec-sync-stale-reference-detection
  - architecture-guard-fixture-false-positive-rate
  - retro-fixture-transcript-extract-null-token-handling
  - retro-fixture-documenter-no-replication-without-verification
  - upstream-fix-fixture-root-cause-not-symptom
  - impetus-fixture-startup-latency-budget
  - impetus-fixture-auto-query-transcripts-on-context-gap
  - sprint-manager-fixture-exclusive-write-authority
  - refine-fixture-stale-story-detection
---

# DEC-010: Fixture-Based Regression Testing as Practice Primitive — Schema, Lifecycle, Skills, and Pruning

## Summary

Evaluated the ForgeCode-derived retro → fixture → micro-eval analysis (2026-04-21) which proposes adopting behavioral micro-evals as a Momentum practice primitive alongside AVFL and distill. All five framings adopted, one with adaptation: probabilistic assertions become the default but not the only allowed semantic. The pattern fills a strategic gap — micro-evals serve as a dual-purpose lens, assessing both model fitness and skill quality, surfacing whether phase skills need updating or replacing rather than only which underlying model performs best. Adoption unlocks the 28 fixture-related stories generated in the same triage session as their dependent infrastructure (schema, runner, retro extension).

---

## Decisions

### D1: Adopt fixture-based regression testing as a Momentum practice primitive — ADOPTED

**Research recommended:** Yes, starting with the minimum viable implementation (fixture YAML schema + `momentum:micro-eval` runner + retro Phase 4b-4f extension). The pattern fills a real gap (operational learning as durable regression coverage) and composes cleanly with existing primitives. ForgeCode's documented 25% → 78.4% Terminal-Bench improvement using behavioral micro-evals grown from failure-class analysis demonstrates the quality lever. Momentum's existing `evals/*.md` scenario convention indicates the team has already internalized evaluation-as-artifact; executable fixtures are the natural next step.

**Decision:** Adopted as recommended.

**Rationale:**
Fills a big need. It's not just which model works better but how our phase skills are working — the fixture suite tells us whether skills need updating or replacing, not only which model performs best. That dual-purpose framing (model fitness AND skill quality) is what makes this load-bearing for Momentum specifically.

---

### D2: Probabilistic assertions as the default fixture semantic — ADAPTED

**Research recommended:** Yes — fixtures should carry expected failure rates and range-based assertions (e.g., `failure_rate_in_range(0.2, 0.6)` with ±20% tolerance), not binary pass/fail. Binary assertions on LLM outputs are either flaky (false alarms) or overly permissive (missed regressions). Probabilistic assertions with recorded baselines reflect actual behavior and are prerequisite for the unexpected-pass investigation workflow (D3).

**Decision:** Adopted with adaptation. Probabilistic assertions are the default and the crucial semantic for behavior-against-baseline cases, but they are not the only allowed assertion type. Deterministic assertions remain valid where appropriate — for example, schema/structural conformance checks, exact CLI output comparison, file existence assertions, or other near-deterministic decisions where one sample suffices.

**Rationale:**
Probabilistic vs baseline is the crucial pattern for behavioral fixtures, but some fixture targets warrant deterministic checks. Forcing every fixture into a probabilistic mold would add noise to assertions that should be sharp.

---

### D3: Unexpected pass is a Suspect state, not a silent success — ADOPTED

**Research recommended:** Yes. When a fixture that should fail passes on replay, flag it as Suspect requiring investigation. Five possible causes: (1) fix shipped, (2) model upgrade resolved it, (3) model nondeterminism, (4) context reconstruction incomplete, (5) original retro finding was a false positive. Only causes 1 & 2 produce valid Protected transitions; causes 3–5 produce invalid coverage. Without investigation the fixture library accumulates noise and becomes unreliable.

**Decision:** Adopted as recommended.

**Rationale:**
Unexpected passes definitely require further investigation. Silent acceptance would erode library integrity over time and turn the fixture suite into a false-confidence machine.

---

### D4: Ship `momentum:micro-eval` and `momentum:fixture-investigate` as new skills — ADOPTED

**Research recommended:** Two skills, in this order:
- `momentum:micro-eval` — the runner. Discovers fixtures across `skills/**/evals/fixtures/*.yml`, executes each, reports probabilistic pass/fail. Ships first; usable immediately with manually-authored fixtures.
- `momentum:fixture-investigate` — investigation workflow for Suspect fixtures. Ships after `micro-eval` has been in use for a few sprints and the Suspect state has become observable.

The retro extension (Phases 4b-4f for fixture generation) is an addition to the existing `momentum:retro` skill, not a separate skill.

**Decision:** Adopted as recommended.

**Rationale:**
Need skills for the micro-evals — runner ships first as foundational infrastructure, fixture-investigate ships once the Suspect state is observable in real operation rather than designed in vacuum.

---

### D5: Fixture library pruning policy (Stale → Retired) — ADOPTED

**Research recommended:** Stale state with defined thresholds. A fixture with N=20 consecutive clean runs across M=3 models is demoted to Stale (runs weekly, not per-commit). A Stale fixture with an additional N=10 consecutive clean runs is Retired (moved out of regular suite, kept as historical record). Thresholds (20/3/10) are tunable parameters. Without pruning the library grows indefinitely and becomes expensive to run.

**Decision:** Adopted as recommended.

**Rationale:**
Fixtures having a built-in recycle mechanism (Stale → Retired) prevents library bloat and keeps per-commit cost bounded as the suite grows.

---

## Phased Implementation Plan

| Phase | Focus | Timing | Key Stories |
|-------|-------|--------|-------------|
| 1 — Foundation | Schema + runner + first promotion | First sprint after adoption | `micro-eval-fixture-yaml-schema-schemamd`, `micro-eval-workflow-fidelity-meta-fixture`, `plan-audit-promote-eval-scenarios-to-yaml-fixtures` |
| 2 — Retro extension | Add Phase 4b-4f to `momentum:retro` so fixtures generate from real findings | After Phase 1 schema lands | (retro extension is a modification to existing skill — covered by an existing or new retro story) |
| 3 — Seed library | Build the 25 phase-specific fixtures stubbed in the same triage session | Rolling, by phase cluster (capture / spec / planning / execution / validation / reflection / orchestration) | The 25 remaining stubs in `stories_affected` |
| 4 — Investigation skill | Ship `momentum:fixture-investigate` once Suspect state is observable | After 3+ retros have run with fixture generation | New story to be created when Phase 3 surfaces Suspect cases |

---

## Decision Gates

| Gate | Timing | Question | Criteria |
|------|--------|----------|----------|
| Gate 1 — schema viability | Phase 1 done | Does the YAML fixture schema cover real failure cases without gymnastics? | First 5 fixtures author cleanly without schema extension; if schema needs >2 extensions, pause and revise SCHEMA.md |
| Gate 2 — retro generation works | After 3 retros under the extended workflow | Does Phase 4b-4f produce useful fixtures from real findings? | ≥50% of severity ≥medium findings produce executable Active fixtures; reconstruction failures <30% |
| Gate 3 — Suspect state observability | Phase 3 underway | Is `momentum:fixture-investigate` worth building now? | At least 2 distinct Suspect-state cases observed in the running suite |
| Gate 4 — pruning thresholds | After 1 quarter of operation | Are 20/3/10 thresholds correct? | Tune based on observed false-Stale and false-Retired rates |

---

## Open Items Deferred

Per developer direction at decision-capture time:

- **Architecture decision impact** — not flagged in `architecture.md` until the Phase 1 stories are actually created and any AD-N additions are clearly warranted. To be revisited at sprint planning when the foundation stories enter ready-for-dev.
- **Named error-class taxonomy** — defer formalization until the first 3-5 retros under the extended workflow surface concrete classes; track in `docs/practice/error-class-taxonomy.md` as a living document.
- **Fixture location convention** — tentatively `skills/<skill>/evals/fixtures/*.yml` (alongside existing `evals/eval-*.md` scenarios). Revisit if the skill tree gets too heavy.
- **CLI `--depends-on` flag for `momentum-tools sprint story-add`** — discovered during the triage session that the CLI does not propagate `proposed_depends_on` to `stories/index.json` (depends_on captured in stub frontmatter only). Flagged for follow-up; affects this decision's downstream stories that have dependencies (B1 → research-recency, D2 → enforce-parallel, F1/F2 → fix-retro stories, G2 → orientation-auto-query).

---

## Source Material

- [Retro → Micro-Eval Feedback Loop analysis](../../research/forgecode-agentic-tools-eval-2026-04-21/analysis/retro-microeval-loop-analysis-2026-04-21.md) — primary source containing Decisions A–E
- [ForgeCode consolidated research](../../research/forgecode-agentic-tools-eval-2026-04-21/final/forgecode-agentic-tools-eval-final-2026-04-21.md) — methodology context
- [ForgeCode — Benchmarks Don't Matter (Part 1)](https://forgecode.dev/blog/benchmarks-dont-matter/) — original methodology source
