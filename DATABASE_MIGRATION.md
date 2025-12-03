# Database Migration Scripts

## Overview

Scripts to help migrate your local PostgreSQL database to Render PostgreSQL and switch between databases.

## Prerequisites

Make sure you have PostgreSQL client tools installed:
- **Ubuntu/Debian**: `sudo apt-get install postgresql-client`
- **macOS**: `brew install postgresql`

## Scripts Available

### 1. `backup_local_to_render.sh`
**Purpose**: Backup local database and restore to Render PostgreSQL

**Usage**:
```bash
chmod +x backup_local_to_render.sh
./backup_local_to_render.sh
```

**What it does**:
1. ✅ Backs up your local PostgreSQL database (`silenteye_db`)
2. ✅ Restores the backup to your Render PostgreSQL database
3. ✅ Runs Django migrations to ensure proper table setup
4. ✅ Collects static files
5. ✅ Provides verification commands

### 2. `switch_database.sh`
**Purpose**: Switch between local and Render PostgreSQL configurations

**Usage**:
```bash
chmod +x switch_database.sh
./switch_database.sh
```

**What it does**:
1. ✅ Shows current database configuration
2. ✅ Switches between local and Render database settings in `.env`
3. ✅ Backs up your `.env` file before changes
4. ✅ Optionally runs migrations after switching

## Database Configuration

### Local PostgreSQL
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=silenteye_db
DB_USER=vasco
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=5432
```

### Render PostgreSQL
```
DATABASE_URL=postgresql://vasco:zt9EdBIRsPpt4Xhpkbah9Ortaf4c3Hwy@dpg-d4nv72euk2gs73807t30-a.frankfurt-postgres.render.com/silenteye_website_db
```

## Migration Workflow

1. **Ensure your local PostgreSQL is running**
2. **Run the backup and restore script**:
   ```bash
   ./backup_local_to_render.sh
   ```
3. **Your app will now be connected to the Render database with your local data**

## Verification Commands

After migration, verify your data:
```bash
# Connect to Django shell
python manage.py shell

# Check data counts
from website.models import *
print(f"SiteConfig: {SiteConfig.objects.count()}")
print(f"Products: {Product.objects.count()}")
print(f"Team Members: {TeamMember.objects.count()}")
```

## Troubleshooting

### Common Issues

1. **"pg_dump not found"**: Install PostgreSQL client tools
2. **Connection refused**: Make sure your local PostgreSQL is running
3. **Authentication failed**: Check local PostgreSQL credentials in `.env`
4. **Render database connection failed**: Verify Render DATABASE_URL

### Manual Steps

If scripts fail, you can do it manually:

1. **Backup local database**:
   ```bash
   pg_dump -h localhost -p 5432 -U vasco -d silenteye_db --no-owner --no-privileges -f local_backup.sql
   ```

2. **Restore to Render**:
   ```bash
   psql "postgresql://vasco:zt9EdBIRsPpt4Xhpkbah9Ortaf4c3Hwy@dpg-d4nv72euk2gs73807t30-a.frankfurt-postgres.render.com/silenteye_website_db" -f local_backup.sql
   ```

3. **Run Django migrations**:
   ```bash
   python manage.py migrate --run-syncdb
   ```

## Important Notes

- 🔐 The `.env` file contains sensitive data and is git-ignored
- 📝 Always backup your `.env` file before making changes
- 🗄️ Media files need to be committed to git for Render deployment
- ✅ Test your application thoroughly after migration