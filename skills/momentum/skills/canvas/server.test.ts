/**
 * Momentum Cycle Dashboard — server.test.ts
 *
 * Tests for the features lens route helpers.
 * Run: bun test
 */

import { describe, expect, it } from "bun:test";
import {
  analyzeGap,
  buildSortedRows,
  type Feature,
  type StoryMap,
} from "./server";

// ---------------------------------------------------------------------------
// analyzeGap — Task 2
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
// buildSortedRows — Task 3
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
      }, // gap
      {
        feature_slug: "b-not-working",
        name: "B Not Working",
        status: "not-working",
        stories_done: 0,
        stories_remaining: 1,
        stories: [],
      }, // gap
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
      }, // gap
    ];
    const storyMap: StoryMap = {};
    const rows = buildSortedRows(features, storyMap);

    // Gap rows come first (sorted alpha by name)
    expect(rows[0].name).toBe("A Partial");
    expect(rows[0].has_gap).toBe(true);
    expect(rows[1].name).toBe("B Not Working");
    expect(rows[1].has_gap).toBe(true);
    expect(rows[2].name).toBe("D Not Started");
    expect(rows[2].has_gap).toBe(true);

    // Non-gap rows: not-working(0) → partial(1) → working(2) → not-started(3)
    // C Partial Done has stories_done=1 so no gap, status=partial (severity 1)
    // Z Working has status=working (severity 2)
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
// Missing stories/index.json — Task 5
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
    // Empty map = stories/index.json absent
    const result = analyzeGap(feature, {});
    expect(result.has_gap).toBe(true);
  });
});
