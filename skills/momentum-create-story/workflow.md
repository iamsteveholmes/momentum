# momentum-create-story Workflow

**Goal:** Create a Momentum story with change-type classification, injected implementation guidance, and AVFL validation.

**Role:** Story creation orchestrator for the Momentum project.
- Invoke `bmad-create-story` for all context extraction — do not re-implement its logic
- Classify change types from the story's tasks and inject Momentum-specific implementation guidance
- Run AVFL checkpoint before handing to developer

---

## INITIALIZATION

Load config from `{project-root}/_bmad/bmm/config.yaml` and resolve:
- `planning_artifacts`

---

## EXECUTION

<workflow>
  <critical>Do not duplicate bmad-create-story logic. Delegate all story creation to that skill.</critical>
  <critical>The Momentum Implementation Guide section you inject is the developer's authoritative guide — make it precise and actionable.</critical>

  <step n="1" goal="Invoke bmad-create-story">
    <action>Invoke the `bmad-create-story` skill. Pass through any story identifier, sprint context, or story path the user provided. Wait for full completion.</action>
    <action>After bmad-create-story completes, capture:
      - {{story_file}}: the output file path (from bmad-create-story's completion message)
      - {{story_key}}: the story key (e.g., "1-2-repository-structure")
    </action>
    <note>bmad-create-story handles: epic analysis, architecture extraction, web research, previous story intelligence, git analysis, Dev Notes population, sprint status update to "ready-for-dev". We own none of this.</note>
    <note>{{story_file}} is parsed from bmad-create-story's completion message. If it cannot be parsed (e.g., non-standard output format), derive it as `{{planning_artifacts}}/{{story_key}}.md` and continue.</note>
  </step>

  <step n="2" goal="Verify story file was written">
    <action>Confirm {{story_file}} exists and is non-empty</action>
    <check if="bmad-create-story halted or story file missing">
      <action>Set {{reason}} = "story file was not produced by bmad-create-story"</action>
      <output>Story creation did not complete — {{reason}}. No further action taken.</output>
      <action>HALT</action>
    </check>
  </step>

  <step n="3" goal="Classify change types from story tasks">
    <action>Read the Tasks/Subtasks section of {{story_file}}</action>
    <action>Load ./references/change-types.md (used for both detection heuristics here and injection templates in Step 4)</action>
    <action>For each task, classify it as one of: `skill-instruction`, `script-code`, `rule-hook`, or `config-structure` — per the signals in change-types.md. If a task matches none of the four detection signals, tag it as `unclassified` and note "No Momentum-specific guidance for this task — standard bmad-dev-story DoD applies."</action>
    <action>Produce a classification list: each task tagged with its change type (or `unclassified`). A story may contain multiple types.</action>
    <action>Store {{classification_list}}: the classification list produced above, with each task number/name and its assigned change type</action>
    <action>Store {{change_types_summary}}: e.g., "3 skill-instruction tasks, 1 config-structure task"</action>

    <output>Change type classification:
      {{classification_list}}
    </output>
  </step>

  <step n="4" goal="Inject Momentum Implementation Guide into story Dev Notes">
    <action>Read the current content of {{story_file}}</action>
    <action>Locate the Dev Notes section (or Developer Context section — may vary by bmad-create-story template version)</action>
    <action>Using {{classification_list}} from Step 3, determine which change types are present and select only the corresponding templates from ./references/change-types.md.</action>
    <check if="skill-instruction tasks are present in {{classification_list}}">
      <action>Identify `{{SKILL_DIR}}` from the story's skill-instruction tasks — this is the directory name of the skill being created (e.g., if creating `skills/momentum-foo/`, then `{{SKILL_DIR}}` = `momentum-foo`). Substitute this value in the skill-instruction template before injecting.</action>
    </check>
    <action>Compose the Momentum Implementation Guide section using the templates for all detected types in this story (from ./references/change-types.md)</action>
    <action>Inject the section at the END of the Dev Notes / Developer Context section, immediately before the Dev Agent Record section. If no Dev Agent Record section exists, inject at the end of the Dev Notes / Developer Context section.</action>

    <critical>The injected section MUST include:
      - Change type classification per task (exact task numbers and names)
      - Implementation approach per type (EDD steps for skill-instruction; TDD delegation for script-code; functional verification for rule-hook; direct+inspect for config-structure)
      - NFR compliance requirements for any skill-instruction tasks
      - DoD additions specific to this story's change types
    </critical>

    <action>Save {{story_file}} with the injected section</action>
    <output>Momentum Implementation Guide injected into {{story_file}}</output>
  </step>

  <step n="5" goal="Run AVFL checkpoint on the story file">
    <action>Invoke the `avfl` skill with these parameters:
      - domain_expert: "story author"
      - task_context: "Momentum story — {{story_key}}"
      - output_to_validate: full content of {{story_file}}
      - source_material: the relevant epic section for {{story_key}} from {{planning_artifacts}}/epics.md
      - profile: checkpoint
      - stage: checkpoint
    </action>
    <note>We use the epic section (not the story ACs) as source_material because AVFL checks whether the story spec correctly captures epic intent — the ACs are what we're validating and cannot be their own ground truth.</note>

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

    <check if="AVFL returns unexpected status or errors">
      <action>Store {{avfl_result}} = "UNKNOWN — {{avfl_status}}"</action>
      <action>Store {{avfl_findings}} = ""</action>
      <ask>AVFL returned an unexpected result. Here is the raw output: {{avfl_raw_output}}. Proceed to review anyway, or halt?</ask>
    </check>
  </step>

  <step n="6" goal="Completion signal">
    <output>Story {{story_key}} is yours to review.

Produced: {{story_file}}
Change types: {{change_types_summary}}
AVFL checkpoint: {{avfl_result}}
{{avfl_findings}}

This story is yours to review and adjust. When ready: invoke `momentum-dev` to implement.</output>
  </step>

</workflow>
