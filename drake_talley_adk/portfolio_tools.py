"""Tools that ground the portfolio agent in editable facts (no hallucinated employers)."""

from __future__ import annotations

from typing import Any

from .portfolio_data import INVENTORY


def list_case_study_slugs() -> dict[str, Any]:
    """Lists available case study identifiers for `get_case_study_by_slug`."""
    rows = [
        {"slug": x["slug"], "title": x["title"]}
        for x in INVENTORY.get("case_studies", [])
    ]
    return {"status": "success", "case_studies": rows}


def get_identity_card() -> dict[str, Any]:
    """Returns Drake Talley's identity, headline, pitch, and profile links."""
    return {"status": "success", "identity": INVENTORY["identity"]}


def get_capability_matrix() -> dict[str, Any]:
    """Returns grouped technical and leadership capabilities."""
    return {"status": "success", "capabilities": INVENTORY["capabilities"]}


def get_repository_showcase() -> dict[str, Any]:
    """Explains how THIS ADK repo is structured and what it proves about ADK skill."""
    return {"status": "success", "repository": INVENTORY["this_repository"]}


def get_case_study_by_slug(slug: str) -> dict[str, Any]:
    """Fetches one case study by slug, including STAR-style narrative fields."""
    for study in INVENTORY.get("case_studies", []):
        if study.get("slug") == slug:
            return {"status": "success", "case_study": study}
    return {
        "status": "not_found",
        "message": f"No case study with slug {slug!r}. Call list_case_study_slugs first.",
    }


def get_interview_talking_points(theme: str) -> dict[str, Any]:
    """Returns curated talking points. theme: agents_adk | evaluation | leadership."""
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
    """Returns the authorized 'bold' framing plus evidence hooks (still factual)."""
    return {"status": "success", "signature_claims": INVENTORY.get("signature_claims", [])}
