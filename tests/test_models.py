from app.models import Product

def test_product_creation(app):
    product = Product(name='Test Product', quantity=10, price=5.99)
    assert product.name == 'Test Product'
    assert product.quantity == 10
    assert product.price == 5.99
