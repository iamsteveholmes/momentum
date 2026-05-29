#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""
Tests for momentum-tools.py — state machine validation and sprint operations.

Run: python3 test-momentum-tools.py
"""

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent / "momentum-tools.py"
PASS_COUNT = 0
FAIL_COUNT = 0


def setup_project(stories: dict | None = None, sprints: dict | None = None) -> Path:
    """Create a temp project directory with .momentum/stories/index.json and .momentum/sprints/index.json."""
    tmpdir = Path(tempfile.mkdtemp())
    stories_dir = tmpdir / ".momentum" / "stories"
    sprints_dir = tmpdir / ".momentum" / "sprints"
    stories_dir.mkdir(parents=True)
    sprints_dir.mkdir(parents=True)

    # Initialize git so project root resolution works
    subprocess.run(["git", "init", "--quiet", str(tmpdir)], check=True)

    if stories is None:
        stories = {
            "test-story": {
                "status": "backlog",
                "title": "Test Story",
                "epic_slug": "test-epic",
                "story_file": False,
                "depends_on": [],
                "touches": []
            },
            "done-story": {
                "status": "done",
                "title": "Done Story",
                "epic_slug": "test-epic",
                "story_file": False,
                "depends_on": [],
                "touches": []
            }
        }
    (stories_dir / "index.json").write_text(json.dumps(stories, indent=2) + "\n")

    if sprints is None:
        sprints = {"active": None, "planning": None, "completed": []}
    (sprints_dir / "index.json").write_text(json.dumps(sprints, indent=2) + "\n")

    return tmpdir


def run_tool(project_dir: Path, *args: str) -> tuple[int, dict]:
    """Run momentum-tools.py and return (exit_code, parsed_json_output)."""
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(project_dir)}
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, env=env
    )
    try:
        output = json.loads(proc.stdout)
    except json.JSONDecodeError:
        output = {"raw_stdout": proc.stdout, "raw_stderr": proc.stderr}
    return proc.returncode, output


def read_stories(project_dir: Path) -> dict:
    path = project_dir / ".momentum" / "stories" / "index.json"
    return json.loads(path.read_text())


def read_sprints(project_dir: Path) -> dict:
    path = project_dir / ".momentum" / "sprints" / "index.json"
    return json.loads(path.read_text())


def assert_eq(test_name: str, actual, expected):
    global PASS_COUNT, FAIL_COUNT
    if actual == expected:
        PASS_COUNT += 1
        print(f"  ✓ {test_name}")
    else:
        FAIL_COUNT += 1
        print(f"  ✗ {test_name}: expected {expected!r}, got {actual!r}")


# --- State Machine Tests ---

def test_valid_forward_transition():
    """Adjacent forward transitions should succeed."""
    print("\n[status-transition] Valid forward transitions")
    transitions = [
        ("backlog", "ready-for-dev"),
        ("ready-for-dev", "in-progress"),
        ("in-progress", "review"),
        ("review", "verify"),
        ("verify", "done"),
    ]
    for current, target in transitions:
        proj = setup_project({"s": {"status": current, "title": "S", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []}})
        code, out = run_tool(proj, "sprint", "status-transition", "--story", "s", "--target", target)
        assert_eq(f"{current} -> {target}", code, 0)
        stories = read_stories(proj)
        assert_eq(f"  file updated to {target}", stories["s"]["status"], target)


def test_invalid_non_adjacent_forward():
    """Non-adjacent forward transitions should fail."""
    print("\n[status-transition] Invalid non-adjacent forward")
    proj = setup_project({"s": {"status": "backlog", "title": "S", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []}})
    code, out = run_tool(proj, "sprint", "status-transition", "--story", "s", "--target", "done")
    assert_eq("backlog -> done rejected", code, 1)
    assert_eq("  file unchanged", read_stories(proj)["s"]["status"], "backlog")


def test_invalid_backward_transition():
    """Backward transitions should fail."""
    print("\n[status-transition] Invalid backward transition")
    proj = setup_project({"s": {"status": "review", "title": "S", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []}})
    code, out = run_tool(proj, "sprint", "status-transition", "--story", "s", "--target", "in-progress")
    assert_eq("review -> in-progress rejected", code, 1)
    assert_eq("  file unchanged", read_stories(proj)["s"]["status"], "review")


def test_terminal_state_blocked():
    """Transitions from terminal states should fail."""
    print("\n[status-transition] Terminal state blocked")
    for state in ["done", "dropped", "closed-incomplete"]:
        proj = setup_project({"s": {"status": state, "title": "S", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []}})
        code, out = run_tool(proj, "sprint", "status-transition", "--story", "s", "--target", "backlog")
        assert_eq(f"{state} -> backlog rejected", code, 1)


def test_force_override():
    """Force flag should bypass all validation."""
    print("\n[status-transition] Force override")
    proj = setup_project({"s": {"status": "done", "title": "S", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []}})
    code, out = run_tool(proj, "sprint", "status-transition", "--story", "s", "--target", "in-progress", "--force")
    assert_eq("done -> in-progress with --force", code, 0)
    assert_eq("  file updated", read_stories(proj)["s"]["status"], "in-progress")


def test_dropped_from_any_non_terminal():
    """dropped is reachable from any non-terminal state."""
    print("\n[status-transition] Dropped from non-terminal")
    for state in ["backlog", "ready-for-dev", "in-progress", "review", "verify"]:
        proj = setup_project({"s": {"status": state, "title": "S", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []}})
        code, out = run_tool(proj, "sprint", "status-transition", "--story", "s", "--target", "dropped")
        assert_eq(f"{state} -> dropped", code, 0)


def test_closed_incomplete_from_any_non_terminal():
    """closed-incomplete is reachable from any non-terminal state."""
    print("\n[status-transition] Closed-incomplete from non-terminal")
    for state in ["backlog", "ready-for-dev", "in-progress", "review", "verify"]:
        proj = setup_project({"s": {"status": state, "title": "S", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []}})
        code, out = run_tool(proj, "sprint", "status-transition", "--story", "s", "--target", "closed-incomplete")
        assert_eq(f"{state} -> closed-incomplete", code, 0)


def test_story_not_found():
    """Transitioning a non-existent story should fail."""
    print("\n[status-transition] Story not found")
    proj = setup_project({})
    code, out = run_tool(proj, "sprint", "status-transition", "--story", "ghost", "--target", "done")
    assert_eq("non-existent story rejected", code, 1)


def test_data_preservation():
    """Status transition should not alter other stories."""
    print("\n[status-transition] Data preservation")
    stories = {
        "a": {"status": "backlog", "title": "A", "epic_slug": "e1", "story_file": True, "depends_on": ["b"], "touches": ["file.md"]},
        "b": {"status": "in-progress", "title": "B", "epic_slug": "e2", "story_file": False, "depends_on": [], "touches": []},
    }
    proj = setup_project(stories)
    run_tool(proj, "sprint", "status-transition", "--story", "a", "--target", "ready-for-dev")
    result = read_stories(proj)
    assert_eq("story a updated", result["a"]["status"], "ready-for-dev")
    assert_eq("story a title preserved", result["a"]["title"], "A")
    assert_eq("story a depends_on preserved", result["a"]["depends_on"], ["b"])
    assert_eq("story a touches preserved", result["a"]["touches"], ["file.md"])
    assert_eq("story b unchanged", result["b"]["status"], "in-progress")
    assert_eq("story b title unchanged", result["b"]["title"], "B")


# --- Sprint Lifecycle Tests ---

def test_sprint_activate():
    """Activating a planning sprint (no stories — approval check passes trivially)."""
    print("\n[sprint activate] Basic activation")
    sprints = {
        "active": None,
        "planning": {"slug": "test-sprint", "name": "Test Sprint", "locked": False,
                     "stories": [], "approvals": []},
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "activate")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("active sprint set", result["active"]["slug"], "test-sprint")
    assert_eq("locked", result["active"]["locked"], True)
    assert_eq("started date set", "started" in result["active"], True)
    assert_eq("planning cleared", result["planning"], None)


def test_sprint_activate_already_active():
    """Cannot activate when an active sprint exists."""
    print("\n[sprint activate] Already active")
    sprints = {
        "active": {"slug": "existing", "locked": True},
        "planning": {"slug": "new", "locked": False},
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "activate")
    assert_eq("rejected", code, 1)


def test_sprint_activate_no_planning():
    """Cannot activate when no planning sprint exists."""
    print("\n[sprint activate] No planning sprint")
    proj = setup_project()
    code, out = run_tool(proj, "sprint", "activate")
    assert_eq("rejected", code, 1)


def test_sprint_complete():
    """Completing an active sprint."""
    print("\n[sprint complete] Basic completion")
    sprints = {
        "active": {"slug": "test-sprint", "name": "Test Sprint", "locked": True, "started": "2026-04-01"},
        "planning": None,
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "complete")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("active cleared", result["active"], None)
    assert_eq("completed has 1 entry", len(result["completed"]), 1)
    assert_eq("completed sprint slug", result["completed"][0]["slug"], "test-sprint")
    assert_eq("completed date set", "completed" in result["completed"][0], True)


def test_sprint_complete_no_active():
    """Cannot complete when no active sprint."""
    print("\n[sprint complete] No active sprint")
    proj = setup_project()
    code, out = run_tool(proj, "sprint", "complete")
    assert_eq("rejected", code, 1)


# --- Epic Membership Tests ---

def test_epic_membership():
    """Change a story's epic."""
    print("\n[epic-membership] Basic change")
    proj = setup_project()
    code, out = run_tool(proj, "sprint", "epic-membership", "--story", "test-story", "--epic", "new-epic")
    assert_eq("exit code 0", code, 0)
    result = read_stories(proj)
    assert_eq("epic updated", result["test-story"]["epic_slug"], "new-epic")
    assert_eq("other story unchanged", result["done-story"]["epic_slug"], "test-epic")


def test_epic_membership_not_found():
    """Cannot change epic of non-existent story."""
    print("\n[epic-membership] Story not found")
    proj = setup_project()
    code, out = run_tool(proj, "sprint", "epic-membership", "--story", "ghost", "--epic", "e")
    assert_eq("rejected", code, 1)


# --- Sprint Plan Tests ---

def test_sprint_plan_add():
    """Add stories to planning sprint."""
    print("\n[sprint plan] Add stories")
    proj = setup_project()
    code, out = run_tool(proj, "sprint", "plan", "--operation", "add", "--stories", "s1,s2", "--wave", "1")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("planning created", result["planning"] is not None, True)
    assert_eq("stories added", set(result["planning"]["stories"]), {"s1", "s2"})
    assert_eq("wave 1 has stories", set(result["planning"]["waves"][0]["stories"]), {"s1", "s2"})


def test_sprint_plan_remove():
    """Remove stories from planning sprint."""
    print("\n[sprint plan] Remove stories")
    sprints = {
        "active": None,
        "planning": {"locked": False, "stories": ["s1", "s2", "s3"], "waves": [{"wave": 1, "stories": ["s1", "s2"]}, {"wave": 2, "stories": ["s3"]}]},
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "plan", "--operation", "remove", "--stories", "s1,s3")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("stories removed", result["planning"]["stories"], ["s2"])
    assert_eq("wave 1 updated", result["planning"]["waves"][0]["stories"], ["s2"])
    assert_eq("empty wave 2 removed", len(result["planning"]["waves"]), 1)


def test_sprint_plan_locked():
    """Cannot modify a locked sprint."""
    print("\n[sprint plan] Locked sprint")
    sprints = {"active": None, "planning": {"locked": True, "stories": []}, "completed": []}
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "plan", "--operation", "add", "--stories", "s1")
    assert_eq("rejected", code, 1)


def test_sprint_plan_no_duplicates():
    """Adding existing stories should not create duplicates."""
    print("\n[sprint plan] No duplicates")
    sprints = {"active": None, "planning": {"locked": False, "stories": ["s1"], "waves": []}, "completed": []}
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "plan", "--operation", "add", "--stories", "s1,s2")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("no duplicate s1", result["planning"]["stories"].count("s1"), 1)
    assert_eq("s2 added", "s2" in result["planning"]["stories"], True)


# --- Helpers for new tests ---

def setup_installed_json(project_dir: Path, data: dict) -> Path:
    """Create .claude/momentum/installed.json in the project dir."""
    installed_dir = project_dir / ".claude" / "momentum"
    installed_dir.mkdir(parents=True, exist_ok=True)
    installed_path = installed_dir / "installed.json"
    installed_path.write_text(json.dumps(data, indent=2) + "\n")
    return installed_path


def read_installed_json(project_dir: Path) -> dict:
    path = project_dir / ".claude" / "momentum" / "installed.json"
    return json.loads(path.read_text())


def setup_versions_json(project_dir: Path, data: dict) -> Path:
    """Create skills/momentum/references/momentum-versions.json."""
    ref_dir = project_dir / "skills" / "momentum" / "references"
    ref_dir.mkdir(parents=True, exist_ok=True)
    versions_path = ref_dir / "momentum-versions.json"
    versions_path.write_text(json.dumps(data, indent=2) + "\n")
    return versions_path


def setup_global_installed(data: dict) -> Path:
    """Create ~/.claude/momentum/global-installed.json (returns path for cleanup)."""
    global_dir = Path.home() / ".claude" / "momentum"
    global_dir.mkdir(parents=True, exist_ok=True)
    global_path = global_dir / "global-installed.json"
    global_path.write_text(json.dumps(data, indent=2) + "\n")
    return global_path


# --- Sprint Status Field Tests ---

def test_sprint_plan_sets_status_planning():
    """sprint plan creates planning entry with status='planning'."""
    print("\n[sprint plan] Sets status planning")
    proj = setup_project()
    code, out = run_tool(proj, "sprint", "plan", "--operation", "add", "--stories", "s1")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("status is planning", result["planning"]["status"], "planning")


def test_sprint_activate_sets_status_active():
    """sprint activate sets active.status='active' (no stories — approval check trivially passes)."""
    print("\n[sprint activate] Sets status active")
    sprints = {
        "active": None,
        "planning": {"slug": "test-sprint", "locked": False, "stories": [], "approvals": []},
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "activate")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("status is active", result["active"]["status"], "active")


def test_sprint_complete_sets_status_done():
    """sprint complete sets active.status='done' and retro_run_at=None."""
    print("\n[sprint complete] Sets status done and retro_run_at null")
    sprints = {
        "active": {"slug": "test-sprint", "locked": True, "started": "2026-04-01"},
        "planning": None,
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "complete")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("status is done", result["completed"][0]["status"], "done")
    assert_eq("retro_run_at is null", result["completed"][0]["retro_run_at"], None)


# --- Sprint Ready Tests ---

def test_sprint_ready_sets_status_ready():
    """sprint ready sets planning.status='ready'."""
    print("\n[sprint ready] Sets status ready")
    sprints = {
        "active": None,
        "planning": {"slug": "test-sprint", "locked": False, "status": "planning", "stories": ["s1"]},
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "ready")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("status is ready", result["planning"]["status"], "ready")


def test_sprint_ready_no_planning():
    """sprint ready fails when no planning sprint exists."""
    print("\n[sprint ready] No planning sprint")
    proj = setup_project()
    code, out = run_tool(proj, "sprint", "ready")
    assert_eq("rejected", code, 1)


# --- Sprint Retro-Complete Tests ---

def test_sprint_retro_complete_basic():
    """sprint retro-complete sets retro_run_at on most recent eligible entry."""
    print("\n[sprint retro-complete] Basic retro completion")
    sprints = {
        "active": None,
        "planning": None,
        "completed": [
            {"slug": "sprint-1", "completed": "2026-03-15", "status": "done", "retro_run_at": "2026-03-16"},
            {"slug": "sprint-2", "completed": "2026-04-01", "status": "done", "retro_run_at": None}
        ]
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "retro-complete")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("sprint-2 retro set", result["completed"][1]["retro_run_at"] is not None, True)
    assert_eq("sprint-1 unchanged", result["completed"][0]["retro_run_at"], "2026-03-16")


def test_sprint_retro_complete_auto_activates():
    """Auto-activates planning sprint when status is 'ready'."""
    print("\n[sprint retro-complete] Auto-activates ready planning sprint")
    sprints = {
        "active": None,
        "planning": {"slug": "next-sprint", "locked": False, "status": "ready", "stories": ["s1"]},
        "completed": [
            {"slug": "sprint-1", "completed": "2026-04-01", "status": "done", "retro_run_at": None}
        ]
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "retro-complete")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("auto_activated", out.get("auto_activated"), True)
    assert_eq("active sprint set", result["active"]["slug"], "next-sprint")
    assert_eq("active status", result["active"]["status"], "active")
    assert_eq("active locked", result["active"]["locked"], True)
    assert_eq("planning cleared", result["planning"], None)


def test_sprint_retro_complete_no_auto_activate_when_planning():
    """Does NOT activate planned sprint when status is 'planning'."""
    print("\n[sprint retro-complete] No auto-activate when status is planning")
    sprints = {
        "active": None,
        "planning": {"slug": "next-sprint", "locked": False, "status": "planning", "stories": ["s1"]},
        "completed": [
            {"slug": "sprint-1", "completed": "2026-04-01", "status": "done", "retro_run_at": None}
        ]
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "retro-complete")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("not auto_activated", out.get("auto_activated"), False)
    assert_eq("planning still exists", result["planning"]["slug"], "next-sprint")
    assert_eq("planning still planning", result["planning"]["status"], "planning")
    assert_eq("active still null", result["active"], None)


def test_sprint_retro_complete_no_completed_sprints():
    """Fails when no completed sprint has retro_run_at unset."""
    print("\n[sprint retro-complete] No eligible completed sprints")
    sprints = {
        "active": None,
        "planning": None,
        "completed": [
            {"slug": "sprint-1", "completed": "2026-03-15", "status": "done", "retro_run_at": "2026-03-16"}
        ]
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "retro-complete")
    assert_eq("rejected", code, 1)


# --- Sprint Next-Stories Tests ---

def test_next_stories_all_unblocked():
    """Returns all stories as ready when no dependencies."""
    print("\n[sprint next-stories] All unblocked")
    stories = {
        "s1": {"status": "backlog", "title": "S1", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
        "s2": {"status": "ready-for-dev", "title": "S2", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
    }
    sprints = {
        "active": {"slug": "test-sprint", "locked": True, "status": "active", "stories": ["s1", "s2"]},
        "planning": None,
        "completed": []
    }
    proj = setup_project(stories=stories, sprints=sprints)
    code, out = run_tool(proj, "sprint", "next-stories")
    assert_eq("exit code 0", code, 0)
    assert_eq("ready has 2", len(out.get("ready", [])), 2)
    assert_eq("blocked empty", len(out.get("blocked", [])), 0)
    assert_eq("done empty", len(out.get("done", [])), 0)


def test_next_stories_some_blocked():
    """Returns correct ready/blocked split based on depends_on."""
    print("\n[sprint next-stories] Some blocked")
    stories = {
        "s1": {"status": "backlog", "title": "S1", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
        "s2": {"status": "backlog", "title": "S2", "epic_slug": "e", "story_file": False, "depends_on": ["s1"], "touches": []},
        "s3": {"status": "backlog", "title": "S3", "epic_slug": "e", "story_file": False, "depends_on": ["s2"], "touches": []},
    }
    sprints = {
        "active": {"slug": "test-sprint", "locked": True, "status": "active", "stories": ["s1", "s2", "s3"]},
        "planning": None,
        "completed": []
    }
    proj = setup_project(stories=stories, sprints=sprints)
    code, out = run_tool(proj, "sprint", "next-stories")
    assert_eq("exit code 0", code, 0)
    assert_eq("s1 is ready", "s1" in out.get("ready", []), True)
    blocked_slugs = [b["slug"] for b in out.get("blocked", [])]
    assert_eq("s2 is blocked", "s2" in blocked_slugs, True)
    assert_eq("s3 is blocked", "s3" in blocked_slugs, True)
    # Check waiting_on for s2
    s2_blocked = [b for b in out["blocked"] if b["slug"] == "s2"][0]
    assert_eq("s2 waiting on s1", s2_blocked["waiting_on"], ["s1"])


def test_next_stories_done_excluded():
    """Done stories not in ready or blocked lists."""
    print("\n[sprint next-stories] Done excluded")
    stories = {
        "s1": {"status": "done", "title": "S1", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
        "s2": {"status": "backlog", "title": "S2", "epic_slug": "e", "story_file": False, "depends_on": ["s1"], "touches": []},
    }
    sprints = {
        "active": {"slug": "test-sprint", "locked": True, "status": "active", "stories": ["s1", "s2"]},
        "planning": None,
        "completed": []
    }
    proj = setup_project(stories=stories, sprints=sprints)
    code, out = run_tool(proj, "sprint", "next-stories")
    assert_eq("exit code 0", code, 0)
    assert_eq("s1 in done", "s1" in out.get("done", []), True)
    assert_eq("s2 is ready (dep done)", "s2" in out.get("ready", []), True)
    assert_eq("blocked empty", len(out.get("blocked", [])), 0)


def test_next_stories_no_active_sprint():
    """Fails when no active sprint exists."""
    print("\n[sprint next-stories] No active sprint")
    proj = setup_project()
    code, out = run_tool(proj, "sprint", "next-stories")
    assert_eq("rejected", code, 1)


# --- Session Stats-Update Tests ---

def test_session_stats_update_creates():
    """session stats-update creates session_stats when absent."""
    print("\n[session stats-update] Creates session_stats")
    proj = setup_project()
    setup_installed_json(proj, {"version": "1.0.0", "hash": "abc123"})
    code, out = run_tool(proj, "session", "stats-update")
    assert_eq("exit code 0", code, 0)
    data = read_installed_json(proj)
    assert_eq("session_stats created", "session_stats" in data, True)
    assert_eq("completions is 1", data["session_stats"]["momentum_completions"], 1)
    assert_eq("last_invocation set", data["session_stats"]["last_invocation"] is not None, True)


def test_session_stats_update_increments():
    """session stats-update increments momentum_completions."""
    print("\n[session stats-update] Increments completions")
    proj = setup_project()
    setup_installed_json(proj, {
        "version": "1.0.0",
        "session_stats": {"momentum_completions": 5, "last_invocation": "2026-04-01"}
    })
    code, out = run_tool(proj, "session", "stats-update")
    assert_eq("exit code 0", code, 0)
    data = read_installed_json(proj)
    assert_eq("completions incremented", data["session_stats"]["momentum_completions"], 6)


def test_session_stats_update_preserves_data():
    """session stats-update does not alter components or other fields."""
    print("\n[session stats-update] Preserves other data")
    proj = setup_project()
    original = {
        "version": "1.0.0",
        "hash": "abc123",
        "components": {"rules": {"version": "1.0.0"}},
        "session_stats": {"momentum_completions": 2, "last_invocation": "2026-04-01"}
    }
    setup_installed_json(proj, original)
    code, out = run_tool(proj, "session", "stats-update")
    assert_eq("exit code 0", code, 0)
    data = read_installed_json(proj)
    assert_eq("version preserved", data["version"], "1.0.0")
    assert_eq("hash preserved", data["hash"], "abc123")
    assert_eq("components preserved", data["components"], {"rules": {"version": "1.0.0"}})
    assert_eq("completions incremented", data["session_stats"]["momentum_completions"], 3)


# --- Session Greeting-State Tests ---

def test_greeting_state_first_session():
    """Returns 'first-session-ever' when no sprints and completions == 0."""
    print("\n[session greeting-state] First session ever")
    proj = setup_project()
    # No installed.json — completions defaults to 0
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "first-session-ever")
    assert_eq("active_sprint null", out.get("active_sprint"), None)
    assert_eq("completions 0", out.get("momentum_completions"), 0)


def test_greeting_state_active_in_progress():
    """Returns 'active-in-progress' with stories moving."""
    print("\n[session greeting-state] Active in progress")
    stories = {
        "s1": {"status": "in-progress", "title": "S1", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
        "s2": {"status": "backlog", "title": "S2", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
    }
    sprints = {
        "active": {"slug": "test-sprint", "status": "active", "locked": True, "stories": ["s1", "s2"]},
        "planning": None,
        "completed": []
    }
    proj = setup_project(stories=stories, sprints=sprints)
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 1, "last_invocation": "2026-04-01"}})
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "active-in-progress")
    assert_eq("active_sprint", out.get("active_sprint"), "test-sprint")


def test_greeting_state_active_not_started():
    """Returns 'active-not-started' when all stories ready-for-dev."""
    print("\n[session greeting-state] Active not started")
    stories = {
        "s1": {"status": "ready-for-dev", "title": "S1", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
        "s2": {"status": "backlog", "title": "S2", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
    }
    sprints = {
        "active": {"slug": "test-sprint", "status": "active", "locked": True, "stories": ["s1", "s2"]},
        "planning": None,
        "completed": []
    }
    proj = setup_project(stories=stories, sprints=sprints)
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 1, "last_invocation": "2026-04-01"}})
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "active-not-started")


def test_greeting_state_active_blocked():
    """Returns 'active-blocked' when story has unmet depends_on."""
    print("\n[session greeting-state] Active blocked")
    stories = {
        "s1": {"status": "backlog", "title": "S1", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
        "s2": {"status": "backlog", "title": "S2", "epic_slug": "e", "story_file": False, "depends_on": ["s1"], "touches": []},
    }
    sprints = {
        "active": {"slug": "test-sprint", "status": "active", "locked": True, "stories": ["s1", "s2"]},
        "planning": None,
        "completed": []
    }
    proj = setup_project(stories=stories, sprints=sprints)
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 1, "last_invocation": "2026-04-01"}})
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "active-blocked")


def test_greeting_state_done_retro_needed():
    """Returns 'done-retro-needed' when active.status == 'done'."""
    print("\n[session greeting-state] Done retro needed")
    sprints = {
        "active": {"slug": "test-sprint", "status": "done", "locked": True, "stories": ["s1"]},
        "planning": {"slug": "next-sprint", "status": "ready", "locked": False, "stories": ["s2"]},
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 3, "last_invocation": "2026-04-01"}})
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "done-retro-needed")


def test_greeting_state_no_active_nothing_planned():
    """Returns correct state when both null."""
    print("\n[session greeting-state] No active, nothing planned")
    sprints = {
        "active": None,
        "planning": None,
        "completed": [{"slug": "old-sprint", "completed": "2026-03-15"}]
    }
    proj = setup_project(sprints=sprints)
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 5, "last_invocation": "2026-04-01"}})
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "no-active-nothing-planned")
    assert_eq("last_completed_sprint", out.get("last_completed_sprint"), "old-sprint")


def test_greeting_state_no_active_planned_ready():
    """Returns correct state with ready planning sprint."""
    print("\n[session greeting-state] No active, planned ready")
    sprints = {
        "active": None,
        "planning": {"slug": "next-sprint", "status": "ready", "locked": False, "stories": ["s1"]},
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 2, "last_invocation": "2026-04-01"}})
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "no-active-planned-ready")
    assert_eq("planning_sprint", out.get("planning_sprint"), "next-sprint")
    assert_eq("planning_status", out.get("planning_status"), "ready")


def test_greeting_state_active_planned_needs_work():
    """Returns correct state with planning sprint in 'planning'."""
    print("\n[session greeting-state] Active, planned needs work")
    stories = {
        "s1": {"status": "in-progress", "title": "S1", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
    }
    sprints = {
        "active": {"slug": "test-sprint", "status": "active", "locked": True, "stories": ["s1"]},
        "planning": {"slug": "next-sprint", "status": "planning", "locked": False, "stories": []},
        "completed": []
    }
    proj = setup_project(stories=stories, sprints=sprints)
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 3, "last_invocation": "2026-04-01"}})
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "active-planned-needs-work")


def test_greeting_state_done_no_planned():
    """Returns 'done-no-planned' when done and no planning sprint."""
    print("\n[session greeting-state] Done, no planned")
    sprints = {
        "active": {"slug": "test-sprint", "status": "done", "locked": True, "stories": ["s1"]},
        "planning": None,
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 3, "last_invocation": "2026-04-01"}})
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "done-no-planned")


# --- Session Startup-Preflight Tests ---


def _with_global_installed(data: dict, fn):
    """Run fn with a temporary global-installed.json, restoring the original after."""
    global_path = Path.home() / ".claude" / "momentum" / "global-installed.json"
    backup = None
    if global_path.exists():
        backup = global_path.read_text()
    global_path.parent.mkdir(parents=True, exist_ok=True)
    global_path.write_text(json.dumps(data, indent=2) + "\n")
    try:
        fn()
    finally:
        if backup is not None:
            global_path.write_text(backup)
        else:
            global_path.unlink(missing_ok=True)


def test_startup_preflight_all_current():
    """Route is 'greeting' when all component versions match current_version."""
    print("\n[session startup-preflight] All current — route greeting")
    proj = setup_project()
    setup_versions_json(proj, {
        "current_version": "1.0.0",
        "versions": {
            "1.0.0": {
                "actions": [
                    {"action": "add", "group": "rules", "scope": "global", "source": "rules/a.md", "target": "~/.claude/rules/a.md"},
                    {"action": "migration", "group": "hooks", "scope": "project", "source": "m.md", "description": "hooks"}
                ]
            }
        }
    })
    setup_installed_json(proj, {"components": {"hooks": {"version": "1.0.0"}}})

    def check():
        code, out = run_tool(proj, "session", "startup-preflight")
        assert_eq("exit code 0", code, 0)
        assert_eq("route", out.get("route"), "greeting")
        assert_eq("needs_work empty", out.get("needs_work"), [])
        assert_eq("hash_drift false", out.get("hash_drift"), False)
        assert_eq("greeting present", out.get("greeting") is not None, True)
        assert_eq("current_version", out.get("current_version"), "1.0.0")

    _with_global_installed({"components": {"rules": {"version": "1.0.0", "hash": ""}}}, check)


def test_startup_preflight_needs_upgrade():
    """Route is 'upgrade' when a component version is behind current_version."""
    print("\n[session startup-preflight] Needs upgrade")
    proj = setup_project()
    setup_versions_json(proj, {
        "current_version": "2.0.0",
        "versions": {
            "2.0.0": {
                "actions": [
                    {"action": "replace", "group": "rules", "scope": "global", "source": "rules/a.md", "target": "~/.claude/rules/a.md"},
                    {"action": "migration", "group": "hooks", "scope": "project", "source": "m.md", "description": "hooks"}
                ]
            }
        }
    })
    setup_installed_json(proj, {"components": {"hooks": {"version": "1.0.0"}}})

    def check():
        code, out = run_tool(proj, "session", "startup-preflight")
        assert_eq("exit code 0", code, 0)
        assert_eq("route", out.get("route"), "upgrade")
        assert_eq("needs_work non-empty", len(out.get("needs_work", [])) > 0, True)
        assert_eq("current_version", out.get("current_version"), "2.0.0")

    _with_global_installed({"components": {"rules": {"version": "1.0.0"}}}, check)


def test_startup_preflight_hash_drift():
    """Route is 'hash-drift' when file hash mismatches stored hash."""
    print("\n[session startup-preflight] Hash drift detected")
    proj = setup_project()

    # Create a target file for hash checking
    rules_dir = Path.home() / ".claude" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    target_file = rules_dir / "test-drift-target.md"
    target_file.write_text("# Modified content\n")

    setup_versions_json(proj, {
        "current_version": "1.0.0",
        "versions": {
            "1.0.0": {
                "actions": [
                    {"action": "add", "group": "test-drift", "scope": "global",
                     "source": "rules/a.md", "target": str(target_file)},
                    {"action": "migration", "group": "hooks", "scope": "project",
                     "source": "m.md", "description": "hooks"}
                ]
            }
        }
    })
    setup_installed_json(proj, {"components": {"hooks": {"version": "1.0.0"}}})

    def check():
        code, out = run_tool(proj, "session", "startup-preflight")
        assert_eq("exit code 0", code, 0)
        assert_eq("route", out.get("route"), "hash-drift")
        assert_eq("hash_drift true", out.get("hash_drift"), True)

    _with_global_installed({
        "components": {
            "test-drift": {"version": "1.0.0", "hash": "wrong-hash-value"}
        }
    }, check)

    # Clean up target file
    target_file.unlink(missing_ok=True)


def test_startup_preflight_first_install():
    """Route is 'first-install' when no installed.json and no global components."""
    print("\n[session startup-preflight] First install")
    proj = setup_project()
    setup_versions_json(proj, {
        "current_version": "1.0.0",
        "versions": {
            "1.0.0": {
                "actions": [
                    {"action": "add", "group": "rules", "scope": "global", "source": "rules/a.md", "target": "~/.claude/rules/a.md"},
                    {"action": "migration", "group": "hooks", "scope": "project", "source": "m.md", "description": "hooks"}
                ]
            }
        }
    })
    # Do NOT create installed.json

    def check():
        code, out = run_tool(proj, "session", "startup-preflight")
        assert_eq("exit code 0", code, 0)
        assert_eq("route", out.get("route"), "first-install")
        assert_eq("needs_work non-empty", len(out.get("needs_work", [])) > 0, True)

    _with_global_installed({}, check)


def test_startup_preflight_journal_threads():
    """has_open_threads is true when journal.jsonl has open threads."""
    print("\n[session startup-preflight] Open journal threads")
    proj = setup_project()
    setup_versions_json(proj, {
        "current_version": "1.0.0",
        "versions": {
            "1.0.0": {
                "actions": [
                    {"action": "add", "group": "rules", "scope": "global", "source": "rules/a.md", "target": "~/.claude/rules/a.md"},
                    {"action": "migration", "group": "hooks", "scope": "project", "source": "m.md", "description": "hooks"}
                ]
            }
        }
    })
    setup_installed_json(proj, {"components": {"hooks": {"version": "1.0.0"}}})

    # Create journal with an open thread
    journal_dir = proj / ".claude" / "momentum"
    journal_dir.mkdir(parents=True, exist_ok=True)
    journal_path = journal_dir / "journal.jsonl"
    journal_path.write_text(json.dumps({
        "thread_id": "T-001", "status": "open",
        "context_summary": "Test thread", "context_summary_short": "Test",
        "last_active": "2026-04-04T00:00:00Z"
    }) + "\n")

    def check():
        code, out = run_tool(proj, "session", "startup-preflight")
        assert_eq("exit code 0", code, 0)
        assert_eq("has_open_threads", out.get("has_open_threads"), True)

    _with_global_installed({"components": {"rules": {"version": "1.0.0", "hash": ""}}}, check)


# --- Specialist Classify Tests ---

def test_specialist_classify_dev_skills():
    """Single path matching dev-skills."""
    print("\n[specialist-classify] Single path — dev-skills")
    proj = setup_project()
    # Create the agent file so fallback is false
    agent_dir = proj / "skills" / "momentum" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "dev-skills.md").write_text("# dev-skills\n")
    code, out = run_tool(proj, "specialist-classify", "--touches", "skills/momentum/SKILL.md")
    assert_eq("exit code 0", code, 0)
    assert_eq("specialist", out.get("specialist"), "dev-skills")
    assert_eq("fallback false", out.get("fallback"), False)
    assert_eq("matches", out.get("matches"), {"dev-skills": 1})


def test_specialist_classify_dev_build():
    """Single path matching dev-build."""
    print("\n[specialist-classify] Single path — dev-build")
    proj = setup_project()
    agent_dir = proj / "skills" / "momentum" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "dev-build.md").write_text("# dev-build\n")
    code, out = run_tool(proj, "specialist-classify", "--touches", "app/build.gradle.kts")
    assert_eq("exit code 0", code, 0)
    assert_eq("specialist", out.get("specialist"), "dev-build")
    assert_eq("fallback false", out.get("fallback"), False)


def test_specialist_classify_dev_frontend():
    """Single path matching dev-frontend."""
    print("\n[specialist-classify] Single path — dev-frontend")
    proj = setup_project()
    agent_dir = proj / "skills" / "momentum" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "dev-frontend.md").write_text("# dev-frontend\n")
    code, out = run_tool(proj, "specialist-classify", "--touches", "app/src/main/ui/HomeScreen.kt")
    assert_eq("exit code 0", code, 0)
    assert_eq("specialist", out.get("specialist"), "dev-frontend")
    assert_eq("fallback false", out.get("fallback"), False)


def test_specialist_classify_no_match():
    """No match returns dev base."""
    print("\n[specialist-classify] No match — dev base")
    proj = setup_project()
    agent_dir = proj / "skills" / "momentum" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "dev.md").write_text("# dev\n")
    code, out = run_tool(proj, "specialist-classify", "--touches", "README.md,src/main.py")
    assert_eq("exit code 0", code, 0)
    assert_eq("specialist", out.get("specialist"), "dev")
    assert_eq("matches empty", out.get("matches"), {})
    assert_eq("fallback false", out.get("fallback"), False)


def test_specialist_classify_majority_rule():
    """Multiple paths — majority wins."""
    print("\n[specialist-classify] Majority rule")
    proj = setup_project()
    agent_dir = proj / "skills" / "momentum" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "dev-skills.md").write_text("# dev-skills\n")
    (agent_dir / "dev-build.md").write_text("# dev-build\n")
    touches = "skills/foo/SKILL.md,skills/bar/SKILL.md,skills/baz/workflow.md,build.gradle.kts"
    code, out = run_tool(proj, "specialist-classify", "--touches", touches)
    assert_eq("exit code 0", code, 0)
    assert_eq("specialist", out.get("specialist"), "dev-skills")
    assert_eq("dev-skills count", out.get("matches", {}).get("dev-skills"), 3)
    assert_eq("dev-build count", out.get("matches", {}).get("dev-build"), 1)


def test_specialist_classify_tie_table_order():
    """Tie broken by table order — dev-skills wins over dev-build."""
    print("\n[specialist-classify] Tie — table order wins")
    proj = setup_project()
    agent_dir = proj / "skills" / "momentum" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "dev-skills.md").write_text("# dev-skills\n")
    (agent_dir / "dev-build.md").write_text("# dev-build\n")
    touches = "skills/foo/SKILL.md,build.gradle.kts"
    code, out = run_tool(proj, "specialist-classify", "--touches", touches)
    assert_eq("exit code 0", code, 0)
    assert_eq("specialist", out.get("specialist"), "dev-skills")
    assert_eq("dev-skills count", out.get("matches", {}).get("dev-skills"), 1)
    assert_eq("dev-build count", out.get("matches", {}).get("dev-build"), 1)


def test_specialist_classify_empty_touches():
    """Empty touches returns dev base."""
    print("\n[specialist-classify] Empty touches — dev base")
    proj = setup_project()
    code, out = run_tool(proj, "specialist-classify", "--touches", "")
    assert_eq("exit code 0", code, 0)
    assert_eq("specialist", out.get("specialist"), "dev")
    assert_eq("matches empty", out.get("matches"), {})


def test_specialist_classify_fallback_missing_agent():
    """Agent file missing on disk sets fallback: true."""
    print("\n[specialist-classify] Fallback — agent file missing")
    proj = setup_project()
    # Do NOT create any agent files
    code, out = run_tool(proj, "specialist-classify", "--touches", "skills/foo/SKILL.md")
    assert_eq("exit code 0", code, 0)
    assert_eq("specialist", out.get("specialist"), "dev-skills")
    assert_eq("fallback true", out.get("fallback"), True)
    assert_eq("agent_file falls back to dev", out.get("agent_file"), "skills/momentum/agents/dev.md")


# --- Quickfix Tests ---

def test_quickfix_register_creates_array():
    """Register creates quickfixes array if absent."""
    print("\n[quickfix register] Creates quickfixes array")
    sprints = {"active": None, "planning": None, "completed": []}
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "quickfix", "register", "--slug", "qf-2026-04-05", "--story", "quick-fix-skill")
    assert_eq("exit code 0", code, 0)
    data = read_sprints(proj)
    assert_eq("quickfixes key exists", "quickfixes" in data, True)
    assert_eq("one entry", len(data["quickfixes"]), 1)


def test_quickfix_register_correct_fields():
    """Register adds entry with correct fields."""
    print("\n[quickfix register] Correct fields")
    sprints = {"active": None, "planning": None, "completed": []}
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "quickfix", "register", "--slug", "qf-2026-04-05", "--story", "quick-fix-skill")
    assert_eq("exit code 0", code, 0)
    data = read_sprints(proj)
    entry = data["quickfixes"][0]
    assert_eq("slug", entry["slug"], "qf-2026-04-05")
    assert_eq("story", entry["story"], "quick-fix-skill")
    assert_eq("started present", "started" in entry, True)
    assert_eq("no completed yet", "completed" not in entry, True)


def test_quickfix_register_auto_increment():
    """Register auto-increments duplicate slugs."""
    print("\n[quickfix register] Auto-increment duplicates")
    sprints = {
        "active": None, "planning": None, "completed": [],
        "quickfixes": [{"slug": "qf-2026-04-05", "story": "s1", "started": "2026-04-05"}]
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "quickfix", "register", "--slug", "qf-2026-04-05", "--story", "s2")
    assert_eq("exit code 0", code, 0)
    assert_eq("resolved slug incremented", out.get("slug"), "qf-2026-04-05-2")
    data = read_sprints(proj)
    assert_eq("two entries", len(data["quickfixes"]), 2)


def test_quickfix_register_empty_story():
    """Register rejects if story key is empty."""
    print("\n[quickfix register] Rejects empty story")
    sprints = {"active": None, "planning": None, "completed": []}
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "quickfix", "register", "--slug", "qf-1", "--story", "")
    assert_eq("rejected", code, 1)
    assert_eq("error reported", out.get("success"), False)


def test_quickfix_complete_sets_date():
    """Complete sets completed date."""
    print("\n[quickfix complete] Sets completed date")
    sprints = {
        "active": None, "planning": None, "completed": [],
        "quickfixes": [{"slug": "qf-1", "story": "s1", "started": "2026-04-05"}]
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "quickfix", "complete", "--slug", "qf-1")
    assert_eq("exit code 0", code, 0)
    data = read_sprints(proj)
    assert_eq("completed date set", "completed" in data["quickfixes"][0], True)
    assert_eq("slug in output", out.get("slug"), "qf-1")


def test_quickfix_complete_missing_slug():
    """Complete errors on missing slug."""
    print("\n[quickfix complete] Errors on missing slug")
    sprints = {"active": None, "planning": None, "completed": [], "quickfixes": []}
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "quickfix", "complete", "--slug", "ghost")
    assert_eq("rejected", code, 1)
    assert_eq("error reported", out.get("success"), False)


def test_quickfix_complete_idempotent():
    """Complete is idempotent — re-completing already-completed is fine."""
    print("\n[quickfix complete] Idempotent re-complete")
    sprints = {
        "active": None, "planning": None, "completed": [],
        "quickfixes": [{"slug": "qf-1", "story": "s1", "started": "2026-04-05", "completed": "2026-04-05"}]
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "quickfix", "complete", "--slug", "qf-1")
    assert_eq("exit code 0", code, 0)
    data = read_sprints(proj)
    assert_eq("completed still present", "completed" in data["quickfixes"][0], True)


def test_quickfix_round_trip():
    """Register + complete round-trip."""
    print("\n[quickfix] Register + complete round-trip")
    sprints = {"active": None, "planning": None, "completed": []}
    proj = setup_project(sprints=sprints)
    # Register
    code1, out1 = run_tool(proj, "quickfix", "register", "--slug", "qf-rt", "--story", "my-story")
    assert_eq("register ok", code1, 0)
    resolved_slug = out1.get("slug", "qf-rt")
    # Complete
    code2, out2 = run_tool(proj, "quickfix", "complete", "--slug", resolved_slug)
    assert_eq("complete ok", code2, 0)
    data = read_sprints(proj)
    entry = data["quickfixes"][0]
    assert_eq("slug matches", entry["slug"], "qf-rt")
    assert_eq("story matches", entry["story"], "my-story")
    assert_eq("started present", "started" in entry, True)
    assert_eq("completed present", "completed" in entry, True)


# --- Priority Field Tests ---

def test_priority_default_on_new_entry():
    """New stories written without priority get 'low' by default via migration."""
    print("\n[priority] Default priority on entries without field")
    stories = {
        "no-priority": {"status": "backlog", "title": "No Priority", "epic_slug": "e",
                        "story_file": False, "depends_on": [], "touches": []},
        "has-priority": {"status": "backlog", "title": "Has Priority", "epic_slug": "e",
                         "story_file": False, "depends_on": [], "touches": [], "priority": "high"},
    }
    proj = setup_project(stories=stories)
    # Run migrate to populate missing priority fields
    code, out = run_tool(proj, "sprint", "migrate-priority")
    assert_eq("exit code 0", code, 0)
    data = read_stories(proj)
    assert_eq("no-priority gets low", data["no-priority"]["priority"], "low")
    assert_eq("has-priority unchanged", data["has-priority"]["priority"], "high")


def test_priority_migrate_idempotent():
    """Migration is idempotent — running twice doesn't corrupt data."""
    print("\n[priority] Migration is idempotent")
    stories = {
        "s1": {"status": "backlog", "title": "S1", "epic_slug": "e",
               "story_file": False, "depends_on": [], "touches": []},
    }
    proj = setup_project(stories=stories)
    run_tool(proj, "sprint", "migrate-priority")
    run_tool(proj, "sprint", "migrate-priority")
    data = read_stories(proj)
    assert_eq("s1 has low priority after two runs", data["s1"]["priority"], "low")


def test_set_priority_valid():
    """set-priority sets a valid priority value."""
    print("\n[set-priority] Valid priority set")
    stories = {
        "my-story": {"status": "backlog", "title": "My Story", "epic_slug": "e",
                     "story_file": False, "depends_on": [], "touches": [], "priority": "low"},
    }
    proj = setup_project(stories=stories)
    code, out = run_tool(proj, "sprint", "set-priority", "--story", "my-story", "--priority", "high")
    assert_eq("exit code 0", code, 0)
    assert_eq("success true", out.get("success"), True)
    assert_eq("old_priority", out.get("old_priority"), "low")
    assert_eq("new_priority", out.get("new_priority"), "high")
    data = read_stories(proj)
    assert_eq("file updated", data["my-story"]["priority"], "high")


def test_set_priority_all_valid_levels():
    """All four priority levels are accepted."""
    print("\n[set-priority] All valid levels accepted")
    for level in ["critical", "high", "medium", "low"]:
        stories = {
            "s": {"status": "backlog", "title": "S", "epic_slug": "e",
                  "story_file": False, "depends_on": [], "touches": [], "priority": "low"},
        }
        proj = setup_project(stories=stories)
        code, out = run_tool(proj, "sprint", "set-priority", "--story", "s", "--priority", level)
        assert_eq(f"level {level} accepted", code, 0)


def test_set_priority_invalid_level():
    """Invalid priority level is rejected with exit code 1."""
    print("\n[set-priority] Invalid level rejected")
    stories = {
        "s": {"status": "backlog", "title": "S", "epic_slug": "e",
              "story_file": False, "depends_on": [], "touches": [], "priority": "low"},
    }
    proj = setup_project(stories=stories)
    code, out = run_tool(proj, "sprint", "set-priority", "--story", "s", "--priority", "urgent")
    assert_eq("rejected", code, 1)
    assert_eq("success false", out.get("success"), False)
    data = read_stories(proj)
    assert_eq("file unchanged", data["s"]["priority"], "low")


def test_set_priority_missing_story():
    """set-priority fails when story slug doesn't exist."""
    print("\n[set-priority] Missing story slug")
    proj = setup_project()
    code, out = run_tool(proj, "sprint", "set-priority", "--story", "ghost", "--priority", "high")
    assert_eq("rejected", code, 1)
    assert_eq("success false", out.get("success"), False)


def test_set_priority_idempotent():
    """Setting the same priority twice is safe."""
    print("\n[set-priority] Idempotent — same priority twice")
    stories = {
        "s": {"status": "backlog", "title": "S", "epic_slug": "e",
              "story_file": False, "depends_on": [], "touches": [], "priority": "medium"},
    }
    proj = setup_project(stories=stories)
    code1, out1 = run_tool(proj, "sprint", "set-priority", "--story", "s", "--priority", "medium")
    assert_eq("first set exit 0", code1, 0)
    assert_eq("old_priority same", out1.get("old_priority"), "medium")
    assert_eq("new_priority same", out1.get("new_priority"), "medium")
    data = read_stories(proj)
    assert_eq("file still medium", data["s"]["priority"], "medium")


def test_sprint_stories_single_priority():
    """stories --priority filters to matching stories only."""
    print("\n[sprint stories] Single priority filter")
    stories = {
        "crit": {"status": "backlog", "title": "Critical Story", "epic_slug": "e",
                 "story_file": False, "depends_on": [], "touches": [], "priority": "critical"},
        "high": {"status": "backlog", "title": "High Story", "epic_slug": "e",
                 "story_file": False, "depends_on": [], "touches": [], "priority": "high"},
        "low": {"status": "backlog", "title": "Low Story", "epic_slug": "e",
                "story_file": False, "depends_on": [], "touches": [], "priority": "low"},
    }
    proj = setup_project(stories=stories)
    code, out = run_tool(proj, "sprint", "stories", "--priority", "high")
    assert_eq("exit code 0", code, 0)
    assert_eq("success true", out.get("success"), True)
    slugs = [s["slug"] for s in out.get("stories", [])]
    assert_eq("high story present", "high" in slugs, True)
    assert_eq("crit story absent", "crit" in slugs, False)
    assert_eq("low story absent", "low" in slugs, False)


def test_sprint_stories_all_grouped():
    """stories --priority all returns stories grouped critical→high→medium→low."""
    print("\n[sprint stories] All grouped by priority")
    stories = {
        "c1": {"status": "backlog", "title": "C1", "epic_slug": "e",
               "story_file": False, "depends_on": [], "touches": [], "priority": "critical"},
        "h1": {"status": "backlog", "title": "H1", "epic_slug": "e",
               "story_file": False, "depends_on": [], "touches": [], "priority": "high"},
        "m1": {"status": "backlog", "title": "M1", "epic_slug": "e",
               "story_file": False, "depends_on": [], "touches": [], "priority": "medium"},
        "l1": {"status": "backlog", "title": "L1", "epic_slug": "e",
               "story_file": False, "depends_on": [], "touches": [], "priority": "low"},
    }
    proj = setup_project(stories=stories)
    code, out = run_tool(proj, "sprint", "stories", "--priority", "all")
    assert_eq("exit code 0", code, 0)
    groups = out.get("groups", {})
    assert_eq("critical group exists", "critical" in groups, True)
    assert_eq("high group exists", "high" in groups, True)
    assert_eq("medium group exists", "medium" in groups, True)
    assert_eq("low group exists", "low" in groups, True)
    assert_eq("c1 in critical", "c1" in [s["slug"] for s in groups.get("critical", [])], True)
    assert_eq("h1 in high", "h1" in [s["slug"] for s in groups.get("high", [])], True)
    assert_eq("m1 in medium", "m1" in [s["slug"] for s in groups.get("medium", [])], True)
    assert_eq("l1 in low", "l1" in [s["slug"] for s in groups.get("low", [])], True)


def test_sprint_stories_invalid_priority():
    """stories --priority rejects invalid priority level with exit code 1."""
    print("\n[sprint stories] Invalid priority level rejected")
    stories = {
        "s1": {"status": "backlog", "title": "S1", "epic_slug": "e",
               "story_file": False, "depends_on": [], "touches": [], "priority": "low"},
    }
    proj = setup_project(stories=stories)
    code, out = run_tool(proj, "sprint", "stories", "--priority", "urgent")
    assert_eq("rejected", code, 1)
    assert_eq("success false", out.get("success"), False)


def test_sprint_stories_empty_results():
    """stories --priority returns empty list when no stories match."""
    print("\n[sprint stories] Empty results")
    stories = {
        "s1": {"status": "backlog", "title": "S1", "epic_slug": "e",
               "story_file": False, "depends_on": [], "touches": [], "priority": "low"},
    }
    proj = setup_project(stories=stories)
    code, out = run_tool(proj, "sprint", "stories", "--priority", "critical")
    assert_eq("exit code 0", code, 0)
    assert_eq("stories empty", out.get("stories"), [])


def test_sprint_stories_missing_priority_defaults_low():
    """stories query treats entries without priority field as 'low'."""
    print("\n[sprint stories] Missing priority field defaults to low")
    stories = {
        "no-field": {"status": "backlog", "title": "No Field", "epic_slug": "e",
                     "story_file": False, "depends_on": [], "touches": []},
    }
    proj = setup_project(stories=stories)
    code, out = run_tool(proj, "sprint", "stories", "--priority", "low")
    assert_eq("exit code 0", code, 0)
    slugs = [s["slug"] for s in out.get("stories", [])]
    assert_eq("no-field treated as low", "no-field" in slugs, True)


# --- Journal Status Tests ---

def setup_journal(project_dir: Path, lines: list[str]) -> Path:
    """Create .claude/momentum/journal.jsonl with given lines."""
    journal_dir = project_dir / ".claude" / "momentum"
    journal_dir.mkdir(parents=True, exist_ok=True)
    journal_path = journal_dir / "journal.jsonl"
    journal_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return journal_path


def test_journal_status_no_file():
    """Returns exists: false when journal.jsonl absent."""
    print("\n[session journal-status] No file")
    proj = setup_project()
    # Do NOT create journal.jsonl
    code, out = run_tool(proj, "session", "journal-status")
    assert_eq("exit code 0", code, 0)
    assert_eq("exists false", out.get("exists"), False)
    assert_eq("open_threads 0", out.get("open_threads"), 0)
    assert_eq("last_entry null", out.get("last_entry"), None)


def test_journal_status_empty_file():
    """Returns exists: true, open_threads: 0 for an empty file."""
    print("\n[session journal-status] Empty file")
    proj = setup_project()
    setup_journal(proj, [])
    code, out = run_tool(proj, "session", "journal-status")
    assert_eq("exit code 0", code, 0)
    assert_eq("exists true", out.get("exists"), True)
    assert_eq("open_threads 0", out.get("open_threads"), 0)
    assert_eq("total_entries 0", out.get("total_entries"), 0)
    assert_eq("parse_errors 0", out.get("parse_errors"), 0)


def test_journal_status_open_threads():
    """Correctly counts open threads (last event not terminal)."""
    print("\n[session journal-status] Open threads")
    proj = setup_project()
    lines = [
        json.dumps({"timestamp": "2026-04-05T10:00:00", "event": "thread_open", "thread_id": "t1"}),
        json.dumps({"timestamp": "2026-04-05T10:01:00", "event": "decision", "thread_id": "t1"}),
        json.dumps({"timestamp": "2026-04-05T10:02:00", "event": "thread_open", "thread_id": "t2"}),
        json.dumps({"timestamp": "2026-04-05T10:03:00", "event": "finding", "thread_id": "t2"}),
    ]
    setup_journal(proj, lines)
    code, out = run_tool(proj, "session", "journal-status")
    assert_eq("exit code 0", code, 0)
    assert_eq("open_threads 2", out.get("open_threads"), 2)
    assert_eq("total_entries 4", out.get("total_entries"), 4)


def test_journal_status_closed_threads():
    """Threads with terminal events (thread_close, session_end, done) are closed."""
    print("\n[session journal-status] Closed threads")
    proj = setup_project()
    lines = [
        json.dumps({"timestamp": "2026-04-05T10:00:00", "event": "thread_open", "thread_id": "t1"}),
        json.dumps({"timestamp": "2026-04-05T10:01:00", "event": "thread_close", "thread_id": "t1"}),
        json.dumps({"timestamp": "2026-04-05T10:02:00", "event": "thread_open", "thread_id": "t2"}),
        json.dumps({"timestamp": "2026-04-05T10:03:00", "event": "session_end", "thread_id": "t2"}),
        json.dumps({"timestamp": "2026-04-05T10:04:00", "event": "thread_open", "thread_id": "t3"}),
        json.dumps({"timestamp": "2026-04-05T10:05:00", "event": "done", "thread_id": "t3"}),
    ]
    setup_journal(proj, lines)
    code, out = run_tool(proj, "session", "journal-status")
    assert_eq("exit code 0", code, 0)
    assert_eq("open_threads 0", out.get("open_threads"), 0)
    assert_eq("total_entries 6", out.get("total_entries"), 6)


def test_journal_status_malformed_lines():
    """Skips bad lines, reports parse_errors count."""
    print("\n[session journal-status] Malformed lines")
    proj = setup_project()
    lines = [
        json.dumps({"timestamp": "2026-04-05T10:00:00", "event": "thread_open", "thread_id": "t1"}),
        "this is not json {{{",
        "also not json",
        json.dumps({"timestamp": "2026-04-05T10:01:00", "event": "decision", "thread_id": "t1"}),
    ]
    setup_journal(proj, lines)
    code, out = run_tool(proj, "session", "journal-status")
    assert_eq("exit code 0", code, 0)
    assert_eq("parse_errors 2", out.get("parse_errors"), 2)
    assert_eq("total_entries 2", out.get("total_entries"), 2)
    assert_eq("open_threads 1", out.get("open_threads"), 1)


def test_journal_status_thread_summary():
    """Returns correct per-thread summary."""
    print("\n[session journal-status] Thread summary")
    proj = setup_project()
    lines = [
        json.dumps({"timestamp": "2026-04-05T19:00:00", "event": "thread_open", "thread_id": "sprint-dev-001"}),
        json.dumps({"timestamp": "2026-04-05T19:30:00", "event": "decision", "thread_id": "sprint-dev-001"}),
        json.dumps({"timestamp": "2026-04-05T18:00:00", "event": "thread_open", "thread_id": "triage-002"}),
        json.dumps({"timestamp": "2026-04-05T18:30:00", "event": "thread_close", "thread_id": "triage-002"}),
    ]
    setup_journal(proj, lines)
    code, out = run_tool(proj, "session", "journal-status")
    assert_eq("exit code 0", code, 0)
    summary = out.get("thread_summary", [])
    assert_eq("two threads", len(summary), 2)
    # Build lookup by thread_id
    by_id = {t["thread_id"]: t for t in summary}
    assert_eq("sprint-dev-001 exists", "sprint-dev-001" in by_id, True)
    assert_eq("triage-002 exists", "triage-002" in by_id, True)
    assert_eq("sprint-dev-001 open", by_id["sprint-dev-001"]["status"], "open")
    assert_eq("sprint-dev-001 last_event", by_id["sprint-dev-001"]["last_event"], "decision")
    assert_eq("sprint-dev-001 last_timestamp", by_id["sprint-dev-001"]["last_timestamp"], "2026-04-05T19:30:00")
    assert_eq("triage-002 closed", by_id["triage-002"]["status"], "closed")
    assert_eq("triage-002 last_event", by_id["triage-002"]["last_event"], "thread_close")


# --- Journal Hygiene Tests ---

def make_journal_entry(thread_id: str, event: str = "thread_open", **kwargs) -> str:
    """Build a JSONL journal entry string."""
    entry = {"thread_id": thread_id, "event": event, **kwargs}
    return json.dumps(entry)


def test_journal_hygiene_no_file():
    """Returns empty threads and no warnings when journal absent."""
    print("\n[session journal-hygiene] No file")
    proj = setup_project()
    # Do NOT create journal.jsonl
    code, out = run_tool(proj, "session", "journal-hygiene")
    assert_eq("exit code 0", code, 0)
    assert_eq("threads empty", out.get("threads"), [])
    assert_eq("open_count 0", out.get("open_count"), 0)
    assert_eq("concurrent empty", out.get("warnings", {}).get("concurrent"), [])
    assert_eq("dormant empty", out.get("warnings", {}).get("dormant"), [])


def test_journal_hygiene_no_open_threads():
    """Returns empty threads when all threads are closed."""
    print("\n[session journal-hygiene] No open threads")
    proj = setup_project()
    lines = [
        make_journal_entry("T-001", "thread_open", last_active="2026-04-08T10:00:00",
                           context_summary_short="Sprint dev", story_ref="s1", phase="impl"),
        make_journal_entry("T-001", "thread_close", last_active="2026-04-08T11:00:00",
                           context_summary_short="Sprint dev", story_ref="s1", phase="impl"),
    ]
    setup_journal(proj, lines)
    code, out = run_tool(proj, "session", "journal-hygiene")
    assert_eq("exit code 0", code, 0)
    assert_eq("threads empty", out.get("threads"), [])
    assert_eq("open_count 0", out.get("open_count"), 0)
    assert_eq("total_count 1", out.get("total_count"), 1)


def test_journal_hygiene_sort_order():
    """Threads sorted by last_active descending."""
    print("\n[session journal-hygiene] Sort order")
    proj = setup_project()
    lines = [
        make_journal_entry("T-001", "thread_open", last_active="2026-04-06T10:00:00",
                           context_summary_short="Older", story_ref="s1", phase="impl"),
        make_journal_entry("T-002", "thread_open", last_active="2026-04-07T10:00:00",
                           context_summary_short="Newer", story_ref="s2", phase="impl"),
    ]
    setup_journal(proj, lines)
    code, out = run_tool(proj, "session", "journal-hygiene")
    assert_eq("exit code 0", code, 0)
    threads = out.get("threads", [])
    assert_eq("two threads", len(threads), 2)
    assert_eq("newer first", threads[0]["context_summary_short"], "Newer")
    assert_eq("older second", threads[1]["context_summary_short"], "Older")


def test_journal_hygiene_elapsed_labels():
    """Correct human-readable elapsed labels for minutes, hours, yesterday, and days."""
    print("\n[session journal-hygiene] Elapsed labels")
    import datetime as dt_module

    proj = setup_project()
    now = dt_module.datetime.now()

    def ts(delta_seconds: float) -> str:
        t = now - dt_module.timedelta(seconds=delta_seconds)
        return t.strftime("%Y-%m-%dT%H:%M:%S")

    lines = [
        make_journal_entry("T-min", "thread_open", last_active=ts(300),
                           context_summary_short="Minutes", story_ref="s1", phase="impl"),
        make_journal_entry("T-hrs", "thread_open", last_active=ts(7200),
                           context_summary_short="Hours", story_ref="s2", phase="impl"),
        make_journal_entry("T-yes", "thread_open", last_active=ts(90000),
                           context_summary_short="Yesterday", story_ref="s3", phase="impl"),
        make_journal_entry("T-day", "thread_open", last_active=ts(86400 * 4),
                           context_summary_short="Days", story_ref="s4", phase="impl"),
    ]
    setup_journal(proj, lines)
    code, out = run_tool(proj, "session", "journal-hygiene")
    assert_eq("exit code 0", code, 0)
    threads = out.get("threads", [])
    by_id = {t["thread_id"]: t for t in threads}
    assert_eq("minutes label", "m ago" in by_id["T-min"]["elapsed_label"], True)
    assert_eq("hours label", "h ago" in by_id["T-hrs"]["elapsed_label"], True)
    assert_eq("yesterday label", by_id["T-yes"]["elapsed_label"], "yesterday")
    assert_eq("days label", "d ago" in by_id["T-day"]["elapsed_label"], True)


def test_journal_hygiene_concurrent_warning():
    """Flags threads active within 30 minutes."""
    print("\n[session journal-hygiene] Concurrent warning")
    import datetime as dt_module

    proj = setup_project()
    now = dt_module.datetime.now()
    recent_ts = (now - dt_module.timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%S")
    old_ts = (now - dt_module.timedelta(hours=5)).strftime("%Y-%m-%dT%H:%M:%S")

    lines = [
        make_journal_entry("T-recent", "thread_open", last_active=recent_ts,
                           context_summary_short="Recent", story_ref="s1", phase="impl"),
        make_journal_entry("T-old", "thread_open", last_active=old_ts,
                           context_summary_short="Old", story_ref="s2", phase="impl"),
    ]
    setup_journal(proj, lines)
    code, out = run_tool(proj, "session", "journal-hygiene")
    assert_eq("exit code 0", code, 0)
    concurrent = out.get("warnings", {}).get("concurrent", [])
    assert_eq("one concurrent warning", len(concurrent), 1)
    assert_eq("concurrent thread_id", concurrent[0]["thread_id"], "T-recent")
    assert_eq("minutes_ago present", "minutes_ago" in concurrent[0], True)


def test_journal_hygiene_dormant_warning():
    """Flags threads inactive more than 3 days."""
    print("\n[session journal-hygiene] Dormant warning")
    import datetime as dt_module

    proj = setup_project()
    now = dt_module.datetime.now()
    dormant_ts = (now - dt_module.timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%S")
    active_ts = (now - dt_module.timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S")

    lines = [
        make_journal_entry("T-dormant", "thread_open", last_active=dormant_ts,
                           context_summary_short="Dormant", story_ref="s1", phase="impl"),
        make_journal_entry("T-active", "thread_open", last_active=active_ts,
                           context_summary_short="Active", story_ref="s2", phase="impl"),
    ]
    setup_journal(proj, lines)
    code, out = run_tool(proj, "session", "journal-hygiene")
    assert_eq("exit code 0", code, 0)
    dormant = out.get("warnings", {}).get("dormant", [])
    assert_eq("one dormant warning", len(dormant), 1)
    assert_eq("dormant thread_id", dormant[0]["thread_id"], "T-dormant")
    assert_eq("days_inactive >= 5", dormant[0]["days_inactive"] >= 5, True)


def test_journal_hygiene_dependency_satisfied():
    """Detects when depends_on_thread target is closed."""
    print("\n[session journal-hygiene] Dependency satisfied")
    import datetime as dt_module

    proj = setup_project()
    now = dt_module.datetime.now()
    ts1 = (now - dt_module.timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S")
    ts2 = (now - dt_module.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")

    lines = [
        # T-dep: was open, now closed
        make_journal_entry("T-dep", "thread_open", last_active=ts1,
                           context_summary_short="Dep story", story_ref="s1", phase="impl"),
        make_journal_entry("T-dep", "thread_close", last_active=ts1,
                           context_summary_short="Dep story", story_ref="s1", phase="impl"),
        # T-wait: depends on T-dep, which is now closed
        make_journal_entry("T-wait", "thread_open", last_active=ts2,
                           context_summary_short="Waiting story", story_ref="s2", phase="impl",
                           depends_on_thread="T-dep"),
    ]
    setup_journal(proj, lines)
    code, out = run_tool(proj, "session", "journal-hygiene")
    assert_eq("exit code 0", code, 0)
    dep_sat = out.get("warnings", {}).get("dependency_satisfied", [])
    assert_eq("one dependency_satisfied", len(dep_sat), 1)
    assert_eq("waiting thread flagged", dep_sat[0]["thread_id"], "T-wait")
    assert_eq("depends_on_summary present", "depends_on_summary" in dep_sat[0], True)


def test_journal_hygiene_dependency_satisfied_uses_context_summary_short():
    """depends_on_summary uses context_summary_short from earlier events, not thread ID.

    Covers the case where the thread_close event does not carry context_summary_short
    (which is the common real-world scenario — the summary is set by earlier events).
    """
    print("\n[session journal-hygiene] Dependency satisfied — summary from earlier event")
    import datetime as dt_module

    proj = setup_project()
    now = dt_module.datetime.now()
    ts1 = (now - dt_module.timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S")
    ts2 = (now - dt_module.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")

    lines = [
        # T-dep: opened with summary, closed without repeating context_summary_short
        make_journal_entry("T-dep", "thread_open", last_active=ts1,
                           context_summary_short="Dependency summary text",
                           story_ref="s1", phase="impl"),
        make_journal_entry("T-dep", "thread_close", last_active=ts1,
                           story_ref="s1", phase="impl"),  # no context_summary_short here
        # T-wait: depends on T-dep, which is now closed
        make_journal_entry("T-wait", "thread_open", last_active=ts2,
                           context_summary_short="Waiting story", story_ref="s2", phase="impl",
                           depends_on_thread="T-dep"),
    ]
    setup_journal(proj, lines)
    code, out = run_tool(proj, "session", "journal-hygiene")
    assert_eq("exit code 0", code, 0)
    dep_sat = out.get("warnings", {}).get("dependency_satisfied", [])
    assert_eq("one dependency_satisfied", len(dep_sat), 1)
    assert_eq("waiting thread flagged", dep_sat[0]["thread_id"], "T-wait")
    assert_eq("depends_on_summary is context_summary_short not thread ID",
              dep_sat[0].get("depends_on_summary"), "Dependency summary text")


def test_journal_hygiene_unwieldy():
    """Warning present when more than 5 open threads exist."""
    print("\n[session journal-hygiene] Unwieldy warning")
    import datetime as dt_module

    proj = setup_project()
    now = dt_module.datetime.now()
    lines = []
    for i in range(6):
        ts = (now - dt_module.timedelta(hours=i + 1)).strftime("%Y-%m-%dT%H:%M:%S")
        lines.append(make_journal_entry(f"T-{i:03d}", "thread_open", last_active=ts,
                                        context_summary_short=f"Thread {i}",
                                        story_ref=f"s{i}", phase="impl"))
    setup_journal(proj, lines)
    code, out = run_tool(proj, "session", "journal-hygiene")
    assert_eq("exit code 0", code, 0)
    unwieldy = out.get("warnings", {}).get("unwieldy")
    assert_eq("unwieldy non-null", unwieldy is not None, True)
    assert_eq("open_count 6", unwieldy.get("open_count"), 6)


def test_journal_hygiene_no_reoff_suppression():
    """Suppresses dormant offer when declined_offers matches context_hash."""
    print("\n[session journal-hygiene] No-Re-Offer suppression")
    import datetime as dt_module
    import subprocess as sp_mod

    proj = setup_project()
    now = dt_module.datetime.now()
    dormant_ts = (now - dt_module.timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%S")

    # Get git hash for the temp project's git repo
    proc = sp_mod.run(["git", "rev-parse", "--short", "HEAD"],
                      capture_output=True, text=True, cwd=str(proj))
    git_hash = proc.stdout.strip() if proc.returncode == 0 else "unknown"

    thread_id = "T-dormant"
    story_ref = "s1"
    phase = "impl"
    context_hash = f"{thread_id}|{story_ref}|{phase}|{git_hash}"

    declined_offers = [{"offer_type": "dormant-closure", "context_hash": context_hash}]

    lines = [
        make_journal_entry(thread_id, "thread_open", last_active=dormant_ts,
                           context_summary_short="Dormant suppressed", story_ref=story_ref,
                           phase=phase, declined_offers=declined_offers),
    ]
    setup_journal(proj, lines)
    code, out = run_tool(proj, "session", "journal-hygiene")
    assert_eq("exit code 0", code, 0)
    dormant = out.get("warnings", {}).get("dormant", [])
    suppressed = out.get("suppressed_offers", [])
    assert_eq("dormant empty (suppressed)", len(dormant), 0)
    assert_eq("suppressed_offers has entry", len(suppressed), 1)
    assert_eq("suppressed thread_id", suppressed[0]["thread_id"], thread_id)
    assert_eq("suppressed offer_type", suppressed[0]["offer_type"], "dormant-closure")


def test_journal_hygiene_no_reoff_context_change():
    """Re-offers dormant thread when context_hash differs from declined entry."""
    print("\n[session journal-hygiene] No-Re-Offer — context changed, re-offer")
    import datetime as dt_module

    proj = setup_project()
    now = dt_module.datetime.now()
    dormant_ts = (now - dt_module.timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%S")

    # Use a stale/wrong context_hash so it won't match the current one
    stale_hash = "T-dormant|s1|impl|oldgithash000"
    declined_offers = [{"offer_type": "dormant-closure", "context_hash": stale_hash}]

    lines = [
        make_journal_entry("T-dormant", "thread_open", last_active=dormant_ts,
                           context_summary_short="Dormant re-offer", story_ref="s1",
                           phase="impl", declined_offers=declined_offers),
    ]
    setup_journal(proj, lines)
    code, out = run_tool(proj, "session", "journal-hygiene")
    assert_eq("exit code 0", code, 0)
    dormant = out.get("warnings", {}).get("dormant", [])
    suppressed = out.get("suppressed_offers", [])
    assert_eq("dormant surfaced (not suppressed)", len(dormant), 1)
    assert_eq("suppressed empty", len(suppressed), 0)


def test_journal_hygiene_suggested_prompts():
    """Returns pre-composed prompt strings for each warning type."""
    print("\n[session journal-hygiene] Suggested prompts")
    proj = setup_project()
    # Prompts are returned even when no journal or no warnings exist
    code, out = run_tool(proj, "session", "journal-hygiene")
    assert_eq("exit code 0", code, 0)
    prompts = out.get("suggested_prompts", {})
    assert_eq("concurrent prompt exists", "concurrent" in prompts, True)
    assert_eq("dormant prompt exists", "dormant" in prompts, True)
    assert_eq("dependency_satisfied prompt exists", "dependency_satisfied" in prompts, True)
    assert_eq("unwieldy prompt exists", "unwieldy" in prompts, True)
    assert_eq("concurrent prompt non-empty", len(prompts.get("concurrent", "")) > 0, True)


# --- Journal Append Tests ---

def test_journal_append_creates_file():
    """Creates journal.jsonl if absent."""
    print("\n[session journal-append] Creates journal.jsonl if absent")
    proj = setup_project()
    entry = json.dumps({"thread_id": "T-001", "event": "thread_open",
                        "last_active": "2026-04-08T10:00:00"})
    code, out = run_tool(proj, "session", "journal-append", "--entry", entry)
    assert_eq("exit code 0", code, 0)
    journal_path = proj / ".claude" / "momentum" / "journal.jsonl"
    assert_eq("journal created", journal_path.exists(), True)
    lines = [l for l in journal_path.read_text().splitlines() if l.strip()]
    assert_eq("one line written", len(lines), 1)


def test_journal_append_appends_line():
    """Appends valid JSON line to existing file."""
    print("\n[session journal-append] Appends to existing file")
    proj = setup_project()
    existing = json.dumps({"thread_id": "T-001", "event": "thread_open",
                           "last_active": "2026-04-08T09:00:00"})
    setup_journal(proj, [existing])

    new_entry = json.dumps({"thread_id": "T-001", "event": "decision",
                             "last_active": "2026-04-08T10:00:00"})
    code, out = run_tool(proj, "session", "journal-append", "--entry", new_entry)
    assert_eq("exit code 0", code, 0)
    journal_path = proj / ".claude" / "momentum" / "journal.jsonl"
    lines = [l for l in journal_path.read_text().splitlines() if l.strip()]
    assert_eq("two lines in journal", len(lines), 2)
    appended = json.loads(lines[1])
    assert_eq("appended event", appended["event"], "decision")


def test_journal_append_invalid_json():
    """Fails with error for non-JSON input."""
    print("\n[session journal-append] Invalid JSON rejected")
    proj = setup_project()
    code, out = run_tool(proj, "session", "journal-append", "--entry", "not valid json {{{")
    assert_eq("exit code 1", code, 1)
    assert_eq("success false", out.get("success"), False)
    # Journal should not be created
    journal_path = proj / ".claude" / "momentum" / "journal.jsonl"
    assert_eq("journal not created", journal_path.exists(), False)


def test_journal_append_regenerates_view():
    """journal-view.md is regenerated after append."""
    print("\n[session journal-append] Regenerates journal-view.md")
    proj = setup_project()
    entry = json.dumps({"thread_id": "T-001", "event": "thread_open",
                        "last_active": "2026-04-08T10:00:00",
                        "context_summary_short": "Sprint dev",
                        "story_ref": "my-story", "phase": "impl"})
    code, out = run_tool(proj, "session", "journal-append", "--entry", entry)
    assert_eq("exit code 0", code, 0)
    view_path = proj / ".claude" / "momentum" / "journal-view.md"
    assert_eq("journal-view.md created", view_path.exists(), True)
    view_content = view_path.read_text()
    assert_eq("view has Thread header", "Thread" in view_content, True)
    assert_eq("view has Status header", "Status" in view_content, True)


def test_journal_append_view_includes_recent_closed():
    """View includes threads closed within the last 7 days but excludes older ones."""
    print("\n[session journal-append] View includes recently closed, excludes old closed")
    import datetime as dt_module

    proj = setup_project()
    now = dt_module.datetime.now()
    recent_close_ts = (now - dt_module.timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S")
    old_close_ts = (now - dt_module.timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%S")

    lines = [
        make_journal_entry("T-recent-closed", "thread_close", last_active=recent_close_ts,
                           context_summary_short="Recent closed", story_ref="s1", phase="impl"),
        make_journal_entry("T-old-closed", "thread_close", last_active=old_close_ts,
                           context_summary_short="Old closed", story_ref="s2", phase="impl"),
    ]
    setup_journal(proj, lines)

    # Append a new entry to trigger view regeneration
    new_entry = json.dumps({"thread_id": "T-open", "event": "thread_open",
                             "last_active": now.strftime("%Y-%m-%dT%H:%M:%S"),
                             "context_summary_short": "Open thread",
                             "story_ref": "s3", "phase": "impl"})
    code, out = run_tool(proj, "session", "journal-append", "--entry", new_entry)
    assert_eq("exit code 0", code, 0)

    view_path = proj / ".claude" / "momentum" / "journal-view.md"
    view_content = view_path.read_text()
    assert_eq("recent closed in view", "Recent closed" in view_content, True)
    assert_eq("old closed not in view", "Old closed" not in view_content, True)
    assert_eq("open thread in view", "Open thread" in view_content, True)


# --- Feature Status Hash Tests ---

def setup_features_file(project_dir: Path, content: str) -> Path:
    """Create _bmad-output/planning-artifacts/features.json."""
    features_dir = project_dir / "_bmad-output" / "planning-artifacts"
    features_dir.mkdir(parents=True, exist_ok=True)
    features_path = features_dir / "features.json"
    features_path.write_text(content)
    return features_path


def setup_feature_status_cache(project_dir: Path, frontmatter: dict, body: str = "") -> Path:
    """Create .claude/momentum/feature-status.md with YAML frontmatter."""
    cache_dir = project_dir / ".claude" / "momentum"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / "feature-status.md"
    lines = ["---"]
    for key, value in frontmatter.items():
        lines.append(f"{key}: {value}")
    lines.append("---")
    if body:
        lines.append("")
        lines.append(body)
    cache_path.write_text("\n".join(lines) + "\n")
    return cache_path


def compute_expected_hash(features_content: str, stories_content: str) -> str:
    """Compute expected SHA-256 hash matching the tool's logic."""
    combined = features_content + ":" + stories_content
    return hashlib.sha256(combined.encode()).hexdigest()


def test_feature_status_hash_no_features_file():
    """Returns features_present: false, empty hash when features.json absent."""
    print("\n[feature-status-hash] No features.json — features_present false")
    proj = setup_project()
    code, out = run_tool(proj, "feature-status-hash")
    assert_eq("exit code 0", code, 0)
    assert_eq("features_present false", out.get("hash_result", {}).get("features_present"), False)
    assert_eq("hash empty string", out.get("hash_result", {}).get("hash"), "")


def test_feature_status_hash_with_features_file():
    """Returns features_present: true, non-empty hash when features.json present."""
    print("\n[feature-status-hash] With features.json — features_present true")
    proj = setup_project()
    setup_features_file(proj, '{"features": [{"slug": "auth"}]}')
    code, out = run_tool(proj, "feature-status-hash")
    assert_eq("exit code 0", code, 0)
    assert_eq("features_present true", out.get("hash_result", {}).get("features_present"), True)
    hash_val = out.get("hash_result", {}).get("hash", "")
    assert_eq("hash non-empty", len(hash_val) > 0, True)


def test_feature_status_hash_deterministic():
    """Same inputs produce same hash on repeated calls."""
    print("\n[feature-status-hash] Deterministic — same inputs same hash")
    proj = setup_project()
    features_content = '{"features": [{"slug": "auth"}]}'
    setup_features_file(proj, features_content)
    code1, out1 = run_tool(proj, "feature-status-hash")
    code2, out2 = run_tool(proj, "feature-status-hash")
    assert_eq("exit code 0 first", code1, 0)
    assert_eq("exit code 0 second", code2, 0)
    assert_eq("hashes match", out1.get("hash_result", {}).get("hash"),
              out2.get("hash_result", {}).get("hash"))


def test_feature_status_hash_changes_on_features_change():
    """Hash differs when features.json content changes."""
    print("\n[feature-status-hash] Hash changes on features change")
    proj = setup_project()
    setup_features_file(proj, '{"features": [{"slug": "auth"}]}')
    code1, out1 = run_tool(proj, "feature-status-hash")
    setup_features_file(proj, '{"features": [{"slug": "payments"}]}')
    code2, out2 = run_tool(proj, "feature-status-hash")
    assert_eq("exit codes 0", code1 == 0 and code2 == 0, True)
    assert_eq("hashes differ", out1.get("hash_result", {}).get("hash") !=
              out2.get("hash_result", {}).get("hash"), True)


def test_feature_status_hash_changes_on_stories_change():
    """Hash differs when stories/index.json content changes."""
    print("\n[feature-status-hash] Hash changes on stories change")
    proj = setup_project()
    setup_features_file(proj, '{"features": [{"slug": "auth"}]}')
    # First run with default stories
    code1, out1 = run_tool(proj, "feature-status-hash")
    # Change stories content
    stories_path = proj / ".momentum" / "stories" / "index.json"
    stories_path.write_text('{"new-story": {"status": "backlog", "title": "New"}}')
    code2, out2 = run_tool(proj, "feature-status-hash")
    assert_eq("exit codes 0", code1 == 0 and code2 == 0, True)
    assert_eq("hashes differ", out1.get("hash_result", {}).get("hash") !=
              out2.get("hash_result", {}).get("hash"), True)


# --- Preflight Feature Status Tests ---

def _setup_preflight_env(proj: Path, version: str = "1.0.0") -> None:
    """Set up versions + installed to get route=greeting."""
    setup_versions_json(proj, {
        "current_version": version,
        "versions": {
            version: {
                "actions": [
                    {"action": "migration", "group": "hooks", "scope": "project",
                     "source": "m.md", "description": "hooks"}
                ]
            }
        }
    })
    setup_installed_json(proj, {
        "components": {"hooks": {"version": version}},
        "session_stats": {"momentum_completions": 3}
    })


def test_preflight_feature_status_no_features():
    """greeting.feature_status.state == 'no-features' when features.json absent."""
    print("\n[startup-preflight] Feature status — no features file")
    proj = setup_project()
    _setup_preflight_env(proj)

    def check():
        code, out = run_tool(proj, "session", "startup-preflight")
        assert_eq("exit code 0", code, 0)
        assert_eq("route greeting", out.get("route"), "greeting")
        greeting = out.get("greeting", {})
        fs = greeting.get("feature_status", {})
        assert_eq("state no-features", fs.get("state"), "no-features")

    _with_global_installed({"components": {"hooks": {"version": "1.0.0", "hash": ""}}}, check)


def test_preflight_feature_status_no_cache():
    """greeting.feature_status.state == 'no-cache' when features.json present but cache absent."""
    print("\n[startup-preflight] Feature status — features present, no cache")
    proj = setup_project()
    _setup_preflight_env(proj)
    setup_features_file(proj, '{"features": [{"slug": "auth"}]}')
    # No cache file created

    def check():
        code, out = run_tool(proj, "session", "startup-preflight")
        assert_eq("exit code 0", code, 0)
        greeting = out.get("greeting", {})
        fs = greeting.get("feature_status", {})
        assert_eq("state no-cache", fs.get("state"), "no-cache")

    _with_global_installed({"components": {"hooks": {"version": "1.0.0", "hash": ""}}}, check)


def test_preflight_feature_status_fresh():
    """state == 'fresh', correct summary when hash matches."""
    print("\n[startup-preflight] Feature status — fresh cache")
    proj = setup_project()
    _setup_preflight_env(proj)
    features_content = '{"features": [{"slug": "auth"}]}'
    setup_features_file(proj, features_content)
    # Read the default stories content to compute the hash
    stories_content = (proj / ".momentum" / "stories" / "index.json").read_text()
    expected_hash = compute_expected_hash(features_content, stories_content)
    setup_feature_status_cache(proj, {
        "input_hash": expected_hash,
        "summary": "2 features: 1 working · 1 partial",
        "generated_at": "2026-04-11T10:00:00"
    })

    def check():
        code, out = run_tool(proj, "session", "startup-preflight")
        assert_eq("exit code 0", code, 0)
        greeting = out.get("greeting", {})
        fs = greeting.get("feature_status", {})
        assert_eq("state fresh", fs.get("state"), "fresh")
        assert_eq("summary correct", fs.get("summary"), "2 features: 1 working · 1 partial")

    _with_global_installed({"components": {"hooks": {"version": "1.0.0", "hash": ""}}}, check)


def test_preflight_feature_status_stale():
    """state == 'stale', correct summary when hash mismatches."""
    print("\n[startup-preflight] Feature status — stale cache")
    proj = setup_project()
    _setup_preflight_env(proj)
    setup_features_file(proj, '{"features": [{"slug": "auth"}]}')
    setup_feature_status_cache(proj, {
        "input_hash": "old-wrong-hash-value",
        "summary": "2 features: 1 working · 1 partial",
        "generated_at": "2026-04-11T10:00:00"
    })

    def check():
        code, out = run_tool(proj, "session", "startup-preflight")
        assert_eq("exit code 0", code, 0)
        greeting = out.get("greeting", {})
        fs = greeting.get("feature_status", {})
        assert_eq("state stale", fs.get("state"), "stale")
        assert_eq("summary correct", fs.get("summary"), "2 features: 1 working · 1 partial")

    _with_global_installed({"components": {"hooks": {"version": "1.0.0", "hash": ""}}}, check)


def test_preflight_feature_status_invalid_cache_json():
    """Invalid cache frontmatter treated as absent — no-cache state."""
    print("\n[startup-preflight] Feature status — invalid cache frontmatter")
    proj = setup_project()
    _setup_preflight_env(proj)
    setup_features_file(proj, '{"features": [{"slug": "auth"}]}')
    # Write a cache file with unparseable frontmatter
    cache_path = proj / ".claude" / "momentum" / "feature-status.md"
    cache_path.write_text("not valid yaml frontmatter\n")

    def check():
        code, out = run_tool(proj, "session", "startup-preflight")
        assert_eq("exit code 0", code, 0)
        greeting = out.get("greeting", {})
        fs = greeting.get("feature_status", {})
        assert_eq("state no-cache", fs.get("state"), "no-cache")

    _with_global_installed({"components": {"hooks": {"version": "1.0.0", "hash": ""}}}, check)


# --- Greeting-State Feature Status Tests ---

def test_greeting_state_feature_status_no_features():
    """greeting-state returns state == 'no-features' when features.json absent."""
    print("\n[session greeting-state] Feature status — no features")
    proj = setup_project()
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 3}})
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    fs = out.get("feature_status", {})
    assert_eq("state no-features", fs.get("state"), "no-features")


def test_greeting_state_feature_status_no_cache():
    """greeting-state returns state == 'no-cache' when features present but cache absent."""
    print("\n[session greeting-state] Feature status — features present, no cache")
    proj = setup_project()
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 3}})
    setup_features_file(proj, '{"features": [{"slug": "auth"}]}')
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    fs = out.get("feature_status", {})
    assert_eq("state no-cache", fs.get("state"), "no-cache")


def test_greeting_state_feature_status_fresh():
    """greeting-state returns state == 'fresh' with correct summary."""
    print("\n[session greeting-state] Feature status — fresh cache")
    proj = setup_project()
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 3}})
    features_content = '{"features": [{"slug": "auth"}]}'
    setup_features_file(proj, features_content)
    stories_content = (proj / ".momentum" / "stories" / "index.json").read_text()
    expected_hash = compute_expected_hash(features_content, stories_content)
    setup_feature_status_cache(proj, {
        "input_hash": expected_hash,
        "summary": "1 feature: 1 working",
        "generated_at": "2026-04-11T10:00:00"
    })
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    fs = out.get("feature_status", {})
    assert_eq("state fresh", fs.get("state"), "fresh")
    assert_eq("summary correct", fs.get("summary"), "1 feature: 1 working")


def test_greeting_state_feature_status_stale():
    """greeting-state returns state == 'stale' with correct summary."""
    print("\n[session greeting-state] Feature status — stale cache")
    proj = setup_project()
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 3}})
    setup_features_file(proj, '{"features": [{"slug": "auth"}]}')
    setup_feature_status_cache(proj, {
        "input_hash": "wrong-hash",
        "summary": "1 feature: 1 not-started",
        "generated_at": "2026-04-11T10:00:00"
    })
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    fs = out.get("feature_status", {})
    assert_eq("state stale", fs.get("state"), "stale")
    assert_eq("summary correct", fs.get("summary"), "1 feature: 1 not-started")


# --- story-add --feature-slug / --story-type Tests ---

def test_story_add_default_story_type():
    """story-add writes story_type: feature by default."""
    print("\n[story-add] Default story_type is feature")
    proj = setup_project(stories={})
    code, out = run_tool(proj, "sprint", "story-add",
                         "--slug", "new-story", "--title", "New Story", "--epic", "core")
    assert_eq("exit code 0", code, 0)
    stories = read_stories(proj)
    assert_eq("story_type field present", "story_type" in stories["new-story"], True)
    assert_eq("story_type default feature", stories["new-story"]["story_type"], "feature")


def test_story_add_explicit_story_type():
    """story-add persists an explicit story_type."""
    print("\n[story-add] Explicit story_type persisted")
    proj = setup_project(stories={})
    code, out = run_tool(proj, "sprint", "story-add",
                         "--slug", "defect-story", "--title", "Defect Story", "--epic", "core",
                         "--story-type", "defect")
    assert_eq("exit code 0", code, 0)
    stories = read_stories(proj)
    assert_eq("story_type defect", stories["defect-story"]["story_type"], "defect")


def test_story_add_invalid_story_type():
    """story-add rejects unknown story_type."""
    print("\n[story-add] Invalid story_type rejected")
    proj = setup_project(stories={})
    code, out = run_tool(proj, "sprint", "story-add",
                         "--slug", "bad-story", "--title", "Bad", "--epic", "core",
                         "--story-type", "unknown-type")
    assert_eq("rejected", code, 1)
    assert_eq("success false", out.get("success"), False)


def test_story_add_feature_slug_persisted():
    """story-add persists feature_slug when provided."""
    print("\n[story-add] feature_slug persisted")
    proj = setup_project(stories={})
    code, out = run_tool(proj, "sprint", "story-add",
                         "--slug", "feat-story", "--title", "Feature Story", "--epic", "core",
                         "--feature-slug", "my-feature")
    assert_eq("exit code 0", code, 0)
    stories = read_stories(proj)
    assert_eq("feature_slug set", stories["feat-story"].get("feature_slug"), "my-feature")


def test_story_add_feature_slug_omitted_when_empty():
    """story-add omits feature_slug field when not provided."""
    print("\n[story-add] feature_slug absent when not provided")
    proj = setup_project(stories={})
    code, out = run_tool(proj, "sprint", "story-add",
                         "--slug", "no-feat-story", "--title", "No Feature Story", "--epic", "core")
    assert_eq("exit code 0", code, 0)
    stories = read_stories(proj)
    assert_eq("feature_slug absent", "feature_slug" not in stories["no-feat-story"], True)


# --- .momentum/ Path Migration Tests ---

def test_stories_path_resolves_to_momentum():
    """stories_path() must resolve to .momentum/stories/index.json."""
    print("\n[.momentum/ migration] stories_path resolves to .momentum/")
    proj = setup_project()
    # Verify the file was created at .momentum/stories/index.json (not old path)
    new_path = proj / ".momentum" / "stories" / "index.json"
    old_path = proj / "_bmad-output" / "implementation-artifacts" / "stories" / "index.json"
    assert_eq("new .momentum path exists", new_path.exists(), True)
    assert_eq("old _bmad-output path absent", old_path.exists(), False)
    # Verify the tool writes to and reads from the new path
    code, out = run_tool(proj, "sprint", "status-transition", "--story", "test-story", "--target", "ready-for-dev")
    assert_eq("exit code 0", code, 0)
    stories = read_stories(proj)
    assert_eq("status updated at new path", stories["test-story"]["status"], "ready-for-dev")


def test_sprints_path_resolves_to_momentum():
    """sprints_path() must resolve to .momentum/sprints/index.json."""
    print("\n[.momentum/ migration] sprints_path resolves to .momentum/")
    proj = setup_project()
    new_path = proj / ".momentum" / "sprints" / "index.json"
    old_path = proj / "_bmad-output" / "implementation-artifacts" / "sprints" / "index.json"
    assert_eq("new .momentum path exists", new_path.exists(), True)
    assert_eq("old _bmad-output path absent", old_path.exists(), False)
    # Verify sprint activate reads/writes from new path
    import json as _json
    new_path.write_text(_json.dumps({
        "active": None,
        "planning": {"slug": "test-sprint", "locked": False, "stories": [], "approvals": []},
        "completed": []
    }, indent=2) + "\n")
    code, out = run_tool(proj, "sprint", "activate")
    assert_eq("activate exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("active sprint set at new path", result["active"]["slug"], "test-sprint")


# --- Plugin Cache Check Tests ---

def _make_cache_dir(base: Path, versions: list[str]) -> Path:
    """Create a fake plugin cache directory structure with given version dirs."""
    cache_root = base / ".claude" / "plugins" / "cache" / "momentum" / "momentum"
    cache_root.mkdir(parents=True, exist_ok=True)
    for v in versions:
        vdir = cache_root / v / ".claude-plugin"
        vdir.mkdir(parents=True, exist_ok=True)
        (vdir / "plugin.json").write_text(json.dumps({"name": "momentum", "version": v}))
    return cache_root


def _make_source_plugin_json(proj: Path, version: str | None = "0.17.4", malformed: bool = False) -> None:
    """Create a fake source-tree plugin.json at the expected location."""
    plugin_dir = proj / "skills" / "momentum" / ".claude-plugin"
    plugin_dir.mkdir(parents=True, exist_ok=True)
    if malformed:
        (plugin_dir / "plugin.json").write_text("THIS IS NOT JSON {{{")
    elif version is None:
        (plugin_dir / "plugin.json").write_text(json.dumps({"name": "momentum"}))
    else:
        (plugin_dir / "plugin.json").write_text(json.dumps({"name": "momentum", "version": version}))


def test_plugin_cache_check_match():
    """Cache version == source version -> status: match."""
    print("\n[session plugin-cache-check] match")
    proj = setup_project()
    home = proj / "fake_home"
    _make_cache_dir(home, ["0.17.4"])
    _make_source_plugin_json(proj, "0.17.4")
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(proj), "HOME": str(home)}
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "session", "plugin-cache-check"],
        capture_output=True, text=True, env=env
    )
    out = json.loads(proc.stdout)
    assert_eq("exit code 0", proc.returncode, 0)
    assert_eq("status is match", out.get("status"), "match")
    assert_eq("cache_version reported", out.get("cache_version"), "0.17.4")
    assert_eq("source_version reported", out.get("source_version"), "0.17.4")


def test_plugin_cache_check_cache_behind():
    """Cache version < source version -> status: skew-cache-behind."""
    print("\n[session plugin-cache-check] cache behind")
    proj = setup_project()
    home = proj / "fake_home"
    _make_cache_dir(home, ["0.17.0"])
    _make_source_plugin_json(proj, "0.18.0")
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(proj), "HOME": str(home)}
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "session", "plugin-cache-check"],
        capture_output=True, text=True, env=env
    )
    out = json.loads(proc.stdout)
    assert_eq("exit code 0", proc.returncode, 0)
    assert_eq("status is skew-cache-behind", out.get("status"), "skew-cache-behind")
    assert_eq("cache_version 0.17.0", out.get("cache_version"), "0.17.0")
    assert_eq("source_version 0.18.0", out.get("source_version"), "0.18.0")


def test_plugin_cache_check_cache_ahead():
    """Cache version > source version -> status: skew-cache-ahead."""
    print("\n[session plugin-cache-check] cache ahead")
    proj = setup_project()
    home = proj / "fake_home"
    _make_cache_dir(home, ["0.18.0"])
    _make_source_plugin_json(proj, "0.17.0")
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(proj), "HOME": str(home)}
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "session", "plugin-cache-check"],
        capture_output=True, text=True, env=env
    )
    out = json.loads(proc.stdout)
    assert_eq("exit code 0", proc.returncode, 0)
    assert_eq("status is skew-cache-ahead", out.get("status"), "skew-cache-ahead")
    assert_eq("cache_version 0.18.0", out.get("cache_version"), "0.18.0")
    assert_eq("source_version 0.17.0", out.get("source_version"), "0.17.0")


def test_plugin_cache_check_no_cache_dir():
    """Missing cache directory -> status: no-cache, exit 0."""
    print("\n[session plugin-cache-check] no cache dir")
    proj = setup_project()
    home = proj / "fake_home"
    home.mkdir(parents=True, exist_ok=True)
    # No cache directory created
    _make_source_plugin_json(proj, "0.17.4")
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(proj), "HOME": str(home)}
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "session", "plugin-cache-check"],
        capture_output=True, text=True, env=env
    )
    out = json.loads(proc.stdout)
    assert_eq("exit code 0", proc.returncode, 0)
    assert_eq("status is no-cache", out.get("status"), "no-cache")
    assert_eq("cache_version is null", out.get("cache_version"), None)


def test_plugin_cache_check_no_source():
    """Source plugin.json not found -> status: no-source, exit 0."""
    print("\n[session plugin-cache-check] no source plugin.json")
    proj = setup_project()
    home = proj / "fake_home"
    _make_cache_dir(home, ["0.17.4"])
    # No source plugin.json created
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(proj), "HOME": str(home)}
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "session", "plugin-cache-check"],
        capture_output=True, text=True, env=env
    )
    out = json.loads(proc.stdout)
    assert_eq("exit code 0", proc.returncode, 0)
    assert_eq("status is no-source", out.get("status"), "no-source")
    assert_eq("source_version is null", out.get("source_version"), None)


def test_plugin_cache_check_malformed_cache_json():
    """Malformed cache plugin.json -> status: indeterminate, exit 0, diagnostic present."""
    print("\n[session plugin-cache-check] malformed cache JSON")
    proj = setup_project()
    home = proj / "fake_home"
    cache_root = home / ".claude" / "plugins" / "cache" / "momentum" / "momentum"
    vdir = cache_root / "0.17.4" / ".claude-plugin"
    vdir.mkdir(parents=True, exist_ok=True)
    (vdir / "plugin.json").write_text("NOT VALID JSON {{{")
    _make_source_plugin_json(proj, "0.17.4")
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(proj), "HOME": str(home)}
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "session", "plugin-cache-check"],
        capture_output=True, text=True, env=env
    )
    out = json.loads(proc.stdout)
    assert_eq("exit code 0", proc.returncode, 0)
    assert_eq("status is indeterminate", out.get("status"), "indeterminate")
    assert_eq("diagnostic key present", "diagnostic" in out, True)


def test_plugin_cache_check_malformed_source_json():
    """Malformed source plugin.json -> status: indeterminate, exit 0, diagnostic present."""
    print("\n[session plugin-cache-check] malformed source JSON")
    proj = setup_project()
    home = proj / "fake_home"
    _make_cache_dir(home, ["0.17.4"])
    _make_source_plugin_json(proj, malformed=True)
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(proj), "HOME": str(home)}
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "session", "plugin-cache-check"],
        capture_output=True, text=True, env=env
    )
    out = json.loads(proc.stdout)
    assert_eq("exit code 0", proc.returncode, 0)
    assert_eq("status is indeterminate", out.get("status"), "indeterminate")
    assert_eq("diagnostic key present", "diagnostic" in out, True)


def test_plugin_cache_check_missing_version_field():
    """Source plugin.json present but no 'version' field -> status: indeterminate, exit 0."""
    print("\n[session plugin-cache-check] missing version field in source")
    proj = setup_project()
    home = proj / "fake_home"
    _make_cache_dir(home, ["0.17.4"])
    _make_source_plugin_json(proj, version=None)  # writes JSON with no version key
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(proj), "HOME": str(home)}
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "session", "plugin-cache-check"],
        capture_output=True, text=True, env=env
    )
    out = json.loads(proc.stdout)
    assert_eq("exit code 0", proc.returncode, 0)
    assert_eq("status is indeterminate", out.get("status"), "indeterminate")


def test_plugin_cache_check_multiple_cache_versions_highest_selected():
    """Multiple cache version dirs present — highest semver wins."""
    print("\n[session plugin-cache-check] multiple cache versions, highest selected")
    proj = setup_project()
    home = proj / "fake_home"
    _make_cache_dir(home, ["0.16.0", "0.17.0", "0.17.1", "0.17.2"])
    _make_source_plugin_json(proj, "0.17.2")
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(proj), "HOME": str(home)}
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "session", "plugin-cache-check"],
        capture_output=True, text=True, env=env
    )
    out = json.loads(proc.stdout)
    assert_eq("exit code 0", proc.returncode, 0)
    assert_eq("status is match (highest selected)", out.get("status"), "match")
    assert_eq("cache_version is 0.17.2", out.get("cache_version"), "0.17.2")


def test_plugin_cache_check_exit_code_zero_on_skew():
    """Exit code must be 0 even when status indicates skew (callers parse JSON)."""
    print("\n[session plugin-cache-check] exit code 0 on skew")
    proj = setup_project()
    home = proj / "fake_home"
    _make_cache_dir(home, ["0.15.0"])
    _make_source_plugin_json(proj, "0.17.4")
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(proj), "HOME": str(home)}
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "session", "plugin-cache-check"],
        capture_output=True, text=True, env=env
    )
    out = json.loads(proc.stdout)
    assert_eq("exit code 0 on skew-cache-behind", proc.returncode, 0)
    assert_eq("status is skew-cache-behind", out.get("status"), "skew-cache-behind")


# --- _parse_semver unit tests (AVFL-019) ---

def _import_parse_semver():
    """Import _parse_semver from momentum-tools.py via importlib."""
    spec = importlib.util.spec_from_file_location("momentum_tools", str(SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod._parse_semver


def test_parse_semver_rc_sorts_before_release():
    """RC pre-release must sort before its release counterpart (0.17.0-rc1 < 0.17.0)."""
    print("\n[_parse_semver] RC sorts before release")
    _parse_semver = _import_parse_semver()
    rc1 = _parse_semver("0.17.0-rc1")
    release = _parse_semver("0.17.0")
    assert_eq("0.17.0-rc1 < 0.17.0", rc1 < release, True)


def test_parse_semver_release_sorts_before_next():
    """Release sorts before next patch (0.17.0 < 0.17.1)."""
    print("\n[_parse_semver] release sorts before next patch")
    _parse_semver = _import_parse_semver()
    v0 = _parse_semver("0.17.0")
    v1 = _parse_semver("0.17.1")
    assert_eq("0.17.0 < 0.17.1", v0 < v1, True)


def test_parse_semver_rc1_sorts_before_rc2():
    """rc1 sorts before rc2 (0.17.0-rc1 < 0.17.0-rc2)."""
    print("\n[_parse_semver] rc1 < rc2")
    _parse_semver = _import_parse_semver()
    rc1 = _parse_semver("0.17.0-rc1")
    rc2 = _parse_semver("0.17.0-rc2")
    assert_eq("0.17.0-rc1 < 0.17.0-rc2", rc1 < rc2, True)


def test_parse_semver_standard_ordering():
    """Standard version ordering preserved (0.16.0 < 0.17.0 < 0.17.1 < 0.18.0)."""
    print("\n[_parse_semver] standard ordering")
    _parse_semver = _import_parse_semver()
    versions = ["0.16.0", "0.17.0", "0.17.1", "0.18.0"]
    tuples = [_parse_semver(v) for v in versions]
    assert_eq("standard ordering correct", tuples, sorted(tuples))


# --- Story Approval Tests ---

def setup_story_file(project_dir: Path, slug: str, content: str) -> Path:
    """Create a story file in .momentum/stories/<slug>.md."""
    stories_dir = project_dir / ".momentum" / "stories"
    stories_dir.mkdir(parents=True, exist_ok=True)
    story_path = stories_dir / f"{slug}.md"
    story_path.write_text(content)
    return story_path


def compute_file_sha(path: Path) -> str:
    """Compute SHA-256 of a file's contents (matching tool logic)."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_story_approve_writes_approved_entry():
    """story-approve writes an approved entry to planning.approvals."""
    print("\n[sprint story-approve] Writes approved entry")
    slug = "my-story"
    proj = setup_project(
        stories={slug: {"status": "ready-for-dev", "title": "My Story", "epic_slug": "e",
                        "story_file": True, "depends_on": [], "touches": []}},
        sprints={"active": None,
                 "planning": {"slug": "test-sprint", "locked": False, "status": "planning",
                              "stories": [slug]},
                 "completed": []}
    )
    story_path = setup_story_file(proj, slug, "# My Story\n\nSome content.\n")
    expected_sha = compute_file_sha(story_path)

    code, out = run_tool(proj, "sprint", "story-approve",
                         "--slug", slug, "--decision", "approved")
    assert_eq("exit code 0", code, 0)
    assert_eq("success true", out.get("success"), True)

    data = read_sprints(proj)
    approvals = data["planning"].get("approvals", [])
    assert_eq("one approval entry", len(approvals), 1)
    entry = approvals[0]
    assert_eq("slug correct", entry.get("story_slug"), slug)
    assert_eq("decision approved", entry.get("decision"), "approved")
    assert_eq("sha matches", entry.get("story_file_sha"), expected_sha)
    assert_eq("approved_at present", "approved_at" in entry, True)


def test_story_approve_writes_rejected_entry():
    """story-approve with decision=rejected writes a rejection entry."""
    print("\n[sprint story-approve] Writes rejected entry")
    slug = "my-story"
    proj = setup_project(
        stories={slug: {"status": "ready-for-dev", "title": "My Story", "epic_slug": "e",
                        "story_file": True, "depends_on": [], "touches": []}},
        sprints={"active": None,
                 "planning": {"slug": "test-sprint", "locked": False, "status": "planning",
                              "stories": [slug]},
                 "completed": []}
    )
    setup_story_file(proj, slug, "# My Story\n\nContent.\n")

    code, out = run_tool(proj, "sprint", "story-approve",
                         "--slug", slug, "--decision", "rejected")
    assert_eq("exit code 0", code, 0)

    data = read_sprints(proj)
    approvals = data["planning"].get("approvals", [])
    assert_eq("one approval entry", len(approvals), 1)
    assert_eq("decision rejected", approvals[0].get("decision"), "rejected")


def test_story_approve_replaces_prior_entry():
    """Re-approving a story replaces the prior entry (idempotent overwrite)."""
    print("\n[sprint story-approve] Replaces prior entry (idempotent)")
    slug = "my-story"
    old_sha = "deadbeef" * 8
    proj = setup_project(
        stories={slug: {"status": "ready-for-dev", "title": "My Story", "epic_slug": "e",
                        "story_file": True, "depends_on": [], "touches": []}},
        sprints={"active": None,
                 "planning": {"slug": "test-sprint", "locked": False, "status": "planning",
                              "stories": [slug],
                              "approvals": [{"story_slug": slug, "decision": "approved",
                                             "approved_at": "2026-01-01T00:00:00Z",
                                             "story_file_sha": old_sha}]},
                 "completed": []}
    )
    story_path = setup_story_file(proj, slug, "# Updated content.\n")
    new_sha = compute_file_sha(story_path)

    code, out = run_tool(proj, "sprint", "story-approve",
                         "--slug", slug, "--decision", "approved")
    assert_eq("exit code 0", code, 0)

    data = read_sprints(proj)
    approvals = data["planning"].get("approvals", [])
    assert_eq("still one entry after re-approve", len(approvals), 1)
    assert_eq("sha updated to new", approvals[0].get("story_file_sha"), new_sha)


def test_story_approve_no_planning_sprint():
    """story-approve fails when no planning sprint exists."""
    print("\n[sprint story-approve] No planning sprint")
    proj = setup_project(sprints={"active": None, "planning": None, "completed": []})
    setup_story_file(proj, "ghost", "content")
    code, out = run_tool(proj, "sprint", "story-approve",
                         "--slug", "ghost", "--decision", "approved")
    assert_eq("rejected", code, 1)
    assert_eq("success false", out.get("success"), False)


def test_story_approve_slug_not_in_sprint():
    """story-approve fails when slug is not in planning.stories."""
    print("\n[sprint story-approve] Slug not in sprint")
    proj = setup_project(
        sprints={"active": None,
                 "planning": {"slug": "s", "locked": False, "status": "planning",
                              "stories": ["other-story"]},
                 "completed": []}
    )
    setup_story_file(proj, "my-story", "content")
    code, out = run_tool(proj, "sprint", "story-approve",
                         "--slug", "my-story", "--decision", "approved")
    assert_eq("rejected", code, 1)
    assert_eq("success false", out.get("success"), False)


def test_story_approve_initializes_approvals_array():
    """story-approve initializes planning.approvals array when absent."""
    print("\n[sprint story-approve] Initializes approvals array if absent")
    slug = "my-story"
    proj = setup_project(
        stories={slug: {"status": "ready-for-dev", "title": "My Story", "epic_slug": "e",
                        "story_file": True, "depends_on": [], "touches": []}},
        sprints={"active": None,
                 "planning": {"slug": "s", "locked": False, "status": "planning",
                              "stories": [slug]},
                 "completed": []}
    )
    setup_story_file(proj, slug, "# Content\n")
    # No approvals key initially
    data = read_sprints(proj)
    assert_eq("no approvals key yet", "approvals" not in data["planning"], True)

    code, out = run_tool(proj, "sprint", "story-approve",
                         "--slug", slug, "--decision", "approved")
    assert_eq("exit code 0", code, 0)

    data = read_sprints(proj)
    assert_eq("approvals key created", "approvals" in data["planning"], True)
    assert_eq("one entry", len(data["planning"]["approvals"]), 1)


def test_verify_approvals_all_approved():
    """verify-approvals returns success when all stories have matching approved entries."""
    print("\n[sprint verify-approvals] All approved — success")
    slug = "my-story"
    proj = setup_project(
        stories={slug: {"status": "ready-for-dev", "title": "My Story", "epic_slug": "e",
                        "story_file": True, "depends_on": [], "touches": []}},
        sprints={"active": None,
                 "planning": {"slug": "s", "locked": False, "status": "planning",
                              "stories": [slug]},
                 "completed": []}
    )
    story_path = setup_story_file(proj, slug, "# Content\n")
    sha = compute_file_sha(story_path)

    # Set up the approval entry manually
    data = read_sprints(proj)
    data["planning"]["approvals"] = [{"story_slug": slug, "decision": "approved",
                                       "approved_at": "2026-04-30T00:00:00Z",
                                       "story_file_sha": sha}]
    (proj / ".momentum" / "sprints" / "index.json").write_text(
        json.dumps(data, indent=2) + "\n")

    code, out = run_tool(proj, "sprint", "verify-approvals", "--scope", "planning")
    assert_eq("exit code 0", code, 0)
    assert_eq("success true", out.get("success"), True)
    assert_eq("missing empty", out.get("missing", []), [])


def test_verify_approvals_missing_approval():
    """verify-approvals fails when a story has no approval entry."""
    print("\n[sprint verify-approvals] Missing approval — fails")
    slug = "my-story"
    proj = setup_project(
        stories={slug: {"status": "ready-for-dev", "title": "My Story", "epic_slug": "e",
                        "story_file": True, "depends_on": [], "touches": []}},
        sprints={"active": None,
                 "planning": {"slug": "s", "locked": False, "status": "planning",
                              "stories": [slug],
                              "approvals": []},
                 "completed": []}
    )
    setup_story_file(proj, slug, "# Content\n")

    code, out = run_tool(proj, "sprint", "verify-approvals", "--scope", "planning")
    assert_eq("rejected", code, 1)
    assert_eq("success false", out.get("success"), False)
    assert_eq("missing contains slug", slug in out.get("missing", []), True)


def test_verify_approvals_sha_mismatch():
    """verify-approvals fails when story file was edited after approval (SHA mismatch)."""
    print("\n[sprint verify-approvals] SHA mismatch — fails")
    slug = "my-story"
    proj = setup_project(
        stories={slug: {"status": "ready-for-dev", "title": "My Story", "epic_slug": "e",
                        "story_file": True, "depends_on": [], "touches": []}},
        sprints={"active": None,
                 "planning": {"slug": "s", "locked": False, "status": "planning",
                              "stories": [slug],
                              "approvals": [{"story_slug": slug, "decision": "approved",
                                             "approved_at": "2026-04-30T00:00:00Z",
                                             "story_file_sha": "old-sha-value"}]},
                 "completed": []}
    )
    setup_story_file(proj, slug, "# Updated content after approval\n")

    code, out = run_tool(proj, "sprint", "verify-approvals", "--scope", "planning")
    assert_eq("rejected", code, 1)
    assert_eq("success false", out.get("success"), False)
    assert_eq("slug in missing", slug in out.get("missing", []), True)


def test_verify_approvals_active_scope():
    """verify-approvals --scope active reads from active sprint."""
    print("\n[sprint verify-approvals] Active scope")
    slug = "my-story"
    story_path_placeholder = None
    proj = setup_project(
        stories={slug: {"status": "in-progress", "title": "My Story", "epic_slug": "e",
                        "story_file": True, "depends_on": [], "touches": []}},
        sprints={"active": {"slug": "s", "locked": True, "status": "active",
                            "stories": [slug],
                            "approvals": [{"story_slug": slug, "decision": "approved",
                                           "approved_at": "2026-04-30T00:00:00Z",
                                           "story_file_sha": "placeholder-sha"}]},
                 "planning": None, "completed": []}
    )
    story_path = setup_story_file(proj, slug, "# Content\n")
    real_sha = compute_file_sha(story_path)

    # Update approval to have the real SHA
    data = read_sprints(proj)
    data["active"]["approvals"][0]["story_file_sha"] = real_sha
    (proj / ".momentum" / "sprints" / "index.json").write_text(
        json.dumps(data, indent=2) + "\n")

    code, out = run_tool(proj, "sprint", "verify-approvals", "--scope", "active")
    assert_eq("exit code 0", code, 0)
    assert_eq("success true", out.get("success"), True)


def test_activate_blocked_missing_approval():
    """sprint activate fails when approvals are missing."""
    print("\n[sprint activate] Blocked — missing approval")
    slug = "my-story"
    proj = setup_project(
        stories={slug: {"status": "ready-for-dev", "title": "My Story", "epic_slug": "e",
                        "story_file": True, "depends_on": [], "touches": []}},
        sprints={"active": None,
                 "planning": {"slug": "test-sprint", "locked": False, "status": "planning",
                              "stories": [slug],
                              "approvals": []},
                 "completed": []}
    )
    setup_story_file(proj, slug, "# Content\n")

    code, out = run_tool(proj, "sprint", "activate")
    assert_eq("rejected", code, 1)
    assert_eq("success false", out.get("success"), False)
    assert_eq("error mentions missing", "missing" in out.get("error", "").lower()
              or len(out.get("missing", [])) > 0, True)


def test_activate_blocked_sha_mismatch():
    """sprint activate fails when story file SHA mismatches approval record."""
    print("\n[sprint activate] Blocked — SHA mismatch")
    slug = "my-story"
    proj = setup_project(
        stories={slug: {"status": "ready-for-dev", "title": "My Story", "epic_slug": "e",
                        "story_file": True, "depends_on": [], "touches": []}},
        sprints={"active": None,
                 "planning": {"slug": "test-sprint", "locked": False, "status": "planning",
                              "stories": [slug],
                              "approvals": [{"story_slug": slug, "decision": "approved",
                                             "approved_at": "2026-04-30T00:00:00Z",
                                             "story_file_sha": "stale-sha"}]},
                 "completed": []}
    )
    setup_story_file(proj, slug, "# Content changed after approval\n")

    code, out = run_tool(proj, "sprint", "activate")
    assert_eq("rejected", code, 1)
    assert_eq("success false", out.get("success"), False)


def test_activate_succeeds_all_approved():
    """sprint activate succeeds when all stories have matching approved SHAs."""
    print("\n[sprint activate] Succeeds when all approved")
    slug = "my-story"
    proj = setup_project(
        stories={slug: {"status": "ready-for-dev", "title": "My Story", "epic_slug": "e",
                        "story_file": True, "depends_on": [], "touches": []}},
        sprints={"active": None,
                 "planning": {"slug": "test-sprint", "locked": False, "status": "planning",
                              "stories": [slug]},
                 "completed": []}
    )
    story_path = setup_story_file(proj, slug, "# Approved story content.\n")
    sha = compute_file_sha(story_path)

    # Write approval with correct SHA
    data = read_sprints(proj)
    data["planning"]["approvals"] = [{"story_slug": slug, "decision": "approved",
                                       "approved_at": "2026-04-30T00:00:00Z",
                                       "story_file_sha": sha}]
    (proj / ".momentum" / "sprints" / "index.json").write_text(
        json.dumps(data, indent=2) + "\n")

    code, out = run_tool(proj, "sprint", "activate")
    assert_eq("exit code 0", code, 0)
    assert_eq("success true", out.get("success"), True)

    result = read_sprints(proj)
    assert_eq("sprint activated", result["active"]["slug"], "test-sprint")
    assert_eq("approvals carried over", len(result["active"].get("approvals", [])), 1)


def test_activate_approvals_carried_to_active():
    """Approvals array is carried verbatim from planning to active on activation."""
    print("\n[sprint activate] Approvals carried to active sprint")
    slug = "my-story"
    proj = setup_project(
        stories={slug: {"status": "ready-for-dev", "title": "My Story", "epic_slug": "e",
                        "story_file": True, "depends_on": [], "touches": []}},
        sprints={"active": None,
                 "planning": {"slug": "test-sprint", "locked": False, "status": "planning",
                              "stories": [slug]},
                 "completed": []}
    )
    story_path = setup_story_file(proj, slug, "# Content\n")
    sha = compute_file_sha(story_path)

    data = read_sprints(proj)
    data["planning"]["approvals"] = [{"story_slug": slug, "decision": "approved",
                                       "approved_at": "2026-04-30T12:00:00Z",
                                       "story_file_sha": sha}]
    (proj / ".momentum" / "sprints" / "index.json").write_text(
        json.dumps(data, indent=2) + "\n")

    run_tool(proj, "sprint", "activate")
    result = read_sprints(proj)
    approvals = result["active"].get("approvals", [])
    assert_eq("one approval on active", len(approvals), 1)
    assert_eq("sha preserved", approvals[0].get("story_file_sha"), sha)
    assert_eq("timestamp preserved", approvals[0].get("approved_at"), "2026-04-30T12:00:00Z")


def test_activate_no_approvals_when_no_stories():
    """sprint activate with no stories in planning still succeeds (empty approvals OK)."""
    print("\n[sprint activate] No stories — succeeds (no approvals needed)")
    proj = setup_project(
        sprints={"active": None,
                 "planning": {"slug": "test-sprint", "locked": False, "status": "planning",
                              "stories": [],
                              "approvals": []},
                 "completed": []}
    )
    code, out = run_tool(proj, "sprint", "activate")
    assert_eq("exit code 0", code, 0)


# --- Runner ---

def main():
    global PASS_COUNT, FAIL_COUNT

    print("momentum-tools test suite")
    print("=" * 50)

    test_valid_forward_transition()
    test_invalid_non_adjacent_forward()
    test_invalid_backward_transition()
    test_terminal_state_blocked()
    test_force_override()
    test_dropped_from_any_non_terminal()
    test_closed_incomplete_from_any_non_terminal()
    test_story_not_found()
    test_data_preservation()
    test_sprint_activate()
    test_sprint_activate_already_active()
    test_sprint_activate_no_planning()
    test_sprint_complete()
    test_sprint_complete_no_active()
    test_epic_membership()
    test_epic_membership_not_found()
    test_sprint_plan_add()
    test_sprint_plan_remove()
    test_sprint_plan_locked()
    test_sprint_plan_no_duplicates()

    # Sprint status field tests
    test_sprint_plan_sets_status_planning()
    test_sprint_activate_sets_status_active()
    test_sprint_complete_sets_status_done()

    # Sprint ready tests
    test_sprint_ready_sets_status_ready()
    test_sprint_ready_no_planning()

    # Sprint retro-complete tests
    test_sprint_retro_complete_basic()
    test_sprint_retro_complete_auto_activates()
    test_sprint_retro_complete_no_auto_activate_when_planning()
    test_sprint_retro_complete_no_completed_sprints()

    # Sprint next-stories tests
    test_next_stories_all_unblocked()
    test_next_stories_some_blocked()
    test_next_stories_done_excluded()
    test_next_stories_no_active_sprint()

    # Session stats-update tests
    test_session_stats_update_creates()
    test_session_stats_update_increments()
    test_session_stats_update_preserves_data()

    # Session greeting-state tests
    test_greeting_state_first_session()
    test_greeting_state_active_in_progress()
    test_greeting_state_active_not_started()
    test_greeting_state_active_blocked()
    test_greeting_state_done_retro_needed()
    test_greeting_state_no_active_nothing_planned()
    test_greeting_state_no_active_planned_ready()
    test_greeting_state_active_planned_needs_work()
    test_greeting_state_done_no_planned()

    # Session startup-preflight tests
    test_startup_preflight_all_current()
    test_startup_preflight_needs_upgrade()
    test_startup_preflight_hash_drift()
    test_startup_preflight_first_install()
    test_startup_preflight_journal_threads()

    # Specialist classify tests
    test_specialist_classify_dev_skills()
    test_specialist_classify_dev_build()
    test_specialist_classify_dev_frontend()
    test_specialist_classify_no_match()
    test_specialist_classify_majority_rule()
    test_specialist_classify_tie_table_order()
    test_specialist_classify_empty_touches()
    test_specialist_classify_fallback_missing_agent()

    # Quickfix tests
    test_quickfix_register_creates_array()
    test_quickfix_register_correct_fields()
    test_quickfix_register_auto_increment()
    test_quickfix_register_empty_story()
    test_quickfix_complete_sets_date()
    test_quickfix_complete_missing_slug()
    test_quickfix_complete_idempotent()
    test_quickfix_round_trip()

    # Priority field tests
    test_priority_default_on_new_entry()
    test_priority_migrate_idempotent()
    test_set_priority_valid()
    test_set_priority_all_valid_levels()
    test_set_priority_invalid_level()
    test_set_priority_missing_story()
    test_set_priority_idempotent()
    test_sprint_stories_single_priority()
    test_sprint_stories_all_grouped()
    test_sprint_stories_invalid_priority()
    test_sprint_stories_empty_results()
    test_sprint_stories_missing_priority_defaults_low()

    # Journal status tests
    test_journal_status_no_file()
    test_journal_status_empty_file()
    test_journal_status_open_threads()
    test_journal_status_closed_threads()
    test_journal_status_malformed_lines()
    test_journal_status_thread_summary()

    # Journal hygiene tests
    test_journal_hygiene_no_file()
    test_journal_hygiene_no_open_threads()
    test_journal_hygiene_sort_order()
    test_journal_hygiene_elapsed_labels()
    test_journal_hygiene_concurrent_warning()
    test_journal_hygiene_dormant_warning()
    test_journal_hygiene_dependency_satisfied()
    test_journal_hygiene_dependency_satisfied_uses_context_summary_short()
    test_journal_hygiene_unwieldy()
    test_journal_hygiene_no_reoff_suppression()
    test_journal_hygiene_no_reoff_context_change()
    test_journal_hygiene_suggested_prompts()

    # Journal append tests
    test_journal_append_creates_file()
    test_journal_append_appends_line()
    test_journal_append_invalid_json()
    test_journal_append_regenerates_view()
    test_journal_append_view_includes_recent_closed()

    # Feature status hash tests
    test_feature_status_hash_no_features_file()
    test_feature_status_hash_with_features_file()
    test_feature_status_hash_deterministic()
    test_feature_status_hash_changes_on_features_change()
    test_feature_status_hash_changes_on_stories_change()

    # Preflight feature status tests
    test_preflight_feature_status_no_features()
    test_preflight_feature_status_no_cache()
    test_preflight_feature_status_fresh()
    test_preflight_feature_status_stale()
    test_preflight_feature_status_invalid_cache_json()

    # Greeting-state feature status tests
    test_greeting_state_feature_status_no_features()
    test_greeting_state_feature_status_no_cache()
    test_greeting_state_feature_status_fresh()
    test_greeting_state_feature_status_stale()

    # story-add --feature-slug / --story-type tests
    test_story_add_default_story_type()
    test_story_add_explicit_story_type()
    test_story_add_invalid_story_type()
    test_story_add_feature_slug_persisted()
    test_story_add_feature_slug_omitted_when_empty()

    # .momentum/ path migration tests
    test_stories_path_resolves_to_momentum()
    test_sprints_path_resolves_to_momentum()

    # session plugin-cache-check tests
    test_plugin_cache_check_match()
    test_plugin_cache_check_cache_behind()
    test_plugin_cache_check_cache_ahead()
    test_plugin_cache_check_no_cache_dir()
    test_plugin_cache_check_no_source()
    test_plugin_cache_check_malformed_cache_json()
    test_plugin_cache_check_malformed_source_json()
    test_plugin_cache_check_missing_version_field()
    test_plugin_cache_check_multiple_cache_versions_highest_selected()
    test_plugin_cache_check_exit_code_zero_on_skew()

    # _parse_semver unit tests (AVFL-019)
    test_parse_semver_rc_sorts_before_release()
    test_parse_semver_release_sorts_before_next()
    test_parse_semver_rc1_sorts_before_rc2()
    test_parse_semver_standard_ordering()

    # Story approval tests (Task 1 / Task 6)
    test_story_approve_writes_approved_entry()
    test_story_approve_writes_rejected_entry()
    test_story_approve_replaces_prior_entry()
    test_story_approve_no_planning_sprint()
    test_story_approve_slug_not_in_sprint()
    test_story_approve_initializes_approvals_array()
    test_verify_approvals_all_approved()
    test_verify_approvals_missing_approval()
    test_verify_approvals_sha_mismatch()
    test_verify_approvals_active_scope()
    test_activate_blocked_missing_approval()
    test_activate_blocked_sha_mismatch()
    test_activate_succeeds_all_approved()
    test_activate_approvals_carried_to_active()
    test_activate_no_approvals_when_no_stories()

    # Triage prefilter tests
    test_prefilter_recall_duplicate_pairs()
    test_prefilter_status_filter_excludes_terminal()
    test_prefilter_empty_backlog()
    test_prefilter_index_not_found()
    test_prefilter_single_item_batch()
    test_prefilter_all_identical_batch()
    test_prefilter_score_fields_present()
    test_prefilter_epic_boost_applied()
    test_prefilter_intra_batch_matrix_dimensions()
    test_prefilter_known_duplicates_from_ac15()
    test_prefilter_runs_triage_group()

    # Practice ledger tests (A1 / DEC-033)
    # Task 2: append writer
    test_practice_ledger_append_creates_file()
    test_practice_ledger_append_correct_fields()
    test_practice_ledger_append_invalid_event_type()
    test_practice_ledger_append_all_valid_event_types()
    test_practice_ledger_append_two_sequential_both_land()
    test_practice_ledger_append_custom_event_type_field()
    test_practice_ledger_append_event_ids_unique()
    # Task 3: append-only consume
    test_practice_ledger_consume_appends_event()
    test_practice_ledger_consume_nonexistent_entity_still_appends()
    test_practice_ledger_consume_twice_both_land()
    # Task 4: DuckDB reader CLI
    test_practice_ledger_summary_empty()
    test_practice_ledger_summary_counts_by_event_type()
    test_practice_ledger_summary_archive_entries()
    test_practice_ledger_open_returns_nonterminal()
    test_practice_ledger_open_terminal_types()
    test_practice_ledger_history_returns_ordered_events()
    test_practice_ledger_history_unknown_entity_empty()
    test_practice_ledger_since_filters_by_ts()
    test_practice_ledger_by_source_filters()
    test_practice_ledger_summary_text_format()
    test_practice_ledger_help_subcommands_registered()
    # Task 5: close-stale
    test_practice_ledger_close_stale_appends_events()
    test_practice_ledger_close_stale_idempotent()
    test_practice_ledger_close_stale_respects_ttl()
    test_practice_ledger_close_stale_skips_terminal()
    # Task 9: end-to-end
    test_practice_ledger_e2e_full_lifecycle()
    test_practice_ledger_e2e_migration_boundary()
    test_practice_ledger_e2e_close_stale_idempotency()

    print(f"\n{'=' * 50}")
    print(f"Results: {PASS_COUNT} passed, {FAIL_COUNT} failed")

    sys.exit(1 if FAIL_COUNT > 0 else 0)


# --- Triage Prefilter Tests ---

def setup_prefilter_project(stories: dict) -> Path:
    """Create a temp project with stories/index.json for prefilter tests."""
    return setup_project(stories=stories)


def run_prefilter(project_dir: Path, items: list, stories: dict | None = None) -> tuple[int, dict]:
    """Run triage prefilter subcommand. stories arg overrides what's in project_dir if provided."""
    import tempfile
    index_path = project_dir / ".momentum" / "stories" / "index.json"
    if stories is not None:
        index_path.write_text(json.dumps(stories, indent=2))
    return run_tool(project_dir, "triage", "prefilter",
                    "--items-json", json.dumps(items),
                    "--stories-index", str(index_path))


def _make_story(title: str, description: str = "", epic_slug: str = "test-epic",
                feature_slug: str = "", status: str = "backlog",
                touches: list | None = None) -> dict:
    """Build a minimal story index entry."""
    entry: dict = {
        "status": status, "title": title, "description": description,
        "epic_slug": epic_slug, "story_file": False,
        "depends_on": [], "touches": touches or []
    }
    if feature_slug:
        entry["feature_slug"] = feature_slug
    return entry


def _make_item(item_id: str, title: str, description: str = "", epic_slug: str = "",
               feature_slug: str = "", touches: list | None = None) -> dict:
    """Build a minimal incoming item for prefilter input."""
    return {
        "id": item_id, "title": title, "description": description,
        "epic_slug": epic_slug, "feature_slug": feature_slug,
        "touches": touches or []
    }


def test_prefilter_recall_duplicate_pairs():
    """Recall fixture: ≥5 synthetic duplicate pairs, recall ≥95% at K=10."""
    print("\n[triage prefilter] Recall fixture (≥5 pairs, ≥95% recall at K=10)")
    # Build 6 duplicate pairs: each item is a paraphrase of its matching story
    pairs = [
        ("iq-p1", "add e2e validator service URL configuration",
         "e2e-validator-hardened", "e2e validator should read service URLs from config not hardcode them",
         "validator hardcoded URLs need to be configurable via environment variable"),
        ("iq-p2", "agent spawn preflight context tier check",
         "agent-preflight-check", "preflight check before spawning subagents validates context tier",
         "add preflight validation step to verify context level before agent spawn"),
        ("iq-p3", "triage dedup gate for backlog hygiene",
         "triage-dedup-gate", "dedup gate in triage prevents duplicate stories from entering backlog",
         "implement deduplication step in triage workflow to catch backlog duplicates"),
        ("iq-p4", "intake queue status filter removes terminal stories",
         "intake-queue-status-filter", "status filter in intake queue excludes done and dropped stories",
         "filter terminal status stories from intake queue processing"),
        ("iq-p5", "retro auditor fan-out parallel spawn",
         "retro-auditor-fanout", "retro spawns three auditors in parallel using fan-out pattern",
         "retro Phase 4 spawns auditors as parallel subagents not sequential"),
        ("iq-p6", "sprint planning wave ordering dependencies",
         "sprint-wave-order", "sprint planning groups stories into waves respecting dependency order",
         "wave-based story ordering in sprint planning respects depends_on fields"),
    ]

    # Build stories index with true matches (high similarity) plus distractors
    stories: dict = {}
    true_slugs: dict[str, str] = {}
    for item_id, item_title, story_slug, story_title, story_desc in pairs:
        stories[story_slug] = _make_story(story_title, story_desc)
        true_slugs[item_id] = story_slug

    # Add distractor stories with unrelated topics
    for i in range(20):
        stories[f"distractor-{i}"] = _make_story(
            f"unrelated topic {i} completely different domain",
            f"nothing to do with the query items, domain {i}"
        )

    items = [_make_item(item_id, item_title)
             for item_id, item_title, _, _, _, in pairs]

    proj = setup_prefilter_project(stories)
    code, out = run_prefilter(proj, items)
    assert_eq("exit code 0", code, 0)
    assert_eq("success true", out.get("success"), True)

    shortlists = out.get("shortlists", {})
    hits = 0
    total = len(pairs)
    for item_id, _, true_slug, _, _ in pairs:
        candidates = shortlists.get(item_id, [])
        candidate_slugs = [c["slug"] for c in candidates]
        if true_slug in candidate_slugs:
            hits += 1
        else:
            print(f"    MISS: item={item_id} expected={true_slug} got top3={candidate_slugs[:3]}")

    recall = hits / total if total > 0 else 0.0
    assert_eq(f"recall ≥95% at K=10 ({hits}/{total} = {recall:.2%})", recall >= 0.95, True)


def test_prefilter_status_filter_excludes_terminal():
    """Terminal-status stories must not appear in any shortlist."""
    print("\n[triage prefilter] Status filter excludes terminal stories")
    terminal_slug = "done-story"
    non_terminal_slug = "active-story"
    stories = {
        terminal_slug: _make_story("add authentication flow to login page",
                                   "implement user login with JWT tokens",
                                   status="done"),
        non_terminal_slug: _make_story("add authentication flow to login page",
                                       "implement user login with JWT tokens",
                                       status="backlog"),
    }
    # Also test dropped and closed-incomplete
    stories["dropped-story"] = _make_story("add authentication flow to login page",
                                           "implement user login with JWT tokens",
                                           status="dropped")
    stories["closed-story"] = _make_story("add authentication flow to login page",
                                          "implement user login with JWT tokens",
                                          status="closed-incomplete")

    items = [_make_item("iq-001", "add authentication flow to login page",
                        "implement user login with JWT tokens")]
    proj = setup_prefilter_project(stories)
    code, out = run_prefilter(proj, items)
    assert_eq("exit code 0", code, 0)

    candidates = out.get("shortlists", {}).get("iq-001", [])
    slugs = [c["slug"] for c in candidates]
    assert_eq("done story excluded", terminal_slug not in slugs, True)
    assert_eq("dropped story excluded", "dropped-story" not in slugs, True)
    assert_eq("closed-incomplete story excluded", "closed-story" not in slugs, True)
    assert_eq("backlog story included", non_terminal_slug in slugs, True)


def test_prefilter_empty_backlog():
    """Empty stories index (file exists, zero stories) returns empty shortlists."""
    print("\n[triage prefilter] Empty backlog edge case")
    proj = setup_prefilter_project({})
    items = [_make_item("iq-001", "some incoming item title")]
    index_path = proj / ".momentum" / "stories" / "index.json"
    index_path.write_text("{}\n")
    code, out = run_prefilter(proj, items)
    assert_eq("exit code 0", code, 0)
    assert_eq("success true", out.get("success"), True)
    shortlists = out.get("shortlists", {})
    assert_eq("iq-001 has empty shortlist", shortlists.get("iq-001"), [])


def test_prefilter_index_not_found():
    """Missing index file computes real item-item cosines, not hardcoded zeros."""
    print("\n[triage prefilter] Missing index file produces real cosines")
    proj = setup_prefilter_project({})
    text = "intake queue deduplication logic refactor performance"
    items = [
        _make_item("iq-001", text),
        _make_item("iq-002", text),
    ]
    # Delete the index file to exercise the if-not-exists early-exit branch
    index_path = proj / ".momentum" / "stories" / "index.json"
    index_path.unlink()
    code, out = run_prefilter(proj, items)
    assert_eq("exit code 0", code, 0)
    assert_eq("success true", out.get("success"), True)
    matrix = out.get("similarity_matrix", [])
    off_diag = [e for e in matrix if e["item_i"] != e["item_j"]]
    assert_eq("matrix has off-diagonal entries", len(off_diag) > 0, True)
    # Identical items must have real cosine > 0, not hardcoded zero
    for entry in off_diag:
        assert_eq("off-diagonal cosine is real (>0 for identical items)",
                  entry.get("cosine_similarity", 0.0) > 0.0, True)


def test_prefilter_single_item_batch():
    """Single-item batch produces a 1x1 similarity matrix (self-entry)."""
    print("\n[triage prefilter] Single-item batch produces 1x1 matrix")
    stories = {"s1": _make_story("some story title", "some story description")}
    items = [_make_item("iq-001", "something something")]
    proj = setup_prefilter_project(stories)
    code, out = run_prefilter(proj, items)
    assert_eq("exit code 0", code, 0)
    matrix = out.get("similarity_matrix", [])
    assert_eq("matrix has exactly 1 entry (1x1)", len(matrix), 1)
    entry = matrix[0]
    assert_eq("item_i == item_j (self)", entry.get("item_i"), entry.get("item_j"))
    assert_eq("self-similarity == 1.0", entry.get("cosine_similarity"), 1.0)


def test_prefilter_all_identical_batch():
    """All-identical items produce inter-item cosine similarities ≥0.4 in matrix."""
    print("\n[triage prefilter] All-identical batch edge case")
    text = "refactor intake queue deduplication logic to improve performance"
    stories = {"dummy-s": _make_story("some unrelated story")}
    # 3 identical incoming items
    items = [_make_item(f"iq-00{i}", text, text) for i in range(1, 4)]
    proj = setup_prefilter_project(stories)
    code, out = run_prefilter(proj, items)
    assert_eq("exit code 0", code, 0)
    matrix = out.get("similarity_matrix", [])
    # Check all non-self pairs
    off_diag = [e for e in matrix if e["item_i"] != e["item_j"]]
    assert_eq(f"matrix has {len(items)**2 - len(items)} off-diagonal entries",
              len(off_diag), len(items) * len(items) - len(items))
    low_pairs = [e for e in off_diag if e["cosine_similarity"] < 0.4]
    assert_eq("all inter-item similarities ≥0.4 for identical items",
              len(low_pairs), 0)


def test_prefilter_score_fields_present():
    """Each shortlist entry contains all required score breakdown fields."""
    print("\n[triage prefilter] Score fields present in shortlist entries")
    stories = {
        "story-a": _make_story("add dedup logic to triage workflow", "dedup prevents backlog duplicates"),
    }
    items = [_make_item("iq-001", "add dedup logic to triage", "prevents duplicate backlog entries")]
    proj = setup_prefilter_project(stories)
    code, out = run_prefilter(proj, items)
    assert_eq("exit code 0", code, 0)
    candidates = out.get("shortlists", {}).get("iq-001", [])
    assert_eq("at least one candidate returned", len(candidates) >= 1, True)
    entry = candidates[0]
    for field in ("slug", "title", "tfidf_score", "jaccard_score", "epic_boost", "combined_score"):
        assert_eq(f"field '{field}' present", field in entry, True)


def test_prefilter_epic_boost_applied():
    """Epic/feature_slug match gives +0.1 boost to combined_score."""
    print("\n[triage prefilter] Epic boost applied on slug match")
    stories = {
        "matching-epic-story": _make_story("configure service endpoint override", status="backlog",
                                            epic_slug="agent-team-model"),
        "different-epic-story": _make_story("configure service endpoint override", status="backlog",
                                             epic_slug="other-epic"),
    }
    items = [_make_item("iq-001", "configure service endpoint override",
                        epic_slug="agent-team-model")]
    proj = setup_prefilter_project(stories)
    code, out = run_prefilter(proj, items)
    assert_eq("exit code 0", code, 0)
    candidates = out.get("shortlists", {}).get("iq-001", [])
    by_slug = {c["slug"]: c for c in candidates}
    match = by_slug.get("matching-epic-story")
    other = by_slug.get("different-epic-story")
    if match and other:
        assert_eq("matching epic has epic_boost=0.1", match["epic_boost"], 0.1)
        assert_eq("different epic has epic_boost=0.0", other["epic_boost"], 0.0)
        assert_eq("matching epic combined > different epic combined",
                  match["combined_score"] > other["combined_score"], True)
    else:
        assert_eq("both candidates in shortlist", len(candidates) >= 2, True)


def test_prefilter_intra_batch_matrix_dimensions():
    """NxN similarity matrix has exactly N*N entries for N items."""
    print("\n[triage prefilter] Intra-batch matrix is NxN")
    N = 4
    stories = {"s1": _make_story("story title")}
    items = [_make_item(f"iq-{i}", f"incoming item number {i} about topic {i}") for i in range(N)]
    proj = setup_prefilter_project(stories)
    code, out = run_prefilter(proj, items)
    assert_eq("exit code 0", code, 0)
    matrix = out.get("similarity_matrix", [])
    assert_eq(f"matrix has {N*N} entries for N={N} items", len(matrix), N * N)


def test_prefilter_known_duplicates_from_ac15():
    """AC 15: known duplicate items from real intake queue appear in shortlists."""
    print("\n[triage prefilter] Known duplicates from AC 15 appear in top-10")
    # Use the real stories index which contains both target stories
    real_index = Path("/Users/steve/projects/momentum/.momentum/stories/index.json")
    if not real_index.exists():
        print("  SKIP: real stories index not found")
        return

    items = [
        _make_item("iq-20260521002617-b66bc747",
                   "e2e-validator hardcoded service assumptions",
                   "e2e validator hardcodes service URLs and assumptions"),
        _make_item("iq-20260521002732-9cde80f6",
                   "subagent spawn pre-flight context tier check",
                   "preflight validation of context tier before spawning subagents"),
    ]
    proj = setup_prefilter_project({})
    index_path = proj / ".momentum" / "stories" / "index.json"
    index_path.write_text(real_index.read_text())

    code, out = run_prefilter(proj, items)
    assert_eq("exit code 0", code, 0)

    s1 = out.get("shortlists", {}).get("iq-20260521002617-b66bc747", [])
    s1_slugs = [c["slug"] for c in s1]
    assert_eq("e2e-validator-black-box-hardening in top-10",
              "e2e-validator-black-box-hardening" in s1_slugs, True)

    s2 = out.get("shortlists", {}).get("iq-20260521002732-9cde80f6", [])
    s2_slugs = [c["slug"] for c in s2]
    assert_eq("agent-spawn-preflight-check in top-10",
              "agent-spawn-preflight-check" in s2_slugs, True)


def test_prefilter_runs_triage_group():
    """Smoke test: 'triage prefilter' subcommand is registered and reachable."""
    print("\n[triage prefilter] Subcommand registered and reachable")
    import subprocess
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "triage", "prefilter", "--help"],
        capture_output=True, text=True
    )
    assert_eq("--help exits 0", proc.returncode, 0)
    assert_eq("'prefilter' in help text", "prefilter" in proc.stdout.lower(), True)


# ---------------------------------------------------------------------------
# Practice Ledger Tests (A1 story: DEC-033)
# ---------------------------------------------------------------------------


def setup_ledger_project() -> Path:
    """Create a temp project with an empty practice-ledger.jsonl."""
    proj = setup_project()
    (proj / ".momentum" / "practice-ledger.jsonl").write_text("")
    return proj


def read_ledger(proj: Path, filename: str = "practice-ledger.jsonl") -> list:
    """Read JSONL ledger file and return list of parsed events."""
    path = proj / ".momentum" / filename
    if not path.exists():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            events.append(json.loads(line))
    return events


# --- Task 2: practice-ledger append writer ---

def test_practice_ledger_append_creates_file():
    """append creates practice-ledger.jsonl if it does not exist."""
    print("\n[practice-ledger append] Creates file on first write")
    proj = setup_project()
    # No practice-ledger.jsonl yet
    code, out = run_tool(proj, "practice-ledger", "append",
                         "--entity-id", "entity-1",
                         "--event-type", "created",
                         "--source", "triage",
                         "--actor", "test-agent",
                         "--payload", "{}")
    assert_eq("exit code 0", code, 0)
    assert_eq("success true", out.get("success"), True)
    ledger = read_ledger(proj)
    assert_eq("one event written", len(ledger), 1)


def test_practice_ledger_append_correct_fields():
    """append writes all required schema fields."""
    print("\n[practice-ledger append] All required fields present")
    proj = setup_ledger_project()
    code, out = run_tool(proj, "practice-ledger", "append",
                         "--entity-id", "entity-abc",
                         "--event-type", "created",
                         "--source", "retro",
                         "--actor", "impetus",
                         "--payload", '{"title": "hello"}')
    assert_eq("exit code 0", code, 0)
    ledger = read_ledger(proj)
    assert_eq("one event", len(ledger), 1)
    ev = ledger[0]
    assert_eq("event_id present", "event_id" in ev, True)
    assert_eq("entity_id", ev.get("entity_id"), "entity-abc")
    assert_eq("ts present", "ts" in ev, True)
    assert_eq("ts ends in Z", ev["ts"].endswith("Z"), True)
    assert_eq("event_type", ev.get("event_type"), "created")
    assert_eq("source", ev.get("source"), "retro")
    assert_eq("actor", ev.get("actor"), "impetus")
    assert_eq("payload is dict", isinstance(ev.get("payload"), dict), True)
    assert_eq("no custom_event_type", "custom_event_type" not in ev, True)


def test_practice_ledger_append_invalid_event_type():
    """append rejects event_type values outside the enum (argparse or explicit check)."""
    print("\n[practice-ledger append] Invalid event_type rejected")
    proj = setup_ledger_project()
    code, out = run_tool(proj, "practice-ledger", "append",
                         "--entity-id", "entity-1",
                         "--event-type", "invalid-type",
                         "--source", "triage",
                         "--actor", "test",
                         "--payload", "{}")
    assert_eq("rejected with error", code != 0, True)
    # success may be False (JSON error) or absent (argparse error) — both are valid rejection signals
    assert_eq("not success", out.get("success") is not True, True)
    # File must not have any new events
    ledger = read_ledger(proj)
    assert_eq("no event written on rejection", len(ledger), 0)


def test_practice_ledger_append_all_valid_event_types():
    """All seven valid event_type values are accepted."""
    print("\n[practice-ledger append] All 7 event types accepted")
    proj = setup_ledger_project()
    valid_types = ["created", "updated", "consumed", "rejected",
                   "closed_stale", "reopened", "custom"]
    for i, etype in enumerate(valid_types):
        extra_args = []
        if etype == "custom":
            extra_args = ["--custom-event-type", "my_custom_type"]
        code, out = run_tool(proj, "practice-ledger", "append",
                             "--entity-id", f"entity-{i}",
                             "--event-type", etype,
                             "--source", "triage",
                             "--actor", "test",
                             "--payload", "{}",
                             *extra_args)
        assert_eq(f"{etype} accepted", code, 0)
    ledger = read_ledger(proj)
    assert_eq("7 events written", len(ledger), 7)


def test_practice_ledger_append_two_sequential_both_land():
    """Two sequential appends both land — no truncation."""
    print("\n[practice-ledger append] Two sequential appends both land")
    proj = setup_ledger_project()
    run_tool(proj, "practice-ledger", "append",
             "--entity-id", "entity-first",
             "--event-type", "created",
             "--source", "triage",
             "--actor", "test",
             "--payload", "{}")
    run_tool(proj, "practice-ledger", "append",
             "--entity-id", "entity-second",
             "--event-type", "updated",
             "--source", "retro",
             "--actor", "test",
             "--payload", "{}")
    ledger = read_ledger(proj)
    assert_eq("two events", len(ledger), 2)
    assert_eq("first entity_id", ledger[0].get("entity_id"), "entity-first")
    assert_eq("second entity_id", ledger[1].get("entity_id"), "entity-second")


def test_practice_ledger_append_custom_event_type_field():
    """custom event_type includes custom_event_type field."""
    print("\n[practice-ledger append] custom event includes custom_event_type")
    proj = setup_ledger_project()
    code, out = run_tool(proj, "practice-ledger", "append",
                         "--entity-id", "entity-c",
                         "--event-type", "custom",
                         "--source", "triage",
                         "--actor", "test",
                         "--custom-event-type", "sprint_rolled_over",
                         "--payload", "{}")
    assert_eq("exit code 0", code, 0)
    ledger = read_ledger(proj)
    ev = ledger[0]
    assert_eq("event_type custom", ev.get("event_type"), "custom")
    assert_eq("custom_event_type present", ev.get("custom_event_type"), "sprint_rolled_over")


def test_practice_ledger_append_event_ids_unique():
    """Each appended row gets a unique event_id."""
    print("\n[practice-ledger append] event_ids are unique")
    proj = setup_ledger_project()
    for i in range(3):
        run_tool(proj, "practice-ledger", "append",
                 "--entity-id", f"e-{i}",
                 "--event-type", "created",
                 "--source", "triage",
                 "--actor", "test",
                 "--payload", "{}")
    ledger = read_ledger(proj)
    ids = [ev["event_id"] for ev in ledger]
    assert_eq("three unique event_ids", len(set(ids)), 3)


# --- Task 3: append-only consume ---

def test_practice_ledger_consume_appends_event():
    """consume appends a consumed event — does NOT mutate the original created line."""
    print("\n[practice-ledger consume] Appends consumed event, original unchanged")
    proj = setup_ledger_project()
    # Append a created event
    run_tool(proj, "practice-ledger", "append",
             "--entity-id", "entity-to-consume",
             "--event-type", "created",
             "--source", "triage",
             "--actor", "test",
             "--payload", '{"title": "original"}')
    # Read original raw text
    path = proj / ".momentum" / "practice-ledger.jsonl"
    original_text = path.read_text(encoding="utf-8")
    # Consume
    code, out = run_tool(proj, "practice-ledger", "consume",
                         "--entity-id", "entity-to-consume",
                         "--actor", "test",
                         "--outcome-ref", "story-abc")
    assert_eq("exit code 0", code, 0)
    # File should be a superset — original line still there
    new_text = path.read_text(encoding="utf-8")
    assert_eq("original line preserved", original_text.strip() in new_text, True)
    # Two events total
    ledger = read_ledger(proj)
    assert_eq("two events", len(ledger), 2)
    assert_eq("first still created", ledger[0].get("event_type"), "created")
    assert_eq("second is consumed", ledger[1].get("event_type"), "consumed")
    assert_eq("consumed entity_id matches", ledger[1].get("entity_id"), "entity-to-consume")


def test_practice_ledger_consume_nonexistent_entity_still_appends():
    """consume on a non-existent entity_id still appends (audit trail first)."""
    print("\n[practice-ledger consume] Non-existent entity_id still appends consumed event")
    proj = setup_ledger_project()
    code, out = run_tool(proj, "practice-ledger", "consume",
                         "--entity-id", "never-created",
                         "--actor", "test",
                         "--outcome-ref", "")
    assert_eq("exit code 0", code, 0)
    ledger = read_ledger(proj)
    assert_eq("one event appended", len(ledger), 1)
    assert_eq("event_type consumed", ledger[0].get("event_type"), "consumed")


def test_practice_ledger_consume_twice_both_land():
    """Two concurrent consume calls for the same entity_id both land (observable duplicate)."""
    print("\n[practice-ledger consume] Two consume calls both land")
    proj = setup_ledger_project()
    run_tool(proj, "practice-ledger", "append",
             "--entity-id", "shared-entity",
             "--event-type", "created",
             "--source", "triage",
             "--actor", "test",
             "--payload", "{}")
    run_tool(proj, "practice-ledger", "consume",
             "--entity-id", "shared-entity",
             "--actor", "consumer-1",
             "--outcome-ref", "ref-1")
    run_tool(proj, "practice-ledger", "consume",
             "--entity-id", "shared-entity",
             "--actor", "consumer-2",
             "--outcome-ref", "ref-2")
    ledger = read_ledger(proj)
    assert_eq("three events total", len(ledger), 3)
    consumed_events = [e for e in ledger if e.get("event_type") == "consumed"]
    assert_eq("two consumed events", len(consumed_events), 2)


# --- Task 4: DuckDB reader CLI ---

def setup_seeded_ledger(proj: Path, events: list) -> None:
    """Write a list of event dicts as JSONL to practice-ledger.jsonl."""
    import uuid
    from datetime import datetime, timezone, timedelta
    path = proj / ".momentum" / "practice-ledger.jsonl"
    lines = []
    for ev in events:
        if "event_id" not in ev:
            ev["event_id"] = f"evt-{uuid.uuid4().hex[:8]}"
        if "ts" not in ev:
            ev["ts"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if "payload" not in ev:
            ev["payload"] = {}
        lines.append(json.dumps(ev))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_practice_ledger_summary_empty():
    """summary returns zero counts on empty ledger."""
    print("\n[practice-ledger summary] Empty ledger returns zero counts")
    proj = setup_ledger_project()
    code, out = run_tool(proj, "practice-ledger", "summary")
    assert_eq("exit code 0", code, 0)
    assert_eq("success true", out.get("success"), True)
    assert_eq("new_entries 0", out.get("new_entries"), 0)


def test_practice_ledger_summary_counts_by_event_type():
    """summary groups counts by event_type."""
    print("\n[practice-ledger summary] Counts by event_type")
    proj = setup_ledger_project()
    setup_seeded_ledger(proj, [
        {"entity_id": "e1", "event_type": "created", "source": "triage", "actor": "a"},
        {"entity_id": "e2", "event_type": "created", "source": "retro", "actor": "a"},
        {"entity_id": "e1", "event_type": "consumed", "source": "triage", "actor": "a"},
    ])
    code, out = run_tool(proj, "practice-ledger", "summary")
    assert_eq("exit code 0", code, 0)
    assert_eq("new_entries 3", out.get("new_entries"), 3)
    by_type = out.get("by_event_type", {})
    assert_eq("created count 2", by_type.get("created"), 2)
    assert_eq("consumed count 1", by_type.get("consumed"), 1)


def test_practice_ledger_summary_archive_entries():
    """summary reports archive_entries from pre-2026-05 file."""
    print("\n[practice-ledger summary] archive_entries count from pre-2026-05 file")
    proj = setup_ledger_project()
    # Create a fake archive with 3 legacy lines (old schema — no event_id)
    archive = proj / ".momentum" / "practice-ledger-pre-2026-05.jsonl"
    archive.write_text(
        '{"id": "old-1", "status": "open"}\n'
        '{"id": "old-2", "status": "open"}\n'
        '{"id": "old-3", "status": "consumed"}\n',
        encoding="utf-8"
    )
    code, out = run_tool(proj, "practice-ledger", "summary")
    assert_eq("exit code 0", code, 0)
    assert_eq("archive_entries 3", out.get("archive_entries"), 3)
    assert_eq("new_entries 0", out.get("new_entries"), 0)


def test_practice_ledger_open_returns_nonterminal():
    """open returns entities whose last event is non-terminal."""
    print("\n[practice-ledger open] Returns only non-terminal entities")
    proj = setup_ledger_project()
    setup_seeded_ledger(proj, [
        {"entity_id": "open-entity", "event_type": "created", "source": "triage", "actor": "a"},
        {"entity_id": "closed-entity", "event_type": "created", "source": "triage", "actor": "a"},
        {"entity_id": "closed-entity", "event_type": "consumed", "source": "triage", "actor": "a"},
    ])
    code, out = run_tool(proj, "practice-ledger", "open")
    assert_eq("exit code 0", code, 0)
    entity_ids = [e.get("entity_id") for e in out.get("entities", [])]
    assert_eq("open-entity present", "open-entity" in entity_ids, True)
    assert_eq("closed-entity absent", "closed-entity" not in entity_ids, True)


def test_practice_ledger_open_terminal_types():
    """open excludes consumed, rejected, closed_stale; includes reopened, created, updated, custom."""
    print("\n[practice-ledger open] Terminal vs non-terminal event types")
    proj = setup_ledger_project()
    from datetime import datetime, timezone
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    setup_seeded_ledger(proj, [
        {"entity_id": "e-consumed", "event_type": "consumed", "source": "triage", "actor": "a", "ts": ts},
        {"entity_id": "e-rejected", "event_type": "rejected", "source": "triage", "actor": "a", "ts": ts},
        {"entity_id": "e-stale", "event_type": "closed_stale", "source": "triage", "actor": "a", "ts": ts},
        {"entity_id": "e-reopened", "event_type": "reopened", "source": "triage", "actor": "a", "ts": ts},
        {"entity_id": "e-created", "event_type": "created", "source": "triage", "actor": "a", "ts": ts},
        {"entity_id": "e-updated", "event_type": "updated", "source": "triage", "actor": "a", "ts": ts},
        {"entity_id": "e-custom", "event_type": "custom", "source": "triage", "actor": "a", "ts": ts},
    ])
    code, out = run_tool(proj, "practice-ledger", "open")
    assert_eq("exit code 0", code, 0)
    entity_ids = [e.get("entity_id") for e in out.get("entities", [])]
    assert_eq("e-consumed excluded", "e-consumed" not in entity_ids, True)
    assert_eq("e-rejected excluded", "e-rejected" not in entity_ids, True)
    assert_eq("e-stale excluded", "e-stale" not in entity_ids, True)
    assert_eq("e-reopened included", "e-reopened" in entity_ids, True)
    assert_eq("e-created included", "e-created" in entity_ids, True)
    assert_eq("e-updated included", "e-updated" in entity_ids, True)
    assert_eq("e-custom included", "e-custom" in entity_ids, True)


def test_practice_ledger_history_returns_ordered_events():
    """history --entity returns all events sorted by ts ascending."""
    print("\n[practice-ledger history] Returns events sorted by ts ascending")
    proj = setup_ledger_project()
    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone.utc)
    ts1 = (now - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
    ts2 = (now - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    ts3 = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    setup_seeded_ledger(proj, [
        {"entity_id": "traced-entity", "event_type": "created", "source": "triage", "actor": "a", "ts": ts1},
        {"entity_id": "other-entity", "event_type": "created", "source": "triage", "actor": "a", "ts": ts2},
        {"entity_id": "traced-entity", "event_type": "updated", "source": "triage", "actor": "a", "ts": ts2},
        {"entity_id": "traced-entity", "event_type": "consumed", "source": "triage", "actor": "a", "ts": ts3},
    ])
    code, out = run_tool(proj, "practice-ledger", "history", "--entity", "traced-entity")
    assert_eq("exit code 0", code, 0)
    events = out.get("events", [])
    assert_eq("three events", len(events), 3)
    assert_eq("all for traced-entity", all(e["entity_id"] == "traced-entity" for e in events), True)
    assert_eq("ordered by ts", [e["event_type"] for e in events], ["created", "updated", "consumed"])


def test_practice_ledger_history_unknown_entity_empty():
    """history --entity for unknown entity returns empty list with exit 0."""
    print("\n[practice-ledger history] Unknown entity returns empty, exit 0")
    proj = setup_ledger_project()
    code, out = run_tool(proj, "practice-ledger", "history", "--entity", "nonexistent")
    assert_eq("exit code 0", code, 0)
    assert_eq("empty events list", len(out.get("events", [])), 0)


def test_practice_ledger_since_filters_by_ts():
    """since <iso-ts> returns events strictly after the given timestamp."""
    print("\n[practice-ledger since] Returns events strictly after timestamp")
    proj = setup_ledger_project()
    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone.utc)
    ts_old = (now - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
    ts_recent = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    cutoff = (now - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    setup_seeded_ledger(proj, [
        {"entity_id": "e-old", "event_type": "created", "source": "triage", "actor": "a", "ts": ts_old},
        {"entity_id": "e-recent", "event_type": "created", "source": "triage", "actor": "a", "ts": ts_recent},
    ])
    code, out = run_tool(proj, "practice-ledger", "since", cutoff)
    assert_eq("exit code 0", code, 0)
    events = out.get("events", [])
    entity_ids = [e.get("entity_id") for e in events]
    assert_eq("recent included", "e-recent" in entity_ids, True)
    assert_eq("old excluded", "e-old" not in entity_ids, True)


def test_practice_ledger_by_source_filters():
    """by-source <source> returns only events with matching source."""
    print("\n[practice-ledger by-source] Filters by source exactly")
    proj = setup_ledger_project()
    setup_seeded_ledger(proj, [
        {"entity_id": "e1", "event_type": "created", "source": "triage", "actor": "a"},
        {"entity_id": "e2", "event_type": "created", "source": "retro", "actor": "a"},
        {"entity_id": "e3", "event_type": "updated", "source": "triage", "actor": "a"},
    ])
    code, out = run_tool(proj, "practice-ledger", "by-source", "triage")
    assert_eq("exit code 0", code, 0)
    events = out.get("events", [])
    assert_eq("two triage events", len(events), 2)
    assert_eq("all source triage", all(e.get("source") == "triage" for e in events), True)


def test_practice_ledger_summary_text_format():
    """summary --format text returns non-JSON human-readable output."""
    print("\n[practice-ledger summary] --format text produces non-JSON output")
    proj = setup_ledger_project()
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "practice-ledger", "summary", "--format", "text"],
        capture_output=True, text=True,
        env={**os.environ, "CLAUDE_PROJECT_DIR": str(proj)}
    )
    assert_eq("exit code 0", proc.returncode, 0)
    # Text format should not be JSON (should not start with '{')
    stdout = proc.stdout.strip()
    assert_eq("not JSON object", stdout.startswith("{"), False)


def test_practice_ledger_help_subcommands_registered():
    """practice-ledger --help lists all expected subcommands."""
    print("\n[practice-ledger] --help lists all subcommands")
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "practice-ledger", "--help"],
        capture_output=True, text=True
    )
    assert_eq("exit code 0", proc.returncode, 0)
    for sub in ["summary", "open", "history", "since", "by-source", "close-stale", "consume"]:
        assert_eq(f"{sub} in help", sub in proc.stdout, True)


# --- Task 5: close-stale subcommand ---

def setup_aged_ledger(proj: Path, age_days: int, count: int) -> None:
    """Seed `count` created events with ts older than age_days."""
    import uuid
    from datetime import datetime, timezone, timedelta
    path = proj / ".momentum" / "practice-ledger.jsonl"
    lines = []
    old_ts = (datetime.now(timezone.utc) - timedelta(days=age_days + 1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    for i in range(count):
        ev = {
            "event_id": f"evt-{uuid.uuid4().hex[:8]}",
            "entity_id": f"stale-entity-{i}",
            "ts": old_ts,
            "event_type": "created",
            "source": "triage",
            "actor": "test",
            "payload": {}
        }
        lines.append(json.dumps(ev))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_practice_ledger_close_stale_appends_events():
    """close-stale appends closed_stale events for stale non-terminal entities."""
    print("\n[practice-ledger close-stale] Appends closed_stale events")
    proj = setup_ledger_project()
    setup_aged_ledger(proj, age_days=20, count=2)
    code, out = run_tool(proj, "practice-ledger", "close-stale", "--age-days", "15")
    assert_eq("exit code 0", code, 0)
    assert_eq("success true", out.get("success"), True)
    assert_eq("closed_count 2", out.get("closed_count"), 2)
    ledger = read_ledger(proj)
    stale_events = [e for e in ledger if e.get("event_type") == "closed_stale"]
    assert_eq("two closed_stale events", len(stale_events), 2)
    for ev in stale_events:
        assert_eq("source is close-stale", ev.get("source"), "momentum-tools-close-stale")
        assert_eq("age_days_at_close in payload", "age_days_at_close" in ev.get("payload", {}), True)


def test_practice_ledger_close_stale_idempotent():
    """close-stale is idempotent: second run appends zero events."""
    print("\n[practice-ledger close-stale] Idempotent — second run adds nothing")
    proj = setup_ledger_project()
    setup_aged_ledger(proj, age_days=20, count=2)
    # First run
    code1, out1 = run_tool(proj, "practice-ledger", "close-stale", "--age-days", "15")
    assert_eq("first run exit 0", code1, 0)
    assert_eq("first run closed 2", out1.get("closed_count"), 2)
    count_after_first = len(read_ledger(proj))
    # Second run
    code2, out2 = run_tool(proj, "practice-ledger", "close-stale", "--age-days", "15")
    assert_eq("second run exit 0", code2, 0)
    assert_eq("second run closed 0", out2.get("closed_count"), 0)
    count_after_second = len(read_ledger(proj))
    assert_eq("no new events on second run", count_after_second, count_after_first)


def test_practice_ledger_close_stale_respects_ttl():
    """close-stale does not close entities younger than --age-days."""
    print("\n[practice-ledger close-stale] Respects TTL — young entities untouched")
    proj = setup_ledger_project()
    import uuid
    from datetime import datetime, timezone, timedelta
    path = proj / ".momentum" / "practice-ledger.jsonl"
    # One old entity (25 days) and one young (5 days)
    old_ts = (datetime.now(timezone.utc) - timedelta(days=25)).strftime("%Y-%m-%dT%H:%M:%SZ")
    young_ts = (datetime.now(timezone.utc) - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        json.dumps({"event_id": f"evt-{uuid.uuid4().hex[:8]}", "entity_id": "old-entity",
                    "ts": old_ts, "event_type": "created", "source": "triage", "actor": "a", "payload": {}}),
        json.dumps({"event_id": f"evt-{uuid.uuid4().hex[:8]}", "entity_id": "young-entity",
                    "ts": young_ts, "event_type": "created", "source": "triage", "actor": "a", "payload": {}}),
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    code, out = run_tool(proj, "practice-ledger", "close-stale", "--age-days", "15")
    assert_eq("exit code 0", code, 0)
    assert_eq("only 1 closed", out.get("closed_count"), 1)
    ledger = read_ledger(proj)
    stale_events = [e for e in ledger if e.get("event_type") == "closed_stale"]
    assert_eq("one stale event", len(stale_events), 1)
    assert_eq("old entity closed", stale_events[0].get("entity_id"), "old-entity")


def test_practice_ledger_close_stale_skips_terminal():
    """close-stale does not close already-terminal entities."""
    print("\n[practice-ledger close-stale] Skips already-terminal entities")
    proj = setup_ledger_project()
    import uuid
    from datetime import datetime, timezone, timedelta
    path = proj / ".momentum" / "practice-ledger.jsonl"
    old_ts = (datetime.now(timezone.utc) - timedelta(days=20)).strftime("%Y-%m-%dT%H:%M:%SZ")
    recent_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        json.dumps({"event_id": f"evt-{uuid.uuid4().hex[:8]}", "entity_id": "consumed-entity",
                    "ts": old_ts, "event_type": "created", "source": "triage", "actor": "a", "payload": {}}),
        json.dumps({"event_id": f"evt-{uuid.uuid4().hex[:8]}", "entity_id": "consumed-entity",
                    "ts": recent_ts, "event_type": "consumed", "source": "triage", "actor": "a", "payload": {}}),
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    code, out = run_tool(proj, "practice-ledger", "close-stale", "--age-days", "15")
    assert_eq("exit code 0", code, 0)
    assert_eq("zero closed", out.get("closed_count"), 0)


# --- Task 9: End-to-end execution tests ---

def test_practice_ledger_e2e_full_lifecycle():
    """AC26: Full lifecycle: create → update → consume → open excludes it → history has 3 events."""
    print("\n[practice-ledger e2e] Full lifecycle test (AC26)")
    proj = setup_ledger_project()
    # create
    run_tool(proj, "practice-ledger", "append",
             "--entity-id", "lifecycle-entity",
             "--event-type", "created",
             "--source", "triage",
             "--actor", "test-agent",
             "--payload", '{"title": "lifecycle test"}')
    # update
    run_tool(proj, "practice-ledger", "append",
             "--entity-id", "lifecycle-entity",
             "--event-type", "updated",
             "--source", "triage",
             "--actor", "test-agent",
             "--payload", '{"title": "lifecycle test updated"}')
    # consume
    run_tool(proj, "practice-ledger", "consume",
             "--entity-id", "lifecycle-entity",
             "--actor", "test-agent",
             "--outcome-ref", "story-123")
    # open should exclude it
    code_open, out_open = run_tool(proj, "practice-ledger", "open")
    assert_eq("open exit 0", code_open, 0)
    open_ids = [e.get("entity_id") for e in out_open.get("entities", [])]
    assert_eq("lifecycle-entity not in open", "lifecycle-entity" not in open_ids, True)
    # history should have 3 events in order
    code_hist, out_hist = run_tool(proj, "practice-ledger", "history",
                                    "--entity", "lifecycle-entity")
    assert_eq("history exit 0", code_hist, 0)
    events = out_hist.get("events", [])
    assert_eq("three events", len(events), 3)
    assert_eq("order: created", events[0].get("event_type"), "created")
    assert_eq("order: updated", events[1].get("event_type"), "updated")
    assert_eq("order: consumed", events[2].get("event_type"), "consumed")


def test_practice_ledger_e2e_migration_boundary():
    """AC27: Migration boundary — archive entries in summary, new file empty."""
    print("\n[practice-ledger e2e] Migration boundary (AC27)")
    proj = setup_project()
    # Create archive with N legacy entries
    archive_path = proj / ".momentum" / "practice-ledger-pre-2026-05.jsonl"
    n_legacy = 7
    legacy_lines = [f'{{"id": "old-{i}", "status": "open"}}' for i in range(n_legacy)]
    archive_path.write_text("\n".join(legacy_lines) + "\n", encoding="utf-8")
    # Empty new ledger
    ledger_path = proj / ".momentum" / "practice-ledger.jsonl"
    ledger_path.write_text("", encoding="utf-8")
    # summary should report archive_entries = N, new_entries = 0
    code, out = run_tool(proj, "practice-ledger", "summary")
    assert_eq("exit code 0", code, 0)
    assert_eq("archive_entries N", out.get("archive_entries"), n_legacy)
    assert_eq("new_entries 0", out.get("new_entries"), 0)


def test_practice_ledger_e2e_close_stale_idempotency():
    """AC28: close-stale idempotency: 2 stale entities → 2 events first, 0 second."""
    print("\n[practice-ledger e2e] close-stale idempotency (AC28)")
    proj = setup_ledger_project()
    setup_aged_ledger(proj, age_days=20, count=2)
    # First run
    code1, out1 = run_tool(proj, "practice-ledger", "close-stale", "--age-days", "15")
    assert_eq("first run exit 0", code1, 0)
    assert_eq("first run 2 closed", out1.get("closed_count"), 2)
    # Run summary to see state
    _, sum1 = run_tool(proj, "practice-ledger", "summary")
    # Second run — must close nothing
    code2, out2 = run_tool(proj, "practice-ledger", "close-stale", "--age-days", "15")
    assert_eq("second run exit 0", code2, 0)
    assert_eq("second run 0 closed", out2.get("closed_count"), 0)


if __name__ == "__main__":
    main()
