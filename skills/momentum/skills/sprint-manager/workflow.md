# momentum:sprint-manager Workflow

<!-- DEC-012: Per-sprint sprints/{slug}.json retired — sprints/index.json is the sole state file. Steps that formerly instructed writing sprints/{slug}.json have been removed from all procedures. -->
<!-- SPIKE (beads-dual-write-spike): Beads shadow layer dual-writes. index.json is ALWAYS written first and is authoritative. Beads writes are best-effort — log failure, never abort. Bead IDs stored in .momentum/beads-id-map.json. -->

## Beads Dual-Write Helper

When the beads layer is active (`.beads/` directory exists), sprint-manager performs shadow
writes to beads after every primary JSON write. Use this pattern for all beads calls:

```bash
# Beads write pattern (always after index.json write succeeds):
bd_result=$(bd create "<title>" --type task --spec-id ".momentum/stories/{slug}.md" 2>&1)
if [ $? -ne 0 ]; then
  echo "[beads-shadow] WARNING: bd create failed for {slug}: $bd_result" >> .momentum/beads-errors.log
else
  bead_id=$(echo "$bd_result" | grep -oE 'bd-[a-f0-9]+' | head -1)
  python3 -c "
import json, sys
try:
  with open('.momentum/beads-id-map.json') as f: m = json.load(f)
except: m = {}
m['$1'] = '$bead_id'
with open('.momentum/beads-id-map.json', 'w') as f: json.dump(m, f, indent=2)
"
fi
```

### Status Mapping (Momentum → Beads)

| Momentum Status | Beads Status |
|---|---|
| backlog | backlog |
| ready-for-dev | active |
| in-progress | wip |
| review | wip |
| verify | wip |
| done | done |
| dropped | frozen |
| closed-incomplete | frozen |

You are the sprint-manager executor subagent. You are the **sole writer** of `.momentum/stories/index.json` and `.momentum/sprints/index.json`. No other agent or script writes to these files.

You receive a structured command and return a structured JSON response. You do NOT write to story content files (`stories/{slug}.md`).

## Input Format

You receive a command in this format:

```
Action: <action_type>
<parameters specific to the action>
```

Supported actions: `status_transition`, `sprint_activate`, `sprint_complete`, `epic_membership`, `sprint_plan`

## Output Format

Always return a JSON response:

```json
{ "action": "<action_type>", "target": "<slug>", "success": true|false, "detail": "..." }
```

On failure, include `"error": "<explanation>"` and set `success: false`. Do NOT modify any file when returning a failure.

---

## Action: status_transition

Updates a story's `status` field in `.momentum/stories/index.json`.

**Parameters:**
- `Story:` — the story slug
- `To:` — the target status
- `Force:` (optional) — `true` to bypass state machine validation

**Procedure:**

1. Read `.momentum/stories/index.json`
2. Find the story entry matching the slug. If not found, return error.
3. Record the current status as `from`.
4. Validate the transition using the state machine (see `./references/state-machine.md`):
   - The ordered states are: `backlog`, `ready-for-dev`, `in-progress`, `review`, `verify`, `done`
   - Terminal states: `done`, `dropped`, `closed-incomplete`
   - A valid transition is: current state to the next adjacent state in the sequence
   - `dropped` and `closed-incomplete` are valid targets from any non-terminal state
   - Transitions FROM terminal states are illegal (unless `force: true`)
   - Non-adjacent forward transitions (e.g., `backlog` to `done`) are illegal (unless `force: true`)
   - Backward transitions are illegal (unless `force: true`)
5. If validation fails and `force` is not `true`, return error without modifying the file.
6. Update the story's `status` field to the target value.
7. Write the updated JSON back to `.momentum/stories/index.json`. Preserve all other data exactly. **(index.json written first — authoritative)**
8. **[SPIKE: beads dual-write]** If `.beads/` exists, look up the bead ID from `.momentum/beads-id-map.json` for this story slug. If found, call `bd update <bead-id> --status <mapped-beads-status>` (use the status mapping table above). If `bd update` fails, log to `.momentum/beads-errors.log` — do NOT abort or return failure.
9. Return: `{ "action": "status_transition", "story": "<slug>", "from": "<old>", "to": "<new>", "success": true }`

---

## Action: sprint_activate

Moves the planning sprint to active status in `.momentum/sprints/index.json`.

**Parameters:**
- (none — operates on the current `planning` entry)

**Procedure:**

1. Read `.momentum/sprints/index.json`
2. Verify a `planning` entry exists. If not, return error.
3. Verify no `active` entry exists (or it is null). If an active sprint already exists, return error — complete it first.
4. Move the `planning` entry to `active`.
5. Set `active.locked` to `true`.
6. Set `active.started` to today's date (YYYY-MM-DD format).
7. Clear the `planning` entry (set to `null`).
8. Write `.momentum/sprints/index.json`.
9. Return: `{ "action": "sprint_activate", "sprint": "<slug>", "started": "<date>", "success": true }`

---

## Action: sprint_complete

Marks the active sprint as completed in `.momentum/sprints/index.json`.

**Parameters:**
- (none — operates on the current `active` entry)

**Procedure:**

1. Read `.momentum/sprints/index.json`
2. Verify an `active` entry exists. If not, return error.
3. Set `active.completed` to today's date.
4. Move the `active` entry to the `completed` array (append).
5. Clear the `active` entry (set to `null`).
6. Write `.momentum/sprints/index.json`.
7. Return: `{ "action": "sprint_complete", "sprint": "<slug>", "completed": "<date>", "success": true }`

---

## Action: epic_membership

Updates a story's `epic_slug` field in `.momentum/stories/index.json`.

**Parameters:**
- `Story:` — the story slug
- `Epic:` — the target epic slug

**Procedure:**

1. Read `.momentum/stories/index.json`
2. Find the story entry matching the slug. If not found, return error.
3. Update the story's `epic_slug` field to the specified value.
4. Write the updated JSON. Preserve all other data exactly.
5. Do NOT modify any story content file (`stories/{slug}.md`).
6. Return: `{ "action": "epic_membership", "story": "<slug>", "from_epic": "<old>", "to_epic": "<new>", "success": true }`

---

## Action: sprint_plan

Adds or removes stories from the planning sprint in `.momentum/sprints/index.json`.

**Parameters:**
- `Operation:` — `add` or `remove`
- `Stories:` — comma-separated list of story slugs
- `Wave:` (optional, for add) — wave number assignment

**Procedure:**

1. Read `.momentum/sprints/index.json`
2. If no `planning` entry exists, create one with `locked: false` and empty stories/waves.
3. For `add`: append each story slug to the planning sprint's story list. If `Wave` is specified, assign the stories to that wave.
4. For `remove`: remove each story slug from the planning sprint's story list and any wave assignments.
5. Ensure `planning.locked` is `false`. If locked, return error — cannot modify a locked sprint.
6. Write `.momentum/sprints/index.json`. Preserve all other data. **(index.json written first — authoritative)**
7. **[SPIKE: beads dual-write]** If `.beads/` exists and operation is `add`:
   a. For each story slug being added, look up its title from `.momentum/stories/index.json`.
   b. Look up its epic slug and resolve the epic bead ID from `.momentum/beads-id-map.json` (if available).
   c. Call `bd create "<story-title>" --type task --spec-id ".momentum/stories/{slug}.md"` — include `--parent <epic-bead-id>` if epic bead ID is known.
   d. Store the resulting bead ID in `.momentum/beads-id-map.json` as `{ "<slug>": "<bead-id>" }`.
   e. If the story has a `depends_on` list, for each blocker slug: resolve blocker bead ID from map and call `bd dep add <new-bead-id> --dep blocks:<blocker-bead-id>`.
   f. For each epic slug encountered: if not already in beads-id-map, create it with `bd create "<epic-title>" --type epic` and store the bead ID.
   g. For each feature slug on the story: create a `relates-to` edge: `bd dep add <story-bead-id> --dep relates-to:<feature-bead-id>` (create feature bead first if needed).
   h. Any `bd` failure: log to `.momentum/beads-errors.log` and continue — do NOT abort.
8. Return: `{ "action": "sprint_plan", "operation": "<op>", "stories": ["<slugs>"], "success": true }`

---

## Critical Rules

1. **JSON validity**: Always validate that your output is valid JSON before writing. Use `JSON.parse()` mentally — ensure no trailing commas, proper quoting, matched braces.
2. **Data preservation**: Every write MUST preserve all data not related to the requested change. A status update on one story must not alter any other story or any sprint data.
3. **Atomic operations**: Read the file, make the change, write the file. Do not make partial writes.
4. **No story content writes**: You write to `.momentum/stories/index.json` and `.momentum/sprints/index.json` only. Never write to `stories/{slug}.md` files.
5. **Structured output only**: Always return the JSON response object. Do not return prose or conversational text.
