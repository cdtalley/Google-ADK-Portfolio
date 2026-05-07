# Drake Talley — AI / ML on GCP · GenAI · Google ADK

**Senior data scientist** who ships **production ML** where stakes are high: **20TB+** federal fraud pipelines, **national** education analytics on **Vertex AI**, **IoT** reliability at scale—and **enterprise GenAI** (including **Morgan Stanley** search on **BigQuery**).  

**Founder, PrismBase AI LLC** (2026–present). **Builder**, not deck-builder: full-stack applied AI, multi-agent orchestration, and this **live [Google ADK](https://google.github.io/adk-docs/)** portfolio you can run in a browser.

| [LinkedIn](https://www.linkedin.com/in/drake-talley) | [GitHub](https://github.com/cdtalley) | [draketalley.ai](https://draketalley.ai/) | **drake.talley.ai@gmail.com** | **+1 (706) 264-2708** |

---

## Highlights

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
- **Meridian BSA/AML alert triage** (`aml_alert_orchestrator`): **Meridian Trust & Savings (synthetic)**—**real-class** financial-crime ops problem (**analyst throughput**, **escalation**, **auditable reasons**) over **synthetic** alerts (`aml_alert_data.py`). Specialists: **policy / risk severity / disposition** with partitioned `AML_TOOLS_*`.
- **Web UI** (`recruiter_demo/`): **Vite + React** chat plus **trace replay** of tool calls and agent authors against `adk api_server` (`POST /run`).
- **No Google bill required to try it:** when **`GOOGLE_API_KEY` is missing or still a placeholder** (e.g. `YOUR_..._HERE`), agents use **`ollama/llama3.2:latest`** via ADK’s **LiteLLM** integration (`drake_talley_adk/portfolio_model.py`). Install [Ollama](https://ollama.com/), `ollama pull llama3.2`, keep **`ollama serve`** running. A **real** long key selects **`gemini-2.0-flash`**.
- **Tool-grounded** answers: résumé facts live in `portfolio_data.py` → exposed via `portfolio_tools.py` so the model **quotes your real wins**, not hallucinated ones.
- **Synthetic case studies** (healthcare, fintech, retail, etc.) are **deliberate ADK design exercises**—clearly separated from **verified** employment data.

### Run it locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**LLM backend (pick one):**

| Mode | What to do |
|------|------------|
| **Local / no Google API** | Install [Ollama](https://ollama.com/), run `ollama pull llama3.2`, keep **`ollama serve`** running. **Delete** `GOOGLE_API_KEY` from `.env` or leave only a placeholder — fake/short keys are ignored so routing stays on **`ollama/llama3.2:latest`**. |
| **Gemini API** | Copy **`env.example`** → **`.env`** and set **`GOOGLE_API_KEY`** ([AI Studio](https://aistudio.google.com/app/apikey)). Agents use **`gemini-2.0-flash`**. |

Override anytime: **`PORTFOLIO_ADK_MODEL`** (see `env.example` and `drake_talley_adk/portfolio_model.py`).

```powershell
adk web --port 8000
```

Open `http://localhost:8000` → select **`drake_talley_adk`**.

### Web UI (`recruiter_demo`)

Terminal **A** — from this repo root (folder that contains `drake_talley_adk/`):

```powershell
.\.venv\Scripts\Activate.ps1
# Optional: GOOGLE_API_KEY in .env for Gemini; omit for local Ollama (see table above)
adk api_server --port 8000
```

Terminal **B**:

```powershell
cd recruiter_demo
npm install
npm run dev
```

Open **`http://localhost:5173`** (use **`npm run dev`** — do not open `file://` or a static build without the proxy). The dev server **proxies** `/run_sse` and `/apps` to ADK and **strips the `Origin` header** so you avoid ADK’s `403 Forbidden: origin not allowed` on POST.

Use **preset prompts** for one-click demos. The UI calls ADK **`POST /run`** (full event list per turn), then **replays** each event into the **Trace** panel so you see tools and agents step-by-step—**reliable** behind Vite’s proxy (SSE streaming is optional and often buffered in dev).

**If you still see “origin not allowed”:** restart Vite after `git pull`, or run ADK with explicit CORS:  
`adk api_server --port 8000 --allow_origins http://localhost:5173 --allow_origins http://127.0.0.1:5173`

**If the UI shows HTTP 500 / “Internal Server Error”:** check the **`adk api_server`** traceback. **Ollama:** `ollama serve` running, `ollama pull llama3.2` done, and **no leftover `GOOGLE_API_KEY`** that looks like a real key (or set **`PORTFOLIO_ADK_MODEL=ollama/llama3.2:latest`** to force local). **Windows:** the app sets **`OLLAMA_API_BASE=http://127.0.0.1:11434`** when using Ollama (avoids `localhost` → IPv6 issues). **Gemini:** valid key and quota. **General:** run from repo root; `pip install -r requirements.txt`. Debug: `adk api_server --port 8000 --log-level debug`.

### Quick demo prompts

**Google ADK in one line:** An `Agent` combines an **LLM** (Gemini API or local via LiteLLM), **instructions**, **function tools** (Python callables returning structured data), and optional **`sub_agents`**. Delegation is **`transfer_to_agent`**: the model chooses when to hand off to a specialist instead of hard-coding orchestration in application code.

**Copy-paste prompts** (each proves a different capability):

1. **Verified résumé grounding** — “Use **get_verified_track_record** and give three bullets on Drake’s SentriLock outcomes (field failure, downtime, cloud cost). Do not invent metrics.”
2. **Synthetic case study (ADK patterns)** — “Call **list_case_study_slugs**, then **get_case_study_by_slug** for `fintech-compliance-analyst`. Summarize the approach and label it **synthetic / illustrative**.”
3. **RevOps multi-agent + CRM tools** — “For **revops_lead_orchestrator**: triage lead **LD-10043**—policy/eligibility, priority score and tier, and next-best action. Say explicitly that leads in `revenue_ops_data.py` are **demo records**.”
4. **Meridian BSA/AML (synthetic bank)** — “For **aml_alert_orchestrator**: triage alert **ALT-20001**—regulatory triggers, severity tier, and recommended disposition. State that **Meridian Trust & Savings** and all alerts are **synthetic**.”

**File map** (if you only read a few files):

| File | What it shows |
|------|----------------|
| [`drake_talley_adk/agent.py`](drake_talley_adk/agent.py) | `root_agent`, portfolio specialists, `sub_agents`, shared portfolio tools |
| [`drake_talley_adk/portfolio_model.py`](drake_talley_adk/portfolio_model.py) | Gemini vs Ollama model selection (`GOOGLE_API_KEY` / `PORTFOLIO_ADK_MODEL`) |
| [`drake_talley_adk/revenue_ops_agents.py`](drake_talley_adk/revenue_ops_agents.py) | RevOps orchestrator + policy / scoring / action subgraph |
| [`drake_talley_adk/portfolio_tools.py`](drake_talley_adk/portfolio_tools.py) | Tool API over résumé + case-study data |
| [`drake_talley_adk/revenue_ops_tools.py`](drake_talley_adk/revenue_ops_tools.py) | Deterministic CRM tools; partitioned tool lists per specialist |
| [`drake_talley_adk/aml_alert_agents.py`](drake_talley_adk/aml_alert_agents.py) | Meridian (synthetic) AML orchestrator + policy / risk / disposition |
| [`drake_talley_adk/aml_alert_tools.py`](drake_talley_adk/aml_alert_tools.py) | Deterministic alert tools; `AML_TOOLS_*` partitions |
| [`recruiter_demo/`](recruiter_demo/) | React UI: `POST /run` + trace replay via Vite proxy |
| [`drake_talley_adk/portfolio_data.py`](drake_talley_adk/portfolio_data.py) | **Verified** track record vs **synthetic** vignettes (data only) |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Agent hierarchies, tool rules, production next steps |

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

## Docker (API server only)

From repo root:

```powershell
docker build -t adk-portfolio .
docker run --rm -p 8000:8000 -e GOOGLE_API_KEY="your-key" adk-portfolio
```

Then open ADK docs UI against `http://localhost:8000` or run `recruiter_demo` with the Vite proxy pointed at that host.

---

## Tests & CI

**pytest** covers deterministic tools and **agent graph wiring** (sub-agent names, tool-list subsets)—**no Gemini calls**.

```powershell
pip install -r requirements.txt
pip install ruff   # optional local lint
ruff check drake_talley_adk tests
pytest
```

**GitHub Actions** runs **Ruff**, **`compileall`**, and **pytest** on Python **3.10** and **3.12**. **Dependabot** watches pip, npm (`recruiter_demo`), and Actions.

---

## Disclosure

Synthetic vignettes in `case_studies` are **fictional** scenarios for **ADK** pattern demos. **RevOps** rows in `revenue_ops_data.py` and **Meridian BSA/AML** rows in `aml_alert_data.py` are **demo records** only. **Employment, clients, and quantitative claims** in `verified_track_record` are transcribed from Drake’s résumé for tool-grounded responses.

ADK **Web** is [development-only per Google](https://google.github.io/adk-docs/); production = Cloud Run, Vertex AI Agent Engine, or `adk api_server` patterns from ADK docs.

---
