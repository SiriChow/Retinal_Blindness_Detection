import os

# Heroku configuration settings

# Database URL will be automatically set by Heroku
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///users.db')

# Fix for Heroku's postgres:// vs postgresql:// issue
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Secret key from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Port from environment variable (Heroku sets this automatically)
PORT = int(os.environ.get('PORT', 8081))

# Debug mode (disable in production)
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Configure uploads folder
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)