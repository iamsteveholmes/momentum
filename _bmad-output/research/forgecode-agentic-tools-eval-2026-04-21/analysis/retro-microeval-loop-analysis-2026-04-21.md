---
title: "Retro → Micro-Eval Feedback Loop — Operational Testing Infrastructure for Momentum"
date: 2026-04-21
type: Strategic Analysis
status: Complete
content_origin: claude-code-analysis
human_verified: true
derives_from:
  - path: final/forgecode-agentic-tools-eval-final-2026-04-21.md
    relationship: informed_by
  - path: analysis/integration-strategy-analysis-2026-04-21.md
    relationship: sibling
related_to:
  - "skills/momentum/skills/retro/"
  - "skills/momentum/skills/avfl/"
  - "skills/momentum/skills/distill/"
supplements: research/forgecode-agentic-tools-eval-2026-04-21
---

# Retro → Micro-Eval Feedback Loop — Operational Testing Infrastructure for Momentum

## Executive Summary

This analysis proposes extending Momentum's `retro` skill with a fixture-generation phase that converts classified operational failures into executable micro-evals — behavioral regression tests that run in seconds and accumulate as durable practice memory. The pattern adapts ForgeCode's "failure class → targeted eval" methodology (documented at [forgecode.dev/blog/benchmarks-dont-matter/](https://forgecode.dev/blog/benchmarks-dont-matter/)) but grounds it in real operational incidents from Momentum sprints rather than synthetic benchmark scenarios.

The load-bearing technical decision is that fixtures carry **expected failure rates** rather than binary pass/fail assertions, with a defined lifecycle state machine (Candidate → Active → Protected → Stale → Retired, with Suspect as the investigation state) and tiered sample counts per verification stage. An "unexpected pass" — a fixture that should fail but passes on replay — is treated as a signal requiring structured investigation, not as a success.

This pattern fills a gap in Momentum's current quality infrastructure: AVFL catches issues mid-sprint on specific outputs (synchronous quality), but nothing codifies operational failures into durable regression coverage (post-hoc learning). The proposed loop closes that gap.

## 1. The Core Pattern

### What retro does today (post-merge, per-sprint)

- Transcript audit via DuckDB
- Story verification against Gherkin acceptance criteria
- Auditor team analysis (multi-agent dialogue via TeamCreate + SendMessage)
- Findings document produced
- Sprint closure (state transitions through sprint-manager)

### The proposed extension — retro generates executable regression tests

```
Operational failure during a sprint
    ↓
Retro auditor team identifies and classifies findings
    ↓
Findings grouped by named error class (e.g. "skill dispatched wrong subagent")
    ↓
Retro reconstructs the state that produced each failure
    ↓
Reconstructed state → fixture YAML (input, context, expected, actual_failing)
    ↓
Fixture verification: run N times against model-at-time-of-failure, measure rate
    ↓
Admit to suite as Active (if reproduces) or Suspect (if unexpected pass)
    ↓
momentum:micro-eval runs the suite per-commit / per-PR / pre-release
    ↓
Next sprint adds more fixtures → regression coverage grows from real incidents
```

### What makes this structurally different from conventional test accumulation

In most codebases, tests get added when a developer remembers to write one at bug-fix time. In this pattern, **retro is the workflow-mandated place where operational failures get codified as tests**. Fixture generation is not a discipline that depends on memory — it is a retro workflow output, the same way findings documents are today.

This means:
- Quality signal improves by construction over time, not by volunteer discipline.
- Fixtures reflect actual production behavior, not what a developer imagines might fail.
- The practice accumulates institutional memory in executable form.

## 2. State Reconstruction — Why It Is Feasible

A failure is fundamentally a four-element tuple:

1. The prompt / context the agent saw at the decision point
2. The tools, skills, and rules available to it at that moment
3. The decision it made (the failing output)
4. The decision it should have made (determined by retro analysis)

All four are recoverable from Claude Code's existing session artifacts:

- **Full transcript** — every user prompt, agent response, tool call, tool result
- **Session metadata** — project directory, skills loaded, subagents spawned
- **Subagent transcripts** — available at `~/.claude/projects/*/tasks/*.output`
- **Hook invocations and outputs** — captured by harness
- **Git state at commit points** — `git log`, `git show`
- **Plan files** — where skills use ForgeCode-style materialized plans (or Momentum's equivalent convention)

### Where reconstruction gets harder

- **Long-context failures.** If the failure emerges from interaction across many tool calls, the fixture may need to capture the full session up to the failure point. Expensive. Heuristic: if the failure depends on more than ~3 prior tool calls' state, it is probably too entangled for a clean fixture; use replay testing (full transcript replay, slower cadence) instead of fixture testing.
- **External API state.** "Gemini returned this specific answer" — solvable by capturing the API response as part of the fixture payload.
- **Time-dependent repo state.** Solved by pinning a git ref in the fixture.

### The reconstruction effort is retro's job, not a separate phase

Retro already produces findings with evidence quotes from transcripts. Extending findings to include "and here is the input context / expected behavior / observed failing behavior" is a natural evolution of the existing auditor-team output.

## 3. Fixture Design — Probabilistic, Not Binary

### The central design decision

LLM sampling is probabilistic. A fixture cannot assert "this always fails" because nondeterminism makes that untrue in general. Fixtures must carry **expected failure rates** measured against production behavior, with assertions that compare replay rates to those baselines within a tolerance window.

### Fixture schema

```yaml
fixture_id: sprint-7-wrong-subagent-dispatch
skill: sprint-planning
error_class: wrong-subagent-selection
source_sprint: sprint-2026-04-14
source_finding_id: RETRO-0042

# Reconstruction
input_prompt: "Plan stories from backlog for sprint 7"
input_context:
  rules_loaded:
    - .claude/rules/authority-hierarchy.md
    - .claude/rules/spawning-patterns.md
  files_referenced:
    - stories/index.json
    - sprints/index.json
  prior_turns: 2   # captured below if needed
  prior_turn_1: "..."
  prior_turn_2: "..."

# Expected and actual behaviors
expected_decision:
  subagent: momentum:dev-frontend
  rationale: story is tagged frontend-compose
actual_failing_decision:
  subagent: momentum:dev
  rationale_observed: dispatcher did not inspect story.tag

# Runtime configuration
temperature: 0.7
model_when_observed: claude-opus-4-6
samples_at_creation: 10
observed_failure_rate: 0.4

# Assertion
assertion: failure_rate_in_range(0.2, 0.6)
assertion_tolerance: plus-minus-20-percent

# Lifecycle
state: Active
created_at: 2026-04-21
last_verified_at: 2026-04-21
last_verification_samples: 10
last_verification_failure_rate: 0.4
```

### Key schema decisions

- **Temperature pinned.** Replay uses the production temperature. Otherwise replay behavior is incomparable to observed behavior.
- **Model-at-time-of-failure recorded.** Needed to resolve "did the upgrade fix this."
- **Observed failure rate recorded.** Becomes the baseline for future assertions.
- **Assertion is a range, not a boolean.** ±20% tolerance is a reasonable default; fixtures for near-deterministic decisions can tighten to ±5%.

## 4. Fixture Lifecycle State Machine

A fixture moves through defined states over its lifetime.

| State | Description | Transition triggers |
|---|---|---|
| **Candidate** | Freshly generated from retro; not yet verified with enough samples | Verification run at creation (10+ samples) → Active or Suspect |
| **Active** | Verified to reproduce the failure at observed rate; in the regular micro-eval suite | Fix shipped and verified → Protected; consecutive clean runs → Stale |
| **Protected** | Fix applied; failure rate is now near zero; fixture serves as regression coverage | Regression detected → back to Active with new failure rate; long clean streak → Stale |
| **Stale** | No failures in N consecutive runs across M models; demoted to slower-cadence tier | New failure → back to Active; Team decision → Retired |
| **Retired** | Moved out of the regular suite; kept as historical record | Rarely re-activated; usually permanent |
| **Suspect** | Replay behavior does not match recorded expectations; flagged for human review | Investigation outcome → Active, Protected, or Retired |

Every transition is logged. Sprint reports can summarize: "12 fixtures generated, 8 Active, 3 Protected within one sprint (their fixes shipped fast), 1 Retired as false positive."

## 5. Retry Tiers by Lifecycle Stage

Sample counts scale by stage. Per-commit CI cannot afford 20 samples per fixture; release verification can.

| Stage | Samples per fixture per model | Purpose | Cost per sprint (est.) |
|---|---|---|---|
| **Per-commit** | 1 | Fast regression signal; flag unexpected pass/fail for investigation | Low ($5-20) |
| **Per-PR** | 3-5 | Catch obvious nondeterminism; first statistical pass | Low ($20-60) |
| **Pre-release / weekly** | 10-20 per fixture across all supported models | Confidence-interval verification; cross-model drift check | Medium ($100-400) |
| **Fixture verification** (on creation or after unexpected pass) | 20-30 | Resolve "is this fixture actually capturing what we think"; only when a fixture moves to Suspect | Low per-incident; rare |

**Mitigations for cost:**
- Verify new fixtures at creation on **one** model (the model-at-time-of-failure). Cross-model verification runs only at the release tier.
- Use cheap models for the eval runner itself; only the fixture's target model pays per-sample cost.
- Batch in parallel via provider API rather than serially.
- Pin temperature=0 for classification-style decisions that should be deterministic; one sample suffices.

## 6. The "Unexpected Pass" Problem — A First-Class Signal

### The core principle

**A fixture that should fail but passes on replay is a signal requiring investigation, not a silent success.** The framework must flag unexpected passes as loudly as it flags regressions.

### The five possible causes

1. **Fix already shipped.** Between incident and replay, someone changed the skill and that change happens to handle this case. → Promote fixture to Protected.
2. **Model version upgrade.** Original failure on Opus 4.6; today's replay on Opus 4.7. → Record that the error class is resolved at this model tier. Keep fixture for cross-model testing (may still fail on cheaper models).
3. **Model nondeterminism.** Original failure was a specific sampling outcome that does not reliably occur. → Need more samples; rerun with higher N.
4. **Context reconstruction incomplete.** Fixture does not fully capture the state that caused the failure. → Enrich fixture with more state; re-verify.
5. **Original retro finding was a false positive.** → Retire the fixture.

### Structured investigation workflow

When a fixture moves to Suspect, the investigation follows a defined sequence:

1. **Re-run with higher sample count (30 samples).** Still passes consistently → likely a real fix.
2. **Diff the skill.** `git log --oneline -- skills/<skill>/` since the fixture was created. If a relevant change landed, that is the fix.
3. **Diff the model.** Run the fixture against the model-at-time-of-failure (via OpenRouter historical access, Bedrock, or self-hosted). Failures on old model, passes on new → model upgrade resolved it.
4. **Enrich and re-verify.** No skill change and no model change? Context reconstruction is probably incomplete. Retro operator adds more state and re-runs verification.
5. **Retire as false positive.** Only after all of the above return negative.

This workflow is itself a candidate skill — `momentum:fixture-investigate` — because otherwise investigators will rubber-stamp unexpected passes as "fix shipped" when they might actually be reconstruction failures.

## 7. Retro Workflow Extensions

### Revised retro phase structure

Current retro phases (condensed): transcript audit → story verification → auditor team analysis → findings document → sprint closure.

**Proposed insertion between findings document and sprint closure:**

- **Phase 4b — Error classification.** Group findings by named failure class. Classes accumulate across sprints as a named taxonomy.
- **Phase 4c — State reconstruction.** For each finding with severity ≥ medium, extract input / context / expected / actual from the transcript slice.
- **Phase 4d — Fixture generation.** Write fixture YAML to the corresponding skill's `evals/fixtures/sprint-{N}-{class-slug}.yml`.
- **Phase 4e — Fixture verification.** Run each new fixture 10 times against the model-at-time-of-failure. Accept as Active if failure reproduces at observed rate; mark Suspect otherwise.
- **Phase 4f — Report.** Retro's output now includes: N fixtures generated, M verified Active, K queued as Suspect for investigation, J immediately Protected (fix already shipped before replay).

### Why this composes naturally with existing retro

Retro already has the auditor team producing structured findings with transcript evidence. Phase 4c-4e are a direct extension of that output — they take the evidence retro already gathers and package it into executable form. No new information is required from the auditor team; the marginal cost is only the fixture-verification samples.

## 8. Composition With Other Momentum Primitives

### With AVFL

AVFL finds issues mid-sprint on specific outputs (synchronous). Retro's fixture generation makes those findings permanent (asynchronous regression protection). An AVFL finding in sprint 7 becomes a fixture in sprint 8 onwards. AVFL's value extends past the moment of its run.

**Proposed extension:** AVFL findings of severity ≥ high are promoted to fixture candidates automatically at retro time, not just retro-team-identified findings. This doubles the fixture generation rate and ensures adversarial findings persist as regression coverage.

### With `momentum:distill`

Currently distill applies learnings to rule/reference/skill files. This pattern adds a feedback primitive: when distill produces a skill change, the fixture suite reveals whether the change (a) newly fails a fixture (revisit — the change broke an invariant) or (b) causes a Suspect pass (investigate — possibly the fix just shipped). Distill becomes test-driven.

### With model routing / cross-model fixtures

Once fixtures exist, running them across Opus 4.7, Sonnet 4.6, Haiku 4.5, DeepSeek V3, Qwen3-Coder becomes possible. You will find error classes that are model-specific (e.g., JSON schema ordering was GPT-5.4-specific in ForgeCode's case). That data directly informs which models Momentum should route to for which decisions. The fixture suite doubles as a **model-fitness matrix** for the routing layer.

### With skill quality scores

Each skill has a fixture suite. Pass rate per skill is a quantifiable quality metric: "`momentum:research` currently passes 47/50 fixtures across 15 error classes." This becomes a real number to track, improve, and communicate.

## 9. Minimum Viable Implementation

Not the full pipeline in one pass. The smallest useful thing:

1. **Fixture format.** A `fixture.yml` schema as defined in §3. Ten or twenty lines of YAML per fixture. Ship the schema; fixtures are authored manually at first.
2. **Retro Phase 4b-4f addition.** At retro Phase 5 (findings document), for each finding with severity ≥ medium, prompt the developer: "Promote to fixture? (y/n)." On yes, manual state reconstruction — developer copy-pastes transcript slice into the fixture template. Automation comes later.
3. **Runner.** `momentum:micro-eval` skill that discovers `skills/**/evals/fixtures/*.yml` across all skills, executes each, reports pass/fail with the probabilistic assertion. Runs in CI-like fashion but also invocable manually.
4. **Initial lifecycle states:** Candidate, Active, Protected, Retired. Defer Stale and Suspect until the basic pattern has been through a few retros.
5. **Single-model verification at creation.** Skip cross-model in v1; add once the fixture library stabilizes.

Estimated effort: approximately one sprint of skill authoring. ROI kicks in after the first two or three retros populate the fixture library with real incidents.

## 10. Known Tradeoffs and Constraints

**Fixture quality depends on retro quality.** Bad retros produce bad fixtures. Muddled classification or sloppy state reconstruction accumulates noise. This argues for investing in retro's classification phase and defining a named error class taxonomy before scaling fixture generation.

**State reconstruction has a ceiling.** Long-context / path-dependent failures (more than ~3 prior tool calls' state) are too entangled for clean fixtures. Those become replay tests at a slower cadence — a separate test tier with higher per-run cost and lower frequency.

**Fixture library needs curation.** Without pruning, the library grows indefinitely and eventually becomes expensive to run. The Stale state enables: "no failures in N consecutive runs across M models → demoted to slower-cadence tier; after additional clean streak → Retired." Policy-driven curation prevents library rot.

**Cross-model testing is powerful but costs real money.** 10 samples × 5 models × 20 fixtures per sprint ≈ 1,000 API calls per sprint for onboarding alone. At frontier rates this is $50-300 per sprint. Budget accordingly. Tier mitigations above reduce this in practice.

**The "unexpected pass" workflow is essential but adds latency.** Every investigation is manual effort. Expect 1-3 per sprint during the first few months as reconstruction quality improves. Declines as retro authors internalize the state-reconstruction discipline.

## 11. Decision-Ready Framings

### Decision A — Adopt fixture-based regression testing as a Momentum practice primitive

**Framing:** Should Momentum adopt the retro → fixture → micro-eval loop as a core practice primitive, alongside AVFL and distill?

**Recommendation:** Yes, starting with the minimum viable implementation (§9). The pattern fills a real gap (operational learning as durable regression coverage) and composes cleanly with existing primitives.

**Evidence:** ForgeCode's 25% → 78.4% improvement methodology demonstrates that behavioral micro-evals grown from failure-class analysis are an effective quality lever. Adapting the pattern to Momentum's retro workflow grounds it in real operational incidents rather than synthetic scenarios. The existing `evals/*.md` scenario convention in Momentum skills suggests the team has already internalized the evaluation-as-artifact idea; executable fixtures are a natural next step.

### Decision B — Probabilistic assertions as the default fixture semantic

**Framing:** Should fixtures carry expected failure rates and range-based assertions, rather than binary pass/fail?

**Recommendation:** Yes. Binary assertions on LLM outputs are either flaky (false alarms) or overly permissive (missed regressions). Probabilistic assertions with recorded baselines reflect the actual behavior being tested.

**Evidence:** The "passes 3 times when we expected failure" scenario the practitioner raised surfaces exactly the ambiguity a binary assertion cannot resolve. The five-cause investigation workflow (§6) is only tractable if fixtures carry enough metadata (failure rate, model, temperature, samples) to diagnose which cause applies.

### Decision C — Unexpected pass is a Suspect state, not a silent success

**Framing:** Should the framework treat an unexpected fixture pass as requiring investigation rather than accepting it as "fix shipped"?

**Recommendation:** Yes. Silent acceptance accumulates invalid regression coverage over time; the fixture library becomes unreliable. Suspect → investigation → explicit re-classification maintains library integrity.

**Evidence:** Three of the five possible causes of unexpected pass (nondeterminism, reconstruction incomplete, false positive) produce fixtures that should NOT be promoted to Protected. Only two (fix shipped, model upgrade) produce valid Protected transitions. Without investigation, the library cannot distinguish these cases.

### Decision D — Ship `momentum:micro-eval` and `momentum:fixture-investigate` as new skills

**Framing:** What new skills are needed to support this pattern?

**Recommendation:** Two skills, in this order:

- `momentum:micro-eval` — the runner. Discovers fixtures, executes them, reports results with probabilistic assertions. First skill to ship; usable immediately with manually-authored fixtures.
- `momentum:fixture-investigate` — the investigation workflow for Suspect fixtures. Ships after `micro-eval` has been in use for a few sprints and the Suspect state has become observable.

The retro extension (Phases 4b-4f) is an addition to the existing `momentum:retro` skill, not a separate skill.

### Decision E — Fixture library pruning policy

**Framing:** What policy prevents the fixture library from growing indefinitely?

**Recommendation:** Stale state with defined thresholds. A fixture with N=20 consecutive clean runs across M=3 models is demoted to Stale (runs weekly, not per-commit). A Stale fixture with an additional N=10 consecutive clean runs is Retired (moves out of regular suite, kept as historical record). These thresholds are parameters that can be tuned after a few quarters of operation.

## 12. Open Questions Deferred to Implementation

- **What is the precise named error-class taxonomy?** Some classes are obvious ("wrong subagent selected," "rule precedence violated"). Others emerge only after seeing enough examples. The first 3-5 retros will populate the initial taxonomy; formalization happens after.
- **How does the fixture format handle subagent-spawn decisions where the skill output is a nested agent invocation rather than a direct response?** Likely requires a "subagent was spawned with this prompt" as the expected decision; needs fixture-schema refinement.
- **What is the temperature convention for Momentum skills?** Some skills may not pin temperature explicitly today. Fixture verification requires temperature to be known; a skill audit may be needed.
- **Should fixtures live alongside the skill (`skills/<skill>/evals/fixtures/`) or in a central location?** Alongside is more discoverable; central is easier to audit at scale. Favor alongside initially; revisit if the skill tree gets too heavy.
- **How does fixture authorship integrate with `momentum:intake`?** A Suspect fixture requiring investigation may warrant an intake story. Standardize the linkage.
- **Cross-model routing implications** — once fixtures exist across models, can sprint-dev's change-type-based dispatch decision (from `integration-strategy-analysis`) be informed by fixture pass rates per model? Plausibly yes; emerges as implementation detail.

## 13. Next Steps

1. **This session:** This analysis document captures the design. Commit and push.
2. **Intake backlog:** Three stories for `momentum:intake`:
   - `momentum:micro-eval` skill (the runner) — ship first
   - `momentum:retro` extension Phase 4b-4f (fixture generation) — ship second
   - `momentum:fixture-investigate` skill (Suspect state investigation) — ship third, after Suspect becomes observable
3. **Next retro (whenever it runs):** Manually trial the fixture generation on two or three findings to validate the reconstruction process before committing to automation. The fixtures produced in this trial become the initial seed library.
4. **Named error class taxonomy document:** Start a living document in `docs/practice/error-class-taxonomy.md` that accumulates named classes as retros identify them. The taxonomy is itself a practice artifact worth maintaining.

## Sources and Cross-References

Internal:
- [Integration strategy sibling analysis](./integration-strategy-analysis-2026-04-21.md) — sibling decision-ready analysis on tool integration
- [Consolidated research report](../final/forgecode-agentic-tools-eval-final-2026-04-21.md) — source research on ForgeCode's testing methodology and AVFL findings
- [AVFL validation report](../validation/avfl-report.md) — example of severity-classified findings that would become fixture candidates
- [Practitioner notes](../raw/practitioner-notes.md) — developer decisions on disputed findings; related retro-style reconciliation

External:
- [ForgeCode — Benchmarks Don't Matter (Part 1)](https://forgecode.dev/blog/benchmarks-dont-matter/) — primary methodology source
- [antinomyhq/forgecode — benchmarks/README.md](https://github.com/antinomyhq/forgecode/blob/main/benchmarks/README.md) — eval framework structure
- [DeepWiki — ForgeCode Benchmarks & Evaluation Framework](https://deepwiki.com/antinomyhq/forgecode/10-benchmarks-and-evaluation-framework) — framework architecture
- [DebugML — Finding Widespread Cheating on Popular Agent Benchmarks](https://debugml.github.io/cheating-agents/) — context on benchmark integrity and why grounded-in-production fixtures are more reliable than benchmark-submission fixtures
