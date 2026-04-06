# Backlog Add Command — Lightweight Story Stub Creation with Design Intent

Status: backlog
Epic: impetus-core

## What This Is

A `/momentum:backlog-add` command that captures design intent when adding stories to the backlog during conversations. It creates an index entry + a descriptive stub file — heavier than a bare 3-line stub, lighter than a full `momentum:create-story` output.

## Why It Matters

Currently there are only two modes: bare stubs (title/status/epic — useless for context) and full create-story output (ACs, tasks, dev notes, implementation guide, AVFL — heavyweight). When ideas emerge during sprint planning, retros, or casual conversations, the context gets lost because the stub captures nothing and create-story is too much ceremony for a backlog item.

## What the Stub Should Capture

- **Description:** What the work is about and why it matters (1-2 paragraphs)
- **Design decisions:** Key decisions already made during the conversation
- **Rough scope:** What's in, what's out, approximate size
- **Context references:** Links to decisions, conversations, or docs that informed it

## What the Stub Should NOT Include

- Formal acceptance criteria (added later by create-story during sprint planning)
- Task breakdowns (added later)
- Dev notes with file paths and patterns (added later)
- Implementation guide (injected by create-story)
- AVFL validation (runs during sprint planning)

## How It Would Work

1. Developer says `/momentum:backlog-add` or Impetus offers it during conversation
2. Skill captures: title, epic, description, design context, rough touches
3. Creates index entry (status: backlog, story_file: true)
4. Creates stub file with the descriptive template
5. No AVFL, no formal ACs, no implementation guide

When the story later gets picked into a sprint, `momentum:create-story` runs on top of it — reading the existing description and enriching it with ACs, tasks, dev notes, and implementation guidance.
