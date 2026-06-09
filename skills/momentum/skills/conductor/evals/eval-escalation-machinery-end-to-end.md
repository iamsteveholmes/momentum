# Eval: Escalation machinery end-to-end — mid-flight, end-gate-expanded, BLOCKED, escalated

**Surface under test:** Step 2.S3 (stage-3 fix loop) + step 2.F (mid-flight escalation
consumption hook). This eval drives real stakes-class findings through the escalation
machinery and observes the four concrete outcomes that the conduct-core sprint never
exercised: mid-flight pause, end-gate-expanded routing, BLOCKED disposition, and escalated
disposition.

**Motivation (retro finding):** Of 105 findings in conduct-core, 104 were routine and 1 was
`high-blast-radius-architecture` with `timing_tier=end-gate-expanded`. The per-story
mid-flight branch (step 2.F), the BLOCKED disposition (retry-bound-3 exhausted), and the
`escalated` disposition on the mid-flight path each fired zero times during a real build.
This eval closes that gap with live runs against fixture findings.

**References:**
- `references/escalation.md` — canonical mid-flight escalation engine contract
- `references/finding-schema.md` — finding shape, stakes classes, timing tiers, dispositions
- `conductor/workflow.md` step 2.S3 (fix loop) and step 2.F (mid-flight hook)

---

## Fixture Definitions

These four fixture findings are used by the scenarios below. Each is a minimal valid finding
in canonical schema format (`finding-schema.md`) that seeds the specific outcome under test.

### Fixture A — mid-flight bar-clearing finding

```yaml
finding_id: fix-A-mid-flight
story_slug: fixture-story-alpha
source: qa-reviewer
verdict: FAIL
severity: critical
stakes_class: irreversible-destructive
type: bug
location: scripts/deploy.sh:42
summary: "Production deploy runs without a dry-run gate — execution is irreversible and imminent."
detail: |
  The deploy script calls `aws s3 sync --delete` without a `--dryrun` flag and no confirmation
  step. Running this story's deploy target would permanently delete production objects. The
  action is irreversible (no rollback on S3 delete) and imminent (the deploy step fires on
  stage-4 merge). This meets both mid-flight criteria: irreversible AND imminent.
evidence: "scripts/deploy.sh line 42: aws s3 sync --delete s3://prod-bucket ."
ac_id: null
legitimate: true
suggested_fix: "Add --dryrun flag or a human confirmation gate before the s3 sync --delete step."
# Fixer sets these:
disposition: escalated
timing_tier: mid-flight
```

**Why this is bar-clearing:** `stakes_class=irreversible-destructive` (non-routine) AND
`timing_tier=mid-flight` (the fixer marks it imminent because the destructive action
executes on the current build step, not a future one). The escalation engine
(`references/escalation.md`) MUST return `pause-branch` for this finding.

### Fixture B — end-gate-expanded stakes finding (does NOT clear mid-flight bar)

```yaml
finding_id: fix-B-end-gate
story_slug: fixture-story-alpha
source: bmad-code-review
verdict: FAIL
severity: major
stakes_class: high-blast-radius-architecture
type: integration
location: skills/momentum/skills/conductor/workflow.md:line-600
summary: "Step 2.S3 dispatches {{mid_flight_escalations}} before all findings are routed — a finding added after dispatch is silently lost."
detail: |
  The mid-flight dispatch fires mid-iteration rather than after the full finding routing
  loop. A stakes-class finding added to {{mid_flight_escalations}} late in the loop could
  miss the single dispatch. This is an architectural concern with wide downstream effect
  (all stories pass through 2.S3). However, it does not describe an irreversible action
  about to execute right now — the build would not compound irreversible state by continuing.
  It therefore belongs at the end-gate-expanded tier, not mid-flight.
evidence: "conductor/workflow.md step 2.S3: dispatch fires before all finding branches are evaluated"
ac_id: null
legitimate: true
suggested_fix: "Move the {{mid_flight_escalations}} dispatch to after the full findings routing loop completes."
# Fixer sets these:
disposition: escalated
timing_tier: end-gate-expanded
```

**Why this does NOT clear the mid-flight bar:** `stakes_class=high-blast-radius-architecture`
(non-routine) BUT `timing_tier=end-gate-expanded` (the finding describes a structural risk, not
an irreversible-and-imminent or build-invalidating action about to execute). The escalation
engine MUST return `continue` for this finding (no mid-flight pause); the Conductor routes it
to `{{end_gate_escalations}}`.

### Fixture C — bound-exhausted finding (for BLOCKED scenario)

```yaml
finding_id: fix-C-blocked
story_slug: fixture-story-beta
source: qa-reviewer
verdict: FAIL
severity: major
stakes_class: routine
type: spec-compliance
location: skills/momentum/skills/conductor/workflow.md:step-2-S3
summary: "Fix loop does not increment {{fix_attempts}} counter — retry bound is never enforced."
detail: |
  The per-finding retry counter {{fix_attempts}}[F.id] must be incremented on each loop
  iteration. If the increment is absent, the loop runs indefinitely. The QA reviewer flags
  this each iteration; the fixer cannot address it because the correct fix is outside the
  current story's writable_files scope (it lives in a shared utility). Three fix attempts
  are made; none converge. Retry bound exhausted.
evidence: "qa-reviewer re-flags fix-C-blocked on iterations 1, 2, and 3 — fix never lands"
ac_id: null
legitimate: true
suggested_fix: "Increment {{fix_attempts}}[F.id] inside the Phase B→D loop body."
# Fixer returns "fixed" three times but QA re-check re-flags each time — convergence never reached.
# After attempt 3, the Conductor marks this finding BLOCKED.
disposition: blocked   # Conductor-internal; maps to escalated for schema consumers
```

**Why this produces BLOCKED:** The finding is `routine` (the fixer can attempt it) but the fix
never converges within 3 iterations. After exhausting `retry-bound-3`, step 2.S3 records
`disposition: blocked` for this finding (Conductor-internal value), does NOT merge story
`fixture-story-beta`, and spins a triage stub via `momentum:triage`.

### Fixture D — escalated disposition (confirming escalated records in build_log)

Fixture A produces an `escalated` disposition via the mid-flight path. This fixture confirms
a second path: an end-gate-expanded escalation visible in `{{build_log}}`.

Fixture B already produces `disposition: escalated` with `timing_tier: end-gate-expanded`.
The `{{build_log}}` entry for Fixture B must read:

```json
{
  "slug": "fixture-story-alpha",
  "event": "stage3-escalation",
  "disposition": "escalated",
  "timing_tier": "end-gate-expanded",
  "finding_summary": "Step 2.S3 dispatches {{mid_flight_escalations}} before all findings are routed — a finding added after dispatch is silently lost."
}
```

---

## Scenario 1 — Mid-flight path fires on a per-story finding

**Given:** A build in progress. Story `fixture-story-alpha` is in phase B (stage-3 fix loop,
step 2.S3). The stage-2 findings for this story include **Fixture A** (`irreversible-destructive`,
`timing_tier=mid-flight`).

**When:**
1. Step 2.S3 receives Fixture A from the directed fixer with `disposition: escalated` and
   `timing_tier: mid-flight`.
2. The Conductor appends Fixture A to `{{mid_flight_escalations}}` and dispatches to step 2.F.
3. The escalation engine (`references/escalation.md`) evaluates the bar:
   - `stakes_class=irreversible-destructive` ✓ (non-routine)
   - `timing_tier=mid-flight` ✓ (irreversible-and-imminent)
   - Bar is met → engine returns `{ outcome: "pause-branch", finding: FixtureA, ... }`.
4. Step 2.F surfaces the pause-ask to the developer (template from `references/escalation.md`).
5. Developer responds **Proceed**.
6. Step 2.F spawns a fix subagent, commits the fix, records resolution `fix-applied`.

**Then:**

1. **The build pauses mid-flight** — a `## Mid-flight Escalation — Branch Paused` surface is
   presented to the developer while `fixture-story-alpha` is still in progress (not after all
   stories complete).
2. **The `{{build_log}}` records a mid-flight event** for `fixture-story-alpha`:
   ```json
   { "slug": "fixture-story-alpha", "event": "stage3-mid-flight-escalation",
     "disposition": "escalated", "timing_tier": "mid-flight",
     "finding_count": 1 }
   ```
3. **`{{escalations}}` contains a mid-flight record** for this finding (workflow.md line 612
   writes exactly these four fields — no `resolution` key is written to the accumulator;
   resolution is observable via the answered pause-ask and the committed fix):
   ```json
   { "slug": "fixture-story-alpha", "stakes_class": "irreversible-destructive",
     "timing_tier": "mid-flight", "disposition": "escalated" }
   ```
4. **The timing recorded is `mid-flight`** — not `end-gate-expanded`. The mid-flight branch
   fired on a per-story in-progress finding, not on a post-merge AVFL result.

**Pass criteria:**
- A `## Mid-flight Escalation — Branch Paused` surface is produced during the build for
  `fixture-story-alpha`, before the story is merged or the build phase completes.
- `{{build_log}}` contains an entry with `event: stage3-mid-flight-escalation` and
  `timing_tier: mid-flight` for this story and this finding.
- `{{escalations}}` contains a record with `timing_tier: mid-flight` and
  `disposition: escalated` for `fixture-story-alpha`.
- The pause-ask surface includes all three self-sufficiency fields (What / Why / Evidence)
  and the three resolution options (Proceed / Change / Abort-that-branch).

**Fail criteria:**
- Fixture A is routed to `{{end_gate_escalations}}` instead of triggering a mid-flight pause.
- No pause-ask surface appears during the build.
- The `{{build_log}}` entry records `timing_tier: end-gate-expanded` for Fixture A.
- The `{{escalations}}` accumulator contains no `mid-flight` records after the run.

---

## Scenario 2 — Non-qualifying stakes-class finding held for end-gate-expanded

**Given:** Same build, same story `fixture-story-alpha`. The stage-2 findings include
**Fixture B** (`high-blast-radius-architecture`, `timing_tier=end-gate-expanded`).

**When:**
1. Step 2.S3 receives Fixture B from the directed fixer with `disposition: escalated` and
   `timing_tier: end-gate-expanded`.
2. The Conductor routes Fixture B to `{{end_gate_escalations}}` (does NOT append to
   `{{mid_flight_escalations}}`).
3. No dispatch to step 2.F is triggered for Fixture B.
4. The fix loop continues for any remaining routine findings in `fixture-story-alpha`.
5. At build-phase completion, `{{end_gate_escalations}}` contains Fixture B and it is
   carried to the Phase 5 end-gate decision cards.

**Then:**

1. **No mid-flight pause fires for Fixture B** — the build does NOT pause when Fixture B is
   processed; `fixture-story-alpha` continues to stage-4 (merge) after routine findings are
   resolved.
2. **`{{build_log}}` records an end-gate-expanded event** for Fixture B:
   ```json
   { "slug": "fixture-story-alpha", "event": "stage3-escalation",
     "disposition": "escalated", "timing_tier": "end-gate-expanded",
     "finding_summary": "Step 2.S3 dispatches {{mid_flight_escalations}} before all findings are routed..." }
   ```
3. **`{{end_gate_escalations}}` contains Fixture B** with `timing_tier: end-gate-expanded`.
   This entry is forwarded to Phase 5 for the decision-card gate.
4. **`{{mid_flight_escalations}}` does NOT contain Fixture B**.

**Pass criteria:**
- No pause-ask surface appears for Fixture B during the build phase.
- `{{build_log}}` records `event: stage3-escalation` with `timing_tier: end-gate-expanded`
  for Fixture B.
- `{{end_gate_escalations}}` contains an entry for `fix-B-end-gate` with
  `timing_tier: end-gate-expanded`.
- `{{mid_flight_escalations}}` does not contain `fix-B-end-gate`.
- Fixture B's finding appears as a decision card at the Phase 5 end-gate (not silently dropped).

**Fail criteria:**
- A mid-flight pause fires for Fixture B (the non-qualifying finding triggers a pause that
  violates the anti-firehose bar).
- Fixture B records `timing_tier: mid-flight` anywhere in `{{build_log}}` or `{{escalations}}`.
- Fixture B is silently dropped (no entry in `{{end_gate_escalations}}` and no decision card
  at Phase 5).

---

## Scenario 3 — Bound-exhausted finding ends BLOCKED; story left unmerged; triage stub spun

**Given:** A separate story `fixture-story-beta` is in phase B (stage-3 fix loop). Its
stage-2 findings include **Fixture C** (`routine`, `spec-compliance`). Fixture C cannot be
fixed within scope: the QA re-check re-flags it on each of 3 fix attempts. By design,
convergence is never reached within the retry bound of 3.

**When:**
1. Iteration 1: directed fixer returns `disposition: fixed` for Fixture C. QA re-check:
   FAIL — re-flags Fixture C. `{{fix_attempts}}["fix-C-blocked"] = 1`.
2. Iteration 2: directed fixer returns `disposition: fixed` again. QA re-check: FAIL.
   `{{fix_attempts}}["fix-C-blocked"] = 2`.
3. Iteration 3: directed fixer returns `disposition: fixed` again. QA re-check: FAIL.
   `{{fix_attempts}}["fix-C-blocked"] = 3`. Retry bound exhausted.
4. Step 2.S3 marks Fixture C `disposition: blocked` in `{{finding_dispositions}}` and
   records it in `{{build_log}}`.
5. The Conductor does NOT invoke stage-4 (merge) for `fixture-story-beta`.
6. The Conductor invokes `momentum:triage` with Fixture C's descriptive fields to spin a
   backlog stub.

**Then:**

1. **Fixture C's disposition is BLOCKED** — `{{finding_dispositions}}` records:
   ```json
   { "finding_id": "fix-C-blocked", "disposition": "blocked",
     "summary": "Fix loop does not increment {{fix_attempts}} counter...",
     "attempts": 3 }
   ```
2. **`{{build_log}}` records the BLOCKED outcome** for `fixture-story-beta` via two entries
   (per workflow.md step 2.S3 — one per-finding entry and one per-story entry):
   ```json
   { "slug": "fixture-story-beta", "event": "stage3-finding-blocked",
     "finding_id": "fix-C-blocked",
     "finding_summary": "Fix loop does not increment {{fix_attempts}} counter...",
     "attempts": 3 }
   ```
   ```json
   { "slug": "fixture-story-beta", "event": "stage3-story-blocked",
     "leftover_count": 1, "stranded": true,
     "note": "story left unmerged per spec §3; terminal status transition deferred to Phase 5 approve" }
   ```
3. **Story `fixture-story-beta` is NOT merged** — it is removed from `{{running}}` and
   never transitions to stage-4.
4. **A triage stub exists** in the backlog for Fixture C after the build completes — the
   finding is not silently dropped.
5. **The rest of the build continues** — `fixture-story-alpha` and any other stories are
   unaffected by `fixture-story-beta` being blocked.

**Pass criteria:**
- `{{finding_dispositions}}` records `disposition: blocked` with `attempts: 3` for
  `fix-C-blocked`.
- `fixture-story-beta` is absent from `{{merged}}` at build-phase completion — it was
  never stage-4 merged.
- A backlog stub linked to `fix-C-blocked` exists after the run (from the
  `momentum:triage` invocation in step 2.S3).
- `fixture-story-alpha` (the other story) is unaffected and proceeds normally.

**Fail criteria:**
- Fixture C records `disposition: fixed` after 3 failed re-checks (convergence falsely
  declared).
- `fixture-story-beta` is merged despite having an unresolved BLOCKED finding.
- No backlog stub is created for Fixture C after the build.
- The BLOCKED finding causes the entire build to halt (whole-build halt is a violation —
  only the single story is held back).

---

## Scenario 4 — Escalated disposition recorded and observable in the build report

**Given:** Scenarios 1 and 2 above run to completion. Both Fixture A and Fixture B have been
processed through their respective escalation paths.

**When:** The build completes (or the Phase 5 end-gate runs) and the `{{build_log}}` is
inspected for escalated disposition records.

**Then:**

1. **Fixture A (mid-flight):** `{{escalations}}` contains at least one record with
   `disposition: escalated` and `timing_tier: mid-flight` for `fixture-story-alpha`
   (workflow.md line 612 writes these four fields: `slug`, `stakes_class`, `timing_tier`,
   `disposition` — no `resolution` field is written to the accumulator; the Proceed resolution
   is observable via the developer's answered pause-ask and the committed fix). This record is
   visible in the Phase 5 end-gate report's "Mid-flight Escalations During Build" section.
2. **Fixture B (end-gate-expanded):** `{{end_gate_escalations}}` contains an entry for
   `fix-B-end-gate` with `disposition: escalated`, `timing_tier: end-gate-expanded`. This
   entry surfaces as a decision card at Phase 5.
3. **At least one `escalated` disposition is observable** — the build report surfaces it to
   the developer without requiring the developer to open a log file or recall prior context.

**Pass criteria:**
- `{{escalations}}` contains a record with `disposition: escalated` and
  `timing_tier: mid-flight` — the mid-flight escalated disposition is present and readable.
- `{{end_gate_escalations}}` contains a record with `disposition: escalated` and
  `timing_tier: end-gate-expanded` — the end-gate escalated disposition is present and
  readable.
- The Phase 5 end-gate report includes a "Mid-flight Escalations During Build" section (or
  equivalent) showing the Fixture A record.
- The Phase 5 end-gate report includes a decision card for Fixture B.

**Fail criteria:**
- No finding ever records `disposition: escalated` in `{{escalations}}` or
  `{{end_gate_escalations}}`.
- The end-gate report omits mid-flight escalation records.
- An escalated finding is dropped (absent from both `{{escalations}}` and
  `{{end_gate_escalations}}`).

---

## Verification Method

**Live execution against the fixture findings above.** This eval is NOT verified by inspection
alone. Each scenario requires driving the real step 2.S3 / step 2.F loop with the fixture
findings and observing the resulting state in `{{build_log}}`, `{{escalations}}`,
`{{end_gate_escalations}}`, and `{{finding_dispositions}}`.

### Step-by-step verification sequence

1. **Seed Fixture A and Fixture B** into the stage-2 findings list for a test story
   `fixture-story-alpha`. Both fixtures carry the full canonical schema shape defined above.

2. **Run step 2.S3** (stage-3 fix loop) for `fixture-story-alpha` with the seeded findings.
   The directed fixer subagent is given the findings and instructed to return the dispositions
   as declared (Fixture A: `escalated/mid-flight`; Fixture B: `escalated/end-gate-expanded`).

3. **Observe step 2.F** fire for Fixture A:
   - Confirm `## Mid-flight Escalation — Branch Paused` appears in the output.
   - Confirm the pause-ask carries What / Why / Evidence / Options inline (self-sufficiency
     floor from `references/escalation.md`).
   - Respond **Proceed**. Confirm `{{escalations}}` contains a record with
     `disposition: escalated` and `timing_tier: mid-flight` for `fixture-story-alpha`
     (the accumulator does not carry a `resolution` field — Proceed resolution is evidenced
     by the developer's response to the pause-ask and the subsequent committed fix).

4. **Observe Fixture B** routed without a pause:
   - Confirm no second pause-ask surfaces for Fixture B.
   - Confirm `{{end_gate_escalations}}` now contains Fixture B with `timing_tier: end-gate-expanded`.
   - Confirm `{{build_log}}` records `event: stage3-escalation` and `timing_tier: end-gate-expanded`.

5. **Seed Fixture C** into the stage-2 findings for a separate test story
   `fixture-story-beta`. Configure the verification harness so the directed fixer returns
   `disposition: fixed` for `fix-C-blocked` on each of 3 iterations, and the QA re-check
   agent returns FAIL each time (convergence never reached).

6. **Run step 2.S3** for `fixture-story-beta` until the retry bound is exhausted.
   - Confirm `{{fix_attempts}}["fix-C-blocked"]` reaches 3.
   - Confirm step 2.S3 records `disposition: blocked` for `fix-C-blocked`.
   - Confirm `fixture-story-beta` is removed from `{{running}}` and NOT sent to stage-4.
   - Confirm `momentum:triage` is invoked and a backlog stub slug is recorded.

7. **Inspect the end-gate report** (Phase 5) or `{{build_log}}`:
   - Confirm `{{escalations}}` contains the mid-flight record for Fixture A.
   - Confirm the Phase 5 "Mid-flight Escalations During Build" section is present and lists
     Fixture A's resolution.
   - Confirm the Phase 5 decision cards section lists Fixture B.

### Inspection-vs-execution note

Scenarios 1–4 cannot be fully verified by workflow inspection alone because:
- The mid-flight bar evaluation (`references/escalation.md`) depends on runtime input — the
  engine result (`pause-branch` vs `continue`) is conditional on `timing_tier` values that
  only appear when the fixer processes real findings.
- The BLOCKED disposition requires the retry-bound-3 loop to run and exhaust — no static
  reading of the workflow can prove this fires correctly without executing it.
- The `{{build_log}}`, `{{escalations}}`, and `{{end_gate_escalations}}` accumulators exist
  only at runtime; their contents cannot be inspected from the workflow text.

**Inspection alone** covers: verifying that step 2.F exists, that the pause-ask template
matches `references/escalation.md`, and that step 2.S3 contains the correct routing branches.
**Live execution** is required to confirm the branches fire in the right order with real
findings, that `{{mid_flight_escalations}}` is populated before step 2.F is invoked, and that
the retry-bound-3 counter is incremented correctly.

This eval is therefore classified as **execution-primary** with an inspection supplement:
inspection verifies the wiring; execution verifies the outcomes.
