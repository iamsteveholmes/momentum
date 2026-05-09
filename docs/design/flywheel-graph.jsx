// Flywheel · Direction B — PROVENANCE GRAPH.
//
// Thesis: the practice is a chain of encoding. A retro finding becomes
// a story stub becomes a distilled skill or rule. Show the chain, not
// the clock. Nodes and edges; the path from observation to durable
// practice is navigable in either direction.
//
// Narrow-column reality: a live d3 / mermaid graph at 700px is noise.
// Instead we render an explicit three-column "provenance slab" —
// findings on the left, generated stories in the middle, distilled
// skills/rules on the right — with SVG edges drawn between columns.
// Columns are selectable; clicking a node highlights its chain.
//
// This is *not* a flowchart of process. It's a ledger of provenance.

const { T, FINDINGS, SKILLS, GENERATED_STORIES } = window;

function FlywheelGraph() {
  const [activeKey, setActiveKey] = React.useState(null); // finding / story / skill key

  // Build a flat list of edges so highlight logic is straightforward.
  const edges = [];
  for (const f of FINDINGS) {
    edges.push({ from: f.key, to: f.producedStory });        // finding → story
    edges.push({ from: f.producedStory, to: f.distilledSkill }); // story → skill
  }

  const chain = activeKey ? chainOf(activeKey, edges) : null;

  const isActive = k => !activeKey ? true : chain.has(k);
  const inChain  = k => activeKey && chain.has(k);

  return (
    <div style={{
      fontFamily: T.fontSans, color: T.ink, background: T.paper,
      width: "100%", height: "100%", boxSizing: "border-box",
      overflow: "auto",
    }}>
      <GraphHeader activeKey={activeKey} onClear={() => setActiveKey(null)} />

      <div style={{
        padding: "16px 16px 36px",
      }}>
        <GraphSlab
          findings={FINDINGS}
          stories={GENERATED_STORIES}
          skills={SKILLS}
          edges={edges}
          activeKey={activeKey}
          setActiveKey={setActiveKey}
          isActive={isActive}
          inChain={inChain}
        />
        <GraphLegend />
      </div>
    </div>
  );
}

function chainOf(key, edges) {
  const set = new Set([key]);
  // walk forward and backward until stable
  let grew = true;
  while (grew) {
    grew = false;
    for (const e of edges) {
      if (set.has(e.from) && !set.has(e.to)) { set.add(e.to); grew = true; }
      if (set.has(e.to) && !set.has(e.from)) { set.add(e.from); grew = true; }
    }
  }
  return set;
}

function GraphHeader({ activeKey, onClear }) {
  return (
    <div style={{
      padding: "20px 24px 16px",
      borderBottom: `1px solid ${T.rule}`,
    }}>
      <div style={{
        fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.4,
        color: T.inkQuiet, textTransform: "uppercase", marginBottom: 8,
      }}>
        Canvas · Flywheel · Provenance
      </div>
      <div style={{
        fontFamily: T.fontSerif, fontSize: 22, letterSpacing: -0.3, fontWeight: 400,
        lineHeight: 1.25,
      }}>
        From observation to durable practice.
      </div>
      <div style={{
        fontFamily: T.fontSerif, fontSize: 15, lineHeight: 1.6,
        color: T.inkMuted, marginTop: 10, maxWidth: "62ch",
      }}>
        Every retro finding has a provenance chain: the story it produced,
        the rule or skill it distilled into. Click any node to trace its
        chain in both directions.
      </div>

      <div style={{
        display: "flex", alignItems: "center", gap: 14, marginTop: 14,
        fontFamily: T.fontMono, fontSize: 11, letterSpacing: 0.3,
        color: T.inkMuted,
      }}>
        <span>{FINDINGS.length} findings → {Object.keys(GENERATED_STORIES).length} stories → {SKILLS.length} skills</span>
        {activeKey && (
          <>
            <span>·</span>
            <span style={{ color: T.accent }}>tracing chain of · {truncate(activeKey, 28)}</span>
            <span style={{
              marginLeft: "auto",
              cursor: "pointer",
              padding: "2px 8px",
              border: `1px solid ${T.accentRule}`,
              color: T.accent,
              fontSize: 10,
            }} onClick={onClear}>
              clear
            </span>
          </>
        )}
      </div>
    </div>
  );
}

const ROW_H = 78;   // vertical space per row
const COL_W = 218;  // column width

function GraphSlab({ findings, stories, skills, edges, activeKey, setActiveKey, isActive, inChain }) {
  // Rows = findings (each finding is one horizontal track).
  const rows = findings;
  const height = rows.length * ROW_H + 60;
  const totalW = COL_W * 3 + 40;

  // Positions:
  //  finding row i  → (x = 0, y = i*ROW_H + 20, centered vertically)
  //  story   row i  → (x = COL_W, ...)
  //  skill   row i  → (x = COL_W*2, ...)
  const nodeY = i => i * ROW_H + 30;

  // Map keys → row index for edge drawing
  const findingIdx = Object.fromEntries(findings.map((f, i) => [f.key, i]));
  const storyIdx   = Object.fromEntries(findings.map((f, i) => [f.producedStory, i]));
  const skillIdx   = Object.fromEntries(findings.map((f, i) => [f.distilledSkill, i]));

  return (
    <div style={{
      overflowX: "auto",
      border: `1px solid ${T.rule}`,
      background: T.paperAlt,
    }}>
      <div style={{ width: totalW, minWidth: totalW, position: "relative", padding: "10px 20px" }}>
        {/* Column headers */}
        <div style={{
          display: "grid", gridTemplateColumns: `${COL_W}px ${COL_W}px ${COL_W}px`,
          gap: 0, marginBottom: 8,
        }}>
          <ColHead label="finding" sub="what was observed" />
          <ColHead label="story"   sub="what we built for it" />
          <ColHead label="skill"   sub="how it became durable" />
        </div>

        {/* Edges canvas — absolute under nodes */}
        <svg width={totalW - 40} height={height} style={{
          position: "absolute", top: 40, left: 20, pointerEvents: "none",
        }}>
          {edges.map((e, i) => {
            const fromX = edgeColX(e.from, findingIdx, storyIdx, skillIdx, true);
            const toX   = edgeColX(e.to,   findingIdx, storyIdx, skillIdx, false);
            const fromY = edgeRowY(e.from, findingIdx, storyIdx, skillIdx);
            const toY   = edgeRowY(e.to,   findingIdx, storyIdx, skillIdx);
            if (fromX == null || toX == null) return null;
            const mid = (fromX + toX) / 2;
            const d = `M ${fromX} ${fromY} C ${mid} ${fromY}, ${mid} ${toY}, ${toX} ${toY}`;
            const dim = activeKey && !(inChain(e.from) && inChain(e.to));
            return (
              <path key={i} d={d}
                stroke={dim ? T.rule : (activeKey ? T.accent : T.ruleStrong)}
                strokeWidth={activeKey && inChain(e.from) && inChain(e.to) ? 1.6 : 1}
                fill="none"
                opacity={dim ? 0.35 : 1}
              />
            );
          })}
        </svg>

        {/* Nodes */}
        <div style={{ position: "relative", height }}>
          {findings.map((f, i) => {
            const story = stories[f.producedStory];
            const skill = skills.find(s => s.key === f.distilledSkill);
            return (
              <React.Fragment key={f.key}>
                <FindingNode
                  finding={f} y={nodeY(i) - 30}
                  active={inChain(f.key)} dim={activeKey && !inChain(f.key)}
                  onClick={() => setActiveKey(f.key)}
                />
                <StoryNode
                  story={story} storyKey={f.producedStory} y={nodeY(i) - 30}
                  active={inChain(f.producedStory)} dim={activeKey && !inChain(f.producedStory)}
                  onClick={() => setActiveKey(f.producedStory)}
                />
                <SkillNode
                  skill={skill} y={nodeY(i) - 30}
                  active={inChain(f.distilledSkill)} dim={activeKey && !inChain(f.distilledSkill)}
                  onClick={() => setActiveKey(f.distilledSkill)}
                />
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </div>
  );
}

function edgeColX(key, fIdx, sIdx, kIdx, right) {
  // finding col right edge = COL_W-20; story col left = COL_W+20, right = COL_W*2-20
  // skill col left = COL_W*2 + 20
  if (key in fIdx) return right ? (COL_W - 18) : 18;
  if (key in sIdx) return right ? (COL_W * 2 - 18) : (COL_W + 18);
  if (key in kIdx) return right ? (COL_W * 3 - 18) : (COL_W * 2 + 18);
  return null;
}
function edgeRowY(key, fIdx, sIdx, kIdx) {
  const i = fIdx[key] ?? sIdx[key] ?? kIdx[key];
  if (i == null) return null;
  return i * ROW_H + 30;
}

function ColHead({ label, sub }) {
  return (
    <div style={{ padding: "0 6px" }}>
      <div style={{
        fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.4,
        color: T.accent, textTransform: "uppercase",
      }}>{label}</div>
      <div style={{
        fontFamily: T.fontSans, fontSize: 11, color: T.inkQuiet, marginTop: 2,
      }}>{sub}</div>
    </div>
  );
}

function FindingNode({ finding, y, active, dim, onClick }) {
  return (
    <NodeCard left={0} y={y} active={active} dim={dim} onClick={onClick}
              accent={finding.severity === "recurring" ? T.gap : T.accent}>
      <div style={{
        fontFamily: T.fontMono, fontSize: 9, letterSpacing: 0.3,
        color: finding.severity === "recurring" ? T.gap : T.inkQuiet,
        marginBottom: 4,
      }}>
        {finding.severity} · {finding.sprint.replace("sprint-2026-", "")}
      </div>
      <div style={{
        fontFamily: T.fontSerif, fontSize: 12.5, fontWeight: 500,
        color: T.ink, lineHeight: 1.35,
        display: "-webkit-box", WebkitLineClamp: 3, WebkitBoxOrient: "vertical",
        overflow: "hidden",
      }}>
        {finding.label}
      </div>
    </NodeCard>
  );
}

function StoryNode({ story, storyKey, y, active, dim, onClick }) {
  if (!story) return null;
  const badgeColor = story.status === "working" ? "#3e7a5a" :
                     story.status === "partial" ? "#a88328" : "#8a8a8a";
  return (
    <NodeCard left={COL_W} y={y} active={active} dim={dim} onClick={onClick} accent={T.inkQuiet}>
      <div style={{
        fontFamily: T.fontMono, fontSize: 9, letterSpacing: 0.3,
        color: T.inkQuiet, marginBottom: 4,
        display: "flex", alignItems: "center", gap: 6,
      }}>
        <span style={{
          width: 6, height: 6, borderRadius: "50%", background: badgeColor,
        }} />
        <span>{story.status}</span>
      </div>
      <div style={{
        fontFamily: T.fontSans, fontSize: 12.5, fontWeight: 500,
        color: T.ink, lineHeight: 1.35,
        display: "-webkit-box", WebkitLineClamp: 3, WebkitBoxOrient: "vertical",
        overflow: "hidden",
      }}>
        {story.title}
      </div>
    </NodeCard>
  );
}

function SkillNode({ skill, y, active, dim, onClick }) {
  if (!skill) return null;
  return (
    <NodeCard left={COL_W * 2} y={y} active={active} dim={dim} onClick={onClick} accent={T.accent}>
      <div style={{
        fontFamily: T.fontMono, fontSize: 9, letterSpacing: 0.3,
        color: T.accent, marginBottom: 4, textTransform: "uppercase",
      }}>
        {skill.kind}
      </div>
      <div style={{
        fontFamily: T.fontSans, fontSize: 12.5, fontWeight: 500,
        color: T.ink, lineHeight: 1.35,
        display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical",
        overflow: "hidden",
        marginBottom: 4,
      }}>
        {skill.name}
      </div>
      <div style={{
        fontFamily: T.fontMono, fontSize: 9, color: T.inkFaint, letterSpacing: 0.3,
        overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
      }}>
        {skill.encodedIn[0]}{skill.encodedIn.length > 1 && ` +${skill.encodedIn.length - 1}`}
      </div>
    </NodeCard>
  );
}

function NodeCard({ left, y, active, dim, onClick, accent, children }) {
  return (
    <div
      onClick={onClick}
      style={{
        position: "absolute", left: left + 14, top: y, width: COL_W - 28,
        padding: "10px 12px",
        background: T.paper,
        border: `1px solid ${active ? accent : T.rule}`,
        borderLeft: `3px solid ${active ? accent : T.ruleStrong}`,
        opacity: dim ? 0.42 : 1,
        cursor: "pointer",
        transition: "opacity 120ms, border-color 120ms",
        boxShadow: active ? `0 0 0 2px ${accent}22` : "none",
      }}>
      {children}
    </div>
  );
}

function GraphLegend() {
  return (
    <div style={{
      marginTop: 16,
      display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16,
      fontFamily: T.fontSans, fontSize: 12, color: T.inkMuted, lineHeight: 1.55,
    }}>
      <div>
        <div style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.3,
          color: T.inkQuiet, textTransform: "uppercase", marginBottom: 6,
        }}>interacting</div>
        Click any node to highlight its full chain. The graph scrolls horizontally at 700px —
        the three columns are fixed-width so reading stays predictable.
      </div>
      <div>
        <div style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.3,
          color: T.inkQuiet, textTransform: "uppercase", marginBottom: 6,
        }}>color</div>
        <span style={{ color: T.accent }}>accent</span> = skill / rule · <span style={{ color: T.gap }}>warm</span> = recurring finding · slate = story.
      </div>
    </div>
  );
}

function truncate(s, n) { return s.length > n ? s.slice(0, n - 1) + "…" : s; }

Object.assign(window, { FlywheelGraph });
