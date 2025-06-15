# Use a slim official Python image
FROM python:3.11-slim

# Avoid Python writing .pyc and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py

# Install build dependencies and then remove cache
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Flask’s default port
EXPOSE 5000

# Run the app (listening on all interfaces)
CMD ["flask", "run", "--host=0.0.0.0"]
