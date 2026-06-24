# === VERIFICATION HEADER (Part A) ===
---
story_slug: nornspun-agent-constitution
verification_method: document-review
harness_profile: document-review
contract_path: .momentum/sprints/sprint-2026-06-18/specs/nornspun-agent-constitution.review.md
how_dev_self_checks: |
  Open the constitution document at its agreed path and read it top to bottom, then
  confirm each item below by direct inspection and a couple of shell commands:
    1. The file exists. Run `wc -l` on it and confirm the body is 150 lines or fewer.
    2. There is a "Project Invariants" section, and it names all five invariants:
       async-first (no blocking calls in async routes; long-running generation runs
       as background async tasks via an in-process task registry, not the web
       framework's built-in background-tasks helper), data-layer access through a
       storage backend abstraction (not ad-hoc direct database calls), an SSE event
       contract that separates conversation events from background-task events by
       documented type-name prefixes on one connection, snake_case JSON wire field
       names, and per-session cost-cap enforcement (e.g., a silence posture that
       suppresses extra evaluation model calls). Each invariant cites a nornspun
       source (architecture doc, a numbered decision, or a guideline).
    3. There is a "Cold KB pointer" section that names the vault path
       ~/projects/nornspun-agentic-kb, says WHEN to query it (unfamiliar API,
       pattern uncertainty, library-version questions), and includes a usable
       wiki-query interface block (a skill invocation or a vault-grep command).
    4. The document does NOT contain agent-specific file-pattern-to-role routing
       entries (e.g., a line mapping `*.kt` or `*.kts` globs to a named agent role).
    5. The document references the global CMUX layout rule at ~/.claude/rules/cmux.md
       rather than restating the layout.
    6. The document contains no Tier-2 specialist content (no Python-backend-dev,
       Kotlin/Compose-dev, or QA specialist body embedded in it).
    7. Every cited source path the document points at actually resolves on disk.
  Done means: file present, 150 lines or fewer, all five invariants present and
  sourced, KB pointer section complete, no agent routing entries, CMUX referenced
  not redefined, no Tier-2 content, and every cited path resolves.
coverage_disposition: dedicated-run
covered_by_scenario: null
acceptance_criteria_ref: .momentum/stories/nornspun-agent-constitution.md#acceptance-criteria
platforms: [host]
---

## Document Under Review

`/Users/steve/projects/nornspun/.claude/guidelines/constitution.md`

This document lives OUT OF the Momentum repository, in a separate project at
`/Users/steve/projects/nornspun`. Inspect it at the path above.

If implementation recorded a different agreed path (with rationale) in the story's
Dev Agent Record, review the document at that recorded path instead, and confirm the
recorded rationale is present.

## Required Claims

Confirm each claim by direct inspection of the document (and the noted shell checks).

- [ ] The document exists at `/Users/steve/projects/nornspun/.claude/guidelines/constitution.md`
      (or at the alternate path recorded in the Dev Agent Record with a stated rationale).
- [ ] The document body is 150 lines or fewer (verify with `wc -l`).
- [ ] The document contains a section titled "Project Invariants" (or a clearly
      equivalent heading).
- [ ] The Project Invariants section documents an **async-first** invariant: no
      blocking calls in async request handlers; long-running generation runs as
      background async tasks managed by an in-process task registry, not the web
      framework's built-in background-tasks helper.
- [ ] The Project Invariants section documents a **data-layer access** invariant: all
      storage access goes through a storage-backend abstraction/protocol, not ad-hoc
      direct database calls.
- [ ] The Project Invariants section documents an **SSE event contract** invariant: on
      a single streaming connection, conversation events and background-task events are
      distinguished by documented event-type name prefixes (conversation-style event
      names vs. a background-task event-name prefix).
- [ ] The Project Invariants section documents a **snake_case wire format** invariant:
      JSON wire payload field names use snake_case.
- [ ] The Project Invariants section documents a **per-session cost-cap enforcement**
      invariant: agents respect a per-session cost-control posture (for example, a
      silence mode that suppresses extra/auxiliary evaluation model calls).
- [ ] Each of the five invariants above carries a citation to a nornspun source — the
      architecture document, a numbered nornspun decision, or a nornspun guideline.
- [ ] The document contains a section pointing to the cold KB (a "Cold KB pointer"
      section or clearly equivalent heading).
- [ ] The Cold KB pointer section names the vault path `~/projects/nornspun-agentic-kb`.
- [ ] The Cold KB pointer section states WHEN to query the KB — at minimum covering
      unfamiliar API, pattern uncertainty, and library-version questions.
- [ ] The Cold KB pointer section includes a usable wiki-query interface block: either
      a concrete invocation of the wiki-query capability or a concrete command to grep
      the vault — actionable, not a bare mention.
- [ ] The document does NOT contain agent-specific file-pattern-to-role routing entries
      (for example, no line mapping a glob like `*.kt` in `composeApp/` or `*.kts` to a
      named agent role).
- [ ] The document references the global CMUX layout rule at `~/.claude/rules/cmux.md`
      and does not restate or redefine the CMUX layout itself.
- [ ] The document contains no Tier-2 specialist content — no embedded
      Python-backend-dev, Kotlin/Compose-dev, or QA specialist body.
- [ ] Every nornspun source path the document cites resolves on disk (the architecture
      document, each cited decision file, each cited guideline, the cold-KB vault path,
      and the CMUX rule path).

## Required Sections

The document MUST contain (headings may differ in exact wording but must be
unambiguously present and identifiable):

- A **Project Invariants** section enumerating the five invariants, each with a source
  citation.
- A **Cold KB pointer** section with: the vault path, WHEN-to-query triggers, and a
  wiki-query interface block.
- A **CMUX reference** — a pointer to `~/.claude/rules/cmux.md` (may be a single line
  inside another section; it must reference rather than redefine the layout).

## Pass Criteria

The review PASSES when ALL of the following hold:

1. The document is present at the Tier-1 path (or the alternate recorded path with a
   stated rationale).
2. `wc -l` on the document reports 150 lines or fewer.
3. The Project Invariants section is present and documents all five invariants
   (async-first, data-layer access via storage-backend abstraction, SSE event-prefix
   contract, snake_case wire format, per-session cost-cap enforcement), and each
   invariant cites a nornspun source.
4. The Cold KB pointer section is present and includes the vault path
   `~/projects/nornspun-agentic-kb`, the WHEN-to-query triggers, and a usable
   wiki-query interface block.
5. The document contains no agent-specific file-pattern-to-role routing entries.
6. The document references `~/.claude/rules/cmux.md` rather than redefining the CMUX
   layout.
7. The document contains no Tier-2 specialist content.
8. Every source path the document cites resolves on disk.

## Fail Criteria

The review FAILS if ANY of the following is true:

1. The document is missing at the Tier-1 path and no alternate path with a rationale is
   recorded.
2. The document body exceeds 150 lines.
3. Any of the five required invariants is missing, or any present invariant lacks a
   citation to a nornspun source.
4. The Cold KB pointer section is missing, or it omits the vault path, the
   WHEN-to-query triggers, or a usable wiki-query interface block (a bare mention with
   no actionable invocation/command counts as a failure).
5. The document contains one or more agent-specific file-pattern-to-role routing
   entries.
6. The document restates/redefines the CMUX layout instead of referencing
   `~/.claude/rules/cmux.md`.
7. The document embeds Tier-2 specialist content (Python-backend-dev, Kotlin/Compose-dev,
   or QA specialist bodies).
8. Any source path the document cites does not resolve on disk.
