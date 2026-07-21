# Eval: build-guidelines Phase 1 Discover marks the produced manifesto valid

**Eval ID:** manifesto-builder-output-passes-build-guidelines-discover
**Stakes:** correctness / pipeline-integrity (producer/consumer seam) — `manifesto-builder` is the producer and `build-guidelines` Phase 1 Discover is the consumer. If the producer's output shape doesn't match what the consumer checks for, the pipeline stays broken even though a manifesto now exists on disk.

**Given** a manifesto produced by a completed `momentum:manifesto-builder` run at `.claude/manifests/{role}-{domain}.md`, and a base body already present at `skills/momentum/agents/{role}.md` for the chosen role,

**When** `momentum:build-guidelines` runs its Phase 1 (Discover) manifest-scan step over `.claude/manifests/`,

**Then** the manifesto is reported `valid: true`: required identity fields (`role`, `domain`, `project_kb`) present, `## Project Stack` present, `## File Ownership` present with a non-empty `file_ownership` list, and `## Diagnostic Table` present with at least one entry. Entry count is informational only — never a pass/fail gate.

## Verification approach

1. Read `skills/momentum/skills/build-guidelines/workflow.md` Phase 1 (Discover) — note its exact five-part validity check (frontmatter fields; `## Project Stack`; `## File Ownership` non-empty; `## Diagnostic Table` ≥1 entry; base body exists at `skills/momentum/agents/{role}.md`).
2. Read `skills/momentum/skills/manifesto-builder/workflow.md` FINALIZE phase — confirm its self-check step explicitly checks against this same checklist (frontmatter present, Project Stack present, File Ownership present + non-empty, Diagnostic Table ≥1 entry) before writing, so the two skills' notions of "complete" cannot silently drift apart.
3. If a reachable KB and a `dev` base body are available (e.g. `skills/momentum/agents/dev.md` exists in this project), run `momentum:manifesto-builder` for `role=dev, domain=kotlin-compose` to produce a manifesto, then run `momentum:build-guidelines`'s Discover step (or its manifest-scan logic directly) over `.claude/manifests/` and confirm the produced entry is reported `valid: true`.
4. Separately confirm the negative case is also handled: a manifesto with one of the four required elements missing or emptied (e.g. an empty `file_ownership: []`) is reported invalid, with the missing/empty element named — not a silent pass and not a generic failure.

## Pass criteria

`build-guidelines` Phase 1 Discover reports the produced manifesto as `valid: true` and proceeds toward composing an agent from it (composition itself is out of this story's scope — only Discover's verdict is the pass bar). The number of Diagnostic Table entries plays no role in the verdict. The negative case (missing/empty required element) is named explicitly, not silently accepted.

## Fail criteria

`build-guidelines` reports the manifesto invalid or skips it despite all four required elements being present (signals a producer/consumer field-shape mismatch); or a manifesto missing/emptying a required element is silently accepted as valid; or entry count is treated as a gate anywhere in either skill's instructions.
