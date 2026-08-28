from functools import wraps
from datetime import datetime, time
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from werkzeug.security import check_password_hash
from extensions import db
from models import Order , Product, Category
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        valid_username = username == current_app.config['ADMIN_USERNAME']
        valid_password = check_password_hash(current_app.config['ADMIN_PASSWORD_HASH'], password)

        if valid_username and valid_password:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template('admin/login.html', error='Usuario o contraseña incorrectos.')

    return render_template('admin/login.html')


@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    resumen = {
        'nuevo': Order.query.filter_by(status='nuevo').count(),
        'en_preparacion': Order.query.filter_by(status='en_preparacion').count(),
        'listo': Order.query.filter_by(status='listo').count(),
        'entregado': Order.query.filter_by(status='entregado').count(),
    }

    hoy_inicio = datetime.combine(datetime.today(), time.min)
    ventas_hoy = db.session.query(func.sum(Order.total)).filter(
        Order.created_at >= hoy_inicio,
        Order.status != 'cancelado'
    ).scalar() or 0.0

    pedidos_recientes = Order.query.order_by(Order.created_at.desc()).limit(10).all()

    return render_template(
        'admin/dashboard.html',
        resumen=resumen,
        ventas_hoy=ventas_hoy,
        pedidos_recientes=pedidos_recientes
    )
ESTADOS_PEDIDO = ['nuevo', 'confirmado', 'en_preparacion', 'listo', 'entregado', 'cancelado']


@admin_bp.route('/orders/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order, estados=ESTADOS_PEDIDO)


@admin_bp.route('/orders/<int:order_id>/status', methods=['POST'])
@login_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    nuevo_estado = request.form.get('status')

    if nuevo_estado in ESTADOS_PEDIDO:
        order.status = nuevo_estado
        db.session.commit()

    return redirect(url_for('admin.order_detail', order_id=order.id))
@admin_bp.route('/products')
@login_required
def products():
    productos = Product.query.order_by(Product.name).all()
    return render_template('admin/products.html', products=productos)


@admin_bp.route('/products/new', methods=['GET', 'POST'])
@login_required
def product_new():
    categories = Category.query.filter_by(active=True).all()

    if request.method == 'POST':
        nuevo_producto = Product(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price', 0)),
            category_id=int(request.form.get('category_id')),
            image=request.form.get('image'),
            active='active' in request.form
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', product=None, categories=categories)


@admin_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def product_edit(product_id):
    producto = Product.query.get_or_404(product_id)
    categories = Category.query.filter_by(active=True).all()

    if request.method == 'POST':
        producto.name = request.form.get('name')
        producto.description = request.form.get('description')
        producto.price = float(request.form.get('price', 0))
        producto.category_id = int(request.form.get('category_id'))
        producto.image = request.form.get('image')
        producto.active = 'active' in request.form
        db.session.commit()
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', product=producto, categories=categories)


@admin_bp.route('/products/<int:product_id>/toggle', methods=['POST'])
@login_required
def product_toggle(product_id):
    producto = Product.query.get_or_404(product_id)
    producto.active = not producto.active
    db.session.commit()
    return redirect(url_for('admin.products'))
@admin_bp.route('/categories')
@login_required
def categories():
    cats = Category.query.order_by(Category.name).all()
    return render_template('admin/categories.html', categories=cats)


@admin_bp.route('/categories/new', methods=['GET', 'POST'])
@login_required
def category_new():
    if request.method == 'POST':
        nueva_categoria = Category(
            name=request.form.get('name'),
            description=request.form.get('description'),
            active='active' in request.form
        )
        db.session.add(nueva_categoria)
        db.session.commit()
        return redirect(url_for('admin.categories'))

    return render_template('admin/category_form.html', category=None)


@admin_bp.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def category_edit(category_id):
    categoria = Category.query.get_or_404(category_id)

    if request.method == 'POST':
        categoria.name = request.form.get('name')
        categoria.description = request.form.get('description')
        categoria.active = 'active' in request.form
        db.session.commit()
        return redirect(url_for('admin.categories'))

    return render_template('admin/category_form.html', category=categoria)


@admin_bp.route('/categories/<int:category_id>/toggle', methods=['POST'])
@login_required
def category_toggle(category_id):
    categoria = Category.query.get_or_404(category_id)
    categoria.active = not categoria.active
    db.session.commit()
    return redirect(url_for('admin.categories'))