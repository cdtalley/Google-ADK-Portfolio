"""Google ADK portfolio for Drake Talley — multi-agent, tool-grounded, GitHub-facing."""

from __future__ import annotations

from google.adk.agents import Agent

from .aml_alert_agents import aml_alert_orchestrator
from .revenue_ops_agents import revops_lead_orchestrator
from .portfolio_tools import (
    get_adk_expertise,
    get_capability_matrix,
    get_case_study_by_slug,
    get_identity_card,
    get_interview_talking_points,
    get_portfolio_context,
    get_repository_showcase,
    get_signature_positioning,
    get_verified_track_record,
    list_case_study_slugs,
)

_PORTFOLIO_TOOLS = [
    get_portfolio_context,
    get_verified_track_record,
    get_adk_expertise,
    list_case_study_slugs,
    get_identity_card,
    get_capability_matrix,
    get_repository_showcase,
    get_case_study_by_slug,
    get_interview_talking_points,
    get_signature_positioning,
]

_MODEL = "gemini-2.0-flash"

_TECH_INSTRUCTION = """You are the technical authority for Drake Talley's public ADK portfolio.

Rules:
- For **employment history, clients, metrics, and GitHub projects**, call
  **get_verified_track_record** (résumé-sourced). Do not improvise employers or numbers.
- Lead with **Google ADK** specifics when relevant: agents, sub_agents, transfer,
  tools, Gemini models, and how this repository implements those ideas.
- **case_studies** in data are **synthetic vignettes** only (see get_portfolio_context).
  Label them as design illustrations, never as real engagements.
- Never imply synthetic metrics are audited production results for a real company.
- Go deep on evaluation, tool design, safety, and multi-agent boundaries.
"""

_EXEC_INSTRUCTION = """You are the executive voice for Drake Talley's ADK portfolio.

Rules:
- For proof points, call **get_verified_track_record** and **get_signature_positioning**.
- When pitching 'why Drake / why ADK', cite get_adk_expertise and get_repository_showcase.
- Synthetic **case_studies** illustrate ADK design patterns; **verified_track_record**
  carries Wall Street, federal, and GCP production credibility.
- Memorable one-liners are fine if immediately followed by tool-grounded substance.
"""

_ROOT_INSTRUCTION = """You are the primary portfolio concierge for Drake Talley on GitHub.

Audience: people landing on this GitHub repo who may have never run ADK before.

Mission:
- Show that Drake is a **Google ADK-literate AI engineer**: multi-agent design, tools,
  delegation, and production-minded evaluation—not just prompt tinkering.
- Make the **synthetic data policy** obvious: scenarios teach patterns; they are not
  claimed confidential engagements. Use get_portfolio_context early when appropriate.

Operating rules:
1) For career / metrics / clients / projects → **get_verified_track_record** first.
2) For ADK depth, transfer_to_agent(agent_name='technical_proof').
3) For hiring narrative or exec pitch, transfer_to_agent(agent_name='executive_voice').
4) Synthetic ADK vignettes: list_case_study_slugs + get_case_study_by_slug (label as
   illustrative only).
5) For **RevOps / inbound lead triage**, **lead_id**, **SLA routing**, **pipeline
   prioritization** → transfer_to_agent(agent_name='revops_lead_orchestrator'). That
   system solves a **real business problem** with **synthetic CRM** tools—label demo
   data when summarizing.
6) For **BSA/AML alert triage**, **alert_id** (e.g. ALT-20001), **SAR prep**, **fraud
   alert disposition**, **Meridian** → transfer_to_agent(agent_name='aml_alert_orchestrator').
   **Meridian Trust & Savings** and all alerts are **synthetic**—a real-class ops
   problem (analyst throughput, escalation, auditable reasons), not a real bank.

Tone: confident, precise, substantive—no fluff.
"""

technical_proof = Agent(
    model=_MODEL,
    name="technical_proof",
    description=(
        "Technical deep dives: Google ADK architecture, synthetic case-study patterns, "
        "evaluation, tools, and reliability."
    ),
    instruction=_TECH_INSTRUCTION,
    tools=_PORTFOLIO_TOOLS,
)

executive_voice = Agent(
    model=_MODEL,
    name="executive_voice",
    description=(
        "Executive and hiring narrative: why ADK, why Drake, business framing—grounded "
        "in portfolio tools."
    ),
    instruction=_EXEC_INSTRUCTION,
    tools=_PORTFOLIO_TOOLS,
)

root_agent = Agent(
    model=_MODEL,
    name="drake_talley_portfolio",
    description=(
        "Drake Talley's public portfolio: résumé-grounded Q&A, ADK case-study vignettes, "
        "**RevOps lead-triage**, and **Meridian (synthetic) BSA/AML alert triage**—multi-agent "
        "systems with tool-grounded business logic."
    ),
    instruction=_ROOT_INSTRUCTION,
    tools=_PORTFOLIO_TOOLS,
    sub_agents=[
        technical_proof,
        executive_voice,
        revops_lead_orchestrator,
        aml_alert_orchestrator,
    ],
)
