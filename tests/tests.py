import pytest
from app import create_app, db
from app.models import Product

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Inventory Management System' in response.data

def test_product_list(client):
    response = client.get('/products')
    assert response.status_code == 200
    assert b'Product List' in response.data

def test_add_product(client):
    response = client.post('/add_product', data={'name': 'Test Product', 'quantity': 10, 'price': 5.99})
    assert response.status_code == 302  # Redirect after adding a product
    assert Product.query.count() == 1
    assert Product.query.first().name == 'Test Product'

