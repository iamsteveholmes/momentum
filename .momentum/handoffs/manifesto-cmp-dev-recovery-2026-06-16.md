# Recovery Brief — The CMP-dev Manifesto (Diagnostic Table → wiki-query KB Routing)

**Date:** 2026-06-16
**For:** the agent-cohort sprint (epics `momentum-agent-spawn-orchestration` / `momentum-agent-composition-pipeline`)
**Provenance:** discovery workflow `wxygicz8y` (run `wf_475fd368`, 5 agents over the nornspun
conversation corpus + on-disk artifacts) → synthesized + re-verified against disk → ratified with
the developer 2026-06-16.
**Status:** RECOVERED in full from a committed on-disk artifact, not just transcripts.

---

## 1. TL;DR

The "full-blown manifesto concept" the developer prototyped (~a day of work, May 2026, nornspun)
is the **`cmp-dev` agent** at `nornspun-client/.claude/agents/cmp-dev.md` (241 lines, verified
verbatim). Its crown jewel is a **`## Quick Routing — wiki-query Delegation Table`**: ~35
`observable-symptom → exact wiki-query string` rows across 9 technology areas. The agent runs a
**two-mode dispatch** — answer directly from always-loaded Standing Rules when they settle the
question; fire a pre-written `wiki-query` against the cold Obsidian KB only when a specific symptom
matches a row. The mechanism is: a small **hot** table of *pointers* (symptom→query) bridging
on-symptom to a large **cold** KB that holds the actual knowledge.

The design **did not survive cleanly into Momentum**: the layering vocabulary carried over, but
"manifesto" now has three contradictory definitions and the per-specialist symptom→query table
exists in no current Momentum spec. This brief recovers the design and records the decisions that
unify it.

---

## 2. The recovered design

### 2a. Artifact & structure (verified verbatim)
`cmp-dev.md` — frontmatter `name/description(+4 worked examples)/model: inherit/color/tools`.
Body in order: **Working Directory** (sole-writer boundary — writes only under `nornspun-client`,
reads stories from `nornspun`) · **Project Stack** (`CMP 1.10.2 · Material3 · Ktor · SQLDelight ·
Kotest · Turbine · kotlinx.coroutines · kotlinx.serialization`) · **How You Use Your Two Modes** ·
**Standing Rules** (TDD red→green→refactor, MVI, Kotest spec style) · **Completion Gate** · **Quick
Routing — wiki-query Delegation Table** · **Working Process** · **Quality Standards** · **Output
Format** · **Edge Cases and Escalation**.

### 2b. The two-mode rule (verbatim)
> 1. **Direct answer from standing rules.** When the question is unambiguously covered by the
>    Standing Rules section below … answer directly. Do not run `wiki-query`. The rules are the answer.
> 2. **Delegate to `wiki-query` via the Skill tool.** When the question is version-pinned,
>    API-specific, project-convention-specific, or otherwise beyond what the standing rules cover,
>    invoke `wiki-query` using the routing table below. The wiki encodes project-specific guidance
>    (version pins, alpha APIs, internal conventions) that may override generic training knowledge.
>
> Both modes are valid. Do **not** always run `wiki-query` … Do **not** skip it when the routing table calls for it.

### 2c. THE CORE MECHANISM — the symptom→wiki-query table
Contract (verbatim): *"Use this table whenever the standing rules don't directly settle the
question. Match your situation to a scenario and invoke `wiki-query` via the `Skill` tool with the
exact terms shown."* Entry shape: `**[observable symptom]** → wiki-query [exact terms]` — markdown in
the agent body, **not** a standalone JSON/YAML schema. Representative rows:

```
- Composable recomposing more than expected
    → wiki-query Compose recomposition stability Strong Skipping unstable types
- LaunchedEffect running on every recomposition instead of once
    → wiki-query Compose LaunchedEffect key recomposition side effects
- Effect (navigation, toast) firing on every recomposition instead of once
    → wiki-query MVI Effect Channel SharedFlow replay receiveAsFlow
- Coroutine test hangs, or delay() runs in real time
    → wiki-query Kotest coroutineTestScope TestCoroutineScheduler virtual time advanceTimeBy
- Flow emissions not arriving — awaitItem times out
    → wiki-query Turbine awaitItem awaitComplete testIn turbineScope StateFlow
- Multiplatform driver setup (Android + Desktop)
    → wiki-query SQLDelight platform drivers Android desktop JVM expect actual factory
```
9 subsections: Compose (Recomposition/Side-Effects, Layout/Modifiers/Lists, Animation), MVI/State,
Navigation, Kotest (Coroutines/Flow, Assertions/Data), SQLDelight, Ktor Client, Material3/Adaptive.
Failure handling (verbatim): *"A required wiki page does not exist or wiki-query returns no useful
results. Note it in your output. Make your best judgment call … flag the gap for the orchestrator,
and continue."*

### 2d. The authoring method
The generalized generator survives in `momentum:constitution-builder`: per concept, `wiki-query
[concept]` → read pages → write **2–4 entries**, each a *specific, observable, diagnostic* symptom +
exact query. Explicitly banned: *"Never write 'consult KB if needed.' Name the exact moment and exact
query string."* Sizing target: **15–40 routing entries, 3–8 standing-rule groups**. Symptoms target
real KB pages — `nornspun-agentic-kb/concepts/` holds 168 concept pages whose titles map ~1:1 to the
query terms.

### 2e. Rationale
Context economy through retrieval-on-symptom: the hot constitution (Tier 1) stays small, always
loaded, carrying only symptom→query pointers; the knowledge lives in the cold KB (Tier 3), accessed
on demand via `wiki-query`; the wiki may override training knowledge. Underpinned by nornspun
**SDR-007** (Two-Store Knowledge Architecture, 2026-05-07): subproject agents access parent knowledge
*only* via `wiki-query`, never by reading `docs/` directly.

---

## 3. What was tested & learned
Run repeatedly on real work and it worked: a Turbine/`awaitItem` question answered correctly from
Standing Rules with **0 wiki-query calls** (two-mode rule working as designed); spawned 4× as a real
implementer for campaign-init fixes (`BUILD SUCCESSFUL`, merged); June worktree CR build; June KB
validation confirmed *"strong, directly usable coverage."* Exposed: (1) the symptom→query *retrieval
path itself* was lightly exercised in month one (May tests answered from rules, never fired a query —
the table's value-add over rules-only is effectively un-A/B-tested); (2) `wiki-query` fell back to
**grep** ("no QMD configured"); (3) **version-pin drift** — manifesto hardcodes `CMP 1.10.2` while the
project moved to 1.11.0, exactly the staleness the routing was meant to absorb.

---

## 4. On disk vs. in-chat

| Artifact | Path | Tracking |
|---|---|---|
| The manifesto/constitution | `nornspun-client/.claude/agents/cmp-dev.md` | **NOW TRACKED** — committed `29f1a25` 2026-06-16 (was untracked; parent repo only had a symlink) |
| Committed symlink to it | `nornspun/.claude/agents/cmp-dev.md` → client | committed `d8cc33f` (2026-05-16) |
| Predecessor `frontend-dev` skill (same table) | `nornspun-client/.claude/skills/frontend-dev/SKILL.md` | tracked (`2cee38f`→`e948113`) |
| `wiki-query` engine | `nornspun-client/.claude/skills/wiki-query/SKILL.md` | UNTRACKED (related risk) |
| Cold KB vault (168 pages) | `nornspun-agentic-kb/` | **not a git repo** — no history (related risk) |
| KB-architecture decision | `nornspun/docs/decisions/sdr-007-...-2026-05-07.md` | committed |

The word "manifesto" appears in **zero** source files — the developer's "manifesto" == the committed
**constitution** (`cmp-dev.md`). No separate `*manifesto*` file, no standalone mapping JSON/YAML.

---

## 5. The three-definitions conflict (the problem this brief resolves)

| Source (verified) | "manifesto" = |
|---|---|
| **DEC-026 D4** | "agent-specific routing" (moved to agent-builder) |
| **`agent-manifesto-format-specification`** story | "role × domain matrix plus stack facts" (composition-input table, no routing) |
| **PRD FR136** | "project/sprint context overlay (current story, sprint guidelines)" |

Three definitions, none of which is the prototype's per-specialist symptom→query table. Where routing
*did* land concretely (constitution-builder `## Quick Routing`), it is **project-shared, not
per-agent/per-domain** — losing the role×domain specialization that made cmp-dev's table valuable.

---

## 6. Ratified decisions (developer, 2026-06-16)

**D1 — One definition: the manifesto IS the agent's diagnostic table.**
The three specs are imprecise attempts at the same idea. Canonical: *the manifesto is the agent's
**diagnostic table** — a **stable** (not per-story) per-role×domain table mapping observable symptoms →
exact KB routing (`wiki-query`), plus the stack facts that scope it.* The "sprint/story context
overlay" reading (FR136) is **corrected**: the manifesto is the **same** across every sprint and
story — it is the agent's standing "how everything is implemented" guidance, not a per-story
injection. **Completeness criterion:** if the agent hits a situation the manifesto doesn't guide, the
manifesto is **incomplete** (→ an acceptance criterion for the format spec). Preferred term:
**"diagnostic table."** DEC-026 / the story / FR136 are reconciled under this definition.

**D2 — KB architecture: per-project KBs, multi-KB allowed, project-scoped agents.**
`cmp-dev` and `nornspun-agentic-kb` are **nornspun** artifacts — `cmp-dev.md` is a **format exemplar
only**, never a Momentum agent. Momentum needs its **own** KB; nornspun keeps its own; **multiple KBs
are allowed**; **agents are project-scoped** (nornspun agents ≠ momentum agents). Therefore "build the
agents" now also includes **standing up each project's KB** — a distinct workstream, plus a multi-KB
support requirement on the pipeline/wiki-query interface.

---

## 7. Recommendations / story reshaping

1. **Formalize D1+D2 as a decision document** (SDR) — supersede/annotate DEC-026, the format story,
   and PRD FR136 so all read consistently. Highest-leverage action; the cohort sprint can't proceed
   coherently while three specs contradict.
2. **Adopt `cmp-dev.md` as the golden exemplar** — preserved at
   `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md` — to seed
   `agent-manifesto-format-specification` with ~35 real worked entries (entry schema
   `**[observable symptom]** → wiki-query [exact terms]`, grouped, per role×domain).
3. **Reshape stories before the sprint:** run create-story on `agent-manifesto-format-specification`
   (load the verified schema + exemplar; mark routing **per-agent**, add the completeness AC);
   decide a **manifesto-builder (generate-then-curate)** skill vs. extending `agent-builder`;
   reconcile `constitution-builder`'s shared `## Quick Routing` ownership vs. per-agent routing;
   add an AC that the pipeline must **actually produce one composed agent** (it never has — use
   cmp-dev as the validation target). Add a **momentum-KB build** story (D2).
4. **Fix the degraded retrieval path** (QMD/grep fallback) and add a **version-pin freshness check**.

---

## 8. Confidence & gaps
- **HIGH (re-verified against disk):** cmp-dev contents/structure/two-mode rule/routing table; now
  tracked at `29f1a25`; the three conflicting manifesto definitions (DEC-026 / story / FR136);
  constitution-builder tiers/entry-format/sizing.
- **MEDIUM (from transcripts):** specific test sessions and the "0 wiki-query calls in May" claim —
  consistent with the verified file's design and the "no QMD → grep" note, but not re-confirmed
  against the session logs.
- **THIN:** the cold KB vault is **not version-controlled** — the "168 pages map 1:1" claim reflects
  current disk state only, no provenance.
- The **`authored vs. generated`** and **`routing scope`** questions are forward design decisions the
  prototype *raises* (and D1/D2 begin to answer), not pure recoveries.
