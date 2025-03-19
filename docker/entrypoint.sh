#!/bin/bash
set -e

# Apply database migrations
python manage.py migrate --noinput
# Collect static files when developing frontend features
# python manage.py collectstatic --noinput

# Execute the command passed to docker run
exec "$@"