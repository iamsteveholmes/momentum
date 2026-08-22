Research Topic: Gas City (gastownhall/gascity) human-in-the-loop gates and multi-phase cycle orchestration

I need a comprehensive analysis of Gas City's current (August 2026) support for human-in-the-loop gates inside orchestrated formula workflows, and its fitness for orchestrating a multi-phase engineering cycle (triage → planning → build → retrospective) where humans must approve at specific gates.

Research Goals: Determine whether Gas City's [steps.gate] mechanism, check loops, and converge gates can implement mandatory human approval points; what notification/watcher infrastructure exists; how mature and stable the project is; and what its beads dependency requires (Dolt vs file backend).

Key questions to investigate:

1. Gate mechanics: how does the v2 formula [steps.gate] table work in current releases — gate beads, blocking edges, manual closure? The spec says the gate type vocabulary (human, timer, gh:pr, mail) is doc-comment-only with no bundled watcher and zero bundled formulas using gates. Is that still true? Any recent releases, PRs, or roadmap items productizing human gates?
2. Human verdict and HITL patterns: how do practitioners implement approve/iterate/reject human decisions in formulas — check loops with verdict-as-bead-metadata, converge manual gates, steps assigned to humans, mail-to-human? What do maintainers recommend?
3. Notification and observation: how does a human learn a gate is waiting — dashboard, gc events --follow, mail beads, integrations? What watcher infrastructure exists or is planned?
4. Multi-phase cycle orchestration: can formulas + orders chain distinct phases (each running a CLI coding agent like claude -p) with event-triggered orders creating a continuous cycle? What are the harness recipes for Claude Code as the agent runtime?
5. Maturity and stability: status of Orchestration v3 (issue #1709), dispatcher wedge bugs #2131/#2168, barrier race #2311, container-dependency gap #3451; release cadence in 2026; v1→v2 formula migration state; production adopters.
6. Beads backend requirements: is GC_BEADS=file still supported, or is Dolt required in current releases? What are the operational costs of the Dolt path (e.g. dolt-bloat-recovery runbooks in the docs)?

Desired output: A structured report with findings organized by question, including:
- Specific actionable recommendations where available
- Example patterns or implementations where relevant
- Citations with URLs for every factual claim
- An honest assessment of current limitations and gaps

Date context: Today is 2026-08-21. Prioritize current and recent sources (docs.gascity.com, github.com/gastownhall/gascity and gascity-packs, maintainer Discord/blog posts from 2026).
