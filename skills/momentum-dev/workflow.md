# momentum-dev Workflow

**Goal:** Implement a Momentum story by selecting the next unblocked story (or using an explicit path), running in an isolated git worktree, delegating to bmad-dev-story, then applying AVFL quality gate and Momentum-specific DoD.

**Role:** Thin orchestrator with sprint awareness. Manages story selection from sprint-status.yaml, worktree lifecycle, and merge gate. The story's Momentum Implementation Guide (injected by momentum-create-story) contains the developer's implementation instructions.

---

## EXECUTION

<workflow>
  <critical>Do not re-implement bmad-dev-story logic. Delegate all implementation to that skill.</critical>
  <critical>AVFL runs on the PRIMARY ARTIFACT (the finished SKILL.md, rule file, or config) — not the story file itself.</critical>
  <critical>If the story does not have a Momentum Implementation Guide section, warn the user: the story was likely created with bmad-create-story directly rather than momentum-create-story. Offer to run the injection step manually before proceeding.</critical>
  <critical>Always create a git worktree for every story session — even if this appears to be the only active session. This prevents mid-session file-change races.</critical>
  <critical>Never auto-execute git merge. Always propose the merge command and wait for explicit user confirmation before running it.</critical>
  <critical>Always write status changes to sprint-status.yaml in the MAIN working tree — not inside the worktree. This ensures all concurrent sessions see the update immediately.</critical>

  <step n="1" goal="Capture target branch">
    <action>Run via Bash tool: `git branch --show-current`</action>
    <action>Store {{target_branch}} = the output of that command (e.g., "main")</action>
  </step>

  <step n="2" goal="Resolve story to develop">
    <action>Check: has the user provided an explicit story file path or story key?</action>

    <check if="explicit story path or key provided">
      <action>If a file path is provided, store {{story_file}} = the provided path</action>
      <action>Read sprint-status.yaml from `{implementation_artifacts}/sprint-status.yaml`</action>
      <action>If a story key is provided, look up {{story_key}} in `momentum_metadata` to get `story_file`. If a file path was provided, find the matching story key by scanning `momentum_metadata` entries for a matching `story_file` value.</action>
      <action>Store {{story_key}} and {{story_file}}</action>
    </check>

    <check if="no story path or key provided">
      <action>Read sprint-status.yaml from `{implementation_artifacts}/sprint-status.yaml`</action>
      <action>Parse `development_status`: collect all story keys (exclude epic keys like `epic-N`, retrospective keys like `epic-N-retrospective`) and their statuses</action>
      <action>Parse `momentum_metadata`: for each story key, read `depends_on`, `touches`, `story_file`</action>
      <action>Filter to candidate stories: `development_status[key] == "ready-for-dev"` AND every key in `momentum_metadata[key].depends_on` has `development_status == "done"`</action>
      <check if="no candidates found">
        <action>Build a status summary: (1) for each story with status `in-progress`, list it as 'in progress in another session'; (2) for each story with status `ready-for-dev` whose `depends_on` includes any key not yet `done`, list: key → blocked on [list of incomplete depends_on keys]. If a depends_on key is `in-progress`, note it as `in-progress (will unblock when done)`.</action>
        <output>No unblocked stories are available. Current story status:
[status summary]

Resolve blocking stories first, then re-invoke momentum-dev.</output>
        <action>HALT</action>
      </check>
      <action>From the candidates, select the highest-priority story using this order:
        1. Epic sprint assignment: Day 1 stories first, then Sprint 1, Sprint 2, Growth
        2. Story order within that epic (parse from key: `1-2-...` → epic 1, story 2)
      </action>
      <action>Store {{story_key}} = selected story key</action>
      <action>Store {{story_file}} = `momentum_metadata[{{story_key}}].story_file`. If absent or null, fall back to `{implementation_artifacts}/{{story_key}}.md`.</action>
      <output>Selected story {{story_key}} (status: ready-for-dev, depends_on satisfied). Proceeding to develop.</output>
    </check>
  </step>

  <step n="3" goal="Crash recovery check">
    <action>Check if branch `story/{{story_key}}` already exists: run `git branch --list story/{{story_key}}`</action>
    <action>Check if worktree `.worktrees/story-{{story_key}}` already exists (check filesystem)</action>

    <check if="branch exists AND worktree directory exists">
      <ask>A previous session for Story {{story_key}} appears to be in progress (branch story/{{story_key}} + worktree .worktrees/story-{{story_key}} both exist). Resume from where it left off, or clean up and start fresh?

  R — Resume: continue in the existing worktree
  C — Clean up: delete branch and worktree, start fresh</ask>
      <check if="user chooses Resume">
        <action>Skip worktree creation (Step 4) — worktree already exists. Continue from Step 5.</action>
      </check>
      <check if="user chooses Clean up">
        <action>Run: `git worktree remove --force .worktrees/story-{{story_key}}`</action>
        <action>Run: `git branch -d story/{{story_key}}`</action>
        <action>Delete lock file `.worktrees/story-{{story_key}}.lock` if it exists</action>
        <action>Proceed to Step 4 (worktree creation).</action>
      </check>
    </check>

    <check if="branch exists but worktree directory does NOT exist">
      <action>Inform the user: "Stale branch story/{{story_key}} found without a worktree. This branch may have uncommitted development work. Force-deleting it."</action>
      <action>Run: `git branch -D story/{{story_key}}`</action>
      <action>Proceed to Step 4 (worktree creation).</action>
    </check>

    <check if="neither branch nor worktree exists">
      <action>Proceed to Step 4 (worktree creation).</action>
    </check>
  </step>

  <step n="4" goal="Create git worktree">
    <action>Run: `git worktree add .worktrees/story-{{story_key}} -b story/{{story_key}}`</action>
    <output>Worktree created at .worktrees/story-{{story_key}} on branch story/{{story_key}}</output>
  </step>

  <step n="5" goal="Mark story in-progress">
    <action>Write (or overwrite) the lock file `.worktrees/story-{{story_key}}.lock` in the main working tree (not inside the worktree). This is a plain text file; content: "locked by momentum-dev session started {{timestamp}}". Overwriting is safe — the new timestamp reflects the current session.</action>
    <action>Read sprint-status.yaml from `{implementation_artifacts}/sprint-status.yaml` in the main working tree</action>
    <action>Update `development_status[{{story_key}}]` to `in-progress` (idempotent — set regardless of current value)</action>
    <action>Update `last_updated` field to current date</action>
    <action>Save sprint-status.yaml, preserving ALL comments and structure</action>
    <output>Story {{story_key}} marked in-progress in sprint-status.yaml. Lock file created.</output>
  </step>

  <step n="6" goal="Invoke bmad-dev-story">
    <action>Enter the worktree context: use the EnterWorktree tool with path `.worktrees/story-{{story_key}}`. This sets the working directory to the worktree for all subsequent file operations until ExitWorktree is called. All bmad-dev-story file writes will land in the worktree, not the main tree.</action>

    <action>Invoke the `bmad-dev-story` skill inside the worktree `.worktrees/story-{{story_key}}`. Pass the story file path ({{story_file}}). bmad-dev-story will read the story's Dev Notes — including the Momentum Implementation Guide section — and implement accordingly.</action>

    <action>Wait for bmad-dev-story to complete fully (story status = "review")</action>
    <action>After bmad-dev-story completes, capture from its completion output:
      - {{story_key}}: the story key
      Then read {{story_file}} and extract:
      - {{file_list}}: from the story's File List section — files created/modified/deleted
    </action>

    <action>Exit the worktree context: use the ExitWorktree tool. This restores the working directory to the main repo root. All subsequent steps operate on the main tree.</action>

    <note>bmad-dev-story handles: story loading, sprint tracking, review continuation detection, task implementation loop, definition-of-done gate, story transition to review status. The Momentum Implementation Guide in the story tells it to use EDD for skill-instruction tasks rather than TDD.</note>
    <note>bmad-dev-story runs inside the worktree — all its file writes land in `.worktrees/story-{{story_key}}/`, isolated from other sessions.</note>
  </step>

  <step n="7" goal="AVFL quality gate on primary artifact">
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
      <action>Store {{primary_config_file}} = the most significant config file from {{file_list}} (e.g., the JSON file with the most fields, or the entry-point config)</action>
      <action>Invoke the `avfl` skill with:
        - domain_expert: "project engineer"
        - task_context: "Momentum config — {{primary_config_file}}"
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
      <action>GOTO step 8</action>
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
      <action>HALT — do not advance to Step 8 until GATE_FAILED findings are resolved and AVFL returns CLEAN or CHECKPOINT_WARNING</action>
    </check>
  </step>

  <step n="8" goal="Momentum-specific DoD supplement">
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
      - AVFL result is documented (written to Dev Agent Record in Step 7)
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

  <step n="9" goal="Mark story done and propose merge">
    <note>At this point the working directory is the main repo root (ExitWorktree was called at the end of Step 6). The merge runs on the main tree, merging story/{{story_key}} into {{target_branch}}.</note>
    <action>Read sprint-status.yaml from `{implementation_artifacts}/sprint-status.yaml` in the MAIN working tree</action>
    <action>Update `development_status[{{story_key}}]` to `done`</action>
    <action>Update `last_updated` field to current date</action>
    <action>Save sprint-status.yaml, preserving ALL comments and structure</action>
    <action>Delete the lock file `.worktrees/story-{{story_key}}.lock`</action>

    <action>Read `momentum_metadata[{{story_key}}].touches` from sprint-status.yaml</action>
    <action>Check for overlap: are any paths in {{touches}} also listed in `momentum_metadata` entries for other stories whose `development_status` is `in-progress`? If yes, note them as potential merge conflict paths. If no other in-progress stories, overlap = none.</action>
    <action>Store {{touches_overlap_summary}} = the result of the overlap check above. If overlapping paths were found, format as "Potential conflicts: [comma-separated list of overlapping paths]". If no other in-progress stories or no overlap, use "none".</action>

    <output>Story {{story_key}} is done and ready to merge.

  Branch:   story/{{story_key}}
  Target:   {{target_branch}}
  Touches overlap: {{touches_overlap_summary}}

To merge, run:
  git merge story/{{story_key}}

Confirm to proceed with merge, or review the diff first.</output>
    <ask>Run the merge now?</ask>

    <check if="user confirms merge">
      <action>Run: `git merge story/{{story_key}}`</action>
      <check if="merge succeeds cleanly">
        <action>Run: `git worktree remove --force .worktrees/story-{{story_key}}`
Note: Using --force because the merge has already succeeded — all work is safely on {{target_branch}}. Any uncommitted files in the worktree are discarded.</action>
        <action>Run: `git branch -d story/{{story_key}}`</action>
        <output>Merged and cleaned up worktree for Story {{story_key}}.</output>
      </check>
      <check if="merge reports conflicts">
        <output>Merge conflicts detected. Resolve conflicts in the affected files, then run:
  git add [resolved files]
  git merge --continue

After merge is complete, clean up the worktree:
  git worktree remove .worktrees/story-{{story_key}}
  git branch -d story/{{story_key}}</output>
        <action>HALT — do not auto-resolve conflicts. Wait for user to resolve and continue.</action>
      </check>
    </check>

    <check if="user declines merge">
      <output>Merge deferred. When ready:
  git merge story/{{story_key}}
  git worktree remove .worktrees/story-{{story_key}}
  git branch -d story/{{story_key}}</output>
    </check>
  </step>

  <step n="10" goal="Code review decision and final completion signal">
    <action>Check {{file_list}}: does it include any script files (.sh, .py, .ts, scripts/)?</action>

    <check if="script files present in file list">
      <ask>The story produced script changes. Would you like to run bmad-code-review on the diff? The story file can serve as the spec for full review mode. (Optional — not required.)</ask>
      <check if="user says yes">
        <action>Invoke the `bmad-code-review` skill. It will detect staged changes automatically.</action>
      </check>
    </check>

    <output>Story {{story_key}} complete.

Produced:
{{file_list}}

AVFL: {{avfl_result}}
Momentum DoD: all passed
Status: complete
Worktree: cleaned up</output>

    <action>Emit the structured completion signal (subagent output contract per Architecture Decision 3b):
{
  "status": "complete",
  "result": {
    "files_modified": [{{file_list}}],
    "tests_run": {{tests_run}},
    "test_result": "{{test_result}}"
  },
  "question": null,
  "confidence": "high"
}
Where: {{tests_run}} = true/false from bmad-dev-story's Dev Agent Record; {{test_result}} = "pass", "fail", or "not_run" from same source.
    </action>
  </step>

</workflow>
