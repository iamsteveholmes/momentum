---
title: Verification routing re-key to assembled surface + DoD reachability item
story_key: verification-routing-re-key-to-assembled-surface-dod
status: ready-for-dev
epic_slug: momentum-quality-gates-enforced
feature_slug:
story_type: practice
priority: high
change_type:
  - skill-instruction
  - agent-definition
  - script-code
  - config-structure
verification_method_advisory: bash
depends_on: []
touches:
  - skills/momentum/references/rules/verification-standard.md
  - skills/momentum/skills/create-story/references/change-types.md
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/agents/e2e-validator.md
  - skills/momentum/agents/qa-reviewer.md
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/sprint-planning/references/contract-format-guide.md
  - skills/momentum/skills/create-story/workflow.md
  - skills/momentum/skills/create-story/evals/eval-selects-method-unambiguous.md
  - skills/momentum/skills/create-story/evals/eval-escalates-on-ambiguous-routing.md
  - skills/momentum/scripts/test-momentum-tools.py
  - momentum/verification-harness.json
---

# Verification routing re-key to assembled surface + DoD reachability item

## Story

As a developer,
I want the Method Routing Table in `verification-standard.md` re-keyed from `change_type`
(a property of the diff) to **assembled surface** (where a user actually meets the
behavior), and a new Definition of Done item requiring reachability from the
application's entry point,
so that user-facing conversational behavior stops being routed to API-only
verification just because its diff happened to touch backend code, and stories can
no longer be marked done while the capability they claim to deliver is unreachable
by an end user.

## Description

Today `verification-standard.md` §1 routes verification by `change_type` — which files
the diff touched. `backend` maps unconditionally to `curl`. That mapping is the defect:
a story whose behavior a user meets by typing into a chat UI gets verified by an HTTP
call the user will never make, and passes. The diff is a property of the implementation;
the surface is a property of the product. Verification must key on the product.

This story re-keys §1 to **assembled surface** — where a user meets the behavior in the
running, assembled product. The existing closed method enum (`skill-invoke`,
`behavioral-trigger`, `bash`, `smoke`, `curl`, `document-review`) is unchanged; only the
key changes. `change_type` is demoted from routing key to a **default inference** used
when a story declares no surface, and that inference can never override a declared one.

It also adds one Definition of Done item that applies to every story regardless of type:
*the capability is reachable from the application's entry point by a user who has read
no code.* Without it, a no-op settings gear, an empty `SurfaceType` enum, and a heroes
API with zero callers all counted as done.

The routing table is duplicated in four places beyond the rule itself, plus mirrored as a
Python constant. Re-keying the rule while leaving those copies keyed on `change_type`
would leave the system enforcing the old behavior. Reconciling every copy is part of this
story, not follow-up work.

**Pain context (Nornspun delivery discovery, 2026-08-02):** `backend → curl` routed
user-facing conversational stories to API-only verification. All three adversarial
council seats converged on this fix independently. Ten sprints shipped zero of fifteen
features; a silent-skip CI class alone shipped green three sprints running.

## Acceptance Criteria

1. **§1 is keyed on assembled surface.** The Method Routing Table in
   `skills/momentum/references/rules/verification-standard.md` §1 has assembled surface as
   its key column. It defines a closed enum of surfaces, and each surface maps to exactly
   one required method drawn from the existing enum (`skill-invoke`, `behavioral-trigger`,
   `bash`, `smoke`, `curl`, `document-review`). No new method tokens are introduced, and no
   existing method token is removed or renamed.

2. **The rule says plainly what a surface is.** §1 states in prose that assembled surface
   means where a user meets the behavior in the running, assembled product — not which
   files the diff touched — and carries the governing example: a conversational behavior a
   user meets in the chat UI is driven through the chat UI even when its diff touched only
   backend files.

3. **`change_type` is demoted to a default inference.** The rule states that `change_type`
   supplies a *starting guess* at the surface, used only when a story declares no surface,
   and that a declared surface always wins over the inference. A reader of §1 alone can tell
   which field is the routing key and which is the fallback.

4. **No unconditional `backend → curl` mapping survives anywhere.** A story whose diff
   touches backend code but whose behavior is met in the application UI routes to the
   application-UI surface (`smoke`), not `curl`. The `curl` method applies only when the
   HTTP endpoint is itself the surface its consumer meets. Searching the repository for a
   surviving unconditional `backend` → `curl` mapping returns no hits in any rule, agent,
   workflow, reference guide, or script.

5. **Every story's routing is visible, never silent.** A story that declares a surface
   routes on it. A story that declares none routes on the inference, and the inferred
   surface is written into the story or its frozen contract so a reader can see which
   surface governed — no story is verified against a surface nobody recorded.

6. **The exception is declared out loud at plan time.** A story may declare that its
   capability cannot be verified through its assembled surface only via a written
   declaration in its frozen contract naming three things: the surface that cannot be
   driven, why it cannot be driven, and the substitute method. The declaration is authored
   by the story creator or product owner, never by the validator. A declaration missing any
   of the three fields is invalid, and the surface's required method applies instead.

7. **One override path, not two.** The surface-exception mechanism and the existing §2
   Method Override are reconciled into a single documented override mechanism. The rule
   does not contain two independent, differently-worded ways to substitute a method, and no
   sentence in the rule contradicts another about when substitution is permitted.

8. **The Definition of Done gains reachability.** `verification-standard.md` carries a
   Definition of Done item, applying to every story regardless of change type or surface:
   *the capability is reachable from the application's entry point by a user who has read no
   code.* It is stated once as a universal item, not repeated per change type.

9. **The reachability item reaches developers.** The Definition-of-Done checklists in
   `skills/momentum/skills/create-story/references/change-types.md` carry the reachability
   item, so a story generated by `momentum:create-story` shows it to the implementing
   developer. Running `momentum:create-story` on any story produces a Momentum
   Implementation Guide whose DoD includes the reachability line.

10. **Every copy of the routing table agrees with the rule.** After the change, these all
    describe surface-based routing and agree with §1 on every surface-to-method pair:
    `skills/momentum/scripts/momentum-tools.py` (the `CHANGE_TYPE_TO_VERIFICATION_METHOD`
    constant and `compute_verification_method`), `skills/momentum/agents/e2e-validator.md`
    (its own routing table), `skills/momentum/agents/qa-reviewer.md` (its §2–§3 references,
    plus a new §1 citation where the silent-downgrade guard cites surface-based routing),
    `skills/momentum/skills/sprint-planning/workflow.md` (contract authoring and Gherkin
    routing), `skills/momentum/skills/sprint-planning/references/contract-format-guide.md`
    (the extension/driver table), `skills/momentum/skills/create-story/workflow.md` (Step 5
    method selection), and `momentum/verification-harness.json`
    (`defaults.execution_surfaces`).

11. **Existing stories keep routing.** A story already in `.momentum/stories/index.json` that
    carries a `change_type` and no declared surface still resolves to a verification method
    through the inference path. Asking the tooling to compute a method for such a story
    returns a valid method token rather than an error or an empty value, so no in-flight
    sprint is blocked by the re-key. Conversely, a story whose index entry declares
    `surface: chat-ui` resolves to `smoke` regardless of its `change_type` — a backend-only
    diff with a declared chat-ui surface never routes to `curl`.

## Tasks / Subtasks

- [ ] **Task 1 — Re-key §1 of `verification-standard.md` to assembled surface** (AC 1, 2, 3, 4)
  - [ ] Replace the `change_type` key column with an assembled-surface key column; define the
        closed surface enum and its one-to-one mapping onto the existing method enum. Two
        things are pinned now so the frozen contract can seed fixtures (the rest of the enum
        is this task's design): the declared surface is recorded as a single `surface` token
        on the story's index entry and frontmatter, and the enum includes at least `chat-ui`
        and `application-ui`, both routing to `smoke`
  - [ ] Write the prose definition of assembled surface plus the chat-UI governing example
  - [ ] Add the `change_type` → surface inference table, labelled explicitly as a fallback
        that a declared surface overrides
  - [ ] Remove the unconditional `backend → curl` row; state the narrowed condition under
        which `curl` is correct
  - [ ] Update the frontmatter `source_decisions` to record DEC-040 D7 amending DEC-029

- [ ] **Task 2 — Reconcile the override mechanisms into one** (AC 5, 6, 7)
  - [ ] Fold the plan-time surface exception and §2 Method Override into a single documented
        override path with the three required fields (surface, reason, substitute method)
  - [ ] State the authorship constraint (story creator or product owner, never the validator)
        and the invalid-declaration fallback
  - [ ] State the visibility requirement: the governing surface — declared or inferred — is
        recorded on the story or its frozen contract
  - [ ] Re-read §1–§5 end to end and confirm no two sentences contradict on substitution

- [ ] **Task 3 — Add the universal reachability Definition of Done item** (AC 8)
  - [ ] Add a Definition of Done section to `verification-standard.md` carrying the
        reachability item as a single universal statement
  - [ ] Confirm it is not duplicated per change type or per surface

- [ ] **Task 4 — Carry reachability into the generated-story DoD** (AC 9)
  - [ ] Add the reachability line via an always-included "Universal DoD" block in the Header
        Template of `skills/momentum/skills/create-story/references/change-types.md` — not by
        editing each per-type checklist block, which would miss change types without a
        template (`script-cli`, `agent-definition`, `backend`, `research-spike`) and duplicate
        the line for multi-type stories
  - [ ] Confirm the header template surfaces it for stories of every change type, including
        types that have no per-type injection template

- [ ] **Task 5 — Update the Python routing constant and resolver** (AC 3, 4, 10, 11)
  - [ ] Re-key `CHANGE_TYPE_TO_VERIFICATION_METHOD` and `compute_verification_method` in
        `skills/momentum/scripts/momentum-tools.py` so surface is the primary input and
        `change_type` is the inference fallback
  - [ ] Preserve the existing degradation behavior: empty, unknown, or list-valued input
        still returns a valid method token rather than raising
  - [ ] Keep `CHANGE_TYPE_PRECEDENCE` consistent with whatever multi-value resolution §1
        specifies after the re-key
  - [ ] Update the six existing `test_compute_verification_method_*` functions in
        `skills/momentum/scripts/test-momentum-tools.py` (lines ~3435–3538) — all currently
        parameterized purely by `change_type` — to assert surface-primary behavior with
        `change_type` as the inference fallback
  - [ ] Exercise `momentum-tools.py sprint compute-verification-method --story <slug>`
        against an existing surface-less story and confirm a valid token comes back

- [ ] **Task 6 — Reconcile the agent-definition copies** (AC 10)
  - [ ] Re-key the routing table in `skills/momentum/agents/e2e-validator.md` to assembled
        surface, keeping its driver column aligned with §1
  - [ ] Update `skills/momentum/agents/qa-reviewer.md`'s §2–§3 references — adding a §1
        citation — so its silent-downgrade guard cites surface-based routing

- [ ] **Task 7 — Reconcile the workflow and reference-guide copies** (AC 10)
  - [ ] Update `skills/momentum/skills/sprint-planning/workflow.md` contract-authoring and
        Gherkin-routing steps to read the surface key
  - [ ] Re-key the extension/driver table in
        `skills/momentum/skills/sprint-planning/references/contract-format-guide.md`
  - [ ] Update `skills/momentum/skills/create-story/workflow.md` Step 5 to select method by
        surface, including how it resolves a story that declares none

- [ ] **Task 8 — Re-key the harness config** (AC 10)
  - [ ] Re-key `defaults.execution_surfaces` in `momentum/verification-harness.json` to the
        surface enum; confirm the file parses and every key matches §1's enum exactly
  - [ ] Re-key the `project` array's template entry (`example-product-app`) the same way —
        its own `execution_surfaces` block is change_type-keyed and carries an unconditional
        `backend → curl` mapping, exactly the pattern AC 4 eliminates

- [ ] **Task 9 — Consumer sweep and no-dangling-rule verification** (AC 4, 10, 11)
  - [ ] Search the repository for surviving `change_type`-keyed routing mappings and for any
        unconditional `backend` → `curl` pair; confirm none remain outside historical
        research and decision documents — sweep JSON config values (harness files, nested
        project templates) explicitly, not only prose and markdown routing tables
  - [ ] Confirm every surface-to-method pair is identical across the rule, the Python
        constant, both agent files, both workflows, the contract-format guide, and the
        harness config
  - [ ] Record the sweep result in the Dev Agent Record

## Dev Notes

### Decision Authority

The authoritative source is **DEC-040 directive D7** —
`_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`,
which **amends DEC-029**. Where DEC-029's original `change_type`-keyed routing conflicts
with D7, D7 governs. Implement the amendment, not the original.

D7 as adopted, verbatim in substance:

> Re-key verification-standard.md's routing table from `change_type` (which files the diff
> touches) to assembled surface (where a user meets the behavior); add one Definition of
> Done item: "the capability is reachable from the application's entry point by a user who
> has read no code." A story whose behavior a user meets in the chat UI is driven through
> the chat UI regardless of its diff — or declares at plan time, out loud, that it cannot be.

Receipt cited in the decision: `backend → curl` routed user-facing conversational stories
to API-only verification; the DoD's missing reachability item let a settings gear, an empty
`SurfaceType` enum, and a heroes API with no callers all count as done.

### Current State of Affected Files

- **`skills/momentum/references/rules/verification-standard.md`** (138 lines) — §1 Method
  Routing Table is keyed `change_type` → method across ten rows, including
  `backend | curl`. §2 Method Override permits substitution given a written justification in
  the frozen contract, authored by creator or owner, never the validator. §3 requires a
  harness-profile declaration. §4 is the anti-insider-knowledge guard. §5 declares the
  routing table non-overridable at lower scope. Frontmatter `source_decisions` currently
  reads `DEC-029 D1, D3, D6, D7` — the D7 there is DEC-029's, not DEC-040's.

- **`skills/momentum/scripts/momentum-tools.py`** — `CHANGE_TYPE_TO_VERIFICATION_METHOD`
  (a ten-entry dict whose comment names verification-standard.md §1 as its source of truth),
  `CHANGE_TYPE_PRECEDENCE` (multi-type tie-break, `app-ui` highest), and
  `compute_verification_method`, which splits `+`/`,`-joined strings, tolerates a list, and
  falls back to `document-review`. Exposed as
  `sprint compute-verification-method --story SLUG`, called by sprint-planning Step 3.5 to
  populate Part-A contract headers. **This graceful-degradation behavior must survive the
  re-key** — it is what keeps a malformed index from aborting a sprint.

- **`skills/momentum/agents/e2e-validator.md`** — carries its own full routing table under
  "Verification Routing" with an extra Driver column, and reads
  `defaults.execution_surfaces` from the harness. A second independent copy of the mapping.

- **`skills/momentum/agents/qa-reviewer.md`** — cites verification-standard.md §2 (override
  authorship) and §3 (harness-profile non-compliance → verdict `BLOCKED`). Does not carry
  its own table but routes on the frozen contract's Part-A `verification_method` and
  `harness_profile`. Its silent-downgrade guard is the enforcement point.

- **`skills/momentum/skills/sprint-planning/workflow.md`** — loads §1 to compute
  `verification_method` during contract authoring, and again to decide which stories get
  behavioral Gherkin contracts by looking up the routing token.

- **`skills/momentum/skills/sprint-planning/references/contract-format-guide.md`** — a
  third copy: `change_type` → file extension → harness driver, including
  `backend | .smoke.sh | curl`.

- **`skills/momentum/skills/create-story/workflow.md`** — Step 5 loads §1, maps each
  classified task's change type to a method, filters `specification`, and escalates to the
  developer when two or more distinct methods survive.

- **`momentum/verification-harness.json`** — `defaults.execution_surfaces` is a
  `change_type`-keyed map whose ten values are all currently `"skip"` — despite the field
  name it is keyed on change type, not assembled surface, and is the map this story re-keys.
  `driver_bindings` is already populated (six entries keyed on method token, each carrying a
  driver) and is unaffected by the re-key, since the method enum itself is unchanged. The
  `project` array's template entry (`example-product-app`) carries its own change_type-keyed
  `execution_surfaces` block — including an unconditional `backend → curl` mapping — and must
  be re-keyed alongside `defaults` (Task 8).

- **`skills/momentum/skills/create-story/references/change-types.md`** — detection heuristics
  plus per-change-type injection templates, each ending in a DoD checklist block. There is
  no universal DoD block today; the reachability item needs a home that reaches every
  generated story regardless of type.

### Architecture Compliance

- The method enum is a **closed enum** and equals the `driver_bindings` keys in
  `momentum/verification-harness.json`. The re-key changes the routing key only. Introducing
  a new method token, or renaming one, breaks the harness contract and AC 1.
- §5 declares the routing table globally non-overridable — project and path scopes may not
  replace, remove, or redefine routing entries. The surface-keyed table inherits that
  property; do not weaken §5 to accommodate the new key.
- The anti-insider-knowledge guard (§4) is unchanged and still applies. Surface-based
  routing strengthens it: driving a behavior through the surface a user meets is, by
  construction, ordinary-user knowledge.
- Verification-method values must remain closed-enum tokens — hyphenated, lowercase, no
  spaces — never free-text descriptions or legacy aliases (`eval`, `trigger`, `review`,
  `gherkin`, `skip`).

### Testing Requirements

No unit-test suite governs the rule text. Verification is behavioral and by execution:

- **Rule and template changes** (Tasks 1–4, 6, 7): confirm by reading each file end to end
  that every surface-to-method pair matches §1 and no sentence contradicts another. The
  no-dangling-rule check in Task 9 is a repository-wide search, and its result is the
  evidence for AC 4 and AC 10.
- **Python change** (Task 5): run
  `momentum-tools.py sprint compute-verification-method --story <slug>` against at least one
  real story that has a `change_type` and no declared surface. A valid method token must come
  back. Also exercise the degradation paths — empty value, unknown value, list value — and
  confirm each returns a token rather than raising. This is the AC 11 evidence.
- **Config change** (Task 8): `momentum/verification-harness.json` must parse cleanly, and
  every key in `defaults.execution_surfaces` must appear in §1's surface enum.
- **Generated-story check** (Task 4 / AC 9): run `momentum:create-story` and confirm the
  reachability line appears in the resulting Momentum Implementation Guide DoD.

### Project Structure Notes

All edits are in this repository. The rule is a `skills/**/references/` file, so it is
`skill-instruction` by the change-types disambiguation rule (files under `skills/*/` are
skill-instruction; only files under `.claude/rules/` are `rule-hook`). The two agent files
under `skills/momentum/agents/` are `agent-definition`. `momentum-tools.py` is `script-code`.
`verification-harness.json` is `config-structure`.

The routing table exists in five places (rule, Python constant, e2e-validator, contract-format
guide, harness config) with two more consumers reading it (sprint-planning, create-story). That
duplication is the story's main risk: a partial re-key leaves the system enforcing
`change_type` routing through whichever copy an agent happens to read. Task 9 exists to close
that specifically, and AC 10 names every file so none is missed.

### References

- Source decision: **DEC-040 D7** — `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md` (amends DEC-029; see also the amendment note at line 25)
- Amended decision: **DEC-029** — the original `change_type`-keyed routing standard
- Discovery that produced D7: `docs/research/nornspun-delivery-discovery-2026-08-02/synthesis.md` and the three council seat positions under `council/`
- Artifact under change: `skills/momentum/references/rules/verification-standard.md`
- Epic context: `momentum-quality-gates-enforced` (from _bmad-output/planning-artifacts/epics.json)

### Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 7 → `skill-instruction` (EDD)
- Task 5 → `script-code` (TDD-delegated)
- Task 6 → `agent-definition` (EDD)
- Task 8 → `config-structure` (direct + inspect)
- Task 9 → verification sweep across all of the above

#### skill-instruction and agent-definition Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for rule files, workflow files, or agent definitions.** These are
non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before editing:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/create-story/evals/` (this story's
   changes are exercised through create-story Step 5 and sprint-planning contract authoring).
   Two existing evals are directly relevant and must be updated rather than duplicated:
   `eval-selects-method-unambiguous.md` and `eval-escalates-on-ambiguous-routing.md` — both
   currently assert `change_type`-keyed selection and will assert the wrong thing after the
   re-key. Format each eval as: "Given [input and context], the skill should [observable
   behavior]." Test decisions and routing outcomes, not exact wording.
2. Cover at minimum: a story whose diff is backend-only but whose behavior is met in the app
   UI routes to `smoke`, not `curl`; and a story that declares no surface still resolves via
   the inference path.

**Then implement:** make the edits in Tasks 1–4, 6, 7.

**Then verify:** for each eval, spawn a subagent with the eval's scenario as its task and the
edited rule/workflow contents as context. Observe whether behavior matches. Max 3
revise-and-rerun cycles; surface to the developer if still failing.

**NFR compliance:** any `SKILL.md` touched must keep `description` ≤150 characters, retain
`model:` and `effort:` frontmatter, and keep its body under 500 lines / 5000 tokens with
overflow in `references/`.

**DoD additions:**
- [ ] 2+ behavioral evals written or updated; the two stale create-story evals reconciled
- [ ] EDD cycle ran — all eval behaviors confirmed, or failures documented with explanation
- [ ] Every surface-to-method pair identical across rule, agents, workflows, and guides
- [ ] AVFL checkpoint on produced artifacts documented (`momentum:dev` runs this automatically)

#### script-code Task: TDD Delegation

Task 5 changes executable Python. Delegate implementation to `bmad-dev-story` and follow its
TDD cycle. The existing graceful-degradation contract in `compute_verification_method` —
empty, unknown, and list-valued input all return a valid token rather than raising — is
load-bearing for in-flight sprints and must be preserved and re-exercised, not assumed.

**DoD additions:**
- [ ] `compute_verification_method` exercised against real story slugs via the CLI, output recorded
- [ ] Degradation paths (empty / unknown / list) confirmed to return a token, not raise
- [ ] `CHANGE_TYPE_PRECEDENCE` consistent with §1's multi-value resolution after re-key

#### config-structure Task: Direct Implementation + Inspection

Task 8 needs no tests or evals. Edit `momentum/verification-harness.json` directly, then:
JSON must parse without error (validate with `jq` or equivalent — not visual inspection);
every `defaults.execution_surfaces` key must exist in §1's surface enum; document what changed
in the Dev Agent Record.

**DoD additions:**
- [ ] `momentum/verification-harness.json` parses without error
- [ ] Every `execution_surfaces` key matches §1's surface enum exactly

#### Universal DoD

- [ ] The capability is reachable from the application's entry point by a user who has read
      no code. *(This is the item this story adds — apply it to this story too: the re-keyed
      routing must be reachable by a developer running `momentum:create-story` or
      `momentum:sprint-planning` normally, not only by reading the rule file.)*

#### Frozen Verification Contract

A frozen verification contract exists for this sprint at
`.momentum/sprints/{sprint-slug}/specs/verification-routing-re-key-to-assembled-surface-dod.{ext}`.
Read the **Part-A header** (`how_dev_self_checks`, `verification_method`, `harness_profile`) as
a self-check before signaling done. Do **not** read the verifier body (Part B: scenarios,
assertion scripts, Gherkin) beyond sections `how_dev_self_checks` explicitly names.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
