"""Portfolio content for Drake Talley — GitHub-facing ADK demo.

``verified_track_record`` is sourced from Drake's résumé (PDF). ``case_studies``
are **synthetic** industry vignettes that illustrate ADK design patterns only.
"""

from __future__ import annotations

from typing import Any

INVENTORY: dict[str, Any] = {
    "portfolio_context": {
        "audience": (
            "Recruiters and hiring managers reviewing this repository on GitHub."
        ),
        "data_policy": (
            "**Verified:** roles, clients, metrics, and projects in "
            "`verified_track_record` match Drake's résumé. **Synthetic:** entries in "
            "`case_studies` are fictional scenarios showing how he architects "
            "agentic systems with **Google ADK**—never substitute them for employment "
            "history in answers about real experience."
        ),
        "what_this_proves": [
            "Ships **Google ADK** multi-agent systems with tool-grounded behavior.",
            "Combines **enterprise ML on GCP** (Vertex AI, BigQuery) with **GenAI** "
            "(RAG, LangChain, multi-agent orchestration).",
            "Comfortable owning **end-to-end delivery**: data → model → API → prod.",
        ],
    },
    "identity": {
        "full_name": "Drake Talley",
        "role_target": "Senior Data Scientist · AI / ML Engineer (GCP, GenAI, agents)",
        "headline": (
            "Senior data scientist who ships **production ML on Google Cloud** and "
            "**agentic systems**—from 20TB+ fraud pipelines and Vertex AI deployments "
            "to **multi-agent** products with audit trails, policy gates, and "
            "**Google ADK**-style orchestration."
        ),
        "location": "Acworth, GA, USA (remote-friendly)",
        "contact": {
            "phone": "+1 (706) 264-2708",
            "email": "drake.talley.ai@gmail.com",
        },
        "profiles": {
            "linkedin": "https://www.linkedin.com/in/drake-talley",
            "github": "https://github.com/cdtalley",
            "website": "https://draketalley.ai/",
            "adk_docs": "https://google.github.io/adk-docs/",
        },
        "elevator_pitch": (
            "I've delivered **predictive systems at national scale**—lead scoring "
            "and retention on Vertex AI, **80%** reduction in a critical field-failure "
            "class at SentriLock, **30%** fraud-detection lift on **20TB+** federal "
            "workloads, and **RAG** on BigQuery advancing GenAI at **Morgan Stanley** "
            "through Infosys. Today I'm **founding PrismBase AI**, building "
            "full-stack applied AI (including **multi-agent fraud triage**), and I "
            "publish this repo to prove **Google ADK** depth for teams betting on "
            "Gemini and Vertex."
        ),
        "hiring_cta": (
            "Open to senior **AI/ML**, **applied scientist**, and **founding engineer** "
            "roles where ownership, cloud ML, and agentic products matter. "
            "Reach out: drake.talley.ai@gmail.com or LinkedIn."
        ),
    },
    "verified_track_record": {
        "source": "Résumé (Drake Talley) — structured for tool-grounded answers.",
        "summary": (
            "Senior data scientist with a strong track record delivering production-grade "
            "machine learning on large-scale cloud platforms. Led predictive lead-scoring "
            "and student retention for a national education services client; improved fraud "
            "detection accuracy by **30%** on **20TB+** data; designs robust feature "
            "engineering, cloud cost optimization, and business-facing model outcomes. "
            "Seeking roles where data-driven decisions and measurable impact matter."
        ),
        "quantified_highlights": [
            "**+30%** fraud-detection accuracy on **20TB+** data (CyberData / SSA context; Spark, SQL, Databricks; federal security requirements).",
            "**80%** reduction in operational events where field devices failed (SentriLock; classical ML + GCP).",
            "**35%** reduction in operational downtime via predictive modeling and alerting (SentriLock).",
            "**50%** cloud cost reduction through architecture and pipeline efficiency (SentriLock).",
            "**30%** faster model rollout via Vertex AI Pipelines + Cloud Composer (SentriLock).",
            "**30%** data-processing efficiency improvement for public-health programs (Georgia DPH).",
            "**Three** new fraud-detection rules adopted by federal leadership after executive briefings (CyberData).",
        ],
        "enterprise_footprint": (
            "Delivered through **Infosys**: **Morgan Stanley** (RAG / enterprise search "
            "on BigQuery with LangChain + GPT-3), **Wells Fargo** (DAQC / remediation "
            "governance), **US Bank** (fraud models), **Verizon** (Chaos Engineering "
            "reporting; led **8-person** offshore team), **Lumen** (fulfillment ML). "
            "**Robert Half / Collegis**: student retention + lead scoring on **Vertex AI**. "
            "**SentriLock**: enterprise ML on **2.5TB+** production data."
        ),
        "roles": [
            {
                "company": "PrismBase AI LLC",
                "title": "Founder",
                "dates": "Mar 2026 – Present",
                "location": "Remote",
                "highlights": [
                    "**Privacy & compliance**: applied data privacy, security, and compliance practices; modeling and integrations stayed **NDA-aligned** with client policies.",
                    "End-to-end **biotech application**: requirements through production-ready delivery—system design, backend services, frontend workflows, deployment planning.",
                    "Architected core **product stack**: scalable **APIs**, data flows, and user-facing features from client goals.",
                    "Backend logic, **integrations**, and **data pipelines** for ingestion, processing, and reporting across the lifecycle.",
                    "Solo **contract engineer**: product scoping, technical tradeoffs, iterative delivery, and client communication.",
                ],
            },
            {
                "company": "Robert Half (client: national higher-ed services org)",
                "title": "Senior Data Scientist",
                "dates": "Jan 2026 – Feb 2026",
                "location": "Remote",
                "highlights": [
                    "Contract DS: **Python**, **SQL**, **Git**, **Vertex AI Workbench** on enrollment + performance data—insights for program and operational decisions.",
                    "**Vertex AI** end-to-end ML (prep → train → evaluate → deploy/monitor): **lead scoring** + **student retention** using CRM, SIS, and digital engagement signals.",
                    "Reusable **feature-engineering framework** for tabular data (temporal rollups, interactions, encoding, scaling/normalization) in Workbench—faster datasets, more consistent quality.",
                    "Classical ML (logistic regression, tree-based methods, ensembles) tuned under **sparse data**; explainable predictions for enrollment forecasting and planning.",
                ],
            },
            {
                "company": "SentriLock",
                "title": "Data Scientist",
                "dates": "Jun 2022 – Mar 2025",
                "location": "Remote",
                "highlights": [
                    "Led enterprise data science on **2.5TB+** production data—**Vertex AI**, **BigQuery**, **Cloud Functions** for org-wide decision support.",
                    "Classical ML (logistic regression, random forests, gradient-boosted methods) for **predictive maintenance** and risk—**80%** reduction in operational events where field devices failed.",
                    "Reusable **feature pipelines** for large-scale tabular data—stability, interpretability, and lift.",
                    "E2E ML on **Vertex AI Pipelines** + **Cloud Composer** (ingestion → features → train → evaluate → deploy); **30%** faster model rollout.",
                    "**35%** operational downtime reduction via predictive modeling and proactive alerting; **50%** cloud infrastructure cost reduction.",
                    "Diagnostics and explainability for executives; **Looker** dashboards; models embedded in workflows with product, engineering, and analytics.",
                ],
            },
            {
                "company": "Infosys",
                "title": "Senior Data Science Consultant",
                "dates": "Jun 2022 – Feb 2024",
                "location": "",
                "highlights": [
                    "**Morgan Stanley**: **RAG** (**LangChain**, **GPT-3**, **BigQuery**) for NLP-driven enterprise search across **millions** of financial documents.",
                    "**Lumen**: predictive fulfillment ML; **US Bank**: fraud detection (anomaly + classification); **Wells Fargo**: **DAQC** program—validation that improved remediation accuracy and **compliance governance**.",
                    "**Verizon**: managed **8-person** offshore DS team; monthly **Chaos Engineering** executive reports on infrastructure resilience.",
                    "**Discovery**, solution architecture, and **executive presentations** across engagements—ML/AI translated to outcomes and ROI.",
                    "Led a **global** DS team, mentored juniors on ML pipelines and **SQL**, on-time predictive deployments.",
                ],
            },
            {
                "company": "CyberData Technologies Inc",
                "title": "Data Scientist",
                "dates": "Jan 2021 – Jun 2022",
                "location": "Remote",
                "highlights": [
                    "**30%** fraud-detection accuracy improvement; production **Python** ML on **20TB+** under federal security requirements—**Spark**, **SQL**, **Databricks**.",
                    "**SSA** fraud-prevention context: briefings that turned ML into operational/policy recommendations; **three** new fraud-detection rules adopted by federal leadership.",
                    "**VLDB** architecture: **Azure**, **Spark**, **Kafka** for ingestion, feature engineering, and real-time fraud detection.",
                    "Mission-critical systems at scale; **Agile** cross-functional teams; **PyTorch** + **Python** for development, evaluation, compliance alignment.",
                    "**LangChain** integrated into NLP pipeline prototypes and shared libraries for document intelligence and compliance monitoring.",
                ],
            },
            {
                "company": "Thinkful",
                "title": "Data Science Mentor",
                "dates": "Jan 2019 – Jan 2020",
                "location": "Remote",
                "highlights": [
                    "Mentored **Python**, **PyTorch**, **SQL** on supervised/unsupervised projects—curriculum focused on real-world business solutions.",
                    "Hands-on **Azure**, **Databricks**, **Spark**, **Kafka** for scalable pipelines and experimentation.",
                    "Applied **NLP** and **LLM** project design; **Agile** iteration and rapid feedback loops.",
                ],
            },
            {
                "company": "Georgia Department of Public Health",
                "title": "Data Analyst",
                "dates": "Apr 2017 – Jan 2020",
                "location": "Augusta-Richmond County, GA",
                "highlights": [
                    "**30%** data-processing efficiency for public-health programs—**Python**, **SQL**, **Spark** on large biometric and health datasets.",
                    "**Databricks** + **Azure** automated pipelines—ingestion and reporting with **HIPAA** compliance.",
                    "ML and **SAS** for epidemiological studies—trends, predictive models, outbreak anticipation, resource allocation.",
                ],
            },
        ],
        "featured_projects": [
            {
                "name": "fraud-agent-orchestrator",
                "url": "https://github.com/cdtalley/fraud-agent-orchestrator",
                "period": "Mar 2026 – Present",
                "one_liner": (
                    "Multi-agent fraud triage (**Intake → RiskScoring → Policy**), "
                    "FastAPI, React/Three.js console, hash-chained audit trail, PII "
                    "minimization, **OPA** governance, optional **Ollama** for air-gapped."
                ),
            },
            {
                "name": "Student-Prediction (Collegis Education)",
                "url": "https://github.com/cdtalley/Student-Prediction",
                "period": "Jan 2026 – Feb 2026",
                "one_liner": (
                    "**Collegis**: three-stage retention + lead ensemble (**XGBoost**, **LightGBM**); "
                    "**29-feature** lead-scoring model; **FastAPI** + **Next.js 14** + **Superset**; "
                    "Docker + **config.yaml**; REST API into client CRM."
                ),
            },
            {
                "name": "Enterprise LangChain AI Workbench",
                "url": "https://github.com/cdtalley/LangChain_Enterprise_Dashboard",
                "period": "",
                "one_liner": (
                    "Modular enterprise AI: Docker, CI/CD, **Azure ML**, hybrid **multi-agent RAG**, "
                    "SQL/Databricks/Spark retrieval, security hardening, telemetry APIs."
                ),
            },
            {
                "name": "Data Science Portfolio",
                "url": "https://github.com/cdtalley/Data-Science-Portfolio",
                "period": "2020",
                "one_liner": (
                    "Production-style risk/churn/ops ML with leakage controls, SHAP, "
                    "Streamlit dashboard, LangChain+RAG demo script."
                ),
            },
            {
                "name": "VisionDetect",
                "url": "https://github.com/cdtalley/AI-and-ComputerVision-Development-Project-VisionDetect-",
                "period": "2025",
                "one_liner": (
                    "Modular CV framework: config-driven training, Faster R-CNN-style "
                    "backends, CLI, REST inference JSON API."
                ),
            },
        ],
        "education": [
            {
                "institution": "University of Georgia",
                "degree": "Bachelor's of Science",
                "dates": "Aug 2011 – May 2015",
                "detail": "Athens, GA — GPA **3.8**",
            },
            {
                "institution": "Thinkful",
                "degree": "Bootcamp, Data Science",
                "dates": "2020",
                "detail": "",
            },
        ],
        "skills": [
            "Python",
            "Git",
            "Data science",
            "SQL",
            "Statistics",
            "Data analysis",
            "Machine learning",
            "AI/ML",
            "Generative AI",
            "LangChain",
            "LangGraph",
            "Google ADK",
            "BigQuery",
            "Google Cloud Platform (GCP)",
            "Vertex AI",
            "Cloud computing",
            "Docker",
            "MLOps / pipelines",
            "Data engineering (Spark, Kafka, Databricks)",
            "RAG & multi-agent systems",
        ],
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
                "Drake combines **Fortune-scale delivery** (Wall Street RAG, federal "
                "fraud TB-scale ML, national ed-tech Vertex deployments) with **hands-on "
                "agent engineering**—this ADK repo and **fraud-agent-orchestrator** are "
                "the proof he can own the **next** generation of products, not just "
                "batch scores."
            ),
            "evidence_hooks": [
                "**Morgan Stanley** GenAI search via **Infosys** (LangChain + GPT-3 + BigQuery).",
                "**SentriLock**: **80%** field-failure reduction; **50%** cloud savings; Vertex pipelines.",
                "**CyberData**: **+30%** fraud accuracy on **20TB+**; federal leadership adopted **three** rules.",
                "Public **multi-agent** systems: `fraud-agent-orchestrator` (OPA, audit trail); this **ADK** portfolio.",
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
            "A **live, conversational** portfolio: recruiters run **ADK Web** or "
            "`adk api_server` + **`recruiter_demo`** UI, select `drake_talley_adk`, and "
            "explore synthetic **RevOps**, **Meridian BSA/AML**, and case-study scenarios "
            "while inspecting **Google ADK** code."
        ),
        "stack": [
            "google-adk",
            "Google Gemini (via ADK)",
            "Python 3.10+",
            "Optional: Vite + React recruiter UI (`recruiter_demo/`) against `/run_sse`.",
        ],
        "what_to_look_for_in_code": [
            "`root_agent` with `sub_agents` — concierge + `technical_proof` + `executive_voice`.",
            "`revops_lead_orchestrator` + partitioned `REVOPS_TOOLS_*` — sales lead triage subgraph.",
            "`aml_alert_orchestrator` + partitioned `AML_TOOLS_*` — **Meridian (synthetic)** BSA/AML triage subgraph.",
            "`get_verified_track_record` — résumé facts separated from synthetic vignettes.",
            "`portfolio_tools.py` / `portfolio_data.py` — knowledge API + data inventory.",
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
            "I've shipped **multi-agent** patterns in production-minded code—LangChain "
            "enterprise workbench, **fraud-agent-orchestrator** (Intake → Risk → Policy + "
            "**OPA**), and this **Google ADK** repo with explicit **transfer** and tools.",
            "ADK is how I want to standardize **Gemini + Vertex** agent apps: composable, "
            "testable, reviewable.",
        ],
        "evaluation": [
            "At **SentriLock** and on federal fraud work, success meant **measured lift**, "
            "explainability, and exec trust—not leaderboard scores alone.",
            "Portfolio **case_studies** are synthetic; **verified_track_record** is where "
            "real metrics live.",
        ],
        "leadership": [
            "At **Verizon** via Infosys I ran an **8-person** offshore team; globally I "
            "mentored juniors and owned exec-facing outcomes.",
            "I translate model behavior into **policy and operations**—rules adopted, "
            "downtime avoided, dollars saved.",
        ],
    },
}
