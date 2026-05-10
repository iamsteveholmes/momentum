// Sprints Level-1 view, designed for 700px wide.
// Sections per Steve's brief §5: active sprint header, stories in bands,
// gate signal row, cross-cut to features, recent sprints strip.

const { T, ACTIVE_SPRINT, SPRINT_ADVANCES, RECENT_SPRINTS,
        Badge, GapFlag, Breadcrumb, SumStat,
        GateTrio, GateDots, GateHealthBar, BADGE_BY_KEY } = window;

function SprintsView() {
  const s = ACTIVE_SPRINT;
  const counts = computeGateCounts(s);
  return (
    <div style={{
      fontFamily: T.fontSans, color: T.ink, background: T.paper,
      width: "100%", height: "100%", boxSizing: "border-box",
      overflow: "auto",
    }}>
      {/* Header */}
      <div style={{
        padding: "20px 24px 16px",
        borderBottom: `1px solid ${T.rule}`,
      }}>
        <Breadcrumb items={["Canvas", "Sprints"]} />
        <div style={{
          display: "flex", alignItems: "baseline", justifyContent: "space-between",
          marginTop: 8, gap: 14,
        }}>
          <div style={{
            fontFamily: T.fontSerif, fontSize: 24, letterSpacing: -0.3, fontWeight: 400,
            lineHeight: 1.2,
          }}>
            {s.key}
          </div>
          <div style={{
            fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
            whiteSpace: "nowrap",
          }}>
            {s.started} · {s.horizon}
          </div>
        </div>
        <div style={{
          fontFamily: T.fontSerif, fontSize: 15, lineHeight: 1.6,
          color: T.ink, marginTop: 10, maxWidth: "60ch",
        }}>
          {s.goal}
        </div>

        {/* Summary strip */}
        <div style={{
          display: "flex", gap: 18, marginTop: 14, flexWrap: "wrap",
          fontFamily: T.fontMono, fontSize: 11, letterSpacing: 0.3,
        }}>
          <SumStat n={s.stories.inWave.length} label="in wave" state="partial" />
          <SumStat n={s.stories.merged.length} label="merged" state="working" />
          <SumStat n={s.stories.blocked.length} label="blocked" state="not-working" />
        </div>
      </div>

      {/* Gate-health strip — per-sprint quality signal */}
      <div style={{
        padding: "14px 24px",
        borderBottom: `1px solid ${T.rule}`,
        background: T.paperAlt,
      }}>
        <div style={{
          display: "flex", alignItems: "baseline", justifyContent: "space-between",
          marginBottom: 8,
        }}>
          <span style={{
            fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.4,
            color: T.inkQuiet, textTransform: "uppercase",
          }}>quality gates</span>
          <span style={{
            fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
          }}>pass / of run · grey = pending</span>
        </div>
        <GateHealthBar counts={counts} />
      </div>

      {/* Story bands */}
      <div style={{ padding: "18px 24px 8px" }}>
        <Band label="in wave" count={s.stories.inWave.length}>
          {s.stories.inWave.map(st => (
            <StoryRow key={st.key} story={st} state="partial" />
          ))}
        </Band>

        <Band label="merged" count={s.stories.merged.length} terminal>
          {s.stories.merged.map(st => (
            <StoryRow key={st.key} story={st} state="working" terminal />
          ))}
        </Band>

        <Band label="blocked" count={s.stories.blocked.length} attention>
          {s.stories.blocked.map(st => (
            <BlockedRow key={st.key} story={st} />
          ))}
        </Band>
      </div>

      {/* Cross-cut: features this sprint is advancing */}
      <div style={{
        padding: "20px 24px 8px",
        borderTop: `1px solid ${T.rule}`,
      }}>
        <div style={{
          display: "flex", alignItems: "baseline", justifyContent: "space-between",
          marginBottom: 10,
        }}>
          <span style={{
            fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.4,
            color: T.accent, textTransform: "uppercase",
          }}>advances ↗ features</span>
          <span style={{
            fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
          }}>jumps to Features view</span>
        </div>
        {SPRINT_ADVANCES.map(a => (
          <div key={a.key} style={{
            display: "grid", gridTemplateColumns: "1fr auto auto",
            alignItems: "center", gap: 10,
            padding: "9px 0", borderBottom: `1px solid ${T.rule}`,
            cursor: "pointer",
          }}>
            <span style={{
              fontFamily: T.fontSans, fontSize: 13, color: T.ink, fontWeight: 500,
              overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
            }}>
              {a.name}
            </span>
            <span style={{
              fontFamily: T.fontMono, fontSize: 10, color: T.inkMuted, letterSpacing: 0.3,
            }}>
              {a.touching} {a.touching === 1 ? "story" : "stories"}
            </span>
            <span style={{
              fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
            }}>→</span>
          </div>
        ))}
      </div>

      {/* Recent sprints strip */}
      <div style={{
        padding: "20px 24px 28px",
        borderTop: `1px solid ${T.rule}`,
        marginTop: 10,
      }}>
        <div style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.4,
          color: T.inkQuiet, textTransform: "uppercase", marginBottom: 10,
        }}>
          recent · last 3 sprints
        </div>
        <div style={{
          display: "grid", gridTemplateColumns: "1fr",
          gap: 1, background: T.rule, border: `1px solid ${T.rule}`,
        }}>
          {RECENT_SPRINTS.map(r => (
            <RecentSprintCard key={r.key} sprint={r} />
          ))}
        </div>
      </div>
    </div>
  );
}

function Band({ label, count, children, terminal, attention }) {
  return (
    <div style={{ marginBottom: 18 }}>
      <div style={{
        display: "flex", alignItems: "baseline", gap: 10,
        marginBottom: 6, paddingBottom: 6,
        borderBottom: `1px solid ${T.rule}`,
      }}>
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.4,
          color: attention ? T.gap : (terminal ? T.inkQuiet : T.accent),
          textTransform: "uppercase",
        }}>{label}</span>
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
        }}>{count}</span>
      </div>
      {count === 0 && (
        <div style={{
          fontFamily: T.fontSans, fontSize: 12, color: T.inkFaint,
          padding: "6px 0 8px",
        }}>
          none.
        </div>
      )}
      {children}
    </div>
  );
}

function StoryRow({ story, terminal }) {
  return (
    <div style={{
      padding: "10px 0",
      borderBottom: `1px solid ${T.rule}`,
      opacity: terminal ? 0.68 : 1,
      cursor: "pointer",
    }}>
      <div style={{
        display: "grid", gridTemplateColumns: "auto 1fr auto",
        alignItems: "center", gap: 10,
      }}>
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 0.3,
          color: T.inkFaint, width: 36,
        }}>
          {story.wave ? `w${story.wave}` : "—"}
        </span>
        <span style={{
          fontFamily: T.fontSans, fontSize: 13, color: T.ink,
          lineHeight: 1.35,
          overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
        }}>
          {story.title}
        </span>
        <GateTrio gates={story.gates} compact />
      </div>
      {story.advances?.length > 0 && (
        <div style={{
          marginTop: 4, marginLeft: 46,
          fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
        }}>
          ↗ {story.advances.map(k => k.replace(/-/g, " ")).join(" · ")}
        </div>
      )}
    </div>
  );
}

function BlockedRow({ story }) {
  return (
    <div style={{
      padding: "10px 0",
      borderBottom: `1px solid ${T.rule}`,
    }}>
      <div style={{
        display: "grid", gridTemplateColumns: "auto 1fr auto",
        alignItems: "center", gap: 10,
      }}>
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 0.3,
          color: T.gap, width: 36,
        }}>
          blk
        </span>
        <span style={{
          fontFamily: T.fontSans, fontSize: 13, color: T.ink,
          overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
        }}>
          {story.title}
        </span>
        <GapFlag />
      </div>
      <div style={{
        marginTop: 6, marginLeft: 46,
        fontFamily: T.fontSans, fontSize: 12, color: T.inkMuted, lineHeight: 1.5,
        maxWidth: "58ch",
      }}>
        {story.reason}
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint,
          letterSpacing: 0.3, marginLeft: 6,
        }}>
          blocked by · {story.blockedBy}
        </span>
      </div>
    </div>
  );
}

function RecentSprintCard({ sprint }) {
  return (
    <div style={{
      background: T.paper, padding: "12px 16px",
      opacity: 0.78,
      cursor: "pointer",
      display: "grid",
      gridTemplateColumns: "1fr auto",
      gap: 10,
    }}>
      <div>
        <div style={{
          display: "flex", alignItems: "baseline", gap: 10,
        }}>
          <span style={{
            fontFamily: T.fontMono, fontSize: 11, color: T.ink, fontWeight: 500,
            letterSpacing: 0.3,
          }}>{sprint.key}</span>
          <span style={{
            fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
          }}>{sprint.dates}</span>
        </div>
        <div style={{
          fontFamily: T.fontSans, fontSize: 12.5, color: T.inkMuted,
          marginTop: 3, lineHeight: 1.45,
          overflow: "hidden", textOverflow: "ellipsis",
          display: "-webkit-box", WebkitLineClamp: 1, WebkitBoxOrient: "vertical",
        }}>
          {sprint.goal}
        </div>
      </div>
      <div style={{
        fontFamily: T.fontMono, fontSize: 10, color: T.inkQuiet,
        letterSpacing: 0.3, textAlign: "right", lineHeight: 1.5,
      }}>
        <div>{sprint.merged} merged</div>
        <div style={{ color: sprint.gateHealth === "clean" ? T.inkMuted : T.gap }}>
          {sprint.gateHealth}
        </div>
        <div style={{ color: T.inkFaint }}>{sprint.findings} findings</div>
      </div>
    </div>
  );
}

function computeGateCounts(sprint) {
  const all = [...sprint.stories.inWave, ...sprint.stories.merged];
  const init = () => ({ pass: 0, fail: 0, pending: 0 });
  const out = { avfl: init(), cr: init(), e2e: init() };
  for (const s of all) {
    for (const g of ["avfl", "cr", "e2e"]) {
      const v = s.gates[g];
      if (v === "pass") out[g].pass++;
      else if (v === "fail") out[g].fail++;
      else out[g].pending++;
    }
  }
  return out;
}

Object.assign(window, { SprintsView });
