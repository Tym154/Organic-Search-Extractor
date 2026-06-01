<div align="center">

# Organic Search Extractor

A Flask application that retrieves Google organic search results using SerpApi, displays them in a web interface, and allows exporting results as JSON.

<p>
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg">
  <img src="https://img.shields.io/badge/Flask-3.x-black.svg">
  <img src="https://img.shields.io/badge/Coverage-98%25-brightgreen.svg">
  <img src="https://img.shields.io/badge/Docker-Supported-blue.svg">
  <img src="https://img.shields.io/badge/Code%20Style-Black-black.svg">
  <img src="https://img.shields.io/badge/Lint-Ruff-orange.svg">
  <img src="https://img.shields.io/badge/Types-Mypy-blue.svg">
</p>

</div>

---

## Table of Contents

* Features
* Architecture
* Project Structure
* Environment Variables
* Local Development
* Docker
* Testing
* Code Quality
* API Endpoints

---

## Features

| Feature         | Description                         |
| --------------- | ----------------------------------- |
| Google Search   | Query Google via SerpApi            |
| Organic Results | Extract only organic search results |
| JSON Export     | Download results as JSON            |
| Validation      | Input validation and error handling |
| Testing         | 98%+ test coverage                  |
| Docker Support  | Docker & Docker Compose support     |
| Code Quality    | Black, Ruff, and Mypy configured    |

---

## Architecture

```text id="arch1"
┌─────────────────────────┐
│ Frontend                │
│ HTML / CSS / JavaScript │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Flask Routes            │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Service Layer           │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Parsing & Models        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ SerpApi                 │
└─────────────────────────┘
```

---

## Project Structure

```text id="structure1"
.
├── models/             # Dataclasses used for API responses
├── routes/             # Flask API endpoints
├── services/           # SerpApi integration and parsing logic
├── static/             # JavaScript and CSS assets
├── templates/          # HTML templates
├── tests/              # Unit tests
├── app.py              # Application entry point
├── config.py           # Configuration handling
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
```

---

## Environment Variables

Create a `.env` file from `.env.example`.

| Variable        | Required | Description                               |
| --------------- | -------- | ----------------------------------------- |
| SERPAPI_API_KEY | Yes      | SerpApi API key                           |
| FLASK_ENV       | No       | development / production / testing        |
| PORT            | No       | Application port (default: 5000)          |
| LOG_LEVEL       | No       | DEBUG / INFO / WARNING / ERROR / CRITICAL |

Example:

```env id="env1"
SERPAPI_API_KEY=your_api_key
FLASK_ENV=development
PORT=5000
LOG_LEVEL=INFO
```

---

## Local Development

### Create virtual environment

```bash id="venv1"
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash id="deps1"
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Configure environment

```bash id="env2"
cp .env.example .env
```

Update the API key in `.env`.

### Run application

```bash id="run1"
python app.py
```

Application will be available at:

```text id="url1"
http://localhost:5000
```

---

## Docker

Run with Docker Compose:

```bash id="docker1"
docker compose up --build
```

---

## Testing

Run tests:

```bash id="test1"
pytest
```

Generate coverage report:

```bash id="cov1"
pytest --cov=. --cov-report=html
```

Coverage:

```text id="cov2"
98%+
```

---

## Code Quality

### Formatting

Check:

```bash id="fmt1"
black --check .
```

Apply:

```bash id="fmt2"
black .
```

### Linting

Check:

```bash id="lint1"
ruff check .
```

Fix:

```bash id="lint2"
ruff --fix
```

### Type checking

```bash id="type1"
mypy .
```

---

## API Endpoints

### Health Check

GET `/health`

Response:

```json id="api1"
{
  "status": "ok"
}
```

---

### Search

POST `/api/search`

Request:

```json id="api2"
{
  "query": "open source llms"
}
```

Success Response:

```json id="api3"
{
  "query": "open source llms",
  "timestamp": "2026-06-01T17:45:12Z",
  "results": [
    {
      "position": 1,
      "title": "Example Result",
      "url": "https://example.com",
      "snippet": "Example snippet"
    }
  ]
}
```

Error Response:

```json id="api4"
{
  "error": "Missing query parameter"
}
```

---

## Test Coverage

The test suite covers:

* API endpoints
* Application startup and configuration validation
* Health endpoint
* SerpApi client behavior
* Error handling paths
* Organic result parsing

---

## Notes

* Only organic Google search results are returned.
* Results can be downloaded as JSON from the web interface.
* SerpApi errors are translated into appropriate API responses.
* Docker support is included for local development and deployment.

---

<div align="center">

Made with Flask, SerpApi, Docker, and Python.

</div>
