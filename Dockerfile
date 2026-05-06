# Runnable ADK api_server (Gemini key required at runtime).
# Build from repo root: docker build -t adk-portfolio .
FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt ./
COPY drake_talley_adk ./drake_talley_adk

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

# ADK discovers agent packages in the working directory.
CMD ["adk", "api_server", "--host", "0.0.0.0", "--port", "8000"]
