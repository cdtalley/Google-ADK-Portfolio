"""Deterministic tests for revenue_ops_tools."""

from __future__ import annotations

from drake_talley_adk.revenue_ops_tools import (
    compute_priority_score,
    evaluate_contact_eligibility,
    get_lead_record,
)


def test_get_lead_record_valid() -> None:
    r = get_lead_record("LD-10041")
    assert r["status"] == "success"
    assert r["lead_id"] == "LD-10041"
    assert r["record"]["segment"] == "enterprise"


def test_get_lead_record_invalid() -> None:
    r = get_lead_record("LD-99999")
    assert r["status"] == "not_found"


def test_eligibility_ld10041() -> None:
    r = evaluate_contact_eligibility("LD-10041")
    assert r["status"] == "success"
    assert r["eligible_for_outreach"] is True


def test_priority_score_ld10041_golden() -> None:
    r = compute_priority_score("LD-10041")
    assert r["status"] == "success"
    assert r["tier"] == "P1"
    assert r["priority_score_0_100"] >= 72
    assert any("demo" in x.lower() or "intent" in x.lower() for x in r["reasons"])


def test_ld10046_ineligible_reduces_tier() -> None:
    r = compute_priority_score("LD-10046")
    assert r["status"] == "success"
    assert r["tier"] == "P3"
