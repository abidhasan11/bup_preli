# GridWise LLM — Smart Campus Energy Optimization Service

[![CI Tests](https://img.shields.io/badge/pytest-13%20passed-brightgreen.svg)](#running-tests)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-BUP%20CSE%20Fest%202026-orange.svg)](#)

> **Competition**: BUP CSE FEST 2026 Hackathon (in association with Poridhi)  
> **Track**: GridWise LLM — Smart Campus Energy Optimization Challenge  
> **Artifact**: Deployed Public HTTP API (`/health` and `/optimize-energy`)  

---

## 1. Overview

**GridWise LLM** is an automated smart campus energy dispatch system that:
1. Ingests 24-hour campus energy profiles (electricity demand, rooftop solar PV forecast, dynamic grid tariffs) and battery specs.
2. Interprets natural-language operator directives using an **LLM** (Google Gemini API with deterministic rule-based NLP fallback).
3. Validates and sanitizes directives using **deterministic guardrails** to prevent hallucinations and out-of-bound parameters.
4. Solves a mathematical **Linear Programming (LP)** model via SciPy HiGHS / PuLP to minimize total grid electricity purchase costs while satisfying battery rate limits, dynamic reserves, and end-of-day battery neutrality ($E_{23} = E_{\text{initial}}$).
5. **Independently replays and verifies** the final 24-hour schedule to guarantee $\pm 0.01$ numerical tolerance compliance with the judge harness.

---

## 2. Project Architecture

```
preli_hackathon/
├── app/
│   ├── config.py                 # Configuration & environment variables
│   ├── schemas/
│   │   ├── request.py            # Pydantic v2 validation for incoming requests
│   │   └── response.py           # Pydantic v2 schemas for API responses
│   ├── optimizer/
│   │   ├── solver.py             # Exact LP mathematical solver (SciPy HiGHS / PuLP)
│   │   └── models.py             # Optimization data containers
│   ├── guardrails/
│   │   └── validator.py          # Deterministic guardrails, interval sanitization, safe failure
│   ├── llm/
│   │   ├── prompts.py            # System instructions, few-shot directive examples
│   │   ├── parser.py             # JSON extractor & robust regex fallback parser
│   │   └── client.py             # Asynchronous Gemini API client
│   ├── verifier/
│   │   └── replay.py             # Judge simulator & integrity replay validator
│   └── main.py                   # FastAPI app with /health and /optimize-energy
├── tests/
│   ├── test_optimizer.py         # Unit tests for LP solver & constraint enforcement
│   ├── test_guardrails.py        # Unit tests for directive validation & safe-failure
│   ├── test_replay.py            # Unit tests for independent replay verifier
│   └── test_api.py               # End-to-end integration tests on API endpoints
├── Dockerfile                    # Containerization for cloud deployment
├── docker-compose.yml           # Compose file for deployment
├── requirements.txt              # Dependencies
├── INSTRUCTION.md                # Canonical architectural and technical manual
├── INPUTS_AND_OUTPUTS.md         # Schema and input/output reference with 24h sample
└── README.md                     # Quickstart documentation
```

---

## 3. Quick Start (Local Setup)

### 3.1 Prerequisites
- Python 3.11+
- Git

### 3.2 Installation
```bash
# Clone or navigate to the directory
cd preli_hackathon

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3.3 Configure Environment (Optional)
Create a `.env` file to configure your Gemini API key (the service automatically falls back to the deterministic extractor if no key is provided):
```ini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
PORT=8000
HOST=0.0.0.0
```

### 3.4 Running the API Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger API documentation will be available at `http://localhost:8000/docs`.

---

## 4. Running Tests

Run the full automated test suite:
```bash
pytest -v
```

All 13 test suites covering optimizer mechanics, guardrails, replay checks, and full API integration should pass with 100% success.

---

## 5. API Endpoints

### 5.1 `GET /health`
- **Response**: HTTP 200
```json
{
  "status": "ok"
}
```

### 5.2 `POST /optimize-energy`
- Ingests 24-hour hourly profile and 1–3 operator notes.
- Returns parsed directives and the 24-hour dispatch plan.
- See **[INPUTS_AND_OUTPUTS.md](INPUTS_AND_OUTPUTS.md)** for the complete schema and sample payload.

---

## 6. Docker Deployment (Poridhi / Cloud VM)

### Build and Run with Docker
```bash
# Build image
docker build -t gridwise-api .

# Run container
docker run -d -p 8000:8000 --name gridwise-api -e GEMINI_API_KEY="your_key" gridwise-api
```

### Run with Docker Compose
```bash
docker-compose up -d --build
```
The service will be publicly accessible on port `8000`.

---
*Developed for BUP CSE Fest 2026 Hackathon (GridWise LLM).*
