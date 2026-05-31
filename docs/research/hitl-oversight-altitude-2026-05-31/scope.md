---
topic: "The HITL sweet spot — decision altitude and review granularity in agentic AI workflows"
goals: "Determine where a human should make decisions vs. delegate to the LLM, and how exhaustively LLM output (plans, code, specs, designs) must be reviewed — using the 'supervising a trusted junior' mental model. Decide whether an LLM can be prompted to communicate at a summarized, decision-grade altitude rather than excruciating detail."
profile: heavy
date: 2026-05-31
method: dynamic-workflow (parallel web discovery + adversarial verification) + Gemini triangulation via Claude-in-Chrome
recency_mandate: "Prioritize sources published 2025-2026. Every claim must trace to a fetched source, not training data."
sub_questions:
  - "SQ1 — Autonomy & delegation levels: What frameworks define the level at which a human should make decisions vs. delegate details to the agent? (autonomy taxonomies, HITL/HOTL/HOOTL, task vs. goal delegation, decision altitude)"
  - "SQ2 — Risk-calibrated oversight: How do you decide review depth by stakes — reversibility, blast radius, security, cost of error? When is exhaustive review warranted vs. a spot-check?"
  - "SQ3 — Reviewing AI-generated artifacts (code/specs): Do you review every line, or sample / review at the behavior level? What are the 2025-2026 practices and empirical findings for reviewing AI-generated code at scale?"
  - "SQ4 — Plan/spec review altitude: When an agent returns a plan, must the human review every line, or can the agent present a summarized, decision-grade plan? Progressive disclosure, dual-track (summary + detail) outputs."
  - "SQ5 — Making LLMs communicate at the right altitude: Concrete techniques and 2026 model features to make a model speak in summaries/principles vs. exhaustive detail (verbosity control, altitude/response shaping, system-prompt patterns)."
  - "SQ6 — Trust calibration & failure modes: Empirical risks of under-reviewing (automation bias, rubber-stamping, complacency) vs. over-reviewing (verification/spec fatigue, throughput loss). Where does the human add the most value? (METR, DORA 2025, HCI literature)"
  - "SQ7 — The 'junior employee' analogy: Does treating the LLM like a junior dev/PO/designer hold up? Delegation-maturity frameworks (situational leadership, levels of delegation). What transfers and where the analogy breaks (no cross-session learning, confident errors, jagged capability)."
  - "SQ8 — Operationalizing HITL gates: How do leading 2026 agentic engineering workflows structure checkpoints — plan approval, milestone review, escalation/ask-vs-act thresholds, gate placement?"
---

# Research Scope: The HITL Sweet Spot — Decision Altitude & Review Granularity

**Date:** 2026-05-31
**Profile:** heavy (8 parallel discovery agents + per-thread adversarial verification + Gemini triangulation)
**Goals:** See frontmatter `goals`.

## Framing

The developer works with LLMs the way a senior works with a trusted junior: scan most output for high-level issues rather than auditing every line, and converse in principles and summaries rather than excruciating detail. The research must establish, from the *latest* evidence, whether that posture is defensible — and where it is not — across planning and post-hoc review of plans, code, specs, and designs.

## Method

1. **Parallel discovery** — one agent per sub-question, recency-mandated (2025-2026), every claim traced to a fetched source.
2. **Adversarial verification** — an independent skeptic re-checks the load-bearing claims of each thread and hunts for contradicting recent evidence.
3. **Gemini triangulation** — Gemini (Deep Research where available) via Claude-in-Chrome, using the developer's existing sign-in, to surface sources the Claude web tools miss.
4. **Synthesis** — a single agent reads all raw + validation + Gemini artifacts and writes a decision-grade report with a provenance chain.
