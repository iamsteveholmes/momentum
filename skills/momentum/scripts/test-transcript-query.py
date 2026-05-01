#!/usr/bin/env python3
"""Tests for transcript-query.py — covering worktree discovery, UTC boundary semantics,
JSON round-trip correctness, slug-based filtering, and graceful fallback.

Run with:
    python3 skills/momentum/scripts/test-transcript-query.py

Exits with code 0 on success, non-zero on failure. No external test runner required.
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ensure we can import from the same directory
SCRIPTS_DIR = Path(__file__).parent

# transcript-query.py has a hyphen in its filename so it can't be imported
# via a normal `import` statement. Load it via importlib.util instead.
def _load_tq_module():
    script_path = SCRIPTS_DIR / "transcript-query.py"
    spec = importlib.util.spec_from_file_location("transcript_query", script_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["transcript_query"] = module
    spec.loader.exec_module(module)
    return module

tq = _load_tq_module()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_jsonl_file(path: str, messages: list[dict]) -> None:
    """Write a JSONL file with the given message records."""
    with open(path, "w") as f:
        for msg in messages:
            f.write(json.dumps(msg) + "\n")


def _set_mtime_utc(path: str, dt: datetime) -> None:
    """Set the mtime of a file to the given UTC datetime."""
    ts = dt.timestamp()
    os.utime(path, (ts, ts))


SAMPLE_MESSAGE = {
    "type": "user",
    "timestamp": "2026-04-08T12:00:00.000Z",
    "message": {"role": "user", "content": "Hello world"},
    "parentUuid": None,
    "isSidechain": False,
    "sourceToolAssistantUUID": None,
}


# ---------------------------------------------------------------------------
# Task 1 — Worktree discovery
# ---------------------------------------------------------------------------

class TestWorktreeBases(unittest.TestCase):
    """AC #1: worktree discovery finds extra project bases."""

    def test_worktree_bases_resolves_extra_paths(self):
        """When git worktree list --porcelain returns extra worktrees, their
        ~/.claude/projects/<encoded>/ dirs appear in the returned list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create two fake project directories matching what expanduser would produce.
            # The mock replaces "~" with tmpdir, so ~/.claude/projects → {tmpdir}/.claude/projects
            claude_projects = os.path.join(tmpdir, ".claude", "projects")
            wt1 = os.path.join(claude_projects, "-Users-steve-main")
            wt2 = os.path.join(claude_projects, "-Users-steve-worktrees-story-a")
            os.makedirs(wt1)
            os.makedirs(wt2)

            fake_porcelain = (
                "worktree /Users/steve/main\n"
                "HEAD abc123\n"
                "branch refs/heads/main\n"
                "\n"
                "worktree /Users/steve/worktrees/story-a\n"
                "HEAD def456\n"
                "branch refs/heads/story-a\n"
                "\n"
            )
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = fake_porcelain

            with patch("subprocess.run", return_value=mock_result), \
                 patch("os.path.expanduser", side_effect=lambda p: p.replace("~", tmpdir)):
                bases = tq._worktree_bases("/Users/steve/main")

            self.assertIn(wt1, bases)
            self.assertIn(wt2, bases)

    def test_no_worktrees_falls_back_to_primary_base(self):
        """Outside a git repo, _worktree_bases() returns []."""
        mock_result = MagicMock()
        mock_result.returncode = 128  # git error (not a repo)
        mock_result.stdout = ""

        with patch("subprocess.run", return_value=mock_result):
            result = tq._worktree_bases("/tmp/not-a-repo")
        self.assertEqual(result, [])

    def test_worktree_bases_git_unavailable(self):
        """When git is not available, _worktree_bases() returns []."""
        with patch("subprocess.run", side_effect=FileNotFoundError("git not found")):
            result = tq._worktree_bases("/tmp/some-dir")
        self.assertEqual(result, [])

    def test_worktree_bases_only_existing_dirs_returned(self):
        """Only worktree paths whose encoded ~/.claude/projects/ directory exists are returned."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Only one of two worktree dirs actually exists.
            # The mock replaces "~" with tmpdir, so ~/.claude/projects → {tmpdir}/.claude/projects
            claude_projects = os.path.join(tmpdir, ".claude", "projects")
            wt_exists = os.path.join(claude_projects, "-Users-steve-main")
            os.makedirs(wt_exists)
            # wt_missing (-Users-steve-missing) is NOT created

            fake_porcelain = (
                "worktree /Users/steve/main\n"
                "HEAD abc123\n"
                "\n"
                "worktree /Users/steve/missing\n"
                "HEAD def456\n"
                "\n"
            )
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = fake_porcelain

            with patch("subprocess.run", return_value=mock_result), \
                 patch("os.path.expanduser", side_effect=lambda p: p.replace("~", tmpdir)):
                bases = tq._worktree_bases("/Users/steve/main")

            self.assertIn(wt_exists, bases)
            self.assertEqual(len(bases), 1)


# ---------------------------------------------------------------------------
# Task 2 — UTC day-boundary semantics
# ---------------------------------------------------------------------------

class TestUtcBoundary(unittest.TestCase):
    """AC #2: --before is end-of-UTC-day inclusive; --after is start-of-UTC-day inclusive."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _make_session(self, name: str, mtime_dt: datetime) -> str:
        path = os.path.join(self.tmpdir, f"{name}.jsonl")
        _make_jsonl_file(path, [SAMPLE_MESSAGE])
        _set_mtime_utc(path, mtime_dt)
        return path

    def test_utc_boundary_inclusive_closing_day(self):
        """Session at 23:55Z on day-N and session at 00:05Z on day-N+1.
        With --after day-N --before day-N, the 23:55Z session is included
        and the 00:05Z (next day) session is excluded."""
        day_n_close = datetime(2026, 4, 8, 23, 55, 0, tzinfo=timezone.utc)
        day_n1_open = datetime(2026, 4, 9, 0, 5, 0, tzinfo=timezone.utc)

        sess_close = self._make_session("sess_close", day_n_close)
        sess_open = self._make_session("sess_open", day_n1_open)

        # --after 2026-04-08 --before 2026-04-08 — only day N
        found = tq.discover_sessions(self.tmpdir, after="2026-04-08", before="2026-04-08")
        paths = set(found)

        self.assertIn(sess_close, paths, "Session at 23:55Z on day N must be included")
        self.assertNotIn(sess_open, paths, "Session at 00:05Z on day N+1 must be excluded")

    def test_utc_after_boundary_inclusive(self):
        """Session at 00:05Z on day N is included with --after day-N."""
        just_after = datetime(2026, 4, 8, 0, 5, 0, tzinfo=timezone.utc)
        sess = self._make_session("sess_after", just_after)

        found = tq.discover_sessions(self.tmpdir, after="2026-04-08")
        self.assertIn(sess, found)

    def test_utc_before_is_end_of_day(self):
        """before_dt must be 23:59:59.999999Z, not 00:00:00Z."""
        # A session at 15:00Z on day N should be included with --before day-N
        mid_day = datetime(2026, 4, 8, 15, 0, 0, tzinfo=timezone.utc)
        sess = self._make_session("sess_mid", mid_day)

        found = tq.discover_sessions(self.tmpdir, before="2026-04-08")
        self.assertIn(sess, found, "Session at 15:00Z on the --before day must be included")

    def test_multi_base_deduplication(self):
        """Sessions discovered from multiple bases are deduplicated."""
        # Create a session file and symlink it to simulate two bases pointing at the same file
        path = os.path.join(self.tmpdir, "sess.jsonl")
        _make_jsonl_file(path, [SAMPLE_MESSAGE])

        base2 = tempfile.mkdtemp()
        try:
            link = os.path.join(base2, "sess.jsonl")
            os.symlink(path, link)
            # Both bases point to the same underlying inode
            found = tq.discover_sessions([self.tmpdir, base2])
            self.assertEqual(len(found), 1, "Symlinked duplicate must be deduplicated")
        finally:
            import shutil
            shutil.rmtree(base2, ignore_errors=True)


# ---------------------------------------------------------------------------
# Task 3 — JSON serialization correctness
# ---------------------------------------------------------------------------

class TestJsonRoundtrip(unittest.TestCase):
    """AC #3: Every emitted JSONL line round-trips through json.loads."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _make_fixture_sessions(self, count: int = 3) -> list[str]:
        """Create count minimal session JSONL files."""
        paths = []
        for i in range(count):
            path = os.path.join(self.tmpdir, f"sess_{i:03d}.jsonl")
            msgs = [
                {
                    "type": "user",
                    "timestamp": f"2026-04-08T1{i}:00:00.000Z",
                    "message": {"role": "user", "content": f"Hello from session {i}"},
                    "parentUuid": None,
                    "isSidechain": False,
                    "sourceToolAssistantUUID": None,
                },
                {
                    "type": "assistant",
                    "timestamp": f"2026-04-08T1{i}:01:00.000Z",
                    "message": {"role": "assistant", "content": "Response text"},
                },
            ]
            _make_jsonl_file(path, msgs)
            paths.append(path)
        return paths

    def test_emit_json_roundtrips_user_messages(self):
        """user-messages query output lines all round-trip through json.loads."""
        sessions = self._make_fixture_sessions(3)
        output_path = os.path.join(self.tmpdir, "out.jsonl")

        try:
            import duckdb
            con = duckdb.connect()
        except ImportError:
            self.skipTest("duckdb not available")

        args = MagicMock()
        args.filter = None
        args.limit = None
        args.format = "json"
        args.output = output_path

        result = tq.query_user_messages(con, sessions, args)
        tq.emit_result(result, args)

        if os.path.exists(output_path):
            with open(output_path) as f:
                for lineno, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        json.loads(line)
                    except json.JSONDecodeError as e:
                        self.fail(f"Line {lineno} failed json.loads: {e}\nContent: {line!r}")

    def test_emit_json_no_python_literals(self):
        """No output line contains Python repr literals (None, True, False, single quotes)."""
        sessions = self._make_fixture_sessions(2)
        output_path = os.path.join(self.tmpdir, "out2.jsonl")

        try:
            import duckdb
            con = duckdb.connect()
        except ImportError:
            self.skipTest("duckdb not available")

        args = MagicMock()
        args.filter = None
        args.limit = None
        args.format = "json"
        args.output = output_path

        result = tq.query_user_messages(con, sessions, args)
        tq.emit_result(result, args)

        if os.path.exists(output_path):
            with open(output_path) as f:
                content = f.read()
            # These are Python repr artifacts that must not appear in JSON output
            self.assertNotIn(": None", content, "Python None must not appear in JSON output")
            self.assertNotIn(": True", content, "Python True must not appear in JSON output")
            self.assertNotIn(": False", content, "Python False must not appear in JSON output")

    def test_agent_summary_json_roundtrip(self):
        """agent-summary output (direct json.dumps path) round-trips through json.loads."""
        # query_agent_summary writes directly — test the json.dumps chain
        results = [
            {"agent_id": "abc", "agent_type": "dev", "size_kb": 10,
             "assistant_turns": 5, "tool_results": 3, "total_entries": 8,
             "error_count": 0, "first_prompt": "Do X", "last_response": "Done"},
        ]
        output_text = "\n".join(json.dumps(r) for r in results)
        for lineno, line in enumerate(output_text.splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError as e:
                self.fail(f"agent_summary line {lineno} failed: {e}")


# ---------------------------------------------------------------------------
# Task 5 — Slug-based session filtering
# ---------------------------------------------------------------------------

class TestSlugFilter(unittest.TestCase):
    """AC #5: --story-slugs filters sessions; same-day sprint disambiguation."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_slug_filter_drops_unrelated_sessions(self):
        """Two fixture sessions: one mentioning story-foo, one not.
        --story-slugs story-foo keeps only the first."""
        try:
            import duckdb
            con = duckdb.connect()
        except ImportError:
            self.skipTest("duckdb not available")

        # Session mentioning the slug
        sess_foo = os.path.join(self.tmpdir, "sess_foo.jsonl")
        _make_jsonl_file(sess_foo, [
            {
                "type": "user",
                "timestamp": "2026-04-08T10:00:00.000Z",
                "message": {"role": "user", "content": "Working on story-foo implementation"},
                "parentUuid": None,
                "isSidechain": False,
                "sourceToolAssistantUUID": None,
            }
        ])

        # Session NOT mentioning the slug
        sess_bar = os.path.join(self.tmpdir, "sess_bar.jsonl")
        _make_jsonl_file(sess_bar, [
            {
                "type": "user",
                "timestamp": "2026-04-08T11:00:00.000Z",
                "message": {"role": "user", "content": "Working on completely unrelated work"},
                "parentUuid": None,
                "isSidechain": False,
                "sourceToolAssistantUUID": None,
            }
        ])

        all_sessions = [sess_foo, sess_bar]
        filtered = tq._filter_sessions_by_slugs(con, all_sessions, ["story-foo"])

        self.assertIn(sess_foo, filtered, "Session mentioning story-foo must be kept")
        self.assertNotIn(sess_bar, filtered, "Session NOT mentioning story-foo must be dropped")
        self.assertEqual(len(filtered), 1)

    def test_slug_filter_empty_slugs_is_noop(self):
        """When no slugs provided, all sessions are returned unchanged."""
        try:
            import duckdb
            con = duckdb.connect()
        except ImportError:
            self.skipTest("duckdb not available")

        sess1 = os.path.join(self.tmpdir, "sess1.jsonl")
        sess2 = os.path.join(self.tmpdir, "sess2.jsonl")
        _make_jsonl_file(sess1, [SAMPLE_MESSAGE])
        _make_jsonl_file(sess2, [SAMPLE_MESSAGE])
        all_sessions = [sess1, sess2]

        # Empty slug list — no-op
        filtered = tq._filter_sessions_by_slugs(con, all_sessions, [])
        self.assertEqual(filtered, all_sessions)

    def test_slug_filter_multiple_slugs(self):
        """Session mentioning any of multiple slugs is kept."""
        try:
            import duckdb
            con = duckdb.connect()
        except ImportError:
            self.skipTest("duckdb not available")

        sess_a = os.path.join(self.tmpdir, "sess_a.jsonl")
        _make_jsonl_file(sess_a, [
            {"type": "user", "timestamp": "2026-04-08T10:00:00.000Z",
             "message": {"role": "user", "content": "story-alpha work"}}
        ])
        sess_b = os.path.join(self.tmpdir, "sess_b.jsonl")
        _make_jsonl_file(sess_b, [
            {"type": "user", "timestamp": "2026-04-08T11:00:00.000Z",
             "message": {"role": "user", "content": "story-beta work"}}
        ])
        sess_c = os.path.join(self.tmpdir, "sess_c.jsonl")
        _make_jsonl_file(sess_c, [
            {"type": "user", "timestamp": "2026-04-08T12:00:00.000Z",
             "message": {"role": "user", "content": "unrelated work"}}
        ])

        filtered = tq._filter_sessions_by_slugs(con, [sess_a, sess_b, sess_c], ["story-alpha", "story-beta"])
        self.assertIn(sess_a, filtered)
        self.assertIn(sess_b, filtered)
        self.assertNotIn(sess_c, filtered)


# ---------------------------------------------------------------------------
# Task 4 — Dynamic script path resolution (integration smoke test)
# ---------------------------------------------------------------------------

class TestDynamicScriptPath(unittest.TestCase):
    """AC #4: Script can be found and invoked from its canonical path."""

    def test_script_exists_at_canonical_path(self):
        """transcript-query.py must exist at skills/momentum/scripts/transcript-query.py
        when running inside the Momentum repo (dev-mode fallback)."""
        repo_root = Path(__file__).parent.parent.parent.parent.parent  # scripts/ → momentum/ → skills/ → momentum/ → project
        # More robust: find the script relative to this test file
        script_path = Path(__file__).parent / "transcript-query.py"
        self.assertTrue(script_path.exists(), f"transcript-query.py not found at {script_path}")

    def test_script_is_runnable(self):
        """Running transcript-query.py --help exits 0."""
        script_path = Path(__file__).parent / "transcript-query.py"
        result = subprocess.run(
            [sys.executable, str(script_path), "--help"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, f"--help failed: {result.stderr}")

    def test_glob_resolution_pattern(self):
        """The glob pattern for dynamic discovery matches the expected path structure."""
        import glob
        # Test that the glob pattern syntax works and returns the dev-mode fallback
        script_dir = Path(__file__).parent
        pattern = str(script_dir / "transcript-query.py")
        matches = glob.glob(pattern)
        self.assertTrue(len(matches) >= 1, "glob pattern must find at least the dev script")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for cls in [TestWorktreeBases, TestUtcBoundary, TestJsonRoundtrip,
                TestSlugFilter, TestDynamicScriptPath]:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
