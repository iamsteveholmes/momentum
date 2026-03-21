# Section 3: Approval/Review Fatigue in Agentic Workflows

## 3.1 The Rubber-Stamping Phenomenon

**The core problem is well-documented across multiple domains.** When humans are asked to oversee AI systems at scale, oversight degrades into ritual approval.

**Cybermaniacs** identifies four root causes: (1) volume and velocity -- AI generates decisions faster than reviewers can meaningfully evaluate them; (2) opacity -- non-technical reviewers lack context to question algorithmic outputs; (3) cognitive fatigue -- extended review sessions reduce critical scrutiny; (4) cultural pressure -- employees assume automation is superior or fear challenging systems. Their conclusion: oversight without role clarity, training, decision criteria, or feedback mechanisms becomes "mechanical rather than analytical."

**MIT Sloan Management Review** covers the explainability angle: 77% of experts disagree that effective human oversight reduces the need for explainability, arguing that explainability and human oversight are complementary. Without insight into *why* an AI reached its conclusion, oversight becomes superficial.

**Lumenova AI** frames the structural impossibility: "AI agents operate at machine speed. An agent might execute dozens of tool calls" in the time a human reviews initial instructions. They identify three failure modes: speed incompatibility (approving every step destroys efficiency; reviewing only final outputs misses errors), cognitive fatigue leading to rubber-stamping, and unsustainable reviewer-to-agent ratios as deployment scales.

A **European Commission study (2025)** reportedly found that "human oversight" too often becomes "ritual supervision, someone clicking 'approve' because the system says so."

**Sources:**
- [Rubber Stamp Risk: Why Human Oversight Can Become False Confidence](https://cybermaniacs.com/cm-blog/rubber-stamp-risk-why-human-oversight-can-become-false-confidence)
- [AI Explainability: How to Avoid Rubber-Stamping Recommendations (MIT Sloan)](https://sloanreview.mit.edu/article/ai-explainability-how-to-avoid-rubber-stamping-recommendations/)
- [Agentic AI Risk Management: Moving Beyond Human Oversight (Lumenova)](https://www.lumenova.ai/blog/agentic-ai-risk-management/)

---

## 3.2 StackAI on Approval Workflow Design

**StackAI's article** on human-in-the-loop AI agents directly addresses the approval burden vs. risk reduction tension. Key positions:

- **Evidence packs are the critical differentiator**: "Most approval workflows fail because reviewers are asked to approve blind. The evidence pack is the difference between a 15-second approval and a 15-minute investigation." Without structured context (decision rationale, confidence scores, historical data), reviewers cannot make informed decisions and default to rubber-stamping.

- **Approval governance must be auditable**: "If you can't show who approved what, when, and why, you don't have a defensible approval workflow."

- **Silent failure risk**: Explicit behavior for "waiting on humans" is necessary to prevent approval queues from becoming silent failure points -- requests that sit indefinitely because no one noticed.

- **Idempotency as trust enabler**: "If you only implement one 'grown-up' engineering practice for human-in-the-loop AI agents, make it idempotency. Duplicated side effects are one of the fastest ways to lose trust."

- **Risk-stratified routing**: High-risk actions (payments, refunds, access provisioning, external communications) require human gates; low-risk actions proceed autonomously.

**Source:**
- [Human-in-the-Loop AI Agents: How to Design Approval Workflows (StackAI)](https://www.stackai.com/insights/human-in-the-loop-ai-agents-how-to-design-approval-workflows-for-safe-and-scalable-automation)

---

## 3.3 Aviation Systems Research: Automation Bias and Omission Errors

**The 55% figure comes from Mosier et al. (1998)**, not from Molloy/Parasuraman (1996), though both are foundational.

**Mosier, Dunbar, McDonnell, Skitka, Burdick & Rosenblatt (1998)** -- "Automation Bias and Errors: Are Teams Better than Individuals?" -- found a **55% omission error rate** in aviation contexts. Omission errors are defined as failures to respond to system irregularities because automated devices fail to detect or indicate them. Critically, omission error rates correlated with pilot experience: more experienced pilots were *more* susceptible, not less, because increased trust in automation served as a heuristic replacement for vigilant information seeking.

**Molloy & Parasuraman (1996)** -- "Monitoring an Automated System for a Single Failure: Vigilance and Task Complexity Effects" -- found that in complex multitask conditions (flight simulation with tracking, fuel management, and engine monitoring), detection of automation failures was significantly poorer under automated control than manual control. Detection rates degraded over time: more participants detected failures in the first 10 minutes of a 30-minute session than in the last 10 minutes (vigilance decrement).

**A systematic review of automation bias (Goddard, Roudsari & Wyatt, 2012, PMC3240751)** synthesized findings across domains: erroneous automated advice increased incorrect decision risk by 26% (risk ratio 1.26, 95% CI 1.11-1.44). The review identified key bias amplifiers: trust calibration, individual cognitive styles, task inexperience, increased workload/complexity, time pressure, and -- paradoxically -- high system reliability (because users stop checking). The optimal reliability threshold for maintaining human vigilance was identified at approximately 70%.

**The two error types** provide a useful framework for agentic workflows:
- **Commission errors**: Following incorrect AI advice without verification (acting on bad output)
- **Omission errors**: Failing to notice problems because the AI didn't flag them (missing what wasn't surfaced)

**Sources:**
- [Mosier et al. 1998 - Automation Bias and Errors (SAGE)](https://journals.sagepub.com/doi/10.1177/154193129804200304)
- [Molloy & Parasuraman 1996 - Monitoring an Automated System (SAGE)](https://journals.sagepub.com/doi/10.1177/001872089606380211)
- [Automation Bias: Systematic Review (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751/)

---

## 3.4 Developer Community Testimony

Four Hacker News threads surface the approval fatigue problem with specific developer testimony:

**"I tried coding with AI, I became lazy and stupid" (HN #44858641)**

- On loss of mental models: "You're building up a mental model of the codebase as you write it...If you're using an AI to produce code you're not building up any model at all." (fzeroracer)
- On rubber-stamping in teams: "It's a large enough team and there are members that rubber stamp everything. Takes just a lunch break for the review to go up and get approved." (cogman10)
- On the irresistible pull: "The only way this can be avoided is by diligently checking every single diff the LLM makes. But let's be honest, its just so damn inviting to let it off the leash for a moment." (CjHuber)

**"Vibe coding creates fatigue?" (HN #46292365)**

- On the generative-to-processing shift: "I still have to do a lot of validation myself that would have been done while writing the code by hand. This turns the process from 'generative' to 'processing.'" (commenter with ADHD)
- On exhaustion by noon: "It's now 11:47am and I am mentally exhausted...Keeping up with AI tools requires a great deal of mental effort."
- On babysitting dynamics: "Watching as a machine does in an hour what would take me a week. But also watching to stop the machine spin around doing nothing for ages because it's got itself in a mess."
- On the review mode trap: "When an LLM is running, you can't do this...you come back into 'review mode' and have to think architecturally about the changes made."

**"Vibe coding has turned senior devs into AI babysitters" (HN #45242788)**

- On fundamental inefficiency: "I spend more time telling AI what to do than it would spend actually writing this all out myself."
- On boredom and role loss: "Reviewing and fixing AI code made me incredibly bored...I want to actually build things, not manage AI."
- On the perception-reality gap: While developers feel 20% faster with AI, studies suggest they are actually "20% SLOWER with it."
- On 2000-line AI PRs: "I've seen people push 2000 line PRs" of poor quality that consume excessive review cycles.

**"Vibe Coding Paralysis" (HN #46844214)**

- On possibility overload: "When everything is instant, nothing feels finished. You stop thinking in terms of 'building' and start thinking in terms of 'possibilities,' which overloads decision-making. Infinite leverage -> infinite branches -> cognitive freeze."

**Sources:**
- [I tried coding with AI, I became lazy and stupid (HN)](https://news.ycombinator.com/item?id=44858641)
- [Vibe coding creates fatigue? (HN)](https://news.ycombinator.com/item?id=46292365)
- [Vibe coding has turned senior devs into AI babysitters (HN)](https://news.ycombinator.com/item?id=45242788)
- [Vibe Coding Paralysis (HN)](https://news.ycombinator.com/item?id=46844214)

---

## 3.5 "Vibe Coding" Criticism and Technical Debt

**Francesco Bonacci** (CEO of Cua, YC X25) coined "vibe coding paralysis" to describe the syndrome where infinite AI productivity leads to finishing nothing. He wrote: "I end each day exhausted -- not from the work itself, but from the managing of the work." His description of the mechanism: within an hour you have "five worktrees, three half-implemented features running in parallel, and you can't remember what the original task was." He frames this as "a kind of cognitive overload masked as productivity."

**The $1.5 trillion debt projection**: Fast Company reported (September 2025) that analysts predict $1.5 trillion in technical debt by 2027, driven by the "code first, understand later" approach. Forrester separately projects 75% of tech decision-makers facing moderate-to-severe debt by 2026. Over 8,000 startups reportedly now need rebuilds or rescue engineering.

**Rachel Thomas (fast.ai)** describes vibe coding as inducing "junk flow" (Csikszentmihalyi's term for addictive but non-growth activities) and "dark flow" (a gambling research term for insidious false-flow states) -- psychological traps similar to gambling addiction where developers experience false accomplishment. She cites the METR study finding that developers estimated they were working 20% faster, yet in reality worked 19% slower -- nearly a 40% perception-reality gap. Developer Armin Ronacher is quoted: "I felt really great about [tools], just to realize that I did not actually use them or they did not end up working as I thought."

**The debt accumulation mechanism** ties directly to approval fatigue: a junior or fatigued senior developer is "lulled into a false sense of security by the 'professionalism' of the AI's output." The developer ships it because it works. Months later, someone needs to modify that code but cannot understand it because the original developer did not write it and does not understand it either.

**Sources:**
- [Francesco Bonacci on Vibe Coding Paralysis (X/Twitter)](https://x.com/francedot/status/2017858253439345092)
- [Vibe Coding Hangover: $1.5T Debt Warning (ByteIota)](https://byteiota.com/vibe-coding-hangover-2/)
- [Breaking the Spell of Vibe Coding (fast.ai)](https://www.fast.ai/posts/2026-01-28-dark-flow/)

---

## 3.6 Stephan Schmidt's "Too Fast to Think"

**Author**: Stephan Schmidt, AI and CTO Coach, Engineering Leadership Veteran.
**Published**: July 14, 2025, Tabula Mag.

Schmidt identifies **three fatigue mechanisms**:

**1. Cognitive Load Mismatch**: AI operates at speeds incompatible with human cognitive processing. Traditional coding allows brain processing time proportional to task complexity, but vibe coding compresses complex tasks into seconds. The developer lacks "baking time to mentally process architecture, decisions and edge cases." Schmidt's metaphor: "running a marathon at the pace of a sprint -- speeds don't match."

**2. Accelerated Context Switching**: Each context switch demands significant mental energy. With AI tools, the frequency increases dramatically, forcing rapid pivots between code modules, functions, and packages. Even tab completions create micro-content switches from function to function that drain cognitive resources faster than the brain can replenish them.

**3. Inverted Dopamine Loop**: Traditional coding provides satisfaction through write code -> encounter failure -> fix -> success. With AI acceleration, this loop speeds up dramatically. Faster dopamine cycles combined with stress hormones create fatigue instead of satisfaction -- the opposite of normal coding fulfillment.

Schmidt's metaphor for the overall experience: "We're like early pilots flying with autopilot -- capable, but drained." His conclusion: "Maybe the future of coding isn't just faster. Maybe it's also slower in a way, on purpose."

**Source:**
- [Too Fast to Think: The Hidden Fatigue of AI Vibe Coding (Tabula Mag)](https://www.tabulamag.com/p/too-fast-to-think-the-hidden-fatigue)

---

## 3.7 Kodus.io on AI Fatigue

Kodus frames the problem as a fundamental role inversion: developers using AI assistants "become a full-time reviewer for a junior developer who never sleeps, never learns your project's specific context, and never gets tired."

**The cognitive cost analysis**: When reviewing an AI suggestion, developers must first reverse-engineer the AI's logic, then map it back to their own. This validation cycle, repeated dozens or hundreds of times per day, "fragments attention, changing cognitive load from focused creative work into scattered validation checks."

**The role shift**: "When your IDE is constantly suggesting entire blocks of code, your job changes from creating to validating." This trades "the focused effort of building for the scattered effort of auditing."

**Proposed solutions** (control-first approach):
- **On-demand use only**: Use AI for scaffolding, boilerplate, and explicit refactoring tasks -- not as a constant suggestion engine
- **Code review practices**: Flag AI-generated code explicitly, check architectural compliance, document AI use
- **Measurement**: Track full cycle time (not just generation time), bug patterns from AI code, and developer feedback on focus quality

**Source:**
- [AI Fatigue for Developers: Managing Cognitive Overload from Code Assistants (Kodus)](https://kodus.io/en/ai-fatigue-developers-reclaim-control/)

---

## 3.8 Proposed Solutions and Effectiveness Evidence

**A. Dynamic Routing by Risk Level**

The **MyEngineeringPath guide (2026)** frames this as "calibrated autonomy": full autonomy for high-confidence, reversible, low-stakes actions; human approval layer for uncertain, irreversible, or high-risk actions.

**Multimodal.dev** describes tiered confidence frameworks in production: high-confidence outputs auto-approve, medium-confidence decisions escalate for supervisor review, and low-confidence results route to specialist human reviewers. Specific thresholds are tuned per workflow based on historical accuracy, domain risk tolerance, and regulatory requirements.

**B. Context/Evidence Packs**

StackAI's central design principle: the difference between a 15-second approval and a 15-minute investigation is the evidence pack.

**C. Confidence Calibration**

The automation bias literature provides the key insight: **calibration matters more than the score itself**. Systems with approximately 70% reliability maintained better human vigilance than those with very high reliability (where users stopped checking).

**D. Automation Bias Mitigators (from the systematic review)**

Effective interventions include: presenting information rather than direct recommendations (forcing the human to form their own conclusion), reducing prominence of advice on-screen, training with accountability emphasis, providing updated confidence levels on system output, and adaptive task allocation that varies system reliability.

**E. Structural Solutions from Lumenova**

Rather than relying on human oversight as the primary control, implement automated guardrails as an "always-on control plane" -- input/output filtering, behavioral constraints, and logic consistency checks that operate in milliseconds. Human oversight becomes "the exception rather than the default control mechanism."

---

## Key Quantitative Findings Summary

| Finding | Source |
|---|---|
| 55% omission error rate in aviation automation monitoring | Mosier et al. 1998 |
| 26% increased risk of incorrect decisions from erroneous automated advice (RR 1.26) | Goddard, Roudsari & Wyatt 2012 systematic review (PMC3240751) |
| ~70% system reliability is optimal for maintaining human vigilance | Goddard et al. 2012, citing Madhavan & Wiegmann |
| Developers perceive 20% speedup but measure 19% slowdown (39% perception gap) | METR study, cited by Thomas (fast.ai, 2026) |
| $1.5 trillion projected technical debt by 2027 from AI-generated code | Fast Company / analyst estimates |
| 75% of tech decision-makers facing moderate-to-severe debt by 2026 | Forrester |
| 8,000+ startups needing rebuilds from vibe-coded systems | ByteIota reporting |

**Sources:**
- [Human-in-the-Loop Patterns for AI Agents 2026 (MyEngineeringPath)](https://myengineeringpath.dev/genai-engineer/human-in-the-loop/)
- [Using Confidence Scoring to Reduce Risk (Multimodal.dev)](https://www.multimodal.dev/post/using-confidence-scoring-to-reduce-risk-in-ai-driven-decisions)
- [Automation Bias Systematic Review (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751/)
- [Agentic AI Risk Management (Lumenova)](https://www.lumenova.ai/blog/agentic-ai-risk-management/)
