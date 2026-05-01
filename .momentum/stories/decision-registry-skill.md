# Decision Registry Skill — Capture Strategic Decisions in SDR Format

Status: backlog
Epic: impetus-core
Priority: medium

## What This Is

A `/momentum:decision-registry` skill that captures strategic decisions as SDR (Strategic Decision Record) documents. When research produces recommendations and the developer makes decisions in response, this skill records what was recommended, what was decided, and why — with proper frontmatter linking to source research, architecture decisions affected, and stories affected.

## Why It Matters

Decisions happen in conversation and evaporate. A research report gets discussed, choices are made, and the only record is buried in chat history. The SDR format (established in nornspun at `_bmad-output/planning-artifacts/decisions/`) bridges research findings and backlog work, but currently requires manual creation. A skill makes capture frictionless and consistent.

SDRs are distinct from architecture decisions (AD-1 through AD-31 in architecture.md). ADs capture single-concern technical decisions. SDRs capture session-level strategic choices that span multiple ADs, emerge from research evaluations, or represent direction changes that don't fit a single AD slot.

## What the Skill Should Do

- Guide the user through recording decisions from a research evaluation or strategic discussion
- Write an SDR document with frontmatter: `id`, `title`, `date`, `status`, `source_research`, `prior_decisions_reviewed`, `architecture_decisions_affected`, `stories_affected`
- Each decision within the SDR: what was recommended, what was decided (adopted/rejected/deferred), rationale
- Optional phased implementation plan and decision gates
- Update `decisions/index.md` registry
- Commit the result
- Support two flows: "new decision from research" and "revisiting a prior decision"
- Be aware of existing ADs in architecture.md — don't duplicate what belongs in an AD slot

## What It Should NOT Do

- Deliberate or evaluate the decisions — that already happened in conversation
- Run research or web searches — it captures conclusions, not produces them
- Modify architecture.md — if an AD needs updating, that's a separate action the skill can suggest
- Create stories automatically — it records which stories are affected, but story creation goes through intake or create-story

## Design Decisions Already Made

- SDR format is established: see `sdr-001-agentic-ui-stack-eval.md` in nornspun for the canonical example
- The `decisions/` directory lives under `_bmad-output/planning-artifacts/`
- The index is a markdown table with ID, Title, Date, Source Research, Status columns
- Voice should match Impetus — dry, forward-moving, no fluff. It captures decisions, it doesn't deliberate them
- SDR IDs are sequential: SDR-001, SDR-002, etc.
- Decision statuses within an SDR: adopted, rejected, deferred (each with rationale)
