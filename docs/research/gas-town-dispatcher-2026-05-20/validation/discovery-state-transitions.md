---
content_origin: research-agent
date: 2026-05-22
sub_question: "Gas City bead state machine, custom statuses, gate states, metadata, molecule state transitions"
---

# Gas City Bead State Machine, Gates, Metadata, and Molecule Transitions

## Sources Consulted

- `gastownhall/beads` — `docs/ARCHITECTURE.md` — canonical schema, status vocabulary, dependency types, status flow diagram
- `gastownhall/beads` — `docs/CLI_REFERENCE.md` — full command surface including `bd update`, `bd statuses`, `bd gate *`, `bd ready`, `bd close`, `bd query`, `bd search`
- `gastownhall/beads` — `docs/MOLECULES.md` — molecule/wisp execution model, dependency blocking semantics, molecule lifecycle
- `gastownhall/beads` — `docs/METADATA.md` — arbitrary metadata field, reserved key prefixes, advisory execution keys
- `gastownhall/beads` — `docs/FAQ.md` — ready/blocked behavior, transition examples
- `gastownhall/gascity` — `engdocs/architecture/formulas.md` — formula resolution, molecule instantiation, wisp GC
- `gastownhall/gascity` — `engdocs/architecture/life-of-a-molecule.md` — seven-phase molecule lifecycle
- `gastownhall/gascity` — `engdocs/architecture/dispatch.md` — sling routing, container expansion, open-only routing invariant
- `gastownhall/gascity` — `engdocs/architecture/controller.md` — controller loop, reconciliation, wisp GC cadence
- `gastownhall/gascity` — `engdocs/architecture/session.md` — runtime.Provider contract, crash adoption
- `gastownhall/gascity` — `engdocs/design/formula-v2-transient-retries.md` — retry semantics design, `gc.outcome`, `gc.failure_class`, `soft_fail` disposition
- `gastownhall/gascity` — `docs/reference/formula.md` — formula TOML step fields including `check`, `loop`, `condition`, `[steps.retry]`

---

## 1. Complete Bead Status Vocabulary

### Built-in statuses

CONFIRMED from `docs/ARCHITECTURE.md` (Issue Schema — Status & Workflow table):

| Status | Category | Description |
|---|---|---|
| `open` | active | Default; appears in `bd ready` and `bd list` |
| `in_progress` | active | Work claimed and underway |
| `blocked` | frozen | Explicitly marked blocked (stored status, distinct from dependency-blocked) |
| `deferred` | frozen | Hidden from `bd ready` until a `defer_until` date |
| `closed` | done | Terminal closed state |
| `tombstone` | done | Soft-delete; set `deleted_at`, `deleted_by`, `delete_reason` |
| `pinned` | — | Pinned issues; can be force-closed with `--force` |
| `hooked` | — | Listed as valid but behavior undocumented in sources reviewed |

The ARCHITECTURE.md schema table quotes the exact status string: `open`, `in_progress`, `blocked`, `deferred`, `closed`, `tombstone`, `pinned`, `hooked`.

**Note on "done":** The research question used `done` as a status. This is NOT a stored status value in the schema. It appears only as a CLI alias for `bd close`. The stored terminal status is `closed`.

**Note on "dependency-blocked":** Issues blocked by open blockers in `blocked_by` remain in `open` stored status. `bd ready` excludes them via blocker-aware logic. `bd blocked` surfaces them. The stored `blocked` status is a separate user-set flag, not the dependency-blocked state.

### Status categories and `bd ready` behavior

CONFIRMED from `bd statuses` CLI reference:

| Category | `bd ready`? | `bd list` (default)? |
|---|---|---|
| `active` | Yes | Yes |
| `wip` | No | Yes |
| `done` | No | No |
| `frozen` | No | No |

### Custom statuses

CONFIRMED: Custom statuses can be configured via:

```
bd config set status.custom "in_review:active,qa_testing:wip,on_hold:frozen"
```

Format: `<status-name>:<category>`. Category controls whether the custom status appears in `bd ready`. Statuses without a category are valid but excluded from `bd ready`.

The `bd statuses` command lists all built-in and custom statuses with icons and categories. Custom types also exist: `bd config set types.custom "..."` in `.beads/config.yaml`.

**There is no hard-coded constraint against arbitrary status names** beyond the category system. `bd update --status <value>` accepts the string; it is stored as-is.

### CLI commands driving status transitions

CONFIRMED from CLI_REFERENCE.md:

- `bd update <id> --status <value>` — general status setter; accepts any configured status string
- `bd update <id> --claim` — atomically sets status to `in_progress` and assignee to caller; idempotent if already claimed by caller
- `bd close <id> [--reason]` — sets status to `closed`; alias `done`
- `bd reopen <id> [--reason]` — sets status to `open`, clears `closed_at`; more explicit than `bd update --status open`; emits a Reopened event
- `bd update <id> --defer <date>` — sets deferral date; hides from `bd ready` until then

There is **no `bd transition` command** — transitions are driven entirely through `bd update --status`, `bd close`, `bd reopen`, and `--claim`.

### Transition constraints: FSM or open?

INFERRED: The architecture does not document an enforced finite state machine with allowed edge definitions. The status column is a string field, and `bd update --status` accepts any configured value without documented pre-condition checks. However:

- `bd close` has a `--force` flag to override pinned/unsatisfied gate blocks, implying some constraints exist at the gate/pin layer.
- `bd reopen` is specifically designed as the inverse of `bd close` and emits an explicit event, suggesting the system tracks semantic direction.
- UNKNOWN: Whether the Dolt storage layer enforces any status transition rules at the SQL constraint level. No schema constraint documentation was found in sources reviewed.

The practical answer is: **any status→status transition is permitted via `bd update --status`, with the exception that gated or pinned issues require `--force` to close**.

---

## 2. Gate States

### Gate types

CONFIRMED from `bd gate` CLI reference:

| Type | Resolution mechanism |
|---|---|
| `human` | Manual `bd gate resolve <gate-id>` (default) |
| `timer` | Auto-expires after `--timeout` duration (Phase 2) |
| `gh:run` | Waits for GitHub Actions run status=completed AND conclusion=success |
| `gh:pr` | Waits for PR state=MERGED |
| `bead` | Waits for a cross-rig bead to reach `status=closed` |

### Gate states

CONFIRMED from `bd gate check` documentation:

A gate is in one of two observable states:
- **Open** — blocking condition not yet satisfied; blocked issue does not appear in `bd ready`
- **Closed/Resolved** — condition satisfied; blocked issue becomes eligible for `bd ready`

Additionally, `bd gate check` documents an **escalated** state:
- `gh:run`: escalated when `status=completed AND conclusion in (failure, canceled)`
- `gh:pr`: escalated when `state=CLOSED` (not merged)

`bd gate check --escalate` triggers escalation of expired/failed gates. `bd gate list --all` shows closed gates. There is no distinct "rejected" gate status as a stored state — escalation is a behavior, not a persistent state distinct from closed.

### Gate reject / "changes requested" workflow

CONFIRMED: There is **no `bd gate reject` command**. The human HITL workflow for "reviewed and want changes" operates through:

1. `bd human respond <id> --response "feedback text"` — adds a comment and closes the human-needed bead
2. `bd gate resolve <gate-id> [--reason "..."]` — closes the gate with optional reason text

The feedback text is carried as a comment on the gate bead, not as a dedicated rejection payload. A human signaling "I want changes" would close the gate (unblocking the workflow) and convey the feedback via the `--reason` flag or as a separate comment — relying on the downstream agent to read that comment before proceeding.

UNKNOWN: Whether there is a standardized convention for agents to read gate close reasons before resuming work. No explicit protocol was found.

### Gate timeout and auto-escalation

CONFIRMED from `bd gate create` flags and `bd gate check` docs:

- Timer gates: `bd gate create --type=timer --timeout=2h` auto-resolves after the duration
- `bd gate check --type=timer` evaluates timer expiry
- `bd gate check --escalate` escalates failed/expired gates
- No built-in auto-escalation without explicit invocation of `bd gate check --escalate`

INFERRED: Auto-escalation requires the controller or an agent to periodically invoke `bd gate check`. There is no push-based timeout that fires without polling.

### Gate payload / metadata

CONFIRMED: Gates carry:
- `--reason string` on `bd gate create` — stored as description/reason on the gate bead
- `--await-id string` — condition identifier (run ID, PR number, cross-rig bead ID)
- Comments via `bd comment <gate-id>` — can carry arbitrary human feedback

Gates are implemented as beads with `issue_type=gate`. They inherit the full bead schema, including the `metadata` JSON field (see Section 3). Any structured payload can be stored in gate metadata.

---

## 3. Custom Bead Metadata

### Arbitrary key-value metadata

CONFIRMED from `docs/METADATA.md`:

The `metadata` field on issues accepts **arbitrary JSON**. Any valid JSON value is stored as-is. This is the documented extension point for integration, orchestration, team workflow, or experimental automation data.

Setting metadata via CLI:

```bash
bd update <id> --metadata '{"team":"platform","sprint":"2026-05-20"}'
bd update <id> --set-metadata key=value        # repeatable key=value pairs
bd update <id> --unset-metadata key            # remove a key
```

### Reserved prefixes

CONFIRMED from `docs/METADATA.md`:

| Prefix | Reserved for |
|---|---|
| `bd:` | Beads internal use |
| `_` | Internal/private keys |

User-defined keys should avoid these prefixes.

### Advisory execution keys (Gas City convention)

CONFIRMED from `docs/METADATA.md`: Gas City uses these metadata keys for agent routing:

| Key | Meaning |
|---|---|
| `execution_agent_type` | Suggested worker class: `explorer`, `worker`, `mixed` |
| `execution_suggested_model` | Suggested model for the agent |
| `execution_reasoning_effort` | `low`, `medium`, `high`, `xhigh` |
| `execution_mode` | `local`, `delegated`, or staged |
| `execution_parallel_group` | Grouping hint for parallel tasks |

These are advisory — agents should read them before spawning subagents.

Gas City's dispatch code also writes `gc.routed_to` metadata on beads when slinging to pool agents, used by `bd ready --metadata-field gc.routed_to=<target>` for pool claim semantics.

### Querying and filtering by custom metadata

CONFIRMED from `bd search` and `bd ready` CLI flags:

```bash
bd search --has-metadata-key <key>               # filter: has this key set
bd search --metadata-field key=value             # filter: key equals value (repeatable)
bd ready --has-metadata-key <key>
bd ready --metadata-field key=value              # repeatable
```

**`bd query` does NOT expose metadata fields** — the `bd query` expression language supports `status`, `priority`, `type`, `assignee`, `label`, `title`, `description`, `notes`, `created`, `updated`, `id`, `parent`, `mol_type`, and a few others, but **not** arbitrary metadata key-value filters. For metadata filtering, `bd search` or `bd ready --metadata-field` are the supported surfaces.

UNKNOWN: Whether `bd sql` (direct SQL access) can query the metadata JSON column with SQL JSON functions. This is documented as existing but no examples of metadata JSON path queries were found.

---

## 4. Bead Relationships and Graph

### Relationship types

CONFIRMED from ARCHITECTURE.md (Dependency Types table) and MOLECULES.md:

| Type | Semantic | Affects `bd ready`? |
|---|---|---|
| `blocks` | Issue X must close before Y starts | Yes |
| `parent-child` | Hierarchical; children blocked if parent blocked | Yes |
| `conditional-blocks` | Y runs only if X fails | Yes (MOLECULES.md) |
| `waits-for` | Y waits for all of X's children (fanout gate) | Yes (MOLECULES.md) |
| `related` | Soft reference link | No |
| `discovered-from` | Found during work on parent | No |
| `replies-to` | Conversational link | No (MOLECULES.md) |
| `tracks` | Available as `bd link --type tracks` per CLI | UNKNOWN |

Note: ARCHITECTURE.md lists four types (`blocks`, `parent-child`, `related`, `discovered-from`). MOLECULES.md adds `conditional-blocks`, `waits-for`, and `replies-to`. The CLI `bd link --type` accepts `blocks|tracks|related|parent-child|discovered-from`. `tracks` appears only in CLI, not in ARCHITECTURE.md or MOLECULES.md — its blocking semantics are UNKNOWN.

### Custom relationship types

UNKNOWN: No documentation found for user-defined relationship types beyond the built-in set. The type field on Dependency is a string in the schema, but whether `bd dep add --type custom-type` is accepted is not confirmed in sources reviewed.

### Dependency graph enforcement

CONFIRMED: The dependency graph is **not fully enforced as a hard constraint** at the close operation level:

- `bd close` has a `--force` flag for closing pinned or gate-blocked issues
- No documentation was found stating that `bd close` rejects a bead that has open `blocked_by` dependencies (i.e., closing a bead that is itself a blocker for another is permitted)
- `bd gate check` auto-closes resolved gates; `bd close --force` bypasses unsatisfied gates

INFERRED: The graph is primarily **advisory with gating as the enforcement mechanism**. Gates are the hard blocking primitive. Dependency links affect what appears in `bd ready` but do not prevent `bd close` operations (with or without `--force` depending on gate vs. dep type).

### How `bd ready` determines readiness

CONFIRMED from `bd ready` CLI reference and FAQ:

`bd ready` uses `GetReadyWork` API with blocker-aware semantics. An issue is ready when:

1. Stored status is `open` (not `in_progress`, `blocked`, `deferred`, `hooked`)
2. No open blockers in `blocked_by` (transitive closure of `blocks` and `parent-child` dependencies)
3. No open gates blocking the issue
4. `defer_until` timestamp has passed (or `--include-deferred` flag set)

Additional filters available: `--mol` (restrict to molecule steps), `--gated` (find molecules where a gate just closed, ready for gate-resume dispatch), `--unassigned`, `--metadata-field`, `--label`.

The `conditional-blocks` and `waits-for` types from MOLECULES.md also affect readiness, but the exact implementation is not documented in the CLI reference — INFERRED that they flow through the same GetReadyWork blocker computation.

---

## 5. Molecule/Formula State Transitions

### Molecule as a bead type

CONFIRMED from ARCHITECTURE.md: Molecules are beads with `issue_type=molecule`. They are epics with children (parent-child dependencies). There is no separate molecule database table — molecule state is bead state.

### Molecule lifecycle phases (Gas City perspective)

CONFIRMED from `engdocs/architecture/life-of-a-molecule.md`:

| Phase | Description |
|---|---|
| Phase 1: Definition | `*.formula.toml` on disk |
| Phase 2: Resolution | `ResolveFormulas()` stages winners into `.beads/formulas/` as symlinks |
| Phase 3: Instantiation | `Store.MolCook()` / `Store.MolCookOn()` creates the bead graph via `bd mol wisp` + `bd mol bond` |
| Phase 4: Routing | `gc sling` or order dispatch assigns the root bead to an agent |
| Phase 5: Execution | Agent works through child beads; `bd ready` surfaces ready steps |
| Phase 6: Completion | All child beads close; root bead transitions to `closed` |
| Phase 7: GC | `wisp_gc.go` purges closed molecules older than `wisp_ttl` |

### Molecule/wisp bead states

CONFIRMED: A molecule root bead has exactly the same status vocabulary as any other bead (`open`, `in_progress`, `closed`, etc.). There are no molecule-specific status values.

The molecule's "active" state is that its root bead is open and its child beads are being worked. There is no "executing" or "paused" molecule-level status as a distinct stored value.

**Wisps** are ephemeral molecules: `Wisp=true` flag set on the root, local-only (never exported or synced), hard-deleted on squash (no tombstone).

### Step failure states and recovery

CONFIRMED from `engdocs/design/formula-v2-transient-retries.md` (Draft design, v0):

When a molecule step (child bead) fails, the classification system uses bead metadata written by the worker:

| Outcome | Classification | Runtime behavior |
|---|---|---|
| `gc.outcome=pass` | — | Logical step closes with `gc.final_disposition=pass` |
| `gc.outcome=fail` + `gc.failure_class=hard` | Hard failure | Logical step closes with `gc.final_disposition=hard_fail`; enclosing scope may abort |
| `gc.outcome=fail` + `gc.failure_class=transient` | Transient failure | If retry budget remains: append new attempt bead; else apply `on_exhausted` policy |
| `gc.outcome=fail` missing `gc.failure_class` | Treated as hard failure | Same as hard |
| Contract violation (malformed metadata) | Treated as transient | Bounded retry rather than immediate hard-fail |

**`on_exhausted` policy** (per `[steps.retry]` formula config):
- `hard_fail` (default) — logical step closes with `gc.final_disposition=hard_fail`
- `soft_fail` — logical step closes with `gc.outcome=pass`, `gc.final_disposition=soft_fail`; enclosing workflow continues with degraded coverage

**This retry design is marked Draft (2026-03-23).** It may not yet be fully implemented in production code. INFERRED that the basic Ralph-style retry (`steps.ralph.max_attempts`) is the current production primitive; `steps.retry` with `transient`/`hard` classification is the v2 extension.

### Workflow-level outcome states

CONFIRMED (formula-v2-transient-retries design):

| `gc.outcome` | `gc.final_disposition` | Meaning |
|---|---|---|
| `pass` | `pass` | Clean success |
| `pass` | `soft_fail` | Success with degraded optional coverage |
| `fail` | `hard_fail` | Terminal failure |

### Manual molecule step advancement

CONFIRMED from `bd close` flags:

- `bd close <step-id> --continue` — auto-advance to next step in molecule (atomically claims the next ready step)
- `bd close <step-id> --no-auto` — with `--continue`, show next step without claiming it
- `bd close <step-id> --suggest-next` — show newly unblocked issues after closing

There is **no explicit "advance molecule to step N" command**. Advancement is driven by closing the current step, which unblocks the next step per the dependency graph. The molecule always resumes from the last completed step — there is no mechanism to skip steps unless the step bead is explicitly closed (with or without genuine completion).

### Step crash/hang before terminal close

CONFIRMED from formula-v2-transient-retries design (Section: "Step crash/hang before a classified result"):

If a worker crashes or hangs before writing a terminal result:
- The same attempt bead is recovered/requeued by the session/provider lifecycle
- Retry budget is **not** consumed
- No new attempt bead is appended yet
- Recovery goes through the existing session crash-adoption path in `internal/session/`

This is a critical split: classified transient failure → formula retry; unclassified crash/hang → same-attempt recovery.

---

## Synthesis

**The status vocabulary is richer than commonly documented.** Beyond the three "well-known" statuses (`open`, `in_progress`, `closed`/`done`), Beads has five additional built-in statuses (`blocked`, `deferred`, `tombstone`, `pinned`, `hooked`) and a full custom status system with category semantics. Integrators building on Beads should account for the full vocabulary, especially `deferred` and `tombstone`, which have specific `bd ready` exclusion and deletion semantics respectively.

**Gates are a single-state bead, not a state machine.** They are open or closed. Escalation is a behavioral outcome of `bd gate check --escalate`, not a distinct stored state. The absence of a `bd gate reject` command means human reviewers who want to signal "needs changes" must use the `--reason` flag or a comment — there is no structured rejection payload. Implementors who need a richer HITL feedback loop should store structured feedback in gate metadata before resolving.

**Custom metadata is the primary extension point and is well-integrated with queries.** `bd search --metadata-field` and `bd ready --metadata-field` enable metadata-based work routing. Gas City uses this pattern directly for pool demand detection (`gc.routed_to`). The `bd query` expression language does NOT expose metadata — a gap for complex compound metadata queries.

**The dependency graph is advisory, not enforced.** Closing a bead with open dependents is not prevented by the system. Only gates create hard blocking that requires `--force` to bypass. This means workflows that need strict sequencing must use gates, not merely dependency links.

**Molecule state is entirely bead state.** There is no separate "molecule state machine" — molecules are epics, their execution state is the closure state of their children, and Gas City's controller drives routing and GC. The formula-v2 retry design (Draft) adds `gc.outcome` / `gc.failure_class` metadata conventions for classifying step terminal states, but this sits on top of the standard bead close mechanism.

**Formula step failure recovery has a draft classification design that is not yet fully implemented.** The current production path uses Ralph retry loops. The `steps.retry` + `gc.failure_class=transient/hard` surface is a Draft design. Implementors should not rely on the transient/soft_fail classification in production code until it is confirmed shipped.

---

## Gap Summary

| Gap | Why it matters |
|---|---|
| `hooked` status behavior is undocumented | Cannot determine when a bead enters `hooked`, what it means for routing, or how it is cleared |
| `tracks` dependency type semantics are UNKNOWN | CLI exposes it but ARCHITECTURE.md and MOLECULES.md do not describe its blocking behavior |
| Custom relationship types: whether user-defined dep types are accepted | Relevant if dispatcher needs to define domain-specific graph edges |
| Whether `bd sql` supports JSON path queries on metadata | Determines whether complex metadata queries are possible without workaround |
| Gate close reason protocol: no standardized agent behavior for reading gate feedback | An agent resuming after a human gate has no defined way to discover the human's feedback text |
| `steps.retry` production status: Draft design vs. shipping | Formula-v2 transient retry classification may not be available in production GC v1.1.0 |
| `bd gate check --escalate` invocation ownership | Who calls this in a running city — the controller loop, the agent, or the operator? Not documented in sources reviewed |
| Transition enforcement at SQL layer | Whether Dolt schema constraints prevent invalid status transitions is UNKNOWN |
