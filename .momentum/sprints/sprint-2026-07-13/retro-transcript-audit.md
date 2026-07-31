# Sprint Transcript Audit — sprint-2026-07-13

## Executive Summary

The sprint shipped 15/15 stories merged with a fundamentally sound control loop: 13 of 15 stories converged in a single dev → dual-review → fix → simplify cycle with zero thrash, the escalation/deferral machinery refused to rubber-stamp anywhere it was tested, and the interrupt/resume hardening built *in this sprint* proved itself live across a 13.5-hour session break, two API-error retries, and a forced fresh-session handoff. The layered gates are demonstrably complementary — executed QA, adversarial code review, simplify, AVFL-on-merge, and E2E each caught at least one real defect the other layers missed.

The struggles cluster into five systemic seams, not story-quality problems: (1) a **worktree sandbox escape** let a diagnostic probe write a phantom entry into the live stories index — the exact defect class the sprint existed to eliminate; (2) the coherence gate merged with its **headline developer-override path non-functional** (renderer emits no fork ids to match against); (3) the Conductor has **no stall watchdog** — a wedged dev burned ~3 hours until the developer noticed; (4) the **subagent completion-signal seam** (SendMessage schema friction, no delivery acks, idle-without-delivery, reply-address ambiguity) taxed nearly every agent in the cohort; and (5) the **retro's own extraction pipeline is 74% blind** — 121 of 163 agent summaries lost to a one-expression parser defect.

111 adversarially-verified findings synthesized: **46 successes (keep), 41 fixes, 24 investigations**; severity split 7 high / 37 medium / 67 low. Zero substantive human interventions on story content during the build — every human touch was environmental (CLI/UI failures, hook misfires, a stall the machine should have caught).

---

## What Worked Well

Each entry: **what happened → evidence → root cause (the design element responsible) → recommendation**.

### 1. Single-cycle convergence was the norm, not the exception
- **What happened:** 13 of 15 stories needed exactly one dev pass, one parallel QA+code-review round, at most one fix pass, and one simplify pass — no re-review loops, no re-dev dispatches.
- **Evidence:** build-ledger.jsonl: 15/15 story-terminal events `outcome: merged`; per-story disposition counts equal finding counts exactly (coherence-gate 6/6, kb-buildout 6/6, staging-ledger 4/4, manifesto-builder 4/4); rename-base-body ran launch-to-merge in ~13.5 min, continuous-cli in 21 min with the fix loop legitimately skipped ("stage-2 findings empty — straight to merge").
- **Root cause:** Frozen eval contracts + planning-time AVFL produced specs precise enough that dev/QA/CR converge on one interpretation; the skip-fix-loop-when-clean policy avoids busywork.
- **Recommendation:** Keep. This is the baseline to protect when tuning any pipeline stage.

### 2. The layered gates are complementary — each caught something the others missed
- **What happened:** Executed QA caught a behavioral defect static review passed; code review caught a story reintroducing its own target hazard (twice); simplify caught fix-pass drift; AVFL-on-merge caught doc/code coherence misses; E2E caught a cross-story regression per-story gates passed.
- **Evidence:** manifesto-builder: live QA run found task-shaped symptom phrasings after code review passed "clean on all 8 ACs"; staging-ledger: CR flagged the silently-dropped-untracked-file hazard (stakes irreversible-destructive) in the very story built to eliminate it, resolved at end-gate card D1 commit 4964ff7; resume-hardening: CR caught the fallback missing the `verify` state — "the exact erroring resume the story exists to prevent"; coherence-gate: simplify caught reason-token drift *introduced by the fix pass*; continuous-cli: AVFL caught the help-text/behavior mismatch both review legs missed; E2E STRU_E-001 caught the debugprobe1 phantom that dev, QA, and CR all passed.
- **Root cause:** Each layer runs a genuinely different method (live execution vs. static adversarial read vs. corpus coherence vs. seam probing), so their miss classes don't overlap.
- **Recommendation:** Keep all layers; resist collapsing them for cost reasons — the cost findings below target *friction*, not the layer structure.

### 3. Escalation, stakes routing, and deferral discharge were honest end-to-end
- **What happened:** Fixers escalated rather than silently fixing out-of-scope or irreversible findings; coverage deferrals were held open until real observation, one for ~9 days.
- **Evidence:** 8 stage3-escalations, all `end-gate-expanded`, none paused the build; fix-staging-ledger escalated its irreversible-destructive finding per directive; endgate-viewer deferral recorded `coverage-deferral-undischarged` ("merged code is precondition, not observation") and discharged 2026-07-31 only on live end-gate behavior; conduct-adoption's discharge waited for `momentum-tools sprint complete` to actually run at this build's own gate; resume-hardening discharged via ledger forensics across the real 13.5h interrupt (15/15 launches, 15/15 terminals, 35 unique dispositions, zero duplicates).
- **Root cause:** The stakes_class routing contract plus the two-step deferral lifecycle (record undischarged → discharge only on observed behavior) structurally forbids rubber-stamping.
- **Recommendation:** Keep. The verified-by-composition pattern (discharging infra-story coverage against the sprint's own real events) is worth institutionalizing.

### 4. Interrupt/resume machinery survived every real disruption
- **What happened:** Two API connection errors resumed in place with no duplicated work; a 13.5-hour session break mid-stage-3 resumed to clean merges for 6 stories; an uncommitted fix survived ~13 hours in a worktree and merged cleanly.
- **Evidence:** conduct-adoption dev retry: "Task 1 done, Task 2 not yet applied" — applied only the missing edit; qa-execute retry resumed with no rework; story-terminal notes "resumed session — merged per handoff order #1..#6", all clean rebases; base-body fix applied 01:43, ledgered and merged 14:49–15:36 next session.
- **Root cause:** The resume-idempotency hardening (built this sprint) + check-worktree-state-before-continuing protocol + the handoff bridge document.
- **Recommendation:** Keep — and note the recursion: the sprint's own deliverable absorbed the sprint's own disruptions.

### 5. The visual plan gate with anti-rubber-stamp verdicts changed developer behavior
- **What happened:** The developer engaged all 7 forks individually with written verdicts instead of blanket-approving; one fork ruling ("Confirm Option A") collapsed an entire rename story to zero renames + verification before any build cost was paid.
- **Evidence:** Sign-off 2026-07-21 21:08 with seven distinct verdicts; gate held across a 2.6-day pause and re-oriented on a single "So where are we now?"; ct-rename was authored to the ruled option — no build-time churn followed.
- **Root cause:** Per-fork written-verdict requirement + exec-summary-first re-orientation.
- **Recommendation:** Keep.

### 6. Verification honesty held under nudge pressure
- **What happened:** Agents nudged mid-verification refused to fabricate completion; contract and dev agents disclosed their own compliance breaches unprompted.
- **Evidence:** dev-coherence-gate: "I don't want to send a completion signal with fabricated or assumed verification results"; qa-manifesto-builder: "Not done yet — still verifying"; ct-continuous self-reported its read-isolation breach and offered a clean re-author; handoff-artifact dev disclosed "no EDD cycle run, no live sprint activate", which E2E then correctly carried as never-fired-live.
- **Root cause:** The executed-QA/EDD discipline and honest-SKIP conventions make truthful status the path of least resistance.
- **Recommendation:** Keep. (The un-dispositioned breach flag is a separate struggle, below.)

### 7. Scope-boundary discipline by fixers
- **What happened:** Fixers respected writable_files, triaging out or escalating cross-story fixes with checkable rationale instead of making out-of-scope edits.
- **Evidence:** fix-repair-phantom: "No in-scope file can carry this fix" (triaged-out with target file named); fix-kb-buildout escalated the constitution-builder change; write-scope exceptions were ledgered inline with rationale (kb-buildout wiki-query ratification).
- **Root cause:** Explicit writable_files declarations + the escalate-don't-silently-fix contract.
- **Recommendation:** Keep the discipline; fix the *scoping model* that forced the workarounds (see Struggles §5).

### 8. Planning-time AVFL and grep-gate ACs paid for themselves
- **What happened:** Story-spec validation caught fabricated constraints and scope mismatches before they could distort dev/QA; mechanically-checkable sweep ACs caught edit sites the spec author missed.
- **Evidence:** manifesto-builder spec: invented 15–40 entry-count gate and stale epic framing removed pre-freeze (7 findings, single round, no residual); base-body-trio: major machine-scope/AC6 mismatch fixed pre-freeze → zero build-time scope escalations; arch-decision-26: AC5 grep sweep caught a third stale `specialist-classify` mention not enumerated in the spec.
- **Root cause:** Adversarial validation at authoring time + ACs written as executable checks rather than prose.
- **Recommendation:** Keep; standardize grep-gate ACs for consistency-sweep stories.

### 9. Pure-reasoning simulation agents are the best cost-to-yield pattern in the sprint
- **What happened:** Five EDD/QA step-simulation agents verified workflow-instruction changes in ≤7 turns with ≤2 tool calls each.
- **Evidence:** Four agents at exactly turns=2, tools=0, 74–122 KB prompt-only transcripts, each returning a complete step-trace verdict — versus 100+ turn averages elsewhere.
- **Root cause:** Fixture inlined in the prompt, zero tool churn, single-shot instruction trace.
- **Recommendation:** Keep; institutionalize for workflow.md edits.

### 10. The finding pipeline's noise filters worked
- **What happened:** Zero review findings overturned as factually wrong; a fabricated-quote AVFL false positive and a fixture-blind E2E false positive were both dismissed with rationale rather than driving false fixes; duplicate QA reports were deduped by finding-id.
- **Evidence:** Disposition tally 27 fixed / 4 triaged-out / 2 dismissed / 2 escalated, all non-fixed with verified rationale; i1-ACCU_A-002-safe-word dismissed ("the word 'safe' appears nowhere"); e2e-resolve-dev-fallback-0 dismissed against the story's own AC1-mandated fixture state; kb-buildout's twice-delivered QA report recorded exactly once.
- **Root cause:** bmad-dismiss pre-filter + verify-before-fix discipline + finding-id dedup at the conductor.
- **Recommendation:** Keep. The known confident-false-positive pattern in audit agents persists but is contained.

---

## What Struggled

Each entry: **what happened → evidence → root cause → recommendation**. Consolidated across lenses; per-story detail in the story rollup.

### 1. Worktree sandbox escape wrote phantom state into the live project index (HIGH)
- **What happened:** A dev agent's diagnostic probe against the installed momentum-tools shim mutated the live `.momentum/stories/index.json` — creating a `debugprobe1` phantom entry, the exact defect class the repair-phantom story existed to eliminate — and a wholesale checkpoint commit laundered the debris into git. Cleanup then required a hand-edit because no removal CLI exists.
- **Evidence:** agent-adev-repair-phantom transcript entry 133 (probe) and 136 (agent's own diagnosis: "the installed shim is a symlink into the main repo, and its sibling-directory lookup always wins over MOMENTUM_HOME"); E2E STRU_E-001: smoke.sh "PHANTOM: debugprobe1 / PHANTOMS: 1"; checkpoint 9afd2d1 (582-line index sweep); conductor-warning 2026-07-24: "no momentum-tools removal command exists (story-add only), so the Conductor removed it surgically" — a sanctioned violation of the sole-writer invariant.
- **Root cause:** Worktree isolation is not enforced for momentum-tools shared-state writes (shim resolution ignores MOMENTUM_HOME), and the sole-writer CLI has an add path but no remove path.
- **Recommendation:** Fix (critical). Make the shim honor MOMENTUM_HOME / fail loudly outside the main repo; add `momentum-tools sprint story-remove`; land the queued create-story write-path follow-up (endgate-fix-6).

### 2. Coherence gate merged with its headline HITL path non-functional (HIGH)
- **What happened:** The sprint's flagship planning feature — developer override of a seam failure at the plan gate — cannot work as shipped: the gate mandates id-based matching of override verdicts, but the renderer's ForkItem shape has no id field, so every override would be classified "NOT an override" and hold the sprint against the developer's decision.
- **Evidence:** stage3-escalation STRU_A-002 (high-blast-radius-architecture), citing plan-gate-renderer.md:208-217/:401-402 vs coherence-gate.md:181-186; self-identified at build as cross-artifact note #10, re-confirmed by AVFL iteration 2; ledger 2026-07-31 major-residual-stub-created with developer verdict "acknowledge + queued … to land before the coherence gate first live firing".
- **Root cause:** The story's spec depended on plan-gate-renderer.md, which was excluded from its writable_files — the fixer structurally could not complete the fix (fix-coherence-gate: "fixed as far as possible within scope"). An ironic instance of the producer/consumer mismatch the gate itself is designed to catch.
- **Recommendation:** Fix (critical). The renderer-id follow-up must land before the next sprint-planning run, which is the gate's first live firing.

### 3. No stall watchdog — humans were the Conductor's only heartbeat (HIGH)
- **What happened:** A dev agent whose tool calls hung (writes to the out-of-repo nornspun fixture) silently stalled the proof story for ~3 hours until the developer typed "3h seems way too long. What's up?" A second ~2h wedge (contradictory spawn constraints) was likewise caught only by human-noticeable silence. The recovery then misdiagnosed the stall and raced the recovering agent.
- **Evidence:** dev-live-run transcript: Write issued 15:41:51Z → result 16:35:43Z (54 min); Bash 16:36:55Z → result 18:41:17Z (2h04m); story wall-clock 3h19 of which ~3h05 stall — 13x working time; ledger retry reason claims "wedged between run-the-real-pipeline … and the no-spawn constraint" but the transcript shows delayed tool results, and the agent's composed-file Write completed 33s before TaskStop; r2 dev found composition "already complete … contrary to the retry brief's premise".
- **Root cause:** No per-agent heartbeat/watchdog in conduct; no dispatch-time consistency check between story instructions and spawn constraints (the delegate-via-spawn vs. no-spawn contradiction); retry briefs are written from inference, not verified state.
- **Recommendation:** Fix (high). Add a tool-call-latency watchdog with probe-stop-redispatch protocol; verify agent state (TaskOutput + disk) before recording a retry diagnosis in the permanent ledger; lint dispatch prompts for constraint contradictions.

### 4. The subagent completion-signal seam taxed the entire cohort (the sprint's biggest recurring friction)
- **What happened:** Four independent failure modes on one seam: (a) agents finish work but idle without sending their required signal; (b) SendMessage's string-only message field rejects the JSON payloads the spawn prompts require, costing 2–3 retries per agent; (c) no delivery ack, so conductor nudges to agents whose reports are in transit trigger duplicate sends; (d) reply address (team-lead vs main) is unpinned, and every agent pays a ToolSearch schema-load round-trip before it can report.
- **Evidence:** (a) 4/4 resume-hardening agents nudged, one with 54 min of dead time while the session was active; 2/4 delivery-bearing agents on rename-base-body; both legs of conduct-adoption; "Six idle agents owe outputs — chasing all." (b) 7 failed sends across 3 of 5 rename-base-body agents; identical invalid_union errors across dev/fixer/simplify on arch-decision-26; r2 dev's "test plain text, not json" probe. (c) 6 duplicate/resend events in one session (8–36s gaps); kb-buildout QA report delivered twice after a ~53-min lag. (d) 84 of 217 team messages are ToolSearch loads of SendMessage; recipient split 71 team-lead / 35 main; one agent sent to both addresses 52s apart; 11 captured payloads double-fill two field conventions defensively.
- **Root cause:** Spawn prompts specify *that* a signal must be sent but not the exact call shape, reply address, or tool pre-grant; the protocol has no ack/idempotency; SendMessage is deferred rather than pre-granted.
- **Recommendation:** Fix (high). One protocol overhaul: pre-grant SendMessage in conduct subagent tool grants, embed a literal working call example (string message + summary) in every spawn prompt, pin the reply address, add an idempotency key + conductor ack, and make "send the signal" the final mandatory task in the prompt's task list.

### 5. writable_files cannot model the scopes stories actually need
- **What happened:** Four distinct scoping failures: out-of-repo surfaces mandated by ACs can't be declared (kb-buildout wiki-query — post-hoc ratification of a fully foreseeable edit); declared seam consumers sat outside the writable set, so a high-blast-radius producer/consumer drift waited ~2 days for end-gate repair (constitution-builder); a spec's contract-coupled renderer file was unwritable, shipping the inert override path (Struggles §2); and a producer story shipped with no consumer existing anywhere (handoff artifact — AVFL invented the consumer post-merge as a fix).
- **Evidence:** conductor-warning 22:49:50Z (wiki-query ratification); fix-kb-buildout escalation → fixed only at end-gate pass 2, commit 798a0c5, ~2 days after detection; the story's own eval.yaml declared "PRODUCER / CONSUMER SCOPE"; avfl i1-DOMA_E-001 (major): "Build-handoff artifact written by sprint-planning was never consumed".
- **Root cause:** Plan-time scoping treats writable_files as an in-repo file list, ignoring declared seams, out-of-repo surfaces, and consumer existence; the coherence gate checks depends_on edges but not producer-without-consumer.
- **Recommendation:** Fix (medium). Extend create-story/sprint-planning: pull declared seam consumers into the writable set or a paired depends_on story; support declared out-of-repo surfaces; add a producer-without-consumer check to the coherence gate.

### 6. AVFL-on-merge convergence scoring is structurally broken (HIGH)
- **What happened:** The post-merge loop reported NON_CONVERGENT to the results gate after burning 4 iterations and 3 fix commits on a corpus whose actual residual was 3 routine doc items — because the score re-counts findings the loop is forbidden to fix (end-gate-held stakes findings) every iteration. Scores were also unstable (dropped 51→46 after fixes were applied).
- **Evidence:** avfl-on-merge-complete: result_status NON_CONVERGENT, scores [51, 46, 77, 71], 11 fixes, 22 findings; the entry's own note: "Score floor is structural: 5 stakes-class findings deliberately held for the end-gate re-count each iteration".
- **Root cause:** The convergence denominator includes escalation-held findings; iteration scoring has no stability control.
- **Recommendation:** Fix (high). Exclude held-for-end-gate findings from the convergence score (report them as a separate escalation count); investigate the scoring noise.

### 7. The retro is largely blind to its own sprint (HIGH)
- **What happened:** Three compounding evidence failures: 121 of 163 agent summaries are parse errors (74% of agents, 60% of transcript bytes unmeasured, including every ct-* and simplify-* agent); the documented Phase-2 extract inputs (build-results.jsonl, finding-cards.json) don't match what conduct actually writes (build-ledger.jsonl); and mtime-keyed session discovery silently dropped the entire wave-2 build session because the retro itself touched the file after the --before window.
- **Evidence:** agent-summaries.jsonl parse_error rows ("Malformed JSON at byte 1 … {'type': NULL"); reproduced live: DuckDB infers toolUseResult as STRUCT and the VARCHAR cast at transcript-query.py:427 renders single-quoted non-JSON; audit-extracts/ lacks both documented conduct artifacts; the prescribed story-slug query returns 163 subagent files, none containing the conduct-live-run build pipeline (session f3aef997 mtime Jul 30, touched during the retro).
- **Root cause:** One-expression extractor defect (STRUCT→VARCHAR cast) + spec/artifact drift between retro preprocessing and conduct's layout + fragile mtime-based session discovery.
- **Recommendation:** Fix (high). Repair the cast (data is fully recoverable — transcripts intact); align the retro spec's inputs with build-ledger.jsonl; key session discovery on content timestamps, not file mtime.

### 8. Known gotchas are re-learned by every wave, and half the cohort is anonymous
- **What happened:** Parallel agents independently re-paid documented error taxes — 27 of 69 errors landed in the wave-1 launch hour (blocked sleep x5, SendMessage summary x3, malformed Read JSON x3, flat-roster spawn, hook denials x5); four cs-* agents ran the identical failing AVFL probe; five dev/qa agents each attempted the blocked sleep-poll. Meanwhile 71 of 163 agents (19.2 MB of transcript) were spawned under generic names ("general-purpose", "claude"), making their cost unattributable.
- **Evidence:** errors.jsonl wave-1 cluster; identical "Exit code 1 / === avfl SKILL.md ===" tool_result in 4 cs transcripts; naming split 92 role-named vs 71 generic.
- **Root cause:** The operational-gotchas knowledge (already in project memory) is not injected into spawn prompts or base bodies; no spawn-time naming convention enforcement.
- **Recommendation:** Fix (medium). Add a standard "environment facts" block (Monitor-not-sleep, flat roster, SendMessage shape, AVFL invocation path, hook-denial patterns) to conduct spawn prompts/base bodies; enforce the role-slug naming convention at spawn.

### 9. Hot-file contention: six stories wrote one file, three wrote one block
- **What happened:** Six sprint stories edited conductor/workflow.md; three edited the same Phase-5 approve block, forcing semantic (not textual) rebase conflict resolution whose integrated control flow "exists in a shape neither parent story validated" — flagged build_invalidating and only positively validated when it executed at this build's own end-gate. Separately, a doctrine change (retiring the printf append mechanism) shipped without sweeping sibling evals, leaving a doctrine fork that survived five gates until AVFL iteration 2.
- **Evidence:** stage3-escalation merge-semantic-resolution-0; end-gate session line 1421 (6 stories touching workflow.md); COHE_A-001-iter2 (major, escalated, fixed at end-gate card D6 commit d0046be); resume-side skip-list omitting the sprint-complete call another story added to the same block.
- **Root cause:** Sprint planning packs same-file/same-block stories in parallel with no block-level coordination declaration; mechanism retirements have no mandatory grep-sweep for the retired construct.
- **Recommendation:** Investigate/fix (medium). Detect multi-story hot files at planning (declare coordination, serialize, or nominate an integration owner); require a retired-construct grep-sweep in the dev pass for doctrine changes.

### 10. Frozen contracts are frozen before they're ever executed
- **What happened:** The proof story's frozen smoke contract could never pass — a grep-anchoring bug false-FAILed it regardless of outcome — and the freeze policy forbade in-story repair, forcing verification back to the manual observation path the contract was meant to mechanize. Contract-author read-isolation is also convention-only: two authors disclosed that a default Read pulled the whole story file, and one self-reported breach received no recorded accept/re-author disposition.
- **Evidence:** qa-reviewer-1 (triaged-out): "smoke.sh:122 … grep -c '^PASS:' always counts 0 against the driver's indented PASS: lines"; ct-liverun: "bash -n syntax-checked, not executed"; ct-continuous disclosure vs. zero hits for "clean re-author" in the session; ct-handoff same disclosure pattern.
- **Root cause:** Freeze happens after a syntax check only; isolation relies on agent self-discipline because Read returns whole files by default; orchestrator has no required disposition step for self-reported compliance breaches.
- **Recommendation:** Fix (medium). Execute every contract against sample driver output before freeze; either mechanize read-scoping or formally accept disclosure-based isolation with a mandatory recorded disposition.

### 11. Orchestrator verification and bookkeeping have stale-state hazards
- **What happened:** The orchestrator challenged already-applied fixes based on stale grep views (tokens legitimately remaining post-rewording), forcing evidence-rebuttal round-trips; conduct bookkeeping used relative paths that wrote sprint-state JSON inside a story worktree, and the recovery command tripped the destructive-git hook.
- **Evidence:** cs-staging-ledger and cs-qa-execute both forced to re-prove applied work ("Your view looks stale … a grep on those tokens gives a false hit"); 15:55:32 cross-artifact note appended in the worktree, 15:58:50 `git checkout -- <file>` denied by hook, 3 extra calls to recover before merge.
- **Root cause:** Verification-by-token-grep is lossy for reworded content (assert absence of exact OLD strings instead); ledger/note appends don't pin absolute paths to the main checkout.
- **Recommendation:** Fix (medium). Standardize fix-verification on exact-old-string absence; make all conduct bookkeeping writes use absolute main-repo paths.

### 12. Cost concentration: story enrichment outweighs implementation; simplify is majority no-op
- **What happened:** The create-story cohort (ct stub + cs enrichment) is the sprint's most expensive role class — cs agents average 119 turns vs dev's 100, with the four heaviest agents all cs-*; the ~13-agent cohort totals ~12.1 MB plus 3.9 MB of ct stubs. Meanwhile the unconditional per-story simplify stage returned zero edits in at least 4 of 7 visible runs (2.5 MB of transcript).
- **Evidence:** Parsed role aggregates (cs n=11, 1,318 turns, 10,420 KB); simplify no-op reports ("no cleanup edits warranted", bare "[]") vs. positive yield on only coherence-gate (4 edits) and one single-edit run.
- **Root cause:** Enrichment likely re-reads shared corpus per story instead of a once-per-sprint pre-digest; simplify runs unconditionally regardless of diff size or finding count. (Caveat: simplify *did* catch two real correctness drifts — conditionality must not lose that.)
- **Recommendation:** Investigate (medium). Profile cs re-reads for a shared pre-digest; gate simplify on diff-size/finding thresholds while preserving its fix-pass-drift net.

---

## User Interventions

Seven human touchpoints, none of them substantive story-content interventions — every one was environmental, tooling, or watchdog work the machine should own.

1. **Plan-gate engagement (strength).** What: seven distinct written fork verdicts at sign-off; gate held over a 2.6-day pause. Evidence: 2026-07-21 21:08 sign-off; anti-rubber-stamp satisfied. Root cause: gate design worked. Recommendation: keep.
2. **Plugin-update over-application (correction).** What: developer questioned a reflexive pre-workflow marketplace update; agent conceded the habit only applies post-release. Evidence: 21:14 "why do we need to do a plugin update after sprint planning?"; update returned "already at 0.31.0". Root cause: memory note applied unconditionally. Recommendation: fix — conditionalize the note on a release having merged.
3. **Blind-Enter rejection pause.** What: a permission dialog failed to render, the developer's blind Enter registered as a tool rejection, and the Conductor correctly held everything (~54 min pause, no lost work). Evidence: 00:10 "Why are you holding? The CLI wasn't showing me the options I just hit enter." Root cause: CLI dialog rendering degrades in long multi-agent sessions. Recommendation: investigate — external (Claude Code CLI), but reduce exposure (below).
4. **UI collapse forcing a session handoff.** What: three interrupts in 4 seconds, then "the UI has gone completely wonky… give me a handoff and I'll start a new session" — second UI disruption of the same build day. Evidence: 15:05:38–42 interrupts; 54 pure idle_notifications flooding the main session (of 91 teammate messages in the user channel). Root cause: probable stressor is teammate idle-notification flood into the main conduct session. Recommendation: investigate — suppress/batch idle notifications; the handoff/resume path absorbed the failure cleanly.
5. **Hook misfire cross-session debug + "Did you fix it?".** What: the hookify block-destructive-git rule misfired on dot-prefixed file paths, escalating prompts mid-build; the agent fully diagnosed it, then idled for 18 minutes until the developer nudged "Did you fix it?". Evidence: 18:44 second-session diagnosis; two PreToolUse denials at 15:58 UTC; post-fix "all six test cases pass". Root cause: overbroad regex (intended for `git checkout -- .`) + diagnosis-only stop on a live blocker. Recommendation: fix — commit the corrected pattern with checked-in test cases; on live blockers, apply-or-explicitly-ask, never diagnose-and-idle.
6. **Model/effort preset interrupt.** What: the developer interrupted a just-started conduct invocation to set /model and /effort, then re-invoked. Evidence: 21:15:57 invoke → 21:16:05 interrupt → /model + /effort → 21:16:54 re-invoke. Root cause: fresh-session-before-conduct protocol has no config-preset step. Recommendation: fix — add a pre-conduct checklist line.
7. **Human as stall watchdog.** What: the developer, not the Conductor, detected the 3-hour stall ("3h seems way too long. What's up?"). Evidence: recovery began only after the 18:43:59Z message. Root cause: Struggles §3. Recommendation: fix via the watchdog.

---

## Story-by-Story Analysis

All 15 stories merged. Convergence shorthand: D=dev passes, R=review rounds, F=fix passes.

### 1. momentum-knowledge-base-buildout — merged, 1D/1R/1F
Clean single-cycle convergence with live QA execution of all four resolver paths. **Struggles:** write-scope gap — the dev's AC-mandated edit to the out-of-repo wiki-query SKILL.md required post-hoc ratification (root cause: writable_files can't model out-of-repo surfaces; fix at planning); seam-consumer gap — constitution-builder (the declared consumer) was outside the writable set, so the wrong-vault-fallback drift waited ~2 days for end-gate repair at commit 798a0c5 (fix: pull declared seam consumers into scope). **Notes:** AVFL fabricated-quote false positive dismissed correctly; nornspun-client's stale wiki-query copy triaged out — confirm it reaches triage (investigate); duplicate QA report absorbed by finding-id dedup.

### 2. manifesto-builder-skill-generate-then-curate — merged, 1D/1R/1F
Textbook convergence, zero human touches. **Strengths:** executed QA caught task-shaped symptom phrasings that static review passed clean on all 8 ACs — direct proof the live-execution QA model earns its cost; planning AVFL removed an invented numeric gate and stale epic framing pre-freeze. **Struggles:** the AC5 behavioral fix was closed on the fixer's self-report without re-running the harness that found it (investigate: re-verify executed-QA findings); the blank Dev Agent Record template burned a QA finding here and on kb-buildout (fix: strip the template or pre-brief QA).

### 3. base-body-collapse-rollback — merged, 1D/1R/1F
Clean 16-file, 4-change-type convergence; planning AVFL caught a major machine-scope/AC6 mismatch pre-freeze; the fix survived a ~13h session gap uncommitted and merged cleanly. **Struggle:** the story's only rework and a QA-vs-CR verdict split (VERIFIED-with-note vs FAIL) both traced to AC5 enumerating a file without stating its expected observable change (fix: per-file reconciliation targets must declare edit-expected vs verify-legitimate).

### 4. rename-base-body-files-to-canonical-naming — merged, 1D/1R/1F, ~13.5 min
The plan-gate Option A ruling collapsed the story to zero renames + verification before any build cost — gate working as designed. **Struggles:** 7 failed SendMessage calls across 3 of 5 agents (schema friction); 2 of 4 delivery-bearing agents needed idle nudges; a low-severity planning-validator finding outside the ruled scope evaporated and was re-discovered from scratch by AVFL (investigate: capture path for out-of-scope planning findings).

### 5. architecture-decision-26-update-for-base-body-collapse — merged, 1D/1R/1F, ~22 min
QA and CR independently converged on the same genuine citation defect — dual-reviewer value on docs stories; the AC5 grep gate caught an unenumerated stale mention; simplify netted the merge to -8 lines by removing fixer-accreted restatements. **Struggles:** the SendMessage JSON-coercion workaround was rediscovered independently by dev, fixer, and simplify; the orchestrator's relative-path bookkeeping wrote sprint JSON into the worktree and the recovery tripped the destructive-git hook (fix: absolute paths for conduct bookkeeping).

### 6. conductor-endgate-viewer-hijack-and-silent-gate — merged, 1D/1R/1F, ~82 min
Critical-priority defect story converged in one cycle; simplify correctly recognized cross-site directive duplication as load-bearing rather than flattening it; the coverage deferral was held ~9 days and discharged only on live end-gate observation of all five runtime legs. **Struggle:** coverage-plan.md claimed the per-story QA leg verified the 3 document-check scenarios, but the ledger shows REVIEWER A was fully deferred — the scenarios had no assigned verifier at merge (self-caught, queued as xnote pl-20260722T201533; fix: reconcile coverage-plan vs covered-by-composition semantics). Both dev and CR needed idle nudges.

### 7. conduct-adoption-retire-sprint-dev — merged, 1D/1R/1F
Resume-in-place absorbed an infra-wide API blip idempotently ("Task 1 done, Task 2 not yet applied" — applied only the delta); the deferral lifecycle was exemplary — held undischarged until `momentum-tools sprint complete` executed live at this build's own gate. **Struggles:** both pipeline agents needed completion-signal nudges; the story's 5-line insert into the shared Phase-5 approve block created the semantic-merge surface that later forced fixer-flagged build_invalidating integration (investigate: hot-file coordination at planning).

### 8. repair-phantom-story-file-entries-and-backfill-live-fixture-scope — merged, 1D/1R/1F, 26 min
The pipeline itself was pristine — 705/705 tests, disciplined write-scope exception documentation, and the story's own frozen smoke contract caught the debugprobe1 leak at E2E exactly as designed. **Struggles (all environmental/cross-story):** the sandbox-escape phantom write (Struggles §1, critical); no removal CLI forced a hand-edit exception to the sole-writer invariant; a same-sprint cross-story contradiction (create-story Step 7 direct index write vs sprint-manager rule 6 sole-writer) was caught only by AVFL iteration 3 (investigate: shared-invariant coherence checking below merge-review).

### 9. conduct-live-run-against-fixture-sprint — merged, 2D (1 effective)/1R/1F
Once unstalled, converged in ~13 minutes with three independent live executions of the driver — the 2026-06-28 structured-status failure mode genuinely prevented. **Struggles:** the ~3h05 stall with no watchdog (Struggles §3, high); the retry misdiagnosis raced the recovering agent and recorded a wrong diagnosis permanently in the ledger; the frozen contract was unexecutable from birth (grep-anchoring bug, freeze policy blocked repair); retro session discovery dropped this story's entire build session (mtime fragility); r2's SendMessage trial-and-error briefly desynchronized conductor and dev.

### 10. sprint-planning-cross-story-coherence-gate — merged, 1D/1R/1F
Clean single cycle on a large skill-instruction story; simplify caught reason-token drift the fix pass introduced; a ~13h interrupt landed mid-stage-3 and resumed to merge without rework. **Struggle:** merged with the developer-override path non-functional (Struggles §2, critical) because plan-gate-renderer.md was outside writable_files — the fixer flagged the residual honestly, escalation and the major-residual stub guard worked, but the feature is inert on its headline path until the renderer follow-up lands.

### 11. conduct-qa-execute-verification-method — merged, 1D/1R/1F
Single-cycle convergence; an API error at +5.5 min resumed in place; the QA deferral was discharged by the story's own deliverable executing live in three polymorphic methods — a self-validating composition. **Struggles:** CR caught the story shipping an unexecutable routing row (Skill tool instructed but absent from qa-reviewer's frontmatter grant) — a mechanically lintable defect class; story files show `status: ready-for-dev` while index.json says done (systemic write-back drift, investigate).

### 12. sprint-planning-continuous-execution-and-cli-fixes — merged, 1D/1R/0F, 21 min
The sprint's cleanest run: zero findings on both review legs, fix loop legitimately skipped, frozen contract pre-verified red on the live bug flipped 5/5 green post-fix. **Struggles:** the contract author's read-isolation breach was self-disclosed but never dispositioned by the orchestrator (fix: mandatory disposition); AVFL caught a help-text/behavior mismatch both legs missed (net working as intended); sprint-planning/workflow.md at ~1273 lines (2.5x the NFR guidance) keeps accreting with no decomposition plan and no owner for the flag (investigate).

### 13. sprint-planning-handoff-artifact — merged, 1D/1R/1F
Clean convergence; the ~13h fixed-but-uncommitted worktree gap resumed cleanly; planning checkpoint caught a spec self-contradiction. **Struggles:** producer-without-consumer — every layer validated emission only, and AVFL invented the consumer post-merge (investigate: coherence-gate check); the feature has never behaviorally fired (all verification was prose-trace; the next planning run is the real acceptance test and nothing schedules that check); a routine AVFL residual (architecture.md:1812 still claims sprint-dev consumes the artifact) exited the sprint with no discharge path and is verified still live (fix: one line).

### 14. conduct-resume-and-rehydration-idempotency-hardening — merged, 1D/1R/1F
CR caught the dev reintroducing the story's own target defect class (resume re-running --target verify from verify) and the fix added eval coverage; acceptance was discharged against the sprint's own real 13.5h interrupt — zero duplicate ledger events across the boundary. **Struggles:** 4/4 subagents needed completion-signal nudges (one 54-min latency while the session was active); the 3-commit semantic rebase across the shared Phase-5 block produced control flow no parent story validated; a low-severity emitter/schema doc drift (workflow.md:2623 `phase: end-gate-approve` vs build-ledger.md:119) survived sprint close because low residuals get no stub.

### 15. conduct-conductor-staging-and-ledger-append-safety — merged, 1D/1R/1F
The strongest single piece of evidence for the escalation tier: the dev implementation introduced a new instance of the exact hazard the story targeted (in-scope untracked deliverables silently dropped and destroyed), and eval contract → code review → stakes routing → end-gate developer choice (cards D1/D3, commit 4964ff7) caught and fixed it. Coverage deferral discharged with checkable composition evidence. **Struggles:** the doctrine change (retiring printf append) shipped without a sibling-eval sweep — the fork survived five gates to AVFL iteration 2 (fix: mandatory retired-construct grep-sweep); planning coherence check produced a false "still unapplied" verdict by grepping tokens that legitimately remained (fix: assert absence of exact OLD strings).

---

## Cross-Cutting Patterns

1. **The pipeline's quality machinery is sound; its operational plumbing is the tax.** Not one story failed on spec quality, review quality, or merge integrity. Nearly all friction concentrates in agent-harness seams: signaling (Struggles §4), stall detection (§3), state isolation (§1, §11), and self-observability (§7). Fix the plumbing without touching the gate structure.

2. **Every high-severity defect that shipped or nearly shipped traces to a scoping/modeling gap, not an execution error.** The inert override path (renderer outside writable_files), the 2-day seam repair latency (consumer outside scope), the phantom write (shim resolution outside the worktree model), and the never-consumed handoff artifact (no consumer-existence check) are all failures of what planning *can express*, not of what agents did.

3. **Self-detection worked; self-repair paths lag.** The practice caught its own defects remarkably well — the coherence-gate contradiction was self-identified at build time, the coverage-plan mismatch self-caught and queued, the deferral system refused rubber stamps. But detection outruns discharge: low-severity residuals evaporate (no stub path), triaged-out items live only in sprint files, and self-reported breaches get no recorded disposition. The finding lifecycle needs a floor for below-major items.

4. **The same knowledge keeps being re-purchased.** Documented gotchas re-paid by every wave, identical failed probes across four agents, the SendMessage workaround rediscovered independently by at least six agents, and 44% of agents anonymous to cost attribution. Spawn-time context injection is the single cheapest efficiency lever in the sprint.

5. **Recursion validated the sprint's own theses.** The resume hardening absorbed the sprint's own interrupts; the staging-safety escalation tier caught the staging-safety story's own hazard; the phantom-repair story's frozen contract caught a live phantom; the qa-execute story's deliverable discharged its own coverage. Conversely, the two features that *couldn't* self-validate (coherence gate override, handoff artifact) are exactly the ones carrying live risk — first-live-firing observation is now the critical path for both.

6. **Human attention was spent almost entirely on machine-owned problems.** CLI rendering, hook regexes, stall detection, config presets. The one place human judgment was genuinely exercised — the plan gate and end-gate cards — worked exceptionally well. The goal for next sprint: keep humans at the gates, out of the boiler room.

---

## Metrics

| Metric | Value |
|---|---|
| User-channel messages | 144 (91 teammate/agent-relayed; 54 pure idle notifications) |
| Subagent transcripts | 163 (92 role-named, 71 generic-named) |
| Agent summaries parseable | 42 of 163 (121 parse errors — see Struggles §7) |
| Errors logged | 69 (27 in the wave-1 launch hour; all recovered) |
| Team messages | 217 (84 = SendMessage schema loads, 39%) |
| Stories merged | 15 / 15 |
| Single-cycle convergence | 13 of 15 stories |
| Build-ledger events | 156 (15 launched, 15 terminal, 35 finding-dispositions, 22 AVFL findings, 8 stage-3 escalations) |
| Finding dispositions | 27 fixed / 4 triaged-out / 2 dismissed / 2 escalated; 0 overturned as wrong |
| Stage-3 escalations | 8, all end-gate-expanded (none paused the build) |
| Verified retro findings | 111 — 46 successes (keep), 41 fix, 24 investigate |
| Finding severity | 7 high / 37 medium / 67 low |
| Duplicate completion sends | 6 in one session (no double-processing — dedup held) |
| Conductor idle nudges | Load-bearing: 4/4 agents on one story; up to 54 min nudge latency |
| Longest stall | ~3h05 of a 3h19 story (human-detected) |

---

## Priority Action Items

Ranked. Each: title, priority, source, suggested story-stub ACs.

### 1. Enforce worktree isolation for momentum-tools shared-state writes, and add a sanctioned index-entry removal command
- **Priority:** critical
- **Source:** sandbox-escape-state-leak (high, repair-phantom) — installed shim's sibling-directory lookup beats MOMENTUM_HOME, so a worktree probe wrote phantom `debugprobe1` into the live stories index; missing-removal-cli (medium) — cleanup required a hand-edit exception to the sole-writer invariant; queued endgate-fix-6 follow-up.
- **Suggested ACs:**
  - Given MOMENTUM_HOME points at a worktree, when any momentum-tools state-writing command runs, then writes land in that worktree's .momentum (or the command fails loudly) — never in the main repo.
  - `momentum-tools sprint story-remove --slug <s>` exists, validates, and is the only sanctioned removal path; the sole-writer invariant needs no hand-edit exceptions.
  - A regression probe (the debugprobe1 scenario) runs in CI/smoke and asserts zero main-repo index mutation.
  - The queued create-story write-path fix (Step 7 direct read-modify-write bypassing cmd_story_add) is landed and the cross-story contradiction with sprint-manager rule 6 is resolved.

### 2. Land the plan-gate renderer fork-id follow-up before the coherence gate's first live firing
- **Priority:** critical
- **Epic:** momentum-sprint-planning-to-ready
- **Source:** major-residual-merged (high, coherence-gate) — STRU_A-002: renderer ForkItem has no id field, gate Step 8 matches overrides by id, so developer overrides classify as "NOT an override" and hold the sprint; developer verdict queued it "to land before the coherence gate first live firing" (= next sprint-planning run).
- **Suggested ACs:**
  - plan-gate-renderer.md emits a stable fork id per ForkItem and its gate JS keys verdict lines by that id.
  - coherence-gate.md Step 8 id-matching succeeds against a rendered gate fixture, including the developer-override path (override honored, sprint proceeds).
  - The first live coherence-gate firing is observed and the override path's behavior recorded as the discharge evidence.

### 3. Repair the retro audit-extraction pipeline (parser, inputs, session discovery)
- **Priority:** high
- **Epic:** momentum-sprint-retro
- **Source:** retro-extraction-defect (high) — 121/163 summaries lost to the STRUCT→VARCHAR cast at transcript-query.py:427; retro-extraction-gap (medium) — documented inputs (build-results.jsonl, finding-cards.json) don't match conduct's actual build-ledger.jsonl; retro-evidence-gap (medium) — mtime-keyed discovery silently dropped the wave-2 build session.
- **Suggested ACs:**
  - query_agent_summary parses toolUseResult without the VARCHAR-cast defect; re-run against sprint-2026-07-13 yields ≥95% parseable agent summaries.
  - Retro Phase-2 preprocessing reads build-ledger.jsonl as the primary conduct build record; spec and extract layout agree.
  - Session discovery keys on transcript content timestamps, not file mtime; a resumed/re-read session inside the window is never dropped.

### 4. Add a per-agent stall watchdog and verified retry diagnosis to the Conductor
- **Priority:** high
- **Epic:** momentum-conductor-core
- **Source:** stall-detection-gap (high + medium) — ~3h05 and ~2h stalls detected only by the developer; retry-misdiagnosis-race (medium) — TaskStop raced a recovering agent and a wrong diagnosis was permanently ledgered; handoff-constraint-contradiction (medium) — contradictory spawn constraints caused one wedge.
- **Suggested ACs:**
  - The Conductor detects a subagent with no tool-result progress past a configurable threshold and runs probe (TaskOutput) → warn → stop/redispatch without human involvement.
  - Retry ledger entries record verified state (disk + transcript probe), not inferred diagnosis; a just-completed artifact is adopted, not redone.
  - Dispatch prompts are checked for instruction/constraint contradictions (e.g., delegate-via-spawn vs no-spawn) before launch.

### 5. Overhaul the subagent completion-signal protocol
- **Priority:** high
- **Epic:** momentum-agent-spawn-orchestration
- **Source:** ~10-finding cluster: subagent-completion-signal-nudges (4/4 agents, 54-min latency), sendmessage-schema-friction (7 failed calls on one story; repeated on 3 stories), duplicate-completion-signals (6 resend events), sendmessage-schema-load-overhead (84/217 team messages), reply-address ambiguity (71 team-lead vs 35 main), handoff-signal-reliability.
- **Suggested ACs:**
  - SendMessage is pre-granted to all conduct subagents (no ToolSearch bootstrap round-trip).
  - Every spawn prompt embeds a literal working SendMessage example (string message, required summary, pinned reply address) and lists signal delivery as the final mandatory task.
  - Completion signals carry an idempotency key; the Conductor acks receipt, and a nudge is only sent after ack-timeout — duplicate payloads are impossible to double-process.
  - Observed nudge rate on the next conducted sprint drops below 1 in 4 delivery-bearing agents.

### 6. Fix AVFL-on-merge convergence scoring to exclude end-gate-held findings
- **Priority:** high
- **Epic:** momentum-quality-gates-enforced
- **Source:** fix-cycle-convergence (high) — NON_CONVERGENT verdict was structural (5 held stakes findings re-counted each iteration); actual residual was 3 routine doc items; scores also unstable (51→46 after fixes).
- **Suggested ACs:**
  - The convergence score excludes findings routed to end-gate tiers; they are reported as a separate escalations count.
  - A corpus whose only open items are end-gate-held findings reports CONVERGED-with-escalations, not NON_CONVERGENT.
  - Iteration-over-iteration score deltas on an unchanged corpus stay within a documented stability band.

### 7. Extend writable_files modeling: out-of-repo surfaces, seam consumers, and producer-consumer existence
- **Priority:** medium
- **Epic:** momentum-sprint-planning-to-ready
- **Source:** write-scope-gap (kb-buildout wiki-query ratification), seam-consumer-out-of-scope (constitution-builder, ~2-day repair latency), writable-files-scoping-gap (coherence-gate renderer → the critical inert path), producer-without-consumer-gap (handoff artifact consumer invented post-merge by AVFL).
- **Suggested ACs:**
  - Stories can declare out-of-repo write surfaces; AC-mandated out-of-repo edits require no post-hoc ratification.
  - When an eval contract declares a producer/consumer seam, plan-time scoping pulls the consumer into writable_files or creates a paired depends_on story.
  - The coherence gate flags any story that produces an artifact no skill/workflow consumes.

### 8. Execute frozen contracts before freezing, and disposition self-reported authoring breaches
- **Priority:** medium
- **Epic:** momentum-quality-gates-enforced
- **Source:** frozen-contract-defect (smoke.sh grep-anchoring bug made the proof story's contract unpassable; frozen after `bash -n` only), frozen-contract-isolation-breach + planning-checkpoint findings (read-isolation is convention-only; one self-reported breach absorbed with no recorded accept/re-author).
- **Suggested ACs:**
  - Every verification contract is executed against sample/synthetic driver output before freeze; a contract that cannot pass its own self-check cannot freeze.
  - A self-reported compliance breach by a contract author receives a recorded disposition (accept / re-author) in the planning session log.
  - Contract-author read-scoping is either mechanized or formally documented as disclosure-based.

### 9. Bake known environment facts into conduct spawn prompts and enforce agent naming
- **Priority:** medium
- **Epic:** momentum-agent-spawn-orchestration
- **Source:** harness-friction-duplication (27 launch-hour errors re-paying documented gotchas), redundant-rediscovery (identical failed AVFL probe x4, blocked sleep x5), cost-attribution-gap (71/163 generic-named agents, 19.2 MB unattributable).
- **Suggested ACs:**
  - A standard environment-facts block (Monitor-not-sleep, flat roster, SendMessage shape, AVFL invocation path, hook-denial patterns) is included in every conduct spawn prompt or base body.
  - Known-gotcha error classes drop measurably (target: <10 wave-launch errors on the next conducted sprint).
  - All conduct spawns use the role-slug naming convention; zero generic-named agents in the next sprint's transcript set.

### 10. Sprint-planning hot-file coordination
- **Priority:** medium
- **Epic:** momentum-sprint-planning-to-ready
- **Source:** hot-file-contention + hot-file-semantic-merge-contention (6 stories on conductor/workflow.md; 3 on one Phase-5 block; integrated flow "neither parent story validated", build_invalidating), doctrine-change-without-sibling-sweep (printf-append fork survived 5 gates), cross-story-invariant-contradiction (caught only at AVFL iter 3).
- **Suggested ACs:**
  - Planning detects when ≥2 selected stories write the same file and requires a declared coordination strategy (serialize, integration owner, or shared-block contract) before gate sign-off.
  - Mechanism/doctrine retirements require a grep-sweep AC for the retired construct across evals and references.
  - Shared-invariant declarations (e.g., sole-writer rules) are checked for contradiction across the sprint's story set at the coherence gate.

### 11. Reconcile coverage-plan claims with covered-by-composition deferral semantics
- **Priority:** medium
- **Epic:** momentum-conductor-core
- **Source:** coverage-plan-vs-deferral-semantics-mismatch (endgate-viewer) — coverage-plan.md claimed the per-story QA leg verified 3 document-check scenarios while the ledger shows REVIEWER A fully deferred; the scenarios had no assigned verifier at merge. Already queued as practice-ledger xnote pl-20260722T201533256847-665bd0e1 — this item carries it so it doesn't die in the queue.
- **Suggested ACs:**
  - The coverage plan cannot claim a QA leg for a story whose disposition is covered-by-composition, or covered-by-composition still runs document-check-only QA legs — one rule, applied consistently.
  - A validator cross-checks coverage-plan.md claims against ledger coverage-disposition events at end-gate.

### 12. Commit the hookify block-destructive-git fix with checked-in test cases
- **Priority:** medium
- **Epic:** ad-hoc
- **Source:** correction (hook misfire) — the overbroad regex denied `git checkout -- .momentum/...` file paths three times mid-build, escalating prompts cross-session; the fix was applied live to .claude/hookify.block-destructive-git.local.md and verified against six cases, but lives only in a local file.
- **Suggested ACs:**
  - The corrected pattern is committed (dot-prefixed file paths allowed; whole-tree `git checkout -- .` still blocked).
  - The six verification cases are checked in as an executable test the hook rule must pass.

### 13. Quick-fix batch: residual doc drifts and the conduct-era story template
- **Priority:** low
- **Epic:** ad-hoc
- **Source:** unfixed-residual-doc-drift (architecture.md:1812 claims sprint-dev consumes the build-handoff; verified still live 2026-07-30), residual-doc-drift-still-live (workflow.md:2623 emits `phase: end-gate-approve`; build-ledger.md:119 doesn't document it), template-pipeline-mismatch + story-file-record-drift (Dev Agent Record blank + `status: ready-for-dev` on done stories — burned 2 QA findings this sprint).
- **Suggested ACs:**
  - architecture.md:1812 names only momentum:conduct as the build-handoff consumer.
  - build-ledger.md documents the end-gate-phase-complete row shape.
  - Conduct-era story specs either drop the Dev Agent Record section and get a status write-back at merge, or QA reviewers are pre-briefed that blank is expected — zero findings burned on it next sprint.

### 14. Pre-conduct session checklist (model/effort preset + conditional plugin update)
- **Priority:** low
- **Epic:** momentum-conductor-core
- **Source:** redirection (developer interrupted a just-started conduct run to set /model + /effort, then re-invoked), correction (plugin-update memory note applied unconditionally; only meaningful after a release merges to main).
- **Suggested ACs:**
  - The fresh-session-before-conduct protocol includes a set-model/set-effort step before invocation.
  - The plugin-update guidance is conditioned on a release having merged since the last update.
