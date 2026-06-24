# momentum:create-story Workflow

**Goal:** Create a Momentum story with change-type classification, injected implementation guidance, and AVFL validation.

**Role:** Story creation orchestrator for the Momentum project.
- Invoke `bmad-create-story` for all context extraction — do not re-implement its logic
- Classify change types from the story's tasks and inject Momentum-specific implementation guidance
- Run design-fidelity pass for UI stories before AVFL validation
- Run AVFL checkpoint before handing to developer

---

## INITIALIZATION

Load config from `{project-root}/_bmad/bmm/config.yaml` and resolve:
- `planning_artifacts`
- `implementation_artifacts`

---

## EXECUTION

<workflow>
  <critical>Do not duplicate bmad-create-story logic. Delegate all story creation to that skill.</critical>
  <critical>The Momentum Implementation Guide section you inject is the developer's authoritative guide — make it precise and actionable.</critical>

  <step n="1" goal="Resolve target story and select mode (enrich existing vs create from epic)">
    <critical>Momentum stories are slug-keyed and live at `.momentum/stories/{{story_key}}.md`.
      bmad-create-story is a CREATE-FROM-EPIC engine: it keys off `epic_num-story_num-title`
      IDs, auto-discovers from `sprint-status.yaml`, and INITIALIZES the output file from a
      template. Running it against an existing Momentum slug-story would overwrite the file
      and destroy its content. So: enrich existing Momentum stories IN PLACE; only delegate
      to bmad-create-story when creating a brand-new story that does not yet exist.</critical>

    <action>Resolve the target from the story identifier the user/orchestrator passed (a slug,
      a story key, or a path). Set {{story_key}} = the basename without extension if a path was
      given, else the slug/key verbatim. Set {{story_file}} = `.momentum/stories/{{story_key}}.md`.</action>

    <check if="{{story_file}} already exists under .momentum/stories/">
      <action>Set {{mode}} = "enrich". This is an existing Momentum story (commonly a
        `momentum:intake` stub). Enrich it IN PLACE — do NOT invoke bmad-create-story.</action>

      <action>Read the FULL existing {{story_file}}. Its current Story, Description, Acceptance
        Criteria, decision/DEC alignment, and References are AUTHORITATIVE content to PRESERVE
        and refine — never to discard.</action>
      <action>Reconcile epic membership (the index is authoritative — sprint-manager owns it):
        if this story already has an entry in `.momentum/stories/index.json` with a non-blank
        `epic_slug`, set {{epic_slug}} = that index value and update the story FILE frontmatter
        `epic_slug` to match (this self-heals stale frontmatter left by an epic move). Otherwise
        set {{epic_slug}} = the frontmatter value. Use {{epic_slug}} for all later epic-record
        lookups and for the index write.</action>

      <action>Load enrichment context (large-file protocol — Grep/chunk; NEVER full-read
        architecture.md, prd.md, epics.json, or stories/index.json):
        · the epics.json record for {{epic_slug}} (`{{planning_artifacts}}/epics.json`)
        · architecture.md sections relevant to this story (Grep by topic / decision id)
        · prd.md FRs relevant to this story (Grep by FR id / keyword)
        · recent git history for touched areas: `git log --oneline -8 -- {{frontmatter touches}}`
        · each existing file the story will modify (from frontmatter `touches`) — capture
          current state, what this story changes, and what must be preserved.</action>

      <action>Refine the story IN PLACE, preserving existing content:
        · Rewrite DRAFT/rough Acceptance Criteria into validated, testable, OBSERVABLE ACs
          (numbered) — keep their intent and any decision references; remove "DRAFT" and
          "INTAKE STUB" markers and stub disclaimers.
        · Add a `## Tasks / Subtasks` breakdown with explicit AC references per task.
        · Populate `## Dev Notes` (Decision Authority, Current State of affected files,
          Architecture Compliance, Testing Requirements, Project Context Reference),
          preserving the existing `### References` subsection.
        · Frontmatter: ensure story_type, priority, depends_on, touches are present — PRESERVE
          existing values; only ADD missing ones derived from analysis. NEVER drop an existing
          `depends_on` edge.
        · Set frontmatter `status: ready-for-dev`.</action>

      <action>Write the refined {{story_file}} in place. Do NOT relocate, template-initialize,
        or regenerate from scratch. Then GOTO Step 3 (Step 2's relocate does not apply —
        the file is already at its canonical path).</action>
    </check>

    <check if="{{story_file}} does NOT exist (new story to be created from an epic)">
      <action>Set {{mode}} = "create".</action>
      <action>Invoke the `bmad-create-story` skill. Pass through any story identifier, sprint context, or story path the user provided. Wait for full completion.</action>
      <action>After bmad-create-story completes, capture:
        - {{story_file}}: the output file path (from bmad-create-story's completion message)
        - {{story_key}}: the story key (e.g., "1-2-repository-structure")
      </action>
      <note>bmad-create-story handles: epic analysis, architecture extraction, web research, previous story intelligence, git analysis, Dev Notes population, sprint status update to "ready-for-dev". We own none of this.</note>
      <note>{{story_file}} is parsed from bmad-create-story's completion message. If it cannot be parsed (e.g., non-standard output format), derive it as `{{implementation_artifacts}}/{{story_key}}.md` and continue.</note>
    </check>
  </step>

  <step n="2" goal="Verify story file was written and relocate to .momentum/stories/">
    <check if="{{mode}} == 'enrich'">
      <action>SKIP this step — enrich mode already wrote the story in place at its canonical
        path during Step 1. Proceed directly to Step 3.</action>
    </check>
    <action>Confirm {{story_file}} exists and is non-empty</action>
    <check if="bmad-create-story halted or story file missing">
      <action>Set {{reason}} = "story file was not produced by bmad-create-story"</action>
      <output>Story creation did not complete — {{reason}}. No further action taken.</output>
      <action>HALT</action>
    </check>
    <action>If {{story_file}} is not already under `.momentum/stories/`, move it: set {{target}} = `.momentum/stories/{{story_key}}.md`, move the file to {{target}}, update {{story_file}} = {{target}}</action>
    <note>Momentum stories live in `.momentum/stories/` regardless of what `implementation_artifacts` is set to in config. bmad-create-story writes to the config-derived path; we own the relocation.</note>
  </step>

  <step n="3" goal="Detect UI story and run design-fidelity pass">
    <action>Scan the story's Title, Description, Acceptance Criteria, and Tasks sections for UI signals:
      - Canvas names, screen names, or screen layout references
      - Component names, UI element descriptions, design system mentions
      - Keywords: "canvas", "screen", "layout", "composable", "@Composable", "compose", "UI component", "design token", "hifi", "DESIGN.md"
      - File paths containing ui/, screen/, composable/, or Compose/Android frontend directories
    </action>
    <check if="no UI signals detected">
      <action>Store {{ui_story}} = false. No design-fidelity pass needed — skip the rest of this step.</action>
    </check>
    <check if="UI signals detected">
      <action>Store {{ui_story}} = true</action>
      <action>Identify {{touched_canvases}}: the specific canvases or screen areas this story modifies. Derive from story content — look for named canvases, journey references, or screen descriptions.</action>
      <action>Derive {{journey_slug}} from {{touched_canvases}}: e.g. "campaign-init canvas" or "campaign-init journey" → journey_slug = "campaign-init". If no journey is identifiable, store {{journey_slug}} = null.</action>

      <action>Load design sources — the system DESIGN.md is always in scope for any UI story, regardless of journey:
        1. ALWAYS read `docs/ux/design-system/DESIGN.md` if it exists — this is the base layer. Store as {{system_design_md}}.
        2. If {{journey_slug}} is not null, ALSO read `docs/ux/design-system/journeys/{{journey_slug}}/DESIGN.md` if it exists — this is a journey-specific supplement to the system doc, not a replacement. Store as {{journey_design_md}}.
        3. If neither exists, try `docs/ux/DESIGN.md` as a last fallback. Store as {{system_design_md}}.
        If no DESIGN.md was found at any path, store {{design_md_found}} = false. Otherwise {{design_md_found}} = true.
        Treat {{journey_design_md}} as an override layer: where it specifies values, those take precedence over {{system_design_md}}; for everything not covered by the journey doc, the system doc applies.
      </action>

      <check if="{{design_md_found}} is false">
        <action>Store {{ui_story}} = true, {{design_fidelity_status}} = "skipped — no DESIGN.md found"</action>
        <output>**Design-fidelity pass skipped** — no DESIGN.md found at expected paths. Developer must manually cross-reference design artifacts for this UI story.</output>
      </check>

      <check if="{{design_md_found}} is true">
        <action>Locate hifi fallback sources — check if these exist and read any that do:
          - `docs/ux/design-system/journeys/{{journey_slug}}/hifi.html` (if {{journey_slug}} is not null)
          - Most recent `docs/ux/design-system/handoff/*/project/components.css` (sort by date directory name, take the latest)
          Store found paths as {{hifi_sources}}.
        </action>

        <action>For each canvas or component in {{touched_canvases}}, extract from DESIGN.md sources (using hifi sources to resolve gaps or ambiguities):
          - Typography: font family, weight, and size per text element (eyebrow, header, body, footer, label, hint text)
          - Copy and vocabulary: exact text strings per canvas state — footer phrases, CTA labels, empty-state copy, error messages
          - Layout and rhythm: component type choices (e.g. FieldNote vs Field), hierarchy, isLoose rhythm setting per state, spacing
          - Design tokens: color, opacity, spacing, corner radius values referenced
          - Text-transform approach: CSS-based (letterSpacing, textDecoration) vs string mutation (.uppercase()) — note which the design uses per element
          - State machines: for every documented state transition, identify ALL states and ALL transitions between them — both directions. A state machine documented as "A → B when condition" implies "B → A when condition reversed" and BOTH directions require explicit ACs.
          Note the DESIGN.md section (system or journey) or hifi element that is the source for each extracted detail.
        </action>

        <action>Compose a `## Design Fidelity Acceptance Criteria` section:
          - Open with: "These ACs are generated from DESIGN.md and hifi sources. Each AC is implementation-level and requires visual review in a running build — behavioral tests alone are insufficient to verify these."
          - One sub-section per touched canvas/component: `### <Canvas Name> — Design Fidelity ACs`
          - Group ACs within each sub-section by: Typography, Copy & Vocabulary, Layout & Rhythm, Design Tokens, State Variations
          - Each AC is a specific, testable implementation-level statement
          - Every AC ends with an explicit source reference: `(Source: DESIGN.md §<section heading>)` or `(Source: hifi.html #<element-id>)`
          - If a detail was ambiguous in DESIGN.md and resolved via hifi, mark it: `(Source: hifi.html — DESIGN.md ambiguous)`
          - For any AC that references a specific implementation symbol name (Composable name, enum value, class name), append: `⚠ Symbol name from story — verify against Compose source before implementing`
        </action>

        <action>Read {{story_file}} and inject the `## Design Fidelity Acceptance Criteria` section immediately after the `## Acceptance Criteria` section (or after the `## Story` section if no AC section exists yet). Save {{story_file}}.</action>
        <action>Count the individual ACs generated. Store {{design_fidelity_ac_count}}.</action>
        <action>Store {{design_fidelity_status}} = "{{design_fidelity_ac_count}} ACs injected across {{touched_canvases}} (sources: system DESIGN.md{{journey_design_md ? ' + journey DESIGN.md' : ''}}{{hifi_sources ? ' + hifi' : ''}})"</action>
        <output>**Design-fidelity ACs injected** — {{design_fidelity_status}}</output>
      </check>
    </check>
  </step>

  <step n="4" goal="Classify change types from story tasks">
    <action>Read the Tasks/Subtasks section of {{story_file}}</action>
    <action>Load ./references/change-types.md (used for both detection heuristics here and injection templates in Step 6)</action>
    <action>For each task, classify it as one of: `skill-instruction`, `script-code`, `rule-hook`, `config-structure`, `app-ui`, `agent-definition`, `script-cli`, `research-spike`, or `specification` — per the signals in change-types.md. If a task matches none of the detection signals, tag it as `unclassified` and note "No Momentum-specific guidance for this task — standard bmad-dev-story DoD applies."</action>
    <action>Produce a classification list: each task tagged with its change type (or `unclassified`). A story may contain multiple types.</action>
    <action>Store {{classification_list}}: the classification list produced above, with each task number/name and its assigned change type</action>
    <action>Store {{change_types_summary}}: e.g., "2 ui-component tasks, 1 config-structure task"</action>

    <action>Persist the classified change types to the story frontmatter so downstream
      sprint-planning steps can route on them (Step 4 Gherkin routing and Step 5 specialist
      assignment read `change_type` from frontmatter). Read {{story_file}}; in the YAML
      frontmatter set `change_type:` to the DISTINCT classified types (exclude `unclassified`),
      written as a YAML list. Preserve all other frontmatter. Write {{story_file}} back.
      Store {{change_type_list}} = that distinct list; store {{change_type_index_str}} =
      the list joined with " + " (e.g., "skill-instruction + config-structure"). If every task
      was `unclassified`, set {{change_type_list}} = [] and {{change_type_index_str}} = "".</action>

    <output>## Change Type Classification

{{classification_list}}
    </output>
  </step>

  <step n="5" goal="Select verification method from change-type routing">
    <action>Check whether `skills/momentum/references/rules/verification-standard.md` exists on disk</action>
    <check if="verification-standard.md does not exist on disk">
      <output>Cannot select verification method — verification-standard.md not found.
This story depends on `enforced-verification-rule-change-type-method-routing-harness-profile-requirement-adversarial-guard` being implemented first.</output>
      <action>HALT</action>
    </check>
    <action>Load `skills/momentum/references/rules/verification-standard.md`</action>
    <action>Read the change-type → verification-method routing table from Section 1 of verification-standard.md</action>
    <action>For each entry in {{classification_list}}, look up its change type in the routing table. Produce {{method_candidates}}: a list of (change-type, method) pairs. Skip any entries tagged `unclassified`.</action>

    <check if="all entries in {{classification_list}} are unclassified (no classified change types)">
      <ask>All tasks in this story are unclassified — no change type matched. What verification method should govern this story? (Refer to the routing table in `skills/momentum/references/rules/verification-standard.md` for available methods.)</ask>
      <action>Set {{verification_method}} = developer's selection</action>
      <goto anchor="write_method" />
    </check>

    <action>Filter {{method_candidates}}: remove any entries where change-type is `specification`. Specification tasks (document review) are always subsumed by the dominant method of the story's primary deliverable — a story with `skill-instruction` + `specification` tasks selects the `skill-instruction` method without escalation.</action>
    <action>Store {{resolved_methods}}: the distinct verification methods from the filtered {{method_candidates}} (deduplicated set of method values)</action>

    <check if="{{resolved_methods}} contains exactly one distinct method OR is empty after filtering (only specification tasks remained)">
      <check if="{{resolved_methods}} is empty">
        <action>Set {{verification_method}} = "document-review"</action>
        <note>All non-unclassified tasks were specification type. document-review is the method for pure specification stories.</note>
      </check>
      <check if="{{resolved_methods}} contains one method">
        <action>Set {{verification_method}} = that single method</action>
      </check>
      <note>No developer prompt — routing is unambiguous.</note>
    </check>

    <check if="{{resolved_methods}} contains two or more distinct methods">
      <ask>The change types in this story map to multiple verification methods:
{{method_candidates}}
Which method should govern this story's verification? Select the method for the story's primary deliverable. Use one of: skill-invoke, behavioral-trigger, bash, smoke, curl, document-review.</ask>
      <action>Set {{verification_method}} = developer's selection</action>
    </check>

    <anchor id="write_method" />
    <note>verification_method is written as an ADVISORY hint only — it is NOT the routing key
    that selects the verifier. The harness and conductor derive routing from change_type via the
    routing table in verification-standard.md. Sprint-planning Step 4 (Gherkin generation) uses
    change_type, not this field, to determine contract format. Any value written here must be a
    closed-enum token (skill-invoke | behavioral-trigger | bash | smoke | curl | document-review)
    — never a free-text description, legacy alias (eval/trigger/review/gherkin/skip), or
    space-containing string.</note>
    <action>Read the current content of {{story_file}}</action>
    <action>Locate the YAML frontmatter block (the `---` delimited header at the top of the file)</action>
    <action>Add or update the `verification_method_advisory:` field in the frontmatter with the value `{{verification_method}}`. Label it `verification_method_advisory` (not `verification_method`) to make clear this is informational, not the routing key used by the harness or conductor.</action>
    <action>Write the updated content back to {{story_file}}</action>
    <output>**Verification method (advisory):** `{{verification_method}}` — written as `verification_method_advisory` in frontmatter. Routing is derived from `change_type` at sprint-planning time.</output>
  </step>

  <step n="6" goal="Inject Momentum Implementation Guide into story Dev Notes">
    <action>Read the current content of {{story_file}}</action>
    <action>Locate the Dev Notes section (or Developer Context section — may vary by bmad-create-story template version)</action>
    <action>Using {{classification_list}} from Step 4, determine which change types are present and select only the corresponding templates from ./references/change-types.md.</action>
    <check if="skill-instruction tasks are present in {{classification_list}}">
      <action>Identify `{{SKILL_DIR}}` from the story's skill-instruction tasks — this is the directory name of the skill being created (e.g., if creating `skills/momentum/skills/foo/`, then `{{SKILL_DIR}}` = `foo`). Substitute this value in the skill-instruction template before injecting.</action>
    </check>
    <check if="app-ui tasks are present in {{classification_list}}">
      <action>Note that design-fidelity ACs were injected in Step 3 (if DESIGN.md was found). The app-ui template in Dev Notes should cross-reference those ACs as the authoritative implementation target for visual fidelity.</action>
    </check>
    <action>Compose the Momentum Implementation Guide section using the templates for all detected types in this story (from ./references/change-types.md)</action>
    <action>Inject the section at the END of the Dev Notes / Developer Context section, immediately before the Dev Agent Record section. If no Dev Agent Record section exists, inject at the end of the Dev Notes / Developer Context section.</action>

    <critical>The injected section MUST include:
      - Change type classification per task (exact task numbers and names)
      - Implementation approach per type (EDD steps for skill-instruction; TDD delegation for script-code; functional verification for rule-hook; direct+inspect for config-structure; visual verification + design-fidelity AC compliance for app-ui; direct authoring with cross-reference verification for specification)
      - NFR compliance requirements for any skill-instruction tasks
      - DoD additions specific to this story's change types
      - A reminder that a frozen verification contract exists for this sprint (in sprints/{sprint-slug}/specs/{story-slug}.{ext}). Dev reads the Part-A header (how_dev_self_checks, verification_method, harness_profile) as a self-check before signaling done. Dev never reads the verifier body (Part B: scenarios, assertion scripts, Gherkin) beyond sections explicitly referenced by how_dev_self_checks.
    </critical>

    <action>Save {{story_file}} with the injected section</action>
    <output>**Momentum Implementation Guide** injected into `{{story_file}}`</output>
  </step>

  <step n="7" goal="Write story metadata to stories/index.json">
    <!-- DEC-034 D6: read epic context from epics.json keyed by epic_slug, not from epics.md narrative -->

    <!-- Guard: epic_slug must be present in story frontmatter -->
    <check if="{{story_file}} frontmatter has no epic_slug field OR epic_slug is blank">
      <output>**Error:** Story `{{story_key}}` has no `epic_slug` in its frontmatter.
Set `epic_slug:` in the story's YAML header before indexing. Use `ad-hoc` as the catch-all
value for stories that do not belong to a named epic.</output>
      <action>HALT</action>
    </check>
    <action>Store {{epic_slug}} = the `epic_slug` value from {{story_file}} frontmatter</action>

    <!-- Load epics.json and resolve the epic record for this story -->
    <action>Load `{{planning_artifacts}}/epics.json` as JSON</action>
    <check if="epics.json does not contain a record keyed by {{epic_slug}}">
      <output>**Error:** Epic `{{epic_slug}}` was not found in `{{planning_artifacts}}/epics.json`.
Either add the epic record to `epics.json` (run `momentum:epic-grooming`) or correct the
`epic_slug` value in the story frontmatter.</output>
      <action>HALT</action>
    </check>
    <action>Store {{epic_record}} = the JSON record at `epics.json["{{epic_slug}}"]`</action>

    <!-- Write epic provenance into the story file BODY (not just index.json/frontmatter) so the
         generated story cites the epic it was routed under. Eval contract b2 Scenario 5 requires
         the story body's References subsection to name the source epic. -->
    <action>Read the current content of {{story_file}}</action>
    <action>Locate the `### References` subsection within the Dev Notes section. If a `### References`
    subsection does not exist, create one at the end of the Dev Notes section (add the `### References`
    heading immediately before the next `##`-level heading, or at end of file if Dev Notes is the last section).</action>
    <action>Append this citation bullet to the `### References` subsection (do not duplicate if an identical
    line already exists):
      `- Epic context: \`{{epic_slug}}\` (from _bmad-output/planning-artifacts/epics.json)`
    </action>
    <action>Write the updated content back to {{story_file}}</action>
    <output>**Epic provenance** cited in `{{story_file}}` body — References → `{{epic_slug}}`</output>

    <!-- Extract depends_on: check epic stories array for cross-references, fall back to [] -->
    <action>Scan {{epic_record}}.stories array for any story object with a non-empty `depends_on`
field whose slugs match other entries in `stories/index.json`. Also scan
{{epic_record}}.system_context and {{epic_record}}.acceptance_conditions for explicit
"depends on Story X" or "requires Story X" language. Collect matching story slugs as
{{depends_on}}. If none found, set {{depends_on}} = [].</action>

    <!-- Extract touches: derive skill directories and config paths from system_context -->
    <action>Scan {{epic_record}}.system_context for skill directory paths
(e.g., `skills/momentum/skills/foo/`), shared config files, or other path references.
Collect these as {{touches}} (e.g., ["skills/momentum/skills/dev/", ".claude/settings.json"]).
If no paths are identifiable, set {{touches}} = [].</action>

    <!-- Preserve real edges: union epic-derived metadata with the story frontmatter so an
         enriched story never loses a depends_on edge or touches path it already declares. -->
    <action>Read the story frontmatter `depends_on` and `touches` (if present). Set
{{depends_on}} = the de-duplicated UNION of {{depends_on}} and the frontmatter `depends_on`.
Set {{touches}} = the de-duplicated UNION of {{touches}} and the frontmatter `touches`.
NEVER drop an edge or path the story file already declares.</action>

    <action>Read `.momentum/stories/index.json`</action>
    <critical>The index `change_type` is the STRING `{{change_type_index_str}}` — never the
      YAML list `{{change_type_list}}` (that list goes ONLY to the story frontmatter in Step 4).
      The two variables are near-identical but opposite-typed; do not swap them. The index entry
      is the consumer for `compute-verification-method`, which expects a "+"-joined string.</critical>
    <critical>The `depends_on`/`touches` union in this step is intentionally ADDITIVE — it never
      drops an edge or path. A developer-removed edge can therefore reappear on a re-enrichment
      pass; that is by design (the story file frontmatter is treated as the floor of truth).</critical>
    <action>Add or update the entry keyed by {{story_key}} with:
      - status: "ready-for-dev"
      - title: human-readable title derived from story key
      - epic_slug: {{epic_slug}}
      - story_file: true
      - change_type: {{change_type_index_str}}   (STRING form, e.g. "skill-instruction + config-structure")
      - depends_on: {{depends_on}}
      - touches: {{touches}}
    </action>
    <action>Save stories/index.json, preserving ALL existing entries</action>
    <output>**Story metadata written** to `stories/index.json` — `depends_on`: {{depends_on}}, `touches`: {{touches}}</output>
  </step>

  <step n="8" goal="Run AVFL checkpoint on the story file">
    <action>Invoke the `avfl` skill with these parameters:
      - domain_expert: "story author"
      - task_context: "Momentum story — {{story_key}}"
      - output_to_validate: full content of {{story_file}}
      - source_material: the epic record for {{story_key}}'s `epic_slug` from {{planning_artifacts}}/epics.json (the JSON record for {{epic_slug}}, serialized as pretty-printed JSON)
      - profile: checkpoint
      - stage: checkpoint
    </action>
    <note>We use the epic JSON record (not the story ACs) as source_material because AVFL checks whether the story spec correctly captures epic intent — the ACs are what we're validating and cannot be their own ground truth. The structured epic record from epics.json (DEC-034 D6) provides richer context than narrative prose from epics.md.</note>

    <check if="AVFL returns CLEAN">
      <action>Store {{avfl_result}} = "CLEAN"</action>
      <action>Store {{avfl_findings}} = ""</action>
    </check>

    <check if="AVFL returns CHECKPOINT_WARNING">
      <action>Store {{n}} = count of findings returned by AVFL</action>
      <action>Store {{avfl_result}} = "CHECKPOINT_WARNING ({{n}} findings)"</action>
      <action>Synthesize findings in plain language — severity indicators (! for critical, · for minor), brief descriptions. Do NOT dump raw AVFL JSON.</action>
      <action>Store {{avfl_findings}} = [the synthesized plain-language findings from the step above]</action>
      <ask>AVFL found {{n}} issues in the story spec. Proceed to dev with known issues, or halt to address them first?</ask>
      <check if="user chooses halt">
        <action>HALT — user will address findings manually</action>
      </check>
    </check>

    <check if="AVFL returns GATE_FAILED">
      <action>Store {{avfl_result}} = "GATE_FAILED"</action>
      <action>Store {{n}} = count of findings returned by AVFL</action>
      <action>Synthesize findings in plain language — severity indicators (! for critical, · for minor), brief descriptions. Do NOT dump raw AVFL JSON.</action>
      <action>Store {{avfl_findings}} = [the synthesized plain-language findings from the step above]</action>
      <output>AVFL GATE FAILED on story {{story_key}} — {{n}} critical issues found. The story spec has defects that should be addressed before development begins:
{{avfl_findings}}

You may proceed to development with known issues, or halt to address them first.</output>
      <ask>Proceed to development with known story spec issues, or halt to fix the story spec first?</ask>
      <check if="user chooses halt">
        <action>HALT — user will address story spec findings before proceeding to dev</action>
      </check>
    </check>

    <check if="AVFL returns unexpected status or errors">
      <action>Store {{avfl_result}} = "UNKNOWN — {{avfl_status}}"</action>
      <action>Store {{avfl_findings}} = ""</action>
      <ask>AVFL returned an unexpected result. Here is the raw output: {{avfl_raw_output}}. Proceed to review anyway, or halt?</ask>
    </check>
  </step>

  <step n="9" goal="Completion signal">
    <output>## Story `{{story_key}}` — Ready for Review

**Produced:** `{{story_file}}`
**Sprint tracking:** `stories/index.json` (status: `ready-for-dev`, metadata: written)
**Change types:** {{change_types_summary}}
**Design fidelity:** {{ui_story == true ? design_fidelity_status : "N/A (non-UI story)"}}
**Verification method:** {{verification_method}}
**AVFL checkpoint:** {{avfl_result}}
{{avfl_findings}}

This story is yours to review and adjust. When ready: invoke `momentum:dev` to implement.</output>
  </step>

</workflow>
