# Agent Manifesto Format

**Version:** 1.0 — initial manifesto format specification; implements DEC-038 D1 + D2 (2026-06-23)

This document is the single authoritative specification of the **agent manifesto** file — its canonical location, identity fields, content model, and completeness rule. A conformant manifesto can be authored from this document alone; no other reference is required.

---

## What the Manifesto Is

The manifesto **is** the agent's **diagnostic table** — a stable, per-role×domain table whose every row pairs an *observable developer symptom* (the trigger) with the *exact `wiki-query` KB lookup* that resolves it, plus the **stack facts** that scope those lookups.

**Normative definition (DEC-038 D1):**

> The manifesto is the agent's stable, per-role×domain diagnostic table. Every entry maps one observable developer symptom to the exact `wiki-query` terms that retrieve the answer from the project KB. The table is the same across every sprint and every story — it is the agent's standing "how everything is implemented here" guidance.

**The manifesto is NOT a per-sprint or per-story context overlay.** The "project- or sprint-scoped context overlay" reading that appeared in PRD FR136 and FR138 is superseded and rejected (DEC-038 D1). The manifesto does not change per story. Context that varies per sprint or story belongs in the story spec, not the manifesto.

The canonical term is **"diagnostic table."** Never use "context overlay," "routing overlay," or "story overlay" to describe the manifesto.

**Source decisions:** DEC-038 D1 + D2; architecture.md Decision 56.

---

## File Location and Naming Convention

Manifesto files are on-disk inputs to the `momentum:agent-builder` pipeline.

```
.claude/manifests/{role}-{domain}.md
```

**Examples:**

| Role | Domain | File |
|---|---|---|
| `dev` | `kotlin-compose` | `.claude/manifests/dev-kotlin-compose.md` |
| `qa` | `python-fastapi` | `.claude/manifests/qa-python-fastapi.md` |
| `e2e` | `kotlin-compose` | `.claude/manifests/e2e-kotlin-compose.md` |
| `architect` | `kotlin-compose` | `.claude/manifests/architect-kotlin-compose.md` |

The manifesto file's location and naming convention are also recorded in architecture.md Decision 56 (see manifesto-format subsection), which cites this document as the canonical format spec.

**Output file produced by agent-builder:** `.claude/guidelines/agents/{role}-{domain}.md`

---

## Identity Block (Required)

Every manifesto must open with a YAML front-matter block containing at least these fields:

```yaml
---
role: dev          # the agent role (dev | qa | e2e | architect | pm — or any future role)
domain: kotlin-compose  # the technology domain (e.g. kotlin-compose, python-fastapi, react-ts)
project_kb: nornspun-agentic-kb   # the project KB that wiki-query resolves against (see KB Scoping below)
---
```

| Field | Type | Required | Description |
|---|---|---|---|
| `role` | string | yes | The agent role this manifesto covers. Controls which base body (`agents/{role}.md`) agent-builder merges. Supported values include `dev`, `qa`, `e2e`, `architect`, `pm`; open to future roles. |
| `domain` | string | yes | The technology domain (stack) this manifesto covers. Used with `role` to produce the output file name: `.claude/guidelines/agents/{role}-{domain}.md`. |
| `project_kb` | string | yes | The name or identifier of the project knowledge base that `wiki-query` resolves against. See KB Scoping below. |

**The `role` × `domain` pair is the manifesto's composite key.** agent-builder uses this pair to determine which composed agent file to generate (`{role}-{domain}.md`) and which routing entry to write to `momentum/agents.json` `project` block.

---

## Project Stack Section (Required)

Immediately after the identity block, the manifesto must include a `## Project Stack` section. This section records the technology stack facts that scope and disambiguate the diagnostic-table lookups.

**Purpose:** symptom→`wiki-query` entries are only meaningful in the context of specific versions and frameworks. The stack-facts section prevents ambiguity — `wiki-query` terms are chosen to match *this* stack, not a generic one.

**Required content:**

- Programming language and version
- Core UI / application framework and version pin
- Data layer technology (ORM, database, etc.)
- Test tooling (framework, key plugins)
- Architecture paradigm (e.g. MVI, MVVM, Clean)
- Any other version pins the symptom→`wiki-query` entries depend on

**Format:** one terse summary line followed by a bullet list, or a compact inline list. Modeled on the reference exemplar's stack line: `CMP 1.10.2 · Material3 · Ktor client · SQLDelight · Kotest · Turbine · kotlinx.coroutines · kotlinx.serialization`.

**Example:**

```markdown
## Project Stack

Compose Multiplatform app targeting **Android and Desktop**.

- **Shared UI:** `composeApp/`
- **Shared logic + data:** `shared/`
- **Architecture:** MVI throughout — no exceptions

Tech: **CMP 1.10.2 · Material3 · Ktor client · SQLDelight · Kotest · Turbine · kotlinx.coroutines · kotlinx.serialization**
```

The stack facts section scopes every entry in the diagnostic table. A `wiki-query` that resolves correctly on CMP 1.10.2 may not resolve correctly on CMP 2.x. Version pins make the table's resolution behavior predictable.

---

## Diagnostic Table Section (Required)

The diagnostic table is the manifesto's core. It maps *observable developer symptoms* to *exact `wiki-query` KB lookups*.

### Section heading

```markdown
## Diagnostic Table
```

### Entry shape

Each entry is a single bullet under a thematic group heading:

```
- **<symptom — observable, specific, diagnostic>** → `wiki-query <exact terms>`
```

| Component | Requirements |
|---|---|
| **Symptom** | Observable, specific, and diagnostic. Written as the condition the developer would *see* — not an abstract concept. Bad: "recomposition issue." Good: "Composable recomposing more than expected." |
| **`wiki-query` terms** | The exact search string to pass to the `wiki-query` skill. Terms must match the KB page titles and content that resolve the symptom. |
| `→` separator | Required literal separator between symptom and `wiki-query` invocation. |
| Backtick-quoted invocation | The `wiki-query <terms>` string is rendered in code formatting so it is machine-readable. |

### Grouping

Entries must be grouped under `###` sub-headings by technology area or concern:

```markdown
### Compose — Recomposition and Side Effects

- **Composable recomposing more than expected** → `wiki-query Compose recomposition stability Strong Skipping unstable types`
- **`LaunchedEffect` running on every recomposition instead of once** → `wiki-query Compose LaunchedEffect key recomposition side effects`

### Kotest — Coroutines and Flow

- **Coroutine test hangs, or `delay()` runs in real time** → `wiki-query Kotest coroutineTestScope TestCoroutineScheduler virtual time advanceTimeBy`
```

Grouping is for human readability and agent speed — the agent scans group headings to narrow the area before reading entries.

### Symptom phrasing rules (normative)

Symptoms must be:

1. **Observable** — describes what the developer sees, not an internal cause. "Coroutine test hangs" (observable) not "virtual time not advancing" (internal).
2. **Specific** — names the API, behavior, or output that is wrong. "Flow emissions not arriving — `awaitItem` times out" (specific) not "async issue in test" (vague).
3. **Diagnostic** — written at the level of detail that distinguishes it from neighboring entries. Two entries under the same group must not be confusable.
4. **Phrased as a situation, not a question.** "Mock state leaking between test cases" (situation) not "How do I reset mocks?" (question).

Poor symptom phrasing degrades routing quality. The investment in symptom quality is what makes the diagnostic table work.

### wiki-query invocation rules (normative)

- Every entry must supply an **exact** `wiki-query` invocation — not "search for X" but the literal terms to pass.
- Terms must be chosen to match the page titles and content that actually resolve the symptom in the project KB. This requires knowing the KB.
- The invocation is rendered as `` `wiki-query <terms>` `` in the manifesto source.
- When the agent invokes: use the `Skill` tool with `skill: "wiki-query"` and pass the terms in `args`.

---

## KB Scoping (Required — Multi-KB Architecture)

Every manifesto must declare which project KB its `wiki-query` entries resolve against via the `project_kb` identity field.

**Why:** multiple project KBs coexist (DEC-038 D2). Momentum agents resolve against the Momentum KB. Nornspun agents resolve against the nornspun KB. The `project_kb` field tells agent-builder (and any future multi-KB-aware `wiki-query` extension) which KB to target.

**Current state:** `wiki-query` (DEC-018) currently resolves against the active vault. The multi-KB extension that routes lookups to the declared `project_kb` is a planned, not yet implemented, extension (FR142 backlog). The manifesto declares the KB now so the pipeline is ready when the extension lands. This document **does not implement** the multi-KB extension — that work is tracked separately under FR142.

**Normative requirement:** every manifesto's `project_kb` field must be set to the name or identifier of the project KB whose pages the `wiki-query` terms are written to match. A manifesto without `project_kb` is incomplete.

**Examples:**

| Project | `project_kb` value |
|---|---|
| Momentum | `momentum-agentic-kb` |
| nornspun | `nornspun-agentic-kb` |

---

## Completeness Criterion (Normative)

A manifesto is **complete** when its diagnostic table covers every technology area and situation the agent routinely encounters, such that for any symptom the agent hits, at least one table entry matches and its `wiki-query` returns a usable result.

### Two incompleteness conditions

A manifesto is **incomplete** under either of the following conditions:

**Condition 1 — No matching symptom entry.** The agent encounters a situation (a developer symptom) for which no entry in the diagnostic table matches. The agent hits un-routed territory.

**Condition 2 — Matching entry, unusable result.** An entry matches the symptom, but the `wiki-query` invocation returns no usable result — either the KB page does not exist, the terms are wrong, or the returned content does not resolve the symptom.

### Detectable incompleteness signal

An agent reaching un-routed territory must **not** fall through silently. The agent must emit a detectable incompleteness signal:

> **When an agent reaches a situation not covered by any entry in its diagnostic table, or when a `wiki-query` invocation returns nothing usable, the agent must log an explicit incompleteness signal** — for example: `[MANIFESTO INCOMPLETE: no diagnostic-table entry for <situation>]` or `[MANIFESTO INCOMPLETE: wiki-query '<terms>' returned no usable result for <symptom>]`.

The incompleteness signal is surfaced to the orchestrator (or developer), not swallowed. Silent fallthrough to generic training knowledge without flagging the gap is not acceptable — it hides the gap and prevents the manifesto from being improved.

**The completeness criterion is an acceptance criterion on this story** (story `agent-manifesto-format-specification`, AC6). A manifesto format that allows silent un-routed territory is not conformant.

---

## Manifesto File Template

A conformant manifesto file has the following structure:

```markdown
---
role: <role>
domain: <domain>
project_kb: <kb-name>
---

# <role>-<domain> — <Short human-readable description>

<One-sentence summary of what this agent owns and when it is used.>

---

## Project Stack

<terse summary line>

- **<fact category>:** <value>
- ...

Tech: **<version-pinned tech line>**

---

## Diagnostic Table

### <Technology Area 1>

- **<observable symptom>** → `wiki-query <exact terms>`
- **<observable symptom>** → `wiki-query <exact terms>`

### <Technology Area 2>

- **<observable symptom>** → `wiki-query <exact terms>`

<!-- Add more groups as needed -->
```

---

## Exemplar Conformance Check (AC7)

The reference exemplar — `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md` — is the verbatim nornspun `cmp-dev.md` artifact. It is a **format reference only — never a Momentum agent.** Its diagnostic table (`## Quick Routing — wiki-query Delegation Table`, lines 121–192) contains ~35 worked symptom→`wiki-query` entries across 9 technology areas.

This section confirms that every exemplar entry is expressible in this format with no loss of meaning.

**Mapping:** the exemplar's `## Quick Routing — wiki-query Delegation Table` maps directly to this format's `## Diagnostic Table`. The exemplar's group headings (`### Compose — Recomposition and Side Effects`, `### Kotest — Coroutines and Flow`, etc.) map directly to this format's `###` group headings. The exemplar's bullet entries follow the exact `- **<symptom>** → \`wiki-query <terms>\`` shape this format requires.

**Entry-by-entry check:**

The exemplar groups and their entries (verbatim) render in this format as follows:

### Compose — Recomposition and Side Effects (4 entries)

- **Composable recomposing more than expected** → `wiki-query Compose recomposition stability Strong Skipping unstable types`
- **`LaunchedEffect` running on every recomposition instead of once** → `wiki-query Compose LaunchedEffect key recomposition side effects`
- **`DisposableEffect` or `SideEffect` — which to use** → `wiki-query Compose side effects DisposableEffect SideEffect all eight APIs`
- **`snapshotFlow` — converting Compose state to Flow for observation** → `wiki-query snapshotFlow Compose State Flow coroutine`

### Compose — Layout, Modifiers, and Lists (3 entries)

- **Modifier order causing unexpected visual result** → `wiki-query Compose modifiers ordering graphicsLayer drawBehind`
- **`LazyColumn` items losing state on scroll or recomposing too aggressively** → `wiki-query Compose lazy lists key contentType recomposition animateItem`
- **Pager setup or page offset effects** → `wiki-query Pager Compose HorizontalPager PagerState peek scroll effects`

### Compose — Animation (3 entries)

- **Choosing the right animation API** → `wiki-query Compose animation APIs animate*AsState AnimatedVisibility AnimatedContent decision tree`
- **Shared element transition between screens** → `wiki-query Compose shared element transitions sharedElement sharedBounds Nav`
- **Predictive back gesture animation** → `wiki-query Compose predictive back PredictiveBackHandler SeekableTransitionState`

### MVI and State Management (4 entries)

- **`StateFlow` value change not triggering recomposition** → `wiki-query MVI StateFlow collectAsStateWithLifecycle Compose lifecycle`
- **Effect (navigation, toast) firing on every recomposition instead of once** → `wiki-query MVI Effect Channel SharedFlow replay receiveAsFlow`
- **ViewModel scoping across destinations in Nav 3** → `wiki-query ViewModel CMP nav scoping initializer lambda viewModelScope`
- **`coroutines` in ViewModel — which scope, which dispatcher** → `wiki-query coroutines dispatchers viewModelScope IO Default Main`

### Navigation (2 entries)

- **Nav 3 back stack and `NavDisplay` setup** → `wiki-query Navigation 3 CMP NavDisplay back stack type-safe SavedStateConfiguration`
- **Deep link handling per platform** → `wiki-query CMP navigation deep links navDeepLink ExternalUriHandler platform`

### Kotest — Coroutines and Flow (5 entries)

- **Coroutine test hangs, or `delay()` runs in real time** → `wiki-query Kotest coroutineTestScope TestCoroutineScheduler virtual time advanceTimeBy`
- **Which spec style to use for a new test** → `wiki-query TDD Kotest spec style FunSpec BehaviorSpec coroutineTestScope forcing function`
- **Flow emissions not arriving — `awaitItem` times out** → `wiki-query Turbine awaitItem awaitComplete testIn turbineScope StateFlow`
- **Polling for an async condition in a test** → `wiki-query Kotest eventually continually retry backoff`
- **Mock state leaking between test cases** → `wiki-query Kotest isolation mode SingleInstance beforeTest MockK reset`

### Kotest — Assertions and Data (4 entries)

- **Asserting on a sealed class or nested data class** → `wiki-query Kotest assertion shouldBe sealed class data class inspection`
- **Soft assertions — accumulate failures instead of stopping** → `wiki-query Kotest soft assertions assertSoftly shouldBe`
- **Property-based testing — generate inputs instead of hand-writing cases** → `wiki-query Kotest property based testing Arb checkAll forAll shrinking`
- **Data-driven tests with multiple input sets** → `wiki-query Kotest data driven testing withData`

### SQLDelight (5 entries)

- **Query result not updating UI reactively** → `wiki-query SQLDelight asFlow mapToList coroutines dispatcher requirements`
- **Multiplatform driver setup (Android + Desktop)** → `wiki-query SQLDelight platform drivers Android desktop JVM expect actual factory`
- **Schema change requires migration** → `wiki-query SQLDelight migrations sqm versioning AfterVersion callbacks`
- **Writing a test against the database** → `wiki-query SQLDelight query testing in-memory driver cross-platform`
- **Gradle source set layout or codegen not running** → `wiki-query SQLDelight multiplatform setup Gradle source directory layout`

### Ktor Client (4 entries)

- **Which engine for Android vs Desktop** → `wiki-query Ktor engine selection CIO OkHttp Darwin KMP expect actual HTTP2`
- **Request failing silently, timeout, or retry behavior** → `wiki-query Ktor client error handling HttpTimeout HttpRequestRetry plugin ordering`
- **Server-sent events or streaming response** → `wiki-query SSE streaming Ktor client Flow collect reconnection buffer`
- **Serialization not working with Ktor** → `wiki-query Ktor serialization ContentNegotiation kotlinx.serialization install`

### Material3 and Adaptive Layout (2 entries)

- **Theme not applying or dark mode not working** → `wiki-query Material3 theming colorScheme MaterialTheme dynamic color dark`
- **Adaptive layout for different window sizes** → `wiki-query Compose adaptive layouts WindowSizeClass NavigationSuiteScaffold ListDetailPaneScaffold`

**Total: 36 entries across 9 technology areas — all expressible in this format with no loss of meaning.**

The exemplar's `## Project Stack` section (`CMP 1.10.2 · Material3 · Ktor client · SQLDelight · Kotest · Turbine · kotlinx.coroutines · kotlinx.serialization`) maps directly to this format's `## Project Stack` required section.

The exemplar's identity (`cmp-dev`, role `dev`, domain `kotlin-compose`, project `nornspun`) maps directly to this format's identity block fields (`role: dev`, `domain: kotlin-compose`, `project_kb: nornspun-agentic-kb`).

**Conformance verdict: the format is exemplar-complete.** No exemplar entry requires capabilities beyond what this format defines.

*The exemplar is a format reference only — never a Momentum agent. See `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md` header banner.*

---

## Build-Guidelines Consumption Contract (AC8)

The `momentum:build-guidelines` skill (story `build-guidelines-skill`) consumes the manifesto as a **sprint-invariant composition input**. The following fields and sections are what build-guidelines reads:

| What build-guidelines reads | Where it lives | What build-guidelines does with it |
|---|---|---|
| `role` | Identity block | Determines which base body to merge (`agents/{role}.md`) |
| `domain` | Identity block | Determines the output file name (`{role}-{domain}.md`) |
| `project_kb` | Identity block | Scopes `wiki-query` resolution to the correct project KB |
| `## Project Stack` | Stack section | Bakes stack facts into the composed agent for disambiguation |
| `## Diagnostic Table` | Diagnostic table section | Injects the full symptom→`wiki-query` routing table into the composed agent |

**Sprint invariance:** build-guidelines does not re-scope or regenerate the diagnostic table per sprint. The manifesto is consumed as-is; the composed agent embeds the table verbatim. Any change to the table requires editing the manifesto file itself — not a per-sprint override.

**Un-routed territory:** when the composed agent (the output of build-guidelines + agent-builder) hits a situation for which no diagnostic-table entry matches, it emits the incompleteness signal defined in the Completeness Criterion section above. This is the manifesto-incompleteness feedback loop: agent encounters un-routed territory → logs incompleteness signal → developer updates the manifesto → manifesto author re-runs agent-builder → improved composed agent.

---

## Cross-References

| Reference | Path | Relationship |
|---|---|---|
| DEC-038 | `_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md` | Binding authority: D1 (diagnostic table definition), D2 (per-project multi-KB) |
| DEC-026 D4 | architecture.md Decision 56 | Original manifesto definition, refined by DEC-038 |
| DEC-018 | (architecture.md) | `wiki-query` cold-KB interface; multi-KB extension pending (FR142) |
| architecture.md Decision 56 | `_bmad-output/planning-artifacts/architecture.md` | Manifesto canonical definition + manifesto-format subsection (AC9) |
| PRD FR136 / FR138 | `_bmad-output/planning-artifacts/prd.md` | Overlay reading superseded by DEC-038 D1 |
| PRD FR142 | `_bmad-output/planning-artifacts/prd.md` | Multi-KB `wiki-query` extension workstream |
| Reference exemplar | `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md` | Format-only exemplar (nornspun `cmp-dev.md`); never a Momentum agent |
| build-guidelines-skill story | `.momentum/stories/build-guidelines-skill.md` | Primary downstream consumer; AC1–AC4 define consumption contract |
| finding-schema.md | `skills/momentum/references/finding-schema.md` | House-style reference (title + version line, normative definition, field table, examples) |
| sprint-tracking-schema.md | `skills/momentum/references/sprint-tracking-schema.md` | House-style reference |
