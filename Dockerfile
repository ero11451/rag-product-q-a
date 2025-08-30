# Dockerfile
FROM python:3.11-slim

# System deps (if you need poppler/textract for PDFs, add them here)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use gunicorn in production
ENV PORT=5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "2", "app:app"]
