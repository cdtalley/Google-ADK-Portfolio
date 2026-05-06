"""Tools for RevOps lead triage — deterministic reads + scoring over synthetic CRM data."""

from __future__ import annotations

from typing import Any

from .revenue_ops_data import (
    BUSINESS_PROBLEM,
    CAPACITY_SNAPSHOT,
    LEADS,
    SEGMENT_POLICIES,
    SLA_CONFIG,
)


def get_revops_problem_brief() -> dict[str, Any]:
    """Returns the real-world business problem this agentic system addresses (dataset is synthetic)."""
    return {"status": "success", "business_problem": BUSINESS_PROBLEM}


def list_open_leads() -> dict[str, Any]:
    """Lists synthetic open leads with id, company, segment, and intent summary."""
    rows = []
    for lid, row in LEADS.items():
        rows.append(
            {
                "lead_id": lid,
                "company": row["company"],
                "segment": row["segment"],
                "intent_score_0_100": row["intent_score_0_100"],
                "demo_requested": row["demo_requested"],
                "last_activity_hours_ago": row["last_activity_hours_ago"],
            }
        )
    rows.sort(key=lambda x: -x["intent_score_0_100"])
    return {"status": "success", "leads": rows}


def get_lead_record(lead_id: str) -> dict[str, Any]:
    """Fetches full synthetic CRM row for one lead."""
    lid = lead_id.strip().upper().replace(" ", "")
    if lid not in LEADS:
        lids = ", ".join(sorted(LEADS.keys()))
        return {
            "status": "not_found",
            "message": f"Unknown lead_id {lead_id!r}. Valid: {lids}",
        }
    return {"status": "success", "lead_id": lid, "record": LEADS[lid]}


def get_segment_policy(segment: str) -> dict[str, Any]:
    """Returns outreach constraints for enterprise | mid_market | smb."""
    key = segment.strip().lower()
    if key not in SEGMENT_POLICIES:
        return {
            "status": "invalid_segment",
            "allowed": list(SEGMENT_POLICIES.keys()),
        }
    return {"status": "success", "segment": key, "policy": SEGMENT_POLICIES[key]}


def get_sla_config() -> dict[str, Any]:
    """Returns synthetic SLA targets for response times."""
    return {"status": "success", "sla": SLA_CONFIG}


def get_capacity_snapshot() -> dict[str, Any]:
    """Returns synthetic AE/SDR capacity and backlog size."""
    return {"status": "success", "capacity": CAPACITY_SNAPSHOT}


def evaluate_contact_eligibility(lead_id: str) -> dict[str, Any]:
    """Policy check: consent flags and segment/region legal review hints (synthetic)."""
    base = get_lead_record(lead_id)
    if base["status"] != "success":
        return base
    rec = base["record"]
    segment = rec["segment"]
    region = rec["region"]
    policy = SEGMENT_POLICIES.get(segment, {})
    legal_regions = policy.get("requires_legal_review_if_region", [])
    needs_legal = region in legal_regions or region in ("EU", "UK")
    email_ok = rec["contact_consent_email"]
    phone_ok = rec["contact_consent_phone"]
    eligible = email_ok or phone_ok
    channels = [c for c in policy.get("allowed_channels", []) if (c != "phone" or phone_ok) and (c != "email" or email_ok)]
    return {
        "status": "success",
        "lead_id": base["lead_id"],
        "eligible_for_outreach": eligible,
        "allowed_channels_respecting_consent": channels,
        "legal_review_suggested": needs_legal,
        "blockers": []
        if eligible
        else ["No contact consent on file for approved channels."],
    }


def compute_priority_score(lead_id: str) -> dict[str, Any]:
    """Deterministic priority score and tier from synthetic CRM fields (explainable)."""
    base = get_lead_record(lead_id)
    if base["status"] != "success":
        return base
    rec = base["record"]
    score = 0.0
    reasons: list[str] = []

    intent = rec["intent_score_0_100"]
    score += intent * 0.35
    reasons.append(f"Intent signal contributes {intent * 0.35:.1f} (35% weight of raw intent).")

    if rec["demo_requested"]:
        score += 25
        reasons.append("+25 demo requested (high buying signal).")
    if rec["trial_started"]:
        score += 15
        reasons.append("+15 active trial.")
    if rec["segment"] == "enterprise":
        score += 12
        reasons.append("+12 enterprise segment (strategic deal).")
    elif rec["segment"] == "mid_market":
        score += 6
        reasons.append("+6 mid-market segment.")

    lag = rec["last_activity_hours_ago"]
    if lag <= 4:
        score += 10
        reasons.append("+10 recency <=4h (hot).")
    elif lag <= 24:
        score += 5
        reasons.append("+5 recency <=24h.")

    if rec["competitor_mentioned"]:
        score += 5
        reasons.append("+5 competitive deal (win/loss intelligence value).")

    elig = evaluate_contact_eligibility(base["lead_id"])
    if elig["status"] == "success" and not elig["eligible_for_outreach"]:
        score -= 40
        reasons.append("-40 ineligible: missing consent (do not waste rep time).")

    if elig["status"] == "success" and elig.get("legal_review_suggested"):
        score += 3
        reasons.append("+3 legal/complexity flag (route to appropriate owner).")

    score = max(0, min(100, round(score, 1)))
    if score >= 72:
        tier = "P1"
    elif score >= 48:
        tier = "P2"
    else:
        tier = "P3"

    return {
        "status": "success",
        "lead_id": base["lead_id"],
        "priority_score_0_100": score,
        "tier": tier,
        "reasons": reasons,
        "sla_hint": (
            "demo_request"
            if rec["demo_requested"]
            else "trial" if rec["trial_started"] else "standard_inbound"
        ),
    }


REVOPS_TOOLS_ALL = [
    get_revops_problem_brief,
    list_open_leads,
    get_lead_record,
    get_segment_policy,
    get_sla_config,
    get_capacity_snapshot,
    evaluate_contact_eligibility,
    compute_priority_score,
]

REVOPS_TOOLS_POLICY = [
    get_revops_problem_brief,
    get_lead_record,
    get_segment_policy,
    evaluate_contact_eligibility,
    get_sla_config,
]

REVOPS_TOOLS_SCORING = [
    get_revops_problem_brief,
    get_lead_record,
    compute_priority_score,
    get_capacity_snapshot,
    list_open_leads,
]

REVOPS_TOOLS_ACTIONS = [
    get_revops_problem_brief,
    get_lead_record,
    compute_priority_score,
    evaluate_contact_eligibility,
    get_segment_policy,
    get_sla_config,
    get_capacity_snapshot,
]
