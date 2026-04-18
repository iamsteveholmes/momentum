Research Topic: Optimal agent communication patterns in LLM workflows — how should agents in multi-agent systems communicate for reliability, correctness, and performance

I need a comprehensive analysis of how to architect communication between LLM agents in multi-agent workflows, with specific focus on Claude Code's mechanisms (Agent tool, SendMessage, TeamCreate).

Research Goals: Inform decisions about how agents in Momentum should communicate — specifically when to use direct agent-to-agent communication vs. orchestrator-mediated return, how to structure message payloads, what context to pass vs. re-derive, and how to prevent known failure modes.

Key questions to investigate:

1. What communication mechanisms exist in Claude Code (Agent tool, SendMessage, TeamCreate), when should agents communicate directly vs. return to an orchestrator, and how do fan-out, pipeline, and collaborative team patterns differ in practice — with concrete tradeoff analysis for each?

2. How should message payloads be structured (JSON vs. natural language vs. hybrid) and what context/state should be passed between agents vs. re-derived — what does poor design here look like, and how does it degrade performance or correctness?

3. What are the known failure modes of multi-agent communication in LLM systems (message loss, context bleed, cascading errors, feedback loops, coordination failures) and what mitigation patterns are empirically validated?

Desired output: A structured report with findings organized by question, including:
- Specific actionable recommendations where available
- Example patterns or implementations where relevant
- Citations with URLs for every factual claim
- An honest assessment of current limitations and gaps

Date context: Today is 2026-04-09. Prioritize current and recent sources.
