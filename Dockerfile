# Multi-stage build for production-ready gcPanel Construction Management Platform
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -e .

# Production stage
FROM python:3.11-slim as production

# Create non-root user for security
RUN groupadd -r gcpanel && useradd -r -g gcpanel gcpanel

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=gcpanel:gcpanel . .

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/uploads && \
    chown -R gcpanel:gcpanel /app

# Health check script
COPY --chown=gcpanel:gcpanel <<EOF /app/healthcheck.py
#!/usr/bin/env python3
import sys
import requests
import os

def health_check():
    try:
        port = os.environ.get('STREAMLIT_SERVER_PORT', '5000')
        response = requests.get(f'http://localhost:{port}/_stcore/health', timeout=10)
        if response.status_code == 200:
            print("Health check passed")
            sys.exit(0)
        else:
            print(f"Health check failed with status: {response.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"Health check failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    health_check()
EOF

RUN chmod +x /app/healthcheck.py

# Set production environment variables
ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=5000
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
ENV STREAMLIT_SERVER_MAX_MESSAGE_SIZE=200
ENV STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION=true
ENV STREAMLIT_THEME_BASE="light"
ENV STREAMLIT_LOGGER_LEVEL="INFO"

# Security and performance settings
ENV STREAMLIT_SERVER_COOKIE_SECRET=""
ENV STREAMLIT_SERVER_ENABLE_STATIC_SERVING=true
ENV STREAMLIT_SERVER_ALLOW_RUN_ON_SAVE=false

# Expose application port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python /app/healthcheck.py

# Switch to non-root user
USER gcpanel

# Start the application
CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]