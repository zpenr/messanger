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
    app = Flask(__name__)    
    app.config.from_object(config_class)

    app.register_blueprint(user)
    app.register_blueprint(massage)
    app.register_blueprint(main)
    app.register_blueprint(me_liza)
    app.register_blueprint(liza_me)
    app.register_blueprint(me_makar)
    app.register_blueprint(makar_me)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Войди бля'

    with app.app_context():
        try:
            # Create database tables
            db.create_all()
            print("Database tables created successfully")
            
            # Test database connection
            from .models.user import User
            user_count = User.query.count()
            print(f"Database connection successful. Users in database: {user_count}")
            
        except Exception as e:
            print(f"Database initialization error: {e}")
            import traceback
            traceback.print_exc()

    # Error handlers
    @app.errorhandler(500)
    def internal_error(error):
        return "Internal Server Error: Please try again later", 500

    @app.errorhandler(404)
    def not_found_error(error):
        return "Page not found", 404

    return app