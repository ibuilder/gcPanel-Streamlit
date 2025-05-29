# Highland Tower Development - gcPanel Production Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN pip install --no-cache-dir uv && \
    uv pip install --system -r uv.lock

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash gcpanel && \
    chown -R gcpanel:gcpanel /app

USER gcpanel

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/_stcore/health || exit 1

# Expose port
EXPOSE 5000

# Production command
CMD ["streamlit", "run", "gcpanel_enhanced_navigation.py", "--server.port=5000", "--server.address=0.0.0.0", "--server.headless=true"]