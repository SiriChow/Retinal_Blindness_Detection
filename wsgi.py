import os

# Use app_heroku.py in production, app.py in development
if os.environ.get('HEROKU', False):
    from app_heroku import app
else:
    from app import app

if __name__ == "__main__":
    app.run()