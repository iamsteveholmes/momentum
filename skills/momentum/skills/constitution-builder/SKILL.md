---
name: constitution-builder
description: "Builds or regenerates the hot constitution (## Permissions + ## Standing Rules + ## Quick Routing) for any KB-backed agent skill. Covers what the agent owns, what it can't touch, always-on behavioral constraints, and symptom→wiki-query routing. Use when: creating a new KB-backed skill, the wiki KB has grown and routing entries are stale, or you hear 'build constitution', 'generate routing table', 'update quick routing', 'add routing to this skill', 'add standing rules', 'define agent permissions', or 'momentum:constitution-builder'. Also invoke proactively after wiki-ingest adds a major new technology area to the KB."
model: claude-opus-4-6
effort: medium
---

# momentum:constitution-builder

Builds the hot constitution for KB-backed agent skills — three always-loaded sections that together define what an agent can touch, how it must behave, and where to look things up.

## Architecture

Three tiers:
- **Cold KB** — full wiki vault (vault path from `~/.obsidian-wiki/config`). Not in context. Everything.
- **Hot Constitution** — `## Permissions` + `## Standing Rules` + `## Quick Routing` in SKILL.md. Always loaded.
- **Hot Selective** — wiki pages pulled into context when a symptom fires.

**Three distinct jobs:**

| Section | Purpose | Enforced by |
|---|---|---|
| `## Permissions` | What the agent owns, what it cannot touch | Claude Code harness (path patterns + tool restrictions) |
| `## Standing Rules` | Always-on behavioral constraints | Agent judgment, informed by this section |
| `## Quick Routing` | Symptom → `wiki-query` fast path to cold KB | Agent judgment, informed by routing table |

Never collapse these. Permissions are enforced by the harness. Rules are honored by the agent. Routing is consulted by the agent.

## Permission Pattern Syntax

Claude Code's permission system supports path-pattern restrictions on file tools:

```json
"allow": ["Edit(/src/**)", "Write(/src/**)"]      // owns these paths
"deny":  ["Edit(/docs/**)", "Read(./.env)"]        // cannot touch these
"allow": ["Bash(./gradlew *)", "Bash(git *)"]      // bash allowlist
"deny":  ["Bash(git push *)", "Bash(rm -rf *)"]    // bash blocklist
```

- `/path` — relative to project root
- `//path` — absolute filesystem path
- `~/path` — home directory
- `*` — one directory level; `**` — recursive

Permissions restrict downward only — a subagent cannot have more access than its parent session.

## Routing Entry Format (DEC-018)

```
**[developer symptom or trigger scenario]** → `wiki-query [specific question]`
**[symptom]** → `wiki-query quick answer: [question]`  ← for fast index-only lookups
```

Never write "consult KB if needed." Name the exact moment and exact query string.

---

## Workflow

### Phase 1 — Elicit

Ask the developer:
1. What skill are we building the constitution for? (name, or path to SKILL.md)
2. What is this agent's role in the development cycle? (e.g., sprint planner, dev, retro, research, analyst)
3. What technologies and domains does this skill cover?
4. What problems does a developer bring to this skill? Describe 3–5 typical scenarios.
5. What non-negotiable practices apply? (TDD discipline, architecture patterns, code style invariants)

Store: `{{target_skill_path}}`, `{{agent_role}}`, `{{technologies}}`, `{{typical_scenarios}}`, `{{practices}}`

Check if any constitution sections already exist in the target SKILL.md. Offer to regenerate, replace, or merge each independently.

### Phase 2 — Permission Scoping

This is the most important phase for multi-agent systems. The goal is to define hard boundaries: what this agent owns and what it has no business touching.

Ask the developer these questions in order:

**A. What does this agent own?** (generates write allowlist)
- "What files or directories is this agent responsible for creating or modifying as part of its job?"
- Examples: source files, sprint indexes, story files, KB research pages, planning artifacts
- For each answer, derive the path pattern: `Edit(/path/**)` or `Write(/path/**)`

**B. What should it never write to?** (generates write denylist)
- "What files or directories should this agent never modify, even if it thinks it needs to?"
- Think about: other agents' domains, config files, secrets, shared indexes it doesn't own
- For each answer, derive: `Edit(/path/**)` or `Write(/path/**)`

**C. What should it never read?** (generates read denylist)
- "Is there anything this agent has no business knowing? Secrets, other projects, business docs it doesn't need?"
- For each answer, derive: `Read(/path/**)` or `Read(./.env)`

**D. What bash commands does it need?** (generates bash allowlist)
- "What shell operations are legitimate for this agent's job?" (build, test, git, search)
- Be specific: `Bash(./gradlew *)` not just "gradle stuff"

**E. What bash commands should it never run?** (generates bash denylist)
- "What's off-limits?" (destructive ops, network calls, deployments, force pushes)
- Be specific: `Bash(git push --force *)`, `Bash(rm -rf *)`

Generate the permission block:

```markdown
## Permissions

### Owns — may read and write
- [path description] → `Edit(/path/**)`, `Write(/path/**)`

### Off-limits — may not write
- [path description] → denied write

### Off-limits — may not read
- [path description] → denied read

### Bash allowlist
- [command] — [why it needs this]

### Bash denylist
- [command] — [why it's blocked]

### settings.json snippet
\`\`\`json
{
  "permissions": {
    "allow": [
      "Edit(/path/**)",
      "Bash(git *)"
    ],
    "deny": [
      "Edit(/other/**)",
      "Read(./.env)",
      "Bash(git push *)"
    ]
  }
}
\`\`\`
```

Present to the developer. Ask: anything missing? Any path patterns that seem too broad or too narrow?

### Phase 3 — Generate Standing Rules

Standing Rules are behavioral constraints — things the agent must always do or never do, without a KB lookup.

**A. KB principle pages** — query for any synthesis or principle pages on the declared practices:
- `wiki-query [practice] principles`
- Extract non-negotiable constraints (never/always rules, sequencing, decision criteria)
- Distill directly into rules — do NOT route to these pages

**B. Developer elicitation** — for project-specific conventions:
- "What should this agent always do when [scenario]?"
- "Any hard rules about ordering, naming, or tooling?"

Rules must be:
- **Actionable** — specific enough to follow without judgment
- **Unconditional** — if it has exceptions, it's a guideline, not a rule
- **Not redundant with routing** — if it needs a KB lookup to apply, it belongs in Quick Routing

Present draft. Ask: anything missing, wrong, or too rigid?

### Phase 4 — Audit the KB

1. `cat ~/.obsidian-wiki/config` — extract `OBSIDIAN_VAULT_PATH`
2. Read `{vault_path}/index.md`
3. For each technology/domain from Phase 1, scan for relevant entries

Present three-category audit:
```
Covered (will generate routing entries): [concept — description]
Partial (entries will be thin): [concept — what's there]
Gaps (no routing possible): [technology]
```

### Phase 5 — Fill Gaps (optional)

For each gap or partial: "Would you like to ingest documentation now? I can invoke wiki-research or wiki-ingest."

If yes: invoke the skill, then re-read the index before continuing.

### Phase 6 — Generate Routing Entries

For each **covered** concept:
1. `wiki-query [concept]` — retrieve relevant pages
2. Read returned pages — understand what problems they answer
3. Write 2–4 entries per concept:
   - **Symptom**: what the agent or developer would say, observe, or ask — specific and observable
   - **Query**: exact wiki-query invocation

Group into thematic subsections. Avoid routing to anything already covered by Standing Rules.

**Strong symptom phrasing:** specific, observable, diagnostic, scenario-based.
**Weak phrasing to avoid:** "general questions about X", "use when you need help with X".

### Phase 7 — Review

Present all three sections together.

For Permissions: are the path patterns right? Too broad, too narrow? Anything missing?
For Standing Rules: anything missing, wrong, or too rigid?
For Quick Routing: missing symptoms? Wrong query strings? Anything to cut?

Incorporate feedback. Target: complete permission coverage, 3–8 standing rule groups, 15–40 routing entries.

### Phase 8 — Write

Write all three sections into `{{target_skill_path}}`.

**Order in SKILL.md:** Permissions first, then Standing Rules, then Quick Routing. All go after the skill's opening description.

```markdown
## Permissions

### Owns — may read and write
- ...

### Off-limits — may not write
- ...

### settings.json snippet
\`\`\`json
{ "permissions": { "allow": [...], "deny": [...] } }
\`\`\`

---

## Standing Rules

### [Practice]
- [constraint]

---

## Quick Routing

Use this table first. Match your situation to a scenario and run the wiki-query before answering.

### [Thematic Group]
- **[symptom]** → `wiki-query [question]`
```

Write behavior:
- No existing sections: insert all three after the opening description
- Partial: show existing, confirm replacement per section, then write

Report: "Constitution written — permissions defined, N standing rules across M groups, P routing entries across Q subsections."
