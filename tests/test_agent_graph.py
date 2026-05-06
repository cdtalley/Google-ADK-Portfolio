"""Smoke tests: agent graph wiring (imports google-adk; no Gemini API calls)."""

from __future__ import annotations

from drake_talley_adk.agent import root_agent
from drake_talley_adk.aml_alert_agents import aml_alert_orchestrator
from drake_talley_adk.revenue_ops_agents import revops_lead_orchestrator


def test_root_agent_subagents() -> None:
    names = {a.name for a in root_agent.sub_agents}
    assert names == {
        "technical_proof",
        "executive_voice",
        "revops_lead_orchestrator",
        "aml_alert_orchestrator",
    }


def test_revops_subagents() -> None:
    names = {a.name for a in revops_lead_orchestrator.sub_agents}
    assert names == {
        "revops_policy_guard",
        "revops_scoring_analyst",
        "revops_action_planner",
    }


def test_aml_subagents() -> None:
    names = {a.name for a in aml_alert_orchestrator.sub_agents}
    assert names == {
        "aml_policy_specialist",
        "aml_risk_analyst",
        "aml_disposition_planner",
    }


def test_tool_partitions_are_strict_subsets() -> None:
    from drake_talley_adk.aml_alert_tools import (
        AML_TOOLS_ALL,
        AML_TOOLS_DISPOSITION,
        AML_TOOLS_POLICY,
        AML_TOOLS_SCORING,
    )
    from drake_talley_adk.revenue_ops_tools import (
        REVOPS_TOOLS_ACTIONS,
        REVOPS_TOOLS_ALL,
        REVOPS_TOOLS_POLICY,
        REVOPS_TOOLS_SCORING,
    )

    assert set(REVOPS_TOOLS_POLICY) <= set(REVOPS_TOOLS_ALL)
    assert set(REVOPS_TOOLS_SCORING) <= set(REVOPS_TOOLS_ALL)
    assert set(REVOPS_TOOLS_ACTIONS) <= set(REVOPS_TOOLS_ALL)
    assert set(AML_TOOLS_POLICY) <= set(AML_TOOLS_ALL)
    assert set(AML_TOOLS_SCORING) <= set(AML_TOOLS_ALL)
    assert set(AML_TOOLS_DISPOSITION) <= set(AML_TOOLS_ALL)
