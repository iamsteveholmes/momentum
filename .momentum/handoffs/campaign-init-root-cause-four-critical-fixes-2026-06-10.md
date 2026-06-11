# Handoff: Four Critical Process Fixes from the nornspun campaign-init Sprint Root-Cause (2026-06-10)

**From:** nornspun session (conduct-by-hand of sprint-2026-05-30, root-cause analysis)
**To:** momentum agent
**Ask:** Capture these four critical-priority backlog stories into the momentum practice
(enrich via create-story when ready, sequence as you see fit). The intake stubs, index
entries (priority: critical), practice-ledger events, and beads are already committed —
this handoff carries the full incident context so nothing depends on the nornspun session.

---

## The incident (all evidence inline)

nornspun's sprint-2026-05-30 (campaign-init iteration 2, 15 stories, 5 waves) was built by
hand-running the conduct engine from a runbook. All 15 stories passed per-story QA and
merged to the sprint branches. The Phase-4 **live** walkthrough (first time the app-ui code
was ever compiled and launched) then found the headline feature functionally broken:

- The campaign-init **conversation is 100% client-local hardcoded copy**.
  `CampaignInitViewModel.kt` (client commonMain) has exactly three imports — all
  StateFlow, zero networking. Every Urd line in the flow (threshold opener, system-choice
  sentence, Frame-3 preface/items/closing) is a `const val`. The only backend call in the
  whole flow is a fire-and-forget `POST /api/campaigns`.
- The code's own comment: *"The backend delivers the active-register version; these
  constants are the hearth-register fallback used when backend payload is unavailable."*
  The "backend payload" never existed. The fallback is the only path.
- Consequence: the sprint's entire backend prompt work (voice register, offered-list copy,
  bold readback) is unreachable by the client. The sprint looked done and didn't work.

## Root cause — three stacked failures, each mapping to one story

**1. The QA leg never executed the declared verification method.**
The story specs declared `verification_method: smoke` and cited nornspun's ASR-004
verbatim — *"the acceptance signal is live on-device/desktop observation, not scenario
pass counts"* (ASR-004: 57/71 scenarios "passed" while the live flow did nothing). The
conduct build phase's QA was diff-inspection against the frozen contract text; it verified
the hardcoded copy matched spec (it did, verbatim) and passed it. Routing existed;
execution didn't.
→ **`conduct-qa-execute-verification-method`** (epic: momentum-sprint-orchestration,
defect): the conduct QA stage must route on the frozen contract's Part-A
`verification_method`/`harness_profile` and EXECUTE it — smoke = build + launch + drive
live; environment-impossible → BLOCKED verdict naming the prerequisite; a guard rejects
diff-only evidence for executable-method stories. Applies to the conductor skill's build
phase and the qa-reviewer agent contract.

**2. A depends_on edge consumed a deliverable its producer never produced — and no gate
could see it.**
Client story `campaign-init-offered-suggestion-list-render-and-routes` instructed *"source
the copy from the backend payload... not a hardcoded client string"*, with
`depends_on: backend-campaign-init-add-offered-suggestion-list-copy`. That backend story
only edited the Urd **system prompt** — no payload, no endpoint, no schema. Each story
individually passed its gates (create-story's AVFL checkpoint validates a story against
its *own epic record* — single story, single direction); the incoherence existed only
*between* stories. The sprint contained two contradictory architectures: backend stories
assumed the conversation flows through Urd chat; client stories assumed client-local
rendering; no story owned the seam.
→ **`sprint-planning-cross-story-coherence-gate`** (epic:
momentum-sprint-planning-to-ready, feature): at contract-freeze, when the full story set
is visible, enumerate every depends_on edge and assert the consumer's named external
inputs map to concrete deliverables in the producer's contract; unmatched edges block
activation or force an explicit wiring story.
→ **`create-story-dependency-deliverable-check`** (epic:
momentum-sprint-planning-to-ready, feature): the per-story half. create-story Step 7
currently only *extracts* depends_on slugs from the epic record; add a step that resolves
every externally-sourced input named in ACs/tasks against existing contracts or the
dependency's ACs, and on failure blocks ready-for-dev or injects a loud
`UNRESOLVED INPUT — architecture gap` marker.

**3. The dev agent silently fabricated instead of blocking.**
Faced with an AC naming a non-existent input, the dev wrote plausible fallback constants
labeled "until the endpoint is live" — no TODO escalation, no BLOCKED signal. The
unimplementable AC was *information* (the spec/dependency graph was wrong) and it was
swallowed.
→ **`dev-block-on-missing-dependency-contract`** (epic: momentum-agent-role-contracts,
feature): binding rule in momentum:dev + specialists + the bmad-dev-story delegation path:
a required input/endpoint/payload/signal that cannot be located → STOP, mark story
blocked, name the missing artifact and responsible dependency. Fallback content only when
the AC itself specifies fallback behavior. Include an eval demonstrating the block.

## Relationships and sequencing notes

- The three gates are defense-in-depth at three altitudes: sprint-planning (whole-set,
  primary), create-story (per-story, catches pre-sprint stories), dev contract (last
  line). They are independent — no hard ordering — but the conductor smoke fix is the one
  that would have caught this incident even with all upstream gates missed, and the next
  nornspun conduct run (consolidation sprint, BLOCKER priority) wants it soonest.
- nornspun carries a local sibling for its hand-run workflow:
  `conduct-round-build-smoke-qa-leg` (nornspun repo, `.momentum/conduct/workflows/
  nornspun-round-build.wf.js` + RUNBOOK.md). Upstreaming the conductor fix does not close
  that story; the local runbook is what nornspun actually runs until conduct ships.
- Five conductor seam-fix stories from the same live run already exist in this backlog
  (state persistence, coverage deferral, commit authority, QA normalization adapter,
  worktree creation — commit c5da23b). The QA normalization adapter story is adjacent to
  fix #1 but does NOT cover method execution — don't merge them without checking.

## Evidence pointers (nornspun repo, branch sprint/sprint-2026-05-30)

- `.momentum/conduct/build-ledger.json` — `phase4_live.wiring_6_conclusive` (the
  conclusive live finding), `held_for_endgate` items #6/#7/#2, AVFL NON_CONVERGENT record.
- `.momentum/stories/campaign-init-offered-suggestion-list-render-and-routes.md` — the
  "source from backend payload" AC + broken depends_on.
- `.momentum/stories/campaign-init-threshold-opening-message-and-system-choice-links.md`
  — spec-mandated client constant + the ASR-004 smoke-verification language QA skipped.
- nornspun-client `shared/src/commonMain/kotlin/com/nornspun/ui/viewmodel/
  CampaignInitViewModel.kt` (sprint branch) — the hardcoded constants + "fallback" comment.

## Already done (do not redo)

- 4 stub files in `.momentum/stories/` (this repo), index entries at priority
  `critical`, practice-ledger `created` events, beads with discovered-from edges
  (map updated in `.momentum/beads-id-map.json`). Committed on main.
- nornspun-side intake committed in the nornspun repo.
