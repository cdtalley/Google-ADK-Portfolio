# Drake Talley — Google ADK Portfolio (GitHub)

Public portfolio for recruiters and hiring managers: a **live [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/)** app that showcases **agentic development**—multi-agent orchestration, function tools, and Gemini—applied across **synthetic, cross-industry scenarios**.

## Disclosure: synthetic scenarios

The **case studies** in `drake_talley_adk/portfolio_data.py` use **fictional organizations and illustrative metrics**. They exist to demonstrate **repeatable ADK design patterns** (routing, tools, delegation, evaluation hooks), not to represent verifiable client engagements. Your real résumé and references stay the source of truth for employment history.

## What this demonstrates (ADK expertise)

| Theme | Where it shows up |
|--------|-------------------|
| **Multi-agent** | `root_agent` + `technical_proof` + `executive_voice` with LLM-driven transfer |
| **Tool-grounded answers** | `portfolio_tools.py` — structured JSON from `portfolio_data.py` |
| **Hiring-ready narrative** | Same facts, different specialist agents for technical vs exec tone |
| **Cross-industry breadth** | Healthcare, fintech, retail, manufacturing, insurance, platform eval (all synthetic) |

Drake positions as an engineer who can **ship and maintain ADK-based agents**, not only prototype chats.

## Quick start

1. Python **3.10+** (tested on 3.13).

2. Virtual environment (recommended):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install:

   ```powershell
   pip install -r requirements.txt
   ```

4. API key: create one in [Google AI Studio](https://aistudio.google.com/app/apikey), then copy `env.example` to `.env` and set `GOOGLE_API_KEY`.

5. From **this directory** (parent of `drake_talley_adk/`):

   ```powershell
   adk web --port 8000
   ```

   Open `http://localhost:8000`, select **`drake_talley_adk`**.

   Example prompts:

   - “What’s the data policy for the case studies?”
   - “How does this repo use Google ADK multi-agent patterns?”
   - “Walk me through the fintech compliance scenario and which ADK patterns it uses.”

   CLI: `adk run drake_talley_adk`

## Customize for your profiles

Update **`drake_talley_adk/portfolio_data.py`** → `identity.profiles` (LinkedIn, GitHub). Keep or replace synthetic scenarios; add real projects in parallel sections if you want both.

## Layout

| Path | Role |
|------|------|
| `drake_talley_adk/agent.py` | ADK `Agent` graph: `root_agent`, sub-agents, tools |
| `drake_talley_adk/portfolio_data.py` | Synthetic scenarios, ADK expertise copy, data policy |
| `drake_talley_adk/portfolio_tools.py` | Function tools (includes `get_portfolio_context`, `get_adk_expertise`) |
| `requirements.txt` | `google-adk` |

## ADK Web note

Google documents **ADK Web** as **development-only**. For production, use paths in the ADK docs (e.g., Cloud Run, Vertex AI Agent Engine, `adk api_server`).
