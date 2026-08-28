from datetime import datetime
from extensions import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    order_type = db.Column(db.String(20), nullable=False)  # 'recojo' o 'delivery'
    address = db.Column(db.String(255))
    reference = db.Column(db.String(255))
    payment_method = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.String(255))

    subtotal = db.Column(db.Float, nullable=False)
    delivery_cost = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, nullable=False)

    status = db.Column(db.String(20), default='nuevo')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación: un pedido tiene muchas líneas de detalle
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Order #{self.id}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    # Datos "congelados" al momento de la compra (no cambian aunque el producto cambie después)
    product_name = db.Column(db.String(100), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<OrderItem {self.product_name} x{self.quantity}>'