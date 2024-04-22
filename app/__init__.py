from quart import Quart
from quart_db import QuartDB
from quart_auth import QuartAuth
from quart_schema import QuartSchema
from config import Config

app = Quart(__name__, template_folder="../templates")
app.config.from_object(Config)
QuartSchema(app)

db = QuartDB(app,url='sqlite:///database/inventory.db', migrations_folder= 'migrations')

login_manager = QuartAuth()
login_manager.init_app(app)

from .route import inventory_bp
app.register_blueprint(inventory_bp)

def create_app():
    return app
