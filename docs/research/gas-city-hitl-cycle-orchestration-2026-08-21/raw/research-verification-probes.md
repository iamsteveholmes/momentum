---
content_origin: claude-code-subagent
date: 2026-08-24
sub_question: "Live verification probes: GC_BEADS=file, FileStore metadata durability, gate persistence on file store, dashboard port, deps.env BD pin — settling AVFL-flagged contradictions"
topic: "Gas City HITL gates and cycle orchestration for Momentum"
---

All probes run live against gc 1.4.1 (installed via `mise` github backend, `mise exec -- gc version` → `1.4.1`) and bd 1.0.4 (separate, already-installed CLI — unrelated to `gc bd`, see Probe 2/3). Throwaway work performed entirely under `/private/tmp/claude-501/-Users-steve-projects-momentum/875c3989-7e5f-4d3b-90ac-d31ceae0ed8c/scratchpad/gc-probe-city/` — momentum's own `.beads`/`.momentum` were never touched. The throwaway city directory was deleted at the end of this session (see final command).

## Probe 1 — GC_BEADS=file existence [EMPIRICAL]

**Verdict: YES — the file provider is real and functional in gc 1.4.1.** `gc init` under `GC_BEADS=file` requires only `tmux` as a missing-dependency blocker (not dolt, not bd); once tmux is present, init succeeds and `gc doctor` reports 79 passed / 2 warnings (both warnings are about no tmux *server* running yet, unrelated to the file backend itself), with `dolt-server`, `dolt-noms-size`, `dolt-journal-size`, `dolt-config`, `dolt-version` all explicitly `✓ skipped (file backend or GC_DOLT=skip)` and `builtin-pack-family — builtin bd/dolt pack family not required`.

Exact commands + output:

```
$ mise ls | grep gascity
github:gastownhall/gascity                 1.4.1              ~/.config/mise/config.toml  latest
$ mise exec -- gc version
1.4.1

$ GC_BEADS=file mise exec -- gc init filecity
...
Created gascity config (Level 1) in "filecity".
gc init: missing required dependencies:

  - tmux
    Install: https://github.com/tmux/tmux/wiki/Installing

gc init: install the missing dependencies, then run 'gc start'
EXIT_CODE=1
```

Note this failure occurs even non-interactively with `--no-start`:

```
$ GC_BEADS=file mise exec -- gc init --template minimal --default-provider claude --no-start filecity2
...
Initialized city "filecity2" with default provider "claude".
gc init: missing required dependencies:

  - tmux
    Install: https://github.com/tmux/tmux/wiki/Installing

gc init: install the missing dependencies, then run 'gc start'
EXIT_CODE=1
```

Despite the exit 1, the file-backed store scaffold is already written on disk after this failing run:

```
$ find filecity -maxdepth 3 -type f
filecity/pack.toml
filecity/.gitignore
filecity/city.toml
filecity/.gc/settings.json
filecity/.gc/file-beads-layout
filecity/.gc/beads.json
filecity/.gc/site.toml
filecity/.gc/events.jsonl
filecity/agents/mayor/prompt.template.md

$ cat filecity/.gc/beads.json
{"seq":0,"beads":[]}
$ cat filecity/.gc/file-beads-layout
scope-local-v1
```

After installing tmux via mise (`mise use -g tmux@latest` → tmux 3.7b) and retrying, init succeeds cleanly:

```
$ GC_BEADS=file mise exec -- gc init --template minimal --default-provider claude --no-start filecity3
[1/8] Creating runtime scaffold
[2/8] Installing hooks (Claude Code)
[3/8] Writing default prompts
[4/8] Writing pack.toml
[5/8] Writing city configuration
Welcome to Gas City!
Initialized city "filecity3" with default provider "claude".
[6/8] Checking provider readiness
[7/8] Skipping supervisor startup
Next: cd .../filecity3 && gc start
EXIT_CODE=0

$ GC_BEADS=file mise exec -- gc doctor
  ✓ city-structure — city.toml present
  ...
  ✓ tmux-binary — found /Users/steve/.local/share/mise/installs/tmux/latest/tmux
  ...
  ✓ controller — controller not running (one-shot mode)
  ✓ supervisor-http-api — supervisor socket not running — HTTP API check skipped
2026/08/24 15:25:19 tmux state cache: refresh failed in 6.688458ms: runtime unavailable: liveness observation failed: no tmux server running
  ⚠ agent-sessions — 3 agent(s) without sessions
      hint: run gc start to reconcile sessions
  ✓ zombie-sessions — no zombie sessions
  ⚠ orphan-sessions — listing sessions partially failed: tmux server unreachable: no tmux server running
  ✓ bd-split-store — no legacy split store detected
  ✓ beads-store — store accessible
  ...
  ✓ dolt-server — skipped (file backend or GC_DOLT=skip)
  ✓ dolt-noms-size — skipped (file backend, external dolt endpoint, or GC_DOLT=skip)
  ✓ dolt-journal-size — skipped (file backend, external dolt endpoint, or GC_DOLT=skip)
  ✓ dolt-config — skipped (file backend, external dolt endpoint, or GC_DOLT=skip)
  ✓ dolt-version — skipped (file backend, external dolt endpoint, or GC_DOLT=skip)
  ✓ builtin-pack-family — builtin bd/dolt pack family not required
  ...
79 passed, 2 warnings
EXIT_CODE=0
```

**Requirement summary under `GC_BEADS=file`:** tmux is required (hard block on `gc init` regardless of `--no-start`); dolt and bd are explicitly *not* required — doctor skips every dolt-specific check and confirms "builtin bd/dolt pack family not required." The two warnings that remain are just "no tmux server started yet" (expected — we used `--no-start` and never ran `gc start`), not file-backend defects.

## Probe 2 — FileStore metadata durability [EMPIRICAL]

**Verdict: metadata IS persisted durably by the file store** — but there is no `gc bd update --set-metadata` (or any) CLI verb exposed for file-backed cities in 1.4.1. `gc bd` is entirely blocked for file backend:

```
$ GC_BEADS=file mise exec -- gc bd --help
gc bd: only supported for bd-backed beads providers (resolved "file" for .../filecity3)
  hint: .../filecity3/.gc/beads.json exists, which marks this scope as file-backed. If it is a
  stale artifact from a previous city or pre-migration layout, move it aside (e.g., rename to
  .gc/beads.json.bak). To positively mark this scope as bd-backed, add
  .../filecity3/.beads/metadata.json (with backend=dolt and the dolt_database name).
```

The full `gc beads` subcommand surface for file-backed cities is `list`/`show`/`health`/`city` only — no `create`, no `update`, no `set-metadata`. I scanned every top-level `gc` subcommand's `--help` text (`event`, `hook`, `mail`, `converge`, `convoy`, `graph`, `analyze`, `formula`, `order`) for any metadata-setting verb; none exists. Bead creation itself has no direct verb either — the only way to create a bead in file mode is indirectly, via `gc sling <target> "<text>"` (auto-creates a task bead from text and routes it):

```
$ mise exec -- gc agent list   # (in a gascity-template city, filecity4, which has a "mayor" agent)
Agents in .../filecity4:
  claude                   active
  core.control-dispatcher  active
  mayor                    active

$ GC_BEADS=file mise exec -- gc sling mayor "probe test bead for metadata durability" --no-convoy --json
{"bead_id":"gc-1","dry_run":false,"method":"bead","ok":true,"queued":false,"routed":true,"schema_version":"1","success":true,"target":"mayor"}

$ cat .gc/beads.json
{
  "seq": 1,
  "beads": [
    {
      "id": "gc-1",
      "title": "probe test bead for metadata durability",
      "status": "open",
      "issue_type": "task",
      "created_at": "2026-08-24T15:26:30.845204-07:00",
      "updated_at": "2026-08-24T15:26:30.845694-07:00",
      "metadata": { "gc.routed_to": "mayor" }
    }
  ],
  "revisions": { "gc-1": 2 },
  "revisions_sealed": true
}
```

Metadata (`gc.routed_to`, written internally by the sling/routing engine) round-trips correctly across two separate, genuinely-fresh CLI process invocations:

```
$ GC_BEADS=file mise exec -- gc beads show gc-1 --format=json   # fresh process #1
{ "id": "gc-1", ..., "metadata": { "gc.routed_to": "mayor" } }
$ GC_BEADS=file mise exec -- gc beads show gc-1 --format=json   # fresh process #2
{ "id": "gc-1", ..., "metadata": { "gc.routed_to": "mayor" } }
```

matches the on-disk file exactly. To rule out "engine-internal keys only" as a confound, I hand-edited the JSON file to add an arbitrary custom metadata key (`probe.custom_key`) and confirmed a fresh `gc` process reads it back faithfully:

```
$ python3 -c "...d['beads'][0]['metadata']['probe.custom_key']='probe-custom-value-12345'; json.dump(...)"
$ GC_BEADS=file mise exec -- gc beads show gc-1 --format=json
{
  "id": "gc-1", ...,
  "metadata": { "gc.routed_to": "mayor", "probe.custom_key": "probe-custom-value-12345" }
}
```

**Conclusion:** the FileStore's persistence/read path is real and durable — it is not a no-op — but in gc 1.4.1 there is no public CLI verb to *write* arbitrary metadata on a file-backed city (only the engine itself writes recognized keys like `gc.routed_to` as a side effect of routing). Any corpus claim of a `gc bd update --set-metadata` workflow on file-backed cities is not reproducible in 1.4.1 — `gc bd` is categorically unsupported there.

## Probe 3 — Gate + metadata on file store [EMPIRICAL]

**Verdict: gate creation is entirely inaccessible on file-backed cities in gc 1.4.1** — this is the same restriction as Probe 2, since gate creation lives under `gc bd` (i.e., `bd gate create --type=human`), which is unconditionally blocked for `GC_BEADS=file`:

```
$ GC_BEADS=file mise exec -- gc bd gate create --type=human
gc bd: only supported for bd-backed beads providers (resolved "file" for .../filecity4)
  hint: .../filecity4/.gc/beads.json exists, which marks this scope as file-backed. ...
EXIT_CODE=1
```

I also searched the full `gc` command surface for any file-mode-native gate primitive. The only "gate" concept exposed on file-backed cities is `gc converge` (convergence loops: root bead + formula + gate = repeat until the gate condition passes), which is a different mechanism (iteration-loop approval, `approve`/`test-gate`/`iterate`) — not a per-bead `await_type=human` HITL gate bead. There is no dedicated top-level `gate` command; `gc --help` lists no `gate` verb at all.

**Conclusion:** the Dolt-backed `bd gate create --type=human` HITL-gate primitive does not have a file-store equivalent in 1.4.1 — it cannot be tested for cross-restart persistence because it cannot be created in the first place on a file-backed city. Any corpus claim describing HITL gate beads working equivalently on file-backed cities is not correct for 1.4.1.

## Probe 4 — Dashboard [EMPIRICAL]

**Verdict: default port 8372, served by the machine-wide supervisor (embedded SPA, same-origin `/api`) — not a standalone static server.**

```
$ GC_BEADS=file mise exec -- gc dashboard --help
Open the GC dashboard in your browser.

The dashboard SPA is embedded in the gc binary and served same-origin by the
supervisor; it is no longer a separate static server. This command resolves the
supervisor URL, opens it in your default browser, and prints it too (or tells
you how to start the supervisor). Use --no-open to print the URL without
launching a browser.
```

Without a running supervisor, `gc dashboard --no-open` / `gc dashboard serve` just print instructions ("start it with `gc supervisor start`"). I started the supervisor (no cities were registered/started, so this came up with no active sessions), resolved the URL, curled it, then stopped it immediately:

```
$ GC_BEADS=file mise exec -- gc supervisor start
Supervisor started (PID 41305)
Dashboard:  http://127.0.0.1:8372/

$ curl -sI http://127.0.0.1:8372/
HTTP/1.1 200 OK
Cache-Control: no-store
Content-Security-Policy: default-src 'self'; script-src 'self' 'sha256-...'; style-src 'self' 'unsafe-inline'; ...
Content-Type: text/html; charset=utf-8
X-Frame-Options: DENY
Content-Length: 1140

$ curl -sI http://127.0.0.1:8372/api
HTTP/1.1 307 Temporary Redirect
Location: /api/

$ GC_BEADS=file mise exec -- gc supervisor stop
Supervisor stopping...
$ GC_BEADS=file mise exec -- gc supervisor status
Supervisor is not running
```

Port 8372 was up for well under a minute, serving only the empty dashboard SPA (no registered cities), and was shut down cleanly.

## Probe 5 — deps.env BD_VERSION pin [EMPIRICAL]

**Verdict: this settles the "v1.2.2 vs v1.1.0" pin contradiction — both figures are correct, for different refs.** The `v1.4.1` tag pins `BD_VERSION=v1.2.2`; the current `main` branch has since **downgraded** `BD_VERSION` to `v1.1.0`, with an extensive in-file comment explaining why: the capability boundary is beads#5008 (`--if-assignee`/`--if-status` on the embedded path, landed on beads main 2026-07-24), and the comment asserts that the newest *published* beads release, **v1.1.2**, predates it.

**One premise inside that upstream comment does not reconcile with this corpus's own evidence — flagged here, not resolved (reconciliation added during AVFL fix pass, COHERENCE3-A-008).** The comment calls v1.1.2 "the newest published release." But beads **v1.2.2 is published — released 2026-08-15** — and this corpus downloaded and ran it: `research-gate-mechanics-handson.md`'s environment table records `bd` 1.2.2 (`6c124203e`) fetched to scratchpad and every gate finding reproduced under it, its Sources list the beads releases page as `v1.2.2 (2026-08-15), v1.0.4 (2026-05-09)`, and gc 1.4.1's own CHANGELOG pins beads "to v1.2.2 everywhere." v1.2.2 therefore exists as a published release **and postdates beads#5008 (2026-07-24)**, so "v1.1.2 is the newest published, and it predates #5008" cannot be the whole story. Two readings survive: the `main` comment is stale with respect to the v1.2.2 release, or its "newest published" is scoped to the v1.1.x hotfix line it is reasoning about. **This probe did not settle which** — `bd 1.2.2 update --help` was never run to check for `--if-assignee`, and that is the one command that would.

**Consequence for the corpus:** the claim "CAS conditional writes are unavailable in *any* published bd release" is inherited from this upstream comment and is **[UNVERIFIED for v1.2.2 specifically]**. It holds as stated for v1.0.4 — the version Momentum actually runs — and for the v1.1.x line. `research-beads-coupling-dec028.md`'s DEC-028 multi-agent-write-safety row is annotated accordingly: its recorded direction ("the safety win is not yet purchasable") is sound for the bd Momentum has installed, but the broader "any published release" premise behind it is unsettled.

`deps.env` @ tag `v1.4.1`:
```
DOLT_VERSION=2.1.7
BD_REPO=gastownhall/beads
BD_VERSION=v1.2.2
BR_VERSION=0.1.20

BD_PREV_VERSION=v1.0.4
BD_CURRENT_VERSION=v1.1.0-rc.1
BD_CURRENT_REF=8c958d225c8357cd474ea8056c2bd9b2e35d9622
```

`deps.env` @ `main` (fetched 2026-08-24):
```
DOLT_VERSION=2.1.7
BD_REPO=gastownhall/beads
# BD_VERSION is the installable default: a PUBLISHED beads release whose tarball
# SHA is pinned in .github/scripts/install-bd-archive.sh. It cannot move past the
# conditional-write flags yet, and that is an upstream fact, not an oversight.
# The capability boundary is ONE commit: `--if-assignee`/`--if-status` (a
# rejected precondition is exit 13, nothing written, which is where the exit-13
# constant comes from) landed on beads main in 6e8af8bf8 (beads#5008,
# 2026-07-24). Compare bd pins against #5008, not against 4b1d9c875 (beads#5364,
# 2026-08-05), which only ports the same CAS to proxied-server mode — a bd after
# #5008 and before #5364 already has the flags on the embedded path this repo's
# contract exercises. The newest published release — v1.1.2 — was cut from the
# hotfix/v1.1.1 branch off v1.1.0 and predates both (verified: its
# `bd update --help` names no --if-assignee).
# Until beads publishes a release cut from main, the only flag-capable bd CI can
# obtain is the source-built BD_CURRENT_REF cell below, which is where the
# ReleaseIfCurrent CAS contract runs. Promote BD_VERSION the day that release
# exists; do not point it at an unpublished tag.
BD_VERSION=v1.1.0
BR_VERSION=0.1.20

BD_PREV_VERSION=v1.0.4
BD_CURRENT_VERSION=v1.1.1-0.20260805093327-bf97b73749ac
BD_CURRENT_REF=bf97b73749ac3ef2fca2365b54537ac041ad4293
```

Key deltas main vs. v1.4.1: `DOLT_VERSION` unchanged (2.1.7 both refs). `BD_VERSION` went v1.2.2 → v1.1.0 (a deliberate downgrade, documented inline, driven by an upstream beads capability gap — as the inline comment tells it, the CAS precondition flags gascity's contract tests require on the embedded path are absent from v1.0.4 and from the v1.1.x line, including v1.1.2, which branched off v1.1.0 before the fix. **Scoped at iter4 (ACCURACY4-A-003 / STRUCTURAL4-A-001):** the comment generalizes that to "no published release," but it is written against a "newest published = v1.1.2" premise, and beads **v1.2.2 (2026-08-15)** postdates `beads#5008` — on the comment's own logic such a release would be expected to *carry* the flags. v1.2.2 was never checked for them, so the universal is **[UNVERIFIED for v1.2.2]** and only the v1.0.4/v1.1.x scoping is supported here). `BD_CURRENT_VERSION` moved from `v1.1.0-rc.1` to a pseudo-version `v1.1.1-0.20260805093327-bf97b73749ac` (a newer source-built commit off beads main). `BD_PREV_VERSION` unchanged at v1.0.4 (also documented on main as load-bearing: it's the floor keeping `BdStore`'s raw-SQL release fallback alive).

**Conclusion for the corpus:** any document citing `BD_VERSION=v1.2.2` is describing the v1.4.1 tag; any document citing `BD_VERSION=v1.1.0` is describing current main (post-downgrade, as of 2026-08-24). These are not in conflict — they are different points in time, and main is *older-pinned* than the v1.4.1 tag on this specific field due to an upstream blocker, which is worth flagging explicitly in the corpus since it's counter-intuitive (main usually tracks ahead, not behind). **Carry the caveat above with the pin, though:** the comment's "the newest published release — v1.1.2" is not reconcilable with published-and-exercised v1.2.2 (2026-08-15), so any downstream claim that CAS is unreachable from *every* published bd release is verified only for v1.0.4 and the v1.1.x line, not for v1.2.2.

---

Throwaway city cleaned up at end of session:
```
$ rm -rf /private/tmp/.../scratchpad/gc-probe-city
```
`/Users/steve/projects/momentum`'s own `.beads`/`.momentum` were never touched by any probe.

## Sources

- Live CLI output: `gc` 1.4.1 (installed via `mise`, github backend `gastownhall/gascity`), run under `GC_BEADS=file` in a throwaway city directory, 2026-08-24.
- `bd` 1.0.4 (unrelated, already-installed CLI — confirmed distinct from `gc bd`, which shells out to a *different*, dolt-backed bd integration and is unsupported for file-backed cities).
- https://raw.githubusercontent.com/gastownhall/gascity/v1.4.1/deps.env (fetched 2026-08-24)
- https://raw.githubusercontent.com/gastownhall/gascity/main/deps.env (fetched 2026-08-24)
