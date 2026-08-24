AVFL Adversary — Structural Integrity lens (corpus mode, skepticism 3, artifact stage: final)
Corpus: docs/research/gas-city-hitl-cycle-orchestration-2026-08-21/raw/ (9 files) vs scope.md
11 findings: 7 major, 4 minor.

---

**STRUCTURAL-A-001**
severity: major
dimension: corpus_completeness
location: corpus-wide (all 9 files) vs scope.md:frontmatter `goals` / `## Prior Decisions`
description: The scope names four goals; the fourth is the decision the whole exercise exists to serve. No file in the corpus addresses it. `DEC-035` appears ZERO times across all nine raw files, and the string `conductor` appears ZERO times in the entire corpus. The revisit clause has two triggers; the "out-of-session" half is covered incidentally (6 mentions across 3 files), and the "multi-Conductor" half — concurrent/parallel conductors, multiple simultaneous cycles, multi-city or multi-rig concurrency — has no substrate anywhere. The corpus LOOKS complete because 8 files map 1:1 onto 8 sub-questions; the goal that sits above the sub-questions is silently unserved, and synthesis cannot manufacture the missing half.
evidence: scope.md:3 — "produce the evidentiary basis for exercising DEC-035's revisit clause." scope.md:37 — "DEC-035 (2026-05-30): conduct adopted as execution engine; Gas City deferred with revisit clause = 'out-of-session or multi-Conductor goal appears'." Confirmed against the decision itself, dec-035-conduct-execution-engine-in-session-workflows-2026-05-30.md:86 — "revisit only if/when an out-of-session or multi-Conductor goal appears." Corpus greps: `DEC-035` → 0 hits in raw/; `multi-conductor|multi conductor` → 0 hits; `multiple conductors|concurrent sprint|parallel sprint` → 0 hits; `grep -rc -i "conductor" raw/*.md` → 0 for every file including the Gemini output.
suggestion: Before synthesis, add coverage (a follow-up subagent or a synthesis-stage section) scoring the evidence explicitly against BOTH revisit triggers: what Gas City buys for out-of-session dispatch (assemblable from existing files) and whether it enables multi-Conductor operation — e.g. concurrent formula runs over one rig, `max_dispatches_per_tick`, the v1.4.0 per-scope control-dispatcher requirement, the multi-city dolt port collisions in the 1.5 "Customer Zero" tranche. Failing that, the synthesis must state plainly that the multi-Conductor trigger was not researched.

---

**STRUCTURAL-A-002**
severity: major
dimension: completeness
location: gemini-deep-research-output.md:`## Follow-Up` → `### Q3: Dolt operational burden + file-backed beads status`
description: A declared section with no content. The file terminates at the Q3 heading followed only by blank lines and trailing whitespace — the third follow-up response was never captured. The research workflow's own AC6 requires each follow-up response to be appended under `## Follow-Up`; two of three were. Q3 targets sub-question 6 (Dolt vs GC_BEADS=file), which is precisely where the corpus carries an unresolved split (research-gate-mechanics-handson.md asserts no file escape hatch exists in 1.4.1; research-beads-coupling-dec028.md §2 documents it as alive and load-bearing). The one independent input that might have adjudicated it is blank.
evidence: `od -c` on the file tail: `# # #   Q 3 :   D o l t   o p e r a t i o n a l   b u r d e n   +   f i l e - b a c k e d   b e a d s   s t a t u s \n \n \n` then EOF. Workflow contract, skills/momentum/skills/research/workflow.md:228 — "After extracting the Deep Research report, send 2-3 targeted follow-up questions… Each response is appended under a `## Follow-Up` section." Frontmatter `extracted: 2026-08-24` vs `date: 2026-08-21` confirms the extraction ran three days later and did not complete.
suggestion: Re-run the Q3 follow-up and append the response, or delete the orphan heading and record the gap in frontmatter/limitations so synthesis does not read an empty section as "nothing found."

---

**STRUCTURAL-A-003**
severity: major
dimension: structural_validity
location: gemini-deep-research-output.md:body (lines 9–18)
description: The report body has no markdown structure. 18,897 characters of the main report sit on a SINGLE line with every heading concatenated into surrounding prose, and both of its tables are flattened into unparseable run-on strings with no row or cell delimiters. TOML configuration content is emitted as bare document lines (10–15) with no code fence, so config and prose are indistinguishable. The file contains ZERO ``` fences and exactly one heading (`## Follow-Up`) for a 4,462-word document. Every other corpus file uses H2 sectioning per the briefing template; this one is structurally unusable for section-targeted synthesis or citation.
evidence: Line 9 opens "Research Report: Gas City Human-in-the-Loop Gates and Multi-Phase Cycle OrchestrationExecutive SummaryThe transition from localized…" — title, section heading, and body glued together. Table 1 renders as "PrimitiveDefinition and Operational FunctionAgentThe configured worker (e.g., Claude Code, Codex) that executes assigned tasks…BeadThe universal persistence substrate…"; Table 3 as "IssueDescriptionCurrent Status and MitigationDispatcher Wedge (#2131 / #2168)Historic issues where…". Line 9 ends mid-construct at "This scaffolds the required configurations within city.toml:   Ini, TOML[workspace]", with lines 10–15 (`provider = "claude"`, `[providers]`, `[providers.claude]`, `base = "builtin:claude"`, `ready_delay_ms = 0`) dangling unfenced before prose resumes at line 16.
suggestion: Re-extract with structure preserved (or post-process): restore H2/H3 headings, re-form the two tables as pipe tables, fence the TOML blocks. If re-extraction is impossible, mark the file as raw unstructured input in its frontmatter so synthesis weights it accordingly.

---

**STRUCTURAL-A-004**
severity: major
dimension: completeness
location: gemini-deep-research-output.md (whole file) vs gemini-prompt.md:"Desired output"
description: The Gemini output contains 3 URLs total across 4,462 words and ZERO evidence-notation tags, against a prompt that explicitly required citations for every factual claim. Every other file in the corpus carries 20–57 URLs. The corpus's only independent triangulation source is therefore entirely uncheckable — including where it CONTRADICTS the empirically-verified files. A reviewer cannot adjudicate a conflict when one side cites nothing.
evidence: gemini-prompt.md:19 — "Citations with URLs for every factual claim". Measured: gemini-deep-research-output.md urls=3, [OFFICIAL]=0, [PRAC]=0, [UNVERIFIED]=0, [EMPIRICAL]=0; compare research-hitl-alternative-patterns.md urls=44, research-cycle-orchestration-fit.md urls=57. Uncited conflicting claim, line 25: "those exact file names do not appear in the current August 2026 release notes. However, Gas City does ship functionally equivalent mechanical housekeeping orders in its tagged releases… meaning they are not restricted to main/edge branches." — against research-notification-watcher-layer.md's verified 404s for those two order files at v1.4.1, v1.4.0 and v1.3.5.
suggestion: Tag the file as [UNVERIFIED]-by-default in synthesis, and adopt no Gemini-only claim that conflicts with an [EMPIRICAL] or URL-cited subagent claim without independent verification.

---

**STRUCTURAL-A-005**
severity: major
dimension: structural_validity
location: corpus-wide (all 8 research-*.md) vs skills/momentum/skills/research/references/briefing-template.md:"Primary Source Directive"
description: The corpus uses a fourth evidence tag, `[EMPIRICAL]`, 112 times, which is not part of the declared evidence notation and has no mapping in the synthesis carry-forward contract. The briefing defines exactly three tags and states anything else is ungrounded; output-structure.md maps only those three plus "claims with no attribution → UNGROUNDED (remove or flag)". `[EMPIRICAL]` marks the corpus's STRONGEST evidence class — first-hand reproduction (bd gate transcripts, repo greps at named commits, local measurements) — so the contract as written routes the most valuable claims toward being dropped or flagged. Only one of eight files defines the tag locally; the other seven use it undefined.
evidence: briefing-template.md — "- **[OFFICIAL]** … - **[PRAC]** … - **[UNVERIFIED]** … Every factual claim should have one of these tags. Claims without any tag are considered UNGROUNDED." `grep -rn "EMPIRICAL" skills/momentum/skills/research/` → no matches. Per-file counts: gate-mechanics 40, production-evidence 37, maturity 10, notification 10, human-verdict 5, beads-coupling 4, cycle-fit 4, hitl-alternatives 2. Sole local definition, research-production-evidence.md:"Method and evidence base" — "1. **[EMPIRICAL]** — direct grep/API queries against cloned repositories at named commits."
suggestion: Add `[EMPIRICAL]` to the briefing template's notation list and to output-structure.md's carry-forward mapping (highest trust, above [OFFICIAL] for behavioral claims), or normalize the corpus to the declared three-tag vocabulary before synthesis. Do not let synthesis silently downgrade 112 first-hand claims.

---

**STRUCTURAL-A-006**
severity: major
dimension: cross_reference_integrity
location: research-production-evidence.md:"Finding 1 — Zero formulas in the wild use `[steps.gate]`" and "Finding 3 — Packs that advertise 'human gates'…"
description: Every file+line citation in this file uses a `packs/…` path prefix that does not exist in the gascity-packs repository. Verified over the network: the repo has NO `packs/` directory — packs live at the repo root. All four cited paths 404 as written; the same paths resolve 200 with the prefix removed. This is the only file in the corpus with this defect (I resolved 17 gascity-packs paths and 27 gascity/beads paths cited elsewhere — all 200), and it lands on the two findings carrying this file's central claim that shipped packs implement "gates" as prompt text rather than structural blocks.
evidence: Cited: "— `packs/pr-pipeline/formulas/mol-pr-start.formula.toml` L108, `packs/contributing/formulas/mol-contributing-plan-implementation.formula.toml` L88–91"; "— `packs/gstack/assets/workflows/gstack-build/qa.md` L11–14"; "— `packs/gstack/assets/workflows/gstack-build/plan-review.md` L8–10". Verified: `GET api.github.com/repos/gastownhall/gascity-packs/contents/packs` → 404; repo root contains `bmad, cass, compound-engineering, contributing, discord, docs, gascity, gastown, github, gstack, oversight-rig, pr-pipeline, …`. `raw.githubusercontent.com/…/main/packs/gstack/assets/workflows/gstack-build/qa.md` → 404; `…/main/gstack/assets/workflows/gstack-build/qa.md` → 200. Same for the other three.
suggestion: Strip the `packs/` prefix from all four citations. The underlying evidence is sound — only the paths are wrong — but fix before synthesis copies the broken paths forward.

---

**STRUCTURAL-A-007**
severity: major
dimension: completeness
location: research-beads-coupling-dec028.md:§7 "What Adoption Forces or Unlocks for DEC-028" — "Re-scored against DEC-028's own gates" table
description: The file re-scores DEC-028 against a decision rule it quotes correctly as "3 of 4 gates positive", but its four-row table covers only G1, G3 and G4 — GATE 2 IS ABSENT — with the fourth row occupied by a non-gate ("Multi-agent write safety (D1 rationale)"). The table therefore looks like a complete 4-gate re-score while being structurally incapable of supporting the 3-of-4 arithmetic it invokes. Worse, Gate 2 is the specific gate DEC-028 makes the authoritative migration conditional on, so the omitted row is the load-bearing one for the go/no-go this file exists to inform.
evidence: File text: "DEC-028's Migration Go criterion is: 3 of 4 gates positive → flip beads authoritative", followed by a table whose Gate column reads only `G1 — did bd ready/--claim simplify scheduling?`, `G3 — was Dolt sync manageable under git-discipline?`, `G4 — did --spec-id linkage hold without in-tree loss?`, `Multi-agent write safety (D1 rationale)`. Ground truth, dec-028-beads-tracker-memory-substrate-adoption-2026-05-16.md:103 — "Gate 2 | End of spike sprint | Did `discovered-from` eliminate intake-queue triage toil? | No items lost; triage hop eliminated for at least 1 sprint worth of discovered work"; and line 94 — "3 — Authoritative Migration | … | **Conditional on Gate 2 passing**".
suggestion: Add a G2 row. If Gas City adoption is genuinely neutral to `discovered-from`/intake-queue toil, say so and mark it Neutral — an explicit "no new evidence" row preserves the 3-of-4 arithmetic; a silent omission does not.

---

**STRUCTURAL-A-008**
severity: major
dimension: corpus_completeness
location: research-beads-coupling-dec028.md:§2/§8 ↔ research-gate-mechanics-handson.md:"The defect: `type` and `timeout` are not persisted" ↔ research-hitl-alternative-patterns.md:§7(b)
description: The corpus's recommended adoption topology depends on a metadata-durability property that it flags as unverified and that NO file closes — an implied dependency documented nowhere. The recommended low-risk topology is a `GC_BEADS=file` city; the recommended gate design puts per-fork verdicts, artifact paths and gate status in BEAD METADATA; and the corpus separately proves the formula-cooked gate path already loses metadata (`await_type: null`). Whether `FileStore.SetMetadata` persists or inherits `MemStore`'s no-op is explicitly named a "must-check" — and the one file with a working `gc` install ran its probe against bd's embedded Dolt store, never against a file-backed city, so the hands-on pass did not close it either. At final stage the corpus recommends a configuration whose viability it has not established.
evidence: research-beads-coupling-dec028.md:§8 — "**FileStore metadata durability.** Whether `FileStore.SetMetadata` persists or inherits `MemStore`'s no-op is not stated in the fetched material **[UNVERIFIED]**. If Gas City's own gate/step bookkeeping rides on bead metadata, this is a hands-on must-check before trusting a file-backed city with `[steps.gate]` state." Same file §5 — "the low-risk topology is a city whose *own* work ledger is `GC_BEADS=file`." Same file §1 table — "`MemStore` | in-memory slice | Test double; `SetMetadata` is a no-op." Dependent recommendation, research-hitl-alternative-patterns.md:§7(b) — "stamps `momentum.plan_gate.artifact_path` and `momentum.plan_gate.status=waiting-human` on the workflow root." Hands-on scope, research-gate-mechanics-handson.md:"City setup" — the probe ran "backed by a plain `bd init` store using **bd's own embedded Dolt**", not a file-backed city.
suggestion: Close it before synthesis — `gc` is now installed globally (`mise use -g github:gastownhall/gascity@latest`), so a `GC_BEADS=file` city plus a `SetMetadata` round-trip is a short probe. Failing that, carry the caveat into the recommendation itself rather than leaving it in one file's appendix.

---

**STRUCTURAL-A-009**
severity: minor
dimension: cross_reference_integrity
location: research-maturity-open-bugs.md:"Project shape and release cadence (May–August 2026)"
description: An unresolvable citation with a literal ellipsis in place of the milestone id. It is also the one inline URL in this file that never appears in its `## Sources` section, so the reader has no second path to the referent. The claim it supports (milestone contents, the "Customer Zero" breakage tranche) is used as maturity evidence for the go/no-go.
evidence: "The `1.5` milestone (due 2026-08-04, already past) holds 11 open / 3 closed, dominated by a 'Customer Zero' dogfooding series (#4362, #4365, #4519–#4526)… [OFFICIAL] ([milestone 1.5](https://github.com/gastownhall/gascity/milestone/…))." Diffing inline URLs against the Sources list across all 8 files returns exactly one unlisted, unresolvable target: `https://github.com/gastownhall/gascity/milestone/…`.
suggestion: Replace with the concrete milestone URL (or an `is:issue milestone:1.5` search URL) and add it to `## Sources`.

---

**STRUCTURAL-A-010**
severity: minor
dimension: cross_reference_integrity
location: research-human-verdict-patterns.md:§5 "`[steps.gate]` — the actual blocking primitive, and the `bd gate` CLI"
description: Malformed section citation — the v2 spec's section number is missing entirely, leaving a bare `§`. The v1 half of the same citation is specific (`§4`). The quoted gate-synthesis text is real and the anchor exists, so this is a dangling pointer rather than a wrong one — but a reader following it lands on a 1,085-line spec with no section to look in.
evidence: "The spec ([formula-spec-v2 §, and formula-spec-v1 §4](https://docs.gascity.com/reference/specs/formula-spec-v2)) **[OFFICIAL]**:"
suggestion: Fill in `§2` (Compilation), where the gate-synthesis language lives — confirmed against docs/reference/specs/formula-spec-v2.md on `main` (`## 2. Compilation`, line 510).

---

**STRUCTURAL-A-011**
severity: minor
dimension: structural_validity
location: research-beads-coupling-dec028.md:§1 "The Provider Contract as It Stands Today"
description: The lead-in states four implementations; the table immediately below enumerates five, with no marker distinguishing the fifth from the four the cited architecture doc names. A reader cannot tell whether `exec.Store` is one of the four "backing stores" or an addition the author appended — which matters because `exec.Store` is the escape hatch the section later leans on.
evidence: "Gas City's bead store is a single Go interface with four implementations, selected at process start. The architecture doc names the interface's ten methods… and the four backing stores" — followed by a five-row table: `BdStore`, `NativeDoltStore`, `FileStore`, `MemStore`, `exec.Store`.
suggestion: Correct the count to five, or mark `exec.Store` explicitly as an additional provider not counted among the architecture doc's four backing stores.

---

CHECKED CLEAN (so the fix pass does not re-litigate): all 8 research-*.md carry the required frontmatter fields and a terminal `## Sources`; all code fences balance (an apparent table-column mismatch at research-human-verdict-patterns.md:228 is escaped `\|` inside cells — false positive); all formula-spec-v2 section anchors cited across the corpus (§0.2, §1.1–§1.3, §1.8, §2, §3.1–§3.4, §4, §5) exist in the live spec; the compile.go gate-synthesis line range and quoted `gateTitle` source line verify against `main` (526–559); all cited local Momentum paths exist (plan-gate-renderer.md, sprint-2026-08-03-plan-gate.html, both decision documents, .gitignore:87, .beads/hooks/); 44 of 45 external repo paths resolved 200 — the `packs/` prefix in A-006 is the sole outlier.

OUT OF LENS (deliberately left to Coherence & Craft's cross_document_consistency): open-issue counts 575 vs 1,011; whether `GC_BEADS=file` survives in 1.4.1; whether `gc` was installed; and the gate-(d) results-gate split ("Fits" in gate-mechanics/hitl-alternatives vs "Blocked — needs a barrier" in maturity-open-bugs).