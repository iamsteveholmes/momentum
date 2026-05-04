/**
 * Tests for computeCycleState()
 * Run: bun test
 */

import { describe, test, expect } from "bun:test";
import { computeCycleState } from "./server";

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
// Test: empty sprints index → all nodes pending/not-run, next-required = sprint-planning
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

  // ---------------------------------------------------------------------------
  // Test: one completed sprint with retro → all required done; new cycle starts
  // ---------------------------------------------------------------------------

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

    // All required phases in the completed cycle are done
    // But this is the NEW cycle after retro — so we look at what's run since retro
    // No new sprint started → next-required = sprint-planning in new cycle
    expect(result.nextRequired).toBe("sprint-planning");
    expect(result.lastSprintSlug).toBe("sprint-2026-04-01");

    // New cycle: no phases have run yet
    expect(result.phases.find((p) => p.slug === "sprint-planning")?.state).toBe("next-required");
    expect(result.phases.find((p) => p.slug === "sprint-dev")?.state).toBe("pending");
    expect(result.phases.find((p) => p.slug === "retro")?.state).toBe("pending");
  });

  // ---------------------------------------------------------------------------
  // Test: sprint-planning done but sprint-dev not started → sprint-planning done, sprint-dev next-required
  // ---------------------------------------------------------------------------

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
    expect(result.lastSprintSlug).toBeNull(); // no completed sprint yet
  });

  // ---------------------------------------------------------------------------
  // Test: all required phases complete → cycle complete, nextRequired = null
  // ---------------------------------------------------------------------------

  test("completed sprint with retro AND active sprint — correctly identifies current cycle", () => {
    // Prior cycle completed. New active sprint ongoing.
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

    // Current cycle: active sprint started → sprint-planning done, sprint-dev done, retro next-required
    expect(result.phases.find((p) => p.slug === "sprint-planning")?.state).toBe("done");
    expect(result.phases.find((p) => p.slug === "sprint-dev")?.state).toBe("done");
    expect(result.phases.find((p) => p.slug === "retro")?.state).toBe("next-required");
    expect(result.nextRequired).toBe("retro");
    expect(result.lastSprintSlug).toBe("sprint-2026-04-01");
  });

  // ---------------------------------------------------------------------------
  // Test: optional phases NEVER get next-required state
  // ---------------------------------------------------------------------------

  test("optional phases never receive next-required state", () => {
    // Even in a fresh cycle where nothing has run, optional phases stay not-run
    const result = computeCycleState(null);

    const optionalSlugs = ["triage", "feature-grooming", "epic-grooming", "refine"];
    for (const slug of optionalSlugs) {
      const phase = result.phases.find((p) => p.slug === slug);
      expect(phase?.required).toBe(false);
      expect(phase?.state).not.toBe("next-required");
    }
  });

  test("optional phases are never next-required even mid-cycle", () => {
    // Sprint planning is done — optional phases still don't get next-required
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

  // ---------------------------------------------------------------------------
  // Test: required flags are correct
  // ---------------------------------------------------------------------------

  test("required field is set correctly for all phases", () => {
    const result = computeCycleState(null);

    const required = result.phases.filter((p) => p.required).map((p) => p.slug);
    const optional = result.phases.filter((p) => !p.required).map((p) => p.slug);

    expect(required).toEqual(["sprint-planning", "sprint-dev", "retro"]);
    expect(optional).toEqual(["triage", "feature-grooming", "epic-grooming", "refine"]);
  });

  // ---------------------------------------------------------------------------
  // Test: lastSprintSlug returns most recent completed sprint
  // ---------------------------------------------------------------------------

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

  // ---------------------------------------------------------------------------
  // Test: cycle with completed sprint that has no retro — sprint-dev done, retro next-required
  // ---------------------------------------------------------------------------

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
