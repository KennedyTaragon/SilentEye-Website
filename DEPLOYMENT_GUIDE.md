# SilentEye Deployment Guide

## Environment Configuration

### Development Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   - Copy `.env.example` to `.env`
   - Update the values in `.env` for your local development
   - The `.env` file is already configured for your current setup

3. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

### Render Deployment

#### Step 1: Push to GitHub
Since you want to include media files for the demo:

```bash
# Your existing push.sh script will handle this
./push.sh
```

**Commit message suggestion:**
```
Add media files and database for Render deployment demo
Configure environment variables for production
```

#### Step 2: Deploy to Render

1. **Create Web Service on Render**
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - Choose "Web Service"

2. **Environment Variables on Render**
   Set these in Render's dashboard under Environment:
   ```
   SECRET_KEY=your-production-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   DATABASE_URL=<Render will provide this automatically>
   ```

3. **Build Settings**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn silent_system.wsgi:application`

#### Step 3: Database Setup
Render will automatically create a PostgreSQL database and provide `DATABASE_URL`. The settings are already configured to use this.

#### Step 4: Media Files
Your media files will be included in the deployment since they're committed to GitHub.

## Environment Variables Reference

### Required for Production
- `SECRET_KEY`: Unique secret key for Django
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Your domain(s)

### Optional
- `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`: For contact forms
- `TIME_ZONE`: Server timezone (defaults to Africa/Nairobi)

## Features Configured

✅ **Environment-based configuration**  
✅ **Render deployment ready**  
✅ **Database auto-configuration**  
✅ **Production security settings**  
✅ **Media files included**  
✅ **Environment variables properly documented**  

## Files Modified

1. `.env` - Development environment variables
2. `.env.example` - Template for environment setup
3. `settings.py` - Updated to use environment variables
4. `requirements.txt` - Added `python-decouple` and `dj-database-url`
5. `.gitignore` - Updated to protect `.env` files

## Post-Deployment

After your demo period, consider:
1. Moving media files to cloud storage (AWS S3, Cloudinary)
2. Implementing proper database backup strategy
3. Setting up monitoring and logging
4. Configuring SSL certificate