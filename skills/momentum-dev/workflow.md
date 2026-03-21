# momentum-dev Workflow

**Goal:** Implement a Momentum story by delegating to bmad-dev-story, then applying AVFL quality gate and Momentum-specific DoD.

**Role:** Thin orchestrator. The story's Momentum Implementation Guide (injected by momentum-create-story) already contains the developer's instructions. This skill reads the story, delegates implementation, then adds quality gates.

---

## INITIALIZATION

Load config from `{project-root}/_bmad/bmm/config.yaml` and resolve:
- `user_name`, `communication_language`
- `implementation_artifacts`

---

## EXECUTION

<workflow>
  <critical>Do not re-implement bmad-dev-story logic. Delegate all implementation to that skill.</critical>
  <critical>AVFL runs on the PRIMARY ARTIFACT (the finished SKILL.md, rule file, or config) — not the story file itself.</critical>
  <critical>If the story does not have a Momentum Implementation Guide section, warn the user: the story was likely created with bmad-create-story directly rather than momentum-create-story. Offer to run the injection step manually before proceeding.</critical>

  <step n="1" goal="Invoke bmad-dev-story">
    <action>Check: has the user provided a story file path?</action>
    <check if="story path provided">
      <action>Invoke the `bmad-dev-story` skill. Pass the story file path. bmad-dev-story will read the story's Dev Notes — including the Momentum Implementation Guide section — and implement accordingly.</action>
    </check>
    <check if="no story path provided">
      <action>Invoke the `bmad-dev-story` skill with no arguments. It will auto-discover the next ready-for-dev story from sprint-status.yaml.</action>
    </check>

    <action>Wait for bmad-dev-story to complete fully (story status = "review")</action>
    <action>Capture from bmad-dev-story's completion:
      - {{story_file}}: the story file path
      - {{story_key}}: the story key
      - {{file_list}}: files created/modified/deleted (from the story's File List section)
    </action>

    <note>bmad-dev-story handles: story loading, sprint tracking, review continuation detection, task implementation loop, definition-of-done gate, story closure. The Momentum Implementation Guide in the story tells it to use EDD for skill-instruction tasks rather than TDD.</note>
  </step>

  <step n="2" goal="AVFL quality gate on primary artifact">
    <action>Load ./references/avfl-invocation.md to determine AVFL parameters</action>
    <action>Read the story's File List to identify what was produced</action>
    <action>Identify the primary artifact type from {{file_list}}:
      - If any SKILL.md or workflow.md files → skill-instruction artifact
      - If any .claude/rules/ files → rule-hook artifact
      - If only JSON configs, version files, directory structure → config-structure artifact
      - If only script files (.sh, .py, .ts) → script-code (skip AVFL)
    </action>

    <check if="primary artifact is skill-instruction">
      <action>Identify the main SKILL.md file from {{file_list}} as the artifact to validate</action>
      <action>Invoke the `avfl` skill with:
        - domain_expert: "skill author"
        - task_context: "Momentum skill — {{skill_name}}"
        - output_to_validate: full content of the produced SKILL.md
        - source_material: the acceptance criteria section from {{story_file}}
        - profile: checkpoint
        - stage: final
      </action>
    </check>

    <check if="primary artifact is rule-hook">
      <action>Identify the primary rule or hook config file from {{file_list}}</action>
      <action>Invoke the `avfl` skill with:
        - domain_expert: "practice engineer"
        - task_context: "Momentum rule/hook — {{rule_name}}"
        - output_to_validate: full content of the produced file
        - source_material: acceptance criteria from {{story_file}}
        - profile: checkpoint
        - stage: final
      </action>
    </check>

    <check if="primary artifact is config-structure only">
      <action>Invoke the `avfl` skill with:
        - domain_expert: "project engineer"
        - task_context: "Momentum config/structure — {{story_key}}"
        - output_to_validate: description of what was created/modified
        - profile: gate
        - stage: final
      </action>
    </check>

    <check if="primary artifact is script-code only">
      <output>Script-code story — AVFL skipped. Tests provide correctness coverage for code.</output>
      <action>Set {{avfl_result}} = "skipped (script-code — tests are the quality gate)"</action>
      <action>GOTO step 3</action>
    </check>

    <check if="AVFL returns CLEAN">
      <action>Store {{avfl_result}} = "CLEAN"</action>
    </check>

    <check if="AVFL returns CHECKPOINT_WARNING or GATE_FAILED">
      <action>Store {{avfl_result}} = "CHECKPOINT_WARNING" or "GATE_FAILED"</action>
      <action>Synthesize findings in plain language — severity indicators (! critical, · minor), brief descriptions per finding. Do NOT dump raw AVFL JSON.</action>
      <ask>AVFL found issues in the produced artifact. Address them now before closing, or proceed with known issues documented?</ask>
    </check>
  </step>

  <step n="3" goal="Momentum-specific DoD supplement">
    <action>Load ./references/dod-checklist.md</action>
    <action>Determine which DoD sections apply based on change types in {{file_list}}</action>
    <action>Verify each applicable item. Items that bmad-dev-story already checked (tests passing, all tasks [x], File List complete, Dev Agent Record updated, Change Log updated) do not need re-verification — focus on Momentum-specific additions.</action>

    <action>For skill-instruction stories, verify:
      - Evals exist at skills/[name]/evals/ (check if directory has 2+ files)
      - SKILL.md description is ≤150 characters (count the description field value)
      - model: and effort: frontmatter are present in the produced SKILL.md
      - AVFL result is documented (it will be, from Step 2 output)
    </action>

    <action>For rule-hook stories, verify:
      - Expected behavior was stated and verified (check Dev Agent Record)
    </action>

    <action>For config-structure stories, verify:
      - Any JSON files parse correctly (check that bmad-dev-story's verification noted this)
    </action>

    <check if="any Momentum DoD item fails">
      <output>⚠ Momentum DoD — FAILED
        Failing item: {{item_description}}
        Required action: {{what_to_fix}}</output>
      <action>HALT — do not advance story until item is resolved</action>
    </check>

    <output>Momentum DoD — all items passed</output>
  </step>

  <step n="4" goal="Code review decision and completion signal">
    <action>Check {{file_list}}: does it include any script files (.sh, .py, .ts, scripts/)?</action>

    <check if="script files present in file list">
      <ask>The story produced script changes. Would you like to run bmad-code-review on the diff? The story file can serve as the spec for full review mode. (Optional — not required.)</ask>
      <check if="user says yes">
        <action>Invoke the `bmad-code-review` skill. It will detect staged changes automatically.</action>
      </check>
    </check>

    <output>Story {{story_key}} is yours to review.

Produced:
{{file_list}}

AVFL: {{avfl_result}}
Momentum DoD: all passed
Status: review

Next: bmad-code-review (if scripts remain), or close the story.</output>
  </step>

</workflow>
