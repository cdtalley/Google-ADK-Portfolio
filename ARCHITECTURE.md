# Architecture — Google ADK portfolio

This document is for reviewers who want **structure**, not a live chat. The runnable app is `adk web` with package **`drake_talley_adk`** (see [README.md](README.md)).

## Why two agent hierarchies?

| Hierarchy | Root agent | Role |
|-----------|------------|------|
| **Portfolio** | `drake_talley_portfolio` in [`drake_talley_adk/agent.py`](drake_talley_adk/agent.py) | Concierge for hiring narrative, résumé-grounded facts, and synthetic case-study walkthroughs. Sub-agents: `technical_proof`, `executive_voice`. |
| **RevOps** | `revops_lead_orchestrator` in [`drake_talley_adk/revenue_ops_agents.py`](drake_talley_adk/revenue_ops_agents.py) | Operational demo: inbound **lead triage** under SLA and policy. Sub-agents: `revops_policy_guard`, `revops_scoring_analyst`, `revops_action_planner`. |

Same **Google ADK** pattern twice: a coordinator `Agent` with **`sub_agents`** and LLM-driven **`transfer_to_agent`**, but **separate tool namespaces** so portfolio Q&A does not mix with synthetic CRM mutations of state (there are no writes here—only reads).

## Tool design rules

- **Structured returns:** Tools return `dict` payloads with a **`status`** field (`success`, `not_found`, `invalid_theme`, etc.) so the model and tests can branch predictably.
- **Source of truth:** Portfolio facts and metrics come from [`drake_talley_adk/portfolio_data.py`](drake_talley_adk/portfolio_data.py) via [`drake_talley_adk/portfolio_tools.py`](drake_talley_adk/portfolio_tools.py). RevOps fields come from [`drake_talley_adk/revenue_ops_data.py`](drake_talley_adk/revenue_ops_data.py) via [`drake_talley_adk/revenue_ops_tools.py`](drake_talley_adk/revenue_ops_tools.py).
- **No invented CRM fields:** Scoring and eligibility use only keys present on lead records; the LLM narrates **tool output**, not made-up pipeline numbers.
- **Synthetic disclosure:** Case studies and RevOps companies are **explicitly fictional / demo** data; `verified_track_record` is résumé-backed.

## Specialist tool partitioning (RevOps)

[`drake_talley_adk/revenue_ops_tools.py`](drake_talley_adk/revenue_ops_tools.py) exposes **`REVOPS_TOOLS_POLICY`**, **`REVOPS_TOOLS_SCORING`**, **`REVOPS_TOOLS_ACTIONS`**, and **`REVOPS_TOOLS_ALL`**. Each sub-agent gets a **subset** of tools—mirroring production **least-privilege** tool access and keeping routing interpretable.

## Production-oriented next steps (not implemented here)

This repo optimizes for **GitHub review** and **local ADK Web** demos. Moving to production would add: an **offline eval** suite (task sets, rubrics, regression checks on tool+agent traces), **observability** (trace IDs, structured logs per tool call), **secrets** via Secret Manager or env injection (never committed), and deployment on **Cloud Run**, **Vertex AI Agent Engine**, or **`adk api_server`** patterns per [ADK docs](https://google.github.io/adk-docs/). ADK Web remains development-oriented per Google’s guidance.
