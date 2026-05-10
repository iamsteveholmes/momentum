// Pass 4 · Sprints + Flywheel lens adapters @ 700px pane.
// Thin wrappers around the existing Pass 3 views, adapted for dark mode and
// the narrower content column (648px inside anchor rail).

const { T, ACTIVE_SPRINT, SPRINT_ADVANCES, RECENT_SPRINTS,
        TIMELINE_SPRINTS, FINDINGS, SKILLS, GENERATED_STORIES,
        Badge, GapFlag, Breadcrumb,
        GateTrio, GateDots, GateHealthBar } = window;

// ─── SPRINTS LENS ─────────────────────────────────────────────────────────
function SprintsLens({ tweaks, onOpenFeature, onOpenSprint }) {
  const s = ACTIVE_SPRINT;
  const d = tweaks.dark;
  const C = lensColors(d);
  const counts = gateCounts(s);

  return (
    <section data-lens-id="sprints" style={{
      padding: "40px 24px 56px",
      background: d ? T.paperDarkAlt : T.paperAlt,
      color: C.ink, fontFamily: T.fontSans,
      borderTop: `1px solid ${C.rule}`,
    }}>
      <Header n="02" label="Sprints" tweaks={tweaks} />

      <div style={{
        display: "flex", alignItems: "baseline", justifyContent: "space-between",
        marginTop: 10, gap: 12,
      }}>
        <div style={{
          fontFamily: T.fontSerif, fontSize: 22, letterSpacing: -0.25, fontWeight: 400,
          lineHeight: 1.25,
        }}>
          {s.key}
        </div>
        <div style={{
          fontFamily: T.fontMono, fontSize: 10, color: C.inkFaint, letterSpacing: 0.3,
          whiteSpace: "nowrap",
        }}>
          {s.started} · {s.horizon}
        </div>
      </div>

      <div style={{
        fontFamily: T.fontSerif, fontSize: 15, lineHeight: 1.6,
        color: C.ink, marginTop: 10, maxWidth: "60ch",
      }}>
        {s.goal}
      </div>

      <div style={{
        display: "flex", gap: 22, marginTop: 14, flexWrap: "wrap",
        fontFamily: T.fontMono, fontSize: 11, letterSpacing: 0.3, color: C.inkMuted,
      }}>
        <SumStat n={s.stories.inWave.length} label="in wave" dot="#c28b3e" />
        <SumStat n={s.stories.merged.length} label="merged" dot="#3e7a5a" />
        <SumStat n={s.stories.blocked.length} label="blocked" dot={T.gap} />
      </div>

      {/* Gate-health */}
      <div style={{
        marginTop: 22, padding: "14px 16px",
        background: d ? "rgba(255,252,245,0.03)" : T.paper,
        border: `1px solid ${C.rule}`,
      }}>
        <div style={{
          display: "flex", alignItems: "baseline", justifyContent: "space-between",
          marginBottom: 10,
        }}>
          <span style={{
            fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.3,
            color: C.inkQuiet, textTransform: "uppercase",
          }}>quality gates</span>
          <span style={{ fontFamily: T.fontMono, fontSize: 10, color: C.inkFaint, letterSpacing: 0.3 }}>
            pass / of run
          </span>
        </div>
        <GateHealthBar counts={counts} />
      </div>

      {/* Bands */}
      <div style={{ marginTop: 24 }}>
        <Band label="in wave" count={s.stories.inWave.length} tweaks={tweaks}>
          {s.stories.inWave.map(st => <StoryRow key={st.key} story={st} tweaks={tweaks} />)}
        </Band>
        <Band label="merged" count={s.stories.merged.length} terminal tweaks={tweaks}>
          {s.stories.merged.map(st => <StoryRow key={st.key} story={st} terminal tweaks={tweaks} />)}
        </Band>
        <Band label="blocked" count={s.stories.blocked.length} attention tweaks={tweaks}>
          {s.stories.blocked.map(st => <BlockedRow key={st.key} story={st} tweaks={tweaks} />)}
        </Band>
      </div>

      {/* Advances ↗ features */}
      <div style={{
        marginTop: 20, paddingTop: 18, borderTop: `1px solid ${C.rule}`,
      }}>
        <div style={{
          display: "flex", alignItems: "baseline", justifyContent: "space-between",
          marginBottom: 10,
        }}>
          <span style={{
            fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.3,
            color: T.accent, textTransform: "uppercase",
          }}>advances ↗ features</span>
          <span style={{ fontFamily: T.fontMono, fontSize: 10, color: C.inkFaint, letterSpacing: 0.3 }}>
            jumps to features
          </span>
        </div>
        {SPRINT_ADVANCES.map(a => (
          <div key={a.key}
            onClick={() => onOpenFeature && onOpenFeature(a.key)}
            style={{
              display: "grid", gridTemplateColumns: "1fr auto auto",
              alignItems: "center", gap: 10,
              padding: "10px 0", borderBottom: `1px solid ${C.rule}`,
              cursor: "pointer",
            }}>
            <span style={{
              fontFamily: T.fontSans, fontSize: 13, color: C.ink, fontWeight: 500,
              overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
            }}>
              {a.name}
            </span>
            <span style={{
              fontFamily: T.fontMono, fontSize: 10, color: C.inkMuted, letterSpacing: 0.3,
            }}>{a.touching} {a.touching === 1 ? "story" : "stories"}</span>
            <span style={{ fontFamily: T.fontMono, fontSize: 11, color: T.accent }}>↗</span>
          </div>
        ))}
      </div>

      {/* Recent */}
      <div style={{ marginTop: 24 }}>
        <div style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.3,
          color: C.inkQuiet, textTransform: "uppercase", marginBottom: 10,
        }}>
          recent · last 3
        </div>
        <div style={{ border: `1px solid ${C.rule}` }}>
          {RECENT_SPRINTS.map((r, i) => (
            <div key={r.key} style={{
              background: d ? "rgba(255,252,245,0.02)" : T.paper,
              padding: "12px 14px", opacity: 0.78,
              borderBottom: i < RECENT_SPRINTS.length - 1 ? `1px solid ${C.rule}` : "none",
              display: "grid", gridTemplateColumns: "1fr auto", gap: 10,
              cursor: "pointer",
            }}>
              <div>
                <div style={{
                  fontFamily: T.fontMono, fontSize: 11, fontWeight: 500,
                  color: C.ink, letterSpacing: 0.3,
                }}>{r.key}</div>
                <div style={{
                  fontFamily: T.fontSans, fontSize: 12, color: C.inkMuted,
                  marginTop: 2, lineHeight: 1.4,
                  overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
                }}>{r.goal}</div>
              </div>
              <div style={{
                fontFamily: T.fontMono, fontSize: 10, color: C.inkQuiet,
                letterSpacing: 0.3, textAlign: "right", lineHeight: 1.5,
              }}>
                <div>{r.merged} merged</div>
                <div style={{ color: r.gateHealth === "clean" ? C.inkMuted : T.gap }}>{r.gateHealth}</div>
                <div style={{ color: C.inkFaint }}>{r.findings} findings</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Band({ label, count, children, terminal, attention, tweaks }) {
  const C = lensColors(tweaks.dark);
  return (
    <div style={{ marginBottom: 18 }}>
      <div style={{
        display: "flex", alignItems: "baseline", gap: 10,
        marginBottom: 6, paddingBottom: 6, borderBottom: `1px solid ${C.rule}`,
      }}>
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.3,
          color: attention ? T.gap : (terminal ? C.inkQuiet : T.accent),
          textTransform: "uppercase",
        }}>{label}</span>
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, color: C.inkFaint, letterSpacing: 0.3,
        }}>{count}</span>
      </div>
      {children}
    </div>
  );
}

function StoryRow({ story, terminal, tweaks }) {
  const C = lensColors(tweaks.dark);
  return (
    <div style={{
      padding: "9px 0", borderBottom: `1px solid ${C.rule}`,
      opacity: terminal ? 0.64 : 1, cursor: "pointer",
    }}>
      <div style={{
        display: "grid", gridTemplateColumns: "auto 1fr auto", alignItems: "center", gap: 10,
      }}>
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 0.3,
          color: C.inkFaint, width: 32,
        }}>{story.wave ? `w${story.wave}` : "—"}</span>
        <span style={{
          fontFamily: T.fontSans, fontSize: 13, color: C.ink, lineHeight: 1.35,
          overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
        }}>{story.title}</span>
        <GateTrio gates={story.gates} compact />
      </div>
    </div>
  );
}

function BlockedRow({ story, tweaks }) {
  const C = lensColors(tweaks.dark);
  return (
    <div style={{ padding: "10px 0", borderBottom: `1px solid ${C.rule}` }}>
      <div style={{
        display: "grid", gridTemplateColumns: "auto 1fr auto", alignItems: "center", gap: 10,
      }}>
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 0.3, color: T.gap, width: 32,
        }}>blk</span>
        <span style={{
          fontFamily: T.fontSans, fontSize: 13, color: C.ink,
          overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
        }}>{story.title}</span>
        <GapFlag />
      </div>
      <div style={{
        marginTop: 6, marginLeft: 42,
        fontFamily: T.fontSans, fontSize: 12, color: C.inkMuted, lineHeight: 1.5,
        maxWidth: "56ch",
      }}>
        {story.reason}
      </div>
    </div>
  );
}

function SumStat({ n, label, dot }) {
  return (
    <span style={{ display: "inline-flex", alignItems: "baseline", gap: 6 }}>
      {dot && <span style={{ width: 6, height: 6, borderRadius: "50%", background: dot }} />}
      <span style={{ fontWeight: 500 }}>{n}</span>
      <span>{label}</span>
    </span>
  );
}

function gateCounts(sprint) {
  const all = [...sprint.stories.inWave, ...sprint.stories.merged];
  const init = () => ({ pass: 0, fail: 0, pending: 0 });
  const out = { avfl: init(), cr: init(), e2e: init() };
  for (const s of all) for (const g of ["avfl", "cr", "e2e"]) {
    const v = s.gates[g];
    if (v === "pass") out[g].pass++;
    else if (v === "fail") out[g].fail++;
    else out[g].pending++;
  }
  return out;
}

// ─── FLYWHEEL LENS · Timeline ─────────────────────────────────────────────
function FlywheelLens({ tweaks, onOpenSprint }) {
  const d = tweaks.dark;
  const C = lensColors(d);
  const sprints = [...TIMELINE_SPRINTS].reverse();
  const bySprint = Object.fromEntries(sprints.map(s => [s.key, []]));
  for (const f of FINDINGS) if (bySprint[f.sprint]) bySprint[f.sprint].push(f);

  return (
    <section data-lens-id="flywheel" style={{
      padding: "40px 24px 72px",
      background: d ? T.paperDark : T.paper,
      color: C.ink, fontFamily: T.fontSans,
      borderTop: `1px solid ${C.rule}`,
    }}>
      <Header n="03" label="Flywheel" tweaks={tweaks} />

      <div style={{
        fontFamily: T.fontSerif, fontSize: 22, letterSpacing: -0.25, fontWeight: 400,
        lineHeight: 1.25, marginTop: 8,
      }}>
        How the practice moved forward.
      </div>
      <div style={{
        fontFamily: T.fontSerif, fontSize: 14.5, lineHeight: 1.6,
        color: C.inkMuted, marginTop: 8, maxWidth: "60ch",
      }}>
        Retro findings attach to the sprint that produced them. Each carries the story
        it generated and the skill or rule it distilled into. Newest first.
      </div>

      <div style={{
        display: "flex", gap: 18, marginTop: 14,
        fontFamily: T.fontMono, fontSize: 11, letterSpacing: 0.3, color: C.inkMuted,
      }}>
        <span>{FINDINGS.length} findings</span>
        <span>·</span>
        <span>{SKILLS.length} distilled</span>
      </div>

      <div style={{ marginTop: 24 }}>
        {sprints.map((sp, i) => (
          <SprintSpineBlock
            key={sp.key} sprint={sp} findings={bySprint[sp.key]}
            tweaks={tweaks}
            isFirst={i === 0} isLast={i === sprints.length - 1}
            onOpenSprint={onOpenSprint}
          />
        ))}
      </div>
    </section>
  );
}

function SprintSpineBlock({ sprint, findings, isFirst, isLast, tweaks, onOpenSprint }) {
  const C = lensColors(tweaks.dark);
  return (
    <div style={{ display: "grid", gridTemplateColumns: "72px 1fr", columnGap: 14 }}>
      {/* Spine */}
      <div style={{ position: "relative", paddingTop: 18 }}>
        <div style={{
          position: "absolute", left: 10,
          top: isFirst ? 28 : 0, bottom: isLast ? 30 : 0,
          width: 1, background: C.ruleStrong,
        }} />
        <div style={{
          position: "absolute", left: 4, top: 24,
          width: 13, height: 13, borderRadius: "50%",
          background: sprint.active ? T.accent : (tweaks.dark ? T.paperDark : T.paper),
          border: `2px solid ${sprint.active ? T.accent : C.ruleStrong}`,
        }} />
        <div style={{ paddingLeft: 24, paddingTop: 16, cursor: "pointer" }}
             onClick={() => onOpenSprint && onOpenSprint(sprint.key)}>
          <div style={{
            fontFamily: T.fontMono, fontSize: 10,
            color: sprint.active ? T.accent : C.inkMuted, fontWeight: 500, letterSpacing: 0.3,
          }}>{sprint.label}</div>
          <div style={{
            fontFamily: T.fontMono, fontSize: 9, color: C.inkFaint, letterSpacing: 0.3,
            marginTop: 2, lineHeight: 1.3,
          }}>{sprint.dates}</div>
        </div>
      </div>

      <div style={{ paddingTop: 18, paddingBottom: 16 }}>
        {findings.length === 0 && (
          <div style={{
            padding: "16px 0 4px", fontFamily: T.fontSans, fontSize: 12, color: C.inkFaint,
          }}>no findings yet.</div>
        )}
        {findings.map(f => <FindingCard key={f.key} finding={f} tweaks={tweaks} />)}
      </div>
    </div>
  );
}

function FindingCard({ finding, tweaks }) {
  const C = lensColors(tweaks.dark);
  const d = tweaks.dark;
  const story = GENERATED_STORIES[finding.producedStory];
  const skill = SKILLS.find(s => s.key === finding.distilledSkill);
  const severityColor = finding.severity === "recurring" ? T.gap : C.inkQuiet;
  const leftAccent = finding.severity === "recurring" ? T.gap : T.accentRule;

  return (
    <div style={{
      marginBottom: 16, padding: "12px 14px",
      background: d ? "rgba(255,252,245,0.03)" : T.paper,
      border: `1px solid ${C.rule}`,
      borderLeft: `3px solid ${leftAccent}`,
    }}>
      <div style={{
        display: "flex", alignItems: "baseline", justifyContent: "space-between",
        gap: 8, marginBottom: 6,
      }}>
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.3,
          color: C.inkQuiet, textTransform: "uppercase",
        }}>finding</span>
        <span style={{
          fontFamily: T.fontMono, fontSize: 9.5, color: severityColor, letterSpacing: 0.3,
        }}>{finding.severity} · {finding.when}</span>
      </div>
      <div style={{
        fontFamily: T.fontSerif, fontSize: 15, fontWeight: 500,
        color: C.ink, lineHeight: 1.35, marginBottom: 6,
      }}>{finding.label}</div>
      <div style={{
        fontFamily: T.fontSerif, fontSize: 13, lineHeight: 1.55,
        color: C.inkMuted, marginBottom: 10,
      }}>{finding.note}</div>
      <div style={{ display: "grid", rowGap: 3 }}>
        {story && <ChainLink type="story" label={story.title} meta={story.status} tweaks={tweaks} />}
        {skill && <ChainLink type="skill" label={skill.name} meta={skill.kind} tweaks={tweaks} />}
      </div>
    </div>
  );
}

function ChainLink({ type, label, meta, tweaks }) {
  const C = lensColors(tweaks.dark);
  return (
    <div style={{
      display: "grid", gridTemplateColumns: "14px 48px 1fr auto",
      alignItems: "baseline", columnGap: 8, padding: "3px 0", cursor: "pointer",
    }}>
      <span style={{ fontFamily: T.fontMono, fontSize: 10, color: C.inkFaint }}>↳</span>
      <span style={{
        fontFamily: T.fontMono, fontSize: 10, letterSpacing: 0.4,
        color: type === "skill" ? T.accent : C.inkQuiet, textTransform: "uppercase",
      }}>{type}</span>
      <span style={{
        fontFamily: T.fontSans, fontSize: 12.5, color: C.ink, lineHeight: 1.4,
        overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
      }}>{label}</span>
      <span style={{
        fontFamily: T.fontMono, fontSize: 10, color: C.inkFaint, letterSpacing: 0.3,
      }}>{meta}</span>
    </div>
  );
}

// ─── shared helpers ───────────────────────────────────────────────────────
function Header({ n, label, tweaks }) {
  const c = tweaks.dark ? "rgba(240,238,233,0.48)" : "rgba(40,30,20,0.45)";
  const rule = tweaks.dark ? T.ruleDark : T.rule;
  return (
    <div style={{ display: "flex", alignItems: "baseline", gap: 12 }}>
      <span style={{
        fontFamily: T.fontMono, fontSize: 11, letterSpacing: 1.4,
        color: c, textTransform: "uppercase",
      }}>{n} · {label}</span>
      <span style={{ flex: 1, height: 1, background: rule }} />
    </div>
  );
}

function lensColors(dark) {
  return dark ? {
    ink: T.inkOnDark,
    inkMuted: T.inkOnDarkMuted,
    inkQuiet: T.inkOnDarkQuiet,
    inkFaint: "rgba(240,238,233,0.36)",
    rule: T.ruleDark,
    ruleStrong: T.ruleDarkStrong,
  } : {
    ink: T.ink, inkMuted: T.inkMuted, inkQuiet: T.inkQuiet, inkFaint: T.inkFaint,
    rule: T.rule, ruleStrong: T.ruleStrong,
  };
}

Object.assign(window, { SprintsLens, FlywheelLens });
