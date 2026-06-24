# momentum:build-guidelines — Workflow

**Six-phase orchestration:** Discover → Consult → Fan Out to agent-builder (Tier 2 composition + registration) → Generate Tier 1 → Verify Registration → Validate

**Orchestrator purity contract:** This workflow contains ZERO KB-synthesis logic and ZERO agents.json self-writes. Tier 2 composition (file assembly + routing-table registration with non-empty patterns[]) is delegated entirely to `momentum:agent-builder`. Domain-knowledge synthesis is optionally delegated to `momentum:constitution-builder`. This skill loops, verifies, and validates only.

---

<workflow>
  <critical>The manifesto is NEVER a per-sprint context overlay. Read it as stable, sprint-invariant input. Do not inject any sprint slug, story slug, or sprint-scoped context into any composed output. DEC-038 D1.</critical>
  <critical>This skill is an orchestrator only — it invokes agent-builder for Tier 2 composition+registration and optionally constitution-builder for KB synthesis. Do not inline any composition, permissions, routing-table generation, or agents.json writes. DEC-038 G1, AC6.</critical>
  <critical>G1 gate is pass/fail: at least one composed agent file written to disk AND registered in momentum/agents.json WITH non-empty patterns[]. An agents.json entry with patterns:[] is NEVER matched by momentum-tools agent resolve --touches — the composed agent is functionally dead. G1 requires the --touches resolver to return the composed slug, not the generic fallback. A run that does not meet G1 is a failed run. DEC-038 G1.</critical>
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

  <step n="3" goal="Invoke agent-builder per role × domain pair for Tier 2 composition + registration">

    <!-- ORCHESTRATION NOTE: This skill delegates ALL composition and agents.json registration to
         momentum:agent-builder. build-guidelines NEVER self-assembles composed files or self-registers
         agents.json entries. agent-builder is the canonical Tier 2 composer — it assembles
         frontmatter + domain-knowledge ABOVE the --- separator + full unmodified base body BELOW
         the separator, and writes the agents.json routing entry with non-empty patterns populated
         from permissions_scope. This is what makes the --touches resolver match. -->

    <action>Initialize: {{composed_agents}} = [] (accumulator for successfully composed files)</action>

    <action>For each entry in {{confirmed_matrix}} (sequential — one pair at a time for clarity):

      current = {role, domain, project_kb, manifesto_path, base_body_path}
      target_path = "{{output_dir}}/{{current.role}}-{{current.domain}}.md"

      1. Read the manifesto file at {{current.manifesto_path}}
         Extract: identity block, ## Project Stack content, ## Diagnostic Table content (verbatim — do NOT rephrase or rewrite)
         Store as {{manifesto_content}}

      2. OPTIONAL — get domain-knowledge sections from constitution-builder:
         If the manifesto's diagnostic table requires synthesis against the project KB
         (i.e., wiki-query terms need to be validated or cross-referenced):
           Invoke momentum:constitution-builder with:
             write_mode: composed_agent_file
             target_path: {{target_path}}.domain-knowledge (temp path)
             project_kb: {{current.project_kb}}
             Context: Role, Domain, Project Stack, Diagnostic Table (verbatim)
             Instruction: "Generate ONLY domain-knowledge sections (Project Guidelines — prose context)
               for a {{current.role}} × {{current.domain}} agent. Do NOT assemble the base body.
               Do NOT generate Quick Routing, Diagnostic Table, or per-agent permissions
               (Diagnostic Table is carried verbatim from the manifesto; routing belongs at agent-builder
               layer per DEC-038).
               Target: {{target_path}}.domain-knowledge (assembly by agent-builder)"
           Store constitution-builder's prose output as {{constitution_prose}}
           Build {{domain_knowledge_content}} by combining:
             1. {{constitution_prose}}  (KB-synthesized Project Guidelines prose)
             2. The verbatim ## Diagnostic Table extracted from {{manifesto_content}} in step 1
                (do NOT rephrase or rewrite — pass it exactly as read)
           NOTE: constitution-builder never emits a Diagnostic Table (see DEC-038 D1 / SKILL.md:35,
           204-206). The manifesto's ## Diagnostic Table MUST be preserved here and passed to
           agent-builder; relying on constitution-builder to supply it silently discards it.
         If the manifesto already provides complete domain knowledge inline (Project Stack +
         Diagnostic Table are sufficient without KB synthesis):
           Build {{manifesto_context}} directly from the manifesto's ## Project Stack and
           ## Diagnostic Table sections (verbatim — do NOT rephrase or rewrite).
           Set {{domain_knowledge_content}} = {{manifesto_context}}

      3. DELEGATE TO momentum:agent-builder for full composition + registration:
         Invoke momentum:agent-builder with:
           base_body_path: {{current.base_body_path}}      (e.g., skills/momentum/agents/dev.md)
           role: {{current.role}}                          (e.g., "dev")
           domain: {{current.domain}}                     (e.g., "kotlin-compose" — the manifesto domain id)
           constitution_path: {{constitution_path}}        (pass current run's constitution path)
           manifesto_context: {{domain_knowledge_content}} (domain-knowledge block from step 2)
           permissions_scope: <file patterns this role owns in this domain — derive from manifesto's
             ## Project Stack "Shared UI" / "Shared logic" paths, or from any "File ownership" section
             in the manifesto. These patterns MUST be non-empty so momentum-tools agent resolve
             --touches matches. Examples:
               dev × kotlin-compose → ["composeApp/**", "shared/**", "*.kt"]
               dev × skills         → ["skills/**/*.md", "skills/**/*.yaml", "skills/**/*.sh"]
               qa × kotlin-compose  → ["**/test/**/*.kt", "**/androidTest/**/*.kt"]
             If no ownership section exists in the manifesto, use the ## Project Stack paths
             as the basis and default to broad-match patterns for this domain.>
           output_dir: {{output_dir}}
         agent-builder will:
           a. Draft composed file: YAML frontmatter + domain specialization block ABOVE --- + full base body BELOW ---
           b. Validate via skill-creator
           c. Write to {{target_path}} (= {{output_dir}}/{{current.role}}-{{current.domain}}.md)
           d. Write routing entry to momentum/agents.json with patterns = permissions_scope (NON-EMPTY)
         If dry_run = true: pass dry_run=true to agent-builder and report "Would write: {{target_path}}" — do not write

      4. After agent-builder completes:
         Confirm file exists at {{target_path}}
         If confirmed: append to {{composed_agents}} = {{composed_agents}} + [{role, domain, path: target_path, slug: "{{current.role}}-{{current.domain}}"}]

      5. Report per-pair result:
         "✓ {{current.role}}-{{current.domain}} → {{target_path}}"
         or
         "✗ {{current.role}}-{{current.domain}} — agent-builder error: {{error}}"
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
  <!-- PHASE 5: VERIFY REGISTRATION + WIRE                     -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="5" goal="Verify agent-builder registered agents correctly + record paths for sprint-dev">

    <!-- REGISTRATION NOTE: momentum/agents.json is written by momentum:agent-builder in Phase 3 —
         NOT by this skill. build-guidelines NEVER writes agents.json directly. This phase only
         verifies the entries that agent-builder produced and writes the sprint-dev handoff record. -->

    <action>Verify each composed agent in {{composed_agents}} is correctly registered:

      Read momentum/agents.json (written by agent-builder in Phase 3).

      For each agent in {{composed_agents}}:
        expected_slug = "{{agent.role}}-{{agent.domain}}"
        Find the project[] entry where slug == expected_slug.
        Assert:
          a. Entry exists in project[]
          b. entry.agent points to a file that exists on disk ({{agent.path}})
          c. entry.patterns is NON-EMPTY (this is the critical G1 resolver requirement —
             empty patterns means --touches will never match this entry)
        If any assertion fails: log "REGISTRATION FAILURE: {{expected_slug}} — {{reason}}"
          and flag for the G1 gate in Phase 6.
    </action>

    <action>Verify resolvability via momentum-tools --touches (CRITICAL — this is the production code path):
      For each composed agent in {{composed_agents}}:
        Derive a representative file path that this agent's patterns should match.
          Example: for dev-kotlin-compose with patterns ["composeApp/**"], use "composeApp/src/main/MyScreen.kt"
          Example: for dev-skills with patterns ["skills/**/*.md"], use "skills/momentum/skills/example/SKILL.md"
        Run: momentum-tools agent resolve --touches "{{representative_path}}"
        Parse the returned results array.
        Assert: at least one result has slug == "{{expected_slug}}" (the COMPOSED slug — not "dev" or generic).
        If assertion passes: log "✓ {{expected_slug}} resolves via --touches"
        If assertion fails (returns generic 'dev' fallback or no match):
          log "✗ RESOLVER FAILURE: {{expected_slug}} — --touches returned {{actual_result}} not the composed slug.
            Cause: patterns[] in agents.json entry is likely empty or does not match {{representative_path}}.
            Fix: re-run momentum:agent-builder with correct permissions_scope for this domain."
          Flag for G1 gate.
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
## Verify Registration + Wire

momentum/agents.json (written by agent-builder):
{{for each composed agent:
  project[slug="{{slug}}"] → {{agent_path}} · patterns: {{patterns_count}} entries · --touches: {{resolve_status}}
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
        b. Count project[] entries in momentum/agents.json with non-empty patterns[]: at least 1
           (entries with patterns:[] are NOT resolvable — they do not satisfy G1)
        c. For (a) and (b): at least one slug matches between disk and agents.json AND has non-empty patterns[]
        d. For at least one composed agent, run: momentum-tools agent resolve --touches "{{representative_path}}"
           Assert the returned slug is the COMPOSED slug (e.g., "dev-kotlin-compose"), NOT the generic
           fallback (e.g., "dev"). A result of the generic fallback means patterns[] is empty or wrong
           and G1 is NOT met — the --touches resolver is the production code path that sprint-dev uses.
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
