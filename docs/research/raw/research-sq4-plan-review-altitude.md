---
content_origin: web-discovery
sub_question: "sq4-plan-review-altitude"
date: 2026-05-31
---

# SQ4 — Plan/Spec Review Altitude: Decision-Grade Summaries

## Synthesis

When an AI agent returns a PLAN (or spec) before execution, the dominant 2025–2026 guidance is unambiguous: **the human should NOT review every line by default.** Instead, the consensus pattern is *progressive disclosure* — present a decision-grade summary at the top (an "executive view" / "bird's-eye view" / "evidence pack"), keep the fine-grained detail available but offloaded, and reserve detailed human attention for the points that genuinely require judgment (high-risk, irreversible, ambiguous, or intent-misalignment-prone decisions). This is the same architectural principle Anthropic codified for Agent Skills (name/description → full instructions → appendix), Will Larson described for large-file agents, and Addy Osmani applied to plan-mode workflows ("a bird's-eye view that can stay in the prompt, while the fine details remain offloaded unless needed").

The strongest operationalization comes from approval-workflow design. StackAI's "evidence pack" frames the goal precisely: surface exactly what a reviewer needs to make a fast decision — "the difference between a 15-second approval and a 15-minute investigation" — with evidence "concise by default with expandable detail options." This is a literal dual-track output: a decision-grade summary plus expandable appendix. The reviewer's job is reframed as *verification, not redoing the work*.

A second, deeper theme is **what altitude to review at, not just how much.** A March 2026 arXiv paper (Zietsman) argues the human (and AI reviewers) should review code *against the specification/intent*, not against the code itself, because reviewing code-against-code is structurally circular. This elevates the plan/spec to the unit of review — the same inversion Amazon's Kiro IDE makes ("the spec is the unit of work; code is what happens after you sign off on the spec"). Reviewing at plan altitude is more decision-grade than reviewing diffs, because the plan encodes intent.

Third, **risk-based gating** governs where full detail is warranted. The recurring rule: require full review/approval at risk boundaries (irreversible, costly, regulated, high blast radius — drafting is cheap, sending at scale is not), and sample or batch low-risk items. This is how teams avoid both reviewer fatigue and rubber-stamping.

The main tension: progressive-disclosure / summarized review trades thoroughness for throughput, and several sources warn that the human becomes the bottleneck and that subtle hallucinations (code that compiles but is wrong) and "agent abandonment" (huge unscoped PRs with no plan) are exactly what summaries can mask. The plan-altitude camp answers this by making intent the reference point so summaries can be checked against something external.

## Key Findings

### 1. Progressive disclosure is the canonical pattern: summary first, detail on demand (Anthropic, primary)
- **Claim:** Agent information should be delivered in graduated levels — metadata/summary first, full instructions when relevant, appendix detail only as needed — like "a table of contents, then specific chapters, and finally a detailed appendix."
- **Evidence:** "Like a well-organized manual that starts with a table of contents, then specific chapters, and finally a detailed appendix, skills let Claude load information only as needed." Three levels: name+description (preloaded) → full SKILL.md (when relevant) → "additional linked files are the third level (and beyond) of detail, which Claude can choose to navigate and discover only as needed."
- **Source:** "Equipping agents for the real world with Agent Skills" — Anthropic Engineering
- **URL:** https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- **Date:** 2025-10-16 | **Type:** vendor-docs | **Confidence:** high

### 2. Hierarchical "bird's-eye view" in the plan keeps reviewers at the right altitude (Addy Osmani, O'Reilly)
- **Claim:** Plan-mode workflows should produce a hierarchical summary giving a high-level overview while fine details stay offloaded unless needed; humans review high-level alignment first, deep detail on demand. Plan Mode acts as a read-only approval gate before code is written.
- **Evidence:** "By creating a hierarchical summary in the planning phase, you get a bird's-eye view that can stay in the prompt, while the fine details remain offloaded unless needed." And: "Tools like Claude Code offer a Plan Mode that restricts the agent to read-only operations—it can analyze your codebase and create detailed plans but won't write any code until you're ready." Phased gates: Specify → Plan → Tasks → Implement, where "you don't move to the next one until the current task is fully validated."
- **Source:** "How to Write a Good Spec for AI Agents" — Addy Osmani, O'Reilly Radar
- **URL:** https://www.oreilly.com/radar/how-to-write-a-good-spec-for-ai-agents/
- **Date:** 2026-02-20 | **Type:** blog (named expert / O'Reilly) | **Confidence:** high

### 3. The "evidence pack": decision-grade summary = fast approval; concise-by-default, expandable detail (StackAI)
- **Claim:** Approval interfaces should present a decision-grade "evidence pack" so reviewers can verify quickly rather than re-do the work — concise by default with expandable detail, highlighting policy triggers and confidence scores.
- **Evidence:** "The evidence pack is the difference between a 15-second approval and a 15-minute investigation." "The reviewer's job is not to re-do the agent's work; it's to verify it quickly." Interfaces should "keep evidence concise by default with expandable detail options" and "batch low-risk items for single-screen review." A strong pack includes draft/action details, context, policy flags, "decision rationale and confidence scores," cited sources/preconditions, and rollback plans.
- **Source:** "Human-in-the-Loop AI Agents: How to Design Approval Workflows…" — StackAI
- **URL:** https://www.stackai.com/insights/human-in-the-loop-ai-agents-how-to-design-approval-workflows-for-safe-and-scalable-automation
- **Date:** 2026-05-29 | **Type:** industry-report (vendor blog) | **Confidence:** high

### 4. Risk-based gates decide where full detail is warranted; confirm only at risk boundaries (icmd)
- **Claim:** High-retention "operator" products show plan previews ("Approve these steps before we run them") and post-hoc receipts, but confirm only at risk boundaries — cheap actions need no gate, irreversible/scaled ones do.
- **Evidence:** "Plan previews for meaningful changes ('Approve these steps before we run them')." "The trick is to confirm only at risk boundaries: drafting is cheap; sending at scale is not; changing access rights is never 'just a click.'" Receipts: "what happened, which records changed, links to the artifacts." Sensitive actions "need dual control: a second approver or an admin-level sign-off."
- **Source:** "The Agentic Product Stack in 2026: How Teams Are Shipping AI 'Operators'…" — icmd
- **URL:** https://icmd.app/article/the-agentic-product-stack-in-2026-how-teams-are-shipping-ai-operators-without-br-1779153812284
- **Date:** 2026-05-19 (updated 2026-05-27) | **Type:** industry-report | **Confidence:** medium

### 5. Review at plan/spec altitude, not code altitude — reviewing code-against-code is circular (arXiv, Zietsman)
- **Claim:** Code should be reviewed against its specification/intent, not against the code itself; reviewing code against code/patterns is structurally circular and propagates systematic errors. The specification provides an external correctness reference, and the right abstraction level depends on the problem domain (Cynefin).
- **Evidence:** "Deploying AI reviewers without executable specifications creates a structurally circular problem where both the generating agent and reviewing agent reason from the same artifact… resulting in the review checking code against itself rather than against intent." Executable specs "perform a domain transition in the Cynefin sense, converting enabling constraints into governing constraints and moving the problem from the complex domain to the complicated domain."
- **Source:** "The Specification as Quality Gate: Three Hypotheses on AI-Assisted Code Review" — Christo Zietsman, arXiv:2603.25773
- **URL:** https://arxiv.org/pdf/2603.25773
- **Date:** 2026-03-30 | **Type:** peer-reviewed (preprint) | **Confidence:** medium

### 6. Make the spec/plan the unit of sign-off (Kiro spec-driven review)
- **Claim:** Spec-driven IDEs invert the flow: generate a formal requirements doc (EARS notation + testable acceptance criteria + design artifacts), require explicit human review/edit/reject before any code, making the spec the reviewed contract.
- **Evidence:** "The spec is the unit of work. Code is what happens after you sign off on the spec." The user can "review the spec. You can edit it. You can reject it and rewrite it." The doc "becomes the explicit contract between what you want and what the agent will build," preventing "vibe coding."
- **Source:** "Amazon Kiro Review — The Agentic IDE That Writes the Spec Before the Code" — ChatForest
- **URL:** https://chatforest.com/reviews/amazon-kiro-aws-agentic-ide-spec-driven-review/
- **Date:** 2026-05-23 | **Type:** news/review | **Confidence:** medium

### 7. Progressive disclosure = present summary/overview first, detail only when requested (Will Larson)
- **Claim:** Progressive disclosure means limiting context to the minimum necessary and adding detail over time; implemented via metadata-first presentation and on-demand expansion (peek/load/extract), it mirrors executive summary + optional deep dive.
- **Evidence:** Progressive disclosure is "limiting what is added to the context window to the minimum necessary amount, and adding more detail over time as necessary." Implemented with metadata-first listing, selective preloading (initial kilobytes), and on-demand tools (`peek_file()`, `load_file()`, `extract_file()`).
- **Source:** "Building an internal agent: Progressive disclosure and handling large files" — Will Larson (Irrational Exuberance)
- **URL:** https://lethain.com/agents-large-files/
- **Date:** 2025-12-26 | **Type:** blog (named expert) | **Confidence:** high

### 8. Decompose review and surface high-impact items first; judgment is the bottleneck (GitHub Blog)
- **Claim:** Efficient review of agent output is risk-ordered and phased (highest-impact checks first within a fixed budget), validating intent capture before code; mechanical checks automate, human effort reserves for architecture/edge cases/operational context.
- **Evidence:** A "10-minute progressive review framework": classify complexity (1–2m) → scan CI changes (2–3m, "highest priority") → check duplicate utilities (3–5m) → trace critical logic (5–8m) → verify security boundaries (8–10m). Red flags include "agent abandonment — large, unscoped PRs with no implementation plan" and "subtle hallucinations" that compile but are wrong. "Judgment is the bottleneck, and that's fine."
- **Source:** "Agent pull requests are everywhere. Here's how to review them." — Andrea Griffiths, GitHub Blog
- **URL:** https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/
- **Date:** 2026-05-07 | **Type:** vendor-docs (GitHub engineering blog) | **Confidence:** high

### 9. Separate "details" (what's reviewed) from "actions" (decision options); gate before consequential steps (Towards Data Science)
- **Claim:** HITL interrupt design should structurally separate the reviewed content from the decision options, offer approve / reject / edit (not binary), and place the gate before the consequential/irreversible action rather than after non-deterministic steps.
- **Evidence:** "The `details` key passed into `interrupt()` contains the generated content, while the `action` key triggers a handler function." Three pathways: approve, reject, inline-edit. Interrupts belong "as a gate before an action" — e.g., before publishing — not after searches.
- **Source:** "Building Human-In-The-Loop Agentic Workflows" — Kenneth Leung, Towards Data Science
- **URL:** https://towardsdatascience.com/building-human-in-the-loop-agentic-workflows/
- **Date:** 2026-03-25 | **Type:** blog | **Confidence:** medium

### 10. "Altitude" = keep instructions/plans at the right abstraction; relevance-gated disclosure beats comprehensive dumps (HumanLayer)
- **Claim:** Plans/instructions degrade when not at the right altitude — irrelevant detail causes the agent (and reviewer) to lose the signal; the fix is relevance-gated disclosure, telling the agent how to find detail rather than front-loading it.
- **Evidence:** "The more information you have in the file that's not universally applicable… the more likely it is that Claude will ignore your instructions." Tell Claude "how to find important information so that it can find and use it, but only when it needs to." Frontier LLMs follow "~150–200 instructions with reasonable consistency."
- **Source:** "Writing a good CLAUDE.md" — Kyle (@0xblacklight), HumanLayer Blog
- **URL:** https://www.humanlayer.dev/blog/writing-a-good-claude-md
- **Date:** 2025-11-25 | **Type:** blog (named practitioner) | **Confidence:** medium

## Named Frameworks

- **Progressive disclosure (three-level model)** — Anthropic Agent Skills: name/description → full SKILL.md → linked appendix files (table-of-contents → chapters → appendix analogy). Directly maps to executive-summary-plus-detail plan presentation.
- **Evidence pack** — StackAI: a decision-grade bundle (action details, context, policy flags, confidence scores, sources, rollback) that is "concise by default with expandable detail."
- **Specify → Plan → Tasks → Implement (phased gates)** — Addy Osmani / spec-driven development: human validation gate between each phase.
- **Hierarchical summary / "bird's-eye view"** — Addy Osmani: summary stays in-context, fine detail offloaded.
- **Specification as Quality Gate (3 hypotheses)** — Zietsman, arXiv: review against intent not code; circularity of code-against-code review; Cynefin domain transition via executable specs.
- **Spec-as-unit-of-work** — Amazon Kiro: EARS-notation requirements + acceptance criteria as the signed-off contract before code.
- **10-minute progressive review framework** — GitHub / Andrea Griffiths: risk-ordered, time-boxed review surfacing highest-impact checks first.
- **Risk-boundary confirmation / dual control** — icmd & StackAI: 100% approval for high-risk/irreversible; sample or batch low-risk.
- **details vs actions separation** — LangGraph-style `interrupt()` pattern (Kenneth Leung): reviewed content separated from decision options; approve/reject/edit.
- **EARS (Easy Approach to Requirements Syntax)** — structured requirement format used by Kiro for testable acceptance criteria.

## Debates & Tensions

- **Summarized review vs thoroughness / bottleneck risk.** Progressive-disclosure advocates (Anthropic, Larson, Osmani, StackAI) optimize for fast decision-grade approval. GitHub's Griffiths counters that "judgment is the bottleneck" and warns summaries can hide "subtle hallucinations" (compiles, but wrong) and "agent abandonment" (huge unscoped PRs) — i.e., the very things a tidy summary obscures. Tension: throughput vs. catching what a summary glosses over.
- **What altitude is the *right* unit of review — plan/spec vs code/diff.** Zietsman and Kiro argue the spec/intent is the correct review altitude (code-against-code is circular). GitHub's diff-review framework still treats the PR diff as the reviewed artifact (while validating intent capture). They are partly reconcilable — review the plan first, then spot-check the diff against it — but they disagree on where the primary sign-off lives.
- **How much to confirm at all.** Some sources push "Approve the plan" previews for "meaningful changes" (icmd); others push sampling/exception-only for low-risk and only 100% review at risk boundaries (StackAI, icmd). The shared worry is reviewer fatigue / rubber-stamping when too much is gated, vs. blind spots when too little is.
- **Confidence/provenance surfacing.** StackAI explicitly recommends surfacing confidence scores and cited sources in the summary; icmd frames it as verification/receipts rather than numeric confidence. No consensus on whether decision-grade summaries should carry explicit confidence numbers.

## Sources

1. Anthropic Engineering — "Equipping agents for the real world with Agent Skills" — https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills — 2025-10-16 — vendor-docs
2. Addy Osmani, O'Reilly Radar — "How to Write a Good Spec for AI Agents" — https://www.oreilly.com/radar/how-to-write-a-good-spec-for-ai-agents/ — 2026-02-20 — blog (named expert)
3. StackAI — "Human-in-the-Loop AI Agents: How to Design Approval Workflows for Safe and Scalable Automation" — https://www.stackai.com/insights/human-in-the-loop-ai-agents-how-to-design-approval-workflows-for-safe-and-scalable-automation — 2026-05-29 — industry-report
4. icmd — "The Agentic Product Stack in 2026: How Teams Are Shipping AI 'Operators' Without Breaking Trust, Cost, or Control" — https://icmd.app/article/the-agentic-product-stack-in-2026-how-teams-are-shipping-ai-operators-without-br-1779153812284 — 2026-05-19 (upd. 2026-05-27) — industry-report
5. Christo Zietsman, arXiv — "The Specification as Quality Gate: Three Hypotheses on AI-Assisted Code Review" (arXiv:2603.25773) — https://arxiv.org/pdf/2603.25773 — 2026-03-30 — peer-reviewed (preprint)
6. ChatForest — "Amazon Kiro Review — The Agentic IDE That Writes the Spec Before the Code" — https://chatforest.com/reviews/amazon-kiro-aws-agentic-ide-spec-driven-review/ — 2026-05-23 — news/review
7. Will Larson (Irrational Exuberance) — "Building an internal agent: Progressive disclosure and handling large files" — https://lethain.com/agents-large-files/ — 2025-12-26 — blog (named expert)
8. Andrea Griffiths, GitHub Blog — "Agent pull requests are everywhere. Here's how to review them." — https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/ — 2026-05-07 — vendor-docs
9. Kenneth Leung, Towards Data Science — "Building Human-In-The-Loop Agentic Workflows" — https://towardsdatascience.com/building-human-in-the-loop-agentic-workflows/ — 2026-03-25 — blog
10. Kyle (@0xblacklight), HumanLayer Blog — "Writing a good CLAUDE.md" — https://www.humanlayer.dev/blog/writing-a-good-claude-md — 2025-11-25 — blog (named practitioner)
