FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install dependencies (including curl for healthcheck)
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p logs staticfiles media

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user and set permissions
RUN adduser --disabled-password --no-create-home appuser \
    && chown -R appuser:appuser /app \
    && chmod -R 755 /app
USER appuser

# Expose port
EXPOSE 8000

# Run gunicorn with configurable workers
CMD ["sh", "-c", "gunicorn remedium_hms.wsgi:application --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS:-4}"]
