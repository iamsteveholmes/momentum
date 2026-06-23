# momentum:build-guidelines — Workflow

**Six-phase orchestration:** Discover → Consult → Fan Out to constitution-builder (Tier 2) → Generate Tier 1 → Register + Wire → Validate

**Orchestrator purity contract:** This workflow contains ZERO KB-synthesis logic. Every Permissions / Standing Rules / Quick Routing generation step is delegated to `momentum:constitution-builder`. This skill loops, registers, wires, and validates only.

---

<workflow>
  <critical>The manifesto is NEVER a per-sprint context overlay. Read it as stable, sprint-invariant input. Do not inject any sprint slug, story slug, or sprint-scoped context into any composed output. DEC-038 D1.</critical>
  <critical>This skill is an orchestrator only — it invokes constitution-builder for all KB synthesis. Do not inline any Permissions / Standing Rules / routing-table generation. DEC-038 G1, AC6.</critical>
  <critical>G1 gate is pass/fail: at least one composed agent file written to disk AND registered in momentum/agents.json. A run that does not meet G1 is a failed run. DEC-038 G1.</critical>
  <critical>Dependency check FIRST: if constitution-builder does not support composed_agent_file / standalone_constitution write modes, HALT with clear message before any other work.</critical>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 1: DISCOVER                                       -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="1" goal="Discover manifests, resolve project + KB, detect base bodies">

    <action>DEPENDENCY CHECK — before any other work:
      Read skills/momentum/skills/constitution-builder/SKILL.md.
      Confirm: the write_mode parameter section lists "composed_agent_file" and "standalone_constitution" as valid values.
      If NOT confirmed: HALT immediately with:
        "build-guidelines requires constitution-builder with composed_agent_file / standalone_constitution write modes
        (story: constitution-builder-write-mode-parameterization). Please complete that dependency first."
    </action>

    <action>Resolve invocation arguments or apply defaults:
      - manifests_dir = argument or ".claude/manifests/"
      - output_dir = argument or ".claude/guidelines/agents/"
      - constitution_path = argument or ".claude/guidelines/constitution.md"
      - dry_run = argument or false
    </action>

    <action>Scan manifests_dir for manifesto files matching {role}-{domain}.md pattern.
      For each file found:
        1. Read the YAML frontmatter block (identity fields: role, domain, project_kb)
        2. Confirm required fields: role, domain, project_kb — all present
        3. Confirm ## Project Stack section present
        4. Confirm ## Diagnostic Table section present with ≥1 entry
        5. Confirm base body exists: skills/momentum/agents/{role}.md
      Build: {{manifest_matrix}} = list of {role, domain, project_kb, manifesto_path, base_body_path, valid: true|false}
      Note any invalid manifests (missing required fields) — surface in Consult phase.

      CRITICAL: Read the diagnostic table as stable, sprint-invariant data.
      DO NOT: ask the developer for sprint context, story context, or per-sprint overlays.
    </action>

    <action>Resolve the target project and KB for this run:
      - Read project_kb from each manifesto's identity block
      - If all manifests share the same project_kb: this is a single-KB run
      - If manifests have different project_kb values: this is a multi-KB run — each constitution-builder invocation will carry the specific project_kb for its manifesto
      - Store: {{kb_scope}} = "single" | "multi", {{default_project_kb}} = project_kb from first valid manifest
      Note: wiki-query multi-KB extension (FR142) is planned, not yet implemented. Store project_kb for pipeline readiness — pass it to constitution-builder as context even if routing is not yet operative.
    </action>

    <action>Check current state:
      - Does .claude/guidelines/agents/ exist? Note which composed agent files already exist (if any)
      - Does .claude/guidelines/constitution.md exist? Note if Tier 1 constitution is already present
      - Does momentum/agents.json exist? If so, read it — note existing project[] entries
      Store: {{existing_agents}} = list of existing {role}-{domain}.md slug names
      Store: {{agents_json_exists}} = true | false
    </action>

    <output>
## Discover — Manifest Matrix

Project KB: {{default_project_kb}} ({{kb_scope}} KB run)
Manifests found: {{manifest_matrix | count}} at {{manifests_dir}}

| Role × Domain | Manifesto | Base Body | Valid |
|---|---|---|---|
{{for each entry in manifest_matrix:
| {{role}} × {{domain}} | {{manifesto_path}} | {{base_body_path}} | {{valid}} |
}}

{{if invalid manifests:
⚠ Invalid manifests (skipped — missing required fields):
{{list them with reason}}
}}

Existing composed agents: {{existing_agents | count or "none"}}
    </output>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 2: CONSULT                                        -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="2" goal="Interactive confirmation of matrix, constitution plan, reference-doc scope">

    <output>
## Consult

Plan for this run:
- Compose {{manifest_matrix | valid count}} agent file(s): {{comma-separated role-domain pairs}}
- Generate Tier 1 constitution at {{constitution_path}}
- Register all composed agents in momentum/agents.json

{{if existing composed agents in output_dir:
ℹ Existing composed agent files will be overwritten:
{{list them}}
}}

{{if dry_run:
DRY RUN — no files will be written. Preview only.
}}
    </output>

    <ask>Confirm matrix is current and plan is correct. Any role × domain pairs to add, remove, or adjust?
    (Enter: Y to proceed / list changes / 'dry-run' to preview only)</ask>

    <action>Process developer response:
      - "Y" or "yes": proceed with matrix as-is
      - Changes listed: update {{manifest_matrix}} accordingly
      - "dry-run": set dry_run = true
      Store final confirmed matrix as {{confirmed_matrix}}
    </action>

    <action>Determine reference-doc scope:
      Check constitution-builder's AC-3 budget (750 lines max for constitution.md).
      If any domain's manifesto is unusually large (>150 lines), note that reference-doc extraction may be needed post-generation.
      Store: {{overflow_risk_domains}} = list of domains where reference-doc extraction is likely
    </action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 3: FAN OUT — Tier 2 Composed Agent Files         -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="3" goal="Invoke constitution-builder per role × domain pair for Tier 2 composition">

    <action>Initialize: {{composed_agents}} = [] (accumulator for successfully composed files)</action>

    <action>For each entry in {{confirmed_matrix}} (sequential — one pair at a time for clarity):

      current = {role, domain, project_kb, manifesto_path, base_body_path}
      target_path = "{{output_dir}}/{{current.role}}-{{current.domain}}.md"

      1. Read the manifesto file at {{current.manifesto_path}}
         Extract: identity block, ## Project Stack content, ## Diagnostic Table content (verbatim — do NOT rephrase or rewrite)
         Store as {{manifesto_content}}

      2. Read the base body at {{current.base_body_path}}
         Store as {{base_body_content}}

      3. Invoke momentum:constitution-builder with:
           write_mode: composed_agent_file
           target_path: {{target_path}}
           project_kb: {{current.project_kb}}
           Context to pass:
             - Role: {{current.role}}
             - Domain: {{current.domain}}
             - Project KB: {{current.project_kb}}
             - Project Stack: {{manifesto_content.project_stack}} (verbatim from manifesto)
             - Diagnostic Table: {{manifesto_content.diagnostic_table}} (verbatim — stable, sprint-invariant)
             - Base body path: {{current.base_body_path}}
           Instruction: "Generate domain-knowledge sections for a {{current.role}} × {{current.domain}} composed agent.
             The Diagnostic Table below is stable and sprint-invariant — embed it verbatim.
             Do NOT generate Quick Routing or per-agent permissions (per DEC-038, those belong at agent-builder layer).
             Target file: {{target_path}}"

      CRITICAL ASSEMBLY RULE — the composed file must match the cmp-dev exemplar shape:
        a. YAML frontmatter: name, model, tools (at minimum)
        b. ## Project Guidelines — {domain} ({date}) section with critical rules
        c. The ## Diagnostic Table (verbatim from manifesto — NO rewriting)
        d. A `---` separator line
        e. The full unmodified base body ({{base_body_content}}) below the separator
        NO sprint identifier, NO story identifier anywhere in the file.

      4. After constitution-builder writes the file:
         Confirm file exists at {{target_path}}
         If dry_run = true: report "Would write: {{target_path}}" — do not write
         If confirmed: append to {{composed_agents}} = {{composed_agents}} + [{role, domain, path: target_path}]

      5. Report per-pair result:
         "✓ {{current.role}}-{{current.domain}} → {{target_path}}"
         or
         "✗ {{current.role}}-{{current.domain}} — constitution-builder error: {{error}}"
    </action>

    <output>
## Tier 2 — Composed Agent Files

{{for each result:
  {{status}} {{role}}-{{domain}} → {{path}}
}}

Successfully composed: {{composed_agents | count}} / {{confirmed_matrix | count}}
    </output>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 4: GENERATE TIER 1 CONSTITUTION                   -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="4" goal="Invoke constitution-builder once for Tier 1 standalone constitution">

    <action>Invoke momentum:constitution-builder with:
      write_mode: standalone_constitution
      (No target_path argument — constitution-builder uses canonical path .claude/guidelines/constitution.md)
      project_kb: {{default_project_kb}}
      Context: use the same project context from Phase 2 (project name, technologies, universal practices)
      Instruction: "Generate the Tier 1 standalone constitution for this project.
        Include the Canonical Wiki-Query Interface Block.
        Do NOT include any ## Quick Routing section or per-agent diagnostic tables (per DEC-038).
        Budget: target ~660 lines, hard ceiling 750 lines."
    </action>

    <action>After constitution-builder writes the constitution:
      Verify .claude/guidelines/constitution.md exists
      Count lines: wc -l .claude/guidelines/constitution.md (or read and count)
      If line count > 750: WARN — constitution exceeds 750-line ceiling (AC-3 failure)
        Prompt: "Constitution is {{N}} lines, exceeding the 750-line ceiling. Extract detail sections to .claude/guidelines/refs/ and add load pointers?"
        If developer confirms: identify overlong sections, move to .claude/guidelines/refs/{section-name}.md, add load pointers
        Re-measure after extraction
    </action>

    <output>
## Tier 1 — Constitution

Written to: {{constitution_path}}
Line count: {{N}} lines {{if N > 750: ⚠ OVER CEILING (750 max)}}
    </output>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 5: REGISTER + WIRE                                -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="5" goal="Register composed agents in momentum/agents.json + record paths for sprint-dev">

    <action>For each successfully composed agent in {{composed_agents}}:

      Load momentum/agents.json:
        If not exists: create with structure {"defaults": {}, "project": []}
        If exists: read it

      Build registration entry:
      {
        "role": "{{agent.role}}",
        "domain": "{{agent.domain}}",
        "slug": "{{agent.role}}-{{agent.domain}}",
        "agent": "{{agent.path}}",
        "patterns": [],
        "write_permissions": []
      }
      Note: patterns and write_permissions are left empty here — they are set per-story
      when sprint-dev resolves the agent. The slug-keyed registration is what matters for G1.

      Check project[] array:
        If entry with slug = "{{agent.role}}-{{agent.domain}}" exists: UPDATE it
        If not exists: APPEND the new entry

      Write updated momentum/agents.json
    </action>

    <action>Verify registration resolves via momentum-tools:
      For at least the first composed agent in {{composed_agents}}:
        Run: momentum-tools agent resolve --touches "{{any file path typical for this domain}}"
        OR: momentum-tools agent resolve --role {{agent.role}} (if role matches a defaults entry)
      Confirm the result includes the registered slug or agent path.
      If resolution fails: log warning — "agent resolve did not return {{slug}}; verify momentum-tools path and agents.json schema"
    </action>

    <action>Record composed-file paths for sprint-dev handoff:
      Write (or update) a handoff record: momentum/build-guidelines-last-run.json
      Structure:
      {
        "run_date": "{{ISO 8601 date}}",
        "sprint_invariant": true,
        "composed_agents": [
          {"slug": "{{slug}}", "path": "{{path}}", "role": "{{role}}", "domain": "{{domain}}"}
        ],
        "constitution_path": "{{constitution_path}}"
      }
      sprint-dev reads this to detect composed files per AC7 (detection/fallback contract).
    </action>

    <output>
## Register + Wire

momentum/agents.json updated:
{{for each composed agent:
  project[slug="{{slug}}"] → {{agent_path}}
}}

Handoff record: momentum/build-guidelines-last-run.json
    </output>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 6: VALIDATE                                       -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="6" goal="AVFL checkpoint — verify G1, line counts, role-bleed, exemplar shape, citation integrity">

    <action>Assert G1 condition explicitly:
      G1 check:
        a. Count composed agent files on disk in {{output_dir}}: at least 1
        b. Count project[] entries in momentum/agents.json: at least 1
        c. For (a) and (b): at least one slug matches between disk and agents.json
      If G1 not met: emit "G1 Gate: FAILED" with details and HALT.
      If G1 met: emit "G1 Gate: PASSED"
    </action>

    <action>For each composed agent file, verify line count:
      Read file, count lines
      Flag if > 400 lines (target for composed agent files per agent-builder conventions)
      Note: composed files can be larger than SKILL.md files — the 400-line guidance is a target, not a ceiling
    </action>

    <action>Role-bleed check — verify no cross-role contamination:
      For each composed agent file:
        The file should reference only the role and domain in its name
        QA manifesto content must not appear in a dev agent file
        Run quick text check: grep for other roles' domain-specific terms in wrong files
        Flag any role-bleed found
    </action>

    <action>Exemplar-shape conformance check (DEC-038 G1 criterion):
      For each composed agent file, verify against cmp-dev exemplar shape
      (reference: docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md — format reference ONLY, never a Momentum agent):
        ✓ YAML frontmatter with name, model, tools fields
        ✓ ## Project Guidelines (or equivalent guidelines section) ABOVE the --- separator
        ✓ Diagnostic table entries in the guidelines section (symptom → wiki-query format)
        ✓ A --- separator line present
        ✓ Full unmodified base body BELOW the separator
        ✓ Incompleteness-signal instruction present: grep the composed file for "MANIFESTO INCOMPLETE"
          If not found: the composed file does not carry the incompleteness signal contract.
          Add the following instruction to the guidelines block (above the --- separator):
            "When encountering a situation not covered by any entry in the Diagnostic Table above,
             emit: [MANIFESTO INCOMPLETE: no diagnostic-table entry for <situation>]
             Do not silently fall through to training knowledge — surface the gap."
        ✗ No sprint identifier anywhere in the file
        ✗ No story identifier anywhere in the file
        ✗ No "overlay" or "per-sprint" language anywhere
    </action>

    <action>Citation integrity spot-check:
      For each diagnostic-table entry in the composed agent files:
        The wiki-query terms should be consistent with the project_kb declared in the manifesto
        (Full AVFL citation gate deferred to citation-integrity-validation-in-build-guidelines-avfl story)
        Here: verify the terms look like legitimate KB queries (not empty strings, not placeholder text)
    </action>

    <action>Constitution validation:
      Verify .claude/guidelines/constitution.md:
        - Contains no ## Quick Routing section
        - Contains no per-agent diagnostic table (role-specific routing rows)
        - Line count ≤ 750
        - Contains ## Wiki-Query Interface section
    </action>

    <output>
## Validate — Build-Guidelines Run Report

**G1 Gate: {{PASSED | FAILED}}**
{{if FAILED: detailed failure reason}}

Composed Agents:
{{for each composed agent:
  {{slug}} ({{line_count}} lines)
    Shape: {{PASS | FAIL — reason}}
    Role-bleed: {{CLEAN | DETECTED — description}}
    Citations: {{CLEAN | WARNING — description}}
}}

Constitution ({{constitution_path}}):
  Line count: {{N}} / 750 max — {{PASS | FAIL}}
  No Quick Routing: {{PASS | FAIL}}
  Wiki-Query Interface present: {{PASS | FAIL}}

Registered in momentum/agents.json: {{N}} entries

**Overall: {{BUILD COMPLETE | BUILD FAILED}}**

{{if BUILD COMPLETE:
Sprint-dev can now detect composed agent files in {{output_dir}}.
Handoff record written to momentum/build-guidelines-last-run.json.
To verify: open any .claude/guidelines/agents/{role}-{domain}.md and confirm
  the diagnostic table appears above the --- separator, and the base body below.
}}
    </output>
  </step>

</workflow>
