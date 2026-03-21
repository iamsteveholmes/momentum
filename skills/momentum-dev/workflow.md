# momentum-dev Workflow

**Goal:** Implement a Momentum story by delegating to bmad-dev-story, then applying AVFL quality gate and Momentum-specific DoD.

**Role:** Thin orchestrator. The story's Momentum Implementation Guide (injected by momentum-create-story) already contains the developer's instructions. This skill reads the story, delegates implementation, then adds quality gates.

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
    <action>After bmad-dev-story completes, capture from its completion output:
      - {{story_file}}: the story file path
      - {{story_key}}: the story key
      Then read {{story_file}} and extract:
      - {{file_list}}: from the story's File List section — files created/modified/deleted
    </action>

    <note>bmad-dev-story handles: story loading, sprint tracking, review continuation detection, task implementation loop, definition-of-done gate, story transition to review status. The Momentum Implementation Guide in the story tells it to use EDD for skill-instruction tasks rather than TDD.</note>
  </step>

  <step n="2" goal="AVFL quality gate on primary artifact">
    <action>Load ./references/avfl-invocation.md to determine AVFL parameters</action>
    <action>Read the story's File List to identify what was produced</action>
    <action>Identify the primary artifact type from {{file_list}}:
      - If any SKILL.md or workflow.md files → skill-instruction artifact (including mixed skill+script stories)
      - If any .claude/rules/ files → rule-hook artifact
      - If only JSON configs, version files, directory structure → config-structure artifact
      - If only script files (.sh, .py, .ts) → script-code (skip AVFL)
    </action>

    <check if="primary artifact is skill-instruction">
      <action>Identify the main SKILL.md file from {{file_list}} as the artifact to validate</action>
      <action>Derive {{skill_name}} from the SKILL.md path in {{file_list}} — extract the directory name containing the SKILL.md (e.g., path `skills/momentum-create-story/SKILL.md` → {{skill_name}} = `momentum-create-story`)</action>
      <action>Invoke the `avfl` skill with:
        - domain_expert: "skill author"
        - task_context: "Momentum skill — {{skill_name}}"
        - output_to_validate: combined content of the produced SKILL.md and workflow.md (SKILL.md provides frontmatter and metadata; workflow.md contains the implementation)
        - source_material: the acceptance criteria section from {{story_file}}
        - profile: checkpoint
        - stage: final
      </action>
    </check>

    <check if="primary artifact is rule-hook">
      <action>Identify the primary rule or hook config file from {{file_list}}</action>
      <action>Derive {{rule_name}} from the rule file path in {{file_list}} — extract the filename (e.g., path `.claude/rules/model-routing.md` → {{rule_name}} = `model-routing.md`)</action>
      <action>Invoke the `avfl` skill with:
        - domain_expert: "practice engineer"
        - task_context: "Momentum rule — {{rule_name}}"
        - output_to_validate: full content of the produced file
        - source_material: acceptance criteria from {{story_file}}
        - profile: checkpoint
        - stage: final
      </action>
    </check>

    <check if="primary artifact is config-structure only">
      <action>Invoke the `avfl` skill with:
        - domain_expert: "project engineer"
        - task_context: "Momentum config — {{story_key}}"
        - output_to_validate: full content of the produced config file(s)
        - source_material: acceptance criteria from {{story_file}}
        - profile: gate
        - stage: final
      </action>
    </check>

    <check if="primary artifact is script-code only">
      <output>Script-code story — AVFL skipped. Tests provide correctness coverage for code.</output>
      <action>Set {{avfl_result}} = "skipped (script-code — tests are the quality gate)"</action>
      <action>Write the AVFL result to the Dev Agent Record in {{story_file}}: record avfl_result, profile used (N/A — skipped), and timestamp</action>
      <action>GOTO step 3</action>
    </check>

    <check if="AVFL returns CLEAN">
      <action>Store {{avfl_result}} = "CLEAN"</action>
      <action>Write the AVFL result to the Dev Agent Record in {{story_file}}: record avfl_result = CLEAN, profile used, and timestamp</action>
    </check>

    <check if="AVFL returns CHECKPOINT_WARNING">
      <action>Store {{avfl_result}} = "CHECKPOINT_WARNING"</action>
      <action>Write the AVFL result to the Dev Agent Record in {{story_file}}: record avfl_result = CHECKPOINT_WARNING, profile used, and timestamp</action>
      <action>Synthesize findings in plain language — severity indicators (! critical or high, · medium or low), brief descriptions per finding. Do NOT dump raw AVFL JSON.</action>
      <ask>AVFL found issues in the produced artifact. Address them now before closing, or proceed with known issues documented?</ask>
    </check>

    <check if="AVFL returns GATE_FAILED">
      <action>Store {{avfl_result}} = "GATE_FAILED"</action>
      <action>Write the AVFL result to the Dev Agent Record in {{story_file}}: record avfl_result = GATE_FAILED, profile used, and timestamp</action>
      <action>Synthesize findings in plain language — severity indicators (! critical or high, · medium or low), brief descriptions per finding. Do NOT dump raw AVFL JSON.</action>
      <output>AVFL GATE FAILED — story cannot proceed. The artifact has defects that must be resolved before closing. Address all findings and re-run AVFL.</output>
      <action>HALT — do not advance to Step 3 until GATE_FAILED findings are resolved and AVFL returns CLEAN or CHECKPOINT_WARNING</action>
    </check>
  </step>

  <step n="3" goal="Momentum-specific DoD supplement">
    <action>Load ./references/dod-checklist.md</action>
    <action>Determine which DoD sections apply based on change types in {{file_list}}</action>
    <action>Verify each applicable item. Items that bmad-dev-story already checked (tests passing, all tasks [x], File List complete, Dev Agent Record updated, Change Log updated) do not need re-verification — focus on Momentum-specific additions.</action>

    <action>For skill-instruction stories, verify:
      - Evals exist at skills/[name]/evals/ (check if directory has 2+ .md eval files)
      - EDD cycle completed (Dev Agent Record documents that evals were run and results recorded)
      - SKILL.md description is ≤150 characters (count the description field value)
      - model: and effort: frontmatter are present in the produced SKILL.md
      - Size compliance (SKILL.md body is under 500 lines; overflow is in references/ with load instructions)
      - Skill name prefix (skill name starts with momentum-)
      - AVFL result is documented (written to Dev Agent Record in Step 2)
    </action>

    <action>For rule-hook stories, verify:
      - Expected behavior was stated (a Given/result statement is present in the Dev Agent Record)
      - Verification was performed (Dev Agent Record documents how verification was conducted)
      - No duplicate hooks (if modifying settings.json, existing hooks were preserved and new entries merged not appended)
      - Format compliance (rule files follow .claude/rules/ markdown format; hook entries follow Agent Skills hooks schema)
    </action>

    <action>For config-structure stories, verify:
      - Any JSON files parse correctly (check that bmad-dev-story's verification noted this)
      - Required fields present (each required field documented in ACs is present with correct type)
      - Path existence (any referenced paths exist after the changes)
    </action>

    <check if="any Momentum DoD item fails">
      <output>⚠ Momentum DoD — FAILED
  Item: [state the exact checklist item that failed]
  Issue: [describe specifically what is wrong]
  Fix: [describe what needs to be done to resolve it]</output>
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
