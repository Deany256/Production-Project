from quart import Quart
# from quart_sqlalchemy import SQLAlchemy
from quart_db import QuartDB
from quart_auth import QuartAuth
from quart_schema import QuartSchema
from config import Config

app = Quart(__name__, template_folder="../templates")
app.config.from_object(Config)
QuartSchema(app)

db = QuartDB(app,url='sqlite:///database/inventory.db', migrations_folder= 'migrations')

login_manager = QuartAuth()

# db.init_app(app)

login_manager.init_app(app)

# async with app.app_context():
#     from .models import User
    
#     @login_manager.user_loader
#     async def load_user(user_id):
#         return await User.query.get(int(user_id))
    
#     await db.create_all()

# from .routes import inventory_bp
from .route import inventory_bp
app.register_blueprint(inventory_bp)



def create_app():
    return app
