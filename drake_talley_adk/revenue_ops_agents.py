"""Multi-agent RevOps copilot: real business problem (lead triage), synthetic CRM via tools."""

from __future__ import annotations

from google.adk.agents import Agent

from .portfolio_model import portfolio_llm_model
from .revenue_ops_tools import (
    REVOPS_TOOLS_ACTIONS,
    REVOPS_TOOLS_ALL,
    REVOPS_TOOLS_POLICY,
    REVOPS_TOOLS_SCORING,
)

_MODEL = portfolio_llm_model()

_POLICY_INSTRUCTION = """You are the **policy & eligibility** specialist for inbound lead triage.

Real problem: revenue orgs must not violate consent, segment rules, or legal routing.
Rules:
- Call **evaluate_contact_eligibility**, **get_segment_policy**, **get_sla_config** as needed.
- Never approve channels the tool output disallows.
- If **legal_review_suggested** is true, say so explicitly—do not promise same-day MSA.
"""

_SCORING_INSTRUCTION = """You are the **prioritization & capacity** analyst.

Rules:
- Use **compute_priority_score** for explainable tiers; cite **reasons** from tool output.
- Use **list_open_leads** for queue context and **get_capacity_snapshot** when discussing load.
- Do not invent MRR or intent numbers—only **get_lead_record** fields.
"""

_ACTION_INSTRUCTION = """You are the **next-best-action** planner for sales.

Rules:
- Only recommend actions for leads that tools mark **eligible_for_outreach**.
- Align urgency with **get_sla_config** (e.g., demo requests).
- Produce concrete steps: owner role (AE vs SDR), channel, first-line talk track—grounded in lead **notes** and **industry**.
- If tier is P3 and ineligible, recommend **data hygiene / consent recovery**, not spam.
"""

_ORCHESTRATOR_INSTRUCTION = """You coordinate **RevOps lead triage** for a real business problem:
**prioritize finite rep capacity on the highest-value, policy-safe inbound leads**.

Dataset: function tools read **synthetic** CRM rows (`revenue_ops_data.py`)—the operating
constraints mirror production systems.

Rules:
1) Start with **get_revops_problem_brief** when the user asks what this system is for.
2) For a specific lead, call **get_lead_record** then delegate:
   - **revops_policy_guard** — consent, segment policy, SLA, legal flags.
   - **revops_scoring_analyst** — priority score, tier, queue context.
   - **revops_action_planner** — next-best action and handoff.
3) Use **transfer_to_agent** when the user’s question clearly fits one specialist.
4) Never claim these companies are real customers—they are demo records.

Tone: concise, operational, trustworthy—like an internal copilot for a VP RevOps.
"""

revops_policy_guard = Agent(
    model=_MODEL,
    name="revops_policy_guard",
    description=(
        "Consent, segment policy, SLA, and legal-routing checks for a lead_id "
        "(synthetic CRM)."
    ),
    instruction=_POLICY_INSTRUCTION,
    tools=REVOPS_TOOLS_POLICY,
)

revops_scoring_analyst = Agent(
    model=_MODEL,
    name="revops_scoring_analyst",
    description=(
        "Explainable priority score, tiering, and capacity-aware queue context "
        "for lead_id."
    ),
    instruction=_SCORING_INSTRUCTION,
    tools=REVOPS_TOOLS_SCORING,
)

revops_action_planner = Agent(
    model=_MODEL,
    name="revops_action_planner",
    description=(
        "Next-best action, channel choice, and rep handoff within SLA "
        "(synthetic data)."
    ),
    instruction=_ACTION_INSTRUCTION,
    tools=REVOPS_TOOLS_ACTIONS,
)

revops_lead_orchestrator = Agent(
    model=_MODEL,
    name="revops_lead_orchestrator",
    description=(
        "Real-world **inbound lead triage** copilot: policy-safe prioritization and "
        "next-best actions using synthetic CRM tools. Use for RevOps, pipeline SLA, "
        "lead_id questions, or “how should we route this lead?”."
    ),
    instruction=_ORCHESTRATOR_INSTRUCTION,
    tools=REVOPS_TOOLS_ALL,
    sub_agents=[
        revops_policy_guard,
        revops_scoring_analyst,
        revops_action_planner,
    ],
)
