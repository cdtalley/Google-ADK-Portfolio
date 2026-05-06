# Drake Talley — Google ADK Portfolio

Interactive hiring artifact built with [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/): a tool-grounded portfolio agent with deliberate delegation between a technical specialist and an executive storyteller.

## Why this exists

Recruiters and hiring managers can **chat with your portfolio** instead of scrolling another static PDF. The agent is instructed to **cite facts from code** (`portfolio_data.py`) rather than invent employers, dates, or metrics.

## Quick start

1. Python **3.10+** recommended (tested on 3.13).

2. Create a virtual environment (optional but recommended):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Configure Gemini API access:

   - Create a key in [Google AI Studio](https://aistudio.google.com/app/apikey).
   - Copy `env.example` to `.env` in this folder and set `GOOGLE_API_KEY`.

5. Run the ADK web UI from **this directory** (the parent of `drake_talley_adk/`):

   ```powershell
   adk web --port 8000
   ```

   Open `http://localhost:8000`, select **`drake_talley_adk`**, and try prompts like:

   - “Give me a two-minute pitch for a staff AI engineer loop.”
   - “Walk me through your ADK architecture in this repo.”
   - “Deep dive on evaluation strategy for agents.”

   CLI alternative:

   ```powershell
   adk run drake_talley_adk
   ```

## Customize your story

Edit **`drake_talley_adk/portfolio_data.py`**:

- Replace bracketed placeholders (`[Title]`, `[Quantified outcome — EDIT]`, links).
- Keep claims truthful—the agent uses those strings as **authoritative** answers.

Behavior and routing live in **`drake_talley_adk/agent.py`**. Tool surfaces are in **`portfolio_tools.py`**.

## Project layout

| Path | Role |
|------|------|
| `drake_talley_adk/agent.py` | `root_agent` + sub-agents (`technical_proof`, `executive_voice`) |
| `drake_talley_adk/portfolio_data.py` | Editable facts and case studies |
| `drake_talley_adk/portfolio_tools.py` | Tool functions the LLM calls for grounded answers |
| `requirements.txt` | `google-adk` dependency |

## Note on ADK Web

Google documents ADK Web as **development-only**, not a production deployment surface. For real traffic, plan for Cloud Run, Vertex AI Agent Engine, or your own API host using `adk api_server` patterns from the ADK docs.
