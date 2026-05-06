"""Deterministic tests for aml_alert_tools."""

from __future__ import annotations

from drake_talley_adk.aml_alert_tools import (
    compute_alert_severity,
    evaluate_regulatory_triggers,
    get_alert_record,
    recommend_disposition,
)


def test_get_alert_valid() -> None:
    r = get_alert_record("ALT-20001")
    assert r["status"] == "success"
    assert r["record"]["pep_or_sanctions_hit"] is True


def test_get_alert_invalid() -> None:
    r = get_alert_record("ALT-99999")
    assert r["status"] == "not_found"


def test_regulatory_triggers_alt20001() -> None:
    r = evaluate_regulatory_triggers("ALT-20001")
    assert r["status"] == "success"
    assert r["triggers"]["list_hit"] is True


def test_severity_alt20001_p1() -> None:
    r = compute_alert_severity("ALT-20001")
    assert r["status"] == "success"
    assert r["tier"] == "P1"
    assert r["severity_score_0_100"] >= 72


def test_disposition_alt20006_low_risk() -> None:
    r = recommend_disposition("ALT-20006")
    assert r["status"] == "success"
    assert r["recommended_disposition"] == "clear_with_monitoring"
