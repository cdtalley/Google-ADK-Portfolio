"""Deterministic tools over synthetic BSA/AML alerts (Meridian demo)."""

from __future__ import annotations

from typing import Any

from .aml_alert_data import (
    ALERTS,
    ANALYST_QUEUE_SNAPSHOT,
    BUSINESS_PROBLEM,
    SEGMENT_ESCALATION,
    SLA_HINTS,
)


def _normalize_alert_id(alert_id: str) -> str:
    return alert_id.strip().upper().replace(" ", "")


def get_aml_problem_brief() -> dict[str, Any]:
    """Returns the business problem for Meridian (synthetic) BSA/AML triage demo."""
    return {"status": "success", "business_problem": BUSINESS_PROBLEM}


def list_open_alerts() -> dict[str, Any]:
    """Lists synthetic open alerts with id, segment, channel, amount, model score."""
    rows = []
    for aid, row in ALERTS.items():
        rows.append(
            {
                "alert_id": aid,
                "customer_segment": row["customer_segment"],
                "channel": row["channel"],
                "amount_usd": row["amount_usd"],
                "model_score_0_100": row["model_score_0_100"],
                "pep_or_sanctions_hit": row["pep_or_sanctions_hit"],
            }
        )
    rows.sort(key=lambda x: -x["model_score_0_100"])
    return {"status": "success", "alerts": rows}


def get_alert_record(alert_id: str) -> dict[str, Any]:
    """Fetches full synthetic alert row."""
    aid = _normalize_alert_id(alert_id)
    if aid not in ALERTS:
        valid = ", ".join(sorted(ALERTS.keys()))
        return {
            "status": "not_found",
            "message": f"Unknown alert_id {alert_id!r}. Valid: {valid}",
        }
    return {"status": "success", "alert_id": aid, "record": ALERTS[aid]}


def get_escalation_policy(customer_segment: str) -> dict[str, Any]:
    """Returns illustrative USD thresholds for segment (synthetic policy)."""
    key = customer_segment.strip().lower()
    if key not in SEGMENT_ESCALATION:
        return {
            "status": "invalid_segment",
            "allowed": list(SEGMENT_ESCALATION.keys()),
        }
    return {"status": "success", "segment": key, "policy": SEGMENT_ESCALATION[key]}


def get_sla_hints() -> dict[str, Any]:
    """Synthetic SLA hints for analyst narrative."""
    return {"status": "success", "sla": SLA_HINTS}


def get_analyst_queue_snapshot() -> dict[str, Any]:
    """Synthetic capacity / backlog snapshot."""
    return {"status": "success", "queue": ANALYST_QUEUE_SNAPSHOT}


def evaluate_regulatory_triggers(alert_id: str) -> dict[str, Any]:
    """Structured flags from alert fields—rules in code, not LLM guesses."""
    base = get_alert_record(alert_id)
    if base["status"] != "success":
        return base
    rec = base["record"]
    amount = rec["amount_usd"]
    flags: dict[str, Any] = {
        "high_value_wire": rec["channel"] == "wire" and amount >= 100_000,
        "structuring_adjacent_pattern": bool(
            rec["velocity_flags"].get("structuring_adjacent")
        ),
        "repeat_subject_90d": rec["prior_alerts_90d"] >= 2,
        "list_hit": bool(rec["pep_or_sanctions_hit"]),
        "geography_elevated": rec["geography_risk_tier"] in ("high", "medium"),
        "model_elevated": rec["model_score_0_100"] >= 75,
    }
    flags["sar_prep_escalation_recommended"] = (
        flags["list_hit"] and flags["high_value_wire"]
    ) or (flags["structuring_adjacent_pattern"] and flags["repeat_subject_90d"])
    reasons = [k for k, v in flags.items() if v and k != "sar_prep_escalation_recommended"]
    return {
        "status": "success",
        "alert_id": base["alert_id"],
        "triggers": flags,
        "trigger_keys_true": reasons,
        "disclaimer": "Illustrative flags for demo; not legal or regulatory advice.",
    }


def compute_alert_severity(alert_id: str) -> dict[str, Any]:
    """Explainable severity score 0–100 and tier P1|P2|P3 from synthetic fields."""
    base = get_alert_record(alert_id)
    if base["status"] != "success":
        return base
    rec = base["record"]
    score = 0.0
    reasons: list[str] = []

    m = rec["model_score_0_100"]
    score += m * 0.4
    reasons.append(f"Model score contributes {m * 0.4:.1f} (40% weight).")

    amt = rec["amount_usd"]
    if amt >= 1_000_000:
        score += 18
        reasons.append("+18 amount >= $1M.")
    elif amt >= 100_000:
        score += 12
        reasons.append("+12 amount >= $100k.")
    elif amt >= 10_000:
        score += 6
        reasons.append("+6 amount >= $10k.")

    if rec["pep_or_sanctions_hit"]:
        score += 14
        reasons.append("+14 list hit (PEP/sanctions flag).")

    if rec["geography_risk_tier"] == "high":
        score += 10
        reasons.append("+10 geography risk high.")
    elif rec["geography_risk_tier"] == "medium":
        score += 5
        reasons.append("+5 geography risk medium.")

    if rec["velocity_flags"].get("burst_24h"):
        score += 8
        reasons.append("+8 velocity burst 24h.")
    if rec["velocity_flags"].get("structuring_adjacent"):
        score += 12
        reasons.append("+12 structuring-adjacent pattern.")

    pri = rec["prior_alerts_90d"]
    if pri >= 3:
        score += 10
        reasons.append("+10 prior alerts 90d >= 3.")
    elif pri >= 1:
        score += 4
        reasons.append("+4 prior alerts 90d >= 1.")

    tr = evaluate_regulatory_triggers(base["alert_id"])
    if tr["status"] == "success" and tr["triggers"].get("sar_prep_escalation_recommended"):
        score += 6
        reasons.append("+6 composite SAR-prep escalation pattern (demo rule).")

    score = max(0, min(100, round(score, 1)))
    if score >= 72:
        tier = "P1"
    elif score >= 48:
        tier = "P2"
    else:
        tier = "P3"

    return {
        "status": "success",
        "alert_id": base["alert_id"],
        "severity_score_0_100": score,
        "tier": tier,
        "reasons": reasons,
    }


def recommend_disposition(alert_id: str) -> dict[str, Any]:
    """Maps tier + triggers to allowed disposition labels (demo only)."""
    base = get_alert_record(alert_id)
    if base["status"] != "success":
        return base
    sev = compute_alert_severity(base["alert_id"])
    tr = evaluate_regulatory_triggers(base["alert_id"])
    if sev["status"] != "success" or tr["status"] != "success":
        return {"status": "error", "message": "Upstream tool failure."}

    tier = sev["tier"]
    flags = tr["triggers"]

    if flags.get("sar_prep_escalation_recommended"):
        disposition = "escalate_sar_prep_workflow"
        summary = (
            "Route to L2 + financial intelligence unit prep **per demo policy**; "
            "no disposition language implying regulatory filing."
        )
    elif tier == "P1" or flags.get("list_hit"):
        disposition = "escalate_l2_urgent"
        summary = "Priority L2 review within SLA hint for list/high materiality patterns."
    elif tier == "P2":
        disposition = "analyst_deep_dive"
        summary = "Standard elevated queue: full narrative + counterparty checks."
    else:
        disposition = "clear_with_monitoring"
        summary = "Document rationale; light-touch monitoring if policy permits."

    return {
        "status": "success",
        "alert_id": base["alert_id"],
        "recommended_disposition": disposition,
        "summary": summary,
        "tier": tier,
        "severity_score_0_100": sev["severity_score_0_100"],
        "depends_on_triggers": {k: v for k, v in flags.items() if v},
        "disclaimer": "Demo recommendation only—not approval to close or escalate in production.",
    }


AML_TOOLS_ALL = [
    get_aml_problem_brief,
    list_open_alerts,
    get_alert_record,
    get_escalation_policy,
    get_sla_hints,
    get_analyst_queue_snapshot,
    evaluate_regulatory_triggers,
    compute_alert_severity,
    recommend_disposition,
]

AML_TOOLS_POLICY = [
    get_aml_problem_brief,
    get_alert_record,
    get_escalation_policy,
    get_sla_hints,
    evaluate_regulatory_triggers,
]

AML_TOOLS_SCORING = [
    get_aml_problem_brief,
    get_alert_record,
    compute_alert_severity,
    get_analyst_queue_snapshot,
    list_open_alerts,
]

AML_TOOLS_DISPOSITION = [
    get_aml_problem_brief,
    get_alert_record,
    compute_alert_severity,
    evaluate_regulatory_triggers,
    recommend_disposition,
    get_escalation_policy,
    get_sla_hints,
]
