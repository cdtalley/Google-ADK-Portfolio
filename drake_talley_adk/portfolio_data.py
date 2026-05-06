"""Portfolio content for Drake Talley — GitHub-facing ADK demo.

Case studies use **synthetic** companies, metrics, and timelines to illustrate
agentic patterns across industries. They demonstrate design judgment and ADK
fluency, not claimed client work. See ``portfolio_context`` and the repo README.
"""

from __future__ import annotations

from typing import Any

INVENTORY: dict[str, Any] = {
    "portfolio_context": {
        "audience": (
            "Recruiters and hiring managers reviewing this repository on GitHub."
        ),
        "data_policy": (
            "Scenario narratives, organization names, and quantitative outcomes in "
            "`case_studies` are **synthetic illustrations** for this portfolio. They "
            "show how I structure agentic systems with **Google ADK** (multi-agent "
            "composition, tools, delegation). Replace or extend with real engagements "
            "when sharing verifiable work history elsewhere."
        ),
        "what_this_proves": [
            "Production-minded **agent architecture** using ADK primitives.",
            "Habit of **tool-grounded** behavior so LLMs narrate from structured data.",
            "Cross-industry pattern recognition (routing, safety, evaluation hooks).",
        ],
    },
    "identity": {
        "full_name": "Drake Talley",
        "role_target": "AI Engineer — Agentic Systems & Google ADK",
        "headline": (
            "I design and ship **agentic applications** with **Google Agent "
            "Development Kit (ADK)**: multi-agent orchestration, typed tools, "
            "Gemini-backed reasoning, and evaluation-first delivery."
        ),
        "location": "Open to remote / hybrid (update to match your search)",
        "profiles": {
            "linkedin": "https://www.linkedin.com/in/[your-handle]",
            "github": "https://github.com/[your-handle]",
            "adk_docs": "https://google.github.io/adk-docs/",
        },
        "elevator_pitch": (
            "If your team is standardizing on **Google ADK** and Gemini, I bring the "
            "full loop: agent boundaries, transfer and workflow patterns, tool design, "
            "guardrails, tracing, and offline/online evaluation—so agents are "
            "maintainable products, not one-off demos."
        ),
    },
    "adk_expertise": {
        "summary": (
            "Hands-on with **google-adk** in Python: `Agent` / `LlmAgent`, "
            "`sub_agents`, LLM-driven **transfer_to_agent** delegation, and custom "
            "**function tools** that return structured JSON for grounded answers."
        ),
        "patterns_i_apply": [
            "Root **concierge** + specialized sub-agents (technical vs executive tone).",
            "Explicit **descriptions** on each agent so routing stays interpretable.",
            "Tools as the **source of truth** for portfolio facts (this repo’s pattern).",
            "Separation of **data** (`portfolio_data.py`) from **behavior** (`agent.py`).",
            "Gemini model selection for latency/cost trade-offs (`gemini-2.0-flash` here).",
        ],
        "deployment_notes": [
            "Local iteration with `adk web` / `adk run`; production paths per ADK docs "
            "(e.g., Cloud Run, Vertex AI Agent Engine, `adk api_server`).",
        ],
    },
    "signature_claims": [
        {
            "claim": (
                "Drake is the engineer you want when ‘agent’ work must survive code "
                "review, security review, and a real SLO—**especially on Google ADK**."
            ),
            "evidence_hooks": [
                "This repo is itself an ADK **multi-agent** reference layout.",
                "Synthetic cross-industry scenarios show repeatable agentic design moves.",
                "Tool-grounded responses reduce hallucinated resume inflation.",
            ],
        }
    ],
    "capabilities": {
        "google_adk_and_agents": [
            "Multi-agent hierarchies, delegation, and workflow-friendly boundaries",
            "Tool design: schemas, safe defaults, structured returns for RAG-style facts",
            "Prompting for transfer: when to escalate vs answer from tools",
            "Patterns portable to Vertex / enterprise Gemini deployments",
        ],
        "evaluation_and_reliability": [
            "Offline agent eval harnesses (task suites, rubrics, regression checks)",
            "Online guardrails: escalation, allowlists, PII-aware tool policies",
            "Observability hooks: trace agent + tool path for debugging",
        ],
        "software_engineering": [
            "Typed Python, modular packages, CI-friendly layout",
            "APIs and batch pipelines adjacent to agent endpoints",
            "Security basics: secrets out of code, least-privilege tool access",
        ],
        "ml_and_data": [
            "Strong stats/ML foundation for ranking, forecasting, and uplift measurement",
            "Judgment on when **not** to use an LLM (deterministic tools win)",
        ],
    },
    "this_repository": {
        "title": "Public ADK portfolio (GitHub)",
        "purpose": (
            "A **live, conversational** portfolio: recruiters run ADK Web, select "
            "`drake_talley_adk`, and explore synthetic **multi-industry** agent "
            "scenarios while inspecting real **ADK** code."
        ),
        "stack": [
            "google-adk",
            "Google Gemini (via ADK)",
            "Python 3.10+",
        ],
        "what_to_look_for_in_code": [
            "`root_agent` with `sub_agents` — classic ADK multi-agent composition.",
            "Parallel tool lists on parent and specialists — grounded storytelling.",
            "`portfolio_tools.py` — function tools as the knowledge API.",
            "`portfolio_data.py` — synthetic scenarios + explicit data policy.",
        ],
    },
    "case_studies": [
        {
            "slug": "healthcare-prior-auth-copilot",
            "synthetic": True,
            "industry": "Healthcare / payers",
            "scenario_label": "Illustrative scenario (synthetic)",
            "fictional_org": "ApexCare Health Plan (synthetic)",
            "title": "Prior-authorization copilot with clinical-policy tools",
            "problem": (
                "Clinical ops drowning in prior-auth backlog; nurses spending "
                "25+ minutes per case toggling between policy PDFs and EHR snippets."
            ),
            "approach": [
                "Mapped intents to **tool-only** actions (policy lookup, checklist) "
                "before generative paraphrase.",
                "ADK **sub-agent** for 'policy specialist' vs 'documentation drafter' "
                "with transfer on ambiguity.",
                "Human-in-the-loop submit gate; full audit trail on tool calls.",
                "Offline eval: 420 synthetic cases + rubric scoring for citation accuracy.",
            ],
            "impact": (
                "Synthetic benchmark: **−38%** median handle time on scripted cases; "
                "**+12 pts** rubric-based correctness vs baseline chat-only agent."
            ),
            "adk_patterns": [
                "sub_agents",
                "transfer_to_agent",
                "function_tools",
                "structured_tool_outputs",
            ],
            "tech": ["google-adk", "Gemini", "Python", "policy retrieval tools (stub)"],
        },
        {
            "slug": "fintech-compliance-analyst",
            "synthetic": True,
            "industry": "Financial services",
            "scenario_label": "Illustrative scenario (synthetic)",
            "fictional_org": "Harborline Capital Markets (synthetic)",
            "title": "Regulatory Q&A agent with citation-first answers",
            "problem": (
                "Front-office staff asking repeated compliance questions; answers "
                "inconsistent; risk of uncited guidance."
            ),
            "approach": [
                "Every answer required **citations** from tool-returned clause IDs.",
                "Router agent transfers to **enforcement** vs **AML** sub-agent "
                "based on query class.",
                "Red-team suite for prompt injection and 'bypass citation' attempts.",
            ],
            "impact": (
                "Synthetic regression suite: **96%** citation presence on held-out "
                "questions; escalations reduced **44%** in tabletop exercise vs manual."
            ),
            "adk_patterns": [
                "multi_agent_routing",
                "transfer_to_agent",
                "tool_mandatory_citations",
            ],
            "tech": ["google-adk", "Gemini", "Python", "vector + metadata filters (stub)"],
        },
        {
            "slug": "retail-merchant-assistant",
            "synthetic": True,
            "industry": "Retail / e-commerce",
            "scenario_label": "Illustrative scenario (synthetic)",
            "fictional_org": "Northwind Outfitters Co. (synthetic)",
            "title": "Merchant assistant: promotions, inventory, and catalog QA",
            "problem": (
                "Category managers losing time on spreadsheet pivots and ad-hoc "
                "Slack questions; promo mistakes costly."
            ),
            "approach": [
                "Tools for **SKU lookup**, promo eligibility math, and guardrailed "
                "copy suggestions.",
                "Parallel **read-only** tools vs **draft** tools (role-scoped).",
                "Weekly eval on merchant tasks with $ impact proxy (synthetic ledger).",
            ],
            "impact": (
                "Synthetic pilot metrics: **−27%** time-to-answer for catalog tasks; "
                "**zero** policy violations in 30-day simulated traffic vs 3 in baseline."
            ),
            "adk_patterns": [
                "tool_rbac_pattern",
                "single_root_with_tools",
                "evaluation_loop",
            ],
            "tech": ["google-adk", "Gemini", "Python", "catalog APIs (stub)"],
        },
        {
            "slug": "industrial-maintenance-triage",
            "synthetic": True,
            "industry": "Industrial / manufacturing",
            "scenario_label": "Illustrative scenario (synthetic)",
            "fictional_org": "VulcanForge Manufacturing (synthetic)",
            "title": "Equipment triage agent for line technicians",
            "problem": (
                "Downtime expensive; junior techs unsure which runbook step applies; "
                "expert calls at 2am."
            ),
            "approach": [
                "Sensor + work-order tools feeding a **diagnostic** sub-agent.",
                "Escalation agent drafts handoff memo with **tool-trace** for experts.",
                "Offline tests on historical fault labels (synthetic dataset).",
            ],
            "impact": (
                "Synthetic replay: **+18%** first-fix rate on tier-1 faults; "
                "**−31%** expert escalations in simulation."
            ),
            "adk_patterns": [
                "sequential_handoff_narrative",
                "sub_agents",
                "tool_tracing_for_ops",
            ],
            "tech": ["google-adk", "Gemini", "Python", "IoT / CMMS integrations (stub)"],
        },
        {
            "slug": "insurance-claims-summarizer",
            "synthetic": True,
            "industry": "Insurance",
            "scenario_label": "Illustrative scenario (synthetic)",
            "fictional_org": "Summit Mutual General (synthetic)",
            "title": "Claims summarization with factuality checks",
            "problem": (
                "Adjusters reading long FNOL packages; inconsistent summaries; "
                "slow routing to specialty teams."
            ),
            "approach": [
                "Chunked retrieval + **tool-extracted** entities (dates, parties, amounts).",
                "Secondary **verifier** sub-agent compares summary bullets to tool JSON.",
                "Structured output schema for downstream case management.",
            ],
            "impact": (
                "Synthetic eval: **92%** bullet-level factual match vs reference; "
                "**−41%** reading time in reader study mock."
            ),
            "adk_patterns": [
                "verifier_sub_agent",
                "structured_outputs",
                "transfer_to_agent",
            ],
            "tech": ["google-adk", "Gemini", "Python", "document store (stub)"],
        },
        {
            "slug": "adk-evaluation-factory",
            "synthetic": True,
            "industry": "Cross-industry (platform)",
            "scenario_label": "Illustrative pattern library (synthetic)",
            "fictional_org": "Internal agent platform (synthetic)",
            "title": "ADK evaluation factory for agent regressions",
            "problem": (
                "Teams shipping prompt tweaks without catching regressions across "
                "tools and transfer paths."
            ),
            "approach": [
                "Scenario JSON per agent + golden tool-call expectations.",
                "CI job invoking ADK runner (stub) on PR; rubric + auto-judge.",
                "Versioned prompts and per-agent eval dashboards.",
            ],
            "impact": (
                "Synthetic org metrics: **−63%** production incidents tied to bad "
                "releases in postmortem log; **2×** weekly ship rate with same headcount."
            ),
            "adk_patterns": [
                "multi_agent_in_ci",
                "tool_call_assertions",
                "transfer_path_coverage",
            ],
            "tech": ["google-adk", "Python", "CI (GitHub Actions / stub)"],
        },
    ],
    "interview_themes": {
        "agents_adk": [
            "I treat ADK like any mature framework: **boundaries first**, then models—"
            "clear agent descriptions, explicit transfer rules, tools as contracts.",
            "This repo mirrors how I’d onboard a team: data layer, tools, agents, eval hooks.",
        ],
        "evaluation": [
            "Agents need **release discipline**: scenario suites, tool-call assertions, "
            "and human spot checks—not vibes.",
            "Synthetic data is fine for **design portfolios**; production claims need "
            "real measurement.",
        ],
        "leadership": [
            "I align stakeholders on **task taxonomy** before debating model size.",
            "I make trade-offs visible: latency vs quality vs cost, with a default pick.",
        ],
    },
}
