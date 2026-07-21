# momentum:manifesto-builder — Workflow

**Goal:** produce one format-conformant manifesto at `.claude/manifests/{role}-{domain}.md` by
auto-drafting its diagnostic table from the project KB, then requiring the developer to curate the
symptom phrasing and File Ownership globs before anything is written.

**Format authority:** `skills/momentum/references/manifesto-format.md` (v1.0) — read it before drafting.
Every section below cites the format-spec section it implements.

**Reuse target:** `skills/momentum/skills/constitution-builder/SKILL.md` Phase 3 — the `wiki-query`-per-concept
KB loop. This skill re-invokes that method; it does not re-implement a parallel KB-lookup approach.

---

<workflow>
  <critical>The manifesto is a stable, per-role×domain diagnostic table — never a per-sprint or per-story artifact. No sprint slug, story slug, or "overlay" language may appear anywhere in the output. DEC-038 D1.</critical>
  <critical>NEVER finalize a raw draft. The CURATE step's elicitation must actually occur — with a real developer response incorporated — before the FINALIZE/WRITE step runs. DEC-038 G2.</critical>
  <critical>`## File Ownership` is authored fresh from the role×domain's actually-owned paths. It is NEVER inferred from `## Project Stack` prose and NEVER copied from the reference exemplar (which predates this field). manifesto-format.md normative rules.</critical>
  <critical>Every diagnostic-table entry's `wiki-query` terms must come from an actual KB lookup performed during GENERATE. Do not invent terms that were not the output of a `wiki-query` call.</critical>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 0: ELICIT                                         -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="0" goal="Collect role, domain, project_kb, and stack facts">
    <action>Check invocation arguments for role, domain, project_kb. If all three are supplied
      (orchestrated or scripted invocation), skip the questions below and proceed to the vault
      lookup.</action>

    <check if="role or domain is missing">
      <ask>What role is this manifesto for? (dev, qa, e2e, architect, pm, or a new role)</ask>
      <ask>What technology domain does this role×domain pair cover? (e.g. kotlin-compose, python-fastapi, react-ts)</ask>
    </check>

    <action>Resolve the KB: run `cat ~/.obsidian-wiki/config` and extract `OBSIDIAN_VAULT_PATH`.
      If the config declares a single vault, that vault is the KB this manifesto's entries resolve
      against — derive {{project_kb}} from the vault's project identity (e.g. the vault directory
      name or its index.md title/project section), and confirm with the developer in one line rather
      than a full question: "Resolving against KB: {{project_kb}} at {{vault_path}} — correct?"
      If the config declares (or the developer indicates) multiple project KBs are relevant, ask
      explicitly: "Which project KB should this manifesto's wiki-query entries resolve against?"
      Store {{project_kb}}, {{vault_path}}, {{kb_mode}} = "single" | "multi".
    </action>

    <action>Collect stack facts for `## Project Stack` (manifesto-format.md → Project Stack Section):
      language + version, core UI/application framework + version pin, data layer technology, test
      tooling, architecture paradigm, and any other version pins the diagnostic table depends on.
      Derive what you can from the project's own build files (e.g. build.gradle.kts, package.json,
      pyproject.toml) if this skill is running inside that project's repo. For facts that cannot be
      derived, ask: "What stack facts scope this {{role}}×{{domain}} agent's lookups? (language +
      version, framework + version, data layer, test tooling, architecture paradigm)"
      Store {{stack_facts}}.
    </action>

    <action>Determine the technology areas this role×domain routinely encounters — these become the
      `###` group headings in the Diagnostic Table. Derive candidates from {{stack_facts}} (each
      named framework/library is a candidate area) and cross-check against the KB index.md's concept
      category headings (Phase 1, next step) for a match. If the derived list looks sparse for the
      domain, ask: "What are the technology areas or recurring problem types a {{role}} on
      {{domain}} routinely hits? (e.g. for kotlin-compose: recomposition/side-effects, layout,
      animation, state management, navigation, plus test-tooling areas)"
      Store {{technology_areas}} = list of area names.
    </action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 1: GENERATE                                       -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="1" goal="Auto-draft the diagnostic table, Project Stack, and a first-pass File Ownership list">

    <action>Read `{{vault_path}}/index.md` for the invoking project's KB. Note the concept
      category headings and page titles present — this is the ground truth the draft must trace to.
      (manifesto-format.md → KB Scoping; constitution-builder SKILL.md Phase 3 step 2.)
    </action>

    <action>For each area in {{technology_areas}}:
      Run `wiki-query [area/concept]` — or, in multi-KB mode, `wiki-query --kb {{project_kb}} [area/concept]`
      — via the Skill tool (skill: "wiki-query", args: the query string).
      Collect the returned pages/sections and their exact terminology (page titles, key API names,
      named patterns). Do NOT paraphrase the KB's own vocabulary away — the wiki-query terms in each
      drafted entry should be drawn from what the KB actually returned.
      For each distinct, diagnosable situation the returned content surfaces, draft one entry:
        `- **<observable symptom, drafted>** → \`wiki-query <exact terms drawn from this lookup>\``
      Group all entries drafted from lookups under the same {{technology_areas}} member under one
      `###` heading matching that area name.
      If a wiki-query for an area returns nothing usable: do not invent an entry for that area. Note
      it as a KB gap instead (see Phase 1 self-check below) — the Dev Notes "KB dependency (soft)"
      note governs: a sparse KB legitimately yields a sparser draft, never a fabricated one.
    </action>

    <action>Draft `## Project Stack` from {{stack_facts}}, formatted per manifesto-format.md's
      example: a terse summary line, a bullet list of fact categories, and a bolded version-pinned
      tech line.
    </action>

    <action>Draft a first-pass `## File Ownership` glob list (manifesto-format.md → File Ownership
      Section, normative authoring rules) from the role×domain's actually-owned paths:
      - If the domain matches a pattern already worked in manifesto-format.md's examples (e.g.
        `kotlin-compose` → `composeApp/**`, `shared/**`, `*.kt`; `skills` → `skills/**/*.md`,
        `skills/**/*.sh`, `skills/**/*.yaml`), use that shape as the starting draft, adjusted to this
        project's actual directory layout (verify the globs match real paths in this repo — Glob or
        Bash `find` the candidate globs before finalizing the draft).
      - Otherwise, derive candidate globs from the project's directory structure for paths this
        role×domain would plausibly touch, and verify each glob matches at least one real file
        (manifesto-format.md rule 2).
      - Never draft only a single `**/*` catch-all unless the role genuinely owns the entire tree.
      - Cover every file type this role routinely edits for this domain (rule 4) — not just the
        primary source extension.
      Store {{draft_file_ownership}} = list of glob strings, each already verified against the repo.
    </action>

    <output>
## Generate — Draft Manifesto for {{role}}×{{domain}}

**Project Stack (draft):**
{{stack_facts summary}}

**File Ownership (draft):**
{{draft_file_ownership, one per line}}

**Diagnostic Table (draft):**
{{for each technology_area with entries:
### {{area}}
- **{{symptom}}** → `wiki-query {{terms}}`
...
}}

{{if any technology_areas produced no usable KB content:
KB gaps (no draft entries — sparse KB, not fabricated): {{list of areas}}
}}
    </output>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 2: CURATE (required — never skipped)              -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="2" goal="Elicit developer curation of symptom phrasing and File Ownership globs — block finalize until answered">

    <action>Present the full draft from Phase 1 output above, then present the curation checklist
      drawn verbatim from manifesto-format.md's normative rules:

      **Symptom phrasing rules (every entry must satisfy all four):**
      1. Observable — what the developer sees, not an internal cause.
      2. Specific — names the API, behavior, or output that is wrong.
      3. Diagnostic — distinguishes this entry from its neighbors in the same group.
      4. Phrased as a situation, not a question.

      **wiki-query invocation rules:**
      - Exact terms, never "search for X."
      - Terms must match real KB page titles/content (already true of the draft — curation should
        preserve this, not loosen it into vaguer language).

      **File Ownership rules:**
      - Non-empty, concrete, standard glob syntax, covers every edited file type, not a bare `**/*`
        unless truly whole-tree.
    </action>

    <ask>Review the draft diagnostic table above against the symptom-phrasing checklist. For each
      entry: keep as-is, reword the symptom, reword the wiki-query terms, split it into more than one
      entry, or drop it. Also review the draft File Ownership glob list — add, remove, or narrow any
      globs. Reply with your changes (or "looks good" to accept the draft as curated).</ask>

    <action>Do NOT proceed to Phase 3 until this question has been answered. There is no
      default-proceed path — an unanswered curation prompt blocks finalize, it does not silently
      pass the draft through.
    </action>

    <action>Apply the developer's response to produce {{curated_table}} and {{curated_file_ownership}}:
      - Incorporate every reword, split, drop, and addition the developer specified.
      - If the developer replied "looks good" / equivalent explicit acceptance, {{curated_table}} =
        the Phase 1 draft table and {{curated_file_ownership}} = the Phase 1 draft globs — curation
        occurred (the developer reviewed and affirmed it), it was not skipped.
      - Re-check every entry in {{curated_table}} against the four symptom-phrasing rules and the
        wiki-query invocation rules one more time. If any entry still fails a rule after the
        developer's response, flag it back to the developer rather than silently writing it: "Entry
        '{{symptom}}' still reads as a question / is still vague — how should this be worded?"
    </action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 3: FINALIZE / WRITE                               -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="3" goal="Self-check against the Discover checklist and completeness criterion, then write">

    <action>Assemble the final manifesto content using manifesto-format.md's Manifesto File Template,
      section order: identity block (`role`, `domain`, `project_kb`) → `## Project Stack` (from Phase
      1) → `## File Ownership` (`{{curated_file_ownership}}`) → `## Diagnostic Table`
      (`{{curated_table}}`, grouped under `###` technology-area headings).
    </action>

    <action>Self-check against `build-guidelines` Phase 1 Discover's validity checklist before writing
      (do not write if any check fails — surface the failure to the developer instead):
      1. Identity block present with `role`, `domain`, `project_kb` all set (non-placeholder values).
      2. `## Project Stack` section present.
      3. `## File Ownership` section present AND `file_ownership` list non-empty.
      4. `## Diagnostic Table` section present with ≥1 entry.
      (The 5th Discover check — a base body existing at `skills/momentum/agents/{{role}}.md` — is
      outside this skill's control; note its presence/absence in the completion report but do not
      block the write on it.)
    </action>

    <action>Self-check against the Completeness Criterion (manifesto-format.md → Completeness
      Criterion) — qualitative, never a count:
      - No entry is placeholder/"DRAFT" residue.
      - No {{technology_areas}} member that the role×domain routinely encounters is conspicuously
        unrouted (a KB gap noted honestly in Phase 1 output is acceptable; a silently dropped area
        with no explanation is not).
      - Entry volume is informational only — a sparse KB legitimately yields a sparse but complete
        table for what it covers.
    </action>

    <action>Write the assembled content to `.claude/manifests/{{role}}-{{domain}}.md`. Create
      `.claude/manifests/` if it does not exist.
    </action>

    <output>
## Manifesto Written: {{role}}-{{domain}}

**File:** `.claude/manifests/{{role}}-{{domain}}.md`

**Self-check:**
- Identity block: {{PASS}}
- Project Stack: {{PASS}}
- File Ownership: {{PASS}} ({{N}} globs)
- Diagnostic Table: {{PASS}} ({{N}} entries across {{M}} technology areas)
- Base body at `skills/momentum/agents/{{role}}.md`: {{present | ABSENT — build-guidelines will still discover this manifesto but cannot compose an agent from it until the base body exists}}

**Next step:** run `momentum:build-guidelines` to discover this manifesto and compose the runnable agent.
    </output>
  </step>

</workflow>
