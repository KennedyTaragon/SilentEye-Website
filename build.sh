#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "=== Render Build Script Starting ==="
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"

# Set environment variable to indicate deployment
export RENDER=True

# Upgrade pip and install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Ensure required directories exist
echo "Creating necessary directories..."
mkdir -p static
mkdir -p staticfiles
mkdir -p media
mkdir -p logs

# Optional: create log files (not required for Render logging)
touch logs/django.log logs/security.log logs/access.log

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --no-input

echo "=== Build completed successfully ==="