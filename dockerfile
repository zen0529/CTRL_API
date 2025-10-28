# # ============================================
# # Dockerfile - Multi-stage build for production
# # ============================================

# # Stage 1: Builder - Install dependencies
# FROM python:3.12-slim AS builder

# # Install build dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

# # Create virtual environment
# RUN python -m venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"

# # Copy only requirements first (layer caching optimization)
# COPY requirements.txt .

# # Install Python packages
# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt

# # ============================================
# # Stage 2: Runtime - Minimal production image
# # ============================================
# FROM python:3.12-slim

# # Copy virtual environment from builder
# COPY --from=builder /opt/venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"

# # Create non-root user for security
# RUN useradd -m -u 1000 appuser && \
#     mkdir -p /app && \
#     chown appuser:appuser /app

# # Set working directory
# WORKDIR /app

# # Copy application code (as non-root user)
# COPY --chown=appuser:appuser . .

# # Switch to non-root user
# USER appuser

# # Expose port
# EXPOSE 8000

# # Health check
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#     CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# # Run application
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# ============================================
# Dockerfile - Optimized for Railway
# ============================================

FROM python:3.12-slim AS builder

# Install build dependencies in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy and install requirements FIRST (critical for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip wheel && \
    pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ============================================
# Runtime stage
# ============================================
FROM python:3.12-slim

WORKDIR /app

# Copy pre-built wheels and install (FAST)
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt && \
    rm -rf /wheels

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Copy application code LAST
COPY --chown=appuser:appuser . .

EXPOSE 8000

# Simple CMD without health check (Railway handles monitoring)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]