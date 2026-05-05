---
name: constitution-builder
description: "Builds or regenerates the hot constitution (## Standing Rules + ## Quick Routing) for any KB-backed agent skill. Standing Rules encode always-on behavioral constraints; Quick Routing maps developer symptoms to exact wiki-query invocations. Use when: creating a new KB-backed skill, the wiki KB has grown and routing entries are stale, or you hear 'build constitution', 'generate routing table', 'update quick routing', 'add routing to this skill', 'add standing rules', or 'momentum:constitution-builder'. Also invoke proactively after wiki-ingest adds a major new technology area to the KB."
model: claude-opus-4-6
effort: medium
---

# momentum:constitution-builder

Builds the hot constitution for KB-backed agent skills — two always-loaded sections that together define how the skill behaves without reading anything from the cold KB.

## Architecture

Three tiers:
- **Cold KB** — full wiki vault (vault path from `~/.obsidian-wiki/config`). Not in context. Everything.
- **Hot Constitution** — `## Standing Rules` + `## Quick Routing` in SKILL.md. Always loaded. Rules and routing.
- **Hot Selective** — wiki pages pulled into context when a symptom fires.

**Two distinct jobs:**

| Section | Purpose | Source |
|---|---|---|
| `## Standing Rules` | Always-on behavioral constraints the agent must follow without looking anything up | Developer practices + KB principle pages |
| `## Quick Routing` | Symptom → `wiki-query` — fast path to cold KB content | Derived from cold KB index |

Never collapse these. A TDD rule ("write the test first") is a constraint, not a reference. A Kotest assertion syntax question is a reference, not a constraint.

## Routing Entry Format (DEC-018)

Entries must be prescriptive named scenarios — exact invocations, not advisory language:

```
**[developer symptom or trigger scenario]** → `wiki-query [specific question]`
```

For fast index-only lookups (definitions, API lookups, quick facts):
```
**[symptom]** → `wiki-query quick answer: [question]`
```

Never write "consult KB if needed." Name the exact moment and exact query string.

---

## Workflow

### Phase 1 — Elicit

Ask the developer:
1. What skill are we building the constitution for? (name, or path to SKILL.md)
2. What technologies and domains does this skill cover?
3. What problems does a developer bring to this skill? Describe 3–5 typical scenarios.
4. What non-negotiable practices apply? (e.g., TDD discipline, architecture patterns, code style invariants, specific library conventions)

Store: `{{target_skill_path}}`, `{{technologies}}`, `{{typical_scenarios}}`, `{{practices}}`

Check if `## Standing Rules` or `## Quick Routing` already exist in the target SKILL.md. If either does, note it — offer to regenerate, replace, or merge each section independently.

### Phase 2 — Generate Standing Rules

Standing Rules are hard-coded behavioral constraints — things the agent must always do or never do, without a KB lookup. They come from two sources:

**A. KB principle pages** — if the developer listed practices (e.g., TDD, a specific architecture), query the KB for any synthesis or principle pages on those practices:
- `wiki-query [practice] principles` — retrieve the relevant pages
- Extract the non-negotiable constraints (never/always rules, sequencing requirements, decision criteria)
- Do NOT route to these pages — distill the rules directly into the section

**B. Developer elicitation** — for practices not in the KB, or where the developer has project-specific conventions that override general guidance, ask:
- "What should the agent always do when [scenario from Phase 1]?"
- "Are there any hard rules about ordering, naming, patterns, or tooling in this codebase?"

Format as grouped rules under named subsections:

```markdown
## Standing Rules

### [Practice Name, e.g., Test-Driven Development]
- [Constraint phrased as always/never/must/before]
- ...

### [Architecture Pattern, e.g., MVI]
- ...
```

Rules should be:
- **Actionable** — specific enough that the agent can follow without judgment
- **Unconditional** — if it has exceptions, it's a guideline, not a rule
- **Not redundant with routing** — if it needs a KB lookup to apply, it belongs in Quick Routing, not here

Present the draft Standing Rules to the developer. Ask: anything missing, wrong, or too rigid?

### Phase 3 — Audit the KB

Read the wiki KB index:

1. Get vault path: `cat ~/.obsidian-wiki/config` — extract `OBSIDIAN_VAULT_PATH`
2. Read `{vault_path}/index.md`
3. For each technology/domain from Phase 1, scan the index for relevant entries

Present a three-category audit:

```
Covered (will generate routing entries):
  - [concept] — [index description]

Partial (entries will be thin — consider ingesting more):
  - [concept] — [what's there]

Gaps (no routing entries possible without more KB content):
  - [technology]
```

The audit grounds the next step — don't generate routing entries for concepts with no KB backing.

### Phase 4 — Fill Gaps (optional)

For each gap or partial concept, ask: "Would you like to ingest documentation for [technology] now? I can invoke wiki-research or wiki-ingest."

If yes: invoke the appropriate wiki skill. After ingest, re-read the index for newly added concepts before continuing.

If no: note the gap — routing coverage will be limited for that domain.

### Phase 5 — Generate Routing Entries

For each **covered** concept:

1. Retrieve the relevant wiki pages: `wiki-query [concept]`
2. Read the returned pages — understand what problems they answer, what errors they address, what decisions they inform
3. Write 2–4 routing entries per concept:
   - **Symptom**: what a developer would say, observe, or ask — specific and observable
   - **Query**: the exact wiki-query invocation that retrieves the right pages

Group entries into thematic subsections (e.g., `### Validation`, `### Testing`, `### State Management`).

**Strong symptom phrasing:**
- "coroutine test won't advance virtual time" — specific, observable
- "StateFlow not updating UI after emit" — diagnostic
- "how to wire Ktor request into a use case" — scenario-based

**Weak phrasing to avoid:**
- "general Kotest questions" — not a symptom
- "use when you need help with X" — not prescriptive

**Avoid routing to principles already in Standing Rules.** If TDD red-green-refactor is a standing rule, don't add a routing entry for "how does TDD work" — that's already answered. Route only to implementation details the standing rule doesn't cover.

### Phase 6 — Review

Present both sections together. For Standing Rules, ask:
- Any rules missing?
- Any that are too rigid or have valid exceptions we should handle differently?

For Quick Routing, ask:
- Any symptoms missing?
- Do the query strings match what you'd actually search?
- Anything to cut?

Incorporate feedback. Target 3–8 standing rule groups, 15–40 routing entries.

### Phase 7 — Write

Format and write both sections into `{{target_skill_path}}`.

**Order in SKILL.md:** Standing Rules before Quick Routing. Both go after the skill's opening description.

```markdown
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
- If neither section exists: insert both after the opening description
- If one or both exist: show existing, confirm replacement per section, then write

Report: "Constitution written — N standing rules across M groups, P routing entries across Q subsections."
