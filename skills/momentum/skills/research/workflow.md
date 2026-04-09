# momentum:research Workflow

**Goal:** Conduct structured deep research through a 6-phase pipeline producing validated, provenance-tracked research documents.

**Role:** Research orchestrator. You manage the pipeline — subagents do the research.

---

## PREREQUISITE

**Web search required.** If WebSearch is unavailable, abort and tell the user.

## INITIALIZATION

Load config via `bmad-init` skill (or directly from `{project-root}/_bmad/bmm/config.yaml`):
- `output_folder`, `user_name`, `communication_language`
- Set `research_root` = `{output_folder}/research/`
- Set `date` = today's date (YYYY-MM-DD)

---

## EXECUTION

<workflow>
  <critical>Research happens in subagents, not the main context. Never accumulate raw research findings in the orchestrator's context — subagents write to files, parent reads summaries.</critical>
  <critical>Every file written must include provenance frontmatter (content_origin, date). The final document must include a derives_from chain.</critical>
  <critical>Do not skip phases based on convenience. Light profile has explicit skip rules; medium and heavy run all phases.</critical>

  <!-- ============================================================ -->
  <!-- PHASE 1: SCOPE                                               -->
  <!-- ============================================================ -->

  <step n="1.1" goal="Elicit research topic and goals">
    <check if="An existing project directory path was provided by the user">
      <action>Read scope.md from the provided directory</action>
      <action>Present summary: topic, goals, sub-questions, profile</action>
      <action>Ask user: "Resume this research project, or start fresh?"</action>
      <check if="user says resume">
        <action>Store {{project_dir}}, {{topic}}, {{goals}}, {{sub_questions}}, {{profile}} from scope.md</action>
        <action>GOTO step 2.1 (resume detection)</action>
      </check>
    </check>

    <action>Ask the user: "What do you want to research? What decisions will this inform?"</action>
    <action>Store {{topic}} and {{goals}} from user response</action>
  </step>

  <step n="1.2" goal="Decompose into sub-questions">
    <action>Based on {{topic}} and {{goals}}, propose 4-8 sub-questions that collectively cover the research space</action>
    <action>Load ./references/profiles.md for profile definitions</action>
    <action>Present the sub-questions to the user for review and refinement</action>
    <action>Ask user to select profile: light (3 agents, fast), medium (5-6 agents, verified), or heavy (6-8 agents, full rigor). Default: medium.</action>
    <action>Store {{sub_questions}} (final list) and {{profile}}</action>
    <action>Adjust sub-question count to match profile: light=3, medium=5-6, heavy=6-8. If user provided more or fewer, offer to merge or split.</action>
  </step>

  <step n="1.3" goal="Create project directory and scope document">
    <action>Generate {{topic_slug}} from {{topic}} — lowercase, hyphens, max 40 chars</action>
    <action>Set {{project_dir}} = {research_root}/{{topic_slug}}-{{date}}/</action>
    <action>Create directories: {{project_dir}}, {{project_dir}}/raw/, {{project_dir}}/validation/, {{project_dir}}/final/</action>
    <action>Write {{project_dir}}/scope.md:</action>

```yaml
---
topic: "{{topic}}"
goals: "{{goals}}"
profile: {{profile}}
date: {{date}}
sub_questions:
  - "First sub-question text"
  - "Second sub-question text"
  - "Third sub-question text"
  # ... one entry per sub-question from step 1.2
---

# Research Scope: {{topic}}

**Date:** {{date}}
**Profile:** {{profile}}
**Goals:** {{goals}}

## Sub-Questions

1. First sub-question
2. Second sub-question
3. Third sub-question
(expand inline — one numbered entry per sub-question)
```

**Important:** Write the sub-questions inline as literal YAML strings and numbered list items. Do not use template loop syntax — expand each sub-question directly.

    <output>Research project created at {{project_dir}}. Profile: {{profile}}. {{count}} sub-questions defined.</output>
  </step>

  <step n="1.4" goal="Gemini triangulation — Deep Research via cmux-browser (with gemini -p fallback)">
    <!-- ── GATE 1: Check for existing output ──────────────────────────── -->
    <check if="{{project_dir}}/raw/gemini-deep-research-output.md exists OR {{project_dir}}/raw/gemini-output.md exists">
      <output>Gemini output already exists — skipping Gemini step.</output>
      <action>Continue to Phase 2</action>
    </check>

    <!-- ── GATE 2: Generate prompt (used by both paths) ──────────────── -->
    <action>Load ./references/gemini-prompt-template.md</action>
    <action>Generate prompt by substituting {{topic}}, {{goals}}, {{sub_questions}}, {{date}}</action>
    <action>Write to {{project_dir}}/raw/gemini-prompt.md</action>

    <!-- ── GATE 3: cmux availability check ───────────────────────────── -->
    <action>Check if cmux is available: run `which cmux` via Bash</action>
    <check if="cmux is NOT available">
      <!-- Degrade to gemini -p basic path -->
      <action>GOTO [[gemini-basic-fallback]]</action>
    </check>

    <!-- ── DEEP RESEARCH PATH (cmux available) ───────────────────────── -->

    <!-- Auth state load/verify/save -->
    <action>Set {{auth_state_path}} = ~/.claude/browser-state/google-auth.json</action>
    <action>Open browser surface to https://gemini.google.com via: cmux browser open https://gemini.google.com --json</action>
    <action>Capture {{surface}} from the JSON output (e.g. "surface:1")</action>
    <action>Wait for page load: cmux browser {{surface}} wait --load-state complete --timeout-ms 15000</action>

    <check if="~/.claude/browser-state/google-auth.json exists">
      <action>Load auth state: cmux browser {{surface}} state load ~/.claude/browser-state/google-auth.json</action>
      <action>Reload page to apply session: cmux browser {{surface}} reload</action>
      <action>Wait for page load: cmux browser {{surface}} wait --load-state complete --timeout-ms 15000</action>
    </check>

    <!-- Verify authentication via DOM inspection (not URL) -->
    <action>Snapshot the page: cmux browser {{surface}} snapshot --interactive</action>
    <action>Inspect DOM for auth status: cmux browser {{surface}} eval 'document.querySelectorAll("[aria-label*=\"Sign in\"], a[href*=\"accounts.google.com\"]").length'</action>
    <check if="sign-in elements found (count > 0)">
      <output>Not authenticated — no saved auth state or stale session detected.</output>
      <ask>Please log in to your Google account in the browser pane, then confirm when done.</ask>
      <action>Wait for user confirmation of login</action>
      <action>Verify auth again: cmux browser {{surface}} eval 'document.querySelectorAll("[aria-label*=\"Sign in\"], a[href*=\"accounts.google.com\"]").length'</action>
      <action>Create directory if needed: mkdir -p ~/.claude/browser-state/</action>
      <action>Save auth state: cmux browser {{surface}} state save ~/.claude/browser-state/google-auth.json</action>
      <output>Auth state saved to ~/.claude/browser-state/google-auth.json</output>
    </check>

    <!-- Ensure surface is wide enough for follow-up input to be visible -->
    <note>UI width requirement: Deep Research renders as a full-screen overlay at narrow widths, hiding the chat input. Maximize or widen the surface before starting to ensure follow-up input remains accessible after research completes.</note>

    <!-- Deep Research execution pipeline -->
    <action>Set {{dr_retry_count}} = 0</action>
    <action>Set {{dr_max_retries}} = 2</action>

    <!-- [[deep-research-attempt]] -->
    <action>Navigate to chat: cmux browser {{surface}} goto https://gemini.google.com</action>
    <action>Wait for page load: cmux browser {{surface}} wait --load-state complete --timeout-ms 15000</action>

    <!-- Enable Deep Research via Tools menu -->
    <action>Click Tools menu: cmux browser {{surface}} click "button[aria-label='Tools']" --snapshot-after</action>
    <action>Enable Deep Research checkbox via eval: cmux browser {{surface}} eval 'Array.from(document.querySelectorAll("[role=menuitemcheckbox]")).find(el => el.textContent.includes("Deep research"))?.click()'</action>
    <action>Close Tools menu if still open: cmux browser {{surface}} press Escape</action>

    <!-- Fill research prompt -->
    <action>Fill prompt: cmux browser {{surface}} fill "[contenteditable], textarea, [role=textbox]" "$(cat {{project_dir}}/raw/gemini-prompt.md)"</action>

    <!-- Submit -->
    <action>Click send: cmux browser {{surface}} eval 'Array.from(document.querySelectorAll("button")).find(b => b.getAttribute("aria-label")?.includes("Send") || b.textContent.trim() === "Send message")?.click()'</action>

    <!-- Poll for "Start research" button (plan generation) -->
    <note>Poll every 10 seconds for up to 3 minutes. If "Start research" button appears, auto-click it immediately without waiting for user approval.</note>
    <action>Poll for plan readiness: cmux browser {{surface}} wait --function 'Array.from(document.querySelectorAll("button")).some(b => b.textContent.includes("Start research"))' --timeout-ms 180000</action>

    <check if="plan generation times out (no 'Start research' button after 3 minutes)">
      <check if="{{dr_retry_count}} < {{dr_max_retries}}">
        <action>Increment {{dr_retry_count}} by 1</action>
        <output>Plan generation timed out. Reloading and retrying (attempt {{dr_retry_count}} of {{dr_max_retries}})...</output>
        <action>Reload page: cmux browser {{surface}} reload</action>
        <action>Wait for load: cmux browser {{surface}} wait --load-state complete --timeout-ms 15000</action>
        <action>GOTO [[deep-research-attempt]]</action>
      </check>
      <check if="{{dr_retry_count}} >= {{dr_max_retries}}">
        <output>Deep Research failed after {{dr_max_retries}} retries. Falling back to gemini -p basic mode.</output>
        <action>GOTO [[gemini-basic-fallback]]</action>
      </check>
    </check>

    <!-- Auto-approve the research plan -->
    <action>Click "Start research": cmux browser {{surface}} eval 'Array.from(document.querySelectorAll("button")).find(b => b.textContent.includes("Start research"))?.click()'</action>
    <output>Research plan approved — research underway.</output>

    <!-- Poll for research completion via text length stabilization -->
    <note>Poll every 30 seconds. Read the largest .markdown.markdown-main-panel element. If text length hasn't changed in 5 minutes, treat as stale and reload. Research is complete when text length > 10000 and stable (same value across two reads 30s apart).</note>
    <action>Initialize {{prev_length}} = 0, {{stable_since}} = now</action>
    <action>Loop: read cmux browser {{surface}} eval 'Math.max(0, ...Array.from(document.querySelectorAll(".markdown.markdown-main-panel")).map(el => el.textContent.length))'</action>
    <action>Store result as {{current_length}}</action>
    <check if="{{current_length}} == {{prev_length}} AND {{current_length}} > 10000">
      <action>Research complete — exit polling loop</action>
    </check>
    <check if="{{current_length}} == {{prev_length}} AND time since {{stable_since}} > 5 minutes">
      <output>Response stalled. Reloading page — completed report should reload from Gemini server-side state.</output>
      <action>Reload page: cmux browser {{surface}} reload</action>
      <action>Wait for load: cmux browser {{surface}} wait --load-state complete --timeout-ms 30000</action>
      <!-- Session recovery: if reload loses the conversation -->
      <action>Check if report text is present: cmux browser {{surface}} eval 'Math.max(0, ...Array.from(document.querySelectorAll(".markdown.markdown-main-panel")).map(el => el.textContent.length))'</action>
      <check if="report text NOT found (length == 0)">
        <note>Session recovery: open sidebar, find most recent conversation matching {{topic}}, click into it to recover the completed output.</note>
        <action>Snapshot sidebar: cmux browser {{surface}} snapshot --interactive</action>
        <action>Click the most recent conversation item whose text matches {{topic}}</action>
        <action>Wait for load: cmux browser {{surface}} wait --load-state complete --timeout-ms 15000</action>
      </check>
    </check>
    <action>Update {{prev_length}} = {{current_length}}; sleep 30s; continue polling</action>

    <!-- Extract report -->
    <action>Extract report text: cmux browser {{surface}} eval 'Array.from(document.querySelectorAll(".markdown.markdown-main-panel")).filter(el => el.textContent.length > 10000).sort((a,b) => b.textContent.length - a.textContent.length)[0]?.textContent'</action>
    <action>Store as {{deep_research_report}}</action>

    <!-- Write output with provenance frontmatter -->
    <action>Write {{project_dir}}/raw/gemini-deep-research-output.md with content:</action>

```yaml
---
content_origin: gemini-deep-research
date: {{date}}
topic: "{{topic}}"
method: cmux-browser
---
```

    <action>Append {{deep_research_report}} to the file after the frontmatter</action>
    <output>Gemini Deep Research output saved to raw/gemini-deep-research-output.md</output>

    <!-- Follow-up questions cycle (AC6) -->
    <note>AC6: After extracting the Deep Research report, send 2-3 targeted follow-up questions in the same Gemini conversation to probe gaps from scope.md sub-questions thinly covered. Each response is appended under a ## Follow-Up section. Ensure the surface is wide enough that the chat input is visible alongside the report panel before submitting follow-ups.</note>
    <action>Review sub-questions from scope.md against report content. Identify 2-3 areas with thin coverage.</action>
    <action>Generate follow-up questions targeting those gaps.</action>
    <action>For each follow-up question:</action>
    <action>  Verify chat input is visible: cmux browser {{surface}} snapshot --interactive — confirm text input element is present</action>
    <check if="chat input NOT visible">
      <action>Widen browser surface or scroll to make input visible before proceeding</action>
    </check>
    <action>  Fill follow-up question: cmux browser {{surface}} fill "[contenteditable], textarea, [role=textbox]" "{{follow_up_question}}"</action>
    <action>  Submit: cmux browser {{surface}} eval 'Array.from(document.querySelectorAll("button")).find(b => b.getAttribute("aria-label")?.includes("Send") || b.textContent.trim() === "Send message")?.click()'</action>
    <action>  Poll for response: read last .markdown.markdown-main-panel element (not the main report one), check length stabilization (two reads 5s apart with same non-zero length)</action>
    <action>  Extract response text and append to raw/gemini-deep-research-output.md under ## Follow-Up section</action>

    <action>Continue to Phase 2</action>

    <!-- ── GEMINI -p BASIC FALLBACK ────────────────────────────────── -->
    <!-- [[gemini-basic-fallback]] -->
    <action>Check if gemini CLI is available: run `which gemini` via Bash</action>
    <check if="gemini is NOT available">
      <output>Neither cmux nor gemini CLI available — skipping Gemini triangulation. Continuing to Phase 2.</output>
      <action>Continue to Phase 2</action>
    </check>

    <check if="gemini is available">
      <ask>Gemini Deep Research via browser is unavailable. Would you like to run a basic Gemini prompt via `gemini -p` for triangulation instead?</ask>
      <check if="user says yes or confirms">
        <action>Run: gemini -p "$(cat {{project_dir}}/raw/gemini-prompt.md)" and capture output</action>
        <check if="gemini command fails or auth error">
          <output>Gemini auth failed. Run `! gemini` in the terminal to authenticate, then re-invoke.</output>
          <action>Continue to Phase 2 without Gemini output — it can be added later</action>
        </check>
        <check if="gemini succeeds">
          <action>Write output to {{project_dir}}/raw/gemini-output.md with frontmatter:</action>

```yaml
---
content_origin: gemini-cli
date: {{date}}
topic: "{{topic}}"
---
```

          <output>Gemini output saved to raw/gemini-output.md</output>
        </check>
      </check>
      <check if="user declines">
        <action>Continue to Phase 2 without Gemini output</action>
      </check>
    </check>
  </step>

  <!-- ============================================================ -->
  <!-- PHASE 2: EXECUTE                                             -->
  <!-- ============================================================ -->

  <step n="2.1" goal="Resume detection — check for existing raw files">
    <action>List all files matching {{project_dir}}/raw/research-*.md</action>
    <action>For each sub-question, derive {{subtopic_slug}}: take the first 3-5 significant words, lowercase, hyphens between words, max 30 chars. Example: "How does context compaction work?" → "context-compaction". This MUST match the slug used in step 2.2 for resume to work correctly.</action>
    <action>Generate the expected filename: research-{{subtopic_slug}}.md</action>
    <action>Compare: which expected files exist, which are missing</action>

    <check if="ALL expected files exist">
      <output>All {{count}} research files found. Skipping to Phase 3.</output>
      <action>GOTO step 3.1</action>
    </check>

    <check if="SOME files exist">
      <action>Store {{missing_subtopics}} = sub-questions without a corresponding raw file</action>
      <output>Found {{existing_count}} of {{total_count}} research files. Will research {{missing_count}} remaining subtopics.</output>
    </check>

    <check if="NO files exist">
      <action>Store {{missing_subtopics}} = all sub-questions</action>
    </check>
  </step>

  <step n="2.2" goal="Spawn research subagents for missing subtopics">
    <action>Load ./references/briefing-template.md</action>
    <action>For EACH sub-question in {{missing_subtopics}}:</action>
    <action>Generate the briefing by substituting: {{sub_question}}, {{topic}}, {{goals}}, {{date}}, {{output_file_path}} = {{project_dir}}/raw/research-{{subtopic_slug}}.md</action>

    <critical>Launch ALL subagents in a SINGLE message for maximum parallelism. Use the Agent tool with run_in_background: true for each. Each agent is general-purpose type with WebSearch access.</critical>

    <action>Wait for all background agents to complete. As each finishes, note its inline summary.</action>

    <output>All research subagents complete. {{count}} files written to raw/.</output>
  </step>

  <!-- ============================================================ -->
  <!-- PHASE 3: VERIFY                                              -->
  <!-- ============================================================ -->

  <step n="3.1" goal="AVFL corpus validation (profile-dependent)">
    <check if="{{profile}} == light">
      <output>Light profile — skipping AVFL verification. Proceeding to synthesis.</output>
      <action>GOTO step 5.1</action>
    </check>

    <action>Collect all file paths from {{project_dir}}/raw/*.md into {{corpus_files}} array</action>

    <check if="{{profile}} == medium">
      <action>Invoke momentum:avfl skill with:
        - corpus: true
        - profile: checkpoint
        - output_to_validate: {{corpus_files}}
        - domain_expert: "research analyst"
        - task_context: "Multi-document research corpus on {{topic}} ({{file_count}} files)"
        - stage: checkpoint
        - source_material: contents of {{project_dir}}/scope.md
      </action>
    </check>

    <check if="{{profile}} == heavy">
      <action>Invoke momentum:avfl skill with:
        - corpus: true
        - profile: full
        - output_to_validate: {{corpus_files}}
        - domain_expert: "research analyst"
        - task_context: "Multi-document research corpus on {{topic}} ({{file_count}} files)"
        - stage: final
        - source_material: contents of {{project_dir}}/scope.md
        - authority_hierarchy: {{corpus_files}} ordered by evidence quality (official docs first, community sources last)
      </action>
    </check>

    <action>Write AVFL output to {{project_dir}}/validation/avfl-report.md</action>
    <action>Store {{avfl_findings_summary}} for Phase 4</action>
    <output>AVFL validation complete. Report at validation/avfl-report.md.</output>
  </step>

  <!-- ============================================================ -->
  <!-- PHASE 4: Q&A                                                 -->
  <!-- ============================================================ -->

  <step n="4.1" goal="Practitioner Q&A (profile-dependent)">
    <check if="{{profile}} == light">
      <action>GOTO step 5.1</action>
    </check>

    <check if="no AVFL report exists at {{project_dir}}/validation/avfl-report.md">
      <output>No AVFL report available — skipping Q&A phase.</output>
      <action>GOTO step 5.1</action>
    </check>

    <action>Read {{project_dir}}/validation/avfl-report.md</action>
    <action>Extract: unresolved contradictions, low-confidence findings, corpus completeness gaps, claims with weak evidence</action>
    <action>Present these as targeted questions to the user — not generic, specifically derived from AVFL findings</action>
    <action>Capture user responses interactively</action>
    <action>Write all Q&A to {{project_dir}}/raw/practitioner-notes.md with frontmatter:</action>

```yaml
---
content_origin: human
date: {{date}}
topic: "{{topic}}"
---
```

    <output>Practitioner notes captured at raw/practitioner-notes.md</output>
  </step>

  <!-- ============================================================ -->
  <!-- PHASE 5: SYNTHESIZE                                          -->
  <!-- ============================================================ -->

  <step n="5.1" goal="Synthesize research into final document">
    <action>Collect all input file paths:
      - All {{project_dir}}/raw/research-*.md files
      - {{project_dir}}/raw/gemini-deep-research-output.md (if exists — Deep Research path)
      - {{project_dir}}/raw/gemini-output.md (if exists — gemini -p fallback path)
      - {{project_dir}}/validation/avfl-report.md (if exists)
      - {{project_dir}}/raw/practitioner-notes.md (if exists)
      - {{project_dir}}/scope.md
    </action>

    <action>Load ./references/output-structure.md for the default synthesis template</action>

    <action>Determine {{human_verified}}: true if practitioner-notes.md exists, false otherwise</action>

    <action>Build the derives_from chain:
      - Each raw/research-*.md → relationship: synthesized_from
      - raw/gemini-deep-research-output.md (if present) → relationship: synthesized_from
      - raw/gemini-output.md (if present) → relationship: synthesized_from
      - validation/avfl-report.md (if present) → relationship: validated_by
      - raw/practitioner-notes.md (if present) → relationship: informed_by
    </action>

    <action>Load ./references/synthesis-briefing-template.md</action>
    <action>Generate the synthesis briefing by substituting: {{topic}}, {{goals}}, {{profile}}, {{date}}, {{project_dir}}, {{topic_slug}}, the list of raw file paths, and {{human_verified}}</action>

    <action>Spawn a SINGLE Opus subagent in the FOREGROUND (not background). Pass the generated synthesis briefing as the agent prompt.</action>

    <critical>The synthesis agent must read ALL input files from disk — it receives file paths, not inline content. This gives it a clean 200K context window for synthesis, not polluted by the orchestrator's conversation history.</critical>

    <action>Confirm the final document was written</action>
    <output>Final research document at final/{{topic_slug}}-final-{{date}}.md</output>
  </step>

  <!-- ============================================================ -->
  <!-- PHASE 6: COMMIT                                              -->
  <!-- ============================================================ -->

  <step n="6.1" goal="Propose git commit">
    <action>List all files in {{project_dir}}/ recursively</action>
    <action>Propose commit message: docs(research): {{topic}} — {{profile}} profile, {{file_count}} sources</action>
    <action>Show the file list and commit message to the user</action>
    <ask>Stage and commit these research artifacts?</ask>
    <check if="user confirms">
      <action>git add {{project_dir}}/ && git commit with the proposed message</action>
      <output>Research committed. Project directory: {{project_dir}}</output>
    </check>
    <check if="user declines">
      <output>Commit deferred. Files are at {{project_dir}}/.</output>
    </check>
  </step>

</workflow>
