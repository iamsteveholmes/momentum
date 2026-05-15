# Consultation Log — LaunchedEffect Recomposition Query

## Routing Decision

Symptom matched the cmp-dev routing table exactly:

> **"LaunchedEffect running on every recomposition instead of once"** → `wiki-query Compose LaunchedEffect key recomposition side effects`

Invoked `wiki-query` via Skill tool with args: `Compose LaunchedEffect key recomposition side effects`

---

## Retrieval Steps

### Step 1: hot.md scan
- hot.md confirmed a Compose Multiplatform research pass was completed (2026-05-02)
- Key takeaway in hot: "Strong Skipping Mode default in Kotlin 2.0.20+" and MVI effects patterns noted
- No direct LaunchedEffect key mention in hot.md — proceeded to index

### Step 2: Index Pass
- Scanned `index.md` for candidates
- Found two high-confidence matches:
  - `[[Compose Side Effects]]` — "All 8 Effect APIs (LaunchedEffect, DisposableEffect, SideEffect, etc.)"
  - `[[Coroutines in Compose]]` — "LaunchedEffect, collectAsStateWithLifecycle, snapshotFlow, rememberCoroutineScope"
- Also identified `[[Compose Recomposition and Stability]]` as a supporting page

### Step 3: Full Page Reads (3 pages)

**Page 1: `concepts/Compose Side Effects.md`**  
Key insight: LaunchedEffect key rules stated explicitly:
- "Pass all mutable variables used in the block as keys"
- "LaunchedEffect(true) or LaunchedEffect(Unit) = runs once for composable's lifetime"
- API comparison table confirms: `LaunchedEffect` restarts (cancel+relaunch) on every key change
- Common patterns table: "Network call on screen open → LaunchedEffect(Unit)"

**Page 2: `concepts/Coroutines in Compose.md`**  
Key insight: Reiterates key contract:
- "Keys: any value that should restart the effect; use `Unit` or `true` only for truly one-time effects"
- Common Pitfall #2 documented: "Calling `launch` in composable body without `LaunchedEffect`: creates new coroutines on every recomposition"
- Shows correct ViewModel → Compose pattern using `collectAsStateWithLifecycle()`

**Page 3: `concepts/Compose Recomposition and Stability.md`**  
Key insight: Explains what triggers recomposition (what makes the composable re-execute):
- Unstable parameters cause recomposition whenever parent recomposes
- Strong Skipping Mode (default Kotlin 2.0.20+) changes this: unstable params compared by `===` instance equality
- Confirms that a `uiState` data class containing `passwordValue` would be a new instance on every keystroke → triggers recomposition of anything that takes it as a parameter

---

## Synthesis

The answer required combining three pages:
1. **Compose Side Effects**: what the key contract IS and the fix (`Unit`)
2. **Coroutines in Compose**: why the wrong key causes the symptom (restart on every key change)
3. **Compose Recomposition and Stability**: why a state object containing `passwordValue` would itself change on every keystroke (new data class instance = recomposition trigger = key change = LaunchedEffect restart)

All three pages consulted via full read. No escalation to broad grep needed. Answer confidence: high (extracted provenance 0.92–0.95 on source pages).

---

## Log Entry Written
Appended to `/Users/steve/projects/nornspun-agentic-kb/log.md`:
```
- [2026-05-14] QUERY query="Compose LaunchedEffect key recomposition side effects" result_pages=3 mode=normal escalated=false
```
