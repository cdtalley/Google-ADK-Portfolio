import { useCallback, useRef, useState } from "react";

const APP_NAME = "drake_talley_adk";
const USER_ID = "recruiter_ui";

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
  kind: "call" | "result" | "text" | "meta";
  title: string;
  body?: string;
};

function summarizeEvent(ev: Record<string, unknown>): TraceItem[] {
  const id = String(ev.id ?? crypto.randomUUID());
  const author = typeof ev.author === "string" ? ev.author : undefined;
  const content = ev.content as Record<string, unknown> | undefined;
  const parts = (content?.parts as unknown[]) ?? [];
  const out: TraceItem[] = [];

  for (const p of parts) {
    const part = p as Record<string, unknown>;
    if (part.functionCall) {
      const fc = part.functionCall as Record<string, unknown>;
      const name = String(fc.name ?? "?");
      const args = fc.args;
      out.push({
        id: `${id}-call-${name}`,
        author,
        kind: "call",
        title: `Tool call: ${name}`,
        body: JSON.stringify(args, null, 2),
      });
    }
    if (part.functionResponse) {
      const fr = part.functionResponse as Record<string, unknown>;
      const name = String(fr.name ?? "?");
      const response = fr.response;
      out.push({
        id: `${id}-res-${name}`,
        author,
        kind: "result",
        title: `Result: ${name}`,
        body:
          typeof response === "object"
            ? JSON.stringify(response, null, 2)
            : String(response ?? ""),
      });
    }
    if (part.text != null) {
      const t = String(part.text);
      if (t.trim()) {
        out.push({
          id: `${id}-txt`,
          author,
          kind: "text",
          title: "Model text",
          body: t.length > 2000 ? `${t.slice(0, 2000)}…` : t,
        });
      }
    }
  }

  if (out.length === 0) {
    out.push({
      id,
      author,
      kind: "meta",
      title: "Event",
      body: JSON.stringify(ev, null, 2).slice(0, 4000),
    });
  }

  return out;
}

async function parseSseStream(
  reader: ReadableStreamDefaultReader<Uint8Array>,
  onEvent: (obj: Record<string, unknown>) => void
): Promise<void> {
  const dec = new TextDecoder();
  let buf = "";
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += dec.decode(value, { stream: true });
    buf = buf.replace(/\r\n/g, "\n");
    let idx: number;
    while ((idx = buf.indexOf("\n\n")) >= 0) {
      const chunk = buf.slice(0, idx);
      buf = buf.slice(idx + 2);
      for (const line of chunk.split("\n")) {
        const t = line.trim();
        if (t.startsWith("data:")) {
          const json = t.slice(5).trim();
          if (json && json !== "[DONE]") {
            try {
              onEvent(JSON.parse(json) as Record<string, unknown>);
            } catch {
              /* ignore */
            }
          }
        }
      }
    }
  }
}

const shell: React.CSSProperties = {
  display: "grid",
  gridTemplateColumns: "1fr 380px",
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
  const [messages, setMessages] = useState<ChatMsg[]>([
    {
      role: "assistant",
      text: "Select a **preset** (Meridian AML, RevOps, …). **Live:** watch the **Trace** panel stream each **tool call** and **agent** (`author`) as Gemini runs—multi-agent work, not a canned script. Requires **`adk api_server --port 8000`** and this UI via **`npm run dev`** on port **5173** (proxy fixes ADK origin checks).",
    },
  ]);
  const [input, setInput] = useState("");
  const [trace, setTrace] = useState<TraceItem[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const assistantBuf = useRef("");

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
      setBusy(true);
      setMessages((m) => [...m, { role: "user", text: trimmed }]);
      assistantBuf.current = "";
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

        const res = await fetch("/run_sse", {
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
            streaming: true,
          }),
        });

        if (!res.ok) {
          const t = await res.text();
          throw new Error(t || `API ${res.status}`);
        }

        const reader = res.body?.getReader();
        if (!reader) throw new Error("No response body");

        await parseSseStream(reader, (ev) => {
          const items = summarizeEvent(ev);
          setTrace((prev) => [...prev, ...items]);
          for (const it of items) {
            if (it.kind === "text" && it.body) {
              assistantBuf.current += it.body;
            }
          }
          const acc = assistantBuf.current;
          setMessages((m) => {
            const copy = [...m];
            const last = copy.length - 1;
            if (last >= 0 && copy[last].role === "assistant") {
              copy[last] = { role: "assistant", text: acc || "…" };
            }
            return copy;
          });
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
              text: `**Error:** ${msg}\n\nStart API server from repo root: \`adk api_server --port 8000\``,
            };
          }
          return copy;
        });
      } finally {
        setBusy(false);
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
            {busy ? (
              <span style={{ color: "#4dd0e1" }}>Running agent — trace updating…</span>
            ) : (
              <>
                Live SSE · session <code style={{ color: "#80cbc4" }}>{sessionId}</code>
              </>
            )}
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
                padding: "6px 10px",
                borderRadius: 6,
                border: "1px solid #37474f",
                background: "#1c2832",
                color: "#b0bec5",
                cursor: busy ? "wait" : "pointer",
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
              }}
            >
              {msg.text || (msg.role === "assistant" && busy ? "…" : "")}
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
              onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && (e.preventDefault(), sendMessage(input))}
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
          Trace · real-time tools & agents
        </div>
        <div style={{ fontSize: "0.72rem", padding: "8px 14px", color: "#78909c" }}>
          <strong>Agents:</strong> drake_talley_portfolio → technical_proof | executive_voice |
          revops_lead_orchestrator | aml_alert_orchestrator (+ specialists)
        </div>
        <div style={{ flex: 1, overflowY: "auto", padding: "0 10px 16px" }}>
          {trace.length === 0 ? (
            <div style={{ color: "#546e7a", padding: 12, fontSize: "0.85rem" }}>
              Run a preset to see **functionCall** / **functionResponse** and **author** stream here.
            </div>
          ) : (
            trace.map((t, idx) => (
              <details
                key={`${t.id}-${idx}`}
                open={t.kind === "call" || t.kind === "result"}
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
