---
topic: "Optimal agent communication patterns in LLM workflows"
goals: "Inform decisions about how agents in Momentum should communicate"
profile: light
date: 2026-04-09
sub_questions:
  - "What communication mechanisms exist in Claude Code (Agent tool, SendMessage, TeamCreate), when should agents communicate directly vs. return to an orchestrator, and how do fan-out, pipeline, and collaborative team patterns differ in practice?"
  - "How should message payloads be structured (JSON vs. natural language vs. hybrid) and what context/state should be passed between agents vs. re-derived — and how do poor decisions here degrade performance?"
  - "What are the known failure modes of multi-agent communication in LLM systems (message loss, context bleed, cascading errors) and how are they mitigated?"
---

# Research Scope: Optimal Agent Communication Patterns in LLM Workflows

**Date:** 2026-04-09
**Profile:** light
**Goals:** Inform decisions about how agents in Momentum should communicate

## Sub-Questions

1. What communication mechanisms exist in Claude Code (Agent tool, SendMessage, TeamCreate), when should agents communicate directly vs. return to an orchestrator, and how do fan-out, pipeline, and collaborative team patterns differ in practice?
2. How should message payloads be structured (JSON vs. natural language vs. hybrid) and what context/state should be passed between agents vs. re-derived — and how do poor decisions here degrade performance?
3. What are the known failure modes of multi-agent communication in LLM systems (message loss, context bleed, cascading errors) and how are they mitigated?
