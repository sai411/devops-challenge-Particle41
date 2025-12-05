# Stage 1 — Build Environment #
FROM python:3.11-slim AS builder

# Creating app directory
WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

# Install dependencies into a clean folder
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

################################################################################################
# Stage 2 - which is required to make image smaller with minimal code file only
FROM python:3.11-alpine

# Create a non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Copying installed libraries from previous stage
COPY --from=builder /install /usr/local

# Copy application code
COPY main.py .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Run using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app", "--workers", "2", "--threads", "4"]
