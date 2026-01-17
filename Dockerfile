FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download TextBlob corpora
RUN python -m textblob.download_corpora

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Use ENTRYPOINT to force the start command even if the platform tries to override CMD
ENTRYPOINT ["python", "-m", "app.main"]
