# Used a slimmed-down environment to save bandwidth and reduce security attack surface.
FROM python:3.12-slim

# Security: Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Optimizations
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV PORT=5000

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Permissions
RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 5000

# Healthcheck (slim image doesn't have curl, so we just use a python script)
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Using Gunicorn instead of Flask's built-in server. Gunicorn handles 
# multiple concurrent requests efficiently using worker processes.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "app:app"]