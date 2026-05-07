"""Model selection: Gemini when key present, else Ollama id (no live LLM calls)."""

from __future__ import annotations

import os

from drake_talley_adk.portfolio_model import portfolio_llm_model


def test_explicit_portfolio_model_wins(monkeypatch) -> None:
    monkeypatch.setenv("PORTFOLIO_ADK_MODEL", "ollama/mistral")
    monkeypatch.setenv("GOOGLE_API_KEY", "should-not-matter-but-long-enough-key")
    assert portfolio_llm_model() == "ollama/mistral"


def test_google_key_selects_gemini(monkeypatch) -> None:
    monkeypatch.delenv("PORTFOLIO_ADK_MODEL", raising=False)
    monkeypatch.setenv("GOOGLE_API_KEY", "fake-google-api-key-for-testing-12345")
    assert portfolio_llm_model() == "gemini-2.0-flash"


def test_placeholder_google_key_uses_ollama(monkeypatch) -> None:
    monkeypatch.delenv("PORTFOLIO_ADK_MODEL", raising=False)
    monkeypatch.delenv("PORTFOLIO_ADK_OLLAMA_MODEL", raising=False)
    monkeypatch.setenv("GOOGLE_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
    assert portfolio_llm_model() == "ollama/llama3.2:latest"


def test_short_google_key_uses_ollama(monkeypatch) -> None:
    monkeypatch.delenv("PORTFOLIO_ADK_MODEL", raising=False)
    monkeypatch.delenv("PORTFOLIO_ADK_OLLAMA_MODEL", raising=False)
    monkeypatch.setenv("GOOGLE_API_KEY", "short")
    assert portfolio_llm_model() == "ollama/llama3.2:latest"


def test_no_key_selects_ollama_default(monkeypatch) -> None:
    monkeypatch.delenv("PORTFOLIO_ADK_MODEL", raising=False)
    monkeypatch.delenv("PORTFOLIO_ADK_OLLAMA_MODEL", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    assert portfolio_llm_model() == "ollama/llama3.2:latest"


def test_no_key_respects_ollama_override(monkeypatch) -> None:
    monkeypatch.delenv("PORTFOLIO_ADK_MODEL", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.setenv("PORTFOLIO_ADK_OLLAMA_MODEL", "ollama/qwen2.5")
    assert portfolio_llm_model() == "ollama/qwen2.5"


def test_ollama_sets_api_base(monkeypatch) -> None:
    monkeypatch.delenv("PORTFOLIO_ADK_MODEL", raising=False)
    monkeypatch.delenv("PORTFOLIO_ADK_OLLAMA_MODEL", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("OLLAMA_API_BASE", raising=False)
    portfolio_llm_model()
    assert os.environ.get("OLLAMA_API_BASE") == "http://127.0.0.1:11434"
