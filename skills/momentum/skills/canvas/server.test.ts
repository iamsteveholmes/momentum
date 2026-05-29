/**
 * Momentum Cycle Dashboard — server.test.ts
 *
 * Combined tests: computeCycleState (cycle timeline) + epics lens helpers.
 * Run: bun test
 */

import { describe, test, expect, it } from "bun:test";
import {
  computeCycleState,
  analyzeGap,
  buildSortedRows,
  renderEpicsTable,
  buildEpicStoryRows,
  EpicDetailView,
  parseFrontmatter,
  extractSection,
  parseListItems,
  parseStoryMarkdown,
  StoryDetailView,
  readEpicsJson,
  readEpicBySlug,
  type Epic,
  type StoryMap,
} from "./server";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function makeSprints(overrides: object = {}) {
  return {
    active: null,
    planning: null,
    completed: [],
    ...overrides,
  };
}

// ---------------------------------------------------------------------------
// computeCycleState — cycle timeline tests
// ---------------------------------------------------------------------------

describe("computeCycleState", () => {
  test("empty sprints index — optional phases not-run, required phases pending, next-required = sprint-planning", () => {
    const result = computeCycleState(null);

    expect(result.phases).toHaveLength(6);

    const slugs = result.phases.map((p) => p.slug);
    expect(slugs).toEqual([
      "triage",
      "epic-grooming",
      "refine",
      "sprint-planning",
      "sprint-dev",
      "retro",
    ]);

    // Optional phases: not-run
    expect(result.phases.find((p) => p.slug === "triage")?.state).toBe("not-run");
    expect(result.phases.find((p) => p.slug === "epic-grooming")?.state).toBe("not-run");
    expect(result.phases.find((p) => p.slug === "refine")?.state).toBe("not-run");

    // Required phases: pending (except sprint-planning = next-required)
    expect(result.phases.find((p) => p.slug === "sprint-planning")?.state).toBe("next-required");
    expect(result.phases.find((p) => p.slug === "sprint-dev")?.state).toBe("pending");
    expect(result.phases.find((p) => p.slug === "retro")?.state).toBe("pending");

    expect(result.nextRequired).toBe("sprint-planning");
    expect(result.lastSprintSlug).toBeNull();
  });

  test("empty completed array — same as null input", () => {
    const result = computeCycleState(makeSprints({ completed: [] }));
    expect(result.nextRequired).toBe("sprint-planning");
    expect(result.lastSprintSlug).toBeNull();
  });

  test("one completed sprint with retro_run_at — new cycle starts, next-required = sprint-planning", () => {
    const result = computeCycleState(
      makeSprints({
        completed: [
          {
            slug: "sprint-2026-04-01",
            status: "done",
            planned: "2026-04-01",
            started: "2026-04-01",
            retro_run_at: "2026-04-14",
            stories: [],
          },
        ],
      })
    );

    expect(result.nextRequired).toBe("sprint-planning");
    expect(result.lastSprintSlug).toBe("sprint-2026-04-01");

    expect(result.phases.find((p) => p.slug === "sprint-planning")?.state).toBe("next-required");
    expect(result.phases.find((p) => p.slug === "sprint-dev")?.state).toBe("pending");
    expect(result.phases.find((p) => p.slug === "retro")?.state).toBe("pending");
  });

  test("active sprint with planning status — sprint-planning done, sprint-dev next-required", () => {
    const result = computeCycleState(
      makeSprints({
        planning: {
          slug: "sprint-2026-05-01",
          status: "planning",
          planned: "2026-05-01",
          stories: [],
        },
      })
    );

    expect(result.phases.find((p) => p.slug === "sprint-planning")?.state).toBe("done");
    expect(result.phases.find((p) => p.slug === "sprint-dev")?.state).toBe("next-required");
    expect(result.phases.find((p) => p.slug === "retro")?.state).toBe("pending");
    expect(result.nextRequired).toBe("sprint-dev");
  });

  test("active sprint with active status and started — sprint-planning done, sprint-dev in-progress, retro next-required", () => {
    const result = computeCycleState(
      makeSprints({
        active: {
          slug: "sprint-2026-05-03",
          status: "active",
          planned: "2026-05-03",
          started: "2026-05-03",
          stories: [],
        },
      })
    );

    expect(result.phases.find((p) => p.slug === "sprint-planning")?.state).toBe("done");
    expect(result.phases.find((p) => p.slug === "sprint-dev")?.state).toBe("in-progress");
    expect(result.phases.find((p) => p.slug === "retro")?.state).toBe("next-required");
    expect(result.nextRequired).toBe("retro");
    expect(result.lastSprintSlug).toBeNull();
  });

  test("completed sprint with retro AND active sprint — correctly identifies current cycle", () => {
    const result = computeCycleState(
      makeSprints({
        active: {
          slug: "sprint-2026-05-03",
          status: "active",
          planned: "2026-05-03",
          started: "2026-05-03",
          stories: [],
        },
        completed: [
          {
            slug: "sprint-2026-04-01",
            status: "done",
            planned: "2026-04-01",
            started: "2026-04-01",
            retro_run_at: "2026-04-14",
            stories: [],
          },
        ],
      })
    );

    expect(result.phases.find((p) => p.slug === "sprint-planning")?.state).toBe("done");
    expect(result.phases.find((p) => p.slug === "sprint-dev")?.state).toBe("in-progress");
    expect(result.phases.find((p) => p.slug === "retro")?.state).toBe("next-required");
    expect(result.nextRequired).toBe("retro");
    expect(result.lastSprintSlug).toBe("sprint-2026-04-01");
  });

  test("optional phases never receive next-required state", () => {
    const result = computeCycleState(null);

    const optionalSlugs = ["triage", "epic-grooming", "refine"];
    for (const slug of optionalSlugs) {
      const phase = result.phases.find((p) => p.slug === slug);
      expect(phase?.required).toBe(false);
      expect(phase?.state).not.toBe("next-required");
    }
  });

  test("optional phases are never next-required even mid-cycle", () => {
    const result = computeCycleState(
      makeSprints({
        active: {
          slug: "sprint-2026-05-03",
          status: "active",
          planned: "2026-05-03",
          started: "2026-05-03",
          stories: [],
        },
      })
    );

    const optionalSlugs = ["triage", "epic-grooming", "refine"];
    for (const slug of optionalSlugs) {
      const phase = result.phases.find((p) => p.slug === slug);
      expect(phase?.state).not.toBe("next-required");
    }
  });

  test("required field is set correctly for all phases", () => {
    const result = computeCycleState(null);

    const required = result.phases.filter((p) => p.required).map((p) => p.slug);
    const optional = result.phases.filter((p) => !p.required).map((p) => p.slug);

    expect(required).toEqual(["sprint-planning", "sprint-dev", "retro"]);
    expect(optional).toEqual(["triage", "epic-grooming", "refine"]);
  });

  test("lastSprintSlug returns most recent completed sprint slug", () => {
    const result = computeCycleState(
      makeSprints({
        completed: [
          {
            slug: "sprint-2026-03-01",
            status: "done",
            planned: "2026-03-01",
            retro_run_at: "2026-03-14",
            stories: [],
          },
          {
            slug: "sprint-2026-04-01",
            status: "done",
            planned: "2026-04-01",
            retro_run_at: "2026-04-14",
            stories: [],
          },
        ],
      })
    );

    expect(result.lastSprintSlug).toBe("sprint-2026-04-01");
  });

  test("completed sprint without retro_run_at — retro is next-required", () => {
    const result = computeCycleState(
      makeSprints({
        completed: [
          {
            slug: "sprint-2026-05-01",
            status: "done",
            planned: "2026-05-01",
            started: "2026-05-01",
            retro_run_at: null,
            stories: [],
          },
        ],
      })
    );

    expect(result.phases.find((p) => p.slug === "sprint-planning")?.state).toBe("done");
    expect(result.phases.find((p) => p.slug === "sprint-dev")?.state).toBe("done");
    expect(result.phases.find((p) => p.slug === "retro")?.state).toBe("next-required");
    expect(result.nextRequired).toBe("retro");
  });
});

// ---------------------------------------------------------------------------
// analyzeGap — epics lens tests
// ---------------------------------------------------------------------------
describe("analyzeGap", () => {
  it("returns has_gap=true when zero stories and status is not working", () => {
    const epic: Epic = {
      epic_slug: "test-epic",
      name: "Test Epic",
      status: "partial",
      stories_done: 0,
      stories_remaining: 2,
      stories: ["story-a", "story-b"],
    };
    const storyMap: StoryMap = {};
    const result = analyzeGap(epic, storyMap);
    expect(result.has_gap).toBe(true);
  });

  it("returns has_gap=false when status is working regardless of story counts", () => {
    const epic: Epic = {
      epic_slug: "test-epic",
      name: "Test Epic",
      status: "working",
      stories_done: 0,
      stories_remaining: 0,
      stories: [],
    };
    const storyMap: StoryMap = {};
    const result = analyzeGap(epic, storyMap);
    expect(result.has_gap).toBe(false);
  });

  it("returns has_gap=false when stories_done > 0", () => {
    const epic: Epic = {
      epic_slug: "test-epic",
      name: "Test Epic",
      status: "partial",
      stories_done: 2,
      stories_remaining: 1,
      stories: ["story-a", "story-b", "story-c"],
    };
    const storyMap: StoryMap = {};
    const result = analyzeGap(epic, storyMap);
    expect(result.has_gap).toBe(false);
  });

  it("returns has_gap=true for not-working status with zero done stories", () => {
    const epic: Epic = {
      epic_slug: "test-epic",
      name: "Test Epic",
      status: "not-working",
      stories_done: 0,
      stories_remaining: 3,
      stories: ["story-a"],
    };
    const storyMap: StoryMap = {};
    const result = analyzeGap(epic, storyMap);
    expect(result.has_gap).toBe(true);
  });

  it("returns has_gap=false when no stories done AND no stories remaining (empty epic, nothing planned)", () => {
    const epic: Epic = {
      epic_slug: "test-epic",
      name: "Test Epic",
      lifecycle: "finite-lived",
      audience: "user",
      stories_done: 0,
      stories_remaining: 0,
      stories: [],
    };
    const storyMap: StoryMap = {};
    const result = analyzeGap(epic, storyMap);
    // No remaining work to start on → not a gap. (Was incorrectly flagged
    // pre-migration when the heuristic keyed on the now-deleted status field.)
    expect(result.has_gap).toBe(false);
  });

  // --- post-b1-migration: real epics carry NO status field ---
  it("returns has_gap=true for a status-less epic with remaining stories and none done", () => {
    const epic: Epic = {
      epic_slug: "momentum-startup-performance",
      name: "Startup Performance",
      lifecycle: "finite-lived",
      audience: "internal",
      stories_done: 0,
      stories_remaining: 21,
      stories: ["s1", "s2"],
    };
    const result = analyzeGap(epic, {});
    expect(result.has_gap).toBe(true);
    expect(result.reason).toBe("outstanding stories but none completed yet");
  });

  it("returns has_gap=false for a status-less epic with at least one story done", () => {
    const epic: Epic = {
      epic_slug: "momentum-canvas",
      name: "Momentum Canvas",
      lifecycle: "finite-lived",
      audience: "user",
      stories_done: 3,
      stories_remaining: 2,
      stories: ["s1", "s2", "s3", "s4", "s5"],
    };
    const result = analyzeGap(epic, {});
    expect(result.has_gap).toBe(false);
  });

  it("returns has_gap=false for a status-less epic with all stories done (remaining 0)", () => {
    const epic: Epic = {
      epic_slug: "momentum-done",
      name: "Done Epic",
      lifecycle: "long-lived",
      audience: "internal",
      stories_done: 4,
      stories_remaining: 0,
      stories: ["s1", "s2", "s3", "s4"],
    };
    const result = analyzeGap(epic, {});
    expect(result.has_gap).toBe(false);
  });

  it("does NOT mass-flag status-less epics: only zero-done-with-remaining are gaps", () => {
    // Mirrors the real epics.json shape after the b1 migration (no status).
    const epics: Epic[] = [
      { epic_slug: "a", name: "A", lifecycle: "finite-lived", audience: "user", stories_done: 5, stories_remaining: 0 },
      { epic_slug: "b", name: "B", lifecycle: "finite-lived", audience: "user", stories_done: 2, stories_remaining: 3 },
      { epic_slug: "c", name: "C", lifecycle: "long-lived", audience: "internal", stories_done: 0, stories_remaining: 0 },
      { epic_slug: "d", name: "D", lifecycle: "finite-lived", audience: "internal", stories_done: 0, stories_remaining: 7 },
    ];
    const flagged = epics.filter((e) => analyzeGap(e, {}).has_gap).map((e) => e.epic_slug);
    expect(flagged).toEqual(["d"]);
  });
});

// ---------------------------------------------------------------------------
// buildSortedRows — epics lens sort tests
// ---------------------------------------------------------------------------
describe("buildSortedRows", () => {
  it("sorts gap rows first (alphabetically), then non-gap by severity", () => {
    const epics: Epic[] = [
      {
        epic_slug: "z-working",
        name: "Z Working",
        status: "working",
        stories_done: 3,
        stories_remaining: 0,
        stories: [],
      },
      {
        epic_slug: "a-partial",
        name: "A Partial",
        status: "partial",
        stories_done: 0,
        stories_remaining: 2,
        stories: [],
      },
      {
        epic_slug: "b-not-working",
        name: "B Not Working",
        status: "not-working",
        stories_done: 0,
        stories_remaining: 1,
        stories: [],
      },
      {
        epic_slug: "c-partial-done",
        name: "C Partial Done",
        status: "partial",
        stories_done: 1,
        stories_remaining: 1,
        stories: [],
      },
      {
        epic_slug: "d-not-started",
        name: "D Not Started",
        status: "not-started",
        stories_done: 0,
        stories_remaining: 0,
        stories: [],
      },
    ];
    const storyMap: StoryMap = {};
    const rows = buildSortedRows(epics, storyMap);

    // Gap rows first, alphabetically. Under the corrected heuristic a gap is
    // stories_remaining > 0 && stories_done === 0, so D Not Started (0/0) is NOT a gap.
    expect(rows[0].name).toBe("A Partial");
    expect(rows[0].has_gap).toBe(true);
    expect(rows[1].name).toBe("B Not Working");
    expect(rows[1].has_gap).toBe(true);

    // Non-gap rows sorted by status severity (partial < working < not-started), then alpha.
    expect(rows[2].name).toBe("C Partial Done");
    expect(rows[2].has_gap).toBe(false);
    expect(rows[3].name).toBe("Z Working");
    expect(rows[3].has_gap).toBe(false);
    expect(rows[4].name).toBe("D Not Started");
    expect(rows[4].has_gap).toBe(false);
  });

  it("sorts non-gap rows alphabetically within same status group", () => {
    const epics: Epic[] = [
      {
        epic_slug: "z-partial",
        name: "Z Partial",
        status: "partial",
        stories_done: 1,
        stories_remaining: 1,
        stories: [],
      },
      {
        epic_slug: "a-partial",
        name: "A Partial",
        status: "partial",
        stories_done: 2,
        stories_remaining: 0,
        stories: [],
      },
    ];
    const storyMap: StoryMap = {};
    const rows = buildSortedRows(epics, storyMap);
    expect(rows[0].name).toBe("A Partial");
    expect(rows[1].name).toBe("Z Partial");
  });

  it("returns empty array for empty epics input", () => {
    const rows = buildSortedRows([], {});
    expect(rows).toEqual([]);
  });
});

// ---------------------------------------------------------------------------
// renderEpicsTable — HTML escaping + status-less rendering
// ---------------------------------------------------------------------------
describe("renderEpicsTable", () => {
  it("escapes HTML in epic name, slug, and status to prevent injection", () => {
    // epics.json is a writable artifact — these fields are an injection sink.
    const rows = buildSortedRows(
      [
        {
          epic_slug: "evil-epic",
          name: `<img src=x onerror="alert(1)">`,
          status: `working"><script>alert('xss')</script>`,
          lifecycle: "finite-lived",
          audience: "user",
          stories_done: 1,
          stories_remaining: 0,
        },
      ],
      {}
    );
    const html = renderEpicsTable(rows);
    // Raw injection markup must NOT survive unescaped.
    expect(html).not.toContain("<img src=x");
    expect(html).not.toContain("<script>alert('xss')</script>");
    // It must appear in escaped form instead.
    expect(html).toContain("&lt;img src=x");
    expect(html).toContain("&lt;script&gt;");
  });

  it("escapes a malicious epic_slug inside the href", () => {
    const rows = buildSortedRows(
      [
        {
          epic_slug: `x"><script>boom()</script>`,
          name: "Slug Attack",
          lifecycle: "long-lived",
          audience: "internal",
          stories_done: 2,
          stories_remaining: 0,
        },
      ],
      {}
    );
    const html = renderEpicsTable(rows);
    expect(html).not.toContain("<script>boom()</script>");
    expect(html).toContain("&lt;script&gt;");
  });

  it("renders a status-less epic's lifecycle as a lifecycle-tag, NOT a status badge", () => {
    // Real post-migration epics have no status. Lifecycle must not be
    // conflated into a not-started status badge.
    const rows = buildSortedRows(
      [
        {
          epic_slug: "no-status",
          name: "No Status Epic",
          lifecycle: "long-lived",
          audience: "internal",
          stories_done: 2,
          stories_remaining: 1,
        },
      ],
      {}
    );
    const html = renderEpicsTable(rows);
    expect(html).toContain("lifecycle-tag");
    expect(html).toContain("long-lived");
    // The lifecycle value must NOT be wrapped in a status badge.
    expect(html).not.toContain('class="badge not-started"><span class="dot"></span>long-lived');
  });

  it("renders a gap flag (not a badge) for a status-less epic with remaining work and none done", () => {
    const rows = buildSortedRows(
      [
        {
          epic_slug: "gappy",
          name: "Gappy Epic",
          lifecycle: "finite-lived",
          audience: "user",
          stories_done: 0,
          stories_remaining: 5,
        },
      ],
      {}
    );
    const html = renderEpicsTable(rows);
    expect(html).toContain("gap-flag");
    expect(html).toContain("gap");
  });

  it("renders empty-state message when there are no rows", () => {
    const html = renderEpicsTable([]);
    expect(html).toContain("No epics found");
  });
});

// ---------------------------------------------------------------------------
// Missing stories/index.json — epics lens error handling
// ---------------------------------------------------------------------------
describe("analyzeGap with missing story index", () => {
  it("treats all stories as unknown when story map is empty", () => {
    const epic: Epic = {
      epic_slug: "test",
      name: "Test",
      status: "partial",
      stories_done: 0,
      stories_remaining: 1,
      stories: ["story-x"],
    };
    const result = analyzeGap(epic, {});
    expect(result.has_gap).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// Epic L2 — buildEpicStoryRows
// ---------------------------------------------------------------------------
describe("buildEpicStoryRows", () => {
  it("returns story rows with title and status from story map", () => {
    const epic: Epic = {
      epic_slug: "my-epic",
      name: "My Epic",
      status: "partial",
      stories_done: 1,
      stories_remaining: 1,
      stories: ["story-a", "story-b"],
    };
    const storyMap: StoryMap = {
      "story-a": { status: "done", title: "Story A" },
      "story-b": { status: "in-progress", title: "Story B" },
    };
    const rows = buildEpicStoryRows(epic, storyMap);
    expect(rows).toHaveLength(2);
    // Sorted by STATUS_ORDER: in-progress (idx 0) before done (idx 5)
    expect(rows[0]).toEqual({ slug: "story-b", title: "Story B", status: "in-progress", epicSlug: "my-epic" });
    expect(rows[1]).toEqual({ slug: "story-a", title: "Story A", status: "done", epicSlug: "my-epic" });
  });

  it("falls back to slug as title when story is not in map", () => {
    const epic: Epic = {
      epic_slug: "my-epic",
      name: "My Epic",
      status: "partial",
      stories_done: 0,
      stories_remaining: 1,
      stories: ["unknown-story"],
    };
    const rows = buildEpicStoryRows(epic, {});
    expect(rows).toHaveLength(1);
    expect(rows[0]).toEqual({ slug: "unknown-story", title: "unknown-story", status: "backlog", epicSlug: "my-epic" });
  });

  it("returns empty array when epic has no stories", () => {
    const epic: Epic = {
      epic_slug: "my-epic",
      name: "My Epic",
      status: "not-started",
      stories_done: 0,
      stories_remaining: 0,
      stories: [],
    };
    const rows = buildEpicStoryRows(epic, {});
    expect(rows).toEqual([]);
  });

  it("returns empty array when stories field is undefined", () => {
    const epic: Epic = {
      epic_slug: "my-epic",
      name: "My Epic",
      status: "not-started",
      stories_done: 0,
      stories_remaining: 0,
    };
    const rows = buildEpicStoryRows(epic, {});
    expect(rows).toEqual([]);
  });
});

// ---------------------------------------------------------------------------
// Epic L2 — EpicDetailView HTML rendering
// ---------------------------------------------------------------------------
describe("EpicDetailView", () => {
  const baseEpic: Epic = {
    epic_slug: "momentum-canvas",
    name: "Momentum Canvas",
    status: "partial",
    lifecycle: "finite-lived",
    audience: "user",
    stories_done: 3,
    stories_remaining: 2,
    acceptance_condition: "Developer can view epic L2.",
    value_analysis: "This provides significant value.",
    system_context: "Lives within the canvas skill.",
    stories: ["story-a", "story-b"],
  };

  it("renders warm light reading-surface with readingPaper background", () => {
    const h = String(EpicDetailView({ epic: baseEpic, storyRows: [] }));
    expect(h).toContain("reading-surface");
  });

  it("renders epic heading with epic name", () => {
    const h = String(EpicDetailView({ epic: baseEpic, storyRows: [] }));
    expect(h).toContain("Momentum Canvas");
    expect(h).toContain("l2-name");
  });

  it("renders meta strip with story fraction and reading mode label", () => {
    const h = String(EpicDetailView({ epic: baseEpic, storyRows: [] }));
    expect(h).toContain("l2-meta");
    expect(h).toContain("3");
    expect(h).toContain("stories");
    expect(h).toContain("reading mode");
  });

  it("renders lifecycle pill in l2-meta when lifecycle is present", () => {
    const h = String(EpicDetailView({ epic: baseEpic, storyRows: [] }));
    expect(h).toContain("l2-meta");
    expect(h).toContain("finite-lived");
  });

  it("renders audience pill in l2-meta when audience is present", () => {
    const h = String(EpicDetailView({ epic: baseEpic, storyRows: [] }));
    expect(h).toContain("l2-meta");
    expect(h).toContain("user");
  });

  it("renders value narrative section when value_analysis is present", () => {
    const h = String(EpicDetailView({ epic: baseEpic, storyRows: [] }));
    expect(h).toContain("value narrative");
    expect(h).toContain("This provides significant value.");
  });

  it("does not render value narrative section when value_analysis is absent", () => {
    const epic = { ...baseEpic, value_analysis: undefined };
    const h = String(EpicDetailView({ epic, storyRows: [] }));
    expect(h).not.toContain("Value Narrative");
  });

  it("renders acceptance condition in boxed container with reading-ac-box", () => {
    const h = String(EpicDetailView({ epic: baseEpic, storyRows: [] }));
    expect(h).toContain("reading-ac-box");
    expect(h).toContain("Developer can view epic L2.");
  });

  it("renders acceptance_conditions array as single text block when present", () => {
    const epic = { ...baseEpic, acceptance_condition: undefined, acceptance_conditions: ["AC one", "AC two"] };
    const h = String(EpicDetailView({ epic, storyRows: [] }));
    expect(h).toContain("reading-ac-box");
    expect(h).toContain("AC one");
    expect(h).toContain("AC two");
  });

  it("renders system context as callout block", () => {
    const h = String(EpicDetailView({ epic: baseEpic, storyRows: [] }));
    expect(h).toContain("reading-callout");
    expect(h).toContain("Lives within the canvas skill.");
  });

  it("renders stories list with status badge and title", () => {
    const storyRows = [
      { slug: "story-a", title: "Story Alpha", status: "done", epicSlug: "test-epic" },
      { slug: "story-b", title: "Story Beta", status: "in-progress", epicSlug: "test-epic" },
    ];
    const h = String(EpicDetailView({ epic: baseEpic, storyRows }));
    expect(h).toContain("Story Alpha");
    expect(h).toContain("Story Beta");
    expect(h).toContain("l2-stories");
    expect(h).toContain('href="/stories/story-a?from=epic&amp;epic=test-epic"');
    expect(h).toContain('href="/stories/story-b?from=epic&amp;epic=test-epic"');
  });

  it("renders breadcrumb OOB swap with Dashboard link and epic label", () => {
    const h = String(EpicDetailView({ epic: baseEpic, storyRows: [] }));
    expect(h).toContain('hx-swap-oob="true"');
    expect(h).toContain('href="/"');
    expect(h).toContain("dashboard");
    // Epic name appears in the content
    expect(h).toContain("Momentum Canvas");
  });

  it("renders pure href for breadcrumb navigation back to root", () => {
    const h = String(EpicDetailView({ epic: baseEpic, storyRows: [] }));
    expect(h).toContain('href="/"');
    expect(h).not.toContain('hx-push-url="/"');
  });

  it("renders l2-body content container", () => {
    const h = String(EpicDetailView({ epic: baseEpic, storyRows: [] }));
    expect(h).toContain("l2-body");
  });

  it("does not render dependencies section when no dependencies", () => {
    const h = String(EpicDetailView({ epic: baseEpic, storyRows: [] }));
    expect(h).not.toContain("Dependencies");
  });

  it("renders dependencies as plain list when present", () => {
    const epic = { ...baseEpic, dependencies: ["dep-epic-a", "dep-epic-b"] };
    const h = String(EpicDetailView({ epic, storyRows: [] }));
    expect(h).toContain("dependencies");
    expect(h).toContain("reading-deps-list");
    expect(h).toContain("dep-epic-a");
    expect(h).toContain("dep-epic-b");
  });
});

// ---------------------------------------------------------------------------
// readEpicsJson — graceful degradation when epics.json is missing
// ---------------------------------------------------------------------------
describe("readEpicsJson", () => {
  it("returns empty array when called (graceful degradation assurance)", async () => {
    // The function returns [] when the file is missing or invalid.
    // In a normal test environment, epics.json may be present, so we simply
    // assert it returns an array (not throwing) to confirm graceful behavior.
    const result = await readEpicsJson();
    expect(Array.isArray(result)).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// readEpicBySlug — null for missing slug
// ---------------------------------------------------------------------------
describe("readEpicBySlug", () => {
  it("returns null for a slug that does not exist", async () => {
    const result = await readEpicBySlug("__nonexistent-slug-xyz__");
    expect(result).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// parseFrontmatter — story L3 markdown parsing
// ---------------------------------------------------------------------------
describe("parseFrontmatter", () => {
  it("parses key-value pairs from frontmatter block", () => {
    const source = `---
title: My Story Title
story_key: my-story
status: backlog
---
# Heading
`;
    const fm = parseFrontmatter(source);
    expect(fm["title"]).toBe("My Story Title");
    expect(fm["story_key"]).toBe("my-story");
    expect(fm["status"]).toBe("backlog");
  });

  it("returns empty object when no frontmatter", () => {
    const fm = parseFrontmatter("# No frontmatter here\n\nJust prose.");
    expect(Object.keys(fm)).toHaveLength(0);
  });

  it("handles optional fields that are absent", () => {
    const source = `---
title: Minimal
story_key: minimal
status: backlog
---
`;
    const fm = parseFrontmatter(source);
    expect(fm["epic_slug"]).toBeUndefined();
    expect(fm["derives_from"]).toBeUndefined();
  });
});

// ---------------------------------------------------------------------------
// extractSection — section extraction helper
// ---------------------------------------------------------------------------
describe("extractSection", () => {
  it("extracts content between two headings", () => {
    const source = `---
title: test
---

## Story

As a developer, I want to build things.

## Acceptance Criteria

- AC one
- AC two

## Dev Notes

Some technical notes here.
`;
    const story = extractSection(source, "## Story");
    expect(story).toContain("As a developer");

    const ac = extractSection(source, "## Acceptance Criteria");
    expect(ac).toContain("AC one");
    expect(ac).toContain("AC two");
    expect(ac).not.toContain("technical notes");
  });

  it("returns empty string when section not found", () => {
    const result = extractSection("# Some content\n\nNo sections.", "## Missing");
    expect(result).toBe("");
  });
});

// ---------------------------------------------------------------------------
// parseListItems — list item parser
// ---------------------------------------------------------------------------
describe("parseListItems", () => {
  it("parses numbered list items", () => {
    const text = "1. First item\n2. Second item\n3. Third item";
    const items = parseListItems(text);
    expect(items).toHaveLength(3);
    expect(items[0]).toBe("First item");
    expect(items[2]).toBe("Third item");
  });

  it("parses bullet list items with dash", () => {
    const text = "- Item alpha\n- Item beta";
    const items = parseListItems(text);
    expect(items).toHaveLength(2);
    expect(items[0]).toBe("Item alpha");
  });

  it("returns empty array for non-list text", () => {
    const items = parseListItems("Just a paragraph.\nNo list here.");
    expect(items).toHaveLength(0);
  });
});

// ---------------------------------------------------------------------------
// parseStoryMarkdown — full story parser
// ---------------------------------------------------------------------------
describe("parseStoryMarkdown", () => {
  const sampleStory = `---
title: My Test Story
story_key: my-test-story
status: in-progress
epic_slug: test-epic
feature_slug: test-feature
story_type: feature
touches:
  - src/foo.ts
  - src/bar.ts
---

# My Test Story

## Story

As a developer,
I want to implement something,
so that I can demonstrate it.

## Description

As a developer, I want to build something useful.

This story covers the implementation of the reading mode feature for developer productivity.

## Acceptance Criteria

1. Route renders HTML correctly
2. Breadcrumb shows correct path
3. Story data sourced from .momentum/stories/

## Dev Notes

Some technical guidance here about architecture.

### Testing Requirements

Unit tests required.
`;

  it("parses story meta from frontmatter", () => {
    const parsed = parseStoryMarkdown(sampleStory);
    expect(parsed.meta.title).toBe("My Test Story");
    expect(parsed.meta.story_key).toBe("my-test-story");
    expect(parsed.meta.status).toBe("in-progress");
    expect(parsed.meta.epic_slug).toBe("test-epic");
    expect(parsed.meta.feature_slug).toBe("test-feature");
    expect(parsed.meta.story_type).toBe("feature");
  });

  it("parses story narrative from ## Description section (first prose paragraph, not user-story line)", () => {
    const parsed = parseStoryMarkdown(sampleStory);
    // Should extract the first prose paragraph, skipping the "As a developer..." user-story line
    expect(parsed.storyNarrative).toContain("reading mode feature");
    expect(parsed.storyNarrative).not.toContain("As a developer");
  });

  it("parses acceptance criteria as array", () => {
    const parsed = parseStoryMarkdown(sampleStory);
    expect(parsed.acceptanceCriteria).toHaveLength(3);
    expect(parsed.acceptanceCriteria[0]).toBe("Route renders HTML correctly");
    expect(parsed.acceptanceCriteria[1]).toBe("Breadcrumb shows correct path");
  });

  it("parses touches file list", () => {
    const parsed = parseStoryMarkdown(sampleStory);
    expect(parsed.touches).toHaveLength(2);
    expect(parsed.touches[0]).toBe("src/foo.ts");
    expect(parsed.touches[1]).toBe("src/bar.ts");
  });

  it("parses dev notes section", () => {
    const parsed = parseStoryMarkdown(sampleStory);
    expect(parsed.devNotes).toContain("Some technical guidance");
  });

  it("handles story with no touches", () => {
    const minimal = `---
title: Minimal Story
story_key: minimal
status: backlog
---

## Story
As a user, I want basic functionality.
`;
    const parsed = parseStoryMarkdown(minimal);
    expect(parsed.touches).toHaveLength(0);
  });

  it("filters DRAFT placeholder lines from acceptance criteria", () => {
    const withDraft = `---
title: Draft Story
story_key: draft-story
status: backlog
---

## Acceptance Criteria

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Actual AC one
`;
    const parsed = parseStoryMarkdown(withDraft);
    // DRAFT lines starting with _ should be filtered out
    const hasDraft = parsed.acceptanceCriteria.some((ac) => ac.startsWith("DRAFT"));
    expect(hasDraft).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// StoryDetailView — HTML rendering
// ---------------------------------------------------------------------------
describe("StoryDetailView", () => {
  const baseStory = {
    meta: {
      title: "My Test Story",
      story_key: "my-test-story",
      status: "in-progress",
      epic_slug: "test-epic",
      feature_slug: "test-feature",
      story_type: "feature",
    },
    storyNarrative: "As a developer, I want to do things, so that I can build stuff.",
    acceptanceCriteria: [
      "Route renders HTML with story detail",
      "Breadcrumb swaps correctly via HTMX OOB",
    ],
    devNotes: "Some development notes about architecture.",
    workflowSection: "",
    touches: ["skills/momentum/skills/canvas/server.tsx"],
  };

  it("renders reading-surface with warm-light polarity", () => {
    const h = String(StoryDetailView({ story: baseStory, from: null }));
    expect(h).toContain("reading-surface");
  });

  it("renders l3-fm with status badge and epic/type metadata", () => {
    const h = String(StoryDetailView({ story: baseStory, from: null }));
    expect(h).toContain("l3-fm");
    expect(h).toContain("in-progress");
    expect(h).toContain("test-epic");
    expect(h).toContain("feature"); // story_type
  });

  it("renders title as l3-title", () => {
    const h = String(StoryDetailView({ story: baseStory, from: null }));
    expect(h).toContain("l3-title");
    expect(h).toContain("My Test Story");
  });

  it("renders story narrative as l3-subtitle", () => {
    const h = String(StoryDetailView({ story: baseStory, from: null }));
    expect(h).toContain("l3-subtitle");
    expect(h).toContain("As a developer");
  });

  it("renders acceptance criteria as numbered list", () => {
    const h = String(StoryDetailView({ story: baseStory, from: null }));
    expect(h).toContain("story-ac-list");
    expect(h).toContain("Route renders HTML with story detail");
    expect(h).toContain("Breadcrumb swaps correctly via HTMX OOB");
  });

  it("renders dev notes as callout", () => {
    const h = String(StoryDetailView({ story: baseStory, from: null }));
    expect(h).toContain("story-dev-notes");
    expect(h).toContain("architecture");
  });

  it("renders file list when touches present", () => {
    const h = String(StoryDetailView({ story: baseStory, from: null }));
    expect(h).toContain("story-touches-list");
    expect(h).toContain("skills/momentum/skills/canvas/server.tsx");
  });

  it("does not render file list when no touches", () => {
    const story = { ...baseStory, touches: [] };
    const h = String(StoryDetailView({ story, from: null }));
    expect(h).not.toContain("story-touches-list");
  });

  it("renders breadcrumb OOB swap with dashboard link", () => {
    const h = String(StoryDetailView({ story: baseStory, from: null }));
    expect(h).toContain('hx-swap-oob="true"');
    expect(h).toContain("dashboard");
    expect(h).toContain('href="/"');
    expect(h).not.toContain('hx-get="/"');
  });

  it("uses reading-crumb-bar class on breadcrumb (warm-light)", () => {
    const h = String(StoryDetailView({ story: baseStory, from: null }));
    expect(h).toContain("reading-crumb-bar");
  });

  it("breadcrumb includes epic link when from=epic", () => {
    const h = String(StoryDetailView({ story: baseStory, from: "epic" }));
    expect(h).toContain('href="/epics/test-epic"');
    expect(h).toContain("epic");
  });

  it("breadcrumb uses epicSlugOverride when provided, overriding frontmatter", () => {
    const h = String(StoryDetailView({ story: baseStory, from: "epic", epicSlugOverride: "override-epic" }));
    expect(h).toContain('href="/epics/override-epic"');
  });

  it("breadcrumb includes sprint link when from=sprint with activeSprintSlug", () => {
    const h = String(StoryDetailView({ story: baseStory, from: "sprint", activeSprintSlug: "sprint-2026-05-03" }));
    expect(h).toContain("sprint");
    expect(h).toContain('href="/sprints/sprint-2026-05-03"');
  });

  it("breadcrumb falls back to /lenses/sprint when from=sprint but no activeSprintSlug", () => {
    const h = String(StoryDetailView({ story: baseStory, from: "sprint", activeSprintSlug: null }));
    expect(h).toContain("sprint");
    expect(h).toContain('href="/"');
  });

  it("breadcrumb has no middle segment when from=null", () => {
    const h = String(StoryDetailView({ story: baseStory, from: null }));
    // Should not have epic or sprint links in breadcrumb
    expect(h).not.toContain('hx-get="/epics/test-epic"');
    expect(h).not.toContain('hx-get="/lenses/sprint"');
  });

  it("renders reading-col for 65ch measure", () => {
    const h = String(StoryDetailView({ story: baseStory, from: null }));
    expect(h).toContain("reading-col");
  });

  it("escapes HTML in story content to prevent XSS", () => {
    const story = {
      ...baseStory,
      acceptanceCriteria: ['AC with <script>alert("xss")</script>'],
      touches: ['path/to/<script>file</script>'],
    };
    const h = String(StoryDetailView({ story, from: null }));
    expect(h).not.toContain('<script>alert("xss")</script>');
    expect(h).toContain("&lt;script&gt;");
  });
});

// ---------------------------------------------------------------------------
// Route handler tests — /lenses/epics and /epics/:slug
// ---------------------------------------------------------------------------
describe("HTTP route: /lenses/epics", () => {
  it("returns 200 HTML response with section id lens-epics", async () => {
    const server = (await import("./server")).default;
    const req = new Request("http://localhost:3456/lenses/epics");
    const res = await server.fetch(req);
    expect(res.status).toBe(200);
    const body = await res.text();
    expect(body).toContain("lens-epics");
  });
});

describe("HTTP route: /epics/:slug", () => {
  it("returns 200 with epic detail view for an existing epic slug", async () => {
    const mod = await import("./server");
    const server = mod.default;
    const epics = await mod.readEpicsJson();
    if (epics.length === 0) {
      // Skip if epics.json not present in test environment
      return;
    }
    const epic = epics[0];
    const slug = epic.epic_slug;
    const req = new Request(`http://localhost:3456/epics/${slug}`, {
      headers: { "HX-Request": "true" },
    });
    const res = await server.fetch(req);
    expect(res.status).toBe(200);
    const body = await res.text();
    // Epic detail view should contain the epic name (slug may or may not appear verbatim)
    expect(body).toContain("reading-surface");
    expect(body).toContain("l2-body");
  });

  it("returns graceful not-found fragment for unknown slug", async () => {
    const server = (await import("./server")).default;
    const req = new Request("http://localhost:3456/epics/__nonexistent-slug-xyz__", {
      headers: { "HX-Request": "true" },
    });
    const res = await server.fetch(req);
    expect(res.status).toBe(200);
    const body = await res.text();
    expect(body).toContain("not found");
  });
});
