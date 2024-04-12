def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Inventory Management System' in response.data

def test_product_list(client):
    response = client.get('/products')
    assert response.status_code == 200
    assert b'Product List' in response.data
