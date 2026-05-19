# momentum:agent-builder Workflow

**Goal:** Compose one Tier 2 agent file from a base body + constitution excerpt + manifesto inputs, and register a routing entry in `momentum/agents.json`.

**Role:** Per-agent composer in the Momentum build pipeline. Runs once per role × domain pair. Orchestrated by sprint-dev or invoked directly via momentum:agent-builder.

**Pipeline position:**
```
constitution-builder (Tier 1, once per project)
  → agent-builder × N (Tier 2, once per role × domain)
    → momentum/agents.json (routing table, updated by this skill)
```

---

## INPUTS

The skill accepts these inputs (via invocation arguments or interactive elicitation):

| Input | Description | Example |
|---|---|---|
| `base_body_path` | Path to the base body agent file in the plugin | `skills/momentum/agents/dev.md` |
| `role` | The agent's role slug (BMAD-aligned) | `dev`, `architect`, `qa`, `researcher` |
| `domain` | The domain this agent specializes in (stack or concern) | `cmp`, `android`, `backend`, `research` |
| `constitution_path` | Path to the project constitution | `momentum/architecture/constitution.md` |
| `manifesto_context` | Free-text domain knowledge block for this agent | Compose patterns, API ownership, conventions |
| `permissions_scope` | List of file patterns this agent owns and may write | `["src/**/ui/**", "**/*.kt"]` |
| `output_dir` | Directory for composed agent file | `.claude/guidelines/agents/` (default) |

---

## EXECUTION

<workflow>
  <critical>The composed agent file is NOT a workflow — it is a system prompt with role statement, constraints, process, and output format. Follow agent definition conventions from the dev guide.</critical>
  <critical>Every composed agent file MUST include a ## Large File Handling section per the agent-skill-development-guide.md standard.</critical>
  <critical>Write the routing entry to momentum/agents.json — never skip this step. The routing table is how skills discover this agent.</critical>
  <critical>Use skill-creator to validate the composed agent file before writing. Do not bypass this quality gate.</critical>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 1: ELICIT                                         -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="1" goal="Collect and validate inputs">
    <action>Check invocation arguments for the required inputs: base_body_path, role, domain, constitution_path, manifesto_context, permissions_scope.</action>

    <check if="any required input is missing">
      <action>Elicit missing inputs interactively. Ask one question at a time.</action>
      <ask>Which base body should this agent extend? (e.g., skills/momentum/agents/dev.md)</ask>
      <ask>What role slug? (BMAD-aligned: dev, architect, qa, ux, analyst, researcher, sm, e2e)</ask>
      <ask>What domain does this agent specialize in? (e.g., cmp, android, backend, frontend, research)</ask>
      <ask>Path to project constitution? (default: momentum/architecture/constitution.md)</ask>
      <ask>Describe this agent's domain specialization — what it owns, what patterns apply, what conventions it must follow.</ask>
      <ask>What file patterns does this agent own and may write? (e.g., src/**/ui/**, **/*.kt)</ask>
    </check>

    <action>Set computed values:
      - {{agent_slug}} = "{{role}}-{{domain}}" (e.g., "dev-cmp")
      - {{output_path}} = "{{output_dir}}/{{agent_slug}}.md" (e.g., ".claude/guidelines/agents/dev-cmp.md")
      - {{output_dir}} defaults to ".claude/guidelines/agents/" if not provided
    </action>

    <action>Read the base body file at {{base_body_path}} — capture its system prompt body (strip frontmatter).</action>
    <action>Store as {{base_body_content}}</action>

    <check if="constitution_path exists">
      <action>Read {{constitution_path}}. Extract the sections relevant to this agent's role and domain — do not include the full constitution, only what's relevant.</action>
      <action>Store as {{constitution_excerpt}}</action>
    </check>
    <check if="constitution_path does not exist">
      <action>Note absence. Proceed without constitution excerpt. Log: "No constitution found at {{constitution_path}} — composed file will use base body + manifesto only."</action>
      <action>Set {{constitution_excerpt}} = ""</action>
    </check>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 2: COMPOSE                                        -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="2" goal="Draft composed agent file">
    <action>Read the agent-skill-development-guide.md for agent definition conventions:
      - File: skills/momentum/references/agent-skill-development-guide.md
    </action>

    <action>Draft the composed agent file using this template:

```markdown
---
name: {{agent_slug}}
description: {{role_description}} — specialized for {{domain}} domain. Spawned by sprint-dev for {{domain}}-related work.
model: sonnet
effort: medium
tools: [Read, Grep, Glob, Bash, Edit, Write]
---

{{base_body_content}}

## Domain Specialization: {{domain}}

{{manifesto_context}}

{{constitution_excerpt}}

## Large File Handling

Some project files exceed the Read tool's token limit (10,000 tokens). When you
encounter a file-too-large error or need to read a file known to be large, use
these strategies:

1. **Search before reading** — Use Grep to find the specific section, heading, or
   keyword you need. Note the line number from Grep output, then Read with offset
   and limit targeting that area.
2. **Read in chunks** — Use `offset` and `limit` parameters: `offset=0, limit=200`
   for the first 200 lines, then adjust as needed.
3. **Known large files** — These commonly exceed limits: architecture.md, prd.md,
   epics.md, stories/index.json, and JSONL audit extracts. Never attempt a full
   read of these files.
4. **On error, narrow scope** — If a Read fails with a token-limit error, do not
   retry the same read. Instead, Grep for what you need and read only that section.

[inject base body ## Output Format section here — per Rule 4, strip from {{base_body_content}} and re-append after Large File Handling]
```
</action>

    <action>Apply the following composition rules:
      1. Base body content is injected verbatim — do not paraphrase or abbreviate
      2. Domain Specialization section describes: what this agent owns, what conventions apply, what it must always/never do in this domain
      3. Constitution excerpt is trimmed to only include knowledge relevant to this role × domain — do not paste the full constitution
      4. Large File Handling section is always present. When composing, place it immediately BEFORE the base body's `## Output Format` section. If the base body's Output Format appears at the end of `{{base_body_content}}`, strip it from the injected content and re-append it AFTER the Large File Handling section so the final order is: ... Domain Specialization → Constitution excerpt → Large File Handling → Output Format.
      5. Total file length target: 200–400 lines. If base body + manifesto pushes past 400, extract domain conventions to a reference file and link it
    </action>

    <action>Store the draft as {{composed_content}}</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 3: VALIDATE VIA SKILL-CREATOR                     -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="3" goal="Validate composed file via skill-creator eval loop">
    <action>Write the draft to a temporary path: {{output_path}}.draft</action>

    <action>Invoke the `skill-creator:skill-creator` skill with:
      - mode: eval-only (do not rewrite from scratch, only validate and improve the existing draft)
      - target: {{output_path}}.draft
      - context: "This is a Tier 2 composed agent file for role={{role}}, domain={{domain}}. The base body is {{base_body_path}}. Validate that the composition follows agent definition conventions, the Large File Handling section is present and correct, the domain specialization is actionable and specific, and the file is within the 400-line target."
    </action>

    <check if="skill-creator reports issues">
      <action>Apply skill-creator's improvements to {{composed_content}}.</action>
      <action>Re-run one additional eval pass. Accept the result.</action>
    </check>

    <check if="skill-creator invocation not available">
      <action>Log: "skill-creator not available — performing manual validation checklist."</action>
      <action>Verify manually:
        - [ ] Frontmatter has: name, description, model, effort, tools
        - [ ] description is under 250 chars and front-loaded
        - [ ] Base body content present and unmodified
        - [ ] Domain Specialization section is specific and actionable
        - [ ] Large File Handling section present
        - [ ] File under 400 lines
      </action>
    </check>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 4: WRITE OUTPUT FILES                             -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="4" goal="Write composed agent file and routing entry">
    <action>Ensure the output directory exists: {{output_dir}}</action>
    <action>Write the validated composed content to {{output_path}}. Remove the .draft file if it exists.</action>

    <action>Update the routing entry in momentum/agents.json.

    If momentum/agents.json does not exist, create it with this structure:
```json
{
  "defaults": {},
  "project": []
}
```

    Read the existing file. Find the "project" array. Check if an entry already exists with "slug": "{{agent_slug}}".

    If exists: update the existing entry.
    If not exists: append a new entry.

    Entry format:
```json
{
  "role": "{{role}}",
  "domain": "{{domain}}",
  "slug": "{{agent_slug}}",
  "agent": "{{output_path}}",
  "patterns": {{permissions_scope}},
  "write_permissions": {{permissions_scope}}
}
```

    Write the updated momentum/agents.json.
    </action>

    <action>Update the project harness profile in momentum/harness.json.

    If momentum/harness.json does not exist, create it with this structure (matching the agents.json defaults/project split):
```json
{
  "defaults": {
    "env": { "startup": [], "readiness_probes": [] },
    "execution_surfaces": {},
    "driver_bindings": {},
    "platform_matrix": { "default": ["host"] },
    "human_review_carveouts": [],
    "trivial_smoke_escape": { "enabled": false, "change_types": [] }
  },
  "project": []
}
```

    Read the existing file. Check if the "project" array already contains an entry for this agent's domain (keyed by "domain": "{{domain}}").

    If this agent introduces a new execution surface or driver binding for its domain that differs from the defaults, append or update a project-level entry:
```json
{
  "domain": "{{domain}}",
  "env": {
    "startup": [],
    "readiness_probes": []
  },
  "execution_surfaces": {},
  "driver_bindings": {},
  "platform_matrix": []
}
```

    Only add fields that differ from the plugin defaults. Skip this step entirely if the agent's domain requires no harness overrides (e.g., a pure skill-instruction agent using the default Skill driver).

    Write the updated momentum/harness.json only if changes were made.
    </action>

    <output>
## Agent Built: {{agent_slug}}

**Composed file:** `{{output_path}}`
**Routing entry:** `momentum/agents.json` → project[slug="{{agent_slug}}"]

**Agent covers:**
- Role: {{role}}
- Domain: {{domain}}
- File patterns: {{permissions_scope}}

**Next steps:**
- Invoke `momentum:agent-builder` directly for remaining role × domain pairs
- Verify the composed file in `{{output_path}}` before deploying
- If this agent story came from sprint-dev, the approval gate is next
    </output>
  </step>

</workflow>
