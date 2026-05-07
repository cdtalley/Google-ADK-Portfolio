"""Pick the LLM id for all portfolio agents (Gemini API vs local Ollama, no extra code paths)."""

from __future__ import annotations

import os

_DEFAULT_GEMINI = "gemini-2.0-flash"
# Explicit :latest helps LiteLLM/Ollama agree on the tag; see README for `ollama pull`.
_DEFAULT_OLLAMA = "ollama/llama3.2:latest"


def _strip_optional_quotes(raw: str) -> str:
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "'\"":
        return raw[1:-1].strip()
    return raw


def _google_api_key_is_configured() -> bool:
    """True only when the env var looks like a real key (not env.example placeholders)."""
    raw = _strip_optional_quotes(os.environ.get("GOOGLE_API_KEY", ""))
    if not raw:
        return False
    low = raw.lower()
    # Copied env.example / docs — must not force Gemini.
    if "your_" in low and "key" in low:
        return False
    if "paste" in low and "key" in low:
        return False
    if low in {"changeme", "placeholder", "xxx", "sk-placeholder"}:
        return False
    # Real AI Studio keys are long; short values are almost always mistakes.
    if len(raw) < 12:
        return False
    return True


def _ensure_litellm_ollama_base_url() -> None:
    """LiteLLM uses OLLAMA_API_BASE; 127.0.0.1 avoids Windows localhost IPv6 (::1) mismatches."""
    if os.environ.get("OLLAMA_API_BASE", "").strip():
        return
    os.environ.setdefault("OLLAMA_API_BASE", "http://127.0.0.1:11434")


def portfolio_llm_model() -> str:
    """Return the model string passed to ``google.adk.agents.Agent``.

    Order:

    1. ``PORTFOLIO_ADK_MODEL`` if set — full control (any ADK-supported id).
    2. ``gemini-2.0-flash`` if ``GOOGLE_API_KEY`` looks configured.
    3. Else Ollama (``ollama/llama3.2:latest`` or ``PORTFOLIO_ADK_OLLAMA_MODEL``).
    """
    explicit = os.environ.get("PORTFOLIO_ADK_MODEL", "").strip()
    if explicit:
        if explicit.lower().startswith("ollama/"):
            _ensure_litellm_ollama_base_url()
        return explicit
    if _google_api_key_is_configured():
        return _DEFAULT_GEMINI
    fallback = os.environ.get("PORTFOLIO_ADK_OLLAMA_MODEL", _DEFAULT_OLLAMA).strip()
    out = fallback or _DEFAULT_OLLAMA
    if out.lower().startswith("ollama/"):
        _ensure_litellm_ollama_base_url()
    return out
