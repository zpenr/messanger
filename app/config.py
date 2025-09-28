import os

class Config(object):
    # Database configuration
    if os.environ.get('DATABASE_URL'):
        # Railway/Heroku with PostgreSQL
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        # Fallback to SQLite for Railway without database
        SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/project.db'
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ewsdrftvgyhbujni12345uiasdjk1')
    SQLALCHEMY_TRACK_MODIFICATIONS = False