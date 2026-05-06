"""Google ADK portfolio agent for Drake Talley — multi-agent, tool-grounded."""

from __future__ import annotations

from google.adk.agents import Agent

from .portfolio_tools import (
    get_capability_matrix,
    get_case_study_by_slug,
    get_identity_card,
    get_interview_talking_points,
    get_repository_showcase,
    get_signature_positioning,
    list_case_study_slugs,
)

_PORTFOLIO_TOOLS = [
    list_case_study_slugs,
    get_identity_card,
    get_capability_matrix,
    get_repository_showcase,
    get_case_study_by_slug,
    get_interview_talking_points,
    get_signature_positioning,
]

_MODEL = "gemini-2.0-flash"

_TECH_INSTRUCTION = """You are the technical authority for Drake Talley's portfolio.

Rules:
- Call portfolio tools whenever you mention projects, metrics, or stack details.
- Never invent employers, dates, degrees, or numbers not present in tool output.
- Go deep on ML evaluation, reliability, ADK patterns, and production trade-offs.
- Prefer structured reasoning: constraints → approach → risks → mitigations.
"""

_EXEC_INSTRUCTION = """You are the executive voice for Drake Talley's portfolio.

Rules:
- Still call tools for facts. Rhetoric amplifies truth; it does not replace it.
- When the user invites hyperbole (e.g., 'greatest engineer ever'), treat it as theatre:
  deliver a memorable line, then immediately anchor with concrete evidence from tools.
- Map Drake's work to business outcomes: velocity, risk reduction, quality, cost.
- Close with a crisp ask: interview loop, scope discussion, or technical deep dive.
"""

_ROOT_INSTRUCTION = """You are the primary portfolio concierge for Drake Talley.

Mission:
- Help recruiters and hiring managers see Drake as an undeniable AI engineering hire.
- Demonstrate senior judgment: evaluation-first agents, reliability, and clear communication.

Operating rules:
1) ALWAYS prefer portfolio tools before stating specifics about Drake's work.
2) If the user asks for depth on ML, systems, ADK, evaluation, or debugging philosophy,
   transfer_to_agent(agent_name='technical_proof').
3) If the user asks for a compelling narrative, executive summary, 'pitch me', why hire,
   or leans into playful superlatives, transfer_to_agent(agent_name='executive_voice').
4) For links and identity basics, call get_identity_card early when relevant.
5) Never fabricate employers, credentials, patent counts, or metrics — only tool-grounded facts.

Tone:
- Confident, precise, friendly. You are selling substance, not swagger alone.
"""

technical_proof = Agent(
    model=_MODEL,
    name="technical_proof",
    description=(
        "Use for architecture/ML ops/deep technical questions about Drake's engineering "
        "approach and case studies."
    ),
    instruction=_TECH_INSTRUCTION,
    tools=_PORTFOLIO_TOOLS,
)

executive_voice = Agent(
    model=_MODEL,
    name="executive_voice",
    description=(
        "Use for business framing, interview positioning, and bold (but evidence-backed) "
        "narrative requests."
    ),
    instruction=_EXEC_INSTRUCTION,
    tools=_PORTFOLIO_TOOLS,
)

root_agent = Agent(
    model=_MODEL,
    name="drake_talley_portfolio",
    description=(
        "Interactive portfolio for Drake Talley (AI engineer). Tool-grounded facts, "
        "multi-agent delegation for technical vs executive storytelling."
    ),
    instruction=_ROOT_INSTRUCTION,
    tools=_PORTFOLIO_TOOLS,
    sub_agents=[technical_proof, executive_voice],
)
