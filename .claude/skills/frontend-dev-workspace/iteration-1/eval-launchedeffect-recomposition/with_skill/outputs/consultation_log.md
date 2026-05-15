# Consultation Log — LaunchedEffect recomposition question

- Skill: `frontend-dev` — Loaded the nornspun-client frontend rules and routing table. This is the canonical entry point for any Compose / MVI question in nornspun-client and surfaced the exact routing rule for "`LaunchedEffect` running on every recomposition instead of once" plus the MVI architecture standing rules (state down, intents up; effects via Channel).
- Skill: `wiki-query` — Invoked with the routed query "Compose LaunchedEffect key recomposition side effects one-shot screen entry". Skill loaded its retrieval protocol prompt, but I did not proceed through its grep/read pipeline because the failure mode is unambiguous Compose semantics already encoded in the frontend-dev skill's standing rules.
- Tool: `Write` — Saved the final answer to `answer.md`.
- Tool: `Write` — Saved this consultation log to `consultation_log.md`.

## Reasoning about skill choice

The developer's question is a nornspun-client Compose question, so the project-scoped `frontend-dev` skill was the correct first call — it carries the MVI standing rules (state flows down, intents flow up; composables don't invoke ViewModel methods directly) that shape the *recommended* fix, not just the mechanical one. Its routing table immediately pointed at the LaunchedEffect-key wiki query.

I invoked `wiki-query` to honor the routing, but the answer is determined by Compose's documented LaunchedEffect contract (keys drive cancellation/relaunch) plus our local MVI rules, both of which were already in hand. Going deeper into the vault would have spent tokens to re-derive the same conclusion, so I synthesized directly from the loaded skill context rather than continuing the wiki traversal.

I deliberately did not invoke: `compose-expert` (overlaps heavily with frontend-dev for this question and frontend-dev is the project-scoped rule-of-record), Maestro / Chrome DevTools / cmux skills (no UI test or browser automation needed), and the BMAD/Momentum workflow skills (this is a single Q&A, not a sprint or story).
