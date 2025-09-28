import os

class Config(object):
    # Для Railway/Heroku
    if os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
        print(f"Using DATABASE_URL from environment")
    else:
        # Локальная разработка или Railway без базы данных
        USER = os.environ.get('POSTGRES_USER', 'zpenr')
        PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'Qq12ww345')
        HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
        PORT = os.environ.get('POSTGRES_PORT', '5532')
        DB = os.environ.get('POSTGRES_DB', 'mydb')
        
        # Fallback to SQLite if no PostgreSQL connection available
        if HOST == '127.0.0.1' and not os.environ.get('POSTGRES_HOST'):
            # Use SQLite for Railway if no database is configured
            SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/project.db'
            print(f"Using SQLite fallback database")
        else:
            SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
            print(f"Using local database config: {HOST}:{PORT}/{DB}")
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ewsdrftvgyhbujni12345uiasdjk1')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    # Debug info
    print(f"Database URI configured: {SQLALCHEMY_DATABASE_URI[:20]}...")
    print(f"Environment variables: DATABASE_URL={'SET' if os.environ.get('DATABASE_URL') else 'NOT SET'}")
    print(f"PORT: {os.environ.get('PORT', 'NOT SET')}")