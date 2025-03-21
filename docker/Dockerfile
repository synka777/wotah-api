
# Base image
FROM python:3.12 AS base
# Create a non-root user for security
RUN useradd -ms /bin/bash appuser
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings \
    PATH="/home/appuser/.local/bin:${PATH}"
WORKDIR /app
COPY ./requirements/base.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r base.txt
# Copy project files
COPY . .
# Change ownership to non-root user
RUN chown -R appuser:appuser /app
# Use an entrypoint script for flexibility
COPY docker/entrypoint.sh /
RUN chmod +x /entrypoint.sh
# Switch to non-root user
USER appuser
ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 8000

# Production image (adds gunicorn)
FROM base AS prod
COPY ./requirements/prod.txt ./requirements/prod.txt
RUN pip install --no-cache-dir -r requirements/prod.txt
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
