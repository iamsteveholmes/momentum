---
content_origin: human
date: 2026-04-26
topic: "everything-claude-code vs Momentum — comparative analysis"
practitioner: Steve Holmes
---

# Practitioner Notes — Steve's Q&A Responses

These notes capture Steve's (the Momentum maintainer's) reactions to AVFL-derived practitioner questions on 2026-04-26. They are practitioner judgment captured for synthesis grounding.

## Critical practice feedback — Q&A model is wrong

**Steve's feedback:**
> "I believe we have a weakness in the way we do the research Q/A. How could I possibly know if I agree with something I haven't myself researched? I would think the Q/A would be perhaps a presentation to me about what various researchers found and an open question about what questions I have rather than the agent asking me my own opinion on research I haven't looked at at all."

**Action taken:**
Saved as durable feedback memory: `feedback_research_qa_model.md` in `~/.claude/projects/.../memory/`. The next iteration of `momentum:research` Phase 4 should: (1) present a structured findings digest first, (2) prompt the practitioner with open invitations to investigate further, (3) optionally spawn additional verification subagents based on the practitioner's questions, (4) capture all of this as `raw/practitioner-notes.md`.

## Q1 — Integration scope

Steve declined to opine on which ECC components to adopt without first reading the components themselves. Defers to deeper investigation. See Q3 below — same pattern.

## Q2 — AGENTS.md / cross-agent compatibility

**Steve:** "Definitely want it to be cross-agent."

Verdict: Momentum should adopt `AGENTS.md` and pursue cross-CLI usability (OpenCode/Codex/Cursor/etc.). The portability subagent estimated this as a few hours of work — adding a project-root `AGENTS.md` is the cheapest first step.

## Q3 — ECC's adversarial validation skills (gan-style-harness vs santa-method)

**Steve:** Same as Q1 — wants to *see* what those skills offer before forming an opinion on adoption.

Action: Defer until synthesis presents the actual mechanisms; flag for follow-up.

## Q4 — `continuous-learning-v2`

**Steve:** "I'd sure like to understand it better."

Action: Spawned a follow-up subagent (`deep-dive-continuous-learning.md`) to read the actual SKILL.md, hooks, and data flow. Output will be presented in synthesis.

## Q5 — Bus factor & star anomaly

**Steve:** "Definitely. I'm seeing over and over that many of the AI projects are faking their github stars. This isn't necessarily something the project itself is doing, it might be external, or they have a single malicious bot or developer causing this misalignment. In my experience that doesn't mean that the project isn't legit, but it definitely DOES mean that the github stars and many other metrics should be wholly thrown out. The actual commits, bug fixes, etc. are a better metric. Not really gamed as easily."

**Action taken:**
Saved as durable feedback memory: `feedback_github_stars_unreliable.md`. For AI / agentic-tooling research, surface metrics like GitHub stars are gameable and should be discarded. Trust commits, contributor distribution, downloads, issue/PR throughput.

**Implication for synthesis:** when characterizing ECC's traction, lead with verified-commit and contributor metrics (1,465 commits, 159 contributors, bus factor 1, monthly major releases, 36-job CI matrix), and explicitly bracket the 167K star count as an unreliable surface metric.

## Q6 — Hackathon attribution — DIG IN

**Steve:** "This definitely matters. I don't want fakeness. Dig into this one. Fire off sub agents to get additional verifications if you need to."

**Action taken:**
Spawned a follow-up subagent (`verification-hackathon-and-identity.md`) to verify both hackathons (Forum Ventures Sep 2025 and Cerebral Valley × Anthropic Feb 2026) AND Affaan Mustafa's identity. Subagent will report what's verifiable from independent sources vs only-from-the-README.

## Q7 — Synthesis emphasis

**Steve:** "I'd say C → B → A as one sort of leads to the other."

So the synthesis structure is:
1. **C — Philosophical contrast** (toolkit vs practice) — establishes the framing
2. **B — Granular component-by-component scorecard** with effort estimates — concrete inventory
3. **A — Strategic verdict** (stay independent + cherry pick) — emerges from B

This matches the SQ8 (integration-assessment) report's recommendation pattern.

## Q8 — Anything else

**Steve:** "No. Except I think we need to update how we do Q/A. Some of this was very useful, and some of it was not."

Both feedback items captured as memory entries (Q&A model + GitHub stars unreliable). Done.

## Implications for synthesis

- Lead with philosophical contrast (C).
- Component scorecard (B) needs effort estimates for every adoption candidate, not just the top 3.
- Final strategic verdict (A) should integrate Q4's `continuous-learning-v2` findings and Q6's hackathon verification when those subagents report.
- De-emphasize GitHub star count as a maturity signal; use commit volume, contributor distribution, downloads, CI infrastructure instead.
- Note explicitly in the synthesis the `AGENTS.md` adoption recommendation as a concrete short-term action.
- Acknowledge the corpus has degraded validator coverage in 3 of 4 lenses (one validator failed, one stalled, one returned a stub) — synthesis should be tagged accordingly.
