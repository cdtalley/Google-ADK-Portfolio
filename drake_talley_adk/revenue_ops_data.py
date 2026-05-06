"""Synthetic CRM-style dataset for a *real* business problem demo (lead prioritization).

The **problem** is real: revenue teams mis-allocate rep time when high-value,
high-intent leads queue behind low-fit noise. Rows below are **fabricated** records
so the ADK agent can call deterministic tools without external APIs.
"""

from __future__ import annotations

from typing import Any

BUSINESS_PROBLEM: dict[str, Any] = {
    "title": "Inbound B2B lead triage under SLA and policy constraints",
    "why_it_matters": (
        "Sales capacity is finite. When routing is FIFO or round-robin, **high-intent "
        "and high-LTV** opportunities wait while reps chase poor-fit accounts—directly "
        "hitting pipeline, win rate, and CAC payback. The fix is not “more AI scoring” "
        "alone: you need **policy gates** (compliance, territory, contact consent), "
        "**explainable** prioritization, and **actionable** next steps reps can execute."
    ),
    "what_good_looks_like": [
        "Every prioritized lead has **machine-readable reasons** tied to CRM fields.",
        "No outreach recommendation violates **segment rules** or consent flags.",
        "Handoff respects **SLA** (e.g., demo requests within hours, not days).",
        "Orchestration is **auditable**: which agent/tool path produced the decision.",
    ],
    "how_adk_maps": (
        "A coordinator agent **delegates** to specialists (policy, scoring, action "
        "planning). **Function tools** return structured facts from synthetic CRM data "
        "so Gemini narrates and plans without inventing pipeline numbers."
    ),
    "data_note": (
        "Companies and leads in `LEADS` are **synthetic**. The business problem and "
        "operating constraints are representative of production RevOps systems."
    ),
}

SLA_CONFIG: dict[str, Any] = {
    "demo_request_hours": 4,
    "trial_signup_hours": 24,
    "enterprise_inbound_hours": 8,
    "working_hours_timezone": "America/New_York",
}

SEGMENT_POLICIES: dict[str, Any] = {
    "enterprise": {
        "max_auto_outreach_per_day": 3,
        "requires_legal_review_if_region": ["EU", "UK"],
        "allowed_channels": ["email", "phone", "linkedin"],
    },
    "mid_market": {
        "max_auto_outreach_per_day": 8,
        "requires_legal_review_if_region": [],
        "allowed_channels": ["email", "phone"],
    },
    "smb": {
        "max_auto_outreach_per_day": 15,
        "requires_legal_review_if_region": [],
        "allowed_channels": ["email"],
    },
}

CAPACITY_SNAPSHOT: dict[str, Any] = {
    "ae_available_hours_this_week": 118,
    "sdr_available_hours_this_week": 210,
    "backlog_untouched_leads": 47,
    "note": "Synthetic capacity snapshot for portfolio demo.",
}

# Synthetic leads keyed by id
LEADS: dict[str, dict[str, Any]] = {
    "LD-10041": {
        "company": "Harbor Mill Steelworks",
        "segment": "enterprise",
        "region": "US-East",
        "industry": "Industrial manufacturing",
        "mrr_band_usd": "80k–120k",
        "intent_score_0_100": 88,
        "demo_requested": True,
        "trial_started": False,
        "last_activity_hours_ago": 2,
        "source": "inbound pricing page",
        "contact_consent_email": True,
        "contact_consent_phone": True,
        "competitor_mentioned": False,
        "notes": "Asked for Vertex + BigQuery security worksheet.",
    },
    "LD-10042": {
        "company": "Lumenfold Analytics",
        "segment": "mid_market",
        "region": "EU",
        "industry": "Business analytics",
        "mrr_band_usd": "15k–25k",
        "intent_score_0_100": 62,
        "demo_requested": False,
        "trial_started": True,
        "last_activity_hours_ago": 18,
        "source": "product-led growth signup",
        "contact_consent_email": True,
        "contact_consent_phone": False,
        "competitor_mentioned": True,
        "notes": "Compared us to incumbent in RFP language.",
    },
    "LD-10043": {
        "company": "Cedarline Health Co-op",
        "segment": "enterprise",
        "region": "US-West",
        "industry": "Healthcare payer services",
        "mrr_band_usd": "200k+",
        "intent_score_0_100": 91,
        "demo_requested": True,
        "trial_started": False,
        "last_activity_hours_ago": 5,
        "source": "partner referral",
        "contact_consent_email": True,
        "contact_consent_phone": True,
        "competitor_mentioned": False,
        "notes": "Needs BAA + data residency discussion.",
    },
    "LD-10044": {
        "company": "Pinewood Retail Group",
        "segment": "mid_market",
        "region": "US-Central",
        "industry": "Retail",
        "mrr_band_usd": "10k–18k",
        "intent_score_0_100": 44,
        "demo_requested": False,
        "trial_started": False,
        "last_activity_hours_ago": 96,
        "source": "webinar",
        "contact_consent_email": True,
        "contact_consent_phone": False,
        "competitor_mentioned": False,
        "notes": "Low engagement post-webinar.",
    },
    "LD-10045": {
        "company": "VectorRail Logistics",
        "segment": "enterprise",
        "region": "UK",
        "industry": "Transportation",
        "mrr_band_usd": "150k–220k",
        "intent_score_0_100": 77,
        "demo_requested": True,
        "trial_started": False,
        "last_activity_hours_ago": 1,
        "source": "event scan",
        "contact_consent_email": True,
        "contact_consent_phone": True,
        "competitor_mentioned": False,
        "notes": "UK entity; legal review likely for MSAs.",
    },
    "LD-10046": {
        "company": "Bluecanoe SaaS",
        "segment": "smb",
        "region": "US-East",
        "industry": "Vertical SaaS",
        "mrr_band_usd": "2k–4k",
        "intent_score_0_100": 35,
        "demo_requested": False,
        "trial_started": False,
        "last_activity_hours_ago": 200,
        "source": "content download",
        "contact_consent_email": False,
        "contact_consent_phone": False,
        "competitor_mentioned": False,
        "notes": "**Do not email** — missing consent.",
    },
}
