#!/bin/bash

# PostgreSQL Database Migration Script: Local → Render
# This script backs up your local PostgreSQL database and restores it to Render PostgreSQL

set -e  # Exit on any error

echo "🚀 Starting PostgreSQL database migration: Local → Render"
echo "=================================================="

# Create backup directory
mkdir -p ./backup_migration
BACKUP_FILE="./backup_migration/local_backup_$(date +%Y%m%d_%H%M%S).sql"

# Check if PostgreSQL client tools are available
if ! command -v pg_dump &> /dev/null; then
    echo "❌ Error: pg_dump not found. Please install PostgreSQL client tools:"
    echo "   Ubuntu/Debian: sudo apt-get install postgresql-client"
    echo "   macOS: brew install postgresql"
    exit 1
fi

if ! command -v psql &> /dev/null; then
    echo "❌ Error: psql not found. Please install PostgreSQL client tools:"
    echo "   Ubuntu/Debian: sudo apt-get install postgresql-client"
    echo "   macOS: brew install postgresql"
    exit 1
fi

echo "📋 Step 1: Creating backup of local database..."

# Backup local database
pg_dump -h localhost -p 5432 -U vasco -d silenteye_db --no-owner --no-privileges -f "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Local database backup created: $BACKUP_FILE"
else
    echo "❌ Failed to backup local database"
    exit 1
fi

echo "📋 Step 2: Restoring backup to Render PostgreSQL..."

# Restore to Render database
psql "postgresql://vasco:zt9EdBIRsPpt4Xhpkbah9Ortaf4c3Hwy@dpg-d4nv72euk2gs73807t30-a.frankfurt-postgres.render.com/silenteye_website_db" -f "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Database successfully restored to Render!"
else
    echo "❌ Failed to restore database to Render"
    echo "💡 You may need to manually create tables first:"
    echo "   python manage.py migrate"
    echo "   Then run this script again"
    exit 1
fi

echo "📋 Step 3: Running Django migrations on Render database..."

# Run Django migrations to ensure all tables are properly set up
python manage.py migrate --run-syncdb

echo "📋 Step 4: Collecting static files..."

python manage.py collectstatic --noinput

echo "🎉 Migration completed successfully!"
echo "=================================================="
echo "✅ Local database backed up to: $BACKUP_FILE"
echo "✅ Data restored to Render PostgreSQL database"
echo "✅ Django migrations completed"
echo "✅ Static files collected"
echo ""
echo "📋 Next steps:"
echo "1. Test your application with the new Render database"
echo "2. If everything works, you can delete the backup file:"
echo "   rm $BACKUP_FILE"
echo ""
echo "🔍 To verify data in Render database:"
echo "   python manage.py shell -c 'from website.models import *; print(f\"SiteConfig: {SiteConfig.objects.count()}\")'"