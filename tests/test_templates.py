def test_index_template(client):
    response = client.get('/')
    assert b'Welcome to Inventory Management System' in response.data

def test_product_list_template(client):
    response = client.get('/products')
    assert b'Product List' in response.data
