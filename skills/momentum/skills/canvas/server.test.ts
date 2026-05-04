/**
 * Momentum Cycle Dashboard — server.test.ts
 *
 * Combined tests: computeCycleState (cycle timeline) + features lens helpers.
 * Run: bun test
 */

import { describe, test, expect, it } from "bun:test";
import {
  computeCycleState,
  analyzeGap,
  buildSortedRows,
  type Feature,
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

    expect(result.phases).toHaveLength(7);

    const slugs = result.phases.map((p) => p.slug);
    expect(slugs).toEqual([
      "triage",
      "feature-grooming",
      "epic-grooming",
      "refine",
      "sprint-planning",
      "sprint-dev",
      "retro",
    ]);

    // Optional phases: not-run
    expect(result.phases.find((p) => p.slug === "triage")?.state).toBe("not-run");
    expect(result.phases.find((p) => p.slug === "feature-grooming")?.state).toBe("not-run");
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

  test("active sprint with active status and started — sprint-planning done, sprint-dev done, retro next-required", () => {
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
    expect(result.phases.find((p) => p.slug === "sprint-dev")?.state).toBe("done");
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
    expect(result.phases.find((p) => p.slug === "sprint-dev")?.state).toBe("done");
    expect(result.phases.find((p) => p.slug === "retro")?.state).toBe("next-required");
    expect(result.nextRequired).toBe("retro");
    expect(result.lastSprintSlug).toBe("sprint-2026-04-01");
  });

  test("optional phases never receive next-required state", () => {
    const result = computeCycleState(null);

    const optionalSlugs = ["triage", "feature-grooming", "epic-grooming", "refine"];
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

    const optionalSlugs = ["triage", "feature-grooming", "epic-grooming", "refine"];
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
    expect(optional).toEqual(["triage", "feature-grooming", "epic-grooming", "refine"]);
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
// analyzeGap — features lens tests
// ---------------------------------------------------------------------------
describe("analyzeGap", () => {
  it("returns has_gap=true when zero stories and status is not working", () => {
    const feature: Feature = {
      feature_slug: "test-feature",
      name: "Test Feature",
      status: "partial",
      stories_done: 0,
      stories_remaining: 2,
      stories: ["story-a", "story-b"],
    };
    const storyMap: StoryMap = {};
    const result = analyzeGap(feature, storyMap);
    expect(result.has_gap).toBe(true);
  });

  it("returns has_gap=false when status is working regardless of story counts", () => {
    const feature: Feature = {
      feature_slug: "test-feature",
      name: "Test Feature",
      status: "working",
      stories_done: 0,
      stories_remaining: 0,
      stories: [],
    };
    const storyMap: StoryMap = {};
    const result = analyzeGap(feature, storyMap);
    expect(result.has_gap).toBe(false);
  });

  it("returns has_gap=false when stories_done > 0", () => {
    const feature: Feature = {
      feature_slug: "test-feature",
      name: "Test Feature",
      status: "partial",
      stories_done: 2,
      stories_remaining: 1,
      stories: ["story-a", "story-b", "story-c"],
    };
    const storyMap: StoryMap = {};
    const result = analyzeGap(feature, storyMap);
    expect(result.has_gap).toBe(false);
  });

  it("returns has_gap=true for not-working status with zero done stories", () => {
    const feature: Feature = {
      feature_slug: "test-feature",
      name: "Test Feature",
      status: "not-working",
      stories_done: 0,
      stories_remaining: 3,
      stories: ["story-a"],
    };
    const storyMap: StoryMap = {};
    const result = analyzeGap(feature, storyMap);
    expect(result.has_gap).toBe(true);
  });

  it("returns has_gap=true for not-started status with zero done stories", () => {
    const feature: Feature = {
      feature_slug: "test-feature",
      name: "Test Feature",
      status: "not-started",
      stories_done: 0,
      stories_remaining: 0,
      stories: [],
    };
    const storyMap: StoryMap = {};
    const result = analyzeGap(feature, storyMap);
    expect(result.has_gap).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// buildSortedRows — features lens sort tests
// ---------------------------------------------------------------------------
describe("buildSortedRows", () => {
  it("sorts gap rows first (alphabetically), then non-gap by severity", () => {
    const features: Feature[] = [
      {
        feature_slug: "z-working",
        name: "Z Working",
        status: "working",
        stories_done: 3,
        stories_remaining: 0,
        stories: [],
      },
      {
        feature_slug: "a-partial",
        name: "A Partial",
        status: "partial",
        stories_done: 0,
        stories_remaining: 2,
        stories: [],
      },
      {
        feature_slug: "b-not-working",
        name: "B Not Working",
        status: "not-working",
        stories_done: 0,
        stories_remaining: 1,
        stories: [],
      },
      {
        feature_slug: "c-partial-done",
        name: "C Partial Done",
        status: "partial",
        stories_done: 1,
        stories_remaining: 1,
        stories: [],
      },
      {
        feature_slug: "d-not-started",
        name: "D Not Started",
        status: "not-started",
        stories_done: 0,
        stories_remaining: 0,
        stories: [],
      },
    ];
    const storyMap: StoryMap = {};
    const rows = buildSortedRows(features, storyMap);

    expect(rows[0].name).toBe("A Partial");
    expect(rows[0].has_gap).toBe(true);
    expect(rows[1].name).toBe("B Not Working");
    expect(rows[1].has_gap).toBe(true);
    expect(rows[2].name).toBe("D Not Started");
    expect(rows[2].has_gap).toBe(true);

    expect(rows[3].name).toBe("C Partial Done");
    expect(rows[3].has_gap).toBe(false);
    expect(rows[4].name).toBe("Z Working");
    expect(rows[4].has_gap).toBe(false);
  });

  it("sorts non-gap rows alphabetically within same status group", () => {
    const features: Feature[] = [
      {
        feature_slug: "z-partial",
        name: "Z Partial",
        status: "partial",
        stories_done: 1,
        stories_remaining: 1,
        stories: [],
      },
      {
        feature_slug: "a-partial",
        name: "A Partial",
        status: "partial",
        stories_done: 2,
        stories_remaining: 0,
        stories: [],
      },
    ];
    const storyMap: StoryMap = {};
    const rows = buildSortedRows(features, storyMap);
    expect(rows[0].name).toBe("A Partial");
    expect(rows[1].name).toBe("Z Partial");
  });

  it("returns empty array for empty features input", () => {
    const rows = buildSortedRows([], {});
    expect(rows).toEqual([]);
  });
});

// ---------------------------------------------------------------------------
// Missing stories/index.json — features lens error handling
// ---------------------------------------------------------------------------
describe("analyzeGap with missing story index", () => {
  it("treats all stories as unknown when story map is empty", () => {
    const feature: Feature = {
      feature_slug: "test",
      name: "Test",
      status: "partial",
      stories_done: 0,
      stories_remaining: 1,
      stories: ["story-x"],
    };
    const result = analyzeGap(feature, {});
    expect(result.has_gap).toBe(true);
  });
});
