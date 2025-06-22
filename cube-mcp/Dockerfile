# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV MCP_PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        gcc \
        g++ \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
RUN pip install uv

# Copy dependency files
COPY pyproject.toml ./
COPY README.md ./

# Install Python dependencies
RUN uv pip install --system -e .

# Copy application code
COPY main.py ./

# Create non-root user for security
RUN adduser --disabled-password --gecos '' --uid 1001 appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose the SSE port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]