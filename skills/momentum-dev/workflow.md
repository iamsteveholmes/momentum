# momentum-dev Workflow

**Goal:** Implement a Momentum story by selecting the next unblocked story (or using an explicit path), running in an isolated git worktree, delegating to bmad-dev-story, then applying AVFL quality gate and Momentum-specific DoD.

**Role:** Thin orchestrator with sprint awareness. Manages story selection from frontmatter status, worktree lifecycle, and merge gate. The story's Momentum Implementation Guide (injected by momentum-create-story) contains the developer's implementation instructions.

---

## EXECUTION

<workflow>
  <critical>Do not re-implement bmad-dev-story logic. Delegate all implementation to that skill.</critical>
  <critical>AVFL runs on the PRIMARY ARTIFACT (the finished SKILL.md, rule file, or config) — not the story file itself.</critical>
  <critical>If the story does not have a Momentum Implementation Guide section, warn the user: the story was likely created with bmad-create-story directly rather than momentum-create-story. Offer to run the injection step manually before proceeding.</critical>
  <critical>Always create a git worktree for every story session — even if this appears to be the only active session. This prevents mid-session file-change races.</critical>
  <critical>Never auto-execute git merge. Always propose the merge command and wait for explicit user confirmation before running it.</critical>
  <critical>Always write status changes (in_progress, complete) to the story spec in the MAIN working tree — not inside the worktree. This ensures all concurrent sessions see the update immediately.</critical>

  <step n="1" goal="Capture target branch">
    <action>Run via Bash tool: `git branch --show-current`</action>
    <action>Store {{target_branch}} = the output of that command (e.g., "main")</action>
  </step>

  <step n="2" goal="Resolve story to develop">
    <action>Check: has the user provided an explicit story file path?</action>

    <check if="explicit story path provided">
      <action>Store {{story_file}} = the provided path</action>
      <action>Read {{story_file}} frontmatter to extract {{story_id}} (from `story_id:` field)</action>
      <action>If {{story_id}} is not present in the frontmatter, derive it from the file name (e.g., `_bmad-output/stories/3.1.md` → {{story_id}} = "3.1")</action>
    </check>

    <check if="no story path provided">
      <action>Read all files in `_bmad-output/stories/` (glob: `_bmad-output/stories/*.md`)</action>
      <action>For each file, read its frontmatter fields: `story_id`, `status`, `depends_on`, `touches`</action>
      <action>Filter to candidate stories: `status == ready` AND every story_id in `depends_on` has `status == complete` in its own spec file</action>
      <check if="no candidates found">
        <action>Build a blocked-on summary: for each story with `status == ready` whose `depends_on` includes any story not yet `complete`, list: story_id → blocked on [list of incomplete depends_on ids]</action>
        <output>No unblocked stories available.

All remaining stories are blocked on:
[blocked-on summary]

Resolve blocking stories first, then re-invoke momentum-dev.</output>
        <action>HALT</action>
      </check>
      <action>From the candidates, select the highest-priority story using this order:
        1. Epic sprint assignment: Day 1 stories first, then Sprint 1, Sprint 2, Growth
        2. Story order within that epic (lower story_id number = higher priority)
      </action>
      <action>Store {{story_id}} = selected story's story_id</action>
      <action>Store {{story_file}} = `_bmad-output/stories/{{story_id}}.md` (read the `story_file:` frontmatter field if present for the full story path)</action>
      <output>Selected story {{story_id}} (status: ready, depends_on satisfied). Proceeding to develop.</output>
    </check>
  </step>

  <step n="3" goal="Crash recovery check">
    <action>Check if branch `story/{{story_id}}` already exists: run `git branch --list story/{{story_id}}`</action>
    <action>Check if worktree `.worktrees/story-{{story_id}}` already exists (check filesystem)</action>

    <check if="branch exists AND worktree directory exists">
      <ask>A previous session for Story {{story_id}} appears to be in progress (branch story/{{story_id}} + worktree .worktrees/story-{{story_id}} both exist). Resume from where it left off, or clean up and start fresh?

  R — Resume: continue in the existing worktree
  C — Clean up: delete branch and worktree, start fresh</ask>
      <check if="user chooses Resume">
        <action>Skip worktree creation (Step 4) — worktree already exists. Continue from Step 5.</action>
      </check>
      <check if="user chooses Clean up">
        <action>Run: `git worktree remove --force .worktrees/story-{{story_id}}`</action>
        <action>Run: `git branch -d story/{{story_id}}`</action>
        <action>Delete lock file `.worktrees/story-{{story_id}}.lock` if it exists</action>
        <action>Proceed to Step 4 (worktree creation).</action>
      </check>
    </check>

    <check if="branch exists but worktree directory does NOT exist">
      <action>Stale branch detected — deleting: `git branch -d story/{{story_id}}`</action>
      <action>Proceed to Step 4 (worktree creation).</action>
    </check>

    <check if="neither branch nor worktree exists">
      <action>Proceed to Step 4 (worktree creation).</action>
    </check>
  </step>

  <step n="4" goal="Create git worktree">
    <action>Run: `git worktree add .worktrees/story-{{story_id}} -b story/{{story_id}}`</action>
    <output>Worktree created at .worktrees/story-{{story_id}} on branch story/{{story_id}}</output>
  </step>

  <step n="5" goal="Mark story in-progress">
    <action>Create lock file `.worktrees/story-{{story_id}}.lock` in the main working tree (not inside the worktree). This is a plain text file; content: "locked by momentum-dev session started {{timestamp}}"</action>
    <action>Read `_bmad-output/stories/{{story_id}}.md` from the main working tree</action>
    <action>Update the `status:` frontmatter field from `ready` to `in_progress`</action>
    <action>Write the updated file back to `_bmad-output/stories/{{story_id}}.md` in the main working tree</action>
    <output>Story {{story_id}} marked in_progress. Lock file created.</output>
  </step>

  <step n="6" goal="Invoke bmad-dev-story">
    <action>Invoke the `bmad-dev-story` skill inside the worktree `.worktrees/story-{{story_id}}`. Pass the story file path ({{story_file}}). bmad-dev-story will read the story's Dev Notes — including the Momentum Implementation Guide section — and implement accordingly.</action>

    <action>Wait for bmad-dev-story to complete fully (story status = "review")</action>
    <action>After bmad-dev-story completes, capture from its completion output:
      - {{story_key}}: the story key
      Then read {{story_file}} and extract:
      - {{file_list}}: from the story's File List section — files created/modified/deleted
    </action>

    <note>bmad-dev-story handles: story loading, sprint tracking, review continuation detection, task implementation loop, definition-of-done gate, story transition to review status. The Momentum Implementation Guide in the story tells it to use EDD for skill-instruction tasks rather than TDD.</note>
    <note>bmad-dev-story runs inside the worktree — all its file writes land in `.worktrees/story-{{story_id}}/`, isolated from other sessions.</note>
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

  <step n="9" goal="Mark story complete and propose merge">
    <action>Read `_bmad-output/stories/{{story_id}}.md` from the MAIN working tree (not the worktree)</action>
    <action>Update the `status:` frontmatter field to `complete`</action>
    <action>Write the updated file back to `_bmad-output/stories/{{story_id}}.md` in the main working tree</action>
    <action>Delete the lock file `.worktrees/story-{{story_id}}.lock`</action>

    <action>Read {{touches}} from the story spec frontmatter</action>
    <action>Check for overlap: are any paths in {{touches}} also listed in other currently in_progress story specs' `touches` fields? If yes, note them as potential merge conflict paths. If no other in_progress stories, overlap = none.</action>

    <output>Story {{story_id}} is complete and ready to merge.

  Branch:   story/{{story_id}}
  Target:   {{target_branch}}
  Touches overlap: {{touches_overlap_summary}}

To merge, run:
  git merge story/{{story_id}}

Confirm to proceed with merge, or review the diff first.</output>
    <ask>Run the merge now?</ask>

    <check if="user confirms merge">
      <action>Run: `git merge story/{{story_id}}`</action>
      <check if="merge succeeds cleanly">
        <action>Run: `git worktree remove .worktrees/story-{{story_id}}`</action>
        <action>Run: `git branch -d story/{{story_id}}`</action>
        <output>Merged and cleaned up worktree for Story {{story_id}}.</output>
      </check>
      <check if="merge reports conflicts">
        <output>⚠ Merge conflicts detected. Resolve conflicts in the affected files, then run:
  git add [resolved files]
  git merge --continue

After merge is complete, clean up the worktree:
  git worktree remove .worktrees/story-{{story_id}}
  git branch -d story/{{story_id}}</output>
        <action>HALT — do not auto-resolve conflicts. Wait for user to resolve and continue.</action>
      </check>
    </check>

    <check if="user declines merge">
      <output>Merge deferred. When ready:
  git merge story/{{story_id}}
  git worktree remove .worktrees/story-{{story_id}}
  git branch -d story/{{story_id}}</output>
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
  </step>

</workflow>
