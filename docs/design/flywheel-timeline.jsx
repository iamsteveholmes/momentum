// Flywheel · Direction A — TIMELINE.
//
// Thesis: the practice moves forward in time. Show sprints as vertical
// lanes; retro findings attach at the sprint they were produced;
// distilled skills appear where they were encoded. The story is the
// chronology — how thought accumulated into practice over weeks.
//
// Narrow-column reality: at 700px wide, horizontal lanes don't breathe.
// We use vertical lanes as a time spine, with findings + skills as
// off-spine entries linked by a short connector. Reads top-to-bottom,
// oldest to newest (or newest first — see Tweak).

const { T, TIMELINE_SPRINTS, FINDINGS, SKILLS, GENERATED_STORIES, BADGE_BY_KEY } = window;

function FlywheelTimeline() {
  // Group findings by sprint, newest sprint first.
  const sprints = [...TIMELINE_SPRINTS].reverse();
  const bySprint = Object.fromEntries(sprints.map(s => [s.key, []]));
  for (const f of FINDINGS) if (bySprint[f.sprint]) bySprint[f.sprint].push(f);

  return (
    <div style={{
      fontFamily: T.fontSans, color: T.ink, background: T.paper,
      width: "100%", height: "100%", boxSizing: "border-box",
      overflow: "auto",
    }}>
      <TimelineHeader />

      <div style={{ padding: "10px 24px 32px" }}>
        {sprints.map((sp, i) => (
          <TimelineSprintBlock
            key={sp.key}
            sprint={sp}
            findings={bySprint[sp.key]}
            isFirst={i === 0}
            isLast={i === sprints.length - 1}
          />
        ))}
        <TimelineLegend />
      </div>
    </div>
  );
}

function TimelineHeader() {
  return (
    <div style={{
      padding: "20px 24px 16px",
      borderBottom: `1px solid ${T.rule}`,
    }}>
      <div style={{
        fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.4,
        color: T.inkQuiet, textTransform: "uppercase", marginBottom: 8,
      }}>
        Canvas · Flywheel · Timeline
      </div>
      <div style={{
        fontFamily: T.fontSerif, fontSize: 22, letterSpacing: -0.3, fontWeight: 400,
        lineHeight: 1.25,
      }}>
        How the practice moved forward.
      </div>
      <div style={{
        fontFamily: T.fontSerif, fontSize: 15, lineHeight: 1.6,
        color: T.inkMuted, marginTop: 10, maxWidth: "62ch",
      }}>
        Each sprint is a step in the chronology. Retro findings attach at the
        sprint that produced them; distilled skills and rules show up where they
        were encoded. Scroll top-to-bottom, newest first.
      </div>

      <div style={{
        display: "flex", gap: 18, marginTop: 14,
        fontFamily: T.fontMono, fontSize: 11, letterSpacing: 0.3,
        color: T.inkMuted,
      }}>
        <span>{FINDINGS.length} findings</span>
        <span>·</span>
        <span>{SKILLS.length} distilled</span>
        <span>·</span>
        <span>{TIMELINE_SPRINTS.length} sprints</span>
      </div>
    </div>
  );
}

function TimelineSprintBlock({ sprint, findings, isFirst, isLast }) {
  const dim = !sprint.active;
  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "84px 1fr",
      columnGap: 16,
    }}>
      {/* Spine column */}
      <div style={{
        position: "relative",
        paddingTop: 22,
      }}>
        {/* vertical line */}
        <div style={{
          position: "absolute",
          left: 12,
          top: isFirst ? 32 : 0,
          bottom: isLast ? 40 : 0,
          width: 1,
          background: T.ruleStrong,
        }} />
        {/* node */}
        <div style={{
          position: "absolute", left: 6, top: 26,
          width: 13, height: 13, borderRadius: "50%",
          background: sprint.active ? T.accent : T.paper,
          border: `2px solid ${sprint.active ? T.accent : T.ruleStrong}`,
        }} />
        {/* sprint label */}
        <div style={{
          paddingLeft: 28, paddingTop: 18,
        }}>
          <div style={{
            fontFamily: T.fontMono, fontSize: 10, color: sprint.active ? T.accent : T.inkMuted,
            fontWeight: 500, letterSpacing: 0.3,
          }}>
            {sprint.label}
          </div>
          <div style={{
            fontFamily: T.fontMono, fontSize: 9, color: T.inkFaint, letterSpacing: 0.3,
            marginTop: 2, lineHeight: 1.3,
          }}>
            {sprint.dates}
          </div>
        </div>
      </div>

      {/* Entries column */}
      <div style={{
        paddingTop: 22, paddingBottom: 18,
        opacity: dim ? 0.92 : 1,
      }}>
        {findings.length === 0 && (
          <div style={{
            padding: "16px 0 8px",
            fontFamily: T.fontSans, fontSize: 12, color: T.inkFaint,
          }}>
            no findings yet.
          </div>
        )}
        {findings.map(f => <TimelineFindingEntry key={f.key} finding={f} />)}
      </div>
    </div>
  );
}

function TimelineFindingEntry({ finding }) {
  const story = GENERATED_STORIES[finding.producedStory];
  const skill = SKILLS.find(s => s.key === finding.distilledSkill);
  const severityColor = finding.severity === "recurring" ? T.gap : T.inkQuiet;

  return (
    <div style={{
      marginBottom: 18,
      padding: "14px 16px",
      background: T.paper,
      border: `1px solid ${T.rule}`,
      borderLeft: `3px solid ${finding.severity === "recurring" ? T.gap : T.accentRule}`,
    }}>
      <div style={{
        display: "flex", alignItems: "baseline", justifyContent: "space-between",
        gap: 8, marginBottom: 6,
      }}>
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.3,
          color: T.inkQuiet, textTransform: "uppercase",
        }}>
          finding
        </span>
        <span style={{
          fontFamily: T.fontMono, fontSize: 9.5, color: severityColor, letterSpacing: 0.3,
        }}>
          {finding.severity} · {finding.when}
        </span>
      </div>

      {/* Label */}
      <div style={{
        fontFamily: T.fontSerif, fontSize: 15, fontWeight: 500,
        color: T.ink, lineHeight: 1.35, marginBottom: 6,
      }}>
        {finding.label}
      </div>

      {/* Note — the prose */}
      <div style={{
        fontFamily: T.fontSerif, fontSize: 13.5, lineHeight: 1.55,
        color: T.inkMuted, marginBottom: 12, maxWidth: "58ch",
      }}>
        {finding.note}
      </div>

      {/* Chain */}
      <div style={{ display: "grid", rowGap: 4 }}>
        <TimelineChainLink type="story" label={story?.title} meta={story?.status} refKey={finding.producedStory} />
        <TimelineChainLink type="skill" label={skill?.name} meta={skill?.kind} refKey={finding.distilledSkill} />
      </div>
    </div>
  );
}

function TimelineChainLink({ type, label, meta, refKey }) {
  if (!label) return null;
  return (
    <div style={{
      display: "grid", gridTemplateColumns: "16px 54px 1fr auto", alignItems: "baseline",
      columnGap: 8,
      padding: "4px 0",
      cursor: "pointer",
    }}>
      <span style={{
        fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
      }}>↳</span>
      <span style={{
        fontFamily: T.fontMono, fontSize: 10, letterSpacing: 0.4,
        color: type === "skill" ? T.accent : T.inkQuiet,
        textTransform: "uppercase",
      }}>
        {type}
      </span>
      <span style={{
        fontFamily: T.fontSans, fontSize: 12.5, color: T.ink,
        lineHeight: 1.4,
        overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
      }}>
        {label}
      </span>
      <span style={{
        fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
      }}>
        {meta}
      </span>
    </div>
  );
}

function TimelineLegend() {
  return (
    <div style={{
      marginTop: 10, paddingTop: 18, borderTop: `1px solid ${T.rule}`,
      display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18,
      fontFamily: T.fontSans, fontSize: 12, color: T.inkMuted, lineHeight: 1.55,
    }}>
      <div>
        <div style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.3,
          color: T.inkQuiet, textTransform: "uppercase", marginBottom: 6,
        }}>reading this</div>
        Time runs top-to-bottom, newest first. Each sprint block contains the findings that
        landed during its retro. Findings carry forward: the story they produced and the
        skill they distilled.
      </div>
      <div>
        <div style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.3,
          color: T.inkQuiet, textTransform: "uppercase", marginBottom: 6,
        }}>severity</div>
        <span style={{ color: T.gap }}>recurring</span> — same shape seen before.<br/>
        <span style={{ color: T.inkQuiet }}>one-shot</span> — first observation.
      </div>
    </div>
  );
}

Object.assign(window, { FlywheelTimeline });
