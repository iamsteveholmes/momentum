# momentum:dev Workflow

**Goal:** Implement a Momentum story by resolving the target story and delegating implementation to bmad-dev-story, then returning implementation-complete output with a list of files changed.

**Role:** Pure implementer. Receives a story (explicit path or unblocked selection), delegates all implementation to bmad-dev-story, and reports what was changed. The story's Momentum Implementation Guide (injected by momentum:create-story) contains the developer's implementation instructions.

**Conductor owns everything else.** Worktree creation/lifecycle, lockfile handling, git mutation (merge, rebase, conflict resolution), worktree cleanup, and crash recovery are all Conductor responsibilities (spec sections 3, 6, 12). The dev agent does not touch any of those concerns — adding them back here would break the Conductor's single-owner model and the precondition for mid-flight escalation (DEC-035, DEC-036 D1).

---

## EXECUTION

<workflow>
  <critical>Do not re-implement bmad-dev-story logic. Delegate all implementation to that skill.</critical>
  <critical>Never read files under sprints/{sprint-slug}/specs/ or any .feature file. Gherkin specs are for verifier agents only (Decision 30 — black-box separation). The dev agent must implement against plain English ACs in the story file, not against Gherkin specs. This is a read barrier, not just a write barrier — dev agents must never access specs regardless of protected-paths.json policy.</critical>
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
  "test_results": {
    "tests_run": {{tests_run}},
    "outcome": "{{test_result}}"
  }
}
AGENT_OUTPUT_END
```
Where {{file_list}} is the comma-separated list of files from the story's File List section, {{tests_run}} is true|false, and {{test_result}} is "pass", "fail", or "not_run" — all captured in Step 2 from bmad-dev-story's Dev Agent Record.

If implementation failed (bmad-dev-story did not reach story status "review"), emit the failed variant instead:
```
AGENT_OUTPUT_START
{
  "status": "failed",
  "story_key": "{{story_key}}",
  "error": "{{error_description}}",
  "files_changed": [],
  "test_results": {
    "tests_run": false,
    "outcome": "not_run"
  }
}
AGENT_OUTPUT_END
```
    </action>

    <note>Terminal contract: implementation-complete + file_list. Nothing more. The Conductor owns all git mutation (merge, rebase, conflict resolution), worktree lifecycle, lockfile handling, and crash recovery per spec sections 3, 6, and 12. Relocating those authorities out of dev is the precondition for the Conductor to own the narrow, stakes-gated mid-flight escalation tier (DEC-036 D1).</note>
  </step>

</workflow>
