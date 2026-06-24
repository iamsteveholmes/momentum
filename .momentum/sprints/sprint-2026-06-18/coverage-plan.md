# Coverage Plan — sprint-2026-06-18

> **Anti-redundancy principle:** Never validate in isolation what an integrated scenario already
> exercises. Where an end-to-end run exercises a story's happy path, the verifier should reuse that
> run rather than re-driving it; dedicated verification then focuses on each story's edge and
> standalone observables that the integrated run does not assert.

## Integration scenarios (informational — reuse these runs during verification)

### IS-1 — Compose one agent end-to-end (Gate G1)
A single `momentum:build-guidelines` run against a project with a real KB produces a composed
specialist agent file and registers it, generating along the way a standalone constitution that
contains the wiki-query interface block and consumes a diagnostic-table manifesto.

- **Exercises (happy paths):** `build-guidelines-skill` (G1), `constitution-builder-write-mode-parameterization` (composed_agent_file + standalone_constitution write modes), `wiki-query-interface-block-for-hot-constitution` (the block in the generated constitution), `agent-manifesto-format-specification` (the manifesto consumed), `nornspun-agent-constitution` (nornspun as the real-KB target whose Tier-1 constitution is produced).
- **Does NOT assert** (→ still need dedicated runs): invalid-write_mode rejection + path-prompt behavior (write-mode-param); fast-mode trigger prefixes + multi-KB-vs-single-KB selection (wiki-query-block); manifesto completeness criterion + exemplar-expressibility (manifesto-format); the out-of-repo nornspun constitution's required claims (nornspun); constitution.md generation ACs (constitutionmd).

### IS-2 — Conduct build finding/ledger integrity
A single conduct build run with review findings (including a duplicate) exercises both conduct seams.

- **Exercises (happy paths):** `conduct-assign-finding-id-before-directed-fix-invocation` (finding_id present at the fixer hand-off), `conduct-ledger-append-site-dedup-guards` (a duplicate `(story_slug, event, finding_id)` append is suppressed).
- **Does NOT assert** (→ still need dedicated runs): each seam's MISMATCH/FAIL scenario (finding handed off lacking finding_id; a duplicate yielding two entries) and idempotence/edge paths.

## Disposition

Every story is **dedicated-run** — each contract carries distinct standalone and failure-path
observables that IS-1 / IS-2 do not fully discharge. The integration scenarios above are reused for
happy-path coverage; dedicated runs cover the rest.

| Story | Disposition | Rationale |
|---|---|---|
| build-guidelines-skill | dedicated-run | Keystone; its contract IS the Gate G1 assertion — verified directly, not by composition. |
| constitution-builder-write-mode-parameterization | dedicated-run | Invalid-mode rejection, path-prompt logic, and content-preservation are not asserted by IS-1. |
| wiki-query-interface-block-for-hot-constitution | dedicated-run | Exact two-mode syntax, fast-mode prefixes, prescriptive triggers, multi-KB selection need direct checks. |
| agent-manifesto-format-specification | dedicated-run | Document-review of the format spec; completeness criterion + exemplar-expressibility are standalone. |
| constitutionmd-generation-acceptance-criteria | dedicated-run | Document-review of the generation ACs spec; standalone. |
| nornspun-agent-constitution | dedicated-run | Document-review of an out-of-repo constitution; its required claims are standalone. |
| conduct-assign-finding-id-before-directed-fix-invocation | dedicated-run | Seam MISMATCH/idempotence scenarios are not asserted by the IS-2 happy path. |
| conduct-ledger-append-site-dedup-guards | dedicated-run | Seam duplicate-yields-two-entries failure path is standalone. |

**Validation:** all 8 stories appear exactly once; both integration scenarios name ≥1 story they
exercise. No story is covered-by-composition, so no contract header back-fill is required
(`coverage_disposition: dedicated-run`, `covered_by_scenario: null` stand as authored).
