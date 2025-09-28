import os

class Config(object):
    # Database configuration
    if os.environ.get('DATABASE_URL'):
        # Railway/Heroku with PostgreSQL - disable SSL
        db_url = os.environ.get('DATABASE_URL')
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://')
        SQLALCHEMY_DATABASE_URI = db_url + '?sslmode=disable'
    else:
        # Fallback to SQLite for Railway without database
        SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/project.db'
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ewsdrftvgyhbujni12345uiasdjk1')
    SQLALCHEMY_TRACK_MODIFICATIONS = False