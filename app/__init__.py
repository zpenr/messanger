from flask import Flask, render_template
from .extensions import db, migrate, login_manager
from .config import Config

from .routes.user import user
from .routes.massage import massage
from .routes.chat_me_liza import me_liza
from .routes.chat_me_makar import me_makar
from .routes.chat_liza_me import liza_me
from .routes.chat_makar_me import makar_me
from .routes.main import main

def create_app(config_class=Config):
    print("Starting Flask app initialization...")
    app = Flask(__name__)    
    app.config.from_object(config_class)
    print("Configuration loaded successfully")

    app.register_blueprint(user)
    app.register_blueprint(massage)

    app.register_blueprint(main)
    app.register_blueprint(me_liza)
    app.register_blueprint(liza_me)
    app.register_blueprint(me_makar)
    app.register_blueprint(makar_me)

    print("Initializing extensions...")
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    print("Extensions initialized successfully")

    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Войди бля'

    print("Creating database tables...")
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Database initialization warning: {e}")
            # Continue without failing - tables might already exist

    print("Flask app initialization completed successfully")
    return app