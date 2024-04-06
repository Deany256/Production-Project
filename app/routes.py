from flask import Blueprint, render_template
from .models import Product

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
