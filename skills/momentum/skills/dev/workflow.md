# momentum:dev Workflow

**Goal:** Implement a Momentum story by resolving the target story and delegating implementation to bmad-dev-story, then returning implementation-complete output with a list of files changed.

**Role:** Pure implementer. Receives a story (explicit path or unblocked selection), delegates all implementation to bmad-dev-story, and reports what was changed. The story's Momentum Implementation Guide (injected by momentum:create-story) contains the developer's implementation instructions.

**Conductor owns everything else.** Worktree creation/lifecycle, lockfile handling, git mutation (merge, rebase, conflict resolution), worktree cleanup, and crash recovery are all Conductor responsibilities (spec sections 3 and 6). The dev agent does not touch any of those concerns — adding them back here would break the Conductor's single-owner model and the precondition for mid-flight escalation (DEC-035, DEC-036 D1).

---

## EXECUTION

<workflow>
  <critical>Do not re-implement bmad-dev-story logic. Delegate all implementation to that skill.</critical>
  <critical>The verification contract is a two-part file at `.momentum/sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Dev reads only the Part-A header (the `# === VERIFICATION HEADER` YAML block) as a self-check. Dev never reads the verifier body (Part B: scenarios, assertion scripts, Gherkin, etc.) beyond sections explicitly referenced by `how_dev_self_checks`. Dev never writes, edits, appends to, or alters any part of the contract. Dev never chooses the verification method — it is given in Part A. Stakes classification and mid-flight escalation do not change this read surface; dev reads only Part A regardless of any stakes class or disposition active elsewhere in the flow.</critical>
  <critical>If the story does not have a Momentum Implementation Guide section, warn the user: the story was likely created with bmad-create-story directly rather than momentum:create-story. Offer to run the injection step manually before proceeding.</critical>

  <step n="1" goal="Resolve story to develop">
    <action>Check: has the user provided an explicit story file path or story key?</action>

    <check if="explicit story path or key provided">
      <action>If a file path is provided, store {{story_file}} = the provided path</action>
      <action>Read `.momentum/stories/index.json`</action>
      <action>If a story key is provided, look up {{story_key}} in stories/index.json. The story implementation file is at `.momentum/stories/{{story_key}}.md`. If a file path was provided, derive the story key from the filename.</action>
      <action>Store {{story_key}} and {{story_file}}</action>
    </check>

    <check if="no story path or key provided">
      <action>Read `.momentum/stories/index.json`</action>
      <action>Parse all story entries: each entry has slug (the key), status, depends_on, touches</action>
      <action>Filter to candidate stories: `status == "ready-for-dev"` AND every slug in `depends_on` has `status == "done"` in the same index</action>
      <check if="no candidates found">
        <action>Build a status summary: (1) for each story with status `in-progress`, list it as 'in progress in another session'; (2) for each story with status `ready-for-dev` whose `depends_on` includes any key not yet `done`, list: key → blocked on [list of incomplete depends_on keys]. If a depends_on key is `in-progress`, note it as `in-progress (will unblock when done)`.</action>
        <output>## No Unblocked Stories Available

> Resolve blocking stories first, then re-invoke `momentum:dev`.

**Current story status:**
[status summary]</output>
        <action>HALT</action>
      </check>
      <action>From the candidates, select the highest-priority story using this order:
        1. Epic sprint assignment: Day 1 stories first, then Sprint 1, Sprint 2, Growth
        2. Story order within that epic (parse from key: `1-2-...` → epic 1, story 2)
      </action>
      <action>Store {{story_key}} = selected story key</action>
      <action>Store {{story_file}} = `.momentum/stories/{{story_key}}.md`.</action>
      <output>> Selected story `{{story_key}}` (status: `ready-for-dev`, depends_on satisfied). Proceeding to develop.</output>
    </check>

  </step>

  <step n="2" goal="Invoke bmad-dev-story">
    <action>Invoke the `bmad-dev-story` skill. Pass the story file path ({{story_file}}). bmad-dev-story will read the story's Dev Notes — including the Momentum Implementation Guide section — and implement accordingly.</action>

    <action>Wait for bmad-dev-story to complete fully (story status = "review")</action>
    <action>After bmad-dev-story completes, capture:
      - {{story_key}}: the story key
      Then read {{story_file}} and extract:
      - {{file_list}}: from the story's File List section — files created/modified/deleted
      - {{tests_run}}: true if bmad-dev-story ran tests, false otherwise (from the Dev Agent Record or implementation output)
      - {{test_result}}: "pass", "fail", or "not_run" — the outcome of the test run (from the same source; use "not_run" if {{tests_run}} is false)
    </action>

    <note>bmad-dev-story handles: story loading, sprint tracking, review continuation detection, task implementation loop, definition-of-done gate, story transition to review status. The Momentum Implementation Guide in the story tells it to use EDD for skill-instruction tasks rather than TDD.</note>
    <note>Working directory: the Conductor spawns this agent already scoped to the story worktree (spec section 6 — 'Dev subagents write and commit inside their worktrees'). The dev agent neither creates nor enters/exits worktrees; bmad-dev-story writes and commits land in the Conductor-provided worktree automatically.</note>
  </step>

  <step n="2.5" goal="Part-A header self-check">
    <action>Locate the story's verification contract. Derive the sprint slug from context or read `.momentum/sprints/index.json` to find the active sprint. Look up the story's `verification_method` from the sprint assignment record (`.momentum/sprints/index.json` or the assignment JSON); the extension maps 1:1: eval_yaml→.eval.yaml, smoke_sh→.smoke.sh, trigger_md→.trigger.md, review_md→.review.md, gherkin→.feature. If the verification_method is unavailable, glob `.momentum/sprints/{sprint-slug}/specs/{{story_key}}.*` and take the single matching file (expect 0 or 1 result).</action>

    <check if="contract file exists AND contains a Part-A header (line starting with '# === VERIFICATION HEADER')">
      <action>Read the Part-A header block only — the YAML front-matter from `# === VERIFICATION HEADER` through the end of the YAML block. Extract the `how_dev_self_checks` prompt. Note: `how_dev_self_checks` is Part A's plain-language restatement of the observable acceptance target. It may explicitly reference observable clauses in the contract body (e.g., "the scenarios below") — those referenced clauses are Part-A-sanctioned and form part of your acceptance target alongside the prompt itself.</action>
      <action>Self-check: execute the directives in `how_dev_self_checks` against the just-built implementation in the current worktree, including any observable clauses the prompt explicitly references in the contract body. Hold the full acceptance target (prompt + any referenced clauses) alongside the story's plain-English ACs. Do not read beyond the sections explicitly referenced — the verifier body as a whole (scenarios not referenced by the prompt, assertion scripts, Gherkin) remains off-limits.</action>
      <output>**Part-A self-check:** Performed. `how_dev_self_checks` prompt executed; implementation satisfies all Part-A header requirements.</output>
      <action>Store {{part_a_self_check}} = "performed"</action>
    </check>

    <check if="no contract file found OR file has no Part-A header">
      <output>**Part-A self-check:** Skipped — no contract or no Part-A header available. Proceeding on story ACs.</output>
      <action>Store {{part_a_self_check}} = "skipped-no-contract"</action>
    </check>

    <note>Dev reads the Part-A header and any observable clauses explicitly referenced by `how_dev_self_checks`. Never read the verifier body beyond those referenced sections. Never write, edit, or alter any part of the contract. Stakes classification and mid-flight escalation do not change this read surface.</note>
    <note>No EnterWorktree/ExitWorktree is needed — the Conductor already scoped this agent to the story worktree. The self-check inspects the just-built implementation in the current working directory automatically.</note>
  </step>

  <step n="3" goal="Report implementation-complete">
    <output>## Story `{{story_key}}` — Implementation Complete

**Files changed:**
{{file_list}}

Implementation is done. The Conductor handles merge, worktree cleanup, and any recovery from here.
    </output>

    <action>Emit the structured completion signal:
```
AGENT_OUTPUT_START
{
  "status": "complete",
  "story_key": "{{story_key}}",
  "files_changed": [{{file_list}}],
  "part_a_self_check": "{{part_a_self_check}}",
  "test_results": {
    "tests_run": {{tests_run}},
    "outcome": "{{test_result}}"
  }
}
AGENT_OUTPUT_END
```
Where {{file_list}} is the comma-separated list of files from the story's File List section; {{part_a_self_check}} is "performed" or "skipped-no-contract" from Step 2.5; {{tests_run}} is true|false and {{test_result}} is "pass", "fail", or "not_run" — all captured in Step 2 from bmad-dev-story's Dev Agent Record.

If implementation failed (bmad-dev-story did not reach story status "review"), emit the failed variant instead. Populate files_changed with whatever files were committed before the failure (check git log in the worktree); use an empty array only if no commits were made:
```
AGENT_OUTPUT_START
{
  "status": "failed",
  "story_key": "{{story_key}}",
  "error": "{{error_description}}",
  "files_changed": [{{files_committed_before_failure_or_empty}}],
  "part_a_self_check": "{{part_a_self_check}}",
  "test_results": {
    "tests_run": false,
    "outcome": "not_run"
  }
}
AGENT_OUTPUT_END
```
    </action>

    <note>Terminal contract: implementation-complete + file_list. Nothing more. The Conductor owns all git mutation (merge, rebase, conflict resolution), worktree lifecycle, lockfile handling, and crash recovery per spec sections 3 and 6. Relocating those authorities out of dev is the precondition for the Conductor to own the narrow, stakes-gated mid-flight escalation tier (DEC-036 D1).</note>
  </step>

</workflow>
