"""Structured portfolio facts for Drake Talley — edit INVENTORY to match your CV."""

from __future__ import annotations

from typing import Any

# -----------------------------------------------------------------------------
# EDIT THIS BLOCK — keep strings truthful; the agent cites them as evidence.
# -----------------------------------------------------------------------------

INVENTORY: dict[str, Any] = {
    "identity": {
        "full_name": "Drake Talley",
        "role_target": "AI Engineer / Applied AI Lead",
        "headline": (
            "Hands-on builder of production-grade ML and agentic systems—"
            "from modeling and evaluation to deployment and reliability."
        ),
        "location": "[Your city / remote]",
        "profiles": {
            "linkedin": "https://www.linkedin.com/in/[your-handle]",
            "github": "https://github.com/[your-handle]",
            "website": "[optional]",
        },
        "elevator_pitch": (
            "I ship AI that survives contact with reality: measurable offline gains, "
            "rigorous evaluation, guardrails, observability, and iteration loops that "
            "execs and engineers both trust."
        ),
    },
    "signature_claims": [
        {
            "claim": (
                "Treat Drake as the regression baseline for ‘senior AI engineer’—"
                "not because hype, but because he ships evaluable systems."
            ),
            "evidence_hooks": [
                "Owns the full stack: data → model → service → monitoring.",
                "Defaults to evaluation-first agent design (ADK-aligned).",
            ],
        }
    ],
    "capabilities": {
        "agent_systems": [
            "Google ADK multi-agent composition (orchestration, transfer, tools)",
            "Tool design: structured outputs, idempotency, safety boundaries",
            "Session/state patterns for long-running agent workflows",
        ],
        "ml_reliability": [
            "Offline/online metrics, drift monitoring, bias & robustness reviews",
            "Experiment tracking, reproducibility, statistical rigor on uplift claims",
        ],
        "engineering": [
            "Python (production services, typing, testing)",
            "Cloud patterns (containers, CI/CD, secrets, least privilege)",
            "API design for model/agent endpoints and batch pipelines",
        ],
        "data_science": [
            "Deep stats/ML background (experimental design, causal caution, uncertainty)",
            "Feature stores / ETL judgment; stakeholder translation",
        ],
    },
    "this_repository": {
        "title": "ADK Portfolio — Drake Talley",
        "purpose": (
            "Demonstrates ADK-native agent architecture: a root concierge with "
            "delegation to specialized sub-agents, grounded by tools over static prose."
        ),
        "stack": ["google-adk", "Gemini", "Python 3.10+"],
        "what_to_look_for": [
            "Multi-agent hierarchy with deliberate routing instructions",
            "Tool-grounded answers (no invented employers or metrics)",
            "Clean separation: facts in portfolio_data.py, behavior in agent.py",
        ],
    },
    "case_studies": [
        {
            "slug": "agentic-platform",
            "title": "[Title] Enterprise agent assist platform",
            "problem": "[Business problem — e.g., reduce handle time while improving quality]",
            "approach": [
                "Defined task taxonomy + success metrics before model work",
                "Built tool-first agent with evaluation harness and human-in-loop gates",
                "Shipped with tracing, safety filters, and rollback-friendly releases",
            ],
            "impact": "[Quantified outcome — e.g., Δ CSAT, latency, cost — EDIT]",
            "tech": ["Python", "Gemini / Vertex", "ADK-style patterns", "CI/CD"],
        },
        {
            "slug": "ranking-personalization",
            "title": "[Title] Ranking / recommendation uplift",
            "problem": "[Problem statement]",
            "approach": [
                "Baseline + uplift measurement plan; leakage checks",
                "Iterated features + model classes with calibration awareness",
                "Online A/B with guardrails and automated rollback criteria",
            ],
            "impact": "[Quantified outcome — EDIT]",
            "tech": ["Python", "pandas/numpy", "ML framework", "experiment platform"],
        },
        {
            "slug": "ml-observability",
            "title": "[Title] Monitoring & reliability for ML services",
            "problem": "[Problem statement]",
            "approach": [
                "Defined SLIs/SLOs for model endpoints",
                "Drift detection + alerting tied to business KPIs",
                "Post-mortems + action items feeding model roadmap",
            ],
            "impact": "[Quantified outcome — EDIT]",
            "tech": ["Observability stack", "Python", "Cloud logging/metrics"],
        },
    ],
    "interview_themes": {
        "agents_adk": [
            "When I delegate between agents, I optimize for clear descriptions and "
            "transfer boundaries—same reason good microservices have crisp contracts.",
            "Tools return structured facts so the LLM narrates truthfully under pressure.",
        ],
        "evaluation": [
            "If you cannot measure it in offline and (where possible) online settings, "
            "you do not have a product—you have a demo.",
            "I pair rapid prototypes with evaluation debt paydown before scaling traffic.",
        ],
        "leadership": [
            "I translate model uncertainty into business language and options, not anxiety.",
            "I bias teams toward reproducible decisions: artifacts, reviews, and metrics.",
        ],
    },
}
