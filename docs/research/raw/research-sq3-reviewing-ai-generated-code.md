---
content_origin: web-discovery
sub_question: "sq3-reviewing-ai-generated-code"
date: 2026-05-31
---

# Reviewing AI-Generated Artifacts: Every Line vs. Sampling

## Synthesis

The 2025–2026 evidence shows the question has shifted from *"review every line vs. sample?"* to *"where in the pipeline does verification happen, and what is the trust mechanism?"* The strong consensus across vendor docs (GitHub), named practitioners (Simon Willison), and industry telemetry (DORA, Faros AI) is that **the human committing the code remains fully accountable for it** — Willison's framing is "a computer can never be held accountable; that's your job as the human in the loop." But almost no one argues that a human should re-read every AI-generated line by eye. Instead, the emerging multi-layer model pushes mechanical/structural errors *left* into the IDE and CI (static analysis, type-checking, dependency verification, tests) so that scarce human judgment is reserved for **requirement fidelity, business logic, architecture, and consequence** — the things automation cannot check.

The empirical signal on *review burden* is the most consistent and alarming finding. Faros AI's longitudinal telemetry on 10,000+ developers found that moving from low to high AI adoption produced **154% larger pull requests, 91% longer code-review times, and 9% more bugs per developer** — i.e., throughput moved upstream into the review bottleneck rather than relieving it. METR's RCT found experienced developers were **19% slower** with AI despite believing they were faster, and a separate analysis found that even when 73.8% of automated review comments were acted upon, PR closure time still *rose 42%*. The 2025 DORA report frames AI as an "amplifier": positive for throughput but negatively correlated with delivery stability, with ~30% of developers reporting little or no trust in AI-generated code and an explicit "trust but verify" recommendation.

On **test-as-trust**, the strongest 2026 framing is acceptance-criteria-driven TDD: humans define testable "done" criteria *before* the AI generates code, and tests validate the specification, not the implementation. Practitioners flag a specific failure mode — "tautological testing," where AI-generated tests share the same blind spots as the AI-generated code they validate — and therefore recommend higher coverage bars for AI code (85–90% vs. 70–80% for human code) plus mandatory human checkpoints for business/regulatory logic. Meta's Just-in-Time Tests (JiTTests) generate diff-aware tests claimed to produce ~4x more useful catches than generic hardening tests.

On **diff-level vs behavior-level review**, the academic MSR/EASE 2026 corpus reveals the real-world pattern: a large fraction of agent-authored PRs receive *no recorded human review at all* (61% in one EASE 2026 study; 38% of rejected PRs in another were simply "abandoned/not reviewed"). When humans do intervene in agent PRs, they intervene *less often* than on human PRs (52% vs 84%) but each intervention costs *more* effort (larger churn, longer duration). Reviewer attention is also biased: one 2026 study found AI PRs with ~2x the redundancy drew *fewer* negative reactions, suggesting surface plausibility suppresses scrutiny. AI code-review tooling itself is empirically noisy — 60.2% of agent-only-reviewed PRs fell into the lowest (0–30%) signal band, and CRA-only PRs merged at 45% vs 68% for human-reviewed PRs.

Bottom line: practitioners do **not** review every line; they review at the behavior/acceptance level *backed by* automated structural gates, while remaining personally accountable. But the empirical record (2025–2026) warns that this is not yet working at scale — review is the new bottleneck, AI review bots add noise, and "silent merges" of unreviewed AI code are common.

## Key Findings

### Review burden / throughput / defect escape

1. **AI adoption inflates PR size and review time and modestly raises bugs.** Faros AI telemetry (10,000+ developers, 1,255 teams, up to 2 years): moving from low→high AI adoption produced "154% increase" in PR size, "91% longer" review duration, and "9% more bugs per developer," alongside 98% more merged PRs. Throughput moves into the review bottleneck.
   - Source: "What METR's Study Missed About AI Productivity in the Wild" / Faros AI telemetry study — https://www.faros.ai/blog/lab-vs-reality-ai-productivity-study-findings — 2025-07-28 — industry-report — confidence: high

2. **Experienced developers were 19% slower with AI in an RCT, despite perceiving a ~20% speedup.** METR study of 16 experienced OSS developers on 246 real tasks; developers spent ~9% of total task time reviewing/modifying AI output. The perception–reality gap (~39 points) is the headline.
   - Source: METR via Augment Code guide (citing arxiv.org/abs/2507.09089) — https://www.augmentcode.com/guides/why-ai-coding-tools-make-experienced-developers-19-slower-and-how-to-fix-it — 2025-10-03 (updated 2026-01-23) — industry-report — confidence: high

3. **Automated review comments don't reduce burden even when acted upon.** "Even with 73.8% of automated review comments acted on, pull request closure time still increased 42%" (2024 study cited in 2026). Review-rate was a statistically significant factor in defect-removal effectiveness — rushed reviews miss more bugs.
   - Source: "Stop Sending IDE-Catchable AI Code Errors to Review" (Colette Des Georges) — https://blog.jetbrains.com/ai/2026/05/stop-sending-ide-catchable-ai-code-errors-to-review/ — 2026-05 — vendor-docs/blog — confidence: medium

4. **DORA 2025: AI is an amplifier — up on throughput, down on stability; ~30% distrust AI code.** "30% report little or no trust in the code generated by AI"; researchers recommend "trust but verify." AI adoption has a negative relationship with delivery stability absent strong testing/version-control/fast feedback.
   - Source: DORA — State of AI-assisted Software Development 2025 — https://dora.dev/dora-report-2025/ — 2025-07 — industry-report — confidence: high

5. **Quantified DORA-era review degradation.** Secondary analysis citing DORA/telemetry: "Median time in PR review is up 441%, compared to 91% in our 2025 dataset, and 31% more PRs are merging with no review at all"; PR size +51.3%; "Incidents per PR are up 242.7%."
   - Source: Faros AI — "Key Takeaways from the DORA Report 2025" — https://www.faros.ai/blog/key-takeaways-from-the-dora-report-2025 — 2025-09-25 — industry-report — confidence: medium

### Diff-level vs behavior-level review (academic / empirical)

6. **A majority of agent PRs receive no recorded human review.** EASE 2026 study of 33,596 agent-authored PRs (AIDev dataset, repos ≥100 stars): "61.38% of AI-generated PRs received no recorded review activity." Agent-authored comments dominated review threads at 71.58%; agent-steering commands were 16× more frequent than in human PRs.
   - Source: "These Aren't the Reviews You're Looking For: How Humans Review AI-Generated Pull Requests" (Duma et al., EASE 2026) — https://arxiv.org/html/2605.02273v1 — 2026-05-04 — peer-reviewed — confidence: high

7. **Reviewer abandonment is the #1 failure mode for agent PRs.** MSR 2026 study (33,596 agent PRs, 5 agents; 600 manually annotated): "Abandoned/Not Reviewed" = 228 (38%) of rejections; Duplicate PR 23%; CI/Test Failure 17%; Incorrect Implementation only 3%. Each failed CI check reduces merge odds ~15%. Overall merge rate 71.48%.
   - Source: "Where Do AI Coding Agents Fail? An Empirical Study of Failed Agentic Pull Requests in GitHub" (Ehsani et al., MSR 2026) — https://arxiv.org/html/2601.15195 — 2026-04 — peer-reviewed — confidence: high

8. **Humans intervene less on agent PRs but each intervention costs more.** MSR 2026: "human interventions occur less frequently in APRs than in HPRs (52.17% vs. 83.59%)" but "when it occurs in APRs, it requires higher review effort, including larger code churn and longer durations." Intervention taxonomy: Guidance 58%, Decision 21%, Direct code changes 17%, Operational 4%. Work is "shifting … from implementation to supervision, guidance and quality control."
   - Source: "Behind Agentic Pull Requests: An Empirical Study on Developer Interventions" (Khelifi, Ouni, Khemaja, MSR 2026) — https://2026.msrconf.org/details/msr-2026-mining-challenge/26/Behind-Agentic-Pull-Requests-An-Empirical-Study-on-Developer-Interventions-in-AI-Age — 2026-04-13 — peer-reviewed — confidence: high

9. **AI code-review bots are empirically noisy and correlate with worse merge outcomes.** MSR 2026 study of 13 CRAs (3,109 PRs, 19,450 comments): "60.2% of closed CRA-only PRs fell into the 0–30% signal range"; 12 of 13 CRAs had signal ratios below 60%. CRA-only PRs merged at 45.20% vs human-only 68.37% (χ²=83.03, p<0.001).
   - Source: "From Industry Claims to Empirical Reality: An Empirical Study of Code Review Agents in Pull Requests" (Chowdhury et al., MSR 2026) — https://arxiv.org/html/2604.03196v1 — 2026-04-03 — peer-reviewed — confidence: high

10. **Surface plausibility suppresses reviewer scrutiny of AI code.** A 2026 study found AI-generated PRs containing "nearly twice the code redundancy drew fewer negative reactions from reviewers than human-written ones," indicating reviewer bias toward plausible-looking AI output.
    - Source: search synthesis citing MSR 2026 mining-challenge work — https://2026.msrconf.org/details/msr-2026-mining-challenge/19/Where-Do-AI-Coding-Agents-Fail-An-Empirical-Study-of-Failed-Agentic-Pull-Requests-in — 2026 — peer-reviewed — confidence: low

### Test-as-trust / acceptance-criteria review

11. **Acceptance-criteria-driven TDD is the recommended trust mechanism: humans define "done" before the AI codes.** "Tests should validate the specification, not the implementation's self understanding." Recommended coverage: 85–90% for AI code vs 70–80% for human code, because AI "passes the happy path but fails on edge cases." Mandatory human checkpoint for business/regulatory logic.
    - Source: "How to Test AI Generated Code: A QA Checklist for 2026" (ContextQA) — https://contextqa.com/blog/what-is-ai-generated-code-testing-checklist/ — 2026-04-08 — blog — confidence: medium

12. **"Tautological testing" is the key risk of test-as-trust.** When the same AI generates both code and tests, "both outputs share the same blind spots" — coverage metrics give false confidence without quality assertions. Diff-aware generation (Meta JiTTests) claimed to yield ~4x more useful catches than generic hardening tests.
    - Source: ContextQA checklist (above) + search synthesis of The New Stack "AI Is Testing AI-Generated Code" — https://thenewstack.io/ai-is-testing-ai-generated-code-should-you-trust-it/ — 2026 — blog — confidence: medium

13. **Named-practitioner stance (Simon Willison): you must prove it works; review burden you skip is dumped on reviewers.** "A computer can never be held accountable. That's your job as the human in the loop." Submitting untested AI code "shifts the actual work to reviewers, [a] dereliction of duty." Reviewing/testing/understanding all AI-written lines is "using an LLM as a typing assistant," not vibe coding.
    - Source: "Simon Willison on delivering AI generated code" (Stefan Judis notes) — https://www.stefanjudis.com/notes/simon-willison-on-delivering-ai-generated-code/ — 2025-12-18 — blog/expert — confidence: high

### Vendor guidance / shift-left

14. **GitHub's official guidance is multi-layered, not line-by-line.** Eight areas: functional checks (compiles, tests pass), context/intent, code quality, dependencies, AI-specific pitfalls (hallucinated APIs, *deleted tests*, logic errors), collaborative review, automation (CodeQL, Dependabot, linting), workflow improvement. Explicit caution: don't accept tests that are "deleted or skipped, instead of fixed."
    - Source: GitHub Docs — "Review AI-generated code" — https://docs.github.com/en/copilot/tutorials/review-ai-generated-code — 2025/2026 (living doc) — vendor-docs — confidence: high

15. **Shift mechanical detection left; reserve human judgment for what automation can't catch.** "20–25% of AI hallucinations are detectable through automated structural and static analysis" before review; "roughly 44% of AI errors escape automated detection entirely, requiring human judgment." "Your reviewers' judgment is a finite resource." AI users merge 60% more PRs/week (DX Q4 2025).
    - Source: JetBrains AI Blog — "Stop Sending IDE-Catchable AI Code Errors to Review" — https://blog.jetbrains.com/ai/2026/05/stop-sending-ide-catchable-ai-code-errors-to-review/ — 2026-05 — vendor-docs/blog — confidence: medium

16. **Practitioner six-layer review process targeting AI failure modes.** Layer 1 requirement fidelity (keep the ticket/acceptance criteria open — "non-negotiable"), Layer 2 logic/edge cases (manually trace null/zero/boundary), Layer 3 API integrity (cross-reference calls against actual library versions), Layer 4 security. Emphasis: "run it" — AI code "looks right but breaks on edge inputs."
    - Source: "How to Review AI-Generated Code: The Complete Developer's Guide" (Shift Asia) — https://shiftasia.com/column/how-to-review-ai-generated-code-the-complete-developers-guide/ — 2026 — blog — confidence: low

## Named Frameworks

- **DORA "AI as amplifier" model** — AI magnifies existing org strengths/weaknesses; positive on throughput, negative on stability (DORA 2025).
- **Acceptance-Criteria-Driven TDD (AC-TDD)** — human-defined testable "done" precedes AI generation; tests validate spec, not implementation (ContextQA / ubos).
- **JiTTests (Just-in-Time Tests / Meta Engineering)** — diff-aware test generation, ~4x more useful catches than generic hardening tests.
- **Six-Layer AI Code Review** — requirement fidelity → logic/edge cases → API integrity → security (Shift Asia); plus GitHub's 8-area multi-layer checklist.
- **Signal-to-noise (CRA) two-tier keyword framework** — 0–30% noisy / 31–59% / 60–79% / 80–100% high-quality bands for AI review-bot comments (Chowdhury et al., MSR 2026).
- **Agent-PR rejection taxonomy** — 4-level hierarchical (Reviewer / Pull Request / Code / Agentic) failure taxonomy (Ehsani et al., MSR 2026).
- **Developer-intervention taxonomy** — Guidance / Decision / Direct-code / Operational (Khelifi et al., MSR 2026).
- **Review-interaction taxonomy** — Agent-steering / Automation-CI / Human-review (Duma et al., EASE 2026).
- **"Tautological testing"** (anti-pattern) and **"On-the-loop" supervision** (engineers design validation systems, set acceptance criteria, interpret pipeline-level results).
- **"Lethal trifecta"** (Willison, June 2025) — adjacent security framing for autonomous agents.

## Debates & Tensions

- **Does test-as-trust replace line-by-line review?** AC-TDD advocates say validated specs + high coverage substitute for re-reading every line; the "tautological testing" critique says AI tests can inherit AI blind spots, so a human business-logic checkpoint is irreducible. GitHub and Willison both insist on human accountability regardless.
- **Do AI review tools reduce or increase reviewer burden?** Vendors imply reduction; the empirical record (MSR 2026 CRA study, 2024 42%-closure-time study) shows bots are noisy (60% low-signal) and burden often *rises*. Net: tools help triage but don't relieve the human bottleneck.
- **Lab vs. field on productivity.** METR RCT (19% slower) vs. Faros field telemetry (21% more tasks, 98% more PRs) vs. DORA (>80% perceive productivity gains). Faros explicitly argues METR's lab setting missed real-world dynamics; reconciliation is that *individual output* rises while *organizational quality/stability* and *review throughput* degrade.
- **Review every line vs. behavior-level.** Practitioner/vendor guidance converges on behavior+structural-gates over line-by-line, but the academic data shows the failure mode in practice is the *opposite extreme* — silent, unreviewed merges (38–61% no review), i.e. neither line-by-line nor disciplined behavior review.
- **Reviewer bias.** Surface plausibility of AI code reduces critical scrutiny (fewer negative reactions despite 2x redundancy), arguing *against* relaxing review for AI output.

## Sources

- https://www.faros.ai/blog/lab-vs-reality-ai-productivity-study-findings — Faros AI telemetry study — 2025-07-28 — industry-report
- https://www.augmentcode.com/guides/why-ai-coding-tools-make-experienced-developers-19-slower-and-how-to-fix-it — METR 19% slowdown (cites arXiv 2507.09089) — 2025-10-03 (upd. 2026-01-23) — industry-report
- https://blog.jetbrains.com/ai/2026/05/stop-sending-ide-catchable-ai-code-errors-to-review/ — JetBrains AI Blog (Des Georges) — 2026-05 — vendor blog
- https://dora.dev/dora-report-2025/ — DORA State of AI-assisted Software Development 2025 — 2025-07 — industry-report
- https://www.faros.ai/blog/key-takeaways-from-the-dora-report-2025 — Faros AI DORA 2025 takeaways — 2025-09-25 — industry-report
- https://arxiv.org/html/2605.02273v1 — "These Aren't the Reviews You're Looking For" (Duma et al., EASE 2026) — 2026-05-04 — peer-reviewed
- https://arxiv.org/html/2601.15195 — "Where Do AI Coding Agents Fail?" (Ehsani et al., MSR 2026) — 2026-04 — peer-reviewed
- https://2026.msrconf.org/details/msr-2026-mining-challenge/26/Behind-Agentic-Pull-Requests-An-Empirical-Study-on-Developer-Interventions-in-AI-Age — Khelifi et al., MSR 2026 — 2026-04-13 — peer-reviewed
- https://arxiv.org/html/2604.03196v1 — "From Industry Claims to Empirical Reality: Code Review Agents" (Chowdhury et al., MSR 2026) — 2026-04-03 — peer-reviewed
- https://arxiv.org/pdf/2603.26130 — SWE-PRBench (Kumar) — 2026-03-30 — peer-reviewed/preprint
- https://contextqa.com/blog/what-is-ai-generated-code-testing-checklist/ — ContextQA QA checklist 2026 — 2026-04-08 — blog
- https://thenewstack.io/ai-is-testing-ai-generated-code-should-you-trust-it/ — The New Stack (JiTTests, test-as-trust) — 2026 — blog
- https://www.stefanjudis.com/notes/simon-willison-on-delivering-ai-generated-code/ — Simon Willison on delivering AI code — 2025-12-18 — expert blog
- https://docs.github.com/en/copilot/tutorials/review-ai-generated-code — GitHub Docs: Review AI-generated code — 2025/2026 — vendor docs
- https://shiftasia.com/column/how-to-review-ai-generated-code-the-complete-developers-guide/ — Shift Asia six-layer review guide — 2026 — blog
