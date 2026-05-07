import { useCallback, useEffect, useMemo, useRef, useState } from "react";

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
  {
    label: "Root → executive voice",
    text: "Ask the root agent to transfer_to_agent to executive_voice and give a tight 4-bullet summary of Drake's ADK + production ML positioning using portfolio tools for facts only.",
  },
];

type ChatMsg = { role: "user" | "assistant"; text: string };

type TraceKind = "call" | "transfer" | "result" | "text" | "meta" | "error";

type TraceItem = {
  id: string;
  author?: string;
  kind: TraceKind;
  title: string;
  body?: string;
};

function runStatsFromTrace(items: TraceItem[]) {
  const authors = new Set<string>();
  for (const t of items) {
    if (t.author) authors.add(t.author);
  }
  const toolCalls = items.filter((t) => t.kind === "call").length;
  const handoffs = items.filter((t) => t.kind === "transfer").length;
  const toolResults = items.filter((t) => t.kind === "result").length;
  const modelChunks = items.filter((t) => t.kind === "text").length;
  return {
    steps: items.length,
    toolCalls,
    handoffs,
    toolResults,
    modelChunks,
    agents: [...authors].sort(),
  };
}

/** FastAPI often returns `{ "detail": "..." }` or a list of validation errors; plain 500s may be empty. */
async function readAdkHttpError(res: Response): Promise<string> {
  const raw = (await res.text()).trim();
  if (!raw) {
    return `${res.status} ${res.statusText || "Error"}`.trim();
  }
  try {
    const j = JSON.parse(raw) as { detail?: unknown };
    if (typeof j.detail === "string") {
      return j.detail;
    }
    if (Array.isArray(j.detail)) {
      return j.detail
        .map((item) => {
          if (item && typeof item === "object" && "msg" in item) {
            return String((item as { msg: unknown }).msg);
          }
          return JSON.stringify(item);
        })
        .join("; ");
    }
    if (j.detail != null) {
      return String(j.detail);
    }
  } catch {
    /* not JSON */
  }
  return raw;
}

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
      const isHandoff = name === "transfer_to_agent" || name === "transferToAgent";
      out.push({
        id: `${id}-call-${name}-${out.length}`,
        author,
        kind: isHandoff ? "transfer" : "call",
        title: isHandoff ? `Agent handoff: ${name}` : `Tool call: ${name}`,
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

/** Minimal inline **bold** and `code` — no HTML from model is interpreted as tags. */
function FormattedMessage({ text }: { text: string }) {
  const lines = text.split("\n");
  return (
    <>
      {lines.map((line, li) => (
        <span key={li}>
          {formatLine(line)}
          {li < lines.length - 1 ? <br /> : null}
        </span>
      ))}
    </>
  );
}

function formatLine(line: string): React.ReactNode {
  const out: React.ReactNode[] = [];
  let remaining = line;
  let k = 0;
  while (remaining.length > 0) {
    const bold = remaining.match(/^\*\*([^*]+)\*\*/);
    const code = remaining.match(/^`([^`]+)`/);
    if (bold) {
      out.push(
        <strong key={k++} style={{ color: "#e0e0e0" }}>
          {bold[1]}
        </strong>
      );
      remaining = remaining.slice(bold[0].length);
    } else if (code) {
      out.push(
        <code key={k++} className="msg-code">
          {code[1]}
        </code>
      );
      remaining = remaining.slice(code[0].length);
    } else {
      const nextIdx = (() => {
        const a = remaining.indexOf("**");
        const b = remaining.indexOf("`");
        const cands = [a, b].filter((n) => n >= 0);
        return cands.length ? Math.min(...cands) : -1;
      })();
      if (nextIdx === -1) {
        out.push(remaining);
        break;
      }
      out.push(remaining.slice(0, nextIdx));
      remaining = remaining.slice(nextIdx);
    }
  }
  return <>{out}</>;
}

function traceKindColor(kind: TraceKind): string {
  switch (kind) {
    case "call":
      return "#ffcc80";
    case "transfer":
      return "#ce93d8";
    case "result":
      return "#a5d6a7";
    case "text":
      return "#90caf9";
    case "error":
      return "#ef9a9a";
    default:
      return "#b0bec5";
  }
}

export default function App() {
  const [sessionId, setSessionId] = useState(() => crypto.randomUUID().slice(0, 12));
  const [apiOk, setApiOk] = useState<boolean | null>(null);
  const [messages, setMessages] = useState<ChatMsg[]>([
    {
      role: "assistant",
      text: "This UI drives **`POST /run`** through the Vite proxy (full turn, all events). The **Trace** panel **replays** tool calls, **`transfer_to_agent`** handoffs, and model text. Start **`adk api_server --port 8000`** from the repo root: use **Gemini** (`GOOGLE_API_KEY` in `.env`) or **local Ollama** (no Google key — see README).",
    },
  ]);
  const [input, setInput] = useState("");
  const [trace, setTrace] = useState<TraceItem[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stepLabel, setStepLabel] = useState("");
  const [lastRunMs, setLastRunMs] = useState<number | null>(null);

  const chatEndRef = useRef<HTMLDivElement>(null);
  const traceEndRef = useRef<HTMLDivElement>(null);

  const stats = useMemo(() => runStatsFromTrace(trace), [trace]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, busy]);

  useEffect(() => {
    traceEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [trace]);

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
    throw new Error(await readAdkHttpError(r));
  }, []);

  const sendMessage = useCallback(
    async (text: string) => {
      const trimmed = text.trim();
      if (!trimmed || busy) return;
      const t0 = performance.now();
      setError(null);
      setStepLabel("");
      setBusy(true);
      setLastRunMs(null);
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

        setStepLabel("Running agent (LLM + tools)…");
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
          const detail = await readAdkHttpError(res);
          throw new Error(
            res.status === 500 && detail === "Internal Server Error"
              ? `${detail} — check the **adk api_server** terminal for the traceback (Gemini key/quota, or **Ollama** not running / model not pulled).`
              : detail
          );
        }

        const raw = await res.json();
        if (!Array.isArray(raw)) {
          throw new Error(`Expected event array from /run, got: ${JSON.stringify(raw).slice(0, 200)}`);
        }

        const events = raw as Record<string, unknown>[];
        if (events.length === 0) {
          throw new Error(
            "Agent returned no events — check LLM backend (GOOGLE_API_KEY for Gemini, or ollama serve + pulled model for local)."
          );
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
                text: textSoFar || `Working… (${i + 1}/${events.length} ADK events)`,
              };
            }
            return copy;
          });
          setStepLabel(`Trace: ADK event ${i + 1} / ${events.length}`);
          await delay(Math.min(120, 40 + i * 8));
        }

        setLastRunMs(Math.round(performance.now() - t0));

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
              text: `**Error:** ${msg}\n\n— Is \`adk api_server --port 8000\` running from the **repo root** (folder that contains \`drake_talley_adk/\`)?\n— **Ollama:** \`ollama serve\` + \`ollama pull llama3.2\`; remove fake \`GOOGLE_API_KEY\` lines from \`.env\` (placeholders like YOUR_... are ignored — pull latest code).\n— **Gemini:** real long \`GOOGLE_API_KEY\` only.\n— Open via \`npm run dev\` (5173). Read the **api_server** traceback if this is still vague.`,
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
    <div className="portfolio-shell">
      <div className="portfolio-chat">
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
            {lastRunMs != null && !busy ? (
              <span style={{ color: "#78909c", marginLeft: 8 }}>· last run {lastRunMs} ms</span>
            ) : null}
          </div>
        </header>

        <div style={{ padding: "10px 14px", display: "flex", flexWrap: "wrap", gap: 8 }}>
          {PRESETS.map((p) => (
            <button key={p.label} type="button" disabled={busy} className="preset-btn" onClick={() => sendMessage(p.text)}>
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
            minHeight: 0,
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
              {msg.text ? (
                <FormattedMessage text={msg.text} />
              ) : msg.role === "assistant" && busy ? (
                <span style={{ color: "#78909c" }}>Running…</span>
              ) : null}
            </div>
          ))}
          <div ref={chatEndRef} />
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
              placeholder="Message drake_talley_adk…"
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

      <div className="portfolio-trace">
        <div
          style={{
            padding: "12px 14px",
            borderBottom: "1px solid #263238",
            fontWeight: 600,
            fontSize: "0.9rem",
          }}
        >
          Trace · tools, handoffs & agents
        </div>
        <div style={{ fontSize: "0.72rem", padding: "8px 14px", color: "#78909c" }}>
          <strong style={{ color: "#90a4ae" }}>[transfer]</strong> rows are{" "}
          <code className="msg-code">transfer_to_agent</code> — LLM-chosen delegation. Tool calls and results are
          grounded data from this repo.
        </div>
        {trace.length > 0 ? (
          <div className="trace-stats">
            <span className="trace-stat-pill">
              trace steps <strong>{stats.steps}</strong>
            </span>
            <span className="trace-stat-pill">
              tool calls <strong>{stats.toolCalls}</strong>
            </span>
            <span className="trace-stat-pill">
              handoffs <strong>{stats.handoffs}</strong>
            </span>
            <span className="trace-stat-pill">
              agents <strong>{stats.agents.length}</strong>
            </span>
            {stats.agents.length > 0 ? (
              <span className="trace-stat-pill" title={stats.agents.join(", ")}>
                <span style={{ maxWidth: 220, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                  {stats.agents.join(" · ")}
                </span>
              </span>
            ) : null}
          </div>
        ) : null}
        <div style={{ flex: 1, overflowY: "auto", padding: "0 10px 16px", minHeight: 0 }}>
          {trace.length === 0 ? (
            <div style={{ color: "#546e7a", padding: 12, fontSize: "0.85rem" }}>
              Run a preset — watch tool calls and agent handoffs replay step by step (synthetic CRM / AML data +
              local or cloud LLM).
            </div>
          ) : (
            trace.map((t, idx) => (
              <details
                key={`${t.id}-${idx}`}
                open={t.kind === "call" || t.kind === "transfer" || t.kind === "result" || t.kind === "error"}
                className="trace-row"
                style={{ borderLeft: t.kind === "transfer" ? "3px solid #ce93d8" : undefined }}
              >
                <summary
                  style={{
                    cursor: "pointer",
                    padding: "8px 10px",
                    fontSize: "0.78rem",
                    listStyle: "none",
                    display: "flex",
                    alignItems: "center",
                    flexWrap: "wrap",
                    gap: 4,
                  }}
                >
                  <span className="trace-row-index">{idx + 1}</span>
                  <span style={{ color: traceKindColor(t.kind), fontWeight: 700 }}>[{t.kind}]</span>
                  <span>{t.title}</span>
                  {t.author ? (
                    <span style={{ color: "#78909c", marginLeft: "auto" }}>@ {t.author}</span>
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
          <div ref={traceEndRef} />
        </div>
      </div>
    </div>
  );
}
