"""Tools that ground the portfolio agent in structured data (synthetic scenarios + ADK story)."""

from __future__ import annotations

from typing import Any

from .portfolio_data import INVENTORY


def get_portfolio_context() -> dict[str, Any]:
    """Returns audience, data policy (synthetic scenarios), and what this repo demonstrates."""
    return {"status": "success", "portfolio_context": INVENTORY["portfolio_context"]}


def get_verified_track_record() -> dict[str, Any]:
    """Returns résumé-backed experience: roles, metrics, projects, education, skills."""
    return {"status": "success", "verified_track_record": INVENTORY["verified_track_record"]}


def get_adk_expertise() -> dict[str, Any]:
    """Returns Drake's stated Google ADK expertise: patterns, primitives, deployment notes."""
    return {"status": "success", "adk_expertise": INVENTORY["adk_expertise"]}


def list_case_study_slugs() -> dict[str, Any]:
    """Lists synthetic case studies with industry labels for browsing."""
    rows = []
    for x in INVENTORY.get("case_studies", []):
        rows.append(
            {
                "slug": x["slug"],
                "title": x["title"],
                "industry": x.get("industry"),
                "synthetic": x.get("synthetic", True),
            }
        )
    return {"status": "success", "case_studies": rows}


def get_identity_card() -> dict[str, Any]:
    """Returns Drake Talley's identity, headline, pitch, and profile links."""
    return {"status": "success", "identity": INVENTORY["identity"]}


def get_capability_matrix() -> dict[str, Any]:
    """Returns grouped capabilities (ADK, evaluation, engineering, ML)."""
    return {"status": "success", "capabilities": INVENTORY["capabilities"]}


def get_repository_showcase() -> dict[str, Any]:
    """Explains how THIS repo is structured and what it proves about ADK skill."""
    return {"status": "success", "repository": INVENTORY["this_repository"]}


def get_case_study_by_slug(slug: str) -> dict[str, Any]:
    """Fetches one synthetic case study by slug (industry scenario + ADK patterns used)."""
    for study in INVENTORY.get("case_studies", []):
        if study.get("slug") == slug:
            return {"status": "success", "case_study": study}
    return {
        "status": "not_found",
        "message": f"No case study with slug {slug!r}. Call list_case_study_slugs first.",
    }


def get_interview_talking_points(theme: str) -> dict[str, Any]:
    """Returns curated talking points. theme: agents_adk | evaluation | leadership | hiring_manager."""
    themes = INVENTORY.get("interview_themes", {})
    key = theme.strip().lower()
    if key not in themes:
        return {
            "status": "invalid_theme",
            "allowed": list(themes.keys()),
            "message": "Pick a supported theme or ask the concierge for a recommendation.",
        }
    return {"status": "success", "theme": key, "points": themes[key]}


def get_signature_positioning() -> dict[str, Any]:
    """Returns positioning lines plus evidence hooks tied to this repository."""
    return {"status": "success", "signature_claims": INVENTORY.get("signature_claims", [])}
