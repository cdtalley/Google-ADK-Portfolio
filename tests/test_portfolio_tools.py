"""Deterministic tests for portfolio_tools."""

from __future__ import annotations

from drake_talley_adk.portfolio_tools import (
    get_case_study_by_slug,
    get_interview_talking_points,
    get_verified_track_record,
    list_case_study_slugs,
)


def test_verified_track_record_shape() -> None:
    r = get_verified_track_record()
    assert r["status"] == "success"
    v = r["verified_track_record"]
    assert "roles" in v
    assert "summary" in v
    assert isinstance(v["roles"], list)
    assert len(v["roles"]) >= 1


def test_list_case_study_slugs_nonempty() -> None:
    r = list_case_study_slugs()
    assert r["status"] == "success"
    assert len(r["case_studies"]) >= 1


def test_get_case_study_found_and_not_found() -> None:
    ok = get_case_study_by_slug("fintech-compliance-analyst")
    assert ok["status"] == "success"
    assert ok["case_study"]["slug"] == "fintech-compliance-analyst"

    bad = get_case_study_by_slug("no-such-slug-xyz")
    assert bad["status"] == "not_found"
    assert "message" in bad


def test_interview_talking_points_invalid_theme() -> None:
    r = get_interview_talking_points("not_a_real_theme")
    assert r["status"] == "invalid_theme"
    assert "allowed" in r


def test_interview_technical_screen_theme() -> None:
    r = get_interview_talking_points("technical_screen")
    assert r["status"] == "success"
    assert r["theme"] == "technical_screen"
    assert len(r["points"]) >= 1
