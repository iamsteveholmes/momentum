---
id: DEC-004
title: Feature Schema Value-First Redesign — value_analysis and system_context Required Fields
date: '2026-04-11'
status: decided
source_assessment: AES-002
decisions_produced:
  - stories: [feature-grooming]
---

# DEC-004: Feature Schema Value-First Redesign

## Decision

The `features.json` schema adds two required fields: **`value_analysis`** and
**`system_context`**. These fields are required for all new features written by the
`feature-grooming` skill and for all features updated at refine time. Existing features
without these fields are flagged as incomplete.

---

## Rationale

AES-002 identified that the current features.json schema captures structural information
(what a feature is, what stories drive it, what acceptance condition verifies it) but
does not capture the most important information: what value it delivers to users, what
the current state of that value delivery is, and how it enhances the overall product.

Features are the unit of value delivery. A feature without a value analysis is not a
feature — it is a label. And without honest value analysis, the practice will continue
to complete sprints and advance stories without delivering anything users can use.

---

## Schema Contract

### value_analysis (required, multi-paragraph string)

What value does this feature deliver — currently and at full vision?

**Coverage requirements:**
1. **Current state**: what value is being delivered right now, honestly assessed
2. **Full vision**: what the feature aspires to deliver, including capabilities the user
   did not previously know they could have (not just pain removal)
3. **Gaps**: what is missing between current state and full vision

**Standards:**
- Minimum one substantive paragraph (not a sentence)
- Must cover the full value spectrum: pain removal, new capabilities, knowledge, experience
- Must not reduce to pain removal only — new capabilities and experiential dimensions
  are explicitly considered
- Status of "working" requires evidence of actual user value, not just story completion

### system_context (required, string)

How does this feature fit the overall product? How does its value enhance or interact
with the whole? What becomes possible or impossible without it?

**Standards:**
- Minimum one clear sentence, typically a short paragraph
- Must address how this feature relates to at least one other feature
- Must answer: "what does the rest of the product depend on from this feature?"

---

## Value Philosophy

Formalizing the developer insight from 2026-04-11:

1. **Value is a spectrum, not a binary.** A feature can be partially delivering value
   and still have a clear path to delivering more. The question is not "does it deliver
   value?" but "how much does it currently deliver, and what is the path to delivering more?"

2. **Value goes beyond pain removal.** New capabilities the user didn't know they wanted,
   knowledge that elevates their judgment, experiences that make their work richer — these
   are all valid value dimensions alongside pain removal.

3. **Simplicity as value.** A feature that is too hard to use, duplicates another, or
   confuses the developer may deliver negative value. Consolidation or removal can be the
   highest-value action.

4. **Honest status.** A feature with status "working" that has 0 users is not working.
   Status must reflect actual value delivery.

---

## Applies To

- **Feature-grooming skill (bootstrap mode):** must populate value_analysis and
  system_context for every proposed feature; must create foundation docs (assessment +
  decision) before writing features.json
- **Feature-grooming skill (refine mode):** must flag existing features without these
  fields as incomplete; must evaluate whether value_analysis is honest about current
  delivery vs. full vision
- **All future features.json writes:** value_analysis and system_context are required;
  a feature without them fails schema validation
- **Existing Nornspun features:** must be retrofitted at next feature-grooming run
- **Existing Momentum features:** must be retrofitted at next feature-grooming run (this
  session constitutes the first grooming run — new fields are populated in this session)

---

## Relationship to Architecture Decisions

Architecture decisions 44-48 (feature-artifact-schema, feature-status-skill, etc.)
captured the structural schema. This decision extends the schema with the value layer.
Architecture decisions should be updated to reference these new required fields.

---

## Stories Produced

| Story | Purpose |
|-------|---------|
| feature-grooming | Skill that implements value-first feature discovery, analysis, and writing |
