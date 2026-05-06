import { useCallback, useEffect, useState } from "react";

const APP_NAME = "drake_talley_adk";
const USER_ID = "portfolio_ui";

const PRESETS: { label: string; text: string }[] = [
  {
    label: "Meridian AML — ALT-20001",
    text: "Using aml_alert_orchestrator: triage alert ALT-20001 — regulatory triggers, severity tier, and recommended disposition. State clearly that Meridian and data are synthetic.",
  },
  {
    label: "RevOps — LD-10043",
    text: "Using revops_lead_orchestrator: triage lead LD-10043 for policy, priority score, and next-best action. Note demo CRM data.",
  },
  {
    label: "Résumé — SentriLock",
    text: "Call get_verified_track_record and summarize three quantified SentriLock outcomes (field failure, downtime, cloud). Do not invent metrics.",
  },
  {
    label: "Case study — fintech",
    text: "List case study slugs, then get_case_study_by_slug for fintech-compliance-analyst. Summarize ADK patterns; label synthetic.",
  },
  {
    label: "ADK architecture",
    text: "Transfer to technical_proof: explain how this repo uses sub_agents, transfer_to_agent, and partitioned tools—cite file names.",
  },
];

type ChatMsg = { role: "user" | "assistant"; text: string };

type TraceItem = {
  id: string;
  author?: string;
  kind: "call" | "result" | "text" | "meta" | "error";
  title: string;
  body?: string;
};

/** ADK serializes with camelCase; tolerate snake_case from older payloads. */
function getPartField(part: Record<string, unknown>, camel: string, snake: string): unknown {
  if (part[camel] != null) return part[camel];
  return part[snake];
}

function summarizeEvent(ev: Record<string, unknown>): TraceItem[] {
  if (ev.error != null) {
    return [
      {
        id: String(ev.id ?? crypto.randomUUID()),
        kind: "error",
        title: "Stream error",
        body: String(ev.error),
      },
    ];
  }

  const id = String(ev.id ?? crypto.randomUUID());
  const author = typeof ev.author === "string" ? ev.author : undefined;
  const content = ev.content as Record<string, unknown> | undefined;
  const parts = (content?.parts as unknown[]) ?? [];
  const out: TraceItem[] = [];

  for (const p of parts) {
    const part = p as Record<string, unknown>;
    const fc = getPartField(part, "functionCall", "function_call") as Record<string, unknown> | undefined;
    if (fc && typeof fc === "object") {
      const name = String(fc.name ?? "?");
      const args = fc.args;
      out.push({
        id: `${id}-call-${name}-${out.length}`,
        author,
        kind: "call",
        title: `Tool call: ${name}`,
        body: JSON.stringify(args ?? {}, null, 2),
      });
    }
    const fr = getPartField(part, "functionResponse", "function_response") as Record<string, unknown> | undefined;
    if (fr && typeof fr === "object") {
      const name = String(fr.name ?? "?");
      const response = fr.response;
      out.push({
        id: `${id}-res-${name}-${out.length}`,
        author,
        kind: "result",
        title: `Result: ${name}`,
        body:
          typeof response === "object" && response !== null
            ? JSON.stringify(response, null, 2)
            : String(response ?? ""),
      });
    }
    if (part.text != null) {
      const t = String(part.text);
      if (t.trim()) {
        out.push({
          id: `${id}-txt-${out.length}`,
          author,
          kind: "text",
          title: "Model text",
          body: t,
        });
      }
    }
  }

  if (out.length === 0) {
    out.push({
      id,
      author,
      kind: "meta",
      title: "Event (raw)",
      body: JSON.stringify(ev, null, 2).slice(0, 6000),
    });
  }

  return out;
}

function collectAssistantText(items: TraceItem[]): string {
  return items
    .filter((i) => i.kind === "text" && i.body)
    .map((i) => i.body!)
    .join("");
}

const delay = (ms: number) => new Promise((r) => setTimeout(r, ms));

const shell: React.CSSProperties = {
  display: "grid",
  gridTemplateColumns: "1fr min(420px, 38vw)",
  gap: 0,
  minHeight: "100vh",
};

const panel: React.CSSProperties = {
  borderRight: "1px solid #263238",
  display: "flex",
  flexDirection: "column",
  background: "#121a21",
};

const tracePanel: React.CSSProperties = {
  background: "#0d1117",
  display: "flex",
  flexDirection: "column",
  overflow: "hidden",
};

export default function App() {
  const [sessionId, setSessionId] = useState(() => crypto.randomUUID().slice(0, 12));
  const [apiOk, setApiOk] = useState<boolean | null>(null);
  const [messages, setMessages] = useState<ChatMsg[]>([
    {
      role: "assistant",
      text: "This UI calls ADK **`/run`** (full agent turn) through the Vite proxy—**reliable** with Gemini + tools + sub-agents. After you send, watch the **Trace** panel **replay** each tool step. Start **`adk api_server --port 8000`** from the repo root and keep **`GOOGLE_API_KEY`** set.",
    },
  ]);
  const [input, setInput] = useState("");
  const [trace, setTrace] = useState<TraceItem[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stepLabel, setStepLabel] = useState("");

  useEffect(() => {
    let cancelled = false;
    fetch("/list-apps")
      .then((r) => {
        if (!cancelled) setApiOk(r.ok);
      })
      .catch(() => {
        if (!cancelled) setApiOk(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const createSession = useCallback(async (sid: string) => {
    const r = await fetch(`/apps/${APP_NAME}/users/${USER_ID}/sessions/${sid}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: "{}",
    });
    if (r.ok) return true;
    if (r.status === 409 || r.status === 400) return false;
    const t = await r.text();
    throw new Error(t || `HTTP ${r.status}`);
  }, []);

  const sendMessage = useCallback(
    async (text: string) => {
      const trimmed = text.trim();
      if (!trimmed || busy) return;
      setError(null);
      setStepLabel("");
      setBusy(true);
      setMessages((m) => [...m, { role: "user", text: trimmed }]);
      setMessages((m) => [...m, { role: "assistant", text: "" }]);

      let sid = sessionId;
      try {
        let ok = await createSession(sid);
        if (!ok) {
          sid = crypto.randomUUID().slice(0, 12);
          setSessionId(sid);
          ok = await createSession(sid);
          if (!ok) throw new Error("Could not create ADK session");
        }

        setStepLabel("Running agent (Gemini + tools)…");
        const res = await fetch("/run", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            appName: APP_NAME,
            userId: USER_ID,
            sessionId: sid,
            newMessage: {
              role: "user",
              parts: [{ text: trimmed }],
            },
          }),
        });

        if (!res.ok) {
          const t = await res.text();
          throw new Error(t || `API ${res.status}`);
        }

        const raw = await res.json();
        if (!Array.isArray(raw)) {
          throw new Error(`Expected event array from /run, got: ${JSON.stringify(raw).slice(0, 200)}`);
        }

        const events = raw as Record<string, unknown>[];
        if (events.length === 0) {
          throw new Error("Agent returned no events — check GOOGLE_API_KEY and model access.");
        }

        setTrace([]);
        let accumulated: TraceItem[] = [];
        let textSoFar = "";

        for (let i = 0; i < events.length; i++) {
          const ev = events[i];
          const items = summarizeEvent(ev);
          accumulated = [...accumulated, ...items];
          setTrace(accumulated);
          textSoFar = collectAssistantText(accumulated);
          setMessages((m) => {
            const copy = [...m];
            const last = copy.length - 1;
            if (last >= 0 && copy[last].role === "assistant") {
              copy[last] = {
                role: "assistant",
                text: textSoFar || `Working… (${i + 1}/${events.length} events)`,
              };
            }
            return copy;
          });
          setStepLabel(`Trace: step ${i + 1} / ${events.length}`);
          await delay(Math.min(120, 40 + i * 8));
        }

        setMessages((m) => {
          const copy = [...m];
          const last = copy.length - 1;
          if (last >= 0 && copy[last].role === "assistant") {
            const finalText = collectAssistantText(accumulated).trim();
            copy[last] = {
              role: "assistant",
              text:
                finalText ||
                "Run finished but no model text was parsed — expand **Event (raw)** rows in Trace to inspect the payload.",
            };
          }
          return copy;
        });
      } catch (e) {
        const msg = e instanceof Error ? e.message : String(e);
        setError(msg);
        setMessages((m) => {
          const copy = [...m];
          const last = copy.length - 1;
          if (last >= 0 && copy[last].role === "assistant") {
            copy[last] = {
              role: "assistant",
              text: `**Error:** ${msg}\n\n— Is \`adk api_server --port 8000\` running from the repo root?\n— Is \`GOOGLE_API_KEY\` set?\n— Open this app only via \`npm run dev\` (port 5173), not a static file.`,
            };
          }
          return copy;
        });
      } finally {
        setBusy(false);
        setStepLabel("");
      }
    },
    [busy, createSession, sessionId]
  );

  return (
    <div style={shell}>
      <div style={panel}>
        <header
          style={{
            padding: "14px 18px",
            borderBottom: "1px solid #263238",
            background: "#0d1318",
          }}
        >
          <div style={{ fontSize: "1.05rem", fontWeight: 600 }}>
            Drake Talley — Google ADK portfolio
          </div>
          <div style={{ fontSize: "0.8rem", color: "#8b9bab", marginTop: 4 }}>
            API{" "}
            {apiOk === null ? (
              <span>checking…</span>
            ) : apiOk ? (
              <span style={{ color: "#81c784" }}>● connected</span>
            ) : (
              <span style={{ color: "#e57373" }}>● offline — start adk api_server :8000</span>
            )}{" "}
            · session <code style={{ color: "#80cbc4" }}>{sessionId}</code>
            {stepLabel ? (
              <span style={{ color: "#4dd0e1", marginLeft: 8 }}>{stepLabel}</span>
            ) : null}
          </div>
        </header>

        <div style={{ padding: "10px 14px", display: "flex", flexWrap: "wrap", gap: 8 }}>
          {PRESETS.map((p) => (
            <button
              key={p.label}
              type="button"
              disabled={busy}
              onClick={() => sendMessage(p.text)}
              style={{
                fontSize: "0.75rem",
                padding: "8px 12px",
                borderRadius: 6,
                border: "1px solid #37474f",
                background: busy ? "#263238" : "#1c2832",
                color: "#eceff1",
                cursor: busy ? "wait" : "pointer",
                fontWeight: 500,
              }}
            >
              {p.label}
            </button>
          ))}
        </div>

        <div
          style={{
            flex: 1,
            overflowY: "auto",
            padding: "16px 18px",
            display: "flex",
            flexDirection: "column",
            gap: 12,
          }}
        >
          {messages.map((msg, i) => (
            <div
              key={i}
              style={{
                alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
                maxWidth: "92%",
                padding: "10px 14px",
                borderRadius: 10,
                background: msg.role === "user" ? "#1a237e" : "#1e272e",
                border: "1px solid #37474f",
                whiteSpace: "pre-wrap",
                fontSize: "0.9rem",
                lineHeight: 1.45,
              }}
            >
              {msg.text ||
                (msg.role === "assistant" && busy ? "…" : "")}
            </div>
          ))}
        </div>

        <div style={{ padding: 12, borderTop: "1px solid #263238", background: "#0d1318" }}>
          {error ? (
            <div style={{ color: "#ef9a9a", fontSize: "0.8rem", marginBottom: 8 }}>{error}</div>
          ) : null}
          <div style={{ display: "flex", gap: 8 }}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) =>
                e.key === "Enter" && !e.shiftKey && (e.preventDefault(), sendMessage(input), setInput(""))
              }
              placeholder="Message drake_talley_portfolio…"
              disabled={busy}
              style={{
                flex: 1,
                padding: "10px 12px",
                borderRadius: 8,
                border: "1px solid #455a64",
                background: "#0f1419",
                color: "#eceff1",
                fontSize: "0.9rem",
              }}
            />
            <button
              type="button"
              disabled={busy}
              onClick={() => {
                sendMessage(input);
                setInput("");
              }}
              style={{
                padding: "10px 18px",
                borderRadius: 8,
                border: "none",
                background: "#00838f",
                color: "#fff",
                fontWeight: 600,
                cursor: busy ? "wait" : "pointer",
              }}
            >
              Send
            </button>
          </div>
        </div>
      </div>

      <div style={tracePanel}>
        <div
          style={{
            padding: "12px 14px",
            borderBottom: "1px solid #263238",
            fontWeight: 600,
            fontSize: "0.9rem",
          }}
        >
          Trace · tools & agents (live replay)
        </div>
        <div style={{ fontSize: "0.72rem", padding: "8px 14px", color: "#78909c" }}>
          Each row is one ADK event: **functionCall** → **functionResponse** → model **text**. Authors show
          which agent acted (e.g. aml_alert_orchestrator).
        </div>
        <div style={{ flex: 1, overflowY: "auto", padding: "0 10px 16px" }}>
          {trace.length === 0 ? (
            <div style={{ color: "#546e7a", padding: 12, fontSize: "0.85rem" }}>
              Run a preset — the trace fills as the agent executes tools (deterministic CRM / AML data + Gemini
              reasoning).
            </div>
          ) : (
            trace.map((t, idx) => (
              <details
                key={`${t.id}-${idx}`}
                open={t.kind === "call" || t.kind === "result" || t.kind === "error"}
                style={{
                  marginBottom: 8,
                  border: "1px solid #263238",
                  borderRadius: 8,
                  background: "#161b22",
                }}
              >
                <summary
                  style={{
                    cursor: "pointer",
                    padding: "8px 10px",
                    fontSize: "0.78rem",
                    listStyle: "none",
                  }}
                >
                  <span
                    style={{
                      color:
                        t.kind === "call"
                          ? "#ffcc80"
                          : t.kind === "result"
                            ? "#a5d6a7"
                            : t.kind === "text"
                              ? "#90caf9"
                              : t.kind === "error"
                                ? "#ef9a9a"
                                : "#b0bec5",
                    }}
                  >
                    [{t.kind}]
                  </span>{" "}
                  {t.title}
                  {t.author ? (
                    <span style={{ color: "#78909c", marginLeft: 8 }}>@ {t.author}</span>
                  ) : null}
                </summary>
                {t.body ? (
                  <pre
                    style={{
                      margin: 0,
                      padding: "0 10px 10px",
                      fontSize: "0.72rem",
                      overflow: "auto",
                      color: "#cfd8dc",
                      whiteSpace: "pre-wrap",
                      maxHeight: 320,
                    }}
                  >
                    {t.body}
                  </pre>
                ) : null}
              </details>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
