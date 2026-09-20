FROM python:3.11.9-slim

# Stay in /app; copy just requirements first to maximise Docker layer cache.
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the project. .dockerignore excludes notebooks/, .venv/, etc.
COPY . .

# Render sets $PORT at runtime; fall back to 5000 for other platforms.
EXPOSE 5000
CMD ["sh", "-c", "gunicorn app:app --workers 1 --timeout 120 --bind 0.0.0.0:${PORT:-5000}"]
