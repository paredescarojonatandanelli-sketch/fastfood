from flask import Blueprint, render_template, request, jsonify, current_app
from extensions import db
from models import Category, Product, Order, OrderItem
from utils.whatsapp import generar_link_whatsapp

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/')
def index():
    return render_template('index.html')

@customer_bp.route('/menu')
def menu():
    categories = Category.query.filter_by(active=True).all()
    return render_template('menu.html', categories=categories)

@customer_bp.route('/cart')
def cart():
    return render_template('cart.html')

@customer_bp.route('/checkout', methods=['GET'])
def checkout_page():
    return render_template('checkout.html')

@customer_bp.route('/checkout', methods=['POST'])
def checkout_submit():
    data = request.get_json()

    if not data or not data.get('items'):
        return jsonify(success=False, error='El carrito está vacío.'), 400

    if not data.get('customer_name') or not data.get('customer_phone'):
        return jsonify(success=False, error='Nombre y teléfono son obligatorios.'), 400

    order_type = data.get('order_type')
    if order_type == 'delivery' and not data.get('address'):
        return jsonify(success=False, error='La dirección es obligatoria para delivery.'), 400

    # --- Recalcular precios desde la base de datos (nunca confiar en el navegador) ---
    subtotal = 0
    order_items_to_create = []

    for item in data['items']:
        product = Product.query.get(item.get('product_id'))
        quantity = item.get('quantity', 0)

        if not product or not product.active:
            return jsonify(success=False, error='Un producto ya no está disponible.'), 400

        if quantity <= 0:
            continue

        item_subtotal = product.price * quantity
        subtotal += item_subtotal

        order_items_to_create.append({
            'product_id': product.id,
            'product_name': product.name,
            'unit_price': product.price,
            'quantity': quantity,
            'subtotal': item_subtotal
        })

    if not order_items_to_create:
        return jsonify(success=False, error='El carrito está vacío.'), 400

    delivery_cost = current_app.config['DELIVERY_COST'] if order_type == 'delivery' else 0.0
    total = subtotal + delivery_cost

    # --- Crear el pedido ---
    new_order = Order(
        customer_name=data['customer_name'],
        customer_phone=data['customer_phone'],
        order_type=order_type,
        address=data.get('address'),
        reference=data.get('reference'),
        payment_method=data.get('payment_method'),
        notes=data.get('notes'),
        subtotal=subtotal,
        delivery_cost=delivery_cost,
        total=total,
        status='nuevo'
    )

    db.session.add(new_order)
    db.session.flush()

    for item_data in order_items_to_create:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item_data['product_id'],
            product_name=item_data['product_name'],
            unit_price=item_data['unit_price'],
            quantity=item_data['quantity'],
            subtotal=item_data['subtotal']
        )
        db.session.add(order_item)

    db.session.commit()

    return jsonify(success=True, order_id=new_order.id)

@customer_bp.route('/order/<int:order_id>/confirmation')
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    whatsapp_link = generar_link_whatsapp(order, current_app.config['WHATSAPP_NUMBER'])
    return render_template('order_confirmation.html', order=order, whatsapp_link=whatsapp_link)