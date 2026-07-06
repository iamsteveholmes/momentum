# Coverage Plan — sprint-2026-06-28

> **Anti-redundancy principle:** Never validate in isolation what an integrated scenario already
> exercises.

This sprint's five stories verify largely distinct surfaces, so there are no fully
covered-by-composition stories. One integration relationship is documented below so the verifier
does not build a redundant isolated test.

## Integration scenarios (anti-redundancy guidance)

### Scenario — Live agent-composition end-to-end
- **Description:** Against the real `nornspun` fixture, the composition pipeline is run and a
  committed driver asserts that resolution on a path matching a declared ownership glob returns the
  composed `{role}-{domain}` slug (not the generic `dev` fallback), that the registered `patterns`
  equal the manifest File Ownership field verbatim, and that a non-matching path falls back to `dev`.
- **Exercises the boundary:** manifest File-Ownership field → `agents.json` `patterns` (verbatim)
  → `momentum-tools agent resolve --touches` → composed slug.
- **Discharges (live, end-to-end):** the *deterministic-resolution* acceptance of
  `manifesto-format-normative-file-pattern-ownership-field` (its patterns-verbatim + composed-slug
  resolution behavior). **Because `live-e2e-compose-register-resolve-gen-2-agent` runs this live,
  the verifier does NOT construct a separate isolated resolution test for the manifesto story** —
  the live E2E is the end-to-end proof of that boundary.
- **Does NOT discharge:** the manifesto story's *format-declaration* acceptance (the required
  ownership section exists in the manifesto format doc) or its *missing-field-signal* acceptance
  (a manifest lacking the field produces an explicit signal, not a guess). Those remain a
  dedicated run.

## Per-story disposition

| Story | Disposition | Rationale |
|---|---|---|
| `companion-surface-pre-sprint-plan-gate` | **dedicated-run** | Only this story exercises the emitted pre-sprint plan-gate surface; no other story's verification touches it. |
| `companion-surface-post-sprint-results-gate` | **dedicated-run** | Only this story exercises the fused post-sprint results surface; no overlap. |
| `companion-surface-rule-sync-and-bulk-derivation` | **dedicated-run** | Standalone document review of the synced project rule; no other story reads it. |
| `manifesto-format-normative-file-pattern-ownership-field` | **dedicated-run** | Its format-declaration and missing-field-signal ACs are not exercised by any other story; its deterministic-resolution ACs are additionally re-exercised live by the E2E (see scenario above), so no isolated resolution test is added. |
| `live-e2e-compose-register-resolve-gen-2-agent` | **dedicated-run** | The integration scenario itself — the live composition+resolution run; nothing else discharges it. Depends on the manifesto story for its deterministic path. |

## Validation

- All five approved stories appear exactly once above (all dedicated-run).
- Every named scenario names at least one story it relates to (the Live agent-composition E2E relates the manifesto story's resolution boundary to the live-E2E story).
