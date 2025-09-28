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
        # Use absolute path in temp directory for Railway
        import tempfile
        temp_dir = tempfile.gettempdir()
        db_path = os.path.join(temp_dir, 'project.db')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
        print(f"Using SQLite database at: {db_path}")
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ewsdrftvgyhbujni12345uiasdjk1')
    SQLALCHEMY_TRACK_MODIFICATIONS = False