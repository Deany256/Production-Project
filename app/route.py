from secrets import compare_digest
from dataclasses import dataclass
from quart import Blueprint, redirect, request, url_for, render_template, g
from quart_auth import login_required, login_user, logout_user, AuthUser, current_user
from quart_schema import QuartSchema, validate_request

inventory_bp = Blueprint('inventory', __name__)

@dataclass
class User_login:
    username: str
    passwork: str
    
@inventory_bp.route('/products')
async def product_list():
    products = await g.connection.fetch_all("""
    SELECT * from product
    """
    )
    return await render_template('product_list.html', products=products)

@inventory_bp.route('/')
async def index():
    return "Welcome to the Quart-Auth Example!"

@inventory_bp.route('/protected')
@login_required
async def protected():
    return "Welcome to the SECURE Quart-Auth Example!"

@inventory_bp.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':
        data = await request.form
        username = data["username"]
        password = data["password"]
        # username = request.form.get('username')
        # password = request.form.get('password')
        if username == "user" and compare_digest(password, "password"):
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
def add_product():
    pass

@inventory_bp.route('/products/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    pass