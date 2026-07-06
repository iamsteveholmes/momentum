# Eval: Plan Gate — Purpose Hero Leads and Structure Is Diagrammed

**ID:** eval-plan-gate-purpose-hero-and-structure-diagram
**Change-type:** skill-instruction
**Phase:** developer review (Step 7) — HTML gate content

## Scenario A: Purpose hero leads before any table or story list

Given a plan gate HTML file emitted for a 5-story sprint

When a reader opens the file and reads from the top

Then:
1. The first content block (after `<h1>` and `<p class="sub">`) is a `<div class="hero">` containing
   a plain-language statement of what the sprint accomplishes
2. The hero text is readable by a non-implementer in under 10 seconds (≤ 2 sentences for the main statement)
3. No story table, story list, or decision card appears before the hero block

## Scenario B: Dependency/wave structure rendered as SVG diagram, not prose

Given a sprint with 4 stories across 2 waves where `story-c` depends on `story-a`

When a reader inspects the structure section of the plan gate

Then:
1. An inline `<svg>` element appears representing the dependency/wave structure
2. The SVG contains node elements for each story (visible `<rect>` or similar shapes)
3. At least one `<path>` connector element appears representing the `story-a → story-c` dependency
4. The structure is NOT described only in prose (no "Wave 1 contains story-a and story-b" text node replacing a diagram)

## Scenario C: Critical-path / SPOF story is visibly marked in the diagram

Given a sprint where `story-a` (Wave 1) is depended on by 2 other stories (`story-c` and `story-d`)
making it the single point of failure for the sprint

When a reader inspects the SVG diagram

Then:
1. The `story-a` node has visually distinct styling (red border / fill `#f6ddd6` stroke `#9a3b2f`) indicating HIGH stakes or SPOF
2. A `⚠` marker or equivalent visual indicator is present on or near the `story-a` node
3. The `story-b` node (no dependents) does NOT receive the same high-stakes styling (correct differentiation)

## Scenario D: Every story appears exactly once in the at-a-glance table

Given a 4-story sprint plan gate

When a reader inspects the items-at-a-glance section

Then:
1. Exactly 4 `.scard` elements appear — one per story, no duplicates
2. Each card carries: story title, wave number, dependency reference, and a verdict badge (`★ CALL` or `✓ batch`)
3. No story's full AC text or Dev Notes are inlined into the card body

## Pass Criteria

- `<div class="hero">` appears before `<div class="cards">` in the HTML document order
- An inline `<svg>` element with at least one `<rect>` and one `<path>` is present
- SPOF story node uses the high-stakes fill/stroke colors from the template
- Story count in `.scard` elements matches `selected_stories` count (no extras, no missing)

## Fail Criteria

- First content block after `<h1>` is a table, story list, or decision card (hero buried)
- Structure described only in prose; no `<svg>` element in the HTML
- SPOF story rendered identically to low-stakes stories (no visual differentiation)
- A story appears zero times or more than once in the cards section
