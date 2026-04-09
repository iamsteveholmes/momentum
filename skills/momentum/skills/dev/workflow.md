# momentum:dev Workflow

**Goal:** Implement a Momentum story by selecting the next unblocked story (or using an explicit path), running in an isolated git worktree, delegating to bmad-dev-story, then returning merge-ready output.

**Role:** Pure executor with agent logging. Manages story selection from stories/index.json, worktree lifecycle, and merge gate. The story's Momentum Implementation Guide (injected by momentum:create-story) contains the developer's implementation instructions.

---

## EXECUTION

<workflow>
  <critical>Do not re-implement bmad-dev-story logic. Delegate all implementation to that skill.</critical>
  <critical>Never read files under sprints/{sprint-slug}/specs/ or any .feature file. Gherkin specs are for verifier agents only (Decision 30 — black-box separation). The dev agent must implement against plain English ACs in the story file, not against Gherkin specs. This is a read barrier, not just a write barrier — dev agents must never access specs regardless of protected-paths.json policy.</critical>
  <critical>If the story does not have a Momentum Implementation Guide section, warn the user: the story was likely created with bmad-create-story directly rather than momentum:create-story. Offer to run the injection step manually before proceeding.</critical>
  <critical>Always create a git worktree for every story session — even if this appears to be the only active session. This prevents mid-session file-change races.</critical>
  <critical>Never auto-execute git merge. Always propose the merge command and wait for explicit user confirmation before running it.</critical>
  <critical>Always write status changes to stories/index.json in the MAIN working tree — not inside the worktree. This ensures all concurrent sessions see the update immediately.</critical>

  <step n="1" goal="Capture target branch">
    <action>Run via Bash tool: `git branch --show-current`</action>
    <action>Store {{target_branch}} = the output of that command (e.g., "main")</action>
  </step>

  <step n="2" goal="Resolve story to develop">
    <action>Check: has the user provided an explicit story file path or story key?</action>

    <check if="explicit story path or key provided">
      <action>If a file path is provided, store {{story_file}} = the provided path</action>
      <action>Read `{implementation_artifacts}/stories/index.json`</action>
      <action>If a story key is provided, look up {{story_key}} in stories/index.json. The story implementation file is at `{implementation_artifacts}/{{story_key}}.md`. If a file path was provided, derive the story key from the filename.</action>
      <action>Store {{story_key}} and {{story_file}}</action>
    </check>

    <check if="no story path or key provided">
      <action>Read `{implementation_artifacts}/stories/index.json`</action>
      <action>Parse all story entries: each entry has slug (the key), status, depends_on, touches</action>
      <action>Filter to candidate stories: `status == "ready-for-dev"` AND every slug in `depends_on` has `status == "done"` in the same index</action>
      <check if="no candidates found">
        <action>Build a status summary: (1) for each story with status `in-progress`, list it as 'in progress in another session'; (2) for each story with status `ready-for-dev` whose `depends_on` includes any key not yet `done`, list: key → blocked on [list of incomplete depends_on keys]. If a depends_on key is `in-progress`, note it as `in-progress (will unblock when done)`.</action>
        <output>No unblocked stories are available. Current story status:
[status summary]

Resolve blocking stories first, then re-invoke momentum:dev.</output>
        <action>HALT</action>
      </check>
      <action>From the candidates, select the highest-priority story using this order:
        1. Epic sprint assignment: Day 1 stories first, then Sprint 1, Sprint 2, Growth
        2. Story order within that epic (parse from key: `1-2-...` → epic 1, story 2)
      </action>
      <action>Store {{story_key}} = selected story key</action>
      <action>Store {{story_file}} = `{implementation_artifacts}/{{story_key}}.md`.</action>
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
    <action>Write (or overwrite) the lock file `.worktrees/story-{{story_key}}.lock` in the main working tree (not inside the worktree). This is a plain text file; content: "locked by momentum:dev session started {{timestamp}}". Overwriting is safe — the new timestamp reflects the current session.</action>
    <output>Story {{story_key}} marked in-progress. Lock file created.</output>
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

  <step n="7" goal="Propose merge and clean up">
    <note>At this point the working directory is the main repo root (ExitWorktree was called at the end of Step 6). The merge runs on the main tree, merging story/{{story_key}} into {{target_branch}}.</note>
    <action>Delete the lock file `.worktrees/story-{{story_key}}.lock`</action>

    <action>Read `{implementation_artifacts}/stories/index.json` and look up {{story_key}}.touches</action>
    <action>Check for overlap: are any paths in {{touches}} also listed in other stories whose `status` is `in-progress` in stories/index.json? If yes, note them as potential merge conflict paths. If no other in-progress stories, overlap = none.</action>
    <action>Store {{touches_overlap_summary}} = the result of the overlap check above. If overlapping paths were found, format as "Potential conflicts: [comma-separated list of overlapping paths]". If no other in-progress stories or no overlap, use "none".</action>

    <output>Story {{story_key}} is done and ready to merge.

  Branch:   story/{{story_key}}
  Target:   {{target_branch}}
  Touches overlap: {{touches_overlap_summary}}

To merge, run:
  git rebase {{target_branch}} story/{{story_key}} && git merge story/{{story_key}}

Confirm to proceed with rebase and merge, or review the diff first.</output>
    <ask>Run the rebase and merge now?</ask>

    <check if="user confirms merge">
      <action>Rebase the story branch onto the latest target branch, then merge:
        Run: `git rebase {{target_branch}} story/{{story_key}}`
        Story branches are local-only (never pushed), so rebase is safe — no history-rewriting risk. This ensures the story branch includes all recent main changes (e.g., status updates from other merged stories) and conflicts are resolved before the merge.</action>
      <check if="rebase reports conflicts">
        <output>Rebase conflicts detected on story/{{story_key}}. Resolve conflicts in the affected files, then run:
  git rebase --continue

After rebase completes, the merge will proceed.</output>
        <action>HALT — wait for user to resolve rebase conflicts before continuing to merge</action>
      </check>
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
