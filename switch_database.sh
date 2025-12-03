#!/bin/bash

# Database Switch Script
# Switches between local and Render PostgreSQL databases

echo "🗄️ Database Switcher"
echo "=================="
echo "Current .env database configuration:"
echo ""

if grep -q "DATABASE_URL=postgresql://vasco:zt9EdBIRsPpt4Xhpkbah9Ortaf4c3Hwy@dpg-d4nv72euk2gs73807t30-a.frankfurt-postgres.render.com" .env; then
    echo "✅ Currently connected to: RENDER PostgreSQL"
    CURRENT_DB="render"
elif grep -q "# DB_ENGINE=django.db.backends.postgresql" .env; then
    echo "✅ Currently configured for: LOCAL PostgreSQL (commented out)"
    CURRENT_DB="local_commented"
else
    echo "❓ Database configuration unclear"
    CURRENT_DB="unknown"
fi

echo ""
echo "Options:"
echo "1) Switch to LOCAL PostgreSQL database"
echo "2) Switch to RENDER PostgreSQL database"
echo "3) Show current .env content"
echo "4) Exit"
echo ""
read -p "Choose an option (1-4): " choice

case $choice in
    1)
        echo "🔄 Switching to LOCAL PostgreSQL database..."
        
        # Backup current .env
        cp .env .env.backup
        
        # Comment out Render DATABASE_URL and uncomment local settings
        sed -i 's/^DATABASE_URL=postgresql:\/\/vasco:zt9EdBIRsPpt4Xhpkbah9Ortaf4c3Hwy@dpg-d4nv72euk2gs73807t30-a.frankfurt-postgres.render.com\/silenteye_website_db/# DATABASE_URL=postgresql:\/\/vasco:zt9EdBIRsPpt4Xhpkbah9Ortaf4c3Hwy@dpg-d4nv72euk2gs73807t30-a.frankfurt-postgres.render.com\/silenteye_website_db/' .env
        
        # Uncomment local settings
        sed -i 's/^# DB_ENGINE=django.db.backends.postgresql/DB_ENGINE=django.db.backends.postgresql/' .env
        sed -i 's/^# DB_NAME=silenteye_db/DB_NAME=silenteye_db/' .env
        sed -i 's/^# DB_USER=vasco/DB_USER=vasco/' .env
        sed -i 's/^# DB_PASSWORD=1234/DB_PASSWORD=1234/' .env
        sed -i 's/^# DB_HOST=localhost/DB_HOST=localhost/' .env
        sed -i 's/^# DB_PORT=5432/DB_PORT=5432/' .env
        
        echo "✅ Switched to LOCAL PostgreSQL database"
        echo "📝 Backup saved to: .env.backup"
        ;;
        
    2)
        echo "🔄 Switching to RENDER PostgreSQL database..."
        
        # Backup current .env
        cp .env .env.backup
        
        # Uncomment Render DATABASE_URL and comment out local settings
        sed -i 's/^# DATABASE_URL=postgresql:\/\/vasco:zt9EdBIRsPpt4Xhpkbah9Ortaf4c3Hwy@dpg-d4nv72euk2gs73807t30-a.frankfurt-postgres.render.com\/silenteye_website_db/DATABASE_URL=postgresql:\/\/vasco:zt9EdBIRsPpt4Xhpkbah9Ortaf4c3Hwy@dpg-d4nv72euk2gs73807t30-a.frankfurt-postgres.render.com\/silenteye_website_db/' .env
        
        # Comment out local settings
        sed -i 's/^DB_ENGINE=django.db.backends.postgresql/# DB_ENGINE=django.db.backends.postgresql/' .env
        sed -i 's/^DB_NAME=silenteye_db/# DB_NAME=silenteye_db/' .env
        sed -i 's/^DB_USER=vasco/# DB_USER=vasco/' .env
        sed -i 's/^DB_PASSWORD=1234/# DB_PASSWORD=1234/' .env
        sed -i 's/^DB_HOST=localhost/# DB_HOST=localhost/' .env
        sed -i 's/^DB_PORT=5432/# DB_PORT=5432/' .env
        
        echo "✅ Switched to RENDER PostgreSQL database"
        echo "📝 Backup saved to: .env.backup"
        ;;
        
    3)
        echo "📋 Current .env database section:"
        echo "================================"
        grep -A 15 "DATABASE\|DB_" .env
        echo "================================"
        ;;
        
    4)
        echo "👋 Goodbye!"
        exit 0
        ;;
        
    *)
        echo "❌ Invalid option. Please choose 1-4."
        exit 1
        ;;
esac

echo ""
echo "💡 After switching databases, remember to:"
echo "   python manage.py migrate --run-syncdb"
echo ""
read -p "Run migrations now? (y/N): " run_migrations

if [[ $run_migrations =~ ^[Yy]$ ]]; then
    echo "🔄 Running Django migrations..."
    python manage.py migrate --run-syncdb
    echo "✅ Migrations completed"
fi