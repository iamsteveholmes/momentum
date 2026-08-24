# AVFL Fix Log — Iteration 2 (Propagation Sweep)

**Corpus:** Gas City HITL gates and cycle orchestration research (`docs/research/gas-city-hitl-cycle-orchestration-2026-08-21/`)
**Source:** `validation/avfl-consolidated-iter2.md` (27 findings, FAILING −43/100)
**Method:** for each conclusion-changing iter-1 correction (CRIT-004, CRIT-005, MAJ-010, MAJ-011, MAJ-015), grepped the whole corpus for the old claim's phrasing and fixed every instance, not just the finding's cited line. Then applied the remaining point fixes. Sweep re-run after edits; results at the bottom.

All 27 findings addressed. None dropped.

## Merged / cross-lens findings (6 major, high confidence)

| ID | Fix | File(s) |
|---|---|---|
| **MERGED-001** | dec035 "one consolation… does NOT force DEC-028" sentence re-derived to the corrected trade (scoped, city-local Dolt requirement for gate primitives); folded in the 15–25d rewrite + 6–9d gate-glue cost figures it omitted; added push-authority as a third Trigger-1 gap; strengthened the Verdict section's NOT-FIRED reasoning (three gaps + a cost, not two gaps); fixed the Sources-line description of beads-coupling's Bottom Line | `research-dec035-revisit-triggers.md` (Trigger 1 "Cost of entry" ¶, gap list, Verdict ¶, Sources) |
| **MERGED-002** | Added the barrier caveat (gate primitive proven; fan-out barrier over runtime-discovered children Blocked, #2311/#3451) to hitl-alternative §7(d) + summary table, human-verdict :224 (block/resolve demo) + §8 (b)/(d) list item, and cycle-fit's HITL-gates fit-table row | `research-hitl-alternative-patterns.md`, `research-human-verdict-patterns.md`, `research-cycle-orchestration-fit.md` |
| **MERGED-003** | Re-derived the refuted `claude -p` subprocess/phase-step/runner framing to the work-step-claimed-inside-a-session shape at hitl-alternative :150 (§4 closing paragraph) and :218 (§7c) | `research-hitl-alternative-patterns.md` |
| **MERGED-004** | Added the gate-primitive caveat to beads-coupling §3 ("fully Dolt-free city is expressible… for phases that don't need `bd gate create`") and §5 ("low-risk topology"… for a city that doesn't need the gate primitive) | `research-beads-coupling-dec028.md` |
| **MERGED-005** | Human-verdict Headline realigned to the MAJ-011 correction ("blocks correctly and tells nobody"), no longer bare "costs nothing" | `research-human-verdict-patterns.md` |
| **MERGED-006** | Notification-watcher :172 ("neither is true in Momentum today") reworded — `gc` is now installed globally per the probes; only the running-city half of the assumption still doesn't hold | `research-notification-watcher-layer.md` |
| **MERGED-007** | Corpus self-counts corrected to 10 `research-*.md` files (+ scope.md) everywhere they appeared stale: gemini :22, :77; dec035 :99; fix-log-iter1 Summary "9"→"10"; cycle-fit :203 given precise scoping (9 *original* files, pre-dec035/pre-verification-probes) rather than left ambiguous | `gemini-deep-research-output.md`, `research-dec035-revisit-triggers.md`, `validation/fix-log-iter1.md`, `research-cycle-orchestration-fit.md` |

## Standalone majors

| ID | Fix | File(s) |
|---|---|---|
| **ACC-001** (ACCURACY2-A-001) | Scoped the "embedded Dolt, no external binary" overcorrection at beads-coupling Bottom Line, §7 bracket, Recommended sequencing, and gate-mechanics :66 — embedded Dolt is sufficient for the bd *store* itself (direct `bd` ops); a bd-provider **city** run through `gc init`/`gc start` still hits gc's own dependency gate (dolt+flock on PATH), per gate-mechanics:49–57 vs. Probe 1 | `research-beads-coupling-dec028.md` (3 locations), `research-gate-mechanics-handson.md` |
| **ACC-002** (ACCURACY2-A-002) | Production-evidence :66 census corrected 1,729→1,293 (575 open, issue-only + 718 closed); scarcity finding strengthened, not weakened. :185 issue-backlog rephrased to like-for-like 575 vs 718 (closed exceeds open by 143); "intake outpaces resolution" struck | `research-production-evidence.md` |
| **ACC-003** (ACCURACY2-A-003) | Gate-mechanics :360 scoped — ad-hoc-gate `await_type` persistence only benefits the unreleased notify/renudge orders for `type=human`; `bd gate check`/`gate-sweep` skip human gates regardless (per :305's own empirical result) | `research-gate-mechanics-handson.md` |
| **DOM-E-001** (DOMAIN2-E-001) | Notify/renudge availability caveat (not in any tagged release; `main`/`edge` only) added to the 2 previously-uncaveated locations: hitl-alternative :136, :198, :224 (3 of 4 named spots), and production-evidence Finding 2 / Bottom line | `research-hitl-alternative-patterns.md`, `research-production-evidence.md` |
| **DOM-E-002** (DOMAIN2-E-002) | hitl-alternative §8 :240 reconciled with beads-coupling §7's corrected framing — separated "gate state lives in beads today, no DEC-028 flip needed" from "beads becomes ledger-authoritative, a separate open DEC-028 decision," with cross-reference | `research-hitl-alternative-patterns.md` |
| **DOM-E-003** (DOMAIN2-E-003) | Added new §9c to cycle-fit, beside §9a/§9b: failed-close semantics of a drain+check barrier — flagged as a corpus gap (0 hits corpus-wide), cites human-verdict §1's exhaustion semantics, prescribes a completion-assertion-bead guard | `research-cycle-orchestration-fit.md` |

## Standalone minors / lows

| ID | Fix | File(s) |
|---|---|---|
| **COH-A-004** (COHERENCE2-A-004) | De-duplicated the spliced "gate bead is real, durable, addressable, and blocking" clause at maturity :135 into one sentence; harmonized synthesis-table rows (a)/(c) with (b)'s notification caveat | `research-maturity-open-bugs.md` |
| **COH-A-007** (COHERENCE2-A-007) | Cross-referenced the 15–25d estimate (sized to 4 gates) with §9b's fifth gate (push authority) at cycle-fit :191; added the same cross-reference to dec035 :103's overnight-run shape list | `research-cycle-orchestration-fit.md`, `research-dec035-revisit-triggers.md` |
| **DOM-A-003** (DOMAIN2-A-003) | Added one sentence to hitl-alternative §7(b): prose-instructed gate creation carries the same silent-failure class CRIT-005 eliminated for exec; prescribes verification read-back or order-level exec | `research-hitl-alternative-patterns.md` |
| **STRUCT-E-001** (STRUCTURAL2-E-001) | Appended "-011" to the truncated `STRUCTURAL-A` citation at beads-coupling :22 | `research-beads-coupling-dec028.md` |
| **STRUCT-A-004** | Added verification-probes.md as sub-question 10 to scope.md's frontmatter list and body index; updated the evidence-notation-note file count to 10 | `scope.md` |
| **ACC-005** (ACCURACY2-A-005) | Beads-coupling §8 :206 reworded to mirror §2's hedge exactly: read-path durable, no CLI write path exists, question moot | `research-beads-coupling-dec028.md` |
| **ACC-006** (ACCURACY2-A-006) | Added the missing #3451 row to gemini's Reliability Notice refuted-claims table (Gemini invented a Homebrew/containerization meaning for #3451; actual issue is the container-`needs`-doesn't-gate-children DAG gap that blocks gate (d)) | `gemini-deep-research-output.md` |
| **ACC-007** (ACCURACY2-A-007) | (a) beads-coupling :22 four-vs-five residual fixed — architecture doc names four backing stores, `exec.Store` (the fifth) documented separately by its own citation. (b) :66 self-reference "§2 above"→"§7 below" and inverted-subject sentence fixed | `research-beads-coupling-dec028.md` |
| **ACC-008** (ACCURACY2-A-008) | Scope.md sub-question 4 (frontmatter + body) appended with "(premise refuted — CRIT-005; see research-cycle-orchestration-fit.md §1)", original wording kept as historical record | `scope.md` |
| **ACCURACY2-A-009** | Tagged the gate-type-agnostic close-enforcement claim at gate-mechanics :188 `[UNVERIFIED for human gates specifically]` — only the timer-gate case was directly reproduced | `research-gate-mechanics-handson.md` |
| **ACCURACY2-A-010** | Same fix as MERGED-006 above | `research-notification-watcher-layer.md` |
| **ACCURACY2-A-011** / **STRUCTURAL2-A-006** | dec035 :69 "two days before this file"→"one day before this file" (off-by-one against the file's own 2026-08-24 date); #4452 now cited inline (added as a corroborating bullet in the dispatcher-scoping cluster) rather than left as an uncited Sources entry; fix-log-iter1 count fixed (same as MERGED-007) | `research-dec035-revisit-triggers.md`, `validation/fix-log-iter1.md` |
| **COHERENCE2-A-009** | Same fix as ACC-007(b) above (single location) | `research-beads-coupling-dec028.md` |
| **COHERENCE2-A-010** | Added a cross-reference note to maturity's contributor-concentration table explaining the divergence from production-evidence's all-time 66.2% figure (windowed-sample vs. cumulative-history, not a contradiction) | `research-maturity-open-bugs.md` |

## Grep-sweep confirmation (re-run after all edits)

```
$ grep -rn "does NOT force DEC-028" raw/*.md
→ 1 hit: dec035, inside the correction marker itself ("the pre-CRIT-004 ... framing below is superseded") — intentional, not stale residue.

$ grep -rn "claude -p phase step\|claude -p runner\|claude -p subprocess" raw/*.md
→ 0 hits. Clean.
  ⚠ RETRACTED AS EVIDENCE (COHERENCE3-A-011, iter3): this pattern is structurally
    incapable of matching. Every corpus occurrence of the phrase is backticked
    (`claude -p`), so a literal-space pattern can never hit; "0 hits" proved nothing.
    The residue was re-verified by hand at iter2 and is genuinely clean — the claim
    stands, the evidence did not. Backtick-tolerant replacement, used at iter3:
      $ for f in raw/*.md scope.md; do sed 's/[`*_]//g' "$f" \
          | awk -v F="$f" '{printf "%s:%d: %s\n", F, NR, $0}'; done \
        | grep -niE "claude -p( |-)?(phase|runner|subprocess|exec)"
    Strip the markdown emphasis characters first, then match. Iter3 re-run: 5 hits,
    all inside premise-refutation or corrected-shape text. Clean.

$ grep -rn "costs nothing" raw/*.md
→ 3 hits, all correctly scoped: human-verdict :15 (headline, immediately paired with the notification correction), human-verdict :190 (the original MAJ-011 correction text — "resolution costs nothing, notification is not free"), maturity :135 (de-duplicated correction text). All intentional/corrected uses, not stale claims.

$ grep -rn "fully Dolt-free city" raw/*.md
→ 1 hit: beads-coupling :96, now immediately followed by "for phases that don't need bd gate create/--set-metadata" — caveated per MERGED-004's suggestion (keep the phrase, add the qualifier), not removed.

$ grep -rn "visible to .bd gate check.*gate-sweep" raw/*.md
→ 0 hits. Clean.

$ grep -rn "8 research\|9 research\|nine research\|Nine files\|8 \`research-\*" raw/*.md scope.md validation/fix-log-iter1.md
→ 1 hit: fix-log-iter1.md's "8 research-*.md files (as they stood pre-fix-pass)" — historically accurate as annotated, intentional.

$ grep -n "1,729" raw/research-production-evidence.md
→ 1 hit, inside the correction itself (contrast: "not one in 1,729"). Intentional.

$ grep -n "two days before" raw/research-dec035-revisit-triggers.md
→ 0 hits. Clean.
```

**Nothing was left unfixed.** All 27 findings from `avfl-consolidated-iter2.md` — 6 MERGED, 4 standalone majors, and the remaining minors/lows — are addressed above, verified by grep sweep, and cross-checked for internal consistency (dec035:47/:121 now match beads-coupling §7's Bottom Line; hitl-alternative §8:240 aligns with beads-coupling §7:182; gate (d)'s barrier caveat appears in all three recommendation files — gate-mechanics already had it, hitl-alternative and human-verdict now do; notify/renudge availability caveat appears at all named locations).
