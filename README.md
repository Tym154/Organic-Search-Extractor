# Organic Search Extractor

A Flask application that retrieves Google organic search results using SerpApi, displays them in a web interface, and allows exporting the results as JSON.

## Features

- Search Google results through SerpApi
- Extract only organic search results
- Export results as JSON
- Input validation and error handling
- Unit tests with 95%+ coverage
- Docker and Docker Compose support
- Black, Ruff, and Mypy configuration

---

## Architecture

```
┌─────────────┐
│  Frontend   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Flask Route │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Service   │
└───┬─────┬───┘
    │     │
    │     ▼
    │  SerpApi
    │
    ▼
┌─────────────┐
│ Parsing &   │
│   Models    │
└──────┬──────┘
       │
       ▼
   JSON Response
```

### Project Structure

```text
.
├── models/            # Dataclasses used for API responses
├── routes/            # Flask API endpoints
├── services/          # SerpApi integration and parsing logic
├── static/            # JavaScript and CSS files
├── templates/         # HTML templates
├── tests/             # Unit tests
├── app.py             # Application entry point
├── config.py          # Configuration handling
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
```

---

## Environment Variables

Create a `.env` file from `.env.example`.

| Variable | Required | Description |
|-----------|-----------|-------------|
| SERPAPI_API_KEY | Yes | SerpApi API key |
| FLASK_ENV | No | development, production, testing |
| PORT | No | Application port (default: 5000) |
| LOG_LEVEL | No | DEBUG, INFO, WARNING, ERROR, CRITICAL |

Example:

```env
SERPAPI_API_KEY=your_api_key
FLASK_ENV=development
PORT=5000
LOG_LEVEL=INFO
```

---

## Local Development

### Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt # For development testing and linting
```

### Configure environment variables

```bash
cp .env.example .env
```

Update the API key inside `.env`.

### Run the application

```bash
python app.py
```

The application will be available at:

```text
http://localhost:5000
```

---

## Docker

### Run with Docker Compose

```bash
docker compose up --build
```

---

## Testing

Run all tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=. --cov-report=html
```

Current coverage:

```text
98%+
```

---

## Code Quality

Format check:

```bash
black --check .
```

If not satisfied:

```bash
black .
```

Linting:

```bash
ruff check .
```

If not satisfied:

```bash
ruff --fix
```

Static type checking:

```bash
mypy .
```

---

## API Endpoints

### Health Check

**GET**

```http
/health
```

Response:

```json
{
  "status": "ok"
}
```

---

### Search

**POST**

```http
/api/search
```

Request:

```json
{
  "query": "open source llms"
}
```

Success Response:

```json
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

```json
{
  "error": "Missing query parameter"
}
```

---

## Test Coverage

The test suite covers:

- API endpoints
- Application startup and configuration validation
- Health endpoint
- SerpApi client behavior
- Error handling paths
- Organic result parsing

---

## Notes

- Only organic Google search results are returned.
- Results can be downloaded as JSON from the web interface.
- SerpApi errors are translated into appropriate API responses.
- The application includes Docker support for local development and deployment.
