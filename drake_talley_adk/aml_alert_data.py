"""Synthetic BSA/AML alert queue for **Meridian Trust & Savings** (fictional bank).

Real problem: analyst throughput, policy-consistent escalation, auditable triage.
All alerts and policies are **demo-only**—not any real institution.
"""

from __future__ import annotations

from typing import Any

FICTIONAL_ORG = "Meridian Trust & Savings (synthetic)"

BUSINESS_PROBLEM: dict[str, Any] = {
    "fictional_org": FICTIONAL_ORG,
    "title": "BSA/AML alert disposition under analyst capacity constraints",
    "why_it_matters": (
        "Scenario engines and ML models flood operations with alerts. **FIFO review** "
        "buries time-sensitive, high-materiality patterns while analysts burn cycles on "
        "noise. The operating need is **explainable prioritization**, **policy-bound "
        "escalation**, and **traceable reasons** tied to alert attributes—not ad hoc "
        "judgment or LLM-invented facts."
    ),
    "what_good_looks_like": [
        "Every triage output cites **tool-derived** fields (amount band, velocity, list hits, priors, model score).",
        "Escalation and disposition labels match **illustrative** policy tables in this demo.",
        "Human compliance sign-off remains explicit; the copilot **recommends** next steps only.",
    ],
    "how_adk_maps": (
        "A coordinator agent **delegates** to policy, risk, and disposition specialists. "
        "**Function tools** return structured facts from synthetic alert rows so Gemini "
        "narrates without fabricating wire amounts or regulatory outcomes."
    ),
    "data_note": (
        "Customer aliases, alert IDs, and dollar amounts in `ALERTS` are **fabricated**. "
        "Policies are **illustrative** for portfolio review—not Meridian's or any bank's "
        "actual procedures. No regulator or institution endorses this demo."
    ),
}

SLA_HINTS: dict[str, Any] = {
    "list_hit_review_hours": 4,
    "high_value_wire_hours": 8,
    "standard_queue_hours": 48,
    "note": "Synthetic SLA hints for demo narrative only.",
}

SEGMENT_ESCALATION: dict[str, Any] = {
    "retail": {
        "default_l2_threshold_usd": 25000,
        "requires_dual_control_above_usd": 100000,
    },
    "smb_commercial": {
        "default_l2_threshold_usd": 50000,
        "requires_dual_control_above_usd": 250000,
    },
    "institutional": {
        "default_l2_threshold_usd": 100000,
        "requires_dual_control_above_usd": 500000,
    },
}

# Synthetic alerts keyed by id (format ALT-xxxxx)
ALERTS: dict[str, dict[str, Any]] = {
    "ALT-20001": {
        "customer_alias": "R. Kline (synthetic)",
        "customer_segment": "retail",
        "channel": "wire",
        "amount_usd": 182_500,
        "model_score_0_100": 94,
        "rule_codes": ["HV_WIRE", "GEO_HIGH", "VELOCITY_BURST"],
        "velocity_flags": {"burst_24h": True, "structuring_adjacent": False},
        "geography_risk_tier": "high",
        "pep_or_sanctions_hit": True,
        "prior_alerts_90d": 0,
        "narrative_summary": (
            "Outbound wire to high-risk corridor; sanctions-adjacent counterparty name "
            "match (low confidence). Model score elevated."
        ),
    },
    "ALT-20002": {
        "customer_alias": "Harbor Bench LLC (synthetic)",
        "customer_segment": "smb_commercial",
        "channel": "ach",
        "amount_usd": 9_200,
        "model_score_0_100": 71,
        "rule_codes": ["STRUCT_PATTERN", "ROUND_TRIP"],
        "velocity_flags": {"burst_24h": False, "structuring_adjacent": True},
        "geography_risk_tier": "medium",
        "pep_or_sanctions_hit": False,
        "prior_alerts_90d": 3,
        "narrative_summary": (
            "Multiple sub-threshold ACH credits aggregated across 6 business days; "
            "prior related alerts closed as inconclusive."
        ),
    },
    "ALT-20003": {
        "customer_alias": "M. Patel (synthetic)",
        "customer_segment": "retail",
        "channel": "cash",
        "amount_usd": 4_100,
        "model_score_0_100": 38,
        "rule_codes": ["CASH_THRESHOLD"],
        "velocity_flags": {"burst_24h": False, "structuring_adjacent": False},
        "geography_risk_tier": "low",
        "pep_or_sanctions_hit": False,
        "prior_alerts_90d": 0,
        "narrative_summary": (
            "Single-branch cash deposit just above threshold; no velocity or list hits."
        ),
    },
    "ALT-20004": {
        "customer_alias": "Cedarline Co-op Payroll (synthetic)",
        "customer_segment": "institutional",
        "channel": "wire",
        "amount_usd": 2_100_000,
        "model_score_0_100": 88,
        "rule_codes": ["HV_WIRE", "NEW_BENEFICIARY"],
        "velocity_flags": {"burst_24h": True, "structuring_adjacent": False},
        "geography_risk_tier": "medium",
        "pep_or_sanctions_hit": False,
        "prior_alerts_90d": 1,
        "narrative_summary": (
            "First-time beneficiary on payroll wire; amount consistent with disclosed "
            "contract but velocity spike vs 90d baseline."
        ),
    },
    "ALT-20005": {
        "customer_alias": "VectorRail Treasury (synthetic)",
        "customer_segment": "institutional",
        "channel": "wire",
        "amount_usd": 640_000,
        "model_score_0_100": 79,
        "rule_codes": ["CROSS_BORDER", "PEP_ADJACENT"],
        "velocity_flags": {"burst_24h": False, "structuring_adjacent": False},
        "geography_risk_tier": "high",
        "pep_or_sanctions_hit": True,
        "prior_alerts_90d": 2,
        "narrative_summary": (
            "Cross-border funding; PEP-adjacent beneficial owner flag from vendor list "
            "(medium confidence)."
        ),
    },
    "ALT-20006": {
        "customer_alias": "Bluecanoe SaaS Ops (synthetic)",
        "customer_segment": "smb_commercial",
        "channel": "ach",
        "amount_usd": 2_800,
        "model_score_0_100": 22,
        "rule_codes": ["LOW_VALUE_ACH"],
        "velocity_flags": {"burst_24h": False, "structuring_adjacent": False},
        "geography_risk_tier": "low",
        "pep_or_sanctions_hit": False,
        "prior_alerts_90d": 0,
        "narrative_summary": (
            "Routine vendor payout; model and rules low severity—candidate for "
            "accelerated documentation-only path if policy allows."
        ),
    },
    "ALT-20007": {
        "customer_alias": "Pinewood Retail AP (synthetic)",
        "customer_segment": "smb_commercial",
        "channel": "card",
        "amount_usd": 17_900,
        "model_score_0_100": 55,
        "rule_codes": ["MERCHANT_RISK", "AFTER_HOURS"],
        "velocity_flags": {"burst_24h": True, "structuring_adjacent": False},
        "geography_risk_tier": "low",
        "pep_or_sanctions_hit": False,
        "prior_alerts_90d": 4,
        "narrative_summary": (
            "Card spend clustering at high-risk MCC; repeat subject with prior "
            "no-action outcomes—watchlist for model drift."
        ),
    },
}

ANALYST_QUEUE_SNAPSHOT: dict[str, Any] = {
    "open_alerts_count": len(ALERTS),
    "analyst_fte_available_today": 11,
    "backlog_hours_est": 186,
    "note": "Synthetic queue snapshot for demo.",
}
