# DocuSign CLM API Portal - Deployment Instructions for Render

This document provides instructions for deploying the DocuSign CLM API Portal Django application to Render.

## Prerequisites

- A Render account (https://render.com)
- Git repository with your Django project (optional, you can also deploy directly from the zip file)

## Deployment Steps

### Option 1: Deploy using the Render Dashboard (Web Service)

1. **Log in to your Render account** and navigate to the Dashboard.

2. **Create a new Web Service**:
   - Click on the "New +" button in the top right corner
   - Select "Web Service"

3. **Connect your repository** (if using Git) or **upload your code**:
   - If using Git, connect your repository
   - If deploying from the zip file, select "Upload Files" and upload the extracted project files

4. **Configure your Web Service**:
   - Name: `docusign-clm-portal` (or your preferred name)
   - Environment: `Python 3`
   - Region: Choose the region closest to your users
   - Branch: `main` (if using Git)
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start Command: `gunicorn docusign_clm_portal.wsgi:application`
   - Plan: Choose the appropriate plan for your needs (Free tier works for testing)

5. **Add Environment Variables**:
   - Click on the "Environment" tab
   - Add the following environment variables:
     - `DJANGO_SECRET_KEY`: Generate a new secret key (you can use https://djecrety.ir/)
     - `DJANGO_DEBUG`: Set to `False` for production
     - `ALLOWED_HOSTS`: Add your Render domain (e.g., `docusign-clm-portal.onrender.com`)
     - `DATABASE_URL`: This will be automatically set by Render if you use their PostgreSQL service

6. **Create Database** (Optional, but recommended for production):
   - Go back to the Render Dashboard
   - Click on "New +" and select "PostgreSQL"
   - Configure your database (name, region, plan)
   - After creation, note the Internal Database URL
   - Add this URL as the `DATABASE_URL` environment variable in your Web Service settings

7. **Deploy**:
   - Click "Create Web Service"
   - Render will build and deploy your application

### Option 2: Deploy using Render Blueprint (YAML Configuration)

1. **Create a `render.yaml` file** in the root of your project with the following content:

```yaml
services:
  - type: web
    name: docusign-clm-portal
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
    startCommand: gunicorn docusign_clm_portal.wsgi:application
    envVars:
      - key: DJANGO_SECRET_KEY
        generateValue: true
      - key: DJANGO_DEBUG
        value: false
      - key: ALLOWED_HOSTS
        value: .onrender.com
      - key: DATABASE_URL
        fromDatabase:
          name: docusign-clm-db
          property: connectionString

databases:
  - name: docusign-clm-db
    plan: free
```

2. **Deploy using the Blueprint**:
   - Push this file to your Git repository (if using Git)
   - In the Render Dashboard, click "New +" and select "Blueprint"
   - Connect your repository and deploy

## Post-Deployment Steps

1. **Create a Superuser**:
   - Go to the "Shell" tab in your Web Service
   - Run: `python manage.py createsuperuser`
   - Follow the prompts to create an admin user

2. **Configure Static Files** (if needed):
   - If static files aren't loading correctly, you may need to configure a static files service
   - Consider using Render's static site hosting or a service like AWS S3

3. **Set Up Custom Domain** (Optional):
   - In your Web Service settings, go to the "Settings" tab
   - Under "Custom Domain", add your domain
   - Follow the instructions to verify ownership and configure DNS

## Troubleshooting

- **Application Error**: Check the logs in the Render Dashboard for error messages
- **Database Connection Issues**: Verify your `DATABASE_URL` environment variable
- **Static Files Not Loading**: Ensure `STATIC_URL` and `STATIC_ROOT` are correctly configured in settings.py

## Additional Configuration for Production

For a production environment, consider the following additional configurations:

1. **Update `settings.py`**:
   - Ensure `DEBUG` is set to `False` in production
   - Configure `ALLOWED_HOSTS` to include your Render domain
   - Set up proper logging

2. **Security Settings**:
   - Enable HTTPS by setting `SECURE_SSL_REDIRECT = True`
   - Set `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True`
   - Consider adding security middleware like `django-csp`

3. **Performance Optimization**:
   - Configure caching
   - Optimize database queries
   - Consider using a CDN for static files

## Maintenance

- Regularly update dependencies
- Monitor application performance and logs
- Set up automated backups for your database

For more information, refer to the [Render documentation](https://render.com/docs) and [Django deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/).
