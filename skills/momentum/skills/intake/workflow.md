# momentum:intake Workflow

**Goal:** Capture a story idea from the current conversation into the backlog as a
stub file — preserving conversational context without the heavyweight create-story
pipeline.

**Role:** Lightweight story capture. Extract intent, populate stub template, write
stub file, add index entry. No analysis, no research, no subagents.

---

<workflow>

  <critical>Do NOT run: artifact analysis, web research, architecture deep-dive,
  change-type classification, AVFL checkpoint, or implementation guide injection.
  Intake is conversational capture only.</critical>

  <critical>The stub file status MUST be `backlog`. Never write `ready-for-dev`.</critical>

  <critical>Use `momentum-tools sprint story-add` to write the index entry.
  Never edit stories/index.json directly.</critical>

  <critical>Minimize tool calls: 1 read (slug conflict check), 1 write (stub file),
  1 bash (CLI index entry). No subagent spawns.</critical>

  <critical>Intake MUST run in the main working tree only. MUST NOT invoke
  EnterWorktree, ExitWorktree, or any `git worktree` command. Caller skills MUST NOT
  wrap intake in a worktree for collision protection. Rationale: `story-add` writes a
  brand-new unique slug key on every invocation — no concurrent-write collision risk
  exists, so worktree isolation provides no benefit and traps the stub inside a branch
  instead of landing it on main. Any number of concurrent intake invocations is safe:
  each generates a unique slug and `story-add` performs an atomic read-modify-write of
  `stories/index.json`.</critical>

  <step n="1" goal="Extract story context from conversation or caller">
    <action>Review the current conversation (or caller-provided context) for story information. Extract:
      - {{title}}: The story title (required — derive from conversation if not explicit)
      - {{description}}: The "why" and scope as described conversationally
      - {{user_role}}: The role in "As a..." (default: "developer" if not explicit)
      - {{action}}: The "I want..." part (derive from the described need)
      - {{benefit}}: The "so that..." part (derive from stated goal/pain)
      - {{rough_acs}}: Rough acceptance criteria from conversation — capture as-is,
        not polished. Use bullet points. Label clearly as rough/draft.
      - {{pain_context}}: Recurrence, workaround burden, forgetting risk, and any
        other rationale the user gave for why this matters
      - {{suggested_epic}}: Epic the user suggested or caller provided, if any
      - {{suggested_priority}}: Priority the user suggested (critical/high/medium/low),
        if any. Default to `low` if not mentioned.
      - {{feature_slug}}: Feature this story belongs to — from caller context or
        conversation. Leave blank if not provided or not determinable.
      - {{story_type}}: Story type classification — feature / maintenance / defect /
        exploration / practice. From caller or heuristic. Default: "feature".
    </action>

    <check if="title cannot be derived from conversation">
      <ask>What title should I use for this story?</ask>
    </check>
  </step>

  <step n="2" goal="Determine epic assignment">
    <check if="{{suggested_epic}} was provided by user">
      <action>Set {{epic_slug}} = {{suggested_epic}} (normalize to kebab-case)</action>
    </check>

    <check if="{{suggested_epic}} was NOT provided">
      <action>Read `_bmad-output/planning-artifacts/epics.md` to get the current epic list</action>
      <action>Based on the story description, identify the 1-2 best-fit epics</action>
      <output>Based on the story description, I'd recommend assigning this to:

**{{recommended_epic}}** — {{brief_reason}}

**Other options:** {{alternative_epics}}
      </output>
      <ask>Which epic should this story belong to? (or confirm {{recommended_epic}})</ask>
      <action>Set {{epic_slug}} = user's confirmed choice (normalize to kebab-case)</action>
    </check>
  </step>

  <step n="3" goal="Generate slug and check for conflicts">
    <action>Derive {{slug}} from {{title}}:
      - Lowercase the title
      - Replace spaces and underscores with hyphens
      - Strip all characters except lowercase letters, digits, and hyphens
      - Collapse multiple consecutive hyphens to one
      - Strip leading/trailing hyphens
      - Truncate to 60 characters at a word boundary
    </action>

    <action>Read `.momentum/stories/index.json`</action>

    <check if="{{slug}} already exists in stories/index.json">
      <output>> **Slug conflict:** `{{slug}}` already exists in the story index (existing title: {{existing_title}}).
      </output>
      <ask>Please suggest an alternative slug or title for this story.</ask>
      <action>Re-derive {{slug}} from the user's alternative and re-check for conflicts</action>
    </check>
  </step>

  <step n="4" goal="Populate stub template and write stub file">
    <action>Load `./references/stub-template.md`</action>
    <action>Substitute all template variables:
      - {{slug}} → story slug
      - {{title}} → story title
      - {{epic_slug}} → confirmed epic slug
      - {{user_role}} → extracted user role (or "developer")
      - {{action}} → extracted "I want..." action
      - {{benefit}} → extracted "so that..." benefit
      - {{description}} → full conversational description of why and scope
      - {{pain_context}} → pain context from conversation
      - {{rough_acs}} → rough ACs captured as bullet points, prefixed with:
          "The following are rough draft ACs captured from conversation:"
      - {{feature_slug}} → feature_slug if provided, else empty string
      - {{story_type}} → story_type if provided, else "feature"
    </action>

    <action>Determine stub file path:
      {{stub_path}} = `.momentum/stories/{{slug}}.md`
    </action>

    <action>Write the populated stub to {{stub_path}}</action>

    <action>Add the index entry via CLI:
      ```
      python3 skills/momentum/scripts/momentum-tools.py sprint story-add \
        --slug "{{slug}}" \
        --title "{{title}}" \
        --epic "{{epic_slug}}" \
        --priority "{{suggested_priority}}" \
        {{if feature_slug is non-empty: --feature-slug "{{feature_slug}}"}} \
        {{if story_type is non-empty: --story-type "{{story_type}}"}}
      ```
    </action>

    <check if="CLI returns an error">
      <output>Failed to write index entry: {{cli_error}}</output>
      <action>HALT — report the error to the user</action>
    </check>

    <!-- SPIKE: beads dual-write — route discovered work via discovered-from edge -->
    <action>[SPIKE: beads] If `.beads/` directory exists:
      1. Determine the origin bead ID:
         - If a source story slug is known from context (the story that prompted this discovery):
           Load `.momentum/beads-id-map.json` and look up the source slug.
           If found: set {{origin_bead_id}} = the mapped bead ID.
         - If no source slug or not found in map: set {{origin_bead_id}} = `bd-discovery-root`
           (a sentinel bead; create it if it does not yet exist: `bd create "Discovery Root" --type epic`)
      2. Call: `bd create "{{title}}" --deps discovered-from:{{origin_bead_id}}`
         Note: `discovered-from` is semantically distinct from `blocks` — it means "this work
         was surfaced while working on the origin bead", not "this blocks the origin bead".
      3. If `bd create` succeeds: store the new bead ID in `.momentum/beads-id-map.json`
         as `{ "{{slug}}": "<new-bead-id>" }` (merge, don't overwrite other entries).
      4. If `bd create` fails: log to `.momentum/beads-errors.log` — do NOT abort.
         The `practice-ledger.jsonl` append above remains the source of record.
      5. Verify: `bd show <new-bead-id>` should show `discovered-from: {{origin_bead_id}}`
         (not `blocks:`) — this confirms the correct edge type.
    </action>
  </step>

  <step n="5" goal="Report what was captured and what still needs enrichment">
    <output>## Story Captured to Backlog

**Stub file:** `{{stub_path}}`
**Story slug:** `{{slug}}`
**Epic:** `{{epic_slug}}`
**Priority:** `{{suggested_priority}}`
**Status:** `backlog`

## What Intake Captured
- Title, description, user story statement
- Pain context: {{pain_context_summary}}
- Rough ACs (draft — need refinement)

## What Still Needs Enrichment
- **Acceptance Criteria** — rough ACs need refinement and validation
- **Tasks/Subtasks** — not yet analyzed or planned
- **Dev Notes** — no architecture analysis performed
- **Testing requirements** — not defined
- **Implementation guide** — not injected

> **Next step:** When ready to develop this story, run `momentum:create-story` on `{{stub_path}}` to enrich it with full analysis and make it dev-ready.
    </output>
  </step>

</workflow>
