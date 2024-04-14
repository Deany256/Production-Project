from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder= "../templates")
    app.config.from_object(Config)

    db.init_app(app)
    
    login_manager.init_app(app)
    
    with app.app_context():
        from .models import User
        
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
        
        db.create_all()

    from .routes import inventory_bp
    app.register_blueprint(inventory_bp)

    return app
