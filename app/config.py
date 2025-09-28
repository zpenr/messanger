import os

class Config(object):
    # Для Railway/Heroku
    if os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        # Локальная разработка
        USER = os.environ.get('POSTGRES_USER', 'zpenr')
        PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'Qq12ww345')
        HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
        PORT = os.environ.get('POSTGRES_PORT', 5532)
        DB = os.environ.get('POSTGRES_DB', 'mydb')
        SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ewsdrftvgyhbujni12345uiasdjk1')
    SQLALCHEMY_TRACK_MODIFICATIONS = True