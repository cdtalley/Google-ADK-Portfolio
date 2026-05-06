# Drake Talley — AI / ML on GCP · GenAI · Google ADK

**Senior data scientist** who ships **production ML** where stakes are high: **20TB+** federal fraud pipelines, **national** education analytics on **Vertex AI**, **IoT** reliability at scale—and **enterprise GenAI** (including **Morgan Stanley** search on **BigQuery**).  

**Founder, PrismBase AI LLC** (2026–present). **Builder**, not deck-builder: full-stack applied AI, multi-agent orchestration, and this **live [Google ADK](https://google.github.io/adk-docs/)** portfolio you can run in a browser.

| [LinkedIn](https://www.linkedin.com/in/drake-talley) | [GitHub](https://github.com/cdtalley) | [draketalley.ai](https://draketalley.ai/) | **drake.talley.ai@gmail.com** | **+1 (706) 264-2708** |

---

## Why hiring managers stop scrolling

- **Wall Street + federal + cloud-native:** Delivered **RAG** (LangChain + GPT-3) on **Google BigQuery** for **Morgan Stanley** (via Infosys); **+30%** fraud-detection lift on **20TB+** workloads with federal-grade constraints; **DAQC / governance** at **Wells Fargo**; **fraud** models at **US Bank**; **Chaos Engineering** leadership reporting at **Verizon** (managed an **8-person** offshore team).
- **Owns the full ML product loop:** At **SentriLock**, **2.5TB+** production data—**Vertex AI**, **BigQuery**, **Cloud Functions**; **80%** reduction in a critical **field-device failure** class; **35%** downtime reduction; **50%** cloud cost reduction; **30%** faster model rollout (**Vertex AI Pipelines** + **Cloud Composer**).
- **Education / CRM scale:** **Robert Half → national higher-ed client**—end-to-end **Vertex AI Workbench** pipelines for **lead scoring** + **student retention**; reusable feature-engineering frameworks; classical ML with explainability under **sparse data** realities.
- **Agentic AI (today):** Public [**fraud-agent-orchestrator**](https://github.com/cdtalley/fraud-agent-orchestrator)—**Intake → Risk → Policy** multi-agent flow, **FastAPI**, **OPA**, tamper-evident audit trail, **PII minimization**, optional **Ollama** for air-gapped. **This repo** proves the same architectural discipline on **Google ADK** (Gemini, `sub_agents`, tool-grounded answers).

**Education:** **University of Georgia**, B.S., GPA **3.8** · **Thinkful** Data Science intensive  

**Location:** Acworth, GA — **remote-friendly**

---

## This repository (Google ADK)

Not a slideshow—a **runnable agent app**:

- **Multi-agent** `root_agent` + specialists (`technical_proof`, `executive_voice`) with LLM-driven **transfer**.
- **RevOps lead triage** subsystem (`revops_lead_orchestrator`): addresses a **real** operating problem—**prioritizing finite sales capacity on policy-safe, high-intent inbound leads**—using **function tools** over a **synthetic** CRM (`revenue_ops_data.py`). Specialists: **policy / scoring / next-best-action**.
- **Tool-grounded** answers: résumé facts live in `portfolio_data.py` → exposed via `portfolio_tools.py` so the model **quotes your real wins**, not hallucinated ones.
- **Synthetic case studies** (healthcare, fintech, retail, etc.) are **deliberate ADK design exercises**—clearly separated from **verified** employment data.

### Run it locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Copy env.example → .env and set GOOGLE_API_KEY (https://aistudio.google.com/app/apikey)
adk web --port 8000
```

Open `http://localhost:8000` → select **`drake_talley_adk`**.

### 5-minute reviewer path

**Google ADK in one line:** An `Agent` combines a Gemini model, **instructions**, **function tools** (Python callables returning structured data), and optional **`sub_agents`**. Delegation is **`transfer_to_agent`**: the model chooses when to hand off to a specialist instead of hard-coding orchestration in application code.

**Copy-paste prompts** (each proves a different capability):

1. **Verified résumé grounding** — “Use **get_verified_track_record** and give three bullets on Drake’s SentriLock outcomes (field failure, downtime, cloud cost). Do not invent metrics.”
2. **Synthetic case study (ADK patterns)** — “Call **list_case_study_slugs**, then **get_case_study_by_slug** for `fintech-compliance-analyst`. Summarize the approach and label it **synthetic / illustrative**.”
3. **RevOps multi-agent + CRM tools** — “For **revops_lead_orchestrator**: triage lead **LD-10043**—policy/eligibility, priority score and tier, and next-best action. Say explicitly that leads in `revenue_ops_data.py` are **demo records**.”

**File map** (if you only read a few files):

| File | What it shows |
|------|----------------|
| [`drake_talley_adk/agent.py`](drake_talley_adk/agent.py) | `root_agent`, portfolio specialists, `sub_agents`, shared portfolio tools |
| [`drake_talley_adk/revenue_ops_agents.py`](drake_talley_adk/revenue_ops_agents.py) | RevOps orchestrator + policy / scoring / action subgraph |
| [`drake_talley_adk/portfolio_tools.py`](drake_talley_adk/portfolio_tools.py) | Tool API over résumé + case-study data |
| [`drake_talley_adk/revenue_ops_tools.py`](drake_talley_adk/revenue_ops_tools.py) | Deterministic CRM tools; partitioned tool lists per specialist |
| [`drake_talley_adk/portfolio_data.py`](drake_talley_adk/portfolio_data.py) | **Verified** track record vs **synthetic** vignettes (data only) |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Why two agent hierarchies, tool rules, production next steps |

**Try asking:** “What business problem does the RevOps agent solve?” “Triage lead **LD-10043**—policy, score, and next action.” “Summarize Drake’s verified Vertex wins.” “How is this ADK repo structured?”

---

## More code (selected)

| Repo | What it shows |
|------|----------------|
| [**Student-Prediction**](https://github.com/cdtalley/Student-Prediction) | Retention + lead ensemble (**XGBoost** / **LightGBM**), **FastAPI**, **Next.js 14**, **Superset**, Docker |
| [**LangChain Enterprise Dashboard**](https://github.com/cdtalley/LangChain_Enterprise_Dashboard) | Enterprise **multi-agent RAG**, hybrid retrieval, Azure ML, security hardening |
| [**Data-Science-Portfolio**](https://github.com/cdtalley/Data-Science-Portfolio) | Leakage-safe sklearn pipelines, SHAP, Streamlit, LangChain+RAG demo |
| [**VisionDetect**](https://github.com/cdtalley/AI-and-ComputerVision-Development-Project-VisionDetect-) | Modular CV: config-driven training, REST JSON inference |

---

## Disclosure

Synthetic vignettes in `case_studies` are **fictional** scenarios for **ADK** pattern demos. **RevOps** companies/leads in `revenue_ops_data.py` are **demo records** for a real-world triage pattern. **Employment, clients, and quantitative claims** in `verified_track_record` are transcribed from Drake’s résumé for tool-grounded responses.

ADK **Web** is [development-only per Google](https://google.github.io/adk-docs/); production = Cloud Run, Vertex AI Agent Engine, or `adk api_server` patterns from ADK docs.

---

**If you need someone who can talk to executives *and* ship agents on Vertex/Gemini: you’re in the right repo.**
