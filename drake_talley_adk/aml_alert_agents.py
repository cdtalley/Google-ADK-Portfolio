"""Meridian Trust & Savings (synthetic) BSA/AML alert triage — multi-agent ADK."""

from __future__ import annotations

from google.adk.agents import Agent

from .aml_alert_tools import (
    AML_TOOLS_ALL,
    AML_TOOLS_DISPOSITION,
    AML_TOOLS_POLICY,
    AML_TOOLS_SCORING,
)
from .portfolio_model import portfolio_llm_model

_MODEL = portfolio_llm_model()

_AML_POLICY_INSTRUCTION = """You are the **policy & regulatory-triggers** specialist for **Meridian Trust & Savings (synthetic)** BSA/AML demo.

Rules:
- Call **get_escalation_policy**, **evaluate_regulatory_triggers**, **get_sla_hints** as needed; **get_alert_record** for facts.
- Never state real-world SAR filing decisions—only **demo** disposition paths.
- If **sar_prep_escalation_recommended** is true from tools, say so clearly.
- Do not imply FDIC, FinCEN, or any regulator endorses this chatbot.
"""

_AML_RISK_INSTRUCTION = """You are the **severity & queue** analyst for Meridian (synthetic) alerts.

Rules:
- Use **compute_alert_severity** for score and tier; cite **reasons** from tool output only.
- Use **list_open_alerts** and **get_analyst_queue_snapshot** for backlog context.
- Never invent USD amounts or model scores—only **get_alert_record** / scoring tools.
"""

_AML_DISPOSITION_INSTRUCTION = """You are the **disposition planning** specialist (demo only).

Rules:
- Call **recommend_disposition** after you have alert context; narrate **recommended_disposition** and **summary** from tool output.
- Align timing narrative with **get_sla_hints** when relevant.
- If disposition is **clear_with_monitoring**, still note residual risks from triggers.
"""

_AML_ORCHESTRATOR_INSTRUCTION = """You coordinate **BSA/AML alert triage** for **Meridian Trust & Savings (synthetic)**—a **real-class** problem
(analyst capacity, policy-consistent escalation, auditable reasons) using **fabricated** alert rows.

Rules:
1) Start with **get_aml_problem_brief** when the user asks what this system is for.
2) For a specific alert, call **get_alert_record** then delegate as needed:
   - **aml_policy_specialist** — segment thresholds, regulatory trigger flags, SLA hints.
   - **aml_risk_analyst** — explainable severity score, tier, queue context.
   - **aml_disposition_planner** — recommended next-step label (demo policy).
3) Use **transfer_to_agent** when the user's question clearly fits one specialist.
4) Always state that **Meridian and all alerts are synthetic** portfolio data.

Tone: calm, precise, compliance-adjacent—like an internal copilot for a BSA officer.
"""

aml_policy_specialist = Agent(
    model=_MODEL,
    name="aml_policy_specialist",
    description=(
        "Meridian (synthetic): escalation thresholds, regulatory trigger flags, SLA "
        "hints for alert_id."
    ),
    instruction=_AML_POLICY_INSTRUCTION,
    tools=AML_TOOLS_POLICY,
)

aml_risk_analyst = Agent(
    model=_MODEL,
    name="aml_risk_analyst",
    description=(
        "Meridian (synthetic): explainable alert severity tier and analyst queue "
        "context for alert_id."
    ),
    instruction=_AML_RISK_INSTRUCTION,
    tools=AML_TOOLS_SCORING,
)

aml_disposition_planner = Agent(
    model=_MODEL,
    name="aml_disposition_planner",
    description=(
        "Meridian (synthetic): demo disposition recommendation from tool rules for "
        "alert_id."
    ),
    instruction=_AML_DISPOSITION_INSTRUCTION,
    tools=AML_TOOLS_DISPOSITION,
)

aml_alert_orchestrator = Agent(
    model=_MODEL,
    name="aml_alert_orchestrator",
    description=(
        "**Meridian Trust & Savings (synthetic)** BSA/AML alert triage: policy triggers, "
        "severity, disposition. Use for **alert_id** (e.g. ALT-20001), AML, BSA, fraud "
        "alert queue, escalation, or disposition questions."
    ),
    instruction=_AML_ORCHESTRATOR_INSTRUCTION,
    tools=AML_TOOLS_ALL,
    sub_agents=[
        aml_policy_specialist,
        aml_risk_analyst,
        aml_disposition_planner,
    ],
)
