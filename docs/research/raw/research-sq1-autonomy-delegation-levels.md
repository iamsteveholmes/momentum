---
content_origin: web-discovery
sub_question: "sq1-autonomy-delegation-levels"
date: 2026-05-31
---

# Autonomy & Delegation Levels — Decision Altitude

## Synthesis

The question of "at what level should a human decide versus delegate details to an AI agent" has, in 2025–2026, converged on a small set of recurring ideas expressed through many named frameworks. The dominant intellectual move, borrowed explicitly from the SAE J3016 self-driving levels, is to treat autonomy as a **graduated, designable property** rather than a binary or an automatic byproduct of model capability. The most-cited academic anchor is Feng, McDonald & Zhang's "Levels of Autonomy for AI Agents" (arXiv 2506.12469, U. Washington / Knight First Amendment Institute, June–July 2025), which defines five levels by **the role the human plays**: Operator → Collaborator → Consultant → Approver → Observer. Crucially, they argue an agent's autonomy level "can be treated as a deliberate design decision, separate from its capability and operational environment," and propose third-party-issued **autonomy certificates** to govern it.

A parallel, near-identical five-rung ladder has been re-skinned for coding specifically: Swarmia's Assistive → Conversational → Task Agent → Autonomous Teammate → Agentic Avalanche (March 2026), and ASDLC.io's L1–L5 (Assistive → Task-Based → Conditional → High → Full, May 2026). Both map a corresponding **human decision altitude**: the human descends from Driver/Operator (deciding every change) to Reviewer, to async Change Owner, to Auditor, to passive Consumer/Observer. The shared thesis of the coding frameworks is that **higher autonomy is not better** — autonomy should be matched to task ambiguity and verifiability, with most teams' value ceiling sitting around Levels 2–3.

The HITL / HOTL / HOOTL vocabulary remains the governance lingua franca and is now explicitly **risk-tiered**: human-in-the-loop (pre-execution approval) for high-risk/irreversible actions, human-on-the-loop (autonomous action + monitored post-hoc intervention) for reversible medium-risk work, and human-out-of-the-loop for low-risk, high-volume actions. Strata's 2026 guide adds concrete "time-boxed decision lanes" (15 seconds for low-risk, 2 minutes for PII, 15 minutes for financial disbursements) and the enterprise governance literature (CSA, Microsoft, Berkeley CMR) frames the target state as **"managed/bounded autonomy"**: agents act freely inside technically enforced boundaries and escalate when they exit them. Anthropic's primary telemetry (Feb 2026) gives the empirical picture: experienced Claude Code users raise auto-approve from ~20% to >40% while *also* raising their interrupt rate (5%→9%) — i.e., they shift from per-action approval to monitoring (a real-world HITL→HOTL migration), evidence of "calibrated trust, not blind trust." The strongest tension in the corpus is between **task-delegation vs goal-delegation**: a persistent "delegation gap" (developers use AI for ~60% of work but fully delegate only 0–20%) is attributed not to capability but to **missing judgment, persistent context, testable outcomes, and explicit constraints** — meaning the binding constraint on decision altitude is specification quality, not model intelligence.

## Key Findings

### Finding 1 — The canonical academic taxonomy is five human-role levels, and autonomy is a deliberate design choice
- **Claim:** The leading academic framework defines five levels of agent autonomy by the role the *user* occupies — Operator, Collaborator, Consultant, Approver, Observer — and insists autonomy is a design decision separable from capability.
- **Evidence:** "an agent's level of autonomy can be treated as a deliberate design decision, separate from its capability and operational environment"; levels are "characterized by the roles a user can take when interacting with an agent."
- **Per-level decision altitude:** L1 Operator — "User makes all decisions; the agent only acts on direct command." L2 Collaborator — "User and agent share planning and execution, allowing fluid control handoffs." L3 Consultant — "Agent takes the lead, consulting the user only for expertise and preferences." L4 Approver — "Agent operates independently, asking for user approval in high-risk or pre-defined cases." L5 Observer — "Agent acts fully autonomously; user can only monitor or activate an emergency stop."
- **Source title:** Levels of Autonomy for AI Agents (Feng, McDonald, Zhang — U. Washington / Knight First Amendment Institute)
- **Source URL:** https://arxiv.org/abs/2506.12469 (also https://knightcolumbia.org/content/levels-of-autonomy-for-ai-agents-1 and https://www.aigl.blog/levels-of-autonomy-for-ai-agents/)
- **Publication date:** 2025-06-14 (submitted), revised 2025-07-28
- **Source type:** peer-reviewed / working paper
- **Confidence:** high

### Finding 2 — "Autonomy certificates": third-party governance of the maximum allowed autonomy level
- **Claim:** The same paper proposes autonomy certificates — third-party-issued digital documents capping the level at which an agent may operate, given its capabilities and operating environment.
- **Evidence:** A certificate is "a digital document that prescribes the maximum level of autonomy at which an agent can operate given 1) some set of technical specifications that define the agent's capabilities... and 2) its operational environment," issued "by a third-party governing body to agent developers" and stored "with the agent's metadata." Developers submit "an operational agent privately deployed for testing" plus "an autonomy case with proof of the agent's interactive behaviors," analogous to safety cases.
- **Source title:** Levels of Autonomy for AI Agents
- **Source URL:** https://knightcolumbia.org/content/levels-of-autonomy-for-ai-agents-1
- **Publication date:** 2025-07-28
- **Source type:** peer-reviewed / working paper
- **Confidence:** high

### Finding 3 — The HITL / HOTL / HOOTL choice is now explicitly risk-driven, with time-boxed "decision lanes"
- **Claim:** The 2026 governance consensus selects oversight model by risk and reversibility: HITL (pre-approval) for high-risk/irreversible, HOTL (autonomous + monitored intervention) for reversible medium-risk, HOOTL for low-risk/high-volume.
- **Evidence:** HITL "requires a human to approve or authorize an action before the AI system executes it" (high-risk: financial disbursements, legal agreements, sensitive data). HOTL "allows the AI to act autonomously while a human monitors outputs and can intervene" (medium-risk where mistakes are reversible). The framework applies time-boxed lanes: "15 seconds for low-risk actions, 2 minutes for PII access, 15 minutes for financial disbursements," and cites aviation Crew Resource Management as the oversight discipline.
- **Source title:** Human-in-the-Loop: A 2026 Guide to AI Oversight (Eric Olden, Strata Identity)
- **Source URL:** https://www.strata.io/blog/agentic-identity/practicing-the-human-in-the-loop/
- **Publication date:** 2026-05-11
- **Source type:** vendor blog
- **Confidence:** high

### Finding 4 — Enterprise governance reframes the goal as "managed/bounded autonomy" with a six-level (L0–L5) escalation taxonomy
- **Claim:** The Cloud Security Alliance defines a six-level autonomy taxonomy (L0 No Autonomy → L5 Full Autonomy) where controls and approval seniority scale with level, and Level 5 is deemed inappropriate for enterprises today.
- **Evidence:** L2 Supervised — "Humans review and approve a plan or batch of actions, and the AI then executes autonomously within that approved scope." L3 Conditional — "The AI makes decisions and takes actions autonomously within defined boundaries, escalating to humans only when it encounters situations that exceed those boundaries." "Autonomy boundaries must be technically enforced, not just policy-documented." Approval seniority scales (business owner→management→review boards→executive sign-off); systems "automatically drop to Level 1 if anomalies are detected." Author: "I don't believe Level 5 is appropriate for enterprise deployment today."
- **Source title:** Autonomy Levels for Agentic AI (Jim Reavis, CSA)
- **Source URL:** https://cloudsecurityalliance.org/blog/2026/01/28/levels-of-autonomy
- **Publication date:** 2026-01-28
- **Source type:** industry-report / standards body
- **Confidence:** high

### Finding 5 — Coding-specific five-level ladders agree higher autonomy is NOT always better; match level to task ambiguity
- **Claim:** Swarmia's five levels for coding agents (Assistive, Conversational, Task Agent, Autonomous Teammate, Agentic Avalanche) explicitly argue the right level depends on task ambiguity/verifiability, and most teams' ceiling is Levels 2–3.
- **Evidence:** "making an industry expert work as an intern is wasted potential; putting a middle-schooler in the CEO chair is a disaster." Level 2 Conversational: "the agent moves fast, but you always decide where it goes." Level 3 Task Agent decision rule: "can you create a pull request from your phone without opening your laptop? If yes, it's Level 3." On Level 5: even with free-running subagents "someone should still be watching at the orchestrator level."
- **Source title:** Five levels of AI coding agent autonomy, and why higher isn't always better (Miikka Holkeri, Swarmia)
- **Source URL:** https://www.swarmia.com/blog/five-levels-ai-agent-autonomy/
- **Publication date:** 2026-03-19
- **Source type:** vendor blog / practitioner
- **Confidence:** high

### Finding 6 — A parallel L1–L5 coding scale explicitly maps each level to a human "decision altitude" role
- **Claim:** ASDLC.io's L1–L5 scale (Assistive, Task-Based, Conditional, High, Full) pairs each autonomy level with the human's oversight role, showing the human's decision altitude rising as autonomy rises.
- **Evidence:** L1 Assistive → human is "Driver (hands-on 100%)"; L2 Task-Based → "Reviewer (sync-checks and manual diff approval)"; L3 Conditional → "Change Owner (async validation of CI/CD and intent drift)" with a "human Context Gate review"; L4 High → "Auditor (post-hoc telemetry analysis)" / "self-directed backlog execution"; L5 Full → "Consumer (passive beneficiary)" / "without human loops."
- **Source title:** Levels of Autonomy: L1-L5 AI Agent Autonomy Scale (ASDLC.io)
- **Source URL:** https://asdlc.io/concepts/levels-of-autonomy/
- **Publication date:** 2026-05-28 (last updated)
- **Source type:** industry framework / knowledge base
- **Confidence:** medium

### Finding 7 — Anthropic's telemetry shows real humans migrating HITL→HOTL as trust calibrates (not blind trust)
- **Claim:** Anthropic's measured Claude Code data shows experienced users increase auto-approval but *also* increase interruptions, indicating a shift from per-action approval to monitoring-based oversight — empirical movement up the autonomy ladder.
- **Evidence:** New users (<50 sessions) use full auto-approval ~20% of the time, rising to >40% among experienced users (~750 sessions). Interrupt rate rises from 5% (new) to 9% (experienced); experienced users "tend to stop reviewing each action and instead let Claude run autonomously, intervening only when needed." 99.9th-percentile turn duration "nearly doubled, from under 25 minutes to over 45 minutes" (Oct 2025→Jan 2026). ~80% of actions have safeguards; 73% have human-in-the-loop elements; software engineering is ~50% of tool calls.
- **Source title:** Measuring AI agent autonomy in practice (Anthropic)
- **Source URL:** https://www.anthropic.com/news/measuring-agent-autonomy
- **Publication date:** 2026-02-18
- **Source type:** vendor primary data / industry report
- **Confidence:** high

### Finding 8 — The "delegation gap": ~60% AI use but only 0–20% full delegation; the bottleneck is judgment/spec, not capability
- **Claim:** Anthropic's 2026 agentic coding report (as analyzed) finds developers use AI in ~60% of work but fully delegate only 0–20% of tasks, because of missing persistent context, testable outcomes, and explicit constraints.
- **Evidence:** "Developers now use AI in roughly 60% of their work — but they report being able to fully delegate only 0–20% of tasks." "The problem isn't capability. It's judgment." Engineers currently delegate "tasks that are easy to verify or low-risk," pulling design-heavy/ambiguous work back to humans; structured intent specs act as "a delegation protocol."
- **Source title:** Anthropic's 2026 Agentic Coding Report: The Delegation/Orchestration Era (Janne Lammi, Pathmode)
- **Source URL:** https://pathmode.io/blog/orchestration-era-needs-intent
- **Publication date:** 2026-03-11
- **Source type:** blog / analysis of vendor report
- **Confidence:** medium

### Finding 9 — Google DeepMind formalizes delegation as a multi-pillar process with atomic vs open-ended vs recursive autonomy
- **Claim:** DeepMind's "Intelligent AI Delegation" defines delegation as a sequenced transfer of authority/responsibility/accountability and distinguishes atomic execution, open-ended delegation, and recursive delegation.
- **Evidence:** Delegation is "a sequence of decisions involving task allocation, that also incorporates transfer of authority, responsibility, accountability, clear specifications regarding roles and boundaries, clarity of intent, and mechanisms for establishing trust." Spectrum: "atomic execution" (strict specs, narrow tasks) → "open-ended delegation" (agents "decompose objectives and pursue sub-goals") → recursive delegation (delegating the act of delegation). Named concepts: "Zone of Indifference" (instructions "executed without critical deliberation"), "Authority Gradient," "Liability Firebreaks," "Privilege Attenuation," "Contract-First Decomposition."
- **Source title:** Intelligent AI Delegation (Tomašev, Franklin, Osindeler — Google DeepMind)
- **Source URL:** https://arxiv.org/html/2602.11865v1
- **Publication date:** 2026-02-12
- **Source type:** peer-reviewed / preprint
- **Confidence:** high

### Finding 10 — Professional developers adopt a "control-first" stance: delegate bounded tasks, retain goal/architecture decisions
- **Claim:** An empirical 2025 study of professional developers finds they delegate specific bounded tasks while controlling high-stakes/architectural decisions — a task-vs-goal delegation split driven by downstream consequence.
- **Evidence:** Title thesis — developers "prioritize control over mere 'vibes.'" Developers "appear more willing to delegate specific, bounded tasks while maintaining control over broader objectives and architectural decisions," retaining control "when outcomes significantly impact code quality, system architecture, or downstream consequences."
- **Source title:** Professional Software Developers Don't Vibe, They Control: AI Agent Use for Coding in 2025 (Huang, Reyna, Lerner, Xia, Hempel)
- **Source URL:** https://arxiv.org/pdf/2512.14012
- **Publication date:** 2025-12-17
- **Source type:** peer-reviewed / preprint
- **Confidence:** medium

### Finding 11 — Enterprise governance defines explicit agent "decision rights" tiered by reversibility
- **Claim:** Enterprise governance guidance frames decision altitude as explicitly assigned agent decision rights — autonomous, HITL-pre-approval, or HOTL-post-review — per action class.
- **Evidence:** Enterprises must define "which decisions the agent can make entirely autonomously, which decisions require a human-in-the-loop for approval before execution, and which ones require a human-on-the-loop for post-execution review." "Bounded autonomy" architectures pair "clear operational limits, escalation paths to humans for high-stakes decisions, and comprehensive audit trails." HITL "becomes a bottleneck as enterprises execute thousands or millions of agentic actions per hour."
- **Source title:** Governing the Agentic Enterprise: A New Operating Model (California Management Review, Berkeley) / 7 Agentic AI Trends to Watch in 2026 (MachineLearningMastery)
- **Source URL:** https://cmr.berkeley.edu/2026/03/governing-the-agentic-enterprise-a-new-operating-model-for-autonomous-ai-at-scale/
- **Publication date:** 2026-03
- **Source type:** industry-report / academic management review
- **Confidence:** medium

### Finding 12 — SAE J3016 is the explicit source analogy for L0–L5 agent ladders (incl. domain-specific data agents)
- **Claim:** Multiple 2026 taxonomies (data agents from HKUST/Tsinghua; coding scales; CSA) explicitly model their L0–L5 ladders on the SAE J3016 driving-automation standard.
- **Evidence:** Researchers "proposed a six-level hierarchy (L0–L5) for data agents, inspired by the SAE driving automation scale," delineating "progressive shifts in autonomy, from manual operations (L0) to fully autonomous data agents (L5)," where the framework "primarily serves to guide discussions rather than provide rigid engineering specifications."
- **Source title:** Data Agents L0-L5: Understanding the New Autonomy Hierarchy (TechLife, on HKUST/Tsinghua work)
- **Source URL:** https://techlife.blog/posts/data-agents/
- **Publication date:** 2026 (exact day unknown)
- **Source type:** blog / summary of academic work
- **Confidence:** medium

## Named Frameworks

- **Five Levels of Autonomy (user-role)** — Operator / Collaborator / Consultant / Approver / Observer. Feng, McDonald & Zhang (U. Washington / Knight First Amendment Inst.), arXiv 2506.12469, 2025. The canonical academic taxonomy; introduces **autonomy certificates**.
- **Autonomy Certificates** — third-party-issued maximum-autonomy cap backed by an "autonomy case" (analogous to a safety case). Same paper.
- **CSA Six-Level Autonomy Taxonomy (L0–L5)** — No Autonomy / Assisted / Supervised / Conditional / High / Full. Jim Reavis, Cloud Security Alliance, Jan 2026. Risk- and approval-seniority-scaled; "technically enforced" boundaries.
- **Swarmia Five Levels of Coding-Agent Autonomy** — Assistive / Conversational / Task Agent / Autonomous Teammate / Agentic Avalanche. Miikka Holkeri, Mar 2026. "Higher isn't always better"; match to task ambiguity.
- **ASDLC L1–L5 Autonomy Scale** — Assistive / Task-Based / Conditional / High / Full, each paired with a human role (Driver / Reviewer / Change Owner / Auditor / Consumer). ASDLC.io, May 2026.
- **HITL / HOTL / HOOTL oversight model** — pre-approval / monitored-intervention / no-involvement, selected by risk + reversibility; with **time-boxed decision lanes**. Strata (Eric Olden), May 2026.
- **Managed / Bounded Autonomy** — agents act within technically enforced limits, escalate on boundary exit; auto-downgrade on anomaly. CSA, Microsoft Agent 365, Berkeley CMR, 2026.
- **Intelligent AI Delegation framework** — five pillars (Dynamic Assessment, Adaptive Execution, Structural Transparency, Scalable Markets, Systemic Resilience); atomic / open-ended / recursive delegation; Zone of Indifference, Authority Gradient, Liability Firebreaks, Privilege Attenuation. Google DeepMind, arXiv 2602.11865, Feb 2026.
- **Enterprise autonomy tiers** — informational / advisory / transactional / autonomous-operational (classifying agents like data sensitivity). Surfaced in enterprise-governance reporting (Computerworld/CIO, May 2026); not individually defined in the fetched article body.
- **Data Agents L0–L5** — SAE-J3016-inspired six-level data-agent hierarchy (HKUST/Tsinghua), 2026.
- **Delegation Gap** — empirical pattern: ~60% AI use, 0–20% full delegation; bottleneck = judgment/context/spec. Anthropic 2026 agentic coding report.
- **SAE J3016 (foundational analogy)** — the autonomous-driving levels that nearly every agent ladder borrows from. Foundational; superseded for agents by the 2025–2026 role-based and risk-based ladders above.

## Debates & Tensions

1. **Higher autonomy = better? No (coding) vs. inevitable trajectory (enterprise hype).** Swarmia and ASDLC argue the value ceiling sits at Levels 2–3 and that misapplied high autonomy creates expensive cleanup; enterprise market framing (Gartner's "40% of apps by 2026," "Pioneer" teams) pushes toward ever-higher autonomy. The practitioner sources treat level as a per-task choice; the market sources treat it as a maturity curve to climb.

2. **Capability vs. judgment as the binding constraint.** Anthropic/Pathmode: "The problem isn't capability. It's judgment" — the delegation gap is about missing context, testable outcomes, and explicit constraints. DeepMind's paper, by contrast, leans on structural/market mechanisms (contracts, reputation, cryptographic verification) to enable delegation — implying the constraint is coordination infrastructure, not (only) judgment.

3. **Autonomy as design choice vs. emergent property.** Feng et al. insist autonomy is "a deliberate design decision, separate from capability." Anthropic's data shows autonomy *drifting upward in practice* as users build trust (turn durations doubling, auto-approve rising) — i.e., emergent escalation, sometimes ahead of formal design.

4. **Is HITL the safety floor or the bottleneck?** Governance sources (EU AI Act Art. 14, OnReach, Strata) treat HITL as mandatory for high-risk domains; the same 2026 sources warn HITL "becomes a bottleneck as enterprises execute thousands or millions of agentic actions per hour," pushing toward HOTL/exception-based oversight. The unresolved tension: how to keep "meaningful human control" without per-action gating.

5. **"Agent-in-the-Loop" replacing HITL.** Analytics India Magazine argues among leading global capability centers "Agent-in-the-Loop (AITL) is replacing HITL" — a contested claim that other governance sources (Strata, CSA, Berkeley CMR) push back on by reasserting human approval for high-stakes/irreversible actions.

6. **Who issues autonomy certificates / decision rights?** Feng et al. propose third-party governing bodies; enterprise vendors (Microsoft Agent 365, Google AI Control Center) internalize it as platform controls; CIO reporting notes "better logs do not automatically settle questions of control or responsibility," flagging an unresolved accountability gap across system chains.

## Sources

- Feng, McDonald, Zhang — *Levels of Autonomy for AI Agents* — https://arxiv.org/abs/2506.12469 — 2025-06-14 (rev. 2025-07-28) — peer-reviewed/working paper. Mirror: https://knightcolumbia.org/content/levels-of-autonomy-for-ai-agents-1 ; summary: https://www.aigl.blog/levels-of-autonomy-for-ai-agents/
- Jim Reavis (Cloud Security Alliance) — *Autonomy Levels for Agentic AI* — https://cloudsecurityalliance.org/blog/2026/01/28/levels-of-autonomy — 2026-01-28 — industry/standards body
- Miikka Holkeri (Swarmia) — *Five levels of AI coding agent autonomy, and why higher isn't always better* — https://www.swarmia.com/blog/five-levels-ai-agent-autonomy/ — 2026-03-19 — vendor/practitioner blog
- ASDLC.io — *Levels of Autonomy: L1-L5 AI Agent Autonomy Scale* — https://asdlc.io/concepts/levels-of-autonomy/ — 2026-05-28 — industry framework
- Anthropic — *Measuring AI agent autonomy in practice* — https://www.anthropic.com/news/measuring-agent-autonomy — 2026-02-18 — vendor primary data
- Janne Lammi (Pathmode) — *Anthropic's 2026 Agentic Coding Report: The Delegation/Orchestration Era* — https://pathmode.io/blog/orchestration-era-needs-intent — 2026-03-11 — blog/analysis
- Tomašev, Franklin, Osindeler (Google DeepMind) — *Intelligent AI Delegation* — https://arxiv.org/html/2602.11865v1 — 2026-02-12 — preprint
- Huang, Reyna, Lerner, Xia, Hempel — *Professional Software Developers Don't Vibe, They Control* — https://arxiv.org/pdf/2512.14012 — 2025-12-17 — preprint
- Eric Olden (Strata Identity) — *Human-in-the-Loop: A 2026 Guide to AI Oversight* — https://www.strata.io/blog/agentic-identity/practicing-the-human-in-the-loop/ — 2026-05-11 — vendor blog
- California Management Review (UC Berkeley) — *Governing the Agentic Enterprise* — https://cmr.berkeley.edu/2026/03/governing-the-agentic-enterprise-a-new-operating-model-for-autonomous-ai-at-scale/ — 2026-03 — academic management review
- MachineLearningMastery — *7 Agentic AI Trends to Watch in 2026* — https://machinelearningmastery.com/7-agentic-ai-trends-to-watch-in-2026/ — 2026 — blog
- Prasanth Aby Thomas (CIO/Computerworld) — *Microsoft, Google push AI agent governance into enterprise IT mainstream* — https://www.cio.com/article/4167059/microsoft-google-push-ai-agent-governance-into-enterprise-it-mainstream-2.html — 2026-05-05 — news
- TechLife — *Data Agents L0-L5: Understanding the New Autonomy Hierarchy* (on HKUST/Tsinghua data-agents work) — https://techlife.blog/posts/data-agents/ — 2026 — blog/summary
- Analytics India Magazine — *Human-in-the-Loop Is Out, Agent-in-the-Loop Is In* — https://analyticsindiamag.com/ai-highlights/human-in-the-loop-is-out-agent-in-the-loop-is-in/ — 2025/2026 — news (contested claim)
- METR — *We are Changing our Developer Productivity Experiment Design* — https://metr.org/blog/2026-02-24-uplift-update/ — 2026-02-24 — research org blog (context on measuring autonomous task completion)
