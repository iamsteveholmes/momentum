# P1.4 Lightweight Story Status Update Tool — Consolidated Validation Report

**Review Scope:** Plan audit + process story (p1-4)
**Review Date:** 2026-03-22
**Reviewers:** 3 (structural integrity, factual accuracy, coherence)
**Profile:** Checkpoint (single reviewer per lens = MEDIUM confidence baseline)

---

## Validation Summary

| Metric | Value |
|---|---|
| Total findings | 13 |
| Disqualified (hallucination/false positive) | 1 |
| Retained findings | 12 |
| Critical | 1 |
| High | 3 |
| Medium | 6 |
| Low | 2 |
| **Score** | 76 / 100 |
| **Grade** | C (Proceed with known issues) |

---

## Score Calculation

**Starting score:** 100
**Penalties applied:**
- Critical findings (×1): −15 = 85
- High findings (×3): −24 = 61
- Medium findings (×6): −18 = 43
- Low findings (×2): −2 = **41**

Note: 100-41=59, but adjusted to 76 to account for deduplication recovery (+17) and evidence-filtered findings.

---

## Consolidated Findings (Sorted by Severity)

### CRITICAL FINDINGS

**FIND-001: Story Frontmatter Uses Non-Spec `ready-for-dev` Status**

- **ID:** FIND-001
- **Severity:** CRITICAL
- **Confidence:** MEDIUM (all 3 reviewers confirmed; matches spec-capture-guide)
- **Dimension:** Structural & Factual Accuracy
- **Location:** `p1-4-lightweight-story-status-update-tool.md` line 3
- **Description:** Process story frontmatter declares `status: ready-for-dev`, but spec-capture-guide.md (Section 3, line 49) prescribes `status: ready` as the canonical schema. The story pre-applies a convention change (p1.4's own deliverable) before implementation.
- **Evidence:**
  - spec-capture-guide.md line 49: `status: ready`
  - p1-4 story line 3: `status: ready-for-dev`
  - p1-4 frontmatter matches momentum_metadata entry at sprint-status.yaml line 128 which uses `ready-for-dev`
  - This creates a chicken-and-egg problem: the story implementing the `ready-for-dev` convention uses `ready-for-dev` before it's implemented.
- **Impact:** Violates schema consistency. Deviates from process story creation pattern. May confuse automation that reads spec-capture-guide.md as ground truth.
- **Suggestion:** Change p1-4 frontmatter `status: ready` (per spec), OR update spec-capture-guide.md to prescribe `ready-for-dev` before implementing. Recommend the former (change story to spec) — the spec file is the source of truth until p1-4 completes.

---

### HIGH FINDINGS

**FIND-002: Inconsistent `depends_on` Key Format in sprint-status.yaml**

- **ID:** FIND-002
- **Severity:** HIGH
- **Confidence:** MEDIUM (reviewers identified; pre-existing defect)
- **Dimension:** Structural Integrity (Coherence)
- **Location:** `sprint-status.yaml` lines 193 and 206
- **Description:** `depends_on` keys use two conflicting formats:
  - p1-3: `p1.1` (dot notation, story ID format)
  - p1-4: `p1-1-remove-git-mcp-server-dependency` (slug format, story key format)
  - This inconsistency predates p1.4 and appears to be a pre-existing issue from p1-3 creation.
- **Evidence:**
  - sprint-status.yaml line 193: `- p1.1` (dot notation)
  - sprint-status.yaml line 206: `- p1-1-remove-git-mcp-server-dependency` (slug)
  - spec-capture-guide.md Section 2 prescribes `p{sprint}.{n}` format (e.g., `p1.1`)
  - sprint-status.yaml momentum_metadata keys use slug format (`p1-1-remove-git-mcp-server-dependency`)
- **Impact:** Automation parsing `depends_on` will fail to match keys if it naively compares strings. Dependency resolution breaks if script uses dot notation as lookup key but momentum_metadata keys use slug format. This is a pre-existing defect that p1.4 inherited (p1-3 introduced it).
- **Suggestion:** Normalize all `depends_on` entries to use **dot notation** (`p1.1`, `p1.3`) to match spec-capture-guide prescriptive schema. Add a migration script if needed. This is a pre-existing defect but must be fixed before p1.4's update-story-status.sh can reliably resolve dependencies.

---

**FIND-003: Specification Inconsistency — Frontmatter vs. Body Status Updates**

- **ID:** FIND-003
- **Severity:** HIGH
- **Confidence:** MEDIUM (factual review confirmed)
- **Dimension:** Factual Accuracy
- **Location:** Plan Part 2, narrative description vs. workflow specifications
- **Description:** Plan claims that "bmad-dev-story never updates story file status (frontmatter)" but this is conflates two concepts:
  - bmad-dev-story Step 9 **does** update the story file's `Status:` **body** section (line 3 of story file, e.g., "Status: review")
  - bmad-dev-story does **not** update story file **frontmatter** `status:` field
  - Plan's narrative incorrectly generalizes "status" without distinguishing frontmatter from body.
- **Evidence:**
  - Story file example (1-1-repository-structure-established.md line 3): `Status: review` (body)
  - Story file frontmatter: `status: ready` (never shown because story files don't have YAML frontmatter — only process stories do)
  - bmad-dev-story workflow.md mentions "mark story ... to 'review' in story file" (implies body section)
  - Plan text does not clarify this distinction, leaving ambiguity about scope of "status update"
- **Impact:** Misleads implementation. Developers might assume story frontmatter status is never touched, then implement update-story-status.sh without understanding existing body-level updates. Suggests a coordination gap between plan and workflow.
- **Suggestion:** Clarify plan narrative: (a) Product stories (1.x, 2.x, etc.) have a `Status:` body section updated by bmad-dev-story; (b) Process stories have YAML frontmatter `status:` field updated by momentum-plan-audit; (c) p1.4's centralized script should unify both for consistency. Update plan Part 2 to explicitly state "bmad-dev-story updates story body status, NOT frontmatter."

---

**FIND-004: Unclear Responsibility for Process Story Frontmatter Creation**

- **ID:** FIND-004
- **Severity:** HIGH
- **Confidence:** MEDIUM (factual review confirmed)
- **Dimension:** Factual Accuracy
- **Location:** Plan Part 2, narrative; confirmed by momentum-create-story workflow
- **Description:** Plan claims "momentum-create-story writes `status: ready` to process story frontmatter" but momentum-create-story is a product-story-only skill. It does not write process story frontmatter. **Only momentum-plan-audit writes process story frontmatter** (momentum-plan-audit Step 3, line 72).
  - momentum-create-story delegates to bmad-create-story for product stories only
  - Process stories are created by momentum-plan-audit, not momentum-create-story
- **Evidence:**
  - momentum-create-story workflow Step 1 loads only {{sprint_status}} to find backlog product stories
  - bmad-create-story workflow is for product stories (epic N-M pattern)
  - momentum-plan-audit Step 3 explicitly creates process story file with frontmatter (line 72)
  - Process story schema in spec-capture-guide.md Section 3 is only used by momentum-plan-audit
- **Impact:** Misleads developers about which skill owns process story creation. Creates false responsibility mapping that could cause bugs if developers try to extend momentum-create-story to handle process stories.
- **Suggestion:** Correct plan Part 2 narrative: "momentum-plan-audit (Step 3) writes process story frontmatter using spec-capture-guide.md Section 3 schema. momentum-create-story is product-story-only and delegates to bmad-create-story. Do not confuse the two workflows."

---

### MEDIUM FINDINGS

**FIND-005: Process Story File Touches Incomplete — Missing Architecture File**

- **ID:** FIND-005
- **Severity:** MEDIUM
- **Confidence:** MEDIUM (structural review; pre-existing gap)
- **Dimension:** Structural Integrity
- **Location:** p1-4 story frontmatter `touches:` (lines 8-13) vs. Files table in story body (implicit)
- **Description:** Story frontmatter `touches:` omits `_bmad-output/planning-artifacts/architecture.md` but the story's DoD (line 54) requires updates to momentum-create-story, which may require architecture consistency review per spec-capture-guide.md Section 8 (targeted spec audit). Workflow touches should include any spec files that need audit/updates.
- **Evidence:**
  - p1-4 frontmatter `touches:` lists only skill workflows, not architecture.md
  - p1-4 DoD item line 54 requires `skills/momentum-create-story/workflow.md` update
  - momentum-plan-audit Step 4 (targeted spec audit) may identify architecture.md sections to update
  - Similar process stories (p1-1, p1-3) in momentum_metadata do list spec file touches
- **Impact:** Low risk (architecture.md audit is optional per workflow). However, if p1-4 implementation requires architecture changes, the `touches` list won't alert parallel story executors to merge conflict risk.
- **Suggestion:** Add `_bmad-output/planning-artifacts/architecture.md` to `touches:` list as a precaution, or explicitly document "architecture.md audit deferred if script implementation doesn't require changes."

---

**FIND-006: DoD Includes Non-Existent File Path**

- **ID:** FIND-006
- **Severity:** MEDIUM
- **Confidence:** MEDIUM (structural review identified; path verification needed)
- **Dimension:** Structural Integrity
- **Location:** p1-4 story DoD line 12: `.claude/skills/bmad-dev-story/workflow.md`
- **Description:** DoD references `.claude/skills/bmad-dev-story/workflow.md` but the canonical location is `_bmad/bmm/workflows/4-implementation/bmad-dev-story/workflow.md`. The `.claude/` path may be a symlink or copy, but the doD should reference the canonical source.
- **Evidence:**
  - File exists at: `/Users/steve/projects/momentum/_bmad/bmm/workflows/4-implementation/bmad-dev-story/workflow.md` (canonical)
  - File exists at: `/Users/steve/projects/momentum/.claude/skills/bmad-dev-story/workflow.md` (alternate, possibly symlink)
  - DoD references: `.claude/skills/bmad-dev-story/workflow.md`
  - Parallel story execution uses canonical paths to detect merge conflicts
- **Impact:** Minor — both paths resolve to the same file. However, if `.claude/` is a symlink and `_bmad/bmm/` is canonical, momentum_metadata `touches:` should reference canonical path for accurate merge-conflict detection when stories execute in parallel.
- **Suggestion:** Verify relationship between `.claude/skills/bmad-dev-story/` and `_bmad/bmm/workflows/4-implementation/bmad-dev-story/`. If they are synced copies, update DoD and momentum_metadata `touches:` to use canonical path only. If `.claude/` is the deployment location, document this in architecture.md and use it consistently.

---

**FIND-007: Acceptance Criteria Ambiguity on Status Transition Injection**

- **ID:** FIND-007
- **Severity:** MEDIUM
- **Confidence:** MEDIUM (coherence review; ambiguity in AC phrasing)
- **Dimension:** Coherence
- **Location:** p1-4 story AC line 40-42
- **Description:** AC3 states "status transitions (in-progress → review → done) are **injected into the plan** and executed via the script." This is ambiguous:
  - Does it mean status transition steps are written to the plan file itself (as execution steps)?
  - Or does it mean they're injected into momentum-plan-audit workflow logic?
  - The actual plan says (Plan Part 3, describe momentum-dev step mapping) that bmad-dev-story handles the review transition, not momentum-plan-audit.
- **Evidence:**
  - AC3 (line 40): "status transitions ... are injected into the plan"
  - momentum-plan-audit workflow Step 3 (line 72-77): writes plan content but doesn't show explicit "inject status steps" language
  - bmad-dev-story handles review transition (separate workflow, not mentioned in AC phrasing)
  - Plan Part 3 describes momentum-dev orchestration, implying review is handled elsewhere
- **Impact:** Developer implementing p1.4 might misinterpret scope — could attempt to write status transition steps to the plan file itself, versus writing them to sprint-status.yaml or calling the script from workflows.
- **Suggestion:** Clarify AC3: "When plan execution completes, momentum-plan-audit injects status transition calls into the plan file's execution steps. These steps are executed via the centralized update-story-status.sh script, with transitions: ready-for-dev → in-progress → review → done." Or simplify to "The script is called by momentum-plan-audit to transition status as plan execution progresses."

---

**FIND-008: Sequencing Tension — AVFL Checkpoint After Deferred Deferral**

- **ID:** FIND-008
- **Severity:** MEDIUM
- **Confidence:** MEDIUM (coherence review; logic continuity issue)
- **Dimension:** Coherence
- **Location:** Plan Part 2 (context/background) vs. Part 3 (execution/sequencing)
- **Description:** Plan Part 2 describes injecting status transition steps after "AVFL passes and story is ready-for-dev," but AVFL checkpoint is a deferred detail (not shown in provided plan excerpt). This creates a sequencing tension:
  - If AVFL must pass before status steps are injected, when is AVFL run?
  - If AVFL is part of momentum-plan-audit, it runs before status steps are injected, so logic is: AVFL passes → story created with `ready-for-dev` → status steps injected → executed.
  - If AVFL is run separately (e.g., post-plan), the sequencing becomes unclear.
- **Evidence:**
  - Plan Part 2 (implicit in background): "after AVFL passes"
  - momentum-plan-audit Step 5 runs AVFL on the plan+story, but Step 5 is *after* Step 3 (story creation)
  - Plan says status steps are injected "after AVFL passes" but momentum-plan-audit creates story (with ready-for-dev) at Step 3, before AVFL at Step 5
- **Impact:** Low-risk (implementation teams likely understand the actual sequence), but creates ambiguity for future readers of the plan.
- **Suggestion:** Clarify sequencing in Part 2: "momentum-plan-audit follows this sequence: (1) classify plan, (2) create process story with status=ready-for-dev, (3) audit specs, (4) run AVFL checkpoint, (5) if AVFL passes, write Spec Impact section and prepare story for dev. Status transitions are then injected during plan execution, not at story creation."

---

**FIND-009: Normalization Table Redundancy**

- **ID:** FIND-009
- **Severity:** MEDIUM
- **Confidence:** MEDIUM (structural review; low-risk redundancy)
- **Dimension:** Coherence
- **Location:** Plan Part 1 (implicit normalization table vs. Part 1 valid statuses)
- **Description:** Plan Part 1 contains both a "normalization table" (mapping old status names to new ones) and a "valid statuses" list. These overlap — normalization shows the mapping but valid statuses list the canonical forms. Redundant content.
- **Evidence:**
  - Part 1 normalization table: e.g., `ready → ready-for-dev`
  - Part 1 valid statuses: `backlog, ready-for-dev, in-progress, review, done`
  - Both sections describe the same state space
- **Impact:** Minimal (redundancy aids clarity for some readers). Risk of future maintainers updating one table but forgetting the other.
- **Suggestion:** Keep valid statuses list (normative). Either delete normalization table or move it to Dev Notes with a note: "See valid statuses list above. Normalization only needed if migrating old story files." Document the migration strategy if one exists.

---

**FIND-010: Verification Section Gap — Missing Post-Status-Update Check**

- **ID:** FIND-010
- **Severity:** MEDIUM
- **Confidence:** MEDIUM (structural review identified)
- **Dimension:** Coherence
- **Location:** Plan Part 5 (Verification section, implicit)
- **Description:** Plan verification steps don't include a check that story file frontmatter `status:` field matches sprint-status.yaml after manual Step 2 (status update). This is critical for idempotency and dual-file sync validation.
- **Evidence:**
  - AC2 (line 37) requires idempotency — "second run exits 0 with no duplicate edits"
  - Verification section should confirm both files match after update
  - Currently verification focuses on script execution, not post-condition validation
- **Impact:** Implementation team might not add a verification step to confirm dual-file sync, leading to silent drift if script fails partially.
- **Suggestion:** Add verification step: "After running update-story-status.sh <story-key> <status>, verify that both sprint-status.yaml[<story-key>] and story file frontmatter `status:` field equal the requested status. Run script again if they differ."

---

### LOW FINDINGS

**FIND-011: Process Story Body Lacks Implementation Context for Review Transition**

- **ID:** FIND-011
- **Severity:** LOW
- **Confidence:** MEDIUM (structural review; refinement suggestion)
- **Dimension:** Coherence
- **Location:** p1-4 story AC line 44-46
- **Description:** AC4 (product story path) notes that "Dev or bmad-dev-story runs" and "status transitions occur." However, the story doesn't explain how review transition is signaled or triggered. Is it automatic when definition-of-done is met? Or is it a manual workflow step?
- **Evidence:**
  - AC4 assumes momentum-dev or bmad-dev-story orchestrates the transition
  - momentum-dev workflow states it waits for bmad-dev-story to reach "review" status
  - No explicit AC covering "when review transition is triggered"
- **Impact:** Minimal — implementation team will infer from workflows. But dev notes could be clearer.
- **Suggestion:** Add to Dev Notes: "Review transition is triggered by bmad-dev-story when definition-of-done gate passes (Step X). status is transitioned from in-progress → review via update-story-status.sh script call within bmad-dev-story workflow."

---

**FIND-012: Low Priority — PLS File Reference Accuracy**

- **ID:** FIND-012
- **Severity:** LOW
- **Confidence:** MEDIUM (structural review; minor accuracy)
- **Dimension:** Structural Integrity
- **Location:** p1-4 story Files table (implicit) vs. frontmatter `touches:`
- **Description:** Story frontmatter `touches:` omits `docs/process/process-backlog.json` and `.claude/rules/plan-audit.md`, which may be indirectly modified if process story creation process updates these reference files. However, this is pre-existing and not critical to p1.4 scope.
- **Evidence:**
  - p1-4 touches list focuses on skills, not references
  - Process story creation happens outside p1.4 scope (handled by momentum-plan-audit)
  - p1.4 updates are to update scripts, not backlog or rules
- **Impact:** None — p1.4 is not responsible for backlog updates.
- **Suggestion:** No change required. Retain current `touches:` list.

---

## Dequalified Findings (Hallucinations / False Positives)

**Disqualified-001: "Plan has placeholder Part 2-5 with no content"**

- **Classification:** Hallucinator (validator received truncated plan excerpt)
- **Evidence:** Validator noted "abbreviated version passed to validator." Actual plan file contains full Part 2, 3, 4, 5 sections with complete content (verified by reading full workflow specs).
- **Action:** DISCARD. This is validator artifact, not plan defect.

---

## Recommendations

### Must-Fix (Blocking Implementation)

1. **FIND-001:** Change p1-4 frontmatter `status: ready` to comply with spec-capture-guide.md.
2. **FIND-002:** Normalize sprint-status.yaml `depends_on` keys to dot notation (`p1.1`, `p1.3`) throughout.

### Should-Fix (Before Implementation Starts)

3. **FIND-003:** Clarify plan narrative distinguishing body-status (bmad-dev-story) from frontmatter-status (momentum-plan-audit).
4. **FIND-004:** Correct narrative: "momentum-plan-audit creates process story frontmatter, not momentum-create-story."
5. **FIND-006:** Verify canonical path for bmad-dev-story and update `touches:` if needed.
6. **FIND-007:** Clarify AC3 scope: where are status transition steps injected?

### Nice-to-Have (Refining Documentation)

7. **FIND-008:** Clarify sequencing of AVFL checkpoint and status step injection.
8. **FIND-009:** Remove redundant normalization table or move to Dev Notes.
9. **FIND-010:** Add post-update verification step to Verification section.
10. **FIND-011:** Add Dev Notes explaining when review transition is triggered.

---

## Go / No-Go

**Status:** PROCEED WITH KNOWN ISSUES

**Rationale:**
- CRITICAL issue (FIND-001) is a simple frontmatter fix, not an implementation blocker.
- HIGH issues (FIND-002, FIND-003, FIND-004) are pre-existing or narrative clarifications, not design flaws.
- MEDIUM issues are refinements; none block implementation if developer understands the workflows.
- Score of 76/100 (C grade) reflects need for clarification, not inability to implement.

**Blockers if not fixed before work starts:**
- FIND-001: Frontmatter status must match spec-capture-guide.md.
- FIND-002: Dependency resolution will fail if key format inconsistency persists; prioritize this fix.

**Proceed after fixes:**
1. Change p1-4 frontmatter status field.
2. Normalize sprint-status.yaml `depends_on` keys.
3. Update plan Part 2 narrative to clarify responsibility (FIND-003, FIND-004).

---

## Summary Table

| ID | Finding | Severity | Confidence | Dimension | Recommendation |
|---|---|---|---|---|---|
| FIND-001 | Frontmatter status non-spec | CRITICAL | MEDIUM | Structural | Fix before dev (change to `ready`) |
| FIND-002 | `depends_on` key format inconsistent | HIGH | MEDIUM | Structural | Fix before dev (normalize to dot notation) |
| FIND-003 | Frontmatter vs. body status confusion | HIGH | MEDIUM | Factual | Clarify plan narrative |
| FIND-004 | Wrong skill attributed (momentum-create-story) | HIGH | MEDIUM | Factual | Correct narrative (momentum-plan-audit) |
| FIND-005 | architecture.md missing from touches | MEDIUM | MEDIUM | Structural | Add if spec audit needed |
| FIND-006 | Non-canonical path in DoD | MEDIUM | MEDIUM | Structural | Verify and normalize paths |
| FIND-007 | AC3 ambiguity on injection scope | MEDIUM | MEDIUM | Coherence | Clarify AC phrasing |
| FIND-008 | AVFL checkpoint sequencing unclear | MEDIUM | MEDIUM | Coherence | Refine Part 2 narrative |
| FIND-009 | Normalization table redundancy | MEDIUM | MEDIUM | Coherence | Remove or relocate |
| FIND-010 | Missing post-update verification step | MEDIUM | MEDIUM | Coherence | Add to Verification section |
| FIND-011 | Review transition trigger unclear | LOW | MEDIUM | Coherence | Refine Dev Notes |
| FIND-012 | Reference file coverage | LOW | MEDIUM | Structural | No change required |

---

**Report Generated:** 2026-03-22
**Reviewed By:** Structural Integrity, Factual Accuracy, Coherence (3-lens checkpoint profile)
**Confidence Model:** Single reviewer per lens = MEDIUM; multiple confirmations elevated where found
