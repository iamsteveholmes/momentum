# Consultation Log

- Skill: `frontend-dev` — invoked first because the question is nornspun-client (Compose Multiplatform) Kotest + Turbine + StateFlow testing, which is squarely in the skill's domain. The skill's Quick Routing table named the exact scenario ("Flow emissions not arriving — `awaitItem` times out") and pointed at a wiki-query.
- Skill: `wiki-query` — followed the routing pointer to retrieve the canonical answer from the compiled wiki: `wiki-query Turbine awaitItem awaitComplete testIn turbineScope StateFlow timeout`.
- Tool: `Bash` (`cat ~/.obsidian-wiki/config`) — to resolve `OBSIDIAN_VAULT_PATH`.
- Tool: `Bash` (`ls` + `test -f hot.md`) — to confirm vault layout and hot.md presence.
- Tool: `Bash` (`grep -rli "turbine" ...`) — index pass to locate Turbine-related pages.
- Tool: `Read` — full read of `concepts/ViewModel StateFlow Testing Patterns.md` (top candidate, exact topic match).
- Tool: `Bash` (`grep -n -A 8 ...`) — section pass on `concepts/MVI ViewModel Testing with Turbine and Kotest.md` for `awaitItem` / `coroutineTestScope` snippets.
- Tool: `Write` — saved `answer.md` to the outputs directory.
- Tool: `Write` — saved `consultation_log.md` (this file).

## Reasoning

The developer's question was a textbook fit for the `frontend-dev` skill (nornspun-client, Kotest, Turbine, MVI ViewModel). That skill is explicit about routing test-flow questions through `wiki-query` against the project's Obsidian wiki, so I followed the routing exactly rather than answering from general training knowledge — the wiki has project-specific guidance (dispatcher rule for Kotest, BehaviorSpec gotcha, conflation behavior under `StandardTestDispatcher`) that is more reliable than generic advice. I deliberately did not invoke `compose-expert` (this is a coroutines/test problem, not a Compose UI problem), `bmad-*` skills (no workflow-grade artifact to author), `chrome-devtools-mcp` / `maestro` / `claude-in-chrome` (not a UI-runtime problem), or `momentum:*` skills (not a practice/workflow change). I used the cheapest retrieval primitive that answered the question — index grep for Turbine pages, then one full read of the most on-target concept page, plus a targeted `grep -A 8` section pass on the second page for code snippets — never escalating to a broad content grep.
