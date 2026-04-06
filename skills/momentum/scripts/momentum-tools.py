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
    momentum-tools.py specialist-classify --touches "path1,path2,..."
    momentum-tools.py quickfix register --slug SLUG --story STORY_KEY
    momentum-tools.py quickfix complete --slug SLUG
    momentum-tools.py version check
"""

import argparse
import json
import sys
from datetime import date, datetime
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

    output = {
        "state": state,
        "active_sprint": active_sprint,
        "planning_sprint": planning_sprint,
        "planning_status": planning_status,
        "momentum_completions": momentum_completions,
        "last_completed_sprint": last_completed_sprint,
    }
    result("session_greeting_state", success=True, **output)


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

        greeting = {
            "state": state,
            "active_sprint": active_sprint,
            "planning_sprint": planning_sprint,
            "planning_status": planning_status,
            "momentum_completions": momentum_completions,
            "last_completed_sprint": last_completed_sprint,
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


# --- Log Command ---

VALID_EVENT_TYPES = {"decision", "error", "retry", "assumption", "finding", "ambiguity"}


def cmd_log(args: argparse.Namespace) -> None:
    event = args.event
    if event not in VALID_EVENT_TYPES:
        error_result("log", f"Invalid event type: '{event}'. Must be one of: {', '.join(sorted(VALID_EVENT_TYPES))}")

    project_dir = resolve_project_dir()

    sprint_slug = args.sprint if args.sprint else "_unsorted"
    log_dir = project_dir / ".claude" / "momentum" / "sprint-logs" / sprint_slug
    log_dir.mkdir(parents=True, exist_ok=True)

    if args.story:
        filename = f"{args.agent}-{args.story}.jsonl"
    else:
        filename = f"{args.agent}.jsonl"

    log_file = log_dir / filename

    entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": args.agent,
        "story": args.story if args.story else None,
        "sprint": args.sprint if args.sprint else None,
        "event": event,
        "detail": args.detail,
    }

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    result("log", success=True, file=str(log_file), entry=entry)


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

    # log command group
    log = subparsers.add_parser("log", help="Append structured event to agent log")
    log.add_argument("--agent", required=True, help="Agent role (e.g. dev, pm, architect)")
    log.add_argument("--event", required=True, help="Event type: decision, error, retry, assumption, finding, ambiguity")
    log.add_argument("--detail", required=True, help="Human-readable detail text")
    log.add_argument("--story", default=None, help="Story slug (optional)")
    log.add_argument("--sprint", default=None, help="Sprint slug (optional, defaults to _unsorted)")
    log.set_defaults(func=cmd_log)

    # version command group
    version = subparsers.add_parser("version", help="Version management")
    version_sub = version.add_subparsers(dest="version_action", required=True)

    vc = version_sub.add_parser("check", help="Check version hash")
    vc.set_defaults(func=cmd_version_check)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
