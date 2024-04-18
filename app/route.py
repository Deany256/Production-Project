from secrets import compare_digest
from dataclasses import dataclass
from quart import Blueprint, redirect, request, url_for, render_template, g, flash
from quart_auth import login_required, login_user, logout_user, AuthUser, current_user
import hashlib
from quart_schema import QuartSchema, validate_request

inventory_bp = Blueprint('inventory', __name__)
    
@inventory_bp.route('/products')
async def product_list():
    products = await g.connection.fetch_all("SELECT * from product")
    return await render_template('product_list.html', products=products)

@inventory_bp.route('/')
async def index():
    return await render_template('index.html')

@inventory_bp.route('/protected')
@login_required
async def protected():
    return "Welcome to the SECURE Quart-Auth Example!"

@inventory_bp.route('/signup', methods=['GET', 'POST'])
async def signup():
    if request.method == 'POST':
        data = await request.form
        username = data["username"]
        password = data["password"]
        # Check if the username already exists
        
        password_hash = hashlib.sha256()
        password_hash.update(password.encode())
        password_hash = password_hash.hexdigest()
        
        userdatabase = await g.connection.fetch_one(f"SELECT 1 FROM User WHERE username = '{username}' LIMIT 1;")
        
        if userdatabase != None:
            return "Username already exists! Please choose a different one."
        else:
            await g.connection.execute(f"INSERT INTO user (username, password_hash) VALUES ('{username}', '{password_hash}');")
            login_user(AuthUser(username))
            return redirect(url_for('inventory.index'))  # Redirect to index page after successful login
        
    return await render_template('signup.html')  # Render signup form
    

@inventory_bp.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':
        data = await request.form
        username = data["username"]
        password = data["password"]
        
        userdatabase = await g.connection.fetch_one(f"SELECT * FROM user WHERE username = '{username}'")
        
        password_hash = hashlib.sha256()
        password_hash.update(password.encode())
        password_hash = password_hash.hexdigest()
        
        if username == userdatabase["username"] and compare_digest(password_hash, userdatabase["password_hash"]):
            login_user(AuthUser(username))
            return redirect(url_for('inventory.index'))  # Redirect to index page after successful login
    
    return await render_template('login.html')

@inventory_bp.route('/logout')
@login_required
async def logout():
    logout_user()
    return redirect(url_for('inventory.index'))  # Redirect to index page after logout

@inventory_bp.route('/products/<int:product_id>')
async def product_details(product_id):
    product = await g.connection.fetch_one(f"""
                                     SELECT * FROM product WHERE id = {product_id}
    """)
    return await render_template('product_details.html', product=product)

@inventory_bp.route('/add_product', methods=['GET', 'POST'])
async def add_product():
    if request.method == 'POST':
        form = await request.form  # Await the form data coroutine
        
        name = form['name']
        quantity = int(form['quantity'])
        price = form['price']
        
         # Check if quantity is greater than zero
        if quantity <= 0:
            await flash('Quantity must be greater than zero', 'error')
            return redirect(request.url)  # Redirect back to the form
        
        new_product = await g.connection.execute(f"INSERT INTO product (name, quantity, price) VALUES ('{name}', {quantity}, {price});")
        
        
        return redirect(url_for('inventory.product_list'))
    
    return await render_template('add_product.html')

@inventory_bp.route('/products/<int:product_id>/delete', methods=['POST'])
async def delete_product(product_id):
    product = await g.connection.execute(f"DELETE FROM Product WHERE id = {product_id};")
    await flash('Product deleted successfully!', 'success')
    return redirect(url_for('inventory.product_list'))

@inventory_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
async def edit_product(product_id):
    product = await g.connection.fetch_all(f"SELECT * FROM product WHERE id = {product_id}")

    if request.method == 'POST':
        form = await request.form  # Await the form data coroutine
        
        name = form['name']
        quantity = int(form['quantity'])
        price = form['price']

        if quantity <= 0:
            await flash('Quantity must be greater than zero', 'error')
            return redirect(request.url)

        await g.connection.execute(f"UPDATE Product SET name = '{name}', quantity = {quantity}, price = {price} WHERE id = {product_id};")
        
        await flash('Product updated successfully', 'success')
        return redirect(url_for('inventory.product_list'))

    return await render_template('edit_product.html', product=product)