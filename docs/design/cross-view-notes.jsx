// Cross-view interactions — annotated wireframe + prose.
// Not a working prototype. Diagrammatic.

const { T } = window;

function CrossViewNotes() {
  return (
    <div style={{
      fontFamily: T.fontSans, color: T.ink, background: T.paper,
      width: "100%", height: "100%", boxSizing: "border-box",
      padding: "28px 36px", overflow: "auto",
    }}>
      <div style={{
        fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.4,
        color: T.inkQuiet, textTransform: "uppercase", marginBottom: 10,
      }}>
        Cross-view interactions
      </div>
      <div style={{
        fontFamily: T.fontSerif, fontSize: 22, letterSpacing: -0.3, fontWeight: 400,
        lineHeight: 1.25, marginBottom: 16,
      }}>
        Three lenses, one project. How they link.
      </div>

      {/* Annotated triangle wireframe */}
      <div style={{ marginBottom: 28 }}>
        <TriangleDiagram />
      </div>

      {/* Prose */}
      <Prose>
        <P title="Features → Sprints">
          Clicking a feature name in the Features view jumps to Sprints, filtered to the
          sprints whose stories advanced that feature. The filter chip at the top of Sprints
          reads <M>advancing · {"{feature-name}"}</M>; clearing it returns to the current
          active sprint. For features with no sprint activity, the filtered view is honest:
          "No sprint has advanced this feature yet." Not an error state — just silence.
        </P>
        <P title="Sprints → Features">
          The "advances ↗ features" block on a sprint lists the features its stories are
          touching. Each item is a jump-back: clicking opens that feature in Features view,
          scrolled to it, with a breadcrumb crumb indicating "from sprint-04-22." The
          developer can bounce between execution and value view without losing orientation.
        </P>
        <P title="Flywheel → Story → Skill (and back)">
          In the provenance direction, every node is navigable in both directions.
          Clicking a <M>finding</M> highlights the chain forward to the story and skill it
          produced. Clicking a <M>skill</M> traces backward: which findings distilled into
          this, across which sprints. Chain-highlighting is local to Flywheel; drilling
          <em> into</em> the story crosses over to Sprints (if the story is in flight) or
          to a Level-2 story page (if it has been merged or is in the backlog).
        </P>
        <P title="Flywheel → Sprints">
          Each finding is stamped with the sprint that produced it. Clicking the sprint
          label on a finding opens that sprint in Sprints view (if historical) or jumps to
          the current Sprints view (if active). Sprints never hides old sprints; it just
          de-emphasizes them. Historical-sprint view is the same Level-1 Sprints layout
          with a "read-only" chrome and terminal opacity.
        </P>
        <P title="Return paths and breadcrumbs">
          Every cross-view jump lands with a breadcrumb that remembers origin —
          <M>Canvas › Sprints › advancing · retro-and-flywheel</M>. The breadcrumb is
          active: clicking the middle segment unfilters; clicking "Canvas" returns to the
          current lens without filters. No separate back button; the breadcrumb IS the
          back button.
        </P>
        <P title="What does NOT cross-link">
          Quality-gate chips are silent. They don't link anywhere. A pending gate is just
          a pending gate; there is no separate gate-drilldown view in this pass. If gates
          grow their own surface later (e.g. "why did AVFL fail on this story?"), that's a
          future feature, not this pass.
        </P>
      </Prose>
    </div>
  );
}

function TriangleDiagram() {
  // Three labeled boxes in a triangle, with annotated arrows between them.
  return (
    <div style={{
      position: "relative",
      width: "100%",
      height: 320,
      background: T.paperAlt,
      border: `1px solid ${T.rule}`,
      padding: 20,
      boxSizing: "border-box",
    }}>
      {/* Nodes */}
      <Node top={18} left="50%" translate="-50%" title="Features" sub="what the product IS" />
      <Node bottom={18} left={18} title="Sprints" sub="what the practice is DOING" />
      <Node bottom={18} right={18} title="Flywheel" sub="how the practice COMPOUNDS" />

      {/* Arrows */}
      <svg width="100%" height="100%" style={{
        position: "absolute", inset: 0, pointerEvents: "none",
      }}>
        {/* Features <-> Sprints */}
        <Arrow x1="35%" y1="26%" x2="22%" y2="72%" label="click feature → filter sprints" side="left" />
        <Arrow x1="28%" y1="72%" x2="42%" y2="30%" label="advances ↗ features" side="right" dashed />
        {/* Sprints <-> Flywheel */}
        <Arrow x1="36%" y1="85%" x2="64%" y2="85%" label="sprint label ↔ sprint view" side="bottom" />
        {/* Flywheel -> Features (optional) */}
        <Arrow x1="78%" y1="72%" x2="58%" y2="26%" label="skill encoded in → feature" side="right" dashed />
      </svg>
    </div>
  );
}

function Node({ title, sub, top, left, right, bottom, translate }) {
  const t = translate ? `translate(${translate}, 0)` : "";
  return (
    <div style={{
      position: "absolute", top, left, right, bottom,
      transform: t,
      padding: "10px 16px",
      background: T.paper, border: `1px solid ${T.ruleStrong}`,
      minWidth: 140, textAlign: "center",
    }}>
      <div style={{
        fontFamily: T.fontMono, fontSize: 11, fontWeight: 500,
        color: T.accent, letterSpacing: 0.3,
      }}>{title}</div>
      <div style={{
        fontFamily: T.fontSans, fontSize: 11, color: T.inkMuted,
        marginTop: 3,
      }}>{sub}</div>
    </div>
  );
}

function Arrow({ x1, y1, x2, y2, label, side, dashed }) {
  return (
    <g>
      <line x1={x1} y1={y1} x2={x2} y2={y2}
        stroke={T.ruleStrong} strokeWidth="1"
        strokeDasharray={dashed ? "3 3" : "none"}
        markerEnd="url(#arrow)"
      />
      <defs>
        <marker id="arrow" viewBox="0 0 8 8" refX="6" refY="4"
                markerWidth="6" markerHeight="6" orient="auto">
          <path d="M 0 0 L 8 4 L 0 8 z" fill={T.ruleStrong} />
        </marker>
      </defs>
      <text x={`calc((${x1} + ${x2}) / 2)`} y={`calc((${y1} + ${y2}) / 2)`}
        fontFamily={T.fontMono} fontSize="9" fill={T.inkQuiet}
        textAnchor="middle">
        {label}
      </text>
    </g>
  );
}

function Prose({ children }) {
  return (
    <div style={{
      display: "flex", flexDirection: "column", gap: 16,
      maxWidth: "72ch",
    }}>
      {children}
    </div>
  );
}
function P({ title, children }) {
  return (
    <div>
      <div style={{
        fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.3,
        color: T.accent, textTransform: "uppercase", marginBottom: 4,
      }}>{title}</div>
      <div style={{
        fontFamily: T.fontSerif, fontSize: 14.5, lineHeight: 1.6, color: T.ink,
      }}>{children}</div>
    </div>
  );
}
function M({ children }) {
  return <span style={{
    fontFamily: T.fontMono, fontSize: 12.5,
    color: T.inkMuted, background: T.paperAlt,
    padding: "1px 5px", borderRadius: 2,
  }}>{children}</span>;
}

Object.assign(window, { CrossViewNotes });
