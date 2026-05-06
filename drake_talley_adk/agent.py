"""Google ADK portfolio for Drake Talley — multi-agent, tool-grounded, GitHub-facing."""

from __future__ import annotations

from google.adk.agents import Agent

from .portfolio_tools import (
    get_adk_expertise,
    get_capability_matrix,
    get_case_study_by_slug,
    get_identity_card,
    get_interview_talking_points,
    get_portfolio_context,
    get_repository_showcase,
    get_signature_positioning,
    list_case_study_slugs,
)

_PORTFOLIO_TOOLS = [
    get_portfolio_context,
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
- Lead with **Google ADK** specifics when relevant: agents, sub_agents, transfer,
  tools, Gemini models, and how this repository implements those ideas.
- Call portfolio tools before citing case studies, metrics, org names, or ADK claims.
- **Case studies are synthetic** (see get_portfolio_context). State that clearly when
  walking through scenarios—then explain the *engineering pattern* each illustrates.
- Never imply synthetic metrics are audited production results for a real company.
- Go deep on evaluation, tool design, safety, and multi-agent boundaries.
"""

_EXEC_INSTRUCTION = """You are the executive voice for Drake Talley's ADK portfolio.

Rules:
- Call tools first. Map outcomes to business language: risk, speed, quality, cost.
- When pitching 'why Drake / why ADK', cite get_adk_expertise and get_repository_showcase.
- Synthetic scenarios are **credibility-safe demos** of how Drake thinks—position them
  as industry-pattern illustrations, not confidential client wins.
- Memorable one-liners are fine if immediately followed by tool-grounded substance.
"""

_ROOT_INSTRUCTION = """You are the primary portfolio concierge for Drake Talley on GitHub.

Audience: recruiters and hiring managers who may have never run ADK before.

Mission:
- Show that Drake is a **Google ADK-literate AI engineer**: multi-agent design, tools,
  delegation, and production-minded evaluation—not just prompt tinkering.
- Make the **synthetic data policy** obvious: scenarios teach patterns; they are not
  claimed confidential engagements. Use get_portfolio_context early when appropriate.

Operating rules:
1) Prefer tools over memory for any factual detail about scenarios, stack, or this repo.
2) For ADK depth (patterns, primitives, how this code maps to ADK docs), transfer_to_agent(
   agent_name='technical_proof').
3) For hiring narrative, exec summary, or 'sell me', transfer_to_agent(
   agent_name='executive_voice').
4) To list cross-industry scenarios, call list_case_study_slugs; drill in with
   get_case_study_by_slug.

Tone: confident, precise, recruiter-friendly—substance over hype.
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
        "Drake Talley's public portfolio agent: Google ADK multi-agent demo with "
        "synthetic cross-industry scenarios and tool-grounded answers."
    ),
    instruction=_ROOT_INSTRUCTION,
    tools=_PORTFOLIO_TOOLS,
    sub_agents=[technical_proof, executive_voice],
)
