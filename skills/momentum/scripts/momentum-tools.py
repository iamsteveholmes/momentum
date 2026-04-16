#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""
momentum-tools — Deterministic CLI for Momentum sprint and story operations.

Sole writer of stories/index.json and sprints/index.json.
All operations are deterministic state machine validations + JSON mutations.

Usage:
    momentum-tools.py sprint status-transition --story SLUG --target STATUS [--force]
    momentum-tools.py sprint activate
    momentum-tools.py sprint complete
    momentum-tools.py sprint epic-membership --story SLUG --epic SLUG
    momentum-tools.py sprint plan --operation add|remove --stories SLUG[,SLUG,...] [--wave N]
    momentum-tools.py sprint story-add --slug SLUG --title TITLE --epic EPIC [--priority PRIORITY]
    momentum-tools.py specialist-classify --touches "path1,path2,..."
    momentum-tools.py quickfix register --slug SLUG --story STORY_KEY
    momentum-tools.py quickfix complete --slug SLUG
    momentum-tools.py intake-queue append --source SOURCE --kind KIND --title TITLE [--description DESC] [--sprint-slug SLUG] [--feature-slug SLUG] [--story-type TYPE] [--feature-state-transition JSON] [--failure-diagnosis JSON]
    momentum-tools.py intake-queue list [--source SOURCE] [--kind KIND] [--status STATUS]
    momentum-tools.py intake-queue consume --id ID [--outcome-ref REF]
    momentum-tools.py version check
"""

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

# --- State Machine ---

ORDERED_STATES = ["backlog", "ready-for-dev", "in-progress", "review", "verify", "done"]
TERMINAL_STATES = {"done", "dropped", "closed-incomplete"}
ALL_STATES = set(ORDERED_STATES) | TERMINAL_STATES


def validate_transition(current: str, target: str, force: bool = False) -> str | None:
    """Return error message if transition is invalid, None if valid."""
    if force:
        return None
    if target not in ALL_STATES:
        return f"Unknown target state: {target}"
    if current in TERMINAL_STATES:
        return f"Cannot transition from terminal state '{current}' without --force"
    if target in {"dropped", "closed-incomplete"}:
        return None  # always valid from non-terminal
    if current not in ORDERED_STATES:
        return f"Unknown current state: {current}"
    if target not in ORDERED_STATES:
        return f"Unknown target state: {target}"
    current_idx = ORDERED_STATES.index(current)
    target_idx = ORDERED_STATES.index(target)
    if target_idx != current_idx + 1:
        direction = "backward" if target_idx < current_idx else "non-adjacent forward"
        return f"Invalid {direction} transition: {current} -> {target}. Use --force to override"
    return None


# --- File I/O ---

def resolve_project_dir() -> Path:
    """Resolve project root from env or git."""
    import os
    env_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_dir:
        return Path(env_dir)
    # Walk up to find .git
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / ".git").exists():
            return parent
    print("Error: Cannot determine project root. Set CLAUDE_PROJECT_DIR or run from a git repo.", file=sys.stderr)
    sys.exit(1)


def stories_path(project_dir: Path) -> Path:
    return project_dir / "_bmad-output" / "implementation-artifacts" / "stories" / "index.json"


def sprints_path(project_dir: Path) -> Path:
    return project_dir / "_bmad-output" / "implementation-artifacts" / "sprints" / "index.json"


def read_json(path: Path) -> dict:
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def result(action: str, success: bool, **kwargs) -> None:
    """Print JSON result and exit."""
    output = {"action": action, "success": success, **kwargs}
    print(json.dumps(output, indent=2))
    sys.exit(0 if success else 1)


def error_result(action: str, message: str, **kwargs) -> None:
    """Print error JSON result and exit with code 1."""
    result(action, success=False, error=message, **kwargs)


# --- Sprint Commands ---

def cmd_status_transition(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = stories_path(project_dir)
    stories = read_json(path)

    slug = args.story
    if slug not in stories:
        error_result("status_transition", f"Story '{slug}' not found in stories/index.json", story=slug)

    current = stories[slug]["status"]
    target = args.target
    err = validate_transition(current, target, args.force)
    if err:
        error_result("status_transition", err, story=slug, current=current, target=target)

    stories[slug]["status"] = target
    ensure_priority(stories[slug])
    write_json(path, stories)
    result("status_transition", success=True, story=slug, **{"from": current, "to": target})


def cmd_sprint_activate(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    if not sprints.get("planning"):
        error_result("sprint_activate", "No planning sprint exists to activate")
    if sprints.get("active"):
        error_result("sprint_activate", "An active sprint already exists. Complete it first.")

    planning = sprints["planning"]
    planning["locked"] = True
    planning["started"] = date.today().isoformat()
    planning["status"] = "active"
    sprints["active"] = planning
    sprints["planning"] = None
    write_json(path, sprints)

    slug = planning.get("slug", "unknown")
    result("sprint_activate", success=True, sprint=slug, started=planning["started"])


def cmd_sprint_complete(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    if not sprints.get("active"):
        error_result("sprint_complete", "No active sprint to complete")

    active = sprints["active"]
    active["completed"] = date.today().isoformat()
    active["status"] = "done"
    active["retro_run_at"] = None
    if "completed" not in sprints:
        sprints["completed"] = []
    sprints["completed"].append(active)
    sprints["active"] = None
    write_json(path, sprints)

    slug = active.get("slug", "unknown")
    result("sprint_complete", success=True, sprint=slug, completed=active["completed"])


def cmd_epic_membership(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = stories_path(project_dir)
    stories = read_json(path)

    slug = args.story
    if slug not in stories:
        error_result("epic_membership", f"Story '{slug}' not found", story=slug)

    old_epic = stories[slug].get("epic_slug", "")
    stories[slug]["epic_slug"] = args.epic
    ensure_priority(stories[slug])
    write_json(path, stories)
    result("epic_membership", success=True, story=slug, from_epic=old_epic, to_epic=args.epic)


def cmd_sprint_plan(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    # Create planning entry if it doesn't exist
    if not sprints.get("planning"):
        sprints["planning"] = {"locked": False, "status": "planning", "stories": [], "waves": []}

    planning = sprints["planning"]
    if planning.get("locked"):
        error_result("sprint_plan", "Cannot modify a locked sprint")

    story_slugs = [s.strip() for s in args.stories.split(",")]

    if args.operation == "add":
        existing = set(planning.get("stories", []))
        for slug in story_slugs:
            if slug not in existing:
                planning.setdefault("stories", []).append(slug)
        if args.wave is not None:
            waves = planning.setdefault("waves", [])
            # Find or create wave
            wave_entry = None
            for w in waves:
                if w.get("wave") == args.wave:
                    wave_entry = w
                    break
            if not wave_entry:
                wave_entry = {"wave": args.wave, "stories": []}
                waves.append(wave_entry)
                waves.sort(key=lambda w: w["wave"])
            existing_wave = set(wave_entry.get("stories", []))
            for slug in story_slugs:
                if slug not in existing_wave:
                    wave_entry["stories"].append(slug)

    elif args.operation == "remove":
        planning["stories"] = [s for s in planning.get("stories", []) if s not in story_slugs]
        for wave in planning.get("waves", []):
            wave["stories"] = [s for s in wave.get("stories", []) if s not in story_slugs]
        # Remove empty waves
        planning["waves"] = [w for w in planning.get("waves", []) if w.get("stories")]

    write_json(path, sprints)
    result("sprint_plan", success=True, operation=args.operation, stories=story_slugs)


def cmd_sprint_ready(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    if not sprints.get("planning"):
        error_result("sprint_ready", "No planning sprint exists")

    sprints["planning"]["status"] = "ready"
    write_json(path, sprints)

    slug = sprints["planning"].get("slug", "unknown")
    result("sprint_ready", success=True, sprint=slug, status="ready")


def cmd_sprint_retro_complete(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    completed = sprints.get("completed", [])
    target = None
    for entry in reversed(completed):
        if entry.get("retro_run_at") is None:
            target = entry
            break

    if target is None:
        error_result("sprint_retro_complete", "No completed sprint with retro_run_at unset")

    target["retro_run_at"] = date.today().isoformat()

    auto_activated = False
    planning = sprints.get("planning")
    if planning and planning.get("status") == "ready":
        planning["locked"] = True
        planning["started"] = date.today().isoformat()
        planning["status"] = "active"
        sprints["active"] = planning
        sprints["planning"] = None
        auto_activated = True

    write_json(path, sprints)

    slug = target.get("slug", "unknown")
    result("sprint_retro_complete", success=True, sprint=slug,
           retro_run_at=target["retro_run_at"], auto_activated=auto_activated)


PRIORITY_LEVELS = ["critical", "high", "medium", "low"]
PRIORITY_ORDER = {p: i for i, p in enumerate(PRIORITY_LEVELS)}


def ensure_priority(story: dict) -> dict:
    """Return story with 'priority' field, defaulting to 'low' if absent."""
    if "priority" not in story:
        story["priority"] = "low"
    return story


def cmd_sprint_migrate_priority(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = stories_path(project_dir)
    stories = read_json(path)

    migrated = []
    for slug, story in stories.items():
        if "priority" not in story:
            story["priority"] = "low"
            migrated.append(slug)

    write_json(path, stories)
    result("migrate_priority", success=True, migrated=migrated, total=len(stories))


def cmd_sprint_set_priority(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = stories_path(project_dir)
    stories = read_json(path)

    slug = args.story
    if slug not in stories:
        error_result("set_priority", f"Story '{slug}' not found in stories/index.json", story=slug)

    priority = args.priority
    if priority not in PRIORITY_LEVELS:
        error_result("set_priority",
                     f"Invalid priority: '{priority}'. Must be one of: {', '.join(PRIORITY_LEVELS)}",
                     story=slug, priority=priority)

    old_priority = stories[slug].get("priority", "low")
    stories[slug]["priority"] = priority
    write_json(path, stories)
    result("set_priority", success=True, story=slug, old_priority=old_priority, new_priority=priority)


def cmd_sprint_stories(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = stories_path(project_dir)
    stories = read_json(path)

    priority_filter = args.priority

    if priority_filter == "all":
        groups: dict[str, list] = {p: [] for p in PRIORITY_LEVELS}
        for slug, story in stories.items():
            p = story.get("priority", "low")
            entry = {"slug": slug, **story}
            groups.get(p, groups["low"]).append(entry)
        result("sprint_stories", success=True, priority="all", groups=groups)
    else:
        if priority_filter not in PRIORITY_LEVELS:
            error_result("sprint_stories",
                         f"Invalid priority: '{priority_filter}'. Must be one of: {', '.join(PRIORITY_LEVELS)} or 'all'",
                         priority=priority_filter)
        matched = [
            {"slug": slug, **story}
            for slug, story in stories.items()
            if story.get("priority", "low") == priority_filter
        ]
        result("sprint_stories", success=True, priority=priority_filter, stories=matched)


def cmd_sprint_next_stories(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    sp = sprints_path(project_dir)
    st = stories_path(project_dir)
    sprints = read_json(sp)
    stories = read_json(st)

    active = sprints.get("active")
    if not active:
        error_result("sprint_next_stories", "No active sprint exists")

    sprint_stories = active.get("stories", [])
    sprint_slug = active.get("slug", "unknown")

    ready = []
    blocked = []
    done_list = []

    terminal = {"done", "dropped", "closed-incomplete"}

    for slug in sprint_stories:
        story = stories.get(slug, {})
        status = story.get("status", "backlog")

        if status in terminal:
            done_list.append(slug)
            continue

        depends_on = story.get("depends_on", [])
        waiting_on = []
        for dep in depends_on:
            dep_story = stories.get(dep, {})
            if dep_story.get("status") != "done":
                waiting_on.append(dep)

        if waiting_on:
            blocked.append({"slug": slug, "waiting_on": waiting_on})
        else:
            ready.append(slug)

    result("sprint_next_stories", success=True, sprint=sprint_slug,
           ready=ready, blocked=blocked, done=done_list)


# --- Session Commands ---

def cmd_session_stats_update(args: argparse.Namespace) -> None:
    import os

    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", resolve_project_dir()))
    installed_path = project_dir / ".claude" / "momentum" / "installed.json"

    if not installed_path.exists():
        error_result("session_stats_update", f"installed.json not found: {installed_path}")

    data = json.loads(installed_path.read_text(encoding="utf-8"))

    if "session_stats" not in data:
        data["session_stats"] = {"momentum_completions": 0, "last_invocation": None}

    data["session_stats"]["momentum_completions"] = data["session_stats"].get("momentum_completions", 0) + 1
    data["session_stats"]["last_invocation"] = datetime.now().isoformat()

    installed_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    result("session_stats_update", success=True,
           momentum_completions=data["session_stats"]["momentum_completions"],
           last_invocation=data["session_stats"]["last_invocation"])


def cmd_session_greeting_state(args: argparse.Namespace) -> None:
    import os

    project_dir = resolve_project_dir()
    claude_project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", project_dir))

    sp = sprints_path(project_dir)
    st = stories_path(project_dir)
    installed_path = claude_project_dir / ".claude" / "momentum" / "installed.json"

    sprints = read_json(sp) if sp.exists() else {"active": None, "planning": None, "completed": []}
    stories = read_json(st) if st.exists() else {}
    installed = json.loads(installed_path.read_text(encoding="utf-8")) if installed_path.exists() else {}

    session_stats = installed.get("session_stats", {})
    momentum_completions = session_stats.get("momentum_completions", 0)

    active = sprints.get("active")
    planning = sprints.get("planning")
    completed = sprints.get("completed", [])

    active_sprint = active.get("slug") if active else None
    planning_sprint = planning.get("slug") if planning else None
    planning_status = planning.get("status") if planning else None

    last_completed_sprint = completed[-1].get("slug") if completed else None

    no_sprints = active is None and planning is None and len(completed) == 0

    # State detection priority order from story
    if momentum_completions == 0 and no_sprints:
        state = "first-session-ever"
    elif active is None and planning is None:
        state = "no-active-nothing-planned"
    elif active is None and planning and planning.get("status") == "ready":
        state = "no-active-planned-ready"
    elif active and active.get("status") == "done" and planning is None:
        state = "done-no-planned"
    elif active and active.get("status") == "done":
        state = "done-retro-needed"
    elif active and active.get("status") == "active" and planning and planning.get("status") in ("planning", "ready"):
        state = "active-planned-needs-work"
    else:
        # Active sprint exists with status "active" — sub-detection
        sprint_stories = active.get("stories", []) if active else []

        # Check for blocked stories
        has_blocked = False
        all_not_started = True
        for slug in sprint_stories:
            story = stories.get(slug, {})
            status = story.get("status", "backlog")
            if status in ("done", "dropped", "closed-incomplete"):
                continue
            if status not in ("backlog", "ready-for-dev"):
                all_not_started = False
            depends_on = story.get("depends_on", [])
            for dep in depends_on:
                dep_story = stories.get(dep, {})
                if dep_story.get("status") != "done":
                    has_blocked = True

        if has_blocked:
            state = "active-blocked"
        elif all_not_started:
            state = "active-not-started"
        else:
            state = "active-in-progress"

    feature_status = _compute_feature_status(project_dir, claude_project_dir)

    output = {
        "state": state,
        "active_sprint": active_sprint,
        "planning_sprint": planning_sprint,
        "planning_status": planning_status,
        "momentum_completions": momentum_completions,
        "last_completed_sprint": last_completed_sprint,
        "feature_status": feature_status,
    }
    result("session_greeting_state", success=True, **output)


def cmd_session_journal_status(args: argparse.Namespace) -> None:
    import os

    project_dir = resolve_project_dir()
    claude_project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", project_dir))
    journal_path = claude_project_dir / ".claude" / "momentum" / "journal.jsonl"

    if not journal_path.exists():
        result("session_journal_status", success=True,
               exists=False, open_threads=0, last_entry=None)
        return

    # Scan all entries
    total_entries = 0
    parse_errors = 0
    last_entry = None
    # thread_id -> list of events in order
    thread_events: dict[str, list[dict]] = {}

    TERMINAL_EVENTS = {"thread_close", "session_end", "done"}

    for line in journal_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            parse_errors += 1
            continue

        total_entries += 1
        ts = entry.get("timestamp")
        if ts and (last_entry is None or ts > last_entry):
            last_entry = ts

        thread_id = entry.get("thread_id")
        if thread_id:
            thread_events.setdefault(thread_id, []).append(entry)

    # Build thread summary
    thread_summary = []
    open_threads = 0
    for thread_id, events in thread_events.items():
        last_event_entry = events[-1]
        last_event = last_event_entry.get("event", "")
        last_ts = last_event_entry.get("timestamp")
        status = "closed" if last_event in TERMINAL_EVENTS else "open"
        if status == "open":
            open_threads += 1
        thread_summary.append({
            "thread_id": thread_id,
            "status": status,
            "last_event": last_event,
            "last_timestamp": last_ts,
        })

    result("session_journal_status", success=True,
           exists=True,
           open_threads=open_threads,
           last_entry=last_entry,
           total_entries=total_entries,
           parse_errors=parse_errors,
           thread_summary=thread_summary)


def cmd_session_journal_hygiene(args: argparse.Namespace) -> None:
    import os
    import subprocess as sp
    from datetime import timedelta

    project_dir = resolve_project_dir()
    claude_project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", project_dir))
    journal_path = claude_project_dir / ".claude" / "momentum" / "journal.jsonl"

    TERMINAL_EVENTS = {"thread_close", "session_end", "done"}

    suggested_prompts = {
        "concurrent": '!  "{summary}" appears active in another tab ({minutes} minutes ago). Opening here may cause conflicts. Proceed anyway?',
        "dormant": "{summary} — {days} days inactive. Close this thread? [Y] Yes · [N] Keep open",
        "dependency_satisfied": 'The work "{dep_summary}" that "{summary}" was waiting on is complete — ready to continue?',
        "unwieldy": "!  {count} open threads — consider a quick triage before starting new work. Close any that are stale?",
    }

    empty_result = {
        "threads": [],
        "warnings": {
            "concurrent": [],
            "dormant": [],
            "dependency_satisfied": [],
            "unwieldy": None,
        },
        "suppressed_offers": [],
        "suggested_prompts": suggested_prompts,
        "open_count": 0,
        "total_count": 0,
    }

    if not journal_path.exists():
        result("session_journal_hygiene", success=True, **empty_result)
        return

    # Parse journal — group by thread_id, collect all entries in order
    thread_entries: dict[str, list[dict]] = {}
    for line in journal_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        tid = entry.get("thread_id")
        if tid:
            thread_entries.setdefault(tid, []).append(entry)

    # Build thread state — last entry per thread determines current state
    thread_states: list[dict] = []
    for tid, entries in thread_entries.items():
        last = entries[-1]
        last_event = last.get("event", "")
        status = "closed" if last_event in TERMINAL_EVENTS else "open"
        state = {**last, "status": status}
        thread_states.append(state)

    total_count = len(thread_states)

    # Filter to open threads only
    open_threads = [t for t in thread_states if t.get("status") == "open"]

    if not open_threads:
        empty_result["total_count"] = total_count
        result("session_journal_hygiene", success=True, **empty_result)
        return

    # Get current datetime and git hash (once per invocation)
    now = datetime.now()
    git_hash = "unknown"
    try:
        proc = sp.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5, cwd=str(project_dir)
        )
        if proc.returncode == 0:
            git_hash = proc.stdout.strip()
    except (sp.TimeoutExpired, FileNotFoundError):
        pass

    def parse_ts(ts_str: str) -> "datetime | None":
        if not ts_str:
            return None
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%f"):
            try:
                return datetime.strptime(ts_str, fmt)
            except ValueError:
                continue
        try:
            return datetime.fromisoformat(ts_str.replace("Z", "+00:00")).replace(tzinfo=None)
        except (ValueError, AttributeError):
            return None

    def elapsed_label(ts: datetime) -> str:
        delta = now - ts
        total_seconds = delta.total_seconds()
        if total_seconds < 3600:
            mins = max(1, int(total_seconds / 60))
            return f"{mins}m ago"
        if total_seconds < 86400:
            hours = int(total_seconds / 3600)
            return f"{hours}h ago"
        if total_seconds < 172800:
            return "yesterday"
        days = int(total_seconds / 86400)
        return f"{days}d ago"

    # Build enriched thread list with elapsed labels
    enriched: list[dict] = []
    for t in open_threads:
        ts_str = t.get("last_active") or t.get("timestamp", "")
        ts = parse_ts(ts_str)
        label = elapsed_label(ts) if ts else "unknown"
        enriched.append({
            "thread_id": t.get("thread_id", ""),
            "context_summary_short": t.get("context_summary_short", ""),
            "context_summary": t.get("context_summary", ""),
            "phase": t.get("phase", ""),
            "story_ref": t.get("story_ref", ""),
            "last_active": ts_str,
            "elapsed_label": label,
            "status": "open",
            # Internal fields for warning computation — stripped before output
            "_ts": ts,
            "_declined_offers": t.get("declined_offers", []),
            "_depends_on_thread": t.get("depends_on_thread"),
        })

    # Sort by last_active descending (most recent first)
    enriched.sort(key=lambda x: x["_ts"] or datetime.min, reverse=True)

    # Lookup for all thread states by thread_id (for dependency resolution)
    all_states_by_id = {t.get("thread_id", ""): t for t in thread_states}

    # Lookup for most recent context_summary_short per thread across all events
    # (thread_close events often lack context_summary_short; scan all entries)
    context_summary_by_tid: dict[str, str] = {}
    for tid, entries in thread_entries.items():
        for entry in reversed(entries):
            css = entry.get("context_summary_short")
            if css:
                context_summary_by_tid[tid] = css
                break

    # --- Warning computation ---
    concurrent: list[dict] = []
    dormant_raw: list[dict] = []
    dependency_satisfied: list[dict] = []

    thirty_min_ago = now - timedelta(minutes=30)
    three_days_ago = now - timedelta(days=3)

    for t in enriched:
        ts = t["_ts"]
        if ts is None:
            continue

        # Concurrent: active within 30 minutes of now
        if ts >= thirty_min_ago:
            minutes_ago = max(0, int((now - ts).total_seconds() / 60))
            concurrent.append({
                "thread_id": t["thread_id"],
                "context_summary_short": t["context_summary_short"],
                "minutes_ago": minutes_ago,
            })

        # Dormant: inactive more than 3 days
        if ts < three_days_ago:
            days_inactive = int((now - ts).total_seconds() / 86400)
            dormant_raw.append({
                "thread_id": t["thread_id"],
                "context_summary_short": t["context_summary_short"],
                "days_inactive": days_inactive,
                "_declined_offers": t["_declined_offers"],
                "_story_ref": t["story_ref"],
                "_phase": t["phase"],
            })

        # Dependency satisfied
        dep_tid = t["_depends_on_thread"]
        if dep_tid:
            dep_state = all_states_by_id.get(dep_tid)
            if dep_state and dep_state.get("status") == "closed":
                dep_summary = context_summary_by_tid.get(dep_tid, dep_tid)
                dependency_satisfied.append({
                    "thread_id": t["thread_id"],
                    "context_summary_short": t["context_summary_short"],
                    "depends_on_summary": dep_summary,
                })

    # Unwieldy: more than 5 open threads
    open_count = len(enriched)
    unwieldy = {"open_count": open_count} if open_count > 5 else None

    # --- No-Re-Offer suppression for dormant threads ---
    dormant: list[dict] = []
    suppressed_offers: list[dict] = []

    for d in dormant_raw:
        tid = d["thread_id"]
        story_ref = d["_story_ref"]
        phase = d["_phase"]
        context_hash = f"{tid}|{story_ref}|{phase}|{git_hash}"

        suppressed = any(
            offer.get("offer_type") == "dormant-closure"
            and offer.get("context_hash") == context_hash
            for offer in d["_declined_offers"]
        )

        if suppressed:
            suppressed_offers.append({
                "thread_id": tid,
                "offer_type": "dormant-closure",
                "reason": "declined, context unchanged",
            })
        else:
            dormant.append({
                "thread_id": tid,
                "context_summary_short": d["context_summary_short"],
                "days_inactive": d["days_inactive"],
            })

    # Strip internal fields before output
    threads_out = [{k: v for k, v in t.items() if not k.startswith("_")} for t in enriched]

    output = {
        "threads": threads_out,
        "warnings": {
            "concurrent": concurrent,
            "dormant": dormant,
            "dependency_satisfied": dependency_satisfied,
            "unwieldy": unwieldy,
        },
        "suppressed_offers": suppressed_offers,
        "suggested_prompts": suggested_prompts,
        "open_count": open_count,
        "total_count": total_count,
    }
    result("session_journal_hygiene", success=True, **output)


def _regenerate_journal_view(journal_path: Path, view_path: Path) -> None:
    """Regenerate journal-view.md from journal.jsonl."""
    from datetime import timedelta

    TERMINAL_EVENTS = {"thread_close", "session_end", "done"}

    if not journal_path.exists():
        return

    # Read and group by thread_id (last entry wins)
    thread_last: dict[str, dict] = {}
    for line in journal_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        tid = entry.get("thread_id")
        if tid:
            thread_last[tid] = entry

    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)

    def parse_ts_view(ts_str: str) -> "datetime | None":
        if not ts_str:
            return None
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%f"):
            try:
                return datetime.strptime(ts_str, fmt)
            except ValueError:
                continue
        try:
            return datetime.fromisoformat(ts_str.replace("Z", "+00:00")).replace(tzinfo=None)
        except (ValueError, AttributeError):
            return None

    rows = []
    for tid, entry in thread_last.items():
        last_event = entry.get("event", "")
        is_closed = last_event in TERMINAL_EVENTS

        ts_str = entry.get("last_active") or entry.get("timestamp", "")
        ts = parse_ts_view(ts_str)

        # For closed threads: only include if closed within 7 days
        if is_closed:
            if ts is None or ts < seven_days_ago:
                continue

        rows.append({
            "thread": entry.get("context_summary_short", ""),
            "story": entry.get("story_ref", ""),
            "phase": entry.get("phase", ""),
            "last_action": last_event,
            "last_active": ts_str,
            "status": "closed" if is_closed else "open",
            "_ts": ts,
            "_is_closed": is_closed,
        })

    # Sort: open threads first (most recent first), then recent closed (most recent first)
    open_rows = sorted(
        [r for r in rows if not r["_is_closed"]],
        key=lambda r: r["_ts"] or datetime.min,
        reverse=True,
    )
    closed_rows = sorted(
        [r for r in rows if r["_is_closed"]],
        key=lambda r: r["_ts"] or datetime.min,
        reverse=True,
    )
    rows = open_rows + closed_rows

    lines = [
        "# Journal View\n",
        "| Thread | Story | Phase | Last Action | Last Active | Status |",
        "|--------|-------|-------|-------------|-------------|--------|",
    ]
    for r in rows:
        thread = r["thread"].replace("|", "&#124;")
        story = r["story"].replace("|", "&#124;")
        phase = r["phase"].replace("|", "&#124;")
        last_action = r["last_action"].replace("|", "&#124;")
        lines.append(
            f"| {thread} | {story} | {phase} | {last_action} | {r['last_active']} | {r['status']} |"
        )

    view_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_session_journal_append(args: argparse.Namespace) -> None:
    import os

    project_dir = resolve_project_dir()
    claude_project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", project_dir))
    journal_dir = claude_project_dir / ".claude" / "momentum"
    journal_path = journal_dir / "journal.jsonl"
    view_path = journal_dir / "journal-view.md"

    entry_str = args.entry

    # Validate JSON
    try:
        entry_data = json.loads(entry_str)
    except json.JSONDecodeError as e:
        error_result("session_journal_append", f"Invalid JSON: {e}")
        return

    # Ensure journal directory exists
    journal_dir.mkdir(parents=True, exist_ok=True)

    # Atomic append: write to temp file, verify, then append to journal
    tmp_path = journal_dir / "journal.jsonl.tmp"
    line = json.dumps(entry_data, ensure_ascii=False)
    try:
        tmp_path.write_text(line + "\n", encoding="utf-8")
        # Verify temp file is valid JSON
        json.loads(tmp_path.read_text(encoding="utf-8").strip())
        # Append to journal
        with open(journal_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        tmp_path.unlink(missing_ok=True)
    except Exception as e:
        tmp_path.unlink(missing_ok=True)
        error_result("session_journal_append", f"Append failed: {e}")
        return

    # Regenerate journal-view.md
    _regenerate_journal_view(journal_path, view_path)

    result("session_journal_append", success=True,
           journal_path=str(journal_path),
           view_path=str(view_path))


def cmd_session_startup_preflight(args: argparse.Namespace) -> None:
    import os
    import subprocess as sp

    project_dir = resolve_project_dir()
    claude_project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", project_dir))

    versions_path = project_dir / "skills" / "momentum" / "references" / "momentum-versions.json"
    installed_path = claude_project_dir / ".claude" / "momentum" / "installed.json"
    global_installed_path = Path.home() / ".claude" / "momentum" / "global-installed.json"
    journal_path = claude_project_dir / ".claude" / "momentum" / "journal.jsonl"

    # Read versions manifest
    current_version = "0.0.0"
    versions_data: dict = {}
    if versions_path.exists():
        try:
            versions_data = json.loads(versions_path.read_text(encoding="utf-8"))
            current_version = versions_data.get("current_version", "0.0.0")
        except json.JSONDecodeError:
            pass

    # Read installed.json (project-scoped)
    installed_data: dict = {}
    if installed_path.exists():
        try:
            installed_data = json.loads(installed_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    # Read global-installed.json
    global_data: dict = {}
    if global_installed_path.exists():
        try:
            global_data = json.loads(global_installed_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    # Per-component version comparison (mirrors workflow Step 1 logic)
    # Collect unique groups and their scopes from the current version's actions
    version_actions = versions_data.get("versions", {}).get(current_version, {}).get("actions", [])
    groups: dict[str, str] = {}  # group_name -> scope
    for action in version_actions:
        group = action.get("group")
        scope = action.get("scope")
        if group and scope and group not in groups:
            groups[group] = scope

    needs_work: list[dict] = []
    for group_name, scope in groups.items():
        if scope == "global":
            group_version = global_data.get("components", {}).get(group_name, {}).get("version")
        else:
            group_version = installed_data.get("components", {}).get(group_name, {}).get("version")

        if group_version is None or group_version < current_version:
            needs_work.append({"group": group_name, "scope": scope, "installed_version": group_version})

    # Determine if any group has a version behind (upgrade) vs absent (first install)
    any_behind = any(g.get("installed_version") is not None for g in needs_work)
    all_absent = all(g.get("installed_version") is None for g in needs_work)
    both_files_empty = not installed_data.get("components") and not global_data.get("components")

    # Hash drift detection — resolve target paths from version manifest actions
    hash_drift = False
    hash_check_errors: list[str] = []
    if not needs_work:  # only check drift when all groups are current
        global_components = global_data.get("components", {})
        for comp_name, comp_info in global_components.items():
            if not isinstance(comp_info, dict):
                continue
            stored_hash = comp_info.get("hash")
            if not stored_hash:
                continue

            # Find the first add/replace action for this group to get the target path
            target = None
            for action in version_actions:
                if action.get("group") == comp_name and action.get("action") in ("add", "replace"):
                    target = action.get("target")
                    break

            if not target:
                continue

            target_path = Path(os.path.expanduser(target))
            if not target_path.exists():
                hash_check_errors.append(f"{comp_name}: target file missing ({target})")
                continue

            try:
                proc = sp.run(
                    ["git", "hash-object", str(target_path)],
                    capture_output=True, text=True, timeout=5
                )
                if proc.returncode == 0:
                    current_hash = proc.stdout.strip()
                    if current_hash != stored_hash:
                        hash_drift = True
                else:
                    hash_check_errors.append(f"{comp_name}: git hash-object failed (rc={proc.returncode})")
            except sp.TimeoutExpired:
                hash_check_errors.append(f"{comp_name}: git hash-object timed out")
            except FileNotFoundError:
                hash_check_errors.append(f"{comp_name}: git not found")

    # Journal thread check
    has_open_threads = False
    if journal_path.exists():
        try:
            threads: dict[str, dict] = {}
            for line in journal_path.read_text(encoding="utf-8").strip().splitlines():
                if not line.strip():
                    continue
                entry = json.loads(line)
                tid = entry.get("thread_id")
                if tid:
                    threads[tid] = entry
            has_open_threads = any(t.get("status") == "open" for t in threads.values())
        except (json.JSONDecodeError, KeyError):
            pass

    # Config gaps
    config_gaps: list[str] = []
    mcp_path = claude_project_dir / ".mcp.json"
    if mcp_path.exists():
        try:
            json.loads(mcp_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            config_gaps.append("invalid .mcp.json")

    # Route determination
    if needs_work and both_files_empty:
        route = "first-install"
    elif needs_work and any_behind:
        route = "upgrade"
    elif needs_work and all_absent:
        route = "first-install"
    elif hash_drift:
        route = "hash-drift"
    else:
        route = "greeting"

    # Inline greeting-state computation when route is "greeting"
    greeting = None
    if route == "greeting":
        _sp = sprints_path(project_dir)
        _st = stories_path(project_dir)
        sprints = read_json(_sp) if _sp.exists() else {"active": None, "planning": None, "completed": []}
        stories = read_json(_st) if _st.exists() else {}
        session_stats = installed_data.get("session_stats", {})
        momentum_completions = session_stats.get("momentum_completions", 0)

        active = sprints.get("active")
        planning = sprints.get("planning")
        completed = sprints.get("completed", [])

        active_sprint = active.get("slug") if active else None
        planning_sprint = planning.get("slug") if planning else None
        planning_status = planning.get("status") if planning else None
        last_completed_sprint = completed[-1].get("slug") if completed else None
        no_sprints = active is None and planning is None and len(completed) == 0

        if momentum_completions == 0 and no_sprints:
            state = "first-session-ever"
        elif active is None and planning is None:
            state = "no-active-nothing-planned"
        elif active is None and planning and planning.get("status") == "ready":
            state = "no-active-planned-ready"
        elif active and active.get("status") == "done" and planning is None:
            state = "done-no-planned"
        elif active and active.get("status") == "done":
            state = "done-retro-needed"
        elif active and active.get("status") == "active" and planning and planning.get("status") in ("planning", "ready"):
            state = "active-planned-needs-work"
        else:
            sprint_stories = active.get("stories", []) if active else []
            has_blocked = False
            all_not_started = True
            for slug in sprint_stories:
                story = stories.get(slug, {})
                status = story.get("status", "backlog")
                if status in ("done", "dropped", "closed-incomplete"):
                    continue
                if status not in ("backlog", "ready-for-dev"):
                    all_not_started = False
                for dep in story.get("depends_on", []):
                    dep_story = stories.get(dep, {})
                    if dep_story.get("status") != "done":
                        has_blocked = True

            if has_blocked:
                state = "active-blocked"
            elif all_not_started:
                state = "active-not-started"
            else:
                state = "active-in-progress"

        # --- Render greeting templates inline (eliminates session-greeting.md read) ---
        _vars = {
            "active_sprint": active_sprint or planning_sprint or "unknown",
            "planning_sprint": planning_sprint or "",
            "last_completed_sprint": last_completed_sprint or "",
        }

        _narratives = {
            "first-session-ever": "I am Impetus. I hold the line on engineering discipline \u2014 sprints, quality, the lifecycle of every story. You build. I make sure nothing falls through the cracks.\n\nThis is the beginning. Let\u2019s forge something worth building.",
            "active-not-started": 'The path is clear. Sprint \u201c{active_sprint}\u201d stands ready \u2014 waiting on you to lead the way.',
            "active-in-progress": 'Sprint \u201c{active_sprint}\u201d is underway \u2014 steady ground, nothing standing in our way.',
            "active-blocked": 'Sprint \u201c{active_sprint}\u201d \u2014 something stands in the way. One story needs you before we can move forward.',
            "active-planned-needs-work": 'Sprint \u201c{active_sprint}\u201d is underway \u2014 holding strong.',
            "done-retro-needed": 'Sprint \u201c{active_sprint}\u201d \u2014 the work is done. Every story carried across the line.',
            "done-no-planned": 'Sprint \u201c{active_sprint}\u201d \u2014 the work is done.',
            "no-active-nothing-planned": 'All still. The last sprint \u2014 \u201c{last_completed_sprint}\u201d \u2014 was carried to completion.',
            "no-active-planned-ready": '\u201c{planning_sprint}\u201d stands ready. The groundwork is laid.',
        }

        _planning_contexts = {
            "active-not-started": '\u201c{planning_sprint}\u201d is taking shape behind it.',
            "active-in-progress": '\u201c{planning_sprint}\u201d is taking shape behind it.',
            "active-blocked": '\u201c{planning_sprint}\u201d is taking shape behind it.',
            "active-planned-needs-work": '\u201c{planning_sprint}\u201d is coming together, but it needs more of your thinking before it\u2019s ready to stand on its own.',
            "done-retro-needed": '\u201c{planning_sprint}\u201d stands ready \u2014 it rises the moment we close this chapter.',
            "done-no-planned": 'Nothing yet follows it. A good moment to look ahead and decide what we build next.',
        }

        _menus = {
            "first-session-ever": ["Plan a sprint", "Refine backlog", "Triage"],
            "active-not-started": ["Run the sprint", "Refine backlog", "Triage"],
            "active-in-progress": ["Continue the sprint", "Refine backlog", "Triage"],
            "active-blocked": ["Continue the sprint", "Refine backlog", "Triage"],
            "active-planned-needs-work": ["Continue the sprint", "Finish planning", "Refine backlog", "Triage"],
            "done-retro-needed": ["Run retro", "Refine backlog", "Triage"],
            "done-no-planned": ["Run retro", "Plan a sprint", "Refine backlog", "Triage"],
            "no-active-nothing-planned": ["Plan a sprint", "Refine backlog", "Triage"],
            "no-active-planned-ready": ["Activate sprint", "Refine backlog", "Triage"],
        }

        _closers = {
            "first-session-ever": "Where do we begin?",
            "active-not-started": "Where do we begin?",
            "active-in-progress": "Lead on.",
            "active-blocked": "Let\u2019s face it together.",
            "active-planned-needs-work": "I\u2019m with you.",
            "done-retro-needed": "One last step to honor the work.",
            "done-no-planned": "The road is open.",
            "no-active-nothing-planned": "When you\u2019re ready, I\u2019m here.",
            "no-active-planned-ready": "Give the word.",
        }

        rendered_narrative = _narratives.get(state, "").format(**_vars)
        rendered_planning_context = (_planning_contexts.get(state) or "").format(**_vars) or None
        rendered_menu = [f"[{i+1}] {item}" for i, item in enumerate(_menus.get(state, []))]
        rendered_closer = _closers.get(state, "")

        feature_status = _compute_feature_status(project_dir, claude_project_dir)

        greeting = {
            "state": state,
            "active_sprint": active_sprint,
            "planning_sprint": planning_sprint,
            "planning_status": planning_status,
            "momentum_completions": momentum_completions,
            "last_completed_sprint": last_completed_sprint,
            "narrative": rendered_narrative,
            "planning_context": rendered_planning_context,
            "menu": rendered_menu,
            "closer": rendered_closer,
            "feature_status": feature_status,
        }

    result("session_startup_preflight", success=True,
           route=route,
           needs_work=[{"group": g["group"], "scope": g["scope"]} for g in needs_work],
           hash_drift=hash_drift,
           hash_check_errors=hash_check_errors,
           has_open_threads=has_open_threads,
           config_gaps=config_gaps,
           greeting=greeting,
           current_version=current_version)


# --- Feature Status Cache ---

def _compute_feature_status(project_dir: Path, claude_project_dir: Path) -> dict:
    """Compute feature status dict from cache and hash inputs.

    Returns a dict with a 'state' key — one of:
      - 'no-features': features.json absent
      - 'no-cache':    features.json present but cache missing/unparseable
      - 'fresh':       cache present and hash matches
      - 'stale':       cache present but hash mismatches
    """
    import hashlib

    features_path = project_dir / "_bmad-output" / "planning-artifacts" / "features.json"
    stories_path_val = project_dir / "_bmad-output" / "implementation-artifacts" / "stories" / "index.json"
    cache_path = claude_project_dir / ".claude" / "momentum" / "feature-status.md"

    if not features_path.exists():
        return {"state": "no-features"}

    # Read raw content for hashing
    try:
        features_content = features_path.read_text(encoding="utf-8")
    except OSError:
        features_content = ""

    try:
        stories_content = stories_path_val.read_text(encoding="utf-8") if stories_path_val.exists() else ""
    except OSError:
        stories_content = ""

    computed_hash = hashlib.sha256(
        (features_content + ":" + stories_content).encode()
    ).hexdigest()

    # Parse frontmatter from cache file
    frontmatter = _read_frontmatter(cache_path)
    if frontmatter is None:
        return {"state": "no-cache"}

    cached_hash = frontmatter.get("input_hash", "")
    summary = frontmatter.get("summary", "")

    if cached_hash == computed_hash:
        return {"state": "fresh", "summary": summary}
    else:
        return {"state": "stale", "summary": summary}


def _read_frontmatter(path: Path) -> dict | None:
    """Read YAML-style frontmatter from a markdown file.

    Returns None if file is absent, not readable, or has no valid frontmatter block.
    Returns a dict of key: value pairs parsed from the --- block.
    """
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    # Find closing ---
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return None

    frontmatter: dict = {}
    for line in lines[1:end_idx]:
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            # Strip surrounding quotes if present
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            frontmatter[key] = value

    return frontmatter


def cmd_feature_status_hash(args: argparse.Namespace) -> None:
    """Compute SHA-256 hash of features.json + stories/index.json."""
    import hashlib
    import os

    project_dir = resolve_project_dir()

    features_path = project_dir / "_bmad-output" / "planning-artifacts" / "features.json"
    stories_path_val = project_dir / "_bmad-output" / "implementation-artifacts" / "stories" / "index.json"

    if not features_path.exists():
        result("feature_status_hash", success=True,
               hash_result={"hash": "", "features_present": False})
        return

    try:
        features_content = features_path.read_text(encoding="utf-8")
    except OSError:
        features_content = ""

    try:
        stories_content = stories_path_val.read_text(encoding="utf-8") if stories_path_val.exists() else ""
    except OSError:
        stories_content = ""

    combined = features_content + ":" + stories_content
    digest = hashlib.sha256(combined.encode()).hexdigest()

    result("feature_status_hash", success=True,
           hash_result={"hash": digest, "features_present": True})


# --- Specialist Classify Command ---

SPECIALIST_PATTERNS: list[tuple[list[str], str]] = [
    # (glob-like patterns, specialist name) — checked in table order
    (["skills/*/SKILL.md", "skills/*/workflow.md", "*/agents/*.md", "agents/*.md"], "dev-skills"),
    (["*.gradle*", "*.kts", "build.gradle*"], "dev-build"),
    (["*compose*", "*Compose*", "*ui/*", "*screen*"], "dev-frontend"),
]


def _match_specialist(path: str) -> str | None:
    """Return specialist name if path matches any pattern, else None."""
    import fnmatch
    for patterns, specialist in SPECIALIST_PATTERNS:
        for pat in patterns:
            if fnmatch.fnmatch(path, pat):
                return specialist
    return None


def cmd_specialist_classify(args: argparse.Namespace) -> None:
    touches_raw = args.touches if args.touches else ""
    paths = [p.strip() for p in touches_raw.split(",") if p.strip()]

    if not paths:
        result("specialist_classify", success=True,
               specialist="dev",
               agent_file="skills/momentum/agents/dev.md",
               matches={},
               fallback=False)
        return

    tally: dict[str, int] = {}
    for p in paths:
        spec = _match_specialist(p)
        if spec:
            tally[spec] = tally.get(spec, 0) + 1

    if not tally:
        # No matches — base dev
        project_dir = resolve_project_dir()
        agent_file = "skills/momentum/agents/dev.md"
        fallback = not (project_dir / agent_file).exists()
        result("specialist_classify", success=True,
               specialist="dev",
               agent_file=agent_file,
               matches={},
               fallback=fallback)
        return

    # Majority rule; ties broken by table order
    max_count = max(tally.values())
    winner = None
    for _patterns, specialist in SPECIALIST_PATTERNS:
        if tally.get(specialist, 0) == max_count:
            winner = specialist
            break

    agent_file = f"skills/momentum/agents/{winner}.md"
    project_dir = resolve_project_dir()
    fallback = not (project_dir / agent_file).exists()

    if fallback:
        agent_file = "skills/momentum/agents/dev.md"

    result("specialist_classify", success=True,
           specialist=winner,
           agent_file=agent_file,
           matches=tally,
           fallback=fallback)


# --- Quickfix Commands ---

def cmd_quickfix_register(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    slug = args.slug
    story = args.story

    if not story or not story.strip():
        error_result("quickfix_register", "Story key must not be empty", slug=slug)

    if "quickfixes" not in sprints:
        sprints["quickfixes"] = []

    # Auto-increment duplicate slugs
    existing_slugs = {qf["slug"] for qf in sprints["quickfixes"]}
    resolved_slug = slug
    if resolved_slug in existing_slugs:
        counter = 2
        while f"{slug}-{counter}" in existing_slugs:
            counter += 1
        resolved_slug = f"{slug}-{counter}"

    entry = {
        "slug": resolved_slug,
        "story": story,
        "started": date.today().isoformat(),
    }
    sprints["quickfixes"].append(entry)
    write_json(path, sprints)

    result("quickfix_register", success=True, **entry)


def cmd_quickfix_complete(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    slug = args.slug
    quickfixes = sprints.get("quickfixes", [])

    target = None
    for qf in quickfixes:
        if qf["slug"] == slug:
            target = qf
            break

    if target is None:
        error_result("quickfix_complete", f"Quickfix '{slug}' not found", slug=slug)

    target["completed"] = date.today().isoformat()
    write_json(path, sprints)

    result("quickfix_complete", success=True, slug=slug, completed=target["completed"])


# --- Story Commands ---

VALID_PRIORITIES = {"critical", "high", "medium", "low"}


def cmd_story_add(args: argparse.Namespace) -> None:
    """Add a new story entry to stories/index.json."""
    project_dir = resolve_project_dir()
    path = stories_path(project_dir)
    stories = read_json(path)

    slug = args.slug.strip()
    if not slug:
        error_result("story_add", "Slug must not be empty", slug=slug)

    if slug in stories:
        error_result("story_add", f"Story slug '{slug}' already exists in stories/index.json", slug=slug)

    priority = args.priority if args.priority else "low"
    if priority not in VALID_PRIORITIES:
        error_result("story_add", f"Invalid priority '{priority}'. Must be one of: {', '.join(sorted(VALID_PRIORITIES))}", slug=slug)

    VALID_STORY_TYPES = {"feature", "maintenance", "defect", "exploration", "practice"}
    story_type = (args.story_type or "feature").strip().lower()
    if story_type not in VALID_STORY_TYPES:
        error_result("story_add", f"Invalid story_type '{story_type}'. Must be one of: {', '.join(sorted(VALID_STORY_TYPES))}", slug=slug)

    entry = {
        "status": "backlog",
        "title": args.title.strip(),
        "epic_slug": args.epic.strip(),
        "story_file": True,
        "depends_on": [],
        "touches": [],
        "priority": priority,
        "story_type": story_type,
    }

    feature_slug = (args.feature_slug or "").strip()
    if feature_slug:
        entry["feature_slug"] = feature_slug

    stories[slug] = entry
    write_json(path, stories)

    result("story_add", success=True, slug=slug, **entry)


# --- Intake Queue Commands ---

INTAKE_QUEUE_KINDS = {"shape", "watch", "rejected", "handoff"}
INTAKE_QUEUE_SOURCES = {"triage", "retro", "assessment"}
INTAKE_QUEUE_STATUSES = {"open", "consumed"}


def intake_queue_path(project_dir: Path) -> Path:
    return project_dir / "_bmad-output" / "implementation-artifacts" / "intake-queue.jsonl"


def cmd_intake_queue_append(args: argparse.Namespace) -> None:
    """Append an event to intake-queue.jsonl."""
    import uuid

    project_dir = resolve_project_dir()
    queue_path = intake_queue_path(project_dir)

    kind = args.kind
    source = args.source
    if kind not in INTAKE_QUEUE_KINDS:
        error_result("intake_queue_append", f"Invalid kind '{kind}'. Must be one of: {', '.join(sorted(INTAKE_QUEUE_KINDS))}")
        return
    if source not in INTAKE_QUEUE_SOURCES:
        error_result("intake_queue_append", f"Invalid source '{source}'. Must be one of: {', '.join(sorted(INTAKE_QUEUE_SOURCES))}")
        return

    # Build the event
    event_id = f"iq-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:8]}"
    event: dict = {
        "id": event_id,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": source,
        "kind": kind,
        "status": "open",
        "title": args.title,
        "description": args.description or "",
        "sprint_slug": args.sprint_slug or None,
    }

    # Optional enrichment fields
    if args.feature_slug:
        event["feature_slug"] = args.feature_slug
    if args.story_type:
        event["story_type"] = args.story_type
    if args.feature_state_transition:
        try:
            fst = json.loads(args.feature_state_transition)
            event["feature_state_transition"] = fst
        except json.JSONDecodeError as e:
            error_result("intake_queue_append", f"Invalid JSON for --feature-state-transition: {e}")
            return
    if args.failure_diagnosis:
        try:
            fd = json.loads(args.failure_diagnosis)
            event["failure_diagnosis"] = fd
        except json.JSONDecodeError as e:
            error_result("intake_queue_append", f"Invalid JSON for --failure-diagnosis: {e}")
            return

    # Ensure directory exists
    queue_path.parent.mkdir(parents=True, exist_ok=True)

    # Atomic append
    line = json.dumps(event, ensure_ascii=False)
    tmp_path = queue_path.parent / "intake-queue.jsonl.tmp"
    try:
        tmp_path.write_text(line + "\n", encoding="utf-8")
        json.loads(tmp_path.read_text(encoding="utf-8").strip())
        with open(queue_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        tmp_path.unlink(missing_ok=True)
    except Exception as e:
        tmp_path.unlink(missing_ok=True)
        error_result("intake_queue_append", f"Append failed: {e}")
        return

    result("intake_queue_append", success=True, id=event_id, queue_path=str(queue_path))


def cmd_intake_queue_list(args: argparse.Namespace) -> None:
    """List events from intake-queue.jsonl, with optional filters."""
    project_dir = resolve_project_dir()
    queue_path = intake_queue_path(project_dir)

    if not queue_path.exists():
        result("intake_queue_list", success=True, events=[], count=0,
               queue_path=str(queue_path), note="intake-queue.jsonl does not exist yet")
        return

    events = []
    with open(queue_path, encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                # Skip malformed lines silently
                continue

            # Apply filters
            if args.source and event.get("source") != args.source:
                continue
            if args.kind and event.get("kind") != args.kind:
                continue
            if args.status and event.get("status") != args.status:
                continue

            events.append(event)

    result("intake_queue_list", success=True, events=events, count=len(events),
           queue_path=str(queue_path))


def cmd_intake_queue_consume(args: argparse.Namespace) -> None:
    """Mark an intake-queue event as consumed by rewriting its status field."""
    project_dir = resolve_project_dir()
    queue_path = intake_queue_path(project_dir)

    if not queue_path.exists():
        error_result("intake_queue_consume", "intake-queue.jsonl does not exist")
        return

    event_id = args.id
    outcome_ref = args.outcome_ref or ""

    lines = queue_path.read_text(encoding="utf-8").splitlines()
    updated = False
    new_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            new_lines.append(line)
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            new_lines.append(line)
            continue
        if event.get("id") == event_id:
            event["status"] = "consumed"
            event["consumed_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            if outcome_ref:
                event["outcome_ref"] = outcome_ref
            updated = True
        new_lines.append(json.dumps(event, ensure_ascii=False))

    if not updated:
        error_result("intake_queue_consume", f"Event id '{event_id}' not found in intake-queue.jsonl")
        return

    queue_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    result("intake_queue_consume", success=True, id=event_id, queue_path=str(queue_path))


# --- Version Command ---

def cmd_version_check(args: argparse.Namespace) -> None:
    import hashlib
    import os

    project_dir = resolve_project_dir()
    source_skill = project_dir / "skills" / "momentum" / "SKILL.md"
    installed_json = Path(os.environ.get("CLAUDE_PROJECT_DIR", project_dir)) / ".claude" / "momentum" / "installed.json"

    if not source_skill.exists():
        error_result("version_check", f"Source skill not found: {source_skill}")

    source_hash = hashlib.sha256(source_skill.read_bytes()).hexdigest()[:12]

    installed_hash = None
    if installed_json.exists():
        try:
            installed = json.loads(installed_json.read_text(encoding="utf-8"))
            installed_hash = installed.get("hash", None)
        except (json.JSONDecodeError, KeyError):
            installed_hash = None

    matches = source_hash == installed_hash
    result("version_check", success=True, source_hash=source_hash,
           installed_hash=installed_hash, up_to_date=matches)


# --- CLI Parser ---

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="momentum-tools",
        description="Deterministic CLI for Momentum sprint and story operations",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # sprint command group
    sprint = subparsers.add_parser("sprint", help="Sprint and story operations")
    sprint_sub = sprint.add_subparsers(dest="sprint_action", required=True)

    # sprint status-transition
    st = sprint_sub.add_parser("status-transition", help="Transition a story's status")
    st.add_argument("--story", required=True, help="Story slug")
    st.add_argument("--target", required=True, help="Target status")
    st.add_argument("--force", action="store_true", help="Bypass state machine validation")
    st.set_defaults(func=cmd_status_transition)

    # sprint activate
    sa = sprint_sub.add_parser("activate", help="Activate the planning sprint")
    sa.set_defaults(func=cmd_sprint_activate)

    # sprint complete
    sc = sprint_sub.add_parser("complete", help="Complete the active sprint")
    sc.set_defaults(func=cmd_sprint_complete)

    # sprint epic-membership
    em = sprint_sub.add_parser("epic-membership", help="Change a story's epic")
    em.add_argument("--story", required=True, help="Story slug")
    em.add_argument("--epic", required=True, help="Target epic slug")
    em.set_defaults(func=cmd_epic_membership)

    # sprint plan
    sp = sprint_sub.add_parser("plan", help="Add/remove stories from planning sprint")
    sp.add_argument("--operation", required=True, choices=["add", "remove"], help="Add or remove")
    sp.add_argument("--stories", required=True, help="Comma-separated story slugs")
    sp.add_argument("--wave", type=int, default=None, help="Wave number (for add)")
    sp.set_defaults(func=cmd_sprint_plan)

    # sprint ready
    sr = sprint_sub.add_parser("ready", help="Mark planning sprint as ready")
    sr.set_defaults(func=cmd_sprint_ready)

    # sprint retro-complete
    src = sprint_sub.add_parser("retro-complete", help="Mark retro done on most recent completed sprint")
    src.set_defaults(func=cmd_sprint_retro_complete)

    # sprint next-stories
    sns = sprint_sub.add_parser("next-stories", help="List unblocked stories in active sprint")
    sns.set_defaults(func=cmd_sprint_next_stories)

    # sprint migrate-priority
    smp = sprint_sub.add_parser("migrate-priority", help="Add priority=low to any story entry missing the field")
    smp.set_defaults(func=cmd_sprint_migrate_priority)

    # sprint set-priority
    ssp = sprint_sub.add_parser("set-priority", help="Set priority on a story")
    ssp.add_argument("--story", required=True, help="Story slug")
    ssp.add_argument("--priority", required=True, help="Priority level: critical, high, medium, low")
    ssp.set_defaults(func=cmd_sprint_set_priority)

    # sprint story-add
    sta = sprint_sub.add_parser("story-add", help="Add a new story entry to stories/index.json")
    sta.add_argument("--slug", required=True, help="Story slug (kebab-case, unique)")
    sta.add_argument("--title", required=True, help="Human-readable story title")
    sta.add_argument("--epic", required=True, help="Epic slug this story belongs to")
    sta.add_argument("--priority", default="low", help="Priority: critical, high, medium, low (default: low)")
    sta.add_argument("--feature-slug", default="", help="Feature slug this story belongs to (optional)")
    sta.add_argument("--story-type", default="feature", help="Story type: feature, maintenance, defect, exploration, practice (default: feature)")
    sta.set_defaults(func=cmd_story_add)

    # sprint stories
    ss = sprint_sub.add_parser("stories", help="Query stories by priority")
    ss.add_argument("--priority", required=True,
                    help="Priority level (critical, high, medium, low) or 'all' for grouped output")
    ss.set_defaults(func=cmd_sprint_stories)

    # session command group
    session = subparsers.add_parser("session", help="Session management operations")
    session_sub = session.add_subparsers(dest="session_action", required=True)

    # session stats-update
    ssu = session_sub.add_parser("stats-update", help="Increment session stats in installed.json")
    ssu.set_defaults(func=cmd_session_stats_update)

    # session greeting-state
    sgs = session_sub.add_parser("greeting-state", help="Detect greeting state from sprint/story data")
    sgs.set_defaults(func=cmd_session_greeting_state)

    # session startup-preflight
    ssc = session_sub.add_parser("startup-preflight", help="Consolidated startup routing: versions, hash drift, journal, greeting state")
    ssc.set_defaults(func=cmd_session_startup_preflight)

    # session journal-status
    sjs = session_sub.add_parser("journal-status", help="Scan journal for open threads")
    sjs.set_defaults(func=cmd_session_journal_status)

    # session journal-hygiene
    sjh = session_sub.add_parser("journal-hygiene", help="Return structured hygiene data for all open threads")
    sjh.set_defaults(func=cmd_session_journal_hygiene)

    # session journal-append
    sja = session_sub.add_parser("journal-append", help="Atomic append to journal.jsonl and regenerate view")
    sja.add_argument("--entry", required=True, help="JSON string to append as a new journal line")
    sja.set_defaults(func=cmd_session_journal_append)

    # specialist-classify command
    sc_parser = subparsers.add_parser("specialist-classify", help="Classify touched paths to a dev specialist")
    sc_parser.add_argument("--touches", required=True, help="Comma-separated file paths")
    sc_parser.set_defaults(func=cmd_specialist_classify)

    # quickfix command group
    quickfix = subparsers.add_parser("quickfix", help="Quickfix tracking operations")
    quickfix_sub = quickfix.add_subparsers(dest="quickfix_action", required=True)

    # quickfix register
    qfr = quickfix_sub.add_parser("register", help="Register a new quickfix")
    qfr.add_argument("--slug", required=True, help="Quickfix slug")
    qfr.add_argument("--story", required=True, help="Story key")
    qfr.set_defaults(func=cmd_quickfix_register)

    # quickfix complete
    qfc = quickfix_sub.add_parser("complete", help="Complete a registered quickfix")
    qfc.add_argument("--slug", required=True, help="Quickfix slug")
    qfc.set_defaults(func=cmd_quickfix_complete)

    # intake-queue command group
    iq = subparsers.add_parser("intake-queue", help="Intake queue (intake-queue.jsonl) operations")
    iq_sub = iq.add_subparsers(dest="iq_action", required=True)

    # intake-queue append
    iqa = iq_sub.add_parser("append", help="Append an event to intake-queue.jsonl")
    iqa.add_argument("--source", required=True,
                     choices=sorted(INTAKE_QUEUE_SOURCES),
                     help="Event source (triage|retro|assessment)")
    iqa.add_argument("--kind", required=True,
                     choices=sorted(INTAKE_QUEUE_KINDS),
                     help="Event kind (handoff|shape|watch|rejected)")
    iqa.add_argument("--title", required=True, help="Short title for the event")
    iqa.add_argument("--description", default="", help="Full description")
    iqa.add_argument("--sprint-slug", default=None, help="Retro sprint slug (provenance)")
    iqa.add_argument("--feature-slug", default=None, help="Associated feature slug")
    iqa.add_argument("--story-type", default=None,
                     help="Suggested story type (feature|maintenance|defect|exploration|practice)")
    iqa.add_argument("--feature-state-transition", default=None,
                     help='JSON object: {"feature_slug":"...","prior_state":"...","observed_state":"...","evidence":"..."}')
    iqa.add_argument("--failure-diagnosis", default=None,
                     help='JSON object: {"attempted":"...","didnt_work":"...","learned":"..."}')
    iqa.set_defaults(func=cmd_intake_queue_append)

    # intake-queue list
    iql = iq_sub.add_parser("list", help="List events from intake-queue.jsonl")
    iql.add_argument("--source", default=None, help="Filter by source")
    iql.add_argument("--kind", default=None, help="Filter by kind")
    iql.add_argument("--status", default=None, help="Filter by status (open|consumed)")
    iql.set_defaults(func=cmd_intake_queue_list)

    # intake-queue consume
    iqc = iq_sub.add_parser("consume", help="Mark an event consumed in intake-queue.jsonl")
    iqc.add_argument("--id", required=True, help="Event ID to mark consumed")
    iqc.add_argument("--outcome-ref", default=None,
                     help="Reference to the outcome (story slug, decision ID, etc.)")
    iqc.set_defaults(func=cmd_intake_queue_consume)

    # version command group
    version = subparsers.add_parser("version", help="Version management")
    version_sub = version.add_subparsers(dest="version_action", required=True)

    vc = version_sub.add_parser("check", help="Check version hash")
    vc.set_defaults(func=cmd_version_check)

    # feature-status-hash command
    fsh = subparsers.add_parser("feature-status-hash",
                                help="Compute SHA-256 hash of features.json + stories/index.json")
    fsh.set_defaults(func=cmd_feature_status_hash)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
