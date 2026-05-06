# Architecture — Google ADK portfolio

This document summarizes **structure**, not a live chat. Run **`adk web`** or **`adk api_server`** with package **`drake_talley_adk`** (see [README.md](README.md)). Optional **[`recruiter_demo/`](recruiter_demo/)** is a React UI proxied to ADK **`/run`** and **`/apps`**.

## Agent hierarchies

| Hierarchy | Root / entry | Role |
|-----------|----------------|------|
| **Portfolio** | `drake_talley_portfolio` in [`drake_talley_adk/agent.py`](drake_talley_adk/agent.py) | Concierge: résumé tools, case studies. Sub-agents: `technical_proof`, `executive_voice`. |
| **RevOps** | `revops_lead_orchestrator` in [`drake_talley_adk/revenue_ops_agents.py`](drake_talley_adk/revenue_ops_agents.py) | Synthetic **CRM** lead triage. Sub-agents: policy, scoring, action. |
| **Meridian AML** | `aml_alert_orchestrator` in [`drake_talley_adk/aml_alert_agents.py`](drake_talley_adk/aml_alert_agents.py) | Synthetic **BSA/AML** alert triage (**Meridian Trust & Savings** is fictional). Sub-agents: policy, risk, disposition. |

Same **Google ADK** pattern: coordinator `Agent` with **`sub_agents`** and LLM-driven **`transfer_to_agent`**, **separate tool namespaces** per domain.

## Tool design rules

- **Structured returns:** Tools return `dict` payloads with a **`status`** field so models and tests branch predictably.
- **Sources of truth:** Portfolio → [`portfolio_data.py`](drake_talley_adk/portfolio_data.py) via [`portfolio_tools.py`](drake_talley_adk/portfolio_tools.py). RevOps → [`revenue_ops_data.py`](drake_talley_adk/revenue_ops_data.py) via [`revenue_ops_tools.py`](drake_talley_adk/revenue_ops_tools.py). AML → [`aml_alert_data.py`](drake_talley_adk/aml_alert_data.py) via [`aml_alert_tools.py`](drake_talley_adk/aml_alert_tools.py).
- **No invented domain fields:** Scores and flags use only keys on records; the LLM narrates **tool output**.
- **Synthetic disclosure:** Case studies, RevOps leads, and Meridian alerts are **explicitly demo** data; `verified_track_record` is résumé-backed.

## Specialist tool partitioning

- **RevOps:** [`REVOPS_TOOLS_POLICY`](drake_talley_adk/revenue_ops_tools.py), `REVOPS_TOOLS_SCORING`, `REVOPS_TOOLS_ACTIONS`, `REVOPS_TOOLS_ALL`.
- **AML:** [`AML_TOOLS_POLICY`](drake_talley_adk/aml_alert_tools.py), `AML_TOOLS_SCORING`, `AML_TOOLS_DISPOSITION`, `AML_TOOLS_ALL`.

## Web UI (`recruiter_demo`)

[`recruiter_demo/`](recruiter_demo/) uses **Vite** with **proxy** to `http://127.0.0.1:8000` for ADK **`/run`**, **`/apps/**`, **`/list-apps`**. Chat plus **trace** replay (function calls, responses, `author`). ADK Web remains fine for quick debugging. See [ADK API server](https://google.github.io/adk-docs/runtime/api-server/).

## Production-oriented next steps (not implemented here)

Offline **eval** suites, **tracing** to observability backends, **secrets** via Secret Manager, deploy **Cloud Run** / **Vertex AI Agent Engine** per [ADK docs](https://google.github.io/adk-docs/).
