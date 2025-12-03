#!/usr/bin/env bash
# Exit on error
set -o errexit

# Print useful debug info
echo "Current directory: $(pwd)"
echo "Python version: $(python3 --version)"
echo "Setting RENDER=True for deployment"
export RENDER=True

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p staticfiles
mkdir -p media/secure_uploads

# Logging setup
mkdir -p logs
touch logs/django.log logs/security.log logs/access.log
chmod 777 logs/django.log logs/security.log logs/access.log

# Clean static files directory
echo "Cleaning staticfiles directory"
rm -rf staticfiles/*

# Collect static files
echo "Collecting static files with Django..."
python3 manage.py collectstatic --no-input --clear

# Verify static files were collected
echo "Static files directory contents:"
ls -la staticfiles/

# Apply database migrations
echo "Applying database migrations..."
python3 manage.py migrate

# Fix gunicorn permissions - adding only this section to your original script
which gunicorn
echo "Making gunicorn executable..."
chmod 755 $(which gunicorn) 2>/dev/null || echo "Could not change gunicorn permissions directly"

echo "Build script completed successfully!"
#DATA