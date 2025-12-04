# Dockerfile
FROM python:3.11-slim

# create a non-root user
ENV APP_USER=appuser
ENV APP_HOME=/home/$APP_USER

# create user and app directory
RUN addgroup --system $APP_USER && adduser --system --ingroup $APP_USER $APP_USER \
    && mkdir -p $APP_HOME/app

WORKDIR $APP_HOME/app

# Install runtime deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copy only what's necessary
COPY requirements.txt .

# Install python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY main.py .

# Set permissions
RUN chown -R $APP_USER:$APP_USER $APP_HOME

# Switch to non-root user
USER $APP_USER

# Expose default port
EXPOSE 8080

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app", "--workers", "2", "--threads", "4"]
