from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder= "../templates")
    app.config.from_object(Config)

    db.init_app(app)
    
    with app.app_context():
        from . import models
        db.create_all()

    from .routes import inventory_bp
    app.register_blueprint(inventory_bp)

    return app
