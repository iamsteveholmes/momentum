# momentum-research Workflow

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
{{#each sub_questions}}
  - "{{this}}"
{{/each}}
---

# Research Scope: {{topic}}

**Date:** {{date}}
**Profile:** {{profile}}
**Goals:** {{goals}}

## Sub-Questions

{{numbered list of sub_questions}}
```

    <output>Research project created at {{project_dir}}. Profile: {{profile}}. {{count}} sub-questions defined.</output>
  </step>

  <step n="1.4" goal="Optional Gemini triangulation setup">
    <action>Check if gemini CLI is available: run `which gemini` via Bash</action>
    <check if="gemini is available">
      <ask>Gemini CLI detected. Would you like to generate a Gemini Deep Research prompt for external triangulation? (The prompt will be written to raw/gemini-prompt.md and you can choose to run it.)</ask>
      <check if="user says yes">
        <action>Load ./references/gemini-prompt-template.md</action>
        <action>Generate prompt by substituting {{topic}}, {{goals}}, {{sub_questions}}, {{date}}</action>
        <action>Write to {{project_dir}}/raw/gemini-prompt.md</action>
        <ask>Prompt written to raw/gemini-prompt.md. Run it now via `gemini -p`?</ask>
        <check if="user confirms">
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
      </check>
    </check>
    <check if="gemini is NOT available">
      <action>Skip Gemini — continue to Phase 2</action>
    </check>
  </step>

  <!-- ============================================================ -->
  <!-- PHASE 2: EXECUTE                                             -->
  <!-- ============================================================ -->

  <step n="2.1" goal="Resume detection — check for existing raw files">
    <action>List all files matching {{project_dir}}/raw/research-*.md</action>
    <action>For each sub-question in {{sub_questions}}, generate the expected filename: research-{{subtopic_slug}}.md</action>
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
      <action>Invoke momentum-avfl skill with:
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
      <action>Invoke momentum-avfl skill with:
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
      - {{project_dir}}/raw/gemini-output.md (if exists)
      - {{project_dir}}/validation/avfl-report.md (if exists)
      - {{project_dir}}/raw/practitioner-notes.md (if exists)
      - {{project_dir}}/scope.md
    </action>

    <action>Load ./references/output-structure.md for the default synthesis template</action>

    <action>Determine {{human_verified}}: true if practitioner-notes.md exists, false otherwise</action>

    <action>Build the derives_from chain:
      - Each raw/research-*.md → relationship: synthesized_from
      - raw/gemini-output.md (if present) → relationship: synthesized_from
      - validation/avfl-report.md (if present) → relationship: validated_by
      - raw/practitioner-notes.md (if present) → relationship: informed_by
    </action>

    <action>Spawn a SINGLE Opus subagent in the FOREGROUND (not background). Give it:</action>

    <critical>The synthesis agent must read ALL input files from disk — it receives file paths, not inline content. This gives it a clean 200K context window for synthesis, not polluted by the orchestrator's conversation history.</critical>

    Synthesis agent prompt:
    - Read all files listed above
    - Use the output structure template as a starting point, adapting sections to match the sub-questions from scope.md
    - Apply the evidence notation mapping (OFFICIAL→VERIFIED, PRAC→CITED, etc.)
    - Write the final document to: {{project_dir}}/final/{{topic_slug}}-final-{{date}}.md
    - Include the provenance frontmatter (content_origin, human_verified, derives_from chain)
    - Return a brief completion summary inline

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
