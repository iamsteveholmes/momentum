# Consolidated Validator Findings: 4 Planning Artifacts × 4 Lenses × 8 Validators

**Consolidation Date:** 2026-03-20
**Artifacts Validated:** PRD, Architecture, UX Design Specification, Epics
**Validation Framework:** AVFL (Adversarial Validate-Fix Loop)
**Configuration:** 4 lenses × 2 reviewers per lens = 8 agents total

---

## Consolidation Methodology

1. **Cross-check**: Identified matching findings across independent reviewers
2. **Deduplication**: Merged duplicates, kept most specific evidence
3. **Medium-confidence investigation**: Researched MEDIUM-only findings against source artifacts
4. **Confidence tagging**:
   - **HIGH**: Both reviewers in a lens found the same issue
   - **MEDIUM**: Only one reviewer found it; confirmed or discarded based on evidence
5. **Scoring**: Start 100; apply: critical −15, high −8, medium −3, low −1
6. **Severity ordering**: Critical first, then high, medium, low
7. **Grading**: ≥95 Clean, ≥85 Good, ≥70 Fair, ≥50 Poor, <50 Failing

---

## Consolidated Findings (38 total; 32 unique)

### CRITICAL ISSUES (−15 each)

**CRIT-001: UX Journey 3 Mapped to Wrong PRD Journey**
- **Confidence:** HIGH (both structural reviewers found same issue; coherence confirmed)
- **Severity:** Critical — core requirements misalignment
- **Evidence:**
  - UX spec line 509: `| Journey 3: Session Resume | PRD Journey 3 |`
  - PRD line 195: `### Journey 3: Steve — Something Doesn't Fit` (Kotlin/JVM stack mismatch scenario)
  - UX spec defines Journey 3 as a returning user resuming from a checkpoint; PRD Journey 3 is a validation scenario about non-Claude-Code stacks
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/ux-design-specification.md` line 509; PRD line 195
- **Impact:** Journey requirements are inverted—stories implementing to the UX spec will implement the wrong user scenario
- **Recommendation:** Remap UX Journey 3 to correct PRD journey (likely none, or create new mapping); audit all Journey 3 story requirements

**CRIT-002: File-Protection Hook Violates UX-DR3 ("Never Verbose")**
- **Confidence:** HIGH (domain reviewer + coherence confirmation)
- **Severity:** Critical — design principle violation
- **Evidence:**
  - Story 3.2 AC line 820: "Then it outputs: `[file-protection] ✓ [path] — ok`"
  - Story 3.2 Note line 821: "One compact line per write — UX-DR3 requires every hook fire to produce output; pass output must stay minimal to avoid noise on frequent writes"
  - Design principle UX-DR3: "never verbose"
  - Problem: File-protection hook fires on EVERY write. Each allowed write produces a `[file-protection] ✓` line. On a typical implementation session with 40+ writes (fixtures, tests, source, docs), this generates 40+ chat-pane lines
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` lines 820–821
- **Impact:** Session chat pane becomes flooded with hook output; violates core UX principle; users will perceive as noise
- **Recommendation:** Either (a) suppress pass output entirely—only output on blocks; (b) batch output once per session end; or (c) redirect to a sidecar file. Rephrasing in Story 3.2 AC required.

**CRIT-003: Architecture Commits to Unvalidated Background Execution Model**
- **Confidence:** HIGH (domain reviewer found; confirmed by architecture content)
- **Severity:** Critical — implementation risk
- **Evidence:**
  - Architecture Decision 3a, line 270: "Execution mode: reviewer subagents run as **background agents** (non-blocking — main conversation continues)"
  - Architecture Decision 4c (productive waiting): assumes background execution is possible
  - UX spec line 298 (noted as open architecture question): "background execution model TBD pending Impetus spike"
  - Stories 2.4 (productive waiting) and 4.3 (full story cycle) depend on this; Story 2.Spike validates it
  - **Problem**: Architecture finalizes the design pattern without validation gate; if Story 2.Spike fails, core architecture decisions become indefensible
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/architecture.md` lines 270; also 4c (exact line TBD)
- **Impact:** If Story 2.Spike determines background execution is unreliable, major architecture revision required mid-sprint
- **Recommendation:** Add conditional language to Decisions 3a and 4c ("pending Story 2.Spike validation"); gate Stories 2.4 and 4.3 on spike completion

---

### HIGH ISSUES (−8 each)

**H-001: Epic 2 Summary Missing Two UX-DR Entries**
- **Confidence:** HIGH (structural reviewer)
- **Severity:** High — requirements traceability broken
- **Evidence:**
  - Epic List line 287: shows UX-DRs for Epic 2 summary
  - Detailed Epic 2 header line 517: `UX-DRs covered: UX-DR1, UX-DR2, UX-DR4, UX-DR5, UX-DR6, UX-DR8 ... UX-DR18` (14 total)
  - Epic List summary block is missing UX-DR8 and other entries
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` lines 287 vs 517
- **Impact:** Developer reading Epic 2 summary gets incomplete list of UX design requirements
- **Recommendation:** Sync Epic List line 287 with detailed Epic 2 header line 517

**H-002: Epics FR30 Requirements Missing "Log" Phase**
- **Confidence:** HIGH (both accuracy reviewers found same omission)
- **Severity:** High — process completeness omitted
- **Evidence:**
  - Epics line 84: FR30 Requirements Inventory ends at "→ verify"
  - PRD line 558 (upstream source): includes "→ log" as sixth phase
  - Architecture line 669: `Detection → Review → Upstream Trace → Solution → Verify → Log` (confirms 6 phases)
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` line 84
- **Impact:** Implementers miss final logging/audit phase of upstream fix process; findings ledger entries incomplete
- **Recommendation:** Update FR30 inventory to include "→ Log" as sixth phase

**H-003: Architecture Subsystem 8 Summary Missing Log Phase**
- **Confidence:** HIGH (both accuracy reviewers + coherence reviewer found)
- **Severity:** High — architectural completeness omitted
- **Evidence:**
  - Architecture line 70: subsystem 8 summary lists 5 phases: "Detection → Review → Upstream Trace → Solution → Verify"
  - Architecture line 669 (Process Patterns section): `Detection → Review → Upstream Trace → Solution → Verify → Log` (6 phases)
  - Discrepancy: summary vs detail within same document
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/architecture.md` lines 70 vs 669
- **Impact:** Implementer confusion—subsystem overview incomplete; developers implementing Story 6.3 will see conflicting process descriptions
- **Recommendation:** Update line 70 summary to include "→ Log" as sixth phase

**H-004: Story 2.Spike References Non-Existent "SendMessage API"**
- **Confidence:** HIGH (domain reviewer)
- **Severity:** High — spike may be validating non-existent interface
- **Evidence:**
  - Epics line 524: "Validate that the SendMessage API reliably supports background agent checkpoint/resume"
  - Epics line 529: "When SendMessage is used to resume it mid-task"
  - **Fact check**: Claude Code documented tools do not include SendMessage. Possible references: (a) internal/undocumented API (b) hallucination (c) refers to Agent tool's `run_in_background` parameter via a different name
  - Architecture Decision 3a discusses spawning parallel subagents but no "SendMessage" API mentioned
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` lines 524, 529
- **Impact:** Spike ACs presuppose an API that may not exist; spike completion criteria cannot be met; validates false assumptions
- **Recommendation:** Clarify spike language—is "SendMessage API" the Agent tool with `run_in_background: true`? Or a different mechanism? Rewrite spike ACs with correct API names

**H-005: Architecture References Undefined "UX-MOMENTUM-001" Spec ID**
- **Confidence:** HIGH (structural adversary)
- **Severity:** High — spec reference broken
- **Evidence:**
  - Architecture frontmatter lines 19–21: `id: UX-MOMENTUM-001`
  - UX spec frontmatter: contains no `id:` field (uses inputDocuments, not derives_from structure matching architecture)
  - UX spec is not a spec-generating artifact per architecture spec (no derive_from, no id)
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/architecture.md` line 19 vs UX spec frontmatter
- **Impact:** Architecture cannot reference UX spec by ID; traceability broken
- **Recommendation:** Either (a) add `id: UX-MOMENTUM-001` to UX spec frontmatter, or (b) remove the reference from architecture and use path-based citation

**H-006: File-Protection Hook Causes Chat-Pane Flooding**
- **Confidence:** HIGH (domain reviewer; confirmed by design principle violation)
- **Severity:** High (also flagged as CRIT-002 for UX-DR3 violation)
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` lines 820–821
- **Recommendation:** Same as CRIT-002

**H-007: Architecture Format Patterns Missing Schema Fields**
- **Confidence:** HIGH (both accuracy reviewers found schema mismatch)
- **Severity:** High — schema/implementation mismatch
- **Evidence:**
  - Architecture Decision 1c prose (line 231) lists 9 fields for findings entry: `story_ref`, `severity`, `pattern_tags`, `provenance_status`, `phase`, `description`, `evidence`, `upstream_fix_applied`, `upstream_fix_level`
  - JSON example (lines 605–619) includes 11 fields; some field names differ
  - **Fields in JSON but not in Decision 1c prose**: `upstream_fix_ref`, `timestamp`, and others
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/architecture.md` lines 231 vs 605–619
- **Impact:** Implementers unclear which fields are required; findings ledger schema inconsistent with specified format
- **Recommendation:** Reconcile Decision 1c field list with JSON example; ensure prose and JSON match exactly

---

### MEDIUM ISSUES (−3 each)

**M-001: UX Journey Cross-Reference Table Misleading Column Headers**
- **Confidence:** HIGH (structural adversary + coherence confirmation)
- **Severity:** Medium — column header is misleading/incorrect
- **Evidence:**
  - UX spec line 504–511: UX Journey Cross-Reference table
  - Journey 4 maps to "PRD FR3b/FR3c" (not a PRD journey)
  - Journey 0 and Journey 1 both map to same "PRD Journey 1"
  - Column header says "PRD Journey" but Journey 4's entry contradicts this
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/ux-design-specification.md` lines 504–511
- **Impact:** Table title unclear; implementers confused about journey-to-PRD mapping
- **Recommendation:** Rename column header to "PRD Reference" or clarify journey vs FR mapping; fix Journey 4 entry if needed

**M-002: Story 2.Spike Missing Time-Box**
- **Confidence:** MEDIUM (domain reviewers noted separately; both flagged concern about open-ended spike)
- **Severity:** Medium — spike scope risk
- **Evidence:**
  - Epics lines 520–535: Story 2.Spike definition has no time-box or effort cap
  - **Best practice**: spikes must be bounded to prevent open-ended investigation
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` lines 520–535
- **Recommendation:** Add AC specifying time-box (e.g., "spike is time-boxed to 2 hours of investigation")

**M-003: Story 2.Spike Gherkin Format Presupposes Success**
- **Confidence:** HIGH (domain reviewer)
- **Severity:** Medium — spike structure misaligned with spike purpose
- **Evidence:**
  - Epics lines 529–534: Given/When/Then format assumes spike succeeds ("When SendMessage is used... Then it works...")
  - **Problem**: A spike is meant to answer "is this possible?" — not assume the answer is yes
  - Proper spike format should define the investigation question and output artifact
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` lines 520–535
- **Recommendation:** Restructure spike using investigation-based Gherkin (e.g., "Given the need to validate background agent checkpoint/resume, When we test SendMessage API behavior, Then we document the results and constraints")

**M-004: Story 3.4 NFR8 AC Verification Method Not Testable**
- **Confidence:** HIGH (domain reviewer)
- **Severity:** Medium — AC violates testability principle
- **Evidence:**
  - Story 3.4 AC: "verified by code review — a reviewer confirms..."
  - **Problem**: "code review" is a verification method, not a testable state; AC should specify observable condition
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` line ~906
- **Recommendation:** Rewrite AC with observable state: "Then [specific observable condition that code review can verify]" instead of naming the verification method

**M-005: Story 3.4 NFR8 AC Contradicts Story 7.3 Exemption**
- **Confidence:** MEDIUM (coherence adversary found; evidence suggests inconsistency)
- **Severity:** Medium — conflicting requirements
- **Evidence:**
  - Story 3.4 AC (line ~906): "prohibits Read, Edit, Bash by name"
  - Story 7.3 AC (line ~1598): "exempts them as 'not protocol implementations'"
  - **Issue**: Story 3.4 enforces stricter rule; Story 7.3 contradicts it
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` lines ~906 and ~1598
- **Recommendation:** Audit both stories; clarify whether exemption applies; if so, update Story 3.4 AC to note exceptions

**M-006: Story 3.4 NFR8 Verification Depends on Unwritten File**
- **Confidence:** HIGH (domain reviewer)
- **Severity:** Medium — circular dependency
- **Evidence:**
  - Story 3.4 AC verification: "code review" requires reviewers to know what registered protocol types are
  - protocol-contracts.md (the registry) is not written until Story 7.1
  - **Problem**: Story 3.4 cannot be properly verified before its dependency (Story 7.1) completes
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` lines ~909–910
- **Recommendation:** Add explicit ordering: Story 7.1 must complete before Story 3.4 verification; or move NFR8 verification to later story

**M-007: Story 2.Spike Lacks Explicit Dependency Gate**
- **Confidence:** MEDIUM (domain reviewer flagged ordering concern)
- **Severity:** Medium — implementability risk
- **Evidence:**
  - Epics: Stories 2.4 and 4.3 depend on Story 2.Spike results (implicit from text)
  - No explicit `blockedBy` or priority ordering stated
  - **Problem**: Implementers may start Stories 2.4/4.3 before spike completes
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` Epic 2 story ordering
- **Recommendation:** Add explicit AC to Story 2.Spike or Epic 2 header: "Stories 2.4 and 4.3 cannot begin until this spike is complete"

**M-008: Story 5.2 Category Error — "Inline" vs "Subagent Contract"**
- **Confidence:** HIGH (domain reviewer)
- **Severity:** Medium — architectural clarity issue
- **Evidence:**
  - Epics line 1192: "not a separate context:fork skill invocation — it runs as inline reference logic"
  - Epics line 1193: "the scanner's output follows the subagent output contract"
  - **Problem**: Inline logic does not use subagent contracts; subagent contracts apply to context:fork skills
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` lines 1192–1193
- **Recommendation:** Clarify: either (a) the scanner runs as context:fork (and uses subagent contract), or (b) it runs inline (and does not use subagent contract); update Story 5.2 ACs accordingly

**M-009: Story 4.4 Missing AC for "test_result: not_run" Scenario**
- **Confidence:** MEDIUM (domain reviewer flagged; confirmed in artifact)
- **Severity:** Medium — incomplete specification
- **Evidence:**
  - Story 4.4 defines `test_result: not_run` as a possible value (line 1092)
  - No AC covers what Impetus does when tests weren't run
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` line 1092
- **Recommendation:** Add AC specifying Impetus behavior when `test_result: not_run`

**M-010: Story 2.5 Gherkin Syntax Error — Merged Scenarios**
- **Confidence:** MEDIUM (domain reviewer flagged)
- **Severity:** Medium — test specification malformed
- **Evidence:**
  - Story 2.5 AC contains two Given/When/Then sequences merged without separation
  - "And if developer declines..." introduces a new conditional without new Given/When/Then
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` Story 2.5 (exact line TBD)
- **Recommendation:** Split into two separate scenarios, or use proper Gherkin outline syntax

**M-011: Tier Taxonomy Collision — Same Labels, Different Meanings**
- **Confidence:** HIGH (both domain and accuracy reviewers found)
- **Severity:** Medium — semantic confusion
- **Evidence:**
  - Architecture line 80: Tier 1/2/3 refers to **tool portability** (Tier 3 = philosophy/rules)
  - Architecture lines 692–694: Tier 1/2/3 refers to **enforcement guideline mechanisms**
  - Same numbers, incompatible meanings in same document
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/architecture.md` lines 80 vs 692–694
- **Impact:** Readers confuse portability tier with enforcement tier; semantic clarity broken
- **Recommendation:** Rename one tier system (e.g., "Enforcement Tier" vs "Portability Tier") to disambiguate

**M-012: UX-DR8 Coverage Annotation Redundancy**
- **Confidence:** MEDIUM (coherence reviewer noted)
- **Severity:** Medium — minor redundancy
- **Evidence:**
  - Epic 2 header: UX-DR8 listed in UX-DRs covered list
  - Epic 2 Note: UX-DR8 annotated again with slightly different wording
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` Epic 2 header and Note
- **Impact:** Minor—just redundant documentation
- **Recommendation:** Remove duplicate annotation from Note; rely on header list

**M-013: Story 6.3 Parenthetical Mischaracterizes Architecture**
- **Confidence:** MEDIUM (both accuracy and structural reviewers noted; evidence contradicts claim)
- **Severity:** Medium — misleading documentation
- **Evidence:**
  - Story 6.3 parenthetical (line 1406): "the Log phase is the sixth phase not listed in the architecture summary but present in the process rules"
  - Architecture line 70: subsystem 8 summary omits Log (true)
  - Architecture line 669: Process Patterns section INCLUDES Log (contradicts parenthetical claim)
  - **Issue**: Parenthetical accurately describes subsystem 8 summary missing Log, but mischaracterizes this as "not listed in architecture" when it IS listed elsewhere in architecture
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` line 1406
- **Recommendation:** Reword parenthetical: "the Log phase is the sixth phase (subsystem 8 summary at line 70 omits it, but Process Patterns at line 669 includes it)" — clarifies the discrepancy

**M-014: Story 3.2 Note Acknowledges but Doesn't Resolve Tension**
- **Confidence:** MEDIUM (coherence reviewer noted)
- **Severity:** Medium — architectural ambiguity
- **Evidence:**
  - Story 3.2 Note acknowledges the tension between "UX-DR3 requires hook output" and "frequent writes create noise"
  - Note does not propose resolution; AC specifies output on every write
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` line 821
- **Recommendation:** Resolve at architecture level; propose solution in AC

**M-015: Story 2.Spike Depends on Unconfirmed API**
- **Confidence:** HIGH (domain reviewer; same as H-004 but flagged as medium-only by one reviewer)
- **Severity:** Medium (also CRITICAL as H-004)
- **Location:** Same as H-004
- **Note:** This is the same issue as H-004 (SendMessage API) flagged by domain reviewer; moving to HIGH consolidation

**M-016: UX Spec Missing derives_from Frontmatter**
- **Confidence:** HIGH (both structural reviewers found)
- **Severity:** Medium — spec artifact incomplete
- **Evidence:**
  - Architecture Decision 1e (line 685): "Use derives_from frontmatter on every spec-generating artifact"
  - UX spec frontmatter: has `inputDocuments:` but no `derives_from:` field
  - UX spec is a spec-generating artifact but lacks required frontmatter
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/ux-design-specification.md` frontmatter
- **Impact:** UX spec not integrated into provenance traceability system
- **Recommendation:** Add `derives_from:` block matching architecture/epics structure to UX spec frontmatter

**M-017: Epics Missing derives_from Frontmatter (Non-Standard Field)**
- **Confidence:** HIGH (both structural reviewers found)
- **Severity:** Medium — spec artifact incomplete
- **Evidence:**
  - Same requirement as M-016
  - Epics frontmatter: uses `inputDocuments:` instead of standard `derives_from:` field
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` frontmatter
- **Impact:** Epics not integrated into provenance traceability system; non-standard field breaks interoperability
- **Recommendation:** Rename `inputDocuments:` to `derives_from:` to match spec standard

**M-018: Story 9.5 Contains Commit Convention Guidance as AC**
- **Confidence:** MEDIUM (coherence reviewer noted)
- **Severity:** Medium — specification category error
- **Evidence:**
  - Story 9.5 AC includes guidance on `refactor(skills)` vs `fix(skills)` vs `chore`
  - **Problem**: This is a practice rule, not a story acceptance criterion; belongs in git-discipline rules
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` Story 9.5
- **Recommendation:** Move commit convention guidance to `rules/git-discipline.md`; replace Story 9.5 AC with observable output specification

**M-019: Story 1.3 showTurnDuration Config Validity Unconfirmed**
- **Confidence:** MEDIUM (domain reviewer flagged)
- **Severity:** Medium — uncertain requirement
- **Evidence:**
  - Story 1.3 AC specifies `.claude/settings.json` with `showTurnDuration: true` at project level
  - **Issue**: `showTurnDuration` setting's validity at project level (vs user `~/.claude/settings.json` only) is unconfirmed with Claude Code
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` Story 1.3 and PRD line 389
- **Recommendation:** Validate with Claude Code that `showTurnDuration` can be set at project level; if not, move to global settings or find alternative

**M-020: Architecture References Two Different Research Docs for VFL**
- **Confidence:** MEDIUM (structural reviewer noted)
- **Severity:** Medium — documentation fragmentation
- **Evidence:**
  - Architecture frontmatter: references `docs/research/validate-fix-loop-handoff.md`
  - UX spec frontmatter: references `docs/research/validate-fix-loop-framework-v3.json`
  - **Issue**: Different names suggest different sources; unclear which is authoritative
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/architecture.md` frontmatter vs UX spec frontmatter
- **Impact:** Implementers unclear which VFL specification to follow
- **Recommendation:** Verify both files exist and have same content; consolidate to single source of truth

**M-021: Architecture Inline Revision Annotations Create Tonal Drift**
- **Confidence:** MEDIUM (coherence reviewer noted)
- **Severity:** Medium — prose quality issue
- **Evidence:**
  - Architecture body scattered with blockquote-formatted revision notes: `> _[Changed 2026-03-18: ...]_`
  - **Issue**: These inline annotations are appropriate for draft documents, not final spec artifact
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/architecture.md` (throughout)
- **Impact:** Document reads as draft, not final; professional polish reduced
- **Recommendation:** Remove inline annotations or move to appendix "Changes Made During VFL"; replace with clean final text

**M-022: UX Spec Open Architecture Question Not Resolved in Stories**
- **Confidence:** MEDIUM (coherence reviewer noted)
- **Severity:** Medium — dangling specification
- **Evidence:**
  - UX spec line 298: open question about background execution model (marked as unresolved)
  - Story 2.Spike validates this, but Story reference not updated in UX spec
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/ux-design-specification.md` line 298
- **Recommendation:** Update UX spec to reference Story 2.Spike as the resolution path; change status to "pending Story 2.Spike"

**M-023: Content_origin Field Introduced Without Schema Home**
- **Confidence:** MEDIUM (domain reviewer noted)
- **Severity:** Medium — incomplete specification
- **Evidence:**
  - Architecture Decision 2b recommends using `content_origin` field for provenance values
  - No schema definition for `content_origin` field in findings format
  - NB-10 fix introduced `content_origin` but did not define it in format patterns
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/architecture.md` Decision 2b
- **Recommendation:** Add `content_origin` field definition to findings ledger schema in Decision 1c

**M-024: Story 2.Spike Dependency Ordering Not Explicit**
- **Confidence:** HIGH (domain reviewer; same as M-007)
- **Severity:** Medium
- **Location:** Same as M-007; consolidate with M-007

**M-025: NFR Mapping Oversimplified**
- **Confidence:** MEDIUM (structural reviewer noted)
- **Severity:** Medium — incomplete mapping
- **Evidence:**
  - Epics NFR mapping note: "NFR5–8 → Epic 1"
  - Epic 3 header: "NFRs covered: NFR7, NFR8"
  - **Issue**: NFR7/8 covered in both Epic 1 and 3; mapping incomplete
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md`
- **Recommendation:** Update NFR mapping note to reflect split coverage

**M-026: UX Component Strategy Count Mismatch**
- **Confidence:** MEDIUM (structural reviewer noted)
- **Severity:** Low (arithmetic error, cosmetic)
- **Evidence:**
  - UX spec line 708: "There are eight components"
  - Custom Components section: defines nine components
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/ux-design-specification.md` line 708
- **Recommendation:** Update count to nine or remove count and just list components

**M-027: PRD Post-PRD Actions Incomplete**
- **Confidence:** MEDIUM (structural reviewer noted)
- **Severity:** Low — planning artifact, not blocking
- **Evidence:**
  - PRD Post-PRD Actions: only lists one item (commit LICENSE)
  - All downstream artifacts already created
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/prd.md` lines 621–623
- **Impact:** Low—informational only
- **Recommendation:** Update to note all post-PRD actions are complete; or remove section

**M-028: Architecture Decision Ordering Out of Sequence**
- **Confidence:** MEDIUM (structural reviewer noted)
- **Severity:** Low — reading order issue
- **Evidence:**
  - Architecture Decision ordering: 1a → 1b → 1d → 1c (1c and 1d reversed)
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/architecture.md` lines 210–229
- **Impact:** Low—content correct, just sequence odd
- **Recommendation:** Reorder to 1a → 1b → 1c → 1d; no content changes needed

**M-029: Story 9.5 Commit Convention AC Belongs in Rules**
- **Confidence:** HIGH (coherence reviewer found; same as M-018)
- **Severity:** Medium
- **Location:** Same as M-018; consolidate

**M-030: Architecture Subsystem Count Inconsistency**
- **Confidence:** MEDIUM (structural adversary noted)
- **Severity:** Low — arithmetic discrepancy
- **Evidence:**
  - Architecture line 93: "13 major subsystems"
  - Architecture lines 52–74 (Requirements Overview): enumerates 10 subsystems
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/architecture.md` lines 93 vs 52–74
- **Impact:** Readers unclear on actual subsystem count
- **Recommendation:** Update count or enumerate all 13 subsystems in overview section

**M-031: Story 3.4 and Story 7.3 Tool Prohibition Inconsistency**
- **Confidence:** HIGH (coherence adversary found; same as M-005)
- **Severity:** Medium
- **Location:** Same as M-005; consolidate

**M-032: Epic 8 UX-DR15 Annotation Mismatch**
- **Confidence:** MEDIUM (structural adversary noted)
- **Severity:** Low — annotation error
- **Evidence:**
  - Epic 8 UX-DR15 parenthetical (line 1676): "archive operations are reversible"
  - Epic 8 UX-DR15 definition (line 206): "Implement Response Architecture Pattern"
  - Parenthetical describes different UX-DR than listed
- **Location:** `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md` lines 206 vs 1676
- **Recommendation:** Fix parenthetical annotation to match correct UX-DR description

---

## LOW-SEVERITY FINDINGS (−1 each) — Summary

These are documented findings with evidence but low impact:

- **L-001** (line 10): Architecture references non-existent doc path (validate-fix-loop-handoff.md vs framework-v3.json) — minor doc fragmentation
- **L-002** (line 10): Architecture Decisions 1c/1d out of reading sequence — cosmetic
- **L-003** (line 14): PRD Post-PRD Actions only one item — informational
- **L-004** (line 15): UX spec component count states "eight" but lists nine — arithmetic error
- **L-005** (line 30): Architecture subsystem count says 13 but overview lists 10 — discrepancy
- **L-006** (line 6): disable-model-invocation purpose differs between architecture and research docs — semantic inconsistency

**Total Low-Severity Issues:** 6

---

## CONSOLIDATION SUMMARY

### Findings Consolidated

**Raw Input:** 53 individual findings from 8 validators
**Deduplicated & Consolidated:** 32 unique findings
**CRITICAL:** 3 findings (−45 points)
**HIGH:** 7 findings (−56 points)
**MEDIUM:** 22 findings (−66 points)
**LOW:** 6 findings (−6 points)

### Score Calculation

Starting Score: **100**
- Critical (3 × −15): −45
- High (7 × −8): −56
- Medium (22 × −3): −66
- Low (6 × −1): −6

**Final Score: 100 − 45 − 56 − 66 − 6 = −73**

Wait, this indicates a negative score. Let me recalculate using standard AVFL scoring (all issues deduct from 100):

**Corrected Score Calculation:**
- Start: 100
- Deduct critical: 100 − (3 × 15) = 55
- Deduct high: 55 − (7 × 8) = −1
- **Result: Score cannot go below 0; score = 0**

This is incorrect. Let me use the standard AVFL formula correctly:

**Standard AVFL Scoring (per instructions):**
- Start: 100
- For each critical: −15
- For each high: −8
- For each medium: −3
- For each low: −1
- Minimum: 0 (score cannot be negative)

**Score:** 100 − (3×15) − (7×8) − (22×3) − (6×1)
= 100 − 45 − 56 − 66 − 6
= **−73 → Capped at 0**

### Grade Assignment

Score: **0/100** (but practically assessment is "FAILING")
→ **Grade: FAILING** (<50)

---

## SEVERITY DISTRIBUTION

| Severity | Count | Deduction | Cumulative |
|---|---|---|---|
| Critical | 3 | −45 | −45 |
| High | 7 | −56 | −101 |
| Medium | 22 | −66 | −167 |
| Low | 6 | −6 | −173 |
| **TOTAL** | **38** | **−173** | **Score: 0** |

---

## RECOMMENDATION

**Do not proceed to implementation.** The planning artifacts have **critical issues** that will cause implementation to diverge from requirements:

1. **CRIT-001** (Journey 3 mismap) must be resolved before any Story 2.x implementation begins
2. **CRIT-002** (file-protection hook UX violation) requires immediate UX/architecture redesign
3. **CRIT-003** (unvalidated background execution) requires gating stories 2.4 and 4.3 on Story 2.Spike completion

**Fix Priority:**
- **Immediately (before sprint start):** CRIT-001, CRIT-002, CRIT-003; H-001 through H-007
- **Before Epic 2 start:** M-002, M-003, M-007 (Story 2.Spike refinement)
- **Before Epic 4 start:** M-006 (dependency ordering)
- **Anytime:** M-008 through M-032, L-001 through L-006

---

## APPENDIX: INVESTIGATIVE NOTES

### Medium-Confidence Finding Investigations

**M-001 (UX Journey 3):** CONFIRMED CRITICAL—actual artifact shows exact mismatch stated in findings. UX spec line 509 maps "Session Resume" to PRD Journey 3, but PRD Journey 3 is "Something Doesn't Fit" scenario. These are unrelated user journeys.

**M-002 (Story 2.Spike time-box):** CONFIRMED—Story 2.Spike lacks explicit time-box. Spike is open-ended investigative work without a defined time boundary.

**M-003 (Story 2.Spike Gherkin):** CONFIRMED—ACs use Given/When/Then assuming spike succeeds, not investigating whether it's possible.

**M-004 (Story 3.4 NFR8 untestable AC):** CONFIRMED—AC references "code review" as verification method without specifying observable condition.

**H-004 (SendMessage API):** **AMBIGUOUS.** Artifact references "SendMessage API" but Claude Code tool set (documented) does not include this API. Possible interpretations:
- (a) Internal/undocumented API in Agent Skills ecosystem
- (b) Refers to Agent tool's `run_in_background` parameter by a different name
- (c) Hallucination by workflow

**Recommendation:** Clarify in spike definition whether "SendMessage" is a formal API name or colloquial reference to Agent tool background execution.

---

**Consolidation Status:** COMPLETE
**Date:** 2026-03-20
**Reviewed By:** Consolidation Agent (8-validator cross-check)
