# build-guidelines Live E2E — Run Procedure

This directory contains the **deterministic assertion driver** (`live-compose-resolve.sh`) for
the live end-to-end proof that the build-guidelines + agent-builder pipeline composes, registers,
and resolves a Gen-2 specialist agent against a real manifesto and project KB.

Story: `live-e2e-compose-register-resolve-gen-2-agent`
DEC-038 G1 gate: a run is valid only if a composed agent file is written AND registered in
`momentum/agents.json` with non-empty `patterns[]` AND `momentum-tools agent resolve --touches`
returns the composed slug (not the generic `dev` fallback).

---

## Overview — Two-Phase E2E

| Phase | What happens | Who runs it |
|---|---|---|
| **Phase 1: Composition** | `momentum:build-guidelines` → `momentum:agent-builder` writes the composed `.claude/guidelines/agents/dev-kotlin-compose.md` and populates the fixture's `momentum/agents.json` | Developer / agent (LLM skill invocation; no headless CLI) |
| **Phase 2: Assertion** | `live-compose-resolve.sh` checks the composed outputs deterministically | Script (this driver) |

Running-app proof = Phase 1 ran AND Phase 2 driver asserted on the real outputs (not a trace).

---

## Prerequisites

### Tool check

```bash
momentum-tools version check    # confirms momentum-tools is on PATH
```

### Fixture: ~/projects/nornspun

The nornspun practice project (`~/projects/nornspun`) is the fixture. It must have:

1. `.claude/guidelines/constitution.md` — Tier-1 context (already present)
2. `docs/guidelines/` KB — 5 guideline files (already present: compose-ui-patterns.md,
   gradle-agp-build.md, kmp-testing-stack.md, kotlin-kmp-conventions.md, ktor-sse-patterns.md)
3. `.claude/manifests/dev-kotlin-compose.md` — manifesto with a `## File Ownership` field
   (see "Stage the manifesto" below; NOT yet present — must be created before Phase 1)
4. `momentum/agents.json` with a `defaults` block (see "Fixture setup" below)

---

## Fixture Setup (one-time, before Phase 1)

### A. Create the manifests directory and manifesto

```bash
mkdir -p ~/projects/nornspun/.claude/manifests
```

Create `~/projects/nornspun/.claude/manifests/dev-kotlin-compose.md` with this content
(copy verbatim — the `file_ownership` list becomes `patterns[]` in agents.json):

```markdown
---
role: dev
domain: kotlin-compose
project_kb: nornspun-agentic-kb
---

# dev-kotlin-compose — Nornspun Compose Multiplatform Developer

The specialist dev agent for the nornspun Compose Multiplatform project.
Implements screens, ViewModels, state machines, data layer, and tests
in the CMP app targeting Android and Desktop.

---

## Project Stack

Compose Multiplatform app targeting **Android and Desktop**.

- **Shared UI:** `composeApp/`
- **Shared logic + data:** `shared/`
- **Architecture:** MVI throughout — no exceptions

Tech: **CMP 1.10.2 · Material3 · Ktor client · SQLDelight · Kotest · Turbine
· kotlinx.coroutines · kotlinx.serialization**

---

## File Ownership

file_ownership:
  - "composeApp/**"
  - "shared/**"

---

## Diagnostic Table

### Compose — Recomposition and Side Effects

- **Composable recomposing more than expected** → `wiki-query Compose recomposition stability Strong Skipping unstable types`
- **`LaunchedEffect` running on every recomposition instead of once** → `wiki-query Compose LaunchedEffect key recomposition side effects`
- **`DisposableEffect` or `SideEffect` — which to use** → `wiki-query Compose side effects DisposableEffect SideEffect all eight APIs`
- **`snapshotFlow` — converting Compose state to Flow for observation** → `wiki-query snapshotFlow Compose State Flow coroutine`

### Compose — Layout, Modifiers, and Lists

- **Modifier order causing unexpected visual result** → `wiki-query Compose modifiers ordering graphicsLayer drawBehind`
- **`LazyColumn` items losing state on scroll or recomposing too aggressively** → `wiki-query Compose lazy lists key contentType recomposition animateItem`
- **Pager setup or page offset effects** → `wiki-query Pager Compose HorizontalPager PagerState peek scroll effects`

### MVI and State Management

- **`StateFlow` value change not triggering recomposition** → `wiki-query MVI StateFlow collectAsStateWithLifecycle Compose lifecycle`
- **Effect (navigation, toast) firing on every recomposition instead of once** → `wiki-query MVI Effect Channel SharedFlow replay receiveAsFlow`
- **ViewModel scoping across destinations in Nav 3** → `wiki-query ViewModel CMP nav scoping initializer lambda viewModelScope`

### Kotest — Coroutines and Flow

- **Coroutine test hangs, or `delay()` runs in real time** → `wiki-query Kotest coroutineTestScope TestCoroutineScheduler virtual time advanceTimeBy`
- **Flow emissions not arriving — `awaitItem` times out** → `wiki-query Turbine awaitItem awaitComplete testIn turbineScope StateFlow`
- **Mock state leaking between test cases** → `wiki-query Kotest isolation mode SingleInstance beforeTest MockK reset`

### SQLDelight

- **Query result not updating UI reactively** → `wiki-query SQLDelight asFlow mapToList coroutines dispatcher requirements`
- **Multiplatform driver setup (Android + Desktop)** → `wiki-query SQLDelight platform drivers Android desktop JVM expect actual factory`

### Ktor Client

- **Which engine for Android vs Desktop** → `wiki-query Ktor engine selection CIO OkHttp Darwin KMP expect actual HTTP2`
- **Server-sent events or streaming response** → `wiki-query SSE streaming Ktor client Flow collect reconnection buffer`
```

**Important:** the `file_ownership` list (`["composeApp/**","shared/**"]`) is the exact value
that must be passed as `OWNERSHIP_GLOBS` when running the driver. Any change here requires
updating the driver invocation accordingly.

### B. Pre-create agents.json with a defaults block

The composition pipeline adds to `project[]` but never overwrites `defaults`. Create the
initial `momentum/agents.json` so the negative-control resolve (AC5) has a valid `defaults.dev`
path after composition:

```bash
mkdir -p ~/projects/nornspun/momentum
cat > ~/projects/nornspun/momentum/agents.json << 'EOF'
{
  "defaults": {
    "dev": ".claude/guidelines/agents/dev-kotlin-compose.md"
  },
  "project": []
}
EOF
```

This sets `defaults.dev` to the composed agent path (which will exist after Phase 1).
The `project[]` array is populated by agent-builder in Phase 1.

---

## Phase 1 — Composition (LLM skill invocation)

Run this from the nornspun practice project (`~/projects/nornspun`) with the manifesto staged:

```
/momentum:build-guidelines
```

The skill will:
1. Discover `.claude/manifests/dev-kotlin-compose.md`, parse `## File Ownership` verbatim
2. Read the base body from `skills/momentum/agents/dev.md`
3. Read the constitution from `.claude/guidelines/constitution.md`
4. Compose `base_body + constitution_excerpt + manifesto` → `.claude/guidelines/agents/dev-kotlin-compose.md`
5. Register the entry in `momentum/agents.json` `project[]` with `patterns = file_ownership`

After Phase 1 succeeds, verify:
```bash
ls ~/projects/nornspun/.claude/guidelines/agents/dev-kotlin-compose.md   # composed file
cat ~/projects/nornspun/momentum/agents.json                              # project[] entry
```

The `project[]` entry should contain:
```json
{
  "slug": "dev-kotlin-compose",
  "agent": ".claude/guidelines/agents/dev-kotlin-compose.md",
  "patterns": ["composeApp/**", "shared/**"],
  ...
}
```

---

## Phase 2 — Assertion Driver

Run from the **Momentum repo root** (so `docs/research/` is reachable):

```bash
cd ~/projects/momentum

FIXTURE_DIR=~/projects/nornspun \
COMPOSED_SLUG=dev-kotlin-compose \
MATCH_PATH="composeApp/src/commonMain/kotlin/App.kt" \
NONMATCH_PATH="README.md" \
OWNERSHIP_GLOBS='["composeApp/**","shared/**"]' \
bash skills/momentum/skills/build-guidelines/e2e/live-compose-resolve.sh
```

Expected output on success:

```
--- build-guidelines E2E: asserting composed fixture state ---
  fixture : /Users/steve/projects/nornspun
  slug    : dev-kotlin-compose
  match   : composeApp/src/commonMain/kotlin/App.kt
  nonmatch: README.md

  PASS: agents.json project entry 'dev-kotlin-compose' exists; patterns == manifesto File Ownership verbatim (AC3 / AC5-guard)
  PASS: AC2: resolve --touches 'composeApp/src/commonMain/kotlin/App.kt' → 'dev-kotlin-compose' (composed slug, not dev)
  File: /Users/steve/projects/nornspun/.claude/guidelines/agents/dev-kotlin-compose.md
  ...
  PASS: AC4: composed file has base body + '## Diagnostic Table' section
  PASS: AC5: resolve --touches 'README.md' → 'dev' (genuine pattern match, not vacuous)

PASS — all assertions hold.
Evidence artifact: docs/research/live-e2e-compose-resolve-evidence-YYYY-MM-DD.md
```

Exit 0 = DEC-038 G1 gate is met.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `fixture agents.json not found` | Phase 1 not run, or FIXTURE_DIR wrong | Run Phase 1 first; check FIXTURE_DIR |
| `composed project entry missing` | agent-builder did not register the entry | Re-run Phase 1; check build-guidelines output |
| `patterns != ownership field verbatim` | Manifesto file_ownership was edited after composition | Re-run Phase 1 with updated manifesto |
| `resolve returned 'dev' on matching path` | fnmatch mismatch between MATCH_PATH and patterns | Verify MATCH_PATH actually matches the declared globs |
| `momentum-tools exited non-zero` (AC5) | `defaults.dev` in agents.json points to a missing file | Re-run Fixture Setup step B |
| `composed file missing base-body marker` | Composition incomplete or wrong base body merged | Inspect composed file; re-run Phase 1 |

---

## AC to driver mapping

| AC | Assertion in driver |
|---|---|
| AC2 | resolve on MATCH_PATH → COMPOSED_SLUG (not dev) |
| AC3 | patterns[] == file_ownership list verbatim (exact list equality) |
| AC4 | composed file exists, has `## Diagnostic Table`, has base-body marker |
| AC5 | wrong-file guard (project entry exists); negative control on NONMATCH_PATH → dev |
| AC6 | evidence artifact written to docs/research/live-e2e-compose-*.md |
| AC7 | AC3 exact-equality assertion proves deterministic path (patterns from field, not LLM inference) |
