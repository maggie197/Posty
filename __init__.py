# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    # ---------- CLI command you already had ----------
    @app.cli.command("init-db")
    def init_db():
        """Create all database tables."""
        db.create_all()
        print("Database initialized.")

    # ---------- register existing blueprints ----------
    # dont have: from .views import main_bp
    # dont have: app.register_blueprint(main_bp)

    # ---------- NEW: register the gallery blueprint ----------
    from .gallery import gallery_bp     
    app.register_blueprint(gallery_bp)        
    
    return app
