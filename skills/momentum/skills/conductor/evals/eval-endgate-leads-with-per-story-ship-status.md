# Eval: End-gate leads with per-story ship status

**Skill under test:** `momentum:conductor` (Phase 5 end-gate renderer)
**Renderer spec:** `skills/momentum/skills/conductor/references/endgate-report-renderer.md`

## Scenario

**Given:** A conduct build for `sprint-2026-07-01` completes with:
- 3 stories merged (`auth-login`, `profile-ui`, `search-api`)
- 1 story blocked (`analytics-dashboard`)
- 1 story quarantined (`export-csv`)

**When:** The Conductor renders the end-gate HTML at Phase 5.

**Then:**

1. The first content section after the metrics hero strip is a **per-story ship status block** — not narrative prose, not §01 "What shipped".
2. Every sprint story is listed with an explicit outcome label: one of `shipped-merged`, `blocked`, `closed-incomplete`, or `quarantined`.
3. The ship-status block appears **before** §01 "What shipped" in the document order.
4. Status is presented as scannable pills or a strip — not as flat prose sentences.
5. `auth-login`, `profile-ui`, and `search-api` carry `shipped-merged` labels; `analytics-dashboard` is labeled `blocked`; `export-csv` is labeled `quarantined`.

## Pass Criteria

- A ship-status section (§00) exists in the renderer spec section spine, positioned before §01
- Every sprint story appears in the block with an explicit outcome
- Outcome labels match the four canonical values (`shipped-merged`, `blocked`, `closed-incomplete`, `quarantined`)
- Status is visually scannable (pills, strip, or table) — not prose sentences

## Fail Criteria

- The first content section after the hero is §01 narrative without a prior ship-status lead
- Any sprint story is absent from the status block
- Outcome is stated as a sentence rather than a labeled pill/badge
- The ship-status block appears after §01 in the section spine table

## Verification Note

Verified by inspecting the renderer spec §3 section spine table: the ship-status section must appear before the §01 row. The spec must also define the status pill/strip rendering requirement and the four canonical outcome labels. This eval does not require a live build run — inspection of the renderer spec is sufficient.
