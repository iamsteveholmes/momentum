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
- **Tier 1 — Hot Constitution** — `## Permissions` + `## Standing Rules` + `## Quick Routing` in SKILL.md. Project-wide, shared by every agent, always loaded.
- **Tier 2 — Composed Agent File** — per-agent system prompt assembled from `base_body` + constitution + manifesto. Built at agent-spawn time.
- **Tier 3 — Cold KB** — full wiki vault (vault path from `~/.obsidian-wiki/config`). Not in context. Accessed on-demand via `wiki-query`.

The **runtime retrieval pattern** — symptom fires → `wiki-query` pull-in from Tier 3 — is a usage pattern, not a tier.

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

---

## Constitution.md (Tier 1) — Acceptance Criteria

> **Purpose:** This section is the quality bar for the `constitution.md` (Tier 1) artifact
> produced by the agent-composition pipeline. The generator (`momentum:constitution-builder`)
> and any post-generation AVFL gate use these criteria to determine whether a generated
> constitution is correct and complete. Verification method: **document-review** (inspection
> against the generated artifact and its cited sources — no automated driver).
>
> **Story:** `constitutionmd-generation-acceptance-criteria`
> **Authoritative decisions:** DEC-038, DEC-026 D3/D4/D5, DEC-015 D3, DEC-018, DEC-001/DEC-008 D1

---

### AC-1 — File Format: Location, Section Headings, and Section Order

**Stated contract for constitution.md:**

| Property | Value |
|---|---|
| Canonical path | `.claude/guidelines/constitution.md` |
| Write mode | `standalone_constitution` (see `write_mode` parameter) |
| Encoding | UTF-8, markdown |

**Required sections (in order):**

1. `## Project Identity` — Who this project is; the stack, mission, and team context that every agent needs to orient on.
2. `## Core Values` — The non-negotiable principles that govern all agent behavior on this project (e.g., "never commit secrets", "always use conventional commits").
3. `## Constraints` — Hard limits that apply to every agent without exception: architectural boundaries, forbidden operations, compliance rules.
4. `## Glossary` — Project-specific terms, acronyms, and role names that agents must know to parse developer requests without a KB lookup.
5. `## Cross-Cutting Standing Rules` — Always-on behavioral rules that span every role and every task. Rules specific to a single agent role do NOT belong here.
6. `## Cross-Cutting Permissions` — Path-pattern allow/deny grants that apply to ALL agents on the project. Agent-specific permissions are NOT here.
7. `## Wiki-Query Interface` — The DEC-018 `wiki-query` cold-KB access block: how agents invoke `wiki-query`, when to use it, and the shared multi-KB scope (per DEC-038).

**Sections the shared constitution MUST NOT contain:**

- Any per-agent `## Quick Routing` section (see AC-8 and AC-9).
- Any role-specific symptom→`wiki-query` diagnostic table.
- Agent-specific `## Permissions` or `## Standing Rules` blocks.

**Verification:** A reviewer confirms every required section is present (no missing section) and that each section contains only the content its purpose describes (no section repurposed — e.g., no routing table inside `## Glossary`).

---

### AC-2 — Section Purpose and Expected-Content Statements

Each required section has an explicit purpose and expected-content contract (the table in AC-1 expresses this). A reviewer uses these to verify:

- **Completeness:** all seven required sections are present in the generated constitution.
- **Well-formedness:** no section is repurposed (e.g., routing entries do not appear in `## Core Values`).

The one-line purpose for each section:

| Section | Purpose (one line) | Expected content |
|---|---|---|
| `## Project Identity` | Orient every agent on what project it is working in | Stack, mission, team role map — no routing, no rules |
| `## Core Values` | Non-negotiable principles for all agents | Short, unconditional value statements |
| `## Constraints` | Hard limits applying to every agent | Forbidden paths, operations, compliance items |
| `## Glossary` | Shared vocabulary so agents parse developer language correctly | Term → definition pairs; no rules or routing |
| `## Cross-Cutting Standing Rules` | Always-on behavioral rules for every role | Actionable, unconditional, non-role-specific rules |
| `## Cross-Cutting Permissions` | Harness-enforced path grants for all agents | `allow`/`deny` path patterns; no role-specific entries |
| `## Wiki-Query Interface` | Shared cold-KB access infrastructure (DEC-018, DEC-038) | Interface spec, invocation syntax, multi-KB scope |

---

### AC-3 — Line-Count Budget

**Budget:**

| Metric | Value |
|---|---|
| Target | ~660 lines |
| Upper bound | 750 lines (hard ceiling — a generated constitution exceeding this value fails this AC) |
| Rationale | The decision-document model: a document that must be read and understood in full should fit within the same cognitive budget as a project decision document (~660 lines). A longer constitution becomes a context liability rather than a hot asset. |

**Measurement:** Line count is measured on the final written file at the canonical path `.claude/guidelines/constitution.md` (blank lines and comment lines included).

---

### AC-4 — Budget Overflow Resolution

**On overflow (line count exceeds 750):**

1. **Do NOT delete content.** An over-budget constitution that deleted content to comply has lost value.
2. **Move detail into `references/`.** Any elaboration, examples, edge-case explanations, or extended reasoning are relocated to a file under `skills/momentum/references/` with a descriptive name (e.g., `references/constitution-constraints-detail.md`).
3. **Add a load pointer in the constitution.** Where the detail was moved, replace it with a single line:
   ```
   > Load detail: `skills/momentum/references/<filename>.md`
   ```
4. **Re-measure.** After moving detail, the constitution must fall within the 750-line ceiling.

**Named enforcement owner:** The post-generation check in `build-guidelines` orchestration (story `build-guidelines-skill`) is the owner that flags an over-budget constitution at generation time. Until `build-guidelines` exists, the enforcer is the AVFL gate in `citation-integrity-validation-in-build-guidelines-avfl`. Constitution-builder itself may also self-check at Phase 8 (Write) and warn the developer before writing.

---

### AC-5 — Critical-Only Content Rule

**Rule:** The constitution carries **critical, always-loaded rules only.** A rule is critical if and only if it meets the following test:

> **Critical test:** "Would an agent that lacked this rule make a materially wrong decision or a harmful action on the very first task, before any KB lookup, across every possible role on this project?"

If the answer is **yes** → the rule belongs in the hot constitution.
If the answer is **no** (the rule applies only sometimes, or only in specific contexts an agent could look up) → the rule belongs in `references/` with a load pointer or in the per-agent manifesto.

**Examples:**

| Content | Critical? | Disposition |
|---|---|---|
| "Never commit secrets to version control" | Yes — universal, immediate, harmful if violated | Hot constitution |
| "Use conventional commits format" | Yes — universal, applies to every commit | Hot constitution |
| "When classifying domain, query the KB" | No — context-specific trigger | `## Wiki-Query Interface` trigger |
| "Kotest test naming conventions" | No — domain-specific, frontend agents only | Per-agent manifesto / `references/` |
| "Run gradlew test before merging" | Borderline — check if universal | Include only if every agent on the project runs tests |

**Reviewer adjudication:** When a borderline case exists, the reviewer applies the critical test literally. If the answer is not clearly "yes, across every role", the content moves to `references/` or the per-agent manifesto.

---

### AC-6 — Prescriptive KB-Trigger Language (DEC-015 D3)

**Rule:** The constitution's KB-trigger language is **prescriptive**, not permissive.

**Forbidden phrasing (permissive):**
- "If you need domain knowledge, check the KB."
- "Consult the wiki when unsure about X."
- "The KB may have useful information about Y."
- Any phrasing that makes the KB lookup optional or judgment-based.

**Required phrasing (prescriptive):** Each KB trigger must:
1. Name the **exact scenario** that compels the lookup (not a vague topic).
2. Include the **exact `wiki-query` invocation** (no free-form phrasing).
3. Leave **no judgment call** to the agent about whether to look up.

**Correct trigger examples:**
```
When classifying a story's change_type before sprint planning → `wiki-query change_type classification rules`
When selecting a test pattern for a library the project hasn't used before → `wiki-query test patterns [library name]`
When an architectural constraint is referenced but not defined in the constitution → `wiki-query architectural constraints [constraint name]`
```

**Verification:** A reviewer reads every KB-trigger statement in the generated constitution. Any permissive or optional-phrased trigger is a failure of this AC. Every trigger must name a concrete scenario and an exact query string.

**Authority:** DEC-015 D3 — prescriptive named-scenario triggers only. Rationale: LLMs default to training data; vague permission is effectively no instruction.

---

### AC-7 — Citation Integrity

**Rule:** Every rule, constraint, value, or claim in the generated constitution is **traceable** to one of:
- A `wiki-query`-resolvable KB page (the agent can retrieve it via `wiki-query <topic>`), OR
- A named project decision (`DEC-NNN`)

**Traceability requirement:** The constitution document itself, or its accompanying generation record, must note the source for each non-obvious rule. Obvious universal rules (e.g., "never commit passwords") do not require individual citations; project-specific or architecture-derived rules do.

**Verification procedure (per-rule check):**

For each rule or claim in the generated constitution:
1. Identify the asserted source (wiki KB page slug or `DEC-NNN`).
2. Attempt to resolve it: run `wiki-query <topic>` and confirm a page is returned, OR confirm the named DEC file exists at `_bmad-output/planning-artifacts/decisions/dec-NNN-*.md`.
3. If no resolvable source exists → **citation-integrity failure** for that rule.

**Failure condition:** An uncited rule (a rule with no traceable source that is not a universally obvious practice) is a citation-integrity AC failure.

**Enforcement owner:** The AVFL gate in `citation-integrity-validation-in-build-guidelines-avfl` (story `citation-integrity-validation-in-build-guidelines-avfl`) is the named owner of automating this check at generation time. Until that gate exists, citation integrity is verified by the document-review pass.

**Authority:** DEC-018 (wiki-query as Tier 3 cold-KB interface, extended by DEC-038 to multiple per-project KBs).

---

### AC-8 — DEC-038 Routing-Ownership Boundary (No Per-Agent Routing in Shared Constitution)

**Rule:** The shared constitution (`constitution.md`) contains **no per-agent diagnostic-table or routing content.**

**What is prohibited:**
- Any `## Quick Routing` section in `constitution.md`.
- Any symptom→`wiki-query` routing table scoped to a specific agent role (e.g., a Compose/Kotest routing table that only applies to a frontend agent).
- Any per-role, per-domain routing entries, regardless of section name.

**Why:** Per DEC-038, per-agent routing is the *manifesto* — a stable, per-role×domain diagnostic table owned at the `agent-builder` layer. A project-shared routing table is meaningless for most agents on the project (a Compose routing table means nothing to a `pm` or `architect`). The shared constitution is for genuinely project-universal content only.

**Verification:** Inspect the generated `constitution.md`. The presence of any per-agent or role-specific routing table (symptom → `wiki-query` entries scoped to a role or domain) is a failure of this AC.

**Authority:** DEC-038 (Manifesto as Per-Agent Diagnostic Table + Per-Project Multi-KB). Architecture Decision 56, "Routing ownership — per-agent, not shared constitution (DEC-038)" block.

---

### AC-9 — Quick Routing Reconciliation and Committed Architecture Option

**Committed reconciliation choice:** This story and its sibling `constitution-builder-write-mode-parameterization` commit to the same routing-ownership resolution. The sibling story's ACs (specifically AC 7: "The constitution output contains no `## Quick Routing` section — routing tables are not generated by constitution-builder under any write mode") make the stance explicit.

**Resolution recorded here:** `constitution-builder` emits **no `## Quick Routing` content** in the shared constitution under any write mode. All routing-table / diagnostic-table generation is delegated entirely to `momentum:agent-builder` (the manifesto/Tier 2 layer), per DEC-038 and DEC-026 D4.

**Alignment with architecture.md ~line 3061 ("Routing ownership — per-agent, not shared constitution (DEC-038)"):**
This resolution directly implements the DEC-038 Phase 1 ratification recorded there: "symptom→`wiki-query` routing belongs in the **per-agent manifesto (diagnostic table)**, not the shared constitution. `constitution-builder` emits **no `## Quick Routing`** section under any write mode — routing generation is removed from constitution-builder and owned by the manifesto / `agent-builder` layer." The architecture block names this story (`constitutionmd-generation-acceptance-criteria`) as a co-owner of that ratification alongside the sibling story. The shared constitution may still carry project-universal, agent-agnostic content and the wiki-query interface block; it carries no per-agent routing.

**FR136 reconciliation:** PRD FR136 (Gen-2 Agent Composition Model) already carries a DEC-038 in-line annotation (see `_bmad-output/planning-artifacts/prd.md` at FR136) stating that "per DEC-038 the constitution carries **no per-agent quick-routing table** — per-agent symptom→`wiki-query` routing lives in the manifesto." This story's AC-9 is fully consistent with FR136 as annotated: the constitution carries domain knowledge and the wiki-query interface block only; the diagnostic routing table belongs in the per-agent manifesto. No further amendment to prd.md FR136 is required — the DEC-038 annotation already reflects the superseded reading.

**Sibling consistency verification:** The sibling story `constitution-builder-write-mode-parameterization` AC 7 states "The constitution output contains no `## Quick Routing` section — routing tables are not generated by constitution-builder under any write mode." This story's AC-9 is consistent with that stance — both stories commit to zero routing output from the constitution layer.

**Verification:** Confirm the generated `constitution.md` contains no `## Quick Routing` section and no symptom→`wiki-query` routing table, consistent with the sibling story's AC 7.

---

### AC-10 — Enforcement Hook

**The following post-generation checks own enforcement of the criteria above at generation time:**

| ACs Enforced | Enforcement Owner | Location | Status |
|---|---|---|---|
| AC-3 (line count target), AC-4 (upper bound + overflow) | Post-generation line-count check | `build-guidelines` orchestration (story `build-guidelines-skill`) / constitution-builder Phase 8 self-check | `build-guidelines` forthcoming; self-check in Phase 8 interim |
| AC-7 (citation integrity) | AVFL citation gate | `citation-integrity-validation-in-build-guidelines-avfl` (story of same name) | Forthcoming |
| AC-8 (no per-agent routing) | Post-generation routing-absence check | `build-guidelines` orchestration and/or constitution-builder Phase 8 self-check | `build-guidelines` forthcoming; constitution-builder self-check interim |
| AC-9 (Quick Routing reconciliation) | Same as AC-8 | Same as AC-8 | Same as AC-8 |

**Interim enforcement (until `build-guidelines` and the citation gate exist):** The document-review pass at story verification time enforces all ACs by inspection. Constitution-builder's Phase 8 (Write) should self-check line count and routing-absence before writing, warning the developer of violations.

**Integration note:** These ACs are the verification target for the `citation-integrity-validation-in-build-guidelines-avfl` story's AVFL gate and the `build-guidelines-skill` story's orchestration layer. When those stories are implemented, their implementation MUST reference this AC document and enforce ACs 3, 4, 7, 8, and 9 as stated here.

---

### Cross-References

All identifiers used in this AC document and their resolution paths:

| Identifier | Resolution path |
|---|---|
| DEC-038 | `_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md` |
| DEC-026 D3/D4/D5 | `_bmad-output/planning-artifacts/decisions/` (DEC-026 file) |
| DEC-015 D3 | `_bmad-output/planning-artifacts/decisions/` (DEC-015 file) |
| DEC-018 | `_bmad-output/planning-artifacts/decisions/` (DEC-018 file) |
| DEC-001 / DEC-008 D1 | `_bmad-output/planning-artifacts/decisions/` |
| FR136 | `_bmad-output/planning-artifacts/prd.md` — FR136 (Gen-2 Agent Composition Model) |
| FR142 | `_bmad-output/planning-artifacts/prd.md` — FR142 (per-project multi-KB) |
| Architecture Decision 56 | `_bmad-output/planning-artifacts/architecture.md` (~line 3061, "Routing ownership" block) |
| Sibling story | `.momentum/stories/constitution-builder-write-mode-parameterization.md` |
| Citation gate story | `.momentum/stories/citation-integrity-validation-in-build-guidelines-avfl.md` |
| Build-guidelines story | `.momentum/stories/build-guidelines-skill.md` |
| wiki-query interface story | `.momentum/stories/wiki-query-interface-block-for-hot-constitution.md` |
| `constitution-builder/SKILL.md` | `skills/momentum/skills/constitution-builder/SKILL.md` |
| `build-guidelines/SKILL.md` | `skills/momentum/skills/build-guidelines/SKILL.md` (forthcoming — story `build-guidelines-skill`) |
