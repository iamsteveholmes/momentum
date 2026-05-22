---
content_origin: claude-code-subagent
date: 2026-05-22
sub_question: "Why did Gas Town/Gas City build their own orchestration primitives instead of adopting Temporal, Prefect, or LangGraph?"
topic: "Gas Town as dispatcher/coordinator for Momentum agentic engineering"
---

# Gas City Design Rationale: Why They Built Their Own Orchestration Primitives

## Research Question

Has the Gas Town/Gas City team explicitly explained why they didn't build on top of Temporal, Prefect, LangGraph, or another existing workflow engine — and what is the principled basis (if any) for building from scratch?

## Sources Consulted

- `AGENTS.md` [OFFICIAL] — gastownhall/gascity — primary design contract document
- `README.md` [OFFICIAL] — gastownhall/gascity — architecture and design principles
- `README.md` [OFFICIAL] — gastownhall/gastown — problem statement and concept definitions
- PR #2394: `engdocs/research/w-gc-004-orchestration-framework-survey.md` [OFFICIAL] — Gas City's own internal orchestration framework comparison survey (2026-05-20, open but reviewed)
- "Welcome to Gas City" — steve-yegge.medium.com [PRAC] — design philosophy post
- "Gas Town: From Clown Show to v1.0" — steve-yegge.medium.com [PRAC]
- "Welcome to the Wasteland" — steve-yegge.medium.com [PRAC]
- HN threads on Gas Town/Gas City announcements [PRAC]

---

## The Team's Stated Rationale

**They don't explain the Temporal decision because they never framed it as a Temporal decision.** [CONFIRMED]

Across all blog posts, the Gas City README, and AGENTS.md, Temporal, Prefect, and LangGraph are never mentioned as rejected alternatives. The team did not arrive at Gas City by evaluating workflow engines and finding them wanting — they arrived by extracting primitives from Gas Town (a working system they had already built) and asking what had to be in the SDK versus what was role configuration. The internal orchestration survey (PR #2394, authored May 2026, after Gas City was already built) is the first time the team formally maps their primitives to existing frameworks. This is retrospective comparison, not build-or-buy deliberation.

The stated origin story, from the Gas City AGENTS.md [OFFICIAL], is explicit:

> "Gas Town proved multi-agent orchestration works, but all its roles are hardwired in Go code. Steve realized the MEOW stack (Molecular Expression of Work) was powerful enough to abstract roles into configuration. Gas City extracts that insight into an SDK where Gas Town becomes one configuration among many."

The catalyst was an internal refactoring insight — not a competitive analysis.

---

## The Core Thesis: Four Architectural Laws

The Gas City architecture is organized around four named principles, all sourced directly from the Gas City README [OFFICIAL]:

**Zero Framework Cognition (ZFC):** "Go handles transport, not reasoning. If a line of Go contains a judgment call, it's a violation. The ZFC test: does any line of Go contain a judgment call? An `if stuck then restart` is framework intelligence. Move the decision to the prompt."

**The Bitter Lesson filter:** "Every primitive must become MORE useful as models improve, not less. Don't build heuristics or decision trees."

**GUPP (pull model):** "If you find work on your hook, YOU RUN IT. No confirmation, no waiting. The hook having work IS the assignment. This is rendered into agent prompts via templates, not enforced by Go code."

**Nondeterministic Idempotence (NDI):** "The system converges to correct outcomes because work (beads), hooks, and molecules are all persistent. Sessions come and go; the work survives. Multiple independent observers check the same state idempotently. Redundancy is the reliability mechanism."

These four together constitute the real answer to "why not Temporal." Temporal's durable execution model is fundamentally framework-intelligent: it makes decisions about retries, checkpoints, and replay inside the engine. Under ZFC, every such decision is a bug. The engine must not reason; only the model reasons.

---

## Whether They Addressed Temporal/Prefect Directly

**Never explicitly, until the internal survey — and even then, Temporal and Prefect are absent.** [CONFIRMED]

The internal survey (w-gc-004, PR #2394 [OFFICIAL]) covers: AutoGen, CrewAI, LangGraph, OpenAI Swarm/Agents SDK, smolagents, Inspect AI, Claude Agent SDK, and Magentic-One. Temporal and Prefect are not included.

On LangGraph specifically, the survey identifies both the strength and the incompatibility:

> "Gets right: Durable resume from checkpoint provides strongest failure model in survey. Where Gas City diverges: Control flow encoded in Python; conditional edges violate ZFC; Gas City expresses branching via Event Bus gate conditions."

The survey notes that AWS Bedrock Agents, Google Vertex, and OpenAI Assistants are "category errors — they compete with running Gas City, not being one." Temporal and Prefect would likely receive the same categorization: they are general-purpose workflow engines for human-written deterministic code, not SDKs for building LLM-coordinated agent systems. The survey doesn't state this — it simply doesn't survey them.

The HN discussions on both major threads show no commenter pressed this comparison and received no team response on it. The question was never engaged publicly.

---

## The Coding-Agent Specificity Argument

This is where the most principled reasoning lives. From the Gas City README [OFFICIAL]:

> **What Gas City does NOT contain — permanent exclusions, not "not yet." Each fails the Bitter Lesson test — it becomes LESS useful as models improve:**
> - No skills system — the model IS the skill system
> - No capability flags — a sentence in the prompt is sufficient
> - No MCP/tool registration — if a tool has a CLI, the agent uses it
> - No decision logic in Go — the agent decides from prompt and reality
> - No hardcoded role names — roles are pure configuration

This is the answer to why Temporal breaks for this domain. Temporal encodes workflow logic in code — it assumes the workflow is deterministic and the human wrote it. Gas City's thesis is that model-driven workflows should never encode their own logic in the orchestrator. The orchestrator provides: session management, a durable task store, an event bus, config, and prompt templates. The model decides everything else. Any orchestrator that makes decisions — Temporal's retry policies, LangGraph's conditional edges, CrewAI's hierarchical process selection — is violating ZFC and failing the Bitter Lesson.

The internal survey confirms this pattern holds across all surveyed frameworks:

> "ZFC is genuinely uncommon. LangGraph's conditional edges, Magentic-One's stall detection, CrewAI's Process selection, and AutoGen's topic routing all contain framework judgment calls. Only smolagents and Inspect AI take minimal stance by punting orchestration."

The honest gap acknowledged in the survey: Gas City has no checkpoint primitive equivalent to LangGraph's durable execution. The team's position appears to be that NDI (beads survive sessions; rehook on restart) is sufficient, but this is noted as an open question.

---

## Synthesis and Assessment

**Is this a principled design choice or NIH?** [INFERRED]: It is a principled design choice that happens to make NIH rational, not NIH rationalized as principle.

Evidence for principled design:

1. The four constraints (ZFC, Bitter Lesson, GUPP, NDI) are stated as falsifiable tests, not aesthetics. A `primitive-test.md` document applies these as gates on all new additions. These are load-bearing architectural rules, not post-hoc justifications.

2. The internal survey honestly acknowledges gaps and borrowable patterns — LangGraph's checkpointer, Inspect AI's handoff/as_tool split, Magentic-One's dual ledger. A NIH posture would not produce that list.

3. The permanent exclusion list is specific and falsifiable. "No skills system — the model IS the skill system" is a testable claim about model capability.

4. The "Kubernetes mated with Temporal" framing does not appear in any primary source. It is external characterization. Gas City describes itself as an "orchestration-builder SDK" with k8s as one of five runtime backends (tmux, subprocess, exec, k8s, fake).

The case against pure principle: Gas City was extracted from Gas Town, which Yegge built rapidly under his own description ("janky," "a lot of duct tape"). The principled framework (ZFC, Bitter Lesson) appears to have been articulated during and after Gas City's extraction, not before Gas Town's construction. The principles fit the system that was built. Given the survey's intellectual honesty about gaps, this reads as genuine learning rather than rationalization.

---

## Open Questions

1. **Yegge has never directly answered "why not Temporal" in any indexed public forum.** The question has not been put to him directly.

2. **The checkpoint gap is acknowledged but unresolved.** Whether NDI (rehook on crash, beads survive) is sufficient for production coding-agent reliability at scale is an empirical question the team has not answered publicly.

3. **Temporal and Prefect's absence from the survey is itself significant.** The team appears to view them as category-mismatched (deterministic workflow engines for human-written code, not LLM-agent SDKs), but this is inferred, not stated.
