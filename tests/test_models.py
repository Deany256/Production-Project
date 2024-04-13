from app.models import Product

def test_product_creation(app):
    product = Product(name='Test Product', quantity=10, price=5.99)
    assert product.name == 'Test Product'
    assert product.quantity == 10
    assert product.price == 5.99

# Test adding a valid item to the database
def test_add_valid_product(client, app):
    # Make a POST request to add a product
    response = client.post('/add_product', data={'name': 'Test Product', 'quantity': 10, 'price': 5.99})
    assert response.status_code == 302  # Expecting a redirect after adding a product

    # Check that the product was added to the database
    with app.app_context():
        product = Product.query.filter_by(name='Test Product').first()
        assert product is not None
        assert product.quantity == 10
        assert product.price == 5.99

# Test adding an item with missing data
def test_add_product_missing_data(client):
    # Make a POST request with missing data
    response = client.post('/add_product', data={'name': 'Incomplete Product'})
    assert response.status_code == 400  # Expecting a bad request status code

# Test adding an item with invalid data
def test_add_product_invalid_data(client):
    # Make a POST request with invalid data (e.g., negative quantity)
    response = client.post('/add_product', data={'name': 'Invalid Product', 'quantity': -10, 'price': 5.99})
    assert response.status_code == 302  # Expecting a bad request status code

# Test adding an item with duplicate name
def test_add_product_duplicate_name(client, app):
    # Add a product with the same name to the database
    with app.app_context():
        existing_product = Product(name='Test Product', quantity=5, price=10.99)
        existing_product.save()

    # Make a POST request to add a product with the same name
    response = client.post('/add_product', data={'name': 'Test Product', 'quantity': 8, 'price': 15.99})
    assert response.status_code == 400  # Expecting a bad request status code

    # Check that the original product remains unchanged
    with app.app_context():
        product = Product.query.filter_by(name='Test Product').first()
        assert product is not None
        assert product.quantity == 5  # Quantity should remain unchanged

# Test adding an item with invalid price
def test_add_product_invalid_price(client):
    # Make a POST request with invalid price (e.g., non-numeric)
    response = client.post('/add_product', data={'name': 'Invalid Price Product', 'quantity': 5, 'price': 'invalid'})
    assert response.status_code == 400  # Expecting a bad request status code