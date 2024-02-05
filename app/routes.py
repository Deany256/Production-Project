from app import app, db
from flask import render_template, request, redirect, url_for
from models import Product

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Add other routes as needed
