import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app, db
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import TestConfig

@pytest.fixture
def app():
    app = create_app()  
    app.config.from_object(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.engine.execute(table.delete())