from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from .models import Product, User, db

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/')
def index():
    return render_template('index.html')

@inventory_bp.route('/products')
def product_list():
    products = Product.query.all()
    return render_template('product_list.html', products=products)

@inventory_bp.route('/products/<int:product_id>')
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_details.html', product=product)

@inventory_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = request.form['price']
        
         # Check if quantity is greater than zero
        if quantity <= 0:
            flash('Quantity must be greater than zero', 'error')
            return redirect(request.url)  # Redirect back to the form
        
        new_product = Product(name=name, quantity=quantity, price=price)
        db.session.add(new_product)
        db.session.commit()
        
        return redirect(url_for('inventory.product_list'))
    
    return render_template('add_product.html')

@inventory_bp.route('/products/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('inventory.product_list'))

@inventory_bp.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.quantity = int(request.form['quantity'])
        product.price = request.form['price']

        if product.quantity <= 0:
            flash('Quantity must be greater than zero', 'error')
            return redirect(request.url)

        db.session.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('inventory.product_list'))

    return render_template('edit_product.html', product=product)

@inventory_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('inventory.index'))  # Redirect if user is already logged in

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            return "Username already exists! Please choose a different one."
        
        # Create a new user
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # Automatically log in the new user
        login_user(new_user)
        return redirect(url_for('inventory.index'))  # Redirect to index page after successful signup

    return render_template('signup.html')  # Render signup form

@inventory_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('inventory.index'))  # Redirect if user is already logged in

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('inventory.index'))  # Redirect to index page after successful login

    return render_template('login.html')  # Render login form

@inventory_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('inventory.index'))  # Redirect to index page after logout

@inventory_bp.route('/protected')
@login_required
def protected():
    return 'This is a protected route. You can only see this if you are logged in.'